"""Attach existing Lean statements by canonical ID; preserve approved membership."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OLD = ROOT  # Migration is complete; all inputs are local.


def dump(value):
    return json.dumps(value, ensure_ascii=False, indent=2) + '\n'


def sha(text):
    return hashlib.sha256(text.encode()).hexdigest()


def integrate(outputs, stats):
    for relative, expected in json.loads((ROOT / 'inputs/lean_source_hashes.json').read_text()).items():
        assert hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() == expected, relative
    frozen_text = (ROOT / 'metadata/frozen_split.json').read_text()
    frozen = json.loads(frozen_text)
    outputs['metadata/frozen_split.json'] = frozen_text
    old_registry = json.loads((ROOT / 'inputs/lean_statements.json').read_text())
    old_rows = json.loads((ROOT / 'inputs/source_sections.json').read_text())
    registry, migration, source_hashes = {}, [], {}

    def read_old(relative):
        path = ROOT / relative
        if relative.startswith('metadata/'):
            path = ROOT / 'inputs' / Path(relative).name
        elif relative.startswith('formalization/'):
            path = ROOT / 'history' / relative
        data = path.read_bytes()
        source_hashes[relative] = hashlib.sha256(data).hexdigest()
        return data.decode()

    for path in sorted((OLD / 'lean').rglob('*.lean')):
        relative = path.relative_to(OLD)
        if '.lake' in relative.parts or 'Statements' in relative.parts or path.name in ('Train.lean', 'Test.lean'):
            continue
        outputs[str(relative)] = read_old(str(relative))
    for name in ('lean-toolchain', 'lakefile.toml', 'lake-manifest.json'):
        outputs[f'lean/{name}'] = read_old(f'lean/{name}')
    for name in ('classification.json', 'classification_provenance.json', 'families.json', 'groups.json'):
        outputs[f'metadata/{name}'] = read_old(f'metadata/{name}')
    read_old('metadata/lean_statements.json')
    for split in ('train', 'test'):
        rows = list(map(json.loads, outputs[f'splits/{split}.jsonl'].splitlines()))
        assert [r['id'] for r in rows] == frozen[split], 'Approved split changed'
        imports = []
        for row in rows:
            identity = row['id']
            old = old_registry[identity]
            old_text = read_old(old['lean_path'])
            assert sha(old_text) == old['lean_sha256']
            path = f"lean/Benchmark/Statements/{split.title()}/{Path(old['lean_path']).name}"
            # Only the provenance comment changes. Namespace and theorem stay byte-identical.
            old_comment = f"Frozen statement: formulas/{old['split']}/{identity}.md"
            new_comment = f"Frozen statement: {row['md_path']}"
            assert old_text.count(old_comment) == 1, identity
            new_text = old_text.replace(old_comment, new_comment)
            assert new_text.replace(new_comment, old_comment) == old_text
            outputs[path] = new_text
            row.update(lean_path=path, lean_sha256=sha(new_text), lean_batch=old['lean_batch'],
                       lean_status=old['lean_status'],
                       source_md_path=old_rows[identity]['source_md_path'],
                       source_section_sha256=old_rows[identity]['source_section_sha256'])
            registry[identity] = {k: row[k] for k in ('md_sha256', 'lean_path', 'lean_sha256', 'lean_batch', 'lean_status')}
            registry[identity]['split'] = split
            imports.append('import ' + path[5:-5].replace('/', '.'))
            migration.append({'id': identity, 'old_split': old['split'], 'new_split': split,
                              'old_lean_path': old['lean_path'], 'new_lean_path': path,
                              'old_sha256': old['lean_sha256'], 'new_sha256': sha(new_text),
                              'only_provenance_comment_changed': old_text != new_text})
        outputs[f'lean/Benchmark/{split.title()}.lean'] = '\n'.join(sorted(imports)) + '\n'
        outputs[f'splits/{split}.jsonl'] = ''.join(json.dumps(r, ensure_ascii=False)+'\n' for r in rows)
    assert set(registry) == set(old_registry)
    outputs['metadata/lean_statements.json'] = dump(registry)
    for batch in sorted({r['lean_batch'] for r in registry.values()}):
        old_manifest = json.loads(read_old(f'formalization/{batch}/manifest.json'))
        manifest = []
        for historical in old_manifest:
            identity = historical['id']
            current = registry[identity]
            manifest.append({
                'index': historical['index'], 'id': identity, 'split': current['split'],
                'md_path': f"formulas/{current['split']}/{identity}.md",
                'lean_path': current['lean_path'], 'draft_lean_path': current['lean_path'],
                'lean_sha256': current['lean_sha256'], 'status': current['lean_status'],
                'target_proof_policy': 'sorry_allowed', 'auxiliary_proof_policy': 'proved_without_sorry',
                'historical_compiled': historical.get('compiled', False),
                'current_validation': 'reports/lean_validation.json'})
        outputs[f'formalization/{batch}/manifest.json'] = dump(manifest)
        outputs[f'formalization/{batch}/README.md'] = (
            f'# {batch} 迁移记录\n\n'
            f'本批 {len(manifest)} 条，按当前划分重新登记文件路径；历史批次编号保留。'
            f'原数学审阅、specs 与辅助引理审计见 [旧批次记录](../../history/formalization/{batch}/README.md)。\n\n'
            '目标定理证明仍待完成；新项目类型检查结果见 [当前验证](../../reports/lean_validation.json)。\n')
    outputs['formalization/migration.json'] = (ROOT / 'formalization/migration.json').read_text()
    cfg = json.loads(outputs['config.json'])
    cfg.update(scope='statements_with_deferred_proofs', frozen_split_source='metadata/frozen_split.json',
               lean_statements={'generated': 446, 'target_proofs': 'deferred'})
    outputs['config.json'] = dump(cfg)
    outputs['metadata/split_statistics.csv'] = 'family_id,name,total,proportion,test_target,test_actual,train_actual\n' + ''.join(
        f"{f},{r['name']},{r['total']},{r['total']/446},{r['test']},{r['test']},{r['train']}\n"
        for f, r in stats['families'].items())
    readme = outputs['README.md'].replace('`problems/train/` 或 `problems/test/`', '`formulas/train/` 或 `formulas/test/`')
    readme = readme.replace('仅整理题目、来源、分类及划分元数据，不含形式化文件或证明答案。',
        '逐题 Markdown 保留无证明提示的题目文本；另外迁入旧 benchmark 的全部 Lean 声明和共享辅助模块。目标定理仍保留 `sorry`，不是已完成证明。')
    readme += '''
## 形式化迁移

沿用旧目录的 `formulas/`、`splits/`、`metadata/`、`lean/`、`formalization/` 和 `scripts/` 布局。已确认的划分冻结在 `metadata/frozen_split.json`；重建必须逐项匹配，不会重新选择成员。

446 条声明按原公式 ID 对应迁入 `lean/Benchmark/Statements/Train/`（346 条）和 `Test/`（100 条）。保留 Identity 编号、命名空间和定理内容，仅更新文件内的公式路径注释；重建 `Benchmark/Train.lean`、`Test.lean` 的 imports。工具链、依赖锁和共享模块沿用旧版，不复制缓存或已有证明运行结果。旧 benchmark 已删除；重建仅使用本目录的冻结输入和原公式目录。

`metadata/lean_statements.json` 与两份 split 清单记录新路径、新哈希及原批次。迁移来源、旧新集合和逐文件哈希见 [migration.json](formalization/migration.json)。原五批数学审阅和编译记录归档在本目录 `history/formalization/`，是历史证据，不是新划分的测试成绩。

迁移后的完整类型检查：`python3 benchmark_four_families/scripts/check_lean.py --workers 8`。检查依赖顺序、全部声明及总入口，复用项目 mathlib 缓存；新编译产物和日志只写入本目录。结果见 `reports/lean_validation.json`。`sorry` 警告符合原目标证明待完成的约定，类型检查通过不表示证明完成。

结构校验也可运行：`python3 benchmark_four_families/scripts/validate_split.py`。
'''
    outputs['README.md'] = readme
