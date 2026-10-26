"""Independent exact single-base q-summation and q-Ore core built on P1.

No benchmark membership, theorem target, Lean source, or proof emitter is used.
The public solve() isolates every symbolic call in a time-bounded process.
"""
import argparse
from dataclasses import asdict, dataclass
import hashlib
import json
import math
import multiprocessing as mp
import os
from pathlib import Path
import re
import signal
import sys
import time
import sympy as s

from expressions import expression, shift_ratio, rationalize, n, k, q, Q, X
from qgosper import Budget, UnsupportedDomain, antidifference, coefficient_field
from qparameterized import solve as parameterized
from zeilberger import search as zeilberger


@dataclass(frozen=True)
class CoreBudget(Budget):
    max_order: int | None = None
    max_states: int = 128

    def validate(self):
        if isinstance(self.seconds, bool) or not math.isfinite(self.seconds) or self.seconds <= 0:
            raise ValueError('seconds must be a finite positive number')
        for name in ('max_unknowns', 'max_normal_form_degree', 'max_states'):
            value = getattr(self, name)
            if type(value) is not int or value < 1:
                raise ValueError(name+' must be a positive integer')
        if self.max_order is not None and (type(self.max_order) is not int or self.max_order < 0):
            raise ValueError('max_order must be nonnegative or null')


def rational_input(node):
    """Exact arithmetic trees only; never evaluate expression strings as code."""
    if type(node) is int:
        return s.Integer(node)
    if isinstance(node, str) and re.fullmatch(r'[A-Za-z][A-Za-z0-9_]*', node):
        if node in ('n', 'k'):
            raise UnsupportedDomain('ratio inputs use Q=q^n and X=q^k, not raw indices n/k')
        return {'q':q, 'Q':Q, 'X':X}.get(node, s.Symbol(node))
    if not isinstance(node, list) or len(node) < 2:
        raise ValueError('exact integer/symbol/arithmetic tree required')
    op, *children = node
    if op == 'pow':
        if len(children) != 2 or type(children[1]) is not int:
            raise UnsupportedDomain('rational shift powers must be integer literals')
        base = rational_input(children[0])
        if base == 0 and children[1] < 0:
            raise ValueError('zero denominator')
        return base**children[1]
    args = list(map(rational_input, children))
    if op == 'add':
        return s.Add(*args)
    if op == 'mul':
        return s.Mul(*args)
    if op == 'neg' and len(args) == 1:
        return -args[0]
    if op in ('sub', 'div') and len(args) == 2:
        if op == 'div' and args[1] == 0:
            raise ValueError('zero denominator')
        return args[0]-args[1] if op == 'sub' else args[0]/args[1]
    raise ValueError('unsupported rational operator: '+str(op))


def denominators(values):
    return sorted({str(s.factor(s.fraction(s.cancel(v))[1])) for v in values
                   if s.fraction(s.cancel(v))[1] != 1})


def compute(request, budget):
    if not isinstance(request, dict) or set(request) != {'schema_version','solver','input'}:
        raise ValueError('only schema_version, solver and input are accepted; no targets or proof hints')
    if type(request['schema_version']) is not int or request['schema_version'] != 1:
        raise ValueError('unsupported schema version')
    solver, data = request['solver'], request['input']
    if solver == 'rational_omega':
        from qomega import compute as omega_compute
        return omega_compute(data,budget,rational_input)
    if solver == 'difference_equation':
        from qplde import compute as plde_compute
        return plde_compute(data,budget,rational_input)
    if solver == 'difference_system':
        from qpisigma_system import compute as system_compute
        return system_compute(data,budget,rational_input)
    if solver == 'finite_difference_ring':
        from qfinite import compute as finite_compute
        return finite_compute(data,budget,rational_input)
    if solver == 'difference_field':
        from qpisigma import compute as field_compute
        return field_compute(data,budget,rational_input)
    if solver == 'difference_ring':
        from qdifference import compute as difference_compute
        return difference_compute(data,budget,rational_input)
    if solver == 'q_ore':
        from ore_core import compute as ore_compute
        return ore_compute(data,budget,rational_input)
    if solver == 'q_zeilberger_joint':
        from qjoint import compute as joint_compute
        return joint_compute(data,budget,rational_input)
    if solver in ('q_holonomic','parameterized_q_system'):
        from qholonomic import compute as matrix_compute
        return matrix_compute(solver,data,budget,rational_input)
    if solver not in ('q_gosper', 'q_zeilberger', 'parameterized_q_gosper'):
        raise ValueError('unsupported core solver')
    if not isinstance(data, dict):
        raise ValueError('input must be an object')
    F = None
    if set(data) == {'summand'} and solver != 'parameterized_q_gosper':
        # This is the existing mathematical expression IR, not a Lean frontend.
        F = expression(data['summand'])
        if F.has(s.Float, s.nan, s.zoo, s.oo, -s.oo):
            raise UnsupportedDomain('finite exact symbolic summand required')
        if F == 0:
            return dict(status='constructed', solver=solver,
                        result=dict(kind='zero_summand', certificate='0', rational_residual='0'),
                        domain=dict(specialization_policy='identically zero input'))
        V = rationalize(shift_ratio(F, k))
        U = rationalize(shift_ratio(F, n)) if solver == 'q_zeilberger' else None
        rhs = None
    else:
        expected = {'k_shift'} | ({'n_shift'} if solver == 'q_zeilberger' else
                                  {'rhs_basis'} if solver == 'parameterized_q_gosper' else set())
        if set(data) != expected:
            raise ValueError('unexpected input fields for '+solver)
        V = rational_input(data['k_shift'])
        U = rational_input(data['n_shift']) if solver == 'q_zeilberger' else None
        rhs = data.get('rhs_basis')
        if solver == 'parameterized_q_gosper':
            if not isinstance(rhs, list) or not rhs:
                raise ValueError('nonempty rhs_basis required')
            rhs = list(map(rational_input, rhs))
    inputs = [V]+([U] if U is not None else [])+(rhs or [])
    for value in inputs:
        coefficient_field(value, X, q)
    if V == 0 or U == 0:
        raise ValueError('nonzero summand shift ratios required')
    if solver == 'q_zeilberger':
        raw = zeilberger(U, V, max_order=budget.max_order, min_order=0, budget=budget)
    elif solver == 'parameterized_q_gosper':
        raw = parameterized(V, rhs, X, q, budget)
    else:
        raw = antidifference(V.subs(X, X/q), X, q, budget)
        if raw['status'] == 'constructed':
            raw['certificate'] = str(raw['antidifference_ratio'])
            raw['antidifference_ratio'] = str(raw['antidifference_ratio'])
    status = {'no_q_hypergeometric_antidifference':'no_solution_in_class',
              'no_relation_in_joint_system':'no_relation_in_declared_basis'}.get(raw['status'],raw['status'])
    result = dict(status=status, solver=solver,
                  normalized_input=dict(k_shift=str(V), **({'n_shift':str(U)} if U is not None else {}),
                                        **({'rhs_basis':list(map(str,rhs))} if rhs is not None else {})),
                  result=raw)
    outputs = []
    if raw['status'] == 'constructed':
        symbols = {str(t): t for t in set().union(*(v.free_symbols for v in inputs), {q,Q,X})}
        parse = lambda value: s.sympify(value, locals=symbols)
        R = parse(raw['certificate'])
        outputs.append(R)
        if F is not None:
            # Compact endpoint expression only, with no assertion about a sum's domain.
            result['certificate_term_expression'] = str(R.subs({X:q**k, Q:q**n})*F)
        if solver == 'q_zeilberger':
            pcs = list(map(parse, raw['primitive_relation']['coefficients']))
            outputs += pcs+[parse(raw['primitive_relation']['certificate'])]
            result['operator'] = dict(variable='n', shift='n -> n+1; Q -> q*Q',
                                      order=raw['order'], coefficients=raw['primitive_relation']['coefficients'],
                                      leading_coefficient=raw['primitive_relation']['leading_coefficient'])
            if F is not None:
                result['operator_certificate_term_expression'] = str(
                    parse(raw['primitive_relation']['certificate']).subs({X:q**k,Q:q**n})*F)
    result['domain'] = dict(coefficient_field='QQ(q, Q, other independent parameters)(X)',
        base='q is an indeterminate; characteristic zero',
        normalized_input_denominators=denominators(inputs), output_denominators=denominators(outputs),
        specialization_policy='generic rational-function result only; special parameter values not checked',
        negative_result_scope='specified rational shift field and ansatz; never impossibility of the original identity')
    return result


def _worker(request, budget, connection):
    from ore import OreResourceLimit
    if hasattr(os,'setsid'):os.setsid()
    try:
        result = compute(request, budget)
    except OreResourceLimit as exc:
        result = dict(status='resource_exhausted', reason=str(exc))
    except UnsupportedDomain as exc:
        result = dict(status='unsupported_domain', reason=str(exc))
    except ValueError as exc:
        result = dict(status=('unsupported_domain' if str(exc).startswith('unsupported_domain:') else
            'unsupported_input' if str(exc).startswith(
            ('representation_gap:', 'unsupported_expression', 'unsupported_structure:')) else 'invalid_input'), reason=str(exc))
    except Exception as exc:
        result = dict(status='implementation_error', reason=type(exc).__name__+': '+str(exc))
    try:
        connection.send(result)
    finally:
        connection.close()


def solve(request, budget=CoreBudget()):
    """Hard timeout includes factorization, normalization and exact linear algebra."""
    budget.validate()
    payload = json.dumps(request, sort_keys=True, ensure_ascii=False)
    started = time.monotonic()
    context = mp.get_context('spawn')
    parent, child = context.Pipe(duplex=False)
    process = context.Process(target=_worker, args=(request, budget, child))
    process.start()
    child.close()
    try:
        if parent.poll(max(0, budget.seconds-(time.monotonic()-started))):
            try:
                result = parent.recv()
            except EOFError:
                result = dict(status='worker_failed', reason='symbolic process exited without a result')
        else:
            result = dict(status='resource_exhausted', reason='wall-clock budget exhausted')
    finally:
        if process.is_alive():
            # A number-field solve can have a synchronous PARI child. Keep it
            # in the worker's process group so a hard budget also stops it.
            if hasattr(os,'killpg'):
                try:os.killpg(process.pid,signal.SIGTERM)
                except ProcessLookupError:pass
            process.terminate()
        process.join(timeout=1)
        if process.is_alive():
            process.kill()
            process.join()
        parent.close()
    sources = [Path(__file__), *[Path(__file__).with_name(p) for p in
               ('qgosper.py','qparameterized.py','zeilberger.py','expressions.py','ore.py','ore_core.py','qjoint.py',
                'qrational_system.py','qholonomic.py','qdifference.py','qpisigma.py','qfinite.py','qpisigma_system.py',
                'qplde.py','qnumberfield.py','qconstant.py','qomega.py')]]
    result.update(schema_version=1, request_sha256=hashlib.sha256(payload.encode()).hexdigest(),
        elapsed_seconds=round(time.monotonic()-started,6), budget=asdict(budget),
        source_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},
        sympy_version=s.__version__, python_version=sys.version.split()[0],
        output_scope='local symbolic certificate; finite-sum boundaries and initial values not discharged',
        original_identity_proved=False, benchmark_files_read=0)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--seconds', type=float, default=30)
    parser.add_argument('--max-order', type=int, default=None)
    parser.add_argument('--max-unknowns', type=int, default=10000)
    parser.add_argument('--max-normal-form-degree', type=int, default=10000)
    parser.add_argument('--max-states', type=int, default=128)
    args = parser.parse_args()
    result = solve(json.loads(args.input.read_text()), CoreBudget(
        seconds=args.seconds, max_order=args.max_order, max_unknowns=args.max_unknowns,
        max_normal_form_degree=args.max_normal_form_degree,max_states=args.max_states))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('status','elapsed_seconds','original_identity_proved')},ensure_ascii=False))
    return 1 if result['status'] in ('implementation_error','worker_failed','invalid_input') else 0


if __name__ == '__main__':
    raise SystemExit(main())
