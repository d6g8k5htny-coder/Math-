# Independent finite smooth incidence reconstruction

17 October 2026. Nonauthor reviewer `/root/reverse_localization_nonauthor_review_20261017`.
This is an analytic reconstruction of the finite case used by the frozen proposal,
not a new stochastic hypothesis, an implementation test, or a general nonsmooth
area/coarea claim.

Let Phi:Omega subset R^n -> R^n be smooth. On a compact subdomain its derivative
is bounded and uniformly continuous. For a grid cube of side delta meeting the
critical set, choose a critical point x in that cube. Taylor's first-order
remainder is bounded by epsilon(delta)*delta throughout that cube, with
epsilon(delta)->0 uniformly. Since D Phi(x) has rank at most n-1, the image
of the cube lies in a rotated box whose n-1 long dimensions are at most C delta
and whose remaining dimension is at most C epsilon(delta) delta. Its outer
Lebesgue measure is at most C epsilon(delta) delta^n. There are O(delta^-n)
cubes in a fixed bounded subdomain. Thus the image of the critical set there
has outer measure at most C epsilon(delta), hence zero. Exhaust compact
subdomains. This proves exactly equal-dimensional smooth Sard as needed here;
no infinite-dimensional transversality is involved. The same argument works
in chart domains by compact exhaustion.

At every regular point the inverse-function theorem supplies a neighborhood
on which Phi is a diffeomorphism. A countable such cover exists. Partition the
regular set into disjoint Borel pieces subordinate to that cover. On each
piece, ordinary change of variables, first for indicators and then simple
functions and monotone limits, gives for nonnegative Borel h

    integral h(z) |det D Phi(z)| dz
      = integral sum_{z in Phi^-1(y)} h(z) dy.

Sum the pieces by Tonelli. The critical source set contributes zero on the
left; all of its target values form a null set by the preceding argument,
so it contributes zero on the right. Truncate h first if necessary to avoid
any ambiguous infinite-times-zero notation. This is the full Borel weighted
equal-dimensional area formula for the particular smooth maps used in the
proposal. General locally Lipschitz area theory is a permitted explicit
import, but is stronger than necessary for these incidence maps.

For a fixed smooth Gaussian-tail realization and a finite standard coefficient
block split into (a,eta), invert a gradient minor B(p). The critical-point
incidence is parameterized by

    (p,eta) -> (a(p,eta),eta),
    a=-B(p)^-1(grad T+D(p)eta).

Implicit differentiation at a zero gives a_p=-B^-1 H in physical orthonormal
coordinates. Therefore the incidence Jacobian is |det H|/|det B|. For two
sites the Jacobian is |det H_p det H_q|/|det B_pair|. The coefficient density
and linear observation-fiber Jacobian cancel the minor denominator to give
the actual Gaussian density of the observations. This retains precisely one
Hessian determinant at each root. With coordinate rather than orthonormal
rows, the corresponding volume factors cancel in the ordinary chart
change of variables. Smooth local frames suffice.

The mark h can include every nonnegative Borel function of the sites and the
entire smooth field, including a nonlocal elder bar indicator. There is no
continuity assumption on that indicator. Fixing a smooth tail makes its
field dependence a Borel function of the remaining finite coefficients.
Tonelli integrates tails only after the finite identity has been proved.
The possible infinitude of total counts is harmless for the extended identity;
local finiteness follows later from the actual covariance and moment bounds.
The same construction under a contact target uses an orthonormal basis of the
finite contact kernel and its remaining standard Gaussian coordinates.

This reduction still requires identifying the finite-coefficient fiber at its
literal observation target with the canonical whole-field conditional kernel.
That is a separate Gaussian calculation, not a consequence of area formula
or support. It is reconstructed in the main review and independently by the
focused dense-support/Rice reviewer. In particular the unweighted original
tail must not replace its target-dependent Bayes-weighted distribution.

Primary-source check: Abhishek Shivkumar's UT differential-topology notes for
Daniel Allcock's Spring 2023 course state smooth Sard as Theorem 1.5.1 on
one-based PDF page 14. The reviewer read that exact statement and its
surrounding definition of manifold null sets, including a rendered page.
This is a bounded theorem-statement read, not a read of the full 60-page
notes or a claim that the notes prove every import. The exact retained PDF
is 636727 bytes, SHA256
f1018cc3f838da11b3b98a5c39abc6498c0edb0eb615a3ab1f408b68e485e807.
Source: https://web.ma.utexas.edu/users/abhishek/files/notes/Differential%20Topology.pdf
The independent finite argument above and IFT/change of variables suffice for
the area formula used here; no abstract-only area/coarea citation is treated
as a proof of an all-Borel conditional Rice identity.
