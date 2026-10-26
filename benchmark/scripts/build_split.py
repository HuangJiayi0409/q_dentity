#!/usr/bin/env python3
"""Reproducible problem-only split. --check compares without writing files."""
import argparse
from collections import Counter
import csv
import hashlib
import io
import json
from pathlib import Path
import random
import re

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
SEED = 20261018


def encode(value):
    return json.dumps(value, ensure_ascii=False, indent=2) + '\n'


def build():
    outputs, hashes = {}, {}

    def source(path):
        raw = (REPO / path).read_bytes()
        hashes[path] = hashlib.sha256(raw).hexdigest()
        return raw.decode()

    catalog = json.loads(source('round2_identity_catalog/data/catalog.json'))
    classes = json.loads(source('benchmark_four_families/inputs/classification.json'))
    families = json.loads(source('benchmark_four_families/inputs/families.json'))
    group_data = json.loads(source('benchmark_four_families/inputs/groups.json'))
    difficulty = json.loads(source('benchmark_four_families/inputs/difficulty_trial_v2_annotations.json'))
    sources = json.loads(source('round2_identity_catalog/data/normalized_sources.json'))
    by_id = {x['id']: x for x in classes}
    levels = {x['id']: x['level'] for x in difficulty['annotations']}
    src = {x['source_id']: x for x in sources}
    assert len(catalog) == len(by_id) == len(levels) == 446
    assert {x['id'] for x in catalog} == set(by_id) == set(levels)
    counts = Counter(x['primary_family'] for x in classes)
    assert dict(counts) == {'A': 253, 'C': 67, 'F': 74, 'G': 52}
    assert Counter(levels.values()) == {'低': 84, '中': 255, '高': 107}
    # Integer quotas minimizing squared distance from proportional allocation.
    targets = dict.fromkeys(sorted(counts), 0)
    for _ in range(100):
        family = min(targets, key=lambda f: (446*(2*targets[f]+1)-200*counts[f], f))
        targets[family] += 1
    groups = group_data['groups']
    group_for = {i: g['group_id'] for g in groups for i in g['members']}
    assert sum(len(g['members']) for g in groups) == len(group_for) == 446
    assert set(group_for) == set(by_id)
    for g in groups:
        assert g['family_counts'] == Counter(by_id[i]['primary_family'] for i in g['members'])
    rng = random.Random(SEED)
    for attempt in range(10000):
        order = list(groups)
        rng.shuffle(order)
        remaining, selected = targets.copy(), set()
        for g in order:
            if all(n <= remaining[f] for f, n in g['family_counts'].items()):
                selected.update(g['members'])
                for f, n in g['family_counts'].items():
                    remaining[f] -= n
        if not any(remaining.values()):
            break
    else:
        raise RuntimeError('No whole-group allocation meets exact quotas')
    assert len(selected) == 100
    for g in groups:
        assert len(selected.intersection(g['members'])) in (0, len(g['members']))
    for edge in group_data['edges']:
        assert (edge['source'] in selected) == (edge['target'] in selected)

    # Keep local object definitions; do not export algorithm/proof annotations.
    local_definitions = {}
    for path in sorted((REPO / 'round2_identity_catalog/families').glob('*.md')):
        body = source(str(path.relative_to(REPO)))
        sections = list(re.finditer(r'^## (FQI-\S+) · .*$', body, re.M))
        for j, match in enumerate(sections):
            section = body[match.end():sections[j+1].start() if j+1 < len(sections) else len(body)]
            local_definitions[match[1]] = re.findall(r'^局部定义：.*$', section, re.M)

    names = {f['id']: f['name'] for f in families}
    manifests = {'train': [], 'test': []}
    problems = []
    definition_references = set()
    for item in sorted(catalog, key=lambda x: x['id']):
        identity = item['id']
        split = 'test' if identity in selected else 'train'
        family = by_id[identity]['primary_family']
        variants = []
        for domain in item['domain_variants']:
            original = src[domain['source_id']]
            record = original['source_record']
            definitions = original.get('definition_files', [])
            definition_references.update(definitions)
            variants.append({**domain, 'formula_latex': original['formula_latex'],
                             'source_book': record.get('source_book'),
                             'source_locator': record.get('source_locator'),
                             'definition_references': definitions})
        problem = {'id': identity, 'name': item['name'], 'family_id': family,
                   'difficulty': levels[identity], 'group_id': group_for[identity],
                   'split': split, 'formula_latex': item['formula_latex'],
                   'representative_source': item['representative_source'],
                   'source_ids': item['source_ids'],
                   'domain_semantics': item['domain_semantics'],
                   'domain_variants': variants,
                   'local_definitions': local_definitions.get(identity, [])}
        problems.append(problem)
        path = f'formulas/{split}/{identity}.md'
        lines = [f"# {identity} · {item['name']}", '',
                 f'家族：{family} · {names[family]}；难度：{levels[identity]}；集合：{split}。', '',
                 '[统一记号与条件](../../metadata/NOTATION.md)', '',
                 '在以下来源条件及记号约定下，证明所列关系。', '',
                 '$$', item['formula_latex'], '$$', '',
                 f"代表来源：`{item['representative_source']}`。", '',
                 *problem['local_definitions'], '',
                 '来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。', '']
        for variant in variants:
            lines += [f"- **{variant['source_id']}**（{variant['source_book']}；{variant['source_locator']}）：{variant['conditions']['source_text']}",
                      f"  变量对应：{variant['witness']}"]
        refs = sorted({r for v in variants for r in v['definition_references']})
        if refs:
            lines += ['', '原目录的定义文件引用（保留出处路径，文件可用性见 README）：', '']
            lines += [f'- `{r}`' for r in refs]
        outputs[path] = '\n'.join(lines).strip() + '\n'
        manifests[split].append({k: problem[k] for k in
                                ('id', 'name', 'family_id', 'difficulty', 'group_id', 'representative_source', 'source_ids')})
        manifests[split][-1].update(md_path=path, md_sha256=hashlib.sha256(outputs[path].encode()).hexdigest())

    outputs['metadata/NOTATION.md'] = source('round2_identity_catalog/NOTATION.md')
    outputs['metadata/families.json'] = encode([{'id': f['id'], 'name': f['name'], 'criterion': f['criterion']} for f in families])
    outputs['metadata/groups.json'] = encode({'status': group_data['status'], 'groups': groups,
                                            'edges': [{'source': e['source'], 'target': e['target'], 'type': e['type']} for e in group_data['edges']]})
    outputs['metadata/difficulty.json'] = encode({'source': 'benchmark_four_families/inputs/difficulty_trial_v2_annotations.json',
        'version': difficulty['version'], 'source_status': difficulty['status'],
        'accepted_for_split': True, 'annotations': [{'id': i, 'level': levels[i]} for i in sorted(levels)]})
    outputs['metadata/definition_references.json'] = encode([
        {'path': p, 'exists_in_repository': (REPO / p).is_file()} for p in sorted(definition_references)])
    outputs['metadata/source_hashes.json'] = encode(hashes)
    outputs['config.json'] = encode({'seed': SEED, 'test_size': 100, 'train_size': 346,
        'stratification': 'four_families', 'test_family_targets': targets,
        'allocation': 'integer_minimum_squared_distance_to_proportional_quotas',
        'sampling': 'seeded_whole_group_shuffle_first_exact_fit',
        'group_policy': 'preserve_existing_recorded_relation_components',
        'difficulty_policy': 'retain_accepted_v2_labels_without_separate_quotas',
        'scope': 'problems_only'})
    stats = {'total': 446, 'train': 346, 'test': 100, 'seed': SEED,
             'sampling_attempt': attempt+1, 'groups': len(groups),
             'families': {}, 'difficulty': {}}
    for f in sorted(names):
        stats['families'][f] = {'name': names[f], 'total': counts[f],
                               **{s: sum(x['family_id'] == f for x in rows) for s, rows in manifests.items()}}
    for level in ('低', '中', '高'):
        stats['difficulty'][level] = {'total': sum(v == level for v in levels.values()),
                                     **{s: sum(x['difficulty'] == level for x in rows) for s, rows in manifests.items()}}
    outputs['metadata/statistics.json'] = encode(stats)
    for split, rows in manifests.items():
        assert len(rows) == (100 if split == 'test' else 346)
        outputs[f'splits/{split}.jsonl'] = ''.join(json.dumps(r, ensure_ascii=False)+'\n' for r in rows)
        outputs[f'splits/{split}_problems.jsonl'] = ''.join(json.dumps(p, ensure_ascii=False)+'\n' for p in problems if p['split'] == split)
        outputs[f'{split.upper()}.md'] = '\n'.join([
            f'# {split.upper()} · {len(rows)} 条题目', '',
            '| ID | 题目 | 家族 | 难度 |', '|---|---|---|---|',
            *[f"| {r['id']} | [{r['name']}]({r['md_path']}) | {r['family_id']} | {r['difficulty']} |" for r in rows], ''])
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=['split', 'id', 'name', 'family_id', 'difficulty', 'group_id'])
    writer.writeheader()
    writer.writerows({k: p[k] for k in writer.fieldnames} for p in problems)
    outputs['splits/all_446.csv'] = buffer.getvalue()
    table = '\n'.join(f"| {f} · {r['name']} | {r['total']} | {r['train']} | {r['test']} |" for f, r in stats['families'].items())
    difficulty_table = '\n'.join(f"| {level} | {r['total']} | {r['train']} | {r['test']} |" for level, r in stats['difficulty'].items())
    outputs['README.md'] = f'''# 四家族 Benchmark（2026-10-18）

共 446 条题目，Train 346 条、Test 100 条。新划分使用 A、C、F、G 四个家族；G 合并原 B、D、E。旧版 `benchmark/` 已删除，当前目录为保留版本。

| 家族 | 总数 | Train | Test |
|---|---:|---:|---:|
{table}
| 合计 | 446 | 346 | 100 |

沿用已确认的修订版难度标签；本轮按家族比例分层，不另外设置难度配额。

| 难度 | 总数 | Train | Test |
|---|---:|---:|---:|
{difficulty_table}

入口：[Train 题目索引](TRAIN.md)、[Test 题目索引](TEST.md)、[完整划分表](splits/all_446.csv)。
清单为 `splits/train.jsonl` 和 `splits/test.jsonl`；带公式、条件及各来源原式的数据为同目录的 `train_problems.jsonl` 和 `test_problems.jsonl`。
每题 Markdown 位于 `problems/train/` 或 `problems/test/`。仅整理题目、来源、分类及划分元数据，不含形式化文件或证明答案。

划分规则：以 100/446 的比例计算四家族整数配额，最小化配额平方误差；固定种子 {SEED}，按已有 {len(groups)} 个关联组整体抽取，首个满足精确配额的结果即固定。已记录关联边不跨集合；该隔离依据已有记录，不表示穷尽所有数学等价关系。不参考旧系统证明结果，也不要求新旧成员相同。

公式和条件来自原目录，保留不同来源的参数域与变量对应。共同记号见 [NOTATION.md](metadata/NOTATION.md)。部分题目的原始辅助定义引用指向当前仓库中缺失的 `round1_source_collection/`；本次保留出处并在 [定义引用清单](metadata/definition_references.json) 标明可用性，没有重构这些辅助文件，不能把这次题目划分视为已完成自包含声明整理。

难度采用修订版 V2 的 84 条低、255 条中、107 条高；源标注的待复核状态仍保留在元数据中。本轮不重新评定难度。

重建：`python3 benchmark_four_families/scripts/build_split.py`

只读校验：`python3 benchmark_four_families/scripts/build_split.py --check`

校验覆盖 446 个唯一 ID、346/100 数量、四家族配额、难度标签、关联组及关联边隔离、源文件哈希和所有生成文件的一致性。生成器只写入本目录。
'''
    from migrate_formalization import integrate
    integrate(outputs, stats)
    return outputs, stats


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    outputs, stats = build()
    for name, text in outputs.items():
        path = ROOT / name
        if args.check:
            assert path.is_file() and path.read_bytes() == text.encode(), f'Mismatch: {name}'
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(text.encode())
    actual = {str(p.relative_to(ROOT)) for folder in ('formulas', 'splits', 'metadata', 'lean/Benchmark', 'formalization') for p in (ROOT / folder).rglob('*') if p.is_file() and p.suffix not in ('.olean', '.ilean')}
    expected = {p for p in outputs if p.startswith(('formulas/', 'splits/', 'metadata/', 'lean/Benchmark/', 'formalization/'))}
    assert actual == expected, 'Unexpected or missing generated files'
    assert len(list((ROOT / 'lean/Benchmark/Statements').rglob('*.lean'))) == 446
    print(('Validated' if args.check else 'Built') + ': ' + json.dumps(stats, ensure_ascii=False))


if __name__ == '__main__':
    main()
