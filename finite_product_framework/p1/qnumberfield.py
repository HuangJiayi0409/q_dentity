"""Exact algebraic-number coefficient arithmetic for PiSigma PLDE.

Polynomial arithmetic and factorization use SymPy number fields. Multiplicative
relations use certified PARI S-units, with exact reconstruction of every input.
No numerical logarithm relation is accepted as a certificate.
"""
import ast
import hashlib
from functools import lru_cache
from pathlib import Path
import shutil
import subprocess
import sympy as s
from expressions import q
from qpisigma import PiSigma,unit_signature
from qgosper import UnsupportedDomain
from ore import OreResourceLimit


def gp_executable():
    local=Path(__file__).resolve().parent.parent/'.tools/pari/bin/gp'
    path=local if local.is_file() else shutil.which('gp')
    if not path:raise UnsupportedDomain('certified number-field multiplicative relations require PARI/GP; see p1/DIFFERENCE_GENERAL.md')
    return str(path)


@lru_cache(maxsize=4)
def backend_info(executable):
    binary=Path(executable);files=[binary]
    local_lib=binary.parent.parent/'lib'
    if local_lib.is_dir():files.extend(sorted({p.resolve() for p in local_lib.glob('libpari*.so*') if p.is_file()}))
    version=subprocess.run([executable,'--version-short'],capture_output=True,text=True,check=True,timeout=5).stdout.strip()
    return dict(version=version,artifacts={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in files})


def gp_polynomial(coefficients):
    """Only exact rational coefficients enter the GP program, never source text."""
    return '('+'+'.join('('+str(s.Rational(c).p)+'/'+str(s.Rational(c).q)+')*x^'+str(i)
                        for i,c in enumerate(coefficients))+')'


def s_unit_coordinates(tower,values):
    values=list(map(tower.normal,values))
    field=tower.ground;degree=field.mod.degree()
    def coefficients(v):
        row=list(reversed(field.from_sympy(v).to_list()))
        return [s.Rational(c) for c in row]+[s.Integer(0)]*(degree-len(row))
    polynomial=gp_polynomial(list(reversed(field.mod.to_list())))
    encoded=[gp_polynomial(coefficients(v)) for v in values]
    program='''default(parisize,64000000);
default(parisizemax,512000000);
{ my(P=POLYNOMIAL, K=bnfinit(P,1), A=INPUTS);
  if(bnfcertify(K)!=1,error("number field certification failed"));
  my(S=List());
  for(i=1,#A, my(F=idealfactor(K,A[i])); for(j=1,matsize(F)[1],listput(S,F[j,1])));
  S=Set(Vec(S)); my(U=bnfunits(K,S), E=vector(#A,i,bnfisunit(K,A[i],U)));
  for(i=1,#E, if(#E[i]!=#U[1],error("missing S-unit coordinates")));
  my(G=vector(#U[1],i,lift(nfbasistoalg(K,nffactorback(K,U[1][i])))));
  for(i=1,#A, if(Mod(prod(j=1,#G,G[j]^E[i][j])-A[i],P)!=0,error("S-unit reconstruction failed")));
  print("CERTIFIED"); print(K.tu[1]);
  print(vector(#G,i,vector(poldegree(P),j,Str(polcoef(G[i],j-1)))));
  print(vector(#E,i,Vec(E[i])));
}
quit;
'''.replace('POLYNOMIAL',polynomial).replace('INPUTS','['+','.join(encoded)+']')
    executable=gp_executable()
    try:
        result=subprocess.run([executable,'-fq'],input=program,text=True,capture_output=True,timeout=tower.budget.seconds)
    except subprocess.TimeoutExpired as exc:raise OreResourceLimit('certified number-field S-unit computation timed out') from exc
    lines=result.stdout.splitlines()
    if result.returncode or 'CERTIFIED' not in lines:
        raise OreResourceLimit('PARI did not complete certified S-unit computation: '+result.stderr[-600:])
    index=lines.index('CERTIFIED');order=int(lines[index+1])
    unit_coefficients=ast.literal_eval(lines[index+2]);exponents=ast.literal_eval(lines[index+3])
    generators=[tower.normal(sum(s.Rational(c)*tower.root**i for i,c in enumerate(row))) for row in unit_coefficients]
    if not generators or len(exponents)!=len(values) or any(len(row)!=len(generators) for row in exponents):
        raise ArithmeticError('invalid S-unit coordinate dimensions')
    if any(type(e) is not int for row in exponents for e in row):raise ArithmeticError('nonintegral S-unit exponent')
    for value,row in zip(values,exponents):
        if tower.normal(s.prod(g**e for g,e in zip(generators,row))-value)!=0:
            raise ArithmeticError('independent S-unit reconstruction failed')
    if order<1 or tower.normal(generators[-1]**order-1)!=0:raise ArithmeticError('invalid torsion generator')
    tower.backend_records.append(dict(algorithm='PARI bnfcertify + bnfunits + bnfisunit',certified=True,
        runtime=backend_info(executable),
        values=list(map(str,values)),generators=list(map(str,generators)),exponents=exponents,torsion_order=order,
        exact_reconstruction_verified=True))
    # The last generator is torsion. Radical multiplicative relations quotient
    # out torsion; hyper() separately tests the exact remaining unit.
    return s.Matrix(exponents).T[:-1,:]


class NumberFieldTower(PiSigma):
    def __init__(self,budget,polynomial,base_ratio=q):
        super().__init__(budget,base_ratio)
        poly=s.Poly(polynomial)
        if not poly.is_irreducible or poly.get_domain()!=s.QQ and not poly.get_domain().is_ZZ:
            raise ValueError('irreducible rational number-field polynomial required')
        self.root=s.CRootOf(poly,0,radicals=False)
        self.ground=s.QQ.algebraic_field(self.root) if poly.degree()>1 else s.QQ
        self.marker=s.Dummy('algebraic_root')
        self.minpoly=poly.as_expr().xreplace({poly.gen:self.marker})
        self.normal_cache={};self.domains={};self.backend_records=[]

    def normal(self,value):
        value=s.sympify(value)
        if self.ground==s.QQ:return s.cancel(value)
        if value in self.normal_cache:return self.normal_cache[value]
        # Work in QQ(parameters)[z]/p(z). This avoids repeatedly asking the
        # generic algebraic-number recognizer to identify the same CRootOf.
        # Both representations use exactly the same irreducible polynomial.
        symbols=tuple(sorted(value.free_symbols,key=str))
        if symbols not in self.domains:self.domains[symbols]=s.QQ.frac_field(*symbols) if symbols else s.QQ
        field=self.domains[symbols];num,den=s.fraction(s.cancel(value.xreplace({self.root:self.marker})))
        modulus=s.Poly(self.minpoly,self.marker,domain=field)
        numerator=s.Poly(num,self.marker,domain=field).rem(modulus)
        denominator=s.Poly(den,self.marker,domain=field).rem(modulus)
        if denominator.is_zero:raise ValueError('zero denominator in algebraic coefficient field')
        if denominator.degree()==0:result=numerator.as_expr()/denominator.nth(0)
        else:result=(numerator*s.invert(denominator,modulus)).rem(modulus).as_expr()
        result=s.cancel(result).xreplace({self.marker:self.root})
        if len(self.normal_cache)<self.budget.max_unknowns*10:self.normal_cache[value]=result
        return result

    def constant_signature(self,values):
        if self.ground==s.QQ:return super().constant_signature(values)
        variables=sorted(set().union(*(v.free_symbols for v in values),{q}),key=str)
        columns=[];units=[]
        for value in values:
            entries={};scalar=s.Integer(1)
            for part,sign in zip(s.fraction(self.normal(value)),(1,-1)):
                unit,factors=s.Poly(part,*variables,domain=self.ground).factor_list();scalar=self.normal(scalar*unit**sign)
                for factor,e in factors:
                    scalar=self.normal(scalar*factor.LC()**(sign*e));key=str(factor.monic().as_expr())
                    entries[key]=entries.get(key,0)+sign*e
            columns.append(entries);units.append(scalar)
        keys=sorted(set().union(*(set(c) for c in columns)))
        top=s.Matrix([[c.get(k,0) for c in columns] for k in keys]) if keys else s.zeros(0,len(values))
        if all(v.is_Rational for v in units):
            records=list(map(unit_signature,units));keys=sorted(set().union(*(set(c) for c in records)))
            lower=s.Matrix([[c.get(k,0) for c in records] for k in keys]) if keys else s.zeros(0,len(units))
        else:lower=s_unit_coordinates(self,units)
        return top.col_join(lower)


def constant_components(algebra):
    """Primitive element and CRT decomposition of a finite reduced QQ algebra."""
    variables=set(algebra.variables)
    if any(p.free_symbols-variables for p in algebra.relations):return None
    dimension=len(algebra.basis);z=s.Dummy('number_field')
    for trial in range(1,algebra.budget.max_unknowns+1):
        primitive=sum((j+1)**trial*v for j,v in enumerate(algebra.variables))
        multiplication=algebra.multiplication(primitive);poly=multiplication.charpoly(z).as_poly();z=poly.gen
        if poly.sqf_part().degree()!=dimension:continue
        powers=[s.Integer(1)]
        for j in range(1,dimension):powers.append(algebra.normal(powers[-1]*primitive))
        matrix=s.Matrix([algebra.vector(v) for v in powers]);inverse=matrix.inv()
        expressions={v:s.Poly(sum(c*z**j for j,c in enumerate(s.Matrix([algebra.vector(v)])*inverse)),z).as_expr()
                     for v in algebra.variables}
        components=[]
        for factor,m in poly.factor_list()[1]:
            if m!=1:raise ArithmeticError('reduced constant algebra has repeated primitive factor')
            other=poly.exquo(factor)
            idempotent=(other*s.invert(other,factor)).rem(poly).as_expr()
            components.append(dict(polynomial=factor,primitive=primitive,variable=z,images=expressions,
                                   idempotent=algebra.normal(idempotent.xreplace({z:primitive}))))
        if algebra.normal(sum(c['idempotent'] for c in components)-1)!=0:raise ArithmeticError('CRT idempotents do not sum to one')
        for i,c in enumerate(components):
            if algebra.normal(c['idempotent']**2-c['idempotent'])!=0:raise ArithmeticError('CRT component is not idempotent')
            if any(algebra.normal(c['idempotent']*d['idempotent'])!=0 for d in components[:i]):
                raise ArithmeticError('CRT components are not orthogonal')
        return components
    raise OreResourceLimit('constant algebra primitive element search exceeds budget')


def fixed_constant_solve(algebra,parsed,rhs,budget,A,B,operator=None,base_ratio=q):
    """Native algebraic coefficients throughout arbitrary interleaved PiSigma."""
    if any(algebra.normal(v-z)!=0 for z,v in zip(algebra.variables,algebra.images)):return None
    components=constant_components(algebra)
    if components is None:return rational_constant_solve(algebra,parsed,rhs,budget,A,B,operator,base_ratio)
    from qpisigma_system import build_tower
    answer=[];traces=[]
    for component in components:
        tower=NumberFieldTower(budget,component['polynomial'],base_ratio=base_ratio)
        substitutions={v:f.xreplace({component['variable']:tower.root}) for v,f in component['images'].items()}
        convert=lambda f:tower.normal(s.sympify(f).xreplace(substitutions))
        local=[(t,k,convert(v)) for t,k,v in parsed]
        coefficients=[B,A] if operator is None else operator
        values=list(map(convert,[*coefficients,*rhs]))
        tower=build_tower(local,values,budget,tower=tower,normalize_base=True)
        normalized=[tower.normal(v.xreplace(tower.aliases)) for v in values]
        from qplde import solve as scalar_solve
        if not any(normalized[:len(coefficients)]):
            raise UnsupportedDomain('operator vanishes on a finite component; unrestricted function kernel is not finite-dimensional')
        pairs=scalar_solve(tower,normalized[:len(coefficients)],normalized[len(coefficients):])
        definitions=dict(tower.generated_definitions)
        for c,v in tower.constants.items():definitions[c]=tower.normal(v.xreplace(definitions))
        def restore(v):
            v=tower.normal(v.xreplace(definitions))
            # AlgebraicField output is in the declared primitive root basis.
            if tower.ground!=s.QQ:v=v.xreplace({tower.root:component['primitive']})
            return algebra.normal(v*component['idempotent'])
        answer.extend(([restore(c) for c in cs],restore(g)) for cs,g in pairs)
        traces.append(dict(polynomial=str(component['polynomial'].as_expr()),idempotent=str(component['idempotent']),
                           tower=tower.records,scalar_trace=tower.trace,number_field_backend=tower.backend_records))
        # Use the actual recursively restored constants, not arbitrary generated
        # product coordinates. They generate the newly enlarged fixed field.
        traces[-1]['constant_definitions']=[str(restore(c)) for c in tower.constants]
    return answer,dict(algorithm='native algebraic-number PiSigma PLDE with exact CRT',components=traces,
                       basis_over_full_invariants=True)


def rational_constant_solve(algebra,parsed,rhs,budget,A,B,operator=None,base_ratio=q):
    """Birational normalization when one constant relation is linear in a parameter.

    QQ(C)[z]/(p(z)-C) is QQ(z), not a number field with C specialized to
    a value. The inverse map sends the new transcendental constant back to z.
    """
    from expressions import X
    from qpisigma_system import build_tower
    from qplde import solve as scalar_solve
    if len(algebra.variables)!=1:return None
    z=algebra.variables[0];relation=algebra.relations[0]
    free={X,*[t for t,k,v in parsed]}
    if relation.free_symbols&free:return None
    parameters=sorted(relation.free_symbols-{z},key=lambda v:(v==q,str(v)))
    parameter=next((v for v in parameters if s.Poly(relation,v).degree()==1),None)
    if parameter is None:return None
    polynomial=s.Poly(relation,parameter);image=s.cancel(-polynomial.nth(0)/polynomial.nth(1))
    convert=lambda value:s.cancel(s.sympify(value).xreplace({parameter:image}))
    if convert(relation)!=0:raise ArithmeticError('constant rationalization is not a field map')
    local=[(t,k,convert(v)) for t,k,v in parsed];coefficients=[B,A] if operator is None else operator
    values=list(map(convert,[*coefficients,*rhs]));tower=PiSigma(budget,base_ratio=convert(base_ratio))
    tower=build_tower(local,values,budget,tower=tower,normalize_base=True)
    values=[tower.normal(v.xreplace(tower.aliases)) for v in values]
    pairs=scalar_solve(tower,values[:len(coefficients)],values[len(coefficients):])
    definitions=dict(tower.generated_definitions)
    for c,v in tower.constants.items():definitions[c]=s.cancel(v.xreplace(definitions))
    pairs=[([algebra.normal(c.xreplace(definitions)) for c in cs],algebra.normal(g.xreplace(definitions))) for cs,g in pairs]
    return pairs,dict(algorithm='birational constant parameter elimination followed by complete PiSigma PLDE',
        parameter=str(parameter),parameter_image=str(image),transcendental_constant=str(z),inverse_map=str(z),
        constant_definitions=[str(algebra.normal(c.xreplace(definitions))) for c in tower.constants],
        scalar_trace=tower.trace,tower=tower.records,basis_over_full_invariants=True)


def fixed_constant_system(algebra,parsed,V,rhs,budget,base_ratio=q):
    from qpisigma_system import build_tower,solve as system_solve
    if any(algebra.normal(v-z)!=0 for z,v in zip(algebra.variables,algebra.images)):return None
    components=constant_components(algebra)
    if components is None:return rational_constant_system(algebra,parsed,V,rhs,budget,base_ratio)
    answer=[];traces=[]
    for component in components:
        tower=NumberFieldTower(budget,component['polynomial'],base_ratio=base_ratio)
        substitutions={v:f.xreplace({component['variable']:tower.root}) for v,f in component['images'].items()}
        convert=lambda v:tower.normal(s.sympify(v).xreplace(substitutions))
        local=[(t,k,convert(v)) for t,k,v in parsed];matrix=V.applyfunc(convert);rows=[[convert(v) for v in row] for row in rhs]
        tower=build_tower(local,[*matrix,*[v for row in rows for v in row]],budget,tower=tower,normalize_base=True)
        normalize=lambda v:tower.normal(v.xreplace(tower.aliases))
        pairs,trace=system_solve(tower,matrix.applyfunc(normalize),[[normalize(v) for v in row] for row in rows])
        definitions=dict(tower.generated_definitions)
        for c,v in tower.constants.items():definitions[c]=tower.normal(v.xreplace(definitions))
        def restore(v):
            v=tower.normal(v.xreplace(definitions))
            if tower.ground!=s.QQ:v=v.xreplace({tower.root:component['primitive']})
            return algebra.normal(v*component['idempotent'])
        answer.extend(([restore(c) for c in cs],g.applyfunc(restore)) for cs,g in pairs)
        traces.append(dict(polynomial=str(component['polynomial'].as_expr()),system=trace,number_field_backend=tower.backend_records,
                           constant_definitions=[str(restore(c)) for c in tower.constants]))
    return answer,dict(algorithm='native algebraic-number coupled PiSigma PLDE and CRT',components=traces)


def rational_constant_system(algebra,parsed,V,rhs,budget,base_ratio=q):
    from expressions import X
    from qpisigma_system import build_tower,solve as system_solve
    if len(algebra.variables)!=1:return None
    z=algebra.variables[0];relation=algebra.relations[0]
    if relation.free_symbols&{X,*[t for t,k,v in parsed]}:return None
    parameters=sorted(relation.free_symbols-{z},key=lambda v:(v==q,str(v)))
    parameter=next((v for v in parameters if s.Poly(relation,v).degree()==1),None)
    if parameter is None:return None
    p=s.Poly(relation,parameter);image=s.cancel(-p.nth(0)/p.nth(1))
    convert=lambda v:s.cancel(s.sympify(v).xreplace({parameter:image}))
    matrix=V.applyfunc(convert);rows=[[convert(v) for v in r] for r in rhs]
    tower=PiSigma(budget,base_ratio=convert(base_ratio))
    tower=build_tower([(t,k,convert(v)) for t,k,v in parsed],[*matrix,*[v for r in rows for v in r]],budget,tower=tower,normalize_base=True)
    normalize=lambda v:s.cancel(v.xreplace(tower.aliases))
    pairs,trace=system_solve(tower,matrix.applyfunc(normalize),[[normalize(v) for v in r] for r in rows])
    definitions=dict(tower.generated_definitions)
    for c,v in tower.constants.items():definitions[c]=s.cancel(v.xreplace(definitions))
    restore=lambda v:algebra.normal(v.xreplace(definitions))
    return [([restore(c) for c in cs],g.applyfunc(restore)) for cs,g in pairs],dict(
        algorithm='birational constant parameter elimination and coupled PiSigma PLDE',parameter=str(parameter),parameter_image=str(image),
        constant_definitions=[str(restore(c)) for c in tower.constants],system=trace)


def rationalizable_constant_algebra(algebra,parsed):
    from expressions import X
    if len(algebra.variables)!=1:return False
    relation=algebra.relations[0];z=algebra.variables[0]
    return not relation.free_symbols&{X,*[t for t,k,v in parsed]} and any(s.Poly(relation,v).degree()==1 for v in relation.free_symbols-{z})


def periodic_constant_system(algebra,parsed,V,rhs,budget):
    import math
    from expressions import X
    from qfinite import FiniteAlgebra,finite_order
    from qdifference import rational_read
    components=constant_components(algebra)
    if components is None and not rationalizable_constant_algebra(algebra,parsed):return None
    order=finite_order(algebra.V,[X,*[t for t,k,v in parsed]],budget)
    if order is None:return None
    if algebra.multiplication(algebra.normal(V.det())).det()==0:raise ValueError('invertible periodic system required')
    root_order=2 if components is None else 1
    for component in components or []:
        tower=NumberFieldTower(budget,component['polynomial'])
        if tower.ground==s.QQ:m=2
        else:s_unit_coordinates(tower,[1]);m=tower.backend_records[-1]['torsion_order']
        root_order=math.lcm(root_order,m)
    def shift(value,count=1):
        for _ in range(count):value=algebra.sigma(value)
        return value
    attempts=[];n=V.rows;width=len(rhs)
    for multiple in map(int,s.divisors(root_order)):
        ell=order*multiple
        if ell>budget.max_normal_form_degree:raise OreResourceLimit('periodic matrix unrolling exceeds budget')
        transformed=[(t,k,algebra.normal(shift(t,ell)-t if k=='sum' else shift(t,ell)/t)) for t,k,v in parsed]
        fixed=FiniteAlgebra([(z,p,shift(z,ell)) for z,p in zip(algebra.variables,algebra.relations)],
            {X:q**ell*X,**{t:t+v if k=='sum' else t*v for t,k,v in transformed}},budget,
            set().union(*(v.free_symbols for v in [*V,*[v for r in rhs for v in r]])))
        M=s.eye(n);targets=[s.zeros(1,n) for r in rhs]
        for j in range(ell):
            targets=[(f+s.Matrix([r]).applyfunc(lambda v:shift(v,j))*M).applyfunc(algebra.normal) for f,r in zip(targets,rhs)]
            M=(V.applyfunc(lambda v:shift(v,j))*M).applyfunc(algebra.normal)
        try:solved=fixed_constant_system(fixed,transformed,M,[list(f) for f in targets],budget,base_ratio=q**ell)
        except UnsupportedDomain as exc:
            attempts.append(dict(order=ell,reason=str(exc)))
            if multiple==root_order:raise
            continue
        if solved is None:raise ArithmeticError('periodic matrix unrolling did not fix the constant algebra')
        pairs,trace=solved;break
    else:raise UnsupportedDomain('periodic matrix tower normalization failed')
    constants=[]
    for component in trace.get('components',[trace]):
        for value in component['constant_definitions']:
            value=rational_read(value)
            if algebra.normal(shift(value)-value)!=0 and value not in constants:constants.append(value)
    if len(algebra.basis)*ell**len(constants)*len(pairs)>budget.max_unknowns:
        raise OreResourceLimit('periodic matrix descent spanning set exceeds budget')
    weights=list(algebra.basis)
    for constant in constants:weights=[algebra.normal(w*constant**j) for w in weights for j in range(ell)]
    answer=[];seen=set()
    for source_cs,source_g in pairs:
        for weight in dict.fromkeys(weights):
            current_cs=[algebra.normal(c*weight) for c in source_cs];current_g=(source_g*weight).applyfunc(algebra.normal)
            total_cs=[s.Integer(0)]*width;total_g=s.zeros(1,n)
            for _ in range(ell):
                total_cs=[algebra.normal(a+b) for a,b in zip(total_cs,current_cs)]
                total_g=(total_g+current_g).applyfunc(algebra.normal)
                current_cs=list(map(shift,current_cs))
                current_g=(current_g.applyfunc(shift)*V-sum((c*s.Matrix([f]) for c,f in zip(current_cs,rhs)),s.zeros(1,n))).applyfunc(algebra.normal)
            cs=tuple(algebra.normal(c/ell) for c in total_cs);g=(total_g/ell).applyfunc(algebra.normal);key=(*cs,*g)
            if any(v!=0 for v in key) and key not in seen:answer.append((cs,g));seen.add(key)
    return answer,dict(algorithm='general periodic number-algebra matrix unrolling and invariant descent',order=ell,
                       attempts=attempts,constant_generators=list(map(str,constants)),unrolled_system=trace)


def rational_periodic_algebra(parsed,values,budget):
    from expressions import X
    from qfinite import FiniteAlgebra
    occupied=set().union(*(v.free_symbols for v in [*values,*[v for t,k,v in parsed]]),{t for t,k,v in parsed})
    index=0
    while s.Symbol('FTrivial'+str(index)) in occupied:index+=1
    z=s.Symbol('FTrivial'+str(index))
    return FiniteAlgebra([(z,z-1,z)],{X:q*X,**{t:t+v if k=='sum' else t*v for t,k,v in parsed}},budget,occupied)


def periodic_scalar(algebra,parsed,a,rhs,budget):
    """Companion reduction of an arbitrary-order operator, then full descent."""
    from qfinite import inverse_shift
    a=list(map(algebra.normal,a));rhs=list(map(algebra.normal,rhs))
    while a and a[-1]==0:a.pop()
    if not a:raise ValueError('nonzero difference operator required')
    first=next(i for i,v in enumerate(a) if v!=0)
    for _ in range(first):
        a=[inverse_shift(algebra,parsed,v) for v in a[1:]]
        rhs=[inverse_shift(algebra,parsed,v) for v in rhs]
    if any(algebra.multiplication(v).det()==0 for v in (a[0],a[-1])):
        raise UnsupportedDomain('periodic higher-order companion reduction requires unit endpoint coefficients')
    if len(a)==1:
        return [(tuple(s.Integer(i==j) for i in range(len(rhs))),algebra.normal(f/a[0])) for j,f in enumerate(rhs)],dict(algorithm='unit multiplication')
    n=len(a)-1;companion=s.zeros(n)
    for i in range(n-1):companion[i,i+1]=1
    for i in range(n):companion[n-1,i]=algebra.normal(-a[i]/a[-1])
    V=companion.T.inv().applyfunc(algebra.normal);rows=[]
    for f in rhs:
        forcing=s.zeros(n,1);forcing[-1]=algebra.normal(f/a[-1])
        rows.append(list((V.T*forcing).applyfunc(algebra.normal)))
    solved=periodic_constant_system(algebra,parsed,V,rows,budget)
    if solved is None:raise UnsupportedDomain('periodic PLDE needs a finite number algebra')
    pairs,trace=solved
    return [(cs,g[0]) for cs,g in pairs],trace


def periodic_constant_solve(algebra,parsed,rhs,budget,A,B):
    """Finite-order constant automorphisms and torsion via exact descent.

    Unroll until the number algebra is fixed, solve natively there, then use
    the finite-group Reynolds operator on (c,g). Newly acquired constants are
    integral of degree <= order over the original fixed ring, so their bounded
    monomials, together with the number-algebra basis, span the descent module.
    """
    import math
    from expressions import X
    from qfinite import FiniteAlgebra,finite_order
    from qdifference import rational_read
    components=constant_components(algebra)
    if components is None and not rationalizable_constant_algebra(algebra,parsed):return None
    order=finite_order(algebra.V,[X,*[t for t,k,v in parsed]],budget)
    if order is None:return None
    if algebra.multiplication(A).det()==0 or algebra.multiplication(B).det()==0:
        raise UnsupportedDomain('periodic weighted descent needs unit endpoint coefficients')
    def shift(value,count=1):
        for _ in range(count):value=algebra.sigma(value)
        return value
    root_order=2 if components is None else 1
    for component in components or []:
        tower=NumberFieldTower(budget,component['polynomial'])
        if tower.ground==s.QQ:m=2
        else:
            s_unit_coordinates(tower,[s.Integer(1)]);m=tower.backend_records[-1]['torsion_order']
        root_order=math.lcm(root_order,m)
    attempts=[]
    for multiple in map(int,s.divisors(root_order)):
        ell=order*multiple
        if ell>budget.max_normal_form_degree:raise OreResourceLimit('algebraic periodic unrolling order exceeds budget')
        transformed=[(t,k,algebra.normal(shift(t,ell)-t if k=='sum' else shift(t,ell)/t)) for t,k,v in parsed]
        fixed=FiniteAlgebra([(z,p,shift(z,ell)) for z,p in zip(algebra.variables,algebra.relations)],
            {X:q**ell*X,**{t:t+v if k=='sum' else t*v for t,k,v in transformed}},budget,
            set().union(*(v.free_symbols for v in [A,B,*rhs])))
        ratio=algebra.normal(-B/A);forcing=[algebra.normal(f/A) for f in rhs]
        multiplier=s.Integer(1);targets=[s.Integer(0)]*len(rhs)
        for j in range(ell):
            rj=shift(ratio,j);targets=[algebra.normal(rj*f+shift(h,j)) for f,h in zip(targets,forcing)]
            multiplier=algebra.normal(rj*multiplier)
        try:solved=fixed_constant_solve(fixed,transformed,targets,budget,1,-multiplier,base_ratio=q**ell)
        except UnsupportedDomain as exc:
            attempts.append(dict(order=ell,reason=str(exc)))
            if multiple==root_order:raise
            continue
        if solved is None:raise ArithmeticError('finite-order unrolling did not fix the number algebra')
        pairs,trace=solved;break
    else:raise UnsupportedDomain('algebraic periodic tower normalization failed')
    constants=[]
    for row in trace.get('components',[trace]):
        for value in row['constant_definitions']:
            value=rational_read(value)
            if algebra.normal(shift(value)-value)!=0 and value not in constants:constants.append(value)
    predicted=len(algebra.basis)*ell**len(constants)*len(pairs)
    if predicted>budget.max_unknowns:raise OreResourceLimit('finite constant descent spanning set exceeds budget')
    weights=list(algebra.basis)
    for constant in constants:
        weights=[algebra.normal(w*constant**j) for w in weights for j in range(ell)]
    weights=list(dict.fromkeys(weights));answer=[];seen=set()
    for cs,g in pairs:
        for weight in weights:
            current_cs=[algebra.normal(c*weight) for c in cs];current_g=algebra.normal(g*weight)
            total_cs=[s.Integer(0)]*len(rhs);total_g=s.Integer(0)
            for _ in range(ell):
                total_cs=[algebra.normal(a+b) for a,b in zip(total_cs,current_cs)];total_g=algebra.normal(total_g+current_g)
                current_cs=list(map(shift,current_cs))
                current_g=algebra.normal((shift(current_g)-sum(c*f for c,f in zip(current_cs,forcing)))/ratio)
            total_cs=tuple(algebra.normal(c/ell) for c in total_cs);total_g=algebra.normal(total_g/ell)
            key=(*total_cs,total_g)
            if any(v!=0 for v in key) and key not in seen:answer.append((list(total_cs),total_g));seen.add(key)
    return answer,dict(algorithm='number-algebra periodic unrolling and exact invariant descent',order=ell,
                       attempts=attempts,constant_generators=list(map(str,constants)),unrolled_system=trace,
                       basis_over_full_invariants=True)
