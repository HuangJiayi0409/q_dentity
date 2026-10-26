"""Bounded, read-only inspection of the verified public Lean DAG.

Only the target, its reachable definition bodies, and original context types are
inspected. Proof terms, conversion evidence, theorem IDs and result archives do
not enter mathematical features. No solver, Lean process or CAS is imported.
"""
from collections import Counter
import hashlib
import json
import time

ARITY = {
    'Eq': 2, 'Ne': 2, 'And': 2, 'Or': 2, 'Not': 1, 'Iff': 2,
    'HAdd.hAdd': 2, 'HSub.hSub': 2, 'HMul.hMul': 2, 'HDiv.hDiv': 2,
    'HPow.hPow': 2, 'HSMul.hSMul': 2, 'Neg.neg': 1, 'Inv.inv': 1,
    'LT.lt': 2, 'LE.le': 2, 'Finset.sum': 2, 'Finset.prod': 2,
    'Finset.range': 1, 'Finset.Icc': 2, 'Finset.Ico': 2,
    'Finset.univ': 0, 'Finset.powerset': 1, 'Finset.powersetCard': 2,
    'Matrix.det': 1, 'Matrix.mul': 2, 'Matrix.transpose': 1,
    'Polynomial.coeff': 2, 'PowerSeries.coeff': 2,
    'IsPrimitiveRoot': 2, 'Fin': 1,
    'FiniteQBenchmark.poch': 3, 'FiniteQBenchmark.pochInt': 3,
    'FiniteQBenchmark.pochList': 3, 'FiniteQBenchmark.pochListInt': 3,
    'FiniteQBenchmark.gaussian': 3, 'FiniteQBenchmark.gaussianInt': 3,
    'FiniteQBenchmark.gaussianQuotient': 3,
}
MATH_OBJECTS = {
    'FiniteQBenchmark.phi', 'FiniteQBenchmark.phiDefined',
    'FiniteQBenchmark.rogersSzego', 'FiniteQBenchmark.fineC',
    'FiniteQBenchmark.kacX', 'FiniteQBenchmark.kacM',
    'FiniteQBenchmark.rectangle', 'FiniteQBenchmark.rectangleWeight',
    'FiniteQMacMahon.omegaGE', 'FiniteQMacMahon.omegaAll',
    'FiniteQMacMahon.rectangleSeries', 'FiniteQMacMahon.coneProduct',
    'FiniteQMacMahon.geometric', 'FiniteQMacMahon.gaussianSeries',
}
SCALAR = {'HAdd.hAdd', 'HSub.hSub', 'HMul.hMul', 'HDiv.hDiv',
          'HPow.hPow', 'Neg.neg', 'Inv.inv', 'Nat.cast', 'Int.cast',
          'Int.ofNat', 'OfNat.ofNat', 'OfScientific.ofScientific'}
SAFE_ATOMS = {'Nat', 'Int', 'Rat', 'Real', 'Complex', 'True', 'False'}


class FeatureLimit(ValueError):
    pass


def name(node):
    parts = []
    for _ in range(128):
        if node.get('tag') == 'anonymous': return '.'.join(reversed(parts))
        if node.get('tag') not in ('str', 'num'): raise ValueError('invalid Lean name')
        parts.append(str(node['value'])); node = node['prefix']
    raise FeatureLimit('name_depth_limit')


class Graph:
    def __init__(self, standard, *, seconds=5., max_nodes=100000):
        if standard.get('schema_version') != 'finite-q-preprocess/2':
            raise ValueError('unsupported preprocessing schema')
        if standard.get('status') not in ('verified_normalized', 'verified_unchanged'):
            raise ValueError('unverified preprocessing input')
        self.data = standard; self.nodes = standard['nodes']
        if not isinstance(self.nodes, dict) or len(self.nodes) > max_nodes:
            raise FeatureLimit('representation_node_limit')
        self.deadline = time.monotonic()+seconds
        self.steps = 0; self.max_steps = max_nodes*20
        self.app_cache = {}; self.token_cache = {}
        self.definitions = {name(d['name']): d['body'] for d in standard.get('declarations', [])
                            if d.get('kind') == 'definition' and 'body' in d}

    def tick(self):
        self.steps += 1
        if self.steps > self.max_steps or time.monotonic() >= self.deadline:
            raise FeatureLimit('feature_inspection_budget')

    def node(self, key):
        self.tick()
        if key not in self.nodes: raise ValueError('dangling expression reference')
        return self.nodes[key]

    def application(self, key):
        if key in self.app_cache: return self.app_cache[key]
        original = key; args = []; seen = set()
        while True:
            if key in seen: raise ValueError('cyclic expression')
            seen.add(key); node = self.node(key)
            if node['constructor'] != 'app': break
            args.append(node['arg']); key = node['fn']
        args.reverse()
        head = name(node['name']) if node['constructor'] == 'const' else '@'+node['constructor']
        result = head, args, key
        self.app_cache[original] = result
        return result

    def operands(self, key):
        head, args, _ = self.application(key)
        if head in ARITY:
            arity = ARITY[head]
            signature = self.data.get('signatures', {}).get(head)
            if signature and len(args) != len(signature['binders']):
                return head, [], False
            if len(args) < arity: return head, [], False
            return head, args[-arity:] if arity else [], True
        signature = self.data.get('signatures', {}).get(head)
        if signature and len(args) == len(signature['binders']):
            return head, [a for a, b in zip(args, signature['binders'])
                          if b['binder_info'] == 'explicit'], True
        return head, args, head in MATH_OBJECTS or head in SCALAR

    def numeral(self, key):
        node = self.node(key)
        if node['constructor'] == 'nat': return node['value']
        head, args, _ = self.application(key)
        if head == 'OfNat.ofNat' and len(args) == 3:
            n = self.node(args[1])
            if n['constructor'] == 'nat': return n['value']
        return None

    def token(self, key, depth=0, stack=()):
        """Scope-aware symbolic token, only for exact side-condition matching."""
        cache_key = key, depth
        if cache_key in self.token_cache: return self.token_cache[cache_key]
        if key in stack: raise ValueError('cyclic expression')
        if len(stack) >= 80: raise FeatureLimit('term_depth_limit')
        node = self.node(key); tag = node['constructor']
        n = self.numeral(key)
        if n is not None: result = ('number', n)
        elif tag == 'bvar':
            index = node['index']
            result = ('bound', index) if index < depth else ('parameter', index-depth)
        elif tag == 'const': result = ('constant', name(node['name']))
        elif tag == 'app':
            head, args, ok = self.operands(key)
            if not ok: result = ('opaque', key)  # No equality inference through opaque terms.
            else: result = (head, tuple(self.token(a, depth, stack+(key,)) for a in args))
        else: result = ('opaque', key)
        self.token_cache[cache_key] = result
        return result

    def inspect(self):
        key = self.data['normalized']; closed_binders = 0; seen = set()
        while self.node(key)['constructor'] == 'forall':
            if key in seen: raise ValueError('cyclic expression')
            seen.add(key); closed_binders += 1
            if closed_binders > 512: raise FeatureLimit('context_depth_limit')
            key = self.node(key)['body']
        self.target = key
        head, operands, complete = self.operands(key)
        self.target_head = head
        self.sides = operands if head == 'Eq' and complete else []
        self.constants = set(); self.direct_constants = set(); self.unknown = set()
        self.objects = []; self.definition_expansions = set(); self.visited = set()
        self.scalar_grammar = bool(self.sides); self.fin_sizes = []; self.dimensions = []
        # Never traverse bridge_type, transformations, evidence, or unused declarations.
        stack = [(a, 0, 0, ()) for a in (self.sides or [key])]
        while stack:
            k, depth, expansion, ancestors = stack.pop()
            self.tick()
            if k in ancestors: raise ValueError('cyclic expression')
            if len(ancestors) > 160: raise FeatureLimit('expression_depth_limit')
            visit = k, depth, expansion
            if visit in self.visited: continue
            self.visited.add(visit)
            node = self.node(k); tag = node['constructor']
            if tag in ('nat', 'bvar'): continue
            if tag == 'lam':
                stack.append((node['body'], depth+1, expansion, ancestors+(k,))); continue
            if tag in ('forall', 'let', 'proj', 'sort', 'string'):
                self.unknown.add('@'+tag); self.scalar_grammar = False; continue
            op, args, ok = self.operands(k)
            self.constants.add(op)
            if expansion == 0: self.direct_constants.add(op)
            if self.numeral(k) is not None: continue
            if op not in SCALAR: self.scalar_grammar = False
            if op in ('Finset.sum', 'Finset.prod') and ok:
                domain, _ = args
                dh, da, dok = self.operands(domain)
                self.objects.append(dict(kind=op, node=k, domain=dh,
                    bound=da[-1] if da and dok else None, depth=depth, expansion=expansion))
            if op in ('Finset.sum', 'Finset.prod', 'Matrix.det'):
                _, full, _ = self.application(k)
                if full:
                    th, ta, tok = self.operands(full[0])
                    if th == 'Fin' and tok:
                        size=self.numeral(ta[0]);self.fin_sizes.append(size)
                        self.dimensions.append(dict(kind=op,node=k,size=size,top_level=k in self.sides,expansion=expansion))
            if op not in ARITY and op not in SCALAR and op not in SAFE_ATOMS:
                if op in self.definitions and expansion < 2:
                    self.definition_expansions.add(op)
                    stack.append((self.definitions[op], 0, expansion+1, ancestors+(k,)))
                if op not in MATH_OBJECTS: self.unknown.add(op)
            if not ok and op not in SAFE_ATOMS:
                self.unknown.add(op)
            stack.extend((a, depth, expansion, ancestors+(k,)) for a in args)
        self.hypotheses = []; self.context_constants = set(); self.natural_parameters = 0
        _, target_arguments, _ = self.application(self.target)
        scalar_type = target_arguments[0] if head == 'Eq' and len(target_arguments) == 3 else None
        scalar_token = self.token(scalar_type) if scalar_type is not None else None
        scalar_head = self.operands(scalar_type)[0] if scalar_type is not None else None
        self.domain = dict(field=scalar_head in ('Rat','Real','Complex'),
                           char_zero=scalar_head in ('Rat','Real','Complex'), evidence=[])
        for row in self.data.get('context', []):
            self.tick()
            ref = row.get('type_in_full_context', {}).get('expression')
            if ref is None: continue
            th, _, _ = self.operands(ref)
            _, full_args, _ = self.application(ref)
            if th in ('Field','CharZero') and full_args and self.token(full_args[0]) == scalar_token:
                self.domain['field' if th=='Field' else 'char_zero'] = True
                self.domain['evidence'].append(ref)
            if row.get('role') == 'parameter' and th == 'Nat': self.natural_parameters += 1
            if row.get('role') not in ('hypothesis', 'assumption'): continue
            pending = [ref]; visited = set()
            while pending:
                fact = pending.pop()
                if fact in visited: continue
                visited.add(fact)
                fh, fa, fok = self.operands(fact)
                self.context_constants.add(fh)
                if fh == 'And' and fok: pending.extend(fa)
                else: self.hypotheses.append((fact, self.token(fact)))
        return self

    def root_product(self):
        """Recognize exactly prod (1-x*w^j)=1-x^m, including reversed equality."""
        if len(self.sides) != 2: return None
        for product, other in (self.sides, list(reversed(self.sides))):
            op, args, ok = self.operands(product)
            if op != 'Finset.prod' or not ok: continue
            dh, da, dok = self.operands(args[0]); fn = self.node(args[1])
            if dh != 'Finset.range' or not dok or fn['constructor'] != 'lam': continue
            body = self.token(fn['body'], 1); order = self.token(da[0])
            if body[0] != 'HSub.hSub' or body[1][0] != ('number', 1): continue
            mul = body[1][1]
            if mul[0] != 'HMul.hMul': continue
            for x, power in (mul[1], tuple(reversed(mul[1]))):
                if power[0] != 'HPow.hPow' or power[1][1] != ('bound', 0): continue
                if self._contains_bound(x) or self._contains_bound(power[1][0]): continue
                expected = ('HSub.hSub', (('number', 1), ('HPow.hPow', (x, order))))
                if self.token(other) == expected:
                    root = power[1][0]
                    positive = ('LT.lt', (('number', 0), order))
                    primitive = ('IsPrimitiveRoot', (root, order))
                    tokens = {t for _, t in self.hypotheses}
                    n = self.numeral(da[0])
                    return dict(node=product,
                        positive=positive in tokens or (n is not None and n > 0),
                        primitive=primitive in tokens,
                        positive_evidence=[k for k,t in self.hypotheses if t == positive],
                        primitive_evidence=[k for k,t in self.hypotheses if t == primitive])
        return None

    @staticmethod
    def _contains_bound(value):
        return isinstance(value, tuple) and (bool(value) and value[0] == 'bound'
                or any(Graph._contains_bound(v) for v in value))

    def summary(self):
        root = self.root_product()
        result = dict(goal_head=self.target_head, target_node=self.target,
            side_heads=[self.operands(k)[0] for k in self.sides],
            symbols=sorted(self.constants), direct_symbols=sorted(self.direct_constants),
            unknown_symbols=sorted(self.unknown), objects=self.objects,
            natural_parameter_count=self.natural_parameters, fin_sizes=self.fin_sizes,
            dimensions=self.dimensions,
            scalar_grammar=self.scalar_grammar,
            scalar_domain=self.domain,
            context_predicates=sorted(self.context_constants),
            inspected_nodes=len(self.visited), definition_expansions=sorted(self.definition_expansions),
            root_product=root,
            counts=dict(Counter(x['kind'] for x in self.objects)))
        result['feature_sha256'] = hashlib.sha256(json.dumps(result, sort_keys=True).encode()).hexdigest()
        return result


def extract(standard, **limits):
    return Graph(standard, **limits).inspect().summary()
