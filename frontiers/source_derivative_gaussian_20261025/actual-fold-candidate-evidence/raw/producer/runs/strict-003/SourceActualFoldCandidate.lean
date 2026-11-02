import SourceActualFoldH0

/-! Literal Lifetime critical types for the unchanged actual source, together
with its attained death and ordinary-H0 interval. No canonical elder partner
or global conditional Morse assertion is made. -/

noncomputable section
open Set MeasureTheory
open UniversalLaw.Spec.Lifetime I4LifetimeField I4SmoothCarrier
open I4SourceConfluentPins I4SourceRawPinConditioning
open I4SourceCompactTargetMoments I4SourceAdaptiveFoldChart
open I4SourceAdaptiveFoldEstimates AdaptiveFoldTransverseRidge AdaptiveFoldBoundaryPath
set_option autoImplicit false

namespace I4SourceActualFoldCandidate

/-- Two coordinate directional pins give the whole derivative, before transport. -/
theorem derivative_zero_of_coordinate_pins
    (D : (Fin 2 → ℝ) →L[ℝ] ℝ)
    (hx : D directionX = 0) (hy : D directionY = 0) : D = 0 := by
  ext q
  have hq : q = q 0 • directionX + q 1 • directionY := by
    ext i
    fin_cases i <;> simp [directionX, directionY]
  rw [hq, map_add, map_smul, map_smul, hx, hy]
  simp

/-- The forward criticality implication uses actual smoothness and the chain rule. -/
theorem actual_critical_of_coordinate_pins {L : ℝ} (hL : 0 < L)
    (sample : SmoothSample 2 L) (x : E 2)
    (hx : fderiv ℝ (smoothSourceField 2 L sample) (coordinates 2 x) directionX = 0)
    (hy : fderiv ℝ (smoothSourceField 2 L sample) (coordinates 2 x) directionY = 0) :
    IsCriticalPoint 2 (actualField 2 L sample) x := by
  have hd := (smoothSourceField_smooth 2 hL.ne' sample).differentiable (by simp)
  have hc := (hd (coordinates 2 x)).hasFDerivAt.comp x (coordinates 2).hasFDerivAt
  change fderiv ℝ (actualField 2 L sample) x = 0
  rw [show fderiv ℝ (actualField 2 L sample) x =
    (fderiv ℝ (smoothSourceField 2 L sample) (coordinates 2 x)).comp
      (coordinates 2).toContinuousLinearMap from hc.fderiv]
  rw [derivative_zero_of_coordinate_pins _ hx hy]
  rfl

/-- Both literal endpoint lifts are critical under the original six raw pins. -/
theorem actual_rawPins_critical {L r b k : ℝ} (hL : 0 < L)
    (sample : SmoothSample 2 L)
    (hp : rawPins L r sample = ![b,b-k*r^3,0,0,0,0]) :
    IsCriticalPoint 2 (actualField 2 L sample) ((coordinates 2).symm (endpointM r)) ∧
      IsCriticalPoint 2 (actualField 2 L sample) ((coordinates 2).symm (endpointS r)) := by
  have h2 := congrFun hp (2 : Fin 6)
  have h3 := congrFun hp (3 : Fin 6)
  have h4 := congrFun hp (4 : Fin 6)
  have h5 := congrFun hp (5 : Fin 6)
  simp [rawPins] at h2 h3 h4 h5
  constructor
  · apply actual_critical_of_coordinate_pins hL sample
    · simpa only [ContinuousLinearEquiv.apply_symm_apply] using h2
    · simpa only [ContinuousLinearEquiv.apply_symm_apply] using h4
  · apply actual_critical_of_coordinate_pins hL sample
    · simpa only [ContinuousLinearEquiv.apply_symm_apply] using h3
    · simpa only [ContinuousLinearEquiv.apply_symm_apply] using h5

/-- Actual Hessians transport every pair of vectors through the literal
continuous linear coordinate equivalence. This makes no isometry assertion. -/
theorem actual_hessian_coordinates {L : ℝ} (hL : 0 < L)
    (sample : SmoothSample 2 L) (x v w : E 2) :
    hessian 2 (actualField 2 L sample) x v w =
      iteratedFDeriv ℝ 2 (smoothSourceField 2 L sample) (coordinates 2 x)
        ![coordinates 2 v, coordinates 2 w] := by
  have h := (coordinates 2).toContinuousLinearMap.iteratedFDeriv_comp_right
    (smoothSourceField_smooth 2 hL.ne' sample) x (i := 2) (by simp)
  have hh := congrArg (fun D => D ![v,w]) h
  have hdirs : (fun i => coordinates 2 (![v,w] i)) =
      ![coordinates 2 v, coordinates 2 w] := by
    ext i
    fin_cases i <;> rfl
  change iteratedFDeriv ℝ 2 (fun y => smoothSourceField 2 L sample (coordinates 2 y)) x ![v,w] = _
  simpa only [Function.comp_def,
    ContinuousMultilinearMap.compContinuousLinearMap_apply,
    ContinuousLinearEquiv.coe_coe, hdirs] using hh

/-- The physical Hessian amplitude is 6kr after both spatial derivatives;
the physical potential itself retains the positive amplitude 6kr³. -/
theorem actual_hessian_physical {L r k : ℝ} (hL : 0 < L)
    (sample : SmoothSample 2 L) (hr : 0 < r) (hk : 0 < k)
    (p : ℝ × ℝ) (v w : E 2) :
    hessian 2 (actualField 2 L sample)
        ((coordinates 2).symm (r • ![p.1,p.2])) v w =
      (6*k*r) * iteratedFDeriv ℝ 2 (actualFoldPotential r k sample) p
        ![(coordinates 2 v 0, coordinates 2 v 1),
          (coordinates 2 w 0, coordinates 2 w 1)] := by
  rw [actual_hessian_coordinates hL, ContinuousLinearEquiv.apply_symm_apply]
  let vv : Fin 2 → ℝ × ℝ :=
    ![(coordinates 2 v 0, coordinates 2 v 1),
      (coordinates 2 w 0, coordinates 2 w 1)]
  have hj := I4ActualFoldChartJets.pullback_jet (smoothSourceField 2 L sample)
    (smoothSourceField_smooth 2 hL.ne' sample) 2 (6*k*r^3)⁻¹ r p vv
  have hV : (fun q : ℝ × ℝ => (6*k*r^3)⁻¹ *
      smoothSourceField 2 L sample (r • ![q.1,q.2])) = actualFoldPotential r k sample := by
    ext q
    simp [actualFoldPotential, div_eq_mul_inv, mul_comm]
  rw [hV] at hj
  have hdirs : (fun i => ![(vv i).1,(vv i).2]) =
      ![coordinates 2 v, coordinates 2 w] := by
    ext i j
    fin_cases i <;> fin_cases j <;> rfl
  rw [hdirs] at hj
  change _ = (6*k*r) * iteratedFDeriv ℝ 2 (actualFoldPotential r k sample) p vv
  rw [hj]
  field_simp [hr.ne', hk.ne']

end I4SourceActualFoldCandidate
