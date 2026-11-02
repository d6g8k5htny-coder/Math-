import SourceIntrinsicH0Interface
import SourceCompactFoldWeightedProbability
import SourceSmoothTopology
import Mathlib.Analysis.Calculus.FDeriv.Symmetric
import Mathlib.MeasureTheory.Constructions.BorelSpace.Order
import ResearchFormalCoreR1.DeterminantMoment
import Mathlib.LinearAlgebra.FiniteDimensional.Lemmas

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

/- Frozen genuine planar inertia helper integrated once; no standalone execution. -/
/- UNCOMPILED TEXT ONLY. Insert once inside namespace
   I4SourceIntrinsicH0WeightedProbability and its noncomputable section.
   The actual source/derivative transport is supplied by the producer. -/

open UniversalLaw.Spec.Lifetime I4LifetimeField ResearchFormalCoreR1
open scoped BigOperators

private def planarInertiaVector (u v : ℝ) : E 2 :=
  (coordinates 2).symm ![u,v]

private theorem planarInertiaVector_coordinates (u v : ℝ) :
    coordinates 2 (planarInertiaVector u v) = ![u,v] :=
  (coordinates 2).apply_symm_apply _

private theorem planarInertiaVector_quadratic
    (g : E 2 → ℝ) (x : E 2) (a b c : ℝ)
    (hQ : ∀ v : E 2, hessian 2 g x v v =
      a * (coordinates 2 v 0)^2 +
        2 * b * (coordinates 2 v 0) * (coordinates 2 v 1) +
        c * (coordinates 2 v 1)^2) (u v : ℝ) :
    hessian 2 g x (planarInertiaVector u v) (planarInertiaVector u v) =
      a*u^2 + 2*b*u*v + c*v^2 := by
  simpa only [planarInertiaVector_coordinates] using hQ (planarInertiaVector u v)

private theorem planar_all_negative_iff
    (g : E 2 → ℝ) (x : E 2) (a b c : ℝ)
    (hQ : ∀ v : E 2, hessian 2 g x v v =
      a * (coordinates 2 v 0)^2 +
        2 * b * (coordinates 2 v 0) * (coordinates 2 v 1) +
        c * (coordinates 2 v 1)^2) :
    (∀ v : E 2, v ≠ 0 → hessian 2 g x v v < 0) ↔
      a < 0 ∧ 0 < a*c-b^2 := by
  have hmatrix :
      (∀ v : E 2, v ≠ 0 → hessian 2 g x v v < 0) ↔
        dm2Negative !![a,b;b,c] := by
    constructor
    · intro hn v hv
      have hv' : (coordinates 2).symm v ≠ 0 := by
        intro hz
        apply hv
        simpa using congrArg (coordinates 2) hz
      have hval := hn ((coordinates 2).symm v) hv'
      rw [hQ] at hval
      have hscalar : a*(v 0)^2 + 2*b*(v 0)*(v 1) + c*(v 1)^2 < 0 := by
        simpa only [(coordinates 2).apply_symm_apply] using hval
      simp only [Fin.sum_univ_two]
      change v 0*a*v 0 + v 0*b*v 1 + (v 1*b*v 0 + v 1*c*v 1) < 0
      nlinarith [hscalar]
    · intro hm v hv
      have hv' : coordinates 2 v ≠ 0 := by
        intro hz
        apply hv
        apply (coordinates 2).injective
        simpa using hz
      have hval := hm (coordinates 2 v) hv'
      simp only [Fin.sum_univ_two] at hval
      change coordinates 2 v 0*a*coordinates 2 v 0 +
        coordinates 2 v 0*b*coordinates 2 v 1 +
        (coordinates 2 v 1*b*coordinates 2 v 0 +
          coordinates 2 v 1*c*coordinates 2 v 1) < 0 at hval
      rw [hQ]
      nlinarith [hval]
  exact hmatrix.trans (dm2_negative_iff a b c)

private theorem planar_det_neg_of_signs (a b c u₀ u₁ v₀ v₁ : ℝ)
    (hn : a*u₀^2 + 2*b*u₀*u₁ + c*u₁^2 < 0)
    (hp : 0 < a*v₀^2 + 2*b*v₀*v₁ + c*v₁^2) :
    a*c-b^2 < 0 := by
  by_contra hnot
  have hd : 0 ≤ a*c-b^2 := le_of_not_gt hnot
  rcases lt_trichotomy a 0 with ha | ha | ha
  · have hprod : a*(a*v₀^2 + 2*b*v₀*v₁ + c*v₁^2) < 0 :=
      mul_neg_of_neg_of_pos ha hp
    have hsum : 0 ≤ (a*v₀+b*v₁)^2 + (a*c-b^2)*v₁^2 :=
      add_nonneg (sq_nonneg _) (mul_nonneg hd (sq_nonneg _))
    have hid : a*(a*v₀^2 + 2*b*v₀*v₁ + c*v₁^2) =
        (a*v₀+b*v₁)^2 + (a*c-b^2)*v₁^2 := by ring
    nlinarith
  · have hb : b = 0 := by
      rw [ha] at hd
      nlinarith [sq_nonneg b]
    have hn' : c*u₁^2 < 0 := by simpa [ha,hb] using hn
    have hp' : 0 < c*v₁^2 := by simpa [ha,hb] using hp
    have hc : c < 0 := by
      by_contra hcn
      have hc0 : 0 ≤ c := le_of_not_gt hcn
      exact (not_lt_of_ge (mul_nonneg hc0 (sq_nonneg u₁))) hn'
    exact (not_lt_of_ge (mul_nonpos_of_nonpos_of_nonneg hc.le (sq_nonneg v₁))) hp'
  · have hprod : a*(a*u₀^2 + 2*b*u₀*u₁ + c*u₁^2) < 0 :=
      mul_neg_of_pos_of_neg ha hn
    have hsum : 0 ≤ (a*u₀+b*u₁)^2 + (a*c-b^2)*u₁^2 :=
      add_nonneg (sq_nonneg _) (mul_nonneg hd (sq_nonneg _))
    have hid : a*(a*u₀^2 + 2*b*u₀*u₁ + c*u₁^2) =
        (a*u₀+b*u₁)^2 + (a*c-b^2)*u₁^2 := by ring
    nlinarith

private theorem planar_inertia_one_of_sign_witnesses
    (g : E 2 → ℝ) (x : E 2) (a b c : ℝ)
    (hQ : ∀ v : E 2, hessian 2 g x v v =
      a * (coordinates 2 v 0)^2 +
        2 * b * (coordinates 2 v 0) * (coordinates 2 v 1) +
        c * (coordinates 2 v 1)^2)
    (n p : E 2) (hn : hessian 2 g x n n < 0)
    (hp : 0 < hessian 2 g x p p) : HessianHasInertia 2 g x 1 := by
  have hzero : hessian 2 g x 0 0 = 0 := by rw [hQ]; simp
  have hn0 : n ≠ 0 := by
    intro hz
    rw [hz,hzero] at hn
    exact (lt_irrefl (0 : ℝ)) hn
  have hp0 : p ≠ 0 := by
    intro hz
    rw [hz,hzero] at hp
    exact (lt_irrefl (0 : ℝ)) hp
  have hscale (t : ℝ) (v : E 2) :
      hessian 2 g x (t • v) (t • v) = t^2 * hessian 2 g x v v := by
    rw [hQ,hQ]
    simp only [map_smul,Pi.smul_apply,smul_eq_mul]
    ring
  have hnspan : ∀ v ∈ Submodule.span ℝ {n}, v ≠ 0 → hessian 2 g x v v < 0 := by
    intro v hv hv0
    obtain ⟨t,rfl⟩ := Submodule.mem_span_singleton.mp hv
    have ht : t ≠ 0 := by
      intro ht
      exact hv0 (by simp [ht])
    rw [hscale]
    exact mul_neg_of_pos_of_neg (sq_pos_of_ne_zero ht) hn
  have hpspan : ∀ v ∈ Submodule.span ℝ {p}, v ≠ 0 → 0 < hessian 2 g x v v := by
    intro v hv hv0
    obtain ⟨t,rfl⟩ := Submodule.mem_span_singleton.mp hv
    have ht : t ≠ 0 := by
      intro ht
      exact hv0 (by simp [ht])
    rw [hscale]
    exact mul_pos (sq_pos_of_ne_zero ht) hp
  have hndim : Module.finrank ℝ (Submodule.span ℝ {n}) = 1 :=
    finrank_span_singleton hn0
  have hpdim : Module.finrank ℝ (Submodule.span ℝ {p}) = 1 :=
    finrank_span_singleton hp0
  have hdisj : Disjoint (Submodule.span ℝ {n}) (Submodule.span ℝ {p}) := by
    rw [Submodule.disjoint_def]
    intro v hvn hvp
    by_contra hv0
    have hneg := hnspan v hvn hv0
    have hpos := hpspan v hvp hv0
    linarith
  have hcompl : IsCompl (Submodule.span ℝ {n}) (Submodule.span ℝ {p}) := by
    apply (Submodule.isCompl_iff_disjoint _ _ ?_).mpr hdisj
    simp [E,hndim,hpdim]
  refine ⟨Submodule.span ℝ {n},Submodule.span ℝ {p},hcompl,hndim,?_,hnspan,hpspan⟩
  simpa using hpdim

private theorem planar_inertia_two_iff
    (g : E 2 → ℝ) (x : E 2) (a b c : ℝ)
    (hQ : ∀ v : E 2, hessian 2 g x v v =
      a * (coordinates 2 v 0)^2 +
        2 * b * (coordinates 2 v 0) * (coordinates 2 v 1) +
        c * (coordinates 2 v 1)^2) :
    HessianHasInertia 2 g x 2 ↔ a < 0 ∧ 0 < a*c-b^2 := by
  constructor
  · rintro ⟨V,_W,_hcompl,hV,_hW,hneg,_hpos⟩
    have hVtop : V = ⊤ :=
      Submodule.eq_top_of_finrank_eq (by simpa [E] using hV)
    apply (planar_all_negative_iff g x a b c hQ).1
    intro v hv
    exact hneg v (by simp [hVtop]) hv
  · intro hs
    have hn := (planar_all_negative_iff g x a b c hQ).2 hs
    refine ⟨⊤,⊥,isCompl_top_bot,?_,?_,?_,?_⟩
    · simp [E]
    · simp
    · intro v _hv hv0
      exact hn v hv0
    · intro w hw hw0
      exact (hw0 ((Submodule.mem_bot ℝ).mp hw)).elim

private theorem planar_inertia_one_iff
    (g : E 2 → ℝ) (x : E 2) (a b c : ℝ)
    (hQ : ∀ v : E 2, hessian 2 g x v v =
      a * (coordinates 2 v 0)^2 +
        2 * b * (coordinates 2 v 0) * (coordinates 2 v 1) +
        c * (coordinates 2 v 1)^2) :
    HessianHasInertia 2 g x 1 ↔ a*c-b^2 < 0 := by
  constructor
  · rintro ⟨V,W,_hcompl,hV,hW,hneg,hpos⟩
    obtain ⟨n,hn0⟩ :=
      (Module.finrank_pos_iff_exists_ne_zero (R := ℝ) (M := V)).1
        (by rw [hV]; norm_num)
    obtain ⟨p,hp0⟩ :=
      (Module.finrank_pos_iff_exists_ne_zero (R := ℝ) (M := W)).1
        (by rw [hW]; norm_num)
    have hn0' : (n : E 2) ≠ 0 := by
      intro hz
      apply hn0
      exact Subtype.ext hz
    have hp0' : (p : E 2) ≠ 0 := by
      intro hz
      apply hp0
      exact Subtype.ext hz
    have hn := hneg (n : E 2) n.property hn0'
    have hp := hpos (p : E 2) p.property hp0'
    rw [hQ] at hn hp
    exact planar_det_neg_of_signs a b c
      (coordinates 2 (n : E 2) 0) (coordinates 2 (n : E 2) 1)
      (coordinates 2 (p : E 2) 0) (coordinates 2 (p : E 2) 1) hn hp
  · intro hd
    by_cases ha : a = 0
    · have hb : b ≠ 0 := by
        intro hb
        rw [ha,hb] at hd
        norm_num at hd
      let n : E 2 := planarInertiaVector ((-1-c)/(2*b)) 1
      let p : E 2 := planarInertiaVector ((1-c)/(2*b)) 1
      have hnQ : hessian 2 g x n n = -1 := by
        change hessian 2 g x
          (planarInertiaVector ((-1-c)/(2*b)) 1)
          (planarInertiaVector ((-1-c)/(2*b)) 1) = -1
        rw [planarInertiaVector_quadratic g x a b c hQ]
        rw [ha]
        field_simp [hb] <;> ring
      have hpQ : hessian 2 g x p p = 1 := by
        change hessian 2 g x
          (planarInertiaVector ((1-c)/(2*b)) 1)
          (planarInertiaVector ((1-c)/(2*b)) 1) = 1
        rw [planarInertiaVector_quadratic g x a b c hQ]
        rw [ha]
        field_simp [hb] <;> ring
      apply planar_inertia_one_of_sign_witnesses g x a b c hQ n p
      · rw [hnQ]; norm_num
      · rw [hpQ]; norm_num
    · have he : hessian 2 g x (planarInertiaVector 1 0) (planarInertiaVector 1 0) = a := by
        rw [planarInertiaVector_quadratic g x a b c hQ]
        ring
      have hw : hessian 2 g x
          (planarInertiaVector (-b) a) (planarInertiaVector (-b) a) =
            a*(a*c-b^2) := by
        rw [planarInertiaVector_quadratic g x a b c hQ]
        ring
      rcases lt_trichotomy a 0 with haneg | haeq | hapos
      · apply planar_inertia_one_of_sign_witnesses g x a b c hQ
          (planarInertiaVector 1 0) (planarInertiaVector (-b) a)
        · rw [he]
          exact haneg
        · rw [hw]
          exact mul_pos_of_neg_of_neg haneg hd
      · exact (ha haeq).elim
      · apply planar_inertia_one_of_sign_witnesses g x a b c hQ
          (planarInertiaVector (-b) a) (planarInertiaVector 1 0)
        · rw [hw]
          exact mul_neg_of_pos_of_neg hapos hd
        · rw [he]
          exact hapos

/- The three private finite controls instantiate the new genuine adapters.
   They assume exact quadratic identities and assert no source realization. -/
private theorem planar_negative_diagonal_control
    (g : E 2 → ℝ) (x : E 2)
    (hQ : ∀ v : E 2, hessian 2 g x v v =
      (-1 : ℝ) * (coordinates 2 v 0)^2 +
        2 * 0 * (coordinates 2 v 0) * (coordinates 2 v 1) +
        (-1 : ℝ) * (coordinates 2 v 1)^2) :
    HessianHasInertia 2 g x 2 :=
  (planar_inertia_two_iff g x (-1) 0 (-1) hQ).2 (by norm_num)

private theorem planar_saddle_diagonal_control
    (g : E 2 → ℝ) (x : E 2)
    (hQ : ∀ v : E 2, hessian 2 g x v v =
      (1 : ℝ) * (coordinates 2 v 0)^2 +
        2 * 0 * (coordinates 2 v 0) * (coordinates 2 v 1) +
        (-1 : ℝ) * (coordinates 2 v 1)^2) :
    HessianHasInertia 2 g x 1 :=
  (planar_inertia_one_iff g x 1 0 (-1) hQ).2 (by norm_num)

private theorem planar_zero_diagonal_saddle_control
    (g : E 2 → ℝ) (x : E 2)
    (hQ : ∀ v : E 2, hessian 2 g x v v =
      (0 : ℝ) * (coordinates 2 v 0)^2 +
        2 * 1 * (coordinates 2 v 0) * (coordinates 2 v 1) +
        (0 : ℝ) * (coordinates 2 v 1)^2) :
    HessianHasInertia 2 g x 1 :=
  (planar_inertia_one_iff g x 0 1 0 hQ).2 (by norm_num)

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

private theorem actualMaximum_measurable {L : ℝ} (hL : 0 < L) (x : E 2) :
    MeasurableSet {ω : SmoothSample 2 L | IsNondegMax 2 (actualField 2 L ω) x} := by
  have ha : Measurable (fun ω : SmoothSample 2 L => hA (actualField 2 L ω) x) :=
    actualHessian_measurable hL x basisX basisX
  have hb : Measurable (fun ω : SmoothSample 2 L => hB (actualField 2 L ω) x) :=
    actualHessian_measurable hL x basisX basisY
  have hc : Measurable (fun ω : SmoothSample 2 L => hC (actualField 2 L ω) x) :=
    actualHessian_measurable hL x basisY basisY
  have hd := (ha.mul hc).sub (hb.pow_const 2)
  have hm := (actualCritical_measurable hL x).inter
    ((measurableSet_lt ha measurable_const).inter (measurableSet_lt measurable_const hd))
  convert hm using 1
  ext ω
  change (IsCriticalPoint 2 (actualField 2 L ω) x ∧
      HessianHasInertia 2 (actualField 2 L ω) x 2) ↔ _
  exact and_congr_right (fun _ => planar_inertia_two_iff _ _ _ _ _
    (hessian_quadratic _ (actualField_smooth 2 hL ω 2) x))

private theorem actualSaddle_measurable {L : ℝ} (hL : 0 < L) (x : E 2) :
    MeasurableSet {ω : SmoothSample 2 L | IsIndexSaddle 2 (actualField 2 L ω) x} := by
  have ha : Measurable (fun ω : SmoothSample 2 L => hA (actualField 2 L ω) x) :=
    actualHessian_measurable hL x basisX basisX
  have hb : Measurable (fun ω : SmoothSample 2 L => hB (actualField 2 L ω) x) :=
    actualHessian_measurable hL x basisX basisY
  have hc : Measurable (fun ω : SmoothSample 2 L => hC (actualField 2 L ω) x) :=
    actualHessian_measurable hL x basisY basisY
  have hd := (ha.mul hc).sub (hb.pow_const 2)
  have hm := (actualCritical_measurable hL x).inter (measurableSet_lt hd measurable_const)
  convert hm using 1
  ext ω
  change (IsCriticalPoint 2 (actualField 2 L ω) x ∧
      HessianHasInertia 2 (actualField 2 L ω) x 1) ↔ _
  exact and_congr_right (fun _ => planar_inertia_one_iff _ _ _ _ _
    (hessian_quadratic _ (actualField_smooth 2 hL ω 2) x))

/-- The literal intrinsic finite-bar event is Borel on the full actual carrier,
for each fixed radius, including zero. No Good-event surrogate is used. -/
theorem sourceIntrinsicFiniteBarEvent_measurable {L : ℝ} (hL : 0 < L) (r : ℝ) :
    MeasurableSet (sourceIntrinsicFiniteBarEvent L r) := by
  have hdist : MeasurableSet {ω : SmoothSample 2 L |
      0 < torusDist 2 L (endpointLiftM r) (endpointLiftS r)} := by
    by_cases hd : 0 < torusDist 2 L (endpointLiftM r) (endpointLiftS r) <;> simp [hd]
  have hgap := measurableSet_lt measurable_const
    ((actualField_eval_measurable 2 L (endpointLiftM r)).sub
      (actualField_eval_measurable 2 L (endpointLiftS r)))
  have heq := measurableSet_eq_fun (actualDeath_measurable hL (endpointLiftM r))
    (actualField_eval_measurable 2 L (endpointLiftS r))
  have hm := (actualMaximum_measurable hL (endpointLiftM r)).inter
    ((actualSaddle_measurable hL (endpointLiftS r)).inter
      (hdist.inter (hgap.inter ((actualNonempty_measurable hL (endpointLiftM r)).inter heq))))
  convert hm using 1
  ext ω
  exact event_characterization hL r ω

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

/-- Actual normalized weighted mass and complement estimate, uniformly before
all compact marks and fixed-axis radii. The event and physical law are literal. -/
theorem sourceIntrinsicFiniteBarProbability_uniform {L : ℝ} (hL : 0 < L)
    (B k₀ k₁ : ℝ) (hB : 0 ≤ B) (hk₀ : 0 < k₀) (hk₀₁ : k₀ ≤ k₁) :
    ∃ C rStar : ℝ, 0 ≤ C ∧ 0 < rStar ∧ rStar ≤ 1 ∧ rStar ≤ L/2 ∧
      ∀ r : ℝ, 0 < r → r ≤ rStar → ∀ b k : ℝ, |b| ≤ B → k₀ ≤ k → k ≤ k₁ →
        let QW := sourceCompactFoldWeightedLaw hL.ne' r b k
        let E := sourceIntrinsicFiniteBarEvent L r
        let p := sourceIntrinsicFiniteBarProbability hL r b k
        IsProbabilityMeasure QW ∧ QW.real Eᶜ = 1-p ∧
          0 ≤ p ∧ p ≤ 1 ∧ 0 ≤ 1-p ∧ 1-p ≤ C*r^3 :=
  probability_uniform_given_measurable hL (sourceIntrinsicFiniteBarEvent_measurable hL)
    B k₀ k₁ hB hk₀ hk₀₁

end I4SourceIntrinsicH0WeightedProbability
