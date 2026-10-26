S={
62:'''(a b c q : K) (A : ℕ → K) (n : ℕ) (hq : regular q)
 (hp : ∀ x ∈ [a,b,c], x ≠ 0)
 (ho : phiDefined [a*q/b,a*q/c] q n)
 (hi : ∀ j ≤ n, phiDefined [a*q^j] q (n-j)) :
 (∑ k ∈ Finset.range (n+1), pochList [b,c,q^(-(n : ℤ))] q k /
 pochList [q,a*q/b,a*q/c] q k*A k) =
 ∑ j ∈ Finset.range (n+1),
 pochList [a*q/(b*c),a*q^j,q^(-(n : ℤ))] q j/pochList [q,a*q/b,a*q/c] q j *
 (-1)^j*q^(-((j : ℤ)*(j-1)/2)) *
 ∑ i ∈ Finset.range (n-j+1),
 pochList [q^((j : ℤ)-n),a*q^(2*j)] q i/pochList [q,a*q^j] q i *
 q^(-((i : ℤ)*j))*(b*c/(a*q))^(i+j)*A (i+j)''',
63:'''(a b c q z : K) (us vs : List K) (n : ℕ) (hq : regular q)
 (hlen : vs.length = us.length+1) (hp : ∀ x ∈ [a,b,c], x ≠ 0)
 (ho : phiDefined ([a*q/b,a*q/c] ++ vs) q n)
 (hi : ∀ j ≤ n, phiDefined (vs.map (fun v => q^j*v)) q (n-j)) :
 phi ([a,b,c] ++ us ++ [q^(-(n : ℤ))]) ([a*q/b,a*q/c] ++ vs) q z n =
 ∑ j ∈ Finset.range (n+1),
 pochList ([a*q/(b*c)] ++ us ++ [q^(-(n : ℤ))]) q j * poch a q (2*j) /
 pochList ([q,a*q/b,a*q/c] ++ vs) q j * (-b*c*z/(a*q))^j * q^(-((j : ℤ)*(j-1)/2)) *
 phi ([a*q^(2*j)] ++ us.map (fun u => q^j*u) ++ [q^((j : ℤ)-n)])
 (vs.map (fun v => q^j*v)) q (b*c*z/(a*q^(j+1))) (n-j)''',
64:'''(a q : K) (m : ℕ) (hq : regular q)
 (hl : phiDefined [a*q^(m+1)] q m)
 (hr : poch (a*q^(2*(m/2)+2)) (q^2) ((m+1)/2) ≠ 0) :
 phi [a,q^(-(m : ℤ))] [a*q^(m+1)] q (-q^(m+1)) m =
 poch (-q) q m * poch (a*q) (q^2) ((m+1)/2) /
 poch (a*q^(2*(m/2)+2)) (q^2) ((m+1)/2)''',
65:'''(a q : K) (n : ℕ) (hq : regular q) (ha : a ≠ 1)
 (hd : phiDefined [a*q^(n+1)] q n) :
 (∑ k ∈ Finset.range (n+1), (1-a*q^(2*k))/(1-a)*
 pochList [a,q^(-(n : ℤ))] q k/pochList [q,a*q^(n+1)] q k*q^(n*k)) =
 if n=0 then 1 else 0''',
66:'''(a q : K) (n : ℕ) (hq : regular q) (ha : a ≠ 1)
 (hd : phiDefined [a*q^(n+1)] q n) :
 (∑ k ∈ Finset.range (n+1), poch a q k*(1-a*q^(2*k))*poch (q^(-(n : ℤ))) q k /
 (poch q q k*(1-a)*poch (a*q^(n+1)) q k)*q^(2*k^2)*(a^2*q^n)^k) =
 poch (a*q) q n * ∑ k ∈ Finset.range (n+1),
 poch (q^(-(n : ℤ))) q k/poch q q k*(-a*q^(n+1))^k*q^(k*(k-1)/2)''',
67:'''(a b c l q : K) (A : ℕ → K) (N : ℕ) (hq : regular q)
 (hp : ∀ x ∈ [a,b,c,l], x ≠ 0) (hl : l ≠ 1)
 (hsupport : ∀ k, N < k → A k = 0)
 (hleft : phiDefined [a*q/b,a*q/c] q N)
 (ho : ∀ j ≤ N, pochList [q,a*q/b,a*q/c,q*a^2/(l*b*c)] q j * poch (l*q) q (2*j) ≠ 0)
 (hi : ∀ j ≤ N, phiDefined [l*q^(2*j+1),a^2*q^(j+1)/(l*b*c)] q (N-j)) :
 (∑ k ∈ Finset.range (N+1), pochList [a,b,c] q k/pochList [q,a*q/b,a*q/c] q k*A k) =
 ∑ j ∈ Finset.range (N+1),
 poch l q j*(1-l*q^(2*j))*pochList [l*b/a,l*c/a,a*q/(b*c)] q j*poch a q (2*j) /
 (poch q q j*(1-l)*pochList [a*q/b,a*q/c,q*a^2/(l*b*c)] q j*poch (l*q) q (2*j)) * (a/l)^j *
 ∑ k ∈ Finset.range (N-j+1),
 pochList [a*q^(2*j),a/l,l*b*c*q^j/a] q k /
 pochList [q,l*q^(2*j+1),a^2*q^(j+1)/(l*b*c)] q k*A (j+k)''',
68:'''(a b c d e l q : K) (n : ℕ) (hq : regular q)
 (hp : ∀ x ∈ [a,b,c,d,e,l], x ≠ 0) (hdef : l = q*a^2/(b*c*d))
 (hl : wDefined a [b,c,d,e,q^(-(n : ℤ))] q n)
 (hr : wDefined l [l*b/a,l*c/a,l*d/a,e,q^(-(n : ℤ))] q n)
 (hf : pochList [a*q/e,l*q] q n ≠ 0) :
 wellPoisedRaw a [b,c,d,e,q^(-(n : ℤ))] q (a^2*q^(n+2)/(b*c*d*e)) n =
 pochList [a*q,l*q/e] q n/pochList [a*q/e,l*q] q n *
 wellPoisedRaw l [l*b/a,l*c/a,l*d/a,e,q^(-(n : ℤ))] q (a*q^(n+1)/e) n''',
69:'''(a b c d e f q : K) (n : ℕ) (hq : regular q)
 (hp : ∀ x ∈ [a,b,c,d,e,f], x ≠ 0)
 (hl : wDefined a [b,c,d,e,f,a^3*q^(n+2)/(b*c*d*e*f),q^(-(n : ℤ))] q n)
 (hr : wDefined (d*e*f*q^(-(n : ℤ)-1)/a)
 [a*q/(b*c),d,e,f,b*d*e*f*q^(-(n : ℤ)-1)/a^2,c*d*e*f*q^(-(n : ℤ)-1)/a^2,q^(-(n : ℤ))] q n)
 (hf : pochList [a*q/d,a*q/e,a*q/f,a*q/(d*e*f)] q n ≠ 0) :
 wellPoisedRaw a [b,c,d,e,f,a^3*q^(n+2)/(b*c*d*e*f),q^(-(n : ℤ))] q q n =
 pochList [a*q,a*q/(d*e),a*q/(d*f),a*q/(e*f)] q n /
 pochList [a*q/d,a*q/e,a*q/f,a*q/(d*e*f)] q n *
 wellPoisedRaw (d*e*f*q^(-(n : ℤ)-1)/a)
 [a*q/(b*c),d,e,f,b*d*e*f*q^(-(n : ℤ)-1)/a^2,c*d*e*f*q^(-(n : ℤ)-1)/a^2,q^(-(n : ℤ))] q q n''',
70:'''(a b c q : K) (n : ℕ) (hq : regular q)
 (hp : ∀ x ∈ [a,b,c], x ≠ 0) (hw : wDefined a [b,c,a/(b*c)] q n)
 (hd : pochList [q,a*q/b,a*q/c,b*c*q] q n ≠ 0) :
 wellPoisedRaw a [b,c,a/(b*c)] q q n =
 pochList [a*q,b*q,c*q,a*q/(b*c)] q n/pochList [q,a*q/b,a*q/c,b*c*q] q n''',
71:'''(b c q : K) (n : ℕ) (hq : regular q) (hb : b ≠ 0) (hc : c ≠ 0)
 (hl : phiDefined [q^(1-(n : ℤ))/b,q^(1-(n : ℤ))/c,-b*c] q n)
 (hr : n%2=0 → pochList [b,c] q n*poch (b^2*c^2) (q^2) (n/2) ≠ 0) :
 phi [q^(-(n : ℤ)),b,c,-q^(1-(n : ℤ))/(b*c)]
 [q^(1-(n : ℤ))/b,q^(1-(n : ℤ))/c,-b*c] q q n =
 if n%2=0 then pochList [q,b^2,c^2] (q^2) (n/2)*poch (b*c) q n /
 (pochList [b,c] q n*poch (b^2*c^2) (q^2) (n/2)) else 0''',
72:'''(t a b c q : K) (N n : ℕ) (hq : regular q) (hn : n ≤ N) (hc : c ≠ 0) (ht : t ≠ 0)
 (hl : phiDefined [a*q,b*c*q,q^(-(N : ℤ))] q n)
 (hr : phiDefined [b*q,a/c*q,q^(-(N : ℤ))] q n) :
 qRacah t a b c q N n = pochList [a*q/c,b*q] q n/pochList [a*q,b*c*q] q n*c^n*
 qRacah (q^N/t) b a c⁻¹ q N n''',
73:'''(t a b c d q : K) (n : ℕ) (hq : regular q)
 (hp : ∀ x ∈ [a,b,t], x ≠ 0)
 (hl : phiDefined [a*b,a*c,a*d] q n) (hr : phiDefined [b*a,b*c,b*d] q n) :
 askeyWilson t a b c d q n = askeyWilson t b a c d q n ∧
 askeyWilson (-t) a b c d q n = (-1)^n*askeyWilson t (-a) (-b) (-c) (-d) q n''',
74:'''(a b q : K) (n : ℕ) (hq : regular q) (ha : a ≠ 0) (hb : b ≠ 0) (ha1 : a ≠ 1)
 (hl : ∀ k ≤ n, pochList [q,b*q,b*q^(-(n : ℤ))/a,a*q^(n+1)] q k *
 pochList [a^2*q^2/b,a^2*q/b] (q^2) k ≠ 0)
 (hr : pochList [a*q/b,a^2*q/b] q n ≠ 0) :
 (∑ k ∈ Finset.range (n+1), (1-a*q^(2*k))/(1-a)*
 pochList [a,a/b,a^2*q^(n+1)/b,q^(-(n : ℤ))] q k * pochList [b,b*q] (q^2) k*q^k /
 (pochList [q,b*q,b*q^(-(n : ℤ))/a,a*q^(n+1)] q k * pochList [a^2*q^2/b,a^2*q/b] (q^2) k)) =
 pochList [a*q,a^2*q/b^2] q n/pochList [a*q/b,a^2*q/b] q n''',
75:'''(a b q : K) (n : ℕ) (hq : regular q) (ha : a ≠ 0)
 (hl : ∀ k ≤ n, pochList [q,b] q k * poch (a*q^(1-(n : ℤ))) (q^2) k ≠ 0)
 (hr : n%2=0 → pochList [b*q,q/a] (q^2) (n/2) ≠ 0) :
 (∑ k ∈ Finset.range (n+1), pochList [q^(-(n : ℤ)),a] q k * poch b (q^2) k*q^k /
 (pochList [q,b] q k * poch (a*q^(1-(n : ℤ))) (q^2) k)) =
 if n%2=0 then pochList [q,b*q/a] (q^2) (n/2)/pochList [b*q,q/a] (q^2) (n/2) else 0''',
76:'''(s b q : K) (n : ℕ) (hq : regular q) (hb : b ≠ 0)
 (hl : phiDefined [s,s^2*q/b,b^2*q^(1-(n : ℤ))] q n)
 (hr : pochList [1/b^2,s^2*q/b,-s/b] q n ≠ 0) :
 phi [s^2,q*s,b,q^(-(n : ℤ))] [s,s^2*q/b,b^2*q^(1-(n : ℤ))] q q n =
 pochList [s^2/b^2,1/b,-q*s/b] q n/pochList [1/b^2,s^2*q/b,-s/b] q n''',
77:'''(s b c d l q : K) (n : ℕ) (hq : regular q)
 (hp : ∀ x ∈ [s,b,c,d,l], x ≠ 0) (hdef : l = q*s^4/(b*c*d)) (hl1 : l ≠ 1)
 (hl : phiDefined [s,s^2*q/b,s^2*q/c,s^2*q/d,s^4*q^(1-(n : ℤ))/l^2] q n)
 (hf : pochList [l*q,l^2/s^4,-l/s] q n ≠ 0)
 (hr : ∀ k ≤ n,
 pochList [q,s^2*q/b,s^2*q/c,s^2*q/d,l/s,-l*q/s,s^2*q^(1-(n : ℤ))/l,l*q^(n+1)] q k *
 poch (l^2*q/s^2) (q^2) k ≠ 0) :
 phi [s^2,q*s,b,c,d,q^(-(n : ℤ))]
 [s,s^2*q/b,s^2*q/c,s^2*q/d,s^4*q^(1-(n : ℤ))/l^2] q q n =
 pochList [l/s^2,l^2/s^2,-l*q/s] q n/pochList [l*q,l^2/s^4,-l/s] q n *
 ∑ k ∈ Finset.range (n+1),
 (1-l*q^(2*k))*pochList [l,l*b/s^2,l*c/s^2,l*d/s^2,q*s,-s,l^2*q^n/s^2,q^(-(n : ℤ))] q k *
 poch (s^2*q) (q^2) k*q^k /
 ((1-l)*pochList [q,s^2*q/b,s^2*q/c,s^2*q/d,l/s,-l*q/s,s^2*q^(1-(n : ℤ))/l,l*q^(n+1)] q k *
 poch (l^2*q/s^2) (q^2) k)''',
78:'''(a b c d e f g q : K) (n : ℕ) (hq : regular q)
 (hp : ∀ x ∈ [a,b,c,d,e,f,g], x ≠ 0) (hbal : a^3*q^(n+2)=b*c*d*e*f*g)
 (hl : wDefined a [b,c,d,e,f,g,q^(-(n : ℤ))] q n)
 (hr : wDefined (e*q^(-(n : ℤ))/b)
 [e,a*q/(b*c),a*q/(b*d),a*q/(b*f),a*q/(b*g),e*q^(-(n : ℤ))/a,q^(-(n : ℤ))] q n)
 (hf : pochList [a*q/c,a*q/d,a*q/e,a*q/f,a*q/g,b/e] q n ≠ 0) :
 wellPoisedRaw a [b,c,d,e,f,g,q^(-(n : ℤ))] q q n =
 pochList [a*q,a*q/(c*e),a*q/(d*e),a*q/(e*f),a*q/(e*g),b] q n /
 pochList [a*q/c,a*q/d,a*q/e,a*q/f,a*q/g,b/e] q n*e^n *
 wellPoisedRaw (e*q^(-(n : ℤ))/b)
 [e,a*q/(b*c),a*q/(b*d),a*q/(b*f),a*q/(b*g),e*q^(-(n : ℤ))/a,q^(-(n : ℤ))] q q n''',
79:'''(a b c d e f g q : K) (n : ℕ) (hq : regular q)
 (hp : ∀ x ∈ [a,b,c,d,e,f,g], x ≠ 0)
 (hl : wDefined a [b,c,d,e,f,g,q^(-(n : ℤ))] q n)
 (hf : pochList [a*q/f,a*q/g] q n ≠ 0)
 (ho : phiDefined [a*q/d,a*q/e,f*g*q^(-(n : ℤ))/a] q n)
 (hi : ∀ j ≤ n, phiDefined [a*q/b,a*q/c,d*e*q^(-(j : ℤ))/a] q j) :
 wellPoisedRaw a [b,c,d,e,f,g,q^(-(n : ℤ))] q (a^3*q^(n+3)/(b*c*d*e*f*g)) n =
 pochList [a*q,a*q/(f*g)] q n/pochList [a*q/f,a*q/g] q n *
 ∑ j ∈ Finset.range (n+1), pochList [q^(-(n : ℤ)),f,g,a*q/(d*e)] q j*q^j /
 pochList [q,a*q/d,a*q/e,f*g*q^(-(n : ℤ))/a] q j *
 phi [q^(-(j : ℤ)),d,e,a*q/(b*c)] [a*q/b,a*q/c,d*e*q^(-(j : ℤ))/a] q q j'''
}
