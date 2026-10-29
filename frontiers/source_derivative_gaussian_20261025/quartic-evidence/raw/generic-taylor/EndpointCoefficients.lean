import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring
import Mathlib.Tactic.GCongr

noncomputable section
set_option autoImplicit false

namespace I4ActualQuarticTransfer

/-- Honest cubic Taylor remainders at two exact zero endpoints recover the
constant and linear coefficients, with their half-interval factors. -/
theorem endpoint_taylor_low_coefficients (v : ℝ → ℝ) (r G A B T C : ℝ)
    (hr : 0 < r) (hp : v (r/2) = 0) (hm : v (-r/2) = 0)
    (hTp : |v (r/2) - (A+B*(r/2)+T*(r/2)^2/2+C*(r/2)^3/6)| ≤ G*r^4/384)
    (hTm : |v (-r/2) - (A+B*(-r/2)+T*(-r/2)^2/2+C*(-r/2)^3/6)| ≤ G*r^4/384) :
    |A+T*r^2/8| ≤ G*r^4/384 ∧ |B+C*r^2/24| ≤ G*r^3/192 := by
  rw [hp, zero_sub, abs_neg] at hTp
  rw [hm, zero_sub, abs_neg] at hTm
  obtain ⟨hpL,hpU⟩ := abs_le.mp hTp
  obtain ⟨hmL,hmU⟩ := abs_le.mp hTm
  constructor
  · apply abs_le.mpr
    constructor <;> nlinarith
  · have hodd : |r*(B+C*r^2/24)| ≤ G*r^4/192 := by
      apply abs_le.mpr
      constructor <;> nlinarith
    rw [abs_mul, abs_of_pos hr] at hodd
    apply le_of_mul_le_mul_left _ hr
    calc
      _ ≤ G*r^4/192 := hodd
      _ = _ := by ring

/-- The Peano improvement t=2+O(r²G) gives the corrected axial constant
coefficient 11/1920, rather than an assumed ordinary Taylor coefficient. -/
theorem corrected_axial_constant (r G A T : ℝ)
    (hconst : |A+T*r^2/8| ≤ G*r^4/384)
    (hcubic : |T-2| ≤ G*r^2/40) :
    |A+r^2/4| ≤ (11/1920 : ℝ)*G*r^4 := by
  calc
    _ = |(A+T*r^2/8) + (2-T)*r^2/8| := by congr 1; ring
    _ ≤ |A+T*r^2/8| + |(2-T)*r^2/8| := abs_add_le _ _
    _ = |A+T*r^2/8| + |T-2| *r^2/8 := by
      rw [abs_div, abs_mul, abs_sub_comm 2 T, abs_sq]
      norm_num
    _ ≤ G*r^4/384 + (G*r^2/40)*r^2/8 := by
      gcongr
    _ = _ := by ring

end I4ActualQuarticTransfer
