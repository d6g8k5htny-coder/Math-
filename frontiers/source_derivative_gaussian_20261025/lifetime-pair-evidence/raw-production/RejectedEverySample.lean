import SourceLifetimePairFiniteness

open MeasureTheory I4SmoothCarrier I4LifetimeField UniversalLaw.Spec.Lifetime
open I4SourceLifetimePairFiniteness

-- Deliberate false mutation: replace almost surely by every actual sample.
-- Controls.zeroSample_criticalFundDomain_infinite supplies the counterexample.
example {L : ℝ} (hL : 0 < L) (ω : SmoothSample 2 L) :
    {x | x ∈ FundDomain 2 L ∧ IsCriticalPoint 2 (actualField 2 L ω) x}.Finite := by
  exact smoothLaw_ae_finite_criticalFundDomain hL
