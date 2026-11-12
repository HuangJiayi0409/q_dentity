"""CLI orchestration tests use offline clients and isolated source fixtures."""
from argparse import Namespace
from dataclasses import replace
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from agent_v2.models import Artifact, Budget, initial_state
from agent_v2.storage import RunStore, freeze_source, sha256_file, IntegrityError
from agent_v2.autonomous_cli import train_run, resume_run


class AutonomousCLITests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.root = Path(self.tmp.name)
        self.store = RunStore.create(self.root/'runs', 'run')
        self.path = self.root/'source.lean'; self.path.write_text('import Init\ntheorem demo : True := by\n  sorry\n')
        self.source = freeze_source(self.path, 'synthetic', 'demo', self.store)
        self.dependency = self.root/'dependency.py'; self.dependency.write_text('pure = True\n')
        self.args = Namespace(identity='synthetic', methods='a,b', seconds=100., max_steps=5,
            action_seconds=10., max_model_calls=3, max_expansions=2, max_repairs=1,
            selector='rule', model='configured-model', model_credential=str(self.root/'credential'),
            model_endpoint='https://unused.invalid/v1/responses', jev_credential=None, pause_after=1)
        self.specs = {name: SimpleNamespace(id=name, version='1', family='method '+name,
            supported_structures=('pure fixture',), limitations=('fixture only',), local_lean=True,
            estimated_seconds=0.1, frontend='frontend_'+name, dependency_provider='deps_'+name,
            capability_level='L3') for name in ('a','b')}
        self.frontends = {name: {'status':'applicable', 'original_proposition':'True',
            'local_proposition':'True', 'closure_proof':'must not enter capability'} for name in self.specs}
        self.registry = SimpleNamespace(ids=lambda:tuple(self.specs), get=lambda name:self.specs[name])
        self.dep = Artifact(str(self.dependency), sha256_file(self.dependency))
        self.observed=[]

    def tearDown(self): self.tmp.cleanup()

    def resolve(self, name):
        if name.startswith('frontend_'):
            method=name[len('frontend_'):]
            return lambda *args, **kwargs: dict(self.frontends[method])
        return lambda: (self.dep,)

    def execute(self, *, library_effect=None, library_records=None, formal_error=None):
        from agent_v2.autonomous import AutonomousStore
        def stop(state, graph, store, **kwargs):
            from agent_v2.loop import finish
            self.observed.append((state,graph,store.runtime,kwargs))
            return finish(store,replace(state,status='incomplete'),graph,'checkpoint_paused')
        with patch('agent_v2.autonomous_cli.load_train',return_value=self.source), \
             patch('agent_v2.method_registry.builtin_registry',return_value=self.registry), \
             patch('agent_v2.method_registry.resolve',side_effect=self.resolve), \
             patch('agent_v2.cli.runtime_dependencies',return_value=(self.dep,)), \
             patch('agent_v2.library.LocalLibrary.query',return_value=library_records or [],side_effect=library_effect), \
             patch('agent_v2.local_proof_checker.LocalLeanChecker._bound',return_value=object(),side_effect=formal_error), \
             patch('agent_v2.autonomous.run',side_effect=stop):
            return train_run(self.args,self.store)

    def test_all_applicable_frontends_get_capabilities_without_closure_proofs(self):
        self.assertEqual(self.execute(),'incomplete')
        state,graph,runtime,kwargs=self.observed[0]
        self.assertEqual(set(runtime.capabilities), {'a','b'})
        self.assertTrue(all('closure_proof' not in c for c in runtime.capabilities.values()))
        self.assertEqual(sum(a.path==self.dep.path for a in state.G.dependencies),1)
        self.assertEqual(state.G.proposition,'True')
        self.assertEqual(kwargs, {'pause_after':1})
        self.assertTrue(any(o.M=='LLM' for o in graph.outlets.values()))
        self.assertEqual(json.loads(self.store.path('frontend_inventory.json').read_text())['methods']['a']['status'],'applicable')
        self.assertLess(state.b.seconds,100)

    def test_semantic_disagreement_never_selects_a_convenient_frontend(self):
        self.frontends['b']['original_proposition']='False'
        self.assertEqual(self.execute(),'incomplete')
        self.assertFalse(self.observed)
        self.assertEqual(json.loads(self.store.path('run.json').read_text())['stop_reason'],'unsupported_original_proposition')

    def test_nonapplicable_frontend_cannot_supply_an_executable_capability(self):
        self.frontends['b']={'status':'not_applicable','reason':'fixture boundary'}
        self.execute()
        self.assertEqual(set(self.observed[0][2].capabilities), {'a'})

    def test_resume_restores_call_counts_without_loading_library_or_new_network(self):
        self.execute()
        from agent_v2.autonomous import AutonomousStore
        state,graph,runtime,_=self.observed[0]
        runtime.model.calls_used=2
        auto=AutonomousStore(self.store.root,runtime)
        auto.save_checkpoint({'schema_version':1,'state':state.to_dict(),'graph':graph.to_dict(),'inflight':False})
        with patch('agent_v2.autonomous.run',side_effect=lambda state,graph,store,**kw: self.capture_resume(state,store)), \
             patch('agent_v2.library.LocalLibrary.query',side_effect=AssertionError('no repeat library build')):
            self.assertEqual(resume_run(Namespace(pause_after=1),self.store),'incomplete')
        self.assertEqual(self.resumed.model.calls_used,2)

    def capture_resume(self,state,store):
        self.resumed=store.runtime
        return replace(state,status='incomplete')

    def test_resume_refuses_config_file_mutation_and_excess_call_counter(self):
        self.execute()
        metadata=self.store.read_json('autonomous_config.json')
        metadata['config']['model']['model']='foreign-model'
        self.store.write_json('autonomous_config.json',metadata)
        with self.assertRaises(IntegrityError): resume_run(Namespace(pause_after=1),self.store)

    def test_invalid_or_duplicate_method_selection_is_rejected(self):
        self.args.methods='a,a'
        with self.assertRaises(ValueError): self.execute()

    def test_resume_rejects_excess_model_calls_before_building_clients(self):
        self.execute()
        saved=self.store.load_checkpoint(); saved['autonomous']['model_calls']=4
        self.store.save_checkpoint(saved)
        with self.assertRaises(ValueError): resume_run(Namespace(pause_after=1),self.store)

    def test_resume_rejects_completed_method_without_checked_certificate(self):
        self.execute()
        saved=self.store.load_checkpoint(); saved['autonomous']['completed_methods']={'a':['missing']}
        self.store.save_checkpoint(saved)
        with self.assertRaises(IntegrityError): resume_run(Namespace(pause_after=1),self.store)

    def test_effective_provider_endpoint_is_frozen_from_credential_config(self):
        credential=Path(self.args.model_credential)
        credential.write_text(json.dumps({'key':'offline-unit-key','url':'https://initial.invalid'}))
        self.args.model_endpoint=None
        self.execute()
        configured=self.observed[0][2].config['model']['endpoint']
        self.assertEqual(configured,'https://initial.invalid/v1/responses')
        credential.write_text(json.dumps({'key':'rotated-offline-key','url':'https://changed.invalid'}))
        with patch('agent_v2.autonomous.run',side_effect=lambda state,graph,store,**kw:self.capture_resume(state,store)):
            resume_run(Namespace(pause_after=1),self.store)
        self.assertEqual(self.resumed.model.config.endpoint,'https://initial.invalid/v1/responses')

    def test_setup_budget_exhaustion_is_reported_as_budget_exhausted(self):
        import time
        from agent_v2.autonomous_cli import _unsupported
        status=_unsupported(self.store,self.source,self.args,time.monotonic()-101.,'setup_budget_exhausted')
        self.assertEqual(status,'budget_exhausted')
        self.assertEqual(self.store.read_json('run.json')['stop_reason'],'setup_budget_exhausted')

    def test_library_timeout_after_shared_budget_is_budget_exhausted(self):
        import time
        from agent_v2.library import LibraryUnavailable
        self.args.seconds=.1
        def timeout(*args,**kwargs):
            time.sleep(.12)
            raise LibraryUnavailable('library_timeout')
        self.assertEqual(self.execute(library_effect=timeout),'budget_exhausted')
        self.assertFalse(self.observed)
        self.assertEqual(self.store.read_json('run.json')['remaining_budget']['seconds'],0.)

    def test_missing_library_environment_is_environment_blocked(self):
        from agent_v2.library import LibraryUnavailable
        def unavailable(*args,**kwargs): raise LibraryUnavailable('package_unavailable')
        self.assertEqual(self.execute(library_effect=unavailable),'environment_blocked')
        self.assertFalse(self.observed)

    def test_actual_library_provenance_and_common_foundations_are_source_dependencies(self):
        origin=self.root/'foundation.lean'; origin.write_text('pure mathematical declaration\n')
        records=[{'name':'demo','type':'True','provenance':{'path':str(origin),'sha256':sha256_file(origin)}}]
        self.execute(library_records=records)
        state=self.observed[0][0]
        frozen={artifact.path:artifact.sha256 for artifact in state.G.dependencies}
        self.assertEqual(frozen[str(origin)],sha256_file(origin))
        project=Path(__file__).resolve().parents[2]
        for relative in ('benchmark/lean/Benchmark/Definitions.lean','benchmark/lean/Benchmark/Auxiliary.lean',
                         'benchmark/lean/Benchmark/Gaussian.lean','finite_product_framework/p1/lean/GaussianRules.lean',
                         'project/lake-manifest.json','project/lean-toolchain','project/lakefile.toml'):
            self.assertIn(str(project/relative),frozen)
        origin.write_text('changed declaration\n')
        with self.assertRaises(IntegrityError): resume_run(Namespace(pause_after=1),self.store)

    def test_library_provenance_drift_during_setup_is_rejected(self):
        origin=self.root/'foundation.lean'; origin.write_text('changed declaration\n')
        records=[{'name':'demo','type':'True','provenance':{'path':str(origin),'sha256':'0'*64}}]
        with self.assertRaises(IntegrityError): self.execute(library_records=records)
        self.assertFalse(self.observed)

    def test_formal_source_unsupported_stops_before_library_and_model(self):
        touched=[]
        self.assertEqual(self.execute(formal_error=IntegrityError('Source has no implemented formal original translation'),
            library_effect=lambda *a,**k:touched.append(True) or []),'incomplete')
        self.assertFalse(touched);self.assertFalse(self.observed)
        self.assertEqual(self.store.read_json('run.json')['stop_reason'],'formal_source_translation_unavailable')
