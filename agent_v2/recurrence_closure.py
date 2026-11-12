"""Source-bound second-order closure proposals, never verification receipts.

One call constructs one unverified candidate. The common checker owns receipt
binding and fresh Lean verification; the executor alone changes C/O/ProofLink.
"""
from collections.abc import Mapping
from dataclasses import replace
import json
from textwrap import indent

import sympy as s

from .formal_frontend import _closed_prefix, _node, _num, _var
from .models import Candidate, ContractError, Obligation, VerifiedCertificate, digest
from .recurrence_frontend import PROFILE, analyze_source, lean
from .recurrence_translation import _PREFIX, _substitute, read_rational, reconstruct_candidate
from .storage import IntegrityError


TASKS = ('uniqueness_bridge', 'rhs_recurrence', 'initial_zero', 'initial_one')


def _validate_frontend(frontend):
    if frontend.get('status') != 'applicable' or frontend.get('profile') != PROFILE:
        raise ValueError('unsupported recurrence closure profile')
    if analyze_source(frontend['source']) != frontend:
        raise IntegrityError('recurrence closure frontend differs from frozen source')
    n, q = (frontend['symbols'][key] for key in ('bound', 'base'))
    target = _node('ite', _node('=', _node('%', _var(n), _num(2)), _num(0)),
                   _node('poch', _var(q), _node('^', _var(q), _num(2)),
                         _node('/', _var(n), _num(2))), _num(0))
    if frontend['target'] != target:
        raise ValueError('recurrence full closure requires the parsed parity/Pochhammer target')


def _local_dependency(frontend, approved_certificates):
    """Select at most one exact, reconstructed monic order-two local witness.

    Membership in this input says the controller approved a certificate; it
    does not let the mathematical module authenticate the associated receipt.
    Unrelated closure certificates may coexist without becoming dependencies.
    """
    if approved_certificates is None:
        return None
    if not isinstance(approved_certificates, Mapping):
        raise IntegrityError('approved recurrence certificates must be an object')
    selected = []
    for key, raw in approved_certificates.items():
        if not isinstance(key, str):
            raise IntegrityError('approved recurrence certificate keys must be strings')
        try:
            cert = raw if isinstance(raw, VerifiedCertificate) else VerifiedCertificate.from_dict(raw)
        except (ContractError, TypeError) as error:
            raise IntegrityError('malformed approved recurrence certificate') from error
        local_claim = (key.startswith('recurrence-local-') or cert.id.startswith('recurrence-local-')
                       or cert.proof_term.startswith(_PREFIX))
        if not local_claim:
            continue
        if key != cert.id or cert.source_sha256 != frontend['source']['sha256'] or cert.dependencies:
            raise IntegrityError('approved local recurrence has inconsistent source, key, or dependencies')
        try:
            rebuilt = reconstruct_candidate(frontend, cert.proof_term)
            witness = json.loads(cert.proof_term.partition('\n')[0][len(_PREFIX):-3])
            q, Q = s.symbols('q Q')
            coefficients = [read_rational(c) for c in witness['coefficients']]
            matches = (len(coefficients) == 3 and
                       all(s.cancel(a-b) == 0 for a, b in zip(coefficients, (Q*q-1, 0, 1))))
        except (ValueError, TypeError, KeyError, SyntaxError) as error:
            raise IntegrityError('approved local recurrence is not a controlled witness') from error
        if (not matches or rebuilt.id != cert.id or rebuilt.proposition != cert.proposition
                or rebuilt.source_sha256 != cert.source_sha256 or rebuilt.dependencies != cert.dependencies):
            raise IntegrityError('approved local recurrence differs from the required source-bound recurrence')
        selected.append(cert)
    if len(selected) > 1:
        raise IntegrityError('ambiguous approved local recurrence certificates')
    return selected[0] if selected else None


def _semantic_id(frontend, role, proposition):
    return 'recurrence-' + role.replace('_', '-') + '-' + digest({
        'profile': PROFILE, 'closure_version': 1, 'source_sha256': frontend['source']['sha256'],
        'role': role, 'proposition': proposition})[:24]


def _at(frontend, expression, bound):
    return lean(_substitute(expression, frontend['symbols']['bound'], bound))


def closure_blueprint(frontend, approved_certificates=None):
    """Return stable closed types even before the local certificate exists."""
    _validate_frontend(frontend)
    local = _local_dependency(frontend, approved_certificates)
    n, q = (frontend['symbols'][key] for key in ('bound', 'base'))
    prefix = _closed_prefix(frontend['binders']) + ', '
    rhs = frontend['target']
    rhs_type = prefix + (
        f'{_at(frontend, rhs, _node("+", _var(n), _num(2)))} + '
        f'(((-1) + (({q}^{n}) * {q})) * {lean(rhs)} + (0) * '
        f'{_at(frontend, rhs, _node("+", _var(n), _num(1)))}) = 0')
    initial_types = [prefix + _at(frontend, frontend['summation'], _num(index)) + ' = '
                     + _at(frontend, rhs, _num(index)) for index in (0, 1)]
    propositions = [rhs_type, *initial_types]
    obligations = [Obligation(_semantic_id(frontend, task, prop), 'boundary', prop,
                              'AgentV2Candidate.proof', frontend['source']['sha256'])
                   for task, prop in zip(TASKS[1:], propositions)]
    bridge = ' → '.join('(' + prop + ')' for prop in [*propositions, frontend['original_proposition']])
    bridge_id = _semantic_id(frontend, TASKS[0], bridge)
    local_id = local.id if local else None
    return {'local_id': local_id, 'local_proposition': local.proposition if local else None,
            'bridge_id': bridge_id, 'bridge_proposition': bridge,
            'obligations': [o.to_dict() for o in obligations],
            'obligation_ids': {task: o.id for task, o in zip(TASKS[1:], obligations)},
            'certificate_ids': {'local': local_id, TASKS[0]: bridge_id,
                **{task: _semantic_id(frontend, task + '_proof', prop)
                   for task, prop in zip(TASKS[1:], propositions)}},
            'tasks': list(TASKS)}


def _proof_names(frontend):
    used = {b['name'] for b in frontend['binders']} | {frontend['symbols']['index']}
    names = {}
    for role in ('inst', 'rhs', 'zero', 'one', 'local', 'S', 'R', 'n', 'all',
                 'ih', 'hi', 'hs', 'hr', 'mod', 'div', 'even', 'exp', 'pow'):
        name = 'qv2' + role
        while name in used:
            name += 'x'
        used.add(name)
        names[role] = name
    intro = ' '.join(names['inst'] if b['kind'] == 'instance' else b['name'] for b in frontend['binders'])
    return names, intro


def _arguments(frontend, bound):
    n = frontend['symbols']['bound']
    return ' '.join('(' + bound + ')' if b['name'] == n else b['name']
                    for b in frontend['binders'] if b['kind'] == 'explicit')


def _rhs_proof(frontend):
    names, intro = _proof_names(frontend)
    n, q = (frontend['symbols'][key] for key in ('bound', 'base'))
    mod, div, even, exp, power = (names[k] for k in ('mod', 'div', 'even', 'exp', 'pow'))
    return (f'by\n  intro {intro}\n'
            f'  have {mod} : ({n}+2)%2 = {n}%2 := by omega\n'
            f'  have {div} : ({n}+2)/2 = {n}/2+1 := by omega\n'
            f'  simp only [zero_mul, add_zero, {mod}, {div}]\n'
            f'  split_ifs with {even}\n'
            f'  · rw [FiniteQBenchmark.poch_succ]\n'
            f'    have {exp} : 2*({n}/2) = {n} := by omega\n'
            f'    have {power} : {q} * ({q}^2)^({n}/2) = {q}^{n}*{q} := by\n'
            f'      rw [← pow_mul, {exp}]\n      ring\n'
            f'    rw [{power}]\n    ring\n  · ring')


def _bridge_proof(frontend, local):
    names, intro = _proof_names(frontend)
    n, q, field = (frontend['symbols'][key] for key in ('bound', 'base', 'field'))
    hrhs, hzero, hone, hlocal, S, R, index, hall, ih, hi, hs, hr = (
        names[key] for key in ('rhs', 'zero', 'one', 'local', 'S', 'R', 'n', 'all', 'ih', 'hi', 'hs', 'hr'))
    summation = _at(frontend, frontend['summation'], _var(index))
    target = _at(frontend, frontend['target'], _var(index))
    args, step_args = _arguments(frontend, n), _arguments(frontend, index)
    direction = '.symm' if frontend['orientation'] == 'target_equals_sum' else ''
    return (f'by\n  intro {hrhs} {hzero} {hone} {intro}\n'
            f'  have {hlocal} : {local.proposition} := (\n{indent(local.proof_term, "    ")}\n  )\n'
            f'  let {S} : ℕ → {field} := fun {index} => {summation}\n'
            f'  let {R} : ℕ → {field} := fun {index} => {target}\n'
            f'  have {hall} : ∀ {index}, {S} {index} = {R} {index} := by\n'
            f'    intro {index}\n    induction {index} using Nat.strong_induction_on with\n'
            f'    | h {index} {ih} =>\n      cases {index} with\n'
            f'      | zero => exact {hzero} {args}\n'
            f'      | succ {index} =>\n        cases {index} with\n'
            f'        | zero => exact {hone} {args}\n'
            f'        | succ {index} =>\n'
            f'          have {hi} : {S} {index} = {R} {index} := {ih} {index} (by omega)\n'
            f'          have {hs} := {hlocal} {step_args}\n'
            f'          have {hr} := {hrhs} {step_args}\n'
            f'          change {S} ({index}+2) + ((-1+{q}^{index}*{q}) * {S} {index} + '
            f'0 * {S} ({index}+1)) = 0 at {hs}\n'
            f'          change {R} ({index}+2) + ((-1+{q}^{index}*{q}) * {R} {index} + '
            f'0 * {R} ({index}+1)) = 0 at {hr}\n'
            f'          simp only [zero_mul, add_zero, {hi}] at {hs} {hr}\n'
            f'          change {S} ({index}+2) = {R} ({index}+2)\n'
            f'          linear_combination {hs} - {hr}\n'
            f'  exact ({hall} {n}){direction}')


def make_closure_candidate(frontend, task, approved_certificates, action_id):
    """Construct precisely one pending bridge or pending leaf proof."""
    if task not in TASKS:
        raise ValueError('unknown recurrence closure task')
    if not isinstance(action_id, str) or not action_id:
        raise ValueError('recurrence closure requires its origin action')
    # Leaf proofs have no mathematical dependency and do not consult receipts.
    bp = closure_blueprint(frontend, approved_certificates if task == TASKS[0] else None)
    source_sha256 = frontend['source']['sha256']
    if task == TASKS[0]:
        local = _local_dependency(frontend, approved_certificates)
        if local is None:
            raise IntegrityError('uniqueness bridge requires an approved local recurrence')
        children = tuple(replace(Obligation.from_dict(o), origin_action=action_id) for o in bp['obligations'])
        return Candidate(bp['bridge_id'], bp['bridge_proposition'], _bridge_proof(frontend, local),
                         'AgentV2Candidate.proof', source_sha256, (local.id,), 'original', children)
    obligation = Obligation.from_dict(bp['obligations'][TASKS.index(task)-1])
    if task == 'rhs_recurrence':
        proof = _rhs_proof(frontend)
    else:
        _, intro = _proof_names(frontend)
        simp = 'FiniteQBenchmark.gaussian' if task == 'initial_zero' else (
            'Finset.sum_range_succ, FiniteQBenchmark.gaussian')
        proof = f'by\n  intro {intro}\n  simp [{simp}]'
    return Candidate(bp['certificate_ids'][task], obligation.proposition, proof,
                     'AgentV2Candidate.proof', source_sha256, closes=obligation.id)


def reconstruct_closure_candidate(frontend, request, approved_certificates):
    """Return a canonical template, ignoring only the supplied proof body.

    The common profile decides which deliberately wrong bodies may reach Lean.
    An unknown target is not a closure; a known ID/type with any mismatched
    binding is an integrity error, never a fallback to another profile.
    """
    bp = closure_blueprint(frontend)
    targets = {TASKS[0]: bp['bridge_proposition'],
               **{task: o['proposition'] for task, o in zip(TASKS[1:], bp['obligations'])}}
    if not isinstance(request, Mapping):
        raise IntegrityError('recurrence closure request must be an object')
    matches = [task for task in TASKS if request.get('id') == bp['certificate_ids'][task]
               or request.get('proposition') == targets[task]]
    if not matches:
        if isinstance(request.get('id'), str) and any(request['id'].startswith('recurrence-' + task.replace('_', '-') + '-')
                                                    for task in TASKS):
            raise IntegrityError('unknown source-bound recurrence closure identity')
        return None
    if len(matches) != 1:
        raise IntegrityError('recurrence closure ID and proposition identify different tasks')
    task = matches[0]
    candidate = make_closure_candidate(frontend, task, approved_certificates, 'checker-template')
    if (request.get('id') != candidate.id or request.get('proposition') != candidate.proposition
            or request.get('source_sha256') != candidate.source_sha256
            or request.get('theorem') != candidate.theorem
            or request.get('dependencies') not in (list(candidate.dependencies), candidate.dependencies)):
        raise IntegrityError('recurrence closure identity, proposition, or dependency binding mismatch')
    return candidate
