import Specifications.P15
import SpecificationProofs.P15Elementary
import Closure.ProductMass
import Closure.RatioGate

namespace UniversalLaw.P15Closure

open UniversalLaw.Spec.P15

/-- The local good condition is precisely its capacity restriction. -/
theorem localRestriction {X : Type} [Fintype X] [DecidableEq X]
    (F : RealizedData X) : LocalRestriction F := by
  classical
  intro hF i S hS
  constructor
  · intro hgood
    simpa only [Finset.inter_eq_left.mpr hS] using hgood.1 i
  · intro hcard
    have hsupp : supp F S ⊆ {i} := by
      intro j hj
      obtain ⟨v, hv, rfl⟩ := Finset.mem_image.mp hj
      have hvblock := hS hv
      simpa only [block, Finset.mem_filter, Finset.mem_univ, true_and,
        Finset.mem_singleton] using hvblock
    refine ⟨?_, ?_⟩
    · intro j
      by_cases hji : j = i
      · subst j
        simpa only [Finset.inter_eq_left.mpr hS] using hcard
      · have hempty : S ∩ block F j = ∅ := by
          apply Finset.eq_empty_iff_forall_notMem.mpr
          intro v hv
          obtain ⟨hvS, hvj⟩ := Finset.mem_inter.mp hv
          have hvi := hS hvS
          have h1 : F.blk v = i := by simpa [block] using hvi
          have h2 : F.blk v = j := by simpa [block] using hvj
          exact hji (h2.symm.trans h1)
        simp [hempty]
    · intro e he hesub
      have hsub : e ⊆ {i} := hesub.trans hsupp
      have hc := Finset.card_le_card hsub
      have hc2 := hF.2.2.2.1 e he
      simp only [Finset.card_singleton] at hc
      omega

/-- The logarithmic ceiling can be bounded using any common probability ceiling. -/
theorem price_le_div_common (p c pBound : ℝ)
    (hp0 : 0 ≤ p) (hpp : p ≤ pBound) (hp1 : pBound < 1)
    (hc : c ≤ phi p) : c ≤ p / (1 - pBound) := by
  have hp : p < 1 := hpp.trans_lt hp1
  have hphi : phi p ≤ -Real.log (1 - p) := by
    simp only [phi, hp, ↓reduceIte]
    exact min_le_right _ _
  calc
    c ≤ -Real.log (1 - p) := hc.trans hphi
    _ ≤ p / (1 - p) := UniversalLaw.Proofs.P15Elementary.logRatioBound p hp0 hp
    _ ≤ p / (1 - pBound) :=
      div_le_div_of_nonneg_left hp0 (sub_pos.mpr hp1) (by linarith)

/-- The full product is bounded without dividing by selected-coordinate products.
This formulation includes zero coordinates and the zero probability ceiling. -/
theorem generator_ratio_reduction {X : Type} [DecidableEq X]
    (B S : Finset X) (p c : X → ℝ) (pBound : ℝ)
    (hS : S ⊆ B) (hp0 : 0 ≤ pBound) (hp1 : pBound < 1)
    (hp : ∀ v ∈ B, 0 ≤ p v ∧ p v ≤ pBound)
    (hc : ∀ v ∈ B, 0 ≤ c v ∧ c v ≤ phi (p v)) :
    genPrice c B ≤
      (pBound ^ (B.card - S.card) / (1 - pBound) ^ B.card) * (∏ v ∈ S, p v) := by
  classical
  have hden : 0 < (1 - pBound) ^ B.card := pow_pos (sub_pos.mpr hp1) _
  have hprodS : 0 ≤ ∏ v ∈ S, p v :=
    Finset.prod_nonneg (fun v hv => (hp v (hS hv)).1)
  have hrest : (∏ v ∈ B \ S, p v) ≤ pBound ^ (B.card - S.card) := by
    calc
      (∏ v ∈ B \ S, p v) ≤ ∏ _v ∈ B \ S, pBound :=
        Finset.prod_le_prod₀
          (fun v hv => (hp v (Finset.mem_sdiff.mp hv).1).1)
          (fun v hv => (hp v (Finset.mem_sdiff.mp hv).1).2)
      _ = pBound ^ (B.card - S.card) := by
        rw [Finset.prod_const, Finset.card_sdiff_of_subset hS]
  calc
    genPrice c B ≤ ∏ v ∈ B, p v / (1 - pBound) :=
      Finset.prod_le_prod₀ (fun v hv => (hc v hv).1)
        (fun v hv => price_le_div_common (p v) (c v) pBound
          (hp v hv).1 (hp v hv).2 hp1 (hc v hv).2)
    _ = (∏ v ∈ B, p v) / (1 - pBound) ^ B.card := by
      rw [Finset.prod_div_distrib, Finset.prod_const]
    _ = ((∏ v ∈ B \ S, p v) * (∏ v ∈ S, p v)) /
        (1 - pBound) ^ B.card := by rw [Finset.prod_sdiff hS]
    _ ≤ (pBound ^ (B.card - S.card) * (∏ v ∈ S, p v)) /
        (1 - pBound) ^ B.card :=
      div_le_div_of_nonneg_right (mul_le_mul_of_nonneg_right hrest hprodS) hden.le
    _ = _ := by ring

/-- A realized block has an over-capacity selected set of size `a + 1`.
The remaining product carries exactly the exponent in `rhoTest`. -/
theorem exists_block_ratio_witness {X : Type} [Fintype X] [DecidableEq X]
    (F : RealizedData X) (hF : IsRealizedFamily F)
    (p c : X → ℝ) (pBound : ℝ) (hp0 : 0 ≤ pBound) (hp1 : pBound < 1)
    (hc : ∀ v, 0 ≤ c v ∧ c v ≤ phi (p v))
    (i : Fin F.b) (hp : ∀ v ∈ block F i, 0 ≤ p v ∧ p v ≤ pBound) :
    ∃ S ⊆ block F i, S.card = F.a i + 1 ∧
      genPrice c (block F i) ≤ rhoTest (F.a i) (F.d i) pBound * (∏ v ∈ S, p v) := by
  classical
  have had : F.a i ≤ F.a i * F.d i := by
    simpa using Nat.mul_le_mul_left (F.a i) (hF.2.1 i)
  have hcard : F.a i + 1 ≤ (block F i).card := by
    rw [hF.2.2.1 i]
    omega
  obtain ⟨S, hS, hScard⟩ := Finset.exists_subset_card_eq hcard
  refine ⟨S, hS, hScard, ?_⟩
  have hbound := generator_ratio_reduction (block F i) S p c pBound hS hp0 hp1 hp
    (fun v _ => hc v)
  have hexp : (block F i).card - S.card = F.a i * F.d i - F.a i := by
    rw [hF.2.2.1 i, hScard]
    omega
  rw [hexp, hF.2.2.1 i] at hbound
  exact hbound

/-- The transformed ceiling dominates the probability throughout its domain. -/
theorem le_phi (q : ℝ) (hq0 : 0 ≤ q) (hq1 : q ≤ 1) : q ≤ phi q := by
  by_cases hq : q < 1
  · have hlog := Real.log_le_sub_one_of_pos (sub_pos.mpr hq)
    simp only [phi, hq, ↓reduceIte]
    exact le_min hq1 (by linarith)
  · have heq : q = 1 := le_antisymm hq1 (not_lt.mp hq)
    simp [phi, heq]

/-- The full block has price at most its sufficient ratio times actual failure. -/
theorem local_ratio_bound {X : Type} [Fintype X] [DecidableEq X]
    (F : RealizedData X) (hF : IsRealizedFamily F)
    (p c : X → ℝ) (pBound : ℝ) (hp0 : 0 ≤ pBound) (hp1 : pBound < 1)
    (hc : ∀ v, 0 ≤ c v ∧ c v ≤ phi (p v))
    (i : Fin F.b) (hp : ∀ v ∈ block F i, 0 ≤ p v ∧ p v ≤ pBound) :
    genPrice c (block F i) ≤ rhoTest (F.a i) (F.d i) pBound * localFailure F p i := by
  obtain ⟨S, hS, hScard, hprice⟩ :=
    exists_block_ratio_witness F hF p c pBound hp0 hp1 hc i hp
  have hprod := selected_product_le_localFailure F p i S hS
    (by omega) (fun v hv => ⟨(hp v hv).1, (hp v hv).2.trans hp1.le⟩)
  have hrho : 0 ≤ rhoTest (F.a i) (F.d i) pBound :=
    div_nonneg (pow_nonneg hp0 _) (pow_nonneg (sub_pos.mpr hp1).le _)
  exact hprice.trans (mul_le_mul_of_nonneg_left hprod hrho)

/-- Exact closure of the specification's block-local sufficient ratio test. -/
theorem rhoTestSufficient {X : Type} [Fintype X] [DecidableEq X]
    (F : RealizedData X) : RhoTestSufficient F := by
  intro hF p c pBound hp0 hp1 hc i hp hrho
  have hq := localFailure_nonneg F p i
    (fun v hv => ⟨(hp v hv).1, (hp v hv).2.trans hp1.le⟩)
  exact (local_ratio_bound F hF p c pBound hp0 hp1 hc i hp).trans
    (mul_le_of_le_one_left hq hrho)

/-- Exact closure of the restricted local price budget at probability ceiling `1/4`. -/
theorem restrictedLocalBudget {X : Type} [Fintype X] [DecidableEq X]
    (F : RealizedData X) : RestrictedLocalBudget F := by
  intro hF hd p c hp hc i
  have hpB : ∀ v ∈ block F i, 0 ≤ p v ∧ p v ≤ 1 := by
    intro v hv
    exact ⟨(hp v).1, (hp v).2.trans (by norm_num)⟩
  have hq0 := localFailure_nonneg F p i hpB
  have hq1 := localFailure_le_one F p i hpB
  have hrho : rhoTest (F.a i) (F.d i) (1 / 4) ≤ (16 / 27 : ℝ) := by
    have h := UniversalLaw.CertifiedFrontier.rhoTest_envelope (F.a i) (F.d i)
      (1 / 4) (hF.1 i) (hd i) (by norm_num) (by norm_num) (by norm_num)
    norm_num at h ⊢
    exact h
  refine ⟨?_, ?_⟩
  · exact (local_ratio_bound F hF p c (1 / 4) (by norm_num) (by norm_num)
      hc i (fun v _ => hp v)).trans (mul_le_mul_of_nonneg_right hrho hq0)
  · calc
      (16 / 27 : ℝ) * localFailure F p i ≤ localFailure F p i :=
        mul_le_of_le_one_left hq0 (by norm_num)
      _ ≤ phi (localFailure F p i) := le_phi _ hq0 hq1

/-- The original untransformed local price chain, with the exact specification type. -/
theorem localPriceChain {X : Type} [Fintype X] [DecidableEq X]
    (F : RealizedData X) : LocalPriceChain F := by
  intro hF p c hp hc i
  have hcard : F.a i < (block F i).card := by
    have had : F.a i ≤ F.a i * F.d i := by
      simpa using Nat.mul_le_mul_left (F.a i) (hF.2.1 i)
    rw [hF.2.2.1 i]
    omega
  refine ⟨?_, ?_, ?_⟩
  · exact Finset.prod_le_prod₀ (fun v _ => (hc v).1) (fun v _ => (hc v).2)
  · exact selected_product_le_localFailure F p i (block F i) (by rfl) hcard (fun v _ => hp v)
  · exact le_phi _ (localFailure_nonneg F p i (fun v _ => hp v))
      (localFailure_le_one F p i (fun v _ => hp v))

/-- Every transformed-admissible generator has price at most one. -/
theorem genPrice_phi_le_one {X : Type} (c p : X → ℝ) (B : Finset X)
    (hc : ∀ v ∈ B, 0 ≤ c v ∧ c v ≤ phi (p v)) : genPrice c B ≤ 1 := by
  apply Finset.prod_le_one₀ (fun v hv => (hc v hv).1)
  intro v hv
  apply (hc v hv).2.trans
  unfold phi
  split_ifs
  · exact min_le_left _ _
  · exact le_rfl

/-- Enumerating a finite block transports its restricted product weight exactly. -/
theorem blockWeight_map {X : Type} [DecidableEq X] (n : ℕ)
    (e : Fin n ↪ X) (p : X → ℝ) (S : Finset (Fin n)) :
    blockWeight p (Finset.univ.map e) (S.map e) = weight (fun j => p (e j)) S := by
  unfold blockWeight weight
  rw [← Finset.map_sdiff]
  simp only [Finset.prod_map]

/-- A finite block can be enumerated without changing any coordinate. -/
theorem exists_block_embedding {X : Type} [DecidableEq X] (B : Finset X) :
    ∃ e : Fin B.card ↪ X, Finset.univ.map e = B := by
  classical
  let e : Fin B.card ↪ X :=
    ⟨fun j => (B.equivFin.symm j).val, fun j k h =>
      B.equivFin.symm.injective (Subtype.ext h)⟩
  refine ⟨e, ?_⟩
  ext v
  simp only [Finset.mem_map, Finset.mem_univ, true_and]
  constructor
  · rintro ⟨j, rfl⟩
    exact (B.equivFin.symm j).property
  · intro hv
    refine ⟨B.equivFin ⟨v, hv⟩, ?_⟩
    change (B.equivFin.symm (B.equivFin ⟨v, hv⟩)).val = v
    rw [Equiv.symm_apply_apply]

/-- The local good probability agrees with the standard finite capacity family
after any enumeration of its block. -/
theorem localGood_reindex {X : Type} [Fintype X] [DecidableEq X]
    (F : RealizedData X) (hF : IsRealizedFamily F) (p : X → ℝ)
    (i : Fin F.b) (n : ℕ) (e : Fin n ↪ X)
    (he : Finset.univ.map e = block F i) :
    localGood F p i = muOf (capacityFamily n (F.a i)) (fun j => p (e j)) := by
  classical
  have hsets : (block F i).powerset =
      (Finset.univ : Finset (Fin n)).powerset.image (fun S => S.map e) := by
    rw [← he]
    simp only [Finset.map_eq_image, Finset.powerset_image]
  unfold localGood muOf capacityFamily
  rw [hsets, Finset.sum_image]
  · rw [Finset.sum_filter]
    apply Finset.sum_congr rfl
    intro S hS
    have hsub : S.map e ⊆ block F i := by
      rw [← he]
      exact Finset.map_subset_map.mpr (Finset.subset_univ _)
    have hgood : S.map e ∈ downset F ↔ S.card ≤ F.a i := by
      simpa only [downset, Set.mem_setOf_eq, Finset.card_map] using
        localRestriction F hF i (S.map e) hsub
    by_cases hcard : S.card ≤ F.a i
    · rw [Set.indicator_of_mem (hgood.mpr hcard)]
      simp only [hcard, ite_true]
      change blockWeight p (block F i) (S.map e) = _
      rw [← he]
      exact blockWeight_map n e p S
    · rw [Set.indicator_of_notMem (fun h => hcard (hgood.mp h))]
      simp only [hcard, ite_false]
  · exact fun S _ T _ h => Finset.map_injective e h

/-- A nontrivial capacity restriction is a proper decreasing family. -/
theorem capacityFamily_isProper (n a : ℕ) (ha : a < n) :
    IsProperDownset (capacityFamily n a) := by
  classical
  refine ⟨by simp [capacityFamily], ?_, ?_⟩
  · simp [capacityFamily, not_le.mpr ha]
  · intro U hU V hV
    have hUcard := (Finset.mem_filter.mp hU).2
    exact Finset.mem_filter.mpr
      ⟨Finset.mem_powerset.mpr (Finset.subset_univ _), (Finset.card_le_card hV).trans hUcard⟩

/-- The full local transformed-price theorem follows from the generic hazard
interpolation theorem; all enumeration and capacity constants are discharged. -/
theorem localPriceBoundFull_of_hazardPhiBound {X : Type} [Fintype X] [DecidableEq X]
    (F : RealizedData X) (hHaz : HazardPhiBound) : LocalPriceBoundFull F := by
  classical
  intro hF hd p c hp hc i hmu
  let n := (block F i).card
  obtain ⟨e, he⟩ := exists_block_embedding (block F i)
  have hn : 2 * F.a i + 1 ≤ n := by
    have had := Nat.mul_le_mul_left (F.a i) (hd i)
    change 2 * F.a i + 1 ≤ (block F i).card
    rw [hF.2.2.1 i]
    omega
  have hn1 : 1 ≤ n := by omega
  have hproper := capacityFamily_isProper n (F.a i) (by omega)
  have hreindex := localGood_reindex F hF p i n e he
  have hmu' : 0 < muOf (capacityFamily n (F.a i)) (fun j => p (e j)) := by
    rw [← hreindex]
    exact hmu
  have hmain := hHaz n (capacityFamily n (F.a i)) hn1 hproper
    (fun j => p (e j)) (fun j => hp (e j)) hmu'
  rw [← hreindex] at hmain
  have hcap := UniversalLaw.Proofs.P15Elementary.capacityWorstCase
  have hbase : hazardStar (capacityFamily 3 1) = hStar := hcap.2.1.trans hcap.2.2.1
  have hH : hStar ≤ hazardStar (capacityFamily n (F.a i)) := by
    rw [← hbase]
    exact hcap.1 (F.a i) n (hF.1 i) hn
  have hstar0 : 0 < hStar := by linarith [hcap.2.2.2]
  have hprice : genPrice c (block F i) ≤ ∏ j : Fin n, phi (p (e j)) := by
    calc
      genPrice c (block F i) = genPrice c (Finset.univ.map e) :=
        congrArg (genPrice c) he.symm
      _ = ∏ j : Fin n, c (e j) := by
        simp only [genPrice, Finset.prod_map]
        rfl
      _ ≤ ∏ j : Fin n, phi (p (e j)) :=
        Finset.prod_le_prod₀ (fun j _ => (hc (e j)).1) (fun j _ => (hc (e j)).2)
  have hphi0 : 0 ≤ ∏ j : Fin n, phi (p (e j)) := by
    apply Finset.prod_nonneg
    intro j hj
    exact (hc (e j)).1.trans (hc (e j)).2
  have hscaled : genPrice c (block F i) * hStar ≤ -Real.log (localGood F p i) := by
    calc
      genPrice c (block F i) * hStar ≤ (∏ j : Fin n, phi (p (e j))) * hStar :=
        mul_le_mul_of_nonneg_right hprice hstar0.le
      _ ≤ (∏ j : Fin n, phi (p (e j))) * hazardStar (capacityFamily n (F.a i)) :=
        mul_le_mul_of_nonneg_left hH hphi0
      _ ≤ -Real.log (localGood F p i) := by simpa only [mul_comm] using hmain
  refine ⟨?_, genPrice_phi_le_one c p (block F i) (fun v _ => hc v)⟩
  calc
    genPrice c (block F i) ≤ (-Real.log (localGood F p i)) / hStar :=
      (le_div_iff₀ hstar0).mpr hscaled
    _ = rhoStar * (-Real.log (localGood F p i)) := by
      unfold rhoStar hStar
      ring

end UniversalLaw.P15Closure

#check UniversalLaw.P15Closure.localRestriction
#check UniversalLaw.P15Closure.price_le_div_common
#check UniversalLaw.P15Closure.generator_ratio_reduction
#check UniversalLaw.P15Closure.exists_block_ratio_witness
#check UniversalLaw.P15Closure.le_phi
#check UniversalLaw.P15Closure.local_ratio_bound
#check UniversalLaw.P15Closure.rhoTestSufficient
#check UniversalLaw.P15Closure.restrictedLocalBudget
#check UniversalLaw.P15Closure.localPriceChain
#check UniversalLaw.P15Closure.genPrice_phi_le_one
#check UniversalLaw.P15Closure.blockWeight_map
#check UniversalLaw.P15Closure.exists_block_embedding
#check UniversalLaw.P15Closure.localGood_reindex
#check UniversalLaw.P15Closure.capacityFamily_isProper
#check UniversalLaw.P15Closure.localPriceBoundFull_of_hazardPhiBound
#print axioms UniversalLaw.P15Closure.localRestriction
#print axioms UniversalLaw.P15Closure.price_le_div_common
#print axioms UniversalLaw.P15Closure.generator_ratio_reduction
#print axioms UniversalLaw.P15Closure.exists_block_ratio_witness
#print axioms UniversalLaw.P15Closure.le_phi
#print axioms UniversalLaw.P15Closure.local_ratio_bound
#print axioms UniversalLaw.P15Closure.rhoTestSufficient
#print axioms UniversalLaw.P15Closure.restrictedLocalBudget
#print axioms UniversalLaw.P15Closure.localPriceChain
#print axioms UniversalLaw.P15Closure.genPrice_phi_le_one
#print axioms UniversalLaw.P15Closure.blockWeight_map
#print axioms UniversalLaw.P15Closure.exists_block_embedding
#print axioms UniversalLaw.P15Closure.localGood_reindex
#print axioms UniversalLaw.P15Closure.capacityFamily_isProper
#print axioms UniversalLaw.P15Closure.localPriceBoundFull_of_hazardPhiBound
