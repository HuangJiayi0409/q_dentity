"""Archive only the immutable, curated phase3 evidence directory."""
from pathlib import Path
import hashlib
import io
import json
import lzma
import os
import tarfile
import time

ROOT = Path(__file__).resolve().parents[3]
SOURCE_REL = Path('output/agent_v2_phase3_evidence_20261112')
SOURCE = ROOT / SOURCE_REL
DEST = Path(__file__).resolve().parent
ARCHIVE = DEST / 'agent_v2_phase3_evidence_20261112.tar.xz'
CHUNK = 1024 * 1024
PART_BYTES = 12 * CHUNK


def sha_file(path):
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        while block := stream.read(CHUNK):
            digest.update(block)
    return digest.hexdigest()


def save(name, data):
    path = DEST / name
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    os.replace(temporary, path)


def progress(stage, **extra):
    status = {'stage': stage, 'elapsed_seconds': time.monotonic() - START, **extra}
    save('progress.json', status)
    print(json.dumps(status), flush=True)


START = time.monotonic()
files = sorted(p for p in SOURCE.rglob('*') if p.is_file())
if len(files) != 6801:
    raise RuntimeError(f'Expected 6801 curated files, found {len(files)}')
if any(p.is_symlink() for p in SOURCE.rglob('*')):
    raise RuntimeError('Curated source contains a symlink')
if ARCHIVE.exists():
    raise RuntimeError('Refusing to overwrite an archive')
members = []
for number, path in enumerate(files, 1):
    rel = path.relative_to(ROOT)
    if not rel.is_relative_to(SOURCE_REL):
        raise RuntimeError('Source escaped curated root')
    members.append({'path': rel.as_posix(), 'bytes': path.stat().st_size,
                    'sha256': sha_file(path)})
expected = {entry['path']: entry for entry in members}
source_bytes = sum(entry['bytes'] for entry in members)
index_sha = sha_file(SOURCE / 'pack_index.json')
save('members.json', {'source_directory': SOURCE_REL.as_posix(), 'files': members})
progress('compressing', members=len(members), source_bytes=source_bytes)
last = time.monotonic()
partial = ARCHIVE.with_suffix('.xz.partial')
with lzma.open(partial, 'wb', format=lzma.FORMAT_XZ, check=lzma.CHECK_CRC64,
               filters=[{'id': lzma.FILTER_LZMA2, 'preset': 6,
                         'dict_size': 64 * 1024 * 1024}]) as compressed:
    with tarfile.open(fileobj=compressed, mode='w|', format=tarfile.PAX_FORMAT) as archive:
        for number, entry in enumerate(members, 1):
            path = ROOT / entry['path']
            info = tarfile.TarInfo(entry['path'])
            info.size = entry['bytes']
            info.uid = info.gid = info.mtime = 0
            info.uname = info.gname = ''
            info.mode = 0o644
            with path.open('rb') as stream:
                archive.addfile(info, stream)
            if time.monotonic() - last > 20:
                progress('compressing', members_done=number, members_total=len(members),
                         compressed_bytes_so_far=partial.stat().st_size)
                last = time.monotonic()
os.replace(partial, ARCHIVE)
progress('roundtrip_verification', archive_bytes=ARCHIVE.stat().st_size)
seen = set()
verified_bytes = 0
with tarfile.open(ARCHIVE, mode='r|xz') as archive:
    for member in archive:
        if not member.isfile() or member.name in seen or member.name not in expected:
            raise RuntimeError(f'Unexpected tar member: {member.name}')
        entry = expected[member.name]
        if member.size != entry['bytes']:
            raise RuntimeError(f'Tar member size mismatch: {member.name}')
        digest = hashlib.sha256()
        actual_bytes = 0
        with archive.extractfile(member) as stream:
            while block := stream.read(CHUNK):
                digest.update(block)
                actual_bytes += len(block)
        if actual_bytes != entry['bytes'] or digest.hexdigest() != entry['sha256']:
            raise RuntimeError(f'Tar member content mismatch: {member.name}')
        seen.add(member.name)
        verified_bytes += actual_bytes
if seen != set(expected) or verified_bytes != source_bytes:
    raise RuntimeError('Roundtrip member set mismatch')
for entry in members:
    path = ROOT / entry['path']
    if path.stat().st_size != entry['bytes'] or sha_file(path) != entry['sha256']:
        raise RuntimeError(f'Source changed during packaging: {entry["path"]}')
archive_sha = sha_file(ARCHIVE)
parts = []
if ARCHIVE.stat().st_size > PART_BYTES:
    with ARCHIVE.open('rb') as source:
        counter = 0
        while block := source.read(PART_BYTES):
            counter += 1
            path = DEST / f'{ARCHIVE.name}.part{counter:03d}'
            path.write_bytes(block)
            parts.append({'path': path.relative_to(ROOT).as_posix(), 'bytes': len(block),
                          'sha256': hashlib.sha256(block).hexdigest()})
    merged = hashlib.sha256()
    for part in parts:
        with (ROOT / part['path']).open('rb') as source:
            while block := source.read(CHUNK):
                merged.update(block)
    if merged.hexdigest() != archive_sha:
        raise RuntimeError('Split parts differ from original archive')
else:
    parts.append({'path': ARCHIVE.relative_to(ROOT).as_posix(),
                  'bytes': ARCHIVE.stat().st_size, 'sha256': archive_sha})
manifest = {
    'schema_version': 1,
    'scope': 'Byte-preserving transport of all curated phase3 evidence; no new proof execution',
    'source_directory': SOURCE_REL.as_posix(),
    'source_pack_index_sha256': index_sha,
    'archive': {'path': ARCHIVE.relative_to(ROOT).as_posix(), 'bytes': ARCHIVE.stat().st_size,
                'sha256': archive_sha, 'format': 'tar.xz', 'tar_format': 'PAX',
                'compression': {'filter': 'LZMA2', 'preset': 6,
                                'dict_size': 64 * 1024 * 1024, 'check': 'CRC64'}},
    'tar_metadata': {'mtime': 0, 'uid': 0, 'gid': 0, 'uname': '', 'gname': '', 'mode': '0644'},
    'members': {'count': len(members), 'total_bytes': source_bytes,
                'manifest': (DEST / 'members.json').relative_to(ROOT).as_posix(),
                'manifest_sha256': sha_file(DEST / 'members.json')},
    'roundtrip': {'passed': True, 'file_members_verified': len(seen),
                  'bytes_verified': verified_bytes,
                  'source_files_unchanged_after_packaging': True,
                  'all_member_sha256_and_sizes_verified': True},
    'publication': {'split': ARCHIVE.stat().st_size > PART_BYTES,
                    'maximum_part_bytes': PART_BYTES, 'parts': parts,
                    'full_archive_kept_locally': True,
                    'concatenated_parts_sha256_verified': True},
    'benchmark_Test_read': False, 'model_API_calls': 0,
    'elapsed_seconds': time.monotonic() - START,
}
save('transport_manifest.json', manifest)
progress('complete', archive_bytes=ARCHIVE.stat().st_size, archive_sha256=archive_sha,
         published_parts=len(parts), roundtrip_passed=True)
