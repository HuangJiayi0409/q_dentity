"""Audit synthetic construction evidence and replay deliberately false witnesses.

Run after the three method checks. Does not load any benchmark problem files.
"""
import json
import copy
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from workflow.contracts import HERE, ROOT, save, sha, accept_proof
from workflow.worker import prepared_environment
from product.pipeline import lean


def main():
    report = dict(status='started', train_proofs_counted=0, test_files_read=0,
                  cases=0, proved=0, computed_witnesses=0, mutations=[],
                  target_independence=[])
    examples = {'kernel_transform': ('constructed_inverse_three', 'synthInverse'),
                'spectral': ('operator_not_supplied', 'synthOperator'),
                'determinant': ('constructed_dense_plu', 'synthL')}
    for method, (example, witness) in examples.items():
        file = HERE/'generated'/f'{method}_validation.json'
        suite = json.loads(file.read_text())
        assert suite['status'] == 'passed', method
        report[method] = dict(report=str(file), sha256=sha(file))
        work = Path(suite['work_directory'])
        env = prepared_environment(json.loads((work/'setup/environment.json').read_text()))
        for case in suite['cases']:
            result = json.loads(Path(case['report']).read_text())
            report['cases'] += 1
            if result['status'] == 'proved':
                folder = Path(case['report']).parent
                source = folder/'source.lean'
                accept_proof(result, dict(sha256=sha(source), snapshot=str(source),
                    path=str(source.relative_to(ROOT)), theorem='StructuralRegression.statement'), folder)
                report['proved'] += 1
                cert = json.loads(Path(result['certificate']['path']).read_text())
                report['computed_witnesses'] += cert.get('certificate_origin') == 'computed_witness'
        folder = work/example
        if method == 'kernel_transform':
            from kernel_transform.construct import construct
            raw = json.loads((folder/'synthesis_input.json').read_text())
            changed = copy.deepcopy(raw)
            changed['proposed_inverse'] = dict(display='0', entries=[])
            assert construct(raw)[0]['certificate'] == construct(changed)[0]['certificate']
            report['target_independence'].append('inverse unchanged after replacing proposed inverse')
        if method == 'determinant':
            good = json.loads((folder/'construction.json').read_text())
            bad = json.loads((work/'wrong_dense_value/construction.json').read_text())
            assert [c['certificate'] for c in good['candidates']] == [
                c['certificate'] for c in bad['candidates']]
            report['target_independence'].append('same determinant witnesses for true and false claimed values')
        original = (folder/'Proof.lean').read_text()
        modified, count = re.subn(r'(?m)^(  let '+witness+r' : .*?) := .*$',
                                  r'\1 := 0', original)
        assert count == 1
        corrupt = folder/'CorruptWitness.lean'
        corrupt.write_text(modified)
        result = lean(corrupt, env)
        save(folder/'corrupt_witness.json', result)
        errors = [line for line in result['output'].splitlines() if 'error:' in line]
        assert result['exit_code'] != 0 and errors and all(
            'unsolved goals' in line or '`field_simp` made no progress' in line
            for line in errors), result
        report['mutations'].append(dict(method=method, witness=witness,
            rejected=True, log=str(folder/'corrupt_witness.json')))
    report.update(status='passed', rejected=report['cases']-report['proved'])
    save(HERE/'generated/matrix_construction_validation.json', report)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
