import SourceCurvatureDecomposition

noncomputable section
open I4Foundation I4Source I4Smooth I4SmoothCarrier I4SourceGaussian I4SourceCovariance
open I4SourceDerivativeGaussian I4SourceDerivativeContinuity I4SourceConfluentPins
open I4SourceConfluentLimits I4ContactCoefficientLimits I4SourceEndpointRegression
open I4SourceContact I4SourceSmoothConditional I4SourceConditionalMajorant I4ContactGram
open I4GaussianRegressionLimits I4SourceEndpointEstimates MeasureTheory ProbabilityTheory Matrix Filter
open scoped BigOperators Topology NNReal
set_option autoImplicit false
namespace I4SourceCurvatureDecomposition

def curvatureDirectionEnvelope (L B : ℝ) (m : SourceMode 2) : ℝ :=
  (|curvatureCoefficient L m| + 6*B*confluentModeMajorant L m) *
    ((Real.sqrt (sourceContactSchur L/2))⁻¹ + (Real.sqrt (sourceContactSchur L/2))⁻¹^2)

theorem curvatureDirectionEnvelope_nonneg {L : ℝ} (B : ℝ) (hB : 0 ≤ B)
    (m : SourceMode 2) : 0 ≤ curvatureDirectionEnvelope L B m := by
  unfold curvatureDirectionEnvelope
  have hA := confluentModeMajorant_nonneg L m
  positivity

theorem curvatureDirectionEnvelope_summable {L : ℝ} (hL : L ≠ 0) (B : ℝ) :
    Summable (curvatureDirectionEnvelope L B) := by
  exact ((curvatureCoefficient_summable hL).abs.add
    ((confluentModeMajorant_summable hL).mul_left (6*B))).mul_right _

theorem curvatureDirectionEnvelope_weighted_summable {L : ℝ} (hL : L ≠ 0) (B : ℝ) (n : ℕ) :
    Summable (fun m => orderModeBound n 2 L m * curvatureDirectionEnvelope L B m) :=
  coefficient_product_summable (orderModeBound_summable n 2 hL)
    (curvatureDirectionEnvelope_summable hL B)

theorem curvatureDirection_envelope_at {L : ℝ} (hL : L ≠ 0) (r B : ℝ)
    (hr : r ≠ 0) (hB : 0 ≤ B) (hβ : ∀ i, |curvatureBeta L r i| ≤ B)
    (hτ : sourceContactSchur L/2 ≤ curvatureVariance L r) (m : SourceMode 2) :
    |curvatureDirection L r m| ≤ curvatureDirectionEnvelope L B m ∧
      |curvatureDirection L r m| / curvatureSigma L r ≤ curvatureDirectionEnvelope L B m := by
  let s := Real.sqrt (sourceContactSchur L/2)
  let D := |curvatureCoefficient L m| + 6*B*confluentModeMajorant L m
  have hs : 0 < s := Real.sqrt_pos.mpr (by linarith [sourceContactSchur_pos hL])
  have hσ : s ≤ curvatureSigma L r := Real.sqrt_le_sqrt hτ
  have hσpos : 0 < curvatureSigma L r := hs.trans_le hσ
  have hD : 0 ≤ D := by
    dsimp [D]
    have hA := confluentModeMajorant_nonneg L m
    positivity
  have hres : |curvatureResidualCoefficient L r m| ≤ D := by
    unfold curvatureResidualCoefficient
    calc
      _ ≤ |curvatureCoefficient L m| + |∑ i, curvatureBeta L r i * pinCoefficient L r i m| :=
        abs_sub _ _
      _ ≤ |curvatureCoefficient L m| + ∑ i, |curvatureBeta L r i * pinCoefficient L r i m| :=
        add_le_add le_rfl (Finset.abs_sum_le_sum_abs _ _)
      _ ≤ |curvatureCoefficient L m| + ∑ _i : Fin 6, B*confluentModeMajorant L m := by
        apply add_le_add le_rfl
        apply Finset.sum_le_sum
        intro i _
        rw [abs_mul]
        exact mul_le_mul (hβ i) (pinCoefficient_abs_le hL r hr i m) (abs_nonneg _) hB
      _ = D := by dsimp [D]; simp; ring
  have hdir : |curvatureDirection L r m| ≤ D/s := by
    rw [curvatureDirection, abs_div, abs_of_pos hσpos]
    exact (div_le_div_of_nonneg_right hres hσpos.le).trans
      (div_le_div_of_nonneg_left hD hs hσ)
  have hfirst : D/s ≤ curvatureDirectionEnvelope L B m := by
    change D/s ≤ D*(s⁻¹+s⁻¹^2)
    rw [div_eq_mul_inv, mul_add]
    exact le_add_of_nonneg_right (mul_nonneg hD (sq_nonneg _))
  have hsecond : (D/s)/s ≤ curvatureDirectionEnvelope L B m := by
    change (D/s)/s ≤ D*(s⁻¹+s⁻¹^2)
    have heq : (D/s)/s = D*s⁻¹^2 := by ring
    rw [heq, mul_add]
    exact le_add_of_nonneg_left (mul_nonneg hD (inv_nonneg.mpr hs.le))
  refine ⟨hdir.trans hfirst, ?_⟩
  calc
    _ ≤ (D/s)/curvatureSigma L r := div_le_div_of_nonneg_right hdir hσpos.le
    _ ≤ (D/s)/s := div_le_div_of_nonneg_left (div_nonneg hD hs.le) hs hσ
    _ ≤ _ := hsecond

theorem curvatureDirection_uniform_envelope {L : ℝ} (hL : L ≠ 0) (b : ℝ) :
    ∃ δ : ℝ, 0 < δ ∧ δ ≤ 1 ∧ ∃ U : SourceMode 2 → ℝ,
      (∀ m, 0 ≤ U m) ∧ Summable U ∧
      (∀ n : ℕ, Summable (fun m => orderModeBound n 2 L m * U m)) ∧
      ∀ r : ℝ, 0 < r → r < δ → ∀ m,
        |curvatureDirection L r m| ≤ U m ∧
          |curvatureDirection L r m| / curvatureSigma L r ≤ U m := by
  obtain ⟨B,M,δ,hB,_hM,hδ,hδ1,hbound⟩ := curvature_uniform_parameter_bounds hL b
  refine ⟨δ,hδ,hδ1,curvatureDirectionEnvelope L B,
    curvatureDirectionEnvelope_nonneg B hB,curvatureDirectionEnvelope_summable hL B,
    curvatureDirectionEnvelope_weighted_summable hL B,?_⟩
  intro r hr hrδ m
  obtain ⟨_hG,hτ,hβ,_hm⟩ := hbound r hr hrδ
  exact curvatureDirection_envelope_at hL r B (ne_of_gt hr) hB hβ hτ m
end I4SourceCurvatureDecomposition
