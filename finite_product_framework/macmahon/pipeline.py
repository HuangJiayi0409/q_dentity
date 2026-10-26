"""Finite Laurent-polynomial MacMahon Omega certificates (not rational CTEuclid)."""
import hashlib
import json
import os
import re
from pathlib import Path
from workflow import structural
from workflow.contracts import HERE, ROOT, save, sha
from product.pipeline import lean, assemble  # compiler/text utilities only
SPEC=dict(method='macmahon',module='MacMahonRules',backend='finite_omega_elimination',
 atoms=[('BatchDefinitions.lean',['rectangle','rectangleWeight'])],
 supported=lambda r: any(c in r['constants'] for c in (
     'FiniteQMacMahon.omegaGE','FiniteQMacMahon.omegaAll','FiniteQBenchmark.rectangleWeight',
     'FiniteQMacMahon.rectangleSeries','FiniteQMacMahon.coneProduct',
     'FiniteQMacMahon.geometric','FiniteQMacMahon.gaussianSeries')),
 scope='finite Omega plus symbolic chain elimination into a factorized formal generating function',
 obligations=['Close unsupported object encoding, constraint elimination, coefficient or index obligations; only certified chain/cone patterns and finite Omega are supported, not general CTEuclid'],
 stages=['elaborate original expression in definition-only environment',
         'encode signed linear constraints in finite Laurent exponents',
         'convolve factors BEFORE Omega projection; verify finite support and nonnegative exponent filtering',
         'eliminate finite constraints, or apply the certified head elimination of an antitone chain',
         'construct formal geometric-factor product and verify its denominator certificate',
         'compare coefficients with the Gaussian definition using shared local polynomial rules (no recurrence pipeline)',
         'reconstruct exact original goal in Lean and audit source, dependencies and axioms'],
 plans=[('chain_geometric_elimination','  macmahon_chain\n  done'),
        ('finite_omega','  macmahon_eliminate\n  done'),
        ('rectangle_constraints','  rw [← FiniteQMacMahon.rectangle_omega]\n  macmahon_eliminate\n  done')])
def prepare(source,work):
    """Definition-only environment plus shared Gaussian LOCAL rules, never target proofs.

    Kept local because the chain backend requires two extra modules; existing
    methods and their frozen dependency records remain unchanged.
    """
    from workflow.preprocessed import prepare_structural
    shared=prepare_structural(source,work,SPEC)
    if shared is not None:return shared
    src,obj=work/'sources',work/'deps'
    (src/'Benchmark').mkdir(parents=True);(obj/'Benchmark').mkdir(parents=True)
    env=dict(os.environ,LEAN_PATH=str(obj));deps=[]
    def track(p):
        deps.append(dict(path=str(p.relative_to(ROOT)),sha256=sha(p)))
        return p.read_text()
    def compile(name,text):
        f=src/'Benchmark'/f'{name}.lean';f.write_text(text)
        r=lean(f,env,'-R',str(src),'-o',str(obj/'Benchmark'/f'{name}.olean'))
        save(work/f'{name}_compile.json',r)
        if r['exit_code']:raise ValueError('dependency_compile_failed: '+r['output'])
    compile('Definitions',track(ROOT/'benchmark/lean/Benchmark/Definitions.lean'))
    atoms=[]
    for filename,names in SPEC['atoms']:
        text=track(ROOT/'benchmark/lean/Benchmark'/filename)
        for name in names:
            match=re.search(r'(?ms)^def '+re.escape(name)+r'\b.*?(?=^def |^/--|^end |\Z)',text)
            if match is None:raise ValueError('missing frozen definition: '+name)
            atoms.append(match[0])
    compile('StructuralAtoms',"""import Benchmark.Definitions
noncomputable section
namespace FiniteQBenchmark
open scoped BigOperators
variable {K : Type*} [Field K]
"""+''.join(atoms)+"""
end FiniteQBenchmark
""")
    text=track(ROOT/'benchmark/lean/Benchmark/Gaussian.lean')
    basic=text.split('namespace FiniteQBenchmark',1)[1].split('/-- Algebraic recurrence',1)[0]
    compile('Gaussian',"""import Benchmark.Definitions
namespace FiniteQBenchmark"""+basic+"""end FiniteQBenchmark
""")
    compile('GaussianRules',track(HERE/'p1/lean/GaussianRules.lean'))
    compile(SPEC['module'],track(HERE/'macmahon/lean/Rules.lean'))
    for p in [Path(__file__),HERE/'workflow/structural.py',HERE/'workflow/StructuralExport.lean',HERE/'product/pipeline.py']:track(p)
    probe=work/'Extract.lean'
    probe.write_text(assemble((HERE/'workflow/StructuralExport.lean').read_text(),structural.slot(source,'  structural_export',SPEC['module'])))
    result=lean(probe,env);save(work/'extraction.json',result)
    lines=[l.split('STRUCTURAL_JSON:',1)[1] for l in result['output'].splitlines() if 'STRUCTURAL_JSON:' in l]
    if len(lines)!=1 or len(re.findall(r'\berror:',result['output']))!=1 or 'STRUCTURAL_EXPORT_ONLY' not in result['output']:
        save(work/'environment.json',dict(dependencies=deps,extraction=result))
        raise RuntimeError('Omega analysis did not elaborate the input; see extraction.json')
    raw=json.loads(lines[0]);ok=SPEC['supported'](raw)
    save(work/'environment.json',dict(dependencies=deps,lean_path=str(obj),expression=raw,
         source_text_sha256=hashlib.sha256(source.encode()).hexdigest(),
         artifacts=[dict(path=str(p),sha256=sha(p)) for p in sorted(obj.rglob('*.olean'))]))
    return [dict(backend=SPEC['backend'],applicable=ok,reason=SPEC['scope'] if ok else 'supported Omega/chain expression absent')]

def prove_source(text,source,work,env,data,budget):
    constants=set(data['expression']['constants'])
    chain=bool(constants & {'FiniteQBenchmark.rectangleWeight',
        'FiniteQMacMahon.rectangleEncoding','FiniteQMacMahon.rectangleSeries',
        'FiniteQMacMahon.coneProduct','FiniteQMacMahon.geometric','FiniteQMacMahon.gaussianSeries'})
    spec=dict(SPEC)
    spec['plans']=[(name,script) for name,script in SPEC['plans']
        if (name!='chain_geometric_elimination' or chain)
        and (name!='rectangle_constraints' or 'FiniteQBenchmark.rectangleWeight' in constants)]
    return structural.prove_source(text,source,work,env,data,budget,spec)
