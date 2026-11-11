import subprocess
import sys
import unittest


class CLITests(unittest.TestCase):
    def test_help_exposes_real_entrypoints(self):
        result = subprocess.run([sys.executable, '-m', 'agent_v2.cli', '--help'],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        for command in ('core-demo', 'run', 'resume'):
            self.assertIn(command, result.stdout)

    def test_invalid_budget_rejected_before_execution(self):
        result = subprocess.run([sys.executable, '-m', 'agent_v2.cli', 'run',
            '--identity', 'synthetic-not-loaded', '--max-steps', '-1'], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('positive', result.stderr)


if __name__ == '__main__': unittest.main()
