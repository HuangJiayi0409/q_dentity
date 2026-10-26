#!/usr/bin/env python3
"""Kernel checks, including false maps, fixed points and characteristic two."""
import copy
import json
from pathlib import Path
import sys
import uuid
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from workflow.contracts import HERE,ROOT,accept_proof,save,sha
from combinatorial.pipeline import environment,extract,plans,prove_source

CASES=[
 ('range_reflection','weighted_bijection','(n : ℕ) (q : ℚ)',
  '(∑ i ∈ Finset.range n, q^(n-1-i)) = ∑ i ∈ Finset.range n, q^i',True),
 ('integer_reflection','weighted_bijection','(n : ℤ) (w : ℤ → ℚ)',
  '(∑ i ∈ Finset.Icc (-n) n, w (-i)) = ∑ i ∈ Finset.Icc (-n) n, w i',True),
 ('bad_weight','weighted_bijection','(n : ℕ)',
  '(∑ i ∈ Finset.range n, (i : ℚ)+1) = ∑ i ∈ Finset.range n, (i : ℚ)',False),
 ('bad_domain','weighted_bijection','(n : ℕ)',
  '(∑ i ∈ Finset.range (n+1), (1 : ℚ)) = ∑ i ∈ Finset.range n, (1 : ℚ)',False),
 ('subset_toggle','sign_reversing_involution','(n : ℕ)',
  '(∑ t ∈ (Finset.range (n+1)).powerset, (-1 : ℚ)^t.card) = 0',True),
 ('weighted_subset_toggle','sign_reversing_involution','(n : ℕ) (w : Finset ℕ → ℚ)',
  '(∑ t ∈ (Finset.range (n+1)).powerset, (-1 : ℚ)^t.card * w (t.erase 0)) = 0',True),
 ('toggle_wrong_weight','sign_reversing_involution','(n : ℕ)',
  '(∑ t ∈ (Finset.range (n+1)).powerset, (1 : ℚ)) = 0',False),
 ('empty_toggle_domain','sign_reversing_involution','',
  '(∑ t ∈ (Finset.range 0).powerset, (-1 : ℚ)^t.card) = 0',False),
 ('integer_cancellation','sign_reversing_involution','(n : ℤ)',
  '(∑ i ∈ Finset.Icc (-n) n, (i : ℚ)) = 0',True),
 ('fixed_point_char_two','sign_reversing_involution','',
  '(∑ i ∈ Finset.range 1, (1 : ZMod 2)) = 0',False),
 ('renamed_subset_bridge','weighted_bijection','{K : Type*} [Field K] (t : K) (m r : ℕ) (ht : t ≠ 0)',
  'FiniteQBenchmark.gaussian t m r = ∑ u ∈ (Finset.Icc 1 m).powersetCard r, t^(((∑ a ∈ u, a):ℤ)-(r:ℤ)*(r+1)/2)',True),
 ('missing_q_nonzero','weighted_bijection','{K : Type*} [Field K] (t : K) (m r : ℕ)',
  'FiniteQBenchmark.gaussian t m r = ∑ u ∈ (Finset.Icc 1 m).powersetCard r, t^(((∑ a ∈ u, a):ℤ)-(r:ℤ)*(r+1)/2)',False),
]

def main():
    work=HERE/'generated/combinatorial_checks'/uuid.uuid4().hex;work.mkdir(parents=True)
    report={'status':'started','cases':[],'train_proofs_counted':0,'test_files_read':0,'work_directory':str(work)}
    try:
        base=work/'environment';base.mkdir()
        env,deps=environment(base)
        data={'dependencies':deps,'lean_path':env['LEAN_PATH']}
        save(base/'environment.json',data)
        report['environment_origin']='fresh current source; no historical Train proof required'
        for name,backend,context,target,expected in CASES:
            case=work/name;case.mkdir()
            text=('import Benchmark.CombinatorialRepresentation\nopen scoped BigOperators\nnamespace CombinatorialRegression\n'
                  'set_option autoImplicit false\nset_option linter.unusedVariables false\n'
                  f'theorem statement {context} :\n {target} := by\n  sorry\nend CombinatorialRegression\n')
            file=case/'source.lean';file.write_text(text)
            source={'path':str(file.relative_to(ROOT)),'snapshot':str(file),'sha256':sha(file),'theorem':'CombinatorialRegression.statement'}
            raw=extract(text,case,env)
            local=copy.deepcopy(data);local.update(expression=raw,plans=plans(raw),source_text_sha256=sha(file))
            result=prove_source(text,source,case,env,local,{'symbolic_seconds':60},backend)
            if result['status']=='proved':
                accept_proof(result,source,case)
                bad=copy.deepcopy(result);bad['certificate']['sha256']='0'*64
                try:accept_proof(bad,source,case)
                except ValueError as exc:
                    if 'certificate' not in str(exc):raise
                else:raise AssertionError('changed certificate accepted')
            passed=(result['status']=='proved')==expected
            report['cases'].append({'name':name,'backend':backend,'status':result['status'],'passed':passed,
                                    'report':str(case/'combinatorial_report.json')})
            save(work/'report.json',report)
            if not passed:raise AssertionError(name)
        report.update(status='passed',certificate_tampering_rejected=True)
    except Exception as exc:report.update(status='failed',error=f'{type(exc).__name__}: {exc}')
    save(work/'report.json',report);save(HERE/'generated/combinatorial_validation.json',report)
    print(json.dumps(report,ensure_ascii=False,indent=2))
    return 0 if report['status']=='passed' else 1
if __name__=='__main__':raise SystemExit(main())
