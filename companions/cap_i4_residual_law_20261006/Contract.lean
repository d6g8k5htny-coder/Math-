import CapI4ResidualLaw
open MeasureTheory

example {Ω : Type*} [MeasurableSpace Ω] (Q : Measure Ω)
    (J : Ω → ℝ) (hJ : Measurable J) (hs : ∀ᵐ ω ∂Q, 1 ≤ J ω) :
    ∀ᵐ j ∂Q.map J, 1 ≤ j :=
  CapI4ResidualLaw.support_transfer Q J hJ hs

example {Ω : Type*} [MeasurableSpace Ω] (Q : Measure Ω)
    (J : Ω → ℝ) (hJ : Measurable J) :
    Integrable (fun j : ℝ => |j|^9) (Q.map J) ↔
      Integrable (fun ω => |J ω|^9) Q :=
  CapI4ResidualLaw.ninth_integrable_iff Q J hJ

example {Ω : Type*} [MeasurableSpace Ω] (Q : Measure Ω)
    (J : Ω → ℝ) (hJ : Measurable J)
    (h9 : Integrable (fun ω => |J ω|^9) Q) :
    (∫ j : ℝ, |j|^9 ∂Q.map J) = ∫ ω, |J ω|^9 ∂Q :=
  CapI4ResidualLaw.ninth_integral_eq Q J hJ h9

example {Ω : Type*} [MeasurableSpace Ω] (Q : Measure Ω)
    (J : Ω → ℝ) (hJ : Measurable J) (hs : ∀ᵐ ω ∂Q, 1 ≤ J ω)
    (h9 : Integrable (fun ω => |J ω|^9) Q) (M : ℝ)
    (hM : (∫ ω, |J ω|^9 ∂Q) ≤ M) :
    (∀ᵐ j ∂Q.map J, 1 ≤ j) ∧
      Integrable (fun j : ℝ => |j|^9) (Q.map J) ∧
      (∫ j : ℝ, |j|^9 ∂Q.map J) ≤ M :=
  CapI4ResidualLaw.outer_inputs Q J hJ hs h9 M hM
