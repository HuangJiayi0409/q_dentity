#!/usr/bin/env python3
"""Independently audit full proofs versus deliberately unfinished normalization attempts."""
import hashlib,json,re,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;P1=HERE.parents[1];ROOT=P1.parents[1];sys.path.insert(0,str(P1))
from lean_pipeline import find_nodes

def read(p):return json.loads(p.read_text())
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    summary=read(HERE/'summary.json');assert summary['selected']==11
    for file,h in summary['code_sha256'].items():assert digest(P1/file)==h,file
    support=read(HERE/'support_validation.json')
    assert support['status']=='passed' and support['lean']['exit_code']==0 and 'sorryAx' not in support['lean']['output']
    assert support['source_sha256']==digest(P1/'lean/SupportRules.lean')
    assert support['proof_sha256']==digest(HERE/'SupportValidation.lean')
    complete=normalized=0
    for row in summary['records']:
        identity=row['id'];source=row['source'];assert source['sha256']==digest(ROOT/source['path'])
        native=read(HERE/row['native_report']);assert native['source']==source
        assert native['status']==row['native_status']
        if row['original_lean_proved']:
            assert native['status']=='proved' and not native['remaining_obligations'] and not row['remaining_obligations']
            v=native['verification'];assert v['lean']['exit_code']==0 and 'sorryAx' not in v['lean']['output']
            assert digest(Path(v['proof_file']))==v['proof_sha256']
            complete+=1
        else:
            assert row['remaining_obligations']
            r=read(HERE/identity/'normalization_validation.json');assert r['original_train_proof'] is False
            assert r['normalizer_sha256']==digest(HERE/'normalize.py')
            assert r['attempt_sha256']==digest(HERE/identity/'NormalizationAttempt.lean')
            assert len(re.findall(r'\berror:',r['lean']['output']))==1 and 'P1_EXPORT_ONLY' in r['lean']['output']
            expr=read(HERE/identity/'normalized_expression.json')
            if 'bilateral_interval_reindexed_with_both_endpoints' in r['steps']:assert not find_nodes(expr,'Finset.Icc')
            if 'explicit_Pochhammer_lists_expanded_in_Lean' in r['steps']:assert not find_nodes(expr,'FiniteQBenchmark.pochList')
            if 'unitBailey_definition_expanded_preserving_zero_branch' in r['steps']:
                assert not find_nodes(expr,'FiniteQBenchmark.unitBailey') and find_nodes(expr,'ite')
            if 'sillsAlpha_definition_and_unit_divisibility_expanded' in r['steps']:assert not find_nodes(expr,'FiniteQBenchmark.sillsAlpha')
            normalized+=1
    assert complete==summary['new_original_proofs']==2 and normalized==9
    report=dict(status='passed',source_hashes_checked=11,new_original_proofs=complete,
        incomplete_but_Lean_preprocessed=normalized,complete_train_proofs=8,
        normalization_does_not_count_as_original_proof=True,code_hashes_checked=len(summary['code_sha256']))
    (HERE/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
