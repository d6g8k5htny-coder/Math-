# Addendum: the global derivative-weighted rare-count bound

Object: OA-SPECTRAL-CLUSTER-CLOSURE-20260929-GD1.
Author: OpenAI / GPT-6 Astra Pro, 29 September 2026.
Disposition: author-side conditional derivation; nonauthor review REQUIRED.
Scientific effect NONE. The main PROOF.md is unchanged and does NOT depend on
this addendum. This closes a separately proposed sufficient route if its source
interfaces and the new insertion argument below are accepted.

## 1. Exact statement and inputs

Use the ORIGINAL count N_r, Q_r, W_r, full Z_r, and Q_r^W of PROOF.md Section1.
Fix d>=2 and L. Birth and positive-gap marks may range over fixed compact sets,
with k bounded away from zero, and the axial frame over O(d). For each fixed
p>=0 there are C_p,r_p>0 such that

    E_(Q_r^W)[ N_r (1+||f||_C4)^p ] <= C_p r^3,   0<r<=r_p.        (GD1)

In fact the same holds with C4 replaced by C6. Constants are not numerical, not
uniform in p, d, L or escaping marks. This is a new consequence of the REGIONAL
proof estimates in [C6], not a consequence of the bare scalar statement
E(N_r)_q=O(r^3). No independence between count and derivatives is assumed.

The only proof input beyond elementary inequalities is the exact pinned [C6]
proof at source cut7a1cb09, blob89eb8adf08fe7afc2cab9662d3a9875c05ae5cc5:
- Lemma4.4: under each actual witness regression Q', the source's
  K=C0(1+||f||_C6)>=1 satisfies E_Q' K^u <= C_u(1+beta)^u for fixed u.
- Lemma5.1: Kac-Rice for a nonnegative Borel full-field mark, with canonical
  Gaussian kernels and monotone exhaustion. It is stated under Q_r.
- Section5.2 and Section6: pathwise geometric bounds on W_r F_j(H_X), density
  bounds and the regional beta/penalty table; the normalized integration ledgers
  of the pin balls, collar, intermediate shells and fixed remote region.

All those inputs are retained at their source scope, not revalidated by this
addendum. SOURCES.json already binds the complete [C6] and its parent [D5]/[P]
identities. No use is made of #157, #159, or the new spectral proof's conclusions.

## 2. One full normalizer, one derivative mark

Let Xi=K^p. It is nonnegative and Borel on the smooth field space. Applying the
source's formula with mark W_r Xi, and then dividing by the ORIGINAL normalizer,

    E_QW[N_r K^p]
      = Z_r^-1 sum_j integral_X integral_Ir p_(grad f(X),f(X)|pins)(0,h)
              E_Q'[W_r F_j(H_X) K^p] dh dX.                       (GD2)

The two conditioned pins are removed by compact exhaustion. In the all-height
pin-ball/collar regions one may integrate the gradient-only kernel instead;
that gives an upper bound on the window count. A height window of length kr^3
is retained in the shell and remote regions. This never becomes an all-height
global O(r^3) assertion.

If a regional source bound is W_r F_j(H_X)<=G_r(X,h) K^(3d), then directly

    E_Q'[W_r F_j(H_X) K^p]
         <= G_r E_Q'[K^(3d+p)]
         <= C_p G_r (1+beta)^(3d+p).                            (GD3)

The source's unmarked estimate is the same expression with exponent3d. Thus the
ONLY new cost is a factor (1+beta)^p; G_r, the spatial/height Jacobians and Z_r
remain unchanged. Where the source has already used Z_r>=z_*r^2 to write a
normalized pathwise bound, use that version exactly once. No additional Z_r
appears and none is removed. This direct moment bound does not use a
Cauchy-Schwarz factor with a missing square root.

If p is not an integer, bound K^p by K^ceil(p); it suffices to prove the integer
cases. The full conditional C6 moment is available for every such fixed order.

## 3. Regional absorption with explicit new losses

For x>=1, M>=0 and a,c>0,

    x^M exp(-c x^a) <= C_(M,a,c) exp(-(c/2)x^a),
    C_(M,a,c)=max{1,[2M/(a c e)]^(M/a)}                         (GD4)

with the M=0 expression interpreted as1. Maximize M log x-(c/2)x^a to obtain
this inequality. Thus a fixed polynomial cost is absorbed by half the Gaussian
penalty; the remaining half is still available for the original positive
regional integration. No power of r or shell radius has to be weakened.

Here is the complete additional-cost ledger from [C6] Section6. All labels and
beta bounds are those of that pinned source, not new nondegeneracy assumptions.

| Region | Source beta bound | Extra K^p cost | Penalty retained for absorption | Resulting normalized integral |
|---|---|---|---|---|
| R1-I, punctured pin ball | C(1+chi) | C_p(1+chi)^p | exp(-c chi^2) | C_p r^3 |
| R1-II, pin axial region | C/r, since chi<=1/r | C_p r^-p | exp(-c/(2r^2)) | C_p r^3 |
| R2a, collar axial strip | C r^-10 | C_p r^-10p | exp(-c r^-2/3) | C_p r^3 |
| R2b, collar small nonzero v | C norm(v)^-4 | C_p norm(v)^-4p | exp(-c/norm(v)^2) | C_p r^3 |
| R2c, collar away from axis | C | C_p | no new penalty needed | C_p r^3 |
| R3a, shell axial strip | C s^-10 | C_p s^-10p | exp(-c s^-1/4) | C_p r^3 s^2 |
| R3b, shell off axis | C norm(v)^-6 | C_p norm(v)^-6p | exp(-c/norm(v)^2), or bounded away from axis | C_p r^3[(r/s)^2+s^2] |
| R4, fixed remote region | C | C_p | no new penalty needed | C_p r^3 |

Details of the integrations:

R1-I: the source's factor r^(3-d)|q|^(2-d) is multiplied by a polynomial in
chi and exp(-c chi^2). The extra (1+chi)^p changes only the finite supremum of
that product. The same omega_d integrability and r^d spatial Jacobian give r^3.
R1-II: chi<=1/r, so use (GD4) with x=1/r, M=p, a=2. The remaining exponential
absorbs the original negative radius powers exactly as in [C6](6.3). The
S-centered pin ball is identical; the full normalizer is unchanged.

R2a: use x=1/r, M=10p, a=2/3, then the original source's density/weight radius
ledger with c replaced by c/2. R2b: use x=1/|v|, M=4p, a=2. The factor
r^(3-d) remains, and integration over the scaled collar supplies r^d. R2c has
bounded beta and hence no new singular factor.

R3a: the source's AXIS-SAFE endpoint-short-column bound is valid on the entire
strip, not only at v=0. It gives W_r F_j(H_X)/Z_r<=C K^(3d). The extra moment
cost s^-10p is absorbed using x=1/s, a=1/4. The normalized intensity can still
be bounded by a constant. The source's spatial strip volume is at most C s^d,
which is at most C s^2 for d>=2 and s<=1; the retained height window gives r^3.
Thus this contribution is C_p r^3 s^2.

R3b: the unchanged geometric and density part leaves
s^(-(d+2))(r+s^2)^2 times an inverse-v polynomial and exp(-c/|v|^2). Absorb the
new |v|^-6p using (GD4). Multiplication by shell volume s^d and height length
kr^3 gives C_p r^3[(r/s)^2+2r+s^2]. Since 2r<=r^2/s^2+s^2, this is at most a
constant times r^3[(r/s)^2+s^2]. The same estimate applies where |v| is bounded
away from zero, by bounded beta rather than a singular exponential inequality.

R4: the complete witness value/gradient law at fixed distance has bounded beta.
The endpoint short columns supply r^2 in W_r, canceled by the one full Z_r~r^2;
the window supplies kr^3. Any fixed added conditional derivative moment remains
bounded. The spatial region has fixed finite volume.

Finally sum the dyadic shells s=2^j*4r up to the fixed small cutoff s0:

    sum_j (r/s_j)^2 <= C,       sum_j s_j^2 <= C s0^2.

Together with the two pin balls, collar and fixed remote region, (GD2)-(GD3)
give (GD1). The proof is uniform on the same fixed compact marks/frames because
all conditional-moment and penalty constants in the pinned source are uniform
there, and p is fixed before those constants are chosen. QED, conditional on
the declared regional source interfaces.

## 4. Consequences and exact relationship to the main proof

For T>=1,

    r^-3 E_QW[N_r; 1+||f||_C4>T] <= C_p T^-p.                  (GD5)

This is an actual rare-intensity derivative tail: it is not obtained by dividing
an unconditioned derivative-tail probability by r^3. It also gives bounded fixed
polynomial derivative moments under the count-size-biased law N_r dQ_r^W/EN_r,
using the already positive order-r^3 lower bound on EN_r.

If #158's compact-sector and deterministic-exclusion arguments are consumed at
their eventual accepted scopes, (GD5) supplies the sufficient probability input
D11 proposed in that packet. The main spectral proof in this packet instead
uses its own residual absorption and does not need (GD1). Neither route is
circular: this addendum uses only the earlier [C6] regional proof, and the main
proof never imports this addendum.

No exponential derivative moment, convergence rate of the cluster coefficients,
numerical constant, or change in a parent source's acceptance status follows.
Nonauthor review focus: one Z_r^-1 in (GD2); the exact conditional K moment in
(GD3); all eight table rows, especially R1-II and the full R3a strip; and the
unchanged height-window factor in the intermediate/remote regions. Finite
companion probes verify powers and the elementary absorption inequality only.
