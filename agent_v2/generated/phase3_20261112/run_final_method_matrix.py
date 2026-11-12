"""Fresh per-method checks on one frozen runtime; no upgrades or proof shortcuts."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from agent_v2.executor import validate_invariant
from agent_v2.models import ResidualState, thaw
from agent_v2.storage import RunStore, verify_source

LOCAL = (
    ('coefficient', 'FQI-FINITE-Q-BINOMIAL'),
    ('interpolation', 'FQI-SRC-GR2-I-20'),
    ('determinant', 'FQI-SRC-AP-11.2.4'),
    ('kernel_transform', 'FQI-SRC-AQ-3.23'),
    ('difference_ring', 'FQI-SRC-FINE-2.1'),
    ('macmahon', 'FQI-SRC-GR2-7.Ex14'),
)
SYMBOLIC = (
    ('product', 'FQI-POCHHAMMER-RESIDUES'),
    ('noncommutative', 'FQI-SRC-KAC-CHEUNG-5.7'),
    ('combinatorial', 'FQI-FINITE-Q-BINOMIAL'),
)


def save(path, data):
    path.write_text(json.dumps(thaw(data), ensure_ascii=False, indent=2) + '\n')


def execute(command, output, label, timeout, expected=0):
    started = time.monotonic()
    with (output / (label + '.stdout.log')).open('w') as stdout, (output / (label + '.stderr.log')).open('w') as stderr:
        process = subprocess.run(command, cwd=ROOT, stdout=stdout, stderr=stderr, timeout=timeout)
    record = {'command': command, 'returncode': process.returncode,
              'wall_seconds': time.monotonic() - started,
              'stdout': str(output / (label + '.stdout.log')), 'stderr': str(output / (label + '.stderr.log'))}
    save(output / (label + '.command.json'), record)
    if process.returncode != expected:
        raise RuntimeError(label + ': unexpected exit ' + str(process.returncode))
    return record


def spectral_boundary(output):
    """A current-source refusal is an expected boundary, not a passing upgrade."""
    identity = 'FQI-SRC-GR2-7.2.24'
    command = [sys.executable, '-m', 'agent_v2.cli', 'run', '--identity', identity,
               '--method', 'spectral', '--seconds', '120', '--output-root', str(output / 'spectral_runs')]
    commands = [execute(command, output, 'spectral_run', 180, expected=2)]
    result = json.loads(Path(commands[0]['stdout']).read_text().splitlines()[-1])
    store = RunStore(result['run_dir'])
    before = ResidualState.from_dict(store.read_json('initial_state.json'))
    first = ResidualState.from_dict(store.load_checkpoint()['state'])
    if store.read_json('run.json')['stop_reason'] != 'not_applicable':
        raise RuntimeError('spectral Source boundary changed')
    commands.append(execute([sys.executable, '-m', 'agent_v2.cli', 'resume', '--run-dir', str(store.root)],
                            output, 'spectral_resume', 180, expected=2))
    last = ResidualState.from_dict(store.load_checkpoint()['state'])
    for state in (first, last):
        validate_invariant(state)
        verify_source(state.G, store.root)
        if (state.status != 'incomplete' or state.G != before.G or state.Gamma != before.Gamma or
                state.r != before.r or state.C or state.O != before.O or state.links or state.round_index != 0):
            raise RuntimeError('spectral refused Source changed the formal state')
    if store.path('rounds').exists() or list(store.root.rglob('Candidate.lean')):
        raise RuntimeError('spectral refusal unexpectedly executed a proof action')
    report = {'verification_passed': True, 'requested_Source_L3_upgrade_passed': False,
              'scope': 'fresh current-runtime Source refusal and resume; no mathematical proof',
              'method': 'spectral', 'identity': identity, 'source_sha256': last.G.sha256,
              'run_dir': str(store.root), 'initial_stop_reason': 'not_applicable',
              'resume_stop_reason': store.read_json('run.json')['stop_reason'],
              'C': 0, 'O': ['original'], 'links': 0, 'lean_calls': 0, 'CAS_calls': 0,
              'original_identity_proved': False, 'commands': commands}
    save(output / 'spectral_boundary.json', report)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-root', required=True)
    args = parser.parse_args()
    output = Path(args.output_root).absolute()
    output.mkdir(parents=True, exist_ok=False)
    started = time.monotonic()
    records = []
    for module, cases, seconds in (
        ('agent_v2.tests.local_method_smoke', LOCAL, 1200),
        ('agent_v2.tests.source_method_smoke', SYMBOLIC, 120),
    ):
        for method, identity in cases:
            print('starting ' + method, flush=True)
            directory = output / method
            command = [sys.executable, '-m', module, '--method', method, '--identity', identity,
                       '--seconds', str(seconds), '--output-root', str(directory)]
            invocation = execute(command, output, method, 4 * seconds + 180)
            summary = json.loads((directory / 'summary.json').read_text())
            if summary.get('passed') is not True or summary.get('method') != method:
                raise RuntimeError(method + ': smoke summary mismatch')
            records.append({'method': method, 'summary': str(directory / 'summary.json'), 'command': invocation})
            save(output / 'progress.json', {'finished': records, 'final_verification_complete': False})
            print('passed ' + method, flush=True)
    boundary = spectral_boundary(output)
    report = {'verification_passed': True, 'third_stage_fully_complete': False,
              'scope': 'fresh six local L3, three Source L2 and one stopped spectral Source boundary',
              'methods': records, 'spectral': boundary, 'wall_seconds': time.monotonic() - started,
              'whole_stage_remaining_gap': 'spectral Source export and local Lean integration',
              'model_calls': 0, 'benchmark_Test_read': False}
    save(output / 'summary.json', report)
    print(json.dumps({'verification_passed': True, 'third_stage_fully_complete': False,
                      'summary': str(output / 'summary.json')}), flush=True)


if __name__ == '__main__':
    main()
