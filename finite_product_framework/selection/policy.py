"""One method from coherent route scores; no training data or proof lookup."""
import hashlib
import json
from pathlib import Path
import time

from .capabilities import ROUTES, RULE_VERSION, assess
from .features import extract
from .scoring import CRITERIA, ahp, bounds

VERSION = 'ahp-fixed-topsis/1-unknown-tie'


def all_unknown_tie(methods):
    """A deterministic display order is not evidence for a method choice."""
    return bool(methods) and all(m['status'] == 'unknown' and m['score'] is not None and
                                m['score'] == methods[0]['score'] for m in methods)


def rank(routes, weights, families):
    def order(row):
        # Lower bound first. Ties prefer fewer unknowns, then a stable route name.
        return (-row['score']['lower'], row['score']['upper']-row['score']['lower'], row['route'])
    for row in routes:
        row['score'] = bounds(row['criteria'], weights) if row['status'] != 'unsupported' else None
    methods = []
    for method in families:
        candidates = sorted([r for r in routes if r['method'] == method and r['score'] is not None], key=order)
        best = candidates[0] if candidates else None
        methods.append(dict(method=method, status=best['status'] if best else 'unsupported',
                            best_route=best['route'] if best else None,
                            score=best['score'] if best else None))
    methods.sort(key=lambda r: (r['score'] is None,
        -r['score']['lower'] if r['score'] else 0,
        r['score']['upper']-r['score']['lower'] if r['score'] else 0, r['method']))
    for i, row in enumerate(methods, 1): row['rank'] = i if row['score'] is not None else None
    return methods


def fingerprint():
    base = Path(__file__).resolve().parents[1]
    paths = list((base/'selection').glob('*.py'))
    paths += [base/source for _, _, _, source in ROUTES]
    files = {str(p.relative_to(base)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(set(paths))}
    return dict(files=files, sha256=hashlib.sha256(json.dumps(files, sort_keys=True).encode()).hexdigest())


def select(standard, *, seconds=5., max_nodes=100000):
    # Import only the shared registry, not any solver, compiler or archived data.
    from workflow.contracts import BACKENDS, FAMILIES
    start = time.monotonic()
    if {b for _, b, _, _ in ROUTES} != set(BACKENDS): raise ValueError('backend coverage mismatch')
    if any(BACKENDS[b] != m for _, b, m, _ in ROUTES): raise ValueError('route/method mismatch')
    features = extract(standard, seconds=seconds, max_nodes=max_nodes)
    config = ahp(); routes = assess(features)
    methods = rank(routes, config['weights'], FAMILIES)
    unresolved = all_unknown_tie(methods)
    best = None if unresolved else next((m for m in methods if m['score'] is not None), None)
    selected = next((r for r in routes if best and r['route'] == best['best_route']), None)
    # Perturb one weight at a time. This measures decision sensitivity, not accuracy.
    sensitivity = []
    for criterion in CRITERIA:
        for factor in (.8, 1.2):
            weights = dict(config['weights']); weights[criterion] *= factor
            total = sum(weights.values()); weights = {k:v/total for k,v in weights.items()}
            copies = [dict(r) for r in routes]
            trial = rank(copies, weights, FAMILIES)
            winner = None if all_unknown_tie(trial) else next((r['method'] for r in trial if r['score'] is not None), None)
            sensitivity.append(dict(criterion=criterion, factor=factor, selected_method=winner))
    provenance = fingerprint()
    if time.monotonic()-start > seconds:
        from .features import FeatureLimit
        raise FeatureLimit('selection_total_budget')
    alternatives = [m for m in methods if m['score'] and (not best or m['method'] != best['method'])]
    robust = bool(best) and all(best['score']['lower'] > m['score']['upper'] for m in alternatives)
    return dict(schema_version='finite-q-selection/1', status='unclassified' if unresolved else 'selected' if best else 'unsupported_input',
        policy_version=VERSION, rules_version=RULE_VERSION, provenance=provenance,
        features=features, ahp=config, routes=routes, ranking=methods,
        selected_method=best['method'] if best else None,
        selected_route=best['best_route'] if best else None,
        reason=selected['reason'] if selected else 'All methods have identical unknown score intervals; display order is not a classification' if unresolved else 'All declared structural routes rejected this representation',
        unclassified_reason='all_methods_unknown_tied' if unresolved else None,
        suggested_methods=list(FAMILIES) if unresolved else [],
        ranking_is_tie_break_only=unresolved,
        unknown_criteria=[k for k in CRITERIA if selected and not selected['criteria'][k]['known']],
        interval_dominates_alternatives=robust,
        weight_sensitivity=sensitivity,
        stable_under_weight_perturbation=bool(best) and all(r['selected_method'] == best['method'] for r in sensitivity),
        scoring=dict(scale='fixed [0,1]', ideal=[1,1,1,1], anti_ideal=[0,0,0,0],
                     weighting='v_j=w_j*s_j; Euclidean distance',
                     ordering='largest lower bound, then smallest interval width, then stable identifier',
                     success_probability=False, proof_search_performed=False),
        elapsed_seconds=time.monotonic()-start,
        limitations=['Structural priority only; no success or runtime prediction',
                     'Unknown definitions/conditions are retained; ranking is not mathematical impossibility',
                     'Construction, singularity, endpoints and original Lean verification remain necessary'])
