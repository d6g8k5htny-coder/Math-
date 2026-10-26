import SourceIntrinsicH0Interface
import SourceCompactFoldWeightedProbability
import SourceSmoothTopology
import Mathlib.Analysis.Calculus.FDeriv.Symmetric
import Mathlib.MeasureTheory.Constructions.BorelSpace.Order

/-! Fixed-axis literal intrinsic finite-bar event and its actual weighted mass.
Norm-Borel field and exact planar inertia adapters supply event measurability;
accepted compact cutoff estimates control its actual normalized complement.
No canonical global label, all-frame law or Parent result is asserted. -/

noncomputable section
open CategoryTheory Limits Set MeasureTheory BoundedContinuousFunction
open UniversalLaw.Spec.Lifetime I4LifetimeField I4SmoothCarrier
open I4SourceH0OlderClearance I4SourceIntrinsicH0Interface
open I4SourceActualFoldCandidate I4SourceSmoothTopology
open SourceCompactFoldWeightedProbability TorusFiltration
open I4SourceConfluentPins I4SourceRawPinConditioning
open I4SourceCompactTargetMoments I4SourceAdaptiveFoldEstimates
set_option autoImplicit false
namespace I4SourceIntrinsicH0WeightedProbability

/- Frozen BCF helper text integrated once; standalone helper uncompiled. -/
/- UNCOMPILED TEXT ONLY. Insert once inside namespace
   I4SourceIntrinsicH0WeightedProbability and its noncomputable section.
   Required imports are frozen separately in IMPORTS.txt. -/

open UniversalLaw.Spec.Lifetime TorusFiltration BoundedContinuousFunction MeasureTheory Set
open scoped BoundedContinuousFunction

private abbrev ScalarBCF := (E 2 →ᵇ ℝ)

private theorem bcfClearance_open (M : E 2) (h : ℝ) :
    IsOpen {F : ScalarBCF |
      h ∈ superlevelBar_clearanceSet (F : E 2 → ℝ) M} := by
  apply Metric.isOpen_iff.mpr
  intro F hF
  obtain ⟨P,hP,γ,hγ⟩ := hF
  obtain ⟨t₀,hmin⟩ :=
    superlevelBar_path_minimum (F : E 2 → ℝ) F.continuous γ
  let ε : ℝ := min ((F P - F M) / 4) ((F (γ t₀) - h) / 2)
  have hε : 0 < ε := by
    apply lt_min
    · linarith
    · have ht₀ := hγ t₀
      linarith
  refine ⟨ε,hε,?_⟩
  intro G hG
  have hGF : dist G F < ε := hG
  have hpert (x : E 2) : |G x - F x| < ε := by
    have hx : dist (G x) (F x) ≤ dist G F :=
      BoundedContinuousFunction.dist_coe_le_dist x
    exact lt_of_le_of_lt (by simpa only [Real.dist_eq] using hx) hGF
  have hεgap : ε ≤ (F P - F M) / 4 := min_le_left _ _
  have hεpath : ε ≤ (F (γ t₀) - h) / 2 := min_le_right _ _
  refine ⟨P,?_,γ,?_⟩
  · have hM := abs_lt.mp (hpert M)
    have hP' := abs_lt.mp (hpert P)
    linarith
  · intro t
    have ht := abs_lt.mp (hpert (γ t))
    have hmt := hmin t
    have ht₀ := hγ t₀
    linarith

private theorem bcfNonempty_open (M : E 2) :
    IsOpen {F : ScalarBCF |
      (superlevelBar_clearanceSet (F : E 2 → ℝ) M).Nonempty} := by
  have hrat :
      {F : ScalarBCF |
        (superlevelBar_clearanceSet (F : E 2 → ℝ) M).Nonempty} =
      ⋃ q : ℚ, {F : ScalarBCF |
        (q : ℝ) ∈ superlevelBar_clearanceSet (F : E 2 → ℝ) M} := by
    ext F
    constructor
    · rintro ⟨h,hh⟩
      obtain ⟨q,hq⟩ := exists_rat_lt h
      exact Set.mem_iUnion.mpr ⟨q,
        superlevelBar_clearance_downward (F : E 2 → ℝ) M hq hh⟩
    · intro hF
      obtain ⟨q,hq⟩ := Set.mem_iUnion.mp hF
      exact ⟨(q : ℝ),hq⟩
  rw [hrat]
  exact isOpen_iUnion fun q : ℚ => bcfClearance_open M (q : ℝ)

private theorem bcfDeath_preimage (M : E 2) (h : ℝ) :
    {F : ScalarBCF | h < superlevelBar_deathHeight (F : E 2 → ℝ) M} =
      {F : ScalarBCF | h ∈ superlevelBar_clearanceSet (F : E 2 → ℝ) M} ∪
        (if h < 0 then
          {F : ScalarBCF |
            ¬ (superlevelBar_clearanceSet (F : E 2 → ℝ) M).Nonempty}
        else ∅) := by
  classical
  ext F
  by_cases hne : (superlevelBar_clearanceSet (F : E 2 → ℝ) M).Nonempty
  · have hnonessential : ¬ superlevelBar_isEssential (F : E 2 → ℝ) M :=
      (superlevelBar_clearance_nonempty_iff (F : E 2 → ℝ) F.continuous M).1 hne
    have hcut := superlevelBar_strict_cut
      (F : E 2 → ℝ) F.continuous M hnonessential h
    by_cases hh : h < 0 <;> simpa [hh,hne] using hcut
  · have hempty : superlevelBar_clearanceSet (F : E 2 → ℝ) M = ∅ :=
      Set.not_nonempty_iff_eq_empty.mp hne
    have hd : superlevelBar_deathHeight (F : E 2 → ℝ) M = 0 :=
      superlevelBar_death_eq_zero_of_empty (F : E 2 → ℝ) M hempty
    by_cases hh : h < 0 <;> simp [hh,hd,hempty]

private theorem bcfDeath_measurable (M : E 2) :
    @Measurable ScalarBCF ℝ (borel ScalarBCF) _
      (fun F => superlevelBar_deathHeight (F : E 2 → ℝ) M) := by
  borelize ScalarBCF
  apply measurable_of_Ioi
  intro h
  change MeasurableSet
    {F : ScalarBCF | h < superlevelBar_deathHeight (F : E 2 → ℝ) M}
  rw [bcfDeath_preimage M h]
  refine (bcfClearance_open M h).measurableSet.union ?_
  by_cases hh : h < 0
  · rw [ite_eq_left hh]
    exact (bcfNonempty_open M).measurableSet.compl
  · rw [ite_eq_right hh]
    exact MeasurableSet.empty

private def operatorEval (k : ℕ) (v : Fin k → (Fin 2 → ℝ)) :
    DerivativeOperator 2 k →L[ℝ] ℝ where
  toFun f := f v
  map_add' _ _ := rfl
  map_smul' _ _ := rfl
  cont := continuous_eval_const v

private def actualBCF {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) : E 2 →ᵇ ℝ :=
  ((operatorEval 0 (fun i => Fin.elim0 i)).compLeftContinuousBounded (Fin 2 → ℝ)
    (sourceDerivativeBCF 2 hL 0 ω)).compContinuous
      ⟨coordinates 2, (coordinates 2).continuous⟩

private theorem actualBCF_apply {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) (x : E 2) :
    actualBCF hL ω x = actualField 2 L ω x := by
  change sourceDerivativeBCF 2 hL 0 ω (coordinates 2 x) (fun i => Fin.elim0 i) = _
  simp only [sourceDerivativeBCF_apply, iteratedFDeriv_zero_apply, actualField]

private theorem actualBCF_measurable {L : ℝ} (hL : L ≠ 0) :
    @Measurable (SmoothSample 2 L) (E 2 →ᵇ ℝ) _ (borel _) (actualBCF hL) := by
  borelize (DerivativeBCF 2 0) (E 2 →ᵇ ℝ)
  have hc : Continuous (fun f : DerivativeBCF 2 0 =>
      ((operatorEval 0 (fun i => Fin.elim0 i)).compLeftContinuousBounded (Fin 2 → ℝ) f).compContinuous ⟨coordinates 2, (coordinates 2).continuous⟩) :=
    (BoundedContinuousFunction.compContinuousCLM ℝ ℝ
      ⟨coordinates 2, (coordinates 2).continuous⟩).continuous.comp
        ((operatorEval 0 (fun i => Fin.elim0 i)).compLeftContinuousBounded (Fin 2 → ℝ)).continuous
  exact hc.measurable.comp (sourceDerivativeBCF_borel 2 hL 0)

private theorem jetScalar_measurable {L : ℝ} (hL : L ≠ 0) (k : ℕ)
    (x : Fin 2 → ℝ) (v : Fin k → (Fin 2 → ℝ)) :
    Measurable (fun ω : SmoothSample 2 L =>
      iteratedFDeriv ℝ k (smoothSourceField 2 L ω) x v) := by
  borelize (DerivativeBCF 2 k) (DerivativeOperator 2 k)
  have hc : Continuous (fun f : DerivativeBCF 2 k => f x v) :=
    (operatorEval k v).continuous.comp (BoundedContinuousFunction.evalCLM ℝ x).continuous
  have hm := hc.measurable.comp (sourceDerivativeBCF_borel 2 hL k)
  change Measurable (fun ω => sourceDerivativeBCF 2 hL k ω x v) at hm
  simpa only [sourceDerivativeBCF_apply] using hm

private def basisX : E 2 := (coordinates 2).symm directionX
private def basisY : E 2 := (coordinates 2).symm directionY

private theorem actualCritical_iff {L : ℝ} (hL : 0 < L) (ω : SmoothSample 2 L) (x : E 2) :
    IsCriticalPoint 2 (actualField 2 L ω) x ↔
      fderiv ℝ (smoothSourceField 2 L ω) (coordinates 2 x) directionX = 0 ∧
      fderiv ℝ (smoothSourceField 2 L ω) (coordinates 2 x) directionY = 0 := by
  constructor
  · intro hc
    have hd := (smoothSourceField_smooth 2 hL.ne' ω).differentiable (by simp)
    have hchain := (hd (coordinates 2 x)).hasFDerivAt.comp x (coordinates 2).hasFDerivAt
    change fderiv ℝ (actualField 2 L ω) x = 0 at hc
    have hf : (fderiv ℝ (smoothSourceField 2 L ω) (coordinates 2 x)).comp
        (coordinates 2).toContinuousLinearMap = 0 := hchain.fderiv.symm.trans hc
    constructor
    · simpa [basisX] using congrArg (fun D => D basisX) hf
    · simpa [basisY] using congrArg (fun D => D basisY) hf
  · rintro ⟨hx,hy⟩
    exact actual_critical_of_coordinate_pins hL ω x hx hy

private theorem actualCritical_measurable {L : ℝ} (hL : 0 < L) (x : E 2) :
    MeasurableSet {ω : SmoothSample 2 L | IsCriticalPoint 2 (actualField 2 L ω) x} := by
  have hx := jetScalar_measurable hL.ne' 1 (coordinates 2 x) ![directionX]
  have hy := jetScalar_measurable hL.ne' 1 (coordinates 2 x) ![directionY]
  simp only [iteratedFDeriv_one_apply] at hx hy
  convert (measurableSet_eq_fun hx measurable_const).inter
    (measurableSet_eq_fun hy measurable_const) using 1
  ext ω
  exact actualCritical_iff hL ω x

private def hA (g : E 2 → ℝ) (x : E 2) : ℝ := hessian 2 g x basisX basisX
private def hB (g : E 2 → ℝ) (x : E 2) : ℝ := hessian 2 g x basisX basisY
private def hC (g : E 2 → ℝ) (x : E 2) : ℝ := hessian 2 g x basisY basisY

private theorem vector_decomp (v : E 2) :
    v = (coordinates 2 v 0) • basisX + (coordinates 2 v 1) • basisY := by
  apply (coordinates 2).injective
  simp only [map_add, map_smul, basisX, basisY, ContinuousLinearEquiv.apply_symm_apply]
  ext i
  fin_cases i <;> simp [directionX,directionY]

private theorem hessian_quadratic (g : E 2 → ℝ) (hg : ContDiff ℝ 2 g)
    (x v : E 2) :
    hessian 2 g x v v = hA g x * (coordinates 2 v 0)^2 +
      2 * hB g x * (coordinates 2 v 0) * (coordinates 2 v 1) +
      hC g x * (coordinates 2 v 1)^2 := by
  have hsym : fderiv ℝ (fderiv ℝ g) x basisY basisX =
      fderiv ℝ (fderiv ℝ g) x basisX basisY :=
    hg.contDiffAt.isSymmSndFDerivAt (by simp) basisY basisX
  unfold hA hB hC hessian
  simp only [iteratedFDeriv_two_apply, Matrix.cons_val_zero, Matrix.cons_val_one]
  conv_lhs => rw [vector_decomp v]
  simp only [map_add, map_smul, _root_.add_apply, _root_.smul_apply, smul_eq_mul]
  rw [hsym]
  ring

private theorem actualHessian_measurable {L : ℝ} (hL : 0 < L) (x v w : E 2) :
    Measurable (fun ω : SmoothSample 2 L => hessian 2 (actualField 2 L ω) x v w) := by
  have hm := jetScalar_measurable hL.ne' 2 (coordinates 2 x) ![coordinates 2 v, coordinates 2 w]
  convert hm using 1
  funext ω
  exact actual_hessian_coordinates hL ω x v w

/-- Literal fixed-axis intrinsic finite-bar membership on the original carrier. -/
def sourceIntrinsicFiniteBarEvent (L r : ℝ) : Set (SmoothSample 2 L) :=
  {ω | IsFiniteBar 2 L (h0Interface 2 L) (actualField 2 L ω)
    (endpointLiftM r) (endpointLiftS r)}

/-- The actual unchanged physical weighted law's mass of that literal event. -/
def sourceIntrinsicFiniteBarProbability {L : ℝ} (hL : 0 < L) (r b k : ℝ) : ℝ :=
  (sourceCompactFoldWeightedLaw hL.ne' r b k).real (sourceIntrinsicFiniteBarEvent L r)

private theorem actualBCF_coe_eq {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) :
    (actualBCF hL ω : E 2 → ℝ) = actualField 2 L ω :=
  funext (actualBCF_apply hL ω)

private theorem actualNonempty_measurable {L : ℝ} (hL : 0 < L) (M : E 2) :
    MeasurableSet {ω : SmoothSample 2 L |
      (superlevelBar_clearanceSet (actualField 2 L ω) M).Nonempty} := by
  borelize ScalarBCF
  have hm := (bcfNonempty_open M).measurableSet.preimage (actualBCF_measurable hL.ne')
  convert hm using 1
  ext ω
  change (superlevelBar_clearanceSet (actualField 2 L ω) M).Nonempty ↔
    (superlevelBar_clearanceSet (actualBCF hL.ne' ω : E 2 → ℝ) M).Nonempty
  rw [actualBCF_coe_eq]

private theorem actualDeath_measurable {L : ℝ} (hL : 0 < L) (M : E 2) :
    Measurable (fun ω : SmoothSample 2 L => superlevelBar_deathHeight (actualField 2 L ω) M) := by
  have hm := (bcfDeath_measurable M).comp (actualBCF_measurable hL.ne')
  change Measurable (fun ω => superlevelBar_deathHeight (actualBCF hL.ne' ω : E 2 → ℝ) M) at hm
  simpa only [actualBCF_coe_eq] using hm

private theorem wholeCut_iff_nonempty_death (g : E 2 → ℝ) (hg : Continuous g) (M S : E 2) :
    {h : ℝ | h0OlderClearance ℝ g M h} = Iio (g S) ↔
      (superlevelBar_clearanceSet g M).Nonempty ∧ superlevelBar_deathHeight g M = g S := by
  constructor
  · intro hc
    have hcut : superlevelBar_clearanceSet g M = Iio (g S) :=
      (h0Interface_cut_death_eq_C263 1 g hg M).1.symm.trans hc
    have hn : (superlevelBar_clearanceSet g M).Nonempty := by
      rw [hcut]
      exact ⟨g S - 1, sub_one_lt (g S)⟩
    refine ⟨hn,?_⟩
    rw [superlevelBar_death_eq_sSup_of_nonempty g M hn, hcut, csSup_Iio]
  · rintro ⟨hn,hd⟩
    have hne := (superlevelBar_clearance_nonempty_iff g hg M).1 hn
    exact (h0Interface_cut_death_eq_C263 1 g hg M).1.trans
      ((superlevelBar_clearance_eq_Iio g hg M hne).trans (congrArg Iio hd))

private theorem event_characterization {L : ℝ} (hL : 0 < L) (r : ℝ) (ω : SmoothSample 2 L) :
    ω ∈ sourceIntrinsicFiniteBarEvent L r ↔
      IsNondegMax 2 (actualField 2 L ω) (endpointLiftM r) ∧
      IsIndexSaddle 2 (actualField 2 L ω) (endpointLiftS r) ∧
      0 < torusDist 2 L (endpointLiftM r) (endpointLiftS r) ∧
      0 < heightGap 2 (actualField 2 L ω) (endpointLiftM r) (endpointLiftS r) ∧
      (superlevelBar_clearanceSet (actualField 2 L ω) (endpointLiftM r)).Nonempty ∧
      superlevelBar_deathHeight (actualField 2 L ω) (endpointLiftM r) =
        actualField 2 L ω (endpointLiftS r) := by
  change ((IsNondegMax 2 (actualField 2 L ω) (endpointLiftM r) ∧
      IsIndexSaddle 2 (actualField 2 L ω) (endpointLiftS r) ∧
      0 < torusDist 2 L (endpointLiftM r) (endpointLiftS r)) ∧
      0 < heightGap 2 (actualField 2 L ω) (endpointLiftM r) (endpointLiftS r) ∧
      (IsNondegMax 2 (actualField 2 L ω) (endpointLiftM r) ∧
      IsIndexSaddle 2 (actualField 2 L ω) (endpointLiftS r) ∧
      {h | h0OlderClearance ℝ (actualField 2 L ω) (endpointLiftM r) h} =
        Iio (actualField 2 L ω (endpointLiftS r)))) ↔ _
  rw [wholeCut_iff_nonempty_death _ (actualField_smooth 2 hL ω 0).continuous]
  constructor
  · rintro ⟨⟨hM,hS,hd⟩,hg,_hM,_hS,hn,hdeath⟩
    exact ⟨hM,hS,hd,hg,hn,hdeath⟩
  · rintro ⟨hM,hS,hd,hg,hn,hdeath⟩
    exact ⟨⟨hM,hS,hd⟩,hg,hM,hS,hn,hdeath⟩

private theorem probability_uniform_given_measurable {L : ℝ} (hL : 0 < L)
    (hE : ∀ r : ℝ, MeasurableSet (sourceIntrinsicFiniteBarEvent L r))
    (B k₀ k₁ : ℝ) (hB : 0 ≤ B) (hk₀ : 0 < k₀) (hk₀₁ : k₀ ≤ k₁) :
    ∃ C rStar : ℝ, 0 ≤ C ∧ 0 < rStar ∧ rStar ≤ 1 ∧ rStar ≤ L/2 ∧
      ∀ r : ℝ, 0 < r → r ≤ rStar → ∀ b k : ℝ, |b| ≤ B → k₀ ≤ k → k ≤ k₁ →
        let QW := sourceCompactFoldWeightedLaw hL.ne' r b k
        let E := sourceIntrinsicFiniteBarEvent L r
        let p := sourceIntrinsicFiniteBarProbability hL r b k
        IsProbabilityMeasure QW ∧ QW.real Eᶜ = 1-p ∧
          0 ≤ p ∧ p ≤ 1 ∧ 0 ≤ 1-p ∧ 1-p ≤ C*r^3 := by
  obtain ⟨C,δP,hC,hδP,hδP1,hP⟩ := sourceCompactFoldWeightedProbability_bound hL.ne'
    B k₀ k₁ hB hk₀ hk₀₁
  obtain ⟨δH,hδH,_hδH1,hδHL,hH⟩ := sourceGapLaw_intrinsic_h0_finiteBar_uniform hL
  have hmin : 0 < min δP δH := lt_min hδP hδH
  have hhalf : min δP δH / 2 < min δP δH := by linarith
  refine ⟨C,min δP δH / 2,hC,by positivity,?_,?_,?_⟩
  · exact hhalf.le.trans ((min_le_left _ _).trans hδP1)
  · exact hhalf.le.trans ((min_le_right _ _).trans hδHL)
  intro r hr hrStar b k hb hk hk'
  have hrP : r < δP := (hrStar.trans_lt hhalf).trans_le (min_le_left _ _)
  have hrH : r < δH := (hrStar.trans_lt hhalf).trans_le (min_le_right _ _)
  obtain ⟨hp,hbad⟩ := hP r hr hrP b k hb hk hk'
  let _ := hp
  have hs : ∀ᵐ ω ∂sourceCompactFoldWeightedLaw hL.ne' r b k,
      ω ∈ sourceCompactFoldGood L k₀ r k → ω ∈ sourceIntrinsicFiniteBarEvent L r := by
    have ha := (sourceCompactFoldWeightedLaw_absolutelyContinuous hL.ne' r b k).ae_le
      (hH ℝ k₀ hk₀ r hr hrH b k hk)
    filter_upwards [ha] with ω hω
    intro hgood
    exact (hω hgood.1 hgood.2).1
  have hsub : ∀ᵐ ω ∂sourceCompactFoldWeightedLaw hL.ne' r b k,
      ω ∈ (sourceIntrinsicFiniteBarEvent L r)ᶜ → ω ∈ (sourceCompactFoldGood L k₀ r k)ᶜ :=
    hs.mono (fun ω hω hnot hgood => hnot (hω hgood))
  have hmono := measure_mono_ae hsub
  have hm : (sourceCompactFoldWeightedLaw hL.ne' r b k).real
        (sourceIntrinsicFiniteBarEvent L r)ᶜ ≤
      (sourceCompactFoldWeightedLaw hL.ne' r b k).real
        (sourceCompactFoldGood L k₀ r k)ᶜ :=
    ENNReal.toReal_mono (measure_ne_top _ _) hmono
  have heq := probReal_compl_eq_one_sub
    (μ := sourceCompactFoldWeightedLaw hL.ne' r b k) (hE r)
  have hp0 : 0 ≤ sourceIntrinsicFiniteBarProbability hL r b k := measureReal_nonneg
  have hp1 : sourceIntrinsicFiniteBarProbability hL r b k ≤ 1 := measureReal_le_one
  refine ⟨hp,heq,hp0,hp1,sub_nonneg.mpr hp1,?_⟩
  change 1 - (sourceCompactFoldWeightedLaw hL.ne' r b k).real
    (sourceIntrinsicFiniteBarEvent L r) ≤ C*r^3
  rw [← heq]
  exact hm.trans hbad

end I4SourceIntrinsicH0WeightedProbability
