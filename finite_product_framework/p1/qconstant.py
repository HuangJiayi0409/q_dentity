"""Exact birational normalization of radical product dependencies.

An integral coboundary for a power of a new product yields a monomial
invariant. A primitive integer relation is completed to a unimodular basis;
the invariant becomes a free constant. The reconstructed tower is accepted
only after triangularity and every Pi/Sigma condition have been checked.
"""
import copy
import math
import sympy as s
from qgosper import UnsupportedDomain
from ore import OreResourceLimit


def radical_hyper(tower,value,depth):
    value=tower.normal(value)
    if value==1:return 1,s.Integer(1)
    if depth==0:
        if value==-1:return 2,s.Integer(1)
        if tower.ground==s.QQ or any(tower.signature([value],0)):return None
        from qnumberfield import s_unit_coordinates
        if not tower.backend_records:s_unit_coordinates(tower,[value])
        order=tower.backend_records[-1]['torsion_order']
        for m in s.divisors(order):
            if tower.normal(value**m-1)==0:return int(m),s.Integer(1)
        return None
    top,units,witnesses=tower.multiplicative_parts([value],depth)
    if any(top):return None
    t,kind,alpha=tower.nodes[depth-1];m=1;exponent=s.Integer(0);unit=units[0]
    if kind=='product':
        exponent=tower.exponent(alpha,unit,depth-1)
        if exponent is None:return None
        m=int(exponent.q);unit=tower.normal(unit**m/alpha**(m*exponent))
    lower=radical_hyper(tower,unit,depth-1)
    if lower is None:return None
    n,h=lower;power=m*n
    witness=tower.normal(witnesses[0]**power*t**(power*exponent)*h)
    if tower.normal(tower.sigma(witness,depth)/witness-value**power)!=0:
        raise ArithmeticError('radical multiplicative witness residual')
    return power,witness


def normalize_product(tower,t,value):
    if getattr(tower,'normalizing_radical',False):return False
    relation=radical_hyper(tower,value,len(tower.nodes))
    if relation is None:return False
    m,h=relation
    if m>tower.budget.max_normal_form_degree:raise OreResourceLimit('radical dependency exponent exceeds budget')
    products=[(z,a) for z,k,a in tower.nodes if k=='product']
    if not products:return False
    variables=[z for z,k,a in tower.nodes];exponents=[0]*len(products);w=s.Integer(1)
    parameters=sorted((h.free_symbols|{s.Symbol('q')})-set(variables),key=str)
    domain=tower.ground.frac_field(*parameters)
    for part,sign in zip(s.fraction(h),(1,-1)):
        poly=s.Poly(part,*variables,domain=domain)
        for factor,e in poly.factor_list()[1]:
            factor=factor.monic().as_expr();e*=sign
            index=next((i for i,(z,a) in enumerate(products) if factor==z),None)
            if index is not None:exponents[index]+=e
            elif e%m:return False
            else:w=tower.normal(w*factor**(e//m))
    row=[-e for e in exponents]+[m];common=math.gcd(*row)
    row=[e//common for e in row]
    # A nontrivial torsion invariant needs periodic unrolling first.
    new_ratio=tower.normal(value*w/tower.sigma(w))
    ratios=[a for z,a in products]+[new_ratio]
    if tower.normal(s.prod(a**e for a,e in zip(ratios,row))-1)!=0:return False
    if not any(exponents):return False
    from qpisigma import column_basis
    from qpisigma_system import build_tower
    U,rank=column_basis(s.Matrix([row]));M=U.T.inv()
    if list(M[:,0])!=row:raise ArithmeticError('primitive product relation completion failed')
    shadow=copy.copy(tower);shadow.nodes=[];shadow.aliases={};shadow.cache={};shadow.orbit_cache={};shadow.mult_cache={}
    shadow.constants=dict(tower.constants);shadow.generated_definitions=dict(tower.generated_definitions)
    shadow.occupied=set(tower.occupied)|{str(t)};shadow.records=list(tower.records);shadow.trace=list(tower.trace)
    shadow.torsion=[];shadow.normalizing_radical=True
    old=[z for z,a in products]+[tower.normal(t/w)]
    definitions=dict(tower.generated_definitions)
    for c,v in tower.constants.items():definitions[c]=tower.normal(v.xreplace(definitions))
    forward=[];coordinates=[]
    for j in range(M.cols):
        definition=tower.normal(s.prod(v**int(M[i,j]) for i,v in enumerate(old)))
        definition=tower.normal(definition.xreplace(definitions))
        if j==0:coordinate=shadow.fresh(definition)
        else:
            index=0
            while 'PSRadical'+str(index) in shadow.occupied:index+=1
            coordinate=s.Symbol('PSRadical'+str(index));shadow.occupied.add(str(coordinate))
            shadow.generated_definitions[coordinate]=definition
        coordinates.append(coordinate);forward.append(definition)
    inverse=M.inv()
    backward=[tower.normal(s.prod(v**int(inverse[j,i]) for j,v in enumerate(coordinates))) for i in range(M.rows)]
    substitutions={z:backward[i] for i,(z,a) in enumerate(products)}
    substitutions[t]=tower.normal(w.xreplace(substitutions)*backward[-1])
    newnodes=[]
    for j,z in enumerate(coordinates[1:],1):
        ratio=tower.normal(s.prod(a**int(M[i,j]) for i,a in enumerate(ratios)))
        newnodes.append((z,'product',tower.normal(ratio.xreplace(substitutions))))
    newnodes.extend((z,k,tower.normal(a.xreplace(substitutions))) for z,k,a in tower.nodes if k=='sum')
    # Verify forward shift intertwining before rebuilding the new tower.
    original_shift={z:z+a if k=='sum' else z*a for z,k,a in tower.nodes};original_shift[t]=t*value
    # Use definitions in the old current coordinates (before generated-variable
    # restoration) for this check, so aliases do not change the shift map.
    raw_forward=[tower.normal(s.prod(v**int(M[i,j]) for i,v in enumerate(old))) for j in range(M.cols)]
    if tower.normal(raw_forward[0].xreplace(original_shift)-raw_forward[0])!=0:
        raise ArithmeticError('constructed radical constant is not invariant')
    try:shadow=build_tower(newnodes,[value,h],tower.budget,tower=shadow)
    except (UnsupportedDomain,ValueError):return False
    if shadow.torsion:return False
    substitutions={z:tower.normal(v.xreplace(shadow.aliases)) for z,v in substitutions.items()}
    previous_aliases={z:tower.normal(v.xreplace(substitutions)) for z,v in tower.aliases.items()}
    shadow.aliases={**shadow.aliases,**substitutions,**previous_aliases}
    mapping={z:shadow.aliases.get(z,z) for z in original_shift}
    for z,shifted in original_shift.items():
        if shadow.normal(shadow.sigma(mapping[z])-shifted.xreplace(mapping))!=0:
            raise ArithmeticError('radical tower rebuild does not intertwine the original shift')
    shadow.records.append(dict(action='primitive_radical_product_normalization',name=str(t),
        power=m,coboundary=str(h),removed_coboundary=str(w),primitive_relation=row,
        unimodular_matrix=[[int(v) for v in M.row(i)] for i in range(M.rows)],
        invariant=str(coordinates[0]),invariant_definition=str(forward[0]),
        aliases={str(z):str(v) for z,v in substitutions.items()},triangular_rebuild_verified=True))
    shadow.normalizing_radical=False;shadow.clear_cache();tower.__dict__.update(shadow.__dict__)
    return True
