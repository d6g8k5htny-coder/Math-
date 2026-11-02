import AdaptiveFoldScalarBarrier

noncomputable section
open Set AdaptiveFoldScalar
namespace AdaptiveFoldScalarControls

/-- The exact canonical normalized fold derivative. -/
def canonicalA (x : ℝ) : ℝ := x ^ 2 - 1 / 4

def canonicalA₁ (x : ℝ) : ℝ := 2 * x

def canonicalA₂ (_ : ℝ) : ℝ := 2

def canonicalPhi (x : ℝ) : ℝ := x ^ 3 / 3 - x / 4

theorem canonicalA_jet (x : ℝ) : HasDerivAt canonicalA (canonicalA₁ x) x := by
  convert (hasDerivAt_pow 2 x).sub_const (1 / 4 : ℝ) using 1 <;> first | rfl | (unfold canonicalA₁; ring)

theorem canonicalA₁_jet (x : ℝ) : HasDerivAt canonicalA₁ (canonicalA₂ x) x := by
  convert (hasDerivAt_id x).const_mul 2 using 1 <;> first | rfl | norm_num [canonicalA₂]

theorem canonicalPhi_jet (x : ℝ) : HasDerivAt canonicalPhi (canonicalA x) x := by
  convert ((hasDerivAt_pow 3 x).div_const 3).sub
    ((hasDerivAt_id x).div_const 4) using 1 <;>
    first | rfl | (unfold canonicalA; ring)

/-- The final second-derivative theorem applies to an actual concrete profile. -/
theorem canonical_barrier : ScalarBarrier canonicalA canonicalA₁ canonicalPhi := by
  apply scalarBarrier_of_secondDerivative canonicalA canonicalA₁ canonicalA₂ canonicalPhi
  · exact fun x _ => canonicalA_jet x
  · exact fun x _ => canonicalA₁_jet x
  · intro x _; norm_num [canonicalA₂]
  · exact fun x _ => canonicalPhi_jet x
  · norm_num [canonicalA]
  · norm_num [canonicalA]
  · norm_num [canonicalPhi]

/-- Both normalized one-quarter margins are genuine consequences of the bundle. -/
theorem canonical_arm_separation :
    canonicalPhi (-(3 / 2 : ℝ)) ≤ canonicalPhi (1 / 2 : ℝ) - 1 / 4 ∧
      canonicalPhi (-(1 / 2 : ℝ)) + 1 / 4 ≤ canonicalPhi (3 / 2 : ℝ) :=
  ⟨canonical_barrier.left_barrier, canonical_barrier.right_older⟩

/-- The asymmetric ceiling has the domain required by the conventional proof. -/
theorem canonical_asymmetric_ceiling :
    ∀ x ∈ Icc (-(3 / 2 : ℝ)) (1 / 2), canonicalPhi x ≤ canonicalPhi (-(1 / 2 : ℝ)) :=
  canonical_barrier.ceiling

/-- Concrete arithmetic witness used to reject the false symmetric ceiling. -/
theorem canonical_symmetric_violation :
    canonicalPhi (-(1 / 2 : ℝ)) < canonicalPhi (3 / 2 : ℝ) := by
  norm_num [canonicalPhi]

/-- A successful positive refutation, separate from the deliberately failing mutant. -/
theorem no_full_symmetric_ceiling :
    ¬ ∀ x ∈ J, canonicalPhi x ≤ canonicalPhi (-(1 / 2 : ℝ)) := by
  intro h
  exact (not_le_of_gt canonical_symmetric_violation) (h (3 / 2) (by norm_num [J]))

end AdaptiveFoldScalarControls
