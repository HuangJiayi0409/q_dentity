"""Independent local algebraic replay; not a Lean or original-theorem checker."""
import sympy as s
from core import CoreBudget, rational_input
from qdifference import rational_read
from qomega import prepare


def certified_side(factor, z, weights):
    # Independently inspect the lowest external graded part. It must have
    # only z**0 (positive block) or z**degree (negative block).
    p = s.Poly(factor, z)
    if p.degree() == 0:
        return 'independent'
    graded = []
    for (j,), coefficient in p.terms():
        for term in s.Add.make_args(s.expand(coefficient)):
            grade = sum(w*term.as_powers_dict().get(x, 0) for x, w in weights.items())
            graded.append((grade, j))
    least = min(g for g, _ in graded)
    degrees = {j for g, j in graded if g == least}
    if degrees == {0}:
        return 'positive'
    if degrees == {p.degree()}:
        return 'negative'
    raise AssertionError('uncertified formal expansion')


def replay(request, response):
    source, weights, operations = prepare(request['input'], CoreBudget(), rational_input)
    assert response['status'] == 'constructed'
    allowed = source.free_symbols | set(weights) | {z for z, _ in operations}
    def read(text):
        v = rational_read(text)
        assert not v.free_symbols-allowed, 'undeclared certificate symbol'
        assert not v.has(s.zoo, s.nan, s.Float, s.oo, -s.oo)
        return v
    assert s.cancel(read(response['normalized_input'])-source) == 0
    steps = response['result']['steps']
    assert len(steps) == len(operations), 'missing elimination step'
    for step, (z, op) in zip(steps, operations):
        assert (step['variable'], step['operator']) == (str(z), op)
        assert s.cancel(read(step['input'])-source) == 0
        p, a, dp, b, dm = [read(step[key]) for key in (
            'polynomial','positive_numerator','positive_denominator',
            'negative_numerator','negative_denominator')]
        assert dp != 0 and dm != 0
        s.Poly(p, z)
        assert s.Poly(a, z).degree() < s.Poly(dp, z).degree(), 'positive fraction is improper'
        assert s.Poly(b, z).degree() < s.Poly(dm, z).degree(), 'negative fraction is improper'
        positive = s.S.One
        negative = s.S.One
        all_factors = s.S.One
        for row in step['factors']:
            factor, m = read(row['factor']), row['multiplicity']
            assert type(m) is int and m > 0
            side = certified_side(factor, z, weights)
            assert row['side'] == side, 'wrong expansion direction'
            all_factors *= factor**m
            if side == 'positive':positive *= factor**m
            if side == 'negative':negative *= factor**m
        ratio = s.cancel(s.fraction(s.cancel(source))[1]/all_factors)
        assert ratio.is_Rational and ratio != 0, 'factorization not bound to input'
        assert s.cancel(dp-positive) == s.cancel(dm-negative) == 0
        assert s.cancel(source-p-a/dp-b/dm) == 0, 'wrong decomposition'
        target = s.cancel(p+a/dp).subs(z, 1 if op == 'ge' else 0)
        source = read(step['output'])
        assert not source.has(z)
        assert s.cancel(source-target) == 0, 'wrong projection'
    assert s.cancel(read(response['result']['value'])-source) == 0, 'wrong final result'
    return len(steps)
