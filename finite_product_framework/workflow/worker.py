"""Isolated adapters for legacy module namespaces; no backend code copied here."""
import argparse
import json
import os
from pathlib import Path
import sys
import subprocess

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from workflow.contracts import HERE,ROOT,BACKENDS,check_source,save,sha


def prepared_environment(data):
    for entry in data['dependencies']:
        if sha(ROOT/entry['path'])!=entry['sha256']:raise ValueError('dependency source changed')
    for entry in data['artifacts']:
        if sha(entry['path'])!=entry['sha256']:raise ValueError('compiled dependency changed')
    env=dict(os.environ);env['LEAN_PATH']=data['lean_path']
    return env


def prepare(source,work,kind,method):
    if kind in ('kernel_transform','spectral','determinant','macmahon'):
        from importlib import import_module
        return import_module(kind+'.pipeline').prepare(source,work)
    if kind=='difference_ring':
        from difference_ring.pipeline import prepare as prepare_difference
        return prepare_difference(source,work)
    if kind=='combinatorial':
        from combinatorial.pipeline import prepare as prepare_combinatorial
        return prepare_combinatorial(source,work)
    if kind=='noncommutative':
        from noncommutative.pipeline import prepare as prepare_operator
        return prepare_operator(source,work)
    if kind=='interpolation':
        from interpolation.pipeline import prepare as prepare_interpolation
        return prepare_interpolation(source,work)
    if kind=='product':
        from product.pipeline import prepare as prepare_product
        return prepare_product(source,work)
    sys.path.insert(0,str(HERE/kind))
    import run as backend
    env,deps=backend.environment(work) if kind=='p2' else __import__('lean_pipeline').environment(work)
    data={'dependencies':deps,'lean_path':env['LEAN_PATH'],
          'artifacts':[{'path':str(p),'sha256':sha(p)} for p in sorted((work/'deps').rglob('*.olean'))]}
    save(work/'environment.json',data)
    if kind=='p2':
        # Probe the actual Lean expression after coefficient normalization. No ID-based routing.
        import re
        rules=backend.rules_text()
        exporter=(backend.HERE/'lean/Export.lean').read_text()
        probes=[]
        for depth in range(0,5):
            file=work/'Analyze.lean'
            file.write_text(backend.assemble(rules,exporter,backend.proof_slot(source,
                backend.preparation(depth=depth)+'  p2_export')))
            result=backend.lean(file,env)
            lines=[line.split('P2_JSON:',1)[1] for line in result['output'].splitlines() if 'P2_JSON:' in line]
            probes.append({'depth':depth,'lean':result})
            if len(lines)==1 and 'P2_EXPORT_ONLY' in result['output'] and len(re.findall(r'\berror:',result['output']))==1:
                raw=json.loads(lines[0]);save(work/'lean_expression.json',raw)
                save(work/'probes.json',probes)
                goals=raw.get('goals',[raw])
                supported=raw.get('closed_by_preparation') or any('lhs' in g for g in goals)
                return [{'backend':'cauchy_coefficient','applicable':bool(supported),
                         'reason':'All goal branches exported; coefficient residuals still require construction' if supported
                                  else 'No equality goal in declared coefficient domain',
                         'depth':depth, 'goal_count':len(goals),
                         'unsupported_goals':sum('unsupported_goal' in g for g in goals),
                         'cross_method_dependencies':[]}]
        save(work/'probes.json',probes)
        return [{'backend':'cauchy_coefficient','applicable':False,'reason':'coefficient representation not exposed in supported depths'}]
    from lean_pipeline import extract,frontend
    from general_summation import telescoping_frontend as direct
    from general_summation import recurrence_frontend as zeil
    from bibasic_pipeline import frontend as bibasic
    from multisum_pipeline import frontend as multi
    from ore_pipeline import prepare as ore
    raw=extract(source,work,env)
    candidates=[]
    for name,probe in [('direct_q_gosper',direct),('bibasic_gosper',bibasic),
                       ('target_first_order',frontend),('general_q_zeilberger',zeil),
                       ('ore_closure',None),('multisum',multi)]:
        if BACKENDS[name]!=method:continue
        try:
            case=work/'frontends'/name;case.mkdir(parents=True,exist_ok=True)
            formula,model=ore(raw,'analysis',case,env) if probe is None else probe(raw,'analysis')
            save(case/'problem.json',formula)
            checks={'representation':'accepted','core_domain':'unknown','proof_exit':'unknown',
                    'obligations':['Construct and verify certificate, boundary, initial values and original-domain transport']}
            if name=='multisum':
                from multisum import derive
                from workflow.admission import multisum_exit
                derive(formula)
                checks=multisum_exit(model)
            candidates.append({'backend':name,'applicable':True,'reason':'actual Lean expression accepted',
                               'admission_checks':checks})
        except (ValueError,NotImplementedError) as exc:
            candidates.append({'backend':name,'applicable':False,'reason':str(exc),
                               'admission_checks':{'core_domain':'rejected','proof_exit':'unavailable',
                                                   'obligations':['Provide a supported source representation']}})
    return candidates


def execute(request):
    from workflow.preprocessed import activated, describe, audit_result
    validate_request(request)
    if request['action']=='preprocess':
        from preprocessing.cache import cached_run
        check_source(request['source'])
        output,result=cached_run(request['source']['identity'],timeout=request['timeout'],
                   support_modules=('Benchmark.Batch5Definitions',),view=request.get('normalization_view','structured'))
        return dict(status=result['status'],descriptor=describe(output),
                    cache_hit=result['cache_hit'],cache_key=result['cache_key'])
    if request['action']=='select':
        check_source(request['source'])
        from selection import select
        from selection.features import FeatureLimit
        descriptor=request['source'].get('preprocessing')
        if descriptor is None:raise ValueError('selection requires verified preprocessing')
        path=Path(descriptor['directory'])/'standard.json'
        if path.stat().st_size>64*1024*1024:raise ValueError('selection input file limit')
        before=sha(path)
        try:result=select(json.loads(path.read_text()),seconds=request['timeout'])
        except FeatureLimit as exc:
            return dict(status='selection_failed',error=str(exc),remaining_obligations=['Structural assessment incomplete; no method was run'])
        check_source(request['source'])
        if sha(path)!=before:raise ValueError('selection input changed')
        return dict(result,source_sha256=request['source']['sha256'],standard_sha256=before)
    with activated(request['source']):
        result=execute_method(request)
        if request['action']=='prove':
            result=audit_result(result,request['source'],request['work'],request['environment'])
        return result


def validate_request(request):
    method=request['method']
    if method=='auto' and request['action'] in ('preprocess','select'):return
    if method not in BACKENDS.values():raise ValueError('inactive method')
    if request['action']=='analyze' and request['kind']!=(method if method in ('product','interpolation','noncommutative','combinatorial','difference_ring','kernel_transform','spectral','determinant','macmahon') else 'p2' if method=='coefficient' else 'p1'):
        raise ValueError('adapter outside selected method')
    if request['action']=='prove' and BACKENDS.get(request['backend'])!=method:
        raise ValueError('backend outside selected method')
    if request['action'] not in ('analyze','prove','preprocess'):
        raise ValueError('unknown worker action')


def execute_method(request):
    method=request['method']
    source=request['source'];check_source(source)
    work=Path(request['work']);work.mkdir(parents=True,exist_ok=True)
    text=Path(source['snapshot']).read_text()
    if request['action']=='analyze':
        from workflow.admission import annotate
        return {'status':'analyzed','candidates':[annotate(c) for c in prepare(text,work,request['kind'],method)]}
    if method in ('kernel_transform','spectral','determinant','macmahon'):
        from importlib import import_module
        data=json.loads(Path(request['environment']).read_text());env=prepared_environment(data)
        report=import_module(method+'.pipeline').prove_source(text,source,work,env,data,request['budget'])
        prepared_environment(data);check_source(source)
        return report
    if method=='difference_ring':
        from difference_ring.pipeline import prove_source
        data=json.loads(Path(request['environment']).read_text());env=prepared_environment(data)
        report=prove_source(text,source,work,env,data,request['budget'])
        prepared_environment(data);check_source(source)
        return report
    if method=='combinatorial':
        from combinatorial.pipeline import prove_source
        data=json.loads(Path(request['environment']).read_text());env=prepared_environment(data)
        report=prove_source(text,source,work,env,data,request['budget'],request['backend'])
        prepared_environment(data);check_source(source)
        return report
    if method=='noncommutative':
        from noncommutative.pipeline import prove_source
        data=json.loads(Path(request['environment']).read_text());env=prepared_environment(data)
        report=prove_source(text,source,work,env,data,request['budget'])
        prepared_environment(data);check_source(source)
        return report
    if method=='interpolation':
        from interpolation.pipeline import prove_source
        data=json.loads(Path(request['environment']).read_text());env=prepared_environment(data)
        report=prove_source(text,source,work,env,data,request['budget'],request['backend'])
        prepared_environment(data);check_source(source)
        return report
    if method=='product':
        from product.pipeline import prove_source
        data=json.loads(Path(request['environment']).read_text());env=prepared_environment(data)
        report=prove_source(text,source,work,env,data,request['budget'])
        prepared_environment(data);check_source(source)
        return report
    name=request['backend'];kind='p2' if name=='cauchy_coefficient' else 'p1'
    if name not in BACKENDS:raise ValueError('inactive backend')
    data=json.loads(Path(request['environment']).read_text());env=prepared_environment(data)
    sys.path.insert(0,str(HERE/kind));import run as backend
    if kind=='p2':
        result=backend.prove_source(text,work,env)
        report={'status':result['status'],'source':source,'dependencies':data['dependencies'],
                'verification':result,'remaining_obligations':result['remaining_obligations']}
    else:
        from zeilberger import ZeilbergerBudget
        from multisum import MultisumBudget
        settings=request['budget'];options={'seconds':settings['symbolic_seconds'],
                 'max_order':settings['max_order'],'max_unknowns':settings['max_unknowns']}
        if name=='multisum':options.update(max_degree=settings['max_degree'],laurent_floor=settings['laurent_floor'])
        budget=(MultisumBudget if name=='multisum' else ZeilbergerBudget)(**options)
        report=backend.run(source['identity'],budget=budget,branch=name,
            output_root=work,prepared={'env':env,'dependencies':data['dependencies'],'artifacts':data['artifacts']},
            source_context=source if source.get('preprocessing') else None)
        if report.get('branch',name)!=name:raise ValueError('backend route changed unexpectedly')
    prepared_environment(data);check_source(source)
    return report

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('request');parser.add_argument('result');args=parser.parse_args()
    try:result=execute(json.loads(Path(args.request).read_text()))
    except subprocess.TimeoutExpired as exc:result={'status':'timeout','error':str(exc),
                                  'remaining_obligations':['Complete the adapter stage within its time budget']}
    except Exception as exc:result={'status':'adapter_failed','error':f'{type(exc).__name__}: {exc}',
                                  'remaining_obligations':['Resolve adapter or representation failure']}
    save(args.result,result)
