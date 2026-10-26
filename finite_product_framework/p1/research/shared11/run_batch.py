#!/usr/bin/env python3
"""Retry the fixed eleven candidates; keep formal preprocessing distinct from proofs."""
import csv,hashlib,html,json,re,sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
HERE=Path(__file__).resolve().parent;P1=HERE.parents[1];sys.path.insert(0,str(P1))
from run import ROOT,prepare_batch,batch_environment,run,load_target
from lean_pipeline import assemble,proof_slot,lean,find_nodes

def read(p):return json.loads(p.read_text())
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    selection=HERE/'selection.json'
    if not selection.exists():
        old=read(P1/'research/remaining12/summary.json')
        ids=[r['id'] for r in old['records'] if not r['original_lean_proved']]
        assert len(ids)==11
        write(selection,{'identities':ids,'initial_complete_train_proofs':6})
    ids=read(selection)['identities'];notes=read(HERE/'obligations.json')
    if '--render-only' in sys.argv:
        rows=[read(HERE/identity/'result.json') for identity in ids]
        for r in rows:
            r['remaining_obligations']=notes[r['id']]['remaining']
            assert bool(r['remaining_obligations']) != r['original_lean_proved']
            write(HERE/r['id']/'result.json',r)
        render(rows)
        return
    prepared=prepare_batch(HERE/'shared')
    write(HERE/'dependencies.json',{k:prepared[k] for k in ('dependencies','artifacts')})
    env,_=batch_environment(prepared)
    support=HERE/'SupportValidation.lean'
    support.write_text((P1/'lean/SupportRules.lean').read_text()+'\n#print axioms FiniteQP1.sum_bilateral_range\n#print axioms FiniteQP1.gaussianInt_centered\n')
    result=lean(support,env)
    assert result['exit_code']==0 and 'sorryAx' not in result['output'],result
    write(HERE/'support_validation.json',dict(status='passed',lean=result,source_sha256=digest(P1/'lean/SupportRules.lean'),proof_sha256=digest(support),original_train_proofs_claimed=0))
    def task(identity):
        work=HERE/identity;work.mkdir(exist_ok=True)
        native=run(identity,prepared=prepared,output_root=HERE/'native')
        write(work/'native.json',native)
        source=load_target(identity)
        proved=native['status']=='proved'
        if proved:
            v=native['verification'];assert not native['remaining_obligations']
            assert v['lean']['exit_code']==0 and 'sorryAx' not in v['lean']['output']
            assert digest(Path(v['proof_file']))==v['proof_sha256']
        row=dict(id=identity,source=source,native_status=native['status'],original_lean_proved=proved,
                 remaining_obligations=[] if proved else notes[identity]['remaining'],
                 native_report=identity+'/native.json')
        raw=read(HERE/'native'/identity/'lean_expression.json')
        if not proved:
            from normalize import normalize
            env,_=batch_environment(prepared)
            preprocessing=normalize((ROOT/source['path']).read_text(),raw,
                read(HERE/'native'/identity/'lean_hypotheses.json'),work,env)
            row['verified_preprocessing_steps']=preprocessing['steps']
            if find_nodes(raw,'Finset.Icc'):
                row['support_normalization']='original goal reindexed by Lean; not a full proof'
        write(work/'result.json',row);print(identity,row['native_status'],flush=True);return row
    with ThreadPoolExecutor(max_workers=3) as pool:rows=list(pool.map(task,ids))
    render(rows)

def render(rows):
    new=sum(r['original_lean_proved'] for r in rows)
    summary=dict(status='batch_completed',selected=11,new_original_proofs=new,remaining_original_proofs=11-new,
        initial_complete_train_proofs=6,complete_train_proofs=6+new,
        support_normalizations=sum('support_normalization' in r for r in rows),
        lean_preprocessed_unclosed_goals=sum('verified_preprocessing_steps' in r for r in rows),
        code_sha256={name:digest(P1/name) for name in ['run.py','lean_pipeline.py','expressions.py','search.py','qgosper.py','lean/DomainRules.lean','lean/PhiRules.lean','lean/GaussianRules.lean','lean/SupportRules.lean','research/shared11/normalize.py']},records=rows)
    write(HERE/'summary.json',summary)
    with (HERE/'table.csv').open('w') as f:
        w=csv.writer(f);w.writerow(['identity','original Lean','support normalization','remaining obligations'])
        for r in rows:w.writerow([r['id'],r['native_status'],r.get('support_normalization',''),'；'.join(r['remaining_obligations'])])
    page='''<!doctype html><html lang="zh"><meta charset="utf-8"><title>P1 公共能力扩展：11条验收</title>
<style>body{font:16px sans-serif;margin:32px;line-height:1.6}table{border-collapse:collapse}td,th{border:1px solid #bbb;padding:10px;vertical-align:top;text-align:left}</style><h1>P1 公共能力扩展：11条验收</h1>'''
    page+=f'<p>本批11条全部重试，新增完整原题证明{new}条，累计{6+new}条；仍有{11-new}条未闭合。其余9条已执行经过Lean检查的表示预处理，其中3条双边求和完成重编号；这些不计完整证明。</p><table><tr><th>公式</th><th>原题证明</th><th>剩余义务</th><th>证据</th></tr>'
    for r in rows:
        page+='<tr><td>'+html.escape(r['id'])+'</td><td>'+('完整通过' if r['original_lean_proved'] else '未完成')+'</td><td>'+html.escape('；'.join(r['remaining_obligations']) or '无')+'</td><td><a href="'+r['native_report']+'">原生入口报告</a></td></tr>'
    (HERE/'index.html').write_text(page+'</table></html>')
    print(json.dumps({k:v for k,v in summary.items() if k not in ('records','code_sha256')},ensure_ascii=False))
if __name__=='__main__':main()
