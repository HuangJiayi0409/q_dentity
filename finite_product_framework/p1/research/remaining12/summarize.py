#!/usr/bin/env python3
"""Auditable batch accounting: local algebra is never counted as an original proof."""
import csv,hashlib,html,json,re,sys
from pathlib import Path
import sympy as s
HERE=Path(__file__).resolve().parent;P1=HERE.parents[1];ROOT=P1.parents[1]
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def main():
    selection=read(HERE/'selection.json');notes=read(HERE/'obligations.json');records=[]
    for identity in selection['identities']:
        work=HERE/identity;symbolic=read(work/'native_symbolic.json');local=read(work/'local_validation.json')
        typed=read(work/'typecheck.json');native=read(work/'native.json')
        assert typed['well_typed_original_goal'] and symbolic['status']=='constructed'
        assert local['status']=='passed' and local['native_report_sha256']==digest(work/'native_symbolic.json')
        assert local['proof_sha256']==digest(Path(local['source_file']))
        assert 'sorryAx' not in local['lean']['output'] and local['lean']['exit_code']==0
        assert symbolic['source']['sha256']==digest(ROOT/symbolic['source']['path'])
        assert symbolic['translator_sha256']==digest(HERE/'native_symbolic.py')
        for key,file in [('goal_export_sha256','lean_expression.json'),('hypotheses_export_sha256','lean_hypotheses.json')]:
            assert symbolic[key]==digest(HERE/'native'/identity/file),(identity,key)
        # Independently recompute the rational identity; no stored zero is trusted.
        names=set()
        for value in symbolic['shifts'].values():names.update(re.findall(r'[A-Za-z_][A-Za-z_0-9]*',value))
        env={name:s.Symbol(name) for name in names};q,X=env['q'],env['X']
        shifts={name:s.sympify(value,locals=env) for name,value in symbolic['shifts'].items()}
        direct=symbolic['case']['route']=='direct'
        R=s.sympify(symbolic['construction']['antidifference_ratio' if direct else 'certificate'],locals=env)
        residual=shifts['V']*R.subs(X,q*X)-R-(1 if direct else shifts['U']-shifts['c'])
        assert s.cancel(residual)==0
        proved=native['status']=='proved'
        if proved:
            assert not native['remaining_obligations']
            v=native['verification'];assert v['lean']['exit_code']==0 and 'sorryAx' not in v['lean']['output']
            assert v['proof_sha256']==digest(Path(v['proof_file']))
            assert not notes[identity]['remaining']
        else:assert notes[identity]['remaining']
        records.append(dict(id=identity,source=symbolic['source'],typechecked=True,
            actual_lean_expr_extracted=True,certificate_constructed=True,local_lean_verified=True,
            independent_rational_residual_verified=True,original_lean_proved=proved,
            native_status=native['status'],route=symbolic['case']['route'],
            group=notes[identity]['group'],remaining_obligations=notes[identity]['remaining'],
            certificate_denominator=str(s.factor(s.denom(s.cancel(R)))),
            report_links={'native':identity+'/native.json',
                          'symbolic':identity+'/native_symbolic.json','local':identity+'/local_validation.json'}))
    new=sum(r['original_lean_proved'] for r in records)
    result=dict(scope='fixed twelve remaining train A candidates; other candidates not reclassified',
        initial_complete_train_proofs=selection['initial_complete_train_proofs'],
        selected=12,actual_expr_symbolic_success=12,local_lean_verified=12,
        new_original_proofs=new,remaining_original_proofs=12-new,
        complete_train_proofs=selection['initial_complete_train_proofs']+new,
        limitation='Rational field relations do not establish original-domain representations, denominator conditions, boundaries or initial values.',
        records=records)
    (HERE/'summary.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    with (HERE/'table.csv').open('w') as f:
        writer=csv.writer(f);writer.writerow(['identity','route','local Lean','original Lean','remaining obligations'])
        for r in records:writer.writerow([r['id'],r['route'],'passed',r['native_status'],'；'.join(r['remaining_obligations'])])
    rows=[]
    for r in records:
        links=' / '.join(f'<a href="{html.escape(path)}">{name}</a>' for name,path in r['report_links'].items())
        rows.append('<tr>'+''.join('<td>'+v+'</td>' for v in [html.escape(r['id']),r['route'],'通过','完整通过' if r['original_lean_proved'] else '未完成',html.escape('；'.join(r['remaining_obligations']) or '无'),links])+'</tr>')
    page='''<!doctype html><html lang="zh"><meta charset="utf-8"><title>P1 剩余12条推进结果</title>
<style>body{font:16px sans-serif;margin:32px;line-height:1.6}table{border-collapse:collapse}td,th{border:1px solid #bbb;padding:10px;text-align:left;vertical-align:top}th{background:#eee}</style>
<h1>P1 剩余12条推进结果</h1>'''
    page+=f'<p>12条均从原Lean表达式导出并动态构造证书；12条局部代数关系通过Lean。新增完整原题证明{new}条，累计{result["complete_train_proofs"]}条；本批仍有{12-new}条未完成。</p>'
    page+='<p>局部证书通过不等于原恒等式证明通过。下表缺口属于当前P1实现的剩余义务，不能据此判定这些公式不适用于P1。证书分母没有自动成为原定理的新假设。</p>'
    page+='<table><tr><th>原train公式</th><th>分支</th><th>局部Lean</th><th>原式Lean</th><th>具体剩余义务</th><th>证据</th></tr>'+''.join(rows)+'</table></html>'
    (HERE/'index.html').write_text(page)
    print(json.dumps({k:v for k,v in result.items() if k!='records'},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
