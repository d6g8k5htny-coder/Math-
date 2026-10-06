# LM006 coefficient: a finer outward rectangle enclosure

Dylan Roy — delegated AI mathematical/numerical work. Actual author OpenAI /
GPT-6 Astra Pro, `r22-enclosure-refinement-and-queue-audit-20261006`.
Scientific effect NONE; organizational-independence credit 0.

## 1. Exact claim and relationship to the reviewed predecessor

For the exact coefficient defined by Math-#358 and enclosed in Math-#362,
this separate computation gives the inclusive interval

    0.001313658238 <= C_(24,6/5) <= 0.001330377065.            (1)

The object remains the original-axis, d=2, L=24 normalized-periodized Gaussian
field at birth b=6/5 with the same six pins and gap r^3/6. Its determinant-tilted
saddle-transverse sign probability has leading coefficient C. This computation
neither reproves that asymptotic nor supplies a finite-r remainder or radius.
In particular (1) is NOT a bound on a probability obtained just by multiplying
its endpoints by r^3.

The predecessor's five files at commit
`1f64b8f8ee450262e0f56e6bdf9dfb37931f48c6` are unchanged. Its source directory is
`coefficients/lm006_wrong_sign_20261006_r20/`. We consume its NOTE's coefficient,
cell-extremum, tail and outward-arithmetic arguments, and execute its exact
`enclose.py` primitives after authentication:

    Git blob e680ddb7aa0abd4b6aab2cac6a54c1ff28efc782
    bytes 7215
    SHA256 157e02ee22699b4fa2efdde1894824b92b962900dbb8da9bd65acee41ae91e88.

The predecessor's complete NOTE is blob a79f080851bba69a03ec4b8348dc93d04143bf62,
SHA256 1a145132e05aa2721397d30fd3c422bbaab496ac8c24b947e416a3f4e0e0a526.
Its numerical review is #362 comment6015313010. That review does not review
THIS new driver or output. An actual new scoped review is required.

The previous saved 2048-grid interval is
[0.001305365507,0.001338803452]. Interval (1) lies strictly inside it. The
old/new widths, as displayed exact decimals, have ratio
33437945/16718827, slightly greater than two. Grid agreement or nesting is
not the proof: each enclosure follows its own cell bounds and included tails.
The actual #358 proof and its pinned model definitions remain the source of the
coefficient; no generic numerical method or mathematical novelty is claimed.

## 2. The same integral, scaling and unbounded tails

Use the source's raw torus moments m2,m4, delta=m4-m2^2, v=m2*delta. Under the
UNTILTED Gaussian input law used to compute the coefficient, D and B are
independent centered Gaussians of variance v and v/4, respectively. Let

    J(d,u) = integral_0^(d_+) (d-u-t)_+ (u-t)_+ dt, u>=0,
    Gamma = E J(D,B^2),
    C = p0 Gamma/z0,
    Q ~ N(-m2*(6/5),delta), z0=E(Q_-)^2>0, p0=density_Q(0).

The probability whose coefficient is C is determinant-tilted; independence is
not asserted under that tilted probability law. The full z0 is not conditioned
on the sign event. B's variance is v/4, not v.

For d>u>0, set ell=min(u,d-u), M=max(u,d-u). Then
J=ell^2(3M-ell)/6, and it is zero if u=0 or d<=u. At fixed u, J is
nondecreasing in d; at fixed d, its maximum is at u=d/2 and it increases then
decreases. The predecessor proves, for each rectangle in (d,u),

    lower = min(J(d0,u0), J(d0,u1)),
    upper = J(d1, clamp(d1/2,u0,u1)).                        (2)

Retain R=12, T=4, and the symmetry factor two when B is integrated on [0,T].
The imported `parameters()` returns the same periodic moment intervals, z0 and
p0 intervals, with the image error enclosed, not discarded. The same `density`
function uses outward integer/Fraction exponential, square-root and pi bounds,
with fixed scale S=10^36. All certified values are rational; this new driver
uses no floating quadrature, Monte Carlo or transcendental library.

The complement of [0,R] x [-T,T] is covered by the same union bound from
J(D,B^2)<=D_+^3/24. Its two contributions are

    tail_D <= (v_hi R^2+2 v_hi^2) upper_density_D(R)/24,
    tail_B <= [2 v_hi^2 upper_density_D(0)/24]
                     [v_hi/(2T) upper_density_B(T)].         (3)

Their sum is ADDED to upper Gamma, not lower Gamma. These expressions use
untilted input independence only. They bound the true tails uniformly over the
same variance box as the predecessor. Their outward decimal sum is unchanged:

    tail_Gamma <= 0.000000001492544918.

The coefficient endpoints multiply the corresponding p0 bound and divide by
the OPPOSITE strictly positive z0 bound. No parameter interval is tightened by
this new execution, so the density/normalizer enclosures remain

    p0 in [0.196810857928,0.196810857929],
    z0 in [3.230978535287,3.230978535288].

## 3. Exact larger-grid formula and zero-cell pruning

The parent's public `enclosure` function deliberately refuses n>2048. That
function and guard are NOT edited or bypassed. This separate `refinement`
implements the same proven sum for 2<=n<=8192; default and certified saved
execution here are n=4096. It imports only the unchanged authenticated module
and calls its parameter, density, integer cubic and rounding functions.

For cell indices i,k in {0,...,n-1}, take d_i=Ri/n, b_k=Tk/n and u_k=b_k^2.
With common coordinate denominator q=2n^2, use the exact integers

    D0=2R i n, D1=2R(i+1)n,
    U0=2T^2 k^2, U1=2T^2(k+1)^2.

The integer function `_jnum(D,U)` is exactly 6q^3 J(D/q,U/q). D1 is even,
so D1//2 is its exact stationary coordinate, not an approximate midpoint.
Let dl,du,bl,bu be the parent's density endpoints multiplied by S (integers).
The lower and upper rectangle sums are, respectively,

    [2RT/(n^2 * 6q^3 * S^2)]
      * sum min(_jnum(D0,U0),_jnum(D0,U1)) dl[i+1] bl[k+1],

    [2RT/(n^2 * 6q^3 * S^2)]
      * sum _jnum(D1,clamp(D1/2,U0,U1)) du[i] bu[k].         (4)

These are precisely (2) times the outward density bounds and the cell area,
including B symmetry. Finite summation preserves both interval directions for
EVERY allowed n; the formula is not justified by extrapolation from n=2048.

The only pruning is exact. If U0>=D1, then for every point of that cell u>=d,
so J(d,u)=0. The unpruned lower and upper terms are both identically zero.
Conversely U0<D1 yields a strictly positive upper maximum: U1>U0 and D1>0.
For these fixed R,T, active indices satisfy

    32 k^2 < 24(i+1)n.

Thus the first omitted index is exactly

    min(n, 1+isqrt(floor((24(i+1)n-1)/32))).                 (5)

The subtraction by one handles equality as the zero side; no positive cell is
removed. Pruning makes (4) algebraically IDENTICAL to the complete rectangle
sum, not an approximation needing another tail estimate. The unbounded tails
in (3) are still included unchanged.

At n=4096 the full grid has 16,777,216 cells. Exactly 9,690,026 are evaluated
and 7,087,190 have zero upper contribution. The certified output is

    Gamma in [0.021565891306,0.021840358727],
    C in the inclusive interval (1).

The width remains primarily a discretization enclosure; no claim of optimal
error, rate, or rounding constant is made.

## 4. Source authentication and actual test coverage

Before executing the parent, `load_source` opens its expected file as a regular
file (rejecting a symlink leaf), verifies its exact size and SHA256, then compiles
THOSE same verified bytes. It does not reread a possibly changed file through
the import loader. The production command has no source-override option.
The module is cached within one process; no assertion that its on-disk source
cannot later change is made. This is trusted-source identity, not an arbitrary
code sandbox, operating-system permission audit or hostile-ancestor-path defense.
The provided executable loader is POSIX-oriented, as are its symlink tests.

Nine test methods first produced nine intended missing-implementation assertion
failures, zero errors, in each Python mode. The completed suite checks:

- exact rational equality to the UNCHANGED parent at n=2,3,5,8,16,32, including
  Gamma, coefficient, tail and every parameter interval;
- zero-cell classification, including exact U0=D1, on five grids;
- an independently assembled, UNPRUNED 64-cell Fraction-coordinate sum using
  `cell_bounds` and the separate density functions rather than integer `_jnum`;
- interior stationary maxima, positive upper tails, opposite-denominator
  division, invalid grid types/bounds, intact original cap and saved result;
- altered-source non-execution, symlink rejection, real child CLI outcomes and
  normal/optimized output identity.

Five isolated wrong-driver variants are tested with the same full suite in both
modes: omit symmetry2; omit upper tail; exclude a positive boundary cell; replace
the interior maximum by the left corner; divide the upper coefficient by the
upper z0 endpoint. They produce 7,7,8,7,7 intended assertion failures per mode,
respectively, with zero test errors. The variants are retained as author-side
evidence, not committed production source. These probes are not a new field
simulation, a proof of all possible execution failures, or a Lean theorem.

## 5. Completed execution and limitations

On the author's Linux CPython3.13.5, both completed n=4096 runs exit zero with
empty stderr and identical 755-byte JSON. That output is stored unchanged as
RESULTS.json (SHA256 4d1c1703601a0faaf7d2dc2920454b8cf77ebd0cf8593d4e5f55bd3658e88201).
Its `independently_reviewed=false` is immutable author-run history, not a field
for automatic promotion when a later review arrives.

Two attempted n=8192 executions (one per Python mode) ended at an OUTER tool
deadline without a completed process receipt or result. They are excluded from
all successful-run counts. The supported upper input bound is not evidence
that n=8192 completed. An unavailable streaming transport and a subsequent
missing-runner attempt also produced no numerical execution. These limitations
are retained in the delivery chronology; no code/budget was weakened to call
a partial result successful. The published default is the completed4096 case.

Reproduce from this directory, with the exact five-file predecessor directory
present next to it:

    python -B -S test_refinement.py
    python -B -O -S test_refinement.py
    python -B -S refine.py --grid 4096
    python -B -O -S refine.py --grid 4096

No existing CI workflow is changed. The new result is NOT automatically run by
the general core-formal job or #366's dedicated 2048 execution. This note and
new driver require their own source-bound review and, before integration, all
applicable current-candidate checks. #362 and #366 keep their separate owners;
this numerical refinement is not a condition delaying their integration.
No full local repository checkout, local Lean, fresh historical archive census,
finite-r probability/radius, arbitrary orientation/mark/model, independent
formal alignment, or full-field capture/elder/persistence result is asserted.
