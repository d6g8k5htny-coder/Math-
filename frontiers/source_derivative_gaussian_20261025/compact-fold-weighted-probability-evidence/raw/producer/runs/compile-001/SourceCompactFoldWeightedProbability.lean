import SourceFoldWeightedProbability
import SourceCompactGapNormalizer

/-! Compact positive-gap normalized fold-cutoff probability on the original
signed-period smooth carrier. The actual varying-mark posterior and physical
weight are retained. The same uniform interval also supports the accepted
ordinary singular-H0 summand and exact strict clearance on the cutoff event.
No canonical Morse partner or measurable geometric selector is asserted. -/

noncomputable section
open Set MeasureTheory CategoryTheory Limits
open I4SmoothCarrier I4SourceSmoothPalm I4SourceConditionalMajorant I4SourceConfluentPins
open I4SourcePinCurvatureBounds I4SourceWeightedCurvature I4SourceGapWeightedNumerator
open I4SourceCompactTargetMoments I4SourceAdaptiveFoldEstimates
open SourceActualFoldTorus SourceActualFoldH0 TorusFiltration I4Torus
open SourceFoldWeightedProbability SourceCompactGapNormalizer ResearchFormalCoreR1
set_option autoImplicit false

namespace SourceCompactFoldWeightedProbability

/-- Literal cutoffs, with the actual positive gap coefficient left variable. -/
def sourceCompactFoldGood (L k₀ r k : ℝ) : Set (SmoothSample 2 L) :=
  {sample | r * sourceT k₀ sample ^ 5 ≤ 1/100 ∧
    1024 * sourceT k₀ sample ^ 5 ≤ sourceKappa r k sample}

/-- Actual physical weighting of the same literal varying-gap posterior. -/
def sourceCompactFoldWeightedLaw {L : ℝ} (hL : L ≠ 0) (r b k : ℝ) :
    Measure (SmoothSample 2 L) :=
  prwMeasure (sourceGapLaw hL r b k) (sourceSmoothWeight L r)

/-- The uniform curvature obstruction retains the full factor 6*k₁. -/
def sourceCompactCutoffA (k₀ k₁ : ℝ) : ℝ := 6*k₁*1024*sourceScale k₀^5

theorem sourceCompactCutoffA_nonneg (k₀ k₁ : ℝ) (hk₁ : 0 ≤ k₁) :
    0 ≤ sourceCompactCutoffA k₀ k₁ := by
  unfold sourceCompactCutoffA
  exact mul_nonneg (by positivity) (pow_nonneg (sourceScale_pos k₀).le 5)

theorem sourceCompactFoldGood_measurable {L : ℝ} (hL : L ≠ 0) (k₀ r k : ℝ) :
    MeasurableSet (sourceCompactFoldGood L k₀ r k) := by
  exact (measurableSet_le (((sourceT_measurable L k₀).pow_const 5).const_mul r)
    measurable_const).inter
      (measurableSet_le (((sourceT_measurable L k₀).pow_const 5).const_mul 1024)
        (sourceKappa_measurable hL r k))

/-- Scalar failure arithmetic: strict cutoff failure gives the closed uniform
one-sided curvature obstruction, using the original nonnegative radius. -/
theorem varying_cutoff_failure_inclusion (lam r Γ q k k₁ : ℝ)
    (hlam : 0 < lam) (hr : 0 < r) (hΓ : 0 ≤ Γ) (hk : 0 < k) (hk₁ : k ≤ k₁)
    (hbad : ¬ (r*(lam*Γ)^5 ≤ 1/100 ∧ 1024*(lam*Γ)^5 ≤ -q/(6*k*r))) :
    1/(100*lam^5) < r*Γ^5 ∨ -(6*k₁*1024*lam^5)*r*Γ^5 ≤ q := by
  rcases not_and_or.mp hbad with h | h
  · left
    have hf : (1 : ℝ)/100 < (r*Γ^5)*lam^5 := by
      convert lt_of_not_ge h using 1; ring
    apply (div_lt_iff₀ (mul_pos (by norm_num : (0:ℝ) < 100) (pow_pos hlam 5))).2
    nlinarith
  · right
    have hf := (div_lt_iff₀ (by positivity : 0 < 6*k*r)).mp (lt_of_not_ge h)
    have heq : 1024*(lam*Γ)^5*(6*k*r) = k*(6*1024*lam^5*r*Γ^5) := by ring
    rw [heq] at hf
    have hm := mul_le_mul_of_nonneg_right hk₁
      (by positivity : 0 ≤ 6*1024*lam^5*r*Γ^5)
    nlinarith

theorem sourceCompactFoldGood_compl_subset (L k₀ k₁ r k : ℝ)
    (hk₀ : 0 < k₀) (hk : k₀ ≤ k) (hk₁ : k ≤ k₁) (hr : 0 < r) :
    (sourceCompactFoldGood L k₀ r k)ᶜ ⊆
      sourceRegularityBad L r (sourceCutoffEps k₀) ∪
        sourceCurvatureOneSided L r (sourceCompactCutoffA k₀ k₁) := by
  intro sample hs
  change ¬ (_ ∧ _) at hs
  rw [sourceT_eq_scale] at hs
  exact varying_cutoff_failure_inclusion (sourceScale k₀) r (sourceGammaRadius L sample)
    (sourceQ L sample) k k₁ (sourceScale_pos k₀) hr
    (sourceGammaRadius_nonneg L sample) (hk₀.trans_le hk) hk₁ hs

/-- Absolute continuity is derived for exactly the law being normalized. -/
theorem sourceCompactFoldWeightedLaw_absolutelyContinuous {L : ℝ} (hL : L ≠ 0)
    (r b k : ℝ) :
    sourceCompactFoldWeightedLaw hL r b k ≪ sourceGapLaw hL r b k :=
  prwMeasure_absolutelyContinuous _ _

/-- Closed compact endpoint. The actual numerator and positive normalizer are
derived internally; one C and delta precede radius and both varying marks. -/
theorem sourceCompactFoldWeightedProbability_bound {L : ℝ} (hL : L ≠ 0)
    (B k₀ k₁ : ℝ) (hB : 0 ≤ B) (hk₀ : 0 < k₀) (hk₀₁ : k₀ ≤ k₁) :
    ∃ C δ : ℝ, 0 ≤ C ∧ 0 < δ ∧ δ ≤ 1 ∧
      ∀ r : ℝ, 0 < r → r < δ → ∀ b k : ℝ, |b| ≤ B → k₀ ≤ k → k ≤ k₁ →
        IsProbabilityMeasure (sourceCompactFoldWeightedLaw hL r b k) ∧
        (sourceCompactFoldWeightedLaw hL r b k).real
          (sourceCompactFoldGood L k₀ r k)ᶜ ≤ C*r^3 := by
  have hk₁ : 0 ≤ k₁ := hk₀.le.trans hk₀₁
  obtain ⟨N,δN,hN,hδN,hδN1,hnum⟩ := sourceGapLaw_bad_union_numerator hL B k₁
    (sourceCompactCutoffA k₀ k₁) (sourceCutoffEps k₀) hB hk₁
    (sourceCompactCutoffA_nonneg k₀ k₁ hk₁) (sourceCutoffEps_pos k₀)
  obtain ⟨c,δc,hc,hδc,_hδc1,hnorm⟩ := sourceGapLaw_compact_normalizer hL B k₀ k₁
    hB hk₀ hk₀₁
  refine ⟨N/c,min δN δc,div_nonneg hN hc.le,lt_min hδN hδc,
    (min_le_left _ _).trans hδN1,?_⟩
  intro r hr hrδ b k hb hk hk'
  have hkabs : |k| ≤ k₁ := by rw [abs_of_nonneg (hk₀.le.trans hk)]; exact hk'
  obtain ⟨hW,_hOn,hn⟩ := hnum r hr (hrδ.trans_le (min_le_left _ _)) b k hb hkabs
  obtain ⟨_hW,hfloor⟩ := hnorm r hr (hrδ.trans_le (min_le_right _ _)) b k hb hk hk'
  have hZ : 0 < ∫ ω, sourceSmoothWeight L r ω ∂sourceGapLaw hL r b k :=
    (mul_pos hc (sq_pos_of_pos hr)).trans_le hfloor
  have hp : IsProbabilityMeasure (sourceCompactFoldWeightedLaw hL r b k) :=
    prw_isProbabilityMeasure _ _ hW (sourceSmoothWeight_nonneg L r) hZ
  let _ := hp
  refine ⟨hp,?_⟩
  calc
    _ ≤ (sourceCompactFoldWeightedLaw hL r b k).real
        (sourceRegularityBad L r (sourceCutoffEps k₀) ∪
          sourceCurvatureOneSided L r (sourceCompactCutoffA k₀ k₁)) :=
      measureReal_mono (sourceCompactFoldGood_compl_subset L k₀ k₁ r k hk₀ hk hk' hr)
    _ = (∫ ω in sourceRegularityBad L r (sourceCutoffEps k₀) ∪
          sourceCurvatureOneSided L r (sourceCompactCutoffA k₀ k₁),
          sourceSmoothWeight L r ω ∂sourceGapLaw hL r b k) /
        ∫ ω, sourceSmoothWeight L r ω ∂sourceGapLaw hL r b k :=
      prw_measure_real _ _ hW (sourceSmoothWeight_nonneg L r) hZ _
        ((sourceRegularityBad_measurable L r _).union
          (sourceCurvatureOneSided_measurable hL r _))
    _ ≤ (N*r^5)/(c*r^2) :=
      div_le_div₀ (by positivity) hn (mul_pos hc (sq_pos_of_pos hr)) hfloor
    _ = (N/c)*r^3 := by field_simp [hr.ne']

/-- One uniform radius is chosen before all marks and every coefficient field.
On Good, weighted-almost every sample has an actual ordinary-H0 interval
[-b,-(b-k*r^3)), a complement and exact strict clearance and real supremum. -/
theorem sourceCompactFoldWeightedProbability_h0 {L : ℝ} (hL : L ≠ 0)
    (B k₀ k₁ : ℝ) (hB : 0 ≤ B) (hk₀ : 0 < k₀) (hk₀₁ : k₀ ≤ k₁) :
    ∃ C δ : ℝ, 0 ≤ C ∧ 0 < δ ∧ δ ≤ 1 ∧
      ∀ r : ℝ, 0 < r → r < δ → ∀ b k : ℝ, |b| ≤ B → k₀ ≤ k → k ≤ k₁ →
        IsProbabilityMeasure (sourceCompactFoldWeightedLaw hL r b k) ∧
        (sourceCompactFoldWeightedLaw hL r b k).real
          (sourceCompactFoldGood L k₀ r k)ᶜ ≤ C*r^3 ∧
        ∀ (K : Type) [Field K], ∀ᵐ sample ∂sourceCompactFoldWeightedLaw hL r b k,
          sample ∈ sourceCompactFoldGood L k₀ r k →
            ∃ D : ℝ ⥤ ModuleCat K,
              Nonempty (superlevel_h0Filtration (actualTorusField hL sample)
                (ModuleCat.of K K) ≅ elderInterval K b (b-k*r^3) ⊞ D) ∧
              strictClearanceSet (actualTorusField hL sample)
                (torusProjection 2 L (endpointM r)) = Iio (b-k*r^3) ∧
              strictClearanceDeath (actualTorusField hL sample)
                (torusProjection 2 L (endpointM r)) = b-k*r^3 := by
  obtain ⟨C,δP,hC,hδP,hδP1,hP⟩ := sourceCompactFoldWeightedProbability_bound hL
    B k₀ k₁ hB hk₀ hk₀₁
  obtain ⟨δH,hδH,_hδH1,hH⟩ := sourceGapLaw_actual_torus_h0 hL
  refine ⟨C,min δP δH,hC,lt_min hδP hδH,(min_le_left _ _).trans hδP1,?_⟩
  intro r hr hrδ b k hb hk hk'
  obtain ⟨hp,hbad⟩ := hP r hr (hrδ.trans_le (min_le_left _ _)) b k hb hk hk'
  refine ⟨hp,hbad,?_⟩
  intro K instK
  have hs := (sourceCompactFoldWeightedLaw_absolutelyContinuous hL r b k).ae_le
    (hH K k₀ hk₀ r hr (hrδ.trans_le (min_le_right _ _)) b k hk)
  filter_upwards [hs] with sample hs
  intro hgood
  exact hs hgood.1 hgood.2

end SourceCompactFoldWeightedProbability
