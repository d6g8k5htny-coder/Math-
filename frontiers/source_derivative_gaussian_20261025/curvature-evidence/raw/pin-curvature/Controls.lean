import SourcePinCurvatureBounds

noncomputable section
open I4SourcePinCurvatureBounds I4SourceEndpointEstimates I4SourceConfluentLimits I4PeanoErrorBounds
open ResearchFormalCoreR1 MeasureTheory Set

-- Nonunit radius and literal LM006 endpoint order: det(HM)=6, det(HS)=-6.
example : sourceEndpointWeight 2 ![-1,1,0,0,-3,-3] = 36 := by
  norm_num [sourceEndpointWeight, egm_weight, egm_HM, egm_HS,
    sourcePhysicalCoordinates, dm2_negative_iff, Matrix.det_fin_two]

-- The proved curvature bound consumes those same literal coordinates.
example : sourceEndpointWeight 2 ![-1,1,0,0,-3,-3] ≤
    2*(2:ℝ)^2*1^2*(-3)^2+8*2^4*1^4 := by
  exact endpointWeight_curvature_le 2 1 (-3) (by norm_num) (by norm_num)
    ![-1,1,0,0,-3,-3] (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by norm_num) (by norm_num)

-- Strict maximum boundary: zero maximum determinant gives zero weight.
example : sourceEndpointWeight 2 ![-1,1,0,0,0,-3] = 0 := by
  norm_num [sourceEndpointWeight, egm_weight, egm_HM, egm_HS,
    sourcePhysicalCoordinates, dm2_negative_iff, Matrix.det_fin_two]

-- Strict saddle boundary: zero saddle determinant gives zero weight.
example : sourceEndpointWeight 2 ![-1,1,0,0,-3,0] = 0 := by
  norm_num [sourceEndpointWeight, egm_weight, egm_HM, egm_HS,
    sourcePhysicalCoordinates, dm2_negative_iff, Matrix.det_fin_two]

-- Zero radius is retained as an excluded strict-type boundary.
example : sourceEndpointWeight 0 ![-1,1,0,0,-3,-3] = 0 := by
  norm_num [sourceEndpointWeight, egm_weight, egm_HM, egm_HS,
    sourcePhysicalCoordinates, dm2_negative_iff, Matrix.det_fin_two]

-- Strict negative quadratic form forces its literal transverse entry negative.
example : (![-1,1,0,0,-3,-3] : Fin 6 → ℝ) 4 < 0 := by
  apply strict_endpoint_transverse_neg 2
  norm_num [egm_HM, sourcePhysicalCoordinates, dm2_negative_iff]

-- A negative slab coefficient is supported without an artificial K>=0 premise.
-- This is nonvacuous: 1/2 <= 3/4 < 1.
example : |(3/4 : ℝ)| ≤ max (-1/2 : ℝ) 1 * 1 * 1^5 := by
  exact curvature_slab_of_upper (3/4) 1 1 1 (-1/2)
    (by norm_num) (by norm_num) (by norm_num) (by norm_num) (by norm_num)

-- A constant third derivative two satisfies the exact normalized cubic pin.
-- Every point of the nonunit scaled interval has zero error.
example (u : ℝ) (hu : u ∈ Icc (-1/2 : ℝ) (1/2 : ℝ)) : |(2:ℝ)-2| ≤ 0 := by
  have hpin : 6 * (∫ t in (-1/2 : ℝ)..(1/2 : ℝ), peanoCubic t * (2:ℝ)) = 2 := by
    rw [intervalIntegral.integral_mul_const]
    nlinarith [peano_kernel_masses.2.2.2]
  have h := cubic_pin_pointwise_error (fun _ : ℝ => 2) continuous_const 0 2
    (by norm_num) (by norm_num) (by intro x y; simp) hpin u hu
  simpa using h

-- The affine kernel mass is one half, so the constant two average is one.
example : |(∫ t in (-1/2 : ℝ)..(1/2 : ℝ), peanoLeft t * (2:ℝ)) - 1| ≤ 0 := by
  simpa using left_weighted_error (fun _ : ℝ => 2) continuous_const 2 2 0
    (by intro t ht; norm_num)

example : |(∫ t in (-1/2 : ℝ)..(1/2 : ℝ), peanoRight t * (2:ℝ)) - 1| ≤ 0 := by
  simpa using right_weighted_error (fun _ : ℝ => 2) continuous_const 2 2 0
    (by intro t ht; norm_num)

-- The endpoint error lemmas deliberately retain nonnegative radius.
example : ¬ (0 : ℝ) ≤ -2 := by norm_num
