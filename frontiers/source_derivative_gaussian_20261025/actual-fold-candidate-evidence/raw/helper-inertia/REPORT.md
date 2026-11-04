# Actual candidate inertia helper: frozen scratch handoff

26 October 2026. OpenAI/Codex agent `/root/candidate_inertia`, delegated by `/root` to support producer `/root/actual_fold_candidate_construct`. Owned path only: `/workspace/scratch/actual-fold-candidate-inertia/`. Scientific effect **NONE**; separate research-target credit **0**; provider-distinct credit **0**.

## Frozen source and integration

- Source: `/workspace/scratch/actual-fold-candidate-inertia/Inertia.lean`.
- SHA256: `b234842b8d4c68991d1c4e0310f2a46a7512bd6f403d9acdae85338050783a9d`.
- Strict-success source snapshot: `logs/run-004/Inertia.lean`, identical bytes.
- Imports: existing `SourceActualFoldH0` and narrow `Mathlib.LinearAlgebra.FiniteDimensional.Lemmas` only.
- Namespace: `I4SourceActualFoldCandidate`.
- Needed declaration/proof section for one-time integration: **lines 11–128**, under the namespace opened at line 7 and `open UniversalLaw.Spec.Lifetime I4LifetimeField` at line 9. Producer can retain its own namespace/open envelope.
- Scratch source frozen after strict success ending **2026-10-26 10:36:23.950303 UTC**. No more source edits or checks planned. Root/producer owns integrated qualification.

Public APIs are exactly the agreed names/order:

```lean
planar_quadratic_complete_square (a b c u v : ℝ) (hc : c ≠ 0) :
  a*u^2 + 2*b*u*v + c*v^2 =
    (a-b^2/c)*u^2 + c*(v+b/c*u)^2

hessianHasInertia_two_of_diag
  (g : E 2 → ℝ) (x : E 2) (α s c : ℝ)
  (hα : 0 < α) (hs : s < 0) (hc : c < 0) (β : ℝ)
  (hQ : ∀ v : E 2, hessian 2 g x v v =
    α*(s*(coordinates 2 v 0)^2 +
       c*(coordinates 2 v 1 + β*coordinates 2 v 0)^2)) :
  HessianHasInertia 2 g x 2

hessianHasInertia_one_of_diag
  (g : E 2 → ℝ) (x : E 2) (α s c : ℝ)
  (hα : 0 < α) (hs : 0 < s) (hc : c < 0) (β : ℝ)
  (hQ : ∀ v : E 2, hessian 2 g x v v =
    α*(s*(coordinates 2 v 0)^2 +
       c*(coordinates 2 v 1 + β*coordinates 2 v 0)^2)) :
  HessianHasInertia 2 g x 1
```

These conclusions unfold the **old** `UniversalLaw.Spec.Lifetime.HessianHasInertia` definition. Maximum witnesses are `V=⊤`, `W=⊥`, with dimensions 2 and 0. Saddle witnesses are `V=span ℝ {(coordinates 2).symm ![0,1]}` and `W=span ℝ {(coordinates 2).symm ![1,-β]}`. Both generators are proved nonzero, each span has finrank 1, their intersection is zero by the zeroth coordinate, and the ambient dimension 2 supplies complementarity. Strict negative/positive quadratic signs are proved for all nonzero vectors on the specified lines by reducing to nonzero scalar multiples. No isometry claim about `coordinates` is used. The desired inertia is not a premise.

Producer uses `α=6*k*r`, `s=a-b²/c`, `β=b/c`, with `c<0` supplied by the actual ridge helper. The scalar identity was added at the ridge helper's request to save repeated algebra in producer integration.

## Bounded verification and preserved failures

Uncovered obligation warranting these runs: the two **new** genuine Lifetime inertia constructions and their scalar square-completion adapter had no existing Lean elaboration. Every rerun followed the specific new-source correction below. No old theorem, dependency, qualification or conventional proof was reverified.

The executed runner is `compile.py`, SHA256 `08068e142137a2db0225598bb30f03dc69ccd55a0e5534fd7491c15d05146fe2`. Every run preserves the exact source snapshot, runner bytes, complete stdout/stderr, argument array, working directory, source SHA256, UTC start/end, measured monotonic elapsed seconds, and exit in `logs/run-NNN/`. `EXECUTION_RECORD_INDEX.json` aggregates those receipts and diagnostic identities.

| Run | Exit | Seconds | Source SHA256 | Affected issue |
|---|---:|---:|---|---|
| 001 | 1 | 3.778373216 | `d61e13d8054cd33f90c165ce2a5260b76c70e141578dc1700957b34bd4f7fc55` | Exact Mathlib namespace arguments and coordinate simplification required explicit coordinate equalities. |
| 002 | 1 | 3.636282750 | `12a285458a12331580f4290f476bce2656246145109f1af0ba9f6449243d53e4` | Two `unnecessarySimpa` strict lints. |
| 003 | 1 | 3.837514034 | `7c7a610de4178f2480906570284ec7c841456aa8d38b9aff8b26107cb53be603` | Two `unnecessarySeqFocus` strict lints; replaced scalar final simplification explicitly. |
| 004 | 0 | 3.541879800 | `b234842b8d4c68991d1c4e0310f2a46a7512bd6f403d9acdae85338050783a9d` | Corrected lints and added new scalar square-completion theorem; empty diagnostics. |

All use `/home/agent/.elan/bin/lake env lean -DwarningAsError=true <snapshot>`, with cwd the source packet. No `-o` was passed; no helper object was placed in any production/cache location. No standalone kernel, axiom/inventory audit, controls, mutation campaign, old-proof review or qualification campaign was performed. The producer's one integrated-module qualification covers the integrated new material.

`environment.json` records the post-success read-only environment observation: packet `git rev-parse HEAD` is exact precode **`d7c3634a1ac7ea80da32863cb3348e856bd26a88`**; `lake env printenv LEAN_PATH` resolves existing packet and pinned Mathlib build roots and Lean `v4.34.1`. This is an environment observation, not an upstream source/artifact requalification. Existing Mathlib identity `d13f23b723b8a846827a245b89c10fc7d3f11612` is reused from precode/preflight authority.

Two pre-implementation discovery commands exited nonzero and did not change source: (1) a batched read tried absent `lakefile.lean` (actual configuration is `lakefile.toml`), exit 1, tool elapsed 0.000033645 seconds; (2) the next discovery batch tried the producer scratch directory before it existed, exit 2, tool elapsed 0.00004232 seconds. The tool transcript retains these exact commands and diagnostics; they are not Lean validation failures. Subsequent discovery used the actual `.toml` and no producer scratch write occurred.

## Authority and reuse carried forward

Read `/workspace/AGENTS.md`, repository `AGENTS.md` and `README.md`, local standing owner mandate/delegation/workflow, source packet `SOURCE_ACTUAL_FOLD_CANDIDATE.md` and its plan at precode `d7c3634`, and `/workspace/scratch/actual-canonical-partner-preflight/REPORT.md`. Direct producer API agreement was obtained before heavy proof; direct ridge-helper coordination confirmed coefficient meanings. No worker agent was dispatched.

Controlling owner clarification: completed applicable verification remains reusable; a new session, agent or handoff alone does not justify repeating checks. A new check needs a specific changed defect or uncovered obligation, limited to affected scope. Provider-distinct/process obligations remain separate from established mathematical verification. All qualified upstream actual geometry/H0/moments/numerator/normalizer evidence is reused without replay; this helper does not promote it.

Canonical standing links for future onboarding (carrying links does not establish recipient reading):

- https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OWNER_MANDATE_20261015.md
- https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OP-AUTONOMY-20260923-v2.1.md

The local candidate/death/H0 result is not canonical partner selection, conditional global Morse/distinctness or intrinsic finite-event elder semantics. No production/input/config/cache/manifest edit, commit, external post or scientific-status change occurred in this helper lane.
