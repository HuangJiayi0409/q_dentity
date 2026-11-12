"""Real single-Train local method, actual Lean rejection and fresh CLI replay.

Used separately for each newly integrated method. No checker/core substitutes.
"""
import argparse
from dataclasses import replace
import json
from pathlib import Path
import subprocess
import sys
import time

from agent_v2.cli import positive_float
from agent_v2.executor import _candidate_request,normalize_result,validate_invariant,verify_and_update
from agent_v2.lean_checker import LeanChecker
from agent_v2.method_registry import builtin_registry
from agent_v2.models import JointAction,ResidualState,thaw
from agent_v2.storage import RunStore,guard_path,sha256_file,verify_source

ROOT=Path(__file__).resolve().parents[2]


def require(value,message):
    if not value:raise RuntimeError(message)


def save(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(thaw(value),ensure_ascii=False,indent=2)+'\n')


def cli(command,output,label,seconds):
    began=time.monotonic()
    result=subprocess.run([sys.executable,'-m','agent_v2.cli',*command],cwd=ROOT,
        capture_output=True,text=True,timeout=seconds+60)
    record={'command':[sys.executable,'-m','agent_v2.cli',*command],
        'returncode':result.returncode,'stdout':result.stdout,'stderr':result.stderr,
        'wall_seconds':time.monotonic()-began}
    save(output/(label+'.json'),record)
    require(result.returncode==2,label+': expected incomplete CLI exit2')
    summary=json.loads(result.stdout.splitlines()[-1])
    require(summary['status']=='incomplete' and summary['original_identity_proved'] is False,
            label+': local proof was mislabeled original success')
    return RunStore(summary['run_dir']),record


def receipt(evidence,source,profile):
    require(evidence.get('returncode')==0 and evidence.get('source_sha256')==source.sha256,
            'missing actual Lean receipt or wrong Source')
    require(evidence.get('profile')==profile and evidence.get('profile_version')=='1','wrong profile')
    audit=evidence.get('audit',{})
    require(audit.get('theorem')=='AgentV2Candidate.proof','wrong audited theorem')
    require(set(audit.get('axioms',[]))<={'propext','Classical.choice','Quot.sound'},'unapproved axioms')
    paths=[Path(x['path']) for x in evidence.get('artifacts',[])]
    require(any(p.name=='Candidate.lean' for p in paths) and any(p.name=='Candidate.olean' for p in paths)
            and any(p.name=='stdout.jsonl' for p in paths),'retained proof artifacts missing')


def acceptance(args,output):
    spec=builtin_registry().get(args.method)
    require(spec.capability_level=='L3' and spec.local_lean and not spec.full_original,
            'this smoke is only for a newly registered local-only L3')
    command=['run','--identity',args.identity,'--method',args.method,'--scope','local',
        '--max-steps','1','--seconds',str(args.seconds),'--output-root',str(output/'runs')]
    store,run_command=cli(command,output,'cli_run',args.seconds)
    initial=ResidualState.from_dict(store.read_json('initial_state.json'))
    first=ResidualState.from_dict(store.load_checkpoint()['state'])
    validate_invariant(first);verify_source(first.G,store.root)
    require(first.G==initial.G and first.Gamma==initial.Gamma and first.r==initial.r,'original changed')
    require(len(first.C)==1 and first.O==initial.O==(initial.root,) and not first.links,'local boundary crossed')
    require(first.round_index==1 and first.b.actions==0 and first.b.seconds<initial.b.seconds,'wrong action budget')
    require(store.read_json('run.json')['stop_reason']=='local_certificate_verified_original_open','wrong stop reason')
    result=normalize_result(store.read_json('rounds/1/result.json'))
    require(result.status=='symbolic_constructed' and len(result.C_partial)==1 and not result.O_res,
            'one pending formal candidate required')
    require(result.raw_result['core']['status']=='constructed','actual core did not construct')
    translation=result.raw_result['translation']
    require(translation['independent_symbolic_check']['status']=='passed' and translation['lean_verified'] is False,
            'symbolic construction bypassed independent checking or claimed Lean acceptance')
    candidate=result.C_partial[0]
    require(candidate.closes is None and not candidate.dependencies and not candidate.replaces,
            'local candidate must not change original obligations')
    receipt(first.C[0].evidence,first.G,spec.lean_profile)
    records=[result.to_dict(),first.C[0].to_dict()['evidence']]
    _,resume_command=cli(['resume','--run-dir',str(store.root)],output,'cli_resume',args.seconds)
    replay=ResidualState.from_dict(store.load_checkpoint()['state'])
    validate_invariant(replay);verify_source(replay.G,store.root)
    require(replay.round_index==1 and replay.b.actions==0 and replay.O==first.O and replay.links==first.links,
            'resume repeated an action or changed obligations')
    require(len(replay.C)==1 and replace(first.C[0],evidence=replay.C[0].evidence)==replay.C[0],
            'resume changed mathematical certificate')
    require(replay.C[0].evidence['artifacts']!=first.C[0].evidence['artifacts'] and replay.b.seconds<first.b.seconds,
            'fresh replay was skipped or not charged')
    require(len(list(store.path('resume_checks').glob('*/result.json')))==1,'one fresh replay check required')
    receipt(replay.C[0].evidence,replay.G,spec.lean_profile);records.append(replay.C[0].to_dict()['evidence'])

    # Negative mathematical proof preserves all legitimate IDs/types/Source.
    action=JointAction.from_dict(store.read_json('rounds/1/action.json'))
    wrong=replace(candidate,proof_term='by exact True.intro')
    negative=replace(result,C_partial=(wrong,),artifacts=())
    context={'source_sha256':initial.G.sha256,'run_dir':str(store.root),
        'attempt_dir':str(store.path('negative-proof')),'seconds':args.seconds}
    began=time.monotonic();after,checks=verify_and_update(initial,action,negative,LeanChecker(),context)
    save(store.path('negative-proof/candidate.json'),wrong.to_dict())
    save(store.path('negative-proof/verification.json'),{'checks':checks,'wall_seconds':time.monotonic()-began,
        'scope':'diagnostic probe; not an additional committed runtime action'})
    save(store.path('negative-proof/state_before.json'),initial.to_dict())
    save(store.path('negative-proof/state_after.json'),after.to_dict())
    require(after==initial,'wrong proof changed C/O/links')
    checked=[x['check'] for x in checks if 'check' in x]
    require(len(checked)==1 and checked[0]['accepted'] is False and checked[0]['status']=='incomplete'
        and checked[0]['sigma']['code']=='lean_check_failed'
        and checked[0]['evidence'].get('returncode') not in (None,0),'negative did not reach actual Lean rejection')
    records.append(checked[0]['evidence'])
    tamper_context=dict(context,source=initial.G.to_dict(),attempt_dir=str(store.path('binding-negative')))
    request=_candidate_request(candidate);tamper=[]
    for key,value in [('source_sha256','0'*64),('proposition','True'),('dependencies',['foreign']),('id','renamed')]:
        answer=LeanChecker().check_partial(dict(request,**{key:value}),tamper_context)
        require(answer['accepted'] is False and answer['status']=='integrity_error','binding tamper was accepted')
        tamper.append({'field':key,'result':answer})
    save(store.path('binding-negative.json'),tamper)
    mismatch,command_mismatch=cli(['run','--identity',args.mismatch_identity,'--method',args.method,
        '--seconds',str(args.seconds),'--output-root',str(output/'mismatch')],output,'cli_mismatch',args.seconds)
    mismatch_state=ResidualState.from_dict(mismatch.load_checkpoint()['state'])
    require(mismatch_state.round_index==0 and not mismatch_state.C and mismatch_state.O==(mismatch_state.root,),
            'source mismatch executed or altered formal state')
    require(mismatch.read_json('run.json')['stop_reason']=='not_applicable','wrong mismatch category')
    seen={}
    for record in records:
        for artifact in record.get('artifacts',[]):
            path=guard_path(artifact['path'],store.root)
            require(sha256_file(path)==artifact['sha256'],'artifact hash mismatch')
            seen[str(path)]=artifact['sha256']
    summary={'passed':True,'method':spec.id,'method_version':spec.version,'capability_level':spec.capability_level,
        'scope':'one_real_Train_local_certificate_only','identity':initial.G.identity,'theorem':initial.G.theorem,
        'source_sha256':initial.G.sha256,'run_dir':str(store.root),'mismatch_run_dir':str(mismatch.root),
        'profile':spec.lean_profile,'local_proposition':candidate.proposition,'certificate_id':candidate.id,
        'C_before':0,'C_after':1,'O_before':['original'],'O_after':['original'],'links_before':0,'links_after':0,
        'original_identity_proved':False,'actual_core_constructed':True,'independent_symbolic_check':translation['independent_symbolic_check'],
        'real_partial_lean_checks':1,'fresh_replay_checks':1,'real_negative_lean_checks':1,
        'resume_repeated_actions':0,'artifact_hashes_checked':len(seen),'axioms':replay.C[0].evidence['audit']['axioms'],
        'commands':[run_command,resume_command,command_mismatch],'model_calls':0,'test_data_read':False}
    save(output/'summary.json',summary)
    print(json.dumps({'passed':True,'method':spec.id,'summary':str(output/'summary.json')},ensure_ascii=False))


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--method',required=True)
    parser.add_argument('--identity',required=True)
    parser.add_argument('--mismatch-identity',default='FQI-GAUSS-ALTERNATING')
    parser.add_argument('--output-root',required=True)
    parser.add_argument('--seconds',type=positive_float,default=1200)
    args=parser.parse_args(argv);output=Path(args.output_root).absolute()
    output=guard_path(output,output.anchor);output.mkdir(parents=True,exist_ok=True)
    require(not any(output.iterdir()),'evidence directory must be empty')
    acceptance(args,output)


if __name__=='__main__':main()
