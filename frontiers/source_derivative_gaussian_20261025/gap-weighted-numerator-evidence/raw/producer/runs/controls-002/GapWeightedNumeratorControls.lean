import SourceGapWeightedNumerator

noncomputable section
open I4SmoothCarrier I4SourceSmoothConditional I4SourceSmoothPalm
open I4SourcePinCurvatureBounds I4SourceCompactTargetMoments
open I4SourceWeightedCurvature I4SourceGapWeightedNumerator
open MeasureTheory Set

set_option autoImplicit false

namespace GapWeightedNumeratorControls

/-- The integrability interval precedes every real height and gap mark. -/
theorem hL_only_integrability {L : ℝ} (hL : L ≠ 0) :
    ∃ δ : ℝ, 0 < δ ∧ δ ≤ 1 ∧ ∀ r : ℝ, 0 < r → r < δ → ∀ b k : ℝ,
      Integrable (sourceSmoothWeight L r) (sourceGapLaw hL r b k) :=
  sourceGapLaw_weight_integrable hL

/-- The closed endpoint retains its exact actual bad union and both integrabilities. -/
theorem generic_compact_endpoint {L : ℝ} (hL : L ≠ 0)
    (B K A eps : ℝ) (hB : 0 ≤ B) (hK : 0 ≤ K) (hA : 0 ≤ A) (heps : 0 < eps) :
    ∃ N δ : ℝ, 0 ≤ N ∧ 0 < δ ∧ δ ≤ 1 ∧
      ∀ r : ℝ, 0 < r → r < δ → ∀ b k : ℝ, |b| ≤ B → |k| ≤ K →
        Integrable (sourceSmoothWeight L r) (sourceGapLaw hL r b k) ∧
        IntegrableOn (sourceSmoothWeight L r)
          (sourceRegularityBad L r eps ∪ sourceCurvatureOneSided L r A)
          (sourceGapLaw hL r b k) ∧
        (∫ ω in sourceRegularityBad L r eps ∪ sourceCurvatureOneSided L r A,
          sourceSmoothWeight L r ω ∂sourceGapLaw hL r b k) ≤ N*r^5 :=
  sourceGapLaw_bad_union_numerator hL B K A eps hB hK hA heps

/-- A literal negative period, height 3 and nondefault gap 2 survive specialization. -/
theorem negative_period_height3_gap2 :
    ∃ N δ : ℝ, 0 ≤ N ∧ 0 < δ ∧ δ ≤ 1 ∧ ∀ r : ℝ, 0 < r → r < δ →
      Integrable (sourceSmoothWeight (-1) r) (sourceGapLaw (by norm_num : (-1:ℝ) ≠ 0) r 3 2) ∧
      IntegrableOn (sourceSmoothWeight (-1) r)
        (sourceRegularityBad (-1) r 1 ∪ sourceCurvatureOneSided (-1) r 4)
        (sourceGapLaw (by norm_num : (-1:ℝ) ≠ 0) r 3 2) ∧
      (∫ ω in sourceRegularityBad (-1) r 1 ∪ sourceCurvatureOneSided (-1) r 4,
        sourceSmoothWeight (-1) r ω ∂sourceGapLaw (by norm_num : (-1:ℝ) ≠ 0) r 3 2) ≤ N*r^5 := by
  obtain ⟨N,δ,hN,hδ,hδ1,hbound⟩ := sourceGapLaw_bad_union_numerator
    (by norm_num : (-1:ℝ) ≠ 0) 3 2 4 1 (by norm_num) (by norm_num) (by norm_num) (by norm_num)
  exact ⟨N,δ,hN,hδ,hδ1,fun r hr hrδ => hbound r hr hrδ 3 2 (by norm_num) (by norm_num)⟩

theorem nondefault_literal_target (r : ℝ) :
    sourceGapPins r 3 2 = ![3-r^3,0,0,0,0,24] := by
  ext i
  fin_cases i <;> (simp [sourceGapPins]; ring)

theorem exact_actual_bad_union (L r A eps : ℝ) :
    sourceRegularityBad L r eps ∪ sourceCurvatureOneSided L r A =
      {ω : SmoothSample 2 L | eps < r*sourceGammaRadius L ω^5 ∨
        -A*r*sourceGammaRadius L ω^5 ≤ sourceQ L ω} := rfl

theorem actual_bad_union_measurable {L : ℝ} (hL : L ≠ 0) (r A eps : ℝ) :
    MeasurableSet (sourceRegularityBad L r eps ∪ sourceCurvatureOneSided L r A) :=
  (sourceRegularityBad_measurable L r eps).union (sourceCurvatureOneSided_measurable hL r A)

/-- Markov uses the thirtieth moment at the actual gap law and keeps r^6. -/
theorem actual_gamma30_sixth_power {L : ℝ} (hL : L ≠ 0)
    (r b k eps M : ℝ) (hr : 0 < r) (heps : 0 < eps)
    (hint : Integrable (fun ω => sourceGammaRadius L ω^30) (sourceGapLaw hL r b k))
    (hb : (∫ ω, sourceGammaRadius L ω^30 ∂sourceGapLaw hL r b k) ≤ M) :
    (sourceGapLaw hL r b k).real (sourceRegularityBad L r eps) ≤ (M/eps^6)*r^6 :=
  sourceGapLaw_regularity_base_bound hL r b k eps M hr heps hint hb

/-- Every compact moment has one shared interval before n and its own Cn. -/
theorem compact_moment_order {L : ℝ} (hL : L ≠ 0)
    (B K : ℝ) (hB : 0 ≤ B) (hK : 0 ≤ K) :
    ∃ δ : ℝ, 0 < δ ∧ δ ≤ 1 ∧ ∀ n : ℕ, ∃ C : ℝ, 0 ≤ C ∧
      ∀ r : ℝ, 0 < r → r < δ → ∀ b k : ℝ, |b| ≤ B → |k| ≤ K →
        Integrable (fun ω => sourceGammaRadius L ω^n) (sourceGapLaw hL r b k) ∧
        (∫ ω, sourceGammaRadius L ω^n ∂sourceGapLaw hL r b k) ≤ C :=
  sourceGapLaw_compact_moments hL B K hB hK

/-- The tail export includes actual physical W-square integrability. -/
theorem tail_square_and_fifth_power {L : ℝ} (hL : L ≠ 0)
    (B K eps : ℝ) (hB : 0 ≤ B) (hK : 0 ≤ K) (heps : 0 < eps) :
    ∃ N δ : ℝ, 0 ≤ N ∧ 0 < δ ∧ δ ≤ 1 ∧
      ∀ r : ℝ, 0 < r → r < δ → ∀ b k : ℝ, |b| ≤ B → |k| ≤ K →
        Integrable (fun ω => sourceSmoothWeight L r ω^2) (sourceGapLaw hL r b k) ∧
        (∫ ω in sourceRegularityBad L r eps, sourceSmoothWeight L r ω
          ∂sourceGapLaw hL r b k) ≤ N*r^5 :=
  sourceGapLaw_regularity_numerator hL B K eps hB hK heps

/-- The regular product result applies at the same literal varying gap law. -/
theorem regular_fifth_power {L : ℝ} (hL : L ≠ 0)
    (B K A eps : ℝ) (hB : 0 ≤ B) (hK : 0 ≤ K) (hA : 0 ≤ A) (heps : 0 < eps) :
    ∃ N δ : ℝ, 0 ≤ N ∧ 0 < δ ∧ δ ≤ 1 ∧
      ∀ r : ℝ, 0 < r → r < δ → ∀ b k : ℝ, |b| ≤ B → |k| ≤ K →
        (∫ ω in sourceRegularCurvatureSlab L r A eps, sourceSmoothWeight L r ω
          ∂sourceGapLaw hL r b k) ≤ N*r^5 :=
  sourceGapLaw_regular_numerator hL B K A eps hB hK hA heps

/-- Explicitly retain the physical square and exact Gamma eighth power. -/
theorem physical_square_gamma8 (r W Γ : ℝ) (hW : 0 ≤ W) (hb : W ≤ 10*r^2*Γ^4) :
    W^2 ≤ 100*r^4*Γ^8 := by
  have hh := pow_le_pow_left₀ hW hb 2
  convert hh using 1; ring

/-- The exact Holder/Markov powers are 2+3=5. -/
theorem holder_markov_rate (r C T : ℝ) (hr : 0 ≤ r) (hC : 0 ≤ C) (hT : 0 ≤ T) :
    Real.sqrt (C*r^4)*Real.sqrt (T*r^6) = Real.sqrt C*Real.sqrt T*r^5 := by
  rw [Real.sqrt_mul hC,Real.sqrt_mul hT,
    show r^4 = (r^2)^2 by ring,show r^6 = (r^3)^2 by ring,
    Real.sqrt_sq (sq_nonneg r),Real.sqrt_sq (pow_nonneg hr 3)]
  ring

/-- A sole power-erasure mutation has a concrete arithmetic counterexample. -/
theorem wrong_power_counterexample :
    (0:ℝ) < 1/2 ∧ (1/2:ℝ) ≤ 1 ∧ ¬ ((1/2:ℝ)^4 ≤ (1/2:ℝ)^5) := by
  norm_num

end GapWeightedNumeratorControls
