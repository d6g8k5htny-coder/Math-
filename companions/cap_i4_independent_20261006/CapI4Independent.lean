import CapI4ProductTransport
import Mathlib.Probability.Independence.Basic

/-!
Original probability-law independence supplies the product-law premise used by
Cap I4's density transport. Almost-everywhere weight bounds suffice. The field's
independence, marginal density and deterministic envelope remain caller inputs.
-/
noncomputable section
set_option autoImplicit false
open MeasureTheory ProbabilityTheory Set
open scoped ENNReal
namespace CapI4Independent

/-- Independence concerns the original law and the entire matrix-valued variable. -/
theorem jointLaw_of_independence {Ω : Type*} [MeasurableSpace Ω]
    (Q : Measure Ω) [IsProbabilityMeasure Q]
    (J : Ω → ℝ) (B : Ω → ℝ × (ℝ × ℝ))
    (hJ : Measurable J) (hB : Measurable B) (hI : IndepFun J B Q)
    (p : ℝ × (ℝ × ℝ) → ℝ≥0∞)
    (hB_law : Measure.map B Q = (volume : Measure (ℝ × (ℝ × ℝ))).withDensity p) :
    Measure.map (fun ω => (J ω, B ω)) Q =
      (Measure.map J Q).prod ((volume : Measure (ℝ × (ℝ × ℝ))).withDensity p) := by
  simpa only [hB_law] using hI.map_prod_eq_prod_map_map hJ.aemeasurable hB.aemeasurable

/-- The actual residual marginal has unit mass, not an unspecified envelope mass. -/
theorem residual_law_mass {Ω : Type*} [MeasurableSpace Ω]
    (Q : Measure Ω) [IsProbabilityMeasure Q] (J : Ω → ℝ) (hJ : Measurable J) :
    (Measure.map J Q) univ = 1 := by
  rw [Measure.map_apply hJ MeasurableSet.univ]
  simp

/-- Null exceptional configurations need not satisfy the pointwise weight envelope. -/
theorem independent_weight_bound_ae {Ω : Type*} [MeasurableSpace Ω]
    (Q : Measure Ω) [IsProbabilityMeasure Q]
    (J : Ω → ℝ) (B : Ω → ℝ × (ℝ × ℝ))
    (hJ : Measurable J) (hB : Measurable B) (hI : IndepFun J B Q)
    (p : ℝ × (ℝ × ℝ) → ℝ≥0∞)
    (hB_law : Measure.map B Q = (volume : Measure (ℝ × (ℝ × ℝ))).withDensity p)
    (H : ℝ × ℝ → ℝ≥0∞) (K : ℝ × (ℝ × ℝ) → ℝ≥0∞)
    (hp : Measurable p) (hH : Measurable H) (hK : Measurable K)
    (hdom : ∀ e, p e ≤ H (CapI4Polar.eigenvalues e))
    (W : Ω → ℝ≥0∞)
    (hW : ∀ᵐ ω ∂Q, W ω ≤ if 0 < (CapI4Polar.eigenvalues (B ω)).1 then
      K (J ω,CapI4Polar.eigenvalues (B ω)) else 0) :
    (∫⁻ ω, W ω ∂Q) ≤
    ∫⁻ j, (ENNReal.ofReal Real.pi * ∫⁻ l : ℝ × ℝ in {l | 0 < l.1 ∧ l.1 < l.2},
      ENNReal.ofReal (l.2-l.1) * (H l * K (j,l))) ∂Measure.map J Q := by
  let : IsFiniteMeasure ((volume : Measure (ℝ × (ℝ × ℝ))).withDensity p) := by
    rw [← hB_law]
    infer_instance
  have hlaw := jointLaw_of_independence Q J B hJ hB hI p hB_law
  exact (lintegral_mono_ae hW).trans
    (CapI4ProductTransport.jointLaw_positive_spectral_bound Q J B hJ hB
      (Measure.map J Q) p H K hp hH hK hdom hlaw)

end CapI4Independent
