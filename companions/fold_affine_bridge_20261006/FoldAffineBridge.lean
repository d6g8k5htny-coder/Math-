import ResearchFormalCoreR1.AlgebraV2

/-! Exact polynomial/affine companion. No field model or persistence pairing.
The canonical subtraction is consumed from AlgebraV2, not re-proved here. -/
namespace FoldAffineBridge

open ResearchFormalCoreR1
set_option autoImplicit false

noncomputable def affinePotential (s a b c y : ℝ) : ℝ := c * foldPotential s (a*y+b)
noncomputable def plusPoint (s a b : ℝ) : ℝ := (s-b)/a
noncomputable def minusPoint (s a b : ℝ) : ℝ := (-s-b)/a
noncomputable def physicalSeparation (s a : ℝ) : ℝ := 2*|s|/|a|

theorem fold_hasDerivAt (s x : ℝ) : HasDerivAt (foldPotential s) (s^2-x^2) x := by
  unfold foldPotential
  convert ((hasDerivAt_pow 3 x).neg.div_const 3).add
    ((hasDerivAt_id x).const_mul (s^2)) using 1 <;> first | rfl | (funext z; dsimp; ring) | ring

theorem fold_deriv (s x : ℝ) : deriv (foldPotential s) x = s^2-x^2 :=
  (fold_hasDerivAt s x).deriv

theorem fold_second (s x : ℝ) : deriv (deriv (foldPotential s)) x = -2*x := by
  have hf : deriv (foldPotential s) = fun z => s^2-z^2 := funext (fold_deriv s)
  rw [hf]
  have hd : HasDerivAt (fun z : ℝ => s^2-z^2) (-2*x) x := by
    convert (hasDerivAt_const x (s^2)).sub (hasDerivAt_pow 2 x) using 1 <;> first | rfl | (funext z; dsimp; ring) | ring
  exact hd.deriv

theorem fold_critical (s x : ℝ) : deriv (foldPotential s) x = 0 ↔ x=s ∨ x= -s := by
  rw [fold_deriv]
  constructor
  · intro h
    have hp : (x-s)*(x+s)=0 := by nlinarith
    rcases mul_eq_zero.mp hp with h1 | h2
    · left; linarith
    · right; linarith
  · rintro (rfl | rfl) <;> ring

theorem fold_nondegenerate (s : ℝ) :
    (deriv (deriv (foldPotential s)) s ≠ 0 ∧
     deriv (deriv (foldPotential s)) (-s) ≠ 0) ↔ s ≠ 0 := by
  simp only [fold_second]
  constructor
  · rintro ⟨h, _⟩ hs
    apply h
    rw [hs, mul_zero]
  · intro hs
    exact ⟨mul_ne_zero (by norm_num) hs, mul_ne_zero (by norm_num) (neg_ne_zero.mpr hs)⟩

theorem fold_curvature (s : ℝ) :
    (deriv (deriv (foldPotential s)) s < 0 ↔ 0 < s) ∧
    (0 < deriv (deriv (foldPotential s)) (-s) ↔ 0 < s) := by
  simp only [fold_second]
  constructor <;> constructor <;> intro h <;> nlinarith

theorem affine_hasDerivAt (s a b c y : ℝ) : HasDerivAt (affinePotential s a b c)
    (c*a*(s^2-(a*y+b)^2)) y := by
  have hl : HasDerivAt (fun z : ℝ => a*z+b) a y := by
    simpa using ((hasDerivAt_id y).const_mul a).add_const b
  unfold affinePotential
  convert ((fold_hasDerivAt s (a*y+b)).comp y hl).const_mul c using 1 <;> first | rfl | (funext z; dsimp; ring) | ring

theorem affine_deriv (s a b c y : ℝ) : deriv (affinePotential s a b c) y =
    c*a*(s^2-(a*y+b)^2) := (affine_hasDerivAt s a b c y).deriv

theorem affine_hasDerivAt_deriv (s a b c y : ℝ) :
    HasDerivAt (deriv (affinePotential s a b c)) (-2*c*a^2*(a*y+b)) y := by
  have hf : deriv (affinePotential s a b c) = fun z => c*a*(s^2-(a*z+b)^2) :=
    funext (affine_deriv s a b c)
  rw [hf]
  have hl : HasDerivAt (fun z : ℝ => a*z+b) a y := by
    simpa using ((hasDerivAt_id y).const_mul a).add_const b
  convert ((hasDerivAt_const y (s^2)).sub (hl.pow 2)).const_mul (c*a) using 1 <;> first | rfl | (funext z; dsimp; ring) | ring

theorem affine_second (s a b c y : ℝ) : deriv (deriv (affinePotential s a b c)) y =
    -2*c*a^2*(a*y+b) := (affine_hasDerivAt_deriv s a b c y).deriv

theorem affine_coordinates (s a b : ℝ) (ha : a ≠ 0) :
    a*plusPoint s a b+b=s ∧ a*minusPoint s a b+b= -s := by
  unfold plusPoint minusPoint
  constructor <;> field_simp [ha] <;> ring

theorem affine_critical (s a b c y : ℝ) (ha : a ≠ 0) (hc : c ≠ 0) :
    deriv (affinePotential s a b c) y=0 ↔ y=plusPoint s a b ∨ y=minusPoint s a b := by
  rw [affine_deriv]
  constructor
  · intro h
    have hz : s^2-(a*y+b)^2=0 := (mul_eq_zero.mp h).resolve_left (mul_ne_zero hc ha)
    have hp : (a*y+b-s)*(a*y+b+s)=0 := by nlinarith
    rcases mul_eq_zero.mp hp with h1 | h2
    · left
      unfold plusPoint
      field_simp [ha]
      nlinarith
    · right
      unfold minusPoint
      field_simp [ha]
      nlinarith
  · rintro (rfl | rfl)
    · rw [(affine_coordinates s a b ha).1]; ring
    · rw [(affine_coordinates s a b ha).2]; ring

theorem affine_orientation (s a b : ℝ) : plusPoint s a b-minusPoint s a b=2*s/a := by
  unfold plusPoint minusPoint
  ring

theorem affine_distinct (s a b : ℝ) (ha : a ≠ 0) :
    plusPoint s a b ≠ minusPoint s a b ↔ s ≠ 0 := by
  constructor
  · intro h hs
    apply h
    simp [hs, plusPoint, minusPoint]
  · intro hs heq
    apply hs
    unfold plusPoint minusPoint at heq
    field_simp [ha] at heq
    linarith

theorem affine_curvature (s a b c : ℝ) (ha : a ≠ 0) :
    deriv (deriv (affinePotential s a b c)) (plusPoint s a b)= -2*c*a^2*s ∧
    deriv (deriv (affinePotential s a b c)) (minusPoint s a b)=2*c*a^2*s := by
  rw [affine_second, affine_second, (affine_coordinates s a b ha).1,
    (affine_coordinates s a b ha).2]
  constructor <;> ring

theorem affine_nondegenerate (s a b c : ℝ) (ha : a ≠ 0) (hc : c ≠ 0) :
    (deriv (deriv (affinePotential s a b c)) (plusPoint s a b) ≠ 0 ∧
     deriv (deriv (affinePotential s a b c)) (minusPoint s a b) ≠ 0) ↔ s ≠ 0 := by
  rw [(affine_curvature s a b c ha).1, (affine_curvature s a b c ha).2]
  constructor
  · rintro ⟨h, _⟩ hs
    apply h
    rw [hs, mul_zero]
  · intro hs
    exact ⟨mul_ne_zero (mul_ne_zero (mul_ne_zero (by norm_num) hc) (pow_ne_zero 2 ha)) hs,
      mul_ne_zero (mul_ne_zero (mul_ne_zero (by norm_num) hc) (pow_ne_zero 2 ha)) hs⟩

theorem affine_curvature_sign (s a b c : ℝ) (ha : a ≠ 0) :
    (deriv (deriv (affinePotential s a b c)) (plusPoint s a b) < 0 ↔ 0<c*s) ∧
    (0 < deriv (deriv (affinePotential s a b c)) (minusPoint s a b) ↔ 0<c*s) := by
  rw [(affine_curvature s a b c ha).1, (affine_curvature s a b c ha).2]
  have hk : 0 < 2*a^2 := mul_pos (by norm_num) (sq_pos_of_ne_zero ha)
  have he1 : -2*c*a^2*s = -(2*a^2*(c*s)) := by ring
  have he2 : 2*c*a^2*s = 2*a^2*(c*s) := by ring
  rw [he1, he2]
  constructor
  · constructor
    · intro h
      by_contra hn
      have hh := mul_nonpos_of_nonneg_of_nonpos (le_of_lt hk) (le_of_not_gt hn)
      linarith
    · intro h
      exact neg_lt_zero.mpr (mul_pos hk h)
  · constructor
    · intro h
      by_contra hn
      have hh := mul_nonpos_of_nonneg_of_nonpos (le_of_lt hk) (le_of_not_gt hn)
      linarith
    · intro h
      exact mul_pos hk h

theorem separation_eq (s a b : ℝ) :
    |plusPoint s a b-minusPoint s a b|=physicalSeparation s a := by
  rw [affine_orientation]
  simp [physicalSeparation, abs_div, abs_mul]

theorem separation_nonneg (s a : ℝ) : 0 ≤ physicalSeparation s a :=
  div_nonneg (mul_nonneg (by norm_num) (abs_nonneg s)) (abs_nonneg a)

theorem separation_zero (s a : ℝ) (ha : a ≠ 0) : physicalSeparation s a=0 ↔ s=0 := by
  unfold physicalSeparation
  constructor
  · intro h
    field_simp [abs_ne_zero.mpr ha] at h
    have hs : |s|=0 := by linarith
    exact abs_eq_zero.mp hs
  · intro h
    simp [h]

theorem affine_signed_gap (s a b c : ℝ) (ha : a ≠ 0) :
    affinePotential s a b c (plusPoint s a b)-affinePotential s a b c (minusPoint s a b)=
      c*(2*s)^3/6 := by
  unfold affinePotential
  rw [(affine_coordinates s a b ha).1, (affine_coordinates s a b ha).2]
  calc
    c*foldPotential s s-c*foldPotential s (-s) =
        c*(foldPotential s s-foldPotential s (-s)) := by ring
    _ = c*((2*s)^3/6) := by rw [ec005_fold_gap]
    _ = c*(2*s)^3/6 := by ring

theorem affine_absolute_gap (s a b c : ℝ) (ha : a ≠ 0) :
    |affinePotential s a b c (plusPoint s a b)-affinePotential s a b c (minusPoint s a b)|=
      |c| * |a|^3*(physicalSeparation s a)^3/6 := by
  rw [affine_signed_gap s a b c ha]
  simp only [abs_div, abs_mul, abs_pow]
  norm_num
  unfold physicalSeparation
  field_simp [abs_ne_zero.mpr ha]
  ring

theorem affine_increments (s a b c h : ℝ) (ha : a ≠ 0) :
    affinePotential s a b c (plusPoint s a b+h)-affinePotential s a b c (plusPoint s a b)=
      -c*(a*h)^2*(s+a*h/3) ∧
    affinePotential s a b c (minusPoint s a b+h)-affinePotential s a b c (minusPoint s a b)=
      c*(a*h)^2*(s-a*h/3) := by
  have hp := (affine_coordinates s a b ha).1
  have hm := (affine_coordinates s a b ha).2
  have hp' : a*(plusPoint s a b+h)+b=s+a*h := by nlinarith [hp]
  have hm' : a*(minusPoint s a b+h)+b= -s+a*h := by nlinarith [hm]
  unfold affinePotential
  rw [hp, hm, hp', hm']
  unfold foldPotential
  constructor <;> ring

theorem affine_local_signs (s a b c h : ℝ) (ha : a ≠ 0) (hc : c ≠ 0) (hs : s ≠ 0)
    (hh0 : 0 < |h|) (hh1 : |h| < |s|/|a|) :
    c*s*(affinePotential s a b c (plusPoint s a b+h)-affinePotential s a b c (plusPoint s a b)) < 0 ∧
    0 < c*s*(affinePotential s a b c (minusPoint s a b+h)-affinePotential s a b c (minusPoint s a b)) := by
  rw [(affine_increments s a b c h ha).1, (affine_increments s a b c h ha).2]
  have haabs : 0 < |a| := abs_pos.mpr ha
  have hhbound : |h| * |a| < |s| := (lt_div_iff₀ haabs).mp hh1
  have hah : |a*h| < |s| := by rw [abs_mul]; nlinarith
  have hsprod : 0 < s*(s+a*h/3) ∧ 0 < s*(s-a*h/3) := by
    rcases lt_or_gt_of_ne hs with hn | hp
    · rw [abs_of_neg hn] at hah
      have hb := abs_lt.mp hah
      constructor
      · exact mul_pos_of_neg_of_neg hn (by linarith [hb.2])
      · exact mul_pos_of_neg_of_neg hn (by linarith [hb.1])
    · rw [abs_of_pos hp] at hah
      have hb := abs_lt.mp hah
      constructor
      · exact mul_pos hp (by linarith [hb.1])
      · exact mul_pos hp (by linarith [hb.2])
  have hch : 0 < c^2*(a*h)^2 :=
    mul_pos (sq_pos_of_ne_zero hc) (sq_pos_of_ne_zero (mul_ne_zero ha (abs_pos.mp hh0)))
  have hp := mul_pos hch hsprod.1
  have hm := mul_pos hch hsprod.2
  constructor <;> nlinarith

theorem affine_zero_degenerate (a b c : ℝ) (ha : a ≠ 0) :
    plusPoint 0 a b=minusPoint 0 a b ∧ plusPoint 0 a b= -b/a ∧
    deriv (affinePotential 0 a b c) (-b/a)=0 ∧
    deriv (deriv (affinePotential 0 a b c)) (-b/a)=0 := by
  have hx : a*(-b/a)+b=0 := by field_simp [ha]; ring
  refine ⟨by simp [plusPoint, minusPoint], by simp [plusPoint], ?_, ?_⟩
  · rw [affine_deriv, hx]; ring
  · rw [affine_second, hx]; ring

theorem affine_zero_increment (a b c h : ℝ) (ha : a ≠ 0) :
    affinePotential 0 a b c (-b/a+h)-affinePotential 0 a b c (-b/a)= -c*a^3*h^3/3 := by
  have hp := (affine_increments 0 a b c h ha).1
  simp only [plusPoint, zero_sub] at hp
  rw [hp]
  ring

/-- Nonzero a and c are essential: without them the function is constant. -/
theorem affine_zero_crossing (a b c h : ℝ) (ha : a ≠ 0) (hc : c ≠ 0) (hh : h ≠ 0) :
    (affinePotential 0 a b c (-b/a+h)-affinePotential 0 a b c (-b/a))*
    (affinePotential 0 a b c (-b/a-h)-affinePotential 0 a b c (-b/a)) < 0 := by
  rw [show -b/a-h = -b/a+(-h) by ring,
    affine_zero_increment a b c h ha, affine_zero_increment a b c (-h) ha]
  have hz : c*a^3*h^3/3 ≠ 0 :=
    div_ne_zero (mul_ne_zero (mul_ne_zero hc (pow_ne_zero 3 ha)) (pow_ne_zero 3 hh)) (by norm_num)
  calc
    (-c*a^3*h^3/3)*(-c*a^3*(-h)^3/3) = -(c*a^3*h^3/3)^2 := by ring
    _ < 0 := neg_lt_zero.mpr (sq_pos_of_ne_zero hz)

theorem affine_constant_a (s b c y : ℝ) : affinePotential s 0 b c y=c*foldPotential s b ∧
    deriv (affinePotential s 0 b c) y=0 := by
  simp [affinePotential, affine_deriv]

theorem affine_constant_c (s a b y : ℝ) : affinePotential s a b 0 y=0 ∧
    deriv (affinePotential s a b 0) y=0 := by
  simp [affinePotential, affine_deriv]

end FoldAffineBridge
