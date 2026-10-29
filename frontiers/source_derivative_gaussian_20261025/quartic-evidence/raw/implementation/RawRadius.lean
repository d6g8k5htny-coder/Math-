import SourcePinPreservingQuartic

noncomputable section
open I4SmoothCarrier I4SourceConfluentPins I4SourcePinCurvatureBounds
open I4SourceConditionalMajorant I4SourcePinPreservingQuartic I4SourceSmoothPalm
open I4SourceEndpointRegression I4SourceEndpointEstimates
open MeasureTheory Filter Set
open scoped BigOperators Topology
set_option autoImplicit false

namespace I4SourcePinPreservingQuartic

theorem source_origin_derivative_abs_le {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L)
    (k : ℕ) (u : Fin k → (Fin 2 → ℝ)) (hu : ∀ i, ‖u i‖ ≤ 1) :
    |iteratedFDeriv ℝ k (smoothSourceField 2 L ω) 0 u| ≤
      sourceDerivativeMajorant L k ω := by
  have h0 : (![0,0] : Fin 2 → ℝ) = 0 := by ext i; fin_cases i <;> rfl
  simpa only [h0] using source_axis_derivative_abs_le hL ω k u hu 0

theorem sourceRawU_abs_le {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) (i : Fin 8) :
    |sourceRawU L ω i| ≤ if (i : ℕ) < 3 then sourceDerivativeMajorant L 3 ω
      else sourceDerivativeMajorant L 4 ω := by
  fin_cases i
  · exact sourceA_abs_le hL ω
  all_goals
    apply source_origin_derivative_abs_le hL ω
    intro j
    fin_cases j <;> first | exact directionX_norm_le_one | exact directionY_norm_le_one

theorem sourceRawRadius_one_le (L : ℝ) (ω : SmoothSample 2 L) :
    1 ≤ sourceRawRadius L ω :=
  le_add_of_nonneg_right (Finset.sum_nonneg (fun _ _ => abs_nonneg _))

theorem sourceRawRadius_le_majorants {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) :
    sourceRawRadius L ω ≤ 1+3*sourceDerivativeMajorant L 3 ω+5*sourceDerivativeMajorant L 4 ω := by
  calc
    _ ≤ 1+∑ i : Fin 8, if (i : ℕ) < 3 then sourceDerivativeMajorant L 3 ω
        else sourceDerivativeMajorant L 4 ω :=
      by
        change 1+(∑ i : Fin 8, |sourceRawU L ω i|) ≤ _
        exact add_le_add le_rfl (Finset.sum_le_sum (fun i _ => sourceRawU_abs_le hL ω i))
    _ = _ := by norm_num [Fin.sum_univ_succ]; ring

theorem sourceRawRadius_le_global {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) :
    sourceRawRadius L ω ≤ 5*sourceGammaRadius L ω := by
  have h := sourceRawRadius_le_majorants hL ω
  have hg := sourceGammaRadius_ge_third_fourth L ω
  have h3 := sourceDerivativeMajorant_nonneg L 3 ω
  linarith

theorem sourcePhysicalPins_ae {L : ℝ} (hL : L ≠ 0) (r b : ℝ) (hr : r ≠ 0)
    (hG : IsUnit (sourcePinCovarianceAt L r)) :
    ∀ᵐ ω ∂sourceSmoothLaw hL r b, sourcePhysicalPins L r ω := by
  filter_upwards [sourceSmoothLaw_raw_pin_fiber_ae hL r b hr hG] with ω hω
  unfold sourcePhysicalPins
  rw [hω]
  simp
  ring

theorem sourcePhysicalPins_eventually {L : ℝ} (hL : L ≠ 0) (b : ℝ) :
    ∃ δ : ℝ, 0 < δ ∧ δ ≤ 1 ∧ ∀ r : ℝ, 0 < r → r < δ →
      ∀ᵐ ω ∂sourceSmoothLaw hL r b, sourcePhysicalPins L r ω := by
  obtain ⟨δ,hδ,hsub⟩ := mem_nhdsGT_iff_exists_Ioo_subset.mp
    (sourceEndpoint_parameter_limits hL b).1
  refine ⟨min δ 1,lt_min hδ (by norm_num),min_le_right _ _,?_⟩
  intro r hr hrδ
  exact sourcePhysicalPins_ae hL r b hr.ne'
    (hsub ⟨hr,lt_of_lt_of_le hrδ (min_le_left _ _)⟩)

end I4SourcePinPreservingQuartic
