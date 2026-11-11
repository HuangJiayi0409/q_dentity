"""Explicit offline boundaries: no internal model calls and no populated library."""
from __future__ import annotations

import time

from .cas_adapter import adapter_result
from .process import prepare_attempt, validate_seconds, write_json


class LLMAdapter:
    def execute(self, request: dict, attempt_dir, seconds: float) -> dict:
        started = time.monotonic()
        try:
            validate_seconds(seconds)
            attempt = prepare_attempt(attempt_dir)
            write_json(attempt / "llm_request.json", request, attempt)
            return adapter_result(started, "environment_blocked", "adapter_disabled",
                                  "本轮未启用内部 LLM 接口；需外部主控明确提交候选。", attempt=attempt)
        except (OSError, TypeError, ValueError) as exc:
            return adapter_result(started, "integrity_error", "artifact_integrity", str(exc))


class EmptyLibrary:
    """Deliberately contains no objects, rules, retrieved facts or proof evidence."""
    def lookup(self, symbol, purpose=None) -> dict:
        return {"schema_version": 1, "status": "unknown", "symbol": symbol,
                "purpose": purpose, "rules": [], "objects": [],
                "diagnostics": [{"code": "library_disabled", "message": "本轮 Library 为空。"}]}
