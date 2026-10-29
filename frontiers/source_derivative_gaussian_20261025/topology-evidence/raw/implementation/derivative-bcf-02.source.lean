import SourceDerivativeGaussian
import Mathlib.Topology.ContinuousMap.Bounded.Normed
import Mathlib.MeasureTheory.Function.StronglyMeasurable.Basic
import Mathlib.MeasureTheory.Constructions.BorelSpace.Metrizable

noncomputable section
open I4Foundation I4Source I4Smooth I4SmoothCarrier I4SourceDerivativeGaussian
open MeasureTheory Filter BoundedContinuousFunction
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
  rw [norm_smul, Real.norm_eq_abs]
  exact (mul_le_mul_of_nonneg_left (modeDerivativeBCF_norm_le d hL k m) (abs_nonneg _)).trans_eq
    (mul_comm _ _)

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
  simp [modeDerivativeBCF, derivativeCoefficient, smul_eq_mul, mul_comm]

theorem stronglyMeasurable_of_countable_hasSum {I Ω E : Type*} [Countable I]
    [MeasurableSpace Ω] [NormedAddCommGroup E]
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
    fun m ω => ω.val m • (fun j => modeDerivativeBCF d hL j m)
  have ha (m : SourceMode d) : StronglyMeasurable (a m) := by
    exact (((measurable_pi_apply m).comp measurable_subtype_coe).stronglyMeasurable).smul_const
      (fun j : Fin (K+1) => modeDerivativeBCF d hL j m)
  apply stronglyMeasurable_of_countable_hasSum a _ ha
  intro ω
  exact Pi.hasSum.mpr (fun j => (sourceDerivativeBCF_summable d hL j ω).hasSum)

theorem sourceFiniteJet_borel (d : ℕ) {L : ℝ} (hL : L ≠ 0) (K : ℕ) :
    @Measurable (SmoothSample d L) ((j : Fin (K+1)) → DerivativeBCF d j)
      _ (borel _) (sourceFiniteJet d hL K) := by
  borelize ((j : Fin (K+1)) → DerivativeBCF d j)
  exact (sourceFiniteJet_stronglyMeasurable d hL K).measurable

end I4SourceSmoothTopology
