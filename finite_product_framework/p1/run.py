#!/usr/bin/env python3
"""P1 entry: no identity-specific proof adapters or fallback to archived proofs."""
import argparse
from dataclasses import asdict
import hashlib
import json
import multiprocessing as mp
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]

ACTIVE_BRANCHES = frozenset(('target_first_order', 'direct_q_gosper',
    'general_q_zeilberger', 'bibasic_gosper', 'ore_closure', 'multisum'))


def load_target(identity, *, current_train=False):
    train = {r['id']: r for r in map(json.loads,
             (ROOT/'benchmark/splits/train.jsonl').read_text().splitlines())}
    if identity not in train or (not current_train and train[identity]['family_id'] != 'A'):
        raise ValueError('unsupported_input: requires an A-family train identity')
    row = train[identity]
    path = ROOT/'benchmark'/row['lean_path']
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if digest != row['lean_sha256']:
        raise ValueError('source_changed')
    return {'identity_id': identity, 'path': str(path.relative_to(ROOT)), 'sha256': digest}


def construct_in_process(problem, budget, branch):
    if branch not in ACTIVE_BRANCHES:
        raise ValueError("unsupported_input: inactive or unknown branch")
    if problem.get('mode') in ('general_recurrence','general_telescoping'):
        expected = 'general_q_zeilberger' if problem['mode']=='general_recurrence' else 'direct_q_gosper'
        if branch != expected:
            raise ValueError('invalid_problem: general summation mode does not match method')
        from general_summation import construct as general_construct
        return general_construct(problem,budget)
    if branch == 'multisum':
        from multisum import construct as multisum_construct
        return multisum_construct(problem,budget)
    if branch == 'ore_closure':
        from ore_pipeline import construct as ore_construct
        return ore_construct(problem,budget)
    if branch == 'bibasic_gosper':
        from bibasic import construct as bibasic_construct
        return bibasic_construct(problem,budget)
    if branch == 'general_q_zeilberger':
        from zeilberger import construct as zeilberger_construct
        return zeilberger_construct(problem, budget)
    if branch == 'direct_q_gosper':
        from direct import construct as direct_construct
        return direct_construct(problem,budget)
    if 'conjuncts' in problem:
        if (set(problem) != {'schema_version','source_id','conjuncts'} or
                problem['schema_version'] != 1 or len(problem['conjuncts']) != 2):
            raise ValueError('invalid_problem: binary conjunction required')
        results = [construct_in_process(p,budget,branch) for p in problem['conjuncts']]
        status = next((r['construction']['status'] for r in results
                       if r['construction']['status'] != 'constructed'), 'constructed')
        return {'conjunct_results':results,'construction':{'status':status}}
    from expressions import derive, X, q
    from search import search
    shifts = derive(problem)
    construction = search(shifts['n_shift'], shifts['k_shift'],
                          shifts['target_coefficient'], X, q, budget)
    return {'shifts': {k: str(v) for k, v in shifts.items()}, 'construction': construction}


def worker(problem, budget, connection, branch):
    try:
        connection.send(construct_in_process(problem,budget,branch))
    except Exception as exc:
        connection.send({'error': f'{type(exc).__name__}: {exc}'})
    finally:
        connection.close()


def construct(problem, budget, branch='target_first_order'):
    # Hard process timeout also covers individual symbolic solver calls.
    context = mp.get_context('spawn')
    parent, child = context.Pipe(duplex=False)
    process = context.Process(target=worker, args=(problem, budget, child, branch))
    process.start()
    child.close()
    try:
        if not parent.poll(budget.seconds+5):
            process.terminate()
            return {'error': 'timeout: symbolic worker exceeded wall-clock budget'}
        try:
            return parent.recv()
        except EOFError:
            return {'error': 'backend_failed: symbolic worker exited without result'}
    finally:
        process.join(timeout=1)
        if process.is_alive():
            process.terminate()
            process.join()
        parent.close()


def prepare_batch(work):
    """Compile shared source dependencies once; every batch task checks the snapshot."""
    from lean_pipeline import environment
    env, dependencies = environment(work)
    artifacts = [{'path':str(path), 'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
                 for path in sorted((work/'deps').rglob('*.olean'))]
    return {'env':env, 'dependencies':dependencies, 'artifacts':artifacts}


def batch_environment(prepared):
    for entry in prepared['dependencies']:
        if hashlib.sha256((ROOT/entry['path']).read_bytes()).hexdigest() != entry['sha256']:
            raise ValueError('dependency_compile_failed: batch source snapshot changed')
    for entry in prepared['artifacts']:
        if hashlib.sha256(Path(entry['path']).read_bytes()).hexdigest() != entry['sha256']:
            raise ValueError('dependency_compile_failed: batch compiled snapshot changed')
    return dict(prepared['env']), list(prepared['dependencies'])


def run(identity=None, problem=None, budget=None, *, prepared=None, output_root=None, branch=None, source_context=None):
    from search import Budget
    budget = budget or Budget()
    report = {'schema_version': 2, 'status': 'started',
              'automatic_train_proofs': 0, 'complete_train_proofs': 0,
              'test_files_read': 0, 'preset_proof_fallback': False,
              'budget': asdict(budget), 'lean_proof_generated': False,
              'stages': []}
    try:
        if branch is not None and branch not in ACTIVE_BRANCHES:
            raise ValueError('unsupported_input: inactive or unknown branch')
        source_id = identity if problem is None else problem['source_id']
        if source_context is not None:
            from workflow.contracts import check_source
            if not source_context.get('preprocessing') or source_context['identity']!=source_id:
                raise ValueError('unverified source override')
            check_source(source_context)
        report['source'] = load_target(source_id,current_train=source_context is not None)
        if problem is None:
            from lean_pipeline import environment, extract, frontend, synthesize
            from expressions import derive
            work = (Path(output_root)/source_id if output_root is not None else
                    HERE/'generated'/('automatic' if identity is None else 'runs/'+source_id))
            work.mkdir(parents=True, exist_ok=True)
            source_path = ROOT/report['source']['path']
            source = source_path.read_text()
            env, dependencies = environment(work) if prepared is None else batch_environment(prepared)
            report['dependencies'] = dependencies
            report['stages'].append('source_dependencies_recompiled' if prepared is None else
                                    'source_dependencies_verified_from_batch_snapshot')
            raw = extract(source, work, env)
            report['stages'].append('lean_goal_elaborated_and_exported')
            if branch == 'target_first_order':
                formula, model = frontend(raw, source_id)
            elif branch == 'direct_q_gosper':
                from general_summation import telescoping_frontend as direct_frontend
                formula, model = direct_frontend(raw, source_id)
            elif branch == 'multisum':
                from multisum_pipeline import frontend as multisum_frontend
                formula,model=multisum_frontend(raw,source_id)
            elif branch == 'ore_closure':
                from ore_pipeline import prepare as ore_prepare
                formula,model=ore_prepare(raw,source_id,work,env)
            elif branch == 'bibasic_gosper':
                from bibasic_pipeline import frontend as bibasic_frontend
                formula, model = bibasic_frontend(raw, source_id)
            elif branch == 'general_q_zeilberger':
                from general_summation import recurrence_frontend as zeil_frontend
                formula, model = zeil_frontend(raw, source_id)
            else:
                from general_summation import telescoping_frontend as direct_frontend
                try:
                    formula, model = frontend(raw, source_id)
                    branch = 'target_first_order'
                except ValueError as first_error:
                    try:
                        formula, model = direct_frontend(raw, source_id)
                        branch = 'direct_q_gosper'
                    except ValueError as second_error:
                        from general_summation import recurrence_frontend as zeil_frontend
                        try:
                            formula, model = zeil_frontend(raw, source_id)
                            branch = 'general_q_zeilberger'
                        except ValueError as third_error:
                            from bibasic_pipeline import frontend as bibasic_frontend
                            try:
                                formula,model=bibasic_frontend(raw,source_id)
                                branch='bibasic_gosper'
                            except ValueError as fourth_error:
                                from ore_pipeline import prepare as ore_prepare
                                try:
                                    formula,model=ore_prepare(raw,source_id,work,env)
                                    branch='ore_closure'
                                except ValueError as fifth_error:
                                    from multisum_pipeline import frontend as multisum_frontend
                                    try:
                                        formula,model=multisum_frontend(raw,source_id)
                                        branch='multisum'
                                    except ValueError as sixth_error:
                                        raise ValueError(f'unsupported_structure: first-order: {first_error}; direct: {second_error}; Zeilberger: {third_error}; bibasic: {fourth_error}; Ore: {fifth_error}; multisum: {sixth_error}')
            report['branch'] = branch
            report['input_formula'] = formula
            if branch == 'multisum':
                report['support'] = {k:model[k] for k in ('dimension','domain','bounds')}
                report['lean_expression_sha256'] = hashlib.sha256((work/'lean_expression.json').read_bytes()).hexdigest()
            report['representation_status'] = 'extracted_from_Lean_Expr; final proof checks original target'
            result = construct(formula, budget, branch)
            report.update(result)
            if 'error' in result:
                report['status'] = ('timeout' if branch == 'multisum' and
                    result['error'].startswith('timeout:') else 'construction_failed')
            elif result['construction']['status'] != 'constructed':
                report['status'] = result['construction']['status']
            else:
                report['stages'].append('multivariate_local_relation_constructed' if branch == 'multisum' else 'ore_closure_and_elimination_constructed' if branch == 'ore_closure' else 'joint_recurrence_and_certificate_constructed'
                    if branch == 'general_q_zeilberger' else ('bibasic_gosper_certificate_constructed'
                    if branch == 'bibasic_gosper' else 'q_gosper_certificate_constructed'))
                if branch == 'multisum':
                    from multisum_pipeline import synthesize as multisum_synthesize
                    verification=multisum_synthesize(source,model,result['construction'],work,env)
                elif branch == 'ore_closure':
                    from ore_pipeline import synthesize as ore_synthesize
                    verification=ore_synthesize(source,model,result['construction'],work,env)
                elif branch == 'bibasic_gosper':
                    from bibasic_pipeline import synthesize as bibasic_synthesize
                    verification=bibasic_synthesize(source,model,result['construction'],work,env)
                elif branch == 'general_q_zeilberger':
                    from zeilberger_pipeline import synthesize as zeil_synthesize
                    verification = zeil_synthesize(source,model,result['construction'],work,env)
                elif branch == 'direct_q_gosper':
                    from direct import synthesize as direct_synthesize
                    verification = direct_synthesize(source,model,result['construction'],work,env)
                else:
                    if 'conjuncts' in model:
                        from lean_pipeline import synthesize_conjunction
                        verification = synthesize_conjunction(source,model,result,work,env)
                    else:
                        verification = synthesize(source, model, derive(formula), result['construction'], work, env)
                report['verification'] = verification
                report['status'] = verification['status']
                report['lean_proof_generated'] = verification.get('lean_proof_generated',True)
                if verification['status'] == 'proved':
                    if hashlib.sha256(source_path.read_bytes()).hexdigest() != report['source']['sha256']:
                        raise ValueError('source_changed_during_run')
                    if prepared is not None:
                        batch_environment(prepared)
                    report['automatic_train_proofs'] = report['complete_train_proofs'] = 1
                    report['stages'] += ['original_target_equivalence_verified',
                        ('local_and_endpoints_verified' if branch in ('direct_q_gosper','bibasic_gosper') else
                         'local_boundary_initial_target_verified'), 'kernel_and_axiom_audit_passed']
        else:
            report['input_formula'] = problem
            report['representation_status'] = 'unverified_formula_transcription'
            result = construct(problem, budget, branch or 'target_first_order')
            report.update(result)
            if 'error' in result:
                report['status'] = 'construction_failed'
            else:
                status = result['construction']['status']
                report['status'] = 'constructed_not_proved' if status == 'constructed' else status
        if report['status'] == 'proved':
            report['remaining_obligations'] = []
        elif problem is not None:
            report['remaining_obligations'] = ['Connect symbolic transcription to original Lean target',
                'Verify local relation, boundary and target in original parameter domain']
        elif report.get('branch') == 'multisum':
            report['remaining_obligations'] = report.get('verification',{}).get('remaining_obligations',[
                'Construct a multivariate relation within the explicit search budget',
                'Lift certificates to original products; verify finite-domain faces and moving shells',
                'Verify target recurrence, initial values and original Lean declaration'])
        elif report.get('branch') in ('direct_q_gosper','bibasic_gosper'):
            report['remaining_obligations'] = ['Verify computed antidifference and both endpoints in Lean',
                                               'Compile and audit the original target']
        else:
            report['remaining_obligations'] = ['Verify local relation, boundary, initial and target recurrence in Lean',
                                               'Compile and audit the original target']
    except Exception as exc:
        category = str(exc).split(':',1)[0]
        if category not in ('representation_gap','unsupported_structure','unsupported_expression',
                             'unsupported_declaration','domain_unresolved','dependency_compile_failed'):
            category = 'pipeline_incomplete'
        report.update(status=category, error=f'{type(exc).__name__}: {exc}',
                      automatic_train_proofs=0, complete_train_proofs=0,
                      remaining_obligations=['Resolve '+category+' before continuing proof generation'])
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    inputs = parser.add_mutually_exclusive_group(required=True)
    inputs.add_argument('--identity')
    inputs.add_argument('--problem', type=Path)
    parser.add_argument('--seconds', type=float, default=30)
    parser.add_argument('--branch', choices=['general_q_zeilberger','bibasic_gosper','ore_closure','multisum'])
    parser.add_argument('--max-order', type=int, default=4)
    parser.add_argument('--max-degree', type=int, default=2,
                        help='multisum certificate numerator total degree bound')
    parser.add_argument('--laurent-floor', type=int, default=0,
                        help='multisum minimum Laurent exponent in each direction')
    parser.add_argument('--output-root', type=Path, help='separate native proof artifacts by backend')
    args = parser.parse_args()
    from search import Budget
    if not 0 < args.seconds <= 600:
        parser.error('--seconds must be between 0 and 600')
    problem = json.loads(args.problem.read_text()) if args.problem else None
    from zeilberger import ZeilbergerBudget
    if not 1 <= args.max_order <= 16:
        parser.error('--max-order must be between 1 and 16')
    from multisum import MultisumBudget
    budget_type = MultisumBudget if args.branch == 'multisum' else ZeilbergerBudget
    if not 0 <= args.max_degree <= 12:
        parser.error('--max-degree must be between 0 and 12')
    if not -8 <= args.laurent_floor <= 0:
        parser.error('--laurent-floor must be between -8 and 0')
    options={'max_degree':args.max_degree,'laurent_floor':args.laurent_floor} if args.branch == 'multisum' else {}
    report = run(args.identity, problem, budget_type(seconds=args.seconds,max_order=args.max_order,**options), branch=args.branch,output_root=args.output_root)
    out = HERE/'generated'/('symbolic_run.json' if problem is not None else 'run.json')
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    if problem is None and 'source' in report:
        saved = (args.output_root if args.output_root is not None else HERE/'generated/runs')/report['source']['identity_id']/'report.json'
        saved.parent.mkdir(parents=True,exist_ok=True)
        saved.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({key:value for key,value in report.items()
                      if key not in ('input_formula','construction','verification','conjunct_results')}, ensure_ascii=False, indent=2))
    # Structured formula mode remains symbolic only; native mode must pass Lean.
    sys.exit(0 if report['status'] in ('proved','constructed_not_proved') else 2)
