import SourcePinPreservingQuartic

noncomputable section
open I4SmoothCarrier I4SourceConfluentPins I4SourcePinCurvatureBounds
open I4SourcePinPreservingQuartic
set_option autoImplicit false

namespace I4SourcePinPreservingQuartic

theorem sourceGradientTaylorRaw_sub_quartic_zero {L : ℝ} (hL : L ≠ 0)
    (r : ℝ) (hr : r ≠ 0) (ω : SmoothSample 2 L) (p : Fin 2 → ℝ) :
    sourceGradientTaylorRaw L r ω p 0 -
      pinPreservingQuartic r (sourceQ L ω) (sourceRawU L ω) p 0 =
      (fderiv ℝ (smoothSourceField 2 L ω) 0 directionX+r^2/4)/r^2 +
      (iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω) 0 ![directionX,directionX]+
        sourceRawU L ω 3*r^2/24)/r*p 0 +
      (iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω) 0 ![directionX,directionY]+
        sourceRawU L ω 4*r^2/24)/r*p 1 +
      (sourceAxialThird L ω-2)*(p 0)^2/2 := by
  have h2 := source_second_p_basis hL ω (r • p) 0
  simp only [Matrix.cons_val_zero] at h2
  unfold sourceGradientTaylorRaw
  rw [coordinateDirection_zero]
  change (fderiv ℝ (smoothSourceField 2 L ω) 0 directionX +
    iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω) 0 ![r • p,directionX] +
    iteratedFDeriv ℝ 3 (smoothSourceField 2 L ω) 0 ![r • p,r • p,directionX]/2 +
    iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![r • p,r • p,r • p,directionX]/6)/r^2 - _ = _
  rw [h2,source_third_ppx_expansion hL ω,source_fourth_pppx_expansion hL ω]
  simp only [Pi.smul_apply,smul_eq_mul,pinPreservingQuartic,Matrix.cons_val_zero]
  field_simp [hr]
  ring

theorem sourceGradientTaylorRaw_sub_quartic_one {L : ℝ} (hL : L ≠ 0)
    (r : ℝ) (hr : r ≠ 0) (ω : SmoothSample 2 L) (p : Fin 2 → ℝ) :
    sourceGradientTaylorRaw L r ω p 1 -
      pinPreservingQuartic r (sourceQ L ω) (sourceRawU L ω) p 1 =
      (fderiv ℝ (smoothSourceField 2 L ω) 0 directionY+sourceRawU L ω 0*r^2/8)/r^2 +
      (iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω) 0 ![directionX,directionY]+
        sourceRawU L ω 4*r^2/24)/r*p 0 := by
  have h2 := source_second_p_basis hL ω (r • p) 1
  simp only [Matrix.cons_val_one,Matrix.cons_val_zero] at h2
  unfold sourceGradientTaylorRaw
  rw [coordinateDirection_one]
  change (fderiv ℝ (smoothSourceField 2 L ω) 0 directionY +
    iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω) 0 ![r • p,directionY] +
    iteratedFDeriv ℝ 3 (smoothSourceField 2 L ω) 0 ![r • p,r • p,directionY]/2 +
    iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![r • p,r • p,r • p,directionY]/6)/r^2 - _ = _
  rw [h2,source_third_ppy_expansion hL ω,source_fourth_pppy_expansion hL ω]
  simp only [Pi.smul_apply,smul_eq_mul,pinPreservingQuartic,Matrix.cons_val_one,Matrix.cons_val_zero]
  field_simp [hr]
  ring

private theorem source_second_transpose {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) :
    iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω) 0 ![directionY,directionX] =
      iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω) 0 ![directionX,directionY] := by
  have hw : (![directionX,directionY] ∘ Equiv.swap (0 : Fin 2) 1) =
      ![directionY,directionX] := by ext i; fin_cases i <;> rfl
  simpa only [hw] using source_derivative_comp_perm hL ω 2 0
    ![directionX,directionY] (Equiv.swap 0 1)

private theorem coordinateDirection_eq_array (i : Fin 2) :
    coordinateDirection i = ![directionX,directionY] i := by
  fin_cases i <;> simp [directionX,directionY]

theorem sourceHessianTaylor_sub_quarticJacobian {L : ℝ} (hL : L ≠ 0)
    (r : ℝ) (hr : r ≠ 0) (ω : SmoothSample 2 L) (p : Fin 2 → ℝ) :
    sourceHessianTaylor L r ω p -
      pinPreservingJacobian r (sourceQ L ω) (sourceRawU L ω) p =
      !![(iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω) 0 ![directionX,directionX]+
            sourceRawU L ω 3*r^2/24)/r + (sourceAxialThird L ω-2)*p 0,
          (iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω) 0 ![directionX,directionY]+
            sourceRawU L ω 4*r^2/24)/r;
          (iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω) 0 ![directionX,directionY]+
            sourceRawU L ω 4*r^2/24)/r,0] := by
  ext i j
  simp only [Matrix.sub_apply,sourceHessianTaylor,coordinateDirection_eq_array,
    source_third_p_basis_basis hL ω,source_fourth_pp_basis_basis hL ω]
  fin_cases i <;> fin_cases j <;>
    simp only [pinPreservingJacobian,Matrix.of_apply,Matrix.cons_val_zero,Matrix.cons_val_one,
      Fin.reduceFinMk,Pi.smul_apply,smul_eq_mul,source_second_transpose hL ω,sourceQ] <;>
    field_simp [hr] <;> ring

end I4SourcePinPreservingQuartic
