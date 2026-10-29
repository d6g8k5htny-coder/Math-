import SourcePinPreservingQuartic

noncomputable section
open I4SourcePinPreservingQuartic I4ActualQuarticTransfer
open Matrix WithLp
open scoped BigOperators

namespace QuarticQualificationControls

private def mixedU : Fin 8 → ℝ := ![1,2,3,4,5,6,7,8]
private def cutoffU : Fin 8 → ℝ := ![1,0,0,0,5,0,0,0]

-- Literal LM001 polynomial at a rational point, with nonunit radius and
-- all eight raw coefficients mixed. Expected fractions are frozen canaries.
example : pinPreservingQuartic 2 (-3) mixedU ![1/3,-1/4] =
    ![-869/5184,241/2592] := by
  norm_num [pinPreservingQuartic,mixedU]

example : pinPreservingJacobian 2 (-3) mixedU ![1/3,-1/4] =
    !![5/72,-85/144;-85/144,-19/12] := by
  norm_num [pinPreservingJacobian,mixedU]

-- The actual Euclidean fderiv theorem consumes that same literal Jacobian.
example : fderiv ℝ (fun z : EuclideanSpace ℝ (Fin 2) =>
      toLp 2 (pinPreservingQuartic 2 (-3) mixedU (ofLp z))) (toLp 2 ![1/3,-1/4]) =
    matrixLinearEuclidean !![5/72,-85/144;-85/144,-19/12] := by
  rw [fderiv_pinPreservingQuartic]
  congr 1
  norm_num [pinPreservingJacobian,mixedU]

-- Exact polynomial pins hold for every coefficient choice and constant radius.
example (r q : ℝ) (U : Fin 8 → ℝ) : pinPreservingQuartic r q U ![1/2,0] = 0 := by
  ext i
  fin_cases i <;> norm_num [pinPreservingQuartic]

example (r q : ℝ) (U : Fin 8 → ℝ) : pinPreservingQuartic r q U ![-1/2,0] = 0 := by
  ext i
  fin_cases i <;> norm_num [pinPreservingQuartic]

-- Sharp factorial 1/24: x^4 has fourth derivative 24, and at x=2 the
-- cubic Taylor remainder equals 16, exactly 24*2^4/24.
example : |(2:ℝ)^4-scalarTaylor (fun t : ℝ => t^4) 3 2| = 24*2^4/24 := by
  rw [scalarTaylor_three]
  norm_num [iteratedDeriv_pow,deriv_pow_field]

example : |(2:ℝ)^4-scalarTaylor (fun t : ℝ => t^4) 3 2| ≤ 24*2^4/24 := by
  have h := scalar_taylor_remainder (fun t : ℝ => t^4) (by fun_prop) 3 24
    (by intro y; norm_num [iteratedDeriv_pow]) 2
  norm_num at h ⊢
  exact h

-- Sharp factorial 1/6 on the negative side of the origin.
example : |(-2:ℝ)^3-scalarTaylor (fun t : ℝ => t^3) 2 (-2)| = 6*|-2|^3/6 := by
  rw [scalarTaylor_two]
  norm_num [iteratedDeriv_pow,deriv_pow_field]

example : |(-2:ℝ)^3-scalarTaylor (fun t : ℝ => t^3) 2 (-2)| ≤ 6*|-2|^3/6 := by
  have h := scalar_taylor_remainder (fun t : ℝ => t^3) (by fun_prop) 2 6
    (by intro y; norm_num [iteratedDeriv_pow]) (-2)
  norm_num at h ⊢
  exact h

private theorem sup_norm_34 : ‖(![3,4] : Fin 2 → ℝ)‖ = 4 := by
  apply le_antisymm
  · apply (pi_norm_le_iff_of_nonneg (by norm_num : (0:ℝ) ≤ 4)).mpr
    intro i
    fin_cases i <;> norm_num
  · have h := norm_le_pi_norm (![3,4] : Fin 2 → ℝ) (1 : Fin 2)
    norm_num at h
    exact h

private theorem euclidean_norm_34 : ‖toLp 2 (![3,4] : Fin 2 → ℝ)‖ = 5 := by
  have h := euclidean_two_norm_sq (toLp 2 (![3,4] : Fin 2 → ℝ))
  norm_num at h
  nlinarith [norm_nonneg (toLp 2 (![3,4] : Fin 2 → ℝ))]

-- The bridge is an inequality between distinct norms, not a claimed equality.
example : ‖(![3,4] : Fin 2 → ℝ)‖ < ‖toLp 2 (![3,4] : Fin 2 → ℝ)‖ := by
  rw [sup_norm_34,euclidean_norm_34]
  norm_num

example : ‖(![3,4] : Fin 2 → ℝ)‖ ≤ ‖toLp 2 (![3,4] : Fin 2 → ℝ)‖ :=
  pi_norm_le_euclidean_norm _

-- The factor two for a 2x2 entrywise bound is attained by the all-ones matrix.
example : ‖matrixLinearEuclidean !![1,1;1,1]‖ = 2 := by
  apply le_antisymm
  · have h := matrixLinearEuclidean_norm_le_two_mul !![1,1;1,1] 1 (by norm_num)
      (by intro i j; fin_cases i <;> fin_cases j <;> norm_num)
    simpa using h
  · let v : EuclideanSpace ℝ (Fin 2) := toLp 2 ![1,1]
    have hv : 0 < ‖v‖ := by
      apply norm_pos_iff.mpr
      intro hzero
      have h := congrArg (fun x : EuclideanSpace ℝ (Fin 2) => x 0) hzero
      norm_num [v] at h
    have hm : matrixLinearEuclidean !![1,1;1,1] v = (2:ℝ) • v := by
      ext i
      fin_cases i <;> norm_num [matrixLinearEuclidean,v]
    have h := (matrixLinearEuclidean !![1,1;1,1]).le_opNorm v
    rw [hm,norm_smul] at h
    norm_num at h
    exact le_of_mul_le_mul_right h hv

-- LM004 uses the MAX of the value and derivative suprema.
example : (683/480 : ℝ) ≤ 3 := by norm_num
example : (2623/960 : ℝ) ≤ 3 := by norm_num
example : max (683/480 : ℝ) (2623/960 : ℝ) ≤ 3 := by norm_num
example : (4:ℝ) < 683/480+2623/960 := by norm_num

-- Exact constants and literal coefficient normalization of LM001 Fstar.
example : quarticK0 = 4096 ∧ quarticKcap = 25600010 ∧
    quarticEpsilonStar = 1/13107200000 := by
  norm_num [quarticK0,quarticKcap,quarticEpsilonStar]

example : quarticFstar 2 cutoffU = 4/3 := by norm_num [quarticFstar,cutoffU]
example : 1+(∑ i : Fin 8, |cutoffU i|) = 7 := by
  norm_num [cutoffU,Fin.sum_univ_succ]

-- Nonunit raw radius 7 <= 5*2, with r=epsilonStar/32 on the cutoff boundary.
example : (quarticEpsilonStar/32)*7^5 ≤ 1/(1024*quarticK0) := by
  exact cutoff_raw_regularity (quarticEpsilonStar/32) 2 7
    (by norm_num [quarticEpsilonStar]) (by norm_num) (by norm_num)
    (by norm_num [quarticEpsilonStar])

example : 3*(quarticEpsilonStar/32)^2*2 ≤
    7*quarticWidth (quarticEpsilonStar/32) cutoffU 7/4 := by
  exact cutoff_quarticWidth_tolerance (quarticEpsilonStar/32) 2 7 2 cutoffU
    (by norm_num [quarticEpsilonStar]) (by norm_num [quarticEpsilonStar])
    (by norm_num) (by norm_num) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num [quarticEpsilonStar])

example : (-quarticKcap*quarticEpsilonStar)/(quarticEpsilonStar/32) ≤
    -(2*quarticK0*7^5+2*7) := by
  exact cutoff_curvature_threshold (-quarticKcap*quarticEpsilonStar)
    (quarticEpsilonStar/32) 2 7 (by norm_num [quarticEpsilonStar])
    (by norm_num) (by norm_num) (by norm_num)
    (by norm_num [quarticKcap,quarticEpsilonStar])

example : (1/14336 : ℝ) ≤ 1/2048 ∧ 8*7*(1/14336 : ℝ) ≤ 1/256 :=
  certificate_width_geometry 7 (1/14336) (by norm_num) (by norm_num)

end QuarticQualificationControls
