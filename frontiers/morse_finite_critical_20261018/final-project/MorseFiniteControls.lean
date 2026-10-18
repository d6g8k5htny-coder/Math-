import Lifetime

/-!
C293 mathematical negative controls, authored by OpenAI Codex /root for Dylan Roy.
These prove limitations of nearby statements. They do not establish the main
finite-quotient theorem or any stochastic/barcode assertion.
-/

noncomputable section
open UniversalLaw.Spec.Lifetime

namespace TorusMorseControls

/-- An explicitly bilinear, nonsymmetric form with a nonzero left radical. -/
def nonsymmetricForm (v w : ℝ × ℝ) : ℝ := (v.1 - v.2) * (w.1 + w.2)

theorem nonsymmetricForm_bilinear (u v w : ℝ × ℝ) (a : ℝ) :
    nonsymmetricForm (u + v) w = nonsymmetricForm u w + nonsymmetricForm v w ∧
    nonsymmetricForm u (v + w) = nonsymmetricForm u v + nonsymmetricForm u w ∧
    nonsymmetricForm (a • v) w = a * nonsymmetricForm v w ∧
    nonsymmetricForm v (a • w) = a * nonsymmetricForm v w := by
  change
    (u.1 + v.1 - (u.2 + v.2)) * (w.1 + w.2) =
      (u.1 - u.2) * (w.1 + w.2) + (v.1 - v.2) * (w.1 + w.2) ∧
    (u.1 - u.2) * (v.1 + w.1 + (v.2 + w.2)) =
      (u.1 - u.2) * (v.1 + v.2) + (u.1 - u.2) * (w.1 + w.2) ∧
    (a * v.1 - a * v.2) * (w.1 + w.2) = a * ((v.1 - v.2) * (w.1 + w.2)) ∧
    (v.1 - v.2) * (a * w.1 + a * w.2) = a * ((v.1 - v.2) * (w.1 + w.2))
  exact ⟨by ring, by ring, by ring, by ring⟩

theorem complementary_axes :
    (∀ z : ℝ × ℝ, z = (0, z.2) + (z.1, 0)) ∧
    (∀ a b : ℝ, (0, a) = (b, 0) → a = 0 ∧ b = 0) := by
  constructor
  · intro z; ext <;> simp
  · intro a b h
    exact ⟨congrArg Prod.snd h, (congrArg Prod.fst h).symm⟩

theorem nonsymmetric_signed_axes_singular :
    (∀ t : ℝ, t ≠ 0 → nonsymmetricForm (0, t) (0, t) < 0) ∧
    (∀ t : ℝ, t ≠ 0 → 0 < nonsymmetricForm (t, 0) (t, 0)) ∧
    ((1, 1) : ℝ × ℝ) ≠ 0 ∧
    (∀ w : ℝ × ℝ, nonsymmetricForm (1, 1) w = 0) ∧
    nonsymmetricForm (1, 0) (0, 1) = 1 ∧
    nonsymmetricForm (0, 1) (1, 0) = -1 := by
  constructor
  · intro t ht
    have hp : 0 < t ^ 2 := sq_pos_of_ne_zero ht
    dsimp [nonsymmetricForm]
    nlinarith
  constructor
  · intro t ht
    simpa [nonsymmetricForm, pow_two] using sq_pos_of_ne_zero ht
  norm_num [nonsymmetricForm]

/-- Literal criticality alone does not imply differentiability: fderiv defaults
to zero at a nondifferentiable point. This example is not claimed periodic. -/
theorem nonsmooth_literal_critical :
    (¬ DifferentiableAt ℝ (fun x : E 1 => ‖x‖) 0) ∧
    IsCriticalPoint 1 (fun x : E 1 => ‖x‖) 0 := by
  have h := not_differentiableAt_norm_zero (E 1)
  exact ⟨h, fderiv_zero_of_not_differentiableAt h⟩

/-- A half-open representative domain cannot supply compactness by itself. -/
theorem half_open_not_compact :
    ¬ IsCompact (Set.Ico (0 : ℝ) 1) := by
  simp

theorem closed_interval_compact : IsCompact (Set.Icc (0 : ℝ) 1) := isCompact_Icc

end TorusMorseControls
