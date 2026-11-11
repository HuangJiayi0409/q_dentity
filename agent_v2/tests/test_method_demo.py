"""Actual standalone symbolic method probes have no fabricated formal state."""
import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest

from agent_v2 import cli


class MethodDemoTests(unittest.TestCase):
    def test_real_coefficient_core_demo_is_only_a_symbolic_construction(self):
        from agent_v2.symbolic_methods import example_request
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            request = root / 'input.json'
            request.write_text(json.dumps(example_request('coefficient')))
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                code = cli.main(['method-demo', '--method', 'coefficient', '--input', str(request),
                                 '--output-root', str(root / 'runs'), '--seconds', '30'])
            self.assertEqual(code, 2)
            summary = json.loads(output.getvalue().splitlines()[-1])
            run = Path(summary['run_dir'])
            report = json.loads((run / 'run.json').read_text())
            self.assertEqual(report['symbolic_status'], 'symbolic_constructed')
            self.assertFalse(report['formal_state'])
            self.assertFalse(report['original_identity_proved'])
            self.assertEqual(report['verified_certificates'], [])
            self.assertIsNone(json.loads((run / 'graph.json').read_text())['formal_graph'])
            self.assertFalse((run / 'checkpoint_manifest.json').exists())
            result = json.loads((run / 'rounds/1/result.json').read_text())
            self.assertEqual(result['raw_result']['method_id'], 'coefficient')
            self.assertEqual(result['raw_result']['capability_level'], 'L2')
            self.assertTrue(result['raw_result']['method_version'])

    def test_formal_only_method_does_not_fake_a_symbolic_request_contract(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            request = root / 'input.json'; request.write_text('{}')
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                code = cli.main(['method-demo', '--method', 'recurrence', '--input', str(request),
                                 '--output-root', str(root / 'runs')])
            self.assertEqual(code, 2)
            report = json.loads((Path(json.loads(output.getvalue())['run_dir']) / 'run.json').read_text())
            self.assertEqual(report['stop_reason'], 'capability_unavailable')


if __name__ == '__main__':
    unittest.main()
