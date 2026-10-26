"""Bibasic Gosper with simultaneous (X,Y)->(p X,q Y) shift.

Factor-orbit GP normalization and a derived Laurent rectangle, followed by exact
linear algebra. No target, candidate denominator or degree bound is accepted.
The Laurent formulation handles coordinate monomial poles as units.
See branches/bibasic_gosper.md for the original Riese algorithm and scope.
"""
import sympy as s
from qgosper import Budget, UnsupportedDomain
from expressions import expression, shift_ratio, k, n, Poch

p,q,X,Y = s.symbols('p q X Y')


def shift(f, amount=1):
    return f.subs({X:p**amount*X,Y:q**amount*Y}, simultaneous=True)


def base_powers(value):
    """Recognize exactly p**i*q**j over independent formal bases."""
    a,b = [s.Poly(t,p,q,domain='EX') for t in s.fraction(s.cancel(value))]
    if len(a.terms())!=1 or len(b.terms())!=1: return None
    (ma,ca),(mb,cb)=a.terms()[0],b.terms()[0]
    if s.cancel(ca/cb-1)!=0: return None
    return tuple(i-j for i,j in zip(ma,mb))


def dispersion(A,B,field):
    fa=s.Poly(A,X,Y,domain=field).factor_list()[1]
    fb=s.Poly(B,X,Y,domain=field).factor_list()[1]
    shifts=set()
    for f,_ in fa:
        ft=dict(f.terms())
        if len(ft)<2: continue  # Coordinate monomials are Laurent units.
        for g,_ in fb:
            gt=dict(g.terms())
            if set(ft)!=set(gt): continue
            anchor=next(iter(ft)); candidate=None; valid=True
            for m in ft:
                if m==anchor: continue
                pair=base_powers(ft[m]*gt[anchor]/(ft[anchor]*gt[m]))
                delta=tuple(a-b for a,b in zip(m,anchor))
                if pair is None: valid=False;break
                for power,d in zip(pair,delta):
                    if d==0:
                        if power!=0: valid=False
                    elif power % d or power//d < 0: valid=False
                    elif candidate is None: candidate=power//d
                    elif candidate!=power//d: valid=False
                if not valid: break
            if valid and candidate is not None:
                gs=s.Poly(shift(g.as_expr(),candidate),X,Y,domain=field)
                if f.monic()==gs.monic(): shifts.add(candidate)
    return sorted(shifts)


def normal_form(ratio,field):
    A,B=s.fraction(s.cancel(ratio)); P=s.Integer(1)
    shifts=dispersion(A,B,field); updates=[]
    for j in shifts:
        d=s.gcd(s.Poly(A,X,Y,domain=field),s.Poly(shift(B,j),X,Y,domain=field)).monic().as_expr()
        if not d.has(X,Y): continue
        A=s.cancel(A/d);B=s.cancel(B/shift(d,-j))
        P=s.expand(P*s.prod(shift(d,-i) for i in range(j)))
        updates.append({'shift':j,'factor':str(d)})
    if s.cancel(ratio-P/shift(P,-1)*A/B)!=0 or dispersion(A,B,field):
        raise ArithmeticError('bibasic GP invariant failed')
    return P,A,B,{'dispersion':shifts,'updates':updates,'P':str(P),'A':str(A),'B':str(B),
                  'normal_form_residual':'0','remaining_dispersion':[]}


def bounds(P,A,B):
    """Leading/trailing comparison in each coordinate, including resonance.

If equal extreme degrees cancel, comparing the lowest other-coordinate terms
forces a pure p,q monomial ratio. Its current-base exponent fixes the exceptional
degree. Other-coordinate Laurent valuations may be arbitrary integers.
"""
    answer=[]
    for axis,(var,other) in enumerate([(X,Y),(Y,X)]):
        polys=[s.Poly(v,var) for v in (P,A,B)]
        lows=[min(m[0] for m in t.monoms()) for t in polys]
        highs=[t.degree() for t in polys]
        lo=lows[0]-min(lows[1:]);hi=highs[0]-max(highs[1:])
        resonances=[]
        for extreme in (lows,highs):
            resonance=None
            if extreme[1]==extreme[2]:
                ac,bc=[s.Poly(t.nth(extreme[i+1]),other) for i,t in enumerate(polys[1:])]
                av,bv=[min(m[0] for m in t.monoms()) for t in (ac,bc)]
                if av==bv:
                    pair=base_powers(bc.nth(bv)/ac.nth(av))
                    if pair is not None: resonance=pair[axis]-extreme[1]
            resonances.append(resonance)
        if resonances[0] is not None:lo=min(lo,resonances[0])
        if resonances[1] is not None:hi=max(hi,resonances[1])
        answer.append({'variable':str(var),'lower':int(lo),'upper':int(hi),
                       'lower_resonance':resonances[0],'upper_resonance':resonances[1]})
    return answer


def antidifference(down_ratio,budget=Budget()):
    ratio=s.cancel(down_ratio)
    if ratio==0 or ratio.has(s.Float) or not ratio.is_rational_function():
        raise UnsupportedDomain('exact nonzero bibasic rational ratio required')
    field=s.QQ.frac_field(*sorted((ratio.free_symbols|{p,q})-{X,Y},key=str))
    P,A,B,normal=normal_form(ratio,field)
    rectangle=bounds(P,A,B)
    trace={'algorithm':'bibasic Gosper','coefficient_domain':str(field),
           'down_ratio':str(ratio),'normal_form':normal,'laurent_bounds':rectangle,
           'target_used_in_search':False}
    sizes=[max(0,b['upper']-b['lower']+1) for b in rectangle]
    if sizes[0]*sizes[1]>budget.max_unknowns:
        return dict(trace,status='resource_exhausted',reason='derived rectangle exceeds unknown limit')
    if 0 in sizes:
        return dict(trace,status='no_solution_in_derived_laurent_system',reason='empty degree rectangle')
    monomials=[X**i*Y**j for i in range(rectangle[0]['lower'],rectangle[0]['upper']+1)
               for j in range(rectangle[1]['lower'],rectangle[1]['upper']+1)]
    cs=[s.Dummy(f'c{i}') for i in range(len(monomials))]
    f=s.Add(*(a*m for a,m in zip(cs,monomials)))
    eq=s.Poly(s.fraction(s.cancel(shift(A)*f-B*shift(f,-1)-P))[0],X,Y).coeffs()
    trace['linear_system']={'unknowns':len(cs),'equations':len(eq)}
    solution=s.linsolve(eq,cs)
    if solution==s.EmptySet:
        return dict(trace,status='no_solution_in_derived_laurent_system',reason='inconsistent coefficient system')
    solved=s.cancel(f.subs(dict(zip(cs,next(iter(solution)))),simultaneous=True).subs(dict.fromkeys(cs,0)))
    R=s.cancel(B/P*shift(solved,-1))
    if s.cancel(shift(ratio)*shift(R)-R-1)!=0:
        raise ArithmeticError('bibasic certificate residual nonzero')
    return dict(trace,status='constructed',laurent_solution=str(solved),certificate=str(R),rational_residual='0')


def rationalize(expr):
    for base,var in [(p,X),(q,Y)]:
        def convert(t):
            exponent=s.Poly(s.expand(t.exp),k)
            if exponent.degree()>1 or not all(c.is_Integer for c in exponent.all_coeffs()):
                raise UnsupportedDomain('affine integral base exponents required')
            return var**exponent.nth(1)*base**exponent.nth(0)
        expr=expr.replace(lambda t:t.is_Pow and t.base==base and t.exp.has(k),convert)
    result=s.cancel(expr)
    if result.has(k,n,Poch) or not result.is_rational_function():
        raise UnsupportedDomain('not a rational function of the two shift variables')
    return result


def construct(problem,budget):
    if set(problem)!={'schema_version','source_id','summand'} or problem['schema_version']!=1:
        raise ValueError('invalid_problem: only summand and source metadata are accepted')
    F=expression(problem['summand'])
    U=rationalize(shift_ratio(F,k))
    result=antidifference(shift(U,-1),budget)
    return {'shifts':{'k_shift':str(U)},'construction':result}
