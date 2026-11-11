import contextlib
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


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


class CustomOutputCLITests(unittest.TestCase):
    """Real CLI/store/loop with a tiny temporary Train repository; no Test data."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='agent-v2-custom-output-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.repository = self.root / 'repository'
        self.generated = self.repository / 'agent_v2/generated'
        self.custom = self.root / 'custom-output'
        self.identity = 'SYNTHETIC-TRAIN-FIXTURE'
        self.source = self.repository / 'benchmark/lean/Benchmark/Statements/Train/Fixture.lean'
        self.source.parent.mkdir(parents=True)
        self.source.write_text('import Init\nnamespace Synthetic.TrainFixture\n'
                               'theorem statement : True := by sorry\nend Synthetic.TrainFixture\n')
        self.manifest = self.repository / 'benchmark/splits/train.jsonl'
        self.manifest.parent.mkdir(parents=True)
        self.manifest.write_text(json.dumps({'id': self.identity,
            'lean_path': 'lean/Benchmark/Statements/Train/Fixture.lean',
            'lean_sha256': hashlib.sha256(self.source.read_bytes()).hexdigest()}) + '\n')
        from agent_v2 import cli
        for name, value in [('REPOSITORY', self.repository), ('GENERATED', self.generated)]:
            override = patch.object(cli, name, value)
            override.start()
            self.addCleanup(override.stop)

    def invoke(self, *args):
        from agent_v2 import cli
        stdout, stderr = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = cli.main(args)
        return code, json.loads(stdout.getvalue().splitlines()[-1]), stderr.getvalue()

    def create_custom_run(self):
        code, result, error = self.invoke('run', '--identity', self.identity,
            '--output-root', str(self.custom), '--seconds', '10', '--max-steps', '1')
        self.assertEqual(code, 3, error)
        self.assertEqual(result['status'], 'environment_blocked')
        run = Path(result['run_dir'])
        self.assertEqual(run.parent, self.custom)
        self.assertTrue((run / 'checkpoint_manifest.json').is_file())
        return run

    def test_custom_output_run_is_resumable_through_real_cli(self):
        run = self.create_custom_run()
        code, result, error = self.invoke('resume', '--run-dir', str(run))
        self.assertEqual(code, 3, error)
        self.assertEqual(result['run_dir'], str(run))
        self.assertEqual(result['status'], 'budget_exhausted')
        self.assertFalse(result['original_identity_proved'])
        self.assertEqual(json.loads((run / 'run.json').read_text())['rounds'], 1)

    def test_resume_existing_run_outside_default_generated_tree(self):
        from agent_v2 import cli
        from agent_v2.storage import RunStore
        store = RunStore.create(self.custom)
        args = cli.parser().parse_args(['run', '--identity', self.identity,
                                       '--seconds', '10', '--max-steps', '1'])
        self.assertEqual(cli.train_run(args, store), 'environment_blocked')
        code, result, error = self.invoke('resume', '--run-dir', str(store.root))
        self.assertEqual(code, 3, error)
        self.assertEqual(result['status'], 'budget_exhausted')
        self.assertEqual(result['run_dir'], str(store.root))

    def test_custom_resume_still_rejects_source_tampering(self):
        run = self.create_custom_run()
        self.source.write_text('changed original')
        code, result, error = self.invoke('resume', '--run-dir', str(run))
        self.assertEqual(code, 4)
        self.assertEqual(result['status'], 'integrity_error')
        self.assertIn('hash mismatch', error)

    def test_custom_resume_still_rejects_checkpoint_tampering(self):
        run = self.create_custom_run()
        manifest = json.loads((run / 'checkpoint_manifest.json').read_text())
        (run / manifest['path']).write_text('{}\n')
        code, result, error = self.invoke('resume', '--run-dir', str(run))
        self.assertEqual(code, 4)
        self.assertEqual(result['status'], 'integrity_error')
        self.assertIn('checkpoint hash mismatch', error)

    def test_custom_resume_still_checks_train_identity_binding(self):
        from agent_v2.storage import RunStore
        run = self.create_custom_run()
        store = RunStore(run)
        checkpoint = store.load_checkpoint()
        checkpoint['state']['G']['identity'] = 'NOT-IN-TRAIN'
        store.save_checkpoint(checkpoint)
        code, result, error = self.invoke('resume', '--run-dir', str(run))
        self.assertEqual(code, 4)
        self.assertEqual(result['status'], 'integrity_error')
        self.assertIn('not bound to the selected Train original', error)

    def test_resume_guards_train_manifest_before_any_read(self):
        run = self.create_custom_run()
        forbidden = self.root / 'Test' / 'synthetic-manifest.jsonl'
        forbidden.parent.mkdir()
        forbidden.write_text('synthetic bytes that must never be read\n')
        self.manifest.unlink()
        self.manifest.symlink_to(forbidden)
        read_attempts = []
        original_read = Path.read_text

        def monitored_read(path, *args, **kwargs):
            if path.resolve() == forbidden:
                read_attempts.append(str(path))
                raise AssertionError('attempted a read before the Test path guard')
            return original_read(path, *args, **kwargs)

        with patch.object(Path, 'read_text', monitored_read):
            try:
                code, result, error = self.invoke('resume', '--run-dir', str(run))
            except AssertionError as failure:
                self.fail(str(failure))
        self.assertEqual(read_attempts, [])
        self.assertEqual(code, 4)
        self.assertEqual(result['status'], 'integrity_error')
        self.assertIn('held-out Test path refused', error)

    def test_custom_resume_keeps_snapshot_inside_its_own_run(self):
        from agent_v2.storage import RunStore
        run = self.create_custom_run()
        store = RunStore(run)
        checkpoint = store.load_checkpoint()
        initial = store.read_json('initial_state.json')
        # Keep bytes and the Train binding valid, but point the snapshot outside
        # this run in both states; only the run's artifact boundary can reject it.
        checkpoint['state']['G']['snapshot_path'] = str(self.source)
        initial['G']['snapshot_path'] = str(self.source)
        store.save_checkpoint(checkpoint)
        store.write_json('initial_state.json', initial)
        code, result, error = self.invoke('resume', '--run-dir', str(run))
        self.assertEqual(code, 4)
        self.assertEqual(result['status'], 'integrity_error')
        self.assertIn('artifact escapes run directory', error)

    def test_explicit_output_and_resume_paths_reject_symlink_ancestors(self):
        run = self.create_custom_run()
        alias = self.root / 'alias'
        alias.symlink_to(self.custom, target_is_directory=True)
        code, result, error = self.invoke('resume', '--run-dir', str(alias / run.name))
        self.assertEqual(code, 4)
        self.assertIn('symlink', error)
        before = set(self.custom.iterdir())
        code, result, error = self.invoke('run', '--identity', self.identity,
            '--output-root', str(alias / 'new-output'))
        self.assertEqual(code, 4)
        self.assertIn('symlink', error)
        self.assertEqual(set(self.custom.iterdir()), before)

    def test_explicit_test_paths_are_rejected_before_creation(self):
        forbidden = self.root / 'Test' / 'must-not-exist'
        for args in [('run', '--identity', self.identity, '--output-root', str(forbidden)),
                     ('resume', '--run-dir', str(forbidden))]:
            with self.subTest(command=args[0]):
                code, result, error = self.invoke(*args)
                self.assertEqual(code, 4)
                self.assertIn('held-out Test path refused', error)
                self.assertFalse(forbidden.exists())


if __name__ == '__main__': unittest.main()
