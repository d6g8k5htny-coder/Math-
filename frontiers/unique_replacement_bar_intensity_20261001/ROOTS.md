# All-root stability and null membership boundaries

Object: OA-UNIQUE-REPLACEMENT-BAR-ROOTS-20261001-v1.
Authors: OpenAI/Codex root and delegated coauthor
`/root/c50_multiplicity_feasibility`; the latter's child
`boundary_nullity` independently derived the scaling-nullity and algebraic
exclusion arguments. This is disclosed author-side work, not independent review.
Scientific effect: NONE. This additive consumer does not change a source proof,
review verdict, status, graph, prize, or premise.

The exact source cut is Math- `044d42d5bd7f31df6f7e6b9034d6711e8fb7ee43`.
We consume [CUB](../planar_cubic_cluster_20260929/PROOF.md), blob
`bb446d08db8a944537a743ad550b88c1c2ad5758`, equations (C1)--(C13),
and [ELDER](../local_elder_geometry_20260930/PROOF.md), blob
`ef2aa57959ea9f721bbf2316ce94cf616c1c9113`, Theorem E and its unique-position
conclusion. Their dispositions are retained; the following lemmas are new
deterministic and measure-theoretic consumer steps. In particular, CUB's
window-only Lemma S is NOT used as an all-root stability assertion.

## R1. Explicit all-root exclusion

Use distinct notation for the distance band `0<c_0<C_0` and the cubic
coefficient `q`. For `k>0`, `theta=(s,a,beta,q)`, let

```text
P(X,Z)=2kX^3-3kX/2-k/2+(s/2)Z^2
       +(a/2)(X^2-1/4)Z+(beta/2)XZ^2+(q/6)Z^3,
M0=(-1/2,0), S0=(1/2,0),
u=X+aZ/(12k), B_s=beta-a^2/(12k),
D_s=(q-a beta/(4k)+a^3/(72k^2))/2.
```

Assume strict endpoint typing `s<-|B_s|/2`. Besides the two pins, every
critical point satisfies

```text
Q=6k(u^2-1/4)+(B_s/2)Z^2=0,
s+B_s u+D_s Z=0, Z!=0.                                 (R1.1)
```

There are at most two such points anywhere in the plane. For `B_s,D_s!=0`
elimination gives

```text
(12k D_s^2+B_s^3)u^2+2B_s^2 s u+B_s s^2-3k D_s^2=0.    (R1.2)
```

This polynomial cannot vanish identically: its linear coefficient is nonzero
because `B_s!=0` and `s<0`. Each root determines one `Z`. If `D_s=0,B_s!=0`,
the line determines `u=-s/B_s`, and `Q` gives at most two `Z`. If `B_s=0,D_s!=0`,
`Q` determines `u=+/-1/2`, and the line determines `Z=-s/D_s`. If `B_s=D_s=0`,
the strict inequality `s<0` rules out every extra point.

At every extra critical point, CUB (C8) gives

```text
det Hess P=-3k(B_s+4su).
```

Put

```text
H=12k D_s^2+B_s^3-4B_s s^2.
```

Multiplying the two equations in (R1.1) gives the identity

```text
H Z^2=3k(B_s+4su)^2.                                    (R1.3)
```

For an explicit verification, substitute `D_s Z=-s-B_s u` in `12k D_s^2 Z^2`
and substitute `B_s Z^2=-12k(u^2-1/4)` in the remaining two terms of
`HZ^2`; the sum is `3k(B_s+4su)^2`. This involves no division by `B_s` or
`D_s` and includes their zero cases. Since `Z!=0`, a degenerate extra root
forces `H=0`. The pins have determinants `3k(B_s-2s)` and `3k(B_s+2s)`,
both nonzero under strict typing. Thus outside `H=0`, EVERY finite
critical point of the cubic is nondegenerate, including points below `-k`.

This additional exclusion is a genuine null algebraic set. Define

```text
U=12k beta-a^2,
V=72k^2 q-18ka beta+a^3,
H_poly=V^2+U^3-576k^2 U s^2.
```

Then `H=H_poly/(1728k^3)`. At fixed `k>0`, the `q^2` coefficient
of `H_poly` is `5184k^4>0`, so it is a nonzero polynomial in `theta`.
Its zero set is Lebesgue null for each fixed `k`, and also for the
integrated `dk dtheta` measure. No numerical probe is used for this fact.

Retain the source exclusions

```text
Sigma=12k D_s^2+(s-B_s)^2(B_s+2s),
Delta=12k D_s^2+B_s^3,
D_s=0.
```

They respectively support window stability, ELDER's global escape argument,
and a unique limiting partner position. They are nonzero polynomial zero
sets after clearing positive `k` denominators. The new `H=0` exclusion
does not replace them. On strict typing outside this finite union,
the cubic has at most four critical points, all nondegenerate; on failure
ELDER selects a unique highest window saddle `Y_*`.

## R2. Null membership boundaries under the integrated measure

Fix a compact positive gap interval `K=[k_-,k_+]` with
`0<k_-<k_+` and the distance band above. All distances in this note are
in the original `(X,Z)` coordinates, not in `(u,Z)` coordinates.

For either `q0=k_-` or `q0=k_+`, consider the parameter set on which
some critical root `Y!=M0` obeys

```text
-P(Y)/|Y-M0|^3=q0.                                    (R2.1)
```

This set is measurable. Indeed its root condition can be written with
polynomial equalities and inequalities using `grad P(Y)=0`,
`|Y-M0|^2>0`, `P(Y)<0`, and
`P(Y)^2=q0^2 (|Y-M0|^2)^3`. Projection gives a semialgebraic set.

It is null for `dk dtheta` on the typed domain. Set `eta=theta/k`.
The map `(k,eta)->(k,k eta)` is a smooth bijection for `k>0`, with
absolute Jacobian `k^4`. Because all coefficients scale together,

```text
P_(k,k eta)=k P_(1,eta).
```

Thus all root locations remain fixed on each positive scaling ray, while
each gap ratio is multiplied by `k`. Strict typing is also preserved:
`B_s(k,k eta)=k B_s(1,eta)` and `s=k eta_s`. For fixed typed `eta`, R1's
root finiteness shows that (R2.1) permits at most one positive `k` per
root. Its `k`-section is therefore finite. Fubini in `(k,eta)`, followed
by the Jacobian `k^4`, proves nullity. This proof includes all roots
below `-k`; no window restriction was imposed.

For the radius boundaries, fix `(k,theta)` with its finite root set.
For any root `Y!=M0`, either equality

```text
t |Y-M0|=c_0 or C_0
```

permits at most one value of `t` for each endpoint. Fubini proves that
their union is null for `dt dk dtheta`, in particular when
`t in [c_0,C_0]`. The endpoints of the `t` and `k` integration
intervals themselves are null.

All these nullities persist under any measure absolutely continuous
with respect to `dt dk dtheta`, and after appending other parameters
with absolutely continuous measures. This includes the integrated
Gaussian failure measure used in PROOF.md: CUB supplies a nonsingular
ten-dimensional contact-jet covariance, hence an actual Gaussian
density `h_0(0,a,beta,q)`; multiplying it by a determinant weight,
an indicator, `z_0^(-1)`, or the outer candidate density preserves
absolute continuity. No independence between coefficients is required.

The gap-boundary assertion is deliberately integrated in `k`. At the
fixed slice `k=q0`, the pinned saddle itself has gap ratio `q0` for
every `theta`. It would be false to declare all fixed-`k` boundary
slices null. Fubini provides good `(k,t)` slices for almost every
outer integration parameter, which is exactly what the consumer uses.

## R3. Stability of all admissible roots and of the rejected count

Fix typed `(k,theta,t)` outside the exclusions of R1 and membership
boundaries of R2, with `t in (c_0,C_0)` and `k in (k_-,k_+)`.
Suppose `g_i` are normalized local functions from ELDER Theorem E,
retaining the exact two pins, their gradients and values `0,-k`,
and converging to `P` in `C^2` on every fixed disk. Their physical
scales are `r_i->0`; put `h_i=r_i/t`. Assume the actual global
fields are Morse with distinct critical values, as in the source.

Every saddle admissible for the physical `h_i` distance band belongs
in scaled coordinates to the fixed disk

```text
|Y-M0|<=C_0/t<=C_0/c_0.                           (R3.1)
```

Choose a larger fixed disk with root-free boundary, possible because
R1 gives only finitely many roots in the whole plane. Choose disjoint
small balls around each root inside that disk. All their Hessians
are nonsingular by R1. On each ball, fix the inverse Hessian at the
limiting root. By reducing the ball and the `C^2` error, the map
`x -> x-H_root^(-1) grad g_i(x)` is a contraction carrying the ball
into itself. It gives exactly one continued root there. The continued
root converges to the limiting one and has the same Hessian inertia.
On the compact complement of these balls, `|grad P|` has a positive
minimum. `C^1` convergence therefore excludes every additional root
there. Roots outside the larger disk cannot be candidates by (R3.1).
This proves complete root control in the band; no in-window count
lemma, growth of the disk with `i`, or unproved global Morse property
of the cubic is used.

The continuations retain their distance and gap membership because
the inequalities have strict limiting margins, by R2. The denominator
in a gap ratio is bounded away from zero at any admissible root;
the only zero-distance root is the exact maximum pin, whose inertia
is stable and which cannot become a saddle. The height restriction
`P(Y)<0` adds no unhandled boundary: a root at height zero has gap
ratio zero and cannot enter `K`, whose lower endpoint is positive.

If `n(theta)>0`, ELDER Theorem E and `D_s!=0` give that the actual
global partner is eventually the continuation of `Y_*`; the global
bar is eventually finite. Hence removing the actual partner from
the finite candidate list also stabilizes. Define

```text
mathcal D_(t,k)(theta)=#{saddles Y:
  P(Y)<0, Y!=Y_*,
  c_0<=t|Y-M0|<=C_0,
  -P(Y)/|Y-M0|^3 in K}.
```

Then the actual physical rejected-candidate count at scale `h_i`
is eventually exactly `mathcal D_(t,k)(theta)`. On `n=0`, ELDER
instead says that the failure indicator is eventually zero; the
consumer's failure-weighted reciprocal mark is therefore eventually
zero regardless of any other rejected candidates.

On `n>0`, the pinned saddle is admissible and rejected because
its distance is one, its gap ratio is `k`, and its height is `-k`.
Thus `mathcal D_(t,k)>=1`. There are at most two extra roots, and one of
them is the actual partner `Y_*`. Only the pinned saddle and at most
one other extra root can remain as rejected saddles. Consequently

```text
mathcal D_(t,k)(theta) in {1,2}                         (R3.2)
```

on the limiting failure population. This bound concerns the cubic
limit, not an asserted deterministic upper bound on all finite-scale
Gaussian configurations.

## R4. Exact finite checks and their limits

`check_exact.py` uses only standard-library rational arithmetic and
explicit conditional guards, so its checks remain active under
`python -O`. It verifies gradients, heights, Hessian determinants,
typing, all exclusion values being nonzero, and exact distance/gap
membership with strict boundary margins, without computing floating-point
square roots. It also verifies the seven entries of SOURCES.json against
repository-contained canonical paths, rejects symlink path components,
and checks byte lengths, SHA-256 digests and Git blob identities. An
executed wrong-digest probe must be rejected. These byte checks bind
inputs; they do not validate their mathematical content.

The original two-window fixture is

```text
k=1,a=0,beta=-3,s=-21/10,q=3/5,
Y1=(-5/8,3/4),     P(Y1)=-23/320, det Hess=-27/4,
Y2=(-5/6,-4/3),    P(Y2)=-13/45,  det Hess=-12.
```

For band `[1/2,2]`, gap range `[1/10,2]`, and `t=1`, the count is
two; at `t=8/5` it is one. Both extras are in `(-1,0)`, so this
fixture alone does NOT detect omission of candidates below the pin.

A separate below-window fixture supplies that control:

```text
k=1,a=0,beta=-3,s=-39/16,q=3/2,
Y1=(-5/8,3/4),       P(Y1)=-53/512,    det Hess=-297/32,
Y2=(-37/24,-35/12),  P(Y2)=-11125/4608,det Hess=-1155/32.
```

Here `P(Y2)<-1`, the pin determinants are `45/8,-189/8`, and
`Y1` is the unique highest window saddle. For band `[1/2,4]`,
gap range `[1/100,2]`, and `t=1`, both `S0` and `Y2` are rejected
admissible candidates:

```text
|Y2-M0|^2=5525/576,
(-P(Y2)/|Y2-M0|^3)^2=71289/10793861.
```

The full count is two; the incorrect count restricted to the
original height window plus `S0` is one. A third fixture uses a
nonzero shear and catches use of sheared distances. Further controls
catch inclusion of the actual partner, omission of reciprocal
multiplicity, and retaining a root after a radius-boundary crossing.

These are finite arithmetic checks of proof fixtures. They do not
prove continuum root stability, nullity, Kac--Rice measurability,
Palm integrability, dominated convergence, or any scientific status.
