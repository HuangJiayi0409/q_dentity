#!/usr/bin/env python3
"""Native multisum proof regression, using only the train acceptance source.

Variants reuse a freshly searched runtime certificate and recheck it against
all their actual shift ratios. Production run.py always constructs its own.
"""
import copy
import hashlib
import json
import os
import re
from pathlib import Path
from lean_pipeline import HERE,ROOT,extract
from multisum_pipeline import frontend,synthesize
from multisum_lean import Compiler


def main(run_directory=None):
    checks=[]
    report={'status':'failed','checks':checks,'synthetic_tests_count_as_train_proofs':False,
            'new_train_proofs':0,'test_files_read':0}
    try:
        original=Path(run_directory) if run_directory else HERE/'generated/runs/FQI-SRC-GR2-10.Ex18'
        baseline=json.loads((original/'report.json').read_text())
        assert baseline['status']=='proved',baseline['status']
        source=(ROOT/baseline['source']['path']).read_text()
        assert hashlib.sha256(source.encode()).hexdigest()==baseline['source']['sha256']
        deps=original/'deps'
        if not deps.exists():deps=HERE/'generated/runs/FQI-SRC-GR2-10.Ex18/deps'
        env=dict(os.environ);env['LEAN_PATH']=str(deps)
        substitutions={'a':'alpha','b':'beta','c':'gamma','d':'delta','ee':'epsilon',
                       'q':'rho','n':'length','j':'idx','k':'idy','hbase':'regularBase',
                       'hnz':'nonzeroInputs','h_domain':'domainAssumptions'}
        renamed=re.sub(r'\b('+ '|'.join(substitutions)+r')\b',lambda m:substitutions[m.group()],source)
        marker='(∑ k ∈ Finset.range (n-j+1), '
        rhs='= ((pochList [c,'
        assert source.count(marker)==source.count(rhs)==1
        scaled=source.replace(marker,marker+'(3 : K) * ').replace(rhs,'= (3 : K) * ((pochList [c,')
        wrong=source.replace(rhs,'= (2 : K) * ((pochList [c,')
        for label,text,positive in [('renamed',renamed,True),('scaled_kernel_and_target',scaled,True),
                                    ('wrong_initial_value',wrong,False)]:
            work=HERE/'generated/multisum_regression'/label;work.mkdir(parents=True,exist_ok=True)
            raw=extract(text,work,env)
            problem,model=frontend(raw,'synthetic-'+label)
            c=copy.deepcopy(baseline['construction'])
            result=synthesize(text,model,c,work,env)
            (work/'verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
            assert result['status']==('proved' if positive else 'lean_failed'),(label,result['status'],result.get('lean'))
            checks.append({'case':label,'status':'passed' if positive else 'rejected_by_Lean',
                           'verification':str(work/'verification.json')})
            print(label,checks[-1]['status'],flush=True)
            if label=='renamed':
                hypotheses=json.loads((work/'lean_hypotheses.json').read_text())
                bad=copy.deepcopy(c);bad['certificates'][0]='1+('+bad['certificates'][0]+')'
                try:Compiler(model,bad,hypotheses)
                except ValueError as exc:assert 'residual' in str(exc),str(exc)
                else:raise AssertionError('tampered certificate accepted')
                checks.append({'case':'tampered_vector_certificate','status':'rejected'})
                try:Compiler(model,c,[h for h in hypotheses if h['type']['op']!='forall'])
                except ValueError as exc:assert 'domain_unresolved' in str(exc),str(exc)
                else:raise AssertionError('missing finite domain accepted')
                checks.append({'case':'missing_domain','status':'rejected'})
        report['status']='passed'
    except Exception as exc:
        report['error']=f'{type(exc).__name__}: {exc}'
    report['code_sha256']={name:hashlib.sha256((HERE/name).read_bytes()).hexdigest() for name in
        ('multisum.py','multisum_pipeline.py','multisum_lean.py','exact_linear.py','test_multisum_native.py',
         'lean/Extract.lean','lean/MultisumRules.lean','lean/MultisumProductRules.lean')}
    (HERE/'generated/multisum_native_tests.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False))
    return 0 if report['status']=='passed' else 1

if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--run-directory')
    raise SystemExit(main(parser.parse_args().run_directory))
