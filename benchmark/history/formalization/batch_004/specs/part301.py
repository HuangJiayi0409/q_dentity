from common import *
S={};a,b,c,q,x,z,t=vs('a b c q x z t')
S[301]='''(q : K) (k r n : ℕ) (hk : 0 < k) (hr : 0 < r) (hq : q ≠ 0) :
 planeBoxPi q k r n = (∑ ns ∈ rectangle n k, planePi q r (fun i => (ns i).val)) ∧
 (∑ ns ∈ rectangle n k, planePi q r (fun i => (ns i).val)) = q^(-((k:ℤ)*n))*planePi q (r+1) (fun _ : Fin k => n)'''
S[302]='''(q : K) (N M : ℕ) (hN : 0 < N) (hM : 0 < M) :
 (∑ n ∈ Finset.Icc M (M*N), (boundedCompositionCount N M n : K)*q^n) =
 (∑ j ∈ Finset.Icc 1 N, q^j)^M'''
S[303]='''(q : K) (N : ℤ) (n : ℕ) (a : ℕ → ℤ)
 (hq : q ≠ 0) (hden : ∀ j ≤ n, poch q q j ≠ 0)
 (hstep : ∀ i, 1 ≤ i → i < n → a (i+1)-a i = 0 ∨ a (i+1)-a i = 1) :
 integerTopGaussian q N n = ∑ k ∈ Finset.range (n+1),
 q^(((n:ℤ)-k)*(a (k+1)-k))*integerTopGaussian q (a k) k *
 integerTopGaussian q (N-a (k+1)) (n-k)'''
S[304]='''(x q : K) (r : ℕ) (hr : 2 ≤ r) (hx : x ≠ 0) :
 aqHermite x q r = (x+x⁻¹)*aqHermite x q (r-1)-(1-q^(r-1))*aqHermite x q (r-2) ∧
 aqHermite x q 0 = 1 ∧ aqHermite x q 1 = x+x⁻¹'''
S[305]='''(q : ℂ) (theta : ℝ) (r : ℕ) :
 aqHermite (Complex.exp (Complex.I*(theta:ℂ))) q r =
 (∑ j ∈ Finset.range (r+1), gaussian q r j*(Real.cos (((r:ℝ)-2*j)*theta) : ℂ)) ∧
 (∑ j ∈ Finset.range (r+1), gaussian q r j*(Real.cos (((r:ℝ)-2*j)*theta) : ℂ)) =
 (∑ j ∈ Finset.range (r+1), gaussian q r j*Complex.exp (Complex.I*((r:ℂ)-2*j)*(theta:ℂ)))'''
S[306]=ST('(q : K) (r N : ℕ)',SUM('j','N/2',lambda j:G('r+2*j','j')*e('(aqInverseT q (r+2*j) (N-2*j))')),KD('N','0'))
S[307]='''(q : K) (r N : ℕ) (hN : 1 ≤ N) :
 aqInverseT q r 0 = 1 ∧ aqInverseT q r N =
 -(∑ j ∈ Finset.Icc 1 (N/2), gaussian q (r+2*j) j*aqInverseT q (r+2*j) (N-2*j))'''
r=e('(-1:K)')**'n'*q**'(n*(n-1)/2)'*P([q**'(r+1)'],'n-1')*(1-q**'(r+2*n)')/P([q],'n')
S[308]=CL('(q : K) (r n : ℕ)',[(e('(aqInverseT q r 0)'),1),(e('(aqInverseT q r (2*n+1))'),0)],'')+' ∧\n (1 ≤ n → '+f'({conj(r.req)}) → aqInverseT q r (2*n) = {r})'
S[309]=ST('(a c z q : K) (n : ℕ)',SUM('j','n',lambda j:P([a,Q('-n')],'j')*z**'j'/P([q,c],'j')),1/P([c],'n')*SUM('j','n',lambda j:P([Q('-n'),a*z*Q('-n')/c],'j')*(c*Q('n'))**'j'/P([q],'j')*P([z*Q('j-n')],'n-j')),'(hq : q ≠ 0) (hc : c ≠ 0)')
S[310]=ST('(q : K) (n : ℕ)',ISUM('r','-(n:ℤ)-1','n',lambda r:e('((-1:K)^r*q^(3*r*(r+1)/2).toNat)')*GI('2*(n:ℤ)+1','(n:ℤ)-r')),0)
S[311]=ST('(q : K) (n : ℕ)',ISUM('r','-(n:ℤ)','(n:ℤ)-1',lambda r:e('((-1:K)^r*q^(r*(3*r+1)/2).toNat)')*GI('2*(n:ℤ)-1','(n:ℤ)-1-r')),P([q**'n'],'n'),'(hn : 1 ≤ n)')
S[312]=ST('(q : K) (n : ℕ)',ISUM('r','-(n:ℤ)','n',lambda r:e('((-1:K)^r*q^(r*(3*r+1)/2).toNat)')*GI('2*(n:ℤ)','(n:ℤ)-r')),P([q**'(n+1)'],'n'))
S[313]='''{R : Type*} [CommRing R] (N : ℕ) (alpha delta u v : ℕ → R) :
 (∑ n ∈ Finset.range (N+1), alpha n * ∑ r ∈ Finset.Icc n N, delta r*u (r-n)*v (r+n)) =
 ∑ r ∈ Finset.range (N+1), delta r * ∑ n ∈ Finset.range (r+1), alpha n*u (r-n)*v (r+n)'''
S[314]=ST('(q : K) (n : ℕ)',1/P([q],'n'),1/P([q],'n')**'2'+SUM('r','n',lambda r:e('(-1:K)')**'r'*q**'(r*(3*r-1)/2)'*(1+q**'r')/(P([q],'n-r')*P([q],'n+r')),lo='1'))
S[315]=ST('(q : K) (n : ℕ)',SUM('r','n',lambda r:e('(-1:K)')**'r'*q**'(r*(r-1)/2)'*(1-q**'(2*r+1)')/((1-q)*P([q],'n-r')*P([q**'2'],'n+r'))),KD('n','0'))
u,v=vs('rho1 rho2')
def beta(N):return E(f'(baileySum a q alpha ({N}))',(f'baileyDefined a q ({N})',))
def bp(N):return 1/P([a*q/u,a*q/v],N)*SUM('k',N,lambda k:P([u,v],'k')*P([a*q/(u*v)],f'{N}-k')*(a*q/(u*v))**'k'/P([q],f'{N}-k')*beta('k'))
S[316]=ST('(a rho1 rho2 q : K) (alpha : ℕ → K) (n : ℕ)',beta('n'),SUM('j','n',lambda j:P([a*q/u,a*q/v],'j')*P([u*v/(a*q)],'n-j')*(u*v/(a*q))**'j'/(P([u,v],'n')*P([q],'n-j'))*bp('j')),'(hnz : q*a*rho1*rho2 ≠ 0)')
S[318]=ST('(q : K) (a b c : ℕ)',ISUM('k','-((min a (min b c)):ℤ)','min a (min b c)',lambda k:e('((-1:K)^k*q^(k*(3*k+1)/2).toNat)')*GI('(b:ℤ)+c','(c:ℤ)+k')*GI('(c:ℤ)+a','(a:ℤ)+k')*GI('(a:ℤ)+b','(b:ℤ)+k')),P([q],'a+b+c')/(P([q],'a')*P([q],'b')*P([q],'c')))
S[319]='''(q : K) (n : ℕ) (hn : 1 ≤ n)
 (hden : ∀ j ≤ n, poch (q^3) (q^3) j ≠ 0) (hstep : ∀ j ∈ Finset.Icc 1 n, 1-q^(3*j) ≠ 0) :
 aqSchurCoeff q 0 = 1 ∧ aqSchurCoeff q n =
 (1+q^(3*n-1))*(1+q^(3*n-2))/(1-q^(3*n))*aqSchurCoeff q (n-1)'''
S[320]=ST('(q : K) (n : ℕ)',e('(aqSchurCoeff q n)'),P([-q,-q**'2'],'n',q**'3')/P([q**'3'],'n',q**'3'),'(hstep : ∀ j ∈ Finset.Icc 1 n, 1-q^(3*j) ≠ 0) (hden : ∀ j ≤ n, poch (q^3) (q^3) j ≠ 0)')
S[321]='''(q : K) (sigma : Bool) (N : ℕ) (hN : 3 ≤ N) :
 aqF q sigma N = aqF q sigma (N-1)+q^(N-1)*aqF q sigma (N-2) ∧
 aqF q sigma 1 = 1 ∧ aqF q false 2 = 1+q ∧ aqF q true 2 = 1'''
for idx,sigma,ex,shift in [(322,'false','j*(5*j+1)','0'),(323,'true','j*(5*j-3)','1')]:
 S[idx]=ST('(q : K) (N : ℕ)',e(f'(aqG q {sigma} N)'),ISUM('j','-(N:ℤ)-2','(N:ℤ)+2',lambda j:e(f'((-1:K)^j*q^({ex}).toNat)')*GI('N',f'((N:ℤ)-5*j)/2+{shift}')))
S[324]='''(q : K) (sigma : Bool) (N : ℕ) (hN : 3 ≤ N) :
 aqG q sigma N = aqG q sigma (N-1)+q*aqG q sigma (N-2)-(q-q^(N-1))*aqG q sigma (N-3) ∧
 aqG q false 0 = 1 ∧ aqG q true 0 = 0 ∧ aqG q sigma 1 = 1 ∧
 aqG q false 2 = 1+q ∧ aqG q true 2 = 1'''
def invG():return q**'(N*N)'*e('(aqG q⁻¹ false (2*N))')
S[325]=ST('(q : K) (N : ℕ)',invG(),ISUM('k','-(N:ℤ)-2','(N:ℤ)+2',lambda k:e('(q^(5*k*k-2*k).toNat)')*(GI('2*(N:ℤ)','(N:ℤ)-5*k')-GI('2*(N:ℤ)','(N:ℤ)-5*k+2'))),'(hq : q ≠ 0)')
S[326]=ST('(q : K) (N : ℕ)',invG(),ISUM('k','-(N:ℤ)-2','(N:ℤ)+2',lambda k:e('(q^(5*k*k-2*k).toNat)')*(GI('2*(N:ℤ)-1','(N:ℤ)-5*k')-GI('2*(N:ℤ)-1','(N:ℤ)-5*k+1')))+q**'N'*ISUM('k','-(N:ℤ)-2','(N:ℤ)+2',lambda k:e('(q^(5*k*k+3*k).toNat)')*(GI('2*(N:ℤ)-1','(N:ℤ)-5*k-1')-GI('2*(N:ℤ)-1','(N:ℤ)-5*k-3'))),'(hq : q ≠ 0) (hN : 1 ≤ N)')
S[328]=CL('(q : K) (N : ℕ)',[(e('(schurD q N)'),e('(aqF q false N)')),(e('(aqF q false N)'),SUM('n','N/2',lambda n:q**'(n*n)'*G('N-n','n')))])
S[329]=ST('(q : K) (N : ℕ)',e('(aqG q false N)'),SUM('n','(N+1)/3',lambda n:SUM('j','(N+1-3*n)/2',lambda j:q**'(n*(3*n-1)/2+j)'*G('n+N+1-3*n-2*j','n')*e('(if n = 0 then (if j = 0 then (1:K) else 0) else gaussian (q^2) (n+j-1) j)'))))
S[330]=ST('(q : K) (N : ℕ)',q**'(N*(N+1))'*e('(schurD q⁻¹ (2*N+1))'),SUM('n','N',lambda n:q**'(n*(n+1))'*G('N+n+1','2*n+1')),'(hq : q ≠ 0)')
S[331]=ST('(q : K) (N : ℕ)',q**'(N*N)'*e('(schurD q⁻¹ (2*N))'),SUM('n','N',lambda n:q**'(n*n)'*G('N+n','2*n')),'(hq : q ≠ 0)')
S[332]='''(a b q : K) (n : ℕ) :
 aqX a b q (-1) = a ∧ aqX a b q 0 = b ∧
 aqX a b q (2*(n:ℤ)+1) = aqX a b q (2*(n:ℤ))+q^(2*n+1)*aqX a b q (2*(n:ℤ)-1) ∧
 aqX a b q (2*(n:ℤ)+2) = aqX a b q (2*(n:ℤ)+1)+q^(n+1)*(1+q^(n+1))*(aqX a b q (2*(n:ℤ))+aqX a b q (2*(n:ℤ)-1))'''
S[333]=ST('(q : K) (n : ℕ)',e('(aqX 1 1 q (2*(n:ℤ)-1))'),G('2*n','n')+2*SUM('j','n/2',lambda j:q**'(j*j)'*G('2*n','n-2*j'),lo='1'))
S[334]=CL('(a q : K) (alpha : ℕ → K) (n : ℕ)',[(e('(alpha 0)'),beta('0')),(e('(alpha n)'),P([a*q],'2*n')*beta('n')-SUM('r','n-1',lambda r:P([a*Q('n+r+1')],'n-r')/P([q],'n-r')*e('(alpha r)')))],'(hn : 1 ≤ n) (hq : q ≠ 0)')
S[335]='''(q t : K) (n : ℤ) (hn : 5 ≤ n) (hq : q ≠ 0) (d : ℤ → K) :
 aqOperator q (t*q^6) (n-1) (aqOperatorG q t d n) (aqOperatorG q t d (n-1))
 (aqOperatorG q t d (n-2)) (aqOperatorG q t d (n-3)) (aqOperatorG q t d (n-4)) =
 aqJ q t d (n+1)-t*q^(6*n-6)*(q^2+q^4+q^5)*aqJ q t d n +
 t^2*q^(12*n-12)*(1+q+q^3)*aqJ q t d (n-1)-t^3*q^(18*n-25)*aqJ q t d (n-2)'''
S[336]='''(a : ℕ → ℤ) (n : ℕ) (hn : 1 ≤ n) :
 eulerTransformCoeff a 0 = 1 ∧ (n:ℚ)*eulerTransformCoeff a n =
 ∑ j ∈ Finset.Icc 1 n, (divisorWeight a j : ℚ)*eulerTransformCoeff a (n-j)'''
S[337]='''(a : ℕ → ℤ) (n : ℕ) (hn : 1 ≤ n) :
 (n:ℚ)*(a n:ℚ) = (n:ℚ)*eulerTransformCoeff a n -
 (∑ d ∈ n.divisors.filter (· < n), (d:ℚ)*(a d:ℚ)) -
 ∑ j ∈ Finset.Icc 1 (n-1), (divisorWeight a j:ℚ)*eulerTransformCoeff a (n-j)'''
S[338]=CL('(q : K) (n : ℕ)',[(e('(aqRRCoeff q 0)'),1),(e('(aqRRCoeff q n)'),q**'(2*n-1)'/(1-q**'n')*e('(aqRRCoeff q (n-1))')),(q**'(2*n-1)'/(1-q**'n')*e('(aqRRCoeff q (n-1))'),q**'(n*n)'/P([q],'n'))],'(hn : 1 ≤ n) (hden : ∀ j ∈ Finset.Icc 1 n, 1-q^j ≠ 0)')
S[339]='''(q l m v : ℂ) (n : ℕ) (hn : 1 ≤ n) (hden : ∀ j ≤ n, poch q q j ≠ 0) :
 qDelta q (fun x => aqH x m v q n) l = aqH l m v q (n-1) ∧
 qDelta q (fun x => aqH l x v q n) m = aqH l m v q (n-1) ∧
 qDelta q (fun x => aqH l m x q n) v = aqH l m v q (n-1)'''
def coeff(r,s,t):return 1/(P([q],r)*P([q],s)*P([q],t))
S[340]=CL('(q : K) (r s t : ℕ)',[((1-q**'(r+1)')*coeff('r+1','s','t'),(1-q**'(s+1)')*coeff('r','s+1','t')),((1-q**'(s+1)')*coeff('r','s+1','t'),(1-q**'(t+1)')*coeff('r','s','t+1'))])
