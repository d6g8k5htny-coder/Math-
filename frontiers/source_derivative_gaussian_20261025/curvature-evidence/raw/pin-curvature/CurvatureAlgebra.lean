import SourcePinCurvatureBounds

noncomputable section
open I4SmoothCarrier I4SourcePinCurvatureBounds I4SourceEndpointEstimates
open ResearchFormalCoreR1 Matrix
open scoped BigOperators Matrix
set_option autoImplicit false

namespace I4SourcePinCurvatureBounds

theorem endpoint_det_abs_le (r R q : ℝ) (hr : 0 ≤ r) (hR : 0 ≤ R)
    (a b c : ℝ) (ha : |a| ≤ R) (hb : |b| ≤ R) (hc : |c-q| ≤ r*R) :
    |a*c-r*b^2| ≤ R*|q|+2*r*R^2 := by
  have hc' : |c| ≤ |q|+r*R := by
    calc
      _ = |(c-q)+q| := by ring_nf
      _ ≤ |c-q|+|q| := abs_add_le _ _
      _ ≤ _ := by linarith
  have hb2 : |b|^2 ≤ R^2 := pow_le_pow_left₀ (abs_nonneg b) hb 2
  calc
    _ ≤ |a*c|+|r*b^2| := abs_sub _ _
    _ = |a| *|c|+r*|b|^2 := by rw [abs_mul,abs_mul,abs_of_nonneg hr,abs_pow]
    _ ≤ R*(|q|+r*R)+r*R^2 := add_le_add
      (mul_le_mul ha hc' (abs_nonneg _) hR) (mul_le_mul_of_nonneg_left hb2 hr)
    _ = _ := by ring

theorem endpointWeight_curvature_le (r R q : ℝ) (hr : 0 ≤ r) (hR : 0 ≤ R)
    (v : Fin 6 → ℝ) (h0 : |v 0| ≤ R) (h1 : |v 1| ≤ R)
    (h2 : |v 2| ≤ R) (h3 : |v 3| ≤ R)
    (h4 : |v 4-q| ≤ r*R) (h5 : |v 5-q| ≤ r*R) :
    sourceEndpointWeight r v ≤ 2*r^2*R^2*q^2+8*r^4*R^4 := by
  have hM := endpoint_det_abs_le r R q hr hR (v 0) (v 2) (v 4) h0 h2 h4
  have hS := endpoint_det_abs_le r R q hr hR (v 1) (v 3) (v 5) h1 h3 h5
  have hB : 0 ≤ R*|q|+2*r*R^2 := by positivity
  have hprod : |v 0*v 4-r*v 2^2| *|v 1*v 5-r*v 3^2| ≤
      (R*|q|+2*r*R^2)^2 := by
    simpa only [pow_two] using mul_le_mul hM hS (abs_nonneg _) hB
  have hsquare : r^2*(R*|q|+2*r*R^2)^2 ≤ 2*r^2*R^2*q^2+8*r^4*R^4 := by
    have hh : (R*|q|+2*r*R^2)^2 ≤ 2*(R*|q|)^2+2*(2*r*R^2)^2 := by
      nlinarith [sq_nonneg (R*|q|-2*r*R^2)]
    calc
      _ ≤ r^2*(2*(R*|q|)^2+2*(2*r*R^2)^2) :=
        mul_le_mul_of_nonneg_left hh (sq_nonneg r)
      _ = _ := by rw [mul_pow R, sq_abs]; ring
  unfold sourceEndpointWeight egm_weight
  split_ifs
  · have heq : (egm_HM r (sourcePhysicalCoordinates v)).det *
        (egm_HS r (sourcePhysicalCoordinates v)).det =
        r^2*((v 0*v 4-r*v 2^2)*(v 1*v 5-r*v 3^2)) := by
      simp [egm_HM,egm_HS,sourcePhysicalCoordinates,Matrix.det_fin_two]
      ring
    rw [heq,abs_mul,abs_of_nonneg (sq_nonneg r),abs_mul]
    exact (mul_le_mul_of_nonneg_left hprod (sq_nonneg r)).trans hsquare
  · positivity

theorem strict_endpoint_transverse_neg (r : ℝ) (v : Fin 6 → ℝ)
    (ht : dm2Negative (egm_HM r (sourcePhysicalCoordinates v))) : v 4 < 0 := by
  have h := ht ![0,1] (by simp)
  simpa [egm_HM,sourcePhysicalCoordinates,Fin.sum_univ_two] using h

theorem curvature_slab_of_upper (q r R Γ K : ℝ) (hr : 0 ≤ r) (hR : 1 ≤ R)
    (hΓ : Γ ≤ R) (hu : q < r*Γ) (hl : -K*r*R^5 ≤ q) :
    |q| ≤ max K 1*r*R^5 := by
  have hR0 : 0 ≤ R := le_trans (by norm_num) hR
  have hp : R ≤ R^5 := by
    calc
      R = R^1 := by simp
      _ ≤ R^5 := pow_le_pow_right₀ hR (by norm_num)
  have hmax : 1 ≤ max K 1 := le_max_right _ _
  have hl' : -(max K 1*r*R^5) ≤ q := by
    have hh := mul_le_mul_of_nonneg_right (le_max_left K 1) (mul_nonneg hr (pow_nonneg hR0 5))
    nlinarith
  have hu' : q ≤ max K 1*r*R^5 := by
    have hq := hu.le.trans (mul_le_mul_of_nonneg_left (hΓ.trans hp) hr)
    have hh := mul_le_mul_of_nonneg_right hmax (mul_nonneg hr (pow_nonneg hR0 5))
    nlinarith
  exact abs_le.mpr ⟨hl',hu'⟩

end I4SourcePinCurvatureBounds
