# IBA2-012: full soft power with an optimal logarithmic cap penalty

Object: IBA2-012-LOG-CAP-TRANSFER-20261006-v1.
Dylan Roy — delegated AI mathematical work. Actual author OpenAI / GPT-6 Astra Pro,
`iba2-log-cap-transfer-20261006-r7`, pickup main#259/6008206382. Author-exposed
continuation of FR/#319/#324; organizational-independence credit0; scientific effect NONE.
**Conditional author-side proof candidate. Nonauthor mathematical review required.**
No prior proof, acceptance record, scientific register or formal target changes.

## 1. Sources, new scope and ancestry

Repository `d6g8k5htny-coder/Math-`. Source cut:
`b25cac0bcbb4032d624f14795257d9578c90d105`.

| Tag | Path | Complete Git blob | Consumed interface |
|---|---|---|---|
| FR | `reviews/iba2_012_finite_radius_20261005/PROOF.md` | `5ed684c9bb446efc9bef5f3980717c6dc039abfd` | Sections3–5/8, original finite-radius mixed-threshold event bound with each fixed derivative-norm power |
| SH | `frontiers/c6_sharpened_20260929/PROOF.md` | `70ba19726a9114bfceae04d021095e6c8eed5026` | Sections3–4 and section5 BEFORE its first-moment assembly: measurable cap Psi, original-law tail(5.1), and fixed moments |
| P | `imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md` | `dfed3b8d318a3ab1950957f393307733a4bef3f2` | (4.1), (5.1)–(5.5): uniform derivative and W/r^2 moments, and full normalizer Z>=z_*r^2 |
| CT | `reviews/iba2_012_count_transfer_20261006/PROOF.md` | `752bc9da5e49af3d0724d80c91cffc0dde35a2d8` | Provenance/comparison; section3 only for the OPTIONAL minimum with its fixed-order bound |

FR's spectral integration and CT's count insertion/abstract no-constant-loss
obstruction are already recorded. This note does not duplicate those results or
replace #324's localized-moment addendum. It uses an ADDITIONAL quantitative input:
SH's tail for the analytic critical-count cap. The preceding chat derived a
logarithmic improvement but did not publish or execute it; this packet supplies
full source bindings, a dyadic exact-control sharpness family and finite tests.

SH's cap statement precedes its later use of G_d/I5 to assemble factorial moments.
The proof of LT below does not consume that first-moment assembly or C6 Palm
Theorem Q. This is a dependency distinction at the quoted interface, NOT a new
independent proof of SH's cap, its multidimensional Rouche/Bezout, covariance,
complexification or protected-cover premises. Their exact stated scope and
unresolved ancestral qualifications remain. No old author-side header, merge or
green workflow is converted into independent mathematical acceptance here.

All SH first-moment theorem qualifications remain in its source; only the cap-tail
interface is imported. A defect in that tail invalidates its use below. P's
congruence explanation is not used as a new equality: only the quoted uniform
moments and full-normalizer estimate are consumed. No inverse-Hessian bound or
extra soft-sector normalizer is introduced.

## 2. Setting and statement

Fix d>=3, torus side L>0, observation radius R>=1, a compact birth interval and
compact positive gap marks 0<k_-<=k<=k_+. Frames range over O(d), with uniform
constants on that compact set. The field, pins, open between-pin height window,
typed maximum/saddle weight W_r, original Gaussian pin law Q_r and normalizer
Z_r=E_Q W_r are EXACTLY those of FR and P. Write

    P_r=Q_r^W,     D_r=W_r/Z_r,     dP_r=D_r dQ_r.

Here D_r is a density, not a determinant or a derivative. N counts all critical
points in the between-pin window on the torus, pins removed. N_R counts the
subset in the Rr-ball. SH supplies a measurable Psi dominating the TOTAL critical
count, so 0<=N_R<=N<=Psi. Its cover is fixed independently of r and of the soft
thresholds. Use FR's C4 norm control K>=1; do not identify this K with another
source's differently named cover radius, derivative constant or gap interval.

For 1<=q<=d-2, let h_j be FR's ordered eigenvalues of the negative midpoint
transverse Hessian. Choose deterministic ordered thresholds

    0<=eta_2<=...<=eta_(q+1)<=1/2,     0<r<=1/2.

Define

    S={h_j<=eta_j for 2<=j<=q+1},    E={N_R>0} intersect S,
    Xi=product_(j=2)^(q+1)(eta_j+r)^(j+2),
    beta=q(q+7)/2.

Then r^beta<=Xi<=1. Midpoint eigenvalues may be negative, zero thresholds are
allowed, no unmentioned lower bound on other eigenvalues is assumed, and q=d-2
includes the all-soft transverse case. FR-mixed states, for each fixed a>=0,

    E_(P_r)[K^a 1_E] <= C_a r^3 Xi.                    (F)

For sufficiently small r put

    u=log(1/r),      Lambda(r)=u/log u.

**Theorem LT.** Conditional on the quoted interfaces, for every fixed a>=0 and
s>0 there are C<infinity and r_*>0 such that throughout the fixed parameter set,

    E_(P_r)[K^a N^s 1_E]
       <= C r^3 Xi Lambda(r)^(d s),                   (LT)
    E_(P_r)[K^a N_R^s 1_S]
       <= C r^3 Xi Lambda(r)^(d s).                   (LT-local)

Constants can depend on a,s,q,d,L,R, the fixed cover and the compact marks; no
numerical field constant or radius is evaluated. This is full soft POWER with a
logarithmic penalty, NOT the constant loss-free estimate O(r^3 Xi).

## 3. Proof: a cutoff and four-factor Holder under the original law

### 3.1 Exactly the moments and tail used

SH(5.1) gives constants c,C0,x0>0, uniform in the stated pin parameters, with

    Q_r(Psi>x)<=C0 exp[-c x^(1/d) log x], x>=x0.        (T)

It implies uniformly bounded E_Q Psi^t for every fixed t>0 by tail integration.
P(4.1) gives the same fixed-order moment property for K. P(5.3)'s following
moment statement and (5.5) give

    ||D_r||_(L4(Q_r))
      = ||W_r/r^2||_4 / (Z_r/r^2) <= C.               (M)

In particular E_Q K^(4a) and E_Q Psi^(4s) are bounded. All these orders are
FIXED, independent of r. No joint independence or joint conditional moment
estimate is assumed. The density has integral1 and the full Z is used once.

### 3.2 Charge both sides of the cutoff

For any T>=max(1,x0), split the nonnegative expectation at Psi=T. Since N<=Psi,

    E_P[K^a N^s 1_E; Psi<=T]
      <= T^s E_P[K^a 1_E] <= C_a T^s r^3 Xi.           (1)

For the other branch, drop E and return to Q:

    E_P[K^a N^s 1_E; Psi>T]
      <= E_Q[D_r K^a Psi^s 1_{Psi>T}]
      <= ||D_r||_4 ||K^a||_4 ||Psi^s||_4
                            Q_r(Psi>T)^(1/4)
      <= C_(a,s) exp[-(c/4) T^(1/d) log T].            (2)

The four conjugate reciprocal exponents sum to1. The quarter in (2) must be
retained when selecting the cutoff. No separate count-moment theorem, random
matrix inverse, witness conditioning or uncharged exceptional branch appears.

### 3.3 A uniform cutoff and tail absorption

Take A>=max(1,4(beta+4)/c), fixed, and

    T=A^d (u/log u)^d.

Reduce r_* so u>=e^2 and T>=max(1,x0). If t=log u>=2, then log t<=t/2: the
function t/2-log t is positive at2 and nondecreasing for t>=2. Thus

    log T=d(log A+log u-loglog u)>=(d/2)log u>=log u,
    T^(1/d) log T >= A u.

The last inequality uses d>=2; our field application has d>=3. Consequently

    exp[-(c/4)T^(1/d)log T]
       <= exp[-(beta+4)u]=r^(beta+4)<=r^3 Xi.           (3)

The last step uses Xi>=r^beta and r<=1. At eta_j=0 it remains valid; there is
no missing diagonal layer. Since T^s=A^(ds)Lambda(r)^(ds) and Lambda(r)>=1,
adding (1)–(3) proves LT. For s>0,

    N_R^s 1_S=N_R^s 1_E<=N^s 1_E,

which proves LT-local. For s=0 use FR directly with the NONEMPTY event E; do not
reinterpret N_R^0 1_S as that event. This completes the ordinary proof.

## 4. Consequences and comparison with the recorded fixed-order bound

For eta_j=r^alpha_j with fixed alpha_2>=...>=alpha_(q+1)>0, set

    B=sum_(j=2)^(q+1)(j+2)min(alpha_j,1)>0.

The same finite-r saturation as FR gives

    E_P[K^a N_R^s 1_S]
       =O(r^(3+B) Lambda(r)^(ds))=o(r^3).             (4)

Examples at eta_j=r:

| d | q | count power s | bound |
|---|---|---|---|
| 3 | 1 | 1 | O(r^7 Lambda^3) |
| 3 | 1 | 2 | O(r^7 Lambda^6) |
| 4 | 2 | 1 | O(r^12 Lambda^4) |

With the CT interface additionally assumed at one fixed integer p>s, the two
separately proved estimates may be combined:

    E_P[K^a N_R^s 1_S]
      <= C r^3 min{Xi^(1-s/p), Xi Lambda(r)^(ds)}.      (5)

The first estimate can be better for very slowly shrinking thresholds. LT ALONE
does not show negligibility for every deterministic Xi->0; one needs
Xi Lambda^(ds)->0. CT supplies the broader qualitative statement under its own
inputs. We do not send p to infinity or claim constants uniform in p.

For each fixed integer s>=1, (N_R)_s<=N_R^s. Therefore deleting configurations in
S from the r^-3-rescaled positive ordered-s-tuple intensity changes its total
variation mass by at most C Xi Lambda^(ds), with the same K^a-weighted upper bound
for tuple observables bounded by K^a. The convention is total mass for a positive
measure, not half the L1 norm of probabilities. This concerns only the deleted
sector. There is no assertion of a full point-process limit, location density,
normalized factorial Palm law, local nonempty lower bound or elder selection.

## 5. Sharpness for the NUMERICAL interfaces, not for the actual field

The logarithmic factor cannot be replaced by o(Lambda^(ds)) solely from the event,
density-moment and cap-tail inequalities used above. The following one family
works for every fixed count order simultaneously. A sequence r_j suffices to
refute any proposed uniform inequality; a continuous interpolation is unnecessary.

Fix d>=3. For integers j>=2 put

    n=2^j, r_j=2^(-n), v_j=floor(n/j)>=2, M_j=v_j^d.

On an abstract three-atom probability space set Q_j=P_j. The ordinary atom has
probability r_j^3 and count N_R=N=2. The rare atom has probability r_j^7 and
count N_R=N=M_j. The remaining probability 1-r_j^3-r_j^7 has count0.
Set W_j=r_j^2, Z_j=r_j^2, D_j=1, K=3 and Psi=N+2. These give a normalized
density and all required W/r^2 and K moments. Set h_1=r_j/2 throughout; h_2=r_j
on the rare atom and h_2=2 otherwise. For d>3 take h_3=...=h_(d-1)=3.
These are abstract ordered marks, not an actual field Hessian or derivative norm.

### 5.1 Event bounds for EVERY threshold

For q=1 and every eta in [0,1/2], E={N_R>0,h_2<=eta} is empty if eta<r_j and
consists only of the rare atom otherwise. Hence

    E_P[K^a 1_E] <= 3^a r_j^3 (eta+r_j)^4.

This holds for all a>=0. For q>=2 the extra mark h_3=3 makes E empty throughout
the allowed thresholds. Thus no untested off-diagonal threshold is hidden.

### 5.2 Uniform cap tail with an explicit numerical constant

At t>=4 the ordinary cap value4 and the zero-count cap value2 contribute nothing
to {Psi>t}. The tail is either0, or exactly r_j^7 when t<M_j+2. In the latter case,

    t^(1/d)<=v_j+1<=3v_j/2,
    log t<=d log(v_j+1)<=d(j+1)log2,

using M_j+2<=(v_j+1)^d. Since v_j<=n/j and j>=2,

    t^(1/d)log t <= (3/2)d n[(j+1)/j]log2
                  <=3d n log2.

Therefore, for every j>=2 and t>=4,

    Q_j(Psi>t) <= exp[-(1/d)t^(1/d)log t],             (6)

because its nonzero value is exp[-7n log2]. Thus (T) holds with C0=1,c=1/d,x0=4,
not just a vaguely fitted tail. All fixed Psi moments consequently are uniformly
finite. Also, for each fixed real p>0,

    E[N^p]/r_j^3=2^p+2^(-4n)v_j^(dp)<=C_p.

The final boundedness follows from exponential decay against any fixed polynomial;
all factorial upper bounds follow. Even an added global first/second lower scale
holds: P(N_R>0)>=r_j^3 and E[(N)_2]>=2r_j^3.

### 5.3 Match the logarithmic order

At eta=r_j,

    E[N_R^s;S]/[r_j^3(2r_j)^4]=v_j^(ds)/16.           (7)

Now Lambda(r_j)=n log2/(j log2+loglog2). The elementary inequalities
1/2<log2<1 imply, for j>=2,

    n/j <= Lambda(r_j) <= 2n/j,
    n/(2j) <= v_j <= n/j.

Hence Lambda(r_j)/4<=v_j<=Lambda(r_j), and (7) lies between
4^(-ds)Lambda(r_j)^(ds)/16 and Lambda(r_j)^(ds)/16. It is not
O(1) and not o(Lambda(r_j)^(ds)). The same model works for each fixed s>0.

This establishes numerical-interface sharpness. It does NOT instantiate the
periodic Gaussian law, density on Hessian space, analytic sample paths, Rouche
construction of Psi, independence of a Gaussian residual or geometric relations
between N and K. Those structures might imply a stronger result for the actual
field. A uniform joint sector-conditioned count estimate would be additional
information, not a consequence of this abstract bound. No actual-field lower
asymptotic or impossibility theorem is claimed.

## 6. Finite controls, execution and review boundaries

`test_log_cap.py` exercises12 exact finite methods against `log_cap_check.py`.
The initial missing-implementation run produced12 assertion failures and no test
errors. The companion uses Fraction/integer arithmetic only. It checks mixed
powers, the tail quarter/cutoff coefficient, a dyadic sharpness family, correlated
four-factor Holder cases, the event-retaining truncation, one normalizer, zero
threshold absorption, remote-only exclusion, and elementary factorial domination.
It does NOT evaluate log at floating precision or numerically certify a Gaussian
constant; the transcendental cutoff and infinite limits are the written arguments.

Five intentional wrong variants must fail for their intended assertion reasons:
M1 omits the cutoff's Holder-quarter compensation; M2 uses (d-1)s rather than ds;
M3 drops the common radial r^3; M4 removes the divisor j in the spike scale;
M5 drops the full normalizer. Unexpected exceptions are errors, not mathematical
rejections. Normal/optimized results and exact source identities are recorded in
separate receipts. The original failures remain preserved.

Smallest nonauthor review: quoted law/scope alignment, (M), four-factor bound(2),
cutoff and absorption(3), plus ALL-threshold/event/tail and order comparison in
section5. Check the optional CT premise in(5) rather than conflating it with LT's
inputs. The whole numerical-interface countermodel must remain explicitly
non-Gaussian. No duplicate review of P/FR/CT ancestors is requested.

General IBA2-012 and IBA2-009, escaping marks or observation radius, higher-jet
sector exhaustion, remote-only events, lifetime integration, actual conditional
count law, full process convergence, independent formal alignment and scientific
acceptance remain outside this note. No source from #319/#324 is rewritten.
