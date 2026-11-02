# Scratch derivative and quantitative helpers

26 October 2026. Owner: `/root/transverse_ridge_jets`. OpenAI author-side helper contribution only; **no independent-family review credit**. No production/shared source, lakefile, manifest, commit, publication, or other agent's scratch files were changed. All written artifacts are under this directory.

## Binding and reuse

Read the binding contract before other task work: `SOURCE_ADAPTIVE_FOLD_TRANSVERSE_RIDGE.md` under `frontiers/source_derivative_gaussian_20261025`. Requested frozen identity `66037c5c7083161f9a14fb4103227d15fc2cf6e6`; native activation `6408541927`. The contract bytes read have SHA256 `1cab24530a0759e3b91b1ac77eef29c822aaf0cbdf2adf74f8ef3b8fcf1cdd16`. Read the exact pinned API preflight at `/workspace/scratch/transverse-ridge-preflight/REPORT.md` and `/workspace/AGENTS.md`.

The completed applicable 31-module/25-input proofs and checks are reused. None were replayed. Helper elaboration covered only newly written source. The producer owns construction of ζ and the integrated new module's qualification, controls, named kernel replay, and axiom/inventory coverage. This helper assumes the previously constructed C² graph and its equation; it makes no existence, actual-elder, Parent A/B, or literal Gaussian-source claim. Pending source-review/provider process requirements remain distinct from established mathematical evidence.

## Delivered source and lineage

The producer explicitly reported integrating first the derivative segment from `runs/run-004/TransverseRidgeJets.lean`, then the quantitative-only segment from `runs/run-007/TransverseRidgeJets.lean`, each once with attribution comments. These frozen snapshots are the authoritative delivered sources; no additional copy is required.

- Run 004 new-only elaboration: exit 0 in 3.263885 seconds. Source SHA256 `7415419e565b7f8bfb443c26cc5b39057ade38ae1e6b9e5d18531ccd86a89cc1`. Output artifact SHA256 `b3839e589c74a1e9e6b389a3d3029a94a151be6686a31c82846109ae758e2ae2`.
- Run 007 new-only elaboration: exit 0 in 3.75347 seconds. Source SHA256 `5695d5815ca1bf5ba03c81643192326249902351a068a915f8df891bef841767`. Output artifact SHA256 `8ce4e1dfa2fadd2aaf358109a13e4a12d2041ac8bcb10da5b2ccecefd9f236a4`.
- `EXACT_SIGNATURES.lean.txt` gives all twelve exact delivered theorem signatures.
- `BINDINGS.json` inventories all commands, timestamps, exit codes, snapshots, hashes, theorem names, and output identities. Each `runs/run-NNN/record.json` and `stdout.log` preserve the complete run evidence, including failures.

Everything is in namespace `AdaptiveFoldTransverseRidge`, with literal `ex=(1,0)`, `ey=(0,1)`, `partialX G p=fderiv ℝ G p ex`, and `partialY G p=fderiv ℝ G p ey`. Those four temporary standalone definitions were intentionally duplicated only in scratch; production uses the producer's established identical definitions.

## Exact export roles

1. `clm_graph_vector`, `clm_vertical_vector`: literal coordinate expansions.
2. `c2_full_derivative_jets`: C² ζ on open U gives full `HasDerivAt ζ (deriv ζ x) x` and `HasDerivAt (deriv ζ) (deriv (deriv ζ) x) x`.
3. `zero_graph_first_chain`, `zero_graph_second_chain`: differentiate the zero equation twice using actual first/second Frechet derivatives. Both use eventual zero on open U, so original closed-interval endpoints have full derivatives.
4. `zero_graph_derivative_formulas`: nonzero actual partialY denominator gives the two requested quotient identities.
5. `bilinear_graph_vector`, `abs_bilinear_graph_vector_le`: expand all four coordinate terms and derive `|B(1,z)(1,z)| ≤ M*(1+|z|)^2`. No norm conversion or symmetry premise occurs.
6. `abs_neg_div_le_of_le_neg`, `zero_graph_derivative_bounds`: the explicit negative denominator bound and all four actual coordinate second derivative bounds give `|ζ'|≤M₁/c` and `|ζ''|≤(M₂/c)*(1+|ζ'|)^2`.
7. `root_abs_le_center_div`, `zero_graph_center_bound`: scalar real mean-value inequality, then actual-G/partialY adapter, giving `|z|≤M/c` from the center bound and a root in `[-R,R]`.

## Failures retained and API correction

Run 001 failed because an absolute scratch Lean input requires explicit `-R` package root. Run 002 exposed that pinned `HasFDerivAt.comp_hasDerivAt` requires the explicit scalar basepoint: `.comp_hasDerivAt x hp`; this corrects the preflight's incomplete argument observation. Run 003 required explicit `Filter.Eventually.mono` for open-neighborhood membership. Runs 005–006 were new quantitative elaboration failures (bilinear rewrite shape, current `abs_add_le` name, mean-value equation rewrite scope and explicit slice function); run 007 resolves them. Every failing snapshot/log remains intact.

Run 008 had already been launched when the producer reported its independent profile jets and asked for no extra work. It completed successfully and contains optional appended `graph_composite_derivative_jets` and `potential_graph_hasDerivAt`. These two exports are **not** part of the requested/integrated helper lineage and require no further use or checking. The authoritative twelve delivered exports remain run 007.

No custom axioms, admissions, `sorry`, `admit`, `native_decide`, or full Mathlib umbrella import were introduced. Helper-only axiom/kernel qualification was intentionally not duplicated because the producer will cover every integrated new declaration in the full new module's required qualification. There is no remaining requested mathematical helper gap.
