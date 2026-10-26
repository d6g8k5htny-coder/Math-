import SourceActualFoldH0
import SourceWeightedCurvatureBound

/-! Fixed sixth-gap normalized cutoff probability on the original smooth
carrier. The old cubic curvature bound and actual ordinary-H0 theorem are
composed on the same literal weighted gap law. No varying-mark uniformity,
canonical partner, selector measurability or count-density claim is made. -/

noncomputable section
open Set MeasureTheory CategoryTheory Limits
open I4SmoothCarrier I4SourceSmoothPalm I4SourceConditionalMajorant I4SourceConfluentPins
open I4SourcePinCurvatureBounds I4SourceWeightedCurvature
open I4SourceCompactTargetMoments I4SourceAdaptiveFoldEstimates
open SourceActualFoldTorus SourceActualFoldH0 TorusFiltration I4Torus
open ResearchFormalCoreR1
set_option autoImplicit false

namespace SourceFoldWeightedProbability

/-- The full scale includes the factor eight from the source radius. -/
def sourceScale (k₀ : ℝ) : ℝ := 8 * max 1 (1/(6*k₀))
def sourceCutoffEps (k₀ : ℝ) : ℝ := 1/(100 * sourceScale k₀ ^ 5)
def sourceCutoffA (k₀ : ℝ) : ℝ := 1024 * sourceScale k₀ ^ 5

/-- Literal sample cutoffs; no geometric selector enters this event. -/
def sourceFoldGood (L k₀ r : ℝ) : Set (SmoothSample 2 L) :=
  {sample | r * sourceT k₀ sample ^ 5 ≤ 1/100 ∧
    1024 * sourceT k₀ sample ^ 5 ≤ sourceKappa r (1/6) sample}

/-- Actual determinant weighting of the actual sixth-gap posterior. -/
def sourceFoldWeightedLaw {L : ℝ} (hL : L ≠ 0) (r b : ℝ) :
    Measure (SmoothSample 2 L) :=
  prwMeasure (sourceGapLaw hL r b (1/6)) (sourceSmoothWeight L r)

theorem sourceScale_pos (k₀ : ℝ) : 0 < sourceScale k₀ := by
  have h : (1 : ℝ) ≤ max 1 (1/(6*k₀)) := le_max_left _ _
  unfold sourceScale
  positivity

theorem sourceCutoffEps_pos (k₀ : ℝ) : 0 < sourceCutoffEps k₀ := by
  unfold sourceCutoffEps
  exact one_div_pos.mpr (mul_pos (by norm_num) (pow_pos (sourceScale_pos k₀) 5))

theorem sourceCutoffA_nonneg (k₀ : ℝ) : 0 ≤ sourceCutoffA k₀ := by
  unfold sourceCutoffA
  exact mul_nonneg (by norm_num) (pow_nonneg (sourceScale_pos k₀).le 5)

theorem sourceT_eq_scale {L : ℝ} (k₀ : ℝ) (sample : SmoothSample 2 L) :
    sourceT k₀ sample = sourceScale k₀ * sourceGammaRadius L sample := by
  unfold sourceT sourceScale
  ring

theorem sourceKappa_one_sixth {L : ℝ} (r : ℝ) (sample : SmoothSample 2 L) :
    sourceKappa r (1/6) sample = -sourceQ L sample / r := by
  unfold sourceKappa
  congr 1
  ring

theorem sourceT_measurable (L k₀ : ℝ) : Measurable (@sourceT L k₀) := by
  unfold sourceT
  exact ((sourceGammaRadius_measurable L).const_mul 8).const_mul _

theorem sourceKappa_measurable {L : ℝ} (hL : L ≠ 0) (r k : ℝ) :
    Measurable (@sourceKappa L r k) := by
  exact (sourceQ_measurable hL).neg.div_const _

theorem sourceFoldGood_measurable {L : ℝ} (hL : L ≠ 0) (k₀ r : ℝ) :
    MeasurableSet (sourceFoldGood L k₀ r) := by
  exact (measurableSet_le (((sourceT_measurable L k₀).pow_const 5).const_mul r)
    measurable_const).inter
      (measurableSet_le (((sourceT_measurable L k₀).pow_const 5).const_mul 1024)
        (sourceKappa_measurable hL r (1/6)))

/-- Scalar arithmetic retaining every scale factor and the division by r.
The curvature obstruction is closed, although failure of the cutoff is strict. -/
theorem cutoff_failure_inclusion (lam r Γ q : ℝ) (hlam : 0 < lam) (hr : 0 < r)
    (hbad : ¬ (r*(lam*Γ)^5 ≤ 1/100 ∧ 1024*(lam*Γ)^5 ≤ -q/r)) :
    1/(100*lam^5) < r*Γ^5 ∨ -(1024*lam^5)*r*Γ^5 ≤ q := by
  rcases not_and_or.mp hbad with h | h
  · left
    have hf : (1 : ℝ)/100 < (r*Γ^5)*lam^5 := by
      convert lt_of_not_ge h using 1 <;> ring
    apply (div_lt_iff₀ (mul_pos (by norm_num : (0:ℝ) < 100) (pow_pos hlam 5))).2
    nlinarith
  · right
    have hf := (div_lt_iff₀ hr).mp (lt_of_not_ge h)
    have heq : 1024*(lam*Γ)^5*r = (1024*lam^5)*r*Γ^5 := by ring
    rw [heq] at hf
    linarith

theorem sourceFoldGood_compl_subset (L k₀ r : ℝ) (hr : 0 < r) :
    (sourceFoldGood L k₀ r)ᶜ ⊆
      sourceRegularityBad L r (sourceCutoffEps k₀) ∪
        sourceCurvatureOneSided L r (sourceCutoffA k₀) := by
  intro sample hs
  change ¬ (_ ∧ _) at hs
  rw [sourceT_eq_scale, sourceKappa_one_sixth] at hs
  exact cutoff_failure_inclusion (sourceScale k₀) r (sourceGammaRadius L sample)
    (sourceQ L sample) (sourceScale_pos k₀) hr hs

theorem sourceFoldWeightedLaw_eq {L : ℝ} (hL : L ≠ 0) (r b : ℝ) :
    sourceFoldWeightedLaw hL r b = sourceSmoothWeightedLaw hL r b := by
  unfold sourceFoldWeightedLaw sourceSmoothWeightedLaw
  rw [sourceGapLaw_one_sixth]

/-- Absolute continuity is derived for the same literal gap law and weight. -/
theorem sourceFoldWeightedLaw_absolutelyContinuous {L : ℝ} (hL : L ≠ 0) (r b : ℝ) :
    sourceFoldWeightedLaw hL r b ≪ sourceGapLaw hL r b (1/6) :=
  prwMeasure_absolutelyContinuous _ _

/-- Fixed b and any positive lower scale: the normalized bad probability is cubic.
All constants, probability and the normalizer facts come from the old bound. -/
theorem sourceFoldWeightedProbability_bound {L : ℝ} (hL : L ≠ 0) (b k₀ : ℝ)
    (_hk₀ : 0 < k₀) :
    ∃ C δ : ℝ, 0 ≤ C ∧ 0 < δ ∧ δ ≤ 1 ∧
      ∀ r : ℝ, 0 < r → r < δ →
        IsProbabilityMeasure (sourceFoldWeightedLaw hL r b) ∧
        (sourceFoldWeightedLaw hL r b).real (sourceFoldGood L k₀ r)ᶜ ≤ C*r^3 := by
  obtain ⟨C,δ,hC,hδ,hδ1,h⟩ := sourceWeightedCurvature_bound hL b
    (sourceCutoffA k₀) (sourceCutoffEps k₀) (sourceCutoffA_nonneg k₀)
    (sourceCutoffEps_pos k₀)
  refine ⟨C,δ,hC,hδ,hδ1,?_⟩
  intro r hr hrδ
  obtain ⟨hp,hb⟩ := h r hr hrδ
  rw [← sourceFoldWeightedLaw_eq hL r b] at hp hb
  let _ := hp
  exact ⟨hp, (measureReal_mono (sourceFoldGood_compl_subset L k₀ r hr)).trans hb⟩

/-- One derived radius works before the coefficient field is chosen. On the
literal cutoff event, weighted-almost every sample has an actual ordinary-H0
interval [-b,-(b-r³/6)) and complement, with exact strict clearance and sSup.
The interval and probability constants need only L,b,k₀, not r or K. -/
theorem sourceFoldWeightedProbability_h0 {L : ℝ} (hL : L ≠ 0) (b k₀ : ℝ)
    (hk₀ : 0 < k₀) (hk : k₀ ≤ 1/6) :
    ∃ C δ : ℝ, 0 ≤ C ∧ 0 < δ ∧ δ ≤ 1 ∧
      ∀ r : ℝ, 0 < r → r < δ →
        IsProbabilityMeasure (sourceFoldWeightedLaw hL r b) ∧
        (sourceFoldWeightedLaw hL r b).real (sourceFoldGood L k₀ r)ᶜ ≤ C*r^3 ∧
        ∀ (K : Type) [Field K], ∀ᵐ sample ∂sourceFoldWeightedLaw hL r b,
          sample ∈ sourceFoldGood L k₀ r →
            ∃ D : ℝ ⥤ ModuleCat K,
              Nonempty (superlevel_h0Filtration (actualTorusField hL sample)
                (ModuleCat.of K K) ≅ elderInterval K b (b-r^3/6) ⊞ D) ∧
              strictClearanceSet (actualTorusField hL sample)
                (torusProjection 2 L (endpointM r)) = Iio (b-r^3/6) ∧
              strictClearanceDeath (actualTorusField hL sample)
                (torusProjection 2 L (endpointM r)) = b-r^3/6 := by
  obtain ⟨C,δP,hC,hδP,hδP1,hP⟩ := sourceFoldWeightedProbability_bound hL b k₀ hk₀
  obtain ⟨δH,hδH,_hδH1,hH⟩ := sourceGapLaw_actual_torus_h0 hL
  refine ⟨C,min δP δH,hC,lt_min hδP hδH,(min_le_left _ _).trans hδP1,?_⟩
  intro r hr hrδ
  obtain ⟨hp,hb⟩ := hP r hr (lt_of_lt_of_le hrδ (min_le_left _ _))
  refine ⟨hp,hb,?_⟩
  intro K instK
  have hs := (sourceFoldWeightedLaw_absolutelyContinuous hL r b).ae_le
    (hH K k₀ hk₀ r hr (lt_of_lt_of_le hrδ (min_le_right _ _)) b (1/6) hk)
  filter_upwards [hs] with sample hs
  intro hgood
  have hh := hs hgood.1 hgood.2
  convert hh using 1 <;> ring

end SourceFoldWeightedProbability
