#!/usr/bin/env python3
"""Audit all twelve original goals before extending their proof construction."""
import json,sys,re,hashlib
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
HERE=Path(__file__).resolve().parent;P1=HERE.parents[1];sys.path.insert(0,str(P1))
from run import ROOT,load_target,prepare_batch,batch_environment,run
from lean_pipeline import assemble,proof_slot,lean

def write(path,data):path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
def main():
    selection=HERE/'selection.json'
    if not selection.exists():
        rows=json.loads((P1/'research/trials41/table.json').read_text())['records']
        done={c['id'] for c in json.loads((P1/'cases.json').read_text())['cases'] if c['status']=='proved'}
        ids=[r['id'] for r in rows if r['status']=='all_local_certificates_constructed' and r['id'] not in done]
        assert len(ids)==12;write(selection,{'identities':ids,'initial_complete_train_proofs':5})
    ids=json.loads(selection.read_text())['identities'];assert len(ids)==12
    prepared=prepare_batch(HERE/'shared')
    write(HERE/'dependencies.json',{k:prepared[k] for k in ('dependencies','artifacts')})
    prelude='''import Lean
open Lean Elab Tactic Meta
elab "p1_typecheck" : tactic => withMainContext do
  logInfo m!"P1_ELABORATED_GOAL: {← getMainTarget}"
  throwError "P1_TYPECHECK_ONLY"
'''
    def task(identity):
        source=load_target(identity);work=HERE/identity;work.mkdir(exist_ok=True)
        env,_=batch_environment(prepared)
        path=work/'Typecheck.lean'
        path.write_text(assemble([prelude,proof_slot((ROOT/source['path']).read_text(),'  p1_typecheck')]))
        result=lean(path,env)
        # One deliberate error is expected. Any other error is a genuine issue.
        typed=(len(re.findall(r'\berror:',result['output']))==1 and 'P1_TYPECHECK_ONLY' in result['output'])
        report={'id':identity,'source':source,'well_typed_original_goal':typed,
                'typecheck':result,'is_proof':False}
        write(work/'typecheck.json',report)
        native=run(identity,prepared=prepared,output_root=HERE/'native')
        write(work/'native.json',native)
        report['native_status']=native['status']
        print(identity,typed,native['status'],flush=True)
        return report
    with ThreadPoolExecutor(max_workers=3) as pool:reports=list(pool.map(task,ids))
    write(HERE/'audit.json',{'records':reports,'complete_proofs':sum(r['native_status']=='proved' for r in reports)})

if __name__=='__main__':main()
