"""Bounded q-Gosper witness decoding and untrusted local Lean candidate generation."""
import ast
import hashlib
import json
import sympy as s

from .formal_frontend import PROFILE, analyze_source
from .models import Candidate
from .storage import IntegrityError


def _read_rational(text):
    """Interpret a small arithmetic AST, never sympify/eval external strings."""
    if not isinstance(text, str) or len(text) > 4096:
        raise ValueError('oversized certificate expression')
    tree = ast.parse(text, mode='eval')
    if sum(1 for _ in ast.walk(tree)) > 128: raise ValueError('certificate node limit')
    symbols = {name: s.Symbol(name) for name in ('q', 'a', 'X')}

    def visit(node, depth=0):
        if depth > 24: raise ValueError('certificate nesting limit')
        if isinstance(node, ast.Constant) and type(node.value) is int and abs(node.value) <= 1000000000:
            return s.Integer(node.value), (0, 0)
        if isinstance(node, ast.Name) and node.id in symbols:
            return symbols[node.id], (1, 0)
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
            value, degree = visit(node.operand, depth+1)
            return (-value if isinstance(node.op, ast.USub) else value), degree
        if not isinstance(node, ast.BinOp): raise ValueError('unsupported certificate syntax')
        left, ld = visit(node.left, depth+1)
        if isinstance(node.op, ast.Pow):
            right, rd = visit(node.right, depth+1)
            if rd != (0, 0) or not right.is_Integer or abs(right) > 8:
                raise ValueError('certificate exponent limit')
            degree = tuple(d*abs(int(right)) for d in (ld if right >= 0 else ld[::-1]))
            if max(degree) > 12 or left == 0 and right < 0: raise ValueError('certificate degree or zero division')
            return left ** right, degree
        right, rd = visit(node.right, depth+1)
        if isinstance(node.op, (ast.Add, ast.Sub)):
            degree = (max(ld[0]+rd[1], rd[0]+ld[1]), ld[1]+rd[1])
        elif isinstance(node.op, ast.Mult): degree = (ld[0]+rd[0], ld[1]+rd[1])
        elif isinstance(node.op, ast.Div): degree = (ld[0]+rd[1], ld[1]+rd[0])
        else: raise ValueError('unsupported certificate operator')
        if max(degree) > 12: raise ValueError('certificate degree limit')
        if isinstance(node.op, ast.Add): return left+right, degree
        if isinstance(node.op, ast.Sub): return left-right, degree
        if isinstance(node.op, ast.Mult): return left*right, degree
        if right == 0: raise ValueError('zero certificate denominator')
        return left/right, degree

    value, _ = visit(tree.body)
    if value.has(s.nan, s.zoo, s.oo, -s.oo): raise ValueError('nonfinite certificate')
    return s.cancel(value)


def local_proof(frontend):
    """Only the local difference is generated, never the original sum answer."""
    if frontend.get('status') != 'applicable' or frontend.get('profile') != PROFILE:
        raise ValueError('unsupported local proof profile')
    names = frontend['symbols']; q, m, j = (names[k] for k in ('base', 'offset', 'index'))
    used = {b['name'] for b in frontend['binders']} | {j}
    def fresh(stem):
        while stem in used: stem += 'x'
        used.add(stem); return stem
    instance, h, hi, hs = [fresh(stem) for stem in ('qv2inst', 'qv2pascal', 'qv2index', 'qv2cancel')]
    intro = [instance if b['kind'] == 'instance' else b['name'] for b in frontend['binders']]
    return (f'by\n  intro {" ".join(intro)} {j}\n'
            f'  have {h} := FiniteQP1.gaussian_pascal {q} ({m} + {j}) {m} (by omega)\n'
            f'  have {hi} : {m} + ({j} + 1) = ({m} + {j}) + 1 := by omega\n'
            f'  have {hs} : {m} + {j} - {m} = {j} := by omega\n'
            f'  rw [{hi}, {h}, {hs}]\n  ring')


def translate_candidate(frontend: dict, core_raw: dict) -> dict:
    pending = {'status': 'translation_pending', 'lean_verified': False,
               'original_identity_proved': False}
    try:
        if frontend.get('status') != 'applicable' or frontend.get('profile') != PROFILE:
            raise ValueError('unsupported frontend profile')
        fresh = analyze_source(frontend['source'])
        if fresh != frontend: raise IntegrityError('frontend output differs from frozen source reconstruction')
        request_hash = hashlib.sha256(json.dumps(frontend['core_request'], sort_keys=True,
                                                ensure_ascii=False).encode()).hexdigest()
        if (not isinstance(core_raw, dict) or core_raw.get('status') != 'constructed' or
                core_raw.get('solver') != 'q_gosper' or type(core_raw.get('schema_version')) is not int or
                core_raw.get('schema_version') != 1 or
                core_raw.get('request_sha256') != request_hash or
                core_raw.get('original_identity_proved') is not False):
            raise ValueError('CAS result is not a bound q-Gosper construction')
        q, a, X = s.symbols('q a X')
        V = q * (1-a*X)/(1-q*X)
        if s.cancel(_read_rational(core_raw['normalized_input']['k_shift'])-V) != 0:
            raise ValueError('CAS normalized shift differs from the frontend request')
        result = core_raw['result']
        if result.get('status') != 'constructed': raise ValueError('missing constructed witness')
        R = _read_rational(result['certificate'])
        if s.cancel(V*R.subs(X, q*X)-R-1) != 0:
            raise ValueError('nonzero rational antidifference residual')
        candidates = []
        representation = None
        # Same Gaussian-neighbour basis as the existing direct.py mathematics.
        # Search is in the generic rational field only. Its singularities are
        # not assumed away: Lean proves the selected polynomial flux directly.
        for shift, ratio in ((0, s.S.One), (1, (1-X)/(1-a))):
            coefficient = s.cancel(R*X/ratio)
            numerator, denominator = s.fraction(coefficient)
            candidates.append({'lower_shift': shift, 'coefficient': str(coefficient)})
            if denominator == 1 and numerator.is_polynomial(q, a, X) and shift == 1 and coefficient == 1:
                representation = {'lower_shift': shift, 'coefficient': '1',
                                  'candidates': candidates, 'division_free': True}
                break
        if representation is None: raise ValueError('no supported denominator-free Gaussian flux')
        source = frontend['source']
        candidate = Candidate('telescoping-local-' + source['sha256'][:20], frontend['local_proposition'],
                              local_proof(frontend), 'AgentV2Candidate.proof', source['sha256'])
        return {'status': 'candidate_ready', 'candidate': candidate.to_dict(),
                'representation': representation, 'lean_verified': False,
                'original_identity_proved': False,
                'reason': {'code': 'local_candidate_requires_lean'},
                'rational_certificate': str(R), 'rational_residual': '0'}
    except IntegrityError:
        raise
    except (ValueError, SyntaxError, TypeError, KeyError, AttributeError, RecursionError) as error:
        return {**pending, 'reason': {'code': 'translation_pending', 'message': str(error)}}
