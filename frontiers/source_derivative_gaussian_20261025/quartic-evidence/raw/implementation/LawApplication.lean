import SourcePinPreservingQuartic

noncomputable section
open I4SmoothCarrier I4SourceConditionalMajorant I4SourcePinCurvatureBounds
open I4SourcePinPreservingQuartic I4SourceEndpointRegression I4SourceSmoothPalm
open MeasureTheory Filter Set
open scoped Topology
set_option autoImplicit false

namespace I4SourcePinPreservingQuartic

theorem sourceQuartic_cutoff_estimates {L : ℝ} (hL : L ≠ 0) (b : ℝ) :
    ∃ δ : ℝ, 0 < δ ∧ δ ≤ 1 ∧ ∀ r : ℝ, 0 < r → r < δ →
      ∀ᵐ ω ∂sourceSmoothLaw hL r b,
        r*sourceGammaRadius L ω^5 ≤ quarticEpsilonStar →
          (r*sourceRawRadius L ω^5 ≤ 1/(1024*quarticK0)) ∧
          (∀ p : SourcePlane, ‖p‖ ≤ 2 →
            max ‖sourceScaledGradient L r ω p-sourceQuartic L r ω p‖
              ‖fderiv ℝ (sourceScaledGradient L r ω) p-fderiv ℝ (sourceQuartic L r ω) p‖ ≤
                sourceRawRadius L ω*quarticWidth r (sourceRawU L ω) (sourceRawRadius L ω)/4) ∧
          (sourceQ L ω ≤ -quarticKcap*r*sourceGammaRadius L ω^5 →
            sourceQ L ω/r ≤ -(2*quarticK0*sourceRawRadius L ω^5+2*sourceRawRadius L ω)) := by
  obtain ⟨δ,hδ,hδ1,hpin⟩ := sourcePhysicalPins_eventually hL b
  refine ⟨δ,hδ,hδ1,?_⟩
  intro r hr hrδ
  have hr1 : r ≤ 1 := hrδ.le.trans hδ1
  filter_upwards [hpin r hr hrδ] with ω hω
  intro hcut
  have h := sourceQuartic_cutoff_tolerance hL r hr hr1 ω hω hcut
  exact ⟨h.1,h.2,sourceQuartic_curvature_threshold hL r hr ω⟩

/-- The actual weighted carrier law inherits the analytic comparison through
its literal density. This is not a geometric point-process Palm assertion. -/
theorem sourceQuartic_weighted_C1_estimates {L : ℝ} (hL : L ≠ 0) (b : ℝ) :
    ∃ δ : ℝ, 0 < δ ∧ δ ≤ 1 ∧ ∀ r : ℝ, 0 < r → r < δ →
      ∀ᵐ ω ∂sourceSmoothWeightedLaw hL r b, ∀ p : SourcePlane, ‖p‖ ≤ 2 →
        max ‖sourceScaledGradient L r ω p-sourceQuartic L r ω p‖
          ‖fderiv ℝ (sourceScaledGradient L r ω) p-fderiv ℝ (sourceQuartic L r ω) p‖ ≤
            3*r^2*sourceDerivativeMajorant L 5 ω := by
  obtain ⟨δ,hδ,hδ1,hbound⟩ := sourceQuartic_C1_estimates hL b
  refine ⟨δ,hδ,hδ1,?_⟩
  intro r hr hrδ
  have hac : sourceSmoothWeightedLaw hL r b ≪ sourceSmoothLaw hL r b := by
    unfold sourceSmoothWeightedLaw ResearchFormalCoreR1.prwMeasure
    exact withDensity_absolutelyContinuous _ _
  exact hac.ae_le (hbound r hr hrδ)

theorem sourceQuartic_weighted_cutoff_estimates {L : ℝ} (hL : L ≠ 0) (b : ℝ) :
    ∃ δ : ℝ, 0 < δ ∧ δ ≤ 1 ∧ ∀ r : ℝ, 0 < r → r < δ →
      ∀ᵐ ω ∂sourceSmoothWeightedLaw hL r b,
        r*sourceGammaRadius L ω^5 ≤ quarticEpsilonStar →
          (r*sourceRawRadius L ω^5 ≤ 1/(1024*quarticK0)) ∧
          (∀ p : SourcePlane, ‖p‖ ≤ 2 →
            max ‖sourceScaledGradient L r ω p-sourceQuartic L r ω p‖
              ‖fderiv ℝ (sourceScaledGradient L r ω) p-fderiv ℝ (sourceQuartic L r ω) p‖ ≤
                sourceRawRadius L ω*quarticWidth r (sourceRawU L ω) (sourceRawRadius L ω)/4) ∧
          (sourceQ L ω ≤ -quarticKcap*r*sourceGammaRadius L ω^5 →
            sourceQ L ω/r ≤ -(2*quarticK0*sourceRawRadius L ω^5+2*sourceRawRadius L ω)) := by
  obtain ⟨δ,hδ,hδ1,hbound⟩ := sourceQuartic_cutoff_estimates hL b
  refine ⟨δ,hδ,hδ1,?_⟩
  intro r hr hrδ
  have hac : sourceSmoothWeightedLaw hL r b ≪ sourceSmoothLaw hL r b := by
    unfold sourceSmoothWeightedLaw ResearchFormalCoreR1.prwMeasure
    exact withDensity_absolutelyContinuous _ _
  exact hac.ae_le (hbound r hr hrδ)

end I4SourcePinPreservingQuartic
