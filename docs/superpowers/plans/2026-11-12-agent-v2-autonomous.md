# Agent v2 Autonomous Proof Loop Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Run a real Train theorem through CAS, generated local Lean proofs, residual-based selection, incremental representations and original-theorem verification.

**Architecture:** Preserve the existing ResidualState, Graph, proof links, checker transactions and manual CLI. Add an explicit autonomous mode with typed local tasks, a restricted generated-proof checker, real model clients, library lookup, capability-based multiple outlets, and bounded graph proposals. Models propose or rank; deterministic code binds targets, checks contracts, updates proof state and charges the shared budget.

**Tech Stack:** Python 3.10, existing exact CAS backends, fixed Lean 4 / Mathlib environment, configurable model HTTP clients and Jev.

**Spec:** User-approved seven-step roadmap in this conversation; architecture document `/home/hjy/.codex/attachments/099bae63-b79e-48a3-862b-8882df9e747f/Agent框架规划v2.docx`.

## Global Constraints

- Original theorem, original assumptions and source hash remain unchanged; only original Lean acceptance means success.
- No benchmark Test, historical proof borrowing, restored old Agent/controllers, or rewriting old evidence.
- Keep current manual single-method CLI and profile checks unchanged by default.
- Only Lean-verified candidates enter C; open leaves of checked proof links equal O.
- One selected action per round. Preserve checked work, bind all dependencies and retain actual requests, responses, diagnostics and costs.
- Network credentials are read only from explicit local configuration/environment and never written to logs, prompts or reports.
- There is no usable Git repository here (`git rev-parse` fails). Use `agent_v2/generated/autonomous_20261112/before`, hashes and diffs instead of worktrees/commits. No GitHub publication is implied by this implementation request.
- User has already authorized implementation of the roadmap; do not re-request plan approval. Independent tasks may be delegated concurrently with disjoint ownership.

## Review Focus

- Generated proof or proposition attempts command/import injection: accept only bounded terms/tactics inside a trusted Lean command; reject source mutations/new axioms.
- Same Source admits multiple methods: distinguish capability alternatives from ambiguity in statement meaning; never let candidate-selected profiles change the environment.
- A local certificate exists but cannot yet justify a parent replacement: preserve C and keep original O until the connection theorem is verified.
- Resume after model response or local acceptance: bind task/request/receipt hashes, avoid duplicate CAS/model actions and preserve precise stop categories.
- Model/Jev latency or failure: charge shared wall time/calls, preserve unavailable status and do not report a rules fallback as a real model decision.

### Task 1: Typed local proof tasks and generated-proof verification

**Files:** create `agent_v2/local_tasks.py`, `agent_v2/local_proof_checker.py`, `agent_v2/lean/LocalProofCheck.lean`, focused tests; minimally extend common mathematical transaction helpers if required without weakening existing profiles.

**Interfaces:** `LocalTask` binds id, Source hash, representation, exact closed proposition, target obligation, dependencies and replacement obligations. `make_task(state, representation_id, obligation_id, *, children=(), proposition=None, dependencies=())` creates a task from current state; `candidate_for(task, proof_term)` creates a bound Candidate. `LocalLeanChecker` accepts a fixed task registry in addition to existing CAS candidates, supports `register_task(task)`, replay and exact original assembly through the existing checker API.

- [x] Add failing tests for changed target/context/dependency, rejected command injection, invalid proof, valid closed proof and checked implication decomposition.
- [x] Implement typed immutable tasks, restricted generated proof parsing, fixed foundations and genuine Lean compilation/audit; integrate mixed CAS/generated dependencies without trusting receipts alone.
- [x] Run focused real Lean positive/negative, replay and original checks; self-review source/target/environment binding.

### Task 2: Real model, Jev and library adapters

**Files:** create `agent_v2/model_client.py`, `agent_v2/jev_client.py`, `agent_v2/library.py` and tests. Keep the old disabled adapter default intact until autonomous mode explicitly enables it.

**Interfaces:** `ModelClient.generate(task_kind, payload, *, seconds, attempt_dir) -> dict` returns status, parsed JSON content, usage, wall time and sanitized error category, retaining request/response artifacts. Configuration selects existing local credentials, endpoint and model. `JevSelector` implements the existing typed selector protocol with real recorded calls. `LocalLibrary.lookup/query` searches only explicitly allowed mathematical declarations and returns names, types and source provenance, never historical theorem proofs.

- [x] Add request-schema, malformed-response, timeout, secret-redaction, call-limit and typed-selection tests.
- [x] Implement clients against current official request schemas; no silent provider retry or hidden unbounded call loops.
- [x] Check available configuration without printing keys; perform bounded live preflight only after runnable integration is prepared.

### Task 3: Residual-aware execution and autonomous loop

**Files:** create `agent_v2/autonomous.py` and `agent_v2/autonomous_adapter.py`; modify narrowly `executor.py`, `loop.py`, `cli.py` as needed; add integration tests.

**Interfaces:** explicit autonomous `run`/`resume` configuration; task registry and model-call counters saved per run. Autonomous execution receives the selected representation, exact task, approved certificates, library results and bounded diagnostics. Existing manual/local stopping semantics remain available.

- [x] Add tests that a checked local result leads to a different open task, failed generated proof leaves C/O unchanged, replay never repeats accepted CAS, and all call/verification time is charged.
- [x] Build CAS-to-LLM continuation using real current residuals; model-generated decomposition changes O only after its implication bridge passes Lean.
- [x] Exercise genuine Train CAS -> LLM local proof -> original verification with rule selection first; preserve all failed attempts.

### Task 4: Multiple capabilities, real transformations and incremental expansion

**Files:** create `agent_v2/graph_builder.py`, `agent_v2/graph_proposals.py`; integrate autonomous loop and registry; focused tests.

**Interfaces:** initialize candidates from source structure and method contracts, with explicit per-task capability checks. Expansion proposals contain a bounded number of typed representations, exact conditional bridge targets and permitted method outlets. Commit graph changes only through validated state transitions, with unproved conditions represented explicitly.

- [x] Test multiple applicable alternatives, malformed/foreign proposals, unchanged state when bridge is rejected, no identity teleportation, and graph persistence without regeneration.
- [x] Add rule-derived starting alternatives and an LLM expansion request only when existing routes lack capability; actually validate and execute transformations.
- [x] Connect recorded Jev scoring/selection after deterministic legality filtering; only the current first action executes, then selection uses updated state.

### Task 5: End-to-end acceptance, regression and delivery

**Files:** new autonomous smoke drivers/tests, `agent_v2/AUTONOMOUS.md`, `agent_v2/AUTONOMOUS_VALIDATION.md`, final evidence under `agent_v2/generated/autonomous_20261112/`.

- [x] Preselect a small Train set by implemented structures, not post-hoc proof outcomes. Exercise CAS -> LLM, checked representation change -> CAS, and no-route -> incremental expansion where applicable.
- [x] Run an independently audited real original-theorem success, live model/Jev traces, fresh resume, meaningful Lean negative cases and budget boundaries. Distinguish structural/synthetic checks from actual autonomous mathematical success.
- [x] Freeze final source; run appropriate complete regression once integration is stable, then independently review invariants, generated-proof environment, cost accounting and evidence.
- [x] Preserve before/after/diff and exact commands; report implemented scope, unresolved method boundaries and reproducible usage without claiming full Train coverage.

## Acceptance evidence

Implemented and checked 2026-11-12. Full revision 01 suite: 553 passed. Final revision 02 changes only the model-call-limit stop classification, with 66 targeted tests passed. Two preselected Train originals passed with actual model outputs; the third retained two open goals after eight model calls and demonstrated real Jev selection/decomposition/focus. Final revision 02 controlled first-action expansion -> real CAS -> exact original passed with one actual model response. The controlled case is not an autonomous strategy score. See agent_v2/AUTONOMOUS_VALIDATION.md and generated/autonomous_20261112/final_validation.json.
