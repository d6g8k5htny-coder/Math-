import Mathlib.LinearAlgebra.Matrix.NonsingularInverse
import Mathlib.Data.Real.Basic

/-! New scratch coordinate-change algebra only. No Kac–Rice axiom or count theorem.
The source application must separately discharge its actual covariance/row identity. -/

open Matrix
open scoped Matrix
set_option autoImplicit false

namespace ActualGeometricPalmJoin

theorem inverse_congruence {n : Type*} [Fintype n] [DecidableEq n]
    (T G : Matrix n n ℝ) (hT : IsUnit T) :
    T.transpose * (T * G * T.transpose)⁻¹ * T = G⁻¹ := by
  let _ : Invertible T := hT.invertible
  simp only [Matrix.mul_inv_rev, Matrix.mul_assoc,
    Matrix.inv_mul_of_invertible, Matrix.mul_one]
  rw [← Matrix.mul_assoc, Matrix.mul_inv_of_invertible, Matrix.one_mul]

theorem inverse_congruence_mulVec {n : Type*} [Fintype n] [DecidableEq n]
    (T G : Matrix n n ℝ) (hT : IsUnit T) (y : n → ℝ) :
    T.transpose *ᵥ ((T * G * T.transpose)⁻¹ *ᵥ (T *ᵥ y)) = G⁻¹ *ᵥ y := by
  simpa only [Matrix.mulVec_mulVec] using
    congrArg (fun A : Matrix n n ℝ => A *ᵥ y) (inverse_congruence T G hT)

theorem coefficient_lift_congr {n : Type*} [Fintype n] [DecidableEq n]
    (T G : Matrix n n ℝ) (hT : IsUnit T) (a y : n → ℝ) :
    (T *ᵥ a) ⬝ᵥ ((T * G * T.transpose)⁻¹ *ᵥ (T *ᵥ y)) = a ⬝ᵥ (G⁻¹ *ᵥ y) := by
  rw [dotProduct_comm, Matrix.dotProduct_mulVec, ← Matrix.mulVec_transpose,
    dotProduct_comm, inverse_congruence_mulVec T G hT]

#print axioms inverse_congruence
#print axioms inverse_congruence_mulVec
#print axioms coefficient_lift_congr

end ActualGeometricPalmJoin
