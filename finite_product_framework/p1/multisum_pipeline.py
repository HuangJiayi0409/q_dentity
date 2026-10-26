"""Native nested-sum frontend; keeps support obligations separate from formal ratios."""
import sympy as s
import json
from bibasic_pipeline import normalize
from lean_pipeline import OPS,find_nodes
from expressions import expression,n


def frontend(raw,identity):
    raw=normalize(raw)
    if raw['op']!='Eq':raise ValueError('unsupported_structure: equality required')
    left,target=raw['args']
    reverse=target['op']=='Finset.sum'
    if reverse:left,target=target,left
    binders=[];bounds=[];term=left
    while term['op']=='Finset.sum':
        domain,binder=term['args']
        if domain['op']!='Finset.range' or binder['op']!='lambda':
            raise ValueError('unsupported_structure: nested range sums required')
        binders.append(binder['name']);bounds.append(domain['args'][0]);term=binder['body']
    if len(binders)<2 or len(set(binders))!=len(binders):
        raise ValueError('unsupported_structure: at least two distinct sum indices required')
    upper=bounds[0]
    if (upper['op']!='HAdd.hAdd' or upper['args'][0]['op']!='var' or
            upper['args'][1]!={'op':'nat','value':1}):
        raise ValueError('unsupported_structure: outer range(n+1) required')
    index=upper['args'][0]['name']
    bases=[a['args'][1] for a in find_nodes(term,'FiniteQBenchmark.poch')]
    bases += [a['args'][0] for a in find_nodes(term,'FiniteQBenchmark.gaussian')]
    if not bases or bases[0]['op']!='var' or any(b!=bases[0] for b in bases):
        raise ValueError('unsupported_structure: one independent q base required')
    base=bases[0]['name']
    names={index:'n',base:'q',**{v:f'i{i}' for i,v in enumerate(binders)}}
    if len(names)!=len(binders)+2:raise ValueError('unsupported_structure: variable collision')
    def convert(t):
        op=t['op']
        if op=='var':
            name=t['name']
            if name not in names:names[name]='p'+str(len(names))
            return names[name]
        if op=='nat':return t['value']
        if op=='Neg.neg':return ['mul',-1,convert(t['args'][0])]
        if op in OPS:return [OPS[op],*map(convert,t['args'])]
        raise ValueError('unsupported_expression: multisum '+op)
    indices=[f'i{i}' for i in range(len(binders))]
    converted_bounds=[convert(b) for b in bounds]
    # Accepted natural-number syntax is n, n-i0, (n-i0)-i1, ...;
    # under earlier range memberships every subtraction is nonnegative.
    def remaining(i):
        t={'op':'var','name':index}
        for name in binders[:i]:t={'op':'HSub.hSub','args':[t,{'op':'var','name':name}]}
        return {'op':'HAdd.hAdd','args':[t,{'op':'nat','value':1}]}
    if all(b==bounds[0] for b in bounds):domain='box'
    elif all(b==remaining(i) for i,b in enumerate(bounds)):domain='simplex'
    else:raise ValueError('representation_gap: unsupported dependent support syntax')
    F=convert(term);T=convert(target)
    if any(expression(T).has(s.Symbol(i)) for i in indices):
        raise ValueError('unsupported_structure: target contains bound index')
    problem={'schema_version':1,'source_id':identity,'indices':indices,'summand':F}
    model={'names':names,'index':index,'binders':binders,'dimension':len(indices),
           'domain':domain,'bounds':converted_bounds,'summand':F,'target':T,'reverse':reverse,
           'natural_subtraction_obligation':'prove earlier bound memberships before algebraic conversion'}
    return problem,model


def synthesize(source,model,construction,work,env):
    from multisum import derive,verify,q,Q
    problem={'schema_version':1,'source_id':'verification','indices':[
        f'i{i}' for i in range(model['dimension'])],'summand':model['summand']}
    variables,V,U=derive(problem)
    symbols={str(p):p for e in [V,*U] for p in e.free_symbols}
    symbols.update({'q':q,'Q':Q,**{str(x):x for x in variables}})
    cs=[s.sympify(c,locals=symbols) for c in construction['coefficients']]
    rs=[s.sympify(r,locals=symbols) for r in construction['certificates']]
    verify(V,U,variables,cs,rs)
    plan={'dimension':model['dimension'],'domain':model['domain'],'bounds':model['bounds'],
          'directions':[[int(i==j) for j in range(model['dimension'])]
                        for i in range(model['dimension'])],
          'positive_boundary':'(D + e_i) \\ D','negative_boundary':'D \\ (D + e_i)',
          'moving_support':'D(n+r) \\ D(n) minus D(n) \\ D(n+r)',
          'generic_lean_rule':'FiniteQP1.multisum_boundary',
          'rule_instantiated_for_original_source':False,'rational_residual':'0'}
    (work/'boundary_plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n')
    hypotheses=work/'lean_hypotheses.json'
    if source and hypotheses.exists() and model.get('target') is not None:
        from multisum_lean import Compiler
        from lean_pipeline import verify_proof,HERE
        compiler=Compiler(model,construction,json.loads(hypotheses.read_text()))
        proof=compiler.emit()
        (work/'proof_tactic.txt').write_text(proof)
        result=verify_proof(source,proof,plan,work,env,extra_rules=(
            (HERE/'lean/MultisumRules.lean').read_text(),
            (HERE/'lean/MultisumProductRules.lean').read_text(),
            'set_option maxHeartbeats 10000000\nset_option maxRecDepth 4096\n'
            'set_option linter.unusedSimpArgs false'),timeout=600,shared_rules=False)
        plan['rule_instantiated_for_original_source']=result['status']=='proved'
        (work/'boundary_plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n')
        return {**result,'lean_proof_generated':True,'dimension':model['dimension'],
                'domain':model['domain'],'boundary_plan':plan}
    # Never equate a formal ratio identity with a proof at boundary zeros/poles.
    return {'status':'boundary_and_domain_unresolved','lean_proof_generated':False,
            'dimension':model['dimension'],'domain':model['domain'],'boundary_plan':plan,
            'remaining_obligations':[
                'Lift rational vector certificates to original finite-product identities on the support',
                'Verify all boundary fluxes and moving-support shells in the original parameter domain',
                'Verify target recurrence, initial values and original Lean declaration']}
