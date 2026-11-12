"""Source-bound coefficient translation; core output is untrusted arithmetic."""
import copy
import importlib
import importlib.util
from pathlib import Path
import tempfile
import unittest

from agent_v2.coefficient_frontend import analyze_source
from agent_v2.models import Candidate
from agent_v2.storage import IntegrityError, RunStore, freeze_source, load_train
from agent_v2.symbolic_methods import request_digest
from agent_v2.symbolic_worker import construct


class CoefficientTranslationTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(importlib.util.find_spec('agent_v2.coefficient_translation'),
                             'source-bound coefficient translator is missing')
        self.module = importlib.import_module('agent_v2.coefficient_translation')
        temp = tempfile.TemporaryDirectory(); self.addCleanup(temp.cleanup)
        self.root = Path(temp.name); self.store = RunStore.create(self.root / 'runs')
        self.source = load_train('FQI-FINITE-Q-BINOMIAL', self.store)
        self.front = analyze_source(self.source.to_dict(), self.store.root)

    def raw(self):
        request = self.front['core_request']
        return {'schema_version': 1, 'method': 'coefficient', 'status': 'constructed',
                'request_sha256': request_digest(request), 'original_identity_proved': False,
                'construction': construct('coefficient', request['input'])}

    def reject(self, raw):
        result = self.module.translate_candidate(self.front, raw)
        self.assertEqual(result['status'], 'translation_pending', result)
        self.assertNotIn('candidate', result)

    def test_actual_core_yields_bound_all_index_local_candidate(self):
        result = self.module.translate_candidate(self.front, self.raw())
        self.assertEqual(result['status'], 'candidate_ready', result)
        candidate = Candidate.from_dict(result['candidate'])
        self.assertEqual(candidate.source_sha256, self.source.sha256)
        self.assertEqual(candidate.dependencies, ())
        self.assertIsNone(candidate.closes)
        self.assertEqual(candidate.replaces, ())
        self.assertEqual(candidate.proposition,
            '∀ {K : Type u} [Field K] (q : K) (z : K) (n : ℕ), '
            '(AgentV2Coefficient.pochPolynomial q n).eval z = FiniteQBenchmark.poch z q n ∧ '
            '(AgentV2Coefficient.pochPolynomial q (n+1)).coeff 0 = '
            '(AgentV2Coefficient.pochPolynomial q n).coeff 0 ∧ '
            '∀ qv2degree : ℕ, (AgentV2Coefficient.pochPolynomial q (n+1)).coeff (qv2degree+1) = '
            '(AgentV2Coefficient.pochPolynomial q n).coeff (qv2degree+1) - '
            'q^n * (AgentV2Coefficient.pochPolynomial q n).coeff qv2degree')
        self.assertEqual(result['independent_symbolic_check']['checked_goals'], 2)
        self.assertFalse(result['lean_verified'])
        self.assertFalse(result['original_identity_proved'])
        self.assertEqual(candidate, self.module.make_candidate(self.front))

    def test_false_normal_forms_are_rejected_even_with_zero_residual(self):
        for field in ('lhs_normal_form', 'rhs_normal_form'):
            raw = self.raw(); raw['construction']['goals'][0][field] = '0'
            with self.subTest(field=field): self.reject(raw)
        raw = self.raw()
        raw['construction']['goals'][0].update(lhs_normal_form='v0', rhs_normal_form='v0', residual='0')
        self.reject(raw)
        raw = self.raw(); raw['construction']['goals'][0]['residual'] = '1'
        self.reject(raw)

    def test_core_request_identity_status_and_construction_are_bound(self):
        for key, value in [('request_sha256', '0' * 64), ('method', 'interpolation'),
                           ('status', 'search_exhausted'), ('schema_version', True),
                           ('original_identity_proved', True)]:
            raw = self.raw(); raw[key] = value
            with self.subTest(key=key): self.reject(raw)
        for key, value in [('goal_count', 1), ('closed_goal_count', 1),
                           ('denominator_cancellation', True), ('cross_method_dependencies', ['p1'])]:
            raw = self.raw(); raw['construction'][key] = value
            with self.subTest(key=key): self.reject(raw)
        raw = self.raw(); raw['construction']['goals'].pop(); self.reject(raw)
        self.reject(None)

    def test_atom_swaps_duplicates_or_unknowns_are_rejected(self):
        for value in ([{'symbol': 'v0', 'display': 'u'}, {'symbol': 'v1', 'display': 'v'},
                       {'symbol': 'v2', 'display': 'w'}],
                      [{'symbol': 'v0', 'display': 'v'}, {'symbol': 'v0', 'display': 'u'},
                       {'symbol': 'v2', 'display': 'w'}], []):
            raw = self.raw(); raw['construction']['goals'][0]['atoms'] = value
            with self.subTest(atoms=value): self.reject(raw)

    def test_arithmetic_parser_rejects_code_division_and_resource_bombs(self):
        for value in ['__import__("os").system("false")', 'v0 / v0', 'v0**1000000000',
                      'v9', '1.0', 'True', '[v0]', 'v0 << 1', '9' * 5000]:
            raw = self.raw(); raw['construction']['goals'][0]['lhs_normal_form'] = value
            with self.subTest(value=value[:30]): self.reject(raw)

    def test_cas_proof_text_has_no_effect_and_equivalent_arithmetic_is_checked(self):
        raw = self.raw()
        raw['construction']['goals'][0].update(
            lhs_normal_form='(v0 + 0) - v2*v1', rhs_normal_form='-v1*v2 + v0',
            residual='v0-v0', proof='by sorry')
        first = self.module.translate_candidate(self.front, raw)
        self.assertEqual(first['status'], 'candidate_ready', first)
        self.assertNotIn('sorry', first['candidate']['proof_term'])
        self.assertEqual(first['candidate'], self.module.make_candidate(self.front).to_dict())

    def test_frontend_source_or_semantic_map_injection_is_rejected(self):
        for key, value in [('coefficient_atoms', {}), ('binders', []), ('all_natural_indices', False),
                           ('original_proposition', 'True'), ('representation', {})]:
            front = copy.deepcopy(self.front); front[key] = value
            with self.subTest(key=key), self.assertRaises(IntegrityError):
                self.module.make_candidate(front)
        front = copy.deepcopy(self.front); front['source']['Gamma'] = 'True'
        with self.assertRaises(IntegrityError): self.module.translate_candidate(front, self.raw())
        front = copy.deepcopy(self.front); front['core_request']['input']['goals'][0]['rhs'] = {'op':'integer','value':0}
        with self.assertRaises(IntegrityError): self.module.make_candidate(front)

    def test_alpha_renamed_extra_binders_and_identifier_collisions_survive(self):
        original_id = self.module.make_candidate(self.front).id
        text = self.source.declaration.replace('(q z : K) (n : ℕ)',
            '(a b : K) (m : ℕ) (qv2inst : True) (qv2degree : ℕ)')
        text = text.replace('(-1)^k*z^k*q^(k*(k-1)/2)*gaussian q n k',
                            '(-1)^k*b^k*a^(k*(k-1)/2)*gaussian a m k')
        text = text.replace('(n+1)', '(m+1)').replace('poch z q n', 'poch b a m')
        path = self.root / 'Renamed.lean'; path.write_text(text)
        source = freeze_source(path, 'structural_test_only', self.source.theorem, self.store)
        front = analyze_source(source.to_dict(), self.store.root)
        candidate = self.module.make_candidate(front)
        self.assertIn('(a : K) (b : K) (m : ℕ) (qv2inst : True) (qv2degree : ℕ)', candidate.proposition)
        self.assertIn('∀ qv2degreex : ℕ', candidate.proposition)
        self.assertIn('intro K qv2instx a b m qv2inst qv2degree', candidate.proof_term)
        self.assertIn('product_coefficients a b m', candidate.proof_term)
        self.assertNotEqual(candidate.id, original_id)

    def test_json_boolean_integer_alias_does_not_bypass_source_reconstruction(self):
        front = copy.deepcopy(self.front); front['all_natural_indices'] = 1
        with self.assertRaises(IntegrityError): self.module.make_candidate(front)


if __name__ == '__main__': unittest.main()
