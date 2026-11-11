"""Residual-driven, one-action-at-a-time control with crash-safe checkpoints."""
from dataclasses import replace
from pathlib import Path
import time

from .executor import (_candidate_request, assemble_term, validate_invariant,
                       verify_and_update)
from .models import (Attempt, Candidate, ContractError, Cost, ExecutionResult,
                     FailureSignature, ResidualState, action_fingerprint, canonical)
from .storage import IntegrityError, guard_path, sha256_file, verify_source
from .recovery import classify_stop


def checkpoint(store, state, graph, inflight=False):
    store.write_json('graph.json', graph.to_dict())
    store.save_checkpoint({'schema_version': 1, 'state': state.to_dict(),
                           'graph': graph.to_dict(), 'inflight': inflight})


def finish(store, state, graph, reason, diagnostics=()):
    checkpoint(store, state, graph)
    store.write_json('run.json', {'schema_version': 1, 'status': state.status,
        'stop_reason': reason, 'identity': state.G.identity, 'source_sha256': state.G.sha256,
        'original_identity_proved': state.status == 'original_theorem_proved',
        'rounds': state.round_index, 'verified_certificates': len(state.C),
        'open_obligations': [o.id for o in state.O], 'remaining_budget': state.b.to_dict(),
        'diagnostics': list(diagnostics), 'benchmark_split': 'Train_or_synthetic',
        'test_data_read': False})
    return state


def _final(state, graph, store, checker):
    started = time.monotonic()
    report = {'proof_term': assemble_term(state), 'theorem': state.G.theorem,
              'proposition': state.G.proposition, 'seconds': state.b.seconds,
              'run_dir': str(store.root)}
    final_dir = store.path('final/attempt-' + str(state.round_index))
    final_dir.mkdir(parents=True, exist_ok=True)
    store.write_json(str(final_dir.relative_to(store.root) / 'request.json'), report)
    checked = None
    def rejected(status, code, message):
        previous = checked
        try:
            canonical(previous)
        except (TypeError, ValueError, RecursionError):
            previous = {'discarded_non_json_result': True, 'python_type': type(previous).__name__}
        return {'schema_version': 1, 'accepted': False, 'status': status,
                'evidence': {}, 'sigma': {'stage': 'original', 'code': code, 'message': message},
                'checker_result': previous}
    try:
        checked = checker.accept_original(report, state.G.to_dict(), final_dir)
        try:
            canonical(checked)
        except (TypeError, ValueError, RecursionError) as error:
            raise ContractError('original checker result is not finite serializable JSON') from error
        if (not isinstance(checked, dict) or type(checked.get('accepted')) is not bool or
                checked.get('status') not in {'original_theorem_proved', 'incomplete',
                    'integrity_error', 'environment_blocked', 'budget_exhausted'} or
                not isinstance(checked.get('evidence'), dict)):
            raise ContractError('invalid original checker result')
        evidence = checked['evidence']
        if checked['accepted'] is True or checked['status'] == 'original_theorem_proved':
            if (checked['accepted'] is not True or checked['status'] != 'original_theorem_proved' or
                    evidence.get('source_sha256') != state.G.sha256 or
                    evidence.get('theorem') != state.G.theorem):
                checked = rejected('integrity_error', 'original_evidence_binding_mismatch',
                                   'Original proof receipt does not match the exact source and theorem.')
        try:
            verify_source(state.G, store.root)
        except (IntegrityError, OSError) as error:
            raise IntegrityError('original source integrity failed after final verification: ' + str(error)) from error
    except (IntegrityError, ContractError) as error:
        checked = rejected('integrity_error', 'final_integrity_error', str(error))
    except TimeoutError as error:
        checked = rejected('budget_exhausted', 'final_checker_timeout', str(error))
    except Exception as error:
        checked = rejected('environment_blocked', 'final_checker_exception', str(error))
    elapsed = time.monotonic() - started
    state = replace(state, b=state.b.charge(elapsed, 0))
    store.write_json(str(final_dir.relative_to(store.root) / 'checked.json'), checked)
    evidence = checked.get('evidence', {})
    accepted = (checked.get('accepted') is True and checked.get('status') == 'original_theorem_proved'
                and evidence.get('source_sha256') == state.G.sha256
                and evidence.get('theorem') == state.G.theorem and elapsed <= report['seconds'])
    if accepted:
        return finish(store, replace(state, status='original_theorem_proved'), graph, 'strict_original_accepted')
    reported = checked['status']
    status = reported if reported in {'integrity_error', 'budget_exhausted', 'environment_blocked'} else (
        'budget_exhausted' if state.b.seconds <= 0 else 'incomplete')
    # The local lemmas remain checked. The failed original assembly cannot keep
    # an empty obligation set: reopen the exact original and drop only its links.
    state = replace(state, O=(state.root,), links=(), status=status)
    validate_invariant(state)
    sigma = checked.get('sigma')
    code = sigma.get('code') if isinstance(sigma, dict) else None
    reason = code if status != 'incomplete' and isinstance(code, str) and code else 'original_acceptance_failed'
    if status == 'budget_exhausted' and reported != 'budget_exhausted':
        reason = 'wall_budget_exhausted'
    return finish(store, state, graph, reason, [checked])


def run(state, graph, store, executor, checker, router=None):
    from .router import RuleBasedRouter
    router = router or RuleBasedRouter()
    verify_source(state.G, store.root)
    validate_invariant(state)
    if not store.path('initial_state.json').exists():
        store.write_json('initial_state.json', state.to_dict())
    state = replace(state, status='running')
    while True:
        started = time.monotonic()
        verify_source(state.G, store.root)
        validate_invariant(state)
        if state.b.seconds <= 0:
            return finish(store, replace(state, status='budget_exhausted'), graph, 'wall_budget_exhausted')
        if not state.O:
            return _final(state, graph, store, checker)
        if state.b.actions <= 0:
            return finish(store, replace(state, status='budget_exhausted'), graph, 'action_budget_exhausted')
        legal, reasons = graph.legal_candidates(state, llm_enabled=False)
        if not legal:
            if graph.expand(state):
                legal, reasons = graph.legal_candidates(state, llm_enabled=False)
            if not legal:
                state = replace(state, b=state.b.charge(time.monotonic() - started, 0))
                status, reason = classify_stop(state, legal, reasons)
                return finish(store, replace(state, status=status), graph, reason, reasons)
        action = router.choose(state, legal)
        if action is None or action not in legal:
            raise ContractError('router returned no legal registered action')
        n = state.round_index + 1
        round_path = f'rounds/{n}'
        attempt_dir = store.path(round_path)
        if attempt_dir.exists():
            # Existing evidence is never overwritten, including after a crash.
            raise IntegrityError('round directory already exists')
        attempt_dir.mkdir(parents=True)
        before = state
        store.write_json(f'{round_path}/state_before.json', before.to_dict())
        store.write_json(f'{round_path}/candidates.json', {'schema_version': 1,
            'legal': [candidate.to_dict() for candidate in legal], 'filtered': reasons})
        store.write_json(f'{round_path}/action.json', action.to_dict())
        fingerprint = action_fingerprint(before, action)
        reserved = min(before.b.seconds, action.theta.get('seconds', before.b.seconds))
        # Crash recovery cannot silently rerun an action whose outcome is unknown.
        interrupted = replace(before, round_index=n,
            b=before.b.charge(reserved, 1), attempts=before.attempts + (
                Attempt(fingerprint, action.id, 'interrupted_inflight', n),))
        checkpoint(store, interrupted, graph, inflight=True)
        try:
            remaining = max(0.0, before.b.seconds - (time.monotonic() - started))
            execution_state = replace(before, b=replace(before.b, seconds=remaining))
            result = executor.execute(execution_state, action, graph, attempt_dir)
            store.write_json(f'{round_path}/raw_result.json', result.raw_result)
            remaining = max(0.0, before.b.seconds - (time.monotonic() - started))
            updated, diagnostics = verify_and_update(before, action, result, checker,
                {'source_sha256': before.G.sha256, 'run_dir': str(store.root),
                 'attempt_dir': str(attempt_dir), 'seconds': remaining})
        except Exception as error:
            # Exceptions are technical outcomes; they consume this action and
            # preserve the unchanged obligations, never a mathematical verdict.
            integrity = isinstance(error, (IntegrityError, ContractError))
            result = ExecutionResult('integrity_error' if integrity else 'incomplete', (), (),
                FailureSignature('execution', 'contract_or_integrity_error' if integrity else 'execution_exception',
                                 str(error), type(error).__name__),
                Cost(time.monotonic() - started, 1), {}, (), (), False)
            updated, diagnostics = before, [{'code': result.sigma.code, 'message': str(error)}]
            store.write_json(f'{round_path}/raw_result.json', {})
        elapsed = time.monotonic() - started
        result = replace(result, cost=Cost(elapsed, 1))
        state = replace(updated, round_index=n, b=before.b.charge(elapsed, 1),
            attempts=before.attempts + (Attempt(fingerprint, action.id, result.sigma.code, n),))
        if result.status != 'symbolic_constructed' and state.O:
            graph.mark_failure(action, result.sigma.code)
        store.write_json(f'{round_path}/result.json', result.to_dict())
        store.write_json(f'{round_path}/verification.json', {'schema_version': 1, 'checks': diagnostics})
        store.write_json(f'{round_path}/state_after.json', state.to_dict())
        checkpoint(store, state, graph)
        if result.status == 'environment_blocked':
            alternatives, _ = graph.legal_candidates(state, llm_enabled=False)
            if alternatives:
                continue
        if result.status in ('environment_blocked', 'integrity_error', 'budget_exhausted'):
            return finish(store, replace(state, status=result.status), graph, result.sigma.code, diagnostics)


def resume(store, checker):
    """Rebind all saved proof terms by actual checks before resuming selection."""
    from .graph import Graph
    saved = store.load_checkpoint()
    if (set(saved) != {'schema_version', 'state', 'graph', 'inflight'} or
            type(saved['schema_version']) is not int or saved['schema_version'] != 1 or
            type(saved['inflight']) is not bool):
        raise IntegrityError('invalid checkpoint schema')
    state = ResidualState.from_dict(saved['state'])
    graph = Graph.from_dict(saved['graph'])
    initial = ResidualState.from_dict(store.read_json('initial_state.json'))
    if state.G != initial.G or state.Gamma != initial.Gamma or graph.source_sha256 != state.G.sha256:
        raise IntegrityError('checkpoint changed original theorem/context')
    verify_source(state.G, store.root)
    validate_invariant(state)
    started = time.monotonic()
    replayed = []
    try:
        for index, cert in enumerate(state.C):
            remaining = state.b.seconds - (time.monotonic() - started)
            if remaining <= 0:
                raise IntegrityError('insufficient budget to recheck checkpoint certificates')
            for artifact in cert.evidence.get('artifacts', ()):
                path = guard_path(artifact['path'], store.root)
                if sha256_file(path) != artifact['sha256']:
                    raise IntegrityError('saved Lean artifact hash mismatch')
            candidate = Candidate(cert.id, cert.proposition, cert.proof_term, 'AgentV2Candidate.proof',
                                  cert.source_sha256, cert.dependencies)
            checked = checker.check_partial(_candidate_request(candidate),
                {'source_sha256': state.G.sha256, 'run_dir': str(store.root),
                 'attempt_dir': str(store.path(f'resume_checks/{time.time_ns()}-{index}')),
                 'seconds': remaining})
            if checked.get('accepted') is not True or checked.get('status') != 'partial_lean_verified':
                raise IntegrityError('checkpoint certificate failed fresh Lean replay')
            evidence = checked.get('evidence', {})
            if evidence.get('source_sha256') != state.G.sha256 or evidence.get('proposition') != cert.proposition:
                raise IntegrityError('fresh checkpoint evidence binding mismatch')
            replayed.append(replace(cert, evidence=evidence))
    except Exception as error:
        state = replace(state, b=state.b.charge(time.monotonic() - started, 0), status='integrity_error')
        if not state.O:
            state = replace(state, O=(state.root,), links=())
        finish(store, state, graph, 'checkpoint_replay_failed', [{'message': str(error)}])
        raise IntegrityError('checkpoint replay refused; actual verification cost recorded') from error
    state = replace(state, C=tuple(replayed), b=state.b.charge(time.monotonic() - started, 0), status='running')
    validate_invariant(state)
    checkpoint(store, state, graph)
    return state, graph
