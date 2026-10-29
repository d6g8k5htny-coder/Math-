import SourcePinPreservingQuartic
import Mathlib.Tactic.GCongr

noncomputable section

namespace I4SourcePinPreservingQuartic

def quarticK0 : ℝ := 4096
def quarticEpsilonStar : ℝ := 1/(1024*4096*5^5)
def quarticKcap : ℝ := 25600010

def quarticFstar (r : ℝ) (U : Fin 8 → ℝ) : ℝ :=
  1+|U 0|/8+r*|U 4|/48

def quarticWidth (r : ℝ) (U : Fin 8 → ℝ) (R0 : ℝ) : ℝ :=
  quarticFstar r U / (quarticK0*R0^5)

theorem one_le_quarticFstar (r : ℝ) (hr : 0 ≤ r) (U : Fin 8 → ℝ) :
    1 ≤ quarticFstar r U := by
  unfold quarticFstar
  have h0 : 0 ≤ |U 0|/8 := div_nonneg (abs_nonneg _) (by norm_num)
  have h4 : 0 ≤ r*|U 4|/48 := div_nonneg (mul_nonneg hr (abs_nonneg _)) (by norm_num)
  linarith

theorem quarticWidth_pos (r R0 : ℝ) (hr : 0 ≤ r) (hR0 : 1 ≤ R0) (U : Fin 8 → ℝ) :
    0 < quarticWidth r U R0 := by
  unfold quarticWidth
  exact div_pos (lt_of_lt_of_le (by norm_num) (one_le_quarticFstar r hr U))
    (mul_pos (by norm_num [quarticK0]) (pow_pos (by linarith) 5))

/-- The actual cutoff also gives the exact LM001 raw-radius regularity budget. -/
theorem cutoff_raw_regularity (r R R0 : ℝ) (hr : 0 ≤ r) (hR0 : 1 ≤ R0)
    (hR0R : R0 ≤ 5*R) (hcut : r*R^5 ≤ quarticEpsilonStar) :
    r*R0^5 ≤ 1/(1024*quarticK0) := by
  have hpow : R0^5 ≤ (5*R)^5 := pow_le_pow_left₀ (by linarith) hR0R 5
  calc
    _ ≤ r*(5*R)^5 := mul_le_mul_of_nonneg_left hpow hr
    _ = 5^5*(r*R^5) := by ring
    _ ≤ 5^5*quarticEpsilonStar := mul_le_mul_of_nonneg_left hcut (by norm_num)
    _ = _ := by norm_num [quarticEpsilonStar,quarticK0]

/-- The same cutoff controls the fifth derivative through G≤R; no additional
fifth-derivative tail condition is needed for this arithmetic consequence. -/
theorem cutoff_scaled_error_budget (r R R0 G : ℝ)
    (hr : 0 ≤ r) (hr1 : r ≤ 1) (hR : 1 ≤ R) (hR0 : 1 ≤ R0)
    (hR0R : R0 ≤ 5*R) (hG0 : 0 ≤ G) (hGR : G ≤ R)
    (hcut : r*R^5 ≤ quarticEpsilonStar) :
    12*quarticK0*R0^4*r^2*G ≤ 1 := by
  have hK : 0 < quarticK0 := by norm_num [quarticK0]
  have hR00 : 0 ≤ R0 := by linarith
  have hRpos : 0 ≤ R := by linarith
  calc
    _ ≤ 12*quarticK0*(5*R)^4*r^2*R := by gcongr
    _ = (12*quarticK0*5^4*r)*(r*R^5) := by ring
    _ ≤ (12*quarticK0*5^4*r)*quarticEpsilonStar :=
      mul_le_mul_of_nonneg_left hcut (by positivity)
    _ ≤ (12*quarticK0*5^4)*quarticEpsilonStar := by
      apply mul_le_mul_of_nonneg_right _ (by norm_num [quarticEpsilonStar])
      nlinarith [hr1]
    _ ≤ 1 := by norm_num [quarticK0,quarticEpsilonStar]

/-- The radius cutoff implies the literal LM004 quarter-width tolerance for
any LM001 Fstar≥1, keeping every denominator strictly positive. -/
theorem cutoff_adaptive_tolerance (r R R0 G Fstar : ℝ)
    (hr : 0 ≤ r) (hr1 : r ≤ 1) (hR : 1 ≤ R) (hR0 : 1 ≤ R0)
    (hR0R : R0 ≤ 5*R) (hG0 : 0 ≤ G) (hGR : G ≤ R)
    (hFstar : 1 ≤ Fstar) (hcut : r*R^5 ≤ quarticEpsilonStar) :
    3*r^2*G ≤ R0*(Fstar/(quarticK0*R0^5))/4 := by
  have hbudget := cutoff_scaled_error_budget r R R0 G hr hr1 hR hR0 hR0R hG0 hGR hcut
  have hR00 : 0 ≤ R0 := by linarith
  have hden : 0 < quarticK0*R0^5 := by
    exact mul_pos (by norm_num [quarticK0]) (pow_pos (by linarith) 5)
  have hm : (3*r^2*G*4)*(quarticK0*R0^5) ≤ R0*Fstar := by
    calc
      _ = R0*(12*quarticK0*R0^4*r^2*G) := by ring
      _ ≤ R0*1 := mul_le_mul_of_nonneg_left hbudget hR00
      _ ≤ R0*Fstar := mul_le_mul_of_nonneg_left hFstar hR00
  calc
    _ ≤ ((R0*Fstar)/(quarticK0*R0^5))/4 :=
      (le_div_iff₀ (by norm_num : (0 : ℝ) < 4)).mpr ((le_div_iff₀ hden).mpr hm)
    _ = _ := by ring

theorem cutoff_quarticWidth_tolerance (r R R0 G : ℝ) (U : Fin 8 → ℝ)
    (hr : 0 ≤ r) (hr1 : r ≤ 1) (hR : 1 ≤ R) (hR0 : 1 ≤ R0)
    (hR0R : R0 ≤ 5*R) (hG0 : 0 ≤ G) (hGR : G ≤ R)
    (hcut : r*R^5 ≤ quarticEpsilonStar) :
    3*r^2*G ≤ R0*quarticWidth r U R0/4 :=
  cutoff_adaptive_tolerance r R R0 G (quarticFstar r U)
    hr hr1 hR hR0 hR0R hG0 hGR (one_le_quarticFstar r hr U) hcut

/-- The exact cutoff curvature constant implies the literal LM001 threshold. -/
theorem cutoff_curvature_threshold (q r R R0 : ℝ) (hr : 0 < r)
    (hR : 1 ≤ R) (hR0 : 1 ≤ R0) (hR0R : R0 ≤ 5*R)
    (hq : q ≤ -quarticKcap*r*R^5) :
    q/r ≤ -(2*quarticK0*R0^5+2*R0) := by
  have hR00 : 0 ≤ R0 := by linarith
  have hRpos : 0 ≤ R := by linarith
  have hR5 : R ≤ R^5 := by
    calc
      R = R^1 := by simp
      _ ≤ R^5 := pow_le_pow_right₀ hR (by norm_num)
  have hcap : 2*quarticK0*R0^5+2*R0 ≤ quarticKcap*R^5 := by
    calc
      _ ≤ 2*quarticK0*(5*R)^5+2*(5*R) := by
        have hK : 0 < quarticK0 := by norm_num [quarticK0]
        gcongr
      _ ≤ 2*quarticK0*5^5*R^5+10*R^5 := by
        have heq : 2*quarticK0*(5*R)^5+2*(5*R) = 2*quarticK0*5^5*R^5+10*R := by ring
        rw [heq]
        linarith [hR5]
      _ = _ := by norm_num [quarticK0,quarticKcap]; ring
  apply (div_le_iff₀ hr).mpr
  calc
    q ≤ -quarticKcap*r*R^5 := hq
    _ = -(quarticKcap*R^5)*r := by ring
    _ ≤ -(2*quarticK0*R0^5+2*R0)*r :=
      mul_le_mul_of_nonneg_right (neg_le_neg hcap) hr.le

/-- The certificate's size bound controls both its strip width and endpoint
radius. No capture or chart transport is asserted. -/
theorem certificate_width_geometry (R0 W : ℝ) (hR0 : 1 ≤ R0)
    (hsmall : R0*W ≤ 1/2048) :
    W ≤ 1/2048 ∧ 8*R0*W ≤ 1/256 := by
  constructor
  · by_cases hW : 0 ≤ W
    · have h := mul_le_mul_of_nonneg_right hR0 hW
      nlinarith [hsmall]
    · linarith
  · nlinarith [hsmall]

end I4SourcePinPreservingQuartic
