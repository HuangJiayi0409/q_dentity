"""Reproduce the existing P1 candidate allocation; no applicability/proof claims."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SOURCE = ROOT / 'finite_product_framework/research/train_a_methods/plans.json'
TARGET = HERE / 'remaining_candidates.json'


def render():
    raw = SOURCE.read_bytes()
    entries = json.loads(raw)['entries']
    assert len(entries) == 197 and len({e['id'] for e in entries}) == 197
    selected = [e for e in entries if e['primary_mechanism'] == 'P1']
    assert len(selected) == 120
    records = []
    for e in selected:
        formula = ROOT / 'benchmark/formulas/train' / (e['id'] + '.md')
        assert formula.is_file(), e['id']
        records.append({
            'id': e['id'], 'main_component': e['main_component'],
            'assignment_basis': e['assignment_basis'],
            'first_action': e['first_action'],
            'component_roles': e['component_roles'],
            'formula_sha256': hashlib.sha256(formula.read_bytes()).hexdigest(),
            'status': 'inherited_candidate_not_new_applicability_verification',
        })
    return json.dumps({
        'schema_version': 1,
        'scope': 'existing P1 primary allocation within A-family train only',
        'source': str(SOURCE.relative_to(ROOT)),
        'source_sha256': hashlib.sha256(raw).hexdigest(),
        'meaning': 'Candidate allocation, not disjoint mathematical applicability or proof coverage. W/G retained for context.',
        'new_backend_implementations': 0, 'new_train_proofs': 0,
        'main_component_counts': dict(sorted(Counter(e['main_component'] for e in selected).items())),
        'entries': records,
    }, ensure_ascii=False, indent=2) + '\n'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = render()
    if args.check:
        assert TARGET.read_text() == result, 'Stale candidate index'
    else:
        TARGET.write_text(result)
    print(json.dumps({'status': 'passed', 'candidates': 120, 'new_train_proofs': 0}))
