"""Focused original-statement and adversarial checks for parameter exits.

Requires a prepared P1 environment. Only the two explicitly selected Train
sources are read. Synthetic variants do not alter the benchmark.
"""
from pathlib import Path
import argparse,copy,json,os,re,sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from workflow.contracts import ROOT
from lean_pipeline import extract,verify_proof,HERE
from zeilberger import ZeilbergerBudget
import defined_relation as relation


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--environment',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--kind',choices=['closed','shift'])
    args=parser.parse_args();out=args.output.resolve();out.mkdir(parents=True,exist_ok=False)
    env=dict(os.environ,LEAN_PATH=json.loads(args.environment.read_text())['lean_path'])
    rows={r['id']:r for r in map(json.loads,(ROOT/'benchmark/splits/train.jsonl').read_text().splitlines())}
    results=[]
    for kind,identity in [('closed','FQI-ROGERS-SZEGO-SQRT'),('shift','FQI-SRC-FINE-20.64b')]:
        if args.kind and args.kind!=kind:continue
        source=(ROOT/'benchmark'/rows[identity]['lean_path']).read_text()
        w=out/kind;w.mkdir();raw=extract(source,w,env)
        p,m=relation.prepare(raw,identity,w,env)
        cert=relation.construct(p,ZeilbergerBudget(seconds=120,max_order=4))['construction']
        (w/'construction.json').write_text(json.dumps(cert,indent=2))
        for case in ['bad_certificate','bad_coefficients']+(['bad_closure'] if kind=='shift' else []):
            bad=copy.deepcopy(cert);base=bad.get('base_recurrence',bad)
            if case=='bad_certificate':base['certificate']='2*('+base['certificate']+')'
            elif case=='bad_coefficients':base['coefficients'][0]='1+('+base['coefficients'][0]+')'
            else:bad['witnesses'][0][2]='0'
            try:relation.emit(m,bad)
            except (ValueError,ArithmeticError) as e:results.append(dict(kind=kind,case=case,status='rejected',reason=str(e)))
            else:raise AssertionError((kind,case,'accepted'))
        cases=['renamed','wrong_target']+(['missing_lower_bound','scaled'] if kind=='shift' else ['reversed'])
        for case in cases:
            text=source
            if case=='renamed':text=re.sub(r'\b(u|q|n)\b',lambda v:{'u':'weightParam','q':'baseParam','n':'indexParam'}[v[0]],text)
            elif case=='wrong_target':
                text=text.replace('poch (-u) u n','poch u u n') if kind=='closed' else text.replace('1 - (q^n)','1 + (q^n)')
            elif case=='missing_lower_bound':text=text.replace(' (hn : 1 ≤ n)','')
            elif case=='reversed':text=text.replace('rogersSzego u (u^2) n = poch (-u) u n','poch (-u) u n = rogersSzego u (u^2) n')
            else:
                text=text.replace('(((rogersSzego','(3:K)*(((rogersSzego')
            assert text!=source,(kind,case,"synthetic source was unchanged")
            cw=w/case;cw.mkdir();raw=extract(text,cw,env)
            problem,model=relation.prepare(raw,'synthetic-'+case,cw,env)
            # Recompute closure when target observable changes; definition-only
            # certificate is identical, never a stored identity proof.
            certificate=relation.construct(problem,ZeilbergerBudget(seconds=120,max_order=4))['construction']
            proof,plan=relation.emit(model,certificate)
            v=verify_proof(text,proof,plan,cw,env,[(HERE/'lean/OreRules.lean').read_text()])
            (cw/'verification.json').write_text(json.dumps(v,indent=2))
            expect=case not in ('wrong_target','missing_lower_bound')
            assert (v['status']=='proved')==expect,(kind,case,v['status'])
            results.append(dict(kind=kind,case=case,status=v['status'],verification=str(cw/'verification.json')))
            print(kind,case,v['status'],flush=True)
        (out/'validation.json').write_text(json.dumps(results,indent=2))
    print('passed',len(results),flush=True)

if __name__=='__main__':main()
