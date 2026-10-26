import Mathlib.Tactic
import Mathlib.Algebra.Polynomial.AlgebraMap
import Mathlib.Algebra.Polynomial.Eval.Defs

/- Finite word normalization: no commutativity of the carrier is assumed.
   Local equalities are rewrite rules, not additional axioms. -/
macro "operator_words" : tactic => `(tactic|
  (try simp only [Polynomial.mul_comp, Polynomial.X_comp,
    Polynomial.C_mul', smul_mul_assoc, mul_smul_comm, smul_smul,
    smul_add, add_smul, one_smul, zero_smul, smul_zero] at *)
  <;> first
    | (rfl)
    | (assumption)
    | (noncomm_ring [*, smul_add, add_smul, smul_smul, one_smul,
        zero_smul, smul_zero]; done))
