"""Validate and render bounded symbolic experiments, separate from Lean coverage."""
import collections
import hashlib
import html
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]


def main():
    finite=json.loads((HERE/'finite_results.json').read_text())
    assert finite['status']=='passed'
    counts=dict(collections.Counter(x['id'] for x in finite['results']))
    assert counts=={'FQI-SRC-GR2-7.6.8':4,'FQI-SRC-GR2-1.Ex33':5,'FQI-SRC-GR2-9.Ex5ii':21}
    for row in json.loads((HERE/'inputs.json').read_text()):
        assert hashlib.sha256((ROOT/row['lean_path']).read_bytes()).hexdigest()==row['lean_sha256']
    log=(HERE/'qfps_probe.log').read_text()
    assert 'P2_QFPS_LOADED' in log and 'P2_QFPS_FINISHED' in log
    assert 'SANITY_RE ' in log and ' = 0' in log
    assert 'GF_ERROR ' in log and 'AW_RAW_ERROR ' in log
    assert 'GENERIC_ERROR [qshift, "improper op or subscript selector"]' in log
    files=['finite_trials.py','qfps_probe.mpl','finite_results.json','qfps_probe.log',
           'inputs.json','vendor/qFPS.mpl','build_report.py']
    summary={'date':'2026-10-13','status':'bounded_trials_completed',
       'new_lean_proofs':0,'new_general_parameter_proofs':0,'fixed_degree_checks':counts,
       'negative_controls':'Adding 1 to each tested target is rejected; no Float allowed',
       'tool_status':'Maple 2024.2 loads original qFPS; built-in LittleqJacobi symbolic recurrence computed',
       'qfps_gf_status':'Raw qHolonomicRE call failed; internal qphi path triggers qshift selector error',
       'qfps_aw_status':'Raw qHolonomicRE call failed; specialized AW divided-difference preprocessing not implemented',
       'decision':'Prioritize generic basis inversion; retain operator route as integration work',
       'scope_limitations':finite['limitations'],
       'vendor':{'url':'https://hypergeometric-summation.org/qFPS.mpl','original_unmodified':True,
                 'copyright':'Original author copyright notices retained; not a Python port'},
       'sha256':{f:hashlib.sha256((HERE/f).read_bytes()).hexdigest() for f in files}}
    (HERE/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    e=html.escape
    page='''<!doctype html><html lang="zh"><meta charset="utf-8"><title>P2三路线实际试验</title>
<style>body{font:16px/1.7 system-ui;max-width:1100px;margin:40px auto;padding:20px}td,th{border:1px solid #ddd;padding:10px}table{border-collapse:collapse}pre{white-space:pre-wrap;background:#f5f5f5;padding:16px}</style>
<h1>P2三路线实际试验 · 2026-10-13</h1>
<p><b>本轮新增原train完整证明0条，新增泛参数证明0条。</b>固定次数/部分参数特化实验用于选择研发路线，不计入Lean覆盖。</p>
<table><tr><th>原train公式</th><th>实际试验与结果</th><th>尚缺能力</th></tr>
<tr><td>GR2-7.6.8</td><td>n=0..3，保留alpha及Laurent变量z；从两组AW定义做三角消元，独立计算连接系数，与目标系数逐个精确相等。</td><td>这采用三角消元，不是已实现论文的AW分差算子算法。符号n、全参数域、归一化与Lean桥接仍未完成。</td></tr>
<tr><td>GR2-1.Ex33</td><td>n=0..4，保留一侧参数c及变量t；从小q-Jacobi定义计算基底反演，连接系数与原目标一致。</td><td>固定维数成功不证明泛n。下一步需通用反演系数或系数核及完整原域证明。</td></tr>
<tr><td>GR2-9.Ex5ii</td><td>N=0..5、全部0≤x≤N共21组，保留t，有限定义展开后系数精确一致。qFPS实际原输入构造失败。</td><td>qFPS的qshift内部选择器报错；有限终止定义与工具qPhi的对应、函数方程、初值和Lean输出仍未接通。</td></tr></table>
<p>所有试验均为精确代数而非浮点抽样；仍固定了q=2/3及若干参数。符号参数结果是有理函数域上的等式，未处理原Lean允许的全部退化参数。三条输入来自显式转写，未做Lean Expr自动提取。每个比较还验证了目标加1后不成立。</p>
<h2>工具实际状态</h2><p>作者qFPS源码已下载，原版权标注保留，未修改。Maple 2024.2成功加载，并计算了小q-Jacobi的符号递推。直接处理生成函数与AW原始表达式失败；内部诊断定位到qshift选择器错误，不将该错误解释为数学算法不适用。</p>
<p>建议先推进基底反演，再扩展符号n的通用核；AW可先复用此入口，专门算子算法另需实现。当前P2运行分支与P1均未改动。</p>
<p><a href="finite_trials.py">有限次数试验代码</a> · <a href="finite_results.json">30组精确结果</a> · <a href="qfps_probe.mpl">Maple试验脚本</a> · <a href="inputs.json">原声明快照</a> · <a href="summary.json">验证与文件哈希</a></p>
<h2>Maple原始日志</h2><pre>'''+e(log)+'''</pre></html>'''
    (HERE/'index.html').write_text(page)
    print(json.dumps({'status':summary['status'],'checks':counts,'new_lean_proofs':0},ensure_ascii=False))


if __name__=='__main__':
    main()
