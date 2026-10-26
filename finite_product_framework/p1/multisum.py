"""Dimension-independent, bounded rational-certificate creative telescoping.

Searches L F = sum_i Delta_i(R_i F). This is an exact ansatz search, not
a complete multivariate Gosper algorithm. Exhaustion is never unsummability.
Input contains a summand, indices and metadata, never a target or certificate.
"""
from dataclasses import dataclass
from math import comb
import time
import random
from functools import lru_cache
import sympy as s
from expressions import expression, shift_ratio, Poch, n, q, Q
from qgosper import Budget


@dataclass(frozen=True)
class MultisumBudget(Budget):
    max_order: int = 2
    max_degree: int = 2
    max_equations: int = 1500
    max_matrix_terms: int = 20000
    laurent_floor: int = 0


def monomials(dimension, degree):
    """All nonnegative exponent vectors of total degree at most degree."""
    if dimension == 0:
        yield ()
    else:
        for first in range(degree+1):
            for tail in monomials(dimension-1, degree-first):
                yield (first,)+tail


def rationalize(expr, indices, variables):
    def convert(t):
        poly = s.Poly(s.expand(t.exp), n, *indices)
        if poly.total_degree() > 1:
            raise ValueError('representation_gap: nonlinear shift exponent')
        cs = [poly.coeff_monomial(v) for v in (n,)+tuple(indices)]
        cs.append(poly.coeff_monomial(1))
        if not all(c.is_Integer for c in cs):
            raise ValueError('representation_gap: nonintegral shift exponent')
        return Q**cs[0]*s.prod(v**c for v,c in zip(variables,cs[1:-1]))*q**cs[-1]
    result = s.cancel(expr.replace(
        lambda t:t.is_Pow and t.base == q and t.exp.has(n,*indices),convert))
    if result.has(n,*indices,Poch,s.Float) or not result.is_rational_function(*result.free_symbols):
        raise ValueError('representation_gap: nonrational multivariate shift')
    return result


def derive(problem):
    if (set(problem) != {'schema_version','source_id','indices','summand'} or
            problem['schema_version'] != 1):
        raise ValueError('invalid_problem: only summand, indices and source metadata accepted')
    names = problem['indices']
    if (not isinstance(names,list) or not names or
            names != [f'i{i}' for i in range(len(names))]):
        raise ValueError('invalid_problem: canonical ordered indices i0, i1, ... required')
    indices = tuple(s.Symbol(name) for name in names)
    variables = tuple(s.Symbol(f'X{i}') for i in range(len(names)))
    F = expression(problem['summand'])
    if F == 0 or F.has(s.Float):
        raise ValueError('unsupported_structure: nonzero exact summand required')
    U = [rationalize(shift_ratio(F,i),indices,variables) for i in indices]
    V = rationalize(shift_ratio(F,n),indices,variables)
    return variables,V,U


def verify(V,U,variables,coefficients,certificates):
    if len(U) != len(variables) or len(certificates) != len(variables) or not coefficients:
        raise ValueError('invalid_certificate: dimensions')
    if any(c.has(*variables) for c in coefficients) or all(c == 0 for c in coefficients):
        raise ValueError('invalid_certificate: telescoper coefficients')
    if any(e.has(s.Float) or not e.is_rational_function(*e.free_symbols)
           for e in [*coefficients,*certificates]):
        raise ValueError('invalid_certificate: exact rational functions required')
    ratios = [s.Integer(1)]
    for j in range(1,len(coefficients)):
        ratios.append(s.cancel(ratios[-1]*V.subs(Q,q**(j-1)*Q)))
    from exact_linear import flint_available,rational_normal_form
    residual = sum(c*v for c,v in zip(coefficients,ratios)) - sum(
        u*r.subs(x,q*x)-r for u,r,x in zip(U,certificates,variables))
    residual = rational_normal_form(residual) if flint_available() else s.cancel(residual)
    if residual != 0:
        raise ValueError('invalid_certificate: multivariate local residual')
    return ratios


def full_rank_specialization(matrix,parameters,prime=32003):
    """A nonzero specialized maximal minor proves generic column independence.

    Rank deficiency gives NO conclusion. In particular specialization is never
    used to accept a certificate or infer a generic rank deficiency.
    """
    if not matrix or len(matrix)<len(matrix[0]):return None
    assignment={p:2*i+3 for i,p in enumerate(parameters)}
    def evaluate(e):
        if e.is_Rational:return int(e.p)*pow(int(e.q)%prime,-1,prime)%prime
        if e.is_Symbol:return assignment[e]%prime
        if e.is_Add:return sum(evaluate(t) for t in e.args)%prime
        if e.is_Mul:
            v=1
            for t in e.args:v=v*evaluate(t)%prime
            return v
        if e.is_Pow and e.exp.is_Integer:return pow(evaluate(e.base),int(e.exp),prime)
        raise ValueError('unsupported modular coefficient')
    try:rows=[[evaluate(e) for e in row] for row in matrix]
    except (ValueError,KeyError):return None
    pivot=0;permutation=list(range(len(rows)))
    for col in range(len(rows[0])):
        found=next((j for j in range(pivot,len(rows)) if rows[j][col]),None)
        if found is None:return None
        rows[pivot],rows[found]=rows[found],rows[pivot]
        permutation[pivot],permutation[found]=permutation[found],permutation[pivot]
        inverse=pow(rows[pivot][col],-1,prime)
        rows[pivot]=[a*inverse%prime for a in rows[pivot]]
        for j in range(pivot+1,len(rows)):
            factor=rows[j][col]
            if factor:rows[j]=[(a-factor*b)%prime for a,b in zip(rows[j],rows[pivot])]
        pivot+=1
    return {'prime':prime,'parameter_values':{str(p):v for p,v in assignment.items()},
            'minor_rows':permutation[:pivot],'rank':pivot}


def clear_columns(columns):
    """Clear denominators over QQ[all symbols], avoiding nested fraction fields.

    Factor powers are matched exactly. Parameter factors are retained, rather
    than silently specialized away; original-domain lifting remains separate.
    """
    descriptions=[];common={}
    for column in columns:
        numerator,denominator=s.fraction(column)
        content,factors=s.factor_list(denominator)
        powers=dict(factors)
        descriptions.append((numerator,content,powers))
        for factor,power in factors:common[factor]=max(common.get(factor,0),power)
    return [s.expand(numerator/content*s.prod(f**(e-powers.get(f,0)) for f,e in common.items()))
            for numerator,content,powers in descriptions]


def prune_zero_unknowns(rows):
    """Homogeneous singleton equations force exact zero, without divisions."""
    active=list(range(len(rows[0]))) if rows else []
    forced=[]
    while True:
        singles={nonzero[0] for row in rows
                 if len(nonzero:=[i for i in active if row[i]!=0])==1}
        if not singles:break
        forced.extend(sorted(singles))
        active=[i for i in active if i not in singles]
    return active,forced,[[row[i] for i in active] for row in rows if any(row[i]!=0 for i in active)]


def reduce_pair_equations(rows):
    """Exact homogeneous two-term substitutions; returns an expansion matrix."""
    count=len(rows[0]) if rows else 0
    expressions=s.eye(count)
    while rows:
        pair=next(([(i,c) for i,c in enumerate(row) if c!=0] for row in rows
                   if sum(c!=0 for c in row)==2),None)
        if pair is None:break
        (i,a),(j,b)=pair
        if s.count_ops(a)>s.count_ops(b):i,j,a,b=j,i,b,a
        ratio=s.cancel(-b/a)
        # Eliminate i, expressing it in terms of j. Matrix composition keeps
        # enough information to reconstruct and independently verify every R_i.
        keep=[k for k in range(len(rows[0])) if k!=i]
        replacement=s.zeros(len(rows[0]),len(keep))
        for col,k in enumerate(keep):replacement[k,col]=1
        replacement[i,keep.index(j)]=ratio
        expressions=(expressions*replacement).applyfunc(s.cancel)
        new=[]
        for row in rows:
            values=[s.cancel(row[k]+(row[i]*ratio if k==j else 0)) for k in keep]
            if any(v!=0 for v in values):new.append(values)
        rows=new
        # Singleton equations revealed by substitutions can be removed too.
        if rows:
            active,forced,rows=prune_zero_unknowns(rows)
            if forced:expressions=expressions[:,active]
    return rows,expressions


def evaluation_full_rank(columns,variables,parameters,prime=32003):
    """Nonzero evaluation minor implies rational-function column independence.

    Parameters are fixed across rows; only summation variables vary. Never
    infer dependence from failure, and never accept a certificate numerically.
    """
    fixed={p:2*i+3 for i,p in enumerate(parameters)}
    pivots={};points=[]
    generator=random.Random(0)
    for trial in range(2*len(columns)+8):
        point={v:generator.randrange(1,prime) for v in variables}
        values={**fixed,**point}
        @lru_cache(None)
        def ev(e):
            if e.is_Rational:return int(e.p)*pow(int(e.q)%prime,-1,prime)%prime
            if e.is_Symbol:return values[e]
            if e.is_Add:return sum(map(ev,e.args))%prime
            if e.is_Mul:
                a=1
                for t in e.args:a=a*ev(t)%prime
                return a
            if e.is_Pow and e.exp.is_Integer:return pow(ev(e.base),int(e.exp),prime)
            raise ValueError('unsupported coefficient')
        try:row=list(map(ev,columns))
        except (ValueError,KeyError):continue
        for pivot,basis in sorted(pivots.items()):
            a=row[pivot]
            if a:row=[(x-a*y)%prime for x,y in zip(row,basis)]
        pivot=next((i for i,a in enumerate(row) if a),None)
        if pivot is None:continue
        inv=pow(row[pivot],-1,prime)
        pivots[pivot]=[a*inv%prime for a in row]
        points.append([point[v] for v in variables])
        if len(pivots)==len(columns):
            return {'kind':'rational_function_evaluation_minor','prime':prime,
                    'parameters':{str(p):v for p,v in fixed.items()},
                    'variables':list(map(str,variables)),'points':points,'rank':len(pivots)}
    return None


def search(V,U,variables,budget=MultisumBudget()):
    started=time.monotonic()
    attempts=[]
    def stopped(reason,status='resource_exhausted'):
        return {'status':status,'reason':reason,'attempts':attempts,
                'algorithm':'bounded rational multivariate creative telescoping',
                'dimension':len(variables),'target_used_in_search':False,
                'complete_search':False}
    if not variables or len(U)!=len(variables) or len(set(variables))!=len(variables):
        raise ValueError('invalid_problem: dimensions')
    for value in [V,*U]:
        if value.has(s.Float) or not value.is_rational_function(*value.free_symbols):
            raise ValueError('unsupported_domain: exact rational shift ratios required')
    parameters=sorted(set.union(*(e.free_symbols for e in [V,*U]))-set(variables)|{q,Q},key=str)
    field=s.QQ.frac_field(*parameters)
    ratios=[s.Integer(1)]
    denominator_factors={}
    for order in range(1,getattr(budget,'max_order',2)+1):
        ratios.append(s.cancel(ratios[-1]*V.subs(Q,q**(order-1)*Q)))
        for factor,power in s.factor_list(s.fraction(ratios[-1])[1])[1]:
            if factor.has(*variables):denominator_factors[factor]=max(denominator_factors.get(factor,0),power)
        floor=getattr(budget,'laurent_floor',0)
        if type(floor) is not int or floor>0:
            raise ValueError('invalid_problem: nonpositive Laurent floor required')
        D=s.prod(f**e for f,e in denominator_factors.items())*s.prod(variables)**(-floor)
        # Each direction uses the same denominator. Enlargements are a future
        # search strategy, not an assertion that this denominator is complete.
        for degree in range(getattr(budget,'max_degree',2)+1):
            size=comb(len(variables)+degree,degree)
            count=order+1+len(variables)*size
            if count>min(budget.max_unknowns,256):
                return stopped('joint unknown budget')
            if time.monotonic()-started>budget.seconds:
                return stopped('symbolic time budget','timeout')
            basis=[s.prod(x**e for x,e in zip(variables,p))/D
                   for p in monomials(len(variables),degree)]
            columns=[*ratios,*[r-u*r.subs(x,q*x)
                       for u,x in zip(U,variables) for r in basis]]
            trace={'order':order,'degree':degree,'denominator':str(D),'unknowns':count}
            attempts.append(trace)
            sampled=evaluation_full_rank(columns,variables,parameters)
            if sampled is not None:
                trace['full_column_rank_witness']=sampled
                trace['nullity']=0
                continue
            columns=list(map(s.cancel,columns))
            polys=[s.Poly(c,*variables,domain=field) for c in clear_columns(columns)]
            powers=sorted(set().union(*(set(p.monoms()) for p in polys)))
            trace['equations']=len(powers)
            if len(powers)>getattr(budget,'max_equations',1500):
                return stopped('polynomial equation budget')
            complexity=sum(s.count_ops(v) for p in polys for v in p.coeffs())
            trace['coefficient_operations']=int(complexity)
            rows=[[p.coeff_monomial(power) for p in polys] for power in powers]
            active,forced,reduced=prune_zero_unknowns(rows)
            trace['forced_zero_columns']=forced
            trace['reduced_unknowns']=len(active)
            if order not in active:
                trace['status']='highest_coefficient_forced_zero'
                continue
            witness=full_rank_specialization(rows,parameters)
            if witness is not None:
                trace['full_column_rank_witness']=witness
                trace['nullity']=0
                continue
            reduced_complexity=sum(s.count_ops(v) for row in reduced for v in row)
            trace['reduced_coefficient_operations']=int(reduced_complexity)
            expansion=s.eye(len(active))
            if reduced_complexity>getattr(budget,'max_matrix_terms',20000):
                reduced,expansion=reduce_pair_equations(reduced)
                trace['paired_unknowns']=expansion.cols
                reduced_complexity=sum(s.count_ops(v) for row in reduced for v in row)
                trace['paired_coefficient_operations']=int(reduced_complexity)
                if all(v==0 for v in expansion.row(active.index(order))):
                    trace['status']='highest_coefficient_forced_zero'
                    continue
            if reduced_complexity>getattr(budget,'max_matrix_terms',20000):
                from exact_linear import flint_available,nullspace
                if not flint_available():
                    return stopped('exact coefficient complexity budget; optional python-flint backend unavailable')
                null=nullspace(reduced,transform=expansion,normalize_index=active.index(order))
                trace['linear_backend']='FLINT primitive fraction-free elimination with full residual verification'
            else:
                matrix=s.polys.matrices.DomainMatrix.from_Matrix(
                    s.Matrix(reduced) if reduced else s.zeros(0,expansion.cols)).to_field()
                null=matrix.nullspace().to_Matrix()*expansion.T
                trace['linear_backend']='SymPy exact domain matrix'
            trace['nullity']=null.rows
            reduced_row=next((list(null.row(i)) for i in range(null.rows) if null[i,active.index(order)]!=0),None)
            if reduced_row is None:continue
            row=[s.S.Zero]*count
            for i,v in zip(active,reduced_row):row[i]=v
            row=[s.cancel(e/row[order]) for e in row]
            cs=row[:order+1]
            rs=[s.cancel(sum(c*m for c,m in zip(row[order+1+i*size:order+1+(i+1)*size],basis)))
                for i in range(len(variables))]
            verify(V,U,variables,cs,rs)
            return {'status':'constructed','algorithm':'bounded rational multivariate creative telescoping',
                    'dimension':len(variables),'order':order,'coefficients':list(map(str,cs)),
                    'certificates':list(map(str,rs)),'rational_residual':'0',
                    'n_shift_ratios':list(map(str,ratios)), 'attempts':attempts,
                    'target_used_in_search':False,'complete_search':False,
                    'proof_status':'local_rational_identity_only'}
    return stopped('no relation in enumerated denominator/degree/order space; not unsummability',
                   'search_exhausted')


def construct(problem,budget):
    variables,V,U=derive(problem)
    return {'shifts':{'variables':list(map(str,variables)), 'n_shift':str(V),
                      'index_shifts':list(map(str,U))},
            'construction':search(V,U,variables,budget)}
