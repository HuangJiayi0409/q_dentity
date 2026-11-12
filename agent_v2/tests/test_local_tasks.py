"""Generated local tasks are exact obligations or independent checked lemmas."""
import importlib.util
from dataclasses import replace
import hashlib
import tempfile
from pathlib import Path
import unittest

from agent_v2.models import Budget, Source, Obligation, initial_state
from agent_v2.lean_checker import init_original_template


class LocalTaskTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(importlib.util.find_spec('agent_v2.local_tasks'), 'typed local tasks missing')
        from agent_v2.local_tasks import make_task, candidate_for
        self.make_task, self.candidate_for = make_task, candidate_for
        tmp = tempfile.TemporaryDirectory(); self.addCleanup(tmp.cleanup)
        self.run = Path(tmp.name)
        declaration = init_original_template('Synthetic.statement', 'True ∧ True')
        original = self.run / 'source.lean'; original.write_text(declaration)
        self.source = Source('synthetic', str(original), str(original), hashlib.sha256(declaration.encode()).hexdigest(),
            'Synthetic.statement', declaration, declaration, 'True ∧ True')
        self.state, _ = initial_state(self.source, Budget(300, 10))

    def test_exact_connection_and_independent_lemma(self):
        children = tuple(Obligation('child' + str(i), 'subgoal', 'True', 'Synthetic.statement', self.source.sha256) for i in range(2))
        task = self.make_task(self.state, 'original', 'original', children=children)
        self.assertEqual(task.proposition, '(True) → (True) → (True ∧ True)')
        self.assertEqual(task.closes, 'original')
        self.assertEqual(type(task).from_dict(task.to_dict()), task)
        lemma = self.make_task(self.state, 'original', 'original', proposition='True')
        self.assertIsNone(lemma.closes)
        self.assertEqual(self.candidate_for(lemma, 'True.intro').replaces, ())

    def test_changed_context_foreign_children_missing_dependency_refused(self):
        with self.assertRaises(ValueError):
            replace(self.state, Gamma='False')
        for state, kwargs in [(self.state, {'dependencies': ('missing',)}),
                              (self.state, {'children': (Obligation('x', 'subgoal', 'True', 'x', '0'*64),)})]:
            with self.assertRaises(ValueError):
                self.make_task(state, 'original', 'original', **kwargs)

    def test_registered_target_dependency_and_source_cannot_be_changed(self):
        from agent_v2.local_proof_checker import LocalLeanChecker
        from agent_v2.executor import _candidate_request
        task = self.make_task(self.state, 'original', 'original')
        checker = LocalLeanChecker(tasks=(task,))
        request = _candidate_request(self.candidate_for(task, 'by constructor <;> trivial'))
        context = {'source': self.source.to_dict(), 'source_sha256': self.source.sha256,
                   'run_dir': str(self.run), 'attempt_dir': str(self.run/'check'), 'seconds': 0}
        for changed in [dict(request, proposition='True'), dict(request, dependencies=['fake']), dict(request, source_sha256='0'*64)]:
            result = checker.check_partial(changed, context)
            self.assertFalse(result['accepted'], result)
            self.assertEqual(result['status'], 'integrity_error', result)

    def test_changed_checked_dependency_cannot_be_rebound(self):
        from agent_v2.models import VerifiedCertificate
        from agent_v2.local_proof_checker import LocalLeanChecker
        from agent_v2.executor import _candidate_request
        # This is only an untrusted boundary fixture; it has no Lean receipt
        # and is never counted as accepted mathematical evidence.
        previous = VerifiedCertificate('previous', 'True', 'True.intro', self.source.sha256, (),
            {'source_sha256': self.source.sha256, 'proposition': 'True'})
        state = replace(self.state, C=(previous,))
        task = self.make_task(state, 'original', 'original', dependencies=(previous.id,))
        checker = LocalLeanChecker(tasks=(task,))
        altered = replace(previous, proof_term='by trivial')
        result = checker.check_partial(_candidate_request(self.candidate_for(task, 'by constructor <;> trivial')),
            {'source': self.source.to_dict(), 'source_sha256': self.source.sha256,
             'run_dir': str(self.run), 'attempt_dir': str(self.run/'check'), 'seconds': 10,
             'approved_certificates': {previous.id: altered.to_dict()}})
        self.assertEqual(result['status'], 'integrity_error', result)
        self.assertIn('dependency changed', result['sigma']['message'])
        self.assertFalse((self.run/'check').exists())


if __name__ == '__main__': unittest.main()
