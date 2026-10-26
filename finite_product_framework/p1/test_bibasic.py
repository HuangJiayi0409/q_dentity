"""Bibasic construction and original-domain rejection tests (train only)."""
import json
import os
import re
import tempfile
from pathlib import Path
import sympy as s
from bibasic import X,Y,p,q,shift,dispersion,antidifference
from bibasic_pipeline import frontend,synthesize,emit
from qgosper import Budget
from lean_pipeline import HERE,ROOT,extract,verify_proof
from run import construct


def main():
    checks=[]
    report={'status':'failed','synthetic_tests_count_as_train_proofs':False,'checks':checks}
    try:
        a=s.Symbol('a');field=s.QQ.frac_field(p,q,a)
        assert dispersion(shift(1-a*X*Y,17),1-a*X*Y,field)==[17]
        assert dispersion(shift(X+Y,7),X+Y,field)==[7]
        checks.append({'case':'exact_large_and_mixed_factor_dispersion','status':'passed'})
        primitives=[X**9/Y**4,1/(1-a*X*Y),1/(1-a*X)**2,X+Y,1/(X+Y),X**-3+Y**-2]
        for i,H in enumerate(primitives):
            F=s.cancel(shift(H)-H)
            c=antidifference(s.cancel(F/shift(F,-1)))
            assert c['status']=='constructed',c
            R=s.sympify(c['certificate'],locals={'p':p,'q':q,'X':X,'Y':Y,'a':a})
            assert s.cancel(shift(R*F)-R*F-F)==0
            checks.append({'case':f'independent_primitive_{i}','status':'passed'})
        assert antidifference(1/(1-X-Y))['status']=='no_solution_in_derived_laurent_system'
        assert antidifference(p,Budget(max_unknowns=0))['status']=='resource_exhausted'
        checks.append({'case':'no_solution_and_resource_statuses','status':'passed'})
        run=json.loads((HERE/'generated/runs/FQI-SRC-GR2-II-34/report.json').read_text())
        assert run['status']=='proved' and run['branch']=='bibasic_gosper'
        source=(ROOT/run['source']['path']).read_text()
        env=os.environ.copy();env['LEAN_PATH']=str(Path(run['verification']['proof_file']).parent/'deps')
        baseline=run['construction']['certificate']
        source_no_domain=re.sub(r' \(h_domain :.*?\) :\n', ' :\n', source, flags=re.S)
        assert source_no_domain!=source
        # Change the complete RHS only; all construction inputs must stay identical.
        start=source.index('\n (∑');eq=source.index(' = ',start)
        bad_rhs=source[:eq+3]+'(2:K) * '+source[eq+3:]
        scaled=source[:eq+3]+'(3:K) * '+source[eq+3:]
        scaled=scaled.replace('∑ k ∈ Finset.range (n+1), ', '∑ k ∈ Finset.range (n+1), (3:K) * ',1)
        variants=[
            ('scaled_weight',scaled,True),
            ('renamed',re.sub(r'\b(a|c|p|q|n|k|h_domain)\b',lambda m:{'a':'alpha','c':'gamma','p':'u','q':'v','n':'length','k':'idx','h_domain':'definedTerms'}[m.group()],source),True),
            ('wrong_endpoint',bad_rhs,False),
            ('missing_finite_denominator_domain',source_no_domain,False),
        ]
        for label,text,positive in variants:
            with tempfile.TemporaryDirectory(prefix='p1-bibasic-') as directory:
                work=Path(directory)
                formula,model=frontend(extract(text,work,env),'synthetic-'+label)
                r=construct(formula,Budget(),'bibasic_gosper')
                c=r['construction'];assert c['status']=='constructed' and c['certificate']==baseline
                v=synthesize(text,model,c,work,env)
                assert v['status']==('proved' if positive else 'lean_failed'),v
                checks.append({'case':label,'status':'passed' if positive else 'rejected_by_Lean',
                               'lean_output':v['lean']['output']})
                if label=='renamed':
                    try:emit(model,dict(c,certificate='2*('+c['certificate']+')'))
                    except ValueError as exc:assert 'invalid_certificate' in str(exc)
                    else:raise AssertionError('tampered certificate accepted')
                    checks.append({'case':'tampered_certificate','status':'rejected'})
                    proof,plan=emit(model,c)
                    assert '≠ 1' not in proof and '≠ (1)' not in proof
                    assert not plan['target_used_for_representation']
        # Search schema refuses a target instead of silently accepting answer guidance.
        rejected=construct(dict(run['input_formula'],target=1),Budget(),'bibasic_gosper')
        assert 'invalid_problem' in rejected.get('error',''),rejected
        checks.append({'case':'search_rejects_target_input','status':'passed'})
        report['status']='passed'
    except Exception as exc:
        report['error']=f'{type(exc).__name__}: {exc}'
    (HERE/'generated/bibasic_tests.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='checks'},ensure_ascii=False))
    print('checks:',len(checks))
    if report['status']!='passed':raise SystemExit(1)


if __name__=='__main__':main()
