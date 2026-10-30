# C293: finite literal critical classes on the torus

For every natural dimension `d`, real `L > 0`, and literal smooth, `L`-periodic,
Morse-distinct `g : E d → ℝ`, the image of **all** literal critical points under
C263's actual lattice quotient projection is finite. The core theorem needs
only nondegeneracy at critical points, not the distinct-height conjunct.

The exact Lean theorem is
[`TorusMorseFinite.quotientCriticalSet_finite`](final-project/MorseFiniteCritical.lean).
Its conclusion is `(torus_proj d L hL '' {x | IsCriticalPoint d g x}).Finite`.
The implementation is 9,445 bytes, SHA-256
`95a660134eda49eecfe6181884bd23b4e4ca210e228d2463de29e5f821df047b`.
It keeps the literal `Lifetime` predicates and `TorusTopology` quotient. It
does not accept a finite critical list or invertibility certificate as an input.

Actual local verification completed on Lean 4.34.1 and pinned Mathlib
`d13f23b723b8a846827a245b89c10fc7d3f11612`: five isolated module builds,
warnings-as-errors for the three new modules, and three standard named-module
`leanchecker -v` replays passed. The complete module-origin transitive axiom
census covers 169 unique declarations (103/38/20/8) and contains only
`propext`, `Classical.choice`, and `Quot.sound`. This was standard kernel replay,
not `--fresh`, external verification, or a fresh proof check of every import.

The [nonauthor review](reviews/NONAUTHOR_REVIEW.md) gives
`ACCEPT_SCOPED_FORMAL`. [Compiled mathematical controls](final-project/MorseFiniteControls.lean)
show why symmetry and smoothness cannot simply be dropped. The separate
[missing-premise control](negative-project/WithoutMorse.lean) actually fails
with the expected absent `IsMorseDistinct` argument; this interface rejection
is not itself a counterexample theorem. Full execution receipts and output are
under `final-runs/` and `negative-final/`.

OpenAI Codex `/root/adapter_feasibility_c292` authored the proof, `/root` authored
controls and orchestrated execution/custody, `/root/current_pr_triage_c292`
assisted infrastructure/preflight, and `/root/c292_geometry_review` performed
the substantive nonauthor review, all delegated for Dylan Roy. The reviewer
was exposed to source/design and C292; organizational independence and human
review credit are zero. Dylan is not represented as personally reviewing it.

This closes one formal dependency of the frozen conventional C292 adapter
([PR 479](https://github.com/d6g8k5htny-coder/Math-/pull/479)). It does not prove
almost-sure Morse behavior, critical closed-superlevel local path connectivity,
critical-level path attainment, the full C292 Lean adapter, elder pairing,
exhaustive once-counted finite ordinary persistence bars, an all-small-bars
converse, or regional shrinking multiple-witness collision bounds. It gives
no uniform critical-count bound. Scientific acceptance remains unchanged.

Next useful task: freshly scope and claim the literal critical-level
closed-superlevel geometry/path-attainment dependency, preserving existing
companion, kernel and registration owners. The broader research and project
audit remain active.

See [author argument](AUTHOR_NOTES.md), [root check](evidence/ROOT_MATHEMATICAL_CHECK.md),
[scope](SCOPE.md), [source bindings](PUBLIC_SOURCE_BINDINGS.json),
[replay instructions](REPLAY.md), and [preserved execution history](evidence/EXECUTION_HISTORY.md).
`PUBLIC_PROJECTION.json` distinguishes exact native bytes from local-path-only
projections of receipts. Original hashes in projected records refer to native
bytes; the projection manifest separately hashes the published bytes. Private
Drive locators and local machine paths are withheld.

This new formal unit is **not registered in hosted formal CI**. Any hosted
checks on this draft PR cover the existing registered target set and repository
gates. Local C293 execution, hosted existing-target checks, byte custody and
scientific acceptance remain separate. Subsequent exact-head CI/custody/native
registration receipts belong to the PR's append-only terminal delivery comment.
