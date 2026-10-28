import SourceActualFoldCandidate
import SourceFiniteTrig
import Mathlib.LinearAlgebra.QuadraticForm.Real
import Mathlib.LinearAlgebra.QuadraticForm.Signature
import Mathlib.Analysis.Calculus.TaylorIntegral
import Mathlib.Analysis.Calculus.ParametricIntervalIntegral
import Mathlib.MeasureTheory.Integral.DominatedConvergence
import Mathlib.Analysis.SpecialFunctions.Sqrt
import Mathlib.Analysis.SpecialFunctions.Integrals.Basic
import Mathlib.LinearAlgebra.Matrix.Charpoly.Coeff
import Mathlib.Analysis.Calculus.InverseFunctionTheorem.ContDiff
import Mathlib.Analysis.Calculus.ContDiff.FiniteDimension
import Mathlib.Analysis.Convex.PathConnected
import Mathlib.Topology.OpenPartialHomeomorph.IsImage
import Mathlib.Analysis.Normed.Module.FiniteDimension
import Mathlib.LinearAlgebra.QuadraticForm.Radical
import Mathlib.Analysis.Calculus.FDeriv.Symmetric
import Mathlib.Tactic.FinCases
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith

/-! Actual-source C¹ quadratic local coordinates. This new application
constructs the local model from the literal criticality/inertia data.
All functional/matrix/fixture adapters are private. -/

noncomputable section
set_option autoImplicit false
open scoped BigOperators Matrix Topology
open Set MeasureTheory I4Foundation I4Source I4Smooth I4SmoothCarrier
  I4SourceDerivativeGaussian I4SourceSmoothConditional I4SourceFinitePinKernel
  I4SourceFiniteTrig I4LifetimeField UniversalLaw.Spec.Lifetime

namespace I4SourceActualMorseLocalModel

private abbrev Point2 := Fin 2 → ℝ
private abbrev E2 := UniversalLaw.Spec.Lifetime.E 2
private abbrev Mat2 := Matrix (Fin 2) (Fin 2) ℝ
private def basis2 (i : Fin 2) : Point2 := Pi.single i 1
private def sign2 (j : ℕ) (i : Fin 2) : ℝ := if i.val < j then -1 else 1
private def jMatrix (j : ℕ) : Mat2 := Matrix.diagonal (sign2 j)

private def normalizedField (g : E2 → ℝ) (X : E2)
    (P : Point2 ≃L[ℝ] E2) (y : Point2) : ℝ := g (X + P y) - g X

private def taylorMatrix (h : Point2 → ℝ) (y : Point2) : Mat2 :=
  fun i k => ∫ t : ℝ in (0 : ℝ)..1,
    (1-t) * iteratedFDeriv ℝ 2 h (t • y) ![basis2 i,basis2 k]

private def orderedNormalization (g : E2 → ℝ) (X : E2) (j : ℕ)
    (P : Point2 ≃L[ℝ] E2) : Prop :=
  ∀ u v : Point2, iteratedFDeriv ℝ 2 g X ![P u,P v] =
    2 * ∑ i : Fin 2, sign2 j i * u i * v i

private def criticalConeBasis (g : E2 → ℝ) (X : E2)
    (phi : OpenPartialHomeomorph E2 Point2) : Prop :=
  ∀ O : Set E2, IsOpen O → X ∈ O →
    ∃ V : Set E2, IsOpen V ∧ X ∈ V ∧ V ⊆ O ∩ phi.source ∧
      IsPathConnected (V ∩ {x | g X ≤ g x})

private def localModel (g : E2 → ℝ) (X : E2) (j : ℕ)
    (phi : OpenPartialHomeomorph E2 Point2) : Prop :=
  X ∈ phi.source ∧ phi X = 0 ∧ (0 : Point2) ∈ phi.target ∧
    ContDiffOn ℝ 1 phi phi.source ∧ ContDiffOn ℝ 1 phi.symm phi.target ∧
    (∀ x ∈ phi.source, g x = g X + ∑ i : Fin 2, sign2 j i * (phi x i)^2) ∧
    criticalConeBasis g X phi

private def hessianMatrix (h : Point2 → ℝ) : Mat2 :=
  fun i k => iteratedFDeriv ℝ 2 h 0 ![basis2 i,basis2 k]

private theorem taylor_weight_integral :
    (∫ t : ℝ in (0 : ℝ)..1, (1-t)) = (1/2 : ℝ) := by
  rw [intervalIntegral.integral_sub intervalIntegrable_const intervalIntegrable_id]
  norm_num [intervalIntegral.integral_id]

private theorem taylorMatrix_zero_general (h : Point2 → ℝ) :
    taylorMatrix h 0 = (1/2 : ℝ) • hessianMatrix h := by
  ext i k
  simp only [taylorMatrix, hessianMatrix, smul_zero, Pi.smul_apply, smul_eq_mul]
  rw [intervalIntegral.integral_mul_const, taylor_weight_integral]

end I4SourceActualMorseLocalModel
