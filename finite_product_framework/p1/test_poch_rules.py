"""Kernel regressions for nonzero matching and division-free shifts."""
import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parent)]
from proof_fixture import source_for
from lean_pipeline import verify_proof
from workflow.contracts import sha

CASES = [
    ('literal_shift_two', '(c q : K) (k N : ℕ) (h : k+3 ≤ N) '
     '(hd : poch c q N ≠ 0) : 1-c*q^(k+2) ≠ 0',
     '  have pa : c*q^2 = c*q^2 := by\n'
     '    simp only [pow_one]\n'
     '    all_goals first | (ring; done) | (field_simp <;> ring)\n'
     '  have hp := FiniteQShift.shifted_ne c q 2 (k+1) N (by omega) hd\n'
     '  have hf := FiniteQShift.factor_ne (c*q^2) q k (k+1) (by omega) hp\n'
     '  convert hf using 1 <;> simp only [pow_add] <;> ring', True),
    ('constant_inner_power', '(q : K) (n : ℕ) (ptComposite : (q^2)^n - 1 ≠ 0) : '
     '((q^n)^2-1)*((q^n)^2-1)⁻¹ = 1',
     '  poch_normalize_powers\n  poch_orient_powers\n  poch_clear_denominators <;> ring', True),
    ('parameter_cancellation', '(a b c q : K) (k : ℕ) (hq : q ≠ 0) : '
     'poch (a*q*b*c⁻¹*q⁻¹) q k = poch (a*b*c⁻¹) q k',
     '  poch_normalize_arguments\n  all_goals ring_nf', True),
    ('opposite_factor', '(a b c x : K) (ptScalar : a*b + -1*c*x ≠ 0) : '
     '(x*c-a*b)*(x*c-a*b)⁻¹ = 1',
     '  poch_clear_denominators <;> ring', True),
    ('product_argument', '(a b c q x : K) (k : ℕ) '
     '(ptAtom : poch (a*b*(c^1)⁻¹*(q^1/x)) q k ≠ 0) : '
     'poch (a*q*b*x⁻¹*c⁻¹) q k * (poch (a*q*b*x⁻¹*c⁻¹) q k)⁻¹ = 1',
     '  poch_clear_denominators <;> ring', True),
    ('domain_transport', '(a q : K) (d k N : ℕ) (hd : d+k ≤ N) '
     '(hp : poch a q N ≠ 0) : poch (a*q^d) q k ≠ 0',
     '  exact FiniteQShift.shifted_ne a q d k N hd hp', True),
    ('vanishing_prefix', '(q : K) (d k : ℕ) : '
     'poch (q^d) q k * poch 1 q d = poch 1 q k * poch (q^k) q d',
     '  simpa only [one_mul] using (FiniteQShift.shift_cross (1 : K) q d k)', True),
    ('missing_nonzero', '(a b c x : K) : (x*c-a*b)*(x*c-a*b)⁻¹ = 1',
     '  poch_clear_denominators <;> ring', False),
]


# Support-dependent lengths must be discharged in the original context.
from expressions import n, k, q, Poch
from poch_local import normalize, NORMAL
import sympy as s
_a = s.Symbol('a')
_support_expressions = [Poch(_a/q, q, n+1-k), (1-_a/q)*Poch(_a, q, n-k)]
_support_tactic = normalize(_support_expressions, {'a':'a','q':'q','n':'n','k':'k'}, 2)
_support_tactic += '  all_goals try simp only [poch_zero]\n  all_goals field_simp [hq] <;> ring\n'
for _name, _hypothesis, _expected in [('support_length', '(hkn : k ≤ n)', True),
                                      ('missing_support', '', False)]:
    CASES.append((_name, '(a q : K) (n k : ℕ) (hq : q ≠ 0) '+_hypothesis+
                  ' : poch (a/q) q (n+1-k) = (1-a/q)*poch a q (n-k)',
                  _support_tactic, _expected))


_support_tail = [Poch(_a/q,q,n+2-k),
                 (1-_a/q)*Poch(_a,q,n-k)*(1-_a*q**(n-k))]
_support_tail_tactic = normalize(_support_tail, {'a':'a','q':'q','n':'n','k':'k'}, 2)
_support_tail_tactic += '  all_goals try simp only [poch_zero]\n  all_goals field_simp [hq] <;> ring\n'
CASES.append(('support_tail', '(a q : K) (n k : ℕ) (hq : q ≠ 0) (hkn : k ≤ n) : '
              'poch (a/q) q (n+2-k) = (1-a/q)*poch a q (n-k)*(1-a*q^n/q^k)',
              _support_tail_tactic, True))


_factor_tactic = normalize([Poch(q,q,n), Poch(q,q,n+2)],
                           {'q':'q','n':'n','k':'k'}, 2)
_factor_tactic += ('  all_goals\n    poch_normalize_powers\n'
                  '    poch_orient_powers\n    poch_clear_denominators <;> ring\n')
CASES.append(('split_denominator_evidence', '(q : K) (n : ℕ) '
              '(ptAtom : poch q q (n+2) ≠ 0) : '
              '(1-q^(n+1)-q^(n+2)+q^(2*n+3))*'
              '(1-q^(n+1)-q^(n+2)+q^(2*n+3))⁻¹ = 1', _factor_tactic, True))


def run(out=None):
    out = out or HERE.parent/'generated/recurrence_full_20261019/rules_regression'
    out.mkdir(parents=True, exist_ok=True)
    base = HERE.parent/'generated/recurrence_full_20261019/regression'
    manifest = json.loads((base/'environment_manifest.json').read_text())
    for path, digest in manifest['files'].items():
        assert sha(Path(path)) == digest, path
    env = dict(os.environ, LEAN_PATH=str(base/'environment/deps'))
    records = []
    for name, target, tactic, expected in CASES:
        work = out/name
        work.mkdir(exist_ok=True)
        source = source_for(target)
        (work/'source.lean').write_text(source)
        v = verify_proof(source, tactic, dict(kind='poch_rule_regression'), work, env,
                         extra_rules=((HERE/'lean/PochShiftRules.lean').read_text(),),
                         shared_rules=False, timeout=60)
        (work/'verification.json').write_text(json.dumps(v, indent=2))
        records.append(dict(name=name, status=v['status'],
                            passed=(v['status']=='proved') == expected))
        print(records[-1], flush=True)
    result = dict(status='passed' if all(r['passed'] for r in records) else 'failed',
                  records=records)
    (out/'validation.json').write_text(json.dumps(result, indent=2))
    return result


if __name__ == '__main__':
    sys.exit(run()['status'] != 'passed')
