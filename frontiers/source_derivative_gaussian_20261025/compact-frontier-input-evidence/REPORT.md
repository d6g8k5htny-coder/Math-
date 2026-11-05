# Reused compact-image frontier support

Frozen on 26 October 2026. `ReusedCompactFrontier.lean` compiled successfully once with `-DwarningAsError=true` on Lean 4.34.1 / Mathlib `d13f23b723b8a846827a245b89c10fc7d3f11612`. Exit 0; empty stdout and stderr; measured 1.180510808 seconds, 06:35:15.040623–06:35:16.221105 UTC. There were no failed import/compile attempts and no plain-Lean fallback. This is one reused support root, zero new mathematical research targets, and scientific effect NONE.

## Binding and scope

Binding source: `frontiers/source_derivative_gaussian_20261025/SOURCE_ACTUAL_FOLD_TORUS.md` at published/precode commit `5f49444d13b9c322f5214e11bc3936b2271b615f`; preflight: `/workspace/scratch/actual-fold-torus-elder-preflight/REPORT.md` §3. Both were read first. Their exact observed hashes are in `BINDINGS.json`.

The only new uncovered obligation is composition of the accepted, unchanged theorem with a finite narrow import environment. The completed accepted Cap mathematics is reused pursuant to `/workspace/AGENTS.md`: completed applicable verification is reusable evidence; a new agent/session/handoff and pending provider-distinct process requirements do not invalidate it. No old Cap kernel, controls, axioms, mathematical proof review, torus/chart/probability campaigns, or historical tests were replayed. Provider-distinct review is separate; no such new review credit is claimed.

Standing owner links carried for handoff:

- https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OWNER_MANDATE_20261015.md
- https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OP-AUTONOMY-20260923-v2.1.md

Writes were limited to the new `inputs/elder/ReusedCompactFrontier.lean` and `/workspace/scratch/reused-compact-frontier`. No old source, packet configuration, manifest, producer, production cache, permission, or setting was edited. No commits, posts, or subagents were created. Root owns sole support-root registration and cache copying.

## Exact accepted origin and custody

Origin repository `/workspace/Math-curvature-20261026`, published commit `5f49444d13b9c322f5214e11bc3936b2271b615f`, path `frontiers/cap_first_exit_lean_20261002/CapFirstExit.lean`. Git blob SHA-1: `01744e2cf571049d7d1557b9ed54646881d341cf`. Origin file: 326607 bytes, SHA-256 `040aa91fcbdf25ccdaced1c828dd779318217a7c41ac928f87e8d17a8d3c3ef0`. Last-change commit: `c4eabc1a917ba2c1b96fe4af425cf2a484877c03`. The working source exactly equaled this pinned Git blob at extraction.

The sole extracted declaration is `CapFirstExit.frontier_image_subset`, source lines 359–369, including its immediately preceding documentation. The namespace preflight hint was correct. The accepted implicit context is `variable {X : Type*} [TopologicalSpace X]`; it is retained exactly. `open Set` is retained; unused `open unitInterval` is omitted. No other theorem, definition, torus fact, chart fact, probability lemma, or wrapper was copied or invented.

The producer `/root/actual_fold_torus_construct` directly confirmed it would import `ReusedCompactFrontier` and refer to the original `CapFirstExit.frontier_image_subset` namespace/signature. No new mathematical glue was necessary, so no new `SourceActualFoldTorus` declaration was introduced in this support module.

Exact accepted statement:

```lean
theorem frontier_image_subset {Y : Type*} [TopologicalSpace Y] [T2Space X] {e : Y → X}
    (hec : Continuous e) (heo : IsOpenMap e) {C : Set Y} (hC : IsCompact C) :
    frontier (e '' C) ⊆ e '' frontier C := by
```

The documentation/declaration/proof slice is saved as `accepted_theorem.lean.txt`; its 743 bytes equal the successor slice exactly. SHA-256 `f891109a501642f4c1f44e47c7601d58fbdefd5497408177691b5bceb8a93007`. Statement-and-proof SHA-256: `0a9af73f1cefe45a94ea1a99b18a2a336b150a5d6ca5f9dcca65f7996b03fdf0`. The proof-body bytes after `:= by\n` are saved as `accepted_proof_body.txt`; SHA-256 `ce1e3e8de7a4c2f2d7b80497f661cf183aa0ea361774e3cefd0a115155b31925`. `extract.py` performs the literal byte comparison and records the results in `BINDINGS.json`.

The 1360-byte successor source has SHA-256 `29d77453ef7c3cd216521a8ac84639aa30daf5a1d4061785a826b2c2d42d23db`.

## Narrow import delta and reused mathematical evidence

The old whole-file `import Mathlib` is replaced by the single finite import `Mathlib.Topology.Separation.Hausdorff`. The original statement and proof body are unchanged. This supplies compact-image closedness and the elementary topology used by the accepted proof. No tactic umbrella, `Mathlib` umbrella, or full Cap module is imported.

The binding explicitly accepts this Cap proof; preflight §3 identifies the same theorem and hypotheses. The existing Cap `ALIGNMENT.md` §2 records this exact frontier inclusion as interface I1 and states that injectivity is not required. The existing Cap `MANIFEST.json` has `CapFirstExit.frontier_image_subset` in its accepted axiom map, restricted to `Classical.choice`, `Quot.sound`, `propext`. These accepted mathematical/axiom facts are reused, not recomputed. Cap README's execution contract documents its historical strict build/kernel/axiom/control gate; this extraction does not manufacture a fresh execution receipt for that old campaign. No admissions, custom axioms, `native_decide`, `implemented_by`, disabled linters, or option suppression appear in the new code. The module defines only the retained old theorem.

## Exact new composition command and environment

`python3 /workspace/scratch/reused-compact-frontier/compile.py` exited 0. It invoked exactly:

```text
/home/agent/.elan/toolchains/leanprover--lean4---v4.34.1/bin/lean -DwarningAsError=true -o /workspace/scratch/reused-compact-frontier/build/ReusedCompactFrontier.olean -i /workspace/scratch/reused-compact-frontier/build/ReusedCompactFrontier.ilean /workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025/inputs/elder/ReusedCompactFrontier.lean
```

Working directory: `/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025`. Exact argument array, complete `LEAN_PATH`, source identity, measured monotonic elapsed time, UTC start/end, exit and diagnostic paths are retained in `strict-01.json`. The helper's own scratch build directory is prepended to the packet's `lake env printenv LEAN_PATH`; no production cache is changed.

`environment.json` records exact observation commands (`lake env printenv LEAN_PATH`, Lean `--version`, Mathlib `git rev-parse HEAD`), their outputs, exit codes, UTC timestamps, and elapsed times. The observed official Lean release is version 4.34.1, commit `5045d0056413266e57c625dcd7c365b10e377c52`, Release. Mathlib resolves to `/workspace/Math-/frontiers/determinant_moment_20261025/.lake/packages/mathlib`, HEAD `d13f23b723b8a846827a245b89c10fc7d3f11612`.

`python3 /workspace/scratch/reused-compact-frontier/extract.py` exited 0; its extraction identity observation was 06:34:53.892033 UTC. It read the origin with exact `git show 5f49444d13b9c322f5214e11bc3936b2271b615f:frontiers/cap_first_exit_lean_20261002/CapFirstExit.lean`, used `git rev-parse` for that same commit/path, and `git log -1 --format=%H 5f49444d13b9c322f5214e11bc3936b2271b615f -- frontiers/cap_first_exit_lean_20261002/CapFirstExit.lean` for last change. These are custody observations, not mathematical replay.

Exploratory discovery diagnostics were retained in this session's tool outputs: a broad read/search command exited 2 because nonexistent `LOCAL*` and `*REPORT*` globs were passed to `rg` in the Cap folder; a later topology search printed a nonexistent `Topology/Compactness/Basic.lean` path, while its compound shell command exited 0. Neither was a Lean/import attempt. No failed Lean/import command or discarded proof candidate exists. The sole artifact compile passed, and no subsequent Lean verification was run.

## Qualified named artifacts

Only these stable qualified artifacts may be copied by root:

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| `/workspace/scratch/reused-compact-frontier/build/ReusedCompactFrontier.olean` | 27896 | `e9e4a4051fbaae8f62b27dc5d83f343d58aa4d45b5e683c61bdbe899be2e666b` |
| `/workspace/scratch/reused-compact-frontier/build/ReusedCompactFrontier.ilean` | 3371 | `da1c18e2413cda4aefd042ba62e6402692d67f918bf7f2a4eab774c59d74bd81` |

`ARTIFACTS.json` retains these identities. Root was notified immediately after success. Source is frozen at the recorded identity; no unchanged verification is to be replayed. Any future check must identify an actual changed dependency, defect, or uncovered obligation first. This support root supplies no new torus theorem, actual-law endpoint, canonical pairing result, scientific status, or independent provider-review claim.
