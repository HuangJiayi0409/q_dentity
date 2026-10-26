"""Lean-executed, structure-selected preprocessing; does not claim a sum proof."""
import hashlib,json,re,sys
from pathlib import Path
P1=Path(__file__).resolve().parents[2];sys.path.insert(0,str(P1))
from lean_pipeline import HERE,assemble,proof_slot,lean,find_nodes

def normalize(source,raw,hypotheses,work,env):
    steps=[];tactics=[]
    if find_nodes(raw,'Finset.Icc'):
        tactics.append('  rw [FiniteQP1.sum_bilateral_range]')
        steps.append('bilateral_interval_reindexed_with_both_endpoints')
    rules=[]
    if find_nodes(raw,'FiniteQBenchmark.pochList'):
        rules+=['pochList_cons','pochList_nil','mul_one']
        steps.append('explicit_Pochhammer_lists_expanded_in_Lean')
    if find_nodes(raw,'FiniteQBenchmark.unitBailey'):
        rules+=['unitBailey']
        steps.append('unitBailey_definition_expanded_preserving_zero_branch')
    if find_nodes(raw,'FiniteQBenchmark.sillsAlpha'):
        rules+=['sillsAlpha','one_dvd','ite_true','Nat.div_one','pow_one','mul_one','one_mul']
        steps.append('sillsAlpha_definition_and_unit_divisibility_expanded')
    if rules:tactics.append('  simp only ['+', '.join(dict.fromkeys(rules))+']')
    for hyp in hypotheses:
        ty=hyp['type']
        if ty['op']!='Eq':continue
        a,b=ty['args'];direction=None
        if b['op']=='var' and a['op']=='HPow.hPow':direction='← '
        elif a['op']=='var' and b['op']=='HPow.hPow':direction=''
        if direction is not None:
            # The rewrite is checked against the actual local hypothesis by Lean.
            assert re.fullmatch(r'[A-Za-z_][A-Za-z_0-9]*',hyp['name'])
            tactics.append('  rw ['+direction+hyp['name']+']')
            steps.append('parameter_power_equality_rewritten_in_Lean')
    assert steps
    attempt=work/'NormalizationAttempt.lean'
    attempt.write_text(assemble([(HERE/'lean/SupportRules.lean').read_text(),
        (HERE/'lean/Extract.lean').read_text(),proof_slot(source,'\n'.join(tactics)+'\n  p1_export')]))
    result=lean(attempt,env)
    assert len(re.findall(r'\berror:',result['output']))==1 and 'P1_EXPORT_ONLY' in result['output'],result
    expressions=[json.loads(line.split('P1_JSON:',1)[1]) for line in result['output'].splitlines() if 'P1_JSON:' in line]
    assert len(expressions)==1 and expressions[0]!=raw
    report=dict(status='normalized_not_proved',steps=steps,original_train_proof=False,lean=result,
        attempt_sha256=hashlib.sha256(attempt.read_bytes()).hexdigest(),
        normalizer_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    (work/'normalized_expression.json').write_text(json.dumps(expressions[0],ensure_ascii=False,indent=2)+'\n')
    (work/'normalization_validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    return report
