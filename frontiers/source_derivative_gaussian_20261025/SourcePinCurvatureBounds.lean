import SourceConditionalMajorant
import ConfluentIntegralIdentities
import Mathlib.Analysis.Calculus.MeanValue

/-! Literal Peano endpoint and curvature estimates on the actual pin fiber. -/

noncomputable section

open I4Foundation I4Source I4Weights I4SmoothCarrier I4Smooth I4SourceConfluentPins I4SourceEndpointRegression
open I4SourceConditionalMajorant I4SourceSmoothPalm I4SourceContact
open I4SourceEndpointEstimates ResearchFormalCoreR1
open I4SourceSmoothConditional I4SourceDerivativeGaussian I4SourceGaussian
open I4ModeCurveChains I4SourceConfluentLimits I4ConfluentIntegralIdentities
open MeasureTheory ProbabilityTheory Filter Set Matrix
open scoped BigOperators Interval Topology

set_option autoImplicit false

namespace I4PeanoErrorBounds

/-- A nonnegative continuous scalar weight preserves a uniform error bound,
with its exact mass. -/
theorem abs_weighted_integral_le (w f : ℝ → ℝ)
    (hwc : Continuous w) (hfc : Continuous f) (B : ℝ)
    (hw : ∀ t ∈ Icc (-1/2 : ℝ) (1/2 : ℝ), 0 ≤ w t)
    (hf : ∀ t ∈ Icc (-1/2 : ℝ) (1/2 : ℝ), |f t| ≤ B) :
    |∫ t in (-1/2 : ℝ)..(1/2 : ℝ), w t * f t| ≤
      B * ∫ t in (-1/2 : ℝ)..(1/2 : ℝ), w t := by
  calc
    _ ≤ ∫ t in (-1/2 : ℝ)..(1/2 : ℝ), |w t * f t| :=
      intervalIntegral.abs_integral_le_integral_abs (by norm_num)
    _ ≤ ∫ t in (-1/2 : ℝ)..(1/2 : ℝ), B * w t := by
      apply intervalIntegral.integral_mono_on (by norm_num)
        ((hwc.mul hfc).abs.intervalIntegrable _ _)
        ((continuous_const.mul hwc).intervalIntegrable _ _)
      intro t ht
      change |w t * f t| ≤ B * w t
      rw [abs_mul, abs_of_nonneg (hw t ht)]
      calc
        w t * |f t| ≤ w t * B := mul_le_mul_of_nonneg_left (hf t ht) (hw t ht)
        _ = B * w t := mul_comm _ _
    _ = _ := intervalIntegral.integral_const_mul _ _

/-- Subtracting a constant from the averaged function subtracts that constant
times the exact weight mass. -/
theorem abs_weighted_integral_sub_mass_le (w g : ℝ → ℝ)
    (hwc : Continuous w) (hgc : Continuous g) (r c B : ℝ)
    (hw : ∀ t ∈ Icc (-1/2 : ℝ) (1/2 : ℝ), 0 ≤ w t)
    (hg : ∀ t ∈ Icc (-1/2 : ℝ) (1/2 : ℝ), |g (r*t) - c| ≤ B) :
    |(∫ t in (-1/2 : ℝ)..(1/2 : ℝ), w t * g (r*t)) -
      c * (∫ t in (-1/2 : ℝ)..(1/2 : ℝ), w t)| ≤
      B * (∫ t in (-1/2 : ℝ)..(1/2 : ℝ), w t) := by
  have hc : Continuous (fun t => g (r*t)) :=
    hgc.comp (continuous_const.mul continuous_id)
  have heq : (∫ t in (-1/2 : ℝ)..(1/2 : ℝ), w t * (g (r*t)-c)) =
      (∫ t in (-1/2 : ℝ)..(1/2 : ℝ), w t * g (r*t)) -
        c * (∫ t in (-1/2 : ℝ)..(1/2 : ℝ), w t) := by
    simp_rw [mul_sub]
    have hi1 : IntervalIntegrable (fun t => w t * g (r*t)) volume (-1/2 : ℝ) (1/2 : ℝ) :=
      (hwc.mul hc).intervalIntegrable _ _
    have hi2 : IntervalIntegrable (fun t => w t * c) volume (-1/2 : ℝ) (1/2 : ℝ) :=
      (hwc.mul continuous_const).intervalIntegrable _ _
    rw [intervalIntegral.integral_sub hi1 hi2]
    rw [intervalIntegral.integral_mul_const]
    ring
  rw [← heq]
  exact abs_weighted_integral_le w _ hwc (hc.sub continuous_const) B hw hg

theorem peanoCubic_nonneg (t : ℝ) (ht : t ∈ Icc (-1/2 : ℝ) (1/2 : ℝ)) :
    0 ≤ peanoCubic t := by
  unfold peanoCubic
  have hp : 0 ≤ (t+1/2)*(1/2-t) := mul_nonneg (by linarith [ht.1]) (by linarith [ht.2])
  nlinarith

/-- The same scalar Lipschitz bound controls every point of the scaled interval
around the literal value at the origin, retaining the half-interval factor. -/
theorem scaled_lipschitz_center_error (g : ℝ → ℝ) (C r : ℝ) (hC : 0 ≤ C) (hr : 0 ≤ r)
    (hlip : ∀ x y : ℝ, |g x-g y| ≤ C * |x-y|)
    (u : ℝ) (hu : u ∈ Icc (-1/2 : ℝ) (1/2 : ℝ)) :
    |g (r*u)-g 0| ≤ r*C/2 := by
  have huabs : |u| ≤ (1/2 : ℝ) := abs_le.mpr ⟨by linarith [hu.1], hu.2⟩
  calc
    _ ≤ C * |r*u-0| := hlip _ _
    _ = C * (r*|u|) := by rw [sub_zero, abs_mul, abs_of_nonneg hr]
    _ ≤ C * (r*(1/2)) :=
      mul_le_mul_of_nonneg_left (mul_le_mul_of_nonneg_left huabs hr) hC
    _ = r*C/2 := by ring

/-- A globally Lipschitz function with cubic Peano average two stays within
`r*C` of two everywhere in the scaled interval. -/
theorem cubic_pin_pointwise_error (g : ℝ → ℝ) (hgc : Continuous g)
    (C r : ℝ) (hC : 0 ≤ C) (hr : 0 ≤ r)
    (hlip : ∀ x y : ℝ, |g x - g y| ≤ C * |x-y|)
    (hpin : 6 * (∫ t in (-1/2 : ℝ)..(1/2 : ℝ), peanoCubic t * g (r*t)) = 2)
    (u : ℝ) (hu : u ∈ Icc (-1/2 : ℝ) (1/2 : ℝ)) :
    |g (r*u) - 2| ≤ r*C := by
  have hcK : Continuous peanoCubic := by unfold peanoCubic; fun_prop
  have hcG : Continuous (fun t => g (r*u) - g (r*t)) := by
    exact continuous_const.sub (hgc.comp (continuous_const.mul continuous_id))
  have hbound : ∀ t ∈ Icc (-1/2 : ℝ) (1/2 : ℝ), |g (r*u) - g (r*t)| ≤ r*C := by
    intro t ht
    have hud : |u-t| ≤ 1 := abs_le.mpr ⟨by linarith [hu.1, ht.2], by linarith [hu.2, ht.1]⟩
    calc
      _ ≤ C * |r*u-r*t| := hlip _ _
      _ = C * (r*|u-t|) := by rw [← mul_sub, abs_mul, abs_of_nonneg hr]
      _ ≤ C * r := mul_le_mul_of_nonneg_left (mul_le_of_le_one_right hr hud) hC
      _ = r*C := mul_comm _ _
  have hi := abs_weighted_integral_le peanoCubic _ hcK hcG (r*C) peanoCubic_nonneg hbound
  have hmass := peano_kernel_masses.2.2.2
  have hmass' : (∫ t in (-1/2 : ℝ)..(1/2 : ℝ), peanoCubic t) = 1/6 := by
    linarith [hmass]
  rw [hmass'] at hi
  have heq : 6 * (∫ t in (-1/2 : ℝ)..(1/2 : ℝ),
      peanoCubic t * (g (r*u)-g (r*t))) = g (r*u)-2 := by
    simp_rw [mul_sub]
    have hi1 : IntervalIntegrable (fun t => peanoCubic t * g (r*u)) volume
        (-1/2 : ℝ) (1/2 : ℝ) := (hcK.mul continuous_const).intervalIntegrable _ _
    have hi2 : IntervalIntegrable (fun t => peanoCubic t * g (r*t)) volume
        (-1/2 : ℝ) (1/2 : ℝ) :=
      (hcK.mul (hgc.comp (continuous_const.mul continuous_id))).intervalIntegrable _ _
    rw [intervalIntegral.integral_sub hi1 hi2]
    rw [intervalIntegral.integral_mul_const]
    rw [hmass']
    nlinarith [hpin, hmass]
  have habs : |g (r*u)-2| = 6 * |∫ t in (-1/2 : ℝ)..(1/2 : ℝ),
      peanoCubic t * (g (r*u)-g (r*t))| := by
    rw [← heq, abs_mul]
    norm_num
  rw [habs]
  nlinarith [hi, hmass]

/-- The left affine Peano average retains half the uniform pointwise error. -/
theorem left_weighted_error (g : ℝ → ℝ) (hgc : Continuous g) (r c B : ℝ)
    (hg : ∀ t ∈ Icc (-1/2 : ℝ) (1/2 : ℝ), |g (r*t)-c| ≤ B) :
    |(∫ t in (-1/2 : ℝ)..(1/2 : ℝ), peanoLeft t * g (r*t)) - c/2| ≤ B/2 := by
  have hc : Continuous peanoLeft := by unfold peanoLeft; fun_prop
  have hw : ∀ t ∈ Icc (-1/2 : ℝ) (1/2 : ℝ), 0 ≤ peanoLeft t := by
    intro t ht
    unfold peanoLeft
    linarith [ht.2]
  have h := abs_weighted_integral_sub_mass_le peanoLeft g hc hgc r c B hw hg
  rw [peano_kernel_masses.2.1] at h
  simpa only [mul_one_div] using h

/-- The right affine Peano average retains half the uniform pointwise error. -/
theorem right_weighted_error (g : ℝ → ℝ) (hgc : Continuous g) (r c B : ℝ)
    (hg : ∀ t ∈ Icc (-1/2 : ℝ) (1/2 : ℝ), |g (r*t)-c| ≤ B) :
    |(∫ t in (-1/2 : ℝ)..(1/2 : ℝ), peanoRight t * g (r*t)) - c/2| ≤ B/2 := by
  have hc : Continuous peanoRight := by unfold peanoRight; fun_prop
  have hw : ∀ t ∈ Icc (-1/2 : ℝ) (1/2 : ℝ), 0 ≤ peanoRight t := by
    intro t ht
    unfold peanoRight
    linarith [ht.1]
  have h := abs_weighted_integral_sub_mass_le peanoRight g hc hgc r c B hw hg
  rw [peano_kernel_masses.2.2.1] at h
  simpa only [mul_one_div] using h

end I4PeanoErrorBounds

open I4PeanoErrorBounds

namespace I4SourcePinCurvatureBounds

/-- One measurable certificate controlling the field derivatives through order five. -/
def sourceGammaRadius (L : ℝ) (ω : SmoothSample 2 L) : ℝ :=
  1 + ∑ k : Fin 6, sourceDerivativeMajorant L (k : ℕ) ω

def sourceQ (L : ℝ) (ω : SmoothSample 2 L) : ℝ :=
  iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω) 0 ![directionY,directionY]

def sourceA (L : ℝ) (ω : SmoothSample 2 L) : ℝ :=
  iteratedFDeriv ℝ 3 (smoothSourceField 2 L ω) 0 ![directionX,directionX,directionY]

theorem sourceQ_eq_sourceContactQ (L : ℝ) (ω : SmoothSample 2 L) :
    sourceQ L ω = sourceContactQ L ω := rfl

theorem sourceA_eq_sourceContactA (L : ℝ) (ω : SmoothSample 2 L) :
    sourceA L ω = sourceContactA L ω := rfl

theorem sourceDerivativeMajorant_nonneg (L : ℝ) (k : ℕ) (ω : SmoothSample 2 L) :
    0 ≤ sourceDerivativeMajorant L k ω :=
  sampleMajorant_nonneg _ (orderModeBound_nonneg k 2 L) ω

theorem sourceGammaRadius_measurable (L : ℝ) : Measurable (sourceGammaRadius L) := by
  exact measurable_const.add (Finset.measurable_sum _
    (fun k _ => sourceDerivativeMajorant_measurable L k))

theorem one_le_sourceGammaRadius (L : ℝ) (ω : SmoothSample 2 L) :
    1 ≤ sourceGammaRadius L ω := by
  unfold sourceGammaRadius
  exact le_add_of_nonneg_right (Finset.sum_nonneg (fun k _ =>
    sourceDerivativeMajorant_nonneg L k ω))

theorem sourceGammaRadius_nonneg (L : ℝ) (ω : SmoothSample 2 L) :
    0 ≤ sourceGammaRadius L ω := (by norm_num : (0 : ℝ) ≤ 1).trans
      (one_le_sourceGammaRadius L ω)

theorem sourceDerivativeMajorant_le_radius (L : ℝ) (ω : SmoothSample 2 L) (k : Fin 6) :
    sourceDerivativeMajorant L k ω ≤ sourceGammaRadius L ω := by
  have h := Finset.single_le_sum (fun j (_ : j ∈ (Finset.univ : Finset (Fin 6))) =>
    sourceDerivativeMajorant_nonneg L j ω) (Finset.mem_univ k)
  exact h.trans (by unfold sourceGammaRadius; linarith)

lemma orderModeBound_mono (d : ℕ) (L : ℝ) {k n : ℕ} (hkn : k ≤ n) (m : SourceMode d) :
    orderModeBound k d L m ≤ orderModeBound n d L m := by
  cases m with
  | none => rfl
  | some p =>
    unfold orderModeBound orderPairedBound orderProductBound orderCoordinateBound
    apply mul_le_mul_of_nonneg_left _ (Real.sqrt_nonneg _)
    apply Finset.prod_le_prod₀
    · intro i _
      exact mul_nonneg (Real.exp_pos _).le (pow_nonneg (by positivity) k)
    · intro i _
      apply mul_le_mul_of_nonneg_left _ (Real.exp_pos _).le
      exact pow_le_pow_right₀ (by linarith [abs_nonneg (sourceC L * (p.1.val i : ℝ))]) hkn

lemma sourceDerivativeMajorant_mono (L : ℝ) {k n : ℕ} (hkn : k ≤ n)
    (ω : SmoothSample 2 L) : sourceDerivativeMajorant L k ω ≤ sourceDerivativeMajorant L n ω := by
  exact (ω.property k).tsum_le_tsum
    (fun m => mul_le_mul_of_nonneg_right (orderModeBound_mono 2 L hkn m) (abs_nonneg _))
    (ω.property n)

lemma sourceGammaRadius_le_fifth (L : ℝ) (ω : SmoothSample 2 L) :
    sourceGammaRadius L ω ≤ 1 + 6 * sourceDerivativeMajorant L 5 ω := by
  unfold sourceGammaRadius
  apply add_le_add_right
  calc
    _ ≤ ∑ _k : Fin 6, sourceDerivativeMajorant L 5 ω :=
      Finset.sum_le_sum (fun k _ => sourceDerivativeMajorant_mono L (Nat.le_of_lt_succ k.isLt) ω)
    _ = _ := by simp

theorem sourceGammaRadius_moments {L : ℝ} (hL : L ≠ 0) (b : ℝ) :
    ∃ δ : ℝ, 0 < δ ∧ δ ≤ 1 ∧ ∀ n : ℕ, ∃ M : ℝ, 0 ≤ M ∧
      ∀ r : ℝ, 0 < r → r < δ →
        Integrable (fun ω => sourceGammaRadius L ω ^ n) (sourceSmoothLaw hL r b) ∧
        (∫ ω, sourceGammaRadius L ω ^ n ∂sourceSmoothLaw hL r b) ≤ M := by
  obtain ⟨δ,hδ,hδ1,hmom⟩ := sourceConditionalDerivative_moments hL b 5
  refine ⟨δ,hδ,hδ1,?_⟩
  intro n
  obtain ⟨M,hM,hbound⟩ := hmom n
  refine ⟨(2:ℝ)^(n-1)*(1+6^n*M),by positivity,?_⟩
  intro r hr hrδ
  obtain ⟨hΓ,hint⟩ := hbound r hr hrδ
  let Q := sourceSmoothLaw hL r b
  have : IsProbabilityMeasure Q := inferInstance
  change Integrable (fun ω => sourceDerivativeMajorant L 5 ω ^ n) Q at hΓ
  change (∫ ω, sourceDerivativeMajorant L 5 ω ^ n ∂Q) ≤ M at hint
  have hnon (ω : SmoothSample 2 L) : 0 ≤ sourceGammaRadius L ω :=
    (show (0:ℝ) ≤ 1 by norm_num).trans (one_le_sourceGammaRadius L ω)
  have hΓ0 (ω : SmoothSample 2 L) : 0 ≤ sourceDerivativeMajorant L 5 ω :=
    sampleMajorant_nonneg _ (orderModeBound_nonneg _ 2 L) ω
  have hpoint (ω : SmoothSample 2 L) : sourceGammaRadius L ω ^ n ≤
      (2:ℝ)^(n-1)*(1+6^n*sourceDerivativeMajorant L 5 ω^n) := by
    calc
      _ ≤ (1+6*sourceDerivativeMajorant L 5 ω)^n :=
        pow_le_pow_left₀ (hnon ω) (sourceGammaRadius_le_fifth L ω) n
      _ ≤ (2:ℝ)^(n-1)*(1^n+(6*sourceDerivativeMajorant L 5 ω)^n) :=
        add_pow_le (by norm_num) (mul_nonneg (by norm_num) (hΓ0 ω)) n
      _ = _ := by rw [one_pow, mul_pow]
  have hmajor : Integrable (fun ω =>
      (2:ℝ)^(n-1)*(1+6^n*sourceDerivativeMajorant L 5 ω^n)) Q :=
    ((integrable_const 1).add (hΓ.const_mul _)).const_mul _
  have hR : Integrable (fun ω => sourceGammaRadius L ω^n) Q := by
    apply hmajor.mono' ((sourceGammaRadius_measurable L).pow_const n).aestronglyMeasurable
    filter_upwards [] with ω
    rw [Real.norm_eq_abs, abs_of_nonneg (pow_nonneg (hnon ω) n)]
    exact hpoint ω
  refine ⟨hR,?_⟩
  calc
    _ ≤ ∫ ω, (2:ℝ)^(n-1)*(1+6^n*sourceDerivativeMajorant L 5 ω^n) ∂Q :=
      integral_mono hR hmajor hpoint
    _ = (2:ℝ)^(n-1)*(1+6^n*(∫ ω, sourceDerivativeMajorant L 5 ω^n ∂Q)) := by
      rw [integral_const_mul,
        integral_add (f := fun _ => (1 : ℝ)) (g := fun ω => 6^n*sourceDerivativeMajorant L 5 ω^n)
          (integrable_const _) (hΓ.const_mul _), integral_const_mul]
      simp
    _ ≤ _ := by gcongr




def sourceF (L : ℝ) (ω : SmoothSample 2 L) (t : ℝ) : ℝ :=
  smoothSourceField 2 L ω ![t,0]

def sourceH (L : ℝ) (ω : SmoothSample 2 L) (t : ℝ) : ℝ :=
  fderiv ℝ (smoothSourceField 2 L ω) ![t,0] directionY

def sourceQCurve (L : ℝ) (ω : SmoothSample 2 L) (t : ℝ) : ℝ :=
  iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω) ![t,0] ![directionY,directionY]

theorem directionX_norm_le_one : ‖directionX‖ ≤ (1 : ℝ) := by
  apply (pi_norm_le_iff_of_nonneg zero_le_one).mpr
  intro i
  fin_cases i <;> norm_num [directionX]

theorem directionY_norm_le_one : ‖directionY‖ ≤ (1 : ℝ) := by
  apply (pi_norm_le_iff_of_nonneg zero_le_one).mpr
  intro i
  fin_cases i <;> norm_num [directionY]

theorem axis_point_sub_norm_le (s t : ℝ) :
    ‖(![s,0] : Fin 2 → ℝ) - ![t,0]‖ ≤ |s-t| := by
  apply (pi_norm_le_iff_of_nonneg (abs_nonneg _)).mpr
  intro i
  fin_cases i <;> simp [Real.norm_eq_abs]

/-- A bound on the next operator derivative gives a Lipschitz bound for
every fixed unit-bounded derivative tuple along the actual x axis. -/
theorem axis_derivative_lipschitz
    (f : (Fin 2 → ℝ) → ℝ) (hf : ContDiff ℝ (⊤ : ℕ∞) f)
    (k : ℕ) (u : Fin k → (Fin 2 → ℝ)) (hu : ∀ i, ‖u i‖ ≤ 1)
    (C : ℝ) (hbound : ∀ x, ‖iteratedFDeriv ℝ (k+1) f x‖ ≤ C)
    (s t : ℝ) :
    |iteratedFDeriv ℝ k f ![s,0] u - iteratedFDeriv ℝ k f ![t,0] u| ≤ C * |s-t| := by
  have hfk : ContDiff ℝ (k+1 : ℕ) f :=
    hf.of_le (by exact_mod_cast (show (k+1 : ℕ∞) ≤ ⊤ from le_top))
  have hdiff : Differentiable ℝ (iteratedFDeriv ℝ k f) :=
    hfk.differentiable_iteratedFDeriv (by exact_mod_cast Nat.lt_succ_self k)
  have hC : 0 ≤ C := (norm_nonneg _).trans (hbound 0)
  have hD : ‖iteratedFDeriv ℝ k f ![s,0] - iteratedFDeriv ℝ k f ![t,0]‖ ≤
      C * ‖(![s,0] : Fin 2 → ℝ)-![t,0]‖ := by
    apply Convex.norm_image_sub_le_of_norm_fderiv_le
      (fun x _ => hdiff x) (fun x _ => ?_) convex_univ (mem_univ _) (mem_univ _)
    rw [norm_fderiv_iteratedFDeriv]
    exact hbound x
  have hprod : ∏ i, ‖u i‖ ≤ (1 : ℝ) :=
    Finset.prod_le_one₀ (fun _ _ => norm_nonneg _) (fun i _ => hu i)
  calc
    _ = ‖(iteratedFDeriv ℝ k f ![s,0] - iteratedFDeriv ℝ k f ![t,0]) u‖ := by
      rfl
    _ ≤ ‖iteratedFDeriv ℝ k f ![s,0] - iteratedFDeriv ℝ k f ![t,0]‖ * ∏ i, ‖u i‖ :=
      ContinuousMultilinearMap.le_opNorm _ _
    _ ≤ ‖iteratedFDeriv ℝ k f ![s,0] - iteratedFDeriv ℝ k f ![t,0]‖ :=
      mul_le_of_le_one_right (norm_nonneg _) hprod
    _ ≤ C * |s-t| := hD.trans (mul_le_mul_of_nonneg_left (axis_point_sub_norm_le s t) hC)

/-- Literal actual derivative values inherit the globally proved Fourier majorant. -/
theorem source_axis_derivative_abs_le {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L)
    (k : ℕ) (u : Fin k → (Fin 2 → ℝ)) (hu : ∀ i, ‖u i‖ ≤ 1) (t : ℝ) :
    |iteratedFDeriv ℝ k (smoothSourceField 2 L ω) ![t,0] u| ≤
      sourceDerivativeMajorant L k ω := by
  have hprod : ∏ i, ‖u i‖ ≤ (1 : ℝ) :=
    Finset.prod_le_one₀ (fun _ _ => norm_nonneg _) (fun i _ => hu i)
  calc
    _ ≤ ‖iteratedFDeriv ℝ k (smoothSourceField 2 L ω) ![t,0]‖ * ∏ i, ‖u i‖ :=
      ContinuousMultilinearMap.le_opNorm _ _
    _ ≤ ‖iteratedFDeriv ℝ k (smoothSourceField 2 L ω) ![t,0]‖ :=
      mul_le_of_le_one_right (norm_nonneg _) hprod
    _ ≤ _ := smoothSourceField_global_derivative_bound hL k ω ![t,0]

theorem sourceF_third_continuous {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) :
    Continuous (iteratedDeriv 3 (sourceF L ω)) := by
  have hF : ContDiff ℝ (⊤ : ℕ∞) (sourceF L ω) :=
    (smoothSourceField_smooth 2 hL ω).comp axisMap.contDiff
  exact hF.continuous_iteratedDeriv 3 (by simp)

theorem sourceH_second_continuous {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) :
    Continuous (iteratedDeriv 2 (sourceH L ω)) := by
  have hH : ContDiff ℝ (⊤ : ℕ∞) (sourceH L ω) :=
    axis_transverse_smooth _ (smoothSourceField_smooth 2 hL ω)
  exact hH.continuous_iteratedDeriv 2 (by simp)

theorem sourceF_third_lipschitz {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) (s t : ℝ) :
    |iteratedDeriv 3 (sourceF L ω) s - iteratedDeriv 3 (sourceF L ω) t| ≤
      sourceDerivativeMajorant L 4 ω * |s-t| := by
  unfold sourceF
  rw [axis_iteratedDeriv _ (smoothSourceField_smooth 2 hL ω) 3 s,
    axis_iteratedDeriv _ (smoothSourceField_smooth 2 hL ω) 3 t]
  exact axis_derivative_lipschitz _ (smoothSourceField_smooth 2 hL ω) 3
    (fun _ => directionX) (fun _ => directionX_norm_le_one) _
    (smoothSourceField_global_derivative_bound hL 4 ω) s t

theorem sourceH_second_lipschitz {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) (s t : ℝ) :
    |iteratedDeriv 2 (sourceH L ω) s - iteratedDeriv 2 (sourceH L ω) t| ≤
      sourceDerivativeMajorant L 4 ω * |s-t| := by
  unfold sourceH
  rw [axis_transverse_iteratedDeriv _ (smoothSourceField_smooth 2 hL ω) 2 s,
    axis_transverse_iteratedDeriv _ (smoothSourceField_smooth 2 hL ω) 2 t]
  apply axis_derivative_lipschitz _ (smoothSourceField_smooth 2 hL ω) 3 _ ?_ _
    (smoothSourceField_global_derivative_bound hL 4 ω) s t
  intro i
  fin_cases i
  · exact directionX_norm_le_one
  · change ‖directionX‖ ≤ (1 : ℝ)
    exact directionX_norm_le_one
  · change ‖directionY‖ ≤ (1 : ℝ)
    exact directionY_norm_le_one

theorem sourceQCurve_lipschitz {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) (s t : ℝ) :
    |sourceQCurve L ω s - sourceQCurve L ω t| ≤
      sourceDerivativeMajorant L 3 ω * |s-t| := by
  apply axis_derivative_lipschitz _ (smoothSourceField_smooth 2 hL ω) 2 _ ?_ _
    (smoothSourceField_global_derivative_bound hL 3 ω) s t
  intro i
  fin_cases i <;> exact directionY_norm_le_one

theorem sourceF_third_abs_le {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) (t : ℝ) :
    |iteratedDeriv 3 (sourceF L ω) t| ≤ sourceDerivativeMajorant L 3 ω := by
  unfold sourceF
  rw [axis_iteratedDeriv _ (smoothSourceField_smooth 2 hL ω) 3 t]
  exact source_axis_derivative_abs_le hL ω 3 (fun _ => directionX)
    (fun _ => directionX_norm_le_one) t

theorem sourceH_second_abs_le {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) (t : ℝ) :
    |iteratedDeriv 2 (sourceH L ω) t| ≤ sourceDerivativeMajorant L 3 ω := by
  unfold sourceH
  rw [axis_transverse_iteratedDeriv _ (smoothSourceField_smooth 2 hL ω) 2 t]
  apply source_axis_derivative_abs_le hL ω 3 _ ?_ t
  intro i
  fin_cases i
  · exact directionX_norm_le_one
  · change ‖directionX‖ ≤ (1 : ℝ)
    exact directionX_norm_le_one
  · change ‖directionY‖ ≤ (1 : ℝ)
    exact directionY_norm_le_one

theorem sourceQCurve_abs_le {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) (t : ℝ) :
    |sourceQCurve L ω t| ≤ sourceDerivativeMajorant L 2 ω := by
  apply source_axis_derivative_abs_le hL ω 2 _ ?_ t
  intro i
  fin_cases i <;> exact directionY_norm_le_one


theorem sourceF_C3 {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) :
    ContDiff ℝ 3 (sourceF L ω) :=
  ((smoothSourceField_smooth 2 hL ω).comp axisMap.contDiff).of_le (by simp)

theorem sourceH_C2 {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) :
    ContDiff ℝ 2 (sourceH L ω) :=
  (axis_transverse_smooth _ (smoothSourceField_smooth 2 hL ω)).of_le (by simp)

theorem sourceF_deriv {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) (t : ℝ) :
    deriv (sourceF L ω) t = fderiv ℝ (smoothSourceField 2 L ω) ![t,0] directionX := by
  change deriv (fun s => smoothSourceField 2 L ω ![s,0]) t = _
  have h := axis_iteratedDeriv _ (smoothSourceField_smooth 2 hL ω) 1 t
  simpa [sourceF,iteratedDeriv_one,iteratedFDeriv_one_apply] using h

theorem sourceF_second {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) (t : ℝ) :
    iteratedDeriv 2 (sourceF L ω) t =
      iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω) ![t,0] ![directionX,directionX] := by
  change iteratedDeriv 2 (fun s => smoothSourceField 2 L ω ![s,0]) t = _
  have h := axis_iteratedDeriv _ (smoothSourceField_smooth 2 hL ω) 2 t
  have hd : (fun _ : Fin 2 => directionX) = ![directionX,directionX] := by
    ext i; fin_cases i <;> rfl
  simpa only [sourceF,hd] using h

theorem sourceH_deriv {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) (t : ℝ) :
    deriv (sourceH L ω) t =
      iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω) ![t,0] ![directionX,directionY] := by
  change deriv (fun s => fderiv ℝ (smoothSourceField 2 L ω) ![s,0] directionY) t = _
  have h := axis_transverse_iteratedDeriv _ (smoothSourceField_smooth 2 hL ω) 1 t
  have hd : Fin.snoc (fun _ : Fin 1 => directionX) directionY =
      ![directionX,directionY] := by ext i; fin_cases i <;> rfl
  simpa only [sourceH,iteratedDeriv_one,hd] using h

theorem sourceH_second_zero {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) :
    iteratedDeriv 2 (sourceH L ω) 0 = sourceA L ω := by
  change iteratedDeriv 2 (fun s => fderiv ℝ (smoothSourceField 2 L ω) ![s,0] directionY) 0 = _
  have h := axis_transverse_iteratedDeriv _ (smoothSourceField_smooth 2 hL ω) 2 0
  have hd : Fin.snoc (fun _ : Fin 2 => directionX) directionY =
      ![directionX,directionX,directionY] := by ext i; fin_cases i <;> rfl
  have h0 : (![0,0] : Fin 2 → ℝ) = 0 := by ext i; fin_cases i <;> rfl
  simpa only [sourceA,hd,h0] using h

theorem source_pin3_eq {L : ℝ} (hL : L ≠ 0) (r : ℝ) (ω : SmoothSample 2 L) :
    sourceConfluentPinsAt L r ω 3 = pin3 (sourceF L ω) r := by
  simp [sourceConfluentPinsAt,confluentTransform,rawPins,pin3,sourceF_deriv hL,
    endpointM,endpointS]

theorem source_pin4_eq (L r : ℝ) (ω : SmoothSample 2 L) :
    sourceConfluentPinsAt L r ω 4 = pin4 (sourceH L ω) r := rfl

theorem source_pin5_eq {L : ℝ} (hL : L ≠ 0) (r : ℝ) (ω : SmoothSample 2 L) :
    sourceConfluentPinsAt L r ω 5 = pin5 (sourceF L ω) r := by
  change (12/r^2) *
    ((fderiv ℝ (smoothSourceField 2 L ω) ![-r/2,0] directionX +
      fderiv ℝ (smoothSourceField 2 L ω) ![r/2,0] directionX)/2 -
      (smoothSourceField 2 L ω ![r/2,0] - smoothSourceField 2 L ω ![-r/2,0])/r) = _
  unfold pin5
  rw [sourceF_deriv hL,sourceF_deriv hL]
  change (12/r^2) *
    ((fderiv ℝ (smoothSourceField 2 L ω) ![-r/2,0] directionX +
      fderiv ℝ (smoothSourceField 2 L ω) ![r/2,0] directionX)/2 -
      (smoothSourceField 2 L ω ![r/2,0] - smoothSourceField 2 L ω ![-r/2,0])/r) =
    (12/r^2) *
    ((fderiv ℝ (smoothSourceField 2 L ω) ![r/2,0] directionX +
      fderiv ℝ (smoothSourceField 2 L ω) ![-r/2,0] directionX)/2 -
      (smoothSourceField 2 L ω ![r/2,0] - smoothSourceField 2 L ω ![-r/2,0])/r)
  ring

theorem source_normalized_peano {L : ℝ} (hL : L ≠ 0) (r : ℝ) (hr : r ≠ 0)
    (ω : SmoothSample 2 L) (h3 : sourceConfluentPinsAt L r ω 3 = 0)
    (h4 : sourceConfluentPinsAt L r ω 4 = 0) :
    sourceNormalizedEndpoints L r ω =
      ![-(∫ u in (-1/2:ℝ)..(1/2:ℝ), peanoLeft u * iteratedDeriv 3 (sourceF L ω) (r*u)),
        (∫ u in (-1/2:ℝ)..(1/2:ℝ), peanoRight u * iteratedDeriv 3 (sourceF L ω) (r*u)),
        -(∫ u in (-1/2:ℝ)..(1/2:ℝ), peanoLeft u * iteratedDeriv 2 (sourceH L ω) (r*u)),
        (∫ u in (-1/2:ℝ)..(1/2:ℝ), peanoRight u * iteratedDeriv 2 (sourceH L ω) (r*u)),
        sourceQCurve L ω (-r/2),sourceQCurve L ω (r/2)] := by
  have hx := adjusted_second_left (sourceF L ω) (sourceF_C3 hL ω) r hr
  have hy := adjusted_second_right (sourceF L ω) (sourceF_C3 hL ω) r hr
  have hz := adjusted_transverse_left (sourceH L ω) (sourceH_C2 hL ω) r hr
  have hw := adjusted_transverse_right (sourceH L ω) (sourceH_C2 hL ω) r hr
  have hp3 : pin3 (sourceF L ω) r = 0 := (source_pin3_eq hL r ω).symm.trans h3
  have hp4 : pin4 (sourceH L ω) r = 0 := (source_pin4_eq L r ω).symm.trans h4
  rw [hp3,sub_zero,sourceF_second hL] at hx hy
  rw [hp4,sub_zero,sourceH_deriv hL] at hz hw
  ext i
  fin_cases i
  · simpa [sourceNormalizedEndpoints,rawPinsWithHessians,endpointM,peanoLeft] using hx
  · simpa [sourceNormalizedEndpoints,rawPinsWithHessians,endpointS,peanoRight] using hy
  · simpa [sourceNormalizedEndpoints,rawPinsWithHessians,endpointM,peanoLeft] using hz
  · simpa [sourceNormalizedEndpoints,rawPinsWithHessians,endpointS,peanoRight] using hw
  · rfl
  · rfl




theorem endpoint_det_abs_le (r R q : ℝ) (hr : 0 ≤ r) (hR : 0 ≤ R)
    (a b c : ℝ) (ha : |a| ≤ R) (hb : |b| ≤ R) (hc : |c-q| ≤ r*R) :
    |a*c-r*b^2| ≤ R*|q|+2*r*R^2 := by
  have hc' : |c| ≤ |q|+r*R := by
    calc
      _ = |(c-q)+q| := by ring_nf
      _ ≤ |c-q|+|q| := abs_add_le _ _
      _ ≤ _ := by linarith
  have hb2 : |b|^2 ≤ R^2 := pow_le_pow_left₀ (abs_nonneg b) hb 2
  calc
    _ ≤ |a*c|+|r*b^2| := abs_sub _ _
    _ = |a| *|c|+r*|b|^2 := by rw [abs_mul,abs_mul,abs_of_nonneg hr,abs_pow]
    _ ≤ R*(|q|+r*R)+r*R^2 := add_le_add
      (mul_le_mul ha hc' (abs_nonneg _) hR) (mul_le_mul_of_nonneg_left hb2 hr)
    _ = _ := by ring

theorem endpointWeight_curvature_le (r R q : ℝ) (hr : 0 ≤ r) (hR : 0 ≤ R)
    (v : Fin 6 → ℝ) (h0 : |v 0| ≤ R) (h1 : |v 1| ≤ R)
    (h2 : |v 2| ≤ R) (h3 : |v 3| ≤ R)
    (h4 : |v 4-q| ≤ r*R) (h5 : |v 5-q| ≤ r*R) :
    sourceEndpointWeight r v ≤ 2*r^2*R^2*q^2+8*r^4*R^4 := by
  have hM := endpoint_det_abs_le r R q hr hR (v 0) (v 2) (v 4) h0 h2 h4
  have hS := endpoint_det_abs_le r R q hr hR (v 1) (v 3) (v 5) h1 h3 h5
  have hB : 0 ≤ R*|q|+2*r*R^2 := by positivity
  have hprod : |v 0*v 4-r*v 2^2| *|v 1*v 5-r*v 3^2| ≤
      (R*|q|+2*r*R^2)^2 := by
    simpa only [pow_two] using mul_le_mul hM hS (abs_nonneg _) hB
  have hsquare : r^2*(R*|q|+2*r*R^2)^2 ≤ 2*r^2*R^2*q^2+8*r^4*R^4 := by
    have hh : (R*|q|+2*r*R^2)^2 ≤ 2*(R*|q|)^2+2*(2*r*R^2)^2 := by
      nlinarith [sq_nonneg (R*|q|-2*r*R^2)]
    calc
      _ ≤ r^2*(2*(R*|q|)^2+2*(2*r*R^2)^2) :=
        mul_le_mul_of_nonneg_left hh (sq_nonneg r)
      _ = _ := by rw [mul_pow R, sq_abs]; ring
  unfold sourceEndpointWeight egm_weight
  split_ifs
  · have heq : (egm_HM r (sourcePhysicalCoordinates v)).det *
        (egm_HS r (sourcePhysicalCoordinates v)).det =
        r^2*((v 0*v 4-r*v 2^2)*(v 1*v 5-r*v 3^2)) := by
      simp [egm_HM,egm_HS,sourcePhysicalCoordinates,Matrix.det_fin_two]
      ring
    rw [heq,abs_mul,abs_of_nonneg (sq_nonneg r),abs_mul]
    exact (mul_le_mul_of_nonneg_left hprod (sq_nonneg r)).trans hsquare
  · positivity

theorem strict_endpoint_transverse_neg (r : ℝ) (v : Fin 6 → ℝ)
    (ht : dm2Negative (egm_HM r (sourcePhysicalCoordinates v))) : v 4 < 0 := by
  have h := ht ![0,1] (by simp)
  simpa [egm_HM,sourcePhysicalCoordinates,Fin.sum_univ_two] using h

theorem curvature_slab_of_upper (q r R Γ K : ℝ) (hr : 0 ≤ r) (hR : 1 ≤ R)
    (hΓ : Γ ≤ R) (hu : q < r*Γ) (hl : -K*r*R^5 ≤ q) :
    |q| ≤ max K 1*r*R^5 := by
  have hR0 : 0 ≤ R := le_trans (by norm_num) hR
  have hp : R ≤ R^5 := by
    calc
      R = R^1 := by simp
      _ ≤ R^5 := pow_le_pow_right₀ hR (by norm_num)
  have hmax : 1 ≤ max K 1 := le_max_right _ _
  have hl' : -(max K 1*r*R^5) ≤ q := by
    have hh := mul_le_mul_of_nonneg_right (le_max_left K 1) (mul_nonneg hr (pow_nonneg hR0 5))
    nlinarith
  have hu' : q ≤ max K 1*r*R^5 := by
    have hq := hu.le.trans (mul_le_mul_of_nonneg_left (hΓ.trans hp) hr)
    have hh := mul_le_mul_of_nonneg_right hmax (mul_nonneg hr (pow_nonneg hR0 5))
    nlinarith
  exact abs_le.mpr ⟨hl',hu'⟩




theorem sourceQCurve_zero (L : ℝ) (ω : SmoothSample 2 L) :
    sourceQCurve L ω 0 = sourceQ L ω := by
  have h0 : (![0,0] : Fin 2 → ℝ) = 0 := by ext i; fin_cases i <;> rfl
  simp only [sourceQCurve,sourceQ,h0]

theorem sourceQ_abs_le {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) :
    |sourceQ L ω| ≤ sourceDerivativeMajorant L 2 ω :=
  by simpa only [sourceQCurve_zero] using sourceQCurve_abs_le hL ω 0

theorem sourceA_abs_le {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) :
    |sourceA L ω| ≤ sourceDerivativeMajorant L 3 ω := by
  rw [← sourceH_second_zero hL ω]
  exact sourceH_second_abs_le hL ω 0

/-- Six literal endpoint errors on the actual confluent pin fiber. -/
theorem source_normalized_endpoint_errors {L : ℝ} (hL : L ≠ 0) (r : ℝ)
    (hr : 0 < r) (ω : SmoothSample 2 L)
    (h3 : sourceConfluentPinsAt L r ω 3 = 0)
    (h4 : sourceConfluentPinsAt L r ω 4 = 0)
    (h5 : sourceConfluentPinsAt L r ω 5 = 2) :
    |sourceNormalizedEndpoints L r ω 0 + 1| ≤ r*sourceDerivativeMajorant L 4 ω ∧
    |sourceNormalizedEndpoints L r ω 1 - 1| ≤ r*sourceDerivativeMajorant L 4 ω ∧
    |sourceNormalizedEndpoints L r ω 2 + sourceA L ω/2| ≤ r*sourceDerivativeMajorant L 4 ω ∧
    |sourceNormalizedEndpoints L r ω 3 - sourceA L ω/2| ≤ r*sourceDerivativeMajorant L 4 ω ∧
    |sourceNormalizedEndpoints L r ω 4 - sourceQ L ω| ≤ r*sourceDerivativeMajorant L 3 ω ∧
    |sourceNormalizedEndpoints L r ω 5 - sourceQ L ω| ≤ r*sourceDerivativeMajorant L 3 ω := by
  have hΓ4 := sourceDerivativeMajorant_nonneg L 4 ω
  have hΓ3 := sourceDerivativeMajorant_nonneg L 3 ω
  have hhalf : r*sourceDerivativeMajorant L 4 ω/2 ≤ r*sourceDerivativeMajorant L 4 ω :=
    by nlinarith [mul_nonneg hr.le hΓ4]
  have hpin := pin5_integral (sourceF L ω) (sourceF_C3 hL ω) r hr.ne'
  rw [← source_pin5_eq hL r ω,h5] at hpin
  have hp : 6*(∫ t in (-1/2:ℝ)..(1/2:ℝ),
      peanoCubic t * iteratedDeriv 3 (sourceF L ω) (r*t)) = 2 := hpin.symm
  have hf := cubic_pin_pointwise_error _ (sourceF_third_continuous hL ω)
    _ r hΓ4 hr.le (sourceF_third_lipschitz hL ω) hp
  have hFleft := left_weighted_error _ (sourceF_third_continuous hL ω) r 2
    (r*sourceDerivativeMajorant L 4 ω) hf
  have hFright := right_weighted_error _ (sourceF_third_continuous hL ω) r 2
    (r*sourceDerivativeMajorant L 4 ω) hf
  have hh (t : ℝ) (ht : t ∈ Icc (-1/2:ℝ) (1/2:ℝ)) :
      |iteratedDeriv 2 (sourceH L ω) (r*t)-sourceA L ω| ≤
        r*sourceDerivativeMajorant L 4 ω := by
    have h := scaled_lipschitz_center_error _ _ r hΓ4 hr.le
      (sourceH_second_lipschitz hL ω) t ht
    rw [sourceH_second_zero hL ω] at h
    exact h.trans (by nlinarith [mul_nonneg hr.le hΓ4])
  have hHleft := left_weighted_error _ (sourceH_second_continuous hL ω) r (sourceA L ω)
    (r*sourceDerivativeMajorant L 4 ω) hh
  have hHright := right_weighted_error _ (sourceH_second_continuous hL ω) r (sourceA L ω)
    (r*sourceDerivativeMajorant L 4 ω) hh
  have hq (t : ℝ) (ht : t ∈ Icc (-1/2:ℝ) (1/2:ℝ)) :
      |sourceQCurve L ω (r*t)-sourceQ L ω| ≤ r*sourceDerivativeMajorant L 3 ω := by
    have h := scaled_lipschitz_center_error _ _ r hΓ3 hr.le
      (sourceQCurve_lipschitz hL ω) t ht
    rw [sourceQCurve_zero] at h
    exact h.trans (by nlinarith [mul_nonneg hr.le hΓ3])
  have hQM : |sourceQCurve L ω (-r/2)-sourceQ L ω| ≤ r*sourceDerivativeMajorant L 3 ω := by
    have h := hq (-1/2) (by constructor <;> norm_num)
    have he : r*(-1/2) = -r/2 := by ring
    rw [he] at h
    exact h
  have hQS : |sourceQCurve L ω (r/2)-sourceQ L ω| ≤ r*sourceDerivativeMajorant L 3 ω := by
    have h := hq (1/2) (by constructor <;> norm_num)
    have he : r*(1/2) = r/2 := by ring
    rw [he] at h
    exact h
  rw [source_normalized_peano hL r hr.ne' ω h3 h4]
  change |-(∫ u in (-1/2:ℝ)..(1/2:ℝ), peanoLeft u * iteratedDeriv 3 (sourceF L ω) (r*u))+1| ≤ r*sourceDerivativeMajorant L 4 ω ∧
    |(∫ u in (-1/2:ℝ)..(1/2:ℝ), peanoRight u * iteratedDeriv 3 (sourceF L ω) (r*u))-1| ≤ r*sourceDerivativeMajorant L 4 ω ∧
    |-(∫ u in (-1/2:ℝ)..(1/2:ℝ), peanoLeft u * iteratedDeriv 2 (sourceH L ω) (r*u))+sourceA L ω/2| ≤ r*sourceDerivativeMajorant L 4 ω ∧
    |(∫ u in (-1/2:ℝ)..(1/2:ℝ), peanoRight u * iteratedDeriv 2 (sourceH L ω) (r*u))-sourceA L ω/2| ≤ r*sourceDerivativeMajorant L 4 ω ∧
    |sourceQCurve L ω (-r/2)-sourceQ L ω| ≤ r*sourceDerivativeMajorant L 3 ω ∧
    |sourceQCurve L ω (r/2)-sourceQ L ω| ≤ r*sourceDerivativeMajorant L 3 ω
  refine ⟨?_,?_,?_,?_,hQM,hQS⟩
  · have he : |-(∫ u in (-1/2:ℝ)..(1/2:ℝ), peanoLeft u *
        iteratedDeriv 3 (sourceF L ω) (r*u))+1| =
        |(∫ u in (-1/2:ℝ)..(1/2:ℝ), peanoLeft u *
        iteratedDeriv 3 (sourceF L ω) (r*u))-2/2| := by
      rw [show (2:ℝ)/2=1 by norm_num,← abs_neg]; congr 1; ring
    rw [he]
    exact hFleft.trans hhalf
  · rw [show (2:ℝ)/2=1 by norm_num] at hFright
    exact hFright.trans hhalf
  · have he : |-(∫ u in (-1/2:ℝ)..(1/2:ℝ), peanoLeft u *
        iteratedDeriv 2 (sourceH L ω) (r*u))+sourceA L ω/2| =
        |(∫ u in (-1/2:ℝ)..(1/2:ℝ), peanoLeft u *
        iteratedDeriv 2 (sourceH L ω) (r*u))-sourceA L ω/2| := by
      rw [← abs_neg]; congr 1; ring
    rw [he]
    exact hHleft.trans hhalf
  · exact hHright.trans hhalf

theorem sourceGammaRadius_ge_third_fourth (L : ℝ) (ω : SmoothSample 2 L) :
    1+sourceDerivativeMajorant L 3 ω+sourceDerivativeMajorant L 4 ω ≤ sourceGammaRadius L ω := by
  have h0 := sourceDerivativeMajorant_nonneg L 0 ω
  have h1 := sourceDerivativeMajorant_nonneg L 1 ω
  have h2 := sourceDerivativeMajorant_nonneg L 2 ω
  have h5 := sourceDerivativeMajorant_nonneg L 5 ω
  unfold sourceGammaRadius
  simp only [Fin.sum_univ_succ]
  change 1+sourceDerivativeMajorant L 3 ω+sourceDerivativeMajorant L 4 ω ≤
    1+(sourceDerivativeMajorant L 0 ω+(sourceDerivativeMajorant L 1 ω+
      (sourceDerivativeMajorant L 2 ω+(sourceDerivativeMajorant L 3 ω+
        (sourceDerivativeMajorant L 4 ω+(sourceDerivativeMajorant L 5 ω+0))))))
  linarith

theorem source_normalized_endpoint_first_four_bounds {L : ℝ} (hL : L ≠ 0) (r : ℝ)
    (hr : 0 < r) (hr1 : r ≤ 1) (ω : SmoothSample 2 L)
    (h3 : sourceConfluentPinsAt L r ω 3 = 0)
    (h4 : sourceConfluentPinsAt L r ω 4 = 0)
    (h5 : sourceConfluentPinsAt L r ω 5 = 2) :
    ∀ i : Fin 4, |sourceNormalizedEndpoints L r ω i.castSucc.castSucc| ≤ sourceGammaRadius L ω := by
  obtain ⟨h0,h1,h2,h3',_,_⟩ := source_normalized_endpoint_errors hL r hr ω h3 h4 h5
  have hΓ4 := sourceDerivativeMajorant_nonneg L 4 ω
  have hΓ3 := sourceDerivativeMajorant_nonneg L 3 ω
  have hA := sourceA_abs_le hL ω
  have hR := sourceGammaRadius_ge_third_fourth L ω
  have he : r*sourceDerivativeMajorant L 4 ω ≤ sourceDerivativeMajorant L 4 ω :=
    mul_le_of_le_one_left hΓ4 hr1
  intro i
  fin_cases i
  · have hh := abs_add_le (sourceNormalizedEndpoints L r ω 0+1) (-1)
    norm_num at hh
    have heq : sourceNormalizedEndpoints L r ω 0+1+-1=sourceNormalizedEndpoints L r ω 0 := by ring
    exact hh.trans (by linarith)
  · have hh := abs_add_le (sourceNormalizedEndpoints L r ω 1-1) 1
    norm_num at hh
    have heq : sourceNormalizedEndpoints L r ω 1-1+1=sourceNormalizedEndpoints L r ω 1 := by ring
    exact hh.trans (by linarith)
  · have hh := abs_add_le (sourceNormalizedEndpoints L r ω 2+sourceA L ω/2) (-sourceA L ω/2)
    have heq : sourceNormalizedEndpoints L r ω 2+sourceA L ω/2+-sourceA L ω/2=
        sourceNormalizedEndpoints L r ω 2 := by ring
    rw [heq,abs_div,abs_neg] at hh
    norm_num at hh
    exact hh.trans (by linarith)
  · have hh := abs_add_le (sourceNormalizedEndpoints L r ω 3-sourceA L ω/2) (sourceA L ω/2)
    have heq : sourceNormalizedEndpoints L r ω 3-sourceA L ω/2+sourceA L ω/2=
        sourceNormalizedEndpoints L r ω 3 := by ring
    rw [heq,abs_div] at hh
    norm_num at hh
    exact hh.trans (by linarith)




theorem sourceQ_measurable {L : ℝ} (hL : L ≠ 0) : Measurable (sourceQ L) := by
  have he : sourceQ L = fun ω => scalarSeries
      (derivativeCoefficient 2 L 2 0 ![directionY,directionY]) (sampleInclusion 2 L ω) := by
    funext ω
    exact smoothSourceField_derivative_series 2 hL ω 2 0 _
  rw [he]
  exact (scalarSeries_measurable _).comp (sampleInclusion_measurable 2 L)

theorem sourceA_measurable {L : ℝ} (hL : L ≠ 0) : Measurable (sourceA L) := by
  have he : sourceA L = fun ω => scalarSeries
      (derivativeCoefficient 2 L 3 0 ![directionX,directionX,directionY]) (sampleInclusion 2 L ω) := by
    funext ω
    exact smoothSourceField_derivative_series 2 hL ω 3 0 _
  rw [he]
  exact (scalarSeries_measurable _).comp (sampleInclusion_measurable 2 L)

theorem source_normalized_determinant_bounds {L : ℝ} (hL : L ≠ 0) (r : ℝ)
    (hr : 0 < r) (hr1 : r ≤ 1) (ω : SmoothSample 2 L)
    (h3 : sourceConfluentPinsAt L r ω 3 = 0)
    (h4 : sourceConfluentPinsAt L r ω 4 = 0)
    (h5 : sourceConfluentPinsAt L r ω 5 = 2) :
    |sourceNormalizedEndpoints L r ω 0*sourceNormalizedEndpoints L r ω 4-
      r*sourceNormalizedEndpoints L r ω 2^2| ≤
      sourceGammaRadius L ω*|sourceQ L ω|+2*r*sourceGammaRadius L ω^2 ∧
    |sourceNormalizedEndpoints L r ω 1*sourceNormalizedEndpoints L r ω 5-
      r*sourceNormalizedEndpoints L r ω 3^2| ≤
      sourceGammaRadius L ω*|sourceQ L ω|+2*r*sourceGammaRadius L ω^2 := by
  have hv := source_normalized_endpoint_first_four_bounds hL r hr hr1 ω h3 h4 h5
  obtain ⟨_,_,_,_,hM,hS⟩ := source_normalized_endpoint_errors hL r hr ω h3 h4 h5
  have hΓ : sourceDerivativeMajorant L 3 ω ≤ sourceGammaRadius L ω :=
    sourceDerivativeMajorant_le_radius L ω 3
  have hM' := hM.trans (mul_le_mul_of_nonneg_left hΓ hr.le)
  have hS' := hS.trans (mul_le_mul_of_nonneg_left hΓ hr.le)
  exact ⟨endpoint_det_abs_le r _ _ hr.le (sourceGammaRadius_nonneg L ω) _ _ _
      (hv 0) (hv 2) hM',
    endpoint_det_abs_le r _ _ hr.le (sourceGammaRadius_nonneg L ω) _ _ _
      (hv 1) (hv 3) hS'⟩

/-- The physical strict-type determinant weight of the actual field has the
curvature bound, including its zero-type boundary. -/
theorem sourceSmoothWeight_curvature_bound {L : ℝ} (hL : L ≠ 0) (r : ℝ)
    (hr : 0 < r) (hr1 : r ≤ 1) (ω : SmoothSample 2 L)
    (h3 : sourceConfluentPinsAt L r ω 3 = 0)
    (h4 : sourceConfluentPinsAt L r ω 4 = 0)
    (h5 : sourceConfluentPinsAt L r ω 5 = 2) :
    sourceSmoothWeight L r ω ≤
      2*r^2*sourceGammaRadius L ω^2*sourceQ L ω^2+8*r^4*sourceGammaRadius L ω^4 := by
  have hv := source_normalized_endpoint_first_four_bounds hL r hr hr1 ω h3 h4 h5
  obtain ⟨_,_,_,_,hM,hS⟩ := source_normalized_endpoint_errors hL r hr ω h3 h4 h5
  have hΓ : sourceDerivativeMajorant L 3 ω ≤ sourceGammaRadius L ω :=
    sourceDerivativeMajorant_le_radius L ω 3
  rw [sourceSmoothWeight_eq L r hr.ne' ω]
  exact endpointWeight_curvature_le r _ _ hr.le (sourceGammaRadius_nonneg L ω) _
    (hv 0) (hv 1) (hv 2) (hv 3)
    (hM.trans (mul_le_mul_of_nonneg_left hΓ hr.le))
    (hS.trans (mul_le_mul_of_nonneg_left hΓ hr.le))

theorem source_positive_weight_curvature_upper {L : ℝ} (hL : L ≠ 0) (r : ℝ)
    (hr : 0 < r) (ω : SmoothSample 2 L)
    (h3 : sourceConfluentPinsAt L r ω 3 = 0)
    (h4 : sourceConfluentPinsAt L r ω 4 = 0)
    (h5 : sourceConfluentPinsAt L r ω 5 = 2)
    (hW : 0 < sourceSmoothWeight L r ω) :
    sourceQ L ω < r*sourceDerivativeMajorant L 3 ω := by
  have ht := (sourceSmoothWeight_pos_iff L r ω).mp hW
  have hneg : sourceNormalizedEndpoints L r ω 4 < 0 := by
    apply strict_endpoint_transverse_neg r _
    rw [← sourceRawHM_eq_normalized L r hr.ne' ω]
    exact ht.1
  have herror := (source_normalized_endpoint_errors hL r hr ω h3 h4 h5).2.2.2.2.1
  have hlow := (abs_le.mp herror).1
  linarith

theorem source_bad_curvature_slab {L : ℝ} (hL : L ≠ 0) (r : ℝ)
    (hr : 0 < r) (ω : SmoothSample 2 L)
    (h3 : sourceConfluentPinsAt L r ω 3 = 0)
    (h4 : sourceConfluentPinsAt L r ω 4 = 0)
    (h5 : sourceConfluentPinsAt L r ω 5 = 2)
    (hW : 0 < sourceSmoothWeight L r ω) (K : ℝ)
    (hq : -K*r*sourceGammaRadius L ω^5 ≤ sourceQ L ω) :
    |sourceQ L ω| ≤ max K 1*r*sourceGammaRadius L ω^5 :=
  curvature_slab_of_upper _ _ _ _ K hr.le (one_le_sourceGammaRadius L ω)
    (sourceDerivativeMajorant_le_radius L ω 3)
    (source_positive_weight_curvature_upper hL r hr ω h3 h4 h5 hW) hq

/-- The completed actual all-pin support supplies the three pin equations. -/
theorem source_prescribed_pin_constraints_ae {L : ℝ} (hL : L ≠ 0) (r b : ℝ)
    (hG : IsUnit (sourcePinCovarianceAt L r)) :
    ∀ᵐ ω ∂sourceSmoothLaw hL r b,
      sourceConfluentPinsAt L r ω 3 = 0 ∧ sourceConfluentPinsAt L r ω 4 = 0 ∧
      sourceConfluentPinsAt L r ω 5 = 2 := by
  have hm : MeasurableSet {ω : SmoothSample 2 L |
      sourceConfluentPinsAt L r ω = sourcePrescribedPins r b} :=
    measurableSet_eq_fun (sourceConfluentPinsAt_measurable hL r) measurable_const
  have hp : ∀ᵐ ω ∂sourceSmoothLaw hL r b,
      sourceConfluentPinsAt L r ω = sourcePrescribedPins r b := by
    apply (mem_ae_iff_prob_eq_one hm).2
    exact sourceSmoothKernel_pin_fiber hL r hG (sourcePrescribedPins r b)
  filter_upwards [hp] with ω hω
  exact ⟨by simpa [sourcePrescribedPins] using congrFun hω 3,
    by simpa [sourcePrescribedPins] using congrFun hω 4,
    by simpa [sourcePrescribedPins] using congrFun hω 5⟩

theorem sourceSmoothLaw_curvature_bound_ae {L : ℝ} (hL : L ≠ 0) (r b : ℝ)
    (hr : 0 < r) (hr1 : r ≤ 1) (hG : IsUnit (sourcePinCovarianceAt L r)) :
    ∀ᵐ ω ∂sourceSmoothLaw hL r b,
      sourceSmoothWeight L r ω ≤
        2*r^2*sourceGammaRadius L ω^2*sourceQ L ω^2+8*r^4*sourceGammaRadius L ω^4 ∧
      (∀ K : ℝ, 0 < sourceSmoothWeight L r ω →
        -K*r*sourceGammaRadius L ω^5 ≤ sourceQ L ω →
        |sourceQ L ω| ≤ max K 1*r*sourceGammaRadius L ω^5) := by
  filter_upwards [source_prescribed_pin_constraints_ae hL r b hG] with ω hω
  exact ⟨sourceSmoothWeight_curvature_bound hL r hr hr1 ω hω.1 hω.2.1 hω.2.2,
    fun K hW hq => source_bad_curvature_slab hL r hr ω hω.1 hω.2.1 hω.2.2 hW K hq⟩

/-- Only the actual nonzero period and fixed height remain as model premises;
current covariance invertibility and all-pin support are derived upstream. -/
theorem source_curvature_estimates {L : ℝ} (hL : L ≠ 0) (b : ℝ) :
    ∃ δ : ℝ, 0 < δ ∧ δ ≤ 1 ∧ ∀ r : ℝ, 0 < r → r < δ →
      ∀ᵐ ω ∂sourceSmoothLaw hL r b,
        sourceSmoothWeight L r ω ≤
          2*r^2*sourceGammaRadius L ω^2*sourceQ L ω^2+8*r^4*sourceGammaRadius L ω^4 ∧
        (∀ K : ℝ, 0 < sourceSmoothWeight L r ω →
          -K*r*sourceGammaRadius L ω^5 ≤ sourceQ L ω →
          |sourceQ L ω| ≤ max K 1*r*sourceGammaRadius L ω^5) := by
  obtain ⟨δ,hδ,hsub⟩ := mem_nhdsGT_iff_exists_Ioo_subset.mp
    (sourceEndpoint_parameter_limits hL b).1
  refine ⟨min δ 1,lt_min hδ (by norm_num),min_le_right _ _,?_⟩
  intro r hr hrδ
  exact sourceSmoothLaw_curvature_bound_ae hL r b hr
    (hrδ.le.trans (min_le_right _ _))
    (hsub ⟨hr,lt_of_lt_of_le hrδ (min_le_left _ _)⟩)

/-- Literal centers in LM006 endpoint order, retaining the actual mixed third
derivative and the actual transverse curvature. -/
def sourceEndpointCenters (L : ℝ) (ω : SmoothSample 2 L) : Fin 6 → ℝ :=
  ![-1,1,-(sourceA L ω/2),sourceA L ω/2,sourceQ L ω,sourceQ L ω]

def sourceEndpointErrorOrder (i : Fin 6) : ℕ := if (i : ℕ) < 4 then 4 else 3

theorem source_normalized_endpoint_errors_all {L : ℝ} (hL : L ≠ 0) (r : ℝ)
    (hr : 0 < r) (ω : SmoothSample 2 L)
    (h3 : sourceConfluentPinsAt L r ω 3 = 0)
    (h4 : sourceConfluentPinsAt L r ω 4 = 0)
    (h5 : sourceConfluentPinsAt L r ω 5 = 2) :
    ∀ i : Fin 6, |sourceNormalizedEndpoints L r ω i-sourceEndpointCenters L ω i| ≤
      r*sourceDerivativeMajorant L (sourceEndpointErrorOrder i) ω := by
  obtain ⟨h0,h1,h2,h3',h4',h5'⟩ := source_normalized_endpoint_errors hL r hr ω h3 h4 h5
  intro i
  fin_cases i
  · simpa [sourceEndpointCenters,sourceEndpointErrorOrder] using h0
  · simpa [sourceEndpointCenters,sourceEndpointErrorOrder] using h1
  · simpa [sourceEndpointCenters,sourceEndpointErrorOrder] using h2
  · simpa [sourceEndpointCenters,sourceEndpointErrorOrder] using h3'
  · simpa [sourceEndpointCenters,sourceEndpointErrorOrder] using h4'
  · simpa [sourceEndpointCenters,sourceEndpointErrorOrder] using h5'

theorem sourceSmoothLaw_endpoint_errors_ae {L : ℝ} (hL : L ≠ 0) (r b : ℝ)
    (hr : 0 < r) (hG : IsUnit (sourcePinCovarianceAt L r)) :
    ∀ᵐ ω ∂sourceSmoothLaw hL r b, ∀ i : Fin 6,
      |sourceNormalizedEndpoints L r ω i-sourceEndpointCenters L ω i| ≤
        r*sourceDerivativeMajorant L (sourceEndpointErrorOrder i) ω := by
  filter_upwards [source_prescribed_pin_constraints_ae hL r b hG] with ω hω
  exact source_normalized_endpoint_errors_all hL r hr ω hω.1 hω.2.1 hω.2.2

theorem source_endpoint_error_estimates {L : ℝ} (hL : L ≠ 0) (b : ℝ) :
    ∃ δ : ℝ, 0 < δ ∧ δ ≤ 1 ∧ ∀ r : ℝ, 0 < r → r < δ →
      ∀ᵐ ω ∂sourceSmoothLaw hL r b, ∀ i : Fin 6,
        |sourceNormalizedEndpoints L r ω i-sourceEndpointCenters L ω i| ≤
          r*sourceDerivativeMajorant L (sourceEndpointErrorOrder i) ω := by
  obtain ⟨δ,hδ,hsub⟩ := mem_nhdsGT_iff_exists_Ioo_subset.mp
    (sourceEndpoint_parameter_limits hL b).1
  refine ⟨min δ 1,lt_min hδ (by norm_num),min_le_right _ _,?_⟩
  intro r hr hrδ
  exact sourceSmoothLaw_endpoint_errors_ae hL r b hr
    (hsub ⟨hr,lt_of_lt_of_le hrδ (min_le_left _ _)⟩)

end I4SourcePinCurvatureBounds
