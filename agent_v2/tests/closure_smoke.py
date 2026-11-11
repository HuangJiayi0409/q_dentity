"""Explicit integration: real Train finite-sum closure, fresh replay and bad bridge.

Run with ``python3 -m agent_v2.tests.closure_smoke``. Every mathematical check
uses the production LeanChecker. No test doubles, model APIs, Test inputs or
historical proof imports are used. This module is not a unittest-discovery test.
"""
import argparse
from dataclasses import replace
import json
from pathlib import Path
import subprocess
import sys
import time

from agent_v2.cli import positive_float
from agent_v2.executor import (assemble_term, normalize_result, validate_invariant,
                               verify_and_update)
from agent_v2.lean_checker import LeanChecker
from agent_v2.models import Cost, JointAction, ResidualState
from agent_v2.storage import RunStore, guard_path, sha256_file, verify_source


ROOT = Path(__file__).resolve().parents[2]
IDENTITY = 'FQI-SRC-AP-3.3.9'
SOURCE_SHA256 = 'd9a88ffda89d1bbb38da774ac9f30bba41b11674e6057b698c11d0407dc26efa'
ALLOWED_AXIOMS = {'propext', 'Classical.choice', 'Quot.sound'}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def execute(command, output, label, timeout):
    started = time.monotonic()
    record = {'command': command}
    try:
        process = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=timeout)
        record.update(returncode=process.returncode, stdout=process.stdout, stderr=process.stderr)
    except subprocess.TimeoutExpired as error:
        record.update(returncode=None, timed_out=True,
                      stdout=str(error.stdout or ''), stderr=str(error.stderr or ''))
        raise
    finally:
        record['seconds'] = time.monotonic() - started
        save(output / (label + '.json'), record)
    require(process.returncode == 0, f'{label}: original proof CLI did not exit 0; see {label}.json')
    summary = json.loads(process.stdout.splitlines()[-1])
    require(summary.get('status') == 'original_theorem_proved'
            and summary.get('original_identity_proved') is True,
            f'{label}: missing strict original-theorem acceptance: {summary}')
    return summary, record


def check_receipt(receipt, source, *, original=False):
    require(receipt.get('returncode') == 0, 'Lean compilation did not succeed')
    require(receipt.get('source_sha256') == source.sha256, 'Lean receipt source mismatch')
    require(isinstance(receipt.get('axioms'), (list, tuple))
            and set(receipt['axioms']) <= ALLOWED_AXIOMS, 'unexpected or absent axiom audit')
    audit = receipt.get('audit', {})
    expected = source.theorem if original else 'AgentV2Candidate.proof'
    require(audit.get('theorem') == expected, 'Lean audit theorem mismatch')
    require(bool(receipt.get('artifacts')), 'Lean artifact inventory missing')


def artifact_hashes(store, records):
    count = 0
    for record in records:
        for artifact in record.get('artifacts', ()):
            path = guard_path(artifact['path'], store.root)
            require(sha256_file(path) == artifact['sha256'], 'artifact hash mismatch: ' + str(path))
            count += 1
    return count


def audit_rounds(store, initial):
    steps, records = [], []
    prior = initial
    for number in range(1, 5):
        prefix = f'rounds/{number}'
        before = ResidualState.from_dict(store.read_json(prefix + '/state_before.json'))
        after = ResidualState.from_dict(store.read_json(prefix + '/state_after.json'))
        action = JointAction.from_dict(store.read_json(prefix + '/action.json'))
        result = normalize_result(store.read_json(prefix + '/result.json'))
        validate_invariant(before)
        validate_invariant(after)
        verify_source(after.G, store.root)
        require(before == prior, 'round does not start from the previous saved residual')
        require(before.G == initial.G and after.G == initial.G and after.Gamma == initial.Gamma,
                'source or original context changed')
        require(action.T == 'identity' and action.source == action.target == before.r == after.r,
                'identity action changed the current representation')
        require(len(result.C_partial) == 1 and len(after.C) == len(before.C) + 1,
                'each closure round must construct and verify exactly one candidate')
        require(after.C[:-1] == before.C and after.C[-1].id == result.C_partial[0].id,
                'certificate progress differs from the selected candidate')
        require(after.b.actions == before.b.actions - 1 and result.cost.actions == 1,
                'one round did not charge exactly one action')
        require(0 < result.cost.wall_seconds <= before.b.seconds
                and after.b.seconds < before.b.seconds, 'missing actual round cost')
        candidates = store.read_json(prefix + '/candidates.json')
        require(action.to_dict() in candidates['legal'], 'selected action was not in the legal set')
        selection = store.read_json(prefix + '/selection.json')
        require(selection.get('selected') == action.id and bool(selection.get('reason')),
                'selection reason missing or unbound')
        candidate = result.C_partial[0]
        check_receipt(after.C[-1].evidence, initial.G)
        verification = store.read_json(prefix + '/verification.json')
        require(verification.get('certificates_added') == 1
                and verification.get('original_identity_proved') is False,
                'partial candidate validation was confused with final acceptance')
        task = action.theta['task']
        if number == 1:
            require(task == 'local' and after.O == initial.O and not after.links,
                    'local difference candidate prematurely replaced the original')
            require(result.raw_result['core']['status'] == 'constructed', 'real core did not construct')
        elif number == 2:
            require(task == 'bridge' and candidate.dependencies == (before.C[0].id,),
                    'finite-sum bridge lacks its local difference dependency')
            require(candidate.closes == 'original' and len(after.O) == 2 and len(after.links) == 1,
                    'verified bridge did not replace the original with two endpoints')
            require(after.O == candidate.replaces == result.O_res,
                    'formal endpoint obligations differ from the verified connection')
            require(all(o.origin_action == action.id and o.source_sha256 == initial.G.sha256
                        and o.proposition and o.lean_anchor for o in after.O),
                    'endpoint obligations lack exact origin/source/proposition anchors')
        else:
            require(task in ('zero_endpoint', 'upper_endpoint') and not candidate.replaces,
                    'round must close one exact endpoint')
            require(len(after.O) == len(before.O) - 1 and len(after.links) == len(before.links) + 1,
                    'endpoint did not remove exactly one verified leaf')
            require({o.id for o in after.O} == {o.id for o in before.O} - {candidate.closes},
                    'endpoint removed the wrong obligation')
        steps.append({'round': number, 'task': task, 'action_id': action.id,
            'candidate_id': candidate.id, 'proposition': candidate.proposition,
            'dependencies': list(candidate.dependencies), 'C_before': [c.id for c in before.C],
            'C_after': [c.id for c in after.C], 'O_before': [o.to_dict() for o in before.O],
            'O_after': [o.to_dict() for o in after.O], 'links_before': len(before.links),
            'links_after': len(after.links), 'r': after.r, 'cost': result.cost.to_dict()})
        records.extend([after.C[-1].to_dict()['evidence'], result.to_dict()])
        prior = after
    require({step['task'] for step in steps[2:]} == {'zero_endpoint', 'upper_endpoint'},
            'endpoint actions repeated or omitted')
    return steps, records


def negative_bridge(store, seconds):
    """A real rejected connection must leave the saved parent and local C intact."""
    before = ResidualState.from_dict(store.read_json('rounds/2/state_before.json'))
    action = JointAction.from_dict(store.read_json('rounds/2/action.json'))
    original = normalize_result(store.read_json('rounds/2/result.json'))
    candidate = replace(original.C_partial[0], proof_term='by rfl')
    outcome = replace(original, C_partial=(candidate,), artifacts=())
    store.write_json('negative-bridge/candidate.json', candidate.to_dict())
    store.write_json('negative-bridge/state_before.json', before.to_dict())
    started = time.monotonic()
    after, checks = verify_and_update(before, action, outcome, LeanChecker(), {
        'source_sha256': before.G.sha256, 'run_dir': str(store.root),
        'attempt_dir': str(store.path('negative-bridge')), 'seconds': seconds})
    elapsed = time.monotonic() - started
    store.write_json('negative-bridge/result.json', replace(outcome, cost=Cost(elapsed, 1)).to_dict())
    store.write_json('negative-bridge/verification.json', {'checks': checks, 'seconds': elapsed})
    store.write_json('negative-bridge/state_after.json', after.to_dict())
    validate_invariant(after)
    require(after.O == before.O and after.links == before.links and after.C == before.C,
            'bad bridge removed a parent or lost the independent local certificate')
    rejected = [item['check'] for item in checks if 'check' in item]
    require(len(rejected) == 1, 'bad bridge did not receive exactly one actual check')
    checked = rejected[0]
    require(checked.get('accepted') is False and checked.get('status') == 'incomplete'
            and checked.get('sigma', {}).get('code') == 'lean_check_failed'
            and checked.get('evidence', {}).get('returncode') not in (None, 0),
            'bad bridge was not rejected by real Lean compilation')
    require(any(item.get('code') == 'invariant_update_rejected' for item in checks),
            'unverified endpoint replacement was not rolled back')
    return {'passed': True, 'actual_wall_seconds': elapsed, 'parent_preserved': True,
            'independent_local_certificate_preserved': True, 'real_lean_rejection': True}, checked['evidence']


def acceptance(args, output):
    command = [sys.executable, '-m', 'agent_v2.cli', 'run', '--identity', IDENTITY,
        '--method', 'telescoping', '--scope', 'full', '--selector', 'rule', '--max-steps', '4',
        '--seconds', str(args.seconds), '--output-root', str(output / 'runs')]
    summary, initial_command = execute(command, output, 'cli_run', args.seconds + 60)
    store = RunStore(summary['run_dir'])
    initial = ResidualState.from_dict(store.read_json('initial_state.json'))
    first = ResidualState.from_dict(store.load_checkpoint()['state'])
    validate_invariant(initial)
    validate_invariant(first)
    verify_source(first.G, store.root)
    require(first.G.identity == IDENTITY and first.G.sha256 == SOURCE_SHA256
            and first.G.theorem == 'FiniteQBenchmark.Identity272.statement', 'selected Train source drifted')
    require(not initial.C and len(initial.O) == 1 and not initial.links, 'unexpected initial residual')
    require(first.status == 'original_theorem_proved' and not first.O and len(first.C) == 4
            and len(first.links) == 3 and first.round_index == 4, 'incomplete original proof tree')
    steps, records = audit_rounds(store, initial)
    final_paths = set(store.path('final').glob('*/checked.json'))
    require(len(final_paths) == 1, 'expected one initial original acceptance')
    first_final_path = next(iter(final_paths))
    first_final = json.loads(first_final_path.read_text())
    require(first_final.get('accepted') is True, 'first final acceptance was rejected')
    check_receipt(first_final['evidence'], first.G, original=True)
    request = json.loads((first_final_path.parent / 'request.json').read_text())
    require(request['proof_term'] == assemble_term(first), 'final term differs from the actual proof tree')
    store.write_bytes('assembled_proof.txt', (assemble_term(first) + '\n').encode())
    records.append(first_final['evidence'])
    command = [sys.executable, '-m', 'agent_v2.cli', 'resume', '--run-dir', str(store.root)]
    _, replay_command = execute(command, output, 'cli_resume', args.seconds + 60)
    replay = ResidualState.from_dict(store.load_checkpoint()['state'])
    validate_invariant(replay)
    verify_source(replay.G, store.root)
    require(replay.round_index == first.round_index and replay.b.actions == first.b.actions
            and replay.links == first.links and not replay.O,
            'resume reran an action, recharged an action or changed the closed proof tree')
    require(replay.b.seconds < first.b.seconds, 'fresh replay/final verification cost was not charged')
    require(len(list(store.path('rounds').iterdir())) == 4, 'resume created an extra CAS/closure action')
    for old, fresh in zip(first.C, replay.C):
        require(replace(old, evidence=fresh.evidence) == fresh, 'replay changed a retained certificate')
        require(old.evidence['artifacts'] != fresh.evidence['artifacts'], 'resume trusted an old receipt')
        check_receipt(fresh.evidence, replay.G)
        records.append(fresh.to_dict()['evidence'])
    replay_files = list(store.path('resume_checks').glob('*/result.json'))
    require(len(replay_files) == 4, 'resume did not freshly check all four certificates')
    new_final_paths = set(store.path('final').glob('*/checked.json')) - final_paths
    require(len(new_final_paths) == 1 and first_final_path.exists(), 'resume overwrote final evidence')
    replay_final = json.loads(next(iter(new_final_paths)).read_text())
    require(replay_final.get('accepted') is True and replay.status == 'original_theorem_proved',
            'fresh original acceptance failed')
    check_receipt(replay_final['evidence'], replay.G, original=True)
    records.append(replay_final['evidence'])
    negative, negative_receipt = negative_bridge(store, args.seconds)
    records.append(negative_receipt)
    report = {'schema_version': 1, 'passed': True, 'identity': IDENTITY,
        'scope': 'single_real_Train_complete_residual_proof', 'run_dir': str(store.root),
        'source_sha256': replay.G.sha256, 'original_theorem': replay.G.theorem,
        'bridge_proposition': steps[1]['proposition'], 'steps': steps,
        'C_final': [c.id for c in replay.C], 'O_final': [], 'links_final': len(replay.links),
        'original_identity_proved': True, 'real_core_constructed': True,
        'real_partial_lean_checks': 4, 'fresh_replay_checks': 4, 'real_original_lean_checks': 2,
        'resume_repeated_actions': 0, 'negative_bridge': negative,
        'artifact_hashes_checked': artifact_hashes(store, records),
        'commands': [initial_command['command'], replay_command['command']],
        'initial_cli_seconds': initial_command['seconds'], 'resume_cli_seconds': replay_command['seconds'],
        'remaining_budget': replay.b.to_dict(), 'test_data_read': False,
        'test_data_scope': 'benchmark held-out split', 'model_calls': 0,
        'standard_library_modules_with_Test_component': list(
            replay.C[0].evidence.get('standard_library_modules_with_Test_component', [])),
        'historical_proofs_reused': False}
    save(output / 'summary.json', report)
    print(json.dumps(report, ensure_ascii=False))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--seconds', type=positive_float, default=1800.0)
    parser.add_argument('--output-root', default=str(
        ROOT / 'agent_v2/generated/closure_and_methods_20261111/closure_acceptance'))
    args = parser.parse_args(argv)
    path = Path(args.output_root).absolute()
    output = guard_path(path, path.anchor)
    output.mkdir(parents=True, exist_ok=True)
    require(not any(output.iterdir()), 'evidence directory already exists; choose a new directory')
    try:
        acceptance(args, output)
    except Exception as error:
        save(output / 'summary.json', {'schema_version': 1, 'passed': False,
            'scope': 'single_real_Train_complete_residual_proof', 'identity': IDENTITY,
            'error_type': type(error).__name__, 'message': str(error)})
        raise


if __name__ == '__main__':
    main()
