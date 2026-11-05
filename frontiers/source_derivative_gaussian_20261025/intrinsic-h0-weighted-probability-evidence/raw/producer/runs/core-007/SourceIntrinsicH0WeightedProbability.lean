import SourceIntrinsicH0Interface
import SourceCompactFoldWeightedProbability
import SourceSmoothTopology
import Mathlib.Analysis.Calculus.FDeriv.Symmetric

/-! Fixed-axis literal intrinsic finite-bar event and its actual weighted mass.
Norm-Borel field and exact planar inertia adapters supply event measurability;
accepted compact cutoff estimates control its actual normalized complement.
No canonical global label, all-frame law or Parent result is asserted. -/

noncomputable section
open CategoryTheory Limits Set MeasureTheory BoundedContinuousFunction
open UniversalLaw.Spec.Lifetime I4LifetimeField I4SmoothCarrier
open I4SourceH0OlderClearance I4SourceIntrinsicH0Interface
open I4SourceActualFoldCandidate I4SourceSmoothTopology
open SourceCompactFoldWeightedProbability TorusFiltration
open I4SourceConfluentPins I4SourceRawPinConditioning
open I4SourceCompactTargetMoments I4SourceAdaptiveFoldEstimates
set_option autoImplicit false
namespace I4SourceIntrinsicH0WeightedProbability

private def operatorEval (k : ℕ) (v : Fin k → (Fin 2 → ℝ)) :
    DerivativeOperator 2 k →L[ℝ] ℝ where
  toFun f := f v
  map_add' _ _ := rfl
  map_smul' _ _ := rfl
  cont := continuous_eval_const v

private def actualBCF {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) : E 2 →ᵇ ℝ :=
  ((operatorEval 0 (fun i => Fin.elim0 i)).compLeftContinuousBounded (Fin 2 → ℝ)
    (sourceDerivativeBCF 2 hL 0 ω)).compContinuous
      ⟨coordinates 2, (coordinates 2).continuous⟩

private theorem actualBCF_apply {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) (x : E 2) :
    actualBCF hL ω x = actualField 2 L ω x := by
  change sourceDerivativeBCF 2 hL 0 ω (coordinates 2 x) (fun i => Fin.elim0 i) = _
  simp only [sourceDerivativeBCF_apply, iteratedFDeriv_zero_apply, actualField]

private theorem actualBCF_measurable {L : ℝ} (hL : L ≠ 0) :
    @Measurable (SmoothSample 2 L) (E 2 →ᵇ ℝ) _ (borel _) (actualBCF hL) := by
  borelize (DerivativeBCF 2 0) (E 2 →ᵇ ℝ)
  have hc : Continuous (fun f : DerivativeBCF 2 0 =>
      ((operatorEval 0 (fun i => Fin.elim0 i)).compLeftContinuousBounded (Fin 2 → ℝ) f).compContinuous ⟨coordinates 2, (coordinates 2).continuous⟩) :=
    (BoundedContinuousFunction.compContinuousCLM ℝ ℝ
      ⟨coordinates 2, (coordinates 2).continuous⟩).continuous.comp
        ((operatorEval 0 (fun i => Fin.elim0 i)).compLeftContinuousBounded (Fin 2 → ℝ)).continuous
  exact hc.measurable.comp (sourceDerivativeBCF_borel 2 hL 0)

private theorem jetScalar_measurable {L : ℝ} (hL : L ≠ 0) (k : ℕ)
    (x : Fin 2 → ℝ) (v : Fin k → (Fin 2 → ℝ)) :
    Measurable (fun ω : SmoothSample 2 L =>
      iteratedFDeriv ℝ k (smoothSourceField 2 L ω) x v) := by
  borelize (DerivativeBCF 2 k) (DerivativeOperator 2 k)
  have hc : Continuous (fun f : DerivativeBCF 2 k => f x v) :=
    (operatorEval k v).continuous.comp (BoundedContinuousFunction.evalCLM ℝ x).continuous
  have hm := hc.measurable.comp (sourceDerivativeBCF_borel 2 hL k)
  change Measurable (fun ω => sourceDerivativeBCF 2 hL k ω x v) at hm
  simpa only [sourceDerivativeBCF_apply] using hm

private def basisX : E 2 := (coordinates 2).symm directionX
private def basisY : E 2 := (coordinates 2).symm directionY

private theorem actualCritical_iff {L : ℝ} (hL : 0 < L) (ω : SmoothSample 2 L) (x : E 2) :
    IsCriticalPoint 2 (actualField 2 L ω) x ↔
      fderiv ℝ (smoothSourceField 2 L ω) (coordinates 2 x) directionX = 0 ∧
      fderiv ℝ (smoothSourceField 2 L ω) (coordinates 2 x) directionY = 0 := by
  constructor
  · intro hc
    have hd := (smoothSourceField_smooth 2 hL.ne' ω).differentiable (by simp)
    have hchain := (hd (coordinates 2 x)).hasFDerivAt.comp x (coordinates 2).hasFDerivAt
    change fderiv ℝ (actualField 2 L ω) x = 0 at hc
    have hf : (fderiv ℝ (smoothSourceField 2 L ω) (coordinates 2 x)).comp
        (coordinates 2).toContinuousLinearMap = 0 := hchain.fderiv.symm.trans hc
    constructor
    · simpa [basisX] using congrArg (fun D => D basisX) hf
    · simpa [basisY] using congrArg (fun D => D basisY) hf
  · rintro ⟨hx,hy⟩
    exact actual_critical_of_coordinate_pins hL ω x hx hy

private theorem actualCritical_measurable {L : ℝ} (hL : 0 < L) (x : E 2) :
    MeasurableSet {ω : SmoothSample 2 L | IsCriticalPoint 2 (actualField 2 L ω) x} := by
  have hx := jetScalar_measurable hL.ne' 1 (coordinates 2 x) ![directionX]
  have hy := jetScalar_measurable hL.ne' 1 (coordinates 2 x) ![directionY]
  simp only [iteratedFDeriv_one_apply] at hx hy
  convert (measurableSet_eq_fun hx measurable_const).inter
    (measurableSet_eq_fun hy measurable_const) using 1
  ext ω
  exact actualCritical_iff hL ω x

private def hA (g : E 2 → ℝ) (x : E 2) : ℝ := hessian 2 g x basisX basisX
private def hB (g : E 2 → ℝ) (x : E 2) : ℝ := hessian 2 g x basisX basisY
private def hC (g : E 2 → ℝ) (x : E 2) : ℝ := hessian 2 g x basisY basisY

private theorem vector_decomp (v : E 2) :
    v = (coordinates 2 v 0) • basisX + (coordinates 2 v 1) • basisY := by
  apply (coordinates 2).injective
  simp only [map_add, map_smul, basisX, basisY, ContinuousLinearEquiv.apply_symm_apply]
  ext i
  fin_cases i <;> simp [directionX,directionY]

private theorem hessian_quadratic (g : E 2 → ℝ) (hg : ContDiff ℝ 2 g)
    (x v : E 2) :
    hessian 2 g x v v = hA g x * (coordinates 2 v 0)^2 +
      2 * hB g x * (coordinates 2 v 0) * (coordinates 2 v 1) +
      hC g x * (coordinates 2 v 1)^2 := by
  have hsym : fderiv ℝ (fderiv ℝ g) x basisY basisX =
      fderiv ℝ (fderiv ℝ g) x basisX basisY :=
    hg.contDiffAt.isSymmSndFDerivAt (by simp) basisY basisX
  unfold hA hB hC hessian
  simp only [iteratedFDeriv_two_apply, Matrix.cons_val_zero, Matrix.cons_val_one]
  conv_lhs => rw [vector_decomp v]
  simp only [map_add, map_smul, _root_.add_apply, _root_.smul_apply, smul_eq_mul]
  rw [hsym]
  ring

private theorem actualHessian_measurable {L : ℝ} (hL : 0 < L) (x v w : E 2) :
    Measurable (fun ω : SmoothSample 2 L => hessian 2 (actualField 2 L ω) x v w) := by
  have hm := jetScalar_measurable hL.ne' 2 (coordinates 2 x) ![coordinates 2 v, coordinates 2 w]
  convert hm using 1
  funext ω
  exact actual_hessian_coordinates hL ω x v w

/-- Literal fixed-axis intrinsic finite-bar membership on the original carrier. -/
def sourceIntrinsicFiniteBarEvent (L r : ℝ) : Set (SmoothSample 2 L) :=
  {ω | IsFiniteBar 2 L (h0Interface 2 L) (actualField 2 L ω)
    (endpointLiftM r) (endpointLiftS r)}

/-- The actual unchanged physical weighted law's mass of that literal event. -/
def sourceIntrinsicFiniteBarProbability {L : ℝ} (hL : 0 < L) (r b k : ℝ) : ℝ :=
  (sourceCompactFoldWeightedLaw hL.ne' r b k).real (sourceIntrinsicFiniteBarEvent L r)

end I4SourceIntrinsicH0WeightedProbability
