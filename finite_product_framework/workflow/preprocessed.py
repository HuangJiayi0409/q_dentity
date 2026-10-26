"""Method-side consumption of the shared, proof-carrying preprocessing output.

No mathematics is rewritten here. Every backend enters the same normalized
Lean goal, while its own reader and solver retain their existing domain limits.
"""
from contextlib import contextmanager
from contextvars import ContextVar
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess

from .contracts import HERE, ROOT, save, sha

ACTIVE = ContextVar('preprocessed_input', default=None)


def describe(directory):
    directory = Path(directory).resolve()
    status = json.loads((directory/'status.json').read_text())
    if status['status'] not in ('verified_normalized', 'verified_unchanged'):
        raise ValueError('preprocessing_not_verified')
    paths = [directory/x for x in ('request.json','standard.json','bundle.json','original.lean')]
    paths += sorted((directory/'build').rglob('*.olean'))
    return dict(directory=str(directory), status=status['status'],
                files=[dict(path=str(p),sha256=sha(p)) for p in paths])


def check(descriptor, source):
    for item in descriptor['files']:
        if sha(item['path']) != item['sha256']:
            raise ValueError('preprocessing_artifact_changed: '+item['path'])
    directory = Path(descriptor['directory'])
    from preprocessing.pipeline import check_snapshot
    request = json.loads((directory/'request.json').read_text())
    check_snapshot(directory, request)
    if request['source']['identity'] != source['identity'] or request['source']['sha256'] != source['sha256']:
        raise ValueError('preprocessing_source_mismatch')
    standard = json.loads((directory/'standard.json').read_text())
    if standard['evidence']['bundle_sha256'] != sha(directory/'bundle.json'):
        raise ValueError('preprocessing_bundle_mismatch')
    return request


@contextmanager
def activated(source):
    descriptor = source.get('preprocessing')
    if descriptor is not None:
        check(descriptor, source)
    token = ACTIVE.set(descriptor)
    try:
        yield
        if descriptor is not None:
            check(descriptor, source)
    finally:
        ACTIVE.reset(token)


def slot(source, proof, modules=()):
    """Return None for historical mode. Keep original theorem bytes unchanged."""
    descriptor = ACTIVE.get()
    if descriptor is None:
        return None
    directory = Path(descriptor['directory'])
    if hashlib.sha256(source.encode()).hexdigest() != sha(directory/'original.lean'):
        raise ValueError('preprocessing_slot_source_mismatch')
    pattern = r'(?m)^  sorry\s*$'
    if len(re.findall(pattern, source)) != 1:
        raise ValueError('preprocessing_proof_slot_shape')
    imports = ['import FiniteQPreprocess.Export'] + ['import '+m for m in modules]
    path = json.dumps(str(directory/'bundle.json'), ensure_ascii=False)
    script = '  preprocess_enter '+path+'\n'+proof.rstrip()+'\n'
    return '\n'.join(imports)+'\n'+re.sub(pattern,lambda _:script,source)


PROFILES = {
    'p1': [('P1Atoms', None)],
    'p2': [('P2Atoms', None), ('GaussianRules', 'p1/lean/GaussianRules.lean')],
    'product': [('ProductAtoms', None), ('ProductRules', 'product/lean/Rules.lean')],
    'interpolation': [('InterpolationAtoms', None), ('InterpolationRules','interpolation/lean/Rules.lean'),
                      ('InterpolationExport','interpolation/lean/Export.lean')],
    'noncommutative': [('OperatorAtoms', None), ('OperatorRules','noncommutative/lean/Rules.lean')],
    'difference_ring': [('DifferenceAtoms', None), ('DifferenceRules','difference_ring/lean/Rules.lean')],
    'combinatorial': [('GaussianRules','p1/lean/GaussianRules.lean'),
                      ('CombinatorialRules','combinatorial/lean/Rules.lean'),
                      ('CombinatorialRepresentation','combinatorial/lean/Representation.lean')],
    'kernel_transform': [('StructuralAtoms', None), ('KernelRules','kernel_transform/lean/Rules.lean')],
    'spectral': [('StructuralAtoms', None), ('SpectralRules','spectral/lean/Rules.lean')],
    'determinant': [('StructuralAtoms', None), ('DeterminantRules','determinant/lean/Rules.lean')],
    'macmahon': [('StructuralAtoms', None), ('GaussianRules','p1/lean/GaussianRules.lean'),
                 ('MacMahonRules','macmahon/lean/Rules.lean')],
}


def environment(work, profile):
    """Use exact shared declarations, never regex-redeclare a subset of atoms."""
    descriptor = ACTIVE.get()
    if descriptor is None:
        return None
    base = Path(descriptor['directory'])
    request = json.loads((base/'request.json').read_text())
    src, obj = work/'sources', work/'deps'
    src.mkdir(parents=True, exist_ok=True)
    shutil.copytree(base/'build', obj)
    packages = sorted((ROOT/'project/.lake/packages').glob('*/.lake/build/lib/lean'))
    env = dict(os.environ, LEAN_PATH=os.pathsep.join(map(str,[obj,*packages])))
    toolchain = (base/'lean-toolchain').read_text().strip().replace('/','--').replace(':','---')
    exe = Path.home()/'.elan/toolchains'/toolchain/'bin/lean'
    dependencies = list(request['source']['dependencies'])
    common = 'import Benchmark.Batch5Definitions\nimport FiniteQPreprocess.Export\n'
    for name, relative in PROFILES[profile]:
        path = src/'Benchmark'/f'{name}.lean'; path.parent.mkdir(parents=True, exist_ok=True)
        text = common if relative is None else (HERE/relative).read_text()
        if relative is not None:
            dependencies.append(dict(path=str((HERE/relative).relative_to(ROOT)),sha256=sha(HERE/relative)))
        path.write_text(text)
        target = obj/'Benchmark'/f'{name}.olean'
        result = subprocess.run([str(exe),'-R',str(src),'-o',str(target),str(path)],
                                cwd=src, env=env,capture_output=True,text=True,timeout=120)
        save(work/(name+'_compile.json'),dict(exit_code=result.returncode,output=result.stdout+result.stderr))
        if result.returncode:
            raise ValueError('preprocessed_method_rules_compile_failed: '+name+': '+result.stdout+result.stderr)
    # Preserve all framework source dependencies as well as the exact Lean inputs.
    for path in sorted(HERE.rglob('*')):
        if path.suffix in ('.py','.lean') and not set(path.relative_to(HERE).parts)&{'generated','__pycache__','archive'}:
            dependencies.append(dict(path=str(path.relative_to(ROOT)),sha256=sha(path)))
    save(work/'preprocessing_consumed.json',dict(directory=str(base),
         normalized=json.loads((base/'standard.json').read_text())['normalized'],
         method_profile=profile, transport='preprocess_enter_then_Eq.mpr'))
    return env, dependencies


def prepare_structural(source, work, spec):
    shared = environment(work, spec['method'])
    if shared is None:
        return None
    from product.pipeline import lean, assemble
    env, deps = shared
    script = slot(source, '  structural_export', ('Benchmark.'+spec['module'],))
    probe = work/'Extract.lean'
    probe.write_text(assemble((HERE/'workflow/StructuralExport.lean').read_text(),script))
    result = lean(probe,env)
    save(work/'extraction.json',result)
    lines = [l.split('STRUCTURAL_JSON:',1)[1] for l in result['output'].splitlines() if 'STRUCTURAL_JSON:' in l]
    if len(lines)!=1 or len(re.findall(r'\berror:',result['output']))!=1 or 'STRUCTURAL_EXPORT_ONLY' not in result['output']:
        save(work/'environment.json',dict(dependencies=deps,extraction=result))
        raise RuntimeError('shared normalized target analysis did not complete; see extraction.json')
    raw=json.loads(lines[0]); ok=spec['supported'](raw)
    save(work/'environment.json',dict(dependencies=deps,lean_path=env['LEAN_PATH'],expression=raw,
         source_text_sha256=hashlib.sha256(source.encode()).hexdigest(),
         artifacts=[dict(path=str(p),sha256=sha(p)) for p in sorted((work/'deps').rglob('*.olean'))]))
    return [dict(backend=spec['backend'],applicable=ok,reason=spec['scope'] if ok else 'required structural expression absent')]


def audit_result(result, source, work, environment_file):
    """Kernel recheck original proof and prohibit historical identity reuse."""
    if result.get('status')!='proved' or not source.get('preprocessing'):
        return result
    from product.pipeline import lean
    data=json.loads(Path(environment_file).read_text())
    env=dict(os.environ,LEAN_PATH=data['lean_path'])
    proof=Path(result['verification']['proof_file'])
    file=Path(work)/'PreprocessingAudit.lean'
    file.write_text(proof.read_text()+'\nrun_elab FiniteQPreprocess.auditCompleted ``'+source['theorem']+'\n')
    checked=lean(file,env)
    evidence=dict(file=str(file),sha256=sha(file),lean=checked,
                  source_sha256=source['sha256'],proof_sha256=sha(proof),
                  bundle_sha256=sha(Path(source['preprocessing']['directory'])/'bundle.json'))
    save(Path(work)/'preprocessing_acceptance.json',evidence)
    result['preprocessing_acceptance']=evidence
    if checked['exit_code'] or 'PREPROCESS_ORIGINAL_PROOF_AUDIT_OK' not in checked['output']:
        result.update(status='preprocessing_acceptance_failed',remaining_obligations=['Original proof dependency audit failed'])
    return result
