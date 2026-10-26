from common import *
S={};q=e('q')
for idx,fn,ex in [(386,'schurD','n-1'),(387,'schurE','n')]:
 S[idx]=f'''(q : K) (n : ℕ) (hn : 2 ≤ n) :
 {fn} q n = {fn} q (n-1)+q^({ex})*{fn} q (n-2) ∧ {fn} q 0 = 1 ∧ {fn} q 1 = 1'''
S[388]=ST('(q : K) (n : ℕ)',e('(schurD q n)'),ISUM('k','-(n:ℤ)-2','(n:ℤ)+2',lambda k:e('(q^(10*k*k+k).toNat*sillsC q n (5*k))')-e('(q^(10*k*k-9*k+2).toNat*sillsC q n (5*k-2))')))
S[389]=ST('(q : K) (n : ℕ)',e('(schurE q (n-1))'),ISUM('k','-(n:ℤ)-2','(n:ℤ)+2',lambda k:e('(q^(10*k*k+3*k).toNat*sillsC q n (5*k+1))')-e('(q^(10*k*k-7*k+1).toNat*sillsC q n (5*k-2))')),'(hn : 1 ≤ n)')
for idx,fn,ex,deg,midsum,up,e1,l1,e2,l2 in [
 (390,'schurD','m*(m+1)','2*m+1','m*(m+1)','2*(m:ℤ)+1','15*k*k+4*k','(m:ℤ)+5*k+1','15*k*k+14*k+3','(m:ℤ)+5*k+3'),
 (391,'schurE','m*(m+1)','2*m','m*(m+1)','2*(m:ℤ)+1','15*k*k+2*k','(m:ℤ)+5*k+1','15*k*k+8*k+1','(m:ℤ)+5*k+2'),
 (392,'schurE','m*(m+2)','2*m+1','m*(m+2)','2*(m:ℤ)+2','15*k*k+7*k','(m:ℤ)+5*k+2','15*k*k+13*k+2','(m:ℤ)+5*k+3')]:
 left=q**f'({ex})'*e(f'({fn} q⁻¹ ({deg}))')
 middle=SUM('j','m',lambda j:q**('(j*(j+2))'if idx==392 else'(j*(j+1))')*G('m+j'if idx==391 else'm+j+1','2*j'if idx==391 else'2*j+1'))
 right=ISUM('k','-(m:ℤ)-2','(m:ℤ)+2',lambda k:e(f'(q^({e1}).toNat)')*GI(up,l1)-e(f'(q^({e2}).toNat)')*GI(up,l2))
 S[idx]=CL('(q : K) (m : ℕ)',[(left,middle),(middle,right)],'(hq : q ≠ 0)')
S[393]='''(q : K) (n : ℕ) :
 sillsB q (n+2) = (q^(2*n+3)+q-q^(n+2)+1)*sillsB q (n+1)-q*(1-q^(n+1))*sillsB q n ∧
 sillsB q 0 = 1 ∧ sillsB q 1 = 1+q'''
S[394]=ST('(q : K) (n : ℕ)',SUM('k','n',lambda k:q**'(k*k)'*G('n','k')),ISUM('k','-(n:ℤ)-1','(n:ℤ)+1',lambda k:e('((-1:K)^k*q^(k*(5*k+1)/2).toNat)')*GI('2*(n:ℤ)','(n:ℤ)+2*k')))
S[395]='''(q : K) (n : ℕ) : 0 =
 sillsB q (n+5)-(1+q+q^2+q^3+q^4+q^(2*n+7)+q^(2*n+8)+q^(2*n+9))*sillsB q (n+4) +
 q*(q^(4*n+12)+q^(2*n+10)+q^(2*n+6)+q^(2*n+7)+2*q^(2*n+8)+2*q^(2*n+9)+q^(4*n+13)+q^(4*n+14)+q^6+q^5+2*q^4+2*q^3+2*q^2+q+1)*sillsB q (n+3) -
 q^3*(q^(4*n+12)+q^(2*n+7)+q^(2*n+8)+q^(2*n+9)+q^(4*n+11)+q^(6*n+15)+q^6+q^5+2*q^4+2*q^3+2*q^2+q+1)*sillsB q (n+2) -
 q^6*(q^(5*n+10)+q^(2*n+3)+q^(2*n+4)+q^(2*n+5)+q^(5*n+8)-q^4-q^3-q^2-q-1)*sillsB q (n+1) -
 q^10*(q^(2*n+1)-1)*(q^(2*n+2)-1)*sillsB q n'''
S[396]=ST('(q : K) (n : ℕ)',e('(sillsB q n)'),e('(1/2:K)')*ISUM('k','-(n:ℤ)-1','(n:ℤ)+1',lambda k:e('((-1:K)^k*q^(k*(5*k+1)/2).toNat*(1+q^(-k)))')*GI('2*(n:ℤ)','(n:ℤ)+2*k')),'(hq : q ≠ 0) (h2 : (2:K) ≠ 0)')
S[397]=ST('(q : K) (n : ℕ)',SUM('k','n',lambda k:q**'(k*(k+1))'*G('n','k')),ISUM('k','-(n:ℤ)-2','(n:ℤ)+2',lambda k:e('((-1:K)^k*q^(k*(5*k+3)/2).toNat)')*GI('2*(n:ℤ)+1','(n:ℤ)+2*k+1')))
S[398]='''(q : K) (n : ℕ) (hn : 2 ≤ n) :
 sillsP q n = (1+q^(2*n-1))*sillsP q (n-1)+q^(2*n-2)*sillsP q (n-2) ∧
 sillsP q 0 = 1 ∧ sillsP q 1 = 1+q'''
S[399]='''(q : K) (n : ℕ) (j : ℤ) (hn : 1 ≤ n) (hq : q ≠ 0) :
 sillsT01 q true n j = sillsT01 q true (n-1) j +
 q^((n:ℤ)+j)*sillsT01 q false (n-1) (j+1)+q^((n:ℤ)-j)*sillsT01 q false (n-1) (j-1)'''
S[400]='''(q : K) (n : ℕ) (j : ℤ) (hn : 1 ≤ n) (hq : q ≠ 0) :
 sillsT01 q false n j = sillsT01 q false (n-1) (j-1)+
 q^((n:ℤ)+j)*sillsT01 q true (n-1) j+q^(2*(n:ℤ)+2*j)*sillsT01 q false (n-1) (j+1)'''
