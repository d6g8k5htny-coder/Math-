import SourceH0OlderClearance

noncomputable section
open CategoryTheory Limits Set MeasureTheory
open SourceActualFoldTorus TorusFiltration
open AdaptiveFoldBoundaryPath I4SmoothCarrier I4SourceConfluentPins
open I4SourceRawPinConditioning I4SourceCompactTargetMoments
open I4SourceAdaptiveFoldChart I4SourceAdaptiveFoldEstimates I4Torus
open I4SourceH0OlderClearance
set_option autoImplicit false
namespace OlderClearanceControls

private theorem real_coefficients_nonzero :
    (𝟙 (ModuleCat.of ℝ ℝ) : ModuleCat.of ℝ ℝ ⟶ ModuleCat.of ℝ ℝ) ≠ 0 := by
  intro h
  have h1 := ConcreteCategory.congr_hom h (1 : ℝ)
  change (1 : ℝ) = 0 at h1
  exact one_ne_zero h1

def pointZero : superlevel_set (id : ℝ → ℝ) 0 := ⟨0, by norm_num [superlevel_set]⟩
def pointOne : superlevel_set (id : ℝ → ℝ) 0 := ⟨1, by norm_num [superlevel_set]⟩

/-- The literal straight path lies in the actual closed level [0,infinity). -/
theorem identity_closed_joined : JoinedIn (superlevel_set (id : ℝ → ℝ) 0) 0 1 := by
  refine ⟨Path.segment 0 1, ?_⟩
  intro t
  change -(0 : ℝ) ≤ (Path.segment (0 : ℝ) 1) t
  simpa [Path.segment] using t.property.1

/-- Actual ordinary H0 inclusion map, at source and target time zero. -/
theorem identity_difference_zero :
    (ordinaryH0_pointClass (TopCat.of (superlevel_set (id : ℝ → ℝ) 0))
        (ModuleCat.of ℝ ℝ) pointZero -
      ordinaryH0_pointClass (TopCat.of (superlevel_set (id : ℝ → ℝ) 0))
        (ModuleCat.of ℝ ℝ) pointOne) ≫
      (superlevel_h0Filtration (id : ℝ → ℝ) (ModuleCat.of ℝ ℝ)).map
        (homOfLE (le_refl (0 : ℝ))) = 0 :=
  (ordinaryH0_filtration_difference_zero_iff_joinedIn (id : ℝ → ℝ)
    (ModuleCat.of ℝ ℝ) real_coefficients_nonzero (le_refl 0) pointZero pointOne).2
      identity_closed_joined

theorem identity_first_point_nonzero :
    ordinaryH0_pointClass (TopCat.of (superlevel_set (id : ℝ → ℝ) 0))
      (ModuleCat.of ℝ ℝ) pointZero ≠ 0 :=
  ordinaryH0_pointClass_ne_zero _ _ real_coefficients_nonzero _

theorem identity_second_point_nonzero :
    ordinaryH0_pointClass (TopCat.of (superlevel_set (id : ℝ → ℝ) 0))
      (ModuleCat.of ℝ ℝ) pointOne ≠ 0 :=
  ordinaryH0_pointClass_ne_zero _ _ real_coefficients_nonzero _

theorem identity_strict_at_neg_one : h0OlderClearance ℝ (id : ℝ → ℝ) 0 (-1) := by
  refine ⟨1, by norm_num, 0, by norm_num, by norm_num, ?_⟩
  exact identity_difference_zero

/-- Every proposed strict path already fails at its starting point. -/
theorem identity_no_strict_clearance_at_zero :
    (0 : ℝ) ∉ strictClearanceSet (id : ℝ → ℝ) 0 := by
  rintro ⟨P,_hP,γ,hγ⟩
  have hstart := hγ 0
  simpa using hstart

theorem identity_not_strict_at_zero : ¬ h0OlderClearance ℝ (id : ℝ → ℝ) 0 0 := by
  rw [h0OlderClearance_iff_strictClearance ℝ _ continuous_id]
  exact identity_no_strict_clearance_at_zero

theorem constant_empty_cut (K : Type) [Field K] (a : ℝ) :
    {h | h0OlderClearance K (fun _ : ℝ => a) 0 h} = ∅ := by
  ext h
  constructor
  · rintro ⟨P,hP,_⟩
    exact (lt_irrefl a hP).elim
  · exact False.elim

/- The sole semantic mutation: the strict margin h<c becomes h<=c.
The subtype points are the same literal birth-level points. -/
def relaxedOlderClearance (K : Type) [Field K] {X : Type} [TopologicalSpace X]
    (F : X → ℝ) (M : X) (h : ℝ) : Prop :=
  ∃ (P : X) (hP : F M < F P), ∃ c : ℝ, h ≤ c ∧ ∃ hc : c ≤ F M,
    (ordinaryH0_pointClass (TopCat.of (superlevel_set F (-F M)))
        (ModuleCat.of K K) ⟨M, by simp [superlevel_set]⟩ -
      ordinaryH0_pointClass (TopCat.of (superlevel_set F (-F M)))
        (ModuleCat.of K K) ⟨P, by simpa [superlevel_set] using hP.le⟩) ≫
      (superlevel_h0Filtration F (ModuleCat.of K K)).map
        (homOfLE (neg_le_neg hc)) = 0

theorem relaxed_actual_at_zero : relaxedOlderClearance ℝ (id : ℝ → ℝ) 0 0 := by
  refine ⟨1, by norm_num, 0, le_rfl, le_rfl, ?_⟩
  exact identity_difference_zero

/-- Separately passed actual H0 witness and strict-start obstruction. -/
theorem relaxed_margin_counterexample :
    relaxedOlderClearance ℝ (id : ℝ → ℝ) 0 0 ∧
      (0 : ℝ) ∉ strictClearanceSet (id : ℝ → ℝ) 0 :=
  ⟨relaxed_actual_at_zero,identity_no_strict_clearance_at_zero⟩

theorem negativePeriod : (-1 : ℝ) ≠ 0 := by norm_num

/-- Actual original signed period -1, absolute levels, same law and two cutoffs.
The existential radius still precedes every field and symbolic r. -/
theorem signed_source_closed_endpoint :
    ∃ δ : ℝ, 0 < δ ∧ δ ≤ 1 ∧
      ∀ (K : Type) [Field K], ∀ r : ℝ, 0 < r → r < δ →
        ∀ᵐ sample ∂sourceGapLaw negativePeriod r 3 1,
          let T := sourceT 1 sample
          let κ := sourceKappa r 1 sample
          let F := actualTorusField negativePeriod sample
          let Mbar := torusProjection 2 (-1) (endpointM r)
          r*T^5 ≤ 1/100 → 1024*T^5 ≤ κ →
            {h | h0OlderClearance K F Mbar h} = Iio (3-r^3) ∧
            sSup {h | h0OlderClearance K F Mbar h} = 3-r^3 ∧
            ∃ C : ℝ ⥤ ModuleCat K,
              Nonempty (superlevel_h0Filtration F (ModuleCat.of K K) ≅
                elderInterval K 3 (3-r^3) ⊞ C) := by
  obtain ⟨δ,hδ,hδ1,h⟩ := sourceGapLaw_h0OlderClearance_uniform negativePeriod
  refine ⟨δ,hδ,hδ1,?_⟩
  intro K instK r hr hrδ
  simpa only [one_mul] using h K 1 (by norm_num) r hr hrδ 3 1 le_rfl

/-- Existing retained interval signs at the concrete signed-source interface. -/
theorem signed_endpoint_convention (r : ℝ) (hr : 0 < r) :
    elderActive 3 (3-r^3) (-3) ∧
      ¬ elderActive 3 (3-r^3) (-(3-r^3)) ∧
      -(3-r^3)-(-3) = r^3 ∧ 0 < r^3 := by
  simpa only [one_mul] using SourceActualFoldH0.fold_interval_endpoints 3 1 r (by norm_num) hr

end OlderClearanceControls
