"""Fully consumed tail-product Source and symbolic degree-one factor export."""
import re
from .formal_frontend import _Unsupported, _closed_prefix, _node, _num, _var
from .models import Source
from .recurrence_frontend import RecurrenceParser, _bounded_ast
from .storage import IntegrityError, verify_source

PROFILE = 'poch_tail_factor_interpolation_v1'
_TOKEN = re.compile(r'\s+|:=|[A-Za-z][A-Za-z0-9_]*(?:\.[A-Za-z][A-Za-z0-9_]*)*|[0-9]+|[(){}\[\]:,+*^=\-/]|[ℕℤ≠≤]')


def _tokens(text):
    if len(text) > 65536: raise _Unsupported('source exceeds bounded grammar')
    out, i, depth = [], 0, 0
    while i < len(text):
        pair = text[i:i+2]
        if pair == '/-': depth += 1; out.append(' '); i += 2
        elif pair == '-/' and depth: depth -= 1; out.append(' '); i += 2
        elif not depth and pair == '--':
            end = text.find('\n', i); i = len(text) if end < 0 else end; out.append(' ')
        else: out.append(' ' if depth else text[i]); i += 1
    if depth: raise _Unsupported('unterminated comment')
    clean = ''.join(out); position, tokens = 0, []
    for match in _TOKEN.finditer(clean):
        if match.start() != position: raise _Unsupported('unsupported source token')
        position = match.end()
        if not match.group().isspace(): tokens.append(match.group())
    if position != len(clean) or len(tokens) > 4096: raise _Unsupported('unsupported or oversized syntax')
    return tokens


def lean(node):
    op = node['op']
    if op == 'var': return node['name']
    if op == 'nat': return str(node['value'])
    if op == 'cast': return '(' + lean(node['args'][0]) + ' : ' + node['type'] + ')'
    if op == 'list': return '[' + ', '.join(lean(a) for a in node['args']) + ']'
    if op in ('regular', 'pochList'):
        return '(FiniteQBenchmark.' + op + ' ' + ' '.join(lean(a) for a in node['args']) + ')'
    return '(' + (' ' + op + ' ').join(lean(a) for a in node['args']) + ')'


class InterpolationParser(RecurrenceParser):
    def __init__(self, text): self.tokens, self.pos = _tokens(text), 0

    def name(self):
        value = super().name()
        if value in {'regular', 'pochList'}: raise _Unsupported('reserved source binder')
        return value

    def binder(self):
        self.take('('); names = [self.name()]
        while self.peek() != ':':
            if len(names) > 8: raise _Unsupported('binder group exceeds bound')
            names.append(self.name())
        self.take(':')
        if self.peek() in ('ℕ', 'ℤ', 'True'):
            value = {'op':'var','name':self.take()}
        else: value = self.expr()
        self.take(')')
        return [{'name':name, 'kind':'explicit', 'type':lean(value), 'type_ast':value} for name in names]

    def expr(self, precedence=0, depth=0):
        if depth > 64: raise _Unsupported('expression nesting bound')
        left = self.primary(depth+1)
        operations = {'=':1, '≠':1, '≤':1, '+':2, '-':2, '*':3, '/':3, '^':4}
        while self.peek() in operations and operations[self.peek()] >= precedence:
            op = self.take(); rank = operations[op]
            left = _node(op, left, self.expr(rank if op == '^' else rank+1, depth+1))
        return left

    def primary(self, depth):
        if depth > 64: raise _Unsupported('expression nesting bound')
        if self.peek() == '(':
            self.take(); value = self.expr(depth=depth+1)
            if self.peek() == ':':
                self.take(); ty = self.take()
                if ty != 'ℤ': raise _Unsupported('only original integer exponent casts supported')
                value = {'op':'cast','args':[value],'type':ty}
            self.take(')'); return value
        if self.peek() == '[':
            self.take(); values = []
            while self.peek() != ']':
                values.append(self.expr(depth=depth+1))
                if len(values) > 8: raise _Unsupported('bounded explicit list required')
                if self.peek() != ',': break
                self.take(',')
            self.take(']'); return _node('list', *values)
        if self.peek() in ('regular', 'FiniteQBenchmark.regular', 'pochList', 'FiniteQBenchmark.pochList'):
            op = self.take().split('.')[-1]
            return _node(op, *(self.primary(depth+1) for _ in range(1 if op == 'regular' else 3)))
        return super().primary(depth)


def core_request():
    a, u, v = ({'op':'atom','key':i,'display':name} for i,name in enumerate(('a','u','v')))
    one = {'op':'integer','value':1}
    mul = lambda x,y: {'op':'HMul.hMul','args':[x,y]}
    sub = lambda x,y: {'op':'HSub.hSub','args':[x,y]}
    return {'schema_version':1,'method':'interpolation','input':{'max_degree':1,'goal':{
        'lhs':sub(one,mul(mul(a,u),v)), 'rhs':sub(one,mul(a,mul(u,v))),
        'type':'K','char_zero':False}}}


def analyze_source(source, run_root=None):
    bound = Source.from_dict(source); verify_source(bound, run_root)
    if bound.Gamma != bound.declaration: raise IntegrityError('interpolation original context mismatch')
    failure = {'status':'not_applicable','profile':PROFILE,'source':bound.to_dict()}
    try:
        theorem, field, binders, equation = InterpolationParser(bound.declaration).source()
        _bounded_ast(equation)
        if theorem != bound.theorem: raise IntegrityError('interpolation theorem binding mismatch')
        names = [b['name'] for b in binders if b['name']]
        if len(names) != len(set(names)): raise _Unsupported('duplicate source binder')
        if equation['op'] != '=': raise _Unsupported('source equality required')
        left, right = equation['args']
        tail, quotient = (left,right) if left['op']=='pochList' else (right,left)
        if tail['op']!='pochList' or quotient['op']!='/': raise _Unsupported('tail product and quotient required')
        numerator, denominator = quotient['args']
        if numerator['op']!='pochList' or denominator['op']!='pochList': raise _Unsupported('Pochhammer quotient required')
        params,q,n = numerator['args']
        if params['op']!='list' or len(params['args'])!=1: raise _Unsupported('one original Pochhammer parameter required')
        a = params['args'][0]; k = denominator['args'][2]
        if any(x['op']!='var' for x in (a,q,n,k)) or len({x['name'] for x in (a,q,n,k)})!=4:
            raise _Unsupported('four distinct original scalar and natural variables required')
        cast = {'op':'cast','args':[{'op':'cast','args':[k],'type':'ℤ'}],'type':'ℤ'}
        expected = _node('pochList',_node('list',_node('*',a,_node('^',q,cast))),q,_node('-',n,k))
        if denominator != _node('pochList',params,q,k) or tail != expected:
            raise _Unsupported('source shift, integer exponent, range or denominator differs')
        required = [_node('regular',q),_node('≤',k,n),_node('≠',a,_num(0)),
                    _node('≠',_node('pochList',params,q,k),_num(0))]
        context = {}; found = []
        for binder in binders[2:]:
            ast = binder['type_ast']; ty = binder['type']
            if ty in (field,'ℕ','True'): context[binder['name']] = ty
            elif ast in required:
                # Dependencies must already be present at the original binder position.
                if not all(context.get(x['name']) == t for x,t in ((a,field),(q,field),(n,'ℕ'),(k,'ℕ'))):
                    raise _Unsupported('hypothesis precedes its original typed parameters')
                found.append(ast); context[binder['name']] = 'Prop'
            else: raise _Unsupported('unsupported original binder domain or hypothesis')
        if any(context.get(x['name']) != t for x,t in ((a,field),(q,field),(n,'ℕ'),(k,'ℕ'))):
            raise _Unsupported('source scalar and natural domains differ')
        if any(found.count(h) != 1 for h in required): raise _Unsupported('exact original hypotheses required')
        original = _closed_prefix(binders) + ', ' + lean(equation)
        if bound.proposition is not None and bound.proposition != original:
            raise IntegrityError('interpolation original proposition binding mismatch')
        j = 'qv2j'
        while j in names: j += 'x'
        symbols = {'field':field,'parameter':a['name'],'base':q['name'],'bound':n['name'],'offset':k['name']}
        factor = _node('-',_num(1),_node('*',tail['args'][0]['args'][0],_node('^',q,_var(j))))
        target = _node('-',_num(1),_node('*',a,_node('^',q,_node('+',k,_var(j)))))
        return {'status':'applicable','profile':PROFILE,'source':bound.to_dict(),'binders':binders,
            'symbols':symbols,'factor_index':j,'original_proposition':original,'equation':equation,
            'orientation':'tail_equals_quotient' if tail is left else 'quotient_equals_tail',
            'core_request':core_request(), 'factor_equation':_node('=',factor,target),
            'factor_range':_node('-',n,k),'mapping':{'a':lean(a),'u':lean(_node('^',q,k)),
                'v':lean(_node('^',q,_var(j))), 'integer_power_bridge':'zpow_natCast',
                'combined_power_bridge':'pow_add'},'adds_original_assumptions':False,
            'all_tail_indices':True,'remaining_work':['Product assembly, quotient domain bridge and original equality remain open.']}
    except (_Unsupported, RecursionError) as error:
        return dict(failure,reason=str(error))
