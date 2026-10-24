# IBA2-012: a shifted count tail and growing factorial orders

Object: IBA2-012-LOG-CAP-CONCENTRATION-20261006-v1.
Dylan Roy — delegated AI mathematical work. Actual author OpenAI / GPT-6 Astra Pro,
`iba2-concentration-continuation-20261006-r8`, pickup main#259/6008758240.
Author-exposed continuation of the FR/CT/LT lineage; organizational credit 0;
scientific effect NONE. **Conditional author-side candidate; nonauthor review required.**
No existing source, scientific status, formal target or workflow is changed.

## 1. New scope, exact inputs, and inherited limits

The fixed-power logarithmic bound is already LT, Math-#327. The fixed-moment
transfer and its all-order no-loss obstruction are CT, Math-#319. Neither is
claimed again. This note retains the cap-tail's dependence on log(1/r), proving
an exponential bound for a shifted, budget-scaled finite measure. It then permits
explicitly GROWING count orders without pretending fixed-order constants are
uniform. Its threshold is an inference result, not actual-field optimality.

At source cut `07ff1191f3f99987060517b6413417287b5adf21`, the quantitative inputs are:

| Tag | Path | Full Git blob | Consumed scope |
|---|---|---|---|
| FR | `reviews/iba2_012_finite_radius_20261005/PROOF.md` | `5ed684c9bb446efc9bef5f3980717c6dc039abfd` | Sections3–5/8: exact law, full Z, derivative-weighted event bound |
| SH | `frontiers/c6_sharpened_20260929/PROOF.md` | `70ba19726a9114bfceae04d021095e6c8eed5026` | Sections3–4 and (5.1): original-law cap tail, BEFORE first-moment assembly |
| P | `imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md` | `dfed3b8d318a3ab1950957f393307733a4bef3f2` | (4.1), moment sentence after (5.3), (5.5) |

Provenance-only LT is `reviews/iba2_012_log_cap_transfer_20261006/NOTE.md`, blob
`b158965faf0f4113309d825ce1892743910fc028`, at its reviewed head
`e71fd6ecd59071181d4e476d0e4e87287d4488b1`. Its (dyadic) abstract family is reused
and credited in section6. LT review6008413541 does NOT review this note. CT is
blob `752bc9da5e49af3d0724d80c91cffc0dde35a2d8` at the source cut above. Neither
LT integration nor a new verdict on its ancestors is an assumption here.

Keep FR's fixed d>=3, torus side L, physical observation radius R>=1, compact
birth interval, compact gap marks with k_->0, and compact frame space. Use its
original Gaussian pin law Q_r and its FULL tilted law P_r=Q_r^W with density
D_r=W_r/Z_r. N is the torus-wide between-pin count, N_R its local subcount, and
K>=1 is FR's fixed multiple of 1+||f||_C4. No source's other use of K is identified
with this variable. Let 1<=q<=d-2 and choose deterministic ordered thresholds
0<=eta_2<=...<=eta_(q+1)<=1/2. Set

    S_r = {h_j<=eta_j, j=2,...,q+1},
    E_r = {N_R>0} intersect S_r,
    beta = q(q+7)/2,
    Xi_r = product_(j=2..q+1)(eta_j+r)^(j+2),
    rho_r = r^3 Xi_r.

At r<=1/2, r^beta<=Xi_r<=1. The remaining eigenvalues have no unmentioned hard
lower bound; zero thresholds and the all-soft transverse case remain included.
FR supplies for the one fixed derivative power a>=0

    E_(P_r)[K^a 1_Er] <= A_a rho_r.                        (F)

SH supplies a measurable cap Psi>=N and fixed C_t,c,x0>0 such that

    Q_r(Psi>x) <= C_t exp[-c x^(1/d) log x], x>=x0.        (T)

Its moment/cover/Gram qualifications remain inherited. In particular this note
does not repair an invalid tail or re-audit the complex-gradient argument. The
later G_d/I5 first-moment assembly of SH is NOT consumed. All constants below
are conditional on the stated inputs at their existing scope.

## 2. A finite measure, not a conditional probability

Put u=log(1/r), Lambda=u/log u and X=N^(1/d)/Lambda. Reduce the common radius
cutoff so u>=u0>=8 and Lambda^d>=max(1,x0). This is possible since Lambda grows
and is increasing for u>e. No numerical field radius is supplied.

Define a finite measure on [0,infinity) by

    mu_r(B) = rho_r^(-1) E_(P_r)[K^a 1_Er 1_{X in B}].    (M)

Its total mass is at most A_a. rho_r is an upper-bound SCALE, not the measured
mass of E_r, and mu_r is not in general a probability measure. No lower local,
Palm, factorial or derivative-weighted event denominator is assumed.

P supplies uniform ||D_r||_(L4(Q_r)) and ||K^a||_(L4(Q_r)). Write

    H_a = sup_r ||D_r||_4 ||K^a||_4 sqrt(C_t) < infinity.

This follows from ||D_r||_4=||W_r/r^2||_4/(Z_r/r^2), the full floor in P(5.5),
and the fixed moment order4a in P(4.1). The density is inserted once. Correlation
among D_r,K,Psi, and E_r is unrestricted.

**Tail lemma.** For every y>=1,

    mu_r((y,infinity))
       <= H_a exp[(beta+3-c y/2)u].                     (1)

**Proof.** Cauchy–Schwarz under ORIGINAL Q_r, then Holder on D_r K^a, gives

    E_(P_r)[K^a; E_r, X>y]
      <= ||D_r K^a||_2 Q_r(Psi>(y Lambda)^d)^(1/2)
      <= H_a exp[-(c/2) y Lambda log((y Lambda)^d)].

Only the cap EVENT is in this tail inequality, not a Psi^s factor; the exponent
is therefore one half rather than LT's four-factor one quarter. For u>=8 we
have log u>2. At t=log u>=2, t/2-log t is positive and nondecreasing. Hence
log((y Lambda)^d)>=d(log u-loglog u)>=(d/2)log u>=log u.
The exponent is at most -(c/2)y u. Finally rho_r^(-1)<=r^(-3-beta), proving (1).
Neither independence nor a global count first moment was used.

## 3. Shifted exponential control with its actual u dependence

Let

    y0 = max(1,4(beta+3)/c),
    Y = (X-y0)_+,
    kappa_r = c u/8.

For z>=0, (1) and beta+3<=c y0/4 imply

    mu_r(Y>z) <= H_a exp[-c u(y0+z)/4].                 (2)

The original unshifted bound with y=y0+z is valid even at z=0 because Y>0 is
X>y0. The stronger inequality from (1) has a z coefficient c/2; (2) only weakens
it to c/4.

**Exponential theorem EC.** Uniformly in r and every allowed threshold,

    integral exp[kappa_r (x-y0)_+] dmu_r(x)
        <= A_a + H_a exp[-c u y0/4] <= A_a+H_a=:M_a.    (EC)

**Proof.** For a finite measure, Tonelli and exp(kY)=1+integral_0^Y k exp(kz)dz
show that the left side equals mu_r(total)+kappa_r integral_0^infinity
exp(kappa_r z) mu_r(Y>z) dz. Insert (2). Since c u/4=2 kappa_r, the exponential
integral contributes H_a exp[-c u y0/4]. This proves finiteness as well as the
bound. It is not a probability-only layer-cake identity.

As a quantitative tail-budget consequence, for 0<delta<1 define

    z_delta = max(0, 4 log(max(1,H_a)/delta)/(c u) - y0).

Equation (2) bounds the K^a-weighted mass above
N>[Lambda(y0+z_delta)]^d on E_r by delta*rho_r. Constants are existential source
constants; this is not an evaluated numerical sampler budget. It does not
normalize by an unknown conditional-event probability.

## 4. Uniform count-order envelope and its growing-order consequence

For every real s>0 satisfying

    d s <= kappa_r y0 = c u y0/8,                       (O)

EC implies the SAME-constant bound

    E_(P_r)[K^a N^s;E_r]
        <= M_a rho_r (y0 Lambda)^(d s).                (G)

M_a,y0,c are independent of s in (O). Indeed let v=d s. The scalar inequality

    x^v <= y0^v exp[kappa_r(x-y0)_+], x>=0,             (3)

holds because it is immediate for x<=y0 and, for x>=y0, the derivative of
v log(x/y0)-kappa_r(x-y0) is v/x-kappa_r<=0 under (O). Integrate (3) in (M).
Since s>0 and 0<=N_R<=N, the same bound holds for E[K^a N_R^s;S_r]. The s=0
case keeps E_r and uses (F); N_R^0 1_Sr is not identified with that event.

**Growing-degree corollary.** Suppose Xi_r<=C_X r^B for some fixed B>0. For a
fixed theta with 0<theta<=B/d set integer s(r)=floor(theta Lambda(r)), once it is
at least1. Then

    r^(-3) E_(P_r)[K^a (N_R)_(s(r)); S_r] -> 0.         (4)

This also holds with the falling factorial replaced by N_R^(s(r)). To prove it,
note s(r)/u<=theta/log u->0, so (O) holds eventually with the SAME constants.
Use (N_R)_s<=N_R^s and (G). The logarithm of its upper bound, apart from a fixed
constant, is at most

    -B u + d theta (u/log u) [log u - loglog u + log y0]. (5)

For theta<B/d its leading coefficient -B+d theta is negative. The endpoint
case theta=B/d ALSO decays: (5) becomes

    -B u (loglog u-log y0)/log u -> -infinity.           (6)

We do not infer (4) by choosing an r-dependent p in CT or s in LT with unknown
constant dependence. It follows from EC and its explicit simultaneous envelope.
The endpoint statement is for this precise floor(theta Lambda) convention;
arbitrary sequences asymptotic to (B/d)Lambda can have consequential second-order
changes. No claim at every such critical sequence is made.

For eta_j=r^alpha_j with fixed consistently ordered positive alpha_j,
B=sum_(j=2..q+1)(j+2)min(alpha_j,1)>0 and C_X can be 2^beta. In d3,q1,eta=r,
B=4, so (4) holds for s(r)=floor(theta Lambda) with 0<theta<=4/3.

At each r one may regard (4) as a bound on the total mass of the positive ordered
s(r)-tuple intensity measure deleted on S_r. Its underlying product space changes
with s(r); no fixed-space process limit, density, event-selection or elder theorem
is inferred. No factorial size-biased probability is formed, since its lower
normalizer would be a separate premise.

## 5. No hidden normalization or independent field claim

The preceding bounds are for mu_r, not the law conditional on E_r. An upper mass
bound cannot supply that missing denominator. Even an abstract measure of mass
exp(-2 k t) at Y=t has bounded integral exp(kY), whereas its normalized one-atom
probability has exponential moment exp(k t), unbounded as t grows. This illustrates
the distinction and is not an additional field example.

No assertion is made that actual higher degeneracies realize large critical
counts, or that any of the upper estimates are sharp for the field. Existing
fixed-power LT and CT statements remain unchanged and useful at their own scopes.
The all-mark/small-k, growing-R, arbitrary higher-jet, remote-only, lifetime and
independent-alignment questions remain separate. General IBA2-012/009 is not closed.

## 6. The leading growing-order threshold is optimal from the numerical inputs

We reuse LT section5's SINGLE abstract family, not a new field construction.
Fix d>=3,q=1, j>=2, n=2^j, r_j=2^(-n), v_j=floor(n/j). Under Q_j=P_j give an
ordinary atom probability r_j^3,count N=N_R=2,h2=2; a rare atom probability r_j^7,
count N=N_R=v_j^d,h2=r_j; all remaining mass count0. Put h1=r_j/2, K=3,
W=Z=r_j^2 and Psi=N+2. Remaining transverse marks, if any, can be fixed at3.

For completeness these numerical interfaces hold simultaneously:
- Only the rare atom belongs to E at eta in[r_j,1/2]; below r_j the event is empty.
  Thus FR's weighted bound holds with A_a=3^a/16, since (eta+r_j)^4>=16r_j^4.
- D=1 and K=3 have uniform fixed moments and full Z/r_j^2=1.
- For t>=4, a nonzero cap tail has probability r_j^7 and t<v_j^d+2.
  As v_j>=2, t^(1/d)<=2v_j and log t<=d log(2v_j), so
  t^(1/d)log t <=2 d(n/j) log(2n/j)<=3 d n log2 for j>=2.
  Thus Q(Psi>t)<=exp[-(1/d)t^(1/d)log t]; one c=1/d works for all j.
- Every fixed count moment is O(r_j^3), since
  E N^p/r_j^3=2^p+r_j^4 v_j^(dp) and exponential decay dominates fixed powers.

These checks retain exactly the type of quantitative information consumed above,
not Gaussian/spectral/geometric realizability. In particular K is an abstract
mark here, not the C4 norm of a constructed analytic field.

Let u_j=n log2 and Lambda_j=u_j/log u_j. Then

    v_j/Lambda_j -> 1,  Lambda_j -> infinity.

Indeed n/j divided by Lambda_j is (j log2+loglog2)/(j log2)->1, and the floor
has vanishing relative effect. Choose s_j=floor(theta Lambda_j) for fixed theta>0.
N=v_j^d and s_j=O(v_j), so s_j^2/N->0 for d>=3. Consequently

    (N)_(s_j)/N^(s_j) -> 1,                            (7)

using product_(i=0..s-1)(1-i/N)>=1-s(s-1)/(2N) and the upper bound1, valid once
s<=N. The deleted r_j^-3 factorial mass on eta=r_j is r_j^4(N)_(s_j). Therefore

    lim_j u_j^(-1) log[r_j^-3 E[(N_R)_(s_j);S]]
         = -4+d theta.                                (8)

The harmless constant K^a does not change this rate. For theta>4/d the mass grows
instead of vanishing. Hence a universally larger leading threshold than B/d
cannot be deduced from the numerical inputs, already at B=4. For theta=4/d the
leading rate is zero; the actual endpoint decay in (6) is a second-order result,
not contradicted by (8). We do not claim a complete sharp subleading transition.

The finite diagnostic uses s_j=floor(theta*n/j) rather than numerical logarithms;
it is asymptotic to theta Lambda_j and checks only STRICT sides of (8). It does
not test the endpoint convention or prove the infinite limit. The written proof
does so. Exact log2 brackets avoid calculating enormous factorials/probabilities.

**Stronger-input boundary.** The concurrent fixed-order marked-sector proposal
(main#259/6008806185) uses MF1's rare-scale marked stretched-exponential input,
not just (F)/(T)/P, and has a different claimed fixed-power penalty. Its writer,
source, reviews and status are separate. Nothing here says B/d is optimal when
that additional information is supplied. This note neither consumes nor reviews
MF1 or that proposal, and does not rename it as part of this work.

## 7. Verification and review focus

The supplied standard-library helper and eleven-method suite check the half-tail
factor, full budget normalization, shift, finite layer integral coefficient,
order condition, leading threshold and second-order exponent ledger, factorial
product bounds, strict-side dyadic brackets, correlated finite marks and invalid
domains. Exact Fraction/integer arithmetic only. Symbolic log-values in one ledger
are not numerical certification of field constants or transcendental inequalities.

The initial ten-method source absence produced ten intended assertions, zero
errors; the critical-boundary addition had one missing-ledger assertion before
implementation. Six wrong variants exercise the named half/shift/exponential/
order/dimension/normalizer steps. Their exact assertion-name sets, both Python
modes, actual commands and hashes belong to execution receipts. They do not prove
Tonelli, arbitrary-law Holder, the SH tail or any continuum field statement.

Read (1)–(3), rho's meaning and constant dependence, then the growing-order step
(5)–(6) and the factorial comparison (7)–(8). Reuse only the exact quoted source
interfaces; no full ancestor review is claimed. Required hosted checks and a
separate eligible integration remain distinct from mathematical review. No author
self-merge and no change to a previous frozen packet or scientific register.
