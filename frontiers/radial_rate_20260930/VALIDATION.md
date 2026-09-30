# Author validation and limits

The initial eight-test mathematics scaffold returned seven failing assertions
(the zero odd-series test already passed on the zero scaffold). After exact
implementation all eight passed. Expanded mathematics tests total21.

The nineteen-test custody scaffold returned25 failing assertions including
subtests. The implemented verifier passed all19. It rejects changed identities,
missing/duplicate/unexpected source IDs, unsafe or missing paths, noncommit tree
and tag objects, Git symlinks, replacement refs, and altered packet inventories.
The replacement fixture verifies that ordinary Git reads really see the forged
bytes before confirming that the protected verifier still authenticates only
the actual original source. This is a test fixture, not observed source tampering.

Complete local result:40 tests PASS in each normal and optimized Python mode;
12 exact formal-series parameter cases; eight explicit semantic mutants rejected
with rc1 in each mode; unknown mutant rc2; deterministic baseline equal to
RESULTS.json. The source/packet verifier checks its inventory before and after
execution. No temporary output is placed in the packet during replay.

Exact controls cover all four shape integrals, formal physical-cutoff equations,
odd-term cancellation, the signed first-order term, the density multiplier13,
the TV crossing at sqrt(13/11), and exact planar Schur regressions. A Decimal
scalar diagnostic checks the constant-density endpoint remainder at three
thresholds; it is a finite diagnostic, not a Gaussian coefficient enclosure.
Exploratory SymPy integration reproduced the shape constants, but SymPy is not
a shipped dependency or a substitute for the analytic derivation.

Local runtime Python3.13.5, Git2.47.3. The workflow requests Python3.11.16, as in
the actual upstream workflows. All shipped syntax uses standard-library3.11
features. The local raw.githubusercontent.com request failed with DNS resolution
error, so no complete upstream checkout was obtained. Local-only replay states
source_pins_checked=false. The real three-source authentication remains a
HOSTED requirement, not inferred from local Git fixtures or manifest strings.
No hosted pass is anticipated in this author-time record.

The full Gaussian derivative domination and L1 smoothness are written analytic
obligations. There is no Lean formalization of this new packet. No numerical
value of C0,C2,Bsign or the critical-moment finite part is evaluated. The retained
sign and the order r->0 before t->infinity are load-bearing qualifications.

Peer support actually delivered: native review5360751376 accepts PR173 §3 Route C
at its conditional count-estimate scope and requests an explicit diagonal repair
of the alternate fixed-R/moving-cutoff reading. It does not authorize graph
execution or count as an independent review of this conversation's source proofs.
