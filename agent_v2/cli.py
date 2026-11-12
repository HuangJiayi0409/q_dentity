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
from .loop import ReplayFailure

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


def _explicit_directory(path):
    """Accept the chosen location without resolving away unsafe path aliases.

    The filesystem anchor permits arbitrary explicit output locations while
    retaining guard_path's traversal and symlink checks for every ancestor.
    Individual artifacts remain bounded by their actual RunStore directory.
    """
    path = Path(path).absolute()
    return guard_path(path, path.anchor)


def parser():
    from .method_registry import builtin_registry
    result = argparse.ArgumentParser(description='Agent v2: residual certificate MVP; Train only')
    sub = result.add_subparsers(dest='command', required=True)
    sub.add_parser('methods', help='show actual registered capabilities and limitations')
    core = sub.add_parser('core-demo', help='one real local symbolic construction; never an original proof')
    core.add_argument('--input', required=True)
    probe = sub.add_parser('method-demo', help='one registered typed symbolic request; no formal theorem is implied')
    probe.add_argument('--method', choices=builtin_registry().ids(), required=True)
    probe.add_argument('--input', required=True)
    run = sub.add_parser('run', help='one Train original, using only new v2 components')
    run.add_argument('--identity', required=True)
    run.add_argument('--method', choices=builtin_registry().ids(), default='telescoping')
    run.add_argument('--selector', choices=['rule'], default='rule')
    run.add_argument('--scope', choices=['local', 'full'], default='local',
                     help='local certificate only, or the verified finite-sum/endpoint chain')
    run.add_argument('--max-steps', type=positive_int, default=1)
    for command in (core, probe, run):
        command.add_argument('--seconds', type=positive_float, default=30.0)
        command.add_argument('--output-root', default=str(GENERATED))
    resume = sub.add_parser('resume', help='recheck a v2 Train checkpoint, then continue within remaining budget')
    resume.add_argument('--run-dir', required=True)
    for command in (run, resume):
        command.add_argument('--pause-after', type=positive_int, default=None,
            help='save a checkpoint after this many additional actions; preserve unused budget')
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


def telescoping_dependencies():
    """Freeze the original meaning of the selected mathematical profile."""
    names = [
        'benchmark/lean/Benchmark/Definitions.lean',
        'benchmark/lean/Benchmark/Auxiliary.lean',
        'benchmark/lean/Benchmark/Gaussian.lean',
        'finite_product_framework/p1/lean/GaussianRules.lean',
        'benchmark/lean/lean-toolchain', 'benchmark/lean/lakefile.toml',
        'project/lake-manifest.json', 'project/lakefile.toml', 'project/lean-toolchain',
    ]
    paths = [REPOSITORY / name for name in names]
    paths += [REPOSITORY / 'finite_product_framework/solve_core.py']
    paths += sorted((REPOSITORY / 'finite_product_framework/p1').glob('*.py'))
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


def method_demo(args, store):
    from .method_registry import builtin_registry
    from .cas_adapter import adapter_result
    from .executor import normalize_result
    spec = builtin_registry().get(args.method)
    spec.validate_parameters({'seconds': args.seconds})
    path = guard_path(args.input)
    if path.stat().st_size > 1000000:
        raise ContractError('method request exceeds the input size limit')
    content = path.read_bytes()
    try:
        request = json.loads(content)
    except RecursionError as error:
        raise ContractError('method request exceeds the nesting limit') from error
    store.write_bytes('source/request.json', content)
    store.write_json('method_spec.json', spec.to_dict())
    initial = {'schema_version': 1, 'scope': 'non_formal_registered_method_probe',
               'method': spec.id, 'method_version': spec.version, 'formal_state': False,
               'input_sha256': hashlib.sha256(content).hexdigest(),
               'verified_certificates': [], 'formal_obligations': None,
               'original_identity_proved': False}
    store.write_json('initial_state.json', initial)
    store.write_json('rounds/1/state_before.json', initial)
    store.write_json('rounds/1/action.json', {'schema_version': 1, 'method': spec.id,
        'method_version': spec.version, 'seconds': args.seconds, 'formal_action': False})
    started = time.monotonic()
    adapter = None if spec.capability_level == 'L0' else spec.factory()()
    if adapter is None or not hasattr(adapter, 'execute_request'):
        raw = adapter_result(started, 'incomplete', 'capability_unavailable',
                             'This method has no standalone typed-request execution contract.')
    else:
        raw = adapter.execute_request(request, store.path('rounds/1/backend'), args.seconds)
    result = normalize_result(raw)
    if result.C_partial or result.O_res:
        raise ContractError('non-formal method probe cannot claim formal candidates or residuals')
    result = replace(result, raw_result=dict(result.raw_result, method_id=spec.id,
        method_version=spec.version,
        capability_level='L2' if adapter is not None and hasattr(adapter, 'execute_request') else 'L0',
        registered_method_capability_level=spec.capability_level))
    for artifact in result.artifacts:
        artifact_path = guard_path(artifact.path, store.path('rounds/1/backend'))
        if sha256_file(artifact_path) != artifact.sha256:
            raise IntegrityError('method probe artifact hash mismatch')
    if sha256_file(path) != initial['input_sha256']:
        raise IntegrityError('method probe input changed during execution')
    result = replace(result, cost=Cost(time.monotonic() - started, 1))
    store.write_json('rounds/1/result.json', result.to_dict())
    store.write_json('rounds/1/raw_result.json', result.raw_result)
    status = result.status if result.status in ('environment_blocked', 'budget_exhausted', 'integrity_error') else 'incomplete'
    final = dict(initial, status=status, symbolic_status=result.status, stop_reason=result.sigma.code,
                 actual_cost=result.cost.to_dict(), test_data_read=False)
    store.write_json('rounds/1/state_after.json', final)
    store.write_json('run.json', final)
    store.write_json('graph.json', {'schema_version': 1, 'scope': initial['scope'], 'formal_graph': None})
    return status


def train_run(args, store):
    from .graph import Graph, Outlet
    from .loop import run
    from .method_registry import builtin_registry, resolve
    spec = builtin_registry().get(args.method)
    spec.validate_parameters({'seconds': args.seconds, 'scope': args.scope})
    store.write_json('method_spec.json', spec.to_dict())
    source = load_train(args.identity, store, REPOSITORY)
    source = replace(source, dependencies=source.dependencies + runtime_dependencies())
    if spec.capability_level == 'L0':
        from .loop import finish
        state, representation = initial_state(source, Budget(args.seconds, args.max_steps))
        graph = Graph(source.sha256)
        graph.add_node(representation)
        store.write_json('initial_state.json', state.to_dict())
        return finish(store, replace(state, status='incomplete'), graph, 'capability_unavailable',
                      [spec.to_dict()]).status
    analyze_source = resolve(spec.frontend)
    frontend = analyze_source(source.to_dict(), run_root=store.root)
    if frontend['status'] == 'applicable':
        source = replace(source, proposition=frontend.get('original_proposition', source.proposition),
                         dependencies=source.dependencies + tuple(resolve(spec.dependency_provider)()))
        frontend = analyze_source(source.to_dict(), run_root=store.root)
    store.write_json('frontend.json', frontend)
    state, representation = initial_state(source, Budget(args.seconds, args.max_steps))
    graph = Graph(source.sha256)
    graph.add_node(representation)
    if frontend['status'] != 'applicable' and not source.declaration.lstrip().startswith('import Init\n'):
        from .loop import finish
        store.write_json('initial_state.json', state.to_dict())
        return finish(store, replace(state, status='incomplete'), graph,
                      'not_applicable', [frontend]).status
    if args.method == 'telescoping' and args.scope == 'full' and frontend['status'] == 'applicable':
        from .telescoping_closure import closure_blueprint
        plan = closure_blueprint(frontend)
        store.write_json('closure_contract.json', plan)
        for task in ('local', 'bridge', 'zero_endpoint', 'upper_endpoint'):
            handles = ('original',) if task in ('local', 'bridge') else (plan['obligation_ids'][task],)
            graph.add_outlet(Outlet('telescoping-' + task, representation.id, 'CAS', 'method',
                {'method': args.method, 'method_version': spec.version,
                 'seconds': args.seconds, 'scope': 'full', 'task': task,
                 'produces_certificate': plan['certificate_ids'][task]}, ('closed_prop',),
                estimated_seconds=spec.estimated_seconds,
                handles=handles,
                required_certificates=(plan['local_id'],) if task == 'bridge' else (),
                provenance=('new_v2_finite_sum_contract',)))
    elif args.method == 'recurrence' and args.scope == 'full' and frontend['status'] == 'applicable':
        from .method_tasks import full_scope_contract, initial_full_outlet
        try:
            contract = full_scope_contract(frontend)
        except IntegrityError:
            raise
        except ValueError as error:
            from .loop import finish
            store.write_json('initial_state.json', state.to_dict())
            return finish(store, replace(state, status='incomplete'), graph,
                          'not_applicable', [{'scope': 'full', 'message': str(error)}]).status
        store.write_json('closure_contract.json', contract)
        graph.add_outlet(initial_full_outlet(frontend, args.seconds, spec.version, spec.estimated_seconds))
    else:
        graph.add_outlet(Outlet(args.method, representation.id, 'CAS', 'method',
            {'method': args.method, 'method_version': spec.version, 'seconds': args.seconds}, spec.accepted_kinds,
            estimated_seconds=spec.estimated_seconds if frontend['status'] == 'applicable' else 0.01,
            provenance=('new_v2_method_contract',)))
    executor, checker = _production()
    options = {} if getattr(args, 'pause_after', None) is None else {'pause_after': args.pause_after}
    return run(state, graph, store, executor, checker, **options).status


def resume_run(args):
    from .loop import resume, run
    store = RunStore(_explicit_directory(args.run_dir))
    executor, checker = _production()
    saved = store.load_checkpoint()['state']['G']
    # A CLI checkpoint cannot remap a Train identity to a convenient synthetic
    # theorem even if a caller recomputes the checkpoint's content hashes.
    manifest = guard_path(REPOSITORY / 'benchmark/splits/train.jsonl')
    rows = [json.loads(line) for line in manifest.read_text().splitlines() if line.strip()]
    matches = [row for row in rows if row['id'] == saved['identity']]
    if len(matches) != 1 or saved['sha256'] != matches[0]['lean_sha256'] or \
            Path(saved['path']) != guard_path(REPOSITORY / 'benchmark' / matches[0]['lean_path']):
        raise IntegrityError('checkpoint not bound to the selected Train original')
    state, graph = resume(store, checker)
    options = {} if getattr(args, 'pause_after', None) is None else {'pause_after': args.pause_after}
    return run(state, graph, store, executor, checker, **options).status, store


def main(argv=None):
    args = parser().parse_args(argv)
    if args.command == 'methods':
        from .method_registry import builtin_registry
        print(json.dumps(builtin_registry().to_dict(), ensure_ascii=False))
        return 0
    store = None
    try:
        if args.command == 'resume':
            status, store = resume_run(args)
        else:
            if args.command in ('core-demo', 'method-demo'): guard_path(args.input)
            root = _explicit_directory(args.output_root)
            store = RunStore.create(root)
            handler = {'core-demo': core_demo, 'method-demo': method_demo, 'run': train_run}[args.command]
            status = handler(args, store)
    except ReplayFailure as error:
        status = error.status
        store = RunStore(error.run_dir)
        store.write_json('error.json', {'schema_version': 1, 'status': status,
            'code': error.code, 'message': str(error), 'original_identity_proved': False})
        print(json.dumps({'status': status, 'code': error.code, 'message': str(error)},
                         ensure_ascii=False), file=sys.stderr)
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
