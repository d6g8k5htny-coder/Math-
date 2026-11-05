import SourceActualFoldH0

noncomputable section
open Set
open scoped ContDiff
set_option autoImplicit false
namespace I4SourceActualFoldCandidate
open AdaptiveFoldTransverseRidge AdaptiveFoldBoundaryPath
open AdaptiveFoldScalar (J)
open I4SmoothCarrier I4SourceAdaptiveFoldChart I4SourceAdaptiveFoldEstimates

/-- The existing graph derivative formula identifies the literal profile
second derivative with the Schur complement of the literal partials. -/
theorem ridge_profileSlopeFirst_eq_schur
    {V : ℝ × ℝ → ℝ} {O : Set (ℝ × ℝ)}
    {R c M₀ M₁ M₂ A : ℝ} {U : Set ℝ} {z : ℝ → ℝ}
    (hs : StructuralRectangleData V O R c M₀ M₁ M₂ A)
    (hz : RidgeScalarData V O R c M₀ M₁ M₂ U z)
    {x : ℝ} (hx : x ∈ J)
    (hmix : partialY (Vx V) (x,z x) = partialX (Vy V) (x,z x)) :
    profileSlopeFirst V z x = partialX (Vx V) (x,z x) -
      (partialY (Vx V) (x,z x)) ^ 2 / partialY (Vy V) (x,z x) := by
  have hxU := hz.interval_subset hx
  have hneg : partialY (Vy V) (x,z x) < 0 := by
    have hv := hs.vertical_negative x hx (z x)
      (Ioo_subset_Icc_self (hz.root x hxU).1)
    linarith [hs.concavity_pos]
  have hG : ContDiffOn ℝ 2 (Vy V) O :=
    contDiffOn_partialY hs.domain_open hs.regularity (by norm_num)
  have hgraph : ∀ t ∈ U, (t,z t) ∈ O := fun t ht => (hz.root t ht).2.1
  have hzero : ∀ t ∈ U, Vy V (t,z t) = 0 := fun t ht => (hz.root t ht).2.2
  have hd := (zero_graph_derivative_formulas hs.domain_open hz.domain_open
    hG hz.regularity hgraph hzero hxU (ne_of_lt hneg)).1
  unfold profileSlopeFirst
  rw [clm_graph_vector]
  change partialX (Vx V) (x,z x) + deriv z x * partialY (Vx V) (x,z x) = _
  rw [hd, ← hmix]
  ring

/-- The retained barrier gives the two strict Schur signs; the retained
structural rectangle supplies the strict negative vertical entries. -/
theorem endpoint_schur_signs
    {V : ℝ × ℝ → ℝ} {O : Set (ℝ × ℝ)}
    {R c M₀ M₁ M₂ A : ℝ} {U : Set ℝ} {z : ℝ → ℝ}
    (hs : StructuralRectangleData V O R c M₀ M₁ M₂ A)
    (hz : RidgeScalarData V O R c M₀ M₁ M₂ U z)
    (hmix : ∀ p, partialY (Vx V) p = partialX (Vy V) p) :
    partialY (Vy V) (-(1/2:ℝ),0) < 0 ∧
    partialX (Vx V) (-(1/2:ℝ),0) -
      (partialY (Vx V) (-(1/2:ℝ),0)) ^ 2 /
        partialY (Vy V) (-(1/2:ℝ),0) < 0 ∧
    partialY (Vy V) ((1/2:ℝ),0) < 0 ∧
    0 < partialX (Vx V) ((1/2:ℝ),0) -
      (partialY (Vx V) ((1/2:ℝ),0)) ^ 2 /
        partialY (Vy V) ((1/2:ℝ),0) := by
  have hxM : -(1/2:ℝ) ∈ J := by norm_num [J]
  have hxS : (1/2:ℝ) ∈ J := by norm_num [J]
  have hy : (0:ℝ) ∈ Icc (-R) R := by
    constructor <;> linarith [hs.radius_pos]
  have hcM := hs.vertical_negative _ hxM 0 hy
  have hcS := hs.vertical_negative _ hxS 0 hy
  have hM := ridge_profileSlopeFirst_eq_schur hs hz hxM (hmix _)
  have hS := ridge_profileSlopeFirst_eq_schur hs hz hxS (hmix _)
  rw [hz.pin_left] at hM
  rw [hz.pin_right] at hS
  have hbM := hz.barrier.left_deriv
  have hbS := hz.barrier.right_deriv
  rw [hM] at hbM
  rw [hS] at hbS
  exact ⟨by linarith [hs.concavity_pos], by linarith,
    by linarith [hs.concavity_pos], by linarith⟩

/-- Actual source symmetry is consumed internally; no desired endpoint type
or desired Schur sign is an assumption of this deterministic adapter. -/
theorem actual_endpoint_schur_signs
    {L r k : ℝ} (hL : L ≠ 0) (sample : SmoothSample 2 L)
    {O : Set (ℝ × ℝ)} {R c M₀ M₁ M₂ A : ℝ} {U : Set ℝ} {z : ℝ → ℝ}
    (hs : StructuralRectangleData (actualFoldPotential r k sample) O R c M₀ M₁ M₂ A)
    (hz : RidgeScalarData (actualFoldPotential r k sample) O R c M₀ M₁ M₂ U z) :
    let V := actualFoldPotential r k sample
    partialY (Vy V) (-(1/2:ℝ),0) < 0 ∧
    partialX (Vx V) (-(1/2:ℝ),0) -
      (partialY (Vx V) (-(1/2:ℝ),0)) ^ 2 /
        partialY (Vy V) (-(1/2:ℝ),0) < 0 ∧
    partialY (Vy V) ((1/2:ℝ),0) < 0 ∧
    0 < partialX (Vx V) ((1/2:ℝ),0) -
      (partialY (Vx V) ((1/2:ℝ),0)) ^ 2 /
        partialY (Vy V) ((1/2:ℝ),0) :=
  endpoint_schur_signs hs hz (actual_Hy_eq_Gx hL sample)

/-- Every pair vector splits in the literal horizontal and vertical basis. -/
theorem planar_vector_decomposition (v : ℝ × ℝ) :
    v = v.1 • ex + v.2 • ey := by
  ext <;> simp [ex,ey]

/-- Coordinate expansion of an arbitrary planar bilinear diagonal. -/
theorem planar_bilinear_quadratic
    (B : (ℝ × ℝ) →L[ℝ] (ℝ × ℝ) →L[ℝ] ℝ) (v : ℝ × ℝ) :
    B v v = B ex ex * v.1 ^ 2 + (B ex ey + B ey ex) * v.1 * v.2 +
      B ey ey * v.2 ^ 2 := by
  conv_lhs => rw [planar_vector_decomposition v]
  simp only [map_add, map_smul, ContinuousLinearMap.add_apply,
    ContinuousLinearMap.smul_apply, smul_eq_mul]
  ring

/-- The actual Hessian diagonal in literal pair coordinates. Source second
derivative permutation supplies equality of its two ordered mixed entries. -/
theorem actual_planar_hessian_quadratic
    {L r k : ℝ} (hL : L ≠ 0) (sample : SmoothSample 2 L) (p v : ℝ × ℝ) :
    let V := actualFoldPotential r k sample
    iteratedFDeriv ℝ 2 V p ![v,v] = partialX (Vx V) p * v.1 ^ 2 +
      2 * partialY (Vx V) p * v.1 * v.2 + partialY (Vy V) p * v.2 ^ 2 := by
  dsimp only
  let V := actualFoldPotential r k sample
  have hV := actualFoldPotential_smooth hL r k sample
  have hx : partialX (Vx V) p = fderiv ℝ (fderiv ℝ V) p ex ex := by
    change fderiv ℝ (fun q => fderiv ℝ V q ex) p ex = _
    rw [component_first V hV, iteratedFDeriv_two_apply]
    rfl
  have hxy : partialY (Vx V) p = fderiv ℝ (fderiv ℝ V) p ey ex := by
    change fderiv ℝ (fun q => fderiv ℝ V q ex) p ey = _
    rw [component_first V hV, iteratedFDeriv_two_apply]
    rfl
  have hyx : partialX (Vy V) p = fderiv ℝ (fderiv ℝ V) p ex ey := by
    change fderiv ℝ (fun q => fderiv ℝ V q ey) p ex = _
    rw [component_first V hV, iteratedFDeriv_two_apply]
    rfl
  have hy : partialY (Vy V) p = fderiv ℝ (fderiv ℝ V) p ey ey := by
    change fderiv ℝ (fun q => fderiv ℝ V q ey) p ey = _
    rw [component_first V hV, iteratedFDeriv_two_apply]
    rfl
  change iteratedFDeriv ℝ 2 V p ![v,v] = _
  rw [iteratedFDeriv_two_apply]
  simp only [Matrix.cons_val_zero, Matrix.cons_val_one, Matrix.head_cons]
  rw [planar_bilinear_quadratic, ← hx, ← hxy, ← hyx, ← hy,
    actual_Hy_eq_Gx hL sample p]
  ring

end I4SourceActualFoldCandidate
