"""Exact graded Elliott-rational Omega by two-block partial fractions.

Input denominators are geometric factors, not proof hints. Strictly positive
external grading specifies their expansion and makes every graded coefficient
a finite Laurent polynomial in the auxiliary variables. No series sampling is
used by this solver. See ../macmahon/RATIONAL_OMEGA.md for the contract.
"""
import sympy as s
from ore import OreResourceLimit
from qgosper import UnsupportedDomain


def monomial(value, symbols):
    """Return rational coefficient and integer exponents; reject other forms."""
    powers = value.as_powers_dict()
    exponents = []
    coefficient = value
    for x in symbols:
        e = powers.get(x, s.S.Zero)
        if not e.is_Integer:
            raise UnsupportedDomain('integer Laurent exponents required')
        exponents.append(int(e))
        coefficient /= x**e
    coefficient = s.cancel(coefficient)
    if coefficient.is_Rational is not True:
        raise UnsupportedDomain('Laurent polynomial with rational coefficients required')
    return coefficient, exponents


def prepare(data, budget, parse):
    if not isinstance(data, dict) or set(data) != {
            'numerator', 'denominator_monomials', 'grading', 'eliminate'}:
        raise ValueError('Omega requires numerator, denominator_monomials, grading, eliminate only')
    grading, eliminate = data['grading'], data['eliminate']
    if not isinstance(grading, dict) or not grading:
        raise ValueError('nonempty external grading required')
    weights = {}
    for name, weight in grading.items():
        x = parse(name)
        if not isinstance(x, s.Symbol) or type(weight) is not int or weight < 0:
            raise ValueError('grading must assign nonnegative integer weights to symbols')
        weights[x] = weight
    if not any(weights.values()):
        raise ValueError('at least one positive external weight required')
    if not isinstance(eliminate, list) or not eliminate:
        raise ValueError('nonempty elimination list required')
    operations = []
    for row in eliminate:
        if not isinstance(row, dict) or set(row) != {'variable', 'operator'}:
            raise ValueError('elimination row requires variable and operator only')
        z = parse(row['variable'])
        if not isinstance(z, s.Symbol) or row['operator'] not in ('ge', 'ct'):
            raise ValueError('auxiliary symbol and ge/ct operator required')
        if z in weights or z in [v for v, _ in operations]:
            raise ValueError('auxiliary variables must be distinct and disjoint from external variables')
        operations.append((z, row['operator']))
    factors = data['denominator_monomials']
    if not isinstance(factors, list):
        raise ValueError('denominator_monomials must be a list (repetitions allowed)')
    if len(factors) + len(operations) > budget.max_states:
        raise OreResourceLimit('Omega input factor/variable count exceeds max_states')
    symbols = list(weights) + [z for z, _ in operations]
    values = [parse(data['numerator']), *map(parse, factors)]
    if any(v.free_symbols - set(symbols) for v in values):
        raise ValueError('every symbol must be declared in grading or eliminate')
    numerator = s.expand(values[0])
    terms = s.Add.make_args(numerator)
    if len(terms) > budget.max_unknowns:
        raise OreResourceLimit('Omega numerator term count exceeds max_unknowns')
    for term in terms:
        _, exps = monomial(term, symbols)
        if any(abs(e) > budget.max_normal_form_degree for e in exps):
            raise OreResourceLimit('Omega Laurent exponent exceeds max_normal_form_degree')
    for value in values[1:]:
        c, exps = monomial(value, symbols)
        if c == 0:
            raise ValueError('zero is not a denominator monomial; omit the factor')
        if sum(weights[x]*exps[i] for i, x in enumerate(weights)) <= 0:
            raise UnsupportedDomain('every geometric monomial must have strictly positive external grade')
        if any(abs(e) > budget.max_normal_form_degree for e in exps):
            raise OreResourceLimit('Omega denominator exponent exceeds max_normal_form_degree')
    return s.cancel(numerator/s.prod(1-v for v in values[1:])), weights, operations


def homogeneous_weight(value, weights):
    """All auxiliary variables have weight zero. Used after exact factoring."""
    grades = set()
    for term in s.Add.make_args(s.expand(value)):
        powers = term.as_powers_dict()
        grades.add(sum(w*powers.get(x, 0) for x, w in weights.items()))
    if len(grades) != 1:
        raise UnsupportedDomain('intermediate factor coefficient is not grade homogeneous')
    return next(iter(grades))


def factor_side(factor, z, weights):
    """Certify one-sided z expansion, including cyclotomic/repeated factors.

    Relative to the constant (leading) coefficient, every other coefficient
    must have positive external grade. The inverse then contains only
    nonnegative (nonpositive after removing z**degree) powers of z.
    """
    p = s.Poly(factor, z)
    if p.degree() == 0:
        return 'independent'
    if len(p.terms()) == 1:
        return 'negative'  # z powers; independent multiplier is harmless.
    grades = {int(e[0]): homogeneous_weight(c, weights) for e, c in p.terms()}
    d = p.degree()
    if 0 in grades and all(g > grades[0] for j, g in grades.items() if j != 0):
        return 'positive'
    if all(g > grades[d] for j, g in grades.items() if j != d):
        return 'negative'
    raise UnsupportedDomain('intermediate denominator has no certified one-sided graded expansion')


def eliminate_one(value, z, operator, weights, budget):
    num, den = s.fraction(s.cancel(value))
    if max(s.degree(num, z) if num != 0 else 0, s.degree(den, z)) > budget.max_normal_form_degree:
        raise OreResourceLimit('Omega polynomial degree exceeds max_normal_form_degree')
    scalar, factors = s.factor_list(den)
    if sum(m for _, m in factors) > budget.max_states:
        raise OreResourceLimit('Omega factored denominator exceeds max_states')
    positive, negative, independent = s.S.One, s.S.One, scalar
    classified = []
    for factor, multiplicity in factors:
        multiplicity = int(multiplicity)
        side = factor_side(factor, z, weights)
        classified.append(dict(factor=str(factor), multiplicity=multiplicity, side=side))
        if side == 'positive':
            positive *= factor**multiplicity
        elif side == 'negative':
            negative *= factor**multiplicity
        else:
            independent *= factor**multiplicity
    parameters = sorted((num.free_symbols | den.free_symbols)-{z}, key=str)
    field = s.QQ.frac_field(*parameters) if parameters else s.QQ
    poly = lambda v: s.Poly(v, z, domain=field)
    dp, dm = poly(positive), poly(negative)
    polynomial, remainder = poly(num/independent).div(dp*dm)
    if dp.degree() == 0:
        a = poly(0)
    else:
        # No roots or guessed degree: CRT gives the unique proper positive block.
        a = (remainder*dm.invert(dp)).rem(dp)
    b = (remainder-a*dm).exquo(dp)
    if a.degree() >= dp.degree() or b.degree() >= dm.degree():
        raise ArithmeticError('partial fraction properness invariant failed')
    p, a, b = [t.as_expr() for t in (polynomial, a, b)]
    dp, dm = dp.as_expr(), dm.as_expr()
    if s.cancel(value-p-a/dp-b/dm) != 0:
        raise ArithmeticError('partial fraction reconstruction failed')
    pt = s.cancel(p+a/dp)
    point = 1 if operator == 'ge' else 0
    result = s.cancel(pt.subs(z, point))
    if result.has(s.nan, s.zoo, s.oo, -s.oo):
        raise UnsupportedDomain('projection evaluation has an unresolved specialization pole')
    if result.has(z):
        raise ArithmeticError('auxiliary variable survived elimination')
    if sum(len(s.Add.make_args(s.expand(v))) for v in s.fraction(result)) > budget.max_unknowns:
        raise OreResourceLimit('Omega output term count exceeds max_unknowns')
    return result, dict(variable=str(z), operator=operator, input=str(value),
        factors=classified, polynomial=str(p), positive_numerator=str(a),
        positive_denominator=str(dp), negative_numerator=str(b),
        negative_denominator=str(dm), output=str(result), rational_residual='0')


def compute(data, budget, parse):
    value, weights, operations = prepare(data, budget, parse)
    source = value
    steps = []
    for z, operator in operations:
        value, step = eliminate_one(value, z, operator, weights, budget)
        steps.append(step)
    return dict(status='constructed', solver='rational_omega',
        normalized_input=str(source), result=dict(value=str(s.factor(value)), steps=steps),
        domain=dict(coefficient_field='QQ(external indeterminates)',
            expansion='each 1/(1-M) expands as sum(M**j,j>=0); grade(M)>0',
            grading={str(x): w for x, w in weights.items()},
            scope='fixed finite dimension, positively graded Elliott-rational input',
            specialization_policy='formal generic result; parameter specialization requires a separate check',
            negative_result_scope='unsupported/resource status is never impossibility of an identity'))
