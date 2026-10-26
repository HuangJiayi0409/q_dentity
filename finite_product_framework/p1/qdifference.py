"""Parameterized telescoping in certified Laurent-product / polynomial-sum towers.

Base: QQ(q, independent constants)(X), sigma(X)=q*X. Product ratios are
base rational functions; sum increments are Laurent-polynomial expressions
in preceding extensions. No target, certificate or guessed degree is input.
See DIFFERENCE_CORE.md for completeness, constant-field checks and exclusions.
"""
import re
import sympy as s
from expressions import q, X
from qgosper import UnsupportedDomain, dispersion, q_power
from qrational_system import field_for, solve_system, shift
from ore import OreResourceLimit


def rational_read(value):
    # Only internally generated SymPy strings, NEVER public expression input.
    return s.sympify(value, locals={v:s.Symbol(v) for v in re.findall(r'[A-Za-z][A-Za-z0-9_]*', value)})


def monomial(variables, exponents):
    return s.prod(v**e for v, e in zip(variables, exponents))


def laurent_coefficients(value, variables):
    """Exact sparse Laurent polynomial over the complementary rational field."""
    value = s.cancel(value)
    if not variables:
        return {(): value} if value != 0 else {}
    num, den = s.fraction(value)
    try:
        pp, dd = s.Poly(num, *variables), s.Poly(den, *variables)
    except s.PolynomialError as exc:
        raise UnsupportedDomain('Laurent-polynomial product expressions required') from exc
    if len(dd.terms()) != 1:
        raise UnsupportedDomain('denominators involving sums of product monomials are not supported')
    dm, dc = dd.terms()[0]
    return {tuple(a-b for a, b in zip(m, dm)): s.cancel(c/dc)
            for m, c in pp.terms() if c != 0}


def constant_signature(value):
    """Multiplicative valuations of K* modulo {+/- q**integer}.

    K is a purely transcendental extension of QQ. Rational primes and monic
    irreducible parameter polynomials form a free multiplicative basis.
    Ignoring sign is deliberate: Pi admissibility tests ALL positive powers.
    """
    value = s.cancel(value)
    symbols = sorted(value.free_symbols | {q}, key=str)
    answer = {}
    scalar = s.Integer(1)
    for poly, sign in zip(s.fraction(value), (1, -1)):
        unit, factors = s.Poly(poly, *symbols, domain=s.QQ).factor_list()
        scalar *= unit**sign
        for factor, exponent in factors:
            scalar *= factor.LC()**(sign*exponent)
            factor = factor.monic().as_expr()
            if factor != q:
                key = 'constant_factor:'+str(factor)
                answer[key] = answer.get(key, 0)+sign*exponent
    scalar = abs(s.Rational(scalar))
    for integer, sign in ((scalar.p, 1), (scalar.q, -1)):
        for prime, exponent in s.factorint(integer).items():
            key = 'rational_prime:'+str(prime)
            answer[key] = answer.get(key, 0)+sign*exponent
    return {k: int(v) for k, v in answer.items() if v}


def product_lattice(ratios, budget):
    """Decide multiplicative independence modulo rational coboundaries/radicals.

    Each ratio is reduced to X-valuation, nonzero q-shift orbit totals and a
    constant unit. Coboundary witnesses retain the orbit offsets exactly.
    A null vector yields prod(b_i**e_i)=sigma(g)/g, after squaring if needed.
    """
    if not ratios:
        return dict(rank=0, columns=0, rows=[], matrix=[], reductions=[]), None
    field = field_for(ratios, X, q)
    representatives, signatures, reductions, witnesses = [], [], [], []
    for ratio in ratios:
        signature = {}; coboundary = s.Integer(1); totals = {}
        for part, sign in zip(s.fraction(s.cancel(ratio)), (1, -1)):
            polynomial = s.Poly(part, X, domain=field)
            if polynomial.degree() > budget.max_normal_form_degree:
                raise OreResourceLimit('product ratio exceeds normal-form degree budget')
            _, factors = polynomial.factor_list()
            for factor, exponent in factors:
                factor = factor.monic().as_expr(); exponent *= sign
                if factor == X:
                    signature['X_valuation'] = signature.get('X_valuation', 0)+exponent
                    continue
                orbit = None; offset = 0
                for i, representative in enumerate(representatives):
                    forward = dispersion(factor, representative, X, q, field)
                    backward = dispersion(representative, factor, X, q, field)
                    if forward or backward:
                        orbit = i; offset = forward[0] if forward else -backward[0]
                        break
                if orbit is None:
                    orbit = len(representatives); representatives.append(factor)
                degree = int(s.degree(representatives[orbit], X))
                if abs(offset)*degree*abs(exponent) > budget.max_normal_form_degree:
                    raise OreResourceLimit('product orbit coboundary exceeds degree budget')
                if offset >= 0:
                    h = s.prod(shift(representatives[orbit], X, q, j) for j in range(offset))
                else:
                    h = 1/s.prod(shift(representatives[orbit], X, q, j) for j in range(offset, 0))
                coboundary = s.cancel(coboundary*h**exponent)
                totals[orbit] = totals.get(orbit, 0)+exponent
        reduced = s.cancel(ratio*coboundary/shift(coboundary, X, q))
        unit = s.cancel(reduced/X**signature.get('X_valuation', 0)/
                        s.prod(representatives[i]**e for i, e in totals.items()))
        if unit.has(X):
            raise ArithmeticError('product orbit normalization residual')
        for i, exponent in totals.items():
            if exponent: signature['orbit:'+str(i)] = exponent
        signature.update(constant_signature(unit))
        signatures.append(signature); witnesses.append(coboundary)
        reductions.append(dict(ratio=str(ratio), coboundary=str(coboundary),
                               reduced=str(reduced), constant_unit=str(unit)))
    keys = sorted(set().union(*(set(v) for v in signatures)))
    matrix = s.Matrix([[v.get(key, 0) for v in signatures] for key in keys]) if keys else s.zeros(0, len(ratios))
    trace = dict(rank=matrix.rank(), columns=len(ratios), rows=keys,
                 matrix=[list(map(int, matrix.row(i))) for i in range(matrix.rows)],
                 orbit_representatives=list(map(str, representatives)), reductions=reductions)
    kernel = matrix.nullspace()
    if not kernel: return trace, None
    # In incremental use previous columns are independent, so the last entry is nonzero.
    vector = kernel[0]
    common = s.ilcm(*[v.q for v in vector]) if len(vector) > 1 else vector[0].q
    vector = [int(v*common) for v in vector]
    if vector[-1] < 0: vector = [-v for v in vector]
    H = s.cancel(s.prod(h**e for h, e in zip(witnesses, vector)))
    ratio = s.cancel(s.prod(b**e for b, e in zip(ratios, vector)))
    unit = s.cancel(ratio*H/shift(H, X, q))
    exponent = q_power(unit, q)
    multiplier = 1
    if exponent is None:
        exponent = q_power(-unit, q); multiplier = 2
    if exponent is None: raise ArithmeticError('multiplicative signature kernel did not give a q-power unit')
    H = s.cancel((H*X**exponent)**multiplier)
    vector = [multiplier*e for e in vector]
    residual = s.cancel(s.prod(b**e for b, e in zip(ratios, vector))-shift(H, X, q)/H)
    if residual != 0: raise ArithmeticError('multiplicative dependence witness residual')
    return trace, dict(exponents=vector, rational_witness=str(H), residual='0')


class Tower:
    """Certified Pi block followed by any finite triangular polynomial Sigma tower."""
    def __init__(self, budget, occupied=()):
        self.budget = budget
        self.products = []; self.ratios = []; self.sums = []; self.increments = []
        self.aliases = {}; self.constants = []; self.constant_definitions = {}
        self.records = []; self.trace = []; self.cache = {}; self.occupied = set(occupied)
        self.rational_calls = 0

    def fresh_constant(self, definition):
        i = len(self.constants)
        while 'DRConstant'+str(i) in self.occupied: i += 1
        symbol = s.Symbol('DRConstant'+str(i)); self.occupied.add(str(symbol))
        self.constants.append(symbol); self.constant_definitions[symbol] = definition
        return symbol

    def sigma(self, value, depth=None):
        depth = len(self.sums) if depth is None else depth
        replacements = {X: q*X, **dict(zip(self.products, [b*p for b, p in zip(self.ratios, self.products)])),
                        **dict(zip(self.sums[:depth], [t+a for t, a in zip(self.sums[:depth], self.increments[:depth])]))}
        return s.cancel(s.sympify(value).xreplace(replacements))

    def normalize(self, value):
        return s.cancel(s.sympify(value).xreplace(self.aliases))

    def ring_check(self, value, depth=None):
        depth = len(self.sums) if depth is None else depth
        value = s.cancel(value)
        if self.sums[:depth]:
            try: coefficients = s.Poly(value, *self.sums[:depth]).coeffs()
            except s.PolynomialError as exc:
                raise UnsupportedDomain('sum extensions must occur polynomially; general tower denominators are unsupported') from exc
        else: coefficients = [value]
        for coefficient in coefficients:
            for base in laurent_coefficients(coefficient, self.products).values():
                field_for([base], X, q)
        return value

    def check_basis(self, rhs, basis, depth):
        variables = {X, *self.products, *self.sums}
        for cs, g in basis:
            if len(cs) != len(rhs) or any(c.free_symbols & variables for c in cs):
                raise ArithmeticError('nonconstant parameterized coefficients')
            if s.cancel(self.sigma(g, depth)-g-sum(c*f for c, f in zip(cs, rhs))) != 0:
                raise ArithmeticError('original tower equation residual')

    def rational_basis(self, ratio, rhs):
        self.rational_calls += 1
        raw = solve_system([[ratio]], [[f] for f in rhs], X, q, self.budget, include_basis=True)
        self.trace.append(dict(kind='rational_base', ratio=str(ratio), rhs_basis=list(map(str, rhs)), result=raw))
        return [(tuple(map(rational_read, row['coefficients'])), rational_read(row['certificate_row'][0]))
                for row in raw['solution_basis']]

    def solve(self, rhs, depth=None):
        """Return the COMPLETE basis of (c_1,...,c_m,g), including c=0."""
        depth = len(self.sums) if depth is None else depth
        rhs = tuple(self.ring_check(s.sympify(f), depth) for f in rhs)
        if not rhs: raise ValueError('nonempty RHS basis required')
        if len(rhs) > self.budget.max_unknowns:
            raise OreResourceLimit('parameterized tower dimension exceeds unknown limit')
        key = (depth, rhs)
        if key in self.cache: return self.cache[key]
        if all(f == 0 for f in rhs):
            basis = [(tuple(int(i == j) for i in range(len(rhs))), s.Integer(0)) for j in range(len(rhs))]
            basis.append((tuple(s.Integer(0) for _ in rhs), s.Integer(1)))
            basis = [(tuple(map(s.sympify, cs)), g) for cs, g in basis]
        elif depth == 0:
            basis = self.solve_products(rhs)
        else:
            t = self.sums[depth-1]
            degree = max(int(s.degree(f, t)) for f in rhs if f != 0)+1
            if degree > self.budget.max_normal_form_degree:
                raise OreResourceLimit('derived Sigma degree bound exceeds limit')
            self.trace.append(dict(kind='sigma_degree', variable=str(t), upper=degree,
                                   reason='deg(g) <= max deg(rhs)+1 in a certified Sigma-star extension',
                                   rhs_basis=list(map(str, rhs))))
            basis = [(tuple(s.Integer(i == j) for i in range(len(rhs))), s.Integer(0)) for j in range(len(rhs))]
            for d in range(degree, -1, -1):
                targets = [s.Poly(s.cancel(sum(c*f for c, f in zip(cs, rhs))-
                                           (self.sigma(g, depth)-g)), t).nth(d) for cs, g in basis]
                lower = self.solve(targets, depth-1)
                basis = self.combine(basis, lower, t**d)
        self.check_basis(rhs, basis, depth)
        self.cache[key] = basis
        return basis

    def combine(self, basis, solutions, term):
        answer = []
        for weights, coefficient in solutions:
            cs = tuple(s.cancel(sum(w*row[0][j] for w, row in zip(weights, basis))) for j in range(len(basis[0][0])))
            g = s.cancel(sum(w*row[1] for w, row in zip(weights, basis))+coefficient*term)
            answer.append((cs, g))
        if len(answer) > self.budget.max_unknowns:
            raise OreResourceLimit('intermediate tower solution dimension exceeds limit')
        return answer

    def solve_products(self, rhs):
        if not self.products: return self.rational_basis(s.Integer(1), rhs)
        coefficients = [laurent_coefficients(f, self.products) for f in rhs]
        zero = (0,)*len(self.products)
        support = [zero]+sorted(set().union(*(set(c) for c in coefficients))-{zero})
        if len(support) > self.budget.max_states:
            raise OreResourceLimit('derived product support exceeds state limit')
        self.trace.append(dict(kind='product_support', exponents=[list(e) for e in support],
                               reason='RHS support plus constant monomial; nonzero homogeneous modes excluded by Pi independence'))
        basis = [(tuple(s.Integer(i == j) for i in range(len(rhs))), s.Integer(0)) for j in range(len(rhs))]
        for exponent in support:
            targets = [s.cancel(sum(c*row.get(exponent, 0) for c, row in zip(cs, coefficients))) for cs, _ in basis]
            ratio = monomial(self.ratios, exponent)
            solutions = self.rational_basis(ratio, targets)
            basis = self.combine(basis, solutions, monomial(self.products, exponent))
        return basis

    def add_sum(self, symbol, increment):
        increment = self.ring_check(self.normalize(increment))
        basis = self.solve([increment])
        relation = next(((cs, g) for cs, g in basis if cs[0] != 0), None)
        record = dict(name=str(symbol), kind='sum', increment=str(increment))
        if relation:
            cs, g = relation; g = s.cancel(g/cs[0])
            constant = self.fresh_constant(symbol-g)
            self.aliases[symbol] = g+constant
            record.update(action='constant_reduction', primitive=str(g), alias=str(g+constant),
                          new_constant=str(constant), constant_definition=str(symbol-g), residual='0',
                          original_extension_preserves_constants=False)
        else:
            self.sums.append(symbol); self.increments.append(increment)
            record.update(action='sigma_star_extension', original_extension_preserves_constants=True,
                          criterion='no telescoping primitive in the preceding field',
                          obstruction_basis=[dict(coefficients=list(map(str, cs)), certificate=str(g)) for cs, g in basis])
        self.records.append(record); self.cache.clear()

    def add_product(self, symbol, ratio):
        ratio = self.normalize(ratio)
        if ratio == 0: raise ValueError('product shift ratio must be nonzero')
        if ratio.free_symbols & {*self.products, *self.sums}:
            raise UnsupportedDomain('product shift ratios must lie in the base rational field')
        if self.sums: raise UnsupportedDomain('product block must precede genuine sum extensions')
        field_for([ratio], X, q)
        trace, dependency = product_lattice([*self.ratios, ratio], self.budget)
        record = dict(name=str(symbol), kind='product', ratio=str(ratio), independence=trace)
        if dependency is None:
            self.products.append(symbol); self.ratios.append(ratio)
            record.update(action='pi_extension', original_extension_preserves_constants=True)
        elif dependency['exponents'][-1] == 1:
            g = s.cancel(rational_read(dependency['rational_witness'])/
                         monomial(self.products, dependency['exponents'][:-1]))
            constant = self.fresh_constant(symbol/g)
            self.aliases[symbol] = g*constant
            record.update(action='constant_reduction', dependency=dependency, alias=str(g*constant),
                          new_constant=str(constant), constant_definition=str(symbol/g), residual='0',
                          original_extension_preserves_constants=False, constant_must_be_nonzero=True)
        else:
            record.update(action='algebraic_or_torsion_dependency', dependency=dependency,
                          original_extension_preserves_constants=False)
            self.records.append(record)
            return False
        self.records.append(record); self.cache.clear()
        return True


def verify_relation(tower, rhs, coefficients, certificate):
    """Independent exact check of a claimed nontrivial tower relation."""
    cs = list(map(s.sympify, coefficients)); g = s.sympify(certificate)
    if not cs or not any(cs) or len(cs) != len(rhs): raise ValueError('nonzero compatible relation required')
    field_for(cs, X, q)
    tower.ring_check(g)
    if any(c.free_symbols & {X, *tower.products, *tower.sums} for c in cs):
        raise ValueError('coefficients must be shift constants')
    residual = s.cancel(tower.sigma(g)-g-sum(c*f for c, f in zip(cs, rhs)))
    if residual != 0: raise ValueError('tower certificate residual is nonzero')
    return residual


def compute(data, budget, parse):
    if not isinstance(data, dict) or set(data) != {'extensions', 'rhs_basis'}:
        raise ValueError('difference_ring accepts only extensions and rhs_basis; no target or certificate hints')
    extensions, rhs_nodes = data['extensions'], data['rhs_basis']
    if not isinstance(extensions, list) or not isinstance(rhs_nodes, list) or not rhs_nodes:
        raise ValueError('extensions list and nonempty rhs_basis list required')
    if len(extensions) > budget.max_states or len(rhs_nodes) > budget.max_unknowns:
        raise OreResourceLimit('tower input size exceeds budget')
    parsed = []; names = set()
    for row in extensions:
        if not isinstance(row, dict) or row.get('kind') not in ('sum', 'product'):
            raise ValueError('sum/product extension required')
        field = 'increment' if row['kind'] == 'sum' else 'ratio'
        if set(row) != {'kind', 'name', field}: raise ValueError('unexpected extension fields')
        name = row['name']
        if not isinstance(name, str) or not re.fullmatch(r'[A-Za-z][A-Za-z0-9_]*', name) or name in ('X','q','Q','n','k') or name in names:
            raise ValueError('unique nonreserved extension name required')
        names.add(name); parsed.append((s.Symbol(name), row['kind'], parse(row[field])))
    rhs = list(map(parse, rhs_nodes)); all_names = {row[0] for row in parsed}; seen = set()
    values = [row[2] for row in parsed]+rhs
    field_for(values, X, q)
    tower = Tower(budget, {str(v) for f in values for v in f.free_symbols} | names)
    for symbol, kind, value in parsed:
        if value.free_symbols & (all_names-seen): raise ValueError('extension shift must reference only preceding extensions')
        seen.add(symbol)
        if kind == 'sum': tower.add_sum(symbol, value)
        elif not tower.add_product(symbol, value):
            return dict(status='unsupported_domain', solver='difference_ring',
                        reason='dependent product needs algebraic constants or root-of-unity ring; no false Pi extension admitted',
                        tower=tower.records, original_identity_proved=False)
    normalized_rhs = [tower.ring_check(tower.normalize(f)) for f in rhs]
    basis = tower.solve(normalized_rhs)
    def encode(cs, g):
        return dict(coefficients=list(map(str, cs)), certificate=str(g), residual='0')
    result = dict(solution_basis=[encode(cs, g) for cs, g in basis],
                  constant_field_extensions=[dict(name=str(c), definition=str(tower.constant_definitions[c])) for c in tower.constants],
                  rational_subproblems=tower.rational_calls, reduction_trace=tower.trace,
                  completeness='complete parameterized telescoping for admitted Laurent-product / polynomial-sum towers')
    candidate = next(((cs, g) for cs, g in basis if any(cs)), None)
    status = 'no_relation_in_declared_basis'
    if candidate:
        cs, g = candidate; pivot = next(c for c in cs if c != 0)
        cs = tuple(s.cancel(c/pivot) for c in cs); g = s.cancel(g/pivot)
        verify_relation(tower, normalized_rhs, cs, g)
        result.update(encode(cs, g)); status = 'constructed'
    # Also verify in the ORIGINAL named tower after restoring constant definitions.
    source_shift = {X:q*X, **{t: t+a if kind == 'sum' else t*a for t, kind, a in parsed}}
    restoration = dict(tower.constant_definitions)
    # Definitions of later constants can involve earlier fresh constants.
    for c in tower.constants: restoration[c] = restoration[c].xreplace(restoration)
    for item in [*result['solution_basis'], *([result] if candidate else [])]:
        cs = [rational_read(v).xreplace(restoration) for v in item['coefficients']]
        g = rational_read(item['certificate']).xreplace(restoration)
        residual = s.cancel(g.xreplace(source_shift)-g-sum(c*f for c, f in zip(cs, rhs)))
        if residual != 0 or any(s.cancel(c.xreplace(source_shift)-c) != 0 for c in cs):
            raise ArithmeticError('original named tower restoration residual')
        item.update(original_certificate=str(g), original_coefficients=list(map(str, cs)), original_residual='0')
    return dict(status=status, solver='difference_ring', result=result, tower=tower.records,
                normalized_input=dict(rhs_basis=list(map(str, normalized_rhs)),
                    products=[dict(name=str(p), ratio=str(b)) for p, b in zip(tower.products, tower.ratios)],
                    sums=[dict(name=str(t), increment=str(a)) for t, a in zip(tower.sums, tower.increments)]),
                domain=dict(base='QQ(q, independent parameters)(X), sigma(X)=q*X; q transcendental',
                    extension_class='base-rational Pi block followed by polynomial Sigma tower',
                    constant_policy='certify each extension or explicitly introduce a free shift constant; never set it to zero',
                    specialization_policy='generic formal field only; no specialized q or parameter domains discharged',
                    negative_result_scope='admitted tower only, never impossibility of the original identity',
                    excluded='general tower denominators, products depending on sums, algebraic/root-of-unity extensions',
                    boundary_policy='initial values, finite sum endpoints, source evaluation and Lean remain external'))
