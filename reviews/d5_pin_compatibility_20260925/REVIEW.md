# D5 review: finite-r pin offsets survive the contact blow-up

Review ID: D5-PIN-COMPATIBILITY-20260925-v1.
Reviewer/derivation lane: OpenAI / ChatGPT. Source author lane: Cursor; its underlying provider is not established by this review.
Source: Math- PR9 commit `25141b9154b5afcaa16e526f1d9055a2a4e2483d`,
`frontiers/rn_mesoscopic_chart_20260925/PROOF.md`, blob `d56613025439cce57e76e2846a80af908fcd2dd6`, sections 2, 3 and 4.5.

**Disposition: AMEND REQUIRED for the displayed deterministic pin/Taylor rows.**
This review does not refute the global Gaussian lifetime theorem, establish the full stochastic annulus estimate,
or award organizational independence. It provides an exact local counterexample to the stated algebraic expansion.

## 1. Exact six-pin witness

Let r>0, k>0, with longitudinal coordinate x and transverse coordinate z. Define

    F_r(x,z) = b - k*r^3/2 + 2*k*x^3 - (3/2)*k*r^2*x
               + (A/2)*z^2 + (a/2)*(x^2-r^2/4)*z
               + (c/2)*x*z^2 + (d/6)*z^3.

Direct substitution gives F_r(-r/2,0)=b, F_r(r/2,0)=b-k*r^3 and both gradients zero.
Its midpoint jet U_r tends to the source's U_0=(b,0,0,12k,0,0).
For A<0 and a=c=d=0 the left-pin Hessian is diag(-6kr,A), negative definite;
the right-pin Hessian is diag(6kr,A), a saddle. Thus even the required endpoint types
are compatible with the discrepancy.

The finite-r offsets are F_x(0)=-(3/2)kr^2 and F_z(0)=-a*r^2/8.
Although both vanish as r tends to zero, they do not vanish after the relevant divisions.

## 2. Corrected rows for this witness, and the failed interchange

At (x,z)=r(y1,y2), exact differentiation gives

    F_x(ry)/r^2 = 6k*(y1^2-1/4) + a*y1*y2 + (c/2)*y2^2,
    F_z(ry) = r*A*y2 + r^2*[a*(y1^2-1/4)/2 + c*y1*y2 + d*y2^2/2],
    (F_r(ry)-b)/r^2 = A*y2^2/2 + r*H_next,
    H_next = -k/2 + 2k*y1^3 - (3/2)k*y1
             + (a/2)*(y1^2-1/4)*y2 + (c/2)*y1*y2^2 + (d/6)*y2^3.

The source's row `6k*y1^2+...` omits -3k/2. Its axial transverse row
`a*y1^2/2` omits -a/8. Its height coefficient omits -k/2-(3/2)k*y1-a*y2/8.
For r=1/10,k=1,y1=2,a=2,y2=0, the actual divided gradients are 45/2 and 15/4,
whereas the unshifted formulas give 24 and 4.

This is not a remainder-size disagreement: the scaled discrepancies are nonzero constants.
The invalid operation is substituting U_0 for the finite-r constraints before dividing by r^2/r^3.
The polynomial is a local smooth deterministic witness, not a claimed sample of a periodic Gaussian field.
Its role is to test the necessary pin-compatible Taylor calculation underlying that field argument.

## 3. General deterministic correction under explicit remainder control

For a family of C^5 functions with derivatives uniformly bounded on a common neighborhood,
with the exact same six pins, put h=r/2 and evaluate midpoint derivatives. Taylor expansion of
F_x(±h,0)=0 gives

    F_x(0) = -r^2*F_xxx(0)/8 + O(r^4),
    F_xx(0) = -r^2*F_xxxx(0)/24 + O(r^3).

The height difference is -kr^3; substituting the first relation gives
F_xxx(0)=12k+O(r^2). Averaging heights gives F(0)=b-kr^3/2+O(r^4).
Similarly F_z(0)=-r^2*F_xxz(0)/8+O(r^4) and F_xz(0)=O(r^2).
These identities reproduce the shifted leading longitudinal gradient and the shifted axial
transverse gradient. For the height next coefficient one must also carry the O(r^2)
F_xz(0) term at its correct order; it contributes only O(r^4) after evaluation at ry.
The stated uniform C^5 hypothesis is deterministic. It has not been verified here as a
uniform conditional Gaussian moment/density assertion over the project's parameter region.

## 4. A bounded repair target, not another jet-enumeration campaign

Add the pin-preserving quartic term

    (D/24)*(x^2-r^2/4)^2.

All pins remain exact and F_xxxx(0)=D. On the axis the exact factorization is

    F_x(r*y1,0) = r^2*(y1^2-1/4)*(6k + r*D*y1/6).

The first free longitudinal residual in this example is order r^3. For fixed y1 away from
0 and ±1/2, cancellation requires D=-36k/(r*y1), outside a bounded-jet regime as r shrinks.
A determinant formed by varying k does not produce a density under a law that already fixes k.

A suitable next analytic lemma should establish the actual conditional mean and covariance of
(r^-3[F_x-E F_x], r^-2[F_z-E F_z]) uniformly on the stated axial chart.
If its covariance is bounded above and below and the first scaled target has size at least c/r,
the two-dimensional Gaussian density is at most C*r^-5*exp(-c'/r^2).
This follows from the standard Gaussian density formula and the diagonal Jacobian r^-5.
It is a CONDITIONAL implication: the covariance and drift hypotheses, typed Hessian factors,
height conditioning and extension to the thin belt are NOT discharged by this review.

## 5. Actions and evidence

Author: rederive finite-r Hermite pin identities, correct contact/height/axial rows and every dependent
Jacobian, conditional-Hessian and power ledger; add endpoint-preserving polynomial controls.
Mapping PR14: do not consume the old source digest as corrected chart algebra; retain noncontrolling state.
Reviewer: check the corrected digest and conditional Gaussian compensation lemma separately.
Do not spend further cycles enumerating seventh-and-higher jets before the leading constraints are fixed.

`pin_compatibility.py` and `test_pin_compatibility.py` use only Fraction-based standard-library arithmetic.
16 distinct tests passed in normal and optimized Python 3.13.5. This is exact algebraic regression evidence,
not a stochastic simulation, interval certificate, formal proof-assistant result or global theorem closure.
