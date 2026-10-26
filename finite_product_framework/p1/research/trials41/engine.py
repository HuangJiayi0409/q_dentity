"""Untrusted research algebra; supports affine dependent-base Pochhammer shifts."""
import sympy as s
from inputs import P,G,n,k,q,Q,X,m,u,v

def gaussian_form(expr):
 return expr.replace(lambda t:t.func==G,lambda t:P(t.args[0],t.args[0],t.args[1])/(P(t.args[0],t.args[0],t.args[2])*P(t.args[0],t.args[0],t.args[1]-t.args[2])))

def q_exponent(expr):
 expr=s.powsimp(s.expand_power_base(expr,force=True),force=True)
 if expr==1:return s.Integer(0)
 if expr==q:return s.Integer(1)
 if expr.is_Pow and expr.base==q:return s.expand(expr.exp)
 raise ValueError('not an exact q power: '+str(expr))

def ratio(expr,index):
 if not expr.has(index):return s.Integer(1)
 if expr.func==P:
  A,B,L=expr.args
  D=q_exponent(B)
  if not D.is_Integer or D<=0:raise ValueError('unsupported base step')
  A1=A.subs(index,index+1);deltaA=s.cancel(A1/A)
  h=q_exponent(deltaA)/D
  if not h.is_Integer:raise ValueError('fractional base-step start shift: '+str(h))
  h=int(h); E=s.expand(L.subs(index,index+1)-L)
  if not E.is_Integer:raise ValueError('nonconstant length shift')
  E=int(E)
  if abs(h)>32 or abs(E)>32:raise ValueError('resource limit: long shift products')
  start=(s.prod((1-A*B**(L+j))/(1-A*B**j) for j in range(h)) if h>=0 else
         s.prod((1-A*B**j)/(1-A*B**(L+j)) for j in range(h,0)))
  length=(s.prod(1-A1*B**(L+j) for j in range(E)) if E>=0 else
          1/s.prod(1-A1*B**(L+j) for j in range(E,0)))
  return start*length
 if expr.is_Mul:return s.prod(ratio(t,index) for t in expr.args)
 if expr.is_Pow and expr.exp.is_Integer:return ratio(expr.base,index)**expr.exp
 if expr.has(P):raise ValueError('additive Pochhammer expression')
 return s.powsimp(s.expand_power_base(expr.subs(index,index+1)/expr,force=True),force=True)

def rational(expr):
 expr=s.powsimp(s.expand_power_base(expr,force=True),force=True)
 powers={}
 def convert(t):
  E=s.expand(t.exp);variables=sorted(E.free_symbols,key=str)
  if variables and s.Poly(E,*variables).total_degree()>1:raise ValueError('nonlinear shift exponent: '+str(E))
  out=s.Integer(1);constant=E
  for var in variables:
   coefficient=E.coeff(var)
   if not coefficient.is_Integer:raise ValueError('nonintegral exponent')
   symbol=Q if var==n else X if var==k else s.Symbol('E_'+str(var))
   powers[str(symbol)]=str(var);out*=symbol**coefficient;constant-=coefficient*var
  if not constant.is_Integer:raise ValueError('noninteger power constant')
  return out*q**constant
 expr=expr.replace(lambda t:t.is_Pow and t.base==q,convert)
 expr=s.cancel(expr)
 if expr.has(n,k,P) or not expr.is_rational_function(*expr.free_symbols):raise ValueError('nonrational shift: '+str(expr))
 return expr,powers

PARAMS={q:s.Rational(2,3),m:s.Integer(2),u:s.Integer(1),v:s.Integer(2)}
for name,val in zip('a b c d e f t x z w'.split(),[s.Rational(2,7),s.Rational(3,11),s.Rational(5,13),s.Rational(7,17),s.Rational(11,19),s.Rational(13,23),s.Rational(17,29),s.Rational(19,31),s.Rational(23,37),s.Rational(29,41)]):PARAMS[s.Symbol(name)]=val

def evaluate(expr,N,K=0):
 expr=expr.subs(PARAMS).subs({n:N,k:K})
 def poch(A,B,L):
  L=int(L)
  return s.sympify(s.prod(1-A*B**j for j in range(L))) if L>=0 else s.Integer(1)/s.prod(1-A*B**j for j in range(L,0))
 def gauss(t):
  B,U,L=t.args;U=int(U);L=int(L)
  if U<0 or L<0 or L>U:return s.Integer(0)
  return poch(B,B,U)/(poch(B,B,L)*poch(B,B,U-L))
 expr=expr.replace(lambda t:t.func==G,gauss)
 expr=expr.replace(lambda t:t.func==P,lambda t:poch(*t.args))
 return s.cancel(expr)

def diagnostics(case,shifts=None,powers=None):
 checks=[];mismatches=[];skipped=[]
 for N in (0,1,2):
  lo=int(evaluate(case['lo'],N));hi=int(evaluate(case['hi'],N))
  if hi-lo>40:continue
  total=0
  for K in range(lo,hi+1):
   if case['id']=='FQI-BAILEY-UNIT' and K==0:
    # Respect the original piecewise zero term, not its generic continuation.
    term=evaluate(1/(P(q,q,n)*P(s.Symbol('a')*q,q,n)),N)
   else:term=evaluate(case['F'],N,K)
   total+=term
  target=evaluate(case['T'],N)
  if (total-target).has(s.zoo,s.nan,s.oo):skipped.append({'n':N,'reason':'singular diagnostic point'});continue
  residual=s.cancel(total-target)
  checks.append({'n':N,'lower':lo,'upper':hi,'equal':residual==0})
  if residual!=0:mismatches.append({'n':N,'residual':str(residual)})
 if shifts is not None:
  checked=0
  for N in (4,5):
   lo=int(evaluate(case['lo'],N));hi=int(evaluate(case['hi'],N))
   K=(lo+hi)//2
   for key in shifts:
    A=case['F'] if key in ('U','V') else case['T']
    den=evaluate(A,N,K);num=evaluate(A,N+(key!='V'),K+(key=='V'))
    if den==0 or den.has(s.zoo,s.nan) or num.has(s.zoo,s.nan):continue
    env=dict(PARAMS);env.update({Q:PARAMS[q]**N,X:PARAMS[q]**K})
    for symbol,original in (powers or {}).items():
     if symbol not in ('Q','X'):
      old=next(t for t in PARAMS if str(t)==original);env[s.Symbol(symbol)]=PARAMS[q]**PARAMS[old]
    delta=s.cancel(num/den-shifts[key].subs(env))
    if delta!=0:raise ValueError('independent shift check failed: '+key+' '+str(delta))
    checked+=1
 else:checked=0
 return {'sum_checks':checks,'mismatches':mismatches,'skipped':skipped,'independent_shift_checks':checked,
         'sample_parameters':{str(a):str(b) for a,b in PARAMS.items()},
         'interpretation':'exact finite diagnostics only; a mismatch needs original-source/domain review, not automatic rejection of the theorem'}
