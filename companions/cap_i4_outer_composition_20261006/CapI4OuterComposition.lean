import CapI4InnerIntegration
import CapI4GaussianEnvelope
import Mathlib.Tactic

noncomputable section
set_option autoImplicit false
open MeasureTheory Set
open scoped ENNReal Real
namespace CapI4OuterComposition

/-- Compose the actual moving inner kernel with the finite Gaussian product envelope. -/
theorem gaussian_depth_outer_le (ν : Measure ℝ) [IsFiniteMeasure ν]
    (C0 c r K k0 : ℝ) (hC0 : 0 ≤ C0) (hc : 0 < c)
    (hr : 0 ≤ r) (hK : 0 ≤ K) (hk0 : 0 < k0)
    (hsupp : ∀ᵐ j ∂ν, 1 ≤ j) (h9 : Integrable (fun j : ℝ => |j|^9) ν) :
    ENNReal.ofReal Real.pi * (∫⁻ j, (∫⁻ T : ℝ in Ioi 0,
      ∫⁻ x : ℝ in Ioo 0 T, ENNReal.ofReal (T-x) *
        (ENNReal.ofReal (C0*Real.exp (-c*(x^2+T^2))) *
          CapI4DepthKernel.depthKernel r K k0 (j,(x,T)))) ∂ν) ≤
    ENNReal.ofReal (256*Real.pi*C0*(K^2*(1+K)/4)*
      (((4*K^2/(3*k0))^3/3)+((3*K/2)*(4*K^2/(3*k0))^2/2))*r^5*
      ((∫ j : ℝ, |j|^9 ∂ν)*(∫ T : ℝ in Ioi 0, T^2*Real.exp (-c*T^2)) +
        ν.real univ*(∫ T : ℝ in Ioi 0, |T|^11*Real.exp (-c*T^2)))) := by
  let d : ℝ := C0*(K^2*(1+K)/4)*
    (((4*K^2/(3*k0))^3/3)+((3*K/2)*(4*K^2/(3*k0))^2/2))*r^5
  let F : ℝ × ℝ → ℝ := fun z =>
    (|z.1|+|z.2|)^9*z.2^2*Real.exp (-c*z.2^2)
  let B : ℝ := (∫ j : ℝ, |j|^9 ∂ν)*(∫ T : ℝ in Ioi 0, T^2*Real.exp (-c*T^2)) +
    ν.real univ*(∫ T : ℝ in Ioi 0, |T|^11*Real.exp (-c*T^2))
  have hd : 0 ≤ d := by dsimp [d]; positivity
  have hF : Measurable (fun z : ℝ × ℝ => ENNReal.ofReal (F z)) := by
    dsimp [F]
    fun_prop
  have hdF : Measurable (fun z : ℝ × ℝ => ENNReal.ofReal (d*F z)) := by
    dsimp [F]
    fun_prop
  have hmajor :
      (∫⁻ j, (∫⁻ T : ℝ in Ioi 0,
        ∫⁻ x : ℝ in Ioo 0 T, ENNReal.ofReal (T-x) *
          (ENNReal.ofReal (C0*Real.exp (-c*(x^2+T^2))) *
            CapI4DepthKernel.depthKernel r K k0 (j,(x,T)))) ∂ν) ≤
      ∫⁻ j, (∫⁻ T : ℝ in Ioi 0, ENNReal.ofReal (d*F (j,T))) ∂ν := by
    apply lintegral_mono_ae
    filter_upwards [hsupp] with j hj
    apply lintegral_mono_ae
    filter_upwards [ae_restrict_mem measurableSet_Ioi] with T hT
    calc
      _ ≤ _ := CapI4InnerIntegration.gaussian_depth_slice_ninth_le
        C0 c r K k0 j T hC0 hc.le hr hK hk0 hj hT.le
      _ = ENNReal.ofReal (d*F (j,T)) := by
        congr 1
        dsimp [d, F]
        rw [abs_of_nonneg (le_trans (by norm_num : (0 : ℝ) ≤ 1) hj),
          abs_of_nonneg hT.le]
        ring
  have hprod :
      (∫⁻ j, (∫⁻ T : ℝ in Ioi 0, ENNReal.ofReal (d*F (j,T))) ∂ν) =
      ∫⁻ z : ℝ × ℝ, ENNReal.ofReal (d*F z) ∂ν.prod (volume.restrict (Ioi 0)) :=
    (lintegral_prod _ hdF.aemeasurable).symm
  have hfactor :
      (∫⁻ z : ℝ × ℝ, ENNReal.ofReal (d*F z) ∂ν.prod (volume.restrict (Ioi 0))) =
      ENNReal.ofReal d * ∫⁻ z : ℝ × ℝ, ENNReal.ofReal (F z)
        ∂ν.prod (volume.restrict (Ioi 0)) := by
    simp_rw [ENNReal.ofReal_mul hd]
    exact lintegral_const_mul _ hF
  have henv :
      (∫⁻ z : ℝ × ℝ, ENNReal.ofReal (F z) ∂ν.prod (volume.restrict (Ioi 0))) ≤
      ENNReal.ofReal (256*B) := by
    simpa only [F, B] using CapI4GaussianEnvelope.mixed_envelope_lintegral_le ν c hc h9
  calc
    _ ≤ ENNReal.ofReal Real.pi *
        (∫⁻ j, (∫⁻ T : ℝ in Ioi 0, ENNReal.ofReal (d*F (j,T))) ∂ν) := by
      gcongr
    _ = ENNReal.ofReal Real.pi *
        (∫⁻ z : ℝ × ℝ, ENNReal.ofReal (d*F z) ∂ν.prod (volume.restrict (Ioi 0))) := by
      rw [hprod]
    _ = ENNReal.ofReal Real.pi * (ENNReal.ofReal d *
        ∫⁻ z : ℝ × ℝ, ENNReal.ofReal (F z) ∂ν.prod (volume.restrict (Ioi 0))) := by
      rw [hfactor]
    _ ≤ ENNReal.ofReal Real.pi * (ENNReal.ofReal d * ENNReal.ofReal (256*B)) := by
      gcongr
    _ = _ := by
      rw [← mul_assoc, ← ENNReal.ofReal_mul Real.pi_pos.le,
        ← ENNReal.ofReal_mul (mul_nonneg Real.pi_pos.le hd)]
      congr 1
      dsimp [d, B]
      ring

/-- The displayed iterated mass is genuinely finite under these same hypotheses. -/
theorem gaussian_depth_outer_lt_top (ν : Measure ℝ) [IsFiniteMeasure ν]
    (C0 c r K k0 : ℝ) (hC0 : 0 ≤ C0) (hc : 0 < c)
    (hr : 0 ≤ r) (hK : 0 ≤ K) (hk0 : 0 < k0)
    (hsupp : ∀ᵐ j ∂ν, 1 ≤ j) (h9 : Integrable (fun j : ℝ => |j|^9) ν) :
    ENNReal.ofReal Real.pi * (∫⁻ j, (∫⁻ T : ℝ in Ioi 0,
      ∫⁻ x : ℝ in Ioo 0 T, ENNReal.ofReal (T-x) *
        (ENNReal.ofReal (C0*Real.exp (-c*(x^2+T^2))) *
          CapI4DepthKernel.depthKernel r K k0 (j,(x,T)))) ∂ν) < ∞ := by
  exact (gaussian_depth_outer_le ν C0 c r K k0 hC0 hc hr hK hk0 hsupp h9).trans_lt ENNReal.ofReal_lt_top

end CapI4OuterComposition
