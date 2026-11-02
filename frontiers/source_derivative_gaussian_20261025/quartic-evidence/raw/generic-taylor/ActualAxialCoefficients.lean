import SourcePinPreservingQuartic

noncomputable section
open I4SmoothCarrier I4SourceConditionalMajorant I4SourceConfluentPins
open I4SourcePinCurvatureBounds I4ModeCurveChains I4ConfluentIntegralIdentities
open I4SourceConfluentLimits I4ActualQuarticTransfer MeasureTheory Set
open scoped Interval
set_option autoImplicit false

namespace I4SourcePinPreservingQuartic

private theorem sourceF_third_zero {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) :
    iteratedDeriv 3 (sourceF L ω) 0 = sourceAxialThird L ω := by
  have hd : (fun _ : Fin 3 => directionX) = ![directionX,directionX,directionX] := by
    ext i; fin_cases i <;> rfl
  have h0 : (![0,0] : Fin 2 → ℝ) = 0 := by ext i; fin_cases i <;> rfl
  change iteratedDeriv 3 (fun s => smoothSourceField 2 L ω ![s,0]) 0 =
    iteratedFDeriv ℝ 3 (smoothSourceField 2 L ω) 0 ![directionX,directionX,directionX]
  simpa only [hd,h0] using
    axis_iteratedDeriv _ (smoothSourceField_smooth 2 hL ω) 3 0

private theorem sourceF_fourth_zero {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) :
    iteratedDeriv 4 (sourceF L ω) 0 = sourceRawU L ω 3 := by
  have hd : (fun _ : Fin 4 => directionX) = ![directionX,directionX,directionX,directionX] := by
    ext i; fin_cases i <;> rfl
  have h0 : (![0,0] : Fin 2 → ℝ) = 0 := by ext i; fin_cases i <;> rfl
  change iteratedDeriv 4 (fun s => smoothSourceField 2 L ω ![s,0]) 0 =
    iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![directionX,directionX,directionX,directionX]
  simpa only [hd,h0] using
    axis_iteratedDeriv _ (smoothSourceField_smooth 2 hL ω) 4 0

private theorem sourceH_third_zero {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) :
    iteratedDeriv 3 (sourceH L ω) 0 = sourceRawU L ω 4 := by
  have hd : Fin.snoc (fun _ : Fin 3 => directionX) directionY =
      ![directionX,directionX,directionX,directionY] := by ext i; fin_cases i <;> rfl
  have h0 : (![0,0] : Fin 2 → ℝ) = 0 := by ext i; fin_cases i <;> rfl
  change iteratedDeriv 3 (fun s => fderiv ℝ (smoothSourceField 2 L ω) ![s,0] directionY) 0 =
    iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![directionX,directionX,directionX,directionY]
  simpa only [hd,h0] using
    axis_transverse_iteratedDeriv _ (smoothSourceField_smooth 2 hL ω) 3 0

private theorem sourceF_deriv_pins {L : ℝ} (hL : L ≠ 0) (r : ℝ)
    (ω : SmoothSample 2 L) (hp : sourcePhysicalPins L r ω) :
    deriv (sourceF L ω) (-r/2) = 0 ∧ deriv (sourceF L ω) (r/2) = 0 := by
  constructor
  · rw [sourceF_deriv hL]
    exact hp.1
  · rw [sourceF_deriv hL]
    exact hp.2.1

private theorem sourceH_pins (L r : ℝ) (ω : SmoothSample 2 L)
    (hp : sourcePhysicalPins L r ω) : sourceH L ω (-r/2) = 0 ∧ sourceH L ω (r/2) = 0 :=
  ⟨hp.2.2.1,hp.2.2.2.1⟩

theorem source_axial_third_error {L : ℝ} (hL : L ≠ 0) (r : ℝ) (hr : 0 < r)
    (ω : SmoothSample 2 L) (hp : sourcePhysicalPins L r ω) :
    |sourceAxialThird L ω - 2| ≤ r^2 * sourceDerivativeMajorant L 5 ω / 40 := by
  have hFp := sourceF_deriv_pins hL r ω hp
  have hpin : pin5 (sourceF L ω) r = 2 := by
    unfold pin5
    rw [hFp.1,hFp.2]
    have hgap : sourceF L ω (r/2) - sourceF L ω (-r/2) = -r^3/6 := hp.2.2.2.2
    rw [hgap]
    field_simp [ne_of_gt hr]
    ring
  have hpeano : 6 * (∫ u in (-1/2 : ℝ)..(1/2 : ℝ), peanoCubic u *
      iteratedDeriv 3 (sourceF L ω) (r*u)) = 2 := by
    simpa only [peanoCubic] using
      (pin5_integral (sourceF L ω) (sourceF_C3 hL ω) r (ne_of_gt hr)).symm.trans hpin
  have hbound (y : ℝ) : |iteratedDeriv 2 (iteratedDeriv 3 (sourceF L ω)) y| ≤
      sourceDerivativeMajorant L 5 ω := by
    rw [iteratedDeriv_iteratedDeriv]
    exact sourceF_iteratedDeriv_abs_le hL ω 5 y
  have hb := symmetric_cubic_pin_second_order (iteratedDeriv 3 (sourceF L ω))
    (sourceF_third_continuous hL ω) r (sourceAxialThird L ω) (sourceRawU L ω 3)
    (sourceDerivativeMajorant L 5 ω) (sourceDerivativeMajorant_nonneg L 5 ω) hpeano
    (by
      intro u hu
      have ht := scalar_taylor_one_bound (iteratedDeriv 3 (sourceF L ω))
        (smooth_iteratedDeriv _ (sourceF_smooth hL ω) 3) _ hbound (r*u)
      rw [sourceF_third_zero hL ω] at ht
      have hd : deriv (iteratedDeriv 3 (sourceF L ω)) 0 = sourceRawU L ω 3 := by
        rw [← iteratedDeriv_succ]
        exact sourceF_fourth_zero hL ω
      rw [hd] at ht
      convert ht using 1
      ring)
  simpa only [mul_comm] using hb

private theorem endpoint_derivative_low (v : ℝ → ℝ) (hv : ContDiff ℝ (⊤ : ℕ∞) v)
    (G : ℝ) (hG : ∀ y, |iteratedDeriv 4 v y| ≤ G) (r : ℝ) (hr : 0 < r)
    (hp : v (r/2) = 0) (hm : v (-r/2) = 0) :
    |v 0 + iteratedDeriv 2 v 0*r^2/8| ≤ G*r^4/384 ∧
    |deriv v 0 + iteratedDeriv 3 v 0*r^2/24| ≤ G*r^3/192 := by
  apply endpoint_taylor_low_coefficients v r G (v 0) (deriv v 0)
    (iteratedDeriv 2 v 0) (iteratedDeriv 3 v 0) hr hp hm
  · have hb := scalar_taylor_three_bound v hv G hG (r/2)
    convert hb using 1
    · congr 1; ring
    · ring
  · have hb := scalar_taylor_three_bound v hv G hG (-r/2)
    convert hb using 1
    · congr 1; ring
    · ring

/-- The literal low derivatives forced by the physical pins, using actual
fifth derivative bounds rather than any assumed Taylor remainder. -/
theorem source_low_pin_coefficients {L : ℝ} (hL : L ≠ 0) (r : ℝ) (hr : 0 < r)
    (ω : SmoothSample 2 L) (hp : sourcePhysicalPins L r ω) :
    |fderiv ℝ (smoothSourceField 2 L ω) 0 directionX + r^2/4| ≤
      (11/1920 : ℝ)*sourceDerivativeMajorant L 5 ω*r^4 ∧
    |fderiv ℝ (smoothSourceField 2 L ω) 0 directionY + sourceRawU L ω 0*r^2/8| ≤
      sourceDerivativeMajorant L 5 ω*r^4/384 ∧
    |iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω) 0 ![directionX,directionX] +
      sourceRawU L ω 3*r^2/24| ≤ sourceDerivativeMajorant L 5 ω*r^3/192 ∧
    |iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω) 0 ![directionX,directionY] +
      sourceRawU L ω 4*r^2/24| ≤ sourceDerivativeMajorant L 5 ω*r^3/192 := by
  have h0 : (![0,0] : Fin 2 → ℝ) = 0 := by ext i; fin_cases i <;> rfl
  have hfxs : ContDiff ℝ (⊤ : ℕ∞) (deriv (sourceF L ω)) := by
    simpa only [iteratedDeriv_one] using smooth_iteratedDeriv _ (sourceF_smooth hL ω) 1
  have hfx4 (y : ℝ) : |iteratedDeriv 4 (deriv (sourceF L ω)) y| ≤
      sourceDerivativeMajorant L 5 ω := by
    rw [← iteratedDeriv_succ']
    exact sourceF_iteratedDeriv_abs_le hL ω 5 y
  have hfp := sourceF_deriv_pins hL r ω hp
  have hbX := endpoint_derivative_low _ hfxs _ hfx4 r hr hfp.2 hfp.1
  have h2 : iteratedDeriv 2 (deriv (sourceF L ω)) = iteratedDeriv 3 (sourceF L ω) :=
    (iteratedDeriv_succ' (n := 2)).symm
  have h3 : iteratedDeriv 3 (deriv (sourceF L ω)) = iteratedDeriv 4 (sourceF L ω) :=
    (iteratedDeriv_succ' (n := 3)).symm
  have hB : deriv (deriv (sourceF L ω)) 0 = iteratedDeriv 2 (sourceF L ω) 0 := by
    rw [show 2 = 1+1 from rfl, iteratedDeriv_succ, iteratedDeriv_one]
  rw [h2,h3,hB,sourceF_third_zero hL ω,sourceF_fourth_zero hL ω] at hbX
  have hax : |sourceAxialThird L ω-2| ≤ sourceDerivativeMajorant L 5 ω*r^2/40 := by
    simpa only [mul_comm] using source_axial_third_error hL r hr ω hp
  have hfx := corrected_axial_constant r (sourceDerivativeMajorant L 5 ω)
    (deriv (sourceF L ω) 0) (sourceAxialThird L ω) hbX.1 hax
  have hHy := sourceH_pins L r ω hp
  have hbY := endpoint_derivative_low _ (sourceH_smooth hL ω) _
    (sourceH_iteratedDeriv_abs_le hL ω 4) r hr hHy.2 hHy.1
  rw [sourceH_second_zero hL ω,sourceH_third_zero hL ω] at hbY
  have hfx0 := sourceF_deriv hL ω 0
  have hfxx0 := sourceF_second hL ω 0
  have hfxy0 := sourceH_deriv hL ω 0
  rw [h0] at hfx0 hfxx0 hfxy0
  have hfy0 : sourceH L ω 0 = fderiv ℝ (smoothSourceField 2 L ω) 0 directionY := by
    change fderiv ℝ (smoothSourceField 2 L ω) ![0,0] directionY = _
    rw [h0]
  rw [hfx0] at hfx
  rw [hfxx0] at hbX
  rw [hfy0,hfxy0] at hbY
  exact ⟨hfx,hbY.1,hbX.2,hbY.2⟩

end I4SourcePinPreservingQuartic
