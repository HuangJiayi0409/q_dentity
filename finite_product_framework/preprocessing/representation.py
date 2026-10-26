"""Lossless public DAG plus method-neutral object annotations.

The Lean wire tree is authoritative; the DAG does not erase implicit arguments,
universes, typeclass instances, dependent binder types, or unknown constants.
"""
import hashlib
import json

SYMBOLS = {
    'HAdd.hAdd': ('add', 2), 'HSub.hSub': ('subtract', 2),
    'HMul.hMul': ('multiply', 2), 'HDiv.hDiv': ('divide', 2),
    'HPow.hPow': ('power', 2), 'Neg.neg': ('negate', 1),
    'Eq': ('equal', 2), 'Ne': ('not_equal', 2), 'And': ('and', 2),
    'Or': ('or', 2), 'Not': ('not', 1), 'Iff': ('iff', 2),
    'LE.le': ('less_equal', 2), 'LT.lt': ('less', 2),
    'Finset.sum': ('finite_sum', 2), 'Finset.prod': ('finite_product', 2),
    'Finset.range': ('nat_prefix', 1), 'Finset.Icc': ('closed_interval', 2),
    'Finset.Ico': ('half_open_interval', 2),
    'FiniteQBenchmark.gaussian': ('gaussian_nat', 3),
    'FiniteQBenchmark.gaussianInt': ('gaussian_integer_support', 3),
    'FiniteQBenchmark.gaussianQuotient': ('gaussian_quotient', 3),
    'FiniteQBenchmark.poch': ('q_pochhammer_nat', 3),
    'FiniteQBenchmark.pochInt': ('q_pochhammer_integer', 3),
    'FiniteQBenchmark.pochList': ('q_pochhammer_list', 3),
    'FiniteQBenchmark.pochListInt': ('q_pochhammer_integer_list', 3),
}


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',', ':'))


def name_text(name):
    if name['tag'] == 'anonymous': return ''
    parent = name_text(name['prefix'])
    part = str(name['value'])
    return parent + '.' + part if parent else part


def application(tree):
    args = []
    while tree['tag'] == 'app':
        args.append(tree['arg']); tree = tree['fn']
    args.reverse()
    return tree, args


class DAG:
    def __init__(self, limit=200000):
        self.memo = {}; self.nodes = {}; self.limit = limit; self.unrecognized = set()

    def add(self, expr):
        if id(expr) in self.memo: return self.memo[id(expr)]
        tag = expr['tag']
        node = {'constructor': tag}
        if tag == 'app':
            node.update(fn=self.add(expr['fn']), arg=self.add(expr['arg']))
        elif tag in ('lam', 'forall'):
            # De Bruijn indices carry binding identity; display names are nonsemantic.
            node.update(type=self.add(expr['type']), body=self.add(expr['body']),
                        binder_info=expr['binder_info'])
        elif tag == 'let':
            node.update(type=self.add(expr['type']), value=self.add(expr['value']),
                        body=self.add(expr['body']), nondependent=expr['nondependent'])
        elif tag == 'proj':
            node.update(structure=expr['structure'], index=expr['index'], body=self.add(expr['body']))
        elif tag in ('const', 'sort', 'bvar', 'nat', 'string'):
            node.update({k: v for k, v in expr.items() if k != 'tag'})
        else:
            raise ValueError('unsupported_wire_constructor: ' + tag)
        key = 'e_' + hashlib.sha256(canonical(node).encode()).hexdigest()
        if key not in self.nodes:
            if len(self.nodes) >= self.limit: raise ValueError('representation_node_budget')
            self.nodes[key] = node
        self.memo[id(expr)] = key
        return key

    def annotate(self, signatures):
        """Annotations are views only. All application arguments remain in the DAG."""
        views = {}
        for key, node in self.nodes.items():
            args, head = [], node
            while head['constructor'] == 'app':
                args.append(head['arg']); head = self.nodes[head['fn']]
            args.reverse()
            if head['constructor'] != 'const': continue
            name = name_text(head['name'])
            if name in SYMBOLS:
                kind, _ = SYMBOLS[name]
                signature = signatures.get(name, {})
                binders = signature.get('binders', [])
                views[key] = dict(symbol_kind=kind, symbol=name, all_arguments=args,
                    signature=signature.get('type'),
                    operands=[dict(position=i, expression=arg, **binders[i])
                              for i, arg in enumerate(args) if i < len(binders)],
                    application_status=('fully_applied' if len(args) == len(binders) else
                                        'partially_applied' if len(args) < len(binders) else 'overapplied')
                                       if signature else 'signature_unavailable')
            elif name.startswith('FiniteQBenchmark.'):
                self.unrecognized.add(name)
                views[key] = dict(kind='defined_object', symbol=name, all_arguments=args,
                                  normalization='preserved_without_unfolding')
        return views


def standardize(bundle, source, verified=False):
    dag = DAG()
    original = dag.add(bundle['original_closed'])
    normalized = dag.add(bundle['normalized_closed'])
    bridge = dag.add(bundle['bridge_type'])
    declarations = []
    for declaration in bundle['declarations']:
        row = {k: v for k, v in declaration.items() if k not in ('type', 'body')}
        row['type'] = dag.add(declaration['type'])
        if 'body' in declaration:
            row['body'] = dag.add(declaration['body'])
        declarations.append(row)
    def references(value):
        if isinstance(value, dict):
            if value.get('tag') in ('app', 'lam', 'forall', 'let', 'proj', 'const', 'sort', 'bvar', 'nat', 'string'):
                return {'expression': dag.add(value)}
            return {k: references(v) for k, v in value.items()}
        if isinstance(value, list): return [references(v) for v in value]
        return value
    relations = references(bundle.get('relations', []))
    context = references(bundle['context'])
    transformations = references(bundle['transformations'])
    signatures = {row['symbol']: dict(type=dag.add(row['type']), binders=row['binders'])
                  for row in bundle.get('signatures', [])}
    views = dag.annotate(signatures)
    if verified:
        status = 'verified_unchanged' if original == normalized else 'verified_normalized'
    else:
        status = 'unverified_candidate'
    return dict(schema_version='finite-q-preprocess/2', status=status,
                source=source, normalization_view=bundle.get('normalization_view', 'expanded'), original=original, normalized=normalized,
                bridge_type=bridge, nodes=dag.nodes, objects=views,
                declarations=declarations, signatures=signatures, relations=relations,
                context=context, transformations=transformations,
                normalization=dict(allowed_rules=bundle['allowed_rules'],
                                   round_limit_reached=bundle['round_limit_reached'],
                                   missing_side_conditions='skip_rewrite_without_adding_assumptions',
                                   complete_canonical_form=False),
                unresolved=[dict(symbol=n, reason='preserved_defined_object') for n in sorted(dag.unrecognized)],
                semantics=dict(binding='de_bruijn', types='explicit_binder_types_and_full_arguments',
                               assumptions='unchanged_in_closed_forall_context',
                               equivalence='forall_original_context_original_eq_normalized',
                               identity='structural_hash_not_mathematical_equivalence'))
