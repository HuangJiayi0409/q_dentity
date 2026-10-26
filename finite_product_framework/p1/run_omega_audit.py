"""Reproduce synthetic Omega CLI audit (never reads benchmark data)."""
import copy
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import sympy as s
from check_omega_core import replay
from qdifference import rational_read

ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'generated/omega_core_20261014'


def run(row):
    source=ROOT/'p1'/row['input']
    output=OUT/('cli_'+row['name']+'.json')
    command=[sys.executable,str(ROOT/'solve_core.py'),'--input',str(source),
             '--output',str(output),*row['args']]
    process=subprocess.run(command,capture_output=True,text=True,timeout=50)
    assert process.returncode==0,(row['name'],process.stdout,process.stderr)
    response=json.loads(output.read_text())
    assert response['status']==row['status'],(row['name'],response)
    assert response['original_identity_proved'] is False and response['benchmark_files_read']==0
    request=json.loads(source.read_text())
    digest=hashlib.sha256(json.dumps(request,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
    assert response['request_sha256']==digest
    for name,digest in response['source_sha256'].items():
        assert hashlib.sha256((ROOT/'p1'/name).read_bytes()).hexdigest()==digest
    steps=0
    if row['status']=='constructed':
        steps=replay(request,response)
        assert s.cancel(rational_read(response['result']['value'])-rational_read(row['expected']))==0
    return dict(name=row['name'],status=response['status'],steps_replayed=steps,
                output=output.name,elapsed_seconds=response['elapsed_seconds'])


def main():
    examples=json.loads((OUT/'examples.json').read_text())
    with ThreadPoolExecutor(max_workers=4) as pool:records=list(pool.map(run,examples))
    response=json.loads((OUT/'cli_inequality.json').read_text())
    request=json.loads((ROOT/'p1/examples/core_omega_inequality.json').read_text())
    variants={}
    bad=copy.deepcopy(response);bad['result']['value']='0';variants['final_value']=bad
    bad=copy.deepcopy(response);bad['result']['steps'][0]['positive_numerator']='0';variants['decomposition']=bad
    bad=copy.deepcopy(response)
    row=bad['result']['steps'][0]['factors'][0];row['side']='positive' if row['side']=='negative' else 'negative'
    variants['expansion_direction']=bad
    bad=copy.deepcopy(response);bad['result']['steps']=[];variants['missing_step']=bad
    bad=copy.deepcopy(response);bad['result']['steps'][0]['operator']='ct';variants['operator']=bad
    bad=copy.deepcopy(response);step=bad['result']['steps'][0]
    step['polynomial']=str(rational_read(step['polynomial'])+1)
    step['negative_numerator']=str(rational_read(step['negative_numerator'])-rational_read(step['negative_denominator']))
    variants['algebraically_equal_but_wrong_support']=bad
    rejected=[]
    for name,bad in variants.items():
        try:replay(request,bad)
        except AssertionError:rejected.append(name)
        else:raise AssertionError('tampering was accepted: '+name)
    report=dict(cli=records,steps_replayed=sum(r['steps_replayed'] for r in records),
        tampering_rejected=rejected,train_run=False,test_split_read=False,lean_run=False)
    (OUT/'artifact_audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False))


if __name__=='__main__':main()
