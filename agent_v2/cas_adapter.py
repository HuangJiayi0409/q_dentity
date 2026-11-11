"""New adapters over the independent symbolic core; no retired agent imports."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import sys
import time

from .process import (collect_artifacts, guard_artifact, prepare_attempt,
                      run_process, validate_seconds, write_json)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CORE_ENTRY = PROJECT_ROOT / "finite_product_framework" / "solve_core.py"
SUPPORTED_CORE_SOLVERS = frozenset({"q_gosper", "q_zeilberger", "parameterized_q_gosper"})


def adapter_result(started, status, code, message, *, stage="adapter", backend_status=None,
                   raw_result=None, diagnostics=None, attempt=None):
    artifacts = []
    if attempt is not None:
        artifacts = collect_artifacts(attempt)
    return {"schema_version": 1, "status": status, "C_partial": [], "O_res": [],
            "sigma": {"stage": stage, "code": code, "message": message,
                      "backend_status": backend_status},
            "cost": {"wall_seconds": time.monotonic() - started, "actions": 1},
            "raw_result": raw_result if raw_result is not None else {},
            "artifacts": artifacts, "diagnostics": diagnostics or [],
            "original_identity_proved": False}


def _tree(value, summand=False, depth=0, count=None):
    if count is None:
        count = [0]
    count[0] += 1
    if depth > 64 or count[0] > 10000:
        raise ValueError("symbolic input exceeds structural limits")
    if type(value) is int:
        return
    if isinstance(value, str):
        pattern = r"[a-z][a-z0-9_]*" if summand else r"[A-Za-z][A-Za-z0-9_]*"
        if not re.fullmatch(pattern, value) or (not summand and value in {"n", "k"}):
            raise ValueError("invalid symbolic atom; rational shifts use Q and X")
        return
    if not isinstance(value, list) or not value or not isinstance(value[0], str):
        raise ValueError("symbolic expressions must be typed arrays, integers or symbols")
    op, args = value[0], value[1:]
    arities = {"sub": 2, "div": 2, "pow": 2}
    arities.update({"poch": 3, "fall": 4, "gaussian": 3} if summand else {"neg": 1})
    if op in {"add", "mul"}:
        if not args:
            raise ValueError("add and mul require arguments")
    elif op not in arities or len(args) != arities[op]:
        raise ValueError("unsupported operator or wrong arity: " + op)
    if not summand and op == "pow" and type(args[1]) is not int:
        raise ValueError("rational powers require a literal integer exponent")
    for arg in args:
        _tree(arg, summand, depth + 1, count)


def validate_request(request):
    if not isinstance(request, dict) or set(request) != {"schema_version", "solver", "input"}:
        raise ValueError("core request requires exactly schema_version, solver and input")
    if type(request["schema_version"]) is not int or request["schema_version"] != 1:
        raise ValueError("schema_version must be integer 1")
    solver, data = request["solver"], request["input"]
    if not isinstance(solver, str) or solver not in SUPPORTED_CORE_SOLVERS:
        raise ValueError("this MVP supports q_gosper, q_zeilberger and parameterized_q_gosper")
    if not isinstance(data, dict):
        raise ValueError("input must be an object")
    keys = set(data)
    if solver in {"q_gosper", "q_zeilberger"} and keys == {"summand"}:
        _tree(data["summand"], summand=True)
        return
    expected = {"k_shift"}
    if solver == "q_zeilberger":
        expected.add("n_shift")
    elif solver == "parameterized_q_gosper":
        expected.add("rhs_basis")
    if keys != expected:
        raise ValueError("input fields do not match the selected independent solver")
    for key, value in data.items():
        if key == "rhs_basis":
            if not isinstance(value, list) or not value:
                raise ValueError("rhs_basis must be a nonempty expression list")
            for tree in value:
                _tree(tree)
        else:
            _tree(value)


class CoreAdapter:
    """Run a local symbolic construction without treating it as a Lean proof."""

    def execute(self, request: dict, attempt_dir: Path, seconds: float) -> dict:
        started = time.monotonic()
        attempt = None
        raw = {}
        try:
            attempt = prepare_attempt(attempt_dir)
            # A fresh directory prevents stale results from being accepted.
            if any(attempt.iterdir()):
                raise ValueError("core attempt directory must be empty")
            try:
                validate_seconds(seconds)
                validate_request(request)
            except (ValueError, TypeError) as exc:
                write_json(attempt / "rejection.json", {"code": "input_mismatch", "message": str(exc)}, attempt)
                return adapter_result(started, "incomplete", "input_mismatch", str(exc), attempt=attempt)
            write_json(attempt / "core_request.json", request, attempt)
            if not CORE_ENTRY.is_file():
                return adapter_result(started, "environment_blocked", "core_unavailable",
                                      "独立符号计算入口不存在。", attempt=attempt)
            remaining = seconds - (time.monotonic() - started)
            if remaining <= 0:
                return adapter_result(started, "budget_exhausted", "timeout", "动作预算已耗尽。", attempt=attempt)
            output = guard_artifact(attempt / "core_result.json", attempt)
            command = [sys.executable, "-B", str(CORE_ENTRY), "--input", str(attempt / "core_request.json"),
                       "--output", str(output), "--seconds", str(remaining),
                       "--max-unknowns", "10000", "--max-normal-form-degree", "10000",
                       "--max-states", "128"]
            process = run_process(command, PROJECT_ROOT, remaining,
                                  attempt / "stdout.txt", attempt / "stderr.txt")
            write_json(attempt / "process.json", process, attempt)
            if process.get("cleanup_survivors"):
                return adapter_result(started, "environment_blocked", "cleanup_failed",
                                      "后端进程清理未完成。", diagnostics=[process], attempt=attempt)
            if output.exists():
                guard_artifact(output, attempt)
                try:
                    raw = json.loads(output.read_text(encoding="utf-8"))
                except (ValueError, UnicodeError) as exc:
                    return adapter_result(started, "integrity_error", "malformed_core_output", str(exc), attempt=attempt)
                expected_hash = hashlib.sha256(json.dumps(request, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
                if (not isinstance(raw, dict) or type(raw.get("schema_version")) is not int or
                        raw.get("schema_version") != 1 or raw.get("request_sha256") != expected_hash or
                        ("solver" in raw and raw["solver"] != request["solver"]) or
                        (raw.get("status") == "constructed" and raw.get("solver") != request["solver"]) or
                        (raw.get("status") == "constructed" and not isinstance(raw.get("result"), dict)) or
                        raw.get("original_identity_proved") is not False):
                    return adapter_result(started, "integrity_error", "core_output_mismatch",
                                          "后端输出版本、请求哈希或原题状态不符合局部核心契约。",
                                          raw_result=raw if isinstance(raw, dict) else {"invalid_output": raw}, attempt=attempt)
            if process.get("timed_out"):
                return adapter_result(started, "budget_exhausted", "timeout", "局部计算达到墙钟预算。",
                                      raw_result=raw, diagnostics=[process], attempt=attempt)
            if process.get("environment_error"):
                return adapter_result(started, "environment_blocked", "process_error",
                                      str(process["environment_error"]), raw_result=raw, diagnostics=[process], attempt=attempt)
            if not raw:
                return adapter_result(started, "environment_blocked", "core_output_missing",
                                      "独立核心未返回结构化结果；原始 stdout/stderr 已保留。",
                                      diagnostics=[process], attempt=attempt)
            status = raw.get("status")
            if status == "constructed":
                if process.get("returncode") != 0:
                    return adapter_result(started, "integrity_error", "core_exit_mismatch",
                                          "后端声称构造成功但进程异常退出。", raw_result=raw, attempt=attempt)
                message = "已生成局部符号候选；尚无 Lean 转译与验证，不能计入已验证证书。"
                return adapter_result(started, "symbolic_constructed", "translation_pending", message,
                                      stage="translation", backend_status=status, raw_result=raw,
                                      diagnostics=[{"code": "translation_pending", "message": message,
                                                    "formal_obligations_exported": False}], attempt=attempt)
            if status == "resource_exhausted":
                code = "timeout" if "wall-clock" in str(raw.get("reason", "")) else "resource_exhausted"
                mapped = "budget_exhausted"
            elif status in {"implementation_error", "worker_failed"}:
                code, mapped = status, "environment_blocked"
            elif status in {"invalid_input", "unsupported_input", "unsupported_domain"}:
                code, mapped = "input_mismatch", "incomplete"
            elif status in {"no_solution_in_class", "no_relation_in_declared_basis", "search_exhausted"}:
                code, mapped = "search_exhausted", "incomplete"
            else:
                code, mapped = "unknown_core_status", "integrity_error"
            return adapter_result(started, mapped, code,
                                  str(raw.get("reason") or raw.get("message") or status), stage="symbolic_core",
                                  backend_status=status, raw_result=raw, attempt=attempt)
        except (OSError, ValueError, TypeError) as exc:
            # Do not hash or follow any rejected path while reporting rejection.
            return adapter_result(started, "integrity_error", "artifact_integrity", str(exc), raw_result=raw)


class TelescopingAdapter:
    """One bounded Train method: frontend -> real core -> unverified local term.

    Only the controller's independent Lean checker may turn these candidates
    into certificates or apply their proposed conditional proof connections.
    """

    def execute_action(self, state, action, attempt_dir, seconds):
        """Construct exactly one local step, with an explicit input contract."""
        task = action.theta.get('task')
        if action.theta.get('method') != 'telescoping' or action.theta.get('scope') != 'full':
            raise ValueError('unregistered method task contract')
        if task == 'local':
            outcome = self.execute(state.G.identity, 'telescoping', state.G.to_dict(), attempt_dir, seconds)
            outcome['raw_result']['execution_scope'] = 'certificate_chain'
            outcome['raw_result'].pop('remaining_work', None)
            return outcome
        started = time.monotonic()
        attempt = prepare_attempt(attempt_dir)
        if any(attempt.iterdir()):
            raise ValueError('method attempt directory must be empty')
        validate_seconds(seconds)
        from .formal_frontend import analyze_source
        from .storage import verify_source
        from .telescoping_closure import make_closure_candidate, closure_blueprint
        run_root = Path(state.G.snapshot_path).parent.parent
        verify_source(state.G, run_root)
        frontend = analyze_source(state.G.to_dict(), run_root=run_root)
        write_json(attempt / 'method_request.json', {
            'method': 'telescoping', 'task': task, 'source': state.G.to_dict(),
            'seconds': seconds, 'action_id': action.id,
            'approved_certificates': [c.id for c in state.C],
            'open_obligations': [o.to_dict() for o in state.O]}, attempt)
        write_json(attempt / 'frontend.json', frontend, attempt)
        if frontend['status'] != 'applicable':
            return adapter_result(started, 'incomplete', 'not_applicable',
                'The frozen original is outside the finite-sum closure contract.',
                raw_result={'execution_scope': 'certificate_chain'}, attempt=attempt)
        plan = closure_blueprint(frontend)
        write_json(attempt / 'task_contract.json', plan, attempt)
        candidate = make_closure_candidate(frontend, task,
            {c.id: c.to_dict() for c in state.C}, action.id)
        if candidate.closes not in {o.id for o in state.O}:
            raise ValueError('task has no matching open formal obligation')
        write_json(attempt / 'candidate.json', candidate.to_dict(), attempt)
        verify_source(state.G, run_root)
        outcome = adapter_result(started, 'symbolic_constructed', 'closure_candidate_ready',
            'One conditional connection or endpoint candidate awaits independent Lean verification.',
            stage='translation', raw_result={'execution_scope': 'certificate_chain',
                'method': 'telescoping', 'task': task, 'cas_invoked': False,
                'dependency_ids': list(candidate.dependencies), 'frontend_profile': frontend['profile']},
            attempt=attempt)
        outcome['C_partial'] = [candidate.to_dict()]
        outcome['O_res'] = [o.to_dict() for o in candidate.replaces]
        return outcome

    def execute(self, identity, method, source, attempt_dir, seconds) -> dict:
        started = time.monotonic()
        try:
            validate_seconds(seconds)
            attempt = prepare_attempt(attempt_dir)
            if any(attempt.iterdir()):
                raise ValueError('method attempt directory must be empty')
            write_json(attempt / "method_request.json", {"identity": identity, "method": method,
                        "source": source, "seconds": seconds}, attempt)
            # Keep the existing explicit boundary for callers without a formal
            # Benchmark source (including the Init-only CLI unit fixtures).
            if not source:
                return adapter_result(started, 'environment_blocked', 'formal_frontend_unavailable',
                                      'A frozen Benchmark mathematical source is required.', attempt=attempt)
            from .models import Source
            from .storage import verify_source
            from .formal_frontend import analyze_source
            from .telescoping_translation import translate_candidate
            bound = Source.from_dict(source)
            if identity != bound.identity or method != 'telescoping':
                raise ValueError('method/identity does not match the frozen source')
            run_root = Path(bound.snapshot_path).parent.parent
            verify_source(bound, run_root)
            frontend = analyze_source(source, run_root=run_root)
            write_json(attempt / 'frontend.json', frontend, attempt)
            if frontend['status'] != 'applicable':
                if bound.declaration.lstrip().startswith('import Init\n'):
                    return adapter_result(started, 'environment_blocked', 'formal_frontend_unavailable',
                        'This CAS profile requires a supported Benchmark mathematical source.',
                        raw_result={'frontend': frontend}, attempt=attempt)
                return adapter_result(started, 'incomplete', 'not_applicable',
                    'The frozen theorem is outside the supported telescoping structural pattern.',
                    raw_result={'frontend': frontend}, attempt=attempt)
            request = frontend['core_request']
            write_json(attempt / 'mapping.json', frontend['mapping'], attempt)
            write_json(attempt / 'cas_request.json', request, attempt)
            remaining = seconds - (time.monotonic() - started)
            if remaining <= 0:
                return adapter_result(started, 'budget_exhausted', 'timeout',
                                      'Frontend exhausted the action budget.', attempt=attempt)
            core = CoreAdapter().execute(request, attempt / 'core', remaining)
            write_json(attempt / 'cas_return.json', core, attempt)
            verify_source(bound, run_root)
            raw = {'frontend_profile': frontend['profile'], 'core': core['raw_result']}
            if core['status'] != 'symbolic_constructed':
                return adapter_result(started, core['status'], core['sigma']['code'],
                    core['sigma']['message'], stage=core['sigma']['stage'],
                    backend_status=core['sigma'].get('backend_status'), raw_result=raw,
                    diagnostics=core.get('diagnostics', []), attempt=attempt)
            translation = translate_candidate(frontend, core['raw_result'])
            write_json(attempt / 'translation.json', translation, attempt)
            raw.update(translation=translation, execution_scope='local_certificate_only',
                remaining_work={
                    'formal_obligations_exported': False,
                    'open_obligation': 'original',
                    'explanation': [
                        '尚未提供将逐项差分等式提升到原有限范围求和的已验证连接。',
                        '尚未证明零端点以及末端点与原题左端的一致性。',
                        '尚未组装并独立验收未经修改的原命题。',
                    ]})
            if translation['status'] != 'candidate_ready':
                return adapter_result(started, 'symbolic_constructed', 'translation_pending',
                    'The symbolic result has no supported original-domain Lean translation.',
                    stage='translation', backend_status='constructed', raw_result=raw, attempt=attempt)
            candidate = translation['candidate']
            write_json(attempt / 'candidate.json', candidate, attempt)
            verify_source(bound, run_root)
            outcome = adapter_result(started, 'symbolic_constructed', 'local_candidate_ready',
                'A source-bound local difference candidate awaits independent Lean verification; the original remains open.',
                stage='translation', backend_status='constructed', raw_result=raw, attempt=attempt)
            outcome['C_partial'] = [candidate]
            return outcome
        except (OSError, ValueError, TypeError) as exc:
            return adapter_result(started, "integrity_error", "artifact_integrity", str(exc))


class MethodAdapter:
    """Dispatch only registered methods, preserving the strict result boundary."""

    def _dispatch(self, method, parameters):
        from .method_registry import builtin_registry
        spec = builtin_registry().get(method)
        spec.validate_parameters(parameters)
        return spec, None if spec.capability_level == 'L0' else spec.factory()()

    def validate_action(self, action):
        self._dispatch(action.theta.get('method'), action.theta)

    @staticmethod
    def _annotate(result, spec):
        from .executor import normalize_result
        from .models import ContractError
        result = normalize_result(result).to_dict()
        if spec.capability_level in ('L0', 'L2') and (result['C_partial'] or result['O_res']):
            raise ContractError('method without a Lean bridge cannot export formal candidates or residuals')
        result['raw_result'].update(method_id=spec.id, method_version=spec.version,
            capability_level=spec.capability_level,
            input_contract='see retained frontend.json and method_request.json')
        return normalize_result(result).to_dict()

    def execute(self, identity, method, source, attempt_dir, seconds):
        spec, adapter = self._dispatch(method, {'seconds': seconds})
        if adapter is None:
            return self._annotate(adapter_result(time.monotonic(), 'incomplete', 'capability_unavailable',
                'This method has a description only; no mathematical construction was executed.'), spec)
        return self._annotate(adapter.execute(identity, method, source, attempt_dir, seconds), spec)

    def execute_action(self, state, action, attempt_dir, seconds):
        spec, adapter = self._dispatch(action.theta.get('method'), action.theta)
        if adapter is None:
            return self._annotate(adapter_result(time.monotonic(), 'incomplete', 'capability_unavailable',
                'This method has no registered executable capability.'), spec)
        return self._annotate(adapter.execute_action(state, action, attempt_dir, seconds), spec)

    def execute_request(self, method, request, attempt_dir, seconds):
        from .models import ContractError
        spec, adapter = self._dispatch(method, {'seconds': seconds})
        if adapter is None or 'core_request' not in spec.accepted_kinds or not hasattr(adapter, 'execute_request'):
            raise ContractError('method has no executable core-request contract')
        return self._annotate(adapter.execute_request(request, attempt_dir, seconds), spec)
