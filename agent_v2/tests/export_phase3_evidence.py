"""Export retained evidence bytes and an explicit path/hash map; never certify proofs.

CLI: --index <JSON object with cases: [{id, run_dir}, ...]>
     --output-root <new or empty directory>

Sources under agent_v2/generated may be aggregate evidence directories. A
source elsewhere must be an explicitly indexed, structurally valid RunStore
with a content-addressed checkpoint and matching frozen source snapshot.
"""
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import stat

from agent_v2.graph import Graph
from agent_v2.models import ResidualState
from agent_v2.storage import IntegrityError, RunStore, guard_path


ROOT = Path(__file__).resolve().parents[2]
GENERATED = ROOT / 'agent_v2/generated'
CHUNK = 1024 * 1024
NOTE = """This package contains retained evidence, not a new mathematical proof.

Original JSON, Lean source, log and Candidate.olean bytes are copied without
rewriting. Absolute paths inside original receipts intentionally remain
unchanged. manifest.json maps each origin_path to its package_path and records
SHA-256 and size. Omitted files have package_path null and an explicit reason.
The exporter does not validate Lean proofs, trust receipts or change results.
Dependencies-before/after inventories, drivers and foundation Lean sources
are retained. External toolchains/import caches remain external dependencies
described by those original inventories; this is not a standalone toolchain.
Generated export metadata is an inventory aid and must not be treated as proof.
"""


def safe_path(value, root=None):
    if not isinstance(value, (str, Path)) or not str(value):
        raise IntegrityError('a nonempty filesystem path is required')
    raw = Path(value)
    if '..' in raw.parts:
        raise IntegrityError('parent traversal refused')
    path = raw.absolute()
    # Inspect every ancestor before resolve can erase evidence of a symlink.
    if any(parent.is_symlink() for parent in (path, *path.parents)):
        raise IntegrityError('symlink source or output path refused')
    return guard_path(path, root or path.anchor)


def load_json(path):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise IntegrityError('duplicate JSON object key')
            result[key] = value
        return result
    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=unique,
                      parse_constant=lambda _: (_ for _ in ()).throw(IntegrityError('nonfinite JSON')))


def signature(info):
    return (info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns, info.st_ctime_ns)


def inventory(directory):
    """Walk metadata only, rejecting links/special files even in omitted caches."""
    result = {}
    pending = [directory]
    while pending:
        parent = pending.pop()
        for entry in sorted(parent.iterdir()):
            entry = safe_path(entry, directory)
            info = entry.lstat()
            if stat.S_ISDIR(info.st_mode):
                pending.append(entry)
            elif stat.S_ISREG(info.st_mode):
                result[entry.relative_to(directory).as_posix()] = signature(info)
            else:
                raise IntegrityError('nonregular evidence file refused: ' + str(entry))
    return result


def check_source_directory(directory):
    if not directory.is_dir():
        raise IntegrityError('indexed run directory does not exist')
    if directory.is_relative_to(GENERATED):
        return 'project_generated_directory'
    # Validate the container and local snapshot, not old proof receipts or
    # external dependencies that this exporter does not own or reconstruct.
    store = RunStore(directory)
    checkpoint = store.load_checkpoint()
    if (not isinstance(checkpoint, dict)
            or set(checkpoint) != {'schema_version', 'state', 'graph', 'inflight'}
            or type(checkpoint['schema_version']) is not int or checkpoint['schema_version'] != 1
            or type(checkpoint['inflight']) is not bool):
        raise IntegrityError('external source is not a valid RunStore checkpoint')
    state = ResidualState.from_dict(checkpoint['state'])
    graph = Graph.from_dict(checkpoint['graph'])
    source = state.G
    if graph.source_sha256 != source.sha256 or state.r not in graph.nodes:
        raise IntegrityError('external RunStore graph is not bound to its source/current representation')
    snapshot = safe_path(source.snapshot_path, directory)
    safe_path(source.path)
    if (source.Gamma != source.declaration or state.Gamma != source.declaration
            or hashlib.sha256(source.declaration.encode()).hexdigest() != source.sha256
            or not snapshot.is_file() or snapshot.read_bytes() != source.declaration.encode()):
        raise IntegrityError('external RunStore frozen source snapshot differs from its declaration')
    return 'explicit_RunStore_checkpoint_and_snapshot'


def omission_reason(relative):
    path = Path(relative)
    if '__pycache__' in path.parts:
        return 'python_bytecode_cache'
    if path.name == 'Candidate.olean':
        return None
    if path.suffix in {'.ilean', '.c', '.o', '.pyc', '.pyo'}:
        return 'reproducible_compilation_or_bytecode_output'
    if (path.suffix in {'.olean', '.ir'} or
            any(path.name.endswith(suffix) for suffix in ('.olean.private', '.olean.server', '.olean.sig'))):
        return 'repeated_Lean_compilation_cache_except_Candidate.olean'
    return None


def transfer(origin, destination, expected_signature):
    """Hash every file; stream copied bytes without parsing or rewriting them."""
    origin = safe_path(origin)
    flags = os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0)
    fd = os.open(origin, flags)
    digest, size = hashlib.sha256(), 0
    target = None
    try:
        with os.fdopen(fd, 'rb') as source:
            if signature(os.fstat(source.fileno())) != expected_signature:
                raise IntegrityError('source changed before export: ' + str(origin))
            if destination is not None:
                destination = safe_path(destination)
                destination.parent.mkdir(parents=True, exist_ok=True)
                target = destination.open('xb')
            while block := source.read(CHUNK):
                digest.update(block)
                size += len(block)
                if target is not None:
                    target.write(block)
            if signature(os.fstat(source.fileno())) != expected_signature:
                raise IntegrityError('source changed while exporting: ' + str(origin))
            if target is not None:
                target.flush()
                os.fsync(target.fileno())
    finally:
        if target is not None:
            target.close()
    if signature(safe_path(origin).stat()) != expected_signature:
        raise IntegrityError('source path changed while exporting: ' + str(origin))
    checksum = digest.hexdigest()
    if destination is not None:
        copied = hashlib.sha256()
        with safe_path(destination).open('rb') as stream:
            while block := stream.read(CHUNK):
                copied.update(block)
        if copied.hexdigest() != checksum or destination.stat().st_size != size:
            raise IntegrityError('copied bytes differ from their source')
    return checksum, size


def export(index_path, output_root):
    index_path, output = safe_path(index_path), safe_path(output_root)
    if not index_path.is_file():
        raise IntegrityError('index must be an existing JSON file')
    index_signature = signature(index_path.stat())
    index = load_json(index_path)
    if not isinstance(index, dict) or not isinstance(index.get('cases'), list) or not index['cases']:
        raise IntegrityError('index must contain a nonempty cases array')
    cases, ids = [], set()
    for raw in index['cases']:
        if not isinstance(raw, dict) or set(raw) != {'id', 'run_dir'}:
            raise IntegrityError('each case must contain exactly id and run_dir')
        identity = raw['id']
        if (not isinstance(identity, str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,127}', identity)
                or identity in ids):
            raise IntegrityError('case IDs must be unique safe names')
        ids.add(identity)
        source = safe_path(raw['run_dir'])
        if output.is_relative_to(source) or source.is_relative_to(output):
            raise IntegrityError('output and source directories must not contain each other')
        category = check_source_directory(source)
        files = inventory(source)
        cases.append((identity, source, category, files))
    if output.exists() and (not output.is_dir() or any(output.iterdir())):
        raise IntegrityError('output root must be a new or empty directory')
    output.mkdir(parents=True, exist_ok=True)
    files, case_reports, reasons = [], [], Counter()
    for identity, source, category, before in cases:
        copied, omitted, copied_bytes, omitted_bytes = 0, 0, 0, 0
        for relative, expected in sorted(before.items()):
            reason = omission_reason(relative)
            package_path = (Path('cases') / identity / relative).as_posix()
            destination = safe_path(output / package_path, output) if reason is None else None
            checksum, size = transfer(source / relative, destination, expected)
            files.append({'case_id': identity, 'origin_path': str(source / relative),
                          'relative_path': relative, 'package_path': package_path if reason is None else None,
                          'sha256': checksum, 'size': size, 'status': 'copied' if reason is None else 'omitted',
                          'reason': reason})
            if reason is None:
                copied += 1; copied_bytes += size
            else:
                omitted += 1; omitted_bytes += size; reasons[reason] += 1
        case_reports.append({'id': identity, 'run_dir': str(source), 'source_category': category,
                             'package_root': 'cases/' + identity, 'copied': copied, 'omitted': omitted,
                             'copied_bytes': copied_bytes, 'omitted_bytes': omitted_bytes})
    # Refuse a successful manifest if anything changed or appeared during the
    # export. Incomplete output is retained for diagnosis, never reported valid.
    for _, source, _, before in cases:
        if inventory(source) != before:
            raise IntegrityError('evidence tree changed during export: ' + str(source))
    index_hash, index_size = transfer(index_path, output / 'export_index.json', index_signature)
    (output / 'README.txt').write_text(NOTE, encoding='utf-8')
    manifest = {'schema_version': 1, 'created_utc': datetime.now(timezone.utc).isoformat(),
                'scope': 'byte-preserving_evidence_export_only', 'proof_verification_performed': False,
                'receipt_paths_rewritten': False, 'absolute_path_mapping': 'files[].origin_path -> files[].package_path',
                'source_index': {'origin_path': str(index_path), 'package_path': 'export_index.json',
                                 'sha256': index_hash, 'size': index_size},
                'cases': case_reports, 'files': files,
                'copied': sum(c['copied'] for c in case_reports),
                'omitted': sum(c['omitted'] for c in case_reports),
                'copied_bytes': sum(c['copied_bytes'] for c in case_reports),
                'omitted_bytes': sum(c['omitted_bytes'] for c in case_reports),
                'omission_reasons': dict(sorted(reasons.items())),
                'generated_metadata': ['manifest.json', 'README.txt']}
    (output / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return manifest


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--index', required=True)
    parser.add_argument('--output-root', required=True)
    args = parser.parse_args(argv)
    manifest = export(args.index, args.output_root)
    print(json.dumps({'status': 'exported', 'proof_verification_performed': False,
                      'manifest': str(safe_path(args.output_root) / 'manifest.json'),
                      'cases': len(manifest['cases']), 'copied': manifest['copied'],
                      'omitted': manifest['omitted']}, ensure_ascii=False))


if __name__ == '__main__':
    main()
