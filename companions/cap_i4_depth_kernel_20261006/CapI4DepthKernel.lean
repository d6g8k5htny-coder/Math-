import CapI4Independent
import Mathlib.Tactic

/-!
Explicit m=2 depth cutoff and the determinant-product envelope for Cap I4.
The source bound is needed only on positive-weight support. Actual field
independence, density, derivatives, moments, geometry and normalization are
not constructed here. Both soft factors and the hard eigenvalue remain.
-/
noncomputable section
set_option autoImplicit false
open MeasureTheory ProbabilityTheory Set
open scoped ENNReal
namespace CapI4DepthKernel

/-- The moving width depends on the residual and the largest eigenvalue. -/
def depthKernel (r K k0 : ℝ) (z : ℝ × (ℝ × ℝ)) : ℝ≥0∞ :=
  if z.2.1 ≤ (4*K^2/(3*k0))*r*(z.1+z.2.2)^2 then
    ENNReal.ofReal ((K^2*(1+K)/4)*r^2*z.2.2*(z.1+z.2.2)^3*z.2.1*
      (z.2.1+(3*K/2)*r*(z.1+z.2.2))) else 0

theorem measurable_depthKernel (r K k0 : ℝ) :
    Measurable (depthKernel r K k0) := by
  have hs : MeasurableSet {z : ℝ × (ℝ × ℝ) |
      z.2.1 ≤ (4*K^2/(3*k0))*r*(z.1+z.2.2)^2} := by
    apply measurableSet_le <;> fun_prop
  have hp : Measurable (fun z : ℝ × (ℝ × ℝ) =>
      ENNReal.ofReal ((K^2*(1+K)/4)*r^2*z.2.2*(z.1+z.2.2)^3*z.2.1*
        (z.2.1+(3*K/2)*r*(z.1+z.2.2)))) := by fun_prop
  change Measurable ({z : ℝ × (ℝ × ℝ) |
      z.2.1 ≤ (4*K^2/(3*k0))*r*(z.1+z.2.2)^2}.indicator _)
  exact hp.indicator hs

/-- Scalar consequence of P(6.2); no spectral-density or independence input. -/
theorem double_soft_majorant (r K j lam top h : ℝ) (hr : 0 ≤ r) (hr1 : r ≤ 1)
    (hK : 0 ≤ K) (hj : 0 ≤ j) (hlam : 0 ≤ lam) (htop : 0 ≤ top)
    (hh : 0 ≤ h) (hhU : h ≤ K*(j+top)) :
    (r^2*h^2/4)*lam*(lam+(3/2)*r*h)*top*(top+r*h) ≤
      (K^2*(1+K)/4)*r^2*top*(j+top)^3*lam*(lam+(3*K/2)*r*(j+top)) := by
  have hU : 0 ≤ j+top := add_nonneg hj htop
  have hKU : 0 ≤ K*(j+top) := mul_nonneg hK hU
  have hrh : r*h ≤ h := by nlinarith
  have hhard : top+r*h ≤ (1+K)*(j+top) := by nlinarith
  calc
    _ ≤ (r^2*(K*(j+top))^2/4)*lam*(lam+(3/2)*r*(K*(j+top)))*
        top*((1+K)*(j+top)) := by gcongr
    _ = _ := by ring

/-- A positive mark floor and derivative envelope enlarge the actual failure cutoff. -/
theorem depth_cutoff (r K k0 k j lam top h : ℝ) (hr : 0 ≤ r) (hK : 0 ≤ K)
    (hk0 : 0 < k0) (hk : k0 ≤ k) (hj : 0 ≤ j) (htop : 0 ≤ top)
    (hh : 0 ≤ h) (hhU : h ≤ K*(j+top))
    (hfail : lam ≤ (4/(3*k))*r*h^2) :
    lam ≤ (4*K^2/(3*k0))*r*(j+top)^2 := by
  have hkpos : 0 < k := lt_of_lt_of_le hk0 hk
  have hU : 0 ≤ j+top := add_nonneg hj htop
  have hKU : 0 ≤ K*(j+top) := mul_nonneg hK hU
  have hc : (4 : ℝ)/(3*k) ≤ 4/(3*k0) := by gcongr
  calc
    lam ≤ (4/(3*k))*r*h^2 := hfail
    _ ≤ (4/(3*k0))*r*(K*(j+top))^2 := by gcongr
    _ = _ := by ring

/-- No positive-cone hypothesis is imposed at nonpositive real weight. -/
theorem typed_depth_weight_le (r K k0 k j lam top h w : ℝ) (hr : 0 ≤ r) (hr1 : r ≤ 1)
    (hK : 0 ≤ K) (hk0 : 0 < k0) (hk : k0 ≤ k)
    (hs : 0 < w → 0 < lam ∧ lam ≤ top ∧ 0 ≤ j ∧ 0 ≤ h ∧
      h ≤ K*(j+top) ∧ w ≤ (r^2*h^2/4)*lam*(lam+(3/2)*r*h)*top*(top+r*h)) :
    ENNReal.ofReal (if lam ≤ (4/(3*k))*r*h^2 then w else 0) ≤
      if 0 < lam then depthKernel r K k0 (j,(lam,top)) else 0 := by
  by_cases hfail : lam ≤ (4/(3*k))*r*h^2
  · by_cases hwpos : 0 < w
    · rcases hs hwpos with ⟨hlam, horder, hj, hh, hhU, hw⟩
      have htop : 0 ≤ top := le_trans (le_of_lt hlam) horder
      have hcut := depth_cutoff r K k0 k j lam top h hr hK hk0 hk hj htop hh hhU hfail
      have hbound := hw.trans
        (double_soft_majorant r K j lam top h hr hr1 hK hj (le_of_lt hlam) htop hh hhU)
      simpa only [if_pos hfail, if_pos hlam, depthKernel, if_pos hcut] using
        ENNReal.ofReal_le_ofReal hbound
    · have hw : w ≤ 0 := le_of_not_gt hwpos
      simp only [if_pos hfail, ENNReal.ofReal_eq_zero.mpr hw]
      exact zero_le _
  · simp only [if_neg hfail, ENNReal.ofReal_zero]
    exact zero_le _

/-- The actual depth-truncated weight uses the explicit kernel, not an assumed final bound. -/
theorem independent_depth_bound_ae {Ω : Type*} [MeasurableSpace Ω] (Q : Measure Ω) [IsProbabilityMeasure Q]
    (J : Ω → ℝ) (B : Ω → ℝ × (ℝ × ℝ)) (hJ : Measurable J) (hB : Measurable B)
    (hI : IndepFun J B Q) (p : ℝ × (ℝ × ℝ) → ℝ≥0∞)
    (hB_law : Measure.map B Q = (volume : Measure (ℝ × (ℝ × ℝ))).withDensity p)
    (H : ℝ × ℝ → ℝ≥0∞) (hp : Measurable p) (hH : Measurable H)
    (hdom : ∀ e, p e ≤ H (CapI4Polar.eigenvalues e))
    (r K k0 k : ℝ) (hr : 0 ≤ r) (hr1 : r ≤ 1) (hK : 0 ≤ K)
    (hk0 : 0 < k0) (hk : k0 ≤ k) (h w : Ω → ℝ)
    (hdata : ∀ᵐ ω ∂Q, 0 < w ω →
      0 < (CapI4Polar.eigenvalues (B ω)).1 ∧
      (CapI4Polar.eigenvalues (B ω)).1 ≤ (CapI4Polar.eigenvalues (B ω)).2 ∧
      0 ≤ J ω ∧ 0 ≤ h ω ∧ h ω ≤ K*(J ω+(CapI4Polar.eigenvalues (B ω)).2) ∧
      w ω ≤ (r^2*(h ω)^2/4)*(CapI4Polar.eigenvalues (B ω)).1*
        ((CapI4Polar.eigenvalues (B ω)).1+(3/2)*r*h ω)*
        (CapI4Polar.eigenvalues (B ω)).2*((CapI4Polar.eigenvalues (B ω)).2+r*h ω)) :
    (∫⁻ ω, ENNReal.ofReal (if (CapI4Polar.eigenvalues (B ω)).1 ≤
      (4/(3*k))*r*(h ω)^2 then w ω else 0) ∂Q) ≤
    ∫⁻ j, (ENNReal.ofReal Real.pi * ∫⁻ l : ℝ × ℝ in {l | 0 < l.1 ∧ l.1 < l.2},
      ENNReal.ofReal (l.2-l.1)*(H l*depthKernel r K k0 (j,l))) ∂Measure.map J Q := by
  apply CapI4Independent.independent_weight_bound_ae Q J B hJ hB hI p hB_law
    H (depthKernel r K k0) hp hH (measurable_depthKernel r K k0) hdom
  filter_upwards [hdata] with ω hω
  exact typed_depth_weight_le r K k0 k (J ω)
    (CapI4Polar.eigenvalues (B ω)).1 (CapI4Polar.eigenvalues (B ω)).2
    (h ω) (w ω) hr hr1 hK hk0 hk hω

end CapI4DepthKernel
