"""q-Gosper over Q(q, parameters)(x), with q an indeterminate.

Down-ratio normal form and Laurent degree bounds follow REDUCE QSUM's
qgosper_qupdate/qdegreebound/qfindf (Koepf and Boeing); see QSUM_LICENSE.txt.
This Python implementation uses exact SymPy polynomial arithmetic. It does not
enumerate candidate certificate denominators or guessed degree bounds.
"""
from dataclasses import dataclass
import sympy as s


@dataclass(frozen=True)
class Budget:
    seconds: float = 30
    max_unknowns: int = 10000
    max_normal_form_degree: int = 10000


class UnsupportedDomain(ValueError):
    pass


class NormalFormLimit(RuntimeError):
    pass


def coefficient_field(expr, x, q):
    if not isinstance(q, s.Symbol) or not isinstance(x, s.Symbol) or x == q:
        raise UnsupportedDomain('requires distinct indeterminate base and shift variable')
    expr = s.sympify(expr)
    if (expr.has(s.Float, s.nan, s.zoo, s.oo, -s.oo) or
            not expr.is_rational_function(*expr.free_symbols)):
        raise UnsupportedDomain('requires exact rational functions in independent symbols')
    parameters = sorted(expr.free_symbols - {x} | {q}, key=str)
    return s.QQ.frac_field(*parameters)


def q_power(value, q):
    """Return m iff value == q**m, m an integer; no numerical logs or cutoff."""
    numerator, denominator = s.fraction(s.cancel(value))
    p, r = s.Poly(numerator, q, domain='EX'), s.Poly(denominator, q, domain='EX')
    if len(p.terms()) != 1 or len(r.terms()) != 1:
        return None
    (i, a), (j, b) = p.terms()[0], r.terms()[0]
    if s.cancel(a/b-1) != 0:
        return None
    return int(i[0]-j[0])


def dispersion(A, B, x, q, field):
    """Exact nonnegative shift set from irreducible factors; x is a Laurent unit."""
    factors_a = s.Poly(A, x, domain=field).factor_list()[1]
    factors_b = s.Poly(B, x, domain=field).factor_list()[1]
    shifts = set()
    for f, _ in factors_a:
        for g, _ in factors_b:
            d = f.degree()
            if d != g.degree() or d <= 0 or f.nth(0) == 0 or g.nth(0) == 0:
                continue
            power = q_power(f.LC()*g.nth(0)/(f.nth(0)*g.LC()), q)
            if power is None or power < 0 or power % d:
                continue
            j = power // d
            shifted = s.Poly(g.as_expr().subs(x, q**j*x), x, domain=field)
            if f.monic() == shifted.monic():
                shifts.add(j)
    return sorted(shifts)


def normal_form(ratio, x, q, field, max_degree=None):
    """r(x) = P(x)/P(x/q) * A(x)/B(x), with A and B q-shift reduced."""
    A, B = s.fraction(s.cancel(ratio))
    P = s.Integer(1)
    shifts = dispersion(A, B, x, q, field)
    updates = []
    for j in shifts:
        divisor = s.gcd(s.Poly(A, x, domain=field),
                        s.Poly(B.subs(x, q**j*x), x, domain=field)).monic().as_expr()
        if not divisor.has(x):
            continue
        projected_degree = s.Poly(P, x, domain=field).degree() + j*s.degree(divisor, x)
        if max_degree is not None and projected_degree > max_degree:
            raise NormalFormLimit('derived normal-form degree exceeds resource limit')
        A = s.cancel(A/divisor)
        B = s.cancel(B/divisor.subs(x, x/q**j))
        P = s.expand(P*s.prod(divisor.subs(x, x/q**i) for i in range(j)))
        updates.append({'shift': j, 'factor': str(divisor)})
    if s.cancel(ratio-P/P.subs(x, x/q)*A/B) != 0:
        raise ArithmeticError('q-Gosper normal form invariant failed')
    remaining = dispersion(A, B, x, q, field)
    if remaining:
        raise ArithmeticError('q-Gosper normal form is not shift reduced')
    return P, A, B, {'dispersion': shifts, 'updates': updates,
                     'P': str(P), 'A': str(A), 'B': str(B),
                     'normal_form_residual': '0', 'remaining_dispersion': remaining}


def degree_bounds(P, A, B, x, q, field):
    """Necessary and sufficient finite search interval for the Laurent ansatz.

    Solve A(q*x) f(x) - B(x) f(x/q) = P(x). Leading/trailing
    cancellation can occur only at exactly recognized integer powers of q.
    """
    pp, aa, bb = [s.Poly(v, x, domain=field) for v in (P, A, B)]
    low_p, low_a, low_b = [min(m[0] for m in poly.monoms()) for poly in (pp, aa, bb)]
    high_p, high_a, high_b = [poly.degree() for poly in (pp, aa, bb)]
    lo = low_p-min(low_a, low_b)
    hi = high_p-max(high_a, high_b)
    low_resonance = high_resonance = None
    if low_a == low_b:
        power = q_power(bb.nth(low_b)/aa.nth(low_a), q)
        if power is not None:
            low_resonance = power-low_a
            lo = min(lo, low_resonance)
    if high_a == high_b:
        power = q_power(bb.LC()/aa.LC(), q)
        if power is not None:
            high_resonance = power-high_a
            hi = max(hi, high_resonance)
    return int(lo), int(hi), {'lower': int(lo), 'upper': int(hi),
                             'lower_resonance': low_resonance,
                             'upper_resonance': high_resonance,
                             'source': 'q-Gosper Laurent leading/trailing coefficient bounds'}


def antidifference(down_ratio, x, q, budget=Budget()):
    """Given t(x)/t(x/q), find S with t(qx)/t(x)*S(qx)-S(x)=1.

    Returns no_q_hypergeometric_antidifference only after the exact Laurent
    system is inconsistent. Resource exhaustion is a distinct result.
    """
    coefficient_field(s.sympify(down_ratio), x, q)
    down_ratio = s.cancel(down_ratio)
    if down_ratio == 0:
        raise UnsupportedDomain('zero term must be handled before taking its ratio')
    field = coefficient_field(down_ratio, x, q)
    try:
        P, A, B, normal = normal_form(down_ratio, x, q, field,
                                    budget.max_normal_form_degree)
    except NormalFormLimit as exc:
        return dict(status='resource_exhausted', algorithm='q-Gosper', reason=str(exc))
    lo, hi, bounds = degree_bounds(P, A, B, x, q, field)
    trace = {'algorithm': 'q-Gosper',
             'coefficient_domain': str(field), 'down_ratio': str(down_ratio),
             'normal_form': normal, 'laurent_bounds': bounds}
    if hi < lo:
        return dict(trace, status='no_q_hypergeometric_antidifference', reason='empty Laurent interval')
    if hi-lo+1 > budget.max_unknowns:
        return dict(trace, status='resource_exhausted', reason='derived system exceeds unknown limit')
    unknowns = [s.Dummy(f'c{i}') for i in range(hi-lo+1)]
    f = sum(a*x**i for a, i in zip(unknowns, range(lo, hi+1)))
    residual = s.expand(A.subs(x, q*x)*f-B*f.subs(x, x/q)-P)
    equations = s.Poly(s.fraction(s.cancel(residual))[0], x).all_coeffs()
    solutions = s.linsolve(equations, unknowns)
    trace['linear_system'] = {'unknowns': len(unknowns), 'equations': len(equations)}
    if solutions == s.EmptySet:
        return dict(trace, status='no_q_hypergeometric_antidifference', reason='inconsistent Laurent system')
    values = next(iter(solutions))
    solved = s.cancel(f.subs(dict(zip(unknowns, values)), simultaneous=True)
                      .subs(dict.fromkeys(unknowns, 0)))
    if s.cancel(A.subs(x, q*x)*solved-B*solved.subs(x, x/q)-P) != 0:
        raise ArithmeticError('Laurent equation verification failed')
    certificate = s.cancel(B/P*solved.subs(x, x/q))
    if s.cancel(down_ratio.subs(x, q*x)*certificate.subs(x, q*x)-certificate-1) != 0:
        raise ArithmeticError('antidifference certificate verification failed')
    return dict(trace, status='constructed', laurent_solution=str(solved),
                antidifference_ratio=certificate, rational_residual='0')
