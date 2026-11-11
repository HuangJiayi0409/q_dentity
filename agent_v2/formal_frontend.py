"""A fully consumed, typed finite grammar for one Gaussian finite-sum family.

This is deliberately not a general Lean parser. Unknown commands, binders,
hypotheses and arithmetic return not_applicable. The full original bytes stay
bound to the request; generated expressions remain untrusted until Lean checks.
"""
import re

from .models import Source
from .storage import IntegrityError, verify_source


PROFILE = 'gaussian_weighted_range_v1'
_TOKEN = re.compile(r'\s+|:=|[A-Za-z][A-Za-z0-9_]*(?:\.[A-Za-z][A-Za-z0-9_]*)*|[0-9]+|[(){}\[\]:,+*^=−\-/]|[ℕℤ∑∈≠]')
_NAME = re.compile(r'[A-Za-z][A-Za-z0-9_]*')
_RESERVED = set('Type Field True False Nat gaussian forall fun by theorem variable namespace end u'.split())


class _Unsupported(ValueError):
    pass


def _tokens(text):
    if len(text) > 65536:
        raise _Unsupported('source exceeds the finite grammar size limit')
    # Nested comments are removed lexically, never interpreted as source.
    clean, i, depth = [], 0, 0
    while i < len(text):
        pair = text[i:i+2]
        if pair == '/-':
            depth += 1; clean.append(' '); i += 2
        elif pair == '-/' and depth:
            depth -= 1; clean.append(' '); i += 2
        elif not depth and pair == '--':
            end = text.find('\n', i)
            i = len(text) if end < 0 else end
            clean.append(' ')
        else:
            clean.append(' ' if depth else text[i]); i += 1
    if depth:
        raise _Unsupported('unterminated source comment')
    clean = ''.join(clean)
    position, result = 0, []
    for match in _TOKEN.finditer(clean):
        if match.start() != position:
            raise _Unsupported('unsupported source token')
        token = match.group(); position = match.end()
        if not token.isspace(): result.append(token)
    if position != len(clean) or len(result) > 4096:
        raise _Unsupported('unsupported or oversized source syntax')
    return result


def _var(name):
    return {'op': 'var', 'name': name}


def _num(value):
    return {'op': 'nat', 'value': value}


def _node(op, *args):
    return {'op': op, 'args': list(args)}


class _Parser:
    def __init__(self, text):
        self.tokens = _tokens(text)
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def take(self, expected=None):
        token = self.peek()
        if token is None or expected is not None and token != expected:
            raise _Unsupported('unsupported declaration structure; expected ' + str(expected))
        self.pos += 1
        return token

    def name(self):
        token = self.take()
        if len(token) > 64 or not _NAME.fullmatch(token) or token in _RESERVED:
            raise _Unsupported('unsupported or reserved binder name')
        return token

    def sequence(self, *tokens):
        for token in tokens: self.take(token)

    def binder(self):
        self.take('(')
        names = [self.name()]
        while self.peek() != ':':
            if len(names) > 8: raise _Unsupported('too many binder names')
            names.append(self.name())
        self.take(':'); kind = self.take(); self.take(')')
        return [{'name': name, 'type': kind, 'kind': 'explicit'} for name in names]

    def expr(self, precedence=0, depth=0):
        if depth > 64: raise _Unsupported('expression nesting limit')
        left = self.primary(depth+1)
        operators = {'=': 1, '+': 2, '-': 2, '*': 3, '/': 3, '^': 4}
        while self.peek() in operators and operators[self.peek()] >= precedence:
            op = self.take(); rank = operators[op]
            right = self.expr(rank if op == '^' else rank+1, depth+1)
            left = _node(op, left, right)
        return left

    def primary(self, depth):
        if depth > 64: raise _Unsupported('expression nesting limit')
        token = self.peek()
        if token == '(':
            self.take(); value = self.expr(depth=depth+1); self.take(')'); return value
        if token in ('gaussian', 'FiniteQBenchmark.gaussian'):
            self.take()
            return _node('gaussian', *(self.primary(depth+1) for _ in range(3)))
        if token == '∑':
            self.take(); index = self.name()
            self.sequence('∈', 'Finset.range', '(')
            bound = self.expr(depth=depth+1); self.sequence(')', ',')
            return {'op': 'sum', 'index': index, 'range': _node('Finset.range', bound),
                    'body': self.expr(depth=depth+1)}
        if token and token.isdecimal():
            self.take()
            if len(token) > 5: raise _Unsupported('oversized natural literal')
            return _num(int(token))
        return _var(self.name())

    def source(self):
        imports = []
        while self.peek() == 'import':
            self.take(); module = self.take()
            if module not in {'Benchmark.Batch3Proofs', 'Benchmark.Gaussian'}:
                raise _Unsupported('source import outside the supported structural profile')
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
        return namespace + '.' + theorem, field, binders, proposition, imports


def _typecheck(node, names, field, depth=0):
    if depth > 64: raise _Unsupported('typed expression nesting limit')
    op = node['op']
    if op == 'var':
        if node['name'] not in names: raise _Unsupported('unbound expression variable')
        return names[node['name']]
    if op == 'nat': return 'ℕ'
    if op == 'sum':
        if node['index'] in names: raise _Unsupported('sum binder shadows original context')
        if _typecheck(node['range']['args'][0], names, field, depth+1) != 'ℕ':
            raise _Unsupported('non-natural range')
        return _typecheck(node['body'], {**names, node['index']: 'ℕ'}, field, depth+1)
    types = [_typecheck(arg, names, field, depth+1) for arg in node['args']]
    if op == 'gaussian' and types == [field, 'ℕ', 'ℕ']: return field
    if op == '^' and types == [field, 'ℕ']: return field
    if op in ('+', '-', '*') and len(set(types)) == 1 and types[0] in ('ℕ', field): return types[0]
    if op == '=' and types == [field, field]: return 'Prop'
    raise _Unsupported('unsupported typed arithmetic')


def _lean(node):
    if node['op'] == 'var': return node['name']
    if node['op'] == 'nat': return str(node['value'])
    if node['op'] == 'gaussian':
        return '(FiniteQBenchmark.gaussian ' + ' '.join(_lean(a) for a in node['args']) + ')'
    if node['op'] == 'sum':
        return '(∑ ' + node['index'] + ' ∈ Finset.range ' + _lean(node['range']['args'][0]) + ', ' + _lean(node['body']) + ')'
    return '(' + (' ' + node['op'] + ' ').join(_lean(a) for a in node['args']) + ')'


def _closed_prefix(binders):
    pieces = []
    for binder in binders:
        if binder['kind'] == 'instance': pieces.append('[' + binder['type'] + ']')
        else:
            left, right = ('{', '}') if binder['kind'] == 'implicit' else ('(', ')')
            pieces.append(left + binder['name'] + ' : ' + binder['type'] + right)
    return '∀ ' + ' '.join(pieces)


def analyze_source(source: dict, run_root=None) -> dict:
    """Recognize one explicit family without any identity-name dispatch.

    Integrity failures raise IntegrityError. Supportedness failures return an
    ordinary not_applicable record, retaining the complete source binding.
    """
    bound = Source.from_dict(source)
    verify_source(bound, run_root)
    if bound.Gamma != bound.declaration:
        raise IntegrityError('frontend original context binding mismatch')
    failure = {'status': 'not_applicable', 'profile': PROFILE, 'source': bound.to_dict()}
    try:
        theorem, field, binders, ast, imports = _Parser(bound.declaration).source()
        if theorem != bound.theorem: raise IntegrityError('frontend theorem binding mismatch')
        explicit = binders[2:]
        names = [b['name'] for b in binders if b['name'] is not None]
        if len(set(names)) != len(names): raise _Unsupported('duplicate original binder')
        if any(b['type'] not in (field, 'ℕ', 'True') for b in explicit):
            raise _Unsupported('unknown original parameter domain or hypothesis')
        context = {b['name']: b['type'] for b in explicit}
        if _typecheck(ast, context, field) != 'Prop' or ast['op'] != '=':
            raise _Unsupported('a field equality is required')
        left, right = ast['args']
        summation, target, orientation = (right, left, 'target_equals_sum') if right['op'] == 'sum' else (left, right, 'sum_equals_target')
        if summation['op'] != 'sum': raise _Unsupported('a complete finite range sum is required')
        body, index, length = summation['body'], summation['index'], summation['range']['args'][0]
        if body['op'] != '*' or body['args'][0]['op'] != '^' or body['args'][1]['op'] != 'gaussian':
            raise _Unsupported('expected a q-power weighted Gaussian summand')
        weight, atom = body['args']
        if weight['args'][0]['op'] != 'var' or atom['args'][2]['op'] != 'var':
            raise _Unsupported('variable base and lower index required')
        base, offset = weight['args'][0]['name'], atom['args'][2]['name']
        if length['op'] != '+' or length['args'][0]['op'] != 'var':
            raise _Unsupported('range must have the exact natural prefix n+1')
        end = length['args'][0]['name']
        if (weight != _node('^', _var(base), _var(index)) or
                atom != _node('gaussian', _var(base), _node('+', _var(offset), _var(index)), _var(offset)) or
                length != _node('+', _var(end), _num(1)) or
                target != _node('gaussian', _var(base), _node('+', _node('+', _var(end), _var(offset)), _num(1)),
                                _node('+', _var(offset), _num(1)))):
            raise _Unsupported('weighted Gaussian finite-prefix structure does not match')
        if len({base, offset, end, index, field}) != 5:
            raise _Unsupported('mathematical roles overlap')
        assumptions = [b for b in explicit if b['type'] == 'True']
        if (len(explicit) != 4 or len(assumptions) != 1 or
                context.get(base) != field or context.get(offset) != 'ℕ' or context.get(end) != 'ℕ'):
            raise _Unsupported('complete Field/base/two-natural/True context required')
        prefix = _closed_prefix(binders)
        original = prefix + ', ' + _lean(ast)
        if bound.proposition is not None and bound.proposition != original:
            raise IntegrityError('frontend original proposition binding mismatch')
        local = (prefix + f' ({index} : ℕ), FiniteQBenchmark.gaussian {base} ({offset} + ({index} + 1)) ({offset} + 1) - '
                 f'FiniteQBenchmark.gaussian {base} ({offset} + {index}) ({offset} + 1) = '
                 f'{base} ^ {index} * FiniteQBenchmark.gaussian {base} ({offset} + {index}) {offset}')
        result = {'status': 'applicable', 'profile': PROFILE, 'source': bound.to_dict(),
                  'reason': {'code': 'supported_structure'}, 'binders': binders, 'ast': ast,
                  'original_proposition': original, 'local_proposition': local,
                  'context': {'raw': bound.Gamma, 'binders': binders, 'assumptions': assumptions,
                              'additional_hypotheses': [], 'domain': 'arbitrary Field; all original q values'},
                  'summation': summation, 'orientation': orientation,
                  'symbols': {'field': field, 'base': base, 'offset': offset, 'bound': end,
                              'assumption': assumptions[0]['name'], 'index': index},
                  'mapping': {'q': {'lean': base, 'type': field},
                              'a': {'lean': f'{base} ^ ({offset} + 1)', 'type': field},
                              'X': {'lean': f'{base} ^ {index}', 'type': field}},
                  'core_request': {'schema_version': 1, 'solver': 'q_gosper', 'input': {
                      'k_shift': ['div', ['mul', 'q', ['sub', 1, ['mul', 'a', 'X']]],
                                  ['sub', 1, ['mul', 'q', 'X']]]}},
                  'semantic_anchors': {'theorem': theorem, 'source_sha256': bound.sha256,
                      'source_imports': imports, 'sum_body': body, 'sum_range': summation['range'],
                      'specialization_policy': 'generic rational search only; denominator-free local theorem must be checked in original Field'}}
        verify_source(bound, run_root)
        return result
    except _Unsupported as error:
        verify_source(bound, run_root)
        return {**failure, 'reason': {'code': 'not_applicable', 'message': str(error)}}
