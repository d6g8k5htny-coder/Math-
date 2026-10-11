import MorseCongruence
import DeterministicSourceC4
import Mathlib.Analysis.Calculus.TaylorIntegral
import Mathlib.Analysis.Calculus.ParametricIntegral
import Mathlib.Analysis.Calculus.FDeriv.Symmetric
import Mathlib.Analysis.Normed.Group.Bounded
import Mathlib.Analysis.SpecialFunctions.Integrals.Basic

noncomputable section
set_option backward.isDefEq.respectTransparency false
open MeasureTheory Filter Set
open scoped Topology ContDiff Matrix.Norms.Frobenius
namespace TaylorMatrix
abbrev E (n : ℕ) := EuclideanSpace ℝ (Fin n)
abbrev X (n : ℕ) := Fin n → ℝ

def matrix {n : ℕ} (F : X n → ℝ) (x0 : X n) (P : E n →L[ℝ] X n)
    (u : E n) : MorseCongruence.Mat n := fun i j =>
  ∫ t in (0 : ℝ)..1, (1-t) * iteratedFDeriv ℝ 2 F (x0+t • P u)
    ![P (EuclideanSpace.single i 1), P (EuclideanSpace.single j 1)]

section ParameterIntegral
variable {H B : Type*} [NormedAddCommGroup H] [NormedSpace ℝ H]
  [FiniteDimensional ℝ H] [NormedAddCommGroup B] [NormedSpace ℝ B] [CompleteSpace B]

omit [CompleteSpace B] in
private theorem integral_deriv (G : H × ℝ → B) (D : H × ℝ → H →L[ℝ] B)
    (hG : Continuous G) (hD : Continuous D)
    (hd : ∀ u t, HasFDerivAt (fun v => G (v,t)) (D (u,t)) u) (u0 : H) :
    HasFDerivAt (fun u => ∫ t in (0 : ℝ)..1, G (u,t))
      (∫ t in (0 : ℝ)..1, D (u0,t)) u0 := by
  obtain ⟨C,hC⟩ := ((isCompact_closedBall u0 1).prod (isCompact_Icc : IsCompact (Icc (0:ℝ) 1))).exists_bound_of_continuousOn hD.continuousOn
  apply hasFDerivAt_integral_of_dominated_of_fderiv_le'' (s := Metric.ball u0 1)
    (bound := fun _ => C) (Metric.ball_mem_nhds u0 (by norm_num))
  · exact Eventually.of_forall (fun u => (hG.comp (continuous_const.prodMk continuous_id)).aestronglyMeasurable)
  · exact (hG.comp (continuous_const.prodMk continuous_id)).intervalIntegrable 0 1
  · exact (hD.comp (continuous_const.prodMk continuous_id)).aestronglyMeasurable
  · filter_upwards [ae_restrict_mem measurableSet_uIoc] with t ht
    intro u hu
    exact hC (u,t) ⟨Metric.ball_subset_closedBall hu, (by simpa [uIcc_of_le zero_le_one] using uIoc_subset_uIcc ht)⟩
  · exact intervalIntegrable_const
  · exact Eventually.of_forall (fun t u _ => hd u t)

private def partialD (G : H × ℝ → B) (p : H × ℝ) : H →L[ℝ] B :=
  (fderiv ℝ G p).comp (ContinuousLinearMap.inl ℝ H ℝ)

omit [FiniteDimensional ℝ H] [CompleteSpace B] in
private theorem partialD_contDiff {G : H × ℝ → B} {k : ℕ}
    (hG : ContDiff ℝ (k+1) G) : ContDiff ℝ k (partialD G) := by
  exact (hG.fderiv_right (by simp)).clm_comp contDiff_const

omit [FiniteDimensional ℝ H] [CompleteSpace B] in
private theorem partialD_deriv {G : H × ℝ → B} {k : ℕ}
    (hG : ContDiff ℝ (k+1) G) (u : H) (t : ℝ) :
    HasFDerivAt (fun v => G (v,t)) (partialD G (u,t)) u := by
  exact ((hG.differentiable (by simp) (u,t)).hasFDerivAt).comp u (hasFDerivAt_prodMk_left u t)

omit [CompleteSpace B] in
private theorem integral_continuous {G : H × ℝ → B} (hG : Continuous G) :
    Continuous (fun u => ∫ t in (0:ℝ)..1, G (u,t)) := by
  apply continuous_iff_continuousAt.mpr
  intro u0
  obtain ⟨C,hC⟩ := ((isCompact_closedBall u0 1).prod (isCompact_Icc : IsCompact (Icc (0:ℝ) 1))).exists_bound_of_continuousOn hG.continuousOn
  apply intervalIntegral.continuousAt_of_dominated_interval (bound := fun _ => C)
  · exact Eventually.of_forall (fun u => (hG.comp (continuous_const.prodMk continuous_id)).aestronglyMeasurable)
  · filter_upwards [Metric.ball_mem_nhds u0 (by norm_num : (0:ℝ)<1)] with u hu
    exact Eventually.of_forall (fun t ht => hC (u,t)
      ⟨Metric.ball_subset_closedBall hu, by simpa [uIcc_of_le zero_le_one] using uIoc_subset_uIcc ht⟩)
  · exact intervalIntegrable_const
  · exact Eventually.of_forall (fun t _ => (hG.comp (continuous_id.prodMk continuous_const)).continuousAt)

omit [CompleteSpace B] in
private theorem integral_contDiff_one {G : H × ℝ → B} (hG : ContDiff ℝ 1 G) :
    ContDiff ℝ 1 (fun u => ∫ t in (0:ℝ)..1, G (u,t)) := by
  apply contDiff_one_iff_hasFDerivAt.mpr
  refine ⟨fun u => ∫ t in (0:ℝ)..1, partialD G (u,t), ?_, ?_⟩
  · exact integral_continuous (partialD_contDiff (k := 0) hG).continuous
  · intro u
    exact integral_deriv G (partialD G) hG.continuous
      ((partialD_contDiff (k := 0) hG).continuous) (partialD_deriv (k := 0) hG) u

omit [CompleteSpace B] in
private theorem integral_contDiff_two {G : H × ℝ → B} (hG : ContDiff ℝ 2 G) :
    ContDiff ℝ 2 (fun u => ∫ t in (0:ℝ)..1, G (u,t)) := by
  apply (contDiff_succ_iff_hasFDerivAt (n := 1)).mpr
  refine ⟨fun u => ∫ t in (0:ℝ)..1, partialD G (u,t), ?_, ?_⟩
  · exact integral_contDiff_one (partialD_contDiff (k := 1) hG)
  · intro u
    exact integral_deriv G (partialD G) hG.continuous
      ((partialD_contDiff (k := 1) hG).continuous) (partialD_deriv (k := 1) hG) u
end ParameterIntegral

private def assemble (n : ℕ) : ((Fin n × Fin n) → ℝ) →L[ℝ] MorseCongruence.Mat n :=
  (show ((Fin n × Fin n) → ℝ) →ₗ[ℝ] MorseCongruence.Mat n from
    { toFun := fun a i j => a (i,j)
      map_add' := by intros; rfl
      map_smul' := by intros; rfl }).toContinuousLinearMap

theorem matrix_contDiff {n : ℕ} {F : X n → ℝ} (hF : ContDiff ℝ 4 F)
    (x0 : X n) (P : E n →L[ℝ] X n) : ContDiff ℝ 2 (matrix F x0 P) := by
  have he : ContDiff ℝ 2 (fun u : E n => fun ij : Fin n × Fin n => matrix F x0 P u ij.1 ij.2) := by
    apply contDiff_pi.mpr
    intro ij
    rcases ij with ⟨i,j⟩
    change ContDiff ℝ 2 (fun u => ∫ t in (0:ℝ)..1, (1-t)*iteratedFDeriv ℝ 2 F (x0+t • P u) ![P (EuclideanSpace.single i 1),P (EuclideanSpace.single j 1)])
    apply integral_contDiff_two (G := fun q : E n × ℝ => (1-q.2)*iteratedFDeriv ℝ 2 F (x0+q.2 • P q.1) ![P (EuclideanSpace.single i 1),P (EuclideanSpace.single j 1)])
    have hD : ContDiff ℝ 2 (iteratedFDeriv ℝ 2 F) := hF.iteratedFDeriv_right (by norm_num)
    have hx : ContDiff ℝ 2 (fun q : E n × ℝ => x0 + q.2 • P q.1) := by fun_prop
    have hev : ContDiff ℝ 2 (ContinuousMultilinearMap.apply ℝ (fun _ : Fin 2 => X n) ℝ
      ![P (EuclideanSpace.single i 1),P (EuclideanSpace.single j 1)]) := (ContinuousMultilinearMap.apply ℝ (fun _ : Fin 2 => X n) ℝ
      ![P (EuclideanSpace.single i 1),P (EuclideanSpace.single j 1)]).contDiff
    exact (contDiff_const.sub contDiff_snd).mul (hev.comp (hD.comp hx))

  exact (assemble n).contDiff.comp he

private theorem expansion {n : ℕ} (P : E n →L[ℝ] X n) (u : E n) :
    P u = ∑ i, u i • P (EuclideanSpace.single i 1) := by
  have hu : (∑ i, u i • EuclideanSpace.single i (1:ℝ)) = u := by
    apply PiLp.ext
    intro k
    simp [WithLp.ofLp_sum, Pi.single_apply, Finset.sum_apply]
  calc
    P u = P (∑ i, u i • EuclideanSpace.single i (1:ℝ)) := congrArg P hu.symm
    _ = _ := by rw [map_sum]; simp

private theorem bilinear_expansion {n : ℕ} (P : E n →L[ℝ] X n) (u : E n)
    (B : X n →L[ℝ] X n →L[ℝ] ℝ) :
    B (P u) (P u) = ∑ i, ∑ j, u i * B (P (EuclideanSpace.single i 1))
      (P (EuclideanSpace.single j 1)) * u j := by
  rw [expansion P u]
  simp only [map_sum, map_smul, sum_apply, smul_apply, smul_eq_mul]
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro i hi
  rw [Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro j hj
  ring

theorem matrix_quadratic {n : ℕ} {F : X n → ℝ} (hF : ContDiff ℝ 4 F)
    (x0 : X n) (P : E n →L[ℝ] X n) (hcrit : fderiv ℝ F x0 = 0) (u : E n) :
    F (x0+P u) = F x0 + ∑ i, ∑ j, u i * matrix F x0 P u i j * u j := by
  have ht := map_add_eq_sum_add_integral_iteratedFDeriv (n := 1)
    (x := x0) (y := P u) (fun t _ => hF.contDiffAt.of_le (by norm_num))
  simp only [Finset.sum_range_succ, Finset.sum_range_zero, zero_add,
    Nat.factorial_zero, Nat.factorial_one, Nat.cast_one, inv_one,
    iteratedFDeriv_zero_apply, iteratedFDeriv_one_apply, hcrit, zero_apply,
    add_zero, pow_one, smul_eq_mul, one_mul, mul_zero] at ht
  rw [ht]
  congr 1
  have hint (i j : Fin n) : IntervalIntegrable
      (fun t => u i * ((1-t)*iteratedFDeriv ℝ 2 F (x0+t • P u)
        ![P (EuclideanSpace.single i 1),P (EuclideanSpace.single j 1)]) * u j) volume 0 1 := by
    have hD : Continuous (iteratedFDeriv ℝ 2 F) :=
      (hF.iteratedFDeriv_right (m := 0) (by norm_num)).continuous
    apply Continuous.intervalIntegrable
    fun_prop
  calc
    (∫ t in (0:ℝ)..1, (1-t)*iteratedFDeriv ℝ 2 F (x0+t • P u) (fun _ => P u)) =
      ∫ t in (0:ℝ)..1, ∑ i, ∑ j, u i * ((1-t)*iteratedFDeriv ℝ 2 F (x0+t • P u)
        ![P (EuclideanSpace.single i 1),P (EuclideanSpace.single j 1)]) * u j := by
          apply intervalIntegral.integral_congr
          intro t ht
          simp only [iteratedFDeriv_two_apply, Matrix.cons_val_zero, Matrix.cons_val_one]
          rw [bilinear_expansion P u]
          simp only [Finset.mul_sum]
          apply Finset.sum_congr rfl
          intro i hi
          apply Finset.sum_congr rfl
          intro j hj
          ring
    _ = ∑ i, ∑ j, u i * matrix F x0 P u i j * u j := by
      rw [intervalIntegral.integral_finsetSum (s := Finset.univ)
        (f := fun i t => ∑ j, u i * ((1-t)*iteratedFDeriv ℝ 2 F (x0+t • P u)
          ![P (EuclideanSpace.single i 1),P (EuclideanSpace.single j 1)]) * u j)
        (fun i _ => by
          convert IntervalIntegrable.sum Finset.univ (fun j _ => hint i j) using 1
          ext t
          simp only [Finset.sum_apply])]
      apply Finset.sum_congr rfl
      intro i hi
      rw [intervalIntegral.integral_finsetSum (s := Finset.univ)
        (f := fun j t => u i * ((1-t)*iteratedFDeriv ℝ 2 F (x0+t • P u)
          ![P (EuclideanSpace.single i 1),P (EuclideanSpace.single j 1)]) * u j)
        (fun j _ => hint i j)]
      apply Finset.sum_congr rfl
      intro j hj
      simp only [intervalIntegral.integral_mul_const, intervalIntegral.integral_const_mul, matrix]

theorem source_matrix_contDiff {n : ℕ} {L : ℝ} (hL : L ≠ 0)
    (omega : I4Source.SourceMode n → ℝ)
    (hmajor : Summable (fun m => I4Source.modeMajorant n L m * |omega m|))
    (x0 : X n) (P : E n →L[ℝ] X n) :
    ContDiff ℝ 2 (matrix (I4Source.sourceField n L omega) x0 P) := by
  exact matrix_contDiff (I4DeterministicC4.sourceField_contDiff_of_majorant n hL omega hmajor) x0 P

theorem source_matrix_selfAdjoint {n : ℕ} {L : ℝ} (hL : L ≠ 0)
    (omega : I4Source.SourceMode n → ℝ)
    (hmajor : Summable (fun m => I4Source.modeMajorant n L m * |omega m|))
    (x0 : X n) (P : E n →L[ℝ] X n) (u : E n) :
    IsSelfAdjoint (matrix (I4Source.sourceField n L omega) x0 P u) := by
  have hf := I4DeterministicC4.sourceField_contDiff_of_majorant n hL omega hmajor
  change star (matrix (I4Source.sourceField n L omega) x0 P u) = _
  ext i j
  simp only [Matrix.star_apply, star_trivial]
  apply intervalIntegral.integral_congr
  intro t ht
  exact congrArg (fun a : ℝ => (1-t)*a) ((hf.contDiffAt.isSymmSndFDerivAt (by norm_num)).iteratedFDeriv_cons)

theorem source_matrix_zero {n : ℕ} {L : ℝ} (hL : L ≠ 0)
    (omega : I4Source.SourceMode n → ℝ)
    (hmajor : Summable (fun m => I4Source.modeMajorant n L m * |omega m|))
    (x0 : X n) (P : E n →L[ℝ] X n) (i j : Fin n) :
    matrix (I4Source.sourceField n L omega) x0 P 0 i j =
      (1/2 : ℝ) * iteratedFDeriv ℝ 2 (I4Source.sourceField n L omega) x0
        ![P (EuclideanSpace.single i 1), P (EuclideanSpace.single j 1)] := by
  clear hL hmajor
  simp only [matrix, map_zero, smul_zero, add_zero]
  rw [intervalIntegral.integral_mul_const]
  congr 1
  rw [intervalIntegral.integral_sub (f := fun _ : ℝ => (1:ℝ)) (g := fun t : ℝ => t) intervalIntegrable_const (continuous_id.intervalIntegrable 0 1)]
  norm_num [integral_id]

theorem source_matrix_quadratic {n : ℕ} {L : ℝ} (hL : L ≠ 0)
    (omega : I4Source.SourceMode n → ℝ)
    (hmajor : Summable (fun m => I4Source.modeMajorant n L m * |omega m|))
    (x0 : X n) (P : E n →L[ℝ] X n)
    (hcrit : fderiv ℝ (I4Source.sourceField n L omega) x0 = 0) (u : E n) :
    I4Source.sourceField n L omega (x0+P u) = I4Source.sourceField n L omega x0 +
      ∑ i, ∑ j, u i * matrix (I4Source.sourceField n L omega) x0 P u i j * u j := by
  exact matrix_quadratic (I4DeterministicC4.sourceField_contDiff_of_majorant n hL omega hmajor) x0 P hcrit u

end TaylorMatrix
