"""Shared isolated compilation and certificate transport; no mathematical routing."""
import hashlib,json,os,re,subprocess,time
from pathlib import Path
from workflow.contracts import HERE,ROOT,save,sha
from product.pipeline import lean,assemble

def slot(source,script,module):
    from workflow.preprocessed import slot as shared_slot
    shared=shared_slot(source,script,('Benchmark.'+module,))
    if shared is not None:return shared
    if len(re.findall(r'(?m)^  sorry\s*$',source))!=1:raise ValueError('one proof slot required')
    source=re.sub(r'^import[^\n]*$',f'import Benchmark.{module}',source,flags=re.M)
    return re.sub(r'(?m)^  sorry\s*$',lambda _:script,source)

def prepare(source,work,spec):
    from workflow.preprocessed import prepare_structural
    shared=prepare_structural(source,work,spec)
    if shared is not None:return shared
    src,obj=work/'sources',work/'deps'
    (src/'Benchmark').mkdir(parents=True);(obj/'Benchmark').mkdir(parents=True)
    env=dict(os.environ,LEAN_PATH=str(obj));deps=[]
    def track(p):deps.append(dict(path=str(p.relative_to(ROOT)),sha256=sha(p)))
    def compile(name,text):
        f=src/'Benchmark'/f'{name}.lean';f.write_text(text)
        r=lean(f,env,'-R',str(src),'-o',str(obj/'Benchmark'/f'{name}.olean'))
        save(work/f'{name}_compile.json',r)
        if r['exit_code']:raise ValueError('dependency_compile_failed: '+r['output'])
    p=ROOT/'benchmark/lean/Benchmark/Definitions.lean';track(p);compile('Definitions',p.read_text())
    atoms=[]
    for filename,names in spec.get('atoms',[]):
        p=ROOT/'benchmark/lean/Benchmark'/filename;track(p)
        for name in names:
            match=re.search(r'(?ms)^def '+re.escape(name)+r'\b.*?(?=^def |^/--|^end |\Z)',p.read_text())
            if match is None:raise ValueError('missing frozen definition: '+name)
            atoms.append(match[0])
    compile('StructuralAtoms','import Benchmark.Definitions\nnoncomputable section\nnamespace FiniteQBenchmark\nopen scoped BigOperators\nvariable {K : Type*} [Field K]\n'+''.join(atoms)+'\nend FiniteQBenchmark\n')
    rules=HERE/spec['method']/'lean/Rules.lean';track(rules)
    compile(spec['module'],rules.read_text())
    for p in [HERE/spec['method']/'pipeline.py',Path(__file__),HERE/'workflow/StructuralExport.lean',HERE/'product/pipeline.py']:track(p)
    probe=work/'Extract.lean'
    probe.write_text(assemble((HERE/'workflow/StructuralExport.lean').read_text(),slot(source,'  structural_export',spec['module'])))
    result=lean(probe,env);save(work/'extraction.json',result)
    lines=[l.split('STRUCTURAL_JSON:',1)[1] for l in result['output'].splitlines() if 'STRUCTURAL_JSON:' in l]
    if len(lines)!=1 or len(re.findall(r'\berror:',result['output']))!=1 or 'STRUCTURAL_EXPORT_ONLY' not in result['output']:
        save(work/'environment.json',{'dependencies':deps,'extraction':result})
        raise RuntimeError('structural analysis did not elaborate the input; see extraction.json')
    raw=json.loads(lines[0]);ok=spec['supported'](raw)
    save(work/'environment.json',dict(dependencies=deps,lean_path=str(obj),expression=raw,
         source_text_sha256=hashlib.sha256(source.encode()).hexdigest(),
         artifacts=[dict(path=str(p),sha256=sha(p)) for p in sorted(obj.rglob('*.olean'))]))
    return [dict(backend=spec['backend'],applicable=ok,reason=spec['scope'] if ok else 'required structural expression absent')]

def prove_source(text,source,work,env,data,budget,spec):
    if hashlib.sha256(text.encode()).hexdigest()!=data['source_text_sha256']:raise ValueError('source mismatch')
    if not spec['supported'](data['expression']):raise ValueError('unsupported representation')
    report=dict(backend=spec['backend'],dependencies=data['dependencies'],status='search_exhausted',attempts=[],
         remaining_obligations=spec['obligations'])
    deadline=time.monotonic()+budget['symbolic_seconds']
    for i,(name,script) in enumerate(spec['plans']):
        if time.monotonic()>=deadline:report['status']='resource_exhausted';break
        file=work/f'Candidate{i}.lean';file.write_text(slot(text,script,spec['module'])+'\n#print axioms '+source['theorem']+'\n')
        try:r=lean(file,env,timeout=max(.01,deadline-time.monotonic()))
        except subprocess.TimeoutExpired:report['status']='resource_exhausted';break
        save(work/f'candidate{i}.json',r);report['attempts'].append(dict(plan=name,exit_code=r['exit_code']))
        if r['exit_code'] or 'sorryAx' in r['output']:continue
        proof=work/'Proof.lean';proof.write_bytes(file.read_bytes());cert=work/'certificate.json'
        save(cert,dict(schema_version=1,kind=spec['backend'],source_sha256=source['sha256'],proof_sha256=sha(proof),
             expression=data['expression'],plan=name,proof_script=script,stages=spec['stages'],remaining_obligations=[]))
        report.update(status='proved',remaining_obligations=[],certificate=dict(path=str(cert),sha256=sha(cert)),
             verification=dict(proof_file=str(proof),proof_sha256=sha(proof),lean=r));break
    save(work/(spec['method']+'_report.json'),report);return report
