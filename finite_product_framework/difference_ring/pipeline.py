"""Independent evaluated triangular difference-ring proof pipeline.

Target-guided local shift/inductive invariant reduction, not a general Karr or
Sigma implementation. Never imports another method's solver or target proofs.
"""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time
from workflow.contracts import HERE,ROOT,save,sha
from product.pipeline import lean,assemble  # process/text utilities
from .algebra import reduce_goal

LEAN=HERE/'difference_ring/lean'
BACKEND='triangular_difference_ring'


def slot(source,proof):
    from workflow.preprocessed import slot as shared_slot
    shared=shared_slot(source,proof,('Benchmark.DifferenceRules',))
    if shared is not None:return shared
    if len(re.findall(r'(?m)^  sorry\s*$',source))!=1:raise ValueError('one deferred proof slot required')
    source=re.sub(r'^import[^\n]*$','import Benchmark.DifferenceRules',source,flags=re.M)
    return re.sub(r'(?m)^  sorry\s*$',lambda _:proof,source)


def environment(work):
    from workflow.preprocessed import environment as shared_environment
    shared=shared_environment(work,'difference_ring')
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
    atoms=[]
    for filename,name in [('Batch4Definitions.lean','fineC'),('BatchDefinitions.lean','regular')]:
        file=ROOT/'benchmark/lean/Benchmark'/filename;dep(file)
        m=re.search(r'(?m)^def '+name+r'\b[^\n]*\n',file.read_text())
        if m is None:raise ValueError('frozen definition changed: '+name)
        atoms.append(m[0])
    compile('DifferenceAtoms','import Benchmark.Definitions\nnoncomputable section\nnamespace FiniteQBenchmark\nvariable {K : Type*} [Field K]\n'+''.join(atoms)+'end FiniteQBenchmark\n')
    dep(LEAN/'Rules.lean');compile('DifferenceRules',(LEAN/'Rules.lean').read_text())
    for path in (LEAN/'Structure.lean',LEAN/'Export.lean',Path(__file__),HERE/'difference_ring/algebra.py',
                 HERE/'difference_ring/core_bridge.py',HERE/'product/pipeline.py'):dep(path)
    for path in sorted((HERE/'p1').glob('*.py')):
        if not path.name.startswith('test_'):dep(path)
    return env,deps


def probe(source,script,work,env,label,timeout=120):
    structure=label=='Structure';prefix='DIFFERENCE_STRUCTURE' if structure else 'DIFFERENCE'
    exporter=LEAN/('Structure.lean' if structure else 'Export.lean')
    file=work/f'{label}.lean';file.write_text(assemble(exporter.read_text(),slot(source,script)))
    r=lean(file,env,timeout=timeout);save(work/f'{label}.json',r)
    lines=[line.split(prefix+'_JSON:',1)[1] for line in r['output'].splitlines() if prefix+'_JSON:' in line]
    if structure:lines=[line.split('DIFFERENCE_STRUCTURE:',1)[1] for line in r['output'].splitlines() if 'DIFFERENCE_STRUCTURE:' in line]
    marker='DIFFERENCE_STRUCTURE_ONLY' if structure else 'DIFFERENCE_EXPORT_ONLY'
    if len(lines)!=1 or marker not in r['output'] or len(re.findall(r'\berror:',r['output']))!=1:
        raise ValueError('representation/shift/denominator obligations not closed: '+r['output'])
    return json.loads(lines[0])


def nodes(node):
    yield node
    for child in node.get('args',[]):yield from nodes(child)
    if 'body' in node:yield from nodes(node['body'])


def tower(raw):
    result=[]
    for node in reversed(list(nodes(raw['target']))):
        op=node['op']
        if op in ('Finset.sum','Finset.prod'):
            if node['args'][0]['op']!='Finset.range':raise ValueError('only natural prefix domains in first version')
            kind='Sigma' if op=='Finset.sum' else 'product'
            result.append({'kind':kind,'expression':node.get('text'),
                'evaluation_rule':'sum_range_succ' if kind=='Sigma' else 'prod_range_succ',
                'initial_value':0 if kind=='Sigma' else 1,
                'transition':'S(k+1)=S(k)+f(k)' if kind=='Sigma' else 'P(k+1)=P(k)*f(k)'})
        if op=='FiniteQBenchmark.poch':result.append({'kind':'product','expression':node.get('text'),
            'evaluation_rule':'FiniteQDifference.poch_shift','initial_value':1,
            'transition':'P(k+1)=P(k)*(1-a*q^k)'})
    if not result:raise ValueError('no supported sum/product tower exposed')
    return result


def plans(raw):
    tower(raw)
    from .core_bridge import frontend,BridgeGap
    try:frontend(raw);core=[{'mode':'core_antidifference'}]
    except (BridgeGap,ValueError,NotImplementedError):core=[]
    return core+[{'mode':'local_shift'}]+[{'mode':'invariant','index':n} for n in raw['indices'][:4]]


def prepare(source,work):
    env,deps=environment(work)
    raw=probe(source,'  dr_expand\n  dr_structure',work,env,'Structure')
    try:candidates=plans(raw);extensions=tower(raw);reason='evaluated sum/product tower with kernel-checked shift rules'
    except ValueError as exc:candidates=[];extensions=[];reason=str(exc)
    save(work/'environment.json',{'dependencies':deps,'lean_path':env['LEAN_PATH'],
        'expression':raw,'plans':candidates,'tower':extensions,'source_text_sha256':hashlib.sha256(source.encode()).hexdigest(),
        'artifacts':[{'path':str(p),'sha256':sha(p)} for p in sorted((work/'deps').rglob('*.olean'))]})
    return [{'backend':BACKEND,'applicable':bool(candidates),'reason':reason,
             'admission_checks':dict(representation='accepted' if candidates else 'rejected',
                 core_domain='unknown',proof_exit='conditional' if candidates else 'unavailable',
                 branches=dict(strong_core_source_bridge=any(p['mode']=='core_antidifference' for p in candidates),
                               evaluated_local_tower=bool(candidates)),
                 obligations=['Core tower admissibility, constructed witness, evaluated shifts and both original endpoints'])}]


def prefix(plan):
    lines=['  classical','  dr_expand']
    if plan['mode']=='invariant':
        name=plan['index']
        if not re.fullmatch(r'[A-Za-z_][A-Za-z_0-9]*',name):raise ValueError('unsupported index name')
        lines.append('  induction '+name)
    lines.append('  all_goals dr_shift')
    lines.append('  all_goals dr_name_locals')
    return '\n'.join(lines)


def prove_source(text,source,work,env,data,budget):
    if hashlib.sha256(text.encode()).hexdigest()!=data['source_text_sha256']:raise ValueError('analysis/source mismatch')
    if data['plans']!=plans(data['expression']) or data['tower']!=tower(data['expression']):raise ValueError('analysis data changed')
    report={'backend':BACKEND,'dependencies':data['dependencies'],'status':'search_exhausted',
        'construction':{'attempts':[]},'remaining_obligations':['No plan closed evaluation, initial, shift and domain obligations']}
    deadline=time.monotonic()+budget['symbolic_seconds']
    for index,plan in enumerate(data['plans']):
        if time.monotonic()>=deadline:report['status']='resource_exhausted';break
        attempt={'plan':plan};report['construction']['attempts'].append(attempt)
        try:
            core_certificate=None
            if plan['mode']=='core_antidifference':
                from .core_bridge import frontend,construct
                core_certificate=construct(frontend(data['expression']),dict(budget,symbolic_seconds=max(.01,deadline-time.monotonic())))
                save(work/'strong_core.json',core_certificate)
                script=core_certificate['proof_script'];goals=[];certificates=[]
                attempt['core_solver']='difference_field'
            else:
                start=prefix(plan)
                goals=probe(text,start+'\n  dr_export',work,env,f'Probe{index}',timeout=max(.01,deadline-time.monotonic()))
                certificates=[reduce_goal(g,dict(budget,symbolic_seconds=max(.01,deadline-time.monotonic()))) for g in goals]
                script=start+'\n'+''.join('  · '+c['script']+'\n    done\n' for c in certificates)+'  done'
            file=work/f'Candidate{index}.lean';file.write_text(slot(text,script)+'\n#print axioms '+source['theorem']+'\n')
            r=lean(file,env,timeout=max(.01,deadline-time.monotonic()));save(work/f'candidate{index}.json',r)
            attempt['exit_code']=r['exit_code']
            if r['exit_code'] or 'sorryAx' in r['output']:continue
            proof=work/'Proof.lean';proof.write_bytes(file.read_bytes());cert=work/'certificate.json'
            save(cert,{'schema_version':1,'kind':BACKEND,'source_sha256':source['sha256'],'proof_sha256':sha(proof),
                'tower':data['tower'],'plan':plan,'normalized_goals':goals,'reductions':certificates,'proof_script':script,
                'strong_core':core_certificate,
                'semantics':'evaluated triangular sequence ring; no algebraic-independence or constant-field claim',
                'remaining_obligations':[]})
            report.update(status='proved',remaining_obligations=[],certificate={'path':str(cert),'sha256':sha(cert)},
                verification={'proof_file':str(proof),'proof_sha256':sha(proof),'lean':r})
            break
        except (ValueError,subprocess.TimeoutExpired) as exc:attempt['error']=str(exc)
    save(work/'difference_ring_report.json',report);return report
