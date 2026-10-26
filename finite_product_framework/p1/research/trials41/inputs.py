"""Explicit formula transcriptions and candidate changes of variables, NOT proofs.
Only mathematical inputs are supplied; no certificates, recurrences or degrees.
All domain equivalences and special parameter values remain Lean obligations.
"""
import sympy as s
n,k=s.symbols('n k',integer=True)
q,Q,X=s.symbols('q Q X')
a,b,c,d,e,f,t,x,z,w=s.symbols('a b c d e f t x z w')
m,u,v=s.symbols('m u v',integer=True,nonnegative=True)
P=s.Function('Poch');G=s.Function('Gaussian')
def pl(aa,base,L):return s.prod(P(y,base,L) for y in aa)
def phi(aa,bb,base,z0):return pl(aa,base,k)/pl([base]+bb,base,k)*((-1)**k*base**(k*(k-1)/2))**(1+len(bb)-len(aa))*z0**k
def wp(a0,bb,z0):return (1-a0*q**(2*k))/(1-a0)*pl([a0]+bb,q,k)/pl([q]+[a0*q/y for y in bb],q,k)*z0**k
def bi(aa,bb,cc,dd,z0):return phi(aa,bb,q**2,z0)*pl(cc,q,k)/pl(dd,q,k)*((-1)**k*q**(k*(k-1)/2))**(len(dd)-len(cc))
def fall(A,B,L):return A**L*P(B/A,q,L)
def alpha(A,base,D,H,j):return (-1)**j*A**((H-D)*j)*base**s.expand((D*(2*H-2*D+1)*j*j-D*j)/2)*(1-A*base**(2*D*j))*P(A,base**D,j)/((1-A)*P(base**D,base**D,j))
CASES=[]
def add(id,F,T,lo=0,hi=n,branch='main',route='qwz',change='identity',obligations='Original parameter domain, boundary and initial values; no Lean representation proof yet.'):
 CASES.append(dict(id=id,branch=branch,F=s.sympify(F),T=s.sympify(T),lo=s.sympify(lo),hi=s.sympify(hi),route=route,change=change,obligations=obligations))
add('FQI-CHU-VANDERMONDE-Q',phi([a,q**(-n)],[c],q,q),a**n*P(c/a,q,n)/P(c,q,n))
add('FQI-CHU-VANDERMONDE-BALANCED',phi([a,q**(-n)],[c],q,c*q**n/a),P(c/a,q,n)/P(c,q,n))
add('FQI-TERMINATING-6PHI5',wp(a,[b,c,q**(-n)],a*q**(n+1)/(b*c)),pl([a*q,a*q/(b*c)],q,n)/pl([a*q/b,a*q/c],q,n),obligations='Raw form equals wellPoised only generically; separately verify k=0 and the original a=1 removable extension.')
unit=(-1)**k*q**(k*(k-1)/2)*(1-a*q**(2*k))*P(a*q,q,k-1)/P(q,q,k)
add('FQI-BAILEY-UNIT',unit/(P(q,q,n-k)*P(a*q,q,n+k)),s.KroneckerDelta(n,0),route='direct',change='fixed external n; generic continuation of r>=1; true r=0 handled separately',obligations='At r=0 use unitBailey=1, including a=1; split n=0 and n>0. n-dependent summands are allowed by the mathematical direct algorithm.')
for label,weight in [('b_power',b**k),('a_power',a**(n-k))]:
 add('FQI-SRC-GR2-1.Ex3i',G(q,n,k)*weight*P(a,q,k)*P(b,q,n-k),P(a*b,q,n),branch=label,obligations='Both conjuncts required; preserve a,b,q zero values.')
add('FQI-SRC-GR2-1.Ex5',P(b/c,q,n)/P(b,q,n)*pl([q**(-n),c],q,k)/pl([q,c*q**(1-n)/b],q,k)*q**k*P(c*q**k,q,m),pl([c,b*q**n],q,m)/P(b,q,m),change='hold m fixed; absorb outside prefactor into F without dividing it away')
for delta in (0,1):
 N=2*n+delta
 add('FQI-SRC-GR2-1.Ex6i',phi([q**(-N),q**(1-N)],[q*b*b],q*q,q*q),P(b*b,q*q,N)/P(b*b,q,N)*q**(-N*(N-1)/2),branch=f'parity_{delta}',change=f'original n=2*n+{delta}, upper=floor(original n/2)=n')
add('FQI-SRC-GR2-1.Ex6iii',phi([a,q**(-n)],[],q,q**n/a),a**(-n))
for delta in (0,1):
 N=2*n+delta
 add('FQI-SRC-GR2-2.3.2',phi([a,q**(-N)],[a*q**(N+1)],q,-q**(N+1)),P(-q,q,N)*P(a*q,q*q,n+delta)/P(a*q**(2*n+2),q*q,n+delta),branch=f'parity_{delta}',hi=N,change=f'original m=2*n+{delta}; two new tail terms per n step')
add('FQI-SRC-GR2-2.Ex5',wp(a,[b,c,a/(b*c)],q),pl([a*q,b*q,c*q,a*q/(b*c)],q,n)/pl([q,a*q/b,a*q/c,b*c*q],q,n),route='direct',change='n-independent nonterminating partial sum; keep actual endpoints')
add('FQI-SRC-GR2-2.Ex12',(1-a*q**(2*k))/(1-a)*pl([a,a/b,a*a*q**(n+1)/b,q**(-n)],q,k)*pl([b,b*q],q*q,k)*q**k/(pl([q,b*q,b*q**(-n)/a,a*q**(n+1)],q,k)*pl([a*a*q*q/b,a*a*q/b],q*q,k)),pl([a*q,a*a*q/b**2],q,n)/pl([a*q/b,a*a*q/b],q,n))
add('FQI-SRC-GR2-2.Ex14i',phi([a*a,q*a,b,q**(-n)],[a,a*a*q/b,b*b*q**(1-n)],q,q),pl([a*a/b**2,1/b,-q*a/b],q,n)/pl([1/b**2,a*a*q/b,-a/b],q,n),change='rename original s to a')
add('FQI-SRC-GR2-3.10.5',bi([a*a,a*q*q,-a*q*q],[a,-a],[-a*q/w,q**(-n)],[w,-a*q**(n+1)],w*q**(n-1)/a),pl([-a*q,a*q*q/w,w/(a*q)],q,n)/pl([-q,a*q/w,w],q,n))
add('FQI-SRC-GR2-3.10.6',bi([a*a,-a*q*q,b*b],[-a,a*a*q*q/b**2],[-a*q**n/b**2,q**(-n)],[b*b*q**(1-n),-a*q**(n+1)],q*q),pl([q**n/b**2,-a*q],q,n)*pl([a*q/b**2,a*q*q/b**2],q*q,n)/(pl([a*q**n/b**2,-q],q,n)*pl([q/b**2,a*a*q*q/b**2],q*q,n)))
add('FQI-SRC-GR2-3.10.8',bi([a*a,a*q*q,-a*q*q,b*b],[a,-a,a*a*q*q/b**2],[-a*q**(n-1)/b**2,q**(-n)],[b*b*q**(2-n),-a*q**(n+1)],q*q),pl([-a*q,a/(q*b*b)],q,n)*pl([a*q/b**2,1/(q*q*b*b)],q*q,n)*q**n/(pl([-q,1/(q*b*b)],q,n)*pl([a/(q*b*b),a*a*q*q/b**2],q*q,n)))
# Combine the paired q^2 denominators into one q product of length 2k.
add('FQI-SRC-GR2-3.Ex34',pl([q**(-2*n),c*c,a,q*a],q*q,k)/pl([q*q,q*q*a*a],q*q,k)/P(c*q**(-n),q,2*k)*(q*q)**k,pl([-q,q*a/c],q,n)/pl([-a*q,q/c],q,n),change='(c q^-n;q^2)_k (c q^(1-n);q^2)_k -> (c q^-n;q)_(2k); identity of finite products to verify')
for offset,last,basefactor in [(1,0,1),(3,1,1-q)]:
 E=q**(n+offset)/(b*c*d)
 add('FQI-SRC-GR2-5.Ex18'+('iii' if offset==1 else 'iv'),pl([b,c,d,E,q**(-n)],q,k)/pl([q**(1+last)/b,q**(1+last)/c,q**(1+last)/d,q**(1+last)/E,q**(n+1+last)],q,k)*q**k,basefactor*pl([q**(1+last),q**(1+last)/(b*c),q**(1+last)/(b*d),q**(1+last)/(c*d)],q,n)/pl([q**(1+last)/b,q**(1+last)/c,q**(1+last)/d,q**(1+last)/(b*c*d)],q,n),lo=-n-last,change=f'eliminate e=q^(n+{offset})/(b*c*d); signed Pochhammer lengths use reciprocal definition')
for odd in (0,1):
 add('FQI-SRC-GR2-5.Ex19'+('ii' if odd else 'i'),(-1)**k*G(q,2*n+odd,n+k+odd)**3*q**(k*(3*k+1)/2),P(q,q,3*n+odd)/P(q,q,n)**3,lo=-n-odd,change='integer k; quadratic exponent is nonnegative integral on all integer k; keep both boundaries')
for flip in (0,1):
 j0,h0=(n+m,m) if flip==0 else (m,n+m)
 r=j0 if flip==0 else h0
 r=r+k
 F=pl([q],q,j0)*P(q,q,h0)*P(a,q,j0+h0)*pl([t,a/t],q,r)*(-1)**(j0+h0+r)*q**(j0*(j0-1)/2+h0*(h0-1)/2+r*(r+1)/2-r*(j0+h0))/(P(a,q,r)*P(q,q,r-j0)*P(q,q,r-h0)*P(q,q,j0+h0-r))
 add('FQI-SRC-GR2-8.1.2',F,pl([t,a/t],q,j0)*pl([t,a/t],q,h0),hi=m,branch=f'ordered_{flip}',change=f'original (j,k)={("n+m,m" if not flip else "m,n+m")}; original summation index=n+m+k; bound m constant')
F=(1-a*q**(3*k))/(1-a)*pl([b,c,d],q,k)*pl([e,f,q**(-2*n)],q*q,k)*q**k/(pl([a*q*q/b,a*q*q/c,a*q*q/d],q*q,k)*pl([a*q/e,a*q/f,a*q**(2*n+1)],q,k))
T=pl([a*q*q,a*a*q*q/(b*c*e),a*a*q*q/(b*d*e),a*q*q/(c*d)],q*q,n)/pl([a*a*q*q/(b*e),a*q*q/c,a*q*q/d,a*a*q*q/(b*c*d*e)],q*q,n)
for label,sub in [('b_eq_a',{b:a,d:q/c,f:a*a*q**(2*n+1)/e}),('e_eq_a',{e:a,d:a*q/(b*c),f:a*q**(2*n+1)})]:
 add('FQI-SRC-GR2-11.Ex21-p0',F.subs(sub,simultaneous=True),T.subs(sub,simultaneous=True),branch=label,change='split given disjunction; eliminate parameters so both balances hold: '+str(sub))
for delta in (0,1):
 N=2*n+delta
 add('FQI-SRC-GR2-II-19',phi([q**(-N),q**(N+1),c,-c],[e,c*c*q/e,-q],q,q),q**(N*(N+1)/2)*pl([e*q**(-N),c*c*q**(1-N)/e],q*q,n+delta)/pl([e*q**(1-delta),c*c*q**(2-delta)/e],q*q,n+delta),hi=N,branch=f'parity_{delta}',change=f'original n=2*n+{delta}; ceil length=n+{delta}')
E=a*a*q**(n+1)/(b*c*d)
add('FQI-SRC-GR2-II-22',wp(a,[b,c,d,E,q**(-n)],q),pl([a*q,a*q/(b*c),a*q/(b*d),a*q/(c*d)],q,n)/pl([a*q/b,a*q/c,a*q/d,a*q/(b*c*d)],q,n),change='e=a^2*q^(n+1)/(b*c*d), preserving original balance')
for flip in (0,1):
 D,N=(v+u,v) if flip==0 else (v,v+u)
 M=m+D;NN=v+u+n
 add('FQI-SRC-AP-3.3.11',G(q,D,k)*G(q,N+m,m+k)*G(q,m+NN+k,M+N)*q**((N-k)*(D-k)),G(q,m+NN,M)*G(q,NN,N),hi=v,branch=f'support_{flip}',change='M=m+D, (D,N)='+str((D,N))+'; original n=max(D,N)+n; zero region original n<max(D,N) requires separate support proof')
add('FQI-SRC-AP-3.3.14',pl([a,b],q,k)*P(c/(a*b),q,n-k)/(pl([q,c],q,k)*P(q,q,n-k))*(a*b/c)**(n-k),pl([c/a,c/b],q,n)/pl([q,c],q,n)*(a*b/c)**n)
add('FQI-SRC-AP-3.E1',q**(k*k)*x**k*G(q*q,2*n,n+k),pl([-q/x,-x*q],q*q,n),lo=-n,change='bilateral integer k; nonnegative square exponent, generic q not zero; original q=0 still pending')
add('FQI-SRC-AP-13.E3',G(q,n,k)*fall(b,c,k)*fall(a,b,n-k),fall(a,c,n),change='rename X,Y,Z -> a,b,c; formal fall(A,B,L)=A^L*(B/A;q)_L only generically; zero parameters require polynomial bridge')
add('FQI-SRC-AQ-3.17',(-1)**k*q**(k*(3*k+1)/2)*G(q,2*(n+1)-1,n-k),P(q**(n+1),q,n+1),lo=-n-1,hi=n,change='original n=n+1 to preserve n>=1; negative indices and both endpoints retained')
add('FQI-SRC-AQ-3.18',(-1)**k*q**(k*(3*k+1)/2)*G(q,2*n,n-k),P(q**(n+1),q,n),lo=-n)
add('FQI-SRC-AQ-3.37',(-1)**k*q**(k*(k-1)/2)*(1-q**(2*k+1))/((1-q)*P(q,q,n-k)*P(q*q,q,n+k)),s.KroneckerDelta(n,0),route='direct',change='n fixed external parameter; endpoint split n=0 and n>0')
A,B,C=n,n+u,n+v
add('FQI-SRC-AQ-4.24',(-1)**k*q**(k*(3*k+1)/2)*G(q,B+C,C+k)*G(q,C+A,A+k)*G(q,A+B,B+k),P(q,q,A+B+C)/(P(q,q,A)*P(q,q,B)*P(q,q,C)),lo=-n,change='choose cyclically smallest parameter as a=n, b=n+u,c=n+v; cyclic symmetry covers other minima, proof pending')
add('FQI-SRC-SILLS-1.JacobiFinite',(-1)**k*q**(k*(k-1)/2)*x**k*G(q,2*n,n+k),pl([q/x,x],q,n),lo=-n)
add('FQI-SRC-SILLS-1.75',(-1)**k*q**(k*(3*k+1)/2)*x**(3*k)*G(q,2*n,n+k)*(1-x*x*q**(2*k+1))/(P(x*x*q*q,q,n+k)*P(x**(-2),q,n-k)),(1-x*x*q)/pl([x*q,1/x],q,n),lo=-n)
add('FQI-SRC-SILLS-2.Pair122',alpha(x,q,1,2,k)/(P(q*q,q*q,n-k)*P(x*x*q*q,q*q,n+k)),1/(P(q*q,q*q,n)*P(-x*q,q,2*n)),change='d=1 removes divisibility restriction; keep r=0 quotient')
add('FQI-SRC-SILLS-2.Lem2.31',G(q*q,2*n,n+k)*a**k*q**(k*k),pl([-a*q,-q/a],q*q,n),lo=-n,change='use t as new base q; replace original q by t^2 using given equality; original t=0 requires separate bridge')
add('FQI-SRC-SILLS-2.Ex2c',alpha(x,q,1,2,k)/(P(q**3,q**3,n-k)*P(x**3*q**3,q**3,n+k)),P(x*q,q,3*n)/(P(q**3,q**3,n)*P(x**3*q**3,q**3,2*n)),change='d=1 support; q^3 is dependent base')
for delta in (0,1,2):
 N=3*n+delta
 add('FQI-SRC-SILLS-2.Ex2f',alpha(x,q,3,4,k)/(P(q,q,N-3*k)*P(x*q,q,N+3*k)),P(x,q**3,N)/(P(q,q,N)*P(x,q,2*N)),branch=f'residue_{delta}',change=f'original r=3*k, original n=3*n+{delta}; zero nonmultiples removed by definition')
add('FQI-SRC-SILLS-2.Lem2.53',q**(2*k*k+k)*(1+q**(2*k+1))/(1+q)/(P(q*q,q*q,n-k)*P(q**4,q*q,n+k)),1/(P(q**3,q*q,n)*P(q*q,q*q,n)),change='use t as new base q; original q=t^2; preserve t=0 and denominator conditions')
add('FQI-SRC-SILLS-3.Lem3.3',(-1)**k*q**(k*k)*(1-x*q**(2*k))*P(x*x,q*q,k)/((1-x)*P(q*q,q*q,k)*P(q,q,n-k)*P(x*q,q,n+k)),1/P(q*q,q*q,n))
add('FQI-SRC-KAC-CHEUNG-4.4',G(q,n,k)*fall(x,1,k),x**n,change='formal fall representation; x=0 remains polynomial bridge obligation')
