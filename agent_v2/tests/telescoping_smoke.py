"""Integration acceptance: one real Train CAS/Lean run, replay, and wrong-proof rejection.

Run explicitly with ``python3 -m agent_v2.tests.telescoping_smoke``. There are no
test doubles, model calls, held-out inputs or historical proof imports here.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

from agent_v2.formal_frontend import analyze_source
from agent_v2.lean_checker import LeanChecker
from agent_v2.models import ResidualState
from agent_v2.executor import validate_invariant
from agent_v2.storage import RunStore, guard_path, verify_source

ROOT = Path(__file__).resolve().parents[2]
IDENTITY = 'FQI-SRC-AP-3.3.9'


def execute(command, output, label, timeout):
    started = time.monotonic()
    process = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=timeout)
    record = {'command': command, 'returncode': process.returncode,
              'seconds': time.monotonic() - started, 'stdout': process.stdout, 'stderr': process.stderr}
    (output / (label + '.json')).write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n')
    if process.returncode != 2:
        raise RuntimeError(f'{label}: expected explicit incomplete exit 2; got {record}')
    summary = json.loads(process.stdout.splitlines()[-1])
    if summary['status'] != 'incomplete' or summary['original_identity_proved']:
        raise RuntimeError(f'{label}: inaccurate original proof status: {summary}')
    return summary, record


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--seconds', type=float, default=600.0)
    parser.add_argument('--output-root', default=str(ROOT / 'agent_v2/generated/telescoping_phase1_20261111/acceptance'))
    args = parser.parse_args(argv)
    output = guard_path(Path(args.output_root).absolute(), Path(args.output_root).absolute().anchor)
    output.mkdir(parents=True, exist_ok=True)
    if any(output.iterdir()):
        raise RuntimeError('acceptance evidence already exists; choose a new output directory')
    command = [sys.executable, '-m', 'agent_v2.cli', 'run', '--identity', IDENTITY,
               '--method', 'telescoping', '--selector', 'rule', '--max-steps', '1',
               '--seconds', str(args.seconds), '--output-root', str(output / 'runs')]
    summary, initial_command = execute(command, output, 'cli_run', args.seconds + 60)
    store = RunStore(summary['run_dir'])
    before = ResidualState.from_dict(store.read_json('initial_state.json'))
    first = ResidualState.from_dict(store.load_checkpoint()['state'])
    validate_invariant(first)
    verify_source(first.G, store.root)
    assert before.C == () and len(before.O) == 1
    assert len(first.C) == 1 and first.O == before.O and first.links == ()
    frontend = analyze_source(first.G.to_dict(), run_root=store.root)
    assert first.C[0].proposition == frontend['local_proposition']
    method = store.read_json('rounds/1/result.json')
    assert method['raw_result']['core']['status'] == 'constructed'
    first_receipt = first.C[0].evidence
    assert first_receipt['returncode'] == 0
    assert set(first_receipt['axioms']) <= {'propext', 'Classical.choice', 'Quot.sound'}
    command = [sys.executable, '-m', 'agent_v2.cli', 'resume', '--run-dir', str(store.root)]
    _, replay_command = execute(command, output, 'cli_resume', args.seconds + 60)
    replay = ResidualState.from_dict(store.load_checkpoint()['state'])
    validate_invariant(replay)
    verify_source(replay.G, store.root)
    assert replay.round_index == first.round_index == 1
    assert replay.O == before.O and len(replay.C) == 1
    assert replay.C[0].evidence['artifacts'] != first_receipt['artifacts'], 'resume reused old receipt'
    assert replay.C[0].evidence['returncode'] == 0
    candidate = {key: getattr(replay.C[0], key) for key in
                 ('id', 'proposition', 'proof_term', 'source_sha256')}
    candidate.update(theorem='AgentV2Candidate.proof', dependencies=[], proof_term='by rfl')
    negative = LeanChecker().check_partial(candidate,
        {'run_dir': str(store.root), 'attempt_dir': str(store.root / 'negative-proof'),
         'source_sha256': replay.G.sha256, 'source': replay.G.to_dict(), 'seconds': args.seconds})
    store.write_json('negative-proof/result.json', negative)
    assert not negative['accepted'] and negative['status'] == 'incomplete', negative
    assert negative['sigma']['code'] == 'lean_check_failed', negative
    assert negative['evidence']['returncode'] != 0, negative
    records = [first_receipt, replay.C[0].evidence, negative['evidence']]
    count = 0
    for receipt in records:
        for artifact in receipt['artifacts']:
            path = guard_path(artifact['path'], store.root)
            assert hashlib.sha256(path.read_bytes()).hexdigest() == artifact['sha256'], str(path)
            count += 1
    report = {'schema_version': 1, 'passed': True, 'identity': IDENTITY,
        'scope': 'single_real_Train_local_proof', 'run_dir': str(store.root),
        'source_sha256': replay.G.sha256, 'local_proposition': replay.C[0].proposition,
        'C_before': len(before.C), 'C_after': len(replay.C),
        'O_before': [o.id for o in before.O], 'O_after': [o.id for o in replay.O],
        'status': replay.status, 'original_identity_proved': False,
        'real_core_constructed': True, 'real_lean_verified': True,
        'resume_fresh_lean_verified': True, 'wrong_proof_rejected_by_lean': True,
        'artifact_hashes_checked': count, 'commands': [initial_command['command'], replay_command['command']],
        'test_data_read': False, 'test_data_scope': 'benchmark held-out split',
        'standard_library_modules_with_Test_component':
            list(replay.C[0].evidence.get('standard_library_modules_with_Test_component', [])),
        'model_calls': 0}
    (output / 'acceptance.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(report, ensure_ascii=False))


if __name__ == '__main__':
    main()
