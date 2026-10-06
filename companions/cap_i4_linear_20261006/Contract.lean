import CapI4Linear
open MeasureTheory Set
open scoped ENNReal
example : Measure.map CapI4Linear.tracePair (volume : Measure (ℝ × ℝ)) =
    (2 : ℝ≥0∞) • volume := CapI4Linear.map_tracePair
example : Measure.map CapI4Linear.spectralPair (volume : Measure (ℝ × ℝ)) =
    (1/2 : ℝ≥0∞) • volume := CapI4Linear.map_spectralPair
example (G : ℝ × ℝ → ℝ≥0∞) (hG : Measurable G) :
    (∫⁻ q : ℝ × ℝ in {q | 0 < q.2 ∧ q.2 < q.1},
      ENNReal.ofReal q.2 * G (q.1-q.2, q.1+q.2)) =
      (1/4 : ℝ≥0∞) * ∫⁻ e : ℝ × ℝ in {e | 0 < e.1 ∧ e.1 < e.2},
        ENNReal.ofReal (e.2-e.1) * G e := CapI4Linear.weighted_positive_chamber_change G hG
example : CapI4Linear.tracePair (CapI4Linear.spectralPair (2,1)) = (2,-1) := by
  exact CapI4Linear.tracePair_spectralPair (2,1)
