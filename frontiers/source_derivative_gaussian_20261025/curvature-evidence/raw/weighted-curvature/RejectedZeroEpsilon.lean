import SourceWeightedCurvatureBound
open I4SmoothCarrier I4SourceSmoothPalm I4SourcePinCurvatureBounds I4SourceWeightedCurvature
open MeasureTheory Set
example : (sourceSmoothLaw (by norm_num : (1 : ℝ) ≠ 0) 1 0).real
    (sourceRegularityBad 1 1 0) ≤ ((1 : ℝ)/0^6)*1^6 := by
  have hE : sourceRegularityBad 1 1 0 = (Set.univ : Set (SmoothSample 2 1)) := by
    ext ω
    change (0 < (1 : ℝ)*sourceGammaRadius 1 ω^5) ↔ True
    have hR : 0 < sourceGammaRadius 1 ω := zero_lt_one.trans_le (one_le_sourceGammaRadius 1 ω)
    simp [pow_pos hR]
  rw [hE]
  norm_num
