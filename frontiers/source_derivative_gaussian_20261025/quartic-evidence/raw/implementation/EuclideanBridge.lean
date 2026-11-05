import Mathlib.Analysis.CStarAlgebra.Matrix
import Mathlib.Tactic.FinCases
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring

noncomputable section

open Matrix WithLp
open scoped BigOperators

namespace I4SourcePinPreservingQuartic

/-- The Pi sup norm is bounded by the actual Euclidean norm. -/
theorem pi_norm_le_euclidean_norm {ι : Type*} [Fintype ι] (v : ι → ℝ) :
    ‖v‖ ≤ ‖toLp 2 v‖ := by
  apply (pi_norm_le_iff_of_nonneg (norm_nonneg _)).mpr
  intro i
  exact PiLp.norm_apply_le (toLp 2 v) i

theorem euclidean_two_norm_sq (v : EuclideanSpace ℝ (Fin 2)) :
    ‖v‖^2 = (v 0)^2+(v 1)^2 := by
  simpa only [Fin.sum_univ_two] using EuclideanSpace.real_norm_sq_eq v

theorem euclidean_two_norm_le_abs_sum (v : EuclideanSpace ℝ (Fin 2)) :
    ‖v‖ ≤ |v 0|+|v 1| := by
  have hs := euclidean_two_norm_sq v
  have habs : 0 ≤ |v 0|+|v 1| := add_nonneg (abs_nonneg _) (abs_nonneg _)
  have hp : 0 ≤ |v 0| * |v 1| := mul_nonneg (abs_nonneg _) (abs_nonneg _)
  nlinarith [sq_abs (v 0),sq_abs (v 1),norm_nonneg v]

theorem euclidean_two_norm_le_two_mul (v : EuclideanSpace ℝ (Fin 2)) (B : ℝ)
    (h0 : |v 0| ≤ B) (h1 : |v 1| ≤ B) : ‖v‖ ≤ 2*B := by
  exact (euclidean_two_norm_le_abs_sum v).trans (by linarith)

/-- Matrix action on Euclidean space, with row=output and column=input. -/
def matrixLinearEuclidean (A : Matrix (Fin 2) (Fin 2) ℝ) :
    EuclideanSpace ℝ (Fin 2) →L[ℝ] EuclideanSpace ℝ (Fin 2) :=
  Matrix.toEuclideanCLM (𝕜 := ℝ) A

@[simp] theorem matrixLinearEuclidean_apply (A : Matrix (Fin 2) (Fin 2) ℝ)
    (v : EuclideanSpace ℝ (Fin 2)) :
    ofLp (matrixLinearEuclidean A v) = A *ᵥ ofLp v := rfl

/-- A square-sum coefficient bound controls the induced Euclidean norm. -/
theorem matrixLinearEuclidean_norm_le_of_sqsum
    (A : Matrix (Fin 2) (Fin 2) ℝ) (B : ℝ) (hB : 0 ≤ B)
    (hA : (A 0 0)^2+(A 0 1)^2+(A 1 0)^2+(A 1 1)^2 ≤ B^2) :
    ‖matrixLinearEuclidean A‖ ≤ B := by
  apply ContinuousLinearMap.opNorm_le_bound _ hB
  intro v
  have hx := euclidean_two_norm_sq v
  have hy : ‖matrixLinearEuclidean A v‖^2 =
      (A 0 0*v 0+A 0 1*v 1)^2+(A 1 0*v 0+A 1 1*v 1)^2 := by
    simpa [matrixLinearEuclidean_apply, Matrix.mulVec, dotProduct, Fin.sum_univ_two] using
      euclidean_two_norm_sq (matrixLinearEuclidean A v)
  have hc0 : (A 0 0*v 0+A 0 1*v 1)^2 ≤
      ((A 0 0)^2+(A 0 1)^2)*((v 0)^2+(v 1)^2) := by
    nlinarith [sq_nonneg (A 0 0*v 1-A 0 1*v 0)]
  have hc1 : (A 1 0*v 0+A 1 1*v 1)^2 ≤
      ((A 1 0)^2+(A 1 1)^2)*((v 0)^2+(v 1)^2) := by
    nlinarith [sq_nonneg (A 1 0*v 1-A 1 1*v 0)]
  have hp := mul_le_mul_of_nonneg_right hA (sq_nonneg ‖v‖)
  rw [hx] at hp
  have hs : ‖matrixLinearEuclidean A v‖^2 ≤ (B*‖v‖)^2 := by
    nlinarith [hc0,hc1,hp]
  exact (sq_le_sq₀ (norm_nonneg _) (mul_nonneg hB (norm_nonneg _))).mp hs

/-- Every one of four entry errors bounded by B gives the safe factor two. -/
theorem matrixLinearEuclidean_norm_le_two_mul
    (A : Matrix (Fin 2) (Fin 2) ℝ) (B : ℝ) (hB : 0 ≤ B)
    (hA : ∀ i j, |A i j| ≤ B) : ‖matrixLinearEuclidean A‖ ≤ 2*B := by
  apply matrixLinearEuclidean_norm_le_of_sqsum A (2*B) (by positivity)
  have hs (i j : Fin 2) : (A i j)^2 ≤ B^2 := by
    simpa only [sq_abs] using pow_le_pow_left₀ (abs_nonneg _) (hA i j) 2
  nlinarith [hs 0 0,hs 0 1,hs 1 0,hs 1 1]

theorem matrixLinearEuclidean_offdiag_norm_le (b : ℝ) :
    ‖matrixLinearEuclidean !![0,b;b,0]‖ ≤ |b| := by
  apply ContinuousLinearMap.opNorm_le_bound _ (abs_nonneg b)
  intro v
  have hy : ‖matrixLinearEuclidean !![0,b;b,0] v‖^2 = (b*v 1)^2+(b*v 0)^2 := by
    simpa [matrixLinearEuclidean_apply, Matrix.mulVec, dotProduct, Fin.sum_univ_two] using
      euclidean_two_norm_sq (matrixLinearEuclidean !![0,b;b,0] v)
  have heq : ‖matrixLinearEuclidean !![0,b;b,0] v‖^2 = (|b| * ‖v‖)^2 := by
    rw [hy]
    simp only [mul_pow,sq_abs,euclidean_two_norm_sq]
    ring
  exact (sq_le_sq₀ (norm_nonneg _) (mul_nonneg (abs_nonneg _) (norm_nonneg _))).mp heq.le

/-- The symmetric three-coefficient correction has the sum of its three
absolute coefficients as an induced Euclidean operator bound. -/
theorem matrixLinearEuclidean_symmetric_norm_le_abs_sum (a b c : ℝ) :
    ‖matrixLinearEuclidean !![a,b;b,c]‖ ≤ |a|+|b|+|c| := by
  have h0 : ‖matrixLinearEuclidean !![a,0;0,0]‖ ≤ |a| := by
    apply matrixLinearEuclidean_norm_le_of_sqsum _ _ (abs_nonneg _)
    norm_num [sq_abs]
  have h1 : ‖matrixLinearEuclidean !![0,0;0,c]‖ ≤ |c| := by
    apply matrixLinearEuclidean_norm_le_of_sqsum _ _ (abs_nonneg _)
    norm_num [sq_abs]
  have heq : (!![a,b;b,c] : Matrix (Fin 2) (Fin 2) ℝ) =
      !![a,0;0,0]+!![0,b;b,0]+!![0,0;0,c] := by
    ext i j
    fin_cases i <;> fin_cases j <;> simp
  rw [heq]
  simp only [matrixLinearEuclidean,map_add]
  calc
    _ ≤ ‖Matrix.toEuclideanCLM (𝕜 := ℝ) !![a,0;0,0] +
        Matrix.toEuclideanCLM (𝕜 := ℝ) !![0,b;b,0]‖ +
        ‖Matrix.toEuclideanCLM (𝕜 := ℝ) !![0,0;0,c]‖ := norm_add_le _ _
    _ ≤ ‖matrixLinearEuclidean !![a,0;0,0]‖+
        ‖matrixLinearEuclidean !![0,b;b,0]‖+
        ‖matrixLinearEuclidean !![0,0;0,c]‖ :=
      add_le_add (norm_add_le _ _) le_rfl
    _ ≤ _ := add_le_add (add_le_add h0 (matrixLinearEuclidean_offdiag_norm_le b)) h1

theorem matrixLinearEuclidean_symmetric_norm_le_three_mul (a b c B : ℝ)
    (ha : |a| ≤ B) (hb : |b| ≤ B) (hc : |c| ≤ B) :
    ‖matrixLinearEuclidean !![a,b;b,c]‖ ≤ 3*B :=
  (matrixLinearEuclidean_symmetric_norm_le_abs_sum a b c).trans (by linarith)

end I4SourcePinPreservingQuartic
