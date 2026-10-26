"""Input-driven parameterized q-Gosper (q-Zeilberger) construction.

For each order, clear the n-shift denominators D, normalize H=F/D,
and solve A(qX) f(X)-B(X) f(X/q)=P sum_j c_j D V_j jointly.
The Laurent bounds come from the existing exact q-Gosper bounds, applied
to each RHS basis polynomial. No target, certificate, or recurrence is input.
"""
from dataclasses import dataclass
import sympy as s
from qgosper import Budget, coefficient_field
from expressions import expression, shift_ratio, rationalize, n, k, q, Q, X


@dataclass(frozen=True)
class ZeilbergerBudget(Budget):
    max_order: int = 4


def search(n_shift, k_shift, max_order=4, budget=Budget(), *, min_order=1):
    """Search orders with mathematically derived Laurent systems.

    max_order=None is allowed for the independently time-bounded core runner.
    The legacy pipeline keeps its default minimum order 1 and monic output.
    """
    from itertools import count
    from qparameterized import solve, primitive_relation
    if max_order is not None and (type(max_order) is not int or max_order < 0):
        raise ValueError('max_order must be a nonnegative integer or None')
    if type(min_order) is not int or min_order < 0 or (max_order is not None and min_order > max_order):
        raise ValueError('invalid minimum order')
    n_shift, k_shift = map(s.sympify, (n_shift, k_shift))
    coefficient_field(n_shift, X, q)
    coefficient_field(k_shift, X, q)
    n_shift, k_shift = map(s.cancel, (n_shift, k_shift))
    if n_shift == 0 or k_shift == 0:
        raise ValueError('nonzero compatible shift ratios required')
    compatibility = s.cancel(n_shift*k_shift.subs(Q, q*Q)-k_shift*n_shift.subs(X, q*X))
    if compatibility != 0:
        raise ValueError('incompatible n/k shift ratios: shifts do not commute')
    parameters = sorted((n_shift.free_symbols | k_shift.free_symbols | {q}) - {X}, key=str)
    vs = [s.Integer(1)]
    attempts = []
    orders = count(min_order) if max_order is None else range(min_order, max_order+1)
    for order in orders:
        while len(vs) <= order:
            j = len(vs)-1
            vs.append(s.cancel(vs[-1]*n_shift.subs(Q, q**j*Q)))
        result = solve(k_shift, vs, X, q, budget, normalize_index=order)
        trace = dict(result, order=order)
        attempts.append(trace)
        if result['status'] == 'resource_exhausted':
            return dict(status='resource_exhausted', attempts=attempts, reason=result['reason'])
        if result['status'] != 'constructed':
            trace['status'] = 'no_relation_at_order_in_joint_system'
            continue
        symbols = {str(t): t for t in set(parameters) | {X, Q, q}}
        parse = lambda value: s.sympify(value, locals=symbols)
        coefficients = list(map(parse, result['coefficients']))
        R = parse(result['certificate'])
        primitive = primitive_relation(coefficients, R, parameters)
        pcs = list(map(parse, primitive['coefficients']))
        pr = parse(primitive['certificate'])
        if s.cancel(k_shift*pr.subs(X, q*X)-pr-sum(a*v for a,v in zip(pcs,vs))) != 0:
            raise ArithmeticError('primitive q-Zeilberger relation residual failed')
        return {'status': 'constructed', 'algorithm': 'parameterized q-Gosper / q-Zeilberger',
                'order': order, 'coefficients': result['coefficients'],
                'n_shift_ratios': list(map(str, vs)), 'certificate': result['certificate'],
                'laurent_solution': result['laurent_solution'], 'rational_residual': '0',
                'coefficient_domain': result['coefficient_domain'], 'attempts': attempts,
                'primitive_relation': primitive, 'shift_compatibility_residual': '0',
                'target_used_in_search': False, 'sympy_version': s.__version__}
    return {'status': 'search_exhausted', 'algorithm': 'q-Zeilberger',
            'reason': 'no relation found through max_order; not an impossibility result',
            'attempts': attempts, 'max_order': max_order, 'target_used_in_search': False}


def construct(problem, budget):
    if set(problem) != {'schema_version', 'source_id', 'summand'} or problem['schema_version'] != 1:
        raise ValueError('invalid_problem: Zeilberger search accepts only a summand and source metadata')
    F = expression(problem['summand'])
    if F == 0:
        raise ValueError('unsupported_structure: identically zero summand')
    shifts = {'n_shift': rationalize(shift_ratio(F, n)),
              'k_shift': rationalize(shift_ratio(F, k))}
    result = search(**shifts, max_order=getattr(budget, 'max_order', 4), budget=budget)
    return {'shifts': {a: str(b) for a, b in shifts.items()}, 'construction': result}
