import CapI4DepthKernel
import CapI4ClippedIntegral
import Mathlib.Tactic

/-!
Inner integration of the actual R16 kernel, consuming the exact R17 primitive.
The signed eigenvalue gap is never extended past the positive chamber.
Outer moments, field realization, and normalization remain separate.
-/
noncomputable section
set_option autoImplicit false
open MeasureTheory Set
open scoped ENNReal
namespace CapI4InnerIntegration

/-- The cutoff includes equality and clips the interval before any estimate. -/
theorem cutoff_gap_lintegral_eq (T L b : ℝ) :
    (∫⁻ x : ℝ in Ioc 0 T,
      if x ≤ L then ENNReal.ofReal (x*(x+b)*(T-x)) else 0) =
    ∫⁻ x : ℝ in Ioc 0 (min T L), ENNReal.ofReal (x*(x+b)*(T-x)) := by
  rw [← lintegral_indicator measurableSet_Ioc,
    ← lintegral_indicator measurableSet_Ioc]
  apply lintegral_congr
  intro x
  by_cases hx : 0 < x <;> by_cases ht : x ≤ T <;> by_cases hl : x ≤ L <;>
    simp [Set.indicator, hx, ht, hl]

/-- Use the finite clipped primitive; no zero-totalized divergent real integral. -/
theorem cutoff_gap_lintegral_le (T L b : ℝ) (hT : 0 ≤ T) (hL : 0 ≤ L) (hb : 0 ≤ b) :
    (∫⁻ x : ℝ in Ioc 0 T,
      if x ≤ L then ENNReal.ofReal (x*(x+b)*(T-x)) else 0) ≤
    ENNReal.ofReal (T*(L^3/3+b*L^2/2)) := by
  rw [cutoff_gap_lintegral_eq,
    CapI4ClippedIntegral.clipped_lintegral_eq T L b hT hL hb]
  apply ENNReal.ofReal_le_ofReal
  simpa only [CapI4ClippedIntegral.gap_integral_exact] using
    CapI4ClippedIntegral.clipped_integral_le T L b hT hL hb

/-- Actual depthKernel, both soft factors, and the hard-eigenvalue square. -/
theorem depth_slice_le (r K k0 j T : ℝ) (hr : 0 ≤ r) (hK : 0 ≤ K)
    (hk0 : 0 < k0) (hj : 0 ≤ j) (hT : 0 ≤ T) :
    (∫⁻ x : ℝ in Ioo 0 T, ENNReal.ofReal (T-x) *
      CapI4DepthKernel.depthKernel r K k0 (j,(x,T))) ≤
    ENNReal.ofReal ((K^2*(1+K)/4)*r^5*T^2*
      (((4*K^2/(3*k0))^3/3)*(j+T)^9+
       ((3*K/2)*(4*K^2/(3*k0))^2/2)*(j+T)^8)) := by
  let A := K^2*(1+K)/4
  let D := 4*K^2/(3*k0)
  let E := 3*K/2
  let U := j+T
  let P := A*r^2*T*U^3
  have hA : 0 ≤ A := by dsimp [A]; positivity
  have hD : 0 ≤ D := by dsimp [D]; positivity
  have hE : 0 ≤ E := by dsimp [E]; positivity
  have hU : 0 ≤ U := add_nonneg hj hT
  have hP : 0 ≤ P := by dsimp [P]; positivity
  let F : ℝ → ℝ≥0∞ := fun x =>
    if x ≤ D*r*U^2 then ENNReal.ofReal (x*(x+E*r*U)*(T-x)) else 0
  have hF : Measurable F := by
    change Measurable ((Iic (D*r*U^2)).indicator
      (fun x : ℝ => ENNReal.ofReal (x*(x+E*r*U)*(T-x))))
    exact (by fun_prop : Measurable
      (fun x : ℝ => ENNReal.ofReal (x*(x+E*r*U)*(T-x)))).indicator measurableSet_Iic
  have hfactor (x : ℝ) (hx : x ∈ Ioo 0 T) :
      ENNReal.ofReal (T-x)*CapI4DepthKernel.depthKernel r K k0 (j,(x,T)) =
        ENNReal.ofReal P * F x := by
    change ENNReal.ofReal (T-x)*
      (if x ≤ D*r*U^2 then ENNReal.ofReal (P*x*(x+E*r*U)) else 0) =
      ENNReal.ofReal P *
        (if x ≤ D*r*U^2 then ENNReal.ofReal (x*(x+E*r*U)*(T-x)) else 0)
    by_cases hcut : x ≤ D*r*U^2
    · simp only [ite_eq_left hcut]
      rw [← ENNReal.ofReal_mul (sub_nonneg.mpr hx.2.le), ← ENNReal.ofReal_mul hP]
      congr 1
      ring
    · simp only [ite_eq_right hcut, mul_zero]
  have hset : (∫⁻ x : ℝ in Ioo 0 T, F x) ≤ ∫⁻ x : ℝ in Ioc 0 T, F x :=
    lintegral_mono_set (fun _ hx => ⟨hx.1, hx.2.le⟩)
  have hcutbound := cutoff_gap_lintegral_le T (D*r*U^2) (E*r*U)
    hT (by positivity) (by positivity)
  change _ ≤ ENNReal.ofReal (A*r^5*T^2*((D^3/3)*U^9+(E*D^2/2)*U^8))
  calc
    _ = ∫⁻ x : ℝ in Ioo 0 T, ENNReal.ofReal P * F x :=
      setLIntegral_congr_fun measurableSet_Ioo hfactor
    _ = ENNReal.ofReal P * ∫⁻ x : ℝ in Ioo 0 T, F x := lintegral_const_mul _ hF
    _ ≤ ENNReal.ofReal P * ∫⁻ x : ℝ in Ioc 0 T, F x := by gcongr
    _ ≤ ENNReal.ofReal P * ENNReal.ofReal (T*((D*r*U^2)^3/3+(E*r*U)*(D*r*U^2)^2/2)) := by
      gcongr
    _ = _ := by
      rw [← ENNReal.ofReal_mul hP]
      congr 1
      dsimp [P]
      ring

/-- Drop only the nonpositive soft Gaussian exponent on the original chamber. -/
theorem gaussian_depth_slice_le (C0 c r K k0 j T : ℝ) (hC0 : 0 ≤ C0) (hc : 0 ≤ c)
    (hr : 0 ≤ r) (hK : 0 ≤ K) (hk0 : 0 < k0) (hj : 0 ≤ j) (hT : 0 ≤ T) :
    (∫⁻ x : ℝ in Ioo 0 T, ENNReal.ofReal (T-x) *
      (ENNReal.ofReal (C0*Real.exp (-c*(x^2+T^2))) *
       CapI4DepthKernel.depthKernel r K k0 (j,(x,T)))) ≤
    ENNReal.ofReal (C0*Real.exp (-c*T^2)*(K^2*(1+K)/4)*r^5*T^2*
      (((4*K^2/(3*k0))^3/3)*(j+T)^9+
       ((3*K/2)*(4*K^2/(3*k0))^2/2)*(j+T)^8)) := by
  have hdrop (x : ℝ) : ENNReal.ofReal (C0*Real.exp (-c*(x^2+T^2))) ≤
      ENNReal.ofReal (C0*Real.exp (-c*T^2)) := by
    apply ENNReal.ofReal_le_ofReal
    apply mul_le_mul_of_nonneg_left _ hC0
    apply Real.exp_le_exp.mpr
    nlinarith [mul_nonneg hc (sq_nonneg x)]
  have hF : Measurable (fun x : ℝ => ENNReal.ofReal (T-x)*
      CapI4DepthKernel.depthKernel r K k0 (j,(x,T))) := by
    apply Measurable.mul
    · fun_prop
    · exact (CapI4DepthKernel.measurable_depthKernel r K k0).comp (by fun_prop)
  have hs := depth_slice_le r K k0 j T hr hK hk0 hj hT
  calc
    _ ≤ ∫⁻ x : ℝ in Ioo 0 T, ENNReal.ofReal (C0*Real.exp (-c*T^2)) *
        (ENNReal.ofReal (T-x)*CapI4DepthKernel.depthKernel r K k0 (j,(x,T))) := by
      apply lintegral_mono
      intro x
      calc
        _ ≤ ENNReal.ofReal (T-x)*(ENNReal.ofReal (C0*Real.exp (-c*T^2))*
            CapI4DepthKernel.depthKernel r K k0 (j,(x,T))) := by gcongr
        _ = _ := by ac_rfl
    _ = ENNReal.ofReal (C0*Real.exp (-c*T^2)) *
        ∫⁻ x : ℝ in Ioo 0 T, ENNReal.ofReal (T-x)*
          CapI4DepthKernel.depthKernel r K k0 (j,(x,T)) := lintegral_const_mul _ hF
    _ ≤ ENNReal.ofReal (C0*Real.exp (-c*T^2)) *
        ENNReal.ofReal ((K^2*(1+K)/4)*r^5*T^2*
          (((4*K^2/(3*k0))^3/3)*(j+T)^9+
           ((3*K/2)*(4*K^2/(3*k0))^2/2)*(j+T)^8)) := by gcongr
    _ = _ := by
      rw [← ENNReal.ofReal_mul (mul_nonneg hC0 (Real.exp_pos _).le)]
      congr 1
      ring

/-- The ninth-only shortcut has its genuine unit residual lower bound. -/
theorem gaussian_depth_slice_ninth_le (C0 c r K k0 j T : ℝ) (hC0 : 0 ≤ C0) (hc : 0 ≤ c)
    (hr : 0 ≤ r) (hK : 0 ≤ K) (hk0 : 0 < k0) (hj : 1 ≤ j) (hT : 0 ≤ T) :
    (∫⁻ x : ℝ in Ioo 0 T, ENNReal.ofReal (T-x) *
      (ENNReal.ofReal (C0*Real.exp (-c*(x^2+T^2))) *
       CapI4DepthKernel.depthKernel r K k0 (j,(x,T)))) ≤
    ENNReal.ofReal (C0*Real.exp (-c*T^2)*(K^2*(1+K)/4)*r^5*T^2*
      (((4*K^2/(3*k0))^3/3)+((3*K/2)*(4*K^2/(3*k0))^2/2))*(j+T)^9) := by
  have hj0 : 0 ≤ j := le_trans zero_le_one hj
  have hU : 0 ≤ j+T := add_nonneg hj0 hT
  have hU1 : 1 ≤ j+T := by linarith
  have hpow : (j+T)^8 ≤ (j+T)^9 := by
    calc
      _ = (j+T)^8*1 := by ring
      _ ≤ (j+T)^8*(j+T) := by gcongr
      _ = _ := by ring
  have hpoly : ((4*K^2/(3*k0))^3/3)*(j+T)^9+
        ((3*K/2)*(4*K^2/(3*k0))^2/2)*(j+T)^8 ≤
      (((4*K^2/(3*k0))^3/3)+((3*K/2)*(4*K^2/(3*k0))^2/2))*(j+T)^9 := by
    calc
      _ ≤ ((4*K^2/(3*k0))^3/3)*(j+T)^9+
          ((3*K/2)*(4*K^2/(3*k0))^2/2)*(j+T)^9 := by gcongr
      _ = _ := by ring
  refine (gaussian_depth_slice_le C0 c r K k0 j T hC0 hc hr hK hk0 hj0 hT).trans ?_
  apply ENNReal.ofReal_le_ofReal
  calc
    _ ≤ C0*Real.exp (-c*T^2)*(K^2*(1+K)/4)*r^5*T^2*
        ((((4*K^2/(3*k0))^3/3)+((3*K/2)*(4*K^2/(3*k0))^2/2))*(j+T)^9) :=
      mul_le_mul_of_nonneg_left hpoly (by positivity)
    _ = _ := by ring

end CapI4InnerIntegration
