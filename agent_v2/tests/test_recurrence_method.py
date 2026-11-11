"""Method wiring fixtures are separate from the real integration below."""
from pathlib import Path
import tempfile
import time
import unittest
from unittest.mock import patch

from agent_v2.cas_adapter import adapter_result
from agent_v2.executor import normalize_result
from agent_v2.recurrence_frontend import analyze_source
from agent_v2.storage import RunStore, load_train
from agent_v2.tests.test_recurrence_translation import fixture


class RecurrenceMethodTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.store = RunStore.create(Path(self.temp.name) / 'runs')
        self.source = load_train('FQI-GAUSS-ALTERNATING', self.store)

    def execute(self):
        from agent_v2.recurrence_adapter import RecurrenceAdapter
        return normalize_result(RecurrenceAdapter().execute(self.source.identity, 'recurrence',
            self.source.to_dict(), self.store.root / 'backend', 60))

    def test_constructed_output_remains_only_an_unverified_candidate(self):
        raw = fixture(analyze_source(self.source.to_dict()))
        fake = adapter_result(time.monotonic(), 'symbolic_constructed', 'translation_pending',
                              'unit fixture only', raw_result=raw)
        with patch('agent_v2.cas_adapter.CoreAdapter.execute', return_value=fake) as core:
            outcome = self.execute()
        self.assertEqual(core.call_count, 1)
        self.assertEqual(outcome.status, 'symbolic_constructed')
        self.assertEqual(len(outcome.C_partial), 1)
        self.assertEqual(outcome.O_res, ())
        self.assertIsNone(outcome.C_partial[0].closes)
        self.assertFalse(outcome.original_identity_proved)

    def test_mismatch_never_runs_core(self):
        self.source = load_train('FQI-SRC-AP-3.3.9', self.store)
        with patch('agent_v2.cas_adapter.CoreAdapter.execute') as core:
            outcome = self.execute()
        core.assert_not_called()
        self.assertEqual(outcome.sigma.code, 'not_applicable')

    def test_timeout_failure_category_survives_normalization(self):
        with patch('agent_v2.cas_adapter.CoreAdapter.execute', return_value=adapter_result(
                time.monotonic(), 'budget_exhausted', 'timeout', 'unit timeout')):
            outcome = self.execute()
        self.assertEqual(outcome.status, 'budget_exhausted')
        self.assertEqual(outcome.sigma.code, 'timeout')
        self.assertFalse(outcome.C_partial)


if __name__ == '__main__': unittest.main()
