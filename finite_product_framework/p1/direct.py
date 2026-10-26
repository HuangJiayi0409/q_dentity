"""Direct q-Gosper branch for index-independent finite Gaussian sums.

The antidifference is computed first. A small structural basis is only a Lean
representation search: failure here never means q-Gosper found no antidifference.
"""
import copy
import sympy as s
from expressions import expression, shift_ratio, k, q, X, Poch
from lean_pipeline import (OPS, find_nodes, lean_expression, polynomial_lean,
                           HERE)


def frontend(raw, identity):
    if raw['op'] != 'Eq':
        raise ValueError('unsupported_structure: equality required')
    left, right = raw['args']
    reverse = right['op'] == 'Finset.sum'
    summation, target = (right,left) if reverse else (left,right)
    if summation['op'] != 'Finset.sum':
        raise ValueError('unsupported_structure: direct branch needs a range sum')
    domain, binder = summation['args']
    if domain['op'] != 'Finset.range' or binder['op'] != 'lambda':
        raise ValueError('unsupported_structure: direct branch needs a range sum')
    upper = domain['args'][0]
    if (upper['op'] != 'HAdd.hAdd' or upper['args'][0]['op'] != 'var'
        or upper['args'][1] != {'op':'nat','value':1}):
        raise ValueError('unsupported_structure: expected range(n+1)')
    index = upper['args'][0]['name']
    term = binder['body']
    if any(v['name'] == index for v in find_nodes(term,'var')):
        raise ValueError('unsupported_structure: direct branch needs n-independent summand')
    atoms = find_nodes(term,'FiniteQBenchmark.gaussian')
    if len(atoms) != 1 or atoms[0]['args'][0]['op'] != 'var':
        raise ValueError('unsupported_structure: one Gaussian atom with variable base required')
    base = atoms[0]['args'][0]['name']
    names = {index:'n',binder['name']:'k',base:'q'}
    if len(names) != 3:
        raise ValueError('unsupported_structure: overlapping variables')
    def convert(node):
        op = node['op']
        if op == 'var':
            name = node['name']
            if name not in names:
                names[name] = 'p'+str(len(names))
            return names[name]
        if op == 'nat': return node['value']
        if op == 'Neg.neg': return ['mul',-1,convert(node['args'][0])]
        if op in OPS: return [OPS[op], *map(convert,node['args'])]
        raise ValueError('unsupported_expression: '+op)
    formula = {'schema_version':1,'source_id':identity,
               'summand':convert(term),'target':convert(target)}
    atom = convert(atoms[0])
    model = {'kind':'direct_q_gosper','names':names,'index':index,'base':base,
             'binder':binder['name'],'summand':term,'target':target,
             'atom':atoms[0],'atom_formula':atom,'reverse':reverse}
    return formula, model


def rationalize(expr):
    """Affine q-exponents; other index parameters become independent q-powers."""
    powers = {}
    def convert(t):
        exponent = s.expand(t.exp)
        variables = sorted(exponent.free_symbols, key=str)
        poly = s.Poly(exponent,*variables) if variables else None
        if poly is not None and poly.total_degree() > 1:
            raise ValueError('representation_gap: nonlinear q-exponent')
        result = s.Integer(1)
        constant = exponent
        for variable in variables:
            coefficient = exponent.coeff(variable)
            if not coefficient.is_Integer:
                raise ValueError('representation_gap: nonintegral q-exponent')
            constant -= coefficient*variable
            name = X if variable == k else s.Symbol('E_'+str(variable))
            if variable != k: powers[str(name)] = str(variable)
            result *= name**coefficient
        if not constant.is_Integer:
            raise ValueError('representation_gap: q-exponent constant')
        return result*q**constant
    result = s.cancel(expr.replace(lambda t:t.is_Pow and t.base==q,convert))
    if result.has(k,Poch) or not result.is_rational_function():
        raise ValueError('representation_gap: non-rational direct shift')
    return result, powers


def construct(formula, budget):
    from qgosper import antidifference
    if set(formula) != {'schema_version','source_id','summand','target'} or formula['schema_version'] != 1:
        raise ValueError('invalid_problem: proof hints are not accepted')
    F = expression(formula['summand'])
    V, powers = rationalize(shift_ratio(F,k))
    result = antidifference(s.cancel(V.subs(X,X/q)),X,q,budget)
    result = {name:str(value) if isinstance(value,s.Basic) else value for name,value in result.items()}
    if result['status'] != 'constructed': return {'construction':result}
    R = s.sympify(result['antidifference_ratio'])
    if s.cancel(V*R.subs(X,q*X)-R-1) != 0:
        raise ValueError('invalid direct q-Gosper certificate')
    # Enumerate structural Gaussian neighbours, not a preselected certificate.
    def atoms(tree):
        if not isinstance(tree,list): return []
        return ([tree] if tree[0]=='gaussian' else []) + sum((atoms(t) for t in tree[1:]),[])
    atom = atoms(formula['summand'])[0]
    atom_expr = expression(atom)
    weight = s.cancel(F/atom_expr)
    weight, extra = rationalize(weight); powers.update(extra)
    _, _, upper, lower = atom
    u,l = expression(upper),expression(lower)
    candidates = []
    ratio = s.Integer(1)
    # A verifier capability bound; q-Gosper itself has already finished.
    for lower_shift in (0,1):
        if lower_shift:
            ratio, extra = rationalize((1-q**(u-l))/(1-q**(l+1)))
            powers.update(extra)
        coefficient = s.cancel(R*weight/ratio)
        num,den = s.fraction(coefficient)
        candidates.append({'lower_shift':lower_shift,'coefficient':str(coefficient)})
        if den == 1 and num.is_polynomial(*num.free_symbols):
            result['representation'] = {'lower_shift':lower_shift,'coefficient':str(coefficient),
                                         'q_power_parameters':powers,'candidates':candidates}
            return {'shifts':{'k_shift':str(V)},'construction':result}
    result.update(status='domain_unresolved',representation_candidates=candidates,
                  reason='no polynomial Gaussian-neighbour representation supported by verifier')
    return {'shifts':{'k_shift':str(V)},'construction':result}


def emit(model, construction):
    rep = construction['representation']
    used = set(model['names'])
    def fresh(name):
        while name in used: name += '_'
        used.add(name);return name
    j,F,G,h = map(fresh,('p1j','p1F','p1G','p1local'))
    base,index,binder = model['base'],model['index'],model['binder']
    names = {binder:j}
    atom = copy.deepcopy(model['atom'])
    if rep['lower_shift']:
        atom['args'][2] = {'op':'HAdd.hAdd','args':[atom['args'][2],{'op':'nat','value':1}]}
    mapping = {canonical:original for original,canonical in model['names'].items()}
    mapping.update(q=base,X=f'({base}^{j})')
    for symbol,parameter in rep['q_power_parameters'].items():
        mapping[symbol] = f'({base}^{mapping[parameter]})'
    coefficient = polynomial_lean(s.sympify(rep['coefficient']),mapping)
    gtext = f'{coefficient} * {lean_expression(atom,names)}'
    ftext = lean_expression(model['summand'],names)
    ttext = lean_expression(model['target'])
    u,l = [lean_expression(a,names) for a in model['atom']['args'][1:]]
    us = lean_expression(model['atom']['args'][1],{binder:f'({j}+1)'})
    # The local rule is generic Pascal. Its side conditions and index alignment
    # are proved, not inferred as trusted facts from the formal quotient.
    local = f'''    have hindex : {us} = {u}+1 := by omega
    have hle : {l} ≤ {u} := by omega
    rw [hindex, FiniteQP1.gaussian_pascal {base} {u} {l} hle]
    simp only [Nat.add_sub_cancel_left, Nat.add_sub_cancel_right, pow_add, pow_one]
    ring'''
    u0,l0 = [lean_expression(a,{binder:'0'}) for a in atom['args'][1:]]
    proof = f'''  {'symm' if model['reverse'] else 'skip'}
  let {F} := fun ({j} : ℕ) => {ftext}
  let {G} := fun ({j} : ℕ) => {gtext}
  change (∑ {j} ∈ Finset.range ({index}+1), {F} {j}) = {ttext}
  have {h} : ∀ {j}, {F} {j} = {G} ({j}+1)-{G} {j} := by
    intro {j}
    dsimp only [{F}, {G}]
{local}
  calc
    _ = ∑ {j} ∈ Finset.range ({index}+1), ({G} ({j}+1)-{G} {j}) :=
      Finset.sum_congr rfl (fun {j} _ => {h} {j})
    _ = {G} ({index}+1)-{G} 0 := FiniteQP1.telescope {G} ({index}+1)
    _ = _ := by
      dsimp only [{G}]
      simp only [one_mul, Nat.add_zero]
      have hzero : FiniteQBenchmark.gaussian {base} {u0} {l0} = 0 :=
        gaussian_above {base} (by omega)
      simp only [Nat.add_zero] at hzero
      rw [hzero]
      simp only [mul_zero, sub_zero]
      congr 1 <;> (first | omega | (congr 1 <;> omega))
'''
    return proof, {'algorithm':'direct_q_gosper','antidifference_ratio':construction['antidifference_ratio'],
                   'representation':rep,'endpoint_policy':'evaluate computed G at actual range endpoints in Lean'}


def synthesize(source,model,construction,work,env):
    if model.get('mode')=='general_telescoping':
        from general_summation import synthesize as general_synthesize
        return general_synthesize(source,model,construction,work,env)
    from lean_pipeline import verify_proof
    proof,plan = emit(model,construction)
    return verify_proof(source,proof,plan,work,env)
