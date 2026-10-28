import Mathlib.Analysis.Normed.Module.FiniteDimension
import Mathlib.Topology.Bases
import Mathlib.Topology.MetricSpace.ProperSpace
import Mathlib.MeasureTheory.OuterMeasure.AE
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
open I4SourceSmoothConditional I4SourceGaussian I4SourceCovariance I4SourceDerivativeGaussian
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
  have heq : (rawPosteriorSample hL r t) ⁻¹' A =
      (fun ω => (freeResidualSample F ω,freeCoordinate F ω)) ⁻¹' (φ ⁻¹' A) := by
    ext ω
    simp only [Set.mem_preimage,φ]
    rw [← rawPosteriorSample_free_reconstruction hL F t ω]
  rw [heq]
  exact hprod

/-!
Private deterministic countable compact-subchart and a.e. globalization
application. Insert inside the frozen59 namespace/noncomputable context.
Original text identifier: GAP_MORSE_GLOBAL_COVER_TEXT_V1.
-/

private theorem countable_compact_response_subcharts
    {X J : Type*} [MetricSpace X] [ProperSpace X]
    [SecondCountableTopology X]
    (S : Set X) (hS : IsOpen S) (V : J → Set X)
    (hV : ∀ j, IsOpen (V j))
    (hcover : ∀ x ∈ S, ∃ j, x ∈ V j) :
    ∃ (K : S → Set X) (chart : S → J) (T : Set S),
      T.Countable ∧
      (∀ x : S, IsCompact (K x) ∧ K x ⊆ S ∩ V (chart x) ∧
        (x : X) ∈ interior (K x)) ∧
      S ⊆ ⋃ x ∈ T, interior (K x) := by
  classical
  have hsmall : ∀ x : S, ∃ j : J, ∃ radius : ℝ,
      0 < radius ∧ Metric.closedBall (x : X) radius ⊆ S ∩ V j := by
    intro x
    obtain ⟨j, hj⟩ := hcover (x : X) x.property
    obtain ⟨radius, hradius, hball⟩ :=
      Metric.isOpen_iff.mp (hS.inter (hV j)) (x : X) ⟨x.property, hj⟩
    refine ⟨j, radius / 2, half_pos hradius, ?_⟩
    exact (Metric.closedBall_subset_ball (half_lt_self hradius)).trans hball
  let chart : S → J := fun x => Classical.choose (hsmall x)
  let radius : S → ℝ := fun x =>
    Classical.choose (Classical.choose_spec (hsmall x))
  let K : S → Set X := fun x => Metric.closedBall (x : X) (radius x)
  have hradius : ∀ x : S,
      0 < radius x ∧ K x ⊆ S ∩ V (chart x) := by
    intro x
    exact Classical.choose_spec (Classical.choose_spec (hsmall x))
  have hK : ∀ x : S, IsCompact (K x) ∧ K x ⊆ S ∩ V (chart x) ∧
      (x : X) ∈ interior (K x) := by
    intro x
    refine ⟨isCompact_closedBall (x : X) (radius x), (hradius x).2, ?_⟩
    exact Metric.ball_subset_interior_closedBall
      (Metric.mem_ball_self (hradius x).1)
  obtain ⟨T, hT, hTcover⟩ :=
    isOpen_iUnion_countable (fun x : S => interior (K x))
      (fun _ => isOpen_interior)
  refine ⟨K, chart, T, hT, hK, ?_⟩
  intro x hx
  rw [hTcover]
  exact Set.mem_iUnion.mpr ⟨⟨x, hx⟩, (hK ⟨x, hx⟩).2.2⟩

private theorem ae_forall_of_countable_subcharts
    {X Ω : Type*} [TopologicalSpace X] [MeasurableSpace Ω]
    (μ : Measure Ω) (S : Set X) (K : S → Set X) (T : Set S)
    (hT : T.Countable)
    (hcover : S ⊆ ⋃ x ∈ T, interior (K x))
    (P : Ω → X → Prop)
    (hP : ∀ x ∈ T, ∀ᵐ ω ∂μ, ∀ y ∈ K x, P ω y) :
    ∀ᵐ ω ∂μ, ∀ y ∈ S, P ω y := by
  have hall : ∀ᵐ ω ∂μ, ∀ x ∈ T, ∀ y ∈ K x, P ω y :=
    (MeasureTheory.ae_ball_iff hT).mpr hP
  refine hall.mono ?_
  intro ω hω y hy
  obtain ⟨x, hx⟩ := Set.mem_iUnion.mp (hcover hy)
  obtain ⟨hxT, hyK⟩ := Set.mem_iUnion.mp hx
  exact hω x hxT y (Set.interior_subset hyK)

private theorem countable_compact_local_ae
    {X Ω : Type*} [NormedAddCommGroup X] [NormedSpace ℝ X]
    [FiniteDimensional ℝ X] [MeasurableSpace Ω]
    (μ : Measure Ω) (S : Set X) (hS : IsOpen S) (P : Ω → X → Prop)
    (hlocal : ∀ x ∈ S, ∃ U : Set X, IsOpen U ∧ x ∈ U ∧ U ⊆ S ∧
      ∀ K : Set X, IsCompact K → K ⊆ U → ∀ᵐ ω ∂μ, ∀ y ∈ K, P ω y) :
    ∀ᵐ ω ∂μ, ∀ y ∈ S, P ω y := by
  classical
  let V : S → Set X := fun x => Classical.choose (hlocal (x : X) x.property)
  have hV : ∀ x : S, IsOpen (V x) ∧ (x : X) ∈ V x ∧ V x ⊆ S ∧
      ∀ K : Set X, IsCompact K → K ⊆ V x → ∀ᵐ ω ∂μ, ∀ y ∈ K, P ω y := by
    intro x
    exact Classical.choose_spec (hlocal (x : X) x.property)
  have hcoverV : ∀ x ∈ S, ∃ j : S, x ∈ V j := by
    intro x hx
    exact ⟨⟨x, hx⟩, (hV ⟨x, hx⟩).2.1⟩
  obtain ⟨K, chart, T, hT, hK, hcover⟩ :=
    countable_compact_response_subcharts S hS V (fun x => (hV x).1) hcoverV
  refine ae_forall_of_countable_subcharts μ S K T hT hcover P ?_
  intro x _hxT
  exact (hV (chart x)).2.2.2 (K x) (hK x).1
    ((hK x).2.1.trans Set.inter_subset_right)

end I4SourceGapConditionalMorseDistinct
