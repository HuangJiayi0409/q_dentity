"""Exact q-Ore arithmetic and finite-state polynomial closure.

Coefficients lie in Q(q,Q,parameters); E*a(Q)=a(qQ)*E. Algorithms
return explicit witnesses; no identity names or preset object recurrences.
"""
import sympy as s
from expressions import q,Q


class OreResourceLimit(RuntimeError):
    """A construction budget, never a mathematical nonexistence result."""


def sigma(a,j=1):
    return a.applyfunc(lambda v:s.cancel(v.subs(Q,q**j*Q))) if isinstance(a,s.MatrixBase) else s.cancel(s.sympify(a).subs(Q,q**j*Q))


def clean(a):
    a=list(map(s.cancel,a))
    if not a or any(v.has(s.Float,s.nan,s.zoo,s.oo,-s.oo) or not v.is_rational_function() for v in a):
        raise ValueError("unsupported_domain: exact rational Ore coefficients required")
    for v in a:
        symbols=sorted(v.free_symbols | {q,Q},key=str)
        numerator,denominator=s.fraction(v)
        try:
            s.Poly(numerator,*symbols,domain=s.QQ)
            s.Poly(denominator,*symbols,domain=s.QQ)
        except (s.PolynomialError,s.polys.polyerrors.CoercionFailed) as exc:
            raise ValueError('unsupported_domain: coefficients must lie in QQ(q,Q,parameters)') from exc
    while len(a)>1 and a[-1]==0:a.pop()
    return a


def multiply(a,b):
    a,b=clean(a),clean(b)
    out=[s.Integer(0)]*(len(a)+len(b)-1)
    for i,ai in enumerate(a):
        for j,bj in enumerate(b):out[i+j]+=ai*sigma(bj,i)
    return clean(out)


def add(a,b):
    return clean((a[i] if i<len(a) else 0)+(b[i] if i<len(b) else 0)
                 for i in range(max(len(a),len(b))))


def direct_sum(A,B):
    return s.diag(A,B)


def tensor_product(A,B):
    return s.kronecker_product(A,B)


def companion(coefficients):
    cs=clean(coefficients);r=len(cs)-1
    if r<1 or cs[-1]==0:raise ValueError('positive order required')
    M=s.zeros(r)
    for j in range(r-1):M[j,j+1]=1
    for j in range(r):M[r-1,j]=s.cancel(-cs[j]/cs[-1])
    return M


def monomials(dimension,degree):
    if dimension==1:return [(degree,)]
    return [(j,*tail) for j in range(degree+1) for tail in monomials(dimension-1,degree-j)]


def polynomial_closure(M,degree,max_states=10000):
    if M.rows!=M.cols or M.rows<1 or degree<1:raise ValueError('nonempty square transition and positive degree required')
    clean(list(M))
    from math import comb
    if comb(M.rows+degree-1,degree)>max_states:raise ValueError('resource_exhausted: polynomial state count')
    powers=monomials(M.rows,degree);u=tuple(s.Dummy(f'u{i}') for i in range(M.rows))
    shifted=M*s.Matrix(u)
    rows=[]
    for exps in powers:
        expr=s.Poly(s.prod(v**e for v,e in zip(shifted,exps)),*u)
        rows.append([expr.coeff_monomial(m) for m in powers])
    return s.Matrix(rows),powers,u


def observable_row(expr,u,powers):
    poly=s.Poly(s.expand(expr),*u)
    if any(m not in powers for m in poly.monoms()):raise ValueError('unsupported_structure: observable is not homogeneous at closure degree')
    return s.Matrix([[poly.coeff_monomial(m) for m in powers]])


def iterate_row(row,M,j):
    for _ in range(j):row=(sigma(row)*M).applyfunc(s.cancel)
    return row


def eliminate(M,row):
    """Krylov row dependence; includes every shifted-row witness."""
    if M.rows!=M.cols or row.shape!=(1,M.rows) or M.rows<1:
        raise ValueError('nonempty square transition and compatible row required')
    clean(list(M));clean(list(row))
    if row==s.zeros(1,M.rows):
        return {'coefficients':['1'],'shifted_rows':[[str(a) for a in row]],'residual':'0'}
    rows=[row]
    for r in range(1,M.rows+1):
        rows.append(iterate_row(rows[-1],M,1))
        null=s.Matrix.vstack(*rows).T.nullspace()
        witness=next((v for v in null if v[-1]!=0),None)
        if witness is not None:
            cs=[s.cancel(v/witness[-1]) for v in witness]
            residual=sum((c*v for c,v in zip(cs,rows)),s.zeros(1,M.rows)).applyfunc(s.cancel)
            if residual!=s.zeros(1,M.rows):raise ArithmeticError('elimination residual')
            return {'coefficients':list(map(str,cs)),'shifted_rows':[[str(a) for a in v] for v in rows], 'residual':'0'}
    raise ArithmeticError('finite state elimination failed')


def forced_relation(M,observable,forcing,max_order=4):
    """Search sum(c_j sigma^j(D)) = b*forcing with monic last c_j."""
    rows=[observable]
    for order in range(1,max_order+1):
        rows.append(iterate_row(rows[-1],M,1))
        unknown=s.symbols(f'c0:{order+1}')
        residual=rows[-1]+sum((c*r for c,r in zip(unknown[:-1],rows[:-1])),s.zeros(1,M.rows))-unknown[-1]*forcing
        sol=s.linsolve(list(residual),unknown)
        if sol==s.EmptySet:continue
        values=[s.cancel(v.subs(dict.fromkeys(unknown,0))) for v in next(iter(sol))]
        check=rows[-1]+sum((c*r for c,r in zip(values[:-1],rows[:-1])),s.zeros(1,M.rows))-values[-1]*forcing
        if check.applyfunc(s.cancel)!=s.zeros(1,M.rows):raise ArithmeticError('forced relation residual')
        return {'order':order,'coefficients':list(map(str,values[:-1]+[s.Integer(1)])),
                'forcing_coefficient':str(values[-1]),'residual':'0',
                'shifted_rows':[[str(a) for a in r] for r in rows], 'forcing_row':list(map(str,forcing))}
    return {'status':'search_exhausted','max_order':max_order}


def common_left_multiple(a,b,max_unknowns=10000):
    """Return L=U*a=V*b, with exact Ore multiplication witnesses."""
    a,b=clean(a),clean(b);ra,rb=len(a)-1,len(b)-1
    if a==[0] or b==[0]:
        return {'operator':['0'],'left_multiplier':['0'],'right_multiplier':['0'],'residual':'0'}
    for degree in range(max(ra,rb),ra+rb+1):
        if 2*degree-ra-rb+2>max_unknowns:
            raise OreResourceLimit('common multiple linear system exceeds unknown limit')
        us=tuple(s.Dummy(f'l{i}') for i in range(degree-ra+1))
        vs=tuple(s.Dummy(f'r{i}') for i in range(degree-rb+1))
        lhs=multiply(us,a);rhs=multiply(vs,b)
        matrix,_=s.linear_eq_to_matrix([x-y for x,y in zip(lhs,rhs)],us+vs)
        for vector in matrix.nullspace():
            U=list(vector[:len(us)]);V=list(vector[len(us):]);L=multiply(U,a)
            if L==[0]:continue
            lc=L[-1];U=[s.cancel(v/lc) for v in U];V=[s.cancel(v/lc) for v in V];L=multiply(U,a)
            if L!=multiply(V,b):raise ArithmeticError('common left multiple residual')
            return {'operator':list(map(str,L)),'left_multiplier':list(map(str,U)),'right_multiplier':list(map(str,V)),'residual':'0'}
    raise ArithmeticError('Ore common multiple failed')


def subtract(a,b):
    return add(a,[-v for v in b])


def divide(a,b,side='right'):
    """Right divisor: a=u*b+r. Left divisor: a=b*u+r.

    The remainder has order below b; sigma is an automorphism, including
    negative shifts. These are skew Euclidean divisions over the rational field.
    """
    a,b=clean(a),clean(b)
    if b==[0]:raise ValueError('division by zero Ore operator')
    if side not in ('right','left'):raise ValueError('division side must be right or left')
    quotient=[s.Integer(0)];remainder=a
    while remainder!=[0] and len(remainder)>=len(b):
        degree=len(remainder)-len(b)
        c=(s.cancel(remainder[-1]/sigma(b[-1],degree)) if side=='right'
           else sigma(remainder[-1]/b[-1],1-len(b)))
        term=[s.Integer(0)]*degree+[c]
        quotient=add(quotient,term)
        previous=len(remainder)
        remainder=subtract(remainder,multiply(term,b) if side=='right' else multiply(b,term))
        if remainder!=[0] and len(remainder)>=previous:
            raise ArithmeticError('Ore division did not decrease order')
    check=add(multiply(quotient,b) if side=='right' else multiply(b,quotient),remainder)
    if subtract(check,a)!=[0]:raise ArithmeticError('Ore division residual')
    return quotient,remainder


def greatest_common_right_divisor(a,b):
    """Monic G with G=U*a+V*b and a=A*G, b=B*G; gcd(0,0)=0."""
    a,b=clean(a),clean(b)
    old,r=a,b
    old_u,u=[s.Integer(1)],[s.Integer(0)]
    old_v,v=[s.Integer(0)],[s.Integer(1)]
    while r!=[0]:
        quotient,remainder=divide(old,r)
        old,r=r,remainder
        old_u,u=u,subtract(old_u,multiply(quotient,u))
        old_v,v=v,subtract(old_v,multiply(quotient,v))
    if old==[0]:
        G=U=V=A=B=[s.Integer(0)]
    else:
        scale=[1/old[-1]]
        G=multiply(scale,old);U=multiply(scale,old_u);V=multiply(scale,old_v)
        A,ar=divide(a,G);B,br=divide(b,G)
        if ar!=[0] or br!=[0]:raise ArithmeticError('gcrd divisibility residual')
    if subtract(add(multiply(U,a),multiply(V,b)),G)!=[0]:
        raise ArithmeticError('gcrd Bezout residual')
    return dict(operator=list(map(str,G)),bezout_a=list(map(str,U)),bezout_b=list(map(str,V)),
                a_left_quotient=list(map(str,A)),b_left_quotient=list(map(str,B)),residual='0')


def graded_polynomial_closure(M,expr,variables,max_states=1000):
    """State space for all homogeneous degrees actually present in expr.

    This includes constants and mixed degrees, with coefficients in the base
    rational field. Linear transitions preserve each degree separately.
    """
    from math import comb
    if M.rows!=M.cols or M.rows!=len(variables) or M.rows<1:
        raise ValueError('nonempty transition and compatible variables required')
    clean(list(M))
    try:poly=s.Poly(expr,*variables)
    except s.PolynomialError as exc:
        raise ValueError('unsupported_structure: polynomial sequence observable required') from exc
    clean(poly.coeffs())
    degrees=sorted({sum(m) for m in poly.monoms()})
    count=sum(comb(M.rows+d-1,d) for d in degrees)
    if count>max_states:raise OreResourceLimit('graded polynomial state count exceeds limit')
    blocks=[];powers=[]
    for degree in degrees:
        if degree==0:
            blocks.append(s.ones(1));powers.append((0,)*M.rows)
        else:
            block,monoms,_=polynomial_closure(M,degree,max_states)
            blocks.append(block);powers.extend(monoms)
    transition=s.diag(*blocks)
    row=s.Matrix([[poly.coeff_monomial(m) for m in powers]])
    return transition,row,powers
