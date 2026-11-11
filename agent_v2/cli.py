"""Bounded local CLI. No old Agent, network model or test-double entrypoints."""
import argparse
from dataclasses import replace
import hashlib
import json
import math
from pathlib import Path
import sys
import time

from .models import Artifact, Budget, ContractError, Cost, initial_state
from .storage import IntegrityError, RunStore, guard_path, load_train, sha256_file

REPOSITORY = Path(__file__).resolve().parents[1]
GENERATED = REPOSITORY / 'agent_v2/generated'
EXIT_CODES = {'original_theorem_proved': 0, 'incomplete': 2,
              'environment_blocked': 3, 'budget_exhausted': 3, 'integrity_error': 4}


def positive_float(value):
    value = float(value)
    if not math.isfinite(value) or value <= 0:
        raise argparse.ArgumentTypeError('expected positive finite seconds')
    return value


def positive_int(value):
    value = int(value)
    if value <= 0:
        raise argparse.ArgumentTypeError('expected positive action count')
    return value


def parser():
    result = argparse.ArgumentParser(description='Agent v2: residual certificate MVP; Train only')
    sub = result.add_subparsers(dest='command', required=True)
    core = sub.add_parser('core-demo', help='one real local symbolic construction; never an original proof')
    core.add_argument('--input', required=True)
    run = sub.add_parser('run', help='one Train original, using only new v2 components')
    run.add_argument('--identity', required=True)
    run.add_argument('--method', choices=['telescoping'], default='telescoping')
    run.add_argument('--selector', choices=['rule'], default='rule')
    run.add_argument('--max-steps', type=positive_int, default=1)
    for command in (core, run):
        command.add_argument('--seconds', type=positive_float, default=30.0)
        command.add_argument('--output-root', default=str(GENERATED))
    resume = sub.add_parser('resume', help='recheck a v2 Train checkpoint, then continue within remaining budget')
    resume.add_argument('--run-dir', required=True)
    return result


def _production():
    from .cas_adapter import CoreAdapter, MethodAdapter
    from .executor import Executor
    from .lean_checker import LeanChecker
    return Executor({'core': CoreAdapter(), 'method': MethodAdapter()}), LeanChecker()


def runtime_dependencies():
    root = REPOSITORY / 'agent_v2'
    paths = sorted(root.glob('*.py')) + sorted((root / 'lean').glob('*.lean'))
    return tuple(Artifact(str(path), sha256_file(path)) for path in paths)


def core_demo(args, store):
    from .cas_adapter import CoreAdapter
    from .executor import normalize_result
    input_path = guard_path(args.input)
    raw_bytes = input_path.read_bytes()
    request = json.loads(raw_bytes)
    store.write_bytes('source/request.json', raw_bytes)
    probe = {'schema_version': 1, 'scope': 'non_formal_core_adapter_probe',
             'input_path': str(input_path), 'input_sha256': hashlib.sha256(raw_bytes).hexdigest(),
             'formal_state': False, 'verified_certificates': [], 'formal_obligations': None,
             'original_identity_proved': False}
    store.write_json('initial_state.json', probe)
    store.write_json('rounds/1/state_before.json', probe)
    store.write_json('rounds/1/candidates.json', {'schema_version': 1, 'candidates': [
        {'T': 'identity', 'M': 'CAS', 'backend': 'core', 'solver': request.get('solver')}]})
    store.write_json('rounds/1/action.json', {'schema_version': 1, 'T': 'identity', 'M': 'CAS',
        'backend': 'core', 'request': request, 'seconds': args.seconds})
    started = time.monotonic()
    result = normalize_result(CoreAdapter().execute(request, store.path('rounds/1/backend'), args.seconds))
    result = replace(result, cost=Cost(time.monotonic() - started, 1))
    if sha256_file(input_path) != probe['input_sha256']:
        raise IntegrityError('core input changed during execution')
    store.write_json('rounds/1/raw_result.json', result.raw_result)
    store.write_json('rounds/1/result.json', result.to_dict())
    status = result.status if result.status in ('environment_blocked', 'budget_exhausted', 'integrity_error') else 'incomplete'
    final = dict(probe, status=status, symbolic_status=result.status,
        stop_reason=result.sigma.code, actual_cost=result.cost.to_dict(),
        diagnostics=list(result.diagnostics), test_data_read=False)
    store.write_json('rounds/1/state_after.json', final)
    store.write_json('run.json', final)
    # The raw input has no original Lean G/Gamma. Do not fabricate an empty-O
    # ResidualState or a graph that claims to formalize a symbolic CAS domain.
    store.write_json('graph.json', {'schema_version': 1, 'scope': 'non_formal_probe',
                                  'formal_graph': None})
    return status


def train_run(args, store):
    from .graph import Graph, Outlet
    from .loop import run
    source = load_train(args.identity, store, REPOSITORY)
    source = replace(source, dependencies=source.dependencies + runtime_dependencies())
    state, representation = initial_state(source, Budget(args.seconds, args.max_steps))
    graph = Graph(source.sha256)
    graph.add_node(representation)
    graph.add_outlet(Outlet('telescoping', representation.id, 'CAS', 'method',
        {'method': args.method, 'seconds': args.seconds}, ('lean_source',),
        provenance=('new_v2_method_contract',)))
    executor, checker = _production()
    return run(state, graph, store, executor, checker).status


def resume_run(args):
    from .loop import resume, run
    store = RunStore(guard_path(args.run_dir, GENERATED))
    executor, checker = _production()
    saved = store.load_checkpoint()['state']['G']
    # A CLI checkpoint cannot remap a Train identity to a convenient synthetic
    # theorem even if a caller recomputes the checkpoint's content hashes.
    manifest = REPOSITORY / 'benchmark/splits/train.jsonl'
    rows = [json.loads(line) for line in manifest.read_text().splitlines() if line.strip()]
    matches = [row for row in rows if row['id'] == saved['identity']]
    if len(matches) != 1 or saved['sha256'] != matches[0]['lean_sha256'] or \
            Path(saved['path']) != guard_path(REPOSITORY / 'benchmark' / matches[0]['lean_path']):
        raise IntegrityError('checkpoint not bound to the selected Train original')
    state, graph = resume(store, checker)
    return run(state, graph, store, executor, checker).status, store


def main(argv=None):
    args = parser().parse_args(argv)
    store = None
    try:
        if args.command == 'resume':
            status, store = resume_run(args)
        else:
            if args.command == 'core-demo': guard_path(args.input)
            root = guard_path(args.output_root, GENERATED)
            store = RunStore.create(root)
            status = core_demo(args, store) if args.command == 'core-demo' else train_run(args, store)
    except (IntegrityError, ContractError, ValueError, KeyError, TypeError) as error:
        status = 'integrity_error'
        if store:
            store.write_json('error.json', {'schema_version': 1, 'status': status,
                                         'message': str(error), 'original_identity_proved': False})
        print(json.dumps({'status': status, 'message': str(error)}, ensure_ascii=False), file=sys.stderr)
    except (OSError, ImportError) as error:
        status = 'environment_blocked'
        if store:
            store.write_json('error.json', {'schema_version': 1, 'status': status,
                                         'message': str(error), 'original_identity_proved': False})
        print(json.dumps({'status': status, 'message': str(error)}, ensure_ascii=False), file=sys.stderr)
    print(json.dumps({'schema_version': 1, 'status': status,
        'original_identity_proved': status == 'original_theorem_proved',
        'run_dir': str(store.root) if store else None}, ensure_ascii=False))
    return EXIT_CODES[status]


if __name__ == '__main__':
    raise SystemExit(main())
