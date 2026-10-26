#!/usr/bin/env python3
"""Verify current input-driven contract, shared kernel and train provenance."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def main():
    report = {'schema_version': 2, 'status': 'failed', 'automatic_train_proofs': 0,
              'complete_train_proofs': 0, 'historical_manual_lean_proofs': 1,
              'test_files_read': 0, 'preset_proof_fallback': False,
              'active_algorithms': ['q-WZ with q-Gosper antidifference', 'direct q-Gosper with endpoint evaluation', 'general q-Zeilberger joint recurrence/certificate search', 'bibasic Gosper with original-domain endpoint verification', 'q-Ore polynomial closure and elimination', 'bounded multivariate q creative telescoping with native triangular 2D Lean exit'],
              'experimental_algorithms': ['higher-dimensional native multisum Lean exit'],
              'symbolic_coefficient_domain': 'Q(q, independent parameters); bibasic Q(p,q,independent parameters)'}
    try:
        train = {r['id']: r for r in map(json.loads,
                 (ROOT/'benchmark/splits/train.jsonl').read_text().splitlines())}
        for case in json.loads((HERE/'cases.json').read_text())['cases']:
            row = train[case['id']]
            assert row['family_id'] == 'A'
            for pathkey, hashkey in [('lean_path', 'lean_sha256'), ('md_path', 'md_sha256')]:
                path = ROOT/'benchmark'/row[pathkey]
                assert hashlib.sha256(path.read_bytes()).hexdigest() == row[hashkey]
        test = subprocess.run([sys.executable, str(HERE/'test_pipeline.py')],
                              capture_output=True, text=True, timeout=120)
        report['tests'] = {'exit_code': test.returncode, 'output': test.stdout+test.stderr}
        assert test.returncode == 0
        cases = [c for c in json.loads((HERE/'cases.json').read_text())['cases']
                 if c['status'] == 'proved']
        report['native_runs'] = []
        for case in cases:
            native = subprocess.run([sys.executable, str(HERE/'run.py'), '--identity', case['id'], *case.get('run_args',[])],
                                    capture_output=True, text=True, timeout=case.get('validation_timeout',600))
            report['native_runs'].append({'identity':case['id'],'exit_code':native.returncode,
                                          'output':native.stdout+native.stderr})
            assert native.returncode == 0, native.stdout+native.stderr
            result = json.loads((HERE/'generated/runs'/case['id']/'report.json').read_text())
            assert result['status'] == 'proved' and not result['remaining_obligations']
            verification = result['verification']
            assert hashlib.sha256(Path(verification['proof_file']).read_bytes()).hexdigest() == verification['proof_sha256']
            assert verification['lean']['exit_code'] == 0 and 'sorryAx' not in verification['lean']['output']
            assert result['source']['sha256'] == case['lean_sha256']
        integration = subprocess.run([sys.executable, str(HERE/'test_lean_pipeline.py')],
                                     capture_output=True, text=True, timeout=600)
        report['integration_tests'] = {'exit_code': integration.returncode,
                                       'output': integration.stdout+integration.stderr}
        assert integration.returncode == 0
        direct = subprocess.run([sys.executable, str(HERE/'test_direct.py')],
                                capture_output=True,text=True,timeout=600)
        report['direct_tests'] = {'exit_code':direct.returncode,'output':direct.stdout+direct.stderr}
        assert direct.returncode == 0, direct.stdout+direct.stderr
        product = subprocess.run([sys.executable, str(HERE/'test_product_pipeline.py')],
                                 capture_output=True,text=True,timeout=600)
        report['product_tests'] = {'exit_code':product.returncode,'output':product.stdout+product.stderr}
        assert product.returncode == 0, product.stdout+product.stderr
        convolution = subprocess.run([sys.executable, str(HERE/'test_convolution_pipeline.py')],
                                     capture_output=True,text=True,timeout=600)
        report['convolution_tests'] = {'exit_code':convolution.returncode,
                                      'output':convolution.stdout+convolution.stderr}
        assert convolution.returncode == 0, convolution.stdout+convolution.stderr
        phi = subprocess.run([sys.executable, str(HERE/'test_phi_pipeline.py')],
                             capture_output=True,text=True,timeout=600)
        report['phi_tests'] = {'exit_code':phi.returncode,'output':phi.stdout+phi.stderr}
        assert phi.returncode == 0, phi.stdout+phi.stderr
        domain = subprocess.run([sys.executable, str(HERE/'test_domain_pipeline.py')],
                                capture_output=True,text=True,timeout=600)
        report['domain_tests'] = {'exit_code':domain.returncode,'output':domain.stdout+domain.stderr}
        assert domain.returncode == 0, domain.stdout+domain.stderr
        zeilberger = subprocess.run([sys.executable, str(HERE/'test_zeilberger.py')],
                                    capture_output=True,text=True,timeout=600)
        report['zeilberger_tests'] = {'exit_code':zeilberger.returncode,
                                      'output':zeilberger.stdout+zeilberger.stderr}
        assert zeilberger.returncode == 0, zeilberger.stdout+zeilberger.stderr
        bibasic = subprocess.run([sys.executable, str(HERE/'test_bibasic.py')],
                                 capture_output=True,text=True,timeout=600)
        report['bibasic_tests'] = {'exit_code':bibasic.returncode,'output':bibasic.stdout+bibasic.stderr}
        assert bibasic.returncode == 0, bibasic.stdout+bibasic.stderr
        ore = subprocess.run([sys.executable, str(HERE/'test_ore.py')],
                             capture_output=True,text=True,timeout=600)
        report['ore_tests'] = {'exit_code':ore.returncode,'output':ore.stdout+ore.stderr}
        assert ore.returncode == 0, ore.stdout+ore.stderr
        multisum = subprocess.run([sys.executable, str(HERE/'test_multisum.py')],
                                  capture_output=True,text=True,timeout=600)
        report['multisum_tests'] = {'exit_code':multisum.returncode,'output':multisum.stdout+multisum.stderr}
        assert multisum.returncode == 0, multisum.stdout+multisum.stderr
        if any(c.get('role')=='multisum_triangular_certificate' for c in cases):
            native_multisum = subprocess.run([sys.executable,str(HERE/'test_multisum_native.py')],
                                            capture_output=True,text=True,timeout=2000)
            report['multisum_native_tests']={'exit_code':native_multisum.returncode,
                                             'output':native_multisum.stdout+native_multisum.stderr}
            assert native_multisum.returncode==0,native_multisum.stdout+native_multisum.stderr
        report['automatic_train_proofs'] = report['complete_train_proofs'] = len(cases)
        report['synthetic_tests_count_as_train_proofs'] = False
        for name in ('run.py', 'search.py', 'expressions.py', 'qgosper.py', 'lean_pipeline.py', 'direct.py', 'zeilberger.py', 'zeilberger_pipeline.py', 'bibasic.py', 'bibasic_pipeline.py', 'lean/BibasicRules.lean', 'ore.py', 'ore_pipeline.py', 'lean/OreRules.lean', 'multisum.py', 'multisum_pipeline.py', 'multisum_domains.py', 'exact_linear.py', 'multisum_lean.py', 'lean/MultisumRules.lean', 'lean/MultisumProductRules.lean',
                                              'lean/Extract.lean', 'lean/GaussianRules.lean', 'lean/ProductRules.lean', 'lean/PhiRules.lean', 'lean/DomainRules.lean', 'lean/Shared.lean'):
            source = (HERE/name).read_text()
            for forbidden in ('SUPPORTED_ID', 'binomial_search', 'binomialFlux',
                              'Binomial.lean', 'FiniteQBinomial.lean', 'PROOF ='):
                assert forbidden not in source, (name, forbidden)
        assert 'antidifference(' in (HERE/'search.py').read_text()
        assert 'shift_radius' not in (HERE/'qgosper.py').read_text()
        assert 'max_degree' not in (HERE/'qgosper.py').read_text()
        source = json.loads((HERE/'references/source.json').read_text())
        assert hashlib.sha256((HERE/'references/qsum.red').read_bytes()).hexdigest() == source['sha256']
        report['code_sha256'] = {name: hashlib.sha256((HERE/name).read_bytes()).hexdigest()
                                 for name in ('run.py', 'search.py', 'expressions.py', 'qgosper.py', 'lean_pipeline.py', 'direct.py', 'zeilberger.py', 'zeilberger_pipeline.py', 'bibasic.py', 'bibasic_pipeline.py', 'lean/BibasicRules.lean', 'ore.py', 'ore_pipeline.py', 'lean/OreRules.lean', 'multisum.py', 'multisum_pipeline.py', 'multisum_domains.py', 'exact_linear.py', 'multisum_lean.py', 'lean/MultisumRules.lean', 'lean/MultisumProductRules.lean',
                                              'lean/Extract.lean', 'lean/GaussianRules.lean', 'lean/ProductRules.lean', 'lean/PhiRules.lean', 'lean/DomainRules.lean', 'lean/Shared.lean')}
        assert not (HERE/'lean/Binomial.lean').exists()
        assert not (HERE/'generated/FiniteQBinomial.lean').exists()
        report['status'] = 'passed'
    except Exception as exc:
        report['error'] = f'{type(exc).__name__}: {exc}'
    (HERE/'validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('tests','native_runs','integration_tests','direct_tests','product_tests','convolution_tests')}, ensure_ascii=False, indent=2))
    return 0 if report['status'] == 'passed' else 1


if __name__ == '__main__':
    sys.exit(main())
