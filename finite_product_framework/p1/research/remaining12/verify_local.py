#!/usr/bin/env python3
"""Lean-check unsimplified cleared local relations from the constructed certificates.
These theorems do not discharge original domains, boundaries, or representation bridges.
"""
import sys,json,hashlib
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import sympy as s
HERE=Path(__file__).resolve().parent;P1=HERE.parents[1];sys.path.insert(0,str(P1))
from lean_pipeline import lean,polynomial_lean
from run import ROOT

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def check(identity):
    work=HERE/identity;path=work/'native_symbolic.json';r=json.loads(path.read_text())
    assert r['status']=='constructed'
    names=set()
    import re
    for expr in r['shifts'].values():names.update(re.findall(r'[A-Za-z_][A-Za-z_0-9]*',expr))
    env={name:s.Symbol(name) for name in names};q,X=env['q'],env['X']
    shifts={name:s.sympify(expr,locals=env) for name,expr in r['shifts'].items()}
    direct=r['case']['route']=='direct'
    R=s.sympify(r['construction']['antidifference_ratio' if direct else 'certificate'],locals=env)
    pieces=[shifts['V'],R.subs(X,q*X),R, s.Integer(1) if direct else shifts['U']]
    if not direct:pieces.append(shifts['c'])
    # Common denominator of the separate summands, without simplifying their sum.
    fractions=[s.fraction(s.cancel(e)) for e in (pieces[0]*pieces[1], *pieces[2:])]
    common=s.lcm([b for a,b in fractions])
    mapping={name:'v'+str(i) for i,name in enumerate(sorted(names))}
    terms=[polynomial_lean(s.cancel(a*common/b),mapping) for a,b in fractions]
    rhs=terms[0]+' - '+terms[1]+' - '+terms[2]
    if not direct:rhs+=' + '+terms[3]
    theorem='FiniteQP1.native_local_relation'
    source='import Mathlib.Tactic.Ring\nset_option maxHeartbeats 4000000\nset_option maxRecDepth 4096\n'
    source+='theorem '+theorem+' {K : Type*} [Field K] ('+' '.join(mapping.values())+' : K) :\n'
    source+=f'  {rhs} = 0 := by\n  ring\n#print axioms {theorem}\n'
    file=work/'LocalRelation.lean';file.write_text(source)
    import os
    result=lean(file,os.environ.copy())
    passed=result['exit_code']==0 and 'sorryAx' not in result['output'] and theorem in result['output']
    assert digest(ROOT/r['source']['path'])==r['source']['sha256']
    report={'id':identity,'status':'passed' if passed else 'failed','lean':result,
       'source_file':str(file),'proof_sha256':digest(file),'native_report_sha256':digest(path),
       'scope':'local cleared rational identity only; not the original finite sum proof',
       'automatic_train_proof':False,'symbol_mapping':mapping}
    (work/'local_validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(identity,report['status'],flush=True)
    return report

if __name__=='__main__':
    ids=json.loads((HERE/'selection.json').read_text())['identities']
    with ThreadPoolExecutor(max_workers=3) as pool:reports=list(pool.map(check,ids))
    (HERE/'local_validation.json').write_text(json.dumps({'records':reports,
       'passed':sum(r['status']=='passed' for r in reports),'original_proofs_claimed':0},ensure_ascii=False,indent=2)+'\n')
    assert all(r['status']=='passed' for r in reports)
