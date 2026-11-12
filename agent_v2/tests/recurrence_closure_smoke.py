"""Explicit five-action Train recurrence closure, paused replay and Lean negatives.

Run only after production sources are frozen. This is not unittest discovery.
Every proof check uses the production LeanChecker; no API, held-out benchmark,
synthetic theorem, saved historical proof or receipt-shaped fixture is used.
"""
import argparse
from dataclasses import replace
import json
from pathlib import Path
import subprocess
import sys
import time

from agent_v2.cli import positive_float
from agent_v2.executor import assemble_term, normalize_result, validate_invariant, verify_and_update
from agent_v2.lean_checker import LeanChecker
from agent_v2.models import Cost, JointAction, ResidualState
from agent_v2.recurrence_closure import TASKS, closure_blueprint, make_closure_candidate
from agent_v2.recurrence_frontend import PROFILE, analyze_source
from agent_v2.recurrence_translation import reconstruct_candidate
from agent_v2.storage import RunStore, guard_path, sha256_file, verify_source


ROOT = Path(__file__).resolve().parents[2]
IDENTITY = 'FQI-GAUSS-ALTERNATING'
THEOREM = 'FiniteQBenchmark.Identity009.statement'
SOURCE_SHA256 = 'c49f5a4417e3d4d19df4463a377c4d3117cea07619d1867156eccb454ca8123c'
ALLOWED_AXIOMS = {'propext', 'Classical.choice', 'Quot.sound'}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def execute(command, output, label, timeout, *, proved=False):
    began = time.monotonic()
    record = {'command': command}
    try:
        process = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=timeout)
        record.update(returncode=process.returncode, stdout=process.stdout, stderr=process.stderr)
    except subprocess.TimeoutExpired as error:
        record.update(returncode=None, timed_out=True,
                      stdout=str(error.stdout or ''), stderr=str(error.stderr or ''))
        raise
    finally:
        record['seconds'] = time.monotonic() - began
        save(output / (label + '.json'), record)
    expected_status = 'original_theorem_proved' if proved else 'incomplete'
    require(process.returncode == (0 if proved else 2), f'{label}: unexpected CLI exit; inspect saved command log')
    require(bool(process.stdout.splitlines()), f'{label}: CLI did not return a summary')
    summary = json.loads(process.stdout.splitlines()[-1])
    require(summary.get('status') == expected_status and summary.get('original_identity_proved') is proved,
            f'{label}: CLI proof boundary differs from the expected stage')
    return summary, record


def check_receipt(evidence, source, *, original=False):
    require(evidence.get('returncode') == 0, 'real Lean compilation did not succeed')
    require(evidence.get('source_sha256') == source.sha256 and evidence.get('profile') == PROFILE,
            'Lean receipt has a different Source or profile')
    require(evidence.get('profile_version') == '1', 'Lean receipt has an unexpected profile version')
    axioms = evidence.get('axioms')
    require(isinstance(axioms, (list, tuple)) and set(axioms) <= ALLOWED_AXIOMS,
            'Lean receipt lacks an allowed axiom audit')
    audit = evidence.get('audit', {})
    require(audit.get('theorem') == (source.theorem if original else 'AgentV2Candidate.proof'),
            'the actual audited theorem differs from the requested theorem')
    if original:
        require(audit.get('universe_parameter_count') == 1, 'original Field universe was specialized')
    else:
        require(list(audit.get('universe_parameters', ())) == ['u'], 'local Field universe was specialized')
    paths = [Path(a['path']) for a in evidence.get('artifacts', ())]
    require(any(p.name == 'Candidate.lean' for p in paths)
            and any(p.name == 'Candidate.olean' for p in paths)
            and any(p.name == 'stdout.jsonl' for p in paths)
            and any(p.name == 'process.json' for p in paths),
            'actual Lean source, compiled artifact or diagnostic logs are missing')


def artifact_hashes(store, records):
    seen = {}
    for record in records:
        for artifact in record.get('artifacts', ()):
            path = guard_path(artifact['path'], store.root)
            expected = artifact['sha256']
            require(path not in seen or seen[path] == expected, 'one artifact has conflicting retained hashes')
            seen[path] = expected
    for path, expected in seen.items():
        require(sha256_file(path) == expected, 'artifact hash mismatch: ' + str(path))
    return len(seen)


def checkpoint_snapshot(store, output, label, initial, *, rounds, count, leaves, links, proved=False):
    checkpoint = store.load_checkpoint()
    state = ResidualState.from_dict(checkpoint['state'])
    validate_invariant(state)
    verify_source(state.G, store.root)
    require(state.G == initial.G and state.Gamma == initial.Gamma and state.root == initial.root,
            label + ': frozen theorem or context changed')
    require(state.G.identity == IDENTITY and state.G.theorem == THEOREM and state.G.sha256 == SOURCE_SHA256,
            label + ': fixed Train source drifted')
    require(state.round_index == rounds and len(state.C) == count and len(state.O) == leaves
            and len(state.links) == links, label + ': residual counts do not match the completed actions')
    require(state.b.actions == initial.b.actions - rounds, label + ': actions were repeated or charged twice')
    require(state.status == ('original_theorem_proved' if proved else 'incomplete'),
            label + ': checkpoint claimed the wrong proof status')
    run = store.read_json('run.json')
    require(run['original_identity_proved'] is proved, label + ': saved run crossed the proof boundary')
    if not proved:
        require(run['stop_reason'] == 'checkpoint_paused', label + ': CLI did not pause at the requested boundary')
    for cert in state.C:
        check_receipt(cert.evidence, state.G)
    folder = output / 'stages' / label
    save(folder / 'checkpoint.json', checkpoint)
    save(folder / 'run.json', run)
    paths = {'resume_checks': sorted(str(p) for p in store.path('resume_checks').glob('*/result.json')),
             'final_checks': sorted(str(p) for p in store.path('final').glob('*/checked.json')),
             'rounds': sorted(p.name for p in store.path('rounds').iterdir() if p.is_dir())}
    save(folder / 'retained_paths.json', paths)
    require(len(paths['rounds']) == rounds, label + ': extra or missing action directories')
    return state, paths


def audit_resume(store, previous, current, old_paths, new_paths, *, action_delta, final_delta):
    require(current.round_index == previous.round_index + action_delta
            and current.b.actions == previous.b.actions - action_delta,
            'resume repeated an action or charged replay as a new action')
    require(current.b.seconds < previous.b.seconds, 'resume did not charge actual replay/verification wall time')
    require(len(current.C) == len(previous.C) + action_delta, 'resume omitted or duplicated a formal certificate')
    for old, fresh in zip(previous.C, current.C):
        require(replace(old, evidence=fresh.evidence) == fresh, 'resume changed a retained mathematical certificate')
        require(old.evidence['artifacts'] != fresh.evidence['artifacts'], 'resume trusted an old Lean receipt')
    replay_paths = set(new_paths['resume_checks']) - set(old_paths['resume_checks'])
    require(len(replay_paths) == len(previous.C), 'resume did not recheck precisely its saved certificates')
    records = []
    for path in sorted(replay_paths):
        checked = json.loads(Path(path).read_text())
        require(checked.get('accepted') is True and checked.get('status') == 'partial_lean_verified',
                'a fresh checkpoint certificate check failed')
        check_receipt(checked['evidence'], current.G)
        records.append(checked['evidence'])
    finals = set(new_paths['final_checks']) - set(old_paths['final_checks'])
    require(len(finals) == final_delta, 'resume skipped or duplicated original-theorem acceptance')
    for path in sorted(finals):
        checked = json.loads(Path(path).read_text())
        require(checked.get('accepted') is True and checked.get('status') == 'original_theorem_proved',
                'the frozen original theorem failed final acceptance')
        check_receipt(checked['evidence'], current.G, original=True)
        request = json.loads((Path(path).parent / 'request.json').read_text())
        require(request['proof_term'] == assemble_term(current), 'final proof differs from the complete proof tree')
        records.append(checked['evidence'])
    require(set(old_paths['resume_checks']) <= set(new_paths['resume_checks'])
            and set(old_paths['final_checks']) <= set(new_paths['final_checks']),
            'resume overwrote or removed prior verification evidence')
    return records, len(replay_paths)


def audit_rounds(store, initial):
    front = analyze_source(initial.G.to_dict(), store.root)
    require(front['status'] == 'applicable', 'frozen original is outside the supported recurrence source')
    steps, records, prior = [], [], initial
    for number in range(1, 6):
        prefix = f'rounds/{number}'
        before = ResidualState.from_dict(store.read_json(prefix + '/state_before.json'))
        after = ResidualState.from_dict(store.read_json(prefix + '/state_after.json'))
        action = JointAction.from_dict(store.read_json(prefix + '/action.json'))
        result = normalize_result(store.read_json(prefix + '/result.json'))
        validate_invariant(before); validate_invariant(after)
        verify_source(after.G, store.root)
        require(before.G == after.G == initial.G and before.Gamma == after.Gamma == initial.Gamma,
                'an action changed the frozen original context')
        require(before.O == prior.O and before.links == prior.links and before.attempts == prior.attempts
                and len(before.C) == len(prior.C), 'resume changed the mathematical state before an action')
        require(all(replace(old, evidence=fresh.evidence) == fresh for old, fresh in zip(prior.C, before.C)),
                'resume substituted a different certificate')
        require(before.b.actions == prior.b.actions and before.b.seconds <= prior.b.seconds,
                'replay increased budget or charged another action')
        require(action.T == 'identity' and action.source == action.target == before.r == after.r,
                'identity action changed representation')
        require(action.theta['method'] == 'recurrence' and action.theta['scope'] == 'full', 'wrong action scope')
        require(result.status == 'symbolic_constructed' and result.original_identity_proved is False,
                'one partial action claimed final proof success')
        require(len(result.C_partial) == 1 and len(after.C) == len(before.C) + 1
                and after.C[:-1] == before.C, 'one action did not verify exactly one candidate')
        candidate = result.C_partial[0]
        require(after.C[-1].id == candidate.id, 'C differs from the selected candidate')
        require(after.b.actions == before.b.actions - 1 and result.cost.actions == 1
                and 0 < result.cost.wall_seconds <= before.b.seconds and after.b.seconds < before.b.seconds,
                'one action lacks its actual budget charge')
        legal = store.read_json(prefix + '/candidates.json')['legal']
        selected = store.read_json(prefix + '/selection.json')
        require(action.to_dict() in legal and selected.get('selected') == action.id and selected.get('reason'),
                'saved selection is not a bound legal action')
        verification = store.read_json(prefix + '/verification.json')
        require(verification.get('certificates_added') == 1 and verification.get('original_identity_proved') is False,
                'partial verification was confused with original acceptance')
        task = action.theta['task']
        if number == 1:
            require(task == 'local' and after.O == initial.O and not after.links and not result.O_res,
                    'local recurrence prematurely changed the original obligation')
            rebuilt = reconstruct_candidate(front, candidate.proof_term)
            require(rebuilt == candidate, 'local recurrence differs from its source-bound witness reconstruction')
            core = result.raw_result['core']
            require(core.get('status') == 'constructed' and core.get('solver') == 'q_zeilberger'
                    and core['result']['order'] == 2, 'actual q-Zeilberger core did not construct the recurrence')
        else:
            approved = {cert.id: cert.to_dict() for cert in before.C}
            expected = make_closure_candidate(front, task, approved, action.id)
            require(expected == candidate, 'closure candidate differs from its canonical source/dependency template')
            if number == 2:
                require(task == 'uniqueness_bridge' and candidate.dependencies == (before.C[0].id,),
                        'uniqueness bridge lacks the actual local recurrence dependency')
                require(after.O == candidate.replaces == result.O_res and len(after.O) == 3
                        and len(after.links) == 1 and candidate.closes == 'original',
                        'verified bridge did not introduce exactly three formal children')
                require(all(o.origin_action == action.id and o.proposition and o.lean_anchor
                            and o.source_sha256 == initial.G.sha256 for o in after.O),
                        'bridge children lack source/proposition/origin anchors')
            else:
                require(task in TASKS[1:] and not candidate.dependencies and not candidate.replaces,
                        'a leaf candidate has the wrong role or hidden dependencies')
                require({o.id for o in after.O} == {o.id for o in before.O} - {candidate.closes}
                        and len(after.O) == len(before.O)-1 and len(after.links) == len(before.links)+1,
                        'one leaf action changed another obligation')
        check_receipt(after.C[-1].evidence, initial.G)
        steps.append({'round':number,'task':task,'action_id':action.id,'candidate_id':candidate.id,
            'proposition':candidate.proposition,'dependencies':list(candidate.dependencies),
            'C_before':[c.id for c in before.C],'C_after':[c.id for c in after.C],
            'O_before':[o.to_dict() for o in before.O],'O_after':[o.to_dict() for o in after.O],
            'links_before':len(before.links),'links_after':len(after.links), 'r':after.r,
            'budget_before':before.b.to_dict(),'budget_after':after.b.to_dict(),'cost':result.cost.to_dict()})
        records.extend([result.to_dict(),after.C[-1].to_dict()['evidence']])
        prior = after
    require({step['task'] for step in steps[2:]} == set(TASKS[1:]), 'an initial value or RHS task was skipped/repeated')
    require(sum(step['task']=='local' for step in steps) == 1, 'CAS local construction was repeated')
    return steps, records


def negative_round(store, number, task, seconds):
    """Keep canonical IDs/types/dependencies; only the proof body is wrong."""
    prefix = f'rounds/{number}'
    before = ResidualState.from_dict(store.read_json(prefix + '/state_before.json'))
    action = JointAction.from_dict(store.read_json(prefix + '/action.json'))
    positive = normalize_result(store.read_json(prefix + '/result.json'))
    require(action.theta['task'] == task, 'negative task does not match its saved action')
    proof = 'by exact True.intro'  # Explicitly allowed through to Lean by proof_profiles.
    if task == 'local':
        proof = positive.C_partial[0].proof_term.partition('\n')[0] + '\n' + proof
    candidate = replace(positive.C_partial[0], proof_term=proof)
    outcome = replace(positive, C_partial=(candidate,), artifacts=())
    folder = 'negative-' + task
    checkpoint_before = store.load_checkpoint()
    store.write_json(folder+'/candidate.json',candidate.to_dict())
    store.write_json(folder+'/state_before.json',before.to_dict())
    began = time.monotonic()
    after, checks = verify_and_update(before,action,outcome,LeanChecker(),{
        'source_sha256':before.G.sha256,'run_dir':str(store.root),
        'attempt_dir':str(store.path(folder)),'seconds':seconds})
    elapsed = time.monotonic()-began
    store.write_json(folder+'/result.json',replace(outcome,cost=Cost(elapsed,1)).to_dict())
    store.write_json(folder+'/verification.json',{'checks':checks,'seconds':elapsed,
        'scope':'diagnostic probe; not a committed runtime action'})
    store.write_json(folder+'/state_after.json',after.to_dict())
    validate_invariant(after)
    require(after == before, task+': rejected proof changed the state or its budget')
    require(store.load_checkpoint() == checkpoint_before, task+': diagnostic probe changed the live checkpoint')
    rejected = [d['check'] for d in checks if 'check' in d]
    require(len(rejected)==1, task+': wrong proof did not receive exactly one actual check')
    checked = rejected[0]
    require(checked.get('accepted') is False and checked.get('status') == 'incomplete'
            and checked.get('sigma',{}).get('code') == 'lean_check_failed'
            and checked.get('evidence',{}).get('returncode') not in (None,0),
            task+': wrong proof was not rejected by real Lean compilation')
    evidence = checked['evidence']
    paths = [Path(a['path']) for a in evidence.get('artifacts',())]
    require(any(p.name=='Candidate.lean' for p in paths) and any(p.name=='stdout.jsonl' for p in paths),
            task+': actual rejected Lean source or diagnostic log is missing')
    if task == 'uniqueness_bridge':
        require(any(d.get('code')=='invariant_update_rejected' for d in checks),
                'unverified bridge children were not rolled back')
    return {'task':task,'round':number,'passed':True,'real_lean_rejection':True,
            'state_unchanged':True,'checkpoint_unchanged':True,'actual_wall_seconds':elapsed,
            'evidence_directory':str(store.path(folder))},evidence


def acceptance(args, output):
    command = [sys.executable,'-m','agent_v2.cli','run','--identity',IDENTITY,
        '--method','recurrence','--scope','full','--selector','rule','--max-steps','5',
        '--pause-after','1','--seconds',str(args.seconds),'--output-root',str(output/'runs')]
    summary, record = execute(command,output,'cli_local',args.seconds+60)
    store = RunStore(summary['run_dir'])
    initial = ResidualState.from_dict(store.read_json('initial_state.json'))
    validate_invariant(initial)
    require(not initial.C and initial.O==(initial.root,) and not initial.links and initial.b.actions==5,
            'unexpected initial proof state')
    state, paths = checkpoint_snapshot(store,output,'local',initial,rounds=1,count=1,leaves=1,links=0)
    require(not paths['resume_checks'] and not paths['final_checks'], 'initial action performed hidden replay or final acceptance')
    records = [cert.to_dict()['evidence'] for cert in state.C]
    commands, stage_reports, replay_count = [record], [], 0
    # Two distinct leaves always include an initial value, regardless of routing.
    schedule = [('bridge',1,2,3,1,False),('two_leaves',2,4,1,3,False),
                ('all_leaves',1,5,0,4,False),('original',None,5,0,4,True),
                ('final_replay',None,5,0,4,True)]
    initial_pause_round, initial_pause_tasks = 4, []
    for label,pause,rounds,leaves,links,proved in schedule:
        previous, old_paths = state, paths
        command = [sys.executable,'-m','agent_v2.cli','resume','--run-dir',str(store.root)]
        if pause is not None: command += ['--pause-after',str(pause)]
        _, record = execute(command,output,'cli_'+label,args.seconds+60,proved=proved)
        commands.append(record)
        state, paths = checkpoint_snapshot(store,output,label,initial,rounds=rounds,
                                          count=rounds,leaves=leaves,links=links,proved=proved)
        fresh, checked_count = audit_resume(store,previous,state,old_paths,paths,
            action_delta=rounds-previous.round_index,final_delta=1 if proved else 0)
        records.extend(fresh); replay_count += checked_count
        stage_reports.append({'stage':label,'rounds':state.round_index,'C':len(state.C),'O':len(state.O),
            'links':len(state.links),'original_identity_proved':proved,'fresh_replay_checks':checked_count,
            'budget_before':previous.b.to_dict(),'budget_after':state.b.to_dict(),
            'wall_seconds':record['seconds']})
        if label == 'two_leaves':
            initial_pause_tasks = [store.read_json(f'rounds/{number}/action.json')['theta']['task']
                                   for number in (3,4)]
            closed_tasks = set(initial_pause_tasks)
            require(len(closed_tasks)==2 and closed_tasks <= set(TASKS[1:])
                    and bool(closed_tasks & {'initial_zero','initial_one'}),
                    'C4 checkpoint did not close two distinct leaves including an initial value')
        if label == 'bridge':
            front = analyze_source(state.G.to_dict(),store.root)
            bp = closure_blueprint(front,{c.id:c.to_dict() for c in state.C})
            require({o.id for o in state.O} == set(bp['obligation_ids'].values()), 'bridge opened incorrect children')
        if label == 'all_leaves':
            require(not paths['final_checks'] and state.status=='incomplete',
                    'O empty was wrongly accepted before original-theorem checking')
            require(previous.round_index == initial_pause_round,
                    'closure did not exercise recovery immediately after an initial value')
    require(replay_count==17 and len(paths['final_checks'])==2,
            'staged replay/final checks were omitted or duplicated')
    steps, round_records = audit_rounds(store,initial)
    records.extend(round_records)
    store.write_bytes('assembled_proof.txt',(assemble_term(state)+'\n').encode())
    negatives = []
    for step in steps:
        negative,evidence = negative_round(store,step['round'],step['task'],args.seconds)
        negatives.append(negative); records.append(evidence)
    verify_source(state.G,store.root)
    report = {'schema_version':1,'passed':True,'identity':IDENTITY,'original_theorem':THEOREM,
        'scope':'single_real_Train_five_action_recurrence_closure','run_dir':str(store.root),
        'source_sha256':state.G.sha256,'original_declaration':state.G.declaration,
        'steps':steps,'stages':stage_reports,'C_final':[c.id for c in state.C],
        'O_final':[],'links_final':len(state.links),'original_identity_proved':True,
        'real_core_constructions':1,'real_partial_lean_checks':5,'fresh_replay_checks':replay_count,
        'initial_value_pause_round':initial_pause_round,'resumed_after_initial_value':True,
        'tasks_closed_before_initial_value_resume':initial_pause_tasks,
        'real_original_lean_checks':2,'negative_proofs':negatives,'resume_repeated_actions':0,
        'artifact_hashes_checked':artifact_hashes(store,records),
        'commands':[r['command'] for r in commands],'cli_seconds':sum(r['seconds'] for r in commands),
        'diagnostic_probe_seconds':sum(n['actual_wall_seconds'] for n in negatives),
        'remaining_budget':state.b.to_dict(),'test_data_read':False,'model_calls':0,
        'historical_proofs_reused':False,'standard_library_modules_with_Test_component':list(
            state.C[0].evidence.get('standard_library_modules_with_Test_component',()))}
    save(output/'summary.json',report)
    print(json.dumps(report,ensure_ascii=False))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--seconds',type=positive_float,default=4000.0)
    parser.add_argument('--output-root',default=str(ROOT/'agent_v2/generated/phase3_20261112/recurrence_closure_acceptance'))
    args = parser.parse_args(argv)
    path = Path(args.output_root).absolute()
    output = guard_path(path,path.anchor)
    output.mkdir(parents=True,exist_ok=True)
    require(not any(output.iterdir()),'evidence directory already exists; choose a new directory')
    try:
        acceptance(args,output)
    except Exception as error:
        save(output/'summary.json',{'schema_version':1,'passed':False,'identity':IDENTITY,
            'scope':'single_real_Train_five_action_recurrence_closure','error_type':type(error).__name__,
            'message':str(error),'original_identity_proved':False})
        raise


if __name__ == '__main__':
    main()
