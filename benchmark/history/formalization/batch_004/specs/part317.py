from common import *
S={};a,q=vs('a q')
def B(i):return e(f'(b ({i}))')
def C(i):return e(f'(c ({i}))')
def PROD(v,typ,term):
 return E(f'(∏ {v} : {typ}, {term})',()if not term.req else(f'∀ {v} : {typ}, ({conj(term.req)})',))
def coords(j):return e(f'((ns {j}).val)')
def NP(xs,j):return P(xs,f'(ns {j}).val')
beta=lambda N:E(f'(baileySum a q alpha ({N}))',(f'baileyDefined a q ({N})',))
# k+1 is the positive number of parameter pairs; i=0 corresponds to source i=1.
L=SUM('r','N',lambda r:P([Q('-N')],'r')/P([a*Q('N+1')],'r')*PROD('i','Fin (k+1)',P([B('i.val'),C('i.val')],'r')/P([a*q/B('i.val'),a*q/C('i.val')],'r'))*(a**'(k+1)'*Q('k+1+N')/e('(∏ i : Fin (k+1), b i.val*c i.val)'))**'r'*e('(-1:K)')**'r'*Q('-r*(r-1)/2')*e('(alpha r)'))
term=NP([Q('-N')],'(Fin.last k)')*beta('(ns 0).val')/NP([B('k')*C('k')*Q('-N')/a],'(Fin.last k)')*PROD('i','Fin (k+1)',NP([B('i.val'),C('i.val')],'i'))*PROD('i','Fin k',P([a*q/(B('i.val')*C('i.val'))],'(ns i.succ).val-(ns i.castSucc).val')*(a*q/(B('i.val')*C('i.val')))**'((ns i.castSucc).val)'/(P([q],'(ns i.succ).val-(ns i.castSucc).val')*NP([a*q/B('i.val'),a*q/C('i.val')],'i.succ')))*e('(q^((ns (Fin.last k)).val))')
scope='((Finset.univ : Finset (Fin (k+1) → Fin (N+1))).filter Monotone)'
rhs=P([a*q,a*q/(B('k')*C('k'))],'N')/P([a*q/B('k'),a*q/C('k')],'N')*E(f'(∑ ns ∈ {scope}, {term})',(f'∀ ns ∈ {scope}, ({conj(term.req)})',))
S[317]=ST('(a q : K) (k N : ℕ) (b c alpha : ℕ → K)',L,rhs,'(ha : a ≠ 0) (hq : q ≠ 0) (hbc : ∀ i ≤ k, b i*c i ≠ 0)')
# k+2 parameter pairs; v0 = m1+R and vi=mi+1 (i>0).
# Each v lies in [0,N+R] and total(v) ≤ N+R, exactly the source simplex.
def pref(i):return e(f'((∑ h ∈ Finset.univ.filter (fun h : Fin (k+1) => h ≤ {i}), ((v h).val : ℤ))-(R:ℤ))')
def total():return e('((∑ h : Fin (k+1), ((v h).val : ℤ))-(R:ℤ))')
def IP(xs,idx):
 xs=list(map(e,xs));return E(f'(pochListInt {args(xs)} q ({idx}))',uniq(combine(xs)+(f'pochListIntDefined {args(xs)} q ({idx})',)))
L=ISUM('r','-(R:ℤ)','N',lambda r:(1-a*e('(q^(2*r))'))/(1-a)*IP([a*Q('-R'),Q('-N')],r)/IP([Q('R+1'),a*Q('N+1')],r)*PROD('i','Fin (k+2)',IP([B('i.val'),C('i.val')],r)/IP([a*q/B('i.val'),a*q/C('i.val')],r))*(a**'(k+2)'*Q('k+2+N+R')/e('(∏ i : Fin (k+2), b i.val*c i.val)'))**'r')
term=IP([a*Q('R+1')/(B('0')*C('0'))],e('((v 0).val : ℤ)-(R:ℤ)'))/IP([Q('R+1')],e('((v 0).val : ℤ)-(R:ℤ)'))*PROD('i','Fin k',P([a*q/(B('i.val+1')*C('i.val+1'))],'(v i.succ).val')/P([q],'(v i.succ).val'))*PROD('i','Fin (k+1)',IP([B('i.val+1'),C('i.val+1')],pref('i'))/IP([a*q/B('i.val'),a*q/C('i.val')],pref('i')))*IP([Q('-N')],total())/IP([B('k+1')*C('k+1')*Q('-N')/a],total())*e(f'(a^(∑ i : Fin k, {pref("i.castSucc")}))')*e(f'(q^(∑ i : Fin (k+1), {pref("i")}))')/PROD('i','Fin k',E(f'((b (i.val+1)*c (i.val+1))^{pref("i.castSucc")})'))
scope='(subCompositions (k+1) (N+R))'
rr=E(f'(∑ v ∈ {scope}, {term})',(f'∀ v ∈ {scope}, ({conj(term.req)})',))
rr=P([q/a,a*q/(B('0')*C('0'))],'R')*P([a*q,a*q/(B('k+1')*C('k+1'))],'N')/(P([q/B('0'),q/C('0')],'R')*P([a*q/B('k+1'),a*q/C('k+1')],'N'))*rr
S[327]=ST('(a q : K) (k N R : ℕ) (b c : ℕ → K)',L,rr,'(ha : a ≠ 0) (ha1 : a ≠ 1) (hq : q ≠ 0) (hbc : ∀ i ≤ k+1, b i*c i ≠ 0)')
