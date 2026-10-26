#!/usr/bin/env python3
"""Screen all 197 A-family train targets and run the unmodified proof routes.
Only scheduling, provenance, reporting and shared dependency reuse are added.
"""
import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
import csv
import hashlib
import html
import io
import json
from pathlib import Path
import re
import time
from run import HERE, ROOT, run, prepare_batch, batch_environment
from search import Budget

OUT = HERE/'generated/train_a_screen'
RESEARCH = HERE.parent/'research/train_a_methods'
CODE = ['batch.py','run.py','lean_pipeline.py','direct.py','expressions.py','search.py',
        'qgosper.py','lean/Extract.lean','lean/GaussianRules.lean','lean/Shared.lean']


def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def write(path,data): path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')


def screen():
    manifest = ROOT/'benchmark/splits/train.jsonl'
    train = [json.loads(l) for l in manifest.read_text().splitlines() if l.strip()]
    selected = [r for r in train if r['family_id']=='A']
    notes = json.loads((RESEARCH/'annotations.json').read_text())
    plans = json.loads((RESEARCH/'plans.json').read_text())
    assert digest(manifest)==notes['input_train_manifest_sha256']
    assert digest(RESEARCH/'annotations.json')==plans['annotations_sha256']
    note_map = {r['id']:r for r in notes['entries']}
    plan_map = {r['id']:r for r in plans['entries']}
    assert len(selected)==197 and set(note_map)==set(r['id'] for r in selected)
    rows=[]
    for row in selected:
        identity=row['id']; note=note_map[identity]; plan=plan_map[identity]
        source=ROOT/'benchmark'/row['lean_path']
        formula=ROOT/'benchmark'/row['md_path']
        assert source.resolve().is_relative_to((ROOT/'benchmark/lean/Benchmark/Statements/Train').resolve())
        assert formula.resolve().is_relative_to((ROOT/'benchmark/formulas/train').resolve())
        assert digest(source)==row['lean_sha256'] and digest(formula)==row['md_sha256']
        declaration=source.read_text().split('theorem statement',1)[1].split(':= by',1)[0]
        features=[name for pattern,name in [
            (r'\bphi\b','phi'),(r'\bpochList\b','pochList'),(r'\bgaussianInt\b','gaussianInt'),
            (r'\bgaussian\b','gaussian'),(r'Finset\.Icc','Icc'),(r'Finset\.range','range'),
            (r'∧','conjunction'),(r'\bif\b','piecewise'),(r'ℤ','integer_indices_or_powers'),
            (r'\bwellPoised\b','wellPoised')]
            if re.search(pattern,declaration)]
        current=[{'W':'target_first_order','G':'direct_q_gosper'}[c]
                 for c in note['route_ids'] if c in ('W','G')]
        p1=any(c['mechanism_id']=='P1' for c in plan['component_roles'])
        rows.append({'id':identity,'order':note['train_a_order'],
            'structure':note['structure'],'features':features,
            'primary_mechanism':plan['primary_mechanism'],
            'candidate_routes':current,'candidate_components':note['route_ids'],
            'screening_status':'current_route_candidate_unverified' if current else
                'other_p1_route_candidate_unverified' if p1 else 'no_current_route_listed_not_excluded',
            'applicability_basis':note['applicability_basis'],
            'pending_mathematical_checks':note['pending_checks'],
            'screening_basis':'existing per-formula structure review; not an algorithmic applicability proof',
            'source_path':str(source.relative_to(ROOT)),'source_sha256':row['lean_sha256'],
            'formula_path':str(formula.relative_to(ROOT)),'formula_sha256':row['md_sha256']})
    return rows


def outcome(report):
    status=report['status']; error=report.get('error','')
    if status=='proved': return 'proved','complete','原始 Lean 目标完整通过'
    if status=='dependency_compile_failed':return 'shared_dependency_failure','environment',error[:500]
    if status=='representation_gap':
        # Replacement of broad proof imports with verified shared definitions is
        # intentionally conservative. Missing original definitions are environment
        # support gaps, never mathematical evidence against the method.
        if any(t in error for t in ('Unknown identifier','Unknown constant','unknown identifier',
                                     'Function expected','failed to synthesize')):
            return 'definition_context_gap','elaboration',error[:500]
        match=re.search(r'Unsupported expression in P1 frontend: ([^\n]+)',error)
        if match:return 'expression_export_gap','expression_export',match.group(1)[:500]
        return 'elaboration_or_export_gap','expression_export',error[:500]
    if status=='unsupported_structure':return 'route_structure_gap','routing',error[:500]
    if status in ('unsupported_expression','unsupported_declaration'):return status,'expression_export',error[:500]
    if status=='construction_failed':
        if 'timeout' in error:return 'timeout','symbolic_construction',error[:500]
        if 'representation_gap' in error:return 'symbolic_representation_gap','shift_conversion',error[:500]
        return status,'symbolic_construction',error[:500]
    if status in ('resource_exhausted','timeout','no_q_hypergeometric_antidifference'):
        return status,'symbolic_construction',report.get('construction',{}).get('reason','')
    if status=='domain_unresolved':return status,'certificate_translation',error[:500]
    if status in ('lean_failed','axiom_audit_failed'):
        return status,'lean_verification',report.get('verification',{}).get('lean',{}).get('output','')[-1000:]
    return status,'unclassified',error[:500]


def task(row,prepared,seconds):
    started=time.monotonic()
    report=run(row['id'],budget=Budget(seconds=seconds),prepared=prepared,output_root=OUT/'runs')
    work=OUT/'runs'/row['id'];work.mkdir(parents=True,exist_ok=True)
    write(work/'report.json',report)
    category,stage,detail=outcome(report)
    return dict(row,run_status=report['status'],outcome=category,failure_stage=stage,
                detail=detail,actual_route=report.get('branch'),
                elapsed_seconds=round(time.monotonic()-started,3),
                reached_symbolic_backend='construction' in report,
                certificate_constructed='q_gosper_certificate_constructed' in report.get('stages',[]),
                report_path=str((work/'report.json').relative_to(OUT)),
                report_sha256=digest(work/'report.json'),
                proof_path=(str(Path(report['verification']['proof_file']).relative_to(OUT))
                            if report['status']=='proved' else None))


def render(rows,summary):
    write(OUT/'table.json',{'scope':'197 A-family train only','records':rows})
    write(OUT/'summary.json',summary)
    fields=['order','id','structure','candidate_routes','screening_status','applicability_basis',
            'pending_mathematical_checks','features','actual_route','run_status','outcome',
            'failure_stage','detail','report_path','proof_path','source_sha256']
    stream=io.StringIO();writer=csv.DictWriter(stream,fieldnames=fields);writer.writeheader()
    for row in rows:
        writer.writerow({k:'; '.join(row[k]) if isinstance(row.get(k),list) else row.get(k,'') for k in fields})
    (OUT/'table.csv').write_text('\ufeff'+stream.getvalue())
    e=html.escape
    body=[]
    for r in rows:
        links=f'<a href="{e(r["report_path"])}">运行日志</a>'
        if r['proof_path']:links+=f' · <a href="{e(r["proof_path"])}">Lean证明</a>'
        body.append('<tr>'+''.join('<td>'+cell+'</td>' for cell in [str(r['order']),e(r['id']),
            e(r['structure']),e(', '.join(r['candidate_routes']) or '未列出现有两分支'),
            e(r['applicability_basis'])+'<br><small>待核：'+e(r['pending_mathematical_checks'])+'</small>',
            e(r['outcome'])+'<br><small>'+e(r['failure_stage'])+'</small>',
            '<details><summary>细节</summary><pre>'+e(r['detail'])+'</pre></details>'+links])+'</tr>')
    page='''<!doctype html><html lang="zh"><meta charset="utf-8"><title>P1：197 条 train 筛选与实测</title>
<style>body{font:15px/1.6 system-ui;margin:28px;color:#172033}table{border-collapse:collapse;width:100%}th,td{padding:10px;border:1px solid #ddd;text-align:left;vertical-align:top}th{background:#eef2f8;position:sticky;top:0}small{color:#526078}pre{white-space:pre-wrap;max-width:500px}input{padding:10px;width:70%}a{color:#245fc9}</style>
<h1>P1：197 条 train 筛选与实测</h1><p>结构候选不等于数学适用性已证明；实现缺口不等于恒等式不可证明。全部条目实际调用同一 P1 入口，无人工证书或证明提示。共享依赖只编译一次并逐项核对哈希。</p>'''
    page+='<p>'+e(json.dumps(summary['outcomes'],ensure_ascii=False))+'</p>'
    page+='<p><a href="table.csv">CSV</a> · <a href="table.json">JSON</a> · <a href="summary.json">统计与来源</a></p>'
    page+='<input id="query" placeholder="输入公式 ID、结构、失败阶段或关键词筛选"><p id="count"></p><table><thead><tr>'
    page+=''.join('<th>'+x+'</th>' for x in ['序号','公式','结构','现有分支候选','适用性依据','实际结果','证据'])
    page+='</tr></thead><tbody>'+''.join(body)+'''</tbody></table><script>
const rows=[...document.querySelectorAll('tbody tr')],input=document.getElementById('query');
function filter(){let n=0;for(const r of rows){r.hidden=!r.textContent.toLowerCase().includes(input.value.toLowerCase());if(!r.hidden)n++}document.getElementById('count').textContent=`显示 ${n} / ${rows.length} 条`;}input.addEventListener('input',filter);filter();</script></html>'''
    (OUT/'index.html').write_text(page)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workers',type=int,default=4)
    parser.add_argument('--seconds',type=float,default=30)
    args=parser.parse_args()
    if not 1<=args.workers<=8 or not 0<args.seconds<=600:parser.error('invalid resource budget')
    OUT.mkdir(parents=True,exist_ok=True)
    rows=screen();write(OUT/'screening.json',rows)
    hashes={name:digest(HERE/name) for name in CODE}
    prepared=prepare_batch(OUT/'shared');write(OUT/'dependencies.json',{k:v for k,v in prepared.items() if k!='env'})
    results=[];started=time.monotonic()
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures={pool.submit(task,row,prepared,args.seconds):row['id'] for row in rows}
        for future in as_completed(futures):
            result=future.result();results.append(result)
            print(f'{len(results)}/197 {result["id"]}: {result["outcome"]}',flush=True)
            write(OUT/'progress.json',{'finished':len(results),'total':len(rows),
                                      'outcomes':dict(Counter(r['outcome'] for r in results))})
    results.sort(key=lambda r:r['order'])
    assert hashes=={name:digest(HERE/name) for name in CODE},'code changed during batch'
    batch_environment(prepared)
    assert len(results)==197 and len({r['id'] for r in results})==197
    summary={'scope':'197 A-family train; no test files read','total':len(results),
        'attempted':len(results),'workers':args.workers,'symbolic_seconds_per_target':args.seconds,
        'elapsed_seconds':round(time.monotonic()-started,3),
        'outcomes':dict(Counter(r['outcome'] for r in results)),
        'screening':dict(Counter(r['screening_status'] for r in results)),
        'existing_primary_mechanism':dict(Counter(str(r['primary_mechanism']) for r in results)),
        'symbolic_backend_results':sum(r['reached_symbolic_backend'] for r in results),
        'certificates_constructed':sum(r['certificate_constructed'] for r in results),
        'proved':[r['id'] for r in results if r['outcome']=='proved'],
        'code_sha256':hashes,'train_manifest_sha256':digest(ROOT/'benchmark/splits/train.jsonl'),
        'annotations_sha256':digest(RESEARCH/'annotations.json'),
        'plans_sha256':digest(RESEARCH/'plans.json'),
        'notes':['screening is inherited structural evidence, not proof of algorithm applicability',
                 'failures before symbolic construction do not imply q-Gosper failure',
                 'no algorithm branch or proof rule extended during this batch']}
    render(results,summary)
    print(json.dumps(summary,ensure_ascii=False,indent=2))


if __name__=='__main__':main()
