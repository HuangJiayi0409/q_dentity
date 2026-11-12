"""The difference_ring candidate enters only the common source/profile checker."""
from dataclasses import replace
from pathlib import Path
import tempfile
import unittest

from agent_v2.difference_ring_frontend import analyze_source,PROFILE
from agent_v2.difference_ring_translation import make_candidate
from agent_v2.executor import _candidate_request
from agent_v2.lean_checker import LeanChecker
from agent_v2.storage import RunStore,load_train


class DifferenceRingProfileTests(unittest.TestCase):
    def setUp(self):
        temp=tempfile.TemporaryDirectory();self.addCleanup(temp.cleanup)
        self.store=RunStore.create(Path(temp.name)/'runs')
        source=load_train('FQI-SRC-FINE-2.1',self.store)
        front=analyze_source(source.to_dict(),self.store.root)
        self.source=replace(source,proposition=front['original_proposition'])
        self.front=analyze_source(self.source.to_dict(),self.store.root)
        self.candidate=make_candidate(self.front)
        self.context={'source':self.source.to_dict(),'source_sha256':self.source.sha256,
            'run_dir':str(self.store.root),'attempt_dir':str(self.store.path('check')),'seconds':0}

    def test_unique_source_profile_and_fixed_rule_configuration(self):
        from agent_v2.proof_profiles import resolve_source_profile
        bound=resolve_source_profile(self.source,self.store.root)
        self.assertIsNotNone(bound)
        self.assertEqual(bound.profile.id,PROFILE)
        self.assertEqual(bound.profile.method,'difference_ring')
        self.assertEqual(bound.profile.rules,('agent_v2/lean/DifferenceRingRules.lean',))
        self.assertEqual(bound.profile.foundations,('Definitions','Auxiliary','Gaussian'))
        self.assertEqual(bound.frontend,self.front)

    def test_canonical_candidate_reaches_budget_boundary_without_compilation(self):
        checked=LeanChecker().check_partial(_candidate_request(self.candidate),self.context)
        self.assertEqual(checked['status'],'budget_exhausted',checked)
        self.assertFalse(self.store.path('check').exists())

    def test_source_proposition_identity_and_dependencies_are_exact(self):
        request=_candidate_request(self.candidate)
        for changed in (dict(request,id='renamed'),dict(request,proposition='True'),
                        dict(request,source_sha256='0'*64),dict(request,dependencies=['foreign'])):
            with self.subTest(request=changed['id']):
                checked=LeanChecker().check_partial(changed,self.context)
                self.assertEqual(checked['status'],'integrity_error',checked)
                self.assertFalse(checked['accepted'])

    def test_coefficient_candidate_cannot_be_reused_as_an_difference_ring_certificate(self):
        from agent_v2.coefficient_frontend import analyze_source as coefficient_source
        from agent_v2.coefficient_translation import make_candidate as coefficient_candidate
        foreign=RunStore.create(self.store.root.parent/'foreign')
        other=load_train('FQI-FINITE-Q-BINOMIAL',foreign)
        candidate=coefficient_candidate(coefficient_source(other.to_dict(),foreign.root))
        request=dict(_candidate_request(candidate),source_sha256=self.source.sha256)
        checked=LeanChecker().check_partial(request,self.context)
        self.assertFalse(checked['accepted'])
        self.assertEqual(checked['status'],'integrity_error')
        self.assertFalse(self.store.path('check').exists())

    def test_bounded_wrong_term_is_not_silently_replaced_by_good_template(self):
        from agent_v2.proof_profiles import resolve_source_profile,reconstruct_bound_candidate
        bound=resolve_source_profile(self.source,self.store.root)
        request=dict(_candidate_request(self.candidate),proof_term='by exact True.intro')
        rebuilt=reconstruct_bound_candidate(bound,request,{},allow_negative=True)
        self.assertNotEqual(request['proof_term'],rebuilt.proof_term)
        for term in ('by sorry','by admit','by aesop'):
            with self.assertRaises(ValueError):
                reconstruct_bound_candidate(bound,dict(request,proof_term=term),{},allow_negative=True)


if __name__=='__main__':unittest.main()
