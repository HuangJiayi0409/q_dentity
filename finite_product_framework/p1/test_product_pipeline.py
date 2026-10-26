"""Finite-product input regression: generalization and rejection by Lean."""
import json,os,re,tempfile
from pathlib import Path
from expressions import derive,X,q
from search import search
from lean_pipeline import HERE,ROOT,extract,frontend,synthesize

def main():
    report={'status':'failed','synthetic_tests_count_as_train_proofs':False,'checks':[]}
    try:
        run=json.loads((HERE/'generated/runs/FQI-SRC-KAC-CHEUNG-4.4/report.json').read_text())
        assert run['status']=='proved'
        source=(ROOT/run['source']['path']).read_text()
        env=os.environ.copy()
        env['LEAN_PATH']=str(Path(run['verification']['proof_file']).parent/'deps')
        # The original assumptions are unnecessary: test every q, including zero and one.
        unrestricted=source.replace(' (hq : q ≠ 0) (hq1 : q ≠ 1)\n','')
        squared=unrestricted.replace('(x^n)', '((x^2)^n)').replace('kacPowerNat x 1 q j','kacPowerNat (x^2) 1 q j')
        squared=re.sub(r'\b(q|x|n|j)\b',lambda m:{'q':'u','x':'v','n':'m','j':'r'}[m.group()],squared)
        for label,text in [('unrestricted_q',unrestricted),('renamed_squared_parameter',squared)]:
            with tempfile.TemporaryDirectory(prefix='p1-product-') as directory:
                work=Path(directory)
                formula,model=frontend(extract(text,work,env),'synthetic-product')
                shifts=derive(formula)
                construction=search(shifts['n_shift'],shifts['k_shift'],shifts['target_coefficient'],X,q)
                assert construction['status']=='constructed'
                result=synthesize(text,model,shifts,construction,work,env)
                assert result['status']=='proved',result
                report['checks'].append({'case':label,'status':'passed','plan':result['plan'],'axiom_output':result['lean']['output']})
                if label=='unrestricted_q':
                    bad=dict(construction,certificate='2*('+construction['certificate']+')')
                    rejected=synthesize(text,model,shifts,bad,work,env)
                    assert rejected['status']=='lean_failed',rejected
                    report['checks'].append({'case':'tampered_certificate','status':'rejected_by_Lean'})
                    wrong=text.replace('(x^n)', '(x^n+1)')
                    _,wrong_model=frontend(extract(wrong,work,env),'synthetic-wrong-target')
                    rejected=synthesize(wrong,wrong_model,shifts,construction,work,env)
                    assert rejected['status']=='lean_failed',rejected
                    report['checks'].append({'case':'wrong_target_initial_value','status':'rejected_by_Lean'})
        report['status']='passed'
    except Exception as exc:
        report['error']=f'{type(exc).__name__}: {exc}'
    (HERE/'generated/product_tests.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False,indent=2))
    if report['status']!='passed':raise SystemExit(1)

if __name__=='__main__':main()
