#!/usr/bin/env python3
"""Original-statement regression and adversarial tests, never added to train coverage."""
import json
import os
from pathlib import Path
import re
import sys

import run


def main():
    report = {'status': 'failed', 'complete_train_proofs': 0, 'checks': [],
              'synthetic_cases_count_as_train': False}
    try:
        identity = 'FQI-SRC-FINE-15.2'
        native = run.run(identity)
        assert native['status'] == 'proved', native.get('error', native['status'])
        report['native_report'] = 'generated/runs/'+identity+'/report.json'
        report['complete_train_proofs'] = 1
        env = os.environ.copy()
        env['LEAN_PATH'] = str(run.HERE/'generated/runs'/identity/'deps')
        source = run.load_target(identity)[0].read_text()

        def check(name, text, expected, *, forged=False):
            work = run.HERE/'generated/tests'/name
            work.mkdir(parents=True, exist_ok=True)
            original = run.construct
            if forged:
                run.construct = lambda raw: {'status': 'constructed', 'residual': '0',
                                             'test_forged_backend': True}
            try:
                result = run.prove_source(text, work, env, max_depth=2)
            finally:
                run.construct = original
            run.save(work/'report.json', result)
            assert result['status'] == expected, (name, result['status'])
            report['checks'].append({'name': name, 'status': 'passed', 'result': expected,
                                     'report': str((work/'report.json').relative_to(run.HERE))})

        names = {'a': 'alpha', 'b': 'beta', 'q': 'base', 'N': 'length'}
        renamed = re.sub(r'\b(a|b|q|N)\b', lambda m: names[m.group()], source)
        check('renamed_parameters', renamed, 'proved')
        no_domain = re.sub(r'\n \(h_domain .*?\) :\n', '\n :\n', source, flags=re.S)
        assert no_domain != source
        check('no_nonzero_assumptions', no_domain, 'proved')
        wrong = source.replace('((-1:K)^k)', '((2:K)*(-1:K)^k)')
        assert wrong != source
        check('wrong_coefficient_rejected', wrong, 'unsupported_or_unclosed_structure')
        check('forged_backend_rejected', wrong, 'lean_verification_failed', forged=True)
        prefix = '''import Benchmark.P2Atoms
open scoped BigOperators
namespace P2Synthetic
variable {K : Type*} [Field K]
'''
        triple = prefix+'''theorem statement (f g h : ℕ → K) (n : ℕ) :
    PowerSeries.coeff n ((PowerSeries.mk f * PowerSeries.mk g) * PowerSeries.mk h) =
      ∑ k ∈ Finset.range (n+1), ∑ j ∈ Finset.range (k+1),
        h (n-k) * g (k-j) * f j := by
  sorry
end P2Synthetic
'''
        check('three_arbitrary_series', triple, 'proved')
        zero_inv = prefix+'''theorem statement (f : ℕ → K) (n : ℕ) :
    PowerSeries.coeff n (PowerSeries.mk f * PowerSeries.mk (fun k => (f k)⁻¹)) =
      ∑ k ∈ Finset.range (n+1), (1:K) := by
  sorry
end P2Synthetic
'''
        check('invalid_inverse_cancellation_rejected', zero_inv, 'unsupported_or_unclosed_structure')
        try:
            run.load_target('FQI-FINITE-Q-BINOMIAL')
            raise AssertionError('P1-only source incorrectly accepted')
        except ValueError as exc:
            assert 'unsupported_input' in str(exc)
        report['checks'].append({'name': 'scope_guard', 'status': 'passed'})
        for dependency in native['dependencies']:
            assert run.sha(run.ROOT/dependency['path']) == dependency['sha256']
        report['code_sha256'] = {name: run.sha(run.HERE/name) for name in
                                 ('run.py', 'check.py', 'lean/Coefficient.lean', 'lean/Export.lean')}
        report['status'] = 'passed'
    except Exception as exc:
        report['error'] = f'{type(exc).__name__}: {exc}'
    run.save(run.HERE/'validation.json', report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report['status'] == 'passed' else 1


if __name__ == '__main__':
    sys.exit(main())
