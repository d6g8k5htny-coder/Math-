import SourceLifetimePairFiniteness

set_option autoImplicit false
noncomputable section
open MeasureTheory I4SmoothCarrier I4LifetimeField I4ActualSourceMorse
open UniversalLaw.Spec.Lifetime I4SourceLifetimePairFiniteness

namespace LifetimePairFinitenessControls

/-- Removing endpoint criticality permits infinitely many pairs even for the
unchanged actual source, irrespective of its sample values. -/
theorem fundDomain_infinite {L : ℝ} (hL : 0 < L) : (FundDomain 2 L).Infinite := by
  let c : ℝ → E 2 := fun t => (coordinates 2).symm (fun _ => t)
  have hi : Function.Injective c := by
    intro s t h
    exact congrFun (congrArg (coordinates 2) h) 0
  apply ((Set.Ico_infinite hL).image hi.injOn).mono
  rintro x ⟨t, ht, rfl⟩ i
  simpa only [c, ← coordinates_apply, ContinuousLinearEquiv.apply_symm_apply] using (show 0 ≤ t ∧ t < L from ht)

theorem arbitraryPair_pairSet_infinite {L : ℝ} (hL : 0 < L)
    (ω : SmoothSample 2 L) :
    (pairSet 2 L (fun _ _ _ => True) (actualField 2 L ω) Set.univ).Infinite := by
  have h0 : (0 : E 2) ∈ FundDomain 2 L := fun _ => ⟨le_rfl, hL⟩
  have hi : Function.Injective (fun x : E 2 => (x, (0 : E 2))) :=
    fun _ _ h => congrArg Prod.fst h
  apply ((fundDomain_infinite hL).image hi.injOn).mono
  rintro p ⟨x, hx, rfl⟩
  exact ⟨hx, h0, trivial, Set.mem_univ _⟩

/-- The actual carrier contains a zero sample. It is an exceptional realization,
so the almost-sure statement cannot be strengthened to every sample. -/
theorem zeroSample_field_eq_zero (L : ℝ) :
    actualField 2 L (I4SourceSmoothConditional.zeroSample 2 L) = fun _ => 0 := by
  funext x
  simp [actualField, smoothSourceField, sampleInclusion,
    I4SourceSmoothConditional.zeroSample, I4Source.sourceField, I4Foundation.scalarSeries]

theorem zeroSample_criticalFundDomain_infinite {L : ℝ} (hL : 0 < L) :
    {x | x ∈ FundDomain 2 L ∧ IsCriticalPoint 2
      (actualField 2 L (I4SourceSmoothConditional.zeroSample 2 L)) x}.Infinite := by
  simpa [zeroSample_field_eq_zero, IsCriticalPoint] using fundDomain_infinite hL

/-- Concrete positive specialization consumes the actual window theorem with
no Morse or finiteness input from the caller. -/
theorem positive_actual_candidate_window :
    ∀ᵐ ω ∂smoothLaw 2 1, ∀ A : Set ℝ,
      (pairSet 2 1 (IsWindowPair 2 1 1 (-1) 1 1 2)
        (actualField 2 1 ω) A).Finite := by
  filter_upwards [smoothLaw_ae_finite_windowPairSet (by norm_num : (0 : ℝ) < 1)] with ω hω
  exact hω 1 (-1) 1 1 2

end LifetimePairFinitenessControls
