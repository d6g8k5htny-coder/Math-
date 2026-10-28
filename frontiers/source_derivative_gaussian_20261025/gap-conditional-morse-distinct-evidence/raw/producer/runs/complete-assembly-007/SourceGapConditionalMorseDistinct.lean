import Mathlib.Analysis.Matrix.Spectrum
import Mathlib.Analysis.Calculus.ContDiff.FTaylorSeries
import Mathlib.Analysis.Calculus.FDeriv.Symmetric
import Mathlib.LinearAlgebra.FiniteDimensional.Lemmas
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Abel
import Mathlib.Analysis.Calculus.ContDiff.FiniteDimension
import Mathlib.Analysis.Normed.Ring.Units
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
open WithLp Set MeasureTheory ProbabilityTheory I4Foundation I4Source I4Smooth I4SmoothCarrier
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
  change DifferentiableAt ℝ (fun y => -((B y).inverse (g y))) x
  exact (hId.clm_apply hgd).neg

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
  change fderiv ℝ (g+(fun y => B y z)) x = _
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
    (μ : Measure V) [MeasureTheory.Measure.IsAddHaarMeasure μ] (theta : V → V) (S : Set V)
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
      rw [(hG.symm e).map_eq] at h
      change (Measure.pi (fun _ : Fin (n+1) => gaussianReal 0 1)) ≪
        (volume : Measure (ℝ × (Fin n → ℝ))).map e.symm at h
      rwa [(hV.symm e).map_eq] at h

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
    (μ : Measure V) [MeasureTheory.Measure.IsAddHaarMeasure μ]
    (P : V →L[ℝ] D) (J : D → V) (hPJ : ∀ x, P (J x)=x)
    (w : V) (hw : w≠0) (hPw : P w=0)
    (theta : D → V) (U : Set D)
    (htheta : ∀ x∈U, DifferentiableAt ℝ theta x) :
    μ (theta '' U)=0 := by
  have hnull : μ ((fun y => theta (P y)) '' (P ⁻¹' U))=0 := by
    apply addHaar_image_eq_zero_of_det_fderivWithin_eq_zero μ
      (f' := fderiv ℝ (fun y => theta (P y)))
    · intro x hx
      have hd := (htheta (P x) hx).comp x P.differentiableAt
      simpa only [Function.comp_def] using hd.hasFDerivAt.hasFDerivWithinAt
        (s := P ⁻¹' U)
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
    ite_true] using hi

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
  simp [Finsupp.finsetSum_apply,Finsupp.single_apply ]

private theorem finiteFrame_extend_off (S : Finset (SourceMode 2))
    (u : EuclideanSpace ℝ S) (m : SourceMode 2) (hm : m ∉ S) :
    finiteFrame_extend S u m=0 := by
  classical
  change (∑ k : S, u k • Finsupp.single k.val 1) m=0
  rw [Finsupp.finsetSum_apply]
  apply Finset.sum_eq_zero
  intro k hk
  have hkm : k.val ≠ m := by intro h; exact hm (h ▸ k.property)
  simp [hkm]

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
    simp only [Submodule.map_span,← Set.range_comp,Function.comp_def] at hh
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
      ite_true] using hz
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
        ite_true] using hr
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
      rw [ite_eq_left rfl,finiteFrame_pair_sub_left,hright,hright]
      fin_cases j <;> norm_num [sel]
    · rw [ite_eq_right hi,hright]
      simp only [hsel.eq_iff]
  obtain ⟨F,hspan,hF⟩ := finiteFrame_of_rightInverse (tieRows L p) (fun j => v (sel j))
    (fun i j => hraw i (sel j)) hright5
  exact ⟨F,hF⟩

/- Complete TEXT ONLY for one integration inside
namespace I4SourceGapConditionalMorseDistinct.
All declarations are private. No helper execution or qualification is claimed. -/

private theorem geometry59_spectral_quadratic
    (A : Matrix (Fin 2) (Fin 2) ℝ) (hA : A.IsHermitian) (v : E 2) :
    dotProduct (coordinates 2 v) (A *ᵥ coordinates 2 v) =
      ∑ i : Fin 2, hA.eigenvalues i * (hA.eigenvectorBasis.repr v i)^2 := by
  classical
  let b : OrthonormalBasis (Fin 2) ℝ (E 2) := hA.eigenvectorBasis
  let T : (E 2) →ₗ[ℝ] (E 2) := A.toEuclideanLin
  have hT : T.IsSymmetric := Matrix.isSymmetric_toEuclideanLin_iff.mpr hA
  have hTb (i : Fin 2) : T (b i) = hA.eigenvalues i • b i := by
    change toLp 2 (A *ᵥ (b i : Fin 2 → ℝ)) = hA.eigenvalues i • b i
    rw [show A *ᵥ (b i : Fin 2 → ℝ) =
      hA.eigenvalues i • (b i : Fin 2 → ℝ) from hA.mulVec_eigenvectorBasis i]
    rfl
  have hrepr (i : Fin 2) :
      b.repr (T v) i = hA.eigenvalues i * b.repr v i := by
    calc
      b.repr (T v) i = inner ℝ (b i) (T v) := b.repr_apply_apply _ _
      _ = inner ℝ (T (b i)) v := (hT (b i) v).symm
      _ = hA.eigenvalues i * b.repr v i := by
        rw [hTb]
        simp only [real_inner_smul_left, b.repr_apply_apply]
  have hinner : inner ℝ v (T v) =
      ∑ i : Fin 2, hA.eigenvalues i * (b.repr v i)^2 := by
    rw [← b.sum_inner_mul_inner v (T v)]
    apply Finset.sum_congr rfl
    intro i _hi
    have he1 : inner ℝ v (b i) = b.repr v i := by
      exact (real_inner_comm _ _).trans (b.repr_apply_apply v i).symm
    have he2 : inner ℝ (b i) (T v) = b.repr (T v) i :=
      (b.repr_apply_apply (T v) i).symm
    rw [he1,he2,hrepr]
    ring
  calc
    dotProduct (coordinates 2 v) (A *ᵥ coordinates 2 v) = inner ℝ v (T v) := by
      change dotProduct (coordinates 2 v) (A *ᵥ coordinates 2 v) =
        dotProduct (A *ᵥ coordinates 2 v) (coordinates 2 v)
      exact dotProduct_comm _ _
    _ = _ := hinner

/-- A spectral sign decomposition, with genuine submodules and no pivot premise. -/
private theorem inertia_of_symmetric_matrix
    (g : E 2 → ℝ) (X : E 2) (A : Matrix (Fin 2) (Fin 2) ℝ)
    (hA : A.IsHermitian)
    (hform : ∀ v : E 2, hessian 2 g X v v =
      dotProduct (coordinates 2 v) (A *ᵥ coordinates 2 v))
    (hdet : A.det ≠ 0) : ∃ j : ℕ, HessianHasInertia 2 g X j := by
  classical
  let b : OrthonormalBasis (Fin 2) ℝ (E 2) := hA.eigenvectorBasis
  let eigen : Fin 2 → ℝ := hA.eigenvalues
  have heigen : ∀ i : Fin 2, eigen i ≠ 0 := by
    have hp : (∏ i : Fin 2, eigen i) ≠ 0 := by
      have hdprod : A.det = ∏ i : Fin 2, eigen i := by
        simpa [eigen] using hA.det_eq_prod_eigenvalues
      rw [← hdprod]
      exact hdet
    intro i
    exact (Finset.prod_ne_zero_iff.mp hp) i (Finset.mem_univ i)
  have hq (v : E 2) :
      hessian 2 g X v v = ∑ i : Fin 2, eigen i * (b.repr v i)^2 := by
    exact (hform v).trans (geometry59_spectral_quadratic A hA v)
  let V : Submodule ℝ (E 2) :=
    { carrier := {v | ∀ i : Fin 2, ¬ eigen i < 0 → b.repr v i = 0}
      zero_mem' := by intro i _hi; simp
      add_mem' := by
        intro v w hv hw i hi
        simp only [map_add, PiLp.add_apply, hv i hi, hw i hi, add_zero]
      smul_mem' := by
        intro c v hv i hi
        simp only [map_smul, PiLp.smul_apply, hv i hi, smul_zero] }
  let W : Submodule ℝ (E 2) :=
    { carrier := {v | ∀ i : Fin 2, eigen i < 0 → b.repr v i = 0}
      zero_mem' := by intro i _hi; simp
      add_mem' := by
        intro v w hv hw i hi
        simp only [map_add, PiLp.add_apply, hv i hi, hw i hi, add_zero]
      smul_mem' := by
        intro c v hv i hi
        simp only [map_smul, PiLp.smul_apply, hv i hi, smul_zero] }
  have hdis : Disjoint V W := by
    apply Submodule.disjoint_def.mpr
    intro v hv hw
    apply b.repr.injective
    ext i
    by_cases hi : eigen i < 0
    · simpa only [map_zero, PiLp.zero_apply] using hw i hi
    · simpa only [map_zero, PiLp.zero_apply] using hv i hi
  have hsup : V ⊔ W = ⊤ := by
    apply le_antisymm le_top
    intro v _hv
    let vn : E 2 := b.repr.symm (toLp 2 (fun i =>
      if eigen i < 0 then b.repr v i else 0))
    let vp : E 2 := b.repr.symm (toLp 2 (fun i =>
      if eigen i < 0 then 0 else b.repr v i))
    have hvn : vn ∈ V := by
      intro i hi
      simp only [vn, LinearIsometryEquiv.apply_symm_apply, PiLp.toLp_apply,
        ite_eq_right hi]
    have hvp : vp ∈ W := by
      intro i hi
      simp only [vp, LinearIsometryEquiv.apply_symm_apply, PiLp.toLp_apply,
        ite_eq_left hi]
    have hvsum : vn + vp = v := by
      apply b.repr.injective
      ext i
      by_cases hi : eigen i < 0
      · simp only [map_add, PiLp.add_apply, vn, vp,
          LinearIsometryEquiv.apply_symm_apply,
          ite_eq_left hi, add_zero]
      · simp only [map_add, PiLp.add_apply, vn, vp,
          LinearIsometryEquiv.apply_symm_apply,
          ite_eq_right hi, zero_add]
    exact Submodule.mem_sup.mpr ⟨vn, hvn, vp, hvp, hvsum⟩
  have hcompl : IsCompl V W := ⟨hdis, codisjoint_iff.mpr hsup⟩
  have hdim : Module.finrank ℝ V + Module.finrank ℝ W = 2 := by
    simpa only [finrank_euclideanSpace_fin] using
      (Submodule.finrank_add_eq_of_isCompl hcompl)
  have hnonzero_coordinate (v : E 2) (hv : v ≠ 0) :
      ∃ i : Fin 2, b.repr v i ≠ 0 := by
    by_contra h
    have hz (i : Fin 2) : b.repr v i = 0 := by
      by_contra hi
      exact h ⟨i, hi⟩
    apply hv
    apply b.repr.injective
    ext i
    simpa only [map_zero, PiLp.zero_apply] using hz i
  refine ⟨Module.finrank ℝ V, V, W, hcompl, rfl, ?_, ?_, ?_⟩
  · omega
  · intro v hv hv0
    rw [hq]
    apply Finset.sum_neg'
    · intro i _hi
      by_cases hn : eigen i < 0
      · exact mul_nonpos_of_nonpos_of_nonneg hn.le (sq_nonneg _)
      · rw [hv i hn]
        simp only [zero_pow (by decide : 2 ≠ 0), mul_zero, le_refl]
    · obtain ⟨i, hi⟩ := hnonzero_coordinate v hv0
      have hn : eigen i < 0 := by
        by_contra hni
        exact hi (hv i hni)
      exact ⟨i, Finset.mem_univ i, mul_neg_of_neg_of_pos hn (sq_pos_of_ne_zero hi)⟩
  · intro v hv hv0
    rw [hq]
    apply Finset.sum_pos'
    · intro i _hi
      by_cases hn : eigen i < 0
      · rw [hv i hn]
        simp only [zero_pow (by decide : 2 ≠ 0), mul_zero, le_refl]
      · exact mul_nonneg (le_of_not_gt hn) (sq_nonneg _)
    · obtain ⟨i, hi⟩ := hnonzero_coordinate v hv0
      have hn : ¬ eigen i < 0 := by
        intro hni
        exact hi (hv i hni)
      have hp : 0 < eigen i := lt_of_le_of_ne (le_of_not_gt hn) (heigen i).symm
      exact ⟨i, Finset.mem_univ i, mul_pos hp (sq_pos_of_ne_zero hi)⟩

private theorem actual_inertia_of_source_det {L : ℝ} (hL : 0 < L)
    (ω : SmoothSample 2 L) (X : E 2)
    (hdet :
      (iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω) (coordinates 2 X)
        ![directionX, directionX]) *
      (iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω) (coordinates 2 X)
        ![directionY, directionY]) -
      (iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω) (coordinates 2 X)
        ![directionX, directionY])^2 ≠ 0) :
    ∃ j : ℕ, HessianHasInertia 2 (actualField 2 L ω) X j := by
  let D := fderiv ℝ (fderiv ℝ (smoothSourceField 2 L ω)) (coordinates 2 X)
  let a : ℝ := D directionX directionX
  let b : ℝ := D directionX directionY
  let c : ℝ := D directionY directionY
  let A : Matrix (Fin 2) (Fin 2) ℝ := ![![a,b], ![b,c]]
  have hsym : D directionY directionX = b :=
    ((smoothSourceField_smooth 2 hL.ne' ω).contDiffAt.isSymmSndFDerivAt
      (by simp)) directionY directionX
  have hA : A.IsHermitian := by
    change Aᴴ = A
    ext i j
    change A j i = A i j
    fin_cases i <;> fin_cases j <;> rfl
  have hdetA : A.det ≠ 0 := by
    have hd : a*c-b^2 ≠ 0 := by
      simpa only [a, b, c, D, iteratedFDeriv_two_apply,
        Matrix.cons_val_zero, Matrix.cons_val_one] using hdet
    rw [Matrix.det_fin_two]
    change a*c-b*b≠0
    simpa only [pow_two] using hd
  have hquad (u : Point2) : D u u = a*u 0^2+2*b*u 0*u 1+c*u 1^2 := by
    have hu : u = u 0 • directionX + u 1 • directionY := by
      ext i
      fin_cases i <;> simp [directionX, directionY]
    calc
      D u u = D (u 0 • directionX + u 1 • directionY)
          (u 0 • directionX + u 1 • directionY) := congrArg₂ (fun v w => D v w) hu hu
      _ = _ := by
        simp only [map_add, map_smul, _root_.add_apply,
          _root_.smul_apply, smul_eq_mul]
        change u 0*(u 0*a+u 1*(D directionY directionX))+u 1*(u 0*b+u 1*c) = _
        rw [hsym]
        ring
  apply inertia_of_symmetric_matrix (actualField 2 L ω) X A hA _ hdetA
  intro v
  calc
    hessian 2 (actualField 2 L ω) X v v = D (coordinates 2 v) (coordinates 2 v) := by
      rw [actual_hessian_coordinates hL, iteratedFDeriv_two_apply]
      rfl
    _ = a*(coordinates 2 v 0)^2+2*b*(coordinates 2 v 0)*(coordinates 2 v 1)+
        c*(coordinates 2 v 1)^2 := hquad _
    _ = dotProduct (coordinates 2 v) (A *ᵥ coordinates 2 v) := by
      simp only [A, Matrix.mulVec, dotProduct, Fin.sum_univ_two,
        Matrix.cons_val_zero, Matrix.cons_val_one]
      ring

/- Honest finite-form positives. The premise is the displayed quadratic identity,
not a Gaussian realization or supplied inertia certificate. Each directly calls
the new generic spectral adapter, including the zero-diagonal saddle. -/
private theorem inertia_control_positive (g : E 2 → ℝ) (X : E 2)
    (hq : ∀ v : E 2, hessian 2 g X v v =
      (coordinates 2 v 0)^2 + (coordinates 2 v 1)^2) :
    ∃ j : ℕ, HessianHasInertia 2 g X j := by
  let A : Matrix (Fin 2) (Fin 2) ℝ := ![![1,0], ![0,1]]
  apply inertia_of_symmetric_matrix g X A
  · change Aᴴ = A
    ext i j
    change A j i = A i j
    fin_cases i <;> fin_cases j <;> rfl
  · intro v
    rw [hq]
    simp only [A, Matrix.mulVec, dotProduct, Fin.sum_univ_two,
      Matrix.cons_val_zero, Matrix.cons_val_one]
    ring
  · rw [Matrix.det_fin_two]
    norm_num [A]

private theorem inertia_control_negative (g : E 2 → ℝ) (X : E 2)
    (hq : ∀ v : E 2, hessian 2 g X v v =
      -(coordinates 2 v 0)^2 - (coordinates 2 v 1)^2) :
    ∃ j : ℕ, HessianHasInertia 2 g X j := by
  let A : Matrix (Fin 2) (Fin 2) ℝ := ![![-1,0], ![0,-1]]
  apply inertia_of_symmetric_matrix g X A
  · change Aᴴ = A
    ext i j
    change A j i = A i j
    fin_cases i <;> fin_cases j <;> rfl
  · intro v
    rw [hq]
    simp only [A, Matrix.mulVec, dotProduct, Fin.sum_univ_two,
      Matrix.cons_val_zero, Matrix.cons_val_one]
    ring
  · rw [Matrix.det_fin_two]
    norm_num [A]

private theorem inertia_control_axis_saddle (g : E 2 → ℝ) (X : E 2)
    (hq : ∀ v : E 2, hessian 2 g X v v =
      (coordinates 2 v 0)^2 - (coordinates 2 v 1)^2) :
    ∃ j : ℕ, HessianHasInertia 2 g X j := by
  let A : Matrix (Fin 2) (Fin 2) ℝ := ![![1,0], ![0,-1]]
  apply inertia_of_symmetric_matrix g X A
  · change Aᴴ = A
    ext i j
    change A j i = A i j
    fin_cases i <;> fin_cases j <;> rfl
  · intro v
    rw [hq]
    simp only [A, Matrix.mulVec, dotProduct, Fin.sum_univ_two,
      Matrix.cons_val_zero, Matrix.cons_val_one]
    ring
  · rw [Matrix.det_fin_two]
    norm_num [A]

private theorem inertia_control_zero_diagonal_saddle (g : E 2 → ℝ) (X : E 2)
    (hq : ∀ v : E 2, hessian 2 g X v v =
      2*(coordinates 2 v 0)*(coordinates 2 v 1)) :
    ∃ j : ℕ, HessianHasInertia 2 g X j := by
  let A : Matrix (Fin 2) (Fin 2) ℝ := ![![0,1], ![1,0]]
  apply inertia_of_symmetric_matrix g X A
  · change Aᴴ = A
    ext i j
    change A j i = A i j
    fin_cases i <;> fin_cases j <;> rfl
  · intro v
    rw [hq]
    simp only [A, Matrix.mulVec, dotProduct, Fin.sum_univ_two,
      Matrix.cons_val_zero, Matrix.cons_val_one]
    ring
  · rw [Matrix.det_fin_two]
    norm_num [A]

private theorem geometry59_projection_eq_lattice {L : ℝ} (x y : Point2)
    (h : I4Torus.torusProjection 2 L x = I4Torus.torusProjection 2 L y) :
    ∃ n : Fin 2 → ℤ, y = fun i => x i + L*(n i : ℝ) := by
  classical
  have hz (i : Fin 2) : ∃ n : ℤ, n • L = y i - x i := by
    apply (AddCircle.coe_eq_zero_iff (p := L)).mp
    rw [AddCircle.coe_sub]
    exact sub_eq_zero.mpr (congrFun h i).symm
  choose n hn using hz
  refine ⟨n, ?_⟩
  ext i
  have hi := hn i
  rw [zsmul_eq_mul] at hi
  linarith

private theorem projection_eq_torusDist_zero {L : ℝ} (_hL : 0 < L) (X Y : E 2)
    (h : I4Torus.torusProjection 2 L (coordinates 2 X) =
      I4Torus.torusProjection 2 L (coordinates 2 Y)) : torusDist 2 L X Y = 0 := by
  obtain ⟨n, hn⟩ := geometry59_projection_eq_lattice (coordinates 2 X) (coordinates 2 Y) h
  have hY : Y = X + latticeVec 2 L n := by
    apply (coordinates 2).injective
    rw [map_add, coordinates_latticeVec]
    exact hn
  have hzero : X-Y+latticeVec 2 L n = 0 := by rw [hY]; abel
  change (⨅ m : Fin 2 → ℤ, ‖X-Y+latticeVec 2 L m‖) = 0
  apply le_antisymm
  · have hbounded : BddBelow (Set.range (fun m : Fin 2 → ℤ => ‖X-Y+latticeVec 2 L m‖)) :=
      ⟨0, by rintro z ⟨m, rfl⟩; exact norm_nonneg _⟩
    have hle := ciInf_le hbounded n
    simpa only [hzero, norm_zero] using hle
  · exact le_ciInf (fun m => norm_nonneg (X-Y+latticeVec 2 L m))

private theorem source_jets_of_projection_eq {L : ℝ} (hL : 0 < L)
    (ω : SmoothSample 2 L) (x y : Point2)
    (h : I4Torus.torusProjection 2 L x = I4Torus.torusProjection 2 L y) :
    smoothSourceField 2 L ω x = smoothSourceField 2 L ω y ∧
      (∀ k : ℕ, iteratedFDeriv ℝ k (smoothSourceField 2 L ω) x =
        iteratedFDeriv ℝ k (smoothSourceField 2 L ω) y) := by
  obtain ⟨n, hn⟩ := geometry59_projection_eq_lattice x y h
  let s : Point2 := fun i => L*(n i : ℝ)
  have hy : y = x+s := hn
  have hp (z : Point2) : smoothSourceField 2 L ω (z+s) = smoothSourceField 2 L ω z := by
    exact I4Lattice.sourceField_lattice_shift 2 hL.ne' (sampleInclusion 2 L ω) n z
  have hfun : (fun z : Point2 => smoothSourceField 2 L ω (z+s)) =
      smoothSourceField 2 L ω := funext hp
  refine ⟨?_, ?_⟩
  · rw [hy]
    exact (hp x).symm
  · intro k
    rw [hy]
    calc
      iteratedFDeriv ℝ k (smoothSourceField 2 L ω) x =
          iteratedFDeriv ℝ k (fun z : Point2 => smoothSourceField 2 L ω (z+s)) x :=
        (congrArg (fun F : Point2 → ℝ => iteratedFDeriv ℝ k F x) hfun).symm
      _ = iteratedFDeriv ℝ k (smoothSourceField 2 L ω) (x+s) :=
        iteratedFDeriv_comp_add_right k s x

private theorem source_directionX_eq : directionX = Pi.single (0 : Fin 2) (1 : ℝ) := by
  ext i
  fin_cases i <;> simp [directionX]

private theorem source_directionY_eq : directionY = Pi.single (1 : Fin 2) (1 : ℝ) := by
  ext i
  fin_cases i <;> simp [directionY]

private theorem mode_smooth (L : ℝ) (m : SourceMode 2) :
    ContDiff ℝ (⊤ : ℕ∞) (modeCoefficient 2 L m) := by
  cases m with
  | none => exact contDiff_const
  | some p =>
    rcases p with ⟨k,b⟩
    have hp : ContDiff ℝ (⊤ : ℕ∞) (phase 2 L k) := by
      have he : phase 2 L k = (I4C4.phaseCLM 2 L k : Point2 → ℝ) := by
        funext x
        exact (I4C4.phaseCLM_apply 2 L k x).symm
      rw [he]
      exact (I4C4.phaseCLM 2 L k).contDiff
    cases b
    · change ContDiff ℝ (⊤ : ℕ∞) (fun x : Point2 =>
        Real.sqrt (2*I4Weights.sourceWeight 2 L k/I4Weights.sourceZ 2 L) *
          Real.cos (phase 2 L k x))
      exact contDiff_const.mul hp.cos
    · change ContDiff ℝ (⊤ : ℕ∞) (fun x : Point2 =>
        Real.sqrt (2*I4Weights.sourceWeight 2 L k/I4Weights.sourceZ 2 L) *
          Real.sin (phase 2 L k x))
      exact contDiff_const.mul hp.sin

private theorem gradientRows_eq (L : ℝ) (x : Point2) (i : Fin 2) (m : SourceMode 2) :
    gradientRows L x i m = coordinateGradient (modeCoefficient 2 L m) x i := by
  fin_cases i <;>
    simp [gradientRows,remoteJetCoefficient,derivativeCoefficient,coordinateGradient,
      iteratedFDeriv_one_apply,source_directionX_eq,source_directionY_eq]

private theorem levelRows_eq (L : ℝ) (x : Point2) (i : Fin 3) (m : SourceMode 2) :
    levelRows L x i m = ![modeCoefficient 2 L m x,
      coordinateGradient (modeCoefficient 2 L m) x 0,
      coordinateGradient (modeCoefficient 2 L m) x 1] i := by
  fin_cases i <;>
    simp [levelRows,remoteJetCoefficient,derivativeCoefficient,coordinateGradient,
      iteratedFDeriv_one_apply,source_directionX_eq,source_directionY_eq]

private theorem tieRows_eq (L : ℝ) (p : Point4) (i : Fin 5) (m : SourceMode 2) :
    tieRows L p i m = ![coordinateGradient (modeCoefficient 2 L m) p.1 0,
      coordinateGradient (modeCoefficient 2 L m) p.1 1,
      coordinateGradient (modeCoefficient 2 L m) p.2 0,
      coordinateGradient (modeCoefficient 2 L m) p.2 1,
      modeCoefficient 2 L m p.1-modeCoefficient 2 L m p.2] i := by
  fin_cases i <;>
    simp [tieRows,twoRemoteFirstJetCoefficient,remoteJetCoefficient,derivativeCoefficient,
      coordinateGradient,iteratedFDeriv_one_apply,source_directionX_eq,source_directionY_eq]

private theorem rowResponse_smooth
    {X : Type*} [NormedAddCommGroup X] [NormedSpace ℝ X]
    {L r : ℝ} {n : ℕ} (a : X → Fin n → SourceMode 2 → ℝ)
    (F : RawPinFreeFrame L r n)
    (ha : ∀ i j, ContDiff ℝ (⊤ : ℕ∞) (fun x => finitePairing (a x i) (F.chi j))) :
    ContDiff ℝ (⊤ : ℕ∞) (fun x => rowResponse (a x) F) := by
  apply contDiff_clm_apply_iff.mpr
  intro z
  apply contDiff_pi.mpr
  intro i
  simp_rw [rowResponse_apply]
  exact ContDiff.sum (fun j _ => (ha i j).mul contDiff_const)

private theorem gradient_response_smooth {L r : ℝ} (F : RawPinFreeFrame L r 2) :
    ContDiff ℝ (⊤ : ℕ∞) (fun x => rowResponse (gradientRows L x) F) := by
  classical
  apply rowResponse_smooth
  intro i j
  simp_rw [finitePairing,Finsupp.sum,gradientRows_eq]
  exact ContDiff.sum (fun m _ =>
    ((contDiff_pi.mp (coordinateGradient_contDiff _ (mode_smooth L m))) i).mul contDiff_const)

private theorem level_response_smooth {L r : ℝ} (F : RawPinFreeFrame L r 3) :
    ContDiff ℝ (⊤ : ℕ∞) (fun x => rowResponse (levelRows L x) F) := by
  classical
  apply rowResponse_smooth
  intro i j
  simp_rw [finitePairing,Finsupp.sum,levelRows_eq]
  apply ContDiff.sum
  intro m _
  fin_cases i
  · exact (mode_smooth L m).mul contDiff_const
  · exact ((contDiff_pi.mp (coordinateGradient_contDiff _ (mode_smooth L m))) 0).mul contDiff_const
  · exact ((contDiff_pi.mp (coordinateGradient_contDiff _ (mode_smooth L m))) 1).mul contDiff_const

private theorem tie_response_smooth {L r : ℝ} (F : RawPinFreeFrame L r 5) :
    ContDiff ℝ (⊤ : ℕ∞) (fun x => rowResponse (tieRows L x) F) := by
  classical
  apply rowResponse_smooth
  intro i j
  simp_rw [finitePairing,Finsupp.sum,tieRows_eq]
  apply ContDiff.sum
  intro m _
  have hg := coordinateGradient_contDiff _ (mode_smooth L m)
  fin_cases i
  · exact (((contDiff_pi.mp hg) 0).comp contDiff_fst).mul contDiff_const
  · exact (((contDiff_pi.mp hg) 1).comp contDiff_fst).mul contDiff_const
  · exact (((contDiff_pi.mp hg) 0).comp contDiff_snd).mul contDiff_const
  · exact (((contDiff_pi.mp hg) 1).comp contDiff_snd).mul contDiff_const
  · exact (((mode_smooth L m).comp contDiff_fst).sub
      ((mode_smooth L m).comp contDiff_snd)).mul contDiff_const

private theorem response_neighborhood
    {X : Type*} [TopologicalSpace X] {n : ℕ}
    (B : X → (Fin n → ℝ) →L[ℝ] (Fin n → ℝ)) (hB : Continuous B)
    (x : X) (hx : Function.Bijective (B x)) :
    ∃ U : Set X, IsOpen U ∧ x∈U ∧ ∀ y∈U, Function.Bijective (B y) := by
  refine ⟨{y | IsUnit (B y)},Units.isOpen.preimage hB,?_,?_⟩
  · exact ContinuousLinearMap.isUnit_iff_bijective.mpr hx
  · intro y hy
    exact ContinuousLinearMap.isUnit_iff_bijective.mp hy

private def levelConstraint {L : ℝ} (α : ℝ) (ω : SmoothSample 2 L)
    (x : Point2) : Fin 3 → ℝ :=
  ![smoothSourceField 2 L ω x-α,coordinateGradient (smoothSourceField 2 L ω) x 0,
    coordinateGradient (smoothSourceField 2 L ω) x 1]

private def tieConstraint {L : ℝ} (ω : SmoothSample 2 L) (p : Point4) : Fin 5 → ℝ :=
  ![coordinateGradient (smoothSourceField 2 L ω) p.1 0,
    coordinateGradient (smoothSourceField 2 L ω) p.1 1,
    coordinateGradient (smoothSourceField 2 L ω) p.2 0,
    coordinateGradient (smoothSourceField 2 L ω) p.2 1,
    smoothSourceField 2 L ω p.1-smoothSourceField 2 L ω p.2]

private theorem level_constraint_smooth {L : ℝ} (hL : L≠0) (α : ℝ)
    (ω : SmoothSample 2 L) : ContDiff ℝ (⊤ : ℕ∞) (levelConstraint α ω) := by
  have hf := smoothSourceField_smooth 2 hL ω
  have hg := coordinateGradient_contDiff _ hf
  apply contDiff_pi.mpr
  intro i
  fin_cases i
  · exact hf.sub contDiff_const
  · exact (contDiff_pi.mp hg) 0
  · exact (contDiff_pi.mp hg) 1

private theorem tie_constraint_smooth {L : ℝ} (hL : L≠0) (ω : SmoothSample 2 L) :
    ContDiff ℝ (⊤ : ℕ∞) (tieConstraint ω) := by
  have hf := smoothSourceField_smooth 2 hL ω
  have hg := coordinateGradient_contDiff _ hf
  apply contDiff_pi.mpr
  intro i
  fin_cases i
  · exact ((contDiff_pi.mp hg) 0).comp contDiff_fst
  · exact ((contDiff_pi.mp hg) 1).comp contDiff_fst
  · exact ((contDiff_pi.mp hg) 0).comp contDiff_snd
  · exact ((contDiff_pi.mp hg) 1).comp contDiff_snd
  · exact (hf.comp contDiff_fst).sub (hf.comp contDiff_snd)

private theorem freeShift_value {L r : ℝ} {n : ℕ} (hL : L≠0)
    (F : RawPinFreeFrame L r n) (z : Fin n → ℝ) (ω : SmoothSample 2 L) (x : Point2) :
    smoothSourceField 2 L (freeShiftSample F z ω) x = smoothSourceField 2 L ω x+
      ∑ j,z j*finitePairing (fun m => modeCoefficient 2 L m x) (F.chi j) := by
  have he : derivativeCoefficient 2 L 0 x (fun i => Fin.elim0 i) =
      fun m => modeCoefficient 2 L m x := by funext m; rfl
  simpa only [iteratedFDeriv_zero_apply,he] using
    freeShift_derivative hL F z ω 0 x (fun i => Fin.elim0 i)

private theorem freeShift_gradient_component {L r : ℝ} {n : ℕ} (hL : L≠0)
    (F : RawPinFreeFrame L r n) (z : Fin n → ℝ) (ω : SmoothSample 2 L)
    (x : Point2) (i : Fin 2) :
    coordinateGradient (smoothSourceField 2 L (freeShiftSample F z ω)) x i =
      coordinateGradient (smoothSourceField 2 L ω) x i+
        ∑ j,z j*finitePairing (fun m => coordinateGradient (modeCoefficient 2 L m) x i)
          (F.chi j) := by
  have he : derivativeCoefficient 2 L 1 x (fun _ => Pi.single i 1) =
      fun m => coordinateGradient (modeCoefficient 2 L m) x i := by
    funext m
    simp [derivativeCoefficient,coordinateGradient,iteratedFDeriv_one_apply]
  simpa only [iteratedFDeriv_one_apply,he,coordinateGradient] using
    freeShift_derivative hL F z ω 1 x (fun _ => Pi.single i 1)

private theorem freeShift_gradient {L r : ℝ} (hL : L≠0)
    (F : RawPinFreeFrame L r 2) (z : Fin 2 → ℝ) (ω : SmoothSample 2 L) (x : Point2) :
    coordinateGradient (smoothSourceField 2 L (freeShiftSample F z ω)) x =
      coordinateGradient (smoothSourceField 2 L ω) x+rowResponse (gradientRows L x) F z := by
  have he : gradientRows L x = fun i m => coordinateGradient (modeCoefficient 2 L m) x i := by
    funext i m
    exact gradientRows_eq L x i m
  ext i
  rw [freeShift_gradient_component hL]
  simp only [Pi.add_apply,rowResponse_apply,he,mul_comm]

private theorem freeShift_level {L r : ℝ} (hL : L≠0)
    (F : RawPinFreeFrame L r 3) (z : Fin 3 → ℝ) (ω : SmoothSample 2 L)
    (α : ℝ) (x : Point2) :
    levelConstraint α (freeShiftSample F z ω) x =
      levelConstraint α ω x+rowResponse (levelRows L x) F z := by
  have he : levelRows L x = fun i m => ![modeCoefficient 2 L m x,
      coordinateGradient (modeCoefficient 2 L m) x 0,
      coordinateGradient (modeCoefficient 2 L m) x 1] i := by
    funext i m
    exact levelRows_eq L x i m
  ext i
  fin_cases i <;> simp [levelConstraint,rowResponse_apply,he,freeShift_value hL,
    freeShift_gradient_component hL,mul_comm]
  all_goals ring

private theorem finitePairing_sub_observation {ι : Type*} (a b : ι → ℝ) (v : ι →₀ ℝ) :
    finitePairing (fun m => a m-b m) v = finitePairing a v-finitePairing b v := by
  classical
  simp [finitePairing,Finsupp.sum,sub_mul,Finset.sum_sub_distrib]

private theorem freeShift_tie {L r : ℝ} (hL : L≠0)
    (F : RawPinFreeFrame L r 5) (z : Fin 5 → ℝ) (ω : SmoothSample 2 L) (p : Point4) :
    tieConstraint (freeShiftSample F z ω) p =
      tieConstraint ω p+rowResponse (tieRows L p) F z := by
  have he : tieRows L p = fun i m =>
      ![coordinateGradient (modeCoefficient 2 L m) p.1 0,
        coordinateGradient (modeCoefficient 2 L m) p.1 1,
        coordinateGradient (modeCoefficient 2 L m) p.2 0,
        coordinateGradient (modeCoefficient 2 L m) p.2 1,
        modeCoefficient 2 L m p.1-modeCoefficient 2 L m p.2] i := by
    funext i m
    exact tieRows_eq L p i m
  ext i
  fin_cases i <;> simp [tieConstraint,rowResponse_apply,he,freeShift_value hL,
    freeShift_gradient_component hL,finitePairing_sub_observation,mul_sub,
    Finset.sum_sub_distrib,mul_comm]
  all_goals ring

private theorem sourceGradient_eval_measurable {L : ℝ} (hL : L≠0) (x : Point2) :
    Measurable (fun ω : SmoothSample 2 L => coordinateGradient (smoothSourceField 2 L ω) x) := by
  apply Measurable.of_eval
  intro i
  simpa only [iteratedFDeriv_one_apply,coordinateGradient,Matrix.cons_val_zero] using
    sourceDerivative_eval_measurable 2 hL 1 x (fun _ => Pi.single i 1)

private theorem level_eval_measurable {L : ℝ} (hL : L≠0) (α : ℝ) (x : Point2) :
    Measurable (fun ω : SmoothSample 2 L => levelConstraint α ω x) := by
  apply Measurable.of_eval
  intro i
  fin_cases i
  · exact ((I4Source.sourceField_eval_measurable 2 L x).comp
      (sampleInclusion_measurable 2 L)).sub measurable_const
  · exact (measurable_pi_apply 0).comp (sourceGradient_eval_measurable hL x)
  · exact (measurable_pi_apply 1).comp (sourceGradient_eval_measurable hL x)

private theorem tie_eval_measurable {L : ℝ} (hL : L≠0) (p : Point4) :
    Measurable (fun ω : SmoothSample 2 L => tieConstraint ω p) := by
  apply Measurable.of_eval
  intro i
  fin_cases i
  · change Measurable (fun ω : SmoothSample 2 L => coordinateGradient (smoothSourceField 2 L ω) p.1 0)
    exact (measurable_pi_apply 0).comp (sourceGradient_eval_measurable hL p.1)
  · change Measurable (fun ω : SmoothSample 2 L => coordinateGradient (smoothSourceField 2 L ω) p.1 1)
    exact (measurable_pi_apply 1).comp (sourceGradient_eval_measurable hL p.1)
  · exact (measurable_pi_apply 0).comp (sourceGradient_eval_measurable hL p.2)
  · exact (measurable_pi_apply 1).comp (sourceGradient_eval_measurable hL p.2)
  · exact (((I4Source.sourceField_eval_measurable 2 L p.1).comp
      (sampleInclusion_measurable 2 L))).sub
      ((I4Source.sourceField_eval_measurable 2 L p.2).comp (sampleInclusion_measurable 2 L))

private def constraintSquare {n : ℕ} (v : Fin n → ℝ) : ℝ := ∑ i,v i^2

private theorem constraintSquare_pos_iff {n : ℕ} (v : Fin n → ℝ) :
    0<constraintSquare v ↔ v≠0 := by
  classical
  constructor
  · intro h hv
    simp [hv,constraintSquare] at h
  · intro hv
    have hex : ∃ i,v i≠0 := by
      by_contra! h
      exact hv (funext h)
    obtain ⟨i,hi⟩ := hex
    exact Finset.sum_pos' (fun j _ => sq_nonneg (v j))
      ⟨i,Finset.mem_univ i,sq_pos_of_ne_zero hi⟩

private theorem constraintSquare_continuous {n : ℕ} :
    Continuous (constraintSquare : (Fin n → ℝ) → ℝ) := by
  unfold constraintSquare
  fun_prop

private theorem rawKernel_ae_of_sections {L r : ℝ} {n : ℕ}
    (hL : L≠0) (F : RawPinFreeFrame L r n) (t : Fin 6 → ℝ)
    (P : SmoothSample 2 L → Prop) (hP : MeasurableSet {ω | P ω})
    (hsections : ∀ ρ : SmoothSample 2 L,
      ∀ᵐ z ∂(Measure.pi (fun _ : Fin n => gaussianReal 0 1)),
        P (freeShiftSample F z (rawPosteriorSample hL r t ρ))) :
    ∀ᵐ ω ∂rawPinKernel hL r t,P ω := by
  apply (ae_iff).2
  exact rawKernel_null_of_sections hL F t {ω | ¬P ω} hP.compl
    (fun ρ => (ae_iff).1 (hsections ρ))

private theorem remote_open (L r : ℝ) : IsOpen {x : Point2 | Remote L r x} := by
  have hp := SourceActualFoldTorus.torusProjection2L_continuous L
  exact (isOpen_ne hp continuous_const).inter (isOpen_ne hp continuous_const)

private theorem remotePair_open (L r : ℝ) : IsOpen {p : Point4 | RemotePair L r p} := by
  have hp := SourceActualFoldTorus.torusProjection2L_continuous L
  exact ((remote_open L r).preimage continuous_fst).inter
    (((remote_open L r).preimage continuous_snd).inter
      (isOpen_ne (hp.comp continuous_fst) (hp.comp continuous_snd)))

private theorem morse_discriminant_nonneg {L : ℝ} (ω : SmoothSample 2 L) (x : Point2) :
    0≤sourceMorseDiscriminant L ω x := by
  unfold sourceMorseDiscriminant
  positivity

private theorem rawKernel_morse_compact {L r : ℝ} (hL : L≠0)
    (F : RawPinFreeFrame L r 2) (U : Set Point2) (hU : IsOpen U)
    (hinv : ∀x∈U,Function.Bijective(rowResponse (gradientRows L x) F))
    (K : Set Point2) (hK : IsCompact K) (hKU : K⊆U) (t : Fin 6 → ℝ) :
    ∀ᵐ ω ∂rawPinKernel hL r t,∀x∈K,0<sourceMorseDiscriminant L ω x := by
  classical
  apply rawKernel_ae_of_sections hL F t (fun ω => ∀x∈K,0<sourceMorseDiscriminant L ω x)
  · exact measurableSet_forall_mem_pos_of_isCompact hK (sourceMorseDiscriminant L)
      (fun ω => (sourceMorseDiscriminant_spatial_continuous hL ω).continuousOn)
      (fun x _ => sourceMorseDiscriminant_eval_measurable hL x)
  · intro ρ
    let σ := rawPosteriorSample hL r t ρ
    let g := coordinateGradient (smoothSourceField 2 L σ)
    let B := fun x => rowResponse (gradientRows L x) F
    have hnull := incidence_morse_null U hU g B
      (coordinateGradient_contDiff _ (smoothSourceField_smooth 2 hL σ)).contDiffOn
      (gradient_response_smooth F).contDiffOn hinv
    apply (ae_iff).2
    apply measure_mono_null ?_ hnull
    intro z hz
    simp only [not_forall,not_imp,not_lt] at hz
    obtain ⟨x,hx,hbad⟩ := hz
    have hd : sourceMorseDiscriminant L (freeShiftSample F z σ) x=0 :=
      le_antisymm hbad (morse_discriminant_nonneg _ _)
    rw [sourceMorseDiscriminant_eq L hL] at hd
    let G := coordinateGradient (smoothSourceField 2 L (freeShiftSample F z σ))
    have h0 : G x 0=0 := by
      apply sq_eq_zero_iff.mp
      have h1 := sq_nonneg (G x 1)
      have h2 := sq_nonneg ((fderiv ℝ G x).det)
      change (G x 0)^2+(G x 1)^2+(fderiv ℝ G x).det^2=0 at hd
      nlinarith
    have h1 : G x 1=0 := by
      apply sq_eq_zero_iff.mp
      have h2 := sq_nonneg ((fderiv ℝ G x).det)
      change (G x 0)^2+(G x 1)^2+(fderiv ℝ G x).det^2=0 at hd
      nlinarith
    have hG : G x=0 := by ext i; fin_cases i <;> assumption
    have hdet : (fderiv ℝ G x).det=0 := by
      apply sq_eq_zero_iff.mp
      change (G x 0)^2+(G x 1)^2+(fderiv ℝ G x).det^2=0 at hd
      simpa only [h0,h1,zero_pow (by decide : 2≠0),zero_add] using hd
    have hsing : ¬Function.Injective (fderiv ℝ G x) := by
      have hk := LinearMap.det_eq_zero_iff_ker_ne_bot.mp hdet
      intro hi
      exact hk (LinearMap.ker_eq_bot.mpr hi)
    have hfun : (fun y => g y+B y z)=G := by
      funext y
      exact (freeShift_gradient hL F z σ y).symm
    refine ⟨x,hKU hx,?_,?_⟩
    · rw [← hfun] at hG
      exact hG
    · simpa only [hfun] using hsing

private theorem rawKernel_level_compact {L r : ℝ} (hL : L≠0)
    (F : RawPinFreeFrame L r 3) (U : Set Point2) (hU : IsOpen U)
    (hinv : ∀x∈U,Function.Bijective(rowResponse (levelRows L x) F))
    (K : Set Point2) (hK : IsCompact K) (hKU : K⊆U)
    (t : Fin 6 → ℝ) (α : ℝ) :
    ∀ᵐ ω ∂rawPinKernel hL r t,∀x∈K,0<constraintSquare (levelConstraint α ω x) := by
  classical
  apply rawKernel_ae_of_sections hL F t
    (fun ω => ∀x∈K,0<constraintSquare (levelConstraint α ω x))
  · apply measurableSet_forall_mem_pos_of_isCompact hK
      (fun ω x => constraintSquare (levelConstraint α ω x))
    · intro ω
      exact (constraintSquare_continuous.comp (level_constraint_smooth hL α ω).continuous).continuousOn
    · intro x _
      exact constraintSquare_continuous.measurable.comp (level_eval_measurable hL α x)
  · intro ρ
    let σ := rawPosteriorSample hL r t ρ
    have hnull := incidence_level_null U hU (levelConstraint α σ)
      (fun x => rowResponse (levelRows L x) F)
      (level_constraint_smooth hL α σ).contDiffOn
      (level_response_smooth F).contDiffOn hinv
    apply (ae_iff).2
    apply measure_mono_null ?_ hnull
    intro z hz
    simp only [not_forall,not_imp] at hz
    obtain ⟨x,hx,hbad⟩ := hz
    have hc : levelConstraint α (freeShiftSample F z σ) x=0 := by
      by_contra hc
      exact hbad ((constraintSquare_pos_iff _).2 hc)
    exact ⟨x,hKU hx,(freeShift_level hL F z σ α x).symm.trans hc⟩

private theorem rawKernel_tie_compact {L r : ℝ} (hL : L≠0)
    (F : RawPinFreeFrame L r 5) (U : Set Point4) (hU : IsOpen U)
    (hinv : ∀x∈U,Function.Bijective(rowResponse (tieRows L x) F))
    (K : Set Point4) (hK : IsCompact K) (hKU : K⊆U) (t : Fin 6 → ℝ) :
    ∀ᵐ ω ∂rawPinKernel hL r t,∀x∈K,0<constraintSquare (tieConstraint ω x) := by
  classical
  apply rawKernel_ae_of_sections hL F t
    (fun ω => ∀x∈K,0<constraintSquare (tieConstraint ω x))
  · apply measurableSet_forall_mem_pos_of_isCompact hK
      (fun ω x => constraintSquare (tieConstraint ω x))
    · intro ω
      exact (constraintSquare_continuous.comp (tie_constraint_smooth hL ω).continuous).continuousOn
    · intro x _
      exact constraintSquare_continuous.measurable.comp (tie_eval_measurable hL x)
  · intro ρ
    let σ := rawPosteriorSample hL r t ρ
    have hnull := incidence_tie_null U hU (tieConstraint σ)
      (fun x => rowResponse (tieRows L x) F)
      (tie_constraint_smooth hL σ).contDiffOn
      (tie_response_smooth F).contDiffOn hinv
    apply (ae_iff).2
    apply measure_mono_null ?_ hnull
    intro z hz
    simp only [not_forall,not_imp] at hz
    obtain ⟨x,hx,hbad⟩ := hz
    have hc : tieConstraint (freeShiftSample F z σ) x=0 := by
      by_contra hc
      exact hbad ((constraintSquare_pos_iff _).2 hc)
    exact ⟨x,hKU hx,(freeShift_tie hL F z σ x).symm.trans hc⟩

private theorem rawKernel_remote_morse {L : ℝ} (hL : L≠0) (r : ℝ) (t : Fin 6 → ℝ) :
    ∀ᵐ ω ∂rawPinKernel hL r t,∀x,Remote L r x → 0<sourceMorseDiscriminant L ω x := by
  apply countable_compact_local_ae (rawPinKernel hL r t) {x | Remote L r x}
    (remote_open L r) (fun ω x => 0<sourceMorseDiscriminant L ω x)
  intro x hx
  obtain ⟨F,hF⟩ := gradient_frame hL r x hx
  obtain ⟨U,hU,hxU,hInv⟩ := response_neighborhood
    (fun y => rowResponse (gradientRows L y) F) (gradient_response_smooth F).continuous x hF
  refine ⟨U∩{y | Remote L r y},hU.inter (remote_open L r),⟨hxU,hx⟩,
    inter_subset_right,?_⟩
  intro K hK hKU
  exact rawKernel_morse_compact hL F U hU hInv K hK
    (hKU.trans inter_subset_left) t

private theorem rawKernel_remote_level {L : ℝ} (hL : L≠0) (r : ℝ)
    (t : Fin 6 → ℝ) (α : ℝ) :
    ∀ᵐ ω ∂rawPinKernel hL r t,∀x,Remote L r x →
      coordinateGradient (smoothSourceField 2 L ω) x=0 → smoothSourceField 2 L ω x≠α := by
  have hall : ∀ᵐ ω ∂rawPinKernel hL r t,∀x∈{x | Remote L r x},
      0<constraintSquare (levelConstraint α ω x) := by
    apply countable_compact_local_ae (rawPinKernel hL r t) {x | Remote L r x}
      (remote_open L r) (fun ω x => 0<constraintSquare (levelConstraint α ω x))
    intro x hx
    obtain ⟨F,hF⟩ := level_frame hL r x hx
    obtain ⟨U,hU,hxU,hInv⟩ := response_neighborhood
      (fun y => rowResponse (levelRows L y) F) (level_response_smooth F).continuous x hF
    refine ⟨U∩{y | Remote L r y},hU.inter (remote_open L r),⟨hxU,hx⟩,
      inter_subset_right,?_⟩
    intro K hK hKU
    exact rawKernel_level_compact hL F U hU hInv K hK
      (hKU.trans inter_subset_left) t α
  filter_upwards [hall] with ω hω
  intro x hx hc hv
  have hn := (constraintSquare_pos_iff _).1 (hω x hx)
  apply hn
  ext i
  fin_cases i <;> simp [levelConstraint,hv,hc]

private theorem rawKernel_remote_tie {L : ℝ} (hL : L≠0) (r : ℝ) (t : Fin 6 → ℝ) :
    ∀ᵐ ω ∂rawPinKernel hL r t,∀p,RemotePair L r p →
      coordinateGradient (smoothSourceField 2 L ω) p.1=0 →
      coordinateGradient (smoothSourceField 2 L ω) p.2=0 →
      smoothSourceField 2 L ω p.1≠smoothSourceField 2 L ω p.2 := by
  have hall : ∀ᵐ ω ∂rawPinKernel hL r t,∀p∈{p | RemotePair L r p},
      0<constraintSquare (tieConstraint ω p) := by
    apply countable_compact_local_ae (rawPinKernel hL r t) {p | RemotePair L r p}
      (remotePair_open L r) (fun ω p => 0<constraintSquare (tieConstraint ω p))
    intro p hp
    obtain ⟨F,hF⟩ := tie_frame hL r p hp
    obtain ⟨U,hU,hpU,hInv⟩ := response_neighborhood
      (fun q => rowResponse (tieRows L q) F) (tie_response_smooth F).continuous p hF
    refine ⟨U∩{q | RemotePair L r q},hU.inter (remotePair_open L r),⟨hpU,hp⟩,
      inter_subset_right,?_⟩
    intro K hK hKU
    exact rawKernel_tie_compact hL F U hU hInv K hK
      (hKU.trans inter_subset_left) t
  filter_upwards [hall] with ω hω
  intro p hp hc1 hc2 hv
  have hn := (constraintSquare_pos_iff _).1 (hω p hp)
  apply hn
  ext i
  fin_cases i <;> simp [tieConstraint,hv,hc1,hc2]

/- These source-local positives directly exercise the new private solved-source
   normal-equation and dummy adapters, with actual original source functions. -/
private theorem actual_source_normal_equation {L r : ℝ} (hL : L≠0)
    (F : RawPinFreeFrame L r 2) (ω : SmoothSample 2 L)
    (U : Set Point2) (hU : IsOpen U)
    (hinv : ∀x∈U,Function.Bijective(rowResponse (gradientRows L x) F))
    (x : Point2) (hx : x∈U) (v : Point2) :
    let g := coordinateGradient (smoothSourceField 2 L ω)
    let B := fun y => rowResponse (gradientRows L y) F
    B x (fderiv ℝ (incidence_theta g B) x v)=
      -(fderiv ℝ g x v+(fderiv ℝ B x v) (incidence_theta g B x)) := by
  exact incidence_full_normal_equation U hU _ _
    (coordinateGradient_contDiff _ (smoothSourceField_smooth 2 hL ω)).contDiffOn
    (gradient_response_smooth F).contDiffOn hinv x hx v

private theorem actual_level_dummy_control {L r : ℝ} (hL : L≠0)
    (F : RawPinFreeFrame L r 3) (ω : SmoothSample 2 L) (α : ℝ)
    (U : Set Point2) (hU : IsOpen U)
    (hinv : ∀x∈U,Function.Bijective(rowResponse (levelRows L x) F))
    (x : Point2) (hx : x∈U) :
    let θ := incidence_theta (levelConstraint α ω) (fun y => rowResponse (levelRows L y) F)
    (fderiv ℝ (fun y => θ (incidence_project3 y)) (incidence_embed3 x)).det=0 := by
  apply incidence_dummy3_det_zero
  rw [incidence_project3_embed3]
  exact incidence_theta_differentiable U hU _ _
    (level_constraint_smooth hL α ω).contDiffOn (level_response_smooth F).contDiffOn hinv x hx

private theorem actual_tie_dummy_control {L r : ℝ} (hL : L≠0)
    (F : RawPinFreeFrame L r 5) (ω : SmoothSample 2 L)
    (U : Set Point4) (hU : IsOpen U)
    (hinv : ∀x∈U,Function.Bijective(rowResponse (tieRows L x) F))
    (x : Point4) (hx : x∈U) :
    let θ := incidence_theta (tieConstraint ω) (fun y => rowResponse (tieRows L y) F)
    (fderiv ℝ (fun y => θ (incidence_project5 y)) (incidence_embed5 x)).det=0 := by
  apply incidence_dummy5_det_zero
  rw [incidence_project5_embed5]
  exact incidence_theta_differentiable U hU _ _
    (tie_constraint_smooth hL ω).contDiffOn (tie_response_smooth F).contDiffOn hinv x hx

private def sourceDet {L : ℝ} (ω : SmoothSample 2 L) (x : Point2) : ℝ :=
  (iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω) x ![directionX,directionX]) *
    (iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω) x ![directionY,directionY]) -
    (iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω) x ![directionX,directionY])^2

private theorem positive_discriminant_det {L : ℝ} (_hL : L≠0)
    (ω : SmoothSample 2 L) (x : Point2)
    (hpos : 0<sourceMorseDiscriminant L ω x)
    (hcrit : coordinateGradient (smoothSourceField 2 L ω) x=0) : sourceDet ω x≠0 := by
  have hx := congrFun hcrit (0 : Fin 2)
  have hy := congrFun hcrit (1 : Fin 2)
  change fderiv ℝ (smoothSourceField 2 L ω) x (Pi.single 0 1)=0 at hx
  change fderiv ℝ (smoothSourceField 2 L ω) x (Pi.single 1 1)=0 at hy
  change (iteratedFDeriv ℝ 1 (smoothSourceField 2 L ω) x ![directionX])^2+
    (iteratedFDeriv ℝ 1 (smoothSourceField 2 L ω) x ![directionY])^2+
      (sourceDet ω x)^2>0 at hpos
  simp only [iteratedFDeriv_one_apply,Matrix.cons_val_zero,source_directionX_eq,
    source_directionY_eq,hx,hy,zero_pow (by decide : 2≠0),zero_add] at hpos
  exact sq_pos_iff.mp hpos

private theorem sourceDet_projection {L : ℝ} (hL : 0<L) (ω : SmoothSample 2 L)
    (x y : Point2) (h : I4Torus.torusProjection 2 L x=I4Torus.torusProjection 2 L y) :
    sourceDet ω x=sourceDet ω y := by
  unfold sourceDet
  rw [(source_jets_of_projection_eq hL ω x y h).2 2]

private theorem small_pins_separate {L r : ℝ} (hL : 0<L) (hr : 0<r) (hrL : r<L/2) :
    I4Torus.torusProjection 2 L (endpointM r)≠I4Torus.torusProjection 2 L (endpointS r) := by
  intro h
  have hzero := projection_eq_torusDist_zero hL (endpointLiftM r) (endpointLiftS r)
    (by simpa [endpointLiftM,endpointLiftS] using h)
  rw [endpoint_lifts_torusDist hL hr hrL] at hzero
  exact hr.ne' hzero

private theorem endpoint_determinants {L : ℝ} (hL : L≠0) (r : ℝ)
    (hsep : I4Torus.torusProjection 2 L (endpointM r)≠I4Torus.torusProjection 2 L (endpointS r))
    (t : Fin 6 → ℝ) :
    ∀ᵐ ω ∂rawPinKernel hL r t,sourceDet ω (endpointM r)≠0 ∧ sourceDet ω (endpointS r)≠0 := by
  filter_upwards [I4SourceEndpointHessianGaussian.rawPinKernel_ae_endpointHessian_det_ne_zero
    hL r hsep t] with ω hω
  have hM := hω (0 : Fin 2)
  have hS := hω (1 : Fin 2)
  change sourceDet ω (endpointM r)≠0 at hM
  change sourceDet ω (endpointS r)≠0 at hS
  exact ⟨hM,hS⟩

private theorem critical_values_distinct {L r b k : ℝ} (ω : SmoothSample 2 L)
    (hgap : b≠b-k*r^3)
    (hM : ∀x, I4Torus.torusProjection 2 L x=I4Torus.torusProjection 2 L (endpointM r) →
      smoothSourceField 2 L ω x=b)
    (hS : ∀x, I4Torus.torusProjection 2 L x=I4Torus.torusProjection 2 L (endpointS r) →
      smoothSourceField 2 L ω x=b-k*r^3)
    (hlevelM : ∀x,Remote L r x → coordinateGradient (smoothSourceField 2 L ω) x=0 →
      smoothSourceField 2 L ω x≠b)
    (hlevelS : ∀x,Remote L r x → coordinateGradient (smoothSourceField 2 L ω) x=0 →
      smoothSourceField 2 L ω x≠b-k*r^3)
    (htie : ∀p,RemotePair L r p → coordinateGradient (smoothSourceField 2 L ω) p.1=0 →
      coordinateGradient (smoothSourceField 2 L ω) p.2=0 →
      smoothSourceField 2 L ω p.1≠smoothSourceField 2 L ω p.2)
    (x y : Point2) (hx : coordinateGradient (smoothSourceField 2 L ω) x=0)
    (hy : coordinateGradient (smoothSourceField 2 L ω) y=0)
    (hxy : I4Torus.torusProjection 2 L x≠I4Torus.torusProjection 2 L y) :
    smoothSourceField 2 L ω x≠smoothSourceField 2 L ω y := by
  classical
  intro heq
  by_cases hxM : I4Torus.torusProjection 2 L x=I4Torus.torusProjection 2 L (endpointM r)
  · by_cases hyM : I4Torus.torusProjection 2 L y=I4Torus.torusProjection 2 L (endpointM r)
    · exact hxy (hxM.trans hyM.symm)
    by_cases hyS : I4Torus.torusProjection 2 L y=I4Torus.torusProjection 2 L (endpointS r)
    · exact hgap ((hM x hxM).symm.trans (heq.trans (hS y hyS)))
    · exact hlevelM y ⟨hyM,hyS⟩ hy (heq.symm.trans (hM x hxM))
  by_cases hxS : I4Torus.torusProjection 2 L x=I4Torus.torusProjection 2 L (endpointS r)
  · by_cases hyM : I4Torus.torusProjection 2 L y=I4Torus.torusProjection 2 L (endpointM r)
    · exact hgap ((hM y hyM).symm.trans (heq.symm.trans (hS x hxS)))
    by_cases hyS : I4Torus.torusProjection 2 L y=I4Torus.torusProjection 2 L (endpointS r)
    · exact hxy (hxS.trans hyS.symm)
    · exact hlevelS y ⟨hyM,hyS⟩ hy (heq.symm.trans (hS x hxS))
  by_cases hyM : I4Torus.torusProjection 2 L y=I4Torus.torusProjection 2 L (endpointM r)
  · exact hlevelM x ⟨hxM,hxS⟩ hx (heq.trans (hM y hyM))
  by_cases hyS : I4Torus.torusProjection 2 L y=I4Torus.torusProjection 2 L (endpointS r)
  · exact hlevelS x ⟨hxM,hxS⟩ hx (heq.trans (hS y hyS))
  exact htie (x,y) ⟨⟨hxM,hxS⟩,⟨hyM,hyS⟩,hxy⟩ hx hy heq

private theorem rawKernel_gap_morseDistinct {L r b k : ℝ} (hL : 0<L)
    (hr : 0<r) (hrL : r<L/2) (hk : 0<k)
    (hG : IsUnit (I4SourceEndpointRegression.sourcePinCovarianceAt L r)) :
    ∀ᵐ ω ∂rawPinKernel hL.ne' r ![b,b-k*r^3,0,0,0,0],
      IsMorseDistinct 2 L (actualField 2 L ω) := by
  let t : Fin 6 → ℝ := ![b,b-k*r^3,0,0,0,0]
  have hfiber : ∀ᵐ ω ∂rawPinKernel hL.ne' r t, rawPins L r ω=t := by
    apply (mem_ae_iff_prob_eq_one
      (measurableSet_eq_fun (rawPins_measurable hL.ne' r) measurable_const)).2
    exact rawPinKernel_pin_fiber hL.ne' r hr.ne' hG t
  have hgap : b≠b-k*r^3 := by
    have hp := mul_pos hk (pow_pos hr 3)
    linarith
  filter_upwards [hfiber,rawKernel_remote_morse hL.ne' r t,
    rawKernel_remote_level hL.ne' r t b,rawKernel_remote_level hL.ne' r t (b-k*r^3),
    rawKernel_remote_tie hL.ne' r t,
    endpoint_determinants hL.ne' r (small_pins_separate hL hr hrL) t] with
      ω hp hremote hlevelM hlevelS htie hend
  have hheights := actual_rawPins_heights ω hp
  have hM0 : smoothSourceField 2 L ω (endpointM r)=b := by
    simpa only [actualField,ContinuousLinearEquiv.apply_symm_apply] using hheights.1
  have hS0 : smoothSourceField 2 L ω (endpointS r)=b-k*r^3 := by
    simpa only [actualField,ContinuousLinearEquiv.apply_symm_apply] using hheights.2.1
  have hM (x : Point2)
      (hx : I4Torus.torusProjection 2 L x=I4Torus.torusProjection 2 L (endpointM r)) :
      smoothSourceField 2 L ω x=b :=
    (source_jets_of_projection_eq hL ω x (endpointM r) hx).1.trans hM0
  have hS (x : Point2)
      (hx : I4Torus.torusProjection 2 L x=I4Torus.torusProjection 2 L (endpointS r)) :
      smoothSourceField 2 L ω x=b-k*r^3 :=
    (source_jets_of_projection_eq hL ω x (endpointS r) hx).1.trans hS0
  constructor
  · intro X hX
    have hcrit := actual_critical_coordinateGradient_zero hL ω X hX
    apply actual_inertia_of_source_det hL ω X
    change sourceDet ω (coordinates 2 X)≠0
    by_cases hxM : I4Torus.torusProjection 2 L (coordinates 2 X)=
        I4Torus.torusProjection 2 L (endpointM r)
    · rw [sourceDet_projection hL ω _ _ hxM]
      exact hend.1
    by_cases hxS : I4Torus.torusProjection 2 L (coordinates 2 X)=
        I4Torus.torusProjection 2 L (endpointS r)
    · rw [sourceDet_projection hL ω _ _ hxS]
      exact hend.2
    exact positive_discriminant_det hL.ne' ω _ (hremote _ ⟨hxM,hxS⟩) hcrit
  · intro X Y hX hY hdist
    have hxy : I4Torus.torusProjection 2 L (coordinates 2 X)≠
        I4Torus.torusProjection 2 L (coordinates 2 Y) := by
      intro heq
      exact (ne_of_gt hdist) (projection_eq_torusDist_zero hL X Y heq)
    exact critical_values_distinct ω hgap hM hS hlevelM hlevelS htie
      (coordinates 2 X) (coordinates 2 Y)
      (actual_critical_coordinateGradient_zero hL ω X hX)
      (actual_critical_coordinateGradient_zero hL ω Y hY) hxy

/-- The actual positive-gap sampling law is almost surely literally Morse with
distinct critical values; one interval precedes all target marks. -/
theorem sourceGapLaw_ae_isMorseDistinct {L : ℝ} (hL : 0<L) :
    ∃ δ : ℝ, 0<δ ∧ δ≤1 ∧ δ≤L/2 ∧
      ∀ r : ℝ, 0<r → r<δ → ∀ b k : ℝ, 0<k →
        ∀ᵐ ω ∂sourceGapLaw hL.ne' r b k,IsMorseDistinct 2 L (actualField 2 L ω) := by
  obtain ⟨C,δ0,_hC,hδ0,hδ01,hI⟩ := sourceInverse_target_uniform_bounds hL.ne'
  refine ⟨min δ0 (L/2),lt_min hδ0 (half_pos hL),
    (min_le_left _ _).trans hδ01,min_le_right _ _,?_⟩
  intro r hr hrδ b k hk
  have hrδ0 := hrδ.trans_le (min_le_left δ0 (L/2))
  have hrL := hrδ.trans_le (min_le_right δ0 (L/2))
  rw [sourceGapLaw_eq_rawPinKernel hL.ne' r b k hr.ne']
  exact rawKernel_gap_morseDistinct hL hr hrL hk (hI r hr hrδ0).1

end I4SourceGapConditionalMorseDistinct
