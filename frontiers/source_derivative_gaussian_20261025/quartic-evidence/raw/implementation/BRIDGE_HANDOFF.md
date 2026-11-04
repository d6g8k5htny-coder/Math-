# Author-side Euclidean bridge handoff

Both scratch files are frozen and compiled cleanly with exit 0 and empty raw
output. `bridge_handoff.json` records exact source hashes and raw evidence paths.
No final evidence was produced by rerunning unchanged proofs.

Actual helper lineage: OpenAI/Codex
`/root/dm2_landed_composition/peano_strategy`, delegated by
`/root/dm2_landed_composition`. This is author-side support, not independent
scientific review.

## EuclideanBridge.lean

Namespace `I4SourcePinPreservingQuartic`:

- `pi_norm_le_euclidean_norm`: arbitrary finite Pi sup norm is at most the
  actual norm of `WithLp.toLp 2 v`.
- `euclidean_two_norm_sq`, `euclidean_two_norm_le_abs_sum`,
  `euclidean_two_norm_le_two_mul`.
- `matrixLinearEuclidean A := Matrix.toEuclideanCLM A` and its literal
  `ofLp`/`mulVec` application identity.
- `matrixLinearEuclidean_norm_le_of_sqsum` and
  `matrixLinearEuclidean_norm_le_two_mul` give induced Euclidean operator bounds.
- `matrixLinearEuclidean_offdiag_norm_le` and the symmetric three-coefficient
  correction bounds by `|a|+|b|+|c|` and `3*B`.

## GradientBridge.lean

The three-line `matrixLinearEuclidean` definition is duplicated only to keep
this new scratch independently compilable after the norm file was frozen.
Copy it only once when integrating into the single production module.

`coordinateDirection i` is `Pi.single i 1`; its zero and one values are proved
equal to the literal `[1,0]`, `[0,1]` coordinate directions.

`hessianMatrix f x i j` is the literal second multilinear derivative evaluated
on `[coordinateDirection j,coordinateDirection i]`: row is output, column is
domain input. `hessianMatrix_apply` proves its exact iterated-fderiv identity.

`hasFDerivAt_gradientEuclidean` derives the gradient derivative from C-infinity
and ordinary derivative chain rules, using the actual continuous linear
equivalences between Euclidean/Pi coordinates.

`hasFDerivAt_scaledGradientEuclidean f hf r hr z` gives the actual scaled
gradient derivative as `matrixLinearEuclidean (fun i j =>
hessianMatrix f (r • ofLp z) i j / r)` for arbitrary signed nonzero r.
`scaledGradientEuclidean_eq_components` identifies the function with the exact
two components `fderiv f (r • ofLp z) dx / r²`, `... dy / r²`.

No Taylor remainder, higher derivative permutation, or actual source conclusion
is asserted by these helpers. Parent owns those distinct integration steps.

Completed applicable evidence must be reused per `/workspace/AGENTS.md`.
