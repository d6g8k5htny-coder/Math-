# Fixed-r lifetime moments: the inverse boundary is 2/3

OpenAI / GPT-6 Astra Pro. **New author-side theorem candidate; nonauthor review
OPEN. Scientific effect NONE. No self-merge.**

For the exact determinant-weighted maximum/saddle pair-Palm law, hold the two
prescribed pins at any fixed positive embedded separation r. Let ell be the
ACTUAL ordinary elder lifetime, excluding the essential infinite lifetime.
The new proof gives two-sided small-lifetime bounds

    c_r epsilon^(2/3) <= P(0<ell<=epsilon) <= C_r epsilon^(2/3)

for all sufficiently small epsilon. Below the prescribed gap this event is
necessarily a pairing failure. Consequently the full finite-death moment domain
is q>-2/3. Inverse moments of order p are finite exactly when p<2/3, both under
the finite-death restriction and conditional on failure and finite death.
The capped critical inverse moment grows as Theta(log T); above criticality
it grows as Theta(T^(p-2/3)). No exact leading coefficient is asserted.

This fills the inverse-moment exclusion in the separately merged PR177. It
uses neither PR170/175's marked-limit candidates nor PR181's extreme-selected
law. The latter conditions on distant partners AFTER r->0 and has a different
small-lifetime exponent; it must not be substituted for this fixed-r law.

## Why the exponent is 2/3

A deterministic sphere around the prescribed maximum forces
ell >= c lambda_min^3/K^2, where K controls the third derivative. Conditional
Gaussian norm moments retain K inside the endpoint determinant weight. The
remaining soft-eigenvalue integral is exactly

    integral_0^1 lambda min(1,s^3/lambda^3)d lambda=(3/2)s^2-s^3.

An open Schur-coordinate sector gives the converse. The Hessian has a soft
curvature -lambda but a positive cubic derivative along an adapted direction.
A short straight path reaches a point above birth with only O(lambda^3) loss.
The original determinant weight supplies lambda, and full jet support supplies
d lambda. Thus the lower probability is of order epsilon^(2/3) as well.
The off-diagonal Hessian entries range over a fixed OPEN box, not a zero-measure
slice or a box shrinking with lambda.

## Exact boundaries

All constants can depend on fixed r,d,L,b,k and frame. No r-uniform rate,
interchange of limits, density equivalent, numerical amplitude, inverse-moment
convergence as r->0, or result conditional on a distant partner is claimed.
No source selection theorem, global count asymptotic or hard-fibre bridge is
required: maximin paths and local barriers control the actual lifetime directly.

PROOF.md contains the full arguments. SOURCES.json binds the one parent model
carrier; only its model/weight conventions and fixed-jet Fourier facts are used,
and the latter are proved again here. Parent asymptotic theorems are not promoted.

## Replay

    python -B -S frontiers/fixed_r_inverse_lifetime_20260930/verify.py

The full mode requires the exact parent Git object. For a standalone extraction:

    python -B -S verify.py --local-only

Local-only explicitly reports that historical project sources are not checked.
Thirty test methods run in each normal/optimized mode; six intentionally wrong
variants must fail per mode. Exact controls include36 Schur matrices across
four hard dimensions,36 Taylor-path cases/612 grid checks,36 local barriers,
and11 source/inventory fixture tests. These finite checks are not acceptance
of the Gaussian integration or the theorem. No new Lean formalization.

The foreground work follows Dylan's NEW explicit September30 continuation
request, after the September27 stop. No stopped process or timer is restarted.
Review A covers Gaussian support/regression and the upper weighted bound;
review B covers the Schur sector, lower bound and moment domain.
