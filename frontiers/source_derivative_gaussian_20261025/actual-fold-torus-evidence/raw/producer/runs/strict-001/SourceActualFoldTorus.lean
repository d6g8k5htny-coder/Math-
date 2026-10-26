import SourceActualFoldDeath
import ReusedCompactFrontier

/-! Same-period actual torus trap, explicit strict clearance and its real sSup.
The compact-image frontier inclusion uses only continuity and openness.
The typed H0 ElderTrap conversion remains a separate downstream obligation. -/

/-! Same-period descent of the actual smooth source to the literal product AddCircle torus. -/
noncomputable section
open I4Torus I4SmoothCarrier I4LifetimeField
set_option autoImplicit false

namespace SourceActualFoldTorus

/-- The literal product quotient projection is continuous for every period. -/
theorem torusProjection2L_continuous (L : ℝ) :
    Continuous (I4Torus.torusProjection 2 L) := by
  exact Continuous.piMap (fun _ => continuous_quotient_mk')

/-- The literal product quotient projection is open for every period. -/
theorem torusProjection2L_open (L : ℝ) :
    IsOpenMap (I4Torus.torusProjection 2 L) := by
  exact IsOpenMap.piMap (fun _ => QuotientAddGroup.isOpenMap_coe)
    (Filter.Eventually.of_forall fun _ => QuotientAddGroup.mk_surjective)

/-- Every torus point has a real-cover lift, for either sign of the period. -/
theorem torusProjection2L_surjective (L : ℝ) :
    Function.Surjective (I4Torus.torusProjection 2 L) := by
  exact Function.Surjective.piMap (fun _ => QuotientAddGroup.mk_surjective)

/-- The literal torus carrier is Hausdorff for either sign of the period. -/
theorem sourceTorus2L_t2 (L : ℝ) : T2Space (I4Torus.SourceTorus 2 L) := inferInstance

/-- Descend the SAME real-cover sample field through the literal product quotient.
The chosen lift does not change the original period or sample law. -/
def actualTorusField {L : ℝ} (_hL : L ≠ 0) (sample : SmoothSample 2 L) :
    I4Torus.SourceTorus 2 L → ℝ := fun q =>
  smoothSourceField 2 L sample (Classical.choose ((torusProjection2L_surjective L) q))

/-- Exact pullback identifies the descended value with the original smooth field. -/
theorem actualTorusField_pullback {L : ℝ} (hL : L ≠ 0)
    (sample : SmoothSample 2 L) (x : Fin 2 → ℝ) :
    actualTorusField hL sample (I4Torus.torusProjection 2 L x) =
      smoothSourceField 2 L sample x := by
  unfold actualTorusField smoothSourceField
  exact I4Torus.sourceField_eq_of_torusProjection_eq 2 hL
    (sampleInclusion 2 L sample) _ x
    (Classical.choose_spec ((torusProjection2L_surjective L)
      (I4Torus.torusProjection 2 L x)))

/-- Continuous descent follows from the quotient projection and smooth real lift. -/
theorem actualTorusField_continuous {L : ℝ} (hL : L ≠ 0)
    (sample : SmoothSample 2 L) : Continuous (actualTorusField hL sample) := by
  have hquot : Topology.IsQuotientMap (I4Torus.torusProjection 2 L) :=
    (torusProjection2L_open L).isQuotientMap
      (torusProjection2L_continuous L) (torusProjection2L_surjective L)
  apply hquot.continuous_iff.mpr
  have heq : actualTorusField hL sample ∘ I4Torus.torusProjection 2 L =
      smoothSourceField 2 L sample := by
    funext x
    exact actualTorusField_pullback hL sample x
  rw [heq]
  exact (smoothSourceField_smooth 2 hL sample).continuous

/-- Physical normalized coordinates on the literal torus. -/
def torusPhysicalMap (L r : ℝ) (p : ℝ × ℝ) : I4Torus.SourceTorus 2 L :=
  I4Torus.torusProjection 2 L (r • ![p.1,p.2])

private theorem physicalPi_eq_chart (r : ℝ) (hr : r ≠ 0) (p : ℝ × ℝ) :
    r • ![p.1,p.2] = coordinates 2 (I4SourceActualFoldDeath.physicalChart r hr p) := by
  simp [I4SourceActualFoldDeath.physicalChart_apply]

/-- The physical map is continuous for every scale. -/
theorem torusPhysicalMap_continuous (L r : ℝ) : Continuous (torusPhysicalMap L r) := by
  unfold torusPhysicalMap
  apply (torusProjection2L_continuous L).comp
  exact (continuous_const (y := r)).smul (show Continuous (fun p : ℝ × ℝ =>
    (![p.1,p.2] : Fin 2 → ℝ)) from continuous_pi (by
      intro i
      fin_cases i
      · exact continuous_fst
      · exact continuous_snd))

/-- A nonzero physical scale makes the physical map open. -/
theorem torusPhysicalMap_open (L r : ℝ) (hr : 0 < r) :
    IsOpenMap (torusPhysicalMap L r) := by
  have hr0 : r ≠ 0 := ne_of_gt hr
  have hpi : IsOpenMap (fun p : ℝ × ℝ => (r • ![p.1,p.2] : Fin 2 → ℝ)) := by
    convert (coordinates 2).isOpenMap.comp
      (I4SourceActualFoldDeath.physicalChart r hr0).isOpenMap using 1
    funext p
    exact physicalPi_eq_chart r hr0 p
  exact (torusProjection2L_open L).comp hpi

/-- The descended field agrees with the same real-cover source at physical lifts. -/
theorem actualTorusField_physical_pullback {L : ℝ} (hL : L ≠ 0)
    (sample : SmoothSample 2 L) (r : ℝ) (p : ℝ × ℝ) :
    actualTorusField hL sample (torusPhysicalMap L r p) =
      smoothSourceField 2 L sample (r • ![p.1,p.2]) := by
  exact actualTorusField_pullback hL sample _

end SourceActualFoldTorus

noncomputable section
open Set MeasureTheory
set_option autoImplicit false
namespace SourceActualFoldTorus

/-- Strict clearance through an actual path to a strictly higher endpoint. -/
def strictClearanceSet {X : Type*} [TopologicalSpace X] (g : X → ℝ) (M : X) : Set ℝ :=
  {h | ∃ P, g M < g P ∧ ∃ γ : Path M P, ∀ t : unitInterval, h < g (γ t)}

/-- The real supremum of the explicit strict-clearance set. -/
def strictClearanceDeath {X : Type*} [TopologicalSpace X] (g : X → ℝ) (M : X) : ℝ :=
  sSup (strictClearanceSet g M)

/-- On the old Euclidean carrier the new predicate is literally C263. -/
theorem strictClearanceSet_eq_C263 {n : ℕ}
    (g : TorusFiltration.superlevelBar_E n → ℝ) (M : TorusFiltration.superlevelBar_E n) :
    strictClearanceSet g M = TorusFiltration.superlevelBar_clearanceSet g M := rfl

/-- Visible geometric trap data, with separation derived at the strict level.
No clearance equation, selected partner or homology conclusion is a field. -/
structure TorusTrapData {X : Type*} [TopologicalSpace X]
    (g : X → ℝ) (M P : X) (b d : ℝ) (D : Set X) : Prop where
  death_lt_birth : d < b
  maximum_height : g M = b
  older_height : b < g P
  domain_closed : IsClosed D
  maximum_inside : M ∈ D
  older_outside : P ∉ D
  height_ceiling : ∀ x ∈ D, g x ≤ b
  frontier_bound : ∀ x ∈ frontier D, g x ≤ d
  strict_trace : IsClopen (TorusFiltration.elderTrap_strictTrace g D d)
  closed_path : ∃ γ : Path M P, ∀ t : unitInterval, d ≤ g (γ t)

/-- The accepted arbitrary-space threshold theorem supplies the upper cut;
the retained closed-level path supplies every strictly lower level. -/
theorem TorusTrapData.strictClearanceSet_eq_Iio {X : Type*} [TopologicalSpace X]
    {g : X → ℝ} {M P : X} {b d : ℝ} {D : Set X}
    (T : TorusTrapData g M P b d D) : strictClearanceSet g M = Iio d := by
  ext h
  constructor
  · rintro ⟨y,hy,γ,hγ⟩
    obtain ⟨t,ht⟩ := TorusFiltration.elderTrap_higher_path_meets_threshold g D d
      T.strict_trace M T.maximum_inside
      (fun x hx => (T.height_ceiling x hx).trans_eq T.maximum_height.symm) hy γ
    exact (hγ t).trans_le ht
  · intro hh
    obtain ⟨γ,hγ⟩ := T.closed_path
    exact ⟨P, T.maximum_height.trans_lt T.older_height, γ,
      fun t => hh.trans_le (hγ t)⟩

/-- The explicit clearance interval has supremum exactly d. -/
theorem TorusTrapData.strictClearanceDeath_eq {X : Type*} [TopologicalSpace X]
    {g : X → ℝ} {M P : X} {b d : ℝ} {D : Set X}
    (T : TorusTrapData g M P b d D) : strictClearanceDeath g M = d := by
  rw [strictClearanceDeath, T.strictClearanceSet_eq_Iio, csSup_Iio]



open AdaptiveFoldBoundaryPath

/-- A continuous open physical map transports the compact box and its actual
path. Frontier inclusion is enough; no injectivity premise occurs. -/
theorem scaled_rectangle_trap {X : Type*} [TopologicalSpace X] [T2Space X]
    (e : ℝ × ℝ → X) (he : Continuous e) (heo : IsOpenMap e)
    (g : X → ℝ) (V : ℝ × ℝ → ℝ) (a b d R c : ℝ) (z : ℝ → ℝ)
    (ha : 0 < a) (hpull : ∀ p, g (e p) = a * V p)
    (hm : g (e M) = b) (hs : g (e S) = d)
    (h : RectangleBoundaryPathData V R c z) :
    TorusTrapData g (e M) (e (olderPoint z)) b d (e '' leftBox R) ∧
      b + a/4 ≤ g (e (olderPoint z)) ∧
      ∃ η : Path (e M) (e (olderPoint z)),
        (∀ t : unitInterval, d ≤ g (η t)) ∧ η pathMidpoint = e S := by
  let D := e '' leftBox R
  have hcompact : IsCompact D := (isCompact_Icc.prod isCompact_Icc).image he
  have hboundary : ∀ x ∈ frontier D, g x ≤ d := by
    intro x hx
    obtain ⟨p,hp,rfl⟩ := CapFirstExit.frontier_image_subset he heo
      (isCompact_Icc.prod isCompact_Icc) hx
    rw [hpull, ← hs, hpull]
    exact mul_le_mul_of_nonneg_left (h.frontier_bound p hp) ha.le
  have hheight : ∀ x ∈ D, g x ≤ b := by
    rintro x ⟨p,hp,rfl⟩
    rw [← hm, hpull, hpull]
    exact mul_le_mul_of_nonneg_left (h.ceiling p hp) ha.le
  have hgain : b + a/4 ≤ g (e (olderPoint z)) := by
    rw [← hm, hpull, hpull]
    have hh := mul_le_mul_of_nonneg_left h.older_gain ha.le
    nlinarith only [hh]
  have holder : b < g (e (olderPoint z)) := by linarith
  obtain ⟨γ,_hgraph,hfloor,hmid⟩ := h.path
  let η := γ.map he
  have hη : ∀ t : unitInterval, d ≤ g (η t) := by
    intro t
    change d ≤ g (e (γ t))
    rw [← hs, hpull, hpull]
    exact mul_le_mul_of_nonneg_left (hfloor t) ha.le
  have htrap : TorusTrapData g (e M) (e (olderPoint z)) b d D := {
    death_lt_birth := by
      rw [← hs, ← hm, hpull, hpull]
      exact mul_lt_mul_of_pos_left h.death_lt_maximum ha
    maximum_height := hm
    older_height := holder
    domain_closed := hcompact.isClosed
    maximum_inside := mem_image_of_mem e h.maximum_mem
    older_outside := fun hP => (not_lt_of_ge (hheight _ hP)) holder
    height_ceiling := hheight
    frontier_bound := hboundary
    strict_trace := TorusFiltration.elderTrap_strictTrace_isClopen g D d
      hcompact.isClosed hboundary
    closed_path := ⟨η,hη⟩ }
  exact ⟨htrap,hgain,η,hη,congrArg e hmid⟩


open I4SmoothCarrier I4SourceConfluentPins I4SourceRawPinConditioning
open I4SourceCompactTargetMoments I4SourceAdaptiveFoldChart
open I4SourceAdaptiveFoldEstimates I4Torus

/-- The literal physical map lands at the original raw maximum pin. -/
@[simp] theorem torusPhysicalMap_M (L r : ℝ) :
    torusPhysicalMap L r M = torusProjection 2 L (endpointM r) := by
  unfold torusPhysicalMap
  simp only [M]
  rw [show -(1/2 : ℝ) = -1/2 by ring, chart_endpointM]

/-- The literal physical map lands at the original raw saddle pin. -/
@[simp] theorem torusPhysicalMap_S (L r : ℝ) :
    torusPhysicalMap L r S = torusProjection 2 L (endpointS r) := by
  change torusProjection 2 L (r • ![1/2,0]) = _
  rw [chart_endpointS]

/-- The physical field has its positive amplitude and its absolute offset. -/
theorem torusPhysicalMap_field_eq {L r k : ℝ} (hL : L ≠ 0)
    (sample : SmoothSample 2 L) (hr : r ≠ 0) (hk : k ≠ 0) (p : ℝ × ℝ) :
    actualTorusField hL sample (torusPhysicalMap L r p) =
      (6*k*r^3) * actualFoldPotential r k sample p := by
  rw [torusPhysicalMap, actualTorusField_pullback]
  simp only [actualFoldPotential]
  field_simp

/-- Absolute raw pins and the same retained rectangle/path yield a torus trap,
physical older gain, saddle midpoint, explicit strict clearance and its sSup. -/
theorem actual_rectangle_torus {L r k b R c : ℝ} (hL : L ≠ 0)
    (sample : SmoothSample 2 L) (z : ℝ → ℝ) (hr : 0 < r) (hk : 0 < k)
    (hp : rawPins L r sample = ![b,b-k*r^3,0,0,0,0])
    (h : RectangleBoundaryPathData (actualFoldPotential r k sample) R c z) :
    TorusTrapData (actualTorusField hL sample)
        (torusProjection 2 L (endpointM r)) (torusPhysicalMap L r (olderPoint z))
        b (b-k*r^3) (torusPhysicalMap L r '' leftBox R) ∧
      b + (3/2)*k*r^3 ≤ actualTorusField hL sample (torusPhysicalMap L r (olderPoint z)) ∧
      (∃ η : Path (torusProjection 2 L (endpointM r)) (torusPhysicalMap L r (olderPoint z)),
        (∀ t : unitInterval, b-k*r^3 ≤ actualTorusField hL sample (η t)) ∧
          η pathMidpoint = torusProjection 2 L (endpointS r)) ∧
      strictClearanceSet (actualTorusField hL sample) (torusProjection 2 L (endpointM r))
        = Iio (b-k*r^3) ∧
      strictClearanceDeath (actualTorusField hL sample) (torusProjection 2 L (endpointM r))
        = b-k*r^3 := by
  have hm := congrFun hp (0 : Fin 6)
  have hs := congrFun hp (1 : Fin 6)
  simp only [rawPins, Matrix.cons_val_zero, Matrix.cons_val_one] at hm hs
  have hM : actualTorusField hL sample (torusPhysicalMap L r M) = b := by
    rw [torusPhysicalMap_M, actualTorusField_pullback]
    exact hm
  have hS : actualTorusField hL sample (torusPhysicalMap L r S) = b-k*r^3 := by
    rw [torusPhysicalMap_S, actualTorusField_pullback]
    exact hs
  obtain ⟨htrap,hgain,η,hfloor,hmid⟩ := scaled_rectangle_trap
    (torusPhysicalMap L r) (torusPhysicalMap_continuous L r) (torusPhysicalMap_open L r hr)
    (actualTorusField hL sample) (actualFoldPotential r k sample)
    (6*k*r^3) b (b-k*r^3) R c z (by positivity)
    (torusPhysicalMap_field_eq hL sample hr.ne' hk.ne') hM hS h
  have hgain' : b + (3/2)*k*r^3 ≤
      actualTorusField hL sample (torusPhysicalMap L r (olderPoint z)) := by
    convert hgain using 1 <;> ring
  have hresult := And.intro htrap (And.intro hgain'
    (And.intro (show ∃ η : Path (torusPhysicalMap L r M) (torusPhysicalMap L r (olderPoint z)),
      (∀ t : unitInterval, b-k*r^3 ≤ actualTorusField hL sample (η t)) ∧
        η pathMidpoint = torusPhysicalMap L r S from ⟨η,hfloor,hmid⟩)
      (And.intro htrap.strictClearanceSet_eq_Iio htrap.strictClearanceDeath_eq)))
  simpa only [torusPhysicalMap_M, torusPhysicalMap_S] using hresult

/-- One positive radius from the original nonzero period alone precedes all
scales and targets. The literal actual law derives pins and retained geometry
internally; its only sample hypotheses are the qualified numeric cutoffs. -/
theorem sourceGapLaw_actual_torus_trap_clearance {L : ℝ} (hL : L ≠ 0) :
    ∃ δ : ℝ, 0 < δ ∧ δ ≤ 1 ∧
      ∀ k₀ : ℝ, 0 < k₀ → ∀ r : ℝ, 0 < r → r < δ →
        ∀ b k : ℝ, k₀ ≤ k → ∀ᵐ sample ∂sourceGapLaw hL r b k,
          let T := sourceT k₀ sample
          let κ := sourceKappa r k sample
          let R := 4/Real.sqrt κ
          r*T^5 ≤ 1/100 → 1024*T^5 ≤ κ →
            ∃ (U : Set ℝ) (z : ℝ → ℝ),
              RidgeScalarData (actualFoldPotential r k sample)
                univ R (κ/2) T (3*T) T U z ∧
              TorusTrapData (actualTorusField hL sample)
                (torusProjection 2 L (endpointM r)) (torusPhysicalMap L r (olderPoint z))
                b (b-k*r^3) (torusPhysicalMap L r '' leftBox R) ∧
              b + (3/2)*k*r^3 ≤ actualTorusField hL sample (torusPhysicalMap L r (olderPoint z)) ∧
              (∃ η : Path (torusProjection 2 L (endpointM r))
                  (torusPhysicalMap L r (olderPoint z)),
                (∀ t : unitInterval, b-k*r^3 ≤ actualTorusField hL sample (η t)) ∧
                  η pathMidpoint = torusProjection 2 L (endpointS r)) ∧
              strictClearanceSet (actualTorusField hL sample) (torusProjection 2 L (endpointM r))
                = Iio (b-k*r^3) ∧
              strictClearanceDeath (actualTorusField hL sample) (torusProjection 2 L (endpointM r))
                = b-k*r^3 := by
  obtain ⟨δ₁,hδ₁,hδ₁1,hwide⟩ := sourceGapLaw_actual_rectangle_boundary_path hL
  obtain ⟨_K,δ₂,_hK,hδ₂,_hδ₂1,hbounds⟩ := sourceInverse_target_uniform_bounds hL
  refine ⟨min δ₁ δ₂, lt_min hδ₁ hδ₂, (min_le_left _ _).trans hδ₁1, ?_⟩
  intro k₀ hk₀ r hr hrδ b k hk
  have hr₁ : r < δ₁ := hrδ.trans_le (min_le_left _ _)
  have hr₂ : r < δ₂ := hrδ.trans_le (min_le_right _ _)
  have hG := (hbounds r hr hr₂).1
  have hpins : ∀ᵐ sample ∂sourceGapLaw hL r b k,
      rawPins L r sample = ![b,b-k*r^3,0,0,0,0] := by
    rw [sourceGapLaw_eq_rawPinKernel hL r b k hr.ne']
    have hm : MeasurableSet {sample : SmoothSample 2 L |
        rawPins L r sample = ![b,b-k*r^3,0,0,0,0]} :=
      measurableSet_eq_fun (rawPins_measurable hL r) measurable_const
    apply (ae_iff_measure_eq hm.nullMeasurableSet).mpr
    simpa using rawPinKernel_pin_fiber hL r hr.ne' hG ![b,b-k*r^3,0,0,0,0]
  filter_upwards [hwide k₀ hk₀ r hr hr₁ b k hk, hpins] with sample hw hp
  dsimp only at hw ⊢
  intro hrT hκ
  obtain ⟨U,z,hz,hbox⟩ := hw hrT hκ
  exact ⟨U,z,hz,actual_rectangle_torus hL sample z hr (hk₀.trans_le hk) hp hbox⟩

/-- The closed actual-law strict-clearance and death endpoint on the literal
original-period torus, without a desired geometric certificate premise. -/
theorem sourceGapLaw_actual_torus_clearance {L : ℝ} (hL : L ≠ 0) :
    ∃ δ : ℝ, 0 < δ ∧ δ ≤ 1 ∧
      ∀ k₀ : ℝ, 0 < k₀ → ∀ r : ℝ, 0 < r → r < δ →
        ∀ b k : ℝ, k₀ ≤ k → ∀ᵐ sample ∂sourceGapLaw hL r b k,
          let T := sourceT k₀ sample
          let κ := sourceKappa r k sample
          r*T^5 ≤ 1/100 → 1024*T^5 ≤ κ →
            strictClearanceSet (actualTorusField hL sample) (torusProjection 2 L (endpointM r))
              = Iio (b-k*r^3) ∧
            strictClearanceDeath (actualTorusField hL sample) (torusProjection 2 L (endpointM r))
              = b-k*r^3 := by
  obtain ⟨δ,hδ,hδ1,h⟩ := sourceGapLaw_actual_torus_trap_clearance hL
  refine ⟨δ,hδ,hδ1,?_⟩
  intro k₀ hk₀ r hr hrδ b k hk
  filter_upwards [h k₀ hk₀ r hr hrδ b k hk] with sample hs
  dsimp only at hs ⊢
  intro hrT hκ
  obtain ⟨U,z,_hz,_htrap,_hgain,_hpath,hclear,hdeath⟩ := hs hrT hκ
  exact ⟨hclear,hdeath⟩

end SourceActualFoldTorus
