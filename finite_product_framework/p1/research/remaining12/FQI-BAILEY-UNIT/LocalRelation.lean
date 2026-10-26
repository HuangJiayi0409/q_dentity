import Mathlib.Tactic.Ring
set_option maxHeartbeats 4000000
set_option maxRecDepth 4096
theorem FiniteQP1.native_local_relation {K : Type*} [Field K] (v0 v1 v2 v3 : K) :
  (v1 + ((-1) * v0) + ((-1) * v2 * (v1 ^ 2)) + (v0 * v1 * v2)) - ((-1) + v1 + (v0 * v1 * v2) + ((-1) * v0 * v2 * (v1 ^ 2))) - ((1) + ((-1) * v0) + ((-1) * v2 * (v1 ^ 2)) + (v0 * v2 * (v1 ^ 2))) = 0 := by
  ring
#print axioms FiniteQP1.native_local_relation
