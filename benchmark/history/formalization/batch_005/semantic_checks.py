"""Independent exact rational and finite-field checks; these are not Lean proofs."""
from fractions import Fraction as F
from itertools import product
from functools import lru_cache
from math import prod
from pathlib import Path
import json
checks=[]
def check(s,a,b):
    assert a==b,(s,a,b)
    checks.append(s)
def add(a,b):return [ (a[i] if i<len(a) else 0)+(b[i] if i<len(b) else 0) for i in range(max(len(a),len(b))) ]
def scale(a,c):return [c*x for x in a]
def mul(a,b):
    c=[F(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):c[i+j]+=x*y
    return c
def power(a,n):
    r=[F(1)]
    for _ in range(n):r=mul(r,a)
    return r
def ev(a,x):return sum(v*x**i for i,v in enumerate(a))
def poch(a,q,n):return prod((1-a*q**i for i in range(n)),start=F(1))
@lru_cache(None)
def G(q,n,k):
    if k<0 or k>n:return F(0)
    if k==0:return F(1)
    return G(q,n-1,k-1)+q**k*G(q,n-1,k)
def KP(x,a,q,n):
    if n>=0:return prod((x-q**i*a for i in range(n)),start=F(1))
    return 1/KP(x,q**n*a,q,-n)
def qnum(q,n):return (q**n-1)/(q-1)
def snum(q,n):return (q**n-q**(-n))/(q-1/q)
def sfact(q,n):return prod((snum(q,i) for i in range(1,n+1)),start=F(1))
# Borwein components come from the original product, not the Gaussian identities.
for q in [F(0),F(1),F(2),F(1,2)]:
    for n in range(7):
        f=[F(1)]
        for i in range(n):
            for d in [3*i+1,3*i+2]:f=mul(f,[F(1)]+[F(0)]*(d-1)+[F(-1)])
        for r,sign,exp,offset in [(0,1,lambda j:j*(9*j+1)//2,0),(1,-1,lambda j:j*(9*j-5)//2,-1),(2,-1,lambda j:j*(9*j+7)//2,1)]:
            lhs=sign*sum(c*q**(i//3) for i,c in enumerate(f) if i%3==r)
            rhs=sum(F((-1)**j)*q**exp(j)*G(q,2*n,n+3*j+offset) for j in range(-n-1,n+2))
            check(f'Borwein {q,n,r}',lhs,rhs)
# Signed lengths: direct products / shifted reciprocals, including n=0.
q,x,a=F(2),F(5),F(3)
for n in range(-4,5):
    for m in range(-3,4):check(f'signed add {n,m}',KP(x,a,q,n+m),KP(x,a,q,m)*KP(x,q**m*a,q,n))
    check(f'signed reverse {n}',KP(a,x,q,n),F((-1)**n)*q**(n*(n-1)//2)*KP(x,q**(1-n)*a,q,n))
    D=lambda f:(f(x)-f(q*x))/((1-q)*x)
    check(f'signed first derivative {n}',D(lambda y:KP(y,a,q,n)),qnum(q,n)*KP(x,a,q,n-1))
    check(f'signed reciprocal first {n}',D(lambda y:1/KP(y,a,q,n)),qnum(q,-n)*KP(x,q**n*a,q,-n-1))
    check(f'signed second derivative {n}',D(lambda y:KP(a,y,q,n)),-qnum(q,n)*KP(a,q*x,q,n-1))
    check(f'signed reciprocal second {n}',D(lambda y:1/KP(a,y,q,n)),qnum(q,n)/KP(a,x,q,n+1))
# Construct the general Taylor family from its polynomial difference operator.
def dmono(q,r,h,hp,m):
    v=[F(0)]*m
    for i in range(m):v=add(v,mul(power([h,q],m-1-i),power([hp,r],i)))
    return v
def family(q,r,h,hp,a,N):
    ts=[[F(1)]]
    for n in range(1,N+1):
        rem=ts[-1]+[F(0)];u=[F(0)]*(n+1)
        for m in range(n,0,-1):
            dm=dmono(q,r,h,hp,m);c=rem[m-1]/dm[m-1];u[m]=c;rem=add(rem,scale(dm,-c))
        assert all(v==0 for v in rem)
        u[0]=-ev(u,a);ts.append(u)
    return ts
def pair(q,r,n):return sum(q**(n-1-i)*r**i for i in range(n))
for q,r,h,hp in [(F(2),F(3),F(1,5),F(2,7)),(F(2),F(2),F(1,5),F(2,7)),(F(2),F(3),F(1,5),F(1,5))]:
    a=F(4,9);ts=family(q,r,h,hp,a,6)
    ss=lambda n:-ts[n][n-1]/ts[n][n]
    for n in range(2,7):
        rhs=(F(n)*q/(n-1)*ss(n-1)+F(n)*(h+hp)/2) if q==r else pair(q,r,n)/pair(q,r,n-1)*ss(n-1)+(n*(q**(n-1)*h-r**(n-1)*hp)-pair(q,r,n)*(h-hp))/(q**(n-1)-r**(n-1))
        check(f'Taylor root recurrence {q,r,h,hp,n}',ss(n),rhs)
    if h==hp:
        for n in range(1,7):check(f'Taylor root finite sum {n}',ss(n),(a-h)*pair(q,r,n)+h*pair(q,r,n)*sum(F(j)/pair(q,r,j) for j in range(1,n+1)))
# Corrected symmetric Taylor: independently compare triangular construction to operator construction.
for q in [F(2),F(1,3)]:
    a=F(3,7);ts=[[F(1)]];reference=family(q,1/q,F(0),F(0),a,7)
    for n in range(1,8):
        t=[F(0)]*n+[1/sfact(q,n)]
        for k in range(n):t=add(t,scale(ts[k],-a**(n-k)/sfact(q,n-k)))
        ts.append(t)
        check(f'symTaylor polynomial {q,n}',t,reference[n])
        check(f'symTaylor boundary {q,n}',ev(t,a),F(0))
        check(f'symTaylor lowering {q,n}',[t[i]*snum(q,i) for i in range(1,n+1)],ts[n-1])
# Rank enumeration over prime fields (actual Gaussian elimination).
def rank(rows,p):
    a=[list(row) for row in rows];m=len(a);n=len(a[0]) if m else 0;r=0
    for j in range(n):
        pivot=next((i for i in range(r,m) if a[i][j]%p),None)
        if pivot is None:continue
        a[r],a[pivot]=a[pivot],a[r];inv=pow(a[r][j],-1,p);a[r]=[(v*inv)%p for v in a[r]]
        for i in range(m):
            if i!=r:
                fac=a[i][j];a[i]=[(v-fac*w)%p for v,w in zip(a[i],a[r])]
        r+=1
    return r
for p,m,n in [(2,2,3),(3,2,2),(2,3,2)]:
    counts=[0]*(min(m,n)+1)
    for xs in product(range(p),repeat=m*n):counts[rank([xs[i*n:(i+1)*n] for i in range(m)],p)]+=1
    for j in range(min(m,n)+1):
        check(f'matrix rank {p,m,n,j}',counts[j],G(F(p),n,j)*prod(p**m-p**i for i in range(j)))
    check(f'independent tuples {p,m,n}',counts[min(m,n)],prod(p**max(m,n)-p**i for i in range(min(m,n))))
Path(__file__).with_suffix('.json').write_text(json.dumps(dict(checks=len(checks),passed=len(checks),arithmetic='exact rational and prime-field enumeration',labels=checks),ensure_ascii=False,indent=2)+'\n')
print(f'{len(checks)} exact checks passed')
