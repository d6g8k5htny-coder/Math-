# DM2 execution delivery

Delegated AI implementation for Dylan Roy: OpenAI/Codex `/root`.
Scientific effect NONE. No parent acceptance or status change.

## Result

The exact P02-LM-002 pointwise inequality and its eighth-moment integration
corollary are supplied and locally kernel-checked, together with a stronger
untyped determinant inequality, the quadratic-form Sylvester criterion and
measurability of the literal typed weight. SOURCE_MAP.md and SCOPE.md bind the
mathematics. No conclusion or type assumption was inserted as a premise.

## Exact executed source

- Checked commit: dcfc89366f590342b4cd30b141a22c9ae2a562bb.
- Proof manifest SHA256: cb2b4870debf98cdf3663663797ccfc524e23d5f41f89e1c9ecdba5b6e680811.
- DM2 module SHA256: 661b73c3f21c6d2529f5e09ce426d89c01939ab27a5cc868db3802c7e66ea82d.
- Original receipt SHA256: 8fe7ab0f131a8a5c3e459d3bbbd10b4ab2b135438793851c11b25f7bb69f9eeb.
- Lean v4.34.1, release commit 5045d0056413266e57c625dcd7c365b10e377c52.
- Mathlib d13f23b723b8a846827a245b89c10fc7d3f11612; all nine locked dependency HEADs
  and clean worktrees observed before and after execution.

The exact local command was `PATH=/home/agent/.elan/bin:$PATH python -B -S
frontiers/determinant_moment_20261025/gate.py --execute` from the repository root.
The gate sets every child cwd to the packet root. Parent exit was 0. It removed
the package build directory and ran a fresh `lake build`, then
`lake env leanchecker ResearchFormalCoreR1`, the generated axiom/type queries,
five controls and final runtime/source/dependency observations. All succeeded
under their declared expected outcomes. leanchecker's successful stdout is empty;
its process exit 0 and sequence are recorded in gate-terminal.log.

All 18 declarations (13 retained scalar companions plus five new declarations)
have transitive axiom sets limited to propext, Classical.choice and Quot.sound.
The five retained controls rejected two false arithmetic proofs via Lean, and
sorry, imported-custom-axiom and native_decide proofs via their actual transitive
axiom reports. Their successful elaboration does not mean gate acceptance.

The unchanged gate's 78 tests passed in normal and optimized Python modes on the
frozen proof/control source. Test logs are included. The nonauthor independently
ran the same two 78-test modes and reported the results in its own review.

Two additional real Lean false-goal controls were run after the full gate:

- false_r6: r=1/128, q=-1, all other jets zero. Untyped squared product=2^-28,
  proposed r^6 bound=2^-30. Lean exit1, `unsolved goals`, goal False.
- false_omit_q: r=1/2, q=-100, all others zero. Squared product=6250000,
  bound omitting q from R=1. Lean exit1, `unsolved goals`, goal False.

Their fixtures are in controls/*.lean.txt. Replay by copying each fixture to
`.lake/formal-evidence/dm2_<label>.lean` and running `lake env lean` on that path
from the packet directory; each must exit1 on the false goal. Their commands,
exit codes, elapsed times, source/log hashes are in final/dm2_extra_controls.json.
Both witnesses also satisfy the actual type indicators, as the nonauthor checked.

## Evidence custody and limits

final/receipt.json is an exact copy of the original gate output, without any
metadata edited. Its 11 original log hashes were verified before copying, and
final/EXPORT_IDENTITIES.json gives every exported byte count/hash. Generated
Audit/Types/control Lean queries are preserved with `.lean.txt` suffixes to keep
output artifacts out of the package module census. No source content is changed
by that filename projection. Supplemental DM2 logs are outside the original
receipt's 11-log map and are bound by their own control record and export index.
Later delivery-only commits do not change or rebind the checked commit.

This was a direct local managed-cloud execution. repository/workflow/run fields
are honestly null; it is not a trusted hosted workflow receipt. Existing generic
repository CI runs the original core package, not this standalone packet. No new
workflow was introduced and no hosted target-package success is claimed.

The earlier umbrella-Mathlib build at deb28a751f620715ec65d3bd73690905e6fee94d
passed, but leanchecker was OOM-killed at a 16GiB limit. Its failure remains in
history/umbrella-mathlib-oom/. Only import headers changed in the successor;
every theorem, hypothesis, definition and proof body is unchanged. Gate, pins,
allowlist and five controls stayed identical. Preservation tests compare the
complete baseline bodies with originals and exact replacement imports. The RED
run used the precursor deprecated Data.Real headers; final canonical headers
were selected from the compiler's explicit replacement guidance. This is not
represented as a RED replay of the final literal header strings.

## Actual review and remaining boundary

DM2_NONAUTHOR_REVIEW.md covers deb28a; DM2_IMPORT_SUCCESSOR_REVIEW.md is the fresh
review of dcfc8936. Actual reviewer OpenAI/GPT-6-Codex family,
`/root/dm2_statement_review`, separate context, source exposed, no production
source authorship. Exact underlying model identifier unavailable to reviewer.
Organizational/blind/human independence 0. No historical primary Drive proof or
review was inspected or transferred. The source export's historical acceptance
labels are provenance only.

Same-provider technical statement review exists; a provider-distinct full-target
alignment record does not. The unchanged validator remains fail-closed and its
receipt remains PENDING_INDEPENDENT_REVIEW. Public request is on draft Math-#511
and main#539/6402508582; no eligible provider-distinct pickup is presumed.
No fake reviewer JSON is supplied. No merge, Ready transition or scientific
promotion is attempted.

This supplies the exact normalized-jet second-moment interface cW=16*M8. Still
unproved here: concrete field/jet identification, uniform Gaussian eighth
moments, normalizer lower bound, actual same-law Palm identification, event-tail
and good-event coverage, GT5, P0.2, and parent lifetime/persistence conclusions.
