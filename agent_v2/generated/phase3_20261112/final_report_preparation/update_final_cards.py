"""Write final-runtime metadata cards from completed summaries; never rewrite receipts."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];BASE=ROOT/'agent_v2/generated/phase3_20261112';FINAL=BASE/'final_validation_01';OUT=FINAL/'report_metadata'
read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def save(path,value):path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
prepared=read(OUT/'method_cards_index_prepared.json');entries=[]
for entry in prepared['cards']:
 method=entry['method'];summary_path=Path(entry['final_summary_expected']);item=dict(entry)
 card_path=OUT/(method+'_acceptance_card.json');item['final_card']=str(card_path)
 if not summary_path.is_file():
  item['final_result_status']='pending';entries.append(item);continue
 summary=read(summary_path);spectral=method=='spectral';complete=method in ('telescoping','recurrence')
 assert summary.get('verification_passed' if spectral else 'passed') is True
 if spectral:
  assert summary['requested_Source_L3_upgrade_passed'] is False
  run=Path(summary['run_dir']);state=read(run/'checkpoint.json')['state']
  card={'schema_version':1,'method':method,'method_version':entry['version'],'capability_level':'L2',
   'status':'branch_stopped','requested_Source_upgrade_passed':False,'evidence_validation_passed':True,
   'identity':summary['identity'],'source_sha256':summary['source_sha256'],'theorem':state['G']['theorem'],
   'actual_Source_execution':'not_applicable then graph_capability_missing on resume',
   'CAS_calls':0,'lean_calls':0,'local_lean':False,'full_original':False,'original_identity_proved':False,
   'C':0,'O':['original'],'links':0,'scope':'current-runtime Source refusal; old explicit-core L2 retained',
   'remaining_work':'Symbolic size, original phi eigenrelations and denominators, diagonal norm and valid Lean foundation import.'}
 else:
  run=Path(summary['run_dir']);state=read(run/'checkpoint.json')['state'];source=state['G']
  assert len(state['C'])==(len(summary.get('C_final',[])) if complete else summary['C_after'])
  card={'schema_version':1,'method':method,'method_version':entry['version'],'capability_level':entry['capability_level'],
   'status':'original_theorem_proved' if complete else ('local_Lean_verified_original_open' if entry['capability_level']=='L3' else 'Source_symbolic_constructed_translation_pending'),
   'identity':source['identity'],'theorem':source['theorem'],'source_sha256':source['sha256'],
   'source_context_unchanged':True,'full_original':entry['full_original'],'local_lean':entry['local_lean'],
   'C':len(state['C']),'O':[o['id'] for o in state['O']],'links':len(state['links']),
   'original_identity_proved':bool(summary['original_identity_proved']),
   'scope':'final frozen runtime, new execution; detailed mathematical contract also retained in stage card',
   'certificates':[{'id':c['id'],'proposition':c['proposition'],'dependencies':c['dependencies'],'profile':c['evidence'].get('profile'),
    'axioms':c['evidence'].get('axioms',c['evidence'].get('audit',{}).get('axioms'))} for c in state['C']],
   'remaining_budget':state['b'],'resume_repeated_actions':summary['resume_repeated_actions']}
  if complete:
   original=[]
   for path in sorted(run.glob('final/*/checked.json')):
    check=read(path);assert check['accepted'] is True;receipt=check['evidence']
    assert receipt['theorem']==source['theorem'] and receipt['source_sha256']==source['sha256']
    original.append({'result':str(path),'sha256':sha(path),'theorem':receipt['theorem'],
     'proposition':receipt['proposition'],'axioms':receipt['audit']['axioms'],'returncode':receipt['returncode']})
   assert len(original)==2 and state['O']==[]
   card.update(original_checks=original,real_partial_lean_checks=summary['real_partial_lean_checks'],
    fresh_replay_checks=summary['fresh_replay_checks'],real_original_lean_checks=summary['real_original_lean_checks'],
    negative_evidence=summary.get('negative_proofs',summary.get('negative_bridge')))
  elif entry['capability_level']=='L3':
   assert len(state['C'])==1 and [o['id'] for o in state['O']]==['original'] and not state['links']
   card.update(real_partial_lean_checks=summary['real_partial_lean_checks'],fresh_replay_checks=summary['fresh_replay_checks'],
    real_negative_lean_checks=summary['real_negative_lean_checks'],actual_core_constructed=summary['actual_core_constructed'],
    independent_symbolic_check=summary['independent_symbolic_check'])
  else:
   assert not state['C'] and not state['links'] and summary['lean_calls']==0
   card.update(lean_calls=0,formal_candidate_count=0,formal_obligations_exported=0,proof_profile_registered=False,
    stop_reason=summary['stop_reason'],independent_symbolic_check=summary['independent_symbolic_check'],
    old_generic_standalone_capability='L0',original_identity_proved=False)
 card.update(run_dir=str(run),final_summary=str(summary_path),final_summary_sha256=sha(summary_path),
  commands=summary.get('commands',[]),final_frozen_manifest=str(FINAL/'frozen/manifest.json'),
  final_frozen_manifest_sha256=sha(FINAL/'frozen/manifest.json'),stage_acceptance_card=entry['stage_acceptance_card'],
  stage_card_sha256=entry['stage_card_sha256'],source_frontend=entry['source_frontend'],adapter=entry['adapter'],
  lean_profile=entry['lean_profile'],limitations=entry['limitations'],benchmark_Test_read=False,model_calls=0)
 save(card_path,card)
 item.update(final_result_status=card['status'],final_card_sha256=sha(card_path),final_summary_sha256=sha(summary_path))
 entries.append(item)
save(OUT/'method_cards_index.json',{'scope':'final-runtime cards from actual completed cases; overall final gate awaits all audits',
 'cards':entries,'cards_available':sum(e['final_result_status']!='pending' for e in entries),
 'L3':8,'L2':4,'Source_routes':11,'spectral_requested_upgrade_passed':False,
 'third_stage_fully_complete':False,'final_overall_gate_status':'pending'})
print(json.dumps({'cards_available':sum(e['final_result_status']!='pending' for e in entries),'pending':[e['method'] for e in entries if e['final_result_status']=='pending']}))
