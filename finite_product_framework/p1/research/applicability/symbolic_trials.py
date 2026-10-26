"""Research probes from explicitly transcribed definitions; never Lean proof coverage.
No certificates, recurrence answers or degrees are provided as inputs.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import sympy as s
P1=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(P1))
from expressions import Poch,n,k,q,Q,X,rationalize
from search import search,Budget
from run import load_target,ROOT


def ratio(expr,index):
    if not expr.has(index):return s.Integer(1)
    if expr.func==Poch:
        a,b,L=expr.args
        a1=a.subs(index,index+1);L1=s.expand(L.subs(index,index+1))
        if b!=q:raise ValueError('probe supports base q only')
        h=s.simplify(s.expand_power_base(a1/a,force=True))
        if h==1:d=0
        elif h==q:d=1
        elif h==1/q:d=-1
        else:raise ValueError('probe only supports start shifts -1,0,1')
        shift=(s.prod((1-a*q**(L+j))/(1-a*q**j) for j in range(d)) if d>=0 else
               s.prod((1-a*q**j)/(1-a*q**(L+j)) for j in range(d,0)))
        delta=s.expand(L1-L)
        if not delta.is_Integer:raise ValueError('nonconstant length shift')
        e=int(delta)
        length=s.prod(1-a1*q**(L+j) for j in range(e)) if e>=0 else 1/s.prod(1-a1*q**(L+j) for j in range(e,0))
        return shift*length
    if expr.is_Mul:return s.prod(ratio(t,index) for t in expr.args)
    if expr.is_Pow and expr.exp.is_Integer:return ratio(expr.base,index)**expr.exp
    if expr.has(Poch):raise ValueError('unsupported additive Poch expression')
    return s.powsimp(s.expand_power_base(expr.subs(index,index+1)/expr,force=True),force=True)


def inputs():
    a,c,z=s.symbols('a c z')
    core=Poch(a,q,k)*Poch(q**(-n),q,k)/(Poch(q,q,k)*Poch(c,q,k))
    return [
      ('FQI-CHU-VANDERMONDE-Q',core*q**k,a**n*Poch(c/a,q,n)/Poch(c,q,n)),
      ('FQI-CHU-VANDERMONDE-BALANCED',core*(c*q**n/a)**k,Poch(c/a,q,n)/Poch(c,q,n)),
      ('FQI-SRC-GR2-1.Ex6iii',Poch(a,q,k)*Poch(q**(-n),q,k)/Poch(q,q,k)*((-1)**k*q**(k*(k-1)/2))**(-1)*(q**n/a)**k,a**(-n)),
      ('FQI-SRC-KAC-CHEUNG-4.4',Poch(q,q,n)/(Poch(q,q,k)*Poch(q,q,n-k))*z**k*Poch(1/z,q,k),z**n),
    ]


def diagnostics(F,T,shifts):
    """Exact small finite evaluations check the research transcription, not a proof."""
    parameters={s.Symbol('a'):s.Rational(2,7),s.Symbol('c'):s.Rational(3,11),
                s.Symbol('z'):s.Rational(5,13),q:s.Rational(2,3)}
    def value(expr,N,K=0):
        result=expr.subs(parameters).subs({n:N,k:K})
        result=result.replace(lambda t:t.func==Poch,
            lambda t:s.prod(1-t.args[0]*t.args[1]**i for i in range(int(t.args[2]))))
        return s.cancel(result)
    for N in (3,4):
        for K in (1,2):
            actual={'U':value(F,N+1,K)/value(F,N,K),
                    'V':value(F,N,K+1)/value(F,N,K),
                    'c':value(T,N+1)/value(T,N)}
            for label,ratio_value in actual.items():
                symbolic=shifts[label].subs(parameters).subs({Q:parameters[q]**N,X:parameters[q]**K})
                assert s.cancel(ratio_value-symbolic)==0,(N,K,label)
    for N in range(4):
        assert s.cancel(sum(value(F,N,K) for K in range(N+1))-value(T,N))==0,N
    return {'status':'passed','shift_checks':12,'finite_sum_checks':4,
            'scope':'exact rational diagnostics only; not general proof or Lean representation verification'}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--index',type=int,required=True);args=parser.parse_args()
    identity,F,T=inputs()[args.index]
    source=load_target(identity)
    report={'id':identity,'source':source,'input_origin':'explicit research transcription of the original formula and shared definitions',
       'lean_representation_verified':False,'automatic_train_proof':False,
       'formal_domain':'Q(q, independent parameters); special values and all original domain conditions remain Lean obligations',
       'F':str(F),'T':str(T),'status':'started','budget_seconds':30}
    try:
        shifts={name:rationalize(s.expand_power_base(ratio(expr,index),force=True))
                for name,expr,index in [('U',F,n),('V',F,k),('c',T,n)]}
        report['derived_shifts']={a:str(b) for a,b in shifts.items()}
        report['diagnostics']=diagnostics(F,T,shifts)
        result=search(shifts['U'],shifts['V'],shifts['c'],X,q,Budget(seconds=30))
        report.update(status=result['status'],construction=result)
    except Exception as e:report.update(status='probe_gap',error=f'{type(e).__name__}: {e}')
    report['probe_code_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    report['source_unchanged']=hashlib.sha256((ROOT/source['path']).read_bytes()).hexdigest()==source['sha256']
    out=Path(__file__).parent/'trials';out.mkdir(exist_ok=True)
    (out/(identity+'.json')).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(identity,report['status'],report.get('error',''))


if __name__=='__main__':main()
