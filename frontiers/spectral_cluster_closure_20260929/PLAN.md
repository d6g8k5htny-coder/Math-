# Spectral cluster closure implementation plan

Goal: publish an additive, test-backed conditional replacement for the failed
unbounded-shear domination, proving the fixed-d global count law without assuming
a global derivative-weighted estimate. Preserve all source proofs.

Architecture: PROOF.md contains vector exclusion, orthogonal spectral coordinates,
residual-target absorption and the nonempty-measure limit. check.py implements
finite exact identities only; test_check.py compares separate formulations.
verify.py and test_verify.py authenticate every declared source and inventory.
SOURCES.json binds consumed/credited sources; MANIFEST.json binds packet files.
The workflow checks the full source objects and leaves existing gates unchanged.

Tech stack: Python standard library, exact Fraction arithmetic, Git, Markdown.

Tasks:
1. Audit #159 at its exact head and give reproducible blockers; keep a repair log.
2. Write the full replacement proof and enumerate the remaining non-claims.
3. Write finite tests before implementation, observe intended RED, implement and
   replay normal/-O, and reject semantic mutations and unknown labels.
4. Test custody with real temporary Git repositories, including wrong hash,
   missing source, duplicate identity, unsafe path and symlink rejection.
5. Generate manifests and exact results. Authenticate remote tree blobs; publish
   a new branch/PR, never overwrite peer proof bodies.
6. Request distinct-provider analytic review of three scoped slices. Do not infer
   acceptance or a merge from passing tests. Check exact-current-head hosted gates.

Review focus: near-zero hard spectra; the exceptional absorption branch; rotation
versus isotropy; uncentered zero counts; compact-only cross-term rates; actual
versus limiting compound-Poisson parameters. Finite controls do not prove analysis.
