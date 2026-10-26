"""Parameterized rational q-telescoping using the existing Gosper normal form.

Given V=F(k+1)/F(k) and rational b_i, compute c_i independent of X and R:
       V(X) R(qX) - R(X) = sum_i c_i b_i(X).
No identity, target value, supplied denominator, or guessed degree is accepted.
"""
import sympy as s
from qgosper import (Budget, UnsupportedDomain, NormalFormLimit, coefficient_field,
                     normal_form, degree_bounds)


def _prepare_block(k_shift, rhs_basis, x, q, budget, cs, remaining):
    """Derive one Laurent equation, retaining the shared coefficient symbols."""
    k_shift = s.sympify(k_shift)
    rhs_basis = list(map(s.sympify, rhs_basis))
    if not rhs_basis:
        raise ValueError('nonempty right-hand-side basis required')
    for value in [k_shift, *rhs_basis]:
        coefficient_field(value, x, q)
    k_shift = s.cancel(k_shift)
    if k_shift == 0:
        raise UnsupportedDomain('a nonzero summand requires a nonzero shift ratio')
    rhs_basis = list(map(s.cancel, rhs_basis))
    parameters = sorted(set().union(*(v.free_symbols for v in [k_shift, *rhs_basis]),
                                   {q}) - {x}, key=str)
    field = s.QQ.frac_field(*parameters)
    denominator = s.Poly(1, x, domain=field)
    for value in rhs_basis:
        denominator = denominator.lcm(s.Poly(s.fraction(value)[1], x, domain=field))
    D = denominator.monic().as_expr()
    # Apply Gosper to H=F/D, for which D*b_i are polynomials.
    ratio = s.cancel(k_shift.subs(x, x/q)*D.subs(x, x/q)/D)
    try:
        P, A, B, normal = normal_form(ratio, x, q, field, budget.max_normal_form_degree)
    except NormalFormLimit as exc:
        return dict(status='resource_exhausted', reason=str(exc))
    rhs = [s.cancel(P*D*v) for v in rhs_basis]
    bounds = [degree_bounds(p, A, B, x, q, field)[2] for p in rhs if p != 0]
    # If every RHS is zero, R=0 and a nonzero coefficient vector already solve it.
    lo = min((b['lower'] for b in bounds), default=0)
    hi = max((b['upper'] for b in bounds), default=-1)
    trace = dict(common_denominator=str(D), normal_form=normal,
                 rhs_basis=list(map(str, rhs)), basis_bounds=bounds, lower=lo, upper=hi,
                 coefficient_domain=str(field))
    count = max(0, hi-lo+1)
    if count > remaining:
        return dict(trace=trace, status='resource_exhausted', reason='derived joint system exceeds aggregate unknown limit')
    fs = [s.Dummy(f'f{j}') for j in range(count)]
    f = s.Add(*(a*x**i for a, i in zip(fs, range(lo, hi+1))))
    residual = s.cancel(A.subs(x, q*x)*f-B*f.subs(x, x/q)
                        -sum(a*p for a, p in zip(cs, rhs)))
    equations = s.Poly(s.fraction(residual)[0], x).all_coeffs()
    return dict(status='prepared',trace=trace,equations=equations,unknowns=fs,
                f=f,factor=s.cancel(B/(D*P)),k_shift=k_shift,rhs_basis=rhs_basis)


def solve_joint(k_shifts, rhs_bases, x, q, budget=Budget(), *, normalize_index=None):
    """Solve V_i*R_i(qx)-R_i = sum_j c_j*b_ij with ONE shared c vector.

    All block equations are assembled before choosing a nullspace vector.
    Selecting one scalar solution per block would lose possible intersections.
    Nonexistence is scoped to these independent component equations only.
    """
    k_shifts=list(k_shifts);rhs_bases=[list(row) for row in rhs_bases]
    if not k_shifts or len(k_shifts)!=len(rhs_bases):
        raise ValueError('matching nonempty shift and RHS component lists required')
    width=len(rhs_bases[0])
    if not width or any(len(row)!=width for row in rhs_bases):
        raise ValueError('all RHS components require the same nonzero width')
    if normalize_index is not None and (type(normalize_index) is not int or not 0<=normalize_index<width):
        raise ValueError('invalid coefficient normalization index')
    if width>budget.max_unknowns:
        return dict(status='resource_exhausted',reason='shared coefficient count exceeds unknown limit',blocks=[])
    cs=[s.Dummy(f'c{j}') for j in range(width)]
    blocks=[];equations=[];unknowns=list(cs);traces=[]
    for index,(V,rhs) in enumerate(zip(k_shifts,rhs_bases)):
        block=_prepare_block(V,rhs,x,q,budget,cs,budget.max_unknowns-len(unknowns))
        if block['status']=='resource_exhausted':
            return dict(status='resource_exhausted',reason=block['reason'],blocks=traces,
                        failed_component=index,failed_block=block.get('trace',{}))
        blocks.append(block);traces.append(block['trace'])
        equations.extend(block['equations']);unknowns.extend(block['unknowns'])
    matrix, _ = s.linear_eq_to_matrix(equations, unknowns)
    basis = matrix.nullspace()
    trace=dict(blocks=traces,component_count=len(blocks),
               linear_system=dict(equations=matrix.rows,unknowns=matrix.cols,
                                  shared_coefficients=width,nullity=len(basis)))
    # Pure homogeneous antidifferences with c=0 are not telescopers.
    candidates = [v for v in basis if (v[normalize_index] != 0 if normalize_index is not None
                                      else any(v[i] != 0 for i in range(len(cs))))]
    if not candidates:
        return dict(trace, status='no_relation_in_joint_system')
    selected = candidates[0]
    pivot = normalize_index if normalize_index is not None else next(
        i for i in range(len(cs)) if selected[i] != 0)
    vector = [s.cancel(a/selected[pivot]) for a in selected]
    coefficients = vector[:width]
    assignment=dict(zip(unknowns,vector));certificates=[];solutions=[]
    for block in blocks:
        solved=s.cancel(block['f'].subs(assignment,simultaneous=True))
        R=s.cancel(block['factor']*solved.subs(x,x/q))
        if s.cancel(block['k_shift']*R.subs(x,q*x)-R-
                    sum(a*b for a,b in zip(coefficients,block['rhs_basis'])))!=0:
            raise ArithmeticError('joint parameterized q-Gosper component residual failed')
        certificates.append(str(R));solutions.append(str(solved))
    return dict(trace, status='constructed', coefficients=list(map(str, coefficients)),
                certificates=certificates,laurent_solutions=solutions,
                component_residuals=['0']*len(blocks),rational_residual='0')


def solve(k_shift, rhs_basis, x, q, budget=Budget(), *, normalize_index=None):
    """Backward-compatible scalar view of the shared block algorithm."""
    result=solve_joint([k_shift],[rhs_basis],x,q,budget,normalize_index=normalize_index)
    trace=result['blocks'][0] if result.get('blocks') else result.get('failed_block',{})
    output=dict(trace,status=result['status'])
    for key in ('reason','linear_system'):
        if key in result:output[key]=result[key]
    if result['status']=='constructed':
        output.update(coefficients=result['coefficients'],certificate=result['certificates'][0],
                      laurent_solution=result['laurent_solutions'][0],rational_residual='0')
    return output


def primitive_relation(coefficients, certificate, parameters):
    """Clear recurrence denominators/content and scale the certificate with it.

    The returned leading polynomial may vanish on specialization. No division by
    that polynomial, nor permission to discard its zeros, is part of this result.
    """
    parameters = sorted(set(parameters), key=str)
    common = s.Poly(1, *parameters, domain=s.QQ)
    for c in coefficients:
        common = common.lcm(s.Poly(s.fraction(s.cancel(c))[1], *parameters, domain=s.QQ))
    polynomials = [s.Poly(s.cancel(c*common.as_expr()), *parameters, domain=s.QQ)
                   for c in coefficients]
    content = polynomials[0]
    for p in polynomials[1:]:
        content = content.gcd(p)
    if content.is_zero:
        raise ValueError('zero recurrence is not a certificate')
    polynomials = [p.exquo(content) for p in polynomials]
    leading = next(p for p in reversed(polynomials) if not p.is_zero)
    scale = s.cancel(common.as_expr()/content.as_expr()/leading.LC())
    values = [s.cancel(c*scale) for c in coefficients]
    result = s.cancel(certificate*scale)
    return dict(coefficients=list(map(str, values)), certificate=str(result),
                scaling_factor=str(scale), leading_coefficient=str(values[-1]),
                normalization='primitive over QQ[parameters]; lexicographic leading scalar normalized',
                specialization_policy='leading-coefficient zeros are retained, not assumed away')
