import SourceActualFoldCandidate

noncomputable section
set_option autoImplicit false
open Set MeasureTheory UniversalLaw.Spec.Lifetime I4LifetimeField I4SmoothCarrier
open I4SourceConfluentPins I4SourceRawPinConditioning
open I4SourceCompactTargetMoments I4SourceAdaptiveFoldChart I4SourceAdaptiveFoldEstimates
open I4SourceActualFoldCandidate AdaptiveFoldTransverseRidge AdaptiveFoldBoundaryPath
open SourceActualFoldTorus I4Torus TorusFiltration CategoryTheory Limits

namespace ActualCandidateControls

/-- At L=1,r=1/4,b=3,k=1 the actual zero-gradient pins prove full criticality. -/
theorem actual_critical (sample : SmoothSample 2 1)
    (hp : rawPins 1 (1/4) sample = ![3,3-1*(1/4)^3,0,0,0,0]) :
    IsCriticalPoint 2 (actualField 2 1 sample) (endpointLiftM (1/4)) ∧
      IsCriticalPoint 2 (actualField 2 1 sample) (endpointLiftS (1/4)) :=
  actual_rawPins_critical (b := 3) (k := 1) (by norm_num) sample hp

/-- Exact physical Hessian amplitude is 3/2 at k=1,r=1/4. -/
theorem actual_physical_hessian (sample : SmoothSample 2 1) (p : ℝ × ℝ) (v w : E 2) :
    hessian 2 (actualField 2 1 sample)
      ((coordinates 2).symm ((1/4:ℝ) • ![p.1,p.2])) v w =
      (3/2) * iteratedFDeriv ℝ 2 (actualFoldPotential (1/4) 1 sample) p
        ![(coordinates 2 v 0,coordinates 2 v 1),(coordinates 2 w 0,coordinates 2 w 1)] := by
  convert actual_hessian_physical (by norm_num : (0:ℝ)<1) sample
    (by norm_num : (0:ℝ)<1/4) (by norm_num : (0:ℝ)<1) p v w using 1
  norm_num

/-- The actual retained ridge yields the literal complementary-subspace inertias. -/
theorem actual_inertias (sample : SmoothSample 2 1)
    (hp : rawPins 1 (1/4) sample = ![3,3-1*(1/4)^3,0,0,0,0])
    {R c M₀ M₁ M₂ A : ℝ} {U : Set ℝ} {z : ℝ → ℝ}
    (hs : StructuralRectangleData (actualFoldPotential (1/4) 1 sample) univ R c M₀ M₁ M₂ A)
    (hz : RidgeScalarData (actualFoldPotential (1/4) 1 sample) univ R c M₀ M₁ M₂ U z) :
    HessianHasInertia 2 (actualField 2 1 sample) (endpointLiftM (1/4)) 2 ∧
      HessianHasInertia 2 (actualField 2 1 sample) (endpointLiftS (1/4)) 1 := by
  have h := actual_rawPins_ridge_types (b := 3) (by norm_num : (0:ℝ)<1) sample
    (by norm_num : (0:ℝ)<1/4) (by norm_num : (0:ℝ)<1) hp hs hz
  exact ⟨h.1.2,h.2.2⟩

/-- The same literal candidate has exact positive gap1/64 and distance1/4. -/
theorem actual_candidate_gap (sample : SmoothSample 2 1)
    (hp : rawPins 1 (1/4) sample = ![3,3-1*(1/4)^3,0,0,0,0])
    {R c M₀ M₁ M₂ A : ℝ} {U : Set ℝ} {z : ℝ → ℝ}
    (hs : StructuralRectangleData (actualFoldPotential (1/4) 1 sample) univ R c M₀ M₁ M₂ A)
    (hz : RidgeScalarData (actualFoldPotential (1/4) 1 sample) univ R c M₀ M₁ M₂ U z) :
    IsCandidatePair 2 1 (actualField 2 1 sample) (endpointLiftM (1/4)) (endpointLiftS (1/4)) ∧
      torusDist 2 1 (endpointLiftM (1/4)) (endpointLiftS (1/4)) = 1/4 ∧
      heightGap 2 (actualField 2 1 sample) (endpointLiftM (1/4)) (endpointLiftS (1/4)) = 1/64 := by
  have h := actual_rawPins_ridge_candidate (b := 3) (by norm_num : (0:ℝ)<1) sample
    (by norm_num : (0:ℝ)<1/4) (by norm_num : (1/4:ℝ)<1/2) (by norm_num : (0:ℝ)<1) hp hs hz
  exact ⟨h.1,h.2.1,by simpa using h.2.2.1⟩

/-- This exact parent lattice distance has no sample or derivative premise. -/
theorem literal_distance :
    torusDist 2 1 (endpointLiftM (1/4)) (endpointLiftS (1/4)) = 1/4 :=
  endpoint_lifts_torusDist (by norm_num) (by norm_num) (by norm_num)

/-- The counterexample is a genuine full-period wrap of the literal lifts. -/
theorem full_period_wrap :
    torusDist 2 1 (endpointLiftM 1) (endpointLiftS 1) = 0 ∧
      torusDist 2 1 (endpointLiftM 1) (endpointLiftS 1) ≠ 1 :=
  ⟨endpoint_lifts_torusDist_unit_zero,endpoint_lifts_torusDist_unit_ne_radius⟩

/-- The actual product torus pulls back to exactly the same Lifetime source. -/
theorem pullback_same_sample (sample : SmoothSample 2 1) (x : E 2) :
    actualTorusField (by norm_num : (1:ℝ) ≠ 0) sample
      (torusProjection 2 1 (coordinates 2 x)) = actualField 2 1 sample x :=
  actual_torus_lifetime_pullback (by norm_num) sample x

/-- The closed actual-law endpoint specializes L=1,b=3,k0=k=1 without raw-pin,
ridge, candidate, Morse, death or H0 assumptions; K remains after the radius. -/
theorem actual_closed_candidate_death_h0 :
    ∃ δ : ℝ, 0 < δ ∧ δ ≤ 1 ∧ δ ≤ 1/2 ∧
      ∀ (K : Type) [Field K], ∀ r : ℝ, 0 < r → r < δ →
      ∀ᵐ sample ∂sourceGapLaw (by norm_num : (1:ℝ) ≠ 0) r 3 1,
        r*(sourceT 1 sample)^5 ≤ 1/100 →
        1024*(sourceT 1 sample)^5 ≤ sourceKappa r 1 sample →
        IsCandidatePair 2 1 (actualField 2 1 sample) (endpointLiftM r) (endpointLiftS r) ∧
        torusDist 2 1 (endpointLiftM r) (endpointLiftS r) = r ∧
        heightGap 2 (actualField 2 1 sample) (endpointLiftM r) (endpointLiftS r) = r^3 ∧
        ¬ superlevelBar_isEssential (actualField 2 1 sample) (endpointLiftM r) ∧
        superlevelBar_deathHeight (actualField 2 1 sample) (endpointLiftM r) = 3-r^3 ∧
        strictClearanceSet (actualTorusField (by norm_num : (1:ℝ) ≠ 0) sample)
          (torusProjection 2 1 (endpointM r)) = Iio (3-r^3) ∧
        strictClearanceDeath (actualTorusField (by norm_num : (1:ℝ) ≠ 0) sample)
          (torusProjection 2 1 (endpointM r)) = 3-r^3 ∧
        ∃ C : ℝ ⥤ ModuleCat K,
          Nonempty (superlevel_h0Filtration
            (actualTorusField (by norm_num : (1:ℝ) ≠ 0) sample) (ModuleCat.of K K) ≅
              elderInterval K 3 (3-r^3) ⊞ C) := by
  obtain ⟨δ,hδ,hδ1,hδL,h⟩ := sourceGapLaw_actual_candidate_death_h0 (by norm_num : (0:ℝ)<1)
  refine ⟨δ,hδ,hδ1,hδL,?_⟩
  intro K instK r hr hrδ
  filter_upwards [h K 1 (by norm_num) r hr hrδ 3 1 le_rfl] with sample hs
  dsimp only at hs
  intro hrT hκ
  obtain ⟨U,z,_hz,hcan,hd,_hM,hS,hgap,_hpos,hne,hdeath,_hrealc,
    ET,_hgain,_hpath,hclear,htdeath,hiso⟩ := hs hrT hκ
  refine ⟨hcan,hd,by simpa using hgap,hne,?_,?_,?_,kernel (elderRetraction (k := K) ET),?_⟩
  · simpa only [one_mul] using hdeath.trans hS
  · simpa only [one_mul] using hclear
  · simpa only [one_mul] using htdeath
  · simpa only [one_mul] using hiso

/-- At the same physical heights birth is included, death is excluded and the
ordinary interval has positive length r³. -/
theorem actual_interval_endpoints (r : ℝ) (hr : 0 < r) :
    elderActive 3 (3-r^3) (-3) ∧ ¬ elderActive 3 (3-r^3) (-(3-r^3)) ∧
      -(3-r^3)-(-3) = r^3 ∧ 0 < r^3 := by
  simpa only [one_mul] using SourceActualFoldH0.fold_interval_endpoints 3 1 r (by norm_num) hr

/-- The optional interface comparison uses no global Morse certificate. -/
theorem any_interface_value (sample : SmoothSample 2 1) (I : SuperlevelBarInterface 2 1)
    (hne : ¬ superlevelBar_isEssential (actualField 2 1 sample) (endpointLiftM (1/4))) :
    ¬ I.IsEssential (actualField 2 1 sample) (endpointLiftM (1/4)) ∧
      I.deathHeight (actualField 2 1 sample) (endpointLiftM (1/4)) =
        superlevelBar_deathHeight (actualField 2 1 sample) (endpointLiftM (1/4)) :=
  interface_values_eq_actual (by norm_num) sample I _ hne

end ActualCandidateControls
