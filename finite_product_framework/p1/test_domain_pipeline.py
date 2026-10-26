"""Finite-domain, shifted-product and certificate-derived adjacent-index regressions."""
import json,os,re,tempfile
from pathlib import Path
from expressions import derive,X,q,shift_ratio,Poch,n,k
from search import search
from lean_pipeline import HERE,ROOT,extract,frontend,synthesize
import sympy as s

def main():
    report={'status':'failed','synthetic_tests_count_as_train_proofs':False,'checks':[]}
    try:
        a=s.Symbol('a')
        assert s.cancel(shift_ratio(Poch(a*q**k,q,n-k),k)-1/(1-a*q**k))==0
        assert shift_ratio(Poch(0,q,k),k)==1
        report['checks'].append({'case':'shifted_start_and_zero_start','status':'passed'})
        for identity in ['FQI-CHU-VANDERMONDE-BALANCED','FQI-CHU-VANDERMONDE-Q']:
            run=json.loads((HERE/'generated/runs'/identity/'report.json').read_text());assert run['status']=='proved'
            source=(ROOT/run['source']['path']).read_text()
            env=os.environ.copy();env['LEAN_PATH']=str(Path(run['verification']['proof_file']).parent/'deps')
            renamed=re.sub(r'\b(a|c|q|n)\b',lambda m:{'a':'u','c':'v','q':'b','n':'m'}[m.group()],source)
            with tempfile.TemporaryDirectory(prefix='p1-domain-') as directory:
                work=Path(directory)
                def trial(label,text,expected,tamper=False):
                    formula,model=frontend(extract(text,work,env),'synthetic-domain')
                    shifts=derive(formula)
                    construction=search(shifts['n_shift'],shifts['k_shift'],shifts['target_coefficient'],X,q)
                    assert construction['status']=='constructed',construction
                    if tamper:construction=dict(construction,certificate='2*('+construction['certificate']+')')
                    result=synthesize(text,model,shifts,construction,work,env)
                    assert result['status']==expected,(label,result)
                    report['checks'].append({'case':label,'status':expected,'plan':result['plan'],'lean':result['lean']})
                trial('renamed_'+identity,renamed,'proved')
                if identity.endswith('BALANCED'):
                    trial('missing_finite_denominator_hypothesis',renamed.replace('(hden : phiDefined [v] b m)',''),'lean_failed')
                    trial('tampered_shifted_tail_certificate',renamed,'lean_failed',True)
                    before,goal=renamed.split('    phi ',1)
                    lhs,rhs=goal.split(' =',1)
                    wrong=before+'    phi '+lhs+' ='+rhs.replace('poch (v/u) b m /','(2*poch (v/u) b m) /')
                    assert wrong!=renamed
                    trial('wrong_target_initial_value',wrong,'lean_failed')
                    unrestricted='''import Benchmark.Representation
open scoped BigOperators
open FiniteQBenchmark
namespace SyntheticTail
variable {K : Type*} [Field K]
theorem statement (a d q : K) (n : ℕ) :
  (∑ k ∈ Finset.range (n+1), gaussian q n k * (-d)^k * q^(k*(k-1)/2) *
    poch a q k * poch ((a*d)*q^k) q (n-k)) = poch d q n := by
  sorry
end SyntheticTail
'''
                    trial('polynomial_tail_without_nonzero_assumptions',unrestricted,'proved')
        report['status']='passed'
    except Exception as exc:report['error']=f'{type(exc).__name__}: {exc}'
    (HERE/'generated/domain_tests.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='checks'},ensure_ascii=False))
    if report['status']!='passed':raise SystemExit(1)
if __name__=='__main__':main()
