import Mathlib.Analysis.InnerProductSpace.GramSchmidtOrtho
import Mathlib.Analysis.InnerProductSpace.PiL2
import Mathlib.LinearAlgebra.FiniteDimensional.Basic
import Mathlib.Tactic.Ring
import SourceMorseIncidence
import Mathlib.Analysis.Calculus.FDeriv.CompCLM
import Mathlib.Analysis.Calculus.ContDiff.Operations
import Mathlib.Topology.Algebra.Module.ContinuousLinearMap.Invertible
import Mathlib.Analysis.Normed.Operator.Banach
import Mathlib.MeasureTheory.Function.Jacobian
import Mathlib.MeasureTheory.Constructions.Pi
import Mathlib.MeasureTheory.Measure.Prod
import Mathlib.Probability.Distributions.Gaussian.Real
import Mathlib.Tactic.FinCases
import Mathlib.Tactic.NormNum
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
open scoped BigOperators Topology Matrix NNReal
open Set MeasureTheory MeasureTheory.Measure ProbabilityTheory I4Foundation I4Source I4Smooth I4SmoothCarrier
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
  simpa only [mul_add,scalarSeries,sampleInclusion] using h.tsum_eq

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
    TopologicalSpace.isOpen_iUnion_countable (fun x : S => interior (K x))
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
  exact hω x hxT y (interior_subset hyK)

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

/- Complete text-only helper B. Insert once INSIDE namespace
   I4SourceGapConditionalMorseDistinct after the frozen private aliases.
   No namespace wrapper is added here. Every declaration is private. -/

private theorem incidence_clm_isInvertible
    {C : Type*} [NormedAddCommGroup C] [NormedSpace ℝ C]
    [FiniteDimensional ℝ C] (A : C →L[ℝ] C) (hA : Function.Bijective A) :
    A.IsInvertible := by
  let e : C ≃L[ℝ] C := (LinearEquiv.ofBijective A.toLinearMap hA).toContinuousLinearEquiv
  refine ⟨e,?_⟩
  ext v
  rfl

private def incidence_theta
    {D C : Type*} [NormedAddCommGroup D] [NormedSpace ℝ D]
    [NormedAddCommGroup C] [NormedSpace ℝ C]
    (g : D → C) (B : D → C →L[ℝ] C) (x : D) : C :=
  -((B x).inverse (g x))

private theorem incidence_theta_section
    {D C : Type*} [NormedAddCommGroup D] [NormedSpace ℝ D]
    [NormedAddCommGroup C] [NormedSpace ℝ C] [FiniteDimensional ℝ C]
    (g : D → C) (B : D → C →L[ℝ] C) (x : D)
    (hinv : Function.Bijective (B x)) :
    g x+B x (incidence_theta g B x)=0 := by
  have hI := incidence_clm_isInvertible (B x) hinv
  simp only [incidence_theta,map_neg,hI.self_apply_inverse,add_neg_cancel]

private theorem incidence_constraint_unique
    {D C : Type*} [NormedAddCommGroup D] [NormedSpace ℝ D]
    [NormedAddCommGroup C] [NormedSpace ℝ C] [FiniteDimensional ℝ C]
    (g : D → C) (B : D → C →L[ℝ] C) (x : D)
    (hinv : Function.Bijective (B x)) (z : C) (hz : g x+B x z=0) :
    z=incidence_theta g B x := by
  apply hinv.1
  apply add_left_cancel (a := g x)
  exact hz.trans (incidence_theta_section g B x hinv).symm

private theorem incidence_constraint_parameters_image
    {D C : Type*} [NormedAddCommGroup D] [NormedSpace ℝ D]
    [NormedAddCommGroup C] [NormedSpace ℝ C] [FiniteDimensional ℝ C]
    (U : Set D) (g : D → C) (B : D → C →L[ℝ] C)
    (hinv : ∀ x∈U, Function.Bijective (B x)) :
    {z | ∃ x∈U, g x+B x z=0}=incidence_theta g B '' U := by
  ext z
  constructor
  · rintro ⟨x,hx,hz⟩
    exact ⟨x,hx,(incidence_constraint_unique g B x (hinv x hx) z hz).symm⟩
  · rintro ⟨x,hx,rfl⟩
    exact ⟨x,hx,incidence_theta_section g B x (hinv x hx)⟩

private theorem incidence_theta_differentiable
    {D C : Type*} [NormedAddCommGroup D] [NormedSpace ℝ D]
    [NormedAddCommGroup C] [NormedSpace ℝ C] [FiniteDimensional ℝ C]
    (U : Set D) (hU : IsOpen U) (g : D → C) (B : D → C →L[ℝ] C)
    (hg : ContDiffOn ℝ (⊤ : ℕ∞) g U) (hB : ContDiffOn ℝ (⊤ : ℕ∞) B U)
    (hinv : ∀ x∈U, Function.Bijective (B x)) (x : D) (hx : x∈U) :
    DifferentiableAt ℝ (incidence_theta g B) x := by
  have hBc : ContDiffAt ℝ (⊤ : ℕ∞) B x :=
    (hB x hx).contDiffAt (hU.mem_nhds hx)
  have hgc : ContDiffAt ℝ (⊤ : ℕ∞) g x :=
    (hg x hx).contDiffAt (hU.mem_nhds hx)
  have hIc : ContDiffAt ℝ (⊤ : ℕ∞) ContinuousLinearMap.inverse (B x) :=
    (incidence_clm_isInvertible (B x) (hinv x hx)).contDiffAt_map_inverse
  have hId : DifferentiableAt ℝ (fun y => (B y).inverse) x :=
    (hIc.comp x hBc).differentiableAt (by simp)
  have hgd : DifferentiableAt ℝ g x := hgc.differentiableAt (by simp)
  simpa only [incidence_theta,Pi.neg_apply] using (hId.clm_apply hgd).neg

/- This is the derivative with the free parameter z HELD FIXED. -/
private theorem incidence_fixed_parameter_derivative
    {D C : Type*} [NormedAddCommGroup D] [NormedSpace ℝ D]
    [NormedAddCommGroup C] [NormedSpace ℝ C]
    (g : D → C) (B : D → C →L[ℝ] C) (x : D) (z : C)
    (hg : DifferentiableAt ℝ g x) (hB : DifferentiableAt ℝ B x) :
    fderiv ℝ (fun y => g y+B y z) x =
      fderiv ℝ g x+(fderiv ℝ B x).flip z := by
  have h := hg.hasFDerivAt.add
    (hB.hasFDerivAt.clm_apply (hasFDerivAt_const z x))
  simpa only [ContinuousLinearMap.comp_zero,zero_add] using h.fderiv

/- Mandatory full variable-response equation. The DB(x)v * theta(x)
   contribution comes from differentiating B(x)theta(x), not from dtheta. -/
private theorem incidence_full_normal_equation
    {D C : Type*} [NormedAddCommGroup D] [NormedSpace ℝ D]
    [NormedAddCommGroup C] [NormedSpace ℝ C] [FiniteDimensional ℝ C]
    (U : Set D) (hU : IsOpen U) (g : D → C) (B : D → C →L[ℝ] C)
    (hg : ContDiffOn ℝ (⊤ : ℕ∞) g U) (hB : ContDiffOn ℝ (⊤ : ℕ∞) B U)
    (hinv : ∀ x∈U, Function.Bijective (B x)) (x : D) (hx : x∈U) (v : D) :
    B x (fderiv ℝ (incidence_theta g B) x v) =
      -(fderiv ℝ g x v+(fderiv ℝ B x v) (incidence_theta g B x)) := by
  have hgd : DifferentiableAt ℝ g x :=
    ((hg x hx).contDiffAt (hU.mem_nhds hx)).differentiableAt (by simp)
  have hBd : DifferentiableAt ℝ B x :=
    ((hB x hx).contDiffAt (hU.mem_nhds hx)).differentiableAt (by simp)
  have htd := incidence_theta_differentiable U hU g B hg hB hinv x hx
  have hall := hgd.hasFDerivAt.add (hBd.hasFDerivAt.clm_apply htd.hasFDerivAt)
  have heq : (fun y => g y+B y (incidence_theta g B y)) =ᶠ[𝓝 x] (fun _ => (0 : C)) := by
    filter_upwards [hU.mem_nhds hx] with y hy
    exact incidence_theta_section g B y (hinv y hy)
  have hz : fderiv ℝ (fun y => g y+B y (incidence_theta g B y)) x=0 := by
    rw [heq.fderiv_eq]
    simp
  have hv := congrArg (fun A : D →L[ℝ] C => A v) (hall.fderiv.symm.trans hz)
  change fderiv ℝ g x v+
    (B x (fderiv ℝ (incidence_theta g B) x v)+
      (fderiv ℝ B x v) (incidence_theta g B x))=0 at hv
  apply eq_neg_iff_add_eq_zero.mpr
  simpa only [add_assoc,add_comm,add_left_comm] using hv

private theorem incidence_normal_equation_shifted
    {D C : Type*} [NormedAddCommGroup D] [NormedSpace ℝ D]
    [NormedAddCommGroup C] [NormedSpace ℝ C] [FiniteDimensional ℝ C]
    (U : Set D) (hU : IsOpen U) (g : D → C) (B : D → C →L[ℝ] C)
    (hg : ContDiffOn ℝ (⊤ : ℕ∞) g U) (hB : ContDiffOn ℝ (⊤ : ℕ∞) B U)
    (hinv : ∀ x∈U, Function.Bijective (B x)) (x : D) (hx : x∈U) (v : D) :
    B x (fderiv ℝ (incidence_theta g B) x v) =
      -(fderiv ℝ (fun y => g y+B y (incidence_theta g B x)) x v) := by
  have hgd : DifferentiableAt ℝ g x :=
    ((hg x hx).contDiffAt (hU.mem_nhds hx)).differentiableAt (by simp)
  have hBd : DifferentiableAt ℝ B x :=
    ((hB x hx).contDiffAt (hU.mem_nhds hx)).differentiableAt (by simp)
  rw [incidence_fixed_parameter_derivative g B x (incidence_theta g B x) hgd hBd]
  exact incidence_full_normal_equation U hU g B hg hB hinv x hx v

private theorem incidence_det_zero_of_killed_nonzero
    {V : Type*} [NormedAddCommGroup V] [NormedSpace ℝ V]
    [FiniteDimensional ℝ V] (A : V →L[ℝ] V) (w : V)
    (hw : w≠0) (hAw : A w=0) : A.det=0 := by
  apply LinearMap.det_eq_zero_iff_ker_ne_bot.mpr
  intro hker
  have hi : Function.Injective A := LinearMap.ker_eq_bot.mp hker
  apply hw
  apply hi
  simpa only [map_zero] using hAw

private theorem incidence_singular_image_null
    {V : Type*} [NormedAddCommGroup V] [NormedSpace ℝ V]
    [FiniteDimensional ℝ V] [MeasurableSpace V] [BorelSpace V]
    (μ : Measure V) [IsAddHaarMeasure μ] (theta : V → V) (S : Set V)
    (htheta : ∀ x∈S, DifferentiableAt ℝ theta x)
    (hsing : ∀ x∈S, ¬Function.Injective (fderiv ℝ theta x)) :
    μ (theta '' S)=0 := by
  apply addHaar_image_eq_zero_of_det_fderivWithin_eq_zero μ (f' := fderiv ℝ theta)
  · intro x hx
    exact (htheta x hx).hasFDerivAt.hasFDerivWithinAt
  · intro x hx
    apply LinearMap.det_eq_zero_iff_ker_ne_bot.mpr
    intro hker
    exact hsing x hx (LinearMap.ker_eq_bot.mp hker)

private theorem incidence_theta_singular
    (U : Set Point2) (hU : IsOpen U) (g : Point2 → Point2)
    (B : Point2 → Point2 →L[ℝ] Point2)
    (hg : ContDiffOn ℝ (⊤ : ℕ∞) g U) (hB : ContDiffOn ℝ (⊤ : ℕ∞) B U)
    (hinv : ∀ x∈U, Function.Bijective (B x)) (x : Point2) (hx : x∈U)
    (hH : ¬Function.Injective
      (fderiv ℝ (fun y => g y+B y (incidence_theta g B x)) x)) :
    ¬Function.Injective (fderiv ℝ (incidence_theta g B) x) := by
  let D := fderiv ℝ (incidence_theta g B) x
  let H := fderiv ℝ (fun y => g y+B y (incidence_theta g B x)) x
  let A : (Point2 × ℝ) →L[ℝ] (Point2 × ℝ) :=
    (D.comp (ContinuousLinearMap.fst ℝ Point2 ℝ)).prod
      (ContinuousLinearMap.snd ℝ Point2 ℝ)
  have hA : ¬Function.Injective A :=
    I4ActualSourceMorse.incidence_noninjective_of_normal_equations A (B x) H
      (hinv x hx).1 hH (fun _ => rfl) (fun v =>
        incidence_normal_equation_shifted U hU g B hg hB hinv x hx v)
  intro hD
  apply hA
  intro a b hab
  apply Prod.ext
  · apply hD
    have hh := congrArg Prod.fst hab
    change D a.1=D b.1 at hh
    exact hh
  · have hh := congrArg Prod.snd hab
    change a.2=b.2 at hh
    exact hh

private theorem incidence_gaussian_pi_ac (n : ℕ) :
    (Measure.pi (fun _ : Fin n => gaussianReal 0 1)) ≪
      (volume : Measure (Fin n → ℝ)) := by
  induction n with
  | zero =>
      change (Measure.pi (fun _ : Fin 0 => gaussianReal 0 1)) ≪
        Measure.pi (fun _ : Fin 0 => (volume : Measure ℝ))
      rw [Measure.pi_of_empty _ (0 : Fin 0 → ℝ),Measure.pi_of_empty _ (0 : Fin 0 → ℝ)]
  | succ n ih =>
      let e := MeasurableEquiv.piFinSuccAbove (fun _ : Fin (n+1) => ℝ) (0 : Fin (n+1))
      have hG := measurePreserving_piFinSuccAbove
        (fun _ : Fin (n+1) => gaussianReal 0 1) (0 : Fin (n+1))
      have hV := volume_preserving_piFinSuccAbove
        (fun _ : Fin (n+1) => ℝ) (0 : Fin (n+1))
      have hp : (gaussianReal 0 1).prod (Measure.pi (fun _ : Fin n => gaussianReal 0 1)) ≪
          (volume : Measure ℝ).prod (volume : Measure (Fin n → ℝ)) :=
        (gaussianReal_absolutelyContinuous 0 (by norm_num : (1 : ℝ≥0)≠0)).prod ih
      have h := e.symm.measurableEmbedding.absolutelyContinuous_map hp
      rw [(hG.symm e).map_eq,(hV.symm e).map_eq] at h
      exact h

private theorem incidence_gaussian3_ac :
    (Measure.pi (fun _ : Fin 3 => gaussianReal 0 1)) ≪
      (volume : Measure (Fin 3 → ℝ)) := incidence_gaussian_pi_ac 3

private theorem incidence_gaussian5_ac :
    (Measure.pi (fun _ : Fin 5 => gaussianReal 0 1)) ≪
      (volume : Measure (Fin 5 → ℝ)) := incidence_gaussian_pi_ac 5

private theorem incidence_morse_null
    (U : Set Point2) (hU : IsOpen U) (g : Point2 → Point2)
    (B : Point2 → Point2 →L[ℝ] Point2)
    (hg : ContDiffOn ℝ (⊤ : ℕ∞) g U) (hB : ContDiffOn ℝ (⊤ : ℕ∞) B U)
    (hinv : ∀ x∈U, Function.Bijective (B x)) :
    (Measure.pi (fun _ : Fin 2 => gaussianReal 0 1))
      {z | ∃ x∈U, g x+B x z=0 ∧
        ¬Function.Injective (fderiv ℝ (fun y => g y+B y z) x)}=0 := by
  let theta := incidence_theta g B
  let S : Set Point2 := {x | x∈U ∧ ¬Function.Injective (fderiv ℝ theta x)}
  have hnull : (volume : Measure Point2) (theta '' S)=0 :=
    incidence_singular_image_null volume theta S
      (fun x hx => incidence_theta_differentiable U hU g B hg hB hinv x hx.1)
      (fun _ hx => hx.2)
  apply measure_mono_null ?_ ((I4ActualSourceMorse.gaussian_two_absolutelyContinuous
    (fun _ => 0) (fun _ => 1) (fun _ => one_ne_zero)) hnull)
  rintro z ⟨x,hx,hzero,hH⟩
  have hz : z=theta x := incidence_constraint_unique g B x (hinv x hx) z hzero
  refine ⟨x,⟨hx,?_⟩,hz.symm⟩
  apply incidence_theta_singular U hU g B hg hB hinv x hx
  simpa only [hz] using hH

/- Explicit flattenings: (y0,y1,s) and (u0,u1,v0,v1,s).
   The final coordinate is not used by either projection. -/
private def incidence_project3 : (Fin 3 → ℝ) →L[ℝ] Point2 :=
  ContinuousLinearMap.pi ![ContinuousLinearMap.proj (0 : Fin 3),ContinuousLinearMap.proj 1]

private def incidence_embed3 (p : Point2) : Fin 3 → ℝ := ![p 0,p 1,0]

private def incidence_project5 : (Fin 5 → ℝ) →L[ℝ] Point4 :=
  (ContinuousLinearMap.pi ![ContinuousLinearMap.proj (0 : Fin 5),ContinuousLinearMap.proj 1]).prod
    (ContinuousLinearMap.pi ![ContinuousLinearMap.proj (2 : Fin 5),ContinuousLinearMap.proj 3])

private def incidence_embed5 (p : Point4) : Fin 5 → ℝ := ![p.1 0,p.1 1,p.2 0,p.2 1,0]

private theorem incidence_project3_apply (x : Fin 3 → ℝ) :
    incidence_project3 x=![x 0,x 1] := by
  ext i
  fin_cases i <;> rfl

private theorem incidence_project5_apply (x : Fin 5 → ℝ) :
    incidence_project5 x=(![x 0,x 1],![x 2,x 3]) := by
  apply Prod.ext <;> funext i <;> fin_cases i <;> rfl

private theorem incidence_project3_embed3 (p : Point2) :
    incidence_project3 (incidence_embed3 p)=p := by
  ext i
  fin_cases i <;> rfl

private theorem incidence_project5_embed5 (p : Point4) :
    incidence_project5 (incidence_embed5 p)=p := by
  apply Prod.ext <;> funext i <;> fin_cases i <;> rfl

private theorem incidence_dummy3_kernel_vector :
    (Pi.single (2 : Fin 3) (1 : ℝ) : Fin 3 → ℝ)≠0 ∧
      incidence_project3 (Pi.single (2 : Fin 3) (1 : ℝ))=0 := by
  constructor
  · intro h
    have hh := congrFun h (2 : Fin 3)
    norm_num [Pi.single_apply] at hh
  · rw [incidence_project3_apply]
    ext i
    fin_cases i <;> norm_num [Pi.single_apply]

private theorem incidence_dummy5_kernel_vector :
    (Pi.single (4 : Fin 5) (1 : ℝ) : Fin 5 → ℝ)≠0 ∧
      incidence_project5 (Pi.single (4 : Fin 5) (1 : ℝ))=0 := by
  constructor
  · intro h
    have hh := congrFun h (4 : Fin 5)
    norm_num [Pi.single_apply] at hh
  · rw [incidence_project5_apply]
    apply Prod.ext <;> funext i <;> fin_cases i <;> norm_num [Pi.single_apply]

private theorem incidence_composite_kills
    {D V : Type*} [NormedAddCommGroup D] [NormedSpace ℝ D]
    [NormedAddCommGroup V] [NormedSpace ℝ V]
    (P : V →L[ℝ] D) (theta : D → V) (x w : V)
    (htheta : DifferentiableAt ℝ theta (P x)) (hPw : P w=0) :
    fderiv ℝ (fun y => theta (P y)) x w=0 := by
  change fderiv ℝ (theta ∘ P) x w=0
  rw [(htheta.hasFDerivAt.comp x P.hasFDerivAt).fderiv]
  change fderiv ℝ theta (P x) (P w)=0
  rw [hPw,map_zero]

private theorem incidence_dummy3_derivative_kernel
    (theta : Point2 → (Fin 3 → ℝ)) (x : Fin 3 → ℝ)
    (htheta : DifferentiableAt ℝ theta (incidence_project3 x)) :
    fderiv ℝ (fun y => theta (incidence_project3 y)) x
      (Pi.single (2 : Fin 3) (1 : ℝ))=0 :=
  incidence_composite_kills incidence_project3 theta x _ htheta incidence_dummy3_kernel_vector.2

private theorem incidence_dummy5_derivative_kernel
    (theta : Point4 → (Fin 5 → ℝ)) (x : Fin 5 → ℝ)
    (htheta : DifferentiableAt ℝ theta (incidence_project5 x)) :
    fderiv ℝ (fun y => theta (incidence_project5 y)) x
      (Pi.single (4 : Fin 5) (1 : ℝ))=0 :=
  incidence_composite_kills incidence_project5 theta x _ htheta incidence_dummy5_kernel_vector.2

private theorem incidence_dummy3_det_zero
    (theta : Point2 → (Fin 3 → ℝ)) (x : Fin 3 → ℝ)
    (htheta : DifferentiableAt ℝ theta (incidence_project3 x)) :
    (fderiv ℝ (fun y => theta (incidence_project3 y)) x).det=0 :=
  incidence_det_zero_of_killed_nonzero _ _ incidence_dummy3_kernel_vector.1
    (incidence_dummy3_derivative_kernel theta x htheta)

private theorem incidence_dummy5_det_zero
    (theta : Point4 → (Fin 5 → ℝ)) (x : Fin 5 → ℝ)
    (htheta : DifferentiableAt ℝ theta (incidence_project5 x)) :
    (fderiv ℝ (fun y => theta (incidence_project5 y)) x).det=0 :=
  incidence_det_zero_of_killed_nonzero _ _ incidence_dummy5_kernel_vector.1
    (incidence_dummy5_derivative_kernel theta x htheta)

private theorem incidence_dummy_image_inclusion
    {D V : Type*} [NormedAddCommGroup D] [NormedSpace ℝ D]
    [NormedAddCommGroup V] [NormedSpace ℝ V]
    (P : V →L[ℝ] D) (J : D → V) (hPJ : ∀ x, P (J x)=x)
    (theta : D → V) (U : Set D) :
    theta '' U ⊆ (fun y => theta (P y)) '' (P ⁻¹' U) := by
  rintro z ⟨x,hx,rfl⟩
  refine ⟨J x,?_,?_⟩
  · change P (J x)∈U
    rw [hPJ]
    exact hx
  · change theta (P (J x))=theta x
    rw [hPJ]

private theorem incidence_dummy3_image_inclusion
    (theta : Point2 → (Fin 3 → ℝ)) (U : Set Point2) :
    theta '' U ⊆ (fun y => theta (incidence_project3 y)) '' (incidence_project3 ⁻¹' U) :=
  incidence_dummy_image_inclusion incidence_project3 incidence_embed3 incidence_project3_embed3 theta U

private theorem incidence_dummy5_image_inclusion
    (theta : Point4 → (Fin 5 → ℝ)) (U : Set Point4) :
    theta '' U ⊆ (fun y => theta (incidence_project5 y)) '' (incidence_project5 ⁻¹' U) :=
  incidence_dummy_image_inclusion incidence_project5 incidence_embed5 incidence_project5_embed5 theta U

private theorem incidence_dummy_image_null
    {D V : Type*} [NormedAddCommGroup D] [NormedSpace ℝ D]
    [NormedAddCommGroup V] [NormedSpace ℝ V] [FiniteDimensional ℝ V]
    [MeasurableSpace V] [BorelSpace V]
    (μ : Measure V) [IsAddHaarMeasure μ]
    (P : V →L[ℝ] D) (J : D → V) (hPJ : ∀ x, P (J x)=x)
    (w : V) (hw : w≠0) (hPw : P w=0)
    (theta : D → V) (U : Set D)
    (htheta : ∀ x∈U, DifferentiableAt ℝ theta x) :
    μ (theta '' U)=0 := by
  have hnull : μ ((fun y => theta (P y)) '' (P ⁻¹' U))=0 := by
    apply addHaar_image_eq_zero_of_det_fderivWithin_eq_zero μ
      (f' := fderiv ℝ (fun y => theta (P y)))
    · intro x hx
      exact ((htheta (P x) hx).hasFDerivAt.comp x P.hasFDerivAt).hasFDerivWithinAt
    · intro x hx
      exact incidence_det_zero_of_killed_nonzero _ w hw
        (incidence_composite_kills P theta x w (htheta (P x) hx) hPw)
  exact measure_mono_null (incidence_dummy_image_inclusion P J hPJ theta U) hnull

private theorem incidence_dummy3_image_null
    (theta : Point2 → (Fin 3 → ℝ)) (U : Set Point2)
    (htheta : ∀ x∈U, DifferentiableAt ℝ theta x) :
    (volume : Measure (Fin 3 → ℝ)) (theta '' U)=0 :=
  incidence_dummy_image_null volume incidence_project3 incidence_embed3 incidence_project3_embed3
    _ incidence_dummy3_kernel_vector.1 incidence_dummy3_kernel_vector.2 theta U htheta

private theorem incidence_dummy5_image_null
    (theta : Point4 → (Fin 5 → ℝ)) (U : Set Point4)
    (htheta : ∀ x∈U, DifferentiableAt ℝ theta x) :
    (volume : Measure (Fin 5 → ℝ)) (theta '' U)=0 :=
  incidence_dummy_image_null volume incidence_project5 incidence_embed5 incidence_project5_embed5
    _ incidence_dummy5_kernel_vector.1 incidence_dummy5_kernel_vector.2 theta U htheta

private theorem incidence_level_null
    (U : Set Point2) (hU : IsOpen U) (g : Point2 → (Fin 3 → ℝ))
    (B : Point2 → (Fin 3 → ℝ) →L[ℝ] (Fin 3 → ℝ))
    (hg : ContDiffOn ℝ (⊤ : ℕ∞) g U) (hB : ContDiffOn ℝ (⊤ : ℕ∞) B U)
    (hinv : ∀ x∈U, Function.Bijective (B x)) :
    (Measure.pi (fun _ : Fin 3 => gaussianReal 0 1)) {z | ∃ x∈U,g x+B x z=0}=0 := by
  rw [incidence_constraint_parameters_image U g B hinv]
  apply incidence_gaussian3_ac
  exact incidence_dummy3_image_null (incidence_theta g B) U
    (fun x hx => incidence_theta_differentiable U hU g B hg hB hinv x hx)

private theorem incidence_tie_null
    (U : Set Point4) (hU : IsOpen U) (g : Point4 → (Fin 5 → ℝ))
    (B : Point4 → (Fin 5 → ℝ) →L[ℝ] (Fin 5 → ℝ))
    (hg : ContDiffOn ℝ (⊤ : ℕ∞) g U) (hB : ContDiffOn ℝ (⊤ : ℕ∞) B U)
    (hinv : ∀ x∈U, Function.Bijective (B x)) :
    (Measure.pi (fun _ : Fin 5 => gaussianReal 0 1)) {z | ∃ x∈U,g x+B x z=0}=0 := by
  rw [incidence_constraint_parameters_image U g B hinv]
  apply incidence_gaussian5_ac
  exact incidence_dummy5_image_null (incidence_theta g B) U
    (fun x hx => incidence_theta_differentiable U hU g B hg hB hinv x hx)

/- TEXT ONLY: insert once inside I4SourceGapConditionalMorseDistinct after
   SHARED_CONTEXT59_V1's private aliases/rows/rowResponse. All declarations here
   are PRIVATE. The only Euclidean space is the finite union of source supports;
   no random coefficient sequence is viewed as an l2 vector. -/

private theorem finiteFrame_pair_lc (a : SourceMode 2 → ℝ)
    (v : SourceMode 2 →₀ ℝ) :
    finitePairing a v = Finsupp.linearCombination ℝ a v := by
  classical
  simp only [finitePairing,Finsupp.linearCombination_apply,Finsupp.sum]
  apply Finset.sum_congr rfl
  intro m hm
  simp only [smul_eq_mul]
  ring

private theorem finiteFrame_pair_sum {ι : Type*} [Fintype ι] (a : SourceMode 2 → ℝ)
    (c : ι → ℝ) (v : ι → SourceMode 2 →₀ ℝ) :
    finitePairing a (∑ j, c j • v j) = ∑ j, c j * finitePairing a (v j) := by
  simp only [finiteFrame_pair_lc,map_sum,map_smul,smul_eq_mul]

private theorem finiteFrame_pair_single (a : SourceMode 2 → ℝ) (m : SourceMode 2) :
    finitePairing a (Finsupp.single m 1) = a m := by
  classical
  simp [finitePairing]

private theorem finiteFrame_pair_sub_left (a b : SourceMode 2 → ℝ)
    (v : SourceMode 2 →₀ ℝ) :
    finitePairing (fun m => a m-b m) v = finitePairing a v-finitePairing b v := by
  classical
  simp only [finitePairing,Finsupp.sum,sub_mul,Finset.sum_sub_distrib]

private theorem finiteFrame_response_apply {L r : ℝ} {n : ℕ}
    (a : Fin n → SourceMode 2 → ℝ) (F : RawPinFreeFrame L r n)
    (c : Fin n → ℝ) (i : Fin n) :
    rowResponse a F c i = ∑ j, c j * finitePairing (a i) (F.chi j) := by
  classical
  simp [rowResponse,mul_comm]

private theorem finiteFrame_independent_of_rightInverse {n : ℕ}
    (a : Fin n → SourceMode 2 → ℝ) (v : Fin n → SourceMode 2 →₀ ℝ)
    (hright : ∀ i j, finitePairing (a i) (v j)=if i=j then 1 else 0) :
    LinearIndependent ℝ v := by
  classical
  apply Fintype.linearIndependent_iff.mpr
  intro c hc i
  have h := congrArg (Finsupp.linearCombination ℝ (a i)) hc
  have hi : finitePairing (a i) (∑ j, c j • v j)=0 := by
    simpa only [finiteFrame_pair_lc,map_zero] using h
  rw [finiteFrame_pair_sum] at hi
  simpa only [hright,mul_ite,mul_one,mul_zero,Finset.sum_ite_eq,Finset.mem_univ,
    if_true] using hi

private def finiteFrame_extend (S : Finset (SourceMode 2)) :
    EuclideanSpace ℝ S →ₗ[ℝ] (SourceMode 2 →₀ ℝ) where
  toFun u := ∑ m : S, u m • Finsupp.single m.val 1
  map_add' u v := by
    change (∑ m : S, (u m+v m) • Finsupp.single m.val 1) =
      (∑ m : S, u m • Finsupp.single m.val 1)+(∑ m : S, v m • Finsupp.single m.val 1)
    simp only [add_smul,Finset.sum_add_distrib]
  map_smul' c u := by
    change (∑ m : S, (c*u m) • Finsupp.single m.val 1) =
      c • ∑ m : S, u m • Finsupp.single m.val 1
    simp only [Finset.smul_sum,smul_smul]

private theorem finiteFrame_extend_on (S : Finset (SourceMode 2))
    (u : EuclideanSpace ℝ S) (m : S) : finiteFrame_extend S u m.val=u m := by
  classical
  change (∑ k : S, u k • Finsupp.single k.val 1) m.val=u m
  simp [Finsupp.finsetSum_apply,Finsupp.single_apply,Subtype.coe_inj]

private theorem finiteFrame_extend_off (S : Finset (SourceMode 2))
    (u : EuclideanSpace ℝ S) (m : SourceMode 2) (hm : m ∉ S) :
    finiteFrame_extend S u m=0 := by
  classical
  change (∑ k : S, u k • Finsupp.single k.val 1) m=0
  rw [Finsupp.finsetSum_apply]
  apply Finset.sum_eq_zero
  intro k hk
  have hkm : k.val ≠ m := by intro h; exact hm (h ▸ k.property)
  simp [Finsupp.single_apply,hkm]

private theorem finiteFrame_extend_injective (S : Finset (SourceMode 2)) :
    Function.Injective (finiteFrame_extend S) := by
  intro u v h
  ext m
  have hm := congrArg (fun w : SourceMode 2 →₀ ℝ => w m.val) h
  simpa only [finiteFrame_extend_on] using hm

private theorem finiteFrame_extend_gram (S : Finset (SourceMode 2))
    (u v : EuclideanSpace ℝ S) :
    finitePairing (fun m => finiteFrame_extend S u m) (finiteFrame_extend S v) =
      inner ℝ u v := by
  classical
  change finitePairing (fun m => finiteFrame_extend S u m)
    (∑ k : S, v k • Finsupp.single k.val 1)=_
  rw [finiteFrame_pair_sum]
  simp only [finiteFrame_pair_single,finiteFrame_extend_on,
    EuclideanSpace.inner_eq_star_dotProduct,star_trivial,dotProduct]

/- This intermediate also handles overlapping nonorthogonal source directions.
   The caller must derive LI from actual source data; there is no rank premise
   on the public global theorem. -/
private theorem finiteFrame_of_linearIndependent {L r : ℝ} {n : ℕ}
    (v : Fin n → SourceMode 2 →₀ ℝ) (hv : LinearIndependent ℝ v)
    (hraw : ∀ (i : Fin 6) (j : Fin n),
      finitePairing (rawPinCoefficient L r i) (v j)=0) :
    ∃ F : RawPinFreeFrame L r n,
      Submodule.span ℝ (Set.range F.chi)=Submodule.span ℝ (Set.range v) := by
  classical
  let S : Finset (SourceMode 2) := Finset.univ.biUnion (fun j : Fin n => (v j).support)
  let f : Fin n → EuclideanSpace ℝ S := fun j => WithLp.toLp 2 (fun m : S => v j m.val)
  let E := finiteFrame_extend S
  have hsupport (j : Fin n) : (v j).support ⊆ S := by
    intro m hm
    exact Finset.mem_biUnion.mpr ⟨j,Finset.mem_univ _,hm⟩
  have hEf (j : Fin n) : E (f j)=v j := by
    ext m
    by_cases hm : m ∈ S
    · exact finiteFrame_extend_on S (f j) ⟨m,hm⟩
    · rw [finiteFrame_extend_off S (f j) m hm]
      exact (Finsupp.notMem_support_iff.mp (fun h => hm (hsupport j h))).symm
  have hfi : LinearIndependent ℝ f := by
    apply LinearIndependent.of_comp E
    have he : E ∘ f=v := funext hEf
    rw [he]
    exact hv
  let w : Fin n → EuclideanSpace ℝ S := InnerProductSpace.gramSchmidtNormed ℝ f
  have hw : Orthonormal ℝ w := InnerProductSpace.gramSchmidtNormed_orthonormal hfi
  have hwli : LinearIndependent ℝ w := InnerProductSpace.gramSchmidtNormed_linearIndependent hfi
  let chi : Fin n → (SourceMode 2 →₀ ℝ) := fun j => E (w j)
  have hspan : Submodule.span ℝ (Set.range chi)=Submodule.span ℝ (Set.range v) := by
    have hs : Submodule.span ℝ (Set.range w)=Submodule.span ℝ (Set.range f) :=
      (InnerProductSpace.span_gramSchmidtNormed_range (𝕜 := ℝ) f).trans (InnerProductSpace.span_gramSchmidt ℝ f)
    have hh := congrArg (fun P : Submodule ℝ (EuclideanSpace ℝ S) => P.map E) hs
    simp only [Submodule.map_span,Set.image_range,Function.comp_def] at hh
    have he : (fun j => E (f j))=v := funext hEf
    rw [he] at hh
    exact hh
  have hchiGram (j k : Fin n) :
      finitePairing (fun m => chi j m) (chi k)=if j=k then 1 else 0 := by
    rw [show chi j=finiteFrame_extend S (w j) from rfl,
      show chi k=finiteFrame_extend S (w k) from rfl,finiteFrame_extend_gram]
    exact orthonormal_iff_ite.mp hw j k
  have hchiRaw (i : Fin 6) (j : Fin n) :
      finitePairing (rawPinCoefficient L r i) (chi j)=0 := by
    have hker : Submodule.span ℝ (Set.range v) ≤
        LinearMap.ker (Finsupp.linearCombination ℝ (rawPinCoefficient L r i)) := by
      apply Submodule.span_le.mpr
      rintro u ⟨k,rfl⟩
      change Finsupp.linearCombination ℝ (rawPinCoefficient L r i) (v k)=0
      rw [← finiteFrame_pair_lc]
      exact hraw i k
    have hj : chi j ∈ Submodule.span ℝ (Set.range v) := by
      rw [← hspan]
      exact Submodule.subset_span ⟨j,rfl⟩
    rw [finiteFrame_pair_lc]
    exact hker hj
  exact ⟨⟨chi,hchiGram,hchiRaw⟩,hspan⟩

/- A response/change-of-basis companion is kept separate so an overlapping
   nonorthogonal control can use its normalized span without pretending its
   output response is still the input identity. -/
private theorem finiteFrame_response_bijective_of_same_span {L r : ℝ} {n : ℕ}
    (a : Fin n → SourceMode 2 → ℝ) (v : Fin n → SourceMode 2 →₀ ℝ)
    (hright : ∀ i j, finitePairing (a i) (v j)=if i=j then 1 else 0)
    (F : RawPinFreeFrame L r n)
    (hspan : Submodule.span ℝ (Set.range F.chi)=Submodule.span ℝ (Set.range v)) :
    Function.Bijective (rowResponse a F) := by
  classical
  have hFli : LinearIndependent ℝ F.chi := by
    apply Fintype.linearIndependent_iff.mpr
    intro c hc i
    have hp := congrArg (Finsupp.linearCombination ℝ (fun m => F.chi i m)) hc
    have hz : finitePairing (fun m => F.chi i m) (∑ j,c j • F.chi j)=0 := by
      simpa only [finiteFrame_pair_lc,map_zero] using hp
    rw [finiteFrame_pair_sum] at hz
    simpa only [F.gram,mul_ite,mul_one,mul_zero,Finset.sum_ite_eq,Finset.mem_univ,
      if_true] using hz
  have hinj : Function.Injective (rowResponse a F) := by
    intro c d hcd
    let t : Fin n → ℝ := c-d
    let u : SourceMode 2 →₀ ℝ := ∑ j,t j • F.chi j
    have huSpan : u ∈ Submodule.span ℝ (Set.range v) := by
      rw [← hspan]
      exact Submodule.sum_mem _ (fun j hj => Submodule.smul_mem _ _ (Submodule.subset_span ⟨j,rfl⟩))
    obtain ⟨e,he⟩ := (Submodule.mem_span_range_iff_exists_fun ℝ).mp huSpan
    have he0 (i : Fin n) : e i=0 := by
      have hr : finitePairing (a i) u=0 := by
        dsimp [u]
        rw [finiteFrame_pair_sum]
        have hi := congrFun hcd i
        simp only [finiteFrame_response_apply] at hi
        simpa only [t,Pi.sub_apply,sub_mul,Finset.sum_sub_distrib,sub_eq_zero] using hi
      rw [← he,finiteFrame_pair_sum] at hr
      simpa only [hright,mul_ite,mul_one,mul_zero,Finset.sum_ite_eq,Finset.mem_univ,
        if_true] using hr
    have hu0 : u=0 := by
      rw [← he]
      simp only [he0,zero_smul,Finset.sum_const_zero]
    have ht0 := Fintype.linearIndependent_iff.mp hFli t hu0
    funext i
    exact sub_eq_zero.mp (ht0 i)
  exact ⟨hinj,LinearMap.surjective_of_injective
    (f := (rowResponse a F).toLinearMap) hinj⟩

/- Identity is consumed BEFORE normalization; afterwards only bijectivity of
   the actual response is concluded. -/
private theorem finiteFrame_of_rightInverse {L r : ℝ} {n : ℕ}
    (a : Fin n → SourceMode 2 → ℝ) (v : Fin n → SourceMode 2 →₀ ℝ)
    (hraw : ∀ (i : Fin 6) (j : Fin n), finitePairing (rawPinCoefficient L r i) (v j)=0)
    (hright : ∀ i j, finitePairing (a i) (v j)=if i=j then 1 else 0) :
    ∃ F : RawPinFreeFrame L r n,
      Submodule.span ℝ (Set.range F.chi)=Submodule.span ℝ (Set.range v) ∧
      Function.Bijective (rowResponse a F) := by
  have hv := finiteFrame_independent_of_rightInverse a v hright
  obtain ⟨F,hspan⟩ := finiteFrame_of_linearIndependent v hv hraw
  exact ⟨F,hspan,finiteFrame_response_bijective_of_same_span a v hright F hspan⟩

private theorem gradient_frame {L : ℝ} (hL : L ≠ 0) (r : ℝ)
    (x : Point2) (hx : Remote L r x) :
    ∃ F : RawPinFreeFrame L r 2, Function.Bijective (rowResponse (gradientRows L x) F) := by
  classical
  obtain ⟨v,hraw,hright⟩ := actual_finite_remoteJet_witnesses hL r x hx.1 hx.2
  let sel : Fin 2 → Fin 6 := ![1,2]
  have hsel : Function.Injective sel := by
    intro i j h
    fin_cases i <;> fin_cases j <;> simp_all [sel]
  have hrows (i : Fin 2) : gradientRows L x i=remoteJetCoefficient L x (sel i) := by
    fin_cases i <;> rfl
  have hright2 (i j : Fin 2) :
      finitePairing (gradientRows L x i) (v (sel j))=if i=j then 1 else 0 := by
    rw [hrows]
    simpa only [hsel.eq_iff] using hright (sel i) (sel j)
  obtain ⟨F,hspan,hF⟩ := finiteFrame_of_rightInverse (gradientRows L x) (fun j => v (sel j))
    (fun i j => hraw i (sel j)) hright2
  exact ⟨F,hF⟩

private theorem level_frame {L : ℝ} (hL : L ≠ 0) (r : ℝ)
    (x : Point2) (hx : Remote L r x) :
    ∃ F : RawPinFreeFrame L r 3, Function.Bijective (rowResponse (levelRows L x) F) := by
  classical
  obtain ⟨v,hraw,hright⟩ := actual_finite_remoteJet_witnesses hL r x hx.1 hx.2
  let sel : Fin 3 → Fin 6 := ![0,1,2]
  have hsel : Function.Injective sel := by
    intro i j h
    fin_cases i <;> fin_cases j <;> simp_all [sel]
  have hrows (i : Fin 3) : levelRows L x i=remoteJetCoefficient L x (sel i) := by
    fin_cases i <;> rfl
  have hright3 (i j : Fin 3) :
      finitePairing (levelRows L x i) (v (sel j))=if i=j then 1 else 0 := by
    rw [hrows]
    simpa only [hsel.eq_iff] using hright (sel i) (sel j)
  obtain ⟨F,hspan,hF⟩ := finiteFrame_of_rightInverse (levelRows L x) (fun j => v (sel j))
    (fun i j => hraw i (sel j)) hright3
  exact ⟨F,hF⟩

private theorem tie_frame {L : ℝ} (hL : L ≠ 0) (r : ℝ)
    (p : Point4) (hp : RemotePair L r p) :
    ∃ F : RawPinFreeFrame L r 5, Function.Bijective (rowResponse (tieRows L p) F) := by
  classical
  obtain ⟨v,hraw,hright⟩ := actual_finite_twoRemoteFirstJet_witnesses hL r p.1 p.2
    hp.1.1 hp.1.2 hp.2.1.1 hp.2.1.2 hp.2.2
  let sel : Fin 5 → Fin 6 := ![1,2,4,5,0]
  have hsel : Function.Injective sel := by
    intro i j h
    fin_cases i <;> fin_cases j <;> simp_all [sel]
  have hrows (i : Fin 5) : tieRows L p i=
      if i=(4 : Fin 5) then
        (fun m => twoRemoteFirstJetCoefficient L p.1 p.2 0 m-
          twoRemoteFirstJetCoefficient L p.1 p.2 3 m)
      else twoRemoteFirstJetCoefficient L p.1 p.2 (sel i) := by
    fin_cases i <;> rfl
  have hright5 (i j : Fin 5) :
      finitePairing (tieRows L p i) (v (sel j))=if i=j then 1 else 0 := by
    rw [hrows]
    by_cases hi : i=(4 : Fin 5)
    · subst i
      rw [if_pos rfl,finiteFrame_pair_sub_left,hright,hright]
      fin_cases j <;> norm_num [sel]
    · rw [if_neg hi,hright]
      simp only [hsel.eq_iff]
  obtain ⟨F,hspan,hF⟩ := finiteFrame_of_rightInverse (tieRows L p) (fun j => v (sel j))
    (fun i j => hraw i (sel j)) hright5
  exact ⟨F,hF⟩

end I4SourceGapConditionalMorseDistinct
