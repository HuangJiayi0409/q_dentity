"""Explicit integration: one real Train recurrence, replay and rejected proof.

Run with ``python3 -m agent_v2.tests.recurrence_smoke`` after production sources
are frozen. This is not unittest discovery and contains no fake kernel or CAS.
The verified output is a local sum recurrence; the original theorem stays open.
"""
import argparse
from dataclasses import replace
import json
from pathlib import Path
import subprocess
import sys
import time

from agent_v2.cli import positive_float
from agent_v2.executor import normalize_result, validate_invariant, verify_and_update
from agent_v2.lean_checker import LeanChecker
from agent_v2.models import Cost, JointAction, ResidualState
from agent_v2.recurrence_frontend import PROFILE, analyze_source
from agent_v2.recurrence_translation import reconstruct_candidate
from agent_v2.storage import RunStore, guard_path, sha256_file, verify_source


ROOT = Path(__file__).resolve().parents[2]
IDENTITY = 'FQI-GAUSS-ALTERNATING'
SOURCE_SHA256 = 'c49f5a4417e3d4d19df4463a377c4d3117cea07619d1867156eccb454ca8123c'
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
    require(process.returncode == 2, f'{label}: expected incomplete exit 2; see {label}.json')
    summary = json.loads(process.stdout.splitlines()[-1])
    require(summary.get('status') == 'incomplete' and summary.get('original_identity_proved') is False,
            f'{label}: local recurrence must not imply original proof success')
    return summary, record


def check_receipt(receipt, source):
    require(receipt.get('returncode') == 0, 'real Lean compilation did not succeed')
    require(receipt.get('source_sha256') == source.sha256, 'Lean receipt source mismatch')
    require(receipt.get('profile') == PROFILE, 'wrong mathematical Lean profile')
    require(isinstance(receipt.get('axioms'), (tuple, list))
            and set(receipt['axioms']) <= ALLOWED_AXIOMS, 'absent or unexpected axiom audit')
    audit = receipt.get('audit', {})
    require(audit.get('theorem') == 'AgentV2Candidate.proof', 'wrong audited local theorem')
    require(audit.get('universe_parameters') == ['u'] or audit.get('universe_parameters') == ('u',),
            'original Field universe was specialized')
    require(bool(receipt.get('artifacts')), 'missing verification artifacts')


def check_artifacts(store, records):
    count = 0
    for record in records:
        for artifact in record.get('artifacts', ()):
            path = guard_path(artifact['path'], store.root)
            require(sha256_file(path) == artifact['sha256'], 'artifact hash mismatch: ' + str(path))
            count += 1
    return count


def negative_proof(store, seconds):
    before = ResidualState.from_dict(store.read_json('rounds/1/state_before.json'))
    action = JointAction.from_dict(store.read_json('rounds/1/action.json'))
    original = normalize_result(store.read_json('rounds/1/result.json'))
    candidate = original.C_partial[0]
    # The header carries the untrusted symbolic witness used by deterministic
    # reconstruction. Retain it so the wrong body reaches the actual kernel.
    header = candidate.proof_term.partition('\n')[0]
    candidate = replace(candidate, proof_term=header + '\nby rfl')
    outcome = replace(original, C_partial=(candidate,), artifacts=())
    store.write_json('negative-proof/candidate.json', candidate.to_dict())
    store.write_json('negative-proof/state_before.json', before.to_dict())
    started = time.monotonic()
    after, checks = verify_and_update(before, action, outcome, LeanChecker(), {
        'source_sha256': before.G.sha256, 'run_dir': str(store.root),
        'attempt_dir': str(store.path('negative-proof')), 'seconds': seconds})
    elapsed = time.monotonic() - started
    store.write_json('negative-proof/result.json', replace(outcome, cost=Cost(elapsed, 1)).to_dict())
    store.write_json('negative-proof/verification.json', {'checks': checks, 'seconds': elapsed})
    store.write_json('negative-proof/state_after.json', after.to_dict())
    validate_invariant(after)
    require(after.C == before.C and after.O == before.O and after.links == before.links
            and after.r == before.r, 'rejected recurrence altered the proof state')
    rejected = [item['check'] for item in checks if 'check' in item]
    require(len(rejected) == 1, 'wrong recurrence did not receive exactly one actual check')
    checked = rejected[0]
    require(checked.get('accepted') is False and checked.get('status') == 'incomplete'
            and checked.get('sigma', {}).get('code') == 'lean_check_failed'
            and checked.get('evidence', {}).get('returncode') not in (None, 0),
            'wrong recurrence was not rejected by real Lean compilation')
    return {'passed': True, 'actual_wall_seconds': elapsed, 'real_lean_rejection': True,
            'original_obligation_preserved': True, 'C_unchanged': True}, checked['evidence']


def mismatch(args, output):
    command = [sys.executable, '-m', 'agent_v2.cli', 'run', '--identity', 'FQI-SRC-AP-3.3.9',
        '--method', 'recurrence', '--scope', 'local', '--selector', 'rule', '--max-steps', '1',
        '--seconds', str(args.seconds), '--output-root', str(output / 'mismatched-runs')]
    summary, record = execute(command, output, 'cli_mismatch', args.seconds + 60)
    store = RunStore(summary['run_dir'])
    state = ResidualState.from_dict(store.load_checkpoint()['state'])
    validate_invariant(state)
    verify_source(state.G, store.root)
    require(store.read_json('frontend.json')['status'] == 'not_applicable'
            and store.read_json('run.json')['stop_reason'] == 'not_applicable',
            'mismatched structure did not retain its explicit applicability category')
    require(state.round_index == 0 and state.b.actions == 1 and not state.C
            and state.O == (state.root,) and not state.links,
            'mismatched method executed an action or altered the residual')
    require(store.read_json('graph.json')['outlets'] == [], 'mismatch created a fake executable outlet')
    return {'passed': True, 'run_dir': str(store.root), 'reason': 'not_applicable',
            'actions_executed': 0, 'original_identity_proved': False}, record


def symbolic_only(args, output, frontend):
    request = output / 'recurrence_core_request.json'
    save(request, frontend['core_request'])
    command = [sys.executable, '-m', 'agent_v2.cli', 'core-demo', '--input', str(request),
               '--seconds', str(args.seconds), '--output-root', str(output / 'symbolic-runs')]
    summary, record = execute(command, output, 'cli_core_demo', args.seconds + 60)
    store = RunStore(summary['run_dir'])
    initial = store.read_json('initial_state.json')
    final = store.read_json('run.json')
    result = normalize_result(store.read_json('rounds/1/result.json'))
    require(initial.get('formal_state') is False and initial.get('verified_certificates') == []
            and initial.get('formal_obligations') is None,
            'symbolic-only request fabricated a formal proof state')
    require(result.status == 'symbolic_constructed' and result.sigma.code == 'translation_pending'
            and result.raw_result.get('solver') == 'q_zeilberger'
            and result.raw_result.get('status') == 'constructed',
            'real core-only recurrence did not construct its unverified witness')
    require(not result.C_partial and not result.O_res and result.original_identity_proved is False
            and final.get('verified_certificates') == []
            and final.get('original_identity_proved') is False,
            'symbolic construction bypassed Lean certification')
    return {'passed': True, 'scope': 'non_formal_core_adapter_probe', 'run_dir': str(store.root),
            'symbolic_status': result.status, 'sigma': result.sigma.code,
            'C_increased': False, 'original_identity_proved': False,
            'artifact_hashes_checked': check_artifacts(store, [result.to_dict()])}, record


def acceptance(args, output):
    command = [sys.executable, '-m', 'agent_v2.cli', 'run', '--identity', IDENTITY,
        '--method', 'recurrence', '--scope', 'local', '--selector', 'rule', '--max-steps', '1',
        '--seconds', str(args.seconds), '--output-root', str(output / 'runs')]
    summary, initial_command = execute(command, output, 'cli_run', args.seconds + 60)
    store = RunStore(summary['run_dir'])
    initial = ResidualState.from_dict(store.read_json('initial_state.json'))
    first = ResidualState.from_dict(store.load_checkpoint()['state'])
    validate_invariant(initial)
    validate_invariant(first)
    verify_source(first.G, store.root)
    require(first.G.identity == IDENTITY and first.G.sha256 == SOURCE_SHA256
            and first.G.theorem == 'FiniteQBenchmark.Identity009.statement', 'selected Train source drifted')
    require(first.G == initial.G and first.Gamma == initial.Gamma, 'original source or context changed')
    require(not initial.C and initial.O == (initial.root,) and not initial.links, 'unexpected initial state')
    require(first.status == 'incomplete' and len(first.C) == 1 and first.O == initial.O
            and not first.links and first.round_index == 1, 'local recurrence changed the original proof claim')
    require(first.b.actions == initial.b.actions - 1 and first.b.seconds < initial.b.seconds,
            'actual action/wall-clock budget was not charged')
    action = JointAction.from_dict(store.read_json('rounds/1/action.json'))
    require(action.T == 'identity' and action.source == action.target == first.r == initial.r,
            'identity changed representation')
    require(action.theta['method'] == 'recurrence', 'wrong method executed')
    result = normalize_result(store.read_json('rounds/1/result.json'))
    require(result.status == 'symbolic_constructed' and len(result.C_partial) == 1
            and not result.O_res and result.C_partial[0].closes is None,
            'recurrence adapter did not return one unverified local candidate')
    raw = result.raw_result['core']
    require(raw['solver'] == 'q_zeilberger' and raw['status'] == 'constructed'
            and raw['result']['order'] == 2, 'real core did not construct the supported second-order recurrence')
    frontend = analyze_source(first.G.to_dict(), run_root=store.root)
    require(frontend['status'] == 'applicable', 'saved original no longer satisfies the recurrence contract')
    rebuilt = reconstruct_candidate(frontend, first.C[0].proof_term)
    require(rebuilt.proposition == first.C[0].proposition and rebuilt.id == first.C[0].id,
            'verified local recurrence differs from source-bound witness reconstruction')
    require(first.C[0].id == result.C_partial[0].id, 'C does not contain the selected candidate')
    check_receipt(first.C[0].evidence, first.G)
    records = [result.to_dict(), first.C[0].to_dict()['evidence']]

    command = [sys.executable, '-m', 'agent_v2.cli', 'resume', '--run-dir', str(store.root)]
    _, replay_command = execute(command, output, 'cli_resume', args.seconds + 60)
    replay = ResidualState.from_dict(store.load_checkpoint()['state'])
    validate_invariant(replay)
    verify_source(replay.G, store.root)
    require(replay.round_index == 1 and replay.b.actions == first.b.actions
            and replay.O == first.O and replay.links == first.links and len(replay.C) == 1,
            'resume repeated an action or changed the local proof state')
    require(replay.b.seconds < first.b.seconds, 'fresh replay cost was not charged')
    require(replace(first.C[0], evidence=replay.C[0].evidence) == replay.C[0]
            and first.C[0].evidence['artifacts'] != replay.C[0].evidence['artifacts'],
            'resume trusted an old receipt or changed a certificate')
    require(len(list(store.path('rounds').iterdir())) == 1
            and len(list(store.path('resume_checks').glob('*/result.json'))) == 1,
            'resume did not perform exactly one fresh certificate check without a new round')
    check_receipt(replay.C[0].evidence, replay.G)
    records.append(replay.C[0].to_dict()['evidence'])
    negative, negative_receipt = negative_proof(store, args.seconds)
    records.append(negative_receipt)
    mismatch_report, mismatch_command = mismatch(args, output)
    symbolic_report, core_command = symbolic_only(args, output, frontend)
    report = {'schema_version': 1, 'passed': True, 'identity': IDENTITY,
        'scope': 'single_real_Train_local_recurrence', 'run_dir': str(store.root),
        'source_sha256': replay.G.sha256, 'original_theorem': replay.G.theorem,
        'local_proposition': replay.C[0].proposition, 'certificate_id': replay.C[0].id,
        'real_core_constructed': True, 'recurrence_order': raw['result']['order'],
        'recurrence_coefficients': list(raw['result']['coefficients']),
        'recurrence_certificate': raw['result']['certificate'],
        'C_before': len(initial.C), 'C_after': len(replay.C),
        'O_before': [o.id for o in initial.O], 'O_after': [o.id for o in replay.O],
        'links_before': len(initial.links), 'links_after': len(replay.links),
        'real_partial_lean_checks': 1, 'fresh_replay_checks': 1, 'resume_repeated_actions': 0,
        'original_identity_proved': False, 'status': replay.status,
        'negative_proof': negative, 'not_applicable': mismatch_report, 'symbolic_only': symbolic_report,
        'artifact_hashes_checked': check_artifacts(store, records),
        'commands': [item['command'] for item in
                     (initial_command, replay_command, mismatch_command, core_command)],
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
    parser.add_argument('--seconds', type=positive_float, default=1200.0)
    parser.add_argument('--output-root', default=str(
        ROOT / 'agent_v2/generated/closure_and_methods_20261111/recurrence_acceptance'))
    args = parser.parse_args(argv)
    path = Path(args.output_root).absolute()
    output = guard_path(path, path.anchor)
    output.mkdir(parents=True, exist_ok=True)
    require(not any(output.iterdir()), 'evidence directory already exists; choose a new directory')
    try:
        acceptance(args, output)
    except Exception as error:
        save(output / 'summary.json', {'schema_version': 1, 'passed': False, 'identity': IDENTITY,
            'scope': 'single_real_Train_local_recurrence', 'error_type': type(error).__name__,
            'message': str(error), 'original_identity_proved': False})
        raise


if __name__ == '__main__':
    main()
