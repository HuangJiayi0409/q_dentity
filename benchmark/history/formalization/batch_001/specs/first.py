S={
1:'''(q : K) (n : ℕ) (k : ℤ) :
 gaussianInt q n k = gaussianInt q n ((n : ℤ)-k)''',
2:'''(q : K) (n k : ℕ) (hn : 1 ≤ n) (hk : k ≤ n) :
 gaussian q n k = gaussianInt q ((n : ℤ)-1) k +
 q^(n-k)*gaussianInt q ((n : ℤ)-1) ((k : ℤ)-1)''',
3:'''(q : K) (n k : ℕ) (hn : 1 ≤ n) (hk : k ≤ n) :
 gaussian q n k = q^k*gaussianInt q ((n : ℤ)-1) k +
 gaussianInt q ((n : ℤ)-1) ((k : ℤ)-1)''',
4:'''(q : K) (n k : ℕ) (hq : q ≠ 0) (hk : k ≤ n) :
 gaussian q⁻¹ n k = q^((k : ℤ)*((k : ℤ)-n))*gaussian q n k''',
5:'''(q z : K) (n : ℕ) :
 (∑ k ∈ Finset.range (n+1), (-1)^k*z^k*q^(k*(k-1)/2)*gaussian q n k) = poch z q n''',
6:'''(q : K) (n k : ℕ) (hk : k ≤ n) :
 gaussian q n k = rectangleWeight q (n-k) k''',
7:'''(F : Type*) [Field F] [Fintype F] (n k : ℕ) (hk : k ≤ n) :
 gaussian (Nat.card F : ℚ) n k =
 (Nat.card { U : Submodule F (Fin n → F) // Module.finrank F U = k } : ℚ)''',
8:'''(q : K) (m n h : ℕ) (hh : h ≤ m+n) :
 (∑ k ∈ Finset.Icc (h-m) (min h n), gaussian q n k * gaussian q m (h-k) * q^((n-k)*(h-k))) = gaussian q (m+n) h''',
9:'''(q : K) (m : ℕ) :
 (∑ j ∈ Finset.range (m+1), (-1)^j*gaussian q m j) =
 if m%2 = 0 then poch q (q^2) (m/2) else 0''',
10:'''(q t : K) (n : ℕ) (hn : 1 ≤ n) :
 rogersSzego t q (n+1) = (1+t)*rogersSzego t q n-(1-q^n)*t*rogersSzego t q (n-1)''',
11:'''(u : K) (n : ℕ) : rogersSzego u (u^2) n = poch (-u) u n''',
15:'''(a b c q : K) (n : ℕ) (hq : q ≠ 0) (hb : b ≠ 0) (hc : c ≠ 0)
 (hl : phiDefined [a*q/b,a*q/c,a*q^(n+1)] q n)
 (hr : pochList [a*q/b,a*q/c] q n ≠ 0) :
 wellPoised a [b,c,q^(-(n : ℤ))] q (a*q^(n+1)/(b*c)) n =
 pochList [a*q,a*q/(b*c)] q n / pochList [a*q/b,a*q/c] q n''',
16:'''(a b c d e q : K) (n : ℕ) (hq : q ≠ 0) (ha1 : a ≠ 1)
 (hp : ∀ x ∈ [a,b,c,d,e], x ≠ 0)
 (hl : phiDefined [a*q/b,a*q/c,a*q/d,a*q/e,a*q^(n+1)] q n)
 (hr : phiDefined [a*q/b,a*q/c,d*e*q^(-(n : ℤ))/a] q n)
 (hf : pochList [a*q/d,a*q/e] q n ≠ 0) :
 wellPoisedRaw a [b,c,d,e,q^(-(n : ℤ))] q (a^2*q^(n+2)/(b*c*d*e)) n =
 pochList [a*q,a*q/(d*e)] q n / pochList [a*q/d,a*q/e] q n *
 phi [a*q/(b*c),d,e,q^(-(n : ℤ))] [a*q/b,a*q/c,d*e*q^(-(n : ℤ))/a] q q n''',
17:'''(a b c d e f q : K) (n : ℕ) (hq : q ≠ 0)
 (hp : ∀ x ∈ [a,b,c,e,f], x ≠ 0)
 (hbal : d*e*f = a*b*c*q^(1-(n : ℤ)))
 (hl : phiDefined [d,e,f] q n)
 (hr : phiDefined [e*f/(a*b),e*f/(a*c),q^(1-(n : ℤ))/a] q n)
 (hf : pochList [e,f,e*f/(a*b*c)] q n ≠ 0) :
 phi [q^(-(n : ℤ)),a,b,c] [d,e,f] q q n =
 pochList [a,e*f/(a*b),e*f/(a*c)] q n / pochList [e,f,e*f/(a*b*c)] q n *
 phi [q^(-(n : ℤ)),e/a,f/a,e*f/(a*b*c)] [e*f/(a*b),e*f/(a*c),q^(1-(n : ℤ))/a] q q n''',
21:'''(q : K) (m : ℕ) (hm : 1 ≤ m) (a : Fin m → ℕ)
 (hden : ∀ i, poch q q (a i) ≠ 0) :
 (dysonProduct q a).coeff 0 = poch q q (∑ i, a i) / ∏ i, poch q q (a i)''',
24:'''(a q w : ℂ) (m n : ℕ) (hm : 0 < m) (hw : IsPrimitiveRoot w m) :
 poch (a^m) (q^m) n = ∏ j ∈ Finset.range m, poch (a*w^j) q n''',
25:'''(q x : ℂ) (n : ℕ) (hq : q ≠ 0) (hq1 : q ≠ 1) :
 jackson q (fun y => y^n) x = (1-q^n)/(1-q)*x^(n-1)''',
26:'''(t q : K) (N : ℕ) (hN : 7 ≤ N) :
 gollnitz t q N = gollnitz t q ((N : ℤ)-1) +
 if N%6 = 2 ∨ N%6 = 4 ∨ N%6 = 5
 then t*q^N*gollnitz t q ((N : ℤ)-6)
 else t^2*q^N*gollnitz t q ((N : ℤ)-7)''',
27:'''(t q : K) (n : ℤ) (hn : 1 ≤ n) :
 gollnitz t q (6*n+3)-t*q^(6*n+2)*gollnitz t q (6*n-3) =
 (1+t*q^2)*(1+t*q^4)*(1+t*q^5)*gollnitz (t*q^6) q (6*n-7)''',
28:'''(t q : K) (n : ℤ) (hn : 3 ≤ n) (hq : q ≠ 0) :
 gollnitz t q (6*n-1) =
 (1+t*q^(6*n)*(q^(-1 : ℤ)+q^(-2 : ℤ)+q^(-4 : ℤ)))*gollnitz t q (6*n-7) +
 t^2*q^(6*n)*(q^(-3 : ℤ)+q^(-5 : ℤ)+q^(-6 : ℤ))*(1-q^(6*n-6))*gollnitz t q (6*n-13) +
 t^3*q^(12*n-13)*(t*(q^(-1 : ℤ)+q^(-2 : ℤ)+q^(-4 : ℤ))+q^(6*n-12))*gollnitz t q (6*n-19) +
 t^6*q^(18*n-32)*gollnitz t q (6*n-25)''',
29:'''(t q : K) (n : ℤ) (hn : 2 ≤ n) :
 gollnitz t q (6*n+3)-t*q^(6*n+2)*gollnitz t q (6*n-3) =
 gollnitz t q (6*n+5)-t*q^(6*n+2)*(1+q^2+q^3)*gollnitz t q (6*n-1) +
 t^2*q^(12*n)*(1+q+q^3)*gollnitz t q (6*n-7)-t^3*q^(18*n-7)*gollnitz t q (6*n-13)''',
30:'''(q : K) (n : ℕ) (a : ℤ) (ha : a = 0 ∨ a = 1) :
 (∑ j ∈ Finset.Icc (0 : ℤ) (((n : ℤ)+1-a)/2),
 q^(j^2+a*j)*gaussianInt q ((n : ℤ)+1-a-j) j) =
 ∑ h ∈ Finset.Icc (-(n : ℤ)-2) ((n : ℤ)+2),
 (-1)^h*q^(h*(5*h+1)/2-2*a*h)*gaussianInt q ((n : ℤ)+1) ((((n : ℤ)+1-5*h)/2)+a)''',
31:'''[CharZero K] (q : K) (n : ℕ) (hden : ∀ j ∈ Finset.Icc 1 n, 1-q^j ≠ 0) :
 (poch q q n)⁻¹ = ∑ p ∈ cayleyVectors n,
 ∏ j : Fin n, ((j.val+1 : K)^(p j).val * (Nat.factorial (p j).val : K) * (1-q^(j.val+1))^(p j).val)⁻¹''',
32:'''(q : K) (k i a b mu : ℕ) (hi : 1 ≤ i) (hik : i ≤ k)
 (hab : b = a ∨ b+1 = a) :
 oscillationPoly q false k i a b (2*mu) =
 q^((mu : ℤ)*((4*(k : ℤ)+2)*mu+2*k-2*i+1)) *
 gaussianInt q (a+b) ((b : ℤ)-(2*(k : ℤ)+1)*mu)''',
33:'''(q : K) (k i a b mu : ℕ) (hi : 1 ≤ i) (hik : i ≤ k)
 (hab : b = a ∨ b+1 = a) (hmu : 1 ≤ mu) :
 oscillationPoly q false k i a b (2*mu-1) =
 q^((2*(mu : ℤ)-1)*((2*(k : ℤ)+1)*mu-2*k+i-1)) *
 gaussianInt q (a+b) ((b : ℤ)-(2*(k : ℤ)+1)*mu+2*k-i+1)''',
34:'''(q : K) (k i a b mu : ℕ) (hi : 1 ≤ i) (hik : i ≤ k)
 (hab : b = a ∨ b+1 = a) :
 oscillationPoly q true k i a b (2*mu) =
 q^((mu : ℤ)*((4*(k : ℤ)+2)*mu-2*k+2*i-1)) *
 gaussianInt q (a+b) ((b : ℤ)+(2*(k : ℤ)+1)*mu)''',
35:'''(q : K) (k i a b mu : ℕ) (hi : 1 ≤ i) (hik : i ≤ k)
 (hab : b = a ∨ b+1 = a) (hmu : 1 ≤ mu) :
 oscillationPoly q true k i a b (2*mu-1) =
 q^((2*(mu : ℤ)-1)*((2*(k : ℤ)+1)*mu-i)) *
 gaussianInt q (a+b) ((a : ℤ)-(2*(k : ℤ)+1)*mu+i)''',
36:'''(q : K) (n : ℕ) :
 schurD q n = ∑ j ∈ Finset.Icc (-(n : ℤ)-1) ((n : ℤ)+1),
 (-1)^j*q^(j*(5*j+1)/2)*gaussianInt q n (((n : ℤ)+5*j+1)/2)''',
37:'''(q : K) (n : ℕ) :
 schurE q n = ∑ j ∈ Finset.Icc (-(n : ℤ)-2) ((n : ℤ)+2),
 (-1)^j*q^(j*(5*j+3)/2)*gaussianInt q (n+1) (((n : ℤ)+5*j+3)/2)''',
38:'''(q : K) (m : ℕ) (hq : q ≠ 0) :
 q^(m*m)*schurD q⁻¹ (2*m) =
 (∑ j ∈ Finset.range (m+1), q^(j*j)*gaussian q (m+j) (2*j)) ∧
 (∑ j ∈ Finset.range (m+1), q^(j*j)*gaussian q (m+j) (2*j)) =
 ∑ k ∈ Finset.Icc (-(m : ℤ)-2) ((m : ℤ)+2),
 (q^(15*k^2-k)*gaussianInt q (2*m) ((m : ℤ)+5*k) -
 q^(15*k^2-11*k+2)*gaussianInt q (2*m) ((m : ℤ)+5*k-2))'''
}
