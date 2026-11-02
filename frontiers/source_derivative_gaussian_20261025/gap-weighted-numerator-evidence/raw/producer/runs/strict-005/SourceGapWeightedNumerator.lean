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
  have : IsProbabilityMeasure Q := by
    change IsProbabilityMeasure (sourceSmoothKernel hL r (sourceGapPins r b k))
    infer_instance
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
    convert hh using 1; ring
  have hmajor : Integrable (fun ω => 100*r^4*sourceGammaRadius L ω^8)
      (sourceGapLaw hL r b k) := h8int.const_mul _
  have hsqint : Integrable (fun ω => sourceSmoothWeight L r ω^2) (sourceGapLaw hL r b k) := by
    apply hmajor.mono' ((sourceSmoothWeight_measurable hL r hr.ne').pow_const 2).aestronglyMeasurable
    filter_upwards [hsq] with ω hω
    simpa only [Real.norm_eq_abs,abs_of_nonneg (sq_nonneg (sourceSmoothWeight L r ω))] using hω
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
  have hsqrtW : Real.sqrt (∫ ω, sourceSmoothWeight L r ω^2 ∂sourceGapLaw hL r b k) ≤
      Real.sqrt C*r^2 := by
    calc
      _ ≤ Real.sqrt (C*r^4) := Real.sqrt_le_sqrt hsqbound
      _ = _ := by
        rw [Real.sqrt_mul hC,show r^4 = (r^2)^2 by ring,Real.sqrt_sq (sq_nonneg r)]
  have : IsProbabilityMeasure (sourceGapLaw hL r b k) := by
    change IsProbabilityMeasure (sourceSmoothKernel hL r (sourceGapPins r b k))
    infer_instance
  have hevent := prw_numerator_bound (sourceGapLaw hL r b k) (sourceSmoothWeight L r)
    (sourceSmoothWeight_measurable hL r hr.ne') (sourceSmoothWeight_nonneg L r) hsqint
    (sourceRegularityBad L r eps) (sourceRegularityBad_measurable L r eps)
  refine ⟨hsqint,hevent.trans ?_⟩
  calc
    _ ≤ Real.sqrt C*r^2*(Real.sqrt T*r^3) :=
      mul_le_mul hsqrtW hsqrt (Real.sqrt_nonneg _) (by positivity)
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
