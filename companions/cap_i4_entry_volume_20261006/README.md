# Cap I4: the three-entry Lebesgue lift

Dylan Roy — delegated AI work. Author: OpenAI / GPT-6 Astra Pro,
`cap-i4-entry-volume-20261006`, pickup main#229/6008449524.
Scientific effect NONE; author-exposed, organizational-independence credit 0.

## Intended exact contract

For measurable nonnegative extended-real F on the ACTUAL entry association
`(a,(b,d))`, prove

    integral F(traceCoordinates e) d e = 2 * integral F(u) d u,
    traceCoordinates(a,(b,d))=((a+d)/2,((a-d)/2,b)).

The factor is the entry-Lebesgue volume factor, not a Frobenius-orthonormal
volume convention. Reorder the inner b,d integrals using Tonelli, apply the
already explicit pair map to (a,d), and regroup the x,b plane. Measurability
is retained throughout. Infinite integrals are allowed; no Bochner integral
is used and no integrability premise is silently dropped.

The exact-type Contract is published before the implementation. The first
run37407234767 stopped in the parent linear module, not the absent child;
this is not the intended missing-module RED. The parent's explicit one_div
repair at9ab41dc815f94aff9cdfeeb535938bad2fbc02c8 is adopted unchanged here.
The exact missing-module contract is rerun before adding the implementation.
No successful Lean statement is claimed until the actual complete successor
runs. Later source-alignment dispositions belong in main#229 and do not
retroactively change a failed attempt into successful execution.

## Source and scope

Initially based on linear29fa17b54559a30a389fb6cae899baf2dae71fdb;
source-preserving adoption now includes linear9ab41dc815f94aff9cdfeeb535938bad2fbc02c8.
The compiled parents are pinned as source files: CapI4Polar blob
9d0bdbfb5ad77c159fe623cf2dcad31cc9402ba4 and CapI4Linear blob
3c571603f2aabae49144cdba4bc52cd94a6f4d82. The reused evidence parser is also
pinned, at blob01ccc2ef0c0af691a89d5836346a8d87535e4b2d. Parent reviews are not
extended to this new composition. No parent branch or production formal/
source/manifest/receipt is changed. No primary-package theorem-count change.

The imported product integration rules are in mathlib
Mathlib/MeasureTheory/Measure/Prod.lean, blob
dcda187671ab2b4ded4e301fb30ca0391eb41c3b at
d13f23b723b8a846827a245b89c10fc7d3f11612, Lean4.34.1.
P's entry-density interface and spectral integration are in
imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md,
blobdfed3b8d318a3ab1950957f393307733a4bef3f2; its existing congruence erratum
213594d6ca6a86fb938110f4d166d9ce275a02d0 remains bound to the normalizer.

This module does NOT yet compose the angular/radial positive-chamber integral
into a final eigenvalue pushforward, instantiate a Gaussian density, identify
a matrix-library eigensystem, or prove residual independence, weighted
moments, cap geometry or the full-normalizer floor. It proves a missing
coordinate-volume interface, not the Cap selection theorem.

## Replay

Run `bash companions/cap_i4_entry_volume_20261006/replay.sh` from a complete
checkout with the pinned toolchain/dependencies installed. The read-only
workflow sets these up. Only the two imported modules and the new module are
compiled, followed by all exact contract applications, three axiom/type
reports, fresh leanchecker and a concrete false-coordinate rejection. The
latter is a sanity check, not a continuum falsification. Each process has an
explicit status file. Every consumed versioned source and all dependency
heads are checked before and after; existing output is rejected. A timeout
or any failed stage remains failure. The larger fresh-checker budget is not
a skipped or cached validation. No new 63-target primary replay is claimed.
