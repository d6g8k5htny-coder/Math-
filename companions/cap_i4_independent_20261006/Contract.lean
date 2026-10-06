import CapI4Independent
open MeasureTheory ProbabilityTheory Set
open scoped ENNReal

example {Ω : Type*} [MeasurableSpace Ω] (Q : Measure Ω) [IsProbabilityMeasure Q]
    (J : Ω → ℝ) (B : Ω → ℝ × (ℝ × ℝ))
    (hJ : Measurable J) (hB : Measurable B) (hI : IndepFun J B Q)
    (p : ℝ × (ℝ × ℝ) → ℝ≥0∞)
    (hB_law : Measure.map B Q = (volume : Measure (ℝ × (ℝ × ℝ))).withDensity p) :
    Measure.map (fun ω => (J ω, B ω)) Q =
      (Measure.map J Q).prod ((volume : Measure (ℝ × (ℝ × ℝ))).withDensity p) :=
  CapI4Independent.jointLaw_of_independence Q J B hJ hB hI p hB_law

example {Ω : Type*} [MeasurableSpace Ω] (Q : Measure Ω) [IsProbabilityMeasure Q]
    (J : Ω → ℝ) (hJ : Measurable J) : (Measure.map J Q) univ = 1 :=
  CapI4Independent.residual_law_mass Q J hJ

example {Ω : Type*} [MeasurableSpace Ω] (Q : Measure Ω) [IsProbabilityMeasure Q]
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
      ENNReal.ofReal (l.2-l.1) * (H l * K (j,l))) ∂Measure.map J Q :=
  CapI4Independent.independent_weight_bound_ae Q J B hJ hB hI p hB_law H K hp hH hK hdom W hW
