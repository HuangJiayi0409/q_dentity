"""Run and independently replay the persisted stage-four synthetic CLI examples."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import sympy as s
from core import CoreBudget,rational_input
from expressions import X,q
from qdifference import rational_read
from qfinite import FiniteAlgebra

ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'generated/difference_full_20261014'


def audit(row,run):
    source=ROOT/row['input'];output=ROOT/row['output']
    if run:subprocess.run([sys.executable,str(ROOT/'solve_core.py'),'--input',str(source),'--output',str(output),'--seconds','90'],check=True)
    req=json.loads(source.read_text());res=json.loads(output.read_text())
    assert res['status']==row['expected_status'],(row['name'],res)
    payload=json.dumps(req,sort_keys=True,ensure_ascii=False).encode()
    assert hashlib.sha256(payload).hexdigest()==res['request_sha256']
    for name,digest in res['source_sha256'].items():assert hashlib.sha256((ROOT/'p1'/name).read_bytes()).hexdigest()==digest
    assert not res['original_identity_proved'] and res['benchmark_files_read']==0
    data=req['input'];sigma={X:q*X}
    for r in data['extensions']:
        t=s.Symbol(r['name']);v=rational_input(r['increment' if r['kind']=='sum' else 'ratio'])
        sigma[t]=t+v if r['kind']=='sum' else t*v
    rhs=list(map(rational_input,data['rhs_basis']));count=0
    if 'result' in res:
        vectors=res['result']['solution_basis']+([res['result']] if res['status']=='constructed' else [])
        if req['solver']=='difference_field':
            A,B=map(rational_input,data.get('operator',[1,-1]))
            for v in vectors:
                cs=list(map(rational_read,v['original_coefficients']));g=rational_read(v['original_certificate'])
                assert all(s.cancel(c.xreplace(sigma)-c)==0 for c in cs)
                assert s.cancel(A*g.xreplace(sigma)+B*g-sum(c*f for c,f in zip(cs,rhs)))==0
                count+=1
        else:
            definitions=[]
            for r in data['algebraic_extensions']:
                if r.get('kind')=='root_unity':
                    # This independent fixture expands the known cubic example.
                    assert r['order']==3
                    z=s.Symbol('FRoot0');E=s.Symbol(r['name'])
                    definitions.extend([(z,z**2+z+1,z),(E,E**3-1,z*E)])
                else:definitions.append((s.Symbol(r['name']),rational_input(r['polynomial']),rational_input(r['shift'])))
            alg=FiniteAlgebra(definitions,sigma,CoreBudget(),set().union(*(f.free_symbols for f in rhs)))
            for v in vectors:
                cs=list(map(rational_read,v['coefficients']));g=rational_read(v['certificate'])
                assert all(alg.normal(alg.sigma(c)-c)==0 for c in cs)
                assert alg.normal(alg.sigma(g)-g-sum(c*f for c,f in zip(cs,rhs)))==0
                count+=1
    return dict(name=row['name'],status=res['status'],seconds=res['elapsed_seconds'],vectors_checked=count,hashes_verified=True)


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--run',action='store_true');args=parser.parse_args()
    examples=[audit(row,args.run) for row in json.loads((OUT/'examples.json').read_text())]
    baseline=json.loads((OUT/'baseline_sources.json').read_text())
    for name,digest in baseline.items():
        assert hashlib.sha256((OUT/'baseline_sources'/name).read_bytes()).hexdigest()==digest
        if name!='p1/core.py':assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,name
    report=dict(status='passed',examples=examples,baseline_files_verified=len(baseline),
                allowed_existing_source_changes=['p1/core.py: solver dispatch and source registry'],
                benchmark_files_read=0,lean_invoked=False)
    (OUT/'artifact_audit.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
