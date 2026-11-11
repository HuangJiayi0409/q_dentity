"""Real integration uses the current symbolic core and production Lean kernel."""
from dataclasses import replace
from pathlib import Path
import tempfile
import unittest

from agent_v2.executor import _candidate_request, normalize_result, validate_invariant, verify_and_update
from agent_v2.lean_checker import LeanChecker
from agent_v2.models import Budget, Candidate, JointAction, initial_state
from agent_v2.recurrence_adapter import RecurrenceAdapter, dependencies
from agent_v2.recurrence_frontend import analyze_source
from agent_v2.recurrence_translation import translate_candidate
from agent_v2.storage import RunStore, load_train
from agent_v2.tests.test_recurrence_translation import fixture


class RecurrenceCheckerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.store = RunStore.create(Path(self.temp.name) / 'runs')
        source = load_train('FQI-GAUSS-ALTERNATING', self.store)
        front = analyze_source(source.to_dict())
        self.source = replace(source, proposition=front['original_proposition'], dependencies=dependencies())
        self.front = analyze_source(self.source.to_dict())
        self.context = {'source_sha256': self.source.sha256, 'source': self.source.to_dict(),
                        'run_dir': str(self.store.root), 'attempt_dir': str(self.store.root / 'check'),
                        'seconds': 300}
        self.checker = LeanChecker()

    def candidate(self):
        return Candidate.from_dict(translate_candidate(self.front, fixture(self.front))['candidate'])

    def test_source_proposition_and_uncontrolled_term_are_rejected_before_lean(self):
        c = self.candidate()
        for altered in [replace(c, proposition='True'), replace(c, id='different_witness'),
                        replace(c, dependencies=('fake',))]:
            checked = self.checker.check_partial(_candidate_request(altered), self.context)
            self.assertFalse(checked['accepted'])
            self.assertEqual(checked['status'], 'integrity_error')
        altered = replace(c, proof_term=c.proof_term + '\n  run_tac unsafe_action')
        checked = self.checker.check_partial(_candidate_request(altered), self.context)
        self.assertFalse(checked['accepted'])
        self.assertEqual(checked['sigma']['code'], 'unsupported_term_syntax')
        self.assertFalse(self.store.path('check').exists())

    def test_real_recurrence_core_lean_update_and_wrong_proof_rejection(self):
        if self.checker.binary is None or not self.checker.binary.is_file():
            self.skipTest('integration: fixed Lean toolchain unavailable')
        result = normalize_result(RecurrenceAdapter().execute(self.source.identity, 'recurrence',
            self.source.to_dict(), self.store.root / 'backend', 90))
        self.assertEqual(result.status, 'symbolic_constructed', result.to_dict())
        self.assertEqual(result.raw_result['core']['solver'], 'q_zeilberger')
        self.assertEqual(result.raw_result['core']['status'], 'constructed')
        state, _ = initial_state(self.source, Budget(600, 1))
        action = JointAction('recurrence', 'identity', 'original', 'original', 'CAS', 'method', {})
        updated, diagnostics = verify_and_update(state, action, result, self.checker, self.context)
        self.assertEqual(len(updated.C), 1, diagnostics)
        self.assertEqual(updated.O, state.O)
        self.assertEqual(updated.links, ())
        validate_invariant(updated)
        self.assertEqual(updated.C[0].evidence['profile'], 'gaussian_geometric_recurrence_v1')
        audit = updated.C[0].evidence['audit']
        self.assertEqual(audit['universe_parameters'], ('u',))
        self.assertTrue(set(audit['axioms']) <= {'propext', 'Classical.choice', 'Quot.sound'})
        self.assertFalse(any('Statements' in m or m == 'Benchmark.Representation' for m in audit['modules']))
        candidate = result.C_partial[0]
        bad = replace(candidate, proof_term=candidate.proof_term.partition('\n')[0] + '\nby rfl')
        rejected, checks = verify_and_update(state, action, replace(result, C_partial=(bad,)),
            self.checker, dict(self.context, attempt_dir=str(self.store.root / 'negative')))
        self.assertEqual(rejected.C, ())
        self.assertEqual(rejected.O, state.O)
        self.assertIn('lean_check_failed', str(checks))


if __name__ == '__main__': unittest.main()
