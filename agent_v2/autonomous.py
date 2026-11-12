"""Budgeted CAS/model residual loop with atomic autonomous checkpoints."""
from dataclasses import replace
import time

from .autonomous_adapter import AutonomousExecutor, outcome
from .executor import validate_invariant, verify_and_update
from .graph import Outlet
from .graph_builder import sync_residual_graph
from .loop import _final, checkpoint, finish
from .models import Attempt, ContractError, Cost, digest
from .recovery import classify_stop
from .router import JevRouter, RuleBasedRouter
from .storage import IntegrityError, RunStore, verify_source


def default_config():
    return {'action_seconds': 180.0, 'max_model_calls': 8, 'max_expansions': 3,
            'max_repairs': 2, 'selector': 'rule', 'model': {}, 'jev': {}}


class AutonomousRuntime:
    def __init__(self, config, capabilities, model, checker, library_records, jev=None):
        self.config, self.capabilities = dict(config), dict(capabilities)
        if set(self.config) != set(default_config()):
            raise ContractError('invalid autonomous configuration fields')
        for key in ('max_model_calls', 'max_expansions', 'max_repairs'):
            if type(config[key]) is not int or config[key] < (1 if key == 'max_model_calls' else 0):
                raise ContractError('invalid autonomous count limit')
        import math
        if (type(config['action_seconds']) not in (int, float) or
                not math.isfinite(config['action_seconds']) or not 0 < config['action_seconds'] <= 86400):
            raise ContractError('invalid autonomous action timeout')
        if config['selector'] not in ('rule', 'jev'):
            raise ContractError('invalid autonomous selector')
        self.model, self.checker, self.jev = model, checker, jev
        self.library = list(library_records)
        self.executor = AutonomousExecutor(model, checker, capabilities, library=self.library)
        self.expansions, self.repairs = 0, 0
        self.completed_methods = {}
        self.reserved_model_calls, self.reserved_jev_calls = 0, 0
        if config['selector'] == 'jev' and jev is None:
            raise ContractError('Jev selection requires an explicit client')
        self.router = JevRouter(jev) if jev else RuleBasedRouter()

    def snapshot(self):
        return {'schema_version': 1, 'config': self.config, 'capabilities': self.capabilities,
                'tasks': [t.to_dict() for t in self.checker.tasks.values()],
                'model_calls': max(self.model.calls_used, self.reserved_model_calls),
                'jev_calls': max(self.jev.calls_used if self.jev else 0, self.reserved_jev_calls),
                'library': self.library, 'feedback': self.executor.feedback,
                'expansions': self.expansions, 'repairs': self.repairs,
                'completed_methods': self.completed_methods}


class AutonomousStore(RunStore):
    """Keep state, graph, task registry and reserved calls in ONE atomic record.

    The legacy resume verifier sees its original exact schema. Its every
    checkpoint and finalization still uses this wrapper and retains metadata.
    """
    def __init__(self, root, runtime):
        super().__init__(root)
        self.runtime = runtime

    def save_checkpoint(self, data):
        if 'autonomous' in data:
            raise IntegrityError('autonomous metadata must come from the active runtime')
        return super().save_checkpoint(dict(data, autonomous=self.runtime.snapshot()))

    def load_checkpoint(self):
        data = super().load_checkpoint()
        if 'autonomous' not in data:
            raise IntegrityError('autonomous checkpoint metadata missing')
        saved = data.pop('autonomous')
        if digest(saved) != digest(self.runtime.snapshot()):
            raise IntegrityError('active autonomous runtime differs from its checkpoint')
        return data

    def write_json(self, relative, value):
        if relative == 'run.json':
            value = dict(value, autonomous=True,
                model_calls=max(self.runtime.model.calls_used,self.runtime.reserved_model_calls),
                jev_calls=max(self.runtime.jev.calls_used if self.runtime.jev else 0,
                              self.runtime.reserved_jev_calls),
                expansions=self.runtime.expansions, repairs=self.runtime.repairs,
                selector=self.runtime.config['selector'])
        return super().write_json(relative,value)


def _legal(state, graph, runtime):
    legal, reasons = graph.legal_candidates(state, llm_enabled=True)
    retained = []
    approved = {c.id for c in state.C}
    for action in legal:
        if action.M == 'LLM' and runtime.model.calls_used >= runtime.config['max_model_calls']:
            reasons.append({'route_id': action.id, 'code': 'model_call_limit'})
        elif action.M == 'CAS' and runtime.completed_methods.get(action.theta.get('method')) and all(
                c in approved for c in runtime.completed_methods[action.theta['method']]):
            reasons.append({'route_id': action.id, 'code': 'task_already_completed'})
        else:
            retained.append(action)
    return retained, reasons


def _add_followup(state, graph, runtime):
    if runtime.model.calls_used >= runtime.config['max_model_calls'] or not state.O:
        return False
    last = runtime.executor.feedback[-1] if runtime.executor.feedback else {}
    repair = last.get('model_attempt') and runtime.repairs < runtime.config['max_repairs']
    if not repair and runtime.expansions >= runtime.config['max_expansions']:
        return False
    if repair:
        runtime.repairs += 1
        purpose, number = 'repair', runtime.repairs
    else:
        runtime.expansions += 1
        purpose, number = 'expansion', runtime.expansions
    # Every new route is still from r, via a checked decomposition/focus edge.
    # Do not rewrite the graph or pretend that a different node is identity.
    goal = next((o for o in state.O if o.id == state.r), state.O[0])
    graph.add_outlet(Outlet(f'llm-{purpose}-{number}-{state.round_index}', goal.id, 'LLM', 'llm',
        {'autonomous': True, 'goal_id': goal.id, 'seconds': runtime.config['action_seconds'],
         'purpose': purpose, 'feedback_round': state.round_index}, ('closed_prop',),
        estimated_seconds=0.01, handles=(goal.id,), provenance=('bounded_model_followup',)))
    return True


def _feedback(result, diagnostics, action):
    # Model diagnostics are observations, never instructions or evidence. No
    # historical solutions are retrieved; only this action's own response/log.
    lean_messages = []
    for item in diagnostics:
        checked = item.get('check', {})
        lean_messages.append({'id': item.get('id'), 'code': item.get('code'),
                              'status': checked.get('status'), 'sigma': checked.get('sigma')})
        for artifact in checked.get('evidence', {}).get('artifacts', ()):
            from pathlib import Path
            path = Path(artifact.get('path', ''))
            if path.name in ('stdout.jsonl', 'stdout.txt', 'stderr.txt', 'Candidate.stdout', 'Candidate.stderr'):
                if path.is_file() and path.stat().st_size <= 200000:
                    lean_messages.append({'lean_output': path.read_text(errors='replace')[-12000:]})
        # Some checker rejection reports put diagnostic text outside evidence.
        for key in ('diagnostics', 'stdout', 'stderr'):
            if key in checked:
                lean_messages.append({key: str(checked[key])[-12000:]})
    return {'action': action.to_dict(), 'model_attempt': action.M == 'LLM',
            'code': result.sigma.code, 'proposal': result.raw_result.get('content'),
            'lean': lean_messages, 'adapter_diagnostics': list(result.diagnostics)}


def run(state, graph, store, *, pause_after=None):
    runtime = store.runtime
    deadline = time.monotonic()+state.b.seconds
    def remaining():
        return max(0.0,deadline-time.monotonic())
    if pause_after is not None and (type(pause_after) is not int or pause_after <= 0):
        raise ContractError('pause_after must be positive')
    stop_round = state.round_index + pause_after if pause_after else None
    if not store.path('initial_state.json').exists():
        store.write_json('initial_state.json', state.to_dict())
    state = replace(state, status='running')
    while True:
        started = time.monotonic()
        verify_source(state.G, store.root)
        validate_invariant(state)
        # One absolute deadline includes setup, selection, persistence, proof
        # checking and the next round's pre-final integrity checks.
        state=replace(state,b=replace(state.b,seconds=remaining()))
        if state.b.seconds <= 0:
            return finish(store, replace(state, status='budget_exhausted'), graph, 'wall_budget_exhausted')
        if stop_round is not None and state.round_index >= stop_round:
            return finish(store, replace(state, status='incomplete'), graph, 'checkpoint_paused')
        if not state.O:
            return _final(state, graph, store, runtime.checker)
        if state.b.actions <= 0:
            return finish(store, replace(state, status='budget_exhausted'), graph, 'action_budget_exhausted')
        sync_residual_graph(state, graph, runtime.capabilities, seconds=runtime.config['action_seconds'])
        legal, reasons = _legal(state, graph, runtime)
        if not legal and _add_followup(state, graph, runtime):
            legal, reasons = _legal(state, graph, runtime)
        if not legal:
            status, reason = classify_stop(state, legal, reasons)
            if runtime.model.calls_used >= runtime.config['max_model_calls']:
                status, reason = 'budget_exhausted', 'model_call_limit'
            state = replace(state, b=replace(state.b,seconds=remaining()), status=status)
            return finish(store, state, graph, reason, reasons)
        before, n = state, state.round_index+1
        round_path = f'rounds/{n}'
        attempt_dir = store.path(round_path)
        if attempt_dir.exists():
            raise IntegrityError('autonomous round evidence already exists')
        attempt_dir.mkdir(parents=True)
        store.write_json(round_path+'/state_before.json', state.to_dict())
        store.write_json(round_path+'/candidates.json', {'schema_version':1,
            'legal':[a.to_dict() for a in legal], 'filtered':reasons})
        reserved = min(before.b.seconds, runtime.config['action_seconds'] + (30 if runtime.jev else 0))
        # Reserve calls BEFORE network I/O. Interrupted calls consume their cap
        # on resume even if the HTTP worker never returned its usage record.
        if runtime.jev and len(legal) > 1:
            runtime.reserved_jev_calls = runtime.jev.calls_used + 1
            interrupted = replace(before, round_index=n, b=before.b.charge(reserved,1),
                attempts=before.attempts+(Attempt(digest({'selection':n}), f'selection-{n}',
                                                'interrupted_selection', n),))
            checkpoint(store, interrupted, graph, inflight=True)
            selection_seconds = remaining()
            if selection_seconds <= 0:
                runtime.reserved_jev_calls = 0
                return finish(store,replace(interrupted,b=replace(interrupted.b,seconds=0),
                              status='budget_exhausted'),graph,
                              'wall_budget_exhausted')
            runtime.jev.seconds = min(30, selection_seconds)
            action = runtime.router.choose(state, legal)
            runtime.reserved_jev_calls = 0
        else:
            action = RuleBasedRouter().choose(state, legal)
        if action is None or action not in legal:
            raise ContractError('selector returned an unregistered action')
        from .models import action_fingerprint
        fingerprint = action_fingerprint(before, action)
        store.write_json(round_path+'/action.json', action.to_dict())
        store.write_json(round_path+'/selection.json', {'schema_version':1,
            'selector':runtime.config['selector'], 'selected':action.id,
            'jev_result': runtime.jev.last_result if runtime.jev and len(legal)>1 else None,
            'fallback': getattr(runtime.router, 'last_diagnostic', None),
            'single_legal_action':len(legal)==1})
        if action.M == 'LLM': runtime.reserved_model_calls = runtime.model.calls_used+1
        interrupted = replace(before, round_index=n, b=before.b.charge(reserved,1),
            attempts=before.attempts+(Attempt(fingerprint, action.id, 'interrupted_inflight', n),))
        checkpoint(store, interrupted, graph, inflight=True)
        try:
            execution_seconds = remaining()
            if execution_seconds <= 0:
                runtime.reserved_model_calls = 0
                return finish(store,replace(before,round_index=n,
                    b=replace(before.b,seconds=0),status='budget_exhausted'),
                    graph,'wall_budget_exhausted')
            execution_state = replace(before, b=replace(before.b, seconds=execution_seconds))
            result = runtime.executor.execute(execution_state, action, graph, attempt_dir)
            runtime.reserved_model_calls = 0
            verification_seconds = max(0.0,min(remaining(),reserved-(time.monotonic()-started)))
            updated, diagnostics = verify_and_update(before, action, result, runtime.checker,
                {'source_sha256': before.G.sha256, 'run_dir':str(store.root),
                 'attempt_dir':str(attempt_dir), 'seconds':verification_seconds})
        except Exception as error:
            status = 'integrity_error' if isinstance(error,(IntegrityError,ContractError)) else 'environment_blocked'
            result = outcome(started, status, 'autonomous_execution_exception',
                             diagnostics=({'type':type(error).__name__, 'message':str(error)},))
            updated, diagnostics = before, list(result.diagnostics)
        elapsed = time.monotonic()-started
        result = replace(result, cost=Cost(elapsed,1))
        progress = len(updated.C)>len(before.C) or updated.O != before.O
        code = 'verified_progress' if progress else result.sigma.code
        if not progress:
            graph.mark_failure(action, code)
        elif action.M == 'CAS':
            runtime.completed_methods[action.theta['method']] = [c.id for c in updated.C if c not in before.C]
        runtime.executor.feedback = (runtime.executor.feedback+[_feedback(result,diagnostics,action)])[-3:]
        state = replace(updated, round_index=n,
            b=replace(before.b,seconds=remaining(),actions=max(0,before.b.actions-1)),
            attempts=before.attempts+(Attempt(fingerprint,action.id,code,n),))
        store.write_json(round_path+'/raw_result.json', result.raw_result)
        store.write_json(round_path+'/result.json', result.to_dict())
        store.write_json(round_path+'/verification.json', {'schema_version':1, 'checks':diagnostics,
            'certificates_added':len(state.C)-len(before.C), 'open_obligations':[o.id for o in state.O],
            'original_identity_proved':False})
        store.write_json(round_path+'/state_after.json', state.to_dict())
        checkpoint(store,state,graph)
        # Ordinary Lean failure is feedback for a bounded repair/expansion.
        # Corruption and process/environment failures are explicit stop states.
        fatal = result.status if result.status in ('integrity_error','environment_blocked','budget_exhausted') else None
        for diagnostic in diagnostics:
            check = diagnostic.get('check', {})
            if check.get('status') in ('integrity_error','environment_blocked','budget_exhausted'):
                fatal = check['status']
            if diagnostic.get('code') == 'partial_checker_exception': fatal = 'environment_blocked'
        if fatal:
            return finish(store,replace(state,status=fatal),graph,code,diagnostics)
