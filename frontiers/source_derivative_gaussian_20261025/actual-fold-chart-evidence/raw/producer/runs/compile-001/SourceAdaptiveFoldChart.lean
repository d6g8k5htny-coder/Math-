import SourceCompactTargetMoments
import SourcePinPreservingQuartic
import AdaptiveFoldTransverseRidge

/-!
# Literal normalized fold chart for the actual fixed-axis source law

The original smooth carrier and centered x/y observation are retained. The
normalization includes the genuine varying cubic-gap coefficient `6*k`.
No framed conditional law or wider-rectangle conclusion is asserted here.
-/

noncomputable section

open I4SmoothCarrier I4SourceConfluentPins I4SourceRawPinConditioning
open I4SourceCompactTargetMoments I4ConfluentIntegralIdentities
open AdaptiveFoldTransverseRidge MeasureTheory
open scoped Interval Matrix

set_option autoImplicit false

namespace I4SourceAdaptiveFoldChart

/-- Literal fixed-axis potential on the product/max-norm coordinate domain. -/
def actualFoldPotential {L : ℝ} (r k : ℝ) (ω : SmoothSample 2 L)
    (p : ℝ × ℝ) : ℝ :=
  smoothSourceField 2 L ω (r • ![p.1, p.2]) / (6*k*r^3)

/-- The exact deterministic data exported at every actual conditioned sample. -/
def NormalizedFoldData (V : ℝ × ℝ → ℝ) : Prop :=
  ContDiff ℝ 4 V ∧
  Vx V (-1/2, 0) = 0 ∧ Vx V (1/2, 0) = 0 ∧
  Vy V (-1/2, 0) = 0 ∧ Vy V (1/2, 0) = 0 ∧
  V (-1/2, 0) - V (1/2, 0) = 1/6 ∧
  (∫ u in (-1/2 : ℝ)..(1/2 : ℝ), (3/2-6*u^2) *
    (fderiv ℝ (fderiv ℝ (Vx V)) (u, 0) ex ex)) = 2

/-- The product chart sends the literal left normalized endpoint to the raw one. -/
theorem chart_endpointM (r : ℝ) :
    r • (![-1/2, 0] : Fin 2 → ℝ) = endpointM r := by
  ext i
  fin_cases i <;> simp [endpointM] <;> ring

/-- The product chart sends the literal right normalized endpoint to the raw one. -/
theorem chart_endpointS (r : ℝ) :
    r • (![1/2, 0] : Fin 2 → ℝ) = endpointS r := by
  ext i
  fin_cases i <;> simp [endpointS] <;> ring

/-- The actual raw values give the exact normalized height difference. -/
theorem actualFoldPotential_gap {L r k b : ℝ} (ω : SmoothSample 2 L)
    (hr : 0 < r) (hk : 0 < k)
    (hp : rawPins L r ω = ![b,b-k*r^3,0,0,0,0]) :
    actualFoldPotential r k ω (-1/2,0) -
      actualFoldPotential r k ω (1/2,0) = 1/6 := by
  have hm := congrFun hp (0 : Fin 6)
  have hs := congrFun hp (1 : Fin 6)
  simp only [rawPins, Matrix.cons_val_zero, Matrix.cons_val_one] at hm hs
  simp only [actualFoldPotential, chart_endpointM, chart_endpointS, hm, hs]
  field_simp [hr.ne', hk.ne']
  <;> ring

end I4SourceAdaptiveFoldChart
