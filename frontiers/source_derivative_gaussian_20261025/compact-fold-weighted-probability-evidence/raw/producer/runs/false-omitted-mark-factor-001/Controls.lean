import SourceCompactFoldWeightedProbability

noncomputable section
open Set MeasureTheory CategoryTheory Limits ResearchFormalCoreR1
open I4SmoothCarrier I4SourceSmoothPalm I4SourceConditionalMajorant
open I4SourcePinCurvatureBounds I4SourceCompactTargetMoments I4SourceWeightedCurvature
open I4SourceAdaptiveFoldEstimates I4SourceConfluentPins
open SourceActualFoldTorus SourceActualFoldH0 TorusFiltration I4Torus
open SourceFoldWeightedProbability SourceCompactFoldWeightedProbability
set_option autoImplicit false

namespace CompactFoldWeightedControls

theorem negativePeriod : (-1:ℝ) ≠ 0 := by norm_num

theorem literal_varying_law {L : ℝ} (hL : L ≠ 0) (r b k : ℝ) :
    sourceCompactFoldWeightedLaw hL r b k =
      prwMeasure (sourceGapLaw hL r b k) (sourceSmoothWeight L r) := rfl

theorem literal_varying_good (r k : ℝ) :
    sourceCompactFoldGood (-1) (1/12) r k =
      {sample | r * sourceT (1/12) sample ^ 5 ≤ 1/100 ∧
        1024 * sourceT (1/12) sample ^ 5 ≤ sourceKappa r k sample} := rfl

theorem full_scale_and_mark_constants :
    max (1:ℝ) (1/(6*(1/12))) = 2 ∧ sourceScale (1/12) = 16 ∧
      (16:ℝ)^5 = 1048576 ∧ (8:ℝ)^5 = 32768 ∧
      sourceCutoffEps (1/12) = 1/104857600 ∧
      sourceCompactCutoffA (1/12) 2 = 6*2*1024*16^5 ∧
      sourceCompactCutoffA (1/12) 2 = 12884901888 := by
  norm_num [sourceScale,sourceCutoffEps,sourceCompactCutoffA]

theorem actual_scale_and_curvature (r : ℝ) (sample : SmoothSample 2 (-1)) :
    sourceT (1/12) sample = 16*sourceGammaRadius (-1) sample ∧
      sourceKappa r 2 sample = -sourceQ (-1) sample/(12*r) := by
  constructor
  · rw [sourceT_eq_scale]; norm_num [sourceScale]
  · unfold sourceKappa; congr 1; ring

theorem actual_good_event_measurable (r k : ℝ) :
    MeasurableSet (sourceCompactFoldGood (-1) (1/12) r k) :=
  sourceCompactFoldGood_measurable negativePeriod (1/12) r k

theorem actual_uniform_obstruction (r k : ℝ) (hr : 0 < r)
    (hk : (1:ℝ)/12 ≤ k) (hk' : k ≤ 2) :
    (sourceCompactFoldGood (-1) (1/12) r k)ᶜ ⊆
      sourceRegularityBad (-1) r (1/104857600) ∪
        sourceCurvatureOneSided (-1) r 12884901888 := by
  convert sourceCompactFoldGood_compl_subset (-1) (1/12) 2 r k
    (by norm_num) hk hk' hr using 1
  norm_num [sourceCutoffEps,sourceCompactCutoffA,sourceScale]

/-- The first cutoff holds and the second fails at a finite scalar witness. -/
theorem second_cutoff_failure_witness :
    ((1:ℝ)/1000000000)*(16*1)^5 ≤ 1/100 ∧
      ¬ (1024*(16*1)^5 ≤ -(-5:ℝ)/(6*2*((1:ℝ)/1000000000))) ∧
      ¬ ((1:ℝ)/(100*16^5) < ((1:ℝ)/1000000000)*1^5 ∨
        -(1024*(16:ℝ)^5)*((1:ℝ)/1000000000)*1^5 ≤ -5) := by norm_num

theorem full_coefficient_detects_failure :
    (1:ℝ)/(100*16^5) < ((1:ℝ)/1000000000)*1^5 ∨
      -(6*2*1024*(16:ℝ)^5)*((1:ℝ)/1000000000)*1^5 ≤ -5 := by
  exact varying_cutoff_failure_inclusion 16 (1/1000000000) 1 (-5) 2 2
    (by norm_num) (by norm_num) (by norm_num) (by norm_num) (by norm_num)
    (not_and.mpr fun _ => second_cutoff_failure_witness.2.1)

/-- The curvature obstruction is closed, so it also contains equality cases. -/
theorem closed_boundary_good_witness :
    (((1:ℝ)/1000000000)*(16*1)^5 ≤ 1/100 ∧
      1024*(16*1)^5 ≤ -(-(6*2*1024*(16:ℝ)^5)*((1:ℝ)/1000000000))/
        (6*2*((1:ℝ)/1000000000))) ∧
      -(6*2*1024*(16:ℝ)^5)*((1:ℝ)/1000000000)*1^5 ≤
        -(6*2*1024*(16:ℝ)^5)*((1:ℝ)/1000000000) := by norm_num

theorem fifth_over_second_is_cubic (N c r : ℝ) (hr : 0 < r) :
    (N*r^5)/(c*r^2) = (N/c)*r^3 := by field_simp [hr.ne']

theorem actual_same_law_ac (r b k : ℝ) :
    sourceCompactFoldWeightedLaw negativePeriod r b k ≪ sourceGapLaw negativePeriod r b k :=
  sourceCompactFoldWeightedLaw_absolutelyContinuous negativePeriod r b k

theorem same_law_weighted_ae (r b k : ℝ) (F : SmoothSample 2 (-1) → Prop)
    (h : ∀ᵐ sample ∂sourceGapLaw negativePeriod r b k,
      sample ∈ sourceCompactFoldGood (-1) (1/12) r k → F sample) :
    ∀ᵐ sample ∂sourceCompactFoldWeightedLaw negativePeriod r b k,
      sample ∈ sourceCompactFoldGood (-1) (1/12) r k → F sample :=
  (actual_same_law_ac r b k).ae_le h

/-- One derived pair handles both nondefault heights and positive gap marks. -/
theorem uniform_two_actual_marks :
    ∃ C δ : ℝ, 0 ≤ C ∧ 0 < δ ∧ δ ≤ 1 ∧ ∀ r : ℝ, 0 < r → r < δ →
      (IsProbabilityMeasure (sourceCompactFoldWeightedLaw negativePeriod r (-3) 1) ∧
        (sourceCompactFoldWeightedLaw negativePeriod r (-3) 1).real
          (sourceCompactFoldGood (-1) (1/12) r 1)ᶜ ≤ C*r^3) ∧
      (IsProbabilityMeasure (sourceCompactFoldWeightedLaw negativePeriod r 3 2) ∧
        (sourceCompactFoldWeightedLaw negativePeriod r 3 2).real
          (sourceCompactFoldGood (-1) (1/12) r 2)ᶜ ≤ C*r^3) := by
  obtain ⟨C,δ,hC,hδ,hδ1,h⟩ := sourceCompactFoldWeightedProbability_bound negativePeriod
    3 (1/12) 2 (by norm_num) (by norm_num) (by norm_num)
  exact ⟨C,δ,hC,hδ,hδ1,fun r hr hrδ =>
    ⟨h r hr hrδ (-3) 1 (by norm_num) (by norm_num) (by norm_num),
      h r hr hrδ 3 2 (by norm_num) (by norm_num) (by norm_num)⟩⟩

/-- The same C,delta precede all bounded marks and every coefficient field. -/
theorem uniform_actual_probability_h0 :
    ∃ C δ : ℝ, 0 ≤ C ∧ 0 < δ ∧ δ ≤ 1 ∧
      ∀ r : ℝ, 0 < r → r < δ → ∀ b k : ℝ, |b| ≤ 3 → (1:ℝ)/12 ≤ k → k ≤ 2 →
        IsProbabilityMeasure (sourceCompactFoldWeightedLaw negativePeriod r b k) ∧
        (sourceCompactFoldWeightedLaw negativePeriod r b k).real
          (sourceCompactFoldGood (-1) (1/12) r k)ᶜ ≤ C*r^3 ∧
        ∀ (K : Type) [Field K], ∀ᵐ sample ∂sourceCompactFoldWeightedLaw negativePeriod r b k,
          sample ∈ sourceCompactFoldGood (-1) (1/12) r k →
            ∃ D : ℝ ⥤ ModuleCat K,
              Nonempty (superlevel_h0Filtration (actualTorusField negativePeriod sample)
                (ModuleCat.of K K) ≅ elderInterval K b (b-k*r^3) ⊞ D) ∧
              strictClearanceSet (actualTorusField negativePeriod sample)
                (torusProjection 2 (-1) (endpointM r)) = Iio (b-k*r^3) ∧
              strictClearanceDeath (actualTorusField negativePeriod sample)
                (torusProjection 2 (-1) (endpointM r)) = b-k*r^3 :=
  sourceCompactFoldWeightedProbability_h0 negativePeriod 3 (1/12) 2
    (by norm_num) (by norm_num) (by norm_num)

end CompactFoldWeightedControls
