# Exact confluent integral identities: author-side handoff

Sole new package source:
`frontiers/source_derivative_gaussian_20261025/ConfluentIntegralIdentities.lean`.

Source SHA256:
`0324d7556d485cd360a513587199354fa1f3863d15cf06b52c86e362de5e56b8`.

Read the entire frozen contract at Math- `d382da3`,
`SOURCE_CONFLUENT_INTEGRALS.md`. All seven literal formulas are proved in
namespace `I4ConfluentIntegralIdentities`:

- `pin3_integral`
- `pin4_integral`
- `pin5_integral`
- `adjusted_second_left`
- `adjusted_second_right`
- `adjusted_transverse_left`
- `adjusted_transverse_right`

Definitions `pin3`, `pin4`, `pin5` are the literal divided differences. The
public F theorems assume precisely `ContDiff ℝ 3 F`; H theorems assume precisely
`ContDiff ℝ 2 H`. Every theorem allows signed `r ≠ 0`. No integral identity,
Taylor remainder, convergence or Gaussianity premise is added.

Generic private derivative-chain helpers are instantiated from those stated
smoothness assumptions. The averages use FTOC, adjusted endpoint formulas use
affine-weight integration by parts, and the Peano identity differentiates the
explicit primitive `(1/4-u²)F''(ru)+(2/r)uF'(ru)-(2/r²)F(ru)` before FTOC.

Actual author lineage: OpenAI/Codex `/root/dm2_landed_composition` owns the
module. Actual OpenAI/Codex helper `/root/dm2_landed_composition/peano_strategy`
proved the generic Peano scratch lemma at `../PeanoHelper.lean`; that argument
was copied/adapted into the module. No helper import or new package dependency
was introduced. This is author-side proof work, not independent review.

## Completed new-scope verification

`qualification_receipt.json` binds exact commands, exits, raw logs and source
hashes. Original compilation was reused for later qualification.

- Final new-module compile: exit 0, `.olean` generated. Its raw output has one
  harmless `unnecessarySeqFocus` linter warning at line 71.
- Named `leanchecker ConfluentIntegralIdentities`: run once, exit 0, empty raw
  output.
- All seven public transitive axiom reports: only `propext`, `Classical.choice`,
  `Quot.sound`.
- Positive controls: exit 0. Cubic pin and quadratic average at radius minus
  two; literal H versus H' distinction; opposite adjusted endpoint signs; and
  normalized cubic kernel mass one obtained from the actual Peano theorem.
- False cubic normalization and false H'-based transverse value controls:
  each exit 1 at an unsolved `False` proof goal.

`positive-attempt1.{json,log}` records an initial control-only failure because
`norm_num` already factored the integral, making an extra rewrite obsolete.
Only that new control was corrected/rechecked. No theorem source was changed
after the completed final compile, and no kernel/axiom/old verification was
repeated.

Existing proof evidence is preserved. Actual differentiated-source-mode
instantiation, justified infinite-sum covariance limit, conditional regression
and Palm event joins remain open. Root alone integrates package targets,
inventory and final evidence. Scientific effect NONE.

Per `/workspace/AGENTS.md`, completed applicable verification is reusable; do
not repeat these checks merely because the work is handed off or a separate
process/review requirement remains pending.
