from common import *
S={};q,r,s,t,g,h,x,w=vs('q r s t gamma sigma x w')
# The same zero factor is cancelled before evaluation at j=n,k=0 or s=q.
u=1-zp(s,'-k')*Q('j-n');v=1-zp(s,'j-n-k')
ratio=E(f'(if (j = n ∧ k = 0) ∨ s = q then (1 : K) else {u}/{v})',(f'¬ ((j = n ∧ k = 0) ∨ s = q) → {v} ≠ 0',))
inner=lambda j:(1-g/h*zp(s,'n+k')*zp(t,'n')*Q('j-n'))*ratio*P([Q('-n')],'j')/P([q],'j')*PI([g/h*zp(s*t,'n+1')*Q('j-n-1')],'k-1',s*t/q)*PI([g/h*zp(s,'n+k')*zp(t,'j+1')],'n-j-1',t)*P([g*r*zp(s,'j')*t/q],'j',r*t/q)*PI([g*zp(r*s*t,'j+1')*Q('-j-2')],'n-j-1',r*s*t/q**'2')*P([h*r*zp(s,'1-j')/q],'j',r*s/q)*PI([h*zp(r,'j+1')*Q('-j')],'n-j-1',r)*e('(A j)')*e('(C j (n+k-j))')*w**'j'*Q('n*(j-n-k)')
mid=lambda k:(1-g/h*zp(s*t,'n+k'))*e('(B (n+k))')*x**'k'*zp(s/q,'k*(k+1)/2')/(P([s],'k',s)*P([g*r*zp(s,'n+k')*t/q],'n',r*t/q)*P([h*r*zp(s,'1-n-k')/q],'n',r*s/q))*SUM('j','n',inner)
rhs=SUM('n','N',lambda n:(1-g*zp(r*s*t/q,'n'))*(1-h*zp(r/q,'n'))*(-x)**'n'*Q('n+n*(n-1)/2')/P([q],'n')*SUM('k','N-n',mid))
lhs=SUM('j','N',lambda j:e('(A j)')*e('(B j)')*(x*w)**'j'/P([q],'j'))
S[209]=statement('(q r s t gamma sigma x w : K) (N : ℕ) (A B : ℕ → K) (C : ℕ → ℕ → K)',lhs,rhs,'(hnz : r*s*t*q*gamma*sigma ≠ 0) (hB : ∀ j, N < j → B j = 0) (hC : ∀ j, C j 0 = 1)').replace(' (hbase : regular q)','')
