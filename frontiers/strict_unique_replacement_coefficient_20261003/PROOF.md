# The reciprocal correction is strict in every fixed admissible band

Object: C113-STRICT-UNIQUE-REPLACEMENT-COEFFICIENT-20261003-v1.
Author: actual OpenAI/Codex agent `/root/next_math_triage`, coordinated by
OpenAI/Codex root under Dylan Roy's delegation. Claim
`3cb5f1d5-6f91-4ccf-8697-751a754275b4`, Work Events row 700.
Disposition: AUTHOR-SIDE CONDITIONAL PROOF CANDIDATE; fresh nonauthor review
is required. Organizational-independence credit 0; human review NONE;
scientific effect NONE.

## 1. Exact population, retained inputs, and new conclusion

Use [U] exactly: the centered unit-variance periodized Gaussian field on the
fixed planar torus of admissible side `L>0` under [U]'s retained interfaces;
a compact birth interval (B) of positive
length; a compact gap interval (K=[k_-,k_+]) with (0<k_-<k_+); and a
distance band `0<c_0<C_0<infinity`. All are fixed. [U] counts ordinary finite
superlevel H0 bars once, selected by the existence of a rejected nearby
maximum/saddle candidate. It excludes the essential maximum, uses the
actual global elder partner, and retains distances in the original
Euclidean coordinates of the local chart.

[U] is Math-#233 at commit
`b5bf02879a5645da9a69d9944dee610e6bb14bf6`,
`frontiers/unique_replacement_bar_intensity_20261001/PROOF.md` and `ROOTS.md`.
We consume PROOF (3)--(6) and ROOTS R1--R3. The optional occurrence
corollary below additionally consumes [O], Math-#234 at
`a38449c30c44733dfb5cd128d11071fac2e0ea98`,
`frontiers/replacement_bar_occurrence_20261001/PROOF.md`, (O1)--(O4).
Both remain explicit conditional inputs; their draft or review disposition
is not changed here.

The same seven analytic sources [P, CAP, E1, E2, REC, CUB, ELDER] remain
hypotheses at their exact historical identities. In particular, we retain
the original correlated Gaussian jet density, one full normalizer, actual
elder identification, complete cubic root classification, and the finite
positive coefficient in [U]. The source paths, byte counts, Git blobs,
SHA256 values and consumed slices are listed in `SOURCE_FILES.json`.
No reference-kernel factorization or new source acceptance is used.

**Theorem.** For every fixed parameter choice just specified that satisfies
[U] and its seven retained analytic interfaces, the coefficients of [U]
satisfy

    C_U(1) < C_R.                                          (S1)

This strengthens only the upper inequality in [U] (4). Its earlier lower
bound and subsequent lower-bound refinements are not new claims here.
Under the additional [O] input, its occurrence coefficient therefore obeys

    lambda_U = L^2 C_U(1) < L^2 C_R.                       (S2)

The gap in (S1) is positive for each fixed choice. No lower bound on that
gap uniform over narrowing or varying bands, no decimal enclosure, and no
new finite-h rate is asserted.

## 2. Reduce strictness to positive multiplicity-two mass

Write the [U] cubic as

    P(X,Z) = 2kX^3 - 3kX/2 - k/2 + sZ^2/2
             + (a/2)(X^2-1/4)Z + (beta/2)XZ^2 + (q/6)Z^3,
    theta = (s,a,beta,q),
    M0 = (-1/2,0),  S0 = (1/2,0),
    B_s = beta-a^2/(12k),
    D_s = (q-a beta/(4k)+a^3/(72k^2))/2.

On the generic nonempty typed failure sector, (Y_*) is the unique highest
extra window saddle. [ELDER] identifies its continuation with the actual
elder partner. [U] defines

    D_(t,k)(theta) = #{saddle roots Y:
       P(Y)<0, Y != Y_*,
       c0 <= t|Y-M0| <= C0,
       k_- <= -P(Y)/|Y-M0|^3 <= k_+}.                     (S3)

For the following open-set construction all inequalities are strict.
Equation (S3) keeps [U]'s exact closed-cutoff definition; its integrated
membership boundaries are null by ROOTS R2. In particular,

    D_(t,k) in {1,2} almost everywhere on failure.

Define the finite positive coefficient measure

    dnu = t^4 A_0(b,k,u) dmu_fail^(b,k,u)(theta)
          dt db dk d sigma(u),

on the fixed outer domains and the generic failure sector. By [U] (3),(6),

    C_R = integral dnu,
    C_U(1) = integral D_(t,k)^(-1) dnu.

Consequently the exact comparison identity is

    C_R - C_U(1) = (1/2) nu{D_(t,k)=2}.                  (S4)

It suffices to produce an open set of multiplicity two with positive
measure under this original coefficient measure.

## 3. An explicit symmetric anchor for arbitrary fixed bands

Choose any `k_0 in (k_-,k_+)` and `t_0 in (c_0,C_0)`. For a real

    1/2 < v < 1,

temporarily take (k=k_0) and

    a=q=0,  beta=-12k,  s=-12kv.                         (S5)

This is strictly typed: (s<-|B_s|/2=-6k). Besides the two exact pins,
the two extra critical points are

    Y_+ = (-v, +sqrt(v^2-1/4)),
    Y_- = (-v, -sqrt(v^2-1/4)).                          (S6)

Indeed, at either point,

    P_X = 6k(X^2-1/4)-6kZ^2 = 0,
    P_Z = (-12kv-12kX)Z = 0.

Their Hessians and determinants are

    Hess P(Y_+/-) = [[-12kv, -12kZ], [-12kZ, 0]],
    det Hess P(Y_+/-) = -144k^2(v^2-1/4) < 0.             (S7)

Thus both are nondegenerate saddles. The maximum pin has diagonal Hessian
entries (-6k,-12k(v-1/2)), both negative. The saddle pin has diagonal
entries (6k,-12k(v+1/2)), of opposite signs.

Set

    z(v) = 2v^3 - 3v/2 + 1/2
         = 2(v-1/2)^2(v+1),
    d(v)^2 = v(2v-1),
    rho(v) = z(v)/d(v)^3.                                (S8)

Direct substitution in (S5)--(S6) gives, in the original coordinates,

    P(Y_+) = P(Y_-) = -k z(v),
    |Y_+-M0| = |Y_--M0| = d(v),
    -P(Y_+/-)/|Y_+/-M0|^3 = k rho(v).                   (S9)

On (1/2<v<1), (0<z(v)<1): its derivative is (6v^2-3/2>0), and its
endpoint values are zero and one. Also (d(v)>0), with

    z(v) -> 1,  d(v) -> 1,  rho(v) -> 1
                      as v increases to 1.              (S10)

Because (t_0) and (k_0) are interior to fixed positive-width intervals,
continuity now permits one fixed (v<1), sufficiently close to one, such
that

    c0 < t0 d(v) < C0,
    k_- < k0 rho(v) < k_+.                               (S11)

Both extra saddles then lie strictly in the window ((-k_0,0)) and
strictly satisfy the candidate distance/gap filters. The pinned saddle
also strictly satisfies them, since its distance is one and its gap is
(k_0). This choice uses no lower bound on the widths other than strict
positivity. The threshold for (v) may depend on both fixed intervals.

## 4. Move off the tie and obtain an open generic set

The anchor in (S5) has equal extra saddle heights, so it is only a
construction point; no positive mass or unique partner is asserted on
that lower-dimensional slice. The retained ROOTS R1 polynomials there are

    Sigma = 12k D_s^2 + (s-B_s)^2(B_s+2s)
          = -1728k^3(1-v)^2(1+2v) < 0,
    Delta = 12k D_s^2 + B_s^3 = -1728k^3 < 0,
    H = 12k D_s^2 + B_s^3 - 4B_s s^2
      = 1728k^3(4v^2-1) > 0.                            (S12)

Only (D_s=0) remains among those exclusions. Keep (k,s,a,beta) fixed
and perturb (q) to a sufficiently small positive value. The implicit
function theorem continues both nondegenerate saddles smoothly. Their
inertia, strict window membership and the strict filters in (S11) persist.
The two pins remain exact. ROOTS R1 allows at most two extra roots, so
these continuations exhaust the extra roots. The signs in (S12) persist,
and now (D_s=q/2>0).

For completeness the tie actually splits. Along either continued critical
branch, criticality eliminates its location derivative, giving at (q=0)

    d/dq P_q(Y_+(q)) = +(v^2-1/4)^(3/2)/6,
    d/dq P_q(Y_-(q)) = -(v^2-1/4)^(3/2)/6.               (S13)

The derivative of their height difference is positive. For a sufficiently
small positive (q), (Y_+(q)) is therefore the unique higher extra
window saddle. This also agrees with [ELDER] §7's unique-height statement
when `D_s != 0`. Under the retained actual-elder input it is (Y_*).

Exactly two saddles are rejected candidates: (S_0) and the lower
continued extra saddle. Both satisfy the strict filters; only the higher
extra saddle is excluded as (Y_*). Thus (D_{(t_0,k_0)}=2) at this
perturbed point.

All these properties are open. In particular, the four roots are
nondegenerate; their types, window margins, height ordering and candidate
filter margins persist in a sufficiently small open neighborhood

    O subset (c0,C0) x (k_-,k_+) x R^4

of the full variables ((t,k,s,a,beta,q)). The nonzero values of
(Sigma,Delta,H,D_s) persist there. ROOTS R1 still exhausts the roots,
and [ELDER] still selects the unique higher extra saddle, so

    D_(t,k)(theta)=2 throughout O.                       (S14)

The distance functions in this neighborhood use the continued roots in
the original ((X,Z)) coordinates. We have not replaced them by sheared
distances when (a) varies.

## 5. Positive mass in birth and angle as well as in the cubic variables

The geometry defining (O) is independent of the outer birth (b) and
orientation (u). Choose any `b_0` in the interior of (B) and any
`u_0 in S^1`, then small intervals/arcs `B_0` inside the interior of B
and `U_0` inside S^1 of positive length about them. The same open
geometry works for every `b in B_0, u in U_0`. This uses no isotropy:
only the density, not the cubic geometry, depends on (b,u,L).

In the coefficient measure the single normalizer cancels exactly as in
[U] (6):

    dnu = 12 t^4 pi_0(b,k,u) w(theta)
          h_0^(b,k,u)(0,a,beta,q)
          dt db dk d sigma(u) ds da d beta dq             (S15)

on the failure sector, with (w=9k^2(4s^2-B_s^2)>0). The retained
nonsingular contact and ten-jet Gaussian laws give strictly positive,
continuous densities (pi_0) and (h_0) at these finite parameters.
Their correlations remain inside this density; no independence is used.

Take a smaller open box with compact closure inside (O), and if
necessary smaller birth and angular neighborhoods. On the resulting
compact product the factors in (S15) are continuous and strictly positive,
so they have a positive common lower bound. That product has positive
Lebesgue/arc measure. It follows that

    nu{D_(t,k)=2} >= nu(O x B_0 x U_0) > 0,              (S16)

where (O,B_0,U_0) may denote the smaller neighborhoods. Finiteness is
already supplied by [U]. Equations (S4) and (S16) prove (S1); [O]'s
definition of (lambda_U) gives (S2).

## 6. Limits and falsification targets

This proves a strict comparison of two existing coefficient integrals
under their unchanged hypotheses. It does not prove or reaccept [U], [O]
or the seven analytic sources. It adds no unrestricted persistence law,
factorial bound, quantitative rate, all-mark exhaustion, changing-volume
limit, regional witness uniqueness, higher-dimensional result or scientific
status change. It does not evaluate the mass in (S16).

The proof would fail if the definition of (D) discarded the lower
window saddle, if the actual partner were not the higher extra saddle,
if the original correlated density vanished on the constructed open set,
or if either interval were allowed to have zero width. These are explicit
interfaces, not consequences of finite tests.

`check.py` checks rational algebra, finite band examples, and
deliberately incorrect finite alternatives. It does not prove the implicit
function theorem, open-neighborhood continuity, Gaussian source inputs or
the actual-elder identification. `AUTHOR_CORRECTIONS.md` preserves an
arithmetic typo corrected during author drafting before this proof was
written. The checker must not be substituted for a fresh source-bound
nonauthor reconstruction of the proof.
