"""Convolution regression, including rejection of a false second conjunct."""
import copy,json,os,re,tempfile
from pathlib import Path
from expressions import derive,X,q
from search import search,Budget
from run import construct_in_process
from lean_pipeline import HERE,ROOT,extract,frontend,synthesize,synthesize_conjunction

def main():
    report={'status':'failed','synthetic_tests_count_as_train_proofs':False,'checks':[]}
    try:
        identity='FQI-SRC-AP-13.E3'
        run=json.loads((HERE/'generated/runs'/identity/'report.json').read_text())
        assert run['status']=='proved'
        source=(ROOT/run['source']['path']).read_text()
        env=os.environ.copy();env['LEAN_PATH']=str(Path(run['verification']['proof_file']).parent/'deps')
        source=source.replace('(∏ i ∈ Finset.range n, (X-Z*q^i))',
                              '((2:K) * (∏ i ∈ Finset.range n, (X-Z*q^i)))')
        source=source.replace('gaussian q n k *','(2:K) * gaussian q n k *')
        names={'X':'a','Y':'b','Z':'c','q':'u','n':'m','k':'r','i':'s','j':'t','h':'v'}
        source=re.sub(r'\b(X|Y|Z|q|n|k|i|j|h)\b',lambda m:names[m.group()],source)
        with tempfile.TemporaryDirectory(prefix='p1-convolution-') as directory:
            work=Path(directory)
            formula,model=frontend(extract(source,work,env),'synthetic-renamed-scaled')
            shifts=derive(formula)
            construction=search(shifts['n_shift'],shifts['k_shift'],shifts['target_coefficient'],X,q)
            assert construction['status']=='constructed'
            verified=synthesize(source,model,shifts,construction,work,env)
            assert verified['status']=='proved',verified
            assert 'P1Gap' in verified['plan']['multiplier']
            report['checks'].append({'case':'renamed_scaled_raw_products','status':'passed','plan':verified['plan']})
            altered=dict(construction,certificate='2*('+construction['certificate']+')')
            rejected=synthesize(source,model,shifts,altered,work,env)
            assert rejected['status']=='lean_failed',rejected
            report['checks'].append({'case':'tampered_gap_certificate','status':'rejected_by_Lean'})

        identity='FQI-SRC-GR2-1.Ex3i'
        run=json.loads((HERE/'generated/runs'/identity/'report.json').read_text())
        assert run['status']=='proved'
        source=(ROOT/run['source']['path']).read_text()
        source=re.sub(r'\b(a|b|q|n|k)\b',lambda m:{'a':'x','b':'y','q':'u','n':'m','k':'r'}[m.group()],source)
        with tempfile.TemporaryDirectory(prefix='p1-conjunction-') as directory:
            work=Path(directory)
            formula,model=frontend(extract(source,work,env),'synthetic-conjunction')
            result=construct_in_process(formula,Budget(),'target_first_order')
            assert result['construction']['status']=='constructed' and len(result['conjunct_results'])==2
            verified=synthesize_conjunction(source,model,result,work,env)
            assert verified['status']=='proved',verified
            report['checks'].append({'case':'renamed_both_conjuncts','status':'passed','plan':verified['plan']})
            altered=copy.deepcopy(result)
            second=altered['conjunct_results'][1]['construction']
            second['certificate']='2*('+second['certificate']+')'
            rejected=synthesize_conjunction(source,model,altered,work,env)
            assert rejected['status']=='lean_failed',rejected
            report['checks'].append({'case':'only_second_certificate_tampered','status':'rejected_by_Lean'})
            before,after=source.rsplit('poch (x*y) u m',1)
            wrong=before+'(poch (x*y) u m + 1)'+after
            rejected=synthesize_conjunction(wrong,model,result,work,env)
            assert rejected['status']=='lean_failed',rejected
            report['checks'].append({'case':'only_second_target_changed','status':'rejected_by_Lean'})
        report['status']='passed'
    except Exception as exc:
        report['error']=f'{type(exc).__name__}: {exc}'
    (HERE/'generated/convolution_tests.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='checks'},ensure_ascii=False,indent=2))
    if report['status']!='passed':raise SystemExit(1)

if __name__=='__main__':main()
