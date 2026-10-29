import SourceSmoothConditionalKernel
import Mathlib.Topology.ContinuousMap.Bounded.Normed
import Mathlib.Topology.ContinuousMap.Compact
import Mathlib.MeasureTheory.Function.StronglyMeasurable.Basic
import Mathlib.MeasureTheory.Constructions.BorelSpace.Metrizable

/-!
# Actual derivative fields and finite jets in their norm Borel structures

Every source sample has a normally convergent Fourier series in the bounded
continuous derivative norm. Strong measurability of that limit also controls
whole finite jet tuples, without replacing norm Borel sets by a coordinate
product sigma algebra. See SOURCE_SMOOTH_TOPOLOGY.md for the frozen scope and
the explicit remaining C3-torus/dynamical interface boundary.
-/

noncomputable section
open I4Foundation I4Source I4Smooth I4SmoothCarrier I4SourceDerivativeGaussian
open MeasureTheory Filter BoundedContinuousFunction TopologicalSpace
open scoped BigOperators Topology

set_option autoImplicit false

namespace I4SourceSmoothTopology

abbrev DerivativeOperator (d k : ℕ) :=
  ContinuousMultilinearMap ℝ (fun _ : Fin k => Fin d → ℝ) ℝ

abbrev DerivativeBCF (d k : ℕ) := (Fin d → ℝ) →ᵇ DerivativeOperator d k

theorem modeCoefficient_contDiff (d : ℕ) (L : ℝ) (m : SourceMode d) (k : ℕ) :
    ContDiff ℝ k (modeCoefficient d L m) := by
  cases m with
  | none =>
    change ContDiff ℝ k (fun _ : Fin d → ℝ => Real.sqrt (1 / I4Weights.sourceZ d L))
    fun_prop
  | some p =>
    rcases p with ⟨u,b⟩
    change ContDiff ℝ k (fun x : Fin d → ℝ =>
      Real.sqrt (2 * I4Weights.sourceWeight d L u / I4Weights.sourceZ d L) *
        (if b then Real.sin (phase d L u x) else Real.cos (phase d L u x)))
    cases b <;> simp [phase] <;> fun_prop

def modeDerivativeBCF (d : ℕ) {L : ℝ} (hL : L ≠ 0) (k : ℕ) (m : SourceMode d) :
    DerivativeBCF d k :=
  ofNormedAddCommGroup (iteratedFDeriv ℝ k (modeCoefficient d L m))
    (modeCoefficient_contDiff d L m k).continuous_iteratedFDeriv'
    (orderModeBound k d L m) (modeCoefficient_iteratedFDeriv_order_bound d hL m k)

theorem modeDerivativeBCF_norm_le (d : ℕ) {L : ℝ} (hL : L ≠ 0) (k : ℕ) (m : SourceMode d) :
    ‖modeDerivativeBCF d hL k m‖ ≤ orderModeBound k d L m :=
  norm_ofNormedAddCommGroup_le _ (orderModeBound_nonneg k d L m)
    (modeCoefficient_iteratedFDeriv_order_bound d hL m k)

theorem sourceDerivativeBCF_summable (d : ℕ) {L : ℝ} (hL : L ≠ 0)
    (k : ℕ) (ω : SmoothSample d L) :
    Summable (fun m => ω.val m • modeDerivativeBCF d hL k m) := by
  apply Summable.of_norm_bounded
    (f := fun m => (ω.val m • modeDerivativeBCF d hL k m : DerivativeBCF d k)) (ω.property k)
  intro m
  apply (BoundedContinuousFunction.norm_le
    (mul_nonneg (orderModeBound_nonneg k d L m) (abs_nonneg (ω.val m)))).2
  intro x
  change ‖ω.val m • iteratedFDeriv ℝ k (modeCoefficient d L m) x‖ ≤ _
  rw [norm_smul, Real.norm_eq_abs]
  exact (mul_le_mul_of_nonneg_left (modeCoefficient_iteratedFDeriv_order_bound d hL m k x)
    (abs_nonneg _)).trans_eq (mul_comm _ _)

def sourceDerivativeBCF (d : ℕ) {L : ℝ} (hL : L ≠ 0) (k : ℕ) (ω : SmoothSample d L) :
    DerivativeBCF d k := ∑' m, ω.val m • modeDerivativeBCF d hL k m

theorem sourceDerivativeBCF_apply (d : ℕ) {L : ℝ} (hL : L ≠ 0)
    (k : ℕ) (ω : SmoothSample d L) (x : Fin d → ℝ) :
    sourceDerivativeBCF d hL k ω x = iteratedFDeriv ℝ k (smoothSourceField d L ω) x := by
  have hs := sourceDerivativeBCF_summable d hL k ω
  have hx := hs.hasSum.map (BoundedContinuousFunction.evalCLM ℝ x).toAddMonoidHom
    (BoundedContinuousFunction.evalCLM ℝ x).continuous
  change HasSum (fun m => ω.val m • iteratedFDeriv ℝ k (modeCoefficient d L m) x)
    (sourceDerivativeBCF d hL k ω x) at hx
  apply ContinuousMultilinearMap.ext
  intro u
  rw [← hx.tsum_eq, ContinuousMultilinearMap.tsum_eval hx.summable,
    smoothSourceField_derivative_series d hL ω k x u]
  apply tsum_congr
  intro m
  simp [derivativeCoefficient, smul_eq_mul, mul_comm, sampleInclusion]

theorem stronglyMeasurable_of_countable_hasSum {I Ω E : Type*} [Countable I]
    [MeasurableSpace Ω] [TopologicalSpace E] [PseudoMetrizableSpace E]
    [AddCommMonoid E] [ContinuousAdd E]
    (f : I → Ω → E) (g : Ω → E) (hf : ∀ i, StronglyMeasurable (f i))
    (hs : ∀ ω, HasSum (fun i => f i ω) (g ω)) : StronglyMeasurable g := by
  classical
  apply stronglyMeasurable_of_tendsto (atTop : Filter (Finset I))
    (fun s => s.stronglyMeasurable_fun_sum (fun i _ => hf i))
  exact tendsto_pi_nhds.mpr hs

theorem sourceDerivativeBCF_stronglyMeasurable (d : ℕ) {L : ℝ} (hL : L ≠ 0) (k : ℕ) :
    StronglyMeasurable (sourceDerivativeBCF d hL k) := by
  apply stronglyMeasurable_of_countable_hasSum
    (fun m (ω : SmoothSample d L) => ω.val m • modeDerivativeBCF d hL k m)
  · intro m
    exact (((measurable_pi_apply m).comp measurable_subtype_coe).stronglyMeasurable).smul_const _
  · intro ω
    exact (sourceDerivativeBCF_summable d hL k ω).hasSum

/-- Borel means the norm topology on the actual bounded continuous derivative
field, with no substitution of coordinate-product measurable structure. -/
theorem sourceDerivativeBCF_borel (d : ℕ) {L : ℝ} (hL : L ≠ 0) (k : ℕ) :
    @Measurable (SmoothSample d L) (DerivativeBCF d k) _ (borel _) (sourceDerivativeBCF d hL k) := by
  borelize (DerivativeBCF d k)
  exact (sourceDerivativeBCF_stronglyMeasurable d hL k).measurable

def sourceFiniteJet (d : ℕ) {L : ℝ} (hL : L ≠ 0) (K : ℕ) (ω : SmoothSample d L) :
    (j : Fin (K+1)) → DerivativeBCF d j := fun j => sourceDerivativeBCF d hL j ω

theorem sourceFiniteJet_stronglyMeasurable (d : ℕ) {L : ℝ} (hL : L ≠ 0) (K : ℕ) :
    StronglyMeasurable (sourceFiniteJet d hL K) := by
  let a : SourceMode d → SmoothSample d L → ((j : Fin (K+1)) → DerivativeBCF d j) :=
    fun m ω j => ω.val m • modeDerivativeBCF d hL j m
  have ha (m : SourceMode d) : StronglyMeasurable (a m) := by
    have hc : Continuous (fun c : ℝ => fun j : Fin (K+1) => c • modeDerivativeBCF d hL j m) := by
      apply continuous_pi
      intro j
      exact (continuous_id : Continuous (fun c : ℝ => c)).smul continuous_const
    exact hc.comp_stronglyMeasurable
      (((measurable_pi_apply m).comp measurable_subtype_coe).stronglyMeasurable)
  apply stronglyMeasurable_of_countable_hasSum a _ ha
  intro ω
  exact Pi.hasSum.mpr (fun j => (sourceDerivativeBCF_summable d hL j ω).hasSum)

theorem sourceFiniteJet_borel (d : ℕ) {L : ℝ} (hL : L ≠ 0) (K : ℕ) :
    @Measurable (SmoothSample d L) ((j : Fin (K+1)) → DerivativeBCF d j)
      _ (borel _) (sourceFiniteJet d hL K) := by
  borelize ((j : Fin (K+1)) → DerivativeBCF d j)
  exact (sourceFiniteJet_stronglyMeasurable d hL K).measurable

end I4SourceSmoothTopology

namespace I4SourceSmoothTopology

@[simp] theorem modeDerivativeBCF_apply (d : ℕ) {L : ℝ} (hL : L ≠ 0)
    (k : ℕ) (m : SourceMode d) (x : Fin d → ℝ) :
    modeDerivativeBCF d hL k m x = iteratedFDeriv ℝ k (modeCoefficient d L m) x := rfl

/-- Convergence is uniform in the real source variable and holds for every
sample, rather than only almost surely under one law. -/
theorem sourceDerivativeBCF_tendstoUniformly (d : ℕ) {L : ℝ} (hL : L ≠ 0)
    (k : ℕ) (ω : SmoothSample d L) :
    TendstoUniformly
      (fun s : Finset (SourceMode d) =>
        ((∑ m ∈ s, ω.val m • modeDerivativeBCF d hL k m) : DerivativeBCF d k))
      (iteratedFDeriv ℝ k (smoothSourceField d L ω)) atTop := by
  have hn : Tendsto (fun s : Finset (SourceMode d) => ∑ m ∈ s, ω.val m • modeDerivativeBCF d hL k m)
      atTop (𝓝 (sourceDerivativeBCF d hL k ω)) := (sourceDerivativeBCF_summable d hL k ω).hasSum
  have hu := BoundedContinuousFunction.tendsto_iff_tendstoUniformly.mp hn
  have heq : (sourceDerivativeBCF d hL k ω : (Fin d → ℝ) → DerivativeOperator d k) =
      iteratedFDeriv ℝ k (smoothSourceField d L ω) := funext (sourceDerivativeBCF_apply d hL k ω)
  rw [← heq]
  exact hu

/-- Restrict ambient derivative fields along a continuous chart parameter.
For a compact chart this is the usual uniform restriction map. -/
def jetRestriction {A : Type*} [TopologicalSpace A] (d K : ℕ) (i : C(A, Fin d → ℝ))
    (v : (j : Fin (K+1)) → DerivativeBCF d j) : (j : Fin (K+1)) → (A →ᵇ DerivativeOperator d j) :=
  fun j => (v j).compContinuous i

theorem jetRestriction_continuous {A : Type*} [TopologicalSpace A]
    (d K : ℕ) (i : C(A, Fin d → ℝ)) : Continuous (jetRestriction d K i) := by
  apply continuous_pi
  intro j
  exact (BoundedContinuousFunction.continuous_compContinuous i).comp (continuous_apply j)

theorem jetRestriction_norm_le {A : Type*} [TopologicalSpace A]
    (d K : ℕ) (i : C(A, Fin d → ℝ)) (v : (j : Fin (K+1)) → DerivativeBCF d j) :
    ‖jetRestriction d K i v‖ ≤ ‖v‖ := by
  apply (pi_norm_le_iff_of_nonneg (norm_nonneg v)).2
  intro j
  exact (BoundedContinuousFunction.norm_compContinuous_le (v j) i).trans (norm_le_pi_norm v j)

def sourceRestrictedJet {A : Type*} [TopologicalSpace A] (d : ℕ) {L : ℝ}
    (hL : L ≠ 0) (K : ℕ) (i : C(A, Fin d → ℝ)) (ω : SmoothSample d L) :
    (j : Fin (K+1)) → (A →ᵇ DerivativeOperator d j) := jetRestriction d K i (sourceFiniteJet d hL K ω)

theorem sourceRestrictedJet_apply {A : Type*} [TopologicalSpace A] (d : ℕ) {L : ℝ}
    (hL : L ≠ 0) (K : ℕ) (i : C(A, Fin d → ℝ)) (ω : SmoothSample d L)
    (j : Fin (K+1)) (x : A) :
    sourceRestrictedJet d hL K i ω j x = iteratedFDeriv ℝ j (smoothSourceField d L ω) (i x) :=
  sourceDerivativeBCF_apply d hL j ω (i x)

theorem sourceRestrictedJet_stronglyMeasurable {A : Type*} [TopologicalSpace A]
    (d : ℕ) {L : ℝ} (hL : L ≠ 0) (K : ℕ) (i : C(A, Fin d → ℝ)) :
    StronglyMeasurable (sourceRestrictedJet d hL K i) :=
  (jetRestriction_continuous d K i).comp_stronglyMeasurable (sourceFiniteJet_stronglyMeasurable d hL K)

theorem sourceRestrictedJet_borel {A : Type*} [TopologicalSpace A]
    (d : ℕ) {L : ℝ} (hL : L ≠ 0) (K : ℕ) (i : C(A, Fin d → ℝ)) :
    @Measurable (SmoothSample d L) ((j : Fin (K+1)) → (A →ᵇ DerivativeOperator d j))
      _ (borel _) (sourceRestrictedJet d hL K i) := by
  borelize ((j : Fin (K+1)) → (A →ᵇ DerivativeOperator d j))
  exact (sourceRestrictedJet_stronglyMeasurable d hL K i).measurable

/-- The finite jet norm is exactly a maximum uniform derivative metric. -/
theorem sourceFiniteJet_dist_le_iff (d : ℕ) {L : ℝ} (hL : L ≠ 0) (K : ℕ)
    (ω η : SmoothSample d L) {ε : ℝ} (hε : 0 ≤ ε) :
    dist (sourceFiniteJet d hL K ω) (sourceFiniteJet d hL K η) ≤ ε ↔
      ∀ j : Fin (K+1), ∀ x : Fin d → ℝ,
        dist (iteratedFDeriv ℝ j (smoothSourceField d L ω) x)
          (iteratedFDeriv ℝ j (smoothSourceField d L η) x) ≤ ε := by
  rw [dist_pi_le_iff hε]
  apply forall_congr'
  intro j
  rw [BoundedContinuousFunction.dist_le hε]
  simp only [sourceFiniteJet, sourceDerivativeBCF_apply]

/-- The zeroth component recovers the actual global field; no value-only
claim on arbitrary compact subsets is used. -/
theorem sourceFiniteJet_eq_iff_field_eq (d : ℕ) {L : ℝ} (hL : L ≠ 0) (K : ℕ)
    (ω η : SmoothSample d L) :
    sourceFiniteJet d hL K ω = sourceFiniteJet d hL K η ↔
      smoothSourceField d L ω = smoothSourceField d L η := by
  constructor
  · intro h
    funext x
    have h0 := congrFun h (0 : Fin (K+1))
    have hx := congrArg (fun v : DerivativeBCF d 0 => v x (fun a => Fin.elim0 a)) h0
    change (sourceDerivativeBCF d hL 0 ω x) (fun a => Fin.elim0 a) =
      (sourceDerivativeBCF d hL 0 η x) (fun a => Fin.elim0 a) at hx
    simpa only [sourceDerivativeBCF_apply, iteratedFDeriv_zero_apply] using hx
  · intro h
    funext j
    apply BoundedContinuousFunction.ext
    intro x
    change sourceDerivativeBCF d hL j ω x = sourceDerivativeBCF d hL j η x
    rw [sourceDerivativeBCF_apply, sourceDerivativeBCF_apply, h]

theorem smoothSourceField_lattice_periodic (d : ℕ) {L : ℝ} (hL : L ≠ 0)
    (ω : SmoothSample d L) (n : Fin d → ℤ) (x : Fin d → ℝ) :
    smoothSourceField d L ω (x + fun a => L*(n a : ℝ)) = smoothSourceField d L ω x :=
  I4Lattice.sourceField_lattice_shift d hL ω.val n x

theorem sourceDerivativeBCF_lattice_periodic (d : ℕ) {L : ℝ} (hL : L ≠ 0) (k : ℕ)
    (ω : SmoothSample d L) (n : Fin d → ℤ) (x : Fin d → ℝ) :
    sourceDerivativeBCF d hL k ω (x + fun a => L*(n a : ℝ)) = sourceDerivativeBCF d hL k ω x := by
  rw [sourceDerivativeBCF_apply, sourceDerivativeBCF_apply, ← iteratedFDeriv_comp_add_right]
  have h : (fun z => smoothSourceField d L ω (z + fun a => L*(n a : ℝ))) =
      smoothSourceField d L ω := funext (smoothSourceField_lattice_periodic d hL ω n)
  rw [h]

/-- Compatible periodic jets are required to come from one actual C^K field.
Periodicity and derivative compatibility are properties, not law premises. -/
def compatiblePeriodicJets (d : ℕ) (L : ℝ) (K : ℕ) :
    Set ((j : Fin (K+1)) → DerivativeBCF d j) :=
  {v | ∃ f : (Fin d → ℝ) → ℝ, ContDiff ℝ K f ∧
    (∀ n : Fin d → ℤ, ∀ x, f (x + fun a => L*(n a : ℝ)) = f x) ∧
    ∀ j : Fin (K+1), ∀ x, v j x = iteratedFDeriv ℝ j f x}

theorem sourceFiniteJet_mem_compatible (d : ℕ) {L : ℝ} (hL : L ≠ 0) (K : ℕ)
    (ω : SmoothSample d L) : sourceFiniteJet d hL K ω ∈ compatiblePeriodicJets d L K := by
  refine ⟨smoothSourceField d L ω,smoothSourceField_contDiff d hL ω K,?_,?_⟩
  · exact smoothSourceField_lattice_periodic d hL ω
  · intro j x
    exact sourceDerivativeBCF_apply d hL j ω x

/-- Global compatible jets have a unique underlying field. This statement
does not concern value restrictions to a compact set with empty interior. -/
theorem compatiblePeriodicJets_witness_unique (d : ℕ) (L : ℝ) (K : ℕ)
    (v : (j : Fin (K+1)) → DerivativeBCF d j) (hv : v ∈ compatiblePeriodicJets d L K) :
    ∃! f : (Fin d → ℝ) → ℝ, ContDiff ℝ K f ∧
      (∀ n : Fin d → ℤ, ∀ x, f (x + fun a => L*(n a : ℝ)) = f x) ∧
      ∀ j : Fin (K+1), ∀ x, v j x = iteratedFDeriv ℝ j f x := by
  obtain ⟨f,hf,hper,hjet⟩ := hv
  refine ⟨f,⟨hf,hper,hjet⟩,?_⟩
  intro g hg
  funext x
  have heq : iteratedFDeriv ℝ 0 g x = iteratedFDeriv ℝ 0 f x :=
    (hg.2.2 (0 : Fin (K+1)) x).symm.trans (hjet (0 : Fin (K+1)) x)
  have h := congrArg (fun A : DerivativeOperator d 0 => A (fun a => Fin.elim0 a)) heq
  simpa only [iteratedFDeriv_zero_apply] using h

end I4SourceSmoothTopology

open I4SourceSmoothConditional I4SourceEndpointRegression ProbabilityTheory

namespace I4SourceSmoothTopology

/- These local structures are explicitly the norm-topology Borel structures.
They are closed into the conditional-law statements below. -/
section NormBorel

local instance derivativeMeasurableSpace (d k : ℕ) : MeasurableSpace (DerivativeBCF d k) := borel _
local instance derivativeBorelSpace (d k : ℕ) : BorelSpace (DerivativeBCF d k) := ⟨rfl⟩

local instance (priority := 2000) finiteJetMeasurableSpace (d K : ℕ) :
    MeasurableSpace ((j : Fin (K+1)) → DerivativeBCF d j) := borel _
local instance (priority := 2000) finiteJetBorelSpace (d K : ℕ) :
    BorelSpace ((j : Fin (K+1)) → DerivativeBCF d j) := ⟨rfl⟩

def sourceCompatibleJet (d : ℕ) {L : ℝ} (hL : L ≠ 0) (K : ℕ) (ω : SmoothSample d L) :
    compatiblePeriodicJets d L K :=
  ⟨sourceFiniteJet d hL K ω,sourceFiniteJet_mem_compatible d hL K ω⟩

theorem sourceCompatibleJet_measurable (d : ℕ) {L : ℝ} (hL : L ≠ 0) (K : ℕ) :
    Measurable (sourceCompatibleJet d hL K) :=
  (sourceFiniteJet_borel d hL K).subtype_mk

theorem sourceCompatibleJet_borel (d : ℕ) {L : ℝ} (hL : L ≠ 0) (K : ℕ) :
    @Measurable (SmoothSample d L) (compatiblePeriodicJets d L K) _ (borel _)
      (sourceCompatibleJet d hL K) := by
  rw [← BorelSpace.measurable_eq (α := compatiblePeriodicJets d L K)]
  exact sourceCompatibleJet_measurable d hL K

/-- This is HasCondDistrib in the Borel structure of the BCF norm. -/
theorem sourceDerivativeBCF_hasCondDistrib {L : ℝ} (hL : L ≠ 0) (r : ℝ)
    (hG : IsUnit (sourcePinCovarianceAt L r)) (k : ℕ) :
    HasCondDistrib (sourceDerivativeBCF 2 hL k) (sourceConfluentPinsAt L r)
      ((sourceSmoothKernel hL r).map (sourceDerivativeBCF 2 hL k)) (smoothLaw 2 L) :=
  sourceSmoothKernel_map_hasCondDistrib hL r hG _ (sourceDerivativeBCF_borel 2 hL k)

/-- The whole jet tuple uses its norm Borel structure, not a coordinate-product surrogate. -/
theorem sourceFiniteJet_hasCondDistrib {L : ℝ} (hL : L ≠ 0) (r : ℝ)
    (hG : IsUnit (sourcePinCovarianceAt L r)) (K : ℕ) :
    HasCondDistrib (sourceFiniteJet 2 hL K) (sourceConfluentPinsAt L r)
      ((sourceSmoothKernel hL r).map (sourceFiniteJet 2 hL K)) (smoothLaw 2 L) :=
  sourceSmoothKernel_map_hasCondDistrib hL r hG _ (sourceFiniteJet_borel 2 hL K)

theorem sourceCompatibleJet_hasCondDistrib {L : ℝ} (hL : L ≠ 0) (r : ℝ)
    (hG : IsUnit (sourcePinCovarianceAt L r)) (K : ℕ) :
    HasCondDistrib (sourceCompatibleJet 2 hL K) (sourceConfluentPinsAt L r)
      ((sourceSmoothKernel hL r).map (sourceCompatibleJet 2 hL K)) (smoothLaw 2 L) :=
  sourceSmoothKernel_map_hasCondDistrib hL r hG _ (sourceCompatibleJet_measurable 2 hL K)

theorem sourceFiniteJet_functional_hasCondDistrib {L : ℝ} (hL : L ≠ 0) (r : ℝ)
    (hG : IsUnit (sourcePinCovarianceAt L r)) (K : ℕ) {E : Type*} [MeasurableSpace E]
    (F : ((j : Fin (K+1)) → DerivativeBCF 2 j) → E) (hF : Measurable F) :
    HasCondDistrib (F ∘ sourceFiniteJet 2 hL K) (sourceConfluentPinsAt L r)
      ((sourceSmoothKernel hL r).map (F ∘ sourceFiniteJet 2 hL K)) (smoothLaw 2 L) :=
  sourceSmoothKernel_map_hasCondDistrib hL r hG _ (hF.comp (sourceFiniteJet_borel 2 hL K))

theorem sourceDerivativeBCF_functional_hasCondDistrib {L : ℝ} (hL : L ≠ 0) (r : ℝ)
    (hG : IsUnit (sourcePinCovarianceAt L r)) (k : ℕ) {E : Type*} [MeasurableSpace E]
    (F : DerivativeBCF 2 k → E) (hF : Measurable F) :
    HasCondDistrib (F ∘ sourceDerivativeBCF 2 hL k) (sourceConfluentPinsAt L r)
      ((sourceSmoothKernel hL r).map (F ∘ sourceDerivativeBCF 2 hL k)) (smoothLaw 2 L) :=
  sourceSmoothKernel_map_hasCondDistrib hL r hG _ (hF.comp (sourceDerivativeBCF_borel 2 hL k))

theorem sourceCompatibleJet_functional_hasCondDistrib {L : ℝ} (hL : L ≠ 0) (r : ℝ)
    (hG : IsUnit (sourcePinCovarianceAt L r)) (K : ℕ) {E : Type*} [MeasurableSpace E]
    (F : compatiblePeriodicJets 2 L K → E) (hF : Measurable F) :
    HasCondDistrib (F ∘ sourceCompatibleJet 2 hL K) (sourceConfluentPinsAt L r)
      ((sourceSmoothKernel hL r).map (F ∘ sourceCompatibleJet 2 hL K)) (smoothLaw 2 L) :=
  sourceSmoothKernel_map_hasCondDistrib hL r hG _ (hF.comp (sourceCompatibleJet_measurable 2 hL K))

theorem sourceDerivativeBCF_eventually_hasCondDistrib {L : ℝ} (hL : L ≠ 0) (k : ℕ) :
    ∀ᶠ r in 𝓝[>] (0 : ℝ),
      HasCondDistrib (sourceDerivativeBCF 2 hL k) (sourceConfluentPinsAt L r)
        ((sourceSmoothKernel hL r).map (sourceDerivativeBCF 2 hL k)) (smoothLaw 2 L) :=
  sourceSmoothKernel_eventually_map_hasCondDistrib hL _ (sourceDerivativeBCF_borel 2 hL k)

theorem sourceFiniteJet_eventually_hasCondDistrib {L : ℝ} (hL : L ≠ 0) (K : ℕ) :
    ∀ᶠ r in 𝓝[>] (0 : ℝ),
      HasCondDistrib (sourceFiniteJet 2 hL K) (sourceConfluentPinsAt L r)
        ((sourceSmoothKernel hL r).map (sourceFiniteJet 2 hL K)) (smoothLaw 2 L) :=
  sourceSmoothKernel_eventually_map_hasCondDistrib hL _ (sourceFiniteJet_borel 2 hL K)

theorem sourceCompatibleJet_eventually_hasCondDistrib {L : ℝ} (hL : L ≠ 0) (K : ℕ) :
    ∀ᶠ r in 𝓝[>] (0 : ℝ),
      HasCondDistrib (sourceCompatibleJet 2 hL K) (sourceConfluentPinsAt L r)
        ((sourceSmoothKernel hL r).map (sourceCompatibleJet 2 hL K)) (smoothLaw 2 L) :=
  sourceSmoothKernel_eventually_map_hasCondDistrib hL _ (sourceCompatibleJet_measurable 2 hL K)

theorem sourceFiniteJet_functional_eventually_hasCondDistrib {L : ℝ} (hL : L ≠ 0) (K : ℕ)
    {E : Type*} [MeasurableSpace E] (F : ((j : Fin (K+1)) → DerivativeBCF 2 j) → E)
    (hF : Measurable F) :
    ∀ᶠ r in 𝓝[>] (0 : ℝ),
      HasCondDistrib (F ∘ sourceFiniteJet 2 hL K) (sourceConfluentPinsAt L r)
        ((sourceSmoothKernel hL r).map (F ∘ sourceFiniteJet 2 hL K)) (smoothLaw 2 L) :=
  sourceSmoothKernel_eventually_map_hasCondDistrib hL _ (hF.comp (sourceFiniteJet_borel 2 hL K))

theorem sourceDerivativeBCF_functional_eventually_hasCondDistrib {L : ℝ} (hL : L ≠ 0) (k : ℕ)
    {E : Type*} [MeasurableSpace E] (F : DerivativeBCF 2 k → E) (hF : Measurable F) :
    ∀ᶠ r in 𝓝[>] (0 : ℝ),
      HasCondDistrib (F ∘ sourceDerivativeBCF 2 hL k) (sourceConfluentPinsAt L r)
        ((sourceSmoothKernel hL r).map (F ∘ sourceDerivativeBCF 2 hL k)) (smoothLaw 2 L) :=
  sourceSmoothKernel_eventually_map_hasCondDistrib hL _ (hF.comp (sourceDerivativeBCF_borel 2 hL k))

theorem sourceCompatibleJet_functional_eventually_hasCondDistrib {L : ℝ} (hL : L ≠ 0) (K : ℕ)
    {E : Type*} [MeasurableSpace E] (F : compatiblePeriodicJets 2 L K → E) (hF : Measurable F) :
    ∀ᶠ r in 𝓝[>] (0 : ℝ),
      HasCondDistrib (F ∘ sourceCompatibleJet 2 hL K) (sourceConfluentPinsAt L r)
        ((sourceSmoothKernel hL r).map (F ∘ sourceCompatibleJet 2 hL K)) (smoothLaw 2 L) :=
  sourceSmoothKernel_eventually_map_hasCondDistrib hL _ (hF.comp (sourceCompatibleJet_measurable 2 hL K))

end NormBorel

end I4SourceSmoothTopology
