# Theorem candidates pending review and test

Scientific effect: **NONE**. Publication of this list is not acceptance.

Algebra already checked is noted. Continuum or missing public tests are the pending obligation.

## C1. Planar elder-failure lower bound (Math-#116)

Source: `frontiers/window_multiplicity_laws_20260928/ELDER_LOWER_AND_DENSITY_GAP.md` at head `0507e3a1dbd3dede84cbeb805947c70aa16ebc36`.

Candidate: in d=2, compact marks and frames,

    1 - p_r >= c r^3

for small r, hence with the parent upper bound `1-p_r = Theta(r^3)` and
`nu_cand(ell)-nu_eld(ell)=Theta(ell^{2/3})`.

Finite identities checked: cubic `G_k` pins correctly; path nodes evaluate to `0`, `-7k/32`, `-7k/32`, `+17k/64`; extra saddles at `X=-3/4`, `Z^2=15/8`, height `-7k/32`.

Pending: 10-jet covariance floor; `Q_r` box mass `>= c r`; `W_r >= c r^4` on that box; comparison with `Z_r <= C r^2`; public runnable suite (`algebra.py` is not in the PR).

## C2. Local window multiplicity (Math-#116)

Source: `frontiers/window_multiplicity_laws_20260928/LOCAL_MULTIPLICITY.md` at `0507e3a1dbd3dede84cbeb805947c70aa16ebc36`.

Candidate: `P(N_global >= 2) = Theta(r^3)` in the planar height window.
The same global order conclusion is now available by the separate reviewed Palm
route in `frontiers/c6_palm_route_20260929/PROOF.md`; that theorem does not
validate this candidate's local jet-box mechanism. If the mechanism here were
established with its stated first-moment upper bound, it would give an independent
local explanation of the failure of global conditional uniqueness. This is not an
acceptance transfer from the Palm theorem.

Pending for this candidate: the jet-box probability lower bound together with the
planar first-moment upper bound (I5), as a matched local mechanism, plus public
tests.

## C3. Remote ordered-pair kernel and beta-gap law (Math-#116)

Source: `frontiers/window_multiplicity_laws_20260928/REMOTE_PAIR_LAW.md` at `0507e3a1dbd3dede84cbeb805947c70aa16ebc36`.

Candidate: for fixed remote exclusion and a fixed deterministic positive-volume
Borel set `E`, let `T_ij(E)` count ordered distinct window critical-point pairs with
indices `i,j` and both positions in `E`. Then

    E[T_ij(E)] = r^5 integral_E K_ij(x) dx + o(r^5),
    E[N(E)(N(E)-1)] = r^5 integral_E sum_{i,j} K_ij(x) dx + o(r^5).

The kernel is supported on adjacent indices. Under the normalized expected
ordered-pair measure, the joint deficit density is
`f(a,b)=(5/9)|a-b|^(-1/3)` on `(0,1)^2`. The scalar gap `G=|a-b|` instead has
`f_G(g)=(10/9)g^(-1/3)(1-g)` on `0<g<1`, the Beta(2/3,2) density.
This is a factorial-weighted mean law, not a pair-event-conditioned law. The
little-o is for fixed `E`, not arbitrary oscillatory `E_r`.

Finite identities checked: Beta(2/3, 2) has mean `1/4` and variance `9/176`.

Pending: the contact Gaussian coefficient, extra-conditioned weight limit, overlap `(k-s^3|t|)_+`, L1 translation, and public tests.

## C4. Distance-moment transition (Math-#116)

Source: `frontiers/window_multiplicity_laws_20260928/REMOTE_DISTANCE_MOMENTS.md` at `0507e3a1dbd3dede84cbeb805947c70aa16ebc36`.

Candidate: for each fixed moment order `p>=0`, ordered-pair distance moments `M_p` scale as `r^{5+p} A_p` for `0<=p<1`, `r^6(A_1+B_1)` at `p=1`, and `r^6 B_p` for `p>1`.

Pending: radial envelope `C(r^{12} delta^{-8}+r^6)`, equal-height contact kernel, loss of uniform integrability at moment order 1, public tests.

## C5. Remote singleton height mark (Math-#116)

Source: `frontiers/window_multiplicity_laws_20260928/HEIGHT_MARKS.md` at `0507e3a1dbd3dede84cbeb805947c70aa16ebc36`.

Candidate: conditional on a remote occurrence, height in the window is asymptotically uniform and independent of the joint location/index mark, at `O(r)` TV.

Pending: source-bound use of the pre-height-integrated remote kernel. Math-#115
was integrated at `4b2aa45b2f995fc27c16ec37cccb081821eda74c` with a scoped
nonauthor review, but its proof explicitly omits the height law. This new height
candidate does not inherit acceptance from that merge.

## C6. Torus-wide factorial moments: reviewed global order; regional mechanism open

The reviewed planar Fourier-cutoff theorem now supplies, for fixed `T`, compact
positive-gap marks and existential constants,

    E_{Q_r^W}[N(N-1)] <= C r^3 log(1/r).

Full proof: `frontiers/c6_fourier_cutoff_20260929/PROOF.md` at Math main
`4d062e2a976abc8800a1ae63a49a943526b6bc0d`. The source-bound reading note is
`reviews/c6_fourier_completion_20260929/READING_NOTE.md`; Anthropic nonauthor
review 5356335148 ACCEPTs the stated planar composition. The complete planar
D5/I5 reading rule is load-bearing. Tests and the merge do not substitute for
that analytic review.

The later sharp route is a separate reviewed/merged packet, not part of this
planar graph transition. `frontiers/d5_dimension_lift_20260929/PROOF.md`
(Math-#141, merge `e1ca400`) supplies the fixed-`d` first-moment inputs, and
`frontiers/c6_palm_route_20260929/PROOF.md` (Math-#145, merge `820d443`) gives
`E[(N)_q]<=C_q r^3` for fixed `q>=2` and
`E[N(N-1)]=Theta(r^3)` in every fixed `d>=2`, at the exact scopes and review
exposures stated in those packets. The conditional consequences in
`frontiers/c6_rare_cluster_laws_20260929/PROOF.md` (Math-#153, merge
`190cf2b`) are likewise separate: they do not identify a unique limiting
cluster law and do not move a graph node.

These separate reviewed/merged packets resolve the global sharp-order and
higher-dimensional first-moment statements at their recorded scopes. They do
not close the regional shrinking-witness mechanism: the planar graph node
`math.rn-region.witness-collision` remains `OPEN_ACTIVE`. This catalog line
therefore distinguishes a proved global result from an unresolved regional
explanation rather than treating the global result as open.

The fixed-remote `O(r^5)` result remains separate: both witnesses stay a fixed
distance from the pins. Source: `frontiers/remote_collision_20260928/PROOF.md`.

Open task: prove or refute the shrinking-separation witness-collision mechanism
encoded by the open graph node, without inferring it from the global Palm
bound. Numerical constants and a unique limiting cluster law also remain
outside the reviewed packets cited above.
## C7. Unrestricted selection-difference rate

Candidate: Theorem C's unrestricted densities satisfy

    0 <= nu_cand^{all}(ell) - nu_eld^{all}(ell) <= C ell^{2/3}.

Written support: the compact-mark case is the parent difference estimate under
Theorem A in `imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md`
at `5a5b97d2c518dd5c04c89d17029ec96e721d3b78`. #116 C1 would make the compact exponent sharp.

Pending: a rate in the unbounded-mark dominated-convergence argument of parent §13; parent text presently does not claim this unrestricted remainder.

## C8. Numerical constants

Candidates: explicit finite `C`, `r_*`, `z_*`, `c_{B,K}`, `c_{d,L}` on a declared compact-mark / torus band.

Pending: a certified covariance-enclosure / finite-band program. No numerical value is recorded here.

## Not candidates

All-height intermediate first moment `O(r^3)` is false for the shell method: intensity `O(r)` times shell area `Theta(s^2)` sums to `O(r)`, not `O(r^3)`. The height window in (I18) is load-bearing.
