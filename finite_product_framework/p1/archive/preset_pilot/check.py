if __name__ == "__main__":
    raise SystemExit("Retired preset pilot: use ../../run.py; this archive is not an automatic pipeline.")

#!/usr/bin/env python3
"""Validate train provenance, rerun the first pilot, and audit its proof artifacts."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    report = {
        'schema_version': 1,
        'scope': 'P1 shared assembly and explicit finite q-binomial pilot',
        'status': 'failed',
        'train_cases_checked': [],
        'test_files_read': 0,
        'cas_trials_run': 0,
        'complete_train_proofs': 0,
        'automatic_statement_parser': 'not_implemented',
        'proof_generator': 'explicit finite q-binomial adapter',
    }
    try:
        rows = [json.loads(line) for line in
                (ROOT / 'benchmark/splits/train.jsonl').read_text().splitlines() if line]
        train = {row['id']: row for row in rows}
        cases = json.loads((HERE / 'cases.json').read_text())['cases']
        assert len(cases) == 4 and len({c['id'] for c in cases}) == 4
        for case in cases:
            original = train[case['id']]
            assert case['split'] == 'train' and case['family_id'] == original['family_id'] == 'A'
            for name, source_name, hash_name in [
                ('lean_path', 'lean_path', 'lean_sha256'),
                ('formula_path', 'md_path', 'md_sha256'),
            ]:
                expected = 'benchmark/' + original[source_name]
                assert case[name] == expected
                path = ROOT / expected
                assert digest(path) == original[hash_name]
                assert digest(path) == case['lean_sha256' if name == 'lean_path' else 'formula_sha256']
            assert case['lean_statement'] in (ROOT / case['lean_path']).read_text()
            report['train_cases_checked'].append(case['id'])

        kernel = HERE / 'lean/Shared.lean'
        source = kernel.read_text()
        # The kernel imports only mathlib, never a deferred benchmark theorem.
        imports = re.findall(r'^import (.+)$', source, re.M)
        assert imports and all(item.startswith('Mathlib.') for item in imports)
        report['shared_lean_sha256'] = digest(kernel)
        cmd = [sys.executable, str(HERE / 'run.py')]
        result = subprocess.run(cmd, text=True, capture_output=True, timeout=600)
        assert result.returncode == 0, result.stdout + result.stderr
        run = json.loads((HERE / 'generated/run.json').read_text())
        assert run['status'] == 'proved' and run['complete_train_proofs'] == 1
        assert digest(HERE / run['output']['path']) == run['output']['sha256']
        output = run['lean']['output']
        report['lean'] = run['lean']
        assert 'sorryAx' not in output, 'Placeholder dependency in kernel'
        expected_names = ['telescope', 'growing_sum_recurrence',
                          'first_order_unique', 'prove_growing_sum']
        for name in expected_names:
            assert f"'FiniteQP1.{name}'" in output, f'Missing axiom audit: {name}'
        report['verified_shared_theorems'] = expected_names
        report['complete_train_proofs'] = 1
        report['cas_trials_run'] = 1
        report['proved_train_ids'] = [run['identity_id']]
        report['run_report_sha256'] = digest(HERE / 'generated/run.json')
        report['status'] = 'passed'
    except Exception as exc:
        report['error'] = f'{type(exc).__name__}: {exc}'
    (HERE / 'validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k != 'lean'}, ensure_ascii=False, indent=2))
    return 0 if report['status'] == 'passed' else 1


if __name__ == '__main__':
    sys.exit(main())
