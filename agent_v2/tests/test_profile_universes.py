"""Fixed source profiles preserve polymorphism or explicitly require none."""
from dataclasses import replace
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

from agent_v2.lean_checker import LeanChecker,_lean_environment
from agent_v2.proof_profiles import registered_profiles

ROOT=Path(__file__).resolve().parents[2]


class ProfileUniverseTests(unittest.TestCase):
    def test_existing_source_profiles_keep_their_polymorphic_requirement(self):
        for profile in registered_profiles():
            if profile.method=='macmahon':continue
            with self.subTest(method=profile.method):
                self.assertEqual(profile.universe_parameters,('u',))
                self.assertTrue(profile.matches_universes({'universe_parameters':['u']}))
                for universes in ([],['v'],['u','v'],None):
                    self.assertFalse(profile.matches_universes({'universe_parameters':universes}))

    def test_monomorphic_policy_does_not_accept_polymorphic_or_missing_audits(self):
        profile=replace(registered_profiles()[0],universe_parameters=())
        self.assertTrue(profile.matches_universes({'universe_parameters':[]}))
        for audit in ({},{'universe_parameters':['u']},{'universe_parameters':None},None):
            self.assertFalse(profile.matches_universes(audit))

    def test_original_audit_allows_only_same_arity_and_rejects_boolean_counts(self):
        for parameters in (('u',),()):
            profile=replace(registered_profiles()[0],universe_parameters=parameters)
            names=['source_chosen_name'] if parameters else []
            good={'universe_parameters':names,'universe_parameter_count':len(parameters)}
            self.assertTrue(profile.matches_universes(good,original=True))
            for bad in (dict(good,universe_parameter_count=True),dict(good,universe_parameters=['u','v']),
                        dict(good,universe_parameter_count=None),{}):
                self.assertFalse(profile.matches_universes(bad,original=True))


class MonomorphicDriverIntegrationTests(unittest.TestCase):
    """Actual fixed Lean command checks; no simulated successful checker."""
    def compile(self,driver,proposition,proof,expected,command):
        checker=LeanChecker()
        self.assertIsNotNone(checker.binary,'fixed Lean unavailable; real audit cannot be claimed')
        path=ROOT/'agent_v2/lean'/driver
        self.assertTrue(path.is_file(),'missing fixed universe audit driver')
        with tempfile.TemporaryDirectory(prefix='qv2-universe-audit-') as temporary:
            source=Path(temporary)/'Probe.lean'
            source.write_text(path.read_text()+'\nuniverse u\n'
                +f'theorem Probe : ({proposition}) := {proof}\n'
                +f'def Expected : Prop := ({expected})\n'
                +f'{command} Probe against Expected nonce "universe-test"\n')
            result=subprocess.run([str(checker.binary),'-j','1','--json',str(source)],
                cwd=temporary,env=_lean_environment(checker.binary),capture_output=True,text=True,timeout=60)
        return result

    def test_closed_monomorphic_theorem_is_audited_with_zero_universes(self):
        result=self.compile('MonomorphicCheck.lean','(0 : Nat) = 0','by rfl',
                            '(0 : Nat) = 0','agent_v2_monomorphic_audit')
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)
        records=[json.loads(json.loads(line)['data']) for line in result.stdout.splitlines()
                 if 'agent_v2_audit_v1' in line]
        self.assertEqual(len(records),1)
        self.assertEqual(records[0]['universe_parameters'],[])
        self.assertEqual(records[0]['universe_parameter_count'],0)

    def test_monomorphic_driver_rejects_a_polymorphic_target_and_a_wrong_proof(self):
        proposition='∀ {A : Type u} (x : A), x = x'
        cases=[(proposition,'by intros; rfl',proposition),
               ('False','by exact True.intro','False'),
               ('(0 : Nat) = 0','by rfl','True')]
        for proposition,proof,expected in cases:
            with self.subTest(proposition=proposition,expected=expected):
                result=self.compile('MonomorphicCheck.lean',proposition,proof,expected,'agent_v2_monomorphic_audit')
                self.assertNotEqual(result.returncode,0,result.stdout+result.stderr)
                self.assertNotIn('agent_v2_audit_v1',result.stdout)

    def test_existing_polymorphic_driver_still_rejects_specialization(self):
        result=self.compile('TelescopingCheck.lean','(0 : Nat) = 0','by rfl',
                            '(0 : Nat) = 0','agent_v2_telescoping_audit')
        self.assertNotEqual(result.returncode,0,result.stdout+result.stderr)
        self.assertIn('retain the original universe',result.stdout)


if __name__=='__main__':unittest.main()
