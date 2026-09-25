# Quantified finite-r six-pin remainder contract

**Object:** RN-FINITE-R-C6-REMAINDERS-20260925-v1  
**Author:** OpenAI, OA-FOLLOWTHROUGH-20260925.  
**Disposition:** author-side deterministic derivation; independent review pending.  
**Scientific effect:** NONE. This is a quantitative completion of the local interface in PR19, not a Gaussian count or persistence theorem.

## 1. Hypotheses and domain correction

Let `B >= 1`, `0 < r <= 1`. Let a real function `f = f_r` be C6 on an open neighbourhood of the **entire square**

    K_(B,r) = { (x,z): |x| <= B r, |z| <= B r }.

Assume, for one finite `M`,

    sup_(K_(B,r)) |partial_x^i partial_z^j f| <= M,
    for every i,j >= 0 with i+j <= 6.

For a family as r varies, a uniform conclusion requires the same M for all members. The square includes the midpoint, both pins, and all straight Taylor segments to the witness. Bounds solely on an annulus omitting the midpoint/pins are **not** this hypothesis. More generally one may use a common neighbourhood containing all those segments with the same derivative ceiling.

The six exact constraints are

    f(-r/2,0)=b,  f(r/2,0)=b-k r^3,
    f_x(-r/2,0)=f_x(r/2,0)=0,
    f_z(-r/2,0)=f_z(r/2,0)=0.

Here k may be any real number for the identities; positivity is needed only for later maximum/saddle and drift applications. Every derivative below is of the finite-r function at the actual midpoint. No derivative is replaced by its r=0 limiting law.

## 2. Explicit midpoint estimates

Under these hypotheses:

    |f_x + (r^2/8) f_xxx|              <= M r^4 / 384,             (M1)
    |f_xx + (r^2/24) f_xxxx|           <= M r^4 / 1920,            (M2)
    |f_xxx - 12 k|                    <= (3/80) M r^2,           (M3)
    |f(0)-b + (k/2) r^3|              <= (121/15360) M r^4,       (M4)
    |f_x/r^2 + 3 k/2|                 <= (7/960) M r^2,          (M5)
    |f_z + (r^2/8) f_xxz|             <= M r^4 / 384,             (M6)
    |f_xz + (r^2/24) f_xxxz|          <= M r^4 / 1920.            (M7)

These constants are explicit sufficient bounds; no optimality is claimed.

### Derivation

Set h=r/2 and g(t)=f(t,0). Expand g' at +/-h through cubic order with fourth-order remainder bounded by M h^4/24. Averaging the two zero values cancels the odd terms and gives

    |g'(0)+(h^2/2)g'''(0)| <= M h^4/24.

This is M1. Expanding g' through degree four with fifth-order remainder M h^5/120, subtracting and dividing by 2h gives

    |g''(0)+(h^2/6)g''''(0)| <= M h^4/120,

which is M2. C6 suffices for this fifth-order remainder of g'.

The value difference satisfies

    g(h)-g(-h)=2h g'(0)+(h^3/3)g'''(0)+E,
    |E| <= M h^5/60.

Insert M1 and the exact difference -8k h^3. Then

    |g'''(0)-12k|
       <= (3/(2h^3)) [2h(Mh^4/24)+Mh^5/60]
       = (3/20) M h^2 = (3/80) M r^2.

Combining this with M1 gives M5 because `3/640 + 1/384 = 7/960`.

The mean endpoint height is exactly `b-k r^3/2`. Taylor through cubic order gives

    (g(h)+g(-h))/2 = g(0)+(h^2/2)g''(0)+E0,
    |E0| <= M h^4/24.

By M2, `|g''(0)| <= M h^2/6+M h^4/120`. Therefore

    |g(0)-b+k r^3/2| <= M h^4(1/8+h^2/240)
                      <= (121/960) M h^4
                      = (121/15360) M r^4,

where h<=1/2 is used. Finally apply the same average/difference argument to `w(t)=f_z(t,0)`, whose derivatives through order five are bounded by M and whose values vanish at both pins. This proves M6 and M7.

## 3. Uniform scaled rows, including the height correction

Write

    a=f_zz(0),  q=f_xxz(0),  c=f_xzz(0),  d=f_zzz(0),
    P_x(u,v)=6k(u^2-1/4)+q u v+c v^2/2,
    P_z,ax(u)=q(u^2-1/4)/2,
    H(u,v)=k(2u^3-3u/2-1/2)+q(u^2-1/4)v/2+c u v^2/2+d v^3/6.

For every `|u|,|v|<=B`:

    | f_x(ru,rv)/r^2 - P_x(u,v) | <= M r C_x(B),               (S1)
    | f_z(ru,rv)/r - a v |         <= M r C_y(B),               (S2)
    | f_z(ru,0)/r^2 - P_z,ax(u) |  <= M r C_ax(B),              (S3)
    | [f(ru,rv)-b]/r^2 - a v^2/2 - r H(u,v) |
                                        <= M r^2 C_h(B),       (S4)

where

    C_x(B)  = 7/960 + 27B/320 + 3B^2/160 + 4B^3/3,
    C_y(B)  = 49/384 + 27B/640 + 2B^2,
    C_ax(B) = 1/384 + 27B/640 + B^3/6,
    C_h(B)  = 121/15360 + 19B/1920 + 81B^2/1280 + B^3/160 + 2B^4/3.

### Derivation of S1-S4

The multivariate Taylor remainder after degree m-1 is bounded by

    M (|x|+|z|)^m / m!,

when the relevant order-m partials satisfy the ceiling on the entire segment. This follows by applying the one-variable Taylor formula to `t -> f(tx,tz)` (or a derivative of f) and the binomial theorem.

M2/M7 imply `|f_xx(0)|,|f_xz(0)| <= (27/640) M r^2` for r<=1. For S1, expand f_x to degree two; use M5 for the midpoint drift, M3 for the cubic longitudinal coefficient, and that bound for the two linear coefficients. Its third-order Taylor remainder divided by r^2 is at most `M r (2B)^3/6`. The displayed C_x is the sum of those bounds, using r^2<=r.

For S2, expand f_z only to degree one. M6 bounds `|f_z(0)|/r` by `(49/384) M r`; M7 bounds the x-linear term by `(27B/640) M r`; the remainder contributes `2 M r B^2`.

For S3, expand f_z along the x-axis to degree two. Retain M6's term `-q/8` after division by r^2. M6/M7 and the third-order remainder give respectively `1/384`, `27B/640`, and `B^3/6`.

For S4, expand f through total degree three. Retain the midpoint height offset from M4, the longitudinal drift from M5, and the transverse midpoint offset from M6. The remaining midpoint quadratic x/mixed terms are O(Mr^2) after division by r^2, with coefficient `81B^2/1280`. The error in f_xxx contributes `M r^3 B^3/160`, and the fourth-order Taylor remainder contributes `(2/3) M r^2 B^4`. Adding M4, the x/z midpoint-error terms, and these bounds gives C_h.

The leading terms lost by taking U_r -> U_0 too early are thus controlled explicitly, rather than absorbed in an unspecified remainder.

## 4. A useful rate boundary

The pin-preserving perturbation `(x^2-r^2/4)^2` has zero value and gradient at both pins. Its contribution to `f_x(ru,0)/r^2` is

    4 r u(u^2-1/4).

At u=2 this equals 30r. Thus the S1 error cannot generally be strengthened from O(r) to O(r^2) merely by assuming C6 bounds. This identifies the first residual order without claiming any conditional Gaussian covariance or density estimate.

## 5. Evidence and limits

`test_c6_remainder_contract.py` constructs polynomials by solving a six-by-six rational system for the pinned coefficients of `1,x,x^2,x^3,z,xz`. All 22 other monomials of total degree at most six are exercised separately, at three positive radii, with values and derivatives evaluated independently of `finite_r_contact.py`. The tests check M1-M7, S1-S4, exact cubic compatibility and genuine endpoint types. The maximum of coefficient-sum derivative bounds supplies a rigorous M for each polynomial fixture.

This finite oracle checks the algebra and the stated sufficient constants on its declared fixtures. It is NOT a proof over all C6 functions; the Taylor argument above supplies the author-side analytic derivation and still requires an independent reviewer. It is NOT a random-field simulation, an interval-r Gaussian certificate, or a proof of uniform conditional C6 moments.

In a Gaussian application M is normally random. Using these pathwise inequalities inside a weighted Kac-Rice integral requires the relevant **conditional** moments after all pins; no deterministic M may be silently substituted. The fixed thin-tube/annulus, Gaussian density, height-density rank and typed Hessian estimates remain separate obligations. No controlling status is changed here.

## 6. External context

NIST DLMF 3.3(iii)-(iv), https://dlmf.nist.gov/3.3, describes divided differences and confluent nodes, including derivative/factorial limits at coincident nodes. It is background for why finite-node identities must be retained; it does not supply the specific six-pin constants or validate the Gaussian application. The constants and domain contract in this note are derived explicitly above. No novelty claim is made for Taylor's theorem or Hermite interpolation.
