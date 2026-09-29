# C7 zero-gap limit: a positive coefficient and the rejected-pair intensity law

Object: **OA-C7-ZERO-GAP-LIMIT-20260929-v1**.
Author: **OpenAI / GPT-6 Astra Pro**, foreground session, 29 September 2026.
Disposition: **AUTHOR-SIDE ANALYTIC CANDIDATE; non-OpenAI review required**.
Scientific effect: **NONE**. No existing theorem, review disposition, register,
graph, claim, prize, premise or lemma flag is changed. No self-merge.

## 1. Model, exact convention, and results

Fix an integer d >= 2 and L > 0. Work on the flat torus T_L^d with the same
variance-one periodized Gaussian covariance as the lifetime parent P:

    K_L(x) = [sum_(n in Z^d) exp(-|x+Ln|^2/2)] /
             [sum_(n in Z^d) exp(-|Ln|^2/2)].

P means UNIFORM_MATRIX_CAP_AND_LIFETIME.md with its complete retained reading
rule (CAP, congruence erratum E1, marked-measure repair E2, reconciliation E3).
K means Claude's gap-mark-explicit Theorem K, proof Git blob
`28748b086ec6761ef467dc67cba475fbdf8b7455`, from Math-#150. SOURCES.json binds
these inputs. We consume K1/K2, not its unused normalized-form remark, and do
not re-review P or K here. We do not require Theorem U's positive lower bound.

Count all ORDERED maximum/index-(d-1)-saddle pairs. The index counts negative
Hessian eigenvalues. Birth b is the value at the maximum, not the midpoint of
the two heights. The positive gap is ell=f(M)-f(S). Every density and expected
count below is PER UNIT SPATIAL VOLUME. Only finite ordinary superlevel H0
bars are selected; an essential maximum has elder mark zero for every saddle.

For y != 0 on the torus let

    O_y = (f(0), grad f(0), f(y), grad f(y)),
    v_(b,ell) = (b, 0_d, b-ell, 0_d),
    p_y(v) = the Gaussian density of O_y at v,
    Q_(y,b,ell) = its continuous full-field Gaussian regression law,
    W(f) = |det H_0 det H_y| 1{H_0<0, index(H_y)=d-1}.

For ell>0, write e_y(f) for the parent's Borel ordinary elder-partner mark and
set

    Psi_ell(b,y) = p_y(v_(b,ell)) E_Q[W(f)(1-e_y(f))].       (Z1)

At zero define a different-looking, UNMARKED equal-height kernel:

    Psi_0(b,y) = p_y(v_(b,0)) E_(Q_(y,b,0))[W(f)].           (Z2)

The pins at equal critical heights specify a Gaussian regression kernel, not
a positive-probability conditioning event or a population of actual zero bars.
Define

    B_(d,L) = integral_(T_L^d \ {0}) integral_R
                    Psi_0(b,y) db dy.                     (Z3)

**Theorem Z (candidate).** The integral (Z3) satisfies 0<B_(d,L)<infinity. For
the canonical marked Kac-Rice density versions from P with E2,

    rho_rej(ell) := nu_cand^all(ell)-nu_eld^all(ell)
                  -> B_(d,L) as ell decreases to zero.      (Z4)

More strongly, for every fixed real p>=0,

    integral (1+|b|)^p |Psi_ell(b,y)-Psi_0(b,y)| db dy
                  -> 0.                                   (Z5)

Thus the normalized birth/displacement law obtained by sampling the REJECTED
INTENSITY at gap ell converges in total variation to

    Psi_0(b,y) db dy / B_(d,L).                             (Z6)

This limit has positive density at every (b,y) with y!=0. For 0<delta<r_0,
the rejected intensity at distance below delta is <=C delta, uniformly over
small positive gaps; the limit has no diagonal atom.

**Corollaries.** Write c=c_(d,L)>0 for P's common leading coefficient.

    expected rejected count with gap in (0,t] = B_(d,L)t+o(t),
    integral_0^t ell^q rho_rej(ell) d ell
          ~ B_(d,L)t^(q+1)/(q+1),             q>-1,         (Z7)
    rho_rej(ell)/nu_cand^all(ell)
          ~ [B_(d,L)/c] ell^(1/3),                         (Z8)
    [integral_0^t rho_rej]/[integral_0^t nu_cand^all]
          ~ [2B_(d,L)/(3c)] t^(1/3).                       (Z9)

The rejected inverse-moment boundary is exactly q=-1, with coefficient
B_(d,L) in the logarithmic divergence. The ratios (Z8)-(Z9) concern normalized
ANNEALED INTENSITIES; they are not fixed-radius Palm probabilities, not an
expectation of a samplewise ratio, and not uniformly sampled fields followed
by uniformly sampled pairs. Those are different sampling procedures.

No numerical value for B_(d,L), no error rate in (Z4)-(Z6), and no next-order
expansion of either individual density is asserted.

## 2. Nondegenerate two-site jets and continuous Gaussian coupling

The covariance has strictly positive Fourier coefficients at every lattice
frequency. The full two-site jet list through order two is nondegenerate for
y!=0, by P Section 2's argument: a zero-variance linear combination would be a
finite linear combination T of derivatives of point masses at 0 and y with
all Fourier coefficients zero. Trigonometric polynomials approximate smooth
test functions in their C^2 norm, so the distribution T would vanish. Smooth
functions with arbitrary jets supported in disjoint neighborhoods of the two
sites then force every coefficient of T to be zero. Consequently the full
jet covariance is positive definite, as is the conditional covariance of the
two Hessians given O_y. It has an everywhere positive finite-dimensional
Gaussian density. Singular endpoint Hessians have conditional probability zero.

For fixed y!=0 and b, the covariance of Q_(y,b,ell) does not depend on ell or b.
Using one common centered residual field, Gaussian regression yields the
coupling

    f_ell = f_0 + ell h_y,                                 (Z10)

where f_0 has law Q_(y,b,0) and h_y is a deterministic smooth regression
function. It has h_y(0)=0, h_y(y)=-1 and zero gradient at both sites. Thus all
f_ell have exactly the required pins, and f_ell -> f_0 in C^2 on the torus.
This is only a FIXED-SEPARATION assertion; no bound on h_y as y approaches the
diagonal is assumed. The covariance is not assumed rotationally invariant.

## 3. The local barrier makes every fixed-separation limit rejected

We first record the deterministic point that replaces any supposed global
continuity of the elder selector.

**Local barrier lemma.** Suppose g_j -> g in C^2, grad g_j(M)=0, g_j(M)=b,
and H_g(M)<0. Fix S!=M. There exist a ball B_R(M) disjoint from S and a
constant delta>0 such that, for every sufficiently large j, g_j<b in the
punctured ball and g_j<=b-delta on its boundary. If additionally
0<g_j(M)-g_j(S)<delta, S is not the ordinary elder death partner of M.

**Proof.** Choose an embedded Euclidean ball with R<dist(M,S)/2 and a>0 such
that H_g<=-aI throughout its closure. C^2 convergence gives H_(g_j)<=-aI/2
there for large j. Taylor's integral formula along straight segments, using
the EXACT zero gradient at M, gives

    g_j(x) <= b-(a/4)|x-M|^2.

Take delta=aR^2/4. In particular there is no point higher than b inside the
ball. Every path from M to a point with value higher than b must cross the
boundary, so its minimum is <=b-delta. Therefore the maximin elder-death level
satisfies d_(g_j)(M)<=b-delta<g_j(S). If there is no older point, d=-infinity
and the conclusion is the same. This excludes the elder mark. The stronger
concavity assertion, not merely a low boundary, prevents an older maximum
inside the ball from invalidating the path argument. QED.

Apply this lemma pathwise to (Z10) on {W(f_0)>0}. A ball and delta may depend
on the realization, b and y, but each delta is positive. For all sufficiently
small ell, the mark e_y(f_ell)=0. On the complementary type configurations,
W(f_ell)->0 because the limiting endpoint Hessians are nonsingular almost
surely. Hence in all cases outside a conditional null set,

    W(f_ell)(1-e_y(f_ell)) -> W(f_0).                       (Z11)

There is no assumption that the ordinary elder selector is continuous, that
f_0 has distinct critical values, that a saddle has a particular ascending
trajectory, or that a Morse-Smale property survives the coupling. Its forced
equal critical heights cause no problem for the local concavity argument.

For fixed y,b and 0<=ell<=1, the endpoint Hessians in (Z10) differ by a bounded
deterministic matrix. Their determinant product is dominated by a polynomial
of degree 2d in the norm of the finite Gaussian endpoint Hessian vector under
Q_(y,b,0). This is integrable. Conditional dominated convergence and the
continuity of p_y(v_(b,ell)) give

    Psi_ell(b,y) -> Psi_0(b,y)   for every y!=0 and b in R.  (Z12)

The role of Section 4 is to make this limit integrable even as y approaches
zero. Fixed-separation continuity alone would not justify that step.

## 4. Uniform integrable domination: the two gap-mark regimes

Take P's target-independent r_0 below one and the torus injectivity scale.
For y=ru with 0<r<=r_0, use P's birth convention and put k=ell/r^3. Translation
from centered pins M=-ru/2, S=ru/2 to 0,y preserves their law. Let pi_r(v_r)
be the transformed pin density in P (10.1), and set

    A_r^rej = 12 pi_r(v_r) E_Q[(W_r/r^2)(1-e)].             (Z13)

The original pin density is 12r^(-(d+3))pi_r(v_r). Multiplication by the spatial
polar factor r^(d-1) and the determinant normalization r^2 gives EXACTLY

    r^(d-1) Psi_ell(b,ru) = r^(-2) A_r^rej,
    rho_rej^near(ell) = integral r^(-2) A_r^rej
                                        dr db d sigma(u). (Z14)

Equivalently, transform P's lifetime integral
(1/3)ell^(-1/3)k^(-2/3) A_r^rej dk using k=ell/r^3 and
|dk/dr|=3ell/r^4. The ell powers cancel and the remaining power is r^-2.
The sphere measure sigma is ordinary area, not normalized probability.
The height map (b,ell)->(b,b-ell) has absolute determinant one. There is no
factor 1/2 for ordered critical types and no extra torus-volume multiplier.

The input K gives fixed C,N such that, for every b, k>0 and r<=r_0,

    E_Q[W_r/r^2] <= C(k+r)^2(1+|b|+k)^N,                  (K1)
    E_Q[(W_r/r^2)1_(G_r^c)]
          <= C(r^3/k)(1+|b|+k)^N,   provided r<=k.         (K2)

The parent cap theorem supplies 1-e<=1_(G_r^c) on the generic locus, and its
repaired Borel marked-measure formula legitimizes that bound under Kac-Rice.
P (13.2) gives pi_r(v_r)<=C exp[-c(b^2+k^2)] uniformly over these unrestricted
targets and all frames. Now separate two cases:

* If r<=k, use K2. The right side of (Z14) is at most
  C(r/k)(1+|b|+k)^N exp[-c(b^2+k^2)]. Here r/k<=1.
* If k<r, use K1 and 1-e<=1. The same quantity is at most
  C(1+k/r)^2(1+|b|+k)^N exp[-c(b^2+k^2)]. Here (1+k/r)^2<=4.

Absorbing the polynomial into slightly weaker Gaussian tails therefore yields

    0<=r^(d-1) Psi_ell(b,ru)<=C exp(-c' b^2)               (Z15)

for every 0<r<=r_0 and every ell>0. The K2 bound was NOT used at k<r, the
(k+r)^2 factor was NOT discarded, and no lower floor for Z_r or globally
uniform compact-mark selection probability was introduced.

On the remaining compact displacement set dist(0,y)>=r_0, P Section 14's
nonsingular full-pin covariance bounds give, for 0<ell<=1,

    0<=Psi_ell(b,y)<=C(1+|b|)^(2d) exp(-c b^2)
                   <=C' exp(-c'' b^2).                    (Z16)

Combining (Z15)-(Z16) produces an integrable majorant on db dy:

    D(b,y)=C exp(-c_* b^2)
           [1{0<dist(0,y)<r_0} dist(0,y)^(1-d)
                                      +1{dist(0,y)>=r_0}]. (Z17)

In polar coordinates the near spatial singularity cancels to dr. Thus
D and (1+|b|)^p D are integrable for every fixed p>=0. In particular,

    integral_(dist(0,y)<delta) Psi_ell(b,y) db dy <= C delta (Z18)

uniformly in 0<ell<=1, with the integral over all birth heights. This is a
uniform-integrability estimate, not an assertion that each candidate kernel
has the same bound.

## 5. The equal-height coefficient, positivity and total variation

By (Z12) and (Z17), Psi_0<=D and dominated convergence proves (Z5). The case
p=0 yields finiteness of B_(d,L) and (Z4), using the repaired marked Kac-Rice
identity to identify the integral of Psi_ell with the rejected density version.
The diagonal, cut-locus boundaries and an arbitrary near/far cutoff boundary
are spatially null; no mass is assigned there by this formula.

For positivity, fix any y!=0 and any b. The density p_y(v_(b,0)) is positive.
Section 2 shows that the conditional joint Hessian density is everywhere
positive. An open neighborhood of

    H_0=-I_d,     H_y=diag(1,-1,...,-1)

has the required two types and strictly positive determinant product.
Consequently Psi_0(b,y)>0. The finite-dimensional Gaussian expectation in
(Z2) is continuous away from the diagonal, by continuous regression and a
local polynomial Gaussian majorant (the type boundaries have zero Gaussian
measure). Integrating over any small open product neighborhood proves B>0
and establishes the full-support assertion in Section 1. This positivity
argument does not consume a rare-cap lower theorem or Theorem U.

Let mu_ell and mu_0 be the finite measures with densities Psi_ell and Psi_0;
their masses are rho_rej(ell) and B, respectively. The first mass is positive
for sufficiently small ell because it tends to B>0. The elementary inequality

    ||mu_ell/rho_rej(ell)-mu_0/B||_TV
                <= ||Psi_ell-Psi_0||_(L1)/B               (Z19)

follows by adding/subtracting mu_ell/B and using
|rho_rej(ell)-B|<=||Psi_ell-Psi_0||_1; TV for probability measures is half the
L1 distance. This proves (Z6). The same reasoning with (Z5) gives convergence
of all fixed polynomial birth moments. Pushforward to displacement or distance
preserves TV convergence. From (Z18) and rho_rej(ell)>=B/2 eventually, the
conditional rejected-distance mass below delta is also O(delta).

**Why this does not make the candidate density bounded.** At each fixed
separation the unmarked candidate kernel also tends to (Z2), but its positive-gap
spatial integral diverges like c ell^(-1/3), by P. There is no contradiction:
the uniform near-diagonal bound (Z15) uses the REJECTION factor via K2 on r<=k.
It is unavailable for candidates or selected pairs. Their leading mass can
concentrate at shrinking separation; the rejected population cannot. Interchanging
the candidate's zero-gap and near-diagonal limits would be the invalid step.

## 6. Counts, moment coefficients and intensity sampling

Since rho_rej(ell)=B+o(1), integration gives the first assertion in (Z7). For
any q>-1, for every epsilon>0 the bound |rho_rej(ell)-B|<=epsilon holds for all
sufficiently small positive ell. Its integral against ell^q is at most
epsilon t^(q+1)/(q+1), proving the weighted asymptotic in (Z7).

The positive lower bound rho_rej>=B/2 eventually implies divergence of the
full inverse moment for q<=-1. More precisely, for every sufficiently small
fixed t>0,

    integral_epsilon^t rho_rej(ell) d ell/ell
               ~ B log(t/epsilon)         as epsilon->0, (Z20)

and for q<-1,

    integral_epsilon^t ell^q rho_rej(ell) d ell
               ~ [B/(-q-1)] epsilon^(q+1).                (Z21)

These follow by bounding rho_rej between B plus/minus any positive tolerance
on a small interval; the remaining fixed interval contributes a finite term.
The moments are of the rejected counting measure itself, not the subtraction
of two individually infinite expectations. The individual candidate and selected
threshold remains q=-2/3, as in P.

P's unrestricted leading result is nu_cand^all(ell)~c ell^(-1/3), c>0. Division
of (Z4) by this result gives (Z8). Its cumulative version is
integral_0^t nu_cand^all~(3/2)c t^(2/3); combined with (Z7) it gives (Z9).
These formulas identify the leading rare-rejection coefficient for the indicated
intensity-weighted sampling procedures. They do not change P's compact-window
1-p_r=O(r^3) estimate or replace its fixed-radius probability by a lifetime ratio.

The identity nu_eld^all=nu_cand^all-B+o(1) is legitimate as a DIFFERENCE
statement. Writing nu_eld^all=c ell^(-1/3)-B+o(1) would be unjustified: P gives
no o(1) remainder for nu_cand^all by itself. Nothing here asserts such a remainder.

## 7. Verification and review boundaries

The source manifest retains the parent reading rule and the exact K1/K2 proof.
Twelve finite tests were written first and failed at the intended missing-
implementation check; after implementation they pass in normal and optimized
Python. Eight semantic mutants fail in both modes, and unknown labels are
rejected rather than silently treated as a normal run. RESULTS.json is exact,
deterministic bookkeeping for coarea, the two radial regimes, residual concavity,
the positive type example, normalization of finite measures, and moment/ratio
exponents. Source identity and path-negative controls are tested separately.

These tests do NOT prove continuous Gaussian regression, the local-path topology,
Gaussian nullity of type boundaries, infinite-dimensional marked Kac-Rice, or
dominated convergence. The displayed arguments and the specified inputs are the
analytic evidence. Whole-repository/formal replay is hosted evidence only when
its actual run is inspected; no local repository checkout is claimed.

External reconnaissance is recorded in RECONNAISSANCE.md. No priority or novelty
verdict is asserted. Requested non-OpenAI review slices:

A. (Z10)-(Z12): fixed-site regression, local CONCAVITY barrier and limiting mark;
   in particular exclude an older point inside the ball rather than relying on
   its low boundary alone.
B. (Z13)-(Z18): all normalization factors, domain-correct K1/K2 use, all b/k/axes,
   and the integrable diagonal majorant.
C. (Z3)-(Z9),(Z19)-(Z21): positive finite coefficient, weighted L1 and TV law,
   moment coefficients and the precise intensity-sampling interpretation.

All author-side claims remain candidates pending that review. Same GitHub account
as other model lanes; zero organizational-independence credit. No register fold,
RN numerical closure, Poisson approximation, or uniform-in-d/L assertion is implied.
