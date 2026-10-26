"""Original goal -> exact certificates -> finite-zero theorem -> Lean audit.

No benchmark-ID routing, pre-proved q identities, or cross-method solver calls.
"""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess

from workflow.contracts import HERE,ROOT,save,sha
from .algebra import walk,zero_certificate,principal_certificate

DIRECTORY=HERE/'interpolation/lean'
PREP="repeat' apply And.intro\nall_goals (try simp_all only [FiniteQBenchmark.jackson, ite_false, ite_true])"
CLEAR=('all_goals (try field_simp (disch := first '
       '| (solve | norm_num) '
       '| (solve | simp_all [sub_eq_zero, mul_ne_zero, add_comm, ← sub_eq_add_neg]) '
       '| (apply Ne.symm; solve | simp_all [sub_eq_zero, mul_ne_zero, add_comm, ← sub_eq_add_neg]) '
       '| (solve | field_simp_discharge)))')


def lean(path,env,*args,timeout=120):
    toolchain=(ROOT/'project/lean-toolchain').read_text().strip().replace('/','--').replace(':','---')
    executable=Path.home()/'.elan/toolchains'/toolchain/'bin/lean'
    packages=sorted((ROOT/'project/.lake/packages').glob('*/.lake/build/lib/lean'))
    env=dict(env,LEAN_PATH=os.pathsep.join([env.get('LEAN_PATH',''),*map(str,packages)]))
    p=subprocess.run([str(executable),*args,str(path)],cwd=ROOT/'project',env=env,
                     capture_output=True,text=True,timeout=timeout)
    return {'exit_code':p.returncode,'output':p.stdout+p.stderr}


def slot(source,proof):
    from workflow.preprocessed import slot as shared_slot
    shared=shared_slot(source,indent(proof),('Benchmark.InterpolationAtoms','Benchmark.InterpolationRules','Benchmark.InterpolationExport'))
    if shared is not None:return shared
    pattern=r'(?m)^  sorry\s*$'
    if len(re.findall(pattern,source))!=1:raise ValueError('one frozen proof slot required')
    source=re.sub(r'^import[^\n]*$','import Benchmark.InterpolationAtoms\nimport Benchmark.InterpolationRules\nimport Benchmark.InterpolationExport',source,flags=re.M)
    return re.sub(pattern,lambda _:indent(proof),source)


def indent(text,n=2):return '\n'.join(' '*n+line for line in text.splitlines())


def environment(work):
    from workflow.preprocessed import environment as shared_environment
    shared=shared_environment(work,'interpolation')
    if shared is not None:return shared
    src,obj=work/'sources',work/'deps'
    (src/'Benchmark').mkdir(parents=True);(obj/'Benchmark').mkdir(parents=True)
    env=dict(os.environ,LEAN_PATH=str(obj));deps=[]
    def dependency(path):deps.append({'path':str(path.relative_to(ROOT)),'sha256':sha(path)})
    def compile(name,text):
        file=src/'Benchmark'/f'{name}.lean';file.write_text(text)
        result=lean(file,env,'-R',str(src),'-o',str(obj/'Benchmark'/f'{name}.olean'))
        save(work/f'{name}_compile.json',result)
        if result['exit_code']:raise ValueError('dependency compile failed: '+result['output'])
    file=ROOT/'benchmark/lean/Benchmark/Definitions.lean';dependency(file);compile('Definitions',file.read_text())
    file=ROOT/'benchmark/lean/Benchmark/BatchDefinitions.lean';dependency(file)
    definitions=[]
    for name in ('regular','jackson'):
        found=re.search(r'(?m)^def '+name+r'\b[^\n]*(?:\n[ \t]+[^\n]*)*\n',file.read_text())
        if found is None:raise ValueError('frozen definition changed: '+name)
        definitions.append(found[0])
    compile('InterpolationAtoms','import Mathlib.Analysis.Calculus.Deriv.Basic\nimport Mathlib.Analysis.Complex.Basic\nimport Benchmark.Definitions\nnamespace FiniteQBenchmark\n'
            'noncomputable section\nvariable {K : Type*} [Field K]\n'+'\n'.join(definitions)+'\nend\nend FiniteQBenchmark\n')
    for name in ('Rules','Export'):
        file=DIRECTORY/f'{name}.lean';dependency(file);compile('Interpolation'+name,file.read_text())
    dependency(Path(__file__));dependency(HERE/'interpolation/algebra.py')
    return env,deps


def probe(source,script,work,env,name):
    file=work/(name+'.lean');file.write_text(slot(source,script))
    result=lean(file,env);save(work/(name+'.json'),result)
    rows=[json.loads(line.split('INTERPOLATION_JSON:',1)[1]) for line in result['output'].splitlines() if 'INTERPOLATION_JSON:' in line]
    errors=re.findall(r'\berror:',result['output'])
    if not rows or len(errors)!=len(rows) or result['output'].count('error: INTERPOLATION_EXPORT_ONLY')!=len(rows):
        raise ValueError('representation or denominator obligation unresolved: '+result['output'][:4000])
    return {row['label']:row['goals'] for row in rows}


def prepare(source,work):
    env,deps=environment(work)
    initial=probe(source,PREP+'\ninterpolation_export "initial"',work,env,'Initial')['initial']
    def depth(node):
        children=[depth(x) for x in node.get('args',[])]+([depth(node['arg'])] if 'arg' in node else [])
        return int(node['op'] in ('HDiv.hDiv','inv'))+max(children,default=0)
    rational=any(x['op'] in ('HDiv.hDiv','inv') for g in initial for side in ('lhs','rhs') for x in walk(g[side]))
    nested=any(depth(g[side])>1 for g in initial for side in ('lhs','rhs'))
    candidates=[{'backend':'polynomial_interpolation','applicable':bool(initial),
                 'reason':'scalar equality candidate; certified shifts, reciprocal clearing, finite Lagrange parameter families or bounded polynomial; all conditions checked in Lean'},
                {'backend':'rational_principal_parts','applicable':bool(initial) and rational,
                 'reason':'rational syntax exposed; symbolic simple-pole family or exact explicit split-pole decomposition; complete original-domain reconstruction required'}]
    if nested:candidates.reverse()
    save(work/'environment.json',{'dependencies':deps,'lean_path':env['LEAN_PATH'],
        'artifacts':[{'path':str(p),'sha256':sha(p)} for p in sorted(obj_path(work).rglob('*.olean'))],
        'semantic_objects':[node['semantic'] for goal in initial for side in ('lhs','rhs') for node in walk(goal[side]) if node.get('semantic')],
        'initial':initial,'source_text_sha256':hashlib.sha256(source.encode()).hexdigest()})
    return candidates


def obj_path(work):return work/'deps'


def close_goals(goals,max_degree):
    certificates=[];proofs=[]
    for goal in goals:
        certificate,proof=zero_certificate(goal,max_degree)
        certificates.append(certificate);proofs.append(proof)
    return certificates,'\n'.join('·\n'+indent(proof) for proof in proofs)


def prove_source(text,source,work,env,data,budget,backend):
    if hashlib.sha256(text.encode()).hexdigest()!=data['source_text_sha256']:raise ValueError('source/analysis mismatch')
    report={'backend':backend,'status':'construction_failed','dependencies':data['dependencies'],
            'construction':{},'semantic_objects':data.get('semantic_objects',[]),'remaining_obligations':['Construct and verify the complete certificate']}
    try:
        certificates=[];principal=[]
        if backend not in ('polynomial_interpolation','rational_principal_parts'):
            raise ValueError('inactive interpolation backend')
        tactic='interpolation_symbolic' if backend=='polynomial_interpolation' else 'interpolation_principal'
        symbolic_proof=PREP+'\nall_goals (solve | '+tactic+')\ndone'
        trial=work/'SymbolicBridge.lean';trial.write_text(slot(text,symbolic_proof))
        trial_result=lean(trial,env,timeout=budget['symbolic_seconds'])
        save(work/'symbolic_bridge.json',trial_result)
        schemas=re.findall(r'INTERPOLATION_CERTIFICATE:([a-z_]+)',trial_result['output'])
        report['symbolic_attempt']={'exit_code':trial_result['exit_code'],'constructors':schemas,
            'log':str(work/'symbolic_bridge.json'),
            'failure_meaning':'No declared structural constructor closed all original obligations' if trial_result['exit_code'] else None}
        if trial_result['exit_code']==0:
            if not schemas:raise ValueError('symbolic proof has no constructor trace')
            certificates=[{'kind':'symbolic_polynomial_certificate','constructor':schema,
                'parameters':'instantiated by Lean from the original goal; no identity-ID lookup',
                'closure':'certified parameter polynomial, symbolic degree, distinct roots or Lagrange reconstruction',
                'domain':'all constructor conditions discharged in original context',
                'proof_script':symbolic_proof} for schema in schemas]
            if backend=='rational_principal_parts':
                principal=[{'kind':'symbolic_simple_pole_family','constructor':schema,
                    'polynomial_part':'proper rational function; degree numerator < degree denominator',
                    'domain':'pairwise distinct poles and evaluation away from every pole'} for schema in schemas]
            proof=symbolic_proof
        elif backend=='polynomial_interpolation':
            prefix=PREP+'\n'+CLEAR
            goals=probe(text,prefix+'\ninterpolation_export "cleared"',work,env,'Cleared')['cleared']
            certificates,closure=close_goals(goals,budget['max_degree'])
            proof=prefix+'\n'+closure+'\ndone'
        elif backend=='rational_principal_parts':
            initial=data['initial'];commons=[]
            for goal in initial:
                cert,common=principal_certificate(goal);principal.append(cert);commons.append(common)
            def bridges(closures=None):
                result=[PREP]
                for i,(goal,common) in enumerate(zip(initial,commons)):
                    left=' '.join(goal['lhs_display'].split());right=' '.join(goal['rhs_display'].split())
                    result.append('· calc\n    '+left+' = '+common+' := by')
                    for side in ('left','right'):
                        if side=='right':result.append('    _ = '+right+' := by')
                        label=f'{i}_{side}'
                        body=CLEAR+'\n'+(f'interpolation_export "{label}"' if closures is None else closures[label]+'\ndone')
                        result.append(indent(body,6))
                return '\n'.join(result)
            cleared=probe(text,bridges(),work,env,'Reconstruction')
            closures={}
            for label,goals in cleared.items():
                cs,closure=close_goals(goals,budget['max_degree']);closures[label]=closure
                certificates.extend(dict(c,bridge=label) for c in cs)
            proof=bridges(closures)+'\ndone'
        else:raise ValueError('inactive interpolation backend')
        report['construction']={'principal_parts':principal,'zero_certificates':certificates}
        file=work/'Proof.lean';file.write_text(slot(text,proof)+'\n#print axioms '+source['theorem']+'\n')
        result=lean(file,env,timeout=budget['symbolic_seconds']);save(work/'lean.json',result)
        report['verification']={'proof_file':str(file),'proof_sha256':sha(file),'lean':result}
        if result['exit_code'] or 'sorryAx' in result['output']:
            report['status']='lean_failed'
        else:
            certificate=work/'certificate.json'
            save(certificate,{'schema_version':1,'kind':backend,'source_sha256':source['sha256'],
                'proof_sha256':sha(file),'principal_parts':principal,'zero_certificates':certificates,
                'proof_script':proof,'remaining_obligations':[],
                'domain_policy':'No new assumptions; node distinctness, degree, roots and denominators discharged in original context'})
            report.update(status='proved',remaining_obligations=[],
                          certificate={'path':str(certificate),'sha256':sha(certificate)})
    except (ValueError,NotImplementedError) as exc:report['error']=str(exc)
    save(work/'interpolation_report.json',report)
    return report
