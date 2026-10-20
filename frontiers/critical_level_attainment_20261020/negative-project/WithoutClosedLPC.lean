import CriticalLevelAttainment

/-! N1: deliberately omit the actual closed-superlevel LPC premise.
Expected result: a type mismatch showing the unconsumed LPC argument, never a
syntax/import error. This is an interface guard, not a mathematical counterexample
to the separately open implication from the literal Morse assumptions to LPC. -/

noncomputable section
open Set Topology UniversalLaw.Spec.Lifetime TorusFiltration TorusCriticalAttainment

example (d : ℕ) (L : ℝ) (hL : 0 < L)
    (g : E d → ℝ) (hsmooth : IsSmooth d g) (hperiodic : IsLPeriodic d L g)
    (hmorse : IsMorseDistinct d L g) (M : E d)
    (hnonessential : ¬ superlevelBar_isEssential g M) :
    ∃ y : E d, IsCriticalPoint d g y ∧ g M < g y ∧
      ∃ Γ : Path M y,
        (∀ t : unitInterval, superlevelBar_deathHeight g M ≤ g (Γ t)) ∧
        ∃ t : unitInterval, g (Γ t) = superlevelBar_deathHeight g M :=
  euclidean_death_attainment d L hL g hsmooth hperiodic hmorse M hnonessential
