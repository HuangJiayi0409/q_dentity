"""Division-free common-interval normalization of shifted finite products.

Plans are algebraic candidates. Every length and argument equality remains a
Lean obligation; in particular a negative formal length is never assumed valid.
"""
from dataclasses import dataclass
from functools import lru_cache
import sympy as s
from expressions import n,k,q,Q,X,Poch,rationalize

@dataclass(frozen=True)
class Interval:
    atom: object
    base: object
    unit: object
    start: int
    length_base: object
    length_offset: int


def interval(atom):
    a,b,l=atom.args
    stride=b.as_powers_dict().get(q,s.S.Zero)
    if not stride.is_Integer or stride<=0 or b!=q**stride:
        raise ValueError('proof_representation_gap: positive integral q-power base required')
    a=s.factor(a)
    # Only extract a literal integer q exponent. Dependence on n,k remains in
    # the unit and is matched exactly after rational normalization.
    rat=s.factor(rationalize(a))
    start=rat.as_powers_dict().get(q,s.S.Zero)
    if not start.is_Integer:start=s.S.Zero
    start=s.floor(start/stride)
    unit=s.cancel(rat/b**start)
    poly=s.Poly(s.expand(l),n,k)
    constant=poly.coeff_monomial(1)
    if not constant.is_Integer:raise ValueError('proof_representation_gap: integral product length required')
    return Interval(atom,b,unit,int(start),s.expand(l-constant),int(constant))



def compact(value, operation=s.cancel):
    """Compute with q^n,q^k as indeterminates, retaining opaque products.

    This is candidate algebra only: emitted identities are checked by Lean.
    Keeping a finite rational alphabet avoids exponential expansion of the
    same denominator under many syntactically different affine exponents.
    """
    opaque = sorted(value.atoms(Poch), key=s.default_sort_key)
    forward = {a:s.Dummy('product') for a in opaque}
    result = value.xreplace(forward)
    powers={}
    def power(t):
        poly=s.Poly(s.expand(t.exp),n,k)
        linear=sum(c*n**i*k**j for (i,j),c in poly.terms() if i+j<=1)
        nonlinear=s.expand(t.exp-linear)
        if nonlinear==0:return rationalize(t)
        atom=q**nonlinear
        if atom not in powers:powers[atom]=s.Dummy('nonlinear_power')
        return powers[atom]*rationalize(q**linear)
    result = result.replace(
        lambda t:t.is_Pow and t.base==q and t.exp.has(n,k),
        power)
    result = operation(result)
    return result.subs({Q:q**n,X:q**k}).xreplace({v:a for a,v in {**forward,**powers}.items()})


def plan(expressions):
    return _plan(tuple(expressions))


@lru_cache(maxsize=128)
def _plan(expressions):
    atoms=sorted(set().union(*(x.atoms(Poch) for x in expressions)),key=s.default_sort_key)
    groups={}
    for atom in atoms:
        data=interval(atom)
        groups.setdefault((data.base,data.unit,data.length_base),[]).append(data)
    rewrites={};rows=[];cores={}
    for number,((base,unit,length_base),group) in enumerate(groups.items()):
        start=max(row.start for row in group)
        end=min(row.start+row.length_offset for row in group)
        core_length=s.expand(length_base+end-start)
        core_start=(unit*base**start).subs({Q:q**n,X:q**k})
        core=Poch(core_start,base,core_length)
        symbol=s.Symbol('pc'+str(number));cores[symbol]=core
        for row in group:
            prefix=start-row.start
            suffix=row.start+row.length_offset-end
            original_start=row.atom.args[0]
            front=s.prod(1-original_start*base**j for j in range(prefix))
            back=s.prod(1-core_start*base**(core_length+j) for j in range(suffix))
            replacement=front*symbol*back
            rewrites[row.atom]=replacement
            rows.append(dict(atom=row.atom,core=core,symbol=symbol,prefix=prefix,suffix=suffix,
                             replacement=replacement))
    rewritten=[x.xreplace(rewrites) for x in expressions]
    return dict(rows=rows,cores=cores,rewritten=rewritten,
                normalized=[compact(x) for x in rewritten])


def backward_certificate(F,R):
    """G(k+1)=B(k)F(k), with removable endpoint factors canceled symbolically."""
    from expressions import shift_ratio
    V=rationalize(shift_ratio(F,k))
    return s.cancel(R.subs(X,q*X)*V)
