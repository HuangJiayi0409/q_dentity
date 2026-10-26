S={
90:'''(a b c p q : K) (k : ℕ) (hp : regular p) (hq : regular q)
 (hnz : ∀ x ∈ [a,b,c], x ≠ 0) (ha : a ≠ 1) (hb : b ≠ 1)
 (hd : pochList [q,a*q/b] q k*pochList [a*p/c,b*c*p] p k ≠ 0)
 (hprev : 0 < k → pochList [q,a*q/b] q (k-1)*pochList [a*p/c,b*c*p] p (k-1) ≠ 0) :
 bibasicT a b c p q k - bibasicT a b c p q ((k : ℤ)-1) =
 (1-a*p^k*q^k)*(1-b*p^k*q^(-(k : ℤ)))*pochList [a,b] p k*pochList [c,a/(b*c)] q k*q^k /
 ((1-a)*(1-b)*pochList [q,a*q/b] q k*pochList [a*p/c,b*c*p] p k)''',
91:'''(a b c d p q : K) (k : ℤ) (hp : regular p) (hq : regular q)
 (hnz : ∀ x ∈ [a,b,c,d], x ≠ 0)
 (hc : (1-a)*(1-b)*(1-c)*(1-a*d^2/(b*c)) ≠ 0)
 (hs : bibasicSDefined a b c d p q k ∧ bibasicSDefined a b c d p q (k-1))
 (hi : pochListIntDefined [a,b] p k ∧ pochListIntDefined [c,a*d^2/(b*c)] q k) :
 bibasicS a b c d p q k-bibasicS a b c d p q (k-1) =
 d*(1-c/d)*(1-a*d/(b*c))*(1-a*d*p^k*q^k)*(1-b*p^k/(d*q^k)) /
 ((1-a)*(1-b)*(1-c)*(1-a*d^2/(b*c))) *
 pochListInt [a,b] p k*pochListInt [c,a*d^2/(b*c)] q k*q^k /
 (pochListInt [d*q,a*d*q/b] q k*pochListInt [a*d*p/c,b*c*p/d] p k)''',
92:'''(a b d p q : K) (n : ℕ) (hp : regular p) (hq : regular q)
 (hnz : ∀ x ∈ [a,b,d], x ≠ 0)
 (hc : (1-a*d)*(1-b/d) ≠ 0)
 (hl : ∀ k ≤ n, pochList [d*q,a*d*q/b] q k*pochList [a*d*p*q^n,b*p*q^(-(n : ℤ))/d] p k ≠ 0)
 (hr : (1-a*d)*(1-d/b)*(1-d*q^n)*(1-a*d*q^n/b) ≠ 0) :
 (∑ k ∈ Finset.range (n+1),
 (1-a*d*p^k*q^k)*(1-b*p^k/(d*q^k))*pochList [a,b] p k*pochList [q^(-(n : ℤ)),a*d^2*q^n/b] q k*q^k /
 ((1-a*d)*(1-b/d)*pochList [d*q,a*d*q/b] q k*pochList [a*d*p*q^n,b*p*q^(-(n : ℤ))/d] p k)) =
 (1-d)*(1-a*d/b)*(1-a*d*q^n)*(1-d*q^n/b) /
 ((1-a*d)*(1-d/b)*(1-d*q^n)*(1-a*d*q^n/b))''',
93:'''(a b p q : K) (n : ℕ) (hp : regular p) (hq : regular q)
 (ha : a ≠ 0) (hb : b ≠ 0) (hc : (1-a)*(1-b) ≠ 0)
 (hd : ∀ k ≤ n, pochList [q,a*q/b] q k*pochList [a*p*q^n,b*p*q^(-(n : ℤ))] p k ≠ 0) :
 (∑ k ∈ Finset.range (n+1),
 (1-a*p^k*q^k)*(1-b*p^k*q^(-(k : ℤ)))*pochList [a,b] p k*pochList [q^(-(n : ℤ)),a*q^n/b] q k*q^k /
 ((1-a)*(1-b)*pochList [q,a*q/b] q k*pochList [a*p*q^n,b*p*q^(-(n : ℤ))] p k)) =
 if n=0 then 1 else 0''',
94:'''(a b p q : K) (m n : ℕ) (hmn : m ≤ n) (hp : regular p) (hq : regular q)
 (ha : a ≠ 0) (hb : b ≠ 0)
 (hA : ∀ j ∈ Finset.Icc m n, inverseADefined a b p q n j ∧ inverseADefined a b p q j m)
 (hB : ∀ j ∈ Finset.Icc m n,
 pochList [q,a*q^(1+2*m)/b] q (j-m) ≠ 0 ∧ pochList [q,a*q^(1+2*j)/b] q (n-j) ≠ 0) :
 (∑ j ∈ Finset.Icc m n, inverseA a b p q n j*inverseB a b p q j m) = (if n=m then 1 else 0) ∧
 (∑ j ∈ Finset.Icc m n, inverseB a b p q n j*inverseA a b p q j m) = (if n=m then 1 else 0)''',
95:'''(a b c f q : K) (n : ℕ) (hq : regular q)
 (hp : ∀ x ∈ [a,b,c,f], x ≠ 0) (hac : a*c ≠ 1)
 (hl : ∀ k ≤ n, pochList [c*q^2,a*c*q^2/b,a*b*q] (q^2) k *
 pochList [a*c*q/f,f*q^(-2*(n : ℤ))/(a*c),a*c*q^(2*n+1)] q k ≠ 0)
 (hf : poch (a*c*q/f) q (2*n)*pochList [a*b*q,a*c^2*q^2/b] (q^2) n ≠ 0)
 (hw : wDefined (a*c^2/b) [f,a*c/b,c,c*q/b,c*q^2/b,a^2*c^2*q^(2*n+1)/f,q^(-2*(n : ℤ))] (q^2) n) :
 (∑ k ∈ Finset.range (n+1), (1-a*c*q^(3*k))/(1-a*c)*
 pochList [a,b,c*q/b] q k*pochList [f,a^2*c^2*q^(2*n+1)/f,q^(-2*(n : ℤ))] (q^2) k*q^k /
 (pochList [c*q^2,a*c*q^2/b,a*b*q] (q^2) k * pochList [a*c*q/f,f*q^(-2*(n : ℤ))/(a*c),a*c*q^(2*n+1)] q k)) =
 poch (a*c*q) q (2*n)*pochList [a*c^2*q^2/(b*f),a*b*q/f] (q^2) n /
 (poch (a*c*q/f) q (2*n)*pochList [a*b*q,a*c^2*q^2/b] (q^2) n) *
 wellPoisedRaw (a*c^2/b) [f,a*c/b,c,c*q/b,c*q^2/b,a^2*c^2*q^(2*n+1)/f,q^(-2*(n : ℤ))] (q^2) (q^2) n''',
96:'''(a c d f q : K) (n : ℕ) (hq : regular q)
 (hp : ∀ x ∈ [a,c,d,f], x ≠ 0) (hac : a*c ≠ 1)
 (hl : ∀ k ≤ 2*n, pochList [a*c*q/d,a*c*q/f,d*f/(a*c)] q k *
 pochList [c*q^2,a*q^(1-2*(n : ℤ)),a*c*q^(2*n+2)] (q^2) k ≠ 0)
 (hf : pochList [q/(a*c),a*c*q^2/d,a*c*q^2/f,d*f*q/(a*c)] (q^2) n ≠ 0)
 (hw : wDefined (a*c*q^(-2*(n : ℤ)-1))
 [c,d,f,a^2*c^2*q/(d*f),a*q^(-2*(n : ℤ)-1),q^(1-2*(n : ℤ)),q^(-2*(n : ℤ))] (q^2) n) :
 (∑ k ∈ Finset.range (2*n+1), (1-a*c*q^(3*k))/(1-a*c)*
 pochList [d,f,a^2*c^2*q/(d*f)] (q^2) k*pochList [a,c*q^(2*n+1),q^(-2*(n : ℤ))] q k*q^k /
 (pochList [a*c*q/d,a*c*q/f,d*f/(a*c)] q k * pochList [c*q^2,a*q^(1-2*(n : ℤ)),a*c*q^(2*n+2)] (q^2) k)) =
 pochList [a*c*q^2,d*q/(a*c),f*q/(a*c),a*c*q^2/(d*f)] (q^2) n /
 pochList [q/(a*c),a*c*q^2/d,a*c*q^2/f,d*f*q/(a*c)] (q^2) n *
 wellPoisedRaw (a*c*q^(-2*(n : ℤ)-1))
 [c,d,f,a^2*c^2*q/(d*f),a*q^(-2*(n : ℤ)-1),q^(1-2*(n : ℤ)),q^(-2*(n : ℤ))] (q^2) (q^2) n''',
97:'''(a b c q z : K) (m N : ℕ) (qs : Fin m → K) (cs ds : Fin m → List K)
 (hq : regular q) (hbases : ∀ i, regular (qs i)) (hp : ∀ x ∈ [a,b,c], x ≠ 0)
 (hterm : ∃ i, (qs i)^(-(N : ℤ)) ∈ cs i)
 (hd : phiDefined [a*q/b,a*q/c] q N)
 (hmd : ∀ i, ∀ k ≤ N, pochList (ds i) (qs i) k ≠ 0) :
 (∑ k ∈ Finset.range (N+1), pochList [a,b,c] q k/pochList [q,a*q/b,a*q/c] q k *
 (∏ i, multibaseTerm (qs i) (cs i) (ds i) k)*z^k) =
 ∑ j ∈ Finset.range (N+1), poch (a*q/(b*c)) q j*poch a q (2*j) /
 pochList [q,a*q/b,a*q/c] q j * (-b*c*z/(a*q))^j*q^(-((j : ℤ)*(j-1)/2)) *
 ∑ k ∈ Finset.range (N-j+1), poch (a*q^(2*j)) q k/poch q q k *
 (∏ i, multibaseTerm (qs i) (cs i) (ds i) (j+k)) * (b*c*z/(a*q^(j+1)))^k''',
98:'''(a b c w q : K) (n : ℕ) (hq : regular q) (hp : ∀ x ∈ [a,b,c,w], x ≠ 0)
 (hl : phiDefined [-a,a^2*q^2/b^2,a^2*q^2/c^2] (q^2) n)
 (hb : ∀ k ≤ n, pochList [w,-a*q^(n+1)] q k ≠ 0)
 (hf : pochList [w,-q] q n ≠ 0)
 (hr : phiDefined [a^2*q^2/b^2,a^2*q^2/c^2,a*q^(1-(n : ℤ))/w,a*q^(2-(n : ℤ))/w] (q^2) n) :
 bibasicPhi [a^2,-a*q^2,b^2,c^2] [-a,a^2*q^2/b^2,a^2*q^2/c^2]
 [-a*q/w,q^(-(n : ℤ))] [w,-a*q^(n+1)] (q^2) q (a*w*q^(n+2)/(b^2*c^2)) n =
 pochList [w/a,-a*q] q n/pochList [w,-q] q n *
 phi [a,a*q,a^2*q^2/w^2,a^2*q^2/(b^2*c^2),q^(-2*(n : ℤ))]
 [a^2*q^2/b^2,a^2*q^2/c^2,a*q^(1-(n : ℤ))/w,a*q^(2-(n : ℤ))/w] (q^2) (q^2) n''',
99:'''(a w q : K) (n : ℕ) (hq : regular q) (ha : a ≠ 0) (hw : w ≠ 0)
 (hl : phiDefined [a,-a] (q^2) n)
 (hb : ∀ k ≤ n, pochList [w,-a*q^(n+1)] q k ≠ 0)
 (hr : pochList [-q,a*q/w,w] q n ≠ 0) :
 bibasicPhi [a^2,a*q^2,-a*q^2] [a,-a] [-a*q/w,q^(-(n : ℤ))] [w,-a*q^(n+1)]
 (q^2) q (w*q^((n : ℤ)-1)/a) n =
 pochList [-a*q,a*q^2/w,w/(a*q)] q n/pochList [-q,a*q/w,w] q n''',
100:'''(a b q : K) (n : ℕ) (hq : regular q) (ha : a ≠ 0) (hb : b ≠ 0)
 (hl : phiDefined [-a,a^2*q^2/b^2] (q^2) n)
 (ho : ∀ k ≤ n, pochList [b^2*q^(1-(n : ℤ)),-a*q^(n+1)] q k ≠ 0)
 (hr : pochList [a*q^n/b^2,-q] q n*pochList [q/b^2,a^2*q^2/b^2] (q^2) n ≠ 0) :
 bibasicPhi [a^2,-a*q^2,b^2] [-a,a^2*q^2/b^2]
 [-a*q^n/b^2,q^(-(n : ℤ))] [b^2*q^(1-(n : ℤ)),-a*q^(n+1)] (q^2) q (q^2) n =
 pochList [q^n/b^2,-a*q] q n*pochList [a*q/b^2,a*q^2/b^2] (q^2) n /
 (pochList [a*q^n/b^2,-q] q n*pochList [q/b^2,a^2*q^2/b^2] (q^2) n)'''
}
