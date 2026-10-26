#!/usr/bin/env python3
"""Audit completed batch provenance and summarize first blockers, not mathematical failures."""
from collections import Counter
import copy
import csv
import io
import json
from pathlib import Path
import re
from batch import OUT, HERE, ROOT, CODE, digest, write, screen


def main():
    summary=json.loads((OUT/'summary.json').read_text())
    rows=json.loads((OUT/'table.json').read_text())['records']
    original=screen()
    assert len(rows)==summary['total']==summary['attempted']==197
    assert len({r['id'] for r in rows})==197
    assert summary['code_sha256']=={name:digest(HERE/name) for name in CODE}
    assert summary['outcomes']==dict(Counter(r['outcome'] for r in rows))
    assert [r['id'] for r in rows]==[r['id'] for r in original]
    missing=Counter(); missing_candidates=Counter(); exports=Counter()
    all_failed_before_construct=[]
    proved=[]
    for row,prior in zip(rows,original):
        assert all(row[k]==v for k,v in prior.items())
        path=OUT/row['report_path']; assert digest(path)==row['report_sha256']
        report=json.loads(path.read_text())
        assert report['source']['identity_id']==row['id']
        assert report['source']['sha256']==row['source_sha256']
        assert report['test_files_read']==0 and report['preset_proof_fallback'] is False
        assert report['status']==row['run_status']
        error=report.get('error','')
        unknown=set(re.findall(r'Unknown (?:identifier|constant) [`\']([^`\']+)[`\']',error))
        missing.update(unknown)
        if row['candidate_routes']:missing_candidates.update(unknown)
        if row['outcome']=='expression_export_gap':
            expression=row['detail']
            exports.update([expression.split()[0] if expression else 'unknown'])
        if not row['reached_symbolic_backend']:all_failed_before_construct.append(row['id'])
        if row['outcome']=='proved':
            verified=report['verification']; proof=Path(verified['proof_file'])
            assert proof.resolve().is_relative_to(OUT.resolve())
            assert digest(proof)==verified['proof_sha256']
            assert verified['lean']['exit_code']==0
            assert 'sorryAx' not in verified['lean']['output']
            assert f"'{verified['theorem']}' depends on axioms: [propext, Classical.choice, Quot.sound]" in verified['lean']['output']
            assert not report['remaining_obligations']
            proved.append(row['id'])
    dependencies=json.loads((OUT/'dependencies.json').read_text())
    for entry in dependencies['dependencies']:assert digest(ROOT/entry['path'])==entry['sha256']
    for entry in dependencies['artifacts']:assert digest(Path(entry['path']))==entry['sha256']
    from run import batch_environment
    for key in ('dependencies','artifacts'):
        corrupted=copy.deepcopy(dependencies)
        corrupted['env']={}
        corrupted[key][0]['sha256']='0'*64
        try:batch_environment(corrupted)
        except ValueError as exc:assert 'snapshot changed' in str(exc)
        else:raise AssertionError('corrupt snapshot accepted')
    assert proved==summary['proved']
    candidates=[r for r in rows if r['candidate_routes']]
    features=Counter(f for r in candidates for f in set(r['features']))
    analysis={'status':'passed','scope':'all 197 A-family train; original sources unchanged',
        'completed_runs':len(rows),'automatic_train_proofs':len(proved),'proved':proved,
        'current_route_structural_candidates':len(candidates),
        'candidate_route_counts':dict(Counter(c for r in candidates for c in r['candidate_routes'])),
        'candidate_overlap':sum(len(r['candidate_routes'])>1 for r in candidates),
        'candidate_outcomes':dict(Counter(r['outcome'] for r in candidates)),
        'all_outcomes':summary['outcomes'],
        'all_missing_symbols_per_target':dict(missing.most_common()),
        'candidate_missing_symbols_per_target':dict(missing_candidates.most_common()),
        'export_blocked_expression_heads':dict(exports.most_common()),
        'candidate_statement_features_overlapping':dict(features.most_common()),
        'failed_before_symbolic_result':len(all_failed_before_construct),
        'evidence_limits':['Only the first blocking stage is observed for each unsuccessful target.',
            'The 51-candidate shortlist inherits the earlier structural review; it is not a completeness bound.',
            'Missing definitions result from the current minimal shared-import environment, not invalid train formulas.',
            'No symbolic impossibility conclusion follows from elaboration/export/routing gaps.'],
        'next_work':[
            'Restore audited definition dependencies in the isolated frontend, without importing identity proofs.',
            'Implement phi/list/integer-power extraction for the affected current-route candidates.',
            'Re-run those candidates before prioritizing certificate translation or denominator proof extensions.'],
        'checks':['197 unique source IDs and 394 source hashes', 'all raw report hashes and statuses',
                  'code hashes and compiled dependency hashes', 'successful proof hashes and Lean axiom audits',
                  'no test identities and no preset proof fallback',
                  'source and compiled snapshot mismatch rejected before proof generation']}
    write(OUT/'analysis.json',analysis)
    stream=io.StringIO(); fields=['order','id','structure','candidate_routes','applicability_basis',
                                 'pending_mathematical_checks','outcome','failure_stage','detail','report_path']
    writer=csv.DictWriter(stream,fieldnames=fields);writer.writeheader()
    for r in candidates:writer.writerow({k:'; '.join(r[k]) if isinstance(r[k],list) else r[k] for k in fields})
    (OUT/'current_candidates.csv').write_text('\ufeff'+stream.getvalue())
    print(json.dumps(analysis,ensure_ascii=False,indent=2))


if __name__=='__main__':main()
