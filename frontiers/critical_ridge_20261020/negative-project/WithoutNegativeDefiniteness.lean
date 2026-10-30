import CriticalRidge

/-! Intentionally ill-typed C299 interface control. Draft, not executed.
The actual theorem is applied with one missing premise; only the intended
function-to-existential type mismatch qualifies. Syntax/import/resource failures
do not qualify. This is not a mathematical counterexample. -/

open Set Filter Topology
open UniversalLaw.Spec.Lifetime

example {d : ℕ} (f : E d → ℝ) (p : E d)
    (V : Submodule ℝ (E d)) (hsmooth : IsSmooth d f)
    (hcritical : IsCriticalPoint d f p) :
    ∃ r : E d → V,
      r 0 = 0 ∧
      ContDiffAt ℝ 2 r 0 ∧
      (∀ᶠ w in 𝓝 (0 : E d), ∀ z : V,
        fderiv ℝ f (p + w + (r w : E d)) z = 0) ∧
      (∀ (w : E d) (z : V),
        hessian d f p (w + (fderiv ℝ r 0 w : E d)) z = 0) := by
  exact TorusCriticalRidge.exists_negative_partial_gradient_ridge f p V hsmooth hcritical
