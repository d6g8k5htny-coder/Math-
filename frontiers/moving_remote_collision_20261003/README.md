# Planar moving-cutoff window collisions

[PROOF.md](PROOF.md) proves a source-conditional bound

    E_(Q_r^W) [N(E)(N(E)-1)] <= C r^5 rho^(-98) |E|

for the actual maximum/saddle endpoint determinant tilt, fixed planar torus, compact births and compact positive gap marks, all frames, deterministic Borel E contained in D_rho, and 0 < r <= min(r_*, rho/8). Here |E| is unnormalized torus area and the factorial pairs are ordered. Both witnesses must lie outside the pin ball. Mixed inner/outer pairs, elder identification, barcode counts, global collision closure, small-gap limits and higher dimensions are outside scope.

The rate with rho=r^(1/100) is r^(-3) E(N)_2 <= C r^(51/50)|E|. The exponent 98 is a sufficient analytic bound, not an optimized or numerical constant.

The frozen proof is 29,606 UTF-8 bytes with SHA256
d94f8f2f7e809da37465729d3eca5f9793bce5fc5410d9f83e61db259ddf73df.
[SOURCE_IDENTITIES.json](SOURCE_IDENTITIES.json) binds the six exact snapshots
in [sources/](sources/) to Math- commit
7e2344166e989ae94e5732e445f445598fc75c4c. The imported full normalizer
and Gaussian/Kac–Rice interfaces remain conditional premises. E1 corrects
the parent Hessian congruence, and E2/REC preserve the precise Borel and
selection scope.

The [fresh nonauthor AI review](review/REVIEW.md) accepts the exact frozen
analytic argument conditionally and within this scope, with no required
mathematical amendments. Its [receipt](review/REVIEW_RECEIPT.json) binds the
review, independent controls and exposure record. This is technical review,
not independent human review or a scientific-status promotion.
OpenAI Codex root and /root/c99_custody_audit contributed to authorship.
Same-provider independence credit is 0; human mathematical review is NONE.
Scientific/register effect is NONE.

The standard-library controls are described in
[CONTROLS_DESIGN.md](CONTROLS_DESIGN.md). The recorded Python 3.11.16
author run in [author_controls.normal.stdout](author_controls.normal.stdout)
has 531 exact finite checks and 29 mutant rejections. Normal and -O outputs
were byte-identical. The runtime-version line may differ on another Python;
the mathematical check lines are deterministic. These finite checks are
neither the continuum proof nor mathematical acceptance.

The reviewer independently designed and ran 425 positive exact evaluations
and 46 negative-control rejections before opening the author checker.
[Independent run record](review/INDEPENDENT_RUNS.json).

Run from the repository root, with full Git history available:

    python3 -B -S frontiers/moving_remote_collision_20261003/verify_sources.py
    python3 -B -S -m unittest discover -s frontiers/moving_remote_collision_20261003 -p 'test_*.py' -v
    python3 -B -S frontiers/moving_remote_collision_20261003/author_controls.py
    python3 -B -O -S frontiers/moving_remote_collision_20261003/author_controls.py
    python3 -B -S frontiers/moving_remote_collision_20261003/review/independent_controls.py
    python3 -B -O -S frontiers/moving_remote_collision_20261003/review/independent_controls.py

The source verifier checks the frozen proof/control/review anchors, six local
source snapshots, their current original repository paths, and their exact historical commit/path/blob identities
with Git replacement objects disabled. It never fetches missing history,
executes the mathematical controls, changes source files, authenticates a
reviewer, or promotes a scientific status. Its success is custody evidence
only. The failure-case tests use temporary local Git fixtures.
