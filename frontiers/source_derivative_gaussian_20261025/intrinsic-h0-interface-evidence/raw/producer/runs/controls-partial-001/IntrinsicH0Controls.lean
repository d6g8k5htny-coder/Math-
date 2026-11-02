import SourceIntrinsicH0Interface

noncomputable section
open CategoryTheory Limits Set MeasureTheory
open UniversalLaw.Spec.Lifetime I4SourceH0OlderClearance I4SourceIntrinsicH0Interface
open TorusFiltration I4LifetimeField I4SmoothCarrier I4SourceConfluentPins
open I4SourceRawPinConditioning I4SourceCompactTargetMoments
open I4SourceAdaptiveFoldChart I4SourceAdaptiveFoldEstimates AdaptiveFoldBoundaryPath
open SourceActualFoldTorus I4SourceActualFoldCandidate I4Torus
set_option autoImplicit false
namespace IntrinsicH0Controls

def constantSeven : E 1 → ℝ := fun _ => 7

theorem constant_cut_empty :
    {h : ℝ | h0OlderClearance ℝ constantSeven (0 : E 1) h} = ∅ := by
  ext h
  constructor
  · rintro ⟨P,hP,_⟩
    exact (lt_irrefl (7 : ℝ) hP).elim
  · exact False.elim

theorem intrinsic_constant_essential : (h0Interface 1 2).IsEssential constantSeven 0 :=
  fun _ => le_rfl

theorem intrinsic_constant_death : (h0Interface 1 2).deathHeight constantSeven 0 = 0 := by
  rw [(h0Interface_cut_death_eq_C263 2 constantSeven continuous_const 0).2]
  exact superlevelBar_death_eq_zero_of_essential _ _ intrinsic_constant_essential

theorem constant_no_pair (S : E 1) : ¬ h0ThresholdPair constantSeven 0 S := by
  rintro ⟨_hM,_hS,hcut⟩
  have hi : (6 : ℝ) ∈ Iio (constantSeven S) := by norm_num [constantSeven]
  rw [← hcut, constant_cut_empty] at hi
  exact hi

theorem constant_essential_default_and_no_pair :
    {h : ℝ | h0OlderClearance ℝ constantSeven 0 h} = ∅ ∧
    (h0Interface 1 2).IsEssential constantSeven 0 ∧
    (h0Interface 1 2).deathHeight constantSeven 0 = 0 ∧
    ∀ S : E 1, ¬ h0ThresholdPair constantSeven 0 S :=
  ⟨constant_cut_empty,intrinsic_constant_essential,intrinsic_constant_death,constant_no_pair⟩

/-- A genuine supplied interface: only essential death defaults are changed. -/
def essentialShiftInterface : SuperlevelBarInterface 1 2 where
  deathHeight g M := if (h0Interface 1 2).IsEssential g M then 17
    else (h0Interface 1 2).deathHeight g M
  IsEssential := (h0Interface 1 2).IsEssential
  ElderPartner := (h0Interface 1 2).ElderPartner
  essential_iff := (h0Interface 1 2).essential_iff
  deathHeight_maximin := by
    intro g hs hp M hne h
    rw [ite_eq_right hne]
    exact (h0Interface 1 2).deathHeight_maximin g hs hp M hne h
  elderPartner_iff := by
    intro g hs hp hm M S
    rw [(h0Interface 1 2).elderPartner_iff g hs hp hm M S]
    constructor
    · rintro ⟨hM,hS,hne,hd⟩
      exact ⟨hM,hS,hne,by rw [ite_eq_right hne]; exact hd⟩
    · rintro ⟨hM,hS,hne,hd⟩
      rw [ite_eq_right hne] at hd
      exact ⟨hM,hS,hne,hd⟩

theorem shifted_constant_death : essentialShiftInterface.deathHeight constantSeven 0 = 17 := by
  change (if (h0Interface 1 2).IsEssential constantSeven 0 then 17
    else (h0Interface 1 2).deathHeight constantSeven 0) = 17
  exact ite_eq_left intrinsic_constant_essential

/-- Separately passed counterexample to unguarded supplied-I death equality. -/
theorem essential_default_counterexample :
    essentialShiftInterface.deathHeight constantSeven 0 ≠
      (h0Interface 1 2).deathHeight constantSeven 0 := by
  rw [shifted_constant_death,intrinsic_constant_death]
  norm_num

theorem positivePeriod : (0 : ℝ) < 2 := by norm_num

/-- Original positive period2 and literal sample, with global Morse supplied. -/
theorem actual_given_interface_requires_morse (I : SuperlevelBarInterface 2 2)
    (sample : SmoothSample 2 2) (r : ℝ)
    (hm : IsMorseDistinct 2 2 (actualField 2 2 sample))
    (hf : IsFiniteBar 2 2 (h0Interface 2 2) (actualField 2 2 sample)
      (endpointLiftM r) (endpointLiftS r)) :
    IsFiniteBar 2 2 I (actualField 2 2 sample) (endpointLiftM r) (endpointLiftS r) :=
  ((h0Interface_morse_compatibility 2 I _ (actualField_smooth 2 positivePeriod sample)
    (actualField_periodic 2 positivePeriod sample) hm _ _).2).2 hf

/-- Same actual law/sample/torus, delta before K and symbolic r, exact two cutoffs. -/
theorem actual_positive_period_uniform :
    ∃ δ : ℝ, 0 < δ ∧ δ ≤ 1 ∧
      ∀ (K : Type) [Field K], ∀ r : ℝ, 0 < r → r < δ →
        ∀ᵐ sample ∂sourceGapLaw positivePeriod.ne' r 3 1,
          let T := sourceT 1 sample
          let κ := sourceKappa r 1 sample
          let g := actualField 2 2 sample
          let M := endpointLiftM r
          let S := endpointLiftS r
          let F := actualTorusField positivePeriod.ne' sample
          let Mbar := torusProjection 2 2 (endpointM r)
          r*T^5 ≤ 1/100 → 1024*T^5 ≤ κ →
            IsFiniteBar 2 2 (h0Interface 2 2) g M S ∧
            g M = 3 ∧ g S = 3-r^3 ∧
            (h0Interface 2 2).deathHeight g M = 3-r^3 ∧
            {h : ℝ | h0OlderClearance ℝ g M h} = Iio (3-r^3) ∧
            {h : ℝ | h0OlderClearance K F Mbar h} = Iio (3-r^3) ∧
            ∃ C : ℝ ⥤ ModuleCat K,
              Nonempty (superlevel_h0Filtration F (ModuleCat.of K K) ≅
                elderInterval K 3 (3-r^3) ⊞ C) := by
  obtain ⟨δ,hδ,hδ1,_hδL,h⟩ := sourceGapLaw_intrinsic_h0_finiteBar_uniform positivePeriod
  refine ⟨δ,hδ,hδ1,?_⟩
  intro K instK r hr hrδ
  simpa only [one_mul] using h K 1 (by norm_num) r hr hrδ 3 1 le_rfl

end IntrinsicH0Controls
