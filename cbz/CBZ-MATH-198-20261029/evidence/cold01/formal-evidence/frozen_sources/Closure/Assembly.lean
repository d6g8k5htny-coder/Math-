import Closure.ProductMass
import Closure.PaletteCover
import Closure.LocalRatio
import Closure.HazardInterpolation

namespace UniversalLaw.P15Closure
open UniversalLaw.Spec.P15
open scoped BigOperators

variable {X : Type} [Fintype X] [DecidableEq X]

theorem famPrice_nonneg_closure (c : X → ℝ) (hc : ∀ v, 0 ≤ c v)
    (G : Finset (Finset X)) : 0 ≤ famPrice c G := by
  exact Finset.sum_nonneg (fun g _ => Finset.prod_nonneg (fun v _ => hc v))

theorem coverCost_le_family (F : RealizedData X) (K : ℕ) (c : X → ℝ)
    (hc : ∀ v, 0 ≤ c v) (G : Finset (Finset X))
    (hG : IsGeneratorCover F K G) : coverCost F K c ≤ famPrice c G := by
  apply csInf_le
  · refine ⟨0, ?_⟩
    rintro t ⟨H, _, rfl⟩
    exact famPrice_nonneg_closure c hc H
  · exact ⟨G, hG, rfl⟩

theorem coverCost_le_one (F : RealizedData X) (K : ℕ) (c : X → ℝ)
    (hc : ∀ v, 0 ≤ c v) : coverCost F K c ≤ 1 := by
  classical
  have hG : IsGeneratorCover F K ({∅} : Finset (Finset X)) := by
    intro U _
    exact ⟨∅, by simp, Finset.empty_subset U⟩
  simpa [famPrice, genPrice] using coverCost_le_family F K c hc {∅} hG

theorem realized_block_injective (F : RealizedData X) (hF : IsRealizedFamily F) :
    Function.Injective (block F) := by
  intro i j hij
  have hpos : 0 < (block F i).card := by rw [hF.2.2.1 i]; omega
  obtain ⟨x, hxi⟩ := Finset.card_pos.mp hpos
  have hxj : x ∈ block F j := by rw [← hij]; exact hxi
  have hi : F.blk x = i := (Finset.mem_filter.mp hxi).2
  have hj : F.blk x = j := (Finset.mem_filter.mp hxj).2
  exact hi.symm.trans hj

theorem famPrice_fullBlockFamily (F : RealizedData X) (hF : IsRealizedFamily F)
    (c : X → ℝ) :
    famPrice c (fullBlockFamily F) = ∑ i, genPrice c (block F i) := by
  classical
  unfold famPrice fullBlockFamily
  rw [Finset.sum_image]
  intro i _ j _ hij
  exact realized_block_injective F hF hij

theorem rhoStar_pos_closure : 0 < rhoStar := by
  change 0 < 1 / hStar
  have h : 1 < hStar := UniversalLaw.Proofs.P15Elementary.capacityWorstCase.2.2.2
  exact div_pos zero_lt_one (by linarith)

theorem coverCost_capped_of_sum (F : RealizedData X) (K : ℕ) (c : X → ℝ)
    (hc : ∀ v, 0 ≤ c v) (ρ m : ℝ)
    (hcover : IsGeneratorCover F K (fullBlockFamily F))
    (hsum : 0 < m → famPrice c (fullBlockFamily F) ≤ ρ * (-Real.log m)) :
    coverCost F K c ≤ cappedHazard ρ m := by
  by_cases hm : 0 < m
  · rw [cappedHazard, if_pos hm]
    exact le_min (coverCost_le_one F K c hc)
      ((coverCost_le_family F K c hc (fullBlockFamily F) hcover).trans (hsum hm))
  · rw [cappedHazard, if_neg hm]
    exact coverCost_le_one F K c hc

/-- A conditional assembly theorem; its local/global hypotheses are not erased. -/
theorem fullBudget_of_bridges (F : RealizedData X)
    (hlocal : LocalPriceBoundFull F) (hglobal : GlobalAssemblyHazard F) :
    FullTransformedPriceBudget F := by
  intro hF hd p c hp hc K hK
  have hc0 : ∀ v, 0 ≤ c v := fun v => (hc v).1
  have hcover := fullBlockCover_of_paletteNumber_le F hF hK
  apply coverCost_capped_of_sum F K c hc0 rhoStar (mu F p) hcover
  intro hmu
  have hg := hglobal hF p hp
  have hprod : 0 < ∏ i, localGood F p i := lt_of_lt_of_le hmu hg.1
  have hgood : ∀ i, 0 < localGood F p i := by
    intro i
    have hn := localGood_nonneg F p i (fun v _ => hp v)
    by_contra hnpos
    have hz : localGood F p i = 0 := le_antisymm (le_of_not_gt hnpos) hn
    have hzero : (∏ j, localGood F p j) = 0 := Finset.prod_eq_zero (Finset.mem_univ i) hz
    linarith
  rw [famPrice_fullBlockFamily F hF]
  calc
    _ ≤ ∑ i, rhoStar * (-Real.log (localGood F p i)) :=
      Finset.sum_le_sum (fun i _ => (hlocal hF hd p c hp hc i (hgood i)).1)
    _ = rhoStar * ∑ i, -Real.log (localGood F p i) := (Finset.mul_sum _ _ _).symm
    _ ≤ rhoStar * (-Real.log (mu F p)) :=
      mul_le_mul_of_nonneg_left (hg.2 hmu) rhoStar_pos_closure.le

theorem restrictedTransformedPriceBudget (F : RealizedData X) :
    RestrictedTransformedPriceBudget F := by
  intro hF hd p c hp hc K hK
  have hp01 : ∀ v, 0 ≤ p v ∧ p v ≤ 1 := fun v => ⟨(hp v).1, by linarith [(hp v).2]⟩
  have hc0 : ∀ v, 0 ≤ c v := fun v => (hc v).1
  have hcover := fullBlockCover_of_paletteNumber_le F hF hK
  apply coverCost_capped_of_sum F K c hc0 (16/27) (mu F p) hcover
  intro hmu
  have hlocal := restrictedLocalBudget F hF hd p c hp hc
  have hglobal := (independentBlockHazard F hF p hp01).2 hmu
  rw [famPrice_fullBlockFamily F hF]
  calc
    _ ≤ ∑ i, (16/27) * localFailure F p i :=
      Finset.sum_le_sum (fun i _ => (hlocal i).1)
    _ = (16/27) * ∑ i, localFailure F p i := (Finset.mul_sum _ _ _).symm
    _ ≤ (16/27) * (-Real.log (mu F p)) :=
      mul_le_mul_of_nonneg_left (hglobal.1.trans hglobal.2) (by norm_num)

theorem localPriceBoundFull (F : RealizedData X) : LocalPriceBoundFull F :=
  localPriceBoundFull_of_hazardPhiBound F hazardPhiBound

/-- The exact headline proposition, with no unproved bridge hypotheses. -/
theorem fullTransformedPriceBudget (F : RealizedData X) :
    FullTransformedPriceBudget F :=
  fullBudget_of_bridges F (localPriceBoundFull F) (globalAssemblyHazard F)

/-- The original-price realized-cover bound allows the original d>=1 domain. -/
theorem coverCostHazardBound (F : RealizedData X) : CoverCostHazardBound F := by
  intro hF p c hp hc K hK
  have hc0 : ∀ v, 0 ≤ c v := fun v => (hc v).1
  have hcover := fullBlockCover_of_paletteNumber_le F hF hK
  apply coverCost_capped_of_sum F K c hc0 1 (mu F p) hcover
  intro hmu
  have hlocal := localPriceChain F hF p c hp hc
  have hg := (independentBlockHazard F hF p hp).2 hmu
  rw [famPrice_fullBlockFamily F hF]
  calc
    _ ≤ ∑ i, localFailure F p i :=
      Finset.sum_le_sum (fun i _ => (hlocal i).1.trans (hlocal i).2.1)
    _ ≤ -Real.log (mu F p) := hg.1.trans hg.2
    _ = 1 * (-Real.log (mu F p)) := by ring

theorem fullTransformedPriceBudget_sixSevenths (F : RealizedData X)
    (hF : IsRealizedFamily F) (hd : ∀ i, 2 ≤ F.d i)
    (p c : X → ℝ) (hp : ∀ v, 0 ≤ p v ∧ p v ≤ 1)
    (hc : ∀ v, 0 ≤ c v ∧ c v ≤ phi (p v))
    (K : ℕ) (hK : paletteNumber F.b F.H F.d ≤ K) :
    coverCost F K c ≤ cappedHazard (6/7) (mu F p) := by
  apply (fullTransformedPriceBudget F hF hd p c hp hc K hK).trans
  by_cases hm : 0 < mu F p
  · simp only [cappedHazard, if_pos hm]
    apply min_le_min le_rfl
    have hlog : 0 ≤ -Real.log (mu F p) := by
      have h := Real.log_le_log hm (mu_le_one F p hp)
      exact neg_nonneg.mpr (by simpa only [Real.log_one] using h)
    exact mul_le_mul_of_nonneg_right
      UniversalLaw.Proofs.P15Elementary.rhoStarBelowSixSevenths.le hlog
  · simp only [cappedHazard, if_neg hm, le_refl]

end UniversalLaw.P15Closure

#check UniversalLaw.P15Closure.fullBudget_of_bridges
#check UniversalLaw.P15Closure.restrictedTransformedPriceBudget
#check UniversalLaw.P15Closure.localPriceBoundFull
#check UniversalLaw.P15Closure.fullTransformedPriceBudget
#check UniversalLaw.P15Closure.coverCostHazardBound
#check UniversalLaw.P15Closure.fullTransformedPriceBudget_sixSevenths
#print axioms UniversalLaw.P15Closure.coverCost_le_family
#print axioms UniversalLaw.P15Closure.fullBudget_of_bridges
#print axioms UniversalLaw.P15Closure.restrictedTransformedPriceBudget
#print axioms UniversalLaw.P15Closure.localPriceBoundFull
#print axioms UniversalLaw.P15Closure.fullTransformedPriceBudget
#print axioms UniversalLaw.P15Closure.coverCostHazardBound
#print axioms UniversalLaw.P15Closure.fullTransformedPriceBudget_sixSevenths
