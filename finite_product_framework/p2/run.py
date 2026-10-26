#!/usr/bin/env python3
"""Native train-only P2 entry: definition-driven Cauchy coefficient extraction.

The ID selects a frozen input, never a proof. No other method solver is invoked.
Foundational Gaussian lemmas are shared explicitly, without copying their proofs.
Symbolic construction and Lean replay are separate, persisted stages.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

import sympy as sp

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
if str(HERE.parent) not in sys.path:
    sys.path.append(str(HERE.parent))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def lean(path, env, *args):
    result = subprocess.run(['lake', 'env', 'lean', *args, str(path)],
                            cwd=ROOT/'project', env=env, capture_output=True,
                            text=True, timeout=180)
    return {'exit_code': result.returncode, 'output': result.stdout + result.stderr}


def environment(work):
    from workflow.preprocessed import environment as shared_environment
    shared=shared_environment(work,'p2')
    if shared is not None:return shared
    src, obj = work/'sources', work/'deps'
    (src/'Benchmark').mkdir(parents=True, exist_ok=True)
    (obj/'Benchmark').mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env['LEAN_PATH'] = str(obj)
    origin = ROOT/'benchmark/lean/Benchmark/Definitions.lean'
    snapshot = src/'Benchmark/Definitions.lean'
    snapshot.write_bytes(origin.read_bytes())
    result = lean(snapshot, env, '-R', str(src), '-o', str(obj/'Benchmark/Definitions.olean'))
    if result['exit_code']:
        raise ValueError('dependency_compile_failed: ' + result['output'])
    evidence = [{'path': str(origin.relative_to(ROOT)), 'sha256': sha(origin)}]
    # Frozen representation definitions only. Never load Batch4Proofs or a target theorem.
    origin = ROOT/'benchmark/lean/Benchmark/Batch4Definitions.lean'
    declarations = []
    for name in ('fineC', 'eulerProductSeries', 'fineA'):
        match = re.search(r'(?m)^def '+name+r'\b[^\n]*(?:\n[ \t]+[^\n]*)*\n', origin.read_text())
        if match is None:
            raise ValueError('dependency_compile_failed: missing definition '+name)
        declarations.append(match.group())
        evidence.append({'path': str(origin.relative_to(ROOT)), 'sha256': sha(origin),
                         'loaded_declaration': name,
                         'declaration_sha256': hashlib.sha256(match.group().encode()).hexdigest()})
    snapshot = src/'Benchmark/P2Atoms.lean'
    snapshot.write_text('import Benchmark.Definitions\n'
        'import Mathlib.RingTheory.PowerSeries.Basic\n'
        'namespace FiniteQBenchmark\nnoncomputable section\n'
        'variable {K : Type*} [Field K]\n'+'\n'.join(declarations)+
        '\nend\nend FiniteQBenchmark\n')
    result = lean(snapshot, env, '-R', str(src), '-o', str(obj/'Benchmark/P2Atoms.olean'))
    if result['exit_code']:
        raise ValueError('dependency_compile_failed: '+result['output'])
    # Share only foundational Gaussian coefficient lemmas, never a P1 solver.
    for module, relative in [('Auxiliary', 'benchmark/lean/Benchmark/Auxiliary.lean'),
                             ('Gaussian', 'benchmark/lean/Benchmark/Gaussian.lean'),
                             ('GaussianRules', 'finite_product_framework/p1/lean/GaussianRules.lean')]:
        origin = ROOT/relative
        snapshot = src/'Benchmark'/f'{module}.lean'
        snapshot.write_bytes(origin.read_bytes())
        result = lean(snapshot, env, '-R', str(src), '-o', str(obj/'Benchmark'/f'{module}.olean'))
        if result['exit_code']:
            raise ValueError('dependency_compile_failed: '+result['output'])
        evidence.append({'path':relative,'sha256':sha(origin)})
    return env, evidence


def assemble(*parts):
    imports, body = [], []
    for part in parts:
        for line in part.splitlines():
            if line.startswith('import '):
                if line not in imports:
                    imports.append(line)
            else:
                body.append(line)
    return '\n'.join(imports+body)+'\n'


def proof_slot(source, proof):
    from workflow.preprocessed import slot as shared_slot
    shared=shared_slot(source,proof,('Benchmark.P2Atoms',))
    if shared is not None:return shared
    pattern = r'(?m)^  sorry\s*$'
    if len(re.findall(pattern, source)) != 1:
        raise ValueError('unsupported_declaration: expected exactly one deferred proof')
    # Preserve the complete original declaration; substitute definition-only dependencies.
    source = re.sub(r'(?m)^import Benchmark\.\w+$', 'import Benchmark.P2Atoms', source)
    return re.sub(pattern, lambda _: proof.rstrip(), source)


def rules_text():
    return assemble(*[(HERE/'lean'/name).read_text()
                      for name in ('Coefficient.lean', 'Polynomial.lean', 'Lift.lean')])


def preparation(reverse=False, depth=1, view='series'):
    # These are representation and algebra rules, not identity-specific proof scripts.
    if view not in ('series', 'finite', 'polynomial'):
        raise ValueError('unsupported coefficient view')
    lines = ['  classical', '  p2_goals']
    if reverse:
        lines.append('  all_goals symm')
    if view == 'polynomial':
        lines += ['  all_goals p2_lift_polynomial',
                  '  all_goals apply Polynomial.ext', '  all_goals intro p2_degree',
                  '  all_goals cases p2_degree', '  all_goals p2_polynomial_coefficients']
    if view == 'finite':
        lines += ['  all_goals simp (config := { failIfUnchanged := false }) only [',
                  '    FiniteQBenchmark.rogersSzego, FiniteQBenchmark.phi, FiniteQBenchmark.phiTerm]']
    lines += ['  all_goals simp (config := { failIfUnchanged := false }) only [FiniteQBenchmark.fineA, FiniteQBenchmark.eulerProductSeries,',
              '    FiniteQBenchmark.fineC, FiniteQP2.coeff_mul_range, PowerSeries.coeff_mk,',
              '    FiniteQBenchmark.pochList, List.map_cons, List.map_nil,',
              '    List.prod_cons, List.prod_nil, mul_one, Finset.sum_mul, Finset.mul_sum]',
              '  all_goals p2_coefficients', '  all_goals p2_collect']
    for i in range(depth):
        lines += ['  all_goals p2_descend', '  all_goals p2_coefficients', '  all_goals p2_collect']
    lines += ['  all_goals simp (config := { failIfUnchanged := false }) only [div_eq_mul_inv, mul_inv_rev]']
    return '\n'.join(lines)+'\n'


def construct(raw):
    """Exact commutative-ring normalization, valid even at zero denominators.

    Inverse expressions are independent atoms, not rational-function variables:
    this deliberately does NOT use cancel(a/a)=1 or field_simp assumptions.
    """
    if 'goals' in raw:
        branches = [construct(g) for g in raw['goals']]
        passed = bool(branches) and all(b['status'] == 'constructed' for b in branches)
        return dict(status='constructed' if passed else 'coefficient_obligations_open',
                    algorithm='all-branch coefficient normalization', goals=branches,
                    goal_count=len(branches), closed_goal_count=sum(b['status']=='constructed' for b in branches),
                    denominator_cancellation=False, cross_method_dependencies=[])
    if 'unsupported_goal' in raw:
        return dict(status='unsupported_goal_shape', goal=raw['unsupported_goal'],
                    remaining_obligations=['Goal is not an equality after logical decomposition'])
    if raw=={'closed_by_preparation':True}:
        return dict(status='constructed',algorithm='definition/Cauchy normalization closed all goals; Lean replay required',
                    residual='0',denominator_cancellation=False)
    atoms = {}

    def convert(node):
        op = node['op']
        if op == 'atom':
            key = node['key']
            if key not in atoms:
                atoms[key] = {'symbol': 'v'+str(len(atoms)), 'display': node['display']}
            return sp.Symbol(atoms[key]['symbol'])
        if op == 'integer':
            return sp.Integer(node['value'])
        if op == 'neg':
            return -convert(node['arg'])
        if op == 'pow':
            return convert(node['arg'])**node['exponent']
        a, b = map(convert, node['args'])
        if op == 'HAdd.hAdd':
            return a+b
        if op == 'HSub.hSub':
            return a-b
        if op == 'HMul.hMul':
            return a*b
        raise ValueError('unsupported_expression: '+op)

    left, right = convert(raw['lhs']), convert(raw['rhs'])
    residual = sp.expand(left-right)
    return {'status': 'constructed' if residual == 0 else 'coefficient_mismatch',
            'algorithm': 'Cauchy coefficient extraction + exact polynomial normal form',
            'backend': 'SymPy '+sp.__version__, 'atoms': list(atoms.values()),
            'lhs_normal_form': str(sp.expand(left)), 'rhs_normal_form': str(sp.expand(right)),
            'residual': str(residual), 'denominator_cancellation': False}


def prove_source(source, work, env, *, max_depth=4):
    """Shared representation search; no identity IDs, parameter names or target answers."""
    rules = rules_text()
    exporter = (HERE/'lean/Export.lean').read_text()
    attempts = []
    plans = [(view, depth) for view in ('series', 'finite', 'polynomial') for depth in range(max_depth+1)]
    seen = set()
    saturated_views = set()
    for view, depth in plans:
        if view in saturated_views:
            continue
        # Coefficients on either side are expanded by simp. Orientation is immaterial.
        prep = preparation(depth=depth, view=view)
        file = work/'ExtractTarget.lean'
        file.write_text(assemble(rules, exporter, proof_slot(source, prep+'  p2_export')))
        result = lean(file, env)
        lines = [line.split('P2_JSON:', 1)[1] for line in result['output'].splitlines()
                 if 'P2_JSON:' in line]
        attempt = {'depth': depth, 'view': view, 'lean': result}
        attempts.append(attempt)
        if len(lines) != 1 or 'P2_EXPORT_ONLY' not in result['output']:
            if view == 'polynomial' and 'error: P2_POLYNOMIAL_DOMAIN:' in result['output']:
                attempt['representation_gap'] = True
                saturated_views.add(view)
            continue
        if len(re.findall(r'\berror:', result['output'])) != 1:
            continue
        raw = json.loads(lines[0])
        fingerprint = (view, json.dumps(raw, sort_keys=True))
        if fingerprint in seen:
            attempt['duplicate_residual'] = True
            # The same normal form after one further descent is a fixed point
            # for this view. Do not retry deeper identical preparations.
            saturated_views.add(view)
            continue
        seen.add(fingerprint)
        save(work/'lean_expression.json', raw)
        construction = construct(raw)
        attempt['construction'] = construction
        save(work/f'construction_{view}_{depth}.json', construction)
        save(work/'construction.json', construction)
        if construction['status'] != 'constructed':
            # Deeper sums may still normalize. Preserve the actual failure, no success fallback.
            continue
        namespaces = re.findall(r'^namespace\s+(\S+)', source, re.M)
        names = re.findall(r'^theorem\s+(\S+)', source, re.M)
        if len(names) != 1:
            raise ValueError('unsupported_declaration: one theorem required')
        theorem = '.'.join(namespaces+[names[0]])
        proof = work/'Proof.lean'
        proof.write_text(assemble(rules, proof_slot(source, prep+'  all_goals ring\n  done'))+
                         '\n#print axioms '+theorem+'\n')
        check = lean(proof, env)
        allowed = {'propext', 'Classical.choice', 'Quot.sound'}
        audit = re.search(re.escape("'"+theorem+"' depends on axioms: [")+r'([^\]]*)\]', check['output'])
        axioms = {s.strip() for s in audit.group(1).split(',') if s.strip()} if audit else None
        passed = check['exit_code'] == 0 and axioms is not None and axioms <= allowed
        return {'status': 'proved' if passed else 'lean_verification_failed',
                'branch': 'cauchy_coefficient', 'construction': construction,
                'proof_file': str(proof), 'proof_sha256': sha(proof),
                'lean': check, 'axioms': sorted(axioms) if axioms is not None else None,
                'plan': {'coefficient_rule': 'coeff_mul_range', 'sum_congruence_depth': depth, 'view':view,
                         'all_branches_required':True, 'cross_method_dependencies':[],
                         'shared_foundational_lemmas':['FiniteQP1.gaussian_adjacent'] if view=='polynomial' else [],
                         'polynomial_variables':[line.split('P2_POLYNOMIAL_VARIABLE:',1)[1]
                             for line in result['output'].splitlines() if 'P2_POLYNOMIAL_VARIABLE:' in line],
                         'algebra_rule': 'division-to-inverse; polynomial normalization'},
                'attempts': attempts, 'remaining_obligations': [] if passed else ['Lean replay / axiom audit']}
    return {'status': 'unsupported_or_unclosed_structure', 'attempts': attempts,
            'boundary': {'method':'coefficient','cross_method_dependencies':[],
                         'automatic_fallback':False},
            'remaining_obligations': ['Unclosed coefficient or goal obligations; see per-view, per-depth branch residuals. '
                                     'No recurrence, summation, kernel or Omega backend was invoked.']}


def load_target(identity):
    train = {r['id']: r for r in map(json.loads,
             (ROOT/'benchmark/splits/train.jsonl').read_text().splitlines())}
    plans = json.loads((ROOT/'finite_product_framework/research/train_a_methods/plans.json').read_text())
    ids = {r['id'] for r in plans['entries'] if r['primary_mechanism'] == 'P2'}
    if identity not in ids or identity not in train or train[identity]['family_id'] != 'A':
        raise ValueError('unsupported_input: requires one of the 62 P2 train statements')
    row = train[identity]
    path = ROOT/'benchmark'/row['lean_path']
    if sha(path) != row['lean_sha256']:
        raise ValueError('source_changed: frozen statement hash mismatch')
    return path, row


def run(identity, output_root=None):
    work = (Path(output_root) if output_root else HERE/'generated/runs')/identity
    work.mkdir(parents=True, exist_ok=True)
    report = {'schema_version': 1, 'identity': identity, 'status': 'started',
              'complete_train_proofs': 0, 'test_files_read': 0, 'preset_proof_fallback': False}
    try:
        path, row = load_target(identity)
        source = path.read_text()
        report['source'] = {'path': str(path.relative_to(ROOT)), 'sha256': sha(path)}
        env, dependencies = environment(work)
        report['dependencies'] = dependencies
        report['verification'] = prove_source(source, work, env)
        report['status'] = report['verification']['status']
        if sha(path) != report['source']['sha256']:
            raise ValueError('source_changed: during proof generation')
        for entry in dependencies:
            if sha(ROOT/entry['path']) != entry['sha256']:
                raise ValueError('source_changed: dependency during proof generation')
        if report['status'] == 'proved':
            report['complete_train_proofs'] = 1
        report['remaining_obligations'] = report['verification']['remaining_obligations']
    except Exception as exc:
        report.update(status='pipeline_incomplete', error=f'{type(exc).__name__}: {exc}',
                      complete_train_proofs=0, remaining_obligations=['Resolve reported failure'])
    save(work/'report.json', report)
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--identity', required=True)
    args = parser.parse_args()
    report = run(args.identity)
    print(json.dumps({k: v for k, v in report.items() if k not in ('verification', 'dependencies')},
                     ensure_ascii=False, indent=2))
    sys.exit(0 if report['status'] == 'proved' else 2)
