# Frozen before implementation: all-target curvature residual

Frozen 2026-10-26, author OpenAI/Codex /root/all_target_curvature_residual_construct.
Authority: published PRECODE 5141e92c22edc6a62d307e59f52dbfb2bdb1aba8,
SOURCE_ALL_TARGET_CURVATURE_RESIDUAL.md and PLAN; /workspace/AGENTS.md reuse.
Only new SourceAllTargetCurvatureResidual.lean and this scratch directory writable.
No workers, old-source/cache/config/manifest writes, commits or posts.

## Exact endpoint and dependency reuse

S(hL,r,p,rho) is literally sourceGammaRadius L (posteriorSample hL r p rho)
on SmoothSample 2 L, arbitrary six-vector p, original signed nonzero L.
Reuse existing direction envelope at b=0, generic posterior residual-shift identity,
original shift estimate, all-target posterior moments, positive Schur and local
parameter bounds. Do not reproduce all-target scalar/product laws or densities.
One hL-only delta is chosen before r,p,q,rho,n. A,H nonnegative and independent
of p; every n has a nonnegative Cn independent of r,p. The moment measure is
literally curvatureResidualLaw hL r and growth is Cn*(1+norm p)^n. Gap target
substitution uses sourceGapPins r b k, bounded abs k and original target norm bound.
Old default-radius specialization is definitional equality, with old exports intact.

## New-only qualification, bounded to uncovered obligations

1. Strict lean -DwarningAsError=true compile of only new source to scratch object.
2. Freeze source/object identities; notify root; exactly one named own-module
   leanchecker SourceAllTargetCurvatureResidual after source freeze.
3. Exhaustive actual-module-index constants inventory and collectAxioms audit,
   accepting only propext/Classical.choice/Quot.sound, with every constant classified.
4. Positive controls compile using the exact frozen scratch object:
   - original negative period L=-1 (not merely a sign-polymorphic binder);
   - arbitrary p on the same original carrier;
   - measurability, S>=1 and contactQ domination;
   - exact literal S and exact old default-radius specialization;
   - reconstruction and image bounds sharing delta,A,H before all targets;
   - moment quantifier order delta before n,r,p, target growth factor retained;
   - actual residual law and n=0 integrability/bound;
   - nondefault gap k=2,height b=3 and polynomial all-height specialization;
   - a norm-based arithmetic counterexample to erasing target growth.
5. One distinct intended-negative arithmetic mutation only: erase polynomial
   target growth by claiming (1+norm p)^n<=1, specialize p=(fun _=>3), n=1,
   normalize to exactly one unsolved False and no unrelated diagnostics.
   This witnesses failure of that arithmetic erasure step only; it is NOT a
   counterexample to every conceivable uniform residual moment estimate.

Retain every attempted command, exact source bytes, stdout/stderr, UTC start/end,
exit, source/object hashes, lineage, historical failures and controls. No sorry,
custom axiom, native_decide, implemented_by, Mathlib umbrella import. Never copy
helper/control objects to production cache. Root owns review, registration,
cache installation and publication. Existing 38 qualified modules / 989 targets /
32 inputs at retained published 19f7baf are reusable evidence, never replayed.
Provider-distinct process remains separate; OpenAI organizational credit 0;
scientific effect NONE. No weighted numerator/floor/probability or Parent claim.
