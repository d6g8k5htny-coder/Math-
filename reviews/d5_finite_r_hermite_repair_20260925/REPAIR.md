# D5 finite-r Hermite contact repair candidate

**Object:** RN-MESOSCOPIC-FINITE-R-HERMITE-REPAIR-20260925-v1  
**Author lane:** OpenAI. **Disposition:** repair candidate after PR17 falsified the unshifted PR9 rows.  
**Scientific effect:** NONE. This does not close the Gaussian density, Hessian expectation, thin-belt, pin-collision, intermediate-scale, or RN_UNIF obligations.

Let the longitudinal coordinate be x, transverse coordinate z, midpoint 0, pins M=(-r/2,0), S=(r/2,0), with

    f(M)=b,       f(S)=b-k r^3,
    grad f(M)=0,  grad f(S)=0.

Write midpoint derivatives f_{ij...}=D_{x^i z^j} f(0). Assume a uniformly bounded C^6 jet on an open neighbourhood of the entire square |x|,|z| <= B r (B >= 1), including the midpoint, pins and every Taylor segment to the witness, and Taylor the exact pin equations symmetrically before taking r→0. An annulus-only bound that omits those segments is not sufficient. The displayed O(r^4) midpoint-derivative remainders below use this C^6 control; weaker regularity gives correspondingly weaker remainder notation without changing the exact polynomial witness.

## Longitudinal finite-r Hermite identities

From f_x(±r/2,0)=0,

    f_x(0) = -(r^2/8) f_xxx(0) + O(r^4),
    f_xx(0) = -(r^2/24) f_xxxx(0) + O(r^4).

From the height difference and the preceding derivative relation,

    f_xxx(0) = 12 k + O(r^2),
    f(0)-b = -(k/2) r^3 + O(r^4).

Hence

    f_x(0)/r^2 = -3k/2 + O(r^2).

For x=r u,z=r v, Taylor gives the corrected leading longitudinal row

    f_x(ru,rv)/r^2
      = 6k (u^2-1/4)
        + f_xxz(0) u v
        + (1/2) f_xzz(0) v^2
        + O(r),

uniformly on a fixed compact scaled annulus when the required fourth/fifth derivatives are uniformly bounded.

## Transverse pin identity

From f_z(±r/2,0)=0,

    f_z(0) = -(r^2/8) f_xxz(0) + O(r^4),
    f_xz(0) = -(r^2/24) f_xxxz(0) + O(r^4).

Thus

    f_z(ru,rv)/r
      = f_zz(0) v + O(r),

so the transverse chart's r^1 row is unchanged at leading order when v is bounded away from zero, but on the axial line v=0 the first nonzero row is

    f_z(ru,0)/r^2
      = (1/2) f_xxz(0) (u^2-1/4) + O(r).

## Height row

Using the midpoint height and gradient offsets,

    (f(ru,rv)-b)/r^2
      = (1/2) f_zz(0) v^2
        + r H_corr(u,v) + O(r^2),

where

    H_corr =
        k(2u^3 - 3u/2 - 1/2)
        + (1/2) f_xxz(0) (u^2-1/4) v
        + (1/2) f_xzz(0) u v^2
        + (1/6) f_zzz(0) v^3.

The leading transverse height row remains (v/2) times the leading transverse gradient row, but the next-order height residual must use H_corr rather than the PR9 unshifted expression.

## Immediate consequences

1. Any PR9 consumer using 6 k u^2 or (1/2)f_xxz u^2 on the axial line must be regenerated.
2. The corrected axial deterministic drift is 6k(u^2-1/4), still bounded away from zero on A≤|u|≤B with A>1.
3. The corrected contact map does not by itself prove a Gaussian compensation-density bound. A pin-preserving quartic perturbation contributes at order r^3 to f_x(ru,0), so satisfying f_x=0 requires a fourth-derivative residual of order 1/r in that model. Turning this into a probability bound requires the actual conditional Gaussian mean/covariance.
4. Higher-jet identities built from the unshifted midpoint law must not be promoted merely because their algebra is internally consistent.

This repair candidate should be checked by a distinct lane and then incorporated by the PR9 author, with all dependent Jacobian/Hessian/height/RESULTS fingerprints regenerated from finite-r pin-compatible formulas.

## Quantified follow-through

[C6_REMAINDERS.md](C6_REMAINDERS.md) gives explicit bounds for seven midpoint identities and four scaled remainders, with their derivative-domain assumptions. The additional oracle solves all six finite-r pin equations by rational linear algebra across all 22 free monomial directions through total degree six; it does not construct fixtures using the contact formulas under test. The original cubic witness module and its five tests are byte-identical to the earlier PR19 source. Run `python -B -S run_validation.py --output NEW_DIRECTORY_OUTSIDE_THIS_TREE` for both-mode tests and three missing-pin-term mutants. This author-side validation does not supply the outstanding independent review or conditional Gaussian moment estimates.
