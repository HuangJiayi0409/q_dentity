"""Replay/audit the synthetic CLI cases without reading any benchmark files."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import sympy as s
from core import rational_input
from expressions import X,q
from qdifference import rational_read

ROOT=Path(__file__).resolve().parent.parent
DIRECTORY=ROOT/'generated/difference_core_20261014'


def audit(row, run=False):
    source=ROOT/row['input']; output=ROOT/row['output']
    if run:
        subprocess.run([sys.executable,str(ROOT/'solve_core.py'),'--input',str(source),
                        '--output',str(output),'--seconds','60'],check=True)
    request=json.loads(source.read_text()); result=json.loads(output.read_text())
    assert result['status']==row['expected_status'],(row['name'],result)
    assert result['original_identity_proved'] is False and result['benchmark_files_read']==0
    payload=json.dumps(request,sort_keys=True,ensure_ascii=False).encode()
    assert hashlib.sha256(payload).hexdigest()==result['request_sha256']
    for filename,digest in result['source_sha256'].items():
        assert hashlib.sha256((ROOT/'p1'/filename).read_bytes()).hexdigest()==digest,filename
    # Reconstruct sigma straight from the ORIGINAL request, without Tower.sigma.
    sigma={X:q*X}
    for extension in request['input']['extensions']:
        symbol=s.Symbol(extension['name'])
        if extension['kind']=='sum': sigma[symbol]=symbol+rational_input(extension['increment'])
        else: sigma[symbol]=symbol*rational_input(extension['ratio'])
    rhs=list(map(rational_input,request['input']['rhs_basis']))
    checked=0
    raw=result.get('result',{})
    vectors=raw.get('solution_basis',[])+([raw] if result['status']=='constructed' else [])
    for item in vectors:
        cs=list(map(rational_read,item['original_coefficients']))
        g=rational_read(item['original_certificate'])
        assert all(s.cancel(c.xreplace(sigma)-c)==0 for c in cs)
        assert s.cancel(g.xreplace(sigma)-g-sum(c*f for c,f in zip(cs,rhs)))==0
        checked+=1
    for extension in result.get('tower',[]):
        dependency=extension.get('dependency')
        if dependency:
            ratios=[rational_read(r['ratio']) for r in extension['independence']['reductions']]
            g=rational_read(dependency['rational_witness'])
            assert s.cancel(s.prod(b**e for b,e in zip(ratios,dependency['exponents']))-g.subs(X,q*X)/g)==0
    return dict(name=row['name'],status=result['status'],elapsed_seconds=result['elapsed_seconds'],
                original_vectors_checked=checked,request_and_source_hashes_verified=True)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run',action='store_true',help='rerun CLI cases before audit')
    args=parser.parse_args()
    rows=json.loads((DIRECTORY/'examples.json').read_text())
    results=[audit(row,args.run) for row in rows]
    baseline=json.loads((DIRECTORY/'baseline_sources.json').read_text())
    for name,digest in baseline.items():
        assert hashlib.sha256((DIRECTORY/'baseline_sources'/name).read_bytes()).hexdigest()==digest
        if name!='p1/core.py': assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,name
    report=dict(status='passed',examples=results,baseline_files_verified=len(baseline),
                preexisting_algorithm_sources_unchanged=True,
                allowed_preexisting_source_changes=['p1/core.py: dispatch and source hash registry'],
                benchmark_files_read=0,lean_invoked=False)
    (DIRECTORY/'artifact_audit.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__': main()
