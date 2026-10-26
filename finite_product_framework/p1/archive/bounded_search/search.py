"""Input-derived bounded rational telescoping; no per-identity ansatz interface.

This is not a complete q-Gosper algorithm. Failure means budget exhaustion only.
"""
from dataclasses import dataclass
import time
import sympy as s


@dataclass(frozen=True)
class Budget:
    max_degree: int = 6
    shift_radius: int = 1
    max_denominator_power: int = 2
    max_attempts: int = 100
    seconds: float = 30


def denominators(V, D, x, base, budget):
    """Generate poles from the equation, shifts and lcm closure, not a theorem ID."""
    seeds = [s.fraction(s.cancel(D))[1], *s.fraction(s.cancel(V))]
    seen = set()
    candidates = []
    def add(poly, origin):
        p = s.Poly(s.expand(poly), x, domain='EX').monic()
        key = s.srepr(p.as_expr())
        if key not in seen:
            seen.add(key)
            candidates.append((p.as_expr(), origin))
    add(s.Integer(1), 'polynomial search')
    for radius in range(budget.shift_radius+1):
        for j in ([0] if radius == 0 else [-radius, radius]):
            for i, seed in enumerate(seeds):
                add(s.cancel(seed.subs(x, x*base**j)), f'equation factor {i}, shift {j}')
    current = list(candidates)
    combined = s.Poly(1, x, domain='EX')
    for poly, _ in current:
        combined = s.lcm(combined, s.Poly(poly, x, domain='EX'))
    add(combined.as_expr(), 'lcm of equation-derived candidates')
    for power in range(2, budget.max_denominator_power+1):
        for poly, origin in current:
            add(poly**power, f'power {power} of {origin}')
    return candidates


def search(n_shift, k_shift, coefficient, x, base, budget=Budget()):
    started = time.monotonic()
    D = s.cancel(n_shift-coefficient)
    attempts = []
    candidates = denominators(k_shift, D, x, base, budget)
    for degree in range(budget.max_degree+1):
        for denominator, origin in candidates:
            if len(attempts) >= budget.max_attempts or time.monotonic()-started > budget.seconds:
                return {'status': 'search_exhausted', 'attempts': attempts, 'reason': 'resource budget'}
            unknowns = s.symbols(f'a0:{degree+1}')
            R = sum(a*x**i for i, a in enumerate(unknowns))/denominator
            residual = s.cancel(k_shift*R.subs(x, base*x)-R-D)
            equations = s.Poly(s.fraction(residual)[0], x).all_coeffs()
            solution_set = s.linsolve(equations, unknowns)
            attempts.append({'degree': degree, 'denominator': str(denominator), 'origin': origin})
            if solution_set is s.EmptySet or not solution_set:
                continue
            values = next(iter(solution_set))
            assignment = dict(zip(unknowns, values))
            candidate = s.cancel(R.subs(assignment, simultaneous=True).subs(dict.fromkeys(unknowns, 0)))
            if s.cancel(k_shift*candidate.subs(x, base*x)-candidate-D) != 0:
                continue
            return {'status': 'constructed', 'certificate': str(candidate),
                    'rational_residual': '0', 'attempts': attempts,
                    'equations': [str(e) for e in equations],
                    'algorithm': 'equation-derived bounded rational search',
                    'full_q_gosper': False, 'sympy_version': s.__version__}
    return {'status': 'search_exhausted', 'attempts': attempts, 'reason': 'enumerated search space exhausted'}
