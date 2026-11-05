import SourceGapPinCurvature
import SourceAllTargetCurvatureResidual
import SourceWeightedCurvatureBound

/-!
# Actual varying-gap unnormalized bad-event numerator

The physical determinant weight and original signed-period carrier are retained.
All-target source support, moments, scalar product law and density are derived
from existing source estimates. The conclusion is an unnormalized r^5 integral;
no positive normalizer, weighted probability or parent theorem is asserted.
-/

noncomputable section

open I4SmoothCarrier I4SourceSmoothConditional I4SourceEndpointRegression
open I4SourceSmoothPalm I4SourceConditionalMajorant I4SourcePinCurvatureBounds
open I4SourceCompactTargetMoments I4SourceGapPinCurvature
open I4SourceAllTargetCurvatureResidual I4SourceCurvatureDecomposition
open I4SourceWeightedCurvature I4ScalarProductCurvature I4SourceContact
open I4SourceEndpointEstimates MeasureTheory ProbabilityTheory Set Filter
open ResearchFormalCoreR1
open scoped BigOperators Topology

set_option autoImplicit false

namespace I4SourceGapWeightedNumerator

/-- One interval chosen from the nonzero signed period alone gives integrability
of the actual physical weight at every real height and cubic-gap mark. -/
theorem sourceGapLaw_weight_integrable {L : ℝ} (hL : L ≠ 0) :
    ∃ δ : ℝ, 0 < δ ∧ δ ≤ 1 ∧ ∀ r : ℝ, 0 < r → r < δ → ∀ b k : ℝ,
      Integrable (sourceSmoothWeight L r) (sourceGapLaw hL r b k) := by
  obtain ⟨δW,hδW,hδW1,hW⟩ := sourceGapLaw_curvature_bounds hL
  obtain ⟨δR,hδR,_hδR1,hmom⟩ := sourceGammaRadius_allTarget_moments hL
  obtain ⟨_C,_hC,h4⟩ := hmom 4
  refine ⟨min δW δR,lt_min hδW hδR,(min_le_left _ _).trans hδW1,?_⟩
  intro r hr hrδ b k
  have hrW : r < δW := lt_of_lt_of_le hrδ (min_le_left _ _)
  have hrR : r < δR := lt_of_lt_of_le hrδ (min_le_right _ _)
  have hR : Integrable (fun ω => sourceGammaRadius L ω^4) (sourceGapLaw hL r b k) :=
    (h4 r hr hrR (sourceGapPins r b k)).1
  apply (hR.const_mul (10*r^2)).mono'
    (sourceSmoothWeight_measurable hL r hr.ne').aestronglyMeasurable
  filter_upwards [hW r hr hrW b k] with ω hω
  rw [Real.norm_eq_abs,abs_of_nonneg (sourceSmoothWeight_nonneg L r ω)]
  exact hω.2.2.1


/-- Existing all-height moments specialized uniformly to a compact height set.
The radius is chosen before the moment order and every displayed mark. -/
theorem sourceGapLaw_compact_moments {L : ℝ} (hL : L ≠ 0)
    (B K : ℝ) (hB : 0 ≤ B) (hK : 0 ≤ K) :
    ∃ δ : ℝ, 0 < δ ∧ δ ≤ 1 ∧ ∀ n : ℕ, ∃ C : ℝ, 0 ≤ C ∧
      ∀ r : ℝ, 0 < r → r < δ → ∀ b k : ℝ, |b| ≤ B → |k| ≤ K →
        Integrable (fun ω => sourceGammaRadius L ω^n) (sourceGapLaw hL r b k) ∧
        (∫ ω, sourceGammaRadius L ω^n ∂sourceGapLaw hL r b k) ≤ C := by
  obtain ⟨δ,hδ,hδ1,hmom⟩ := sourceGapLaw_height_moments hL K hK
  refine ⟨δ,hδ,hδ1,?_⟩
  intro n
  obtain ⟨C,hC,hbound⟩ := hmom n
  refine ⟨C*(1+B)^n,by positivity,?_⟩
  intro r hr hrδ b k hb hk
  obtain ⟨hint,hbound⟩ := hbound r hr hrδ b k hk
  exact ⟨hint,hbound.trans (mul_le_mul_of_nonneg_left
    (pow_le_pow_left₀ (by positivity) (by linarith : 1+|b| ≤ 1+B) n) hC)⟩

/-- Sixth-power Markov for the literal varying-gap law. This is the retained
thirtieth-moment calculation with its actual measure changed to the gap law. -/
theorem sourceGapLaw_regularity_base_bound {L : ℝ} (hL : L ≠ 0)
    (r b k eps M : ℝ) (hr : 0 < r) (heps : 0 < eps)
    (hR : Integrable (fun ω => sourceGammaRadius L ω^30) (sourceGapLaw hL r b k))
    (hbound : (∫ ω, sourceGammaRadius L ω^30 ∂sourceGapLaw hL r b k) ≤ M) :
    (sourceGapLaw hL r b k).real (sourceRegularityBad L r eps) ≤ (M/eps^6)*r^6 := by
  let Q := sourceGapLaw hL r b k
  have hint : Integrable (fun ω => (r*sourceGammaRadius L ω^5)^6) Q := by
    simpa only [mul_pow, ← pow_mul] using hR.const_mul (r^6)
  have hnon : 0 ≤ᵐ[Q] (fun ω => (r*sourceGammaRadius L ω^5)^6) :=
    Eventually.of_forall (fun ω => by positivity)
  have hMarkov := mul_meas_ge_le_integral_of_nonneg hnon hint (eps^6)
  have hsub : sourceRegularityBad L r eps ⊆
      {ω | eps^6 ≤ (r*sourceGammaRadius L ω^5)^6} := by
    intro ω hω
    exact pow_le_pow_left₀ heps.le hω.le 6
  have hp : eps^6*Q.real (sourceRegularityBad L r eps) ≤ r^6*M := by
    calc
      _ ≤ eps^6*Q.real {ω | eps^6 ≤ (r*sourceGammaRadius L ω^5)^6} :=
        mul_le_mul_of_nonneg_left (measureReal_mono hsub) (pow_nonneg heps.le 6)
      _ ≤ ∫ ω, (r*sourceGammaRadius L ω^5)^6 ∂Q := hMarkov
      _ = r^6*∫ ω, sourceGammaRadius L ω^30 ∂Q := by
        simp only [mul_pow, ← pow_mul]
        rw [integral_const_mul]
      _ ≤ r^6*M := mul_le_mul_of_nonneg_left hbound (pow_nonneg hr.le 6)
  calc
    _ ≤ (r^6*M)/(eps^6) := (le_div_iff₀ (pow_pos heps 6)).2 (by simpa [mul_comm] using hp)
    _ = _ := by ring

/-- The physical square bound and sixth-power base tail give an r^5
unnormalized irregular-layer numerator by the existing event Cauchy-Schwarz. -/
theorem sourceGapLaw_regularity_numerator {L : ℝ} (hL : L ≠ 0)
    (B K eps : ℝ) (hB : 0 ≤ B) (hK : 0 ≤ K) (heps : 0 < eps) :
    ∃ N δ : ℝ, 0 ≤ N ∧ 0 < δ ∧ δ ≤ 1 ∧
      ∀ r : ℝ, 0 < r → r < δ → ∀ b k : ℝ, |b| ≤ B → |k| ≤ K →
        Integrable (fun ω => sourceSmoothWeight L r ω^2) (sourceGapLaw hL r b k) ∧
        (∫ ω in sourceRegularityBad L r eps, sourceSmoothWeight L r ω
          ∂sourceGapLaw hL r b k) ≤ N*r^5 := by
  obtain ⟨δR,hδR,hδR1,hmom⟩ := sourceGapLaw_compact_moments hL B K hB hK
  obtain ⟨M8,hM8,h8⟩ := hmom 8
  obtain ⟨M30,hM30,h30⟩ := hmom 30
  obtain ⟨δW,hδW,_hδW1,hW⟩ := sourceGapLaw_curvature_bounds hL
  let C := 100*M8
  let T := M30/eps^6
  have hC : 0 ≤ C := by dsimp [C]; positivity
  have hT : 0 ≤ T := div_nonneg hM30 (pow_nonneg heps.le 6)
  refine ⟨Real.sqrt C*Real.sqrt T,min δR δW,by positivity,
    lt_min hδR hδW,(min_le_left _ _).trans hδR1,?_⟩
  intro r hr hrδ b k hb hk
  have hrR : r < δR := lt_of_lt_of_le hrδ (min_le_left _ _)
  have hrW : r < δW := lt_of_lt_of_le hrδ (min_le_right _ _)
  obtain ⟨h8int,h8bound⟩ := h8 r hr hrR b k hb hk
  obtain ⟨h30int,h30bound⟩ := h30 r hr hrR b k hb hk
  have hsq : ∀ᵐ ω ∂sourceGapLaw hL r b k,
      sourceSmoothWeight L r ω^2 ≤ 100*r^4*sourceGammaRadius L ω^8 := by
    filter_upwards [hW r hr hrW b k] with ω hω
    have hh := pow_le_pow_left₀ (sourceSmoothWeight_nonneg L r ω) hω.2.2.1 2
    convert hh using 1 <;> ring
  have hmajor : Integrable (fun ω => 100*r^4*sourceGammaRadius L ω^8)
      (sourceGapLaw hL r b k) := h8int.const_mul _
  have hsqint : Integrable (fun ω => sourceSmoothWeight L r ω^2) (sourceGapLaw hL r b k) := by
    apply hmajor.mono' ((sourceSmoothWeight_measurable hL r hr.ne').pow_const 2).aestronglyMeasurable
    filter_upwards [hsq] with ω hω
    simpa only [Real.norm_eq_abs,abs_of_nonneg (sq_nonneg _)] using hω
  have hsqbound : (∫ ω, sourceSmoothWeight L r ω^2 ∂sourceGapLaw hL r b k) ≤ C*r^4 := by
    calc
      _ ≤ ∫ ω, 100*r^4*sourceGammaRadius L ω^8 ∂sourceGapLaw hL r b k :=
        integral_mono_ae hsqint hmajor hsq
      _ = 100*r^4*(∫ ω, sourceGammaRadius L ω^8 ∂sourceGapLaw hL r b k) := integral_const_mul _ _
      _ ≤ 100*r^4*M8 := mul_le_mul_of_nonneg_left h8bound (by positivity)
      _ = _ := by dsimp [C]; ring
  have hbase := sourceGapLaw_regularity_base_bound hL r b k eps M30 hr heps h30int h30bound
  have hsqrt : Real.sqrt ((sourceGapLaw hL r b k).real (sourceRegularityBad L r eps)) ≤
      Real.sqrt T*r^3 := by
    calc
      _ ≤ Real.sqrt (T*r^6) := Real.sqrt_le_sqrt hbase
      _ = _ := by
        rw [Real.sqrt_mul hT,show r^6 = (r^3)^2 by ring,Real.sqrt_sq (pow_nonneg hr.le 3)]
  have hLp : MemLp (sourceSmoothWeight L r) 2 (sourceGapLaw hL r b k) :=
    (memLp_two_iff_integrable_sq (sourceSmoothWeight_measurable hL r hr.ne').aestronglyMeasurable).mpr hsqint
  have hevent := p02_lm008_event_numerator (sourceGapLaw hL r b k) (sourceSmoothWeight L r)
    (sourceRegularityBad L r eps) hLp
    (Eventually.of_forall (sourceSmoothWeight_nonneg L r))
    (sourceRegularityBad_measurable L r eps) r C hC hsqbound
  refine ⟨hsqint,hevent.trans ?_⟩
  calc
    _ ≤ Real.sqrt C*r^2*(Real.sqrt T*r^3) :=
      mul_le_mul_of_nonneg_left hsqrt (by positivity)
    _ = _ := by ring

/-- Exact pullback at a literal gap target, with only the two zero-gradient pins. -/
theorem sourceGapLaw_regular_numerator_of_product {L : ℝ} (hL : L ≠ 0)
    (r b k K eps A D T : ℝ) (hr : 0 < r) (hK : 0 ≤ K)
    (heps : 0 < eps) (hA : 0 ≤ A) (hD : 0 ≤ D) (_hT : 0 ≤ T)
    (hG : IsUnit (sourcePinCovarianceAt L r))
    (ν : Measure ℝ) [IsProbabilityMeasure ν]
    (ρ : Measure (SmoothSample 2 L)) [IsProbabilityMeasure ρ]
    (Ψ : ℝ × SmoothSample 2 L → SmoothSample 2 L) (hΨ : Measurable Ψ)
    (hmap : (ν.prod ρ).map Ψ = sourceGapLaw hL r b k)
    (hq : ∀ᵐ p ∂ν.prod ρ, sourceQ L (Ψ p) = p.1)
    (S : SmoothSample 2 L → ℝ) (hS : ∀ z, 1 ≤ S z)
    (hS17 : Integrable (fun z => S z^17) ρ) (hSbound : (∫ z, S z^17 ∂ρ) ≤ T)
    (hdom : ∀ p, sourceGammaRadius L (Ψ p) ≤ A*(|p.1|+S p.2))
    (hdensity : ∀ a : ℝ, 0 ≤ a → ν.real (Icc (-a) a) ≤ 2*D*a)
    (hW : Integrable (sourceSmoothWeight L r) (sourceGapLaw hL r b k)) :
    let H := A*(1+K*eps)
    (∫ ω in sourceRegularCurvatureSlab L r K eps, sourceSmoothWeight L r ω
      ∂sourceGapLaw hL r b k) ≤
      ((2*D*(K*H^5)*(2*K^2*H^12+8*H^4))*T)*r^5 := by
  let E := sourceRegularCurvatureSlab L r K eps
  let P := ν.prod ρ
  let pin : SmoothSample 2 L → Prop := fun ω => sourceConfluentPinsAt L r ω 3 = 0 ∧
    sourceConfluentPinsAt L r ω 4 = 0
  have hpinMeas : MeasurableSet {ω | pin ω} := by
    apply MeasurableSet.inter
    · exact measurableSet_eq_fun ((measurable_pi_apply 3).comp (sourceConfluentPinsAt_measurable hL r)) measurable_const
    · exact measurableSet_eq_fun ((measurable_pi_apply 4).comp (sourceConfluentPinsAt_measurable hL r)) measurable_const
  have hpin : ∀ᵐ p ∂P, pin (Ψ p) := by
    have hh : ∀ᵐ ω ∂sourceGapLaw hL r b k, pin ω := by
      have hs := I4SourceGapPinCurvature.sourceSmoothKernel_curvature_bounds_ae hL r hr
        (sourceGapPins r b k) hG (by simp [sourceGapPins]) (by simp [sourceGapPins])
      filter_upwards [hs] with ω hω
      exact ⟨by simpa [sourceGapPins] using congrFun hω.1 3,
        by simpa [sourceGapPins] using congrFun hω.1 4⟩
    rw [← hmap] at hh
    exact (ae_map_iff hΨ.aemeasurable hpinMeas).1 hh
  let e : Set (ℝ × SmoothSample 2 L) :=
    {p | Ψ p ∈ E ∧ pin (Ψ p) ∧ sourceQ L (Ψ p) = p.1}
  have hE : MeasurableSet E := sourceRegularCurvatureSlab_measurable hL r K eps
  have he : MeasurableSet e := (hE.preimage hΨ).inter
    ((hpinMeas.preimage hΨ).inter
      (measurableSet_eq_fun ((sourceQ_measurable_actual hL).comp hΨ) measurable_fst))
  let F : ℝ × SmoothSample 2 L → ℝ := fun p => sourceSmoothWeight L r (Ψ p)
  have hΨLaw : HasLaw Ψ (sourceGapLaw hL r b k) P := ⟨hΨ.aemeasurable,hmap⟩
  have hF : Integrable F P := hΨLaw.integrable_comp hW
  have hEQ : (∫ ω in E, sourceSmoothWeight L r ω ∂sourceGapLaw hL r b k) =
      ∫ p in e, F p ∂P := by
    rw [← integral_indicator hE, ← hmap,
      integral_map hΨ.aemeasurable ((sourceSmoothWeight_measurable hL r hr.ne').indicator hE).aestronglyMeasurable,
      ← integral_indicator he]
    apply integral_congr_ae
    filter_upwards [hpin,hq] with p hp hqp
    by_cases hpE : Ψ p ∈ E
    · simp [e,F,hpE,hp,hqp]
    · simp [e,F,hpE]
  let H := A*(1+K*eps)
  have hH : 0 ≤ H := by dsimp [H]; positivity
  have hprod := scalar_product_regular_integral_bound ν ρ S hS hS17
    (fun p => sourceGammaRadius L (Ψ p))
    (fun p => sourceGammaRadius_nonneg L (Ψ p)) e he F hF
    r A K eps D hr.le hA hK heps.le hD hdensity
    (fun p _ => hdom p)
    (fun p hp => hp.1.1)
    (fun p hp => by rw [← hp.2.2]; exact hp.1.2)
    (fun p hp => by
      have hh := I4SourceGapPinCurvature.sourceSmoothWeight_curvature_bound hL r hr (Ψ p)
        hp.2.1.1 hp.2.1.2
      simpa only [hp.2.2] using hh)
  dsimp only at hprod
  rw [hEQ]
  calc
    _ ≤ (2*D*(K*H^5)*(2*K^2*H^12+8*H^4))*r^5*(∫ z, S z^17 ∂ρ) := hprod
    _ ≤ (2*D*(K*H^5)*(2*K^2*H^12+8*H^4))*r^5*T := by gcongr
    _ = _ := by ring


end I4SourceGapWeightedNumerator
