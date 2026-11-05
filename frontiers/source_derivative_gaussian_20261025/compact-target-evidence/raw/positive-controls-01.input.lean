import SourceCompactTargetMoments

noncomputable section
open I4Foundation I4Source I4SmoothCarrier I4SourceSmoothConditional
open I4SourcePinCurvatureBounds I4SourceSmoothPalm I4SourceRawPinConditioning
open I4SourceCompactTargetMoments MeasureTheory
open scoped Matrix
set_option autoImplicit false

-- The target has five arbitrary components and one fixed nonzero component.
theorem arbitrary_nonzero_target (x y z u v : ℝ) :
    (![1,x,y,z,u,v] : Fin 6 → ℝ) ≠ 0 := by
  intro h
  have h0 := congrFun h 0
  norm_num at h0

theorem arbitrary_nonzero_target_moments {L : ℝ} (hL : L ≠ 0) :
    ∃ δ : ℝ, 0 < δ ∧ δ ≤ 1 ∧ ∀ n : ℕ, ∃ C : ℝ, 0 ≤ C ∧
      ∀ r : ℝ, 0 < r → r < δ → ∀ x y z u v : ℝ,
        Integrable (fun ω => sourceGammaRadius L ω ^ n)
          (sourceSmoothKernel hL r ![1,x,y,z,u,v]) ∧
        (∫ ω, sourceGammaRadius L ω ^ n
          ∂sourceSmoothKernel hL r ![1,x,y,z,u,v]) ≤
          C * (1 + ‖(![1,x,y,z,u,v] : Fin 6 → ℝ)‖)^n := by
  obtain ⟨δ,hδ,hδ1,hm⟩ := sourceGammaRadius_allTarget_moments hL
  refine ⟨δ,hδ,hδ1,?_⟩
  intro n
  obtain ⟨C,hC,hb⟩ := hm n
  exact ⟨C,hC,fun r hr hrδ x y z u v => hb r hr hrδ ![1,x,y,z,u,v]⟩

-- k=1 differs genuinely from the old row5=2 specialization.
theorem varying_gap_nonstandard (r b : ℝ) :
    sourceGapPins r b 1 5 = 12 ∧
      sourceGapPins r b 1 ≠ sourceGapPins r b (1/6) := by
  constructor
  · norm_num [sourceGapPins]
  · intro h
    have h5 := congrFun h 5
    norm_num [sourceGapPins] at h5

theorem nonstandard_gap_raw_transport {L : ℝ} (hL : L ≠ 0)
    (r b : ℝ) (hr : r ≠ 0) :
    sourceGapLaw hL r b 1 = rawPinKernel hL r ![b,b-r^3,0,0,0,0] := by
  simpa using sourceGapLaw_eq_rawPinKernel hL r b 1 hr

theorem nonstandard_gap_height_moments {L : ℝ} (hL : L ≠ 0) :
    ∃ δ : ℝ, 0 < δ ∧ δ ≤ 1 ∧ ∀ n : ℕ, ∃ C : ℝ, 0 ≤ C ∧
      ∀ r : ℝ, 0 < r → r < δ → ∀ b : ℝ,
        Integrable (fun ω => sourceGammaRadius L ω ^ n) (sourceGapLaw hL r b 1) ∧
        (∫ ω, sourceGammaRadius L ω ^ n ∂sourceGapLaw hL r b 1) ≤ C*(1+|b|)^n := by
  obtain ⟨δ,hδ,hδ1,hm⟩ := sourceGapLaw_height_moments hL 1 (by norm_num)
  refine ⟨δ,hδ,hδ1,?_⟩
  intro n
  obtain ⟨C,hC,hb⟩ := hm n
  exact ⟨C,hC,fun r hr hrδ b => hb r hr hrδ b 1 (by norm_num)⟩

-- The height term is forced by the first coordinate of the actual target.
theorem gap_target_has_no_height_uniform_norm_bound (C : ℝ) :
    ¬ ∀ b : ℝ, ‖sourceGapPins (1/2) b 0‖ ≤ C := by
  intro h
  have hn := norm_le_pi_norm (sourceGapPins (1/2) (|C|+1) 0) 0
  have hc := h (|C|+1)
  simp [sourceGapPins, Real.norm_eq_abs, abs_of_nonneg (by positivity : 0 ≤ |C|+1)] at hn
  linarith [le_abs_self C]
