#!/usr/bin/env python3
"""Audit actual trials, independent residuals, exact diagnostics and provenance."""
import contextlib,io,json
from collections import Counter
import sympy as s
from run_trials import HERE,P1,ROOT,digest,summarize
from inputs import CASES,P,G,q,Q,X,n,k
from engine import evaluate,diagnostics,ratio,rational

def check():
 # Regression: zero-length products must remain exact, including whole Gaussian atoms.
 assert evaluate(G(q,0,0),0)==s.Integer(1)
 assert not evaluate(G(q,0,0),0).has(s.Float)
 assert evaluate(G(q,2,3),0)==0
 assert evaluate(P(s.Rational(2,7),q,-1),0)==s.Rational(7,4)
 # A start shift and a negative length shift together, checked against actual products.
 expr=P(s.Rational(2,7)*q**n,q,2*n-k+3)
 for index in (n,k):
  actual=ratio(expr,index)
  for N,K in ((2,1),(3,2)):
   expected=evaluate(expr,N+(index==n),K+(index==k))/evaluate(expr,N,K)
   assert s.cancel(evaluate(actual,N,K)-expected)==0
 names='q Q X a b c d e f t x z w E_m E_u E_v'.split()
 symbols={name:s.Symbol(name) for name in names}
 parse=lambda expr:s.sympify(expr,locals=symbols)
 constructed=finite=shift_checks=0
 for i,case in enumerate(CASES):
  r=json.loads((HERE/'results'/f'{i:02d}.json').read_text())
  assert r['status'] not in ('started','worker_failed','research_representation_gap')
  assert r['id']==case['id'] and r['branch']==case['branch']
  assert all(r[key]==str(value) for key,value in case.items())
  assert r['source_unchanged'] and digest(ROOT/r['source']['path'])==r['source']['sha256']
  assert not r['automatic_train_proof'] and not r['lean_representation_verified']
  assert all(digest(HERE/name)==sha for name,sha in r['code_sha256'].items())
  shifts={name:parse(expr) for name,expr in r.get('derived_shifts',{}).items()}
  diag=diagnostics(case,shifts or None,r.get('q_power_symbols'))
  assert diag==r['diagnostics'] and not diag['mismatches']
  finite+=len(diag['sum_checks']);shift_checks+=diag['independent_shift_checks']
  assert not any(expr.has(s.Float) for expr in shifts.values())
  if r['status']=='constructed':
   direct=case['route']=='direct'
   R=parse(r['construction']['antidifference_ratio' if direct else 'certificate'])
   residual=shifts['V']*R.subs(X,q*X)-R-(1 if direct else shifts['U']-shifts['c'])
   assert not R.has(s.Float) and s.cancel(residual)==0
   constructed+=1
 production=json.loads((P1/'validation.json').read_text())
 assert production['status']=='passed' and production['automatic_train_proofs']==2
 assert all(digest(P1/name)==sha for name,sha in production['code_sha256'].items())
 review=json.loads((HERE.parent/'applicability/review.json').read_text())
 for source in review['summary']['evidence_sources']:
  assert digest(ROOT/source['path'])==source['sha256']
 before={name:(HERE/name).read_bytes() for name in ('summary.json','table.json','table.csv','index.html')}
 with contextlib.redirect_stdout(io.StringIO()):summarize()
 assert all((HERE/name).read_bytes()==data for name,data in before.items())
 table=json.loads((HERE/'table.json').read_text())
 groups={group:dict(Counter(r['status'] for r in table['records'] if r['review_group']==group)) for group in ('prioritize_symbolic_trial','conditional_candidate')}
 result={'status':'passed','identities':41,'subproblems':len(CASES),'groups':groups,
 'independent_local_residuals':constructed,'exact_finite_diagnostic_checks':finite,
 'independent_shift_diagnostic_checks':shift_checks,'production_code_unchanged':True,
 'automatic_train_proofs':2,'new_lean_proofs':0,
 'limitations':'Research transcriptions and transformations remain unproved; finite diagnostics are not general proofs. Thirty-second construction budgets, four concurrent workers.',
 'check_code_sha256':digest(HERE/'check_trials.py'), 'summary_sha256':digest(HERE/'summary.json')}
 (HERE/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':check()
