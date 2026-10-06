import Mathlib.Analysis.SpecialFunctions.Gaussian.GaussianIntegral
import Mathlib.MeasureTheory.Integral.Prod
import Mathlib.Tactic

/-!
Finite outer-envelope integration for Cap I4's existing ninth-moment estimate.
No field density, independence, geometric event or normalizer is instantiated.
-/
noncomputable section
set_option autoImplicit false
open MeasureTheory Set
open scoped ENNReal
namespace CapI4GaussianEnvelope

/-- Gaussian decay supplies every natural absolute moment, not an assumed finite integral. -/
theorem gaussian_abs_moment_integrable (c : ℝ) (hc : 0 < c) (n : ℕ) :
    Integrable (fun t : ℝ => |t|^n * Real.exp (-c*t^2)) := by
  have hn : (-1 : ℝ) < (n : ℝ) :=
    lt_of_lt_of_le (by norm_num : (-1 : ℝ) < 0) (Nat.cast_nonneg n)
  have h : Integrable (fun t : ℝ => t^n * Real.exp (-c*t^2)) := by
    simpa only [Real.rpow_natCast] using (integrable_rpow_mul_exp_neg_mul_sq hc hn)
  simpa only [Real.norm_eq_abs, abs_mul, abs_pow, abs_of_pos (Real.exp_pos _)] using h.norm

/-- The existing factor 256 is retained; equality occurs at x=y. -/
theorem ninth_power_le (x y : ℝ) (hx : 0 ≤ x) (hy : 0 ≤ y) :
    (x+y)^9 ≤ 256*(x^9+y^9) := by
  calc
    _ ≤ (x+y)^9+(x-y)^2*(255*x^7+501*x^6*y+711*x^5*y^2+837*x^4*y^3+
        837*x^3*y^4+711*x^2*y^5+501*x*y^6+255*y^7) := by
      exact le_add_of_nonneg_right (by positivity)
    _ = _ := by ring

/-- The mixed residual/eigenvalue factor is bounded, never factorized as an equality. -/
theorem mixed_envelope_pointwise_le (c j t : ℝ) :
    (|j|+|t|)^9*t^2*Real.exp (-c*t^2) ≤
      256*(|j|^9*(t^2*Real.exp (-c*t^2)) + 1*(|t|^11*Real.exp (-c*t^2))) := by
  have h11 : |t|^11 = |t|^9*t^2 := by
    calc
      _ = |t|^9*|t|^2 := by ring
      _ = _ := by rw [sq_abs]
  calc
    _ ≤ 256*(|j|^9+|t|^9)*t^2*Real.exp (-c*t^2) :=
      mul_le_mul_of_nonneg_right
        (mul_le_mul_of_nonneg_right (ninth_power_le _ _ (abs_nonneg _) (abs_nonneg _))
          (sq_nonneg t)) (Real.exp_pos _).le
    _ = _ := by rw [h11]; ring

/-- Actual integrability on the whole positive half-line, including the region near zero. -/
theorem mixed_envelope_integrable (ν : Measure ℝ) [IsFiniteMeasure ν]
    (c : ℝ) (hc : 0 < c) (h9 : Integrable (fun j : ℝ => |j|^9) ν) :
    Integrable (fun z : ℝ × ℝ => (|z.1|+|z.2|)^9*z.2^2*Real.exp (-c*z.2^2))
      (ν.prod (volume.restrict (Ioi 0))) := by
  have h2 : Integrable (fun t : ℝ => t^2*Real.exp (-c*t^2))
      (volume.restrict (Ioi 0)) := by
    simpa only [IntegrableOn, sq_abs] using (gaussian_abs_moment_integrable c hc 2).integrableOn
  have h11 : Integrable (fun t : ℝ => |t|^11*Real.exp (-c*t^2))
      (volume.restrict (Ioi 0)) := (gaussian_abs_moment_integrable c hc 11).integrableOn
  have hconst : Integrable (fun _ : ℝ => (1 : ℝ)) ν := integrable_const 1
  have hmajor := ((h9.mul_prod h2).add (hconst.mul_prod h11)).const_mul (256 : ℝ)
  refine hmajor.mono' (by fun_prop) ?_
  filter_upwards [] with z
  rw [Real.norm_eq_abs, abs_of_nonneg (by positivity)]
  exact mixed_envelope_pointwise_le c z.1 z.2

/-- Keep the residual measure's actual mass; neither finiteness nor normalization is inferred. -/
theorem mixed_envelope_integral_le (ν : Measure ℝ) [IsFiniteMeasure ν]
    (c : ℝ) (hc : 0 < c) (h9 : Integrable (fun j : ℝ => |j|^9) ν) :
    (∫ z : ℝ × ℝ, (|z.1|+|z.2|)^9*z.2^2*Real.exp (-c*z.2^2)
      ∂ν.prod (volume.restrict (Ioi 0))) ≤
      256*((∫ j : ℝ, |j|^9 ∂ν)*(∫ t : ℝ in Ioi 0, t^2*Real.exp (-c*t^2)) +
        ν.real univ*(∫ t : ℝ in Ioi 0, |t|^11*Real.exp (-c*t^2))) := by
  have h2 : Integrable (fun t : ℝ => t^2*Real.exp (-c*t^2))
      (volume.restrict (Ioi 0)) := by
    simpa only [IntegrableOn, sq_abs] using (gaussian_abs_moment_integrable c hc 2).integrableOn
  have h11 : Integrable (fun t : ℝ => |t|^11*Real.exp (-c*t^2))
      (volume.restrict (Ioi 0)) := (gaussian_abs_moment_integrable c hc 11).integrableOn
  have hconst : Integrable (fun _ : ℝ => (1 : ℝ)) ν := integrable_const 1
  have hmajor := ((h9.mul_prod h2).add (hconst.mul_prod h11)).const_mul (256 : ℝ)
  calc
    _ ≤ ∫ z : ℝ × ℝ, 256*(|z.1|^9*(z.2^2*Real.exp (-c*z.2^2))+
        1*(|z.2|^11*Real.exp (-c*z.2^2))) ∂ν.prod (volume.restrict (Ioi 0)) :=
      integral_mono (mixed_envelope_integrable ν c hc h9) hmajor
        (fun z => mixed_envelope_pointwise_le c z.1 z.2)
    _ = _ := by
      rw [integral_const_mul, integral_add (h9.mul_prod h2) (hconst.mul_prod h11),
        integral_prod_mul (fun j : ℝ => |j|^9) (fun t : ℝ => t^2*Real.exp (-c*t^2)),
        integral_prod_mul (fun _ : ℝ => (1 : ℝ)) (fun t : ℝ => |t|^11*Real.exp (-c*t^2))]
      simp only [integral_const, smul_eq_mul, mul_one]

/-- The finite Bochner calculation legitimately controls the nonnegative measure integral. -/
theorem mixed_envelope_lintegral_le (ν : Measure ℝ) [IsFiniteMeasure ν]
    (c : ℝ) (hc : 0 < c) (h9 : Integrable (fun j : ℝ => |j|^9) ν) :
    (∫⁻ z : ℝ × ℝ, ENNReal.ofReal ((|z.1|+|z.2|)^9*z.2^2*Real.exp (-c*z.2^2))
      ∂ν.prod (volume.restrict (Ioi 0))) ≤
      ENNReal.ofReal (256*((∫ j : ℝ, |j|^9 ∂ν)*(∫ t : ℝ in Ioi 0, t^2*Real.exp (-c*t^2)) +
        ν.real univ*(∫ t : ℝ in Ioi 0, |t|^11*Real.exp (-c*t^2)))) := by
  have hi := mixed_envelope_integrable ν c hc h9
  have hn : 0 ≤ᵐ[ν.prod (volume.restrict (Ioi 0))]
      (fun z : ℝ × ℝ => (|z.1|+|z.2|)^9*z.2^2*Real.exp (-c*z.2^2)) :=
    Filter.Eventually.of_forall (fun _ => by positivity)
  rw [← ofReal_integral_eq_lintegral_ofReal hi hn]
  exact ENNReal.ofReal_le_ofReal (mixed_envelope_integral_le ν c hc h9)

end CapI4GaussianEnvelope
