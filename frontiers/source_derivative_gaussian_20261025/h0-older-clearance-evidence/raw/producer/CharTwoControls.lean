import SourceH0OlderClearance

open I4SourceH0OlderClearance SourceActualFoldTorus

namespace OlderClearanceCharTwoControls

instance primeTwo : Fact (Nat.Prime 2) := ⟨Nat.prime_two⟩

/-- The new equivalence also uses a concrete nontrivial characteristic-two field,
already available through the unchanged narrow import closure. -/
theorem characteristic_two_equivalence (h : ℝ) :
    h0OlderClearance (ZMod 2) (id : ℝ → ℝ) 0 h ↔
      h ∈ strictClearanceSet (id : ℝ → ℝ) 0 :=
  h0OlderClearance_iff_strictClearance (ZMod 2) _ continuous_id _ _

/-- In these coefficients, the difference used in the actual predicate is a sum. -/
theorem characteristic_two_difference (a b : ZMod 2) : a - b = a + b := by
  exact CharTwo.sub_eq_add a b

end OlderClearanceCharTwoControls
