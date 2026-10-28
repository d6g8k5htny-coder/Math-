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
  have h := intervalIntegral.integral_sub
    (μ := volume) (a := (0 : ℝ)) (b := 1)
    (f := fun _ : ℝ => (1 : ℝ)) (g := fun t : ℝ => t)
    intervalIntegrable_const (continuous_id.intervalIntegrable (0 : ℝ) 1)
  norm_num [intervalIntegral.integral_id] at h
  exact h

private theorem taylorMatrix_zero_general (h : Point2 → ℝ) :
    taylorMatrix h 0 = (1/2 : ℝ) • hessianMatrix h := by
  ext i k
  change (∫ t : ℝ in (0 : ℝ)..1,
    (1-t) * iteratedFDeriv ℝ 2 h (t • (0 : Point2)) ![basis2 i,basis2 k]) =
    (1/2 : ℝ) * iteratedFDeriv ℝ 2 h 0 ![basis2 i,basis2 k]
  simp only [smul_zero]
  rw [intervalIntegral.integral_mul_const, taylor_weight_integral]

private theorem normalizedField_contDiff {L : ℝ} (hL : 0 < L)
    (omega : SmoothSample 2 L) (X : E2) (P : Point2 ≃L[ℝ] E2) (n : ℕ) :
    ContDiff ℝ n (normalizedField (actualField 2 L omega) X P) :=
  ((actualField_smooth 2 hL omega n).comp
    (contDiff_const.add P.contDiff)).sub contDiff_const

private theorem normalized_hessian_zero (g : E2 → ℝ) (hg : ContDiff ℝ 2 g)
    (X : E2) (P : Point2 ≃L[ℝ] E2) (u v : Point2) :
    iteratedFDeriv ℝ 2 (normalizedField g X P) 0 ![u,v] =
      iteratedFDeriv ℝ 2 g X ![P u,P v] := by
  let f : E2 → ℝ := fun z => g (X+z)-g X
  have hshiftC : ContDiff ℝ 2 (fun z : E2 => g (X+z)) :=
    hg.comp (contDiff_const.add contDiff_id)
  have hf : ContDiff ℝ 2 f := hshiftC.sub contDiff_const
  have hshift : iteratedFDeriv ℝ 2 f 0 = iteratedFDeriv ℝ 2 g X := by
    change iteratedFDeriv ℝ 2
      ((fun z : E2 => g (X+z))-(fun _ : E2 => g X)) 0 = _
    rw [iteratedFDeriv_sub_apply hshiftC.contDiffAt contDiffAt_const]
    simp only [iteratedFDeriv_const_of_ne (by norm_num : 2 ≠ 0), Pi.zero_apply, sub_zero]
    simpa only [add_zero] using (iteratedFDeriv_comp_add_left (𝕜 := ℝ) (f := g) 2 X 0)
  have hh := P.toContinuousLinearMap.iteratedFDeriv_comp_right hf (0 : Point2)
    (i := 2) (by simp)
  have he := congrArg (fun D => D (![u,v] : Fin 2 → Point2)) hh
  have hdirs : (fun i => P ((![u,v] : Fin 2 → Point2) i)) = ![P u,P v] := by
    ext i
    fin_cases i <;> rfl
  calc
    iteratedFDeriv ℝ 2 (normalizedField g X P) 0 ![u,v] =
        iteratedFDeriv ℝ 2 f 0 ![P u,P v] := by
      simpa only [normalizedField, f, Function.comp_def,
        ContinuousMultilinearMap.compContinuousLinearMap_apply,
        ContinuousLinearEquiv.coe_coe, map_zero, hdirs] using he
    _ = iteratedFDeriv ℝ 2 g X ![P u,P v] := by rw [hshift]

private theorem actual_taylorMatrix_zero {L : ℝ} (hL : 0 < L)
    (omega : SmoothSample 2 L) (X : E2) (j : ℕ)
    (P : Point2 ≃L[ℝ] E2)
    (hP : orderedNormalization (actualField 2 L omega) X j P) :
    taylorMatrix (normalizedField (actualField 2 L omega) X P) 0 = jMatrix j := by
  rw [taylorMatrix_zero_general]
  ext i k
  change (1/2 : ℝ) * iteratedFDeriv ℝ 2
    (normalizedField (actualField 2 L omega) X P) 0 ![basis2 i,basis2 k] = _
  rw [normalized_hessian_zero _ (actualField_smooth 2 hL omega 2), hP]
  fin_cases i <;> fin_cases k <;> simp [basis2, jMatrix, Fin.sum_univ_two]

/- BEGIN COMPLETE ORIGINAL HELPER A -/
/- MORSE60-FINITE2-BRANCH-SECTION-V1.
   Complete PRIVATE text for SHARED_CONTEXT60_V1 + agreed supplement A.
   Insert ONCE inside I4SourceActualMorseLocalModel after sign2/jMatrix/Mat2.
   UNCOMPILED: only the producer's final whole-module qualification covers it. -/

private def jBranchDomain (j : ℕ) : Set Mat2 :=
  {M | 0 < (jMatrix j * M).det ∧
    0 < (jMatrix j * M).trace + 2 * Real.sqrt ((jMatrix j * M).det)}

private def jBranch (j : ℕ) (M : Mat2) : Mat2 :=
  (Real.sqrt ((jMatrix j * M).trace +
      2 * Real.sqrt ((jMatrix j * M).det)))⁻¹ •
    (jMatrix j * M + Real.sqrt ((jMatrix j * M).det) • (1 : Mat2))

private theorem jBranch_sign_square (j : ℕ) (i : Fin 2) :
    sign2 j i * sign2 j i = 1 := by
  by_cases h : i.val < j <;> simp [sign2,h]

private theorem jBranch_jMatrix_square (j : ℕ) : jMatrix j * jMatrix j = 1 := by
  change Matrix.diagonal (sign2 j) * Matrix.diagonal (sign2 j) = 1
  rw [Matrix.diagonal_mul_diagonal]
  have h : (fun i : Fin 2 => sign2 j i * sign2 j i) = (1 : Fin 2 → ℝ) :=
    funext (jBranch_sign_square j)
  rw [h,Matrix.diagonal_one]

private theorem jBranch_jMatrix_transpose (j : ℕ) : (jMatrix j).transpose = jMatrix j := by
  ext i k
  by_cases h : i=k
  · subst k
    rfl
  · simp [jMatrix,Matrix.transpose_apply,Matrix.diagonal_apply,h,Ne.symm h]

private theorem jBranch_det_contDiff (j : ℕ) :
    ContDiff ℝ 1 (fun M : Mat2 => (jMatrix j * M).det) := by
  simp only [Matrix.det_fin_two,Matrix.mul_apply,Fin.sum_univ_two]
  fun_prop

private theorem jBranch_trace_contDiff (j : ℕ) :
    ContDiff ℝ 1 (fun M : Mat2 => (jMatrix j * M).trace) := by
  simp only [Matrix.trace_fin_two,Matrix.mul_apply,Fin.sum_univ_two]
  fun_prop

private theorem jBranch_product_contDiff (j : ℕ) :
    ContDiff ℝ 1 (fun M : Mat2 => jMatrix j * M) := by
  apply contDiff_pi.mpr
  intro i
  apply contDiff_pi.mpr
  intro k
  simp only [Matrix.mul_apply,Fin.sum_univ_two]
  fun_prop

private theorem jBranchDomain_isOpen (j : ℕ) : IsOpen (jBranchDomain j) := by
  have hd : Continuous (fun M : Mat2 => (jMatrix j * M).det) :=
    (jBranch_det_contDiff j).continuous
  have ht : Continuous (fun M : Mat2 => (jMatrix j * M).trace +
      2 * Real.sqrt ((jMatrix j * M).det)) :=
    (jBranch_trace_contDiff j).continuous.add
      (continuous_const.mul (Real.continuous_sqrt.comp hd))
  change IsOpen ({M : Mat2 | 0 < (jMatrix j * M).det} ∩
    {M : Mat2 | 0 < (jMatrix j * M).trace + 2 * Real.sqrt ((jMatrix j * M).det)})
  exact (isOpen_lt continuous_const hd).inter (isOpen_lt continuous_const ht)

private theorem jMatrix_mem_jBranchDomain (j : ℕ) : jMatrix j ∈ jBranchDomain j := by
  change 0 < (jMatrix j * jMatrix j).det ∧
    0 < (jMatrix j * jMatrix j).trace + 2 * Real.sqrt ((jMatrix j * jMatrix j).det)
  rw [jBranch_jMatrix_square]
  norm_num [Matrix.trace_one]

private theorem jBranch_center (j : ℕ) : jBranch j (jMatrix j) = 1 := by
  simp only [jBranch,jBranch_jMatrix_square,Matrix.det_one,Real.sqrt_one,
    Matrix.trace_one,Fintype.card_fin]
  ext i k
  by_cases h : i=k <;>
    norm_num [Matrix.smul_apply,Matrix.add_apply,Matrix.one_apply,h]

private theorem jBranch_contDiffOn (j : ℕ) :
    ContDiffOn ℝ 1 (jBranch j) (jBranchDomain j) := by
  have hd : ContDiffOn ℝ 1 (fun M : Mat2 => (jMatrix j * M).det) (jBranchDomain j) :=
    (jBranch_det_contDiff j).contDiffOn
  have hs : ContDiffOn ℝ 1 (fun M : Mat2 => Real.sqrt ((jMatrix j * M).det))
      (jBranchDomain j) :=
    hd.sqrt (fun M hM => ne_of_gt hM.1)
  have ht : ContDiffOn ℝ 1 (fun M : Mat2 => (jMatrix j * M).trace +
      2 * Real.sqrt ((jMatrix j * M).det)) (jBranchDomain j) :=
    (jBranch_trace_contDiff j).contDiffOn.add (contDiffOn_const.mul hs)
  have hroot : ContDiffOn ℝ 1 (fun M : Mat2 =>
      Real.sqrt ((jMatrix j * M).trace + 2 * Real.sqrt ((jMatrix j * M).det)))
      (jBranchDomain j) :=
    ht.sqrt (fun M hM => ne_of_gt hM.2)
  have hinv : ContDiffOn ℝ 1 (fun M : Mat2 =>
      (Real.sqrt ((jMatrix j * M).trace + 2 * Real.sqrt ((jMatrix j * M).det)))⁻¹)
      (jBranchDomain j) :=
    hroot.inv (fun M hM => (Real.sqrt_pos.mpr hM.2).ne')
  have hnum : ContDiffOn ℝ 1 (fun M : Mat2 => jMatrix j * M +
      Real.sqrt ((jMatrix j * M).det) • (1 : Mat2)) (jBranchDomain j) :=
    (jBranch_product_contDiff j).contDiffOn.add (hs.smul contDiffOn_const)
  exact hinv.smul hnum

/- The finite2 Cayley--Hamilton identity is established entry by entry.
   No eigenvalue, matrix-root or ordinary symmetry hypothesis is used. -/
private theorem jBranch_cayleyHamilton2 (Z : Mat2) :
    Z * Z + Z.det • (1 : Mat2) = Z.trace • Z := by
  ext i k
  fin_cases i <;> fin_cases k <;>
    simp only [Matrix.mul_apply,Fin.sum_univ_two,Matrix.add_apply,Matrix.smul_apply,
      smul_eq_mul,Matrix.det_fin_two,Matrix.trace_fin_two,Matrix.one_apply] <;> ring

/- For symmetric M, Z=J*M is J-self-adjoint: Z^T*J=J*Z.
   It is generally NOT ordinarily symmetric. -/
private theorem jBranch_numerator_congruence (j : ℕ) (M : Mat2)
    (hs : M.transpose=M) (s : ℝ) (hsq : s^2=(jMatrix j * M).det) :
    (jMatrix j * M + s • (1 : Mat2)).transpose * jMatrix j *
        (jMatrix j * M + s • (1 : Mat2)) =
      ((jMatrix j * M).trace + 2*s) • M := by
  let J : Mat2 := jMatrix j
  let Z : Mat2 := J*M
  let N : Mat2 := Z+s • (1 : Mat2)
  have hJJ : J*J=1 := jBranch_jMatrix_square j
  have hJt : J.transpose=J := jBranch_jMatrix_transpose j
  have hself : Z.transpose*J=J*Z := by
    change (J*M).transpose*J=J*(J*M)
    calc
      (J*M).transpose*J=(M.transpose*J.transpose)*J := by rw [Matrix.transpose_mul]
      _ = M*(J*J) := by rw [hs,hJt,Matrix.mul_assoc]
      _ = M := by rw [hJJ,Matrix.mul_one]
      _ = J*(J*M) := by rw [← Matrix.mul_assoc,hJJ,Matrix.one_mul]
  have hNself : N.transpose*J=J*N := by
    dsimp only [N]
    simp only [Matrix.transpose_add,Matrix.transpose_smul,Matrix.transpose_one,
      Matrix.add_mul,Matrix.smul_mul,Matrix.one_mul,hself,
      Matrix.mul_add,Matrix.mul_smul,Matrix.mul_one]
  have hNN : N*N=(Z*Z+s^2 • (1 : Mat2))+(2*s) • Z := by
    dsimp only [N]
    simp only [Matrix.add_mul,Matrix.mul_add,Matrix.smul_mul,Matrix.mul_smul,
      Matrix.one_mul,Matrix.mul_one,smul_smul]
    ext i k
    simp only [Matrix.add_apply,Matrix.smul_apply,smul_eq_mul]
    ring
  have hN2 : N*N=(Z.trace+2*s) • Z := by
    rw [hNN,hsq,jBranch_cayleyHamilton2,← add_smul]
  have hJM : J*Z=M := by
    dsimp only [Z]
    rw [← Matrix.mul_assoc,hJJ,Matrix.one_mul]
  change N.transpose*J*N=(Z.trace+2*s) • M
  calc
    N.transpose*J*N=(J*N)*N := by rw [hNself]
    _ = J*(N*N) := Matrix.mul_assoc _ _ _
    _ = J*((Z.trace+2*s) • Z) := by rw [hN2]
    _ = (Z.trace+2*s) • (J*Z) := Matrix.mul_smul _ _ _
    _ = (Z.trace+2*s) • M := by rw [hJM]

private theorem jBranch_congruence (j : ℕ) (M : Mat2)
    (hM : M ∈ jBranchDomain j) (hs : M.transpose = M) :
    (jBranch j M).transpose * jMatrix j * jBranch j M = M := by
  let Z : Mat2 := jMatrix j*M
  let s : ℝ := Real.sqrt Z.det
  let d : ℝ := Real.sqrt (Z.trace+2*s)
  have hdet : 0 < Z.det := hM.1
  have harg : 0 < Z.trace+2*s := hM.2
  have hsquare : s^2=Z.det := Real.sq_sqrt hdet.le
  have hdsquare : d^2=Z.trace+2*s := Real.sq_sqrt harg.le
  have hd : d ≠ 0 := (Real.sqrt_pos.mpr harg).ne'
  have hnum := jBranch_numerator_congruence j M hs s hsquare
  have hc : d⁻¹*d⁻¹*(Z.trace+2*s)=1 := by
    calc
      d⁻¹*d⁻¹*(Z.trace+2*s)=(d⁻¹*d)*(d⁻¹*d) := by rw [← hdsquare]; ring
      _ = 1 := by simp only [inv_mul_cancel₀ hd,mul_one]
  change (d⁻¹ • (Z+s • (1 : Mat2))).transpose * jMatrix j *
    (d⁻¹ • (Z+s • (1 : Mat2))) = M
  simp only [Matrix.transpose_smul,Matrix.smul_mul,Matrix.mul_smul,smul_smul]
  rw [hnum,smul_smul,hc,one_smul]

/- END COMPLETE ORIGINAL HELPER A -/

end I4SourceActualMorseLocalModel
