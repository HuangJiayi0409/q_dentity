"""Independent operator semantics -> finite word rewriting -> kernel proof.

Symbolic computation is performed by Lean's simplifier/noncomm_ring/abel.
No benchmark proof imports, identity dispatch, or commutative ring assumption.
"""
import hashlib
import json
import os
from pathlib import Path
import re
from workflow.contracts import HERE, ROOT, save, sha
from product.pipeline import lean, assemble  # execution/text utilities only

BACKEND = 'operator_word_normalization'
LEAN = HERE/'noncommutative/lean'
EXPAND = 'try simp only [FiniteQBenchmark.kacX, FiniteQBenchmark.kacM]'
SCRIPT = '  '+EXPAND+'\n  operator_words\n  done'


def slot(source, proof):
    from workflow.preprocessed import slot as shared_slot
    shared=shared_slot(source,proof,('Benchmark.OperatorAtoms','Benchmark.OperatorRules'))
    if shared is not None:return shared
    if len(re.findall(r'(?m)^  sorry\s*$',source)) != 1:
        raise ValueError('one deferred proof slot required')
    source = re.sub(r'^import[^\n]*$', 'import Benchmark.OperatorAtoms\nimport Benchmark.OperatorRules',source,flags=re.M)
    return re.sub(r'(?m)^  sorry\s*$',lambda _:proof,source)


def environment(work):
    from workflow.preprocessed import environment as shared_environment
    shared=shared_environment(work,'noncommutative')
    if shared is not None:return shared
    src,obj=work/'sources',work/'deps'
    (src/'Benchmark').mkdir(parents=True);(obj/'Benchmark').mkdir(parents=True)
    env=dict(os.environ,LEAN_PATH=str(obj));deps=[]
    def dep(path):
        deps.append({'path':str(path.relative_to(ROOT)),'sha256':sha(path)})
    def compile(name,text):
        file=src/'Benchmark'/f'{name}.lean';file.write_text(text)
        r=lean(file,env,'-R',str(src),'-o',str(obj/'Benchmark'/f'{name}.olean'))
        save(work/f'{name}_compile.json',r)
        if r['exit_code']:raise ValueError('dependency_compile_failed: '+r['output'])
    definitions=ROOT/'benchmark/lean/Benchmark/Definitions.lean';dep(definitions)
    compile('Definitions',definitions.read_text())
    original=ROOT/'benchmark/lean/Benchmark/Batch5Definitions.lean';dep(original)
    atoms=[]
    for name in ('kacX','kacM'):
        match=re.search(r'(?m)^def '+name+r'\b[^\n]*\n',original.read_text())
        if match is None:raise ValueError('frozen operator definition changed')
        atoms.append(match[0])
    compile('OperatorAtoms','import Benchmark.Definitions\nimport Mathlib.Algebra.Polynomial.Eval.Defs\nnoncomputable section\nnamespace FiniteQBenchmark\nvariable {K : Type*} [Field K]\n'+''.join(atoms)+'end FiniteQBenchmark\n')
    dep(LEAN/'Rules.lean');compile('OperatorRules',(LEAN/'Rules.lean').read_text())
    for path in (LEAN/'Export.lean',Path(__file__),HERE/'product/pipeline.py'):dep(path)
    return env,deps


def extract(source,work,env):
    file=work/'Extract.lean'
    file.write_text(assemble((LEAN/'Export.lean').read_text(),slot(source,'  operator_export')))
    r=lean(file,env);save(work/'extraction.json',r)
    lines=[s.split('OPERATOR_JSON:',1)[1] for s in r['output'].splitlines() if 'OPERATOR_JSON:' in s]
    if len(lines)!=1 or len(re.findall(r'\berror:',r['output']))!=1 or 'OPERATOR_EXPORT_ONLY' not in r['output']:
        raise ValueError('unsupported expression/context: '+r['output'])
    return json.loads(lines[0])


def nodes(node):
    yield node
    for child in node.get('args',[]):yield from nodes(child)


def supported(raw):
    target=raw['target']
    if target['op']!='Eq':return False,'operator equality required'
    all_nodes=list(nodes(target))
    for relation in raw['relations']:all_nodes.extend(nodes(relation['type']))
    # Conservative grammar: reject hidden sums, symbolic powers and arbitrary
    # function applications. Leaves are variables and numeric literals only.
    allowed={'Eq','var','nat','HAdd.hAdd','HSub.hSub','HMul.hMul','HPow.hPow',
             'HSMul.hSMul','Neg.neg','FiniteQBenchmark.kacX','FiniteQBenchmark.kacM'}
    if any(n['op'] not in allowed for n in all_nodes):
        return False,'unsupported atom, binder or sum; symbolic induction is not implemented'
    for n in all_nodes:
        if n['op']=='HPow.hPow' and (n['args'][1]['op']!='nat' or n['args'][1]['value']>12):
            return False,'only explicit powers at most 12; arbitrary n requires induction'
    if not any(n['op'] in ('HMul.hMul','FiniteQBenchmark.kacX','FiniteQBenchmark.kacM') for n in nodes(target)):
        return False,'no operator action or multiplicative word'
    return True,'elaborated finite words/operator actions; local equality rewriting'


def prepare(source,work):
    env,deps=environment(work);raw=extract(source,work,env)
    applicable,reason=supported(raw)
    save(work/'environment.json',{'dependencies':deps,'lean_path':env['LEAN_PATH'],
        'expression':raw,'source_text_sha256':hashlib.sha256(source.encode()).hexdigest(),
        'artifacts':[{'path':str(p),'sha256':sha(p)} for p in sorted((work/'deps').rglob('*.olean'))]})
    return [{'backend':BACKEND,'applicable':applicable,'reason':reason}]


def prove_source(text,source,work,env,data,budget):
    if hashlib.sha256(text.encode()).hexdigest()!=data['source_text_sha256']:
        raise ValueError('analysis/source mismatch')
    applicable,reason=supported(data['expression'])
    if not applicable:raise ValueError(reason)
    proof=work/'Proof.lean'
    proof.write_text(slot(text,SCRIPT)+'\n#print axioms '+source['theorem']+'\n')
    r=lean(proof,env,timeout=budget['symbolic_seconds']);save(work/'lean.json',r)
    report={'backend':BACKEND,'dependencies':data['dependencies'],
        'status':'construction_failed','construction':{'algorithm':'definition reduction; relation-directed noncomm_ring; abel'},
        'remaining_obligations':['Finite word normalizer did not close the original equality'],
        'verification':{'proof_file':str(proof),'proof_sha256':sha(proof),'lean':r}}
    if r['exit_code']==0 and 'sorryAx' not in r['output']:
        cert=work/'certificate.json'
        save(cert,{'schema_version':1,'kind':'kernel_reconstructed_operator_word_normalization',
            'source_sha256':source['sha256'],'proof_sha256':sha(proof),
            'expression':data['expression'],'proof_script':SCRIPT,
            'stages':['expand frozen operator definitions','normalize polynomial composition and central scalar actions',
                      'expand/distribute finite words, right-associate and rewrite local equalities',
                      'abelian additive normalization; exact Lean kernel checking'],
            'remaining_obligations':[]})
        report.update(status='proved',remaining_obligations=[],certificate={'path':str(cert),'sha256':sha(cert)})
    return report
