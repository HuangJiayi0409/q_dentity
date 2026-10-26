import Benchmark.Batch5Definitions
import Mathlib.Analysis.Complex.Polynomial.Basic

namespace FiniteQBenchmark
open scoped BigOperators
noncomputable section
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem residueEval_reconstruct (f : Polynomial K) (q : K) :
    f.eval q = residueEval f (q^3) 0+q*residueEval f (q^3) 1+q^2*residueEval f (q^3) 2 := by
  simp only [residueEval,Finset.mul_sum,←Finset.sum_add_distrib,Polynomial.eval_eq_sum,Polynomial.sum]
  apply Finset.sum_congr rfl
  intro i _
  have hm : i%3 < 3 := Nat.mod_lt i (by omega)
  have hd := Nat.mod_add_div i 3
  have hp : q^i=(q^3)^(i/3)*q^(i%3) := by
    rw [←pow_mul,←pow_add]
    congr 1
    omega
  rw [hp]
  rcases (show i%3=0 ∨ i%3=1 ∨ i%3=2 by omega) with h|h|h <;> simp [h] <;> ring

theorem borwein_defining_decomposition (q : K) (n : ℕ) :
    (borweinBase K n).eval q = borweinA (q^3) n-q*borweinB (q^3) n-q^2*borweinC (q^3) n := by
  simpa [borweinA,borweinB,borweinC] using residueEval_reconstruct (borweinBase K n) q

theorem borweinBase_eval (q : K) (n : ℕ) :
    (borweinBase K n).eval q = poch q (q^3) n*poch (q^2) (q^3) n := by
  simp [borweinBase,poch,Polynomial.eval_prod,Finset.prod_mul_distrib,pow_add,pow_mul,mul_comm]
  simp only [←pow_mul,Nat.mul_comm]

theorem borwein_initial (q : K) : borweinA q 0=1 ∧ borweinB q 0=0 ∧ borweinC q 0=0 := by
  have hone : (1 : Polynomial K).support={0} := by
    simpa using (Polynomial.support_C (one_ne_zero : (1:K) ≠ 0))
  simp [borweinA,borweinB,borweinC,borweinBase,residueEval,hone]

theorem motivated_initial (q : K) : motivatedA q 3=1 ∧ motivatedA q 4=1 ∧ motivatedB q 3=0 := by
  norm_num [motivatedA,motivatedB]
  simp [Finset.sum_filter]

theorem capparelli_initial (q : K) : capparelliAlpha q 0=1 := by simp [capparelliAlpha]

theorem capparelli_residue_one (q : K) (r : ℕ) :
    capparelliAlpha q (3*r+1) = -q^((9*r*r+9*r+2)/2) := by
  simp [capparelliAlpha,Nat.mul_add_div]

theorem capparelli_residue_two (q : K) (r : ℕ) (hr : 1 ≤ r) :
    capparelliAlpha q (3*r-1) = -q^((9*r*r-9*r+2)/2) := by
  have h0 : 3*r-1 ≠ 0 := by omega
  have hm : (3*r-1)%3=2 := by omega
  have hd : (3*r-1+1)/3=r := by omega
  simp [capparelliAlpha,h0,hm,hd]

theorem capparelli_residue_zero (q : K) (r : ℕ) (hr : 1 ≤ r) :
    capparelliAlpha q (3*r) = q^(3*r*(3*r-1)/2)*(1+q^(3*r)) := by
  have h0 : 3*r ≠ 0 := by omega
  simp [capparelliAlpha,h0]

theorem kacPowerNat_zero (x a q : K) : kacPowerNat x a q 0=1 := by simp [kacPowerNat]

theorem kacPowerNat_succ (x a q : K) (n : ℕ) :
    kacPowerNat x a q (n+1)=kacPowerNat x a q n*(x-q^n*a) := by
  simp [kacPowerNat,Finset.prod_range_succ]

theorem kacPower_nonnegative (x a q : K) (n : ℕ) :
    kacPower x a q (n:ℤ)=kacPowerNat x a q n := by simp [kacPower]

theorem kacPower_negative (x a q : K) (n : ℕ) :
    kacPower x a q (-(n:ℤ))=(kacPowerNat x (q^(-(n:ℤ))*a) q n)⁻¹ := by
  cases n with
  | zero => simp [kacPower,kacPowerNat]
  | succ n =>
    have h : ¬(0:ℤ) ≤ -((n+1:ℕ):ℤ) := by omega
    rw [kacPower,if_neg h]
    simp only [neg_neg,Int.toNat_natCast]

theorem kacPower_negative_inverse (x a q : K) (n : ℕ)
    (h : kacPowerNat x (q^(-(n:ℤ))*a) q n ≠ 0) :
    kacPower x a q (-(n:ℤ))*kacPowerNat x (q^(-(n:ℤ))*a) q n=1 := by
  rw [kacPower_negative]
  exact inv_mul_cancel₀ h

theorem kacPower_nonnegative_defined (x a q : K) (n : ℕ) : kacPowerDefined x a q (n:ℤ) := by
  intro h
  omega

theorem qInteger_nat (q : K) (n : ℕ) (hq : q ≠ 1) : qInteger q n=geometric q n := by
  rw [geometric_quotient q n hq]
  simp only [qInteger,zpow_natCast]
  field_simp [sub_ne_zero.mpr hq,sub_ne_zero.mpr (Ne.symm hq)]
  <;> ring

theorem qFactorial_zero (q : K) : qFactorial q 0=1 := by simp [qFactorial]

theorem qFactorial_nonzero (q : K) (n : ℕ) (h : ∀ j ∈ Finset.Icc 1 n, geometric q j ≠ 0) :
    qFactorial q n ≠ 0 := Finset.prod_ne_zero_iff.mpr h

theorem kacM_eval (q x : K) (f : Polynomial K) : (kacM q f).eval x=f.eval (q*x) := by
  simp [kacM]

theorem kacX_eval (x : K) (f : Polynomial K) : (kacX f).eval x=x*f.eval x := by simp [kacX]

theorem independentTuples_mem {F : Type*} [Field F] [Fintype F] (n j : ℕ) (v : Fin j → Fin n → F) :
    v ∈ independentTuples F n j ↔ LinearIndependent F v := by simp [independentTuples]

theorem rankMatrices_mem {F : Type*} [Field F] [Fintype F] (m n j : ℕ) (A : Matrix (Fin m) (Fin n) F) :
    A ∈ rankMatrices F m n j ↔ A.rank=j := by simp [rankMatrices]

theorem finiteField_card_bound (F : Type*) [Field F] [Fintype F] : 2 ≤ Fintype.card F :=
  Fintype.one_lt_card

theorem symDenominator_nonzero (q : K) (hq : q ≠ 0) (hq2 : q^2 ≠ 1) : q-q⁻¹ ≠ 0 := by
  intro h
  apply hq2
  calc q^2=q*q := pow_two q
       _=q⁻¹*q := congrArg (fun z => z*q) (sub_eq_zero.mp h)
       _=1 := inv_mul_cancel₀ hq

theorem symJackson_nonzero (q x : ℂ) (f : ℂ → ℂ) (hx : x ≠ 0) :
    symJackson q f x=(f (q*x)-f (q⁻¹*x))/((q-q⁻¹)*x) := by simp [symJackson,hx]

theorem symJackson_zero (q : ℂ) (f : ℂ → ℂ) : symJackson q f 0=deriv f 0 := by simp [symJackson]

theorem symNumber_zero (q : K) : symNumber q 0=0 := by simp [symNumber]

theorem symNumber_one (q : K) (hq : q ≠ 0) (hq2 : q^2 ≠ 1) : symNumber q 1=1 := by
  simpa [symNumber] using div_self (symDenominator_nonzero q hq hq2)

theorem symFactorial_zero (q : K) : symFactorial q 0=1 := by simp [symFactorial]

theorem symFactorial_nonzero (q : K) (n : ℕ) (h : ∀ j ∈ Finset.Icc 1 n, symNumber q j ≠ 0) :
    symFactorial q n ≠ 0 := Finset.prod_ne_zero_iff.mpr h

theorem symPower_zero (x a q : K) : symPower x a q 0=1 := by simp [symPower]

theorem pairNumber_one (q r : ℂ) : pairNumber q r 1=1 := by
  unfold pairNumber
  split_ifs with h
  · simp
  · simp [sub_ne_zero.mpr h]

theorem quantumTaylor_pointwise (q r h h' a x : ℂ) (T : ℕ → Polynomial ℂ) (N k : ℕ)
    (hT : quantumTaylorFamily q r h h' a T N) (hk : k ∈ Finset.Icc 1 N)
    (hx : (q-r)*x+(h-h') ≠ 0) :
    ((T k).eval (q*x+h)-(T k).eval (r*x+h'))/((q-r)*x+(h-h'))=(T (k-1)).eval x := by
  have he := congrArg (fun p : Polynomial ℂ => p.eval x) (hT.2 k hk).2.2
  simp only [Polynomial.eval_sub,Polynomial.eval_comp,Polynomial.eval_add,Polynomial.eval_mul,
    Polynomial.eval_C,Polynomial.eval_X] at he
  rw [he]
  exact mul_div_cancel_left₀ _ hx

theorem quantumTaylor_boundary (q r h h' a : ℂ) (T : ℕ → Polynomial ℂ) (N k : ℕ)
    (hT : quantumTaylorFamily q r h h' a T N) (hk : k ∈ Finset.Icc 1 N) :
    (T k).eval a=0 := (hT.2 k hk).2.1

theorem quantumRootSum_coeff (T : ℕ → Polynomial ℂ) (n : ℕ)
    (hn : 1 ≤ (T n).natDegree) :
    quantumRootSum T n = -(T n).coeff ((T n).natDegree-1)/(T n).leadingCoeff := by
  have hp : T n ≠ 0 := by intro hz; simp [hz] at hn
  have hl : (T n).leadingCoeff ≠ 0 := Polynomial.leadingCoeff_ne_zero.mpr hp
  have hd : (T n).natDegree-((T n).natDegree-1)=1 := by omega
  have he := Polynomial.coeff_eq_esymm_roots_of_splits (IsAlgClosed.splits (T n))
    (Nat.sub_le (T n).natDegree 1)
  simp [hd,Multiset.esymm,Multiset.powersetCard_one] at he
  unfold quantumRootSum
  field_simp
  linear_combination he

theorem symTaylor_zero (q a : K) : symTaylor q a 0=1 := by rw [symTaylor]; simp

theorem symTaylor_unique (q a : K) (U : ℕ → Polynomial K) (h0 : U 0=1)
    (hs : ∀ n, n ≠ 0 → U n = Polynomial.C (1/symFactorial q n)*Polynomial.X^n -
      ∑ k : Fin n, Polynomial.C (a^(n-k.val)/symFactorial q (n-k.val))*U k.val) :
    ∀ n, U n=symTaylor q a n := by
  intro n
  induction n using Nat.strong_induction_on with
  | h n ih =>
    by_cases hn : n=0
    · subst n; rw [h0,symTaylor_zero]
    · rw [hs n hn,symTaylor,dif_neg hn]
      congr 1
      apply Finset.sum_congr rfl
      intro k _
      rw [ih k.val k.isLt]

end
end FiniteQBenchmark
