"""Higher-order PLDE in certified PiSigma* towers.

Coefficient order is ascending: sum a[j]*sigma**j(g) = sum c[i]*f[i].
The denominator, Pi Laurent bounds and Sigma degree bound are computed,
never supplied or guessed. See Abramov--Bronstein--Petkovsek--Schneider,
arXiv:2005.04944, Theorems 4, 6 and 7. Resource limits are not nonexistence.
"""
import itertools
import sympy as s
from ore import OreResourceLimit


def trim(tower, coefficients, rhs, depth):
    a=list(map(tower.normal, coefficients)); f=list(map(tower.normal, rhs))
    while a and a[-1]==0:a.pop()
    if not a:raise ValueError('nonzero difference operator required')
    first=next(j for j,v in enumerate(a) if v!=0)
    if first:
        a=[tower.sigma(v,depth,-first) for v in a[first:]]
        f=[tower.sigma(v,depth,-first) for v in f]
    return a,f


def apply(tower,a,g,depth):
    return tower.normal(sum(v*tower.sigma(g,depth,j) for j,v in enumerate(a) if v!=0))


def divisors(tower,poly):
    factors=poly.monic().factor_list()[1]
    count=s.prod(e+1 for p,e in factors)
    if count>tower.budget.max_unknowns:raise OreResourceLimit('hypergeometric divisor count exceeds budget')
    return [tower.normal(s.prod(p.monic().as_expr()**e for (p,m),e in zip(factors,exponents)))
            for exponents in itertools.product(*(range(m+1) for p,m in factors))]


def candidates(tower,coefficients,depth):
    """Finite complete superset of hypergeometric similarity classes."""
    a,_=trim(tower,coefficients,[],depth)
    key=('hypergeometric_candidates',depth,tuple(a))
    if key in tower.cache:return tower.cache[key]
    if len(a)==1:return []
    if depth==0:
        z=s.Dummy('ratio');poly=tower.poly(sum(v*z**j for j,v in enumerate(a)),z)
        result=[tower.normal(-p.nth(0)/p.nth(1)) for p,m in poly.factor_list()[1] if p.degree()==1 and p.nth(0)!=0]
    else:
        t,kind,alpha=tower.nodes[depth-1];alpha=alpha if kind=='product' else s.Integer(1)
        aa=tower.clear_denominators(a,t);order=len(aa)-1
        left=divisors(tower,aa[0]);right=divisors(tower,tower.poly(tower.sigma(aa[-1].as_expr(),depth,1-order),t))
        if len(left)*len(right)>tower.budget.max_unknowns:raise OreResourceLimit('hypergeometric divisor pairs exceed budget')
        result=[];lower_cache={}
        # Common nonzero factors in the lower operator may be omitted.
        # lc(prod sigma**j(a/b), j<i) is computed directly, avoiding
        # convention-dependent nested sigma-product notation.
        for numerator in left:
            for denominator in right:
                ratio=tower.normal(numerator/denominator)
                numerator_degree=tower.poly(numerator,t).degree();denominator_degree=tower.poly(denominator,t).degree()
                degrees=[p.degree()+j*numerator_degree+(order-j)*denominator_degree if not p.is_zero else -s.oo
                         for j,p in enumerate(aa)]
                highest=max(degrees)
                if degrees.count(highest)<2:continue
                degree_difference=numerator_degree-denominator_degree
                factor=s.Integer(1);lower=[]
                for j,p in enumerate(aa):
                    lower.append(tower.normal(p.LC()*factor) if degrees[j]==highest else s.Integer(0))
                    # product_{k=0}^{j-1} sigma^k(alpha) is the leading
                    # multiplier of sigma^j(t).
                    factor=tower.normal(factor*s.prod(tower.sigma(alpha,depth-1,k) for k in range(j))**degree_difference)
                lower_key=tuple(lower)
                if lower_key not in lower_cache:lower_cache[lower_key]=candidates(tower,lower,depth-1)
                result.extend(tower.normal(u*ratio) for u in lower_cache[lower_key])
                if len(result)>tower.budget.max_unknowns:raise OreResourceLimit('hypergeometric candidate set exceeds budget')
        result=list(dict.fromkeys(result))
    tower.cache[key]=result
    return result


def denominator(tower,a,rhs,depth):
    t,kind,alpha=tower.nodes[depth-1]
    polys=tower.clear_denominators([*a,*rhs],t);aa=polys[:len(a)];ff=polys[len(a):]
    def ordinary(p):
        if kind=='product':return tower.poly(p.as_expr()/t**min(m[0] for m in p.monoms()),t).monic()
        return p.monic()
    left,right=ordinary(aa[0]),ordinary(aa[-1]);offsets=[]
    for p,_ in left.factor_list()[1]:
        for r,_ in right.factor_list()[1]:
            j=tower.orbit(p.as_expr(),r.as_expr(),depth)
            if j is not None and j>=0:offsets.append(j)
    radius=max(offsets,default=-1)-(len(a)-1)
    if max(0,radius+1)*left.degree()>tower.budget.max_normal_form_degree:
        raise OreResourceLimit('higher-order universal denominator exceeds budget')
    D=s.Integer(1)
    for j in range(max(0,radius+1)):D=tower.normal(D*tower.monic(tower.sigma(left.as_expr(),depth,j),depth))
    cleared=tower.clear_denominators([p.as_expr()/tower.sigma(D,depth,j) for j,p in enumerate(aa)]+[f.as_expr() for f in ff],t)
    return D,cleared[:len(a)],cleared[len(a):],dict(pole_offsets=sorted(set(offsets)),pole_radius=radius,denominator=str(D))


def integer_roots(tower,value,z):
    if value==0:return []
    result=[]
    for p,m in tower.poly(value,z).factor_list()[1]:
        if p.degree()==1:
            root=tower.normal(-p.nth(0)/p.nth(1))
            if root.is_Integer and root>=0:result.append(int(root))
    return result


def specialized_kernel(tower,matrix,z):
    """Kernel over K(z), with all exceptional nonnegative integer fibers.

    Track every pivot and denominator during exact elimination. Outside their
    roots each row operation specializes invertibly, hence the nullspace basis
    specializes to a full basis. This is the specialization argument of Lemma
    12; a full Smith form is unnecessary for this cofinite guarantee.
    """
    M=s.MutableDenseMatrix(matrix);exceptions=set();pivots=[];row=0
    def observe(value):
        for part in s.fraction(tower.normal(value)):
            exceptions.update(integer_roots(tower,part,z))
    for v in M:observe(s.fraction(tower.normal(v))[1])
    for col in range(M.cols):
        pivot=next((i for i in range(row,M.rows) if M[i,col]!=0),None)
        if pivot is None:continue
        M.row_swap(row,pivot);value=M[row,col];observe(value)
        for j in range(col,M.cols):M[row,j]=tower.normal(M[row,j]/value)
        for i in range(M.rows):
            if i==row or M[i,col]==0:continue
            value=M[i,col]
            for j in range(col,M.cols):M[i,j]=tower.normal(M[i,j]-value*M[row,j])
        pivots.append(col);row+=1
        if row==M.rows:break
    basis=[]
    for col in range(M.cols):
        if col in pivots:continue
        v=s.zeros(M.cols,1);v[col]=1
        for i,p in enumerate(pivots):v[p]=-M[i,col]
        common=s.Integer(1)
        for value in v:
            den=s.fraction(tower.normal(value))[1];observe(den)
            common=tower.poly(common,z).lcm(tower.poly(den,z)).as_expr()
        # Polynomial representatives make the next coefficient splitting exact.
        basis.append(v.applyfunc(lambda e:tower.normal(e*common)))
    return basis,sorted(exceptions)


def sigma_degree(tower,aa,ff,depth):
    t,kind,eta=tower.nodes[depth-1];high=max(p.degree() for p in aa)
    rhs_degree=max([int(p.degree()) for p in ff if not p.is_zero],default=-1)
    leading=[p.nth(high) for p in aa]
    initial=solve(tower,leading,[s.Integer(0)],depth-1)
    vectors=[[g] for cs,g in initial if g!=0]
    bound=max(0,rhs_degree-int(high));steps=[]
    if not vectors:return bound,steps
    degree=s.Dummy('degree');offsets=[tower.normal(tower.sigma(t,depth,j)-t) for j in range(len(aa))]
    level=0
    while True:
        if level>=tower.budget.max_normal_form_degree:raise OreResourceLimit('Sigma degree-bound descent exceeds budget')
        target_level=level+1;polynomials=[]
        for v in vectors:
            total=0
            for i,coefficient in enumerate(v):
                for j,p in enumerate(aa):
                    for k in range(max(0,int(high)+i-target_level),int(high)+1):
                        ell=target_level-i+k-int(high)
                        if ell<0 or p.nth(k)==0:continue
                        choose=s.prod(degree-i-r for r in range(ell))/s.factorial(ell)
                        total-=p.nth(k)*tower.sigma(coefficient,depth-1,j)*choose*offsets[j]**ell
            polynomials.append(tower.poly(tower.normal(total),degree))
        maxdegree=max([int(p.degree()) for p in polynomials if not p.is_zero],default=0)
        width=len(vectors)
        forcing=[p.nth(j) for j in range(maxdegree+1) for p in polynomials]
        if len(forcing)>tower.budget.max_unknowns:raise OreResourceLimit('Sigma degree constraint width exceeds budget')
        lower=solve(tower,leading,forcing,depth-1)
        matrix=s.Matrix([[tower.normal(cs[j*width+i]-degree**j*cs[i]) for cs,g in lower]
                         for j in range(1,maxdegree+1) for i in range(width)])
        if matrix.rows==0:matrix=s.zeros(0,len(lower))
        kernel,exceptions=specialized_kernel(tower,matrix,degree)
        new=[]
        for weights in kernel:
            c=[tower.normal(sum(w*cs[i] for w,(cs,g) in zip(weights,lower))) for i in range(width)]
            v=[tower.normal(sum(w*old[i] for w,old in zip(c,vectors))) for i in range(level+1)]
            v.append(tower.normal(sum(w*g for w,(cs,g) in zip(weights,lower))))
            if any(x!=0 for x in v):new.append(v)
        bound=max(bound+1,max(exceptions,default=-1))
        steps.append(dict(level=target_level,exceptional_degrees=exceptions,remaining_vectors=len(new),bound=bound))
        if not any(v[0]!=0 for v in new):return bound,steps
        vectors=new;level+=1
        if len(vectors)*(level+1)>tower.budget.max_unknowns:raise OreResourceLimit('Sigma formal coefficient space exceeds budget')


def bounds(tower,aa,ff,depth):
    t,kind,alpha=tower.nodes[depth-1]
    if kind=='sum':
        upper,steps=sigma_degree(tower,aa,ff,depth)
        return 0,upper,dict(sigma_degree_descent=steps)
    nonzero=[p for p in aa if not p.is_zero]
    low=min(min(m[0] for m in p.monoms()) for p in nonzero);high=max(p.degree() for p in nonzero)
    limits=[];resonances=[]
    for endpoint in (low,high):
        es=[]
        for u in candidates(tower,[p.nth(endpoint) for p in aa],depth-1):
            e=tower.exponent(alpha,u,depth-1)
            if e is not None and e.is_Integer:es.append(int(e))
        resonances.append(sorted(set(es)));limits.append(es)
    nonzero_rhs=[p for p in ff if not p.is_zero]
    if nonzero_rhs:
        limits[0].append(min(min(m[0] for m in p.monoms()) for p in nonzero_rhs)-low)
        limits[1].append(max(p.degree() for p in nonzero_rhs)-high)
    lo=int(min(limits[0])) if limits[0] else 0
    hi=int(max(limits[1])) if limits[1] else lo-1
    return lo,hi,dict(low_candidate_exponents=resonances[0],high_candidate_exponents=resonances[1])


def solve(tower,coefficients,rhs,depth=None):
    depth=len(tower.nodes) if depth is None else depth
    a,ff=trim(tower,coefficients,rhs,depth)
    if not ff:raise ValueError('nonempty RHS basis required')
    key=('PLDE',depth,tuple(a),tuple(ff))
    if key in tower.cache:return tower.cache[key]
    if len(a)==1 or depth==0:
        result=tower.solve(0,sum(a) if depth==0 else a[0],ff,depth) if depth>0 or sum(a)!=0 else tower.solve(1,-1,ff,0)
    elif len(a)==2:result=tower.solve(a[1],a[0],ff,depth)
    else:
        D,aa,bb,trace=denominator(tower,a,ff,depth)
        lo,hi,degree_trace=bounds(tower,aa,bb,depth)
        tower.trace.append(dict(kind='higher_order_tower_bounds',variable=str(tower.nodes[depth-1][0]),
                                order=len(a)-1,lower=lo,upper=hi,**trace,**degree_trace))
        if hi-lo+1>tower.budget.max_normal_form_degree or hi-lo+1+len(ff)>tower.budget.max_unknowns:
            raise OreResourceLimit('higher-order derived coefficient range exceeds budget')
        t,kind,alpha=tower.nodes[depth-1];high=max(p.degree() for p in aa)
        basis=[(tuple(s.Integer(i==j) for i in range(len(ff))),s.Integer(0)) for j in range(len(ff))]
        operator=[p.as_expr() for p in aa]
        for d in range(hi,lo-1,-1):
            if not basis:break
            targets=[]
            for cs,g in basis:
                residual=tower.normal(sum(c*f.as_expr() for c,f in zip(cs,bb))-apply(tower,operator,g,depth))
                # A shift by a known Laurent valuation enables polynomial extraction.
                num,den=s.fraction(residual);np,dp=tower.poly(num,t),tower.poly(den,t)
                valuation=min(m[0] for m in dp.monoms())
                if len(dp.terms())!=1:raise ArithmeticError('coefficient descent left an ordinary pole')
                targets.append(tower.normal(np.nth(d+high+valuation)/dp.nth(valuation)) if d+high+valuation>=0 else s.Integer(0))
            lower=[tower.normal(p.nth(high)*(tower.sigma(t,depth,j)/t)**d) if kind=='product' else p.nth(high)
                   for j,p in enumerate(aa)]
            local=solve(tower,lower,targets,depth-1);updated=[]
            for weights,coefficient in local:
                cs=tuple(tower.normal(sum(w*b[0][i] for w,b in zip(weights,basis))) for i in range(len(ff)))
                g=tower.normal(sum(w*b[1] for w,b in zip(weights,basis))+coefficient*t**d)
                updated.append((cs,g))
            basis=updated
        residuals=[tower.normal(apply(tower,operator,g,depth)-sum(c*f.as_expr() for c,f in zip(cs,bb))) for cs,g in basis]
        result=[(cs,tower.normal(g/D)) for cs,g in tower.constrain(basis,residuals,depth)]
    for cs,g in result:
        if any(tower.sigma(c,depth)!=c for c in cs) or tower.normal(apply(tower,a,g,depth)-sum(c*f for c,f in zip(cs,ff)))!=0:
            raise ArithmeticError('higher-order original equation residual')
    tower.cache[key]=result
    return result


def compute(data,budget,parse):
    from qpisigma import parse_problem
    from qpisigma_system import build_tower
    from expressions import X,q
    expected={'extensions','operator','rhs_basis'}
    if not isinstance(data,dict) or set(data) not in (expected,expected|{'algebraic_extensions'}):
        raise ValueError('difference_equation requires extensions, operator and RHS basis')
    operator=data['operator']
    if not isinstance(operator,list) or not operator:raise ValueError('nonempty ascending-order operator required')
    if len(operator)>budget.max_states:raise OreResourceLimit('difference operator order exceeds state budget')
    if 'algebraic_extensions' in data:
        from qfinite import prepare
        from qnumberfield import fixed_constant_solve,periodic_scalar
        from qgosper import UnsupportedDomain
        if not isinstance(data['rhs_basis'],list) or not data['rhs_basis']:raise ValueError('nonempty RHS basis required')
        parsed,flat,_,_,algebra=prepare(dict(extensions=data['extensions'],algebraic_extensions=data['algebraic_extensions'],
                                            rhs_basis=operator+data['rhs_basis']),budget,parse)
        a=list(map(algebra.normal,flat[:len(operator)]));rhs=list(map(algebra.normal,flat[len(operator):]))
        if not any(a):raise ValueError('nonzero operator in finite algebra required')
        try:native=fixed_constant_solve(algebra,parsed,rhs,budget,1,-1,operator=a)
        except UnsupportedDomain as exc:
            if 'vanishes on a finite component' in str(exc):raise
            native=periodic_scalar(algebra,parsed,a,rhs,budget)
        if native is None:native=periodic_scalar(algebra,parsed,a,rhs,budget)
        basis,trace=native
        def encode(cs,g):
            allowed=set(algebra.field.symbols)|set(algebra.variables)
            if any(s.sympify(v).free_symbols-allowed for v in [*cs,g]):raise ArithmeticError('unrestored algebraic PLDE symbol')
            current=g;residual=0
            for coefficient in a:residual+=coefficient*current;current=algebra.sigma(current)
            if algebra.normal(residual-sum(c*f for c,f in zip(cs,rhs)))!=0 or any(algebra.normal(algebra.sigma(c)-c)!=0 for c in cs):
                raise ArithmeticError('original algebraic higher-order residual')
            return dict(coefficients=list(map(str,cs)),certificate=str(g),residual='0',
                        unit_coefficient_indices=[j for j,c in enumerate(cs) if algebra.multiplication(c).det()!=0])
        result=dict(solution_basis=[encode(cs,g) for cs,g in basis],reduction_trace=trace,
                    completeness='full invariant-coefficient solution space over the admitted reduced number algebra')
        selected=next(((cs,g) for cs,g in basis if any(cs)),None)
        if selected:result.update(encode(*selected))
        return dict(status='constructed' if selected else 'no_relation_in_declared_basis',solver='difference_equation',result=result,
                    domain=dict(operator_convention='ascending: sum operator[j]*sigma^j(g)',
                                algorithm='native algebraic-number higher-order PiSigma PLDE and CRT',
                                defining_relations_are_input_objects=True,nonunit_coefficients_do_not_isolate_a_summand=True))
    parsed,rhs,_,_=parse_problem(dict(extensions=data['extensions'],rhs_basis=data['rhs_basis']),budget,parse)
    a=list(map(parse,operator))
    from qgosper import UnsupportedDomain
    try:tower=build_tower(parsed,[*a,*rhs],budget)
    except UnsupportedDomain:
        from qnumberfield import rational_periodic_algebra,periodic_scalar
        from qpisigma import PiSigma
        algebra=rational_periodic_algebra(parsed,[*a,*rhs],budget)
        basis,trace=periodic_scalar(algebra,parsed,a,rhs,budget)
        tower=PiSigma(budget);tower.trace=[trace]
    else:
        aa=[tower.normal(v.xreplace(tower.aliases)) for v in a];ff=[tower.normal(v.xreplace(tower.aliases)) for v in rhs]
        basis=solve(tower,aa,ff)
    definitions=dict(tower.generated_definitions)
    for c,v in tower.constants.items():definitions[c]=tower.normal(v.xreplace(definitions))
    shift={X:q*X,**{t:t+v if k=='sum' else t*v for t,k,v in parsed}}
    def encode(cs,g):
        cs=[s.cancel(c.xreplace(definitions)) for c in cs];g=s.cancel(g.xreplace(definitions));current=g;residual=0
        for coefficient in a:
            residual+=coefficient*current;current=s.cancel(current.xreplace(shift))
        residual=s.cancel(residual-sum(c*f for c,f in zip(cs,rhs)))
        if residual!=0 or any(s.cancel(c.xreplace(shift)-c)!=0 for c in cs):raise ArithmeticError('original higher-order equation residual')
        return dict(coefficients=list(map(str,cs)),certificate=str(g),residual='0')
    result=dict(solution_basis=[encode(cs,g) for cs,g in basis],reduction_trace=tower.trace,
                completeness='complete rational solution space in the certified PiSigma-star tower')
    selected=next(((cs,g) for cs,g in basis if any(cs)),None)
    if selected:result.update(encode(*selected))
    return dict(status='constructed' if selected else 'no_relation_in_declared_basis',solver='difference_equation',result=result,
                domain=dict(operator_convention='ascending: sum operator[j]*sigma^j(g)',
                            input_shift_relations_are_premises=True,algorithm='derived universal denominator and recursive PiSigma PLDE',
                            obligations='original finite-sum semantics, boundaries, initial values and Lean remain external'))
