# Intermediate height-window single-witness bridge

Scientific effect: NONE. AUTHOR_SIDE_REVIEW_REQUIRED.

Read PROOF.md. The proposed shell estimate is

    E N_window({s<=|X|<=2s}) <= C r^3[(r/s)^2+s^2],  0<r<=s/4.

Unlike a fixed-scaled-ball estimate, its constants are uniform as r/s tends to
zero. The dyadic sum is bounded by C r^3(A^-2+rho^2). Together with the exact
reviewed local and fixed-remote sources named in the proof, it gives a candidate
O(r^3) global first moment for additional critical points in the between-pin
height window. The two conditioned pins are excluded.

This is NOT an all-height intermediate bound, factorial-moment/collision bound,
elder-rule result, numerical certificate, or automatic change to any scientific
status. The witness height is genuinely conditioned during density disintegration
and then integrated out; there are nine actual observations, not the earlier
all-height proof's eight. The critical-height Euler cancellation supplies the
summable factor, and must be reviewed separately from the Gaussian estimates.

Finite exact reproduction (Python standard library only):

    python -B -S run_validation.py --output /tmp/new-intermediate-check

The output directory must be new and outside the source folder. The runner
checks the complete flat SOURCE_FILES inventory, 15 named tests in each mode,
and ten deliberately incorrect variants, then compares deterministic results
against RESULTS.json and verifies unchanged sources. Tests include confluent
rank, cubic row operations, Euler identities, height-conditioned polynomial
fixtures, and scale/summation ledgers. They do not prove uniform analytic
remainders, Gaussian supremum bounds, Kac-Rice hypotheses or the continuum theorem.

Original #104/#105 proof files, their historical labels, and all governing
scientific verdicts remain unchanged. This packet requires its own exact-source
nonauthor review. Prior reviews are cited for their own scopes only.
