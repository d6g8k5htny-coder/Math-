# Conditional moments, quantiles, and coefficient bounds for the radial ratio

Read-only nonauthor consequence review of Math- PR #176 equation (17), exact head
`71772a8906cf6663d16be2cd5f63e5d4ebdcee2b`, proof blob
`65f24b1f9a7b80522a2ee059f5f6877c9f970f0d`, 15,755 bytes, SHA-256
`a3693664900e23e1e763d88a0b5609936a6f31d844cbe6f18c7d0379b94ba710`.

This is an elementary conditional implication, not a second Slice B verdict.
Claude's Slice A and the competing actual Slice B reviewer retain their scopes.
The reviewer here authored none of this packet or its mathematical sources;
all are OpenAI-source-exposed, and organizational-independence credit is zero.
R17 claim: `13dc84b1-bc12-42df-8c7f-96f23cb1dd7d`, WE317; root coordinates
the actual public disposition. No proof branch or scientific status was changed.

Exposure chronology: the second-order power/log derivations and their first
seven exact arithmetic controls were completed before this reviewer read
author comment [5907459466](https://github.com/d6g8k5htny-coder/Math-/pull/176#issuecomment-5907459466),
posted at 2026-09-30T08:38:26Z. That comment already states these power/log and
fixed-alpha quantile formulas. They are credited to the author's offered
corollaries here; no novelty or source-unexposed credit is claimed. The quantile
analysis below was made after that exposure. The all-order extension was
suggested by root, then reconstructed here using tail integration. Author
comment [5903080058](https://github.com/d6g8k5htny-coder/Math-/pull/176#issuecomment-5903080058)
was read before analysis of its coefficient inequalities.

## Consumed hypothesis and scope

Write Q_t=R/t under the source's point-intensity sampling conditional on R>t,
after the original r limit has already formed its microscopic point measure.
Retain the source's full normalizer; no cluster-maximum selection or extra
factor for multiplicity is introduced. Let c=C_2/C_0, with C_0>0. Consume (17)
in its quantified form: for each fixed source model there are T,K<infinity
such that, for every t>=T and q>=1,

    S_t(q)=P(Q_t>q)
          =q^-11[1+c t^-2(q^-2-1)]+E_t(q),
    |E_t(q)| <= K t^-4 q^-11.                         (M1)

This pointwise remainder, uniform over the unbounded q range, is essential.
Unweighted L1 or total-variation convergence alone would not justify integrating
the unbounded test function Q_t^p or log Q_t. The original source's positive
tail asymptotic also supplies F(x)~C_0 x^-11 as x tends to infinity.

## Every fixed real power below eleven

For every fixed real p<11,

    E Q_t^p = 11/(11-p)
              - [2p c/((13-p)(11-p))] t^-2 + O_p(t^-4). (M2)

For p=0, this means the exact identity E Q_t^0=1 and a zero correction.
For p!=0, the deterministic identity for x>=1 is

    x^p = 1 + p integral_1^x q^(p-1)dq.

For 0<p<11, Tonelli applies to the nonnegative integrand. The tail bound (M1)
makes the resulting integral finite. For p<0, absolute Fubini applies since

    |p| integral_1^infinity q^(p-1) S_t(q)dq
       <= |p| integral_1^infinity q^(p-1)dq = 1.

Thus the SAME identity holds for negative p, with its signed factor p:

    E Q_t^p = 1+p integral_1^infinity q^(p-1) S_t(q)dq.

Inserting (M1) gives the leading coefficient
`1+p/(11-p)=11/(11-p)` and the correction

    pc[1/(13-p)-1/(11-p)] = -2pc/((13-p)(11-p)).

The remainder has the explicit bound

    |p| integral_1^infinity q^(p-1)|E_t(q)|dq
        <= |p|K/(11-p) t^-4.                           (M3)

This proves the assertion for arbitrary fixed real p, not merely the rational
powers used in finite checks. Constants can blow up as p approaches 11. A
uniform bound over all p<11 does not follow and is false for a simple exact
Pareto mixture in the companion checks. Uniformity on a fixed compact subset
of (-infinity,11) does follow from (M3), but is not needed for (M2).

Useful exact cases are

    E Q_t^-1 = 11/12 + (c/84)t^-2 + O(t^-4),
    E Q_t    = 11/10 - (c/60)t^-2 + O(t^-4),
    E Q_t^2  = 11/9  - (4c/99)t^-2 + O(t^-4).

At the separately reviewed aligned planar scope where c>0, the leading
correction is negative for positive p and positive for negative p. These are
asymptotic statements at each fixed model, not uniform finite-threshold bounds.

## The divergence boundary

For any finite t>0 for which this conditional law is defined, and every p>=11,
`E Q_t^p=infinity`. Indeed,

    S_t(q)=F(tq)/F(t) ~ [C_0 t^-11/F(t)] q^-11,

and its positive leading coefficient yields a lower bound by a positive
multiple of q^-11 for all sufficiently large q. The positive-power tail
integral diverges at p=11 logarithmically and at every p>11 as a power.
No limit interchange at p=11 and no claim about the original finite-r field
is involved. The finite capped eleventh moment in #176 is a different object.

## Logarithmic moment

Since log x=integral_1^x q^-1dq for x>=1, direct Tonelli integration gives

    E log Q_t = 1/11 - (2c/143)t^-2 + O(t^-4).           (M4)

The first integral is `1/11`; the correction is
`c(1/13-1/11)=-2c/143`. The absolute remainder is at most `K t^-4/11`.
This derivation does NOT differentiate (M2) with respect to p or assume any
unstated differentiable uniformity in the p-indexed remainder.

## Conditional all-order extension

Consume in addition the finite-order remainder in equation (5), obtained from
the smooth even scalar C in Theorem 1. Let alpha_j=11+2j and D(t)=C(1/t)>0.
For every fixed nonnegative integer N and every t>=T, q>=1,

    t^11 F(tq) = sum_(j=0)^N C_(2j) t^(-2j) q^(-alpha_j)
                 + R_(N,t)(q),
    |R_(N,t)(q)| <= K_N t^(-2N-2) q^(-13-2N).          (M5)

The scalar bound at s=tq provides this uniform remainder directly; no derivative
of a rough O term is taken. For every fixed real p<11, tail integration gives

    E Q_t^p = [sum_(j=0)^N alpha_j/(alpha_j-p)
                              C_(2j)t^(-2j)
                  + O_(p,N)(t^(-2N-2))] / C(1/t).     (M6)

To see the normalization explicitly, multiply the exact tail identity for
E Q_t^p by D(t). Its right side is D(t) plus p times the integral of (M5)
against q^(p-1). Expand D(t) at the same finite order and use
`1+p/(alpha_j-p)=alpha_j/(alpha_j-p)`. The remainder in this numerator is
bounded by `K_N[1+|p|/(13+2N-p)]t^(-2N-2)`. The p=0 moment is exactly one.
Keeping the denominator exact avoids a hidden normalization change. Replacing
it by `sum_(j=0)^N C_(2j)t^(-2j)+O_N(t^(-2N-2))` is equivalent.

For every fixed integer m>=1, direct nonnegative tail integration similarly gives

    E (log Q_t)^m = [m! sum_(j=0)^N C_(2j)t^(-2j)/(11+2j)^m
                         + O_(m,N)(t^(-2N-2))] / C(1/t). (M7)

Indeed, use `m integral_1^infinity (log q)^(m-1)S_t(q)dq/q` and substitute
y=log q. Each integral is m!/alpha_j^m. The numerator remainder is at most
`m! K_N/(13+2N)^m t^(-2N-2)`. These are finite-order expansions for fixed
indices, with no claim of convergence of an infinite Taylor series.

## Fixed upper-tail quantiles

Let 0<alpha<1 be fixed. The exact scalar representation gives

    S_delta(q)=q^-11 C(delta/q)/C(delta), delta=1/t.

It is smooth and even in delta near zero for q near q0=alpha^(-1/11)>1,
and its q derivative at (0,q0) is -11 q0^-12, which is nonzero. The implicit
function theorem therefore gives a smooth even local solution q_alpha(delta).
For sufficiently large t, the separately supplied differentiated expansion
`-F'(s)=11C_0 s^-12+O(s^-14)` makes F strictly decreasing for every s>=t.
Together with S_t(1)=1 and S_t(q)->0, this identifies the local solution as
the unique upper-tail quantile of the conditional law.

Put q=q0(1+a delta^2). Substitution in (17) gives

    S_delta(q)=alpha[1+(-11a+c(q0^-2-1))delta^2]+O_alpha(delta^4).

Consequently

    Q_alpha(t)=alpha^(-1/11)[1+(c/11)(alpha^(2/11)-1)t^-2
                               + O_alpha(t^-4)].      (M8)

The author's quantile formula is correct under these source inputs. Strict
density at sufficiently large radii supplies uniqueness; an unquantified
pointwise distributional limit alone would not supply the error term. At
the aligned planar scope c>0 makes the displayed correction strictly negative.
The eventual approach from below is for each fixed alpha and fixed model;
no uniform claim as alpha tends to an endpoint, or over L,k,b, is needed.

## Scope of the signed-law coefficient bound

Let rho have probability density proportional to H gamma^11 G0 in lambda.
The positive finite normalizer is supplied by C_0 and the source Gaussian
majorant. Equations (13) and (19), with the constants in (12), yield exactly

    B_sign = (11 U_abs/(2I)) E_rho[|A|/sqrt(1+A^2)].

At every finite A, the integrand lies in [0,1). Positivity of G0 on the
nondegenerate Gaussian support gives positive rho mass at a!=0, so its mean
is strictly positive. Its mean is strictly below one because 1 minus the
integrand is a strictly positive measurable function under a probability law.
Thus, throughout the fixed dimension/frame scope of sections 1--5,

    0 < B_sign < 11 U_abs/(2I) = 4587821/876544.        (M9)

This bound does not use a sign of D_a G0 and does not require the aligned
planar factorization of section 7. The author's comment 5903080058 states the
bound after an aligned-planar discussion using the word "Likewise"; (M9)
makes its valid broader scope explicit. By contrast, the offered strict bound
`c>11U_2/(2I)=4587/856` does use section 7's D_a G0<=0, with B<0. In that
case the first geometric integrand ratio `(1+12A^2)/(1+A^2)` is >1 whenever
a!=0, which proves strictness already from the positive Gaussian mass.
Neither coefficient inequality supplies a parameter-uniform remainder.

## Source and verification boundary

`SOURCES.json` is the exact source map from #176. The cached `R.md`, `SC.md`,
and `P.md` were each checked against its declared size, SHA-256 and Git blob.
R and P reused matching local source bytes; SC was fetched at its explicit
historical commit/path. No author program was used for the calculations.

`moment_consequence_checks.py` independently compares tail- and density-based
rational integrals, fixed hand-derived cases, the divergence threshold and log
coefficient. A genuine mixture of Pareto(11), Pareto(13), Pareto(15) validates
the quantitative remainder bound and supplies the nonuniform-in-p counterexample.
Wrong normalization, sign, omitted p, and missing factor-two controls are rejected.
Additional exact mixture checks compare the all-order normalized numerator
against direct component moments. Log-power integrals, quantile coefficients,
and the two rational coefficient factors are checked separately.
These finite checks support arithmetic only; they do not replace (M1), its
Gaussian assumptions, or the pending source-bound A/B analytic reviews.

Preliminary reading of #176 §§4–7 found no blocking error before coordination
redirected this reviewer; that preliminary observation is not a completed B
verdict. The results here are conditional corollary validation (M2)--(M9) and
the positive-tail divergence implication, not acceptance of the consumed
Gaussian theorem or the full PR. Scientific effect: NONE.
