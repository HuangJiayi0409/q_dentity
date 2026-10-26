"""Bounded rational telescoping search; this is not a full q-Gosper implementation."""
import sympy as sp


def search_linear_numerator(n_shift, k_shift, coefficient, denominator, variable, base):
    """Solve V(X) R(qX) - R(X) = U(X) - c for R=(a0+a1 X)/D.

    Ratios belong to a formal rational function field. The caller must provide a
    Lean bridge valid on the original domain, including singular specializations.
    """
    a0, a1 = sp.symbols('a0 a1')
    trial = (a0 + a1 * variable) / denominator
    residual = sp.cancel(k_shift * trial.subs(variable, base * variable)
                         - trial - (n_shift - coefficient))
    numerator = sp.fraction(residual)[0]
    equations = sp.Poly(numerator, variable).all_coeffs()
    solutions = sp.solve(equations, (a0, a1), dict=True)
    verified = []
    for solution in solutions:
        if a0 not in solution or a1 not in solution:
            continue
        candidate = sp.cancel(trial.subs(solution))
        check = sp.cancel(k_shift * candidate.subs(variable, base * variable)
                          - candidate - (n_shift - coefficient))
        if check == 0:
            verified.append((candidate, solution))
    if not verified:
        raise ValueError('search_exhausted: no solution in the selected rational ansatz')
    candidate, solution = verified[0]
    return candidate, {
        'backend': 'SymPy', 'version': sp.__version__,
        'algorithm': 'bounded linear-numerator rational ansatz',
        'full_q_gosper': False,
        'input': {'n_shift_ratio': str(n_shift), 'k_shift_ratio': str(k_shift),
                  'target_coefficient': str(coefficient),
                  'denominator': str(denominator), 'numerator_degree_bound': 1},
        'equations': [str(x) + ' = 0' for x in equations],
        'solution': {str(k): str(v) for k, v in solution.items()},
        'flux_ratio': str(candidate), 'rational_residual': '0',
        'domain': 'formal rational function field; not a pointwise endpoint definition',
    }


def binomial_search():
    q, Q, X, z = sp.symbols('q Q X z')
    # Explicit adapter for the frozen Gaussian summand. No general Lean parser.
    U = (1-q*Q)/(1-q*Q/X)
    V = -z*X*(1-Q/X)/(1-q*X)
    c = 1-z*Q
    R, record = search_linear_numerator(U, V, c, X-q*Q, X, q)
    # Translate R F to A F(k-1); this must have the supported polynomial form.
    backward_ratio = V.subs(X, X/q)
    polynomial_multiplier = sp.cancel(R * backward_ratio)
    if sp.cancel(polynomial_multiplier - z*Q) != 0:
        raise ValueError('representation_gap: no implemented Lean bridge for this flux')
    record['translation'] = {
        'R_times_Fk_over_Fprevious': str(polynomial_multiplier),
        'flux_zero': '0', 'flux_successor': 'z*q^n*F(n,k)',
        'lean_definition': 'FiniteQP1.binomialFlux',
        'bridge': 'division-free Gaussian Pascal and weight shift; verified in Lean',
    }
    return record
