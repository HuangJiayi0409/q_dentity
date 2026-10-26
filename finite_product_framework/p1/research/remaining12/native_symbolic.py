#!/usr/bin/env python3
"""Read actual Lean Expr exports. Generic symbolic construction, NOT a Lean proof.

No formula-specific inputs, certificate tables, or identifier-based mathematics.
Nat subtraction/toNat and singular parameter bridges remain explicit obligations.
"""
import json,sys,hashlib,signal,time
from pathlib import Path
HERE=Path(__file__).resolve().parent;P1=HERE.parents[1]
sys.path.insert(0,str(P1));sys.path.insert(0,str(P1/'research/trials41'))
import sympy as s
from inputs import P,G,n,k,q,Q,X,m,u,v
from engine import gaussian_form,ratio,rational,diagnostics
from search import search,Budget
from qgosper import antidifference
from run import load_target

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2,default=str)+'\n')
def pl(params,base,L):return s.prod(P(a,base,L) for a in params)
def read(node,env):
    op=node['op']
    if op=='var':return env.get(node['name'],s.Symbol(node['name']))
    if op=='nat':return s.Integer(node['value'])
    aa=[read(a,env) for a in node.get('args',[])]
    if op in ('Nat.cast','Int.ofNat','Int.toNat'):return aa[0]
    if op=='List.nil':return []
    if op=='List.cons':return [aa[0]]+aa[1]
    if op=='Neg.neg':return -aa[0]
    if op=='Eq':return s.Eq(*aa)
    if op=='ite':return s.Piecewise((aa[1],aa[0]),(aa[2],True))
    if op in ('HAdd.hAdd','HSub.hSub','HMul.hMul','HDiv.hDiv','HPow.hPow'):
        a,b=aa
        return {'HAdd.hAdd':lambda:a+b,'HSub.hSub':lambda:a-b,'HMul.hMul':lambda:a*b,
                'HDiv.hDiv':lambda:a/b,'HPow.hPow':lambda:a**b}[op]()
    if op=='FiniteQBenchmark.poch':return P(*aa)
    if op=='FiniteQBenchmark.pochList':return pl(*aa)
    if op in ('FiniteQBenchmark.gaussian','FiniteQBenchmark.gaussianInt'):return G(*aa)
    if op=='FiniteQBenchmark.unitBailey':
        a,b,j=aa
        return s.Piecewise((1,s.Eq(j,0)),
             ((-1)**j*b**(j*(j-1)/2)*(1-a*b**(2*j))*P(a*b,b,j-1)/P(b,b,j),True))
    if op=='FiniteQBenchmark.sillsAlpha':
        a,b,D,H,j=aa
        if D!=1:raise ValueError('divisibility support requires a separate residue transformation')
        return (-1)**j*a**((H-D)*j)*b**s.expand((D*(2*H-2*D+1)*j*j-D*j)/2)*(1-a*b**(2*D*j))*P(a,b**D,j)/((1-a)*P(b**D,b**D,j))
    raise ValueError('unhandled native node: '+op)

def sum_node(node):
    if node['op'] in ('Finset.sum','FiniteQBenchmark.phi'):return node
    if node['op']=='HMul.hMul':
        nodes=[sum_node(c) for c in node['args']]
        if sum(x is not None for x in nodes)==1:return next(x for x in nodes if x is not None)
    return None

def index_name(node):
    if node['op'] in ('Nat.cast','Int.ofNat'):return index_name(node['args'][0])
    if node['op']!='var':raise ValueError('non-variable main index')
    return node['name']

def parse(raw,hypotheses):
    assert raw['op']=='Eq'
    left,right=raw['args'];sm=sum_node(left)
    if sm is None:left,right=right,left;sm=sum_node(left)
    if sm is None:raise ValueError('single sum required')
    if sm['op']=='FiniteQBenchmark.phi':
        main=index_name(sm['args'][-1]);binder=None;lo=s.Integer(0);hi=n
    else:
        domain,body=sm['args'];binder=body['name']
        if domain['op']=='Finset.range':
            end=domain['args'][0];assert end['op']=='HAdd.hAdd' and end['args'][1]=={'op':'nat','value':1}
            main=index_name(end['args'][0]);lo=s.Integer(0);hi=n
        elif domain['op']=='Finset.Icc':
            main=index_name(domain['args'][1]);lo=-n;hi=n
        else:raise ValueError('unsupported interval')
    env={'n':n,'m':m,'u':u,'v':v,main:n}
    if binder:env[binder]=k
    if sm['op']=='FiniteQBenchmark.phi':
        aa,bb,base,z,N=[read(x,env) for x in sm['args']]
        F=pl(aa,base,k)/pl([base]+bb,base,k)*((-1)**k*base**(k*(k-1)/2))**(1+len(bb)-len(aa))*z**k
    else:
        F=read(sm['args'][1]['body'],env)
        if sm['args'][0]['op']=='Finset.Icc':
            lo,hi=[read(x,env) for x in sm['args'][0]['args']]
    def outside(node):
        if node is sm:return s.Integer(1)
        if sum_node(node) is None:return read(node,env)
        assert node['op']=='HMul.hMul'
        return s.prod(outside(a) for a in node['args'])
    F*=outside(left);T=read(right,env)
    substitutions=[]
    for h in hypotheses:
        ty=h['type']
        if ty['op']=='Eq':
            A,B=[read(x,env) for x in ty['args']]
            if A.is_Symbol and not B.has(A):sub={A:B}
            elif B.is_Symbol and not A.has(B):sub={B:A}
            else:continue
            if next(iter(sub)) in (n,k):continue
            F=F.subs(sub);T=T.subs(sub);substitutions.append({'hypothesis':h['name'],'substitution':str(sub)})
    bases=set()
    for atom in F.atoms(s.Function)|T.atoms(s.Function):
        if atom.func in (P,G):
            base=atom.args[1] if atom.func==P else atom.args[0]
            bases.update(base.free_symbols)
    if len(bases)!=1:raise ValueError('not a single dependent base: '+str(bases))
    base=bases.pop();F=F.subs(base,q);T=T.subs(base,q)
    generic=F.replace(lambda t:t.func==s.Piecewise,lambda t:t.args[-1][0])
    route='direct' if T.has(s.Piecewise) else 'qwz'
    return {'id':'native_diagnostic','F':F,'T':T,'lo':lo,'hi':hi,'route':route},generic,substitutions,str(base)

def timeout(signum,frame):raise TimeoutError('stage wall-clock budget exhausted')
def trial(identity):
    path=HERE/'native'/identity
    raw=json.loads((path/'lean_expression.json').read_text())
    hypotheses=json.loads((path/'lean_hypotheses.json').read_text())
    out=HERE/identity/'native_symbolic.json'
    report={'id':identity,'source':load_target(identity),'input_origin':'actual Lean Expr export',
       'goal_export_sha256':digest(path/'lean_expression.json'),
       'hypotheses_export_sha256':digest(path/'lean_hypotheses.json'),
       'translator_sha256':digest(Path(__file__)), 'automatic_train_proof':False,
       'obligations':['Lean normalization of Nat subtraction, toNat, named functions and parameter equality',
                      'Original-domain denominator propagation and exceptional terms',
                      'Boundary, initial values and original-goal proof assembly']}
    signal.signal(signal.SIGALRM,timeout);signal.setitimer(signal.ITIMER_REAL,90)
    try:
        case,F,substitutions,base=parse(raw,hypotheses)
        report.update(case={key:str(v) for key,v in case.items()},search_summand=str(F),
                      substitutions=substitutions,chosen_base=base,stage='finite_diagnostics')
        diag=diagnostics(case);report['diagnostics']=diag
        if diag['mismatches']:raise ValueError('finite original-expression diagnostics mismatch')
        report['stage']='shift_derivation';shifts={};powers={}
        for key,expr,var in ([('V',F,k)] if case['route']=='direct' else [('U',F,n),('V',F,k),('c',case['T'],n)]):
            shifts[key],new=rational(ratio(gaussian_form(expr),var));powers.update(new)
        report['shifts']={a:str(b) for a,b in shifts.items()};report['power_symbols']=powers
        report['diagnostics']=diagnostics(case,shifts,powers)
        report['stage']='q_gosper';signal.setitimer(signal.ITIMER_REAL,30)
        if case['route']=='direct':
            result=antidifference(s.cancel(shifts['V'].subs(X,X/q)),X,q,Budget(seconds=30))
            if result['status']=='constructed':
                R=result['antidifference_ratio'];assert s.cancel(shifts['V']*R.subs(X,q*X)-R-1)==0
        else:
            result=search(shifts['U'],shifts['V'],shifts['c'],X,q,Budget(seconds=30))
            if result['status']=='constructed':
                env={str(t):t for e in shifts.values() for t in e.free_symbols}
                R=s.sympify(result['certificate'],locals=env)
                assert s.cancel(shifts['V']*R.subs(X,q*X)-R-shifts['U']+shifts['c'])==0
        report.update(status=result['status'],construction=result,stage='finished')
    except TimeoutError as exc:report.update(status='timeout',error=str(exc))
    except Exception as exc:report.update(status='native_symbolic_gap',error=f'{type(exc).__name__}: {exc}')
    finally:
        signal.setitimer(signal.ITIMER_REAL,0);write(out,report)
    return report

if __name__=='__main__':
    for identity in json.loads((HERE/'selection.json').read_text())['identities']:
        r=trial(identity);print(identity,r['status'],r.get('error',''),flush=True)
