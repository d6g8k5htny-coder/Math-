import SourcePinPreservingQuartic
import Mathlib.Tactic.GCongr

noncomputable section
open I4SourcePinPreservingQuartic
set_option autoImplicit false

namespace I4QuarticCaptureAlgebra

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

end I4QuarticCaptureAlgebra
