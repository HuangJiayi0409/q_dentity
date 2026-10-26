#!/usr/bin/env python3
"""Nested sequence identities and failures of initial/shift/domain obligations."""
import copy
import json
from pathlib import Path
import sys
import uuid
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from workflow.contracts import HERE,ROOT,accept_proof,save,sha
from workflow.worker import prepared_environment
from difference_ring.pipeline import probe,plans,tower,prove_source,lean

CASES=[
 ('nested_sum','(n : ℕ) (f : ℕ → ℚ)',
  '(∑ k ∈ Finset.range n, (((k : ℚ)+1)*f k + ∑ j ∈ Finset.range k, f j)) = (n : ℚ)*(∑ j ∈ Finset.range n, f j)',True),
 ('prefix_square','{K : Type*} [Field K] (n : ℕ) (f : ℕ → K)',
  '(∑ k ∈ Finset.range n, (2*f k*(∑ j ∈ Finset.range k, f j)+(f k)^2)) = (∑ j ∈ Finset.range n, f j)^2',True),
 ('nested_sum_product','(n : ℕ) (f : ℕ → ℚ)',
  '(∑ k ∈ Finset.range n, (∑ i ∈ Finset.range k, f i)*(∏ j ∈ Finset.range k, (1+∑ i ∈ Finset.range j, f i))) = (∏ j ∈ Finset.range n, (1+∑ i ∈ Finset.range j, f i))-1',True),
 ('vanishing_product_allowed','{K : Type*} [Field K] (n : ℕ) (f : ℕ → K)',
  '(∑ k ∈ Finset.range n, (f k-1)*(∏ j ∈ Finset.range k, f j)) = (∏ j ∈ Finset.range n, f j)-1',True),
 ('wrong_initial_value','(n : ℕ) (f : ℕ → ℚ)',
  '(∑ k ∈ Finset.range n, (f k-1)*(∏ j ∈ Finset.range k, f j)) = (∏ j ∈ Finset.range n, f j)',False),
 ('wrong_increment','(n : ℕ) (f : ℕ → ℚ)',
  '(∑ k ∈ Finset.range n, (f k+1)*(∏ j ∈ Finset.range k, f j)) = (∏ j ∈ Finset.range n, f j)-1',False),
 ('missing_denominator','{K : Type*} [Field K] (a b q : K) (n : ℕ)',
  '(1-b*q^(n+1))*FiniteQBenchmark.fineC a b q (n+1) = (1-a*q^(n+1))*FiniteQBenchmark.fineC a b q n',False),
 ('empty_prefix','(f : ℕ → ℚ)',
  '(∑ k ∈ Finset.range 0, (∏ j ∈ Finset.range k, f j)) = 0',True),
]


def main():
    work=HERE/'generated/difference_ring_checks'/uuid.uuid4().hex;work.mkdir(parents=True)
    report={'status':'started','cases':[],'train_proofs_counted':0,'test_files_read':0,'work_directory':str(work)}
    try:
        runs=[]
        for file in (HERE/'generated/difference_ring').glob('*/report.json'):
            r=json.loads(file.read_text())
            if r.get('status')=='proved':runs.append((file.stat().st_mtime,r))
        _,r=max(runs);attempt=Path(r['attempts'][-1]['result']);native=json.loads(attempt.read_text())
        accept_proof(native,r['source'],attempt.parent)
        data=json.loads((Path(r['work_directory'])/'analysis/difference_ring/environment.json').read_text())
        env=prepared_environment(data);report['native_report']=str(Path(r['work_directory'])/'report.json')
        positive=[]
        for name,context,target,expected in CASES:
            case=work/name;case.mkdir()
            text=('import Benchmark.DifferenceRules\nopen scoped BigOperators\nnamespace DifferenceRegression\n'
                  'set_option autoImplicit false\nset_option linter.unusedVariables false\n'
                  f'theorem statement {context} :\n {target} := by\n  sorry\nend DifferenceRegression\n')
            file=case/'source.lean';file.write_text(text)
            source={'path':str(file.relative_to(ROOT)),'snapshot':str(file),'sha256':sha(file),'theorem':'DifferenceRegression.statement'}
            raw=probe(text,'  dr_expand\n  dr_structure',case,env,'Structure')
            local=copy.deepcopy(data);local.update(expression=raw,plans=plans(raw),tower=tower(raw),source_text_sha256=sha(file))
            result=prove_source(text,source,case,env,local,{'symbolic_seconds':100,'max_degree':6,'max_unknowns':10000})
            if result['status']=='proved':
                accept_proof(result,source,case);positive.append((case,result))
            passed=(result['status']=='proved')==expected
            report['cases'].append({'name':name,'status':result['status'],'passed':passed,
                                    'report':str(case/'difference_ring_report.json')})
            save(work/'report.json',report)
            if not passed:raise AssertionError(name)
        # Falsify a nontrivial ideal-membership coefficient, then recompile.
        for case,result in positive:
            text=Path(result['verification']['proof_file']).read_text()
            if 'linear_combination' not in text:continue
            import re
            forged=case/'ForgedReduction.lean'
            forged.write_text(re.sub(r'linear_combination[^\n]*','ring',text))
            checked=lean(forged,env);save(case/'forged_reduction.json',checked)
            if checked['exit_code']==0:raise AssertionError('invalid reduction accepted')
            report['forged_reduction_rejected']=True;break
        if not report.get('forged_reduction_rejected'):raise AssertionError('no nontrivial relation reduction exercised')
        bad=copy.deepcopy(native);bad['certificate']['sha256']='0'*64
        try:accept_proof(bad,r['source'],attempt.parent)
        except ValueError as exc:
            if 'certificate' not in str(exc):raise
        else:raise AssertionError('changed certificate accepted')
        report.update(status='passed',certificate_tampering_rejected=True)
    except Exception as exc:report.update(status='failed',error=f'{type(exc).__name__}: {exc}')
    save(work/'report.json',report);save(HERE/'generated/difference_ring_validation.json',report)
    print(json.dumps(report,ensure_ascii=False,indent=2))
    return 0 if report['status']=='passed' else 1
if __name__=='__main__':raise SystemExit(main())
