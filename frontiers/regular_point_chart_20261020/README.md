# C296: regular scalar chart at a noncritical point

C296 instantiates Mathlib's finite-dimensional implicit-function chart for the
literal C294 project space `E d` and a smooth scalar function `g : E d → ℝ` at
a point `x` satisfying `¬ IsCriticalPoint d g x`.

The production module proves that the derivative has full scalar range, derives
the strict derivative from the project's `IsSmooth` predicate, and exposes an
`OpenPartialHomeomorph (E d) (ℝ × (fderiv ℝ g x).ker)`.  Its first coordinate is
exactly `g`; it sends `x` to `(g x, 0)`; and those points are members of the
chart's source and target.

This is a local regular-point tool only.  It does not construct a chart at a
critical point, prove a Morse normal form, transport local path connectivity
through a quotient or half-space, or remove C294's explicit
`LocallyPathConnectedSpace` premise.  Scientific effect is **NONE**.

## Reproduction

From this directory, with the pinned toolchain available:

```text
lake build RegularPointChart RegularPointChartInterface
lake env lean -E warning RegularPointChart.lean
lake env lean -E warning RegularPointChartInterface.lean
lake env leanchecker RegularPointChart
lake env leanchecker RegularPointChartInterface
lake env lean RegularPointChartAxiomAudit.lean
```

`WithoutNoncriticality.lean` is a negative fixture and must fail with a type
mismatch requiring `¬ IsCriticalPoint`.  See `RESULTS.md` for hosted identities
and `SCOPE.md` for the exact boundary.

[Owner mandate](https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OWNER_MANDATE_20261015.md) · [Standing delegation](https://github.com/d6g8k5htny-coder/main/blob/main/governance/OP-AUTONOMY-20260923-v2.1.md)
