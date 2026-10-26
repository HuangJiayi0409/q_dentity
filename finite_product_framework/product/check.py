#!/usr/bin/env python3
"""Check real generated certificates on synthetic structural and false variants.

Uses the dependencies from an accepted native product run. Synthetic cases are
never counted as train coverage. Outputs retained for review and replay.
"""
import copy
import hashlib
import json
from pathlib import Path
import sys
import uuid

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from workflow.contracts import HERE, ROOT, accept_proof, save, sha
from workflow.worker import prepared_environment
from product.pipeline import extract, plans, prove_source

CASES = [
    ('renamed_no_positive_length',
     'poch u v (s*t) = ∏ r ∈ Finset.range s, poch (u*v^r) (v^s) t', True),
    ('reverse_equality',
     '(∏ r ∈ Finset.range s, poch (u*v^r) (v^s) t) = poch u v (s*t)', True),
    ('split', 'poch u v (s+t) = poch u v s * poch (u*v^s) v t', True),
    ('factor_fusion', 'poch (u^2) (v^2) s = poch u v s * poch (-u) v s', True),
    ('reflection', '(∏ r ∈ Finset.range s, (1-u*v^(s-1-r))) = poch u v s', True),
    ('false_factor', 'poch (u^2) (v^2) s = poch u v s * poch u v s', False),
    ('false_stride', 'poch u v (s*t) = ∏ r ∈ Finset.range s, poch (u*v^r) (v^(s+1)) t', False),
]


def main():
    work=HERE/'generated/product_checks'/uuid.uuid4().hex;work.mkdir(parents=True)
    report={'status':'failed','cases':[],'train_proofs_counted':0,'work_directory':str(work)}
    try:
        native=[]
        for file in (HERE/'generated/product').glob('*/report.json'):
            r=json.loads(file.read_text())
            if r.get('status')=='proved': native.append((file.stat().st_mtime,r))
        _,r=max(native)
        attempt=Path(r['attempts'][-1]['result'])
        accepted=json.loads(attempt.read_text());accept_proof(accepted,r['source'],attempt.parent)
        data=json.loads((Path(r['work_directory'])/'analysis/product/environment.json').read_text())
        env=prepared_environment(data)
        report['native_report']=str(Path(r['work_directory'])/'report.json')
        for name,target,expected in CASES:
            case=work/name;case.mkdir()
            source=('import Benchmark.Representation\nopen scoped BigOperators\nopen FiniteQBenchmark\n'
                    'set_option autoImplicit false\nset_option linter.unusedVariables false\n'
                    'namespace ProductRegression\nvariable {K : Type*} [Field K]\n'
                    'theorem statement (u v : K) (s t : ℕ) :\n    '+target+' := by\n  sorry\n'
                    'end ProductRegression\n')
            source_file=case/'source.lean';source_file.write_text(source)
            raw=extract(source,case,env)
            analysis=copy.deepcopy(data)
            analysis.update(expression=raw,plans=plans(raw),source_text_sha256=sha(source_file))
            snapshot={'path':str(source_file.relative_to(ROOT)),'snapshot':str(source_file),
                      'sha256':sha(source_file),'theorem':'ProductRegression.statement'}
            result=prove_source(source,snapshot,case,env,analysis,{'symbolic_seconds':100})
            if result['status']=='proved':accept_proof(result,snapshot,case)
            ok=(result['status']=='proved') if expected else result['status']=='search_exhausted'
            report['cases'].append({'name':name,'expected_proved':expected,'status':result['status'],
                                    'passed':ok,'report':str(case/'product_report.json')})
            save(work/'report.json',report)
            if not ok:raise AssertionError(name+': '+result['status'])
        # Certificate corruption must fail even if the original Lean log succeeded.
        bad=copy.deepcopy(accepted);bad['certificate']['sha256']='0'*64
        try:accept_proof(bad,r['source'],attempt.parent)
        except ValueError as exc:
            if 'certificate' not in str(exc):raise
        else:raise AssertionError('changed certificate accepted')
        report['certificate_tampering_rejected']=True
        report['status']='passed'
    except Exception as exc:
        report['error']=f'{type(exc).__name__}: {exc}'
    save(work/'report.json',report);save(HERE/'generated/product_validation.json',report)
    print(json.dumps(report,ensure_ascii=False,indent=2))
    return 0 if report['status']=='passed' else 1


if __name__=='__main__':raise SystemExit(main())
