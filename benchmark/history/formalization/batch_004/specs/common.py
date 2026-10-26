"""Hand-authored expression builder; carries only actual denominator obligations.
No LaTeX parser or mathematical inference is used. Bound obligations stay under sums.
"""
import re
from dataclasses import dataclass

def uniq(xs): return tuple(dict.fromkeys(xs))
@dataclass(frozen=True)
class E:
    text: str
    req: tuple = ()
    def __str__(self): return self.text
    def op(self, b, op):
        b=e(b); return E(f'({self} {op} {b})',uniq(self.req+b.req))
    def __add__(self,b): return self.op(b,'+')
    def __radd__(self,b): return e(b)+self
    def __sub__(self,b): return self.op(b,'-')
    def __rsub__(self,b): return e(b)-self
    def __mul__(self,b): return self.op(b,'*')
    def __rmul__(self,b): return e(b)*self
    def __truediv__(self,b):
        b=e(b);x=self.op(b,'/');return E(x.text,uniq(x.req+(f'{b} ≠ 0',)))
    def __rtruediv__(self,b): return e(b)/self
    def __neg__(self): return E(f'(-{self})',self.req)
    def __pow__(self,n): return E(f'({self}^{n})',self.req)
def e(x): return x if isinstance(x,E)else E(str(x))
def vs(s): return tuple(e(x)for x in s.split())
def conj(req): return ' ∧\n    '.join(uniq(req)) or 'True'
def args(xs): return '['+','.join(map(str,xs))+']'
def combine(xs): return uniq(sum((e(x).req for x in xs),()))
def Z(s):
    # Integer arithmetic for exponents: prevents truncated natural subtraction.
    return re.sub(r'\b((?:Kcap|[nmjkrsxyzNMLKR]))\b',r'(\1 : ℤ)',str(s))
def zp(a,s): return E(f'({a}^(({Z(s)}) : ℤ))',e(a).req)
def Q(s): return zp(e('q'),s)
def P(xs,n,q=None):
    q=e('q') if q is None else e(q);xs=list(map(e,xs));return E(f'(pochList {args(xs)} {q} ({n}))',combine(xs+[q]))
def PH(xs,ys,n,z=None,q=None):
    q=e('q')if q is None else e(q);z=q if z is None else e(z);xs=list(map(e,xs));ys=list(map(e,ys))
    return E(f'(phi {args(xs)} {args(ys)} {q} {z} ({n}))',uniq(combine(xs+ys+[q,z])+(f'phiDefined {args(ys)} {q} ({n})',)))
def W(a,bs,n,z=None,q=None):
    q=e('q')if q is None else e(q);z=q if z is None else e(z);a=e(a);bs=list(map(e,bs))
    return E(f'(wellPoisedRaw {a} {args(bs)} {q} {z} ({n}))',uniq(combine([a,q,z]+bs)+(f'wDefined {a} {args(bs)} {q} ({n})',)))
def BI(xs,ys,us,vs,n,z,p=None,q=None):
    p=e('(q^2)')if p is None else e(p);q=e('q')if q is None else e(q);z=e(z)
    xs,ys,us,vs=map(lambda t:list(map(e,t)),[xs,ys,us,vs])
    return E(f'(bibasicPhi {args(xs)} {args(ys)} {args(us)} {args(vs)} {p} {q} {z} ({n}))',uniq(combine(xs+ys+us+vs+[p,q,z])+(f'phiDefined {args(ys)} {p} ({n})',f'∀ k ≤ ({n}), pochList {args(vs)} {q} k ≠ 0')))
def SUM(k,hi,f,lo='0'):
    v=e(k);term=e(f(v));scope=f'Finset.range ({hi}+1)' if lo=='0'else f'Finset.Icc ({lo}) ({hi})'
    req=()if not term.req else (f'∀ {k} ∈ {scope}, ({conj(term.req)})',)
    return E(f'(∑ {k} ∈ {scope}, {term})',req)
def CALL(name,params,req=()):
    return E('('+name+' '+' '.join('('+str(x)+')'for x in params)+')',uniq(combine(params)+tuple(req)))
def statement(params,l,r,extra='',base='q',field='K'):
    l,r=e(l),e(r);domain=conj(l.req+r.req)
    return f'''{params}
 (hbase : regular {base}) {extra}
 (h_domain : {domain}) :
 {l} = {r}'''
def RISE(xs,n):
    xs=list(map(e,xs));return E(f'(risingList {args(xs)} ({n}))',combine(xs))
def PI(xs,k,q=None):
    q=e('q') if q is None else e(q);xs=list(map(e,xs));return E(f'(pochListInt {args(xs)} {q} ({Z(k)}))',uniq(combine(xs+[q])+(f'pochListIntDefined {args(xs)} {q} ({Z(k)})',)))
def KT(a,b,c,p,q,k):
    return (1-a*zp(p,k)*zp(q,k))*(1-b*zp(p,k)*zp(q,'-'+k))/((1-a)*(1-b))*P([a,b],k,p)*P([c,a/(b*c)],k,q)*zp(q,k)/(P([q,a*q/b],k,q)*P([a*p/c,b*c*p],k,p))
def TT(a,b,c,p,q,n):
    return P([a*p,b*p],n,p)*P([c*q,a*q/(b*c)],n,q)/(P([q,a*q/b],n,q)*P([a*p/c,b*c*p],n,p))
def RT(a,b,c,p,q,n,k):
    return P([c*zp(p,'-'+n)/a,zp(p,'-'+n)/(b*c)],k,p)*P([zp(q,'-'+n),b*zp(q,'-'+n)/a],k,q)/(P([zp(q,'-'+n)/c,b*c*zp(q,'-'+n)/a],k,q)*P([zp(p,'-'+n)/a,zp(p,'-'+n)/b],k,p))
def AW(z,a,b,c,d,n,q=None):
    q=e('q')if q is None else q
    expr=PH([zp(q,'-'+n),a*b*c*d*zp(q,n+'-1'),a*z,a/z],[a*b,a*c,a*d],n,q,q)
    return E(f'(askeyWilson ({z}) ({a}) ({b}) ({c}) ({d}) ({q}) ({n}))',uniq(expr.req+(f'{a} ≠ 0',)))
def UL(z,b,n):
    return E(f'(ultraspherical {b} {z} q ({n}))',uniq(combine([z,b])+(f'{z} ≠ 0',f'∀ k ≤ ({n}), poch q q k ≠ 0')))
def LJ(x,a,b,n):return PH([Q('-('+n+')'),a*b*Q(n+'+1')],[a*e('q')],n,e('q')*x)
def BJ(x,a,b,c,n):return PH([Q('-('+n+')'),a*b*Q(n+'+1'),x],[a*e('q'),c*e('q')],n)
def RC(t,a,b,c,d,n):return PH([Q('-('+n+')'),a*b*Q(n+'+1'),t,c*d*e('q')/t],[a*e('q'),c*e('q'),b*d*e('q')],n)
def WR(x,a,b,c,N,n):return PH([Q('-('+n+')'),a*b*Q(n+'+1'),Q('-('+x+')'),c*Q(x+'-('+N+')')],[a*e('q'),Q('-('+N+')'),b*c*e('q')],f'min ({n}) ({x})')
def HAHN(x,a,b,N,n):return PH([Q('-('+n+')'),a*b*Q(n+'+1'),Q('-('+x+')')],[a*e('q'),Q('-('+N+')')],f'min ({n}) ({x})')
def DH(x,b,c,N,n):return PH([Q('-('+n+')'),Q('-('+x+')'),c*Q(x+'-('+N+')')],[Q('-('+N+')'),b*c*e('q')],f'min ({n}) ({x})')
def KD(m,n):return e(f'(if ({m}) = ({n}) then (1 : K) else 0)')
def PREV(x,condition='n = 0'):
    return E(f'(if {condition} then 0 else {x})',tuple(f'¬ ({condition}) → ({r})'for r in x.req))
def MUL0(c,x):
    c,x=e(c),e(x)
    return E(f'(if {c} = 0 then 0 else {c}*{x})',uniq(c.req+tuple(f'{c} ≠ 0 → ({r})'for r in x.req)))
def claims(params,pairs,extra='',base='q'):
    req=uniq(sum((e(l).req+e(r).req for l,r in pairs),()))
    return f'{params}\n (hbase : regular {base}) {extra}\n (h_domain : {conj(req)}) :\n '+ ' ∧\n '.join(f'{l} = {r}'for l,r in pairs)
def RHO(x,a,b,c,N):
    q=e('q');return P([c*Q('-('+N+')'),a*q,b*c*q,Q('-('+N+')')],x)*(1-c*Q('2*('+x+')-('+N+')'))/(P([q,c*Q('-('+N+')')/a,Q('-('+N+')')/b,c*q],x)*(1-c*Q('-('+N+')')))*zp(a*b*q,'-('+x+')')
def HN(n,a,b,c,N):
    q=e('q');return P([b*q,a*q/c],N)/P([a*b*q*q,1/c],N)*P([a*b*q,a*q,b*c*q,Q('-('+N+')')],n)*(1-a*b*Q('2*('+n+')+1'))*Q('('+N+')*('+n+')')*zp(c,'-('+n+')')/(P([q,b*q,a*q/c,a*b*Q(N+'+2')],n)*(1-a*b*q))
def FN(a,d,u,v,w,n):return PH([Q('-('+n+')'),a*Q(n),u,v],[d,w,e('q')*a*u*v/(d*w)],n)
def KA_RS(a,b,c,alpha,gamma,N,M,x,y,r,s):
    return PH([Q('-('+s+')'),Q('('+r+')-('+y+')'),gamma*Q('('+r+')+('+y+')-('+M+')'),a*Q('('+r+')+1'),b*c*Q('('+r+')+1')],[alpha*Q('('+r+')+1'),Q('('+r+')-('+M+')'),a*b*gamma*Q('('+r+')+1')/alpha,c*Q('1+('+r+')-('+s+')')],s)
def KH_RS(a,b,c,alpha,gamma,N,M,x,y,r,s):
    q=e('q');return P([Q('-('+x+')'),c*Q('('+x+')-('+N+')'),Q('-('+y+')'),gamma*Q('('+y+')-('+M+')')],r)*P([Q('('+x+')-('+N+')'),Q('-('+x+')')/c],s)*(1-c*Q('('+r+')-('+s+')'))*Q('-('+r+')*('+s+')')/(P([q,alpha*q,Q('-('+M+')'),a*b*gamma*q/alpha,c*Q('1-('+s+')')],r)*P([q,b*q,a*q/c],s)*(1-c*Q('-('+s+')')))
def WAUTO(a,bs,n,z=None,q=None):
    q=e('q')if q is None else q;cut=f'firstTermination {args([e(a)]+list(bs))} {q} ({n})'
    return W(a,bs,cut,z,q)

# Fourth batch uses actual finite denominator domains, not generic root exclusions.
def ST(params,l,r,extra=''):
    return statement(params,l,r,extra).replace(' (hbase : regular q)','')
def CL(params,pairs,extra=''):
    return claims(params,pairs,extra).replace(' (hbase : regular q)','')
def G(n,k,q=None):return e(f'(gaussian {q if q is not None else "q"} ({n}) ({k}))')
def GI(n,k,q=None):return e(f'(gaussianInt {q if q is not None else "q"} ({n}) ({k}))')
def ISUM(v,lo,hi,f):
 t=e(f(e(v)));scope=f'Finset.Icc ({lo} : ℤ) ({hi} : ℤ)'
 return E(f'(∑ {v} ∈ {scope}, {t})',()if not t.req else(f'∀ {v} ∈ {scope}, ({conj(t.req)})',))
def BA(a,q,N,fn):
 return SUM('r',N,lambda r:fn(r)/(P([q],f'{N}-r',q)*P([a*q],f'{N}+r',q)))
