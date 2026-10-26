from common import *
a,b,c,d,e1,f,p,q,A,B,C,mu=vs('a b c d e f p q A B C mu')
S={}
S[113]=statement('(a b c p q A B C mu : K) [CharZero K] (n : ℕ)',SUM('k','n',lambda k:KT(a,b,c,p,q,'k')*RISE([C-A-e('(n:K)'),-B-C-e('(n:K)'),mu*B-mu*A-e('(n:K)'),-e('(n:K)')],'k')/RISE([-mu*C-e('(n:K)'),mu*B+mu*C-mu*A-e('(n:K)'),-A-e('(n:K)'),-B-e('(n:K)')],'k')),TT(a,b,c,p,q,'n')*e('(Nat.factorial n : K)')*RISE([mu*A+1-mu*B,A+1-C,B+C+1],'n')/RISE([A+1,B+1,mu*C+1,mu*A+1-mu*B-mu*C],'n')*SUM('k','n',lambda k:(A+e('(k:K)')+e('(k:K)')/mu)*(B+e('(k:K)')-e('(k:K)')/mu)/(A*B)*RISE([A,B,mu*C,mu*A-mu*B-mu*C],'k')/(e('(Nat.factorial k:K)')*RISE([mu*A+1-mu*B,A+1-C,B+C+1],'k'))*RT(a,b,c,p,q,'n','k')),'(hp : regular p) (hnz : ∀ x ∈ [A,B,mu,a,b,c], x ≠ 0)')
Pbase,Qbase=vs('p2 q2')
S[114]=statement('(a b c p q A B C p2 q2 : K) (n : ℕ)',SUM('k','n',lambda k:KT(a,b,c,p,q,'k')*RT(A,B,C,Pbase,Qbase,'n','k')),TT(a,b,c,p,q,'n')/TT(A,B,C,Pbase,Qbase,'n')*SUM('k','n',lambda k:KT(A,B,C,Pbase,Qbase,'k')*RT(a,b,c,p,q,'n','k')),'(hp : regular p) (hp2 : regular p2) (hq2 : regular q2) (hnz : ∀ x ∈ [a,b,c,A,B,C], x ≠ 0)')
S[115]='''(a b p q : K) (N : ℕ) (f c : ℕ → K)
 (hp : regular p) (hq : regular q) (ha : a ≠ 0) (hb : b ≠ 0)
 (hA : ∀ n ≤ N, ∀ j ≤ n, inverseADefined a b p q n j)
 (hB : ∀ j ≤ N, ∀ m ≤ j, pochList [q,a*q^(1+2*m)/b] q (j-m) ≠ 0) :
 (∀ j ≤ N, f j = ∑ n ∈ Finset.range (j+1), inverseB a b p q j n*c n) ↔
 (∀ n ≤ N, c n = ∑ j ∈ Finset.range (n+1), inverseA a b p q n j*f j)'''
S[116]=statement('(a b c q : K) (n : ℕ)',SUM('k','n',lambda k:(1-a*c*Q('4*k'))/(1-a*c)*P([a,b],'k')*P([c*q/b],'2*k')*P([a*a*b*c*Q('3*n'),Q('-3*n')],'k',q**3)*Q('k')/(P([c*q**3,a*c*q**3/b],'k',q**3)*P([a*b],'2*k')*P([Q('1-3*n')/(a*b),a*c*Q('3*n+1')],'k'))),(1-a*c*q*q)*(1-a*b/(q*q))*(1-a*b*Q('3*n'))*(1-a*c*Q('3*n'))/((1-a*c*Q('3*n+2'))*(1-a*b*Q('3*n-2'))*(1-a*b)*(1-a*c))*SUM('k','n',lambda k:(1-a*c*Q('6*k+2'))/(1-a*c*q*q)*P([a*q*q,b*q*q,c*q*q/b,c*q**3/b,a*a*b*c*Q('3*n'),Q('-3*n')],'k',q**3)*Q('3*k')/P([c*q**3,a*c*q**3/b,a*b*q**3,a*b*q*q,Q('5-3*n')/(a*b),a*c*Q('3*n+5')],'k',q**3)),'(ha : a ≠ 0) (hb : b ≠ 0)')
S[117]=statement('(a b c q : K) (n : ℕ)',SUM('k','n',lambda k:(1-a*Q('4*k'))*(1-b*Q('-2*k'))/((1-a)*(1-b))*P([a,1/(a*b)],'k')*P([a*b*q],'2*k')*P([c,a/(b*c)],'k',q**3)*Q('3*k')/(P([q**3,a*a*b*q**3],'k',q**3)*P([q/b],'2*k')*P([a*q/c,b*c*q],'k'))),P([a*q,b*q],'n')*P([c*q**3,a*q**3/(b*c)],'n',q**3)/(P([a*q/c,b*c*q],'n')*P([q**3,a*q**3/b],'n',q**3))*W(a/b,[1/(a*b*b),c,a/(b*c),a*Q('n+1'),a*Q('n+2'),a*Q('n+3'),Q('-3*n')],'n',q**3,q**3),'(hnz : ∀ x ∈ [a,b,c], x ≠ 0)')
S[118]=statement('(a c q : K) (n : ℕ)',PH([Q('-2*n'),c*c,a,q*a],[q*q*a*a,c*Q('-n'),c*Q('1-n')],'n',q*q,q*q),P([-q,q*a/c],'n')/P([-a*q,q/c],'n'),'(hc : c ≠ 0)')
S[119]=statement('(a c d e f q : K) (n : ℕ)',SUM('k','(n:ℤ)',lambda k:(1-a*Q('2*k'))/(1-a)*PI([c,d,e1,f,a*Q('-n'),Q('-n')],'k')/PI([a*q/c,a*q/d,a*q/e1,a*q/f,Q('n+1'),a*Q('n+1')],'k')*zp(a*a*Q('2*n+2')/(c*d*e1*f),'k'),lo='-(n:ℤ)'),P([a*q,q/a,a*q/(c*d),a*q/(e1*f)],'n')/P([q/c,q/d,a*q/e1,a*q/f],'n')*SUM('k','(n:ℤ)',lambda k:PI([e1,f,a*Q('n+1')/(c*d),Q('-n')],'k')/PI([a*q/c,a*q/d,Q('n+1'),e1*f/(a*Q('n'))],'k')*Q('k'),lo='-(n:ℤ)'),'(hnz : ∀ x ∈ [a,c,d,e,f], x ≠ 0)')
for i in [120,121]:
 shift=1 if i==120 else 2
 S[i]=statement('(b c d e q : K) (n : ℕ)',SUM('k','(n:ℤ)',lambda k:PI([b,c,d,e1,Q('-n')],'k')/PI([q**shift/b,q**shift/c,q**shift/d,q**shift/e1,Q('n+'+str(shift))],'k')*Q('k'),lo='-(n:ℤ)'if i==120 else'-(n:ℤ)-1'),(1 if i==120 else 1-q)*P([q**shift,q**shift/(b*c),q**shift/(b*d),q**shift/(c*d)],'n')/P([q**shift/b,q**shift/c,q**shift/d,q**shift/(b*c*d)],'n'),f'(hnz : ∀ x ∈ [b,c,d,e], x ≠ 0) (hbal : b*c*d*e = q^(n+{1 if i==120 else 3}))')
for i in [122,123]:
 odd=i==123
 S[i]=statement('(q : K) (n : ℕ)',SUM('k','(n:ℤ)',lambda k:zp(e('(-1:K)'),'k')*e(f'(gaussianInt q ({Z("2*n+1"if odd else"2*n")}) ({Z("n+k+1"if odd else"n+k")}))')**3*Q('k*(3*k+1)/2'),lo='-(n:ℤ)-1'if odd else'-(n:ℤ)'),P([q],'3*n+1'if odd else'3*n')/(P([q],'n')**3))
S[124]=statement('(a b c d q : K) (m : ℕ)',W(a*a*b*c,[a*b*c*d,a*b,a*c,a*a*Q('m+1'),Q('-m')],'m',q/(a*d)),P([a*a*b*c*q,q,a*q/b,a*q/c],'m')/P([q*a*a,a*b*q,a*c*q,q/(b*c)],'m')*SUM('k','m',lambda k:(1-a*a*Q('2*k'))*P([a*a,a*b,a*c,a*d],'k')/((1-a*a)*P([q,a*q/b,a*q/c,a*q/d],'k'))*zp(q/(a*b*c*d),'k')),'(hnz : ∀ x ∈ [a,b,c,d], x ≠ 0)')
S[125]=statement('(q : K) (j k : ℕ)',e('((pochList [laurentMono 1 q,laurentMono (-1) 1] (laurentMono 0 q) j * pochList [laurentMono 2 q,laurentMono (-2) q] (laurentMono 0 (q^2)) k).coeff 0)'),P([q],'2*j')*P([q*q],'2*k',q*q)*P([Q('2*j+1')],'k',q*q)/(P([q],'j')*P([q*q],'k',q*q)*P([q],'j+2*k')))
