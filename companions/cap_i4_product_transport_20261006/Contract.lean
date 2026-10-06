import CapI4ProductTransport
open MeasureTheory Set
open scoped ENNReal

example (K : ℝ × (ℝ × ℝ) → ℝ≥0∞) (hK : Measurable K) :
    Measurable (fun z : ℝ × (ℝ × (ℝ × ℝ)) =>
      if 0 < (CapI4Polar.eigenvalues z.2).1 then K (z.1, CapI4Polar.eigenvalues z.2) else 0) :=
  CapI4ProductTransport.positive_test_measurable K hK

example (p : ℝ × (ℝ × ℝ) → ℝ≥0∞) (H G : ℝ × ℝ → ℝ≥0∞)
    (hp : Measurable p) (hH : Measurable H) (hG : Measurable G)
    (hdom : ∀ e, p e ≤ H (CapI4Polar.eigenvalues e)) :
    (∫⁻ e : ℝ × (ℝ × ℝ),
      if 0 < (CapI4Polar.eigenvalues e).1 then G (CapI4Polar.eigenvalues e) else 0
      ∂(volume : Measure (ℝ × (ℝ × ℝ))).withDensity p) ≤
    ENNReal.ofReal Real.pi * ∫⁻ l : ℝ × ℝ in {l | 0 < l.1 ∧ l.1 < l.2},
      ENNReal.ofReal (l.2-l.1) * (H l * G l) :=
  CapI4ProductTransport.withDensity_positive_spectral_bound p H G hp hH hG hdom

example (ν : Measure ℝ) (p : ℝ × (ℝ × ℝ) → ℝ≥0∞)
    (H : ℝ × ℝ → ℝ≥0∞) (K : ℝ × (ℝ × ℝ) → ℝ≥0∞)
    (hp : Measurable p) (hH : Measurable H)
    (hK : ∀ j, Measurable (fun l => K (j,l)))
    (hdom : ∀ e, p e ≤ H (CapI4Polar.eigenvalues e)) :
    (∫⁻ j, ∫⁻ e : ℝ × (ℝ × ℝ),
      if 0 < (CapI4Polar.eigenvalues e).1 then K (j,CapI4Polar.eigenvalues e) else 0
      ∂(volume : Measure (ℝ × (ℝ × ℝ))).withDensity p ∂ν) ≤
    ∫⁻ j, (ENNReal.ofReal Real.pi * ∫⁻ l : ℝ × ℝ in {l | 0 < l.1 ∧ l.1 < l.2},
      ENNReal.ofReal (l.2-l.1) * (H l * K (j,l))) ∂ν :=
  CapI4ProductTransport.residual_iterated_positive_spectral_bound ν p H K hp hH hK hdom

example (ν : Measure ℝ) (p : ℝ × (ℝ × ℝ) → ℝ≥0∞)
    [SFinite ((volume : Measure (ℝ × (ℝ × ℝ))).withDensity p)]
    (H : ℝ × ℝ → ℝ≥0∞) (K : ℝ × (ℝ × ℝ) → ℝ≥0∞)
    (hp : Measurable p) (hH : Measurable H) (hK : Measurable K)
    (hdom : ∀ e, p e ≤ H (CapI4Polar.eigenvalues e)) :
    (∫⁻ z : ℝ × (ℝ × (ℝ × ℝ)),
      if 0 < (CapI4Polar.eigenvalues z.2).1 then K (z.1,CapI4Polar.eigenvalues z.2) else 0
      ∂ν.prod ((volume : Measure (ℝ × (ℝ × ℝ))).withDensity p)) ≤
    ∫⁻ j, (ENNReal.ofReal Real.pi * ∫⁻ l : ℝ × ℝ in {l | 0 < l.1 ∧ l.1 < l.2},
      ENNReal.ofReal (l.2-l.1) * (H l * K (j,l))) ∂ν :=
  CapI4ProductTransport.product_positive_spectral_bound ν p H K hp hH hK hdom

example {Ω : Type*} [MeasurableSpace Ω] (Q : Measure Ω)
    (J : Ω → ℝ) (B : Ω → ℝ × (ℝ × ℝ)) (hJ : Measurable J) (hB : Measurable B)
    (ν : Measure ℝ) (p : ℝ × (ℝ × ℝ) → ℝ≥0∞)
    [SFinite ((volume : Measure (ℝ × (ℝ × ℝ))).withDensity p)]
    (H : ℝ × ℝ → ℝ≥0∞) (K : ℝ × (ℝ × ℝ) → ℝ≥0∞)
    (hp : Measurable p) (hH : Measurable H) (hK : Measurable K)
    (hdom : ∀ e, p e ≤ H (CapI4Polar.eigenvalues e))
    (hlaw : Measure.map (fun ω => (J ω,B ω)) Q =
      ν.prod ((volume : Measure (ℝ × (ℝ × ℝ))).withDensity p)) :
    (∫⁻ ω, if 0 < (CapI4Polar.eigenvalues (B ω)).1 then
      K (J ω,CapI4Polar.eigenvalues (B ω)) else 0 ∂Q) ≤
    ∫⁻ j, (ENNReal.ofReal Real.pi * ∫⁻ l : ℝ × ℝ in {l | 0 < l.1 ∧ l.1 < l.2},
      ENNReal.ofReal (l.2-l.1) * (H l * K (j,l))) ∂ν :=
  CapI4ProductTransport.jointLaw_positive_spectral_bound Q J B hJ hB ν p H K hp hH hK hdom hlaw

example {Ω : Type*} [MeasurableSpace Ω] (Q : Measure Ω)
    (J : Ω → ℝ) (B : Ω → ℝ × (ℝ × ℝ)) (hJ : Measurable J) (hB : Measurable B)
    (ν : Measure ℝ) (p : ℝ × (ℝ × ℝ) → ℝ≥0∞)
    [SFinite ((volume : Measure (ℝ × (ℝ × ℝ))).withDensity p)]
    (H : ℝ × ℝ → ℝ≥0∞) (K : ℝ × (ℝ × ℝ) → ℝ≥0∞)
    (hp : Measurable p) (hH : Measurable H) (hK : Measurable K)
    (hdom : ∀ e, p e ≤ H (CapI4Polar.eigenvalues e))
    (hlaw : Measure.map (fun ω => (J ω,B ω)) Q =
      ν.prod ((volume : Measure (ℝ × (ℝ × ℝ))).withDensity p))
    (W : Ω → ℝ≥0∞)
    (hW : ∀ ω, W ω ≤ if 0 < (CapI4Polar.eigenvalues (B ω)).1 then
      K (J ω,CapI4Polar.eigenvalues (B ω)) else 0) :
    (∫⁻ ω, W ω ∂Q) ≤
    ∫⁻ j, (ENNReal.ofReal Real.pi * ∫⁻ l : ℝ × ℝ in {l | 0 < l.1 ∧ l.1 < l.2},
      ENNReal.ofReal (l.2-l.1) * (H l * K (j,l))) ∂ν :=
  CapI4ProductTransport.dominated_weight_spectral_bound Q J B hJ hB ν p H K hp hH hK hdom hlaw W hW
