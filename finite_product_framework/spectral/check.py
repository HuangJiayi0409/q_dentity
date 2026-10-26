import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from spectral.pipeline import SPEC,prepare,prove_source
from workflow.structural_check import run
CTX='{I : Type*} [Fintype I] (w : I → ℚ) (A : I → I → ℚ) (f g : I → ℚ) (l m : ℚ)'
B=' (hb : ∀ i j, w i*A i j = w j*A j i)'
F=' (hf : ∀ i, ∑ j, A i j*f j = l*f i)'
G=' (hg : ∀ i, ∑ j, A i j*g j = m*g i)'
S=' (hs : l ≠ m)'
TARGET='(∑ i, w i*f i*g i) = 0'
CASES=[
 ('generic_context_certificate_not_constructor',CTX+B+F+G+S,TARGET,False),
 ('missing_balance',CTX+F+G+S,TARGET,False),
 ('missing_separation',CTX+B+F+G,TARGET,False),
 ('missing_eigenrelation',CTX+B+F+S,TARGET,False),
 ('explicit_symbolic_matrix','(l m : ℚ) (hs : l ≠ m) (A : Fin 2 → Fin 2 → ℚ) (hA : A = !![(l+m)/2,(l-m)/2;(l-m)/2,(l+m)/2])',
 '(∑ i : Fin 2, (1 : ℚ) * (![1,1] : Fin 2 → ℚ) i * (![1,-1] : Fin 2 → ℚ) i) = 0',True)]
FAMILY='{I J : Type*} [Fintype I] [DecidableEq J] (w : I → ℚ) (A : I → I → ℚ) (P : J → I → ℚ) (eigen norm : J → ℚ) (m n : J) (hb : ∀ i j, w i*A i j = w j*A j i) (he : ∀ t i, ∑ j, A i j*P t j = eigen t*P t i) (hinj : Function.Injective eigen)'
NORM=' (hn : ∀ t, ∑ i, w i*P t i*P t i = norm t)'
GOAL='(∑ i, w i*P m i*P n i) = if m=n then norm n else 0'
CASES.extend([('context_norm_not_constructor',FAMILY+NORM,GOAL,False),('missing_norm',FAMILY,GOAL,False)])
CASES.extend([
 ('operator_not_supplied','(q : ℚ)',
  '(∑ i : Fin 3, (1 : ℚ) * (![q,q,q] : Fin 3 → ℚ) i * (![1,-2,1] : Fin 3 → ℚ) i) = 0',True),
 ('weighted_operator_not_supplied','(q : ℚ)',
  '(∑ i : Fin 3, (![1,2,3] : Fin 3 → ℚ) i * (![q,q,q] : Fin 3 → ℚ) i * (![1,1,-1] : Fin 3 → ℚ) i) = 0',True),
 ('false_pairing','(q : ℚ)',
  '(∑ i : Fin 3, (1 : ℚ) * (![q,q,q] : Fin 3 → ℚ) i * (![1,2,1] : Fin 3 → ℚ) i) = 0',False),
 ('zero_left_allowed','',
  '(∑ i : Fin 3, (1 : ℚ) * (![0,0,0] : Fin 3 → ℚ) i * (![1,2,1] : Fin 3 → ℚ) i) = 0',True)])
CASES.append(('constructed_operator_five','(q : ℚ)',
 '(∑ i : Fin 5, (![1,2,3,4,5] : Fin 5 → ℚ) i * (![q,q,q,q,q] : Fin 5 → ℚ) i * (![1,1,1,1,-2] : Fin 5 → ℚ) i) = 0',True))
if __name__=='__main__':raise SystemExit(run(SPEC,CASES,prepare,prove_source,
    required_constructions={k:'constructed_weighted_separator' for k in
        ('explicit_symbolic_matrix','operator_not_supplied','weighted_operator_not_supplied','zero_left_allowed','constructed_operator_five')}))
