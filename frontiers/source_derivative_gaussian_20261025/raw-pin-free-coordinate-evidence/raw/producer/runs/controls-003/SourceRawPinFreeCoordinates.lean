import Mathlib.Probability.Distributions.Gaussian.HasGaussianLaw.Basic
import Mathlib.Probability.Distributions.Gaussian.HasGaussianLaw.Independence
import Mathlib.Probability.Independence.Process.Basic
import Mathlib.MeasureTheory.Function.LpSeminorm.TriangleInequality
import SourceFinitePinKernel
import SourceCurvatureDecomposition
import Mathlib.LinearAlgebra.Finsupp.LinearCombination

/-! Finite raw-pin-free coordinates on the original smooth coefficient carrier.
Only the deterministic directions have finite support. -/

noncomputable section
open scoped BigOperators
set_option autoImplicit false

open MeasureTheory ProbabilityTheory I4Foundation I4Source I4Smooth I4SmoothCarrier
open I4SourceGaussian I4SourceCovariance I4SourceSmoothConditional
open I4SourceCurvatureDecomposition I4SourceFinitePinKernel I4SourceRawPinConditioning

namespace I4SourceRawPinFreeCoordinates

/-- A finite orthonormal family in the literal six-row raw pin kernel. -/
structure RawPinFreeFrame (L r : ℝ) (n : ℕ) where
  chi : Fin n → (SourceMode 2 →₀ ℝ)
  gram : ∀ j k : Fin n,
    finitePairing (fun m => chi j m) (chi k) = if j = k then 1 else 0
  raw_kernel : ∀ (i : Fin 6) (j : Fin n),
    finitePairing (rawPinCoefficient L r i) (chi j) = 0

private def freeLift {L r : ℝ} {n : ℕ} (F : RawPinFreeFrame L r n)
    (z : Fin n → ℝ) : SourceMode 2 →₀ ℝ := ∑ j, z j • F.chi j

/-- All finite original-coefficient coordinates of the supplied frame. -/
def freeCoordinate {L r : ℝ} {n : ℕ} (F : RawPinFreeFrame L r n)
    (ω : SmoothSample 2 L) : Fin n → ℝ := fun j => finitePairing ω.val (F.chi j)

/-- Add the entire finite frame lift to the literal smooth sample. -/
def freeShiftSample {L r : ℝ} {n : ℕ} (F : RawPinFreeFrame L r n)
    (z : Fin n → ℝ) (ω : SmoothSample 2 L) : SmoothSample 2 L :=
  finiteShiftSample (freeLift F z) ω

/-- Subtract the full finite orthogonal projection, on the original carrier. -/
def freeResidualSample {L r : ℝ} {n : ℕ} (F : RawPinFreeFrame L r n)
    (ω : SmoothSample 2 L) : SmoothSample 2 L :=
  freeShiftSample F (-freeCoordinate F ω) ω

private theorem freeLift_apply {L r : ℝ} {n : ℕ} (F : RawPinFreeFrame L r n)
    (z : Fin n → ℝ) (m : SourceMode 2) :
    freeLift F z m = ∑ j, z j * F.chi j m := by
  classical
  simp [freeLift]

private theorem freeShiftSample_val {L r : ℝ} {n : ℕ}
    (F : RawPinFreeFrame L r n) (z : Fin n → ℝ) (ω : SmoothSample 2 L)
    (m : SourceMode 2) :
    (freeShiftSample F z ω).val m = ω.val m + ∑ j, z j * F.chi j m := by
  rw [freeShiftSample, finiteShiftSample_val, freeLift_apply]

private theorem freeResidualSample_val {L r : ℝ} {n : ℕ}
    (F : RawPinFreeFrame L r n) (ω : SmoothSample 2 L) (m : SourceMode 2) :
    (freeResidualSample F ω).val m =
      ω.val m - ∑ j, F.chi j m * freeCoordinate F ω j := by
  simp only [freeResidualSample, freeShiftSample_val, Pi.neg_apply, neg_mul,
    Finset.sum_neg_distrib, mul_comm]
  rfl

private theorem finitePairing_eq_tsum {ι : Type*} (a : ι → ℝ) (v : ι →₀ ℝ) :
    finitePairing a v = ∑' m, a m * v m := by
  classical
  symm
  apply HasSum.tsum_eq
  apply hasSum_sum_of_ne_finset_zero
  intro m hm
  simp [Finsupp.notMem_support_iff.mp hm]

private theorem chi_summable {L r : ℝ} {n : ℕ} (F : RawPinFreeFrame L r n)
    (j : Fin n) : Summable (fun m => F.chi j m) := by
  classical
  apply summable_of_ne_finset_zero (s := (F.chi j).support)
  intro m hm
  exact Finsupp.notMem_support_iff.mp hm

private theorem chi_normSquared {L r : ℝ} {n : ℕ}
    (F : RawPinFreeFrame L r n) (j : Fin n) : ∑' m, (F.chi j m) ^ 2 = 1 := by
  have h := F.gram j j
  rw [finitePairing_eq_tsum] at h
  simpa [pow_two] using h

private theorem freeCoordinate_eq_unitDirection {L r : ℝ} {n : ℕ}
    (F : RawPinFreeFrame L r n) (j : Fin n) :
    (fun ω => freeCoordinate F ω j) = unitDirection (fun m => F.chi j m) := by
  funext ω
  simp only [freeCoordinate, finitePairing_eq_tsum, unitDirection, scalarSeries, mul_comm]

set_option maxHeartbeats 1000000 in
/-- The coordinate vector, joint finite shift, and full residual are measurable. -/
theorem freeMaps_measurable {L r : ℝ} {n : ℕ} (F : RawPinFreeFrame L r n) :
    Measurable (freeCoordinate F) ∧
    Measurable (fun p : (Fin n → ℝ) × SmoothSample 2 L => freeShiftSample F p.1 p.2) ∧
    Measurable (freeResidualSample F) := by
  have hZ : Measurable (freeCoordinate F) := by
    apply Measurable.of_eval
    intro j
    rw [freeCoordinate_eq_unitDirection]
    exact unitDirection_measurable _
  have hS : Measurable (fun p : (Fin n → ℝ) × SmoothSample 2 L =>
      freeShiftSample F p.1 p.2) := by
    apply Measurable.subtype_mk
    apply Measurable.of_eval
    intro m
    change Measurable (fun p : (Fin n → ℝ) × SmoothSample 2 L =>
      p.2.val m + freeLift F p.1 m)
    simp_rw [freeLift_apply]
    exact ((measurable_pi_apply m).comp (measurable_subtype_coe.comp measurable_snd)).add
      (Finset.measurable_sum _ (fun j _ =>
        ((measurable_pi_apply j).comp measurable_fst).mul_const _))
  exact ⟨hZ, hS, hS.comp (hZ.neg.prodMk measurable_id)⟩

private theorem finitePairing_eq_linearCombination {ι : Type*}
    (a : ι → ℝ) (v : ι →₀ ℝ) :
    finitePairing a v = Finsupp.linearCombination ℝ a v := by
  simp only [finitePairing, Finsupp.linearCombination_apply, smul_eq_mul, mul_comm]

private theorem freeLift_raw_kernel {L r : ℝ} {n : ℕ}
    (F : RawPinFreeFrame L r n) (z : Fin n → ℝ) (i : Fin 6) :
    finitePairing (rawPinCoefficient L r i) (freeLift F z) = 0 := by
  classical
  simp only [finitePairing_eq_linearCombination, freeLift, map_sum, map_smul]
  simp_rw [← finitePairing_eq_linearCombination, F.raw_kernel]
  simp

private theorem finitePairing_add_observation {ι : Type*}
    (a b : ι → ℝ) (v : ι →₀ ℝ) :
    finitePairing (a + b) v = finitePairing a v + finitePairing b v := by
  classical
  simp [finitePairing, Finsupp.sum, add_mul, Finset.sum_add_distrib]

private theorem finitePairing_sum_observation {ι : Type*} {n : ℕ}
    (a : Fin n → ι → ℝ) (z : Fin n → ℝ) (v : ι →₀ ℝ) :
    finitePairing (fun m => ∑ j, z j * a j m) v =
      ∑ j, z j * finitePairing (a j) v := by
  classical
  simp only [finitePairing, Finsupp.sum, Finset.sum_mul, Finset.mul_sum]
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro j _hj
  apply Finset.sum_congr rfl
  intro m _hm
  ring

private theorem freeCoordinate_shift {L r : ℝ} {n : ℕ}
    (F : RawPinFreeFrame L r n) (z : Fin n → ℝ) (ω : SmoothSample 2 L) :
    freeCoordinate F (freeShiftSample F z ω) = freeCoordinate F ω + z := by
  classical
  funext k
  change finitePairing (fun m => (freeShiftSample F z ω).val m) (F.chi k) = _
  simp_rw [freeShiftSample_val]
  rw [show (fun m => ω.val m + ∑ j, z j * F.chi j m) =
    ω.val + (fun m => ∑ j, z j * F.chi j m) from rfl,
    finitePairing_add_observation, finitePairing_sum_observation]
  simp [F.gram, freeCoordinate]

private theorem freeCoordinate_residual {L r : ℝ} {n : ℕ}
    (F : RawPinFreeFrame L r n) (ω : SmoothSample 2 L) :
    freeCoordinate F (freeResidualSample F ω) = 0 := by
  rw [freeResidualSample, freeCoordinate_shift, add_neg_cancel]

private theorem free_reconstruction {L r : ℝ} {n : ℕ}
    (F : RawPinFreeFrame L r n) (ω : SmoothSample 2 L) :
    freeShiftSample F (freeCoordinate F ω) (freeResidualSample F ω) = ω := by
  apply Subtype.ext
  funext m
  rw [freeShiftSample_val, freeResidualSample_val]
  simp only [mul_comm (freeCoordinate F ω _)]
  ring

/-- Every full raw target posterior retains the complete finite free lift,
including at singular radii. -/
theorem rawPosteriorSample_free_reconstruction {L r : ℝ} {n : ℕ}
    (hL : L ≠ 0) (F : RawPinFreeFrame L r n) (t : Fin 6 → ℝ)
    (ω : SmoothSample 2 L) :
    rawPosteriorSample hL r t ω = freeShiftSample F (freeCoordinate F ω)
      (rawPosteriorSample hL r t (freeResidualSample F ω)) := by
  conv_lhs => rw [← free_reconstruction F ω]
  exact rawPosteriorSample_finiteShiftSample hL r t (freeLift F (freeCoordinate F ω))
    (freeLift_raw_kernel F _) (freeResidualSample F ω)

/- UNCOMPILED TEXT ONLY. Insert once inside namespace
   I4SourceRawPinFreeCoordinates, after the producer's deterministic identities
   and freeMaps_measurable. Exact assumptions are recorded in provenance. -/

open MeasureTheory ProbabilityTheory I4Foundation I4Source I4SmoothCarrier
open I4SourceSmoothConditional I4SourceCurvatureDecomposition I4SourceFinitePinKernel
open scoped BigOperators

private theorem freeGaussian_scalar_hasLaw
    {L r : ℝ} {n : ℕ} (hL : L ≠ 0) (F : RawPinFreeFrame L r n) (j : Fin n) :
    HasLaw (fun ω => freeCoordinate F ω j) (gaussianReal 0 1) (smoothLaw 2 L) := by
  rw [freeCoordinate_eq_unitDirection F j]
  exact unitDirection_hasLaw hL (fun m => F.chi j m)
    (chi_summable F j) (chi_normSquared F j)

private theorem freeGaussian_finiteCoefficients_hasGaussianLaw
    {L r : ℝ} {n : ℕ} (hL : L ≠ 0) (F : RawPinFreeFrame L r n)
    (I : Finset (SourceMode 2)) :
    HasGaussianLaw (fun ω : SmoothSample 2 L =>
      (freeCoordinate F ω, fun m : I => ω.val m)) (smoothLaw 2 L) := by
  classical
  let q : (Fin n ⊕ I) → SourceMode 2 → ℝ :=
    Sum.elim (fun j m => F.chi j m) (fun m => Pi.single m.val 1)
  have hq (j : Fin n ⊕ I) : Summable (q j) := by
    cases j with
    | inl j => exact chi_summable F j
    | inr m =>
      apply summable_of_ne_finset_zero (s := {m.val})
      intro k hk
      simp only [Finset.mem_singleton] at hk
      simp [q,hk]
  have hG := scalarSeries_finite_hasGaussianLaw q hq
  have hm : Measurable (fun η : SourceMode 2 → ℝ =>
      fun j : Fin n ⊕ I => scalarSeries (q j) η) :=
    Measurable.of_eval (fun j => scalarSeries_measurable (q j))
  have hμ : HasGaussianLaw (fun ω : SmoothSample 2 L =>
      fun j : Fin n ⊕ I => scalarSeries (q j) (sampleInclusion 2 L ω))
      (smoothLaw 2 L) := by
    refine ⟨(hm.comp (sampleInclusion_measurable 2 L)).aemeasurable,?_⟩
    rw [observation_map_eq 2 hL _ hm]
    exact hG.isGaussian_map
  let A : ((Fin n ⊕ I) → ℝ) →L[ℝ] ((Fin n → ℝ) × (I → ℝ)) :=
    (ContinuousLinearMap.pi (fun j => ContinuousLinearMap.proj (Sum.inl j))).prod
      (ContinuousLinearMap.pi (fun m => ContinuousLinearMap.proj (Sum.inr m)))
  apply (hμ.map_fun A).congr
  filter_upwards with ω
  apply Prod.ext
  · funext j
    change scalarSeries (fun m => F.chi j m) ω.val = freeCoordinate F ω j
    exact (congrFun (freeCoordinate_eq_unitDirection F j) ω).symm
  · funext m
    exact scalarSeries_single m.val ω.val

private theorem freeGaussian_vector_hasGaussianLaw
    {L r : ℝ} {n : ℕ} (hL : L ≠ 0) (F : RawPinFreeFrame L r n) :
    HasGaussianLaw (freeCoordinate F) (smoothLaw 2 L) :=
  (freeGaussian_finiteCoefficients_hasGaussianLaw hL F ∅).fst

private theorem freeGaussian_covariance_gram
    {L r : ℝ} {n : ℕ} (hL : L ≠ 0) (F : RawPinFreeFrame L r n)
    (j k : Fin n) :
    covariance (fun ω => freeCoordinate F ω j) (fun ω => freeCoordinate F ω k)
      (smoothLaw 2 L) = if j = k then 1 else 0 := by
  rw [freeCoordinate_eq_unitDirection F j,freeCoordinate_eq_unitDirection F k]
  change covariance
    (fun ω => scalarSeries (fun m => F.chi j m) (sampleInclusion 2 L ω))
    (fun ω => scalarSeries (fun m => F.chi k m) (sampleInclusion 2 L ω))
    (smoothLaw 2 L) = if j = k then 1 else 0
  rw [covariance_comp_inclusion 2 hL _ _
    (scalarSeries_measurable (fun m => F.chi j m))
    (scalarSeries_measurable (fun m => F.chi k m)),
    I4SourceCovariance.scalarSeries_covariance _ _
      (chi_summable F j) (chi_summable F k)]
  exact (finitePairing_eq_tsum (fun m => F.chi j m) (F.chi k)).symm.trans (F.gram j k)

private theorem freeGaussian_coefficient_covariance
    {L r : ℝ} {n : ℕ} (hL : L ≠ 0) (F : RawPinFreeFrame L r n)
    (j : Fin n) (m : SourceMode 2) :
    covariance (fun ω => freeCoordinate F ω j)
      (fun ω : SmoothSample 2 L => ω.val m) (smoothLaw 2 L) = F.chi j m := by
  rw [freeCoordinate_eq_unitDirection F j]
  exact unitDirection_coefficient_covariance hL (fun k => F.chi j k)
    (chi_summable F j) m

private theorem freeGaussian_iIndepFun
    {L r : ℝ} {n : ℕ} (hL : L ≠ 0) (F : RawPinFreeFrame L r n) :
    iIndepFun (fun j ω => freeCoordinate F ω j) (smoothLaw 2 L) := by
  apply (freeGaussian_vector_hasGaussianLaw hL F).iIndepFun_of_covariance_eq_zero
  intro j k hjk
  rw [freeGaussian_covariance_gram hL F j k]
  simp [hjk]

private theorem freeGaussian_pi_map
    {L r : ℝ} {n : ℕ} (hL : L ≠ 0) (F : RawPinFreeFrame L r n) :
    (smoothLaw 2 L).map (freeCoordinate F) =
      Measure.pi (fun _ : Fin n => gaussianReal 0 1) := by
  have hm (j : Fin n) : AEMeasurable
      (fun ω => freeCoordinate F ω j) (smoothLaw 2 L) :=
    ((measurable_pi_apply j).comp (freeMaps_measurable F).1).aemeasurable
  calc
    (smoothLaw 2 L).map (freeCoordinate F) =
        Measure.pi (fun j : Fin n =>
          (smoothLaw 2 L).map (fun ω => freeCoordinate F ω j)) :=
      (freeGaussian_iIndepFun hL F).map_fun_eq_pi_map hm
    _ = Measure.pi (fun _ : Fin n => gaussianReal 0 1) := by
      congr 1
      funext j
      exact (freeGaussian_scalar_hasLaw hL F j).map_eq

private def freeGaussian_projection
    {L r : ℝ} {n : ℕ} (F : RawPinFreeFrame L r n) (I : Finset (SourceMode 2)) :
    (Fin n → ℝ) →L[ℝ] (I → ℝ) :=
  ContinuousLinearMap.pi (fun m =>
    ∑ j : Fin n, F.chi j m.val • ContinuousLinearMap.proj j)

private theorem freeGaussian_projection_apply
    {L r : ℝ} {n : ℕ} (F : RawPinFreeFrame L r n) (I : Finset (SourceMode 2))
    (z : Fin n → ℝ) (m : I) :
    freeGaussian_projection F I z m = ∑ j : Fin n, F.chi j m.val * z j := by
  simp only [freeGaussian_projection,ContinuousLinearMap.pi_apply,
    _root_.sum_apply,_root_.smul_apply,ContinuousLinearMap.proj_apply,smul_eq_mul]

private theorem freeGaussian_finiteResidual_hasGaussianLaw
    {L r : ℝ} {n : ℕ} (hL : L ≠ 0) (F : RawPinFreeFrame L r n)
    (I : Finset (SourceMode 2)) :
    HasGaussianLaw (fun ω : SmoothSample 2 L =>
      (freeCoordinate F ω, fun m : I => (freeResidualSample F ω).val m))
      (smoothLaw 2 L) := by
  let A : ((Fin n → ℝ) × (I → ℝ)) →L[ℝ] ((Fin n → ℝ) × (I → ℝ)) :=
    (ContinuousLinearMap.fst ℝ (Fin n → ℝ) (I → ℝ)).prod
      (ContinuousLinearMap.snd ℝ (Fin n → ℝ) (I → ℝ) -
        (freeGaussian_projection F I).comp
          (ContinuousLinearMap.fst ℝ (Fin n → ℝ) (I → ℝ)))
  apply ((freeGaussian_finiteCoefficients_hasGaussianLaw hL F I).map_fun A).congr
  filter_upwards with ω
  apply Prod.ext
  · rfl
  · funext m
    change ω.val m - freeGaussian_projection F I (freeCoordinate F ω) m =
      (freeResidualSample F ω).val m
    rw [freeGaussian_projection_apply,freeResidualSample_val]

private theorem freeGaussian_residual_zero_covariance
    {L r : ℝ} {n : ℕ} (hL : L ≠ 0) (F : RawPinFreeFrame L r n)
    (j : Fin n) (m : SourceMode 2) :
    covariance (fun ω => freeCoordinate F ω j)
      (fun ω => (freeResidualSample F ω).val m) (smoothLaw 2 L) = 0 := by
  classical
  let : IsProbabilityMeasure (smoothLaw 2 L) := smoothLaw_isProbabilityMeasure 2 hL
  have hZ (k : Fin n) :
      HasGaussianLaw (fun ω => freeCoordinate F ω k) (smoothLaw 2 L) :=
    (freeGaussian_scalar_hasLaw hL F k).hasGaussianLaw
  have hsum : MemLp (fun ω : SmoothSample 2 L =>
      ∑ k : Fin n, F.chi k m * freeCoordinate F ω k) 2 (smoothLaw 2 L) :=
    memLp_finsetSum Finset.univ (fun k _ => (hZ k).memLp_two.const_mul (F.chi k m))
  have hres : (fun ω : SmoothSample 2 L => (freeResidualSample F ω).val m) =
      (fun ω => ω.val m - ∑ k : Fin n, F.chi k m * freeCoordinate F ω k) :=
    funext (fun ω => freeResidualSample_val F ω m)
  rw [hres,covariance_fun_sub_right (hZ j).memLp_two
    (coefficient_hasGaussianLaw hL m).memLp_two hsum,
    freeGaussian_coefficient_covariance hL F j m,
    covariance_fun_sum_right
      (fun k => (hZ k).memLp_two.const_mul (F.chi k m)) (hZ j).memLp_two]
  simp_rw [covariance_const_mul_right,freeGaussian_covariance_gram hL F]
  simp [mul_ite]

private theorem freeGaussian_finiteResidual_indepFun
    {L r : ℝ} {n : ℕ} (hL : L ≠ 0) (F : RawPinFreeFrame L r n)
    (I : Finset (SourceMode 2)) :
    IndepFun (freeCoordinate F)
      (fun ω : SmoothSample 2 L => fun m : I => (freeResidualSample F ω).val m)
      (smoothLaw 2 L) :=
  (freeGaussian_finiteResidual_hasGaussianLaw hL F I).indepFun_of_covariance_eval
    (fun j m => freeGaussian_residual_zero_covariance hL F j m.val)

private theorem freeGaussian_process_indepFun
    {L r : ℝ} {n : ℕ} (hL : L ≠ 0) (F : RawPinFreeFrame L r n) :
    IndepFun (freeCoordinate F)
      (fun ω : SmoothSample 2 L => fun m : SourceMode 2 =>
        (freeResidualSample F ω).val m) (smoothLaw 2 L) := by
  let : IsProbabilityMeasure (smoothLaw 2 L) := smoothLaw_isProbabilityMeasure 2 hL
  apply IndepFun.indepFun_process (freeMaps_measurable F).1
  · intro m
    exact (measurable_pi_apply m).comp
      (measurable_subtype_coe.comp (freeMaps_measurable F).2.2)
  · exact freeGaussian_finiteResidual_indepFun hL F

private theorem freeGaussian_sample_indepFun
    {L r : ℝ} {n : ℕ} (hL : L ≠ 0) (F : RawPinFreeFrame L r n) :
    IndepFun (freeCoordinate F) (freeResidualSample F) (smoothLaw 2 L) := by
  obtain ⟨q,hq,hqleft⟩ := exists_measurable_sampleProjection 2 L
  have h := (freeGaussian_process_indepFun hL F).comp measurable_id hq
  change IndepFun (freeCoordinate F)
    (fun ω : SmoothSample 2 L => q (fun m => (freeResidualSample F ω).val m))
    (smoothLaw 2 L) at h
  have hqR :
      (fun ω : SmoothSample 2 L => q (fun m => (freeResidualSample F ω).val m)) =
        freeResidualSample F := by
    funext ω
    exact hqleft (freeResidualSample F ω)
  rwa [hqR] at h

theorem freeResidual_freeCoordinate_joint_map
    {L r : ℝ} {n : ℕ} (hL : L ≠ 0) (F : RawPinFreeFrame L r n) :
    (smoothLaw 2 L).map (fun ω =>
      (freeResidualSample F ω,freeCoordinate F ω)) =
      ((smoothLaw 2 L).map (freeResidualSample F)).prod
        (Measure.pi (fun _ : Fin n => gaussianReal 0 1)) := by
  let : IsProbabilityMeasure (smoothLaw 2 L) := smoothLaw_isProbabilityMeasure 2 hL
  calc
    (smoothLaw 2 L).map (fun ω => (freeResidualSample F ω,freeCoordinate F ω)) =
        ((smoothLaw 2 L).map (freeResidualSample F)).prod
          ((smoothLaw 2 L).map (freeCoordinate F)) :=
      (freeGaussian_sample_indepFun hL F).symm.map_prod_eq_prod_map_map
        (freeMaps_measurable F).2.2.aemeasurable (freeMaps_measurable F).1.aemeasurable
    _ = ((smoothLaw 2 L).map (freeResidualSample F)).prod
        (Measure.pi (fun _ : Fin n => gaussianReal 0 1)) := by
      rw [freeGaussian_pi_map hL F]

end I4SourceRawPinFreeCoordinates
