"""One real recurrence construction and one unverified local candidate."""
from pathlib import Path
import time

from .models import Artifact, Source
from .storage import verify_source, sha256_file
from .process import prepare_attempt, validate_seconds, write_json
from .recurrence_frontend import analyze_source
from .recurrence_translation import translate_candidate


def dependencies(repository=None):
    repository = Path(repository or Path(__file__).resolve().parents[1])
    paths = ['benchmark/lean/Benchmark/' + name + '.lean' for name in ('Definitions', 'Auxiliary', 'Gaussian')]
    paths += ['finite_product_framework/p1/lean/' + name + '.lean' for name in ('GaussianRules', 'Shared')]
    paths += ['benchmark/lean/lean-toolchain', 'benchmark/lean/lakefile.toml',
              'project/lake-manifest.json', 'project/lakefile.toml', 'project/lean-toolchain',
              'finite_product_framework/solve_core.py']
    paths += ['finite_product_framework/p1/' + name + '.py' for name in (
        'core', 'qgosper', 'qparameterized', 'zeilberger', 'expressions', 'ore', 'ore_core', 'qjoint',
        'qrational_system', 'qholonomic', 'qdifference', 'qpisigma', 'qfinite', 'qpisigma_system',
        'qplde', 'qnumberfield', 'qconstant', 'qomega', 'lean_pipeline', 'zeilberger_pipeline')]
    return tuple(Artifact(str(repository / path), sha256_file(repository / path)) for path in paths)


class RecurrenceAdapter:
    def execute_action(self, state, action, attempt_dir, seconds):
        """Construct one declared full-scope task; approval stays in LeanChecker."""
        from .cas_adapter import adapter_result
        from .recurrence_closure import closure_blueprint, make_closure_candidate
        started = time.monotonic()
        if action.theta.get('method') != 'recurrence' or action.theta.get('scope') != 'full':
            raise ValueError('unregistered recurrence task contract')
        task = action.theta.get('task')
        validate_seconds(seconds)
        run_root = Path(state.G.snapshot_path).parent.parent
        verify_source(state.G, run_root)
        front = analyze_source(state.G.to_dict(), run_root)
        # Full scope must validate the actual RHS, not just the local summand.
        plan = closure_blueprint(front)
        if task == 'local':
            if any(c.id.startswith('recurrence-local-') for c in state.C):
                raise ValueError('local recurrence task already completed')
            remaining = seconds - (time.monotonic() - started)
            if remaining <= 0:
                return adapter_result(started,'budget_exhausted','timeout','Full-scope frontend exhausted budget.')
            outcome = self.execute(state.G.identity, 'recurrence', state.G.to_dict(), attempt_dir, remaining)
            outcome['raw_result']['execution_scope'] = 'certificate_chain'
            outcome['raw_result'].pop('remaining_work', None)
            return outcome
        if task not in plan['tasks']:
            raise ValueError('unknown recurrence closure task')
        approved = {c.id: c.to_dict() for c in state.C}
        candidate = make_closure_candidate(front, task, approved, action.id)
        if candidate.closes not in {o.id for o in state.O}:
            raise ValueError('task has no matching open formal obligation')
        attempt = prepare_attempt(attempt_dir)
        if any(attempt.iterdir()):
            raise ValueError('recurrence attempt directory must be empty')
        write_json(attempt/'method_request.json', {'method':'recurrence','version':'2.0','task':task,
            'source':state.G.to_dict(),'seconds':seconds,'action_id':action.id,
            'approved_certificates':list(approved),'open_obligations':[o.to_dict() for o in state.O]}, attempt)
        write_json(attempt/'frontend.json', front, attempt)
        write_json(attempt/'task_contract.json', closure_blueprint(front,approved), attempt)
        write_json(attempt/'candidate.json', candidate.to_dict(), attempt)
        verify_source(state.G, run_root)
        if time.monotonic() - started >= seconds:
            return adapter_result(started,'budget_exhausted','timeout',
                'Closure reconstruction exhausted action budget.',attempt=attempt)
        outcome = adapter_result(started,'symbolic_constructed','closure_candidate_ready',
            'One recurrence closure candidate awaits independent Lean verification.',stage='translation',
            raw_result={'execution_scope':'certificate_chain','method':'recurrence','task':task,
                        'cas_invoked':False,'frontend_profile':front['profile'],
                        'dependency_ids':list(candidate.dependencies)},attempt=attempt)
        outcome['C_partial'] = [candidate.to_dict()]
        outcome['O_res'] = [o.to_dict() for o in candidate.replaces]
        return outcome

    def execute(self, identity, method, source, attempt_dir, seconds):
        from .cas_adapter import CoreAdapter, adapter_result
        started = time.monotonic(); attempt = None
        try:
            validate_seconds(seconds); attempt = prepare_attempt(attempt_dir)
            if any(attempt.iterdir()): raise ValueError('recurrence attempt directory must be empty')
            bound = Source.from_dict(source)
            if identity != bound.identity or method != 'recurrence':
                raise ValueError('recurrence method/source identity mismatch')
            run_root = Path(bound.snapshot_path).parent.parent
            verify_source(bound, run_root)
            write_json(attempt / 'method_request.json', {'method': method, 'version': '2.0',
                'identity': identity, 'source': source, 'seconds': seconds}, attempt)
            front = analyze_source(source, run_root)
            write_json(attempt / 'frontend.json', front, attempt)
            if front['status'] != 'applicable':
                return adapter_result(started, 'incomplete', 'not_applicable',
                    'Original outside the alternating Gaussian recurrence profile.',
                    raw_result={'frontend': front}, attempt=attempt)
            write_json(attempt / 'mapping.json', front['mapping'], attempt)
            write_json(attempt / 'cas_request.json', front['core_request'], attempt)
            remaining = seconds - (time.monotonic()-started)
            if remaining <= 0:
                return adapter_result(started, 'budget_exhausted', 'timeout', 'Frontend exhausted budget.', attempt=attempt)
            core = CoreAdapter().execute(front['core_request'], attempt / 'core', remaining)
            write_json(attempt / 'cas_return.json', core, attempt)
            verify_source(bound, run_root)
            raw = {'frontend_profile': front['profile'], 'core': core['raw_result'],
                   'execution_scope': 'local_certificate_only'}
            if core['status'] != 'symbolic_constructed':
                return adapter_result(started, core['status'], core['sigma']['code'],
                    core['sigma']['message'], stage=core['sigma']['stage'], raw_result=raw,
                    diagnostics=core.get('diagnostics', []), attempt=attempt)
            translation = translate_candidate(front, core['raw_result'])
            write_json(attempt / 'translation.json', translation, attempt)
            raw['translation'] = translation
            raw['remaining_work'] = {'formal_obligations_exported': False, 'open_obligation': 'original',
                'explanation': ['原题目标的相同递推、两个初值及唯一性连接尚未验证；局部递推不关闭原题。']}
            if translation['status'] != 'candidate_ready':
                return adapter_result(started, 'symbolic_constructed', 'translation_pending',
                    'Real recurrence certificate has no supported local Lean translation.',
                    stage='translation', raw_result=raw, attempt=attempt)
            write_json(attempt / 'candidate.json', translation['candidate'], attempt)
            verify_source(bound, run_root)
            outcome = adapter_result(started, 'symbolic_constructed', 'local_candidate_ready',
                'Source-bound finite-sum recurrence awaits independent Lean verification.',
                stage='translation', backend_status='constructed', raw_result=raw, attempt=attempt)
            outcome['C_partial'] = [translation['candidate']]
            return outcome
        except (OSError, ValueError, TypeError) as error:
            return adapter_result(started, 'integrity_error', 'artifact_integrity', str(error))
