import SourceRawPinFreeCoordinates
import SourceRemoteJetWitness
import SourceTwoRemoteFirstJetWitness
import SourceEndpointHessianGaussian
import SourceCompactTargetMoments
import SourceLifetimePairFiniteness
import SourceActualFoldCandidate
import Mathlib.LinearAlgebra.Finsupp.LinearCombination

/-! Global Morse distinctness for the literal positive-gap sampling law.
The finite source, incidence, probability, quotient and Lifetime adapters are
private; the final global proposition is the only authored public API. -/

noncomputable section
set_option autoImplicit false
open scoped BigOperators Topology Matrix
open Set MeasureTheory ProbabilityTheory I4Foundation I4Source I4Smooth I4SmoothCarrier
open I4SourceGaussian I4SourceCovariance I4SourceDerivativeGaussian
open I4SourceConfluentPins I4SourceConfluentLimits I4SourceRawPinConditioning
open I4SourceFinitePinKernel I4SourceRemoteJetWitness I4SourceTwoRemoteFirstJetWitness
open I4SourceRawPinFreeCoordinates I4SourceCompactTargetMoments I4ActualSourceMorse
open I4LifetimeField I4SourceActualFoldCandidate I4SourceLifetimePairFiniteness
open UniversalLaw.Spec.Lifetime

namespace I4SourceGapConditionalMorseDistinct

private abbrev Point2 := Fin 2 → ℝ
private abbrev Point4 := Point2 × Point2

private def Remote (L r : ℝ) (x : Point2) : Prop :=
  I4Torus.torusProjection 2 L x ≠ I4Torus.torusProjection 2 L (endpointM r) ∧
  I4Torus.torusProjection 2 L x ≠ I4Torus.torusProjection 2 L (endpointS r)

private def RemotePair (L r : ℝ) (p : Point4) : Prop :=
  Remote L r p.1 ∧ Remote L r p.2 ∧
    I4Torus.torusProjection 2 L p.1 ≠ I4Torus.torusProjection 2 L p.2

private def gradientRows (L : ℝ) (x : Point2) : Fin 2 → SourceMode 2 → ℝ :=
  ![remoteJetCoefficient L x 1,remoteJetCoefficient L x 2]

private def levelRows (L : ℝ) (x : Point2) : Fin 3 → SourceMode 2 → ℝ :=
  ![remoteJetCoefficient L x 0,remoteJetCoefficient L x 1,remoteJetCoefficient L x 2]

private def tieRows (L : ℝ) (p : Point4) : Fin 5 → SourceMode 2 → ℝ :=
  ![twoRemoteFirstJetCoefficient L p.1 p.2 1,
    twoRemoteFirstJetCoefficient L p.1 p.2 2,
    twoRemoteFirstJetCoefficient L p.1 p.2 4,
    twoRemoteFirstJetCoefficient L p.1 p.2 5,
    fun m => twoRemoteFirstJetCoefficient L p.1 p.2 0 m -
      twoRemoteFirstJetCoefficient L p.1 p.2 3 m]

private def rowResponse {L r : ℝ} {n : ℕ}
    (a : Fin n → SourceMode 2 → ℝ) (F : RawPinFreeFrame L r n) :
    (Fin n → ℝ) →L[ℝ] (Fin n → ℝ) :=
  ContinuousLinearMap.pi (fun i => ∑ j : Fin n,
    finitePairing (a i) (F.chi j) • ContinuousLinearMap.proj j)

private theorem rowResponse_apply {L r : ℝ} {n : ℕ}
    (a : Fin n → SourceMode 2 → ℝ) (F : RawPinFreeFrame L r n)
    (z : Fin n → ℝ) (i : Fin n) :
    rowResponse a F z i = ∑ j, finitePairing (a i) (F.chi j) * z j := by
  simp [rowResponse]

private theorem finitePairing_hasSum {ι : Type*} (a : ι → ℝ) (v : ι →₀ ℝ) :
    HasSum (fun m => a m * v m) (finitePairing a v) := by
  classical
  apply hasSum_sum_of_ne_finset_zero
  intro m hm
  simp only [Finsupp.notMem_support_iff.mp hm, mul_zero]

private theorem finitePairing_linearCombination {ι : Type*}
    (a : ι → ℝ) (v : ι →₀ ℝ) :
    finitePairing a v = Finsupp.linearCombination ℝ a v := by
  simp only [finitePairing,Finsupp.linearCombination_apply,smul_eq_mul,mul_comm]

private theorem finitePairing_lift {ι : Type*} {n : ℕ}
    (a : ι → ℝ) (v : Fin n → ι →₀ ℝ) (z : Fin n → ℝ) :
    finitePairing a (∑ j, z j • v j) = ∑ j, z j * finitePairing a (v j) := by
  classical
  simp only [finitePairing_linearCombination,map_sum,map_smul,smul_eq_mul]

private theorem finiteShift_derivative {L : ℝ} (hL : L ≠ 0)
    (v : SourceMode 2 →₀ ℝ) (ω : SmoothSample 2 L) (k : ℕ)
    (x : Point2) (u : Fin k → Point2) :
    iteratedFDeriv ℝ k (smoothSourceField 2 L (finiteShiftSample v ω)) x u =
      iteratedFDeriv ℝ k (smoothSourceField 2 L ω) x u +
        finitePairing (derivativeCoefficient 2 L k x u) v := by
  rw [smoothSourceField_derivative_series 2 hL,smoothSourceField_derivative_series 2 hL]
  have h := (derivativeCoefficient_weighted_summable hL ω k x u).hasSum.add
    (finitePairing_hasSum (derivativeCoefficient 2 L k x u) v)
  change (∑' m, derivativeCoefficient 2 L k x u m * (ω.val m + v m)) = _
  simpa only [mul_add] using h.tsum_eq

private theorem freeShift_derivative {L r : ℝ} {n : ℕ} (hL : L ≠ 0)
    (F : RawPinFreeFrame L r n) (z : Fin n → ℝ) (ω : SmoothSample 2 L)
    (k : ℕ) (x : Point2) (u : Fin k → Point2) :
    iteratedFDeriv ℝ k (smoothSourceField 2 L (freeShiftSample F z ω)) x u =
      iteratedFDeriv ℝ k (smoothSourceField 2 L ω) x u +
        ∑ j, z j * finitePairing (derivativeCoefficient 2 L k x u) (F.chi j) := by
  change iteratedFDeriv ℝ k
    (smoothSourceField 2 L (finiteShiftSample (∑ j, z j • F.chi j) ω)) x u = _
  rw [finiteShift_derivative hL,finitePairing_lift]

private theorem rawKernel_null_of_sections {L r : ℝ} {n : ℕ}
    (hL : L ≠ 0) (F : RawPinFreeFrame L r n) (t : Fin 6 → ℝ)
    (A : Set (SmoothSample 2 L)) (hA : MeasurableSet A)
    (hsections : ∀ ρ : SmoothSample 2 L,
      (Measure.pi (fun _ : Fin n => gaussianReal 0 1))
        {z | freeShiftSample F z (rawPosteriorSample hL r t ρ) ∈ A} = 0) :
    rawPinKernel hL r t A = 0 := by
  have hp : Measurable (rawPosteriorSample hL r t) :=
    (rawPosteriorSample_measurable hL r).comp (measurable_const.prodMk measurable_id)
  let φ : SmoothSample 2 L × (Fin n → ℝ) → SmoothSample 2 L :=
    fun p => freeShiftSample F p.2 (rawPosteriorSample hL r t p.1)
  have hφ : Measurable φ := (freeMaps_measurable F).2.1.comp
    (measurable_snd.prodMk (hp.comp measurable_fst))
  have hprod : (((smoothLaw 2 L).map (freeResidualSample F)).prod
      (Measure.pi (fun _ : Fin n => gaussianReal 0 1))) (φ ⁻¹' A) = 0 := by
    apply Measure.measure_prod_null_of_ae_null (hφ hA)
    exact Filter.Eventually.of_forall hsections
  rw [← freeResidual_freeCoordinate_joint_map hL F,
    Measure.map_apply ((freeMaps_measurable F).2.2.prodMk
      (freeMaps_measurable F).1) (hφ hA)] at hprod
  rw [rawPinKernel_apply,Measure.map_apply hp hA]
  convert hprod using 1
  ext ω
  simp only [Set.mem_preimage,φ]
  rw [← rawPosteriorSample_free_reconstruction hL F t ω]

end I4SourceGapConditionalMorseDistinct
