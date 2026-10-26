"""Independent exact samples for newly translated definitions, not target proofs."""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
import json
from pathlib import Path
checks=[]
def check(name,l,r):
 assert l==r,(name,l,r)
 checks.append(name)
def poch(a,q,n):
 x=F(1)
 for j in range(n): x*=1-a*q**j
 return x
def pl(xs,q,n):
 x=F(1)
 for a in xs:x*=poch(a,q,n)
 return x
@lru_cache(None)
def gauss(q,n,k):
 if k<0 or k>n or n<0:return F(0)
 if k==0:return F(1)
 return gauss(q,n-1,k-1)+q**k*gauss(q,n-1,k)
def phi(xs,ys,q,z,N):
 return sum(pl(xs,q,k)/pl([q]+ys,q,k)*((-1)**k*q**(k*(k-1)//2))**(1+len(ys)-len(xs))*z**k for k in range(N+1))
def parts(bound,gap,prefix=()):
 yield prefix
 for j in range(1,bound+1):yield from parts(j-gap,gap,prefix+(j,))
def D(q,n):
 if n==-1:return F(1)
 return sum(q**(j*j)*gauss(q,n+1-j,j)for j in range((n+1)//2+1))
def lam(q,n):
 vals=[F(1)]
 for j in range(n):
  v=(1+(q**2+q**4+q**5)*q**(6*j))*vals[j]
  if j>=1:v+=(q**6+q**7+q**9)*q**(6*(j-1))*(1-q**(6*j))*vals[j-1]
  if j>=2:v+=q**11*q**(6*(j-2))*(1-q**(6*j))*(1-q**(6*(j-1)))*vals[j-2]
  vals.append(v)
 return vals[n]
def lambda_euler_coefficient(q,n):
 # Independent finite convolution of the four Euler-series coefficients.
 Q=q**6;v=F(0)
 for a,b,c in product(range(n+1),repeat=3):
  d=n-a-b-c
  if d<0:continue
  v+=q**(2*a+4*b+5*c+3*(a*(a-1)+b*(b-1)+c*(c-1)))/pl([Q],Q,a)/pl([Q],Q,b)/pl([Q],Q,c)/pl([Q],Q,d)
 return poch(Q,Q,n)*v
def allowed(l):
 return all(x not in [1,3]for x in l) and all(x-y>=6 and (y%6 not in [0,1,3]or x-y>6)for x,y in zip(l,l[1:]))
def determinant(m):
 if not m:return F(1)
 return sum((-1)**j*m[0][j]*determinant([row[:j]+row[j+1:]for row in m[1:]])for j in range(len(m)))
def plane(q,k,r,bound,first=None):
 result=F(0)
 for flat in product(range(bound+1),repeat=k*r):
  a=[flat[i*r:(i+1)*r]for i in range(k)]
  if first is not None and tuple(row[0]for row in a)!=first:continue
  if any(a[i][j]<a[i][j+1]for i in range(k)for j in range(r-1)):continue
  if any(a[i][j]<a[i+1][j]for i in range(k-1)for j in range(r)):continue
  result+=q**sum(flat)
 return result
for q in [F(2),F(1,2)]:
 for n in range(7):check(f'D definition q={q} n={n}',D(q,n),sum(q**sum(l)for l in parts(n,2)))
 for n in range(5):check(f'Lambda Euler coefficients q={q} n={n}',lam(q,n),lambda_euler_coefficient(q,n))
 for n in range(1,5):
  check(f'281 smaller-part gaps q={q} n={n}',sum(q**sum(l)for l in parts(6*n-1,6)if allowed(l)),sum(q**(6*n*j-3*j*j+2*j)*gauss(q**6,n-j,j)*lam(q,n-2*j)for j in range(n//2+1)))
 for k,r,n in product([1,2],[1,2],range(3)):
  lhs=plane(q,k,r,n)
  mat=[[q**((i-j)*(i-j-1)//2)*gauss(q,n+r,r-i+j)for j in range(k)]for i in range(k)]
  check(f'285 plane box determinant q={q} k={k} r={r} n={n}',lhs,determinant(mat))
 for first in [(0,0),(1,0),(1,1),(2,1)]:
  for r in [1,2]:
   mat=[[q**((i-j)*(i-j-1)//2)*gauss(q,first[j]+r-1,r-i+j-1)for j in range(2)]for i in range(2)]
   check(f'284 fixed-first-column q={q} first={first} r={r}',plane(q,2,r,max(first),first),q**sum(first)*determinant(mat))
 b,c,t=F(3),F(5),F(7)
 for N in range(4):
  for x in range(N+1):
   lhs=sum(pl([q**(-N),b*q],q,n)/pl([q,q**(-N)/c],q,n)*phi([q**(-n),q**(-x),b*c*q**(x+1)],[q**(-N),b*q],q,q,min(n,x))*t**n for n in range(N+1))
   rhs=phi([q**(x-N),b*q**(x+1)],[q**(-N)/c],q,t*q**(-x),N-x)*poch(b*c*q*t,q,x)
   check(f'201 Ex9.5 normalization q={q} N={N} x={x}',lhs,rhs)
report={'kind':'exact_samples_not_proofs','passed':len(checks),'checks':checks}
Path(__file__).with_name('semantic_checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(f'{len(checks)} independent exact samples passed.')
