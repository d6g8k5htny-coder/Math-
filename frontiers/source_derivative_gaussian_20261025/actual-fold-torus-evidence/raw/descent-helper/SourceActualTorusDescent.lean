import SourceActualFoldDeath

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
