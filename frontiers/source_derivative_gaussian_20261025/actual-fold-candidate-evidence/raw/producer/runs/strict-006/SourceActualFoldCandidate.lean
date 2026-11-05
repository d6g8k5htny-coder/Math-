import SourceActualFoldH0
import Mathlib.LinearAlgebra.FiniteDimensional.Lemmas

/-! Literal Lifetime critical types for the unchanged actual source, together
with its attained death and ordinary-H0 interval. No canonical elder partner
or global conditional Morse assertion is made. -/

noncomputable section
open Set MeasureTheory
open UniversalLaw.Spec.Lifetime I4LifetimeField I4SmoothCarrier
open I4SourceConfluentPins I4SourceRawPinConditioning
open I4SourceCompactTargetMoments I4SourceAdaptiveFoldChart
open I4SourceAdaptiveFoldEstimates AdaptiveFoldTransverseRidge AdaptiveFoldBoundaryPath
set_option autoImplicit false

namespace I4SourceActualFoldCandidate

open AdaptiveFoldScalar (J)
open scoped ContDiff

/-- Two coordinate directional pins give the whole derivative, before transport. -/
theorem derivative_zero_of_coordinate_pins
    (D : (Fin 2 → ℝ) →L[ℝ] ℝ)
    (hx : D directionX = 0) (hy : D directionY = 0) : D = 0 := by
  ext q
  have hq : q = q 0 • directionX + q 1 • directionY := by
    ext i
    fin_cases i <;> simp [directionX, directionY]
  rw [hq, map_add, map_smul, map_smul, hx, hy]
  simp

/-- The forward criticality implication uses actual smoothness and the chain rule. -/
theorem actual_critical_of_coordinate_pins {L : ℝ} (hL : 0 < L)
    (sample : SmoothSample 2 L) (x : E 2)
    (hx : fderiv ℝ (smoothSourceField 2 L sample) (coordinates 2 x) directionX = 0)
    (hy : fderiv ℝ (smoothSourceField 2 L sample) (coordinates 2 x) directionY = 0) :
    IsCriticalPoint 2 (actualField 2 L sample) x := by
  have hd := (smoothSourceField_smooth 2 hL.ne' sample).differentiable (by simp)
  have hc := (hd (coordinates 2 x)).hasFDerivAt.comp x (coordinates 2).hasFDerivAt
  change fderiv ℝ (actualField 2 L sample) x = 0
  rw [show fderiv ℝ (actualField 2 L sample) x =
    (fderiv ℝ (smoothSourceField 2 L sample) (coordinates 2 x)).comp
      (coordinates 2).toContinuousLinearMap from hc.fderiv]
  rw [derivative_zero_of_coordinate_pins _ hx hy]
  rfl

/-- Both literal endpoint lifts are critical under the original six raw pins. -/
theorem actual_rawPins_critical {L r b k : ℝ} (hL : 0 < L)
    (sample : SmoothSample 2 L)
    (hp : rawPins L r sample = ![b,b-k*r^3,0,0,0,0]) :
    IsCriticalPoint 2 (actualField 2 L sample) ((coordinates 2).symm (endpointM r)) ∧
      IsCriticalPoint 2 (actualField 2 L sample) ((coordinates 2).symm (endpointS r)) := by
  have h2 := congrFun hp (2 : Fin 6)
  have h3 := congrFun hp (3 : Fin 6)
  have h4 := congrFun hp (4 : Fin 6)
  have h5 := congrFun hp (5 : Fin 6)
  simp [rawPins] at h2 h3 h4 h5
  constructor
  · apply actual_critical_of_coordinate_pins hL sample
    · simpa only [ContinuousLinearEquiv.apply_symm_apply] using h2
    · simpa only [ContinuousLinearEquiv.apply_symm_apply] using h4
  · apply actual_critical_of_coordinate_pins hL sample
    · simpa only [ContinuousLinearEquiv.apply_symm_apply] using h3
    · simpa only [ContinuousLinearEquiv.apply_symm_apply] using h5

/-- Actual Hessians transport every pair of vectors through the literal
continuous linear coordinate equivalence. This makes no isometry assertion. -/
theorem actual_hessian_coordinates {L : ℝ} (hL : 0 < L)
    (sample : SmoothSample 2 L) (x v w : E 2) :
    hessian 2 (actualField 2 L sample) x v w =
      iteratedFDeriv ℝ 2 (smoothSourceField 2 L sample) (coordinates 2 x)
        ![coordinates 2 v, coordinates 2 w] := by
  have h := (coordinates 2).toContinuousLinearMap.iteratedFDeriv_comp_right
    (smoothSourceField_smooth 2 hL.ne' sample) x (i := 2) (by simp)
  have hh := congrArg (fun D => D ![v,w]) h
  have hdirs : (fun i => coordinates 2 (![v,w] i)) =
      ![coordinates 2 v, coordinates 2 w] := by
    ext i
    fin_cases i <;> rfl
  change iteratedFDeriv ℝ 2 (fun y => smoothSourceField 2 L sample (coordinates 2 y)) x ![v,w] = _
  simpa only [Function.comp_def,
    ContinuousMultilinearMap.compContinuousLinearMap_apply,
    ContinuousLinearEquiv.coe_coe, hdirs] using hh

/-- The physical Hessian amplitude is 6kr after both spatial derivatives;
the physical potential itself retains the positive amplitude 6kr³. -/
theorem actual_hessian_physical {L r k : ℝ} (hL : 0 < L)
    (sample : SmoothSample 2 L) (hr : 0 < r) (hk : 0 < k)
    (p : ℝ × ℝ) (v w : E 2) :
    hessian 2 (actualField 2 L sample)
        ((coordinates 2).symm (r • ![p.1,p.2])) v w =
      (6*k*r) * iteratedFDeriv ℝ 2 (actualFoldPotential r k sample) p
        ![(coordinates 2 v 0, coordinates 2 v 1),
          (coordinates 2 w 0, coordinates 2 w 1)] := by
  rw [actual_hessian_coordinates hL, ContinuousLinearEquiv.apply_symm_apply]
  let vv : Fin 2 → ℝ × ℝ :=
    ![(coordinates 2 v 0, coordinates 2 v 1),
      (coordinates 2 w 0, coordinates 2 w 1)]
  have hj := I4ActualFoldChartJets.pullback_jet (smoothSourceField 2 L sample)
    (smoothSourceField_smooth 2 hL.ne' sample) 2 (6*k*r^3)⁻¹ r p vv
  have hV : (fun q : ℝ × ℝ => (6*k*r^3)⁻¹ *
      smoothSourceField 2 L sample (r • ![q.1,q.2])) = actualFoldPotential r k sample := by
    ext q
    simp [actualFoldPotential, div_eq_mul_inv, mul_comm]
  rw [hV] at hj
  have hdirs : (fun i => ![(vv i).1,(vv i).2]) =
      ![coordinates 2 v, coordinates 2 w] := by
    ext i j
    fin_cases i <;> fin_cases j <;> rfl
  rw [hdirs] at hj
  change _ = (6*k*r) * iteratedFDeriv ℝ 2 (actualFoldPotential r k sample) p vv
  rw [hj]
  field_simp [hr.ne', hk.ne']

/-- Exact absolute heights are retained from the original raw pin values. -/
theorem actual_rawPins_heights {L r b k : ℝ} (sample : SmoothSample 2 L)
    (hp : rawPins L r sample = ![b,b-k*r^3,0,0,0,0]) :
    actualField 2 L sample ((coordinates 2).symm (endpointM r)) = b ∧
      actualField 2 L sample ((coordinates 2).symm (endpointS r)) = b-k*r^3 ∧
      heightGap 2 (actualField 2 L sample)
        ((coordinates 2).symm (endpointM r))
        ((coordinates 2).symm (endpointS r)) = k*r^3 := by
  have hm := congrFun hp (0 : Fin 6)
  have hs := congrFun hp (1 : Fin 6)
  simp only [rawPins, Matrix.cons_val_zero, Matrix.cons_val_one] at hm hs
  have hM : actualField 2 L sample ((coordinates 2).symm (endpointM r)) = b := by
    simpa only [actualField, ContinuousLinearEquiv.apply_symm_apply] using hm
  have hS : actualField 2 L sample ((coordinates 2).symm (endpointS r)) = b-k*r^3 := by
    simpa only [actualField, ContinuousLinearEquiv.apply_symm_apply] using hs
  exact ⟨hM,hS,by rw [heightGap,hM,hS]; ring⟩

/-- The product AddCircle torus field pulls back to the literal Lifetime field
on every real-cover point of the unchanged original sample. -/
theorem actual_torus_lifetime_pullback {L : ℝ} (hL : 0 < L)
    (sample : SmoothSample 2 L) (x : E 2) :
    SourceActualFoldTorus.actualTorusField hL.ne' sample
        (I4Torus.torusProjection 2 L (coordinates 2 x)) = actualField 2 L sample x := by
  exact SourceActualFoldTorus.actualTorusField_pullback hL.ne' sample (coordinates 2 x)

/-- Values of any given old Lifetime interface agree with the actual real-cover
strict cut. This compares interface values without asserting an elder relation. -/
theorem interface_values_eq_actual {L : ℝ} (hL : 0 < L)
    (sample : SmoothSample 2 L) (I : SuperlevelBarInterface 2 L) (x : E 2)
    (hne : ¬ TorusFiltration.superlevelBar_isEssential (actualField 2 L sample) x) :
    ¬ I.IsEssential (actualField 2 L sample) x ∧
      I.deathHeight (actualField 2 L sample) x =
        TorusFiltration.superlevelBar_deathHeight (actualField 2 L sample) x := by
  have hs := actualField_smooth 2 hL sample
  have hp := actualField_periodic 2 hL sample
  have hc := I4SourceActualFoldDeath.actualField_continuous hL.ne' sample
  have hI : ¬ I.IsEssential (actualField 2 L sample) x := by
    intro hh
    exact hne ((I.essential_iff _ hs hp x).mp hh)
  refine ⟨hI,?_⟩
  apply eq_of_forall_lt_iff
  intro a
  rw [I.deathHeight_maximin _ hs hp x hI a,
    TorusFiltration.superlevelBar_strict_cut _ hc x hne a]
  rfl

/- Integrated once from frozen candidate_distance helper; section SHA256 fa9c5cedf0c740802ff211b5f232ae343f8483a5df03f7708ce3ce7f3a9e5ef3. No helper kernel. -/
/-- The literal Lifetime Euclidean lift of the unchanged source maximum pin. -/
def endpointLiftM (r : ℝ) : E 2 :=
  (I4LifetimeField.coordinates 2).symm (I4SourceConfluentPins.endpointM r)

/-- The literal Lifetime Euclidean lift of the unchanged source saddle pin. -/
def endpointLiftS (r : ℝ) : E 2 :=
  (I4LifetimeField.coordinates 2).symm (I4SourceConfluentPins.endpointS r)

@[simp] theorem coordinates_endpointLiftM (r : ℝ) :
    I4LifetimeField.coordinates 2 (endpointLiftM r) =
      I4SourceConfluentPins.endpointM r := by
  simp [endpointLiftM]

@[simp] theorem coordinates_endpointLiftS (r : ℝ) :
    I4LifetimeField.coordinates 2 (endpointLiftS r) =
      I4SourceConfluentPins.endpointS r := by
  simp [endpointLiftS]

/-- The real-cover maximum lift projects to exactly the existing product-torus pin. -/
@[simp] theorem torusProjection_endpointLiftM (L r : ℝ) :
    I4Torus.torusProjection 2 L (I4LifetimeField.coordinates 2 (endpointLiftM r)) =
      I4Torus.torusProjection 2 L (I4SourceConfluentPins.endpointM r) := by
  rw [coordinates_endpointLiftM]

/-- The real-cover saddle lift projects to exactly the existing product-torus pin. -/
@[simp] theorem torusProjection_endpointLiftS (L r : ℝ) :
    I4Torus.torusProjection 2 L (I4LifetimeField.coordinates 2 (endpointLiftS r)) =
      I4Torus.torusProjection 2 L (I4SourceConfluentPins.endpointS r) := by
  rw [coordinates_endpointLiftS]

@[simp] theorem endpointLiftM_apply (r : ℝ) (i : Fin 2) :
    endpointLiftM r i = I4SourceConfluentPins.endpointM r i := by
  change (I4LifetimeField.coordinates 2 (endpointLiftM r)) i = _
  rw [coordinates_endpointLiftM]

@[simp] theorem endpointLiftS_apply (r : ℝ) (i : Fin 2) :
    endpointLiftS r i = I4SourceConfluentPins.endpointS r i := by
  change (I4LifetimeField.coordinates 2 (endpointLiftS r)) i = _
  rw [coordinates_endpointLiftS]

/-- Parent-norm length for the unshifted Euclidean pin difference. -/
theorem endpoint_lifts_sub_norm {r : ℝ} (hr : 0 ≤ r) :
    ‖endpointLiftM r - endpointLiftS r‖ = r := by
  have heq : endpointLiftM r - endpointLiftS r =
      EuclideanSpace.single (0 : Fin 2) (-r) := by
    ext i
    fin_cases i <;>
      simp [I4SourceConfluentPins.endpointM, I4SourceConfluentPins.endpointS]; ring
  rw [heq, PiLp.norm_single, Real.norm_eq_abs, abs_neg, abs_of_nonneg hr]

/-- Every actual parent lattice shift has length at least the pin distance.
Only the zeroth Euclidean component is needed. -/
theorem endpoint_lifts_lattice_lower {L r : ℝ} (hL : 0 < L)
    (hrL : r < L / 2) (n : Fin 2 → ℤ) :
    r ≤ ‖endpointLiftM r - endpointLiftS r + latticeVec 2 L n‖ := by
  have hcoord : (endpointLiftM r - endpointLiftS r + latticeVec 2 L n) 0 =
      -r + L * (n 0 : ℝ) := by
    have hl := congrFun (I4LifetimeField.coordinates_latticeVec 2 L n) 0
    simp only [I4LifetimeField.coordinates_apply] at hl
    simp [I4SourceConfluentPins.endpointM, I4SourceConfluentPins.endpointS, hl]
    ring
  have habs : r ≤ |-r + L * (n 0 : ℝ)| := by
    by_cases hn : n 0 ≤ 0
    · have hnR : (n 0 : ℝ) ≤ 0 := by exact_mod_cast hn
      have hm : L * (n 0 : ℝ) ≤ 0 := mul_nonpos_of_nonneg_of_nonpos hL.le hnR
      exact (le_abs).2 (Or.inr (by linarith))
    · have hn1 : 1 ≤ n 0 := by omega
      have hnR : (1 : ℝ) ≤ (n 0 : ℝ) := by exact_mod_cast hn1
      have hm : L ≤ L * (n 0 : ℝ) := by nlinarith
      exact (le_abs).2 (Or.inl (by linarith))
  calc
    r ≤ |-r + L * (n 0 : ℝ)| := habs
    _ = ‖(endpointLiftM r - endpointLiftS r + latticeVec 2 L n) 0‖ := by
      rw [hcoord, Real.norm_eq_abs]
    _ ≤ ‖endpointLiftM r - endpointLiftS r + latticeVec 2 L n‖ :=
      PiLp.norm_apply_le _ _

/-- Literal Lifetime lattice-infimum distance, without a quotient-carrier comparison. -/
theorem endpoint_lifts_torusDist {L r : ℝ} (hL : 0 < L)
    (hr : 0 < r) (hrL : r < L / 2) :
    torusDist 2 L (endpointLiftM r) (endpointLiftS r) = r := by
  apply le_antisymm
  · have hb : BddBelow (Set.range (fun n : Fin 2 → ℤ =>
        ‖endpointLiftM r - endpointLiftS r + latticeVec 2 L n‖)) :=
      ⟨0, by rintro _ ⟨n, rfl⟩; exact norm_nonneg _⟩
    have hz : latticeVec 2 L (0 : Fin 2 → ℤ) = 0 := by
      ext i
      fin_cases i <;> simp [latticeVec]
    exact (ciInf_le hb (0 : Fin 2 → ℤ)).trans (by
      rw [hz, add_zero, endpoint_lifts_sub_norm hr.le])
  · exact le_ciInf (endpoint_lifts_lattice_lower hL hrL)

/-- The endpoint separation can wrap through a full parent period. -/
theorem endpoint_lifts_torusDist_unit_zero :
    torusDist 2 1 (endpointLiftM 1) (endpointLiftS 1) = 0 := by
  apply le_antisymm
  · have hb : BddBelow (Set.range (fun n : Fin 2 → ℤ =>
        ‖endpointLiftM 1 - endpointLiftS 1 + latticeVec 2 1 n‖)) :=
      ⟨0, by rintro _ ⟨n, rfl⟩; exact norm_nonneg _⟩
    have hz : endpointLiftM 1 - endpointLiftS 1 +
        latticeVec 2 1 (![1, 0] : Fin 2 → ℤ) = 0 := by
      ext i
      fin_cases i <;>
        norm_num [I4SourceConfluentPins.endpointM, I4SourceConfluentPins.endpointS,
          latticeVec, PiLp.single_apply]
    exact (ciInf_le hb (![1, 0] : Fin 2 → ℤ)).trans (by rw [hz, norm_zero])
  · exact le_ciInf (fun _ => norm_nonneg _)

/-- Concrete witness that deleting the small-radius bound makes the distance claim false. -/
theorem endpoint_lifts_torusDist_unit_ne_radius :
    torusDist 2 1 (endpointLiftM 1) (endpointLiftS 1) ≠ 1 := by
  rw [endpoint_lifts_torusDist_unit_zero]
  norm_num


/- Integrated once from frozen candidate_ridge_schur helper; section SHA256 2f4a3032869f7bc32e699a9af8b2782481c5fd950daaa4f5d7596c8c5fd24240. No helper kernel. -/
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
  simp only [map_add, map_smul, add_apply,
    smul_apply, smul_eq_mul]
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
  simp only [Matrix.cons_val_zero, Matrix.cons_val_one]
  rw [planar_bilinear_quadratic, ← hx, ← hxy, ← hyx, ← hy,
    actual_Hy_eq_Gx hL sample p]
  ring



/- Integrated once from frozen candidate_inertia helper; section SHA256 0198ffd831534bbc0e207cdfe17c8de3a3b0bde1e6c46a6638ca0deb9033dcdd. No helper kernel. -/
/-- Scalar square completion for the planar Schur complement. -/
theorem planar_quadratic_complete_square (a b c u v : ℝ) (hc : c ≠ 0) :
    a * u^2 + 2 * b * u * v + c * v^2 =
      (a - b^2 / c) * u^2 + c * (v + b / c * u)^2 := by
  field_simp
  ring

/-- A negative diagonal square completion gives the literal Lifetime inertia 2. -/
theorem hessianHasInertia_two_of_diag
    (g : E 2 → ℝ) (x : E 2) (α s c : ℝ)
    (hα : 0 < α) (hs : s < 0) (hc : c < 0) (β : ℝ)
    (hQ : ∀ v : E 2, hessian 2 g x v v =
      α * (s * (coordinates 2 v 0)^2 +
        c * (coordinates 2 v 1 + β * coordinates 2 v 0)^2)) :
    HessianHasInertia 2 g x 2 := by
  refine ⟨⊤, ⊥, isCompl_top_bot, ?_, ?_, ?_, ?_⟩
  · simp [E]
  · simp
  · intro v _ hv
    have hA : s * (coordinates 2 v 0)^2 ≤ 0 :=
      mul_nonpos_of_nonpos_of_nonneg hs.le (sq_nonneg _)
    have hC : c * (coordinates 2 v 1 + β * coordinates 2 v 0)^2 ≤ 0 :=
      mul_nonpos_of_nonpos_of_nonneg hc.le (sq_nonneg _)
    rw [hQ]
    apply mul_neg_of_pos_of_neg hα
    by_cases h0 : coordinates 2 v 0 = 0
    · have h1 : coordinates 2 v 1 ≠ 0 := by
        intro h1
        apply hv
        apply (coordinates 2).injective
        ext i
        fin_cases i <;> simp_all
      have hC' : c * (coordinates 2 v 1 + β * coordinates 2 v 0)^2 < 0 := by
        simpa [h0] using mul_neg_of_neg_of_pos hc (sq_pos_of_ne_zero h1)
      exact add_neg_of_nonpos_of_neg hA hC'
    · exact add_neg_of_neg_of_nonpos
        (mul_neg_of_neg_of_pos hs (sq_pos_of_ne_zero h0)) hC
  · intro w hw hw0
    exact (hw0 ((Submodule.mem_bot ℝ).mp hw)).elim

/-- A diagonal square completion with one negative and one positive coefficient
has the literal Lifetime inertia 1. The complementary lines are generated by
`coordinates.symm ![0,1]` and `coordinates.symm ![1,-β]`. -/
theorem hessianHasInertia_one_of_diag
    (g : E 2 → ℝ) (x : E 2) (α s c : ℝ)
    (hα : 0 < α) (hs : 0 < s) (hc : c < 0) (β : ℝ)
    (hQ : ∀ v : E 2, hessian 2 g x v v =
      α * (s * (coordinates 2 v 0)^2 +
        c * (coordinates 2 v 1 + β * coordinates 2 v 0)^2)) :
    HessianHasInertia 2 g x 1 := by
  let n : E 2 := (coordinates 2).symm ![0,1]
  let p : E 2 := (coordinates 2).symm ![1,-β]
  have hn0 : coordinates 2 n 0 = 0 := by
    change (coordinates 2 ((coordinates 2).symm ![0,1])) 0 = 0
    rw [(coordinates 2).apply_symm_apply]
    rfl
  have hn1 : coordinates 2 n 1 = 1 := by
    change (coordinates 2 ((coordinates 2).symm ![0,1])) 1 = 1
    rw [(coordinates 2).apply_symm_apply]
    rfl
  have hp0 : coordinates 2 p 0 = 1 := by
    change (coordinates 2 ((coordinates 2).symm ![1,-β])) 0 = 1
    rw [(coordinates 2).apply_symm_apply]
    rfl
  have hp1 : coordinates 2 p 1 = -β := by
    change (coordinates 2 ((coordinates 2).symm ![1,-β])) 1 = -β
    rw [(coordinates 2).apply_symm_apply]
    rfl
  have hn : n ≠ 0 := by
    intro h
    have h1 := congrArg (fun v : E 2 => coordinates 2 v 1) h
    simp only [hn1, map_zero, Pi.zero_apply, one_ne_zero] at h1
  have hp : p ≠ 0 := by
    intro h
    have h0 := congrArg (fun v : E 2 => coordinates 2 v 0) h
    simp only [hp0, map_zero, Pi.zero_apply, one_ne_zero] at h0
  have hndim : Module.finrank ℝ (Submodule.span ℝ {n}) = 1 :=
    finrank_span_singleton hn
  have hpdim : Module.finrank ℝ (Submodule.span ℝ {p}) = 1 :=
    finrank_span_singleton hp
  have hdisj : Disjoint (Submodule.span ℝ {n}) (Submodule.span ℝ {p}) := by
    rw [Submodule.disjoint_def]
    intro v hvn hvp
    obtain ⟨a, ha⟩ := Submodule.mem_span_singleton.mp hvn
    obtain ⟨b, hb⟩ := Submodule.mem_span_singleton.mp hvp
    have h0 := congrArg (fun v : E 2 => coordinates 2 v 0) (ha.trans hb.symm)
    have hb0 : b = 0 := by
      simpa only [map_smul, Pi.smul_apply, smul_eq_mul, hn0, hp0,
        mul_one, mul_zero] using h0.symm
    simpa [hb0] using hb.symm
  have hcompl : IsCompl (Submodule.span ℝ {n}) (Submodule.span ℝ {p}) := by
    apply (Submodule.isCompl_iff_disjoint _ _ ?_).mpr hdisj
    simp [E, hndim, hpdim]
  refine ⟨Submodule.span ℝ {n}, Submodule.span ℝ {p}, hcompl, hndim, ?_, ?_, ?_⟩
  · simpa using hpdim
  · intro v hv hv0
    obtain ⟨t, rfl⟩ := Submodule.mem_span_singleton.mp hv
    have ht : t ≠ 0 := by
      intro ht
      apply hv0
      simp [ht]
    rw [hQ]
    have hneg := mul_neg_of_pos_of_neg hα
      (mul_neg_of_neg_of_pos hc (sq_pos_of_ne_zero ht))
    simpa only [map_smul, Pi.smul_apply, smul_eq_mul, hn0, hn1,
      mul_zero, mul_one, zero_pow (by decide : 2 ≠ 0), add_zero,
      zero_add] using hneg
  · intro v hv hv0
    obtain ⟨t, rfl⟩ := Submodule.mem_span_singleton.mp hv
    have ht : t ≠ 0 := by
      intro ht
      apply hv0
      simp [ht]
    rw [hQ]
    have hpos := mul_pos hα (mul_pos hs (sq_pos_of_ne_zero ht))
    have hzero : t * -β + β * t = 0 := by ring
    simpa only [map_smul, Pi.smul_apply, smul_eq_mul, hp0, hp1, mul_one,
      hzero, zero_pow (by decide : 2 ≠ 0), mul_zero, add_zero] using hpos


/-- Completion of the physical coordinate quadratic form uses the literal
negative transverse entry and the same retained ridge Schur complement. -/
theorem actual_hessian_complete_square {L r k : ℝ} (hL : 0 < L)
    (sample : SmoothSample 2 L) (hr : 0 < r) (hk : 0 < k) (p : ℝ × ℝ)
    (hc : partialY (Vy (actualFoldPotential r k sample)) p ≠ 0) (v : E 2) :
    let V := actualFoldPotential r k sample
    hessian 2 (actualField 2 L sample)
        ((coordinates 2).symm (r • ![p.1,p.2])) v v =
      (6*k*r) * ((partialX (Vx V) p - (partialY (Vx V) p)^2 / partialY (Vy V) p) *
        (coordinates 2 v 0)^2 + partialY (Vy V) p *
          (coordinates 2 v 1 + partialY (Vx V) p / partialY (Vy V) p *
            coordinates 2 v 0)^2) := by
  dsimp only
  rw [actual_hessian_physical hL sample hr hk,
    actual_planar_hessian_quadratic hL.ne' sample]
  rw [planar_quadratic_complete_square _ _ _ _ _ hc]

/-- Raw zero-gradient pins and the actual retained ridge derive the genuine
Lifetime strict maximum and index-one saddle, with no desired type premise. -/
theorem actual_rawPins_ridge_types {L r k b : ℝ} (hL : 0 < L)
    (sample : SmoothSample 2 L) (hr : 0 < r) (hk : 0 < k)
    (hp : rawPins L r sample = ![b,b-k*r^3,0,0,0,0])
    {O : Set (ℝ × ℝ)} {R c M₀ M₁ M₂ A : ℝ} {U : Set ℝ} {z : ℝ → ℝ}
    (hs : StructuralRectangleData (actualFoldPotential r k sample) O R c M₀ M₁ M₂ A)
    (hz : RidgeScalarData (actualFoldPotential r k sample) O R c M₀ M₁ M₂ U z) :
    IsNondegMax 2 (actualField 2 L sample) (endpointLiftM r) ∧
      IsIndexSaddle 2 (actualField 2 L sample) (endpointLiftS r) := by
  obtain ⟨hcritM,hcritS⟩ := actual_rawPins_critical hL sample hp
  obtain ⟨hcM,hsM,hcS,hsS⟩ := actual_endpoint_schur_signs hL.ne' sample hs hz
  let V := actualFoldPotential r k sample
  have hα : 0 < 6*k*r := by positivity
  have hM : HessianHasInertia 2 (actualField 2 L sample) (endpointLiftM r) 2 := by
    apply hessianHasInertia_two_of_diag _ _ (6*k*r) _ _ hα hsM hcM
      (partialY (Vx V) (-(1/2),0) / partialY (Vy V) (-(1/2),0))
    intro v
    simpa only [endpointLiftM, ← neg_div, chart_endpointM] using
      actual_hessian_complete_square hL sample hr hk (-(1/2),0) hcM.ne v
  have hS : HessianHasInertia 2 (actualField 2 L sample) (endpointLiftS r) 1 := by
    apply hessianHasInertia_one_of_diag _ _ (6*k*r) _ _ hα hsS hcS
      (partialY (Vx V) (1/2,0) / partialY (Vy V) (1/2,0))
    intro v
    simpa only [endpointLiftS, chart_endpointS] using
      actual_hessian_complete_square hL sample hr hk (1/2,0) hcS.ne v
  exact ⟨⟨hcritM,hM⟩,⟨hcritS,hS⟩⟩

/-- Pointwise geometric composition on one unchanged actual source sample. -/
theorem actual_rawPins_ridge_candidate {L r k b : ℝ} (hL : 0 < L)
    (sample : SmoothSample 2 L) (hr : 0 < r) (hrL : r < L/2) (hk : 0 < k)
    (hp : rawPins L r sample = ![b,b-k*r^3,0,0,0,0])
    {O : Set (ℝ × ℝ)} {R c M₀ M₁ M₂ A : ℝ} {U : Set ℝ} {z : ℝ → ℝ}
    (hs : StructuralRectangleData (actualFoldPotential r k sample) O R c M₀ M₁ M₂ A)
    (hz : RidgeScalarData (actualFoldPotential r k sample) O R c M₀ M₁ M₂ U z) :
    IsCandidatePair 2 L (actualField 2 L sample) (endpointLiftM r) (endpointLiftS r) ∧
      torusDist 2 L (endpointLiftM r) (endpointLiftS r) = r ∧
      heightGap 2 (actualField 2 L sample) (endpointLiftM r) (endpointLiftS r) = k*r^3 ∧
      0 < heightGap 2 (actualField 2 L sample) (endpointLiftM r) (endpointLiftS r) := by
  obtain ⟨hM,hS⟩ := actual_rawPins_ridge_types hL sample hr hk hp hs hz
  have hd := endpoint_lifts_torusDist hL hr hrL
  have hg : heightGap 2 (actualField 2 L sample) (endpointLiftM r) (endpointLiftS r) = k*r^3 :=
    (actual_rawPins_heights sample hp).2.2
  exact ⟨⟨hM,hS,by rw [hd]; exact hr⟩,hd,hg,by rw [hg]; positivity⟩

open SourceActualFoldTorus I4Torus TorusFiltration CategoryTheory Limits

/-- One radius from the genuine old Lifetime restriction 0<L precedes the
coefficient field and every scale and target. Only the two established sample
cutoffs remain: all raw pins, structural data, strict types, attained real-cover
death and the same original-torus ordinary-H0 summand are derived internally. -/
theorem sourceGapLaw_actual_candidate_death_h0 {L : ℝ} (hL : 0 < L) :
    ∃ δ : ℝ, 0 < δ ∧ δ ≤ 1 ∧ δ ≤ L/2 ∧
      ∀ (K : Type) [Field K],
      ∀ k₀ : ℝ, 0 < k₀ → ∀ r : ℝ, 0 < r → r < δ →
        ∀ b k : ℝ, k₀ ≤ k → ∀ᵐ sample ∂sourceGapLaw hL.ne' r b k,
          let T := sourceT k₀ sample
          let κ := sourceKappa r k sample
          let R := 4/Real.sqrt κ
          let g := actualField 2 L sample
          r*T^5 ≤ 1/100 → 1024*T^5 ≤ κ →
            ∃ (U : Set ℝ) (z : ℝ → ℝ),
              RidgeScalarData (actualFoldPotential r k sample)
                univ R (κ/2) T (3*T) T U z ∧
              IsCandidatePair 2 L g (endpointLiftM r) (endpointLiftS r) ∧
              torusDist 2 L (endpointLiftM r) (endpointLiftS r) = r ∧
              g (endpointLiftM r) = b ∧ g (endpointLiftS r) = b-k*r^3 ∧
              heightGap 2 g (endpointLiftM r) (endpointLiftS r) = k*r^3 ∧
              0 < heightGap 2 g (endpointLiftM r) (endpointLiftS r) ∧
              ¬ superlevelBar_isEssential g (endpointLiftM r) ∧
              superlevelBar_deathHeight g (endpointLiftM r) = g (endpointLiftS r) ∧
              superlevelBar_clearanceSet g (endpointLiftM r) = Iio (g (endpointLiftS r)) ∧
              ∃ ET : ElderTrap (actualTorusField hL.ne' sample)
                  (torusProjection 2 L (endpointM r)) (torusPhysicalMap L r (olderPoint z))
                  b (b-k*r^3) (torusPhysicalMap L r '' leftBox R),
                b + (3/2)*k*r^3 ≤
                  actualTorusField hL.ne' sample (torusPhysicalMap L r (olderPoint z)) ∧
                (∃ η : Path (torusProjection 2 L (endpointM r))
                    (torusPhysicalMap L r (olderPoint z)),
                  (∀ t : unitInterval, b-k*r^3 ≤ actualTorusField hL.ne' sample (η t)) ∧
                    η pathMidpoint = torusProjection 2 L (endpointS r)) ∧
                strictClearanceSet (actualTorusField hL.ne' sample)
                    (torusProjection 2 L (endpointM r)) = Iio (b-k*r^3) ∧
                strictClearanceDeath (actualTorusField hL.ne' sample)
                    (torusProjection 2 L (endpointM r)) = b-k*r^3 ∧
                Nonempty (superlevel_h0Filtration (actualTorusField hL.ne' sample)
                    (ModuleCat.of K K) ≅ elderInterval K b (b-k*r^3) ⊞
                    kernel (elderRetraction (k := K) ET)) := by
  obtain ⟨δ₁,hδ₁,hδ₁1,hwide⟩ := sourceGapLaw_actual_rectangle_boundary_path hL.ne'
  obtain ⟨_C,δ₂,_hC,hδ₂,_hδ₂1,hbounds⟩ := sourceInverse_target_uniform_bounds hL.ne'
  refine ⟨min (min δ₁ δ₂) (L/2), lt_min (lt_min hδ₁ hδ₂) (by linarith : (0:ℝ) < L/2),
    ((min_le_left _ _).trans (min_le_left _ _)).trans hδ₁1, min_le_right _ _, ?_⟩
  intro K instK k₀ hk₀ r hr hrδ b k hk
  have hr₁ : r < δ₁ := hrδ.trans_le ((min_le_left _ _).trans (min_le_left _ _))
  have hr₂ : r < δ₂ := hrδ.trans_le ((min_le_left _ _).trans (min_le_right _ _))
  have hrL : r < L/2 := hrδ.trans_le (min_le_right _ _)
  have hG := (hbounds r hr hr₂).1
  have hpins : ∀ᵐ sample ∂sourceGapLaw hL.ne' r b k,
      rawPins L r sample = ![b,b-k*r^3,0,0,0,0] := by
    rw [sourceGapLaw_eq_rawPinKernel hL.ne' r b k hr.ne']
    have hm : MeasurableSet {sample : SmoothSample 2 L |
        rawPins L r sample = ![b,b-k*r^3,0,0,0,0]} :=
      measurableSet_eq_fun (rawPins_measurable hL.ne' r) measurable_const
    apply (ae_iff_measure_eq hm.nullMeasurableSet).mpr
    simpa using rawPinKernel_pin_fiber hL.ne' r hr.ne' hG ![b,b-k*r^3,0,0,0,0]
  filter_upwards [hwide k₀ hk₀ r hr hr₁ b k hk,hpins] with sample hw hp
  dsimp only at hw ⊢
  intro hrT hκ
  obtain ⟨U,z,hz,hbox⟩ := hw hrT hκ
  have hkpos := hk₀.trans_le hk
  have hN := actualFoldPotential_normalized_data_of_rawPins hL.ne' sample hr hkpos hp
  have hs := (actual_structural_rectangle hL.ne' sample hr hk₀ hk hN hrT hκ).1
  obtain ⟨hcan,hd,hgap,hpos⟩ := actual_rawPins_ridge_candidate hL sample hr hrL hkpos hp hs hz
  obtain ⟨hM,hS,_⟩ := actual_rawPins_heights sample hp
  obtain ⟨hreald,hrealc⟩ := I4SourceActualFoldDeath.actual_rectangle_death
    hL.ne' sample z hr hkpos hp hbox
  have hne : ¬ superlevelBar_isEssential (actualField 2 L sample) (endpointLiftM r) := by
    apply (superlevelBar_clearance_nonempty_iff _
      (I4SourceActualFoldDeath.actualField_continuous hL.ne' sample) _).mp
    refine ⟨b-k*r^3-1,?_⟩
    rw [show superlevelBar_clearanceSet (actualField 2 L sample) (endpointLiftM r) =
      Iio (b-k*r^3) from hrealc]
    exact sub_one_lt _
  obtain ⟨ht,hgain,hpath,hclear,hdeath⟩ :=
    actual_rectangle_torus hL.ne' sample z hr hkpos hp hbox
  refine ⟨U,z,hz,hcan,hd,hM,hS,hgap,hpos,hne,?_,?_,
    SourceActualFoldH0.toElderTrap ht,hgain,hpath,hclear,hdeath,?_⟩
  · exact hreald.trans hS.symm
  · exact hrealc.trans (congrArg Iio hS.symm)
  · exact ⟨elderDirectSummand (k := K) (SourceActualFoldH0.toElderTrap ht)⟩

end I4SourceActualFoldCandidate
