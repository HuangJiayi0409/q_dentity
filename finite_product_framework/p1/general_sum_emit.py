"""Untrusted finite-range certificate reconstruction; Lean checks every bridge."""
import sympy as s
from expressions import expression, n, k, q, Q, X, Poch
from general_summation import parse, pieces, validate_local
from sum_lean import term, rational, ALGEBRA
from source_ir import candidates


def component_sources(body, binder, model, components):
    """Match additive source leaves to certificate components, without reprinting
    truncated natural arithmetic or integer divisions from a rational AST.
    This is only a printer plan; the emitted local Lean equality is mandatory.
    """
    from source_ir import Converter
    from general_summation import rename
    leaves=[]
    def visit(node, negative=False):
        if node['op'] in ('HAdd.hAdd','HSub.hSub'):
            visit(node['args'][0],negative)
            visit(node['args'][1],negative ^ (node['op']=='HSub.hSub'))
        elif node['op']=='Neg.neg':
            visit(node['args'][0],not negative)
        else:
            leaves.append(dict(op='Neg.neg',args=[node]) if negative else node)
    visit(body)
    conv=Converter.__new__(Converter)
    conv.names=dict(model['names']);conv.obligations=set()
    remaining=[]
    for leaf in leaves:
        value=expression(conv.read(rename(leaf,binder,model['binder'])))
        remaining.append((value,leaf))
    matched=[]
    for value in components:
        match=next((j for j,(v,_) in enumerate(remaining) if v==value),None)
        if match is None:return None
        matched.append(remaining.pop(match)[1])
    return matched if not remaining else None


def source_term(node, names=None):
    """Render atom arguments recursively, including casts in phi parameters."""
    return term(_print_atoms(node,names or {}),names)


def _print_atoms(node,names):
    node=dict(node)
    node['args']=[_print_atoms(a,names) for a in node.get('args',[])]
    if 'body' in node:node['body']=_print_atoms(node['body'],names)
    if node['op']=='HPow.hPow' and node.get('exponent_sort')=='Int':
        base,power=node['args']
        return dict(op='var',name='('+term(base,names)+' ^ ('+term(power,names)+' : ℤ))')
    if node['op'] in ('FiniteQBenchmark.poch','FiniteQBenchmark.gaussian',
                       'FiniteQBenchmark.kacPowerNat','FiniteQBenchmark.phi',
                       'FiniteQBenchmark.rogersSzego'):
        return dict(op='var',name='('+node['op']+' '+' '.join(term(a,names) for a in node['args'])+')')
    return node


def natural(v, mapping):
    p=s.Poly(s.expand(v),n,k)
    out=[]
    for powers,c in p.terms():
        if not c.is_Integer or c<0:
            raise ValueError('proof_representation_gap: natural length needs a nonnegative polynomial')
        factors=[str(c)] if c!=1 or not any(powers) else []
        factors += [f'({mapping[str(x)]} ^ {a})' for x,a in zip((n,k),powers) if a]
        out.append(' * '.join(factors))
    return '('+' + '.join(out)+')'


def symbolic(v,mapping):
    if v.func==Poch:
        a,b,l=v.args
        return f'(poch {symbolic(a,mapping)} {symbolic(b,mapping)} {natural(l,mapping)})'
    if v.is_Pow and v.exp.has(n,k):
        # Integer Laurent powers are split explicitly; never cast a negative length.
        p=s.Poly(s.expand(v.exp),n,k)
        pos=s.S.Zero;neg=s.S.Zero
        for powers,c in p.terms():
            if not c.is_Integer:raise ValueError('proof_representation_gap: nonintegral exponent')
            monomial=n**powers[0]*k**powers[1]
            if c>=0:pos+=c*monomial
            else:neg-=c*monomial
        b=symbolic(v.base,mapping)
        top=f'({b} ^ {natural(pos,mapping)})'
        return top if neg==0 else f'({top} / ({b} ^ {natural(neg,mapping)}))'
    if v.is_Add or v.is_Mul:
        return '('+(' + ' if v.is_Add else ' * ').join(symbolic(a,mapping) for a in v.args)+')'
    if v.is_Pow and v.exp.is_Integer:
        b=symbolic(v.base,mapping);e=int(v.exp)
        return f'({b} ^ {e})' if e>=0 else f'(({b} ^ {-e})⁻¹)'
    return rational(v,mapping)


def choice(cs,mapping):
    out='0'
    for j,c in reversed(list(enumerate(cs))):
        out=f'if gsJ = {j} then {rational(c,mapping)} else ({out})'
    return out


SIMP='''simp only [Finset.sum_range_succ, Finset.sum_range_zero, ite_true, ite_false,
      Nat.reduceEqDiff, Nat.reduceAdd, Nat.add_zero, zero_add, add_zero,
      Nat.mul_zero, Nat.zero_mul, Nat.one_mul, Nat.mul_one, pow_one]'''


def algebra(indent=4):
    return '\n'.join(' '*indent+x for x in [
        'try '+SIMP.replace('\n',' '),
        'try simp only [pochList, List.map_cons, List.map_nil, List.prod_cons, List.prod_nil, mul_one]',
        'all_goals try simp only [pow_add, pow_succ, pow_zero, pow_one, Nat.cast_add, Nat.cast_one, Nat.cast_zero, poch_succ, poch_zero]',
        'all_goals try simp only [← pow_mul, Nat.mul_comm]',
        'all_goals solve | ring | (field_simp [sub_ne_zero, *] <;> ring) | (simp_all <;> ring)'])+'\n'


def emit(model, construction):
    if construction.get('status')!='constructed':raise ValueError('invalid_certificate: not constructed')
    cs=list(map(parse,construction['coefficients']));r=len(cs)-1
    if construction['order']!=r:raise ValueError('invalid_certificate: order mismatch')
    canonical={v:key for key,v in model['names'].items()}
    mapping=dict(canonical,n='gsN',k='gsK',Q=f"({canonical['q']}^gsN)",X=f"({canonical['q']}^gsK)")
    rows=model['sides'];certrows=construction['sides']
    if len(rows)!=2 or len(certrows)!=2:raise ValueError('invalid_certificate: two sides required')
    if any(row['kind']=='sum' and model['raw']['args'][i]['op']!='Finset.sum'
           for i,row in enumerate(rows)):
        if model['mode']=='general_recurrence':
            from poch_recurrence_emit import emit as emit_poch_recurrence
            return emit_poch_recurrence(model,construction)
        raise ValueError('proof_representation_gap: structured sum definition requires a proved source-domain bridge; local certificate only')
    # Explicit moving products use the same recurrence exit as structured
    # sums. Unsupported exponent languages retain the exact-source exit.
    # Only representation failures can fall back; invalid witnesses cannot.
    interval_gap=None
    if model['mode']=='general_recurrence' and any(
            atom.has(n) for row in rows if row['kind']=='sum'
            for atom in expression(row['expression']).atoms(Poch)):
        try:
            from poch_recurrence_emit import emit as emit_poch_recurrence
            return emit_poch_recurrence(model,construction)
        except ValueError as exc:
            if not str(exc).startswith(('proof_representation_gap:', 'representation_gap:')):raise
            interval_gap=str(exc)
    # Bind the witness to the independently retained source IR, never its claimed components.
    for row,witness in zip(rows,certrows):
        if row['kind']=='sum':
            validate_local(pieces(expression(row['expression'])),cs,list(map(parse,witness['certificates'])))
        if list(map(parse,witness['coefficients']))!=cs and model['mode']!='general_telescoping':
            raise ValueError('invalid_certificate: different side recurrence')
    if model['mode']=='general_telescoping':
        from sum_lean import antidifference
        i=next(i for i,row in enumerate(rows) if row['kind']=='sum')
        c=certrows[i]['certificates']
        if cs!=[s.S.One] or len(c)!=1:raise ValueError('invalid_certificate: direct witness')
        binding={'variable_mapping':dict(model['names'])}
        actual=next(c for c in candidates(model['raw']) if c['path']==['args',i])
        binding['variable_mapping'][actual['binder']]='k'
        j='exitIndex'
        while j in binding['variable_mapping']:j+='x'
        dm=dict(canonical,n=canonical['n'],k=j,Q=f"({canonical['q']}^{canonical['n']})",X=f"({canonical['q']}^{j})")
        flux=s.cancel(parse(c[0]).subs({Q:q**n,X:q**k})*expression(rows[i]['expression']))
        return antidifference(model['raw'],binding,parse(c[0]),direct_g=symbolic(flux,dm))
    if r<1 or cs[-1]==0:raise ValueError('invalid_certificate: nonzero positive order required')
    from poch_recurrence_emit import typed_source
    index=model['index'];raw=model['raw'];script=''
    for i,a in enumerate(raw['args']):
        text=source_term(typed_source(a),{index:'gsN'})
        # A scalar numeral otherwise defaults to Nat before recurrence_unique
        # can constrain the codomain. Anchor it in the original base's field.
        if rows[i]['kind']!='sum':text=f'({text}) + 0 * {canonical["q"]}'
        script+=f'  let gsS{i} := fun (gsN : ℕ) => {text}\n'
    script+=f'  let gsC := fun (gsN gsJ : ℕ) => ({choice(cs,mapping)}) + 0 * {canonical["q"]}\n'
    sumdata={c['path'][1]:c for c in candidates(raw) if len(c['path'])==2}
    boundary=[];source_flux_sides=[]
    for i,(row,witness) in enumerate(zip(rows,certrows)):
        if row['kind']!='sum':
            boundary.append(f'(∑ gsJ ∈ Finset.range {r+1}, gsC gsN gsJ * gsS{i} (gsN+gsJ))')
            continue
        data=sumdata[i];a,b=row['slope'],row['offset']
        f=source_term(typed_source(data['body']),{index:'gsN',data['binder']:'gsK'})
        components=pieces(expression(row['expression']))
        # Keep the source's Nat subtraction, exact integer divisions and typed
        # powers intact. Expanding a single summand into a generic rational
        # function and printing it back loses these source-domain semantics.
        # The local Lean identity below still checks the rational multiplier
        # against the actual term, including endpoints and zero parameters.
        if len(components) == 1:
            flux=f'({rational(parse(witness["certificates"][0]),mapping)} * ({f}))'
            source_flux_sides.append(i)
        else:
            source_parts=component_sources(data['body'],data['binder'],model,components)
            if source_parts is not None:
                printed=[source_term(typed_source(part),{index:'gsN',data['binder']:'gsK'})
                         for part in source_parts]
                flux=' + '.join(f'({rational(parse(R),mapping)} * ({part}))'
                               for part,R in zip(printed,witness['certificates']))
                source_flux_sides.append(i)
            else:
                flux=' + '.join(f'({rational(parse(R),mapping)} * {symbolic(F,mapping)})' for F,R in zip(components,witness['certificates']))
        script+=f'  let gsF{i} := fun (gsN gsK : ℕ) => {f}\n'
        script+=f'  let gsG{i} := fun (gsN gsK : ℕ) => {flux}\n'
        bound=f'({a}*gsN+{b})'
        boundary.append(f'(gsG{i} gsN {bound} - gsG{i} gsN 0 + ∑ gsJ ∈ Finset.range {r+1}, gsC gsN gsJ * (∑ gsK ∈ Finset.range ({a}*gsJ), gsF{i} (gsN+gsJ) ({bound}+gsK)))')
        script+=f'''  have gsH{i} : ∀ gsN, gsN+{r} ≤ {index} →
      (∑ gsJ ∈ Finset.range {r+1}, gsC gsN gsJ * gsS{i} (gsN+gsJ)) = {boundary[i]} := by
    intro gsN gsBound
    have h := FiniteQGeneralSum.telescoper_range
      (fun gsJ gsK => gsF{i} (gsN+gsJ) gsK) (gsG{i} gsN)
      (gsC gsN) {r} {bound} (fun gsJ => {a}*gsJ) (by
        intro gsK gsRange
        dsimp only [gsC, gsF{i}, gsG{i}]
'''+algebra(8)+f''')
    simpa only [gsS{i}, gsF{i}, Nat.mul_add, Nat.one_mul, Nat.zero_mul,
      Nat.mul_one, Nat.mul_zero, Nat.add_zero, Nat.zero_add, Nat.reduceAdd,
      Nat.add_assoc, Nat.add_comm, Nat.add_left_comm] using h
'''
    defs=', '.join(['gsC','gsS0','gsS1']+[f'gs{v}{i}' for i,row in enumerate(rows) if row['kind']=='sum' for v in ('F','G')])
    script+=f'''  suffices gsTarget : gsS0 {index} = gsS1 {index} by
    simpa only [gsS0, gsS1, pochList_cons, pochList_nil, mul_one, zero_mul, add_zero] using gsTarget
  apply FiniteQGeneralSum.recurrence_unique gsS0 gsS1 gsC {r} {index} (by omega)
  · intro gsJ gsSmall gsBound
    interval_cases gsJ <;> norm_num [{defs}, poch_zero, poch_succ, Finset.sum_range_succ]
    all_goals try ring
  · intro gsN gsBound
'''
    for i,row in enumerate(rows):
        if row['kind']=='sum':script+=f'    rw [gsH{i} gsN gsBound]\n'
    script+=f'    dsimp only [{defs}]\n'+algebra(4)
    from singular_emit import singular_branch
    script+=singular_branch('gs',r,cs[-1],lambda c:rational(c,mapping),defs)
    return script,dict(kind='finite_prefix_common_recurrence',order=r,coefficients=list(map(str,cs)),
        product_interval_representation_gap=interval_gap,
        source_preserving_flux_sides=source_flux_sides,
        obligations=['source local telescopers','all actual shifted tails','equal boundary forcings','initial values','nonzero leading coefficient or explicit singular cases'])
