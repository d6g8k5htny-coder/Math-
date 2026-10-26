import SourcePinPreservingQuartic

noncomputable section
open I4SmoothCarrier I4SourceConfluentPins I4SourceConditionalMajorant
open I4SourcePinCurvatureBounds I4SourcePinPreservingQuartic
open Matrix WithLp
open scoped BigOperators
set_option autoImplicit false

namespace I4SourcePinPreservingQuartic

theorem matrixLinearEuclidean_sub (A B : Matrix (Fin 2) (Fin 2) ℝ) :
    matrixLinearEuclidean A-matrixLinearEuclidean B = matrixLinearEuclidean (A-B) := by
  ext v i
  change (A *ᵥ ofLp v) i-(B *ᵥ ofLp v) i = ((A-B) *ᵥ ofLp v) i
  rw [Matrix.sub_mulVec]
  rfl

theorem coordinateDirection_norm_le_one (i : Fin 2) : ‖coordinateDirection i‖ ≤ (1 : ℝ) := by
  apply (pi_norm_le_iff_of_nonneg zero_le_one).mpr
  intro j
  fin_cases i <;> fin_cases j <;> norm_num [coordinateDirection]

theorem sourceScaledGradientRaw_apply (L r : ℝ) (ω : SmoothSample 2 L)
    (p : Fin 2 → ℝ) (i : Fin 2) :
    sourceScaledGradientRaw L r ω p i =
      fderiv ℝ (smoothSourceField 2 L ω) (r • p) (coordinateDirection i)/r^2 := by
  fin_cases i
  · change fderiv ℝ (smoothSourceField 2 L ω) (r • p) directionX/r^2 =
      fderiv ℝ (smoothSourceField 2 L ω) (r • p) (coordinateDirection 0)/r^2
    rw [coordinateDirection_zero]
    rfl
  · change fderiv ℝ (smoothSourceField 2 L ω) (r • p) directionY/r^2 =
      fderiv ℝ (smoothSourceField 2 L ω) (r • p) (coordinateDirection 1)/r^2
    rw [coordinateDirection_one]
    rfl

theorem source_scaled_gradient_taylor_coordinate_error {L : ℝ} (hL : L ≠ 0)
    (r : ℝ) (hr : 0 < r) (ω : SmoothSample 2 L) (p : Fin 2 → ℝ) (i : Fin 2) :
    |sourceScaledGradientRaw L r ω p i-sourceGradientTaylorRaw L r ω p i| ≤
      sourceDerivativeMajorant L 5 ω*r^2*‖toLp 2 p‖^4/24 := by
  have hb := source_line_gradient_taylor hL ω (r • p) (coordinateDirection i)
  have hG := sourceDerivativeMajorant_nonneg L 5 ω
  have hdir := coordinateDirection_norm_le_one i
  have hnorm := pi_norm_le_euclidean_norm p
  have hpow : ‖r • p‖^4 ≤ r^4*‖toLp 2 p‖^4 := by
    rw [norm_smul,Real.norm_eq_abs,abs_of_nonneg hr.le,mul_pow]
    exact mul_le_mul_of_nonneg_left (pow_le_pow_left₀ (norm_nonneg p) hnorm 4) (pow_nonneg hr.le 4)
  have hb' : |fderiv ℝ (smoothSourceField 2 L ω) (r • p) (coordinateDirection i)-
      (fderiv ℝ (smoothSourceField 2 L ω) 0 (coordinateDirection i)+
        iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω) 0 ![r • p,coordinateDirection i]+
        iteratedFDeriv ℝ 3 (smoothSourceField 2 L ω) 0 ![r • p,r • p,coordinateDirection i]/2+
        iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![r • p,r • p,r • p,coordinateDirection i]/6)| ≤
      sourceDerivativeMajorant L 5 ω*r^4*‖toLp 2 p‖^4/24 := by
    apply hb.trans
    have hh := mul_le_of_le_one_right (mul_nonneg hG (pow_nonneg (norm_nonneg (r • p)) 4)) hdir
    have hh' := mul_le_mul_of_nonneg_left hpow hG
    nlinarith
  rw [sourceScaledGradientRaw_apply,sourceGradientTaylorRaw,← sub_div,abs_div,
    abs_of_nonneg (sq_nonneg r)]
  calc
    _ ≤ (sourceDerivativeMajorant L 5 ω*r^4*‖toLp 2 p‖^4/24)/r^2 :=
      div_le_div_of_nonneg_right hb' (sq_nonneg r)
    _ = _ := by field_simp [hr.ne']

theorem source_scaled_gradient_taylor_error {L : ℝ} (hL : L ≠ 0)
    (r : ℝ) (hr : 0 < r) (ω : SmoothSample 2 L) (p : SourcePlane) :
    ‖sourceScaledGradient L r ω p-sourceGradientTaylor L r ω p‖ ≤
      sourceDerivativeMajorant L 5 ω*r^2*‖p‖^4/12 := by
  have h0 := source_scaled_gradient_taylor_coordinate_error hL r hr ω (ofLp p) 0
  have h1 := source_scaled_gradient_taylor_coordinate_error hL r hr ω (ofLp p) 1
  calc
    _ ≤ |(sourceScaledGradient L r ω p-sourceGradientTaylor L r ω p) 0|+
        |(sourceScaledGradient L r ω p-sourceGradientTaylor L r ω p) 1| :=
      euclidean_two_norm_le_abs_sum _
    _ ≤ (sourceDerivativeMajorant L 5 ω*r^2*‖p‖^4/24)+
        (sourceDerivativeMajorant L 5 ω*r^2*‖p‖^4/24) := by
      exact add_le_add h0 h1
    _ = _ := by ring

theorem source_scaled_hessian_taylor_coordinate_error {L : ℝ} (hL : L ≠ 0)
    (r : ℝ) (hr : 0 < r) (ω : SmoothSample 2 L) (p : Fin 2 → ℝ) (i j : Fin 2) :
    |iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω) (r • p)
        ![coordinateDirection j,coordinateDirection i]/r-sourceHessianTaylor L r ω p i j| ≤
      sourceDerivativeMajorant L 5 ω*r^2*‖toLp 2 p‖^3/6 := by
  have hb := source_line_hessian_taylor hL ω (r • p) (coordinateDirection j) (coordinateDirection i)
  have hG := sourceDerivativeMajorant_nonneg L 5 ω
  have hi := coordinateDirection_norm_le_one i
  have hj := coordinateDirection_norm_le_one j
  have hnorm := pi_norm_le_euclidean_norm p
  have hpow : ‖r • p‖^3 ≤ r^3*‖toLp 2 p‖^3 := by
    rw [norm_smul,Real.norm_eq_abs,abs_of_nonneg hr.le,mul_pow]
    exact mul_le_mul_of_nonneg_left (pow_le_pow_left₀ (norm_nonneg p) hnorm 3) (pow_nonneg hr.le 3)
  have hb' : |iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω) (r • p)
      ![coordinateDirection j,coordinateDirection i] -
      (iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω) 0 ![coordinateDirection j,coordinateDirection i]+
        iteratedFDeriv ℝ 3 (smoothSourceField 2 L ω) 0 ![r • p,coordinateDirection j,coordinateDirection i]+
        iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![r • p,r • p,coordinateDirection j,coordinateDirection i]/2)| ≤
      sourceDerivativeMajorant L 5 ω*r^3*‖toLp 2 p‖^3/6 := by
    apply hb.trans
    have hh0 := mul_le_of_le_one_right (mul_nonneg hG (pow_nonneg (norm_nonneg (r • p)) 3)) hj
    have hh1 := mul_le_of_le_one_right
      (mul_nonneg (mul_nonneg hG (pow_nonneg (norm_nonneg (r • p)) 3)) (norm_nonneg (coordinateDirection j))) hi
    have hh2 := mul_le_mul_of_nonneg_left hpow hG
    nlinarith
  rw [sourceHessianTaylor,← sub_div,abs_div,abs_of_nonneg hr.le]
  calc
    _ ≤ (sourceDerivativeMajorant L 5 ω*r^3*‖toLp 2 p‖^3/6)/r :=
      div_le_div_of_nonneg_right hb' hr.le
    _ = _ := by field_simp [hr.ne']

theorem source_scaled_hessian_taylor_error {L : ℝ} (hL : L ≠ 0)
    (r : ℝ) (hr : 0 < r) (ω : SmoothSample 2 L) (p : SourcePlane) :
    ‖fderiv ℝ (sourceScaledGradient L r ω) p-
      matrixLinearEuclidean (sourceHessianTaylor L r ω (ofLp p))‖ ≤
      sourceDerivativeMajorant L 5 ω*r^2*‖p‖^3/3 := by
  rw [(sourceScaledGradient_hasFDerivAt hL r hr.ne' ω p).fderiv]
  have he : matrixLinearEuclidean (fun i j => iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω)
      (r • ofLp p) ![coordinateDirection j,coordinateDirection i]/r)-
      matrixLinearEuclidean (sourceHessianTaylor L r ω (ofLp p)) =
      matrixLinearEuclidean (fun i j => iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω)
        (r • ofLp p) ![coordinateDirection j,coordinateDirection i]/r-
          sourceHessianTaylor L r ω (ofLp p) i j) := by
    exact matrixLinearEuclidean_sub _ _
  rw [he]
  have hG := sourceDerivativeMajorant_nonneg L 5 ω
  have hB : 0 ≤ sourceDerivativeMajorant L 5 ω*r^2*‖p‖^3/6 := by positivity
  have hb := matrixLinearEuclidean_norm_le_two_mul _ _ hB
    (fun i j => source_scaled_hessian_taylor_coordinate_error hL r hr ω (ofLp p) i j)
  convert hb using 1
  ring

end I4SourcePinPreservingQuartic
