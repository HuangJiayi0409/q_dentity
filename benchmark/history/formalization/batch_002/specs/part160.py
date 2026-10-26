from common import *
a,b,c,b1,b2,b3,c1,c2,c3,q,s,z,w,beta,u,h,A,B,D,alpha,gamma,t=vs('a b c b1 b2 b3 c1 c2 c3 q s z w beta u h A B D alpha gamma t')
S={};nz=lambda names:'(hnz : ∀ v ∈ ['+names+'], v ≠ 0)'
lam=b*b3*Q('-m-1')/a
inner=lambda j:PH([Q('-j'),Q('1-m')/c,Q('1-m')/c3,lam*Q('j'),c*c3*Q('-m')/(a*c1*c2)],[Q('1-m')/c1,Q('1-m')/c2,b*Q('-m')/a,b3*Q('-m')/a],'j')
S[160]=statement('(a b b1 b2 b3 c c1 c2 c3 q : K) (n : ℕ)',FN(a,b,b1,b2,b3,'n')*FN(a,c,c1,c2,c3,'n'),SUM('m','n',lambda m:P([Q('-n'),a*Q('n'),c1,c2,q*a*b1/(b*b3),q*a*b2/(b*b3)],'m')*Q('m')/P([q,c,c3,q*a/(b*b3),q*a*c1*c2/(c*c3),q*a*b1*b2/(b*b3)],'m')*SUM('j','m',lambda j:(1-lam*Q('2*j'))/(1-lam)*P([lam,b1,b2,b*Q('-m')/a,b3*Q('-m')/a,Q('-m')],'j')/P([q,b*b3*Q('-m')/(a*b1),b*b3*Q('-m')/(a*b2),b3,b,b*b3/a],'j')*zp(b*b3*Q('m')/(b1*b2),'j')*inner(j))),nz('a,b,b1,b2,b3,c,c1,c2,c3'))
S[161]=statement('(a b b1 b2 b3 c1 c2 q : K) (n : ℕ)',FN(a,b,b1,b2,b3,'n')*FN(a,a*q/b,c1,c2,a*q/b3,'n'),SUM('m','n',lambda m:P([Q('-n'),a*Q('n'),c1,c2,q*a*b1/(b*b3),q*a*b2/(b*b3)],'m')*Q('m')/P([q,a*q/b,a*q/b3,a*q/(b*b3),q*a*b1*b2/(b*b3),b*b3*c1*c2/(a*q)],'m')*W(lam,[b1,b2,b*b3*c1/(a*q),b*b3*c2/(a*q),b*Q('-m')/a,b3*Q('-m')/a,Q('-m')],'m',a*q*q/(b1*b2*c1*c2))),nz('a,b,b1,b2,b3,c1,c2'))
mu=b1*b2*c1/q
S[162]=statement('(a b b1 b2 b3 c1 q : K) (n : ℕ)',FN(a,b,b1,b2,b3,'n')*FN(a,b,b*b3*c1/(a*q),b*b3/(b1*b2*c1),b3,'n'),P([a*q/b,a*q/b3],'n')/P([b,b3],'n')*zp(b*b3/(a*q),'n')*SUM('m','n',lambda m:P([Q('-n'),a*Q('n'),b1*c1,b2*c1,a*q/(b1*b2*c1)],'m')*Q('m')/P([q,a*q/b,a*q/b3,b1*b2*c1,b*b3/(b1*b2)],'m')*W(mu,[b1,b2,b1*b2*c1/b,b1*b2*c1/b3,b*b3*c1/(a*q),a*Q('m'),Q('-m')],'m')),nz('a,b,b1,b2,b3,c1'))
S[163]=statement('(a b q : K) (N n x y : ℕ)',HAHN('x',a,b,'N','n')*HAHN('y',a,b,'N','n'),zp(-a*q,'n')*Q('n*(n-1)/2')*P([b*q],'n')/P([a*q],'n')*SUM('m','n',lambda m:MUL0(P([Q('-n'),a*b*Q('n+1'),Q('x-N'),Q('y-N')],'m')*zp(a*Q('x+y'),'-m')/P([q,b*q,Q('-N'),Q('-N')],'m'),PH([Q('-x'),Q('-y'),Q('-m')/b,Q('-m')],[a*q,Q('N-x+1-m'),Q('N-y+1-m')],'m',a*b*Q('2*N+3')))),'(hn : n ≤ N) (hx : x ≤ N) (hy : y ≤ N) '+nz('a,b'))
def RN(z):return PH([Q('-n'),a**4*Q('n'),a*z,a/z],[a*a*s,-a*a,-a*a*s],'n')
S[164]=statement('(a z w s q : K) (n : ℕ)',RN(z)*RN(w),(1+a*a*Q('n'))/(1+a*a)*zp(-1/s,'n')*SUM('m','n',lambda m:P([Q('-n'),a**4*Q('n'),-s*z/w,-a*a*s*w/z],'m')*Q('m')/P([q,a*a*s,-a*a*s,-a*a*q],'m')*PH([Q('-m'),a*a,a*a*w*w,a*a/(z*z)],[a**4,-a*a*s*w/z,-s*Q('-m')*w/z],'m')),'(hs : s^2 = q) '+nz('a,z,w'))
S[165]=statement('(z beta q : K) (m n : ℕ)',UL(z,beta,'m')*UL(z,beta,'n'),SUM('k','min m n',lambda k:P([q],'m+n-2*k')*P([beta],'m-k')*P([beta],'n-k')*P([beta],'k')*P([beta*beta],'m+n-k')*(1-beta*Q('m+n-2*k'))/(P([beta*beta],'m+n-2*k')*P([q],'m-k')*P([q],'n-k')*P([q],'k')*P([beta*q],'m+n-k')*(1-beta))*UL(z,beta,'m+n-2*k')))
H=lambda:KH_RS(a,b,c,alpha,gamma,'N','M','x','y','r','s')
AA=lambda:KA_RS(a,b,c,alpha,gamma,'N','M','x','y','r','s')
bounds='(hNM : N ≤ M) (hx : x ≤ N) (hy : y ≤ M) '+nz('a,b,c,alpha,gamma')
S[166]=statement('(a b c alpha gamma q : K) (N M n x y : ℕ)',WR('x',a,b,c,'N','n')*WR('y',alpha,a*b/alpha,gamma,'M','n'),P([b*q,a*q/c],'n')*zp(c,'n')/P([a*q,b*c*q],'n')*SUM('r','min n (min x y)',lambda r:SUM('s','min (n-r) (N-x)',lambda s:MUL0(P([Q('-n'),a*b*Q('n+1')],'r+s')/P([Q('-N')],'r+s')*H()*Q('r+s'),AA()))),'(hn : n ≤ N) '+bounds)
def BB():
 la=a*b*Q('2*r+2*s+1')
 return SUM('j','z-r-s',lambda j:(1-la*Q('2*j'))/(1-la)*P([la,Q('r+s-N'),Q('r+s-z')],'j')/P([q,a*b*Q('N+r+s+2'),Q('r+s-K')],'j')*Q('(N-r-s)*j'))
S[167]=statement('(a b c alpha gamma q : K) (N M z x y Kcap : ℕ)',SUM('n','z',lambda n:P([Q('-z')],'n')/P([Q('-Kcap')],'n')*HN('n',a,b,c,'N')*WR('x',a,b,c,'N','n')*WR('y',alpha,a*b/alpha,gamma,'M','n')),HN('0',a,b,c,'N')*SUM('r','min z (min x y)',lambda r:SUM('s','min (z-r) (N-x)',lambda s:MUL0(P([Q('-z')],'r+s')*P([a*b*q*q],'2*r+2*s')*zp(e('(-1:K)'),'r+s')*Q('(r+s)*(2*N-r-s+1)/2')/P([Q('-Kcap'),a*b*Q('N+2')],'r+s')*H(),AA()*BB()))),'(hzN : z ≤ N) (hzK : z ≤ Kcap) '+bounds).replace('(K : ℤ)','(Kcap : ℤ)').replace('q^(r+s-K)','q^(r+s-(Kcap : ℤ))')
S[168]=statement('(a w q : K) (n : ℕ)',SUM('k','n',lambda k:(1-a*Q('2*k'))/(1-a)*P([a,Q('-n')],'k')/P([q,w],'k')*zp(w/(a*q),'k')),P([w*Q('-n-1')/a],'n')/P([w],'n')*PH([Q('-n'),Q('1-n')],[w*Q('-n')/a],'n-1',w*Q('n')),nz('a,w'))
def CC():
 la=a*b*Q('2*r+2*s+1')
 return SUM('j','N-r-s',lambda j:(1-la*Q('2*j'))/(1-la)*P([la,Q('r+s-N')],'j')/P([q,a*b*Q('N+r+s+2')],'j')*zp(t*Q('N-r-s'),'j'))
S[169]=statement('(a b c alpha gamma t q : K) (N M x y : ℕ)',SUM('n','N',lambda n:zp(t,'n')*HN('n',a,b,c,'N')*WR('x',a,b,c,'N','n')*WR('y',alpha,a*b/alpha,gamma,'M','n')),HN('0',a,b,c,'N')*SUM('r','min x y',lambda r:SUM('s','N-x',lambda s:MUL0(P([a*b*q*q],'2*r+2*s')/P([a*b*Q('N+2')],'r+s')*H()*zp(-t,'r+s')*Q('(r+s)*(2*N-r-s+1)/2'),AA()*CC()))),bounds)
S[170]=statement('(beta u s z q : K) (n : ℕ)',PH([Q('-n'),beta*beta*Q('n'),u*z,u/z],[beta*s,-beta*s,-beta],'n')**2,PH([Q('-n'),beta*beta*Q('n'),beta,beta*z*z,beta/(z*z)],[beta*beta,beta*s,-beta*s,-beta],'n'),'(hu : u^2 = beta) (hs : s^2 = q) '+nz('beta,z'))
left=PH([Q('-n'),A*Q('n'),B,B*z*z,B/(z*z)],[B*B,h*h*s,-h*h*s,-B],'n')
params='(A B h u s z q : K) (n : ℕ)';extra='(hA : A = h^4) (hB : B = u^2) (hs : s^2 = q) '+nz('A,B,z')
S[171]=statement(params,left,SUM('j','n',lambda j:P([Q('-n'),A*Q('n'),B*s,-B*s],'j')*zp(e('(-1:K)'),'j')*Q('j*(j+1)/2')/P([q,h*h*s,-h*h*s,B*B*Q('j')],'j')*PH([Q('j-n'),A*Q('j+n'),B*s*Q('j'),-B*s*Q('j')],[B*B*Q('2*j+1'),h*h*s*Q('j'),-h*h*s*Q('j')],'n-j')*PH([Q('-j'),B*B*Q('j'),B,B*z*z,B/(z*z)],[B*B,B*s,-B*s,-B],'j')),extra)
def term172(k):
 j='(n-2*k)';J='(n-2*k)'
 return zp(e('(-1:K)'),'n')*P([Q('-n'),A*Q('n'),B*s,-B*s],j)*P([q,A/(B*B)],'k',q*q)*zp(B,'2*k')*Q('2*k*(n-2*k)+k+(n-2*k)*(n-2*k+1)/2')/(P([q,h*h*s,-h*h*s,B*B*Q(J)],j)*P([A*Q('2*'+J+'+1'),B*B*Q('2*'+J+'+2')],'k',q*q))*PH([Q('-'+J),B*B*Q(J),u*z,u/z],[B*s,-B*s,-B],j)**2
S[172]=statement(params,left,SUM('k','n/2',term172),extra)
S[173]=statement(params,PH([Q('-n'),A*Q('n'),B,-B,h*h*z*z,h*h/(z*z)],[B*B,h*h*s,-h*h*s,-h*h,-h*h],'n'),SUM('k','n/2',lambda k:P([Q('-n'),A*Q('n'),h*h,h*h*z*z,h*h/(z*z)],'2*k')*P([q,A/(B*B)],'k',q*q)*Q('2*k*k+k')*zp(B,'2*k')/(P([q,h*h*s,-h*h*s,-h*h,A*Q('2*k-1')],'2*k')*P([A,B*B*q],'k',q*q))*PH([Q('2*k-n'),A*Q('n+2*k'),h*Q('k')*z,h*Q('k')/z],[h*h*s*Q('2*k'),-h*h*s*Q('2*k'),-h*h*Q('2*k')],'n-2*k')**2),extra)
# All nonintegral q-powers use a single explicit logarithm L.
def EXP(s):return e('(Complex.exp (L*('+s+')))')
qa1=EXP('(alpha+1)/2');qa2=EXP('(alpha+2)/2');qa3=EXP('(alpha+3)/2')
S[174]=statement('(alpha L z w q : ℂ) (n : ℕ)',PH([Q('-n'),EXP('(n:ℂ)+alpha+2'),qa1,qa1*z*z,qa1/(z*z),qa2*w*w,qa2/(w*w)],[EXP('alpha+1'),qa3,-qa3,-qa2,-qa2,-qa1],'n'),SUM('j','n',lambda j:P([Q('-n'),EXP('(n:ℂ)+alpha+2'),qa2,qa2*w*w,qa2/(w*w)],'j')*zp(e('(-1:ℂ)'),'j')*Q('j+j*(j-1)/2')/P([q,qa3,-qa3,-qa2,EXP('(j:ℂ)+alpha+1')],'j')*(P([q],'j')*P([q],'n-j')*EXP('((n:ℂ)*(alpha+2)+2*(j:ℂ)*((n:ℂ)-j)-j)/4')/(P([EXP('alpha+1')],'j')*P([EXP('2*(j:ℂ)+alpha+2')],'n-j'))*UL(z,qa1,'j')*UL(w,EXP('(j:ℂ)+(alpha+2)/2'),'n-j'))**2),'(hL : Complex.exp L = q) (hz : z ≠ 0) (hw : w ≠ 0)')
S[175]=statement('(A B D h u s z q : K) (n : ℕ)',PH([Q('-n'),A*Q('n'),h*h,B,h*h*z*z,h*h/(z*z)],[h*h*s,D,A*B/D,-h*h*s,-h*h],'n'),SUM('j','n',lambda j:P([Q('-n'),A*Q('n'),h*h,A/D,D/B,h*h*z*z,h*h/(z*z)],'j')*zp(e('(-1:K)'),'j')*zp(B,'j')*Q('j*(j+1)/2')/P([q,h*h*s,-h*h*s,-h*h,A*Q('j-1'),D,A*B/D],'j')*PH([Q('j-n'),A*Q('j+n'),h*zp(s,'j')*z,h*zp(s,'j')/z],[h*h*s*Q('j'),-h*h*s*Q('j'),-h*h*Q('j')],'n-j')**2),extra+' (hD : D ≠ 0)')
