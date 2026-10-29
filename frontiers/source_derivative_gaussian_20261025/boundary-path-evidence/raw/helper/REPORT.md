# Scalar vertical quadratic loss — frozen helper

26 October 2026. Scratch-only author-side auxiliary for `/root/ridge_boundary_path_construct`. Owned output is confined to `/workspace/scratch/ridge-vertical-loss`; no production, shared setup, configuration, commit or post was changed. No subagent was used.

## Binding scope and inherited evidence

Read the binding `frontiers/source_derivative_gaussian_20261025/SOURCE_ADAPTIVE_FOLD_BOUNDARY_PATH.md`, supplied frozen published commit `e72bc0e221745c496b36c32d08147a4be6695a62`, and the optional `/workspace/scratch/ridge-barrier-join-preflight/REPORT.md`. The commit identity is transcribed from the dispatch, without a new old-source hash/qualification check. The helper supplies only the requested scalar loss and actual-partial slice wrapper. Its supplied `z` is an auxiliary root; the producer's final public theorem must construct its witness internally and retain one witness throughout.

Binding `/workspace/AGENTS.md` owner clarification of 25 October 2026: completed applicable verification is reusable; an agent/session/handoff does not justify rechecking unchanged material; any new verification must identify and target the changed or uncovered obligation; process review is tracked separately from established mathematics. The completed 32-module/25-input qualifications, old Cap/scalar/H0 material and their evidence are inherited unchanged. No old compile, kernel replay, audit, control or hash check was run. The new obligation here was exactly the two newly authored scalar-loss declarations; all Lean invocations below concern their scratch snapshots.

Canonical standing onboarding links carried forward (not claiming a new remote read):

- [15 October owner mandate](https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OWNER_MANDATE_20261015.md)
- [Standing delegation](https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OP-AUTONOMY-20260923-v2.1.md)

## Frozen source and integration receipt

Frozen source: `runs/run-006/VerticalLoss.lean`, whole-source SHA-256 `40a313e48d747774916a240740d136d47ed84c9494b6fd5a2ea68eeacf8042d2`. The top-level `VerticalLoss.lean` is the working alias of these exact final bytes. Integrate the two bodies once into namespace `AdaptiveFoldBoundaryPath`, with `open Set`, `open scoped ContDiff`, and `open AdaptiveFoldTransverseRidge` in scope.

Exact imports:

```lean
import AdaptiveFoldTransverseRidge
import Mathlib.Analysis.Convex.Deriv
import Mathlib.Analysis.Calculus.Deriv.Pow
```

No umbrella import, admission, custom axiom, `native_decide` or `implemented_by` was added. The helper does not use norm or mixed-partial symmetry assumptions. `hasDerivAt_slice` is reused from the qualified transverse module; that lemma supplies the actual full slice derivative and already passes the explicit scalar composition basepoint.

The declaration-section hashes below cover UTF-8 bytes starting at `theorem <name>` and ending immediately before the next documentation comment or final namespace `end`, respectively, including the intervening trailing newlines. Exact boundaries and byte counts are also recorded in `frozen-declarations.json`.

| Declaration | Frozen lines | Declaration-section SHA-256 |
|---|---|---|
| `quadratic_loss_of_second_derivative` | 15–68 | `8345c83c86a13943b092b622bbbd02634a604f0610388dab7c5f5a6acfad1d78` |
| `vertical_quadratic_loss` | 71–89 | `e6dce24c11a073a774426a9e192f2d21aeae7a8d87b270efcabbe372251e9f75` |

## Exact accepted signatures

```lean
theorem quadratic_loss_of_second_derivative
    {f f₁ f₂ : ℝ → ℝ} {a b c z y : ℝ}
    (hf : ∀ t ∈ Icc a b, HasDerivAt f (f₁ t) t)
    (hf₁ : ∀ t ∈ Icc a b, HasDerivAt f₁ (f₂ t) t)
    (hneg : ∀ t ∈ Icc a b, f₂ t ≤ -c)
    (hz : z ∈ Icc a b) (hroot : f₁ z = 0) (hy : y ∈ Icc a b) :
    f y ≤ f z - (c / 2) * (y - z) ^ 2
```

```lean
theorem vertical_quadratic_loss
    {V : ℝ × ℝ → ℝ} {O : Set (ℝ × ℝ)} {R c x z y : ℝ}
    (hO : IsOpen O) (hV : ContDiffOn ℝ 4 V O)
    (hstrip : ∀ t ∈ Icc (-R) R, (x, t) ∈ O)
    (hneg : ∀ t ∈ Icc (-R) R, partialY (Vy V) (x, t) ≤ -c)
    (hz : z ∈ Icc (-R) R) (hroot : Vy V (x, z) = 0)
    (hy : y ∈ Icc (-R) R) :
    V (x, y) ≤ V (x, z) - (c / 2) * (y - z) ^ 2
```

The generic scalar proof sets `g(t)=f(t)+(c/2)(t-z)^2`, with explicit jets `g₁(t)=f₁(t)+c(t-z)` and `g₂(t)=f₂(t)+c`. Mathlib's `concaveOn_of_hasDerivWithinAt2_nonpos` proves concavity on the closed interval. Both secant directions are bounded by the full derivative zero at `z`, proving `g(y)≤g(z)`, then the displayed loss. No positivity premise for `c` or `R` is needed by this auxiliary estimate; the public structural theorem still has its binding positive constants.

The actual-potential wrapper takes first jet `t ↦ Vy V (x,t)` and second jet `t ↦ partialY (Vy V) (x,t)`, both from the literal potential's actual Frechet-coordinate partials. C4 on open `O` supplies these full jets on every point of the closed slice, including its endpoints. The fixed root needs only `z∈[-R,R]` and `Vy V(x,z)=0`; it is not a chosen public ridge premise.

## New-only elaboration evidence

All commands use cwd `/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025` and the pinned executable `/home/agent/.elan/bin/lake`:

```text
/home/agent/.elan/bin/lake env lean -DwarningAsError=true /workspace/scratch/ridge-vertical-loss/runs/run-NNN/VerticalLoss.lean
```

Each run directory retains the exact source, output log and `metadata.json` with argv, cwd, source SHA-256, UTC start/end, exit code and monotonic elapsed wall time. Timings are local observed process elapsed wall time, not CPU time or independent proof-review duration. Successful `run-006` ran 05:15:07.121387–05:15:10.151946 UTC, exit 0, elapsed 3.030425715 seconds, with empty output log and warnings treated as errors.

| Run | Exit | Elapsed seconds | New source SHA-256 |
|---|---:|---:|---|
| run-001 | 1 | 3.849861363 | `8b640a78c0a9203f5b976eba7e39d9e3d3d83c1136029aa2e5df8074eff22281` |
| run-002 | 1 | 3.685196699 | `5b68004a367089dc5d5936d31c2343633ea6e82e8498ced7f9adc8579986f6d8` |
| run-003 | 1 | 3.393865783 | `b5f58c2e2d8748e25bd823cf2decd6f68a046d65175ad3cb5902fa8def7c44f4` |
| run-004 | 1 | 3.492307695 | `f5a5efd958cefa3d664acf49bc257c025c9578e462a10f5324a7b8b5d6d242a8` |
| run-005 | 1 | 2.928965140 | `54886910e711e7f02771cf126fcbbb3be81075537d2e2ed295e53a6c8a010d5e` |
| run-006 | 0 | 3.030425715 | `40a313e48d747774916a240740d136d47ed84c9494b6fd5a2ea68eeacf8042d2` |

Failure record:

- `run-001`: unsimplified function/id forms in the quadratic jet, function/instance presentation mismatch in the linear jet, and explicit zero multiplication needed in the two secant inequalities.
- `run-002`: only the linear-jet function/instance presentation mismatch remained.
- `run-003`: `dsimp` made no progress in an overly broad conversion tactic sequence.
- `run-004`: strict linter rejected an unnecessary `<;>` after `dsimp`.
- `run-005`: semicolon continuation attempted `ring` after `dsimp` had closed a function-equality branch.
- `run-006`: strict elaboration succeeded after splitting the quadratic-jet conversion into its exact function and scalar equality branches.

No standalone helper kernel replay, axiom inventory, audit or controls were run; the producer's final integrated own-module verification is responsible for those new declarations. This avoids duplicate verification of the same integrated proof. No old completed checks were repeated.

## Lineage and limits

Author-side OpenAI/Codex helper lineage only, coordinated directly with `/root/ridge_boundary_path_construct`. Same-provider auxiliary work is not provider-distinct review and earns zero scientific-family credit. Scientific effect: **NONE**. Provider-distinct scientific alignment review remains a separate pending process requirement and does not erase completed mathematical evidence. This receipt claims strict scratch elaboration of exactly these two new declarations, not completion of the producer's public constructed ridge/path theorem or acceptance of any parent scientific theorem.
