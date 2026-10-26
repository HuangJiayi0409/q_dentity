"""Direct branch integration: derived constructions, reuse and false-target rejection."""
import copy
import json
import os
from pathlib import Path
import re
import tempfile
from direct import frontend, construct, synthesize
from lean_pipeline import HERE, ROOT, extract
from qgosper import Budget


def main():
    report = {'status':'failed','synthetic_tests_count_as_train_proofs':False,'checks':[]}
    try:
        case = next(c for c in json.loads((HERE/'cases.json').read_text())['cases']
                    if c['role']=='second_complete_branch')
        run = json.loads((HERE/'generated/runs'/case['id']/'report.json').read_text())
        assert run['status']=='proved'
        source = (ROOT/run['source']['path']).read_text()
        env = os.environ.copy()
        env['LEAN_PATH'] = str(Path(run['verification']['proof_file']).parent/'deps')
        renamed = re.sub(r'\b(q|m|n|j)\b',lambda m:{'q':'u','m':'a','n':'b','j':'r'}[m.group()],source)
        scaled = source.replace('(gaussian q (n+m+1) (m+1)) =',
                                '(3 * gaussian q (n+m+1) (m+1)) =').replace('((q^j) *','((3*q^j) *')
        wrong = source.replace('(gaussian q (n+m+1) (m+1)) =',
                               '(gaussian q (n+m+2) (m+1)) =')
        for label,text in [('renamed_parameters',renamed),('scaled_weight',scaled),('wrong_endpoint',wrong)]:
            assert text != source
            with tempfile.TemporaryDirectory(prefix='p1-direct-') as tmp:
                work = Path(tmp)
                formula,model = frontend(extract(text,work,env),'synthetic-regression')
                try:
                    construct(dict(formula,certificate='1'),Budget())
                except ValueError as exc:
                    assert 'invalid_problem' in str(exc)
                else:
                    raise AssertionError('proof hint accepted')
                constructed = construct(formula,Budget())['construction']
                assert constructed['status']=='constructed'
                result = synthesize(text,model,constructed,work,env)
                expected = 'lean_failed' if label=='wrong_endpoint' else 'proved'
                assert result['status']==expected, result
                report['checks'].append({'case':label,'status':result['status'],
                                         'representation':constructed['representation']})
                if label=='scaled_weight':
                    assert constructed['representation']['coefficient']=='3'
                    altered = copy.deepcopy(constructed)
                    altered['representation']['coefficient']='6'
                    rejected = synthesize(text,model,altered,work,env)
                    assert rejected['status']=='lean_failed'
                    report['checks'].append({'case':'tampered_antidifference','status':'rejected_by_Lean'})
        report['status']='passed'
    except Exception as exc:
        report['error']=f'{type(exc).__name__}: {exc}'
    (HERE/'generated/direct_tests.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False,indent=2))
    return 0 if report['status']=='passed' else 1


if __name__=='__main__':
    raise SystemExit(main())
