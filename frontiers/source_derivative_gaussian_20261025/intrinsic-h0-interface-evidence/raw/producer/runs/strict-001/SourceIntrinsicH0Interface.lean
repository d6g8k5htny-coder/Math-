import SourceH0OlderClearance
import SourceActualFoldCandidate

/-! A literal Lifetime interface with an intrinsic ordinary-H0 transition-cut
relation. Its off-Morse extension is a threshold pair, not a canonical global
labeling. The local actual source result retains its existing genuine interval;
no exhaustive barcode, once-counting or Parent result is asserted. -/

noncomputable section
open CategoryTheory Limits Set MeasureTheory
open UniversalLaw.Spec.Lifetime I4SourceH0OlderClearance TorusFiltration
set_option autoImplicit false

namespace I4SourceIntrinsicH0Interface

private def h0Cut {d : ℕ} (g : E d → ℝ) (M : E d) : Set ℝ :=
  {h | h0OlderClearance ℝ g M h}

private def h0Death {d : ℕ} (g : E d → ℝ) (M : E d) : ℝ := by
  classical
  exact if (h0Cut g M).Nonempty then sSup (h0Cut g M) else 0

/-- Genuine endpoint types and the whole actual ordinary-H0 older-merger cut.
This is a threshold relation, with no chosen global merger saddle. -/
def h0ThresholdPair {d : ℕ} (g : E d → ℝ) (M S : E d) : Prop :=
  IsNondegMax d g M ∧ IsIndexSaddle d g S ∧
    {h : ℝ | h0OlderClearance ℝ g M h} = Iio (g S)

private theorem cut_eq_C263 {d : ℕ} (g : E d → ℝ) (hg : Continuous g) (M : E d) :
    h0Cut g M = superlevelBar_clearanceSet g M := by
  ext h
  exact h0OlderClearance_iff_strictClearance ℝ g hg M h

private theorem death_eq_C263 {d : ℕ} (g : E d → ℝ) (hg : Continuous g) (M : E d) :
    h0Death g M = superlevelBar_deathHeight g M := by
  unfold h0Death superlevelBar_deathHeight
  rw [cut_eq_C263 g hg M]

private theorem thresholdPair_iff {d : ℕ} (g : E d → ℝ) (hg : Continuous g)
    (M S : E d) :
    h0ThresholdPair g M S ↔ IsNondegMax d g M ∧ IsIndexSaddle d g S ∧
      ¬ superlevelBar_isEssential g M ∧ h0Death g M = g S := by
  classical
  constructor
  · rintro ⟨hM,hS,hcut⟩
    change h0Cut g M = Iio (g S) at hcut
    have hcutne : (h0Cut g M).Nonempty := by
      rw [hcut]
      exact ⟨g S - 1, sub_one_lt (g S)⟩
    have hclearne : (superlevelBar_clearanceSet g M).Nonempty := by
      rw [← cut_eq_C263 g hg M]
      exact hcutne
    refine ⟨hM,hS,(superlevelBar_clearance_nonempty_iff g hg M).1 hclearne,?_⟩
    rw [h0Death, if_pos hcutne, hcut, csSup_Iio]
  · rintro ⟨hM,hS,hne,hd⟩
    refine ⟨hM,hS,?_⟩
    change h0Cut g M = Iio (g S)
    rw [cut_eq_C263 g hg M, superlevelBar_clearance_eq_Iio g hg M hne,
      ← death_eq_C263 g hg M, hd]

/-- The explicitly chosen intrinsic H0 threshold interface. Empty death0 is a
real default only; no essential ordinary-H0 class is assigned a finite death. -/
def h0Interface (d : ℕ) (L : ℝ) : SuperlevelBarInterface d L where
  deathHeight := h0Death
  IsEssential := superlevelBar_isEssential
  ElderPartner := h0ThresholdPair
  essential_iff := by intro g _hs _hp M; rfl
  deathHeight_maximin := by
    intro g hs _hp M hne h
    rw [death_eq_C263 g (hs 0).continuous M]
    exact superlevelBar_strict_cut g (hs 0).continuous M hne h
  elderPartner_iff := by
    intro g hs _hp _hm M S
    exact thresholdPair_iff g (hs 0).continuous M S

/-- On continuous inputs the intrinsic H0 cut and its explicit guarded default
agree with C263, including the constructed interface's essential default. -/
theorem h0Interface_cut_death_eq_C263
    {d : ℕ} (L : ℝ) (g : E d → ℝ) (hg : Continuous g) (M : E d) :
    {h : ℝ | h0OlderClearance ℝ g M h} = superlevelBar_clearanceSet g M ∧
      (h0Interface d L).deathHeight g M = superlevelBar_deathHeight g M :=
  ⟨cut_eq_C263 g hg M, death_eq_C263 g hg M⟩

private theorem given_death_eq {d : ℕ} (L : ℝ) (I : SuperlevelBarInterface d L)
    (g : E d → ℝ) (hs : IsSmooth d g) (hp : IsLPeriodic d L g)
    (M : E d) (hne : ¬ superlevelBar_isEssential g M) :
    I.deathHeight g M = h0Death g M := by
  have hI : ¬ I.IsEssential g M := fun h => hne ((I.essential_iff g hs hp M).1 h)
  rw [death_eq_C263 g (hs 0).continuous M]
  apply eq_of_forall_lt_iff
  intro a
  rw [I.deathHeight_maximin g hs hp M hI a,
    superlevelBar_strict_cut g (hs 0).continuous M hne a]
  rfl

/-- An arbitrary supplied interface agrees on its supplied Morse locus.
The death comparison used here is guarded at nonessential points. -/
theorem h0Interface_morse_compatibility
    {d : ℕ} (L : ℝ) (I : SuperlevelBarInterface d L)
    (g : E d → ℝ) (hs : IsSmooth d g)
    (hp : IsLPeriodic d L g) (hm : IsMorseDistinct d L g) (M S : E d) :
    (I.ElderPartner g M S ↔ h0ThresholdPair g M S) ∧
      (IsFiniteBar d L I g M S ↔ IsFiniteBar d L (h0Interface d L) g M S) := by
  have hpair : I.ElderPartner g M S ↔ h0ThresholdPair g M S := by
    rw [I.elderPartner_iff g hs hp hm M S, thresholdPair_iff g (hs 0).continuous M S]
    constructor
    · rintro ⟨hM,hS,hne,hd⟩
      have hne' : ¬ superlevelBar_isEssential g M := by
        intro he
        exact hne ((I.essential_iff g hs hp M).2 he)
      exact ⟨hM,hS,hne',(given_death_eq L I g hs hp M hne').symm.trans hd⟩
    · rintro ⟨hM,hS,hne,hd⟩
      have hne' : ¬ I.IsEssential g M := fun he => hne ((I.essential_iff g hs hp M).1 he)
      exact ⟨hM,hS,hne',(given_death_eq L I g hs hp M hne).trans hd⟩
  refine ⟨hpair,?_⟩
  change (IsCandidatePair d L g M S ∧ 0 < heightGap d g M S ∧ I.ElderPartner g M S) ↔
    (IsCandidatePair d L g M S ∧ 0 < heightGap d g M S ∧ h0ThresholdPair g M S)
  rw [hpair]

open I4LifetimeField I4SmoothCarrier I4SourceConfluentPins
open I4SourceRawPinConditioning I4SourceCompactTargetMoments
open I4SourceAdaptiveFoldChart I4SourceAdaptiveFoldEstimates AdaptiveFoldBoundaryPath
open SourceActualFoldTorus I4SourceActualFoldCandidate I4Torus

/-- The same actual candidate event gives intrinsic literal finite-bar membership,
both H0 cuts and the retained actual torus interval, with its original radius. -/
theorem sourceGapLaw_intrinsic_h0_finiteBar_uniform {L : ℝ} (hL : 0 < L) :
    ∃ δ : ℝ, 0 < δ ∧ δ ≤ 1 ∧ δ ≤ L/2 ∧
      ∀ (K : Type) [Field K],
      ∀ k₀ : ℝ, 0 < k₀ → ∀ r : ℝ, 0 < r → r < δ →
        ∀ b k : ℝ, k₀ ≤ k → ∀ᵐ sample ∂sourceGapLaw hL.ne' r b k,
          let T := sourceT k₀ sample
          let κ := sourceKappa r k sample
          let g := actualField 2 L sample
          let M := endpointLiftM r
          let S := endpointLiftS r
          let F := actualTorusField hL.ne' sample
          let Mbar := torusProjection 2 L (endpointM r)
          r*T^5 ≤ 1/100 → 1024*T^5 ≤ κ →
            IsFiniteBar 2 L (h0Interface 2 L) g M S ∧
            g M = b ∧ g S = b-k*r^3 ∧
            (h0Interface 2 L).deathHeight g M = b-k*r^3 ∧
            {h : ℝ | h0OlderClearance ℝ g M h} = Iio (b-k*r^3) ∧
            {h : ℝ | h0OlderClearance K F Mbar h} = Iio (b-k*r^3) ∧
            ∃ C : ℝ ⥤ ModuleCat K,
              Nonempty (superlevel_h0Filtration F (ModuleCat.of K K) ≅
                elderInterval K b (b-k*r^3) ⊞ C) := by
  obtain ⟨δ,hδ,hδ1,hδL,h⟩ := sourceGapLaw_actual_candidate_death_h0 hL
  refine ⟨δ,hδ,hδ1,hδL,?_⟩
  intro K instK k₀ hk₀ r hr hrδ b k hk
  filter_upwards [h K k₀ hk₀ r hr hrδ b k hk] with sample hs
  dsimp only at hs ⊢
  intro hrT hκ
  obtain ⟨U,z,_hz,hcan,_hd,hM,hS,_hgap,hpos,_hne,hdeath,hreal,
    ET,_hgain,_hpath,htorus,_htdeath,hiso⟩ := hs hrT hκ
  have hcont := I4SourceActualFoldDeath.actualField_continuous hL.ne' sample
  have hrealcut : {h | h0OlderClearance ℝ (actualField 2 L sample) (endpointLiftM r) h} =
      Iio ((actualField 2 L sample) (endpointLiftS r)) :=
    (cut_eq_C263 _ hcont _).trans hreal
  have hpair : h0ThresholdPair (actualField 2 L sample) (endpointLiftM r) (endpointLiftS r) :=
    ⟨hcan.1,hcan.2.1,hrealcut⟩
  have htoruscut : {h | h0OlderClearance K (actualTorusField hL.ne' sample)
      (torusProjection 2 L (endpointM r)) h} = Iio (b-k*r^3) := by
    ext a
    change h0OlderClearance K _ _ a ↔ a ∈ Iio (b-k*r^3)
    rw [h0OlderClearance_iff_strictClearance K _ (actualTorusField_continuous hL.ne' sample),
      htorus]
  refine ⟨⟨hcan,hpos,hpair⟩,hM,hS,?_,?_,htoruscut,?_⟩
  · exact (death_eq_C263 _ hcont _).trans (hdeath.trans hS)
  · exact hrealcut.trans (congrArg Iio hS)
  · exact ⟨kernel (elderRetraction (k := K) ET),hiso⟩

end I4SourceIntrinsicH0Interface
