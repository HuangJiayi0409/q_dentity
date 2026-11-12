# Read-only autonomous control review

Reviewed the new autonomous.py, autonomous_adapter.py and graph_proposals.py;
did not edit those files. Independent probes are `review_controls.py` and
`review_controls.json` in this directory. They use the project's explicitly
test-only model/checker doubles: all reported theorem statuses below describe
controller behavior, never Lean or model success evidence.

**Independent recheck after root's fixes:** rerunning review_controls.py now
returns budget_exhausted with zero remaining time for both previously failing
budget examples. The slow pre-final case no longer reports theorem success;
the execution-before-budget case records wall_budget_exhausted and zero model
calls. The selector receives only the remaining deadline (0.0433 seconds after
0.3572 seconds from an initial 0.4 seconds). Ordinary repair still takes two
fixture calls and records one repair. The defect descriptions below preserve
the earlier observations; they are resolved in the later independently tested
source. review_controls.json contains the latest run.

## Confirmed shared-wall-budget defects

1. **Uncharged pre-final work permits success after the total wall budget.**
   In `autonomous.run`, each loop records a new start time, performs source and
   invariant checks, then `if not state.O` calls `_final` directly. `_final`
   accounts only for its own work; it does not account for the preceding checks
   in that loop. The same early-return gap affects pause and action-limit paths.
   A warm offline probe used a 0.4-second initial budget and a 0.25-second delay
   after genuine source checking. It returned `original_theorem_proved` after
   0.775 seconds of actual run wall time, while reporting 0.0228 seconds left.
   The original final check itself remained correctly bound; the defect is
   total-budget accounting. Root was notified before any official Train run.

2. **Exhaustion before adapter execution is misclassified as corruption.**
   `run` computes execution_state with zero remaining seconds, but still calls
   AutonomousExecutor.execute. That executor re-filters graph legality before
   its zero-timeout branch. The budget filter removes the selected action,
   causing ContractError, which run classifies as integrity_error. The offline
   probe with 0.04 initial seconds and delayed source checking made zero model
   calls but returned `integrity_error/autonomous_execution_exception`, budget
   zero. A normal shared-budget stop should occur before legality revalidation
   against an exhausted execution state.

## Confirmed control behavior and root fixes observed

- Ordinary failed generated-proof verification preserves the original open
  task, then invokes a bounded repair. Offline run: two model-fixture calls,
  repairs=1, second action purpose=`repair`, accepted by the test-only checker.
- Root patched the selector timeout to subtract current-round work before the
  Jev call. The independent selector probe subsequently received 0.0772 seconds
  after 0.3278 seconds elapsed from a 0.4-second budget, consistent with that fix.
- The initial review found `_feedback` omitted actual `stdout.jsonl` files.
  Root reported this fixed, and the later source showed the filename included.
- completed_methods is method-wide; for the currently supported fixed
  source-local contracts, its successful certificate remains usable when a
  later checked decomposition introduces that exact local proposition. Graph
  independently suppresses duplicate CAS by proposition, leaves the obligation
  open, and allows a generated alias-based connection. No obligation is silently
  discharged by the method-completion filter.
- max_repairs/max_expansions currently count added fallback outlets; a regular
  model response may also propose decomposition without incrementing those
  counters. The overall max_model_calls still bounds the total graph growth.
  Root was informed so the option semantics can be stated or tightened.

The list `slow_integrity_checks` in the saved initial JSON was a mutable probe
list later appended by subsequent cases, so its eventual length is not the
number of source checks in the first timed case. The scalar initial budget,
measured wall time, returned status and remaining budget were captured at that
case's completion and establish the finding. The reproducer now records a
scalar count instead, to avoid this reporting artifact on future runs.
