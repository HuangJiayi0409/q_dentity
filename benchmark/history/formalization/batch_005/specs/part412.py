from common import *
S={};q,x,a=vs('q x a')
base='(hq : q ≠ 0) (hq1 : q ≠ 1)'
S[412]=f'''(q x : ℂ) (f g : ℂ → ℂ) {base} (hx : x ≠ 0) :
 jackson q (fun y => f y*g y) x = f (q*x)*jackson q g x+g x*jackson q f x ∧
 f (q*x)*jackson q g x+g x*jackson q f x = f x*jackson q g x+g (q*x)*jackson q f x'''
S[413]=f'''(q x : ℂ) (f g : ℂ → ℂ) {base}
 (hx : x ≠ 0) (hg : g x*g (q*x) ≠ 0) :
 jackson q (fun y => f y/g y) x = (g x*jackson q f x-f x*jackson q g x)/(g x*g (q*x)) ∧
 (g x*jackson q f x-f x*jackson q g x)/(g x*g (q*x)) =
 (g (q*x)*jackson q f x-f (q*x)*jackson q g x)/(g x*g (q*x))'''
S[414]=f'''(q x a : ℂ) (beta : ℤ) (f : ℂ → ℂ) {base}
 (hb : beta ≠ 0) (hax : a*x ≠ 0) (hqb : q^beta ≠ 1) :
 jackson q (fun y => f (a*y^beta)) x = jackson (q^beta) f (a*x^beta)*jackson q (fun y => a*y^beta) x'''
def KP(x,a,n):return E(f'(kacPower {x} {a} q ({n}))',(f'kacPowerDefined {x} {a} q ({n})',))
def J1(n,inverse=False):
 u=KP(x,a,n);v=KP(q*x,a,n)
 return E(f'(jackson q (fun y => {"1/" if inverse else ""}kacPower y a q ({n})) x)',uniq(u.req+v.req+((f'{u} ≠ 0',f'{v} ≠ 0')if inverse else())))
def J2(n,inverse=False):
 u=KP(a,x,n);v=KP(a,q*x,n)
 return E(f'(jackson q (fun y => {"1/" if inverse else ""}kacPower a y q ({n})) x)',uniq(u.req+v.req+((f'{u} ≠ 0',f'{v} ≠ 0')if inverse else())))
S[415]=ST('(q x a : ℂ) (n : ℤ)',J1('n'),e('(qInteger q n)')*KP(x,a,'n-1'),base+' (hx : x ≠ 0)')
S[416]=ST('(q x a : K) (m n : ℤ)',KP(x,a,'m+n'),KP(x,a,'m')*KP(x,e('(q^m*a)'),'n'),base)
S[417]=ST('(q x a : K) (n : ℤ)',KP(a,x,'n'),e('((-1:K)^n*q^(n*(n-1)/2))')*KP(x,e('(q^(1-n)*a)'),'n'),base)
S[418]=ST('(q x a : ℂ) (n : ℤ)',J1('n',True),e('(qInteger q (-n))')*KP(x,e('(q^n*a)'),'-n-1'),base+' (hx : x ≠ 0)')
S[419]=ST('(q x a : ℂ) (n : ℤ)',J2('n'),-e('(qInteger q n)')*KP(a,q*x,'n-1'),base+' (hx : x ≠ 0)')
S[420]=ST('(q x a : ℂ) (n : ℤ)',J2('n',True),e('(qInteger q n)')/KP(a,x,'n+1'),base+' (hx : x ≠ 0)')
