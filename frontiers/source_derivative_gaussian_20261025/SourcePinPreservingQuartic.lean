import SourcePinCurvatureBounds
import Mathlib.Analysis.Calculus.Taylor
import Mathlib.Analysis.Analytic.IteratedFDeriv
import Mathlib.Analysis.InnerProductSpace.PiL2
import Mathlib.Analysis.CStarAlgebra.Matrix
import Mathlib.Analysis.Calculus.Gradient.Basic

/-! Actual fifth-order comparison with the literal LM001 pin-preserving quartic.
The comparison uses Euclidean values and derivative operator norms separately,
so its uniform statement is the maximum C1 norm from LM004.
-/

noncomputable section
open I4SmoothCarrier I4SourceConfluentPins I4SourceEndpointRegression
open I4SourceConditionalMajorant I4SourcePinCurvatureBounds I4ModeCurveChains
open I4SourceDerivativeGaussian I4SourceGaussian I4Source I4Weights I4Foundation
open I4ConfluentIntegralIdentities
open I4SourceSmoothPalm I4SourceEndpointEstimates I4SourceConfluentLimits
open I4PeanoErrorBounds MeasureTheory Set Matrix WithLp Filter InnerProductSpace
open scoped BigOperators Interval Topology Nat
set_option autoImplicit false

namespace I4ActualQuarticTransfer

theorem peanoCubic_first_moment :
    (∫ u in (-1/2 : ℝ)..(1/2 : ℝ), peanoCubic u * u) = 0 := by
  have heq : (fun u : ℝ => peanoCubic u * u) = (fun u => (1/4 : ℝ) * u - u^3) := by
    funext u
    unfold peanoCubic
    ring
  have hi1 : IntervalIntegrable (fun u : ℝ => (1/4 : ℝ)*u) volume (-1/2 : ℝ) (1/2 : ℝ) := by
    apply Continuous.intervalIntegrable
    fun_prop
  have hi2 : IntervalIntegrable (fun u : ℝ => u^3) volume (-1/2 : ℝ) (1/2 : ℝ) :=
    (continuous_id.pow 3).intervalIntegrable _ _
  rw [heq, intervalIntegral.integral_sub hi1 hi2, intervalIntegral.integral_const_mul]
  norm_num [integral_id, integral_pow]

theorem peanoCubic_normalized_second_moment :
    6 * (∫ u in (-1/2 : ℝ)..(1/2 : ℝ), peanoCubic u * u^2) = 1/20 := by
  have heq : (fun u : ℝ => peanoCubic u * u^2) =
      (fun u => (1/4 : ℝ) * u^2 - u^4) := by
    funext u
    unfold peanoCubic
    ring
  have hi1 : IntervalIntegrable (fun u : ℝ => (1/4 : ℝ)*u^2) volume (-1/2 : ℝ) (1/2 : ℝ) := by
    apply Continuous.intervalIntegrable
    fun_prop
  have hi2 : IntervalIntegrable (fun u : ℝ => u^4) volume (-1/2 : ℝ) (1/2 : ℝ) :=
    (continuous_id.pow 4).intervalIntegrable _ _
  rw [heq, intervalIntegral.integral_sub hi1 hi2, intervalIntegral.integral_const_mul]
  norm_num [integral_pow]

theorem symmetric_cubic_pin_second_order (g : ℝ → ℝ) (hgc : Continuous g)
    (r t c G : ℝ) (_hG : 0 ≤ G)
    (hpin : 6 * (∫ u in (-1/2 : ℝ)..(1/2 : ℝ), peanoCubic u * g (r*u)) = 2)
    (hrem : ∀ u ∈ Icc (-1/2 : ℝ) (1/2 : ℝ),
      |g (r*u) - t - r*u*c| ≤ G*r^2*u^2/2) :
    |t-2| ≤ G*r^2/40 := by
  let f : ℝ → ℝ := fun u => g (r*u)-t-r*u*c
  have hcK : Continuous peanoCubic := by unfold peanoCubic; fun_prop
  have hcf : Continuous f := by dsimp [f]; fun_prop
  have hcg : Continuous (fun u => g (r*u)) := by fun_prop
  have hmass : (∫ u in (-1/2 : ℝ)..(1/2 : ℝ), peanoCubic u) = 1/6 := by
    linarith [peano_kernel_masses.2.2.2]
  have hmom : (∫ u in (-1/2 : ℝ)..(1/2 : ℝ), peanoCubic u * u^2) = 1/120 := by
    linarith [peanoCubic_normalized_second_moment]
  have hlinear : (∫ u in (-1/2 : ℝ)..(1/2 : ℝ), peanoCubic u * (r*u*c)) = 0 := by
    calc
      _ = (r*c) * ∫ u in (-1/2 : ℝ)..(1/2 : ℝ), peanoCubic u * u := by
        rw [← intervalIntegral.integral_const_mul]
        congr 1
        funext u
        ring
      _ = 0 := by rw [peanoCubic_first_moment]; ring
  have heq : 6 * (∫ u in (-1/2 : ℝ)..(1/2 : ℝ), peanoCubic u * f u) = 2-t := by
    dsimp [f]
    simp_rw [mul_sub]
    have hi1 : IntervalIntegrable (fun u => peanoCubic u * g (r*u)) volume
        (-1/2 : ℝ) (1/2 : ℝ) := (hcK.mul hcg).intervalIntegrable _ _
    have hi2 : IntervalIntegrable (fun u => peanoCubic u * t) volume
        (-1/2 : ℝ) (1/2 : ℝ) := (hcK.mul continuous_const).intervalIntegrable _ _
    have hi3 : IntervalIntegrable (fun u => peanoCubic u * (r*u*c)) volume
        (-1/2 : ℝ) (1/2 : ℝ) := by
      apply Continuous.intervalIntegrable
      fun_prop
    have hi12 : IntervalIntegrable (fun u => peanoCubic u * g (r*u)-peanoCubic u*t)
        volume (-1/2 : ℝ) (1/2 : ℝ) := hi1.sub hi2
    rw [intervalIntegral.integral_sub hi12 hi3, intervalIntegral.integral_sub hi1 hi2,
      intervalIntegral.integral_mul_const, hmass, hlinear]
    linarith [hpin]
  have hbound : |∫ u in (-1/2 : ℝ)..(1/2 : ℝ), peanoCubic u * f u| ≤ G*r^2/240 := by
    calc
      _ ≤ ∫ u in (-1/2 : ℝ)..(1/2 : ℝ), |peanoCubic u * f u| :=
        intervalIntegral.abs_integral_le_integral_abs (by norm_num)
      _ ≤ ∫ u in (-1/2 : ℝ)..(1/2 : ℝ), peanoCubic u * (G*r^2*u^2/2) := by
        apply intervalIntegral.integral_mono_on (by norm_num)
          ((hcK.mul hcf).abs.intervalIntegrable _ _)
          ((hcK.mul (by fun_prop)).intervalIntegrable _ _)
        intro u hu
        change |peanoCubic u * f u| ≤ peanoCubic u * (G*r^2*u^2/2)
        rw [abs_mul, abs_of_nonneg (peanoCubic_nonneg u hu)]
        exact mul_le_mul_of_nonneg_left (hrem u hu) (peanoCubic_nonneg u hu)
      _ = (G*r^2/2) * ∫ u in (-1/2 : ℝ)..(1/2 : ℝ), peanoCubic u*u^2 := by
        rw [← intervalIntegral.integral_const_mul]
        congr 1
        funext u
        ring
      _ = G*r^2/240 := by rw [hmom]; ring
  have habs : |t-2| = 6 * |∫ u in (-1/2 : ℝ)..(1/2 : ℝ), peanoCubic u * f u| := by
    rw [abs_sub_comm, ← heq, abs_mul]
    norm_num
  rw [habs]
  linarith [hbound]

end I4ActualQuarticTransfer

namespace I4ActualQuarticTransfer

/-- Honest cubic Taylor remainders at two exact zero endpoints recover the
constant and linear coefficients, with their half-interval factors. -/
theorem endpoint_taylor_low_coefficients (v : ℝ → ℝ) (r G A B T C : ℝ)
    (hr : 0 < r) (hp : v (r/2) = 0) (hm : v (-r/2) = 0)
    (hTp : |v (r/2) - (A+B*(r/2)+T*(r/2)^2/2+C*(r/2)^3/6)| ≤ G*r^4/384)
    (hTm : |v (-r/2) - (A+B*(-r/2)+T*(-r/2)^2/2+C*(-r/2)^3/6)| ≤ G*r^4/384) :
    |A+T*r^2/8| ≤ G*r^4/384 ∧ |B+C*r^2/24| ≤ G*r^3/192 := by
  rw [hp, zero_sub, abs_neg] at hTp
  rw [hm, zero_sub, abs_neg] at hTm
  obtain ⟨hpL,hpU⟩ := abs_le.mp hTp
  obtain ⟨hmL,hmU⟩ := abs_le.mp hTm
  constructor
  · apply abs_le.mpr
    constructor <;> nlinarith
  · have hodd : |r*(B+C*r^2/24)| ≤ G*r^4/192 := by
      apply abs_le.mpr
      constructor <;> nlinarith
    rw [abs_mul, abs_of_pos hr] at hodd
    apply le_of_mul_le_mul_left _ hr
    calc
      _ ≤ G*r^4/192 := hodd
      _ = _ := by ring

/-- The Peano improvement t=2+O(r²G) gives the corrected axial constant
coefficient 11/1920, rather than an assumed ordinary Taylor coefficient. -/
theorem corrected_axial_constant (r G A T : ℝ)
    (hconst : |A+T*r^2/8| ≤ G*r^4/384)
    (hcubic : |T-2| ≤ G*r^2/40) :
    |A+r^2/4| ≤ (11/1920 : ℝ)*G*r^4 := by
  calc
    _ = |(A+T*r^2/8) + (2-T)*r^2/8| := by congr 1; ring
    _ ≤ |A+T*r^2/8| + |(2-T)*r^2/8| := abs_add_le _ _
    _ = |A+T*r^2/8| + |T-2| *r^2/8 := by
      rw [abs_div, abs_mul, abs_sub_comm 2 T, abs_sq]
      norm_num
    _ ≤ G*r^4/384 + (G*r^2/40)*r^2/8 := by
      gcongr
    _ = _ := by ring

end I4ActualQuarticTransfer

namespace I4ActualQuarticTransfer

def scalarTaylor (g : ℝ → ℝ) (n : ℕ) (x : ℝ) : ℝ :=
  taylorWithinEval g n univ 0 x

private theorem scalarTaylor_eq_interval (g : ℝ → ℝ)
    (hg : ContDiff ℝ (⊤ : ℕ∞) g) (n : ℕ) (x : ℝ) (hx : 0 ≠ x) :
    scalarTaylor g n x = taylorWithinEval g n (uIcc 0 x) 0 x := by
  rw [scalarTaylor, taylor_within_apply, taylor_within_apply]
  apply Finset.sum_congr rfl
  intro k hk
  rw [iteratedDerivWithin_univ]
  have hkg : ContDiff ℝ k g := hg.of_le (by simp)
  rw [iteratedDerivWithin_eq_iteratedDeriv (uniqueDiffOn_uIcc hx)
    hkg.contDiffAt (left_mem_uIcc : (0 : ℝ) ∈ uIcc 0 x)]

/-- The sharp Lagrange factorial, valid on either side of the origin. -/
theorem scalar_taylor_remainder (g : ℝ → ℝ)
    (hg : ContDiff ℝ (⊤ : ℕ∞) g) (n : ℕ) (G : ℝ)
    (hG : ∀ y : ℝ, |iteratedDeriv (n+1) g y| ≤ G) (x : ℝ) :
    |g x - scalarTaylor g n x| ≤ G * |x| ^ (n+1) / (n+1)! := by
  by_cases hx : x = 0
  · subst x
    simp [scalarTaylor]
  have hnx : (0 : ℝ) ≠ x := Ne.symm hx
  have hgn : ContDiff ℝ (n+1) g := hg.of_le (by simp)
  obtain ⟨y,hy,heq⟩ := taylor_mean_remainder_lagrange_iteratedDeriv hnx hgn.contDiffOn
  rw [scalarTaylor_eq_interval g hg n x hnx, heq]
  simp only [sub_zero]
  calc
    _ = |iteratedDeriv (n+1) g y| * |x| ^ (n+1) / (n+1)! := by
      rw [abs_div, abs_mul, abs_pow, abs_of_nonneg (show 0 ≤ ((n+1)! : ℝ) from Nat.cast_nonneg _)]
    _ ≤ _ := div_le_div_of_nonneg_right
      (mul_le_mul_of_nonneg_right (hG y) (pow_nonneg (abs_nonneg x) _)) (Nat.cast_nonneg _)

theorem scalarTaylor_one (g : ℝ → ℝ) (x : ℝ) :
    scalarTaylor g 1 x = g 0 + x * deriv g 0 := by
  norm_num [scalarTaylor, taylor_within_apply, Finset.sum_range_succ,
    iteratedDerivWithin_univ, smul_eq_mul]

theorem scalarTaylor_three (g : ℝ → ℝ) (x : ℝ) :
    scalarTaylor g 3 x = g 0 + x * deriv g 0 +
      x^2 * iteratedDeriv 2 g 0 / 2 + x^3 * iteratedDeriv 3 g 0 / 6 := by
  norm_num [scalarTaylor, taylor_within_apply, Finset.sum_range_succ,
    iteratedDerivWithin_univ, smul_eq_mul]
  ring

theorem scalarTaylor_two (g : ℝ → ℝ) (x : ℝ) :
    scalarTaylor g 2 x = g 0 + x * deriv g 0 + x^2 * iteratedDeriv 2 g 0 / 2 := by
  norm_num [scalarTaylor, taylor_within_apply, Finset.sum_range_succ,
    iteratedDerivWithin_univ, smul_eq_mul]
  ring

theorem scalar_taylor_one_bound (g : ℝ → ℝ)
    (hg : ContDiff ℝ (⊤ : ℕ∞) g) (G : ℝ)
    (hG : ∀ y : ℝ, |iteratedDeriv 2 g y| ≤ G) (x : ℝ) :
    |g x - g 0 - x * deriv g 0| ≤ G * x^2 / 2 := by
  have hb := scalar_taylor_remainder g hg 1 G hG x
  rw [scalarTaylor_one] at hb
  norm_num only [Nat.reduceAdd, Nat.factorial_succ, Nat.factorial_zero, Nat.cast_ofNat] at hb
  rw [sq_abs] at hb
  convert hb using 1
  congr 1
  ring

theorem scalar_taylor_three_bound (g : ℝ → ℝ)
    (hg : ContDiff ℝ (⊤ : ℕ∞) g) (G : ℝ)
    (hG : ∀ y : ℝ, |iteratedDeriv 4 g y| ≤ G) (x : ℝ) :
    |g x - (g 0 + x * deriv g 0 + x^2 * iteratedDeriv 2 g 0 / 2 +
      x^3 * iteratedDeriv 3 g 0 / 6)| ≤ G * x^4 / 24 := by
  have hb := scalar_taylor_remainder g hg 3 G hG x
  rw [scalarTaylor_three] at hb
  norm_num only [Nat.reduceAdd, Nat.factorial_succ, Nat.factorial_zero, Nat.cast_ofNat] at hb
  have hpow : |x|^4 = x^4 := by rw [← abs_pow, abs_of_nonneg (by positivity : 0 ≤ x^4)]
  rw [hpow] at hb
  exact hb

theorem scalar_taylor_two_bound (g : ℝ → ℝ)
    (hg : ContDiff ℝ (⊤ : ℕ∞) g) (G : ℝ)
    (hG : ∀ y : ℝ, |iteratedDeriv 3 g y| ≤ G) (x : ℝ) :
    |g x - (g 0 + x * deriv g 0 + x^2 * iteratedDeriv 2 g 0 / 2)| ≤
      G * |x|^3 / 6 := by
  have hb := scalar_taylor_remainder g hg 2 G hG x
  rw [scalarTaylor_two] at hb
  norm_num only [Nat.reduceAdd, Nat.factorial_succ, Nat.factorial_zero, Nat.cast_ofNat] at hb
  exact hb

end I4ActualQuarticTransfer

namespace I4ActualQuarticTransfer

theorem smooth_iteratedDeriv (g : ℝ → ℝ) (hg : ContDiff ℝ (⊤ : ℕ∞) g) (k : ℕ) :
    ContDiff ℝ (⊤ : ℕ∞) (iteratedDeriv k g) := by
  induction k with
  | zero => simpa using hg
  | succ k hk =>
    rw [iteratedDeriv_succ]
    have hm : ContDiff ℝ ((⊤ : ℕ∞)+1) (iteratedDeriv k g) := by simpa using hk
    exact hm.deriv'

theorem iteratedDeriv_iteratedDeriv (g : ℝ → ℝ) (n k : ℕ) :
    iteratedDeriv n (iteratedDeriv k g) = iteratedDeriv (n+k) g := by
  simp only [iteratedDeriv_eq_iterate, Function.iterate_add_apply]

theorem sourceF_smooth {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) :
    ContDiff ℝ (⊤ : ℕ∞) (sourceF L ω) :=
  (smoothSourceField_smooth 2 hL ω).comp axisMap.contDiff

theorem sourceH_smooth {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) :
    ContDiff ℝ (⊤ : ℕ∞) (sourceH L ω) :=
  axis_transverse_smooth _ (smoothSourceField_smooth 2 hL ω)

theorem sourceF_iteratedDeriv_abs_le {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L)
    (k : ℕ) (t : ℝ) :
    |iteratedDeriv k (sourceF L ω) t| ≤ sourceDerivativeMajorant L k ω := by
  unfold sourceF
  rw [axis_iteratedDeriv _ (smoothSourceField_smooth 2 hL ω) k t]
  exact source_axis_derivative_abs_le hL ω k (fun _ => directionX)
    (fun _ => directionX_norm_le_one) t

theorem sourceH_iteratedDeriv_abs_le {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L)
    (k : ℕ) (t : ℝ) :
    |iteratedDeriv k (sourceH L ω) t| ≤ sourceDerivativeMajorant L (k+1) ω := by
  unfold sourceH
  rw [axis_transverse_iteratedDeriv _ (smoothSourceField_smooth 2 hL ω) k t]
  apply source_axis_derivative_abs_le hL ω (k+1) _ ?_ t
  intro i
  refine Fin.lastCases ?_ (fun j => ?_) i
  · simpa only [Fin.snoc_last] using directionY_norm_le_one
  · simpa only [Fin.snoc_castSucc] using directionX_norm_le_one

end I4ActualQuarticTransfer

open I4ActualQuarticTransfer

namespace I4SourcePinPreservingQuartic

abbrev SourcePlane := EuclideanSpace ℝ (Fin 2)

def sourceAxialThird (L : ℝ) (ω : SmoothSample 2 L) : ℝ :=
  iteratedFDeriv ℝ 3 (smoothSourceField 2 L ω) 0 ![directionX,directionX,directionX]

/-- Exact LM001 raw order; the transverse curvature q is deliberately separate. -/
def sourceRawU (L : ℝ) (ω : SmoothSample 2 L) : Fin 8 → ℝ :=
  ![sourceA L ω,
    iteratedFDeriv ℝ 3 (smoothSourceField 2 L ω) 0 ![directionX,directionY,directionY],
    iteratedFDeriv ℝ 3 (smoothSourceField 2 L ω) 0 ![directionY,directionY,directionY],
    iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![directionX,directionX,directionX,directionX],
    iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![directionX,directionX,directionX,directionY],
    iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![directionX,directionX,directionY,directionY],
    iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![directionX,directionY,directionY,directionY],
    iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![directionY,directionY,directionY,directionY] ]

def sourceRawRadius (L : ℝ) (ω : SmoothSample 2 L) : ℝ :=
  1 + ∑ i, |sourceRawU L ω i|

/-- Four exact physical gradient pins and the exact height difference. -/
def sourcePhysicalPins (L r : ℝ) (ω : SmoothSample 2 L) : Prop :=
  rawPins L r ω 2 = 0 ∧ rawPins L r ω 3 = 0 ∧
  rawPins L r ω 4 = 0 ∧ rawPins L r ω 5 = 0 ∧
  rawPins L r ω 1 - rawPins L r ω 0 = -r^3/6

/-- Literal LM001 polynomial, in the exact eight-coordinate raw source frame. -/
def pinPreservingQuartic (r q : ℝ) (U : Fin 8 → ℝ) (p : Fin 2 → ℝ) : Fin 2 → ℝ :=
  let X := p 0
  let Y := p 1
  ![X^2-1/4+U 0*X*Y+(U 1/2)*Y^2+
      r*((U 3/6)*X*(X^2-1/4)+(U 4/6)*(3*X^2-1/4)*Y+
        (U 5/2)*X*Y^2+(U 6/6)*Y^3),
    (q/r)*Y+(U 0/2)*(X^2-1/4)+U 1*X*Y+(U 2/2)*Y^2+
      r*((U 4/6)*X*(X^2-1/4)+(U 5/2)*X^2*Y+
        (U 6/2)*X*Y^2+(U 7/6)*Y^3)]

def sourceQuartic (L r : ℝ) (ω : SmoothSample 2 L) (p : SourcePlane) : SourcePlane :=
  toLp 2 (pinPreservingQuartic r (sourceQ L ω) (sourceRawU L ω) (ofLp p))

def sourceScaledGradientRaw (L r : ℝ) (ω : SmoothSample 2 L)
    (p : Fin 2 → ℝ) : Fin 2 → ℝ :=
  ![fderiv ℝ (smoothSourceField 2 L ω) (r • p) directionX/r^2,
    fderiv ℝ (smoothSourceField 2 L ω) (r • p) directionY/r^2]

def sourceScaledGradient (L r : ℝ) (ω : SmoothSample 2 L) (p : SourcePlane) : SourcePlane :=
  toLp 2 (sourceScaledGradientRaw L r ω (ofLp p))



/-- The Pi sup norm is bounded by the actual Euclidean norm. -/
theorem pi_norm_le_euclidean_norm {ι : Type*} [Fintype ι] (v : ι → ℝ) :
    ‖v‖ ≤ ‖toLp 2 v‖ := by
  apply (pi_norm_le_iff_of_nonneg (norm_nonneg _)).mpr
  intro i
  exact PiLp.norm_apply_le (toLp 2 v) i

theorem euclidean_two_norm_sq (v : EuclideanSpace ℝ (Fin 2)) :
    ‖v‖^2 = (v 0)^2+(v 1)^2 := by
  simpa only [Fin.sum_univ_two] using EuclideanSpace.real_norm_sq_eq v

theorem euclidean_two_norm_le_abs_sum (v : EuclideanSpace ℝ (Fin 2)) :
    ‖v‖ ≤ |v 0|+|v 1| := by
  have hs := euclidean_two_norm_sq v
  have habs : 0 ≤ |v 0|+|v 1| := add_nonneg (abs_nonneg _) (abs_nonneg _)
  have hp : 0 ≤ |v 0| * |v 1| := mul_nonneg (abs_nonneg _) (abs_nonneg _)
  nlinarith [sq_abs (v 0),sq_abs (v 1),norm_nonneg v]

theorem euclidean_two_norm_le_two_mul (v : EuclideanSpace ℝ (Fin 2)) (B : ℝ)
    (h0 : |v 0| ≤ B) (h1 : |v 1| ≤ B) : ‖v‖ ≤ 2*B := by
  exact (euclidean_two_norm_le_abs_sum v).trans (by linarith)

/-- Matrix action on Euclidean space, with row=output and column=input. -/
def matrixLinearEuclidean (A : Matrix (Fin 2) (Fin 2) ℝ) :
    EuclideanSpace ℝ (Fin 2) →L[ℝ] EuclideanSpace ℝ (Fin 2) :=
  Matrix.toEuclideanCLM (𝕜 := ℝ) A

@[simp] theorem matrixLinearEuclidean_apply (A : Matrix (Fin 2) (Fin 2) ℝ)
    (v : EuclideanSpace ℝ (Fin 2)) :
    ofLp (matrixLinearEuclidean A v) = A *ᵥ ofLp v := rfl

/-- A square-sum coefficient bound controls the induced Euclidean norm. -/
theorem matrixLinearEuclidean_norm_le_of_sqsum
    (A : Matrix (Fin 2) (Fin 2) ℝ) (B : ℝ) (hB : 0 ≤ B)
    (hA : (A 0 0)^2+(A 0 1)^2+(A 1 0)^2+(A 1 1)^2 ≤ B^2) :
    ‖matrixLinearEuclidean A‖ ≤ B := by
  apply ContinuousLinearMap.opNorm_le_bound _ hB
  intro v
  have hx := euclidean_two_norm_sq v
  have hy : ‖matrixLinearEuclidean A v‖^2 =
      (A 0 0*v 0+A 0 1*v 1)^2+(A 1 0*v 0+A 1 1*v 1)^2 := by
    simpa [matrixLinearEuclidean_apply, Matrix.mulVec, dotProduct, Fin.sum_univ_two] using
      euclidean_two_norm_sq (matrixLinearEuclidean A v)
  have hc0 : (A 0 0*v 0+A 0 1*v 1)^2 ≤
      ((A 0 0)^2+(A 0 1)^2)*((v 0)^2+(v 1)^2) := by
    nlinarith [sq_nonneg (A 0 0*v 1-A 0 1*v 0)]
  have hc1 : (A 1 0*v 0+A 1 1*v 1)^2 ≤
      ((A 1 0)^2+(A 1 1)^2)*((v 0)^2+(v 1)^2) := by
    nlinarith [sq_nonneg (A 1 0*v 1-A 1 1*v 0)]
  have hp := mul_le_mul_of_nonneg_right hA (sq_nonneg ‖v‖)
  rw [hx] at hp
  have hs : ‖matrixLinearEuclidean A v‖^2 ≤ (B*‖v‖)^2 := by
    nlinarith [hc0,hc1,hp]
  exact (sq_le_sq₀ (norm_nonneg _) (mul_nonneg hB (norm_nonneg _))).mp hs

/-- Every one of four entry errors bounded by B gives the safe factor two. -/
theorem matrixLinearEuclidean_norm_le_two_mul
    (A : Matrix (Fin 2) (Fin 2) ℝ) (B : ℝ) (hB : 0 ≤ B)
    (hA : ∀ i j, |A i j| ≤ B) : ‖matrixLinearEuclidean A‖ ≤ 2*B := by
  apply matrixLinearEuclidean_norm_le_of_sqsum A (2*B) (by positivity)
  have hs (i j : Fin 2) : (A i j)^2 ≤ B^2 := by
    simpa only [sq_abs] using pow_le_pow_left₀ (abs_nonneg _) (hA i j) 2
  nlinarith [hs 0 0,hs 0 1,hs 1 0,hs 1 1]

theorem matrixLinearEuclidean_offdiag_norm_le (b : ℝ) :
    ‖matrixLinearEuclidean !![0,b;b,0]‖ ≤ |b| := by
  apply ContinuousLinearMap.opNorm_le_bound _ (abs_nonneg b)
  intro v
  have hy : ‖matrixLinearEuclidean !![0,b;b,0] v‖^2 = (b*v 1)^2+(b*v 0)^2 := by
    simpa [matrixLinearEuclidean_apply, Matrix.mulVec, dotProduct, Fin.sum_univ_two] using
      euclidean_two_norm_sq (matrixLinearEuclidean !![0,b;b,0] v)
  have heq : ‖matrixLinearEuclidean !![0,b;b,0] v‖^2 = (|b| * ‖v‖)^2 := by
    rw [hy]
    simp only [mul_pow,sq_abs,euclidean_two_norm_sq]
    ring
  exact (sq_le_sq₀ (norm_nonneg _) (mul_nonneg (abs_nonneg _) (norm_nonneg _))).mp heq.le

/-- The symmetric three-coefficient correction has the sum of its three
absolute coefficients as an induced Euclidean operator bound. -/
theorem matrixLinearEuclidean_symmetric_norm_le_abs_sum (a b c : ℝ) :
    ‖matrixLinearEuclidean !![a,b;b,c]‖ ≤ |a|+|b|+|c| := by
  have h0 : ‖matrixLinearEuclidean !![a,0;0,0]‖ ≤ |a| := by
    apply matrixLinearEuclidean_norm_le_of_sqsum _ _ (abs_nonneg _)
    norm_num [sq_abs]
  have h1 : ‖matrixLinearEuclidean !![0,0;0,c]‖ ≤ |c| := by
    apply matrixLinearEuclidean_norm_le_of_sqsum _ _ (abs_nonneg _)
    norm_num [sq_abs]
  have heq : (!![a,b;b,c] : Matrix (Fin 2) (Fin 2) ℝ) =
      !![a,0;0,0]+!![0,b;b,0]+!![0,0;0,c] := by
    ext i j
    fin_cases i <;> fin_cases j <;> simp
  rw [heq]
  simp only [matrixLinearEuclidean,map_add]
  calc
    _ ≤ ‖Matrix.toEuclideanCLM (𝕜 := ℝ) !![a,0;0,0] +
        Matrix.toEuclideanCLM (𝕜 := ℝ) !![0,b;b,0]‖ +
        ‖Matrix.toEuclideanCLM (𝕜 := ℝ) !![0,0;0,c]‖ := norm_add_le _ _
    _ ≤ ‖matrixLinearEuclidean !![a,0;0,0]‖+
        ‖matrixLinearEuclidean !![0,b;b,0]‖+
        ‖matrixLinearEuclidean !![0,0;0,c]‖ :=
      add_le_add (norm_add_le _ _) le_rfl
    _ ≤ _ := add_le_add (add_le_add h0 (matrixLinearEuclidean_offdiag_norm_le b)) h1

theorem matrixLinearEuclidean_symmetric_norm_le_three_mul (a b c B : ℝ)
    (ha : |a| ≤ B) (hb : |b| ≤ B) (hc : |c| ≤ B) :
    ‖matrixLinearEuclidean !![a,b;b,c]‖ ≤ 3*B :=
  (matrixLinearEuclidean_symmetric_norm_le_abs_sum a b c).trans (by linarith)




def lineMap (v : Fin 2 → ℝ) : ℝ →L[ℝ] (Fin 2 → ℝ) :=
  (ContinuousLinearMap.id ℝ ℝ).smulRight v

theorem line_iteratedDeriv (f : (Fin 2 → ℝ) → ℝ)
    (hf : ContDiff ℝ (⊤ : ℕ∞) f) (k : ℕ) (v : Fin 2 → ℝ) (t : ℝ) :
    iteratedDeriv k (fun s => f (s • v)) t =
      iteratedFDeriv ℝ k f (t • v) (fun _ => v) := by
  rw [iteratedDeriv_eq_iteratedFDeriv]
  have h := (lineMap v).iteratedFDeriv_comp_right hf t (i := k) (by simp)
  have hh := congrArg (fun A => A (fun _ => (1 : ℝ))) h
  simpa [Function.comp_def,lineMap,ContinuousMultilinearMap.compContinuousLinearMap_apply] using hh

theorem derivativeComponent_smooth (f : (Fin 2 → ℝ) → ℝ)
    (hf : ContDiff ℝ (⊤ : ℕ∞) f) (u : Fin 2 → ℝ) :
    ContDiff ℝ (⊤ : ℕ∞) (fun x => fderiv ℝ f x u) :=
  (hf.fderiv_right (by simp)).clm_apply contDiff_const

theorem derivativeComponent_iteratedFDeriv (f : (Fin 2 → ℝ) → ℝ)
    (hf : ContDiff ℝ (⊤ : ℕ∞) f) (k : ℕ) (x : Fin 2 → ℝ)
    (v : Fin k → (Fin 2 → ℝ)) (u : Fin 2 → ℝ) :
    iteratedFDeriv ℝ k (fun y => fderiv ℝ f y u) x v =
      iteratedFDeriv ℝ (k+1) f x (Fin.snoc v u) := by
  have hdf : ContDiff ℝ (⊤ : ℕ∞) (fderiv ℝ f) := hf.fderiv_right (by simp)
  calc
    _ = iteratedFDeriv ℝ k (fderiv ℝ f) x v u :=
      iteratedFDeriv_clm_apply_const_apply hdf (by simp)
    _ = _ := by rw [iteratedFDeriv_succ_apply_right,Fin.init_snoc,Fin.snoc_last]

theorem line_gradient_iteratedDeriv (f : (Fin 2 → ℝ) → ℝ)
    (hf : ContDiff ℝ (⊤ : ℕ∞) f) (k : ℕ) (v u : Fin 2 → ℝ) (t : ℝ) :
    iteratedDeriv k (fun s => fderiv ℝ f (s • v) u) t =
      iteratedFDeriv ℝ (k+1) f (t • v) (Fin.snoc (fun _ => v) u) := by
  rw [line_iteratedDeriv _ (derivativeComponent_smooth f hf u)]
  exact derivativeComponent_iteratedFDeriv f hf k _ _ u

theorem source_derivative_abs_le {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L)
    (k : ℕ) (x : Fin 2 → ℝ) (u : Fin k → (Fin 2 → ℝ)) :
    |iteratedFDeriv ℝ k (smoothSourceField 2 L ω) x u| ≤
      sourceDerivativeMajorant L k ω * ∏ i, ‖u i‖ := by
  exact (ContinuousMultilinearMap.le_opNorm _ _).trans
    (mul_le_mul_of_nonneg_right (smoothSourceField_global_derivative_bound hL k ω x)
      (Finset.prod_nonneg (fun _ _ => norm_nonneg _)))

theorem source_line_gradient_taylor {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L)
    (v u : Fin 2 → ℝ) :
    |fderiv ℝ (smoothSourceField 2 L ω) v u -
      (fderiv ℝ (smoothSourceField 2 L ω) 0 u +
        iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω) 0 ![v,u] +
        iteratedFDeriv ℝ 3 (smoothSourceField 2 L ω) 0 ![v,v,u]/2 +
        iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![v,v,v,u]/6)| ≤
      sourceDerivativeMajorant L 5 ω * ‖v‖^4 * ‖u‖/24 := by
  let f := smoothSourceField 2 L ω
  have hf : ContDiff ℝ (⊤ : ℕ∞) f := smoothSourceField_smooth 2 hL ω
  let g := fun s : ℝ => fderiv ℝ f (s • v) u
  have hg : ContDiff ℝ (⊤ : ℕ∞) g :=
    (derivativeComponent_smooth f hf u).comp (lineMap v).contDiff
  have hbd (s : ℝ) : |iteratedDeriv 4 g s| ≤ sourceDerivativeMajorant L 5 ω * ‖v‖^4*‖u‖ := by
    rw [show g=(fun s => fderiv ℝ f (s • v) u) from rfl,line_gradient_iteratedDeriv f hf]
    have h := source_derivative_abs_le hL ω 5 (s • v) (Fin.snoc (fun _ : Fin 4 => v) u)
    have he : (fun i : Fin 5 => ‖(Fin.snoc (fun _ : Fin 4 => v) u : Fin 5 → (Fin 2 → ℝ)) i‖) =
        Fin.snoc (fun _ : Fin 4 => ‖v‖) ‖u‖ := by ext i; fin_cases i <;> rfl
    rw [he,Fin.prod_snoc] at h
    simpa only [Finset.prod_const,Finset.card_univ,Fintype.card_fin,mul_assoc] using h
  have h := scalar_taylor_three_bound g hg _ hbd 1
  have hd1 := line_gradient_iteratedDeriv f hf 1 v u 0
  have hd2 := line_gradient_iteratedDeriv f hf 2 v u 0
  have hd3 := line_gradient_iteratedDeriv f hf 3 v u 0
  have h1 : Fin.snoc (fun _ : Fin 1 => v) u = ![v,u] := by ext i; fin_cases i <;> rfl
  have h2 : Fin.snoc (fun _ : Fin 2 => v) u = ![v,v,u] := by ext i; fin_cases i <;> rfl
  have h3 : Fin.snoc (fun _ : Fin 3 => v) u = ![v,v,v,u] := by ext i; fin_cases i <;> rfl
  simp only [iteratedDeriv_one,zero_smul,h1,h2,h3] at hd1 hd2 hd3
  simp only [show g 1=fderiv ℝ f v u by simp [g],show g 0=fderiv ℝ f 0 u by simp [g],
    show deriv g 0=iteratedFDeriv ℝ 2 f 0 ![v,u] from hd1,
    show iteratedDeriv 2 g 0=iteratedFDeriv ℝ 3 f 0 ![v,v,u] from hd2,
    show iteratedDeriv 3 g 0=iteratedFDeriv ℝ 4 f 0 ![v,v,v,u] from hd3,
    one_mul,one_pow,mul_one] at h
  exact h

theorem modeCoefficient_analytic_order (L : ℝ) (m : SourceMode 2) :
    ContDiff ℝ (⊤ : WithTop ℕ∞) (modeCoefficient 2 L m) := by
  cases m with
  | none =>
    change ContDiff ℝ (⊤ : WithTop ℕ∞) (fun _ : Fin 2 → ℝ => Real.sqrt (1/sourceZ 2 L))
    fun_prop
  | some p =>
    rcases p with ⟨k,b⟩
    change ContDiff ℝ (⊤ : WithTop ℕ∞) (fun x : Fin 2 → ℝ => Real.sqrt (2*sourceWeight 2 L k/sourceZ 2 L)*
      if b then Real.sin (phase 2 L k x) else Real.cos (phase 2 L k x))
    cases b <;> simp only [Bool.false_eq_true,ite_false,ite_true] <;> unfold phase <;> fun_prop

/-- Symmetry is proved mode by mode; analyticity of the whole random field
is not asserted or needed. -/
theorem source_derivative_comp_perm {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L)
    (k : ℕ) (x : Fin 2 → ℝ) (u : Fin k → (Fin 2 → ℝ)) (σ : Equiv.Perm (Fin k)) :
    iteratedFDeriv ℝ k (smoothSourceField 2 L ω) x (u ∘ σ) =
      iteratedFDeriv ℝ k (smoothSourceField 2 L ω) x u := by
  rw [smoothSourceField_derivative_series 2 hL,smoothSourceField_derivative_series 2 hL]
  unfold scalarSeries
  apply tsum_congr
  intro m
  congr 1
  exact (modeCoefficient_analytic_order L m).contDiffAt.iteratedFDeriv_comp_perm u σ




private theorem sourceF_third_zero {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) :
    iteratedDeriv 3 (sourceF L ω) 0 = sourceAxialThird L ω := by
  have hd : (fun _ : Fin 3 => directionX) = ![directionX,directionX,directionX] := by
    ext i; fin_cases i <;> rfl
  have h0 : (![0,0] : Fin 2 → ℝ) = 0 := by ext i; fin_cases i <;> rfl
  change iteratedDeriv 3 (fun s => smoothSourceField 2 L ω ![s,0]) 0 =
    iteratedFDeriv ℝ 3 (smoothSourceField 2 L ω) 0 ![directionX,directionX,directionX]
  simpa only [hd,h0] using
    axis_iteratedDeriv _ (smoothSourceField_smooth 2 hL ω) 3 0

private theorem sourceF_fourth_zero {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) :
    iteratedDeriv 4 (sourceF L ω) 0 = sourceRawU L ω 3 := by
  have hd : (fun _ : Fin 4 => directionX) = ![directionX,directionX,directionX,directionX] := by
    ext i; fin_cases i <;> rfl
  have h0 : (![0,0] : Fin 2 → ℝ) = 0 := by ext i; fin_cases i <;> rfl
  change iteratedDeriv 4 (fun s => smoothSourceField 2 L ω ![s,0]) 0 =
    iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![directionX,directionX,directionX,directionX]
  simpa only [hd,h0] using
    axis_iteratedDeriv _ (smoothSourceField_smooth 2 hL ω) 4 0

private theorem sourceH_third_zero {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) :
    iteratedDeriv 3 (sourceH L ω) 0 = sourceRawU L ω 4 := by
  have hd : Fin.snoc (fun _ : Fin 3 => directionX) directionY =
      ![directionX,directionX,directionX,directionY] := by ext i; fin_cases i <;> rfl
  have h0 : (![0,0] : Fin 2 → ℝ) = 0 := by ext i; fin_cases i <;> rfl
  change iteratedDeriv 3 (fun s => fderiv ℝ (smoothSourceField 2 L ω) ![s,0] directionY) 0 =
    iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![directionX,directionX,directionX,directionY]
  simpa only [hd,h0] using
    axis_transverse_iteratedDeriv _ (smoothSourceField_smooth 2 hL ω) 3 0

private theorem sourceF_deriv_pins {L : ℝ} (hL : L ≠ 0) (r : ℝ)
    (ω : SmoothSample 2 L) (hp : sourcePhysicalPins L r ω) :
    deriv (sourceF L ω) (-r/2) = 0 ∧ deriv (sourceF L ω) (r/2) = 0 := by
  constructor
  · rw [sourceF_deriv hL]
    exact hp.1
  · rw [sourceF_deriv hL]
    exact hp.2.1

private theorem sourceH_pins (L r : ℝ) (ω : SmoothSample 2 L)
    (hp : sourcePhysicalPins L r ω) : sourceH L ω (-r/2) = 0 ∧ sourceH L ω (r/2) = 0 :=
  ⟨hp.2.2.1,hp.2.2.2.1⟩

theorem source_axial_third_error {L : ℝ} (hL : L ≠ 0) (r : ℝ) (hr : 0 < r)
    (ω : SmoothSample 2 L) (hp : sourcePhysicalPins L r ω) :
    |sourceAxialThird L ω - 2| ≤ r^2 * sourceDerivativeMajorant L 5 ω / 40 := by
  have hFp := sourceF_deriv_pins hL r ω hp
  have hpin : pin5 (sourceF L ω) r = 2 := by
    unfold pin5
    rw [hFp.1,hFp.2]
    have hgap : sourceF L ω (r/2) - sourceF L ω (-r/2) = -r^3/6 := hp.2.2.2.2
    rw [hgap]
    field_simp [ne_of_gt hr]
    ring
  have hpeano : 6 * (∫ u in (-1/2 : ℝ)..(1/2 : ℝ), peanoCubic u *
      iteratedDeriv 3 (sourceF L ω) (r*u)) = 2 := by
    simpa only [peanoCubic] using
      (pin5_integral (sourceF L ω) (sourceF_C3 hL ω) r (ne_of_gt hr)).symm.trans hpin
  have hbound (y : ℝ) : |iteratedDeriv 2 (iteratedDeriv 3 (sourceF L ω)) y| ≤
      sourceDerivativeMajorant L 5 ω := by
    rw [iteratedDeriv_iteratedDeriv]
    exact sourceF_iteratedDeriv_abs_le hL ω 5 y
  have hb := symmetric_cubic_pin_second_order (iteratedDeriv 3 (sourceF L ω))
    (sourceF_third_continuous hL ω) r (sourceAxialThird L ω) (sourceRawU L ω 3)
    (sourceDerivativeMajorant L 5 ω) (sourceDerivativeMajorant_nonneg L 5 ω) hpeano
    (by
      intro u hu
      have ht := scalar_taylor_one_bound (iteratedDeriv 3 (sourceF L ω))
        (smooth_iteratedDeriv _ (sourceF_smooth hL ω) 3) _ hbound (r*u)
      rw [sourceF_third_zero hL ω] at ht
      have hd : deriv (iteratedDeriv 3 (sourceF L ω)) 0 = sourceRawU L ω 3 := by
        rw [← iteratedDeriv_succ]
        exact sourceF_fourth_zero hL ω
      rw [hd] at ht
      convert ht using 1
      ring)
  simpa only [mul_comm] using hb

private theorem endpoint_derivative_low (v : ℝ → ℝ) (hv : ContDiff ℝ (⊤ : ℕ∞) v)
    (G : ℝ) (hG : ∀ y, |iteratedDeriv 4 v y| ≤ G) (r : ℝ) (hr : 0 < r)
    (hp : v (r/2) = 0) (hm : v (-r/2) = 0) :
    |v 0 + iteratedDeriv 2 v 0*r^2/8| ≤ G*r^4/384 ∧
    |deriv v 0 + iteratedDeriv 3 v 0*r^2/24| ≤ G*r^3/192 := by
  apply endpoint_taylor_low_coefficients v r G (v 0) (deriv v 0)
    (iteratedDeriv 2 v 0) (iteratedDeriv 3 v 0) hr hp hm
  · have hb := scalar_taylor_three_bound v hv G hG (r/2)
    convert hb using 1
    · congr 1; ring
    · ring
  · have hb := scalar_taylor_three_bound v hv G hG (-r/2)
    convert hb using 1
    · congr 1; ring
    · ring

/-- The literal low derivatives forced by the physical pins, using actual
fifth derivative bounds rather than any assumed Taylor remainder. -/
theorem source_low_pin_coefficients {L : ℝ} (hL : L ≠ 0) (r : ℝ) (hr : 0 < r)
    (ω : SmoothSample 2 L) (hp : sourcePhysicalPins L r ω) :
    |fderiv ℝ (smoothSourceField 2 L ω) 0 directionX + r^2/4| ≤
      (11/1920 : ℝ)*sourceDerivativeMajorant L 5 ω*r^4 ∧
    |fderiv ℝ (smoothSourceField 2 L ω) 0 directionY + sourceRawU L ω 0*r^2/8| ≤
      sourceDerivativeMajorant L 5 ω*r^4/384 ∧
    |iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω) 0 ![directionX,directionX] +
      sourceRawU L ω 3*r^2/24| ≤ sourceDerivativeMajorant L 5 ω*r^3/192 ∧
    |iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω) 0 ![directionX,directionY] +
      sourceRawU L ω 4*r^2/24| ≤ sourceDerivativeMajorant L 5 ω*r^3/192 := by
  have h0 : (![0,0] : Fin 2 → ℝ) = 0 := by ext i; fin_cases i <;> rfl
  have hfxs : ContDiff ℝ (⊤ : ℕ∞) (deriv (sourceF L ω)) := by
    simpa only [iteratedDeriv_one] using smooth_iteratedDeriv _ (sourceF_smooth hL ω) 1
  have hfx4 (y : ℝ) : |iteratedDeriv 4 (deriv (sourceF L ω)) y| ≤
      sourceDerivativeMajorant L 5 ω := by
    rw [← iteratedDeriv_succ']
    exact sourceF_iteratedDeriv_abs_le hL ω 5 y
  have hfp := sourceF_deriv_pins hL r ω hp
  have hbX := endpoint_derivative_low _ hfxs _ hfx4 r hr hfp.2 hfp.1
  have h2 : iteratedDeriv 2 (deriv (sourceF L ω)) = iteratedDeriv 3 (sourceF L ω) :=
    (iteratedDeriv_succ' (n := 2)).symm
  have h3 : iteratedDeriv 3 (deriv (sourceF L ω)) = iteratedDeriv 4 (sourceF L ω) :=
    (iteratedDeriv_succ' (n := 3)).symm
  have hB : deriv (deriv (sourceF L ω)) 0 = iteratedDeriv 2 (sourceF L ω) 0 := by
    rw [show 2 = 1+1 from rfl, iteratedDeriv_succ, iteratedDeriv_one]
  rw [h2,h3,hB,sourceF_third_zero hL ω,sourceF_fourth_zero hL ω] at hbX
  have hax : |sourceAxialThird L ω-2| ≤ sourceDerivativeMajorant L 5 ω*r^2/40 := by
    simpa only [mul_comm] using source_axial_third_error hL r hr ω hp
  have hfx := corrected_axial_constant r (sourceDerivativeMajorant L 5 ω)
    (deriv (sourceF L ω) 0) (sourceAxialThird L ω) hbX.1 hax
  have hHy := sourceH_pins L r ω hp
  have hbY := endpoint_derivative_low _ (sourceH_smooth hL ω) _
    (sourceH_iteratedDeriv_abs_le hL ω 4) r hr hHy.2 hHy.1
  rw [sourceH_second_zero hL ω,sourceH_third_zero hL ω] at hbY
  have hfx0 := sourceF_deriv hL ω 0
  have hfxx0 := sourceF_second hL ω 0
  have hfxy0 := sourceH_deriv hL ω 0
  rw [h0] at hfx0 hfxx0 hfxy0
  have hfy0 : sourceH L ω 0 = fderiv ℝ (smoothSourceField 2 L ω) 0 directionY := by
    change fderiv ℝ (smoothSourceField 2 L ω) ![0,0] directionY = _
    rw [h0]
  rw [hfx0] at hfx
  rw [hfxx0] at hbX
  rw [hfy0,hfxy0] at hbY
  exact ⟨hfx,hbY.1,hbX.2,hbY.2⟩


def coordinateDirection (i : Fin 2) : Fin 2 → ℝ := Pi.single i 1

@[simp] theorem coordinateDirection_zero : coordinateDirection 0 = ![1,0] := by
  ext i
  fin_cases i <;> simp [coordinateDirection]

@[simp] theorem coordinateDirection_one : coordinateDirection 1 = ![0,1] := by
  ext i
  fin_cases i <;> simp [coordinateDirection]

def euclideanToPi : EuclideanSpace ℝ (Fin 2) →L[ℝ] (Fin 2 → ℝ) :=
  (PiLp.continuousLinearEquiv 2 ℝ (fun _ : Fin 2 => ℝ)).toContinuousLinearMap

def piToEuclidean : (Fin 2 → ℝ) →L[ℝ] EuclideanSpace ℝ (Fin 2) :=
  (PiLp.continuousLinearEquiv 2 ℝ (fun _ : Fin 2 => ℝ)).symm.toContinuousLinearMap

def gradientPi (f : (Fin 2 → ℝ) → ℝ) (x : Fin 2 → ℝ) : Fin 2 → ℝ :=
  fun i => fderiv ℝ f x (coordinateDirection i)

def gradientEuclidean (f : (Fin 2 → ℝ) → ℝ) (z : EuclideanSpace ℝ (Fin 2)) :
    EuclideanSpace ℝ (Fin 2) := toLp 2 (gradientPi f (ofLp z))

/-- Output coordinate is the row; domain input coordinate is the column. -/
def hessianMatrix (f : (Fin 2 → ℝ) → ℝ) (x : Fin 2 → ℝ) :
    Matrix (Fin 2) (Fin 2) ℝ :=
  fun i j => iteratedFDeriv ℝ 2 f x ![coordinateDirection j,coordinateDirection i]

theorem hessianMatrix_apply (f : (Fin 2 → ℝ) → ℝ) (x : Fin 2 → ℝ) (i j : Fin 2) :
    hessianMatrix f x i j = fderiv ℝ (fderiv ℝ f) x (coordinateDirection j) (coordinateDirection i) := by
  unfold hessianMatrix
  rw [iteratedFDeriv_succ_apply_right]
  have hi : Fin.init ![coordinateDirection j,coordinateDirection i] = ![coordinateDirection j] := by
    ext k
    fin_cases k
    rfl
  rw [hi]
  change iteratedFDeriv ℝ 1 (fderiv ℝ f) x ![coordinateDirection j]
    (coordinateDirection i) = _
  rw [iteratedFDeriv_one_apply]
  rfl

theorem coordinate_decomposition (v : Fin 2 → ℝ) :
    v = v 0 • coordinateDirection 0 + v 1 • coordinateDirection 1 := by
  ext i
  fin_cases i <;> simp [coordinateDirection]

/-- The coordinate gradient on Euclidean space differentiates to the literal
second-derivative matrix, without identifying the two ambient norms. -/
theorem hasFDerivAt_gradientEuclidean
    (f : (Fin 2 → ℝ) → ℝ) (hf : ContDiff ℝ (⊤ : ℕ∞) f)
    (z : EuclideanSpace ℝ (Fin 2)) :
    HasFDerivAt (gradientEuclidean f) (matrixLinearEuclidean (hessianMatrix f (ofLp z))) z := by
  have hdf : Differentiable ℝ (fderiv ℝ f) :=
    (hf.fderiv_right (m := (⊤ : ℕ∞)) (by simp)).differentiable (by simp)
  let D := fderiv ℝ (fderiv ℝ f) (ofLp z)
  have hraw : HasFDerivAt (gradientPi f)
      (ContinuousLinearMap.pi (fun i : Fin 2 => D.flip (coordinateDirection i))) (ofLp z) := by
    apply hasFDerivAt_pi.mpr
    intro i
    have h := (hdf (ofLp z)).hasFDerivAt.clm_apply
      (hasFDerivAt_const (coordinateDirection i) (ofLp z))
    simpa [gradientPi,D] using h
  have hE := piToEuclidean.hasFDerivAt.comp z
    (hraw.comp z euclideanToPi.hasFDerivAt)
  have hmap : matrixLinearEuclidean (hessianMatrix f (ofLp z)) =
      piToEuclidean.comp ((ContinuousLinearMap.pi
        (fun i : Fin 2 => D.flip (coordinateDirection i))).comp euclideanToPi) := by
    ext v i
    change (hessianMatrix f (ofLp z) *ᵥ ofLp v) i = D (ofLp v) (coordinateDirection i)
    rw [coordinate_decomposition (ofLp v)]
    simp [Matrix.mulVec,dotProduct,Fin.sum_univ_two,hessianMatrix_apply,D,map_add,map_smul,coordinateDirection]
    ring
  rw [hmap]
  exact hE

theorem gradientEuclidean_eq_components (f : (Fin 2 → ℝ) → ℝ)
    (z : EuclideanSpace ℝ (Fin 2)) :
    gradientEuclidean f z = toLp 2 ![fderiv ℝ f (ofLp z) ![1,0],
      fderiv ℝ f (ofLp z) ![0,1] ] := by
  ext i
  fin_cases i <;> simp [gradientEuclidean,gradientPi]

def scaledGradientEuclidean (f : (Fin 2 → ℝ) → ℝ) (r : ℝ)
    (z : EuclideanSpace ℝ (Fin 2)) : EuclideanSpace ℝ (Fin 2) :=
  (r^2)⁻¹ • gradientEuclidean f (r • z)

/-- The actual scaled gradient has the literal scaled Hessian matrix as its
derivative. The chain factor r cancels one of the two value-scale factors. -/
theorem hasFDerivAt_scaledGradientEuclidean
    (f : (Fin 2 → ℝ) → ℝ) (hf : ContDiff ℝ (⊤ : ℕ∞) f)
    (r : ℝ) (hr : r ≠ 0) (z : EuclideanSpace ℝ (Fin 2)) :
    HasFDerivAt (scaledGradientEuclidean f r)
      (matrixLinearEuclidean (fun i j => hessianMatrix f (r • ofLp z) i j / r)) z := by
  have hs : HasFDerivAt (fun z : EuclideanSpace ℝ (Fin 2) => r • z)
      (r • ContinuousLinearMap.id ℝ (EuclideanSpace ℝ (Fin 2))) z := by
    exact (r • ContinuousLinearMap.id ℝ (EuclideanSpace ℝ (Fin 2))).hasFDerivAt
  have h := ((hasFDerivAt_gradientEuclidean f hf (r • z)).comp z hs).const_smul (r^2)⁻¹
  have hm : matrixLinearEuclidean (fun i j => hessianMatrix f (r • ofLp z) i j / r) =
      (r^2)⁻¹ • ((matrixLinearEuclidean (hessianMatrix f (ofLp (r • z)))).comp
        (r • ContinuousLinearMap.id ℝ (EuclideanSpace ℝ (Fin 2)))) := by
    ext v i
    change ((fun i j => hessianMatrix f (r • ofLp z) i j / r) *ᵥ ofLp v) i =
      (r^2)⁻¹ * ((hessianMatrix f (r • ofLp z)) *ᵥ (r • ofLp v)) i
    simp only [Matrix.mulVec,dotProduct,Fin.sum_univ_two,Pi.smul_apply,smul_eq_mul]
    field_simp [hr]
  rw [hm]
  exact h

theorem scaledGradientEuclidean_eq_components (f : (Fin 2 → ℝ) → ℝ)
    (r : ℝ) (z : EuclideanSpace ℝ (Fin 2)) :
    scaledGradientEuclidean f r z =
      toLp 2 ![fderiv ℝ f (r • ofLp z) ![1,0] / r^2,
        fderiv ℝ f (r • ofLp z) ![0,1] / r^2] := by
  rw [scaledGradientEuclidean,gradientEuclidean_eq_components]
  ext i
  fin_cases i <;> simp [div_eq_mul_inv,mul_comm]




theorem hessianEntry_eq_derivativeComponent (f : (Fin 2 → ℝ) → ℝ)
    (hf : ContDiff ℝ (⊤ : ℕ∞) f) (x u w : Fin 2 → ℝ) :
    iteratedFDeriv ℝ 2 f x ![u,w] =
      fderiv ℝ (fun y => fderiv ℝ f y w) x u := by
  have h := derivativeComponent_iteratedFDeriv f hf 1 x ![u] w
  have he : Fin.snoc (![u] : Fin 1 → (Fin 2 → ℝ)) w = ![u,w] := by
    ext i; fin_cases i <;> rfl
  simpa only [iteratedFDeriv_one_apply,he,Matrix.cons_val_zero] using h.symm

theorem hessianEntry_smooth (f : (Fin 2 → ℝ) → ℝ)
    (hf : ContDiff ℝ (⊤ : ℕ∞) f) (u w : Fin 2 → ℝ) :
    ContDiff ℝ (⊤ : ℕ∞) (fun x => iteratedFDeriv ℝ 2 f x ![u,w]) := by
  have he : (fun x => iteratedFDeriv ℝ 2 f x ![u,w]) =
      fun x => fderiv ℝ (fun y => fderiv ℝ f y w) x u :=
    funext (fun x => hessianEntry_eq_derivativeComponent f hf x u w)
  rw [he]
  exact derivativeComponent_smooth _ (derivativeComponent_smooth f hf w) u

theorem line_hessian_iteratedDeriv (f : (Fin 2 → ℝ) → ℝ)
    (hf : ContDiff ℝ (⊤ : ℕ∞) f) (k : ℕ) (v u w : Fin 2 → ℝ) (t : ℝ) :
    iteratedDeriv k (fun s => iteratedFDeriv ℝ 2 f (s • v) ![u,w]) t =
      iteratedFDeriv ℝ (k+2) f (t • v)
        (Fin.snoc (Fin.snoc (fun _ => v) u) w) := by
  have he : (fun s : ℝ => iteratedFDeriv ℝ 2 f (s • v) ![u,w]) =
      fun s : ℝ => fderiv ℝ (fun y => fderiv ℝ f y w) (s • v) u :=
    funext (fun s => hessianEntry_eq_derivativeComponent f hf (s • v) u w)
  rw [he,line_gradient_iteratedDeriv _ (derivativeComponent_smooth f hf w)]
  exact derivativeComponent_iteratedFDeriv f hf (k+1) _ _ w

theorem source_line_hessian_taylor {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L)
    (v u w : Fin 2 → ℝ) :
    |iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω) v ![u,w] -
      (iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω) 0 ![u,w] +
        iteratedFDeriv ℝ 3 (smoothSourceField 2 L ω) 0 ![v,u,w] +
        iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![v,v,u,w]/2)| ≤
      sourceDerivativeMajorant L 5 ω * ‖v‖^3 * ‖u‖*‖w‖/6 := by
  let f := smoothSourceField 2 L ω
  have hf : ContDiff ℝ (⊤ : ℕ∞) f := smoothSourceField_smooth 2 hL ω
  let g := fun s : ℝ => iteratedFDeriv ℝ 2 f (s • v) ![u,w]
  have hg : ContDiff ℝ (⊤ : ℕ∞) g :=
    (hessianEntry_smooth f hf u w).comp (lineMap v).contDiff
  have hbd (s : ℝ) : |iteratedDeriv 3 g s| ≤
      sourceDerivativeMajorant L 5 ω * ‖v‖^3*‖u‖*‖w‖ := by
    rw [show g=(fun s => iteratedFDeriv ℝ 2 f (s • v) ![u,w]) from rfl,
      line_hessian_iteratedDeriv f hf]
    have h := source_derivative_abs_le hL ω 5 (s • v)
      (Fin.snoc (Fin.snoc (fun _ : Fin 3 => v) u) w)
    have he : (fun i : Fin 5 => ‖(Fin.snoc (Fin.snoc (fun _ : Fin 3 => v) u) w :
        Fin 5 → (Fin 2 → ℝ)) i‖) =
        Fin.snoc (Fin.snoc (fun _ : Fin 3 => ‖v‖) ‖u‖) ‖w‖ := by
      ext i; fin_cases i <;> rfl
    rw [he,Fin.prod_snoc,Fin.prod_snoc] at h
    simpa only [Finset.prod_const,Finset.card_univ,Fintype.card_fin,mul_assoc] using h
  have h := scalar_taylor_two_bound g hg _ hbd 1
  have hd1 := line_hessian_iteratedDeriv f hf 1 v u w 0
  have hd2 := line_hessian_iteratedDeriv f hf 2 v u w 0
  have he1 : Fin.snoc (Fin.snoc (fun _ : Fin 1 => v) u) w = ![v,u,w] := by
    ext i; fin_cases i <;> rfl
  have he2 : Fin.snoc (Fin.snoc (fun _ : Fin 2 => v) u) w = ![v,v,u,w] := by
    ext i; fin_cases i <;> rfl
  simp only [iteratedDeriv_one,zero_smul,he1,he2] at hd1 hd2
  simp only [show g 1=iteratedFDeriv ℝ 2 f v ![u,w] by simp [g],
    show g 0=iteratedFDeriv ℝ 2 f 0 ![u,w] by simp [g],
    show deriv g 0=iteratedFDeriv ℝ 3 f 0 ![v,u,w] from hd1,
    show iteratedDeriv 2 g 0=iteratedFDeriv ℝ 4 f 0 ![v,v,u,w] from hd2,
    one_mul,one_pow,mul_one,abs_one] at h
  exact h




def quarticK0 : ℝ := 4096
def quarticEpsilonStar : ℝ := 1/(1024*4096*5^5)
def quarticKcap : ℝ := 25600010

def quarticFstar (r : ℝ) (U : Fin 8 → ℝ) : ℝ :=
  1+|U 0|/8+r*|U 4|/48

def quarticWidth (r : ℝ) (U : Fin 8 → ℝ) (R0 : ℝ) : ℝ :=
  quarticFstar r U / (quarticK0*R0^5)

theorem one_le_quarticFstar (r : ℝ) (hr : 0 ≤ r) (U : Fin 8 → ℝ) :
    1 ≤ quarticFstar r U := by
  unfold quarticFstar
  have h0 : 0 ≤ |U 0|/8 := div_nonneg (abs_nonneg _) (by norm_num)
  have h4 : 0 ≤ r*|U 4|/48 := div_nonneg (mul_nonneg hr (abs_nonneg _)) (by norm_num)
  linarith

theorem quarticWidth_pos (r R0 : ℝ) (hr : 0 ≤ r) (hR0 : 1 ≤ R0) (U : Fin 8 → ℝ) :
    0 < quarticWidth r U R0 := by
  unfold quarticWidth
  exact div_pos (lt_of_lt_of_le (by norm_num) (one_le_quarticFstar r hr U))
    (mul_pos (by norm_num [quarticK0]) (pow_pos (by linarith) 5))

/-- The actual cutoff also gives the exact LM001 raw-radius regularity budget. -/
theorem cutoff_raw_regularity (r R R0 : ℝ) (hr : 0 ≤ r) (hR0 : 1 ≤ R0)
    (hR0R : R0 ≤ 5*R) (hcut : r*R^5 ≤ quarticEpsilonStar) :
    r*R0^5 ≤ 1/(1024*quarticK0) := by
  have hpow : R0^5 ≤ (5*R)^5 := pow_le_pow_left₀ (by linarith) hR0R 5
  calc
    _ ≤ r*(5*R)^5 := mul_le_mul_of_nonneg_left hpow hr
    _ = 5^5*(r*R^5) := by ring
    _ ≤ 5^5*quarticEpsilonStar := mul_le_mul_of_nonneg_left hcut (by norm_num)
    _ = _ := by norm_num [quarticEpsilonStar,quarticK0]

/-- The same cutoff controls the fifth derivative through G≤R; no additional
fifth-derivative tail condition is needed for this arithmetic consequence. -/
theorem cutoff_scaled_error_budget (r R R0 G : ℝ)
    (hr : 0 ≤ r) (hr1 : r ≤ 1) (hR : 1 ≤ R) (hR0 : 1 ≤ R0)
    (hR0R : R0 ≤ 5*R) (hG0 : 0 ≤ G) (hGR : G ≤ R)
    (hcut : r*R^5 ≤ quarticEpsilonStar) :
    12*quarticK0*R0^4*r^2*G ≤ 1 := by
  have hK : 0 < quarticK0 := by norm_num [quarticK0]
  have hR00 : 0 ≤ R0 := by linarith
  have hRpos : 0 ≤ R := by linarith
  calc
    _ ≤ 12*quarticK0*(5*R)^4*r^2*R := by gcongr
    _ = (12*quarticK0*5^4*r)*(r*R^5) := by ring
    _ ≤ (12*quarticK0*5^4*r)*quarticEpsilonStar :=
      mul_le_mul_of_nonneg_left hcut (by positivity)
    _ ≤ (12*quarticK0*5^4)*quarticEpsilonStar := by
      apply mul_le_mul_of_nonneg_right _ (by norm_num [quarticEpsilonStar])
      nlinarith [hr1]
    _ ≤ 1 := by norm_num [quarticK0,quarticEpsilonStar]

/-- The radius cutoff implies the literal LM004 quarter-width tolerance for
any LM001 Fstar≥1, keeping every denominator strictly positive. -/
theorem cutoff_adaptive_tolerance (r R R0 G Fstar : ℝ)
    (hr : 0 ≤ r) (hr1 : r ≤ 1) (hR : 1 ≤ R) (hR0 : 1 ≤ R0)
    (hR0R : R0 ≤ 5*R) (hG0 : 0 ≤ G) (hGR : G ≤ R)
    (hFstar : 1 ≤ Fstar) (hcut : r*R^5 ≤ quarticEpsilonStar) :
    3*r^2*G ≤ R0*(Fstar/(quarticK0*R0^5))/4 := by
  have hbudget := cutoff_scaled_error_budget r R R0 G hr hr1 hR hR0 hR0R hG0 hGR hcut
  have hR00 : 0 ≤ R0 := by linarith
  have hden : 0 < quarticK0*R0^5 := by
    exact mul_pos (by norm_num [quarticK0]) (pow_pos (by linarith) 5)
  have hm : (3*r^2*G*4)*(quarticK0*R0^5) ≤ R0*Fstar := by
    calc
      _ = R0*(12*quarticK0*R0^4*r^2*G) := by ring
      _ ≤ R0*1 := mul_le_mul_of_nonneg_left hbudget hR00
      _ ≤ R0*Fstar := mul_le_mul_of_nonneg_left hFstar hR00
  calc
    _ ≤ ((R0*Fstar)/(quarticK0*R0^5))/4 :=
      (le_div_iff₀ (by norm_num : (0 : ℝ) < 4)).mpr ((le_div_iff₀ hden).mpr hm)
    _ = _ := by ring

theorem cutoff_quarticWidth_tolerance (r R R0 G : ℝ) (U : Fin 8 → ℝ)
    (hr : 0 ≤ r) (hr1 : r ≤ 1) (hR : 1 ≤ R) (hR0 : 1 ≤ R0)
    (hR0R : R0 ≤ 5*R) (hG0 : 0 ≤ G) (hGR : G ≤ R)
    (hcut : r*R^5 ≤ quarticEpsilonStar) :
    3*r^2*G ≤ R0*quarticWidth r U R0/4 :=
  cutoff_adaptive_tolerance r R R0 G (quarticFstar r U)
    hr hr1 hR hR0 hR0R hG0 hGR (one_le_quarticFstar r hr U) hcut

/-- The exact cutoff curvature constant implies the literal LM001 threshold. -/
theorem cutoff_curvature_threshold (q r R R0 : ℝ) (hr : 0 < r)
    (hR : 1 ≤ R) (hR0 : 1 ≤ R0) (hR0R : R0 ≤ 5*R)
    (hq : q ≤ -quarticKcap*r*R^5) :
    q/r ≤ -(2*quarticK0*R0^5+2*R0) := by
  have hR00 : 0 ≤ R0 := by linarith
  have hRpos : 0 ≤ R := by linarith
  have hR5 : R ≤ R^5 := by
    calc
      R = R^1 := by simp
      _ ≤ R^5 := pow_le_pow_right₀ hR (by norm_num)
  have hcap : 2*quarticK0*R0^5+2*R0 ≤ quarticKcap*R^5 := by
    calc
      _ ≤ 2*quarticK0*(5*R)^5+2*(5*R) := by
        have hK : 0 < quarticK0 := by norm_num [quarticK0]
        gcongr
      _ ≤ 2*quarticK0*5^5*R^5+10*R^5 := by
        have heq : 2*quarticK0*(5*R)^5+2*(5*R) = 2*quarticK0*5^5*R^5+10*R := by ring
        rw [heq]
        linarith [hR5]
      _ = _ := by norm_num [quarticK0,quarticKcap]; ring
  apply (div_le_iff₀ hr).mpr
  calc
    q ≤ -quarticKcap*r*R^5 := hq
    _ = -(quarticKcap*R^5)*r := by ring
    _ ≤ -(2*quarticK0*R0^5+2*R0)*r :=
      mul_le_mul_of_nonneg_right (neg_le_neg hcap) hr.le

/-- The certificate's size bound controls both its strip width and endpoint
radius. No capture or chart transport is asserted. -/
theorem certificate_width_geometry (R0 W : ℝ) (hR0 : 1 ≤ R0)
    (hsmall : R0*W ≤ 1/2048) :
    W ≤ 1/2048 ∧ 8*R0*W ≤ 1/256 := by
  constructor
  · by_cases hW : 0 ≤ W
    · have h := mul_le_mul_of_nonneg_right hR0 hW
      nlinarith [hsmall]
    · linarith
  · nlinarith [hsmall]




theorem source_origin_derivative_abs_le {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L)
    (k : ℕ) (u : Fin k → (Fin 2 → ℝ)) (hu : ∀ i, ‖u i‖ ≤ 1) :
    |iteratedFDeriv ℝ k (smoothSourceField 2 L ω) 0 u| ≤
      sourceDerivativeMajorant L k ω := by
  have h0 : (![0,0] : Fin 2 → ℝ) = 0 := by ext i; fin_cases i <;> rfl
  simpa only [h0] using source_axis_derivative_abs_le hL ω k u hu 0

theorem sourceRawU_abs_le {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) (i : Fin 8) :
    |sourceRawU L ω i| ≤ if (i : ℕ) < 3 then sourceDerivativeMajorant L 3 ω
      else sourceDerivativeMajorant L 4 ω := by
  fin_cases i
  · exact sourceA_abs_le hL ω
  all_goals
    apply source_origin_derivative_abs_le hL ω
    intro j
    fin_cases j <;> first | exact directionX_norm_le_one | exact directionY_norm_le_one

theorem sourceRawRadius_one_le (L : ℝ) (ω : SmoothSample 2 L) :
    1 ≤ sourceRawRadius L ω :=
  le_add_of_nonneg_right (Finset.sum_nonneg (fun _ _ => abs_nonneg _))

theorem sourceRawRadius_le_majorants {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) :
    sourceRawRadius L ω ≤ 1+3*sourceDerivativeMajorant L 3 ω+5*sourceDerivativeMajorant L 4 ω := by
  calc
    _ ≤ 1+∑ i : Fin 8, if (i : ℕ) < 3 then sourceDerivativeMajorant L 3 ω
        else sourceDerivativeMajorant L 4 ω :=
      by
        change 1+(∑ i : Fin 8, |sourceRawU L ω i|) ≤ _
        exact add_le_add le_rfl (Finset.sum_le_sum (fun i _ => sourceRawU_abs_le hL ω i))
    _ = _ := by norm_num [Fin.sum_univ_succ]; ring

theorem sourceRawRadius_le_global {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) :
    sourceRawRadius L ω ≤ 5*sourceGammaRadius L ω := by
  have h := sourceRawRadius_le_majorants hL ω
  have hg := sourceGammaRadius_ge_third_fourth L ω
  have h3 := sourceDerivativeMajorant_nonneg L 3 ω
  linarith

theorem sourcePhysicalPins_ae {L : ℝ} (hL : L ≠ 0) (r b : ℝ) (hr : r ≠ 0)
    (hG : IsUnit (sourcePinCovarianceAt L r)) :
    ∀ᵐ ω ∂sourceSmoothLaw hL r b, sourcePhysicalPins L r ω := by
  filter_upwards [sourceSmoothLaw_raw_pin_fiber_ae hL r b hr hG] with ω hω
  unfold sourcePhysicalPins
  rw [hω]
  simp
  ring

theorem sourcePhysicalPins_eventually {L : ℝ} (hL : L ≠ 0) (b : ℝ) :
    ∃ δ : ℝ, 0 < δ ∧ δ ≤ 1 ∧ ∀ r : ℝ, 0 < r → r < δ →
      ∀ᵐ ω ∂sourceSmoothLaw hL r b, sourcePhysicalPins L r ω := by
  obtain ⟨δ,hδ,hsub⟩ := mem_nhdsGT_iff_exists_Ioo_subset.mp
    (sourceEndpoint_parameter_limits hL b).1
  refine ⟨min δ 1,lt_min hδ (by norm_num),min_le_right _ _,?_⟩
  intro r hr hrδ
  exact sourcePhysicalPins_ae hL r b hr.ne'
    (hsub ⟨hr,lt_of_lt_of_le hrδ (min_le_left _ _)⟩)


def sourceGradientTaylorRaw (L r : ℝ) (ω : SmoothSample 2 L)
    (p : Fin 2 → ℝ) (i : Fin 2) : ℝ :=
  (fderiv ℝ (smoothSourceField 2 L ω) 0 (coordinateDirection i) +
    iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω) 0 ![r • p,coordinateDirection i] +
    iteratedFDeriv ℝ 3 (smoothSourceField 2 L ω) 0 ![r • p,r • p,coordinateDirection i]/2 +
    iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![r • p,r • p,r • p,coordinateDirection i]/6)/r^2

def sourceGradientTaylor (L r : ℝ) (ω : SmoothSample 2 L) (p : SourcePlane) : SourcePlane :=
  toLp 2 (sourceGradientTaylorRaw L r ω (ofLp p))

def sourceHessianTaylor (L r : ℝ) (ω : SmoothSample 2 L) (p : Fin 2 → ℝ) :
    Matrix (Fin 2) (Fin 2) ℝ :=
  fun i j => (iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω) 0
      ![coordinateDirection j,coordinateDirection i] +
    iteratedFDeriv ℝ 3 (smoothSourceField 2 L ω) 0
      ![r • p,coordinateDirection j,coordinateDirection i] +
    iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0
      ![r • p,r • p,coordinateDirection j,coordinateDirection i]/2)/r

theorem sourceScaledGradient_eq (L r : ℝ) (ω : SmoothSample 2 L) :
    sourceScaledGradient L r ω = scaledGradientEuclidean (smoothSourceField 2 L ω) r := by
  funext p
  rw [scaledGradientEuclidean_eq_components]
  rfl

theorem sourceScaledGradient_hasFDerivAt {L : ℝ} (hL : L ≠ 0) (r : ℝ) (hr : r ≠ 0)
    (ω : SmoothSample 2 L) (p : SourcePlane) :
    HasFDerivAt (sourceScaledGradient L r ω)
      (matrixLinearEuclidean (fun i j =>
        iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω) (r • ofLp p)
          ![coordinateDirection j,coordinateDirection i]/r)) p := by
  rw [sourceScaledGradient_eq]
  exact hasFDerivAt_scaledGradientEuclidean _ (smoothSourceField_smooth 2 hL ω) r hr p



private theorem plane_decompose (p : Fin 2 → ℝ) :
    p = p 0 • directionX + p 1 • directionY := by
  ext i
  fin_cases i <;> simp [directionX,directionY]

private theorem cml_head {n : ℕ}
    (T : ContinuousMultilinearMap ℝ (fun _ : Fin (n+1) => Fin 2 → ℝ) ℝ)
    (p : Fin 2 → ℝ) (v : Fin n → (Fin 2 → ℝ)) :
    T (Fin.cons p v) = p 0 * T (Fin.cons directionX v) +
      p 1 * T (Fin.cons directionY v) := by
  rw [← ContinuousMultilinearMap.curryLeft_apply,plane_decompose p,map_add,map_smul,map_smul]
  simp [ContinuousMultilinearMap.curryLeft_apply,smul_eq_mul,directionX,directionY]

private theorem cml_pp {n : ℕ}
    (T : ContinuousMultilinearMap ℝ (fun _ : Fin (n+2) => Fin 2 → ℝ) ℝ)
    (p : Fin 2 → ℝ) (v : Fin n → (Fin 2 → ℝ)) :
    T (Fin.cons p (Fin.cons p v)) =
      (p 0)^2 * T (Fin.cons directionX (Fin.cons directionX v)) +
      (p 0*p 1) * T (Fin.cons directionX (Fin.cons directionY v)) +
      (p 0*p 1) * T (Fin.cons directionY (Fin.cons directionX v)) +
      (p 1)^2 * T (Fin.cons directionY (Fin.cons directionY v)) := by
  rw [cml_head T p (Fin.cons p v)]
  have hx := cml_head (T.curryLeft directionX) p v
  have hy := cml_head (T.curryLeft directionY) p v
  simp only [ContinuousMultilinearMap.curryLeft_apply] at hx hy
  rw [hx,hy]
  ring

private theorem cml_ppp {n : ℕ}
    (T : ContinuousMultilinearMap ℝ (fun _ : Fin (n+3) => Fin 2 → ℝ) ℝ)
    (p : Fin 2 → ℝ) (v : Fin n → (Fin 2 → ℝ)) :
    T (Fin.cons p (Fin.cons p (Fin.cons p v))) =
      (p 0)^3 * T (Fin.cons directionX (Fin.cons directionX (Fin.cons directionX v))) +
      (p 0)^2*p 1 * T (Fin.cons directionX (Fin.cons directionX (Fin.cons directionY v))) +
      (p 0)^2*p 1 * T (Fin.cons directionX (Fin.cons directionY (Fin.cons directionX v))) +
      p 0*(p 1)^2 * T (Fin.cons directionX (Fin.cons directionY (Fin.cons directionY v))) +
      (p 0)^2*p 1 * T (Fin.cons directionY (Fin.cons directionX (Fin.cons directionX v))) +
      p 0*(p 1)^2 * T (Fin.cons directionY (Fin.cons directionX (Fin.cons directionY v))) +
      p 0*(p 1)^2 * T (Fin.cons directionY (Fin.cons directionY (Fin.cons directionX v))) +
      (p 1)^3 * T (Fin.cons directionY (Fin.cons directionY (Fin.cons directionY v))) := by
  rw [cml_head T p (Fin.cons p (Fin.cons p v))]
  have hx := cml_pp (T.curryLeft directionX) p v
  have hy := cml_pp (T.curryLeft directionY) p v
  simp only [ContinuousMultilinearMap.curryLeft_apply] at hx hy
  rw [hx,hy]
  ring

private theorem source_word_2_xx {L : ℝ} (_hL : L ≠ 0) (ω : SmoothSample 2 L) :
    iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω) 0 ![directionX,directionX] = iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω) 0 ![directionX,directionX] := by
  rfl

private theorem source_word_2_xy {L : ℝ} (_hL : L ≠ 0) (ω : SmoothSample 2 L) :
    iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω) 0 ![directionX,directionY] = iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω) 0 ![directionX,directionY] := by
  rfl

private theorem source_word_2_yx {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) :
    iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω) 0 ![directionY,directionX] = iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω) 0 ![directionX,directionY] := by
  let σ : Equiv.Perm (Fin 2) := Equiv.ofBijective (fun i => ![1,0] i) (by decide)
  have hw : (![directionX,directionY] ∘ σ) = ![directionY,directionX] := by
    ext i; fin_cases i <;> rfl
  simpa only [hw] using source_derivative_comp_perm hL ω 2 0 ![directionX,directionY] σ

private theorem source_word_2_yy {L : ℝ} (_hL : L ≠ 0) (ω : SmoothSample 2 L) :
    iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω) 0 ![directionY,directionY] = sourceQ L ω := by
  rfl

private theorem source_word_3_xxx {L : ℝ} (_hL : L ≠ 0) (ω : SmoothSample 2 L) :
    iteratedFDeriv ℝ 3 (smoothSourceField 2 L ω) 0 ![directionX,directionX,directionX] = sourceAxialThird L ω := by
  rfl

private theorem source_word_3_xxy {L : ℝ} (_hL : L ≠ 0) (ω : SmoothSample 2 L) :
    iteratedFDeriv ℝ 3 (smoothSourceField 2 L ω) 0 ![directionX,directionX,directionY] = sourceRawU L ω 0 := by
  rfl

private theorem source_word_3_xyx {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) :
    iteratedFDeriv ℝ 3 (smoothSourceField 2 L ω) 0 ![directionX,directionY,directionX] = sourceRawU L ω 0 := by
  change iteratedFDeriv ℝ 3 (smoothSourceField 2 L ω) 0 ![directionX,directionY,directionX] = iteratedFDeriv ℝ 3 (smoothSourceField 2 L ω) 0 ![directionX,directionX,directionY]
  let σ : Equiv.Perm (Fin 3) := Equiv.ofBijective (fun i => ![0,2,1] i) (by decide)
  have hw : (![directionX,directionX,directionY] ∘ σ) = ![directionX,directionY,directionX] := by
    ext i; fin_cases i <;> rfl
  simpa only [hw] using source_derivative_comp_perm hL ω 3 0 ![directionX,directionX,directionY] σ

private theorem source_word_3_xyy {L : ℝ} (_hL : L ≠ 0) (ω : SmoothSample 2 L) :
    iteratedFDeriv ℝ 3 (smoothSourceField 2 L ω) 0 ![directionX,directionY,directionY] = sourceRawU L ω 1 := by
  rfl

private theorem source_word_3_yxx {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) :
    iteratedFDeriv ℝ 3 (smoothSourceField 2 L ω) 0 ![directionY,directionX,directionX] = sourceRawU L ω 0 := by
  change iteratedFDeriv ℝ 3 (smoothSourceField 2 L ω) 0 ![directionY,directionX,directionX] = iteratedFDeriv ℝ 3 (smoothSourceField 2 L ω) 0 ![directionX,directionX,directionY]
  let σ : Equiv.Perm (Fin 3) := Equiv.ofBijective (fun i => ![2,0,1] i) (by decide)
  have hw : (![directionX,directionX,directionY] ∘ σ) = ![directionY,directionX,directionX] := by
    ext i; fin_cases i <;> rfl
  simpa only [hw] using source_derivative_comp_perm hL ω 3 0 ![directionX,directionX,directionY] σ

private theorem source_word_3_yxy {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) :
    iteratedFDeriv ℝ 3 (smoothSourceField 2 L ω) 0 ![directionY,directionX,directionY] = sourceRawU L ω 1 := by
  change iteratedFDeriv ℝ 3 (smoothSourceField 2 L ω) 0 ![directionY,directionX,directionY] = iteratedFDeriv ℝ 3 (smoothSourceField 2 L ω) 0 ![directionX,directionY,directionY]
  let σ : Equiv.Perm (Fin 3) := Equiv.ofBijective (fun i => ![1,0,2] i) (by decide)
  have hw : (![directionX,directionY,directionY] ∘ σ) = ![directionY,directionX,directionY] := by
    ext i; fin_cases i <;> rfl
  simpa only [hw] using source_derivative_comp_perm hL ω 3 0 ![directionX,directionY,directionY] σ

private theorem source_word_3_yyx {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) :
    iteratedFDeriv ℝ 3 (smoothSourceField 2 L ω) 0 ![directionY,directionY,directionX] = sourceRawU L ω 1 := by
  change iteratedFDeriv ℝ 3 (smoothSourceField 2 L ω) 0 ![directionY,directionY,directionX] = iteratedFDeriv ℝ 3 (smoothSourceField 2 L ω) 0 ![directionX,directionY,directionY]
  let σ : Equiv.Perm (Fin 3) := Equiv.ofBijective (fun i => ![1,2,0] i) (by decide)
  have hw : (![directionX,directionY,directionY] ∘ σ) = ![directionY,directionY,directionX] := by
    ext i; fin_cases i <;> rfl
  simpa only [hw] using source_derivative_comp_perm hL ω 3 0 ![directionX,directionY,directionY] σ

private theorem source_word_3_yyy {L : ℝ} (_hL : L ≠ 0) (ω : SmoothSample 2 L) :
    iteratedFDeriv ℝ 3 (smoothSourceField 2 L ω) 0 ![directionY,directionY,directionY] = sourceRawU L ω 2 := by
  rfl

private theorem source_word_4_xxxx {L : ℝ} (_hL : L ≠ 0) (ω : SmoothSample 2 L) :
    iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![directionX,directionX,directionX,directionX] = sourceRawU L ω 3 := by
  rfl

private theorem source_word_4_xxxy {L : ℝ} (_hL : L ≠ 0) (ω : SmoothSample 2 L) :
    iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![directionX,directionX,directionX,directionY] = sourceRawU L ω 4 := by
  rfl

private theorem source_word_4_xxyx {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) :
    iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![directionX,directionX,directionY,directionX] = sourceRawU L ω 4 := by
  change iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![directionX,directionX,directionY,directionX] = iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![directionX,directionX,directionX,directionY]
  let σ : Equiv.Perm (Fin 4) := Equiv.ofBijective (fun i => ![0,1,3,2] i) (by decide)
  have hw : (![directionX,directionX,directionX,directionY] ∘ σ) = ![directionX,directionX,directionY,directionX] := by
    ext i; fin_cases i <;> rfl
  simpa only [hw] using source_derivative_comp_perm hL ω 4 0 ![directionX,directionX,directionX,directionY] σ

private theorem source_word_4_xxyy {L : ℝ} (_hL : L ≠ 0) (ω : SmoothSample 2 L) :
    iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![directionX,directionX,directionY,directionY] = sourceRawU L ω 5 := by
  rfl

private theorem source_word_4_xyxx {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) :
    iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![directionX,directionY,directionX,directionX] = sourceRawU L ω 4 := by
  change iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![directionX,directionY,directionX,directionX] = iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![directionX,directionX,directionX,directionY]
  let σ : Equiv.Perm (Fin 4) := Equiv.ofBijective (fun i => ![0,3,1,2] i) (by decide)
  have hw : (![directionX,directionX,directionX,directionY] ∘ σ) = ![directionX,directionY,directionX,directionX] := by
    ext i; fin_cases i <;> rfl
  simpa only [hw] using source_derivative_comp_perm hL ω 4 0 ![directionX,directionX,directionX,directionY] σ

private theorem source_word_4_xyxy {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) :
    iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![directionX,directionY,directionX,directionY] = sourceRawU L ω 5 := by
  change iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![directionX,directionY,directionX,directionY] = iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![directionX,directionX,directionY,directionY]
  let σ : Equiv.Perm (Fin 4) := Equiv.ofBijective (fun i => ![0,2,1,3] i) (by decide)
  have hw : (![directionX,directionX,directionY,directionY] ∘ σ) = ![directionX,directionY,directionX,directionY] := by
    ext i; fin_cases i <;> rfl
  simpa only [hw] using source_derivative_comp_perm hL ω 4 0 ![directionX,directionX,directionY,directionY] σ

private theorem source_word_4_xyyx {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) :
    iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![directionX,directionY,directionY,directionX] = sourceRawU L ω 5 := by
  change iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![directionX,directionY,directionY,directionX] = iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![directionX,directionX,directionY,directionY]
  let σ : Equiv.Perm (Fin 4) := Equiv.ofBijective (fun i => ![0,2,3,1] i) (by decide)
  have hw : (![directionX,directionX,directionY,directionY] ∘ σ) = ![directionX,directionY,directionY,directionX] := by
    ext i; fin_cases i <;> rfl
  simpa only [hw] using source_derivative_comp_perm hL ω 4 0 ![directionX,directionX,directionY,directionY] σ

private theorem source_word_4_xyyy {L : ℝ} (_hL : L ≠ 0) (ω : SmoothSample 2 L) :
    iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![directionX,directionY,directionY,directionY] = sourceRawU L ω 6 := by
  rfl

private theorem source_word_4_yxxx {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) :
    iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![directionY,directionX,directionX,directionX] = sourceRawU L ω 4 := by
  change iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![directionY,directionX,directionX,directionX] = iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![directionX,directionX,directionX,directionY]
  let σ : Equiv.Perm (Fin 4) := Equiv.ofBijective (fun i => ![3,0,1,2] i) (by decide)
  have hw : (![directionX,directionX,directionX,directionY] ∘ σ) = ![directionY,directionX,directionX,directionX] := by
    ext i; fin_cases i <;> rfl
  simpa only [hw] using source_derivative_comp_perm hL ω 4 0 ![directionX,directionX,directionX,directionY] σ

private theorem source_word_4_yxxy {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) :
    iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![directionY,directionX,directionX,directionY] = sourceRawU L ω 5 := by
  change iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![directionY,directionX,directionX,directionY] = iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![directionX,directionX,directionY,directionY]
  let σ : Equiv.Perm (Fin 4) := Equiv.ofBijective (fun i => ![2,0,1,3] i) (by decide)
  have hw : (![directionX,directionX,directionY,directionY] ∘ σ) = ![directionY,directionX,directionX,directionY] := by
    ext i; fin_cases i <;> rfl
  simpa only [hw] using source_derivative_comp_perm hL ω 4 0 ![directionX,directionX,directionY,directionY] σ

private theorem source_word_4_yxyx {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) :
    iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![directionY,directionX,directionY,directionX] = sourceRawU L ω 5 := by
  change iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![directionY,directionX,directionY,directionX] = iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![directionX,directionX,directionY,directionY]
  let σ : Equiv.Perm (Fin 4) := Equiv.ofBijective (fun i => ![2,0,3,1] i) (by decide)
  have hw : (![directionX,directionX,directionY,directionY] ∘ σ) = ![directionY,directionX,directionY,directionX] := by
    ext i; fin_cases i <;> rfl
  simpa only [hw] using source_derivative_comp_perm hL ω 4 0 ![directionX,directionX,directionY,directionY] σ

private theorem source_word_4_yxyy {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) :
    iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![directionY,directionX,directionY,directionY] = sourceRawU L ω 6 := by
  change iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![directionY,directionX,directionY,directionY] = iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![directionX,directionY,directionY,directionY]
  let σ : Equiv.Perm (Fin 4) := Equiv.ofBijective (fun i => ![1,0,2,3] i) (by decide)
  have hw : (![directionX,directionY,directionY,directionY] ∘ σ) = ![directionY,directionX,directionY,directionY] := by
    ext i; fin_cases i <;> rfl
  simpa only [hw] using source_derivative_comp_perm hL ω 4 0 ![directionX,directionY,directionY,directionY] σ

private theorem source_word_4_yyxx {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) :
    iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![directionY,directionY,directionX,directionX] = sourceRawU L ω 5 := by
  change iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![directionY,directionY,directionX,directionX] = iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![directionX,directionX,directionY,directionY]
  let σ : Equiv.Perm (Fin 4) := Equiv.ofBijective (fun i => ![2,3,0,1] i) (by decide)
  have hw : (![directionX,directionX,directionY,directionY] ∘ σ) = ![directionY,directionY,directionX,directionX] := by
    ext i; fin_cases i <;> rfl
  simpa only [hw] using source_derivative_comp_perm hL ω 4 0 ![directionX,directionX,directionY,directionY] σ

private theorem source_word_4_yyxy {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) :
    iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![directionY,directionY,directionX,directionY] = sourceRawU L ω 6 := by
  change iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![directionY,directionY,directionX,directionY] = iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![directionX,directionY,directionY,directionY]
  let σ : Equiv.Perm (Fin 4) := Equiv.ofBijective (fun i => ![1,2,0,3] i) (by decide)
  have hw : (![directionX,directionY,directionY,directionY] ∘ σ) = ![directionY,directionY,directionX,directionY] := by
    ext i; fin_cases i <;> rfl
  simpa only [hw] using source_derivative_comp_perm hL ω 4 0 ![directionX,directionY,directionY,directionY] σ

private theorem source_word_4_yyyx {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) :
    iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![directionY,directionY,directionY,directionX] = sourceRawU L ω 6 := by
  change iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![directionY,directionY,directionY,directionX] = iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![directionX,directionY,directionY,directionY]
  let σ : Equiv.Perm (Fin 4) := Equiv.ofBijective (fun i => ![1,2,3,0] i) (by decide)
  have hw : (![directionX,directionY,directionY,directionY] ∘ σ) = ![directionY,directionY,directionY,directionX] := by
    ext i; fin_cases i <;> rfl
  simpa only [hw] using source_derivative_comp_perm hL ω 4 0 ![directionX,directionY,directionY,directionY] σ

private theorem source_word_4_yyyy {L : ℝ} (_hL : L ≠ 0) (ω : SmoothSample 2 L) :
    iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![directionY,directionY,directionY,directionY] = sourceRawU L ω 7 := by
  rfl


theorem source_third_ppx_expansion {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) (p : Fin 2 → ℝ) :
    iteratedFDeriv ℝ 3 (smoothSourceField 2 L ω) 0 ![p,p,directionX] =
      sourceAxialThird L ω * (p 0)^2 + 2*sourceRawU L ω 0*p 0*p 1 + sourceRawU L ω 1*(p 1)^2 := by
  have h := cml_pp (iteratedFDeriv ℝ 3 (smoothSourceField 2 L ω) 0) p ![directionX]
  simp only [Matrix.Fin.cons_vecCons] at h
  rw [h]
  simp only [source_word_3_xxx hL ω, source_word_3_xyx hL ω, source_word_3_yxx hL ω, source_word_3_yyx hL ω]
  ring

theorem source_third_ppy_expansion {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) (p : Fin 2 → ℝ) :
    iteratedFDeriv ℝ 3 (smoothSourceField 2 L ω) 0 ![p,p,directionY] =
      sourceRawU L ω 0*(p 0)^2 + 2*sourceRawU L ω 1*p 0*p 1 + sourceRawU L ω 2*(p 1)^2 := by
  have h := cml_pp (iteratedFDeriv ℝ 3 (smoothSourceField 2 L ω) 0) p ![directionY]
  simp only [Matrix.Fin.cons_vecCons] at h
  rw [h]
  simp only [source_word_3_xxy hL ω, source_word_3_xyy hL ω, source_word_3_yxy hL ω, source_word_3_yyy hL ω]
  ring

theorem source_fourth_pppx_expansion {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) (p : Fin 2 → ℝ) :
    iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![p,p,p,directionX] =
      sourceRawU L ω 3*(p 0)^3 + 3*sourceRawU L ω 4*(p 0)^2*p 1 + 3*sourceRawU L ω 5*p 0*(p 1)^2 + sourceRawU L ω 6*(p 1)^3 := by
  have h := cml_ppp (iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0) p ![directionX]
  simp only [Matrix.Fin.cons_vecCons] at h
  rw [h]
  simp only [source_word_4_xxxx hL ω, source_word_4_xxyx hL ω, source_word_4_xyxx hL ω, source_word_4_xyyx hL ω, source_word_4_yxxx hL ω, source_word_4_yxyx hL ω, source_word_4_yyxx hL ω, source_word_4_yyyx hL ω]
  ring

theorem source_fourth_pppy_expansion {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) (p : Fin 2 → ℝ) :
    iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![p,p,p,directionY] =
      sourceRawU L ω 4*(p 0)^3 + 3*sourceRawU L ω 5*(p 0)^2*p 1 + 3*sourceRawU L ω 6*p 0*(p 1)^2 + sourceRawU L ω 7*(p 1)^3 := by
  have h := cml_ppp (iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0) p ![directionY]
  simp only [Matrix.Fin.cons_vecCons] at h
  rw [h]
  simp only [source_word_4_xxxy hL ω, source_word_4_xxyy hL ω, source_word_4_xyxy hL ω, source_word_4_xyyy hL ω, source_word_4_yxxy hL ω, source_word_4_yxyy hL ω, source_word_4_yyxy hL ω, source_word_4_yyyy hL ω]
  ring

theorem source_second_p_basis {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L)
    (p : Fin 2 → ℝ) (i : Fin 2) :
    iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω) 0 ![p,![directionX,directionY] i] =
      ![iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω) 0 ![directionX,directionX]*p 0 +
          iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω) 0 ![directionX,directionY]*p 1,
        iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω) 0 ![directionX,directionY]*p 0 +
          sourceQ L ω*p 1] i := by
  have h := cml_head (iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω) 0) p ![![directionX,directionY] i]
  simp only [Matrix.Fin.cons_vecCons] at h
  rw [h]
  fin_cases i <;> simp only [Matrix.cons_val_zero,Matrix.cons_val_one,Fin.reduceFinMk,
    source_word_2_yx hL ω,source_word_2_yy hL ω] <;> ring

theorem source_third_p_basis_basis {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L)
    (p : Fin 2 → ℝ) (i j : Fin 2) :
    iteratedFDeriv ℝ 3 (smoothSourceField 2 L ω) 0
        ![p,![directionX,directionY] i,![directionX,directionY] j] =
      !![sourceAxialThird L ω*p 0+sourceRawU L ω 0*p 1,
          sourceRawU L ω 0*p 0+sourceRawU L ω 1*p 1;
          sourceRawU L ω 0*p 0+sourceRawU L ω 1*p 1,
          sourceRawU L ω 1*p 0+sourceRawU L ω 2*p 1] i j := by
  have h := cml_head (iteratedFDeriv ℝ 3 (smoothSourceField 2 L ω) 0) p
    ![![directionX,directionY] i,![directionX,directionY] j]
  simp only [Matrix.Fin.cons_vecCons] at h
  rw [h]
  fin_cases i <;> fin_cases j <;>
    simp only [Matrix.cons_val_zero,Matrix.cons_val_one,Matrix.of_apply,Fin.reduceFinMk,
      source_word_3_xxx hL ω, source_word_3_xxy hL ω, source_word_3_xyx hL ω, source_word_3_xyy hL ω, source_word_3_yxx hL ω, source_word_3_yxy hL ω, source_word_3_yyx hL ω, source_word_3_yyy hL ω] <;> ring

theorem source_fourth_pp_basis_basis {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L)
    (p : Fin 2 → ℝ) (i j : Fin 2) :
    iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0
        ![p,p,![directionX,directionY] i,![directionX,directionY] j] =
      !![sourceRawU L ω 3*(p 0)^2+2*sourceRawU L ω 4*p 0*p 1+sourceRawU L ω 5*(p 1)^2,
          sourceRawU L ω 4*(p 0)^2+2*sourceRawU L ω 5*p 0*p 1+sourceRawU L ω 6*(p 1)^2;
          sourceRawU L ω 4*(p 0)^2+2*sourceRawU L ω 5*p 0*p 1+sourceRawU L ω 6*(p 1)^2,
          sourceRawU L ω 5*(p 0)^2+2*sourceRawU L ω 6*p 0*p 1+sourceRawU L ω 7*(p 1)^2] i j := by
  have h := cml_pp (iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0) p
    ![![directionX,directionY] i,![directionX,directionY] j]
  simp only [Matrix.Fin.cons_vecCons] at h
  rw [h]
  fin_cases i <;> fin_cases j <;>
    simp only [Matrix.cons_val_zero,Matrix.cons_val_one,Matrix.of_apply,Fin.reduceFinMk,
      source_word_4_xxxx hL ω, source_word_4_xxxy hL ω, source_word_4_xxyx hL ω, source_word_4_xxyy hL ω, source_word_4_xyxx hL ω, source_word_4_xyxy hL ω, source_word_4_xyyx hL ω, source_word_4_xyyy hL ω, source_word_4_yxxx hL ω, source_word_4_yxxy hL ω, source_word_4_yxyx hL ω, source_word_4_yxyy hL ω, source_word_4_yyxx hL ω, source_word_4_yyxy hL ω, source_word_4_yyyx hL ω, source_word_4_yyyy hL ω] <;> ring


def pinPreservingJacobian (r q : ℝ) (U : Fin 8 → ℝ) (p : Fin 2 → ℝ) :
    Matrix (Fin 2) (Fin 2) ℝ :=
  let X := p 0
  let Y := p 1
  let A := 2*X+U 0*Y+r*((U 3/6)*(3*X^2-1/4)+U 4*X*Y+(U 5/2)*Y^2)
  let B := U 0*X+U 1*Y+r*((U 4/6)*(3*X^2-1/4)+U 5*X*Y+(U 6/2)*Y^2)
  let C := q/r+U 1*X+U 2*Y+r*((U 5/2)*X^2+U 6*X*Y+(U 7/2)*Y^2)
  !![A,B;B,C]



-- Uses the actual production Jacobian definition from stage07.

theorem hasFDerivAt_pinPreservingQuartic (r q : ℝ) (U : Fin 8 → ℝ)
    (z : EuclideanSpace ℝ (Fin 2)) :
    HasFDerivAt (fun z : EuclideanSpace ℝ (Fin 2) => toLp 2 (pinPreservingQuartic r q U (ofLp z)))
      (matrixLinearEuclidean (pinPreservingJacobian r q U (ofLp z))) z := by
  let X : EuclideanSpace ℝ (Fin 2) →L[ℝ] ℝ := EuclideanSpace.proj (𝕜 := ℝ) 0
  let Y : EuclideanSpace ℝ (Fin 2) →L[ℝ] ℝ := EuclideanSpace.proj (𝕜 := ℝ) 1
  let M := matrixLinearEuclidean (pinPreservingJacobian r q U (ofLp z))
  have hX := X.hasFDerivAt (x := z)
  have hY := Y.hasFDerivAt (x := z)
  have h0 := (((((hX.pow 2).sub_const (1/4 : ℝ)).add
      ((hX.const_mul (U 0)).mul hY)).add ((hY.pow 2).const_mul (U 1/2))).add
      ((((((hX.const_mul (U 3/6)).mul ((hX.pow 2).sub_const (1/4 : ℝ))).add
        ((((hX.pow 2).const_mul 3).sub_const (1/4 : ℝ)).const_mul (U 4/6) |>.mul hY)).add
        ((hX.const_mul (U 5/2)).mul (hY.pow 2))).add
        ((hY.pow 3).const_mul (U 6/6))).const_mul r))
  have h1 := (((((hY.const_mul (q/r)).add
      (((hX.pow 2).sub_const (1/4 : ℝ)).const_mul (U 0/2))).add
      ((hX.const_mul (U 1)).mul hY)).add ((hY.pow 2).const_mul (U 2/2))).add
      ((((((hX.const_mul (U 4/6)).mul ((hX.pow 2).sub_const (1/4 : ℝ))).add
        (((hX.pow 2).const_mul (U 5/2)).mul hY)).add
        ((hX.const_mul (U 6/2)).mul (hY.pow 2))).add
        ((hY.pow 3).const_mul (U 7/6))).const_mul r))
  have hp0 : HasFDerivAt (fun z : EuclideanSpace ℝ (Fin 2) =>
      pinPreservingQuartic r q U (ofLp z) 0) (X.comp M) z := by
    apply h0.congr_fderiv
    ext v
    simp [X,Y,M,pinPreservingJacobian,matrixLinearEuclidean,
      Matrix.mulVec,dotProduct,Fin.sum_univ_two]
    ring
  have hp1 : HasFDerivAt (fun z : EuclideanSpace ℝ (Fin 2) =>
      pinPreservingQuartic r q U (ofLp z) 1) (Y.comp M) z := by
    apply h1.congr_fderiv
    ext v
    simp [X,Y,M,pinPreservingJacobian,matrixLinearEuclidean,
      Matrix.mulVec,dotProduct,Fin.sum_univ_two]
    ring
  have hraw : HasFDerivAt (fun z : EuclideanSpace ℝ (Fin 2) =>
      pinPreservingQuartic r q U (ofLp z))
      (ContinuousLinearMap.pi (fun i : Fin 2 => (EuclideanSpace.proj (𝕜 := ℝ) i).comp M)) z := by
    apply hasFDerivAt_pi.mpr
    intro i
    fin_cases i
    · exact hp0
    · exact hp1
  have hE := piToEuclidean.hasFDerivAt.comp z hraw
  have hmap : M = piToEuclidean.comp (ContinuousLinearMap.pi
      (fun i : Fin 2 => (EuclideanSpace.proj (𝕜 := ℝ) i).comp M)) := by
    ext v i
    rfl
  change HasFDerivAt _ M z
  rw [hmap]
  exact hE

theorem fderiv_pinPreservingQuartic (r q : ℝ) (U : Fin 8 → ℝ)
    (z : EuclideanSpace ℝ (Fin 2)) :
    fderiv ℝ (fun z : EuclideanSpace ℝ (Fin 2) => toLp 2 (pinPreservingQuartic r q U (ofLp z))) z =
      matrixLinearEuclidean (pinPreservingJacobian r q U (ofLp z)) :=
  (hasFDerivAt_pinPreservingQuartic r q U z).fderiv




theorem sourceGradientTaylorRaw_sub_quartic_zero {L : ℝ} (hL : L ≠ 0)
    (r : ℝ) (hr : r ≠ 0) (ω : SmoothSample 2 L) (p : Fin 2 → ℝ) :
    sourceGradientTaylorRaw L r ω p 0 -
      pinPreservingQuartic r (sourceQ L ω) (sourceRawU L ω) p 0 =
      (fderiv ℝ (smoothSourceField 2 L ω) 0 directionX+r^2/4)/r^2 +
      (iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω) 0 ![directionX,directionX]+
        sourceRawU L ω 3*r^2/24)/r*p 0 +
      (iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω) 0 ![directionX,directionY]+
        sourceRawU L ω 4*r^2/24)/r*p 1 +
      (sourceAxialThird L ω-2)*(p 0)^2/2 := by
  have h2 := source_second_p_basis hL ω (r • p) 0
  simp only [Matrix.cons_val_zero] at h2
  unfold sourceGradientTaylorRaw
  rw [coordinateDirection_zero]
  change (fderiv ℝ (smoothSourceField 2 L ω) 0 directionX +
    iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω) 0 ![r • p,directionX] +
    iteratedFDeriv ℝ 3 (smoothSourceField 2 L ω) 0 ![r • p,r • p,directionX]/2 +
    iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![r • p,r • p,r • p,directionX]/6)/r^2 - _ = _
  rw [h2,source_third_ppx_expansion hL ω,source_fourth_pppx_expansion hL ω]
  simp only [Pi.smul_apply,smul_eq_mul,pinPreservingQuartic,Matrix.cons_val_zero]
  field_simp [hr]
  ring

theorem sourceGradientTaylorRaw_sub_quartic_one {L : ℝ} (hL : L ≠ 0)
    (r : ℝ) (hr : r ≠ 0) (ω : SmoothSample 2 L) (p : Fin 2 → ℝ) :
    sourceGradientTaylorRaw L r ω p 1 -
      pinPreservingQuartic r (sourceQ L ω) (sourceRawU L ω) p 1 =
      (fderiv ℝ (smoothSourceField 2 L ω) 0 directionY+sourceRawU L ω 0*r^2/8)/r^2 +
      (iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω) 0 ![directionX,directionY]+
        sourceRawU L ω 4*r^2/24)/r*p 0 := by
  have h2 := source_second_p_basis hL ω (r • p) 1
  simp only [Matrix.cons_val_one,Matrix.cons_val_zero] at h2
  unfold sourceGradientTaylorRaw
  rw [coordinateDirection_one]
  change (fderiv ℝ (smoothSourceField 2 L ω) 0 directionY +
    iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω) 0 ![r • p,directionY] +
    iteratedFDeriv ℝ 3 (smoothSourceField 2 L ω) 0 ![r • p,r • p,directionY]/2 +
    iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![r • p,r • p,r • p,directionY]/6)/r^2 - _ = _
  rw [h2,source_third_ppy_expansion hL ω,source_fourth_pppy_expansion hL ω]
  simp only [Pi.smul_apply,smul_eq_mul,pinPreservingQuartic,Matrix.cons_val_one,Matrix.cons_val_zero]
  field_simp [hr]
  ring

private theorem source_second_transpose {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) :
    iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω) 0 ![directionY,directionX] =
      iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω) 0 ![directionX,directionY] := by
  have hw : (![directionX,directionY] ∘ Equiv.swap (0 : Fin 2) 1) =
      ![directionY,directionX] := by ext i; fin_cases i <;> rfl
  simpa only [hw] using source_derivative_comp_perm hL ω 2 0
    ![directionX,directionY] (Equiv.swap 0 1)

private theorem coordinateDirection_eq_array (i : Fin 2) :
    coordinateDirection i = ![directionX,directionY] i := by
  fin_cases i <;> simp [directionX,directionY]

theorem sourceHessianTaylor_sub_quarticJacobian {L : ℝ} (hL : L ≠ 0)
    (r : ℝ) (hr : r ≠ 0) (ω : SmoothSample 2 L) (p : Fin 2 → ℝ) :
    sourceHessianTaylor L r ω p -
      pinPreservingJacobian r (sourceQ L ω) (sourceRawU L ω) p =
      !![(iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω) 0 ![directionX,directionX]+
            sourceRawU L ω 3*r^2/24)/r + (sourceAxialThird L ω-2)*p 0,
          (iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω) 0 ![directionX,directionY]+
            sourceRawU L ω 4*r^2/24)/r;
          (iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω) 0 ![directionX,directionY]+
            sourceRawU L ω 4*r^2/24)/r,0] := by
  ext i j
  simp only [Matrix.sub_apply,sourceHessianTaylor,coordinateDirection_eq_array,
    source_third_p_basis_basis hL ω,source_fourth_pp_basis_basis hL ω]
  fin_cases i <;> fin_cases j <;>
    simp only [pinPreservingJacobian,Matrix.of_apply,Matrix.cons_val_zero,Matrix.cons_val_one,
      Fin.reduceFinMk,Pi.smul_apply,smul_eq_mul,source_second_transpose hL ω,sourceQ] <;>
    field_simp [hr] <;> ring




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




def sourceScaledPotential (L r : ℝ) (ω : SmoothSample 2 L) (p : SourcePlane) : ℝ :=
  smoothSourceField 2 L ω (r • ofLp p)/r^3

theorem sourceScaledPotential_hasGradientAt {L : ℝ} (hL : L ≠ 0) (r : ℝ) (hr : r ≠ 0)
    (ω : SmoothSample 2 L) (p : SourcePlane) :
    HasGradientAt (sourceScaledPotential L r ω) (sourceScaledGradient L r ω p) p := by
  let f := smoothSourceField 2 L ω
  have hf : Differentiable ℝ f := (smoothSourceField_smooth 2 hL ω).differentiable (by simp)
  have hc : HasFDerivAt (fun z : SourcePlane => r • ofLp z) (r • euclideanToPi) p :=
    (r • euclideanToPi).hasFDerivAt
  have h := ((hf (r • ofLp p)).hasFDerivAt.comp p hc).const_mul ((r^3)⁻¹)
  have hm : toDual ℝ SourcePlane (sourceScaledGradient L r ω p) =
      (r^3)⁻¹ • ((fderiv ℝ f (r • ofLp p)).comp (r • euclideanToPi)) := by
    ext v
    change inner ℝ (sourceScaledGradient L r ω p) v =
      (r^3)⁻¹ * fderiv ℝ f (r • ofLp p) (r • ofLp v)
    rw [map_smul,coordinate_decomposition (ofLp v),map_add,map_smul,map_smul]
    simp [sourceScaledGradient,sourceScaledGradientRaw,PiLp.inner_apply,Fin.sum_univ_two,
      coordinateDirection_zero,coordinateDirection_one,directionX,directionY,
      smul_eq_mul,f]
    field_simp [hr]
  apply hasGradientAt_iff_hasFDerivAt.mpr
  change HasFDerivAt (fun z : SourcePlane => f (r • ofLp z)/r^3)
    (toDual ℝ SourcePlane (sourceScaledGradient L r ω p)) p
  rw [hm]
  simpa only [div_eq_mul_inv,mul_comm,Function.comp_def,f] using h

theorem sourceScaledGradient_eq_gradient {L : ℝ} (hL : L ≠ 0) (r : ℝ) (hr : r ≠ 0)
    (ω : SmoothSample 2 L) (p : SourcePlane) :
    sourceScaledGradient L r ω p = gradient (sourceScaledPotential L r ω) p :=
  (sourceScaledPotential_hasGradientAt hL r hr ω p).gradient.symm

theorem sourceScaledGradient_smooth {L : ℝ} (hL : L ≠ 0) (r : ℝ) (ω : SmoothSample 2 L) :
    ContDiff ℝ (⊤ : ℕ∞) (sourceScaledGradient L r ω) := by
  let f := smoothSourceField 2 L ω
  have hf := smoothSourceField_smooth 2 hL ω
  have hg : ContDiff ℝ (⊤ : ℕ∞) (gradientPi f) := by
    apply contDiff_pi.mpr
    intro i
    exact derivativeComponent_smooth f hf (coordinateDirection i)
  have he : ContDiff ℝ (⊤ : ℕ∞) (gradientEuclidean f) :=
    piToEuclidean.contDiff.comp (hg.comp euclideanToPi.contDiff)
  rw [sourceScaledGradient_eq]
  exact (he.comp (r • ContinuousLinearMap.id ℝ SourcePlane).contDiff).const_smul _

theorem pinPreservingQuartic_pins (r q : ℝ) (U : Fin 8 → ℝ) :
    pinPreservingQuartic r q U ![-1/2,0] = 0 ∧
    pinPreservingQuartic r q U ![1/2,0] = 0 := by
  constructor <;> ext i <;> fin_cases i <;> norm_num [pinPreservingQuartic]

theorem sourceScaledGradient_pins (L r : ℝ) (ω : SmoothSample 2 L)
    (hp : sourcePhysicalPins L r ω) :
    sourceScaledGradient L r ω (toLp 2 ![-1/2,0]) = 0 ∧
    sourceScaledGradient L r ω (toLp 2 ![1/2,0]) = 0 := by
  have hM : r • (![-1/2,0] : Fin 2 → ℝ) = endpointM r := by
    ext i; fin_cases i <;> simp [endpointM]; ring
  have hS : r • (![1/2,0] : Fin 2 → ℝ) = endpointS r := by
    ext i; fin_cases i <;> simp [endpointS]; ring
  constructor
  · ext i
    fin_cases i
    · change fderiv ℝ (smoothSourceField 2 L ω) (r • ![-1/2,0]) directionX/r^2=0
      rw [hM]
      exact div_eq_zero_iff.mpr (Or.inl hp.1)
    · change fderiv ℝ (smoothSourceField 2 L ω) (r • ![-1/2,0]) directionY/r^2=0
      rw [hM]
      exact div_eq_zero_iff.mpr (Or.inl hp.2.2.1)
  · ext i
    fin_cases i
    · change fderiv ℝ (smoothSourceField 2 L ω) (r • ![1/2,0]) directionX/r^2=0
      rw [hS]
      exact div_eq_zero_iff.mpr (Or.inl hp.2.1)
    · change fderiv ℝ (smoothSourceField 2 L ω) (r • ![1/2,0]) directionY/r^2=0
      rw [hS]
      exact div_eq_zero_iff.mpr (Or.inl hp.2.2.2.1)




theorem sourceQuartic_value_comparison {L : ℝ} (hL : L ≠ 0) (r : ℝ) (hr : 0 < r)
    (ω : SmoothSample 2 L) (hp : sourcePhysicalPins L r ω) (p : SourcePlane) :
    ‖sourceScaledGradient L r ω p-sourceQuartic L r ω p‖ ≤
      sourceDerivativeMajorant L 5 ω*r^2*(1/120+‖p‖/64+‖p‖^2/80+‖p‖^4/12) := by
  calc
    _ ≤ ‖sourceScaledGradient L r ω p-sourceGradientTaylor L r ω p‖+
        ‖sourceGradientTaylor L r ω p-sourceQuartic L r ω p‖ := norm_sub_le_norm_sub_add_norm_sub _ _ _
    _ ≤ sourceDerivativeMajorant L 5 ω*r^2*‖p‖^4/12+
        sourceDerivativeMajorant L 5 ω*r^2*(1/120+‖p‖/64+‖p‖^2/80) :=
      add_le_add (source_scaled_gradient_taylor_error hL r hr ω p)
        (sourceGradientTaylor_quartic_error_le hL r hr ω hp p)
    _ = _ := by ring

theorem sourceQuartic_operator_comparison {L : ℝ} (hL : L ≠ 0) (r : ℝ) (hr : 0 < r)
    (ω : SmoothSample 2 L) (hp : sourcePhysicalPins L r ω) (p : SourcePlane) :
    ‖fderiv ℝ (sourceScaledGradient L r ω) p-fderiv ℝ (sourceQuartic L r ω) p‖ ≤
      sourceDerivativeMajorant L 5 ω*r^2*(1/96+‖p‖/40+‖p‖^3/3) := by
  calc
    _ ≤ ‖fderiv ℝ (sourceScaledGradient L r ω) p-
          matrixLinearEuclidean (sourceHessianTaylor L r ω (ofLp p))‖+
        ‖matrixLinearEuclidean (sourceHessianTaylor L r ω (ofLp p))-
          fderiv ℝ (sourceQuartic L r ω) p‖ := norm_sub_le_norm_sub_add_norm_sub _ _ _
    _ ≤ sourceDerivativeMajorant L 5 ω*r^2*‖p‖^3/3+
        sourceDerivativeMajorant L 5 ω*r^2*(1/96+‖p‖/40) :=
      add_le_add (source_scaled_hessian_taylor_error hL r hr ω p)
        (sourceHessianTaylor_quartic_error_le hL r hr ω hp p)
    _ = _ := by ring

/-- Uniform value and induced-operator errors on the Euclidean ball. These
two simultaneous uniform bounds are the maximum C1 convention of LM004. -/
theorem sourceQuartic_C1_comparison {L : ℝ} (hL : L ≠ 0) (r : ℝ) (hr : 0 < r)
    (ω : SmoothSample 2 L) (hp : sourcePhysicalPins L r ω) :
    ∀ p : SourcePlane, ‖p‖ ≤ 2 →
      max ‖sourceScaledGradient L r ω p-sourceQuartic L r ω p‖
        ‖fderiv ℝ (sourceScaledGradient L r ω) p-fderiv ℝ (sourceQuartic L r ω) p‖ ≤
          3*r^2*sourceDerivativeMajorant L 5 ω := by
  intro p hp2
  have hG := sourceDerivativeMajorant_nonneg L 5 ω
  have hS : 0 ≤ sourceDerivativeMajorant L 5 ω*r^2 := mul_nonneg hG (sq_nonneg r)
  have h2 : ‖p‖^2 ≤ (2:ℝ)^2 := pow_le_pow_left₀ (norm_nonneg p) hp2 2
  have h3 : ‖p‖^3 ≤ (2:ℝ)^3 := pow_le_pow_left₀ (norm_nonneg p) hp2 3
  have h4 : ‖p‖^4 ≤ (2:ℝ)^4 := pow_le_pow_left₀ (norm_nonneg p) hp2 4
  have hv : (1:ℝ)/120+‖p‖/64+‖p‖^2/80+‖p‖^4/12 ≤ 3 := by nlinarith
  have hd : (1:ℝ)/96+‖p‖/40+‖p‖^3/3 ≤ 3 := by nlinarith
  apply max_le
  · calc
      _ ≤ sourceDerivativeMajorant L 5 ω*r^2*
          (1/120+‖p‖/64+‖p‖^2/80+‖p‖^4/12) := sourceQuartic_value_comparison hL r hr ω hp p
      _ ≤ sourceDerivativeMajorant L 5 ω*r^2*3 := mul_le_mul_of_nonneg_left hv hS
      _ = _ := by ring
  · calc
      _ ≤ sourceDerivativeMajorant L 5 ω*r^2*(1/96+‖p‖/40+‖p‖^3/3) :=
        sourceQuartic_operator_comparison hL r hr ω hp p
      _ ≤ sourceDerivativeMajorant L 5 ω*r^2*3 := mul_le_mul_of_nonneg_left hd hS
      _ = _ := by ring

theorem sourceQuartic_cutoff_tolerance {L : ℝ} (hL : L ≠ 0) (r : ℝ)
    (hr : 0 < r) (hr1 : r ≤ 1) (ω : SmoothSample 2 L)
    (hp : sourcePhysicalPins L r ω)
    (hcut : r*sourceGammaRadius L ω^5 ≤ quarticEpsilonStar) :
    r*sourceRawRadius L ω^5 ≤ 1/(1024*quarticK0) ∧
    (∀ p : SourcePlane, ‖p‖ ≤ 2 →
      max ‖sourceScaledGradient L r ω p-sourceQuartic L r ω p‖
        ‖fderiv ℝ (sourceScaledGradient L r ω) p-fderiv ℝ (sourceQuartic L r ω) p‖ ≤
          sourceRawRadius L ω*quarticWidth r (sourceRawU L ω) (sourceRawRadius L ω)/4) := by
  have hR0 := sourceRawRadius_one_le L ω
  have hR := one_le_sourceGammaRadius L ω
  have hR0R := sourceRawRadius_le_global hL ω
  have hG := sourceDerivativeMajorant_nonneg L 5 ω
  have hGR : sourceDerivativeMajorant L 5 ω ≤ sourceGammaRadius L ω :=
    sourceDerivativeMajorant_le_radius L ω 5
  refine ⟨cutoff_raw_regularity r _ _ hr.le hR0 hR0R hcut,?_⟩
  intro p hp2
  exact (sourceQuartic_C1_comparison hL r hr ω hp p hp2).trans
    (cutoff_quarticWidth_tolerance r _ _ _ _ hr.le hr1 hR hR0 hR0R hG hGR hcut)

theorem sourceQuartic_curvature_threshold {L : ℝ} (hL : L ≠ 0) (r : ℝ) (hr : 0 < r)
    (ω : SmoothSample 2 L)
    (hq : sourceQ L ω ≤ -quarticKcap*r*sourceGammaRadius L ω^5) :
    sourceQ L ω/r ≤ -(2*quarticK0*sourceRawRadius L ω^5+2*sourceRawRadius L ω) :=
  cutoff_curvature_threshold _ r _ _ hr (one_le_sourceGammaRadius L ω)
    (sourceRawRadius_one_le L ω) (sourceRawRadius_le_global hL ω) hq

theorem sourceQuartic_C1_comparison_ae {L : ℝ} (hL : L ≠ 0) (r b : ℝ) (hr : 0 < r)
    (hG : IsUnit (sourcePinCovarianceAt L r)) :
    ∀ᵐ ω ∂sourceSmoothLaw hL r b, ∀ p : SourcePlane, ‖p‖ ≤ 2 →
      max ‖sourceScaledGradient L r ω p-sourceQuartic L r ω p‖
        ‖fderiv ℝ (sourceScaledGradient L r ω) p-fderiv ℝ (sourceQuartic L r ω) p‖ ≤
          3*r^2*sourceDerivativeMajorant L 5 ω := by
  filter_upwards [sourcePhysicalPins_ae hL r b hr.ne' hG] with ω hω
  exact sourceQuartic_C1_comparison hL r hr ω hω

theorem sourceQuartic_C1_estimates {L : ℝ} (hL : L ≠ 0) (b : ℝ) :
    ∃ δ : ℝ, 0 < δ ∧ δ ≤ 1 ∧ ∀ r : ℝ, 0 < r → r < δ →
      ∀ᵐ ω ∂sourceSmoothLaw hL r b, ∀ p : SourcePlane, ‖p‖ ≤ 2 →
        max ‖sourceScaledGradient L r ω p-sourceQuartic L r ω p‖
          ‖fderiv ℝ (sourceScaledGradient L r ω) p-fderiv ℝ (sourceQuartic L r ω) p‖ ≤
            3*r^2*sourceDerivativeMajorant L 5 ω := by
  obtain ⟨δ,hδ,hδ1,hpin⟩ := sourcePhysicalPins_eventually hL b
  refine ⟨δ,hδ,hδ1,?_⟩
  intro r hr hrδ
  filter_upwards [hpin r hr hrδ] with ω hω
  exact sourceQuartic_C1_comparison hL r hr ω hω




theorem sourceRawU_abs_le_radius (L : ℝ) (ω : SmoothSample 2 L) (i : Fin 8) :
    |sourceRawU L ω i| ≤ sourceRawRadius L ω := by
  have h := Finset.single_le_sum (fun j (_ : j ∈ (Finset.univ : Finset (Fin 8))) =>
    abs_nonneg (sourceRawU L ω j)) (Finset.mem_univ i)
  exact h.trans (by unfold sourceRawRadius; linarith)

theorem sourceQuartic_Fstar_le_radius (L r : ℝ) (hr1 : r ≤ 1) (ω : SmoothSample 2 L) :
    quarticFstar r (sourceRawU L ω) ≤ 2*sourceRawRadius L ω := by
  have h0 := sourceRawU_abs_le_radius L ω 0
  have h4 := sourceRawU_abs_le_radius L ω 4
  have hR := sourceRawRadius_one_le L ω
  have hm : r*|sourceRawU L ω 4| ≤ |sourceRawU L ω 4| :=
    mul_le_of_le_one_left (abs_nonneg _) hr1
  unfold quarticFstar
  linarith

theorem sourceQuartic_width_size (L r : ℝ) (hr1 : r ≤ 1) (ω : SmoothSample 2 L) :
    sourceRawRadius L ω*quarticWidth r (sourceRawU L ω) (sourceRawRadius L ω) ≤
      1/2048 := by
  have hR := sourceRawRadius_one_le L ω
  have hR0 : 0 ≤ sourceRawRadius L ω := (by norm_num : (0:ℝ) ≤ 1).trans hR
  have hF := sourceQuartic_Fstar_le_radius L r hr1 ω
  have hpow : sourceRawRadius L ω^2 ≤ sourceRawRadius L ω^5 :=
    pow_le_pow_right₀ hR (by norm_num)
  have hm := mul_le_mul_of_nonneg_left hF hR0
  have hden : 0 < quarticK0*sourceRawRadius L ω^5 :=
    mul_pos (by norm_num [quarticK0]) (pow_pos (lt_of_lt_of_le (by norm_num) hR) 5)
  calc
    _ = (sourceRawRadius L ω*quarticFstar r (sourceRawU L ω))/
        (quarticK0*sourceRawRadius L ω^5) := by unfold quarticWidth; ring
    _ ≤ 1/2048 := by
      apply (div_le_iff₀ hden).mpr
      norm_num only [quarticK0]
      nlinarith

theorem sourceQuartic_width_geometry (L r : ℝ) (hr : 0 ≤ r) (hr1 : r ≤ 1)
    (ω : SmoothSample 2 L) :
    0 < quarticWidth r (sourceRawU L ω) (sourceRawRadius L ω) ∧
    quarticWidth r (sourceRawU L ω) (sourceRawRadius L ω) ≤ 1/2048 ∧
    8*sourceRawRadius L ω*quarticWidth r (sourceRawU L ω) (sourceRawRadius L ω) ≤ 1/256 := by
  have hpos := quarticWidth_pos r _ hr (sourceRawRadius_one_le L ω) (sourceRawU L ω)
  have hgeo := certificate_width_geometry _ _ (sourceRawRadius_one_le L ω)
    (sourceQuartic_width_size L r hr1 ω)
  exact ⟨hpos,hgeo⟩

theorem quartic_strip_in_ball_two (W : ℝ) (hW : W ≤ 1/2048) (p : SourcePlane)
    (hx : |p 0| ≤ 1/2) (hy : |p 1| ≤ W) : ‖p‖ ≤ 2 :=
  (euclidean_two_norm_le_abs_sum p).trans (by linarith)

theorem quartic_endpoint_ball_in_ball_two (ρ : ℝ) (hρ : ρ ≤ 1/256)
    (c p : SourcePlane) (hc : ‖c‖ ≤ 1/2) (hp : ‖p-c‖ ≤ ρ) : ‖p‖ ≤ 2 := by
  calc
    _ = ‖(p-c)+c‖ := by congr 1; abel
    _ ≤ ‖p-c‖+‖c‖ := norm_add_le _ _
    _ ≤ 2 := by linarith

theorem quartic_axis_endpoint_norm (x : ℝ) (hx : |x| ≤ 1/2) :
    ‖(toLp 2 ![x,0] : SourcePlane)‖ ≤ 1/2 := by
  have h := euclidean_two_norm_le_abs_sum (toLp 2 ![x,0])
  simpa using h.trans (by simpa using hx)




theorem sourceQuartic_cutoff_estimates {L : ℝ} (hL : L ≠ 0) (b : ℝ) :
    ∃ δ : ℝ, 0 < δ ∧ δ ≤ 1 ∧ ∀ r : ℝ, 0 < r → r < δ →
      ∀ᵐ ω ∂sourceSmoothLaw hL r b,
        r*sourceGammaRadius L ω^5 ≤ quarticEpsilonStar →
          (r*sourceRawRadius L ω^5 ≤ 1/(1024*quarticK0)) ∧
          (∀ p : SourcePlane, ‖p‖ ≤ 2 →
            max ‖sourceScaledGradient L r ω p-sourceQuartic L r ω p‖
              ‖fderiv ℝ (sourceScaledGradient L r ω) p-fderiv ℝ (sourceQuartic L r ω) p‖ ≤
                sourceRawRadius L ω*quarticWidth r (sourceRawU L ω) (sourceRawRadius L ω)/4) ∧
          (sourceQ L ω ≤ -quarticKcap*r*sourceGammaRadius L ω^5 →
            sourceQ L ω/r ≤ -(2*quarticK0*sourceRawRadius L ω^5+2*sourceRawRadius L ω)) := by
  obtain ⟨δ,hδ,hδ1,hpin⟩ := sourcePhysicalPins_eventually hL b
  refine ⟨δ,hδ,hδ1,?_⟩
  intro r hr hrδ
  have hr1 : r ≤ 1 := hrδ.le.trans hδ1
  filter_upwards [hpin r hr hrδ] with ω hω
  intro hcut
  have h := sourceQuartic_cutoff_tolerance hL r hr hr1 ω hω hcut
  exact ⟨h.1,h.2,sourceQuartic_curvature_threshold hL r hr ω⟩

/-- The actual weighted carrier law inherits the analytic comparison through
its literal density. This is not a geometric point-process Palm assertion. -/
theorem sourceQuartic_weighted_C1_estimates {L : ℝ} (hL : L ≠ 0) (b : ℝ) :
    ∃ δ : ℝ, 0 < δ ∧ δ ≤ 1 ∧ ∀ r : ℝ, 0 < r → r < δ →
      ∀ᵐ ω ∂sourceSmoothWeightedLaw hL r b, ∀ p : SourcePlane, ‖p‖ ≤ 2 →
        max ‖sourceScaledGradient L r ω p-sourceQuartic L r ω p‖
          ‖fderiv ℝ (sourceScaledGradient L r ω) p-fderiv ℝ (sourceQuartic L r ω) p‖ ≤
            3*r^2*sourceDerivativeMajorant L 5 ω := by
  obtain ⟨δ,hδ,hδ1,hbound⟩ := sourceQuartic_C1_estimates hL b
  refine ⟨δ,hδ,hδ1,?_⟩
  intro r hr hrδ
  have hac : sourceSmoothWeightedLaw hL r b ≪ sourceSmoothLaw hL r b := by
    unfold sourceSmoothWeightedLaw ResearchFormalCoreR1.prwMeasure
    exact withDensity_absolutelyContinuous _ _
  exact hac.ae_le (hbound r hr hrδ)

theorem sourceQuartic_weighted_cutoff_estimates {L : ℝ} (hL : L ≠ 0) (b : ℝ) :
    ∃ δ : ℝ, 0 < δ ∧ δ ≤ 1 ∧ ∀ r : ℝ, 0 < r → r < δ →
      ∀ᵐ ω ∂sourceSmoothWeightedLaw hL r b,
        r*sourceGammaRadius L ω^5 ≤ quarticEpsilonStar →
          (r*sourceRawRadius L ω^5 ≤ 1/(1024*quarticK0)) ∧
          (∀ p : SourcePlane, ‖p‖ ≤ 2 →
            max ‖sourceScaledGradient L r ω p-sourceQuartic L r ω p‖
              ‖fderiv ℝ (sourceScaledGradient L r ω) p-fderiv ℝ (sourceQuartic L r ω) p‖ ≤
                sourceRawRadius L ω*quarticWidth r (sourceRawU L ω) (sourceRawRadius L ω)/4) ∧
          (sourceQ L ω ≤ -quarticKcap*r*sourceGammaRadius L ω^5 →
            sourceQ L ω/r ≤ -(2*quarticK0*sourceRawRadius L ω^5+2*sourceRawRadius L ω)) := by
  obtain ⟨δ,hδ,hδ1,hbound⟩ := sourceQuartic_cutoff_estimates hL b
  refine ⟨δ,hδ,hδ1,?_⟩
  intro r hr hrδ
  have hac : sourceSmoothWeightedLaw hL r b ≪ sourceSmoothLaw hL r b := by
    unfold sourceSmoothWeightedLaw ResearchFormalCoreR1.prwMeasure
    exact withDensity_absolutelyContinuous _ _
  exact hac.ae_le (hbound r hr hrδ)


end I4SourcePinPreservingQuartic
