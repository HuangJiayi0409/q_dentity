"""q-Ore algebra, closure and native proof acceptance/rejection (train only)."""
import copy
import json
import os
import re
import tempfile
from pathlib import Path
import sympy as s
from ore import *
from ore_pipeline import prepare,synthesize,emit
from lean_pipeline import HERE,ROOT,extract
from run import construct
from qgosper import Budget


def main():
    parse=lambda v:s.sympify(v,locals={'q':q,'Q':Q})
    checks=[];report={'status':'failed','synthetic_tests_count_as_train_proofs':False,'checks':checks}
    def passed(label):checks.append({'case':label,'status':'passed'})
    try:
        assert multiply([0,1],[Q])==[0,q*Q]
        assert multiply([Q],[0,1])==[0,Q]
        passed('noncommutative_q_shift')
        for a,b in [([-Q,1],[-1,1]),([1,Q,1],[Q,1])]:
            r=common_left_multiple(a,b)
            U=list(map(parse,r['left_multiplier']));V=list(map(parse,r['right_multiplier']))
            assert multiply(U,a)==multiply(V,b)==list(map(parse,r['operator']))
        passed('common_left_multiple_witnesses')
        a=s.Symbol('a');M=companion([Q,-a,1])
        for degree in (2,3):
            T,powers,u=polynomial_closure(M,degree)
            state=s.Matrix([s.prod(v**e for v,e in zip(u,m)) for m in powers]);next_u=M*s.Matrix(u)
            expected=s.Matrix([s.prod(v**e for v,e in zip(next_u,m)) for m in powers])
            assert (T*state-expected).applyfunc(s.expand)==s.zeros(T.rows,1)
            row=observable_row(u[0]**degree+u[1]**degree,u,powers)
            r=eliminate(T,row)
            coeff=list(map(parse,r['coefficients']))
            assert sum((c*iterate_row(row,T,j) for j,c in enumerate(coeff)),s.zeros(1,T.rows)).applyfunc(s.cancel)==s.zeros(1,T.rows)
            passed(f'polynomial_degree_{degree}_closure_and_elimination')
        A=s.Matrix([[1+Q]]);B=s.Matrix([[2+Q]])
        assert tensor_product(A,B)==s.Matrix([[(1+Q)*(2+Q)]])
        assert direct_sum(A,B)==s.diag(1+Q,2+Q)
        passed('sum_and_product_state_composition')
        try:polynomial_closure(M,3,max_states=2)
        except ValueError as exc:assert 'resource_exhausted' in str(exc)
        else:raise AssertionError('state budget ignored')
        try:companion([s.Float(0.5),1])
        except ValueError as exc:assert 'unsupported_domain' in str(exc)
        else:raise AssertionError('inexact coefficients accepted')
        passed('state_budget_and_exact_domain')
        run=json.loads((HERE/'generated/runs/FQI-SRC-GR2-7.Ex40/report.json').read_text())
        assert run['status']=='proved' and run['branch']=='ore_closure'
        source=(ROOT/run['source']['path']).read_text();baseline=run['construction']
        env=os.environ.copy();env['LEAN_PATH']=str(Path(run['verification']['proof_file']).parent/'deps')
        wrong=source.replace('= (((1 - q)', '= (((2 - q)')
        assert wrong!=source
        no_base=source.replace('(hbase : regular q)', '')
        scaled=source.replace(' (((rogersSzego', ' (3:K) * (((rogersSzego',1)
        scaled=scaled.replace('∑ k ∈ Finset.Icc (1) (n), ', '∑ k ∈ Finset.Icc (1) (n), (3:K) * ',1)
        variants=[('renamed',re.sub(r'\b(x|q|n|k|hbase|hn)\b',lambda m:{'x':'z','q':'u','n':'length','k':'idx','hbase':'baseCondition','hn':'positiveLength'}[m.group()],source),True),
                  ('scaled_observable_and_weight',scaled,True),('wrong_initial_and_weight',wrong,False),('missing_base_domain',no_base,False)]
        for label,text,positive in variants:
            with tempfile.TemporaryDirectory(prefix='p1-ore-') as directory:
                work=Path(directory);raw=extract(text,work,env);f,model=prepare(raw,'synthetic-'+label,work,env)
                result=construct(f,Budget(),'ore_closure');c=result['construction'];assert c['status']=='constructed'
                assert c['base_recurrence']['coefficients']==baseline['base_recurrence']['coefficients']
                assert c['base_recurrence']['certificate']==baseline['base_recurrence']['certificate']
                if label in ('wrong_initial_and_weight','missing_base_domain'):
                    assert c['forced_relation']==baseline['forced_relation']
                v=synthesize(text,model,c,work,env)
                assert v['status']==('proved' if positive else 'lean_failed'),v
                checks.append({'case':label,'status':'passed' if positive else 'rejected_by_Lean','lean_output':v['lean']['output']})
                if label=='renamed':
                    mutations=[('base_certificate','base_recurrence','certificate'),
                               ('forced_relation','forced_relation','forcing_coefficient'),
                               ('eliminated_operator','observable_operator','coefficients')]
                    for name,section,field in mutations:
                        bad=copy.deepcopy(c)
                        if field=='coefficients':bad[section][field][0]='1+('+bad[section][field][0]+')'
                        else:bad[section][field]='1+('+bad[section][field]+')'
                        try:emit(model,bad)
                        except ValueError as exc:assert 'invalid_certificate' in str(exc),str(exc)
                        else:raise AssertionError('tamper accepted: '+name)
                        checks.append({'case':'tampered_'+name,'status':'rejected'})
        report['status']='passed'
    except Exception as exc:report['error']=f'{type(exc).__name__}: {exc}'
    (HERE/'generated/ore_tests.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='checks'},ensure_ascii=False))
    print('checks:',len(checks))
    if report['status']!='passed':raise SystemExit(1)


if __name__=='__main__':main()
