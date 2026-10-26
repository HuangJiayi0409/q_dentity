from common import *
S={};a,b,c,d,q,t,z,v,A,B,U,V,p,r,s,lam,mu=vs('a b c d q t z v A B U V p r s lam mu');ee=e('ee');f=e('f')
def put(i,ps,l,rr,h=''):S[i]=statement(ps,l,rr,h)
put(201,'(b c t q : K) (N x : ℕ)',SUM('n','N',lambda n:P([Q('-N'),b*q],'n')/P([q,Q('-N')/c],'n')*PH([Q('-n'),Q('-x'),b*c*Q('x+1')],[Q('-N'),b*q],'min n x')*t**'n'),PH([Q('x-N'),b*Q('x+1')],[Q('-N')/c],'N-x',t*Q('-x'))*P([b*c*q*t],'x'),'(hx : x ≤ N) (hc : c ≠ 0)')
put(202,'(alpha beta z q : K) (n : ℕ)',e('(associatedUltra z alpha beta q n)'),SUM('k','n',lambda k:(1-e('alpha'))/(1-e('alpha')*Q('k'))*e('beta')**'k'*UL(z,q/e('beta'),'k')*UL(z,e('beta'),'n-k')),'(hnz : alpha*beta*z ≠ 0) (hrec : ∀ j < n, 1-alpha*q^(j+1) ≠ 0 ∧ 1-alpha*beta*q^j ≠ 0)')
put(203,'(z s q : K) (n : ℕ)',SUM('k','n',lambda k:e('(gaussian (q^2) n k)')*zp(z,'n-2*k')),AW(z,s,-s,e(0),e(0),'n'),'(hz : z ≠ 0) (hs : s^2 = q)')
def RN(z,n):return PH([Q('-('+n+')'),a*b*c*d*Q(n+'-1'),a*z,a/z],[a*b,a*c,a*d],n)
left=SUM('n','N',lambda n:P([Q('-N'),U*V*Q('N-1')],'n')*(1-a*b*c*d*Q('2*n-1'))*P([a*b*c*d/q,a*b,a*c,-a*b],'n')*Q('n*(n+1)/2')*(d/a)**'n'/(P([U,-V],'n')*(1-a*b*c*d/q)*P([q,b*d],'n')*P([a*b*c*d],'2*n'))*PH([Q('n-N'),U*V*Q('n+N-1'),a*b*Q('n'),-c*d*Q('n')],[a*b*c*d*Q('2*n'),U*Q('n'),-V*Q('n')],'N-n')*RN(z,'n')*RN(v,'n'))
right=e('(-1:K)')**'N'*P([-U,V],'N')/P([U,-V],'N')*SUM('m','N',lambda m:P([Q('-N'),U*V*Q('N-1'),-a*b,d*z,d/z,d*v,d/v],'m')*Q('m')/P([q,a*d,a*d,b*d,-U,V,d/a],'m')*W(a*Q('-m')/d,[Q('1-m')/(b*d),Q('1-m')/(c*d),Q('-m'),a*z,a/z,a*v,a/v],'m',b*c*q/(a*d)))
put(204,'(a b c d U V z v q : K) (N : ℕ)',left,right,'(hnz : U*V ≠ 0)')
def J(z,A,B,n):return P([A*q,-B*q],n)/P([q,-q],n)*PH([Q('-('+n+')'),A*B*Q(n+'+1'),s*z,s/z],[A*q,-B*q,-q],n)
put(205,'(A B U V s z q : K) (m : ℕ)',J(z,A,B,'m'),SUM('n','m',lambda n:P([A*q,-B*q],'m')*P([U*V*q,-q],'n')*P([A*B*Q('m+1')],'n')*Q('n*(n-m)')/(P([-q],'m')*P([U*V*q],'2*n')*P([q],'m-n')*P([A*q,-B*q],'n'))*PH([Q('n-m'),A*B*Q('n+m+1'),U*Q('n+1'),-V*Q('n+1')],[U*V*Q('2*n+2'),A*Q('n+1'),-B*Q('n+1')],'m-n')*J(z,U,V,'n')),'(hs : s^2 = q) (hz : z ≠ 0) (hnz : A*B*U*V ≠ 0)')
put(206,'(a b c d ee q : K) (n : ℕ)',SUM('j','n',lambda j:SUM('k','n-j',lambda k:P([Q('-n')],'j+k')*P([a/c,c/d,c/ee],'j')*P([c/a,b/d,b/ee],'k')*Q('j+k')/(P([b*c/(d*ee)],'j+k')*P([q,a,Q('1-n')/b],'j')*P([q,b,Q('1-n')/a],'k')))),P([c,a*b/c],'n')/P([a,b],'n'),'(hnz : a*b*c*d*ee ≠ 0)')
def UU(j):
 aa,bb,cc,dd=[e(f'({x} {j})')for x in ['a','b','c','d']]
 return (1-bb)*(1-cc)*(1-dd)*(1-aa**'2'/(bb*cc*dd))/((1-aa/bb)*(1-aa/cc)*(1-aa/dd)*(1-bb*cc*dd/aa))
def VV(j):
 aa,bb,cc,dd=[e(f'({x} {j})')for x in ['a','b','c','d']]
 return (1-aa)*(1-aa/(bb*cc))*(1-aa/(bb*dd))*(1-aa/(cc*dd))/((1-aa/(bb*cc*dd))*(1-aa/dd)*(1-aa/cc)*(1-aa/bb))
u=UU('j');vp=VV('k')
prod=lambda N:E(f'(∏ j ∈ Finset.range ({N}), {u})',(f'∀ j ∈ Finset.range ({N}), ({conj(u.req)})',))
S[207]=statement('(a b c d : ℕ → K) (n : ℕ)',SUM('k','n',lambda k:vp*prod('k')),1-prod('n+1'),'(hnz : ∀ j ≤ n, a j*b j*c j*d j ≠ 0)').replace(' (hbase : regular q)','')
# Four independently based bilateral products.
def ip(x,base):return E(f'(pochListInt {args([x])} ({base}) k)',uniq(combine([x,base])+(f'pochListIntDefined {args([x])} ({base}) k',)))
def powi(base):return E(f'(({base})^k)',e(base).req)
x=r*s*t/q**'2';y=s*t/q;zz=r*t/q;w=r*s/q
term=(1-a*d*powi(r*s*t/q))*(1-b*powi(r)/(d*powi(q)))*(1-c*powi(s)/(d*powi(q)))*(1-a*d*powi(t)/(b*c*powi(q)))/((1-a*d)*(1-b/d)*(1-c/d)*(1-a*d/(b*c)))*ip(a,x)*ip(b,r)*ip(c,s)*ip(a*d**'2'/(b*c),t)*powi(q)/(ip(d*q,q)*ip(a*d*s*t/(b*q),y)*ip(a*d*r*t/(c*q),zz)*ip(b*c*r*s/(d*q),w))
l=E(f'(∑ k ∈ Finset.Icc (-(m:ℤ)) (n:ℤ), {term})',(f'∀ k ∈ Finset.Icc (-(m:ℤ)) (n:ℤ), ({conj(term.req)})',))
rr=(1-a)*(1-b)*(1-c)*(1-a*d**'2'/(b*c))/(d*(1-a*d)*(1-b/d)*(1-c/d)*(1-a*d/(b*c)))*(P([a*x],'n',x)*P([b*r],'n',r)*P([c*s],'n',s)*P([a*d**'2'*t/(b*c)],'n',t)/(P([d*q],'n')*P([a*d*s*t/(b*q)],'n',y)*P([a*d*r*t/(c*q)],'n',zz)*P([b*c*r*s/(d*q)],'n',w))-P([c/(a*d)],'m+1',zz)*P([d/(b*c)],'m+1',w)*P([1/d],'m+1')*P([b/(a*d)],'m+1',y)/(P([1/c],'m+1',s)*P([b*c/(a*d**'2')],'m+1',t)*P([1/a],'m+1',x)*P([1/b],'m+1',r)))
put(208,'(a b c d r s t q : K) (m n : ℕ)',l,rr,'(hnz : a*b*c*d*r*s*t*q ≠ 0) (hr : regular r) (hs : regular s) (ht : regular t)')
put(212,'(a b c d ee f q : K) (n : ℕ)',SUM('k','n',lambda k:(1-a*Q('3*k'))/(1-a)*P([b,c,d],'k')*P([ee,f,Q('-2*n')],'k',q**'2')*Q('k')/(P([a*q**'2'/b,a*q**'2'/c,a*q**'2'/d],'k',q**'2')*P([a*q/ee,a*q/f,a*Q('2*n+1')],'k'))),P([a*q**'2',a**'2'*q**'2'/(b*c*ee),a**'2'*q**'2'/(b*d*ee),a*q**'2'/(c*d)],'n',q**'2')/P([a**'2'*q**'2'/(b*ee),a*q**'2'/c,a*q**'2'/d,a**'2'*q**'2'/(b*c*d*ee)],'n',q**'2'),'(hnz : a*b*c*d*ee*f ≠ 0) (hbal1 : b*c*d = a*q) (hbal2 : ee*f = a^2*q^(2*n+1)) (hbranch : b = a ∨ ee = a)')
put(213,'(a b c d ee q : K) (n : ℕ)',SUM('k','n',lambda k:(1-a*Q('4*k'))/(1-a)*P([b,c],'k')*P([d],'2*k')*P([ee,Q('-3*n')],'k',q**'3')*Q('k')/(P([a*q**'3'/b,a*q**'3'/c],'k',q**'3')*P([a*q/d],'2*k')*P([a*q/ee,a*Q('3*n+1')],'k'))),P([a*q**'3',a**'2'*q**'3'/(b*c*ee),a**'2'*q**'3'/(b*d*ee),a*q**'3'/(c*d)],'n',q**'3')/P([a**'2'*q**'3'/(b*ee),a*q**'3'/c,a*q**'3'/d,a**'2'*q**'3'/(b*c*d*ee)],'n',q**'3'),'(hnz : a*b*c*d*ee ≠ 0) (hbal1 : b*c*d = a*q) (hbal2 : d*ee = a^2*q^(3*n+1)) (hb : b = a)')
put(214,'(a b c d lam q : K) (n : ℕ)',W(a,[b,-b,c,-c,d*Q('n'),-d*Q('n'),Q('-n'),-Q('-n'),q*a**'2'/lam**'2'],'n'),P([a**'2'*q**'2',d**'2'/lam**'2',b**'2'*d**'2'/a**'2',c**'2'*d**'2'/a**'2'],'n',q**'2')/P([d**'2'/a**'2',q**'2'*lam**'2',a**'2'*q**'2'/b**'2',a**'2'*q**'2'/c**'2'],'n',q**'2')*W(lam**'2',[b**'2',c**'2',d**'2'*Q('2*n'),a**'2'*q**'2'/lam**'2',Q('-2*n'),-lam**'2'/a,-lam**'2'*q/a],'n',lam**'2'*q/a**'2',q**'2'),'(hl : lam = b*c*d/(a*q)) (hnz : a*b*c*d ≠ 0)')
put(215,'(a b c d lam mu q : K) (n : ℕ)',W(a,[a**'2'/lam**'2',b,b*q,c,c*q,d*Q('n'),d*Q('n+1'),Q('1-n'),Q('-n')],'n/2',q**'2',q**'2'),P([a*q,d/lam,lam*q/b,lam*q/c],'n')/P([lam*q,d/a,a*q/b,a*q/c],'n')*W(lam,[a/lam,mu,-mu,b,c,d*Q('n'),Q('-n')],'n',-q*lam/a),'(hl : lam = b*c*d/(a*q)) (hm : mu^2 = lam^2*q/a) (hnz : a*b*c*d ≠ 0)')
