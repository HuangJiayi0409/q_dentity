# Finite product reconstruction extensions

The existing product method remains a bounded structural certificate search,
followed by exact Lean reconstruction. It is not a new CAS factorization solver.
The following rules supplement its existing block, residue, split and reflection
rules without changing the common preprocessor or other methods.

## Nonempty head split

When a product domain contains natural subtraction, the planner can propose
splitting off the first factor of a range product. The generic theorem requires
`0 < n`; Lean must prove that condition from the original context. It rewrites
`∏ k < n, f k` to `f 0 * ∏ k < n-1, f(k+1)`. The latter bound is natural subtraction,
not an unchecked integer subtraction. Product congruence and exact normalization
then check the remaining factors. Empty products cannot silently use this rule.

## Transposition and primitive-root factors

For nested finite range products the planner can propose exchanging the two
independent domains, in either equality orientation. Dependency or domain
mismatches fail during reconstruction.

The factor verifier can now use the polynomial identity
`X^m-C(x^m) = ∏ j<m, (X-C(w^j*x))`, instantiated only with a proved positive order
and `IsPrimitiveRoot w m`. Evaluating this generic mathlib factorization at `X=1`
gives `∏ j<m, (1-x*w^j)=1-x^m`. A weighted variant uses exact ring normalization.
These rules cover integral domains, including zero values of `x`, without
assuming `x ≠ 0`. A condition `w^m=1` alone is insufficient and is not accepted.

This shares a general polynomial factorization theorem; it does not call a
preproved Pochhammer identity, another method, or a historical benchmark proof.
The original statement, assumptions, proof dependency audit and certificate
acceptance contract are unchanged.

## Limits and evidence

The planner is still bounded and incomplete. Only natural range products are
admitted. It does not search arbitrary algebraic factors, synthesize roots of
unity, prove arbitrary reindexing bijections, or support all rational-function
side conditions. Missing hypotheses and unsupported pointwise expressions remain
failures, not claims of mathematical impossibility.

Focused evidence is stored in `../generated/product_completion_20261019/`:
selected old failed Train inputs `FQI-SRC-FINE-2.1`, `FQI-POCHHAMMER-ROOTS`, and all
five product successes from the completed first-round Train baseline. The final
`validation.json` records what actually passed. `test_completion.py` checks
renaming, parameter scaling, wrong factors, removed assumptions, weaker root
conditions, and tampered construction plans. These samples do not determine a
new full Train success rate.
