"""Simultaneous creative telescoping for a diagonal q-hypergeometric system.

The components share telescoper coefficients, with one rational certificate per
component. This suffices for their sum, but does not exploit relations between
components and is not a solver for coupled rational matrix difference systems.
"""
from itertools import count
import sympy as s
from expressions import q,Q,X,n,k,expression,shift_ratio,rationalize
from qgosper import Budget,UnsupportedDomain,coefficient_field
from qparameterized import solve_joint,primitive_relation


def search(components,max_order=4,budget=Budget(),*,min_order=0):
    if max_order is not None and (type(max_order) is not int or max_order<0):
        raise ValueError('max_order must be a nonnegative integer or None')
    if type(min_order) is not int or min_order<0 or (max_order is not None and min_order>max_order):
        raise ValueError('invalid minimum order')
    components=list(components)
    if not components:raise ValueError('nonempty component list required')
    shifts=[]
    for i,component in enumerate(components):
        if not isinstance(component,dict) or set(component)!={'n_shift','k_shift'}:
            raise ValueError('each component requires only n_shift and k_shift')
        U,V=(s.sympify(component[key]) for key in ('n_shift','k_shift'))
        coefficient_field(U,X,q);coefficient_field(V,X,q)
        U,V=s.cancel(U),s.cancel(V)
        if U==0 or V==0:raise ValueError(f'component {i}: nonzero shift ratios required')
        if s.cancel(U*V.subs(Q,q*Q)-V*U.subs(X,q*X))!=0:
            raise ValueError(f'component {i}: incompatible n/k shift ratios')
        shifts.append((U,V))
    parameters=set().union(*(v.free_symbols for pair in shifts for v in pair),{q,Q})-{X}
    symbols={str(v):v for v in parameters|{X}}
    parse=lambda v:s.sympify(v,locals=symbols)
    bases=[[s.Integer(1)] for _ in shifts];attempts=[]
    for order in count(min_order) if max_order is None else range(min_order,max_order+1):
        for (U,_),basis in zip(shifts,bases):
            while len(basis)<=order:
                j=len(basis)-1
                basis.append(s.cancel(basis[-1]*U.subs(Q,q**j*Q)))
        result=solve_joint([V for _,V in shifts],bases,X,q,budget,normalize_index=order)
        attempts.append(dict(result,order=order))
        if result['status']=='resource_exhausted':
            return dict(status='resource_exhausted',reason=result['reason'],attempts=attempts)
        if result['status']!='constructed':continue
        coefficients=list(map(parse,result['coefficients']))
        primitive=primitive_relation(coefficients,s.Integer(1),parameters)
        scale=parse(primitive.pop('certificate'))
        pcs=list(map(parse,primitive['coefficients']))
        certificates=[s.cancel(scale*parse(R)) for R in result['certificates']]
        for (_,V),basis,R in zip(shifts,bases,certificates):
            if s.cancel(V*R.subs(X,q*X)-R-sum(c*b for c,b in zip(pcs,basis)))!=0:
                raise ArithmeticError('primitive joint telescoping component residual failed')
        primitive['certificates']=list(map(str,certificates))
        return dict(status='constructed',algorithm='joint parameterized q-Gosper / diagonal creative telescoping',
            order=order,coefficients=result['coefficients'],certificates=result['certificates'],
            n_shift_ratios=[list(map(str,b)) for b in bases],primitive_relation=primitive,
            component_residuals=['0']*len(shifts),shift_compatibility_residuals=['0']*len(shifts),
            component_count=len(shifts),attempts=attempts,target_used_in_search=False,
            minimality_scope='first successful searched order for independent component equations; not necessarily minimal for their sum')
    return dict(status='search_exhausted',attempts=attempts,max_order=max_order,
        reason='no common componentwise relation through max_order; not impossibility for the sum or original identity',
        target_used_in_search=False)


def compute(data,budget,parse):
    if not isinstance(data,dict) or set(data)!={'components'}:
        raise ValueError('joint input accepts only components; no target or proof hints')
    components=data['components']
    if not isinstance(components,list) or not components:
        raise ValueError('nonempty components list required')
    if len(components)>budget.max_states:
        return dict(status='resource_exhausted',solver='q_zeilberger_joint',reason='diagonal component count exceeds state limit')
    normalized=[];active=[];indices=[];summands=[];inputs=[]
    for i,component in enumerate(components):
        F=None
        if not isinstance(component,dict):raise ValueError('component must be an object')
        if set(component)=={'summand'}:
            F=expression(component['summand'])
            if F.has(s.Float,s.nan,s.zoo,s.oo,-s.oo):
                raise UnsupportedDomain('finite exact symbolic summand required')
            if F==0:
                normalized.append(dict(kind='zero_summand'));summands.append(F);continue
            U,V=rationalize(shift_ratio(F,n)),rationalize(shift_ratio(F,k))
        elif set(component)=={'n_shift','k_shift'}:
            U,V=parse(component['n_shift']),parse(component['k_shift'])
        else:raise ValueError('component requires summand or n_shift and k_shift only')
        active.append(dict(n_shift=U,k_shift=V));indices.append(i);inputs.extend([U,V]);summands.append(F)
        normalized.append(dict(n_shift=str(U),k_shift=str(V)))
    if active:
        raw=search(active,max_order=budget.max_order,budget=budget)
    else:
        primitive=primitive_relation([s.Integer(1)],s.Integer(1),{q,Q})
        primitive.pop('certificate');primitive['certificates']=[]
        raw=dict(status='constructed',kind='all_zero_summands',order=0,coefficients=['1'],
            certificates=[],component_residuals=[],shift_compatibility_residuals=[],
            primitive_relation=primitive,attempts=[],target_used_in_search=False)
    output=dict(status=raw['status'],solver='q_zeilberger_joint',normalized_input=dict(components=normalized),
                result=raw,active_component_indices=indices,input_component_count=len(components))
    outputs=[]
    if raw['status']=='constructed':
        # Expand active certificate lists back to the original input order.
        for relation in (raw,raw['primitive_relation']):
            certs=['0']*len(components)
            for i,R in zip(indices,relation['certificates']):certs[i]=R
            relation['certificates']=certs
        raw['component_residuals']=['0']*len(components)
        raw['shift_compatibility_residuals']=[None if F==0 else '0' for F in summands]
        symbols={str(t):t for t in set().union(*(v.free_symbols for v in inputs),{q,Q,X})}
        read=lambda v:s.sympify(v,locals=symbols)
        for key in ('coefficients','certificates'):
            outputs.extend(map(read,raw['primitive_relation'][key]))
        output['operator']=dict(variable='n',shift='n -> n+1; Q -> q*Q',order=raw['order'],
            coefficients=raw['primitive_relation']['coefficients'],
            leading_coefficient=raw['primitive_relation']['leading_coefficient'])
        terms=[None if F is None else str(read(R).subs({X:q**k,Q:q**n})*F)
               for F,R in zip(summands,raw['primitive_relation']['certificates'])]
        output['operator_certificate_term_expressions']=terms
        raw['active_component_count']=len(active)
    denoms=lambda values:sorted({str(s.factor(s.fraction(s.cancel(v))[1])) for v in values
                                if s.fraction(s.cancel(v))[1]!=1})
    output['domain']=dict(coefficient_field='QQ(q,Q,independent parameters)(X)',
        base='q is an indeterminate; characteristic zero',normalized_input_denominators=denoms(inputs),
        output_denominators=denoms(outputs),specialization_policy='generic rational-function result; singular parameter values not checked',
        relation_scope='L(F_i)=Delta_k(R_i*F_i) for every active component; hence L(sum F_i)=Delta_k(sum R_i*F_i)',
        component_dependence_policy='components treated separately; rational equivalence and cancellation across components not exploited',
        boundary_policy='finite-sum boundaries and initial values remain undischarged')
    return output
