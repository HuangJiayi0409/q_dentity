import Benchmark.BatchAuxiliary

namespace FiniteQBenchmark
open scoped BigOperators
variable {K : Type*} [Field K]

/-- At height at most six there cannot be two allowed parts: the smaller is
at least two, so the gap condition would force the larger to be at least eight. -/
theorem gollnitz_small_classification (s : Finset ℕ)
    (hbound : s ⊆ Finset.range 7) (hg : gollnitzAllowed s) :
    s = ∅ ∨ ∃ j ∈ ({2,4,5,6} : Finset ℕ), s = {j} := by
  have heq := Finset.sort_toFinset s (· ≥ ·)
  generalize hl : s.sort (· ≥ ·) = l at heq
  cases l with
  | nil => exact Or.inl (by simpa using heq.symm)
  | cons x xs =>
    cases xs with
    | nil =>
      have hs : s = {x} := by simpa using heq.symm
      have hx : x ∈ s := by simp [hs]
      have hb := Finset.mem_range.mp (hbound hx)
      have hh := hg.1 x hx
      right
      refine ⟨x, ?_, hs⟩
      simp only [Finset.mem_insert, Finset.mem_singleton]
      omega
    | cons y ys =>
      have hx : x ∈ s := by rw [← heq]; simp
      have hy : y ∈ s := by rw [← heq]; simp
      have hb := Finset.mem_range.mp (hbound hx)
      have hh := hg.1 y hy
      have hpair : (x,y) ∈ (s.sort (· ≥ ·)).zip (s.sort (· ≥ ·)).tail := by
        rw [hl]
        simp
      have hgap := (hg.2 (x,y) hpair).1
      omega

theorem gollnitz_sets_0 : ((Finset.range 1).powerset).filter gollnitzAllowed = ({∅} : Finset (Finset ℕ)) := by
  ext s
  simp only [Finset.mem_filter, Finset.mem_powerset]
  constructor
  · rintro ⟨hsub, hg⟩
    have hb : s ⊆ Finset.range 7 := fun x hx =>
      Finset.mem_range.mpr (by have := Finset.mem_range.mp (hsub hx); omega)
    rcases gollnitz_small_classification s hb hg with hs | ⟨j, hj, hs⟩
    · simp [hs]
    · simp only [Finset.mem_insert, Finset.mem_singleton] at hj
      rcases hj with rfl | rfl | rfl | rfl
      all_goals subst s; simp_all
  · intro hs
    simp only [Finset.mem_insert, Finset.mem_singleton] at hs
    rcases hs with rfl
    all_goals norm_num [gollnitzAllowed]

theorem gollnitz_initial_0 (t q : K) : gollnitz t q 0 = 1 := by
  change (∑ s ∈ ((Finset.range 1).powerset).filter gollnitzAllowed,
    t^(∑ j ∈ s, if j%6 = 2 ∨ j%6 = 4 ∨ j%6 = 5 then 1 else 2)*q^(∑ j ∈ s, j)) = _
  rw [gollnitz_sets_0]
  norm_num
  <;> ring

theorem gollnitz_sets_1 : ((Finset.range 2).powerset).filter gollnitzAllowed = ({∅} : Finset (Finset ℕ)) := by
  ext s
  simp only [Finset.mem_filter, Finset.mem_powerset]
  constructor
  · rintro ⟨hsub, hg⟩
    have hb : s ⊆ Finset.range 7 := fun x hx =>
      Finset.mem_range.mpr (by have := Finset.mem_range.mp (hsub hx); omega)
    rcases gollnitz_small_classification s hb hg with hs | ⟨j, hj, hs⟩
    · simp [hs]
    · simp only [Finset.mem_insert, Finset.mem_singleton] at hj
      rcases hj with rfl | rfl | rfl | rfl
      all_goals subst s; simp_all
  · intro hs
    simp only [Finset.mem_insert, Finset.mem_singleton] at hs
    rcases hs with rfl
    all_goals norm_num [gollnitzAllowed]

theorem gollnitz_initial_1 (t q : K) : gollnitz t q 1 = 1 := by
  change (∑ s ∈ ((Finset.range 2).powerset).filter gollnitzAllowed,
    t^(∑ j ∈ s, if j%6 = 2 ∨ j%6 = 4 ∨ j%6 = 5 then 1 else 2)*q^(∑ j ∈ s, j)) = _
  rw [gollnitz_sets_1]
  norm_num
  <;> ring

theorem gollnitz_sets_2 : ((Finset.range 3).powerset).filter gollnitzAllowed = ({∅, {2}} : Finset (Finset ℕ)) := by
  ext s
  simp only [Finset.mem_filter, Finset.mem_powerset]
  constructor
  · rintro ⟨hsub, hg⟩
    have hb : s ⊆ Finset.range 7 := fun x hx =>
      Finset.mem_range.mpr (by have := Finset.mem_range.mp (hsub hx); omega)
    rcases gollnitz_small_classification s hb hg with hs | ⟨j, hj, hs⟩
    · simp [hs]
    · simp only [Finset.mem_insert, Finset.mem_singleton] at hj
      rcases hj with rfl | rfl | rfl | rfl
      all_goals subst s; simp_all
  · intro hs
    simp only [Finset.mem_insert, Finset.mem_singleton] at hs
    rcases hs with rfl | rfl
    all_goals norm_num [gollnitzAllowed]

theorem gollnitz_initial_2 (t q : K) : gollnitz t q 2 = 1 + t*q^2 := by
  change (∑ s ∈ ((Finset.range 3).powerset).filter gollnitzAllowed,
    t^(∑ j ∈ s, if j%6 = 2 ∨ j%6 = 4 ∨ j%6 = 5 then 1 else 2)*q^(∑ j ∈ s, j)) = _
  rw [gollnitz_sets_2]
  norm_num
  <;> ring

theorem gollnitz_sets_3 : ((Finset.range 4).powerset).filter gollnitzAllowed = ({∅, {2}} : Finset (Finset ℕ)) := by
  ext s
  simp only [Finset.mem_filter, Finset.mem_powerset]
  constructor
  · rintro ⟨hsub, hg⟩
    have hb : s ⊆ Finset.range 7 := fun x hx =>
      Finset.mem_range.mpr (by have := Finset.mem_range.mp (hsub hx); omega)
    rcases gollnitz_small_classification s hb hg with hs | ⟨j, hj, hs⟩
    · simp [hs]
    · simp only [Finset.mem_insert, Finset.mem_singleton] at hj
      rcases hj with rfl | rfl | rfl | rfl
      all_goals subst s; simp_all
  · intro hs
    simp only [Finset.mem_insert, Finset.mem_singleton] at hs
    rcases hs with rfl | rfl
    all_goals norm_num [gollnitzAllowed]

theorem gollnitz_initial_3 (t q : K) : gollnitz t q 3 = 1 + t*q^2 := by
  change (∑ s ∈ ((Finset.range 4).powerset).filter gollnitzAllowed,
    t^(∑ j ∈ s, if j%6 = 2 ∨ j%6 = 4 ∨ j%6 = 5 then 1 else 2)*q^(∑ j ∈ s, j)) = _
  rw [gollnitz_sets_3]
  norm_num
  <;> ring

theorem gollnitz_sets_4 : ((Finset.range 5).powerset).filter gollnitzAllowed = ({∅, {2}, {4}} : Finset (Finset ℕ)) := by
  ext s
  simp only [Finset.mem_filter, Finset.mem_powerset]
  constructor
  · rintro ⟨hsub, hg⟩
    have hb : s ⊆ Finset.range 7 := fun x hx =>
      Finset.mem_range.mpr (by have := Finset.mem_range.mp (hsub hx); omega)
    rcases gollnitz_small_classification s hb hg with hs | ⟨j, hj, hs⟩
    · simp [hs]
    · simp only [Finset.mem_insert, Finset.mem_singleton] at hj
      rcases hj with rfl | rfl | rfl | rfl
      all_goals subst s; simp_all
  · intro hs
    simp only [Finset.mem_insert, Finset.mem_singleton] at hs
    rcases hs with rfl | rfl | rfl
    all_goals norm_num [gollnitzAllowed]

theorem gollnitz_initial_4 (t q : K) : gollnitz t q 4 = 1 + t*q^2 + t*q^4 := by
  change (∑ s ∈ ((Finset.range 5).powerset).filter gollnitzAllowed,
    t^(∑ j ∈ s, if j%6 = 2 ∨ j%6 = 4 ∨ j%6 = 5 then 1 else 2)*q^(∑ j ∈ s, j)) = _
  rw [gollnitz_sets_4]
  norm_num
  <;> ring

theorem gollnitz_sets_5 : ((Finset.range 6).powerset).filter gollnitzAllowed = ({∅, {2}, {4}, {5}} : Finset (Finset ℕ)) := by
  ext s
  simp only [Finset.mem_filter, Finset.mem_powerset]
  constructor
  · rintro ⟨hsub, hg⟩
    have hb : s ⊆ Finset.range 7 := fun x hx =>
      Finset.mem_range.mpr (by have := Finset.mem_range.mp (hsub hx); omega)
    rcases gollnitz_small_classification s hb hg with hs | ⟨j, hj, hs⟩
    · simp [hs]
    · simp only [Finset.mem_insert, Finset.mem_singleton] at hj
      rcases hj with rfl | rfl | rfl | rfl
      all_goals subst s; simp_all
  · intro hs
    simp only [Finset.mem_insert, Finset.mem_singleton] at hs
    rcases hs with rfl | rfl | rfl | rfl
    all_goals norm_num [gollnitzAllowed]

theorem gollnitz_initial_5 (t q : K) : gollnitz t q 5 = 1 + t*q^2 + t*q^4 + t*q^5 := by
  change (∑ s ∈ ((Finset.range 6).powerset).filter gollnitzAllowed,
    t^(∑ j ∈ s, if j%6 = 2 ∨ j%6 = 4 ∨ j%6 = 5 then 1 else 2)*q^(∑ j ∈ s, j)) = _
  rw [gollnitz_sets_5]
  norm_num
  <;> ring

theorem gollnitz_sets_6 : ((Finset.range 7).powerset).filter gollnitzAllowed = ({∅, {2}, {4}, {5}, {6}} : Finset (Finset ℕ)) := by
  ext s
  simp only [Finset.mem_filter, Finset.mem_powerset]
  constructor
  · rintro ⟨hsub, hg⟩
    have hb : s ⊆ Finset.range 7 := fun x hx =>
      Finset.mem_range.mpr (by have := Finset.mem_range.mp (hsub hx); omega)
    rcases gollnitz_small_classification s hb hg with hs | ⟨j, hj, hs⟩
    · simp [hs]
    · simp only [Finset.mem_insert, Finset.mem_singleton] at hj
      rcases hj with rfl | rfl | rfl | rfl
      all_goals subst s; simp_all
  · intro hs
    simp only [Finset.mem_insert, Finset.mem_singleton] at hs
    rcases hs with rfl | rfl | rfl | rfl | rfl
    all_goals norm_num [gollnitzAllowed]

theorem gollnitz_initial_6 (t q : K) : gollnitz t q 6 = 1 + t*q^2 + t*q^4 + t*q^5 + t^2*q^6 := by
  change (∑ s ∈ ((Finset.range 7).powerset).filter gollnitzAllowed,
    t^(∑ j ∈ s, if j%6 = 2 ∨ j%6 = 4 ∨ j%6 = 5 then 1 else 2)*q^(∑ j ∈ s, j)) = _
  rw [gollnitz_sets_6]
  norm_num
  <;> ring

end FiniteQBenchmark
#print axioms FiniteQBenchmark.gollnitz_initial_0
#print axioms FiniteQBenchmark.gollnitz_initial_1
#print axioms FiniteQBenchmark.gollnitz_initial_2
#print axioms FiniteQBenchmark.gollnitz_initial_3
#print axioms FiniteQBenchmark.gollnitz_initial_4
#print axioms FiniteQBenchmark.gollnitz_initial_5
#print axioms FiniteQBenchmark.gollnitz_initial_6
