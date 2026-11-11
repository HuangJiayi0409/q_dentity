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


class ReplayFailure(IntegrityError):
    """Resume refused with a preserved diagnostic category and saved run.

    Inherits the existing refusal exception for API compatibility; callers
    must use ``status`` to distinguish environment/budget/proof outcomes.
    """
    def __init__(self, status, code, message, run_dir):
        super().__init__(message)
        self.status, self.code, self.run_dir = status, code, str(run_dir)


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


def _local_scope_outcome(before, updated, diagnostics, result):
    """Classify a bounded local-proof attempt without implying parent closure."""
    for status in ('integrity_error', 'budget_exhausted', 'environment_blocked'):
        for diagnostic in diagnostics:
            check = diagnostic.get('check', {})
            if check.get('status') == status:
                return status, check.get('sigma', {}).get('code') or status
    for diagnostic in diagnostics:
        if diagnostic.get('code') == 'partial_checker_exception':
            return 'environment_blocked', 'partial_checker_exception'
        if diagnostic.get('code') == 'verification_budget_exhausted':
            return 'budget_exhausted', 'verification_budget_exhausted'
        if (diagnostic.get('code') == 'invariant_update_rejected'
                and len(updated.C) == len(before.C)
                and any(d.get('check', {}).get('accepted') is False
                        and d['check'].get('status') == 'incomplete' for d in diagnostics)):
            # A rejected proof cannot authorize its proposed residuals. Their
            # rollback is expected, not evidence of a corrupted proof state.
            continue
        if diagnostic.get('code') in ('checker_binding_rejected', 'candidate_binding_rejected',
                                      'invariant_update_rejected'):
            return 'integrity_error', diagnostic['code']
    if len(updated.C) > len(before.C):
        return 'incomplete', 'local_certificate_verified_original_open'
    if not result.C_partial:
        return 'incomplete', result.sigma.code
    return 'incomplete', 'local_verification_failed'


def _final(state, graph, store, checker):
    started = time.monotonic()
    report = {'proof_term': assemble_term(state), 'theorem': state.G.theorem,
              'proposition': state.G.proposition, 'seconds': state.b.seconds,
              'run_dir': str(store.root), 'state': state.to_dict()}
    final_dir = store.path('final/attempt-' + str(state.round_index))
    if final_dir.exists():
        final_dir = store.path(f'final/attempt-{state.round_index}-{time.time_ns()}')
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
    if status != 'integrity_error':
        # This is only a proposed tree for a future fresh replay. It is never
        # accepted as proof evidence, nor applied before every C is rechecked.
        store.write_json('final/retry.json', {'schema_version': 1, 'state': report['state']})
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
        if (state.C and state.attempts and
                state.attempts[-1].code == 'local_certificate_verified_original_open'):
            # This method's documented output is an independent local theorem.
            # Fresh resume has already recompiled it; another identical CAS
            # call cannot supply the missing finite-sum/endpoint connection.
            return finish(store, replace(state, status='incomplete'), graph,
                          'local_certificate_verified_original_open')
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
        store.write_json(f'{round_path}/selection.json', {
            'schema_version': 1, 'router': type(router).__name__, 'selected': action.id,
            'open_obligations': [o.id for o in state.O],
            'verified_certificates': [c.id for c in state.C],
            'reason': 'Choose one current legal outlet after obligation, dependency, budget and failure filtering.'})
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
        local_stop = None
        if result.raw_result.get('execution_scope') == 'local_certificate_only' and updated.O:
            if result.status not in ('environment_blocked', 'integrity_error', 'budget_exhausted'):
                if result.raw_result.get('remaining_work'):
                    diagnostics.append({'code': 'original_connection_unavailable',
                                        'remaining_work': result.raw_result['remaining_work']})
                local_stop = _local_scope_outcome(before, updated, diagnostics, result)
                if elapsed >= before.b.seconds and local_stop[0] != 'integrity_error':
                    local_stop = ('budget_exhausted', 'wall_budget_exhausted')
                result = replace(result, sigma=FailureSignature('partial', local_stop[1],
                    'Local proof scope finished; original obligation remains open.',
                    result.sigma.backend_status))
        elif result.raw_result.get('execution_scope') == 'certificate_chain':
            category, code = _local_scope_outcome(before, updated, diagnostics, result)
            if category in ('integrity_error', 'budget_exhausted', 'environment_blocked'):
                local_stop = category, code
            elif result.status in ('integrity_error', 'budget_exhausted', 'environment_blocked'):
                local_stop = result.status, result.sigma.code
            elif len(updated.C) == len(before.C) and updated.O == before.O:
                local_stop = 'incomplete', 'chain_verification_failed' if result.C_partial else result.sigma.code
        state = replace(updated, round_index=n, b=before.b.charge(elapsed, 1),
            attempts=before.attempts + (Attempt(fingerprint, action.id, result.sigma.code, n),),
            status=local_stop[0] if local_stop else updated.status)
        if result.status != 'symbolic_constructed' and state.O:
            graph.mark_failure(action, result.sigma.code)
        store.write_json(f'{round_path}/result.json', result.to_dict())
        store.write_json(f'{round_path}/verification.json', {'schema_version': 1, 'checks': diagnostics,
            'status': 'partial_lean_verified' if len(state.C) > len(before.C) else 'no_verified_progress',
            'certificates_added': len(state.C) - len(before.C),
            'open_obligations': [o.id for o in state.O], 'original_identity_proved': False})
        store.write_json(f'{round_path}/state_after.json', state.to_dict())
        checkpoint(store, state, graph)
        if local_stop:
            return finish(store, state, graph, local_stop[1], diagnostics)
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
    diagnostics = []
    try:
        for index, cert in enumerate(state.C):
            remaining = state.b.seconds - (time.monotonic() - started)
            if remaining <= 0:
                raise ReplayFailure('budget_exhausted', 'checkpoint_replay_budget_exhausted',
                                    'Insufficient budget to recheck checkpoint certificates.', store.root)
            for artifact in cert.evidence.get('artifacts', ()):
                path = guard_path(artifact['path'], store.root)
                if sha256_file(path) != artifact['sha256']:
                    raise IntegrityError('saved Lean artifact hash mismatch')
            candidate = Candidate(cert.id, cert.proposition, cert.proof_term, 'AgentV2Candidate.proof',
                                  cert.source_sha256, cert.dependencies)
            check_dir = f'resume_checks/{time.time_ns()}-{index}'
            checked = checker.check_partial(_candidate_request(candidate),
                {'source_sha256': state.G.sha256, 'source': state.G.to_dict(), 'run_dir': str(store.root),
                 'attempt_dir': str(store.path(check_dir)),
                 'prior_evidence': cert.to_dict()['evidence'],
                 'approved_certificates': {c.id: c.to_dict() for c in replayed},
                 'seconds': remaining})
            try:
                canonical(checked)
            except (TypeError, ValueError, RecursionError) as error:
                raise ContractError('checkpoint checker returned non-JSON evidence') from error
            if (not isinstance(checked, dict) or type(checked.get('accepted')) is not bool or
                    checked.get('status') not in ('partial_lean_verified', 'incomplete',
                        'environment_blocked', 'budget_exhausted', 'integrity_error')):
                raise ContractError('checkpoint checker returned malformed status')
            diagnostics.append({'candidate_id': cert.id, 'check': checked})
            store.write_json(check_dir + '/result.json', checked)
            verify_source(state.G, store.root)
            if checked.get('accepted') is not True or checked.get('status') != 'partial_lean_verified':
                status = checked['status']
                if checked['accepted'] or status == 'partial_lean_verified':
                    raise ContractError('checkpoint checker acceptance/status mismatch')
                sigma = checked.get('sigma', {})
                code = sigma.get('code') if isinstance(sigma, dict) else None
                code = code if isinstance(code, str) and code else 'checkpoint_replay_failed'
                raise ReplayFailure(status, code, 'Checkpoint certificate failed fresh Lean replay.', store.root)
            evidence = checked.get('evidence', {})
            if not isinstance(evidence, dict):
                raise ContractError('checkpoint checker returned malformed evidence')
            if evidence.get('source_sha256') != state.G.sha256 or evidence.get('proposition') != cert.proposition:
                raise IntegrityError('fresh checkpoint evidence binding mismatch')
            replayed.append(replace(cert, evidence=evidence))
        if state.O == (state.root,) and not state.links and state.status != 'integrity_error' \
                and store.path('final/retry.json').exists():
            retry = store.read_json('final/retry.json')
            if (set(retry) != {'schema_version', 'state'}
                    or type(retry['schema_version']) is not int or retry['schema_version'] != 1):
                raise IntegrityError('invalid pending final proof tree')
            proposed = ResidualState.from_dict(retry['state'])
            if (proposed.G != state.G or proposed.Gamma != state.Gamma or proposed.O
                    or proposed.r != state.r or proposed.round_index != state.round_index
                    or proposed.attempts != state.attempts or len(proposed.C) != len(replayed)
                    or any(replace(old, evidence=fresh.evidence) != fresh
                           for old, fresh in zip(proposed.C, replayed))):
                raise IntegrityError('pending final proof tree differs from freshly replayed state')
            restored = replace(state, C=tuple(replayed), O=(), links=proposed.links)
            validate_invariant(restored)
            state = restored
            store.write_json(f'resume_checks/{time.time_ns()}-final-tree.json', {
                'schema_version': 1, 'source_sha256': state.G.sha256,
                'certificates_rechecked': [c.id for c in replayed],
                'restored_links': [link.to_dict() for link in state.links],
                'original_identity_proved': False})
    except Exception as error:
        if isinstance(error, ReplayFailure):
            failure = error
        else:
            status = ('integrity_error' if isinstance(error, (IntegrityError, ContractError)) else
                      'budget_exhausted' if isinstance(error, TimeoutError) else 'environment_blocked')
            failure = ReplayFailure(status, 'checkpoint_replay_failed', str(error), store.root)
        state = replace(state, b=state.b.charge(time.monotonic() - started, 0), status=failure.status)
        if not state.O:
            state = replace(state, O=(state.root,), links=())
        diagnostics.append({'message': str(error), 'type': type(error).__name__})
        finish(store, state, graph, failure.code, diagnostics)
        if failure is error:
            raise
        raise failure from error
    state = replace(state, C=tuple(replayed), b=state.b.charge(time.monotonic() - started, 0), status='running')
    validate_invariant(state)
    checkpoint(store, state, graph)
    return state, graph
