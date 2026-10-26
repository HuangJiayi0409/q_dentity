"""Untrusted polynomial relation reduction in an evaluated difference tower.

All shifts have evaluation proofs in Lean. Atoms are independent indeterminates
for construction only; algebraic independence or constant-field results are not
assumed. The returned ideal-membership witnesses are rechecked in the original ring.
"""
import sympy as s
import time

OPS={'HAdd.hAdd':lambda a,b:a+b,'HSub.hSub':lambda a,b:a-b,'HMul.hMul':lambda a,b:a*b}


def walk(node):
    yield node
    for child in node.get('args',[]):yield from walk(child)
    if 'arg' in node:yield from walk(node['arg'])


def symbolic(node):
    op=node['op']
    if op=='integer':return s.Integer(node['value'])
    if op=='atom':return s.Symbol('a'+str(node['key']))
    if op in OPS:return OPS[op](*(symbolic(a) for a in node['args']))
    if op=='neg':return -symbolic(node['arg'])
    if op=='pow':return symbolic(node['arg'])**node['exponent']
    raise ValueError('uncleared division or unsupported polynomial operation: '+op)


def lean_polynomial(expr,atoms):
    if expr.is_Integer:return str(expr)
    if expr.is_Rational:return f'({expr.p} / {expr.q})'
    if expr.is_Symbol:return '('+atoms[int(str(expr)[1:])]+')'
    if expr.is_Add:return '('+' + '.join(lean_polynomial(x,atoms) for x in expr.args)+')'
    if expr.is_Mul:return '('+' * '.join(lean_polynomial(x,atoms) for x in expr.args)+')'
    if expr.is_Pow and expr.exp.is_Integer and expr.exp>=0:
        return '('+lean_polynomial(expr.base,atoms)+' ^ '+str(expr.exp)+')'
    raise ValueError('non-polynomial certificate coefficient')


def ideal_witness(target,relations,variables,budget):
    """Bounded Buchberger completion with multipliers in ORIGINAL relations.

    A Gröbner remainder alone is insufficient for Lean replay. Each basis row
    carries its exact transformation vector; the final witness is independently
    checked by reduce_goal. Bounds limit search, never certify non-membership.
    """
    deadline=time.monotonic()+budget.get('symbolic_seconds',240)
    limit=budget['max_unknowns'];degree=budget['max_degree']
    basis=[];vectors=[];pairs=[];steps=0
    def check(expressions):
        nonlocal steps
        steps+=1
        if steps>limit or time.monotonic()>=deadline:
            raise ValueError('ideal completion resource budget exhausted')
        count=0
        for p in expressions:
            poly=s.Poly(p,*variables,domain=s.QQ)
            count+=len(poly.terms())
            if poly.total_degree()>degree or count>limit:
                raise ValueError('ideal completion polynomial size/degree budget exhausted')
    def remainder(p,vector):
        if basis:
            quotients,p=s.reduced(p,basis,*variables,domain=s.QQ)
            vector=[s.expand(v-sum(c*w[i] for c,w in zip(quotients,vectors)))
                    for i,v in enumerate(vector)]
        p=s.expand(p);check([p,*vector])
        return p,vector
    def insert(p,vector):
        p,vector=remainder(p,vector)
        if p==0:return
        lc=s.Poly(p,*variables,domain=s.QQ).LC()
        p=s.expand(p/lc);vector=[s.expand(v/lc) for v in vector]
        check([p,*vector])
        pairs.extend((j,len(basis)) for j in range(len(basis)))
        basis.append(p);vectors.append(vector)
    for i,p in enumerate(relations):
        insert(p,[s.Integer(i==j) for j in range(len(relations))])
    cursor=0
    while True:
        quotients,residue=s.reduced(target,basis,*variables,domain=s.QQ)
        if s.expand(residue)==0:
            return [s.expand(sum(c*v[i] for c,v in zip(quotients,vectors)))
                    for i in range(len(relations))]
        if cursor==len(pairs):
            raise ValueError('target outside polynomial ideal over QQ; no stronger difference inference was attempted')
        i,j=pairs[cursor];cursor+=1
        a=s.Poly(basis[i],*variables,domain=s.QQ).monoms()[0]
        b=s.Poly(basis[j],*variables,domain=s.QQ).monoms()[0]
        common=tuple(max(x,y) for x,y in zip(a,b))
        ma=s.prod(x**(c-v) for x,c,v in zip(variables,common,a))
        mb=s.prod(x**(c-v) for x,c,v in zip(variables,common,b))
        insert(s.expand(ma*basis[i]-mb*basis[j]),
               [s.expand(ma*u-mb*v) for u,v in zip(vectors[i],vectors[j])])


def reduce_goal(goal,budget):
    atoms={n['key']:n['display'] for item in [goal,*goal['hypotheses']]
           for side in ('lhs','rhs') for n in walk(item[side]) if n['op']=='atom'}
    if len(atoms)>32:raise ValueError('tower atom limit (32) exceeded')
    difference=s.expand(symbolic(goal['lhs'])-symbolic(goal['rhs']))
    relations=[s.expand(symbolic(h['lhs'])-symbolic(h['rhs'])) for h in goal['hypotheses']]
    active=[i for i,p in enumerate(relations) if p!=0]
    variables=sorted(set().union(difference.free_symbols,*(p.free_symbols for p in relations)),key=str)
    if variables:
        for poly in [difference,*relations]:
            p=s.Poly(poly,*variables,domain=s.QQ)
            if len(p.terms())>budget['max_unknowns'] or p.total_degree()>budget['max_degree']:
                raise ValueError('polynomial size/degree budget exceeded')
    if difference==0:quotients=[s.Integer(0)]*len(active);remainder=s.Integer(0)
    elif not active or not variables:raise ValueError('nonzero shifted residual; no applicable relation')
    else:quotients,remainder=s.reduced(difference,[relations[i] for i in active],*variables)
    algorithm='ordered polynomial reduction'
    if s.expand(remainder)!=0:
        quotients=ideal_witness(difference,[relations[i] for i in active],variables,budget)
        algorithm='bounded Groebner completion with original-relation multipliers'
    if s.expand(difference-sum(c*relations[i] for i,c in zip(active,quotients)))!=0:
        raise ValueError('invalid symbolic reduction witness')
    terms=[f'({lean_polynomial(c,atoms)}) * {goal["hypotheses"][i]["name"]}' for i,c in zip(active,quotients) if c!=0]
    script='linear_combination '+' + '.join(terms) if terms else 'ring'
    return {'algorithm':algorithm,'difference':str(difference),'relations':[str(p) for p in relations],
            'coefficients':{goal['hypotheses'][i]['name']:str(c) for i,c in zip(active,quotients)},
            'remainder':'0','script':script,'atoms':atoms}
