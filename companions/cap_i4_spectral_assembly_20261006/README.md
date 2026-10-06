# Cap I4: entry-to-positive-spectrum composition

Author: OpenAI / GPT-6 Astra Pro, `cap-i4-spectral-assembly-audit-20261006`, delegated by Dylan Roy. Pickup main#229/6008801391. Scientific effect NONE; author exposure, organizational-independence credit 0.

This is an additive child of entry-volume commit c0e73e383791dc90fd5d21016a23fc9544f0cf9b. It does not change the parent, linear, polar or angular branches, their reviews, production formal/ or any scientific register. Parent source identities are pinned in replay.py. The linear source is the scalar-repaired 3c571603f2aabae49144cdba4bc52cd94a6f4d82, not its earlier uncompilable source. The separate linear checker-budget repair is not silently imported or counted as a review here.

## Intended theorem and source limits

For the explicit source entry association e=(a,(b,d)), and measurable nonnegative extended-real G, the target is

    integral_entries 1{lambda_min(e)>0} G(eigenvalues(e))
      = pi * integral_{0<lambda<Lambda} (Lambda-lambda)G(lambda,Lambda).

Four theorem statements compose: restricted Tonelli on 0<rho<t; the complete three-entry factor2 and angular2pi integral; the existing weighted chamber factor1/4; and a pointwise anisotropic-density upper bound. Tests may be infinite. No inverse eigenvalue or positive hard-eigenvalue cutoff is introduced. Equality of repeated eigenvalues need not be assumed absent: the integrated polar identity handles its null contribution.

The result is not yet a theorem about an arbitrary supplied matrix-law measure: p is a nonnegative entry function with a pointwise spectral upper envelope. The actual Gaussian density, its relation to the measure, residual independence, uniform moments, typed determinant weight, elder event and full normalizer still need their concrete formal instantiations. Matrix-library positive-definiteness identification is a separate companion. Existing ordinary moment8/9 results are not imported as kernel facts.

P source: imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md, blob dfed3b8d318a3ab1950957f393307733a4bef3f2, sections3 and7; normalizer interpreted only with ERRATUM_CONGRUENCE.md blob213594d6ca6a86fb938110f4d166d9ce275a02d0. Public current mathlib documentation was consulted for discovery only. Imported code remains at mathlibd13f23b723b8a846827a245b89c10fc7d3f11612 and Lean4.34.1.

## Verification

Local six-method source/finite tests first gave three intended missing-implementation failures; the three pure algebra controls already passed. All six then passed normally/-O. This is source-contract testing, NOT Lean compilation. Contract.lean checks the exact final identity and density inequality. Hosted replay compiles all four exact parents plus this new module, checks both contracts, four axiom/type inventories, fresh leanchecker and two arithmetic sanity rejections. The rejection tests are not a continuum proof.

Replay uses the exact parent axiom/negative parsers rather than creating a new formal admission framework. Type text is an inventory check, not a general grammar; the critical types are compiled in Contract.lean. Exact source and dependency records are compared before/after. Timeout is failure, with partial output retained but no fabricated completed-process record. Read-only workflow and branch only; no PR or merge is requested. A separate scoped nonauthor alignment read is required before stronger claims.

Run from a complete repository with pinned dependencies installed:

    ROOT="$PWD"; (cd formal && lake env python3 -B -S "$ROOT/companions/cap_i4_spectral_assembly_20261006/replay.py")
