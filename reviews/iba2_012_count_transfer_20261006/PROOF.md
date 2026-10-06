# IBA2-012: count-weighted transfer on shrinking multi-soft sectors

Object: IBA2-012-COUNT-TRANSFER-20261006-v1.
Dylan Roy — delegated AI mathematical work. Actual author OpenAI / GPT-6 Astra Pro,
continuation `iba2-count-weight-transfer-r6-20261006`, under main#259/6007422896
and resumption6007796915. The author also authored the finite-radius precursor.
Source-exposed; organizational-independence credit0; scientific effect NONE.
**Author-side conditional proof candidate. Nonauthor analytic review required.**
No existing proof, scientific register, acceptance record or formal manifest changes.

## 1. Exact source cut and the gap being addressed

Repository `d6g8k5htny-coder/Math-`, source cut
`99ba2dfe33ef0052694510355b0c4d811fd66441`.

| Tag | Path | Full Git blob | Consumed slice |
|---|---|---|---|
| FR | `reviews/iba2_012_finite_radius_20261005/PROOF.md` | `5ed684c9bb446efc9bef5f3980717c6dc039abfd` | Sections3–5 and8: same-law finite-radius derivative-weighted nonempty-sector bounds, especially FR-mixed |
| CP | `frontiers/c6_palm_route_20260929/PROOF.md` | `89eb8adf08fe7afc2cab9662d3a9875c05ae5cc5` | Sections1.1–1.3: law/count, Theorem Q(1.1), all inherited scope/dependency qualifications |
| ERR | `reviews/d5_dimension_lift_erratum_20261005/ERRATUM.md` | `23df87bbe4ffd3b2d786cd695fb9f5448cfa1d05` | Entire additive correction, including CP section6.2 R3a's repeated citation |

FR section5 explicitly says that inserting N_R^j needs a separate count-moment
argument. This note supplies that argument. It neither re-proves P section7 nor
reclaims the existing limiting multi-soft measure. FR was integrated by #306 with
scoped nonauthor review6005379068; its original author-side source header remains
historical. CP is imported at Theorem Q's stated scope, not promoted by its merge,
and ERR is read with the unchanged original. No mistaken intermediate Lipschitz
display or doubled normalizer is imported. A defect in an imported interface
invalidates the corresponding application here. No fresh full audit of CP's
ancestors is claimed.

The argument needs only one fixed factorial moment order for each chosen bound.
It does not infer a global first moment from higher factorial moments, assume
count/curvature independence, or assert conditional derivative moments under an
additional witness law. The localization below handles the missing first moment.

## 2. Setting, notation and claimed result

Keep FR's fixed dimension d>=3, torus side L>0, observation radius R>=1, compact
birth interval and compact gap marks 0<k_-<=k<=k_+. Frames range over the compact
orthogonal group. Reduce the common positive radius cutoff so FR and the chosen
instance of CP hold and r<=1. Constants may depend on these fixed data and the
chosen moment orders, but not on r, frames, marks within their sets or thresholds.

Write P_r=Q_r^W, using the exact same Gaussian pin law, typed maximum/saddle weight
and full normalizer as FR and CP. P_r is a probability measure, not source P.
Let N be CP's torus-wide count of all-index critical points between the pin heights,
excluding pins. Let N_R be FR's count in the Rr-ball. Then 0<=N_R<=N pathwise.
Let K>=1 be FR's C4 derivative control; CP's unrelated use of K for a C6 norm
introduces no new assumption about this K.

Fix 1<=q<=d-2 and ordered deterministic thresholds
0<=eta_2<=...<=eta_(q+1)<=1. With FR's ordered midpoint eigenvalues h_j, define

    S = {h_j<=eta_j for 2<=j<=q+1},
    E = {N_R>0} intersect S,
    Xi = product_{j=2}^{q+1}(eta_j+r)^(j+2),
    beta_q = sum_{j=2}^{q+1}(j+2) = q(q+7)/2.

The h_j need not be positive at finite r. Remaining eigenvalues have no hard
lower bound; the all-soft transverse case is allowed. FR gives, for every fixed t>=0,

    E_{P_r}[K^t 1_E] <= A_t r^3 Xi.                     (F)

CP gives, for every fixed integer m>=2,

    E_{P_r}[(N)_m] <= B_m r^3.                         (C)

Here (n)_m=n(n-1)...(n-m+1), with value0 for integers 0<=n<m.
These are the only quantitative inputs.

**Theorem CT.** Fix real a>=0, p>0 and an integer m>=2 with m>p. Then

    E_{P_r}[K^a N^p 1_E] <= C_{a,p,m} r^3 Xi^(1-p/m).  (CT)

Consequently

    E_{P_r}[K^a N_R^p 1_S] <= C_{a,p,m} r^3 Xi^(1-p/m). (CT-local)

For p=0 use (F) directly, with E retained. There is no convention turning
N_R^0 1_S into a nonempty-sector event. The theorem does not bound N^p 1_S
when all witnesses are remote and N_R=0.

## 3. Proof

### 3.1 A localized ordinary moment, without a global first-moment premise

For every nonnegative integer n and integer m>=2,

    n^m <= m^m [1+(n)_m].                              (3.1)

If n<m the constant suffices. If n>=m, each factor n-i, 0<=i<m, is at least n/m,
since n-m+1>=n/m. Therefore (n)_m>=(n/m)^m. Multiplying by 1_E and using (C)
and (F) at t=0 gives

    E[N^m 1_E] <= m^m[P_r(E)+E[(N)_m]]
               <= m^m(A_0 Xi+B_m)r^3 <= D_m r^3,       (3.2)

because Xi<=2^beta_q. Finiteness is licensed by the count interface; alternatively
(C) excludes an infinite count, and truncation proves the same displayed bounds.
The +1 in (3.1) and the event localization are essential: N=1 has all factorial
moments of order>=2 equal to0. We do not replace (3.2) by an unproved global
E N^m=O(r^3).

### 3.2 Holder on the same probability measure

Put u=m/(m-p) and v=m/p. These are conjugate exponents greater than1. Holder gives

    E[K^a N^p 1_E]
      <= (E[N^m 1_E])^(p/m)
         (E[K^(a m/(m-p)) 1_E])^(1-p/m).              (3.3)

Use (3.2) and (F) at the fixed larger derivative moment a m/(m-p):

    <= (D_m r^3)^(p/m)
       (A_(a m/(m-p)) r^3 Xi)^(1-p/m)
     = C_{a,p,m} r^3 Xi^(1-p/m).

The radial exponent is 3, not 3(1-p/m): both factors contain r^3. No independence
is used and no additional division by Z occurs. FR already charged the derivative
tails. There is no joint count/derivative-moment premise or exchange of a limiting
law with shrinking thresholds. For p>0, N_R^p 1_S=N_R^p 1_E<=N^p 1_E. This proves
CT-local and completes the proof.

## 4. Consequences at the r^3 cluster scale

### 4.1 Shrinking thresholds and the quantified loss

For eta_j=r^alpha_j with fixed alpha_2>=...>=alpha_(q+1)>0, let

    B = sum_{j=2}^{q+1}(j+2) min(alpha_j,1)>0.

Each eta_j+r<=2 r^min(alpha_j,1), so

    E[K^a N_R^p 1_S] = O(r^[3+B(1-p/m)]) = o(r^3).     (4.1)

Saturation below the perturbation scale r is unchanged. For equal thresholds r,
B=beta_q. Taking m=2p for a fixed positive integer p gives:

| Additional soft directions q | FR event bound | Count-weighted bound with m=2p |
|---:|---:|---:|
| 1 | O(r^7) | O(r^5) |
| 2 | O(r^12) | O(r^(15/2)) |
| 3 | O(r^18) | O(r^(21/2)) |

Rows require d>=q+2. For q=2, thresholds (r^(1/2),r^(1/4)) give B=13/4;
p=1,m=2 gives O(r^(37/8)), still o(r^3).

For every fixed epsilon in (0,1), choose a fixed integer m>=2 with m>p and
p/m<=epsilon. Then CT implies O(r^3 Xi^(1-epsilon)); for Xi>1 absorb the bounded
range Xi<=2^beta_q into the constant. Neither B_m nor A_t is controlled uniformly
as m grows. Setting epsilon=0 by taking a limit of these inequalities is invalid.
Section5 supplies countermodels. No r-dependent moment order is allowed here.

More generally, ordered thresholds all tending to0 give Xi->0 and o(r^3), without
a prescribed power-law rate. Fixed nonshrinking thresholds give a bound, not an
assertion of negligible contribution as r tends to0.

### 4.2 Factorial intensity measures and polynomial observables

For each fixed integer s>=1, (N_R)_s<=N_R^s. CT-local with p=s bounds the mass of
ordered s-tuples of distinct local window points on S. Let nu_(r,s) be r^-3 times
the expected positive measure of these tuples, with measurable positional or
rescaled-coordinate marks; let nu_(r,s)^keep delete configurations in S. Then

    ||nu_(r,s)-nu_(r,s)^keep||_variation
      = r^-3 E[(N_R)_s 1_S] <= C Xi^(1-s/m),           (4.2)

where m>=2 and m>s. This uses total mass as the norm of a positive measure, not
the half-L1 convention for probability distributions. These are finite measures
at each fixed r: (3.1) and (C) also give finite unlocalized ordinary moments,
though not the r^3 order used in (3.2). There is no assertion that the entire
intensity measures converge; only the deleted mass is controlled.

For a signed tuple observable bounded pointwise by K^a, its deleted expectation
is bounded in absolute value by r^-3 E[K^a(N_R)_s 1_S]. Nonnegative sums of fixed
powers, or polynomials whose constant term is multiplied by 1_{N_R>0}, follow
term by term. Factorial degrees and polynomial degrees stay fixed.

An additional local lower bound P_r(N_R>0)>=c r^3 would allow division to obtain
conditional-on-local-occurrence bounds of order Xi^(1-p/m). That lower bound is
not assumed or proved here. Size-biased normalization needs its own lower bound.
A torus-wide lower obstruction is not silently substituted for a local one.

## 5. What the listed interfaces cannot prove

### 5.1 Optimal exponent with one fixed factorial order

Fix m>=2 and 0<p<m; use d=3, beta_1=4. On an abstract finite probability space,
set r_n=2^(-mn), K=1. An ordinary atom has mass r_n^3, N_R=N=2 and h_2=2.
A rare atom has mass r_n^7, N_R=N=2^(4n) and h_2=r_n. The remainder has count0;
put h_1=r_n/2 throughout. Probabilities sum to less than1 for n>=1.

For every eta in [0,1], E is empty if eta<r_n and consists of the rare atom
otherwise. Thus (F) holds for every derivative power. Also (N)_m<=N^m and
r_n^7 2^(4nm)=r_n^3, proving the mth instance of (C). Yet

    E[N^p;E_(eta=r_n)] = r_n^3 r_n^[4(1-p/m)].          (5.1)

Consequently a uniformly larger Xi exponent is not deducible from (F) and that
one factorial-moment bound. Higher factorial orders need not be O(r^3) for this
family; this is not the all-orders countermodel below.

### 5.2 All fixed factorial orders still do not give loss-free transfer

Use d=3 again, but now r_n=2^(-n), K=1. The ordinary atom has mass r_n^3,
N_R=N=2,h_2=2; the rare atom has mass r_n^7,N_R=N=n+2,h_2=r_n; the remainder has
count0. Set h_1=r_n/2. This is one family for all moment orders simultaneously.
The same all-threshold calculation proves (F), and for every fixed integer s>=2,

    E[(N)_s] <= E[N^s]
      = r_n^3[2^s+2^(-4n)(n+2)^s] <= C_s r_n^3.       (5.2)

For example n+2<=3n and
n^s<=s! binomial(n+s-1,s)<=s!2^(n+s-1) for n>=1 give an explicit finite C_s.
The family also satisfies P(N_R>0)>=r_n^3 and E[(N)_2]>=2r_n^3. Nevertheless,
for every p>0 at eta=r_n,

    E[N_R^p;S]/[r_n^3(eta+r_n)^4] = (n+2)^p/16 -> infinity. (5.3)

Loss-free O(r^3 Xi) count transfer therefore does not follow even from the entire
collection (C),(F) and those occurrence/second-factorial lower bounds. In fact
r_n^-3 E[exp(tN);N>0] is bounded for each fixed 0<t<4 log2: its rare term is
exp(2t) exp[-n(4log2-t)]. Even that additional property does not give a constant
loss-free bound on this sector. The inequality fails already on a sequence r_n;
no continuous interpolation of the family is needed to refute a uniform deduction.

These are abstract count/mark models, not Gaussian fields, Hessian realizations,
or fixed Gaussian residual counterexamples. They limit an inference from the
stated interfaces, not a stronger independently proved field theorem.

### 5.3 A sufficient additional interface for a loss-free bound

One natural sufficient strengthening is a uniform conditional count moment under
the derivative-weighted sector measure:

    E[K^a N_R^p 1_E] <= C E[K^a 1_E].                 (5.4)

Where the right-hand denominator is positive, this states a bounded pth count
moment after normalizing K^a 1_E dP_r; otherwise both integrals vanish. Combining
(5.4) with (F) gives O(r^3 Xi) without exponent loss. This is not claimed to be
logically necessary or already proved by CP. It is a precise missing interface
for that natural route; it needs a sector-conditioned count estimate, not just
unconditional fixed-order moments. The present CT already proves the required
o(r^3) negligibility on shrinking sectors without (5.4).

## 6. Verification and limits

The standard-library test_count_transfer.py contains thirteen finite test methods.
They check the factorial envelope including counts below m, event-localized moments,
finite Holder inequalities with correlated derivative/count marks, common radial
power, unequal exponents, saturation, the all-order spike model and ordered-tuple
mass. M1 drops a radial factor, M2 discards Holder's exponent loss, M3 reverses
unequal threshold weights, and M4 removes the indispensable +1 in (3.1).
Intended failures must be assertions with no unexpected errors; an invalid label
must exit2. These tests do not prove the continuum or imported field interfaces.

At initial publication the author's container/Python execution tools returned
InvalidArgumentError before execution. The test source was written but no new
local execution or SHA-256 calculation is claimed. Native Git blobs bind the
published text; actual runs, review and their exact source identities belong in
subsequent PR receipts. No standalone test is secretly covered by the existing
repository CI, which does not discover tests in this packet automatically.

The smallest nonauthor read is (3.1)–(3.3), with the exact (F)/(C) law alignment,
and the all-threshold countermodel (5.2)–(5.3). Check real p, zero thresholds,
p=0 exclusion, derivative moment order, all-soft dimensions and intensity marking.
Review may reuse the unchanged imported interfaces without repeating their whole
proof chains, while retaining every inherited qualification.

IBA2-012 remains open globally: no all-mark limit, growing observation radius,
general higher-jet classification, remote-only sector bound, lifetime pushforward,
elder-selection theorem, loss-free conditional moment, or full cluster-law rate
is established. IBA2-009 matching is untouched. No numerical field constant,
new Lean theorem, scientific acceptance or claim of independent organization is
created by this note.
