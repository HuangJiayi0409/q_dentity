"""Generic, restricted formula IR. Contains no identity-specific shift ratios."""
import re
import sympy as s

n, k = s.symbols('n k', integer=True)
q, Q, X = s.symbols('q Q X')
Poch = s.Function('Poch')


def expression(node):
    """Read arithmetic trees, never eval/sympify untrusted strings as Python."""
    if type(node) is int:
        return s.Integer(node)
    if isinstance(node, str) and re.fullmatch(r'[a-z][a-z0-9_]*', node):
        return {'n': n, 'k': k, 'q': q}.get(node, s.Symbol(node))
    if not isinstance(node, list) or not node:
        raise ValueError('unsupported_expression')
    op, *children = node
    args = [expression(c) for c in children]
    if op == 'mul' and args:
        return s.Mul(*args)
    if op == 'add' and args:
        return s.Add(*args)
    if op in ('sub', 'div', 'pow') and len(args) == 2:
        a, b = args
        return {'sub': lambda: a-b, 'div': lambda: a/b, 'pow': lambda: a**b}[op]()
    if op == 'poch' and len(args) == 3:
        return Poch(*args)
    if op == 'fall' and len(args) == 4:
        a, b, base, length = args
        # Search representation only; generated Lean verifies the original product.
        return a**length * Poch(b/a, base, length)
    if op == 'gaussian' and len(args) == 3:
        base, upper, lower = args
        # Formal quotient representation, with a mandatory later Lean domain bridge.
        return Poch(base, base, upper)/(Poch(base, base, lower)*Poch(base, base, upper-lower))
    raise ValueError('unsupported_expression: ' + str(op))


def shift_ratio(expr, index):
    if not expr.has(index):
        return s.Integer(1)
    if expr.func == Poch:
        a, base, length = expr.args
        if base.has(index):
            raise ValueError('representation_gap: index-dependent Pochhammer base')
        start_shift = s.cancel(s.powsimp(a.subs(index,index+1)/a, force=True)) if a.has(index) else s.Integer(1)
        start_delta = start_shift.as_powers_dict().get(base,s.Integer(0))
        if not start_delta.is_Integer or s.cancel(start_shift/base**start_delta) != 1:
            raise ValueError('representation_gap: non-geometric Pochhammer start shift')
        delta = s.expand(length.subs(index,index+1)-length)
        if not delta.is_Integer or max(abs(int(delta)),abs(int(start_delta))) > 32:
            raise ValueError('representation_gap: nonconstant or large Pochhammer shift')
        def growth(offset, amount):
            if amount >= 0:
                return s.prod(1-a*base**(offset+j) for j in range(amount))
            return 1/s.prod(1-a*base**(offset+j) for j in range(amount,0))
        return growth(length,int(start_delta+delta))/growth(0,int(start_delta))
    if expr.is_Mul:
        return s.prod(shift_ratio(t, index) for t in expr.args)
    if expr.is_Pow:
        base, exponent = expr.args
        if not base.has(index):
            return base**s.expand(exponent.subs(index, index+1)-exponent)
        if exponent.is_Integer:
            return shift_ratio(base, index)**exponent
    if not expr.has(Poch):
        return s.cancel(expr.subs(index, index+1)/expr)
    raise ValueError('representation_gap: unsupported additive product expression')


def rationalize(expr):
    def convert(power):
        exponent = s.Poly(s.expand(power.exp), n, k)
        if exponent.total_degree() > 1:
            raise ValueError('representation_gap: nonlinear shift exponent')
        a = exponent.coeff_monomial(n)
        b = exponent.coeff_monomial(k)
        c = exponent.coeff_monomial(1)
        if not all(v.is_Integer for v in (a, b, c)):
            raise ValueError('representation_gap: nonintegral shift exponent')
        return Q**a * X**b * q**c
    result = expr.replace(lambda t: t.is_Pow and t.base == q and t.exp.has(n, k), convert)
    result = s.cancel(result)
    if result.has(n, k, Poch) or not result.is_rational_function(X, Q):
        raise ValueError('representation_gap: not a single-base rational shift')
    return result


def derive(problem):
    allowed = {'schema_version', 'source_id', 'summand', 'target'}
    if set(problem) != allowed or problem['schema_version'] != 1:
        raise ValueError('invalid_problem: only source metadata and formula trees are accepted')
    F, T = expression(problem['summand']), expression(problem['target'])
    if T.has(k) or F == 0 or T == 0:
        raise ValueError('unsupported_structure: target must be a nonzero formal expression independent of k')
    return {
        'n_shift': rationalize(shift_ratio(F, n)),
        'k_shift': rationalize(shift_ratio(F, k)),
        'target_coefficient': rationalize(shift_ratio(T, n)),
    }
