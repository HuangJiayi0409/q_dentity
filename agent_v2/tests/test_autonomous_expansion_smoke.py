"""Offline checks for the explicitly controlled expansion integration driver."""
import importlib.util
import unittest


class ControlledExpansionDriverTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(importlib.util.find_spec('agent_v2.tests.autonomous_expansion_smoke'),
                             'controlled expansion driver is not implemented')
        from agent_v2.tests import autonomous_expansion_smoke
        self.driver = autonomous_expansion_smoke

    def test_default_is_offline_with_two_model_calls_and_rule_selection(self):
        args = self.driver.parser().parse_args([])
        self.assertFalse(args.execute)
        auto = self.driver.autonomous_args(args)
        self.assertEqual(auto.identity, 'FQI-SRC-AP-3.3.9')
        self.assertEqual(auto.max_model_calls, 2)
        self.assertEqual(auto.selector, 'rule')
        self.assertEqual(auto.methods, 'telescoping')
        self.assertEqual(auto.max_expansions, 1)
        self.assertEqual(auto.max_repairs, 1)

    def test_constraint_rejects_direct_proof_or_different_children_without_rewriting(self):
        good = {'kind': 'decompose', 'children': ['True'], 'proof_term': 'fun h => h'}
        self.assertTrue(self.driver.matches_protocol(good, 'True'))
        for content in ({'kind': 'prove', 'proof_term': 'True.intro'},
                        dict(good, children=['False']), dict(good, children=['True', 'True']),
                        dict(good, extra=True)):
            self.assertFalse(self.driver.matches_protocol(content, 'True'))
        self.assertEqual(good, {'kind': 'decompose', 'children': ['True'], 'proof_term': 'fun h => h'})

    def test_payload_contains_exact_child_constraint_but_no_supplied_proof(self):
        payload = {'instructions': 'base instructions', 'purpose': 'local_proof',
                   'output_schema': {'prove': {}, 'decompose': {'kind': 'decompose'}}}
        constrained = self.driver.expansion_payload(payload, 'LOCAL_TYPE')
        self.assertEqual(constrained['required_children'], ['LOCAL_TYPE'])
        self.assertEqual(constrained['output_schema'], {'decompose': payload['output_schema']['decompose']})
        self.assertFalse(constrained['controlled_test']['model_proof_supplied'])
        self.assertEqual(payload['purpose'], 'local_proof')
        self.assertNotIn('proof_term', constrained)

    def test_only_actual_generated_json_format_failure_is_repairable(self):
        self.assertTrue(self.driver.format_repairable({'error_code': 'invalid_json_content', 'model_calls': 1}))
        for raw in ({'error_code': 'timeout', 'model_calls': 1},
                    {'error_code': 'provider_failed', 'model_calls': 1},
                    {'error_code': 'invalid_json_content', 'model_calls': 0}):
            self.assertFalse(self.driver.format_repairable(raw))


if __name__ == '__main__': unittest.main()
