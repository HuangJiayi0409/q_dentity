"""Behavioral integration tests; synthetic variants do not count as train proofs."""
import json
import os
import re
import tempfile
from pathlib import Path
from expressions import derive, X, q
from search import search
from lean_pipeline import HERE, ROOT, extract, frontend, synthesize


def main():
    report = {'status':'failed', 'synthetic_tests_count_as_train_proofs':False, 'checks':[]}
    try:
        case = next(c for c in json.loads((HERE/'cases.json').read_text())['cases'] if c['role']=='first_complete_branch')
        run = json.loads((HERE/'generated/runs'/case['id']/'report.json').read_text())
        assert run['status'] == 'proved'
        assert run['automatic_train_proofs'] == 1
        source = (ROOT/run['source']['path']).read_text()
        env = os.environ.copy()
        env['LEAN_PATH'] = str(Path(run['verification']['proof_file']).parent/'deps')
        variants = [
            ('renamed_and_squared_parameter',
             source.replace('z^k','(z^2)^k').replace('poch z q n','poch (z^2) q n')),
            ('positive_weight',
             source.replace('(-1)^k*z^k','z^k').replace('poch z q n','poch (-z) q n')),
        ]
        variants[0] = (variants[0][0], re.sub(r'\b(q|z|n|k)\b',
            lambda m: {'q':'u','z':'v','n':'m','k':'r'}[m.group()], variants[0][1]))
        for label, text in variants:
            with tempfile.TemporaryDirectory(prefix='p1-integration-') as directory:
                work = Path(directory)
                raw = extract(text,work,env)
                formula, model = frontend(raw,'synthetic-regression')
                shifts = derive(formula)
                construction = search(shifts['n_shift'],shifts['k_shift'],shifts['target_coefficient'],X,q)
                assert construction['status'] == 'constructed'
                result = synthesize(text,model,shifts,construction,work,env)
                assert result['status'] == 'proved', result
                report['checks'].append({'case':label, 'status':'passed',
                    'generated_flux':result['plan']['multiplier'], 'axiom_output':result['lean']['output']})
                if label == 'positive_weight':
                    altered = dict(construction, certificate='2*('+construction['certificate']+')')
                    rejected = synthesize(text,model,shifts,altered,work,env)
                    assert rejected['status'] == 'lean_failed'
                    assert 'unsolved goals' in rejected['lean']['output']
                    report['checks'].append({'case':'tampered_computed_certificate', 'status':'rejected_by_Lean'})
        report['status'] = 'passed'
    except Exception as exc:
        report['error'] = f'{type(exc).__name__}: {exc}'
    (HERE/'generated/lean_tests.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='checks'},ensure_ascii=False,indent=2))
    if report['status'] != 'passed':
        raise SystemExit(1)


if __name__ == '__main__':
    main()
