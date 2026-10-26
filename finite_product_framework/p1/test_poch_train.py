"""Four selected original Train declarations through existing production entries."""
import os,sys,json,re,subprocess
from pathlib import Path
fw=Path(__file__).resolve().parent.parent;root=fw.parent
sys.path[:0]=[str(fw),str(fw/'p1')]
from lean_pipeline import extract
from general_summation import recurrence_frontend,telescoping_frontend
from run import construct_in_process
from zeilberger_pipeline import synthesize as zs
from direct import synthesize as ds
from core import CoreBudget
from workflow.contracts import sha,accept_proof

def run(out=None):
    out=out or fw/'generated/recurrence_full_20261019/final_train'
    out.mkdir(parents=True,exist_ok=True)
    base=fw/'generated/recurrence_full_20261019/regression'
    manifest=json.loads((base/'environment_manifest.json').read_text())
    for p,d in manifest['files'].items():assert sha(p)==d
    rows={r['id']:r for r in map(json.loads,open(root/'benchmark/splits/train.jsonl'))}
    records=[]
    for identity,mode in [('FQI-FINITE-Q-BINOMIAL','recurrence'),('FQI-SRC-AP-3.3.9','telescoping'),('FQI-CHU-VANDERMONDE-Q','recurrence'),('FQI-PFAFF-SAALSCHUETZ','recurrence')]:
     work=out/identity;work.mkdir(exist_ok=True)
     row=rows[identity];p=root/'benchmark'/row['lean_path'];assert sha(p)==row['lean_sha256'];src=p.read_text();(work/'source.lean').write_text(src)
     report=dict(identity=identity,mode=mode,status='failed',original_identity_proved=False,remaining_obligations=['unverified'])
     try:
      env=dict(os.environ,LEAN_PATH=str(base/'environment/deps'))
      raw=extract(src,work,env);problem,model=(recurrence_frontend if mode=='recurrence' else telescoping_frontend)(raw,identity)
      report['representation']=model.get('mode','legacy');report['problem']=problem
      result=construct_in_process(problem,CoreBudget(seconds=40,max_order=4),'general_q_zeilberger' if mode=='recurrence' else 'direct_q_gosper');report.update(result)
      if result['construction']['status']=='constructed':
       v=(zs if mode=='recurrence' else ds)(src,model,result['construction'],work,env);report['verification']=v;report['status']=v['status']
       if v['status']=='proved':
        report.update(original_identity_proved=True,remaining_obligations=[])
        info=dict(identity=identity,path=str(p.relative_to(root)),snapshot=str(work/'source.lean'),sha256=sha(p),theorem='.'.join(re.findall(r'^namespace\s+(\S+)',src,re.M)+re.findall(r'^theorem\s+(\S+)',src,re.M)))
        report['acceptance']=accept_proof(report,info,work)
      else:report['status']=result['construction']['status']
     except (ValueError,KeyError,NotImplementedError,subprocess.TimeoutExpired) as e:report.update(status='unsupported_or_unverified',reason=str(e))
     (work/'report.json').write_text(json.dumps(report,indent=2));records.append({k:v for k,v in report.items() if k in ('identity','mode','status','representation','reason','original_identity_proved')});print(records[-1],flush=True)
    result=dict(status='passed' if all(r['status']=='proved' for r in records) else 'failed',records=records,test_split_read=False,train_batch_run=False)
    (out/'validation.json').write_text(json.dumps(result,indent=2))
    return result

if __name__=='__main__':
    sys.exit(run()['status']!='passed')
