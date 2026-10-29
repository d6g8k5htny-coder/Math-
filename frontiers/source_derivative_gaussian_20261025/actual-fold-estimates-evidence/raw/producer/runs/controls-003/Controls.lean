import SourceAdaptiveFoldEstimates

noncomputable section
open Set MeasureTheory
open I4SmoothCarrier I4SourcePinCurvatureBounds I4SourceCompactTargetMoments
open I4SourceAdaptiveFoldChart I4SourceAdaptiveFoldEstimates
open AdaptiveFoldTransverseRidge AdaptiveFoldBoundaryPath
open scoped ContDiff
set_option autoImplicit false

namespace ActualFoldEstimateControls

def armG (x : ℝ) : ℝ := (x^2-1/4)/2

theorem armG_hasDerivAt (x : ℝ) : HasDerivAt armG x x := by
  convert (((hasDerivAt_id x).pow 2).sub_const (1/4)).div_const 2 using 1
  · rfl
  · ring

theorem full_arm_two_pin : ∀ x ∈ AdaptiveFoldScalar.J,
    |armG x| ≤ 1 ∧ |x| ≤ 2*1 := by
  apply I4ActualFoldTwoPin.two_pin_abs_le_on_J armG id (fun _ => 1) 1 (by norm_num)
  · intro x _hx
    exact armG_hasDerivAt x
  · intro x _hx
    exact hasDerivAt_id x
  · intro x _hx
    norm_num
  · norm_num [armG]
  · norm_num [armG]

theorem outer_arm_counterexample :
    (3/2 : ℝ) ∈ AdaptiveFoldScalar.J ∧ |armG (3/2)| = 1 ∧
      ¬ |armG (3/2)| ≤ (1/8 : ℝ) := by
  norm_num [AdaptiveFoldScalar.J, armG]

/-- This bundle instantiates every named positivity, error and geometric budget. -/
theorem numeric_positive : I4ActualFoldNumeric.NumericalBudget 1 (1/10000) 1024 :=
  I4ActualFoldNumeric.numerical_budget (by norm_num) (by norm_num) (by norm_num) (by norm_num)

theorem omitted_kappa_error : profileError (1/2) 3 1 = 342 := by
  norm_num [profileError, accelerationRadius]

theorem omitted_kappa_counterexample :
    (1 : ℝ) ≤ 1 ∧ (0 : ℝ) < 1/100 ∧ (1/100 : ℝ)*1^5 ≤ 1/100 ∧
    ¬ (1 + profileError (1/2) 3 1 ≤ 2-3*(1/100 : ℝ)*1) := by
  norm_num [omitted_kappa_error]

theorem omitted_r_counterexample :
    (1 : ℝ) ≤ 1 ∧ (0 : ℝ) < 1 ∧ (1024 : ℝ)*1^5 ≤ 1024 ∧
    (2-3*(1 : ℝ)*1) = -1 ∧
    ¬ (1 + profileError (1024/2) (3*1) 1 ≤ 2-3*(1 : ℝ)*1) := by
  norm_num [profileError, accelerationRadius]

theorem nonzero_height_and_nongeneric_scale : (3 : ℝ) ≠ 0 ∧ (1 : ℝ) ≠ 1/6 := by norm_num

/-- Closed actual-law interface at nonzero height and k≠1/6. The sample cutoffs
remain antecedents; this theorem asserts no probability of those cutoffs. -/
theorem closed_actual_structure {L : ℝ} (hL : L ≠ 0) :
    ∃ δ : ℝ, 0 < δ ∧ δ ≤ 1 ∧ ∀ r : ℝ, 0 < r → r < δ →
      ∀ᵐ sample ∂sourceGapLaw hL r 3 1,
        let T := sourceT 1 sample
        let κ := sourceKappa r 1 sample
        r*T^5 ≤ 1/100 → 1024*T^5 ≤ κ →
          StructuralRectangleData (actualFoldPotential r 1 sample) univ
            (4/Real.sqrt κ) (κ/2) T (3*T) T (2-3*r*T) ∧
          T/(κ/2) ≤ 4/Real.sqrt κ ∧
          1 ≤ ((κ/2)/2)*(4/Real.sqrt κ-T/(κ/2))^2 := by
  obtain ⟨δ,hδ,hδ1,h⟩ := sourceGapLaw_structural_rectangle hL
  exact ⟨δ,hδ,hδ1,fun r hr hrδ => h 1 (by norm_num) r hr hrδ 3 1 le_rfl⟩

/-- The same closed interface returns one U,z carrying both consumer bundles. -/
theorem closed_actual_path {L : ℝ} (hL : L ≠ 0) :
    ∃ δ : ℝ, 0 < δ ∧ δ ≤ 1 ∧ ∀ r : ℝ, 0 < r → r < δ →
      ∀ᵐ sample ∂sourceGapLaw hL r 3 1,
        let T := sourceT 1 sample
        let κ := sourceKappa r 1 sample
        r*T^5 ≤ 1/100 → 1024*T^5 ≤ κ →
          ∃ (U : Set ℝ) (z : ℝ → ℝ),
            RidgeScalarData (actualFoldPotential r 1 sample) univ
              (4/Real.sqrt κ) (κ/2) T (3*T) T U z ∧
            RectangleBoundaryPathData (actualFoldPotential r 1 sample)
              (4/Real.sqrt κ) (κ/2) z := by
  obtain ⟨δ,hδ,hδ1,h⟩ := sourceGapLaw_actual_rectangle_boundary_path hL
  exact ⟨δ,hδ,hδ1,fun r hr hrδ => h 1 (by norm_num) r hr hrδ 3 1 le_rfl⟩

end ActualFoldEstimateControls
