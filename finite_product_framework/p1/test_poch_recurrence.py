"""Source-to-kernel regressions for the product-interval recurrence exit."""
import copy
import json
import os
import sys
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parent)]
from core import CoreBudget
from proof_fixture import source_for
from general_summation import frontend, construct, synthesize
from lean_pipeline import extract
from workflow.contracts import accept_proof, sha


TARGET = '''(u v q : K) (n : ℕ) (hq : q ≠ 0) (hu : u ≠ 0)
    (hden : phiDefined [v] q n) :
    phi [u, q^(-(n : ℤ))] [v] q q n =
      u^n * poch (v/u) q n / poch v q n'''


def run(out):
    out.mkdir(parents=True, exist_ok=True)
    base = HERE.parent/'generated/recurrence_full_20261019/regression'
    manifest = json.loads((base/'environment_manifest.json').read_text())
    for p, digest in manifest['files'].items():
        assert sha(Path(p)) == digest, p
    env = dict(os.environ, LEAN_PATH=str(base/'environment/deps'))
    records = []
    (out/'validation.json').write_text(json.dumps(dict(status='running', records=[])))
    for name, target, expected in [
        ('renamed_parameters', TARGET, True),
        ('missing_domain', TARGET.replace('(hden : phiDefined [v] q n)', ''), False),
        ('wrong_initial', TARGET+' + 1', False),
    ]:
        work = out/name
        work.mkdir(exist_ok=True)
        source = source_for(target)
        (work/'source.lean').write_text(source)
        raw = extract(source, work, env)
        problem, model = frontend(raw, 'synthetic:'+name)
        result = construct(problem, CoreBudget(seconds=40, max_order=4))
        (work/'construction.json').write_text(json.dumps(result, indent=2))
        try:
            v = synthesize(source, model, result['construction'], work, env)
        except subprocess.TimeoutExpired as exc:
            v = dict(status='timeout_unverified', reason=str(exc))
        except ValueError as exc:
            if 'initial_value_mismatch:' not in str(exc):
                raise
            v = dict(status='initial_value_mismatch', reason=str(exc))
        (work/'verification.json').write_text(json.dumps(v, indent=2))
        passed = v['status'] != 'timeout_unverified' and ((v['status'] == 'proved') == expected)
        if expected and passed:
            info = dict(identity='synthetic:'+name, path=str(work/'source.lean'),
                        snapshot=str(work/'source.lean'), sha256=sha(work/'source.lean'),
                        theorem='CoreExitRegression.statement')
            accept_proof(dict(status='proved', original_identity_proved=True,
                              remaining_obligations=[], verification=v), info, work)
        records.append(dict(name=name, passed=passed, status=v['status']))
        print(records[-1], flush=True)
        bad = copy.deepcopy(result['construction'])
        bad['sides'][0]['certificates'][0] += '+1'
        try:
            from general_sum_emit import emit
            emit(model, bad)
            rejected = False
        except ValueError:
            rejected = True
        records.append(dict(name=name+'_tampered', passed=rejected))
        bad = copy.deepcopy(result['construction'])
        bad['sides'][0]['seed_certificates'][0] += '+1'
        try:
            emit(model, bad)
            rejected = False
        except ValueError:
            rejected = True
        records.append(dict(name=name+'_tampered_seed', passed=rejected))
    result = dict(status='passed' if all(r['passed'] for r in records) else 'failed',
                  records=records, test_split_read=False, train_batch_run=False)
    (out/'validation.json').write_text(json.dumps(result, indent=2))
    return result


if __name__ == '__main__':
    result = run(HERE.parent/'generated/recurrence_full_20261019/adversarial')
    sys.exit(result['status'] != 'passed')
