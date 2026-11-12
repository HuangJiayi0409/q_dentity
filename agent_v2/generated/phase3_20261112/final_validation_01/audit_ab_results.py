"""Audit only frozen A/B and synthetic Init evidence; no third-stage-wide claim."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from agent_v2.executor import assemble_term, validate_invariant
from agent_v2.models import ResidualState
from agent_v2.storage import RunStore, guard_path, verify_source

def read(path):
    return json.loads(Path(path).read_text())

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def require(condition, message):
    if not condition:
        raise AssertionError(message)

def audit_run(label, run, expected_rounds, expected_c, expected_links, expected_replays, expected_negatives):
    store = RunStore(run)
    initial = ResidualState.from_dict(store.read_json('initial_state.json'))
    state = ResidualState.from_dict(store.load_checkpoint()['state'])
    validate_invariant(state)
    verify_source(state.G, store.root)
    require(state.G == initial.G and state.Gamma == initial.Gamma, label + ': original context changed')
    require(state.status == 'original_theorem_proved' and not state.O, label + ': original not accepted')
    require(state.round_index == expected_rounds and len(state.C) == expected_c
            and len(state.links) == expected_links, label + ': final counts differ')
    require(initial.b.actions - state.b.actions == expected_rounds, label + ': actions repeated or charged twice')
    paths = []
    for path in sorted((run / 'rounds').glob('*/verification.json')):
        paths.extend(('partial', path, item['check']) for item in read(path)['checks'] if 'check' in item)
    resume_paths = sorted((run / 'resume_checks').glob('*/result.json'))
    require(len(resume_paths) == expected_replays, label + ': fresh replay count differs')
    paths.extend(('replay', path, read(path)) for path in resume_paths)
    final_paths = sorted((run / 'final').glob('*/checked.json'))
    require(len(final_paths) == (1 if label == 'init' else 2), label + ': original check count differs')
    paths.extend(('original', path, read(path)) for path in final_paths)
    negative_paths = sorted(run.glob('negative-*/verification.json'))
    require(len(negative_paths) == expected_negatives, label + ': negative probe count differs')
    for path in negative_paths:
        paths.extend(('negative', path, item['check']) for item in read(path)['checks'] if 'check' in item)
    counts = {'partial': 0, 'replay': 0, 'original': 0, 'negative': 0}
    artifacts = {}
    audits = []
    for kind, path, checked in paths:
        counts[kind] += 1
        evidence = checked['evidence']
        require(evidence['source_sha256'] == state.G.sha256, label + ': check Source binding differs')
        if kind == 'negative':
            require(checked['accepted'] is False and checked['status'] == 'incomplete'
                    and checked['sigma']['code'] == 'lean_check_failed'
                    and evidence['returncode'] not in (0, None), label + ': negative did not reach real Lean')
        else:
            require(checked['accepted'] is True and evidence['returncode'] == 0, label + ': positive check rejected')
            audit = evidence['audit']
            target = state.G.theorem if kind == 'original' else 'AgentV2Candidate.proof'
            require(audit['theorem'] == target and evidence['theorem'] == target, label + ': audited wrong theorem')
            require(set(audit['axioms']) <= {'propext', 'Classical.choice', 'Quot.sound'}, label + ': unapproved axiom')
            if label != 'init':
                require(evidence['profile'] == ('gaussian_geometric_recurrence_v1' if label == 'recurrence'
                                                else 'gaussian_weighted_range_v1'), label + ': wrong proof profile')
                require(not any(module.startswith('Benchmark.Statements') or module == 'Benchmark.Representation'
                                or 'Batch3Proofs' in module for module in audit['modules']),
                        label + ': original statement/proof cache imported')
                if kind == 'original':
                    require(audit['universe_parameter_count'] == 1, label + ': generic Field specialized')
                else:
                    require(audit['universe_parameters'] == ['u'], label + ': generic local Field specialized')
            if kind == 'original':
                request = read(path.parent / 'request.json')
                request_state = ResidualState.from_dict(request['state'])
                validate_invariant(request_state)
                require(request['proof_term'] == assemble_term(request_state), label + ': final term differs from tree')
                audits.append({'result_path': str(path), 'source_sha256': evidence['source_sha256'],
                    'theorem': audit['theorem'], 'axioms': audit['axioms'],
                    'universe_parameters': audit.get('universe_parameters'),
                    'universe_parameter_count': audit.get('universe_parameter_count'),
                    'returncode': evidence['returncode']})
        for artifact in evidence.get('artifacts', []):
            target = guard_path(artifact['path'], store.root)
            require(target not in artifacts or artifacts[target] == artifact['sha256'], label + ': conflicting artifact SHA')
            artifacts[target] = artifact['sha256']
    require(counts == {'partial': expected_rounds, 'replay': expected_replays,
                      'original': 1 if label == 'init' else 2, 'negative': expected_negatives},
            label + ': actual retained check counts differ')
    for path, digest in artifacts.items():
        require(sha(path) == digest, label + ': retained artifact hash differs: ' + str(path))
    return {'run_dir': str(run), 'source_identity': state.G.identity, 'source_sha256': state.G.sha256,
        'original_theorem': state.G.theorem, 'original_identity_proved': True,
        'rounds': state.round_index, 'C': len(state.C), 'O': len(state.O), 'links': len(state.links),
        'actual_check_counts': counts, 'original_audits': audits, 'remaining_budget': state.b.to_dict(),
        'independent_artifact_hashes_checked': len(artifacts)}

def main():
    manifest_path = OUT / 'frozen/manifest.json'
    manifest = read(manifest_path)
    before = read(OUT / 'ab_hashes_before.json')
    require(sha(manifest_path) == before['manifest_sha256'], 'freeze manifest changed')
    mismatches = []
    for name, item in manifest['files'].items():
        for location, path in [('current', ROOT / name), ('snapshot', Path(item['snapshot_path']))]:
            if sha(path) != item['sha256']:
                mismatches.append({'file': name, 'location': location})
    require(not mismatches and len(manifest['files']) == 262, 'frozen current/snapshot mismatch')
    for name, expected in manifest['baseline_tests_unchanged'].items():
        require(sha(ROOT / name) == expected, 'old test changed: ' + name)
    report = {'schema_version': 1, 'scope': 'final frozen A/B plus real synthetic/test-only Init validation',
        'passed': True, 'created_utc': datetime.now(timezone.utc).isoformat(),
        'freeze_manifest': str(manifest_path), 'freeze_manifest_sha256': sha(manifest_path),
        'frozen_current_and_snapshot_files_checked': len(manifest['files']),
        'current_and_snapshot_mismatches': mismatches,
        'baseline_test_files_unchanged': len(manifest['baseline_tests_unchanged']),
        'results': {}, 'model_calls': 0, 'benchmark_Test_read': False,
        'production_or_existing_test_edits': [], 'entire_phase_three_completion_claimed': False}
    for label in ('recurrence', 'telescoping', 'init'):
        driver = read(OUT / 'driver_logs' / label / 'result.json')
        require(driver['returncode'] == 0, label + ': smoke process failed')
        if label == 'init':
            lines = Path(driver['stdout']).read_text().splitlines()
            smoke = json.loads(lines[-1])
            require(smoke['scope'] == 'synthetic_test_only', 'Init scope is not explicit')
            run = Path(smoke['run_dir'])
            scope = read(run / 'fixture_scope.json')
            require(scope['Train_result'] is False and scope['candidate_provider'] == 'test_only_handwritten',
                    'Init may not be represented as a Train/CAS result')
            audited = audit_run(label, run, 2, 2, 2, 0, 0)
            audited.update(scope='synthetic_test_only', Train_result=False,
                candidate_provider='test_only_handwritten', unchanged_test_budget_seconds=90,
                fixture_scope_path=str(run / 'fixture_scope.json'))
        else:
            smoke = read(OUT / label / 'summary.json')
            require(smoke['passed'] is True and smoke['original_identity_proved'] is True,
                    label + ': smoke self audit failed')
            recurrence = label == 'recurrence'
            require(smoke['resume_repeated_actions'] == 0 and smoke['historical_proofs_reused'] is False,
                    label + ': invalid replay/provenance claims')
            audited = audit_run(label, Path(smoke['run_dir']), 5 if recurrence else 4,
                5 if recurrence else 4, 4 if recurrence else 3, 17 if recurrence else 4,
                5 if recurrence else 1)
            audited.update(scope=smoke['scope'], smoke_summary_path=str(OUT / label / 'summary.json'),
                requested_initial_budget_seconds=4000 if recurrence else 2400,
                smoke_self_checked_artifact_hashes=smoke['artifact_hashes_checked'],
                resume_repeated_actions=smoke['resume_repeated_actions'],
                diagnostic_probes_are_separate_from_runtime_budget=True)
            if recurrence:
                require(smoke['resumed_after_initial_value'] is True and smoke['fresh_replay_checks'] == 17,
                        'recurrence staged replay coverage incomplete')
                audited.update(stages=smoke['stages'], negative_proofs=smoke['negative_proofs'],
                    resumed_after_initial_value=True,
                    original_declaration=smoke['original_declaration'])
            else:
                audited['negative_bridge'] = smoke['negative_bridge']
        audited['driver_record'] = driver
        report['results'][label] = audited
    output = OUT / 'final_ab_summary.json'
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'passed': True, 'summary': str(output),
                     'frozen_files': 262, 'old_tests': 30,
                     'scope': report['scope']}, ensure_ascii=False))

if __name__ == '__main__':
    main()
