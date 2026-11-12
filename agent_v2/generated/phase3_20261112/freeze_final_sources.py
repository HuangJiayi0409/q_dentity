"""Freeze actual registry dependencies, runtime and test sources before final checks."""
import argparse
from datetime import datetime, timezone
import difflib
import json
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from agent_v2.cli import runtime_dependencies
from agent_v2.method_registry import builtin_registry, resolve
from agent_v2.storage import sha256_file


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-root', required=True)
    args = parser.parse_args()
    output = Path(args.output_root).absolute()
    output.mkdir(parents=True, exist_ok=False)
    registry = builtin_registry()
    paths = {Path(a.path).resolve() for a in runtime_dependencies()}
    dependency_sets = {}
    for method in registry.ids():
        artifacts = resolve(registry.get(method).dependency_provider)()
        dependency_sets[method] = [a.to_dict() for a in artifacts]
        for artifact in artifacts:
            path = Path(artifact.path).resolve()
            if sha256_file(path) != artifact.sha256:
                raise RuntimeError('dependency changed before freeze: ' + str(path))
            paths.add(path)
    paths.update((ROOT / 'agent_v2/tests').glob('*.py'))
    paths.update(Path(__file__).parent / name for name in (
        'freeze_final_sources.py', 'run_full_suite.py', 'run_final_method_matrix.py'))
    records, external = {}, {}
    for path in sorted(paths):
        digest = sha256_file(path)
        if path.is_relative_to(ROOT):
            relative = str(path.relative_to(ROOT))
            destination = output / 'source' / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, destination)
            if sha256_file(path) != digest or sha256_file(destination) != digest:
                raise RuntimeError('source changed during freeze: ' + str(path))
            records[relative] = {'sha256': digest, 'bytes': path.stat().st_size,
                                 'snapshot_path': str(destination)}
        else:
            external[str(path)] = {'sha256': digest, 'copied': False, 'reason': 'external fixed dependency'}
    baseline = Path(__file__).parent / 'before'
    unchanged, changes = {}, []
    for old in sorted((baseline / 'agent_v2/tests').glob('*.py')):
        relative = str(old.relative_to(baseline))
        digest = sha256_file(old)
        if sha256_file(ROOT / relative) != digest:
            raise RuntimeError('baseline test source changed: ' + relative)
        unchanged[relative] = digest
    for relative in sorted(records):
        old = baseline / relative
        # The original baseline only froze agent_v2. Later per-method evidence
        # separately records pure mathematical helper changes.
        if not relative.startswith('agent_v2/') or '/generated/' in relative:
            continue
        before = old.read_text().splitlines(keepends=True) if old.is_file() else []
        after = (output / 'source' / relative).read_text().splitlines(keepends=True)
        changes.extend(difflib.unified_diff(before, after, fromfile='before/' + relative, tofile='final/' + relative))
    (output / 'agent_v2_changes.diff').write_text(''.join(changes))
    manifest = {'schema_version': 1, 'frozen_at_utc': datetime.now(timezone.utc).isoformat(),
                'python': sys.version, 'repository': str(ROOT), 'files': records,
                'file_count': len(records), 'external_dependencies': external,
                'method_dependency_sets': dependency_sets, 'registry': registry.to_dict(),
                'baseline_tests_unchanged': unchanged, 'baseline_test_count': len(unchanged),
                'validation_status': 'not yet run', 'proof_claim': False}
    (output / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'frozen_files': len(records), 'baseline_tests_unchanged': len(unchanged),
                      'manifest': str(output / 'manifest.json')}), flush=True)


if __name__ == '__main__':
    main()
