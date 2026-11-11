import dataclasses
import json
import tempfile
import unittest
from pathlib import Path


class ModelsStorageTests(unittest.TestCase):
    def test_strict_schema_and_deep_immutability(self):
        from agent_v2.models import Budget, RepresentationInstance, ContractError
        b = Budget(20.0, 3)
        self.assertEqual(Budget.from_dict(b.to_dict()), b)
        for field, value in [('actions', True), ('seconds', -1), ('seconds', float('nan')),
                             ('actions', '3'), ('schema_version', 2), ('extra', 1)]:
            data = b.to_dict(); data[field] = value
            with self.assertRaises(ContractError): Budget.from_dict(data)
        data = b.to_dict(); del data['actions']
        with self.assertRaises(ContractError): Budget.from_dict(data)
        r = RepresentationInstance('r', 'closed_prop', {'formula': ['True']}, None,
                                   (), 'True', ('initial',), 'a' * 64)
        with self.assertRaises(TypeError): r.payload['new'] = 'bad'
        with self.assertRaises(dataclasses.FrozenInstanceError): b.actions = 5
        data = r.to_dict(); data['kind'] = 'made_up'
        with self.assertRaises(ContractError): RepresentationInstance.from_dict(data)

    def test_guard_rejects_test_and_symlink_escape_without_read(self):
        from agent_v2.storage import guard_path, IntegrityError
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); (root / 'safe').mkdir()
            for name in ['benchmark/TEST.md', 'benchmark/splits/test.jsonl',
                         'benchmark/Statements/Test/NoRead.lean', 'Test/no_read']:
                with self.assertRaises(IntegrityError): guard_path(root / name)
            (root / 'alias').symlink_to(root / 'Test')
            with self.assertRaises(IntegrityError): guard_path(root / 'alias' / 'no_read')
            (root / 'safe' / 'escape').symlink_to(root)
            with self.assertRaises(IntegrityError): guard_path(root / 'safe' / 'escape' / 'x', root / 'safe')
            self.assertEqual(guard_path(root / 'tests' / 'test_ok.py'), root / 'tests' / 'test_ok.py')

    def test_atomic_store_and_source_tampering(self):
        from agent_v2.storage import RunStore, freeze_source, verify_source, IntegrityError
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); src = root / 'source.lean'
            src.write_text('theorem demo : True := by sorry\n')
            store = RunStore.create(root / 'runs', 'example')
            source = freeze_source(src, 'synthetic', 'demo', store, proposition='True')
            verify_source(source)
            from agent_v2.models import Budget, ContractError, initial_state
            state, _ = initial_state(source, Budget(10, 2))
            with self.assertRaises(dataclasses.FrozenInstanceError): source.theorem = 'Changed.statement'
            with self.assertRaises(dataclasses.FrozenInstanceError): state.Gamma = 'False'
            with self.assertRaises(ContractError): dataclasses.replace(state, Gamma='False')
            store.write_json('nested/value.json', {'a': 1})
            self.assertEqual(store.read_json('nested/value.json'), {'a': 1})
            with self.assertRaises(IntegrityError): store.write_json('../escape.json', {})
            with self.assertRaises(IntegrityError): RunStore.create(root / 'runs', 'example')
            src.write_text('theorem demo : False := by sorry\n')
            with self.assertRaises(IntegrityError): verify_source(source)

    def test_checkpoint_hash_mismatch_rejected(self):
        from agent_v2.storage import RunStore, IntegrityError
        with tempfile.TemporaryDirectory() as td:
            store = RunStore.create(Path(td), 'run')
            store.save_checkpoint({'schema_version': 1, 'value': 2})
            self.assertEqual(store.load_checkpoint()['value'], 2)
            manifest = store.read_json('checkpoint_manifest.json')
            store.path(manifest['path']).write_text('{"value": 99}')
            with self.assertRaises(IntegrityError): store.load_checkpoint()

    def test_checkpoint_boolean_version_is_not_integer_schema_one(self):
        from agent_v2.storage import RunStore, IntegrityError
        with tempfile.TemporaryDirectory() as td:
            store = RunStore.create(Path(td), 'run')
            store.save_checkpoint({'schema_version': 1, 'value': 2})
            manifest = store.read_json('checkpoint_manifest.json')
            manifest['schema_version'] = True
            store.write_json('checkpoint_manifest.json', manifest)
            with self.assertRaises(IntegrityError): store.load_checkpoint()

    def test_interrupted_checkpoint_commit_keeps_previous_generation(self):
        from unittest.mock import patch
        from agent_v2.storage import RunStore
        with tempfile.TemporaryDirectory() as td:
            store = RunStore.create(Path(td), 'run')
            store.save_checkpoint({'schema_version': 1, 'value': 2})
            write_json = store.write_json
            def interrupted(name, value):
                if name == 'checkpoint_manifest.json': raise OSError('simulated interruption')
                return write_json(name, value)
            with patch.object(store, 'write_json', interrupted):
                with self.assertRaises(OSError): store.save_checkpoint({'schema_version': 1, 'value': 3})
            self.assertEqual(store.load_checkpoint()['value'], 2)

    def test_renaming_same_action_cannot_bypass_repeat_guard(self):
        from agent_v2.models import Budget, JointAction, initial_state, action_fingerprint
        from agent_v2.storage import RunStore, freeze_source
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); src = root / 'source.lean'; src.write_text('True')
            store = RunStore.create(root, 'run')
            state, _ = initial_state(freeze_source(src, 'x', 'demo', store), Budget(10, 3))
            a = JointAction('a', 'identity', 'original', 'original', 'CAS', 'method', {'seconds': 5})
            b = dataclasses.replace(a, id='renamed-outlet')
            self.assertEqual(action_fingerprint(state, a), action_fingerprint(state, b))


if __name__ == '__main__': unittest.main()
