"""Lift an actually constructed source recurrence and check every initial/tail."""
import copy
import json
import os
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parent)]
import sympy as s
from core import CoreBudget
from proof_fixture import source_for
from expressions import expression
from general_summation import frontend, construct, parse, lift, pieces, synthesize
from lean_pipeline import extract
from ore import multiply
from test_poch_recurrence import TARGET
from workflow.contracts import accept_proof, sha


def run(out=None):
    out = out or HERE.parent/'generated/recurrence_full_20261019/order_regression'
    out.mkdir(parents=True, exist_ok=True)
    base = HERE.parent/'generated/recurrence_full_20261019/regression'
    manifest = json.loads((base/'environment_manifest.json').read_text())
    for path, digest in manifest['files'].items():
        assert sha(Path(path)) == digest, path
    env = dict(os.environ, LEAN_PATH=str(base/'environment/deps'))
    source = source_for(TARGET)
    (out/'source.lean').write_text(source)
    raw = extract(source, out, env)
    problem, model = frontend(raw, 'synthetic:lifted_order_two')
    result = construct(problem, CoreBudget(seconds=40, max_order=4))
    c = copy.deepcopy(result['construction'])
    old = list(map(parse, c['coefficients']))
    multiplier = [s.S.NegativeOne, s.S.One]
    common = multiply(multiplier, old)
    for witness, row in zip(c['sides'], model['sides']):
        witness['seed_coefficients'] = list(witness['coefficients'])
        witness['seed_certificates'] = list(witness['certificates'])
        witness['multiplier'] = list(map(str, multiplier))
        if row['kind'] == 'sum':
            witness['certificates'] = list(map(str, lift(old,
                list(map(parse, witness['certificates'])),
                pieces(expression(row['expression'])), multiplier)))
        witness['coefficients'] = list(map(str, common))
    c['coefficients'] = list(map(str, common))
    c['order'] = len(common)-1
    (out/'construction.json').write_text(json.dumps(c, indent=2))
    status = dict(status='running', passed=False, order=c['order'])
    (out/'validation.json').write_text(json.dumps(status, indent=2))
    try:
        v = synthesize(source, model, c, out, env)
        (out/'verification.json').write_text(json.dumps(v, indent=2))
        status.update(status=v['status'], passed=v['status']=='proved')
        if status['passed']:
            info = dict(identity='synthetic:lifted_order_two', path=str(out/'source.lean'),
                        snapshot=str(out/'source.lean'), sha256=sha(out/'source.lean'),
                        theorem='CoreExitRegression.statement')
            status['acceptance'] = accept_proof(dict(status='proved',
                original_identity_proved=True, remaining_obligations=[], verification=v), info, out)
    except subprocess.TimeoutExpired as exc:
        status.update(status='timeout_unverified', reason=str(exc))
        (out/'verification.json').write_text(json.dumps(status, indent=2))
    (out/'validation.json').write_text(json.dumps(status, indent=2))
    print(json.dumps(status), flush=True)
    return status


if __name__ == '__main__':
    sys.exit(not run()['passed'])
