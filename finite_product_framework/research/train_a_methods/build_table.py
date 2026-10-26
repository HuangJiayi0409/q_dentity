#!/usr/bin/env python3
"""Build/check the A-train method table without opening test or source-family pages.

Usage: python3 build_table.py [--check]
Edit annotations.json (evidence), plans.json (roles), architecture.json (mechanisms),
and methods.json (component specifications), then rebuild.
All generated artifacts remain in this directory. No CAS or Lean is invoked.
"""
import argparse
import csv
import hashlib
import html
import io
import json
import os
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
BENCH = ROOT / 'benchmark'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def encode(data):
    return json.dumps(data, ensure_ascii=False, indent=2) + '\n'


def e(value):
    return html.escape(str(value), quote=True)


def source_file(relative, allowed, expected_sha):
    path = (BENCH / relative).resolve()
    assert path.is_relative_to((BENCH / allowed).resolve()), f'Outside train: {relative}'
    raw = path.read_bytes()
    assert digest(raw) == expected_sha, f'Source hash changed: {relative}'
    return raw.decode(), os.path.relpath(path, HERE)


def collect():
    annotations = json.loads((HERE / 'annotations.json').read_text())
    methods = json.loads((HERE / 'methods.json').read_text())['methods']
    architecture = json.loads((HERE / 'architecture.json').read_text())
    plans = json.loads((HERE / 'plans.json').read_text())
    assert plans['annotations_sha256'] == digest((HERE / 'annotations.json').read_bytes()), 'Re-review plans after annotation changes'
    plan_by_id = {p['id']: p for p in plans['entries']}
    assert len(plan_by_id) == len(plans['entries']) == 197
    manifest = (BENCH / 'splits/train.jsonl').read_bytes()
    assert digest(manifest) == annotations['input_train_manifest_sha256'], 'Re-review changed train manifest'
    selected = [json.loads(line) for line in manifest.splitlines() if line.strip()]
    selected = [row for row in selected if row['family_id'] == 'A']
    indexed = {row['id']: row for row in selected}
    notes = annotations['entries']
    assert len(indexed) == len(selected) == len(notes) == 197
    assert len({row['id'] for row in notes}) == 197
    assert set(indexed) == {row['id'] for row in notes}, 'Missing/extra A train IDs'
    assert set(plan_by_id) == set(indexed), 'Plan scope differs from A train'
    fields = ('core_proof_method', 'applicability_conditions', 'cas_entry',
              'remaining_obligations', 'lean_verification')
    for method in methods.values():
        assert all(method.get(key) for key in fields)
    for mechanism in architecture['mechanisms'].values():
        assert all(mechanism.get(key) for key in fields)
    records = []
    for order, note in enumerate(notes, 1):
        assert note['train_a_order'] == order
        item = indexed[note['id']]
        assert item['id'] == selected[order - 1]['id'], 'Order drift'
        assert note['route_ids'] and len(set(note['route_ids'])) == len(note['route_ids'])
        assert all(code in methods for code in note['route_ids'])
        plan = plan_by_id[note['id']]
        assert plan['primary_mechanism'] is None or plan['primary_mechanism'] in architecture['mechanisms']
        components = plan['component_roles']
        assert len(components) == len(note['route_ids'])
        assert {c['component_id'] for c in components} == set(note['route_ids']), 'Lost/duplicated old candidate'
        for c in components:
            assert c['role'] in architecture['roles'] and c['reason']
            assert c['mechanism_id'] is None or c['mechanism_id'] in architecture['mechanisms']
        main = [c for c in components if c['role'] == 'main_branch']
        if plan['primary_mechanism'] is None:
            assert not main and plan['main_component'] is None and not plan['alternative_plans']
        else:
            assert len(main) == 1 and main[0]['component_id'] == plan['main_component']
            assert main[0]['mechanism_id'] == plan['primary_mechanism']
        alternative_codes = {c['component_id'] for c in components if c['role'] == 'alternative_pipeline'}
        assert alternative_codes == {code for a in plan['alternative_plans'] for code in a['component_ids']}
        for a in plan['alternative_plans']:
            assert a['mechanism_id'] in architecture['mechanisms'] and a['mechanism_id'] != plan['primary_mechanism']
            assert a['condition'] and a['status']
        assert plan['steps'] and plan['first_action']
        assert all(note.get(key) for key in ('bases', 'structure', 'applicability_basis', 'pending_checks', 'review_status'))
        # This initial review intentionally makes no empirical success claim.
        assert note['tool_trial_status'] == 'not_run' and note['tool_trials'] == [], 'Add trial evidence schema before recording experiments'
        md, md_link = source_file(item['md_path'], 'formulas/train', item['md_sha256'])
        lean, lean_link = source_file(item['lean_path'], 'lean/Benchmark/Statements/Train', item['lean_sha256'])
        parts = md.split('$$')
        assert len(parts) >= 3, f'Missing displayed formula: {item["id"]}'
        theorem_start = lean.index('theorem statement')
        theorem_end = lean.index(':= by', theorem_start)
        theorem = lean[theorem_start:theorem_end].strip()
        selected_methods = [methods[code] for code in note['route_ids']]
        history = next((line for line in md.splitlines() if line.startswith('**证明算法状态')), '')
        feature_flags = []
        for token, label in [('Tendsto', '包含解析极限'), ('terminatesAt', '终止来源需分支'),
                             ('List K', '参数列表长度任意'), ('Complex.exp', '复指数表示桥接'),
                             ('∧', '合取或复合域条件'), ('if ', '显式分段或零项保护')]:
            if token in theorem:
                feature_flags.append(label)
        record = dict(note, name=item['name'], split='train', family_id='A',
                      formula_latex=parts[1].strip(), lean_statement=theorem,
                      source_conditions='\n'.join(line for line in md.splitlines() if line.startswith('- **')),
                      formula_path=str(Path('benchmark') / item['md_path']),
                      lean_path=str(Path('benchmark') / item['lean_path']),
                      formula_link=md_link, lean_link=lean_link,
                      formula_sha256=item['md_sha256'], lean_sha256=item['lean_sha256'],
                      source_ids=item['source_ids'], representative_source=item['representative_source'],
                      lexical_lean_flags=feature_flags,
                      evidence_level='公式结构初审；非移位比计算或算法适用性证明',
                      legacy_primary_route=note['route_ids'][0],
                      legacy_candidate_order_note='route_ids/candidate_methods保留原扁平候选追溯；不再用列表位置判断当前角色，以proof_plan为准。',
                      proof_plan=plan,
                      candidate_methods=[dict(route_id=code, **methods[code]) for code in note['route_ids']],
                      legacy_proposed_first_experiment=selected_methods[0]['cas_entry'] + '；本条先处理：' + note['pending_checks'],
                      proposed_first_experiment=(methods[plan['main_component']]['cas_entry'] + '；' if plan['main_component'] else '') + plan['first_action'],
                      legacy_annotation_unverified=history,
                      tool_trial_result='未试验；无本轮CAS输入、输出、耗时或成功记录',
                      lean_proof_result='本轮未生成或验证目标证明')
        for evidence in record.get('definition_evidence', []):
            relative = Path(evidence['path'])
            assert relative.parent == Path('benchmark/lean/Benchmark')
            assert relative.name.endswith('Definitions.lean')
            path = ROOT / relative
            raw = path.read_bytes()
            assert digest(raw) == evidence['sha256'], f'Definition changed: {relative}'
            assert evidence['excerpt'] in raw.decode()
            assert raw.decode().splitlines()[evidence['line'] - 1].startswith('def ' + evidence['declaration'])
            evidence['link'] = os.path.relpath(path, HERE)
        records.append(record)
    summary = dict(schema_version=2, date=plans['date'], scope=annotations['scope'], record_count=len(records),
                   review_basis=annotations['review_basis'],
                   input_train_manifest_sha256=digest(manifest),
                   annotations_sha256=digest((HERE / 'annotations.json').read_bytes()),
                   methods_sha256=digest((HERE / 'methods.json').read_bytes()),
                   architecture_sha256=digest((HERE / 'architecture.json').read_bytes()),
                   plans_sha256=digest((HERE / 'plans.json').read_bytes()),
                   primary_mechanism_counts=dict(sorted(Counter(r['proof_plan']['primary_mechanism'] or 'UNRESOLVED' for r in records).items())),
                   component_role_counts=dict(sorted(Counter(c['role'] for r in records for c in r['proof_plan']['component_roles']).items())),
                   legacy_primary_route_counts=dict(sorted(Counter(r['legacy_primary_route'] for r in records).items())),
                   legacy_candidate_route_counts=dict(sorted(Counter(c for r in records for c in r['route_ids']).items())),
                   count_meaning='三个工程主机制的候选分配；待确定条目单列。分支/内部调用/桥接不增加主机制数，不表示覆盖或互斥。',
                   tool_trials_run=0, lean_proofs_generated=0,
                   shared_definition_files_checked=len({x['path'] for r in records for x in r.get('definition_evidence', [])}),
                   exclusions='不读取test清单、test公式、test statement；不从旧全库证据导入成功状态')
    return records, methods, summary, architecture


def role_text(record, roles, methods, architecture):
    return '；'.join(architecture['roles'][c['role']] + '：' + methods[c['component_id']]['name'] + '（' + c['reason'] + '）'
                    for c in record['proof_plan']['component_roles'] if c['role'] in roles)


def csv_table(records, methods, architecture):
    buf = io.StringIO(newline='')
    writer = csv.writer(buf)
    writer.writerow(['序号', '公式ID', '名称', '基数结构', '结构', '主证明机制', '构造分支', '内部调用', '替代完整路线', '组织与辅助阶段', '主流程步骤',
                     '适用性依据（结构初审）', '适用条件与待核项', '拟议首次试验', '工具试验结果',
                     'Lean证明结果', '公式路径', 'Lean路径', '公式SHA256', 'LeanSHA256'])
    for r in records:
        writer.writerow([r['train_a_order'], r['id'], r['name'], r['bases'], r['structure'],
                         architecture['mechanisms'][r['proof_plan']['primary_mechanism']]['name'] if r['proof_plan']['primary_mechanism'] else '主流程待确定',
                         role_text(r, {'main_branch', 'alternative_branch'}, methods, architecture),
                         role_text(r, {'internal_call'}, methods, architecture),
                         role_text(r, {'alternative_pipeline'}, methods, architecture),
                         role_text(r, {'required_stage', 'conditional_stage', 'orchestration', 'diagnostic_only'}, methods, architecture),
                         ' → '.join(r['proof_plan']['steps']),
                         r['applicability_basis'], r['pending_checks'], r['proposed_first_experiment'],
                         r['tool_trial_result'], r['lean_proof_result'], r['formula_path'], r['lean_path'],
                         r['formula_sha256'], r['lean_sha256']])
    return '\ufeff' + buf.getvalue()


def html_table(records, methods, summary, architecture):
    pieces = ['''<!doctype html><html lang="zh-CN"><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>A族 train · 方法对应表</title>
<style>
body{font:15px/1.65 system-ui,sans-serif;color:#16283b;background:#f5f7fa;margin:24px}
h1{font-size:26px}a{color:#135fa4}header,section{background:white;padding:20px;border-radius:8px;margin-bottom:18px}
input,select{padding:10px;border:1px solid #9aabbd;border-radius:5px;font:inherit;margin:5px}input{width:min(600px,85%)}
.scroll{overflow:auto}table{border-collapse:collapse;width:100%;background:white}th,td{padding:12px;border:1px solid #d9e1ea;text-align:left;vertical-align:top;min-width:170px}th{background:#e5edf5}
th:first-child,td:first-child{min-width:40px}code{overflow-wrap:anywhere;font-size:12px}pre{white-space:pre-wrap;overflow-wrap:anywhere;font-size:13px;background:#f3f6fa;padding:12px}
details{margin:8px 0}summary{cursor:pointer;color:#155986}.muted{color:#58697b}.pill{display:inline-block;background:#e7eef8;padding:2px 8px;border-radius:5px;margin:2px}td p{margin:5px 0}
</style><header><h1>A族 train · 结构—方法对应表</h1>''',
              f'<p>{summary["date"]} · <strong>197 条训练公式</strong> · 初始结构审阅快照（当时工具试验 0 次、完整证明 0 条）</p>',
              '<p><strong>P1数学复审：</strong><a href="../../p1/research/applicability/index.html">51条初筛候选的适用性、条件与转交建议</a>。<strong>历史 P1 实测：</strong><a href="../../p1/generated/train_a_screen/index.html">197 条逐项运行结果、失败阶段与证明</a>。下表保留初始候选审阅，not_run 仅指该历史快照。</p>',
              '<p><strong>已按三种主证明机制重新分层</strong>：差分/望远镜/递推；有限展开/系数/卷积；重编号/配对/直接代数。旧16种标签转为内部构造、调用、替代或附加阶段，不再称为16种独立方法。</p>',
              '<p>三种机制是工程组织方式，可解范围仍可能重叠。尚未逐条计算移位比或运行CAS，所有计划仍是结构候选。5条任意维数根系式缺少统一归纳步，主流程待确定。</p>',
              '<p>原有 A 族归属保留。任意维数、任意参数列表、解析极限与特殊输入另记待核项。历史算法状态只作未复核原文展示，不计入工具试验结果。</p>',
              '<p><a href="table.csv">下载 CSV</a> · <a href="table.json">完整 JSON</a> · <a href="architecture.json">主流程架构</a> · <a href="plans.json">197条分层计划</a> · <a href="annotations.json">原结构审阅</a> · <a href="methods.json">组件规格</a></p>',
              '<label>搜索 <input id="query" placeholder="名称、ID、结构、基数或待核条件"></label><label>主机制 <select id="mechanism"><option value="">全部</option>']
    for code, mechanism in architecture['mechanisms'].items():
        pieces.append(f'<option value="{code}">{code} · {e(mechanism["name"])}</option>')
    pieces.append('<option value="UNRESOLVED">主流程待确定</option></select></label><label>构造/辅助组件 <select id="route"><option value="">全部</option>')
    for code, m in methods.items():
        pieces.append(f'<option value="{e(code)}">{e(code)} · {e(m["name"])}</option>')
    pieces += ['</select></label><p id="count">显示 197 / 197</p></header>',
               '<section><h2>主流程与共享关系</h2><p>P1在内部区分直接原差分、目标引导相邻关系、一般阶递推、多指标/多基消元和定义递推比较。P2归约出的核可以调用P1。P3可直接闭合，也可以调用已证基本求和值。N是外层归纳组织，K和LIMIT是桥接阶段。</p>']
    for code, mechanism in architecture['mechanisms'].items():
        pieces.append(f'<details id="pipeline-{code}"><summary>{code} · {e(mechanism["name"])}：主机制候选 {summary["primary_mechanism_counts"].get(code, 0)} 条</summary><p>{e(mechanism["description"])}</p><p>{e(mechanism["core_proof_method"])}</p>')
        for branch in mechanism['branches']:
            pieces.append(f'<p><strong>{e(branch["name"])}</strong>（{e(", ".join(branch["components"]))}）：{e(branch["relationship"])}</p>')
        pieces.append('</details>')
    pieces += [f'<p>主流程待确定：{summary["primary_mechanism_counts"].get("UNRESOLVED", 0)} 条。固定维数诊断不算泛维目标的完整替代路线。</p>',
               '<details><summary>角色定义</summary>']
    for role, label in architecture['roles'].items():
        pieces.append(f'<p><code>{e(role)}</code>：{e(label)}</p>')
    pieces += ['<p>“同一主流程内的备选分支”只替换局部构造；“可替代主流程”以原目标为对象，仍须核对全套条件。必要桥接不因换后端而省略。</p></details></section>',
               '<section><details><summary>使用说明与组件规格（保留旧标签追溯）</summary>',
               '<p>annotations.json保存原结构依据；plans.json明确每条候选的角色；architecture.json定义主机制；methods.json保留组件规格。修改后运行 <code>python3 build_table.py</code>，用 <code>--check</code>只读校验。输入变化需重新审阅，脚本不修改benchmark。</p>',
               '<p>此初始快照工具试验状态保留为 not_run；实际 P1 试验另见上方实测表。试验应保存版本、原始输入/输出、参数、预算、耗时、结论、边界义务及 Lean 验证结果；数值样本或旧占位框架不能计为完整证明。开始登记实验时需扩展试验记录校验，而非手改生成表。</p>']
    labels = [('core_proof_method', '完整流程'), ('applicability_conditions', '适用条件'), ('cas_entry', '工具计算任务'),
              ('remaining_obligations', '剩余义务'), ('lean_verification', 'Lean组装方式')]
    for code, m in methods.items():
        candidates = summary['legacy_candidate_route_counts'].get(code, 0)
        pieces.append(f'<details id="method-{code}"><summary>{code} · {e(m["name"])}：出现于 {candidates} 条的组件列表</summary><p>{e(architecture["component_levels"][code])}。角色以逐条计划为准。{e(m["tools"])}</p>')
        for field, label in labels:
            pieces.append(f'<p><b>{label}：</b>{e(m[field])}</p>')
        pieces.append('<p>' + ' · '.join(f'<a href="{e(url)}" rel="noreferrer">参考 {i}</a>' for i, url in enumerate(m['references'], 1)) + '</p></details>')
    pieces += ['</details></section><div class="scroll"><table><thead><tr><th>序号</th><th>公式</th><th>结构</th><th>主机制与构造分支</th><th>内部调用</th><th>替代主流程</th><th>组织与辅助阶段</th><th>适用性依据</th><th>待核项与试验</th><th>工具试验结果</th></tr></thead><tbody>']
    for r in records:
        # All source text is escaped. No formula/Lean text is interpolated into JavaScript.
        plan = r['proof_plan']
        mechanism_id = plan['primary_mechanism'] or 'UNRESOLVED'
        pieces.append(f'<tr data-routes="{e(" ".join(r["route_ids"]))}" data-mechanism="{mechanism_id}"><td>{r["train_a_order"]}</td><td><strong>{e(r["name"])}</strong><p><code>{e(r["id"])}</code></p>')
        pieces.append(f'<p><a href="{e(r["formula_link"])}">训练公式</a> · <a href="{e(r["lean_link"])}">Lean statement</a></p>')
        for title, value in [('公式（LaTeX原文）', r['formula_latex']), ('Lean目标及假设', r['lean_statement']),
                             ('原公式条件摘录', r['source_conditions']), ('历史状态原文（未复核）', r['legacy_annotation_unverified'])]:
            pieces.append(f'<details><summary>{e(title)}</summary><pre>{e(value or "无")}</pre></details>')
        for evidence in r.get('definition_evidence', []):
            pieces.append(f'<details><summary>已抽核定义：{e(evidence["declaration"])}</summary><a href="{e(evidence["link"])}">共享定义文件，第 {evidence["line"]} 行</a><pre>{e(evidence["excerpt"])}</pre></details>')
        pieces.append(f'</td><td>{e(r["structure"])}<p class="pill">{e(r["bases"])}</p></td><td>')
        if plan['primary_mechanism']:
            pieces.append(f'<strong><a href="#pipeline-{mechanism_id}">{mechanism_id} · {e(architecture["mechanisms"][mechanism_id]["name"])}</a></strong>')
        else:
            pieces.append('<strong>主流程待确定</strong><p>缺少统一维数归纳步；不以固定维数工具作为完整方法。</p>')
        def component_html(role_set):
            parts = []
            for c in plan['component_roles']:
                if c['role'] not in role_set:
                    continue
                code = c['component_id']
                parts.append(f'<p>{e(architecture["roles"][c["role"]])}：<a href="#method-{code}">{e(methods[code]["name"])}</a></p><p class="muted">{e(c["reason"])}</p>')
            return ''.join(parts) or '<span class="muted">未指定</span>'
        pieces.append(component_html({'main_branch', 'alternative_branch'}))
        pieces.append('<details><summary>完整计划步骤</summary><ol>' + ''.join(f'<li>{e(step)}</li>' for step in plan['steps']) + '</ol></details>')
        pieces.append('</td><td>' + component_html({'internal_call'}))
        pieces.append('</td><td>' + component_html({'alternative_pipeline'}))
        pieces.append('</td><td>' + component_html({'required_stage', 'conditional_stage', 'orchestration', 'diagnostic_only'}))
        pieces.append(f'</td><td>{e(r["applicability_basis"])}<p class="muted">{e(r["evidence_level"])}</p></td>')
        pieces.append(f'<td>{e(r["pending_checks"])}<details><summary>拟议首次试验</summary>{e(r["proposed_first_experiment"])}</details></td>')
        pieces.append(f'<td>{e(r["tool_trial_result"])}<p class="muted">{e(r["lean_proof_result"])}</p></td></tr>')
    pieces += ['''</tbody></table></div><script>
const rows=[...document.querySelectorAll('tbody tr')];
const query=document.getElementById('query'), route=document.getElementById('route'), mechanism=document.getElementById('mechanism');
const haystacks=rows.map(row=>row.textContent.toLowerCase());
function filter(){let count=0;const q=query.value.trim().toLowerCase(),r=route.value,m=mechanism.value;
rows.forEach((row,i)=>{const show=(!q||haystacks[i].includes(q))&&(!r||row.dataset.routes.split(' ').includes(r))&&(!m||row.dataset.mechanism===m);row.hidden=!show;if(show)count++;});
document.getElementById('count').textContent=`显示 ${count} / ${rows.length}`;}
query.addEventListener('input',filter);route.addEventListener('change',filter);mechanism.addEventListener('change',filter);
document.querySelectorAll('a[href^="#method-"],a[href^="#pipeline-"]').forEach(a=>a.addEventListener('click',()=>{
const target=document.querySelector(a.getAttribute('href'));if(target){for(let p=target;p;p=p.parentElement){if(p.tagName==='DETAILS')p.open=true;}}
}));
</script></html>''']
    return '\n'.join(pieces)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    records, methods, summary, architecture = collect()
    outputs = {'table.json': encode(dict(schema_version=2, summary=summary, architecture=architecture, entries=records)),
               'table.csv': csv_table(records, methods, architecture), 'index.html': html_table(records, methods, summary, architecture),
               'summary.json': encode(summary)}
    for name, content in outputs.items():
        path = HERE / name
        if args.check:
            assert path.read_bytes() == content.encode(), f'Stale generated file: {name}'
        else:
            path.write_bytes(content.encode())
    print(encode(dict(action='checked' if args.check else 'built', records=len(records),
                      exact_A_train_membership=True, source_hashes_verified=394,
                      test_files_read=0, tool_trials_run=0,
                      primary_mechanism_counts=summary['primary_mechanism_counts'], outputs=list(outputs))))


if __name__ == '__main__':
    main()
