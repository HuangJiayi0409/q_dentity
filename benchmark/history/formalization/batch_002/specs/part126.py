from common import *
a,b,c,d,q,t,z,beta,s,u,alpha,gamma=vs('a b c d q t z beta s u alpha gamma')
S={}
nz=lambda names:'(hnz : ∀ v ∈ ['+names+'], v ≠ 0)'
def recA():return (1-a*b*Q('n+1'))*(1-a*Q('n+1'))*(1-c*Q('n+1'))*(1-b*d*Q('n+1'))/((1-a*b*Q('2*n+1'))*(1-a*b*Q('2*n+2')))
def recC():return c*d*q*(1-Q('n'))*(1-b*Q('n'))*(1-a*b*Q('n')/c)*(1-a*Q('n')/d)/((1-a*b*Q('2*n'))*(1-a*b*Q('2*n+1')))
S[126]=statement('(t a b c d q : K) (n : ℕ)',(t+c*d*q/t-1-c*d*q)*RC(t,a,b,c,d,'n'),MUL0(recA(),RC(t,a,b,c,d,'n+1')-RC(t,a,b,c,d,'n'))-MUL0(recC(),RC(t,a,b,c,d,'n')-PREV(RC(t,a,b,c,d,'n-1'))),nz('t,c,d'))
S[127]=statement('(t a b c d q : K) (n : ℕ)',RC(t,a,b,c,d,'n')-RC(t,a,b,c,d,'n-1'),-Q('1-n')*(1-a*b*Q('2*n'))*(1-t)*(1-c*d*q/t)/((1-a*q)*(1-c*q)*(1-b*d*q))*PH([Q('1-n'),a*b*Q('n+1'),q*t,c*d*q*q/t],[a*q*q,c*q*q,b*d*q*q],'n-1'),'(hn : 1 ≤ n) '+nz('t,c,d'))
S[128]=claims('(a b c q : K) (N m n x y : ℕ)',[(SUM('j','N',lambda j:RHO('j',a,b,c,'N')*WR('j',a,b,c,'N','m')*WR('j',a,b,c,'N','n')),KD('m','n')/HN('n',a,b,c,'N')),(SUM('j','N',lambda j:HN('j',a,b,c,'N')*WR('x',a,b,c,'N','j')*WR('y',a,b,c,'N','j')),KD('x','y')/RHO('x',a,b,c,'N'))], '(hm : m ≤ N) (hn : n ≤ N) (hx : x ≤ N) (hy : y ≤ N) '+nz('a,b,c'))
S[129]=statement('(a b q : K) (N m n : ℕ)',SUM('x','N',lambda x:HAHN('x',a,b,'N','m')*HAHN('x',a,b,'N','n')*P([a*q],'x')*P([b*q],'N-x')/(P([q],'x')*P([q],'N-x'))*zp(a*q,'-x')),P([a*b*q*q],'N')*zp(a*q,'-N')/P([q],'N')*P([q],'n')*(1-a*b*q)*P([b*q,a*b*Q('N+2')],'n')/(P([a*b*q],'n')*(1-a*b*Q('2*n+1'))*P([a*q,Q('-N')],'n'))*zp(-a*q,'n')*Q('n*(n-1)/2-N*n')*KD('m','n'),'(hm : m ≤ N) (hn : n ≤ N) (ha : a ≠ 0)')
S[130]=statement('(b c q : K) (N m n : ℕ)',SUM('x','N',lambda x:DH('x',b,c,'N','m')*DH('x',b,c,'N','n')*P([c*Q('-N'),b*c*q,Q('-N')],'x')*(1-c*Q('2*x-N'))/(P([q,Q('-N')/b,c*q],'x')*(1-c*Q('-N')))*Q('N*x-x*(x-1)/2')*zp(-b*c*q,'-x')),P([1/c],'N')*P([q,b*q],'n')/(P([b*q],'N')*P([b*c*q,Q('-N')],'n'))*zp(c*Q('-N'),'n')*KD('m','n'),'(hm : m ≤ N) (hn : n ≤ N) '+nz('b,c'))
A=-Q('n')*(1-a*b*Q('n+1'))*(1-a*Q('n+1'))/((1-a*b*Q('2*n+1'))*(1-a*b*Q('2*n+2')))
C=-a*Q('n')*(1-Q('n'))*(1-b*Q('n'))/((1-a*b*Q('2*n'))*(1-a*b*Q('2*n+1')))
x=e('x')
S[131]=statement('(x a b q : K) (n : ℕ)',x*LJ(x,a,b,'n'),MUL0(A,LJ(x,a,b,'n+1')-LJ(x,a,b,'n'))-MUL0(C,LJ(x,a,b,'n')-PREV(LJ(x,a,b,'n-1'))))
S[132]=statement('(a b q : K) (m n : ℕ)',SUM('j','m',lambda j:SUM('k','n',lambda k:P([Q('-m'),a*b*Q('m+1')],'j')*P([Q('-n'),a*b*Q('n+1')],'k')*Q('j+k')/(P([q],'j')*P([q],'k')*P([a*b*q*q],'j+k')))),P([Q('-n'),a*b*Q('n+1')],'n')/P([a*b*q*q],'2*n')*zp(a*b*Q('n+2'),'n')*KD('m','n'),'(hmn : m ≤ n)')
S[133]=statement('(z beta u s q : K) (n : ℕ)',UL(z,beta,'n'),P([beta*beta],'n')/P([q],'n')*zp(u,'-n')*PH([Q('-n'),beta*beta*Q('n'),u*z,u/z],[beta*s,-beta,-beta*s],'n'),'(hu : u^2 = beta) (hs : s^2 = q) '+nz('beta,z'))
A=(1-a*b*c*d*Q('n-1'))/((1-a*b*c*d*Q('2*n-1'))*(1-a*b*c*d*Q('2*n')))
C=(1-Q('n'))*e(1)
for v in [a*b,a*c,a*d,b*c,b*d,c*d]:C=C*(1-v*Q('n-1'))
C=C/((1-a*b*c*d*Q('2*n-2'))*(1-a*b*c*d*Q('2*n-1')))
B=a+1/a-A/a*(1-a*b*Q('n'))*(1-a*c*Q('n'))*(1-a*d*Q('n'))-a*C/((1-a*b*Q('n-1'))*(1-a*c*Q('n-1'))*(1-a*d*Q('n-1')))
S[134]=statement('(z a b c d q : K) (n : ℕ)',(z+1/z)*AW(z,a,b,c,d,'n'),MUL0(A,AW(z,a,b,c,d,'n+1'))+B*AW(z,a,b,c,d,'n')+MUL0(C,PREV(AW(z,a,b,c,d,'n-1'))),nz('a,z'))
S[135]=statement('(a b c d q : K) (m n : ℕ)',SUM('j','m',lambda j:P([Q('-m'),a*b*c*d*Q('m-1')],'j')*Q('j')/P([q,a*b*c*d],'j')*PH([Q('-n'),a*b*c*d*Q('n-1'),a*b*Q('j')],[a*b*c*d*Q('j'),a*b],'n')),P([q,c*d],'n')*(1-a*b*c*d/q)/(P([a*b*c*d/q,a*b],'n')*(1-a*b*c*d*Q('2*n-1')))*zp(a*b,'n')*KD('m','n'),'(hnm : n ≤ m)')
S[136]=statement('(z beta s q : K) (n : ℕ)',UL(z,beta,'2*n'),P([beta,beta*s],'n')/P([q,s],'n')*zp(s,'-n')*PH([Q('-n'),beta*Q('n'),s*z*z,s/(z*z)],[beta*s,-s,-q],'n'),'(hs : s^2 = q) '+nz('beta,z'))
S[137]=statement('(z beta s q : K) [CharZero K] (n : ℕ)',UL(z,beta,'2*n+1'),(z+1/z)/2*P([beta,e(-1)],'n+1')/P([s,-s],'n+1')*zp(s,'-n')*P([beta*s,-q*s],'n')/P([q,-q],'n')*PH([Q('-n'),beta*Q('n+1'),s*z*z,s/(z*z)],[beta*s,-q*s,-q],'n'),'(hs : s^2 = q) '+nz('beta,z'))
S[138]=statement('(z alpha beta gamma a b c d q : K) (n : ℕ)',AW(z,alpha,beta,gamma,d,'n'),SUM('k','n',lambda k:P([alpha*d,beta*d,gamma*d,q],'n')*P([alpha*beta*gamma*d*Q('n-1')],'k')*Q('k*k-n*k')*zp(d,'k-n')/(P([alpha*d,beta*d,gamma*d,q,a*b*c*d*Q('k-1')],'k')*P([q],'n-k'))*PH([Q('k-n'),alpha*beta*gamma*d*Q('n+k-1'),a*d*Q('k'),b*d*Q('k'),c*d*Q('k')],[a*b*c*d*Q('2*k'),alpha*d*Q('k'),beta*d*Q('k'),gamma*d*Q('k')],'n-k')*AW(z,a,b,c,d,'k')),nz('alpha,a,d,z'))
S[139]=statement('(z alpha a b c d q : K) (n : ℕ)',AW(z,alpha,b,c,d,'n'),SUM('k','n',lambda k:P([alpha/a],'n-k')*P([alpha*b*c*d*Q('n-1')],'k')*P([q,b*c,b*d,c*d],'n')*zp(a,'n-k')/(P([q,b*c,b*d,c*d],'k')*P([a*b*c*d*Q('k-1')],'k')*P([q,a*b*c*d*Q('2*k')],'n-k'))*AW(z,a,b,c,d,'k')),nz('a,alpha,z'))
S[140]=statement('(z beta gamma q : K) (n : ℕ)',UL(z,gamma,'n'),SUM('k','n/2',lambda k:zp(beta,'k')*P([gamma/beta],'k')*P([gamma],'n-k')*(1-beta*Q('n-2*k'))/(P([q],'k')*P([beta*q],'n-k')*(1-beta))*UL(z,beta,'n-2*k')),nz('beta,z'))
def DIFF(fn):
    lhs=fn(s*z);rhs=fn(z/s);return (lhs-rhs)/((s-1/s)*(z-1/z)/2)
S[141]=statement('(z a s q : K) [CharZero K] (n : ℕ)',DIFF(lambda t:P([a*t,a/t],'n')),-2*a*(1-Q('n'))/(1-q)*P([a*s*z,a*s/z],'n-1'),'(hn : 1 ≤ n) (hs : s^2 = q) (hz : z ≠ 0)')
def AZ(z):return (1-a*z)*(1-b*z)*(1-c*z)*(1-d*z)/((1-z*z)*(1-q*z*z))
S[142]=statement('(z a b c d q : K) (n : ℕ)',Q('-n')*(1-Q('n'))*(1-a*b*c*d*Q('n-1'))*AW(z,a,b,c,d,'n'),AZ(z)*(AW(q*z,a,b,c,d,'n')-AW(z,a,b,c,d,'n'))+AZ(1/z)*(AW(z/q,a,b,c,d,'n')-AW(z,a,b,c,d,'n')),nz('a,z'))
S[143]=statement('(z a b c d s q : K) [CharZero K] (n : ℕ)',DIFF(lambda t:AW(t,a,b,c,d,'n')),2*zp(s,'1-n')*(1-Q('n'))*(1-a*b*c*d*Q('n-1'))/(1-q)*AW(z,a*s,b*s,c*s,d*s,'n-1'),'(hn : 1 ≤ n) (hs : s^2 = q) '+nz('a,z'))
f,g=vs('f g');ee=e('ee')
A=b*(1-b)*(a*q-b)*(a-ee)*(a-f)*(a-g)
C=-a*(1-a)*(a-b*q)*(ee-b)*(f-b)*(g-b)
B=a*b*(a-b*q)*(a-b)*(a*q-b)*(1-c)*(1-d)-A-C
S[144]=statement('(a b c d ee f g q : K) (L M R : ℕ)',A*PH([a/q,b*q,c,d],[ee,f,g],'L')+B*PH([a,b,c,d],[ee,f,g],'M')+C*PH([a*q,b/q,c,d],[ee,f,g],'R'),0,'(hbal : ee*f*g = a*b*c*d*q) (hL : terminatesAt [a/q,b*q,c,d] q L) (hM : terminatesAt [a,b,c,d] q M) (hR : terminatesAt [a*q,b/q,c,d] q R)')
def KM(n,x):return PH([Q('-('+n+')'),Q('-('+x+')'),-Q(n)/a],[Q('-N'),e(0)],n)
S[145]=statement('(a q : K) (N m n : ℕ)',SUM('x','N',lambda x:KM('m','x')*KM('n','x')*P([Q('-N')],'x')/P([q],'x')*zp(-a,'x')),P([-q/a],'N')*zp(a,'N')*Q('-N*(N+1)/2')*P([q],'n')*(1+1/a)*P([-Q('N+1')/a],'n')/(P([-1/a],'n')*(1+Q('2*n')/a)*P([Q('-N')],'n'))*zp(-a*Q('N+1'),'-n')*Q('n*(n+1)')*KD('m','n'),'(hm : m ≤ N) (hn : n ≤ N) (ha : a ≠ 0)')
def KMT(n,x):return PH([Q('-('+n+')'),Q('-('+x+')')],[Q('-N')],n,a*Q(n+'+1'))
S[146]=statement('(a q : K) (N m n : ℕ)',SUM('x','N',lambda x:KMT('m','x')*KMT('n','x')*P([a*q],'N-x')*zp(e('(-1:K)'),'N-x')*Q('x*(x-1)/2')/(P([q],'x')*P([q],'N-x'))),P([q,a*q],'n')*P([q],'N-n')/(P([q],'N')**2)*zp(e('(-1:K)'),'n')*zp(a,'N')*Q('(N+n+1)*(N+n)/2-n*(n+1)')*KD('m','n'),'(hm : m ≤ N) (hn : n ≤ N)')
A=(1-a*Q('n+1'))*(1-c*Q('n+1'))*(1-a*b*Q('n+1'))/((1-a*b*Q('2*n+1'))*(1-a*b*Q('2*n+2')))
C=a*c*Q('n+1')*(1-Q('n'))*(1-b*Q('n'))*(1-a*b*Q('n')/c)/((1-a*b*Q('2*n'))*(1-a*b*Q('2*n+1')))
S[147]=statement('(x a b c q : K) (n : ℕ)',(x-1)*BJ(x,a,b,c,'n'),MUL0(A,BJ(x,a,b,c,'n+1')-BJ(x,a,b,c,'n'))+MUL0(C,BJ(x,a,b,c,'n')-PREV(BJ(x,a,b,c,'n-1'))),'(hc : c ≠ 0)')
def KA(n,x):return PH([Q('-('+n+')'),Q('-('+x+')'),e(0)],[a*q,Q('-N')],n)
S[148]=statement('(a q : K) (N m n : ℕ)',SUM('x','N',lambda x:KA('m','x')*KA('n','x')*P([a*q,Q('-N')],'x')/P([q],'x')*zp(-Q('N-1')/a,'x')*Q('-x*(x-1)/2')),KD('m','n')/(P([a*q,Q('-N')],'n')/P([q],'n')*zp(e('(-1:K)'),'n')*zp(a*q,'N-n')*Q('N*n-n*(n-1)/2')),'(hm : m ≤ N) (hn : n ≤ N) (ha : a ≠ 0)')
# Complex limit uses punctured neighborhoods; the finite-sum identity covers removable z singularities.
S[149]='''(z q : ℂ) (n : ℕ) (hq : regular q) (hz : z ≠ 0) :
 ultraspherical q z q n = (∑ k ∈ Finset.range (n+1), z^((n:ℤ)-2*k)) ∧
 (z-z⁻¹ ≠ 0 → ultraspherical q z q n = (z^(n+1)-z^(-(n:ℤ)-1))/(z-z⁻¹)) ∧
 (1 ≤ n → Filter.Tendsto (fun beta : ℂ => (1-q^n)/(2*(1-beta))*ultraspherical beta z q n)
    (nhdsWithin 1 ({1}ᶜ)) (nhds ((z^n+z^(-(n:ℤ)))/2)))'''
S[150]='''(beta q : ℂ) (n : ℕ) (hq : regular q) :
 ultraspherical beta Complex.I q n =
 if n%2 = 1 then 0 else (-1)^(n/2)*poch (beta^2) (q^2) (n/2)/poch (q^2) (q^2) (n/2)'''
