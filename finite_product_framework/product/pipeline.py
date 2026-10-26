"""Bounded structural search for finite-index certificates, reconstructed in Lean.

Production selection depends on elaborated expressions, never an identity name.
Only generic product lemmas and the frozen definitions are imported. Search is
incomplete; every success is a proof of the original, unchanged declaration.
"""
import json
import os
from pathlib import Path
import re
import subprocess
import time

from workflow.contracts import HERE, ROOT, save, sha

LEAN_DIR = HERE / 'product/lean'
EXPAND = ('try simp only [FiniteQBenchmark.pochList, List.map_cons, List.map_nil, '
          'List.prod_cons, List.prod_nil, mul_one, FiniteQBenchmark.poch]')
SMALL = ('try simp only [Finset.prod_range_succ, Finset.prod_range_zero, '
         'mul_one, one_mul, Nat.mul_zero, Nat.add_zero, Nat.zero_add, pow_zero, pow_one]')
FUSE = 'try simp only [← Finset.prod_mul_distrib]'
RULES = {
    'residues': ('FiniteQProduct.prod_range_residues', 'k = m*i+j; 0≤j<m, 0≤i<n; transpose block grid'),
    'blocks': ('FiniteQProduct.prod_range_blocks', 'k = m*i+j; 0≤i<n, 0≤j<m; disjoint consecutive blocks'),
    'split': ('Finset.prod_range_add', '[0,n+k) = [0,n) disjoint-union (n+[0,k))'),
    'head': ('FiniteQProduct.prod_range_head', 'k=0 or k=j+1; positivity proved from original hypotheses'),
    'transpose': ('Finset.prod_comm', 'exchange two independent finite index domains'),
    'reflect': ('← Finset.prod_range_reflect', 'k ↦ n-1-k on [0,n), including empty range'),
}


def lean(path, env, *args, timeout=120):
    p = subprocess.run(['lake', 'env', 'lean', *args, str(path)], cwd=ROOT/'project',
                       env=env, capture_output=True, text=True, timeout=timeout)
    return {'exit_code': p.returncode, 'output': p.stdout+p.stderr}


def slot(source, proof):
    from workflow.preprocessed import slot as shared_slot
    shared=shared_slot(source,proof,('Benchmark.ProductAtoms','Benchmark.ProductRules'))
    if shared is not None:return shared
    pattern = r'(?m)^  sorry\s*$'
    if len(re.findall(pattern, source)) != 1:
        raise ValueError('one deferred proof slot required')
    source = re.sub(r'^import[^\n]*$', 'import Benchmark.ProductAtoms\nimport Benchmark.ProductRules',
                    source, flags=re.M)
    return re.sub(pattern, lambda _: proof.rstrip(), source)


def assemble(*texts):
    imports, body = [], []
    for text in texts:
        for line in text.splitlines():
            if line.startswith('import '):
                if line not in imports: imports.append(line)
            else: body.append(line)
    return '\n'.join(imports+['']+body)+'\n'


def environment(work):
    from workflow.preprocessed import environment as shared_environment
    shared=shared_environment(work,'product')
    if shared is not None:return shared
    src, obj = work/'sources', work/'deps'
    (src/'Benchmark').mkdir(parents=True)
    (obj/'Benchmark').mkdir(parents=True)
    env = dict(os.environ, LEAN_PATH=str(obj))
    deps = []

    def dependency(path):
        deps.append({'path': str(path.relative_to(ROOT)), 'sha256': sha(path)})

    def compile_module(name, text):
        file = src/'Benchmark'/f'{name}.lean';file.write_text(text)
        result = lean(file, env, '-R', str(src), '-o', str(obj/'Benchmark'/f'{name}.olean'))
        save(work/f'{name}_compile.json', result)
        if result['exit_code']: raise ValueError('dependency_compile_failed: '+result['output'])

    definitions = ROOT/'benchmark/lean/Benchmark/Definitions.lean'
    dependency(definitions);compile_module('Definitions', definitions.read_text())
    regular_file = ROOT/'benchmark/lean/Benchmark/BatchDefinitions.lean'
    regular = re.search(r'(?m)^def regular\b[^\n]*\n', regular_file.read_text())
    if regular is None: raise ValueError('regular definition changed')
    dependency(regular_file)
    compile_module('ProductAtoms', 'import Benchmark.Definitions\nnamespace FiniteQBenchmark\n'
                   'variable {K : Type*} [Field K]\n'+regular[0]+'end FiniteQBenchmark\n')
    rules = LEAN_DIR/'Rules.lean'
    dependency(rules);compile_module('ProductRules', rules.read_text())
    # Reuse only the expression serializer, not any P1 mathematics or solver.
    dependency(HERE/'p1/lean/Extract.lean')
    dependency(Path(__file__))
    from math_library.registry import dependency_files
    for path in dependency_files():dependency(path)
    return env, deps


def extract(source, work, env):
    from math_library.frontend import extractor_text, query_trace
    file = work/'Extract.lean'
    file.write_text(assemble(extractor_text((HERE/'p1/lean/Extract.lean').read_text()),
                            slot(source, '  '+EXPAND+'\n  p1_export')))
    result = lean(file, env);save(work/'extraction.json', result)
    lines = [line.split('P1_JSON:', 1)[1] for line in result['output'].splitlines() if 'P1_JSON:' in line]
    if len(lines)!=1 or 'P1_EXPORT_ONLY' not in result['output'] or len(re.findall(r'\berror:',result['output']))!=1:
        raise ValueError('unsupported expression or context: '+result['output'])
    raw=json.loads(lines[0]);save(work/'expression.json',raw)
    save(work/'math_library_query.json',query_trace(raw))
    return raw


def nodes(node):
    yield node
    for child in node.get('args',[]): yield from nodes(child)
    if 'body' in node: yield from nodes(node['body'])


def plans(raw):
    if raw['op']!='Eq': raise ValueError('product pipeline requires an equality')
    products=[x for x in nodes(raw) if x['op']=='Finset.prod']
    if not products: raise ValueError('no finite product in elaborated target')
    if any(x['op']=='Finset.sum' for x in nodes(raw)):
        raise ValueError('finite sums belong to other proof methods')
    if any(x['args'][0]['op']!='Finset.range' for x in products):
        raise ValueError('first version requires natural range domains')
    # A small, explicit search space; all choices are structural and certificate
    # reconstruction fails closed when pointwise equalities cannot be proved.
    available=[]
    bounds=[p['args'][0]['args'][0]['op'] for p in products]
    if 'HMul.hMul' in bounds: available += ['residues','blocks']
    if 'HAdd.hAdd' in bounds: available += ['split']
    if any(x['op']=='HSub.hSub' for p in products for x in nodes(p['args'][0])):
        available += ['head']
    if any(any(x['op']=='Finset.prod' for x in nodes(p['args'][1])) for p in products):
        available += ['transpose']
    if any(x['op']=='HPow.hPow' and any(y['op']=='HSub.hSub' for y in nodes(x['args'][1]))
           for p in products for x in nodes(p['args'][1])):
        available += ['reflect']
    result=[{'orientation':'forward','rules':[]}]
    for rule in available:
        for orientation in ('forward','reverse'):
            result.append({'orientation':orientation,'rules':[rule]})
    # Nested partitions may need two index transformations; never recurse into
    # another proof family. Depth/resource exhaustion is reported as unproved.
    bound_operations=sum(x['op'] in ('HMul.hMul','HAdd.hAdd')
                         for p in products for x in nodes(p['args'][0]['args'][0]))
    for first in (available if bound_operations>1 else []):
        for second in available:
            if 'reflect' in (first,second): continue
            for orientation in ('forward','reverse'):
                result.append({'orientation':orientation,'rules':[first,second]})
    return result


def prepare(source, work):
    env,deps=environment(work)
    raw=extract(source,work,env)
    try:
        candidates=plans(raw);save(work/'plans.json',candidates)
        applicable,reason=True,'actual elaborated finite range products; bounded index rewrite search'
    except ValueError as exc:
        candidates=[];applicable,reason=False,str(exc)
    data={'dependencies':deps,'lean_path':env['LEAN_PATH'],'plans':candidates,
          'expression':raw,'source_text_sha256':__import__('hashlib').sha256(source.encode()).hexdigest(),
          'artifacts':[{'path':str(p),'sha256':sha(p)} for p in sorted((work/'deps').rglob('*.olean'))]}
    save(work/'environment.json',data)
    return [{'backend':'finite_product_indices','applicable':applicable,'reason':reason}]


def script(plan):
    lines=['  '+EXPAND]
    if plan['orientation']=='reverse':lines.append('  symm')
    for rule in plan['rules']:
        theorem=RULES[rule][0]
        if rule=='head':theorem+=' _ _ (by omega)'
        lines.append('  conv_lhs => rw ['+theorem+']')
    lines += ['  all_goals '+SMALL,'  all_goals '+FUSE,'  all_goals product_finish 8','  done']
    return '\n'.join(lines)


def prove_source(text, source, work, env, data, budget):
    import hashlib
    if hashlib.sha256(text.encode()).hexdigest()!=data['source_text_sha256']:
        raise ValueError('analysis/source mismatch')
    # Recompute candidates rather than accepting arbitrary scripts in a JSON file.
    if data['plans']!=plans(data['expression']):raise ValueError('analysis plan changed')
    report={'backend':'finite_product_indices','status':'search_exhausted',
            'dependencies':data['dependencies'],'construction':{'attempts':[]},
            'remaining_obligations':['No supported index certificate closed the original target']}
    deadline=time.monotonic()+budget['symbolic_seconds']
    for number,plan in enumerate(data['plans']):
        if time.monotonic()>=deadline:
            report['status']='resource_exhausted';break
        file=work/f'Candidate{number:02d}.lean'
        file.write_text(slot(text,script(plan))+'\n#print axioms '+source['theorem']+'\n')
        try:result=lean(file,env,timeout=max(.01,deadline-time.monotonic()))
        except subprocess.TimeoutExpired:
            report['status']='resource_exhausted';break
        save(work/f'candidate{number:02d}.json',{'plan':plan,'lean':result})
        report['construction']['attempts'].append({'plan':plan,'exit_code':result['exit_code'],
                                                  'log':str(work/f'candidate{number:02d}.json')})
        if result['exit_code'] or 'sorryAx' in result['output']:continue
        proof=work/'Proof.lean';proof.write_bytes(file.read_bytes())
        certificate=work/'certificate.json'
        save(certificate,{'schema_version':1,'kind':'finite_product_index_equivalence',
            'source_sha256':source['sha256'],'proof_sha256':sha(proof),
            'expression':data['expression'],'orientation':plan['orientation'],
            'index_steps':[{'rule':rule,'theorem':RULES[rule][0],'index_map':RULES[rule][1]} for rule in plan['rules']],
            'factor_steps':['expand frozen finite product definitions','evaluate explicit small ranges',
                            'merge equal-domain factors by prod_mul_distrib',
                            'bounded product congruence, power identities, exact ring normalization',
                            'primitive-root polynomial factorization only with proved positivity and root assumptions'],
            'proof_script':script(plan),'remaining_obligations':[]})
        report.update(status='proved',remaining_obligations=[],
                      certificate={'path':str(certificate),'sha256':sha(certificate)},
                      verification={'proof_file':str(proof),'proof_sha256':sha(proof),'lean':result})
        break
    save(work/'product_report.json',report)
    return report
