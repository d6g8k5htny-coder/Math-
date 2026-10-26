import Mathlib.Analysis.CStarAlgebra.Matrix
import Mathlib.Analysis.Calculus.ContDiff.Basic
import Mathlib.Analysis.Calculus.ContDiff.Comp
import Mathlib.Analysis.Calculus.FDeriv.CompCLM
import Mathlib.Analysis.Calculus.ContDiff.FTaylorSeries
import Mathlib.Tactic.FinCases
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Ring

noncomputable section

open Matrix WithLp

namespace I4SourcePinPreservingQuartic

-- This definition duplicates only the three-line interface from the frozen
-- norm-helper scratch. Do not copy it twice into production.
def matrixLinearEuclidean (A : Matrix (Fin 2) (Fin 2) ℝ) :
    EuclideanSpace ℝ (Fin 2) →L[ℝ] EuclideanSpace ℝ (Fin 2) :=
  Matrix.toEuclideanCLM (𝕜 := ℝ) A

def coordinateDirection (i : Fin 2) : Fin 2 → ℝ := Pi.single i 1

@[simp] theorem coordinateDirection_zero : coordinateDirection 0 = ![1,0] := by
  ext i
  fin_cases i <;> simp [coordinateDirection]

@[simp] theorem coordinateDirection_one : coordinateDirection 1 = ![0,1] := by
  ext i
  fin_cases i <;> simp [coordinateDirection]

def euclideanToPi : EuclideanSpace ℝ (Fin 2) →L[ℝ] (Fin 2 → ℝ) :=
  (PiLp.continuousLinearEquiv 2 ℝ (fun _ : Fin 2 => ℝ)).toContinuousLinearMap

def piToEuclidean : (Fin 2 → ℝ) →L[ℝ] EuclideanSpace ℝ (Fin 2) :=
  (PiLp.continuousLinearEquiv 2 ℝ (fun _ : Fin 2 => ℝ)).symm.toContinuousLinearMap

def gradientPi (f : (Fin 2 → ℝ) → ℝ) (x : Fin 2 → ℝ) : Fin 2 → ℝ :=
  fun i => fderiv ℝ f x (coordinateDirection i)

def gradientEuclidean (f : (Fin 2 → ℝ) → ℝ) (z : EuclideanSpace ℝ (Fin 2)) :
    EuclideanSpace ℝ (Fin 2) := toLp 2 (gradientPi f (ofLp z))

/-- Output coordinate is the row; domain input coordinate is the column. -/
def hessianMatrix (f : (Fin 2 → ℝ) → ℝ) (x : Fin 2 → ℝ) :
    Matrix (Fin 2) (Fin 2) ℝ :=
  fun i j => iteratedFDeriv ℝ 2 f x ![coordinateDirection j,coordinateDirection i]

theorem hessianMatrix_apply (f : (Fin 2 → ℝ) → ℝ) (x : Fin 2 → ℝ) (i j : Fin 2) :
    hessianMatrix f x i j = fderiv ℝ (fderiv ℝ f) x (coordinateDirection j) (coordinateDirection i) := by
  unfold hessianMatrix
  rw [iteratedFDeriv_succ_apply_right]
  have hi : Fin.init ![coordinateDirection j,coordinateDirection i] = ![coordinateDirection j] := by
    ext k
    fin_cases k
    rfl
  rw [hi]
  change iteratedFDeriv ℝ 1 (fderiv ℝ f) x ![coordinateDirection j]
    (coordinateDirection i) = _
  rw [iteratedFDeriv_one_apply]
  rfl

theorem coordinate_decomposition (v : Fin 2 → ℝ) :
    v = v 0 • coordinateDirection 0 + v 1 • coordinateDirection 1 := by
  ext i
  fin_cases i <;> simp [coordinateDirection]

/-- The coordinate gradient on Euclidean space differentiates to the literal
second-derivative matrix, without identifying the two ambient norms. -/
theorem hasFDerivAt_gradientEuclidean
    (f : (Fin 2 → ℝ) → ℝ) (hf : ContDiff ℝ (⊤ : ℕ∞) f)
    (z : EuclideanSpace ℝ (Fin 2)) :
    HasFDerivAt (gradientEuclidean f) (matrixLinearEuclidean (hessianMatrix f (ofLp z))) z := by
  have hdf : Differentiable ℝ (fderiv ℝ f) :=
    (hf.fderiv_right (m := (⊤ : ℕ∞)) (by simp)).differentiable (by simp)
  let D := fderiv ℝ (fderiv ℝ f) (ofLp z)
  have hraw : HasFDerivAt (gradientPi f)
      (ContinuousLinearMap.pi (fun i : Fin 2 => D.flip (coordinateDirection i))) (ofLp z) := by
    apply hasFDerivAt_pi.mpr
    intro i
    have h := (hdf (ofLp z)).hasFDerivAt.clm_apply
      (hasFDerivAt_const (coordinateDirection i) (ofLp z))
    simpa [gradientPi,D] using h
  have hE := piToEuclidean.hasFDerivAt.comp z
    (hraw.comp z euclideanToPi.hasFDerivAt)
  have hmap : matrixLinearEuclidean (hessianMatrix f (ofLp z)) =
      piToEuclidean.comp ((ContinuousLinearMap.pi
        (fun i : Fin 2 => D.flip (coordinateDirection i))).comp euclideanToPi) := by
    ext v i
    change (hessianMatrix f (ofLp z) *ᵥ ofLp v) i = D (ofLp v) (coordinateDirection i)
    rw [coordinate_decomposition (ofLp v)]
    simp [Matrix.mulVec,dotProduct,Fin.sum_univ_two,hessianMatrix_apply,D,map_add,map_smul,coordinateDirection]
    ring
  rw [hmap]
  exact hE

theorem gradientEuclidean_eq_components (f : (Fin 2 → ℝ) → ℝ)
    (z : EuclideanSpace ℝ (Fin 2)) :
    gradientEuclidean f z = toLp 2 ![fderiv ℝ f (ofLp z) ![1,0],
      fderiv ℝ f (ofLp z) ![0,1]] := by
  ext i
  fin_cases i <;> simp [gradientEuclidean,gradientPi]

def scaledGradientEuclidean (f : (Fin 2 → ℝ) → ℝ) (r : ℝ)
    (z : EuclideanSpace ℝ (Fin 2)) : EuclideanSpace ℝ (Fin 2) :=
  (r^2)⁻¹ • gradientEuclidean f (r • z)

/-- The actual scaled gradient has the literal scaled Hessian matrix as its
derivative. The chain factor r cancels one of the two value-scale factors. -/
theorem hasFDerivAt_scaledGradientEuclidean
    (f : (Fin 2 → ℝ) → ℝ) (hf : ContDiff ℝ (⊤ : ℕ∞) f)
    (r : ℝ) (hr : r ≠ 0) (z : EuclideanSpace ℝ (Fin 2)) :
    HasFDerivAt (scaledGradientEuclidean f r)
      (matrixLinearEuclidean (fun i j => hessianMatrix f (r • ofLp z) i j / r)) z := by
  have hs : HasFDerivAt (fun z : EuclideanSpace ℝ (Fin 2) => r • z)
      (r • ContinuousLinearMap.id ℝ (EuclideanSpace ℝ (Fin 2))) z := by
    exact (r • ContinuousLinearMap.id ℝ (EuclideanSpace ℝ (Fin 2))).hasFDerivAt
  have h := ((hasFDerivAt_gradientEuclidean f hf (r • z)).comp z hs).const_smul (r^2)⁻¹
  have hm : matrixLinearEuclidean (fun i j => hessianMatrix f (r • ofLp z) i j / r) =
      (r^2)⁻¹ • ((matrixLinearEuclidean (hessianMatrix f (ofLp (r • z)))).comp
        (r • ContinuousLinearMap.id ℝ (EuclideanSpace ℝ (Fin 2)))) := by
    ext v i
    change ((fun i j => hessianMatrix f (r • ofLp z) i j / r) *ᵥ ofLp v) i =
      (r^2)⁻¹ * ((hessianMatrix f (r • ofLp z)) *ᵥ (r • ofLp v)) i
    simp only [Matrix.mulVec,dotProduct,Fin.sum_univ_two,Pi.smul_apply,smul_eq_mul]
    field_simp [hr]
  rw [hm]
  exact h

theorem scaledGradientEuclidean_eq_components (f : (Fin 2 → ℝ) → ℝ)
    (r : ℝ) (z : EuclideanSpace ℝ (Fin 2)) :
    scaledGradientEuclidean f r z =
      toLp 2 ![fderiv ℝ f (r • ofLp z) ![1,0] / r^2,
        fderiv ℝ f (r • ofLp z) ![0,1] / r^2] := by
  rw [scaledGradientEuclidean,gradientEuclidean_eq_components]
  ext i
  fin_cases i <;> simp [div_eq_mul_inv,mul_comm]

end I4SourcePinPreservingQuartic
