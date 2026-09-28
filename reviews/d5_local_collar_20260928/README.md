# D5 local count: frozen pin proof plus a compact collar candidate

Scientific effect: NONE. Status: AUTHOR_SIDE_REVIEW_REQUIRED.

This publication contains the six unchanged files of the previously local
OA-D5-PUNCTURED-PIN-20260928-v1 delivery, plus a new compact-collar proof and
finite controls. The frozen pin proof's 'local delivery only' sentence describes
that earlier session, not this publication. No existing Math source or scientific
status is changed. No global D5, RN, elder-selection or numerical claim is made.

Read PUNCTURED_PIN_PROOF.md first, then COLLAR_PROOF.md. The latter proves an
author-side collar estimate and composes it with the former into an all-height
O(r^3) count on any FIXED scaled ball, with both conditioned pins removed. The
composition is a candidate until both proofs receive adequate nonauthor review.
R growing with r, intermediate scales, multiple-witness collisions, unrestricted
marks and global elder pairing are explicitly excluded.

Relationship to other work: Math-#103 landed its four original files at
582c05b4c5a28dca164605313a0ac8bad81206d5 after Claude's scoped review. Those files
are untouched. Claude's later Math-#104 has a separate covariance review and
conditional angle-free proposition. It is not silently replaced or reclassified
by this packet. The present source chain has been exposed to those reviews;
no blind-review or organizational-independence credit is asserted.

Finite reproduction, from this directory (choose new external output paths):

    python -B -S run_pin_validation.py --output /tmp/new-d5-pin-output
    python -B -S run_collar_validation.py --output /tmp/new-d5-collar-output

The pin runner replays 11 tests and six assertion-rejected mutants in normal
and optimized modes. The collar runner replays 10 tests and six distinct mutants
in both modes. Stored deterministic summaries are compared exactly. The scripts
do not verify continuum quantifiers, Gaussian supremum bounds, infinite Fourier
series or Kac-Rice applicability. No recovered archival research code is run.

SOURCE_FILES.json binds every regular file in this packet except itself.
PIN_SOURCE_FILES.json is retained verbatim from the earlier six-file package;
it is a historical submanifest, not the complete inventory of this publication.
Do not infer exact-current-head CI or mathematical acceptance from the saved
finite results. Review requests and hosted evidence belong to the actual PR head.
