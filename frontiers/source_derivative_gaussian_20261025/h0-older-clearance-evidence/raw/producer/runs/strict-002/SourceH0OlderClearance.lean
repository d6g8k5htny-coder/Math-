import SourceActualFoldH0

/-! Strict clearance as vanishing of an actual ordinary-H0 point-class
*difference* under closed-superlevel inclusion. Individual ordinary point
classes are not asserted to die. The actual signed source application reuses
its qualified threshold and interval/complement on the same sample. -/

noncomputable section
open CategoryTheory Limits Set MeasureTheory
set_option autoImplicit false

namespace I4SourceH0OlderClearance

universe u
open SourceActualFoldTorus TorusFiltration

private def birthPoint {X : Type u} [TopologicalSpace X] (F : X → ℝ) (M : X) :
    superlevel_set F (-F M) :=
  ⟨M, by simp [superlevel_set]⟩

private def olderBirthPoint {X : Type u} [TopologicalSpace X] (F : X → ℝ)
    (M P : X) (hP : F M < F P) : superlevel_set F (-F M) :=
  ⟨P, by simpa [superlevel_set] using hP.le⟩

private theorem coefficient_identity_ne_zero (K : Type u) [Field K] :
    (𝟙 (ModuleCat.of K K) : ModuleCat.of K K ⟶ ModuleCat.of K K) ≠ 0 := by
  intro h
  have h1 := ConcreteCategory.congr_hom h (1 : K)
  exact one_ne_zero (by simpa using h1)

/-- A strictly older point has the same ordinary-H0 class after inclusion
at some closed level strictly above h. The mapped object is the difference
of its two birth-level point-class morphisms. -/
def h0OlderClearance (K : Type u) [Field K] {X : Type u} [TopologicalSpace X]
    (F : X → ℝ) (M : X) (h : ℝ) : Prop :=
  ∃ (P : X) (hP : F M < F P), ∃ c : ℝ, h < c ∧ ∃ hc : c ≤ F M,
    (ordinaryH0_pointClass (TopCat.of (superlevel_set F (-F M)))
        (ModuleCat.of K K) (birthPoint F M) -
      ordinaryH0_pointClass (TopCat.of (superlevel_set F (-F M)))
        (ModuleCat.of K K) (olderBirthPoint F M P hP)) ≫
      (superlevel_h0Filtration F (ModuleCat.of K K)).map
        (homOfLE (neg_le_neg hc)) = 0

/-- The ordinary-H0 difference-map condition is exactly strict clearance.
Only compactness of the path parameter is needed for the reverse direction. -/
theorem h0OlderClearance_iff_strictClearance
    (K : Type u) [Field K] {X : Type u} [TopologicalSpace X]
    (F : X → ℝ) (hF : Continuous F) (M : X) (h : ℝ) :
    h0OlderClearance K F M h ↔ h ∈ strictClearanceSet F M := by
  constructor
  · rintro ⟨P,hP,c,hhc,hc,hzero⟩
    have hj := (ordinaryH0_filtration_difference_zero_iff_joinedIn F
      (ModuleCat.of K K) (coefficient_identity_ne_zero K) (neg_le_neg hc)
      (birthPoint F M) (olderBirthPoint F M P hP)).1 hzero
    obtain ⟨γ,hγ⟩ := hj
    refine ⟨P,hP,γ,?_⟩
    intro t
    have ht : c ≤ F (γ t) := by simpa [superlevel_set] using hγ t
    by_contra hnot
    have hle : F (γ t) ≤ h := le_of_not_gt hnot
    linarith
  · rintro ⟨P,hP,γ,hγ⟩
    obtain ⟨t₀,_,hmin⟩ := (isCompact_univ : IsCompact (univ : Set unitInterval)).exists_isMinOn
      (Set.nonempty_univ) (hF.comp γ.continuous).continuousOn
    let c := F (γ t₀)
    have hc : c ≤ F M := by
      have ht := hmin (Set.mem_univ (0 : unitInterval))
      simpa [c] using ht
    refine ⟨P,hP,c,hγ t₀,hc,?_⟩
    apply (ordinaryH0_filtration_difference_zero_iff_joinedIn F
      (ModuleCat.of K K) (coefficient_identity_ne_zero K) (neg_le_neg hc)
      (birthPoint F M) (olderBirthPoint F M P hP)).2
    refine ⟨γ,?_⟩
    intro t
    simpa [superlevel_set, c] using hmin (Set.mem_univ t)

/-- On the old real carrier, the retained nonessential death height has this
literal homology-map strict cut. No essential finite bar is inferred. -/
theorem h0OlderClearance_realCover_iff_lt_death
    (K : Type) [Field K] {d : ℕ} (g : superlevelBar_E d → ℝ)
    (hg : Continuous g) (M : superlevelBar_E d)
    (hne : ¬ superlevelBar_isEssential g M) (h : ℝ) :
    h0OlderClearance K g M h ↔ h < superlevelBar_deathHeight g M := by
  rw [h0OlderClearance_iff_strictClearance K g hg M h]
  rw [strictClearanceSet_eq_C263]
  exact (superlevelBar_strict_cut g hg M hne h).symm

open AdaptiveFoldBoundaryPath I4SmoothCarrier I4SourceConfluentPins
open I4SourceRawPinConditioning I4SourceCompactTargetMoments
open I4SourceAdaptiveFoldChart I4SourceAdaptiveFoldEstimates I4Torus

/-- The signed original-period actual source law has the same uniform H0 cut,
its exact real supremum and its retained actual interval/complement. -/
theorem sourceGapLaw_h0OlderClearance_uniform {L : ℝ} (hL : L ≠ 0) :
    ∃ δ : ℝ, 0 < δ ∧ δ ≤ 1 ∧
      ∀ (K : Type) [Field K],
      ∀ k₀ : ℝ, 0 < k₀ → ∀ r : ℝ, 0 < r → r < δ →
        ∀ b k : ℝ, k₀ ≤ k → ∀ᵐ sample ∂sourceGapLaw hL r b k,
          let T := sourceT k₀ sample
          let κ := sourceKappa r k sample
          let F := actualTorusField hL sample
          let Mbar := torusProjection 2 L (endpointM r)
          r*T^5 ≤ 1/100 → 1024*T^5 ≤ κ →
            {h | h0OlderClearance K F Mbar h} = Iio (b-k*r^3) ∧
            sSup {h | h0OlderClearance K F Mbar h} = b-k*r^3 ∧
            ∃ C : ℝ ⥤ ModuleCat K,
              Nonempty (superlevel_h0Filtration F (ModuleCat.of K K) ≅
                elderInterval K b (b-k*r^3) ⊞ C) := by
  obtain ⟨δ,hδ,hδ1,h⟩ := SourceActualFoldH0.sourceGapLaw_actual_torus_h0 hL
  refine ⟨δ,hδ,hδ1,?_⟩
  intro K instK k₀ hk₀ r hr hrδ b k hk
  filter_upwards [h K k₀ hk₀ r hr hrδ b k hk] with sample hs
  dsimp only at hs ⊢
  intro hrT hκ
  obtain ⟨C,hiso,hclear,_hdeath⟩ := hs hrT hκ
  have hcut : {h | h0OlderClearance K (actualTorusField hL sample)
      (torusProjection 2 L (endpointM r)) h} = Iio (b-k*r^3) := by
    ext a
    rw [h0OlderClearance_iff_strictClearance K _ (actualTorusField_continuous hL sample),
      hclear]
  exact ⟨hcut, by rw [hcut, csSup_Iio], C, hiso⟩

end I4SourceH0OlderClearance
