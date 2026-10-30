import MorseFiniteCritical

open UniversalLaw.Spec.Lifetime TorusFiltration TorusMorseFinite

-- Deliberately stronger conclusion without the required Morse hypothesis.
-- Expected rejection must concern the missing premise, not import or syntax.
example (d : ℕ) (L : ℝ) (hL : 0 < L) (g : E d → ℝ)
    (hs : IsSmooth d g) (hp : IsLPeriodic d L g) :
    (quotientCriticalSet d L hL g).Finite := by
  exact quotientCriticalSet_finite d L hL g hs hp
