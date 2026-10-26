import SourcePinCurvatureBounds
import ScalarProductCurvatureBound
import SourceCurvatureDecomposition

/-!
# Actual cubic weighted curvature layer

The regularity remainder is controlled by the thirtieth actual conditional
radius moment and the completed whole-carrier square-root event transfer.
The regular curvature layer uses the actual scalar/residual product law;
no scalar density, covariance, moment or desired event estimate is an actual
source premise. See `SOURCE_WEIGHTED_CURVATURE_BOUND.md` for the frozen scope.
-/

noncomputable section

open I4SmoothCarrier I4SourceSmoothConditional I4SourceEndpointRegression I4SourceSmoothPalm
open I4SourceConditionalMajorant I4SourcePinCurvatureBounds I4ScalarProductCurvature I4SourceEndpointEstimates
open I4SourceCurvatureDecomposition I4SourceContact
open MeasureTheory ProbabilityTheory Set Filter ResearchFormalCoreR1
open scoped BigOperators Topology
set_option autoImplicit false

namespace I4SourceWeightedCurvature

def sourceRegularityBad (L r eps : ℝ) : Set (SmoothSample 2 L) :=
  {ω | eps < r * sourceGammaRadius L ω ^ 5}

theorem sourceRegularityBad_measurable (L r eps : ℝ) :
    MeasurableSet (sourceRegularityBad L r eps) :=
  measurableSet_lt measurable_const
    (((sourceGammaRadius_measurable L).pow_const 5).const_mul r)

/-- A sixth-power Markov estimate uses exactly the actual thirtieth radius moment. -/
theorem sourceRegularityBad_base_bound {L : ℝ} (hL : L ≠ 0) (r b eps M : ℝ)
    (hr : 0 < r) (heps : 0 < eps)
    (hR : Integrable (fun ω => sourceGammaRadius L ω ^ 30) (sourceSmoothLaw hL r b))
    (hbound : (∫ ω, sourceGammaRadius L ω ^ 30 ∂sourceSmoothLaw hL r b) ≤ M) :
    (sourceSmoothLaw hL r b).real (sourceRegularityBad L r eps) ≤ (M/eps^6)*r^6 := by
  let Q := sourceSmoothLaw hL r b
  have : IsProbabilityMeasure Q := inferInstance
  have hint : Integrable (fun ω => (r * sourceGammaRadius L ω^5)^6) Q := by
    simpa only [mul_pow, ← pow_mul] using hR.const_mul (r^6)
  have hnon : 0 ≤ᵐ[Q] (fun ω => (r * sourceGammaRadius L ω^5)^6) :=
    Eventually.of_forall (fun ω => by positivity)
  have hMarkov := mul_meas_ge_le_integral_of_nonneg hnon hint (eps^6)
  have hsub : sourceRegularityBad L r eps ⊆
      {ω | eps^6 ≤ (r * sourceGammaRadius L ω^5)^6} := by
    intro ω hω
    exact pow_le_pow_left₀ heps.le hω.le 6
  have hp : eps^6 * Q.real (sourceRegularityBad L r eps) ≤ r^6*M := by
    calc
      _ ≤ eps^6 * Q.real {ω | eps^6 ≤ (r * sourceGammaRadius L ω^5)^6} :=
        mul_le_mul_of_nonneg_left (measureReal_mono hsub) (pow_nonneg heps.le 6)
      _ ≤ ∫ ω, (r * sourceGammaRadius L ω^5)^6 ∂Q := hMarkov
      _ = r^6 * ∫ ω, sourceGammaRadius L ω^30 ∂Q := by
        simp only [mul_pow, ← pow_mul]
        rw [integral_const_mul]
      _ ≤ r^6*M := mul_le_mul_of_nonneg_left hbound (pow_nonneg hr.le 6)
  calc
    _ ≤ (r^6*M)/(eps^6) := (le_div_iff₀ (pow_pos heps 6)).2 (by simpa [mul_comm] using hp)
    _ = _ := by ring

/-- The completed whole-carrier square-root transfer turns the sixth-power base tail
into a genuine cubic bound under the literal determinant-weighted source law. -/
theorem sourceRegularityBad_weighted_cubic {L : ℝ} (hL : L ≠ 0) (b eps : ℝ)
    (heps : 0 < eps) :
    ∃ B δ : ℝ, 0 ≤ B ∧ 0 < δ ∧ δ ≤ 1 ∧ ∀ r : ℝ, 0 < r → r < δ →
      IsProbabilityMeasure (sourceSmoothWeightedLaw hL r b) ∧
      (sourceSmoothWeightedLaw hL r b).real (sourceRegularityBad L r eps) ≤ B*r^3 := by
  obtain ⟨δR,hδR,hδR1,hRm⟩ := sourceGammaRadius_moments hL b
  obtain ⟨M,hM,hR30⟩ := hRm 30
  obtain ⟨C,c,δP,hC,hc,hδP,hδP1,hPalm⟩ := sourceSmoothPalm_estimates hL b
  let A := Real.sqrt C/c
  let T := M/eps^6
  have hA : 0 ≤ A := div_nonneg (Real.sqrt_nonneg _) hc.le
  have hT : 0 ≤ T := div_nonneg hM (pow_nonneg heps.le 6)
  refine ⟨A*Real.sqrt T,min δR δP,mul_nonneg hA (Real.sqrt_nonneg _),
    lt_min hδR hδP,(min_le_left _ _).trans hδR1,?_⟩
  intro r hr hrδ
  have hrR : r < δR := lt_of_lt_of_le hrδ (min_le_left _ _)
  have hrP : r < δP := lt_of_lt_of_le hrδ (min_le_right _ _)
  obtain ⟨h30,hM30⟩ := hR30 r hr hrR
  have hbase := sourceRegularityBad_base_bound hL r b eps M hr heps h30 hM30
  have hp := hPalm r hr hrP
  have he := hp.2.2.2.2.1 (sourceRegularityBad L r eps) (sourceRegularityBad_measurable L r eps)
  have hsqrt : Real.sqrt ((sourceSmoothLaw hL r b).real (sourceRegularityBad L r eps)) ≤
      Real.sqrt T*r^3 := by
    calc
      _ ≤ Real.sqrt (T*r^6) := Real.sqrt_le_sqrt hbase
      _ = _ := by
        rw [Real.sqrt_mul hT, show r^6 = (r^3)^2 by ring, Real.sqrt_sq (pow_nonneg hr.le 3)]
  refine ⟨hp.2.2.2.1,?_⟩
  exact he.trans (by
    change A*Real.sqrt ((sourceSmoothLaw hL r b).real (sourceRegularityBad L r eps)) ≤
      A*Real.sqrt T*r^3
    simpa only [mul_assoc] using mul_le_mul_of_nonneg_left hsqrt hA)

def sourceCurvatureSlab (L r K : ℝ) : Set (SmoothSample 2 L) :=
  {ω | |sourceQ L ω| ≤ K*r*sourceGammaRadius L ω^5}

def sourceRegularCurvatureSlab (L r K eps : ℝ) : Set (SmoothSample 2 L) :=
  {ω | r*sourceGammaRadius L ω^5 ≤ eps ∧ |sourceQ L ω| ≤ K*r*sourceGammaRadius L ω^5}

def sourceCurvatureOneSided (L r K : ℝ) : Set (SmoothSample 2 L) :=
  {ω | -K*r*sourceGammaRadius L ω^5 ≤ sourceQ L ω}

lemma sourceQ_measurable_actual {L : ℝ} (hL : L ≠ 0) : Measurable (sourceQ L) := by
  have heq : sourceQ L = fun ω => I4Foundation.scalarSeries
      (I4SourceDerivativeGaussian.derivativeCoefficient 2 L 2 0
        ![I4SourceConfluentPins.directionY,I4SourceConfluentPins.directionY]) ω.val := by
    funext ω
    exact I4SourceDerivativeGaussian.smoothSourceField_derivative_series 2 hL ω 2 0 _
  rw [heq]
  exact (I4Foundation.scalarSeries_measurable _).comp measurable_subtype_coe

theorem sourceCurvatureSlab_measurable {L : ℝ} (hL : L ≠ 0) (r K : ℝ) :
    MeasurableSet (sourceCurvatureSlab L r K) :=
  measurableSet_le (sourceQ_measurable_actual hL).abs
    (((sourceGammaRadius_measurable L).pow_const 5).const_mul (K*r))

theorem sourceRegularCurvatureSlab_measurable {L : ℝ} (hL : L ≠ 0) (r K eps : ℝ) :
    MeasurableSet (sourceRegularCurvatureSlab L r K eps) :=
  (measurableSet_le (((sourceGammaRadius_measurable L).pow_const 5).const_mul r)
    measurable_const).inter (sourceCurvatureSlab_measurable hL r K)

theorem sourceCurvatureOneSided_measurable {L : ℝ} (hL : L ≠ 0) (r K : ℝ) :
    MeasurableSet (sourceCurvatureOneSided L r K) :=
  measurableSet_le (((sourceGammaRadius_measurable L).pow_const 5).const_mul (-K*r))
    (sourceQ_measurable_actual hL)

/-- Dividing an r⁵ regular-layer numerator by the actual r² normalizer gives r³. -/
theorem sourceRegularCurvatureSlab_weighted_of_numerator {L : ℝ} (hL : L ≠ 0)
    (r b K eps N c : ℝ) (hr : 0 < r) (hN : 0 ≤ N) (hc : 0 < c)
    (hW : Integrable (sourceSmoothWeight L r) (sourceSmoothLaw hL r b))
    (hf : c*r^2 ≤ ∫ ω, sourceSmoothWeight L r ω ∂sourceSmoothLaw hL r b)
    (hn : (∫ ω in sourceRegularCurvatureSlab L r K eps, sourceSmoothWeight L r ω
      ∂sourceSmoothLaw hL r b) ≤ N*r^5) :
    (sourceSmoothWeightedLaw hL r b).real (sourceRegularCurvatureSlab L r K eps) ≤
      (N/c)*r^3 := by
  have hZ : 0 < ∫ ω, sourceSmoothWeight L r ω ∂sourceSmoothLaw hL r b :=
    (mul_pos hc (sq_pos_of_pos hr)).trans_le hf
  rw [sourceSmoothWeightedLaw,
    prw_measure_real _ _ hW (sourceSmoothWeight_nonneg L r) hZ _
      (sourceRegularCurvatureSlab_measurable hL r K eps)]
  calc
    _ ≤ (N*r^5)/(c*r^2) := div_le_div₀ (by positivity) hn (mul_pos hc (sq_pos_of_pos hr)) hf
    _ = _ := by field_simp [hr.ne']

/-- On the actual positive-weight pin support, the one-sided curvature event reduces
to the regular symmetric slab plus the bad-regularity event. -/
theorem sourceCurvatureUnion_reduce {L : ℝ} (hL : L ≠ 0) (r b K eps : ℝ)
    (hr : 0 < r) (hG : IsUnit (sourcePinCovarianceAt L r))
    [IsProbabilityMeasure (sourceSmoothWeightedLaw hL r b)]
    (hZ : 0 < ∫ ω, sourceSmoothWeight L r ω ∂sourceSmoothLaw hL r b) :
    (sourceSmoothWeightedLaw hL r b).real
        (sourceRegularityBad L r eps ∪ sourceCurvatureOneSided L r K) ≤
      (sourceSmoothWeightedLaw hL r b).real (sourceRegularityBad L r eps) +
        (sourceSmoothWeightedLaw hL r b).real (sourceRegularCurvatureSlab L r (max K 1) eps) := by
  let P := sourceSmoothWeightedLaw hL r b
  have hpin : ∀ᵐ ω ∂P, sourceConfluentPinsAt L r ω 3 = 0 ∧
      sourceConfluentPinsAt L r ω 4 = 0 ∧ sourceConfluentPinsAt L r ω 5 = 2 :=
    prwMeasure_ae_of_ae (sourceSmoothLaw hL r b) (sourceSmoothWeight L r)
      (source_prescribed_pin_constraints_ae hL r b hG)
  have hW : ∀ᵐ ω ∂P, 0 < sourceSmoothWeight L r ω :=
    prwMeasure_ae_weight_pos (sourceSmoothLaw hL r b) (sourceSmoothWeight L r)
      (sourceSmoothWeight_measurable hL r hr.ne') hZ
  have hsub : ∀ᵐ ω ∂P, ω ∈ sourceRegularityBad L r eps ∪ sourceCurvatureOneSided L r K →
      ω ∈ sourceRegularityBad L r eps ∪ sourceRegularCurvatureSlab L r (max K 1) eps := by
    filter_upwards [hpin,hW] with ω hpin hW hω
    rcases hω with hbad | hq
    · exact Or.inl hbad
    · by_cases hbad : eps < r*sourceGammaRadius L ω^5
      · exact Or.inl hbad
      · exact Or.inr ⟨le_of_not_gt hbad,
          source_bad_curvature_slab hL r hr ω hpin.1 hpin.2.1 hpin.2.2 hW K hq⟩
  calc
    _ ≤ P.real (sourceRegularityBad L r eps ∪ sourceRegularCurvatureSlab L r (max K 1) eps) :=
      ENNReal.toReal_mono (measure_ne_top _ _) (measure_mono_ae hsub)
    _ ≤ _ := measureReal_union_le _ _

/-- Exact pullback through an honest scalar/residual product law. The actual application
below derives this law and all uniform constants from the source decomposition. -/
theorem sourceRegularCurvatureSlab_numerator_of_product {L : ℝ} (hL : L ≠ 0)
    (r b K eps A D T : ℝ) (hr : 0 < r) (hr1 : r ≤ 1) (hK : 0 ≤ K)
    (heps : 0 < eps) (hA : 0 ≤ A) (hD : 0 ≤ D) (_hT : 0 ≤ T)
    (hG : IsUnit (sourcePinCovarianceAt L r))
    (ν : Measure ℝ) [IsProbabilityMeasure ν]
    (ρ : Measure (SmoothSample 2 L)) [IsProbabilityMeasure ρ]
    (Ψ : ℝ × SmoothSample 2 L → SmoothSample 2 L) (hΨ : Measurable Ψ)
    (hmap : (ν.prod ρ).map Ψ = sourceSmoothLaw hL r b)
    (hq : ∀ᵐ p ∂ν.prod ρ, sourceQ L (Ψ p) = p.1)
    (S : SmoothSample 2 L → ℝ) (hS : ∀ z, 1 ≤ S z)
    (hS17 : Integrable (fun z => S z^17) ρ) (hSbound : (∫ z, S z^17 ∂ρ) ≤ T)
    (hdom : ∀ p, sourceGammaRadius L (Ψ p) ≤ A*(|p.1|+S p.2))
    (hdensity : ∀ a : ℝ, 0 ≤ a → ν.real (Icc (-a) a) ≤ 2*D*a)
    (hW : Integrable (sourceSmoothWeight L r) (sourceSmoothLaw hL r b)) :
    let H := A*(1+K*eps)
    (∫ ω in sourceRegularCurvatureSlab L r K eps, sourceSmoothWeight L r ω
      ∂sourceSmoothLaw hL r b) ≤
      ((2*D*(K*H^5)*(2*K^2*H^12+8*H^4))*T)*r^5 := by
  let E := sourceRegularCurvatureSlab L r K eps
  let P := ν.prod ρ
  let pin : SmoothSample 2 L → Prop := fun ω => sourceConfluentPinsAt L r ω 3 = 0 ∧
    sourceConfluentPinsAt L r ω 4 = 0 ∧ sourceConfluentPinsAt L r ω 5 = 2
  have hpinMeas : MeasurableSet {ω | pin ω} := by
    apply MeasurableSet.inter
    · exact measurableSet_eq_fun ((measurable_pi_apply 3).comp (sourceConfluentPinsAt_measurable hL r)) measurable_const
    · exact (measurableSet_eq_fun ((measurable_pi_apply 4).comp (sourceConfluentPinsAt_measurable hL r)) measurable_const).inter
        (measurableSet_eq_fun ((measurable_pi_apply 5).comp (sourceConfluentPinsAt_measurable hL r)) measurable_const)
  have hpin : ∀ᵐ p ∂P, pin (Ψ p) := by
    have hh := source_prescribed_pin_constraints_ae hL r b hG
    rw [← hmap] at hh
    exact (ae_map_iff hΨ.aemeasurable hpinMeas).1 hh
  let e : Set (ℝ × SmoothSample 2 L) :=
    {p | Ψ p ∈ E ∧ pin (Ψ p) ∧ sourceQ L (Ψ p) = p.1}
  have hE : MeasurableSet E := sourceRegularCurvatureSlab_measurable hL r K eps
  have he : MeasurableSet e := (hE.preimage hΨ).inter
    ((hpinMeas.preimage hΨ).inter
      (measurableSet_eq_fun ((sourceQ_measurable_actual hL).comp hΨ) measurable_fst))
  let F : ℝ × SmoothSample 2 L → ℝ := fun p => sourceSmoothWeight L r (Ψ p)
  have hΨLaw : HasLaw Ψ (sourceSmoothLaw hL r b) P := ⟨hΨ.aemeasurable,hmap⟩
  have hF : Integrable F P := hΨLaw.integrable_comp hW
  have hEQ : (∫ ω in E, sourceSmoothWeight L r ω ∂sourceSmoothLaw hL r b) =
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
      have hh := sourceSmoothWeight_curvature_bound hL r hr hr1 (Ψ p)
        hp.2.1.1 hp.2.1.2.1 hp.2.1.2.2
      simpa only [hp.2.2] using hh)
  dsimp only at hprod
  rw [hEQ]
  calc
    _ ≤ (2*D*(K*H^5)*(2*K^2*H^12+8*H^4))*r^5*(∫ z, S z^17 ∂ρ) := hprod
    _ ≤ (2*D*(K*H^5)*(2*K^2*H^12+8*H^4))*r^5*T := by gcongr
    _ = _ := by ring

/-- Composition with an r⁵ regular numerator. The source product decomposition supplies
this numerator in the final theorem, while all other constants here are already actual. -/
theorem sourceCurvatureUnion_weighted_cubic_of_numerator {L : ℝ} (hL : L ≠ 0)
    (b K eps : ℝ) (heps : 0 < eps)
    (hregular : ∃ N δ : ℝ, 0 ≤ N ∧ 0 < δ ∧ ∀ r : ℝ, 0 < r → r < δ →
      (∫ ω in sourceRegularCurvatureSlab L r (max K 1) eps, sourceSmoothWeight L r ω
        ∂sourceSmoothLaw hL r b) ≤ N*r^5) :
    ∃ C δ : ℝ, 0 ≤ C ∧ 0 < δ ∧ δ ≤ 1 ∧ ∀ r : ℝ, 0 < r → r < δ →
      IsProbabilityMeasure (sourceSmoothWeightedLaw hL r b) ∧
      (sourceSmoothWeightedLaw hL r b).real
        (sourceRegularityBad L r eps ∪ sourceCurvatureOneSided L r K) ≤ C*r^3 := by
  obtain ⟨N,δN,hN,hδN,hnumerator⟩ := hregular
  obtain ⟨B,δB,hB,hδB,hδB1,hbad⟩ := sourceRegularityBad_weighted_cubic hL b eps heps
  obtain ⟨C0,c,δP,hC0,hc,hδP,hδP1,hPalm⟩ := sourceSmoothPalm_estimates hL b
  obtain ⟨δG,hδG,hGinterval⟩ := mem_nhdsGT_iff_exists_Ioo_subset.mp
    (sourceEndpoint_parameter_limits hL b).1
  let δ := min δN (min δB (min δP δG))
  have hδ : 0 < δ := lt_min hδN (lt_min hδB (lt_min hδP hδG))
  have hδB' : δ ≤ δB := (min_le_right _ _).trans (min_le_left _ _)
  have hδP' : δ ≤ δP := (min_le_right _ _).trans ((min_le_right _ _).trans (min_le_left _ _))
  have hδG' : δ ≤ δG := (min_le_right _ _).trans ((min_le_right _ _).trans (min_le_right _ _))
  refine ⟨B+N/c,δ,add_nonneg hB (div_nonneg hN hc.le),hδ,hδB'.trans hδB1,?_⟩
  intro r hr hrδ
  have hrN : r < δN := lt_of_lt_of_le hrδ (min_le_left _ _)
  have hrB : r < δB := lt_of_lt_of_le hrδ hδB'
  have hrP : r < δP := lt_of_lt_of_le hrδ hδP'
  have hG : IsUnit (sourcePinCovarianceAt L r) := hGinterval ⟨hr,lt_of_lt_of_le hrδ hδG'⟩
  obtain ⟨hsq,hm,hf,hprob,hevent,hmap,hraw,htyped⟩ := hPalm r hr hrP
  have : IsProbabilityMeasure (sourceSmoothWeightedLaw hL r b) := hprob
  have hW : Integrable (sourceSmoothWeight L r) (sourceSmoothLaw hL r b) :=
    prw_integrable_of_integrable_sq _ _ (sourceSmoothWeight_measurable hL r hr.ne') hsq
  have hZ : 0 < ∫ ω, sourceSmoothWeight L r ω ∂sourceSmoothLaw hL r b :=
    (mul_pos hc (sq_pos_of_pos hr)).trans_le hf
  have hreg := sourceRegularCurvatureSlab_weighted_of_numerator hL r b (max K 1) eps N c
    hr hN hc hW hf (hnumerator r hr hrN)
  have hbad' := (hbad r hr hrB).2
  refine ⟨hprob,?_⟩
  calc
    _ ≤ (sourceSmoothWeightedLaw hL r b).real (sourceRegularityBad L r eps) +
        (sourceSmoothWeightedLaw hL r b).real (sourceRegularCurvatureSlab L r (max K 1) eps) :=
      sourceCurvatureUnion_reduce hL r b K eps hr hG hZ
    _ ≤ B*r^3+(N/c)*r^3 := add_le_add hbad' hreg
    _ = _ := by ring

/-- The actual scalar-times-whole-residual law supplies an r⁵ regular-layer numerator.
All density, residual moments, domination and Gaussian variance facts are derived
by the source decomposition; they are not premises of this source theorem. -/
theorem sourceRegularCurvatureSlab_numerator {L : ℝ} (hL : L ≠ 0)
    (b K eps : ℝ) (hK : 0 ≤ K) (heps : 0 < eps) :
    ∃ N δ : ℝ, 0 ≤ N ∧ 0 < δ ∧ δ ≤ 1 ∧ ∀ r : ℝ, 0 < r → r < δ →
      (∫ ω in sourceRegularCurvatureSlab L r K eps, sourceSmoothWeight L r ω
        ∂sourceSmoothLaw hL r b) ≤ N*r^5 := by
  obtain ⟨δS,A,_H,hδS,hδS1,hA,_hH,hdom,_hresidual,hMom⟩ :=
    curvatureResidualRadius_uniform_bounds hL b
  obtain ⟨T,hT,hS17⟩ := hMom 17
  obtain ⟨D,δD,hD,hδD,hδD1,hdensity⟩ := curvatureScalarLaw_interval_mass_uniform hL
  obtain ⟨_B,_M,δG,_hB,_hM,hδG,hδG1,hparams⟩ := curvature_uniform_parameter_bounds hL b
  obtain ⟨_C,c,δP,_hC,hc,hδP,hδP1,hPalm⟩ := sourceSmoothPalm_estimates hL b
  let H := A*(1+K*eps)
  let N := (2*D*(K*H^5)*(2*K^2*H^12+8*H^4))*T
  let δ := min δS (min δD (min δG δP))
  have hδ : 0 < δ := lt_min hδS (lt_min hδD (lt_min hδG hδP))
  have hδD' : δ ≤ δD := (min_le_right _ _).trans (min_le_left _ _)
  have hδG' : δ ≤ δG := (min_le_right _ _).trans ((min_le_right _ _).trans (min_le_left _ _))
  have hδP' : δ ≤ δP := (min_le_right _ _).trans ((min_le_right _ _).trans (min_le_right _ _))
  refine ⟨N,δ,by dsimp [N,H]; positivity,hδ,(min_le_left _ _).trans hδS1,?_⟩
  intro r hr hrδ
  have hrS : r < δS := lt_of_lt_of_le hrδ (min_le_left _ _)
  have hrD : r < δD := lt_of_lt_of_le hrδ hδD'
  have hrG : r < δG := lt_of_lt_of_le hrδ hδG'
  have hrP : r < δP := lt_of_lt_of_le hrδ hδP'
  have hr1 : r ≤ 1 := hrS.le.trans hδS1
  obtain ⟨hG,hτfloor,_hbeta,_hmean⟩ := hparams r hr hrG
  have hτ : 0 < curvatureVariance L r :=
    (div_pos (sourceContactSchur_pos hL) (by norm_num)).trans_le hτfloor
  obtain ⟨hSInt,hSbound⟩ := hS17 r hr hrS
  obtain ⟨hsq,_hm,_hf,_hprob,_hevent,_hmap,_hraw,_htyped⟩ := hPalm r hr hrP
  have hW : Integrable (sourceSmoothWeight L r) (sourceSmoothLaw hL r b) :=
    prw_integrable_of_integrable_sq _ _ (sourceSmoothWeight_measurable hL r hr.ne') hsq
  let x := sourcePrescribedPins r b
  let ν := curvatureScalarLaw L r x
  let ρ := curvatureResidualLaw hL r
  let Ψ : ℝ × SmoothSample 2 L → SmoothSample 2 L :=
    fun p => curvatureReconstruct hL r x p.2 p.1
  have hΨ : Measurable Ψ := curvatureReconstruct_swap_measurable hL r x
  have hmap : (ν.prod ρ).map Ψ = sourceSmoothLaw hL r b :=
    (curvatureReconstruct_hasLaw hL r hG hτ x).map_eq
  have hq : ∀ᵐ p ∂ν.prod ρ, sourceQ L (Ψ p) = p.1 :=
    Eventually.of_forall (fun p => by
      rw [sourceQ_eq_sourceContactQ]
      exact curvatureReconstruct_Q hL r hτ x p.2 p.1)
  exact sourceRegularCurvatureSlab_numerator_of_product hL r b K eps A D T
    hr hr1 hK heps hA hD hT hG ν ρ Ψ hΨ hmap hq
    (curvatureResidualRadius hL r b) (one_le_curvatureResidualRadius hL r b)
    hSInt hSbound (fun p => hdom r hr hrS p.2 p.1)
    (hdensity r hr hrD x) hW

/-- Cubic weighted curvature-layer bound for the literal actual source law.
The only model inputs are the nonzero period, fixed height and scalar cutoff
parameters. No geometric noncapture or critical-point Palm conclusion is inferred. -/
theorem sourceWeightedCurvature_bound {L : ℝ} (hL : L ≠ 0) (b K eps : ℝ)
    (_hK : 0 ≤ K) (heps : 0 < eps) :
    ∃ C δ : ℝ, 0 ≤ C ∧ 0 < δ ∧ δ ≤ 1 ∧ ∀ r : ℝ, 0 < r → r < δ →
      IsProbabilityMeasure (sourceSmoothWeightedLaw hL r b) ∧
      (sourceSmoothWeightedLaw hL r b).real
        (sourceRegularityBad L r eps ∪ sourceCurvatureOneSided L r K) ≤ C*r^3 := by
  apply sourceCurvatureUnion_weighted_cubic_of_numerator hL b K eps heps
  obtain ⟨N,δ,hN,hδ,_hδ1,hreg⟩ := sourceRegularCurvatureSlab_numerator hL b (max K 1) eps
    ((by norm_num : (0:ℝ) ≤ 1).trans (le_max_right _ _)) heps
  exact ⟨N,δ,hN,hδ,hreg⟩

/-- The same source-only cubic bound also controls the symmetric curvature slab. -/
theorem sourceWeightedCurvature_slab_bound {L : ℝ} (hL : L ≠ 0) (b K eps : ℝ)
    (hK : 0 ≤ K) (heps : 0 < eps) :
    ∃ C δ : ℝ, 0 ≤ C ∧ 0 < δ ∧ δ ≤ 1 ∧ ∀ r : ℝ, 0 < r → r < δ →
      IsProbabilityMeasure (sourceSmoothWeightedLaw hL r b) ∧
      (sourceSmoothWeightedLaw hL r b).real (sourceCurvatureSlab L r K) ≤ C*r^3 := by
  obtain ⟨C,δ,hC,hδ,hδ1,hbound⟩ := sourceWeightedCurvature_bound hL b K eps hK heps
  refine ⟨C,δ,hC,hδ,hδ1,?_⟩
  intro r hr hrδ
  obtain ⟨hprob,hcurv⟩ := hbound r hr hrδ
  have : IsProbabilityMeasure (sourceSmoothWeightedLaw hL r b) := hprob
  refine ⟨hprob,le_trans (measureReal_mono (μ := sourceSmoothWeightedLaw hL r b) ?_) hcurv⟩
  intro ω hω
  apply Or.inr
  change |sourceQ L ω| ≤ K*r*sourceGammaRadius L ω^5 at hω
  change -K*r*sourceGammaRadius L ω^5 ≤ sourceQ L ω
  simpa only [neg_mul] using (abs_le.mp hω).1

end I4SourceWeightedCurvature
