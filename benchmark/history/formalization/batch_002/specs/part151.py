from common import *
a,b,c,d,q,z,w,v,t,beta,gamma,s,A,B,rho,lam=vs('a b c d q z w v t beta gamma s A B rho lam')
S={}
nz=lambda names:'(hnz : ∀ v ∈ ['+names+'], v ≠ 0)'
S[151]=claims('(z beta q : K) (n : ℕ)',[((z+1/z)*UL(z,beta,'n'),(1-Q('n+1'))/(1-beta*Q('n'))*UL(z,beta,'n+1')+(1-beta*beta*Q('n-1'))/(1-beta*Q('n'))*PREV(UL(z,beta,'n-1'))),(UL(z,beta,'n'),(1-beta)/(1-beta*Q('n'))*(UL(z,beta*q,'n')-beta*PREV(UL(z,beta*q,'n-2'),'n < 2')))],nz('z'))
# Quotients replaced by their finite Laurent extensions, with the quotient bridge proved separately.
GEOM=SUM('k','n',lambda k:Q('0')*zp(z,'n-2*k'))
GM=SUM('k','2*n',lambda k:zp(z,'n-k'))
GP=SUM('k','2*n',lambda k:zp(e('(-1:K)'),'k')*zp(z,'n-k'))
S[152]=claims('(z s q : K) (n : ℕ)',[(AW(z,q,-q,s,-s,'n'),P([Q('n+2')],'n')*GEOM),(AW(z,q,e(-1),s,-s,'n'),P([Q('n+1')],'n')*GM),(AW(z,e(1),-q,s,-s,'n'),P([Q('n+1')],'n')*GP)],'(hs : s^2 = q) (hz : z ≠ 0)')
# The n>=1 branch with a=1 is an additional conjunct, not an excluded degree-zero condition.
extra152=statement('(z s q : K) (n : ℕ)',AW(z,e(1),e(-1),s,-s,'n'),P([Q('n')],'n')*(zp(z,'n')+zp(z,'-n')),'(hn : 1 ≤ n) (hs : s^2 = q) (hz : z ≠ 0)')
# Keep the four printed formulas in one theorem by quantifying the second branch in-place.
# An extra universal conclusion avoids narrowing the other three to n>=1.
S[152]=S[152]+' ∧\n (1 ≤ n → '+str(AW(z,e(1),e(-1),s,-s,'n'))+' = '+str(P([Q('n')],'n')*(zp(z,'n')+zp(z,'-n')))+')'
# Its extra denominator conditions are just [q,-1,s,-s], all implied by regular q and s²=q;
# list them explicitly for transparent checking.
pos=S[152].index(' (h_domain :')
S[152]=S[152][:pos]+' (h_second : phiDefined [-1,s,-s] q n)'+S[152][pos:]
def J(z,A,B):return P([A*q,-B*q],'n')/P([q,-q],'n')*PH([Q('-n'),A*B*Q('n+1'),s*z,s/z],[A*q,-B*q,-q],'n')
def KK(z,A,B):return P([A*A*s],'n')/P([q],'n')*PH([Q('-n'),A*A*B*B*Q('n'),A*z,A/z],[A*A*s,-A*B,-A*B*s],'n')
S[153]=claims('(z A B s q : K) (n : ℕ)',[(J(-z,A,B),zp(e('(-1:K)'),'n')*J(z,B,A)),(KK(-z,A,B),zp(-A/B,'n')*KK(z,B,A))],'(hs : s^2 = q) '+nz('A,B,z'))
def Un(z,n):
    pref=P([q],n)*P([rho*rho*lam*lam*q],n+'+r')*zp(s,'3*('+n+')^2+('+n+')-2*('+n+')*r')*zp(rho,'2*('+n+')')/(P([q],'r-('+n+')')*P([rho*q,rho*rho*q,rho*lam*q,-rho*q,-rho*s,-rho*s,-rho*lam*q],n))
    term=pref*P([rho*q*z,rho*q/z],n)*PH([Q('('+n+')-r'),rho*rho*lam*lam*Q('('+n+')+r+1'),rho*s*Q(n),rho*rho*Q(n),rho*Q('('+n+')+1')*z,rho*Q('('+n+')+1')/z],[rho*rho*Q('2*('+n+')+1'),rho*lam*Q('('+n+')+1'),rho*rho*Q('('+n+')+1'),-rho*lam*Q('('+n+')+1'),-rho*s*Q(n)],'r-('+n+')')
    return PREV(term,f'r < ({n})')
def Tn(z):return (1-Q('-n')/(rho*s*z))/(P([rho*q*s*z],'n')*P([rho*s/z],'n+1'))
Dden=(s-1/s)*(z-1/z)/2
S[154]=statement('(z rho lam s q : K) [CharZero K] (r n : ℕ)',(Un(s*z,'n')/P([rho*q*s*z,rho*q/(s*z)],'n')-Un(z/s,'n')/P([rho*q*z/s,rho*q/(z/s)],'n'))/Dden,-(1-rho*rho*Q('n'))/(1-Q('n+1'))*(Tn(z)*Un(s*z,'n+1')-Tn(1/z)*Un(z/s,'n+1'))/Dden,'(hn : 1 ≤ n) (hnr : n ≤ r) (hs : s^2 = q) '+nz('rho,lam,z'))
def HH(n):return SUM('k','('+n+')/2',lambda k:P([q],n)*zp(e('(-1:K)'),'k')*Q('k*(k-1)')*e('x')**('('+n+'-2*k)')/(P([q*q],'k',q*q)*P([q],n+'-2*k')))
S[155]=statement('(x q : K) (n : ℕ)',HH('n+1'),e('x')*HH('n')-Q('n-1')*(1-Q('n'))*HH('n-1'),'(hn : 1 ≤ n)')
x=e('x');h=lambda n:e(f'(rogersSzego x q ({n}))')
S[156]=statement('(x q : K) (n : ℕ)',h('n')**2-h('n+1')*h('n-1'),(1-q)*P([q],'n-1')*SUM('k','n',lambda k:Q('n-k')*x**'k'/P([q],'n-k')*h('n-k')**2,lo='1'),'(hn : 1 ≤ n)')
S[157]=statement('(q : K) (n x y z : ℕ)',LJ(Q('z'),e(1),e(1),'n')*LJ(Q('z'),Q('x'),e(0),'y'),LJ(Q('x+y'),e(1),e(1),'n')*LJ(Q('y'),e(1),e(1),'n')*LJ(Q('z'),Q('x'),e(0),'y')+SUM('k','n',lambda k:P([q],'x+y+k')*P([q],'n+k')*Q('k*(k+y-n)')/(P([q],'x+y')*P([q],'n-k')*P([q],'k')**2)*LJ(Q('x+y'),Q('k'),Q('k'),'n-k')*LJ(Q('y'),Q('k'),Q('k'),'n-k')*LJ(Q('z'),Q('x'),e(0),'y+k'),lo='1')+SUM('k','min n y',lambda k:P([q],'y')*P([q],'n+k')*Q('k*(x+y-n+1)')/(P([q],'y-k')*P([q],'n-k')*P([q],'k')**2)*LJ(Q('x+y-k'),Q('k'),Q('k'),'n-k')*LJ(Q('y-k'),Q('k'),Q('k'),'n-k')*LJ(Q('z'),Q('x'),e(0),'y-k'),lo='1'))
S[158]=statement('(t a q : K) (j k : ℕ)',P([t,a/t],'j')*P([t,a/t],'k'),P([q],'j')*P([q],'k')*P([a],'j+k')*SUM('m','j+k',lambda m:P([t,a/t],'m')*zp(e('(-1:K)'),'j+k+m')*Q('j*(j-1)/2+k*(k-1)/2+m*(m+1)/2-m*(j+k)')/(P([a],'m')*P([q],'m-j')*P([q],'m-k')*P([q],'j+k-m')),lo='max j k'),'(ht : t ≠ 0)')
S[159]=statement('(a b c q : K) (n : ℕ) (B C : ℕ → K)',SUM('j','n',lambda j:P([Q('-n'),a*Q('n')],'j')*e('(B j)')/P([q,b],'j'))*SUM('k','n',lambda k:P([Q('-n'),a*Q('n')],'k')*e('(C k)')/P([q,c],'k')),SUM('m','n',lambda m:P([Q('-n'),a*Q('n')],'m')*SUM('k','m',lambda k:e('(C k)')*Q('k*k-m*k')/(P([q,c],'k')*P([q,b],'m-k'))*SUM('j','k',lambda j:P([Q('-k'),a*Q('m')],'j')*e('(B (m-k+j))')/P([q,b*Q('m-k')],'j')))))
