"""One residual-aware CAS or model action. No hidden proving loop."""
from dataclasses import replace
import time

from .executor import normalize_result, validate_action_origin
from .graph_proposals import OUTPUT_SCHEMA, bind_proposal
from .local_tasks import dependency_name
from .models import ContractError, Cost, ExecutionResult, FailureSignature, thaw
from .storage import IntegrityError, guard_path, sha256_file


def outcome(started, status, code, *, raw=None, candidates=(), children=(), diagnostics=()):
    return ExecutionResult(status, tuple(candidates), tuple(children),
        FailureSignature('autonomous', code, code, None), Cost(time.monotonic()-started, 1),
        raw or {}, (), tuple(diagnostics), False)


def prompt_context(state, action, representation, capabilities, library, feedback):
    goal = next(o for o in state.O if o.id == action.theta['goal_id'])
    return {
        'instructions': (
            'Perform exactly one local proof action. Return one JSON object in one of output_schema forms. '
            'Use Lean 4 and the supplied fixed mathematical environment. All propositions are closed with '
            'their own binders; preserve the original domain and assumptions. Do not emit imports, declarations, '
            'commands, axioms, sorry, admit, native_decide, run_tac, IO or external tools. '
            'Prefer a short proof using the approved certificate aliases and library declarations. '
            'If a direct proof is unavailable, propose up to three concrete subgoals AND prove their implication '
            'to the selected goal. Do not prove the subgoals in that action. Subgoals can enable an exact listed '
            'CAS local target. Every proposed proof is checked before state changes. '
            'An independent lemma alone does not close the selected goal. '
            'Purpose expansion means try a new mathematically justified representation/decomposition; '
            'purpose repair means respond to actual Lean feedback, not repeat the identical failed text.'),
        'output_schema': OUTPUT_SCHEMA,
        'purpose': action.theta.get('purpose', 'local_proof'),
        'original': {'identity': state.G.identity, 'sha256': state.G.sha256,
                     'proposition': state.G.proposition, 'original_context': state.G.Gamma},
        'selected_representation': representation.to_dict(),
        'selected_goal': goal.to_dict(),
        'open_goals': [o.to_dict() for o in state.O],
        'approved_certificates': [{'id': c.id, 'name': dependency_name(c.id),
                                   'type': c.proposition} for c in state.C],
        'available_cas': capabilities,
        'library': library,
        'feedback': feedback,
        'remaining_budget': state.b.to_dict(),
    }


class AutonomousExecutor:
    def __init__(self, model, checker, capabilities, *, library=None, method_adapter=None, feedback=()):
        from .cas_adapter import MethodAdapter
        self.model, self.checker, self.capabilities = model, checker, capabilities
        self.library = list(library or ())
        self.method_adapter = method_adapter or MethodAdapter()
        self.feedback = list(feedback)

    def execute(self, state, action, graph, attempt_dir):
        started = time.monotonic()
        validate_action_origin(state, action)
        if state.b.seconds <= 0 or state.b.actions <= 0:
            return outcome(started,'budget_exhausted','action_budget_exhausted')
        legal, _ = graph.legal_candidates(state, llm_enabled=True)
        if action not in legal or action.theta.get('autonomous') is not True:
            raise ContractError('autonomous executor requires a currently legal bound action')
        parent = next((o for o in state.O if o.id == action.theta.get('goal_id')), None)
        node = graph.nodes[action.target]
        if parent is None or node.id != parent.id or graph._proposition(node, state) != parent.proposition:
            raise ContractError('selected CAS/LLM input differs from the current typed task')
        seconds = min(state.b.seconds, action.theta.get('seconds', state.b.seconds))
        if seconds <= 0:
            return outcome(started, 'budget_exhausted', 'action_budget_exhausted')
        directory = guard_path(attempt_dir)
        if action.M == 'LLM':
            raw = self.model.generate('residual_action',
                prompt_context(state, action, node, self.capabilities, self.library, self.feedback),
                seconds=seconds, attempt_dir=directory / 'model')
            if raw.get('status') != 'ok':
                code = raw.get('error_code') or 'model_unavailable'
                return outcome(started, 'budget_exhausted' if code in ('call_limit','model_call_limit') else
                               'environment_blocked', code, raw=raw)
            try:
                task, candidate, children = bind_proposal(state, action, raw.get('content'))
                self.checker.register_task(task)
            except (ContractError, ValueError, TypeError) as error:
                # An untrusted proposal is a failed attempt, not corruption of
                # the existing proof state. Its unchanged O is retained.
                return outcome(started, 'incomplete', 'invalid_model_proposal', raw=raw,
                               diagnostics=({'message': str(error)},))
            return outcome(started, 'symbolic_constructed', 'model_candidate_generated',
                raw=dict(raw, task=task.to_dict()), candidates=(candidate,), children=children)
        method = action.theta.get('method')
        capability = self.capabilities.get(method)
        if capability is None or action.theta.get('version') != capability['version']:
            raise ContractError('method is absent from this source capability inventory')
        if parent != state.root and (not capability.get('local_lean') or
                                     parent.proposition != capability.get('local_proposition')):
            raise ContractError('CAS has no exact contract for the selected residual task')
        # Source carries the verified mathematical structure and original
        # domain. It is not a substitute for the checked local target above.
        raw = self.method_adapter.execute(state.G.identity, method, state.G.to_dict(),
                                          directory / 'backend', seconds)
        result = normalize_result(raw)
        if result.O_res:
            raise ContractError('autonomous source CAS must return only local certificates')
        for artifact in result.artifacts:
            path = guard_path(artifact.path, directory)
            if sha256_file(path) != artifact.sha256:
                raise IntegrityError('CAS artifact hash differs')
        candidates = []
        for candidate in result.C_partial:
            if candidate.replaces:
                raise ContractError('source CAS cannot introduce autonomous children')
            if parent != state.root and candidate.proposition != parent.proposition:
                raise ContractError('CAS output does not prove its selected local task')
            closes = parent.id if candidate.proposition == parent.proposition else None
            candidates.append(replace(candidate, closes=closes))
        return replace(result, C_partial=tuple(candidates),
                       raw_result=dict(thaw(result.raw_result), selected_goal=parent.to_dict(),
                                       selected_representation=node.to_dict()))
