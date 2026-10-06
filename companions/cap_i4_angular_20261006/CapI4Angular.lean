import CapI4Polar
import Mathlib.MeasureTheory.Measure.Prod

/-!
Angular integration for the isolated Cap I4 polar sub-bridge.
This evaluates only the angular factor. Entry-volume and spectral-plane
linear changes, matrix identification and the actual Gaussian law remain
separate obligations. All integrals are nonnegative extended integrals.
-/
noncomputable section
set_option autoImplicit false
open MeasureTheory Set
open scoped ENNReal Real
namespace CapI4Angular

/-- Integrate a measurable radial test over the full polar angular interval. -/
theorem angle_lintegral (g : ℝ → ℝ≥0∞) (hg : Measurable g) :
    (∫⁻ q : ℝ × ℝ in polarCoord.target, g q.1) =
      ENNReal.ofReal (2 * Real.pi) * ∫⁻ r : ℝ in Ioi 0, g r := by
  have hv : (volume : Measure ℝ) (Ioo (-Real.pi) Real.pi) =
      ENNReal.ofReal (2 * Real.pi) := by
    rw [Real.volume_Ioo]
    congr 1
    ring
  calc
    _ = ∫⁻ r : ℝ in Ioi 0, ∫⁻ θ : ℝ in Ioo (-Real.pi) Real.pi, g r := by
      change (∫⁻ q : ℝ × ℝ in Ioi (0 : ℝ) ×ˢ Ioo (-Real.pi) Real.pi,
        g q.1 ∂((volume : Measure ℝ).prod volume)) = _
      exact setLIntegral_prod (fun q : ℝ × ℝ => g q.1)
        (hg.comp measurable_fst).aemeasurable
    _ = ∫⁻ r : ℝ in Ioi 0, ENNReal.ofReal (2 * Real.pi) * g r := by
      apply lintegral_congr
      intro r
      simp [hv, mul_comm]
    _ = _ := lintegral_const_mul _ hg

/-- The source polar identity with its angle evaluated and radius retained. -/
theorem polar_spectral_radial (t : ℝ) (F : ℝ × ℝ → ℝ≥0∞)
    (hF : Measurable F) :
    (∫⁻ z : ℝ × ℝ, F (CapI4Polar.spectrum t z)) =
      ENNReal.ofReal (2 * Real.pi) *
        ∫⁻ r : ℝ in Ioi 0, ENNReal.ofReal r * F (t - r, t + r) := by
  have hg : Measurable (fun r : ℝ => ENNReal.ofReal r * F (t - r, t + r)) := by
    fun_prop
  calc
    _ = ∫⁻ q : ℝ × ℝ in polarCoord.target,
        ENNReal.ofReal q.1 * F (t - q.1, t + q.1) :=
      CapI4Polar.polar_spectral_lintegral t F
    _ = _ := angle_lintegral _ hg

/-- The input density may be anisotropic; only the upper envelope is spectral. -/
theorem density_radial_bound (t : ℝ) (p w F : ℝ × ℝ → ℝ≥0∞)
    (hw : Measurable w) (hF : Measurable F)
    (hdom : ∀ z, p z ≤ w (CapI4Polar.spectrum t z)) :
    (∫⁻ z : ℝ × ℝ, p z * F (CapI4Polar.spectrum t z)) ≤
      ENNReal.ofReal (2 * Real.pi) *
        ∫⁻ r : ℝ in Ioi 0, ENNReal.ofReal r *
          (w (t - r, t + r) * F (t - r, t + r)) := by
  have hg : Measurable (fun r : ℝ => ENNReal.ofReal r *
      (w (t - r, t + r) * F (t - r, t + r))) := by
    fun_prop
  calc
    _ ≤ ∫⁻ q : ℝ × ℝ in polarCoord.target,
        ENNReal.ofReal q.1 *
          (w (t - q.1, t + q.1) * F (t - q.1, t + q.1)) :=
      CapI4Polar.density_polar_bound t p w F hdom
    _ = _ := angle_lintegral _ hg

end CapI4Angular
