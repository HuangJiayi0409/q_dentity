"""Single-index, certificate-driven finite q-summation and common recurrences.

Every source expression, shift, tail, specialization and initial value is
rechecked by Lean. Formal rational identities alone never establish a theorem.
This module belongs to the existing telescoping/recurrence methods.
"""
from pathlib import Path
import copy
import json
import subprocess
import sys
import sympy as s

from expressions import expression, shift_ratio, rationalize, Poch, n, k, q, Q, X
from qdifference import rational_read
from lean_pipeline import HERE, verify_proof
sys.path.insert(0, str(HERE.parent))
from source_ir import Converter, candidates, nodes, outer_index, exact_tree


def rename(node, old, new):
    node = copy.deepcopy(node)
    for _, part in nodes(node):
        if part.get('name') == old:
            part['name'] = new
    return node


def recurrence_frontend(raw, identity):
    from zeilberger_pipeline import frontend as legacy
    try:
        return legacy(raw, identity)
    except ValueError:
        return frontend(raw, identity, 'recurrence')


def telescoping_frontend(raw, identity):
    from direct import frontend as legacy
    try:
        return legacy(raw, identity)
    except ValueError:
        return frontend(raw, identity, 'telescoping')


def frontend(raw, identity, mode='recurrence'):
    from math_library.frontend import entry_views
    source_raw=raw
    raw,library_trace=entry_views(raw)
    if raw['op'] != 'Eq':
        raise ValueError('unsupported_structure: general finite sum requires an equality')
    sums = {c['path'][1]: c for c in candidates(raw)
            if len(c['path']) == 2 and c['path'][0] == 'args'}
    if not sums:
        raise ValueError('unsupported_structure: complete sum side required')
    indices = {outer_index(c['domain'], c['binder']) for c in sums.values()}
    if len(indices) != 1 or None in indices:
        raise ValueError('unsupported_structure: one natural outer index required')
    index = indices.pop()
    used = {a['name'] for _, a in nodes(raw) if a['op'] == 'var'}
    binder = 'qsumBoundIndex'
    while binder in used:
        binder += '_'
    bodies = []
    for side, original in enumerate(raw['args']):
        c = sums.get(side)
        bodies.append(rename(c['body'], c['binder'], binder) if c else original)
    conv = Converter(bodies + [c['domain'] for c in sums.values()], index, binder)
    sides = []
    for side, body in enumerate(bodies):
        ir = conv.read(body)
        expr = expression(ir)
        c = sums.get(side)
        row = dict(kind='sum' if c else 'scalar', expression=ir)
        if c:
            if c['domain']['op'] != 'Finset.range':
                raise ValueError('unsupported_structure: general range proof requires a natural prefix')
            bound = conv.read(c['domain']['args'][0])
            length = s.expand(expression(bound))
            slope = length.coeff(n)
            offset = s.expand(length - slope*n)
            if not slope.is_Integer or slope < 0 or not offset.is_Integer or offset < 0:
                raise ValueError('unsupported_structure: nonnegative integer affine range required')
            row.update(bound=bound, slope=int(slope), offset=int(offset))
        elif expr.has(k, Poch) and expr.has(k):
            raise ValueError('unsupported_structure: bound variable in target')
        sides.append(row)
    problem = dict(schema_version=1, source_id=identity, mode='general_'+mode, sides=sides)
    model = dict(mode='general_'+mode, names=conv.names, index=index, binder=binder,
                 raw=raw, sides=sides)
    model['math_library'] = dict(entry_views=library_trace,
        source_views=[step for c in sums.values() for step in c.get('library_trace',[])],
        source_raw=source_raw if library_trace else None,
        proof_status='source_bridge_and_original_proof_still_required')
    return problem, model


def pieces(expr):
    return list(s.Add.make_args(expr))


def parse(value):
    return rational_read(value)


def ratio_shifts(F):
    if F == 0:
        return s.S.One, s.S.One
    return rationalize(shift_ratio(F, n)), rationalize(shift_ratio(F, k))


def lift(coefficients, certificates, components, multiplier):
    """Apply an Ore left multiplier to every local certificate, not just L."""
    lifted = []
    for F, R in zip(components, certificates, strict=True):
        U, V = ratio_shifts(F)
        ratio = s.S.One
        value = s.S.Zero
        for j, a in enumerate(multiplier):
            value += a * R.subs(Q, q**j*Q) * ratio
            ratio = s.cancel(ratio * U.subs(Q, q**j*Q))
        lifted.append(s.cancel(value))
    return lifted


def validate_local(components, coefficients, certificates):
    if len(components) != len(certificates):
        raise ValueError('invalid_certificate: component count')
    for F, R in zip(components, certificates, strict=True):
        U, V = ratio_shifts(F)
        ratio, lhs = s.S.One, s.S.Zero
        for j, a in enumerate(coefficients):
            lhs += a * ratio
            ratio = s.cancel(ratio * U.subs(Q, q**j*Q))
        if s.cancel(V*R.subs(X, q*X)-R-lhs) != 0:
            raise ValueError('invalid_certificate: local telescoper residual')


def construct(problem, budget):
    from core import compute, CoreBudget
    from qjoint import search as joint_search
    from zeilberger import search
    from core import rational_input
    if set(problem) != {'schema_version','source_id','mode','sides'} or problem['schema_version'] != 1:
        raise ValueError('invalid_problem: general finite sum schema')
    if problem['mode'] not in ('general_recurrence','general_telescoping'):
        raise ValueError('invalid_problem: unknown general mode')
    cb = CoreBudget(seconds=budget.seconds, max_order=getattr(budget,'max_order',4),
                    max_unknowns=budget.max_unknowns)
    trace, side_results = [], []
    for row in problem['sides']:
        F = expression(row['expression'])
        components = pieces(F)
        if row['kind'] == 'scalar':
            if problem['mode']=='general_telescoping':
                side_results.append(dict(coefficients=[s.S.One],certificates=[],components=[]))
                continue
            # Zero is annihilated by the identity operator. Giving it E-1
            # needlessly raises the common order and adds false obligations.
            # This is a candidate only: the original scalar source still has
            # to satisfy the emitted recurrence in Lean.
            relations=[[s.S.One] if f==0 else [-rationalize(shift_ratio(f,n)),s.S.One]
                       for f in components]
            coefficients=relations[0]
            trace.append(dict(solver='exact_product_shift',input=row['expression'],relations=[list(map(str,c)) for c in relations]))
            for other in relations[1:]:
                req=dict(schema_version=1,solver='q_ore',input=dict(operation='lclm',
                    a=list(map(exact_tree,coefficients)),b=list(map(exact_tree,other))))
                resp=compute(req,cb);trace.append(dict(request=req,response=resp))
                if resp['status']!='constructed':return dict(construction=resp,core_calls=trace)
                coefficients=list(map(parse,resp['result']['operator']))
            side_results.append(dict(coefficients=coefficients, certificates=[], components=[]))
            continue
        if len(components) == 1:
            U, V = ratio_shifts(F)
            if problem['mode'] == 'general_telescoping':
                request=dict(schema_version=1,solver='q_gosper',input={'k_shift':exact_tree(V)})
                response=compute(request,cb)
                trace.append(dict(request=request,response=response))
                if response['status']!='constructed':return dict(construction=response,core_calls=trace)
                cs=[s.S.One];rs=[parse(response['result']['certificate'])]
            else:
                response=search(U,V,max_order=cb.max_order,budget=cb,min_order=1)
                trace.append(dict(solver='q_zeilberger',input=dict(n_shift=str(U),k_shift=str(V)),response=response))
                if response['status']!='constructed':return dict(construction=response,core_calls=trace)
                rel=response['primitive_relation'];cs=list(map(parse,rel['coefficients']));rs=[parse(rel['certificate'])]
        else:
            if problem['mode']!='general_recurrence':
                raise ValueError('unsupported_structure: direct antiderivative needs one component')
            data={'components':[{'n_shift':exact_tree(ratio_shifts(f)[0]),
                                 'k_shift':exact_tree(ratio_shifts(f)[1])} for f in components]}
            response=joint_search([dict(n_shift=ratio_shifts(f)[0],k_shift=ratio_shifts(f)[1])
                                   for f in components], max_order=cb.max_order,budget=cb,min_order=1)
            trace.append(dict(solver='q_zeilberger_joint',input=data,response=response))
            if response['status']!='constructed':return dict(construction=response,core_calls=trace)
            cs=list(map(parse,response['primitive_relation']['coefficients']))
            rs=list(map(parse,response['primitive_relation']['certificates']))
        validate_local(components,cs,rs)
        side_results.append(dict(coefficients=cs,certificates=rs,components=components))
    if problem['mode']=='general_telescoping':
        if sum(r['kind']=='sum' for r in problem['sides'])!=1:
            raise ValueError('unsupported_structure: direct endpoint comparison needs one sum')
        common=[s.S.One]
    else:
        request=dict(schema_version=1,solver='q_ore',input=dict(operation='lclm',
                     a=list(map(exact_tree,side_results[0]['coefficients'])),
                     b=list(map(exact_tree,side_results[1]['coefficients']))))
        response=compute(request,cb);trace.append(dict(request=request,response=response))
        if response['status']!='constructed':return dict(construction=response,core_calls=trace)
        common=list(map(parse,response['result']['operator']))
        for row, key in zip(side_results,('left_multiplier','right_multiplier')):
            multiplier=list(map(parse,response['result'][key]))
            row['seed_coefficients']=list(row['coefficients'])
            row['seed_certificates']=list(row['certificates'])
            row['certificates']=lift(row['coefficients'],row['certificates'],row['components'],multiplier)
            row['multiplier']=multiplier
            row['coefficients']=common
            validate_local(row['components'],common,row['certificates'])
    serial=[]
    for row in side_results:
        serial.append({key:list(map(str,value)) for key,value in row.items()})
    return dict(construction=dict(status='constructed',algorithm='single-index finite q-sum / common Ore recurrence',
        coefficients=list(map(str,common)),order=len(common)-1,sides=serial,
        boundary_policy='actual common-prefix flux plus every shifted-domain tail',
        target_used_for_local_certificate_search=False),core_calls=trace)


def synthesize(source, model, construction, work, env):
    from general_sum_emit import emit
    proof, plan = emit(model, construction)
    plan['math_library']=model.get('math_library',{})
    (work/'general_sum_plan.json').write_text(json.dumps(plan,indent=2)+'\n')
    (work/'general_sum_tactic.txt').write_text(proof)
    # Structured interval proofs check every local branch and initial value.
    # The caller's overall task deadline remains authoritative.
    timeout = 600 if model.get('mode') == 'general_recurrence' else 240
    heartbeats = 8000000 if model.get('mode') == 'general_recurrence' else 4000000
    try:
        return verify_proof(source,proof,plan,work,env,extra_rules=(
            (HERE/'lean/GeneralSumRules.lean').read_text(),
            (HERE/'lean/PochShiftRules.lean').read_text(),
            f'set_option maxHeartbeats {heartbeats}\nset_option maxRecDepth 4096\nset_option linter.unusedSimpArgs false\n'),timeout=timeout)
    except subprocess.TimeoutExpired as exc:
        output = exc.stdout or b''
        if isinstance(output, bytes):
            output = output.decode('utf-8', errors='replace')
        (work/'lean_timeout.log').write_text(output)
        raise
