"""Finite weighted bijections and sign-reversing involutions.

Plans are selected from elaborated structure. Every map/weight/fixed-point
obligation is reconstructed in Lean; unsupported representations fail closed.
"""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time
import itertools
from workflow.contracts import HERE,ROOT,save,sha
from product.pipeline import lean,assemble  # process and text utilities only

LEAN=HERE/'combinatorial/lean'
BACKENDS=('weighted_bijection','sign_reversing_involution')
FINISH='''  all_goals intros
  all_goals try simp_all only [Finset.mem_range, Finset.mem_Icc,
    Nat.cast_sub (by omega), Nat.cast_add, Nat.cast_one]
  all_goals try push_cast
  all_goals first | assumption | (ring; done) | omega | (simp_all; done) | (norm_cast; omega)
  done'''
SCRIPTS={
 'subset_complement':'  apply FiniteQCombinatorial.subset_complement\n'+FINISH,
 'subset_blocks_rank':'  apply FiniteQCombinatorial.subset_blocks_rank\n  assumption',
 'subset_blocks':'  apply FiniteQCombinatorial.subset_blocks\n  assumption',

 'range_subset_weights':'  apply FiniteQCombinatorial.range_geometric_subsets',
 'range_remainder':'  apply FiniteQCombinatorial.range_remainder\n'+FINISH,
 'geometric_subsets':'''  rw [FiniteQCombinatorial.normalize_subset_weights _ (by assumption)]
  rw [FiniteQCombinatorial.geometric_subsets]
  rw [← mul_assoc, FiniteQCombinatorial.normalized_geometric_factor _ (by assumption), one_mul]''',
 'range_reflect':'  apply FiniteQCombinatorial.range_bijection\n'+FINISH,
 'interval_reflect':'  apply FiniteQCombinatorial.interval_bijection\n'+FINISH,
 'range_cancel':'  apply FiniteQCombinatorial.range_cancel\n'+FINISH,
 'interval_cancel':'  apply FiniteQCombinatorial.interval_cancel\n'+FINISH,
 'toggle_zero':'''  apply FiniteQCombinatorial.toggle_cancel (a := 0)
  · simp_all
  · intro t ht
    first | exact FiniteQCombinatorial.toggle_sign 0 t | (apply FiniteQCombinatorial.toggle_signed_weight; done) | (simp_all; done)''',
 'toggle_one':'''  apply FiniteQCombinatorial.toggle_cancel (a := 1)
  · simp_all
  · intro t ht
    first | exact FiniteQCombinatorial.toggle_sign 1 t | (apply FiniteQCombinatorial.toggle_signed_weight; done) | (simp_all; done)''',
}
MAPS={
 'subset_blocks_rank':{'domain':'rank-filtered subsets of disjoint blocks',
  'map':'(a,b) ↦ a ∪ b','inverse':'u ↦ (u ∩ s,u ∩ t)',
  'rank_condition':'card a + card b = h; explicit, never silently dropped'},
 'gaussian_odd_cancel':{'domain':'ranks 0..n, n odd','map':'k ↦ n-k',
  'fixed_points':'none by odd parity','weight':'opposite signs and equal Gaussian coefficients',
  'shared_lemmas':['gaussian_rank_symmetry'],'other_method_solver_calls':[]},
 'subset_complement':{'domain':'all subsets of an explicit ground set',
  'map':'s \ t', 'inverse':'s \ t', 'weight':'arbitrary, checked termwise'},
 'subset_blocks':{'domain':'subsets of disjoint union and pairs of block subsets',
  'map':'(a,b) ↦ a ∪ b','inverse':'u ↦ (u ∩ s,u ∩ t)',
  'obligations':['block disjointness','membership','injectivity','surjectivity','arbitrary weight']},
 'gaussian_reciprocal':{'domain':'rank indices 0..n',
  'map':'k ↦ n-k','inverse':'k ↦ n-k',
  'weight':'reciprocal monomial transport; nonzero parameter required',
  'shared_lemmas':['gaussian_rank_symmetry: local coefficient symmetry proved from definition and Pascal'],
  'other_method_solver_calls':[]},

 'range_subset_weights':{'domain':'fixed-cardinality subsets of range n',
  'maps':['identity on old subsets','insert n'], 'inverses':['identity','erase n'],
  'weight':'product of q^i; division-free rank bridge, including q=0'},
 'geometric_choices':{'domain':'rank-stratified subsets of range n and binary choices on range n',
  'maps':['(k,s) ↦ s','subset ↦ membership indicator'],
  'inverses':['s ↦ (card s,s)','indicator ↦ selected subset'],
  'weight':'(-z)^card(s) * product(q^i); geometric_rank_sum then weighted_choices',
  'shared_lemmas':['Gaussian local recurrence (representation only)','Finset.sum_powerset','Finset.prod_one_add (choice/subset bijection)'],
  'other_method_solver_calls':[]},
 'range_remainder':{'map':'i ↦ n-1-i','domain':'range n',
  'fixed_points':'retained as filtered weighted sum; cancellation only off fixed points'},
 'geometric_subsets':{'domain':'fixed-cardinality subsets of Icc 1 n',
  'maps':['identity on subsets not containing the new maximum','t ↦ insert (n+1) t'],
  'inverses':['identity','t ↦ erase t (n+1)'],
  'closure':'disjoint partition, sum_image injectivity; induction on symbolic n',
  'weight':'product of q^i; insertion multiplies by q^(n+1); certified Gaussian local recurrence'},
 'range_reflect':{'map':'i ↦ n-1-i','inverse':'i ↦ n-1-i','domain':'range n'},
 'interval_reflect':{'map':'i ↦ a+b-i','inverse':'i ↦ a+b-i','domain':'Icc a b in ℤ'},
 'range_cancel':{'map':'i ↦ n-1-i','domain':'range n','fixed_points':'weight must be zero'},
 'interval_cancel':{'map':'i ↦ a+b-i','domain':'Icc a b in ℤ','fixed_points':'weight must be zero'},
 'toggle_zero':{'map':'toggle membership of 0','domain':'powerset','fixed_points':'none; membership contradiction'},
 'toggle_one':{'map':'toggle membership of 1','domain':'powerset','fixed_points':'none; membership contradiction'},
}


def slot(source,proof):
    from workflow.preprocessed import slot as shared_slot
    shared=shared_slot(source,proof,('Benchmark.CombinatorialRepresentation',))
    if shared is not None:return shared
    if len(re.findall(r'(?m)^  sorry\s*$',source))!=1:raise ValueError('one deferred proof slot required')
    source=re.sub(r'^import[^\n]*$','import Benchmark.CombinatorialRepresentation',source,flags=re.M)
    return re.sub(r'(?m)^  sorry\s*$',lambda _:proof,source)


def environment(work):
    from workflow.preprocessed import environment as shared_environment
    shared=shared_environment(work,'combinatorial')
    if shared is not None:return shared
    src,obj=work/'sources',work/'deps'
    (src/'Benchmark').mkdir(parents=True);(obj/'Benchmark').mkdir(parents=True)
    env=dict(os.environ,LEAN_PATH=str(obj));deps=[]
    def dep(path):deps.append({'path':str(path.relative_to(ROOT)),'sha256':sha(path)})
    def compile(name,text):
        f=src/'Benchmark'/f'{name}.lean';f.write_text(text)
        r=lean(f,env,'-R',str(src),'-o',str(obj/'Benchmark'/f'{name}.olean'))
        save(work/f'{name}_compile.json',r)
        if r['exit_code']:raise ValueError('dependency_compile_failed: '+r['output'])
    definitions=ROOT/'benchmark/lean/Benchmark/Definitions.lean';dep(definitions)
    compile('Definitions',definitions.read_text())
    gaussian=ROOT/'benchmark/lean/Benchmark/Gaussian.lean';dep(gaussian)
    # Only definitional zero/self/support lemmas. No closed form or target theorem.
    basic=gaussian.read_text().split('namespace FiniteQBenchmark',1)[1].split('/-- Algebraic recurrence',1)[0]
    compile('Gaussian','import Benchmark.Definitions\nimport Mathlib.Tactic\nnamespace FiniteQBenchmark'+basic+'end FiniteQBenchmark\n')
    recurrence=HERE/'p1/lean/GaussianRules.lean';dep(recurrence)
    compile('GaussianRules',recurrence.read_text())
    for name,file in [('CombinatorialRules','Rules.lean'),('CombinatorialRepresentation','Representation.lean')]:
        path=LEAN/file;dep(path);compile(name,path.read_text())
    for path in (LEAN/'Export.lean',Path(__file__),HERE/'product/pipeline.py'):dep(path)
    return env,deps


def extract(source,work,env):
    file=work/'Extract.lean';file.write_text(assemble((LEAN/'Export.lean').read_text(),slot(source,'  combinatorial_export')))
    r=lean(file,env);save(work/'extraction.json',r)
    lines=[s.split('COMBINATORIAL_JSON:',1)[1] for s in r['output'].splitlines() if 'COMBINATORIAL_JSON:' in s]
    if len(lines)!=1 or len(re.findall(r'\berror:',r['output']))!=1 or 'COMBINATORIAL_EXPORT_ONLY' not in r['output']:
        raise ValueError('unsupported representation/context: '+r['output'])
    return json.loads(lines[0])


def nodes(node):
    yield node
    for child in node.get('args',[]):yield from nodes(child)
    if 'body' in node:yield from nodes(node['body'])


def oriented_plans(raw):
    if raw['op']!='Eq':return []
    left,right=raw['args'];ops={n['op'] for n in nodes(raw)};result=[]
    if left['op']=='FiniteQBenchmark.rogersSzego' and right['op']=='HMul.hMul':
        for r in nodes(right):
            if r['op']=='FiniteQBenchmark.rogersSzego' and r['args'][1:]==left['args'][1:]:
                result.append({'backend':'weighted_bijection','rule':'gaussian_reciprocal','parameters':r['args']})
    if left['op']=='Finset.sum' and left['args'][0]['op']=='Finset.powerset':
        ground=left['args'][0]['args'][0]
        if right['op']=='Finset.sum' and right['args'][0]==left['args'][0]:
            result.append({'backend':'weighted_bijection','rule':'subset_complement'})
        if ground['op']=='Union.union' and right['op']=='Finset.sum':
            result.append({'backend':'weighted_bijection','rule':'subset_blocks'})
    if left['op']=='Finset.sum' and left['args'][0]['op']=='Finset.powersetCard':
        if left['args'][0]['args'][-1]['op']=='Union.union' and right['op']=='Finset.sum':
            result.append({'backend':'weighted_bijection','rule':'subset_blocks_rank'})
    if {'FiniteQBenchmark.gaussian','Finset.powersetCard'}<=ops and left['op']=='Finset.sum':
        domain=left['args'][0]
        if domain['op']=='Finset.powersetCard':
            # powersetCard's elaborated arguments are cardinality, then ground set.
            ground=domain['args'][-1]
            if ground['op']=='Finset.range':
                result.append({'backend':'weighted_bijection','rule':'range_subset_weights'})
            elif ground['op']=='Finset.Icc':
                result.append({'backend':'weighted_bijection','rule':'geometric_subsets'})
    if left['op']=='Finset.sum' and right['op']=='FiniteQBenchmark.poch':
        z,q,n=right['args']
        if left['args'][0]['op']=='Finset.range' and any(
            node['op']=='FiniteQBenchmark.gaussian' and node['args'][:2]==[q,n] for node in nodes(left)):
            result.append({'backend':'weighted_bijection','rule':'geometric_choices','parameters':[z,q,n]})
    if left['op']=='Finset.sum':
        domain=left['args'][0];op=domain['op']
        is_range=op=='Finset.range'
        is_interval=op=='Finset.Icc' and domain.get('type')=='Finset ℤ'
        if right['op']=='Finset.sum' and domain==right['args'][0]:
            if is_range:result.append({'backend':'weighted_bijection','rule':'range_reflect'})
            if is_interval:result.append({'backend':'weighted_bijection','rule':'interval_reflect'})
        if right['op']=='Finset.sum' and is_range:
            remainder_domain=right['args'][0]
            if remainder_domain['op']=='Finset.filter' and domain==remainder_domain['args'][-1]:
                result.append({'backend':'sign_reversing_involution','rule':'range_remainder'})
        if right=={'op':'nat','value':0}:
            if is_range:
                for node in nodes(left):
                    if node['op']=='FiniteQBenchmark.gaussian':
                        result.append({'backend':'sign_reversing_involution','rule':'gaussian_odd_cancel','parameters':node['args'][:2]})
                result.append({'backend':'sign_reversing_involution','rule':'range_cancel'})
            if is_interval:result.append({'backend':'sign_reversing_involution','rule':'interval_cancel'})
            if op=='Finset.powerset':
                result.extend({'backend':'sign_reversing_involution','rule':r} for r in ('toggle_zero','toggle_one'))
    return result


def plans(raw):
    if raw['op']=='And':
        branches=[plans(child) for child in raw['args']]
        # Full statement only: never count a proof of just one conjunct.
        return [dict(backend='weighted_bijection',rule='conjunction',children=list(pair))
                for pair in itertools.islice(itertools.product(*branches),32)]
    if raw['op']!='Eq':return []
    # Each orientation is tried with an explicit symmetry proof; no mutation
    # of the original statement or target-dependent map is introduced.
    result=[dict(p,reverse=False) for p in oriented_plans(raw)]
    swapped=dict(raw,args=list(reversed(raw['args'])))
    result.extend(dict(p,reverse=True) for p in oriented_plans(swapped))
    return result


def diagnostics(raw,path=()):
    if raw['op']=='And':
        return [item for i,child in enumerate(raw['args']) for item in diagnostics(child,path+(i,))]
    candidates=plans(raw)
    ops={n['op'] for n in nodes(raw)}
    gaps=[]
    if 'FiniteQBenchmark.gaussian' in ops and not candidates:
        gaps.append('Gaussian rank-normalized object bridge and weight transport are not automatically synthesized')
    if 'ite' in ops:
        gaps.append('Conditional branches require complete certificates; odd-rank cancellation alone does not close an even residual product')
    if 'FiniteQBenchmark.gaussianInt' in ops:
        gaps.append('Integer zero-supported Gaussian objects and mixed Nat/Int weight transport are not implemented')
    return [dict(goal_path=list(path),root=raw['op'],plans=candidates,
        status='candidate' if candidates else 'unsupported_representation_or_map',missing_capabilities=gaps,
        obligations=['Object representation','Domain and inverse maps','Weight equality','Fixed/remainder contribution'],
        reason='Kernel obligations remain' if candidates else
        'No object/map grammar covers this leaf; no fallback to another method')]


def term(node):
    if node['op']=='var':return node['name']
    if node['op']=='nat':return str(node['value'])
    if node.get('text'):return '('+node['text']+')'
    raise ValueError('missing reconstructible parameter')


def proof_script(plan):
    if plan['rule']=='conjunction':
        return '  constructor\n'+''.join('  ·\n'+''.join('  '+line+'\n' for line in proof_script(child).splitlines())
                                        for child in plan['children'])
    prefix='  symm\n' if plan.get('reverse') else ''
    if plan['rule']=='gaussian_odd_cancel':
        q,n=map(term,plan['parameters'])
        return prefix+f'''  apply FiniteQCombinatorial.odd_rank_cancel
  · apply Nat.odd_iff.mpr
    omega
  · intro k hk
    exact FiniteQCombinatorial.gaussian_rank_symmetry {q} {n} k hk'''
    if plan['rule']=='gaussian_reciprocal':
        u,q,n=map(term,plan['parameters'])
        return prefix+f'''  simp only [FiniteQBenchmark.rogersSzego, Finset.mul_sum]
  apply FiniteQCombinatorial.range_bijection
  intro k hk
  have hk' : k ≤ {n} := by omega
  simp only [Nat.add_sub_cancel]
  rw [FiniteQCombinatorial.gaussian_rank_symmetry {q} {n} k hk']
  rw [FiniteQCombinatorial.reciprocal_weight {u} (by assumption) {n} k hk']
  ring'''
    if plan['rule']!='geometric_choices':return prefix+SCRIPTS[plan['rule']]
    z,q,n=map(term,plan['parameters'])
    return prefix+f'''  calc
    _ = ∑ k ∈ Finset.range ({n}+1), (-{z})^k * ({q}^(k*(k-1)/2)*FiniteQBenchmark.gaussian {q} {n} k) := by
      apply Finset.sum_congr rfl
      intro k hk
      rw [show (-{z})^k = (-1)^k*{z}^k by rw [neg_eq_neg_one_mul {z}, mul_pow]]
      ring
    _ = ∑ s ∈ (Finset.range {n}).powerset, (-{z})^s.card * ∏ i ∈ s, {q}^i :=
      FiniteQCombinatorial.geometric_rank_sum {q} (fun k => (-{z})^k) {n}
    _ = FiniteQBenchmark.poch {z} {q} {n} := by
      rw [FiniteQCombinatorial.weighted_choices]
      simp only [FiniteQBenchmark.poch, sub_eq_add_neg, neg_mul]'''


def map_certificate(plan):
    if plan['rule']=='conjunction':
        return dict(assembly='And.intro; all leaves required',children=[map_certificate(p) for p in plan['children']])
    return dict(MAPS[plan['rule']],reverse=plan.get('reverse',False))


def prepare(source,work):
    env,deps=environment(work);raw=extract(source,work,env);candidates=plans(raw)
    save(work/'environment.json',{'dependencies':deps,'lean_path':env['LEAN_PATH'],
        'expression':raw,'plans':candidates,'goal_diagnostics':diagnostics(raw),
        'plan_combination_limit':32,'source_text_sha256':hashlib.sha256(source.encode()).hexdigest(),
        'artifacts':[{'path':str(p),'sha256':sha(p)} for p in sorted((work/'deps').rglob('*.olean'))]})
    return [{'backend':b,'applicable':any(p['backend']==b for p in candidates),
             'reason':'actual finite-object structure; all map and weight obligations remain kernel checked' if any(p['backend']==b for p in candidates)
             else 'no supported finite-object representation/map template'} for b in BACKENDS]


def prove_source(text,source,work,env,data,budget,backend):
    if backend not in BACKENDS:raise ValueError('backend outside selected method')
    if hashlib.sha256(text.encode()).hexdigest()!=data['source_text_sha256']:raise ValueError('analysis/source mismatch')
    if data['plans']!=plans(data['expression']):raise ValueError('analysis plan changed')
    report={'backend':backend,'dependencies':data['dependencies'],'status':'search_exhausted',
            'goal_diagnostics':diagnostics(data['expression']),
            'construction':{'attempts':[]},'remaining_obligations':['No candidate closed representation, map, weight and fixed-point obligations']}
    deadline=time.monotonic()+budget['symbolic_seconds']
    for index,plan in enumerate(p for p in data['plans'] if p['backend']==backend):
        remaining=deadline-time.monotonic()
        if remaining<=0:report['status']='resource_exhausted';break
        script='  classical\n'+proof_script(plan)+'\n  done'
        file=work/f'Candidate{index:02d}.lean';file.write_text(slot(text,script)+'\n#print axioms '+source['theorem']+'\n')
        try:r=lean(file,env,timeout=remaining)
        except subprocess.TimeoutExpired:report['status']='resource_exhausted';break
        log=work/f'candidate{index:02d}.json';save(log,{'plan':plan,'lean':r})
        report['construction']['attempts'].append({'plan':plan,'exit_code':r['exit_code'],'log':str(log)})
        if r['exit_code'] or 'sorryAx' in r['output']:continue
        proof=work/'Proof.lean';proof.write_bytes(file.read_bytes());cert=work/'certificate.json'
        save(cert,{'schema_version':1,'kind':backend,'source_sha256':source['sha256'],'proof_sha256':sha(proof),
             'expression':data['expression'],'map_certificate':map_certificate(plan),
             'plan':plan,'proof_script':script,'remaining_obligations':[]})
        report.update(status='proved',remaining_obligations=[],certificate={'path':str(cert),'sha256':sha(cert)},
                      verification={'proof_file':str(proof),'proof_sha256':sha(proof),'lean':r})
        break
    save(work/'combinatorial_report.json',report);return report
