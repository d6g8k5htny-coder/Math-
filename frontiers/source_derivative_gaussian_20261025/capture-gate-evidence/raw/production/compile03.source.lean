import SourcePinPreservingQuartic
import Mathlib.Tactic.GCongr

/-! Exact LM001 polynomial strip/transit inequalities and their actual-source
transfer. Generic geometry was authored by /root/uniform_jet_moment_sources;
the forcing, polynomial gates and actual transfer by /root/regression_kernel.
Frozen scratch proofs and their successful checks are reused; this new module
adds the actual-source gate join. No selected-flow/capture theorem is asserted. -/

noncomputable section
open I4SmoothCarrier I4SourceConfluentPins I4SourcePinCurvatureBounds
open I4SourceConditionalMajorant I4SourceSmoothPalm I4SourceSmoothConditional
open I4SourcePinPreservingQuartic MeasureTheory
open scoped BigOperators
set_option autoImplicit false

namespace I4QuarticCaptureAlgebra


def rawRadius (U : Fin 8 → ℝ) : ℝ := 1 + ∑ i, |U i|

def regular (r : ℝ) (U : Fin 8 → ℝ) : Prop :=
  r * rawRadius U ^ 5 ≤ 1 / (1024 * quarticK0)

def captureWidth (r : ℝ) (U : Fin 8 → ℝ) : ℝ := quarticWidth r U (rawRadius U)

def captureSigma (r : ℝ) (U : Fin 8 → ℝ) : ℝ := 4 * rawRadius U * captureWidth r U

theorem rawRadius_one_le (U : Fin 8 → ℝ) : 1 ≤ rawRadius U := by
  have h : 0 ≤ ∑ i, |U i| := Finset.sum_nonneg (fun _ _ => abs_nonneg _)
  unfold rawRadius
  linarith

theorem rawRadius_pos (U : Fin 8 → ℝ) : 0 < rawRadius U :=
  lt_of_lt_of_le (by norm_num) (rawRadius_one_le U)

theorem rawRadius_sum_abs_eq (U : Fin 8 → ℝ) : ∑ i, |U i| = rawRadius U - 1 := by
  unfold rawRadius
  ring

theorem rawRadius_coord_abs_le_sub_one (U : Fin 8 → ℝ) (i : Fin 8) :
    |U i| ≤ rawRadius U - 1 := by
  rw [← rawRadius_sum_abs_eq]
  exact Finset.single_le_sum (fun j (_ : j ∈ (Finset.univ : Finset (Fin 8))) =>
    abs_nonneg (U j)) (Finset.mem_univ i)

theorem rawRadius_coord_abs_le (U : Fin 8 → ℝ) (i : Fin 8) : |U i| ≤ rawRadius U := by
  linarith [rawRadius_coord_abs_le_sub_one U i]

theorem captureWidth_pos (r : ℝ) (U : Fin 8 → ℝ) (hr : 0 ≤ r) :
    0 < captureWidth r U := quarticWidth_pos r _ hr (rawRadius_one_le U) U

theorem captureFstar_le_radius (r : ℝ) (U : Fin 8 → ℝ) (hr1 : r ≤ 1) :
    quarticFstar r U ≤ 2 * rawRadius U := by
  have h0 := rawRadius_coord_abs_le U 0
  have h4 := rawRadius_coord_abs_le U 4
  have hR := rawRadius_one_le U
  have hm : r * |U 4| ≤ |U 4| := mul_le_of_le_one_left (abs_nonneg _) hr1
  unfold quarticFstar
  linarith

theorem captureWidth_radius_le (r : ℝ) (U : Fin 8 → ℝ) (hr1 : r ≤ 1) :
    rawRadius U * captureWidth r U ≤ 1 / 2048 := by
  have hR := rawRadius_one_le U
  have hR0 : 0 ≤ rawRadius U := (by norm_num : (0 : ℝ) ≤ 1).trans hR
  have hF := captureFstar_le_radius r U hr1
  have hpow : rawRadius U ^ 2 ≤ rawRadius U ^ 5 := pow_le_pow_right₀ hR (by norm_num)
  have hm := mul_le_mul_of_nonneg_left hF hR0
  have hden : 0 < quarticK0 * rawRadius U ^ 5 :=
    mul_pos (by norm_num [quarticK0]) (pow_pos (rawRadius_pos U) 5)
  calc
    _ = (rawRadius U * quarticFstar r U) / (quarticK0 * rawRadius U ^ 5) := by
      unfold captureWidth quarticWidth
      ring
    _ ≤ 1 / 2048 := by
      apply (div_le_iff₀ hden).mpr
      norm_num only [quarticK0]
      nlinarith

theorem captureWidth_le (r : ℝ) (U : Fin 8 → ℝ) (hr1 : r ≤ 1) :
    captureWidth r U ≤ 1 / 2048 :=
  (certificate_width_geometry _ _ (rawRadius_one_le U) (captureWidth_radius_le r U hr1)).1

theorem captureWidth_le_one_sixteenth (r : ℝ) (U : Fin 8 → ℝ) (hr1 : r ≤ 1) :
    captureWidth r U ≤ 1 / 16 := by
  linarith [captureWidth_le r U hr1]

theorem captureWidth_radius_le_one_sixtyfourth (r : ℝ) (U : Fin 8 → ℝ) (hr1 : r ≤ 1) :
    rawRadius U * captureWidth r U ≤ 1 / 64 := by
  linarith [captureWidth_radius_le r U hr1]

theorem capture_r_le_width (r : ℝ) (U : Fin 8 → ℝ) (hr : 0 < r)
    (hreg : regular r U) : r ≤ captureWidth r U / 1024 := by
  have hden : 0 < quarticK0 * rawRadius U ^ 5 :=
    mul_pos (by norm_num [quarticK0]) (pow_pos (rawRadius_pos U) 5)
  have hF := one_le_quarticFstar r hr.le U
  have hb : (r * rawRadius U ^ 5) * (1024 * quarticK0) ≤ 1 :=
    (le_div_iff₀ (by norm_num [quarticK0] : (0 : ℝ) < 1024 * quarticK0)).mp hreg
  apply (le_div_iff₀ (by norm_num : (0 : ℝ) < 1024)).mpr
  unfold captureWidth quarticWidth
  apply (le_div_iff₀ hden).mpr
  calc
    _ = (r * rawRadius U ^ 5) * (1024 * quarticK0) := by ring
    _ ≤ 1 := hb
    _ ≤ quarticFstar r U := hF

theorem captureSigma_pos (r : ℝ) (U : Fin 8 → ℝ) (hr : 0 ≤ r) :
    0 < captureSigma r U := by
  unfold captureSigma
  exact mul_pos (mul_pos (by norm_num) (rawRadius_pos U)) (captureWidth_pos r U hr)

theorem captureSigma_le (r : ℝ) (U : Fin 8 → ℝ) (hr1 : r ≤ 1) :
    captureSigma r U ≤ 1 / 512 := by
  unfold captureSigma
  linarith [captureWidth_radius_le r U hr1]

theorem four_captureWidth_le_captureSigma (r : ℝ) (U : Fin 8 → ℝ) (hr : 0 ≤ r) :
    4 * captureWidth r U ≤ captureSigma r U := by
  have h := mul_le_mul_of_nonneg_right (rawRadius_one_le U) (captureWidth_pos r U hr).le
  unfold captureSigma
  nlinarith



/-- Elementary monomial bounds used only by the first formalization of LM001 Q2/Q3. -/
private theorem abs_mul_three_le {a x y A B C : ℝ}
    (ha : |a| ≤ A) (hx : |x| ≤ B) (hy : |y| ≤ C) :
    |a*x*y| ≤ A*B*C := by
  have hA : 0 ≤ A := (abs_nonneg a).trans ha
  have hB : 0 ≤ B := (abs_nonneg x).trans hx
  rw [abs_mul,abs_mul]
  gcongr

private theorem abs_mul_two_le {a x A B : ℝ}
    (ha : |a| ≤ A) (hx : |x| ≤ B) : |a*x| ≤ A*B := by
  have hA : 0 ≤ A := (abs_nonneg a).trans ha
  rw [abs_mul]
  gcongr

private theorem abs_add_six_le (a b c d e f A B C D E F : ℝ)
    (ha : |a| ≤ A) (hb : |b| ≤ B) (hc : |c| ≤ C)
    (hd : |d| ≤ D) (he : |e| ≤ E) (hf : |f| ≤ F) :
    |a+b+c+d+e+f| ≤ A+B+C+D+E+F := by
  have h1 := abs_add_le a b
  have h2 := abs_add_le (a+b) c
  have h3 := abs_add_le (a+b+c) d
  have h4 := abs_add_le (a+b+c+d) e
  have h5 := abs_add_le (a+b+c+d+e) f
  linarith

private theorem abs_add_five_le (a b c d e A B C D E : ℝ)
    (ha : |a| ≤ A) (hb : |b| ≤ B) (hc : |c| ≤ C)
    (hd : |d| ≤ D) (he : |e| ≤ E) :
    |a+b+c+d+e| ≤ A+B+C+D+E := by
  have h1 := abs_add_le a b
  have h2 := abs_add_le (a+b) c
  have h3 := abs_add_le (a+b+c) d
  have h4 := abs_add_le (a+b+c+d) e
  linarith

private theorem strip_coordinate_bounds {X Y W : ℝ}
    (hX : |X| ≤ 1/2) (hW0 : 0 ≤ W) (hW : W ≤ 1/16) (hY : |Y| ≤ W) :
    |X^2-1/4| ≤ 1/4 ∧ |X*(X^2-1/4)| ≤ 1/8 ∧
    |3*X^2-1/4| ≤ 1/2 ∧ |X^2| ≤ 1/4 ∧ |Y^2| ≤ W/16 ∧ |Y^3| ≤ W/256 := by
  have hX2 : X^2 ≤ 1/4 := by nlinarith [sq_abs X,abs_nonneg X]
  have hbase : |X^2-1/4| ≤ 1/4 := abs_le.mpr ⟨by nlinarith [sq_nonneg X],by nlinarith⟩
  have hxb : |X*(X^2-1/4)| ≤ 1/8 := by
    calc
      _ ≤ (1/2)*(1/4) := abs_mul_two_le hX hbase
      _ = _ := by norm_num
  have hmix : |3*X^2-1/4| ≤ 1/2 := abs_le.mpr ⟨by nlinarith [sq_nonneg X],by nlinarith⟩
  have hY2 : |Y^2| ≤ W^2 := by simpa only [abs_pow] using pow_le_pow_left₀ (abs_nonneg Y) hY 2
  have hW2 : W^2 ≤ W/16 := by nlinarith
  have hY3 : |Y^3| ≤ W/256 := by
    calc
      |Y^3| = |Y| * |Y^2| := by rw [show Y^3=Y*Y^2 by ring,abs_mul]
      _ ≤ W*(W/16) := mul_le_mul hY (hY2.trans hW2) (abs_nonneg _) hW0
      _ ≤ W/256 := by nlinarith
  exact ⟨hbase,hxb,hmix,by simpa [abs_of_nonneg (sq_nonneg X)] using hX2,hY2.trans hW2,hY3⟩

/-- The transverse forcing independent of Y is at most Fstar-1. -/
theorem quartic_transverse_forcing_bound (r : ℝ) (hr : 0 ≤ r) (U : Fin 8 → ℝ)
    (X : ℝ) (hX : |X| ≤ 1/2) :
    |(U 0/2)*(X^2-1/4) + r*(U 4/6)*X*(X^2-1/4)| ≤ quarticFstar r U-1 := by
  have hb := (strip_coordinate_bounds hX (show (0:ℝ)≤0 by norm_num)
    (show (0:ℝ)≤1/16 by norm_num) (show |(0:ℝ)|≤0 by norm_num))
  have h0 : |(U 0/2)*(X^2-1/4)| ≤ |U 0|/8 := by
    calc
      _ = |U 0|/2*|X^2-1/4| := by rw [abs_mul,abs_div]; norm_num
      _ ≤ |U 0|/2*(1/4) := mul_le_mul_of_nonneg_left hb.1 (by positivity)
      _ = _ := by ring
  have h4 : |r*(U 4/6)*X*(X^2-1/4)| ≤ r*|U 4|/48 := by
    calc
      _ = r*|U 4|/6*|X*(X^2-1/4)| := by rw [show r*(U 4/6)*X*(X^2-1/4)=(r*(U 4/6))*(X*(X^2-1/4)) by ring,abs_mul,abs_mul,abs_of_nonneg hr,abs_div]; norm_num only; ring
      _ ≤ r*|U 4|/6*(1/8) := mul_le_mul_of_nonneg_left hb.2.1 (by positivity)
      _ = _ := by ring
  have hs := abs_add_le ((U 0/2)*(X^2-1/4)) (r*(U 4/6)*X*(X^2-1/4))
  unfold quarticFstar
  linarith

private theorem abs_mul_four_le {a x y z A B C D : ℝ}
    (ha : |a| ≤ A) (hx : |x| ≤ B) (hy : |y| ≤ C) (hz : |z| ≤ D) :
    |a*x*y*z| ≤ A*B*C*D :=
  abs_mul_two_le (abs_mul_three_le ha hx hy) hz

/-- Uniform transverse Y-dependent error on the horizontal strip. -/
theorem quartic_transverse_remainder_bound (r R W X Y : ℝ) (U : Fin 8 → ℝ)
    (hr : 0 ≤ r) (hr1 : r ≤ 1) (hR : 0 ≤ R) (hW0 : 0 ≤ W) (hW : W ≤ 1/16)
    (hU : ∀ i, |U i| ≤ R) (hX : |X| ≤ 1/2) (hY : |Y| ≤ W) :
    |U 1*X*Y+(U 2/2)*Y^2+
      r*((U 5/2)*X^2*Y+(U 6/2)*X*Y^2+(U 7/6)*Y^3)| ≤ 2*R*W := by
  have hb := strip_coordinate_bounds hX hW0 hW hY
  have hrabs : |r| ≤ 1 := by rwa [abs_of_nonneg hr]
  have t1 : |U 1*X*Y| ≤ R*W/2 := by
    have h := abs_mul_three_le (hU 1) hX hY
    nlinarith
  have t2 : |(U 2/2)*Y^2| ≤ R*W/32 := by
    have h := abs_mul_two_le (hU 2) hb.2.2.2.2.1
    rw [show (U 2/2)*Y^2=(U 2*Y^2)/2 by ring,abs_div]
    norm_num only
    nlinarith
  have t3 : |r*(U 5/2)*X^2*Y| ≤ R*W/8 := by
    have h := abs_mul_four_le hrabs (hU 5) hb.2.2.2.1 hY
    rw [show r*(U 5/2)*X^2*Y=(r*U 5*X^2*Y)/2 by ring,abs_div]
    norm_num only
    nlinarith
  have t4 : |r*(U 6/2)*X*Y^2| ≤ R*W/64 := by
    have h := abs_mul_four_le hrabs (hU 6) hX hb.2.2.2.2.1
    rw [show r*(U 6/2)*X*Y^2=(r*U 6*X*Y^2)/2 by ring,abs_div]
    norm_num only
    nlinarith
  have t5 : |r*(U 7/6)*Y^3| ≤ R*W/1536 := by
    have h := abs_mul_three_le hrabs (hU 7) hb.2.2.2.2.2
    rw [show r*(U 7/6)*Y^3=(r*U 7*Y^3)/6 by ring,abs_div]
    norm_num only
    nlinarith
  have hs := abs_add_five_le _ _ _ _ _ _ _ _ _ _ t1 t2 t3 t4 t5
  rw [show U 1*X*Y+(U 2/2)*Y^2+
      r*((U 5/2)*X^2*Y+(U 6/2)*X*Y^2+(U 7/6)*Y^3) =
      U 1*X*Y+(U 2/2)*Y^2+r*(U 5/2)*X^2*Y+
      r*(U 6/2)*X*Y^2+r*(U 7/6)*Y^3 by ring]
  nlinarith [mul_nonneg hR hW0]

/-- Absolute X-error around the central model X²-1/4. -/
theorem quartic_axial_remainder_bound (r R W X Y : ℝ) (U : Fin 8 → ℝ)
    (hr : 0 ≤ r) (hr1 : r ≤ 1) (hR : 0 ≤ R) (hW0 : 0 ≤ W) (hW : W ≤ 1/16)
    (hrW : r ≤ W/1024) (hU : ∀ i, |U i| ≤ R)
    (hX : |X| ≤ 1/2) (hY : |Y| ≤ W) :
    |U 0*X*Y+(U 1/2)*Y^2+
      r*((U 3/6)*X*(X^2-1/4)+(U 4/6)*(3*X^2-1/4)*Y+
        (U 5/2)*X*Y^2+(U 6/6)*Y^3)| ≤ (3/4)*R*W := by
  have hb := strip_coordinate_bounds hX hW0 hW hY
  have hrabs : |r| ≤ 1 := by rwa [abs_of_nonneg hr]
  have t1 : |U 0*X*Y| ≤ R*W/2 := by
    have h := abs_mul_three_le (hU 0) hX hY
    nlinarith
  have t2 : |(U 1/2)*Y^2| ≤ R*W/32 := by
    have h := abs_mul_two_le (hU 1) hb.2.2.2.2.1
    rw [show (U 1/2)*Y^2=(U 1*Y^2)/2 by ring,abs_div]
    norm_num only
    nlinarith
  have t3 : |r*(U 3/6)*X*(X^2-1/4)| ≤ R*W/49152 := by
    have hrabsW : |r| ≤ W/1024 := by rwa [abs_of_nonneg hr]
    have h := abs_mul_three_le hrabsW (hU 3) hb.2.1
    rw [show r*(U 3/6)*X*(X^2-1/4)=(r*U 3*(X*(X^2-1/4)))/6 by ring,abs_div]
    norm_num only
    nlinarith
  have t4 : |r*(U 4/6)*(3*X^2-1/4)*Y| ≤ R*W/12 := by
    have h := abs_mul_four_le hrabs (hU 4) hb.2.2.1 hY
    rw [show r*(U 4/6)*(3*X^2-1/4)*Y=(r*U 4*(3*X^2-1/4)*Y)/6 by ring,abs_div]
    norm_num only
    nlinarith
  have t5 : |r*(U 5/2)*X*Y^2| ≤ R*W/64 := by
    have h := abs_mul_four_le hrabs (hU 5) hX hb.2.2.2.2.1
    rw [show r*(U 5/2)*X*Y^2=(r*U 5*X*Y^2)/2 by ring,abs_div]
    norm_num only
    nlinarith
  have t6 : |r*(U 6/6)*Y^3| ≤ R*W/1536 := by
    have h := abs_mul_three_le hrabs (hU 6) hb.2.2.2.2.2
    rw [show r*(U 6/6)*Y^3=(r*U 6*Y^3)/6 by ring,abs_div]
    norm_num only
    nlinarith
  have hs := abs_add_six_le _ _ _ _ _ _ _ _ _ _ _ _ t1 t2 t3 t4 t5 t6
  rw [show U 0*X*Y+(U 1/2)*Y^2+
      r*((U 3/6)*X*(X^2-1/4)+(U 4/6)*(3*X^2-1/4)*Y+
        (U 5/2)*X*Y^2+(U 6/6)*Y^3) =
      U 0*X*Y+(U 1/2)*Y^2+r*(U 3/6)*X*(X^2-1/4)+
      r*(U 4/6)*(3*X^2-1/4)*Y+r*(U 5/2)*X*Y^2+r*(U 6/6)*Y^3 by ring]
  nlinarith [mul_nonneg hR hW0]



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



/-- Euclidean value error controls every scalar component without a norm-convention change. -/
theorem euclidean_component_error_le (v w : SourcePlane) (η : ℝ)
    (h : ‖v-w‖ ≤ η) (i : Fin 2) : |v i-w i| ≤ η := by
  have hi := PiLp.norm_apply_le (v-w) i
  exact (show |v i-w i| ≤ ‖v-w‖ by simpa using hi).trans h

/-- The entire adaptive rectangle lies in the exact comparison ball. -/
theorem capture_strip_in_ball_two (r : ℝ) (U : Fin 8 → ℝ) (hr1 : r ≤ 1)
    (X Y : ℝ) (hX : |X| ≤ 1/2) (hY : |Y| ≤ captureWidth r U) :
    ‖(WithLp.toLp 2 ![X,Y] : SourcePlane)‖ ≤ 2 :=
  quartic_strip_in_ball_two _ (captureWidth_le r U hr1) _ (by simpa using hX) (by simpa using hY)

/-- This is the value-coordinate projection of the qualified maximum C1 tolerance. -/
theorem source_component_error_le {L : ℝ} (hL : L ≠ 0) (r : ℝ)
    (hr : 0 < r) (hr1 : r ≤ 1) (ω : SmoothSample 2 L)
    (hp : sourcePhysicalPins L r ω)
    (hcut : r*sourceGammaRadius L ω^5 ≤ quarticEpsilonStar)
    (p : Fin 2 → ℝ) (hball : ‖(WithLp.toLp 2 p : SourcePlane)‖ ≤ 2) (i : Fin 2) :
    |sourceScaledGradientRaw L r ω p i-
        pinPreservingQuartic r (sourceQ L ω) (sourceRawU L ω) p i| ≤
      rawRadius (sourceRawU L ω)*captureWidth r (sourceRawU L ω)/4 := by
  have h := (sourceQuartic_cutoff_tolerance hL r hr hr1 ω hp hcut).2
    (WithLp.toLp 2 p) hball
  have hv := (le_max_left _ _).trans h
  have hi := euclidean_component_error_le _ _ _ hv i
  simpa [sourceScaledGradient,sourceQuartic,captureWidth,rawRadius,sourceRawRadius] using hi

/-- Actual inward drift at both horizontal adaptive-strip boundaries. -/
def sourceStripGates (L r : ℝ) (ω : SmoothSample 2 L) : Prop :=
  ∀ X : ℝ, |X| ≤ 1/2 →
    sourceScaledGradientRaw L r ω ![X,captureWidth r (sourceRawU L ω)] 1 < 0 ∧
    0 < sourceScaledGradientRaw L r ω ![X,-captureWidth r (sourceRawU L ω)] 1

/-- Actual central leftward drift with the literal quarter-width error budget. -/
def sourceCentralGate (L r : ℝ) (ω : SmoothSample 2 L) : Prop :=
  ∀ X Y : ℝ, |X| ≤ 1/2-captureSigma r (sourceRawU L ω) →
    |Y| ≤ captureWidth r (sourceRawU L ω) →
    sourceScaledGradientRaw L r ω ![X,Y] 0 ≤
      -(11/4)*rawRadius (sourceRawU L ω)*captureWidth r (sourceRawU L ω) ∧
    -(11/4)*rawRadius (sourceRawU L ω)*captureWidth r (sourceRawU L ω) < 0

/-- The original source regularity and negative-curvature cutoffs imply actual strip signs. -/
theorem source_actual_strip_gates {L : ℝ} (hL : L ≠ 0) (r : ℝ)
    (hr : 0 < r) (hr1 : r ≤ 1) (ω : SmoothSample 2 L)
    (hp : sourcePhysicalPins L r ω)
    (hcut : r*sourceGammaRadius L ω^5 ≤ quarticEpsilonStar)
    (hq : sourceQ L ω ≤ -quarticKcap*r*sourceGammaRadius L ω^5) :
    sourceStripGates L r ω := by
  intro X hX
  have hW := captureWidth_pos r (sourceRawU L ω) hr.le
  have hsize := captureWidth_radius_le r (sourceRawU L ω) hr1
  have hs := sourceQuartic_curvature_threshold hL r hr ω hq
  have hupper := quartic_strip_upper r (sourceQ L ω) (sourceRawU L ω) hr hr1 hs X hX
  have hlower := quartic_strip_lower r (sourceQ L ω) (sourceRawU L ω) hr hr1 hs X hX
  have hYupper : |captureWidth r (sourceRawU L ω)| ≤ captureWidth r (sourceRawU L ω) :=
    (abs_of_pos hW).le
  have hYlower : |-captureWidth r (sourceRawU L ω)| ≤ captureWidth r (sourceRawU L ω) := by
    rw [abs_neg,abs_of_pos hW]
  have heUpper := source_component_error_le hL r hr hr1 ω hp hcut
    ![X,captureWidth r (sourceRawU L ω)]
    (capture_strip_in_ball_two r _ hr1 X _ hX hYupper) 1
  have heLower := source_component_error_le hL r hr hr1 ω hp hcut
    ![X,-captureWidth r (sourceRawU L ω)]
    (capture_strip_in_ball_two r _ hr1 X _ hX hYlower) 1
  constructor
  · have h := (le_abs_self _).trans heUpper
    linarith
  · have h := (neg_le_abs _).trans heLower
    linarith

/-- Central actual drift needs regularity but no transverse-curvature threshold. -/
theorem source_actual_central_gate {L : ℝ} (hL : L ≠ 0) (r : ℝ)
    (hr : 0 < r) (hr1 : r ≤ 1) (ω : SmoothSample 2 L)
    (hp : sourcePhysicalPins L r ω)
    (hcut : r*sourceGammaRadius L ω^5 ≤ quarticEpsilonStar) :
    sourceCentralGate L r ω := by
  intro X Y hX hY
  have hreg := (sourceQuartic_cutoff_tolerance hL r hr hr1 ω hp hcut).1
  have hpoly := quartic_central_transit r (sourceQ L ω) (sourceRawU L ω) hr hr1 hreg X Y hX hY
  have hσ := captureSigma_pos r (sourceRawU L ω) hr.le
  have hXstrip : |X| ≤ 1/2 := by linarith
  have he := source_component_error_le hL r hr hr1 ω hp hcut ![X,Y]
    (capture_strip_in_ball_two r _ hr1 X Y hXstrip hY) 0
  have he' := (le_abs_self _).trans he
  constructor
  · linarith [hpoly.1]
  · linarith [hpoly.2]

/-- Every sufficiently small positive radius has actual base-law gates on the stated cutoff. -/
theorem source_actual_gates_estimates {L : ℝ} (hL : L ≠ 0) (b : ℝ) :
    ∃ δ : ℝ, 0 < δ ∧ δ ≤ 1 ∧ ∀ r : ℝ, 0 < r → r < δ →
      ∀ᵐ ω ∂sourceSmoothLaw hL r b,
        r*sourceGammaRadius L ω^5 ≤ quarticEpsilonStar →
          sourceCentralGate L r ω ∧
          (sourceQ L ω ≤ -quarticKcap*r*sourceGammaRadius L ω^5 → sourceStripGates L r ω) := by
  obtain ⟨δ,hδ,hδ1,hpins⟩ := sourcePhysicalPins_eventually hL b
  refine ⟨δ,hδ,hδ1,?_⟩
  intro r hr hrδ
  have hr1 := hrδ.le.trans hδ1
  filter_upwards [hpins r hr hrδ] with ω hp
  intro hcut
  exact ⟨source_actual_central_gate hL r hr hr1 ω hp hcut,
    source_actual_strip_gates hL r hr hr1 ω hp hcut⟩

/-- The literal weighted carrier density inherits these almost-sure gate implications. -/
theorem source_actual_weighted_gates_estimates {L : ℝ} (hL : L ≠ 0) (b : ℝ) :
    ∃ δ : ℝ, 0 < δ ∧ δ ≤ 1 ∧ ∀ r : ℝ, 0 < r → r < δ →
      ∀ᵐ ω ∂sourceSmoothWeightedLaw hL r b,
        r*sourceGammaRadius L ω^5 ≤ quarticEpsilonStar →
          sourceCentralGate L r ω ∧
          (sourceQ L ω ≤ -quarticKcap*r*sourceGammaRadius L ω^5 → sourceStripGates L r ω) := by
  obtain ⟨δ,hδ,hδ1,hbound⟩ := source_actual_gates_estimates hL b
  refine ⟨δ,hδ,hδ1,?_⟩
  intro r hr hrδ
  exact I4SourceSmoothPalm.prwMeasure_ae_of_ae (sourceSmoothLaw hL r b)
    (sourceSmoothWeight L r) (hbound r hr hrδ)

end I4QuarticCaptureAlgebra
