import SourceFoldWeightedProbability

noncomputable section
open Set MeasureTheory CategoryTheory Limits ResearchFormalCoreR1
open I4SmoothCarrier I4SourceSmoothPalm I4SourceConditionalMajorant
open I4SourcePinCurvatureBounds I4SourceCompactTargetMoments
open I4SourceAdaptiveFoldEstimates I4SourceConfluentPins
open SourceActualFoldTorus SourceActualFoldH0 TorusFiltration I4Torus
open SourceFoldWeightedProbability
set_option autoImplicit false

namespace FoldWeightedControls

theorem negativePeriod : (-1:ℝ) ≠ 0 := by norm_num

theorem literal_good_event (r : ℝ) :
    sourceFoldGood (-1) (1/12) r =
      {sample | r * sourceT (1/12) sample ^ 5 ≤ 1/100 ∧
        1024 * sourceT (1/12) sample ^ 5 ≤ sourceKappa r (1/6) sample} := rfl

theorem literal_normalized_law (r : ℝ) :
    sourceFoldWeightedLaw negativePeriod r 3 =
      prwMeasure (sourceGapLaw negativePeriod r 3 (1/6)) (sourceSmoothWeight (-1) r) := rfl

theorem old_weighted_law_identity (r : ℝ) :
    sourceFoldWeightedLaw negativePeriod r 3 = sourceSmoothWeightedLaw negativePeriod r 3 :=
  sourceFoldWeightedLaw_eq negativePeriod r 3

theorem full_scale_constants :
    max (1:ℝ) (1/(6*(1/12))) = 2 ∧ sourceScale (1/12) = 16 ∧
      (16:ℝ)^5 = 1048576 ∧ (8:ℝ)^5 = 32768 ∧
      sourceCutoffEps (1/12) = 1/104857600 ∧
      sourceCutoffA (1/12) = 1073741824 ∧
      0 < sourceCutoffEps (1/12) ∧ 0 ≤ sourceCutoffA (1/12) := by
  norm_num [sourceScale, sourceCutoffEps, sourceCutoffA]

theorem actual_scale (sample : SmoothSample 2 (-1)) :
    sourceT (1/12) sample = 16*sourceGammaRadius (-1) sample := by
  rw [sourceT_eq_scale]
  norm_num [sourceScale]

theorem actual_curvature_sign (r : ℝ) (sample : SmoothSample 2 (-1)) :
    sourceKappa r (1/6) sample = -sourceQ (-1) sample / r :=
  sourceKappa_one_sixth r sample

theorem actual_good_event_measurable (r : ℝ) :
    MeasurableSet (sourceFoldGood (-1) (1/12) r) :=
  sourceFoldGood_measurable negativePeriod (1/12) r

theorem actual_obstruction_inclusion (r : ℝ) (hr : 0 < r) :
    (sourceFoldGood (-1) (1/12) r)ᶜ ⊆
      I4SourceWeightedCurvature.sourceRegularityBad (-1) r (1/104857600) ∪
        I4SourceWeightedCurvature.sourceCurvatureOneSided (-1) r 1073741824 := by
  convert sourceFoldGood_compl_subset (-1) (1/12) r hr using 1
  norm_num [sourceCutoffEps,sourceCutoffA,sourceScale]

/-- A concrete counterexample: forgetting 8^5 misses a genuine failure. -/
theorem omitted_scale_counterexample :
    ¬ ((1:ℝ)/100000000 * (16*1)^5 ≤ 1/100 ∧
      1024*(16*1)^5 ≤ -(-100:ℝ)/((1:ℝ)/100000000)) ∧
    ¬ ((1:ℝ)/(100*2^5) < (1:ℝ)/100000000*1^5 ∨
      -(1024*(16:ℝ)^5)*((1:ℝ)/100000000)*1^5 ≤ -100) := by norm_num

theorem scaled_failure_is_detected :
    (1:ℝ)/(100*16^5) < (1:ℝ)/100000000*1^5 ∨
      -(1024*(16:ℝ)^5)*((1:ℝ)/100000000)*1^5 ≤ -100 :=
  cutoff_failure_inclusion 16 (1/100000000) 1 (-100) (by norm_num) (by norm_num)
    omitted_scale_counterexample.1

theorem failure_witness_cutoffs :
    (1:ℝ)/100 < (1:ℝ)/100000000*(16*1)^5 ∧
      1024*(16*1)^5 ≤ -(-100:ℝ)/((1:ℝ)/100000000) ∧
      (1:ℝ)/(100*16^5) < (1:ℝ)/100000000*1^5 := by norm_num

/-- Closed obstruction includes a boundary point where both good cutoffs hold. -/
theorem reverse_inclusion_counterexample :
    ((1:ℝ)/104857600 * (16*1)^5 ≤ 1/100 ∧
      1024*(16*1)^5 ≤ -(-(256:ℝ)/25)/((1:ℝ)/104857600)) ∧
      -(1024*(16:ℝ)^5)*((1:ℝ)/104857600)*1^5 ≤ -(256:ℝ)/25 := by norm_num

theorem sign_and_division_control :
    -(-(256:ℝ)/25)/((1:ℝ)/104857600) = 1073741824 ∧
      ¬ (1024*(16:ℝ)^5 ≤ -((256:ℝ)/25)/((1:ℝ)/104857600)) := by norm_num

theorem actual_same_law_ac (r : ℝ) :
    sourceFoldWeightedLaw negativePeriod r 3 ≪ sourceGapLaw negativePeriod r 3 (1/6) :=
  sourceFoldWeightedLaw_absolutelyContinuous negativePeriod r 3

theorem actual_closed_probability :
    ∃ C δ : ℝ, 0 ≤ C ∧ 0 < δ ∧ δ ≤ 1 ∧
      ∀ r : ℝ, 0 < r → r < δ →
        IsProbabilityMeasure (sourceFoldWeightedLaw negativePeriod r 3) ∧
        (sourceFoldWeightedLaw negativePeriod r 3).real (sourceFoldGood (-1) (1/12) r)ᶜ ≤ C*r^3 :=
  sourceFoldWeightedProbability_bound negativePeriod 3 (1/12) (by norm_num)

theorem actual_closed_probability_h0 :
    ∃ C δ : ℝ, 0 ≤ C ∧ 0 < δ ∧ δ ≤ 1 ∧
      ∀ r : ℝ, 0 < r → r < δ →
        IsProbabilityMeasure (sourceFoldWeightedLaw negativePeriod r 3) ∧
        (sourceFoldWeightedLaw negativePeriod r 3).real (sourceFoldGood (-1) (1/12) r)ᶜ ≤ C*r^3 ∧
        ∀ (K : Type) [Field K], ∀ᵐ sample ∂sourceFoldWeightedLaw negativePeriod r 3,
          sample ∈ sourceFoldGood (-1) (1/12) r →
            ∃ D : ℝ ⥤ ModuleCat K,
              Nonempty (superlevel_h0Filtration (actualTorusField negativePeriod sample)
                (ModuleCat.of K K) ≅ elderInterval K 3 (3-r^3/6) ⊞ D) ∧
              strictClearanceSet (actualTorusField negativePeriod sample)
                (torusProjection 2 (-1) (endpointM r)) = Iio (3-r^3/6) ∧
              strictClearanceDeath (actualTorusField negativePeriod sample)
                (torusProjection 2 (-1) (endpointM r)) = 3-r^3/6 :=
  sourceFoldWeightedProbability_h0 negativePeriod 3 (1/12) (by norm_num) (by norm_num)

end FoldWeightedControls
