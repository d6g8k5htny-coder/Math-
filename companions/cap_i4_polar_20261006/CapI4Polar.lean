import Mathlib.Analysis.SpecialFunctions.PolarCoord
import Mathlib.Tactic

/-!
Source-bound d=3 polar sub-interface for Cap I4.
This module proves coordinate identities and the NONNEGATIVE polar integral
step. It does not identify entry Lebesgue volume with trace coordinates,
perform the last eigenvalue-plane linear change, or instantiate a field law.
-/
noncomputable section
set_option autoImplicit false
open MeasureTheory Set
open scoped ENNReal Real
namespace CapI4Polar

def radius (z : ℝ × ℝ) : ℝ := Real.sqrt (z.1 ^ 2 + z.2 ^ 2)

def spectrum (t : ℝ) (z : ℝ × ℝ) : ℝ × ℝ :=
  (t - radius z, t + radius z)

/-- Entry convention: e = (a,(b,d)) represents [[a,b],[b,d]]. -/
def traceCoordinates (e : ℝ × (ℝ × ℝ)) : ℝ × (ℝ × ℝ) :=
  ((e.1 + e.2.2) / 2, ((e.1 - e.2.2) / 2, e.2.1))

def eigenvalues (e : ℝ × (ℝ × ℝ)) : ℝ × ℝ :=
  spectrum (traceCoordinates e).1 (traceCoordinates e).2

theorem radius_nonneg (z : ℝ × ℝ) : 0 ≤ radius z :=
  Real.sqrt_nonneg _

theorem radius_sq (z : ℝ × ℝ) : radius z ^ 2 = z.1 ^ 2 + z.2 ^ 2 := by
  exact Real.sq_sqrt (add_nonneg (sq_nonneg z.1) (sq_nonneg z.2))

theorem continuous_radius : Continuous radius := by
  unfold radius
  fun_prop

theorem spectrum_ordered (t : ℝ) (z : ℝ × ℝ) :
    (spectrum t z).1 ≤ (spectrum t z).2 := by
  dsimp [spectrum]
  linarith [radius_nonneg z]

theorem continuous_spectrum (t : ℝ) : Continuous (spectrum t) := by
  unfold spectrum
  exact (continuous_const.sub continuous_radius).prodMk
    (continuous_const.add continuous_radius)

theorem spectrum_sum (t : ℝ) (z : ℝ × ℝ) :
    (spectrum t z).1 + (spectrum t z).2 = 2 * t := by
  dsimp [spectrum]
  ring

theorem spectrum_product (t : ℝ) (z : ℝ × ℝ) :
    (spectrum t z).1 * (spectrum t z).2 = t ^ 2 - z.1 ^ 2 - z.2 ^ 2 := by
  dsimp [spectrum]
  nlinarith [radius_sq z]

theorem spectrum_sq_sum (t : ℝ) (z : ℝ × ℝ) :
    (spectrum t z).1 ^ 2 + (spectrum t z).2 ^ 2 =
      2 * (t ^ 2 + z.1 ^ 2 + z.2 ^ 2) := by
  dsimp [spectrum]
  nlinarith [radius_sq z]

theorem continuous_eigenvalues : Continuous eigenvalues := by
  unfold eigenvalues traceCoordinates spectrum radius
  fun_prop

theorem eigenvalues_sum (e : ℝ × (ℝ × ℝ)) :
    (eigenvalues e).1 + (eigenvalues e).2 = e.1 + e.2.2 := by
  unfold eigenvalues
  rw [spectrum_sum]
  dsimp [traceCoordinates]
  ring

theorem eigenvalues_product (e : ℝ × (ℝ × ℝ)) :
    (eigenvalues e).1 * (eigenvalues e).2 = e.1 * e.2.2 - e.2.1 ^ 2 := by
  unfold eigenvalues
  rw [spectrum_product]
  dsimp [traceCoordinates]
  ring

theorem positive_trace_measurable (t : ℝ) :
    MeasurableSet {z : ℝ × ℝ | 0 < (spectrum t z).1} := by
  exact (isOpen_lt continuous_const
    (continuous_fst.comp (continuous_spectrum t))).measurableSet

theorem radius_polar (p : ℝ × ℝ) (hr : 0 ≤ p.1) :
    radius (polarCoord.symm p) = p.1 := by
  simp only [radius, polarCoord_symm_apply]
  have h : (p.1 * Real.cos p.2) ^ 2 + (p.1 * Real.sin p.2) ^ 2 = p.1 ^ 2 := by
    calc
      _ = p.1 ^ 2 * (Real.cos p.2 ^ 2 + Real.sin p.2 ^ 2) := by ring
      _ = p.1 ^ 2 := by rw [Real.cos_sq_add_sin_sq]; ring
  rw [h, Real.sqrt_sq hr]

theorem spectrum_polar (t : ℝ) (p : ℝ × ℝ) (hr : 0 ≤ p.1) :
    spectrum t (polarCoord.symm p) = (t - p.1, t + p.1) := by
  simp only [spectrum, radius_polar p hr]

/-- Exact nonnegative change of variables; no finite-integrability hypothesis. -/
theorem polar_spectral_lintegral (t : ℝ) (F : ℝ × ℝ → ℝ≥0∞) :
    (∫⁻ z : ℝ × ℝ, F (spectrum t z)) =
      ∫⁻ p : ℝ × ℝ in polarCoord.target,
        ENNReal.ofReal p.1 * F (t - p.1, t + p.1) := by
  calc
    _ = ∫⁻ p : ℝ × ℝ in polarCoord.target,
        ENNReal.ofReal p.1 * F (spectrum t (polarCoord.symm p)) := by
      simpa only [smul_eq_mul] using
        (lintegral_comp_polarCoord_symm (fun z => F (spectrum t z))).symm
    _ = _ := by
      apply setLIntegral_congr_fun polarCoord.open_target.measurableSet
      intro p hp
      change ENNReal.ofReal p.1 * F (spectrum t (polarCoord.symm p)) =
        ENNReal.ofReal p.1 * F (t - p.1, t + p.1)
      rw [spectrum_polar t p (le_of_lt hp.1)]

theorem polar_positive_lintegral (t : ℝ) (F : ℝ × ℝ → ℝ≥0∞) :
    (∫⁻ z : ℝ × ℝ, if 0 < (spectrum t z).1 then F (spectrum t z) else 0) =
      ∫⁻ p : ℝ × ℝ in polarCoord.target,
        ENNReal.ofReal p.1 * (if 0 < t - p.1 then F (t - p.1, t + p.1) else 0) := by
  exact polar_spectral_lintegral t (fun e => if 0 < e.1 then F e else 0)

/-- The actual density p may be anisotropic: only its upper envelope is spectral. -/
theorem density_polar_bound (t : ℝ) (p w F : ℝ × ℝ → ℝ≥0∞)
    (hdom : ∀ z, p z ≤ w (spectrum t z)) :
    (∫⁻ z : ℝ × ℝ, p z * F (spectrum t z)) ≤
      ∫⁻ q : ℝ × ℝ in polarCoord.target,
        ENNReal.ofReal q.1 * (w (t - q.1, t + q.1) * F (t - q.1, t + q.1)) := by
  calc
    _ ≤ ∫⁻ z : ℝ × ℝ, w (spectrum t z) * F (spectrum t z) :=
      lintegral_mono (fun z => by gcongr <;> exact hdom z)
    _ = _ := polar_spectral_lintegral t (fun e => w e * F e)

theorem density_positive_polar_bound (t : ℝ) (p w F : ℝ × ℝ → ℝ≥0∞)
    (hdom : ∀ z, p z ≤ w (spectrum t z)) :
    (∫⁻ z : ℝ × ℝ, p z * (if 0 < (spectrum t z).1 then F (spectrum t z) else 0)) ≤
      ∫⁻ q : ℝ × ℝ in polarCoord.target,
        ENNReal.ofReal q.1 * (w (t - q.1, t + q.1) *
          (if 0 < t - q.1 then F (t - q.1, t + q.1) else 0)) := by
  exact density_polar_bound t p w (fun e => if 0 < e.1 then F e else 0) hdom

/-- Integration over the trace keeps the pointwise-density hypothesis explicit. -/
theorem integrated_density_polar_bound
    (p : ℝ → ℝ × ℝ → ℝ≥0∞) (w F : ℝ × ℝ → ℝ≥0∞)
    (hdom : ∀ t z, p t z ≤ w (spectrum t z)) :
    (∫⁻ t : ℝ, ∫⁻ z : ℝ × ℝ, p t z * F (spectrum t z)) ≤
      ∫⁻ t : ℝ, ∫⁻ q : ℝ × ℝ in polarCoord.target,
        ENNReal.ofReal q.1 * (w (t - q.1, t + q.1) * F (t - q.1, t + q.1)) := by
  exact lintegral_mono (fun t => density_polar_bound t (p t) w F (hdom t))

end CapI4Polar
