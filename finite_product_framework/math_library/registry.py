"""Typed catalogue validation, lookup and bounded untrusted instantiation."""
import copy
import hashlib
import json
import re
from pathlib import Path

from .catalog import SCHEMA, OBJECTS, RULES


class LibraryError(ValueError):
    pass


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def digest(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def names(tree):
    found = set()
    def visit(t, depth=0):
        if depth > 128:
            raise LibraryError('expression_depth_limit')
        if isinstance(t, dict):
            if isinstance(t.get('name'), str): found.add(t['name'])
            for v in t.values(): visit(v, depth+1)
        elif isinstance(t, list):
            for v in t: visit(v, depth+1)
    visit(tree)
    return found


def _source(op, *args):
    return dict(op=op, args=list(args))


def _integer(node):
    if node.get('op') == 'nat': return node['value']
    if node.get('op') == 'Neg.neg':
        value = _integer(node['args'][0])
        return None if value is None else -value
    return None


def _number(value):
    n = dict(op='nat', value=abs(value))
    return n if value >= 0 else _source('Neg.neg', n)


class Library:
    def __init__(self, rules=None):
        self._objects = copy.deepcopy(OBJECTS)
        rows = copy.deepcopy(RULES if rules is None else rules)
        self._rules = {}
        for row in rows:
            self._validate(row)
            if row['id'] in self._rules: raise LibraryError('duplicate_rule_id')
            self._rules[row['id']] = row
        self.sha256 = digest(dict(schema=SCHEMA, objects=self._objects, rules=rows))

    @property
    def objects(self):
        return copy.deepcopy(self._objects)

    @property
    def rules(self):
        return copy.deepcopy(self._rules)

    def _sort(self, tree, params, bound, algebra, depth=0):
        if depth > 64: raise LibraryError('template_depth_limit')
        sub = lambda t, b=bound: self._sort(t, params, b, algebra, depth+1)
        if isinstance(tree, str):
            if tree.startswith('$') and tree[1:] in params: return params[tree[1:]]
            if tree.startswith('@') and tree[1:] in bound: return bound[tree[1:]]
            raise LibraryError('unbound_template_variable: '+tree)
        if not isinstance(tree, list) or not tree: raise LibraryError('invalid_template')
        op,*args = tree
        if op == 'literal' and len(args)==2:
            sort,value=args
            if sort not in ('Nat','Int','K') or type(value) is not int or (sort=='Nat' and value<0):
                raise LibraryError('invalid_literal')
            return sort
        if op == 'call' and args:
            obj=self._objects.get(args[0])
            if obj is None or [sub(x) for x in args[1:]] != obj['arguments']:
                raise LibraryError('invalid_object_signature: '+str(args[0]))
            if obj['algebra']=='Field' and algebra!='Field':
                raise LibraryError('object_requires_field')
            return obj['result']
        if op in ('sum_range','prod_range','sum_Ico','sum_Icc'):
            width=1 if op.endswith('range') else 2
            if len(args)!=width+2 or any(sub(x)!='Nat' for x in args[:width]):
                raise LibraryError('invalid_finite_domain')
            binder=args[width]
            if not isinstance(binder,str) or not re.fullmatch(r'[a-z][a-z0-9_]*',binder) or binder in bound or binder in params:
                raise LibraryError('invalid_template_binder')
            if sub(args[-1],dict(bound,**{binder:'Nat'}))!='K':
                raise LibraryError('invalid_bound_body')
            return 'K'
        signatures={
            'nat_add':(['Nat','Nat'],'Nat'), 'nat_sub':(['Nat','Nat'],'Nat'),
            'nat_mul':(['Nat','Nat'],'Nat'), 'nat_div':(['Nat','Nat'],'Nat'),
            'int_add':(['Int','Int'],'Int'), 'int_sub':(['Int','Int'],'Int'),
            'add':(['K','K'],'K'), 'sub':(['K','K'],'K'), 'mul':(['K','K'],'K'),
            'div':(['K','K'],'K'), 'neg':(['K'],'K'), 'pow':(['K','Nat'],'K'),
            'zpow':(['K','Int'],'K'), 'nil':([], 'ListK'), 'cons':(['K','ListK'],'ListK'),
            'length_int':(['ListK'],'Int'), 'apply':(['NatToK','Nat'],'K')}
        if op in ('eq','ne') and len(args)==2 and sub(args[0])==sub(args[1]): return 'Prop'
        if op not in signatures or [sub(x) for x in args]!=signatures[op][0]:
            raise LibraryError('invalid_typed_operator: '+str(op))
        if op in ('div','zpow') and algebra!='Field': raise LibraryError('operator_requires_field')
        return signatures[op][1]

    def _validate(self,row):
        if not re.fullmatch(r'[A-Za-z][A-Za-z0-9_]*',row.get('id','')): raise LibraryError('invalid_rule_id')
        if row.get('method_core') is not False: raise LibraryError('method_core_not_allowed')
        if row.get('algebra') not in ('CommRing','Field'): raise LibraryError('unsupported_algebra')
        params={p['name']:p['sort'] for p in row['parameters']}
        if len(params)!=len(row['parameters']) or any(not re.fullmatch(r'[a-z][a-zA-Z0-9_]*',n) for n in params):
            raise LibraryError('invalid_parameters')
        if any(s not in ('K','Nat','Int','ListK','NatToK') for s in params.values()):
            raise LibraryError('invalid_parameter_sort')
        left=self._sort(row['lhs'],params,{},row['algebra'])
        right=self._sort(row['rhs'],params,{},row['algebra'])
        if left!=right: raise LibraryError('rule_sort_mismatch')
        if any(self._sort(h,params,{},row['algebra'])!='Prop' for h in row['requires']):
            raise LibraryError('invalid_side_condition')
        if (row['lean']['name']!='FiniteQMathLibrary.'+row['id'] or
            row['lean'].get('module')!='Benchmark.MathLibraryRules' or
            row['lean'].get('source')!='finite_product_framework/math_library/lean/Rules.lean'):
            raise LibraryError('invalid_lean_reference')

    def lookup(self,symbol,purpose=None):
        """Exact Lean identity or an explicitly registered short-name alias."""
        symbol=symbol if '.' in symbol else 'FiniteQBenchmark.'+symbol
        rows=[copy.deepcopy(r) for r in self._rules.values()
              if r['subject']==symbol and (purpose is None or r['purpose']==purpose)]
        return dict(schema=SCHEMA,symbol=symbol,status='found' if rows else 'unknown',
                    object=copy.deepcopy(self._objects.get(symbol)),rules=rows,catalog_sha256=self.sha256,
                    applicability='must_check_original_types_and_conditions_in_Lean')

    def instantiate(self,key,bindings,*,facts=(),avoid=()):
        if key not in self._rules: raise LibraryError('unknown_rule: '+key)
        row=self._rules[key]
        if set(bindings)!={p['name'] for p in row['parameters']}:
            raise LibraryError('binding_names_mismatch')
        for value in bindings.values():validate_source(value)
        for fact in facts:validate_source(fact)
        used=set(avoid)|names(bindings)
        lhs=self._instantiate(row['lhs'],bindings,{},used)
        rhs=self._instantiate(row['rhs'],bindings,{},used)
        requirements=[self._instantiate(h,bindings,{},used) for h in row['requires']]
        supplied={canonical(f) for f in facts}
        unresolved=[h for h in requirements if canonical(h) not in supplied]
        return dict(rule=key,lhs=lhs,rhs=rhs,requires=requirements,unresolved=unresolved,
                    status='conditions_unresolved' if unresolved else 'candidate',
                    binding_types=copy.deepcopy(row['parameters']),
                    lean=copy.deepcopy(row['lean']),catalog_sha256=self.sha256,
                    proof_status='requires_Lean_replay',
                    condition_evidence='caller_supplied_facts_are_not_proof_certificates')

    def _instantiate(self,tree,bindings,bound,used):
        if isinstance(tree,str):
            if tree.startswith('$'): return copy.deepcopy(bindings[tree[1:]])
            return dict(op='var',name=bound[tree[1:]])
        op,*args=tree
        sub=lambda x:self._instantiate(x,bindings,bound,used)
        if op=='literal': return _number(args[1])
        if op=='call': return _source(args[0],*(sub(a) for a in args[1:]))
        if op in ('sum_range','prod_range','sum_Ico','sum_Icc'):
            width=1 if op.endswith('range') else 2
            binder=args[width]; fresh='ml_'+binder
            while fresh in used:fresh+='x'
            used.add(fresh)
            domain=_source({'sum_range':'Finset.range','prod_range':'Finset.range',
                            'sum_Ico':'Finset.Ico','sum_Icc':'Finset.Icc'}[op],*(sub(a) for a in args[:width]))
            body=self._instantiate(args[-1],bindings,dict(bound,**{binder:fresh}),used)
            return _source('Finset.prod' if op=='prod_range' else 'Finset.sum',domain,
                           dict(op='lambda',name=fresh,body=body))
        values=[sub(a) for a in args]
        if op=='length_int':
            current=values[0];length=0
            while current.get('op')=='List.cons':
                length+=1;current=current['args'][1]
                if length>4096:raise LibraryError('list_length_limit')
            if current.get('op')=='List.nil':return _number(length)
            return _source('Int.ofNat',_source('List.length',values[0]))
        if op in ('int_add','int_sub','nat_add','nat_sub','nat_mul','nat_div'):
            x,y=map(_integer,values)
            if x is not None and y is not None:
                if op.endswith('add'):return _number(x+y)
                if op.endswith('sub'):return _number(max(0,x-y) if op=='nat_sub' else x-y)
                if op=='nat_mul':return _number(x*y)
                if op=='nat_div':return _number(x//y if y else 0)
        operations={'add':'HAdd.hAdd','sub':'HSub.hSub','mul':'HMul.hMul','div':'HDiv.hDiv',
            'nat_add':'HAdd.hAdd','nat_sub':'HSub.hSub','nat_mul':'HMul.hMul','nat_div':'HDiv.hDiv',
            'int_add':'HAdd.hAdd','int_sub':'HSub.hSub','neg':'Neg.neg','pow':'HPow.hPow','zpow':'HPow.hPow',
            'nil':'List.nil','cons':'List.cons','eq':'Eq','ne':'Ne','apply':'math_library.apply'}
        result=_source(operations[op],*values)
        if op=='zpow':result['exponent_sort']='Int'
        return result

    def lean_expression(self,tree):
        """Render only validated catalogue templates, never arbitrary source text."""
        if isinstance(tree,str):return tree[1:]
        op,*args=tree
        sub=self.lean_expression
        if op=='literal':return f'({args[1]} : '+{'K':'K','Nat':'ℕ','Int':'ℤ'}[args[0]]+')'
        if op=='call':return '('+args[0]+' '+' '.join(sub(a) for a in args[1:])+')'
        if op in ('sum_range','prod_range','sum_Ico','sum_Icc'):
            width=1 if op.endswith('range') else 2
            domain={'sum_range':'Finset.range','prod_range':'Finset.range','sum_Ico':'Finset.Ico','sum_Icc':'Finset.Icc'}[op]
            return '('+('∏' if op=='prod_range' else '∑')+' '+args[width]+' ∈ '+domain+' '+\
                ' '.join('('+sub(a)+')' for a in args[:width])+', '+sub(args[-1])+')'
        if op=='length_int':return '(('+sub(args[0])+').length : ℤ)'
        if op=='nil':return '([] : List K)'
        if op=='cons':return '('+sub(args[0])+' :: '+sub(args[1])+')'
        if op=='apply':return '('+sub(args[0])+' '+sub(args[1])+')'
        if op=='neg':return '(-'+sub(args[0])+')'
        binary={'add':'+','sub':'-','mul':'*','div':'/','pow':'^','zpow':'^','eq':'=','ne':'≠',
                'nat_add':'+','nat_sub':'-','nat_mul':'*','nat_div':'/','int_add':'+','int_sub':'-'}
        return '('+sub(args[0])+' '+binary[op]+' '+sub(args[1])+')'

    def lean_check(self,key,*,rhs=None):
        row=self._rules[key]
        sorts={'K':'K','Nat':'ℕ','Int':'ℤ','ListK':'List K','NatToK':'ℕ → K'}
        params=' '.join('('+p['name']+' : '+sorts[p['sort']]+')' for p in row['parameters'])
        requirements=' '.join('(h'+str(i)+' : '+self.lean_expression(h)+')' for i,h in enumerate(row['requires']))
        args=' '.join([p['name'] for p in row['parameters']]+['h'+str(i) for i in range(len(row['requires']))])
        target=self.lean_expression(row['lhs'])+' = '+self.lean_expression(row['rhs'] if rhs is None else rhs)
        return (f'theorem check_{key} {{K : Type*}} [{row["algebra"]} K] {params} {requirements} :\n'
                f'    {target} := by\n  exact {row["lean"]["name"]} {args}\n'
                f'#print axioms check_{key}\n')


def dependency_files():
    """Include data and interpreters in every consuming method's freeze manifest."""
    return sorted(p for p in Path(__file__).parent.rglob('*') if p.suffix in ('.py','.lean'))


def validate_source(tree):
    """Validate container shape; source types remain Lean replay obligations."""
    count=0
    def visit(node,depth=0):
        nonlocal count
        count+=1
        if depth>128 or count>20000:raise LibraryError('source_expression_budget')
        if not isinstance(node,dict) or not isinstance(node.get('op'),str):raise LibraryError('invalid_source_node')
        if node['op']=='nat' and (type(node.get('value')) is not int or node['value']<0):
            raise LibraryError('invalid_natural_literal')
        if node['op'] in ('var','lambda','forall') and not isinstance(node.get('name'),str):
            raise LibraryError('invalid_source_name')
        if not isinstance(node.get('args',[]),list):raise LibraryError('invalid_source_arguments')
        for arg in node.get('args',[]):visit(arg,depth+1)
        if 'body' in node:visit(node['body'],depth+1)
    visit(tree)
