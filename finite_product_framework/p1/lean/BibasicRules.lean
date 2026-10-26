import Mathlib.Tactic.Tauto
import Mathlib.Tactic.ClearExcept
import Benchmark.P1Atoms
import Lean

set_option maxHeartbeats 1000000

/-- Expose bounded domain hypotheses at an actual summation index.
    No hypothesis names or identity-specific conditions are assumed. -/
elab "p1_bibasic_domain " idx:term : tactic => Lean.Elab.Tactic.withMainContext do
  let ctx ← Lean.MonadLCtx.getLCtx
  for decl in ctx do
    if !decl.isImplementationDetail && decl.type.isForall && (← Lean.Meta.isProp decl.type) then
      let h := Lean.mkIdent decl.userName
      let fact := Lean.mkIdent (← Lean.Meta.getUnusedUserName `bbDomain)
      try
        Lean.Elab.Tactic.evalTactic (← `(tactic|
          have $fact := $h $idx (by first | omega | (simp only [Finset.mem_range]; omega))))
        let code := "simp only [FiniteQBenchmark.pochList_cons, FiniteQBenchmark.pochList_nil, " ++
          "div_eq_mul_inv, mul_inv_rev, inv_inv, inv_pow, pow_one, neg_mul, mul_neg, " ++
          "one_mul, mul_one, mul_comm, mul_left_comm, mul_assoc, mul_ne_zero_iff] at " ++
          fact.getId.toString
        Lean.Elab.Tactic.evalTactic (← Lean.ofExcept (Lean.Parser.runParserCategory (← Lean.getEnv) `tactic code))
      catch _ => pure ()
