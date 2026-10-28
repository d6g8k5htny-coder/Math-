# Frozen V1 supplement C — actual Taylor neighborhood consumer

Agreed producer/fixture interface supplement before fixture use of these
additional interfaces. No existing signature or endpoint is changed.

Add the narrow import `Mathlib.Analysis.SpecialFunctions.Integrals.Basic`
for the explicit weight-integral calculation. Producer supplies:

```text
private theorem actual_taylorMatrix_contDiff {L : ℝ} (hL : 0 < L)
    (omega : SmoothSample 2 L) (X : E2) (P : Point2 ≃L[ℝ] E2) :
  ContDiff ℝ 1 (taylorMatrix (normalizedField (actualField 2 L omega) X P))

private theorem actual_taylorMatrix_symm {L : ℝ} (hL : 0 < L)
    (omega : SmoothSample 2 L) (X : E2) (P : Point2 ≃L[ℝ] E2) (y : Point2) :
  (taylorMatrix (normalizedField (actualField 2 L omega) X P) y).transpose =
    taylorMatrix (normalizedField (actualField 2 L omega) X P) y
```

Fixtures should combine the C¹/continuity, exact center and this actual
symmetry with jBranchDomain_isOpen/jMatrix_mem_jBranchDomain and
jBranch_congruence to specialize the branch on an actual open neighborhood
of0, not merely on an unrelated constant matrix. These producer functional
interfaces are required independently by the normalized constructor.
All remain private; ZERO helper execution/hash. Original section provenance
records this supplement before these new consumer obligations are written.
