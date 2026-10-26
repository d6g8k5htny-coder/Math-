push=open('/workspace/scratch/regression-kernel/smooth-palm/pushforward/WeightedPushforward.lean').read();pushbody=push[push.index('lemma withDensity_map_comp'):push.rindex('end I4SourceSmoothPalm')]
pins=open('/workspace/scratch/regression-kernel/smooth-palm/pins/RawPinSupport.lean').read();pinsbody=pins[pins.index('def sourceSmoothLaw'):pins.rindex('end I4SourceSmoothPalm')]
header='''import SourceSmoothConditionalKernel

/-!
# Literal determinant weighting on the actual smooth carrier

The base law is the specified actual whole-carrier kernel at the prescribed
six-pin value. The weight uses the actual endpoint Hessian entries and strict
maximum/saddle typing. Exact endpoint pushforward identities transfer the
proved moment and normalizer estimates to every measurable carrier event.

The normalized density formula below is a probability law on the actual smooth
carrier. It is not identified here with a geometric critical-point-process Palm
disintegration, and supplies no Morse, elder, counting or event measurability claim.
See `SOURCE_SMOOTH_PALM.md` for the frozen source contract.
-/

noncomputable section

open I4SmoothCarrier I4SourceConfluentPins I4SourceEndpointRegression I4SourceSmoothConditional
open I4SourceEndpointEstimates I4SourceEndpointParameters
open MeasureTheory ProbabilityTheory ResearchFormalCoreR1 Matrix Filter
open scoped BigOperators ENNReal Topology

set_option autoImplicit false

namespace I4SourceSmoothPalm

'''
new='''/-- Literal actual symmetric endpoint Hessian entries at M. -/
def sourceRawHM (L r : ℝ) (ω : SmoothSample 2 L) : Matrix (Fin 2) (Fin 2) ℝ :=
  let v := rawPinsWithHessians L r ω
  !![v 6,v 7;v 7,v 8]

/-- Literal actual symmetric endpoint Hessian entries at S. -/
def sourceRawHS (L r : ℝ) (ω : SmoothSample 2 L) : Matrix (Fin 2) (Fin 2) ℝ :=
  let v := rawPinsWithHessians L r ω
  !![v 9,v 10;v 10,v 11]

def sourceSmoothTyped (L r : ℝ) (ω : SmoothSample 2 L) : Prop :=
  dm2Negative (sourceRawHM L r ω) ∧ (sourceRawHS L r ω).det < 0

/-- Strict maximum/saddle determinant weight of the actual field at its two endpoints. -/
def sourceSmoothWeight (L r : ℝ) (ω : SmoothSample 2 L) : ℝ := by
  classical
  exact if sourceSmoothTyped L r ω then |(sourceRawHM L r ω).det * (sourceRawHS L r ω).det| else 0

lemma sourceRawHM_eq_normalized (L r : ℝ) (hr : r ≠ 0) (ω : SmoothSample 2 L) :
    sourceRawHM L r ω = egm_HM r (sourcePhysicalCoordinates (sourceNormalizedEndpoints L r ω)) := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [sourceRawHM, egm_HM, sourcePhysicalCoordinates, sourceNormalizedEndpoints, hr]

lemma sourceRawHS_eq_normalized (L r : ℝ) (hr : r ≠ 0) (ω : SmoothSample 2 L) :
    sourceRawHS L r ω = egm_HS r (sourcePhysicalCoordinates (sourceNormalizedEndpoints L r ω)) := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [sourceRawHS, egm_HS, sourcePhysicalCoordinates, sourceNormalizedEndpoints, hr]

theorem sourceSmoothWeight_eq (L r : ℝ) (hr : r ≠ 0) (ω : SmoothSample 2 L) :
    sourceSmoothWeight L r ω = sourceEndpointWeight r (sourceNormalizedEndpoints L r ω) := by
  unfold sourceSmoothWeight sourceSmoothTyped sourceEndpointWeight egm_weight
  rw [sourceRawHM_eq_normalized L r hr ω, sourceRawHS_eq_normalized L r hr ω]

theorem sourceSmoothWeight_nonneg (L r : ℝ) (ω : SmoothSample 2 L) :
    0 ≤ sourceSmoothWeight L r ω := by
  unfold sourceSmoothWeight
  split_ifs
  · exact abs_nonneg _
  · exact le_rfl

theorem sourceSmoothWeight_measurable {L : ℝ} (hL : L ≠ 0) (r : ℝ) (hr : r ≠ 0) :
    Measurable (sourceSmoothWeight L r) := by
  have heq : sourceSmoothWeight L r = sourceEndpointWeight r ∘ sourceNormalizedEndpoints L r :=
    funext (sourceSmoothWeight_eq L r hr)
  rw [heq]
  exact (sourceEndpointWeight_measurable r).comp (sourceNormalizedEndpoints_measurable hL r)

theorem sourceSmoothWeight_pos_iff (L r : ℝ) (ω : SmoothSample 2 L) :
    0 < sourceSmoothWeight L r ω ↔ sourceSmoothTyped L r ω := by
  classical
  by_cases ht : sourceSmoothTyped L r ω
  · have hM : 0 < (sourceRawHM L r ω).det := by
      have h := (dm2_negative_iff _ _ _).mp ht.1
      simpa [sourceRawHM, Matrix.det_fin_two] using h.2
    have hn : (sourceRawHM L r ω).det * (sourceRawHS L r ω).det ≠ 0 :=
      mul_ne_zero hM.ne' ht.2.ne
    simp [sourceSmoothWeight, ht, abs_pos.mpr hn]
  · simp [sourceSmoothWeight, ht]

theorem sourceSmoothTyped_measurableSet {L : ℝ} (hL : L ≠ 0) (r : ℝ) (hr : r ≠ 0) :
    MeasurableSet {ω : SmoothSample 2 L | sourceSmoothTyped L r ω} := by
  have heq : {ω : SmoothSample 2 L | sourceSmoothTyped L r ω} =
      {ω | 0 < sourceSmoothWeight L r ω} := by
    ext ω
    exact (sourceSmoothWeight_pos_iff L r ω).symm
  rw [heq]
  exact measurableSet_lt measurable_const (sourceSmoothWeight_measurable hL r hr)

/-- The whole-carrier probability defined by the literal normalized actual determinant density. -/
def sourceSmoothWeightedLaw {L : ℝ} (hL : L ≠ 0) (r b : ℝ) : Measure (SmoothSample 2 L) :=
  prwMeasure (sourceSmoothLaw hL r b) (sourceSmoothWeight L r)

theorem sourceSmoothLaw_endpoint_hasLaw {L : ℝ} (hL : L ≠ 0) (r b : ℝ)
    (hG : IsUnit (sourcePinCovarianceAt L r)) :
    HasLaw (sourceNormalizedEndpoints L r) (sourcePhysicalEndpointLaw L r b)
      (sourceSmoothLaw hL r b) := by
  refine ⟨(sourceNormalizedEndpoints_measurable hL r).aemeasurable, ?_⟩
  exact sourceSmoothKernel_physical_prescribed_map hL r b hG

theorem sourceSmoothLaw_weight_square_integrable {L : ℝ} (hL : L ≠ 0) (r b : ℝ)
    (hr : r ≠ 0) (hG : IsUnit (sourcePinCovarianceAt L r))
    (hsq : Integrable (fun v => sourceEndpointWeight r v ^ 2) (sourcePhysicalEndpointLaw L r b)) :
    Integrable (fun ω => sourceSmoothWeight L r ω ^ 2) (sourceSmoothLaw hL r b) := by
  simpa only [sourceSmoothWeight_eq L r hr] using
    (sourceSmoothLaw_endpoint_hasLaw hL r b hG).integrable_comp hsq

theorem sourceSmoothLaw_weight_integral {L : ℝ} (hL : L ≠ 0) (r b : ℝ)
    (hr : r ≠ 0) (hG : IsUnit (sourcePinCovarianceAt L r)) :
    (∫ ω, sourceSmoothWeight L r ω ∂sourceSmoothLaw hL r b) =
      ∫ v, sourceEndpointWeight r v ∂sourcePhysicalEndpointLaw L r b := by
  simpa only [sourceSmoothWeight_eq L r hr, Function.comp_def] using
    (sourceSmoothLaw_endpoint_hasLaw hL r b hG).integral_comp
      (sourceEndpointWeight_measurable r).aestronglyMeasurable

theorem sourceSmoothLaw_weight_square_integral {L : ℝ} (hL : L ≠ 0) (r b : ℝ)
    (hr : r ≠ 0) (hG : IsUnit (sourcePinCovarianceAt L r)) :
    (∫ ω, sourceSmoothWeight L r ω ^ 2 ∂sourceSmoothLaw hL r b) =
      ∫ v, sourceEndpointWeight r v ^ 2 ∂sourcePhysicalEndpointLaw L r b := by
  simpa only [sourceSmoothWeight_eq L r hr, Function.comp_def] using
    (sourceSmoothLaw_endpoint_hasLaw hL r b hG).integral_comp
      ((sourceEndpointWeight_measurable r).pow_const 2).aestronglyMeasurable

/-- Exact endpoint pushforward of the literal weighted whole-carrier law. -/
theorem sourceSmoothWeightedLaw_endpoint_map {L : ℝ} (hL : L ≠ 0) (r b : ℝ)
    (hr : r ≠ 0) (hG : IsUnit (sourcePinCovarianceAt L r)) :
    (sourceSmoothWeightedLaw hL r b).map (sourceNormalizedEndpoints L r) =
      sourcePhysicalEndpointWeightedProbability L r b := by
  have heq : sourceSmoothWeight L r = sourceEndpointWeight r ∘ sourceNormalizedEndpoints L r :=
    funext (sourceSmoothWeight_eq L r hr)
  unfold sourceSmoothWeightedLaw sourcePhysicalEndpointWeightedProbability
  rw [heq, prwMeasure_map_comp _ _ _ (sourceNormalizedEndpoints_measurable hL r)
      (sourceEndpointWeight_measurable r), (sourceSmoothLaw_endpoint_hasLaw hL r b hG).map_eq]

'''
open('SourceSmoothPalm.lean','w').write(header+pushbody+pinsbody+new+'end I4SourceSmoothPalm\n')
