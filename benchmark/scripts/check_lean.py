#!/usr/bin/env python3
"""Compile all migrated modules in dependency order using local mathlib cache."""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / 'lean'
PROJECT = ROOT.parent / 'project'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--workers', type=int, default=8)
    args = parser.parse_args()
    assert args.workers > 0
    for name in ('lean-toolchain', 'lake-manifest.json'):
        assert (LEAN/name).read_bytes() == (PROJECT/name).read_bytes()
    toolchain = (LEAN/'lean-toolchain').read_text().strip().replace('/', '--').replace(':', '---')
    exe = Path.home()/'.elan/toolchains'/toolchain/'bin/lean'
    build = LEAN/'.lake/build/lib/lean'
    env = os.environ.copy()
    env['LEAN_PATH'] = ':'.join([str(build)] + [str(p) for p in sorted((PROJECT/'.lake/packages').glob('*/.lake/build/lib/lean'))])
    paths = [LEAN/'Benchmark.lean', *sorted((LEAN/'Benchmark').rglob('*.lean'))]
    modules = {str(p.relative_to(LEAN).with_suffix('')).replace('/', '.'): p for p in paths}
    dependencies = {name: set(re.findall(r'^import\s+(Benchmark(?:\.[\w]+)*)\s*$', p.read_text(), re.M)) for name, p in modules.items()}
    assert all(dep in modules for deps in dependencies.values() for dep in deps)
    reports = ROOT/'reports'
    logs = reports/'lean_compile_logs'
    logs.mkdir(parents=True, exist_ok=True)

    def compile_module(name):
        path = modules[name]
        target = build/path.relative_to(LEAN).with_suffix('.olean')
        target.parent.mkdir(parents=True, exist_ok=True)
        start = time.monotonic()
        try:
            result = subprocess.run([str(exe), '-j1', '-DautoImplicit=false', '-o', str(target), str(path)],
                                    cwd=LEAN, env=env, capture_output=True, text=True, timeout=300)
            code, log = result.returncode, result.stdout+result.stderr
        except subprocess.TimeoutExpired:
            code, log = 124, 'Compilation timed out after 300 seconds.'
        (logs/f'{name}.log').write_text(log)
        return {'module': name, 'exit_code': code, 'seconds': round(time.monotonic()-start, 3),
                'source_sha256': hashlib.sha256(path.read_bytes()).hexdigest()}

    completed, results = set(), []
    while len(completed) < len(modules):
        ready = sorted(n for n in modules if n not in completed and dependencies[n] <= completed)
        assert ready, 'Dependency cycle'
        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            for future in as_completed([pool.submit(compile_module, n) for n in ready]):
                row = future.result()
                results.append(row)
                if row['exit_code'] == 0:
                    completed.add(row['module'])
                if len(results) % 25 == 0 or row['exit_code']:
                    print(f"Checked {len(results)}/{len(modules)}; {row['module']}: {row['exit_code']}", flush=True)
        report = {'total_modules': len(modules), 'checked': len(results), 'passed': len(completed),
                  'all_passed': len(completed) == len(modules), 'target_proofs': 'deferred_sorry_preserved',
                  'results': sorted(results, key=lambda r: r['module'])}
        (reports/'lean_validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
        if any(r['exit_code'] for r in results):
            raise SystemExit('Compilation failed; inspect reports/lean_compile_logs')
        print(f'Completed {len(completed)}/{len(modules)} modules', flush=True)


if __name__ == '__main__':
    main()
