"""Build the reusable Lean library in an isolated, explicitly requested output.

Only mathematical definitions and local library rules are loaded. In particular,
the Batch3Definitions import of completed identity proofs is not imported here:
the registered nonrecursive geometric definition is copied with source hashes.
"""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess

from .registry import Library, LibraryError, dependency_files

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]


def extra_definitions():
    """Shared by standalone builds and the existing P1 source environment."""
    lib=Library()
    return sorted({(Path(obj['source']).stem,obj['declaration']) for obj in lib.objects.values()
                   if Path(obj['source']).stem!='Definitions'})


def prepare(output):
    output=Path(output).resolve();output.mkdir(parents=True,exist_ok=False)
    src=output/'sources';obj=output/'build'
    (src/'Benchmark').mkdir(parents=True);(obj/'Benchmark').mkdir(parents=True)
    env=dict(os.environ,LEAN_PATH=str(obj));deps=[];modules=[]
    def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
    def track(path):
        record=dict(path=str(path.relative_to(ROOT)),sha256=digest(path))
        if record not in deps:deps.append(record)
    def compile_module(name,text):
        file=src/'Benchmark'/(name+'.lean');file.write_text(text)
        run=subprocess.run(['lake','env','lean','-R',str(src),'-o',str(obj/'Benchmark'/(name+'.olean')),str(file)],
            cwd=ROOT/'project',env=env,text=True,capture_output=True,timeout=180)
        result=dict(exit_code=run.returncode,output=run.stdout+run.stderr)
        (output/(name+'_compile.json')).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
        if run.returncode:raise LibraryError('library_compile_failed: '+name+': '+result['output'])
        modules.append(name)
        return result
    path=ROOT/'benchmark/lean/Benchmark/Definitions.lean';track(path)
    compile_module('Definitions',path.read_text())
    declarations=[]
    for filename,name in extra_definitions():
        path=ROOT/'benchmark/lean/Benchmark'/(filename+'.lean');track(path)
        match=re.search(r'(?m)^def '+re.escape(name)+r'\b[^\n]*(?:\n[ \t]+[^\n]*)*\n',path.read_text())
        if match is None:raise LibraryError('registered_definition_changed: '+name)
        declarations.append(match[0])
    compile_module('MathLibraryAtoms','import Benchmark.Definitions\nnamespace FiniteQBenchmark\n'
        'open scoped BigOperators\nnoncomputable section\nvariable {K : Type*} [Field K]\n'+
        '\n'.join(declarations)+'\nend\nend FiniteQBenchmark\n')
    path=HERE/'lean/Rules.lean';track(path)
    compile_module('MathLibraryRules',path.read_text())
    lib=Library()
    checks=compile_module('MathLibraryChecks','import Benchmark.MathLibraryRules\nopen scoped BigOperators\n'+
                          '\n'.join(lib.lean_check(key) for key in lib.rules))
    audits={}
    for key in lib.rules:
        match=re.search(re.escape("'check_"+key+"' depends on axioms: [")+r'([^\]]*)\]',checks['output'])
        axioms={a.strip() for a in match[1].split(',') if a.strip()} if match else set()
        found=match is not None or "'check_"+key+"' does not depend on any axioms" in checks['output']
        if not found or not axioms<={'propext','Classical.choice','Quot.sound'}:
            raise LibraryError('catalogue_axiom_audit_failed: '+key)
        audits[key]=sorted(axioms)
    for path in dependency_files():track(path)
    for name in ('lean-toolchain','lake-manifest.json'):track(ROOT/'project'/name)
    result=dict(status='verified_catalogue',catalog_sha256=lib.sha256,objects=len(lib.objects),rules=len(lib.rules),
        modules=modules,lean_path=str(obj),dependencies=deps,
        artifacts=[dict(path=str(p),sha256=digest(p)) for p in sorted(obj.rglob('*.olean'))],
        machine_templates_checked=True,axioms=audits,original_identity_proved=False)
    (output/'manifest.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    return result
