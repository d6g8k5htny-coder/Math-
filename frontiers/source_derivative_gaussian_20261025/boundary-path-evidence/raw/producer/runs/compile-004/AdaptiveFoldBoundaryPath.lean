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

/-! The following two calculus bodies are integrated exactly once from the
scratch helper `/root/ridge_vertical_loss`, frozen run-006 (26 October 2026),
whole-source SHA256 40a313e48d747774916a240740d136d47ed84c9494b6fd5a2ea68eeacf8042d2.
The public constructor below instantiates them with its internally constructed
ridge; neither a ridge nor a vertical-loss certificate is a public premise. -/

/-- A scalar second-derivative upper bound gives the precise quadratic loss
from a zero of the first derivative. The jets are full derivatives, including
at the endpoints of the closed interval. -/
theorem quadratic_loss_of_second_derivative
    {f f₁ f₂ : ℝ → ℝ} {a b c z y : ℝ}
    (hf : ∀ t ∈ Icc a b, HasDerivAt f (f₁ t) t)
    (hf₁ : ∀ t ∈ Icc a b, HasDerivAt f₁ (f₂ t) t)
    (hneg : ∀ t ∈ Icc a b, f₂ t ≤ -c)
    (hz : z ∈ Icc a b) (hroot : f₁ z = 0) (hy : y ∈ Icc a b) :
    f y ≤ f z - (c / 2) * (y - z) ^ 2 := by
  let g : ℝ → ℝ := fun t => f t + (c / 2) * (t - z) ^ 2
  let g₁ : ℝ → ℝ := fun t => f₁ t + c * (t - z)
  let g₂ : ℝ → ℝ := fun t => f₂ t + c
  have hg : ∀ t ∈ Icc a b, HasDerivAt g (g₁ t) t := by
    intro t ht
    have hq : HasDerivAt (fun t : ℝ => (c / 2) * (t - z) ^ 2)
        (c * (t - z)) t := by
      convert (((hasDerivAt_id t).sub_const z).pow 2).const_mul (c / 2) using 1
      · rfl
      · dsimp
        ring
    exact (hf t ht).add hq
  have hg₁ : ∀ t ∈ Icc a b, HasDerivAt g₁ (g₂ t) t := by
    intro t ht
    have hlin : HasDerivAt (fun t : ℝ => c * (t - z)) c t := by
      simpa only [id_eq, mul_one] using ((hasDerivAt_id t).sub_const z).const_mul c
    exact (hf₁ t ht).add hlin
  have hconc : ConcaveOn ℝ (Icc a b) g := by
    apply concaveOn_of_hasDerivWithinAt2_nonpos (convex_Icc a b)
      (f' := g₁) (f'' := g₂)
    · intro t ht
      exact (hg t ht).continuousAt.continuousWithinAt
    · intro t ht
      exact (hg t (interior_subset ht)).hasDerivWithinAt
    · intro t ht
      exact (hg₁ t (interior_subset ht)).hasDerivWithinAt
    · intro t ht
      dsimp [g₂]
      linarith [hneg t (interior_subset ht)]
  have hgz : HasDerivAt g 0 z := by
    simpa [g₁, hroot] using hg z hz
  have hmax : g y ≤ g z := by
    rcases lt_trichotomy y z with hlt | heq | hgt
    · have hs := hconc.le_slope_of_hasDerivAt hy hz hlt hgz
      rw [slope_def_field] at hs
      have hsub : 0 ≤ g z - g y := by
        simpa only [zero_mul] using (le_div_iff₀ (sub_pos.mpr hlt)).mp hs
      linarith
    · exact heq ▸ le_rfl
    · have hs := hconc.slope_le_of_hasDerivAt hz hy hgt hgz
      rw [slope_def_field] at hs
      have hsub : g y - g z ≤ 0 := by
        simpa only [zero_mul] using (div_le_iff₀ (sub_pos.mpr hgt)).mp hs
      linarith
  dsimp [g] at hmax
  nlinarith

/-- The scalar loss lemma applied to the literal potential and its actual
coordinate partials. No norm convention or mixed-partial symmetry is used. -/
theorem vertical_quadratic_loss
    {V : ℝ × ℝ → ℝ} {O : Set (ℝ × ℝ)} {R c x z y : ℝ}
    (hO : IsOpen O) (hV : ContDiffOn ℝ 4 V O)
    (hstrip : ∀ t ∈ Icc (-R) R, (x, t) ∈ O)
    (hneg : ∀ t ∈ Icc (-R) R, partialY (Vy V) (x, t) ≤ -c)
    (hz : z ∈ Icc (-R) R) (hroot : Vy V (x, z) = 0)
    (hy : y ∈ Icc (-R) R) :
    V (x, y) ≤ V (x, z) - (c / 2) * (y - z) ^ 2 := by
  have hG : ContDiffOn ℝ 2 (Vy V) O := contDiffOn_partialY hO hV (by norm_num)
  apply quadratic_loss_of_second_derivative
    (f := fun t => V (x, t)) (f₁ := fun t => Vy V (x, t))
    (f₂ := fun t => partialY (Vy V) (x, t)) _ _ hneg hz hroot hy
  · intro t ht
    exact hasDerivAt_slice ((hV.contDiffAt (hO.mem_nhds (hstrip t ht))).differentiableAt
      (by norm_num))
  · intro t ht
    exact hasDerivAt_slice ((hG.contDiffAt (hO.mem_nhds (hstrip t ht))).differentiableAt
      (by norm_num))


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
  push Not at hn
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
    rcases hy with hy | hy
    · rw [hy]
      have := (abs_le.mp hz).1
      have := neg_le_abs (-R-z)
      linarith
    · rw [hy]
      have := (abs_le.mp hz).2
      have := le_abs_self (R-z)
      linarith
  have hsq : (R-q)^2 ≤ |y-z|^2 := by nlinarith [abs_nonneg (y-z)]
  have hs := mul_le_mul_of_nonneg_left hsq (by linarith : 0 ≤ c/2)
  rw [sq_abs] at hs
  exact hdrop.trans hs

/-- Affine graph parameter in the full scalar floor interval. -/
def pathX (t : unitInterval) : ℝ := -(1/2:ℝ) + 2 * (t:ℝ)

theorem pathX_mem (t : unitInterval) : pathX t ∈ Icc (-(1/2:ℝ)) (3/2) := by
  have ht₀ := t.property.1
  have ht₁ := t.property.2
  dsimp [pathX]
  constructor <;> linarith

/-- Explicit graph path; its continuity uses the constructed open-collar C²
regularity, and its midpoint is the literal saddle. -/
def ridgePath {z : ℝ → ℝ} {U : Set ℝ} (_hU : IsOpen U) (hJU : J ⊆ U)
    (hz : ContDiffOn ℝ 2 z U) (hL : z (-(1/2:ℝ)) = 0) : Path M (olderPoint z) where
  toFun t := (pathX t, z (pathX t))
  continuous_toFun := by
    have hx : Continuous pathX := continuous_const.add (continuous_const.mul continuous_subtype_val)
    apply hx.prodMk
    apply hz.continuousOn.comp_continuous hx
    intro t
    exact hJU ⟨by linarith [(pathX_mem t).1], (pathX_mem t).2⟩
  source' := by
    have h0 : pathX 0 = -(1/2:ℝ) := by norm_num [pathX]
    change (pathX 0,z (pathX 0)) = M
    rw [h0,hL]
    rfl
  target' := by norm_num [pathX, olderPoint]

def pathMidpoint : unitInterval := ⟨(1/2:ℝ), by norm_num⟩

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
    (∀ t : unitInterval, V S ≤ V (γ t)) ∧ γ pathMidpoint = S

/-- Literal structural inputs produce one analytic witness, its rectangle
boundary bound, and the explicit graph path through the saddle to the older arm. -/
theorem exists_transverse_ridge_boundary_path
    {V : ℝ × ℝ → ℝ} {O : Set (ℝ × ℝ)} {R c M₀ M₁ M₂ A : ℝ}
    (h : StructuralRectangleData V O R c M₀ M₁ M₂ A)
    (hmargin : M₀/c ≤ R) (hdrop : 1 ≤ (c/2)*(R-M₀/c)^2) :
    ∃ (U : Set ℝ) (z : ℝ → ℝ),
      RidgeScalarData V O R c M₀ M₁ M₂ U z ∧ RectangleBoundaryPathData V R c z := by
  obtain ⟨U,z,hz⟩ := exists_transverse_ridge_scalar_barrier h
  have hloss : ∀ x ∈ J, ∀ y ∈ Icc (-R) R,
      V (x,y) ≤ profile V z x - (c/2)*(y-z x)^2 := by
    intro x hx y hy
    exact vertical_quadratic_loss h.domain_open h.regularity
      (fun t ht => h.rectangle_subset ⟨hx,ht⟩) (h.vertical_negative x hx)
      (Ioo_subset_Icc_self (hz.root x (hz.interval_subset hx)).1)
      (hz.root x (hz.interval_subset hx)).2.2 hy
  have hL : profile V z (-(1/2:ℝ)) = V M := by
    simp only [profile, hz.pin_left, M]
  have hR : profile V z (1/2:ℝ) = V S := by
    simp only [profile, hz.pin_right, S]
  have hgap : V M - V S = 1/6 := h.potential_gap
  have hnonneg : ∀ y : ℝ, 0 ≤ (c/2)*y^2 :=
    fun y => mul_nonneg (by linarith [h.concavity_pos]) (sq_nonneg y)
  have hceil : ∀ p ∈ leftBox R, V p ≤ V M := by
    intro p hp
    have hxJ : p.1 ∈ J := ⟨hp.1.1, by linarith [hp.1.2]⟩
    have hv := hloss p.1 hxJ p.2 hp.2
    have hc := hz.barrier.ceiling p.1 hp.1
    rw [hL] at hc
    exact hv.trans (by linarith [hnonneg (p.2-z p.1)])
  have hbound : ∀ p ∈ frontier (leftBox R), V p ≤ V S := by
    intro p hp
    obtain ⟨hpD,hside⟩ := frontier_leftBox_sides hp
    have hxJ : p.1 ∈ J := ⟨hpD.1.1, by linarith [hpD.1.2]⟩
    have hv := hloss p.1 hxJ p.2 hpD.2
    rcases hside with hleft | hright | hbottom | htop
    · have hb := hz.barrier.left_barrier
      rw [hR] at hb
      rw [hleft] at hv
      exact hv.trans (by linarith [hnonneg (p.2-z (-(3/2:ℝ)))])
    · rw [hright,hR] at hv
      exact hv.trans (by linarith [hnonneg (p.2-z (1/2:ℝ))])
    · have hd := side_drop_le h.concavity_pos hmargin (hz.bounds p.1 hxJ).1
        (Or.inl hbottom) hdrop
      have hc := hz.barrier.ceiling p.1 hpD.1
      rw [hL] at hc
      linarith
    · have hd := side_drop_le h.concavity_pos hmargin (hz.bounds p.1 hxJ).1
        (Or.inr htop) hdrop
      have hc := hz.barrier.ceiling p.1 hpD.1
      rw [hL] at hc
      linarith
  refine ⟨U,z,hz,hloss,isClosed_Icc.prod isClosed_Icc,?_,?_,hceil,hbound,?_,?_⟩
  · constructor
    · norm_num [M]
    · change (0:ℝ) ∈ Icc (-R) R
      constructor <;> linarith [h.radius_pos]
  · linarith
  · have hb := hz.barrier.right_older
    rw [hL] at hb
    exact hb
  · let γ := ridgePath hz.domain_open hz.interval_subset hz.regularity hz.pin_left
    refine ⟨γ, fun _ => rfl, ?_, ?_⟩
    · intro t
      have hf := hz.barrier.floor (pathX t) (pathX_mem t)
      rw [hR] at hf
      exact hf
    · have hx : pathX pathMidpoint = (1/2:ℝ) := by norm_num [pathX,pathMidpoint]
      change (pathX pathMidpoint,z (pathX pathMidpoint)) = S
      rw [hx,hz.pin_right]
      rfl

end AdaptiveFoldBoundaryPath
