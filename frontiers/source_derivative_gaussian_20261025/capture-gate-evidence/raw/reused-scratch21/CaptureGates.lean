import GeometrySupport
import CaptureAlgebra

noncomputable section
open I4SourcePinPreservingQuartic
set_option autoImplicit false

namespace I4QuarticCaptureAlgebra

private theorem width_identity (r : ℝ) (U : Fin 8 → ℝ) :
    (quarticK0*rawRadius U^5)*captureWidth r U = quarticFstar r U := by
  have hR := rawRadius_pos U
  unfold captureWidth quarticWidth
  field_simp [hR.ne',show quarticK0 ≠ 0 by norm_num [quarticK0]]

private theorem transverse_decomposition (r q X Y : ℝ) (U : Fin 8 → ℝ) :
    pinPreservingQuartic r q U ![X,Y] 1 =
      (q/r)*Y + ((U 0/2)*(X^2-1/4)+r*(U 4/6)*X*(X^2-1/4)) +
      (U 1*X*Y+(U 2/2)*Y^2+
        r*((U 5/2)*X^2*Y+(U 6/2)*X*Y^2+(U 7/6)*Y^3)) := by
  simp only [pinPreservingQuartic,Matrix.cons_val_zero,Matrix.cons_val_one]
  ring

/-- LM001 Q2, upper horizontal strip boundary, with its original literal polynomial. -/
theorem quartic_strip_upper (r q : ℝ) (U : Fin 8 → ℝ)
    (hr : 0 < r) (hr1 : r ≤ 1)
    (hs : q/r ≤ -(2*quarticK0*rawRadius U^5+2*rawRadius U))
    (X : ℝ) (hX : |X| ≤ 1/2) :
    pinPreservingQuartic r q U ![X,captureWidth r U] 1 ≤ -1 := by
  have hW := captureWidth_pos r U hr.le
  have hR := rawRadius_pos U
  have hforce := quartic_transverse_forcing_bound r hr.le U X hX
  have hrem := quartic_transverse_remainder_bound r (rawRadius U) (captureWidth r U) X
    (captureWidth r U) U hr.le hr1 hR.le hW.le
    (captureWidth_le_one_sixteenth r U hr1) (rawRadius_coord_abs_le U) hX
    (by rw [abs_of_pos hW])
  have hf := (le_abs_self _).trans hforce
  have he := (le_abs_self _).trans hrem
  have hscalar := mul_le_mul_of_nonneg_right hs hW.le
  have hid := width_identity r U
  have hF := one_le_quarticFstar r hr.le U
  rw [transverse_decomposition]
  nlinarith

/-- LM001 Q2, lower horizontal strip boundary. -/
theorem quartic_strip_lower (r q : ℝ) (U : Fin 8 → ℝ)
    (hr : 0 < r) (hr1 : r ≤ 1)
    (hs : q/r ≤ -(2*quarticK0*rawRadius U^5+2*rawRadius U))
    (X : ℝ) (hX : |X| ≤ 1/2) :
    1 ≤ pinPreservingQuartic r q U ![X,-captureWidth r U] 1 := by
  have hW := captureWidth_pos r U hr.le
  have hR := rawRadius_pos U
  have hforce := quartic_transverse_forcing_bound r hr.le U X hX
  have hrem := quartic_transverse_remainder_bound r (rawRadius U) (captureWidth r U) X
    (-captureWidth r U) U hr.le hr1 hR.le hW.le
    (captureWidth_le_one_sixteenth r U hr1) (rawRadius_coord_abs_le U) hX
    (by rw [abs_neg,abs_of_pos hW])
  have hf := (neg_le_abs _).trans hforce
  have he := (neg_le_abs _).trans hrem
  have hscalar := mul_le_mul_of_nonneg_right hs hW.le
  have hid := width_identity r U
  have hF := one_le_quarticFstar r hr.le U
  rw [transverse_decomposition]
  nlinarith

/-- LM001 Q3, strict leftward central transit; only REG is needed here. -/
theorem quartic_central_transit (r q : ℝ) (U : Fin 8 → ℝ)
    (hr : 0 < r) (hr1 : r ≤ 1) (hreg : regular r U)
    (X Y : ℝ) (hX : |X| ≤ 1/2-captureSigma r U)
    (hY : |Y| ≤ captureWidth r U) :
    pinPreservingQuartic r q U ![X,Y] 0 ≤ -3*rawRadius U*captureWidth r U ∧
      -3*rawRadius U*captureWidth r U < 0 := by
  have hW := captureWidth_pos r U hr.le
  have hR := rawRadius_pos U
  have hσ := captureSigma_pos r U hr.le
  have hσsmall := captureSigma_le r U hr1
  have hXstrip : |X| ≤ 1/2 := by linarith
  have hErr := quartic_axial_remainder_bound r (rawRadius U) (captureWidth r U) X Y U
    hr.le hr1 hR.le hW.le (captureWidth_le_one_sixteenth r U hr1)
    (capture_r_le_width r U hr hreg) (rawRadius_coord_abs_le U) hXstrip hY
  have hX2 : X^2 ≤ (1/2-captureSigma r U)^2 := by
    nlinarith [sq_abs X,abs_nonneg X]
  have hσ2 : (captureSigma r U)^2 ≤ captureSigma r U/16 := by
    nlinarith
  have hbase : X^2-1/4 ≤ -(15/4)*rawRadius U*captureWidth r U := by
    unfold captureSigma at *
    nlinarith
  have he := (le_abs_self _).trans hErr
  constructor
  · simp only [pinPreservingQuartic,Matrix.cons_val_zero,Matrix.cons_val_one]
    nlinarith
  · nlinarith [mul_pos hR hW]

end I4QuarticCaptureAlgebra
