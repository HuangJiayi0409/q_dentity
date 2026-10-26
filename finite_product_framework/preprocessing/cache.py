"""Content-addressed shared preprocessing; only verified immutable entries publish.

One per-key flock covers construction and readers. Failed staging directories are
kept for diagnosis and are never cache hits. Waiting consumes the caller's budget.
"""
import fcntl
import json
import os
from pathlib import Path
import time
import uuid

from .pipeline import HERE, check_snapshot, run, write_json
from .source import REPO, digest, load


def key_for(identity, support_modules=(), view="structured"):
    source = load(identity, support_modules)
    toolchain = (REPO/'project/lean-toolchain').read_text().strip()
    exe = Path.home()/'.elan/toolchains'/toolchain.replace('/', '--').replace(':', '---')/'bin/lean'
    material = dict(source=source.evidence(), normalization_view=view,
        implementation={str(p.relative_to(HERE)): digest(p.read_bytes())
                        for p in sorted(HERE.rglob('*')) if p.suffix in ('.py', '.lean')},
        toolchain=toolchain, executable=digest(exe.read_bytes()),
        libraries=digest((REPO/'project/lake-manifest.json').read_bytes()))
    return digest(json.dumps(material, sort_keys=True, separators=(',', ':')).encode())


def validate(directory):
    manifest = json.loads((directory/'cache_manifest.json').read_text())
    actual = {str(p.relative_to(directory)) for p in directory.rglob('*')
              if p.is_file() and p.name != 'cache_manifest.json'}
    if actual != set(manifest['files']): raise ValueError('cache_file_set_changed')
    for relative, expected in manifest['files'].items():
        if digest((directory/relative).read_bytes()) != expected:
            raise ValueError('cache_artifact_changed: '+relative)
    request = json.loads((directory/'request.json').read_text())
    check_snapshot(directory, request)
    status = json.loads((directory/'status.json').read_text())
    if status['status'] not in ('verified_unchanged', 'verified_normalized'):
        raise ValueError('cache_unverified')
    return status


def cached_run(identity, timeout=600, *, support_modules=(), root=None, view="structured"):
    start = time.monotonic()
    root = Path(root or os.environ.get('FINITEQ_PREPROCESS_CACHE',
                    REPO/'finite_product_framework/generated/preprocessing_cache_v2')).resolve()
    root.mkdir(parents=True, exist_ok=True)
    key = key_for(identity, support_modules, view)
    directory = root/key
    with (root/(key+'.lock')).open('a') as lock:
        while True:
            try:
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except BlockingIOError:
                if time.monotonic()-start >= timeout: raise TimeoutError('preprocessing_cache_wait_timeout')
                time.sleep(min(.1, max(0, timeout-(time.monotonic()-start))))
        if time.monotonic()-start >= timeout: raise TimeoutError('preprocessing_total_timeout')
        if directory.exists():
            # Corruption is explicit; never silently use or overwrite suspect evidence.
            status = validate(directory)
            return directory, dict(status, cache_hit=True, cache_key=key)
        staging = root/(key+'.pending-'+uuid.uuid4().hex)
        status = run(identity, staging, timeout=timeout-(time.monotonic()-start),
                     support_modules=support_modules, view=view)
        if key_for(identity, support_modules, view) != key:
            raise ValueError('preprocessing_cache_inputs_changed')
        write_json(staging/'cache_manifest.json', dict(key=key, files={
            str(p.relative_to(staging)): digest(p.read_bytes())
            for p in sorted(staging.rglob('*')) if p.is_file()}))
        staging.rename(directory)
        return directory, dict(status, cache_hit=False, cache_key=key)
