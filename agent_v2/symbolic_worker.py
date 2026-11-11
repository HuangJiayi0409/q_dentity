"""Explicit allowlisted calls to retained pure mathematical cores."""
import argparse
import importlib.util
import importlib.metadata
import json
from pathlib import Path
import sys

from .symbolic_methods import ROOT, METHODS, validate_request, request_digest, core_inventory


def load(relative):
    path=ROOT/relative
    name='agent_v2_retained_'+path.parent.name+'_'+path.stem
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec);sys.modules[name]=module;spec.loader.exec_module(module)
    return module


def construct(method, data):
    if method == 'coefficient': return load('finite_product_framework/p2/run.py').construct(data)
    if method == 'interpolation':
        certificate, proof=load('finite_product_framework/interpolation/algebra.py').zero_certificate(data['goal'],data['max_degree'])
        return {'status':'constructed','certificate':certificate,'unverified_proof_script':proof}
    if method == 'difference_ring':
        certificate=load('finite_product_framework/difference_ring/algebra.py').reduce_goal(data['goal'],
            {'max_degree':data['max_degree'],'max_unknowns':data['max_unknowns'],'symbolic_seconds':60})
        return {'status':'constructed','certificate':certificate}
    if method in ('kernel_transform','spectral','determinant'):
        sys.path.insert(0,str(ROOT/'finite_product_framework'))
        plans=load(METHODS[method]['entry'].split(':')[0]).construct(data)
        helper=sys.modules['workflow.matrix_symbolic']
        if Path(helper.__file__).resolve() != (ROOT/'finite_product_framework/workflow/matrix_symbolic.py').resolve():
            raise RuntimeError('pure scalar helper module was shadowed')
        return {'status':'constructed' if plans else 'search_exhausted','constructions':plans}
    if method=='macmahon':
        sys.path.insert(0,str(ROOT/'finite_product_framework/p1'))
        core=load('finite_product_framework/p1/core.py')
        try:
            return core.compute({'schema_version':1,'solver':'rational_omega','input':data},
                core.CoreBudget(seconds=60,max_unknowns=256,max_normal_form_degree=32,max_states=16))
        except core.UnsupportedDomain as error:
            return {'status':'unsupported_domain','reason':str(error)}
        except sys.modules['ore'].OreResourceLimit as error:
            return {'status':'budget_exhausted','reason':str(error)}
    raise ValueError('unimplemented registered core')


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--input',required=True);parser.add_argument('--output',required=True)
    args=parser.parse_args();request=json.loads(Path(args.input).read_text());validate_request(request)
    raw={'schema_version':1,'method':request['method'],'request_sha256':request_digest(request),
         'original_identity_proved':False,'source_before':core_inventory(request['method']),
         'python_version':sys.version.split()[0],'sympy_version':importlib.metadata.version('sympy')}
    try:
        construction=construct(request['method'],request['input'])
        status=construction.get('status')
        raw.update(status=status if status in ('constructed','unsupported_domain','budget_exhausted') else 'search_exhausted',construction=construction)
    except ValueError as error:
        status='budget_exhausted' if 'budget' in str(error) or 'resource' in str(error) else 'search_exhausted'
        raw.update(status=status,construction={'status':status,'reason':str(error)})
    except Exception as error:
        raw.update(status='environment_blocked',error={'type':type(error).__name__,'message':str(error)})
    raw['source_after']=core_inventory(request['method'])
    Path(args.output).write_text(json.dumps(raw,ensure_ascii=False,indent=2,default=str)+'\n')
    return 1 if raw['status']=='environment_blocked' else 0


if __name__=='__main__': raise SystemExit(main())
