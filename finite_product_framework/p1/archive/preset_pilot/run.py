if __name__ == "__main__":
    raise SystemExit("Retired preset pilot: use ../../run.py; this archive is not an automatic pipeline.")

#!/usr/bin/env python3
"""First end-to-end P1 pilot: an explicit adapter for one frozen train statement."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SUPPORTED_ID = 'FQI-FINITE-Q-BINOMIAL'
THEOREM = 'FiniteQBenchmark.Identity005.statement'
GENERATED = HERE / 'generated'

PROOF = '''  change (∑ k ∈ Finset.range (n+1), FiniteQP1.binomialTerm q z n k) = poch z q n
  refine FiniteQP1.prove_growing_sum
    (FiniteQP1.binomialTerm q z) (FiniteQP1.binomialFlux q z)
    (fun n => poch z q n) (fun n => 1-z*q^n) (fun _ => 0)
    (FiniteQP1.binomial_local q z) (FiniteQP1.binomial_boundary q z) ?_ ?_ n
  · simp [FiniteQP1.binomialTerm, FiniteQP1.binomialWeight, gaussian_zero_right]
  · intro m
    rw [poch_succ]
    ring
'''


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')


def load_target(identity):
    train = {r['id']: r for r in map(json.loads,
             (ROOT/'benchmark/splits/train.jsonl').read_text().splitlines())}
    if identity not in train:
        raise ValueError('unsupported_structure: input is not in train')
    if identity != SUPPORTED_ID:
        raise ValueError('unsupported_structure: this pilot has no adapter for ' + identity)
    row = train[identity]
    assert row['family_id'] == 'A'
    case = next(c for c in json.loads((HERE/'cases.json').read_text())['cases']
                if c['id'] == identity)
    path = ROOT / 'benchmark' / row['lean_path']
    assert digest(path) == row['lean_sha256'] == case['lean_sha256'], 'statement changed'
    text = path.read_text()
    assert case['lean_statement'] in text
    assert text.count('  sorry\n') == 1, 'unexpected deferred proof shape'
    assert 'variable {K : Type*} [Field K]' in text
    return path, text


def emit(original):
    # Preserve the frozen declaration/context; replace only its proof and import.
    # The large Representation import is replaced by the exact audited dependency closure.
    target = original.replace('import Benchmark.Representation\n', '')
    target = target.replace('Only this target theorem\'s proof is deferred. Shared auxiliary results are proved.',
                            'P1 generated proof. Original statement and assumptions preserved.')
    target = target.replace('  sorry\n', PROOF)
    parts = [(HERE/'lean/Shared.lean').read_text(),
             (HERE/'lean/Binomial.lean').read_text(), target]
    imports, body = [], []
    for part in parts:
        for line in part.splitlines():
            if line.startswith('import '):
                if line not in imports:
                    imports.append(line)
            else:
                body.append(line)
    result = '\n'.join(imports + [''] + body) + '\n#print axioms ' + THEOREM + '\n'
    assert not re.search(r'\b(sorry|admit|axiom)\b', result)
    return result


def compile_lean(source, env, extra=()):
    cmd = ['lake', 'env', 'lean', *extra, str(source)]
    proc = subprocess.run(cmd, cwd=ROOT/'project', env=env, capture_output=True,
                          text=True, timeout=180)
    result = {'command': cmd, 'exit_code': proc.returncode,
              'output': proc.stdout + proc.stderr}
    if proc.returncode != 0:
        raise RuntimeError('lean_failed: ' + json.dumps(result, ensure_ascii=False))
    if 'sorryAx' in result['output'] or 'declaration uses' in result['output']:
        raise RuntimeError('lean_failed: placeholder dependency')
    return result


def run(identity):
    start = time.monotonic()
    report = {'schema_version': 1, 'identity_id': identity, 'status': 'started',
              'input_adapter': 'explicit frozen-statement adapter',
              'general_statement_parser': False, 'complete_train_proofs': 0,
              'test_files_read': 0, 'stages': [], 'remaining_obligations': []}
    GENERATED.mkdir(exist_ok=True)
    try:
        path, original = load_target(identity)
        report['input'] = {'path': str(path.relative_to(ROOT)), 'sha256': digest(path)}
        report['stages'].append('train_source_verified')
        from search import binomial_search
        construction = binomial_search()
        save(GENERATED/'construction.json', construction)
        report['construction'] = construction
        report['stages'].append('rational_search_and_polynomial_flux_translation')
        output = GENERATED/'FiniteQBinomial.lean'
        output.write_text(emit(original))
        report['output'] = {'path': str(output.relative_to(HERE)), 'sha256': digest(output)}
        report['stages'].append('original_target_proof_emitted')

        # Recompile exact source snapshots outside benchmark. Never trust old benchmark oleans.
        src, obj = GENERATED/'sources', GENERATED/'deps'
        (src/'Benchmark').mkdir(parents=True, exist_ok=True)
        (obj/'Benchmark').mkdir(parents=True, exist_ok=True)
        env = os.environ.copy()
        env['LEAN_PATH'] = str(obj)
        report['dependencies'] = []
        for name in ['Definitions', 'Auxiliary', 'Gaussian']:
            origin = ROOT/'benchmark/lean/Benchmark'/f'{name}.lean'
            snapshot = src/'Benchmark'/f'{name}.lean'
            snapshot.write_bytes(origin.read_bytes())
            result = compile_lean(snapshot, env, ('-R', str(src), '-o', str(obj/'Benchmark'/f'{name}.olean')))
            report['dependencies'].append({'source': str(origin.relative_to(ROOT)),
                                           'sha256': digest(origin), 'lean': result})
        report['lean'] = compile_lean(output, env)
        audit = report['lean']['output']
        assert f"'{THEOREM}' depends on axioms: [propext, Classical.choice, Quot.sound]" in audit
        assert digest(path) == report['input']['sha256'], 'original statement changed during run'
        report['stages'] += ['local_boundary_initial_target_verified', 'original_theorem_axioms_audited']
        report['status'] = 'proved'
        report['complete_train_proofs'] = 1
    except Exception as exc:
        report['status'] = 'failed'
        report['error'] = f'{type(exc).__name__}: {exc}'
    report['elapsed_seconds'] = round(time.monotonic()-start, 3)
    save(GENERATED/'run.json', report)
    print(json.dumps({k: v for k, v in report.items()
                      if k not in ('construction', 'dependencies', 'lean')}, ensure_ascii=False, indent=2))
    return 0 if report['status'] == 'proved' else 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--identity', default=SUPPORTED_ID)
    args = parser.parse_args()
    sys.exit(run(args.identity))
