#!/usr/bin/env python3
"""Accept twelve independent CLIs; native successes, unresolved attempts and module proofs.

--audit-existing audits completed method-specific runs instead of repeating native runs.
It always executes orchestration regressions and checks current proof artifacts.
Acceptance identities live here, never in production routing code.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from workflow.contracts import HERE,ROOT,BACKENDS,accept_proof,save,sha

CASES={
 'FQI-SRC-AP-3.3.9':'direct_q_gosper',
 'FQI-SRC-GR2-II-34':'bibasic_gosper',
 'FQI-FINITE-Q-BINOMIAL':'target_first_order',
 'FQI-GAUSS-ALTERNATING':'general_q_zeilberger',
 'FQI-SRC-GR2-7.Ex40':'ore_closure',
 'FQI-SRC-GR2-10.Ex18':'multisum',
 'FQI-SRC-FINE-15.2':'cauchy_coefficient',
 'FQI-POCHHAMMER-RESIDUES':'finite_product_indices',
 'FQI-SRC-KAC-CHEUNG-1.11-12':'polynomial_interpolation',
 'FQI-SRC-KAC-CHEUNG-1.13-14':'rational_principal_parts',
 'FQI-SRC-KAC-CHEUNG-5.7':'operator_word_normalization',
 'FQI-SRC-KAC-CHEUNG-6.5':'weighted_bijection',
 'FQI-SRC-FINE-2.3':'triangular_difference_ring',
 'FQI-SRC-AQ-3.23':'finite_kernel_certificate',
 'FQI-RECTANGLE-PARTITIONS':'finite_omega_elimination'}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--audit-existing',action='store_true')
    args=parser.parse_args()
    result={'status':'failed','mode':'audit_existing' if args.audit_existing else 'fresh_native_runs',
            'native_cases':[],'regressions':[],'new_unique_train_proofs':0,
            'test_files_read':0,'legacy_full_suites_rerun':False}
    try:
        for script,timeout in [('test_workflow.py',120),('p1/test_pipeline.py',120)]:
            proc=subprocess.run([sys.executable,str(HERE/script)],capture_output=True,text=True,timeout=timeout)
            result['regressions'].append({'script':script,'exit_code':proc.returncode,'output':proc.stdout+proc.stderr})
            assert proc.returncode==0,script
        for identity,expected in CASES.items():
            if args.audit_existing:
                candidates=[]
                for file in (HERE/'generated'/BACKENDS[expected]).glob('*/report.json'):
                    report=json.loads(file.read_text())
                    if report.get('identity')==identity:candidates.append((file.stat().st_mtime,file,report))
                assert candidates,'Missing method-specific run: '+identity
                _,file,r=max(candidates,key=lambda x:x[0])
            else:
                proc=subprocess.run([sys.executable,str(HERE/f'prove_{BACKENDS[expected]}.py'),'--identity',identity,'--seconds','1000','--symbolic-seconds','500','--attempt-seconds','800'],capture_output=True,text=True,timeout=1030)
                assert proc.returncode==0,(identity,proc.stdout,proc.stderr)
                file=Path(json.loads(proc.stdout)['work_directory'])/'report.json'
                r=json.loads(file.read_text())
            assert r['method_request']==BACKENDS[expected]
            assert all(a['method']==BACKENDS[expected] for a in r['plan'])
            assert r['status']=='proved',(identity,r['status'])
            assert r['selected_backend']==expected,(identity,r['selected_backend'])
            successful=r['attempts'][-1];native_file=Path(successful['result'])
            native=json.loads(native_file.read_text())
            artifact=accept_proof(native,r['source'],native_file.parent)
            assert artifact==r['proof']
            result['native_cases'].append({'identity':identity,'backend':expected,'method':r['selected_method'],
                'status':'proved','report':str(file),'proof_sha256':artifact['proof_sha256']})
        result['methods_verified']=sorted({x['method'] for x in result['native_cases']})
        assert result['methods_verified']==['coefficient','combinatorial','difference_ring','interpolation','kernel_transform','macmahon','noncommutative','product','recurrence','telescoping']
        # Involution module proofs are not additional native Train results.
        if not args.audit_existing:
            proc=subprocess.run([sys.executable,str(HERE/'combinatorial/check.py')],capture_output=True,text=True,timeout=900)
            assert proc.returncode==0,(proc.stdout,proc.stderr)
        module=json.loads((HERE/'generated/combinatorial_validation.json').read_text())
        assert module['status']=='passed'
        result['synthetic_involution_cases']=[]
        for case in module['cases']:
            assert case['passed'],case['name']
            if case['backend']!='sign_reversing_involution' or case['status']!='proved':continue
            file=Path(case['report']);native=json.loads(file.read_text())
            source_file=file.parent/'source.lean'
            source={'path':str(source_file.relative_to(ROOT)),'snapshot':str(source_file),
                    'sha256':sha(source_file),'theorem':'CombinatorialRegression.statement'}
            accept_proof(native,source,file.parent)
            result['synthetic_involution_cases'].append(case['name'])
        assert result['synthetic_involution_cases']
        if not args.audit_existing:
            proc=subprocess.run([sys.executable,str(HERE/'difference_ring/check.py')],capture_output=True,text=True,timeout=1000)
            assert proc.returncode==0,(proc.stdout,proc.stderr)
        module=json.loads((HERE/'generated/difference_ring_validation.json').read_text())
        assert module['status']=='passed'
        assert module['forged_reduction_rejected'] and module['certificate_tampering_rejected']
        result['synthetic_difference_ring_cases']=[]
        for case in module['cases']:
            assert case['passed'],case['name']
            if case['status']!='proved':continue
            file=Path(case['report']);native=json.loads(file.read_text())
            source_file=file.parent/'source.lean'
            source={'path':str(source_file.relative_to(ROOT)),'snapshot':str(source_file),
                    'sha256':sha(source_file),'theorem':'DifferenceRegression.statement'}
            accept_proof(native,source,file.parent)
            result['synthetic_difference_ring_cases'].append(case['name'])
        assert len(result['synthetic_difference_ring_cases'])==5
        result['structural_modules']={}
        for method in ('kernel_transform','spectral','determinant','macmahon'):
            if not args.audit_existing:
                proc=subprocess.run([sys.executable,str(HERE/method/'check.py')],capture_output=True,text=True,timeout=1100)
                assert proc.returncode==0,(proc.stdout,proc.stderr)
            module=json.loads((HERE/'generated'/(method+'_validation.json')).read_text())
            assert module['status']=='passed',method
            assert module['certificate_tampering_rejected']
            accepted=[]
            for case in module['cases']:
                assert case['passed'],case['name']
                if case['status']!='proved':continue
                file=Path(case['report']);native=json.loads(file.read_text());source_file=file.parent/'source.lean'
                source={'path':str(source_file.relative_to(ROOT)),'snapshot':str(source_file),
                    'sha256':sha(source_file),'theorem':'StructuralRegression.statement'}
                accept_proof(native,source,file.parent);accepted.append(case['name'])
            assert accepted,method
            result['structural_modules'][method]=accepted
        result['native_unresolved']=[]
        from workflow.contracts import check_source
        from workflow.worker import prepared_environment
        for method,identity in [('spectral','FQI-SRC-GR2-7.2.22'),('determinant','FQI-SRC-AP-11.2.4')]:
            if not args.audit_existing:
                proc=subprocess.run([sys.executable,str(HERE/f'prove_{method}.py'),'--identity',identity],capture_output=True,text=True,timeout=1030)
                assert proc.returncode==2,(identity,proc.stdout,proc.stderr)
            files=[p for p in (HERE/'generated'/method).glob('*/report.json') if json.loads(p.read_text()).get('identity')==identity]
            file=max(files,key=lambda p:p.stat().st_mtime);r=json.loads(file.read_text())
            assert r['status']=='unproved' and r['automatic_train_proofs']==0 and r['plan'],identity
            assert all(a['method']==method for a in r['plan'])
            check_source(r['source'])
            prepared_environment(json.loads((file.parent/'analysis'/method/'environment.json').read_text()))
            native=json.loads(Path(r['attempts'][-1]['result']).read_text())
            assert native['status']=='search_exhausted' and native['remaining_obligations'],identity
            result['native_unresolved'].append(dict(identity=identity,method=method,report=str(file),remaining_obligations=native['remaining_obligations']))
        result['methods_verified']=sorted(set(result['methods_verified'])|set(result['structural_modules']))
        assert len(result['methods_verified'])==12
        result['status']='passed'  
    except Exception as exc:result['error']=f'{type(exc).__name__}: {exc}'
    result['code_sha256']={str(file.relative_to(HERE)):hashlib.sha256(file.read_bytes()).hexdigest()
        for file in [HERE/'prove.py',*sorted(HERE.glob('prove_*.py')),HERE/'check.py',HERE/'test_workflow.py',HERE/'p1/run.py',*sorted((HERE/'workflow').glob('*.py')),*sorted((HERE/'product').rglob('*.py')),*sorted((HERE/'product/lean').glob('*.lean')),*sorted((HERE/'interpolation').rglob('*.py')),*sorted((HERE/'interpolation/lean').glob('*.lean')),*sorted((HERE/'noncommutative').rglob('*.py')),*sorted((HERE/'noncommutative/lean').glob('*.lean')),*sorted((HERE/'combinatorial').rglob('*.py')),*sorted((HERE/'combinatorial/lean').glob('*.lean')),*sorted((HERE/'difference_ring').rglob('*.py')),*sorted((HERE/'difference_ring/lean').glob('*.lean')),*sorted((HERE/'workflow').glob('*.lean')),*[p for m in ('kernel_transform','spectral','determinant','macmahon') for p in sorted((HERE/m).rglob('*')) if p.suffix in ('.py','.lean')]]}
    save(HERE/'generated/method_pipelines_validation.json',result)
    print(json.dumps({k:v for k,v in result.items() if k not in ('regressions','code_sha256')},ensure_ascii=False,indent=2))
    return 0 if result['status']=='passed' else 1
if __name__=='__main__':raise SystemExit(main())
