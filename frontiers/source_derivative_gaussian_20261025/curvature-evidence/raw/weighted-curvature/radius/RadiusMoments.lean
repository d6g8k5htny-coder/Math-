import SourceConditionalMajorant

noncomputable section
open I4Foundation I4Source I4Weights I4Smooth I4SmoothCarrier I4SourceConditionalMajorant
open I4SourceSmoothConditional I4SourceEndpointRegression I4SourceSmoothPalm
open MeasureTheory ProbabilityTheory Filter
open scoped BigOperators Topology
set_option autoImplicit false

namespace I4SourcePinCurvatureBounds

def sourceGammaRadius (L : ℝ) (ω : SmoothSample 2 L) : ℝ :=
  1 + ∑ k : Fin 6, sourceDerivativeMajorant L (k : ℕ) ω

lemma sourceGammaRadius_measurable (L : ℝ) : Measurable (sourceGammaRadius L) := by
  unfold sourceGammaRadius
  exact measurable_const.add (Finset.measurable_sum _ (fun k _ => sourceDerivativeMajorant_measurable L k))

lemma one_le_sourceGammaRadius (L : ℝ) (ω : SmoothSample 2 L) :
    1 ≤ sourceGammaRadius L ω := by
  have h (k : Fin 6) : 0 ≤ sourceDerivativeMajorant L (k : ℕ) ω :=
    sampleMajorant_nonneg _ (orderModeBound_nonneg _ 2 L) ω
  exact le_add_of_nonneg_right (Finset.sum_nonneg (fun k _ => h k))

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

end I4SourcePinCurvatureBounds
