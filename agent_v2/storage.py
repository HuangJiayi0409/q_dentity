"""Train-only source binding and atomic, run-contained artifact storage."""
import hashlib
import json
import os
import re
import tempfile
import uuid
from datetime import datetime, timezone
from pathlib import Path

from .models import Artifact, Source, canonical


class IntegrityError(ValueError):
    pass


def guard_path(path, root=None):
    path = Path(path).absolute()
    for candidate in (path, path.resolve()):
        parts = [p.casefold() for p in candidate.parts]
        if 'test' in parts or candidate.name.casefold() == 'test.md':
            raise IntegrityError('held-out Test path refused')
        if any(parts[i] == 'splits' and parts[i+1].startswith('test')
               for i in range(len(parts)-1)):
            raise IntegrityError('held-out Test split refused')
    if root is not None:
        root = Path(root).absolute()
        try:
            path.relative_to(root)
            path.resolve().relative_to(root.resolve())
        except ValueError as error:
            raise IntegrityError('artifact escapes run directory') from error
        if '..' in path.parts:
            raise IntegrityError('parent traversal refused')
        for parent in [path, *path.parents]:
            if parent == root.parent:
                break
            if parent.is_symlink():
                raise IntegrityError('symlink artifact refused')
    return path.resolve()


def sha256_file(path):
    path = guard_path(path)
    return hashlib.sha256(path.read_bytes()).hexdigest()


class RunStore:
    def __init__(self, root):
        self.root = guard_path(root)
        if not self.root.is_dir():
            raise IntegrityError('run directory does not exist')

    @classmethod
    def create(cls, output_root, run_id=None):
        run_id = run_id or datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ-') + uuid.uuid4().hex[:10]
        if not re.fullmatch(r'[A-Za-z0-9_-]+', run_id):
            raise IntegrityError('invalid run ID')
        output_root = guard_path(output_root)
        output_root.mkdir(parents=True, exist_ok=True)
        root = guard_path(output_root / run_id, output_root)
        try:
            root.mkdir()
        except FileExistsError as error:
            raise IntegrityError('run ID already exists') from error
        return cls(root)

    def path(self, relative):
        if Path(relative).is_absolute():
            raise IntegrityError('expected run-relative artifact path')
        return guard_path(self.root / relative, self.root)

    def write_bytes(self, relative, data):
        path = self.path(relative)
        path.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp = tempfile.mkstemp(prefix='.write-', dir=path.parent)
        try:
            with os.fdopen(fd, 'wb') as stream:
                stream.write(data); stream.flush(); os.fsync(stream.fileno())
            os.replace(tmp, path)
        finally:
            if os.path.exists(tmp): os.unlink(tmp)
        return path

    def write_json(self, relative, value):
        return self.write_bytes(relative, (canonical(value) + '\n').encode())

    def read_json(self, relative):
        def unique(pairs):
            result = {}
            for key, value in pairs:
                if key in result: raise IntegrityError('duplicate JSON key')
                result[key] = value
            return result
        return json.loads(self.path(relative).read_text(), object_pairs_hook=unique,
                          parse_constant=lambda x: (_ for _ in ()).throw(IntegrityError('nonfinite JSON')))

    def save_checkpoint(self, checkpoint):
        # The manifest points to an immutable content-addressed generation. A
        # crash before manifest replacement leaves the previous generation valid.
        data = (canonical(checkpoint) + '\n').encode()
        digest = hashlib.sha256(data).hexdigest()
        generation = 'checkpoints/' + digest + '.json'
        self.write_bytes(generation, data)
        self.write_bytes('checkpoint.json', data)
        self.write_json('checkpoint_manifest.json', {'schema_version': 1, 'path': generation, 'sha256': digest})

    def load_checkpoint(self):
        manifest = self.read_json('checkpoint_manifest.json')
        if (set(manifest) != {'schema_version', 'path', 'sha256'} or
                type(manifest['schema_version']) is not int or manifest['schema_version'] != 1):
            raise IntegrityError('invalid checkpoint manifest')
        if sha256_file(self.path(manifest['path'])) != manifest['sha256']:
            raise IntegrityError('checkpoint hash mismatch')
        # checkpoint.json is a convenient display copy, not the commit record.
        # It can be newer than the manifest if the process died during a commit.
        return self.read_json(manifest['path'])


def freeze_source(path, identity, theorem, store, proposition=None, dependencies=()):
    path = guard_path(path)
    data = path.read_bytes()
    declaration = data.decode('utf-8')
    sha = hashlib.sha256(data).hexdigest()
    snapshot = store.write_bytes('source/original.lean', data)
    # Until a formal frontend extracts a closed type, the exact entire source
    # carries Gamma; no additional mathematical assumptions are synthesized.
    return Source(identity, str(path), str(snapshot), sha, theorem, declaration,
                  declaration, proposition, tuple(dependencies))


def verify_source(source, run_root=None):
    if hashlib.sha256(source.declaration.encode()).hexdigest() != source.sha256:
        raise IntegrityError('declaration hash mismatch')
    if run_root is not None:
        guard_path(source.snapshot_path, run_root)
    for path in (source.path, source.snapshot_path):
        if sha256_file(path) != source.sha256:
            raise IntegrityError('source or snapshot hash mismatch')
    for dep in source.dependencies:
        if sha256_file(dep.path) != dep.sha256:
            raise IntegrityError('dependency hash mismatch')


def load_train(identity, store, repository=None):
    repository = Path(repository or Path(__file__).resolve().parents[1])
    manifest = guard_path(repository / 'benchmark/splits/train.jsonl')
    rows = [json.loads(line) for line in manifest.read_text().splitlines() if line.strip()]
    selected = [row for row in rows if row['id'] == identity]
    if len(selected) != 1:
        raise IntegrityError('identity not uniquely present in Train')
    row = selected[0]
    train_root = repository / 'benchmark/lean/Benchmark/Statements/Train'
    path = guard_path(repository / 'benchmark' / row['lean_path'], train_root)
    if sha256_file(path) != row['lean_sha256']:
        raise IntegrityError('Train manifest source hash mismatch')
    text = path.read_text()
    namespaces = re.findall(r'^namespace\s+([\w.]+)\s*$', text, re.MULTILINE)
    if len(namespaces) != 1 or len(re.findall(r'^theorem\s+statement\b', text, re.MULTILINE)) != 1:
        raise IntegrityError('unsupported Train theorem layout')
    return freeze_source(path, identity, namespaces[0] + '.statement', store,
                         dependencies=(Artifact(str(manifest), sha256_file(manifest)),))
