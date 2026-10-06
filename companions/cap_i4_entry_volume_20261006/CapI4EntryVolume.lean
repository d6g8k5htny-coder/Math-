import CapI4Polar
import CapI4Linear
import Mathlib.MeasureTheory.Measure.Prod
import Mathlib.Tactic

/-!
The actual three-entry Lebesgue lift for the source association (a,(b,d)).
All tests are measurable and all integrals are nonnegative extended integrals.
This is not yet the angular/chamber assembly or a concrete Gaussian model.
-/
noncomputable section
set_option autoImplicit false
open MeasureTheory Set
open scoped ENNReal Real
namespace CapI4EntryVolume

theorem measurable_traceCoordinates : Measurable CapI4Polar.traceCoordinates := by
  unfold CapI4Polar.traceCoordinates
  fun_prop

/-- Reorder a,d,b without changing product Lebesgue volume. -/
theorem entry_reorder_lintegral (F : ℝ × (ℝ × ℝ) → ℝ≥0∞)
    (hF : Measurable F) :
    (∫⁻ e : ℝ × (ℝ × ℝ), F e) =
      ∫⁻ q : ℝ × ℝ, ∫⁻ b : ℝ, F (q.1, (b, q.2)) := by
  calc
    _ = ∫⁻ a : ℝ, ∫⁻ z : ℝ × ℝ, F (a, z) :=
      lintegral_prod F hF.aemeasurable
    _ = ∫⁻ a : ℝ, ∫⁻ d : ℝ, ∫⁻ b : ℝ, F (a, (b, d)) := by
      apply lintegral_congr
      intro a
      exact lintegral_prod_symm (fun z : ℝ × ℝ => F (a, z)) (by fun_prop)
    _ = _ := by
      exact (lintegral_prod
        (fun q : ℝ × ℝ => ∫⁻ b : ℝ, F (q.1, (b, q.2))) (by fun_prop)).symm

/-- Entry volume becomes twice trace/traceless volume, including the b coordinate. -/
theorem traceCoordinates_lintegral (F : ℝ × (ℝ × ℝ) → ℝ≥0∞)
    (hF : Measurable F) :
    (∫⁻ e : ℝ × (ℝ × ℝ), F (CapI4Polar.traceCoordinates e)) =
      (2 : ℝ≥0∞) * ∫⁻ q : ℝ × (ℝ × ℝ), F q := by
  let H : ℝ × ℝ → ℝ≥0∞ := fun q => ∫⁻ b : ℝ, F (q.1, (q.2, b))
  have hH : Measurable H := by
    dsimp [H]
    fun_prop
  have hcomp : Measurable (fun e => F (CapI4Polar.traceCoordinates e)) :=
    hF.comp measurable_traceCoordinates
  calc
    _ = ∫⁻ q : ℝ × ℝ, H (CapI4Linear.tracePair q) := by
      rw [entry_reorder_lintegral _ hcomp]
      apply lintegral_congr
      intro q
      simp only [H, CapI4Linear.tracePair_apply, CapI4Polar.traceCoordinates]
    _ = (2 : ℝ≥0∞) * ∫⁻ q : ℝ × ℝ, H q :=
      CapI4Linear.lintegral_tracePair H hH
    _ = _ := by
      congr 1
      calc
        _ = ∫⁻ t : ℝ, ∫⁻ x : ℝ, ∫⁻ b : ℝ, F (t, (x, b)) :=
          lintegral_prod H hH.aemeasurable
        _ = ∫⁻ t : ℝ, ∫⁻ z : ℝ × ℝ, F (t, z) := by
          apply lintegral_congr
          intro t
          exact (lintegral_prod (fun z : ℝ × ℝ => F (t, z)) (by fun_prop)).symm
        _ = _ := (lintegral_prod F hF.aemeasurable).symm

end CapI4EntryVolume
