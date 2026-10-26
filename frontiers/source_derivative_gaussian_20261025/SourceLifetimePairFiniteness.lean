import SourceMorseIncidence
import SourceLifetimeGeometry
import Mathlib.Order.Interval.Set.Infinite

/-!
# Actual-source finiteness for the literal Lifetime pair sets

This application reuses the completed source critical-cube theorem. The carrier,
`smoothLaw`, and `actualField` are unchanged; the spatial transport is the existing
`I4LifetimeField.coordinates`. Only pair-set finiteness is proved. No count
integrability, density version, theta identity, elder-rule identification, or
parent lifetime asymptotic is asserted.
-/

set_option autoImplicit false

noncomputable section

open MeasureTheory I4SmoothCarrier I4LifetimeField I4ActualSourceMorse
open UniversalLaw.Spec.Lifetime

namespace I4SourceLifetimePairFiniteness

/-- Literal Lifetime criticality transports to the already used Pi-coordinate
criticality, by the derivative chain rule and the inverse coordinate map. -/
theorem actual_critical_coordinateGradient_zero {L : ℝ} (hL : 0 < L)
    (ω : SmoothSample 2 L) (x : E 2)
    (hx : IsCriticalPoint 2 (actualField 2 L ω) x) :
    coordinateGradient (smoothSourceField 2 L ω) (coordinates 2 x) = 0 := by
  have hdiff := ((smoothSourceField_contDiff 2 hL.ne' ω 1).differentiable
    (by simp) (coordinates 2 x)).hasFDerivAt
  have hcomp := hdiff.comp x (coordinates 2).hasFDerivAt
  change fderiv ℝ (actualField 2 L ω) x = 0 at hx
  have hz : (fderiv ℝ (smoothSourceField 2 L ω) (coordinates 2 x)).comp
      (coordinates 2).toContinuousLinearMap = 0 := hcomp.fderiv.symm.trans hx
  funext i
  have hzi := congrArg (fun D : E 2 →L[ℝ] ℝ =>
    D ((coordinates 2).symm (Pi.single i 1))) hz
  simpa only [ContinuousLinearMap.comp_apply, ContinuousLinearEquiv.coe_coe,
    ContinuousLinearEquiv.apply_symm_apply, zero_apply,
    Pi.zero_apply, coordinateGradient] using hzi

/-- The half-open Lifetime domain is contained in the completed closed source cube. -/
theorem coordinates_fundDomain_mem_sourceMorseCube {L : ℝ} (hL : 0 < L)
    {x : E 2} (hx : x ∈ FundDomain 2 L) :
    coordinates 2 x ∈ sourceMorseCube L := by
  constructor
  · intro i
    exact (hx i).1
  · intro i
    change x i ≤ |L|
    rw [abs_of_pos hL]
    exact (hx i).2.le

/-- Actual critical points in the literal Lifetime fundamental domain are almost
surely finite under the same actual smooth source law. -/
theorem smoothLaw_ae_finite_criticalFundDomain {L : ℝ} (hL : 0 < L) :
    ∀ᵐ ω ∂smoothLaw 2 L,
      {x | x ∈ FundDomain 2 L ∧ IsCriticalPoint 2 (actualField 2 L ω) x}.Finite := by
  filter_upwards [smoothLaw_ae_finite_sourceCriticalCube hL.ne'] with ω hω
  apply (hω.preimage (coordinates 2).injective.injOn).subset
  rintro x ⟨hx, hcrit⟩
  exact ⟨coordinates_fundDomain_mem_sourceMorseCube hL hx,
    actual_critical_coordinateGradient_zero hL ω x hcrit⟩

/-- On one common full-measure event, every height set and every population whose
members are actual critical pairs has a finite literal Lifetime pair set. The
criticality implication is not a finiteness premise. -/
theorem smoothLaw_ae_finite_pairSet_of_critical {L : ℝ} (hL : 0 < L) :
    ∀ᵐ ω ∂smoothLaw 2 L,
      ∀ (Pair : (E 2 → ℝ) → E 2 → E 2 → Prop),
        (∀ M S, Pair (actualField 2 L ω) M S →
          IsCriticalPoint 2 (actualField 2 L ω) M ∧
          IsCriticalPoint 2 (actualField 2 L ω) S) →
        ∀ A : Set ℝ, (pairSet 2 L Pair (actualField 2 L ω) A).Finite := by
  filter_upwards [smoothLaw_ae_finite_criticalFundDomain hL] with ω hω
  intro Pair hPair A
  apply (hω.prod hω).subset
  rintro ⟨M, S⟩ ⟨hM, hS, hpair, _⟩
  exact ⟨⟨hM, (hPair M S hpair).1⟩, ⟨hS, (hPair M S hpair).2⟩⟩

/-- Candidate finiteness uses the criticality clauses of the genuine predicate. -/
theorem smoothLaw_ae_finite_candidatePairSet {L : ℝ} (hL : 0 < L) :
    ∀ᵐ ω ∂smoothLaw 2 L, ∀ A : Set ℝ,
      (pairSet 2 L (IsCandidatePair 2 L) (actualField 2 L ω) A).Finite := by
  filter_upwards [smoothLaw_ae_finite_pairSet_of_critical hL] with ω hω
  exact hω _ (fun _ _ h => ⟨h.1.1, h.2.1.1⟩)

/-- All window parameters and height sets are covered on a common event. -/
theorem smoothLaw_ae_finite_windowPairSet {L : ℝ} (hL : 0 < L) :
    ∀ᵐ ω ∂smoothLaw 2 L, ∀ ρ bLo bHi kLo kHi : ℝ, ∀ A : Set ℝ,
      (pairSet 2 L (IsWindowPair 2 L ρ bLo bHi kLo kHi)
        (actualField 2 L ω) A).Finite := by
  filter_upwards [smoothLaw_ae_finite_pairSet_of_critical hL] with ω hω
  intro ρ bLo bHi kLo kHi
  exact hω _ (fun _ _ h => ⟨h.1.1.1, h.1.2.1.1⟩)

/-- The supplied elder interface only restricts the genuine window population;
no correctness property of that interface is needed for finiteness. -/
theorem smoothLaw_ae_finite_windowElderPairSet {L : ℝ} (hL : 0 < L) :
    ∀ᵐ ω ∂smoothLaw 2 L, ∀ ρ bLo bHi kLo kHi : ℝ,
      ∀ I : SuperlevelBarInterface 2 L, ∀ A : Set ℝ,
        (pairSet 2 L (IsWindowElderPair 2 L ρ bLo bHi kLo kHi I)
          (actualField 2 L ω) A).Finite := by
  filter_upwards [smoothLaw_ae_finite_pairSet_of_critical hL] with ω hω
  intro ρ bLo bHi kLo kHi I
  exact hω _ (fun _ _ h => ⟨h.1.1.1.1, h.1.1.2.1.1⟩)

/-- Unrestricted positive-gap candidate pairs are finite on the same law. -/
theorem smoothLaw_ae_finite_unrestrictedPairSet {L : ℝ} (hL : 0 < L) :
    ∀ᵐ ω ∂smoothLaw 2 L, ∀ A : Set ℝ,
      (pairSet 2 L (IsUnrestrictedPair 2 L) (actualField 2 L ω) A).Finite := by
  filter_upwards [smoothLaw_ae_finite_pairSet_of_critical hL] with ω hω
  exact hω _ (fun _ _ h => ⟨h.1.1.1, h.1.2.1.1⟩)

/-- The genuine finite-bar predicate also carries both criticality clauses. -/
theorem smoothLaw_ae_finite_finiteBarPairSet {L : ℝ} (hL : 0 < L) :
    ∀ᵐ ω ∂smoothLaw 2 L, ∀ I : SuperlevelBarInterface 2 L, ∀ A : Set ℝ,
      (pairSet 2 L (IsFiniteBar 2 L I) (actualField 2 L ω) A).Finite := by
  filter_upwards [smoothLaw_ae_finite_pairSet_of_critical hL] with ω hω
  intro I
  exact hω _ (fun _ _ h => ⟨h.1.1.1, h.1.2.1.1⟩)

end I4SourceLifetimePairFiniteness
