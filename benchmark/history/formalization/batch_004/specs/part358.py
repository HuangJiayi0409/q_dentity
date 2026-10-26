from common import *
S={};a,b,c,d,ee,q,x,z,t=vs('a b c d ee q x z t')
def NP(s):return e(f'(q^(({s} : ℤ).toNat))')
S[358]=ST('(q x : K) (m : ℕ)',P([q/x,x],'m'),ISUM('j','-(m:ℤ)','m',lambda j:e('((-1:K)^j*q^(j*(j-1)/2).toNat*x^j)')*GI('2*(m:ℤ)','(m:ℤ)+j')),'(hx : x ≠ 0)')
def FF(N):
 return ISUM('k',f'-({N}:ℤ)',f'({N}:ℤ)',lambda k:e('((-1:K)^k*q^(k*(3*k+1)/2).toNat*x^(3*k))')*GI(f'2*({N}:ℤ)',f'({N}:ℤ)+k')*(1-x**'2'*e('(q^(2*k+1))'))/(P([x**'2'*q**'2'],f'(({N}:ℤ)+k).toNat')*P([x**'(-2:ℤ)'],f'(({N}:ℤ)-k).toNat')))
S[359]=ST('(x q : K) (n : ℕ)',FF('n'),(1-x**'2'*q)/P([x*q,1/x],'n'),'(hx : x ≠ 0) (hq : q ≠ 0)')
S[360]=CL('(x q : K) (n : ℕ)',[(FF('n'),FF('(n-1:ℕ)')/((1-q**'(n-1)'/x)*(1-x*q**'n'))),(FF('0'),1-x**'2'*q)],'(hn : 1 ≤ n) (hx : x ≠ 0) (hq : q ≠ 0)')
S[361]=CL('(a q : K) (n : ℕ)',[((1-q**'n')*P([a],'n')/P([q],'n'),(1-a*q**'(n-1)')*P([a],'n-1')/P([q],'n-1')),(P([a],'0')/P([q],'0'),1)],'(hn : 1 ≤ n)')
S[362]='''(q : K) (n : ℕ) (j : ℤ) (hn : 1 ≤ n) (hq : q ≠ 0) :
 sillsC q n j = q^((n:ℤ)+j)*sillsC q (n-1) (j+1)+sillsC q (n-1) j+
 q^((n:ℤ)-j)*sillsC q (n-1) (j-1) +
 (if n = 1 then 0 else q^(n-1)*(1-q^(n-1))*sillsC q (n-2) j)'''
S[363]='''(x q : K) (n : ℕ) (hn : 2 ≤ n) (hx : x ≠ 0) :
 sillsT x q n = (1+x*q^(3*n-2)+x⁻¹*q^(3*n-1))*sillsT x q (n-1)+q^(3*n-3)*(1-q^(3*n-3))*sillsT x q (n-2) ∧
 sillsT x q 0 = 1 ∧ sillsT x q 1 = 1+x*q+x⁻¹*q^2'''
def HE(N):return PH([a,b,Q('-('+N+')')],[c,Q('1-('+N+')')/t],N)
S[364]=ST('(a b c t q : K) (n : ℕ)',HE('n'),P([b,a*t],'n')/P([c,t],'n')*PH([c/b,t,Q('-n')],[a*t,Q('1-n')/b],'n'),'(hbt : b*t ≠ 0) (hq : q ≠ 0)')
S[365]=ST('(a b c t q : K) (n : ℕ)',HE('n')+(-a*b*t*Q('2*n')+a*t*Q('n+1')+b*t*Q('n+1')-c*t*Q('2*n')+c*Q('n+1')+Q('n+2')-q**'3'-q**'2')/(q**'2'*(1-c*Q('n-1'))*(1-t*Q('n-1')))*HE('n-1')+q*(1-Q('n-1'))*(1-a*t*Q('n-2'))*(1-b*t*Q('n-2'))/((1-c*Q('n-1'))*(1-t*Q('n-2'))*(1-t*Q('n-1')))*HE('n-2'),0,'(hn : 2 ≤ n) (hq : q ≠ 0) (ht : t ≠ 0)')
def WF(N):return W(a,[b,c,d,ee,Q('-('+N+')')],N,a**'2'*Q(N+'+2')/(b*c*d*ee))
den=q*(b-a*Q('n'))*(c-a*Q('n'))*(d-a*Q('n'))*(ee-a*Q('n'))
S[366]=ST('(a b c d ee q : K) (n : ℕ)',WF('n'),(a*Q('n')-1)*(Q('n')-q)*(a*Q('n')-q)*(b*c*d*ee-a**'2'*Q('n'))/den*WF('n-2')+(a*Q('n')-1)/den*(a**'3'*(q+1)*Q('3*n')+Q('n+1')*(a**'2'*q+a*(b*ee*c+b*ee*d+b*c*d+c*d*ee)+b*c*d*ee)-a*Q('2*n')*(a*q*(a+b+c+d+ee)+b*c*d*ee)-b*c*d*ee*(q+1)*q)*WF('n-1'),'(hn : 2 ≤ n) (hq : q ≠ 0)')
S[367]=ST('(q z : K) (j : ℕ)',SUM('r','j*(j+1)/2',lambda r:SUM('l','j',lambda l:e('((distinctPartitionCount j l r : ℕ) : K)')*z**'l'*q**'r')),P([-z*q],'j'))
S[368]=ST('(a q : K) (n : ℕ)',SUM('k','n',lambda k:(1-a*Q('2*k'))*P([a,Q('-n')],'k')*a**'(2*k)'*Q('(n+2)*k+4*(k*(k-1)/2)')/((1-a)*P([q],'k')*P([a*Q('n+1')],'k'))),P([a*q],'n')*SUM('k','n',lambda k:P([Q('-n')],'k')/P([q],'k')*e('(-1:K)')**'k'*a**'k'*Q('(n+1)*k+k*(k-1)/2')),'(hq : q ≠ 0)')
S[369]=ST('(x q : K) (alpha : ℕ → K) (n : ℕ)',E('(baileySum x q alpha n)',('baileyDefined x q n',)),1/P([q,x*q],'n')*SUM('r','n',lambda r:P([Q('-n')],'r')/P([x*Q('n+1')],'r')*e('(-1:K)')**'r'*Q('n*r-r*(r-1)/2')*e('(alpha r)')),'(hq : q ≠ 0)')
def AL(d,k):return E(f'(sillsAlpha x q {d} {k} r)',(f'{d} ∣ r → (1-x)*poch (q^{d}) (q^{d}) (r/{d}) ≠ 0',))
for idx,d0,e0,k0,rhs in [
 (370,1,1,2,1/P([q],'n')),
 (371,1,2,2,1/(P([q**'2'],'n',q**'2')*P([-x*q],'2*n'))),
 (373,1,2,1,e('(-1:K)')**'n'*q**'(n*n)'/(P([q**'2'],'n',q**'2')*P([-x*q],'2*n'))),
 (374,1,3,2,P([x*q],'3*n')/(P([q**'3'],'n',q**'3')*P([x**'3'*q**'3'],'2*n',q**'3'))),
 (375,2,1,2,q**'(n*(n-1)/2)'/(P([q],'n')*P([x*q],'n',q**'2'))),
 (376,2,1,3,1/(P([q],'n')*P([x*q],'n',q**'2'))),
 (377,3,1,4,P([x],'n',q**'3')/(P([q],'n')*P([x],'2*n')))]:
 S[idx]=ST('(x q : K) (n : ℕ)',BA(x**str(e0),q**str(e0),'n',lambda r:AL(d0,k0)),rhs)
S[372]=ST('(a t q : K) (n : ℕ)',ISUM('r','-(n:ℤ)','n',lambda r:GI('2*(n:ℤ)','(n:ℤ)+r')*e('(a^r*t^(r*r).toNat)')),P([-a*t,-t/a],'n'),'(ha : a ≠ 0) (ht : t^2 = q)')
S[378]=ST('(a q : K) (n : ℕ)',BA(q,q,'n',lambda r:(a**'(r+1)'+zp(a,'-r'))*q**'(r*(r+1)/2)'),P([-a],'n+1')*P([-q/a],'n')*(1-q)/P([q],'2*n+1'),'(ha : a ≠ 0)')
S[379]='''(x q : K) (n : ℕ) (hx : x ≠ 0) :
 sillsS x q (3*(n:ℤ)-1) = ∑ j ∈ Finset.Icc (-(n:ℤ)) (n:ℤ),
 x^j*q^(j*(3*j-1)/2).toNat*sillsC (q^3) n j'''
S[380]='''(x q : K) (n : ℕ) (hn : 2 ≤ n) (hx : x ≠ 0) :
 sillsS x q (3*(n:ℤ)) = sillsS x q (3*(n:ℤ)-1)+q^(3*n)*sillsS x q (3*(n:ℤ)-4) ∧
 sillsS x q (3*(n:ℤ)-1) = sillsS x q (3*(n:ℤ)-2)+x⁻¹*q^(3*n-1)*sillsS x q (3*(n:ℤ)-4) ∧
 sillsS x q (3*(n:ℤ)-2) = sillsS x q (3*(n:ℤ)-3)+x*q^(3*n-2)*sillsS x q (3*(n:ℤ)-5)'''
S[381]=ST('(q t : K) (n : ℕ)',BA(q,q,'n',lambda r:t**'(2*r*r+r)'*(1+t**'(2*r+1)')/(1+t)),1/(P([t**'3'],'n')*P([q],'n')),'(ht : t^2 = q)')
def ALS(r):
 z=q**'(r*(3*r+1)/2)'*ISUM('j','-(r:ℤ)','r',lambda j:e('((-1:K)^j*q^(-j*j))'))-q**'(r*(3*r-1)/2)'*ISUM('j','-(r:ℤ)+1','(r:ℤ)-1',lambda j:e('((-1:K)^j*q^(-j*j))'))
 return E(f'(if r = 0 then 1 else {z})',z.req)
S[382]=ST('(q : K) (n : ℕ)',BA(e(1),q,'n',ALS),1/P([-q],'n'),'(hq : q ≠ 0)')
u,v=vs('rho1 rho2')
S[383]=ST('(x rho1 rho2 q : K) (n : ℕ)',BA(x,q,'n',lambda r:P([u,v],'r')*(x*q/(u*v))**'r'/P([x*q/u,x*q/v],'r')*AL(1,2)),1/P([x*q/u,x*q/v],'n')*SUM('j','n',lambda j:P([u,v],'j')*P([x*q/(u*v)],'n-j')*(x*q/(u*v))**'j'/(P([q],'j')*P([q],'n-j'))),'(hrho : rho1*rho2 ≠ 0)')
S[384]=ST('(x q : K) (n : ℕ)',BA(x,q,'n',lambda r:e('(-1:K)')**'r'*x**'(2*r)'*q**'(r*(5*r-1)/2)'*(1-x*q**'(2*r)')*P([x],'r')/((1-x)*P([q],'r'))),SUM('j','n',lambda j:x**'j'*q**'(j*j)'/(P([q],'j')*P([q],'n-j'))))
S[385]=ST('(x q : K) (n : ℕ)',BA(x,q,'n',lambda r:e('(-1:K)')**'r'*q**'(r*r)'*(1-x*q**'(2*r)')*P([x**'2'],'r',q**'2')/((1-x)*P([q**'2'],'r',q**'2'))),1/P([q**'2'],'n',q**'2'))
