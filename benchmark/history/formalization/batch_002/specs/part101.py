from common import *
a,b,c,d,w,q,lam=vs('a b c d w q lam')
S={}
S[101]=statement('(a b q : K) (n : ℕ)',BI([a*a,a*q*q,-a*q*q,b*b],[a,-a,a*a*q*q/(b*b)],[-a*Q('n')/(b*b),Q('-n')],[b*b*Q('1-n'),-a*Q('n+1')],'n',q),P([-a*q,a/(b*b)],'n')*Q('n')*P([1/(b*b)],'n',q*q)/(P([-q,1/(b*b)],'n')*P([a*a*q*q/(b*b)],'n',q*q)), '(ha : a ≠ 0) (hb : b ≠ 0)')
S[102]=statement('(a b q : K) (n : ℕ)',BI([a*a,a*q*q,-a*q*q,b*b],[a,-a,a*a*q*q/(b*b)],[-a*Q('n-1')/(b*b),Q('-n')],[b*b*Q('2-n'),-a*Q('n+1')],'n',q*q),P([-a*q,a/(q*b*b)],'n')*P([a*q/(b*b),1/(b*b*q*q)],'n',q*q)*Q('n')/(P([-q,1/(q*b*b)],'n')*P([a/(q*b*b),a*a*q*q/(b*b)],'n',q*q)), '(ha : a ≠ 0) (hb : b ≠ 0)')
S[103]=statement('(a b w q : K) (n : ℕ)',PH([a,b,-w/b,Q('-n')],[a*q/b,-b*Q('-n'),w],'n'),P([w/a,-a*q/b],'n')/P([w,-q/b],'n')*PH([a,a*a*q*q/(w*w),a*q/(b*b),Q('-2*n')],[a*a*q*q/(b*b),a*Q('1-n')/w,a*Q('2-n')/w],'n',q*q,q*q),'(ha : a ≠ 0) (hb : b ≠ 0) (hw : w ≠ 0)')
S[104]=statement('(a b c w q : K) (n : ℕ)',BI([a*a,a*q*q,-a*q*q,b*b,c*c],[a,-a,a*a*q*q/(b*b),a*a*q*q/(c*c)],[-a*q/w,Q('-n')],[w,-a*Q('n+1')],'n',a*w*Q('n+1')/(b*b*c*c)),P([-a*q,a*q*q/w,w/(a*q)],'n')/P([-q,a*q/w,w],'n')*PH([a*q,a*q*q,a*a*q*q/(b*b*c*c),a*a*q*q/(w*w),Q('-2*n')],[a*a*q*q/(b*b),a*a*q*q/(c*c),a*Q('2-n')/w,a*Q('3-n')/w],'n',q*q,q*q),'(ha : a ≠ 0) (hb : b ≠ 0) (hc : c ≠ 0) (hw : w ≠ 0)')
for i in [105,106,111,112]:
    even=i in [106,112];ex=i in [111,112]
    xs=[a*a]+([a*q*q]if even else [])+[-a*q*q,b*b,c*c,d*d]
    ys=([a]if even else [])+[-a,a*a*q*q/(b*b),a*a*q*q/(c*c),a*a*q*q/(d*d)]
    shift={105:'n+1',106:'n',111:'n',112:'n-1'}[i]
    low={105:'-n',106:'1-n',111:'1-n',112:'2-n'}[i]
    lhs=BI(xs,ys,[-lam*Q(shift)/a,Q('-n')],[a*a*Q(low)/lam,-a*Q('n+1')],'n',q*q if ex else q)
    if i==105:pref=P([-a*q,lam*q/a],'n')*P([lam*q*q/(a*a)],'n',q*q)/(P([-q,lam*q/(a*a)],'n')*P([lam*q*q],'n',q*q))
    if i==106:pref=P([lam/a,-a*q],'n')*P([lam/(a*a)],'n',q*q)*Q('n')/(P([lam/(a*a),-q],'n')*P([lam*q*q],'n',q*q))
    if i==111:pref=P([-a*q,lam/a],'n')*P([lam/(a*a),lam*q*q/a],'n',q*q)/(P([-q,lam/(a*a)],'n')*P([lam*q*q,lam/a],'n',q*q))
    if i==112:pref=P([-a*q,lam/(a*q)],'n')*P([lam/(a*a*q*q)],'n',q*q)*(1-lam*Q('2*n-1')/a)*Q('n')/(P([-q,lam/(a*a*q)],'n')*P([lam*q*q],'n',q*q)*(1-lam/(a*q)))
    bs=([a*q,a*q*q]if even else[a,a*q])+[lam*b*b/(a*a),lam*c*c/(a*a),lam*d*d/(a*a),lam*lam*Q({105:'2*n+2',106:'2*n',111:'2*n',112:'2*n-2'}[i])/(a*a),Q('-2*n')]
    rhs=pref*W(lam,bs,'n',a*a*Q('3'if ex else'1')/lam,q*q)
    S[i]=statement('(a b c d lam q : K) (n : ℕ)',lhs,rhs,'(hp : ∀ x ∈ [a,b,c,d,lam], x ≠ 0) (hlam : lam = a^4*q^2/(b^2*c^2*d^2))')
S[107]=statement('(a c q : K) (n : ℕ)',PH([a,q/a,Q('-n')],[c,-q],'n'),P([-Q('1-n')/c],'n')/P([-Q('-n')],'n')*PH([c/a,a*c/q,Q('-2*n')],[c*c,e(0)],'n',q*q,q*q),'(ha : a ≠ 0) (hc : c ≠ 0)')
S[108]=statement('(b q : K) (m : ℕ)',SUM('k','2*m+1',lambda k:P([Q('-2*m-1'),b,-b],'k')/P([q,b*b],'k')*Q('(2*m+1)*k-k*(k-1)/2')),0)
S[109]=statement('(a b d q : K) (n : ℕ)',PH([Q('-n'),Q('1-n'),a,a*q],[q*b*b,d,d*q],'n/2',q*q,q*q),P([d/a],'n')/P([d],'n')*(a**'n')*PH([Q('-n'),a,b,-b],[b*b,a*Q('1-n')/d],'n',-q/d),'(ha : a ≠ 0) (hd : d ≠ 0)')
S[110]=statement('(b c d w q : K) (n : ℕ)',BI([Q('-2*n'),-Q('2-n'),b*b,c*c],[-Q('-n'),Q('2-2*n')/(b*b),Q('2-2*n')/(c*c)],[d,-Q('1-n')/w],[-Q('1-n')/d,w],'n',w*Q('2-n')/(b*b*c*c*d)),P([e(-1),w/d],'n')/P([-d,w],'n')*(d**'n')*PH([d*d,Q('2-2*n')/(b*b*c*c),Q('2-2*n')/(w*w),Q('-n'),Q('1-n')],[Q('2-2*n')/(b*b),Q('2-2*n')/(c*c),d*Q('1-n')/w,d*Q('2-n')/w],'n/2',q*q,q*q),'(hp : ∀ x ∈ [b,c,d,w], x ≠ 0)')
