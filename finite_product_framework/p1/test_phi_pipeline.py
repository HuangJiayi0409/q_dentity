"""Terminating phi bridge: renamed input, required domain, and certificate rejection."""
import json,os,re,tempfile
from pathlib import Path
from expressions import derive,X,q
from search import search
from lean_pipeline import HERE,ROOT,extract,frontend,synthesize

def main():
    report={'status':'failed','synthetic_tests_count_as_train_proofs':False,'checks':[]}
    try:
        run=json.loads((HERE/'generated/runs/FQI-SRC-GR2-1.Ex6iii/report.json').read_text())
        assert run['status']=='proved'
        source=(ROOT/run['source']['path']).read_text()
        env=os.environ.copy();env['LEAN_PATH']=str(Path(run['verification']['proof_file']).parent/'deps')
        renamed=re.sub(r'\b(a|q|n)\b',lambda m:{'a':'v','q':'u','n':'m'}[m.group()],source)
        with tempfile.TemporaryDirectory(prefix='p1-phi-') as directory:
            work=Path(directory)
            formula,model=frontend(extract(renamed,work,env),'synthetic-phi')
            shifts=derive(formula)
            construction=search(shifts['n_shift'],shifts['k_shift'],shifts['target_coefficient'],X,q)
            assert construction['status']=='constructed'
            for label,text,certificate,expected in [
                ('renamed_phi',renamed,construction,'proved'),
                ('missing_nonzero_parameter',renamed.replace(' (ha : v ≠ 0)',''),construction,'lean_failed'),
                ('tampered_certificate',renamed,dict(construction,certificate='2*('+construction['certificate']+')'),'lean_failed')]:
                _,model=frontend(extract(text,work,env),'synthetic-phi')
                result=synthesize(text,model,shifts,certificate,work,env)
                assert result['status']==expected,(label,result)
                report['checks'].append({'case':label,'status':expected,'lean':result['lean']})
        report['status']='passed'
    except Exception as exc:report['error']=f'{type(exc).__name__}: {exc}'
    (HERE/'generated/phi_tests.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='checks'},ensure_ascii=False))
    if report['status']!='passed':raise SystemExit(1)
if __name__=='__main__':main()
