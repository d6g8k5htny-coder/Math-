import SourceActualFoldTorus
import Controls

noncomputable section
open Set MeasureTheory
open I4SmoothCarrier I4Torus I4SourceConfluentPins I4SourceCompactTargetMoments
open I4SourceAdaptiveFoldEstimates SourceActualFoldTorus
set_option autoImplicit false
namespace ActualTorusControls

/-- Same-period pullback is exact on the negative original period. -/
theorem negative_period_pullback (sample : SmoothSample 2 (-1)) (x : Fin 2 → ℝ) :
    actualTorusField (by norm_num : (-1:ℝ) ≠ 0) sample (torusProjection 2 (-1) x) =
      smoothSourceField 2 (-1) sample x :=
  actualTorusField_pullback (by norm_num) sample x

/-- The physical amplitude is 6 for k=r=1. -/
theorem actual_physical_scale (sample : SmoothSample 2 (-1)) (p : ℝ × ℝ) :
    actualTorusField (by norm_num : (-1:ℝ) ≠ 0) sample (torusPhysicalMap (-1) 1 p) =
      6 * I4SourceAdaptiveFoldChart.actualFoldPotential 1 1 sample p := by
  simpa using torusPhysicalMap_field_eq (by norm_num : (-1:ℝ) ≠ 0) sample
    (by norm_num : (1:ℝ) ≠ 0) (by norm_num : (1:ℝ) ≠ 0) p

/-- Nonzero b and k different from 1/6 use the literal unchanged negative-L law. -/
theorem negative_period_actual_law :
    ∃ δ : ℝ, 0 < δ ∧ δ ≤ 1 ∧ ∀ r : ℝ, 0 < r → r < δ →
      ∀ᵐ sample ∂sourceGapLaw (by norm_num : (-1:ℝ) ≠ 0) r 3 1,
        r*(sourceT 1 sample)^5 ≤ 1/100 →
          1024*(sourceT 1 sample)^5 ≤ sourceKappa r 1 sample →
            strictClearanceSet (actualTorusField (by norm_num : (-1:ℝ) ≠ 0) sample)
                (torusProjection 2 (-1) (endpointM r)) = Iio (3-r^3) ∧
              strictClearanceDeath (actualTorusField (by norm_num : (-1:ℝ) ≠ 0) sample)
                (torusProjection 2 (-1) (endpointM r)) = 3-r^3 := by
  obtain ⟨δ,hδ,hδ1,h⟩ := sourceGapLaw_actual_torus_clearance
    (by norm_num : (-1:ℝ) ≠ 0)
  refine ⟨δ,hδ,hδ1,?_⟩
  intro r hr hrδ
  simpa using h 1 (by norm_num) r hr hrδ 3 1 le_rfl

/-- Two real lifts separated by one original negative period have equal images. -/
theorem negative_period_lifts_same :
    torusProjection 2 (-1) (![0,0] : Fin 2 → ℝ) =
      torusProjection 2 (-1) (![-1,0] : Fin 2 → ℝ) := by
  ext i
  fin_cases i
  · simpa only [torusProjection, Matrix.cons_val_zero, AddCircle.coe_zero] using
      (AddCircle.coe_period (-1:ℝ)).symm
  · simp [torusProjection]

/-- Their equality in the quotient does not collapse the real cover. -/
theorem negative_period_collapsed_lifts_counterexample :
    (![0,0] : Fin 2 → ℝ) ≠ ![-1,0] := by
  intro h
  have hzero := congrFun h 0
  norm_num at hzero

/-- The global projection is demonstrably noninjective. -/
theorem negative_period_projection_not_injective :
    ¬ Function.Injective (torusProjection 2 (-1)) := by
  intro h
  exact negative_period_collapsed_lifts_counterexample (h negative_period_lifts_same)

/-- The same actual sample is periodic across these quotient-equal lifts. -/
theorem negative_period_field_periodicity (sample : SmoothSample 2 (-1)) :
    smoothSourceField 2 (-1) sample (![0,0] : Fin 2 → ℝ) =
      smoothSourceField 2 (-1) sample (![-1,0] : Fin 2 → ℝ) := by
  simpa only [actualTorusField_pullback] using
    congrArg (actualTorusField (by norm_num : (-1:ℝ) ≠ 0) sample) negative_period_lifts_same

/-- Reuse the qualified physical polynomial control through only the new
predicate adapter; no old polynomial proof is replayed here. -/
theorem reused_physical_clearance_interface :
    strictClearanceSet ActualDeathControls.G ActualDeathControls.Mphys = Iio 2 := by
  rw [strictClearanceSet_eq_C263]
  exact ActualDeathControls.polynomial_physical_death.2

/-- The new supremum definition keeps the same absolute physical level. -/
theorem reused_physical_supremum_interface :
    strictClearanceDeath ActualDeathControls.G ActualDeathControls.Mphys = 2 := by
  rw [strictClearanceDeath, reused_physical_clearance_interface, csSup_Iio]

/-- Strict clearance includes lower levels and excludes the death level. -/
theorem strict_endpoint_interface :
    (1:ℝ) ∈ strictClearanceSet ActualDeathControls.G ActualDeathControls.Mphys ∧
      (2:ℝ) ∉ strictClearanceSet ActualDeathControls.G ActualDeathControls.Mphys := by
  rw [reused_physical_clearance_interface]
  norm_num

end ActualTorusControls
