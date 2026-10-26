"""Synthetic structural/control tests. Synthetic 'verified' tags are not proofs."""
import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from selection import select
from selection.capabilities import ROUTES
from selection.features import FeatureLimit, extract
from selection.policy import rank
from selection.scoring import CRITERIA, ahp, bounds, exact, interval, topsis
from workflow import engine
from workflow.contracts import BACKENDS, FAMILIES, sha


class Fixture:
    def __init__(self): self.nodes = {}; self.context = []
    def add(self, constructor, **kwargs):
        node = dict(constructor=constructor, **kwargs)
        key = 'e_'+hashlib.sha256(json.dumps(node, sort_keys=True).encode()).hexdigest()
        self.nodes[key] = node
        return key
    def const(self, symbol):
        n = dict(tag='anonymous')
        for part in symbol.split('.'): n = dict(tag='str', prefix=n, value=part)
        return self.add('const', name=n, levels=[])
    def nat(self, n): return self.add('nat', value=n)
    def var(self, n): return self.add('bvar', index=n)
    def app(self, symbol, *args):
        k = self.const(symbol)
        for arg in args: k = self.add('app', fn=k, arg=arg)
        return k
    def lam(self, body): return self.add('lam', type=self.const('Nat'), body=body, binder_info='explicit')
    def eq(self, left, right): return self.app('Eq', self.const('Complex'), left, right)
    def sum(self, body, domain=None, size=None):
        typ = self.app('Fin', self.nat(size)) if size is not None else self.const('Nat')
        return self.app('Finset.sum', typ, self.const('Complex'), self.const('testInstance'),
            domain or (self.app('Finset.univ') if size is not None else self.app('Finset.range', self.var(0))), self.lam(body))
    def hypothesis(self, expression):
        self.context.append(dict(role='assumption', original_name='h', type_in_full_context=dict(expression=expression)))
    def parameter(self, typ='Nat'):
        self.context.append(dict(role='parameter', original_name='n', type_in_full_context=dict(expression=self.const(typ))))
    def standard(self, target):
        return dict(schema_version='finite-q-preprocess/2', status='verified_unchanged',
                    normalized=target, original=target, nodes=self.nodes, context=self.context,
                    declarations=[], signatures={}, source={'identity':'not-a-real-benchmark-fixture'})


def root_fixture(*, primitive=True, positive=True, wrong_parameter=False):
    b = Fixture()
    # Outer context variables x=2, w=1, m=0; index j introduces one binder.
    order = b.var(0); root = b.var(1); x = b.var(2)
    factor = b.app('HSub.hSub', b.nat(1), b.app('HMul.hMul', b.var(3),
        b.app('HPow.hPow', b.var(2), b.var(0))))
    product = b.app('Finset.prod', b.const('Nat'), b.const('Complex'), b.const('testInstance'),
                    b.app('Finset.range', order), b.lam(factor))
    rhs = b.app('HSub.hSub', b.nat(1), b.app('HPow.hPow', x, order))
    if primitive: b.hypothesis(b.app('IsPrimitiveRoot', root if not wrong_parameter else x, order))
    if positive: b.hypothesis(b.app('LT.lt', b.nat(0), order))
    return b.standard(b.eq(product, rhs))


class ScoreTests(unittest.TestCase):
    def test_ahp_weights_and_consistency(self):
        a = ahp(); self.assertAlmostEqual(a['consistency_ratio'], 0)
        self.assertEqual([round(a['weights'][k]*11) for k in CRITERIA], [4,2,4,1])
    def test_invalid_and_inconsistent_judgements(self):
        for matrix in ([[1]*4]*3, [[0]*4]*4,
                       [[1,9,1,1],[1/9,1,9,1],[1,1/9,1,9],[1,1,1/9,1]]):
            with self.subTest(matrix=matrix), self.assertRaises(ValueError): ahp(matrix)
    def test_ideal_endpoints_and_monotonicity(self):
        w = ahp()['weights']; zero = dict.fromkeys(CRITERIA,0.); one = dict.fromkeys(CRITERIA,1.)
        self.assertEqual(topsis(zero,w),0); self.assertEqual(topsis(one,w),1)
        for k in CRITERIA:
            lo = dict.fromkeys(CRITERIA,.4); hi = dict(lo); hi[k]=.7
            self.assertLess(topsis(lo,w),topsis(hi,w))
    def test_unknown_is_an_interval_not_a_success_probability(self):
        c = {k: interval(reason='unknown') for k in CRITERIA}
        self.assertEqual(bounds(c,ahp()['weights']),dict(lower=0.,upper=1.))
        with self.assertRaises(ValueError): interval(.8,.2,reason='bad')
    def test_candidate_changes_do_not_rescale_scores(self):
        w=ahp()['weights']; c={k:exact(.6,'test') for k in CRITERIA}
        row=dict(route='a',method='product',status='structural_match',criteria=c)
        rank([row],w,FAMILIES); before=dict(row['score'])
        other=dict(route='b',method='recurrence',status='structural_match',criteria={k:exact(.9,'test') for k in CRITERIA})
        rank([other,row],w,FAMILIES); self.assertEqual(before,row['score'])
    def test_branch_scores_are_never_spliced(self):
        rows=[]
        for name, values in [('a',[1,0,0,0]),('b',[0,1,1,1])]:
            rows.append(dict(route=name,method='product',status='structural_match',
                             criteria={k:exact(v,'test') for k,v in zip(CRITERIA,values)}))
        methods=rank(rows,ahp()['weights'],FAMILIES)
        best=methods[0]; self.assertLess(best['score']['lower'],1)
        self.assertIn(best['score'],[r['score'] for r in rows])


class FeatureTests(unittest.TestCase):
    def test_exact_root_product_and_bound_variables(self):
        r=select(root_fixture()); self.assertEqual(r['selected_method'],'product')
        self.assertEqual(r['selected_route'],'primitive_root_product')
        root=next(x for x in r['routes'] if x['route']=='primitive_root_product')
        self.assertEqual(root['criteria']['conditions']['lower'],1.)
        self.assertEqual(root['score']['lower'],1.)
    def test_missing_and_wrong_parameter_conditions_remain_unknown(self):
        for data in [root_fixture(primitive=False),root_fixture(wrong_parameter=True)]:
            r=select(data); row=next(x for x in r['routes'] if x['route']=='primitive_root_product')
            self.assertEqual(row['criteria']['conditions']['lower'],.5)
            self.assertFalse(row['criteria']['conditions']['known'])
    def test_weak_root_condition_does_not_count_as_primitive(self):
        data=root_fixture(primitive=False); b=Fixture(); b.nodes=data['nodes']; b.context=data['context']
        b.hypothesis(b.eq(b.app('HPow.hPow',b.var(1),b.var(0)),b.nat(1)))
        r=select(data)
        self.assertFalse(r['features']['root_product']['primitive'])
    def test_conjunction_is_decomposed_for_side_conditions(self):
        data=root_fixture(); b=Fixture(); b.nodes=data['nodes']
        facts=[x['type_in_full_context']['expression'] for x in data['context']]
        b.hypothesis(b.app('And',*facts));data['context']=b.context
        self.assertEqual(select(data)['selected_route'],'primitive_root_product')
        self.assertEqual(select(data)['ranking'][0]['score']['lower'],1.)
    def test_metadata_names_and_proof_terms_do_not_affect_selection(self):
        data=root_fixture(); first=select(data); mutated=copy.deepcopy(data)
        mutated['source']={'identity':'OTHER-THEOREM','family_id':'Z','proved':True}
        for c in mutated['context']:c['original_name']='renamed'
        b=Fixture(); b.nodes=mutated['nodes']
        decoy=b.app('Matrix.det',b.var(0));mutated['bridge_type']=decoy
        mutated['transformations']=[{'term':decoy}]
        mutated['declarations']=[dict(kind='definition',name=b.nodes[b.const('unrelated')]['name'],body=decoy)]
        second=select(mutated)
        self.assertEqual(first['ranking'],second['ranking'])
        self.assertNotIn('Matrix.det',second['features']['symbols'])
    def test_hypothesis_objects_do_not_contaminate_goal_features(self):
        data=root_fixture(); b=Fixture(); b.nodes=data['nodes'];b.context=data['context']
        b.hypothesis(b.eq(b.app('Matrix.det',b.var(0)),b.nat(0)))
        self.assertNotIn('Matrix.det',select(data)['features']['symbols'])
    def test_unknown_definition_preserves_candidates(self):
        b=Fixture();d=b.standard(b.eq(b.app('unrecognizedFunction',b.var(0)),b.nat(0)))
        r=select(d)
        self.assertEqual(r['status'],'unclassified')
        self.assertIsNone(r['selected_method'])
        self.assertIsNone(r['selected_route'])
        self.assertEqual(r['unclassified_reason'],'all_methods_unknown_tied')
        self.assertEqual(set(r['suggested_methods']),set(FAMILIES))
        self.assertFalse(r['stable_under_weight_perturbation'])
        self.assertTrue(all(x['status']=='unknown' for x in r['ranking']))
        self.assertEqual(r['ranking'][0]['score'],dict(lower=0.,upper=1.))
    def test_reachable_definition_is_inspected_but_keeps_uncertainty(self):
        b=Fixture(); target=b.eq(b.app('customProduct',b.var(0)),b.nat(0))
        body=b.app('Finset.prod',b.app('Finset.range',b.var(0)),b.lam(b.var(0)))
        d=b.standard(target);d['declarations']=[dict(kind='definition',name=b.nodes[b.const('customProduct')]['name'],body=body)]
        f=extract(d);self.assertIn('Finset.prod',f['symbols']);self.assertNotIn('Finset.prod',f['direct_symbols'])
        self.assertIn('customProduct',f['unknown_symbols'])
    def test_unverified_and_cyclic_inputs_rejected(self):
        d=root_fixture();d['status']='unverified_candidate'
        with self.assertRaisesRegex(ValueError,'unverified'):select(d)
        d=root_fixture();d['nodes'][d['normalized']]={'constructor':'app','fn':d['normalized'],'arg':d['normalized']}
        with self.assertRaisesRegex(ValueError,'cyclic'):select(d)
    def test_input_budgets(self):
        with self.assertRaises(FeatureLimit):select(root_fixture(),max_nodes=1)
        with self.assertRaises(FeatureLimit):select(root_fixture(),seconds=1e-10)
    def test_partial_application_is_not_a_complete_sum(self):
        b=Fixture(); half=b.app('Finset.sum',b.var(0));d=b.standard(b.eq(half,b.nat(0)))
        d['signatures']['Finset.sum']={'binders':[{'binder_info':'explicit'}]*5}
        f=extract(d);self.assertEqual(f['counts'].get('Finset.sum',0),0)
        self.assertIn('Finset.sum',f['unknown_symbols'])
    def test_domain_instances_must_match_target_carrier(self):
        b=Fixture(); k=b.var(1); other=b.var(0)
        for typ in (b.app('Field',k),b.app('CharZero',other)):
            b.context.append(dict(role='parameter',type_in_full_context=dict(expression=typ)))
        data=b.standard(b.app('Eq',k,b.var(2),b.var(3)))
        f=extract(data);self.assertTrue(f['scalar_domain']['field']);self.assertFalse(f['scalar_domain']['char_zero'])


class RoutingTests(unittest.TestCase):
    def test_product_on_one_side_does_not_hide_defined_sequence_on_other(self):
        b=Fixture();b.parameter()
        seq=b.app('FiniteQBenchmark.rogersSzego',b.var(0),b.var(1),b.var(2))
        product=b.app('FiniteQBenchmark.poch',b.var(0),b.var(1),b.var(2))
        self.assertEqual(select(b.standard(b.eq(seq,product)))['selected_method'],'recurrence')
    def test_registry_covers_every_method_and_backend(self):
        self.assertEqual({m for _,_,m,_ in ROUTES},set(FAMILIES))
        self.assertEqual({b for _,b,_,_ in ROUTES},set(BACKENDS))
    def test_distinct_structural_families(self):
        cases=[]
        b=Fixture();cases.append(('interpolation',b.standard(b.eq(b.app('HAdd.hAdd',b.var(0),b.var(0)),b.nat(0)))))
        b=Fixture();cases.append(('coefficient',b.standard(b.eq(b.app('Polynomial.coeff',b.var(0),b.nat(2)),b.nat(0)))))
        b=Fixture();cases.append(('noncommutative',b.standard(b.eq(b.app('FiniteQBenchmark.kacX',b.var(0)),b.var(0)))))
        b=Fixture();cases.append(('macmahon',b.standard(b.eq(b.app('FiniteQMacMahon.omegaGE',b.var(0)),b.nat(0)))))
        for natural,expected in [(False,'telescoping'),(True,'recurrence')]:
            b=Fixture()
            if natural:b.parameter()
            term=b.app('FiniteQBenchmark.poch',b.var(0),b.var(1),b.var(2))
            cases.append((expected,b.standard(b.eq(b.sum(term),b.nat(0)))))
        b=Fixture();cases.append(('difference_ring',b.standard(b.eq(b.sum(b.sum(b.var(0))),b.nat(0)))))
        b=Fixture();cases.append(('kernel_transform',b.standard(b.eq(b.sum(b.sum(b.var(0),size=2),size=2),b.nat(0)))))
        b=Fixture();cases.append(('spectral',b.standard(b.eq(b.sum(b.var(0),size=2),b.nat(0)))))
        b=Fixture();det=b.app('Matrix.det',b.app('Fin',b.nat(2)),b.const('Complex'),b.var(0))
        cases.append(('determinant',b.standard(b.eq(det,b.nat(0)))))
        b=Fixture();domain=b.app('Finset.powersetCard',b.var(0),b.var(1));g=b.app('FiniteQBenchmark.gaussian',b.var(0),b.var(1),b.var(2))
        cases.append(('combinatorial',b.standard(b.eq(b.sum(b.var(0),domain),g))))
        cases.append(('product',root_fixture()))
        for expected,data in cases:
            with self.subTest(expected=expected):self.assertEqual(select(data)['selected_method'],expected)
    def test_dimension_limit_rejects_route_not_whole_determinant_method(self):
        b=Fixture();det=b.app('Matrix.det',b.app('Fin',b.nat(7)),b.const('Complex'),b.var(0))
        r=select(b.standard(b.eq(det,b.nat(0))))
        computed=next(x for x in r['routes'] if x['route']=='determinant_matrix')
        fallback=next(x for x in r['routes'] if x['route']=='determinant_structure')
        self.assertEqual(computed['status'],'unsupported');self.assertNotEqual(fallback['status'],'unsupported')
        self.assertEqual(r['selected_method'],'determinant')
    def test_entry_sum_dimension_is_not_determinant_dimension(self):
        b=Fixture();entry=b.sum(b.var(0),size=7)
        det=b.app('Matrix.det',b.app('Fin',b.nat(2)),b.const('Complex'),entry)
        r=select(b.standard(b.eq(det,b.nat(0))))
        computed=next(x for x in r['routes'] if x['route']=='determinant_matrix')
        self.assertNotEqual(computed['status'],'unsupported')
    def test_selection_does_not_import_solvers(self):
        import builtins
        original=builtins.__import__
        def checked(name,*args,**kwargs):
            if name.split('.')[0] in ('sympy','p1','p2','product','subprocess'):
                raise AssertionError('selector imported a solver/process library: '+name)
            return original(name,*args,**kwargs)
        with patch('builtins.__import__',side_effect=checked):select(root_fixture())


class IntegrationTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name)
        self.standard=self.root/'standard.json';self.standard.write_text(json.dumps(root_fixture()))
        self.source={'identity':'synthetic-control-test','sha256':'synthetic-source','snapshot':'unused'}
        self.calls=[]
    def tearDown(self):self.temp.cleanup()
    def runner(self,req,directory,timeout):
        self.calls.append((req['action'],req['method'],timeout))
        if req['action']=='preprocess':return dict(status='verified_unchanged',descriptor=dict(directory=str(self.root)))
        if req['action']=='select':return dict(select(root_fixture()),source_sha256=self.source['sha256'],standard_sha256=sha(self.standard))
        if req['action']=='analyze':return dict(status='analyzed',candidates=[dict(backend='finite_product_indices',applicable=True,reason='synthetic control test')])
        return dict(status='search_exhausted')
    def run_auto(self,**kwargs):
        with patch.object(engine,'snapshot',return_value=dict(self.source)),patch.object(engine,'check_source'):
            return engine.prove('synthetic-control-test',self.root/'run',method='auto',runner=kwargs.pop('runner',self.runner),**kwargs)
    def test_select_only_preprocesses_once_and_never_runs_solver(self):
        r=self.run_auto(select_only=True)
        self.assertEqual(r['status'],'selected');self.assertEqual(r['automatic_train_proofs'],0)
        self.assertEqual([x[0] for x in self.calls],['preprocess','select'])
    def test_auto_dispatches_only_one_method_with_same_preprocessing(self):
        r=self.run_auto()
        self.assertEqual(r['status'],'unproved')
        self.assertEqual([(a,m) for a,m,_ in self.calls],[('preprocess','auto'),('select','auto'),('analyze','product'),('prove','product')])
        self.assertEqual(r['source']['preprocessing']['directory'],str(self.root))
    def test_selection_failure_never_dispatches(self):
        def fail(req,d,t):
            if req['action']=='select':return dict(status='selection_failed',error='inspection budget')
            return self.runner(req,d,t)
        r=self.run_auto(runner=fail);self.assertEqual(r['status'],'selection_failed');self.assertEqual(r['attempts'],[])
    def test_mismatched_selection_binding_rejected(self):
        def wrong(req,d,t):
            out=self.runner(req,d,t)
            if req['action']=='select':out['standard_sha256']='wrong'
            return out
        r=self.run_auto(runner=wrong);self.assertEqual(r['status'],'selection_failed');self.assertEqual(r['attempts'],[])
    def test_no_budget_reset_after_preprocessing(self):
        clock=[100.]
        def timed(req,d,t):
            out=self.runner(req,d,t)
            if req['action']=='preprocess':clock[0]+=8
            return out
        with patch.object(engine.time,'monotonic',side_effect=lambda:clock[0]):
            r=self.run_auto(runner=timed,budget=engine.Budget(seconds=10))
        self.assertTrue(all(t<=2 for a,_,t in self.calls if a!='preprocess'))
        self.assertEqual(r['status'],'unproved')
    def test_no_dispatch_when_selection_uses_remaining_budget(self):
        clock=[100.]
        def timed(req,d,t):
            out=self.runner(req,d,t)
            if req['action']=='select':clock[0]+=11
            return out
        with patch.object(engine.time,'monotonic',side_effect=lambda:clock[0]):
            r=self.run_auto(runner=timed,budget=engine.Budget(seconds=10))
        self.assertEqual(r['status'],'resource_exhausted');self.assertEqual(r['attempts'],[])
    def test_auto_cannot_bypass_method_local_worker_validation(self):
        from workflow.worker import validate_request
        for req in [dict(action='prove',method='auto',backend='direct_q_gosper'),dict(action='select',method='product')]:
            with self.assertRaises(ValueError):validate_request(req)
    def test_untrusted_preprocessing_descriptor_rejected_by_real_worker(self):
        from workflow.worker import execute
        source=dict(self.source,path='nonexistent')
        with self.assertRaises((ValueError,OSError)):
            execute(dict(action='select',method='auto',source=source,timeout=5))


class UnknownExplorationTests(unittest.TestCase):
    """Control-flow fixtures only; fake successes are not proof evidence."""
    tearDown=IntegrationTests.tearDown
    runner=IntegrationTests.runner
    def run_auto(self,**kwargs):
        with patch('workflow.unknown.check_source'):
            return IntegrationTests.run_auto(self,**kwargs)
    def setUp(self):
        IntegrationTests.setUp(self)
        b=Fixture();self.unknown=b.standard(b.eq(b.app('unknownFunction',b.var(0)),b.nat(0)))
        self.standard.write_text(json.dumps(self.unknown))

    def unknown_runner(self,req,directory,timeout):
        self.calls.append((req['action'],req['method'],timeout))
        if req['action']=='preprocess':
            return dict(status='verified_unchanged',descriptor=dict(directory=str(self.root),status='verified_unchanged'))
        if req['action']=='select':
            return dict(select(self.unknown),source_sha256=self.source['sha256'],standard_sha256=sha(self.standard))
        if req['action']=='analyze':
            backend=next(b for b,m in BACKENDS.items() if m==req['method'])
            return dict(status='analyzed',candidates=[dict(backend=backend,applicable=True,reason='synthetic')])
        return dict(status='search_exhausted')

    def test_unknown_default_only_marks(self):
        r=self.run_auto(runner=self.unknown_runner)
        self.assertEqual(r['status'],'unclassified');self.assertIsNone(r['selected_method'])
        self.assertEqual([a for a,_,_ in self.calls],['preprocess','select'])

    def test_select_only_never_explores_even_with_all_option(self):
        r=self.run_auto(runner=self.unknown_runner,select_only=True,unknown_policy='all')
        self.assertEqual(r['status'],'unclassified')
        self.assertEqual([a for a,_,_ in self.calls],['preprocess','select'])

    def test_all_methods_share_one_preprocessing_and_keep_own_reports(self):
        r=self.run_auto(runner=self.unknown_runner,unknown_policy='all',preprocessing_view='expanded')
        self.assertEqual(r['status'],'unproved');self.assertEqual(r['classification_status'],'unclassified')
        self.assertEqual([m for a,m,_ in self.calls if a=='preprocess'],['auto'])
        self.assertEqual(sorted(m for a,m,_ in self.calls if a=='analyze'),sorted(FAMILIES))
        self.assertEqual(sorted(m for a,m,_ in self.calls if a=='prove'),sorted(FAMILIES))
        self.assertEqual(len(r['exploration']['results']),12)
        for row in r['exploration']['results']:
            child=json.loads(Path(row['report']).read_text())
            self.assertEqual(child['method_request'],row['method'])
            self.assertTrue(child['preprocessing']['reused_from_parent'])
            self.assertEqual(child['preprocessing']['normalization_view'],'expanded')
            self.assertEqual(child['source']['preprocessing']['directory'],str(self.root))
            self.assertEqual(child['budget']['seconds'],900)

    def test_success_does_not_stop_exploration_or_relabel_classification(self):
        def succeeds(req,d,t):
            result=self.unknown_runner(req,d,t)
            if req['action']=='prove' and req['method'] in ('product','interpolation'):
                return dict(status='proved')
            return result
        with patch.object(engine,'accept_proof',return_value={'synthetic_control_test':True}) as accept:
            r=self.run_auto(runner=succeeds,unknown_policy='all')
        self.assertEqual(r['status'],'proved');self.assertEqual(r['classification_status'],'unclassified')
        self.assertIsNone(r['selected_method']);self.assertEqual(r['automatic_train_proofs'],1)
        self.assertEqual(r['successful_methods'],['product','interpolation'])
        self.assertEqual(len(r['exploration']['results']),12);self.assertEqual(accept.call_count,2)

    def test_forged_success_rejected_and_other_methods_still_run(self):
        def forges(req,d,t):
            result=self.unknown_runner(req,d,t)
            return dict(status='proved') if req['action']=='prove' else result
        with patch.object(engine,'accept_proof',side_effect=ValueError('forged certificate')):
            r=self.run_auto(runner=forges,unknown_policy='all')
        self.assertEqual(r['status'],'unproved');self.assertEqual(r['automatic_train_proofs'],0)
        self.assertEqual(len(r['exploration']['results']),12)
        self.assertTrue(all(x['status']=='integrity_error' for x in r['exploration']['results']))

    def test_structural_selection_still_runs_only_one_method(self):
        r=self.run_auto(unknown_policy='all')
        self.assertEqual(r['selected_method'],'product');self.assertNotIn('exploration',r)
        self.assertEqual([m for a,m,_ in self.calls if a=='analyze'],['product'])

    def test_forged_unknown_label_does_not_start_sweep(self):
        def forges(req,d,t):
            result=self.unknown_runner(req,d,t)
            if req['action']=='select':result['ranking'][0]['status']='structural_match'
            return result
        r=self.run_auto(runner=forges,unknown_policy='all')
        self.assertEqual(r['status'],'selection_failed')
        self.assertFalse(any(a=='analyze' for a,_,_ in self.calls))

    def test_invalid_policy_and_workers_rejected_before_dispatch(self):
        for kwargs in (dict(unknown_policy='fallback'),dict(unknown_workers=0),dict(unknown_workers=5)):
            with self.subTest(kwargs=kwargs),self.assertRaises(ValueError):self.run_auto(**kwargs)
        self.assertEqual(self.calls,[])


if __name__=='__main__':unittest.main(verbosity=2)
