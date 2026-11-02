import AdaptiveFoldTransverseRidge
import AdaptiveFoldScalarBarrier
import Mathlib.Topology.Path
import Mathlib.Topology.Constructions.SumProd

/-! Construct one transverse ridge from literal rectangle derivatives, then retain
that witness in normalized scalar, rectangle boundary, and attained path data.
The Gaussian/source and physical chart joins are outside this module. -/

noncomputable section
open Set
open scoped Topology ContDiff

namespace AdaptiveFoldBoundaryPath
open AdaptiveFoldTransverseRidge
open AdaptiveFoldScalar (J)

def slopeRadius (c M₁ : ℝ) : ℝ := M₁ / c
def accelerationRadius (c M₁ M₂ : ℝ) : ℝ := (M₂ / c) * (1 + M₁ / c) ^ 2
def profileError (c M₁ M₂ : ℝ) : ℝ :=
  M₂ * (2 * (M₁ / c) + (M₁ / c) ^ 2) + M₁ * accelerationRadius c M₁ M₂

/-- All input estimates refer to literal coordinate derivatives on the rectangle.
The two ordered mixed entries are separate, without a symmetry premise. -/
structure StructuralRectangleData (V : ℝ × ℝ → ℝ) (O : Set (ℝ × ℝ))
    (R c M₀ M₁ M₂ A : ℝ) : Prop where
  radius_pos : 0 < R
  concavity_pos : 0 < c
  center_nonneg : 0 ≤ M₀
  first_nonneg : 0 ≤ M₁
  second_nonneg : 0 ≤ M₂
  domain_open : IsOpen O
  regularity : ContDiffOn ℝ 4 V O
  rectangle_subset : J ×ˢ Icc (-R) R ⊆ O
  vertical_negative : ∀ x ∈ J, ∀ y ∈ Icc (-R) R, partialY (Vy V) (x,y) ≤ -c
  lower_positive : ∀ x ∈ J, 0 < Vy V (x,-R)
  upper_negative : ∀ x ∈ J, Vy V (x,R) < 0
  center_bound : ∀ x ∈ J, |Vy V (x,0)| ≤ M₀
  Gx_bound : ∀ x ∈ J, ∀ y ∈ Icc (-R) R, |partialX (Vy V) (x,y)| ≤ M₁
  Gxx_bound : ∀ x ∈ J, ∀ y ∈ Icc (-R) R,
    |fderiv ℝ (fderiv ℝ (Vy V)) (x,y) ex ex| ≤ M₂
  Gxy_bound : ∀ x ∈ J, ∀ y ∈ Icc (-R) R,
    |fderiv ℝ (fderiv ℝ (Vy V)) (x,y) ex ey| ≤ M₂
  Gyx_bound : ∀ x ∈ J, ∀ y ∈ Icc (-R) R,
    |fderiv ℝ (fderiv ℝ (Vy V)) (x,y) ey ex| ≤ M₂
  Gyy_bound : ∀ x ∈ J, ∀ y ∈ Icc (-R) R,
    |fderiv ℝ (fderiv ℝ (Vy V)) (x,y) ey ey| ≤ M₂
  Hy_bound : ∀ x ∈ J, ∀ y ∈ Icc (-R) R, |partialY (Vx V) (x,y)| ≤ M₁
  Hxx_lower : ∀ x ∈ J, ∀ y ∈ Icc (-R) R,
    A ≤ fderiv ℝ (fderiv ℝ (Vx V)) (x,y) ex ex
  Hxy_bound : ∀ x ∈ J, ∀ y ∈ Icc (-R) R,
    |fderiv ℝ (fderiv ℝ (Vx V)) (x,y) ex ey| ≤ M₂
  Hyx_bound : ∀ x ∈ J, ∀ y ∈ Icc (-R) R,
    |fderiv ℝ (fderiv ℝ (Vx V)) (x,y) ey ex| ≤ M₂
  Hyy_bound : ∀ x ∈ J, ∀ y ∈ Icc (-R) R,
    |fderiv ℝ (fderiv ℝ (Vx V)) (x,y) ey ey| ≤ M₂
  curvature_budget : 1 + profileError c M₁ M₂ ≤ A
  pin_left : Vx V (-(1/2:ℝ),0) = 0 ∧ Vy V (-(1/2:ℝ),0) = 0
  pin_right : Vx V ((1/2:ℝ),0) = 0 ∧ Vy V ((1/2:ℝ),0) = 0
  potential_gap : V (-(1/2:ℝ),0) - V ((1/2:ℝ),0) = 1/6

/-- The two-step error estimate retains all finite coordinate contributions. -/
theorem profileSlopeSecond_error
    {V : ℝ × ℝ → ℝ} {z : ℝ → ℝ} {x c M₁ M₂ : ℝ}
    (_hc : 0 < c) (hM₁ : 0 ≤ M₁) (hM₂ : 0 ≤ M₂)
    (hHy : |partialY (Vx V) (x,z x)| ≤ M₁)
    (hxy : |fderiv ℝ (fderiv ℝ (Vx V)) (x,z x) ex ey| ≤ M₂)
    (hyx : |fderiv ℝ (fderiv ℝ (Vx V)) (x,z x) ey ex| ≤ M₂)
    (hyy : |fderiv ℝ (fderiv ℝ (Vx V)) (x,z x) ey ey| ≤ M₂)
    (hz₁ : |deriv z x| ≤ M₁/c)
    (hz₂ : |deriv (deriv z) x| ≤ accelerationRadius c M₁ M₂) :
    |profileSlopeSecond V z x - fderiv ℝ (fderiv ℝ (Vx V)) (x,z x) ex ex| ≤
      M₂ * (2 * |deriv z x| + |deriv z x| ^ 2) + M₁ * |deriv (deriv z) x| ∧
    M₂ * (2 * |deriv z x| + |deriv z x| ^ 2) + M₁ * |deriv (deriv z) x| ≤
      profileError c M₁ M₂ := by
  constructor
  · unfold profileSlopeSecond
    rw [bilinear_graph_vector, clm_vertical_vector]
    have heq :
        fderiv ℝ (fderiv ℝ (Vx V)) (x,z x) ex ex +
          deriv z x * fderiv ℝ (fderiv ℝ (Vx V)) (x,z x) ex ey +
          deriv z x * fderiv ℝ (fderiv ℝ (Vx V)) (x,z x) ey ex +
          deriv z x ^ 2 * fderiv ℝ (fderiv ℝ (Vx V)) (x,z x) ey ey +
          deriv (deriv z) x * fderiv ℝ (Vx V) (x,z x) ey -
          fderiv ℝ (fderiv ℝ (Vx V)) (x,z x) ex ex =
        deriv z x * fderiv ℝ (fderiv ℝ (Vx V)) (x,z x) ex ey +
          deriv z x * fderiv ℝ (fderiv ℝ (Vx V)) (x,z x) ey ex +
          deriv z x ^ 2 * fderiv ℝ (fderiv ℝ (Vx V)) (x,z x) ey ey +
          deriv (deriv z) x * fderiv ℝ (Vx V) (x,z x) ey := by ring
    rw [heq]
    calc
      _ ≤ |deriv z x * fderiv ℝ (fderiv ℝ (Vx V)) (x,z x) ex ey| +
          |deriv z x * fderiv ℝ (fderiv ℝ (Vx V)) (x,z x) ey ex| +
          |deriv z x ^ 2 * fderiv ℝ (fderiv ℝ (Vx V)) (x,z x) ey ey| +
          |deriv (deriv z) x * fderiv ℝ (Vx V) (x,z x) ey| := by
        have h₁ := abs_add_le
          (deriv z x * fderiv ℝ (fderiv ℝ (Vx V)) (x,z x) ex ey)
          (deriv z x * fderiv ℝ (fderiv ℝ (Vx V)) (x,z x) ey ex)
        have h₂ := abs_add_le
          (deriv z x * fderiv ℝ (fderiv ℝ (Vx V)) (x,z x) ex ey +
           deriv z x * fderiv ℝ (fderiv ℝ (Vx V)) (x,z x) ey ex)
          (deriv z x ^ 2 * fderiv ℝ (fderiv ℝ (Vx V)) (x,z x) ey ey)
        have h₃ := abs_add_le
          (deriv z x * fderiv ℝ (fderiv ℝ (Vx V)) (x,z x) ex ey +
           deriv z x * fderiv ℝ (fderiv ℝ (Vx V)) (x,z x) ey ex +
           deriv z x ^ 2 * fderiv ℝ (fderiv ℝ (Vx V)) (x,z x) ey ey)
          (deriv (deriv z) x * fderiv ℝ (Vx V) (x,z x) ey)
        linarith
      _ = |deriv z x| * |fderiv ℝ (fderiv ℝ (Vx V)) (x,z x) ex ey| +
          |deriv z x| * |fderiv ℝ (fderiv ℝ (Vx V)) (x,z x) ey ex| +
          |deriv z x| ^ 2 * |fderiv ℝ (fderiv ℝ (Vx V)) (x,z x) ey ey| +
          |deriv (deriv z) x| * |partialY (Vx V) (x,z x)| := by
        simp only [abs_mul, abs_pow, partialY]
      _ ≤ |deriv z x| * M₂ + |deriv z x| * M₂ +
          |deriv z x| ^ 2 * M₂ + |deriv (deriv z) x| * M₁ := by gcongr
      _ = _ := by ring
  · unfold profileError
    gcongr

/-- One constructed witness and its analytic consequences. The jets are full
(two-sided), including at the closed interval's endpoints. -/
structure RidgeScalarData (V : ℝ × ℝ → ℝ) (O : Set (ℝ × ℝ))
    (R c M₀ M₁ M₂ : ℝ) (U : Set ℝ) (z : ℝ → ℝ) : Prop where
  domain_open : IsOpen U
  interval_subset : J ⊆ U
  regularity : ContDiffOn ℝ 2 z U
  root : ∀ x ∈ U, z x ∈ Ioo (-R) R ∧ (x,z x) ∈ O ∧ Vy V (x,z x) = 0
  unique : ∀ x ∈ U, ∀ y ∈ Icc (-R) R, Vy V (x,y) = 0 → y = z x
  pin_left : z (-(1/2:ℝ)) = 0
  pin_right : z (1/2:ℝ) = 0
  bounds : ∀ x ∈ J, |z x| ≤ M₀/c ∧ |deriv z x| ≤ M₁/c ∧
    |deriv (deriv z) x| ≤ accelerationRadius c M₁ M₂
  curvature : ∀ x ∈ J, 1 ≤ profileSlopeSecond V z x
  jets : ∀ x ∈ U, HasDerivAt (profile V z) (profileSlope V z x) x ∧
    HasDerivAt (profileSlope V z) (profileSlopeFirst V z x) x ∧
    HasDerivAt (profileSlopeFirst V z) (profileSlopeSecond V z x) x
  barrier : AdaptiveFoldScalar.ScalarBarrier
    (profileSlope V z) (profileSlopeFirst V z) (profile V z)

/-- The ridge is constructed internally from the finite literal derivative data. -/
theorem exists_transverse_ridge_scalar_barrier
    {V : ℝ × ℝ → ℝ} {O : Set (ℝ × ℝ)} {R c M₀ M₁ M₂ A : ℝ}
    (h : StructuralRectangleData V O R c M₀ M₁ M₂ A) :
    ∃ (U : Set ℝ) (z : ℝ → ℝ), RidgeScalarData V O R c M₀ M₁ M₂ U z := by
  obtain ⟨U,z,hU,hJU,hz,hroot,huniq,_,_,hb,hjets⟩ :=
    exists_unique_c2_transverse_ridge_with_jets h.radius_pos h.concavity_pos
      h.domain_open h.regularity h.rectangle_subset h.vertical_negative
      h.lower_positive h.upper_negative h.first_nonneg h.second_nonneg
      h.center_bound h.Gx_bound h.Gxx_bound h.Gxy_bound h.Gyx_bound h.Gyy_bound
  have hb' : ∀ x ∈ J, |z x| ≤ M₀/c ∧ |deriv z x| ≤ M₁/c ∧
      |deriv (deriv z) x| ≤ accelerationRadius c M₁ M₂ := by
    intro x hx
    refine ⟨(hb x hx).1, (hb x hx).2.1, (hb x hx).2.2.trans ?_⟩
    unfold accelerationRadius
    have hq : 0 ≤ M₂ / c := div_nonneg h.second_nonneg h.concavity_pos.le
    gcongr
    exact (hb x hx).2.1
  have hL : z (-(1/2:ℝ)) = 0 :=
    (huniq _ (hJU (by norm_num [J])) 0
      (by constructor <;> linarith [h.radius_pos]) h.pin_left.2).symm
  have hR : z (1/2:ℝ) = 0 :=
    (huniq _ (hJU (by norm_num [J])) 0
      (by constructor <;> linarith [h.radius_pos]) h.pin_right.2).symm
  have hcurv : ∀ x ∈ J, 1 ≤ profileSlopeSecond V z x := by
    intro x hx
    have hy := Ioo_subset_Icc_self (hroot x (hJU hx)).1
    have he := profileSlopeSecond_error h.concavity_pos h.first_nonneg h.second_nonneg
      (h.Hy_bound x hx _ hy) (h.Hxy_bound x hx _ hy) (h.Hyx_bound x hx _ hy)
      (h.Hyy_bound x hx _ hy) (hb' x hx).2.1 (hb' x hx).2.2
    have he' := (abs_le.mp (he.1.trans he.2)).1
    linarith [h.Hxx_lower x hx _ hy, h.curvature_budget]
  refine ⟨U,z,hU,hJU,hz,hroot,huniq,hL,hR,hb',hcurv,hjets,?_⟩
  apply AdaptiveFoldScalar.scalarBarrier_of_secondDerivative
    (profileSlope V z) (profileSlopeFirst V z) (profileSlopeSecond V z) (profile V z)
    (fun x hx => (hjets x (hJU hx)).2.1)
    (fun x hx => (hjets x (hJU hx)).2.2) hcurv
    (fun x hx => (hjets x (hJU hx)).1)
  · simpa only [profileSlope, hL] using h.pin_left.1
  · simpa only [profileSlope, hR] using h.pin_right.1
  · simpa only [profile, hL, hR] using h.potential_gap

/-- Literal normalized maximum and saddle pins. -/
def M : ℝ × ℝ := (-(1/2:ℝ),0)
def S : ℝ × ℝ := ((1/2:ℝ),0)
def olderPoint (z : ℝ → ℝ) : ℝ × ℝ := (3/2,z (3/2))
def leftBox (R : ℝ) : Set (ℝ × ℝ) := Icc (-(3/2:ℝ)) (1/2) ×ˢ Icc (-R) R

/-- The frontier belongs to the four literal sides of the closed box. -/
theorem frontier_leftBox_sides {R : ℝ} {p : ℝ × ℝ} (hp : p ∈ frontier (leftBox R)) :
    p ∈ leftBox R ∧ (p.1 = -(3/2:ℝ) ∨ p.1 = 1/2 ∨ p.2 = -R ∨ p.2 = R) := by
  have hpD : p ∈ leftBox R := (isClosed_Icc.prod isClosed_Icc).frontier_subset hp
  refine ⟨hpD, ?_⟩
  by_contra hn
  push_neg at hn
  have hx : p.1 ∈ Ioo (-(3/2:ℝ)) (1/2) :=
    ⟨lt_of_le_of_ne hpD.1.1 (Ne.symm hn.1), lt_of_le_of_ne hpD.1.2 hn.2.1⟩
  have hy : p.2 ∈ Ioo (-R) R :=
    ⟨lt_of_le_of_ne hpD.2.1 (Ne.symm hn.2.2.1), lt_of_le_of_ne hpD.2.2 hn.2.2.2⟩
  have hi : p ∈ interior (leftBox R) := by
    rw [leftBox, interior_prod_eq, interior_Icc, interior_Icc]
    exact ⟨hx,hy⟩
  exact hp.2 hi

/-- The structural center bound and margin force the required loss on either
horizontal side. This is finite scalar arithmetic, with c's sign retained. -/
theorem side_drop_le {R c q z y : ℝ} (hc : 0 < c) (hq : q ≤ R)
    (hz : |z| ≤ q) (hy : y = -R ∨ y = R)
    (hdrop : 1 ≤ (c/2) * (R-q)^2) : 1 ≤ (c/2) * (y-z)^2 := by
  have hgap : 0 ≤ R-q := sub_nonneg.mpr hq
  have hab : R-q ≤ |y-z| := by
    rcases hy with rfl | rfl
    · have := (abs_le.mp hz).1
      have := neg_le_abs (-R-z)
      linarith
    · have := (abs_le.mp hz).2
      have := le_abs_self (R-z)
      linarith
  have hsq : (R-q)^2 ≤ |y-z|^2 := by nlinarith [abs_nonneg (y-z)]
  have hs := mul_le_mul_of_nonneg_left hsq (by linarith : 0 ≤ c/2)
  rw [sq_abs] at hs
  exact hdrop.trans hs

/-- Affine graph parameter in the full scalar floor interval. -/
def pathX (t : unitInterval) : ℝ := -(1/2:ℝ) + 2 * (t:ℝ)

theorem pathX_mem (t : unitInterval) : pathX t ∈ Icc (-(1/2:ℝ)) (3/2) := by
  have ht := t.property
  dsimp [pathX]
  constructor <;> linarith

/-- Explicit graph path; its continuity uses the constructed open-collar C²
regularity, and its midpoint is the literal saddle. -/
def ridgePath {z : ℝ → ℝ} {U : Set ℝ} (hU : IsOpen U) (hJU : J ⊆ U)
    (hz : ContDiffOn ℝ 2 z U) (hL : z (-(1/2:ℝ)) = 0) : Path M (olderPoint z) where
  toFun t := (pathX t, z (pathX t))
  continuous_toFun := by
    have hx : Continuous pathX := continuous_const.add (continuous_const.mul continuous_subtype_val)
    apply hx.prodMk
    apply hz.continuousOn.comp_continuous hx
    intro t
    exact hJU ⟨by linarith [(pathX_mem t).1], (pathX_mem t).2⟩
  source' := by simp [pathX, M, hL]
  target' := by norm_num [pathX, olderPoint]

/-- Minimal ambient data for the existing elder-boundary consumer. No elder or
H0 theorem, chart transport, or source probability is asserted here. -/
structure RectangleBoundaryPathData (V : ℝ × ℝ → ℝ) (R c : ℝ) (z : ℝ → ℝ) : Prop where
  vertical_loss : ∀ x ∈ J, ∀ y ∈ Icc (-R) R,
    V (x,y) ≤ profile V z x - (c/2)*(y-z x)^2
  box_closed : IsClosed (leftBox R)
  maximum_mem : M ∈ leftBox R
  death_lt_maximum : V S < V M
  ceiling : ∀ p ∈ leftBox R, V p ≤ V M
  frontier_bound : ∀ p ∈ frontier (leftBox R), V p ≤ V S
  older_gain : V M + 1/4 ≤ V (olderPoint z)
  path : ∃ γ : Path M (olderPoint z),
    (∀ t : unitInterval, γ t = (pathX t,z (pathX t))) ∧
    (∀ t : unitInterval, V S ≤ V (γ t)) ∧ γ (1/2 : unitInterval) = S

end AdaptiveFoldBoundaryPath
