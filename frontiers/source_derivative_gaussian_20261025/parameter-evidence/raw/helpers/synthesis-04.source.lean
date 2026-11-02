import SourceSmoothTopology
import Mathlib.Analysis.Normed.Lp.lpHolder
import WeightedCarrier

noncomputable section
open I4Foundation I4Source I4Smooth I4SmoothCarrier I4SourceSmoothTopology
open MeasureTheory Filter BoundedContinuousFunction TopologicalSpace
open scoped BigOperators Topology lp

set_option autoImplicit false

namespace I4SourceSmoothParameterSpace

abbrev Parameter : Type := ℓ¹(SourceMode 2, ℝ)

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

theorem parameter_abs_summable (a : Parameter) : Summable (fun m => |a m|) := by
  simpa using (lp.memℓp a).summable

def weightedFourierField (L : ℝ) (w : SourceMode 2 → ℝ) (a : Parameter)
    (x : Fin 2 → ℝ) : ℝ := ∑' m, (a m / w m) * modeCoefficient 2 L m x

theorem weighted_mode_derivative_bound {L : ℝ} (hL : L ≠ 0)
    (w : SourceMode 2 → ℝ) (hw : ∀ m, 0 < w m)
    (hdom : ∀ k ≤ 5, ∀ m, orderModeBound k 2 L m ≤ w m)
    (a : Parameter) (k : ℕ) (hk : k ≤ 5) (m : SourceMode 2) (x : Fin 2 → ℝ) :
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
    (hdom : ∀ k ≤ 5, ∀ m, orderModeBound k 2 L m ≤ w m) (a : Parameter) :
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
    (a : Parameter) (k : ℕ) (hk : k ≤ 5) (x : Fin 2 → ℝ) :
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
    Parameter →L[ℝ] DerivativeBCF 2 k :=
  l1Synthesis (normalizedModeDerivative hL k) (normalizedModeDerivative_norm_le hL k hk)

theorem parameterDerivativeCLM_norm_le {L : ℝ} (hL : L ≠ 0) (k : ℕ) (hk : k ≤ 5) :
    ‖parameterDerivativeCLM hL k hk‖ ≤ 1 := l1Synthesis_norm_le _ _

def parameterJetCLM {L : ℝ} (hL : L ≠ 0) :
    Parameter →L[ℝ] ((k : Fin 4) → DerivativeBCF 2 k) :=
  ContinuousLinearMap.pi (fun k => parameterDerivativeCLM hL k (by omega))

theorem parameterJetCLM_norm_le {L : ℝ} (hL : L ≠ 0) : ‖parameterJetCLM hL‖ ≤ 1 := by
  apply ContinuousLinearMap.opNorm_le_bound _ zero_le_one
  intro a
  simp only [one_mul]
  apply (pi_norm_le_iff_of_nonneg (norm_nonneg a)).2
  intro k
  exact (parameterDerivativeCLM hL k (by omega)).le_of_opNorm_le
    (parameterDerivativeCLM_norm_le hL k (by omega)) a |>.trans_eq (one_mul _)

theorem parameterDerivativeCLM_apply {L : ℝ} (hL : L ≠ 0)
    (k : ℕ) (hk : k ≤ 5) (a : Parameter) (x : Fin 2 → ℝ) :
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
  rw [parameterDerivativeCLM_apply,actual_parameter_field_eq]
  exact congrArg (fun A : DerivativeOperator 2 k => A u)
    (sourceDerivativeBCF_apply 2 hL k ω x).symm

theorem weightedFourierField_periodic {L : ℝ} (hL : L ≠ 0) (w : SourceMode 2 → ℝ)
    (a : Parameter) (n : Fin 2 → ℤ) (x : Fin 2 → ℝ) :
    weightedFourierField L w a (x + fun i => L * (n i : ℝ)) = weightedFourierField L w a x := by
  have heq : weightedFourierField L w a = sourceField 2 L (fun m => a m / w m) := by
    ext y
    apply tsum_congr
    intro m
    exact mul_comm _ _
  rw [heq]
  exact I4Lattice.sourceField_lattice_shift 2 hL _ n x

end I4SourceSmoothParameterSpace
