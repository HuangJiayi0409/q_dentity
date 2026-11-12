#!/usr/bin/env python3
"""Build a deterministic, source-preserving audit selection. No network calls."""
from __future__ import annotations

import collections
import lzma
import hashlib
import io
import json
import math
from pathlib import Path, PurePosixPath
import re
import sys
import tarfile
import tempfile

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
BASE = ROOT / "agent_v2/generated/autonomous_20261112"
ARCHIVE = OUT / "autonomous_20261112_audit.tar.xz"
TREES = [
    "before", "after", "final_revision_01", "final_revision_02",
    "math_probe/local_boundary", "preflight_sandbox", "preflight_host",
    "preflight_identified_client", "preflight_updated_credential",
]
FILES = [
    "baseline.json", "changed_files.json", "changes.diff", "final_validation.json",
    "finalize.py", "train_preregistration.json", "live_preflight.py",
    "math_probe/live_hockey_audit.json", "math_probe/live_hockey_audit.md",
    "math_probe/live_hockey_audit.py", "math_probe/runtime_review.md",
    "math_probe/review_controls.json", "math_probe/review_controls.py",
    "math_probe/local_security_review.md", "math_probe/local_boundary_probe.py",
    "task2_independent_review.md", "task2_review_counter_probe.json",
    "task2_review_inflight_probe.json", "task2_tests.log", "task2_validation.json",
    "task2_ua_diagnosis.md", "task2_ua_validation.json",
    "controlled_expansion_driver_report.md",
    "task1/controlled_expansion_driver.diff", "task1/controlled_expansion_driver_manifest.json",
    "task1/controlled_expansion_driver_tests.log", "task1/controlled_expansion_prepare.log",
    "task1/controlled_expansion_prepare_validation.json",
]
ORIGINAL_GZIP_INVENTORY_SHA256 = '881a8ecd14758fe550ca85391eafbe4fbf86fabe6ab0eb55eaa4d9e7dc9dd7e2'
BINARY_SUFFIXES = {".olean", ".ilean", ".o", ".c", ".ir", ".so", ".a", ".pyc", ".pyo"}


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def record(path: Path) -> dict:
    data = path.read_bytes()
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(data), "sha256": digest(data)}


def write_json(path: Path, value) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n")


def exclusion(path: Path) -> str | None:
    if path.is_symlink():
        return "symbolic_link_not_followed"
    if any(part.startswith("API_") or part in {".git", ".aws", "auth", "credentials", ".env"}
           for part in path.parts):
        return "credential_or_auth_configuration"
    if "__pycache__" in path.parts or "build" in path.parts:
        return "generated_build_output_recompile_from_matching_sources_and_environment"
    if path.suffix in BINARY_SUFFIXES or any(".olean." in part for part in path.parts):
        return "compiled_binary_recompile_from_matching_sources_and_environment"
    return None


def selected_files():
    candidates = set()
    summaries = []
    for rel in TREES + FILES:
        root = BASE / rel
        if not root.exists():
            raise RuntimeError(f"Missing explicit allowlist entry: {rel}")
        entries = sorted(p for p in root.rglob("*") if p.is_file()) if root.is_dir() else [root]
        rows = [record(p) for p in entries]
        summaries.append({"path": root.relative_to(ROOT).as_posix(), "files": len(rows),
                          "bytes": sum(x["bytes"] for x in rows),
                          "inventory_sha256": digest(json.dumps(rows, sort_keys=True,
                                                                  separators=(",", ":")).encode())})
        candidates.update(entries)
    selected, omitted = [], []
    for path in sorted(candidates):
        reason = exclusion(path)
        if reason:
            omitted.append({**record(path), "reason": reason,
                            "recoverability": "not_in_archive; rebuild requires matching source dependencies and external Lean environment"})
        else:
            selected.append(path)
    return selected, omitted, summaries


def audit_bound_manifests(selected):
    paths = set(selected)
    revisions = []
    for rev in ("final_revision_01", "final_revision_02"):
        data = json.loads((BASE / rev / "source_manifest.json").read_text())
        rows = data["files"]
        for row in rows:
            path = BASE / rev / "frozen" / row["path"]
            assert path in paths and digest(path.read_bytes()) == row["sha256"], path
        revisions.append({"revision": rev, "files": len(rows), "frozen_hashes_match": True})
    changes = json.loads((BASE / "changed_files.json").read_text())["files"]
    for row in changes:
        path = BASE / "after" / row["path"]
        assert path in paths and digest(path.read_bytes()) == row["sha256"], path
    final = json.loads((BASE / "final_validation.json").read_text())
    for key in ("full_suite", "final_targeted_suite"):
        row = final[key]
        assert digest((BASE / row["path"]).read_bytes()) == row["sha256"]
    return {"revisions": revisions, "changed_files": len(changes),
            "after_hashes_match": True, "suite_logs_match_final_validation": True}


def collect_references(selected, rows, omitted):
    by_path = {r["path"]: r for r in rows}
    by_sha = collections.defaultdict(list)
    for row in rows:
        by_sha[row["sha256"]].append(row["path"])
    omitted_by_path = {r["path"]: r for r in omitted}
    refs = {}

    def visit(value, owner):
        if isinstance(value, dict):
            if isinstance(value.get("path"), str) and re.fullmatch(r"[0-9a-f]{64}", str(value.get("sha256", ""))):
                key = (value["path"], value["sha256"])
                row = refs.setdefault(key, {"references": 0, "first_referenced_by": owner})
                row["references"] += 1
            for v in value.values():
                visit(v, owner)
        elif isinstance(value, list):
            for v in value:
                visit(v, owner)

    for path in selected:
        if path.suffix == ".json":
            visit(json.loads(path.read_text()), path.relative_to(ROOT).as_posix())
    resolved = []
    unresolved_internal = []
    for (raw, sha), meta in sorted(refs.items()):
        path = Path(raw)
        if path.is_absolute():
            try:
                rel = path.relative_to(ROOT).as_posix()
            except ValueError:
                rel = None
        else:
            rel = path.as_posix()
        row = {"path": raw, "sha256": sha, **meta}
        if rel in by_path and by_path[rel]["sha256"] == sha:
            row.update(disposition="included_at_original_relative_path", archive_path=rel)
        elif rel in omitted_by_path:
            assert omitted_by_path[rel]["sha256"] == sha, raw
            row.update(disposition="omitted_compiled_artifact", reason=omitted_by_path[rel]["reason"],
                       recoverability=omitted_by_path[rel]["recoverability"])
        elif sha in by_sha:
            row.update(disposition="identical_content_available_in_archive",
                       archive_path=min(by_sha[sha], key=lambda p: (len(p), p)),
                       note="Original absolute path is historical; locate the identical bytes by this archive path and SHA256.")
        elif rel is not None and rel.startswith(BASE.relative_to(ROOT).as_posix() + "/"):
            row.update(disposition="unresolved_internal_artifact")
            unresolved_internal.append(row)
        else:
            row.update(disposition="external_environment_or_repository_prerequisite_not_packaged",
                       reason="Outside the explicit generated-evidence allowlist; original path/hash retained. Requires the matching repository, dependencies and toolchain; not a standalone replay archive.")
        resolved.append(row)
    if unresolved_internal:
        write_json(OUT / "unresolved_internal.json", unresolved_internal)
        raise RuntimeError("Internal evidence reference missing; see unresolved_internal.json (paths only)")
    return resolved


def entropy(token: bytes) -> float:
    counts = collections.Counter(token)
    return -sum((n / len(token)) * math.log2(n / len(token)) for n in counts.values())


def credential_candidates():
    # Credentials are read only into memory for exact-match scanning. They are never serialized.
    candidates = set()
    sources = []
    for name in ("API_GPT", "API_Jev", "API_deepseek"):
        path = ROOT / name
        if not path.is_file():
            continue
        sources.append(name)
        data = path.read_bytes()
        for token in re.findall(rb"[A-Za-z0-9_~.+/-]{20,}", data):
            if (b"/" not in token and b"." not in token and entropy(token) >= 3.2
                    and any(48 <= c <= 57 for c in token)
                    and any(65 <= c <= 90 or 97 <= c <= 122 for c in token)):
                candidates.add(token)
        for token in re.findall(rb"(?:sk-[A-Za-z0-9_-]{16,}|gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})", data):
            candidates.add(token)
    return candidates, sources


def sensitive_scan(paths):
    candidates, sources = credential_candidates()
    patterns = {
        "private_key": re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
        "provider_token": re.compile(rb"\b(?:sk-[A-Za-z0-9_-]{24,}|gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,})\b"),
        "long_bearer_literal": re.compile(rb"\bBearer[ \t]+[A-Za-z0-9._~-]{28,}"),
    }
    findings = []
    for path in paths:
        data = path.read_bytes()
        rel = path.relative_to(ROOT).as_posix()
        if any(secret in data for secret in candidates):
            findings.append({"path": rel, "rule": "exact_match_to_local_credential"})
        for name, pattern in patterns.items():
            if pattern.search(data):
                findings.append({"path": rel, "rule": name})
    return {"status": "passed" if not findings else "review_required", "files_scanned": len(paths),
            "credential_source_names": sources, "credential_values_saved": False,
            "known_secret_exact_match_scan": True, "regex_scan": True,
            "findings": findings, "scope": "Selected plaintext evidence and transport metadata; credential values never output."}


def make_archive(destination, selected):
    with destination.open("wb") as raw:
        with lzma.LZMAFile(raw, mode="wb", format=lzma.FORMAT_XZ, check=lzma.CHECK_CRC64, preset=9) as zipped:
            with tarfile.open(fileobj=zipped, mode="w", format=tarfile.PAX_FORMAT) as archive:
                for path in selected:
                    data = path.read_bytes()
                    info = tarfile.TarInfo(path.relative_to(ROOT).as_posix())
                    info.size, info.mode, info.uid, info.gid, info.mtime = len(data), 0o644, 0, 0, 0
                    info.uname = info.gname = ""
                    archive.addfile(info, io.BytesIO(data))


def verify_archive(rows):
    expected = {r["path"]: r for r in rows}
    with tempfile.TemporaryDirectory(prefix="verify-", dir=OUT) as temporary:
        target = Path(temporary)
        with tarfile.open(ARCHIVE, "r:xz") as archive:
            members = archive.getmembers()
            assert len(members) == len(expected)
            assert len({m.name for m in members}) == len(members)
            for member in members:
                p = PurePosixPath(member.name)
                assert member.isfile() and not p.is_absolute() and ".." not in p.parts
                assert member.name in expected
                assert (member.uid, member.gid, member.mtime, member.mode) == (0, 0, 0, 0o644)
                destination = target / member.name
                destination.parent.mkdir(parents=True, exist_ok=True)
                stream = archive.extractfile(member)
                assert stream is not None
                destination.write_bytes(stream.read())
        actual = []
        for name, row in expected.items():
            data = (target / name).read_bytes()
            assert len(data) == row["bytes"] and digest(data) == row["sha256"], name
            actual.append(name)
        assert sorted(actual) == sorted(expected)
    return len(expected)


def main():
    selected, omitted, summaries = selected_files()
    rows = [record(p) for p in selected]
    assert digest(json.dumps(rows, sort_keys=True, separators=(",", ":")).encode()) == ORIGINAL_GZIP_INVENTORY_SHA256, "XZ selection differs from original gzip payload"
    bound_checks = audit_bound_manifests(selected)
    references = collect_references(selected, rows, omitted)
    members = {"schema_version": 1, "archive": ARCHIVE.name,
               "path_convention": "repository-relative original paths; original evidence bytes unchanged",
               "files": rows, "omitted_files_within_allowlist": omitted,
               "referenced_artifact_resolution": references,
               "claim": "Curated audit archive, not a complete original runtime image or directly resumable checkpoint."}
    write_json(OUT / "members.json", members)
    counts = collections.Counter(r["disposition"] for r in references)
    manifest = {"schema_version": 1, "source_root": BASE.relative_to(ROOT).as_posix(),
                "allowlist_trees": TREES, "allowlist_files": FILES,
                "original_allowlist_summaries": summaries,
                "payload_files": len(rows), "payload_bytes": sum(r["bytes"] for r in rows),
                "payload_inventory_sha256": digest(json.dumps(rows, sort_keys=True, separators=(",", ":")).encode()),
                "excluded_files_in_allowlist": len(omitted),
                "excluded_bytes_in_allowlist": sum(r["bytes"] for r in omitted),
                "reference_dispositions": dict(sorted(counts.items())),
                "bound_source_and_log_checks": bound_checks,
                "exclusion_policy": [
                    "No recursive repository scan: enumerate only the explicit current-run allowlist.",
                    "No benchmark/Test read or scan; no historical agent frameworks read or archived.",
                    "No API_* files, auth configuration, secrets, toolchain binaries, compiled/build artifacts.",
                    "Unlisted temporary development directories are omitted; reported failed model rounds and the excluded duplicate remain.",
                    "Retain original receipt/dependency hashes; enumerate omitted binaries and locate same-hash source copies.",
                    "Dependencies outside the evidence allowlist are recorded prerequisites, not asserted available in this archive."
                ],
                "archive_metadata": {"member_order": "lexicographic repository-relative path", "mtime": 0,
                                     "uid": 0, "gid": 0, "mode": "0644", "xz_preset": 9, "xz_dictionary_bytes": 67108864, "xz_check": "CRC64"},
                "test_and_network_activity": {"new_model_calls": 0, "network_calls": 0, "lean_reruns": 0,
                                              "historical_tests_rerun": False},
                "limits": ["Not a full runtime backup; archived checkpoints cannot be resumed directly after relocation.",
                           "Frozen source and stored logs support audit; they do not replace a fresh Lean recheck.",
                           "Original raw evidence remains byte-for-byte unchanged; absolute paths are historical provenance."]}
    write_json(OUT / "manifest.json", manifest)
    scan_paths = selected + [OUT / "build_transport.py", OUT / "README.md", OUT / "members.json", OUT / "manifest.json"]
    scan = sensitive_scan(scan_paths)
    write_json(OUT / "sensitive_scan.json", scan)
    if scan["status"] != "passed":
        raise RuntimeError("Sensitive scan needs review; only file paths/rules are in sensitive_scan.json")
    make_archive(ARCHIVE, selected)
    verified = verify_archive(rows)
    with tempfile.TemporaryDirectory(prefix="determinism-", dir=OUT) as temporary:
        again = Path(temporary) / "second.tar.xz"
        make_archive(again, selected)
        assert digest(again.read_bytes()) == digest(ARCHIVE.read_bytes())
    # Recheck sources after both reads to catch concurrent mutation.
    assert rows == [record(p) for p in selected]
    verification = {"status": "passed", "archive": ARCHIVE.name,
                    "archive_bytes": ARCHIVE.stat().st_size, "archive_sha256": digest(ARCHIVE.read_bytes()),
                    "verified_extracted_files": verified, "safe_member_paths": True,
                    "per_member_sha256_and_size_match": True, "second_build_byte_identical": True,
                    "original_selected_files_unchanged_during_packaging": True,
                    "original_gzip_member_inventory_identical": True,
                    "sensitive_scan_status": scan["status"], "unresolved_internal_artifact_references": 0}
    write_json(OUT / "verification.json", verification)
    outputs = sorted([ARCHIVE, OUT / "build_transport.py", OUT / "README.md", OUT / "members.json",
                      OUT / "manifest.json", OUT / "sensitive_scan.json", OUT / "verification.json"])
    (OUT / "SHA256SUMS").write_text("".join(f"{digest(p.read_bytes())}  {p.name}\n" for p in outputs))
    print(json.dumps({**verification, "payload_bytes": manifest["payload_bytes"],
                      "omitted_binary_files": len(omitted), "reference_dispositions": dict(counts)}, ensure_ascii=False))


def finalize_publication():
    """Publish the compressed manifest; keep the original JSON only for local auditing."""
    publication_files = [
        "README.md", ARCHIVE.name, "build_transport.py", "manifest.json", "members.json.xz",
        "sensitive_scan.json", "verification.json", "SHA256SUMS",
    ]
    manifest_path = OUT / "manifest.json"
    manifest = json.loads(manifest_path.read_text())
    manifest["publication_files"] = publication_files
    manifest["local_only_files"] = ["members.json"]
    manifest["compressed_member_inventory"] = {
        "publication_path": "members.json.xz", "decompressed_name": "members.json",
        "compression": "xz preset 9, 64 MiB dictionary, CRC64",
    }
    write_json(manifest_path, manifest)
    raw_members = (OUT / "members.json").read_bytes()
    compressed = lzma.compress(raw_members, format=lzma.FORMAT_XZ, check=lzma.CHECK_CRC64, preset=9)
    assert compressed == lzma.compress(raw_members, format=lzma.FORMAT_XZ, check=lzma.CHECK_CRC64, preset=9)
    assert lzma.decompress(compressed) == raw_members
    (OUT / "members.json.xz").write_bytes(compressed)
    rows = json.loads(raw_members)["files"]
    assert digest(json.dumps(rows, sort_keys=True, separators=(",", ":")).encode()) == ORIGINAL_GZIP_INVENTORY_SHA256
    verification_path = OUT / "verification.json"
    verification = json.loads(verification_path.read_text())
    assert verification["status"] == "passed"
    assert verification["archive_sha256"] == digest(ARCHIVE.read_bytes())
    assert verify_archive(rows) == len(rows)
    verification["compressed_member_inventory"] = {
        "compressed_file": "members.json.xz", "compressed_bytes": len(compressed),
        "compressed_sha256": digest(compressed), "decompressed_bytes": len(raw_members),
        "decompressed_sha256": digest(raw_members), "decompression_matches_original_json": True,
        "second_compression_byte_identical": True,
    }
    verification["publication_files"] = publication_files
    write_json(verification_path, verification)
    selected = [ROOT / row["path"] for row in rows]
    scan_paths = selected + [OUT / "build_transport.py", OUT / "README.md", OUT / "members.json",
                             manifest_path, verification_path]
    scan = sensitive_scan(scan_paths)
    scan["compressed_member_inventory_scanned_as_plaintext"] = True
    write_json(OUT / "sensitive_scan.json", scan)
    assert scan["status"] == "passed", "Sensitive scan needs review; paths only in sensitive_scan.json"
    outputs = sorted(OUT / name for name in publication_files if name != "SHA256SUMS")
    (OUT / "SHA256SUMS").write_text("".join(f"{digest(p.read_bytes())}  {p.name}\n" for p in outputs))
    print(json.dumps({"status": "passed", "publication_files": publication_files,
                      "publication_bytes": sum((OUT / name).stat().st_size for name in publication_files),
                      "archive_bytes": ARCHIVE.stat().st_size, "archive_sha256": digest(ARCHIVE.read_bytes()),
                      "member_inventory": verification["compressed_member_inventory"]}, ensure_ascii=False))


if __name__ == "__main__":
    if sys.argv[1:] != ["--finalize-publication-only"]:
        main()
    finalize_publication()
