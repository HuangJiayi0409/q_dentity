"""Reproduce bounded standalone adapters sequentially; no benchmark/API/Lean calls."""
import argparse
import copy
import datetime
import hashlib
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(ROOT))
from agent_v2.symbolic_methods import METHODS,adapter,example_request,validate_request,core_inventory
from agent_v2.executor import normalize_result
from agent_v2.method_registry import builtin_registry
from agent_v2.storage import sha256_file


def save(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')


def failure_request(method):
    req=example_request(method)
    if method=='coefficient':req['input']['rhs']={'op':'integer','value':0}
    elif method=='interpolation':req['input']['goal']['rhs']={'op':'integer','value':0}
    elif method=='difference_ring':req['input']['goal']['hypotheses']=[]
    elif method=='kernel_transform':req['input']['matrix']['entries'][1]=copy.deepcopy(req['input']['matrix']['entries'][0])
    elif method=='spectral':req['input']['right']['entries']=copy.deepcopy(req['input']['left']['entries'])
    elif method=='macmahon':req['input']['denominator_monomials']=[['pow','L',2]]
    else:return None
    return req


def mathematical_payload(method,value):
    if method=='coefficient':assert value['residual']=='0'
    elif method=='interpolation':assert value['certificate']['nodes']==[{'node':'0','exact_residual':'0'},{'node':'1','exact_residual':'0'}]
    elif method=='difference_ring':assert value['certificate']['coefficients']=={'h0':'a0 + a1'}
    elif method=='kernel_transform':assert value['constructions'][0]['certificate']['inverse']==[['1','-1'],['0','1']]
    elif method=='spectral':assert value['constructions'][0]['certificate']['operator']==[['0','0'],['0','1']]
    elif method=='determinant':assert all(c['certificate']['determinant']=='-2' for c in value['constructions'])
    elif method=='macmahon':
        assert value['solver']=='rational_omega' and len(value['result']['steps'])==1
        assert value['result']['steps'][0]['rational_residual']=='0'


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',required=True)
    args=parser.parse_args();out=Path(args.output).resolve()
    if out.exists():raise ValueError('fresh evidence output required')
    out.mkdir(parents=True)
    before={m:core_inventory(m) for m in METHODS}
    save(out/'source_before.json',before)
    rows=[]
    for index,method in enumerate(METHODS,1):
        row={'sequence':index,'method':method,'started_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'cases':{}}
        request=example_request(method);validate_request(request)
        save(out/method/'example_request.json',request)
        def run(name,data,seconds=30):
            result=normalize_result(adapter(method).execute_request(data,out/method/name,seconds))
            assert result.C_partial==() and result.O_res==() and not result.original_identity_proved
            for artifact in result.artifacts:assert sha256_file(artifact.path)==artifact.sha256
            save(out/method/(name+'_result.json'),result.to_dict())
            row['cases'][name]={'status':result.status,'sigma':result.sigma.code,
                                'wall_seconds':result.cost.wall_seconds,'formal_certificates':0,'formal_obligations':0}
            return result
        positive=run('positive',request)
        mismatch=run('structure_mismatch',dict(request,input={'unsupported':True}))
        assert mismatch.status=='incomplete' and mismatch.sigma.code=='not_applicable'
        if METHODS[method].get('level')=='L0':
            assert positive.sigma.code=='capability_unavailable'
            assert not (out/method/'positive/process.json').exists()
            row['capability_level']='L0'
        else:
            row['capability_level']='L2'
            assert positive.status=='symbolic_constructed'
            mathematical_payload(method,positive.to_dict()['raw_result']['construction'])
            failure=failure_request(method)
            if failure:
                rejected=run('mathematical_failure',failure)
                assert rejected.status=='incomplete'
                assert rejected.sigma.code==('not_applicable' if method=='macmahon' else 'search_exhausted')
            prelaunch=run('prelaunch_budget_exhausted',request,0.000001)
            assert prelaunch.status=='budget_exhausted' and not (out/method/'prelaunch_budget_exhausted/process.json').exists()
            timed=run('worker_timeout',request,0.08)
            assert timed.status=='budget_exhausted' and timed.sigma.code=='timeout'
            assert json.loads((out/method/'worker_timeout/process.json').read_text())['timed_out']
        row['finished_at']=datetime.datetime.now(datetime.timezone.utc).isoformat();rows.append(row)
        save(out/'execution_order.json',rows)
        print(method,row['capability_level'],row['cases']['positive']['status'],flush=True)
    after={m:core_inventory(m) for m in METHODS};save(out/'source_after.json',after);assert before==after
    save(out/'method_registry.json',builtin_registry().to_dict())
    report={'schema_version':1,'status':'passed','execution':'strictly sequential; each method finishes all cases before next',
            'methods':len(rows),'l2':sum(r['capability_level']=='L2' for r in rows),'l0':sum(r['capability_level']=='L0' for r in rows),
            'source_inventory_unchanged':True,'formal_certificates':0,'formal_obligations':0,'benchmark_inputs':0,
            'model_api_calls':0,'lean_calls':0,'cases':sum(len(r['cases']) for r in rows),'rows':rows}
    save(out/'validation.json',report)
    print(json.dumps({k:v for k,v in report.items() if k!='rows'},ensure_ascii=False))


if __name__=='__main__':main()
