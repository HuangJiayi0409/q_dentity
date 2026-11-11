"""Finite, fully consumed grammar for geometric Gaussian sums.

This exports the summand alone to q-Zeilberger. The original target is retained
verbatim in Source and as a typed expression; it never guides core search.
"""
import re

from .formal_frontend import _Parser, _Unsupported, _node, _num, _var, _closed_prefix
from .models import Source
from .storage import IntegrityError, verify_source

PROFILE = 'gaussian_geometric_recurrence_v1'
_TOKEN = re.compile(r'\s+|:=|[A-Za-z][A-Za-z0-9_]*(?:\.[A-Za-z][A-Za-z0-9_]*)*|[0-9]+|[(){}\[\]:,+*^=−\-/%]|[ℕ∑∈]')


def _tokens(text):
    if len(text) > 65536:
        raise _Unsupported('source exceeds size limit')
    clean, i, depth = [], 0, 0
    while i < len(text):
        pair = text[i:i+2]
        if pair == '/-': depth += 1; clean.append(' '); i += 2
        elif pair == '-/' and depth: depth -= 1; clean.append(' '); i += 2
        elif not depth and pair == '--':
            end = text.find('\n', i); i = len(text) if end < 0 else end; clean.append(' ')
        else: clean.append(' ' if depth else text[i]); i += 1
    if depth: raise _Unsupported('unterminated source comment')
    clean = ''.join(clean); position, output = 0, []
    for match in _TOKEN.finditer(clean):
        if match.start() != position: raise _Unsupported('unsupported source token')
        position = match.end()
        if not match.group().isspace(): output.append(match.group())
    if position != len(clean) or len(output) > 4096:
        raise _Unsupported('unsupported or oversized syntax')
    return output


class RecurrenceParser(_Parser):
    def __init__(self, text):
        self.tokens, self.pos = _tokens(text), 0

    def name(self):
        value = super().name()
        if value in {'if', 'then', 'else', 'poch'}:
            raise _Unsupported('reserved recurrence binder')
        return value

    def expr(self, precedence=0, depth=0):
        if depth > 64: raise _Unsupported('expression nesting limit')
        left = self.primary(depth+1)
        operators = {'=': 1, '+': 2, '-': 2, '*': 3, '/': 3, '%': 3, '^': 4}
        while self.peek() in operators and operators[self.peek()] >= precedence:
            op = self.take(); rank = operators[op]
            right = self.expr(rank if op == '^' else rank+1, depth+1)
            left = _node(op, left, right)
        return left

    def primary(self, depth):
        if depth > 64: raise _Unsupported('expression nesting limit')
        if self.peek() == '-':
            self.take(); return _node('neg', self.primary(depth+1))
        if self.peek() in ('poch', 'FiniteQBenchmark.poch'):
            self.take(); return _node('poch', *(self.primary(depth+1) for _ in range(3)))
        if self.peek() == 'if':
            self.take(); condition = self.expr(depth=depth+1); self.take('then')
            yes = self.expr(depth=depth+1); self.take('else')
            return _node('ite', condition, yes, self.expr(depth=depth+1))
        return super().primary(depth)

    def source(self):
        # The import is source metadata only. No Representation/Statements
        # module is imported by the independent mathematical checker.
        imports = []
        while self.peek() == 'import':
            self.take(); module = self.take()
            if module not in {'Benchmark.Representation', 'Benchmark.Gaussian', 'Benchmark.Batch3Proofs'}:
                raise _Unsupported('unsupported source import')
            imports.append(module)
        if not imports: raise _Unsupported('source import required')
        self.sequence('open', 'scoped', 'BigOperators', 'open', 'FiniteQBenchmark')
        self.sequence('set_option', 'autoImplicit', 'false')
        self.sequence('set_option', 'linter.unusedVariables', 'false')
        self.take('namespace'); namespace = self.take()
        if not re.fullmatch(r'[A-Za-z][A-Za-z0-9_]*(?:\.[A-Za-z][A-Za-z0-9_]*)*', namespace):
            raise _Unsupported('unsupported namespace')
        self.sequence('variable', '{'); field = self.name()
        self.sequence(':', 'Type', '*', '}', '[', 'Field', field, ']')
        binders = [{'name': field, 'type': 'Type u', 'kind': 'implicit'},
                   {'name': None, 'type': 'Field ' + field, 'kind': 'instance'}]
        if self.peek() == 'attribute':
            self.sequence('attribute', '[', 'local', 'instance', ']', 'Classical.propDecidable')
        self.take('theorem'); theorem = self.name()
        while self.peek() == '(':
            binders.extend(self.binder())
            if len(binders) > 16: raise _Unsupported('binder count limit')
        self.take(':'); proposition = self.expr()
        self.sequence(':=', 'by', 'sorry', 'end', namespace)
        if self.peek() is not None: raise _Unsupported('unconsumed source commands')
        return namespace + '.' + theorem, field, binders, proposition


def lean(node):
    op = node['op']
    if op == 'var': return node['name']
    if op == 'nat': return str(node['value'])
    if op == 'neg': return '(-' + lean(node['args'][0]) + ')'
    if op in ('gaussian', 'poch'):
        return '(FiniteQBenchmark.' + op + ' ' + ' '.join(lean(a) for a in node['args']) + ')'
    if op == 'sum':
        return '(∑ ' + node['index'] + ' ∈ Finset.range ' + lean(node['range']['args'][0]) + ', ' + lean(node['body']) + ')'
    if op == 'ite':
        c, yes, no = map(lean, node['args']); return f'(if {c} then {yes} else {no})'
    return '(' + (' ' + op + ' ').join(lean(a) for a in node['args']) + ')'


def _check(node, wanted, names, field):
    op = node['op']; args = node.get('args', [])
    if op == 'var': good = names.get(node['name']) == wanted
    elif op == 'nat': good = wanted in ('ℕ', field)
    elif op == 'neg': good = wanted == field and _check(args[0], field, names, field)
    elif op == 'sum':
        good = (wanted == field and node['index'] not in names
                and _check(node['range']['args'][0], 'ℕ', names, field)
                and _check(node['body'], field, {**names, node['index']: 'ℕ'}, field))
    elif op in ('gaussian', 'poch'):
        types = [field, 'ℕ', 'ℕ'] if op == 'gaussian' else [field, field, 'ℕ']
        good = wanted == field and all(_check(a, t, names, field) for a, t in zip(args, types))
    elif op == '^': good = wanted in ('ℕ', field) and _check(args[0], wanted, names, field) and _check(args[1], 'ℕ', names, field)
    elif op in ('+', '-', '*', '/', '%'):
        good = wanted in ('ℕ', field) and (op != '%' or wanted == 'ℕ') and all(_check(a, wanted, names, field) for a in args)
    elif op == 'ite': good = _check(args[0], 'Prop', names, field) and all(_check(a, wanted, names, field) for a in args[1:])
    elif op == '=':
        good = wanted == 'Prop' and any(all(_check(a, t, names, field) for a in args) for t in ('ℕ', field))
    else: good = False
    return good


def emitter_ir(node):
    op = node['op']
    if op in ('var', 'nat'): return node
    if op == 'sum':
        return _node('Finset.sum', _node('Finset.range', emitter_ir(node['range']['args'][0])),
                     {'op': 'lambda', 'name': node['index'], 'body': emitter_ir(node['body'])})
    names = {'+': 'HAdd.hAdd', '-': 'HSub.hSub', '*': 'HMul.hMul', '/': 'HDiv.hDiv',
             '%': 'HMod.hMod', '^': 'HPow.hPow', '=': 'Eq', 'neg': 'Neg.neg',
             'gaussian': 'FiniteQBenchmark.gaussian', 'poch': 'FiniteQBenchmark.poch', 'ite': 'ite'}
    return _node(names[op], *(emitter_ir(a) for a in node['args']))


def _bounded_ast(root):
    """Left-associative parsing can deepen an AST without parser recursion."""
    pending, count = [(root, 0)], 0
    while pending:
        node, depth = pending.pop(); count += 1
        if depth > 64 or count > 2048:
            raise _Unsupported('recurrence expression tree exceeds structural limits')
        for value in node.values():
            if isinstance(value, dict): pending.append((value, depth+1))
            elif isinstance(value, list):
                pending.extend((child, depth+1) for child in value if isinstance(child, dict))


def analyze_source(source, run_root=None):
    bound = Source.from_dict(source); verify_source(bound, run_root)
    if bound.Gamma != bound.declaration: raise IntegrityError('recurrence original context mismatch')
    failure = {'status': 'not_applicable', 'profile': PROFILE, 'source': bound.to_dict()}
    try:
        theorem, field, binders, equation = RecurrenceParser(bound.declaration).source()
        _bounded_ast(equation)
        if theorem != bound.theorem: raise IntegrityError('recurrence theorem binding mismatch')
        names = [b['name'] for b in binders if b['name']]
        context = {b['name']: b['type'] for b in binders[2:]}
        if len(names) != len(set(names)) or any(t not in (field, 'ℕ', 'True') for t in context.values()):
            raise _Unsupported('unsupported original context')
        if equation['op'] != '=' or not all(_check(a, field, context, field) for a in equation['args']):
            raise _Unsupported('typed field equality required')
        left, right = equation['args']
        total, target = (left, right) if left['op'] == 'sum' else (right, left)
        if total['op'] != 'sum': raise _Unsupported('complete range sum required')
        length, body, index = total['range']['args'][0], total['body'], total['index']
        if length['op'] != '+' or length['args'][0]['op'] != 'var' or length['args'][1] != _num(1):
            raise _Unsupported('range(n+1) required')
        n = length['args'][0]['name']
        if body['op'] != '*' or body['args'][0]['op'] != '^' or body['args'][1]['op'] != 'gaussian':
            raise _Unsupported('geometric weight times one Gaussian required')
        weight, gaussian = body['args']; base = gaussian['args'][0]
        if base['op'] != 'var' or gaussian['args'][1:] != [_var(n), _var(index)] or weight['args'][1] != _var(index):
            raise _Unsupported('Gaussian indices or weight exponent differ from range')
        # First native profile uses the full geometric Gaussian emitter with
        # the alternating constant weight; no benchmark identity is inspected.
        if weight['args'][0] != _node('neg', _num(1)):
            raise _Unsupported('native recurrence profile requires alternating weight')
        if len({base['name'], n, index, field}) != 4: raise _Unsupported('overlapping binders')
        proposition = _closed_prefix(binders) + ', ' + lean(equation)
        if bound.proposition is not None and bound.proposition != proposition:
            raise IntegrityError('claimed original differs from reconstructed recurrence source')
        return {'status': 'applicable', 'profile': PROFILE, 'source': bound.to_dict(),
            'binders': binders, 'symbols': {'field': field, 'base': base['name'], 'bound': n, 'index': index},
            'original_proposition': proposition, 'summation': total, 'target': target,
            'orientation': 'sum_equals_target' if left is total else 'target_equals_sum',
            'emitter_expression': emitter_ir(equation),
            'core_request': {'schema_version': 1, 'solver': 'q_zeilberger', 'input': {
                'summand': ['mul', ['pow', -1, 'k'], ['gaussian', 'q', 'n', 'k']]}},
            'mapping': {'n': n, 'k': index, 'q': base['name'],
                        'support': '0 <= k <= n; zero above n', 'shift': 'n -> n+1',
                        'formal_domain': 'arbitrary Field; no added q != 0 assumption'}}
    except _Unsupported as error:
        return {**failure, 'reason': str(error)}
