import WeightedCarrier

noncomputable section
open I4SmoothCarrier I4SourceEndpointRegression I4SourceSmoothConditional
open MeasureTheory ProbabilityTheory Filter
open scoped Topology

set_option autoImplicit false

namespace I4SourceSmoothParameterSpace

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

end I4SourceSmoothParameterSpace
