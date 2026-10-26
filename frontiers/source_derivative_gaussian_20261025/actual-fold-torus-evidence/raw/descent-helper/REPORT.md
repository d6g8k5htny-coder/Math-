# Same-period actual source torus descent helper

26 October 2026, 06:38 UTC. Scratch-only helper for the single production `SourceActualFoldTorus.lean` integration. Scientific credit: zero. Provider-distinct review is a separate process requirement. Completed 36-module/27-input source qualification and old periodicity proofs are reused without re-running old checks under `/workspace/AGENTS.md`. No production/shared/input/config/cache files were edited here; no kernel/audit/control duplicate was run.

Frozen source: `SourceActualTorusDescent.lean`, SHA-256 `924a21801e7fcd9da5b09a15532ecd1ef130d3185fa2821f5fe4a3d5def8d0ef`, 97 lines. Its only import is `SourceActualFoldDeath`; the integrable section is lines 3–97. All declarations are in namespace `SourceActualFoldTorus` and use the unchanged `SmoothSample 2 L`, `sampleInclusion 2 L`, `smoothSourceField 2 L`, and literal `I4Torus.SourceTorus 2 L` for every `hL : L ≠ 0`. There is no `Fact (0 < L)` premise. The T2 theorem is inferred from the pinned Mathlib instance and accepts negative periods.

Exports: `torusProjection2L_continuous L`, `torusProjection2L_open L`, `torusProjection2L_surjective L`, `sourceTorus2L_t2 L`, `actualTorusField hL sample`, `actualTorusField_pullback hL sample x`, `actualTorusField_continuous hL sample`, `torusPhysicalMap L r p`, `torusPhysicalMap_continuous L r`, `torusPhysicalMap_open L r hr` for `hr : 0 < r`, and `actualTorusField_physical_pullback hL sample r p`. The producer owns the normalized potential amplitude identity and geometry joins.

Final strict source-only elaboration: `/workspace/scratch/actual-torus-descent/runs/strict-004/SourceActualTorusDescent.lean` is an exact copy of the frozen source; command (from `/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025`):

```sh
LEAN_PATH=/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025/.lake/build/lib/lean /home/agent/.elan/bin/lake env lean /workspace/scratch/actual-torus-descent/runs/strict-004/SourceActualTorusDescent.lean
```

Exit 0, empty diagnostics, start UTC epoch 1792996676, end 1792996679, wall clock 3 seconds. Exact snapshot, stdout/stderr, exit, timing are retained in `runs/strict-004/`.

Earlier source and failure evidence is retained: `runs/strict-001/` contains API probes (unknown guessed identifiers), `runs/strict-002/` records the first source attempt's failed `/usr/bin/time` launcher (exit 127) and then its real Lean failure at lines 74/76 (exit 1, missing `Fintype` due ambiguous `continuous_pi` elaboration), and `runs/strict-003/` records the corrected Lean success with an unused-binder warning (exit 0). The final source names the deliberately unused definition binder `_hL`; no proof terms or mathematical statement changed. The producer should integrate only the frozen source section; integrated new-module verification covers the new declarations.
