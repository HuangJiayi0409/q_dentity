"""Product completion checks against selected Train sources and false variants.
Uses a prepared product environment; tests never edit benchmark inputs.
"""
from pathlib import Path
import argparse,copy,json,os,re,sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from product import pipeline as p
from workflow.contracts import ROOT,save,sha

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--environment',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
    out=a.output.resolve();out.mkdir(parents=True,exist_ok=False)
    env=dict(os.environ,LEAN_PATH=json.loads(a.environment.read_text())['lean_path'])
    rows={r['id']:r for r in map(json.loads,(ROOT/'benchmark/splits/train.jsonl').read_text().splitlines())}
    checks=[]
    for kind,identity in [('head','FQI-SRC-FINE-2.1'),('roots','FQI-POCHHAMMER-ROOTS')]:
        source=(ROOT/'benchmark'/rows[identity]['lean_path']).read_text()
        cases=['renamed','wrong_factor','missing_condition']
        if kind=='roots':cases+=['scaled_parameter','weaker_root_condition']
        for case in cases:
            text=source
            if case=='renamed':text=re.sub(r'\b(a|q|w|m|n)\b',lambda x:{'a':'alpha','q':'baseParam','w':'rootParam','m':'orderParam','n':'lengthParam'}[x[0]],text)
            elif case=='wrong_factor':
                text=text.replace('(1 - (a * q))','(1 + (a * q))') if kind=='head' else text.replace('poch (a^m)','poch (a^(m+1))')
            elif case=='missing_condition':
                text=text.replace(' (hn : 1 ≤ n)','') if kind=='head' else text.replace(' (hm : 0 < m)','')
            elif case=='scaled_parameter':text=text.replace('poch (a^m)','poch ((3*a)^m)').replace('poch (a*w^j)','poch ((3*a)*w^j)')
            else:text=text.replace('(hw : IsPrimitiveRoot w m)','(hw : w^m = 1)')
            assert text!=source,(kind,case,'source mutation did not match')
            w=out/(kind+'_'+case);w.mkdir()
            raw=p.extract(text,w,env);plans=p.plans(raw)
            successes=[]
            for i,plan in enumerate(plans):
                f=w/f'Candidate{i}.lean';f.write_text(p.slot(text,p.script(plan)))
                v=p.lean(f,env);save(w/f'candidate{i}.json',dict(plan=plan,lean=v))
                if not v['exit_code'] and 'sorryAx' not in v['output']:
                    successes.append(i);break
            expected=case in ('renamed','scaled_parameter')
            assert bool(successes)==expected,(kind,case,successes)
            checks.append(dict(kind=kind,case=case,status='proved' if successes else 'rejected',directory=str(w)))
            print(kind,case,checks[-1]['status'],flush=True)
        # An edited construction plan is rejected before Lean execution.
        w=out/(kind+'_tampered_plan');w.mkdir()
        raw=p.extract(source,w,env);data=dict(plans=p.plans(raw),expression=raw,
            source_text_sha256=__import__('hashlib').sha256(source.encode()).hexdigest(),dependencies=[])
        data['plans'][0]['rules']=['not_a_rule']
        try:p.prove_source(source,{},w,env,data,dict(symbolic_seconds=10))
        except ValueError as e:assert 'analysis plan changed' in str(e)
        else:raise AssertionError('tampered plan accepted')
        checks.append(dict(kind=kind,case='tampered_plan',status='rejected'))
        save(out/'validation.json',checks)
    print('passed',len(checks),flush=True)

if __name__=='__main__':main()
