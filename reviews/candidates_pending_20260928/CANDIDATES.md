# Theorem candidates pending review and test

Scientific effect: **NONE**. Publication of this list is not acceptance.

Algebra already checked is noted. Continuum or missing public tests are the pending obligation.

## C1. Planar elder-failure lower bound (Math-#116)

Source: `frontiers/window_multiplicity_laws_20260928/ELDER_LOWER_AND_DENSITY_GAP.md` at head `0507e3a1`.

Candidate: in d=2, compact marks and frames,

    1 - p_r >= c r^3

for small r, hence with the parent upper bound `1-p_r = Theta(r^3)` and
`nu_cand(ell)-nu_eld(ell)=Theta(ell^{2/3})`.

Finite identities checked: cubic `G_k` pins correctly; path nodes evaluate to `0`, `-7k/32`, `-7k/32`, `+17k/64`; extra saddles at `X=-3/4`, `Z^2=15/8`, height `-7k/32`.

Pending: 10-jet covariance floor; `Q_r` box mass `>= c r`; `W_r >= c r^4` on that box; comparison with `Z_r <= C r^2`; public runnable suite (`algebra.py` is not in the PR).

## C2. Local window multiplicity (Math-#116)

Source: `LOCAL_MULTIPLICITY.md`.

Candidate: `P(N_global >= 2) = Theta(r^3)` in the planar height window, so global conditional uniqueness is false and a global `O(r^5)` factorial upper bound is false.

Pending: the jet-box probability lower bound together with the planar first-moment upper bound (I5), as a matched Theta statement, plus public tests.

## C3. Remote ordered-pair kernel and beta-gap law (Math-#116)

Source: `REMOTE_PAIR_LAW.md`.

Candidate: for fixed remote exclusion and deterministic positive-volume `E`,

    E[N(E)(N(E)-1)] = r^5 integral_E K_{ij} + o(r^5),

with `K_{ij}` supported on adjacent indices; under the normalized expected ordered-pair measure the deficit-pair gap has density `(5/9)|a-b|^{-1/3}` and law Beta(2/3, 2).

Finite identities checked: Beta(2/3, 2) has mean `1/4` and variance `9/176`.

Pending: the contact Gaussian coefficient, extra-conditioned weight limit, overlap `(k-s^3|t|)_+`, L1 translation, and public tests.

## C4. Distance-moment transition (Math-#116)

Source: `REMOTE_DISTANCE_MOMENTS.md`.

Candidate: ordered-pair distance moments `M_p` scale as `r^{5+p} A_p` for `p<1`, `r^6(A_1+B_1)` at `p=1`, and `r^6 B_p` for `p>1`.

Pending: radial envelope `C(r^{12} delta^{-8}+r^6)`, equal-height contact kernel, loss of uniform integrability at moment order 1, public tests.

## C5. Remote singleton height mark (Math-#116)

Source: `HEIGHT_MARKS.md`.

Candidate: conditional on a remote occurrence, height in the window is asymptotically uniform and independent of the joint location/index mark, at `O(r)` TV.

Pending: source-bound use of the pre-height-integrated remote kernel; does not inherit Math-#115 as accepted.

## C6. Torus-wide second factorial moment

Candidate: `E_{Q^W} N(N-1) <= C r^5` for the full torus window count (pins removed).

Written support: off-pin P_eta gives the bound when both witnesses stay a fixed distance `eta>0` from the pins (#110 / P_eta).

Pending: pair Kac-Rice when at least one witness enters `{|X|<eta}`, i.e. a pin-neighborhood pair floor. Cauchy-Schwarz on (I5) does not produce this bound.

## C7. Unrestricted selection-difference rate

Candidate: Theorem C's unrestricted densities satisfy

    0 <= nu_cand^{all}(ell) - nu_eld^{all}(ell) <= C ell^{2/3}.

Written support: the compact-mark case is the parent difference estimate under Theorem A. #116 C1 would make the compact exponent sharp.

Pending: a rate in the unbounded-mark dominated-convergence argument of parent §13; parent text presently does not claim this unrestricted remainder.

## C8. Numerical constants

Candidates: explicit finite `C`, `r_*`, `z_*`, `c_{B,K}`, `c_{d,L}` on a declared compact-mark / torus band.

Pending: a certified covariance-enclosure / finite-band program. No numerical value is recorded here.

## Not candidates

All-height intermediate first moment `O(r^3)` is false for the shell method: intensity `O(r)` times shell area `Theta(s^2)` sums to `O(r)`, not `O(r^3)`. The height window in (I18) is load-bearing.
