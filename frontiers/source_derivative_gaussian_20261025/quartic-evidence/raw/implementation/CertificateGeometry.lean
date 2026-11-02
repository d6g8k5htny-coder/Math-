import SourcePinPreservingQuartic

noncomputable section
open I4SmoothCarrier I4SourcePinPreservingQuartic WithLp
open scoped BigOperators
set_option autoImplicit false

namespace I4SourcePinPreservingQuartic

theorem sourceRawU_abs_le_radius (L : ℝ) (ω : SmoothSample 2 L) (i : Fin 8) :
    |sourceRawU L ω i| ≤ sourceRawRadius L ω := by
  have h := Finset.single_le_sum (fun j (_ : j ∈ (Finset.univ : Finset (Fin 8))) =>
    abs_nonneg (sourceRawU L ω j)) (Finset.mem_univ i)
  exact h.trans (by unfold sourceRawRadius; linarith)

theorem sourceQuartic_Fstar_le_radius (L r : ℝ) (hr1 : r ≤ 1) (ω : SmoothSample 2 L) :
    quarticFstar r (sourceRawU L ω) ≤ 2*sourceRawRadius L ω := by
  have h0 := sourceRawU_abs_le_radius L ω 0
  have h4 := sourceRawU_abs_le_radius L ω 4
  have hR := sourceRawRadius_one_le L ω
  have hm : r*|sourceRawU L ω 4| ≤ |sourceRawU L ω 4| :=
    mul_le_of_le_one_left (abs_nonneg _) hr1
  unfold quarticFstar
  linarith

theorem sourceQuartic_width_size (L r : ℝ) (hr1 : r ≤ 1) (ω : SmoothSample 2 L) :
    sourceRawRadius L ω*quarticWidth r (sourceRawU L ω) (sourceRawRadius L ω) ≤
      1/2048 := by
  have hR := sourceRawRadius_one_le L ω
  have hR0 : 0 ≤ sourceRawRadius L ω := (by norm_num : (0:ℝ) ≤ 1).trans hR
  have hF := sourceQuartic_Fstar_le_radius L r hr1 ω
  have hpow : sourceRawRadius L ω^2 ≤ sourceRawRadius L ω^5 :=
    pow_le_pow_right₀ hR (by norm_num)
  have hm := mul_le_mul_of_nonneg_left hF hR0
  have hden : 0 < quarticK0*sourceRawRadius L ω^5 :=
    mul_pos (by norm_num [quarticK0]) (pow_pos (lt_of_lt_of_le (by norm_num) hR) 5)
  calc
    _ = (sourceRawRadius L ω*quarticFstar r (sourceRawU L ω))/
        (quarticK0*sourceRawRadius L ω^5) := by unfold quarticWidth; ring
    _ ≤ 1/2048 := by
      apply (div_le_iff₀ hden).mpr
      norm_num only [quarticK0]
      nlinarith

theorem sourceQuartic_width_geometry (L r : ℝ) (hr : 0 ≤ r) (hr1 : r ≤ 1)
    (ω : SmoothSample 2 L) :
    0 < quarticWidth r (sourceRawU L ω) (sourceRawRadius L ω) ∧
    quarticWidth r (sourceRawU L ω) (sourceRawRadius L ω) ≤ 1/2048 ∧
    8*sourceRawRadius L ω*quarticWidth r (sourceRawU L ω) (sourceRawRadius L ω) ≤ 1/256 := by
  have hpos := quarticWidth_pos r _ hr (sourceRawRadius_one_le L ω) (sourceRawU L ω)
  have hgeo := certificate_width_geometry _ _ (sourceRawRadius_one_le L ω)
    (sourceQuartic_width_size L r hr1 ω)
  exact ⟨hpos,hgeo⟩

theorem quartic_strip_in_ball_two (W : ℝ) (hW : W ≤ 1/2048) (p : SourcePlane)
    (hx : |p 0| ≤ 1/2) (hy : |p 1| ≤ W) : ‖p‖ ≤ 2 :=
  (euclidean_two_norm_le_abs_sum p).trans (by linarith)

theorem quartic_endpoint_ball_in_ball_two (ρ : ℝ) (hρ : ρ ≤ 1/256)
    (c p : SourcePlane) (hc : ‖c‖ ≤ 1/2) (hp : ‖p-c‖ ≤ ρ) : ‖p‖ ≤ 2 := by
  calc
    _ = ‖(p-c)+c‖ := by congr 1; abel
    _ ≤ ‖p-c‖+‖c‖ := norm_add_le _ _
    _ ≤ 2 := by linarith

theorem quartic_axis_endpoint_norm (x : ℝ) (hx : |x| ≤ 1/2) :
    ‖(toLp 2 ![x,0] : SourcePlane)‖ ≤ 1/2 := by
  have h := euclidean_two_norm_le_abs_sum (toLp 2 ![x,0])
  simpa using h.trans (by simpa using hx)

end I4SourcePinPreservingQuartic
