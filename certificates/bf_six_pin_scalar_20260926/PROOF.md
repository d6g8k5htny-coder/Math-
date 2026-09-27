# Uniform scalar variance under six linear Bargmann-Fock pins

Object: OA-BF-SIX-PIN-SCALAR-20260926-v1. Author: OpenAI / ChatGPT.
Disposition: AUTHOR_DERIVATION; independent technical review requested.
Scientific effect: NONE. No existing proof or scientific status is changed.

## 1. Exact law and statement

Let f be the centered, unperiodized Gaussian field on R^2 with covariance
K(x,y)=exp(-|x-y|^2/2). Write coordinates (t,s), M=(0,0), S=(r,0), r>0.
Condition linearly on P=(f(M),f_t(M),f_s(M),f(S),f_t(S),f_s(S)).
Use the Gaussian regular conditional law, not a law reweighted by Hessian
determinants or by Morse-type/elder-selection events.

Write v(r)=Var(f_ts(M) | P). Then

    v(r) = 1 - r^2/(exp(r^2)-1).

For every 0<r<1,

    (1-r^2)/2 <= v(r)/r^2 <= 1/2.

In particular, simultaneously for every real 0<r<=1/40,

    1599/3200 <= v(r)/r^2 <= 1/2.

The same marginal variance statement holds at S by reflection. This is a
scalar statement; it is not a lower eigenvalue bound for a multi-jet block.

## 2. Gaussian-regression reduction

Set c=exp(-r^2/2), Y=f_ts(M), U=(f_s(M),f_s(S)), and let V be the four other
pins. Differentiating K gives Var(Y)=1, Cov(Y,U)=(0,rc), and

    Cov(U) = [[1,c],[c,1]].

Every covariance between (Y,U) and V vanishes by transverse parity: it has an
odd total number of s-derivatives evaluated at transverse displacement zero.
Since the variables are jointly Gaussian, (Y,U) is independent of V.
The conditional covariance therefore reduces to conditioning on U alone.
For r>0, 1-c^2>0, and Gaussian regression yields

    v(r) = 1 - (0,rc) [[1,-c],[-c,1]] (0,rc)^T/(1-c^2)
         = 1 - r^2*c^2/(1-c^2)
         = 1 - r^2/(exp(r^2)-1).

The covariance is independent of the prescribed linear pin values. This does
not make it independent of a subsequent nonlinear selection or reweighting.

## 3. All-radius inequalities, without a grid or floating point

Put x=r^2. For 0<x<1, the absolutely convergent exponential series gives

    exp(x)-1-x >= x^2/2,
    exp(x)-1 <= sum_(n>=1) x^n = x/(1-x).

Both denominators are positive. Hence

    (exp(x)-1-x)/(x*(exp(x)-1)) >= (1-x)/2.

For the upper bound, expand the difference exactly:

    x*(exp(x)-1)/2 - (exp(x)-1-x)
      = sum_(n>=3) ((n-2)/(2*n!))*x^n >= 0.

The coefficients at degrees zero, one, and two vanish; every coefficient from
degree three onward is positive. Absolute convergence justifies subtraction
of the series. Division by x*(exp(x)-1)>0 proves the upper bound.
For 0<r<=R<1 the lower bound is at least (1-R^2)/2. At R=1/40 this is exactly
1599/3200. The singular radius zero is excluded, although the normalized
expression has limit 1/2 there. No finite list of radii is used in the proof.

## 4. What the executable certificate checks

`certificate.py` checks rational endpoint arithmetic, the exact declared
model/law/domain, and the formal-polynomial 2x2 inverse/quadratic-form identity.
Its coefficient function is checked at finitely many orders by the tests;
the all-order sign argument is the written argument in Section 3, not that loop.
The program is not an independent proof checker for Gaussian regression or
infinite series, and is not Lean/Coq/Isabelle kernel verification.

From the repository root:

    python3 -B -S certificates/bf_six_pin_scalar_20260926/certificate.py
    python3 -B -S certificates/bf_six_pin_scalar_20260926/certificate.py --check certificates/bf_six_pin_scalar_20260926/CERTIFICATE.json
    python3 -B -S -m unittest discover -s certificates/bf_six_pin_scalar_20260926 -p 'test_*.py' -v
    python3 -O -B -S -m unittest discover -s certificates/bf_six_pin_scalar_20260926 -p 'test_*.py' -v

The report remains REVIEW_REQUIRED. Looser valid intervals are allowed; a
narrower unproved lower/upper endpoint is refused. Widening the radius requires
recomputing the lower endpoint. Inputs are canonical rational strings.

## 5. Downstream boundary

This may supply one scalar ingredient after an exact scope match. It supplies
neither a full Schur covariance floor nor a determinant-moment estimate,
normalizer floor, all-angle periodization bound, weighted witness count,
collar estimate, or event-inclusion theorem. It does not close P0.1, D1, D5,
SARD-G, RN-UNIF or an elder-selection obligation. No 2D-to-3D composition follows.

The related author-side TS formula appears in Math- PR87 at
0fab9330c017e78eb9ef6d928e04aba9f376a470,
`incoming/grok-cycle4-20260926/harper/CLOSED_FORMS_FTS_FTT.md`.
This note rederives only TS from the stated kernel. It neither adopts nor
repairs the TT denominator paragraph, other packet claims, or their reviews.
No novelty or first-discovery claim is made.
