import SourceSmoothTopology
import SourcePinCurvatureBounds
import SourcePinPreservingQuartic
import Mathlib.Analysis.Normed.Lp.lpHolder
import Mathlib.Topology.Algebra.Module.Basic
import Mathlib.Topology.MetricSpace.Polish

/-!
# A weighted ℓ1 parameter family for the actual smooth source

The actual all-order smooth carrier maps measurably into a separable Banach
parameter space. Every arbitrary parameter synthesizes a genuine C5 field,
with a continuous linear whole finite jet map. These facts do not assert
measurability of selector, flow, hitting, or capture events; that application
remains an explicit further theorem in SOURCE_SMOOTH_PARAMETER_SPACE.md.
-/

noncomputable section
open I4Foundation I4Source I4Smooth I4SmoothCarrier I4SourceSmoothTopology
open I4SourceConditionalMajorant I4SourcePinCurvatureBounds
open I4SourceEndpointRegression I4SourceSmoothConditional I4SourcePinPreservingQuartic
open MeasureTheory ProbabilityTheory Filter BoundedContinuousFunction TopologicalSpace
open scoped BigOperators Topology lp ENNReal

set_option autoImplicit false

namespace I4SourceSmoothParameterSpace

def parameterWeight (L : ℝ) (m : SourceMode 2) : ℝ :=
  ∑ k : Fin 6, orderModeBound k 2 L m

abbrev SmoothParameter : Type := ℓ¹(SourceMode 2, ℝ)

theorem parameterWeight_nonneg (L : ℝ) (m : SourceMode 2) : 0 ≤ parameterWeight L m :=
  Finset.sum_nonneg (fun k _ => orderModeBound_nonneg k 2 L m)

theorem parameterWeight_mul_abs_summable (L : ℝ) (ω : SmoothSample 2 L) :
    Summable (fun m => parameterWeight L m * |ω.val m|) := by
  have h := summable_sum (fun k (_ : k ∈ (Finset.univ : Finset (Fin 6))) => ω.property k)
  simpa only [parameterWeight, Finset.sum_mul] using h

theorem weightedCarrier_memℓp (L : ℝ) (ω : SmoothSample 2 L) :
    Memℓp (fun m => parameterWeight L m * ω.val m) 1 := by
  apply memℓp_gen
  simpa only [ENNReal.toReal_one, Real.rpow_one, Real.norm_eq_abs, abs_mul,
    abs_of_nonneg (parameterWeight_nonneg L _)] using parameterWeight_mul_abs_summable L ω

def weightedCarrier (L : ℝ) (ω : SmoothSample 2 L) : SmoothParameter :=
  ⟨fun m => parameterWeight L m * ω.val m, weightedCarrier_memℓp L ω⟩

@[simp] theorem weightedCarrier_apply (L : ℝ) (ω : SmoothSample 2 L) (m : SourceMode 2) :
    weightedCarrier L ω m = parameterWeight L m * ω.val m := rfl

theorem weightedCarrier_norm (L : ℝ) (ω : SmoothSample 2 L) :
    ‖weightedCarrier L ω‖ = ∑ k : Fin 6, sourceDerivativeMajorant L k ω := by
  rw [lp.norm_eq_tsum_rpow (by norm_num : (0 : ℝ) < (1 : ℝ≥0∞).toReal)]
  simp only [ENNReal.toReal_one, Real.rpow_one, div_one, weightedCarrier_apply,
    Real.norm_eq_abs, abs_mul, abs_of_nonneg (parameterWeight_nonneg L _)]
  simp only [parameterWeight, Finset.sum_mul, sourceDerivativeMajorant, sampleMajorant]
  exact Summable.tsum_finsetSum (fun k _ => ω.property k)

theorem weightedCarrier_norm_eq_radius_sub_one (L : ℝ) (ω : SmoothSample 2 L) :
    ‖weightedCarrier L ω‖ = sourceGammaRadius L ω - 1 := by
  rw [weightedCarrier_norm]
  simp [sourceGammaRadius]

theorem weightedCarrier_stronglyMeasurable (L : ℝ) : StronglyMeasurable (weightedCarrier L) := by
  apply stronglyMeasurable_of_countable_hasSum
    (fun m (ω : SmoothSample 2 L) => lp.single (1 : ℝ≥0∞) m (parameterWeight L m * ω.val m))
  · intro m
    exact (lp.singleContinuousLinearMap ℝ (fun _ : SourceMode 2 => ℝ) 1 m).continuous.comp_stronglyMeasurable
      ((((measurable_pi_apply m).comp measurable_subtype_coe).const_mul _).stronglyMeasurable)
  · intro ω
    exact lp.hasSum_single (by simp) (weightedCarrier L ω)

theorem weightedCarrier_borel (L : ℝ) :
    @Measurable (SmoothSample 2 L) SmoothParameter _ (borel _) (weightedCarrier L) := by
  borelize SmoothParameter
  exact (weightedCarrier_stronglyMeasurable L).measurable

theorem smoothParameter_complete : CompleteSpace SmoothParameter := inferInstance

/-- The finite coordinate vectors span a dense separable subspace in the lp norm. -/
theorem smoothParameter_separable : SeparableSpace SmoothParameter := by
  let S : Set SmoothParameter := Set.range (fun m : SourceMode 2 => lp.single 1 m (1 : ℝ))
  have hS : IsSeparable S := (Set.countable_range _).isSeparable
  have hspan : IsSeparable (Submodule.span ℝ S : Set SmoothParameter) := hS.span
  have hdense : Dense (Submodule.span ℝ S : Set SmoothParameter) := by
    intro f
    apply mem_closure_of_tendsto (lp.hasSum_single (by simp) f)
    apply Filter.Eventually.of_forall
    intro s
    apply Submodule.sum_mem
    intro m _
    have hm : lp.single 1 m (1 : ℝ) ∈ Submodule.span ℝ S :=
      Submodule.subset_span (Set.mem_range_self m)
    have hs := (Submodule.span ℝ S).smul_mem (f m) hm
    simpa only [← lp.single_smul, smul_eq_mul, mul_one] using hs
  exact hdense.isSeparable_iff.mp hspan

theorem smoothParameter_polish : PolishSpace SmoothParameter := by
  have := smoothParameter_separable
  infer_instance



theorem parameterWeight_pos {L : ℝ} (hL : L ≠ 0) (m : SourceMode 2) :
    0 < parameterWeight L m := by
  have h0 : 0 < orderModeBound 0 2 L m := by
    have hz := I4Weights.sourceZ_pos 2 hL
    cases m with
    | none =>
      change 0 < Real.sqrt (1 / I4Weights.sourceZ 2 L)
      positivity
    | some p =>
      unfold orderModeBound orderPairedBound orderProductBound orderCoordinateBound I4Weights.decay
      positivity
  exact h0.trans_le (Finset.single_le_sum (fun k (_ : k ∈ (Finset.univ : Finset (Fin 6))) =>
    orderModeBound_nonneg k 2 L m) (Finset.mem_univ (0 : Fin 6)))

theorem parameterWeight_dominates (L : ℝ) (k : ℕ) (hk : k ≤ 5) (m : SourceMode 2) :
    orderModeBound k 2 L m ≤ parameterWeight L m := by
  have hk6 : k < 6 := by omega
  exact Finset.single_le_sum (fun j (_ : j ∈ (Finset.univ : Finset (Fin 6))) =>
    orderModeBound_nonneg j 2 L m) (Finset.mem_univ (⟨k,hk6⟩ : Fin 6))

theorem parameter_abs_summable (a : SmoothParameter) : Summable (fun m => |a m|) := by
  simpa using (lp.memℓp a).summable

def weightedFourierField (L : ℝ) (w : SourceMode 2 → ℝ) (a : SmoothParameter)
    (x : Fin 2 → ℝ) : ℝ := ∑' m, (a m / w m) * modeCoefficient 2 L m x

theorem weighted_mode_derivative_bound {L : ℝ} (hL : L ≠ 0)
    (w : SourceMode 2 → ℝ) (hw : ∀ m, 0 < w m)
    (hdom : ∀ k ≤ 5, ∀ m, orderModeBound k 2 L m ≤ w m)
    (a : SmoothParameter) (k : ℕ) (hk : k ≤ 5) (m : SourceMode 2) (x : Fin 2 → ℝ) :
    ‖iteratedFDeriv ℝ k (fun y => (a m / w m) * modeCoefficient 2 L m y) x‖ ≤ |a m| := by
  have heq : (fun y => (a m / w m) * modeCoefficient 2 L m y) =
      (a m / w m) • modeCoefficient 2 L m := by
    ext y
    simp only [Pi.smul_apply,smul_eq_mul]
  rw [heq,iteratedFDeriv_const_smul_apply (modeCoefficient_contDiff 2 L m k).contDiffAt,
    norm_smul,Real.norm_eq_abs,abs_div,abs_of_pos (hw m)]
  calc
    _ ≤ (|a m| / w m) * w m := mul_le_mul_of_nonneg_left
      ((modeCoefficient_iteratedFDeriv_order_bound 2 hL m k x).trans (hdom k hk m))
      (div_nonneg (abs_nonneg _) (hw m).le)
    _ = |a m| := div_mul_cancel₀ _ (hw m).ne'

/-- Arbitrary parameters have genuine C5 fields; no all-order smooth carrier
property is inferred or assumed. -/
theorem weightedFourierField_contDiff {L : ℝ} (hL : L ≠ 0)
    (w : SourceMode 2 → ℝ) (hw : ∀ m, 0 < w m)
    (hdom : ∀ k ≤ 5, ∀ m, orderModeBound k 2 L m ≤ w m) (a : SmoothParameter) :
    ContDiff ℝ 5 (weightedFourierField L w a) := by
  apply contDiff_tsum (v := fun _ m => |a m|)
  · intro m
    exact contDiff_const.mul (modeCoefficient_contDiff 2 L m 5)
  · intro _ _
    exact parameter_abs_summable a
  · intro k m x hk
    have hk' : k ≤ 5 := by exact_mod_cast hk
    exact weighted_mode_derivative_bound hL w hw hdom a k hk' m x

theorem weightedFourierField_derivative {L : ℝ} (hL : L ≠ 0)
    (w : SourceMode 2 → ℝ) (hw : ∀ m, 0 < w m)
    (hdom : ∀ k ≤ 5, ∀ m, orderModeBound k 2 L m ≤ w m)
    (a : SmoothParameter) (k : ℕ) (hk : k ≤ 5) (x : Fin 2 → ℝ) :
    iteratedFDeriv ℝ k (weightedFourierField L w a) x =
      ∑' m, (a m / w m) • iteratedFDeriv ℝ k (modeCoefficient 2 L m) x := by
  have hf (m : SourceMode 2) :
      ContDiff ℝ (5 : ℕ∞) (fun y => (a m / w m) * modeCoefficient 2 L m y) :=
    contDiff_const.mul (modeCoefficient_contDiff 2 L m 5)
  have hmajor (j : ℕ) (_ : (j : ℕ∞) ≤ 5) : Summable (fun m => |a m|) :=
    parameter_abs_summable a
  have hbound (j : ℕ) (m : SourceMode 2) (y : Fin 2 → ℝ) (hj : (j : ℕ∞) ≤ 5) :
      ‖iteratedFDeriv ℝ j (fun z => (a m / w m) * modeCoefficient 2 L m z) y‖ ≤ |a m| :=
    weighted_mode_derivative_bound hL w hw hdom a j (by exact_mod_cast hj) m y
  have hd := iteratedFDeriv_tsum_apply hf hmajor hbound (k := k) (by exact_mod_cast hk) x
  change iteratedFDeriv ℝ k (fun y => ∑' m, (a m / w m) * modeCoefficient 2 L m y) x = _
  rw [hd]
  apply tsum_congr
  intro m
  have heq : (fun y => (a m / w m) * modeCoefficient 2 L m y) =
      (a m / w m) • modeCoefficient 2 L m := by ext y; simp
  rw [heq,iteratedFDeriv_const_smul_apply (modeCoefficient_contDiff 2 L m k).contDiffAt]

def l1Synthesis {I F : Type*} [NormedAddCommGroup F] [NormedSpace ℝ F] [CompleteSpace F]
    (b : I → F) (hb : ∀ i, ‖b i‖ ≤ 1) : ℓ¹(I, ℝ) →L[ℝ] F :=
  (lp.tsumCLM ℝ I F).comp (lp.mapCLM 1
    (fun i => (ContinuousLinearMap.id ℝ ℝ).smulRight (b i)) zero_le_one (fun i => by
      apply ContinuousLinearMap.opNorm_le_bound _ zero_le_one
      intro c
      simpa [norm_smul] using mul_le_mul_of_nonneg_left (hb i) (norm_nonneg c)))

theorem l1Synthesis_norm_le {I F : Type*} [NormedAddCommGroup F] [NormedSpace ℝ F]
    [CompleteSpace F] (b : I → F) (hb : ∀ i, ‖b i‖ ≤ 1) : ‖l1Synthesis b hb‖ ≤ 1 := by
  apply (ContinuousLinearMap.opNorm_comp_le _ _).trans
  calc
    _ ≤ 1 * 1 := mul_le_mul (lp.norm_tsumCLM_le) (lp.norm_mapCLM_le 1 _ _ _)
      (norm_nonneg _) zero_le_one
    _ = _ := by ring

theorem l1Synthesis_apply {I F : Type*} [NormedAddCommGroup F] [NormedSpace ℝ F]
    [CompleteSpace F] (b : I → F) (hb : ∀ i, ‖b i‖ ≤ 1) (a : ℓ¹(I, ℝ)) :
    l1Synthesis b hb a = ∑' i, a i • b i := rfl

theorem l1Synthesis_summable {I F : Type*} [NormedAddCommGroup F] [NormedSpace ℝ F]
    [CompleteSpace F] (b : I → F) (hb : ∀ i, ‖b i‖ ≤ 1) (a : ℓ¹(I, ℝ)) :
    Summable (fun i => a i • b i) := by
  apply Summable.of_norm_bounded (show Summable (fun i => |a i|) by
    simpa using (lp.memℓp a).summable)
  intro i
  rw [norm_smul,Real.norm_eq_abs]
  simpa using mul_le_mul_of_nonneg_left (hb i) (abs_nonneg (a i))

/- Pin inherited normed structures while forming operator norms. The direct
BCF additive/module instances otherwise choose a different structure path. -/
local instance coherentBCFSemi (d k : ℕ) : SeminormedAddCommGroup (DerivativeBCF d k) :=
  (inferInstance : NormedAddCommGroup (DerivativeBCF d k)).toSeminormedAddCommGroup
local instance coherentBCFAdd (d k : ℕ) : AddCommMonoid (DerivativeBCF d k) :=
  (coherentBCFSemi d k).toAddCommMonoid
local instance coherentBCFModule (d k : ℕ) : Module ℝ (DerivativeBCF d k) :=
  (inferInstance : NormedSpace ℝ (DerivativeBCF d k)).toModule

local instance coherentJetSemi (K : ℕ) :
    SeminormedAddCommGroup ((k : Fin (K+1)) → DerivativeBCF 2 k) :=
  (inferInstance : NormedAddCommGroup ((k : Fin (K+1)) → DerivativeBCF 2 k)).toSeminormedAddCommGroup
local instance coherentJetAdd (K : ℕ) : AddCommMonoid ((k : Fin (K+1)) → DerivativeBCF 2 k) :=
  (coherentJetSemi K).toAddCommMonoid
local instance coherentJetModule (K : ℕ) : Module ℝ ((k : Fin (K+1)) → DerivativeBCF 2 k) :=
  (inferInstance : NormedSpace ℝ ((k : Fin (K+1)) → DerivativeBCF 2 k)).toModule

def normalizedModeDerivative {L : ℝ} (hL : L ≠ 0) (k : ℕ) (m : SourceMode 2) :
    DerivativeBCF 2 k := (parameterWeight L m)⁻¹ • modeDerivativeBCF 2 hL k m

theorem normalizedModeDerivative_norm_le {L : ℝ} (hL : L ≠ 0)
    (k : ℕ) (hk : k ≤ 5) (m : SourceMode 2) :
    ‖normalizedModeDerivative hL k m‖ ≤ 1 := by
  apply (BoundedContinuousFunction.norm_le zero_le_one).2
  intro x
  change ‖(parameterWeight L m)⁻¹ • iteratedFDeriv ℝ k (modeCoefficient 2 L m) x‖ ≤ 1
  rw [norm_smul,Real.norm_eq_abs,abs_inv,abs_of_pos (parameterWeight_pos hL m)]
  calc
    _ ≤ (parameterWeight L m)⁻¹ * parameterWeight L m := mul_le_mul_of_nonneg_left
      ((modeCoefficient_iteratedFDeriv_order_bound 2 hL m k x).trans
        (parameterWeight_dominates L k hk m)) (inv_nonneg.mpr (parameterWeight_pos hL m).le)
    _ = 1 := inv_mul_cancel₀ (parameterWeight_pos hL m).ne'

def parameterDerivativeCLM {L : ℝ} (hL : L ≠ 0) (k : ℕ) (hk : k ≤ 5) :
    SmoothParameter →L[ℝ] DerivativeBCF 2 k :=
  l1Synthesis (normalizedModeDerivative hL k) (normalizedModeDerivative_norm_le hL k hk)

theorem parameterDerivativeCLM_norm_le {L : ℝ} (hL : L ≠ 0) (k : ℕ) (hk : k ≤ 5) :
    ‖parameterDerivativeCLM hL k hk‖ ≤ 1 := l1Synthesis_norm_le _ _

def parameterJetCLM {L : ℝ} (hL : L ≠ 0) :
    SmoothParameter →L[ℝ] ((k : Fin 4) → DerivativeBCF 2 k) :=
  ContinuousLinearMap.pi (fun k : Fin 4 => parameterDerivativeCLM hL k (by omega))

theorem parameterJetCLM_norm_le {L : ℝ} (hL : L ≠ 0) : ‖parameterJetCLM hL‖ ≤ 1 := by
  apply ContinuousLinearMap.opNorm_le_bound _ zero_le_one
  intro a
  simp only [one_mul]
  apply (pi_norm_le_iff_of_nonneg (norm_nonneg a)).2
  intro k
  exact (parameterDerivativeCLM hL k (by omega)).le_of_opNorm_le
    (parameterDerivativeCLM_norm_le hL k (by omega)) a |>.trans_eq (one_mul _)

theorem parameterJet_continuous {L : ℝ} (hL : L ≠ 0) :
    Continuous (fun a : SmoothParameter => (parameterJetCLM hL a : (k : Fin 4) → DerivativeBCF 2 k)) :=
  (parameterJetCLM hL).continuous

theorem parameterDerivativeCLM_apply {L : ℝ} (hL : L ≠ 0)
    (k : ℕ) (hk : k ≤ 5) (a : SmoothParameter) (x : Fin 2 → ℝ) :
    parameterDerivativeCLM hL k hk a x =
      iteratedFDeriv ℝ k (weightedFourierField L (parameterWeight L) a) x := by
  have hs := l1Synthesis_summable (normalizedModeDerivative hL k)
    (normalizedModeDerivative_norm_le hL k hk) a
  have hx := hs.hasSum.map (BoundedContinuousFunction.evalCLM ℝ x).toAddMonoidHom
    (BoundedContinuousFunction.evalCLM ℝ x).continuous
  change HasSum (fun m => a m • ((parameterWeight L m)⁻¹ •
    iteratedFDeriv ℝ k (modeCoefficient 2 L m) x)) (parameterDerivativeCLM hL k hk a x) at hx
  rw [← hx.tsum_eq,weightedFourierField_derivative hL _ (parameterWeight_pos hL)
    (parameterWeight_dominates L) a k hk]
  apply tsum_congr
  intro m
  rw [smul_smul,div_eq_mul_inv]

theorem actual_parameter_field_eq {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) :
    weightedFourierField L (parameterWeight L) (weightedCarrier L ω) = smoothSourceField 2 L ω := by
  ext x
  unfold weightedFourierField smoothSourceField sourceField
  apply tsum_congr
  intro m
  rw [weightedCarrier_apply]
  have hw := (parameterWeight_pos hL m).ne'
  simp [sampleInclusion,hw,mul_comm]

theorem actual_parameter_jet_eq {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) :
    parameterJetCLM hL (weightedCarrier L ω) = sourceFiniteJet 2 hL 3 ω := by
  ext k x u
  change parameterDerivativeCLM hL k (by omega) (weightedCarrier L ω) x u = _
  rw [parameterDerivativeCLM_apply,actual_parameter_field_eq hL ω]
  exact congrArg (fun A : DerivativeOperator 2 k => A u)
    (sourceDerivativeBCF_apply 2 hL k ω x).symm

theorem weightedFourierField_periodic {L : ℝ} (hL : L ≠ 0) (w : SourceMode 2 → ℝ)
    (a : SmoothParameter) (n : Fin 2 → ℤ) (x : Fin 2 → ℝ) :
    weightedFourierField L w a (x + fun i => L * (n i : ℝ)) = weightedFourierField L w a x := by
  have heq : weightedFourierField L w a = sourceField 2 L (fun m => a m / w m) := by
    ext y
    apply tsum_congr
    intro m
    exact mul_comm _ _
  rw [heq]
  exact I4Lattice.sourceField_lattice_shift 2 hL _ n x

/-- The actual normalized finite-regularity family on the Banach parameter. -/
def parameterField (L : ℝ) (a : SmoothParameter) : (Fin 2 → ℝ) → ℝ :=
  weightedFourierField L (parameterWeight L) a

theorem parameterField_contDiff {L : ℝ} (hL : L ≠ 0) (a : SmoothParameter) :
    ContDiff ℝ 5 (parameterField L a) :=
  weightedFourierField_contDiff hL _ (parameterWeight_pos hL) (parameterWeight_dominates L) a

theorem parameterField_derivative {L : ℝ} (hL : L ≠ 0) (k : ℕ) (hk : k ≤ 5)
    (a : SmoothParameter) (x : Fin 2 → ℝ) :
    iteratedFDeriv ℝ k (parameterField L a) x = parameterDerivativeCLM hL k hk a x :=
  (parameterDerivativeCLM_apply hL k hk a x).symm

theorem parameterField_actual {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) :
    parameterField L (weightedCarrier L ω) = smoothSourceField 2 L ω :=
  actual_parameter_field_eq hL ω

theorem parameterField_periodic {L : ℝ} (hL : L ≠ 0) (a : SmoothParameter)
    (n : Fin 2 → ℤ) (x : Fin 2 → ℝ) :
    parameterField L a (x + fun i => L * (n i : ℝ)) = parameterField L a x :=
  weightedFourierField_periodic hL _ a n x

theorem parameterJet_norm_le {L : ℝ} (hL : L ≠ 0) (a : SmoothParameter) :
    ‖parameterJetCLM hL a‖ ≤ ‖a‖ := by
  simpa using (parameterJetCLM hL).le_of_opNorm_le (parameterJetCLM_norm_le hL) a

theorem parameterField_derivative_norm_le {L : ℝ} (hL : L ≠ 0) (k : ℕ) (hk : k ≤ 5)
    (a : SmoothParameter) (x : Fin 2 → ℝ) :
    ‖iteratedFDeriv ℝ k (parameterField L a) x‖ ≤ ‖a‖ := by
  rw [parameterField_derivative hL k hk]
  exact ((parameterDerivativeCLM hL k hk a).norm_coe_le_norm x).trans
    (by simpa using ((parameterDerivativeCLM hL k hk).le_of_opNorm_le
      (parameterDerivativeCLM_norm_le hL k hk) a))


local instance parameterMeasurableSpace : MeasurableSpace SmoothParameter := borel _
local instance parameterBorelSpace : BorelSpace SmoothParameter := ⟨rfl⟩

theorem weightedCarrier_hasCondDistrib {L : ℝ} (hL : L ≠ 0) (r : ℝ)
    (hG : IsUnit (sourcePinCovarianceAt L r)) :
    HasCondDistrib (weightedCarrier L) (sourceConfluentPinsAt L r)
      ((sourceSmoothKernel hL r).map (weightedCarrier L)) (smoothLaw 2 L) :=
  sourceSmoothKernel_map_hasCondDistrib hL r hG _ (weightedCarrier_borel L)

theorem weightedCarrier_functional_hasCondDistrib {L : ℝ} (hL : L ≠ 0) (r : ℝ)
    (hG : IsUnit (sourcePinCovarianceAt L r)) {E : Type*} [MeasurableSpace E]
    (F : SmoothParameter → E) (hF : Measurable F) :
    HasCondDistrib (F ∘ weightedCarrier L) (sourceConfluentPinsAt L r)
      ((sourceSmoothKernel hL r).map (F ∘ weightedCarrier L)) (smoothLaw 2 L) :=
  sourceSmoothKernel_map_hasCondDistrib hL r hG _ (hF.comp (weightedCarrier_borel L))

theorem weightedCarrier_eventually_hasCondDistrib {L : ℝ} (hL : L ≠ 0) :
    ∀ᶠ r in 𝓝[>] (0 : ℝ),
      HasCondDistrib (weightedCarrier L) (sourceConfluentPinsAt L r)
        ((sourceSmoothKernel hL r).map (weightedCarrier L)) (smoothLaw 2 L) :=
  sourceSmoothKernel_eventually_map_hasCondDistrib hL _ (weightedCarrier_borel L)

theorem weightedCarrier_functional_eventually_hasCondDistrib {L : ℝ} (hL : L ≠ 0)
    {E : Type*} [MeasurableSpace E] (F : SmoothParameter → E) (hF : Measurable F) :
    ∀ᶠ r in 𝓝[>] (0 : ℝ),
      HasCondDistrib (F ∘ weightedCarrier L) (sourceConfluentPinsAt L r)
        ((sourceSmoothKernel hL r).map (F ∘ weightedCarrier L)) (smoothLaw 2 L) :=
  sourceSmoothKernel_eventually_map_hasCondDistrib hL _ (hF.comp (weightedCarrier_borel L))



/-- Coordinates of the covector in the fixed flat basis. -/
def coordinateGradientCLM : ((Fin 2 → ℝ) →L[ℝ] ℝ) →L[ℝ] (Fin 2 → ℝ) :=
  ContinuousLinearMap.pi (fun i => ContinuousLinearMap.apply ℝ ℝ (coordinateDirection i))

@[simp] theorem coordinateGradientCLM_apply (A : (Fin 2 → ℝ) →L[ℝ] ℝ) (i : Fin 2) :
    coordinateGradientCLM A i = A (coordinateDirection i) := rfl

/-- Contract the last derivative slot against the coordinate basis. -/
def gradientTensorContraction (k : ℕ) :
    DerivativeOperator 2 (k+1) →L[ℝ]
      ContinuousMultilinearMap ℝ (fun _ : Fin k => Fin 2 → ℝ) (Fin 2 → ℝ) :=
  (ContinuousLinearMap.compContinuousMultilinearMapL ℝ (fun _ : Fin k => Fin 2 → ℝ)
    ((Fin 2 → ℝ) →L[ℝ] ℝ) (Fin 2 → ℝ) coordinateGradientCLM).comp
    (continuousMultilinearCurryRightEquiv' ℝ k (Fin 2 → ℝ) ℝ).toContinuousLinearEquiv.toContinuousLinearMap

@[simp] theorem gradientTensorContraction_apply (k : ℕ)
    (A : DerivativeOperator 2 (k+1)) (u : Fin k → Fin 2 → ℝ) (i : Fin 2) :
    gradientTensorContraction k A u i = A (Fin.snoc u (coordinateDirection i)) := by
  simp [gradientTensorContraction, coordinateGradientCLM]

def parameterGradientTensorBCF {L : ℝ} (hL : L ≠ 0) (k : ℕ) (hk : k ≤ 2)
    (a : SmoothParameter) :=
  (gradientTensorContraction k).compLeftContinuousBounded (Fin 2 → ℝ)
    (parameterDerivativeCLM hL (k+1) (by omega) a)

theorem parameterGradientTensorBCF_continuous {L : ℝ} (hL : L ≠ 0)
    (k : ℕ) (hk : k ≤ 2) : Continuous (parameterGradientTensorBCF hL k hk) :=
  ((gradientTensorContraction k).compLeftContinuousBounded (Fin 2 → ℝ)).continuous.comp
    (parameterDerivativeCLM hL (k+1) (by omega)).continuous

theorem gradientPi_iteratedFDeriv {f : (Fin 2 → ℝ) → ℝ}
    (hf : ContDiff ℝ 5 f) (k : ℕ) (hk : k ≤ 2) (x : Fin 2 → ℝ)
    (u : Fin k → Fin 2 → ℝ) (i : Fin 2) :
    iteratedFDeriv ℝ k (gradientPi f) x u i =
      iteratedFDeriv ℝ (k+1) f x (Fin.snoc u (coordinateDirection i)) := by
  have hd : ContDiff ℝ 4 (fderiv ℝ f) := hf.fderiv_right (by norm_num)
  have heq : gradientPi f = coordinateGradientCLM ∘ fderiv ℝ f := rfl
  rw [heq, coordinateGradientCLM.iteratedFDeriv_comp_left hd.contDiffAt (by exact_mod_cast (show k ≤ 4 by omega))]
  change (iteratedFDeriv ℝ k (fderiv ℝ f) x u) (coordinateDirection i) = _
  rw [iteratedFDeriv_succ_apply_right]
  simp

theorem parameterGradientTensorBCF_apply {L : ℝ} (hL : L ≠ 0)
    (k : ℕ) (hk : k ≤ 2) (a : SmoothParameter) (x : Fin 2 → ℝ) :
    parameterGradientTensorBCF hL k hk a x =
      iteratedFDeriv ℝ k (gradientPi (weightedFourierField L (parameterWeight L) a)) x := by
  ext u i
  change gradientTensorContraction k (parameterDerivativeCLM hL (k+1) (by omega) a x) u i = _
  rw [gradientTensorContraction_apply, parameterDerivativeCLM_apply]
  exact (gradientPi_iteratedFDeriv
    (weightedFourierField_contDiff hL _ (parameterWeight_pos hL) (parameterWeight_dominates L) a)
    k hk x u i).symm

def parameterGradientBCF {L : ℝ} (hL : L ≠ 0) (a : SmoothParameter) :=
  (ContinuousMultilinearMap.apply ℝ (fun _ : Fin 0 => Fin 2 → ℝ) (Fin 2 → ℝ)
    (fun j => Fin.elim0 j)).compLeftContinuousBounded (Fin 2 → ℝ)
    (parameterGradientTensorBCF hL 0 (by omega) a)

theorem parameterGradientBCF_continuous {L : ℝ} (hL : L ≠ 0) :
    Continuous (parameterGradientBCF hL) :=
  ((ContinuousMultilinearMap.apply ℝ (fun _ : Fin 0 => Fin 2 → ℝ) (Fin 2 → ℝ)
    (fun j => Fin.elim0 j)).compLeftContinuousBounded (Fin 2 → ℝ)).continuous.comp
      (parameterGradientTensorBCF_continuous hL 0 (by omega))

@[simp] theorem parameterGradientBCF_apply {L : ℝ} (hL : L ≠ 0)
    (a : SmoothParameter) (x : Fin 2 → ℝ) :
    parameterGradientBCF hL a x = gradientPi (weightedFourierField L (parameterWeight L) a) x := by
  change parameterGradientTensorBCF hL 0 (by omega) a x (fun j => Fin.elim0 j) = _
  rw [parameterGradientTensorBCF_apply, iteratedFDeriv_zero_apply]

def parameterGradientDerivativeBCF {L : ℝ} (hL : L ≠ 0) (a : SmoothParameter) :=
  (continuousMultilinearCurryFin1 ℝ (Fin 2 → ℝ) (Fin 2 → ℝ)).toContinuousLinearEquiv.toContinuousLinearMap.compLeftContinuousBounded
    (Fin 2 → ℝ) (parameterGradientTensorBCF hL 1 (by omega) a)

theorem parameterGradientDerivativeBCF_continuous {L : ℝ} (hL : L ≠ 0) :
    Continuous (parameterGradientDerivativeBCF hL) :=
  ((continuousMultilinearCurryFin1 ℝ (Fin 2 → ℝ) (Fin 2 → ℝ)).toContinuousLinearEquiv.toContinuousLinearMap.compLeftContinuousBounded
    (Fin 2 → ℝ)).continuous.comp (parameterGradientTensorBCF_continuous hL 1 (by omega))

@[simp] theorem parameterGradientDerivativeBCF_apply {L : ℝ} (hL : L ≠ 0)
    (a : SmoothParameter) (x : Fin 2 → ℝ) :
    parameterGradientDerivativeBCF hL a x =
      fderiv ℝ (gradientPi (weightedFourierField L (parameterWeight L) a)) x := by
  ext v i
  change parameterGradientTensorBCF hL 1 (by omega) a x (Fin.snoc 0 v) i = _
  rw [parameterGradientTensorBCF_apply, iteratedFDeriv_one_apply]
  rfl

theorem parameterGradient_spatial_C2 {L : ℝ} (hL : L ≠ 0) (a : SmoothParameter) :
    ContDiff ℝ 2 (gradientPi (weightedFourierField L (parameterWeight L) a)) := by
  have hf := weightedFourierField_contDiff hL _ (parameterWeight_pos hL) (parameterWeight_dominates L) a
  have hd : ContDiff ℝ 4 (fderiv ℝ (weightedFourierField L (parameterWeight L) a)) :=
    hf.fderiv_right (by norm_num)
  exact coordinateGradientCLM.contDiff.comp (hd.of_le (by norm_num))

/-- The physical Euclidean gradient is transported by the fixed continuous
linear equivalence, with its actual Euclidean norm retained. -/
def parameterGradientEuclideanBCF {L : ℝ} (hL : L ≠ 0) (a : SmoothParameter) :=
  piToEuclidean.compLeftContinuousBounded (EuclideanSpace ℝ (Fin 2))
    ((parameterGradientBCF hL a).compContinuous ⟨euclideanToPi,euclideanToPi.continuous⟩)

theorem parameterGradientEuclideanBCF_continuous {L : ℝ} (hL : L ≠ 0) :
    Continuous (parameterGradientEuclideanBCF hL) :=
  (piToEuclidean.compLeftContinuousBounded (EuclideanSpace ℝ (Fin 2))).continuous.comp
    ((BoundedContinuousFunction.compContinuousCLM (Fin 2 → ℝ) ℝ
      ⟨euclideanToPi,euclideanToPi.continuous⟩).continuous.comp
        (parameterGradientBCF_continuous hL))

@[simp] theorem parameterGradientEuclideanBCF_apply {L : ℝ} (hL : L ≠ 0)
    (a : SmoothParameter) (z : EuclideanSpace ℝ (Fin 2)) :
    parameterGradientEuclideanBCF hL a z =
      gradientEuclidean (weightedFourierField L (parameterWeight L) a) z := by
  change piToEuclidean (parameterGradientBCF hL a (euclideanToPi z)) = _
  rw [parameterGradientBCF_apply]
  rfl

theorem parameterGradientEuclidean_spatial_C2 {L : ℝ} (hL : L ≠ 0) (a : SmoothParameter) :
    ContDiff ℝ 2 (gradientEuclidean (weightedFourierField L (parameterWeight L) a)) :=
  piToEuclidean.contDiff.comp ((parameterGradient_spatial_C2 hL a).comp euclideanToPi.contDiff)

/-- The whole local C2 vector-field jet varies continuously in the parameter.
Its components are the literal derivatives of one C2 vector field. -/
def parameterGradientJet {L : ℝ} (hL : L ≠ 0) (a : SmoothParameter) :
    (k : Fin 3) → ((Fin 2 → ℝ) →ᵇ
      ContinuousMultilinearMap ℝ (fun _ : Fin k => Fin 2 → ℝ) (Fin 2 → ℝ)) :=
  fun k => parameterGradientTensorBCF hL k (by omega) a

theorem parameterGradientJet_continuous {L : ℝ} (hL : L ≠ 0) :
    Continuous (parameterGradientJet hL) := by
  apply continuous_pi
  intro k
  exact parameterGradientTensorBCF_continuous hL k (by omega)

theorem parameterGradientJet_apply {L : ℝ} (hL : L ≠ 0) (a : SmoothParameter)
    (k : Fin 3) (x : Fin 2 → ℝ) :
    parameterGradientJet hL a k x = iteratedFDeriv ℝ k (gradientPi (parameterField L a)) x :=
  parameterGradientTensorBCF_apply hL k (by omega) a x

theorem parameterGradient_actual {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L)
    (x : Fin 2 → ℝ) :
    parameterGradientBCF hL (weightedCarrier L ω) x = gradientPi (smoothSourceField 2 L ω) x := by
  rw [parameterGradientBCF_apply,actual_parameter_field_eq hL ω]

theorem parameterGradientDerivative_actual {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L)
    (x : Fin 2 → ℝ) :
    parameterGradientDerivativeBCF hL (weightedCarrier L ω) x =
      fderiv ℝ (gradientPi (smoothSourceField 2 L ω)) x := by
  rw [parameterGradientDerivativeBCF_apply,actual_parameter_field_eq hL ω]

theorem parameterGradientEuclidean_actual {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L)
    (z : EuclideanSpace ℝ (Fin 2)) :
    parameterGradientEuclideanBCF hL (weightedCarrier L ω) z =
      gradientEuclidean (smoothSourceField 2 L ω) z := by
  rw [parameterGradientEuclideanBCF_apply,actual_parameter_field_eq hL ω]

end I4SourceSmoothParameterSpace
