from common import *
S={};q,a,b,c,x,t=vs('q a b c x t')
def G(n,k,base=q):return e(f'(gaussian {base} ({n}) ({k}))')
def GI(n,k):return e(f'(gaussianInt q ({n}) ({k}))')
def raw(i,params,l,r,h=''):S[i]=statement(params,l,r,h).replace(' (hbase : regular q)','')
def SD(n):return e(f'(schurDInt q ({n}))')
raw(270,'(q : K) (N M : ℕ)',e('(rectangleWeight q M N)')-e('(rectangleWeight q (M-1) N)'),q**'M'*e('(rectangleWeight q M (N-1))'),'(hN : 1 ≤ N) (hM : 1 ≤ M)')
S[271]='(q : K) (n : ℕ) : gaussian q n 0 = 1 ∧ gaussian q n n = 1'
raw(272,'(q : K) (m n : ℕ)',G('n+m+1','m+1'),SUM('j','n',lambda j:q**'j'*G('m+j','m')))
raw(273,'(q : K) (m n M N : ℕ)',SUM('r','min (M-m) N',lambda r:G('M-m','r')*G('N+m','m+r')*G('m+n+r','M+N')*q**'((N-r)*(M-r-m))'),G('m+n','M')*G('n','N'),'(hM : m ≤ M)')
raw(274,'(a b c q : K) (N : ℕ)',SUM('j','N',lambda j:P([a,b],'j')*P([c/(a*b)],'N-j')/(P([q,c],'j')*P([q],'N-j'))*(a*b/c)**'(N-j)'),P([c/a,c/b],'N')/P([q,c],'N')*(a*b/c)**'N','(hnz : a*b*c ≠ 0)')
for i,stat in [(275,'wordInversions'),(276,'wordIndex')]:
 raw(i,'(q : K) (r : ℕ) (m : Fin r → ℕ)',SUM('s','pairMultiplicity m',lambda s:e(f'((wordStatisticCount m {stat} s : ℕ) : K)')*q**'s'),P([q],'∑ i, m i')/e('(∏ i, poch q q (m i))'),'(hr : 0 < r)')
raw(277,'(q x : K) (n : ℕ)',e('(∑ j ∈ Finset.Icc (-(n:ℤ)) (n:ℤ), q^(j*j).toNat*x^j*gaussianInt (q^2) (2*(n:ℤ)) ((n:ℤ)+j))'),P([-1/x*q,-x*q],'n',q**'2'),'(hx : x ≠ 0)')
raw(278,'(q t : K) (m n : ℕ)',e('(rogersSzego t q m)')*e('(rogersSzego t q n)'),SUM('r','min m n',lambda r:G('m','r')*G('n','r')*P([q],'r')*t**'r'*e('(rogersSzego t q (m+n-2*r))')))
raw(279,'(q : K) (n : ℕ)',e('(schurDInt q (2*(n:ℤ)))'),SUM('j','n',lambda j:q**'(j*n)'*G('n+1','j')*SD('(n:ℤ)-1-j')))
raw(280,'(q : K) (n : ℕ)',e('(schurDInt q n)'),1+SUM('j','n',lambda j:q**'j'*SD('(j:ℤ)-2'),lo='1'))
raw(281,'(q : K) (n : ℕ)',e('(apGollnitz q (6*n-1))'),SUM('j','n/2',lambda j:q**'(6*n*j-3*j*j+2*j)'*G('n-j','j',q**'6')*e('(apLambda q (n-2*j))')),'(hn : 1 ≤ n)')
raw(282,'(q : K) (n : ℕ)',e('(∑ h ∈ Finset.Icc (-(n:ℤ)-2) ((n:ℤ)+2), (-1:K)^h*q^((h*(3*h+1)/2).toNat)*gaussianInt q ((n:ℤ)+1) (((n:ℤ)+1-3*h)/2))'),1)
S[283]='''(q : K) (k r : ℕ) (n : Fin k → ℕ)
 (hk : 0 < k) (hr : 0 < r) (hn : Antitone n) :
 planePi q (r+1) n = q^(∑ j, n j) *
   ∑ m ∈ (Finset.univ : Finset ((j : Fin k) → Fin (n j+1))).filter
     (fun m => Antitone (fun j => (m j).val)), planePi q r (fun j => (m j).val)'''
S[284]='''(q : K) (k r : ℕ) (n : Fin k → ℕ)
 (hk : 0 < k) (hr : 0 < r) (hn : Antitone n) :
 planePi q r n = q^(∑ j, n j) * Matrix.det (fun i j : Fin k =>
   q^((((i.val:ℤ)-j.val)*((i.val:ℤ)-j.val-1)/2).toNat) *
   gaussianInt q ((n j:ℤ)+r-1) ((r:ℤ)-i.val+j.val-1))'''
S[285]='''(q : K) (k r n : ℕ) (hk : 0 < k) (hr : 0 < r) :
 planeBoxPi q k r n = Matrix.det (fun i j : Fin k =>
   q^((((i.val:ℤ)-j.val)*((i.val:ℤ)-j.val-1)/2).toNat) *
   gaussianInt q ((n:ℤ)+r) ((r:ℤ)-i.val+j.val))'''
S[286]='''(q : K) (k r n : ℕ) (hk : 0 < k) (hr : 0 < r)
 (hden : ∀ j ∈ Finset.range k, poch q q (r+j)*poch q q (n+j) ≠ 0) :
 planeBoxPi q k r n = ∏ j ∈ Finset.range k,
   (poch q q j * poch q q (n+r+j)) / (poch q q (r+j)*poch q q (n+j))'''
S[287]='''(X Y Z q : K) (n : ℕ) :
 (∏ i ∈ Finset.range n, (X-Z*q^i)) =
 ∑ k ∈ Finset.range (n+1), gaussian q n k *
   (∏ j ∈ Finset.range k, (Y-Z*q^j)) *
   (∏ h ∈ Finset.range (n-k), (X-Y*q^h))'''
S[288]='''(q : K) (n : ℕ) (L : Polynomial K →ₗ[K] K)
 (hL : ∀ j : ℕ, L (∏ i ∈ Finset.range j, (Polynomial.X-Polynomial.C (q^i))) = 1) :
 L (Polynomial.X^n) = ∑ k ∈ Finset.range (n+1), gaussian q n k'''
S[289]='''(q : K) (r : ℕ) (m : Fin r → ℕ) (hr : 0 < r)
 (hden : (∏ i, poch q q (m i)) ≠ 0) :
 poch q q (∑ i, m i)/(∏ i, poch q q (m i)) =
 ∏ j ∈ (Finset.univ : Finset (Fin r)).filter (fun j => 1 ≤ j.val),
 gaussian q (∑ i ∈ Finset.univ.filter (· ≤ j), m i)
   (∑ i ∈ Finset.univ.filter (· < j), m i)'''
def OP(pos,a,b,mu):return e(f'(oscillationPoly q {str(pos).lower()} k i ({a}) ({b}) ({mu}))')
for num,pos,cond,yes,no in [(290,False,'(a:ℤ)-b > -((i:ℤ)-1)',OP(False,'a-1','b-1','mu'),OP(True,'a-1','b-1','mu-1')),(291,True,'(a:ℤ)-b > 2*(k:ℤ)-i-1',OP(False,'a-1','b-1','mu-1'),OP(True,'a-1','b-1','mu'))]:
 raw(num,'(q : K) (k i a b mu : ℕ)',OP(pos,'a','b','mu')-OP(pos,'a-1','b','mu')-OP(pos,'a','b-1','mu')+OP(pos,'a-1','b-1','mu'),q**'(a+b-1)'*e(f'(if {cond} then {yes} else {no})'),'(hi : 1 ≤ i) (hki : i ≤ k) (ha : 1 ≤ a) (hb : 1 ≤ b) (hmu : 1 ≤ mu)')
S[292]=f'''(q : K) (k i a b : ℕ) (hi : 1 ≤ i) (hki : i ≤ k) :
 {OP(True,'a','b','0')} = {OP(False,'a','b','0')} ∧
 {OP(False,'a','b','0')} = gaussian q (a+b) a'''
S[293]=f'''(q : K) (k i a b mu : ℕ) (hi : 1 ≤ i) (hki : i ≤ k) (hm : 1 ≤ mu) :
 {OP(True,'0','b','mu')} = 0 ∧ {OP(True,'a','0','mu')} = 0 ∧
 {OP(False,'0','b','mu')} = 0 ∧ {OP(False,'a','0','mu')} = 0'''
raw(294,'(q : K) (A B X L : ℤ)',e('(q^L)')*(GI('A+B','B-X')-GI('A+B-1','B-X')-GI('A+B-1','B-X-1')+GI('A+B-2','B-X-1')),e('(q^(L+A+B-1))')*GI('A+B-2','B-X-1'),'(hq : q ≠ 0) (hAB : 2 ≤ A+B)')
raw(295,'(q : K) (A r X Y L : ℤ)',e('(sieveSmallF q A r X Y L)')-e('(sieveSmallF q A (r-1) X Y L)')-e('(sieveSmallF q (A-1) (r+1) X Y L)')+e('(sieveSmallF q (A-1) r X Y L)'),e('(q^(L+2*A+2*Y+r))')*GI('2*A+X+r-2','A+Y'),'(hq : q ≠ 0) (hr : 1 ≤ r) (hAX : 2 ≤ 2*A+X)')
# Integer r admits -1 in 296/297. Bounds ensure dimensions converted to Nat are nonnegative.
for num,par,pos,dim1,dim2,threshold,T,D,R,Eexp in [
 (296,'a',False,'a-1','((a:ℤ)+i-1+r).toNat','2*mu','2*(a:ℤ)+i-3','(a:ℤ)+i-1-(2*k+1)*mu','r+1','(mu:ℤ)*((4*k+2)*mu+2*k-2*i+1)'),
 (297,'a',False,'a-1','((a:ℤ)+i-1+r).toNat','2*mu-1','2*(a:ℤ)+i-3','(a:ℤ)-(2*k+1)*mu+2*k','r+1','(2*(mu:ℤ)-1)*((2*k+1)*mu-2*k+i-1)'),
 (298,'b',True,'((b:ℤ)+2*k-i-1+r).toNat','b-1','2*mu','2*(b:ℤ)+2*k-i-2','(b:ℤ)+2*k-i-(2*k+1)*mu','r','(mu:ℤ)*((4*k+2)*mu-2*k+2*i-1)'),
 (299,'b',True,'((b:ℤ)+2*k-i-1+r).toNat','b-1','2*mu-1','2*(b:ℤ)+2*k-i-2','(b:ℤ)+2*k-(2*k+1)*mu','r','(2*(mu:ℤ)-1)*((2*k+1)*mu-i)')]:
 raw(num,f'(q : K) (k i {par} mu : ℕ) (r : ℤ)',OP(pos,dim1,dim2,threshold),e(f'(sieveF q ({T}) ({D}) ({R}) ({Eexp}))'),f'(hq : q ≠ 0) (hi : 1 ≤ i) (hki : i ≤ k) (hp : 1 ≤ {par}) (hm : 1 ≤ mu) (hr : {"-1" if num<298 else "0"} ≤ r)')
S[300]='''(q : K) (k : ℕ) (n : Fin k → ℕ) (hk : 0 < k) (hn : Antitone n) :
 planePi q 1 n = q^(∑ j, n j)'''
