"""q-Zeilberger behavioral tests; synthetic examples never count as train coverage."""
import json
import os
import re
import tempfile
from pathlib import Path
import sympy as s
from lean_pipeline import HERE, ROOT, extract, verify_proof
from run import construct
from zeilberger import ZeilbergerBudget
from zeilberger_pipeline import frontend, synthesize, emit_proof
from expressions import q, Q, X


def main():
    checks = []
    report = {'status':'failed', 'synthetic_tests_count_as_train_proofs':False, 'checks':checks}
    try:
        budget = ZeilbergerBudget(seconds=30,max_order=3)
        problem = {'schema_version':1,'source_id':'synthetic',
                   'summand':['mul',['pow',-1,'k'],['gaussian','q','n','k']]}
        result = construct(problem,budget,'general_q_zeilberger')
        c = result['construction']
        assert c['status']=='constructed' and c['order']==2 and not c['target_used_in_search']
        assert c['attempts'][0]['status']=='no_relation_at_order_in_joint_system'
        checks.append({'case':'joint_order_search_without_target','status':'passed','coefficients':c['coefficients']})
        exhausted = construct(problem,ZeilbergerBudget(max_order=1),'general_q_zeilberger')
        assert exhausted['construction']['status']=='search_exhausted'
        checks.append({'case':'order_budget_not_impossibility','status':'passed'})
        limited = construct(problem,ZeilbergerBudget(max_unknowns=1),'general_q_zeilberger')
        assert limited['construction']['status']=='resource_exhausted'
        checks.append({'case':'unknown_budget','status':'passed'})
        for d in [1,3]:
            p = dict(problem,summand=['mul',['gaussian','q','n','k'],
                ['pow','q',['div',['mul',d,'k',['sub','k',1]],2]]])
            r = construct(p,budget,'general_q_zeilberger')
            cc = r['construction']
            assert cc['status']=='constructed' and cc['order']==d, r
            symbols = {'q':q,'Q':Q,'X':X}
            R = s.sympify(cc['certificate'],locals=symbols)
            U = s.sympify(r['shifts']['k_shift'],locals=symbols)
            cs = [s.sympify(t,locals=symbols) for t in cc['coefficients']]
            vs = [s.sympify(t,locals=symbols) for t in cc['n_shift_ratios']]
            assert s.cancel(U*R.subs(X,q*X)-R-sum(a*v for a,v in zip(cs,vs)))==0
            checks.append({'case':f'order_{d}_independent_local_residual','status':'passed','coefficients':cc['coefficients']})
        run = json.loads((HERE/'generated/runs/FQI-GAUSS-ALTERNATING/report.json').read_text())
        assert run['status']=='proved' and run['branch']=='general_q_zeilberger'
        source = (ROOT/run['source']['path']).read_text()
        env = os.environ.copy()
        env['LEAN_PATH'] = str(Path(run['verification']['proof_file']).parent/'deps')
        variants = [
            ('renamed',re.sub(r'\b(q|m|j)\b',lambda m:{'q':'u','m':'length','j':'idx'}[m.group()],source),True),
            ('scaled_weight',source.replace('(-1)^j*gaussian','(3:K)*(-1)^j*gaussian')
                .replace('if m%2 = 0 then poch q (q^2) (m/2) else 0',
                         '3 * (if m%2 = 0 then poch q (q^2) (m/2) else 0)'),True),
            ('wrong_even_initial',source.replace('then poch q','then 2 * poch q'),False),
            ('wrong_odd_target',source.replace('else 0 := by','else 1 := by'),False),
        ]
        for label,text,positive in variants:
            with tempfile.TemporaryDirectory(prefix='p1-zeil-') as directory:
                work=Path(directory)
                raw=extract(text,work,env)
                p,model=frontend(raw,'synthetic-'+label)
                r=construct(p,budget,'general_q_zeilberger')
                assert r['construction']['status']=='constructed'
                # Changing the target cannot influence symbolic search.
                assert r['construction']['coefficients']==c['coefficients']
                assert r['construction']['certificate']==c['certificate']
                v=synthesize(text,model,r['construction'],work,env)
                assert v['status']==('proved' if positive else 'lean_failed'),v
                checks.append({'case':label,'status':'passed' if positive else 'rejected_by_Lean',
                               'lean_output':v['lean']['output']})
                if label=='renamed':
                    bad=dict(r['construction'],certificate='2*('+c['certificate']+')')
                    try:
                        synthesize(text,model,bad,work,env)
                    except ValueError as exc:
                        assert 'local relation requires' in str(exc)
                    else:
                        raise AssertionError('tampered certificate accepted')
                    checks.append({'case':'tampered_certificate','status':'rejected_by_local_verifier'})
                    bad=dict(r['construction'],coefficients=['1',*c['coefficients'][1:]])
                    try:
                        synthesize(text,model,bad,work,env)
                    except ValueError as exc:
                        assert 'local relation requires' in str(exc)
                    else:
                        raise AssertionError('tampered recurrence accepted')
                    checks.append({'case':'tampered_recurrence','status':'rejected_by_local_verifier'})
                    proof,plan=emit_proof(model,r['construction'])
                    v=verify_proof(text,proof.replace('| 0 => 0','| 0 => 1'),plan,work,env)
                    assert v['status']=='lean_failed'
                    checks.append({'case':'tampered_flux_endpoint','status':'rejected_by_Lean'})
        # Reuse the first-order emitter, with the coefficient found without the RHS.
        old=json.loads((HERE/'generated/runs/FQI-FINITE-Q-BINOMIAL/report.json').read_text())
        text=(ROOT/old['source']['path']).read_text()
        with tempfile.TemporaryDirectory(prefix='p1-zeil-first-') as directory:
            work=Path(directory)
            p,model=frontend(extract(text,work,env),'synthetic-first-order')
            r=construct(p,budget,'general_q_zeilberger')
            assert r['construction']['order']==1
            v=synthesize(text,model,r['construction'],work,env)
            assert v['status']=='proved',v
            checks.append({'case':'first_order_without_target_guidance','status':'passed'})
        report['status']='passed'
    except Exception as exc:
        report['error']=f'{type(exc).__name__}: {exc}'
    (HERE/'generated/zeilberger_tests.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='checks'},ensure_ascii=False))
    print('checks:',len(checks))
    if report['status']!='passed': raise SystemExit(1)


if __name__=='__main__':
    main()
