# RN mesoscopic annulus: a scaled compactness reduction

**Object:** RN-MESOSCOPIC-ANNULUS-REDUCTION-20260925-v1  
**Author:** OpenAI / ChatGPT. **Disposition:** author-side reduction; nonauthor analytic review open.

## 1. Why this is a new region

The fixed-remote theorem controls witness locations whose distance from the coalescing maximum/saddle midpoint stays above a fixed rho>0. It explicitly does not cover locations x=r y whose distance shrinks with r. This note treats the first missing scale:

    x = r y,       A <= |y| <= B,

for fixed 1<A<B<infinity, with the same exact normalized periodized Gaussian field, pins M=-ru/2, S=ru/2, heights b and b-k r^3, and zero gradients.

The result below is deliberately a REDUCTION. It identifies the exact scaled contact law and proves uniform nonsingularity on every fixed scaled annulus away from the two pin locations. It does not yet bound the resulting three-determinant Kac-Rice integral by the power required for the full RN certificate.

## 2. The correct witness variables

Let R be an orthonormal frame with axial direction u=Re1 and write x=r R y. The endpoint observation transform U_r is the centered nonsingular transform used in the parent and fixed-remote proofs, with contact limit

    U_0=(f, f_x, f_xx, f_xxx, f_yj, f_xyj)_0,

and target v_0=(b,0,0,12k,0,...,0).

A raw remote gradient grad f(rRy) is NOT the right object as r->0: its leading components are already forced by U_0 and its residual covariance collapses. Taylor expansion shows that after the pin constraints the first nontrivial witness gradient information occurs at higher jet order.

Define the scaled residual witness map by subtracting the Hermite polynomial determined by U_r and dividing each component by its first nonzero power of r. Equivalently, choose the unique linear transform S_r(y) of

    (U_r, grad f(rRy), f(rRy))

whose first block is U_r and whose remaining rows are centered divided differences that converge to distinct contact-jet functionals. Denote the latter block J_r(y).

For y separated from the scaled pin sites +-e1/2, the contact rows J_0(y) are nonzero polynomial combinations of derivatives of orders 2 through 4 at the midpoint. Their coefficients are polynomial/rational functions of y. The exact list depends on whether the height row is retained; no finite-r determinant/Jacobian may be inserted twice when this is used only as a re-expression of conditioned observations.

## 3. Scaled-annulus covariance lemma

**Lemma A.** Fix 1<A<B<infinity and a compact birth/gap set with k bounded away from zero. On

    K_AB={ (R,y): R in O(d), A<=|y|<=B },

and after excluding any scaled pin site if it lies in the chosen annulus, the covariance of the independent rows of (U_0,J_0(y)) is positive definite. Its smallest eigenvalue has a positive minimum on K_AB. Moreover the covariance of the finite-r transformed vector (U_r,J_r(y)) and all Schur complements needed for the witness Hessian converge uniformly to their contact limits.

**Proof.** Every contact row is a finite linear combination of derivative-evaluation functionals at one site. After removing any algebraically dependent row, a zero-variance linear combination is a polynomial differential functional P(D)f(0). The periodized field has strictly positive Fourier variance on every lattice mode. Hence zero variance forces P(2pi i n/L)=0 for every n in Z^d, so P is the zero polynomial and every row coefficient vanishes. The coefficients vary continuously in (R,y). On the compact annulus, after a fixed rank chart is chosen, the least covariance eigenvalue is therefore positive and attains a positive minimum.

For finite r, centered Taylor/divided-difference remainder formulas express every row of J_r(y)-J_0(y) as r times (or, for symmetric rows, r^2 times) a bounded linear combination of finitely higher derivatives at points inside a ball of radius Cr. The positive Fourier spectrum gives uniform finite moments and uniform covariance derivative bounds. Thus covariance matrices and cross-covariances converge uniformly. Positive contact eigenvalue margins persist for small r, and Schur-complement continuity gives the same conclusion after conditioning. QED.

**Important qualification.** A single rank chart need not work all the way to the algebraic loci where the chosen divided-difference basis changes rank. A complete annulus proof must cover K_AB by finitely many rank charts and show their overlap transformations have bounded determinants. Lemma A supplies the compactness mechanism once those exact rows are enumerated.

## 4. Kac-Rice after x=rRy: the spatial power is explicit

For an actual witness critical point, dx contributes

    dx = r^d dy

on the scaled annulus. The between-pin height interval still has length k r^3. The endpoint typed product W_r is still O(r^2) under the full pins. After division by Z_r~r^2 these endpoint powers cancel.

What is new is the witness gradient density and witness determinant under the collapsing geometry. Let

    gamma_AB(r,y) =
      p_(grad f(rRy)|U_r=v_r)(0)
      E[(W_r/r^2) F_j(H_(rRy)) | U_r=v_r, grad=0]
      /(Z_r/r^2).

Then

    E_Qr^W N_j({rRy:A<=|y|<=B}, between-pin height)
      = r^d integral_(A<=|y|<=B) integral_(b-kr^3)^b
            gamma_AB(r,y,t) dt dy.

The full RN target for this annulus is therefore equivalent to an explicit bound on gamma_AB. To obtain an O(r^3) expected count it suffices to prove

    gamma_AB(r,y,t) <= C r^(-d)

uniformly; any gain over r^(-d) improves the annulus order. A naive fixed-remote covariance bound cannot establish this because the raw gradient covariance degenerates. Lemma A converts the problem into the scaled contact variables J_r(y), where the degeneracy is represented by an explicit determinant power of the linear transform.

## 5. The next exact calculation

The load-bearing missing quantity is now finite dimensional:

1. enumerate the independent contact rows J_0(y) for gradient plus height after the six/eight pin constraints;
2. compute the exact r-power of det S_r(y) on each rank chart;
3. express the conditioned witness Hessian in the same chart;
4. combine its typed determinant with the gradient-density Jacobian;
5. prove the resulting contact integrand is locally integrable across chart boundaries and uniformly bounded on A<=|y|<=B.

This is the mesoscopic analogue of the endpoint Hermite transform. It is the correct place to use symbolic exact arithmetic and mutation tests. It is NOT enough to sample covariance eigenvalues on a y-grid.

## 6. What this advances and what remains

This note removes one conceptual ambiguity from the open RN annulus task: the obstruction is not failure of Gaussian smoothness or lack of a compactness principle. The obstruction is the exact **scaled divided-difference Jacobian and witness determinant ledger**. Once those powers are computed, every fixed scaled annulus is a compact Gaussian integral problem.

Still open:

- the exact J_0(y) row list and determinant exponent in each chart;
- the inner limit |y| approaching the pin sites +-e1/2;
- the transition from fixed scaled B to distances r<<|x|<<rho;
- witness-witness collision charts;
- numerical all-cell/24-jet certification and any legacy Boolean.

No fixed-remote theorem is silently extended into this scale.
