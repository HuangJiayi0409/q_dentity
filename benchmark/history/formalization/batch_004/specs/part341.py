from common import *
S={};a,b,q,t,x,u,s,zeta=vs('a b q t x u s zeta')
def prodterm(term,hi):return E(f'(∏ j ∈ Finset.range ({hi}), {term})',()if not term.req else(f'∀ j ∈ Finset.range ({hi}), ({conj(term.req)})',))
S[341]=ST('(q : K) (n a b : ℕ)',e('((bnProduct q n a b).coeff 0)'),P([q],'n*b')/P([q],'b')**'n'*prodterm(P([q],'2*a+2*j*b')*P([q],'2*j*b')/(P([q],'a+(n+j-1)*b')*P([q],'a+j*b')),'n'),'(hn : 1 ≤ n)')
S[342]=ST('(a q : K) (n : ℕ)',P([a*q],'n'),(1-a*q)*P([a*q**'2'],'n-1'),'(hn : 1 ≤ n)')
def C(n):return E(f'(fineC a b q ({n}))',(f'poch (b*q) q ({n}) ≠ 0',))
S[343]=ST('(a b q : K) (n : ℕ)',(1-b*q**'(n+1)')*C('n+1'),(1-a*q**'(n+1)')*C('n'))
S[344]=ST('(a b q : K) (n : ℕ)',C('n')-C('n-1'),(b-a)*q**'n'/(1-a*q**'n')*C('n'),'(hn : 1 ≤ n)')
S[345]=CL('(a b t q : K) (n : ℕ)',[(e('((fineHG a b t q (n+1)).1)'),P([b/a],'n+1')/(P([b*q],'n+1')*P([b/(a*t)],'n+1'))),(e('((fineHG a b t q (n+1)).2)'),-(b/(a*t))/(1-b/(a*t))*SUM('j','n',lambda j:P([b/a],'j')*q**'j'/(P([b*q],'j')*P([b*q/(a*t)],'j'))))],'(hat : a*t ≠ 0) (hrec : ∀ j ≤ n, (1-b*q^(j+1))*(b*q^j-a*t) ≠ 0)')
def A(N):return E(f'(fineA a b q ({N}))',(f'∀ j ≤ ({N}), poch q q j ≠ 0 ∧ poch (b*q) q j ≠ 0',))
S[346]=ST('(a b q : K) (N : ℕ)',A('N'),SUM('k','N',lambda k:e('(-1:K)')**'k'*P([a*q],'N-k')*q**'(k*(k-1)/2)'/(P([b*q],'N-k')*P([q],'k'))))
S[347]=ST('(a b q : K) (n : ℕ)',(1-b*q**'n')*A('n'),-a*q**'n'*A('n-1')+e('(-1:K)')**'n'*(1-b)*q**'(n*(n+1)/2)'/P([q],'n'),'(hn : 1 ≤ n)')
S[348]=ST('(a b q : K) (N : ℕ)',A('N'),(-a)**'N'*q**'(N*(N+1)/2)'/P([b*q],'N')*SUM('j','N',lambda j:P([b],'j')*zp(a,'-j')/P([q],'j')),'(ha : a ≠ 0)')
def H(u,n):return e(f'(rogersSzego ({u}) q ({n}))')
S[349]=ST('(u q : K) (n : ℕ)',H(u*q,'n')-H(u,'n')+u*(1-q**'n')*H(u,'n-1'),0,'(hn : 1 ≤ n)')
S[350]=ST('(u q : K) (n : ℕ)',q**'n'*H(u,'n')-H(u*q,'n')+(1-q**'n')*H(u*q,'n-1'),0,'(hn : 1 ≤ n)')
S[351]=ST('(u q : K) (n : ℕ)',H(e('u⁻¹'),'n'),zp(u,'-n')*H(u,'n'),'(hu : u ≠ 0)')
S[352]=ST('(s q : K) (n : ℕ)',H(e('s⁻¹'),'n'),zp(s,'-n')*H(s,'n'),'(hs : s^2 = q) (hq : q ≠ 0)')
S[353]='''(q zeta : ℂ) (k n : ℕ) (hk : 0 < k) (hz : IsPrimitiveRoot zeta k)
 (hden : ∀ j ≤ n, poch q q j ≠ 0)
 (hout : k ∣ n → poch (q^k) (q^k) (n/k) ≠ 0) :
 fineQ q (fun i : Fin k => zeta^i.val) n =
 if k ∣ n then poch q q n/poch (q^k) (q^k) (n/k) else 0'''
S[354]='''(q s : K) (p n : ℕ) (hp : 0 < p) (hs : s^p = q)
 (hden : ∀ j ≤ n, poch q q j ≠ 0) (hout : poch s s n ≠ 0) :
 fineQ q (fun i : Fin p => s^i.val) n = poch q q n/poch s s n'''
S[355]='''(q s zeta : ℂ) (k p n m : ℕ) (hk : 0 < k) (hp : 0 < p)
 (hs : s^p = q) (hz : IsPrimitiveRoot zeta k)
 (hden : ∀ j ≤ max m (n*k), poch q q j ≠ 0) (hout : poch (s^k) (s^k) n ≠ 0) :
 (¬ k ∣ m → fineQ q (fun i : Fin p × Fin k => s^i.1.val*zeta^i.2.val) m = 0) ∧
 fineQ q (fun i : Fin p × Fin k => s^i.1.val*zeta^i.2.val) (n*k) = poch q q (n*k)/poch (s^k) (s^k) n'''
S[356]='''(a q s zeta : ℂ) (n k p : ℕ) (hk : 0 < k) (hp : 0 < p)
 (hs : s^p = q) (hz : IsPrimitiveRoot zeta k) :
 (∏ r : Fin p, ∏ j : Fin k, poch (a*q*zeta^j.val*s^r.val) q n) =
 poch ((a*q)^k) (s^k) (n*p)'''
S[357]='''(q : K) (L r : ℕ) (hL : 1 ≤ L) (hr : r < L) :
 (∑ l ∈ shellPartitions L r, q^(∑ i, (l i).val)) =
 q^(2*L-r-1)*gaussian q (2*L-r-2) (L-1)'''
