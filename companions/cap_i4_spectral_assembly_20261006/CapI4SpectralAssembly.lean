import CapI4EntryVolume
import CapI4Angular
import Mathlib.Tactic

/-!
Composition of the exact entry-volume, angular and linear chamber interfaces.
Only product Lebesgue measure and measurable nonnegative tests occur here.
No Gaussian law, regression, moment bound or weighted selection is instantiated.
-/
noncomputable section
set_option autoImplicit false
open MeasureTheory Set
open scoped ENNReal Real
namespace CapI4SpectralAssembly

/-- Tonelli retains the positive cone and the complete small-radius interval. -/
theorem radial_positive_tonelli (G : ℝ × ℝ → ℝ≥0∞) (hG : Measurable G) :
    (∫⁻ t : ℝ, ∫⁻ r : ℝ in Ioi 0, ENNReal.ofReal r *
      (if 0 < t-r then G (t-r,t+r) else 0)) =
      ∫⁻ q : ℝ × ℝ in {q | 0 < q.2 ∧ q.2 < q.1},
        ENNReal.ofReal q.2 * G (q.1-q.2,q.1+q.2) := by
  have hs : MeasurableSet {q : ℝ × ℝ | 0 < q.2 ∧ q.2 < q.1} :=
    (isOpen_lt continuous_const continuous_snd).measurableSet.inter
      (isOpen_lt continuous_snd continuous_fst).measurableSet
  have hW : Measurable (fun q : ℝ × ℝ => ENNReal.ofReal q.2 *
      G (q.1-q.2,q.1+q.2)) := by fun_prop
  symm
  rw [← lintegral_indicator hs]
  calc
    _ = ∫⁻ t : ℝ, ∫⁻ r : ℝ,
        {q : ℝ × ℝ | 0 < q.2 ∧ q.2 < q.1}.indicator
          (fun q => ENNReal.ofReal q.2 * G (q.1-q.2,q.1+q.2)) (t,r) :=
      lintegral_prod _ (hW.indicator hs).aemeasurable
    _ = _ := by
      apply lintegral_congr
      intro t
      rw [← lintegral_indicator measurableSet_Ioi]
      apply lintegral_congr
      intro r
      by_cases hr : 0 < r <;> by_cases ht : r < t <;>
        simp [Set.indicator, hr, ht, sub_pos, mul_ite]

/-- The three-entry convention is exactly e=(a,(b,d)). -/
theorem entry_spectral_radial (G : ℝ × ℝ → ℝ≥0∞) (hG : Measurable G) :
    (∫⁻ e : ℝ × (ℝ × ℝ), G (CapI4Polar.eigenvalues e)) =
      (2 : ℝ≥0∞) * ENNReal.ofReal (2*Real.pi) *
        ∫⁻ t : ℝ, ∫⁻ r : ℝ in Ioi 0,
          ENNReal.ofReal r * G (t-r,t+r) := by
  have hPhi : Measurable (fun q : ℝ × (ℝ × ℝ) =>
      G (CapI4Polar.spectrum q.1 q.2)) := by
    unfold CapI4Polar.spectrum CapI4Polar.radius
    fun_prop
  calc
    _ = (2 : ℝ≥0∞) * ∫⁻ q : ℝ × (ℝ × ℝ),
        G (CapI4Polar.spectrum q.1 q.2) := by
      simpa only [CapI4Polar.eigenvalues] using
        CapI4EntryVolume.traceCoordinates_lintegral _ hPhi
    _ = (2 : ℝ≥0∞) * ∫⁻ t : ℝ, ∫⁻ z : ℝ × ℝ,
        G (CapI4Polar.spectrum t z) := by
      congr 1
      exact lintegral_prod _ hPhi.aemeasurable
    _ = (2 : ℝ≥0∞) * ∫⁻ t : ℝ, ENNReal.ofReal (2*Real.pi) *
        ∫⁻ r : ℝ in Ioi 0, ENNReal.ofReal r * G (t-r,t+r) := by
      congr 1
      apply lintegral_congr
      intro t
      exact CapI4Angular.polar_spectral_radial t G hG
    _ = _ := by
      rw [lintegral_const_mul _ (by fun_prop), ← mul_assoc]

/-- Exact ordered positive spectral integration in entry Lebesgue volume. -/
theorem entry_positive_spectral_lintegral (G : ℝ × ℝ → ℝ≥0∞)
    (hG : Measurable G) :
    (∫⁻ e : ℝ × (ℝ × ℝ),
      if 0 < (CapI4Polar.eigenvalues e).1 then G (CapI4Polar.eigenvalues e) else 0) =
      ENNReal.ofReal Real.pi *
        ∫⁻ l : ℝ × ℝ in {l | 0 < l.1 ∧ l.1 < l.2},
          ENNReal.ofReal (l.2-l.1) * G l := by
  have hp : MeasurableSet {l : ℝ × ℝ | 0 < l.1} :=
    (isOpen_lt continuous_const continuous_fst).measurableSet
  have hpos : Measurable (fun l : ℝ × ℝ => if 0 < l.1 then G l else 0) := by
    change Measurable ({l : ℝ × ℝ | 0 < l.1}.indicator G)
    exact hG.indicator hp
  have hc : (2 : ℝ≥0∞) * ENNReal.ofReal (2*Real.pi) * (1/4 : ℝ≥0∞) =
      ENNReal.ofReal Real.pi := by
    have htwo : (2 : ℝ≥0∞) = ENNReal.ofReal (2 : ℝ) := by norm_num
    have hquarter : (1/4 : ℝ≥0∞) = ENNReal.ofReal (1/4 : ℝ) := by
      rw [ENNReal.ofReal_div_of_pos (by norm_num : (0 : ℝ) < 4)]
      norm_num
    rw [htwo, hquarter,
      ← ENNReal.ofReal_mul (by norm_num : (0 : ℝ) ≤ 2),
      ← ENNReal.ofReal_mul (by positivity : (0 : ℝ) ≤ 2*(2*Real.pi))]
    congr 1
    ring
  calc
    _ = (2 : ℝ≥0∞) * ENNReal.ofReal (2*Real.pi) *
        ∫⁻ t : ℝ, ∫⁻ r : ℝ in Ioi 0,
          ENNReal.ofReal r * (if 0 < t-r then G (t-r,t+r) else 0) :=
      entry_spectral_radial _ hpos
    _ = (2 : ℝ≥0∞) * ENNReal.ofReal (2*Real.pi) *
        ((1/4 : ℝ≥0∞) * ∫⁻ l : ℝ × ℝ in {l | 0 < l.1 ∧ l.1 < l.2},
          ENNReal.ofReal (l.2-l.1) * G l) := by
      rw [radial_positive_tonelli G hG,
        CapI4Linear.weighted_positive_chamber_change G hG]
    _ = _ := by rw [← mul_assoc, hc]

/-- An arbitrary anisotropic input is bounded, never equated to the envelope. -/
theorem density_positive_spectral_bound
    (p : ℝ × (ℝ × ℝ) → ℝ≥0∞) (H G : ℝ × ℝ → ℝ≥0∞)
    (hH : Measurable H) (hG : Measurable G)
    (hdom : ∀ e, p e ≤ H (CapI4Polar.eigenvalues e)) :
    (∫⁻ e : ℝ × (ℝ × ℝ), p e *
      (if 0 < (CapI4Polar.eigenvalues e).1 then G (CapI4Polar.eigenvalues e) else 0)) ≤
      ENNReal.ofReal Real.pi *
        ∫⁻ l : ℝ × ℝ in {l | 0 < l.1 ∧ l.1 < l.2},
          ENNReal.ofReal (l.2-l.1) * (H l * G l) := by
  calc
    _ ≤ ∫⁻ e : ℝ × (ℝ × ℝ), H (CapI4Polar.eigenvalues e) *
        (if 0 < (CapI4Polar.eigenvalues e).1 then G (CapI4Polar.eigenvalues e) else 0) :=
      lintegral_mono (fun e => by gcongr; exact hdom e)
    _ = ∫⁻ e : ℝ × (ℝ × ℝ),
        if 0 < (CapI4Polar.eigenvalues e).1 then
          H (CapI4Polar.eigenvalues e) * G (CapI4Polar.eigenvalues e) else 0 := by
      apply lintegral_congr
      intro e
      split_ifs <;> simp
    _ = _ := entry_positive_spectral_lintegral _ (hH.mul hG)

end CapI4SpectralAssembly
