import SourceRemoteJetGaussian
import SourceEndpointHessianWitness
import SourceSmoothTopology
import Mathlib.Probability.Distributions.Gaussian.Multivariate
import Mathlib.MeasureTheory.Constructions.Pi
import Mathlib.MeasureTheory.Measure.Prod
import Mathlib.MeasureTheory.Measure.Haar.InnerProductSpace

/-! Ordinary endpoint Hessian-three sampling laws and marginal determinant nullity.
All-radius law statements concern the existing defined sampling kernel. -/

noncomputable section
set_option autoImplicit false
open scoped BigOperators Matrix Topology RealInnerProductSpace
open I4Foundation I4Source I4Weights I4SmoothCarrier I4SourceDerivativeGaussian
open I4SourceConfluentPins I4SourceConfluentLimits I4SourceRawPinConditioning
open I4SourceFinitePinKernel I4SourceRemoteJetWitness I4SourceRemoteJetGaussian
open I4SourceEndpointHessianWitness I4SourceSmoothTopology
open MeasureTheory ProbabilityTheory WithLp Matrix

namespace I4SourceEndpointHessianGaussian

private def endpoint (r : ℝ) (e : Fin 2) : Fin 2 → ℝ :=
  ![endpointM r,endpointS r] e

private def jetIndex (j : Fin 3) : Fin 6 := ![3,4,5] j

private def rawIndex (e : Fin 2) (j : Fin 3) : Fin 12 :=
  ![![6,7,8],![9,10,11]] e j

/-- The literal ordinary XX,XY,YY triple from the actual raw Hessian observation. -/
def endpointHessian (L r : ℝ) (e : Fin 2) (ω : SmoothSample 2 L) : Fin 3 → ℝ :=
  fun j => rawPinsWithHessians L r ω (rawIndex e j)

/-- All raw target components are retained through the selected49 mean. -/
def endpointHessianMean (L r : ℝ) (e : Fin 2) (t : Fin 6 → ℝ) : Fin 3 → ℝ :=
  fun j => remotePosteriorMean L r (endpoint r e) t (jetIndex j)

/-- Target-free principal residual Gram covariance in ordinary Hessian order. -/
def endpointHessianCovariance (L r : ℝ) (e : Fin 2) : Matrix (Fin 3) (Fin 3) ℝ :=
  fun j k => remoteResidualCovariance L r (endpoint r e) (jetIndex j) (jetIndex k)

private theorem endpointHessian_eq_remote (L r : ℝ) (e : Fin 2) (ω : SmoothSample 2 L) :
    endpointHessian L r e ω = fun j => remoteJet L (endpoint r e) ω (jetIndex j) := by
  funext j
  fin_cases e <;> fin_cases j <;> rfl

private theorem derivative_borel {L : ℝ} (hL : L ≠ 0) (k : ℕ)
    (x : Fin 2 → ℝ) (u : Fin k → (Fin 2 → ℝ)) :
    Measurable (fun ω : SmoothSample 2 L => iteratedFDeriv ℝ k (smoothSourceField 2 L ω) x u) := by
  borelize (DerivativeBCF 2 k)
  have he : Continuous (fun F : DerivativeBCF 2 k => F x u) := by fun_prop
  have h := he.measurable.comp (sourceDerivativeBCF_borel 2 hL k)
  simpa only [sourceDerivativeBCF_apply] using h

private theorem remoteJet_borel {L : ℝ} (hL : L ≠ 0) (x : Fin 2 → ℝ) :
    Measurable (remoteJet L x) := by
  apply Measurable.of_eval
  intro j
  fin_cases j
  · simpa only [iteratedFDeriv_zero_apply] using derivative_borel hL 0 x ![]
  · simpa only [iteratedFDeriv_one_apply] using derivative_borel hL 1 x ![directionX]
  · simpa only [iteratedFDeriv_one_apply] using derivative_borel hL 1 x ![directionY]
  · exact derivative_borel hL 2 x ![directionX,directionX]
  · exact derivative_borel hL 2 x ![directionX,directionY]
  · exact derivative_borel hL 2 x ![directionY,directionY]

private theorem endpointHessian_borel {L : ℝ} (hL : L ≠ 0) (r : ℝ) (e : Fin 2) :
    Measurable (endpointHessian L r e) := by
  have he : endpointHessian L r e = fun ω j => remoteJet L (endpoint r e) ω (jetIndex j) :=
    funext (endpointHessian_eq_remote L r e)
  rw [he]
  exact Measurable.of_eval (fun j => measurable_pi_apply (jetIndex j) |>.comp (remoteJet_borel hL _))

private theorem remoteRows_summable {L : ℝ} (hL : L ≠ 0)
    (x : Fin 2 → ℝ) (j : Fin 6) : Summable (remoteJetCoefficient L x j) := by
  fin_cases j
  · change Summable (fun m => modeCoefficient 2 L m x)
    have he : derivativeCoefficient 2 L 0 x (fun i => Fin.elim0 i) =
        fun m => modeCoefficient 2 L m x := by
      funext m
      exact iteratedFDeriv_zero_apply _
    rw [← he]
    exact derivativeCoefficient_summable 2 hL 0 x (fun i => Fin.elim0 i)
  · exact derivativeCoefficient_summable 2 hL 1 x (fun _ => directionX)
  · exact derivativeCoefficient_summable 2 hL 1 x (fun _ => directionY)
  · exact derivativeCoefficient_summable 2 hL 2 x ![directionX,directionX]
  · exact derivativeCoefficient_summable 2 hL 2 x ![directionX,directionY]
  · exact derivativeCoefficient_summable 2 hL 2 x ![directionY,directionY]

private theorem remoteCovariance_posSemidef {L : ℝ} (hL : L ≠ 0)
    (r : ℝ) (x : Fin 2 → ℝ) : (remoteResidualCovariance L r x).PosSemidef := by
  have hc : ∀ j, Summable (remoteResidualCoefficient L r x j) :=
    I4SourceFinitePinKernel.residualCoefficient_summable _ _ _
      (rawPinCoefficient_summable hL r) (remoteRows_summable hL x)
  apply Matrix.PosSemidef.of_dotProduct_mulVec_nonneg
  · ext i j
    simp only [remoteResidualCovariance,I4ContactGram.coefficientGram,
      Matrix.conjTranspose_apply,star_trivial]
    apply tsum_congr
    intro m
    ring
  · intro z
    have hs := I4ContactGram.coefficientGram_quadratic_hasSum _ hc z
    rw [← hs.tsum_eq]
    exact tsum_nonneg (fun m => sq_nonneg _)

private def hessianProjection : EuclideanSpace ℝ (Fin 6) →L[ℝ] EuclideanSpace ℝ (Fin 3) :=
  (PiLp.continuousLinearEquiv 2 ℝ (fun _ : Fin 3 => ℝ)).symm.toContinuousLinearMap.comp
    (ContinuousLinearMap.pi (fun j => EuclideanSpace.proj (jetIndex j)))

private theorem hessianProjection_apply (v : EuclideanSpace ℝ (Fin 6)) :
    hessianProjection v = toLp 2 (fun j => v (jetIndex j)) := rfl

private theorem projected_multivariateGaussian (m : EuclideanSpace ℝ (Fin 6))
    (S : Matrix (Fin 6) (Fin 6) ℝ) (hS : S.PosSemidef) :
    (multivariateGaussian m S).map hessianProjection =
      multivariateGaussian (hessianProjection m) (S.submatrix jetIndex jetIndex) := by
  apply IsGaussian.ext
  · simp only [id_eq,integral_id_multivariateGaussian]
    rw [ContinuousLinearMap.integral_id_map,integral_id_multivariateGaussian]
    exact IsGaussian.integrable_id
  rw [← ContinuousLinearMap.toBilinForm_inj]
  refine LinearMap.BilinForm.ext_basis (EuclideanSpace.basisFun (Fin 3) ℝ).toBasis fun i j => ?_
  rw [ContinuousLinearMap.toBilinForm_apply,ContinuousLinearMap.toBilinForm_apply,
    covarianceBilin_apply_eq_cov,covariance_map]
  · have he (i : Fin 3) :
        (fun u : EuclideanSpace ℝ (Fin 3) => ⟪(EuclideanSpace.basisFun (Fin 3) ℝ).toBasis i,u⟫_ℝ) ∘
          hessianProjection = fun u => u (jetIndex i) := by
      ext u
      simp [PiLp.inner_apply,hessianProjection]
    simp_rw [he,covariance_eval_multivariateGaussian hS,
      covarianceBilin_multivariateGaussian (hS.submatrix jetIndex)]
    simp
  any_goals exact Measurable.aestronglyMeasurable (by fun_prop)
  · fun_prop
  · exact IsGaussian.memLp_two_id

/-- Every-radius defined sampling law, obtained by one fixed projection of49. -/
theorem rawPinKernel_endpointHessian_eq_multivariateGaussian {L : ℝ} (hL : L ≠ 0)
    (r : ℝ) (e : Fin 2) (t : Fin 6 → ℝ) :
    (rawPinKernel hL r t).map (fun ω => toLp 2 (endpointHessian L r e ω)) =
      multivariateGaussian (toLp 2 (endpointHessianMean L r e t))
        (endpointHessianCovariance L r e) := by
  have hm : Measurable (fun ω => toLp 2 (remoteJet L (endpoint r e) ω)) :=
    (by fun_prop : Measurable (fun v : Fin 6 → ℝ => toLp 2 v)).comp (remoteJet_borel hL _)
  have he : (fun ω => toLp 2 (endpointHessian L r e ω)) =
      hessianProjection ∘ (fun ω => toLp 2 (remoteJet L (endpoint r e) ω)) := by
    funext ω
    rw [endpointHessian_eq_remote,hessianProjection_apply]
    rfl
  rw [he,← Measure.map_map hessianProjection.measurable hm,
    rawPinKernel_remoteJet_eq_multivariateGaussian hL,
    projected_multivariateGaussian _ _ (remoteCovariance_posSemidef hL r _)]
  rfl

private def selectedCorrection (L r : ℝ) (e : Fin 2) : Matrix (Fin 3) (Fin 6) ℝ :=
  fun j a => remoteRegressionMatrix L r (endpoint r e) (jetIndex j) a

private theorem endpointCoefficient_eq_remote (L r : ℝ) (e : Fin 2) (j : Fin 3) :
    endpointHessianCoefficient L r e j = remoteJetCoefficient L (endpoint r e) (jetIndex j) := by
  funext m
  fin_cases e <;> fin_cases j <;>
    change derivativeCoefficient 2 L 2 _ _ m = derivativeCoefficient 2 L 2 _ _ m <;>
    congr 1 <;> funext i <;> fin_cases i <;> rfl

private theorem endpointCovariance_eq_Gram (L r : ℝ) (e : Fin 2) :
    endpointHessianCovariance L r e = I4ContactGram.coefficientGram
      (I4SourceFinitePinKernel.residualCoefficient (rawPinCoefficient L r)
        (endpointHessianCoefficient L r e) (selectedCorrection L r e)) := by
  ext j k
  simp only [endpointHessianCovariance,remoteResidualCovariance,I4ContactGram.coefficientGram,
    remoteResidualCoefficient,I4SourceFinitePinKernel.residualCoefficient,
    endpointCoefficient_eq_remote,selectedCorrection]

/-- Actual50 finite marginal witnesses imply positivity at the selected49 correction. -/
theorem endpointHessianCovariance_posDef {L : ℝ} (hL : L ≠ 0) (r : ℝ)
    (hsep : I4Torus.torusProjection 2 L (endpointM r) ≠
      I4Torus.torusProjection 2 L (endpointS r)) (e : Fin 2) :
    (endpointHessianCovariance L r e).PosDef := by
  rw [endpointCovariance_eq_Gram]
  exact actual_endpointHessian_residual_coefficientGram_posDef hL r hsep e (selectedCorrection L r e)

-- Integrated once from frozen text-only fixed3 Gaussian AC helper.
/- UNCOMPILED TEXT ONLY. Insert inside namespace I4SourceEndpointHessianGaussian,
   in its noncomputable section. Required imports are frozen in IMPORTS.txt. -/

open MeasureTheory MeasureTheory.Measure ProbabilityTheory WithLp Matrix
open scoped MatrixOrder Matrix.Norms.L2Operator

private theorem finiteGaussian3_absolutelyContinuous
    (m : EuclideanSpace ℝ (Fin 3)) (S : Matrix (Fin 3) (Fin 3) ℝ)
    (hS : S.PosDef) : multivariateGaussian m S ≪ volume := by
  have hg : gaussianReal 0 1 ≪ (volume : Measure ℝ) :=
    gaussianReal_absolutelyContinuous 0 one_ne_zero
  have h2 :
      (Measure.pi fun _ : Fin 2 => gaussianReal 0 1) ≪
        (volume : Measure (Fin 2 → ℝ)) := by
    let e := MeasurableEquiv.piFinTwo (fun _ : Fin 2 => ℝ)
    have hp := measurePreserving_piFinTwo (fun _ : Fin 2 => gaussianReal 0 1)
    have hv := volume_preserving_piFinTwo (fun _ : Fin 2 => ℝ)
    have hmap := (hg.prod hg).map e.symm.measurable
    rw [(hp.symm e).map_eq] at hmap
    change (Measure.pi fun _ : Fin 2 => gaussianReal 0 1) ≪
      (volume : Measure (ℝ × ℝ)).map e.symm at hmap
    rwa [(hv.symm e).map_eq] at hmap
  have h3 :
      (Measure.pi fun _ : Fin 3 => gaussianReal 0 1) ≪
        (volume : Measure (Fin 3 → ℝ)) := by
    let e := MeasurableEquiv.piFinSuccAbove (fun _ : Fin 3 => ℝ) 0
    have hp := measurePreserving_piFinSuccAbove
      (fun _ : Fin 3 => gaussianReal 0 1) 0
    have hv := volume_preserving_piFinSuccAbove (fun _ : Fin 3 => ℝ) 0
    have hmap := (hg.prod h2).map e.symm.measurable
    rw [(hp.symm e).map_eq] at hmap
    change (Measure.pi fun _ : Fin 3 => gaussianReal 0 1) ≪
      (volume : Measure (ℝ × (Fin 2 → ℝ))).map e.symm at hmap
    rwa [(hv.symm e).map_eq] at hmap
  have hstd : stdGaussian (EuclideanSpace ℝ (Fin 3)) ≪ volume := by
    have hmap := h3.map (PiLp.volume_preserving_toLp (Fin 3)).measurable
    rw [map_pi_eq_stdGaussian, (PiLp.volume_preserving_toLp (Fin 3)).map_eq] at hmap
    exact hmap
  have hsqrt : IsUnit (CFC.sqrt S) := by
    apply isUnit_mul_self_iff.mp
    rw [CFC.sqrt_mul_sqrt_self S hS.posSemidef.nonneg]
    exact hS.isUnit
  let A : EuclideanSpace ℝ (Fin 3) →L[ℝ] EuclideanSpace ℝ (Fin 3) :=
    Matrix.toEuclideanCLM (𝕜 := ℝ) (CFC.sqrt S)
  have hA : IsUnit A := hsqrt.map (Matrix.toEuclideanCLM (𝕜 := ℝ))
  have hdet : A.det ≠ 0 :=
    (LinearMap.isUnit_det A.toLinearMap
      (hA.map ContinuousLinearMap.toLinearMapRingHom)).ne_zero
  have hq : QuasiMeasurePreserving
      (fun x : EuclideanSpace ℝ (Fin 3) => m + A x)
      (volume : Measure (EuclideanSpace ℝ (Fin 3))) volume :=
    (measurePreserving_add_left (volume : Measure (EuclideanSpace ℝ (Fin 3))) m).quasiMeasurePreserving.comp
        (ContinuousLinearMap.quasiMeasurePreserving
          (volume : Measure (EuclideanSpace ℝ (Fin 3))) A hdet)
  change (stdGaussian (EuclideanSpace ℝ (Fin 3))).map (fun x => m + A x) ≪ volume
  exact (hstd.map hq.measurable).trans hq.absolutelyContinuous

-- Integrated once from frozen text-only fixed3 determinant helper.
private theorem determinant3_zero_volume :
    volume {H : EuclideanSpace ℝ (Fin 3) | H 0 * H 2 - (H 1) ^ 2 = 0} = 0 := by
  let Z : Set (ℝ × (ℝ × ℝ)) :=
    {p | p.1 * p.2.2 - p.2.1 ^ 2 = 0}
  have hcont : Continuous (fun p : ℝ × (ℝ × ℝ) =>
      p.1 * p.2.2 - p.2.1 ^ 2) :=
    (continuous_fst.mul continuous_snd.snd).sub (continuous_snd.fst.pow 2)
  have hZ : MeasurableSet Z :=
    (isClosed_eq hcont continuous_const).measurableSet
  have hprod :
      ((volume : Measure ℝ).prod
        ((volume : Measure ℝ).prod (volume : Measure ℝ))) Z = 0 := by
    apply Measure.measure_prod_null_of_ae_null hZ
    refine (Measure.ae_ne (volume : Measure ℝ) 0).mono ?_
    intro a ha
    change ((volume : Measure ℝ).prod (volume : Measure ℝ))
      {p : ℝ × ℝ | a * p.2 - p.1 ^ 2 = 0} = 0
    have hsection : MeasurableSet {p : ℝ × ℝ | a * p.2 - p.1 ^ 2 = 0} :=
      (isClosed_eq
        ((continuous_const.mul continuous_snd).sub (continuous_fst.pow 2))
        continuous_const).measurableSet
    apply Measure.measure_prod_null_of_ae_null hsection
    apply Filter.Eventually.of_forall
    intro b
    change (volume : Measure ℝ) {c : ℝ | a * c - b ^ 2 = 0} = 0
    have hsingleton : {c : ℝ | a * c - b ^ 2 = 0} = {b ^ 2 / a} := by
      ext c
      simp only [Set.mem_setOf_eq, Set.mem_singleton_iff]
      constructor
      · intro hc
        apply (eq_div_iff ha).mpr
        simpa only [mul_comm] using (sub_eq_zero.mp hc)
      · intro hc
        apply sub_eq_zero.mpr
        simpa only [mul_comm] using (eq_div_iff ha).mp hc
    rw [hsingleton]
    exact measure_singleton _
  have hcoord : MeasurePreserving
      (fun H : EuclideanSpace ℝ (Fin 3) => (H 0, (H 1, H 2)))
      volume volume := by
    exact
      ((MeasurePreserving.id (volume : Measure ℝ)).prod
        (volume_preserving_piFinTwo (fun _ : Fin 2 => ℝ))).comp
        ((volume_preserving_piFinSuccAbove (fun _ : Fin 3 => ℝ) 0).comp
          (PiLp.volume_preserving_ofLp (Fin 3)))
  exact hcoord.preimage_null hprod



private theorem finiteGaussian3_det_ne_zero (m : EuclideanSpace ℝ (Fin 3))
    (S : Matrix (Fin 3) (Fin 3) ℝ) (hS : S.PosDef) :
    ∀ᵐ H ∂multivariateGaussian m S, H 0*H 2-(H 1)^2 ≠ 0 := by
  apply (ae_iff).2
  simpa only [not_not] using
    finiteGaussian3_absolutelyContinuous m S hS determinant3_zero_volume

/-- A fixed noncentered finite control, inventory-only and not a realized source parameter. -/
private theorem noncentered_finiteGaussian_control :
    multivariateGaussian (toLp 2 (![1,2,3] : Fin 3 → ℝ)) (1 : Matrix (Fin 3) (Fin 3) ℝ) ≪ volume ∧
    ∀ᵐ H ∂multivariateGaussian (toLp 2 (![1,2,3] : Fin 3 → ℝ)) (1 : Matrix (Fin 3) (Fin 3) ℝ),
      H 0*H 2-(H 1)^2 ≠ 0 :=
  ⟨finiteGaussian3_absolutelyContinuous _ _ Matrix.PosDef.one,
    finiteGaussian3_det_ne_zero _ _ Matrix.PosDef.one⟩

/-- Both marginal endpoint determinants are nonzero on one actual sampling-a.e. event. -/
theorem rawPinKernel_ae_endpointHessian_det_ne_zero {L : ℝ} (hL : L ≠ 0) (r : ℝ)
    (hsep : I4Torus.torusProjection 2 L (endpointM r) ≠
      I4Torus.torusProjection 2 L (endpointS r)) (t : Fin 6 → ℝ) :
    ∀ᵐ ω ∂rawPinKernel hL r t, ∀ e : Fin 2,
      let H := endpointHessian L r e ω
      H 0*H 2-(H 1)^2 ≠ 0 := by
  rw [ae_all_iff]
  intro e
  have h := finiteGaussian3_det_ne_zero (toLp 2 (endpointHessianMean L r e t))
    (endpointHessianCovariance L r e) (endpointHessianCovariance_posDef hL r hsep e)
  rw [← rawPinKernel_endpointHessian_eq_multivariateGaussian hL r e t] at h
  exact ae_of_ae_map (by
    exact ((by fun_prop : Measurable (fun v : Fin 3 → ℝ => toLp 2 v)).comp
      (endpointHessian_borel hL r e)).aemeasurable) h

end I4SourceEndpointHessianGaussian
