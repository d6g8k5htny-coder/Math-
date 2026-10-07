import FoldAffineBridge

open ResearchFormalCoreR1 FoldAffineBridge

example (s x : ℝ) : HasDerivAt (foldPotential s) (s^2-x^2) x := fold_hasDerivAt s x
example (s x : ℝ) : deriv (foldPotential s) x = s^2-x^2 := fold_deriv s x
example (s x : ℝ) : deriv (deriv (foldPotential s)) x = -2*x := fold_second s x
example (s x : ℝ) : deriv (foldPotential s) x = 0 ↔ x=s ∨ x= -s := fold_critical s x
example (s : ℝ) :
    (deriv (deriv (foldPotential s)) s ≠ 0 ∧
     deriv (deriv (foldPotential s)) (-s) ≠ 0) ↔ s ≠ 0 := fold_nondegenerate s
example (s : ℝ) :
    (deriv (deriv (foldPotential s)) s < 0 ↔ 0 < s) ∧
    (0 < deriv (deriv (foldPotential s)) (-s) ↔ 0 < s) := fold_curvature s

example (s a b c y : ℝ) : HasDerivAt (affinePotential s a b c)
    (c*a*(s^2-(a*y+b)^2)) y := affine_hasDerivAt s a b c y
example (s a b c y : ℝ) : deriv (affinePotential s a b c) y =
    c*a*(s^2-(a*y+b)^2) := affine_deriv s a b c y
example (s a b c y : ℝ) : HasDerivAt (deriv (affinePotential s a b c))
    (-2*c*a^2*(a*y+b)) y := affine_hasDerivAt_deriv s a b c y
example (s a b c y : ℝ) : deriv (deriv (affinePotential s a b c)) y =
    -2*c*a^2*(a*y+b) := affine_second s a b c y
example (s a b : ℝ) (ha : a ≠ 0) :
    a*plusPoint s a b+b=s ∧ a*minusPoint s a b+b= -s := affine_coordinates s a b ha
example (s a b c y : ℝ) (ha : a ≠ 0) (hc : c ≠ 0) :
    deriv (affinePotential s a b c) y=0 ↔ y=plusPoint s a b ∨ y=minusPoint s a b :=
  affine_critical s a b c y ha hc
example (s a b : ℝ) : plusPoint s a b-minusPoint s a b=2*s/a := affine_orientation s a b
example (s a b : ℝ) (ha : a ≠ 0) : plusPoint s a b ≠ minusPoint s a b ↔ s ≠ 0 :=
  affine_distinct s a b ha
example (s a b c : ℝ) (ha : a ≠ 0) :
    deriv (deriv (affinePotential s a b c)) (plusPoint s a b)= -2*c*a^2*s ∧
    deriv (deriv (affinePotential s a b c)) (minusPoint s a b)=2*c*a^2*s :=
  affine_curvature s a b c ha
example (s a b c : ℝ) (ha : a ≠ 0) (hc : c ≠ 0) :
    (deriv (deriv (affinePotential s a b c)) (plusPoint s a b) ≠ 0 ∧
     deriv (deriv (affinePotential s a b c)) (minusPoint s a b) ≠ 0) ↔ s ≠ 0 :=
  affine_nondegenerate s a b c ha hc
example (s a b c : ℝ) (ha : a ≠ 0) :
    (deriv (deriv (affinePotential s a b c)) (plusPoint s a b) < 0 ↔ 0<c*s) ∧
    (0 < deriv (deriv (affinePotential s a b c)) (minusPoint s a b) ↔ 0<c*s) :=
  affine_curvature_sign s a b c ha
example (s a b : ℝ) : |plusPoint s a b-minusPoint s a b|=physicalSeparation s a :=
  separation_eq s a b
example (s a : ℝ) : 0 ≤ physicalSeparation s a := separation_nonneg s a
example (s a : ℝ) (ha : a ≠ 0) : physicalSeparation s a=0 ↔ s=0 := separation_zero s a ha
example (s a b c : ℝ) (ha : a ≠ 0) :
    affinePotential s a b c (plusPoint s a b)-affinePotential s a b c (minusPoint s a b)=
      c*(2*s)^3/6 := affine_signed_gap s a b c ha
example (s a b c : ℝ) (ha : a ≠ 0) :
    |affinePotential s a b c (plusPoint s a b)-affinePotential s a b c (minusPoint s a b)|=
      |c|*|a|^3*(physicalSeparation s a)^3/6 := affine_absolute_gap s a b c ha
example (s a b c h : ℝ) (ha : a ≠ 0) :
    affinePotential s a b c (plusPoint s a b+h)-affinePotential s a b c (plusPoint s a b)=
      -c*(a*h)^2*(s+a*h/3) ∧
    affinePotential s a b c (minusPoint s a b+h)-affinePotential s a b c (minusPoint s a b)=
      c*(a*h)^2*(s-a*h/3) := affine_increments s a b c h ha
example (s a b c h : ℝ) (ha : a ≠ 0) (hc : c ≠ 0) (hs : s ≠ 0)
    (hh0 : 0 < |h|) (hh1 : |h| < |s|/|a|) :
    c*s*(affinePotential s a b c (plusPoint s a b+h)-affinePotential s a b c (plusPoint s a b)) < 0 ∧
    0 < c*s*(affinePotential s a b c (minusPoint s a b+h)-affinePotential s a b c (minusPoint s a b)) :=
  affine_local_signs s a b c h ha hc hs hh0 hh1
example (a b c : ℝ) (ha : a ≠ 0) :
    plusPoint 0 a b=minusPoint 0 a b ∧ plusPoint 0 a b= -b/a ∧
    deriv (affinePotential 0 a b c) (-b/a)=0 ∧
    deriv (deriv (affinePotential 0 a b c)) (-b/a)=0 := affine_zero_degenerate a b c ha
example (a b c h : ℝ) (ha : a ≠ 0) :
    affinePotential 0 a b c (-b/a+h)-affinePotential 0 a b c (-b/a)= -c*a^3*h^3/3 :=
  affine_zero_increment a b c h ha
example (a b c h : ℝ) (ha : a ≠ 0) (hc : c ≠ 0) (hh : h ≠ 0) :
    (affinePotential 0 a b c (-b/a+h)-affinePotential 0 a b c (-b/a))*
    (affinePotential 0 a b c (-b/a-h)-affinePotential 0 a b c (-b/a)) < 0 :=
  affine_zero_crossing a b c h ha hc hh
example (s b c y : ℝ) : affinePotential s 0 b c y=c*foldPotential s b ∧
    deriv (affinePotential s 0 b c) y=0 := affine_constant_a s b c y
example (s a b y : ℝ) : affinePotential s a b 0 y=0 ∧
    deriv (affinePotential s a b 0) y=0 := affine_constant_c s a b y

-- Exact positive controls: arbitrary translation and signed parameters.
example (b : ℝ) : physicalSeparation 1 2=1 ∧
    |affinePotential 1 2 b 3 (plusPoint 1 2 b)-affinePotential 1 2 b 3 (minusPoint 1 2 b)|=4 := by
  constructor
  · norm_num [physicalSeparation]
  · rw [affine_absolute_gap 1 2 b 3 (by norm_num)]
    norm_num [physicalSeparation]
example (b : ℝ) : deriv (deriv (affinePotential 1 2 b 3)) (plusPoint 1 2 b)= -24 ∧
    deriv (deriv (affinePotential 1 2 b 3)) (minusPoint 1 2 b)=24 := by
  simpa using affine_curvature 1 2 b 3 (by norm_num)
example : deriv (deriv (foldPotential (-1))) (-1)=2 := by norm_num [fold_second]
example (b : ℝ) : plusPoint 1 (-2) b-minusPoint 1 (-2) b= -1 := by
  rw [affine_orientation]; norm_num
example (b : ℝ) : deriv (deriv (affinePotential 1 2 b (-3))) (plusPoint 1 2 b)=24 := by
  have h := (affine_curvature 1 2 b (-3) (by norm_num)).1
  norm_num at h ⊢
  exact h
