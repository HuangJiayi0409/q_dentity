from common import *
S={};q,a,x=vs('q a x')
base='(hq : q ≠ 0) (hq1 : q ≠ 1)'
S[421]=f'''(q x c : ℂ) (N : ℕ) (f : Polynomial ℂ) {base}
 (hf : f.natDegree ≤ N) (hden : ∀ j ≤ N, qFactorial q j ≠ 0) :
 f.eval x = ∑ j ∈ Finset.range (N+1),
 (((jackson q)^[j]) (fun y => f.eval y) c)/qFactorial q j*kacPowerNat x c q j'''
S[422]=f'''(q x : ℂ) (n j : ℕ) {base} (hden : j ≤ n → qFactorial q (n-j) ≠ 0) :
 ((jackson q)^[j]) (fun y => y^n) x =
 if j ≤ n then qFactorial q n/qFactorial q (n-j)*x^(n-j) else 0'''
S[423]=ST('(q x : K) (n : ℕ)',x**'n',SUM('j','n',lambda j:G('n','j')*e('(kacPowerNat x 1 q j)')),base)
S[424]=f'''(q x a : ℂ) (n j : ℕ) {base} (hj : j ≤ n) (hden : qFactorial q (n-j) ≠ 0) :
 ((jackson q)^[j]) (fun y => kacPowerNat y (-a) q n) x =
 qFactorial q n/qFactorial q (n-j)*kacPowerNat x (-a) q (n-j)'''
S[425]=f'''(q : K) (f : Polynomial K) {base} :
 kacM q (kacX f) = q • kacX (kacM q f)'''
S[426]=f'''{{A : Type*}} [Ring A] [Algebra K A] (q : K) (X Y : A) (n : ℕ) {base}
 (hcomm : Y*X=q • (X*Y)) :
 (X+Y)^n = ∑ j ∈ Finset.range (n+1), gaussian q n j • (X^j*Y^(n-j))'''
S[427]=f'''(q : K) (n j : ℕ) {base} (hj : j ≤ n) :
 gaussian q n j = ∑ s ∈ (Finset.Icc 1 n).powersetCard j, q^(((∑ i ∈ s, i):ℤ)-(j:ℤ)*(j+1)/2)'''
S[428]='''{F : Type*} [Field F] [Fintype F] (n j : ℕ) (hj : j ≤ n) :
 (independentTuples F n j).card = ∏ i ∈ Finset.range j, ((Fintype.card F)^n-(Fintype.card F)^i)'''
S[429]='''{F : Type*} [Field F] [Fintype F] (m n j : ℕ) (hj : j ≤ min m n) :
 ((rankMatrices F m n j).card : ℤ) =
 gaussian (Fintype.card F : ℤ) n j*gaussian (Fintype.card F : ℤ) m j*
 (∏ i ∈ Finset.range j, ((Fintype.card F : ℤ)^j-(Fintype.card F : ℤ)^i)) ∧
 gaussian (Fintype.card F : ℤ) n j*gaussian (Fintype.card F : ℤ) m j*
 (∏ i ∈ Finset.range j, ((Fintype.card F : ℤ)^j-(Fintype.card F : ℤ)^i)) =
 gaussian (Fintype.card F : ℤ) n j*(∏ i ∈ Finset.range j, ((Fintype.card F : ℤ)^m-(Fintype.card F : ℤ)^i))'''
S[430]=f'''(q : K) (n : ℕ) {base} (hn : 1 ≤ n) :
 galoisNumber q (n+1)=2*galoisNumber q n+(q^n-1)*galoisNumber q (n-1) ∧
 galoisNumber q 0=1 ∧ galoisNumber q 1=2'''
S[431]=f'''(q x : ℂ) (n j : ℕ) {base} (hn : 1 ≤ n)
 (hshift : ∀ s ≤ j, kacPowerNat 1 (q^s*x) q n ≠ 0)
 (hout : kacPowerNat 1 x q (n+j) ≠ 0) :
 ((jackson q)^[j]) (fun y => 1/kacPowerNat 1 y q n) x =
 (∏ r ∈ Finset.range j, geometric q (n+r))/kacPowerNat 1 x q (n+j)'''
S[432]=ST('(q a : K) (n : ℕ)',E('(∏ j ∈ Finset.range n, (a-q^(-(j:ℤ))))'),e('(-1:K)')**'n'*e('(q^(-((n:ℤ)*(n-1)/2)))')*P([a],'n'),base)
S[433]=f'''(q x : ℂ) (n j : ℕ) {base} (hj : j ≤ n) (hden : qFactorial q (n-j) ≠ 0) :
 ((jackson q)^[j]) (fun y => kacPowerNat 1 (-y) q n) x =
 q^(j*(j-1)/2)*(qFactorial q n/qFactorial q (n-j))*kacPowerNat 1 (-q^j*x) q (n-j)'''
S[434]=ST('(q a x : K) (M : ℕ)',P([q/(a*x)],'M-1')*x**'(M-1)'/P([Q('1-M')*a*x],'M-1'),e('(-1:K)')**'(M-1)'*q**'(M*(M-1)/2)'*e('(a^(1-(M:ℤ)))'),base+' (hM : 1 ≤ M) (hax : a*x ≠ 0)')
S[435]=f'''(q x : ℂ) (F : ℂ → ℂ) (N : ℕ) {base} (hx : x ≠ 0) :
 (1-q)*x*(∑ j ∈ Finset.range (N+1), q^j*jackson q F (q^j*x)) = F x-F (q^(N+1)*x)'''
