import SourceGapPinCurvature
import SourceAllTargetCurvatureResidual
import SourceWeightedCurvatureBound

/-!
# Actual varying-gap unnormalized bad-event numerator

The physical determinant weight and original signed-period carrier are retained.
All-target source support, moments, scalar product law and density are derived
from existing source estimates. The conclusion is an unnormalized r^5 integral;
no positive normalizer, weighted probability or parent theorem is asserted.
-/

noncomputable section

open I4SmoothCarrier I4SourceSmoothConditional I4SourceEndpointRegression
open I4SourceSmoothPalm I4SourceConditionalMajorant I4SourcePinCurvatureBounds
open I4SourceCompactTargetMoments I4SourceGapPinCurvature
open I4SourceAllTargetCurvatureResidual I4SourceCurvatureDecomposition
open I4SourceWeightedCurvature I4ScalarProductCurvature I4SourceContact
open I4SourceEndpointEstimates MeasureTheory ProbabilityTheory Set Filter
open ResearchFormalCoreR1
open scoped BigOperators Topology

set_option autoImplicit false

namespace I4SourceGapWeightedNumerator

/-- One interval chosen from the nonzero signed period alone gives integrability
of the actual physical weight at every real height and cubic-gap mark. -/
theorem sourceGapLaw_weight_integrable {L : ℝ} (hL : L ≠ 0) :
    ∃ δ : ℝ, 0 < δ ∧ δ ≤ 1 ∧ ∀ r : ℝ, 0 < r → r < δ → ∀ b k : ℝ,
      Integrable (sourceSmoothWeight L r) (sourceGapLaw hL r b k) := by
  obtain ⟨δW,hδW,hδW1,hW⟩ := sourceGapLaw_curvature_bounds hL
  obtain ⟨δR,hδR,_hδR1,hmom⟩ := sourceGammaRadius_allTarget_moments hL
  obtain ⟨_C,_hC,h4⟩ := hmom 4
  refine ⟨min δW δR,lt_min hδW hδR,(min_le_left _ _).trans hδW1,?_⟩
  intro r hr hrδ b k
  have hrW : r < δW := lt_of_lt_of_le hrδ (min_le_left _ _)
  have hrR : r < δR := lt_of_lt_of_le hrδ (min_le_right _ _)
  have hR : Integrable (fun ω => sourceGammaRadius L ω^4) (sourceGapLaw hL r b k) :=
    (h4 r hr hrR (sourceGapPins r b k)).1
  apply (hR.const_mul (10*r^2)).mono'
    (sourceSmoothWeight_measurable hL r hr.ne').aestronglyMeasurable
  filter_upwards [hW r hr hrW b k] with ω hω
  rw [Real.norm_eq_abs,abs_of_nonneg (sourceSmoothWeight_nonneg L r ω)]
  exact hω.2.2.1

end I4SourceGapWeightedNumerator
