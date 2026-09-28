# Fixed-remote witness collisions (CL-D5-REMOTE-COLLISION-20260928-v1)

Author-side proof candidate by Anthropic Claude. Nonauthor review required. Scientific effect: NONE.

Read `PROOF.md`. It proves, in the exact model of the reviewed fixed-remote theorem
(`frontiers/remote_window_20260924/PROOF.md`), four results:

- **Theorem C.** Ordered pairs of height-window critical points in the remote region `D_rho` at any
  separation below a fixed `eta_0` have `Q_r^W`-expected number `O(r^5)`. This is the witness-collision
  region inside `D_rho`.
- **Corollary D.** The second factorial moment on `D_rho` is `O(r^5)`.
- **Corollary E.** The probability of an additional remote window critical point is
  `k r^3 integral Lambda + O(r^4)`. This is a matching lower bound that the remote theorem did not supply.
- **Corollary F.** The torus-wide probability of an additional window critical point is at least
  `c r^3` in every fixed `d`, with `c=(k_-/2) inf integral Lambda_j`. For `d=2` only, the matching `C r^3`
  upper bound is conditional on the pending import (I5) (Math-#107/#109). #107 is planar, so for `d>2`
  no upper half is claimed.

Finite controls (standard library only):

    python -B -S collision_exact_check.py          # rc 0, output = RESULTS.json
    python -B -O -S collision_exact_check.py       # rc 0, byte-identical
    python -B -S collision_exact_check.py --mutant {jacobian-exponent,trapezoid-constant,one-determinant,window-factor,bonferroni-sign}   # rc 1

These checks verify exact identities and power ledgers. They do not certify the continuum
or Gaussian steps.
