import CapI4EntryVolume
open MeasureTheory
open scoped ENNReal
example : Measurable CapI4Polar.traceCoordinates :=
  CapI4EntryVolume.measurable_traceCoordinates
example (F : ℝ × (ℝ × ℝ) → ℝ≥0∞) (hF : Measurable F) :
    (∫⁻ e : ℝ × (ℝ × ℝ), F e) =
      ∫⁻ q : ℝ × ℝ, ∫⁻ b : ℝ, F (q.1, (b, q.2)) :=
  CapI4EntryVolume.entry_reorder_lintegral F hF
example (F : ℝ × (ℝ × ℝ) → ℝ≥0∞) (hF : Measurable F) :
    (∫⁻ e : ℝ × (ℝ × ℝ), F (CapI4Polar.traceCoordinates e)) =
      (2 : ℝ≥0∞) * ∫⁻ q : ℝ × (ℝ × ℝ), F q :=
  CapI4EntryVolume.traceCoordinates_lintegral F hF
