from pathlib import Path
p=Path('/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025/SourceGapWeightedNumerator.lean')
s=p.read_text().replace('convert hh using 1 <;> ring','convert hh using 1; ring').replace('\nend I4SourceGapWeightedNumerator\n','\n')
s+='''
/-- A compact height/mark regular-layer bound, derived from the actual product
law, its mean-uniform scalar density, residual moments and physical zero pins. -/
theorem sourceGapLaw_regular_numerator {L : ℝ} (hL : L ≠ 0)
    (B K A eps : ℝ) (hB : 0 ≤ B) (hK : 0 ≤ K) (hA : 0 ≤ A) (heps : 0 < eps) :
    ∃ N δ : ℝ, 0 ≤ N ∧ 0 < δ ∧ δ ≤ 1 ∧
      ∀ r : ℝ, 0 < r → r < δ → ∀ b k : ℝ, |b| ≤ B → |k| ≤ K →
        (∫ ω in sourceRegularCurvatureSlab L r A eps, sourceSmoothWeight L r ω
          ∂sourceGapLaw hL r b k) ≤ N*r^5 := by
  obtain ⟨δS,C,H,hδS,hδS1,hC,_hH,hdom,_himage,hmom⟩ :=
    allTargetCurvatureResidualRadius_uniform_bounds hL
  obtain ⟨T0,hT0,hS17⟩ := hmom 17
  obtain ⟨D,δD,hD,hδD,_hδD1,hdensity⟩ := curvatureScalarLaw_interval_mass_uniform hL
  obtain ⟨_Bp,_Mp,δG,_hBp,_hMp,hδG,_hδG1,hparam⟩ := curvature_uniform_parameter_bounds hL 0
  obtain ⟨δW,hδW,_hδW1,hWint⟩ := sourceGapLaw_weight_integrable hL
  let T := T0*(1+B+13*K)^17
  let J := C*(1+A*eps)
  let N := (2*D*(A*J^5)*(2*A^2*J^12+8*J^4))*T
  let δ := min δS (min δD (min δG δW))
  have hδ : 0 < δ := lt_min hδS (lt_min hδD (lt_min hδG hδW))
  have hδD' : δ ≤ δD := (min_le_right _ _).trans (min_le_left _ _)
  have hδG' : δ ≤ δG := (min_le_right _ _).trans ((min_le_right _ _).trans (min_le_left _ _))
  have hδW' : δ ≤ δW := (min_le_right _ _).trans ((min_le_right _ _).trans (min_le_right _ _))
  have hT : 0 ≤ T := by dsimp [T]; positivity
  refine ⟨N,δ,by dsimp [N,J]; positivity,hδ,(min_le_left _ _).trans hδS1,?_⟩
  intro r hr hrδ b k hb hk
  have hrS : r < δS := lt_of_lt_of_le hrδ (min_le_left _ _)
  have hrD : r < δD := lt_of_lt_of_le hrδ hδD'
  have hrG : r < δG := lt_of_lt_of_le hrδ hδG'
  have hrW : r < δW := lt_of_lt_of_le hrδ hδW'
  have hr1 : r ≤ 1 := hrS.le.trans hδS1
  obtain ⟨hG,hτfloor,_hbeta,_hmean⟩ := hparam r hr hrG
  have hτ : 0 < curvatureVariance L r :=
    (div_pos (sourceContactSchur_pos hL) (by norm_num)).trans_le hτfloor
  let x := sourceGapPins r b k
  obtain ⟨hSint,hSbound⟩ := hS17 r hr hrS x
  have hST : (∫ ρ, allTargetCurvatureResidualRadius hL r x ρ^17
      ∂curvatureResidualLaw hL r) ≤ T := by
    have hp : ‖x‖ ≤ B+13*K :=
      (sourceGapPins_norm_le r b k K hr.le hr1 hK hk).trans (by linarith)
    exact hSbound.trans (mul_le_mul_of_nonneg_left
      (pow_le_pow_left₀ (by positivity) (by linarith : 1+‖x‖ ≤ 1+B+13*K) 17) hT0)
  let ν := curvatureScalarLaw L r x
  let ρ := curvatureResidualLaw hL r
  let Ψ : ℝ × SmoothSample 2 L → SmoothSample 2 L :=
    fun p => curvatureReconstruct hL r x p.2 p.1
  have hΨ : Measurable Ψ := curvatureReconstruct_swap_measurable hL r x
  have hmap : (ν.prod ρ).map Ψ = sourceGapLaw hL r b k :=
    (curvatureReconstruct_hasLaw hL r hG hτ x).map_eq
  have hq : ∀ᵐ p ∂ν.prod ρ, sourceQ L (Ψ p) = p.1 :=
    Eventually.of_forall (fun p => by
      rw [sourceQ_eq_sourceContactQ]
      exact curvatureReconstruct_Q hL r hτ x p.2 p.1)
  exact sourceGapLaw_regular_numerator_of_product hL r b k A eps C D T
    hr hA heps hC hD hT hG ν ρ Ψ hΨ hmap hq
    (allTargetCurvatureResidualRadius hL r x)
    (one_le_allTargetCurvatureResidualRadius hL r x) hSint hST
    (fun p => hdom r hr hrS x p.2 p.1)
    (hdensity r hr hrD x) (hWint r hr hrW b k)

/-- The actual one-sided obstruction reduces at the integrand level to the
regular symmetric slab and irregular tail. Zero physical weight is retained. -/
theorem sourceBadUnion_integral_le {L : ℝ} (hL : L ≠ 0)
    (r A eps : ℝ) (hr : 0 < r) (Q : Measure (SmoothSample 2 L))
    (hW : Integrable (sourceSmoothWeight L r) Q) :
    (∫ ω in sourceRegularityBad L r eps ∪ sourceCurvatureOneSided L r A,
      sourceSmoothWeight L r ω ∂Q) ≤
      (∫ ω in sourceRegularityBad L r eps, sourceSmoothWeight L r ω ∂Q) +
      (∫ ω in sourceRegularCurvatureSlab L r (max A 1) eps,
        sourceSmoothWeight L r ω ∂Q) := by
  let E := sourceRegularityBad L r eps
  let F := sourceRegularCurvatureSlab L r (max A 1) eps
  let U := E ∪ sourceCurvatureOneSided L r A
  have hE : MeasurableSet E := sourceRegularityBad_measurable L r eps
  have hF : MeasurableSet F := sourceRegularCurvatureSlab_measurable hL r (max A 1) eps
  have hU : MeasurableSet U := hE.union (sourceCurvatureOneSided_measurable hL r A)
  rw [← integral_indicator hU,← integral_indicator hE,← integral_indicator hF,
    ← integral_add (hW.indicator hE) (hW.indicator hF)]
  apply integral_mono (hW.indicator hU) ((hW.indicator hE).add (hW.indicator hF))
  intro ω
  have hW0 := sourceSmoothWeight_nonneg L r ω
  have hEI : 0 ≤ E.indicator (sourceSmoothWeight L r) ω :=
    Set.indicator_nonneg (fun _ _ => sourceSmoothWeight_nonneg L r _) ω
  have hFI : 0 ≤ F.indicator (sourceSmoothWeight L r) ω :=
    Set.indicator_nonneg (fun _ _ => sourceSmoothWeight_nonneg L r _) ω
  by_cases hωU : ω ∈ U
  · rw [Set.indicator_of_mem hωU]
    by_cases hωE : ω ∈ E
    · rw [Set.indicator_of_mem hωE]
      exact le_add_of_nonneg_right hFI
    · have hq : -A*r*sourceGammaRadius L ω^5 ≤ sourceQ L ω := hωU.resolve_left hωE
      by_cases hpos : 0 < sourceSmoothWeight L r ω
      · have hωF : ω ∈ F := ⟨le_of_not_gt hωE,
          I4SourceGapPinCurvature.source_bad_curvature_slab hL r hr ω hpos A hq⟩
        rw [Set.indicator_of_notMem hωE,Set.indicator_of_mem hωF,zero_add]
      · have hz : sourceSmoothWeight L r ω = 0 := le_antisymm (le_of_not_gt hpos) hW0
        rw [hz]
        exact add_nonneg hEI hFI
  · rw [Set.indicator_of_notMem hωU]
    exact add_nonneg hEI hFI

/-- Closed compact varying-mark numerator. All source certificates are derived
internally; N and delta are uniform in r,b,k on the displayed compact bounds.
This theorem gives no positive normalizer or normalized probability. -/
theorem sourceGapLaw_bad_union_numerator {L : ℝ} (hL : L ≠ 0)
    (B K A eps : ℝ) (hB : 0 ≤ B) (hK : 0 ≤ K) (hA : 0 ≤ A) (heps : 0 < eps) :
    ∃ N δ : ℝ, 0 ≤ N ∧ 0 < δ ∧ δ ≤ 1 ∧
      ∀ r : ℝ, 0 < r → r < δ → ∀ b k : ℝ, |b| ≤ B → |k| ≤ K →
        Integrable (sourceSmoothWeight L r) (sourceGapLaw hL r b k) ∧
        IntegrableOn (sourceSmoothWeight L r)
          (sourceRegularityBad L r eps ∪ sourceCurvatureOneSided L r A)
          (sourceGapLaw hL r b k) ∧
        (∫ ω in sourceRegularityBad L r eps ∪ sourceCurvatureOneSided L r A,
          sourceSmoothWeight L r ω ∂sourceGapLaw hL r b k) ≤ N*r^5 := by
  obtain ⟨Nt,δt,hNt,hδt,hδt1,htail⟩ := sourceGapLaw_regularity_numerator hL B K eps hB hK heps
  obtain ⟨Nr,δr,hNr,hδr,_hδr1,hregular⟩ :=
    sourceGapLaw_regular_numerator hL B K (max A 1) eps hB hK
      ((by norm_num : (0:ℝ) ≤ 1).trans (le_max_right _ _)) heps
  obtain ⟨δw,hδw,_hδw1,hw⟩ := sourceGapLaw_weight_integrable hL
  let δ := min δt (min δr δw)
  refine ⟨Nt+Nr,δ,add_nonneg hNt hNr,lt_min hδt (lt_min hδr hδw),
    (min_le_left _ _).trans hδt1,?_⟩
  intro r hr hrδ b k hb hk
  have hrt : r < δt := lt_of_lt_of_le hrδ (min_le_left _ _)
  have hrr : r < δr := lt_of_lt_of_le hrδ ((min_le_right _ _).trans (min_le_left _ _))
  have hrw : r < δw := lt_of_lt_of_le hrδ ((min_le_right _ _).trans (min_le_right _ _))
  have hW := hw r hr hrw b k
  refine ⟨hW,hW.integrableOn,?_⟩
  calc
    _ ≤ (∫ ω in sourceRegularityBad L r eps, sourceSmoothWeight L r ω ∂sourceGapLaw hL r b k) +
        (∫ ω in sourceRegularCurvatureSlab L r (max A 1) eps,
          sourceSmoothWeight L r ω ∂sourceGapLaw hL r b k) :=
      sourceBadUnion_integral_le hL r A eps hr (sourceGapLaw hL r b k) hW
    _ ≤ Nt*r^5+Nr*r^5 := add_le_add (htail r hr hrt b k hb hk).2 (hregular r hr hrr b k hb hk)
    _ = _ := by ring

end I4SourceGapWeightedNumerator
'''
p.write_text(s)
