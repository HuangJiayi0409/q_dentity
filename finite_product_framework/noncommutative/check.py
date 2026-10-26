#!/usr/bin/env python3
"""Positive/negative operator regressions; synthetic cases are not Train coverage."""
import copy
import json
from pathlib import Path
import sys
import uuid
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from workflow.contracts import HERE,ROOT,accept_proof,save,sha
from workflow.worker import prepared_environment
from noncommutative.pipeline import extract,supported,prove_source

CASES=[
 ('distribution','{A : Type*} [Ring A] (X Y Z : A)', 'X*(Y+Z)=X*Y+X*Z',True),
 ('square','{A : Type*} [Ring A] (X Y : A)', '(X+Y)^2=X^2+X*Y+Y*X+Y^2',True),
 ('missing_relation','{A : Type*} [Ring A] (X Y : A)', 'Y*X=X*Y',False),
 ('wrong_commutative_square','{A : Type*} [Ring A] (X Y : A)', '(X+Y)^2=X^2+2*(X*Y)+Y^2',False),
 ('q_relation','{K A : Type*} [Field K] [Ring A] [Algebra K A] (q : K) (X Y : A) (h : Y*X=q • (X*Y))',
  '(X+Y)^2=X^2+X*Y+q • (X*Y)+Y^2',True),
 ('renamed_operators','{K : Type*} [Field K] (t : K) (p : Polynomial K)',
  'FiniteQBenchmark.kacM t (FiniteQBenchmark.kacX p)=t • FiniteQBenchmark.kacX (FiniteQBenchmark.kacM t p)',True),
 ('bad_scalar','{K : Type*} [Field K] (t : K) (p : Polynomial K)',
  'FiniteQBenchmark.kacM t (FiniteQBenchmark.kacX p)=(t+1) • FiniteQBenchmark.kacX (FiniteQBenchmark.kacM t p)',False),
 ('symbolic_power','{A : Type*} [Ring A] (X Y : A) (n : ℕ)', 'X^n*Y=X^n*Y',False),
]

def main():
    work=HERE/'generated/noncommutative_checks'/uuid.uuid4().hex;work.mkdir(parents=True)
    report={'status':'started','cases':[],'train_proofs_counted':0,'test_files_read':0,'work_directory':str(work)}
    try:
        runs=[]
        for file in (HERE/'generated/noncommutative').glob('*/report.json'):
            r=json.loads(file.read_text())
            if r.get('status')=='proved':runs.append((file.stat().st_mtime,r))
        _,r=max(runs);attempt=Path(r['attempts'][-1]['result']);native=json.loads(attempt.read_text())
        accept_proof(native,r['source'],attempt.parent)
        data=json.loads((Path(r['work_directory'])/'analysis/noncommutative/environment.json').read_text())
        env=prepared_environment(data)
        for name,context,target,expected in CASES:
            case=work/name;case.mkdir()
            text=('import Benchmark.OperatorAtoms\nnamespace OperatorRegression\n'
                  'set_option autoImplicit false\nset_option linter.unusedVariables false\n'
                  f'theorem statement {context} :\n {target} := by\n  sorry\nend OperatorRegression\n')
            file=case/'source.lean';file.write_text(text)
            source={'path':str(file.relative_to(ROOT)),'snapshot':str(file),'sha256':sha(file),'theorem':'OperatorRegression.statement'}
            raw=extract(text,case,env);ok,reason=supported(raw)
            if ok:
                local=copy.deepcopy(data);local.update(expression=raw,source_text_sha256=sha(file))
                result=prove_source(text,source,case,env,local,{'symbolic_seconds':60})
                if result['status']=='proved':accept_proof(result,source,case)
            else:result={'status':'unsupported','reason':reason}
            save(case/'result.json',result)
            passed=(result['status']=='proved')==expected
            report['cases'].append({'name':name,'status':result['status'],'passed':passed})
            save(work/'report.json',report)
            if not passed:raise AssertionError(name)
        bad=copy.deepcopy(native);bad['certificate']['sha256']='0'*64
        try:accept_proof(bad,r['source'],attempt.parent)
        except ValueError as exc:
            if 'certificate' not in str(exc):raise
        else:raise AssertionError('changed certificate accepted')
        report.update(status='passed',certificate_tampering_rejected=True)
    except Exception as exc:report.update(status='failed',error=f'{type(exc).__name__}: {exc}')
    save(work/'report.json',report);save(HERE/'generated/noncommutative_validation.json',report)
    print(json.dumps(report,ensure_ascii=False,indent=2))
    return 0 if report['status']=='passed' else 1
if __name__=='__main__':raise SystemExit(main())
