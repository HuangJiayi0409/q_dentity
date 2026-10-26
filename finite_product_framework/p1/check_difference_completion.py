"""Replay current stage-four CLI fixtures in their original symbolic domains."""
import argparse
from concurrent.futures import ThreadPoolExecutor
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
OUT=ROOT/'generated/difference_completion_20261014'


def run(row):
    subprocess.run([sys.executable,str(ROOT/'solve_core.py'),'--input',str(ROOT/row['input']),
                    '--output',str(ROOT/row['output']),'--seconds',str(row.get('seconds',90))],
                   check=True,timeout=row.get('seconds',90)+15,capture_output=True,text=True)


def replay(req,res):
    data=req['input'];sigma={X:q*X}
    for row in data['extensions']:
        t=s.Symbol(row['name']);kind=row['kind'];v=rational_input(row['increment' if kind=='sum' else 'ratio'])
        sigma[t]=t+v if kind=='sum' else t*v
    if 'result' not in res:return 0
    vectors=res['result']['solution_basis']+([res['result']] if res['status']=='constructed' else [])
    if req['solver']=='difference_system':
        V=s.Matrix([[rational_input(v) for v in row] for row in data['matrix']])
        rhs=[s.Matrix([[rational_input(v) for v in row]]) for row in data['rhs_basis']]
        for row in vectors:
            cs=list(map(rational_read,row['coefficients']));g=s.Matrix([list(map(rational_read,row['certificate_row']))])
            assert all(s.cancel(c.xreplace(sigma)-c)==0 for c in cs)
            assert (g.applyfunc(lambda v:v.xreplace(sigma))*V-g-sum((c*f for c,f in zip(cs,rhs)),s.zeros(1,V.rows))).applyfunc(s.cancel)==s.zeros(1,V.rows)
    else:
        A,B=map(rational_input,data.get('operator',[1,-1]));rhs=list(map(rational_input,data['rhs_basis']))
        if req['solver']=='difference_field':
            for row in vectors:
                cs=list(map(rational_read,row['original_coefficients']));g=rational_read(row['original_certificate'])
                assert all(s.cancel(c.xreplace(sigma)-c)==0 for c in cs)
                assert s.cancel(A*g.xreplace(sigma)+B*g-sum(c*f for c,f in zip(cs,rhs)))==0
        else:
            definitions=[]
            for row in data['algebraic_extensions']:
                if row.get('kind')=='root_unity':
                    # The retained automatic declaration fixture is cubic;
                    # spell out its source equations independently here.
                    assert row['order']==3
                    z=s.Symbol('FRoot0');e=s.Symbol(row['name'])
                    definitions.extend([(z,z**2+z+1,z),(e,e**3-1,z*e)])
                else:definitions.append((s.Symbol(row['name']),rational_input(row['polynomial']),rational_input(row['shift'])))
            alg=FiniteAlgebra(definitions,sigma,CoreBudget(),set().union(*(f.free_symbols for f in [A,B,*rhs])))
            for row in vectors:
                cs=list(map(rational_read,row['coefficients']));g=rational_read(row['certificate'])
                assert all(alg.normal(alg.sigma(c)-c)==0 for c in cs)
                assert alg.normal(A*alg.sigma(g)+B*g-sum(c*f for c,f in zip(cs,rhs)))==0
                for i in row['unit_coefficient_indices']:assert alg.multiplication(cs[i]).det()!=0
    return len(vectors)


def audit(row):
    req=json.loads((ROOT/row['input']).read_text());res=json.loads((ROOT/row['output']).read_text())
    assert res['status']==row['expected_status'],(row['name'],res)
    assert res['request_sha256']==hashlib.sha256(json.dumps(req,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
    for name,digest in res['source_sha256'].items():assert hashlib.sha256((ROOT/'p1'/name).read_bytes()).hexdigest()==digest
    assert res['original_identity_proved'] is False and res['benchmark_files_read']==0
    count=replay(req,res)
    return dict(name=row['name'],status=res['status'],seconds=res['elapsed_seconds'],vectors_checked=count,hashes_verified=True)


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--run',action='store_true');args=parser.parse_args()
    rows=json.loads((OUT/'examples.json').read_text())
    if args.run:
        with ThreadPoolExecutor(max_workers=4) as pool:list(pool.map(run,rows))
    results=[audit(row) for row in rows]
    before=json.loads((OUT/'baseline_sources.json').read_text());changed=[]
    for name,digest in before.items():
        assert hashlib.sha256((OUT/'baseline_sources'/name).read_bytes()).hexdigest()==digest
        if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=digest:changed.append(name)
    previous=json.loads((ROOT/'generated/difference_full_20261014/baseline_sources.json').read_text())
    for name,digest in previous.items():
        if name not in ('p1/core.py','p1/qrational_system.py'):
            assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,name
    # A modified certificate must fail the independent original-equation replay.
    fixture=next(row for row in rows if row['name']=='weighted_periodic')
    req=json.loads((ROOT/fixture['input']).read_text());res=json.loads((ROOT/fixture['output']).read_text())
    res['result']['original_certificate']='('+res['result']['original_certificate']+')+X'
    try:replay(req,res)
    except AssertionError:tamper_rejected=True
    else:raise AssertionError('tampered certificate accepted')
    report=dict(status='passed',examples=results,baseline_files_verified=len(before),changed_existing_files=changed,
                earlier_baseline_files_checked=len(previous),allowed_earlier_algorithm_changes=['p1/core.py','p1/qrational_system.py'],
                tampered_certificate_rejected=tamper_rejected,benchmark_files_read=0,lean_invoked=False)
    (OUT/'artifact_audit.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))


if __name__=='__main__':main()
