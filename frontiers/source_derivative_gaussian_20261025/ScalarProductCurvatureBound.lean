import Mathlib.MeasureTheory.Integral.Prod
import Mathlib.MeasureTheory.Constructions.BorelSpace.Real
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Ring
import Mathlib.Tactic.GCongr
import Mathlib.Tactic.Linarith

/-!
# Scalar density times residual integration at cubic curvature scale

An honest scalar interval-mass bound and a residual seventeenth moment turn
an O(r S⁵) tube with O(r⁴ S¹²) weight into an O(r⁵) numerator. The scalar and
residual measure are a literal product; no Gaussian mean or independence
conclusion is assumed for an actual source here.
See SOURCE_WEIGHTED_CURVATURE_BOUND.md for the frozen source contract.
-/

noncomputable section
open MeasureTheory Set
open scoped ENNReal
set_option autoImplicit false

namespace I4ScalarProductCurvature

/- Regular-cutoff arithmetic coauthored by /root, supplied as compiled scratch
CurvatureCutoff.lean; proof authorship is separate from independent review. -/
theorem regular_bounds {A K eps S R q r : ℝ}
    (hA : 0 ≤ A) (hK : 0 ≤ K) (heps : 0 ≤ eps) (hr : 0 ≤ r)
    (hS : 1 ≤ S) (hR : 0 ≤ R) (hdom : R ≤ A * (|q| + S))
    (hcut : r * R^5 ≤ eps) (hslab : |q| ≤ K * r * R^5) :
    let D := A * (1 + K * eps)
    R ≤ D * S ∧ |q| ≤ K * D^5 * r * S^5 ∧
      2*r^2*R^2*q^2 + 8*r^4*R^4 ≤
        (2*K^2*D^12 + 8*D^4)*r^4*S^12 := by
  dsimp only
  let D := A * (1 + K * eps)
  have hS0 : 0 ≤ S := le_trans (by norm_num) hS
  have hD : 0 ≤ D := by dsimp [D]; positivity
  have hqeps : |q| ≤ K * eps := calc
    |q| ≤ K * r * R^5 := hslab
    _ = K * (r * R^5) := by ring
    _ ≤ K * eps := mul_le_mul_of_nonneg_left hcut hK
  have hsmall : |q| + S ≤ (1 + K * eps) * S := by nlinarith [mul_nonneg hK heps, mul_le_mul_of_nonneg_left hS (mul_nonneg hK heps)]
  have hRD : R ≤ D * S := calc
    R ≤ A * (|q| + S) := hdom
    _ ≤ A * ((1 + K * eps) * S) := mul_le_mul_of_nonneg_left hsmall hA
    _ = D * S := by dsimp [D]; ring
  have hq : |q| ≤ K * D^5 * r * S^5 := calc
    |q| ≤ K * r * R^5 := hslab
    _ ≤ K * r * (D*S)^5 := by gcongr
    _ = K * D^5 * r * S^5 := by ring
  have hweight : 2*r^2*R^2*q^2 + 8*r^4*R^4 ≤
      2*r^2*(D*S)^2*(K*D^5*r*S^5)^2 + 8*r^4*(D*S)^4 := by
    rw [← sq_abs q]
    gcongr
  have hS4 : S^4 ≤ S^12 := by
    calc
      S^4 ≤ S^4 * S^8 := le_mul_of_one_le_right (pow_nonneg hS0 _) (one_le_pow₀ hS)
      _ = S^12 := by ring
  refine ⟨hRD, hq, ?_⟩
  calc
    2*r^2*R^2*q^2 + 8*r^4*R^4 ≤
        2*r^2*(D*S)^2*(K*D^5*r*S^5)^2 + 8*r^4*(D*S)^4 := hweight
    _ = 2*K^2*D^12*r^4*S^12 + 8*D^4*r^4*S^4 := by ring
    _ ≤ 2*K^2*D^12*r^4*S^12 + 8*D^4*r^4*S^12 := by gcongr
    _ = (2*K^2*D^12 + 8*D^4)*r^4*S^12 := by ring



/-- The product calculation behind the regular curvature slab estimate.
The interval-mass premise is the direct consequence of a scalar density bound.
It is uniform in the scalar mean, which is not replaced by zero. -/
theorem scalar_product_tube_integral_bound {E : Type*} [MeasurableSpace E]
    (ν : Measure ℝ) [IsProbabilityMeasure ν] (μ : Measure E) [IsProbabilityMeasure μ]
    (S : E → ℝ) (hS : ∀ z, 0 ≤ S z)
    (hS17 : Integrable (fun z => S z ^ 17) μ)
    (e : Set (ℝ × E)) (he : MeasurableSet e)
    (F : ℝ × E → ℝ) (hF : Integrable F (ν.prod μ))
    (r H C M : ℝ) (hr : 0 ≤ r) (hH : 0 ≤ H) (hC : 0 ≤ C) (_hM : 0 ≤ M)
    (hdensity : ∀ a : ℝ, 0 ≤ a → ν.real (Icc (-a) a) ≤ 2 * M * a)
    (htube : ∀ p ∈ e, |p.1| ≤ H * r * S p.2 ^ 5)
    (hweight : ∀ p ∈ e, F p ≤ C * r ^ 4 * S p.2 ^ 12) :
    (∫ p in e, F p ∂ν.prod μ) ≤
      (2 * M * H * C) * r ^ 5 * ∫ z, S z ^ 17 ∂μ := by
  let f := e.indicator F
  have hf : Integrable f (ν.prod μ) := hF.indicator he
  have hinner (z : E) (hi : Integrable (fun q => f (q,z)) ν) :
      (∫ q, f (q,z) ∂ν) ≤ (2 * M * H * C) * r ^ 5 * S z ^ 17 := by
    let a := H * r * S z ^ 5
    let B := C * r ^ 4 * S z ^ 12
    have ha : 0 ≤ a := mul_nonneg (mul_nonneg hH hr) (pow_nonneg (hS z) 5)
    have hB : 0 ≤ B := mul_nonneg (mul_nonneg hC (pow_nonneg hr 4)) (pow_nonneg (hS z) 12)
    have hmajor : Integrable ((Icc (-a) a).indicator (fun _ : ℝ => B)) ν :=
      (integrable_const B).indicator measurableSet_Icc
    have hpoint (q : ℝ) : f (q,z) ≤ (Icc (-a) a).indicator (fun _ : ℝ => B) q := by
      by_cases hp : (q,z) ∈ e
      · have hqa : q ∈ Icc (-a) a := abs_le.mp (htube (q,z) hp)
        rw [Set.indicator_of_mem hqa]
        exact (show f (q,z) = F (q,z) from Set.indicator_of_mem hp F).trans_le
          (hweight (q,z) hp)
      · rw [show f (q,z) = 0 from Set.indicator_of_notMem hp F]
        exact Set.indicator_nonneg (fun _ _ => hB) q
    calc
      _ ≤ ∫ q, (Icc (-a) a).indicator (fun _ : ℝ => B) q ∂ν :=
        integral_mono hi hmajor hpoint
      _ = ν.real (Icc (-a) a) * B := by
        rw [integral_indicator measurableSet_Icc, setIntegral_const, smul_eq_mul]
      _ ≤ (2 * M * a) * B := mul_le_mul_of_nonneg_right (hdensity a ha) hB
      _ = _ := by dsimp [a,B]; ring
  rw [← integral_indicator he, integral_prod_symm f hf]
  calc
    _ ≤ ∫ z, (2 * M * H * C) * r ^ 5 * S z ^ 17 ∂μ := by
      apply integral_mono_ae hf.integral_prod_right (hS17.const_mul _)
      filter_upwards [hf.prod_left_ae] with z hz
      exact hinner z hz
    _ = _ := integral_const_mul _ _

/-- The regular cutoff supplies the tube and twelfth-power weight bounds
required by the product integration theorem. All density and law hypotheses
remain explicit; applications must derive them for their actual scalar law. -/
theorem scalar_product_regular_integral_bound {E : Type*} [MeasurableSpace E]
    (ν : Measure ℝ) [IsProbabilityMeasure ν] (μ : Measure E) [IsProbabilityMeasure μ]
    (S : E → ℝ) (hS : ∀ z, 1 ≤ S z)
    (hS17 : Integrable (fun z => S z ^ 17) μ)
    (R : ℝ × E → ℝ) (hR : ∀ p, 0 ≤ R p)
    (e : Set (ℝ × E)) (he : MeasurableSet e)
    (F : ℝ × E → ℝ) (hF : Integrable F (ν.prod μ))
    (r A K eps M : ℝ) (hr : 0 ≤ r) (hA : 0 ≤ A) (hK : 0 ≤ K)
    (heps : 0 ≤ eps) (hM : 0 ≤ M)
    (hdensity : ∀ a : ℝ, 0 ≤ a → ν.real (Icc (-a) a) ≤ 2 * M * a)
    (hdom : ∀ p ∈ e, R p ≤ A * (|p.1| + S p.2))
    (hcut : ∀ p ∈ e, r * R p ^ 5 ≤ eps)
    (hslab : ∀ p ∈ e, |p.1| ≤ K * r * R p ^ 5)
    (hweight : ∀ p ∈ e, F p ≤ 2 * r ^ 2 * R p ^ 2 * p.1 ^ 2 +
      8 * r ^ 4 * R p ^ 4) :
    let D := A * (1 + K * eps)
    (∫ p in e, F p ∂ν.prod μ) ≤
      (2 * M * (K * D ^ 5) * (2 * K ^ 2 * D ^ 12 + 8 * D ^ 4)) *
        r ^ 5 * ∫ z, S z ^ 17 ∂μ := by
  dsimp only
  let D := A * (1 + K * eps)
  have hD : 0 ≤ D := by dsimp [D]; positivity
  apply scalar_product_tube_integral_bound ν μ S
    (fun z => le_trans (by norm_num) (hS z)) hS17 e he F hF r (K * D ^ 5)
    (2 * K ^ 2 * D ^ 12 + 8 * D ^ 4) M hr (by positivity) (by positivity) hM hdensity
  · intro p hp
    exact (regular_bounds hA hK heps hr (hS p.2) (hR p) (hdom p hp)
      (hcut p hp) (hslab p hp)).2.1
  · intro p hp
    exact (hweight p hp).trans (regular_bounds hA hK heps hr (hS p.2) (hR p)
      (hdom p hp) (hcut p hp) (hslab p hp)).2.2

end I4ScalarProductCurvature
