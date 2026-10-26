import Mathlib.Tactic.Ring
set_option maxHeartbeats 4000000
set_option maxRecDepth 4096
theorem FiniteQP1.native_local_relation {K : Type*} [Field K] (v0 v1 v2 v3 v4 : K) :
  ((v0 * v1 * v3) + ((-1) * v3 * v4 * (v0 ^ 2)) + ((-1) * v0 * v2 * v3 * (v1 ^ 2)) + (v1 * v2 * v3 * v4 * (v0 ^ 2))) - (((-1) * v0 * v2 * v4) + (v0 * v1 * v2 * v3) + (v0 * v1 * v2 * v4) + ((-1) * v0 * v2 * v3 * (v1 ^ 2))) - ((v1 * v2) + ((-1) * v0 * v1 * v2 * v3) + ((-1) * v0 * v1 * v2 * v4) + (v1 * v2 * v3 * v4 * (v0 ^ 2))) + ((v1 * v2) + (v3 * v4 * (v0 ^ 2)) + ((-1) * v0 * v1 * v3) + ((-1) * v0 * v2 * v4)) = 0 := by
  ring
#print axioms FiniteQP1.native_local_relation
