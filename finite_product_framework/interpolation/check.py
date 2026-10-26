#!/usr/bin/env python3
"""Kernel checks of interpolation and principal-part certificates, including negatives."""
import copy
import json
from pathlib import Path
import sys
import uuid

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from workflow.contracts import HERE,ROOT,accept_proof,save,sha
from interpolation.pipeline import PREP,probe,prove_source,lean,environment

CASES=[
 ('cubic','polynomial_interpolation','',
  '(x+y)^3 = x^3+3*x^2*y+3*x*y^2+y^3',True),
 ('insufficient_two_roots','polynomial_interpolation','', 'x*(x-1)=0',False),
 ('simple_poles','rational_principal_parts','(hm : x-1 ≠ 0) (hp : x+1 ≠ 0)',
  '1/(x-1)-1/(x+1)=2/((x-1)*(x+1))',True),
 ('repeated_pole_and_polynomial_part','rational_principal_parts','(hm : x-1 ≠ 0)',
  '(x^3-2*x^2+2*x+1)/(x-1)^2 = x+1/(x-1)+2/(x-1)^2',True),
 ('missing_polynomial_part','rational_principal_parts','(hm : x-1 ≠ 0)',
  '(x^3-2*x^2+2*x+1)/(x-1)^2 = 1/(x-1)+2/(x-1)^2',False),
 ('possibly_coalescing_poles','rational_principal_parts','(ha : x-y ≠ 0) (hb : x-z ≠ 0)',
  '1/(x-y)-1/(x-z)=(y-z)/((x-y)*(x-z))',True),
 ('missing_denominator_condition','polynomial_interpolation','', '(x-1)/(x-1)=1',False),
]


def main():
    work=HERE/'generated/interpolation_checks'/uuid.uuid4().hex;work.mkdir(parents=True)
    report={'status':'started','cases':[],'train_proofs_counted':0,'work_directory':str(work)}
    try:
        build=work/'build';build.mkdir()
        env,deps=environment(build)
        data={'dependencies':deps}
        accepted=[]
        for name,backend,hypotheses,target,expected in CASES:
            case=work/name;case.mkdir()
            source=('import Benchmark.Representation\nnamespace InterpolationRegression\n'
                    'set_option autoImplicit false\nset_option linter.unusedVariables false\n'
                    f'theorem statement (x y z : ℚ) {hypotheses} :\n  {target} := by\n  sorry\n'
                    'end InterpolationRegression\n')
            file=case/'source.lean';file.write_text(source)
            snapshot={'path':str(file.relative_to(ROOT)),'snapshot':str(file),'sha256':sha(file),
                      'theorem':'InterpolationRegression.statement'}
            initial=probe(source,PREP+'\ninterpolation_export "initial"',case,env,'Initial')['initial']
            local=copy.deepcopy(data);local.update(initial=initial,source_text_sha256=sha(file))
            result=prove_source(source,snapshot,case,env,local,{'max_degree':8,'symbolic_seconds':100},backend)
            if result['status']=='proved':
                accept_proof(result,snapshot,case);accepted.append((result,snapshot,case))
            ok=(result['status']=='proved')==expected
            report['cases'].append({'name':name,'backend':backend,'status':result['status'],'passed':ok,
                                    'report':str(case/'interpolation_report.json')})
            save(work/'report.json',report)
            if not ok:raise AssertionError(name+': '+result['status'])
        # A forged degree bound must fail in Lean even though 0 and 1 are roots.
        forged=work/'ForgedDegree.lean'
        forged.write_text('import Benchmark.InterpolationRules\nopen Polynomial\n'
            'example : (X*(X-1) : Polynomial ℚ) = 0 := by\n'
            '  apply FiniteQInterpolation.zero_of_samples _ 1\n'
            '  · compute_degree\n'
            '  · intro i; fin_cases i <;> norm_num\n')
        checked=lean(forged,env);save(work/'forged_degree.json',checked)
        if checked['exit_code']==0:raise AssertionError('forged degree accepted')
        report['forged_degree_rejected']=True
        # Distinctness is now checked per node family, not a global CharZero gate.
        extra=[
          ('field_linear','{K : Type*} [Field K] (x : K)','x+1=1+x',True),
          ('no_nodes_quadratic','{K : Type*} [Field K] (x : K)','(x+1)^2=x^2+2*x+1',False),
          ('geometric_cubic','{K : Type*} [Field K] (x q : K) (h : FiniteQBenchmark.regular q)',
           '(x+1)^3=x^3+3*x^2+3*x+1',True),
          ('positive_characteristic','(x : ZMod 2)','x+1=1+x',True),
          ('symbolic_tail','{K : Type*} [Field K] (a q : K) (n k : ℕ) (h : FiniteQBenchmark.regular q) (hk : k≤n) (hd : FiniteQBenchmark.poch a q k ≠ 0)',
           'FiniteQBenchmark.poch (a*q^k) q (n-k)=FiniteQBenchmark.poch a q n / FiniteQBenchmark.poch a q k',True),
          ('renamed_reversed','{K : Type*} [Field K] (u t : K) (m j : ℕ) (h : FiniteQBenchmark.regular t) (hj : j≤m) (hd : FiniteQBenchmark.poch u t j ≠ 0)',
           'FiniteQBenchmark.poch u t m / FiniteQBenchmark.poch u t j = FiniteQBenchmark.poch (u*t^j) t (m-j)',True),
          ('missing_regular','{K : Type*} [Field K] (a q : K) (n k : ℕ) (hk : k≤n) (hd : FiniteQBenchmark.poch a q k ≠ 0)',
           'FiniteQBenchmark.poch (a*q^k) q (n-k)=FiniteQBenchmark.poch a q n / FiniteQBenchmark.poch a q k',False),
          ('wrong_shift','{K : Type*} [Field K] (a q : K) (n k : ℕ) (h : FiniteQBenchmark.regular q) (hk : k≤n) (hd : FiniteQBenchmark.poch a q k ≠ 0)',
           'FiniteQBenchmark.poch (a*q^(k+1)) q (n-k)=FiniteQBenchmark.poch a q n / FiniteQBenchmark.poch a q k',False),
        ]
        for name,binders,target,expected in extra:
            case=work/name;case.mkdir()
            source=f'import Benchmark.Representation\nnamespace InterpolationRegression\ntheorem statement {binders} : {target} := by\n  sorry\nend InterpolationRegression\n'
            file=case/'source.lean';file.write_text(source)
            snapshot={'path':str(file.relative_to(ROOT)),'snapshot':str(file),'sha256':sha(file),'theorem':'InterpolationRegression.statement'}
            initial=probe(source,PREP+'\ninterpolation_export "initial"',case,env,'Initial')['initial']
            local=dict(data,initial=initial,source_text_sha256=sha(file))
            result=prove_source(source,snapshot,case,env,local,{'max_degree':8,'symbolic_seconds':60},'polynomial_interpolation')
            if result['status']=='proved':
                accept_proof(result,snapshot,case);accepted.append((result,snapshot,case))
            ok=(result['status']=='proved')==expected
            report['cases'].append({'name':name,'status':result['status'],'passed':ok,'report':str(case/'interpolation_report.json')})
            save(work/'report.json',report)
            if not ok:raise AssertionError(name+': '+result['status'])
        native,snapshot,case=accepted[-1]
        bad=copy.deepcopy(native);bad['certificate']['sha256']='0'*64
        try:accept_proof(bad,snapshot,case)
        except ValueError as exc:
            if 'certificate' not in str(exc):raise
        else:raise AssertionError('changed certificate accepted')
        report['certificate_tampering_rejected']=True
        report['status']='passed'
    except Exception as exc:report.update(status='failed',error=f'{type(exc).__name__}: {exc}')
    save(work/'report.json',report);save(HERE/'generated/interpolation_validation.json',report)
    print(json.dumps(report,ensure_ascii=False,indent=2))
    return 0 if report['status']=='passed' else 1


if __name__=='__main__':raise SystemExit(main())
