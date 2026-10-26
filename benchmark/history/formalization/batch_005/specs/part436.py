from common import *
S={}
base='(hq : q ≠ 0) (hq2 : q^2 ≠ 1)'
S[436]=f'''(q x : ℂ) (f g : ℂ → ℂ) {base} (hx : x ≠ 0) :
 symJackson q (fun y => f y*g y) x = f (q*x)*symJackson q g x+g (q⁻¹*x)*symJackson q f x ∧
 f (q*x)*symJackson q g x+g (q⁻¹*x)*symJackson q f x =
 f (q⁻¹*x)*symJackson q g x+g (q*x)*symJackson q f x'''
S[437]=f'''(q x : ℂ) (f g : ℂ → ℂ) {base} (hx : x ≠ 0)
 (hg : g (q*x)*g (q⁻¹*x) ≠ 0) :
 symJackson q (fun y => f y/g y) x =
 (g (q⁻¹*x)*symJackson q f x-f (q⁻¹*x)*symJackson q g x)/(g (q*x)*g (q⁻¹*x)) ∧
 (g (q⁻¹*x)*symJackson q f x-f (q⁻¹*x)*symJackson q g x)/(g (q*x)*g (q⁻¹*x)) =
 (g (q*x)*symJackson q f x-f (q*x)*symJackson q g x)/(g (q*x)*g (q⁻¹*x))'''
S[438]=f'''(q x : ℂ) (n : ℕ) {base} :
 symJackson q (fun y => y^n) x = symNumber q n*x^(n-1)'''
S[439]=f'''(q x a : ℂ) (n : ℕ) {base} (hn : 1 ≤ n) :
 symJackson q (fun y => symPower y a q n) x = symNumber q n*symPower x a q (n-1)'''
S[440]=f'''(q x a : K) (n : ℕ) {base}
 (hden : ∀ j ≤ n, symFactorial q j*symFactorial q (n-j) ≠ 0) :
 symPower x (-a) q n = ∑ j ∈ Finset.range (n+1), symGaussian q n j*a^(n-j)*x^j'''
S[441]='''(q x : K) (n : ℕ) (hq : q ≠ 0) (hq1 : q ≠ 1) :
 symPower 1 x q n = (-1)^n*symPower x 1 q n'''
S[442]=f'''(q x : ℂ) (n : ℕ) {base}
 (hshift : symPower 1 (q*x) q n*symPower 1 (q⁻¹*x) q n ≠ 0)
 (hout : symPower 1 x q (n+1) ≠ 0) :
 symJackson q (fun y => 1/symPower 1 y q n) x = symNumber q n/symPower 1 x q (n+1)'''
S[443]='''(q r h h' a : ℂ) (n : ℕ) (T : ℕ → Polynomial ℂ)
 (hq : q ≠ 0) (hq1 : q ≠ 1) (hqr : q ≠ r) (hn : 2 ≤ n)
 (hpow : q^(n-1) ≠ r^(n-1)) (hnum : ∀ j ∈ Finset.Icc 1 n, pairNumber q r j ≠ 0)
 (hT : quantumTaylorFamily q r h h' a T n) :
 quantumRootSum T n = pairNumber q r n/pairNumber q r (n-1)*quantumRootSum T (n-1) +
 ((n:ℂ)*(q^(n-1)*h-r^(n-1)*h')-pairNumber q r n*(h-h'))/(q^(n-1)-r^(n-1))'''
S[444]='''(q h h' a : ℂ) (n : ℕ) (T : ℕ → Polynomial ℂ)
 (hq : q ≠ 0) (hq1 : q ≠ 1) (hh : h ≠ h') (hn : 2 ≤ n)
 (hT : quantumTaylorFamily q q h h' a T n) :
 quantumRootSum T n = (n:ℂ)*q/((n:ℂ)-1)*quantumRootSum T (n-1)+(n:ℂ)*(h+h')/2'''
S[445]='''(q r h a : ℂ) (n : ℕ) (T : ℕ → Polynomial ℂ)
 (hq : q ≠ 0) (hq1 : q ≠ 1) (hqr : q ≠ r) (hn : 1 ≤ n)
 (hnum : ∀ j ∈ Finset.Icc 1 n, pairNumber q r j ≠ 0)
 (hT : quantumTaylorFamily q r h h a T n) :
 quantumRootSum T n = (a-h)*pairNumber q r n +
 h*pairNumber q r n*(∑ j ∈ Finset.Icc 1 n, (j:ℂ)/pairNumber q r j) ∧ quantumRootSum T 1=a'''
S[446]=f'''(q a : ℂ) (n : ℕ) {base}
 (hden : ∀ j ∈ Finset.Icc 1 n, symNumber q j ≠ 0) :
 symTaylor q a 0 = 1 ∧ (1 ≤ n →
 symTaylor q a n = Polynomial.C (1/symFactorial q n)*Polynomial.X^n -
 (∑ k ∈ Finset.range n, Polynomial.C (a^(n-k)/symFactorial q (n-k))*symTaylor q a k) ∧
 (∀ x : ℂ, symJackson q (fun y => (symTaylor q a n).eval y) x = (symTaylor q a (n-1)).eval x) ∧
 (symTaylor q a n).eval a=0)'''
