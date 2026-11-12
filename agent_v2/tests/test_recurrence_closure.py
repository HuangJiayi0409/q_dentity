"""Closure contracts; fixture certificates never count as Lean evidence."""
import copy
from dataclasses import replace
import importlib
import json
from pathlib import Path
import re
import tempfile
import unittest

from agent_v2.models import Candidate, Obligation, VerifiedCertificate
from agent_v2.recurrence_frontend import analyze_source
from agent_v2.recurrence_translation import translate_candidate
from agent_v2.storage import IntegrityError, RunStore, freeze_source, load_train
from agent_v2.tests.test_recurrence_translation import fixture


class RecurrenceClosureTests(unittest.TestCase):
    def setUp(self):
        try:
            self.module = importlib.import_module('agent_v2.recurrence_closure')
        except ModuleNotFoundError:
            self.fail('source-bound recurrence closure implementation is missing')
        self.temp = tempfile.TemporaryDirectory(prefix='qv2-recurrence-closure-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.store = RunStore.create(self.root / 'runs')
        self.source = load_train('FQI-GAUSS-ALTERNATING', self.store)
        self.front = analyze_source(self.source.to_dict())

    def approved(self, front=None):
        front = front or self.front
        c = Candidate.from_dict(translate_candidate(front, fixture(front))['candidate'])
        cert = VerifiedCertificate(c.id, c.proposition, c.proof_term, c.source_sha256,
                                   c.dependencies, {'test_only': 'not Lean evidence'})
        return {c.id: cert.to_dict()}

    def variant(self, text):
        path = self.root / ('variant'+str(len(list(self.root.glob('variant*.lean'))))+'.lean')
        path.write_text(text)
        store = RunStore.create(self.root / 'runs')
        source = freeze_source(path, 'STRUCTURAL-UNIT-VARIANT', self.source.theorem, store)
        return analyze_source(source.to_dict())

    def test_blueprint_requires_three_separate_initial_and_rhs_obligations(self):
        bp = self.module.closure_blueprint(self.front)
        self.assertIsNone(bp['local_id'])
        self.assertEqual(bp['tasks'], ['uniqueness_bridge', 'rhs_recurrence', 'initial_zero', 'initial_one'])
        self.assertEqual(set(bp['certificate_ids']) - {'local'}, set(bp['tasks']))
        obligations = [Obligation.from_dict(o) for o in bp['obligations']]
        self.assertEqual(len(obligations), 3)
        self.assertEqual(len({o.id for o in obligations}), 3)
        self.assertTrue(all(o.source_sha256 == self.source.sha256 and o.origin_action is None for o in obligations))
        self.assertIn('(FiniteQBenchmark.poch q (q ^ 2) ((m + 2) / 2))', obligations[0].proposition)
        self.assertIn('(FiniteQBenchmark.gaussian q 0 j)', obligations[1].proposition)
        self.assertIn('(FiniteQBenchmark.gaussian q 1 j)', obligations[2].proposition)
        self.assertEqual(bp['bridge_proposition'], ' → '.join('('+p+')' for p in
                         [o.proposition for o in obligations]+[self.front['original_proposition']]))

    def test_initial_and_rhs_candidates_close_only_their_exact_leaf(self):
        bp = self.module.closure_blueprint(self.front)
        for task, raw in zip(bp['tasks'][1:], bp['obligations']):
            with self.subTest(task=task):
                c = self.module.make_closure_candidate(self.front, task, {}, 'leaf-action')
                self.assertEqual(c.id, bp['certificate_ids'][task])
                self.assertEqual(c.closes, raw['id'])
                self.assertEqual(c.proposition, raw['proposition'])
                self.assertEqual(c.dependencies, ())
                self.assertEqual(c.replaces, ())

    def test_bridge_requires_and_inlines_the_exact_local_certificate(self):
        with self.assertRaises(IntegrityError):
            self.module.make_closure_candidate(self.front, 'uniqueness_bridge', {}, 'bridge-action')
        approved = self.approved()
        bp = self.module.closure_blueprint(self.front, approved)
        c = self.module.make_closure_candidate(self.front, 'uniqueness_bridge', approved, 'bridge-action')
        self.assertEqual(bp['local_id'], next(iter(approved)))
        self.assertEqual(c.dependencies, (bp['local_id'],))
        self.assertEqual(c.closes, 'original')
        self.assertEqual(len(c.replaces), 3)
        self.assertTrue(all(o.origin_action == 'bridge-action' for o in c.replaces))
        self.assertEqual(c.proposition, bp['bridge_proposition'])
        self.assertEqual(c.theorem, 'AgentV2Candidate.proof')

    def test_local_receipt_is_not_a_proof_and_exact_term_is_rebuilt(self):
        for field, value in [('id', 'borrowed'), ('proposition', 'True'),
                             ('source_sha256', '0'*64), ('dependencies', ['foreign']),
                             ('proof_term', 'by exact True.intro')]:
            approved = self.approved()
            approved[next(iter(approved))][field] = value
            with self.subTest(field=field), self.assertRaises(IntegrityError):
                self.module.make_closure_candidate(self.front, 'uniqueness_bridge', approved, 'a')

    def test_duplicate_local_mapping_is_rejected_instead_of_arbitrary_selection(self):
        approved = self.approved()
        approved['another-key'] = copy.deepcopy(next(iter(approved.values())))
        with self.assertRaises(IntegrityError):
            self.module.closure_blueprint(self.front, approved)

    def test_nonstring_approval_key_is_an_integrity_error(self):
        cert = next(iter(self.approved().values()))
        with self.assertRaises(IntegrityError):
            self.module.closure_blueprint(self.front, {7: cert})

    def test_local_coefficients_are_revalidated_from_the_actual_witness(self):
        approved = self.approved()
        raw = approved[next(iter(approved))]
        header, _, body = raw['proof_term'].partition('\n')
        prefix = '/- agent_v2_recurrence_v1 '
        witness = json.loads(header[len(prefix):-3])
        witness['coefficients'] = ['1', '0', '1']
        raw['proof_term'] = prefix + json.dumps(witness, sort_keys=True, separators=(',', ':')) + ' -/\n' + body
        with self.assertRaises(IntegrityError):
            self.module.make_closure_candidate(self.front, 'uniqueness_bridge', approved, 'a')

    def test_local_only_target_cannot_silently_gain_a_full_closure(self):
        for old, new in [('else 0 :=', 'else 7 :='), ('m%2 = 0', 'm%2 = 1'),
                         ('(q^2)', '(q^3)'), ('(m/2)', '(m/3)')]:
            front = self.variant(self.source.declaration.replace(old, new))
            self.assertEqual(front['status'], 'applicable')
            with self.subTest(change=(old,new)), self.assertRaises(ValueError):
                self.module.closure_blueprint(front)

    def test_source_bound_frontend_cannot_change_context_target_or_orientation(self):
        for key, value in [('orientation', 'target_equals_sum'), ('original_proposition', 'True'),
                           ('target', {'op':'nat', 'value':0}), ('symbols', {})]:
            front = copy.deepcopy(self.front); front[key] = value
            with self.subTest(field=key), self.assertRaises(IntegrityError):
                self.module.closure_blueprint(front)
        front = copy.deepcopy(self.front)
        front['source'] = replace(self.source, Gamma='True').to_dict()
        with self.assertRaises(IntegrityError): self.module.closure_blueprint(front)

    def test_reconstruction_rejects_spoofed_id_type_and_dependencies(self):
        approved = self.approved()
        for task in ('uniqueness_bridge', 'rhs_recurrence', 'initial_zero', 'initial_one'):
            c = self.module.make_closure_candidate(self.front, task, approved, 'origin')
            request = {key:c.to_dict()[key] for key in ('id','proposition','proof_term','theorem','source_sha256','dependencies')}
            rebuilt = self.module.reconstruct_closure_candidate(self.front, request, approved)
            self.assertEqual(rebuilt.proof_term, c.proof_term)
            self.assertEqual(rebuilt.id, c.id)
            bad_proof = dict(request, proof_term='by rfl')
            self.assertEqual(self.module.reconstruct_closure_candidate(self.front, bad_proof, approved).proof_term,
                             c.proof_term)
            for key, value in [('id','spoofed'), ('proposition','True'),
                               ('source_sha256','0'*64), ('theorem','Wrong.theorem'),
                               ('dependencies', [] if c.dependencies else ['foreign'])]:
                with self.subTest(task=task,field=key), self.assertRaises(IntegrityError):
                    self.module.reconstruct_closure_candidate(self.front, dict(request, **{key:value}), approved)
        self.assertIsNone(self.module.reconstruct_closure_candidate(self.front,
                          {'id':'unknown','proposition':'True'}, {}))

    def test_action_origin_changes_no_semantic_id_but_frozen_source_does(self):
        approved = self.approved()
        first = self.module.make_closure_candidate(self.front, 'uniqueness_bridge', approved, 'first')
        second = self.module.make_closure_candidate(self.front, 'uniqueness_bridge', approved, 'second')
        self.assertEqual(first.id, second.id)
        self.assertEqual(first.proof_term, second.proof_term)
        self.assertEqual([o.id for o in first.replaces], [o.id for o in second.replaces])
        other = self.variant(self.source.declaration+'\n-- distinct source binding\n')
        changed = self.module.make_closure_candidate(other, 'uniqueness_bridge', self.approved(other), 'first')
        self.assertNotEqual(changed.id, first.id)

    def test_full_binders_and_reversed_alpha_source_keep_original_orientation(self):
        text = self.source.declaration.replace('(m : ℕ) :', '(m : ℕ) (qv2inst : True) :')
        lhs = '(∑ j ∈ Finset.range (m+1), (-1)^j*gaussian q m j)'
        rhs = 'if m%2 = 0 then poch q (q^2) (m/2) else 0'
        text = text.replace(lhs+' =\n '+rhs, '('+rhs+') = '+lhs)
        for old,new in [('K','qv2S'),('q','qv2rhs'),('m','qv2n'),('j','qv2one')]:
            text = re.sub(r'\b'+old+r'\b',new,text)
        front = self.variant(text)
        self.assertEqual(front['status'], 'applicable')
        self.assertEqual(front['orientation'], 'target_equals_sum')
        bp = self.module.closure_blueprint(front)
        self.assertTrue(all('(qv2inst : True)' in o['proposition'] for o in bp['obligations']))
        c = self.module.make_closure_candidate(front, 'uniqueness_bridge', self.approved(front), 'a')
        self.assertEqual(c.proposition, bp['bridge_proposition'])
        self.assertEqual(c.closes, 'original')

    def test_unknown_task_and_missing_action_are_rejected(self):
        with self.assertRaises(ValueError):
            self.module.make_closure_candidate(self.front, 'all', {}, 'a')
        with self.assertRaises(ValueError):
            self.module.make_closure_candidate(self.front, 'initial_zero', {}, '')


if __name__ == '__main__': unittest.main()
