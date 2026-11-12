"""Check actual ring normalization and reconstruct a source-bound Lean theorem.

CAS normal forms are parsed as bounded integer polynomials, without eval,
sympify, or trusting a reported zero residual. Coefficient extraction and the
original-domain evaluation bridge are separately proved by fixed Lean rules.
"""
import ast

from .coefficient_frontend import PROFILE, analyze_source
from .formal_frontend import _closed_prefix
from .models import Candidate, canonical, digest
from .storage import IntegrityError
from .symbolic_methods import request_digest


def _bound_frontend(frontend):
    if (not isinstance(frontend, dict) or frontend.get('status') != 'applicable'
            or frontend.get('profile') != PROFILE or 'source' not in frontend):
        raise IntegrityError('coefficient frontend is not a supported frozen source')
    if canonical(analyze_source(frontend['source'])) != canonical(frontend):
        raise IntegrityError('coefficient frontend differs from frozen original reconstruction')


def make_candidate(frontend):
    """Deterministic source reconstruction, not an acceptance or core receipt."""
    _bound_frontend(frontend)
    symbols = frontend['symbols']
    q, z, n, k = (symbols['base'], symbols['parameter'], symbols['bound'],
                  frontend['coefficient_index'])
    p = f'(AgentV2Coefficient.pochPolynomial {q} {n})'
    pnext = f'(AgentV2Coefficient.pochPolynomial {q} ({n}+1))'
    proposition = _closed_prefix(frontend['binders']) + ', ' + (
        f'{p}.eval {z} = FiniteQBenchmark.poch {z} {q} {n} ∧ '
        f'{pnext}.coeff 0 = {p}.coeff 0 ∧ '
        f'∀ {k} : ℕ, {pnext}.coeff ({k}+1) = '
        f'{p}.coeff ({k}+1) - {q}^{n} * {p}.coeff {k}')
    used = {binder['name'] for binder in frontend['binders']}
    instance = 'qv2inst'
    while instance in used:
        instance += 'x'
    introductions = ' '.join(instance if b['kind'] == 'instance' else b['name']
                             for b in frontend['binders'])
    proof = f'by\n  intro {introductions}\n  exact AgentV2Coefficient.product_coefficients {q} {z} {n}'
    identity = digest({'source': frontend['source']['sha256'], 'profile': PROFILE,
                       'proposition': proposition})[:24]
    return Candidate('coefficient-local-' + identity, proposition, proof,
                     'AgentV2Candidate.proof', frontend['source']['sha256'])


def _limited(poly):
    """A monomial is a sorted tuple of names, with repetitions for powers."""
    poly = {monomial: coefficient for monomial, coefficient in poly.items() if coefficient}
    if (len(poly) > 128 or any(len(m) > 32 or abs(c).bit_length() > 4096
                               for m, c in poly.items())):
        raise ValueError('coefficient arithmetic exceeds polynomial resource bound')
    return poly


def _add(left, right, sign=1):
    out = dict(left)
    for monomial, coefficient in right.items():
        out[monomial] = out.get(monomial, 0) + sign * coefficient
    return _limited(out)


def _multiply(left, right):
    if len(left) * len(right) > 4096:
        raise ValueError('coefficient arithmetic multiplication exceeds resource bound')
    out = {}
    for a, x in left.items():
        for b, y in right.items():
            monomial = tuple(sorted(a + b))
            out[monomial] = out.get(monomial, 0) + x * y
    return _limited(out)


def _integer(value):
    if type(value) is not int or abs(value).bit_length() > 4096:
        raise ValueError('coefficient arithmetic requires a bounded exact integer')
    return {(): value} if value else {}


def _read_polynomial(text, symbols):
    if not isinstance(text, str) or not text or len(text) > 4096:
        raise ValueError('invalid or oversized coefficient arithmetic')
    tree = ast.parse(text, mode='eval')
    if sum(1 for _ in ast.walk(tree)) > 256:
        raise ValueError('coefficient arithmetic syntax exceeds resource bound')

    def visit(node, depth=0):
        if depth > 32:
            raise ValueError('coefficient arithmetic nesting exceeds resource bound')
        if isinstance(node, ast.Constant):
            return _integer(node.value)
        if isinstance(node, ast.Name) and node.id in symbols:
            return {(node.id,): 1}
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.USub, ast.UAdd)):
            value = visit(node.operand, depth + 1)
            return _add({}, value, -1 if isinstance(node.op, ast.USub) else 1)
        if isinstance(node, ast.BinOp):
            if isinstance(node.op, ast.Pow):
                if (not isinstance(node.right, ast.Constant) or type(node.right.value) is not int
                        or not 0 <= node.right.value <= 16):
                    raise ValueError('coefficient exponent must be a bounded natural number')
                value, result = visit(node.left, depth + 1), {(): 1}
                for _ in range(node.right.value):
                    result = _multiply(result, value)
                return result
            if isinstance(node.op, (ast.Add, ast.Sub, ast.Mult)):
                left, right = visit(node.left, depth + 1), visit(node.right, depth + 1)
                if isinstance(node.op, ast.Mult):
                    return _multiply(left, right)
                return _add(left, right, -1 if isinstance(node.op, ast.Sub) else 1)
        raise ValueError('unsupported coefficient arithmetic syntax or symbol')

    return visit(tree.body)


def _input_polynomial(node, atoms):
    # The caller has reconstructed this bounded request from the original Source.
    operation = node['op']
    if operation == 'atom':
        key = node['key']
        if key not in atoms:
            atoms[key] = {'symbol': 'v' + str(len(atoms)), 'display': node['display']}
        elif atoms[key]['display'] != node['display']:
            raise IntegrityError('coefficient request has conflicting atom meanings')
        return {(atoms[key]['symbol'],): 1}
    if operation == 'integer':
        return _integer(node['value'])
    if operation == 'neg':
        return _add({}, _input_polynomial(node['arg'], atoms), -1)
    left, right = (_input_polynomial(a, atoms) for a in node['args'])
    if operation == 'HMul.hMul':
        return _multiply(left, right)
    if operation in ('HAdd.hAdd', 'HSub.hSub'):
        return _add(left, right, -1 if operation == 'HSub.hSub' else 1)
    raise IntegrityError('unexpected reconstructed coefficient request operation')


def _check_construction(frontend, raw):
    request = frontend['core_request']
    if (not isinstance(raw, dict) or type(raw.get('schema_version')) is not int
            or raw['schema_version'] != 1 or raw.get('method') != 'coefficient'
            or raw.get('status') != 'constructed'
            or raw.get('request_sha256') != request_digest(request)
            or raw.get('original_identity_proved') is not False):
        raise ValueError('not a source-bound coefficient construction')
    construction = raw['construction']; expected = request['input']['goals']
    if (not isinstance(construction, dict) or construction.get('status') != 'constructed'
            or construction.get('algorithm') != 'all-branch coefficient normalization'
            or construction.get('denominator_cancellation') is not False
            or construction.get('cross_method_dependencies') != []
            or type(construction.get('goal_count')) is not int
            or construction['goal_count'] != len(expected)
            or type(construction.get('closed_goal_count')) is not int
            or construction['closed_goal_count'] != len(expected)
            or not isinstance(construction.get('goals'), list)
            or len(construction['goals']) != len(expected)):
        raise ValueError('missing or malformed complete coefficient construction')
    checks = []
    for source, result in zip(expected, construction['goals']):
        atoms = {}
        lhs = _input_polynomial(source['lhs'], atoms)
        rhs = _input_polynomial(source['rhs'], atoms)
        if (not isinstance(result, dict) or result.get('status') != 'constructed'
                or result.get('algorithm') != 'Cauchy coefficient extraction + exact polynomial normal form'
                or result.get('denominator_cancellation') is not False
                or result.get('atoms') != list(atoms.values())):
            raise ValueError('coefficient branch status or atom binding mismatch')
        symbols = {row['symbol'] for row in atoms.values()}
        reported_lhs = _read_polynomial(result['lhs_normal_form'], symbols)
        reported_rhs = _read_polynomial(result['rhs_normal_form'], symbols)
        residual = _read_polynomial(result['residual'], symbols)
        if (reported_lhs != lhs or reported_rhs != rhs or lhs != rhs
                or residual != _add(lhs, rhs, -1) or residual):
            raise ValueError('independent coefficient polynomial equality check failed')
        checks.append({'atoms': list(atoms.values()), 'input_equality': True,
                       'normal_forms_match_input': True, 'residual_is_zero': True})
    return {'status': 'passed', 'arithmetic': 'bounded exact integer polynomial dictionaries',
            'request_sha256': request_digest(request), 'checked_goals': len(checks), 'goals': checks,
            'coefficient_extraction_requires_lean': True, 'cas_proof_text_used': False}


def translate_candidate(frontend, raw):
    _bound_frontend(frontend)
    try:
        check = _check_construction(frontend, raw)
        candidate = make_candidate(frontend)
        return {'status': 'candidate_ready', 'candidate': candidate.to_dict(),
                'independent_symbolic_check': check, 'lean_verified': False,
                'original_identity_proved': False,
                'remaining_work': 'Gaussian coefficient formula and original identity remain open.'}
    except IntegrityError:
        raise
    except (ValueError, TypeError, KeyError, SyntaxError, AttributeError, RecursionError) as error:
        return {'status': 'translation_pending', 'lean_verified': False,
                'original_identity_proved': False,
                'reason': {'code': 'translation_pending', 'message': str(error)}}
