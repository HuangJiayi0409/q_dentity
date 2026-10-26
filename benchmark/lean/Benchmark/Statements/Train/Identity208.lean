import Benchmark.Batch3Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-SRC-GR2-11.6.6-p0 — 多底数有限双边求和
Original representative source: GR2-11.6.6-p0
Frozen statement: formulas/train/FQI-SRC-GR2-11.6.6-p0.md
Source formula:
\sum_{k=-m}^n\frac{(1-ad(rst/q)^k)(1-br^k/(dq^k))(1-cs^k/(dq^k))(1-adt^k/(bcq^k))}{(1-ad)(1-b/d)(1-c/d)(1-ad/(bc))}\frac{(a;rst/q^2)_k(b;r)_k(c;s)_k(ad^2/(bc);t)_kq^k}{(dq;q)_k(adst/(bq);st/q)_k(adrt/(cq);rt/q)_k(bcrs/(dq);rs/q)_k}=\frac{(1-a)(1-b)(1-c)(1-ad^2/(bc))}{d(1-ad)(1-b/d)(1-c/d)(1-ad/(bc))}\left[\frac{(arst/q^2;rst/q^2)_n(br;r)_n(cs;s)_n(ad^2t/(bc);t)_n}{(dq;q)_n(adst/(bq);st/q)_n(adrt/(cq);rt/q)_n(bcrs/(dq);rs/q)_n}-\frac{(c/(ad);rt/q)_{m+1}(d/(bc);rs/q)_{m+1}(1/d;q)_{m+1}(b/(ad);st/q)_{m+1}}{(1/c;s)_{m+1}(bc/(ad^2);t)_{m+1}(1/a;rst/q^2)_{m+1}(1/b;r)_{m+1}}\right].
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity208
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (a b c d r s t q : K) (m n : ℕ)
 (hbase : regular q) (hnz : a*b*c*d*r*s*t*q ≠ 0) (hr : regular r) (hs : regular s) (ht : regular t)
 (h_domain : ∀ k ∈ Finset.Icc (-(m:ℤ)) (n:ℤ), (q ≠ 0 ∧
    (d * ((q)^k)) ≠ 0 ∧
    ((b * c) * ((q)^k)) ≠ 0 ∧
    d ≠ 0 ∧
    (b * c) ≠ 0 ∧
    ((((1 - (a * d)) * (1 - (b / d))) * (1 - (c / d))) * (1 - ((a * d) / (b * c)))) ≠ 0 ∧
    (q^2) ≠ 0 ∧
    pochListIntDefined [a] ((((r * s) * t) / (q^2))) k ∧
    pochListIntDefined [b] (r) k ∧
    pochListIntDefined [c] (s) k ∧
    pochListIntDefined [((a * (d^2)) / (b * c))] (t) k ∧
    pochListIntDefined [(d * q)] (q) k ∧
    (b * q) ≠ 0 ∧
    pochListIntDefined [((((a * d) * s) * t) / (b * q))] (((s * t) / q)) k ∧
    (c * q) ≠ 0 ∧
    pochListIntDefined [((((a * d) * r) * t) / (c * q))] (((r * t) / q)) k ∧
    (d * q) ≠ 0 ∧
    pochListIntDefined [((((b * c) * r) * s) / (d * q))] (((r * s) / q)) k ∧
    ((((pochListInt [(d * q)] (q) k) * (pochListInt [((((a * d) * s) * t) / (b * q))] (((s * t) / q)) k)) * (pochListInt [((((a * d) * r) * t) / (c * q))] (((r * t) / q)) k)) * (pochListInt [((((b * c) * r) * s) / (d * q))] (((r * s) / q)) k)) ≠ 0) ∧
    (b * c) ≠ 0 ∧
    d ≠ 0 ∧
    ((((d * (1 - (a * d))) * (1 - (b / d))) * (1 - (c / d))) * (1 - ((a * d) / (b * c)))) ≠ 0 ∧
    (q^2) ≠ 0 ∧
    (b * q) ≠ 0 ∧
    q ≠ 0 ∧
    (c * q) ≠ 0 ∧
    (d * q) ≠ 0 ∧
    ((((pochList [(d * q)] q (n)) * (pochList [((((a * d) * s) * t) / (b * q))] ((s * t) / q) (n))) * (pochList [((((a * d) * r) * t) / (c * q))] ((r * t) / q) (n))) * (pochList [((((b * c) * r) * s) / (d * q))] ((r * s) / q) (n))) ≠ 0 ∧
    (a * d) ≠ 0 ∧
    c ≠ 0 ∧
    (a * (d^2)) ≠ 0 ∧
    a ≠ 0 ∧
    b ≠ 0 ∧
    ((((pochList [(1 / c)] s (m+1)) * (pochList [((b * c) / (a * (d^2)))] t (m+1))) * (pochList [(1 / a)] (((r * s) * t) / (q^2)) (m+1))) * (pochList [(1 / b)] r (m+1))) ≠ 0) :
 (∑ k ∈ Finset.Icc (-(m:ℤ)) (n:ℤ), (((((((((((1 - ((a * d) * (((((r * s) * t) / q))^k))) * (1 - ((b * ((r)^k)) / (d * ((q)^k))))) * (1 - ((c * ((s)^k)) / (d * ((q)^k))))) * (1 - (((a * d) * ((t)^k)) / ((b * c) * ((q)^k))))) / ((((1 - (a * d)) * (1 - (b / d))) * (1 - (c / d))) * (1 - ((a * d) / (b * c))))) * (pochListInt [a] ((((r * s) * t) / (q^2))) k)) * (pochListInt [b] (r) k)) * (pochListInt [c] (s) k)) * (pochListInt [((a * (d^2)) / (b * c))] (t) k)) * ((q)^k)) / ((((pochListInt [(d * q)] (q) k) * (pochListInt [((((a * d) * s) * t) / (b * q))] (((s * t) / q)) k)) * (pochListInt [((((a * d) * r) * t) / (c * q))] (((r * t) / q)) k)) * (pochListInt [((((b * c) * r) * s) / (d * q))] (((r * s) / q)) k)))) = ((((((1 - a) * (1 - b)) * (1 - c)) * (1 - ((a * (d^2)) / (b * c)))) / ((((d * (1 - (a * d))) * (1 - (b / d))) * (1 - (c / d))) * (1 - ((a * d) / (b * c))))) * ((((((pochList [(a * (((r * s) * t) / (q^2)))] (((r * s) * t) / (q^2)) (n)) * (pochList [(b * r)] r (n))) * (pochList [(c * s)] s (n))) * (pochList [(((a * (d^2)) * t) / (b * c))] t (n))) / ((((pochList [(d * q)] q (n)) * (pochList [((((a * d) * s) * t) / (b * q))] ((s * t) / q) (n))) * (pochList [((((a * d) * r) * t) / (c * q))] ((r * t) / q) (n))) * (pochList [((((b * c) * r) * s) / (d * q))] ((r * s) / q) (n)))) - (((((pochList [(c / (a * d))] ((r * t) / q) (m+1)) * (pochList [(d / (b * c))] ((r * s) / q) (m+1))) * (pochList [(1 / d)] q (m+1))) * (pochList [(b / (a * d))] ((s * t) / q) (m+1))) / ((((pochList [(1 / c)] s (m+1)) * (pochList [((b * c) / (a * (d^2)))] t (m+1))) * (pochList [(1 / a)] (((r * s) * t) / (q^2)) (m+1))) * (pochList [(1 / b)] r (m+1)))))) := by
  sorry

end FiniteQBenchmark.Identity208
