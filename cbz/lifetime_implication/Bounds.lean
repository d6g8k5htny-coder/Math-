import Specifications.Lifetime

/-!
Conditional logical assembly of the literal E4 statement from the literal E2
lower bound and Theorem A upper input. These are hypotheses about supplied
interfaces, not proofs of the geometric results or interface inhabitance.
-/

namespace CBZ.LifetimeBounds
open UniversalLaw.Spec.Lifetime

theorem lower_implies_twoSided (L : ℝ) (G : GaussianFieldInterface 2 L)
    (I : SuperlevelBarInterface 2 L) (PL : PairLawInterface 2 L G I)
    (bLo bHi kLo kHi : ℝ)
    (lower : PlanarElderLowerE2 L G I PL bLo bHi kLo kHi) :
    PlanarTwoSidedRateE4 L G I PL bLo bHi kLo kHi := by
  intro upper hL hb hk hkk
  obtain ⟨c, hc, rLower, hrLower, lowerBound⟩ := lower hL hb hk hkk
  obtain ⟨rUpper, hrUpper, C, upperBound⟩ :=
    upper (by norm_num) hL hb hk hkk
  refine ⟨c, hc, C, min rLower rUpper, lt_min hrLower hrUpper, ?_⟩
  intro r hr hrStar b hbmem k hkmem R
  exact ⟨lowerBound r hr (le_trans hrStar (min_le_left _ _)) b hbmem k hkmem R,
    (upperBound r hr (le_trans hrStar (min_le_right _ _)) b hbmem k hkmem R).2⟩

#print axioms lower_implies_twoSided

end CBZ.LifetimeBounds
