import SourcePinPreservingQuartic

noncomputable section
open I4SmoothCarrier I4SourceConfluentPins I4SourceConditionalMajorant
open I4SourcePinCurvatureBounds I4SourcePinPreservingQuartic
open I4SourceEndpointRegression I4SourceEndpointEstimates I4SourceSmoothPalm
open MeasureTheory Filter Set Matrix WithLp
open scoped BigOperators Topology
set_option autoImplicit false

namespace I4SourcePinPreservingQuartic

theorem sourceQuartic_value_comparison {L : ℝ} (hL : L ≠ 0) (r : ℝ) (hr : 0 < r)
    (ω : SmoothSample 2 L) (hp : sourcePhysicalPins L r ω) (p : SourcePlane) :
    ‖sourceScaledGradient L r ω p-sourceQuartic L r ω p‖ ≤
      sourceDerivativeMajorant L 5 ω*r^2*(1/120+‖p‖/64+‖p‖^2/80+‖p‖^4/12) := by
  calc
    _ ≤ ‖sourceScaledGradient L r ω p-sourceGradientTaylor L r ω p‖+
        ‖sourceGradientTaylor L r ω p-sourceQuartic L r ω p‖ := norm_sub_le_norm_sub_add_norm_sub _ _ _
    _ ≤ sourceDerivativeMajorant L 5 ω*r^2*‖p‖^4/12+
        sourceDerivativeMajorant L 5 ω*r^2*(1/120+‖p‖/64+‖p‖^2/80) :=
      add_le_add (source_scaled_gradient_taylor_error hL r hr ω p)
        (sourceGradientTaylor_quartic_error_le hL r hr ω hp p)
    _ = _ := by ring

theorem sourceQuartic_operator_comparison {L : ℝ} (hL : L ≠ 0) (r : ℝ) (hr : 0 < r)
    (ω : SmoothSample 2 L) (hp : sourcePhysicalPins L r ω) (p : SourcePlane) :
    ‖fderiv ℝ (sourceScaledGradient L r ω) p-fderiv ℝ (sourceQuartic L r ω) p‖ ≤
      sourceDerivativeMajorant L 5 ω*r^2*(1/96+‖p‖/40+‖p‖^3/3) := by
  calc
    _ ≤ ‖fderiv ℝ (sourceScaledGradient L r ω) p-
          matrixLinearEuclidean (sourceHessianTaylor L r ω (ofLp p))‖+
        ‖matrixLinearEuclidean (sourceHessianTaylor L r ω (ofLp p))-
          fderiv ℝ (sourceQuartic L r ω) p‖ := norm_sub_le_norm_sub_add_norm_sub _ _ _
    _ ≤ sourceDerivativeMajorant L 5 ω*r^2*‖p‖^3/3+
        sourceDerivativeMajorant L 5 ω*r^2*(1/96+‖p‖/40) :=
      add_le_add (source_scaled_hessian_taylor_error hL r hr ω p)
        (sourceHessianTaylor_quartic_error_le hL r hr ω hp p)
    _ = _ := by ring

/-- Uniform value and induced-operator errors on the Euclidean ball. These
two simultaneous uniform bounds are the maximum C1 convention of LM004. -/
theorem sourceQuartic_C1_comparison {L : ℝ} (hL : L ≠ 0) (r : ℝ) (hr : 0 < r)
    (ω : SmoothSample 2 L) (hp : sourcePhysicalPins L r ω) :
    ∀ p : SourcePlane, ‖p‖ ≤ 2 →
      max ‖sourceScaledGradient L r ω p-sourceQuartic L r ω p‖
        ‖fderiv ℝ (sourceScaledGradient L r ω) p-fderiv ℝ (sourceQuartic L r ω) p‖ ≤
          3*r^2*sourceDerivativeMajorant L 5 ω := by
  intro p hp2
  have hG := sourceDerivativeMajorant_nonneg L 5 ω
  have hS : 0 ≤ sourceDerivativeMajorant L 5 ω*r^2 := mul_nonneg hG (sq_nonneg r)
  have h2 : ‖p‖^2 ≤ (2:ℝ)^2 := pow_le_pow_left₀ (norm_nonneg p) hp2 2
  have h3 : ‖p‖^3 ≤ (2:ℝ)^3 := pow_le_pow_left₀ (norm_nonneg p) hp2 3
  have h4 : ‖p‖^4 ≤ (2:ℝ)^4 := pow_le_pow_left₀ (norm_nonneg p) hp2 4
  have hv : (1:ℝ)/120+‖p‖/64+‖p‖^2/80+‖p‖^4/12 ≤ 3 := by nlinarith
  have hd : (1:ℝ)/96+‖p‖/40+‖p‖^3/3 ≤ 3 := by nlinarith
  apply max_le
  · calc
      _ ≤ sourceDerivativeMajorant L 5 ω*r^2*
          (1/120+‖p‖/64+‖p‖^2/80+‖p‖^4/12) := sourceQuartic_value_comparison hL r hr ω hp p
      _ ≤ sourceDerivativeMajorant L 5 ω*r^2*3 := mul_le_mul_of_nonneg_left hv hS
      _ = _ := by ring
  · calc
      _ ≤ sourceDerivativeMajorant L 5 ω*r^2*(1/96+‖p‖/40+‖p‖^3/3) :=
        sourceQuartic_operator_comparison hL r hr ω hp p
      _ ≤ sourceDerivativeMajorant L 5 ω*r^2*3 := mul_le_mul_of_nonneg_left hd hS
      _ = _ := by ring

theorem sourceQuartic_cutoff_tolerance {L : ℝ} (hL : L ≠ 0) (r : ℝ)
    (hr : 0 < r) (hr1 : r ≤ 1) (ω : SmoothSample 2 L)
    (hp : sourcePhysicalPins L r ω)
    (hcut : r*sourceGammaRadius L ω^5 ≤ quarticEpsilonStar) :
    r*sourceRawRadius L ω^5 ≤ 1/(1024*quarticK0) ∧
    (∀ p : SourcePlane, ‖p‖ ≤ 2 →
      max ‖sourceScaledGradient L r ω p-sourceQuartic L r ω p‖
        ‖fderiv ℝ (sourceScaledGradient L r ω) p-fderiv ℝ (sourceQuartic L r ω) p‖ ≤
          sourceRawRadius L ω*quarticWidth r (sourceRawU L ω) (sourceRawRadius L ω)/4) := by
  have hR0 := sourceRawRadius_one_le L ω
  have hR := one_le_sourceGammaRadius L ω
  have hR0R := sourceRawRadius_le_global hL ω
  have hG := sourceDerivativeMajorant_nonneg L 5 ω
  have hGR : sourceDerivativeMajorant L 5 ω ≤ sourceGammaRadius L ω :=
    sourceDerivativeMajorant_le_radius L ω 5
  refine ⟨cutoff_raw_regularity r _ _ hr.le hR0 hR0R hcut,?_⟩
  intro p hp2
  exact (sourceQuartic_C1_comparison hL r hr ω hp p hp2).trans
    (cutoff_quarticWidth_tolerance r _ _ _ _ hr.le hr1 hR hR0 hR0R hG hGR hcut)

theorem sourceQuartic_curvature_threshold {L : ℝ} (hL : L ≠ 0) (r : ℝ) (hr : 0 < r)
    (ω : SmoothSample 2 L)
    (hq : sourceQ L ω ≤ -quarticKcap*r*sourceGammaRadius L ω^5) :
    sourceQ L ω/r ≤ -(2*quarticK0*sourceRawRadius L ω^5+2*sourceRawRadius L ω) :=
  cutoff_curvature_threshold _ r _ _ hr (one_le_sourceGammaRadius L ω)
    (sourceRawRadius_one_le L ω) (sourceRawRadius_le_global hL ω) hq

theorem sourceQuartic_C1_comparison_ae {L : ℝ} (hL : L ≠ 0) (r b : ℝ) (hr : 0 < r)
    (hG : IsUnit (sourcePinCovarianceAt L r)) :
    ∀ᵐ ω ∂sourceSmoothLaw hL r b, ∀ p : SourcePlane, ‖p‖ ≤ 2 →
      max ‖sourceScaledGradient L r ω p-sourceQuartic L r ω p‖
        ‖fderiv ℝ (sourceScaledGradient L r ω) p-fderiv ℝ (sourceQuartic L r ω) p‖ ≤
          3*r^2*sourceDerivativeMajorant L 5 ω := by
  filter_upwards [sourcePhysicalPins_ae hL r b hr.ne' hG] with ω hω
  exact sourceQuartic_C1_comparison hL r hr ω hω

theorem sourceQuartic_C1_estimates {L : ℝ} (hL : L ≠ 0) (b : ℝ) :
    ∃ δ : ℝ, 0 < δ ∧ δ ≤ 1 ∧ ∀ r : ℝ, 0 < r → r < δ →
      ∀ᵐ ω ∂sourceSmoothLaw hL r b, ∀ p : SourcePlane, ‖p‖ ≤ 2 →
        max ‖sourceScaledGradient L r ω p-sourceQuartic L r ω p‖
          ‖fderiv ℝ (sourceScaledGradient L r ω) p-fderiv ℝ (sourceQuartic L r ω) p‖ ≤
            3*r^2*sourceDerivativeMajorant L 5 ω := by
  obtain ⟨δ,hδ,hδ1,hpin⟩ := sourcePhysicalPins_eventually hL b
  refine ⟨δ,hδ,hδ1,?_⟩
  intro r hr hrδ
  filter_upwards [hpin r hr hrδ] with ω hω
  exact sourceQuartic_C1_comparison hL r hr ω hω

end I4SourcePinPreservingQuartic
