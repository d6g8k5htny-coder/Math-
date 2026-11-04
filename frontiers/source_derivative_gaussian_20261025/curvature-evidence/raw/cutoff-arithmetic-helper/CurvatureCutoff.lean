import GaussianWeightedMajorants
import Mathlib.Tactic.GCongr
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring

namespace I4ScalarProductCurvature

theorem regular_bounds {A K eps S R q r : ℝ}
    (hA : 0 ≤ A) (hK : 0 ≤ K) (heps : 0 ≤ eps) (hr : 0 ≤ r)
    (hS : 1 ≤ S) (hR : 0 ≤ R) (hdom : R ≤ A * (|q| + S))
    (hcut : r * R^5 ≤ eps) (hslab : |q| ≤ K * r * R^5) :
    let D := A * (1 + K * eps)
    R ≤ D * S ∧ |q| ≤ K * D^5 * r * S^5 ∧
      2*r^2*R^2*q^2 + 8*r^4*R^4 ≤
        (2*K^2*D^12 + 8*D^4)*r^4*S^12 := by
  dsimp only
  let D := A * (1 + K * eps)
  have hS0 : 0 ≤ S := le_trans (by norm_num) hS
  have hD : 0 ≤ D := by dsimp [D]; positivity
  have hqeps : |q| ≤ K * eps := calc
    |q| ≤ K * r * R^5 := hslab
    _ = K * (r * R^5) := by ring
    _ ≤ K * eps := mul_le_mul_of_nonneg_left hcut hK
  have hsmall : |q| + S ≤ (1 + K * eps) * S := by nlinarith [mul_nonneg hK heps, mul_le_mul_of_nonneg_left hS (mul_nonneg hK heps)]
  have hRD : R ≤ D * S := calc
    R ≤ A * (|q| + S) := hdom
    _ ≤ A * ((1 + K * eps) * S) := mul_le_mul_of_nonneg_left hsmall hA
    _ = D * S := by dsimp [D]; ring
  have hq : |q| ≤ K * D^5 * r * S^5 := calc
    |q| ≤ K * r * R^5 := hslab
    _ ≤ K * r * (D*S)^5 := by gcongr
    _ = K * D^5 * r * S^5 := by ring
  have hweight : 2*r^2*R^2*q^2 + 8*r^4*R^4 ≤
      2*r^2*(D*S)^2*(K*D^5*r*S^5)^2 + 8*r^4*(D*S)^4 := by
    rw [← sq_abs q]
    gcongr
  have hS4 : S^4 ≤ S^12 := by
    calc
      S^4 ≤ S^4 * S^8 := le_mul_of_one_le_right (pow_nonneg hS0 _) (one_le_pow₀ hS)
      _ = S^12 := by ring
  refine ⟨hRD, hq, ?_⟩
  calc
    2*r^2*R^2*q^2 + 8*r^4*R^4 ≤
        2*r^2*(D*S)^2*(K*D^5*r*S^5)^2 + 8*r^4*(D*S)^4 := hweight
    _ = 2*K^2*D^12*r^4*S^12 + 8*D^4*r^4*S^4 := by ring
    _ ≤ 2*K^2*D^12*r^4*S^12 + 8*D^4*r^4*S^12 := by gcongr
    _ = (2*K^2*D^12 + 8*D^4)*r^4*S^12 := by ring

end I4ScalarProductCurvature
