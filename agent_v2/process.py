"""Bounded subprocess execution with an isolated Linux descendant supervisor.

The supervisor is a subreaper: a backend's ``setsid`` does not escape cleanup.
It owns only this invocation's descendants, never unrelated application children.
Commands are argv arrays and never pass through a shell. This is lifecycle and
artifact protection, not a sandbox for executing untrusted arbitrary programs.
"""
from __future__ import annotations

import ctypes
import hashlib
import json
import math
import os
from pathlib import Path
import signal
import subprocess
import sys
import time
from typing import Any


def validate_seconds(seconds: float) -> float:
    if isinstance(seconds, bool) or not isinstance(seconds, (int, float)):
        raise ValueError("seconds must be a finite positive number")
    if not math.isfinite(seconds) or seconds <= 0:
        raise ValueError("seconds must be a finite positive number")
    return float(seconds)


def guard_artifact(path: Path, root: Path | None = None) -> Path:
    path = Path(path)
    if ".." in path.parts or any(p.casefold() == "test" for p in path.parts):
        raise ValueError("artifact traversal or frozen split path refused")
    path = path.absolute()
    if root is not None:
        root = guard_artifact(root)
        if not path.is_relative_to(root):
            raise ValueError("artifact is outside this attempt directory")
    for ancestor in [*reversed(path.parents), path]:
        if ancestor.is_symlink():
            raise ValueError("symbolic links are not allowed in artifact paths")
    return path


def prepare_attempt(path: Path) -> Path:
    path = guard_artifact(path)
    path.mkdir(parents=True, exist_ok=True)
    if not path.is_dir():
        raise ValueError("attempt path is not a directory")
    return guard_artifact(path)


def write_json(path: Path, value: Any, root: Path) -> None:
    """Create a new evidence file; never replace evidence from a prior action."""
    path = guard_artifact(path, root)
    data = (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2,
                       allow_nan=False) + "\n").encode("utf-8")
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    with os.fdopen(descriptor, "wb") as stream:
        stream.write(data)


def sha256_file(path: Path) -> str:
    path = guard_artifact(path)
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def collect_artifacts(root: Path) -> list[dict[str, str]]:
    root = guard_artifact(root)
    artifacts = []
    # Adapter output is flat; refusing nested directories avoids accidental
    # inclusion of unrelated inputs and avoids following directory links.
    for path in sorted(root.iterdir()):
        path = guard_artifact(path, root)
        if path.is_file():
            artifacts.append({"path": str(path), "sha256": sha256_file(path)})
    return artifacts


def _process_table() -> dict[int, tuple[int, str]]:
    table = {}
    for item in Path("/proc").iterdir():
        if not item.name.isdecimal():
            continue
        try:
            # The command name may contain spaces and parentheses.
            fields = (item / "stat").read_text().rsplit(")", 1)[1].split()
            table[int(item.name)] = (int(fields[1]), fields[19])
        except (FileNotFoundError, ProcessLookupError, PermissionError, ValueError, IndexError):
            pass
    return table


def _descendants(owner: int) -> dict[int, str]:
    table = _process_table()
    parents = {owner}
    selected = {}
    while True:
        added = {pid: born for pid, (parent, born) in table.items()
                 if parent in parents and pid not in parents}
        if not added:
            return selected
        selected.update(added)
        parents.update(added)


def _signal_owned(processes: dict[int, str], sig: int) -> None:
    current = _process_table()
    for pid, born in processes.items():
        if pid in current and current[pid][1] == born:
            try:
                os.kill(pid, sig)
            except ProcessLookupError:
                pass


def _reap_adopted() -> None:
    while True:
        try:
            pid, _ = os.waitpid(-1, os.WNOHANG)
        except ChildProcessError:
            return
        if not pid:
            return


def _cleanup(owner: int, process: subprocess.Popen | None = None) -> list[int]:
    started = time.monotonic()
    while time.monotonic() - started < 1.5:
        owned = _descendants(owner)
        if not owned:
            return []
        elapsed = time.monotonic() - started
        _signal_owned(owned, signal.SIGTERM if elapsed < 0.2 else signal.SIGKILL)
        if process is not None:
            # Preserve the direct child's actual code before waitpid(-1).
            process.poll()
            if process.returncode is not None:
                _reap_adopted()
        else:
            _reap_adopted()
        time.sleep(0.01)
    return sorted(_descendants(owner))


def _supervise(request_path: Path) -> int:
    request = json.loads(request_path.read_text(encoding="utf-8"))
    root = guard_artifact(request_path.parent)
    report_path = guard_artifact(Path(request["report_path"]), root)
    report = {"returncode": None, "timed_out": False, "environment_error": None,
              "cleanup_survivors": []}
    process = None
    interrupted = []
    def stop(signum, _frame):
        interrupted.append(signum)
    signal.signal(signal.SIGTERM, stop)
    signal.signal(signal.SIGINT, stop)
    try:
        if not sys.platform.startswith("linux"):
            raise RuntimeError("descendant supervision requires Linux")
        libc = ctypes.CDLL(None, use_errno=True)
        if libc.prctl(36, 1, 0, 0, 0) != 0:  # PR_SET_CHILD_SUBREAPER
            raise OSError(ctypes.get_errno(), "cannot enable isolated child subreaper")
        out = guard_artifact(Path(request["stdout_path"]), root)
        err = guard_artifact(Path(request["stderr_path"]), root)
        out_fd = os.open(out, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
        with os.fdopen(out_fd, "wb") as stdout:
            err_fd = os.open(err, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
            with os.fdopen(err_fd, "wb") as stderr:
                process = subprocess.Popen(request["command"], cwd=request["cwd"],
                                           stdout=stdout, stderr=stderr, stdin=subprocess.DEVNULL,
                                           start_new_session=True, shell=False)
                while process.poll() is None:
                    if time.monotonic() >= request["deadline"] or interrupted:
                        report["timed_out"] = True
                        break
                    time.sleep(0.01)
    except Exception as exc:
        report["environment_error"] = type(exc).__name__ + ": " + str(exc)
    finally:
        report["cleanup_survivors"] = _cleanup(os.getpid(), process)
        if process is not None:
            report["returncode"] = process.poll()
        write_json(report_path, report, root)
    return 0


def run_process(command, cwd, seconds, stdout_path, stderr_path) -> dict:
    """Run one argv command, preserving complete logs and actual process status.

    Log paths must belong to the same attempt directory and be fresh. The caller
    owns that directory and supplies trusted executables; no shell is involved.
    """
    started = time.monotonic()
    seconds = validate_seconds(seconds)
    if (not isinstance(command, (list, tuple)) or not command or
            any(not isinstance(part, str) or not part or "\0" in part for part in command)):
        raise ValueError("command must be a nonempty argv sequence of strings")
    cwd = guard_artifact(Path(cwd))
    if not cwd.is_dir():
        raise ValueError("cwd must be an existing directory")
    out = guard_artifact(Path(stdout_path))
    err = guard_artifact(Path(stderr_path))
    if out.parent != err.parent or out == err:
        raise ValueError("stdout and stderr must be distinct files in one attempt directory")
    root = prepare_attempt(out.parent)
    request_path = root / (out.name + ".process_request.json")
    report_path = root / (out.name + ".process_result.json")
    for path in (out, err, request_path, report_path):
        guard_artifact(path, root)
        if path.exists():
            raise ValueError("refusing to overwrite process evidence: " + str(path))
    request = {"command": list(command), "cwd": str(cwd), "deadline": started + seconds,
               "stdout_path": str(out), "stderr_path": str(err), "report_path": str(report_path)}
    write_json(request_path, request, root)
    supervisor = None
    report = {"returncode": None, "timed_out": False, "environment_error": None,
              "cleanup_survivors": []}
    try:
        supervisor = subprocess.Popen([sys.executable, "-B", str(Path(__file__).absolute()),
                                       "--supervisor", str(request_path)],
                                      stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                                      stderr=subprocess.DEVNULL, start_new_session=True, shell=False)
        try:
            supervisor.wait(timeout=max(0.01, seconds + 2.5 - (time.monotonic() - started)))
        except subprocess.TimeoutExpired:
            supervisor.terminate()  # Its signal handler still performs descendant cleanup.
            try:
                supervisor.wait(timeout=2)
            except subprocess.TimeoutExpired:
                report["cleanup_survivors"] = _cleanup(supervisor.pid)
                supervisor.kill()
                supervisor.wait()
            report["timed_out"] = True
            report["environment_error"] = "supervisor deadline exceeded"
        if report_path.is_file():
            guard_artifact(report_path, root)
            report.update(json.loads(report_path.read_text(encoding="utf-8")))
        elif report["environment_error"] is None:
            report["environment_error"] = "supervisor exited without a result"
    except OSError as exc:
        report["environment_error"] = type(exc).__name__ + ": " + str(exc)
    report.update({"wall_seconds": time.monotonic() - started,
                   "stdout_path": str(out), "stderr_path": str(err),
                   "request_path": str(request_path), "report_path": str(report_path)})
    return report


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] != "--supervisor":
        raise SystemExit("this module is only executable as an internal process supervisor")
    raise SystemExit(_supervise(Path(sys.argv[2])))
