import SourceLifetimePairFiniteness

open MeasureTheory I4SmoothCarrier I4LifetimeField UniversalLaw.Spec.Lifetime
open I4SourceLifetimePairFiniteness

-- Deliberate false mutation: drop the endpoint criticality requirement.
-- Controls.arbitraryPair_pairSet_infinite supplies its mathematical counterexample.
example {L : ℝ} (hL : 0 < L) :
    ∀ᵐ ω ∂smoothLaw 2 L, ∀ A : Set ℝ,
      (pairSet 2 L (fun _ _ _ => True) (actualField 2 L ω) A).Finite := by
  filter_upwards [smoothLaw_ae_finite_pairSet_of_critical hL] with ω hω
  exact hω _ (fun _ _ _ => ⟨rfl, rfl⟩)
