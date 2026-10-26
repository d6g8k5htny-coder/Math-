# SourceConfluentPins author-side handoff

Source file:
`/workspace/Math-/frontiers/source_derivative_gaussian_20261025/SourceConfluentPins.lean`

Frozen source contract read in full from Math- commit `93c9a30`,
`frontiers/source_derivative_gaussian_20261025/SOURCE_CONFLUENT_PINS.md`.

Author: actual OpenAI/Codex agent `/root/dm2_landed_composition`, delegated by
`/root`. No helper agent was created. This is author-side proof work, not
independent scientific review or provider-distinct alignment evidence.

## New proved declarations

Namespace `I4SourceConfluentPins`:

- `rawTransform_confluentTransform`
- `confluentTransform_rawTransform`
- `confluentEquiv_apply`
- `confluentEquiv_symm_apply`
- `prescribed_target`
- `rawPins_hasGaussianLaw`
- `confluentPins_hasGaussianLaw`
- `rawPinsWithHessians_hasGaussianLaw`

The actual `confluentEquiv r hr` continuous linear equivalence contains proved
linearity, continuity and both inverse laws, using the literal stated formulas.
The prescribed target retains arbitrary real height `b` and nonzero radius.

`rawPins` are actual field values and fderiv observations at the two endpoints.
`rawPinsWithHessians` contains the raw six pins followed by actual iterated
second derivatives in order `(fxxM,fxyM,fyyM,fxxS,fxyS,fyyS)`. Their joint
Gaussianity follows from one 12-entry heterogeneous derivative theorem.

No covariance nondegeneracy, conditional field construction, regression block,
Palm event or scientific acceptance is inferred.

## Actual final scoped verification

The completed final command was:

```sh
lake env lean -o .lake/build/lib/lean/SourceConfluentPins.olean SourceConfluentPins.lean
```

Working directory:
`/workspace/Math-/frontiers/source_derivative_gaussian_20261025`

Exit code: 0. Raw merged stdout/stderr: empty.
The `.olean` was generated in the package's existing `.lake/build/lib/lean`.

Direct subprocess-captured evidence:

- `/workspace/scratch/dm2_landed_composition/source_confluent_final.log`
- `/workspace/scratch/dm2_landed_composition/source_confluent_final.meta`

Intermediate attempts are retained as `source_confluent_attempt1.log`,
`source_confluent_attempt2.{log,meta}`, `source_confluent_attempt3.{log,meta}`
and `source_confluent_attempt4.{log,meta}`. Attempt 3 completed the mandatory
scope. Attempt 4 added the optional joint derivative vector and exposed a
tactic sequencing issue in an attempted linter cleanup; the final version
uses `all_goals` and compiled cleanly.

Existing source inputs and `SourceDerivativeGaussian` verification were
reused, not rerun. Per `/workspace/AGENTS.md`, do not repeat completed applicable
checks merely because of a handoff. Root owns package integration, inventory,
final gate receipt and the separate scientific-review process.
