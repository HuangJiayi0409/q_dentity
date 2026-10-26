"""Certificate/target rejection and source-renaming tests for defined relations.
Run with --environment pointing to a prepared P1 environment.json and --output
pointing to a new validation directory. Reads only the specified Train example.
"""
from pathlib import Path
import argparse,json,os,sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from workflow.contracts import ROOT
from lean_pipeline import extract,verify_proof,HERE
from zeilberger import ZeilbergerBudget
import defined_relation as relation
parser=argparse.ArgumentParser()
parser.add_argument('--environment',type=Path,required=True)
parser.add_argument('--output',type=Path,required=True)
args=parser.parse_args()
out=args.output.resolve();out.mkdir(parents=True,exist_ok=False)
env=dict(os.environ,LEAN_PATH=json.loads(args.environment.read_text())['lean_path'])
row=next(r for r in map(json.loads,(ROOT/'benchmark/splits/train.jsonl').read_text().splitlines()) if r['id']=='FQI-ROGERS-SZEGO-RECURRENCE')
source=(ROOT/'benchmark'/row['lean_path']).read_text()
original=out/'original';original.mkdir()
raw=extract(source,original,env)
problem,m=relation.prepare(raw,row['id'],original,env)
c=relation.construct(problem,ZeilbergerBudget(seconds=120,max_order=3))['construction']
assert c['status']=='constructed' and c['target_used_in_search'] is False
(out/'construction.json').write_text(json.dumps(c,indent=2))
import copy,re
results=[]
for name in ['bad_certificate','bad_coefficients','wrong_target']:
 model=copy.deepcopy(m);cert=copy.deepcopy(c)
 if name=='bad_certificate':cert['certificate']='2*('+cert['certificate']+')'
 elif name=='bad_coefficients':cert['coefficients'][0]='1+('+cert['coefficients'][0]+')'
 else:
  # Add a nonzero constant to the actual exported RHS.
  rhs=model['relation_raw']['args'][1]
  model['relation_raw']['args'][1]={'op':'HAdd.hAdd','args':[rhs,{'op':'nat','value':1}]}
 try:relation.emit(model,cert)
 except ValueError as e:results.append(dict(case=name,status='rejected',reason=str(e)))
 else:raise AssertionError(name+' accepted')
for name in ['renamed','scaled','missing_lower_bound']:
 text=source
 if name=='renamed':text=re.sub(r'\b(q|t)\b',lambda m:{'q':'baseParam','t':'weightParam'}[m[0]],text)
 elif name=='scaled':
  text=text.replace(' rogersSzego t q (n+1) = (1+t)*rogersSzego t q n-(1-q^n)*t*rogersSzego t q (n-1)',
   ' (3:K)*rogersSzego t q (n+1) = 3*((1+t)*rogersSzego t q n-(1-q^n)*t*rogersSzego t q (n-1))')
 else:text=text.replace(' (hn : 1 ≤ n)','')
 w=out/name;w.mkdir(parents=True,exist_ok=True)
 raw=extract(text,w,env);p,model=relation.prepare(raw,'synthetic-'+name,w,env)
 # Canonical variable naming makes the same independently computed certificate applicable.
 proof,plan=relation.emit(model,c)
 v=verify_proof(text,proof,plan,w,env,[(HERE/'lean/OreRules.lean').read_text()])
 (w/'verification.json').write_text(json.dumps(v,indent=2))
 assert (v['status']=='proved')==(name!='missing_lower_bound'),(name,v['status'])
 results.append(dict(case=name,status=v['status'],verification=str(w/'verification.json')))
 print(name,v['status'],flush=True)
(out/'validation.json').write_text(json.dumps(results,indent=2))
print('passed',len(results))
