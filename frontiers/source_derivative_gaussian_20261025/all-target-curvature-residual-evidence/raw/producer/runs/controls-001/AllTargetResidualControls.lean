import SourceAllTargetCurvatureResidual

noncomputable section
open I4Foundation I4Source I4Smooth I4SmoothCarrier I4SourceContact
open I4SourceEndpointRegression I4SourceSmoothConditional I4SourceConditionalMajorant
open I4SourcePinCurvatureBounds I4SourceSmoothPalm I4SourceConfluentPins
open I4SourceCurvatureDecomposition I4SourceCompactTargetMoments
open I4SourceAllTargetCurvatureResidual MeasureTheory
open scoped BigOperators
set_option autoImplicit false

namespace AllTargetResidualControls

theorem negativePeriodNonzero : (-1 : ℝ) ≠ 0 := by norm_num

theorem literal_radius (r : ℝ) (p : Fin 6 → ℝ) (ρ : SmoothSample 2 (-1)) :
    allTargetCurvatureResidualRadius negativePeriodNonzero r p ρ =
      sourceGammaRadius (-1) (posteriorSample negativePeriodNonzero r p ρ) := rfl

theorem arbitrary_target_measurable (r : ℝ) (p : Fin 6 → ℝ) :
    Measurable (allTargetCurvatureResidualRadius negativePeriodNonzero r p) :=
  allTargetCurvatureResidualRadius_measurable negativePeriodNonzero r p

theorem arbitrary_target_lower_bound (r : ℝ) (p : Fin 6 → ℝ)
    (ρ : SmoothSample 2 (-1)) :
    1 ≤ allTargetCurvatureResidualRadius negativePeriodNonzero r p ρ :=
  one_le_allTargetCurvatureResidualRadius negativePeriodNonzero r p ρ

theorem arbitrary_target_contact_bound (r : ℝ) (p : Fin 6 → ℝ)
    (ρ : SmoothSample 2 (-1)) :
    |sourceContactQ (-1) (posteriorSample negativePeriodNonzero r p ρ)| ≤
      allTargetCurvatureResidualRadius negativePeriodNonzero r p ρ :=
  sourceContactQ_posterior_abs_le_allTargetRadius negativePeriodNonzero r p ρ

theorem exact_old_default_specialization (r b : ℝ) (ρ : SmoothSample 2 (-1)) :
    allTargetCurvatureResidualRadius negativePeriodNonzero r (sourcePrescribedPins r b) ρ =
      curvatureResidualRadius negativePeriodNonzero r b ρ :=
  allTargetCurvatureResidualRadius_prescribed negativePeriodNonzero r b ρ

/-- L=-1 is fixed; no target, radius, moment or covariance certificate occurs
before the existential constants. Both bounds and moments share the interval. -/
theorem closed_negative_period_endpoint :
    ∃ δ A H : ℝ, 0 < δ ∧ δ ≤ 1 ∧ 0 ≤ A ∧ 0 ≤ H ∧
      (∀ r : ℝ, 0 < r → r < δ → ∀ (p : Fin 6 → ℝ) (ρ : SmoothSample 2 (-1)) (q : ℝ),
        sourceGammaRadius (-1) (curvatureReconstruct negativePeriodNonzero r p ρ q) ≤
          A*(|q|+allTargetCurvatureResidualRadius negativePeriodNonzero r p ρ)) ∧
      (∀ r : ℝ, 0 < r → r < δ → ∀ (p : Fin 6 → ℝ) (ω : SmoothSample 2 (-1)),
        allTargetCurvatureResidualRadius negativePeriodNonzero r p
            (curvatureResidualSample negativePeriodNonzero r ω) ≤
          sourceGammaRadius (-1) (posteriorSample negativePeriodNonzero r p ω) +
            H*|curvatureZ (-1) r ω|) ∧
      ∀ n : ℕ, ∃ C : ℝ, 0 ≤ C ∧ ∀ r : ℝ, 0 < r → r < δ → ∀ p : Fin 6 → ℝ,
        Integrable (fun ρ => allTargetCurvatureResidualRadius negativePeriodNonzero r p ρ^n)
          (curvatureResidualLaw negativePeriodNonzero r) ∧
        (∫ ρ, allTargetCurvatureResidualRadius negativePeriodNonzero r p ρ^n
          ∂curvatureResidualLaw negativePeriodNonzero r) ≤ C*(1+‖p‖)^n :=
  allTargetCurvatureResidualRadius_uniform_bounds negativePeriodNonzero

theorem literal_residual_law (r : ℝ) :
    curvatureResidualLaw negativePeriodNonzero r =
      (smoothLaw 2 (-1)).map (curvatureResidualSample negativePeriodNonzero r) := rfl

theorem zeroth_moment_integrable (r : ℝ) (p : Fin 6 → ℝ) :
    Integrable (fun ρ => allTargetCurvatureResidualRadius negativePeriodNonzero r p ρ^0)
      (curvatureResidualLaw negativePeriodNonzero r) := by
  simpa only [pow_zero] using
    (integrable_const (1:ℝ) : Integrable (fun _ : SmoothSample 2 (-1) => (1:ℝ))
      (curvatureResidualLaw negativePeriodNonzero r))

theorem zeroth_moment_exact (r : ℝ) (p : Fin 6 → ℝ) :
    (∫ ρ, allTargetCurvatureResidualRadius negativePeriodNonzero r p ρ^0
      ∂curvatureResidualLaw negativePeriodNonzero r) = 1 := by simp

theorem nondefault_gap_literal (r : ℝ) :
    sourceGapPins r 3 2 = (![3-r^3,0,0,0,0,24] : Fin 6 → ℝ) := by
  ext i
  fin_cases i <;> simp [sourceGapPins] <;> ring

/-- The interval is independent of height, mark bound and order. -/
theorem all_height_gap_quantifiers :
    ∃ δ : ℝ, 0 < δ ∧ δ ≤ 1 ∧ ∀ K : ℝ, 0 ≤ K → ∀ n : ℕ,
      ∃ C : ℝ, 0 ≤ C ∧ ∀ r : ℝ, 0 < r → r < δ → ∀ b k : ℝ, |k| ≤ K →
        Integrable (fun ρ =>
          allTargetCurvatureResidualRadius negativePeriodNonzero r (sourceGapPins r b k) ρ^n)
          (curvatureResidualLaw negativePeriodNonzero r) ∧
        (∫ ρ, allTargetCurvatureResidualRadius negativePeriodNonzero r (sourceGapPins r b k) ρ^n
          ∂curvatureResidualLaw negativePeriodNonzero r) ≤ C*(1+|b|)^n :=
  allTargetCurvatureResidualRadius_gap_height_moments negativePeriodNonzero

theorem nondefault_gap_moments :
    ∃ δ : ℝ, 0 < δ ∧ δ ≤ 1 ∧ ∀ n : ℕ, ∃ C : ℝ, 0 ≤ C ∧
      ∀ r : ℝ, 0 < r → r < δ →
        Integrable (fun ρ =>
          allTargetCurvatureResidualRadius negativePeriodNonzero r (sourceGapPins r 3 2) ρ^n)
          (curvatureResidualLaw negativePeriodNonzero r) ∧
        (∫ ρ, allTargetCurvatureResidualRadius negativePeriodNonzero r (sourceGapPins r 3 2) ρ^n
          ∂curvatureResidualLaw negativePeriodNonzero r) ≤ C*4^n := by
  obtain ⟨δ,hδ,hδ1,hbound⟩ := all_height_gap_quantifiers
  refine ⟨δ,hδ,hδ1,?_⟩
  intro n
  obtain ⟨C,hC,hCbound⟩ := hbound 2 (by norm_num) n
  refine ⟨C,hC,?_⟩
  intro r hr hrδ
  simpa using hCbound r hr hrδ 3 2 (by norm_num)

/-- A norm-based counterexample to the proposed arithmetic factor-erasure step.
This statement concerns that step, not all possible moment estimates. -/
theorem constant_three_norm : ‖(fun _ : Fin 6 => (3:ℝ))‖ = 3 := by
  have hu : ‖(fun _ : Fin 6 => (3:ℝ))‖ ≤ 3 := by
    apply (pi_norm_le_iff_of_nonneg (by norm_num : (0:ℝ) ≤ 3)).mpr
    intro i
    norm_num
  have hl : (3:ℝ) ≤ ‖(fun _ : Fin 6 => (3:ℝ))‖ := by
    simpa using norm_le_pi_norm (fun _ : Fin 6 => (3:ℝ)) (0 : Fin 6)
  exact le_antisymm hu hl

theorem target_growth_erasure_counterexample :
    ¬ ((1+‖(fun _ : Fin 6 => (3:ℝ))‖)^1 ≤ (1:ℝ)) := by
  rw [constant_three_norm]
  norm_num

end AllTargetResidualControls
