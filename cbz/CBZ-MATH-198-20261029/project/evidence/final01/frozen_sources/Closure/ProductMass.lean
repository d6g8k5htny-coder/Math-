import SpecificationProofs.P15Elementary

namespace UniversalLaw.P15Closure
open UniversalLaw.Spec.P15
open scoped BigOperators
attribute [local instance] Classical.propDecidable

variable {X : Type} [DecidableEq X]

noncomputable def blockWeight (p : X → ℝ) (B U : Finset X) : ℝ :=
  (∏ v ∈ U, p v) * ∏ v ∈ B \ U, (1 - p v)

theorem blockWeight_nonneg (p : X → ℝ) (B U : Finset X) (hU : U ⊆ B)
    (hp : ∀ v ∈ B, 0 ≤ p v ∧ p v ≤ 1) : 0 ≤ blockWeight p B U := by
  apply mul_nonneg
  · exact Finset.prod_nonneg (fun v hv => (hp v (hU hv)).1)
  · exact Finset.prod_nonneg (fun v hv => sub_nonneg.mpr (hp v (Finset.mem_sdiff.mp hv).1).2)

theorem sum_blockWeight (p : X → ℝ) (B : Finset X) :
    ∑ U ∈ B.powerset, blockWeight p B U = 1 := by
  have h := Finset.prod_add p (fun v => 1 - p v) B
  simpa [blockWeight] using h.symm

theorem cylinder_mass (p : X → ℝ) (B S : Finset X) (hS : S ⊆ B) :
    ∑ U ∈ B.powerset.filter (S ⊆ ·), blockWeight p B U = ∏ v ∈ S, p v := by
  classical
  have h := Finset.prod_add p (fun v => if v ∈ S then 0 else 1 - p v) B
  have hl : (∏ v ∈ B, (p v + if v ∈ S then 0 else 1 - p v)) = ∏ v ∈ S, p v := by
    calc
      _ = ∏ v ∈ B, (if v ∈ S then p v else 1) := by
        apply Finset.prod_congr rfl
        intro v hv
        split_ifs <;> ring
      _ = ∏ v ∈ S, (if v ∈ S then p v else 1) :=
        (Finset.prod_subset hS (by intro v hv hvs; simp [hvs])).symm
      _ = _ := by apply Finset.prod_congr rfl; intro v hv; simp [hv]
  rw [hl] at h
  rw [Finset.sum_filter]
  rw [h]
  apply Finset.sum_congr rfl
  intro U hU
  by_cases hs : S ⊆ U
  · simp only [hs, ite_true]
    unfold blockWeight
    congr 1
    apply Finset.prod_congr rfl
    intro v hv
    have hvS : v ∉ S := fun hvS => (Finset.mem_sdiff.mp hv).2 (hs hvS)
    simp [hvS]
  · simp only [hs, ite_false]
    obtain ⟨v, hvS, hvU⟩ := Finset.not_subset.mp hs
    have hv : v ∈ B \ U := Finset.mem_sdiff.mpr ⟨hS hvS, hvU⟩
    rw [Finset.prod_eq_zero hv]
    · simp
    · simp [hvS]

variable [Fintype X]

theorem localGood_nonneg (F : RealizedData X) (p : X → ℝ) (i : Fin F.b)
    (hp : ∀ v ∈ block F i, 0 ≤ p v ∧ p v ≤ 1) : 0 ≤ localGood F p i := by
  classical
  apply Finset.sum_nonneg
  intro U hU
  by_cases hgood : U ∈ downset F
  · rw [Set.indicator_of_mem hgood]
    exact blockWeight_nonneg p _ U (Finset.mem_powerset.mp hU) hp
  · simp only [Set.indicator_of_notMem hgood]
    exact le_rfl

theorem localGood_le_one (F : RealizedData X) (p : X → ℝ) (i : Fin F.b)
    (hp : ∀ v ∈ block F i, 0 ≤ p v ∧ p v ≤ 1) : localGood F p i ≤ 1 := by
  classical
  rw [← sum_blockWeight p (block F i)]
  apply Finset.sum_le_sum
  intro U hU
  by_cases hgood : U ∈ downset F
  · rw [Set.indicator_of_mem hgood]
    exact le_rfl
  · rw [Set.indicator_of_notMem hgood]
    exact blockWeight_nonneg p _ U (Finset.mem_powerset.mp hU) hp

theorem localFailure_nonneg (F : RealizedData X) (p : X → ℝ) (i : Fin F.b)
    (hp : ∀ v ∈ block F i, 0 ≤ p v ∧ p v ≤ 1) : 0 ≤ localFailure F p i := by
  exact sub_nonneg.mpr (localGood_le_one F p i hp)

theorem localFailure_le_one (F : RealizedData X) (p : X → ℝ) (i : Fin F.b)
    (hp : ∀ v ∈ block F i, 0 ≤ p v ∧ p v ≤ 1) : localFailure F p i ≤ 1 := by
  have := localGood_nonneg F p i hp
  unfold localFailure
  linarith

theorem localFailure_eq_sum (F : RealizedData X) (p : X → ℝ) (i : Fin F.b) :
    localFailure F p i = ∑ U ∈ (block F i).powerset,
      if U ∈ downset F then 0 else blockWeight p (block F i) U := by
  classical
  change 1 - localGood F p i = _
  calc
    _ = (∑ U ∈ (block F i).powerset, blockWeight p (block F i) U) - localGood F p i :=
      congrArg (· - localGood F p i) (sum_blockWeight p (block F i)).symm
    _ = _ := ?_
  unfold localGood
  rw [← Finset.sum_sub_distrib]
  apply Finset.sum_congr rfl
  intro U hU
  by_cases hgood : U ∈ downset F <;> simp [hgood, blockWeight]

theorem selected_product_le_localFailure (F : RealizedData X) (p : X → ℝ)
    (i : Fin F.b) (S : Finset X) (hS : S ⊆ block F i) (hcard : F.a i < S.card)
    (hp : ∀ v ∈ block F i, 0 ≤ p v ∧ p v ≤ 1) :
    (∏ v ∈ S, p v) ≤ localFailure F p i := by
  classical
  rw [← cylinder_mass p (block F i) S hS, localFailure_eq_sum, Finset.sum_filter]
  apply Finset.sum_le_sum
  intro U hU
  by_cases hs : S ⊆ U
  · have hbad : U ∉ downset F := by
      intro hgood
      have hcap := hgood.1 i
      have hUB := Finset.mem_powerset.mp hU
      rw [Finset.inter_eq_left.mpr hUB] at hcap
      have hle := Finset.card_le_card hs
      omega
    simp [hs, hbad]
  · simp only [hs, ite_false]
    split_ifs
    · exact le_rfl
    · exact blockWeight_nonneg p _ U (Finset.mem_powerset.mp hU) hp

/-- Every subset of a good set is good. -/
theorem isGood_subset_mass (F : RealizedData X) {U V : Finset X}
    (hU : IsGood F U) (hVU : V ⊆ U) : IsGood F V := by
  constructor
  · intro i
    exact (Finset.card_le_card (Finset.inter_subset_inter_right hVU)).trans (hU.1 i)
  · intro e he hEV
    exact hU.2 e he (hEV.trans (Finset.image_subset_image hVU))

/-- Block restriction gives a bijection with independently chosen subsets of the blocks. -/
noncomputable def blockSubsetEquiv (F : RealizedData X) :
    Finset X ≃ (∀ i : Fin F.b, {S : Finset X // S ⊆ block F i}) where
  toFun U i := ⟨U ∩ block F i, Finset.inter_subset_right⟩
  invFun parts := Finset.univ.filter (fun v => v ∈ (parts (F.blk v)).val)
  left_inv U := by
    ext v
    simp [block]
  right_inv parts := by
    funext i
    apply Subtype.ext
    ext v
    simp only [Finset.mem_inter, Finset.mem_filter, Finset.mem_univ, true_and]
    constructor
    · rintro ⟨hv, hvi⟩
      have heq : F.blk v = i := (Finset.mem_filter.mp hvi).2
      cases heq
      exact hv
    · intro hv
      have hvi := (parts i).property hv
      have heq : F.blk v = i := (Finset.mem_filter.mp hvi).2
      cases heq
      exact ⟨hv, hvi⟩

theorem sum_block_functions (F : RealizedData X) (f : Fin F.b → Finset X → ℝ) :
    (∑ U : Finset X, ∏ i, f i (U ∩ block F i)) =
      ∏ i, ∑ S ∈ (block F i).powerset, f i S := by
  classical
  calc
    _ = ∑ parts : (∀ i : Fin F.b, {S : Finset X // S ⊆ block F i}),
        ∏ i, f i (parts i).val :=
      (blockSubsetEquiv F).sum_comp (fun parts => ∏ i, f i (parts i).val)
    _ = ∏ i, ∑ S : {S : Finset X // S ⊆ block F i}, f i S.val :=
      (Fintype.prod_sum (fun (i : Fin F.b) (S : {S : Finset X // S ⊆ block F i}) => f i S.val)).symm
    _ = _ := by
      apply Finset.prod_congr rfl
      intro i hi
      apply Finset.sum_bij (fun S _ => S.val)
      · intro S hS
        exact Finset.mem_powerset.mpr S.property
      · intro S hS T hT hST
        exact Subtype.ext hST
      · intro S hS
        exact ⟨⟨S, Finset.mem_powerset.mp hS⟩, Finset.mem_univ _, rfl⟩
      · intro S hS
        rfl

theorem weight_eq_prod_blockWeight (F : RealizedData X) (p : X → ℝ) (U : Finset X) :
    weight p U = ∏ i, blockWeight p (block F i) (U ∩ block F i) := by
  classical
  have h1 : (∏ i, ∏ v ∈ U ∩ block F i, p v) = ∏ v ∈ U, p v := by
    convert Finset.prod_fiberwise U F.blk p using 1
    apply Finset.prod_congr rfl
    intro i hi
    congr 1
    ext v
    simp [block]
  have h2 : (∏ i, ∏ v ∈ block F i \ (U ∩ block F i), (1 - p v)) =
      ∏ v ∈ Finset.univ \ U, (1 - p v) := by
    convert Finset.prod_fiberwise (Finset.univ \ U) F.blk (fun v => 1 - p v) using 1
    apply Finset.prod_congr rfl
    intro i hi
    congr 1
    ext v
    simp [block]
    tauto
  simp_rw [blockWeight]
  rw [Finset.prod_mul_distrib, h1, h2]
  rfl

theorem weight_nonneg_mass (p : X → ℝ) (hp : ∀ v, 0 ≤ p v ∧ p v ≤ 1)
    (U : Finset X) : 0 ≤ weight p U :=
  blockWeight_nonneg p Finset.univ U (Finset.subset_univ U) (fun v _ => hp v)

theorem muOf_nonneg (A : Finset (Finset X)) (p : X → ℝ)
    (hp : ∀ v, 0 ≤ p v ∧ p v ≤ 1) : 0 ≤ muOf A p := by
  exact Finset.sum_nonneg (fun U _ => weight_nonneg_mass p hp U)

theorem muOf_le_one (A : Finset (Finset X)) (p : X → ℝ)
    (hp : ∀ v, 0 ≤ p v ∧ p v ≤ 1) : muOf A p ≤ 1 := by
  unfold muOf
  rw [← UniversalLaw.Proofs.P15Elementary.Aux.sum_weight_eq_one p]
  apply Finset.sum_le_sum_of_subset_of_nonneg
  · intro U hU
    exact Finset.mem_powerset.mpr (Finset.subset_univ U)
  · intro U hU hUA
    exact weight_nonneg_mass p hp U

theorem mu_nonneg (F : RealizedData X) (p : X → ℝ)
    (hp : ∀ v, 0 ≤ p v ∧ p v ≤ 1) : 0 ≤ mu F p := by
  classical
  apply Finset.sum_nonneg
  intro U hU
  by_cases hgood : U ∈ downset F
  · rw [Set.indicator_of_mem hgood]
    exact weight_nonneg_mass p hp U
  · simp [hgood]

theorem mu_le_one (F : RealizedData X) (p : X → ℝ)
    (hp : ∀ v, 0 ≤ p v ∧ p v ≤ 1) : mu F p ≤ 1 := by
  classical
  unfold mu
  rw [← UniversalLaw.Proofs.P15Elementary.Aux.sum_weight_eq_one p]
  apply Finset.sum_le_sum
  intro U hU
  by_cases hgood : U ∈ downset F
  · rw [Set.indicator_of_mem hgood]
  · rw [Set.indicator_of_notMem hgood]
    exact weight_nonneg_mass p hp U

theorem mu_le_prod_localGood (F : RealizedData X) (p : X → ℝ)
    (hp : ∀ v, 0 ≤ p v ∧ p v ≤ 1) : mu F p ≤ ∏ i, localGood F p i := by
  classical
  let f : Fin F.b → Finset X → ℝ := fun i S =>
    Set.indicator (downset F) (blockWeight p (block F i)) S
  have hlocal : (∏ i, localGood F p i) =
      ∑ U : Finset X, ∏ i, f i (U ∩ block F i) :=
    (sum_block_functions F f).symm
  rw [hlocal]
  unfold mu
  rw [Finset.powerset_univ]
  apply Finset.sum_le_sum
  intro U hU
  by_cases hgood : U ∈ downset F
  · rw [Set.indicator_of_mem hgood, weight_eq_prod_blockWeight F p U]
    apply le_of_eq
    apply Finset.prod_congr rfl
    intro i hi
    have hgi : U ∩ block F i ∈ downset F :=
      isGood_subset_mass F hgood Finset.inter_subset_left
    exact (Set.indicator_of_mem hgi (blockWeight p (block F i))).symm
  · rw [Set.indicator_of_notMem hgood]
    apply Finset.prod_nonneg
    intro i hi
    change 0 ≤ Set.indicator (downset F) (blockWeight p (block F i)) (U ∩ block F i)
    by_cases hgi : U ∩ block F i ∈ downset F
    · rw [Set.indicator_of_mem hgi]
      exact blockWeight_nonneg p _ _ Finset.inter_subset_right (fun v _ => hp v)
    · simp [hgi]

/-- Exact specification (P5), including zero/one coordinate probabilities and the empty
block-index type. Only disjoint block restrictions are factored; crossing events are never
asserted independent. -/
theorem independentBlockHazard (F : RealizedData X) : IndependentBlockHazard F := by
  classical
  intro hF p hp
  have hmass := mu_le_prod_localGood F p hp
  have hcancel : ∀ i, 1 - localFailure F p i = localGood F p i := by
    intro i
    unfold localFailure
    ring
  simp_rw [hcancel]
  refine ⟨hmass, ?_⟩
  intro hmu
  have hprod : 0 < ∏ i, localGood F p i := lt_of_lt_of_le hmu hmass
  have hlocalpos : ∀ i, 0 < localGood F p i := by
    intro i
    have hne : localGood F p i ≠ 0 :=
      (Finset.prod_ne_zero_iff.mp hprod.ne') i (Finset.mem_univ i)
    exact lt_of_le_of_ne (localGood_nonneg F p i (fun v _ => hp v)) (Ne.symm hne)
  constructor
  · rw [Real.log_prod (fun i _ => (hlocalpos i).ne'), ← Finset.sum_neg_distrib]
    apply Finset.sum_le_sum
    intro i hi
    have hlog := Real.log_le_sub_one_of_pos (hlocalpos i)
    unfold localFailure
    linarith
  · have hlog := Real.log_le_log hmu hmass
    linarith

theorem localGood_pos_of_mu_pos (F : RealizedData X) (p : X → ℝ)
    (hp : ∀ v, 0 ≤ p v ∧ p v ≤ 1) (hmu : 0 < mu F p) (i : Fin F.b) :
    0 < localGood F p i := by
  have hprod : 0 < ∏ i, localGood F p i :=
    lt_of_lt_of_le hmu (mu_le_prod_localGood F p hp)
  have hne : localGood F p i ≠ 0 :=
    (Finset.prod_ne_zero_iff.mp hprod.ne') i (Finset.mem_univ i)
  exact lt_of_le_of_ne (localGood_nonneg F p i (fun v _ => hp v)) (Ne.symm hne)

/-- Exact full-price assembly display (F13). -/
theorem globalAssemblyHazard (F : RealizedData X) : GlobalAssemblyHazard F := by
  classical
  intro hF p hp
  have hmass := mu_le_prod_localGood F p hp
  refine ⟨hmass, ?_⟩
  intro hmu
  rw [Finset.sum_neg_distrib, ← Real.log_prod
    (fun i _ => (localGood_pos_of_mu_pos F p hp hmu i).ne')]
  exact neg_le_neg (Real.log_le_log hmu hmass)

theorem muOf_pos_of_empty_mem (A : Finset (Finset X)) (p : X → ℝ)
    (hA : ∅ ∈ A) (hp0 : ∀ v, 0 ≤ p v) (hp1 : ∀ v, p v < 1) :
    0 < muOf A p := by
  have hweight : 0 < weight p ∅ := by
    simp only [weight, Finset.prod_empty, Finset.sdiff_empty, one_mul]
    exact Finset.prod_pos (fun v _ => sub_pos.mpr (hp1 v))
  have hle : weight p ∅ ≤ muOf A p :=
    Finset.single_le_sum (fun U _ => weight_nonneg_mass p (fun v => ⟨hp0 v, (hp1 v).le⟩) U) hA
  exact hweight.trans_le hle

#check blockWeight_nonneg
#check sum_blockWeight
#check cylinder_mass
#check selected_product_le_localFailure
#check localGood_nonneg
#check localGood_le_one
#check localFailure_nonneg
#check localFailure_le_one
#check muOf_nonneg
#check muOf_le_one
#check muOf_pos_of_empty_mem
#check mu_nonneg
#check mu_le_one
#check sum_block_functions
#check weight_eq_prod_blockWeight
#print axioms cylinder_mass
#print axioms selected_product_le_localFailure
#print axioms sum_block_functions
#print axioms muOf_pos_of_empty_mem
#check mu_le_prod_localGood
#check localGood_pos_of_mu_pos
#check globalAssemblyHazard
#print axioms globalAssemblyHazard
#check independentBlockHazard
#print axioms independentBlockHazard

end UniversalLaw.P15Closure
