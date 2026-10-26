"""Original-statement and adversarial tests for the general finite-range exit."""
from pathlib import Path
import os,sys,json,copy,hashlib,argparse
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE));sys.path.insert(0,str(HERE.parent))
from lean_pipeline import environment,extract
from general_summation import frontend,synthesize
from run import construct_in_process
from proof_fixture import source_for
from core import CoreBudget
from workflow.contracts import accept_proof,sha

CASES={
 'geometric':('telescoping','(q : K) (hq : q ≠ 1) (n : ℕ) : (∑ k ∈ Finset.range (n+1), q^k) = (q^(n+1)-1)/(q-1)'),
 'affine_bound':('telescoping','(q : K) (hq : q ≠ 1) (n : ℕ) : (∑ k ∈ Finset.range (2*n+3), q^k) = (q^(2*n+3)-1)/(q-1)'),
 'poch_specialization':('telescoping','(a q : K) (n : ℕ) : (∑ k ∈ Finset.range n, -a*q^k*poch a q k) = poch a q n - 1'),
 'both_sums':('recurrence','(q : K) (n : ℕ) : (∑ k ∈ Finset.range n, (q^k+q^(k+1))) = (∑ k ∈ Finset.range n, (1+q)*q^k)'),
 'order_two':('recurrence','(q : K) (n : ℕ) : (∑ k ∈ Finset.range n, (q-1)*q^k) = q^n-1'),
 'order_three':('recurrence','(q : K) (n : ℕ) : (∑ k ∈ Finset.range n, ((q-1)*q^k+(q^2-1)*q^(2*k))) = q^n+q^(2*n)-2'),
 'moving_recurrence':('recurrence','(q : K) (n : ℕ) : (∑ k ∈ Finset.range (2*n+3), (q-1)*q^k) = q^(2*n+3)-1'),
}

def run(out,only=None):
 out.mkdir(parents=True,exist_ok=True)
 # A fresh environment on the first run; reuse only with exact dependency hashes.
 manifest=out/'environment_manifest.json'
 if manifest.exists():
  deps=json.loads(manifest.read_text())
  for p,d in deps['files'].items():assert sha(Path(p))==d,p
  env=dict(os.environ,LEAN_PATH=str(out/'environment/deps'))
 else:
  env,evidence=environment(out/'environment')
  files={str(p):sha(p) for p in (out/'environment').rglob('*') if p.is_file()}
  files.update({str(HERE.parents[1]/d['path']):d['sha256'] for d in evidence})
  manifest.write_text(json.dumps(dict(files=files,dependencies=evidence),indent=2))
 records=[]
 for name,(mode,target) in CASES.items():
  if only and name not in only:continue
  work=out/name;work.mkdir(exist_ok=True);source=source_for(target);p=work/'source.lean';p.write_text(source)
  raw=extract(source,work,env);problem,model=frontend(raw,name,mode)
  branch='direct_q_gosper' if mode=='telescoping' else 'general_q_zeilberger'
  result=construct_in_process(problem,CoreBudget(seconds=40,max_order=4),branch)
  (work/'construction.json').write_text(json.dumps(result,indent=2))
  v=synthesize(source,model,result['construction'],work,env)
  (work/'verification.json').write_text(json.dumps(v,indent=2))
  passed=v['status']=='proved'
  if name=='order_two':passed &= result['construction']['order']>=2
  if name=='order_three':passed &= result['construction']['order']>=3
  records.append(dict(name=name,kind='positive',passed=passed,status=v['status'],order=result['construction']['order']))
  print(name,v['status'],result['construction']['order'],flush=True)
  if passed:
   info=dict(identity='synthetic:'+name,path=str(p),snapshot=str(p),sha256=sha(p),theorem='CoreExitRegression.statement')
   report=dict(status='proved',original_identity_proved=True,remaining_obligations=[],verification=v)
   accept_proof(report,info,work)
  if only:continue
  bad=copy.deepcopy(result['construction'])
  si=next(i for i,r in enumerate(model['sides']) if r['kind']=='sum')
  bad['sides'][si]['certificates'][0]='('+bad['sides'][si]['certificates'][0]+')+1'
  try:
   badwork=out/(name+'_tampered');badwork.mkdir(exist_ok=True)
   bv=synthesize(source,model,bad,badwork,env);rejected=bv['status']!='proved'
  except ValueError as e:rejected=True;bv={'rejection':str(e)}
  (out/(name+'_tampered.json')).write_text(json.dumps(bv,indent=2))
  records.append(dict(name=name+'_tampered',kind='negative_certificate',passed=rejected))
 # End-to-end false targets and missing specialization assumptions.
 if not only:
  for name,base,target in [('false_initial','order_two',CASES['order_two'][1].replace('= q^n-1','= q^n')),
       ('wrong_tail','moving_recurrence',CASES['moving_recurrence'][1].replace('q^(2*n+3)-1','q^(2*n+2)-1')),
       ('missing_domain','geometric',CASES['geometric'][1].replace('(hq : q ≠ 1) ',''))]:
   work=out/name;work.mkdir(exist_ok=True);src=source_for(target);(work/'source.lean').write_text(src)
   raw=extract(src,work,env);problem,model=frontend(raw,name,CASES[base][0])
   res=construct_in_process(problem,CoreBudget(seconds=40,max_order=4),'direct_q_gosper' if CASES[base][0]=='telescoping' else 'general_q_zeilberger')
   v=synthesize(src,model,res['construction'],work,env);(work/'verification.json').write_text(json.dumps(v,indent=2))
   records.append(dict(name=name,kind='negative_target_or_domain',passed=v['status']!='proved',status=v['status']))
   print(name,v['status'],flush=True)
 result=dict(status='passed' if all(r['passed'] for r in records) else 'failed',records=records,
   test_split_read=False,train_batch_run=False)
 (out/('selected_validation.json' if only else 'validation.json')).write_text(json.dumps(result,indent=2))
 return result

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--only',nargs='*')
 parser.add_argument('--output',type=Path,default=HERE.parent/'generated/general_summation_20261019/regression')
 a=parser.parse_args()
 r=run(a.output.resolve(),a.only)
 sys.exit(0 if r['status']=='passed' else 1)
