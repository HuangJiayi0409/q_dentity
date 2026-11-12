"""Real Source-only L2 CLI construction and resume; no core/checker substitutes."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import time

from agent_v2.cli import positive_float
from agent_v2.executor import normalize_result, validate_invariant
from agent_v2.method_registry import builtin_registry
from agent_v2.models import ResidualState, thaw
from agent_v2.storage import RunStore, guard_path, sha256_file, verify_source

ROOT = Path(__file__).resolve().parents[2]


def require(value, message):
    if not value:
        raise RuntimeError(message)


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(thaw(value), ensure_ascii=False, indent=2) + '\n')


def cli(command, output, label, seconds, status='incomplete', code=2):
    began = time.monotonic()
    full = [sys.executable, '-m', 'agent_v2.cli', *command]
    proc = subprocess.run(full, cwd=ROOT, capture_output=True, text=True, timeout=seconds+60)
    record = {'command': full, 'returncode': proc.returncode, 'stdout': proc.stdout,
              'stderr': proc.stderr, 'wall_seconds': time.monotonic()-began}
    save(output/(label+'.json'), record)
    require(proc.returncode == code, label + ': unexpected CLI exit')
    summary = json.loads(proc.stdout.splitlines()[-1])
    require(summary['status'] == status and summary['original_identity_proved'] is False,
            label + ': wrong classification or original theorem claim')
    return RunStore(summary['run_dir']), record


def untouched(before, after):
    validate_invariant(after)
    require(after.G == before.G and after.Gamma == before.Gamma and after.r == before.r,
            'original Source/context/representation changed')
    require(not after.C and after.O == before.O == (before.root,) and not after.links,
            'symbolic-only construction changed formal certificates or obligations')


def audit_artifacts(store, result):
    # Every nested backend receipt is covered separately because the common
    # adapter contract deliberately lists only files in its own directory.
    records = [result.to_dict()]
    for path in store.path('rounds/1/backend').rglob('cas_return.json'):
        records.append(json.loads(path.read_text()))
    seen = {}
    for record in records:
        for item in record.get('artifacts', []):
            path = guard_path(item['path'], store.root)
            require(sha256_file(path) == item['sha256'], 'backend artifact hash mismatch')
            seen[str(path)] = item['sha256']
    require(bool(seen), 'missing symbolic evidence artifacts')
    return seen


def acceptance(args, output):
    spec = builtin_registry().get(args.method)
    require(spec.capability_level == 'L2' and not spec.local_lean and not spec.full_original,
            'this smoke requires a registered Source-only L2 method')
    command = ['run', '--identity', args.identity, '--method', args.method,
               '--max-steps', '2', '--seconds', str(args.seconds), '--output-root', str(output/'runs')]
    store, run_command = cli(command, output, 'cli_run', args.seconds)
    initial = ResidualState.from_dict(store.read_json('initial_state.json'))
    first = ResidualState.from_dict(store.load_checkpoint()['state'])
    untouched(initial, first)
    verify_source(first.G, store.root)
    require(first.round_index == 1 and first.b.actions == 1 and first.b.seconds < initial.b.seconds,
            'real construction action was not charged exactly once')
    require(store.read_json('run.json')['stop_reason'] == 'symbolic_translation_pending', 'wrong source-only stop')
    result = normalize_result(store.read_json('rounds/1/result.json'))
    require(result.status == 'symbolic_constructed' and not result.C_partial and not result.O_res,
            'symbolic construction exported formal state or did not construct')
    require(result.raw_result.get('execution_scope') == 'source_symbolic_only', 'missing source-only scope')
    require(result.raw_result.get('capability_level') == 'L2', 'actual Source capability mislabeled')
    require(result.raw_result['core']['status'] == 'constructed', 'actual core did not construct')
    require(result.raw_result['independent_symbolic_check']['status'] == 'passed', 'symbolic checking failed')
    require(result.raw_result['lean_verified'] is False, 'symbolic output incorrectly labeled Lean verified')
    require(result.cost.actions == 1 and result.cost.wall_seconds > 0, 'actual cost missing')
    require(abs(initial.b.seconds-first.b.seconds-result.cost.wall_seconds) < 1e-8, 'budget charge mismatch')
    artifacts = audit_artifacts(store, result)
    processes = list(store.path('rounds/1/backend').rglob('process.json'))
    require(bool(processes), 'no actual mathematical process recorded')
    for path in processes:
        process = json.loads(path.read_text())
        require(process['returncode'] == 0 and not process['timed_out'] and not process['cleanup_survivors'],
                'actual core process failed or leaked descendants')
    require(not list(store.root.rglob('Candidate.lean')) and not store.path('resume_checks').exists(),
            'unexpected Lean proof activity in symbolic-only run')
    save(output/'state_before_resume.json', first.to_dict())
    _, resume_command = cli(['resume', '--run-dir', str(store.root)], output, 'cli_resume', args.seconds)
    replay = ResidualState.from_dict(store.load_checkpoint()['state'])
    untouched(first, replay)
    verify_source(replay.G, store.root)
    require(replay.round_index == 1 and replay.b.actions == 1 and replay.attempts == first.attempts,
            'resume repeated an action')
    require(replay.b.seconds <= first.b.seconds, 'resume restored spent wall budget')
    require(audit_artifacts(store, result) == artifacts, 'resume changed existing symbolic evidence')
    require(len(list(store.path('rounds').iterdir())) == 1 and
            not store.path('resume_checks').exists() and not list(store.root.rglob('Candidate.lean')),
            'resume started a new CAS or Lean attempt')
    require(store.read_json('run.json')['stop_reason'] == 'symbolic_translation_pending', 'wrong resume stop')

    mismatch, mismatch_command = cli(['run', '--identity', args.mismatch_identity,
        '--method', args.method, '--seconds', str(args.seconds), '--output-root', str(output/'mismatch')],
        output, 'cli_mismatch', args.seconds)
    wrong = ResidualState.from_dict(mismatch.load_checkpoint()['state'])
    untouched(ResidualState.from_dict(mismatch.read_json('initial_state.json')), wrong)
    verify_source(wrong.G, mismatch.root)
    require(wrong.round_index == 0 and not mismatch.path('rounds').exists() and
            mismatch.read_json('run.json')['stop_reason'] == 'not_applicable', 'mismatch executed the core')

    tiny, tiny_command = cli(['run', '--identity', args.identity, '--method', args.method,
        '--seconds', '0.000001', '--output-root', str(output/'tiny_budget')],
        output, 'cli_tiny_budget', args.seconds, 'budget_exhausted', 3)
    exhausted = ResidualState.from_dict(tiny.load_checkpoint()['state'])
    untouched(ResidualState.from_dict(tiny.read_json('initial_state.json')), exhausted)
    verify_source(exhausted.G, tiny.root)
    require(exhausted.round_index == 0 and not tiny.path('rounds').exists(),
            'unaffordable action was launched')
    summary = {'passed': True, 'scope': 'one_real_Train_Source_symbolic_only',
        'method': spec.id, 'method_version': spec.version, 'capability_level': spec.capability_level,
        'identity': initial.G.identity, 'theorem': initial.G.theorem, 'source_sha256': initial.G.sha256,
        'run_dir': str(store.root), 'mismatch_run_dir': str(mismatch.root), 'tiny_budget_run_dir': str(tiny.root),
        'C_before': 0, 'C_after': 0, 'O_before': ['original'], 'O_after': ['original'],
        'links_before': 0, 'links_after': 0, 'original_identity_proved': False,
        'result_status': result.status, 'stop_reason': 'symbolic_translation_pending',
        'core_constructed': True, 'independent_symbolic_check': result.raw_result['independent_symbolic_check'],
        'lean_calls': 0, 'resume_repeated_actions': 0, 'resume_lean_calls': 0,
        'budget_actions_charged': 1, 'actual_action_seconds': result.cost.wall_seconds,
        'artifact_hashes_checked': len(artifacts), 'artifacts': artifacts,
        'commands': [run_command, resume_command, mismatch_command, tiny_command],
        'model_calls': 0, 'test_data_read': False}
    save(output/'summary.json', summary)
    print(json.dumps({'passed': True, 'method': spec.id, 'summary': str(output/'summary.json')}))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--method', required=True)
    parser.add_argument('--identity', required=True)
    parser.add_argument('--mismatch-identity', default='FQI-GAUSS-ALTERNATING')
    parser.add_argument('--output-root', required=True)
    parser.add_argument('--seconds', type=positive_float, default=120)
    args = parser.parse_args(argv)
    output = Path(args.output_root).absolute()
    output = guard_path(output, output.anchor)
    output.mkdir(parents=True, exist_ok=True)
    require(not any(output.iterdir()), 'evidence directory must be empty')
    acceptance(args, output)


if __name__ == '__main__':
    main()
