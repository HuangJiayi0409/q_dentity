"""Unverified, source-bound finite-sum and endpoint candidates for one typed family.

This module does not execute CAS, approve certificates, or update residual state.
Each call emits exactly one candidate for the normal Lean/executor transaction.
"""
from collections.abc import Mapping
from dataclasses import replace
from textwrap import indent

from .formal_frontend import PROFILE, _closed_prefix, _lean, analyze_source
from .models import Candidate, ContractError, Obligation, VerifiedCertificate, digest
from .storage import IntegrityError
from .telescoping_translation import local_proof


TASKS = ('bridge', 'zero_endpoint', 'upper_endpoint')


def _validate_frontend(frontend):
    if frontend.get('status') != 'applicable' or frontend.get('profile') != PROFILE:
        raise ValueError('unsupported telescoping closure profile')
    if analyze_source(frontend['source']) != frontend:
        raise IntegrityError('closure frontend differs from frozen source reconstruction')


def _semantic_id(frontend, role, proposition):
    content = {'profile': PROFILE, 'version': 1, 'source_sha256': frontend['source']['sha256'],
               'role': role, 'proposition': proposition}
    return 'telescoping-' + role.replace('_', '-') + '-' + digest(content)[:24]


def closure_blueprint(frontend: dict) -> dict:
    """Return exact closed boundary types and the conditional original-goal bridge.

    IDs depend on the frozen source, role and formal proposition, never an action
    number or benchmark identity name. Origin actions are filled only when a
    bridge candidate proposes these obligations for a particular transaction.
    """
    _validate_frontend(frontend)
    names = frontend['symbols']
    q, m, n = (names[k] for k in ('base', 'offset', 'bound'))
    prefix = _closed_prefix(frontend['binders']) + ', '
    propositions = [
        prefix + f'FiniteQBenchmark.gaussian {q} ({m} + 0) ({m} + 1) = 0',
        prefix + (f'FiniteQBenchmark.gaussian {q} ({m} + ({n} + 1)) ({m} + 1) = '
                  f'FiniteQBenchmark.gaussian {q} ({n} + {m} + 1) ({m} + 1)'),
    ]
    obligations = [Obligation(_semantic_id(frontend, task, prop), 'boundary', prop,
                              'AgentV2Candidate.proof', frontend['source']['sha256'])
                   for task, prop in zip(TASKS[1:], propositions)]
    bridge = ' → '.join('(' + p + ')' for p in propositions + [frontend['original_proposition']])
    local_id = 'telescoping-local-' + frontend['source']['sha256'][:20]
    bridge_id = _semantic_id(frontend, 'bridge', bridge)
    certificate_ids = {'local': local_id, 'bridge': bridge_id,
                       **{task: _semantic_id(frontend, task + '_proof', prop)
                          for task, prop in zip(TASKS[1:], propositions)}}
    return {'local_id': local_id,
            'obligations': [o.to_dict() for o in obligations],
            'bridge_proposition': bridge,
            'bridge_id': bridge_id,
            'certificate_ids': certificate_ids,
            'obligation_ids': {task: o.id for task, o in zip(TASKS[1:], obligations)},
            'tasks': list(TASKS)}


def _local_dependency(frontend, approved_certificates, local_id):
    """Require the exact controlled local certificate already approved upstream.

    Receipt authenticity and artifact hashes remain the production checker's
    responsibility. This gate also prevents arbitrary proof text being inlined.
    """
    if not isinstance(approved_certificates, Mapping) or local_id not in approved_certificates:
        raise IntegrityError('finite-sum bridge requires its approved local difference certificate')
    raw = approved_certificates[local_id]
    try:
        cert = raw if isinstance(raw, VerifiedCertificate) else VerifiedCertificate.from_dict(raw)
    except ContractError as error:
        raise IntegrityError('malformed approved local difference certificate') from error
    if (cert.id != local_id or cert.source_sha256 != frontend['source']['sha256'] or
            cert.proposition != frontend['local_proposition'] or cert.dependencies != () or
            cert.proof_term != local_proof(frontend)):
        raise IntegrityError('approved local difference certificate does not match its source and template')
    return cert


def _proof_names(frontend):
    used = {b['name'] for b in frontend['binders']} | {frontend['symbols']['index']}

    def fresh(stem):
        while stem in used:
            stem += 'x'
        used.add(stem)
        return stem

    names = {key: fresh('qv2' + key) for key in
             ('inst', 'zero', 'upper', 'local', 'flux', 'telescope', 'sum', 'count', 'ih')}
    intro = [names['inst'] if b['kind'] == 'instance' else b['name'] for b in frontend['binders']]
    arguments = [b['name'] for b in frontend['binders'] if b['kind'] == 'explicit']
    return names, ' '.join(intro), ' '.join(arguments)


def _bridge_proof(frontend, local):
    symbols = frontend['symbols']
    q, m, n, j, field = (symbols[k] for k in ('base', 'offset', 'bound', 'index', 'field'))
    names, intro, args = _proof_names(frontend)
    hz, hu, hd, flux, ht, hs, count, ih = (names[k] for k in
                                        ('zero', 'upper', 'local', 'flux', 'telescope', 'sum', 'count', 'ih'))
    summation = _lean(frontend['summation'])
    # Inline the approved term so recursive assembly remains self-contained;
    # Candidate.dependencies still records its actual mathematical provenance.
    local_term = indent(local.proof_term, '    ')
    direction = '.symm' if frontend['orientation'] == 'target_equals_sum' else ''
    return (f'by\n  intro {hz} {hu} {intro}\n'
            f'  have {hd} : {frontend["local_proposition"]} := (\n{local_term}\n  )\n'
            f'  let {flux} : ℕ → {field} := fun {j} => '
            f'FiniteQBenchmark.gaussian {q} ({m} + {j}) ({m} + 1)\n'
            f'  have {ht} : ∀ {count} : ℕ, '
            f'(∑ {j} ∈ Finset.range {count}, ({flux} ({j} + 1) - {flux} {j})) = '
            f'{flux} {count} - {flux} 0 := by\n'
            f'    intro {count}\n    induction {count} with\n'
            f'    | zero => simp\n    | succ {count} {ih} =>\n'
            f'      rw [Finset.sum_range_succ, {ih}]\n      ring\n'
            f'  have {hs} : {summation} = {flux} ({n} + 1) - {flux} 0 := by\n'
            f'    calc\n      _ = ∑ {j} ∈ Finset.range ({n} + 1), '
            f'({flux} ({j} + 1) - {flux} {j}) :=\n'
            f'        Finset.sum_congr rfl (fun {j} _ => ({hd} {args} {j}).symm)\n'
            f'      _ = _ := {ht} ({n} + 1)\n'
            f'  change {summation} =\n'
            f'    FiniteQBenchmark.gaussian {q} ({m} + ({n} + 1)) ({m} + 1) - '
            f'FiniteQBenchmark.gaussian {q} ({m} + 0) ({m} + 1) at {hs}\n'
            f'  rw [{hz} {args}, {hu} {args}, sub_zero] at {hs}\n'
            f'  exact {hs}{direction}')


def make_closure_candidate(frontend: dict, task: str, approved_certificates: dict,
                           action_id: str) -> Candidate:
    """Construct one unverified bridge or endpoint candidate, without state writes."""
    if task not in TASKS:
        raise ValueError('unknown telescoping closure task')
    if not isinstance(action_id, str) or not action_id:
        raise ValueError('a closure candidate requires its origin action')
    blueprint = closure_blueprint(frontend)
    source_sha256 = frontend['source']['sha256']
    if task == 'bridge':
        local = _local_dependency(frontend, approved_certificates, blueprint['local_id'])
        children = tuple(replace(Obligation.from_dict(o), origin_action=action_id)
                         for o in blueprint['obligations'])
        return Candidate(blueprint['bridge_id'], blueprint['bridge_proposition'],
                         _bridge_proof(frontend, local), 'AgentV2Candidate.proof', source_sha256,
                         (local.id,), 'original', children)
    obligation = Obligation.from_dict(blueprint['obligations'][TASKS.index(task) - 1])
    _, intro, _ = _proof_names(frontend)
    proof = f'by\n  intro {intro}\n'
    if task == 'zero_endpoint':
        proof += f'  exact FiniteQBenchmark.gaussian_above {frontend["symbols"]["base"]} (by omega)'
    else:
        proof += '  congr 1 <;> omega'
    return Candidate(blueprint['certificate_ids'][task],
                     obligation.proposition, proof, 'AgentV2Candidate.proof', source_sha256,
                     closes=obligation.id)
