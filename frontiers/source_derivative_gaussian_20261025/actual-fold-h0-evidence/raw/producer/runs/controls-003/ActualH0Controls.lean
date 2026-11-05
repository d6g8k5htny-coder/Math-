import SourceActualFoldH0

noncomputable section
open CategoryTheory Limits Set MeasureTheory
open SourceActualFoldH0 SourceActualFoldTorus TorusFiltration
open AdaptiveFoldBoundaryPath I4SmoothCarrier I4SourceConfluentPins
open I4SourceRawPinConditioning I4SourceCompactTargetMoments
open I4SourceAdaptiveFoldChart I4SourceAdaptiveFoldEstimates I4Torus
set_option autoImplicit false
namespace ActualH0Controls

theorem negativePeriod : (-1 : ℝ) ≠ 0 := by norm_num

/-- Actual signed period -1, absolute birth 3, and k=k0=1; delta precedes K. -/
theorem negative_period_closed_endpoint :
    ∃ δ : ℝ, 0 < δ ∧ δ ≤ 1 ∧
      ∀ (K : Type) [Field K], ∀ r : ℝ, 0 < r → r < δ →
        ∀ᵐ sample ∂sourceGapLaw negativePeriod r 3 1,
          let T := sourceT 1 sample
          let κ := sourceKappa r 1 sample
          r*T^5 ≤ 1/100 → 1024*T^5 ≤ κ →
            ∃ C : ℝ ⥤ ModuleCat K,
              Nonempty (superlevel_h0Filtration (actualTorusField negativePeriod sample)
                (ModuleCat.of K K) ≅ elderInterval K 3 (3-r^3) ⊞ C) ∧
              strictClearanceSet (actualTorusField negativePeriod sample)
                  (torusProjection 2 (-1) (endpointM r)) = Iio (3-r^3) ∧
              strictClearanceDeath (actualTorusField negativePeriod sample)
                  (torusProjection 2 (-1) (endpointM r)) = 3-r^3 := by
  obtain ⟨δ,hδ,hδ1,h⟩ := sourceGapLaw_actual_torus_h0 negativePeriod
  refine ⟨δ,hδ,hδ1,?_⟩
  intro K instK r hr hrδ
  simpa only [one_mul] using h K 1 (by norm_num) r hr hrδ 3 1 le_rfl

variable (K : Type) [Field K] (sample : SmoothSample 2 (-1))
variable (r R : ℝ) (z : ℝ → ℝ)
variable (T : TorusTrapData (actualTorusField negativePeriod sample)
  (torusProjection 2 (-1) (endpointM r)) (torusPhysicalMap (-1) r (olderPoint z))
  3 (3-r^3) (torusPhysicalMap (-1) r '' leftBox R))

include T

/-- The new conversion retains actual points and image domain literally. -/
theorem actual_typed_conversion : ElderTrap (actualTorusField negativePeriod sample)
    (torusProjection 2 (-1) (endpointM r)) (torusPhysicalMap (-1) r (olderPoint z))
    3 (3-r^3) (torusPhysicalMap (-1) r '' leftBox R) := toElderTrap T

def actual_section : elderInterval K 3 (3-r^3) ⟶
    superlevel_h0Filtration (actualTorusField negativePeriod sample) (ModuleCat.of K K) :=
  h0Section K T

def actual_retraction :
    superlevel_h0Filtration (actualTorusField negativePeriod sample) (ModuleCat.of K K) ⟶
      elderInterval K 3 (3-r^3) := h0Retraction K T

theorem actual_section_retraction : actual_section K sample r R z T ≫
    actual_retraction K sample r R z T = 𝟙 (elderInterval K 3 (3-r^3)) :=
  h0Section_retraction K T

theorem actual_complement_is_kernel : h0Complement K T =
    kernel (elderRetraction (k := K) (actual_typed_conversion sample r R z T)) := rfl

def actual_direct_sum :
    superlevel_h0Filtration (actualTorusField negativePeriod sample) (ModuleCat.of K K) ≅
      elderInterval K 3 (3-r^3) ⊞ h0Complement K T := h0DirectSummand K T

theorem actual_generic_clearance :
    strictClearanceSet (actualTorusField negativePeriod sample)
        (torusProjection 2 (-1) (endpointM r)) = Iio (3-r^3) ∧
      strictClearanceDeath (actualTorusField negativePeriod sample)
        (torusProjection 2 (-1) (endpointM r)) = 3-r^3 :=
  ⟨T.strictClearanceSet_eq_Iio,T.strictClearanceDeath_eq⟩

omit T in
/-- Increasing time has birth -3 and death -(3-r^3), with positive length. -/
theorem nondefault_endpoint_signs (r : ℝ) (hr : 0 < r) :
    elderActive 3 (3-r^3) (-3) ∧
      ¬ elderActive 3 (3-r^3) (-(3-r^3)) ∧
      -(3-r^3)-(-3) = r^3 ∧ 0 < r^3 := by
  simpa only [one_mul] using fold_interval_endpoints 3 1 r (by norm_num) hr

/-- A concrete counterexample to including death, proved through the new API. -/
theorem death_inclusion_counterexample : ¬ elderActive 3 (3-(1:ℝ)^3) (-(3-(1:ℝ)^3)) :=
  (nondefault_endpoint_signs 1 (by norm_num)).2.1

/-- The wrong positive height has not replaced increasing time -height. -/
theorem wrong_sign_counterexample : ¬ elderActive 3 (3-(1:ℝ)^3) (3-(1:ℝ)^3) := by
  norm_num [elderActive]

end ActualH0Controls
