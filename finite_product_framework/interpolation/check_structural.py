"""Complete source-to-original-proof checks for symbolic structural constructors."""
import concurrent.futures
import json
import os
from pathlib import Path
import sys
import uuid
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from workflow.contracts import HERE,ROOT,save,sha,accept_proof
from interpolation.pipeline import environment,PREP,probe,prove_source

FIELD='{K : Type*} [Field K]'
SHIFT=FIELD+' (a q : K) (n : ℕ) (s : ℤ) (ha : a≠0) (hq : regular q)'
LAGRANGE=FIELD+' (n : ℕ) (v : Fin (n+1) → K) (hv : Function.Injective v) (P : Polynomial K) (hp : P.natDegree≤n) (x : K)'
LHS='(∑ i : Fin (n+1), P.eval (v i) / (∏ j ∈ Finset.univ.erase i, (v i-v j)) * (∏ j ∈ Finset.univ.erase i, (x-v j)))'
PRINCIPAL='(∑ i : Fin (n+1), (P.eval (v i) / (∏ j ∈ Finset.univ.erase i, (v i-v j))) / (x-v i))'
PARAM=FIELD+' (r n : ℕ) (q x : K) (bs : Fin r → K) (ms : Fin r → ℕ) (hn : (∑ j, ms j)≤n) (v : Fin (n+1) → K) (hv : Function.Injective v)'
PARAMVAL='(∏ j, poch (bs j*x) q (ms j))'
PARAMSUM=LHS.replace('P.eval (v i)','(∏ j, poch (bs j*v i) q (ms j))')
PARAMPRINCIPAL=PRINCIPAL.replace('P.eval (v i)','(∏ j, poch (bs j*v i) q (ms j))')
CASES=[
 ('integer_shift',SHIFT,'poch (a*q^s) q n = (-a)^n*q^(s*(n:ℤ)+(n:ℤ)*((n:ℤ)-1)/2)*poch (q^(1-s-(n:ℤ))/a) q n','polynomial_interpolation','shift_reciprocal'),
 ('shift_missing_a_nonzero',SHIFT.replace(' (ha : a≠0)',''),'poch (a*q^s) q n = (-a)^n*q^(s*(n:ℤ)+(n:ℤ)*((n:ℤ)-1)/2)*poch (q^(1-s-(n:ℤ))/a) q n','polynomial_interpolation',None),
 ('shift_wrong_exponent',SHIFT,'poch (a*q^s) q n = (-a)^n*q^(s*(n:ℤ)+(n:ℤ)*((n:ℤ)-1)/2+1)*poch (q^(1-s-(n:ℤ))/a) q n','polynomial_interpolation',None),
 ('negative_block',FIELD+' (u t : K) (m n : ℕ) (hu : u≠0) (ht : regular t) (hn : n≤m) (hd : poch (t/u) t (m-n)≠0)',
  'poch (u*t^(-(m:ℤ))) t n = (poch (t/u) t m / poch (t/u) t (m-n)) * (-u)^n*t^((n:ℤ)*((n:ℤ)-1)/2-(m:ℤ)*(n:ℤ))','polynomial_interpolation','negative_block'),
 ('shift_cross',FIELD+' (u t : K) (m n : ℕ) (ht : regular t)',
  'poch (u*t^m) t n * poch u t m = poch (u*t^n) t m * poch u t n','polynomial_interpolation','shift_cross'),
 ('lagrange',LAGRANGE,LHS+'=P.eval x','polynomial_interpolation','polynomial_lagrange'),
 ('lagrange_reversed',LAGRANGE,'P.eval x='+LHS,'polynomial_interpolation','polynomial_lagrange'),
 ('lagrange_at_node',LAGRANGE,LHS.replace('(x-v j)','(v 0-v j)')+'=P.eval (v 0)','polynomial_interpolation','polynomial_lagrange'),
 ('lagrange_missing_injectivity',LAGRANGE.replace(' (hv : Function.Injective v)',''),LHS+'=P.eval x','polynomial_interpolation',None),
 ('lagrange_missing_degree',LAGRANGE.replace(' (hp : P.natDegree≤n)',''),LHS+'=P.eval x','polynomial_interpolation',None),
 ('lagrange_wrong_weights',LAGRANGE,LHS.replace('(v i-v j)','(v i+v j)')+'=P.eval x','polynomial_interpolation',None),
 ('poch_family',PARAM,PARAMSUM+'='+PARAMVAL,'polynomial_interpolation','poch_lagrange'),
 ('poch_family_zero_base',PARAM,PARAMSUM.replace(' q (ms j)',' 0 (ms j)')+'='+PARAMVAL.replace(' q (ms j)',' 0 (ms j)'), 'polynomial_interpolation','poch_lagrange'),
 ('poch_family_zero_parameters',PARAM.replace('(r n : ℕ)','(n : ℕ)').replace('Fin r','Fin 0'),PARAMSUM+'='+PARAMVAL,'polynomial_interpolation','poch_lagrange'),
 ('principal_family',LAGRANGE+' (hx : ∀ i, x≠v i)',PRINCIPAL+'= P.eval x / (∏ j, (x-v j))','rational_principal_parts','polynomial_principal_family'),
 ('principal_missing_domain',LAGRANGE,PRINCIPAL+'= P.eval x / (∏ j, (x-v j))','rational_principal_parts',None),
 ('poch_principal_family',PARAM+' (hx : ∀ i, x≠v i)',PARAMPRINCIPAL+'='+PARAMVAL+'/(∏ j, (x-v j))','rational_principal_parts','poch_principal_family'),
 ('square_merge',FIELD+' (u t : K) (n : ℕ) (ht : regular t)','poch (u^2) (t^2) n = poch u t n * poch (-u) t n','polynomial_interpolation','square_multiplicity'),
 ('square_wrong_sign',FIELD+' (u t : K) (n : ℕ) (ht : regular t)','poch (u^2) (t^2) n = poch u t n * poch u t n','polynomial_interpolation',None),
 ('multiplicity_certificate',FIELD+' (r : ℕ) (P : Polynomial K) (v : Fin r → K) (hv : Function.Injective v) (m : Fin r → ℕ) (hd : P.natDegree < ∑ i, m i) (hr : ∀ i, (Polynomial.X-Polynomial.C (v i))^(m i) ∣ P)',
 'P=0','polynomial_interpolation','multiplicity_zero'),
 ('multiplicity_missing_separation',FIELD+' (r : ℕ) (P : Polynomial K) (v : Fin r → K) (m : Fin r → ℕ) (hd : P.natDegree < ∑ i, m i) (hr : ∀ i, (Polynomial.X-Polynomial.C (v i))^(m i) ∣ P)',
 'P=0','polynomial_interpolation',None),
]

# Symbolic geometric interpolation weights and their original phi source bridge.
KM=FIELD+' (q b : K) (r n : ℕ) (bs : Fin r → K) (ms : Fin r → ℕ) (hq : regular q) (hb : b≠0) (hn : (∑ i, ms i)≤n) (hd : phiDefined (b*q :: List.ofFn bs) q n) (hr : ∀ i, poch (bs i) q (ms i)≠0)'
KML='phi (q^(-(n:ℤ)) :: b :: List.ofFn (fun i => bs i*q^(ms i))) (b*q :: List.ofFn bs) q q n'
KMR='b^n*poch q q n/poch (b*q) q n * ∏ i, poch (bs i/b) q (ms i)/poch (bs i) q (ms i)'
GEO=FIELD+' (q b : K) (n : ℕ) (hq : regular q) (hb : b≠0) (hd : poch (b*q) q n≠0) (P : Polynomial K) (hp : P.natDegree≤n)'
GEOL='(∑ k : Fin (n+1), (poch (q^(-(n:ℤ))) q k.val * poch b q k.val / (poch q q k.val * poch (b*q) q k.val)) * q^k.val * P.eval (q^k.val))'
GEOR='(b^n*poch q q n/poch (b*q) q n) * P.eval (1/b)'
for name,binders,target,label in [
 ('shifted_phi',KM,KML+'='+KMR,'shifted_parameter_phi'),
 ('shifted_phi_reversed',KM,KMR+'='+KML,'shifted_parameter_phi'),
 ('shifted_phi_empty_family',KM.replace('(r n : ℕ)','(n : ℕ)').replace('Fin r','Fin 0'),KML+'='+KMR,'shifted_parameter_phi'),
 ('shifted_phi_zero_length',KM.replace('(r n : ℕ)','(r : ℕ)').replace('≤n','≤0').replace(' q n)',' q 0)'),(KML+'='+KMR).replace('(n:ℤ)','(0:ℤ)').replace(' q n',' q 0').replace('b^n','b^0'),'shifted_parameter_phi'),
 ('shifted_phi_missing_degree',KM.replace(' (hn : (∑ i, ms i)≤n)',''),KML+'='+KMR,None),
 ('shifted_phi_missing_domain',KM.replace(' (hd : phiDefined (b*q :: List.ofFn bs) q n)',''),KML+'='+KMR,None),
 ('shifted_phi_missing_parameter_domain',KM.replace(' (hr : ∀ i, poch (bs i) q (ms i)≠0)',''),KML+'='+KMR,None),
 ('shifted_phi_missing_regular',KM.replace(' (hq : regular q)',''),KML+'='+KMR,None),
 ('shifted_phi_missing_b_nonzero',KM.replace(' (hb : b≠0)',''),KML+'='+KMR,None),
 ('shifted_phi_wrong_weight',KM,KML.replace(' q q n',' q (q^2) n')+'='+KMR,None),
 ('geometric_polynomial',GEO,GEOL+'='+GEOR,'geometric_polynomial_sum'),
 ('geometric_polynomial_missing_degree',GEO.replace(' (hp : P.natDegree≤n)',''),GEOL+'='+GEOR,None),
]:
 CASES.append((name,binders,target,'polynomial_interpolation',label))
# Specializations retain the original permitted degenerate parameter values.
import re
for name,old,new,binders in [
 ('shifted_phi_b_one','b','(1:K)',KM.replace('(q b : K)','(q : K)')),
 ('shifted_phi_zero_parameters','bs','(fun _ : Fin r => (0:K))',KM.replace(' (bs : Fin r → K)','')),
 ('shifted_phi_zero_shifts','ms','(fun _ : Fin r => (0:ℕ))',KM.replace(' (ms : Fin r → ℕ)','')),
]:
 sub=lambda text:re.sub(r'\b'+old+r'\b',lambda _:new,text)
 CASES.append((name,sub(binders),sub(KML+'='+KMR),'polynomial_interpolation','shifted_parameter_phi'))
# Rename every mathematical parameter to check that recognition is structural.
rename={'q':'t','b':'c','r':'d','n':'N','bs':'us','ms':'ls'}
sub=lambda text:re.sub(r'\b(q|b|r|n|bs|ms)\b',lambda m:rename[m[0]],text)
CASES.append(('shifted_phi_renamed',sub(KM),sub(KML+'='+KMR),'polynomial_interpolation','shifted_parameter_phi'))

def main():
 work=HERE/'generated/interpolation_structural_checks'/uuid.uuid4().hex;work.mkdir(parents=True)
 build=work/'build';build.mkdir();env,deps=environment(build)
 def run(case):
  name,binders,target,backend,expected=case
  dest=work/name;dest.mkdir()
  text=('import Benchmark.Representation\nopen scoped BigOperators\nopen FiniteQBenchmark\n'
        'set_option autoImplicit false\nnamespace StructuralRegression\n'
        f'theorem statement {binders} : {target} := by\n  sorry\nend StructuralRegression\n')
  src=dest/'source.lean';src.write_text(text)
  snapshot={'path':str(src.relative_to(ROOT)),'snapshot':str(src),'sha256':sha(src),'theorem':'StructuralRegression.statement'}
  try:
   initial=probe(text,PREP+'\ninterpolation_export "initial"',dest,env,'Initial')['initial']
   data={'dependencies':deps,'initial':initial,'source_text_sha256':sha(src)}
   result=prove_source(text,snapshot,dest,env,data,{'max_degree':8,'symbolic_seconds':60},backend)
   labels=result.get('symbolic_attempt',{}).get('constructors',[])
   if result['status']=='proved':accept_proof(result,snapshot,dest)
   passed=(result['status']=='proved')==(expected is not None)
   if expected is not None:passed=passed and expected in labels
   return dict(name=name,passed=passed,status=result['status'],expected_constructor=expected,constructors=labels,report=str(dest/'interpolation_report.json'))
  except Exception as exc:return dict(name=name,passed=False,error=repr(exc))
 report={'status':'running','cases':[],'work_directory':str(work),'train_proofs_counted':0}
 with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
  for row in ex.map(run,CASES):
   report['cases'].append(row);save(work/'report.json',report);print(row['name'],row['passed'],row.get('status',row.get('error')),flush=True)
 report['status']='passed' if all(x['passed'] for x in report['cases']) else 'failed'
 save(work/'report.json',report);save(HERE/'generated/interpolation_structural_validation.json',report)
 print('REPORT',work/'report.json',report['status'],flush=True)
 return 0 if report['status']=='passed' else 1
if __name__=='__main__':raise SystemExit(main())
