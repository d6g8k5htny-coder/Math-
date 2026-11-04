import SourceConfluentPins
import Mathlib.LinearAlgebra.Matrix.NonsingularInverse

noncomputable section
open MeasureTheory ProbabilityTheory Matrix
open scoped BigOperators
set_option autoImplicit false

namespace ActualGeometricPalmJoin

/-- Covariance of an actual finite random vector under an actual matrix map. -/
theorem covariance_matrix_congruence {Ω n m : Type*} [MeasurableSpace Ω]
    [Fintype n] [Fintype m] [DecidableEq n] [DecidableEq m]
    (μ : Measure Ω) [IsFiniteMeasure μ] (X : Ω → n → ℝ)
    (hX : ∀ i, MemLp (fun ω => X ω i) 2 μ) (T : Matrix m n ℝ) :
    (fun i j => covariance (fun ω => (T *ᵥ X ω) i)
      (fun ω => (T *ᵥ X ω) j) μ) =
      T * (Matrix.of fun i j => covariance (fun ω => X ω i) (fun ω => X ω j) μ) * T.transpose := by
  ext i j
  simp only [Matrix.mulVec,dotProduct]
  rw [covariance_fun_sum_fun_sum (fun k => (hX k).const_mul _) (fun k => (hX k).const_mul _)]
  simp_rw [covariance_const_mul_left,covariance_const_mul_right]
  simp only [Matrix.mul_apply,Matrix.of_apply,Matrix.transpose_apply,Finset.sum_mul]
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro k _
  apply Finset.sum_congr rfl
  intro l _
  ring

/-- A nonsingular covariance congruence forces its middle matrix nonsingular.
No separate invertibility premise for the row map is necessary. -/
theorem isUnit_middle_of_congruence {n : Type*} [Fintype n] [DecidableEq n]
    (T G : Matrix n n ℝ) (h : IsUnit (T*G*T.transpose)) : IsUnit G := by
  rw [Matrix.isUnit_iff_isUnit_det,Matrix.det_mul,Matrix.det_mul,
    IsUnit.mul_iff,IsUnit.mul_iff] at h
  exact (Matrix.isUnit_iff_isUnit_det G).mpr h.1.2

end ActualGeometricPalmJoin
