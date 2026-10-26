import SourceMorseIncidence

noncomputable section
open I4Foundation I4Source I4Smooth I4SmoothCarrier I4ActualSourceMorse
open MeasureTheory ProbabilityTheory

namespace MorseIncidenceControls

-- A signed side length is covered by the actual theorem, without replacing it by |L|.
example : ∀ᵐ ω ∂smoothLaw 2 (-1),
    ∀ x, 0 < sourceMorseDiscriminant (-1) ω x :=
  smoothLaw_ae_sourceMorse (by norm_num)

example : ∀ᵐ ω ∂smoothLaw 2 1,
    {x | x ∈ sourceMorseCube 1 ∧
      coordinateGradient (smoothSourceField 2 1 ω) x = 0}.Finite :=
  smoothLaw_ae_finite_sourceCriticalCube (by norm_num)

example (L : ℝ) (hL : L ≠ 0) :
    (smoothLaw 2 L).map (actualGroupedFour 2 L fourMode) =
      (Measure.pi fun _ : Fin 2 => gaussianReal 0 1).prod
        (Measure.pi fun _ : Fin 2 => gaussianReal 0 1) :=
  actualGroupedFour_map_eq 2 hL fourMode fourMode_injective

-- The actual zero coefficient sample is smooth and is degenerate everywhere.
-- Consequently the result cannot be strengthened from almost every to every sample.
def zeroSample (L : ℝ) : SmoothSample 2 L :=
  ⟨0, by
    intro n
    simpa only [Pi.zero_apply, abs_zero, mul_zero] using
      (summable_zero : Summable (fun _ : SourceMode 2 => (0 : ℝ)))⟩

theorem zeroSample_field (L : ℝ) :
    smoothSourceField 2 L (zeroSample L) = fun _ => 0 := by
  funext x
  simp [smoothSourceField, sampleInclusion, zeroSample, sourceField, scalarSeries]

theorem zeroSample_discriminant (L : ℝ) (x : Fin 2 → ℝ) :
    sourceMorseDiscriminant L (zeroSample L) x = 0 := by
  simp [sourceMorseDiscriminant, zeroSample_field]

theorem not_every_source_sample_morse (L : ℝ) :
    ¬ ∀ ω : SmoothSample 2 L, ∀ x ∈ sourceMorseCube L,
      0 < sourceMorseDiscriminant L ω x := by
  intro h
  have hz : (0 : Fin 2 → ℝ) ∈ sourceMorseCube L := by
    constructor
    · exact le_rfl
    · intro i
      exact abs_nonneg L
  have hp := h (zeroSample L) 0 hz
  rw [zeroSample_discriminant] at hp
  exact (lt_irrefl 0) hp

-- Without the actual nonzero amplitudes the full Gaussian parameter law is bad.
theorem zero_amplitudes_bad_univ (c : ℝ) :
    trigonometricDegenerateCriticalParameters (fun _ => 0) 0 c = Set.univ := by
  ext a
  constructor
  · intro _
    trivial
  · intro _
    have hf : (fun y => twoChannelGradientFamily (fun _ => 0)
        (cosineGradientChannel 0 c) (sineGradientChannel 0 c) y a) = fun _ => 0 := by
      funext y i
      simp [twoChannelGradientFamily, cosineGradientChannel, sineGradientChannel]
    refine ⟨0, ?_, ?_⟩
    · exact congrFun hf 0
    · rw [hf, fderiv_const_apply]
      intro hinj
      have he : (Pi.single (0 : Fin 2) 1 : Fin 2 → ℝ) = 0 := hinj (by simp)
      have hz := congrFun he 0
      norm_num at hz

example (c : ℝ) :
    ((Measure.pi fun _ : Fin 2 => gaussianReal 0 1).prod
      (Measure.pi fun _ : Fin 2 => gaussianReal 0 1))
      (trigonometricDegenerateCriticalParameters (fun _ => 0) 0 c) = 1 := by
  rw [zero_amplitudes_bad_univ]
  exact measure_univ

-- Removing the nonzero-frequency premise also makes every parameter degenerate.
theorem zero_frequency_bad_univ (A : Fin 2 → ℝ) :
    trigonometricDegenerateCriticalParameters (fun _ => 0) A 0 = Set.univ := by
  ext a
  constructor
  · intro _
    trivial
  · intro _
    have hf : (fun y => twoChannelGradientFamily (fun _ => 0)
        (cosineGradientChannel A 0) (sineGradientChannel A 0) y a) = fun _ => 0 := by
      funext y i
      simp [twoChannelGradientFamily, cosineGradientChannel, sineGradientChannel]
    refine ⟨0, ?_, ?_⟩
    · exact congrFun hf 0
    · rw [hf, fderiv_const_apply]
      intro hinj
      have he : (Pi.single (0 : Fin 2) 1 : Fin 2 → ℝ) = 0 := hinj (by simp)
      have hz := congrFun he 0
      norm_num at hz

example (A : Fin 2 → ℝ) :
    ((Measure.pi fun _ : Fin 2 => gaussianReal 0 1).prod
      (Measure.pi fun _ : Fin 2 => gaussianReal 0 1))
      (trigonometricDegenerateCriticalParameters (fun _ => 0) A 0) = 1 := by
  rw [zero_frequency_bad_univ]
  exact measure_univ

end MorseIncidenceControls
