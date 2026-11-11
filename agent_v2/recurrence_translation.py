"""Validate an actual q-Zeilberger witness, then reuse its mathematical emitter.

The compact witness comment is untrusted input to deterministic reconstruction;
it never constitutes a verification receipt. Lean checks the reconstructed sum
recurrence in the original Field, including singular values of the base.
"""
import ast
import copy
import hashlib
import importlib
import json
from pathlib import Path
import sys
import sympy as s

from .formal_frontend import _closed_prefix
from .models import Candidate, digest
from .recurrence_frontend import PROFILE, analyze_source, lean
from .storage import IntegrityError
from .telescoping_translation import _read_rational

_PREFIX = '/- agent_v2_recurrence_v1 '
_P1 = Path(__file__).resolve().parents[1] / 'finite_product_framework/p1'


def read_rational(text):
    if not isinstance(text, str) or len(text) > 4096:
        raise ValueError('oversized recurrence arithmetic')
    tree = ast.parse(text, mode='eval')
    if any(isinstance(n, ast.Name) and n.id not in {'q', 'Q', 'X'} for n in ast.walk(tree)):
        raise ValueError('unknown recurrence arithmetic symbol')
    # Reuse the bounded arithmetic interpreter, with an explicit symbol map.
    return _read_rational(text.replace('Q', 'a')).subs(s.Symbol('a'), s.Symbol('Q'))


def _mathematics():
    # Only pure mathematical functions below are called. The retired workflow
    # functions in lean_pipeline are deliberately never invoked.
    if str(_P1) not in sys.path: sys.path.insert(0, str(_P1))
    modules = {name: importlib.import_module(name) for name in
               ('expressions', 'lean_pipeline', 'zeilberger_pipeline')}
    for name, module in modules.items():
        if Path(module.__file__).resolve() != (_P1 / (name + '.py')).resolve():
            raise IntegrityError('mathematical emitter module shadowed: ' + name)
    return modules


def shifts(frontend):
    e = _mathematics()['expressions']
    F = e.expression(frontend['core_request']['input']['summand'])
    return e.rationalize(e.shift_ratio(F, e.n)), e.rationalize(e.shift_ratio(F, e.k))


def _witness(frontend, witness):
    if not isinstance(witness, dict) or set(witness) != {'order', 'coefficients', 'certificate'}:
        raise ValueError('invalid recurrence witness fields')
    if type(witness['order']) is not int or witness['order'] != 2:
        raise ValueError('native local emitter supports monic order two only')
    if not isinstance(witness['coefficients'], list) or len(witness['coefficients']) != 3:
        raise ValueError('recurrence coefficient count mismatch')
    coefficients = [read_rational(v) for v in witness['coefficients']]
    R = read_rational(witness['certificate'])
    q, Q, X = s.symbols('q Q X')
    if coefficients[-1] != 1 or any(c.has(X) or s.fraction(c)[1] != 1 for c in coefficients):
        raise ValueError('nonmonic or nonpolynomial original-domain recurrence')
    U, V = shifts(frontend)
    ratios = [s.S.One, U, s.cancel(U * U.subs(Q, q*Q))]
    if s.cancel(V * R.subs(X, q*X) - R - sum(c*v for c, v in zip(coefficients, ratios))) != 0:
        raise ValueError('nonzero independently checked recurrence residual')
    return {'order': 2, 'coefficients': list(map(str, coefficients)), 'certificate': str(R)}


def _substitute(node, name, value):
    if node.get('op') == 'var' and node.get('name') == name: return copy.deepcopy(value)
    return {k: (_substitute(v, name, value) if isinstance(v, dict) else
                [_substitute(x, name, value) for x in v] if k == 'args' else v)
            for k, v in node.items()}


def candidate_from_witness(frontend, witness):
    if frontend.get('profile') != PROFILE or analyze_source(frontend['source']) != frontend:
        raise IntegrityError('recurrence frontend differs from frozen original reconstruction')
    witness = _witness(frontend, witness)
    modules = _mathematics(); p = modules['zeilberger_pipeline']; printer = modules['lean_pipeline']
    _, model = p.frontend(frontend['emitter_expression'], 'source-bound-recurrence')
    # A local recurrence is independent of the target equality orientation.
    model['reversed_equality'] = False
    proof, plan = p.emit_proof(model, witness, recurrence_only=True)
    names = frontend['symbols']; n, q = names['bound'], names['base']
    sums = [lean(_substitute(frontend['summation'], n,
                   {'op': '+', 'args': [{'op': 'var', 'name': n}, {'op': 'nat', 'value': j}]}))
            if j else lean(frontend['summation']) for j in range(3)]
    coefficients = [printer.polynomial_lean(read_rational(c), {'q': q, 'Q': f'({q}^{n})'})
                    for c in witness['coefficients'][:2]]
    proposition = _closed_prefix(frontend['binders']) + ', ' + (
        f'{sums[2]} + ({coefficients[0]} * {sums[0]} + {coefficients[1]} * {sums[1]}) = 0')
    used = {b['name'] for b in frontend['binders']}
    instance = 'qv2inst'
    while instance in used: instance += 'x'
    intro = ' '.join(instance if b['kind'] == 'instance' else b['name'] for b in frontend['binders'])
    header = _PREFIX + json.dumps(witness, sort_keys=True, separators=(',', ':')) + ' -/\n'
    term = header + 'by\n  intro ' + intro + '\n' + proof
    candidate = Candidate('recurrence-local-' + digest({'source': frontend['source']['sha256'],
        'witness': witness, 'profile': PROFILE})[:24], proposition, term,
        'AgentV2Candidate.proof', frontend['source']['sha256'])
    return candidate, plan


def reconstruct_candidate(frontend, term, *, allow_negative=False):
    if not isinstance(term, str) or len(term) > 48000:
        raise ValueError('oversized recurrence proof template')
    header = term.partition('\n')[0]
    if not header.startswith(_PREFIX) or not header.endswith(' -/') or len(header) > 12000:
        raise ValueError('recurrence proof lacks bounded witness header')
    witness = json.loads(header[len(_PREFIX):-3])
    candidate, _ = candidate_from_witness(frontend, witness)
    if candidate.proof_term != term and not (allow_negative and term.partition('\n')[2] in
                                            ('by rfl', 'by exact True.intro')):
        raise ValueError('recurrence proof differs from reconstructed template')
    return candidate


def translate_candidate(frontend, raw):
    pending = {'status': 'translation_pending', 'lean_verified': False, 'original_identity_proved': False}
    try:
        request_hash = hashlib.sha256(json.dumps(frontend['core_request'], sort_keys=True,
                                                 ensure_ascii=False).encode()).hexdigest()
        if (raw.get('status') != 'constructed' or raw.get('solver') != 'q_zeilberger'
                or type(raw.get('schema_version')) is not int or raw['schema_version'] != 1
                or raw.get('request_sha256') != request_hash or raw.get('original_identity_proved') is not False):
            raise ValueError('not a source-bound q-Zeilberger construction')
        U, V = shifts(frontend)
        if any(s.cancel(read_rational(raw['normalized_input'][k])-v) != 0
               for k, v in [('n_shift', U), ('k_shift', V)]):
            raise ValueError('normalized shifts differ from original summand')
        result = raw['result']
        if result.get('status') != 'constructed': raise ValueError('missing constructed witness')
        witness = _witness(frontend, {k: result[k] for k in ('order', 'coefficients', 'certificate')})
        candidate, plan = candidate_from_witness(frontend, witness)
        return {'status': 'candidate_ready', 'candidate': candidate.to_dict(), 'certificate': witness,
            'plan': plan, 'rational_residual': '0', 'lean_verified': False,
            'original_identity_proved': False,
            'remaining_work': 'Original target still needs a verified recurrence, two initial values, and uniqueness connection.'}
    except IntegrityError:
        raise
    except (ValueError, TypeError, KeyError, SyntaxError, AttributeError, RecursionError) as error:
        return {**pending, 'reason': {'code': 'translation_pending', 'message': str(error)}}
