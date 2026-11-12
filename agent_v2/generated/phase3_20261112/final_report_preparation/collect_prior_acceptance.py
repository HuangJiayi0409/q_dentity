"""Collect stage-frozen evidence for reporting; never substitute it for final regression."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];BASE=ROOT/'agent_v2/generated/phase3_20261112';HERE=Path(__file__).resolve().parent
read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def reference(p):return {'path':str(p),'sha256':sha(p),'size':p.stat().st_size}
def save(name,value):(HERE/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
source_summary=BASE/'ab_recurrence_closure/summary.json';summary=read(source_summary);run=Path(summary['run_dir'])
initial=read(run/'initial_state.json');source=initial['G'];assert source['declaration']==summary['original_declaration']
assert sha(Path(source['snapshot_path']))==source['sha256']==summary['source_sha256']
steps=[]
for row in summary['steps']:
 directory=run/'rounds'/str(row['round']);before=read(directory/'state_before.json');after=read(directory/'state_after.json')
 action=read(directory/'action.json');result=read(directory/'result.json');candidate=result['C_partial'][0]
 assert candidate['id']==row['candidate_id'] and candidate['proposition']==row['proposition']
 assert [x['id'] for x in before['C']]==row['C_before'] and [x['id'] for x in after['C']]==row['C_after']
 assert before['O']==row['O_before'] and after['O']==row['O_after']
 assert before['b']==row['budget_before'] and after['b']==row['budget_after']
 check=read(directory/'verification.json')['checks'][0]['check'];assert check['accepted'] is True
 receipt=check['evidence'];assert set(receipt['audit']['axioms'])<={'propext','Classical.choice','Quot.sound'}
 steps.append({**row,'actual_action':action,'actual_candidate':candidate,
  'r_before':before['r'],'r_after':after['r'],'partial_axioms':receipt['audit']['axioms'],
  'references':[reference(directory/name) for name in ('action.json','result.json','state_before.json','state_after.json','verification.json')]})
assert len(steps)==5
original_checks=[]
for path in sorted((run/'final').glob('*/checked.json')):
 checked=read(path);assert checked['accepted'] is True and checked['status']=='original_theorem_proved'
 receipt=checked['evidence'];assert receipt['theorem']==source['theorem'] and receipt['source_sha256']==source['sha256']
 assert set(receipt['audit']['axioms'])<={'propext','Classical.choice','Quot.sound'}
 artifact_hashes=[]
 for item in receipt['artifacts']:
  p=Path(item['path']);assert sha(p)==item['sha256'];artifact_hashes.append(item)
 original_checks.append({'reference':reference(path),'accepted':True,'status':checked['status'],'cost':checked['cost'],
  'theorem':receipt['theorem'],'proposition':receipt['proposition'],'proof_term':receipt['proof_term'],
  'audit':{k:v for k,v in receipt['audit'].items() if k!='modules'},
  'actual_benchmark_imports':[m for m in receipt['audit']['modules'] if m.startswith('Benchmark.')],
  'external_environment_sha256':receipt['external_environment_sha256'],'lean_binary':receipt['lean_binary'],
  'lean_binary_sha256':receipt['lean_binary_sha256'],'profile':receipt['profile'],'profile_version':receipt['profile_version'],
  'artifact_hashes_checked':len(artifact_hashes)})
assert len(original_checks)==2
negative=[]
for row in summary['negative_proofs']:
 directory=Path(row['evidence_directory']);before=read(directory/'state_before.json');after=read(directory/'state_after.json')
 assert before==after
 check=read(directory/'verification.json')['checks'][0]['check']
 assert check['accepted'] is False and check['evidence']['returncode']!=0
 negative.append({**row,'sigma':check['sigma'],'returncode':check['evidence']['returncode'],
  'references':[reference(directory/name) for name in ('candidate.json','verification.json','state_before.json','state_after.json')]})
record={'scope':'Historical A/B stage-frozen acceptance facts; final-runtime regression is pending',
 'final_regression_complete':False,'summary':reference(source_summary),'source':source,
 'steps':steps,'stages':summary['stages'],'original_checks':original_checks,'negative_proofs':negative,
 'fresh_replay_checks':summary['fresh_replay_checks'],'resume_repeated_actions':summary['resume_repeated_actions'],
 'remaining_budget':summary['remaining_budget'],'commands':summary['commands'],
 'source_versions':'ab_staged snapshot; default CLI compatibility patch has a separate run and package',
 'current_runtime_equivalence_claimed':False}
save('ab_exact_evidence.json',record)
lines=['# A/B 已验材料摘录（阶段冻结版，非最终回归）','',
 '以下来自已有 A/B 分阶段实际运行。后续最终源码的新完整回归和新 smoke 尚待汇入，不能把本页改写为最终运行结果。','',
 '## 原始完整声明','',f"- identity：`{source['identity']}`",f"- theorem：`{source['theorem']}`",f"- SHA-256：`{source['sha256']}`",'',
 '下方是冻结的原题输入声明，原输入中的 `sorry` 仅标记待证题；实际验收证明从证书树另外构造并编译。','',
 '```lean',source['declaration'].rstrip(),'```','','## 五轮实际顺序与精确命题','',
 '实际动作顺序为局部递推 → 唯一性连接 → 初值 1 → 初值 0 → 右端递推。连接获验后才建立后三个义务；初值与右端的执行顺序由当时合法候选选择决定。','']
for row in steps:
 lines += [f"### 第 {row['round']} 轮：{row['task']}",'',f"候选 `{row['candidate_id']}`；动作 `{row['action_id']}`；依赖 `{', '.join(row['dependencies']) or '无'}`。",'',
  '```lean',row['proposition'],'```','']
lines+=['## C/O/links/r/预算轨迹','','| 轮 | task | C 前→后 | O 前→后 | links 前→后 | r | 动作预算 | 秒预算前→后 | 实际动作秒 |','| --- | --- | --- | --- | --- | --- | --- | --- | --- |']
for row in steps:
 lines.append(f"| {row['round']} | {row['task']} | {len(row['C_before'])}→{len(row['C_after'])} | {len(row['O_before'])}→{len(row['O_after'])} | {row['links_before']}→{row['links_after']} | {row['r']} | {row['budget_before']['actions']}→{row['budget_after']['actions']} | {row['budget_before']['seconds']:.6f}→{row['budget_after']['seconds']:.6f} | {row['cost']['wall_seconds']:.6f} |")
lines+=['','轮间差额包含真实恢复重验，因此上一轮结束秒数不一定等于下一轮动作前秒数。完整精度、义务命题和逐阶段预算见同目录 `ab_exact_evidence.json`。','',
 '## 数学关系','',
 '定义 S(m) 为原 Gaussian 交错和，R(m) 为原奇偶 Pochhammer 右端。局部与右端证书分别给出 X(m+2)+(q^(m+1)-1)X(m)=0；实际符号系数保留中间的零项，不改变原式。初值证书给 S(0)=R(0)=1 与 S(1)=R(1)=0。唯一性连接依赖已验 S 递推，对自然数作强归纳，由同一二阶关系和两个初值得到所有 m 的 S(m)=R(m)。','',
 '## 原 theorem 审计与负例','',
 f"真实恢复候选检查 {summary['fresh_replay_checks']} 次，重复动作 {summary['resume_repeated_actions']} 次；独立原 theorem 编译 {len(original_checks)} 次。两次 theorem 均为 `{source['theorem']}`，公理均为 `propext, Classical.choice, Quot.sound`。",'',
 '五类候选各一次实际错误 Lean 证明均被拒绝；唯一性错误连接在替换义务之前失败，前后状态相同。没有以局部 theorem 审计替代原题审计。','']
(HERE/'AB_EXACT_EVIDENCE.md').write_text('\n'.join(lines)+'\n')
methods=[]
for method in ('coefficient','interpolation','determinant','kernel_transform','difference_ring','macmahon'):
 p=BASE/method/'acceptance_final/summary.json';s=read(p);r=Path(s['run_dir']);state=read(r/'checkpoint.json')['state'];certificate=state['C'][0]
 assert len(state['C'])==1 and [o['id'] for o in state['O']]==['original'] and state['links']==[]
 methods.append({'method':method,'identity':state['G']['identity'],'theorem':state['G']['theorem'],'source_sha256':state['G']['sha256'],
  'summary':reference(p),'run_dir':str(r),'certificate_id':certificate['id'],'exact_local_proposition':certificate['proposition'],
  'proof_term':certificate['proof_term'],'profile':certificate['evidence']['profile'],'axioms':certificate['evidence']['audit']['axioms'],
  'C':1,'O':['original'],'links':0,'full_original':False,'commands':s.get('commands',[]),
  'current_runtime_equivalence_claimed':False})
save('C_stage_exact_candidates.json',{'scope':'Six accepted C local propositions from their own frozen stage runs; spectral remains stopped; final regression pending','methods':methods})
save('collection_validation.json',{'passed':True,'A_B_steps_checked':5,'A_B_original_checks_checked':2,'A_B_negative_proofs_checked':5,
 'C_local_candidates_collected':6,'original_artifact_hashes_checked':sum(r['artifact_hashes_checked'] for r in original_checks),
 'final_regression_complete':False,'runtime_edited':False,'old_tests_edited':False,'benchmark_Test_read':False,'model_calls':0})
print(json.dumps({'passed':True,'steps':5,'original_checks':2,'negative_proofs':5,'C_candidates':6,'final_regression_complete':False}))
