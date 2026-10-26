#!/usr/bin/env python3
"""Build a mathematical trial shortlist; never classify by frontend success/failure.
Judgments below are review annotations, not dispatch rules for the proof pipeline.
"""
import csv
from collections import Counter
import hashlib
import html
import io
import json
from pathlib import Path
import sys
P1=Path(__file__).resolve().parents[2]
ROOT=P1.parents[1]
HERE=Path(__file__).resolve().parent

# Each annotation follows reading the original statement and the shared definitions.
REVIEW={}
def add(id,category,route,reason,precondition,action,alternative=''):
    assert id not in REVIEW
    REVIEW[id]=dict(category=category,proposed_route=route,mathematical_reason=reason,
                    required_check_or_preprocessing=precondition,next_action=action,
                    alternative_method=alternative)

V='already_verified';R='prioritize_symbolic_trial';C='conditional_candidate';D='defer_from_current_routes'
add('FQI-FINITE-Q-BINOMIAL',V,'target_first_order','Gaussian核、几何权重和三角指数构成单基超几何项，乘积目标有相邻关系。','原q=0及单位根域仍保留。','保留作无分母多项式域回归。')
add('FQI-SRC-AP-3.3.9',V,'direct_q_gosper','求和项与上限n无关，Gaussian上指标随k移动，原差分可由q-Gosper得到。','真实上下端点而非自然边界假设。','保留作直接原差分回归。')
add('FQI-CHU-VANDERMONDE-Q',R,'target_first_order','2φ1中q^(-n)起点按q移动；F的n、k比与乘积商目标的相邻比可有理化。','phiDefined只约束到当前n；向前归纳需从终点假设向下传递，不能假设n+1处分母非零。','先试目标引导差分的q-Gosper，再制定分母传递证明。')
add('FQI-CHU-VANDERMONDE-BALANCED',R,'target_first_order','同为2φ1，但自变量cq^n/a随n移动；额外移位贡献可写成q^k。','独立计算此式项比；不能沿用另一Chu式的证书。','以本式F和T重新派生U、V、c并搜索。')
add('FQI-TERMINATING-6PHI5',R,'target_first_order','wellPoised展开为单和；良配因子1-aq^(2k)在q^k中有理，右端是有限乘积商。','原定义允许a=1的可去延拓，必须使用wellPoisedNumerator并单列k=0。','先在一般形式域试证书，再核对a=1和k=0；不得给原题增加a≠1。')
add('FQI-SRC-GR2-1.Ex3i',R,'target_first_order','两个子目标各是Gaussian×k与n-k长度Pochhammer；两者分别具有有理项比和共同乘积目标。','Lean是合取；一次子和成功不能算整题通过。','两个子和分别试目标引导差分，或证明合法重编号后复用。','有限卷积也是候选。')
add('FQI-SRC-GR2-1.Ex5',R,'target_first_order','(cq^k;q)_m的k比由两端因子给出；固定m、递推n时全项仍是单基有理移位结构。','把和外前因子乘入F，禁止通过除去可能为零的前因子改写原题。','固定m，吸收和外因子后从实际闭式派生c并试q-Gosper。')
add('FQI-SRC-GR2-1.Ex6iii',R,'target_first_order','2φ0的相位指数为-1；完整相位和(q^n/a)^k仍给出有理移位，目标为a^(-n)。','必须保留phiTerm的负相位，原a及q非零条件需传递。','按2φ0真实定义计算U、V、c，禁止借用2φ1项比。')
add('FQI-SRC-GR2-2.Ex5',R,'direct_q_gosper','非自然终止的wellPoisedRaw部分和，n只控制截断；直接原差分比目标递推更合适。','wDefined包含a≠1；末项通常不为零，需实际求端点。','对展开后的原求和项试q-Gosper，比较G(n+1)-G(0)与目标。')
add('FQI-SRC-GR2-2.Ex12',R,'target_first_order','q、q²因子共享q^k，且含n的起点在q基上移动；混合步长本身不要求独立双基算法。','核对所有q²项的X²移位和良配因子；原分母条件仍须验证。','统一X=q^k、Q=q^n后独立派生比值及证书。')
add('FQI-SRC-GR2-2.Ex14i',R,'target_first_order','固定长度参数列表的4φ3单核，所有起点移动为整数q步，目标为乘积商。','原phiDefined决定特殊s值；不能暗加s≠0等条件。','在形式域搜索目标引导证书，列出消去产生的潜在奇点。')
for id,reason in [
 ('FQI-SRC-GR2-3.10.5','bibasicPhi第一组用q²、第二组用q；含n的移动起点在q组，n和k移位可统一成Q、X。'),
 ('FQI-SRC-GR2-3.10.6','q²组起点固定，长度相关参数在q组；右端含q^n起点但其相邻变化为完整q步。'),
 ('FQI-SRC-GR2-3.10.8','与相邻条目有不同的参数列表和q^n前因子；两组底数仍是同一q的整数幂。')]:
    add(id,R,'target_first_order',reason,'bibasicPhi=phiTerm×multibaseTerm，必须按列表长度保留两组相位及唯一的主阶乘。','按原定义展开、统一Q与X后试q-Gosper；不复用相似公式的证书。')
add('FQI-SRC-AP-3.3.14',R,'target_first_order','k与N-k的Pochhammer卷积乘几何项，目标为长度N的乘积商，形式移位比可有理化。','N-k的自然数减法仅在支撑内使用；单列新增尾项和零参数情形。','以N为递推变量计算局部差分并搜索。','有限卷积为备选。')
add('FQI-SRC-AP-13.E3',R,'target_first_order','线性下降积的相邻因子显式，Gaussian卷积及乘积目标都可形式有理化。','X、Y、Z均允许为零；不能把除以Y等参数的商表示当原语义。','先形式搜索，再寻找不除参数的多项式局部证明。','多项式卷积为备选。')
for id,reason in [('FQI-SRC-SILLS-2.Pair122','sillsAlpha的d=1使整除支撑为全支撑；q与q²长度因子均可用q^r有理化。'),('FQI-SRC-SILLS-2.Ex2c','d=1的alpha与q³分母仍共享单基q；闭式长度n、2n、3n的移位都是有限乘积。')]:
    add(id,R,'target_first_order',reason,'按真实sillsAlpha定义展开，包括r=0的显示商和整数指数；特殊q、x域仍待验证。','先检查展开后的U、V、c，再试目标引导q-Gosper。')
add('FQI-SRC-SILLS-3.Lem3.3',R,'target_first_order','显式q/q²混合单核、二次指数与(1-xq^(2r))因子；目标为有限乘积倒数。','不要将q²当独立底数；原分母范围和初值须核对。','统一q^r，派生目标差分并试q-Gosper。')
add('FQI-SRC-KAC-CHEUNG-4.4',R,'target_first_order','kacPowerNat是∏(x-q^i)，k比为x-q^k；Gaussian项和目标x^n提供有理移位结构。','原x可以为零；将下降积写成x^k(1/x;q)_k只可用于一般形式域试验。','先找证书，再用下降积本身验证以保留x=0。')

add('FQI-BAILEY-UNIT',C,'direct_q_gosper','r≥1时单位Bailey项具有有理项比，但r=0独立定义且目标是Kronecker零值。','固定n作为参数，只对r≥1搜索；补回r=0，并分n=0与n>0。','先建立分段支撑及端点计划，不使用零目标归一化。')
for id,reason in [('FQI-SRC-GR2-1.Ex6i','上界floor(n/2)，两个终止参数在n奇偶分支中交换角色。'),('FQI-SRC-GR2-2.3.2','闭式含floor/ceil长度，未分支时相邻系数不是统一的Q=q^n有理式。'),('FQI-SRC-GR2-II-19','目标含n模2与ceil(n/2)，一步移位会切换表达式。')]:
    add(id,C,'target_first_order_after_residue_split',reason,'先令n=2m+δ（原m变量相应重命名），分别验证支撑、相邻比与初值。','分奇偶后再决定能否用现有一阶构造；不能直接把原n一步递推送入。','步长二递推或其他求值方法。')
add('FQI-SRC-GR2-3.Ex34',C,'target_first_order_after_product_pairing','q²基中cq^(-n)、cq^(1-n)在n移位时只移动半个底数步。','先证明成对乘积合并为q基长度2k，或找到等价的有理消去；单个因子比不能直接假定有理。','完成成对因子分析后检验U、V、c。')
for id,reason in [('FQI-SRC-GR2-5.Ex18iii','双边支撑[-n,n]，约束bcde=q^(n+1)随n变化。'),('FQI-SRC-GR2-5.Ex18iv','双边支撑[-n-1,n]，约束bcde=q^(n+3)随n变化。'),('FQI-SRC-GR2-II-22','终止8φ7有bcde=a²q^(n+1)平衡条件，固定全部参数直接n移位会离开假设域。')]:
    add(id,C,'target_first_order_after_balanced_parameterization',reason,'选取由原非零条件支持的依赖参数消元，例如把e写成其他参数与q^n的商；追踪定义域。','先证明合法参数化并求移位比，再搜索；双边项另外处理两端。')
add('FQI-SRC-GR2-11.Ex21-p0',C,'target_first_order_after_case_and_balance_split','同时有两条平衡约束及b=a或ee=a分支；目标移位需保持这些关系。','分别代入两分支，合法消去依赖参数，检验相位及q/q²混合比值。','只有各分支的完整局部问题确定后才试q-Gosper。')
for id,reason in [('FQI-SRC-GR2-5.Ex19i','Gaussian立方仍给出单基有理项比；支撑为[-n,n]。'),('FQI-SRC-GR2-5.Ex19ii','Gaussian立方与奇上指标，支撑为[-n-1,n]。'),('FQI-SRC-AQ-3.17','负指标支撑[-n,n-1]、起始n≥1以及toNat指数需要同时处理。'),('FQI-SRC-AQ-3.18','双边交错Gaussian单核，形式移位可能有理，但原指数使用toNat。'),('FQI-SRC-SILLS-1.75','双边良配核含n±k长度分母和整数负幂，形式比值可作为候选。')]:
    add(id,C,'target_first_order_after_support_normalization',reason,'先证明整指数/自然数转换在实际支撑内的意义，明确n移位时两个端点及零延拓。','形成合法双边或平移后的局部问题，再做证书试验。')
for id,reason in [('FQI-SRC-GR2-8.1.2','下界max(j,k)、上界j+k，选择哪个外参数推进会改变有效支撑。'),('FQI-SRC-AP-3.3.11','min(M-m,N)及三个Gaussian支持相互作用，目标还可能恒零。'),('FQI-SRC-AQ-4.24','min(a,b,c)控制双边范围；递推某一参数时需区分哪一个参数最小。')]:
    add(id,C,'target_first_order_after_support_cases',reason,'选递推参数并划分有效支撑区域；不能在越界处使用Gaussian阶乘商。','先写清每个区域的移位和端点问题，再决定局部搜索。','有限卷积或已证核变换也可比较。')
for id,reason in [('FQI-SRC-AP-3.E1','双边q² Gaussian与平方指数可尝试平移为有限二项式核。'),('FQI-SRC-SILLS-1.JacobiFinite','双边交错Gaussian经j+m平移可尝试归约为有限二项式核。')]:
    add(id,C,'reindex_then_existing_p1_core',reason,'平移后参数含q负幂时须保留原允许q=0的情形，并证明乘积拆分。','优先验证重编号与原域桥接，再决定复用已证核心还是重新搜索。','P3重编号/乘积拆分后调用P1子核。')
add('FQI-SRC-AQ-3.37',C,'direct_q_gosper_with_parameter','显式单核在r方向形式超几何，目标为δ(n,0)，不能用目标商形成c。','把n作为原差分搜索的参数；证明n=0和n>0各自端点，原q=0等仍需处理。','先对原项求G，再比较端点；不要采用零目标归一化。')
add('FQI-SRC-SILLS-2.Lem2.31',C,'reparameterize_then_existing_p1_core','t²=q给出代数关联；以t统一基数后可尝试平移到二项式核。','证明代入与重编号；原域允许t=q=0，不能通过除t排除。','先验证代数桥接，再评估现有P1子核。','重编号及有限积拆分。')
add('FQI-SRC-SILLS-2.Ex2f',C,'target_first_order_after_residue_split','sillsAlpha仅在3整除r时非零；完整序列的逐r比不是普通有理项比。','先取r=3j，再对n模3分支，得到可用的移动上界及端点。','检验分支后的超几何比值，不对含周期零项的原序列求比。')
add('FQI-SRC-SILLS-2.Lem2.53',C,'target_first_order_after_base_substitution','t²=q且核含t的二次指数；在t基而非独立q,t系数域中才符合单基表示。','先代入q=t²并证明目标和项的表示对应；t=0与1+t分母须保留原域。','用t^r与t^n检验相邻比，再试证书。')

add('FQI-SRC-GR2-1.Ex17',D,'none_current','目标两端都是有限和，没有现成乘积闭式；旧G标签不能保证任一侧自身可原差分。','若将两侧配成单一残差核，须先证明其超几何性，当前未建立。','本轮不进入直接求和队列。','双侧递推比较、有限展开或卷积。')
add('FQI-SRC-GR2-7.2.12',D,'none_current','命题是三个不同参数/长度的φ之间的连续关系，不是单和到显式端点或闭式。','三个核可能经通分产生可望远镜的残差，但须另建连续关系的构造流程。','转交参数连续关系/逐系数验证。','系数比较或参数化望远镜；建立单核后可再入P1。')
add('FQI-SRC-GR2-7.Ex14',D,'none_current','完整Lean命题包含参数趋近1的Tendsto；有限几何和求值只能覆盖部分子目标。','不得把有限和子目标通过算作整题完成。','转交含极限桥接的组合流程。','有限几何和＋解析极限；P1仅可能作为子步骤。')
add('FQI-SRC-GR2-8.7.9-finite',D,'none_current','右端仍为φ有限和，且两侧截断上界不同；不能以一个闭式目标的相邻系数直接推进。','单列n=0并设计双侧关系，而非假定右端是超几何乘积。','本轮移出单和直接求值队列。','双侧变换/递推比较或有限展开。')
add('FQI-SRC-AQ-2.39',D,'none_current','aqInverseT是三角反演递归定义，不是输入时已知项比的单重超几何求和。','候选闭式须满足整个定义递归及奇偶初值。','转交反演或定义归纳；不把闭式代回后的子和当原题已有输入。','三角反演、定义归纳；必要时调用P1子和。')
add('FQI-SRC-FINE-7.GH',D,'none_current','fineHG由一对耦合递推定义，目标也是两个分量的合取。','必须验证两个分量的递推与初值，单次原差分不足以闭合完整命题。','转交定义递推验证。','联立归纳、乘积递推与累积和。')
add('FQI-SRC-SILLS-2.Ex7a-corrected',D,'none_current','核含a^(r+1)+a^(-r)；一般独立a,q下其逐r比不能只由X=q^r有理表示。','先拆成两个超几何和或双边对称化，再说明怎样重组目标；不能直接把整体当单核。','本轮不直接送入现有单核q-Gosper。','拆和、双边化、有限展开；预处理成立后可重新评估P1。')
add('FQI-SRC-KAC-CHEUNG-26.12',D,'none_current','symPower的根随n改变奇偶q²格点；一般的一步目标比不是固定Q=q^n的有理函数。','需普通/对称二项式桥接或步长二重参数化，而非仅把函数名展开。','本轮优先交给二项式记号桥接。','有限二项式变换；或另建奇偶/步长二方案后再评估。')

LABELS={V:'已完整验证',R:'优先符号试验',C:'先核查关键条件',D:'本轮交给其他流程'}

def main():
    original=json.loads((P1/'generated/train_a_screen/table.json').read_text())['records']
    selected=[r for r in original if r['candidate_routes']]
    assert len(selected)==51 and set(REVIEW)=={r['id'] for r in selected}
    rows=[]
    for source in selected:
        path=ROOT/source['source_path'];assert hashlib.sha256(path.read_bytes()).hexdigest()==source['source_sha256']
        review=REVIEW[source['id']]
        trial=HERE/'trials'/(source['id']+'.json')
        evidence=json.loads(trial.read_text()) if trial.exists() else None
        rows.append(dict(id=source['id'],order=source['order'],source_path=source['source_path'],source_sha256=source['source_sha256'],
            structure=source['structure'],previous_candidate_routes=source['candidate_routes'],
            previous_runtime_result=source['outcome'],**review,
            assessment_basis='manual structural review of the frozen Lean statement and shared definitions; frontend outcome not a selection criterion',
            symbolic_trial_status=evidence['status'] if evidence else 'not_run_in_this_review',
            symbolic_trial_path='trials/'+trial.name if evidence else None,
            end_to_end_verified=review['category']==V,
            formal_local_relation_verified=bool(evidence and evidence.get('construction',{}).get('q_wz_residual')=='0'),
            lean_proof_status='proved_in_previous_pipeline_run' if review['category']==V else 'not_proved'))
    counts=dict(Counter(r['category'] for r in rows))
    summary={'scope':'refine the 51 previously shortlisted candidates from 197 A-family train identities',
       'reviewed':len(rows),'categories':counts,'new_lean_proofs':0,
       'symbolic_trials':dict(Counter(r['symbolic_trial_status'] for r in rows)),
       'selection_policy':'P1 is one method family, not a universal prover. Deferred formulas are not declared unprovable.',
       'criteria':{
          'target_first_order':'After justified normalization, F(n+1,k)/F(n,k), F(n,k+1)/F(n,k), and T(n+1)/T(n) must be rational in the chosen single-base shift variables. q-Gosper must then construct the target-difference antidifference, with original-domain local, support, boundary, initial and recurrence obligations closed.',
          'direct_q_gosper':'With external parameters held fixed, the actual summand must have a rational single-base shift ratio; a q-hypergeometric antidifference must be constructed and its endpoint difference must match the original target. Parameter dependence on n is mathematically allowed even though the current emitter is narrower.',
          'limits':'Rational shift ratios are necessary structural evidence, not a guarantee of a certificate. Constructing a certificate over the formal field is not a Lean proof over the original domain.'},
       'next_trial_order':['FQI-CHU-VANDERMONDE-Q','FQI-CHU-VANDERMONDE-BALANCED','FQI-SRC-GR2-1.Ex6iii','FQI-SRC-KAC-CHEUNG-4.4','FQI-SRC-GR2-2.Ex5'],
       'evidence_sources':[{'path':'benchmark/lean/Benchmark/'+f,'sha256':hashlib.sha256((ROOT/'benchmark/lean/Benchmark'/f).read_bytes()).hexdigest()} for f in ['Definitions.lean','BatchDefinitions.lean','Batch4Definitions.lean','Batch5Definitions.lean']],
       'notes':['The rest of the 197 formulas were not reclassified as mathematically inapplicable.',
                'The four probes are explicit research transcriptions, not automatic Lean-expression extraction.',
                'No identity-specific proof content, certificate or recurrence answer was added to the production pipeline.']}
    (HERE/'review.json').write_text(json.dumps({'summary':summary,'records':rows},ensure_ascii=False,indent=2)+'\n')
    fields=['id','structure','category','proposed_route','mathematical_reason','required_check_or_preprocessing','next_action','alternative_method','symbolic_trial_status','lean_proof_status']
    stream=io.StringIO();w=csv.DictWriter(stream,fieldnames=fields);w.writeheader();w.writerows({k:r[k] for k in fields} for r in rows)
    (HERE/'review.csv').write_text('\ufeff'+stream.getvalue())
    e=html.escape
    page='''<!doctype html><html lang="zh"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>P1 数学适用性复审</title><style>body{font:15px/1.6 system-ui;margin:26px;color:#172033}table{border-collapse:collapse;width:100%}td,th{border:1px solid #ddd;padding:10px;vertical-align:top;text-align:left}th{background:#eef3fa}input{padding:10px;width:65%}small{color:#536075}</style><h1>P1 数学适用性复审：51 条初筛候选</h1><p>P1不承担全覆盖。分类依据是数学结构，不是程序能否解析；本轮转交其他流程不表示不可证明。所有未完成项均只列为候选。</p>'''
    page+='<p>'+'；'.join(e(LABELS[c])+f'：{v}' for c,v in counts.items())+'</p>'
    page+='<p>4 条优先候选进行了独立符号试验；证书构造不计 Lean 覆盖，原始目标的语义桥接、边界及参数域仍待验证。</p><p><a href="review.csv">CSV</a> · <a href="review.json">完整依据、条件与定义来源</a></p><input id="query" placeholder="搜索公式、分类、数学条件"><p id="count"></p><table><thead><tr>'
    page+=''.join('<th>'+t+'</th>' for t in ['公式','分类与路线','数学依据','先核查什么','下一步/其他方法','符号试验'])+'</tr></thead><tbody>'
    for r in rows:
        trial=e(r['symbolic_trial_status'])
        if r['symbolic_trial_path']:trial='<a href="'+e(r['symbolic_trial_path'])+'">'+trial+'</a><br><small>研究转录；非Lean证明</small>'
        cells=[e(r['id'])+'<br>'+e(r['structure']),e(LABELS[r['category']])+'<br>'+e(r['proposed_route']),e(r['mathematical_reason']),e(r['required_check_or_preprocessing']),e(r['next_action'])+'<br>'+e(r['alternative_method']),trial]
        page+='<tr>'+''.join('<td>'+t+'</td>' for t in cells)+'</tr>'
    page+='''</tbody></table><script>const rows=[...document.querySelectorAll('tbody tr')],q=document.getElementById('query');function f(){let n=0;for(const r of rows){r.hidden=!r.textContent.toLowerCase().includes(q.value.toLowerCase());if(!r.hidden)n++}document.getElementById('count').textContent=`显示 ${n} / 51 条`;}q.addEventListener('input',f);f();</script></html>'''
    (HERE/'index.html').write_text(page)
    print(json.dumps(summary,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
