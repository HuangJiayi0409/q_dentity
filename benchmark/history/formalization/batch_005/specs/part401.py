from common import *
S={};q=e('q')
S[401]='''(q : K) (n : ℕ) (j : ℤ) (hq : q ≠ 0) :
 sillsT01 q true n j-q^((n:ℤ)-j)*sillsT01 q false n j-
 sillsT01 q true n (j+1)+q^((n:ℤ)+j+1)*sillsT01 q false n (j+1)=0'''
S[402]=ST('(q : K) (n : ℕ)',e('(sillsP q n)'),ISUM('j','-(n:ℤ)-1','(n:ℤ)+1',lambda j:e('((-1:K)^j*q^(4*j*j+j).toNat*(sillsT01 q false n (4*j)+sillsT01 q false n (4*j+1)))')))
for idx,fn,ex,shift in [(403,'A','j*(9*j+1)/2','0'),(404,'B','j*(9*j-5)/2','-1'),(405,'C','j*(9*j+7)/2','1')]:
 S[idx]=ST('(q : K) (n : ℕ)',e(f'(borwein{fn} q n)'),ISUM('j','-(n:ℤ)-1','(n:ℤ)+1',lambda j:e(f'((-1:K)^j*q^({ex}).toNat)')*GI('2*(n:ℤ)',f'(n:ℤ)+3*j+({shift})')))
S[406]=CL('(q : K) (n : ℕ)',[(e('(borweinA q n)'),SUM('j','n/3',lambda j:P([q**'3'],'n-j-1',q**'3')*(1-q**'(2*n)')*P([q],'3*j')*q**'(3*j*j)'/(P([q],'n-3*j')*P([q**'3'],'2*j',q**'3')*P([q**'3'],'j',q**'3')))),(e('(borweinA q 0)'),1)],'(hn : 1 ≤ n)')
for idx,fn,num in [(407,'B',1-q**'(3*j+2)'-q**'(n+3*j+2)'+q**'(n+1)'),(408,'C',1-q**'(3*j+1)'-q**'(n+3*j+2)'+q**'n')]:
 S[idx]=CL('(q : K) (n : ℕ)',[(e(f'(borwein{fn} q n)'),SUM('j','(n-1)/3',lambda j:P([q**'3'],'n-j-1',q**'3')*num*P([q],'3*j')*q**'(3*j*j+3*j)'/(P([q],'n-3*j-1')*P([q**'3'],'2*j+1',q**'3')*P([q**'3'],'j',q**'3')))),(e(f'(borwein{fn} q 0)'),0)],'(hn : 1 ≤ n)')
S[409]='''(q : K) (n : ℕ) (hn : 1 ≤ n) :
 borweinA q n = (1+q^(2*n-1))*borweinA q (n-1)+q^n*(borweinB q (n-1)+borweinC q (n-1)) ∧
 borweinB q n = (1+q^(2*n-1))*borweinB q (n-1)+q^(n-1)*borweinA q (n-1)-q^n*borweinC q (n-1) ∧
 borweinC q n = (1+q^(2*n-1))*borweinC q (n-1)+q^(n-1)*(borweinA q (n-1)-borweinB q (n-1)) ∧
 borweinA q 0=1 ∧ borweinB q 0=0 ∧ borweinC q 0=0'''
S[410]='''(q : K) (i : ℕ) (hi : 3 ≤ i) :
 motivatedA q (i+1)=motivatedA q i+motivatedB q i ∧
 motivatedB q (i+1)=q^i*motivatedA q i ∧
 motivatedA q 3=1 ∧ motivatedB q 3=0 ∧ motivatedA q 4=1 ∧
 (4 ≤ i → motivatedA q (i+1)=motivatedA q i+q^(i-1)*motivatedA q (i-1))'''
S[411]=ST('(q : K) (n : ℕ)',BA(e(1),q,'n',lambda r:e('(capparelliAlpha q r)')),P([-e(1)],'n',q**'3')/(P([q],'2*n')*P([-e(1)],'n')))
