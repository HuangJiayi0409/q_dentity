"""Exact scalar serialization shared by independent finite-matrix constructors.

No proof search or cross-method routing lives here. Unknown scalar applications
are independent atoms during construction; Lean verifies their actual meaning.
"""
import sympy as s


class ScalarCodec:
    def __init__(self):
        self.atoms = {}

    def parse(self, node):
        op = node['op']
        if op == 'integer':
            return s.Integer(node['value'])
        if op == 'atom':
            key = 'z' + str(node['key'])
            if key in self.atoms and self.atoms[key] != node['display']:
                raise ValueError('inconsistent scalar atom')
            self.atoms[key] = node['display']
            return s.Symbol(key)
        if op in ('neg', 'inv', 'pow'):
            a = self.parse(node['arg'])
            return -a if op == 'neg' else 1/a if op == 'inv' else a**node['exponent']
        a, b = map(self.parse, node['args'])
        return {'HAdd.hAdd': lambda: a+b, 'HSub.hSub': lambda: a-b,
                'HMul.hMul': lambda: a*b, 'HDiv.hDiv': lambda: a/b}[op]()

    def matrix(self, obj):
        return s.Matrix([[self.parse(x) for x in row] for row in obj['entries']])

    def vector(self, obj):
        return s.Matrix([self.parse(x) for x in obj['entries']])

    def lean(self, e):
        e = s.sympify(e)
        if e.is_Integer:
            return str(int(e)) if e >= 0 else '(' + str(int(e)) + ')'
        if e.is_Rational:
            return '(' + str(e.p) + ' / ' + str(e.q) + ')'
        if e.is_Symbol:
            return '(' + self.atoms[str(e)] + ')'
        if e.is_Add or e.is_Mul:
            return '(' + (' + ' if e.is_Add else ' * ').join(self.lean(a) for a in e.args) + ')'
        if e.is_Pow and e.exp.is_Integer:
            base, power = self.lean(e.base), int(e.exp)
            if power >= 0:
                return '(' + base + ' ^ ' + str(power) + ')'
            return '((' + base + ' ^ ' + str(-power) + ')⁻¹)'
        raise ValueError('unsupported exact coefficient: ' + str(e))

    def matrix_lean(self, a, ty):
        return ('(!![' + '; '.join(', '.join(self.lean(x) for x in a.row(i))
                                  for i in range(a.rows)) +
                f'] : Matrix (Fin {a.rows}) (Fin {a.cols}) ({ty}))')


def matrix_record(a):
    return [[str(x) for x in a.row(i)] for i in range(a.rows)]


def checked_zero(a):
    if any(s.cancel(x) != 0 for x in a):
        raise ValueError('symbolic certificate residual is not zero')


def scalar_finish():
    # No additional hypotheses are introduced. Failure of a denominator proof
    # leaves the original goal unproved, including exceptional characteristic.
    return 'first | (ring; done) | (field_simp [*] <;> ring)'


def entries_finish(n, names=(), sums=True):
    defs = ', '.join([*names, *(['Matrix.mul_apply', 'Fin.sum_univ_succ'] if sums else [])])
    return ('ext i j\n    fin_cases i <;> fin_cases j <;> '
            f'simp [{defs}] <;> ({scalar_finish()})')
