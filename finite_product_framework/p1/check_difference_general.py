"""CLI provenance and independent original-equation audit for general PLDE."""
import argparse
import copy
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
from qfinite import prepare

ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'generated/difference_general_20261014'


def replay(request,result):
    data=request['input'];kind=request['solver'];algebra=None
    shift={X:q*X}
    for row in data['extensions']:
        t=s.Symbol(row['name']);v=rational_input(row['increment' if row['kind']=='sum' else 'ratio'])
        shift[t]=t+v if row['kind']=='sum' else t*v
    if 'algebraic_extensions' in data:
        flat=[v for row in data['rhs_basis'] for v in row] if kind=='difference_system' else data['rhs_basis']
        flat=flat+([v for row in data['matrix'] for v in row] if kind=='difference_system' else data.get('operator',[]))
        _,_,_,_,algebra=prepare(dict(extensions=data['extensions'],algebraic_extensions=data['algebraic_extensions'],rhs_basis=flat),CoreBudget(),rational_input)
        shift=algebra.shift
    def zero(value):
        value=s.cancel(value)
        if algebra is None:return value==0
        num,den=s.fraction(value)
        assert algebra.multiplication(algebra.remainder(den)).det()!=0,'certificate denominator is not a unit'
        return algebra.G.reduce(s.expand(num))[1]==0
    if 'result' not in result:return 0
    entries=result['result']['solution_basis']+([result['result']] if result['status']=='constructed' else [])
    for entry in entries:
        cs=list(map(rational_read,entry.get('original_coefficients',entry['coefficients'])))
        assert len(cs)==len(data['rhs_basis'])
        assert all(zero(c.xreplace(shift)-c) for c in cs),'noninvariant coefficient'
        if algebra is not None:
            allowed=set(algebra.field.symbols)|set(algebra.variables)
            values=[*cs,*map(rational_read,entry['certificate_row'])] if kind=='difference_system' else [*cs,rational_read(entry.get('original_certificate',entry['certificate']))]
            assert all(not v.free_symbols-allowed for v in values),'unrestored symbol'
            for index in entry.get('unit_coefficient_indices',[]):assert algebra.multiplication(cs[index]).det()!=0
        if kind=='difference_system':
            g=s.Matrix([list(map(rational_read,entry['certificate_row']))]);V=s.Matrix([[rational_input(v) for v in row] for row in data['matrix']])
            rhs=[s.Matrix([[rational_input(v) for v in row]]) for row in data['rhs_basis']]
            residual=g.applyfunc(lambda v:v.xreplace(shift))*V-g-sum((c*f for c,f in zip(cs,rhs)),s.zeros(1,V.rows))
            assert all(zero(v) for v in residual),'original matrix residual'
        else:
            g=rational_read(entry.get('original_certificate',entry['certificate']))
            operator=list(map(rational_input,data.get('operator',[1,-1])))
            if kind!='difference_equation':operator=list(reversed(operator))
            residual=0;current=g
            for a in operator:residual+=a*current;current=s.cancel(current.xreplace(shift))
            rhs=list(map(rational_input,data['rhs_basis']))
            assert zero(residual-sum(c*f for c,f in zip(cs,rhs))),'original scalar residual'
        if result['status']=='no_relation_in_declared_basis':assert all(zero(c) for c in cs)
    return len(entries)


def runtime_hashes(value):
    if isinstance(value,dict):
        if 'runtime' in value and isinstance(value['runtime'],dict):
            for path,digest in value['runtime']['artifacts'].items():assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==digest
        for child in value.values():runtime_hashes(child)
    elif isinstance(value,list):
        for child in value:runtime_hashes(child)


def run(row):
    seconds=row.get('seconds',120)
    subprocess.run([sys.executable,str(ROOT/'solve_core.py'),'--input',str(ROOT/row['input']),
                    '--output',str(ROOT/row['output']),'--seconds',str(seconds)],
                   capture_output=True,text=True,check=True,timeout=seconds+15)


def audit(row):
    request=json.loads((ROOT/row['input']).read_text());result=json.loads((ROOT/row['output']).read_text())
    assert result['status']==row['expected_status'],(row['name'],result.get('status'),result.get('reason'))
    assert result['request_sha256']==hashlib.sha256(json.dumps(request,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
    for name,digest in result['source_sha256'].items():assert hashlib.sha256((ROOT/'p1'/name).read_bytes()).hexdigest()==digest
    assert not result['original_identity_proved'] and result['benchmark_files_read']==0
    runtime_hashes(result)
    return dict(name=row['name'],status=result['status'],seconds=result['elapsed_seconds'],vectors_checked=replay(request,result),hashes_verified=True)


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--run',action='store_true');args=parser.parse_args()
    rows=json.loads((OUT/'examples.json').read_text())
    if args.run:
        with ThreadPoolExecutor(max_workers=4) as pool:list(pool.map(run,rows))
    results=[audit(row) for row in rows]
    mutations=[]
    for name,field in [('higher_sigma','certificate'),('native_pi','certificate'),('native_pi','coefficients'),('periodic_high_order','coefficients')]:
        row=next(row for row in rows if row['name']==name)
        request=json.loads((ROOT/row['input']).read_text());result=copy.deepcopy(json.loads((ROOT/row['output']).read_text()))
        entry=result['result']['solution_basis'][0]
        if field=='certificate':entry[field]=str(rational_read(entry[field])+X)
        else:entry[field][0]=str(rational_read(entry[field][0])+s.Symbol('P'))
        rejected=False
        try:replay(request,result)
        except AssertionError:rejected=True
        assert rejected,(name,field)
        mutations.append(dict(case=name,changed_field=field,rejected=True))
    snapshots=json.loads((OUT/'baseline_sources.json').read_text())
    for row in snapshots:assert hashlib.sha256((OUT/row['snapshot']).read_bytes()).hexdigest()==row['sha256']
    report=dict(results=results,vectors_checked=sum(row['vectors_checked'] for row in results),tampered_certificates=mutations,
                snapshots_verified=len(snapshots),benchmark_files_read=0,lean_run=False)
    (OUT/'artifact_audit.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps(report,ensure_ascii=False))


if __name__=='__main__':main()
