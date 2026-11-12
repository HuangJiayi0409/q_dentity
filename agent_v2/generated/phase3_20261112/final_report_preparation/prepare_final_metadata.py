"""Inventory the final frozen code and prepare twelve method-card slots.

This never reads live test logs as a success signal. A method's frozen earlier
card and its fresh final-runtime result remain distinct evidence records.
"""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];BASE=ROOT/'agent_v2/generated/phase3_20261112';HERE=Path(__file__).resolve().parent
FINAL=BASE/'final_validation_01';OUT=FINAL/'report_metadata';OUT.mkdir(exist_ok=True)
read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,value):(OUT/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
manifest_path=FINAL/'frozen/manifest.json';manifest=read(manifest_path);baseline=read(BASE/'baseline_hashes.json')
roles={
 'loop.py':'single-action loop, terminal classification and Source-only symbolic stop boundary',
 'proof_profiles.py':'unique Source profile selection, candidate/receipt/dependency reconstruction and universe contract',
 'math_lean_profile.py':'fixed mathematical Lean compilation and live receipt audit',
 'recurrence_closure.py':'RHS recurrence, two initial values and uniqueness/original assembly candidates',
 'method_tasks.py':'five declared recurrence tasks, validated dependency binding and open-obligation routing',
 'method_registry.py':'public method contract, version, capability and executable entry points',
 'MonomorphicCheck.lean':'fixed empty-universe original/candidate type and axiom audit',
 'index_construct.py':'pure bounded mixed-radix product index construction',
 'operator_construct.py':'pure ordered polynomial operator action construction',
 'choice_construct.py':'pure arbitrary-bound ranked subset/Boolean choice construction',
}
inventory=[]
for relative,item in manifest['files'].items():
 frozen=Path(item['snapshot_path']);assert sha(frozen)==item['sha256'] and frozen.stat().st_size==item['bytes']
 p=Path(relative);prior=baseline.get(relative)
 if p.is_relative_to('agent_v2/generated'):status='generated_validation_driver_not_production'
 elif prior is not None:status='unchanged_from_recorded_baseline' if prior==item['sha256'] else 'modified_from_recorded_baseline'
 elif p.is_relative_to('agent_v2'):status='new_agent_file_since_recorded_baseline'
 else:status='mathematical_or_configuration_dependency_not_in_agent_baseline'
 if p.is_relative_to('agent_v2/generated'):role='generated invocation/freeze driver; not production Agent logic'
 elif p.name in roles:role=roles[p.name]
 elif p.is_relative_to('agent_v2/tests'):role='test or smoke helper; inspect actual execution records separately'
 elif p.name.endswith('_frontend.py'):role='fully consumed typed Source grammar and mathematical object export'
 elif p.name.endswith('_adapter.py'):role='bounded subprocess adapter, Source/request/artifact binding and strict result'
 elif p.name.endswith('_worker.py'):role='fixed pure mathematical core process entry and source inventory'
 elif p.name.endswith('_check.py'):role='independent mathematical certificate checking'
 elif p.name.endswith('_translation.py'):role='Source-bound mathematical witness to controlled local Lean candidate'
 elif p.suffix=='.lean':role='retained foundation or fixed Lean rule/driver source; import role is receipt-specific'
 else:role='runtime, mathematical implementation or build dependency; preserved exact bytes'
 inventory.append({'path':relative,'sha256':item['sha256'],'bytes':item['bytes'],'snapshot_path':str(frozen),
  'baseline_sha256':prior,'change_classification':status,'responsibility':role})
assert len(inventory)==262
save('frozen_file_inventory.json',{'scope':'final frozen code/test/math dependency inventory; no final test result inferred',
 'manifest':str(manifest_path),'manifest_sha256':sha(manifest_path),'files':inventory,
 'agent_baseline_scope':'67 originally recorded agent files; external mathematical files without baseline hash are not automatically new',
 'final_regression_complete':False})
methods=manifest['registry']['methods'];assert len(methods)==12
cards=[]
for spec in methods:
 method=spec['id'];ab=method in ('telescoping','recurrence')
 if ab:
  final_summary=FINAL/method/'summary.json';stage_card=None;final_card=OUT/(method+'_acceptance_card.json')
 elif method=='spectral':
  stage_card=BASE/'spectral/acceptance_card.json';final_summary=FINAL/'method_matrix/spectral_boundary.json';final_card=stage_card
 else:
  stage_card=BASE/('coefficient_review' if method=='coefficient' else method)/'acceptance_card.json'
  final_summary=FINAL/'method_matrix'/method/'summary.json';final_card=stage_card
 if stage_card is not None:assert stage_card.is_file()
 cards.append({'method':method,'version':spec['version'],'capability_level':spec['capability_level'],
  'local_lean':spec['local_lean'],'full_original':spec['full_original'],
  'source_frontend':spec['frontend'],'adapter':spec['adapter'],'lean_profile':spec['lean_profile'],
  'source_route_accepted':method!='spectral','stage_acceptance_card':str(stage_card) if stage_card else None,
  'stage_card_sha256':sha(stage_card) if stage_card else None,'final_card':str(final_card),
  'final_summary_expected':str(final_summary),'final_result_status':'pending',
  'spectral_requested_upgrade_passed':False if method=='spectral' else None,
  'limitations':spec['limitations']})
assert sum(c['capability_level']=='L3' for c in cards)==8
assert sum(c['capability_level']=='L2' for c in cards)==4
save('method_cards_index_prepared.json',{'scope':'twelve-card structure before all final-runtime summaries complete',
 'cards':cards,'stage_Source_routes':11,'L3':8,'L2':4,'final_regression_complete':False,
 'third_stage_fully_complete':False,'remaining_stage_gap':'spectral Source export and local Lean bridge'})
expected=[{'id':'final_frozen_source','run_dir':str(FINAL/'frozen')},
 {'id':'final_full_suite','run_dir':str(FINAL/'full_suite')},
 {'id':'final_recurrence_full','run_dir':str(FINAL/'recurrence')},
 {'id':'final_telescoping_full','run_dir':str(FINAL/'telescoping')},
 {'id':'final_Init_smoke','run_dir':str(FINAL/'init_runs')}]
expected += [{'id':'final_'+m,'run_dir':str(FINAL/'method_matrix'/m)} for m in
 ('coefficient','interpolation','determinant','kernel_transform','difference_ring','macmahon','product','noncommutative','combinatorial')]
save('evidence_export_plan.json',{'scope':'planned explicit evidence directories; not yet exported while writers run',
 'cases':expected,'export_after_all_writers_stop':True,'earlier_22_packages_immutable':True,
 'additional_selected_metadata':'final CLI commands, stopped spectral Source run, full-suite final summary, Init driver logs, 12 cards and final audit are selected after completion',
 'receipt_paths_rewritten':False,'external_toolchain_cache_bundled':False,'proof_verification_by_exporter':False})
print(json.dumps({'frozen_files_checked':len(inventory),'method_card_slots':len(cards),'L3':8,'L2':4,'Source_routes':11,'final_regression_complete':False}))
