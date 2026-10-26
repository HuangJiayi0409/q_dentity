#!/usr/bin/env python3
"""Run ONLY the 18+23 reviewed candidates, with hard per-stage budgets.
Research transcriptions and changes of variables are explicit and untrusted.
A constructed certificate is NOT an original-domain or Lean proof.
"""
import argparse
from collections import Counter,defaultdict
from concurrent.futures import ThreadPoolExecutor,as_completed
import hashlib,html,json,os,signal,subprocess,sys,time,csv,io
from pathlib import Path
HERE=Path(__file__).resolve().parent;P1=HERE.parents[1];sys.path.insert(0,str(P1))
from inputs import CASES,n,k,q,Q,X
from engine import gaussian_form,ratio,rational,diagnostics
from run import load_target,ROOT
from search import search,Budget
from qgosper import antidifference
import sympy as s
OUT=HERE/'results'

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def write(path,value):
 path.parent.mkdir(parents=True,exist_ok=True)
 tmp=path.with_suffix('.tmp');tmp.write_text(json.dumps(value,ensure_ascii=False,indent=2,default=str)+'\n');tmp.replace(path)
def limit(signum,frame):raise TimeoutError('stage wall-clock budget exhausted')

def worker(index):
 case=CASES[index];source=load_target(case['id']);path=OUT/f'{index:02d}.json'
 report={key:str(value) for key,value in case.items()}
 report.update(source=source,status='started',stage='finite_diagnostics',case_index=index,
  lean_representation_verified=False,automatic_train_proof=False,
  input_origin='explicit research transcription; not production Lean frontend',
  formal_domain='Q(q, independent parameters); original singular values and parameter domains not discharged',
  mathematical_preconditions_status='candidate transformations recorded; Lean equivalence/support proof pending',
  code_sha256={p:digest(HERE/p) for p in ['inputs.py','engine.py','run_trials.py']},budgets_seconds={'preparation':60,'construction':30})
 started=time.monotonic();write(path,report)
 signal.signal(signal.SIGALRM,limit);signal.setitimer(signal.ITIMER_REAL,60)
 try:
  diag=diagnostics(case);report['diagnostics']=diag;write(path,report)
  if diag['mismatches']:
   report.update(status='finite_diagnostic_mismatch',stage='finite_diagnostics')
  else:
   report['stage']='shift_derivation';write(path,report)
   F=gaussian_form(case['F']);T=gaussian_form(case['T'])
   shifts={};powers={}
   for key,expr,index0 in ([('V',F,k)] if case['route']=='direct' else [('U',F,n),('V',F,k),('c',T,n)]):
    shifts[key],new=rational(ratio(expr,index0));powers.update(new)
   report['derived_shifts']={a:str(b) for a,b in shifts.items()};report['q_power_symbols']=powers
   report['diagnostics']=diagnostics(case,shifts,powers);write(path,report)
   signal.setitimer(signal.ITIMER_REAL,30);report['stage']='q_gosper_construction';write(path,report)
   if case['route']=='direct':
    result=antidifference(s.cancel(shifts['V'].subs(X,X/q)),X,q,Budget(seconds=30))
    if result['status']=='constructed':
     R=result['antidifference_ratio'];assert s.cancel(shifts['V']*R.subs(X,q*X)-R-1)==0
     result['independent_direct_residual']='0'
   else:
    result=search(shifts['U'],shifts['V'],shifts['c'],X,q,Budget(seconds=30))
    if result['status']=='constructed':
     symbols={str(z):z for expr in shifts.values() for z in expr.free_symbols}
     R=s.sympify(result['certificate'],locals=symbols)
     assert s.cancel(shifts['V']*R.subs(X,q*X)-R-shifts['U']+shifts['c'])==0
     result['independent_qwz_residual']='0'
   report.update(status=result['status'],construction=result,stage='finished')
 except TimeoutError as exc:report.update(status='timeout',error=str(exc))
 except Exception as exc:report.update(status='research_representation_gap',error=f'{type(exc).__name__}: {exc}')
 finally:
  signal.setitimer(signal.ITIMER_REAL,0)
  report['elapsed_seconds']=round(time.monotonic()-started,3)
  report['source_unchanged']=digest(ROOT/source['path'])==source['sha256']
  write(path,report)
 return report

def task(i):
 try:
  p=subprocess.run([sys.executable,str(Path(__file__).resolve()),'--case',str(i)],capture_output=True,text=True,timeout=100)
  path=OUT/f'{i:02d}.json';r=json.loads(path.read_text())
  if p.returncode and r['status']=='started':r.update(status='worker_failed',error=p.stderr[-2000:]);write(path,r)
 except subprocess.TimeoutExpired:
  path=OUT/f'{i:02d}.json';r=json.loads(path.read_text());r.update(status='timeout',error='outer worker deadline 100 seconds');write(path,r)
 return r

def summarize():
 review=json.loads((HERE.parent/'applicability/review.json').read_text())['records']
 selected=[r for r in review if r['category'] in ('prioritize_symbolic_trial','conditional_candidate')]
 assert len(selected)==41 and {r['id'] for r in selected}=={c['id'] for c in CASES}
 grouped=defaultdict(list)
 for i,c in enumerate(CASES):
  path=OUT/f'{i:02d}.json';r=json.loads(path.read_text());assert r['id']==c['id'];r['report_path']=str(path.relative_to(HERE));grouped[c['id']].append(r)
 rows=[]
 for item in selected:
  reports=grouped[item['id']];counts=Counter(r['status'] for r in reports)
  if counts['constructed']==len(reports):status='all_local_certificates_constructed'
  elif counts['constructed']:status='partial_local_certificates_constructed'
  elif counts['finite_diagnostic_mismatch']:status='finite_diagnostic_mismatch'
  elif counts['timeout']:status='timeout'
  elif counts['research_representation_gap']:status='research_representation_gap'
  elif counts['no_q_hypergeometric_antidifference']==len(reports):status='no_antidifference_for_chosen_local_problems'
  else:status='mixed_unresolved'
  rows.append({'id':item['id'],'review_group':item['category'],'status':status,
      'subproblem_count':len(reports),'subproblem_statuses':dict(counts),
      'original_domain_and_lean_verified':False,
      'reports':[{'branch':r['branch'],'status':r['status'],'stage':r['stage'],'path':r['report_path'],'sha256':digest(HERE/r['report_path'])} for r in reports]})
 summary={'identities_attempted':41,'subproblems_attempted':len(CASES),
    'identity_statuses':dict(Counter(r['status'] for r in rows)),
    'subproblem_statuses':dict(Counter(r['status'] for rr in grouped.values() for r in rr)),
    'excluded_deferred_identities':8,'excluded_existing_proved_identities':2,
    'new_lean_proofs':0,'interpretation':'Local formal certificates and diagnostic checks only; no proof of all original domain, boundaries, initial values or proposed transformations.',
    'code_sha256':{p:digest(HERE/p) for p in ['inputs.py','engine.py','run_trials.py']}}
 write(HERE/'summary.json',summary);write(HERE/'table.json',{'summary':summary,'records':rows})
 buf=io.StringIO();cw=csv.writer(buf);cw.writerow(['id','review_group','status','subproblem_count','subproblem_statuses','Lean完整证明'])
 for r in rows:cw.writerow([r['id'],r['review_group'],r['status'],r['subproblem_count'],json.dumps(r['subproblem_statuses']),'否'])
 (HERE/'table.csv').write_text('\ufeff'+buf.getvalue())
 e=html.escape
 page='''<!doctype html><html lang="zh"><meta charset="utf-8"><title>P1 41条候选实际试验</title><style>body{font:15px/1.6 system-ui;margin:24px}td,th{border:1px solid #ddd;padding:10px;vertical-align:top}table{border-collapse:collapse}input{padding:10px;width:70%}</style><h1>P1：18+23条候选实际试验</h1><p>排除另8条及已证明2条。每个局部问题均实际执行。输入为研究转录；证书不是完整Lean证明。变换、支撑、特殊参数与边界仍待原语义核验。</p>'''
 page+='<pre>'+e(json.dumps(summary,ensure_ascii=False,indent=2))+'</pre><p><a href="table.csv">CSV</a> · <a href="table.json">JSON</a></p><input id="q" placeholder="搜索ID或状态"><table><thead><tr><th>公式</th><th>分组</th><th>结果</th><th>各分支日志</th></tr></thead><tbody>'
 for r in rows:
  links='<br>'.join(f'<a href="{e(a["path"])}">{e(a["branch"])}：{e(a["status"])}</a>' for a in r['reports'])
  page+='<tr>'+''.join('<td>'+x+'</td>' for x in [e(r['id']),e(r['review_group']),e(r['status']),links])+'</tr>'
 page+='''</tbody></table><script>document.getElementById('q').addEventListener('input',e=>{for(const r of document.querySelectorAll('tbody tr'))r.hidden=!r.textContent.toLowerCase().includes(e.target.value.toLowerCase())});</script></html>'''
 (HERE/'index.html').write_text(page);print(json.dumps(summary,ensure_ascii=False,indent=2))

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--case',type=int);parser.add_argument('--summarize',action='store_true');args=parser.parse_args()
 if args.case is not None:worker(args.case);return
 if args.summarize:summarize();return
 OUT.mkdir(exist_ok=True)
 with ThreadPoolExecutor(max_workers=4) as pool:
  futures=[pool.submit(task,i) for i in range(len(CASES))]
  for done,future in enumerate(as_completed(futures),1):
   r=future.result();print(f'{done}/{len(CASES)} {r["id"]}/{r["branch"]}: {r["status"]} ({r["stage"]})',flush=True)
 summarize()

if __name__=='__main__':main()
