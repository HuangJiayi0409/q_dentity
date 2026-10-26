S={
40:'''(q L alpha : ℂ) (n : ℕ) (hlog : Complex.exp L = q) (hq : regular q) :
 (∏ j ∈ Finset.range n, (1-Complex.exp ((alpha+j)*L))/(1-q)) =
 (1-q)^(-(n : ℤ))*poch (Complex.exp (alpha*L)) q n''',
41:'''(q L alpha : ℂ) (n : ℕ) (hlog : Complex.exp L = q) (hq : regular q)
 (hroot : Complex.exp (L/2)-Complex.exp (-L/2) ≠ 0) :
 (∏ j ∈ Finset.range n,
 (Complex.exp ((alpha+j)*L/2)-Complex.exp (-(alpha+j)*L/2)) /
 (Complex.exp (L/2)-Complex.exp (-L/2))) =
 poch (Complex.exp (alpha*L)) q n / (1-q)^n *
 Complex.exp (((n : ℂ)*(1-alpha)/2-(n : ℂ)*(n-1)/4)*L)''',
42:'''(q u : K) (A : PowerSeries K) (n : ℕ) (hq : regular q) (hu : u^2 = q)
 (hzero : PowerSeries.coeff 0 A = 1)
 (hIVP : PowerSeries.rescale u A - PowerSeries.rescale u⁻¹ A =
 PowerSeries.C (u-u⁻¹) * PowerSeries.X * A) :
 PowerSeries.coeff (n+1) A = (1-q)/(1-q^(n+1))*u^n*PowerSeries.coeff n A ∧
 PowerSeries.coeff 0 A = 1 ∧
 PowerSeries.coeff n A = (1-q)^n*u^(n*(n-1)/2)/poch q q n''',
43:'''(q b : K) (r n : ℕ) (bs : Fin r → K) (ms : Fin r → ℕ)
 (hq : regular q) (hb : b ≠ 0) (hn : (∑ i, ms i) ≤ n)
 (hd : phiDefined (b*q :: List.ofFn bs) q n)
 (hr : ∀ i, poch (bs i) q (ms i) ≠ 0) :
 phi (q^(-(n : ℤ)) :: b :: List.ofFn (fun i => bs i*q^(ms i)))
 (b*q :: List.ofFn bs) q q n =
 b^n*poch q q n/poch (b*q) q n * ∏ i, poch (bs i/b) q (ms i)/poch (bs i) q (ms i)''',
44:'''(q : K) (r n : ℕ) (bs : Fin r → K) (ms : Fin r → ℕ)
 (hq : regular q) (hn : (∑ i, ms i) < n) (hd : phiDefined (List.ofFn bs) q n) :
 phi (q^(-(n : ℤ)) :: List.ofFn (fun i => bs i*q^(ms i))) (List.ofFn bs) q q n = 0''',
45:'''(q : K) (r n : ℕ) (bs : Fin r → K) (ms : Fin r → ℕ)
 (hq : regular q) (hn : (∑ i, ms i) ≤ n) (hd : phiDefined (List.ofFn bs) q n)
 (hr : ∀ i, poch (bs i) q (ms i) ≠ 0) :
 phi (q^(-(n : ℤ)) :: List.ofFn (fun i => bs i*q^(ms i))) (List.ofFn bs) q 1 n =
 (-1)^n*poch q q n*q^(-((n : ℤ)*(n+1)/2)) / ∏ i, poch (bs i) q (ms i)''',
46:'''(q : K) (r : ℕ) (bs : Fin r → K) (ms : Fin r → ℕ)
 (hq : regular q) (hd : phiDefined (List.ofFn bs) q (∑ i, ms i))
 (hr : ∀ i, poch (bs i) q (ms i) ≠ 0) :
 phi (q^(-((∑ i, ms i : ℕ) : ℤ)) :: List.ofFn (fun i => bs i*q^(ms i)))
 (List.ofFn bs) q q (∑ i, ms i) =
 (-1)^(∑ i, ms i)*poch q q (∑ i, ms i) *
 ∏ i, (bs i)^(ms i)*q^(ms i*(ms i-1)/2)/poch (bs i) q (ms i)''',
47:'''(a q : K) (k n : ℕ) (hq : regular q) (ha : a ≠ 0)
 (hd : poch (q/a) q k ≠ 0) :
 poch (a*q^(-(k : ℤ)-n)) q n =
 poch (q/a) q (n+k)/poch (q/a) q k * (-a/q)^n*q^(-(n : ℤ)*k-(n : ℤ)*(n-1)/2)''',
48:'''(a b q : K) (n : ℕ) :
 poch (a*b) q n = (∑ k ∈ Finset.range (n+1), gaussian q n k*b^k*poch a q k*poch b q (n-k)) ∧
 poch (a*b) q n = (∑ k ∈ Finset.range (n+1), gaussian q n k*a^(n-k)*poch a q k*poch b q (n-k))''',
49:'''(q : K) (m n : ℕ) (a : Fin (m+1) → K) (hm : 1 ≤ m) (hq : regular q) :
 poch (∏ j, a j) q n =
 ∑ k ∈ (Finset.univ : Finset (Fin m → Fin (n+1))).filter (fun k => (∑ i, (k i).val) ≤ n),
 (poch q q n * (∏ j : Fin m, poch (a j.castSucc) q (k j).val) *
 poch (a (Fin.last m)) q (n-∑ j, (k j).val) /
 ((∏ j : Fin m, poch q q (k j).val)*poch q q (n-∑ j, (k j).val))) *
 ∏ j : Fin (m+1), (a j)^(∑ i : Fin m, if i.val < j.val then (k i).val else 0)''',
50:'''(as bs : List K) (q z : K) (n : ℕ) (hq : regular q) (hz : z ≠ 0)
 (hp : ∀ a ∈ as ++ bs, a ≠ 0) (hd : phiDefined bs q n)
 (hr : phiDefined (as.map (fun a => q^(1-(n : ℤ))/a)) q n) :
 phi (as ++ [q^(-(n : ℤ))]) bs q z n =
 pochList as q n/pochList bs q n*(z/q)^n*
 ((-1 : K)^n*q^(n*(n-1)/2))^((bs.length : ℤ)-as.length-1) *
 ∑ k ∈ Finset.range (n+1),
 pochList (q^(-(n : ℤ)) :: bs.map (fun b => q^(1-(n : ℤ))/b)) q k /
 pochList (q :: as.map (fun a => q^(1-(n : ℤ))/a)) q k *
 (bs.prod/as.prod*q^(n+1)/z)^k''',
51:'''(b c q : K) (m n : ℕ) (hq : regular q) (hb : b ≠ 0) (hc : c ≠ 0)
 (hbden : poch b q m ≠ 0 ∧ poch b q n ≠ 0)
 (hd : phiDefined [c*q^(1-(n : ℤ))/b] q n) :
 pochList [c,b*q^n] q m/poch b q m =
 poch (b/c) q n/poch b q n * ∑ k ∈ Finset.range (n+1),
 pochList [q^(-(n : ℤ)),c] q k/pochList [q,c*q^(1-(n : ℤ))/b] q k*q^k*poch (c*q^k) q m''',
52:'''(b q : K) (n : ℕ) (hq : regular q)
 (hd : phiDefined [q*b^2] (q^2) (n/2)) (hr : poch (b^2) q n ≠ 0) :
 phi [q^(-(n : ℤ)),q^(1-(n : ℤ))] [q*b^2] (q^2) (q^2) (n/2) =
 poch (b^2) (q^2) n/poch (b^2) q n*q^(-((n : ℤ)*(n-1)/2))''',
53:'''(a q : K) (n : ℕ) (hq : regular q) (ha : a ≠ 0) :
 phi [a,q^(-(n : ℤ))] [] q (q^n/a) n = a^(-(n : ℤ))''',
54:'''(q z : ℂ) (f g : ℂ → ℂ) (n : ℕ) (hq : regular q) (hz : z ≠ 0) :
 ((jackson q)^[n] (fun x => f x*g x)) z =
 ∑ k ∈ Finset.range (n+1), gaussian q n k *
 ((jackson q)^[n-k] f) (z*q^k) * ((jackson q)^[k] g) z''',
55:'''(b c q z : K) (n : ℕ) (hq : regular q) (hp : ∀ x ∈ [b,c,z], x ≠ 0)
 (hl : phiDefined [c] q n) (hr : phiDefined [c,c*q/(b*z)] q n) :
 phi [q^(-(n : ℤ)),b] [c] q z n = poch (b*z*q^(-(n : ℤ))/c) q n *
 phi [q^(-(n : ℤ)),c/b,0] [c,c*q/(b*z)] q q n''',
56:'''(a b q : K) (n : ℕ) (hq : regular q)
 (hd : ∀ k ≤ n, 1-a*q^(n-k) ≠ 0) :
 (∑ k ∈ Finset.range (n+1), pochList [a,b] q k/poch q q k * (-a*b)^(n-k)*q^((n-k)*(n+k-1)/2)) =
 poch a q (n+1) * ∑ k ∈ Finset.range (n+1), (-b)^k*q^(k*(k-1)/2) /
 (poch q q k * poch q q (n-k)*(1-a*q^(n-k)))''',
57:'''(beta t q : K) (n : ℕ) (hq : regular q) (hb : beta ≠ 0) (ht : t ≠ 0)
 (hl : phiDefined [beta⁻¹*q^(1-(n : ℤ))] q n)
 (hr : phiDefined [beta^2,0] q n) :
 ultraspherical beta t q n =
 poch beta q n*t^n/poch q q n *
 phi [q^(-(n : ℤ)),beta] [beta⁻¹*q^(1-(n : ℤ))] q (q/(beta*t^2)) n ∧
 ultraspherical beta t q n =
 poch (beta^2) q n*t^(-(n : ℤ))*beta^(-(n : ℤ))/poch q q n *
 phi [q^(-(n : ℤ)),beta,beta*t^2] [beta^2,0] q q n''',
58:'''(b q x : K) (n : ℕ) : deltaOp q b (fun y => y^n) x = (b*q^n-1)*x^n''',
59:'''(as bs : List K) (q z : K) (n : ℕ) (hn : 1 ≤ n) (hq : regular q)
 (hd : phiDefined bs q n) :
 deltaList q (1 :: bs.map (fun b => b/q)) (fun x => phiTerm as bs q x n) z =
 z * deltaList q as (fun x => phiTerm as bs q x (n-1))
 (z*q^((1 : ℤ)+bs.length-as.length))''',
60:'''(a b c d q x : K) (n : ℕ) (hq : regular q)
 (hl : phiDefined [c*q] q n)
 (hp : ∀ k ≤ n, phiDefined [a*q] q k)
 (hc : ∀ k ≤ n, pochList [q,c*q,a*b*q^(k+1)] q k ≠ 0 ∧
 phiDefined [c*q^(k+1),a*b*q^(2*k+2)] q (n-k)) :
 littleJacobi x c d q n = ∑ k ∈ Finset.range (n+1),
 ((-1)^k*q^(k*(k+1)/2)*pochList [q^(-(n : ℤ)),a*q,c*d*q^(n+1)] q k /
 pochList [q,c*q,a*b*q^(k+1)] q k *
 phi [q^((k : ℤ)-n),c*d*q^(n+k+1),a*q^(k+1)]
 [c*q^(k+1),a*b*q^(2*k+2)] q q (n-k))*littleJacobi x a b q k''',
61:'''(R : Type*) [Ring R] [Algebra K R] (q : K) (X Y : R) (n : ℕ)
 (hq : regular q) (hcomm : X*Y = algebraMap K R q * Y*X) :
 (X+Y)^n = (∑ k ∈ Finset.range (n+1), algebraMap K R (gaussian q n k)*Y^k*X^(n-k)) ∧
 (X+Y)^n = (∑ k ∈ Finset.range (n+1), algebraMap K R (gaussian q⁻¹ n k)*X^k*Y^(n-k))'''
}
