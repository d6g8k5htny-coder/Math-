import Mathlib.Analysis.Calculus.FDeriv.Mul
import Mathlib.Analysis.Calculus.FDeriv.CompCLM
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
import Mathlib.Analysis.Matrix.Normed

/-! Actual-source C¹ quadratic local coordinates. This new application
constructs the local model from the literal criticality/inertia data.
All functional/matrix/fixture adapters are private. -/

noncomputable section
set_option autoImplicit false
open scoped BigOperators Matrix Topology
open scoped Matrix.Norms.Elementwise
attribute [local instance 1001]
  NormedAddCommGroup.toAddCommGroup AddCommGroup.toAddCommMonoid
attribute [local instance 1001]
  NormedSpace.toModule PseudoMetricSpace.toUniformSpace UniformSpace.toTopologicalSpace
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
  norm_num [integral_id] at h
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
  have hh' : iteratedFDeriv ℝ 2 (normalizedField g X P) 0 ![u,v] =
      iteratedFDeriv ℝ 2 f 0 ![P u,P v] := by
    change iteratedFDeriv ℝ 2 (fun y => f (P y)) 0 ![u,v] = _
    simpa only [Function.comp_def,
      ContinuousMultilinearMap.compContinuousLinearMap_apply,
      ContinuousLinearEquiv.coe_coe, map_zero, hdirs] using he
  exact hh'.trans (congrArg (fun D => D (![P u,P v] : Fin 2 → E2)) hshift)

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
  rw [h]
  ext i k
  by_cases hik : i = k <;> simp [Matrix.one_apply, hik]

private theorem jBranch_jMatrix_transpose (j : ℕ) : (jMatrix j).transpose = jMatrix j := by
  ext i k
  by_cases h : i=k
  · subst k
    rfl
  · simp [jMatrix,Matrix.transpose_apply,h,Ne.symm h]

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
  unfold jBranch
  rw [jBranch_jMatrix_square]
  ext i k
  change (Real.sqrt ((1 : Mat2).trace + 2 * Real.sqrt ((1 : Mat2).det)))⁻¹ *
    ((1 : Mat2) i k + Real.sqrt ((1 : Mat2).det) * (1 : Mat2) i k) = (1 : Mat2) i k
  norm_num [Matrix.trace_fin_two, Matrix.one_apply]
  have h4 : Real.sqrt (4 : ℝ) = 2 := by
    have h := Real.sqrt_sq_eq_abs (2 : ℝ)
    norm_num at h
    exact h
  rw [h4]
  by_cases hik : i = k <;> norm_num [hik]

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
    simp [Matrix.mul_apply,Fin.sum_univ_two,Matrix.add_apply,Matrix.smul_apply,
      smul_eq_mul,Matrix.det_fin_two,Matrix.trace_fin_two] <;> ring

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
      Matrix.one_mul,Matrix.mul_one]
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

/- BEGIN COMPLETE ORIGINAL HELPER B -/
/- Complete PRIVATE TEXT ONLY for one integration into
I4SourceActualMorseLocalModel under SHARED_CONTEXT60_V1 and supplement B.
No helper execution, hash or standalone qualification is claimed. -/

private def inertia60_bilin (g : E2 → ℝ) (X : E2) :
    E2 →ₗ[ℝ] E2 →ₗ[ℝ] ℝ :=
  (ContinuousLinearMap.coeLM ℝ).comp
    (fderiv ℝ (fderiv ℝ g) X).toLinearMap

private theorem inertia60_bilin_apply (g : E2 → ℝ) (X u v : E2) :
    inertia60_bilin g X u v = iteratedFDeriv ℝ 2 g X ![u,v] := by
  rw [iteratedFDeriv_two_apply]
  rfl

/-- Complementary genuine strict-sign spaces force zero radical; no coordinate pivot. -/
private theorem inertia60_separating
    (C : E2 →ₗ[ℝ] E2 →ₗ[ℝ] ℝ)
    (hs : ∀ u v, C u v = C v u) (V W : Submodule ℝ E2)
    (hc : IsCompl V W)
    (hn : ∀ v ∈ V, v ≠ 0 → C v v < 0)
    (hp : ∀ w ∈ W, w ≠ 0 → 0 < C w w) : C.SeparatingLeft := by
  intro x hx
  have hxmem : x ∈ V ⊔ W := by rw [hc.codisjoint.eq_top]; trivial
  obtain ⟨v, hv, w, hw, hvw⟩ := Submodule.mem_sup.mp hxmem
  have h1 := hx v
  have h2 := hx w
  rw [← hvw, map_add, LinearMap.add_apply] at h1 h2
  rw [hs w v] at h1
  have heq : C v v = C w w := by linarith
  have hw0 : 0 ≤ C w w := by
    by_cases hz : w = 0
    · simp [hz]
    · exact (hp w hw hz).le
  have hvzero : v = 0 := by
    by_contra hz
    have hneg := hn v hv hz
    linarith
  have hwzero : w = 0 := by
    by_contra hz
    have hpos := hp w hw hz
    rw [hvzero] at heq
    simp only [map_zero] at heq
    linarith
  simpa only [hvzero, hwzero, add_zero] using hvw.symm

private def inertia60_swap : Point2 ≃ₗ[ℝ] Point2 where
  toFun u := ![u 1,u 0]
  invFun u := ![u 1,u 0]
  left_inv u := by ext i; fin_cases i <;> rfl
  right_inv u := by ext i; fin_cases i <;> rfl
  map_add' u v := by ext i; fin_cases i <;> rfl
  map_smul' c u := by ext i; fin_cases i <;> rfl

/-- In dimension two the Sylvester signs are explicitly reordered, negative first. -/
private theorem inertia60_order_weights (w : Fin 2 → ℝ)
    (hw : ∀ i, w i = -1 ∨ w i = 1) (j : ℕ)
    (hj : ({i : Fin 2 | w i < 0} : Set (Fin 2)).ncard = j) :
    ∃ S : Point2 ≃ₗ[ℝ] Point2,
      ∀ u : Point2, (∑ i : Fin 2, w i * (S u i)^2) =
        ∑ i : Fin 2, sign2 j i * (u i)^2 := by
  classical
  rcases hw 0 with h0 | h0
  · rcases hw 1 with h1 | h1
    · have hs : {i : Fin 2 | w i < 0} = Set.univ := by
        ext i
        fin_cases i <;> simp [h0,h1]
      have hj2 : j = 2 := by simpa only [hs, Set.ncard_univ, Nat.card_fin] using hj.symm
      rw [hj2]
      refine ⟨LinearEquiv.refl ℝ Point2, ?_⟩
      intro u
      simp [Fin.sum_univ_two,sign2,h0,h1]
    · have hs : {i : Fin 2 | w i < 0} = {0} := by
        ext i
        fin_cases i <;> simp [h0,h1]
      have hj1 : j = 1 := by simpa only [hs, Set.ncard_singleton] using hj.symm
      rw [hj1]
      refine ⟨LinearEquiv.refl ℝ Point2, ?_⟩
      intro u
      simp [Fin.sum_univ_two,sign2,h0,h1]
  · rcases hw 1 with h1 | h1
    · have hs : {i : Fin 2 | w i < 0} = {1} := by
        ext i
        fin_cases i <;> simp [h0,h1]
      have hj1 : j = 1 := by simpa only [hs, Set.ncard_singleton] using hj.symm
      rw [hj1]
      refine ⟨inertia60_swap, ?_⟩
      intro u
      simp [Fin.sum_univ_two,sign2,h0,h1,inertia60_swap,add_comm]
    · have hs : {i : Fin 2 | w i < 0} = ∅ := by
        ext i
        fin_cases i <;> simp [h0,h1]
      have hj0 : j = 0 := by simpa only [hs, Set.ncard_empty] using hj.symm
      rw [hj0]
      refine ⟨LinearEquiv.refl ℝ Point2, ?_⟩
      intro u
      simp [Fin.sum_univ_two,sign2,h0,h1]

private theorem actual_ordered_normalizer {L : ℝ} (hL : 0 < L)
    (omega : SmoothSample 2 L) (X : E2) (j : ℕ)
    (hc : IsCriticalPoint 2 (actualField 2 L omega) X)
    (hi : HessianHasInertia 2 (actualField 2 L omega) X j) :
    j ≤ 2 ∧ ∃ P : Point2 ≃L[ℝ] E2,
      orderedNormalization (actualField 2 L omega) X j P := by
  classical
  have _literal_criticality := hc
  let g : E2 → ℝ := actualField 2 L omega
  let B : E2 →ₗ[ℝ] E2 →ₗ[ℝ] ℝ := inertia60_bilin g X
  let C : E2 →ₗ[ℝ] E2 →ₗ[ℝ] ℝ := (1/2 : ℝ) • B
  let Q : QuadraticForm ℝ E2 := LinearMap.BilinMap.toQuadraticMap C
  have hE : Module.finrank ℝ E2 = 2 := by simp [E2, E]
  have hB (u v : E2) : B u v = hessian 2 g X u v :=
    inertia60_bilin_apply g X u v
  have hBs : ∀ u v : E2, B u v = B v u := by
    intro u v
    exact ((actualField_smooth 2 hL omega 2).contDiffAt.isSymmSndFDerivAt
      (by simp)) u v
  have hCs : ∀ u v : E2, C u v = C v u := by
    intro u v
    change (1/2 : ℝ) * B u v = (1/2 : ℝ) * B v u
    rw [hBs]
  obtain ⟨V,W,hcompl,hVdim,_hWdim,hVneg,hWpos⟩ := hi
  have hj : j ≤ 2 := by
    calc
      j = Module.finrank ℝ V := hVdim.symm
      _ ≤ Module.finrank ℝ E2 := V.finrank_le
      _ = 2 := finrank_euclideanSpace_fin
  have hdim : j + Module.finrank ℝ W = 2 := by
    rw [← hVdim]
    exact (Submodule.finrank_add_eq_of_isCompl hcompl).trans finrank_euclideanSpace_fin
  have hneg (v : E2) (hv : v ∈ V) (hv0 : v ≠ 0) : C v v < 0 := by
    have h := hVneg v hv hv0
    change (1/2 : ℝ) * B v v < 0
    rw [hB]
    linarith
  have hpos (v : E2) (hv : v ∈ W) (hv0 : v ≠ 0) : 0 < C v v := by
    have h := hWpos v hv hv0
    change 0 < (1/2 : ℝ) * B v v
    rw [hB]
    linarith
  have hsepC : C.SeparatingLeft :=
    inertia60_separating C hCs V W hcompl hneg hpos
  have hassoc : QuadraticMap.associated Q = C :=
    QuadraticMap.associated_left_inverse (S := ℝ) hCs
  have hradical : Q.radical = ⊥ := by
    rw [QuadraticMap.radical_eq_ker_associated, hassoc]
    exact LinearMap.separatingLeft_iff_ker_eq_bot.mp hsepC
  have hsepQ : (QuadraticMap.associated Q).SeparatingLeft := by
    rw [LinearMap.separatingLeft_iff_ker_eq_bot,
      ← QuadraticMap.radical_eq_ker_associated]
    exact hradical
  have hVdef : ((-Q).restrict V).PosDef := by
    intro v hv
    change 0 < -(C (v : E2) (v : E2))
    exact neg_pos.mpr (hneg v v.property (by simpa using hv))
  have hWdef : (Q.restrict W).PosDef := by
    intro v hv
    change 0 < C (v : E2) (v : E2)
    exact hpos v v.property (by simpa using hv)
  have hLower : j ≤ sigNeg Q := by
    simpa only [hVdim] using (le_sigNeg_of_negDef Q hVdef)
  have hWnonpos : ∀ v ∈ W, (-Q) v ≤ 0 := by
    intro v hv
    by_cases hv0 : v = 0
    · simp [hv0]
    · change -(C v v) ≤ 0
      exact neg_nonpos.mpr (hpos v hv hv0).le
  have hUpper : sigNeg Q + Module.finrank ℝ W ≤ 2 := by
    simpa only [sigNeg, finrank_euclideanSpace_fin] using
      (QuadraticForm.sigPos_add_finrank_le_of_nonpos (Q := -Q) hWnonpos)
  have hIndex : sigNeg Q = j := by
    apply le_antisymm _ hLower
    have hadd : sigNeg Q + Module.finrank ℝ W ≤ j + Module.finrank ℝ W := by
      rw [hdim]
      exact hUpper
    exact Nat.le_of_add_le_add_right hadd
  obtain ⟨w,hw,he⟩ : ∃ w : Fin 2 → ℝ,
      (∀ i, w i = -1 ∨ w i = 1) ∧
        QuadraticMap.Equivalent Q (QuadraticMap.weightedSumSquares ℝ w) := by
    have hsylv := QuadraticForm.equivalent_one_neg_one_weighted_sum_squared Q hsepQ
    rw [hE] at hsylv
    exact hsylv
  have hcount : ({i : Fin 2 | w i < 0} : Set (Fin 2)).ncard = j :=
    (QuadraticForm.sigNeg_of_equiv_weightedSumSquares he).symm.trans hIndex
  obtain ⟨S,hS⟩ := inertia60_order_weights w hw j hcount
  obtain ⟨e⟩ := he
  let P : Point2 ≃L[ℝ] E2 :=
    (S.trans e.symm.toLinearEquiv).toContinuousLinearEquiv
  have hnorm (u : Point2) : Q (P u) = ∑ i : Fin 2, sign2 j i * (u i)^2 := by
    calc
      Q (P u) = (QuadraticMap.weightedSumSquares ℝ w) (S u) :=
        e.symm.map_app (S u)
      _ = ∑ i : Fin 2, w i * (S u i)^2 := by
        simp only [QuadraticMap.weightedSumSquares_apply, smul_eq_mul, pow_two]
      _ = _ := hS u
  refine ⟨hj,P,?_⟩
  intro u v
  rw [← inertia60_bilin_apply]
  have hpolar : B (P u) (P v) = Q (P (u+v)) - Q (P u) - Q (P v) := by
    change B (P u) (P v) =
      (1/2 : ℝ) * B (P (u+v)) (P (u+v)) -
        (1/2 : ℝ) * B (P u) (P u) - (1/2 : ℝ) * B (P v) (P v)
    simp only [map_add, LinearMap.add_apply]
    rw [hBs (P v) (P u)]
    ring
  calc
    B (P u) (P v) = Q (P (u+v)) - Q (P u) - Q (P v) := hpolar
    _ = 2 * ∑ i : Fin 2, sign2 j i * u i * v i := by
      rw [hnorm,hnorm,hnorm]
      simp only [Fin.sum_univ_two, Pi.add_apply]
      ring

/- END COMPLETE ORIGINAL HELPER B -/

private def parameterDerivative (F : Point2 × ℝ → ℝ) (z : Point2 × ℝ) :
    Point2 →L[ℝ] ℝ :=
  (fderiv ℝ F z).comp (ContinuousLinearMap.inl ℝ Point2 ℝ)

private theorem compact_interval_integral_c1 (F : Point2 × ℝ → ℝ)
    (hF : ContDiff ℝ 1 F) :
    ContDiff ℝ 1 (fun x : Point2 => ∫ t : ℝ in (0 : ℝ)..1, F (x,t)) := by
  let D : Point2 → ℝ → Point2 →L[ℝ] ℝ := fun x t => parameterDerivative F (x,t)
  have hD : Continuous (fun z : Point2 × ℝ => parameterDerivative F z) :=
    (hF.continuous_fderiv (by norm_num)).clm_comp continuous_const
  have hparam (x : Point2) (t : ℝ) :
      HasFDerivAt (fun y : Point2 => F (y,t)) (D x t) x := by
    have hp : HasFDerivAt (fun y : Point2 => (y,t))
        (ContinuousLinearMap.inl ℝ Point2 ℝ) x := by
      simpa using ((ContinuousLinearMap.inl ℝ Point2 ℝ).hasFDerivAt (x := x)).add_const
        ((0 : Point2), t)
    exact (hF.differentiable (by norm_num) (x,t)).hasFDerivAt.comp x hp
  have hlocal (x0 : Point2) :
      ContinuousAt (fun x : Point2 => ∫ t : ℝ in (0 : ℝ)..1, D x t) x0 ∧
      HasFDerivAt (fun x : Point2 => ∫ t : ℝ in (0 : ℝ)..1, F (x,t))
        (∫ t : ℝ in (0 : ℝ)..1, D x0 t) x0 := by
    have hcompact : IsCompact (Metric.closedBall x0 (1 : ℝ) ×ˢ Set.Icc (0 : ℝ) 1) :=
      (isCompact_closedBall x0 1).prod isCompact_Icc
    obtain ⟨C, hC⟩ := hcompact.bddAbove_image hD.norm.continuousOn
    have hbound (x : Point2) (hx : x ∈ Metric.closedBall x0 (1 : ℝ))
        (t : ℝ) (ht : t ∈ Set.Icc (0 : ℝ) 1) : ‖D x t‖ ≤ C :=
      hC ⟨(x,t), ⟨hx,ht⟩, rfl⟩
    have hnear : ∀ᶠ x in 𝓝 x0, x ∈ Metric.closedBall x0 (1 : ℝ) :=
      Metric.closedBall_mem_nhds x0 (by norm_num)
    have hDmeas (x : Point2) : AEStronglyMeasurable (D x)
        (volume.restrict (Set.uIoc (0 : ℝ) 1)) :=
      (hD.comp (continuous_const.prodMk continuous_id)).aestronglyMeasurable
    have hFmeas (x : Point2) : AEStronglyMeasurable (fun t : ℝ => F (x,t))
        (volume.restrict (Set.uIoc (0 : ℝ) 1)) :=
      (hF.continuous.comp (continuous_const.prodMk continuous_id)).aestronglyMeasurable
    have hDFbound : ∀ᶠ x in 𝓝 x0, ∀ᵐ t : ℝ ∂volume,
        t ∈ Set.uIoc (0 : ℝ) 1 → ‖D x t‖ ≤ C := by
      refine hnear.mono ?_
      intro x hx
      refine Filter.Eventually.of_forall ?_
      intro t ht
      have ht' : 0 < t ∧ t ≤ 1 := by
        simpa only [Set.uIoc_of_le zero_le_one, Set.mem_Ioc] using ht
      exact hbound x hx t ⟨ht'.1.le,ht'.2⟩
    have hcontD : ContinuousAt (fun x : Point2 => ∫ t : ℝ in (0 : ℝ)..1, D x t) x0 := by
      apply intervalIntegral.continuousAt_of_dominated_interval
        (μ := volume) (bound := fun _ => C)
        (Filter.Eventually.of_forall hDmeas) hDFbound intervalIntegrable_const
      refine Filter.Eventually.of_forall ?_
      intro t _ht
      exact (hD.comp (continuous_id.prodMk continuous_const)).continuousAt
    refine ⟨hcontD, ?_⟩
    apply intervalIntegral.hasFDerivAt_integral_of_dominated_of_fderiv_le
      (μ := volume) (F' := D) (s := Metric.ball x0 (1 : ℝ))
      (bound := fun _ => C) (Metric.ball_mem_nhds x0 (by norm_num))
      (Filter.Eventually.of_forall hFmeas)
      ((hF.continuous.comp (continuous_const.prodMk continuous_id)).intervalIntegrable 0 1)
      (hDmeas x0)
    · refine Filter.Eventually.of_forall ?_
      intro t ht x hx
      have ht' : 0 < t ∧ t ≤ 1 := by
        simpa only [Set.uIoc_of_le zero_le_one, Set.mem_Ioc] using ht
      exact hbound x (Metric.ball_subset_closedBall hx) t ⟨ht'.1.le,ht'.2⟩
    · exact intervalIntegrable_const
    · exact Filter.Eventually.of_forall (fun t _ht x _hx => hparam x t)
  exact contDiff_one_iff_hasFDerivAt.mpr
    ⟨fun x => ∫ t : ℝ in (0 : ℝ)..1, D x t,
      continuous_iff_continuousAt.mpr (fun x => (hlocal x).1), fun x => (hlocal x).2⟩

private theorem hessianEntry_contDiff (h : Point2 → ℝ) (hh : ContDiff ℝ 3 h)
    (i k : Fin 2) :
    ContDiff ℝ 1 (fun y => iteratedFDeriv ℝ 2 h y ![basis2 i,basis2 k]) := by
  have hd1 : ContDiff ℝ 2 (fderiv ℝ h) := hh.fderiv_right (by norm_num)
  have hd2 : ContDiff ℝ 1 (fderiv ℝ (fderiv ℝ h)) := hd1.fderiv_right (by norm_num)
  convert (hd2.clm_apply (contDiff_const : ContDiff ℝ 1 (fun _ : Point2 => basis2 i))).clm_apply
    (contDiff_const : ContDiff ℝ 1 (fun _ : Point2 => basis2 k)) using 1
  ext y
  simp only [iteratedFDeriv_two_apply]
  rfl

private theorem actual_taylorMatrix_contDiff {L : ℝ} (hL : 0 < L)
    (omega : SmoothSample 2 L) (X : E2) (P : Point2 ≃L[ℝ] E2) :
    ContDiff ℝ 1 (taylorMatrix (normalizedField (actualField 2 L omega) X P)) := by
  apply contDiff_pi.mpr
  intro i
  apply contDiff_pi.mpr
  intro k
  let h := normalizedField (actualField 2 L omega) X P
  have he := hessianEntry_contDiff h (normalizedField_contDiff hL omega X P 3) i k
  have harg : ContDiff ℝ 1 (fun z : Point2 × ℝ => z.2 • z.1) :=
    contDiff_snd.smul contDiff_fst
  have hF : ContDiff ℝ 1 (fun z : Point2 × ℝ =>
      (1-z.2) * iteratedFDeriv ℝ 2 h (z.2 • z.1) ![basis2 i,basis2 k]) :=
    (contDiff_const.sub contDiff_snd).mul (he.comp harg)
  exact compact_interval_integral_c1 _ hF

private theorem actual_taylorMatrix_symm {L : ℝ} (hL : 0 < L)
    (omega : SmoothSample 2 L) (X : E2) (P : Point2 ≃L[ℝ] E2) (y : Point2) :
    (taylorMatrix (normalizedField (actualField 2 L omega) X P) y).transpose =
      taylorMatrix (normalizedField (actualField 2 L omega) X P) y := by
  let h := normalizedField (actualField 2 L omega) X P
  have hh : ContDiff ℝ 2 h := normalizedField_contDiff hL omega X P 2
  ext i k
  change (∫ t : ℝ in (0 : ℝ)..1,
    (1-t) * iteratedFDeriv ℝ 2 h (t • y) ![basis2 k,basis2 i]) =
    ∫ t : ℝ in (0 : ℝ)..1,
      (1-t) * iteratedFDeriv ℝ 2 h (t • y) ![basis2 i,basis2 k]
  apply intervalIntegral.integral_congr
  intro t _ht
  have hs := ((hh.contDiffAt (x := t • y)).isSymmSndFDerivAt (by norm_num))
    (basis2 k) (basis2 i)
  simpa only [iteratedFDeriv_two_apply, Matrix.cons_val_zero, Matrix.cons_val_one] using
    congrArg (fun a : ℝ => (1-t)*a) hs

private theorem point2_decomp (y : Point2) :
    y = y 0 • basis2 0 + y 1 • basis2 1 := by
  ext i
  fin_cases i <;> simp [basis2]

private theorem bilinear_coordinates (B : Point2 →L[ℝ] Point2 →L[ℝ] ℝ)
    (u v : Point2) :
    B u v = ∑ i : Fin 2, ∑ k : Fin 2, u i * v k * B (basis2 i) (basis2 k) := by
  calc
    B u v = B (u 0 • basis2 0 + u 1 • basis2 1)
        (v 0 • basis2 0 + v 1 • basis2 1) := by
      rw [← point2_decomp u, ← point2_decomp v]
    _ = _ := by
      simp only [map_add, map_smul, add_apply,
        smul_apply, smul_eq_mul, Fin.sum_univ_two]
      ring

private theorem taylor_integral_coordinates (h : Point2 → ℝ) (hh : ContDiff ℝ 3 h)
    (y : Point2) :
    (∫ t : ℝ in (0 : ℝ)..1,
      (1-t) * iteratedFDeriv ℝ 2 h (t • y) ![y,y]) =
      ∑ i : Fin 2, ∑ k : Fin 2, y i * y k * taylorMatrix h y i k := by
  have hexp (t : ℝ) : iteratedFDeriv ℝ 2 h (t • y) ![y,y] =
      ∑ i : Fin 2, ∑ k : Fin 2,
        y i * y k * iteratedFDeriv ℝ 2 h (t • y) ![basis2 i,basis2 k] := by
    simpa only [iteratedFDeriv_two_apply, Matrix.cons_val_zero, Matrix.cons_val_one] using
      bilinear_coordinates (fderiv ℝ (fderiv ℝ h) (t • y)) y y
  have hcont (i k : Fin 2) : Continuous (fun t : ℝ =>
      y i * y k * ((1-t) * iteratedFDeriv ℝ 2 h (t • y) ![basis2 i,basis2 k]))
      := by
    exact continuous_const.mul ((continuous_const.sub continuous_id).mul
      ((hessianEntry_contDiff h hh i k).continuous.comp (continuous_id.smul continuous_const)))
  have hi (i k : Fin 2) : IntervalIntegrable (fun t : ℝ =>
      y i * y k * ((1-t) * iteratedFDeriv ℝ 2 h (t • y) ![basis2 i,basis2 k]))
      volume 0 1 := (hcont i k).intervalIntegrable 0 1
  calc
    (∫ t : ℝ in (0 : ℝ)..1,
      (1-t) * iteratedFDeriv ℝ 2 h (t • y) ![y,y]) =
        ∫ t : ℝ in (0 : ℝ)..1, ∑ i : Fin 2, ∑ k : Fin 2,
          y i * y k * ((1-t) * iteratedFDeriv ℝ 2 h (t • y) ![basis2 i,basis2 k]) := by
      apply intervalIntegral.integral_congr
      intro t _ht
      dsimp only
      rw [hexp t]
      simp only [Finset.mul_sum]
      apply Finset.sum_congr rfl
      intro i _hi
      apply Finset.sum_congr rfl
      intro k _hk
      ring
    _ = ∑ i : Fin 2, ∑ k : Fin 2, ∫ t : ℝ in (0 : ℝ)..1,
        y i * y k * ((1-t) * iteratedFDeriv ℝ 2 h (t • y) ![basis2 i,basis2 k]) := by
      rw [intervalIntegral.integral_finsetSum (fun i _ => by
        exact (continuous_finsetSum Finset.univ (fun k _ => hcont i k)).intervalIntegrable 0 1)]
      apply Finset.sum_congr rfl
      intro i _hi
      exact intervalIntegral.integral_finsetSum (fun k _ => hi i k)
    _ = _ := by
      simp only [intervalIntegral.integral_const_mul, taylorMatrix]

private theorem actual_normalized_critical {L : ℝ} (hL : 0 < L)
    (omega : SmoothSample 2 L) (X : E2) (P : Point2 ≃L[ℝ] E2)
    (hc : IsCriticalPoint 2 (actualField 2 L omega) X) :
    fderiv ℝ (normalizedField (actualField 2 L omega) X P) 0 = 0 := by
  change fderiv ℝ (fun y => actualField 2 L omega (X + P y) - actualField 2 L omega X) 0 = 0
  have hd := (((actualField_smooth 2 hL omega 1).differentiable (by norm_num)
    (X + P 0)).hasFDerivAt.comp 0 (P.hasFDerivAt.const_add X)).sub_const
      (actualField 2 L omega X)
  change fderiv ℝ (actualField 2 L omega) X = 0 at hc
  simpa only [Function.comp_def, map_zero, add_zero, hc,
    ContinuousLinearMap.zero_comp] using hd.fderiv

private theorem actual_taylor_formula {L : ℝ} (hL : 0 < L)
    (omega : SmoothSample 2 L) (X : E2) (P : Point2 ≃L[ℝ] E2)
    (hc : IsCriticalPoint 2 (actualField 2 L omega) X) (y : Point2) :
    normalizedField (actualField 2 L omega) X P y =
      ∑ i : Fin 2, ∑ k : Fin 2,
        y i * y k * taylorMatrix (normalizedField (actualField 2 L omega) X P) y i k := by
  let h := normalizedField (actualField 2 L omega) X P
  have h0 : h 0 = 0 := by simp [h, normalizedField]
  have hd0 : fderiv ℝ h 0 = 0 := actual_normalized_critical hL omega X P hc
  have ht := map_add_eq_sum_add_integral_iteratedFDeriv (f := h)
    (x := (0 : Point2)) (y := y) (n := 1)
    (fun t _ht => (normalizedField_contDiff hL omega X P 2).contDiffAt)
  norm_num [Finset.sum_range_succ, iteratedFDeriv_zero_apply,
    iteratedFDeriv_one_apply, h0, hd0] at ht
  have harray : (fun _ : Fin 2 => y) = ![y,y] := by
    ext i
    fin_cases i <;> rfl
  rw [harray] at ht
  exact ht.trans (taylor_integral_coordinates h (normalizedField_contDiff hL omega X P 3) y)

private def matrixCLM (M : Mat2) : Point2 →L[ℝ] Point2 :=
  ContinuousLinearMap.pi (fun i => ∑ k : Fin 2,
    M i k • (ContinuousLinearMap.proj k : Point2 →L[ℝ] ℝ))

private theorem matrixCLM_apply (M : Mat2) (y : Point2) :
    matrixCLM M y = M *ᵥ y := by
  ext i
  simp [matrixCLM, Matrix.mulVec, dotProduct]

private theorem matrixCLM_one : matrixCLM (1 : Mat2) = ContinuousLinearMap.id ℝ Point2 := by
  ext y i
  simp [matrixCLM, Matrix.one_apply]

private theorem matrixCLM_contDiff : ContDiff ℝ 1 matrixCLM := by
  apply contDiff_clm_apply_iff.mpr
  intro y
  apply contDiff_pi.mpr
  intro i
  simp only [matrixCLM, ContinuousLinearMap.pi_apply, sum_apply,
    smul_apply, ContinuousLinearMap.proj_apply, smul_eq_mul]
  fun_prop

private def normalizedResponse (g : E2 → ℝ) (X : E2) (j : ℕ)
    (P : Point2 ≃L[ℝ] E2) (y : Point2) : Point2 :=
  jBranch j (taylorMatrix (normalizedField g X P) y) *ᵥ y

private theorem normalizedResponse_contDiffAt {L : ℝ} (hL : 0 < L)
    (omega : SmoothSample 2 L) (X : E2) (j : ℕ) (P : Point2 ≃L[ℝ] E2)
    (hP : orderedNormalization (actualField 2 L omega) X j P) :
    ContDiffAt ℝ 1 (normalizedResponse (actualField 2 L omega) X j P) 0 := by
  let M := taylorMatrix (normalizedField (actualField 2 L omega) X P)
  have hM : ContDiff ℝ 1 M := actual_taylorMatrix_contDiff hL omega X P
  have hM0 : M 0 = jMatrix j := actual_taylorMatrix_zero hL omega X j P hP
  have hm : M 0 ∈ jBranchDomain j := hM0 ▸ jMatrix_mem_jBranchDomain j
  have hR : ContDiffAt ℝ 1 (jBranch j) (M 0) :=
    (jBranch_contDiffOn j).contDiffAt ((jBranchDomain_isOpen j).mem_nhds hm)
  have hN := matrixCLM_contDiff.contDiffAt.comp 0 (hR.comp 0 hM.contDiffAt)
  have happ := hN.clm_apply (contDiff_id.contDiffAt : ContDiffAt ℝ 1 (fun y : Point2 => y) 0)
  have hfun : normalizedResponse (actualField 2 L omega) X j P =
      fun y => ((matrixCLM ∘ jBranch j ∘ M) y) y := by
    funext y
    exact (matrixCLM_apply _ y).symm
  rw [hfun]
  exact happ

private theorem normalizedResponse_hasFDerivAt {L : ℝ} (hL : 0 < L)
    (omega : SmoothSample 2 L) (X : E2) (j : ℕ)
    (P : Point2 ≃L[ℝ] E2)
    (hc : IsCriticalPoint 2 (actualField 2 L omega) X)
    (hP : orderedNormalization (actualField 2 L omega) X j P) :
    HasFDerivAt (normalizedResponse (actualField 2 L omega) X j P)
      (ContinuousLinearMap.id ℝ Point2) 0 := by
  have _literal_criticality := hc
  let M := taylorMatrix (normalizedField (actualField 2 L omega) X P)
  let N : Point2 → Point2 →L[ℝ] Point2 := fun y => matrixCLM (jBranch j (M y))
  have hM : ContDiff ℝ 1 M := actual_taylorMatrix_contDiff hL omega X P
  have hM0 : M 0 = jMatrix j := actual_taylorMatrix_zero hL omega X j P hP
  have hm : M 0 ∈ jBranchDomain j := hM0 ▸ jMatrix_mem_jBranchDomain j
  have hR : ContDiffAt ℝ 1 (jBranch j) (M 0) :=
    (jBranch_contDiffOn j).contDiffAt ((jBranchDomain_isOpen j).mem_nhds hm)
  have hN : ContDiffAt ℝ 1 N 0 :=
    matrixCLM_contDiff.contDiffAt.comp 0 (hR.comp 0 hM.contDiffAt)
  have hN0 : N 0 = ContinuousLinearMap.id ℝ Point2 := by
    dsimp only [N]
    rw [hM0, jBranch_center, matrixCLM_one]
  have hp := (hN.differentiableAt (by norm_num)).hasFDerivAt.clm_apply
    (hasFDerivAt_id (0 : Point2))
  have hfun : normalizedResponse (actualField 2 L omega) X j P = fun y => N y y := by
    funext y
    exact (matrixCLM_apply _ y).symm
  rw [hfun]
  simpa only [id_eq, hN0, ContinuousLinearMap.comp_id, map_zero, add_zero] using hp

private def q2 (j : ℕ) (y : Point2) : ℝ :=
  ∑ i : Fin 2, sign2 j i * (y i)^2

private theorem q2_smul (j : ℕ) (a : ℝ) (y : Point2) :
    q2 j (a • y) = a^2 * q2 j y := by
  simp only [q2, Fin.sum_univ_two, Pi.smul_apply, smul_eq_mul]
  ring

private theorem cone_ball_pathConnected (j : ℕ) (r : ℝ) (hr : 0 < r) :
    IsPathConnected (Metric.ball (0 : Point2) r ∩ {y | 0 ≤ q2 j y}) := by
  have hc : StarConvex ℝ (0 : Point2) {y | 0 ≤ q2 j y} := by
    intro y hy a b _ha _hb _hab
    change 0 ≤ q2 j (a • (0 : Point2) + b • y)
    simpa only [smul_zero, zero_add, q2_smul] using mul_nonneg (sq_nonneg b) hy
  exact (((convex_ball (0 : Point2) r).starConvex (Metric.mem_ball_self hr)).inter hc).isPathConnected
    ⟨Metric.mem_ball_self hr, by simp [q2]⟩

private theorem criticalConeBasis_of_chart (g : E2 → ℝ) (X : E2) (j : ℕ)
    (phi : OpenPartialHomeomorph E2 Point2) (hx : X ∈ phi.source) (hz : phi X = 0)
    (hquad : ∀ x ∈ phi.source, g x = g X + q2 j (phi x)) :
    criticalConeBasis g X phi := by
  intro O hO hXO
  have himage : (0 : Point2) ∈ phi '' (phi.source ∩ O) := ⟨X, ⟨hx,hXO⟩, hz⟩
  obtain ⟨r, hr, hball⟩ := Metric.isOpen_iff.mp (phi.isOpen_image_source_inter hO) 0 himage
  have htarget : Metric.ball (0 : Point2) r ⊆ phi.target := by
    intro y hy
    obtain ⟨x, hxO, rfl⟩ := hball hy
    exact phi.map_source hxO.1
  let V : Set E2 := phi.symm '' Metric.ball (0 : Point2) r
  have hVopen : IsOpen V := phi.isOpen_image_symm_of_subset_target Metric.isOpen_ball htarget
  have hinv0 : phi.symm 0 = X := by
    rw [← hz]
    exact phi.left_inv hx
  have hXV : X ∈ V := by
    exact ⟨0, Metric.mem_ball_self hr, hinv0⟩
  have hVsub : V ⊆ O ∩ phi.source := by
    rintro x ⟨y,hy,rfl⟩
    obtain ⟨z,hzO,hzy⟩ := hball hy
    rw [← hzy, phi.left_inv hzO.1]
    exact ⟨hzO.2,hzO.1⟩
  have heq : V ∩ {x | g X ≤ g x} =
      phi.symm '' (Metric.ball (0 : Point2) r ∩ {y | 0 ≤ q2 j y}) := by
    ext x
    constructor
    · rintro ⟨⟨y,hy,rfl⟩,hheight⟩
      have hyt := htarget hy
      have hxs : phi.symm y ∈ phi.source := phi.map_target hyt
      have hq := hquad (phi.symm y) hxs
      rw [phi.right_inv hyt] at hq
      exact ⟨y, ⟨hy, by
        change g X ≤ g (phi.symm y) at hheight
        change 0 ≤ q2 j y
        linarith⟩, rfl⟩
    · rintro ⟨y,⟨hy,hqy⟩,rfl⟩
      have hyt := htarget hy
      have hxs : phi.symm y ∈ phi.source := phi.map_target hyt
      have hq := hquad (phi.symm y) hxs
      rw [phi.right_inv hyt] at hq
      exact ⟨⟨y,hy,rfl⟩, by
        change 0 ≤ q2 j y at hqy
        change g X ≤ g (phi.symm y)
        linarith⟩
  refine ⟨V,hVopen,hXV,hVsub,?_⟩
  rw [heq]
  exact (cone_ball_pathConnected j r hr).image'
    (phi.symm.continuousOn.mono (fun y hy => htarget hy.1))

private theorem congruence_quadratic (j : ℕ) (R M : Mat2)
    (h : R.transpose * jMatrix j * R = M) (y : Point2) :
    q2 j (R *ᵥ y) = ∑ i : Fin 2, ∑ k : Fin 2, y i * y k * M i k := by
  calc
    q2 j (R *ᵥ y) = ∑ i : Fin 2, ∑ k : Fin 2,
        y i * y k * (R.transpose * jMatrix j * R) i k := by
      simp [q2, Fin.sum_univ_two, Matrix.mulVec, dotProduct,
        Matrix.mul_apply, jMatrix, Matrix.transpose_apply]
      ring
    _ = _ := by rw [h]

private theorem normalized_localModel {L : ℝ} (hL : 0 < L)
    (omega : SmoothSample 2 L) (X : E2) (j : ℕ) (hj : j ≤ 2)
    (P : Point2 ≃L[ℝ] E2)
    (hc : IsCriticalPoint 2 (actualField 2 L omega) X)
    (hP : orderedNormalization (actualField 2 L omega) X j P) :
    ∃ phi : OpenPartialHomeomorph E2 Point2,
      localModel (actualField 2 L omega) X j phi := by
  have _index_bound := hj
  let g := actualField 2 L omega
  let M := taylorMatrix (normalizedField g X P)
  let e := normalizedResponse g X j P
  let A : E2 → Point2 := fun x => P.symm (x-X)
  let Phi : E2 → Point2 := fun x => e (A x)
  have hM : ContDiff ℝ 1 M := actual_taylorMatrix_contDiff hL omega X P
  have hM0 : M 0 = jMatrix j := actual_taylorMatrix_zero hL omega X j P hP
  have hAc : ContDiff ℝ 1 A := P.symm.contDiff.comp (contDiff_id.sub contDiff_const)
  have hA0 : A X = 0 := by simp [A]
  have he0 : e 0 = 0 := by simp [e, normalizedResponse]
  have hec : ContDiffAt ℝ 1 e 0 := normalizedResponse_contDiffAt hL omega X j P hP
  have hed : HasFDerivAt e (ContinuousLinearMap.id ℝ Point2) 0 :=
    normalizedResponse_hasFDerivAt hL omega X j P hc hP
  have hAd : HasFDerivAt A (P.symm : E2 →L[ℝ] Point2) X := by
    simpa only [A, Function.comp_def, id_eq, ContinuousLinearMap.comp_id] using
      P.symm.hasFDerivAt.comp X ((hasFDerivAt_id X).sub_const X)
  have hecA : ContDiffAt ℝ 1 e (A X) := by rw [hA0]; exact hec
  have hedA : HasFDerivAt e (ContinuousLinearMap.id ℝ Point2) (A X) := by
    rw [hA0]; exact hed
  have hPhic : ContDiffAt ℝ 1 Phi X := hecA.comp X hAc.contDiffAt
  have hPhid : HasFDerivAt Phi (P.symm : E2 →L[ℝ] Point2) X := by
    simpa only [Phi, Function.comp_def, ContinuousLinearMap.id_comp] using hedA.comp X hAd
  have hPhi0 : Phi X = 0 := by change e (A X) = 0; rw [hA0,he0]
  let psi : OpenPartialHomeomorph E2 Point2 :=
    hPhic.toOpenPartialHomeomorph Phi hPhid (by norm_num)
  have hxpsi : X ∈ psi.source :=
    hPhic.mem_toOpenPartialHomeomorph_source hPhid (by norm_num)
  have hzpsi : psi X = 0 := hPhi0
  have hypsi : (0 : Point2) ∈ psi.target := by
    rw [← hzpsi]
    exact psi.map_source hxpsi
  have hinv : psi.symm 0 = X := by
    rw [← hzpsi]
    exact psi.left_inv hxpsi
  have hinvc : ContDiffAt ℝ 1 psi.symm 0 := by
    apply psi.contDiffAt_symm hypsi (f₀' := P.symm)
    · rw [hinv]
      exact hPhid
    · rw [hinv]
      exact hPhic
  let psi1 := psi.restrContDiff ℝ 1 (by norm_num)
  have hxpsi1 : X ∈ psi1.source := by
    change X ∈ psi.source ∩
      {x | ContDiffAt ℝ 1 psi x ∧ ContDiffAt ℝ 1 psi.symm (psi x)}
    exact ⟨hxpsi,hPhic,by simpa only [hzpsi] using hinvc⟩
  have hsrcC : ContDiffOn ℝ 1 psi psi1.source :=
    psi.contDiffOn_restrContDiff_source (𝕜 := ℝ) (by norm_num)
  have htgtC : ContDiffOn ℝ 1 psi.symm psi1.target :=
    psi.contDiffOn_restrContDiff_target (𝕜 := ℝ) (by norm_num)
  let U : Set E2 := (fun x => M (A x)) ⁻¹' jBranchDomain j
  have hU : IsOpen U := (jBranchDomain_isOpen j).preimage (hM.continuous.comp hAc.continuous)
  have hXU : X ∈ U := by
    change M (A X) ∈ jBranchDomain j
    rw [hA0,hM0]
    exact jMatrix_mem_jBranchDomain j
  let phi := psi1.restr U
  have hsource : phi.source = psi1.source ∩ U := psi1.restr_source' U hU
  have hXphi : X ∈ phi.source := hsource ▸ ⟨hxpsi1,hXU⟩
  have hzero : phi X = 0 := hzpsi
  have htarget0 : (0 : Point2) ∈ phi.target := by
    rw [← hzero]
    exact phi.map_source hXphi
  have hsourceSub : phi.source ⊆ psi1.source := by
    intro x hx
    exact (hsource ▸ hx).1
  have htargetSub : phi.target ⊆ psi1.target := by
    intro y hy
    have hx := phi.map_target hy
    have hm := psi1.map_source (hsourceSub hx)
    simpa only [show (psi1 : E2 → Point2) = (phi : E2 → Point2) from rfl,
      phi.right_inv hy] using hm
  have hforward : ContDiffOn ℝ 1 phi phi.source := hsrcC.mono hsourceSub
  have hbackward : ContDiffOn ℝ 1 phi.symm phi.target := htgtC.mono htargetSub
  have hquad : ∀ x ∈ phi.source, g x = g X + q2 j (phi x) := by
    intro x hx
    have hmem : M (A x) ∈ jBranchDomain j := (hsource ▸ hx).2
    have hs : (M (A x)).transpose = M (A x) :=
      actual_taylorMatrix_symm hL omega X P (A x)
    have hcong := jBranch_congruence j (M (A x)) hmem hs
    have hq := congruence_quadratic j (jBranch j (M (A x))) (M (A x)) hcong (A x)
    have ht := actual_taylor_formula hL omega X P hc (A x)
    have hxy : X + P (A x) = x := by simp [A]
    have hval : normalizedField g X P (A x) = g x-g X := by
      unfold normalizedField
      rw [hxy]
    rw [hval] at ht
    have hresponse : phi x = jBranch j (M (A x)) *ᵥ A x := rfl
    rw [← hresponse] at hq
    linarith
  refine ⟨phi,hXphi,hzero,htarget0,hforward,hbackward,?_,?_⟩
  · intro x hx
    exact hquad x hx
  · exact criticalConeBasis_of_chart g X j phi hXphi hzero hquad

/-- The literal actual source has C¹ local quadratic coordinates and a
path-connected critical-superlevel neighborhood basis in that same chart. -/
theorem actualSource_c1_quadratic_localModel {L : ℝ} (hL : 0 < L)
    (omega : SmoothSample 2 L) (X : UniversalLaw.Spec.Lifetime.E 2) (j : ℕ)
    (hc : IsCriticalPoint 2 (actualField 2 L omega) X)
    (hi : HessianHasInertia 2 (actualField 2 L omega) X j) :
    j ≤ 2 ∧ ∃ phi : OpenPartialHomeomorph
      (UniversalLaw.Spec.Lifetime.E 2) (Fin 2 → ℝ),
      X ∈ phi.source ∧ phi X = 0 ∧ (0 : Fin 2 → ℝ) ∈ phi.target ∧
      ContDiffOn ℝ 1 phi phi.source ∧ ContDiffOn ℝ 1 phi.symm phi.target ∧
      (∀ x ∈ phi.source, actualField 2 L omega x = actualField 2 L omega X +
        ∑ i : Fin 2, (if i.val < j then (-1 : ℝ) else 1) * (phi x i)^2) ∧
      (∀ O : Set (UniversalLaw.Spec.Lifetime.E 2), IsOpen O → X ∈ O →
        ∃ V : Set (UniversalLaw.Spec.Lifetime.E 2), IsOpen V ∧ X ∈ V ∧
          V ⊆ O ∩ phi.source ∧
          IsPathConnected (V ∩ {x | actualField 2 L omega X ≤ actualField 2 L omega x})) := by
  obtain ⟨hj,P,hP⟩ := actual_ordered_normalizer hL omega X j hc hi
  obtain ⟨phi,hphi⟩ := normalized_localModel hL omega X j hj P hc hP
  refine ⟨hj,phi,?_⟩
  simpa only [localModel, criticalConeBasis, sign2] using hphi

/- BEGIN COMPLETE ORIGINAL HELPER C -/
/- Complete PRIVATE fixture text60C. Insert once inside the frozen
I4SourceActualMorseLocalModel context, after all producer interfaces.
No standalone helper execution or hashing. -/

private def fixture_axisCos (i : Fin 2) : TrigPoly :=
  [⟨1,Pi.single i 1,0⟩]

private def fixture_axisSin (i : Fin 2) : TrigPoly :=
  [⟨1,Pi.single i 1,-Real.pi/2⟩]

private def fixture_poly : Fin 4 → TrigPoly :=
  ![scale (-1) (fixture_axisCos 0 ++ fixture_axisCos 1),
    fixture_axisCos 0 ++ fixture_axisCos 1,
    fixture_axisCos 0 ++ scale (-1) (fixture_axisCos 1),
    mul (fixture_axisSin 0) (fixture_axisSin 1)]

private def fixture_sample (r : Fin 4) : SmoothSample 2 2 :=
  finiteShiftSample (toSource 2 (fixture_poly r)) (zeroSample 2 2)

private def fixture_a : Fin 4 → ℝ := ![-1,1,1,0]
private def fixture_b : Fin 4 → ℝ := ![-1,1,-1,0]
private def fixture_c : Fin 4 → ℝ := ![0,0,0,1]
private def fixture_index : Fin 4 → ℕ := ![0,2,1,1]

private def fixture_expr (a b c : ℝ) (x : Point2) : ℝ :=
  a * Real.cos (Real.pi*x 0) + b * Real.cos (Real.pi*x 1) +
    c * (Real.sin (Real.pi*x 0) * Real.sin (Real.pi*x 1))

private theorem fixture_axis_phase (i : Fin 2) (x : Point2) :
    phase 2 2 (Pi.single i 1) x = Real.pi*x i := by
  fin_cases i <;> simp [phase,I4Weights.sourceC,Fin.sum_univ_two]

private theorem fixture_axisCos_eval (i : Fin 2) (x : Point2) :
    eval 2 (fixture_axisCos i) x = Real.cos (Real.pi*x i) := by
  simp [fixture_axisCos,eval,termEval,fixture_axis_phase]

private theorem fixture_axisSin_eval (i : Fin 2) (x : Point2) :
    eval 2 (fixture_axisSin i) x = Real.sin (Real.pi*x i) := by
  simp only [fixture_axisSin,eval,List.map_cons,List.map_nil,List.sum_cons,
    List.sum_nil,termEval,one_mul,add_zero,fixture_axis_phase]
  rw [show Real.pi*x i + -Real.pi/2 = Real.pi*x i-Real.pi/2 by ring,
    Real.cos_sub]
  simp

private theorem fixture_poly_eval (r : Fin 4) (x : Point2) :
    eval 2 (fixture_poly r) x = fixture_expr (fixture_a r) (fixture_b r) (fixture_c r) x := by
  fin_cases r <;>
    simp [fixture_poly,eval_scale,eval_append,eval_mul,fixture_axisCos_eval,
      fixture_axisSin_eval,fixture_expr,fixture_a,fixture_b,fixture_c]
  all_goals ring

private theorem fixture_sample_field (r : Fin 4) :
    smoothSourceField 2 2 (fixture_sample r) = eval 2 (fixture_poly r) := by
  classical
  funext x
  rw [← toSource_eval (by norm_num : (2:ℝ) ≠ 0)]
  change (∑' m, modeCoefficient 2 2 m x *
    ((zeroSample 2 2).val m + toSource 2 (fixture_poly r) m)) = _
  simp only [zeroSample,zero_add]
  rw [tsum_eq_sum (s := (toSource 2 (fixture_poly r)).support)
    (fun m hm => by simp [Finsupp.notMem_support_iff.mp hm])]
  rfl

private theorem fixture_field_formula (r : Fin 4) :
    smoothSourceField 2 2 (fixture_sample r) =
      fixture_expr (fixture_a r) (fixture_b r) (fixture_c r) := by
  rw [fixture_sample_field]
  exact funext (fixture_poly_eval r)

private theorem fixture_original_mode_derivative (r : Fin 4) (n : ℕ)
    (x : Point2) (u : Fin n → Point2) :
    iteratedFDeriv ℝ n (smoothSourceField 2 2 (fixture_sample r)) x u =
      finitePairing (derivativeCoefficient 2 2 n x u) (toSource 2 (fixture_poly r)) := by
  rw [fixture_sample_field]
  exact (toSource_derivative (by norm_num : (2:ℝ) ≠ 0) (fixture_poly r) n x u).symm

private def fixture_proj (i : Fin 2) : Point2 →L[ℝ] ℝ := ContinuousLinearMap.proj i

private def fixture_A (a c : ℝ) (x : Point2) : ℝ :=
  (-a*Real.pi)*Real.sin (Real.pi*x 0) +
    (c*Real.pi)*(Real.cos (Real.pi*x 0)*Real.sin (Real.pi*x 1))

private def fixture_B (b c : ℝ) (x : Point2) : ℝ :=
  (-b*Real.pi)*Real.sin (Real.pi*x 1) +
    (c*Real.pi)*(Real.sin (Real.pi*x 0)*Real.cos (Real.pi*x 1))

private def fixture_D (a b c : ℝ) (x : Point2) : Point2 →L[ℝ] ℝ :=
  fixture_A a c x • fixture_proj 0 + fixture_B b c x • fixture_proj 1

private theorem fixture_expr_hasFDerivAt (a b c : ℝ) (x : Point2) :
    HasFDerivAt (fixture_expr a b c) (fixture_D a b c x) x := by
  have h0 : HasFDerivAt (fun y : Point2 => Real.pi*y 0)
      (Real.pi • fixture_proj 0) x :=
    (fixture_proj 0).hasFDerivAt.const_mul Real.pi
  have h1 : HasFDerivAt (fun y : Point2 => Real.pi*y 1)
      (Real.pi • fixture_proj 1) x :=
    (fixture_proj 1).hasFDerivAt.const_mul Real.pi
  have h := ((h0.cos.const_mul a).add (h1.cos.const_mul b)).add
    ((h0.sin.mul h1.sin).const_mul c)
  unfold fixture_expr
  convert h using 1
  ext v
  simp [fixture_D,fixture_A,fixture_B,fixture_proj]
  ring

private theorem fixture_A_hasFDerivAt_zero (a c : ℝ) :
    HasFDerivAt (fixture_A a c)
      ((-a*Real.pi^2) • fixture_proj 0 + (c*Real.pi^2) • fixture_proj 1) 0 := by
  have h0 : HasFDerivAt (fun y : Point2 => Real.pi*y 0)
      (Real.pi • fixture_proj 0) 0 :=
    (fixture_proj 0).hasFDerivAt.const_mul Real.pi
  have h1 : HasFDerivAt (fun y : Point2 => Real.pi*y 1)
      (Real.pi • fixture_proj 1) 0 :=
    (fixture_proj 1).hasFDerivAt.const_mul Real.pi
  have h := ((h0.sin.const_mul (-a*Real.pi)).add
    ((h0.cos.mul h1.sin).const_mul (c*Real.pi)))
  unfold fixture_A
  convert h using 1
  ext v
  simp [fixture_proj]
  ring

private theorem fixture_B_hasFDerivAt_zero (b c : ℝ) :
    HasFDerivAt (fixture_B b c)
      ((c*Real.pi^2) • fixture_proj 0 + (-b*Real.pi^2) • fixture_proj 1) 0 := by
  have h0 : HasFDerivAt (fun y : Point2 => Real.pi*y 0)
      (Real.pi • fixture_proj 0) 0 :=
    (fixture_proj 0).hasFDerivAt.const_mul Real.pi
  have h1 : HasFDerivAt (fun y : Point2 => Real.pi*y 1)
      (Real.pi • fixture_proj 1) 0 :=
    (fixture_proj 1).hasFDerivAt.const_mul Real.pi
  have h := ((h1.sin.const_mul (-b*Real.pi)).add
    ((h0.sin.mul h1.cos).const_mul (c*Real.pi)))
  unfold fixture_B
  convert h using 1
  ext v
  simp [fixture_proj]
  ring

private theorem fixture_expr_jet (a b c : ℝ) :
    fderiv ℝ (fixture_expr a b c) 0 = 0 ∧
      ∀ u v : Point2, iteratedFDeriv ℝ 2 (fixture_expr a b c) 0 ![u,v] =
        Real.pi^2 * (-a*u 0*v 0-b*u 1*v 1+c*(u 0*v 1+u 1*v 0)) := by
  constructor
  · rw [(fixture_expr_hasFDerivAt a b c 0).fderiv]
    simp [fixture_D,fixture_A,fixture_B]
  intro u v
  rw [iteratedFDeriv_two_apply]
  have hfun : fderiv ℝ (fixture_expr a b c) = fixture_D a b c :=
    funext fun x => (fixture_expr_hasFDerivAt a b c x).fderiv
  rw [hfun]
  have hd := ((fixture_A_hasFDerivAt_zero a c).smul_const (fixture_proj 0)).add
    ((fixture_B_hasFDerivAt_zero b c).smul_const (fixture_proj 1))
  rw [show fderiv ℝ (fixture_D a b c) 0 = _ from hd.fderiv]
  simp [fixture_proj]
  ring

private theorem fixture_critical (r : Fin 4) :
    IsCriticalPoint 2 (actualField 2 2 (fixture_sample r)) 0 := by
  have hz : fderiv ℝ (smoothSourceField 2 2 (fixture_sample r)) (coordinates 2 (0:E2)) = 0 := by
    rw [map_zero,fixture_field_formula]
    exact (fixture_expr_jet (fixture_a r) (fixture_b r) (fixture_c r)).1
  apply I4SourceActualFoldCandidate.actual_critical_of_coordinate_pins (by norm_num)
  all_goals rw [hz]; rfl

private theorem fixture_hessian (r : Fin 4) (u v : E2) :
    hessian 2 (actualField 2 2 (fixture_sample r)) 0 u v =
      Real.pi^2 * (-fixture_a r*(coordinates 2 u 0)*(coordinates 2 v 0) -
        fixture_b r*(coordinates 2 u 1)*(coordinates 2 v 1) +
        fixture_c r*((coordinates 2 u 0)*(coordinates 2 v 1)+
          (coordinates 2 u 1)*(coordinates 2 v 0))) := by
  rw [I4SourceActualFoldCandidate.actual_hessian_coordinates (by norm_num),
    map_zero,fixture_field_formula]
  exact (fixture_expr_jet (fixture_a r) (fixture_b r) (fixture_c r)).2 _ _

private theorem fixture_values_at_zero (r : Fin 4) :
    actualField 2 2 (fixture_sample r) 0 = (![-2,2,0,0] : Fin 4 → ℝ) r := by
  change smoothSourceField 2 2 (fixture_sample r) (coordinates 2 (0:E2)) = _
  rw [map_zero,fixture_field_formula]
  fin_cases r <;> norm_num [fixture_expr,fixture_a,fixture_b,fixture_c]

private def fixture_scale : ℝ := Real.sqrt 2 / Real.pi

private theorem fixture_scale_ne : fixture_scale ≠ 0 :=
  div_ne_zero (Real.sqrt_pos.mpr (by norm_num)).ne' Real.pi_ne_zero

private def fixture_scalarEquiv : Point2 ≃L[ℝ] Point2 :=
  ({ toFun := fun y => fixture_scale • y
     invFun := fun y => fixture_scale⁻¹ • y
     left_inv := by intro y; simp [smul_smul,fixture_scale_ne]
     right_inv := by intro y; simp [smul_smul,fixture_scale_ne]
     map_add' := by intro x y; simp [smul_add]
     map_smul' := by intro a y; simp [smul_smul,mul_comm] } :
    Point2 ≃ₗ[ℝ] Point2).toContinuousLinearEquiv

private def fixture_mixedEquiv : Point2 ≃L[ℝ] Point2 :=
  ({ toFun := fun y => ![(y 0+y 1)/Real.pi,(-y 0+y 1)/Real.pi]
     invFun := fun y => ![Real.pi*(y 0-y 1)/2,Real.pi*(y 0+y 1)/2]
     left_inv := by
       intro y; ext i; fin_cases i <;> simp <;> field_simp [Real.pi_ne_zero] <;> ring
     right_inv := by
       intro y; ext i; fin_cases i <;> simp <;> field_simp [Real.pi_ne_zero] <;> ring
     map_add' := by
       intro y z; ext i; fin_cases i <;> simp <;> ring
     map_smul' := by
       intro a y; ext i; fin_cases i <;> simp <;> ring } :
    Point2 ≃ₗ[ℝ] Point2).toContinuousLinearEquiv

private def fixture_P (r : Fin 4) : Point2 ≃L[ℝ] E2 :=
  (if r=3 then fixture_mixedEquiv else fixture_scalarEquiv).trans (coordinates 2).symm

private theorem fixture_P_coordinates (r : Fin 4) (y : Point2) :
    coordinates 2 (fixture_P r y) =
      if r=3 then ![(y 0+y 1)/Real.pi,(-y 0+y 1)/Real.pi]
      else fixture_scale • y := by
  by_cases hr : r = 3 <;> simp [fixture_P,hr,fixture_mixedEquiv,fixture_scalarEquiv]

private theorem fixture_ordered (r : Fin 4) :
    orderedNormalization (actualField 2 2 (fixture_sample r)) 0 (fixture_index r)
      (fixture_P r) := by
  intro u v
  change hessian 2 (actualField 2 2 (fixture_sample r)) 0 (fixture_P r u) (fixture_P r v) = _
  rw [fixture_hessian,fixture_P_coordinates,fixture_P_coordinates]
  fin_cases r <;>
    norm_num [fixture_a,fixture_b,fixture_c,fixture_index,sign2,Fin.sum_univ_two,
      fixture_scale,Real.pi_ne_zero] <;>
    field_simp [Real.pi_ne_zero] <;> ring_nf <;>
    norm_num [Real.sq_sqrt (by norm_num : (0:ℝ) ≤ 2)] <;> ring

private theorem fixture_normalized_jet (r : Fin 4) :
    normalizedField (actualField 2 2 (fixture_sample r)) 0 (fixture_P r) 0 = 0 ∧
    fderiv ℝ (normalizedField (actualField 2 2 (fixture_sample r)) 0 (fixture_P r)) 0 = 0 ∧
    ∀ u v : Point2,
      iteratedFDeriv ℝ 2
        (normalizedField (actualField 2 2 (fixture_sample r)) 0 (fixture_P r)) 0 ![u,v] =
          2 * ∑ i : Fin 2, sign2 (fixture_index r) i * u i * v i := by
  refine ⟨by simp [normalizedField],?_,?_⟩
  · exact actual_normalized_critical (by norm_num) (fixture_sample r) 0
      (fixture_P r) (fixture_critical r)
  · intro u v
    exact (normalized_hessian_zero _ (actualField_smooth 2 (by norm_num) (fixture_sample r) 2)
      0 (fixture_P r) u v).trans (fixture_ordered r u v)

private theorem fixture_point_sq_pos (y : Point2) (hy : y ≠ 0) :
    0 < (y 0)^2+(y 1)^2 := by
  have hn : y 0 ≠ 0 ∨ y 1 ≠ 0 := by
    by_contra! hh
    apply hy
    ext i
    fin_cases i <;> simp_all
  rcases hn with hn|hn
  · exact add_pos_of_pos_of_nonneg (sq_pos_of_ne_zero hn) (sq_nonneg _)
  · exact add_pos_of_nonneg_of_pos (sq_nonneg _) (sq_pos_of_ne_zero hn)

private theorem fixture_inertia_zero
    (g : E2 → ℝ) (P : Point2 ≃L[ℝ] E2)
    (hn : orderedNormalization g 0 0 P) : HessianHasInertia 2 g 0 0 := by
  refine ⟨⊥,⊤,isCompl_bot_top,by simp,by simp [E],?_,?_⟩
  · intro v hv hv0
    exact (hv0 ((Submodule.mem_bot ℝ).mp hv)).elim
  · intro v _ hv
    have hy : P.symm v ≠ 0 := by simpa using hv
    have hh := hn (P.symm v) (P.symm v)
    change hessian 2 g 0 _ _ = _ at hh
    simp only [ContinuousLinearEquiv.apply_symm_apply] at hh
    rw [hh]
    norm_num [sign2,Fin.sum_univ_two]
    nlinarith [fixture_point_sq_pos (P.symm v) hy]

private theorem fixture_inertia_two
    (g : E2 → ℝ) (P : Point2 ≃L[ℝ] E2)
    (hn : orderedNormalization g 0 2 P) : HessianHasInertia 2 g 0 2 := by
  refine ⟨⊤,⊥,isCompl_top_bot,by simp [E],by simp,?_,?_⟩
  · intro v _ hv
    have hy : P.symm v ≠ 0 := by simpa using hv
    have hh := hn (P.symm v) (P.symm v)
    change hessian 2 g 0 _ _ = _ at hh
    simp only [ContinuousLinearEquiv.apply_symm_apply] at hh
    rw [hh]
    norm_num [sign2,Fin.sum_univ_two]
    nlinarith [fixture_point_sq_pos (P.symm v) hy]
  · intro v hv hv0
    exact (hv0 ((Submodule.mem_bot ℝ).mp hv)).elim

private theorem fixture_inertia_one
    (g : E2 → ℝ) (P : Point2 ≃L[ℝ] E2)
    (hn : orderedNormalization g 0 1 P) : HessianHasInertia 2 g 0 1 := by
  let n := P (basis2 0)
  let p := P (basis2 1)
  have hn0 : n ≠ 0 := by
    intro h; have hh := congrArg P.symm h
    have h0 := congrFun hh 0
    simp [n,basis2] at h0
  have hp0 : p ≠ 0 := by
    intro h; have hh := congrArg P.symm h
    have h1 := congrFun hh 1
    simp [p,basis2] at h1
  have hnd : Module.finrank ℝ (Submodule.span ℝ {n}) = 1 := finrank_span_singleton hn0
  have hpd : Module.finrank ℝ (Submodule.span ℝ {p}) = 1 := finrank_span_singleton hp0
  have hd : Disjoint (Submodule.span ℝ {n}) (Submodule.span ℝ {p}) := by
    rw [Submodule.disjoint_def]
    intro v hv hw
    obtain ⟨a,ha⟩ := Submodule.mem_span_singleton.mp hv
    obtain ⟨b,hb⟩ := Submodule.mem_span_singleton.mp hw
    have he := congrArg (fun w => P.symm w 0) (ha.trans hb.symm)
    have ha0 : a=0 := by simpa [n,p,basis2] using he
    simpa [ha0] using ha.symm
  have hc : IsCompl (Submodule.span ℝ {n}) (Submodule.span ℝ {p}) := by
    apply (Submodule.isCompl_iff_disjoint _ _ ?_).mpr hd
    simp [E2,E,hnd,hpd]
  refine ⟨Submodule.span ℝ {n},Submodule.span ℝ {p},hc,hnd,by simpa using hpd,?_,?_⟩
  · intro v hv hv0
    obtain ⟨a,rfl⟩ := Submodule.mem_span_singleton.mp hv
    have ha : a ≠ 0 := by intro h; apply hv0; simp [h]
    have hh := hn (a • basis2 0) (a • basis2 0)
    change hessian 2 g 0 _ _ = _ at hh
    rw [show a • n = P (a • basis2 0) by simp [n]]
    rw [hh]
    norm_num [sign2,basis2,Fin.sum_univ_two]
    nlinarith [sq_pos_of_ne_zero ha]
  · intro v hv hv0
    obtain ⟨a,rfl⟩ := Submodule.mem_span_singleton.mp hv
    have ha : a ≠ 0 := by intro h; apply hv0; simp [h]
    have hh := hn (a • basis2 1) (a • basis2 1)
    change hessian 2 g 0 _ _ = _ at hh
    rw [show a • p = P (a • basis2 1) by simp [p]]
    rw [hh]
    norm_num [sign2,basis2,Fin.sum_univ_two]
    nlinarith [sq_pos_of_ne_zero ha]

private theorem fixture_inertia (r : Fin 4) :
    HessianHasInertia 2 (actualField 2 2 (fixture_sample r)) 0 (fixture_index r) := by
  fin_cases r
  · exact fixture_inertia_zero _ (fixture_P 0) (fixture_ordered 0)
  · exact fixture_inertia_two _ (fixture_P 1) (fixture_ordered 1)
  · exact fixture_inertia_one _ (fixture_P 2) (fixture_ordered 2)
  · exact fixture_inertia_one _ (fixture_P 3) (fixture_ordered 3)

private theorem fixture_true_zero_diagonal :
    hessian 2 (actualField 2 2 (fixture_sample 3)) 0
      ((coordinates 2).symm (basis2 0)) ((coordinates 2).symm (basis2 0)) = 0 ∧
    hessian 2 (actualField 2 2 (fixture_sample 3)) 0
      ((coordinates 2).symm (basis2 1)) ((coordinates 2).symm (basis2 1)) = 0 ∧
    hessian 2 (actualField 2 2 (fixture_sample 3)) 0
      ((coordinates 2).symm (basis2 0)) ((coordinates 2).symm (basis2 1)) = Real.pi^2 := by
  rw [fixture_hessian, fixture_hessian, fixture_hessian]
  simp only [ContinuousLinearEquiv.apply_symm_apply]
  norm_num [fixture_a,fixture_b,fixture_c,basis2]

private theorem fixture_consumers (r : Fin 4) :
    taylorMatrix (normalizedField (actualField 2 2 (fixture_sample r)) 0 (fixture_P r)) 0 =
      jMatrix (fixture_index r) ∧
    jBranch (fixture_index r)
      (taylorMatrix (normalizedField (actualField 2 2 (fixture_sample r)) 0 (fixture_P r)) 0) = 1 ∧
    HasFDerivAt (normalizedResponse (actualField 2 2 (fixture_sample r)) 0
      (fixture_index r) (fixture_P r)) (ContinuousLinearMap.id ℝ Point2) 0 ∧
    ∃ phi : OpenPartialHomeomorph E2 Point2,
      localModel (actualField 2 2 (fixture_sample r)) 0 (fixture_index r) phi := by
  have hc := fixture_critical r
  have hP := fixture_ordered r
  have hM := actual_taylorMatrix_zero (by norm_num : (0:ℝ)<2)
    (fixture_sample r) 0 (fixture_index r) (fixture_P r) hP
  refine ⟨hM,?_,?_,?_⟩
  · rw [hM,jBranch_center]
  · exact normalizedResponse_hasFDerivAt (by norm_num) (fixture_sample r) 0
      (fixture_index r) (fixture_P r) hc hP
  · apply normalized_localModel (by norm_num) (fixture_sample r) 0
      (fixture_index r) _ (fixture_P r) hc hP
    fin_cases r <;> norm_num [fixture_index]

private theorem fixture_same_chart_cone (r : Fin 4) :
    ∃ phi : OpenPartialHomeomorph E2 Point2,
      localModel (actualField 2 2 (fixture_sample r)) 0 (fixture_index r) phi ∧
      criticalConeBasis (actualField 2 2 (fixture_sample r)) 0 phi := by
  obtain ⟨phi,hphi⟩ := (fixture_consumers r).2.2.2
  exact ⟨phi,hphi,hphi.2.2.2.2.2.2⟩

/- Supplement C was read and ACKed before this added consumer. This is the
actual nonconstant Taylor family on its actual open branch neighborhood. -/
private theorem fixture_actual_branch_neighborhood (r : Fin 4) :
    ∃ U : Set Point2, IsOpen U ∧ (0:Point2) ∈ U ∧
      ∀ y ∈ U,
        (jBranch (fixture_index r)
          (taylorMatrix (normalizedField (actualField 2 2 (fixture_sample r)) 0 (fixture_P r)) y)).transpose *
          jMatrix (fixture_index r) *
          jBranch (fixture_index r)
            (taylorMatrix (normalizedField (actualField 2 2 (fixture_sample r)) 0 (fixture_P r)) y) =
          taylorMatrix (normalizedField (actualField 2 2 (fixture_sample r)) 0 (fixture_P r)) y := by
  let M := taylorMatrix (normalizedField (actualField 2 2 (fixture_sample r)) 0 (fixture_P r))
  have hm : Continuous M :=
    (actual_taylorMatrix_contDiff (by norm_num : (0:ℝ)<2) (fixture_sample r) 0 (fixture_P r)).continuous
  refine ⟨M ⁻¹' jBranchDomain (fixture_index r),
    (jBranchDomain_isOpen _).preimage hm,?_,?_⟩
  · change M 0 ∈ jBranchDomain (fixture_index r)
    rw [show M 0 = jMatrix (fixture_index r) from (fixture_consumers r).1]
    exact jMatrix_mem_jBranchDomain _
  · intro y hy
    exact jBranch_congruence _ _ hy
      (actual_taylorMatrix_symm (by norm_num : (0:ℝ)<2) (fixture_sample r) 0 (fixture_P r) y)

/- END COMPLETE ORIGINAL HELPER C -/

end I4SourceActualMorseLocalModel
