"""Adapter contracts. Fixtures are synthetic; no benchmark split is read."""
import hashlib
import importlib
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch


class AdapterTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="agent-v2-adapters-")
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def module(self, name):
        full = "agent_v2." + name
        self.assertIsNotNone(importlib.util.find_spec(full), full + " must exist")
        return importlib.import_module(full)

    def assert_no_process(self, pid):
        self.assertFalse(Path(f"/proc/{pid}").exists(), f"descendant {pid} was not reaped")

    def test_process_captures_real_exit_code_and_both_streams(self):
        process = self.module("process")
        out, err = self.root / "stdout.txt", self.root / "stderr.txt"
        result = process.run_process(
            [sys.executable, "-c", "import sys; print('out'); print('err', file=sys.stderr); sys.exit(7)"],
            self.root, 3.0, out, err,
        )
        self.assertEqual(result["returncode"], 7)
        self.assertFalse(result["timed_out"])
        self.assertEqual(out.read_text(), "out\n")
        self.assertEqual(err.read_text(), "err\n")
        self.assertEqual(result["cleanup_survivors"], [])

    def test_timeout_cleans_a_child_that_started_a_new_session(self):
        process = self.module("process")
        pid_file = self.root / "child.pid"
        program = (
            "import subprocess,sys,time,pathlib; "
            "p=subprocess.Popen([sys.executable,'-c','import time; time.sleep(30)'],start_new_session=True); "
            f"pathlib.Path({str(pid_file)!r}).write_text(str(p.pid)); time.sleep(30)"
        )
        result = process.run_process([sys.executable, "-c", program], self.root, 0.8,
                                     self.root / "stdout.txt", self.root / "stderr.txt")
        self.assertTrue(result["timed_out"])
        self.assertLess(result["wall_seconds"], 4)
        self.assertTrue(pid_file.is_file(), "fixture must actually create a descendant")
        self.assert_no_process(int(pid_file.read_text()))
        self.assertEqual(result["cleanup_survivors"], [])

    def test_normal_parent_exit_does_not_leave_a_detached_child(self):
        process = self.module("process")
        pid_file = self.root / "child.pid"
        program = (
            "import subprocess,sys,pathlib; "
            "p=subprocess.Popen([sys.executable,'-c','import time; time.sleep(30)'],start_new_session=True); "
            f"pathlib.Path({str(pid_file)!r}).write_text(str(p.pid))"
        )
        result = process.run_process([sys.executable, "-c", program], self.root, 3.0,
                                     self.root / "stdout.txt", self.root / "stderr.txt")
        self.assertEqual(result["returncode"], 0)
        self.assertFalse(result["timed_out"])
        self.assert_no_process(int(pid_file.read_text()))

    def test_process_passes_shell_metacharacters_as_literal_arguments(self):
        process = self.module("process")
        sentinel = self.root / "must-not-exist"
        value = "$(touch " + str(sentinel) + ")"
        result = process.run_process([sys.executable, "-c", "import sys;print(sys.argv[1])", value],
                                     self.root, 3.0, self.root / "stdout.txt", self.root / "stderr.txt")
        self.assertEqual(result["returncode"], 0)
        self.assertEqual((self.root / "stdout.txt").read_text().strip(), value)
        self.assertFalse(sentinel.exists())

    def test_process_rejects_symlink_output_without_touching_target(self):
        process = self.module("process")
        outside = self.root / "outside.txt"
        outside.write_text("preserve")
        link = self.root / "stdout.txt"
        link.symlink_to(outside)
        with self.assertRaises(ValueError):
            process.run_process([sys.executable, "-c", "print('bad')"], self.root, 3.0,
                                link, self.root / "stderr.txt")
        self.assertEqual(outside.read_text(), "preserve")

    def test_process_rejects_cross_directory_logs_and_invalid_timeouts(self):
        process = self.module("process")
        other = self.root / "other"
        other.mkdir()
        with self.assertRaises(ValueError):
            process.run_process([sys.executable, "-c", "pass"], self.root, 3.0,
                                self.root / "stdout.txt", other / "stderr.txt")
        for bad in [True, 0, -1, float("nan"), float("inf")]:
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                process.run_process([sys.executable, "-c", "pass"], self.root, bad,
                                    self.root / "stdout.txt", self.root / "stderr.txt")

    def test_core_rejects_invalid_contract_without_running_backend(self):
        adapters = self.module("cas_adapter")
        with patch.object(adapters, "run_process", side_effect=AssertionError("must not invoke core")):
            result = adapters.CoreAdapter().execute(
                {"schema_version": True, "solver": "q_gosper", "input": {"k_shift": "q"}},
                self.root / "attempt", 3.0,
            )
        self.assertEqual(result["sigma"]["code"], "input_mismatch")
        self.assertEqual(result["C_partial"], [])
        self.assertEqual(result["O_res"], [])
        self.assertFalse(result["original_identity_proved"])

    def test_real_independent_core_construction_remains_unverified(self):
        adapters = self.module("cas_adapter")
        # Independent geometric ratio, not the requested final core_qgosper demo.
        request = {"schema_version": 1, "solver": "q_gosper", "input": {"k_shift": "q"}}
        result = adapters.CoreAdapter().execute(request, self.root / "attempt", 8.0)
        self.assertEqual(result["status"], "symbolic_constructed", result)
        self.assertEqual(result["raw_result"]["status"], "constructed")
        self.assertEqual(result["sigma"]["code"], "translation_pending")
        self.assertEqual(result["C_partial"], [])
        self.assertEqual(result["O_res"], [])
        self.assertFalse(result["original_identity_proved"])
        for artifact in result["artifacts"]:
            path = Path(artifact["path"])
            self.assertTrue(path.is_relative_to(self.root / "attempt"))
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), artifact["sha256"])
        raw_path = self.root / "attempt" / "core_result.json"
        self.assertEqual(json.loads(raw_path.read_text()), result["raw_result"])

    def fake_core(self, request, **overrides):
        raw = {"schema_version": 1, "status": "constructed", "solver": "q_gosper",
               "request_sha256": hashlib.sha256(json.dumps(request, sort_keys=True, ensure_ascii=False).encode()).hexdigest(),
               "original_identity_proved": False, "result": {"certificate": "0"}}
        raw.update(overrides)
        if raw.get("solver") is None:
            raw.pop("solver", None)
        def invoke(command, cwd, seconds, stdout_path, stderr_path):
            Path(command[command.index("--output") + 1]).write_text(json.dumps(raw))
            Path(stdout_path).write_text("fixture\n")
            Path(stderr_path).write_text("")
            return {"returncode": 0, "timed_out": False, "wall_seconds": 0.01,
                    "environment_error": None, "cleanup_survivors": []}
        return invoke

    def test_core_rejects_forged_original_proof_claim_and_request_hash(self):
        adapters = self.module("cas_adapter")
        request = {"schema_version": 1, "solver": "q_gosper", "input": {"k_shift": "q"}}
        for name, override in [("proof", {"original_identity_proved": True}),
                               ("hash", {"request_sha256": "0" * 64}),
                               ("solver", {"solver": "q_zeilberger"}),
                               ("version", {"schema_version": True}),
                               ("certificate", {"result": None})]:
            with self.subTest(name=name), patch.object(adapters, "run_process", self.fake_core(request, **override)):
                result = adapters.CoreAdapter().execute(request, self.root / name, 3.0)
            self.assertEqual(result["status"], "integrity_error")
            self.assertFalse(result["original_identity_proved"])
            self.assertEqual(result["C_partial"], [])

    def test_core_timeout_and_missing_environment_are_not_mathematical_failure(self):
        adapters = self.module("cas_adapter")
        request = {"schema_version": 1, "solver": "q_gosper", "input": {"k_shift": "q"}}
        timed = {"returncode": -15, "timed_out": True, "wall_seconds": 0.1,
                 "environment_error": None, "cleanup_survivors": []}
        with patch.object(adapters, "run_process", return_value=timed):
            result = adapters.CoreAdapter().execute(request, self.root / "timed", 3.0)
        self.assertEqual(result["status"], "budget_exhausted")
        self.assertEqual(result["sigma"]["code"], "timeout")
        with patch.object(adapters, "CORE_ENTRY", self.root / "missing.py"):
            result = adapters.CoreAdapter().execute(request, self.root / "missing", 3.0)
        self.assertEqual(result["status"], "environment_blocked")
        self.assertFalse(result["original_identity_proved"])

    def test_core_failure_without_solver_echo_keeps_backend_failure_class(self):
        adapters = self.module("cas_adapter")
        request = {"schema_version": 1, "solver": "q_gosper", "input": {"k_shift": "q"}}
        cases = [("unsupported_domain", "incomplete", "input_mismatch"),
                 ("resource_exhausted", "budget_exhausted", "resource_exhausted"),
                 ("implementation_error", "environment_blocked", "implementation_error")]
        for status, expected, code in cases:
            with self.subTest(status=status):
                with patch.object(adapters, "run_process", self.fake_core(request, status=status, solver=None)):
                    result = adapters.CoreAdapter().execute(request, self.root / status, 3.0)
                self.assertEqual(result["status"], expected)
                self.assertEqual(result["sigma"]["code"], code)
                self.assertEqual(result["sigma"]["backend_status"], status)
                self.assertFalse(result["original_identity_proved"])

    def test_adapter_rejects_symlink_attempt_directory(self):
        adapters = self.module("cas_adapter")
        target = self.root / "outside"
        target.mkdir()
        link = self.root / "attempt"
        link.symlink_to(target, target_is_directory=True)
        result = adapters.CoreAdapter().execute(
            {"schema_version": 1, "solver": "q_gosper", "input": {"k_shift": "q"}}, link, 3.0)
        self.assertEqual(result["status"], "integrity_error")
        self.assertEqual(list(target.iterdir()), [])

    def test_unavailable_original_frontend_does_not_invoke_retired_flows(self):
        adapters = self.module("cas_adapter")
        with patch.object(adapters, "run_process", side_effect=AssertionError("retired flow invoked")):
            result = adapters.MethodAdapter().execute("SYNTHETIC", "telescoping", {}, self.root / "attempt", 3.0)
        self.assertEqual(result["status"], "environment_blocked")
        self.assertEqual(result["sigma"]["code"], "formal_frontend_unavailable")
        self.assertFalse(result["original_identity_proved"])
        self.assertEqual(result["C_partial"], [])
        self.assertEqual(result["O_res"], [])

    def test_disabled_llm_and_empty_library_never_invent_evidence(self):
        llm = self.module("llm_adapter")
        result = llm.LLMAdapter().execute({"goal": "synthetic"}, self.root / "attempt", 3.0)
        self.assertEqual(result["sigma"]["code"], "adapter_disabled")
        self.assertEqual(result["C_partial"], [])
        self.assertFalse(result["original_identity_proved"])
        found = llm.EmptyLibrary().lookup("poch", "length_shift")
        self.assertEqual(found["status"], "unknown")
        self.assertEqual(found["rules"], [])


if __name__ == "__main__":
    unittest.main()
