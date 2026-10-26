"""Parameterized rational q-difference systems over QQ(q,parameters)(x).

Solve sigma(r)*V-r = sum c_j*h_j, c_j independent of x. Invertible V is
uncoupled coordinatewise solely to derive necessary universal bounds. The
finite linear system is then solved in the ORIGINAL coupled equations.
No guessed denominator, pole radius, or degree is accepted.
"""
import sympy as s
from qgosper import Budget,UnsupportedDomain,coefficient_field,dispersion,q_power
from ore import OreResourceLimit


def shift(value,x,q,j=1):
    fn=lambda v:s.cancel(v.subs(x,q**j*x))
    return value.applyfunc(fn) if isinstance(value,s.MatrixBase) else fn(s.sympify(value))


def field_for(values,x,q):
    values=list(map(s.sympify,values))
    for value in values:coefficient_field(value,x,q)
    parameters=sorted(set().union(*(v.free_symbols for v in values),{q})-{x},key=str)
    field=s.QQ.frac_field(*parameters)
    try:
        for value in values:
            num,den=s.fraction(s.cancel(value))
            s.Poly(num,x,domain=field);s.Poly(den,x,domain=field)
    except (s.PolynomialError,s.polys.polyerrors.CoercionFailed) as exc:
        raise UnsupportedDomain('exact rational coefficient field required') from exc
    return field


def polynomialize(coefficients,rhs,x,field,budget):
    values=[s.cancel(v) for v in [*coefficients,*rhs]]
    common=s.Poly(1,x,domain=field)
    for value in values:
        common=common.lcm(s.Poly(s.fraction(value)[1],x,domain=field))
        if common.degree()>budget.max_normal_form_degree:
            raise OreResourceLimit('derived scalar clearing denominator exceeds degree limit')
    polys=[s.Poly(s.cancel(v*common.as_expr()),x,domain=field) for v in values]
    # Removing content shared with ALL RHS columns preserves all parameters c.
    content=polys[0]
    for p in polys[1:]:content=content.gcd(p)
    polys=[p.exquo(content) for p in polys]
    if max(p.degree() for p in polys)>budget.max_normal_form_degree:
        raise OreResourceLimit('derived scalar equation exceeds degree limit')
    m=len(coefficients)
    return polys[:m],polys[m:]


def power_roots(poly,t,q,field):
    """All integers e with poly(q**e)=0. Such roots are linear over field."""
    roots=[]
    for factor,_ in s.Poly(poly,t,domain=field).factor_list()[1]:
        if factor.degree()==1:
            value=s.cancel(-factor.nth(0)/factor.nth(1))
            if value!=0:
                exponent=q_power(value,q)
                if exponent is not None:roots.append(exponent)
    return sorted(set(roots))


def scalar_bounds(coefficients,rhs,x,q,budget=Budget()):
    """Every rational solution y has y=f/D with Laurent f in [lower,upper].

    For polynomial a_i and RHS, a nonzero-pole orbit starts at a factor of a_0
    and ends m shifts before a factor of a_m. If N=disp(a_m,a_0)-m, then
    D=product_{j=0}^N sigma^j(a_0/x^valuation(a_0)) bounds all such poles,
    including multiplicities (see QGOSPER.md for the valuation argument).
    The exceptional orbit x=0 is bounded via indicial q-power roots instead.
    """
    coefficients=list(map(s.sympify,coefficients));rhs=list(map(s.sympify,rhs))
    if len(coefficients)<2 or coefficients[0]==0 or coefficients[-1]==0:
        raise ValueError('positive scalar order with nonzero endpoints required')
    field=field_for([*coefficients,*rhs],x,q)
    aa,bb=polynomialize(coefficients,rhs,x,field,budget)
    order=len(aa)-1
    def without_x(poly):
        valuation=min(m[0] for m in poly.monoms())
        return s.Poly(poly.as_expr()/x**valuation,x,domain=field).monic()
    left,right=without_x(aa[0]),without_x(aa[-1])
    overlaps=dispersion(right.as_expr(),left.as_expr(),x,q,field)
    radius=max(overlaps,default=-1)-order
    predicted_degree=max(0,radius+1)*left.degree()
    if predicted_degree>budget.max_normal_form_degree:
        raise OreResourceLimit('derived universal denominator exceeds degree limit')
    D=s.Poly(1,x,domain=field)
    for j in range(max(0,radius+1)):
        D*=s.Poly(shift(left.as_expr(),x,q,j),x,domain=field).monic()
    den=D.monic().as_expr()
    transformed=[s.cancel(p.as_expr()/shift(den,x,q,j)) for j,p in enumerate(aa)]
    cc,dd=polynomialize(transformed,[p.as_expr() for p in bb],x,field,budget)
    nonzero=[(j,p) for j,p in enumerate(cc) if not p.is_zero]
    low=min(min(m[0] for m in p.monoms()) for _,p in nonzero)
    high=max(p.degree() for _,p in nonzero)
    t=s.Dummy('indicial')
    low_poly=sum(p.nth(low)*t**j for j,p in nonzero)
    high_poly=sum(p.nth(high)*t**j for j,p in nonzero)
    low_roots=power_roots(low_poly,t,q,field)
    high_roots=power_roots(high_poly,t,q,field)
    nonzero_rhs=[p for p in dd if not p.is_zero]
    lows=list(low_roots);highs=list(high_roots)
    if nonzero_rhs:
        lows.append(min(min(m[0] for m in p.monoms()) for p in nonzero_rhs)-low)
        highs.append(max(p.degree() for p in nonzero_rhs)-high)
    lower,upper=(int(min(lows)),int(max(highs))) if lows and highs else (0,-1)
    trace=dict(scalar_coefficients=[str(p.as_expr()) for p in aa],
        scalar_rhs_basis=[str(p.as_expr()) for p in bb],dispersion=overlaps,pole_radius=radius,
        universal_denominator=str(den),denominator_degree=int(D.degree()),
        laurent_equation=[str(p.as_expr()) for p in cc],laurent_rhs_basis=[str(p.as_expr()) for p in dd],
        low_indicial=str(low_poly.xreplace({t:s.Symbol('T')})),
        high_indicial=str(high_poly.xreplace({t:s.Symbol('T')})),
        low_resonances=low_roots,high_resonances=high_roots,lower=lower,upper=upper,
        scope='all rational solutions of this scalar equation in the declared formal field')
    return den,lower,upper,trace


def uncouple_coordinate(A,G,index,x,q):
    """sigma(y)=A*y+G*c; derive scalar equation for coordinate index."""
    dimension=A.rows;width=G.cols
    row=s.zeros(1,dimension);row[index]=1
    rows=[row];forcing=[s.zeros(1,width)]
    for order in range(1,dimension+1):
        shifted=shift(rows[-1],x,q)
        forcing.append((shift(forcing[-1],x,q)+shifted*G).applyfunc(s.cancel))
        rows.append((shifted*A).applyfunc(s.cancel))
        kernel=s.Matrix.vstack(*rows).T.nullspace()
        vector=next((v for v in kernel if v[-1]!=0),None)
        if vector is None:continue
        coefficients=[s.cancel(v/vector[-1]) for v in vector]
        if coefficients[0]==0:raise ArithmeticError('invertible-system scalarization lost trailing coefficient')
        residual=sum((c*r for c,r in zip(coefficients,rows)),s.zeros(1,dimension)).applyfunc(s.cancel)
        if residual!=s.zeros(1,dimension):raise ArithmeticError('uncoupling residual')
        rhs=sum((c*f for c,f in zip(coefficients,forcing)),s.zeros(1,width)).applyfunc(s.cancel)
        return coefficients,list(rhs),dict(order=order,coefficients=list(map(str,coefficients)),
            rhs_basis=list(map(str,rhs)),state_rows=[[str(v) for v in row] for row in rows],
            forcing_rows=[[str(v) for v in row] for row in forcing],residual='0')
    raise ArithmeticError('coordinate uncoupling failed')


def solve_system(V,rhs_rows,x,q,budget=Budget(),*,normalize_index=None,include_basis=False):
    """Exact parameterized row-system solve, complete at a fixed RHS basis."""
    V=s.Matrix(V);rhs_rows=[s.Matrix([list(row)]) for row in rhs_rows]
    if V.rows<1 or V.rows!=V.cols or not rhs_rows or any(r.cols!=V.rows for r in rhs_rows):
        raise ValueError('square nonempty k_matrix and compatible nonempty RHS rows required')
    width=len(rhs_rows)
    if V.rows>getattr(budget,'max_states',128) or width>budget.max_unknowns:
        raise OreResourceLimit('rational system input size exceeds limit')
    field_for([*V,*[v for row in rhs_rows for v in row]],x,q)
    if s.cancel(V.det())==0:raise ValueError('unsupported_structure: invertible k-shift matrix required')
    if normalize_index is not None and (type(normalize_index) is not int or not 0<=normalize_index<width):
        raise ValueError('invalid coefficient normalization index')
    A=V.T.inv().applyfunc(s.cancel)
    G=(A*s.Matrix.vstack(*rhs_rows).T).applyfunc(s.cancel)
    traces=[];bounds=[];count=width
    for index in range(V.rows):
        cs,bs,uncoupling=uncouple_coordinate(A,G,index,x,q)
        D,lo,hi,trace=scalar_bounds(cs,bs,x,q,budget)
        count+=max(0,hi-lo+1)
        traces.append(dict(coordinate=index,uncoupling=uncoupling,**trace));bounds.append((D,lo,hi))
        if count>budget.max_unknowns:
            raise OreResourceLimit('derived rational-system Laurent unknowns exceed aggregate limit')
    cs=[s.Dummy(f'c{j}') for j in range(width)];unknowns=list(cs);ansatz=[]
    for index,(D,lo,hi) in enumerate(bounds):
        fs=[s.Dummy(f'f{index}_{j}') for j in range(max(0,hi-lo+1))]
        unknowns.extend(fs)
        ansatz.append(sum((a*x**j for a,j in zip(fs,range(lo,hi+1))),s.Integer(0))/D)
    row=s.Matrix([ansatz]);target=sum((c*r for c,r in zip(cs,rhs_rows)),s.zeros(1,V.rows))
    residual=shift(row,x,q)*V-row-target
    equations=[]
    for value in residual:
        equations.extend(s.Poly(s.fraction(s.cancel(value))[0],x).all_coeffs())
    matrix,_=s.linear_eq_to_matrix(equations,unknowns)
    # The entries have already been certified rational. Domain arithmetic
    # avoids generic-expression simplification at each Gaussian pivot, which
    # becomes prohibitive for algebraic regular-representation denominators.
    from sympy.polys.matrices import DomainMatrix
    domain_matrix=DomainMatrix.from_Matrix(matrix).to_field()
    kernel_matrix=domain_matrix.nullspace(divide_last=True).to_Matrix()
    kernel=[kernel_matrix.row(i).T for i in range(kernel_matrix.rows)]
    trace=dict(coordinate_bounds=traces,linear_system=dict(equations=matrix.rows,unknowns=matrix.cols,
        shared_coefficients=width,nullity=len(kernel)),fixed_basis_solver='complete rational system via derived bounds')
    def decode(vector):
        assignments=dict(zip(unknowns,vector))
        certificate=row.subs(assignments,simultaneous=True).applyfunc(s.cancel)
        coefficients=[s.cancel(v) for v in vector[:width]]
        check=(shift(certificate,x,q)*V-certificate-
               sum((c*r for c,r in zip(coefficients,rhs_rows)),s.zeros(1,V.rows))).applyfunc(s.cancel)
        if check!=s.zeros(1,V.rows):raise ArithmeticError('original coupled-system residual')
        return dict(coefficients=list(map(str,coefficients)),certificate_row=list(map(str,certificate)),residual='0')
    if include_basis:trace['solution_basis']=[decode(v) for v in kernel]
    candidates=[v for v in kernel if (v[normalize_index]!=0 if normalize_index is not None else any(v[:width]))]
    if not candidates:return dict(trace,status='no_relation_in_declared_basis')
    selected=candidates[0]
    pivot=normalize_index if normalize_index is not None else next(j for j in range(width) if selected[j]!=0)
    return dict(trace,status='constructed',**decode([s.cancel(v/selected[pivot]) for v in selected]))
