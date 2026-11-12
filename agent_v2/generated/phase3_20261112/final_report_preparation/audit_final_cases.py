"""Audit completed final-runtime cases without opening the active recurrence run."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];BASE=ROOT/'agent_v2/generated/phase3_20261112';FINAL=BASE/'final_validation_01'
OUT=FINAL/'report_metadata';read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
manifest=read(FINAL/'frozen/manifest.json');frozen=manifest['files'];inputs=read(OUT/'input_dependency_manifest.json')['files'];artifacts={}
for relative,item in frozen.items():
 p=Path(item['snapshot_path']);assert sha(p)==item['sha256'] and p.stat().st_size==item['bytes']
def walk(obj):
 if isinstance(obj,dict):
  if isinstance(obj.get('artifacts'),list):
   for a in obj['artifacts']:
    p=Path(a['path']);assert sha(p)==a['sha256'];artifacts[str(p)]=a['sha256']
  for value in obj.values():walk(value)
 elif isinstance(obj,list):
  for value in obj:walk(value)
def source_and_checkpoint(run):
 checkpoint=read(run/'checkpoint.json');manifest=read(run/'checkpoint_manifest.json')
 assert sha(run/manifest['path'])==manifest['sha256']
 assert (run/'checkpoint.json').read_bytes()==(run/manifest['path']).read_bytes()
 state=checkpoint['state'];initial=read(run/'initial_state.json');source=state['G']
 assert initial['G']==source and state['Gamma']==source['Gamma']==source['declaration']
 assert sha(Path(source['snapshot_path']))==source['sha256']
 for dep in source['dependencies']:
  relative=str(Path(dep['path']).relative_to(ROOT));item=(frozen|inputs)[relative];assert item['sha256']==dep['sha256'];assert sha(Path(item['snapshot_path']))==dep['sha256']
 return initial,state
suite=read(FINAL/'full_suite/summary.json');assert suite['passed'] is True
assert suite['tests_run']==suite['discovered_tests']==475
for key in ('failures','errors','skipped','expected_failures','unexpected_successes'):assert suite[key]==[]
assert len(read(FINAL/'full_suite/discovered_tests.json'))==475
matrix=read(FINAL/'method_matrix/summary.json');assert matrix['verification_passed'] is True and matrix['third_stage_fully_complete'] is False
rows=[];local=[];symbolic=[]
for item in matrix['methods']:
 summary_path=Path(item['summary']);summary=read(summary_path);method=summary['method'];assert summary['passed'] is True
 assert summary['original_identity_proved'] is False and summary['resume_repeated_actions']==0
 run=Path(summary['run_dir']);initial,state=source_and_checkpoint(run)
 for key in ('O','links','r','Gamma'):assert state[key]==initial[key]
 assert [o['id'] for o in state['O']]==['original'] and state['links']==[] and state['round_index']==1
 result=read(run/'rounds/1/result.json');walk(result);walk(read(run/'rounds/1/backend/cas_return.json'))
 checkpaths=[run/'rounds/1/verification.json',*run.glob('resume_checks/*/result.json')]
 count_before=len(artifacts)
 if summary['capability_level']=='L3':
  assert len(state['C'])==1 and summary['real_partial_lean_checks']==summary['fresh_replay_checks']==summary['real_negative_lean_checks']==1
  cert=state['C'][0];receipt=cert['evidence'];walk(receipt)
  assert set(receipt['audit']['axioms'])<={'propext','Classical.choice','Quot.sound'}
  assert receipt['returncode']==0 and receipt['source_sha256']==state['G']['sha256']
  assert cert['id']==summary['certificate_id'] and cert['proposition']==summary['local_proposition']
  negative=run/'negative-proof/verification.json';checkpaths.append(negative)
  check=read(negative)['checks'][0]['check'];assert check['accepted'] is False and check['evidence']['returncode']!=0
  assert read(run/'negative-proof/state_before.json')==read(run/'negative-proof/state_after.json')
  assert len(list(run.glob('resume_checks/*/result.json')))==1
  local.append(method)
 else:
  assert summary['capability_level']=='L2' and state['C']==[] and result['C_partial']==result['O_res']==[]
  assert summary['lean_calls']==summary['resume_lean_calls']==0
  assert not list(run.rglob('Candidate.lean')) and not list(run.glob('resume_checks/*/result.json'))
  assert result['raw_result']['execution_scope']=='source_symbolic_only'
  assert read(run/'run.json')['stop_reason']=='symbolic_translation_pending'
  symbolic.append(method)
 for p in checkpaths:walk(read(p))
 rows.append({'method':method,'summary':str(summary_path),'summary_sha256':sha(summary_path),
  'run_dir':str(run),'identity':state['G']['identity'],'source_sha256':state['G']['sha256'],
  'source_dependencies':len(state['G']['dependencies']),'C':len(state['C']),'O':['original'],'links':0,
  'capability_level':summary['capability_level'],'original_identity_proved':False,
  'certificate_id':summary.get('certificate_id'),'proposition':summary.get('local_proposition'),
  'remaining_budget':state['b'],'source_snapshot_path':state['G']['snapshot_path'],
  'formal_check_and_negative_artifact_paths_added':len(artifacts)-count_before})
assert len(local)==6 and len(symbolic)==3
spectral=matrix['spectral'];assert spectral['verification_passed'] is True and spectral['requested_Source_L3_upgrade_passed'] is False
assert spectral['initial_stop_reason']=='not_applicable' and spectral['resume_stop_reason']=='graph_capability_missing'
_,state=source_and_checkpoint(Path(spectral['run_dir']));assert state['C']==state['links']==[] and state['round_index']==0
assert spectral['lean_calls']==spectral['CAS_calls']==0
tel=read(FINAL/'telescoping/summary.json');assert tel['passed'] is True and tel['original_identity_proved'] is True
run=Path(tel['run_dir']);_,state=source_and_checkpoint(run)
assert len(state['C'])==4 and state['O']==[] and len(state['links'])==3
assert tel['real_partial_lean_checks']==tel['fresh_replay_checks']==4 and tel['real_original_lean_checks']==2
original=[]
for path in sorted(run.glob('final/*/checked.json')):
 checked=read(path);assert checked['accepted'] is True and checked['status']=='original_theorem_proved'
 receipt=checked['evidence'];assert receipt['theorem']=='FiniteQBenchmark.Identity272.statement'
 assert receipt['source_sha256']==tel['source_sha256'] and receipt['returncode']==0
 assert set(receipt['audit']['axioms'])<={'propext','Classical.choice','Quot.sound'};walk(checked)
 original.append({'path':str(path),'sha256':sha(path),'theorem':receipt['theorem'],'axioms':receipt['audit']['axioms'],
  'universe_parameters':receipt['audit']['universe_parameters'],'source_sha256':receipt['source_sha256']})
assert len(original)==2
for path in [*run.glob('rounds/*/verification.json'),*run.glob('resume_checks/*/result.json'),run/'negative-bridge/verification.json']:walk(read(path))
before=read(run/'negative-bridge/state_before.json');after=read(run/'negative-bridge/state_after.json')
for key in ('O','links','r','G','Gamma'):assert before[key]==after[key]
assert tel['negative_bridge']['real_lean_rejection'] is True and tel['negative_bridge']['independent_local_certificate_preserved'] is True
init=read(FINAL/'init_independent_audit.json');assert init['original_identity_proved'] is True
init_run=Path(init['run_dir']);init_state=read(init_run/'checkpoint.json')['state']
assert init_state['O']==[] and len(init_state['C'])==2 and len(init_state['links'])==2
init_checked=read(Path(init['original_audits'][0]['result_path']));assert init_checked['accepted'] is True
assert init_checked['evidence']['axioms']==[];walk(init_checked)
for path in init_run.glob('rounds/*/verification.json'):walk(read(path))
rec=read(FINAL/'recurrence/summary.json');assert rec['passed'] is True and rec['original_identity_proved'] is True
rec_run=Path(rec['run_dir']);_,rec_state=source_and_checkpoint(rec_run)
assert len(rec_state['C'])==5 and rec_state['O']==[] and len(rec_state['links'])==4
assert rec['real_partial_lean_checks']==5 and rec['fresh_replay_checks']==17 and rec['real_original_lean_checks']==2
assert rec['resume_repeated_actions']==0 and len(rec['negative_proofs'])==5
rec_original=[]
for p in sorted(rec_run.glob('final/*/checked.json')):
 checked=read(p);receipt=checked['evidence'];assert checked['accepted'] is True
 assert checked['status']=='original_theorem_proved' and receipt['theorem']=='FiniteQBenchmark.Identity009.statement'
 assert receipt['source_sha256']==rec['source_sha256'] and receipt['returncode']==0
 assert set(receipt['audit']['axioms'])<={'propext','Classical.choice','Quot.sound'};walk(checked)
 rec_original.append({'path':str(p),'sha256':sha(p),'theorem':receipt['theorem'],'axioms':receipt['audit']['axioms'],
  'universe_parameters':receipt['audit']['universe_parameters'],'source_sha256':receipt['source_sha256']})
assert len(rec_original)==2
for p in [*rec_run.glob('rounds/*/verification.json'),*rec_run.glob('resume_checks/*/result.json')]:walk(read(p))
for negative in rec['negative_proofs']:
 d=Path(negative['evidence_directory']);assert read(d/'state_before.json')==read(d/'state_after.json')
 assert negative['checkpoint_unchanged'] is True and negative['real_lean_rejection'] is True
 v=read(d/'verification.json');check=v['checks'][0]['check']
 assert check['accepted'] is False and check['sigma']['code']=='lean_check_failed' and check['evidence']['returncode']!=0
 walk(v)
for relative,item in frozen.items():assert sha(ROOT/relative)==item['sha256']
for relative,digest in manifest['baseline_tests_unchanged'].items():assert sha(ROOT/relative)==digest
assert len(manifest['baseline_tests_unchanged'])==30

report={'passed':True,'scope':'final-runtime full suite, all eleven Source method routes, stopped spectral refusal and Init evidence; no additional Lean run performed by audit',
 'full_suite':{'tests_run':475,'passed':475,'failures':0,'errors':0,'skips':0,'seconds':suite['wall_seconds']},
 'frozen_files_checked':len(frozen),'additional_input_manifest_files':len(inputs),'methods':rows,'local_L3_count':6,'Source_L2_count':3,
 'spectral_requested_upgrade_passed':False,'telescoping_original_audits':original,
 'Init_original_axioms':[],'unique_artifact_hashes_checked':len(artifacts),'artifacts':artifacts,
 'recurrence_final_validation_complete':True,'recurrence_original_audits':rec_original,'old_test_files_unchanged':30,'third_stage_fully_complete':False,
 'runtime_edited':False,'old_tests_edited':False,'model_calls':0,'benchmark_Test_read':False}
(OUT/'final_cases_audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ('passed','frozen_files_checked','local_L3_count','Source_L2_count','unique_artifact_hashes_checked','recurrence_final_validation_complete')}))
