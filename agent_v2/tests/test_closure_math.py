"""Controlled closure generation; receipt-shaped unit fixtures are not Lean evidence."""
import copy
from dataclasses import replace
from pathlib import Path
import re
import tempfile
import unittest

from agent_v2 import telescoping_closure
from agent_v2.formal_frontend import analyze_source
from agent_v2.models import Obligation, VerifiedCertificate
from agent_v2.storage import IntegrityError, RunStore, freeze_source, load_train
from agent_v2.telescoping_translation import local_proof


class ClosureMathTests(unittest.TestCase):
    def setUp(self):
        self.module = telescoping_closure
        self.temp = tempfile.TemporaryDirectory(prefix='qv2-closure-math-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.store = RunStore.create(self.root, 'selected')
        self.source = load_train('FQI-SRC-AP-3.3.9', self.store)
        self.frontend = analyze_source(self.source.to_dict(), self.store.root)

    def approved(self, frontend=None):
        frontend = frontend or self.frontend
        cert_id = 'telescoping-local-' + frontend['source']['sha256'][:20]
        cert = VerifiedCertificate(cert_id, frontend['local_proposition'],
                                   local_proof(frontend), frontend['source']['sha256'], (),
                                   {'test_only': 'not_Lean_evidence'})
        return {cert_id: cert.to_dict()}

    def altered(self, text, name):
        path = self.root / (name + '.lean')
        path.write_text(text)
        store = RunStore.create(self.root, name)
        source = freeze_source(path, 'STRUCTURAL-VARIANT', self.source.theorem, store)
        return analyze_source(source.to_dict())

    def test_closed_endpoint_obligations_retain_every_original_parameter(self):
        blueprint = self.module.closure_blueprint(self.frontend)
        prefix = '∀ {K : Type u} [Field K] (q : K) (m : ℕ) (n : ℕ) (h_domain : True), '
        expected = [
            prefix + 'FiniteQBenchmark.gaussian q (m + 0) (m + 1) = 0',
            prefix + ('FiniteQBenchmark.gaussian q (m + (n + 1)) (m + 1) = '
                      'FiniteQBenchmark.gaussian q (n + m + 1) (m + 1)'),
        ]
        obligations = [Obligation.from_dict(raw) for raw in blueprint['obligations']]
        self.assertEqual([o.proposition for o in obligations], expected)
        self.assertEqual(len({o.id for o in obligations}), 2)
        self.assertTrue(all(o.kind == 'boundary' and o.source_sha256 == self.source.sha256
                            and o.origin_action is None for o in obligations))
        self.assertEqual(blueprint['bridge_proposition'],
                         ' → '.join('(' + p + ')' for p in expected +
                                    [self.frontend['original_proposition']]))

    def test_bridge_explicitly_depends_on_existing_local_certificate(self):
        candidate = self.module.make_closure_candidate(self.frontend, 'bridge', self.approved(), 'action-bridge')
        self.assertEqual(candidate.dependencies, ('telescoping-local-' + self.source.sha256[:20],))
        self.assertEqual(candidate.closes, 'original')
        self.assertEqual(len(candidate.replaces), 2)
        self.assertTrue(all(o.origin_action == 'action-bridge' for o in candidate.replaces))
        self.assertEqual(candidate.theorem, 'AgentV2Candidate.proof')
        self.assertEqual(candidate.source_sha256, self.source.sha256)

    def test_missing_mismatched_or_uncontrolled_local_dependency_is_rejected(self):
        with self.assertRaises(IntegrityError):
            self.module.make_closure_candidate(self.frontend, 'bridge', {}, 'a')
        for key, value in [('id', 'other'), ('proposition', 'True'), ('source_sha256', '0'*64),
                           ('dependencies', ['unknown']), ('proof_term', 'by exact True.intro')]:
            approved = self.approved()
            approved[next(iter(approved))][key] = value
            with self.subTest(field=key), self.assertRaises(IntegrityError):
                self.module.make_closure_candidate(self.frontend, 'bridge', approved, 'a')

    def test_endpoint_candidates_close_only_their_exact_formal_obligation(self):
        blueprint = self.module.closure_blueprint(self.frontend)
        for task, raw in zip(('zero_endpoint', 'upper_endpoint'), blueprint['obligations']):
            with self.subTest(task=task):
                candidate = self.module.make_closure_candidate(self.frontend, task, {}, 'endpoint')
                self.assertEqual(candidate.closes, raw['id'])
                self.assertEqual(candidate.proposition, raw['proposition'])
                self.assertEqual(candidate.dependencies, ())
                self.assertEqual(candidate.replaces, ())

    def test_task_maps_identify_the_exact_certificate_and_open_obligation(self):
        blueprint = self.module.closure_blueprint(self.frontend)
        for task in ('bridge', 'zero_endpoint', 'upper_endpoint'):
            candidate = self.module.make_closure_candidate(self.frontend, task, self.approved(), 'a')
            self.assertEqual(blueprint['certificate_ids'][task], candidate.id)
            if task != 'bridge':
                self.assertEqual(blueprint['obligation_ids'][task], candidate.closes)
        self.assertEqual(blueprint['certificate_ids']['local'],
                         'telescoping-local-' + self.source.sha256[:20])

    def test_semantic_ids_survive_action_change_but_not_a_changed_source(self):
        first = self.module.make_closure_candidate(self.frontend, 'bridge', self.approved(), 'first')
        second = self.module.make_closure_candidate(self.frontend, 'bridge', self.approved(), 'second')
        self.assertEqual(first.id, second.id)
        self.assertEqual([o.id for o in first.replaces], [o.id for o in second.replaces])
        self.assertEqual(first.proof_term, second.proof_term)
        other = self.altered(self.source.declaration + '\n-- different frozen source\n', 'other')
        changed = self.module.make_closure_candidate(other, 'bridge', self.approved(other), 'first')
        self.assertNotEqual(first.id, changed.id)
        self.assertTrue(set(o.id for o in first.replaces).isdisjoint(o.id for o in changed.replaces))

    def test_alpha_names_and_reversed_equality_are_supported_without_identity_dispatch(self):
        text = self.source.declaration
        equation = ('(gaussian q (n+m+1) (m+1)) = '
                    '(∑ j ∈ Finset.range (n+1), ((q^j) * (gaussian q (m+j) (m))))')
        left, right = equation.split(' = ')
        self.assertIn(equation, text)
        text = text.replace(equation, right + ' = ' + left)
        for old, new in [('q', 'qv2flux'), ('m', 'qv2zero'), ('n', 'qv2sum'),
                         ('j', 'qv2step'), ('h_domain', 'qv2inst')]:
            text = re.sub(r'\b' + old + r'\b', new, text)
        frontend = self.altered(text, 'renamed')
        self.assertEqual(frontend['orientation'], 'sum_equals_target')
        candidate = self.module.make_closure_candidate(frontend, 'bridge', self.approved(frontend), 'a')
        self.assertEqual(candidate.source_sha256, frontend['source']['sha256'])
        self.assertEqual(candidate.closes, 'original')
        self.assertTrue(all('(qv2inst : True)' in o.proposition for o in candidate.replaces))

    def test_frontend_cannot_rebind_source_context_direction_or_endpoints(self):
        for key, value in [('original_proposition', 'True'), ('local_proposition', 'True'),
                           ('orientation', 'sum_equals_target'), ('symbols', {})]:
            frontend = copy.deepcopy(self.frontend)
            frontend[key] = value
            with self.subTest(field=key), self.assertRaises(IntegrityError):
                self.module.closure_blueprint(frontend)
        frontend = copy.deepcopy(self.frontend)
        frontend['source'] = replace(self.source, Gamma='True').to_dict()
        with self.assertRaises(IntegrityError):
            self.module.make_closure_candidate(frontend, 'zero_endpoint', {}, 'a')

    def test_unknown_task_and_missing_origin_action_are_not_silent_fallbacks(self):
        with self.assertRaises(ValueError):
            self.module.make_closure_candidate(self.frontend, 'all', self.approved(), 'a')
        with self.assertRaises(ValueError):
            self.module.make_closure_candidate(self.frontend, 'bridge', self.approved(), '')


if __name__ == '__main__':
    unittest.main()
