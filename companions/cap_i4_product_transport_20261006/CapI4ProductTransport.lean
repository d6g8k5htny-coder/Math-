import CapI4SpectralAssembly
import Mathlib.MeasureTheory.Measure.WithDensity
import Mathlib.MeasureTheory.Integral.Lebesgue.Map
import Mathlib.Tactic

/-!
Density and original-law residual-product transport for the Cap I4 spectral bridge.
The joint law and weight envelope are explicit caller obligations. No Gaussian
construction, moment evaluation, geometric event or normalizer is instantiated.
-/
noncomputable section
set_option autoImplicit false
open MeasureTheory Set
open scoped ENNReal Real
namespace CapI4ProductTransport

/-- Measurability of the joint residual/positive-spectrum test. -/
theorem positive_test_measurable (K : ℝ × (ℝ × ℝ) → ℝ≥0∞) (hK : Measurable K) :
    Measurable (fun z : ℝ × (ℝ × (ℝ × ℝ)) =>
      if 0 < (CapI4Polar.eigenvalues z.2).1 then K (z.1, CapI4Polar.eigenvalues z.2) else 0) := by
  have he : Measurable (fun z : ℝ × (ℝ × (ℝ × ℝ)) =>
      CapI4Polar.eigenvalues z.2) :=
    CapI4Polar.continuous_eigenvalues.measurable.comp measurable_snd
  have hs : MeasurableSet {z : ℝ × (ℝ × (ℝ × ℝ)) |
      0 < (CapI4Polar.eigenvalues z.2).1} :=
    measurableSet_lt measurable_const (measurable_fst.comp he)
  change Measurable ({z : ℝ × (ℝ × (ℝ × ℝ)) |
    0 < (CapI4Polar.eigenvalues z.2).1}.indicator
      (fun z => K (z.1, CapI4Polar.eigenvalues z.2)))
  exact (hK.comp (measurable_fst.prodMk he)).indicator hs

/-- Transfer to a measure with an explicit density; the envelope is only an upper bound. -/
theorem withDensity_positive_spectral_bound (p : ℝ × (ℝ × ℝ) → ℝ≥0∞) (H G : ℝ × ℝ → ℝ≥0∞)
    (hp : Measurable p) (hH : Measurable H) (hG : Measurable G)
    (hdom : ∀ e, p e ≤ H (CapI4Polar.eigenvalues e)) :
    (∫⁻ e : ℝ × (ℝ × ℝ),
      if 0 < (CapI4Polar.eigenvalues e).1 then G (CapI4Polar.eigenvalues e) else 0
      ∂(volume : Measure (ℝ × (ℝ × ℝ))).withDensity p) ≤
    ENNReal.ofReal Real.pi * ∫⁻ l : ℝ × ℝ in {l | 0 < l.1 ∧ l.1 < l.2},
      ENNReal.ofReal (l.2-l.1) * (H l * G l) := by
  have he := CapI4Polar.continuous_eigenvalues.measurable
  have hs : MeasurableSet {e : ℝ × (ℝ × ℝ) |
      0 < (CapI4Polar.eigenvalues e).1} :=
    measurableSet_lt measurable_const (measurable_fst.comp he)
  have hphi : Measurable (fun e : ℝ × (ℝ × ℝ) =>
      if 0 < (CapI4Polar.eigenvalues e).1 then G (CapI4Polar.eigenvalues e) else 0) := by
    change Measurable ({e : ℝ × (ℝ × ℝ) |
      0 < (CapI4Polar.eigenvalues e).1}.indicator (fun e => G (CapI4Polar.eigenvalues e)))
    exact (hG.comp he).indicator hs
  calc
    _ = ∫⁻ e : ℝ × (ℝ × ℝ), p e *
        (if 0 < (CapI4Polar.eigenvalues e).1 then G (CapI4Polar.eigenvalues e) else 0) := by
      simpa only [Pi.mul_apply] using
        (lintegral_withDensity_eq_lintegral_mul
          (volume : Measure (ℝ × (ℝ × ℝ))) hp hphi)
    _ ≤ _ := CapI4SpectralAssembly.density_positive_spectral_bound p H G hH hG hdom

/-- Integrate each spectral slice without factoring a nonseparable kernel. -/
theorem residual_iterated_positive_spectral_bound (ν : Measure ℝ) (p : ℝ × (ℝ × ℝ) → ℝ≥0∞)
    (H : ℝ × ℝ → ℝ≥0∞) (K : ℝ × (ℝ × ℝ) → ℝ≥0∞)
    (hp : Measurable p) (hH : Measurable H)
    (hK : ∀ j, Measurable (fun l => K (j,l)))
    (hdom : ∀ e, p e ≤ H (CapI4Polar.eigenvalues e)) :
    (∫⁻ j, ∫⁻ e : ℝ × (ℝ × ℝ),
      if 0 < (CapI4Polar.eigenvalues e).1 then K (j,CapI4Polar.eigenvalues e) else 0
      ∂(volume : Measure (ℝ × (ℝ × ℝ))).withDensity p ∂ν) ≤
    ∫⁻ j, (ENNReal.ofReal Real.pi * ∫⁻ l : ℝ × ℝ in {l | 0 < l.1 ∧ l.1 < l.2},
      ENNReal.ofReal (l.2-l.1) * (H l * K (j,l))) ∂ν := by
  exact lintegral_mono (fun j =>
    withDensity_positive_spectral_bound p H (fun l => K (j,l)) hp hH (hK j) hdom)

/-- Tonelli under an actual product law; s-finiteness is explicit. -/
theorem product_positive_spectral_bound (ν : Measure ℝ) (p : ℝ × (ℝ × ℝ) → ℝ≥0∞)
    [SFinite ((volume : Measure (ℝ × (ℝ × ℝ))).withDensity p)]
    (H : ℝ × ℝ → ℝ≥0∞) (K : ℝ × (ℝ × ℝ) → ℝ≥0∞)
    (hp : Measurable p) (hH : Measurable H) (hK : Measurable K)
    (hdom : ∀ e, p e ≤ H (CapI4Polar.eigenvalues e)) :
    (∫⁻ z : ℝ × (ℝ × (ℝ × ℝ)),
      if 0 < (CapI4Polar.eigenvalues z.2).1 then K (z.1,CapI4Polar.eigenvalues z.2) else 0
      ∂ν.prod ((volume : Measure (ℝ × (ℝ × ℝ))).withDensity p)) ≤
    ∫⁻ j, (ENNReal.ofReal Real.pi * ∫⁻ l : ℝ × ℝ in {l | 0 < l.1 ∧ l.1 < l.2},
      ENNReal.ofReal (l.2-l.1) * (H l * K (j,l))) ∂ν := by
  calc
    _ = ∫⁻ j, ∫⁻ e : ℝ × (ℝ × ℝ),
        if 0 < (CapI4Polar.eigenvalues e).1 then K (j,CapI4Polar.eigenvalues e) else 0
        ∂(volume : Measure (ℝ × (ℝ × ℝ))).withDensity p ∂ν :=
      lintegral_prod _ (positive_test_measurable K hK).aemeasurable
    _ ≤ _ := residual_iterated_positive_spectral_bound ν p H K hp hH
      (fun j => hK.comp (measurable_const.prodMk measurable_id)) hdom

/-- Transport a measurable pair with the stated JOINT law, not merely given marginals. -/
theorem jointLaw_positive_spectral_bound {Ω : Type*} [MeasurableSpace Ω] (Q : Measure Ω)
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
      ENNReal.ofReal (l.2-l.1) * (H l * K (j,l))) ∂ν := by
  let F : ℝ × (ℝ × (ℝ × ℝ)) → ℝ≥0∞ := fun z =>
    if 0 < (CapI4Polar.eigenvalues z.2).1 then K (z.1,CapI4Polar.eigenvalues z.2) else 0
  have hF : Measurable F := positive_test_measurable K hK
  calc
    _ = ∫⁻ z, F z ∂Measure.map (fun ω => (J ω,B ω)) Q :=
      (lintegral_map hF (hJ.prodMk hB)).symm
    _ = ∫⁻ z, F z ∂ν.prod ((volume : Measure (ℝ × (ℝ × ℝ))).withDensity p) := by
      rw [hlaw]
    _ ≤ _ := product_positive_spectral_bound ν p H K hp hH hK hdom

/-- An arbitrary weight bounded by the spectral/residual kernel; no Cauchy–Schwarz loss. -/
theorem dominated_weight_spectral_bound {Ω : Type*} [MeasurableSpace Ω] (Q : Measure Ω)
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
      ENNReal.ofReal (l.2-l.1) * (H l * K (j,l))) ∂ν := by
  exact (lintegral_mono hW).trans
    (jointLaw_positive_spectral_bound Q J B hJ hB ν p H K hp hH hK hdom hlaw)

end CapI4ProductTransport
