# SourceMorseIncidence registration package

This is metadata-only packaging for root's common frozen source cut
`1b1badc823725e6025823395463d4948c5cdf6d4`. The production source SHA256
`b93fe8f7856d4e632b3ff823788469720ae0814440bbec744fde099d4f29f127` is reused
from the completed source qualification; it was not recomputed for registration.
No production source, proof, lakefile, shared manifest or existing evidence was edited.
No Lean compile, axiom audit, kernel replay, control, baseline hash or baseline test was rerun.

## Exact registration counts

`append-names.txt` contains **99 explicit public theorem names**, one fully qualified
name per line in source order, with a final newline. Its metadata SHA256 is
`4ab40e48c4552104aca74d7c5e5cc27a141e750e4123c3b5027263292ef60c69`.
`append-names.json` contains the same ordered names as a JSON array.

There are 99 explicit public Prop theorems, zero lemmas, and zero named instances
(therefore no Prop/data instance ambiguity). The 40 public data/type definitions and
one type abbreviation are separate in `public-defs-abbrevs.txt`; they are not appended
to the public theorem/instance target registrations.

The existing exhaustive module audit covered **219 kernel declarations**, comprising
140 explicit public declarations (99 theorems + 40 defs + 1 abbrev), one explicit private
Prop theorem, and 78 generated declarations. The latter include auxiliary proofs,
equation/simp declarations, and an imported-unfolding equation generated during this
module's elaboration. These 79 private/generated entries are not public theorem
registrations. `AUDIT_MEMBERSHIP.json` reconciles every recorded audited kernel name
against the source-explicit public inventory; every explicit public name is covered.
This is a new metadata membership reconciliation, not repeated mathematical verification.

`PUBLIC_DECLARATIONS.json` gives each explicit declaration's kind, Prop/data classification,
source line, lineage, frozen source identity and source cut. `PUBLIC_DECLARATIONS.md`
is the human-readable list.

## Final actual-source exports

All names below are in namespace `I4ActualSourceMorse` in
`frontiers/source_derivative_gaussian_20261025/SourceMorseIncidence.lean` at the frozen cut.

| Fully qualified theorem | Line | Conclusion |
| --- | --- | --- |
| `I4ActualSourceMorse.smoothLaw_ae_sourceMorseCube` | 1561 | For `L ≠ 0`, actual `smoothLaw 2 L` almost surely has positive literal five-observation discriminant at every point of the actual fundamental cube. |
| `I4ActualSourceMorse.smoothLaw_ae_sourceMorseCompact` | 1575 | The same statement on any specified compact set of the real cover. |
| `I4ActualSourceMorse.smoothLaw_ae_sourceMorse` | 1587 | A single almost-sure event works at all real-cover points, by countable compact exhaustion. |
| `I4ActualSourceMorse.sourceMorse_regular` | 1636 | Positive actual discriminant at an actual critical point gives an injective derivative of the actual coordinate gradient. |
| `I4ActualSourceMorse.smoothLaw_ae_finite_sourceCriticalCube` | 1697 | The actual coordinate critical set in the fundamental cube is almost surely finite, by existing IFT and compact-discrete finiteness. |

The final source theorem's sole stochastic/source premise is `L ≠ 0`. Desired
parameter nullity, Gaussian density, a.s. Morse and source-law conclusions are derived,
not supplied as final hypotheses. Signed L and the original zero-mode convention are retained.

## Reused evidence and lineage

`raw-production/` preserves the completed author-side qualification and failed-history
files byte-for-byte: the final compile and named module build, exhaustive 219-declaration
axiom audit, named kernel replay, meaningful controls, their actual-exit JSON receipts,
raw logs, input/source snapshots, helper lineage and handoff. The existing final records
are `compact-07`, `module-08`, `axiom-09`, `kernel-10`, and `controls-13`, all actual exit 0.
The audit permits only `propext`, `Classical.choice` and `Quot.sound`.

Support history details remain honestly labeled in `raw-production/INCIDENT_NOTES.md`:
the first two failed Controls input files are explicitly reconstructed from recorded
edits rather than claimed as at-execution snapshots. Original error logs are retained.
The exploratory terminated `leanchecker --help` attempt is not successful verification.

The predecessor source bodies and evidence remain attributable to their original
author-side sessions. `raw-production/helper-lineage.json` retains the exact six
assembly-input source identities. Their compiled source work is reused, including:

- `TrigonometricMorseSard-04`: true equal-dimensional Sard nullity for any differentiable
  residual and nonzero actual amplitudes/frequency, with no desired-nullity premise.
- `FiniteMorseTransfer-02`: every-order carrier preservation, whole-erased-sample
  independence, reconstruction, measurable replacement and exact Fubini transfer.
- `GroupFourCoefficients-02`: the literal original grouped Gaussian coefficient law.
- `ActualMorseEvent-01`: measurable actual compact-cube positivity event.
- `CoordinateMorse-04`: literal Hessian determinant implies singular coordinate-gradient derivative.
- The compiled `FourModes-05` body plus unfinished `ActualFourModeShift-02` source lineage:
  the latter's distinct-frequency injectivity obligation is completed in the final source,
  without representing its failed helper command as a prior success.

The original scratch helper directories and their retained logs are referenced by
`HELPER_EVIDENCE_REFERENCES.json`. No predecessor check was rerun and no original helper
source/receipt was changed. The accepted conventional exact-law finite-L Morse/GAD and
C293 mathematical evidence is reused as established evidence, separately from this new
Lean actual-source adapter. Prior 24 qualified modules/23 inputs and completed Raw7,
Capture8 and Param source verification are reused by reference; no baseline file was
hashed, copied or tested by this metadata task.

## Remaining nonclaims and process work

The exact Lifetime Euclidean-coordinate transport, C263 period-lattice quotient descent,
and literal `HessianHasInertia` adapter are not exported. Actual source regularity and
fundamental-cube critical finiteness are already derived; quotient/inertia transport
is not silently assumed to obtain those results. No conditional Morse assertion at
every specified null pin, distinct critical heights, Palm/counting/elder closure, or
capture/dynamics closure is asserted.

Provider-distinct scientific alignment review is separate from the completed author-side
mathematical verification. Root owns source integration, shared registrations/lakefile,
commits and publication; this package adds no review acceptance or scientific-status claim.
The source cut above is root's supplied integration identity, not a claim of a new
post-integration proof run.

Standing reusable-verification instruction: completed applicable evidence remains reusable
across agents, sessions and handoffs. Changed evidence or a specific uncovered obligation
warrants only affected checks. Pending process review does not erase proved mathematics.
