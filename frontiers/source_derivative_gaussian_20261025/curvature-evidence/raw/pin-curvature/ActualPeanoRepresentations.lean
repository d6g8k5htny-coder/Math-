import SourcePinCurvatureBounds

noncomputable section
open I4SmoothCarrier I4SourceConfluentPins I4SourceEndpointRegression
open I4SourcePinCurvatureBounds I4ModeCurveChains I4ConfluentIntegralIdentities
open I4SourceConfluentLimits MeasureTheory Set
open scoped Interval
set_option autoImplicit false

namespace I4SourcePinCurvatureBounds

def sourceF (L : ℝ) (ω : SmoothSample 2 L) (t : ℝ) : ℝ :=
  smoothSourceField 2 L ω ![t,0]
def sourceH (L : ℝ) (ω : SmoothSample 2 L) (t : ℝ) : ℝ :=
  fderiv ℝ (smoothSourceField 2 L ω) ![t,0] directionY
def sourceQCurve (L : ℝ) (ω : SmoothSample 2 L) (t : ℝ) : ℝ :=
  iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω) ![t,0] ![directionY,directionY]

theorem sourceF_C3 {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) :
    ContDiff ℝ 3 (sourceF L ω) :=
  ((smoothSourceField_smooth 2 hL ω).comp axisMap.contDiff).of_le (by simp)

theorem sourceH_C2 {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) :
    ContDiff ℝ 2 (sourceH L ω) :=
  (axis_transverse_smooth _ (smoothSourceField_smooth 2 hL ω)).of_le (by simp)

theorem sourceF_deriv {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) (t : ℝ) :
    deriv (sourceF L ω) t = fderiv ℝ (smoothSourceField 2 L ω) ![t,0] directionX := by
  change deriv (fun s => smoothSourceField 2 L ω ![s,0]) t = _
  have h := axis_iteratedDeriv _ (smoothSourceField_smooth 2 hL ω) 1 t
  simpa [sourceF,iteratedDeriv_one,iteratedFDeriv_one_apply] using h

theorem sourceF_second {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) (t : ℝ) :
    iteratedDeriv 2 (sourceF L ω) t =
      iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω) ![t,0] ![directionX,directionX] := by
  change iteratedDeriv 2 (fun s => smoothSourceField 2 L ω ![s,0]) t = _
  have h := axis_iteratedDeriv _ (smoothSourceField_smooth 2 hL ω) 2 t
  have hd : (fun _ : Fin 2 => directionX) = ![directionX,directionX] := by
    ext i; fin_cases i <;> rfl
  simpa only [sourceF,hd] using h

theorem sourceH_deriv {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) (t : ℝ) :
    deriv (sourceH L ω) t =
      iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω) ![t,0] ![directionX,directionY] := by
  change deriv (fun s => fderiv ℝ (smoothSourceField 2 L ω) ![s,0] directionY) t = _
  have h := axis_transverse_iteratedDeriv _ (smoothSourceField_smooth 2 hL ω) 1 t
  have hd : Fin.snoc (fun _ : Fin 1 => directionX) directionY =
      ![directionX,directionY] := by ext i; fin_cases i <;> rfl
  simpa only [sourceH,iteratedDeriv_one,hd] using h

theorem sourceH_second_zero {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) :
    iteratedDeriv 2 (sourceH L ω) 0 = sourceA L ω := by
  change iteratedDeriv 2 (fun s => fderiv ℝ (smoothSourceField 2 L ω) ![s,0] directionY) 0 = _
  have h := axis_transverse_iteratedDeriv _ (smoothSourceField_smooth 2 hL ω) 2 0
  have hd : Fin.snoc (fun _ : Fin 2 => directionX) directionY =
      ![directionX,directionX,directionY] := by ext i; fin_cases i <;> rfl
  have h0 : (![0,0] : Fin 2 → ℝ) = 0 := by ext i; fin_cases i <;> rfl
  simpa only [sourceA,hd,h0] using h

theorem source_pin3_eq {L : ℝ} (hL : L ≠ 0) (r : ℝ) (ω : SmoothSample 2 L) :
    sourceConfluentPinsAt L r ω 3 = pin3 (sourceF L ω) r := by
  simp [sourceConfluentPinsAt,confluentTransform,rawPins,pin3,sourceF_deriv hL,
    endpointM,endpointS]

theorem source_pin4_eq (L r : ℝ) (ω : SmoothSample 2 L) :
    sourceConfluentPinsAt L r ω 4 = pin4 (sourceH L ω) r := rfl

theorem source_pin5_eq {L : ℝ} (hL : L ≠ 0) (r : ℝ) (ω : SmoothSample 2 L) :
    sourceConfluentPinsAt L r ω 5 = pin5 (sourceF L ω) r := by
  change (12/r^2) *
    ((fderiv ℝ (smoothSourceField 2 L ω) ![-r/2,0] directionX +
      fderiv ℝ (smoothSourceField 2 L ω) ![r/2,0] directionX)/2 -
      (smoothSourceField 2 L ω ![r/2,0] - smoothSourceField 2 L ω ![-r/2,0])/r) = _
  unfold pin5
  rw [sourceF_deriv hL,sourceF_deriv hL]
  change (12/r^2) *
    ((fderiv ℝ (smoothSourceField 2 L ω) ![-r/2,0] directionX +
      fderiv ℝ (smoothSourceField 2 L ω) ![r/2,0] directionX)/2 -
      (smoothSourceField 2 L ω ![r/2,0] - smoothSourceField 2 L ω ![-r/2,0])/r) =
    (12/r^2) *
    ((fderiv ℝ (smoothSourceField 2 L ω) ![r/2,0] directionX +
      fderiv ℝ (smoothSourceField 2 L ω) ![-r/2,0] directionX)/2 -
      (smoothSourceField 2 L ω ![r/2,0] - smoothSourceField 2 L ω ![-r/2,0])/r)
  ring

theorem source_normalized_peano {L : ℝ} (hL : L ≠ 0) (r : ℝ) (hr : r ≠ 0)
    (ω : SmoothSample 2 L) (h3 : sourceConfluentPinsAt L r ω 3 = 0)
    (h4 : sourceConfluentPinsAt L r ω 4 = 0) :
    sourceNormalizedEndpoints L r ω =
      ![-(∫ u in (-1/2:ℝ)..(1/2:ℝ), peanoLeft u * iteratedDeriv 3 (sourceF L ω) (r*u)),
        (∫ u in (-1/2:ℝ)..(1/2:ℝ), peanoRight u * iteratedDeriv 3 (sourceF L ω) (r*u)),
        -(∫ u in (-1/2:ℝ)..(1/2:ℝ), peanoLeft u * iteratedDeriv 2 (sourceH L ω) (r*u)),
        (∫ u in (-1/2:ℝ)..(1/2:ℝ), peanoRight u * iteratedDeriv 2 (sourceH L ω) (r*u)),
        sourceQCurve L ω (-r/2),sourceQCurve L ω (r/2)] := by
  have hx := adjusted_second_left (sourceF L ω) (sourceF_C3 hL ω) r hr
  have hy := adjusted_second_right (sourceF L ω) (sourceF_C3 hL ω) r hr
  have hz := adjusted_transverse_left (sourceH L ω) (sourceH_C2 hL ω) r hr
  have hw := adjusted_transverse_right (sourceH L ω) (sourceH_C2 hL ω) r hr
  have hp3 : pin3 (sourceF L ω) r = 0 := (source_pin3_eq hL r ω).symm.trans h3
  have hp4 : pin4 (sourceH L ω) r = 0 := (source_pin4_eq L r ω).symm.trans h4
  rw [hp3,sub_zero,sourceF_second hL] at hx hy
  rw [hp4,sub_zero,sourceH_deriv hL] at hz hw
  ext i
  fin_cases i
  · simpa [sourceNormalizedEndpoints,rawPinsWithHessians,endpointM,peanoLeft] using hx
  · simpa [sourceNormalizedEndpoints,rawPinsWithHessians,endpointS,peanoRight] using hy
  · simpa [sourceNormalizedEndpoints,rawPinsWithHessians,endpointM,peanoLeft] using hz
  · simpa [sourceNormalizedEndpoints,rawPinsWithHessians,endpointS,peanoRight] using hw
  · rfl
  · rfl

end I4SourcePinCurvatureBounds
