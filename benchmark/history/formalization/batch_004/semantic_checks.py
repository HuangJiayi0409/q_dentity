"""Independent exact-arithmetic checks of newly translated definitions; not proofs."""
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations
from math import prod
from pathlib import Path
import json
checks=[]
def check(label,lhs,rhs):
    assert lhs==rhs,(label,lhs,rhs)
    checks.append(label)
def poch(a,q,n):return prod((1-a*q**i for i in range(n)),start=F(1))
@lru_cache(None)
def G(q,n,k):
    if k<0 or k>n or n<0:return F(0)
    if k==0:return F(1)
    return G(q,n-1,k-1)+q**k*G(q,n-1,k)
@lru_cache(None)
def T(q,r,N):
    return F(1) if N==0 else -sum(G(q,r+2*j,j)*T(q,r+2*j,N-2*j) for j in range(1,N//2+1))
def C(q,n,j):return sum(q**(k*(k+j))*G(q,n,k)*G(q,n-k,k+j) for k in range(n+1) if 0<=k+j<=n-k)
def T01(q,n,j,one):return sum((-q if one else -1)**k*G(q*q,n,k)*G(q,2*n-2*k,n-j-k) for k in range(n+1))
def alpha(x,q,d,k,r):
    if r%d:return F(0)
    s=r//d
    return (-1)**s*x**((k-d)*s)*q**((d*(2*k-2*d+1)*s*s-d*s)//2)*(1-x*q**(2*d*s))*poch(x,q**d,s)/((1-x)*poch(q**d,q**d,s))
def bailey(x,q,d,e,k,n):return sum(alpha(x,q,d,k,r)/(poch(q**e,q**e,n-r)*poch((x*q)**e,q**e,n+r)) for r in range(n+1))
def partitions(N):
    for k in range(N+1):
        for s in combinations(range(1,N+1),k):
            if all(b-a>=3 and (a%3 or b%3 or b-a>3) for a,b in zip(s,s[1:])):yield s
for q in [F(2),F(1,3)]:
    for r in range(3):
        for n in range(1,4):
            check(f'inverse T {q,r,n}',T(q,r,2*n),(-1)**n*q**(n*(n-1)//2)*poch(q**(r+1),q,n-1)*(1-q**(r+2*n))/poch(q,q,n))
    g=[F(1)]
    for n in range(5):g.append((((q+q*q)*q**(3*n)+q**(6*n+3))*g[n]-(0 if n==0 else q**(6*n)*g[n-1]))/(1-q**(3*(n+1))))
    for n in range(6):check(f'G0 convolution {q,n}',sum(g[j]/poch(q**3,q**3,n-j) for j in range(n+1)),poch(-q,q**3,n)*poch(-q*q,q**3,n)/poch(q**3,q**3,n))
    for n in range(1,5):
        for j in range(-n-1,n+2):
            check(f'T1 {q,n,j}',T01(q,n,j,True),T01(q,n-1,j,True)+q**(n+j)*T01(q,n-1,j+1,False)+q**(n-j)*T01(q,n-1,j-1,False))
            check(f'T0 {q,n,j}',T01(q,n,j,False),T01(q,n-1,j-1,False)+q**(n+j)*T01(q,n-1,j,True)+q**(2*n+2*j)*T01(q,n-1,j+1,False))
    x=F(5,7)
    for n in range(4):
        for d,e,k,rhs in [(1,1,2,1/poch(q,q,n)),(1,2,2,1/(poch(q*q,q*q,n)*poch(-x*q,q,2*n))),(1,2,1,(-1)**n*q**(n*n)/(poch(q*q,q*q,n)*poch(-x*q,q,2*n))),(1,3,2,poch(x*q,q,3*n)/(poch(q**3,q**3,n)*poch(x**3*q**3,q**3,2*n))),(2,1,2,q**(n*(n-1)//2)/(poch(q,q,n)*poch(x*q,q*q,n))),(2,1,3,1/(poch(q,q,n)*poch(x*q,q*q,n))),(3,1,4,poch(x,q**3,n)/(poch(q,q,n)*poch(x,q,2*n)))]:
            check(f'Bailey alpha {q,d,e,k,n}',bailey(x,q,d,e,k,n),rhs)
        lhs=F(1) if n==0 else sum(x**sum(1 if j%3==1 else -1 if j%3==2 else 0 for j in s)*q**sum(s) for s in partitions(3*n-1))
        check(f'Schur partitions {q,n}',lhs,sum(x**j*q**(j*(3*j-1)//2)*C(q**3,n,j) for j in range(-n,n+1)))
    a,b,t=F(2,7),F(3,11),F(5,13)
    h,gg=F(1),F(0)
    for n in range(5):
        h,gg=(b*q**n-a)*t/((1-b*q**(n+1))*(b*q**n-a*t))*h,gg+b*q**n/(b*q**n-a*t)*h
        check(f'Fine H {q,n}',h,poch(b/a,q,n+1)/(poch(b*q,q,n+1)*poch(b/(a*t),q,n+1)))
        check(f'Fine G {q,n}',gg,-b/(a*t)/(1-b/(a*t))*sum(poch(b/a,q,j)*q**j/(poch(b*q,q,j)*poch(b*q/(a*t),q,j)) for j in range(n+1)))
    for n in range(5):
        A=sum((-1)**j*q**(j*(j-1)//2)/poch(q,q,j)*poch(a*q,q,n-j)/poch(b*q,q,n-j) for j in range(n+1))
        check(f'Fine A {q,n}',A,(-a)**n*q**(n*(n+1)//2)/poch(b*q,q,n)*sum(poch(b,q,j)*a**(-j)/poch(q,q,j) for j in range(n+1)))
# Polynomial boundary checks include q=0 and q=1.
for q in [F(0),F(1),F(2)]:
    for n in range(2,6):
        P=lambda n:sum(q**(j*j+k*k)*G(q*q,j,k)*G(q*q,n-k,j) for j in range(n+1) for k in range(min(j,n-j)+1))
        check(f'P recurrence {q,n}',P(n),(1+q**(2*n-1))*P(n-1)+q**(2*n-2)*P(n-2))
# Operator identity is checked on independent basis inputs, not a special d sequence.
q,t=F(2),F(3)
def op(t,n,x,y,z,w,v):
    return x-(1+t*q**(6*n)*(q**-1+q**-2+q**-4))*y-t*t*q**(6*n)*(q**-3+q**-5+q**-6)*(1-q**(6*n-6))*z-t**3*q**(12*n-13)*(t*(q**-1+q**-2+q**-4)+q**(6*n-12))*w-t**6*q**(18*n-32)*v
for n in [5,6]:
    for index in range(6*n-37,6*n+6):
        d=lambda k:F(k==index)
        J=lambda n:op(t,n,*[d(6*n-1-6*j) for j in range(5)])
        GG=lambda n:d(6*n+5)-t*q**(6*n+2)*(1+q*q+q**3)*d(6*n-1)+t*t*q**(12*n)*(1+q+q**3)*d(6*n-7)-t**3*q**(18*n-7)*d(6*n-13)
        check(f'operator basis {n,index}',op(t*q**6,n-1,*[GG(n-j) for j in range(5)]),J(n+1)-t*q**(6*n-6)*(q*q+q**4+q**5)*J(n)+t*t*q**(12*n-12)*(1+q+q**3)*J(n-1)-t**3*q**(18*n-25)*J(n-2))
Path(__file__).with_suffix('.json').write_text(json.dumps({'checks':len(checks),'passed':len(checks),'arithmetic':'exact rational','labels':checks},ensure_ascii=False,indent=2)+'\n')
print(f'{len(checks)} exact checks passed')
