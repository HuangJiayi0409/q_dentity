S={
80:'''(a b c q z : K) (us vs : List K) (n : ℕ) (hq : regular q)
 (hlen : us.length = vs.length) (hp : ∀ x ∈ [a,b,c], x ≠ 0)
 (hl : phiDefined ([a,b] ++ vs) q n)
 (ho : phiDefined [c,c*q^(1-(n : ℤ))/(a*b)] q n)
 (hi : ∀ k ≤ n, phiDefined (c*q^k :: vs) q (n-k)) :
 phi ([q^(-(n : ℤ)),c,a*b/c] ++ us) ([a,b] ++ vs) q z n =
 pochList [c,a*b/c] q n/pochList [a,b] q n *
 ∑ k ∈ Finset.range (n+1),
 pochList [q^(-(n : ℤ)),c/a,c/b] q k*q^k/pochList [q,c,c*q^(1-(n : ℤ))/(a*b)] q k *
 phi ([q^((k : ℤ)-n),c] ++ us) (c*q^k :: vs) q z (n-k)''',
81:'''(a c q z : K) (bs : List K) (n : ℕ) (hq : regular q)
 (hp : ∀ x ∈ [a,c,z] ++ bs, x ≠ 0)
 (hl : phiDefined (bs.map (fun b => a*q/b) ++ [a*q/c,a*q^(n+1)]) q n)
 (hf : pochList [a*q/c,q^(1-(n : ℤ))/(c*z)] q n ≠ 0)
 (hc : 1-q^(-(n : ℤ))/(c*z) ≠ 0)
 (ho : phiDefined [a*q/(c*z),q/(c*z),q^(1-(n : ℤ))/c] q n)
 (hi : ∀ k ≤ n, phiDefined (bs.map (fun b => a*q/b) ++ [a*q^(k+1)/(c*z),a*q^(n+1-k)]) q (n-k)) :
 phi ([a] ++ bs ++ [c,q^(-(n : ℤ))]) (bs.map (fun b => a*q/b) ++ [a*q/c,a*q^(n+1)]) q (q*z) n =
 pochList [a*q/(c*z),q^(1-(n : ℤ))/c] q n/pochList [a*q/c,q^(1-(n : ℤ))/(c*z)] q n *
 ∑ k ∈ Finset.range (n+1),
 pochList [q^(-(n : ℤ))/(c*z),1/z,q^(-(n : ℤ))/a,q^(-(n : ℤ))] q k * (1-q^(2*(k : ℤ)-n)/(c*z)) /
 (pochList [q,a*q/(c*z),q/(c*z),q^(1-(n : ℤ))/c] q k * (1-q^(-(n : ℤ))/(c*z))) *
 (a*q^(n+1)/c)^k *
 phi ([a] ++ bs ++ [c*z*q^(-(k : ℤ)),q^((k : ℤ)-n)])
 (bs.map (fun b => a*q/b) ++ [a*q^(k+1)/(c*z),a*q^(n+1-k)]) q q (n-k)''',
82:'''(a b c d q z : K) (us vs : List K) (n : ℕ) (hq : regular q)
 (hlen : us.length = vs.length) (hl : phiDefined (c*q :: vs) q n)
 (ho : ∀ k ≤ n, pochList [q,c*q,a*b*q^(k+1)] q k ≠ 0)
 (hi : ∀ k ≤ n, phiDefined [c*q^(k+1),a*b*q^(2*k+2)] q (n-k) ∧ phiDefined (a*q :: vs) q k) :
 phi ([q^(-(n : ℤ)),c*d*q^(n+1)] ++ us) (c*q :: vs) q z n =
 ∑ k ∈ Finset.range (n+1),
 (-1)^k*q^(k*(k+1)/2)*pochList [a*q,c*d*q^(n+1),q^(-(n : ℤ))] q k /
 pochList [q,c*q,a*b*q^(k+1)] q k *
 phi [q^((k : ℤ)-n),c*d*q^(n+k+1),a*q^(k+1)] [c*q^(k+1),a*b*q^(2*k+2)] q q (n-k) *
 phi ([q^(-(k : ℤ)),a*b*q^(k+1)] ++ us) (a*q :: vs) q z k''',
83:'''(a b g d l u q : K) (n : ℕ) (hq : regular q)
 (hp : ∀ x ∈ [a,b,g,d,l,u], x ≠ 0) (hl : phiDefined [g,d] q n)
 (hi : ∀ k ≤ n, phiDefined [l,d*u/(a*b)] q k ∧ phiDefined [g/l,d*q^k] q (n-k)) :
 phi [a,b,q^(-(n : ℤ))] [g,d] q q n =
 ∑ k ∈ Finset.range (n+1), gaussian q n k *
 pochList [l,u*d/(a*b)] q k * poch (g/l) q (n-k) /
 (poch g q n*poch d q k) * l^n*(a*b/(l*u))^k *
 phi [u/a,u/b,q^(-(k : ℤ))] [l,d*u/(a*b)] q q k *
 phi [a*b/u,u/l,q^((k : ℤ)-n)] [g/l,d*q^k] q q (n-k)''',
84:'''(a b g d l s q : K) (n : ℕ) (hq : regular q)
 (hl0 : l ≠ 0) (hs0 : s ≠ 0) (hl : phiDefined [g,d] q n)
 (hi : ∀ k ≤ n, phiDefined [l,d/s] q k ∧ phiDefined [g/l,d*q^k] q (n-k)) :
 phi [a,b,q^(-(n : ℤ))] [g,d] q q n =
 ∑ k ∈ Finset.range (n+1), gaussian q n k *
 pochList [l,d/s] q k*poch (g/l) q (n-k)/(poch g q n*poch d q k)*l^n*(s/l)^k *
 phi [a/s,b,q^(-(k : ℤ))] [l,d/s] q q k *
 phi [s,b/l,q^((k : ℤ)-n)] [g/l,d*q^k] q q (n-k)''',
85:'''(a b g d l u v q : K) (n : ℕ) (hq : regular q)
 (hp : ∀ x ∈ [g,l,u,v], x ≠ 0) (hl : phiDefined [g,d] q n)
 (hf : pochList [g,u] q n ≠ 0)
 (hi : ∀ k ≤ n, phiDefined [g*u/(l*v),q^(1-(n : ℤ))/v] q (n-k) ∧ phiDefined [l,v,d] q k) :
 phi [a,b,q^(-(n : ℤ))] [g,d] q q n =
 ∑ k ∈ Finset.range (n+1), gaussian q n k *
 poch v q n*poch l q k*poch (g*u/(l*v)) q (n-k)/pochList [g,u] q n * l^(n-k) *
 phi [u/v,g/v,q^((k : ℤ)-n)] [g*u/(l*v),q^(1-(n : ℤ))/v] q (q^(1-(k : ℤ))/l) (n-k) *
 phi [a,b,u,q^(-(k : ℤ))] [l,v,d] q q k''',
86:'''(a b v g d r l u q : K) (n : ℕ) (hq : regular q)
 (hp : ∀ x ∈ [a,b,v,g,d,r,l,u], x ≠ 0) (hbal : a*b*v*q = d*g*r)
 (hl : phiDefined [g,d,r] q n) (hf : pochList [g,l*v*q/g] q n ≠ 0)
 (ho : ∀ k ≤ n,
 pochList [q,v*q/g,r,d,l*q^(1-(n : ℤ))/g,l*v*q^(n+1)/g] q k * poch (l*v/g) q (2*k) ≠ 0)
 (hi : ∀ k ≤ n, phiDefined [l,d*u/(a*b),u*r/(a*b)] q k ∧ phiDefined [g/l,d*q^k,r*q^k] q (n-k)) :
 phi [a,b,v*q^n,q^(-(n : ℤ))] [g,d,r] q q n =
 pochList [g/l,v*q/g] q n/pochList [g,l*v*q/g] q n*l^n *
 ∑ k ∈ Finset.range (n+1),
 pochList [l*v/g,l,d*u/(a*b),u*r/(a*b),v*q^n,q^(-(n : ℤ))] q k * poch (l*v*q/g) q (2*k) /
 (pochList [q,v*q/g,r,d,l*q^(1-(n : ℤ))/g,l*v*q^(n+1)/g] q k*poch (l*v/g) q (2*k)) *
 (d*r/(u*v))^k *
 phi [u/a,u/b,l*v*q^k/g,q^(-(k : ℤ))] [l,d*u/(a*b),u*r/(a*b)] q q k *
 phi [a*b/u,u/l,v*q^(k+n),q^((k : ℤ)-n)] [g/l,d*q^k,r*q^k] q q (n-k)''',
87:'''(a b v g d r l s q : K) (n : ℕ) (hq : regular q)
 (hp : ∀ x ∈ [a,l,g,s,v], x ≠ 0) (hbal : a*b*v*q = d*g*r)
 (hl : phiDefined [g,d,r] q n) (hf : pochList [g,l*v*q/g] q n ≠ 0)
 (ho : ∀ k ≤ n,
 pochList [q,v*q/g,d,r*s/a,l*q^(1-(n : ℤ))/g,v*l*q^(n+1)/g] q k*poch (l*v/g) q (2*k) ≠ 0)
 (hi : ∀ k ≤ n, phiDefined [l,d/s,r] q k ∧ phiDefined [g/l,d*q^k,s*r*q^k/a] q (n-k)) :
 phi [a,b,v*q^n,q^(-(n : ℤ))] [g,d,r] q q n =
 pochList [g/l,v*q/g] q n/pochList [g,l*v*q/g] q n*l^n *
 ∑ k ∈ Finset.range (n+1),
 pochList [l*v/g,l,r/a,d/s,v*q^n,q^(-(n : ℤ))] q k * poch (l*v*q/g) q (2*k) /
 (pochList [q,v*q/g,d,r*s/a,l*q^(1-(n : ℤ))/g,v*l*q^(n+1)/g] q k*poch (l*v/g) q (2*k)) *
 (s*q/g)^k *
 phi [a/s,b,l*v*q^k/g,q^(-(k : ℤ))] [l,d/s,r] q q k *
 phi [s,b/l,v*q^(n+k),q^((k : ℤ)-n)] [g/l,d*q^k,s*r*q^k/a] q q (n-k)''',
88:'''(v g l u q z : K) (as bs : List K) (n : ℕ) (hq : regular q)
 (hl0 : l ≠ 0) (hv0 : v ≠ 0) (hl : phiDefined (g :: bs) q n)
 (hf : pochList [g,u] q n ≠ 0)
 (ho : ∀ k ≤ n, pochList [q,q^(1-(n : ℤ))/l] q (n-k) ≠ 0)
 (hi : ∀ k ≤ n, phiDefined [g*u/(l*v),q^(1-(n : ℤ))/v] q (n-k) ∧ phiDefined (l :: bs) q k) :
 phi ([q^(-(n : ℤ)),v] ++ as) (g :: bs) q z n =
 pochList [l,v] q n/pochList [g,u] q n * ∑ k ∈ Finset.range (n+1),
 pochList [q^(-(n : ℤ)),g*u/(l*v)] q (n-k)/pochList [q,q^(1-(n : ℤ))/l] q (n-k)*q^(n-k) *
 phi [u/v,g/v,q^((k : ℤ)-n)] [g*u/(l*v),q^(1-(n : ℤ))/v] q (q^(1-(k : ℤ))/l) (n-k) *
 phi ([q^(-(k : ℤ)),u] ++ as) (l :: bs) q z k''',
89:'''(a b d e q : K) (n : ℕ) (hq : regular q)
 (hp : ∀ x ∈ [a,b,d,e], x ≠ 0)
 (hl : phiDefined [d,e] q n) (hr : phiDefined [a*q/d,a*q/e] q n) :
 phi [q^(-(n : ℤ)),a*q^n,b] [d,e] q (d*e/(a*b)) n =
 pochList [a*q/d,a*q/e] q n/pochList [d,e] q n*(d*e/(a*q))^n *
 phi [q^(-(n : ℤ)),a*q^n,a*b*q/(d*e)] [a*q/d,a*q/e] q (q/b) n'''
}
