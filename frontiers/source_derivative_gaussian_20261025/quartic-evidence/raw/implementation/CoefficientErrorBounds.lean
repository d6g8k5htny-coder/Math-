import SourcePinPreservingQuartic

noncomputable section

open I4SmoothCarrier I4SourceConfluentPins I4SourcePinCurvatureBounds I4SourceConditionalMajorant
open Matrix WithLp

namespace I4SourcePinPreservingQuartic

theorem coefficient_vector_error_le (S A B C D T : ℝ) (hS : 0 ≤ S)
    (hA : |A| ≤ 11*S/1920) (hB : |B| ≤ S/384)
    (hC : |C| ≤ S/192) (hD : |D| ≤ S/192) (hT : |T| ≤ S/40)
    (z : EuclideanSpace ℝ (Fin 2)) :
    ‖toLp 2 ![A+C*z 0+D*z 1+T*(z 0)^2/2,B+D*z 0]‖ ≤
      S*(1/120+‖z‖/64+‖z‖^2/80) := by
  have hx : |z 0| ≤ ‖z‖ := PiLp.norm_apply_le z 0
  have hy : |z 1| ≤ ‖z‖ := PiLp.norm_apply_le z 1
  have hx2 : (z 0)^2 ≤ ‖z‖^2 := by
    simpa only [sq_abs] using pow_le_pow_left₀ (abs_nonneg _) hx 2
  have hCX : |C*z 0| ≤ S/192*‖z‖ := by
    rw [abs_mul]
    exact mul_le_mul hC hx (abs_nonneg _) (by positivity)
  have hDX : |D*z 0| ≤ S/192*‖z‖ := by
    rw [abs_mul]
    exact mul_le_mul hD hx (abs_nonneg _) (by positivity)
  have hDY : |D*z 1| ≤ S/192*‖z‖ := by
    rw [abs_mul]
    exact mul_le_mul hD hy (abs_nonneg _) (by positivity)
  have hTX : |T*(z 0)^2/2| ≤ S/40*‖z‖^2/2 := by
    rw [abs_div,abs_mul,abs_of_nonneg (sq_nonneg (z 0))]
    norm_num
    have hprod : |T| * (z 0)^2 ≤ S/40*‖z‖^2 :=
      mul_le_mul hT hx2 (sq_nonneg _) (by positivity)
    linarith [hprod]
  have hv0 : |A+C*z 0+D*z 1+T*(z 0)^2/2| ≤
      11*S/1920+S/192*‖z‖+S/192*‖z‖+S/40*‖z‖^2/2 := by
    nlinarith [abs_add_le (A+C*z 0+D*z 1) (T*(z 0)^2/2),
      abs_add_le (A+C*z 0) (D*z 1),abs_add_le A (C*z 0)]
  have hv1 : |B+D*z 0| ≤ S/384+S/192*‖z‖ :=
    (abs_add_le _ _).trans (add_le_add hB hDX)
  calc
    _ ≤ |A+C*z 0+D*z 1+T*(z 0)^2/2|+|B+D*z 0| :=
      euclidean_two_norm_le_abs_sum _
    _ ≤ _ := by nlinarith [hv0,hv1]

theorem coefficient_matrix_error_le (S C D T : ℝ) (hS : 0 ≤ S)
    (hC : |C| ≤ S/192) (hD : |D| ≤ S/192) (hT : |T| ≤ S/40)
    (z : EuclideanSpace ℝ (Fin 2)) :
    ‖matrixLinearEuclidean !![C+T*z 0,D;D,0]‖ ≤ S*(1/96+‖z‖/40) := by
  have hx : |z 0| ≤ ‖z‖ := PiLp.norm_apply_le z 0
  have hTX : |T*z 0| ≤ S/40*‖z‖ := by
    rw [abs_mul]
    exact mul_le_mul hT hx (abs_nonneg _) (by positivity)
  have ha := abs_add_le C (T*z 0)
  have hm := matrixLinearEuclidean_symmetric_norm_le_abs_sum (C+T*z 0) D 0
  norm_num at hm
  nlinarith [hm,ha]

private theorem actual_normalized_coefficient_errors {L : ℝ} (hL : L ≠ 0)
    (r : ℝ) (hr : 0 < r) (ω : SmoothSample 2 L) (hp : sourcePhysicalPins L r ω) :
    let S := sourceDerivativeMajorant L 5 ω*r^2
    let A := (fderiv ℝ (smoothSourceField 2 L ω) 0 directionX+r^2/4)/r^2
    let B := (fderiv ℝ (smoothSourceField 2 L ω) 0 directionY+sourceRawU L ω 0*r^2/8)/r^2
    let C := (iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω) 0 ![directionX,directionX]+
      sourceRawU L ω 3*r^2/24)/r
    let D := (iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω) 0 ![directionX,directionY]+
      sourceRawU L ω 4*r^2/24)/r
    let T := sourceAxialThird L ω-2
    |A| ≤ 11*S/1920 ∧ |B| ≤ S/384 ∧ |C| ≤ S/192 ∧ |D| ≤ S/192 ∧ |T| ≤ S/40 := by
  dsimp only
  obtain ⟨hA,hB,hC,hD⟩ := source_low_pin_coefficients hL r hr ω hp
  have hT := source_axial_third_error hL r hr ω hp
  refine ⟨?_,?_,?_,?_,?_⟩
  · rw [abs_div,abs_of_nonneg (sq_nonneg r)]
    apply (div_le_iff₀ (sq_pos_of_pos hr)).mpr
    calc
      _ ≤ (11/1920 : ℝ)*sourceDerivativeMajorant L 5 ω*r^4 := hA
      _ = _ := by ring
  · rw [abs_div,abs_of_nonneg (sq_nonneg r)]
    apply (div_le_iff₀ (sq_pos_of_pos hr)).mpr
    calc
      _ ≤ sourceDerivativeMajorant L 5 ω*r^4/384 := hB
      _ = _ := by ring
  · rw [abs_div,abs_of_pos hr]
    apply (div_le_iff₀ hr).mpr
    calc
      _ ≤ sourceDerivativeMajorant L 5 ω*r^3/192 := hC
      _ = _ := by ring
  · rw [abs_div,abs_of_pos hr]
    apply (div_le_iff₀ hr).mpr
    calc
      _ ≤ sourceDerivativeMajorant L 5 ω*r^3/192 := hD
      _ = _ := by ring
  · calc
      _ ≤ r^2*sourceDerivativeMajorant L 5 ω/40 := hT
      _ = _ := by ring

/-- Actual pins force the ordinary Taylor/LM001 polynomial value comparison.
All coefficient errors are derived from the actual pinned source. -/
theorem sourceGradientTaylor_quartic_error_le {L : ℝ} (hL : L ≠ 0)
    (r : ℝ) (hr : 0 < r) (ω : SmoothSample 2 L) (hp : sourcePhysicalPins L r ω)
    (z : EuclideanSpace ℝ (Fin 2)) :
    ‖sourceGradientTaylor L r ω z-sourceQuartic L r ω z‖ ≤
      sourceDerivativeMajorant L 5 ω*r^2*(1/120+‖z‖/64+‖z‖^2/80) := by
  let S := sourceDerivativeMajorant L 5 ω*r^2
  let A := (fderiv ℝ (smoothSourceField 2 L ω) 0 directionX+r^2/4)/r^2
  let B := (fderiv ℝ (smoothSourceField 2 L ω) 0 directionY+sourceRawU L ω 0*r^2/8)/r^2
  let C := (iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω) 0 ![directionX,directionX]+
    sourceRawU L ω 3*r^2/24)/r
  let D := (iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω) 0 ![directionX,directionY]+
    sourceRawU L ω 4*r^2/24)/r
  let T := sourceAxialThird L ω-2
  obtain ⟨hA,hB,hC,hD,hT⟩ := actual_normalized_coefficient_errors hL r hr ω hp
  have hS : 0 ≤ S := mul_nonneg (sourceDerivativeMajorant_nonneg L 5 ω) (sq_nonneg r)
  have heq : sourceGradientTaylor L r ω z-sourceQuartic L r ω z =
      toLp 2 ![A+C*z 0+D*z 1+T*(z 0)^2/2,B+D*z 0] := by
    ext i
    fin_cases i
    · exact sourceGradientTaylorRaw_sub_quartic_zero hL r hr.ne' ω (ofLp z)
    · exact sourceGradientTaylorRaw_sub_quartic_one hL r hr.ne' ω (ofLp z)
  rw [heq]
  exact coefficient_vector_error_le S A B C D T hS hA hB hC hD hT z

/-- The actual Hessian Taylor/LM001 derivative comparison. The symmetric
three-coefficient norm bridge retains a stronger constant than required. -/
theorem sourceHessianTaylor_quartic_error_le {L : ℝ} (hL : L ≠ 0)
    (r : ℝ) (hr : 0 < r) (ω : SmoothSample 2 L) (hp : sourcePhysicalPins L r ω)
    (z : EuclideanSpace ℝ (Fin 2)) :
    ‖matrixLinearEuclidean (sourceHessianTaylor L r ω (ofLp z))-
      fderiv ℝ (sourceQuartic L r ω) z‖ ≤
      sourceDerivativeMajorant L 5 ω*r^2*(1/96+‖z‖/40) := by
  let S := sourceDerivativeMajorant L 5 ω*r^2
  let C := (iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω) 0 ![directionX,directionX]+
    sourceRawU L ω 3*r^2/24)/r
  let D := (iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω) 0 ![directionX,directionY]+
    sourceRawU L ω 4*r^2/24)/r
  let T := sourceAxialThird L ω-2
  obtain ⟨_hA,_hB,hC,hD,hT⟩ := actual_normalized_coefficient_errors hL r hr ω hp
  have hS : 0 ≤ S := mul_nonneg (sourceDerivativeMajorant_nonneg L 5 ω) (sq_nonneg r)
  have hP : fderiv ℝ (sourceQuartic L r ω) z =
      matrixLinearEuclidean (pinPreservingJacobian r (sourceQ L ω) (sourceRawU L ω) (ofLp z)) :=
    fderiv_pinPreservingQuartic r (sourceQ L ω) (sourceRawU L ω) z
  rw [hP]
  change ‖Matrix.toEuclideanCLM (𝕜 := ℝ) (sourceHessianTaylor L r ω (ofLp z))-
    Matrix.toEuclideanCLM (𝕜 := ℝ) (pinPreservingJacobian r (sourceQ L ω) (sourceRawU L ω) (ofLp z))‖ ≤ _
  rw [← map_sub]
  rw [sourceHessianTaylor_sub_quarticJacobian hL r hr.ne' ω (ofLp z)]
  exact coefficient_matrix_error_le S C D T hS hC hD hT z

end I4SourcePinPreservingQuartic
