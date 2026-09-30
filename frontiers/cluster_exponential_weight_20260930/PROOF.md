# Endpoint exponential-weight closure and independent-replica error

Object: OA-CLUSTER-EXP-WEIGHT-20260930-v1.
Author: OpenAI / Codex. Date: 30 September 2026 UTC.
Disposition: AUTHOR_SIDE conditional proof; nonauthor review required.
Scientific effect NONE. No source theorem, review, register, graph, prize or
Boolean is changed. This is a new implication of two exact interfaces, not a
proof or retrospective acceptance of either interface.

## 1. Exact consumption and the mathematical purpose

Fix one dimension d>=2, torus side L>0, real birth b, gap k>0 and frame. Use the
same variance-one periodized field, endpoint observations, ORIGINAL typed
determinant weight W_r, full endpoint-only Z_r and law Q_r^W=(W_r/Z_r)Q_r as
the two sources. N_r is their ALL-INDEX additional critical-point count in
(b-k r^3,b), with both endpoint pins excluded. In the marked source T=L; a
fixed admissible mark can be placed inside its compact family. No further
normalizer, height conditioning, or Palm size bias enters this definition.

The source interface [MF] is MF1 at Math-#157, exact commit
cbb2f978f9b3e8e2eaca94f3b359b18d7c144f1b. For alpha=2/d there exist
theta>0, C<infinity and r_*>0 such that

    E_QW[N_r exp(theta N_r^alpha)] <= C r^3.                  (E1)

The source interface [SC] is (3) at Math-#162, exact commit
7a44130b41b827577424a73c4feac4cde20b5568. At these fixed parameters,

    nu_r(n)=r^-3 Q_r^W(N_r=n), n>=1,
    nu=nu1 delta_1+nu2 delta_2, 0<nu1,nu2<infinity,
    nu_r(n) -> nu(n) for each n>=1.                          (E2)

[SC] proves more than the coordinate convergence consumed here. Its separate
A/B/C review requirements and parent premises remain separate; an open slice
is not discharged by this implication. [MF] has its own Fourier-regression
and regional marked-Kac--Rice premises. SOURCES.json binds both full texts.

[MF] Section7 previously gives only subsequential weighted compactness from
(E1). [SC] identifies the coefficients in polynomial weights without consuming
(E1). Here their intersection removes the subsequence in exponential weights,
including a boundary exponent that does not require slack. It also gives a
finite error bound for replica sums in that stronger norm. The generic
probability argument below is self-contained and does not use a new Gaussian
regression, Kac--Rice formula, spatial independence, or a coefficient rate.

## 2. The endpoint norm theorem

For a signed or complex measure sigma on the nonnegative integers define

    ||sigma||_w = sum_(n>=0) w(n)|sigma(n)|,
    w(n)=exp(theta n^alpha), w(0)=1.                         (E3)

Measures nu_r and nu have zero mass at0. Put epsilon_r=||nu_r-nu||_w.

**Theorem EW1.** Under (E1)--(E2), epsilon_r ->0 as r->0. This is convergence
at theta ITSELF, not only at theta'<theta. Consequently, with
a_r=sum nu_r(n), a=nu1+nu2 and H_r=nu_r-a_r delta_0, H=nu-a delta_0,

    ||r^-3(Law_QW(N_r)-delta_0)-H||_w <= 2 epsilon_r ->0.    (E4)

The zero mass is centered; r^-3 Q(N_r=0) has no finite limit.

**Proof.** Equation(E1) is exactly

    sum_(n>=1) n w(n)nu_r(n)<=C.                            (E5)

For every integer M>=1,

    sum_(n>M) w(n)nu_r(n)<= C/(M+1).                        (E6)

Fatou on finite sums in(E2) gives sum n w(n)nu(n)<=C. Therefore the same
tail estimate holds for nu. On1<=n<=M, coordinate convergence and finiteness
of the sum give convergence in the w-norm. The norm outside that set is at
most2C/(M+1). First let r->0 at fixed M, then M->infinity. This proves EW1.
The retained n factor in(E5), not an extra exponential moment, supplies the
endpoint uniform integrability. Since |a_r-a|<=epsilon_r and the exact law is
delta_0+r^3 H_r, (E4) follows. The full original tilt was used once in(E1)
and(E2); this step introduces no additional field normalizer. QED.

**Theorem EW2.** For every fixed integer q>=0 and0<=theta'<theta,

    sum_(n>=1) n^q exp(theta' n^alpha)|nu_r(n)-nu(n)| ->0.   (E7)

In particular the positive-conditioned law converges in the ENDPOINT w-norm
to nu/a. The size-biased law converges in every STRICTLY smaller exponential
weight exp(theta'n^alpha) to
(nu1 delta_1+2nu2 delta_2)/(nu1+2nu2).

**Proof.** Put gamma=theta-theta'>0. On n>M the weighted tail of nu_r is bounded
by

    C sup_(n>M) n^(q-1) exp(-gamma n^alpha),                (E8)

which tends to zero. The same holds for nu by Fatou. Finite-coordinate
convergence proves(E7). For positive conditioning use a_r->a>0 and

    ||nu_r/a_r-nu/a||_w
    <= epsilon_r/a_r+|a_r-a| ||nu||_w/(a a_r).

For size bias let z_r=sum n nu_r(n), z=nu1+2nu2. The q=1 case of(E7) gives
convergence of n nu_r in the smaller exponential norm and z_r->z>0. Divide
by z_r as above. These are distinct denominators and distinct probability
laws. QED.

## 3. Why endpoint size bias is excluded: an exact escaping-mass example

The endpoint exponent for EW1 does NOT justify n times that weight. For any
0<alpha<=1 and theta>0 take m=m(r)>=3 tending to infinity and

    nu_r=delta_1+delta_2+eta_m delta_m,
    eta_m=1/[m exp(theta m^alpha)].                         (E9)

For small r, define the genuine probability law
mu_r=(1-r^3(2+eta_m))delta_0+r^3 nu_r. Its nonempty intensity satisfies(E2)
with nu1=nu2=1 and satisfies(E5) with the constant
exp(theta)+2exp(theta 2^alpha)+1. Every fixed polynomial moment of nu_r
converges. Its endpoint norm error is exactly1/m, as EW1 requires.

But z_r=3+exp(-theta m^alpha). The size-biased law has w-weighted mass

    w(m) m eta_m/z_r=1/[3+exp(-theta m^alpha)] ->1/3        (E10)

at m, where the limiting size-biased law has zero mass. It therefore fails
endpoint weighted convergence. This is a counterexample to a tempting stronger
inference, not a counterexample to the Gaussian source law. Extra uniform
integrability at n exp(theta n^alpha) would be needed for that inference.

## 4. Weighted convolution and an explicit replica bound

**Lemma EW3 (convolution algebra).** For0<alpha<=1 and x,y>=0,
(x+y)^alpha<=x^alpha+y^alpha, so w(x+y)<=w(x)w(y). Thus on measures with finite
w-norm, convolution satisfies

    ||sigma*tau||_w<=||sigma||_w ||tau||_w.                 (E11)

This normed space is complete, has identity delta_0, and
exp_*(A)=sum_(j>=0) A^(*j)/j! converges in norm with
||exp_*(A)||_w<=exp(||A||_w).

**Proof.** For alpha<1, the derivative in y of (x+y)^alpha-y^alpha is
nonpositive for y>0, and its value at y=0 is x^alpha. For alpha=1 equality
holds. Multiplying absolute convolution coefficients by w, summing and using
nonnegative Fubini gives(E11). Completeness is that of weighted l1, equivalently
ordinary l1 after multiplying coordinates by w. The exponential series is
dominated in norm by the scalar exponential series. QED.

Let delta=r^3, m_r(t)=floor(t/delta), and take m_r(t) deliberately INDEPENDENT
copies of N_r. Write their sum as S_r(t). By(E5), ||H_r||_w<=2C and
||H||_w<=2C. Choose B=2C. Let

    P_t=Law(P1+2P2), P1~Pois(t nu1), P2~Pois(t nu2),
    P1 and P2 independent.

**Theorem EW4.** For every finite T>=0 and all0<=t<=T,

    ||Law(S_r(t))-P_t||_w
    <= exp(TB)[delta(TB^2/2+B)+2T epsilon_r].               (E12)

In particular the replica laws converge uniformly on bounded t intervals in
the endpoint exponential-weight norm. This includes weighted tail control,
not only an ordinary TV or PGF limit. It claims no rate for epsilon_r.

**Proof.** One-copy law is u_r=delta_0+delta H_r. Independence gives the exact
law u_r^(*m). The convolution exponential

    exp_*(s H_r)=exp(-s a_r) sum_(j>=0) s^j nu_r^(*j)/j!

is a compound-Poisson probability law. Thus exp_*(t H)=P_t. These are
convolution exponentials of signed generators, not signed approximating
probability laws. The series remainder obeys

    ||exp_*(delta H_r)-u_r||_w
    <= delta^2 B^2 exp(delta B)/2.                         (E13)

Indeed for every j>=2,1/j!<=1/[2(j-2)!], so the scalar remainder is bounded
by that right side. Also ||u_r||_w<=1+delta B<=exp(delta B).
Telescoping m convolution factors with(E11) gives, for m>=1,

    ||u_r^(*m)-exp_*(m delta H_r)||_w
    <= m delta^2 B^2 exp(m delta B)/2
    <= t delta B^2 exp(tB)/2.                              (E14)

For m=0 the first difference is zero. For any A,D in this commutative algebra,
norm differentiation of the exponential series and integration in s imply

    exp_*(A)-exp_*(D)
    = integral_0^1 exp_*((1-s)D+sA)*(A-D) ds,
    ||exp_*(A)-exp_*(D)||_w
    <= ||A-D||_w exp(max(||A||_w,||D||_w)).                 (E15)

The floor error0<=t-m delta<delta therefore contributes at most
delta B exp(tB). The intensity replacement uses
||H_r-H||_w<=2epsilon_r, hence contributes at most2t epsilon_r exp(tB).
Adding these three differences and t<=T proves(E12). If T=0 both actual laws
are delta_0; the displayed upper bound remains valid. QED.

The construction says nothing about independence between spatial regions or
different pin pairs in one field. No within-field Poisson process is inferred.
Replacing nu_r by nu in a ONE-COPY approximation does not inherit an r^6
rate: its additional norm error is at most2r^3 epsilon_r=o(r^3), with no
source-supplied rate. Likewise(E12) is O_T(r^3+epsilon_r), not automatically
O(r^3). This preserves the canonical actual-mark/limit-mark distinction.

## 5. Complex generating functions: the dimension boundary

In d=2, alpha=1. Absolute weighted convergence implies uniform convergence
of the intensity PGFs on the CLOSED disk |z|<=exp(theta):

    sup |sum_(n>=1)(nu_r(n)-nu(n))(z^n-1)|<=2epsilon_r.

Each PGF is analytic in its interior and continuous on the boundary. By(E12)
the replica PGFs converge uniformly on that closed disk to
exp[t nu1(z-1)+t nu2(z^2-1)], uniformly0<=t<=T. This does not claim an analytic
neighborhood beyond that disk for each prelimit.

For d>2, alpha<1. No common disk extending the unit disk follows from(E1)
and(E2), despite the finite-support limit. To see this, let q(n),n>=3, be a
probability proportional to n^-3 exp(-2theta n^alpha), and set
nu_r=delta_1+delta_2+epsilon(r)q with epsilon(r)>0 tending to zero. It satisfies
(E1)--(E2): sum n exp(theta n^alpha)q(n)<infinity. Yet for every real z>1,
sum z^n q(n)=infinity, since n log z-2theta n^alpha-3log n ->infinity.
The associated small-r probability laws are constructed exactly as in(E9).
So prelimit PGFs may have radius1. The endpoint convolution norm result still
holds. This generic counterexample does not assert that Gaussian counts
actually have radius1; a larger radius needs another argument.

## 6. Scope, source exposure, falsifiers and review division

The elementary theorems EW1--EW4 apply to ANY nonnegative-integer laws satisfying
(E1)--(E2), with delta=r^3; the proofs also work for another positive delta->0.
Their application here is conditional on BOTH full mathematical interfaces
at the listed fixed parameters. This does not upgrade [SC]'s fixed-parameter
claim to mark-uniform convergence, or [MF]'s compact-family statement to
unbounded birth/gap/dimension/volume. Constants theta,C,B are existential;
no extra coefficient digits or numerical enclosure is claimed.

The author is exposed to both OpenAI source packets and the prior Slice-C
review of [SC]. That source-exposed work is not independent acceptance of
[SC] or [MF]. Internal OpenAI challenge agents have zero organizational
independence. A contributor who changes this proof cannot self-accept it.
Finite checks, custody hashes and CI establish finite/custody facts only.

Falsifiers of the conditional application: unequal original W/Z/count
interfaces; failure of(E1) at any sufficiently small r; failure of(E2)'s
coefficient limit; replacement of independent copies by coupled copies.
Falsifiers of the NEW implication: an arithmetic/algebra error in the tail
bound(E6), absolute convolution(E11), floor/telescoping ledger(E12)--(E15),
or normalized-law passage. The exact examples(E9)--(E10) preserve the failure
of endpoint SIZE-BIASED convergence; they must not be removed from an honest
stronger-weight statement. The dimension counterexample preserves the
non-implication of a complex neighborhood for alpha<1.

Proposed nonauthor slices, each independently rejectable:
A: endpoint intensity tails, strict-weight moments, positive/size-biased
normalizations and the escaping-mass falsifier (§§2--3).
B: submultiplicative convolution, uniform replica error and actual-versus-limit
mark rate (§4), plus the complex-disk boundary (§5).
The parent Gaussian/spectral and Fourier arguments are OUTSIDE these slices.
No merge or scientific-status transition is justified solely by this packet.
