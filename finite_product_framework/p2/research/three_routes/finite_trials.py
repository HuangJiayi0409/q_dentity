"""Exact, fixed-degree diagnostics; independently computed connection coefficients.

These are explicit transcriptions, NOT native Lean extraction or general proofs.
Target coefficient formulas are only used after the triangular solve.
"""
from pathlib import Path
import hashlib
import json
import sympy as s

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
q = s.Rational(2, 3)
z, t, alpha, cc = s.symbols('z t alpha cc')


def poch(a, n):
    return s.prod((1-a*q**i for i in range(n)), start=s.S.One)


def pl(xs, n):
    return s.prod((poch(a, n) for a in xs), start=s.S.One)


def phi(aa, bb, v, n):
    terms = []
    for k in range(n+1):
        den = pl(bb, k)*poch(q, k)
        if den == 0:
            raise ValueError('undefined finite term')
        terms.append(pl(aa, k)/den*v**k *
                     ((-1)**k*q**(k*(k-1)//2))**(1+len(bb)-len(aa)))
    result=s.cancel(sum(terms))
    assert not result.has(s.Float), 'exact arithmetic required'
    return result


def aw(a,b,c,d,n):
    return s.cancel(a**(-n)*pl([a*b,a*c,a*d],n)*
                    phi([q**(-n),a*b*c*d*q**(n-1),a*z,a/z],[a*b,a*c,a*d],q,n))


def jac(a,b,n):
    return phi([q**(-n),a*b*q**(n+1)],[a*q],q*t,n)


def connect(poly, basis, var, n, laurent=False):
    # Descending leading coefficient elimination; no target answer enters here.
    def expanded(expr):
        shift=n if laurent else 0
        polynomial=s.Poly(s.cancel(expr*var**shift),var)
        return sum(coef*var**(power[0]-shift) for power,coef in polynomial.terms())
    residual = expanded(poly)
    result = [s.S.Zero]*(n+1)
    for k in range(n,-1,-1):
        element = expanded(basis[k])
        pivot = element.coeff(var,k)
        assert pivot != 0
        result[k] = s.cancel(residual.coeff(var,k)/pivot)
        residual = expanded(residual-result[k]*element)
    assert s.cancel(residual) == 0
    return result


def main():
    table=json.loads((ROOT/'finite_product_framework/research/train_a_methods/table.json').read_text())
    ids=['FQI-SRC-GR2-7.6.8','FQI-SRC-GR2-9.Ex5ii','FQI-SRC-GR2-1.Ex33']
    sources=[]
    for r in table['entries']:
        if r['id'] in ids:
            path=ROOT/r['lean_path']
            assert hashlib.sha256(path.read_bytes()).hexdigest()==r['lean_sha256']
            sources.append({k:r[k] for k in ['id','lean_path','lean_sha256','lean_statement','formula_latex']})
    assert len(sources)==3
    (HERE/'inputs.json').write_text(json.dumps(sources,ensure_ascii=False,indent=2)+'\n')
    a,b,c,d=map(s.Rational,['1/13','1/5','2/7','3/11'])
    results=[]
    for n in range(4):
        basis=[aw(a,b,c,d,k) for k in range(n+1)]
        got=connect(aw(alpha,b,c,d,n),basis,z,n,True)
        expected=[s.cancel(poch(alpha/a,n-k)*poch(alpha*b*c*d*q**(n-1),k)*
                    pl([q,b*c,b*d,c*d],n)*a**(n-k)/
                    (pl([q,b*c,b*d,c*d],k)*poch(a*b*c*d*q**(k-1),k)*
                     pl([q,a*b*c*d*q**(2*k)],n-k))) for k in range(n+1)]
        assert all(s.cancel(u-v)==0 for u,v in zip(got,expected))
        assert s.cancel(got[0]-(expected[0]+1)) != 0
        results.append({'id':ids[0],'n':n,'status':'fixed_degree_exact_match',
                        'free_parameters':['alpha','z'],'computed_coefficients':list(map(str,got)),
                        'algorithm':'triangular Laurent coefficient elimination; not specialized AW paper algorithm'})
        print('AW',n,'passed',flush=True)
    for n in range(5):
        got=connect(jac(cc,d,n),[jac(a,b,k) for k in range(n+1)],t,n)
        expected=[s.cancel((-1)**k*q**(k*(k+1)//2)*pl([q**(-n),a*q,cc*d*q**(n+1)],k)/
                    pl([q,cc*q,a*b*q**(k+1)],k)*
                    phi([q**(k-n),cc*d*q**(n+k+1),a*q**(k+1)],
                        [cc*q**(k+1),a*b*q**(2*k+2)],q,n-k)) for k in range(n+1)]
        assert all(s.cancel(u-v)==0 for u,v in zip(got,expected))
        assert s.cancel(got[0]-(expected[0]+1)) != 0
        results.append({'id':ids[2],'n':n,'status':'fixed_degree_exact_match',
                        'free_parameters':['cc','t'],'computed_coefficients':list(map(str,got)),
                        'algorithm':'triangular basis inversion'})
        print('Jacobi',n,'passed',flush=True)
    for N in range(6):
        for x in range(N+1):
            lhs=sum(pl([q**(-N),b*q],n)/pl([q,q**(-N)/c],n)*
                    phi([q**(-n),q**(-x),b*c*q**(x+1)],[q**(-N),b*q],q,min(n,x))*t**n
                    for n in range(N+1))
            rhs=phi([q**(x-N),b*q**(x+1)],[q**(-N)/c],t*q**(-x),N-x)*poch(b*c*q*t,x)
            assert s.cancel(lhs-rhs)==0
            assert s.cancel(lhs-(rhs+1)) != 0
            results.append({'id':ids[1],'N':N,'x':x,'status':'fixed_degree_exact_match',
                            'free_parameters':['t'],'algorithm':'exact coefficient expansion; not qFPS proof'})
        print('GF',N,'passed',flush=True)
    report={'status':'passed','scope':'three P2 train inputs only','results':results,
            'specialized_parameters':{'q':str(q),'a':str(a),'b':str(b),'c':str(c),'d':str(d)},
            'new_lean_proofs':0,'general_parameter_proofs':0,
            'limitations':['Explicit formula transcription has not been linked to Lean Expr',
                           'Fixed integer degrees and specialized parameters are diagnostic only',
                           'Free symbolic parameter results hold as rational functions away from poles',
                           'AW diagnostic uses triangular elimination, not the specialized operator algorithm']}
    (HERE/'finite_results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':
    main()
