"""Bind bounded model proposals to one selected obligation, before Lean checks.

This module grants no evidence and makes no state/graph changes. A decomposition
is committed only by executor.verify_and_update after its implication passes.
"""
from dataclasses import replace

from .local_tasks import candidate_for, make_task
from .models import ContractError, Obligation, digest


OUTPUT_SCHEMA = {
    'prove': {'kind': 'prove', 'proof_term': 'a Lean term proving the selected goal'},
    'decompose': {'kind': 'decompose', 'children': ['1 to 3 closed Lean propositions'],
                  'proof_term': 'a Lean term of type (child1) → ... → (selected goal)'},
    'lemma': {'kind': 'lemma', 'proposition': 'a useful closed Lean proposition',
              'proof_term': 'a Lean term proving this proposition'},
}


def bind_proposal(state, action, response):
    if not isinstance(response, dict):
        raise ContractError('model proposal must be a JSON object')
    kind = response.get('kind')
    fields = {'prove': {'kind', 'proof_term'},
              'decompose': {'kind', 'proof_term', 'children'},
              'lemma': {'kind', 'proof_term', 'proposition'}}
    if kind not in fields or set(response) != fields[kind]:
        raise ContractError('model proposal has unknown fields or kind')
    proof = response['proof_term']
    if not isinstance(proof, str) or not proof.strip() or len(proof) > 64000:
        raise ContractError('model proof must be a bounded, nonempty Lean term')
    goal_id = action.theta.get('goal_id')
    parent = next((o for o in state.O if o.id == goal_id), None)
    if parent is None or action.target != goal_id:
        raise ContractError('model target is not the selected open obligation')
    children = ()
    if kind == 'decompose':
        values = response['children']
        if not isinstance(values, list) or not 1 <= len(values) <= 3 or any(
                not isinstance(p, str) or not p.strip() or len(p) > 16000 for p in values):
            raise ContractError('decomposition requires one to three bounded closed propositions')
        if values == [parent.proposition]:
            raise ContractError('decomposition merely renames the same goal')
        scope = digest({'source': state.G.sha256, 'parent': parent.id,
                        'round': state.round_index, 'action': action.id, 'children': values})[:24]
        children = tuple(Obligation(f'goal-{scope}-{i}', 'subgoal', p, p,
                                   state.G.sha256, action.id) for i, p in enumerate(values))
    proposition = response.get('proposition')
    if kind == 'lemma' and (not isinstance(proposition, str) or not proposition.strip()
                            or len(proposition) > 16000):
        raise ContractError('independent lemma requires a bounded closed proposition')
    # The graph has already verified the transition. This temporary selected
    # view does not mutate the persistent current pointer or proof tree.
    selected = replace(state, r=action.target)
    task = make_task(selected, action.target, parent.id, children=children,
                     proposition=proposition, dependencies=tuple(c.id for c in state.C))
    return task, candidate_for(task, proof), children
