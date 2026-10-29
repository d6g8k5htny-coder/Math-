import SourceWeightedCurvatureBound
open I4SmoothCarrier I4SourceSmoothPalm I4SourcePinCurvatureBounds I4SourceWeightedCurvature
open I4ScalarProductCurvature MeasureTheory Set

example : ∃ C δ : ℝ, 0 ≤ C ∧ 0 < δ ∧ δ ≤ 1 ∧ ∀ r : ℝ, 0 < r → r < δ →
    (sourceSmoothWeightedLaw (by norm_num : (1 : ℝ) ≠ 0) r 3).real
      (sourceRegularityBad 1 r (1/2) ∪ sourceCurvatureOneSided 1 r 2) ≤ C*r^3 := by
  obtain ⟨C,δ,hC,hδ,hδ1,hbound⟩ := sourceWeightedCurvature_bound
    (by norm_num : (1 : ℝ) ≠ 0) 3 2 (1/2) (by norm_num) (by norm_num)
  exact ⟨C,δ,hC,hδ,hδ1,fun r hr hrδ => (hbound r hr hrδ).2⟩

example : sourceRegularityBad 1 1 0 = (Set.univ : Set (SmoothSample 2 1)) := by
  ext ω
  change (0 < (1 : ℝ)*sourceGammaRadius 1 ω^5) ↔ True
  have hR : 0 < sourceGammaRadius 1 ω := zero_lt_one.trans_le (one_le_sourceGammaRadius 1 ω)
  simp [pow_pos hR]

example : (sourceSmoothLaw (by norm_num : (1 : ℝ) ≠ 0) 1 0).real (sourceRegularityBad 1 1 0) = 1 := by
  have hE : sourceRegularityBad 1 1 0 = (Set.univ : Set (SmoothSample 2 1)) := by
    ext ω
    change (0 < (1 : ℝ)*sourceGammaRadius 1 ω^5) ↔ True
    have hR : 0 < sourceGammaRadius 1 ω := zero_lt_one.trans_le (one_le_sourceGammaRadius 1 ω)
    simp [pow_pos hR]
  rw [hE]
  simp

example : ((101:ℝ)/100 ≤ (1*(1+1*1))*1) ∧
    |(1:ℝ)/100| ≤ 1*(1*(1+1*1))^5*(1/100)*1^5 := by
  have h := regular_bounds (A := (1:ℝ)) (K := 1) (eps := 1) (S := 1)
    (R := 101/100) (q := 1/100) (r := 1/100)
    (by norm_num) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by norm_num) (by norm_num) (by norm_num) (by norm_num)
  exact ⟨h.1,h.2.1⟩
