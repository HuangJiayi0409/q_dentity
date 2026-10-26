from common import *
S={};q,a,b,c,d,ee,f,g,lam=vs('q a b c d ee f g lam')
def prod(i,typ,fn,filter=None):
 t=e(fn(e(i)));scope=f'(Finset.univ : Finset ({typ}))'+(f'.filter ({filter})'if filter else '')
 return E(f'(∏ {i} ∈ {scope}, {t})',()if not t.req else (f'∀ {i} ∈ {scope}, ({conj(t.req)})',))
def at(v,i):return e(f'({v} {i})')
def ki(i):return e(f'((k {i}).val)')
def PQ(i):return e(f'(q^((k {i}).val))')
def PD(xs,idx,base=q):return P(xs,f'(k {idx}).val',base)
def tot():return e('(∑ i, (k i).val)')
def vand():return e('(vandermonde (fun i => z i*q^((k i).val)))')/e('(vandermonde z)')
def summ(term,sub=False,box=False):
 scope='(Finset.univ : Finset ((i : Fin ell) → Fin (m i+1)))'if box else f'({"subCompositions" if sub else "compositions"} d N)'
 return E(f'(∑ k ∈ {scope}, {term})',(f'∀ k ∈ {scope}, ({conj(term.req)})',))
def nz(ds='d'):return f'(hd : 0 < {ds}) (hz : ∀ i, z i ≠ 0) (hzd : Function.Injective z)'
term=vand()*prod('r','Fin d',lambda r:prod('s','Fin d',lambda s:PD([at('aa',r)*at('z',s)/at('z',r)],s)/PD([q*at('z',s)/at('z',r)],s)))
rhs=P([e('(∏ i, aa i)')],'N')/P([q],'N')
S[210]=statement('(q : K) (d N : ℕ) (aa z : Fin d → K)',summ(term),rhs,nz())
term=vand()*prod('r','Fin d',lambda r:prod('s','Fin (d+1)',lambda s:PD([at('aa',s)*at('z',r)],r))/(PD([b*at('z',r)],r)*prod('s','Fin d',lambda s:PD([q*at('z',r)/at('z',s)],r))))
rhs=prod('s','Fin (d+1)',lambda s:P([b/at('aa',s)],'N'))/(P([q],'N')*prod('r','Fin d',lambda r:P([b*at('z',r)],'N')))
S[211]=statement('(q b : K) (d N : ℕ) (aa : Fin (d+1) → K) (z : Fin d → K)',summ(term),rhs,nz()+' (ha : ∀ i, aa i ≠ 0) (hb : b = (∏ i, aa i)*(∏ i, z i))')
def cross():return prod('r','Fin d',lambda r:prod('s','Fin d',lambda s:1/P([at('z',r)*at('z',s)],'(k r).val+(k s).val'),filter='fun s => r < s'))
term=vand()*cross()*prod('s','Fin d',lambda s:at('z',s)**'((k s).val)'*e('(q^((k s).val*((k s).val-1)/2))')*prod('r','Fin (d-1)',lambda r:PD([at('z',s)*at('aa',r),at('z',s)/at('aa',r)],s))/(PD([b*at('z',s),at('z',s)*Q('1-N')/b],s)*prod('r','Fin d',lambda r:PD([q*at('z',s)/at('z',r)],s))))
rhs=(-b*Q('N-1'))**'N'*prod('s','Fin (d-1)',lambda s:P([b*at('aa',s),b/at('aa',s)],'N'))/(P([q],'N')*prod('s','Fin d',lambda s:P([b*at('z',s),b/at('z',s)],'N')))
S[216]=statement('(q b : K) (d N : ℕ) (aa : Fin (d-1) → K) (z : Fin d → K)',summ(term),rhs,nz()+' (ha : ∀ i, aa i ≠ 0) (hb : b ≠ 0)')
term=vand()*prod('s','Fin d',lambda s:(1-a*at('z',s)*e('(q^((k s).val + ∑ i, (k i).val))'))/(1-a*at('z',s)))*cross()*prod('r','Fin d',lambda r:prod('s','Fin d',lambda s:PD([at('z',s)*at('bs',r),at('z',s)/at('bs',r)],s)/PD([q*at('z',s)/at('z',r)],s)))*prod('r','Fin d',lambda r:P([a*at('z',r)],'∑ i, (k i).val')*P([a*q/at('z',r)],'(∑ i, (k i).val)-(k r).val')/P([a*q*at('bs',r),a*q/at('bs',r)],'∑ i, (k i).val'))*P([Q('-N'),c,a**'2'*Q('N+1')/c],'∑ i, (k i).val')*e('(q^(∑ i, (k i).val))')/prod('s','Fin d',lambda s:PD([a*q*at('z',s)/c,c*at('z',s)/(a*Q('N')),a*at('z',s)*Q('N+1')],s))
rhs=prod('s','Fin d',lambda s:P([a*q*at('z',s),a*q/at('z',s),a*q*at('bs',s)/c,a*q/(at('bs',s)*c)],'N')/P([a*q*at('z',s)/c,a*q/(at('z',s)*c),a*q*at('bs',s),a*q/at('bs',s)],'N'))
S[217]=statement('(q a c : K) (d N : ℕ) (bs z : Fin d → K)',summ(term,sub=True),rhs,nz()+' (ha : a ≠ 0) (hc : c ≠ 0) (hb : ∀ i, bs i ≠ 0)')
# Rosengren corollary 8.1, p=0; dependent Fin types enumerate the entire box.
def SC(A,B,C,D,Ee,F,G):
 term=vand()*e('(q^(∑ i, (k i).val))')*prod('s','Fin ell',lambda s:(1-A*at('z',s)*e('(q^((k s).val + ∑ i, (k i).val))'))/(1-A*at('z',s)))*P([B,C,D],'∑ i, (k i).val')/P([A*q/Ee,A*q/F,A*q/G],'∑ i, (k i).val')*prod('r','Fin ell',lambda r:P([A*at('z',r)],'∑ i, (k i).val')/P([A*at('z',r)*e('(q^(m r+1))')],'∑ i, (k i).val'))*prod('s','Fin ell',lambda s:PD([Ee*at('z',s),F*at('z',s),G*at('z',s)],s)/PD([A*q*at('z',s)/B,A*q*at('z',s)/C,A*q*at('z',s)/D],s))*prod('r','Fin ell',lambda r:prod('s','Fin ell',lambda s:PD([e('(q^(-(m r:ℤ)))')*at('z',s)/at('z',r)],s)/PD([q*at('z',s)/at('z',r)],s)))
 return summ(term,box=True)
rhs=(a/lam)**'(∑ i, m i)'*P([lam*q/f,lam*q/g],'∑ i, m i')/P([a*q/f,a*q/g],'∑ i, m i')*prod('s','Fin ell',lambda s:P([a*q*at('z',s),lam*q*at('z',s)/d],'m s')/P([lam*q*at('z',s),a*q*at('z',s)/d],'m s'))*SC(lam,lam*b/a,lam*c/a,d,lam*ee/a,f,g)
S[218]=statement('(q a b c d ee f g lam : K) (ell : ℕ) (m : Fin ell → ℕ) (z : Fin ell → K)',SC(a,b,c,d,ee,f,g),rhs,'(hell : 0 < ell) (hzd : Function.Injective z) (hl : lam = a^2*q/(b*c*ee)) (hbal : a^3*q^(2+∑ i, m i) = b*c*d*ee*f*g)')
