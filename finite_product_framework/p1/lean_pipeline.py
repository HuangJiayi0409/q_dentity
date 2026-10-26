"""Elaborated Lean input and certificate-driven proof synthesis for a restricted grammar."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import sympy as s

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
if str(HERE.parent) not in sys.path:
    sys.path.append(str(HERE.parent))


def assemble(parts):
    imports, body = [], []
    for part in parts:
        for line in part.splitlines():
            if line.startswith('import '):
                if line not in imports:
                    imports.append(line)
            else:
                body.append(line)
    return '\n'.join(imports+['']+body)+'\n'


def lean(source, env, *args, timeout=180):
    proc = subprocess.run(['lake', 'env', 'lean', *args, str(source)], cwd=ROOT/'project',
                          env=env, text=True, capture_output=True, timeout=timeout)
    return {'exit_code': proc.returncode, 'output': proc.stdout+proc.stderr}


def environment(work):
    from workflow.preprocessed import environment as shared_environment
    shared=shared_environment(work,'p1')
    if shared is not None:return shared
    src, obj = work/'sources', work/'deps'
    (src/'Benchmark').mkdir(parents=True, exist_ok=True)
    (obj/'Benchmark').mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env['LEAN_PATH'] = str(obj)
    evidence = []
    for name in ('Definitions', 'Auxiliary', 'Gaussian'):
        origin = ROOT/'benchmark/lean/Benchmark'/f'{name}.lean'
        snapshot = src/'Benchmark'/f'{name}.lean'
        snapshot.write_bytes(origin.read_bytes())
        result = lean(snapshot, env, '-R', str(src), '-o', str(obj/'Benchmark'/f'{name}.olean'))
        if result['exit_code']:
            raise RuntimeError('dependency_compile_failed: '+result['output'])
        evidence.append({'path': str(origin.relative_to(ROOT)),
                         'sha256': hashlib.sha256(origin.read_bytes()).hexdigest()})
    # Load the supported finite-product atom from its frozen definition, not the
    # large proof imports (which can contain completed sum identities).
    declarations = []
    from math_library.build import extra_definitions
    for filename, name in [('Batch5Definitions','kacPowerNat'),
                           ('BatchDefinitions','regular'), ('Batch4Definitions','sillsAlpha'),
                           *extra_definitions()]:
        origin = ROOT/'benchmark/lean/Benchmark'/f'{filename}.lean'
        definition = re.search(r'(?m)^def '+name+r'\b[^\n]*(?:\n[ \t]+[^\n]*)*\n',origin.read_text())
        if definition is None:
            raise ValueError('dependency_compile_failed: supported source declaration changed: '+name)
        declarations.append(definition.group())
        evidence.append({'path':str(origin.relative_to(ROOT)),
            'sha256':hashlib.sha256(origin.read_bytes()).hexdigest(),
            'loaded_declaration':'FiniteQBenchmark.'+name,
            'declaration_sha256':hashlib.sha256(definition.group().encode()).hexdigest()})
    snapshot = src/'Benchmark/P1Atoms.lean'
    snapshot.write_text('import Benchmark.Gaussian\nnamespace FiniteQBenchmark\n'
        'open scoped BigOperators\nnoncomputable section\nvariable {K : Type*} [Field K]\n'+
        '\n'.join(declarations)+'end\n'+
        'end FiniteQBenchmark\n')
    result = lean(snapshot, env, '-R', str(src), '-o', str(obj/'Benchmark/P1Atoms.olean'))
    if result['exit_code']:
        raise RuntimeError('dependency_compile_failed: '+result['output'])
    from math_library.registry import dependency_files
    evidence.extend({'path':str(p.relative_to(ROOT)),
                     'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in dependency_files())
    return env, evidence


def proof_slot(source, proof):
    from workflow.preprocessed import slot as shared_slot
    shared=shared_slot(source,proof,('Benchmark.P1Atoms',))
    if shared is not None:return shared
    # Only the deferred proof changes. The original declaration and context survive byte-for-byte.
    pattern = r'(?m)^  sorry\s*$'
    if len(re.findall(pattern, source)) != 1:
        raise ValueError('unsupported_declaration: expected one deferred target')
    source = re.sub(r'(?m)^import Benchmark\.\w+$', 'import Benchmark.P1Atoms', source)
    return re.sub(pattern, lambda _: proof.rstrip(), source)


def extract(source, work, env, prelude=""):
    from math_library.frontend import extractor_text, query_trace
    file = work/'ExtractTarget.lean'
    file.write_text(assemble([extractor_text((HERE/'lean/Extract.lean').read_text()), proof_slot(source, prelude+'\n  p1_export')]))
    result = lean(file, env)
    lines = [line.split('P1_JSON:', 1)[1] for line in result['output'].splitlines() if 'P1_JSON:' in line]
    if len(lines) != 1 or 'P1_EXPORT_ONLY' not in result['output']:
        raise ValueError('representation_gap: '+result['output'])
    if len(re.findall(r'\berror:', result['output'])) != 1:
        raise ValueError('other_elaboration_errors: '+result['output'])
    raw = json.loads(lines[0])
    hypotheses = [line.split('P1_HYPOTHESES_JSON:',1)[1] for line in result['output'].splitlines()
                  if 'P1_HYPOTHESES_JSON:' in line]
    if hypotheses:
        (work/'lean_hypotheses.json').write_text(json.dumps(json.loads(hypotheses[0]),ensure_ascii=False,indent=2)+'\n')
    (work/'lean_expression.json').write_text(json.dumps(raw, ensure_ascii=False, indent=2)+'\n')
    (work/'math_library_query.json').write_text(json.dumps(query_trace(raw),ensure_ascii=False,indent=2)+'\n')
    return raw


OPS = {'HAdd.hAdd':'add', 'HSub.hSub':'sub', 'HMul.hMul':'mul',
       'HDiv.hDiv':'div', 'HPow.hPow':'pow', 'FiniteQBenchmark.gaussian':'gaussian',
       'FiniteQBenchmark.poch':'poch', 'FiniteQBenchmark.kacPowerNat':'fall'}


def find_nodes(node, op):
    result = [node] if node['op'] == op else []
    for arg in node.get('args', []):
        result += find_nodes(arg, op)
    if 'body' in node:
        result += find_nodes(node['body'], op)
    return result


def frontend(raw, identity):
    raw, preparation = normalize_phi(raw)
    raw = normalize_products(raw)
    if raw['op'] == 'And':
        components = [frontend(child,identity) for child in raw['args']]
        formulas,models = map(list,zip(*components))
        return ({'schema_version':1,'source_id':identity,'conjuncts':formulas},
                {'conjuncts':models,'formulas':formulas})
    if raw['op'] != 'Eq':
        raise ValueError('unsupported_structure: equality required')
    left, target = raw['args']
    reversed_equality = target['op'] == 'Finset.sum'
    if reversed_equality:
        left, target = target, left
    if left['op'] != 'Finset.sum':
        raise ValueError('unsupported_structure: one finite sum required')
    domain, binder = left['args']
    if domain['op'] != 'Finset.range' or binder['op'] != 'lambda':
        raise ValueError('unsupported_structure: range sum required')
    upper = domain['args'][0]
    if upper['op'] != 'HAdd.hAdd' or upper['args'][1] != {'op':'nat','value':1}:
        raise ValueError('unsupported_structure: expected variable range(n+1)')
    length = upper['args'][0]
    if length['op'] != 'var':
        raise ValueError('unsupported_structure: variable product length required')
    index = length['name']
    summand = binder['body']
    gaussians = find_nodes(summand, 'FiniteQBenchmark.gaussian')
    if not gaussians:
        raise ValueError('unsupported_structure: Gaussian weight required')
    qnode = gaussians[0]['args'][0]
    if qnode['op'] != 'var':
        raise ValueError('unsupported_structure: base variable required')
    base = qnode['name']
    if not gaussians or any(g['args'] != [qnode, length, {'op':'var','name':binder['name']}] for g in gaussians):
        raise ValueError('unsupported_structure: Gaussian indices/base do not match this verifier')
    names = {index:'n', binder['name']:'k', base:'q'}
    if len(names) != 3:
        raise ValueError('unsupported_structure: overlapping binders')
    def convert(node):
        op = node['op']
        if op == 'var':
            name = node['name']
            if name not in names:
                names[name] = 'p'+str(len(names))
            return names[name]
        if op == 'nat':
            return node['value']
        if op == 'Neg.neg':
            return ['mul', -1, convert(node['args'][0])]
        if op == 'P1.parameter':
            text = lean_expression(node)
            if text not in names:names[text] = 'p'+str(len(names))
            return names[text]
        if op == 'Inv.inv':
            if any(v['name'] in (index,binder['name']) for v in find_nodes(node,'var')):
                raise ValueError('unsupported_structure: index-dependent inverse parameter')
            text = lean_expression(node)
            if text not in names:names[text] = 'p'+str(len(names))
            return names[text]
        if op in OPS:
            return [OPS[op], *map(convert, node['args'])]
        raise ValueError('unsupported_expression: '+op)
    upper = convert(domain['args'][0])
    if upper != ['add','n',1]:
        raise ValueError('unsupported_structure: expected range(n+1)')
    problem = {'schema_version':1, 'source_id':identity,
               'summand':convert(summand), 'target':convert(target)}
    def remove_gaussian(t):
        if t['op']=='FiniteQBenchmark.gaussian':return {'op':'nat','value':1}
        return dict(t,args=[remove_gaussian(x) for x in t['args']]) if 'args' in t else t
    weight=remove_gaussian(summand)
    return problem, {'weight_formula':convert(weight),'weight_expression':weight,
                     'names':names, 'index':index, 'base':base,
                     'binder':binder['name'], 'summand':summand, 'target':target,
                     'reversed_equality':reversed_equality, 'preparation':preparation}


def lean_expression(node, names=None):
    names = names or {}
    op = node['op']
    if op == 'var':
        return names.get(node['name'], node['name'])
    if op == 'nat':
        return str(node['value'])
    args = [lean_expression(a, names) for a in node.get('args', [])]
    if op == 'Neg.neg':
        return f'(-{args[0]})'
    if op == 'P1.parameter':
        return args[0]
    if op == 'Inv.inv':
        return f'({args[0]})⁻¹'
    if op == 'ite':
        return f'(if {args[0]} then {args[1]} else {args[2]})'
    binary = {'HAdd.hAdd':'+','HSub.hSub':'-','HMul.hMul':'*','HDiv.hDiv':'/','HPow.hPow':'^',
              'HMod.hMod':'%', 'Eq':'='}
    if op in binary:
        return f'({args[0]} {binary[op]} {args[1]})'
    if op in ('FiniteQBenchmark.gaussian', 'FiniteQBenchmark.poch', 'FiniteQBenchmark.kacPowerNat'):
        return '('+op+' '+' '.join(args)+')'
    raise ValueError('unsupported_emission: '+op)


def polynomial_lean(expr, mapping):
    if expr.is_Integer:
        return f'({int(expr)})'
    if expr.is_Symbol:
        return mapping[str(expr)]
    if expr.is_Add or expr.is_Mul:
        op = ' + ' if expr.is_Add else ' * '
        return '('+op.join(polynomial_lean(a, mapping) for a in expr.args)+')'
    if expr.is_Pow and expr.exp.is_Integer and expr.exp >= 0:
        return f'({polynomial_lean(expr.base,mapping)} ^ {int(expr.exp)})'
    raise ValueError('domain_unresolved: non-polynomial certificate coefficient')


def normalize_products(node):
    """Recognize a finite product from its actual binder/body, independent of IDs."""
    node = dict(node)
    if 'args' in node:
        node['args'] = [normalize_products(a) for a in node['args']]
    if 'body' in node:
        node['body'] = normalize_products(node['body'])
    if node['op'] != 'Finset.prod':
        return node
    domain, binder = node['args']
    if domain['op'] != 'Finset.range' or binder['op'] != 'lambda':
        raise ValueError('unsupported_structure: finite range product required')
    body = binder['body']
    if body['op'] != 'HSub.hSub' or body['args'][1]['op'] != 'HMul.hMul':
        raise ValueError('unsupported_structure: affine geometric factor required')
    a, product = body['args']
    for b, power in (product['args'], product['args'][::-1]):
        if power['op'] != 'HPow.hPow' or power['args'][1] != {'op':'var','name':binder['name']}:
            continue
        base = power['args'][0]
        if any(v['name'] == binder['name'] for e in (a,b,base) for v in find_nodes(e,'var')):
            continue
        return {'op':'FiniteQBenchmark.kacPowerNat','args':[a,b,base,domain['args'][0]]}
    raise ValueError('unsupported_structure: product factor depends on its binder beyond q^i')


def normalize_phi(raw):
    """A proved representation rule; never a sum evaluation or a preset certificate."""
    if raw['op']!='Eq':return raw,''
    left,right=raw['args']
    side=0 if left['op']=='FiniteQBenchmark.phi' else 1 if right['op']=='FiniteQBenchmark.phi' else None
    if side is None:return raw,''
    ph=raw['args'][side];aa,bb,base,z,length=ph['args']
    nil={'op':'List.nil','args':[]}
    if aa['op']!='List.cons' or aa['args'][1]['op']!='List.cons':return raw,''
    a=aa['args'][0];upper,tail=aa['args'][1]['args']
    if tail!=nil:return raw,''
    def node(op,*args):return {'op':op,'args':list(args)}
    expected=node('HPow.hPow',base,node('Neg.neg',node('Nat.cast',length)))
    if upper!=expected:return raw,''
    if bb['op']=='List.cons' and bb['args'][1]==nil:
        c=bb['args'][0]
        balanced=z==node('HDiv.hDiv',node('HMul.hMul',c,node('HPow.hPow',base,length)),a)
        unbalanced=z==base
        if not (balanced or unbalanced):return raw,''
        other=raw['args'][1-side]
        den=node('FiniteQBenchmark.poch',c,base,length)
        if other['op']!='HDiv.hDiv' or other['args'][1]!=den:return raw,''
        if length['op']!='var' or base['op']!='var':return raw,''
        d=node('P1.parameter',node('HDiv.hDiv',c,a))
        used={v['name'] for v in find_nodes(raw,'var')};binder='p1index'
        while binder in used:binder+='_' 
        ki={'op':'var','name':binder};one={'op':'nat','value':1};two={'op':'nat','value':2}
        gap=node('HSub.hSub',length,ki)
        triangle=lambda e:node('HDiv.hDiv',node('HMul.hMul',e,node('HSub.hSub',e,one)),two)
        factors=[node('FiniteQBenchmark.gaussian',base,length,ki),
                 node('HPow.hPow',node('Neg.neg',d if balanced else one),ki),
                 node('HPow.hPow',base,triangle(ki if balanced else gap)),
                 node('FiniteQBenchmark.poch',a,base,ki),
                 node('FiniteQBenchmark.poch',node('HMul.hMul',node('HMul.hMul',a,d),node('HPow.hPow',base,ki)),base,node('HSub.hSub',length,ki))]
        body=factors[0]
        for factor in factors[1:]:body=node('HMul.hMul',body,factor)
        sm=node('Finset.sum',node('Finset.range',node('HAdd.hAdd',length,one)),{'op':'lambda','name':binder,'body':body})
        def replace_ratio(t):
            if t==d['args'][0]:return d
            return dict(t,args=[replace_ratio(x) for x in t['args']]) if 'args' in t else t
        target=replace_ratio(other['args'][0])
        atext,ctext,btext,ntext=map(lean_expression,(a,c,base,length))
        if balanced:
            prefix=f"  rw [FiniteQP1.phi_balanced_sum {atext} {ctext} {btext} {ntext} (by assumption) (by assumption) (by assumption)]\n"
            prefix+=f"  apply congrArg (fun z => z / {lean_expression(den)})\n"
        else:
            scale=node('HPow.hPow',base,triangle(length))
            target=node('HMul.hMul',target,scale)
            prefix=f"  apply (eq_div_iff ((FiniteQP1.phi_defined_single {ctext} {btext} {ntext} (by assumption)).2 {ntext} le_rfl)).2\n"
            prefix+=f"  apply mul_right_cancel₀ (show {lean_expression(scale)} ≠ 0 from pow_ne_zero _ (by assumption))\n"
            prefix+=f"  rw [FiniteQP1.phi_q_sum {atext} {ctext} {btext} {ntext} (by assumption) (by assumption) (by assumption)]\n"
        return (node('Eq',sm,target) if side==0 else node('Eq',target,sm)),prefix
    if bb!=nil or z!=node('HDiv.hDiv',node('HPow.hPow',base,length),a):return raw,''
    if length['op']!='var' or base['op']!='var':return raw,''
    # Require the actual nonzero/regular assumptions via Lean's assumption tactic.
    atext,btext=lean_expression(a),lean_expression(base)
    prefix=f'''  rw [FiniteQP1.phi_zero_lower_sum {atext} {btext} (by assumption) (by assumption)]
  simp only [zpow_neg, zpow_natCast, ← inv_pow]
'''
    used={v['name'] for v in find_nodes(raw,'var')};binder='p1index'
    while binder in used:binder+='_' 
    ki={'op':'var','name':binder};one={'op':'nat','value':1};inv=node('Inv.inv',a)
    body=node('HMul.hMul',node('FiniteQBenchmark.gaussian',base,length,ki),
              node('FiniteQBenchmark.kacPowerNat',inv,one,base,ki))
    sm=node('Finset.sum',node('Finset.range',node('HAdd.hAdd',length,one)),
            {'op':'lambda','name':binder,'body':body})
    def powers(t):
        if t['op']=='HPow.hPow':
            b,e=t['args']
            if e['op']=='Neg.neg' and e['args'][0]['op']=='Nat.cast':
                return node('HPow.hPow',node('Inv.inv',b),e['args'][0]['args'][0])
        return dict(t,args=[powers(x) for x in t['args']]) if 'args' in t else t
    other=powers(raw['args'][1-side])
    return node('Eq',sm,other) if side==0 else node('Eq',other,sm),prefix


def choose_flux(R, V, x, q):
    # A backward shift of the summand may remove all certificate poles.
    # Only shifts 0/1 are currently verified; not finding one is a verifier gap, not search failure.
    # Reindex before checking polynomiality: X/q becomes X at k+1.
    for shift, coefficient in [(0,s.cancel(R)), (1,s.cancel(R.subs(x,q*x)*V))]:
        num, den = s.fraction(coefficient)
        if den == 1 and num.is_polynomial(*num.free_symbols):
            return shift, coefficient
        if shift == 1:
            # Q/X represents q^(n-k) on 0<=k<=n. The actual Lean goals check
            # the support and its zero-extension; no division by q is emitted.
            gap = s.Symbol('P1Gap')
            reexpressed = s.cancel(coefficient.subs(s.Symbol('Q'),gap*x))
            num, den = s.fraction(reexpressed)
            if den == 1 and num.is_polynomial(*num.free_symbols):
                return shift, reexpressed
    raise ValueError('domain_unresolved: no supported polynomial shifted-summand representation')


def emit_proof(model, shifts, construction):
    from expressions import X, q
    symbol_map = {str(v):v for v in set().union(*(e.free_symbols for e in shifts.values()))}
    # Certificate text is produced by our own q-Gosper backend, never supplied by the input schema.
    R = s.sympify(construction['certificate'], locals=symbol_map)
    shift, multiplier = choose_flux(R, shifts['k_shift'], X, q)
    used = set(model['names'])
    def fresh(stem):
        while stem in used:
            stem += '_'
        used.add(stem)
        return stem
    i,j,F,G,T,C = [fresh(x) for x in ('p1n','p1k','p1F','p1G','p1T','p1C')]
    index, base, binder = model['index'], model['base'], model['binder']
    replacements = {index:i, binder:j}
    ftext = lean_expression(model['summand'], replacements)
    ttext = lean_expression(model['target'], replacements)
    mapping = {canonical: original for original,canonical in model['names'].items()
               if canonical not in ('n','k','q')}
    mapping.update(q=base, Q=f'({base}^{i})', X=f'({base}^{j})')
    ctext = polynomial_lean(shifts['target_coefficient'], mapping)
    flux_mapping = dict(mapping)
    flux_mapping['P1Gap'] = f'({base}^({i}-{j}))'
    htext = polynomial_lean(multiplier, flux_mapping)
    if shift == 1:
        gtext = f'fun ({i} {j} : ℕ) => match {j} with\n    | 0 => 0\n    | {j}+1 => {htext} * {F} {i} {j}'
    else:
        gtext = f'fun ({i} {j} : ℕ) => {htext} * {F} {i} {j}'
    # A shifted tail can be expanded at its head while the neighbouring tail
    # expands at its end. Both rewrites are polynomial identities, even at zero.
    head_rewrites=[]
    for atom in find_nodes(model['summand'],'FiniteQBenchmark.poch'):
        start,pbase,length=atom['args']
        if (start['op']=='HMul.hMul' and
            start['args'][1]=={'op':'HPow.hPow','args':[{'op':'var','name':base},{'op':'var','name':binder}]} and
            length=={'op':'HSub.hSub','args':[{'op':'var','name':index},{'op':'var','name':binder}]}):
            stem=lean_expression(start['args'][0],replacements)
            head_rewrites.append(f'              rw [FiniteQP1.poch_head ({stem}*{base}^{j}) {base} ({i}-({j}+1))]')
            head_rewrites.append(f'              rw [show ({stem}*{base}^{j})*{base} = {stem}*{base}^({j}+1) by simp only [pow_succ]; ring]')
    adjacent_finish='              ring'
    if shift==1 and 'weight_formula' in model:
        from expressions import expression,shift_ratio,rationalize,n as formal_n
        weight=expression(model['weight_formula'])
        un=rationalize(shift_ratio(weight,formal_n)).subs(X,q*X)
        hnext=multiplier.subs(s.Symbol('P1Gap'),s.Symbol('Q')/X).subs(X,q*X)
        factor=s.cancel((un-shifts['target_coefficient']-hnext)/(1-q*X))
        try:
            numerator,denominator=s.fraction(factor)
            clearing=''
            if denominator!=1:
                symbols={s.Symbol('q'),s.Symbol('Q'),s.Symbol('X')}
                if not denominator.free_symbols<=symbols or len(s.Poly(denominator,*symbols).terms())!=1 or s.Poly(denominator,*symbols).coeffs()!=[1]:
                    raise ValueError('unsupported adjacent witness denominator')
                den_text=polynomial_lean(denominator,mapping)
                clearing=f'              apply mul_right_cancel₀ (show {den_text} ≠ 0 by simp [show {base} ≠ 0 by assumption])\n'
            factor_text=polynomial_lean(numerator,mapping)
            weight_text=lean_expression(model['weight_expression'],{index:i,binder:f'({j}+1)'})
            adjacent_finish=clearing+f'''              have hadj := congrArg (fun z => ({factor_text} * {weight_text}) * z)
                (FiniteQP1.gaussian_adjacent {base} {i} {j} hle)
              try simp only [Nat.triangle_succ] at hadj
              simp only [Nat.succ_sub_succ_eq_sub, hlen,
                poch_succ, pow_succ, pow_add, hp] at hadj
              simp only [mul_assoc] at hadj ⊢
              linear_combination hadj'''
        except ValueError:
            pass
    tail_branch=''
    if head_rewrites:
        tail_branch=f'''           | (rw [FiniteQP1.gaussian_pascal {base} {i} {j} hle]
              simp only [show {i}+1-({j}+1) = {i}-{j} by omega, hlen]
'''+ '\n'.join(head_rewrites)+f'''
              simp only [poch_succ, Nat.triangle_succ, pow_succ, pow_add, hp]
{adjacent_finish})
'''
    orientation = '  symm\n' if model.get('reversed_equality') else ''
    proof = model.get('preparation','') + orientation + f'''  let {F} := fun ({i} {j} : ℕ) => {ftext}
  let {T} := fun ({i} : ℕ) => {ttext}
  let {C} := fun ({i} : ℕ) => {ctext}
  let {G} := {gtext}
  try simp only [FiniteQP1.product_eq_fall]
  change (∑ {j} ∈ Finset.range ({index}+1), {F} {index} {j}) = {T} {index}
  refine FiniteQP1.prove_growing_sum {F} {G} {T} {C} (fun _ => 0) ?_ ?_ ?_ ?_ {index}
  · intro {i} {j} hmem
    cases {j} with
    | zero =>
      dsimp only [{F}, {G}, {C}]
      try simp only [Nat.sub_zero, Nat.triangle_succ]
      simp [gaussian_zero_right, FiniteQP1.fall_zero, FiniteQP1.fall_succ,
        poch_succ, pow_add] <;> ring
    | succ {j} =>
      have hle : {j} ≤ {i} := by simp only [Finset.mem_range] at hmem; omega
      dsimp only [{F}, {G}, {C}]
      try simp only [Nat.triangle_succ]
      solve
      | (rw [FiniteQP1.gaussian_pascal {base} {i} {j} hle]
         simp only [Nat.triangle_succ, pow_add, pow_succ, FiniteQP1.fall_succ]
         have hp : {base}^{j} * {base}^({i}-{j}) = {base}^{i} := by
           rw [← pow_add, Nat.add_sub_of_le hle]
         simp only [← hp]
         ring)
      | (simp only [gaussian, FiniteQP1.fall_succ, pow_succ]
         ring)
      | (by_cases he : {j} = {i}
         · subst {j}
           simp [FiniteQP1.gaussian_pascal, gaussian_self, gaussian_above,
             FiniteQP1.fall_zero, FiniteQP1.fall_succ, poch_succ, Nat.triangle_succ, pow_succ]
           <;> ring
         · have hlen : {i}-{j} = ({i}-({j}+1))+1 := by omega
           have hp : {base}^{i} = {base}^{j} * {base}^({i}-({j}+1)) * {base} := by
             rw [← pow_add, ← pow_succ]
             congr 1
             omega
           solve
{tail_branch}           | (rw [FiniteQP1.gaussian_pascal {base} {i} {j} hle]
              simp only [Nat.succ_sub_succ_eq_sub, hlen, FiniteQP1.fall_succ,
                poch_succ, pow_succ, hp]
              ring)
           | (simp only [gaussian, Nat.succ_sub_succ_eq_sub, hlen,
                FiniteQP1.fall_succ, poch_succ, pow_succ, hp]
              ring))
  · intro {i}
    dsimp only [{F}, {G}]
    simp only [gaussian_self, Nat.triangle_succ, pow_add, pow_succ, mul_one, sub_zero,
      FiniteQP1.fall_succ, FiniteQP1.fall_zero, Nat.sub_self, poch_zero, poch_succ]
    ring
  · simp [{F}, {T}, gaussian_zero_right, FiniteQBenchmark.poch, FiniteQP1.fall_zero]
  · intro {i}
    dsimp only [{T}, {C}]
    simp only [Nat.triangle_succ, poch_succ, FiniteQP1.fall_succ, pow_succ, pow_add]
    ring
'''
    return proof, {'shift':shift, 'multiplier':str(multiplier),
                   'certificate':str(R), 'target_coefficient':str(shifts['target_coefficient']),
                   'flux_origin':'q-Gosper certificate multiplied by actual backward term ratio',
                   'boundary_requirement':'derived homogeneous target requires boundary correction zero; checked in Lean'}


def synthesize(source, model, shifts, construction, work, env):
    proof, plan = emit_proof(model, shifts, construction)
    return verify_proof(source, proof, plan, work, env)


def synthesize_conjunction(source, model, result, work, env):
    from expressions import derive
    from textwrap import indent
    def emit(m, r, formula=None):
        if 'conjuncts' not in m:
            return emit_proof(m,derive(formula),r['construction'])
        children = [emit(cm,cr,cf) for cm,cr,cf in
                    zip(m['conjuncts'],r['conjunct_results'],m['formulas'],strict=True)]
        proof = '  constructor\n'+''.join('  ·\n'+indent(p,'  ') for p,_ in children)
        return proof, {'conjunct_plans':[plan for _,plan in children],
                       'all_conjuncts_required':True}
    proof,plan = emit(model,result)
    return verify_proof(source,proof,plan,work,env)


def verify_proof(source, proof, plan, work, env, extra_rules=(), *, timeout=180, shared_rules=True):
    parts = ([(HERE/'lean/Shared.lean').read_text(),
              (HERE/'lean/GaussianRules.lean').read_text(),
              (HERE/'lean/DomainRules.lean').read_text(),
              (HERE/'lean/PhiRules.lean').read_text(),
              (HERE/'lean/ProductRules.lean').read_text()] if shared_rules else [])
    parts += [*extra_rules, proof_slot(source, proof)]
    namespaces = re.findall(r'^namespace\s+(\S+)', source, re.M)
    theorem_names = re.findall(r'^theorem\s+(\S+)\s*\(', source, re.M)
    if len(theorem_names) != 1:
        raise ValueError('unsupported_declaration: unique named theorem required')
    theorem = '.'.join(namespaces+[theorem_names[0]])
    output = work/'Proof.lean'
    output.write_text(assemble(parts)+'\n#print axioms '+theorem+'\n')
    result = lean(output, env, timeout=timeout)
    if result['exit_code'] or 'sorryAx' in result['output']:
        return {'status':'lean_failed', 'plan':plan, 'lean':result}
    expected = f"'{theorem}' depends on axioms: [propext, Classical.choice, Quot.sound]"
    if expected not in result['output']:
        return {'status':'axiom_audit_failed', 'plan':plan, 'lean':result}
    return {'status':'proved', 'plan':plan, 'lean':result,
            'proof_file':str(output), 'proof_sha256':hashlib.sha256(output.read_bytes()).hexdigest(),
            'original_declaration_preserved':True, 'theorem':theorem}
