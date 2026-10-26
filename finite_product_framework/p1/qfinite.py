"""Exact finite reduced algebras and periodic difference-ring telescoping.

Algebraic relations describe the input objects, not precomputed certificates.
Denominators must be units; zero divisors are never silently divided out.
"""
import itertools
import math
import re
import sympy as s
from expressions import X,q
from qdifference import rational_read
from qrational_system import solve_system,field_for
from qpisigma import PiSigma,parse_problem
from qgosper import UnsupportedDomain
from ore import OreResourceLimit


class FiniteAlgebra:
    def __init__(self,extensions,free_shift,budget,extra_symbols=()):
        self.budget=budget;self.variables=[row[0] for row in extensions]
        self.relations=[row[1] for row in extensions];self.images=[row[2] for row in extensions]
        self.shift={**free_shift,**dict(zip(self.variables,self.images))}
        parameters=set().union(*(v.free_symbols for v in [*self.relations,*self.images,*free_shift.values()]),{q,X},set(extra_symbols))-set(self.variables)
        self.field=s.QQ.frac_field(*sorted(parameters,key=str))
        degrees=[];earlier=set()
        for z,polynomial,image in extensions:
            if polynomial.free_symbols&(set(self.variables)-earlier-{z}):raise ValueError('triangular algebraic relations required')
            try:poly=s.Poly(polynomial,z)
            except s.PolynomialError as exc:raise ValueError('polynomial algebraic relation required') from exc
            if poly.degree()<1 or s.cancel(poly.LC()-1)!=0:raise ValueError('positive-degree monic algebraic relation required')
            degrees.append(int(poly.degree()));earlier.add(z)
        dimension=math.prod(degrees)
        if dimension>budget.max_states:raise OreResourceLimit('finite quotient dimension exceeds state budget')
        self.basis=[s.prod(v**e for v,e in zip(self.variables,es)) for es in itertools.product(*(range(d) for d in degrees))]
        self.G=s.groebner(self.relations,*reversed(self.variables),domain=self.field)
        self.triangular_polys=[s.Poly(p,z,domain=s.EX) for z,p in zip(self.variables,self.relations)]
        self.exponents=[s.Poly(v,*self.variables).monoms()[0] for v in self.basis]
        for z,poly,image in extensions:
            if self.multiplication(s.diff(poly,z)).det()==0:raise UnsupportedDomain('nonreduced or inseparable quotient is not admitted')
        for poly in self.relations:
            if self.normal(poly.xreplace(self.shift))!=0:raise ValueError('shift does not preserve the algebraic defining ideal')
        self.V=s.Matrix([self.vector(v.xreplace(self.shift)) for v in self.basis])
        if s.cancel(self.V.det())==0:raise ValueError('algebraic shift is not an automorphism')

    def remainder(self,value):
        # Monic triangular leading monomials are pairwise coprime, hence this
        # reverse substitution is the same unique normal form as G.reduce.
        # Keep rational coefficients as expressions until after elimination;
        # converting a large unreduced numerator into QQ(parameters) first
        # needlessly constructs and cancels many multivariate fractions.
        for z,poly in reversed(list(zip(self.variables,self.triangular_polys))):
            value=s.Poly(value,z,domain=s.EX).rem(poly).as_expr()
        return s.cancel(value)

    def polynomial_vector(self,value):
        poly=s.Poly(self.remainder(value),*self.variables)
        return [poly.coeff_monomial(e) for e in self.exponents]

    def multiplication(self,value):
        value=self.remainder(value)
        # row coefficients act on the right.
        return s.Matrix([self.polynomial_vector(value*b) for b in self.basis])

    def normal(self,value):
        numerator,denominator=s.fraction(s.cancel(value))
        numerator=self.remainder(numerator);denominator=self.remainder(denominator)
        if denominator==0:raise ValueError('zero denominator in finite quotient')
        if not denominator.has(*self.variables):return s.cancel(numerator/denominator)
        matrix=self.multiplication(denominator)
        if s.cancel(matrix.det())==0:raise ValueError('nonunit denominator (zero divisor) in finite quotient')
        inverse=s.Matrix([self.polynomial_vector(s.Integer(1))])*matrix.inv()
        return self.remainder(numerator*sum(c*b for c,b in zip(inverse,self.basis)))

    def vector(self,value):return self.polynomial_vector(self.normal(value))
    def expression(self,row):return self.normal(sum(c*b for c,b in zip(row,self.basis)))
    def sigma(self,value):return self.normal(s.sympify(value).xreplace(self.shift))


def finite_order(V,shifting_variables,budget):
    if any(v.free_symbols&set(shifting_variables) for v in V):return None
    poly=V.charpoly().as_poly();T=poly.gen
    order=1
    for f,m in poly.factor_list()[1]:
        found=None
        for n in range(1,2*V.rows**2+1):
            if s.expand(s.cyclotomic_poly(n,T)-f.monic().as_expr())==0:found=n;break
        if found is None:return None
        order=s.ilcm(order,found)
    if order>budget.max_normal_form_degree:raise OreResourceLimit('finite automorphism order exceeds budget')
    return int(order) if (V**order-s.eye(V.rows)).applyfunc(s.cancel)==s.zeros(V.rows) else None


def constant_kernel(residuals,variables,width):
    equations=[]
    for coordinate in range(width):
        values=[s.cancel(row[coordinate]) for row in residuals]
        denominator=s.prod(s.fraction(v)[1] for v in values)
        polys=[s.Poly(s.cancel(v*denominator),*variables) for v in values]
        monomials=set().union(*(set(p.monoms()) for p in polys))
        equations.extend([[p.coeff_monomial(m) for p in polys] for m in monomials])
    return s.Matrix(equations).nullspace()


def periodic_solve(algebra,tower,rhs,budget):
    V=algebra.V;rank=V.rows;variables=[t for t,k,v in tower.nodes]
    order=finite_order(V,variables,budget)
    if order is None:raise UnsupportedDomain('nonperiodic algebraic shift over a nonrational PiSigma tower needs general coupled PLDE')
    constants=[v.T for v in (V.T-s.eye(rank)).nullspace()]
    expanded=[list(c*algebra.multiplication(algebra.normal(f))) for f in rhs for c in constants]
    width=len(expanded)
    iterated=[]
    for row in expanded:
        row=s.Matrix([row]);total=s.zeros(1,rank)
        for j in range(order):
            total+=row.applyfunc(lambda v:tower.sigma(v,j=j))*V**j
        iterated.append(list(total.applyfunc(s.cancel)))
    lifted=PiSigma(budget,base_ratio=q**order)
    lifted.nodes=[(t,k,s.cancel(tower.sigma(t,j=order)-t) if k=='sum' else s.cancel(tower.sigma(t,j=order)/t)) for t,k,v in tower.nodes]
    basis=[(tuple(s.Integer(i==j) for i in range(width)),s.zeros(1,rank)) for j in range(width)]
    for coordinate in range(rank):
        targets=[s.cancel(sum(c*f[coordinate] for c,f in zip(cs,iterated))) for cs,g in basis]
        solutions=lifted.solve(1,-1,targets)
        updated=[]
        for weights,g in solutions:
            cs=tuple(s.cancel(sum(w*b[0][j] for w,b in zip(weights,basis))) for j in range(width))
            row=sum((w*b[1] for w,b in zip(weights,basis)),s.zeros(1,rank));row[coordinate]+=g
            updated.append((cs,row.applyfunc(s.cancel)))
        basis=updated
    residuals=[list((g.applyfunc(tower.sigma)*V-g-
                     sum((c*s.Matrix([f]) for c,f in zip(cs,expanded)),s.zeros(1,rank))).applyfunc(s.cancel)) for cs,g in basis]
    answer=[]
    for weights in constant_kernel(residuals,variables,rank):
        cs=[s.cancel(sum(w*b[0][j] for w,b in zip(weights,basis))) for j in range(width)]
        g=sum((w*b[1] for w,b in zip(weights,basis)),s.zeros(1,rank))
        coefficients=[algebra.expression(sum((cs[i*len(constants)+j]*c for j,c in enumerate(constants)),s.zeros(1,rank))) for i in range(len(rhs))]
        answer.append((coefficients,algebra.expression(g)))
    return answer,dict(algorithm='finite automorphism unrolling and original-equation constraint',
                       automorphism_order=order,constant_basis=[str(algebra.expression(c)) for c in constants],
                       scalar_reduction_trace=lifted.trace)


def split_components(algebra):
    """All rational components, or None if an irreducible extension is needed."""
    components=[{}]
    for z,relation in zip(algebra.variables,algebra.relations):
        updated=[]
        for values in components:
            poly=s.Poly(s.cancel(relation.xreplace(values)),z)
            unit,factors=poly.factor_list()
            if any(f.degree()!=1 or m!=1 for f,m in factors):return None
            for f,m in factors:updated.append({**values,z:s.cancel(-f.nth(0)/f.nth(1))})
        components=updated
    return components if len(components)==len(algebra.basis) else None


def component_solve(algebra,parsed,rhs,components,budget,A=s.Integer(1),B=s.Integer(-1)):
    """Interlaced component fields, including free shifts depending on signs."""
    free=[(X,'product',q),*parsed];variables=[t for t,k,v in free]
    maps=[];inverses=[]
    for values in components:
        forward={};inverse={};earlier=set()
        for t,k,v in free:
            a=s.cancel(v.xreplace(values))
            if a.free_symbols&(set(variables)-earlier):raise UnsupportedDomain('component shift is not triangular PiSigma')
            forward[t]=t+a if k=='sum' else t*a
            inverse[t]=s.cancel(t-a.xreplace(inverse)) if k=='sum' else s.cancel(t/a.xreplace(inverse))
            earlier.add(t)
        maps.append(forward);inverses.append(inverse)
    permutation=[]
    for i,values in enumerate(components):
        images=[s.cancel(v.xreplace(values)) for v in algebra.images]
        choices=[j for j,target in enumerate(components)
                 if all(s.cancel(target[z].xreplace(maps[i])-v)==0 for z,v in zip(algebra.variables,images))]
        if len(choices)!=1:raise ValueError('component shift is not a unique permutation')
        permutation.append(choices[0])
    if sorted(permutation)!=list(range(len(components))):raise ValueError('component map is not a permutation')
    evaluation=s.Matrix([[s.cancel(b.xreplace(c)) for b in algebra.basis] for c in components])
    inverse_evaluation=evaluation.inv()
    def restore(values):return algebra.expression(inverse_evaluation*s.Matrix(values))
    rhs_components=[[s.cancel(algebra.normal(f).xreplace(c)) for f in rhs] for c in components]
    coefficients=[(s.cancel(algebra.normal(A).xreplace(c)),s.cancel(algebra.normal(B).xreplace(c))) for c in components]
    if any(a==0 for a,b in coefficients):raise UnsupportedDomain('component operator with a vanishing leading coefficient requires singular-system solving')
    ratios=[s.cancel(-b/a) for a,b in coefficients]
    forcing=[[s.cancel(f/a) for f in row] for row,(a,b) in zip(rhs_components,coefficients)]
    pending=set(range(len(components)));answer=[];traces=[]
    while pending:
        start=min(pending);cycle=[start];next_index=permutation[start]
        while next_index!=start:cycle.append(next_index);next_index=permutation[next_index]
        pending-=set(cycle)
        accumulated={t:t for t in variables};targets=[s.Integer(0)]*len(rhs);multiplier=s.Integer(1)
        for component in cycle:
            ratio=s.cancel(ratios[component].xreplace(accumulated))
            targets=[s.cancel(ratio*f+g.xreplace(accumulated)) for f,g in zip(targets,forcing[component])]
            multiplier=s.cancel(ratio*multiplier)
            accumulated={t:s.cancel(maps[component][t].xreplace(accumulated)) for t in variables}
        lifted=PiSigma(budget,base_ratio=q**len(cycle))
        lifted.occupied|={str(z) for f in [*targets,*accumulated.values()] for z in f.free_symbols}
        for t,k,v in parsed:
            increment=s.cancel(accumulated[t]-t) if k=='sum' else s.cancel(accumulated[t]/t)
            if not lifted.add(t,k,increment) or lifted.torsion:
                raise UnsupportedDomain('component field needs further algebraic constant normalization')
        basis=lifted.solve(1,-s.cancel(multiplier.xreplace(lifted.aliases)),[s.cancel(f.xreplace(lifted.aliases)) for f in targets])
        definitions={}
        for c,v in lifted.constants.items():definitions[c]=s.cancel(v.xreplace(definitions))
        for cs,g in basis:
            cs=[s.cancel(c.xreplace(definitions)) for c in cs];g=s.cancel(g.xreplace(definitions))
            cvalues=[[s.Integer(0)]*len(components) for f in rhs];gvalues=[s.Integer(0)]*len(components)
            current_cs=cs;current_g=g
            for component in cycle:
                for j,c in enumerate(current_cs):cvalues[j][component]=c
                gvalues[component]=current_g
                current_g=s.cancel((ratios[component]*current_g+sum(c*f for c,f in zip(current_cs,forcing[component]))).xreplace(inverses[component]))
                current_cs=[s.cancel(c.xreplace(inverses[component])) for c in current_cs]
            if any(s.cancel(a-b)!=0 for a,b in zip(cs,current_cs)) or s.cancel(g-current_g)!=0:
                raise ArithmeticError('component cycle did not close')
            answer.append(([restore(v) for v in cvalues],restore(gvalues)))
        traces.append(dict(cycle=cycle,unrolled_multiplier=str(multiplier),unrolled_shift={str(t):str(v) for t,v in accumulated.items()},
                           scalar_trace=lifted.trace,constant_definitions={str(c):str(v) for c,v in definitions.items()}))
    return answer,dict(algorithm='rational idempotent components and interlaced PiSigma field solve',
                       components=[{str(z):str(v) for z,v in c.items()} for c in components],permutation=permutation,cycles=traces)


def coupled_solve(algebra,tower,rhs,budget,A=s.Integer(1),B=s.Integer(-1)):
    """Solve for the certificate AND invariant finite-algebra coefficients."""
    from qpisigma_system import solve
    d=algebra.V.rows;width=len(rhs);size=d*(width+1)
    if size>budget.max_states:raise OreResourceLimit('augmented algebraic constant-space system exceeds state budget')
    MA=algebra.multiplication(algebra.normal(A));MB=algebra.multiplication(algebra.normal(B))
    if s.cancel(MA.det())==0 or s.cancel(MB.det())==0:
        raise UnsupportedDomain('nonsplit singular operator needs singular coupled-system solving')
    inverse=MB.inv();W=s.zeros(size);W[:d,:d]=-algebra.V*MA*inverse
    for i,f in enumerate(rhs):
        row=slice(d*(i+1),d*(i+2));W[row,row]=algebra.V
        W[row,:d]=algebra.V*algebra.multiplication(algebra.normal(f))*inverse
    pairs,trace=solve(tower,W,[[s.Integer(0)]*size]);answer=[]
    for dummy,row in pairs:
        if not any(row):continue
        answer.append(([algebra.expression(row[d*(i+1):d*(i+2)]) for i in range(width)],algebra.expression(row[:d])))
    return answer,dict(algorithm='augmented coupled PiSigma system including invariant coefficients',system=trace)


def additive_gauge(algebra,value,prefix,budget):
    """Reduce an algebraic increment modulo exact rational differences.

    Fixed algebraic basis elements turn scalar cohomology relations into an
    affine gauge u*T+v. A one-dimensional residual quotient suffices, even
    when the raw increment has several independent rational coordinates.
    """
    coordinates=algebra.vector(value)
    if all(algebra.normal(algebra.sigma(b)-b)==0 for b in algebra.basis):
        from qpisigma_system import build_tower
        tower=build_tower(prefix,coordinates,budget)
        definitions=dict(tower.generated_definitions)
        for c,v in tower.constants.items():definitions[c]=s.cancel(v.xreplace(definitions))
        def equation(targets):
            targets=[s.cancel(v.xreplace(tower.aliases)) for v in targets]
            return [(tuple(s.cancel(c.xreplace(definitions)) for c in cs),s.cancel(g.xreplace(definitions)))
                    for cs,g in tower.solve(1,-1,targets)]
        residual=None;offset=s.Integer(0);unit=s.Integer(0)
        for b,r in zip(algebra.basis,coordinates):
            if r==0:continue
            if residual is None:
                pair=next(((cs,g) for cs,g in equation([r]) if cs[0]!=0),None)
                if pair:offset+=b*pair[1]/pair[0][0]
                else:residual=r;unit=b
            else:
                pair=next(((cs,g) for cs,g in equation([r,residual]) if cs[0]!=0),None)
                if pair is None:raise UnsupportedDomain('algebraic increment has a cohomology quotient of dimension greater than one; general algebraic coefficient-field PLDE is required')
                cs,g=pair;offset+=b*g/cs[0];unit-=b*cs[1]/cs[0]
        if residual is None:return s.Integer(1),algebra.normal(offset),s.Integer(0)
        unit=algebra.normal(unit)
        if algebra.multiplication(unit).det()!=0:return unit,algebra.normal(offset),residual
    # Fast rank-one case also covers an invariant unit in a nontrivial finite
    # automorphism. All equalities are rechecked after building the new algebra.
    pivot=next((r for r in coordinates if r!=0),None)
    if pivot is None:return s.Integer(1),s.Integer(0),s.Integer(0)
    unit=algebra.normal(value/pivot)
    free={X,*[t for t,k,v in prefix]}
    if not unit.free_symbols&free and algebra.normal(algebra.sigma(unit)-unit)==0 and algebra.multiplication(unit).det()!=0:
        return unit,s.Integer(0),pivot
    raise UnsupportedDomain('algebraic increment does not admit the current invertible affine rationalizing gauge')


def multiplicative_gauge(algebra,value,prefix,budget):
    """Construct a finite-algebra unit gauge using exact homogeneous systems.

    Candidate rational ratios are input coordinates and 1; failure here is
    unsupported, never a claim of nonsummability. A successful gauge gives a
    bijection and hence preserves the completeness of the subsequent solver.
    """
    from qpisigma_system import build_tower,solve
    # Preserve the input's factor representation before reducing modulo the
    # algebraic ideal. A rational coboundary may have an algebraic linear
    # denominator whose norm would hide the gauge in the regular matrix.
    units=list(algebra.basis)
    for part in s.fraction(s.cancel(value)):
        units.append(part)
        for factor,power in s.factor_list(part)[1]:units.append(factor**power)
    for candidate in units:
        candidate=algebra.normal(candidate)
        if candidate==0 or algebra.multiplication(candidate).det()==0:continue
        ratio=algebra.normal(value*candidate/algebra.sigma(candidate))
        if not ratio.free_symbols&set(algebra.variables):return candidate,s.Integer(0),ratio
    value=algebra.normal(value)
    tower=build_tower(prefix,[value],budget)
    if tower.aliases:raise UnsupportedDomain('multiplicative algebraic gauge requires normalized preceding free variables')
    candidates=list(dict.fromkeys([s.Integer(1),*[v for v in algebra.vector(value) if v!=0]]))
    for ratio in candidates:
        matrix=algebra.V*algebra.multiplication(algebra.normal(ratio/value))
        try:pairs,trace=solve(tower,matrix,[[s.Integer(0)]*matrix.rows])
        except UnsupportedDomain:continue
        vectors=[algebra.expression(g) for cs,g in pairs if any(g)]
        if not vectors:continue
        # det(M(sum a_i*h_i)) has degree at most d. On a_i=t^i, a
        # nonzero determinant has at most d*(m-1) roots. This family need
        # not hit every unit subspace, so verify and keep a negative result
        # classified as an unsupported gauge, never as a no-solution result.
        bound=algebra.V.rows*max(0,len(vectors)-1)+1
        if bound>budget.max_unknowns:raise OreResourceLimit('unit gauge construction exceeds budget')
        for number in range(1,bound+1):
            unit=algebra.normal(sum(s.Integer(number)**i*v for i,v in enumerate(vectors)))
            if algebra.multiplication(unit).det()!=0:
                return unit,s.Integer(0),ratio
    raise UnsupportedDomain('nonsplit algebraic product ratio needs general algebraic coefficient-field multiplicative normalization')


def gauge_free_tower(algebra,parsed,rhs,A,B,budget):
    """Exact triangular change t=u*T for invariant algebraic units u.

    This is a bijective change inside the input algebra, with explicit inverse;
    no auxiliary sums or guessed initial values are introduced. If one step
    cannot be rationalized, it is rejected, not classified as unsummable.
    """
    names={str(z) for z in algebra.shift}|{str(z) for f in [A,B,*rhs,*algebra.relations] for z in s.sympify(f).free_symbols}
    generated=[]
    for _ in parsed:
        index=0
        while 'FGauge'+str(index) in names:index+=1
        symbol=s.Symbol('FGauge'+str(index));names.add(str(symbol));generated.append(symbol)
    algebra=FiniteAlgebra(list(zip(algebra.variables,algebra.relations,algebra.images)),
                          {t:v for t,v in algebra.shift.items() if t not in algebra.variables},budget,
                          set(algebra.field.symbols)|set(generated))
    source_vars={X,*[t for t,k,v in parsed]};forward={};backward={};new=[];witnesses=[]
    for (t,kind,value),symbol in zip(parsed,generated):
        raw_value=s.cancel(value.xreplace(forward));value=algebra.normal(raw_value);gauge=s.Integer(1);offset=s.Integer(0)
        if value.free_symbols&set(algebra.variables):
            prefix_algebra=FiniteAlgebra([(z,s.cancel(p.xreplace(forward)),algebra.normal(v.xreplace(forward)))
                                        for z,p,v in zip(algebra.variables,algebra.relations,algebra.images)],
                                       {X:q*X,**{u:u+a if k=='sum' else u*a for u,k,a in new}},budget,
                                       set(algebra.field.symbols))
            gauge,offset,value=(additive_gauge if kind=='sum' else multiplicative_gauge)(prefix_algebra,value if kind=='sum' else raw_value,new,budget)
        forward[t]=algebra.normal(gauge*symbol+offset)
        backward[symbol]=algebra.normal(((t-offset)/gauge).xreplace(backward))
        new.append((symbol,kind,value))
        witnesses.append(dict(original=str(t),new=str(symbol),unit=str(gauge),offset=str(offset),inverse=str(backward[symbol])))
    transformed_relations=[(z,s.cancel(p.xreplace(forward)),
                            algebra.normal(v.xreplace(forward))) for z,p,v in zip(algebra.variables,algebra.relations,algebra.images)]
    targets=[algebra.normal(v.xreplace(forward)) for v in [A,B,*rhs]]
    transformed=FiniteAlgebra(transformed_relations,{X:q*X,**{t:t+v if k=='sum' else t*v for t,k,v in new}},budget,
                              set().union(*(v.free_symbols for v in targets)))
    for t,kind,value in parsed:
        original_image=algebra.shift[t].xreplace(forward)
        if transformed.normal(transformed.sigma(forward[t])-original_image)!=0:
            raise ArithmeticError('algebraic gauge does not intertwine the original shift')
        if algebra.normal(forward[t].xreplace(backward)-t)!=0:raise ArithmeticError('algebraic gauge inverse residual')
    return transformed,new,targets,backward,witnesses


def split_additive_solve(algebra,parsed,rhs,budget,A,B):
    """Constant-field descent for a final algebraic Sigma extension.

    Write beta = Delta(v)+sum(u_j*r_j), with independent rational summation
    classes r_j and algebraic constants u_j. Embed H=v+sum(u_j*T_j) in the
    constant-preserving tower Delta(T_j)=r_j. The original field is precisely
    the common kernel of u_p*d/dT_j-u_j*d/dT_p. Restrict the complete solution
    space by these exact linear constraints, then retract to H.
    """
    from qpisigma_system import build_tower,constant_nullspace
    t,kind,increment=parsed[-1];prefix=parsed[:-1];algvars=set(algebra.variables)
    if kind!='sum' or any(v.free_symbols&algvars for u,k,v in prefix):
        raise UnsupportedDomain('algebraic additive descent currently requires a final Sigma extension over a rational preceding tower')
    if any(v!=z for z,v in zip(algebra.variables,algebra.images)) or any(p.free_symbols&{X,*[u for u,k,v in parsed]} for p in algebra.relations):
        raise UnsupportedDomain('algebraic additive descent requires a fixed finite constant algebra')
    tower=build_tower(prefix,[A,B,*rhs,increment,*algebra.relations],budget)
    if tower.aliases:raise UnsupportedDomain('normalize preceding constants before algebraic additive descent')
    residuals=[];units=[];offset=s.Integer(0)
    for b,r in zip(algebra.basis,algebra.vector(increment)):
        if r==0:continue
        pairs=tower.solve(1,-1,[r,*residuals])
        pair=next(((cs,g) for cs,g in pairs if cs[0]!=0),None)
        if pair is None:residuals.append(r);units.append(b)
        else:
            cs,g=pair;offset+=b*g/cs[0]
            units=[algebra.normal(u-b*c/cs[0]) for u,c in zip(units,cs[1:])]
    if len(residuals)<2:raise UnsupportedDomain('additive descent expected more than one residual summation class')
    pivot=next((i for i,u in enumerate(units) if algebra.multiplication(u).det()!=0),None)
    if pivot is None:raise UnsupportedDomain('additive descent needs a unit coordinate or further idempotent splitting')
    occupied=tower.occupied|{str(z) for z in algebra.variables};symbols=[]
    for _ in residuals:
        index=0
        while 'FAdd'+str(index) in occupied:index+=1
        z=s.Symbol('FAdd'+str(index));occupied.add(str(z));symbols.append(z)
    new=[*prefix,*[(z,'sum',r) for z,r in zip(symbols,residuals)]]
    image=offset+sum(u*z for u,z in zip(units,symbols));forward={t:image}
    definitions=list(zip(algebra.variables,algebra.relations,algebra.images))
    targets=[s.cancel(v.xreplace(forward)) for v in [A,B,*rhs]]
    larger=FiniteAlgebra(definitions,{X:q*X,**{u:u+v if k=='sum' else u*v for u,k,v in new}},budget,
                         set().union(*(v.free_symbols for v in targets)))
    if larger.normal(larger.sigma(image)-image-increment)!=0:raise ArithmeticError('additive embedding shift residual')
    pairs,trace=free_solve(larger,new,targets[2:],budget,*targets[:2])
    constraints=[]
    for cs,g in pairs:
        row=[]
        for j,z in enumerate(symbols):
            if j==pivot:continue
            for v in [*cs,g]:
                row.extend(larger.vector(units[pivot]*s.diff(v,z)-units[j]*s.diff(v,symbols[pivot])))
        constraints.append(row)
    answer=[];variables=[X,*[u for u,k,v in new]]
    section={z:s.Integer(0) for z in symbols};section[symbols[pivot]]=algebra.normal((t-offset)/units[pivot])
    for weights in constant_nullspace(constraints,variables,len(constraints[0]) if constraints else 0):
        cs=[larger.normal(sum(w*p[0][i] for w,p in zip(weights,pairs))) for i in range(len(rhs))]
        g=larger.normal(sum(w*p[1] for w,p in zip(weights,pairs)))
        cs=[algebra.normal(c.xreplace(section)) for c in cs];g=algebra.normal(g.xreplace(section))
        answer.append((cs,g))
    return answer,dict(algorithm='constant-preserving additive embedding and differential descent',
                       original=str(t),image=str(image),residual_basis=list(map(str,residuals)),
                       algebraic_coefficients=list(map(str,units)),offset=str(offset),pivot=pivot,
                       retraction={str(z):str(v) for z,v in section.items()},system=trace)


def free_solve(algebra,parsed,rhs,budget,A=s.Integer(1),B=s.Integer(-1)):
    components=split_components(algebra)
    if components is not None:return component_solve(algebra,parsed,rhs,components,budget,A,B)
    if any(v.free_symbols&set(algebra.variables) for t,k,v in parsed):
        try:transformed,new,targets,backward,witnesses=gauge_free_tower(algebra,parsed,rhs,A,B,budget)
        except UnsupportedDomain as exc:
            from qnumberfield import fixed_constant_solve,periodic_constant_solve
            try:native=fixed_constant_solve(algebra,parsed,rhs,budget,A,B)
            except UnsupportedDomain:native=periodic_constant_solve(algebra,parsed,rhs,budget,A,B)
            if native is None:native=periodic_constant_solve(algebra,parsed,rhs,budget,A,B)
            if native is not None:return native
            if 'cohomology quotient' in str(exc):return split_additive_solve(algebra,parsed,rhs,budget,A,B)
            raise
        pairs,trace=free_solve(transformed,new,targets[2:],budget,*targets[:2])
        pairs=[([algebra.normal(c.xreplace(backward)) for c in cs],algebra.normal(g.xreplace(backward))) for cs,g in pairs]
        return pairs,dict(algorithm='invertible algebraic coefficient gauge followed by exact coupled solve',gauges=witnesses,system=trace)
    from qpisigma_system import build_tower
    tower=build_tower(parsed,[A,B,*rhs,*algebra.relations,*algebra.images],budget)
    if tower.aliases:
        normalized=lambda f:s.cancel(f.xreplace(tower.aliases))
        new=list(tower.nodes[1:]);targets=list(map(normalized,[A,B,*rhs]))
        transformed=FiniteAlgebra([(z,normalized(p),normalized(v)) for z,p,v in zip(algebra.variables,algebra.relations,algebra.images)],
                                  {X:q*X,**{t:t+v if k=='sum' else t*v for t,k,v in new}},budget,
                                  set().union(*(v.free_symbols for v in targets)))
        pairs,trace=free_solve(transformed,new,targets[2:],budget,*targets[:2])
        definitions=dict(tower.generated_definitions)
        for c,v in tower.constants.items():definitions[c]=s.cancel(v.xreplace(definitions))
        pairs=[([algebra.normal(c.xreplace(definitions)) for c in cs],algebra.normal(g.xreplace(definitions))) for cs,g in pairs]
        return pairs,dict(algorithm='free constant normalization inside the finite algebra',definitions={str(k):str(v) for k,v in definitions.items()},system=trace)
    if (A,B)==(1,-1) and finite_order(algebra.V,[t for t,k,v in tower.nodes],budget) is not None:
        return periodic_solve(algebra,tower,rhs,budget)
    return coupled_solve(algebra,tower,rhs,budget,A,B)


def inverse_shift(algebra,parsed,value):
    """Invert the input automorphism in two exact triangular configurations."""
    algebraic=set(algebra.variables);free={X,*[t for t,k,v in parsed]}
    inverse={X:X/q}
    if not any(v.free_symbols&algebraic for t,k,v in parsed):
        for t,kind,v in parsed:
            v=v.xreplace(inverse);inverse[t]=t-v if kind=='sum' else t/v
        row=s.Matrix([algebra.vector(value)])*algebra.V.inv()
        result=algebra.expression([s.cancel(v.xreplace(inverse)) for v in row])
    elif not any(v.free_symbols&free for v in algebra.V):
        matrix=algebra.V.inv()
        inverse.update({z:algebra.expression(s.Matrix([algebra.vector(z)])*matrix) for z in algebra.variables})
        for t,kind,v in parsed:
            v=algebra.normal(v.xreplace(inverse));inverse[t]=t-v if kind=='sum' else t/v
        result=algebra.normal(value.xreplace(inverse))
    else:raise UnsupportedDomain('inverse mixed automorphism requires further algebraic triangularization')
    if algebra.normal(algebra.sigma(result)-value)!=0:raise ArithmeticError('inverse finite-algebra shift residual')
    return result


def prepare(data,budget,parse):
    if not isinstance(data,dict) or set(data) not in ({'extensions','algebraic_extensions','rhs_basis'},{'extensions','algebraic_extensions','rhs_basis','operator'}):
        raise ValueError('finite_difference_ring requires extensions, algebraic_extensions and rhs_basis')
    parsed,rhs,A,B=parse_problem({k:data[k] for k in ('extensions','rhs_basis','operator') if k in data},budget,parse)
    rows=data['algebraic_extensions']
    if not isinstance(rows,list) or not rows:raise ValueError('nonempty algebraic extension list required')
    names={str(t) for t,k,v in parsed}|{'X','q','Q','n','k'};algebraic=[]
    occupied=names|{str(v) for f in rhs for v in f.free_symbols}|{str(row.get('name')) for row in rows if isinstance(row,dict)}
    expanded=[]
    for row in rows:
        if isinstance(row,dict) and row.get('kind')=='root_unity':
            if set(row)!={'name','kind','order'} or type(row['order']) is not int or row['order']<1:
                raise ValueError('root_unity requires name and positive integer order')
            order=row['order'];name=row['name']
            if not isinstance(name,str) or not re.fullmatch('[A-Za-z][A-Za-z0-9_]*',name):raise ValueError('valid root-unity name required')
            if order*int(s.totient(order))>budget.max_states:raise OreResourceLimit('root-of-unity algebra exceeds state budget')
            z=s.Symbol(name)
            if order<=2:multiplier=s.Integer(1 if order==1 else -1)
            else:
                index=0
                while 'FRoot'+str(index) in occupied:index+=1
                multiplier=s.Symbol('FRoot'+str(index));occupied.add(str(multiplier))
                expanded.append((multiplier,s.cyclotomic_poly(order,multiplier),multiplier))
            expanded.append((z,z**order-1,multiplier*z))
        else:expanded.append(row)
    rows=expanded
    for row in rows:
        if isinstance(row,tuple):
            z,p,v=row
            if str(z) in names:raise ValueError('duplicate or reserved algebraic variable')
            names.add(str(z));algebraic.append((z,p,v));continue
        if not isinstance(row,dict) or set(row)!={'name','polynomial','shift'}:raise ValueError('algebraic name, polynomial and shift required')
        name=row['name']
        if not isinstance(name,str) or not re.fullmatch('[A-Za-z][A-Za-z0-9_]*',name) or name in names:raise ValueError('unique algebraic variable name required')
        names.add(name);algebraic.append((s.Symbol(name),parse(row['polynomial']),parse(row['shift'])))
    algebraic_names={z for z,p,v in algebraic}
    dependent=any(v.free_symbols&algebraic_names for t,k,v in parsed)
    field_for([*rhs,*[v for z,p,v in algebraic],*[p for z,p,v in algebraic]],X,q)
    algebra=FiniteAlgebra(algebraic,{X:q*X,**{t:t+v if k=='sum' else t*v for t,k,v in parsed}},budget,
                          set().union(*(f.free_symbols for f in [A,B,*rhs])))
    for t,kind,value in parsed:
        value=algebra.normal(value)
        if kind=='product' and algebra.multiplication(value).det()==0:
            raise ValueError('nonunit product ratio does not define an invertible free extension')
    A,B=map(algebra.normal,(A,B))
    if A==B==0:raise ValueError('nonzero operator in the finite algebra required')
    return parsed,rhs,A,B,algebra


def compute(data,budget,parse):
    parsed,rhs,A,B,algebra=prepare(data,budget,parse)
    if A==0 or B==0:
        factor=B if A==0 else A
        if algebra.multiplication(factor).det()==0:raise UnsupportedDomain('singular multiplication operator over a finite algebra')
        answer=[]
        for j,f in enumerate(rhs):
            g=algebra.normal(f/factor)
            if B==0:g=inverse_shift(algebra,parsed,g)
            answer.append(([s.Integer(i==j) for i in range(len(rhs))],g))
        trace=dict(algorithm='invertible one-term operator',basis_over_full_invariants=True)
    elif not parsed:
        answer,trace=coupled_solve(algebra,PiSigma(budget),rhs,budget,A,B)
    else:
        answer,trace=free_solve(algebra,parsed,rhs,budget,A,B)
    def encode(cs,g):
        allowed=set(algebra.field.symbols)|set(algebra.variables)
        if any(s.sympify(v).free_symbols-allowed for v in [*cs,g]):raise ArithmeticError('unrestored symbol in finite-algebra certificate')
        if any(algebra.normal(algebra.sigma(c)-c)!=0 for c in cs):raise ArithmeticError('algebraic coefficient not invariant')
        if algebra.normal(A*algebra.sigma(g)+B*g-sum(c*f for c,f in zip(cs,rhs)))!=0:raise ArithmeticError('algebraic certificate residual')
        units=[]
        for i,c in enumerate(cs):
            if c!=0 and algebra.multiplication(c).det()!=0:units.append(i)
        return dict(coefficients=list(map(str,cs)),certificate=str(g),residual='0',unit_coefficient_indices=units)
    result=dict(solution_basis=[encode(cs,g) for cs,g in answer],reduction_trace=trace,
                basis_field=('full invariant ring of the input automorphism' if trace.get('basis_over_full_invariants') else
                             'component invariant constant fields; a generating system over their product ring'
                             if 'components' in trace else
                             'QQ(q,independent parameters); coefficients may lie in the full invariant finite algebra'))
    candidate=next(((cs,g) for cs,g in answer if any(c!=0 for c in cs)),None)
    if candidate:result.update(encode(*candidate))
    return dict(status='constructed' if candidate else 'no_relation_in_declared_basis',solver='finite_difference_ring',
        result=result,algebra=dict(basis=list(map(str,algebra.basis)),relations=list(map(str,algebra.relations)),
                                 shift_matrix=[[str(v) for v in algebra.V.row(j)] for j in range(algebra.V.rows)]),
        domain=dict(defining_relations_are_input_objects=True,denominator_policy='unit check in the finite reduced quotient',
                    nonunit_coefficients_do_not_isolate_a_summand=True,
                    completeness='full constant-coefficient solution space in the admitted finite algebra',
                    excluded='algebraic function constant fields without admitted normalization; uncertified constant-changing towers; singular nonsplit operators',
                    obligations='source semantics, initial values, parameter specializations and Lean remain external'))
