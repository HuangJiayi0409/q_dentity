"""Bounded original-domain reconstruction at singular recurrence indices.

Factorization only proposes a case split. Lean proves the factored leading
coefficient, every zero-factor branch and the original equality. In particular,
zero denominators and positive characteristic must not be silently discarded.
"""
import sympy as s


def singular_branch(prefix,order,coefficient,printer,definitions):
    leading=printer(s.factor(coefficient))
    return f'''  · intro gsN gsBound gsZero
    first
    | have gsNonzero : {prefix}C gsN {order} ≠ 0 := by
        dsimp only [{prefix}C]
        norm_num at *
        all_goals first | assumption | (exact pow_ne_zero _ (by assumption)) | aesop
      exact False.elim (gsNonzero gsZero)
    | have gsFactorZero : {leading} = 0 := by
        convert gsZero using 1 <;> norm_num [{prefix}C] <;>
          first | ring | (congr 1 <;> ring)
      simp (config := {{ failIfUnchanged := false }}) only [mul_eq_zero, div_eq_zero_iff,
        inv_eq_zero, pow_eq_zero_iff, neg_add_eq_sub, sub_eq_zero, or_false, false_or] at gsFactorZero
      repeat' (rcases gsFactorZero with gsFactorZero | gsFactorZero)
      all_goals dsimp only [{definitions}]
      all_goals first
        | (simp_all [poch_zero, poch_succ, Finset.sum_range_succ]; done)
        | (simp_all [poch_zero, poch_succ, Finset.sum_range_succ] <;> ring <;> done)
        | (by_cases gsIndexZero : gsN = 0 <;>
            simp_all [poch_zero, poch_succ, Finset.sum_range_succ] <;> done)
        | (norm_cast at gsFactorZero; omega)
'''
