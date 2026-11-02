# Frozen generic extended two-pin helper

Scope: requirement 2 only of SOURCE_ACTUAL_FOLD_ESTIMATES.md, published commit
48b2ffb8b3204108ad53f8f6ad4c7decd774196a. Binding source and authoritative
/workspace/scratch/actual-fold-estimates-preflight/REPORT.md read. No production,
shared, commits, posts, subagents, standalone kernels, audits, or controls.

Author/helper lineage: OpenAI Codex, generic helper fold_two_pin_bounds; same
provider lineage, **zero different-family credit**. Producer must integrate the
frozen section once into its new final source, retain this lineage, and cover
its declarations in the producer's final module verification.

Completed applicable 34-module/25-input, Mathlib, actual-source and conventional
mathematical evidence is REUSED. No old builds, hashes, axiom inventories,
controls, or theorem reproving were performed. This is new scratch elaboration,
not an independent new module qualification. Provider-distinct review is a
separate process obligation and does not invalidate mathematical evidence.

## Frozen files

TwoPin.lean is the full strict-elaboration input, with imports:

```
import AdaptiveFoldScalarBarrier
import Mathlib.Analysis.Calculus.LocalExtr.Rolle
import Mathlib.Analysis.Calculus.MeanValue
```

INTEGRATION_SECTION.lean.txt is the exact section from namespace
I4ActualFoldTwoPin through its end, including private convex_zero_pin_sign.
The producer needs `open Set` (or qualified equivalents), the available imports,
and can copy the section verbatim. Namespace and interfaces were agreed directly
with /root/actual_fold_estimates_construct.

Frozen SHA256 identities:
- `TwoPin.lean`: `d85a5ff3e6be506b1762dfe91a6f0a3efc44229311b4f448c0b90e84b0b31038`
- `INTEGRATION_SECTION.lean.txt`: `5cd3f6ef111a6045e4e3a8b52af6bec5c5f2616b77131c7e5452560c73a4f87c`

## Exact exported signatures

```lean
theorem I4ActualFoldTwoPin.two_pin_bounds_on_J
    (g g1 g2 : ℝ → ℝ) (T : ℝ) (hT : 0 ≤ T)
    (hg : ∀ x ∈ AdaptiveFoldScalar.J, HasDerivAt g (g1 x) x)
    (hg1 : ∀ x ∈ AdaptiveFoldScalar.J, HasDerivAt g1 (g2 x) x)
    (hg2 : ∀ x ∈ AdaptiveFoldScalar.J, |g2 x| ≤ T)
    (hm : g (-(1 / 2 : ℝ)) = 0) (hp : g (1 / 2 : ℝ) = 0) :
    ∀ x ∈ AdaptiveFoldScalar.J,
      |g x| ≤ (T / 2) * |x ^ 2 - 1 / 4| ∧ |g1 x| ≤ 2 * T

theorem I4ActualFoldTwoPin.two_pin_abs_le_on_J
    (g g1 g2 : ℝ → ℝ) (T : ℝ) (hT : 0 ≤ T)
    (hg : ∀ x ∈ AdaptiveFoldScalar.J, HasDerivAt g (g1 x) x)
    (hg1 : ∀ x ∈ AdaptiveFoldScalar.J, HasDerivAt g1 (g2 x) x)
    (hg2 : ∀ x ∈ AdaptiveFoldScalar.J, |g2 x| ≤ T)
    (hm : g (-(1 / 2 : ℝ)) = 0) (hp : g (1 / 2 : ℝ) = 0) :
    ∀ x ∈ AdaptiveFoldScalar.J, |g x| ≤ T ∧ |g1 x| ≤ 2 * T
```

No gap or potential assumption. The domain is the full closed interval J.
Convex T*q+g and T*q-g give the central and both outer-arm comparisons;
Rolle gives an interior zero of g1, then the mean-value estimate controls g1
by T times distance at most 2. The corollary uses |x²-1/4|≤2 on all of J.
The old scalarBarrier theorem was not invoked or reproved; its finite slope
comparison pattern was reused. No interpolation theorem restricted to the pins
was used. No source-law or probability assertion is made by this helper.

## New-only scratch elaboration history

Each runs/run-NN directory contains the exact immutable attempt snapshot,
output.log, and meta.json with exact command, cwd, exit, UTC completion time,
measured elapsed seconds, and source identity. run.py records every attempt.
The enclosing Python recorder exits 0 after saving results; meta.json records
the actual Lean exit, independently of the wrapper exit.

All commands had cwd:
/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025

- `run-01`: `lake env lean -DwarningAsError=true /workspace/scratch/fold-two-pin-bounds/runs/run-01/TwoPin.lean`; Lean exit 1; 6.298989404 seconds; SHA `3eef32ca94b490336c15997905fe1f44f36714a44618b44edfb28babafbe71b1`.
- `run-02`: `lake env lean -DwarningAsError=true /workspace/scratch/fold-two-pin-bounds/runs/run-02/TwoPin.lean`; Lean exit 1; 7.127315587 seconds; SHA `32c9f1c21f21074c2ed6c2fec4a021345916dc0d4beccff6bfb36f6eaaecaa6c`.
- `run-03`: `lake env lean -DwarningAsError=true /workspace/scratch/fold-two-pin-bounds/runs/run-03/TwoPin.lean`; Lean exit 0; 8.933060619 seconds; SHA `d85a5ff3e6be506b1762dfe91a6f0a3efc44229311b4f448c0b90e84b0b31038`.

run-01 failed only on endpoint simp normalization and two function-equality
closing goals. run-02 fixed those and failed because endpoint rewrites had
already closed goals before two extra `exact le_rfl` lines. run-03 removed those
redundant lines; exit 0, no output or warnings under -DwarningAsError=true.
No later source change occurred. Final integrated verification belongs to the
producer; do not rerun unchanged scratch checks due to handoff alone.

One exploratory source read (not verification) returned exit 2 because the
namespace AdaptiveFoldScalar lives in AdaptiveFoldScalarBarrier.lean and there
is no AdaptiveFoldScalar.lean. Exact command:

```
sed -n '1,190p' /workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025/AdaptiveFoldScalarBarrier.lean; sed -n '1,100p' /workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025/AdaptiveFoldScalar.lean
```

Tool wall time 0.000050422 seconds; output contained the successfully read
barrier body followed by:
`sed: can't read /workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025/AdaptiveFoldScalar.lean: No such file or directory`.
The actual namespace location was used thereafter. No Lean failure was hidden.
