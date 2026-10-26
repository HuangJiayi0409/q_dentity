"""Fresh Lean checks of machine templates, guards, and an actual solver consumer.

Synthetic statements only. No Test/Train statements, API calls or batch launches.
"""
import argparse
import json
import os
from pathlib import Path
import re
import sys
import time

HERE=Path(__file__).resolve().parent
FRAMEWORK=HERE.parent
ROOT=FRAMEWORK.parent
sys.path[:0]=[str(FRAMEWORK/'p1'),str(FRAMEWORK)]

from math_library.registry import Library
from math_library.build import prepare as build_library
from lean_pipeline import environment, extract, lean, assemble
from general_summation import frontend, synthesize
from run import construct_in_process
from core import CoreBudget
from proof_fixture import source_for
from workflow.contracts import accept_proof, sha


def save(path,value):path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();out=args.output.resolve();out.mkdir(parents=True,exist_ok=False)
    start=time.monotonic();lib=Library();records=[]
    built=build_library(out/'library')
    env=dict(os.environ,LEAN_PATH=built['lean_path'])
    deps=built['dependencies']
    def compile_case(name,body,expected=True):
        path=out/(name+'.lean');path.write_text('import Benchmark.MathLibraryRules\nopen scoped BigOperators\n'+body)
        result=lean(path,env,timeout=120);save(out/(name+'.json'),result)
        success=result['exit_code']==0 and 'sorryAx' not in result['output']
        records.append(dict(case=name,expected_success=expected,passed=success==expected))
        print(name,'passed' if success==expected else 'FAILED',flush=True)
        return result
    result=compile_case('catalogue_equations','\n'.join(lib.lean_check(k) for k in lib.rules))
    for key in lib.rules:
        marker="'check_"+key+"' depends on axioms: ["
        match=re.search(re.escape(marker)+r'([^\]]*)\]',result['output'])
        axioms={s.strip() for s in match[1].split(',') if s.strip()} if match else set()
        found=match is not None or "'check_"+key+"' does not depend on any axioms" in result['output']
        records.append(dict(case='axioms_'+key,passed=found and axioms<={'propext','Classical.choice','Quot.sound'},axioms=sorted(axioms)))
    compile_case('tampered_equation',lib.lean_check('poch_zero',rhs=['literal','K',2]),False)
    # Same formula but a missing hypothesis must fail in Lean, regardless of
    # any caller-supplied Python "fact".
    compile_case('missing_nonzero','''example (a q : ℚ) (d k : ℕ) :
  FiniteQBenchmark.poch (a*q^d) q k = FiniteQBenchmark.poch a q k *
    FiniteQBenchmark.poch (a*q^k) q d / FiniteQBenchmark.poch a q d := by
  apply FiniteQMathLibrary.poch_shift_quotient
  assumption
''',False)
    compile_case('zero_parameters_and_empty_support','''example (n : ℕ) :
  FiniteQBenchmark.poch (0 : ℚ) 0 (n+1) = FiniteQBenchmark.poch 0 0 n * (1-0*0^n) := by
  exact FiniteQMathLibrary.poch_successor 0 0 n
example (d k : ℕ) :
  FiniteQBenchmark.poch ((1 : ℚ)*1^d) 1 k * FiniteQBenchmark.poch 1 1 d =
  FiniteQBenchmark.poch 1 1 k * FiniteQBenchmark.poch (1*1^k) 1 d := by
  exact FiniteQMathLibrary.poch_shift_cross 1 1 d k
example (f : ℕ → ℚ) : (∑ i ∈ Finset.Icc 3 1, f i) = ∑ i ∈ Finset.range 0, f (3+i) := by
  exact FiniteQMathLibrary.sum_Icc f 3 1
''')
    # Check the *instantiated* representation consumed by the solver, in
    # addition to the universal typed templates checked by the library build.
    from math_library.source_views import finite_sum_view
    from math_library.test_library import node,li,v
    from general_sum_emit import source_term
    for name,aa,bb in [('empty',[],[]),('balanced',[v('a')],[]),('negative',[v('a'),v('b')],[])]:
        raw=node('FiniteQBenchmark.phi',li(*aa),li(*bb),v('q'),v('z'),v('n'))
        view=finite_sum_view(raw)
        def list_text(items):return '['+','.join(x['name'] for x in items)+']'
        compile_case('phi_view_'+name,
            'example {K : Type*} [Field K] (a b q z : K) (n : ℕ) :\n'
            '  FiniteQBenchmark.phi '+list_text(aa)+' '+list_text(bb)+' q z n = '+source_term(view['expression'])+' := by\n'
            '  simp [FiniteQBenchmark.phi, FiniteQBenchmark.phiTerm, FiniteQBenchmark.pochList, mul_assoc, mul_comm, mul_left_comm]\n')
    # Test source extraction and actual methods in their own production environment.
    env,p1deps=environment(out/'environment')
    deps+=p1deps
    # A new input wrapper enters the existing symbolic constructor and its
    # existing original-statement proof exit. No library summation formula.
    cases=[('geometric_wrapper', '(q : K) (hq : q ≠ 1) (n : ℕ) : '
        'FiniteQBenchmark.geometric q n = (q^n-1)/(q-1)',True),
        ('geometric_missing_condition','(q : K) (n : ℕ) : '
        'FiniteQBenchmark.geometric q n = (q^n-1)/(q-1)',False)]
    for name,statement,expected in cases:
        work=out/name;work.mkdir();source=source_for(statement);path=work/'source.lean';path.write_text(source)
        raw=extract(source,work,env);problem,model=frontend(raw,name,'telescoping')
        save(work/'problem.json',problem);save(work/'model.json',model)
        result=construct_in_process(problem,CoreBudget(seconds=40,max_order=4),'direct_q_gosper')
        save(work/'construction.json',result)
        if result['construction']['status']!='constructed':raise RuntimeError('synthetic construction unexpectedly failed')
        verify=synthesize(source,model,result['construction'],work,env);save(work/'verification.json',verify)
        success=verify['status']=='proved'
        audit=None
        if success:
            source_info=dict(identity='synthetic:'+name,path=str(path),snapshot=str(path),sha256=sha(path),theorem='CoreExitRegression.statement')
            audit=accept_proof(dict(status='proved',remaining_obligations=[],verification=verify,dependencies=deps),source_info,work)
            save(work/'original_audit.json',audit)
        records.append(dict(case=name,passed=success==expected,expected_success=expected,status=verify['status'],original_audit=audit))
        print(name,verify['status'],flush=True)
    # Existing extractor reports the formerly unsupported function; do not count
    # a relabelled failure as a newly supported proof.
    from lean_pipeline import proof_slot
    old_extract=(FRAMEWORK/'p1/lean/Extract.lean').read_text()
    before=out/'before_library_extraction.lean'
    before.write_text(assemble([old_extract,proof_slot(source_for(cases[0][1]),'  p1_export')]))
    prior=lean(before,env);save(out/'before_library_extraction.json',prior)
    records.append(dict(case='before_library_rejected_wrapper',passed=prior['exit_code']!=0 and
        'Unsupported expression in P1 frontend:' in prior['output'] and 'geometric' in prior['output']))
    # The product method shares the extended serializer. Check that its existing
    # constructor and complete-original exit still work, without importing the
    # library's split lemma into the method's proof environment.
    from product import pipeline as product
    work=out/'product_regression';work.mkdir()
    source=source_for('(a q : K) (m n : ℕ) : poch a q (m+n) = poch a q m * poch (a*q^m) q n')
    path=work/'source.lean';path.write_text(source)
    source_info=dict(identity='synthetic:product_regression',path=str(path),snapshot=str(path),
                     sha256=sha(path),theorem='CoreExitRegression.statement')
    product.prepare(source,work)
    data=json.loads((work/'environment.json').read_text())
    report=product.prove_source(source,source_info,work,dict(os.environ,LEAN_PATH=data['lean_path']),data,
                                dict(symbolic_seconds=60))
    audit=accept_proof(report,source_info,work) if report['status']=='proved' else None
    save(work/'original_audit.json',audit)
    deps+=data['dependencies']
    records.append(dict(case='product_regression',passed=report['status']=='proved',original_audit=audit))
    print('product_regression',report['status'],flush=True)
    for dep in deps:
        if sha(ROOT/dep['path'])!=dep['sha256']:raise RuntimeError('dependency changed during validation')
    result=dict(status='passed' if all(r['passed'] for r in records) else 'failed',records=records,
        catalogue_objects=len(lib.objects),catalogue_rules=len(lib.rules),catalogue_sha256=lib.sha256,
        dependencies=deps,elapsed_seconds=round(time.monotonic()-start,3),test_files_read=0,
        train_proofs_attempted=0,api_calls=0)
    save(out/'validation.json',result)
    return 0 if result['status']=='passed' else 1


if __name__=='__main__':raise SystemExit(main())
