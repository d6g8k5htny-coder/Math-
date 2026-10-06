# IBA2-012: a sector-size logarithmic transfer from the marked Fourier moment

Object: IBA2-MARKED-SECTOR-20261006-R8-v1.
Dylan Roy — delegated AI research. Actual performer: OpenAI / GPT-6 Astra Pro,
original continuation `iba2-marked-entropy-audit-20261006-r8`; publication continuation
`iba2-marked-sector-publication-20261006-r9`, pickup main#259/6008806185.
**Author-side conditional publication candidate; nonauthor review required.**
Author-exposed to the FR/CT/log-cap work and its reviews; organizational credit 0.
Scientific effect NONE. No repository proof, historical review or status changes.

## 1. Provenance and the input missed by the preceding comparison

This note does not re-publish #319's count-transfer theorem, #324's localized
factorial-moment lemma, or #327's original-law analytic-cap truncation. Those are
credited predecessors with their own hypotheses and reviews. Their bounds remain
valid at their stated scope. In particular #327's numerical-interface sharpness
claim is relative to ITS cap-tail inputs, not to every theorem in the repository.

A stronger, previously published INPUT is already present in #157: a marked
Fourier estimate at the rare r^3 scale. The purpose of this proposal is to use
that existing estimate together with FR, rather than assert a new Fourier or
Kac–Rice theorem. General inequalities used below are elementary; no literature
novelty claim is made.

The quantitative inputs were read at Math- source cut
`39c10a4bb6a670b12aed47c13cba43f846b61baa`:

| Tag | Path | Full Git blob | Consumed interface |
|---|---|---|---|
| FR | `reviews/iba2_012_finite_radius_20261005/PROOF.md` | `5ed684c9bb446efc9bef5f3980717c6dc039abfd` | Sections 3 and 8: the same-law mixed soft-sector event bound with fixed derivative powers |
| MF | `frontiers/c6_marked_fourier_20260929/PROOF.md` | `efb702f601eb0c0a24dad6d125061158158867b9` | Section 1 (MF1) and its exact law, fixed-parameter scope and dependency qualifications |

Full direct source bytes are included under sources/ in the retained R8 offline
delivery, not duplicated in this five-file repository packet. Git and SHA-256 identities were checked
locally after recovering the bytes from dated retained archives, and compared with
native current-source identities. Recovery from an older archive is not an older
proof version when the complete Git blob is equal. MF's original author-side header
is preserved; #157's native PR records its scoped analytic reviews and integration.
Those reviews are not new reviews of this proposal. MF's conditional/regional
proof ancestry remains a premise, including its source-exposed review limitations.
No ancestor's scope is improved by this new use.

For comparison only: CT proof blob752bc9da5e49af3d0724d80c91cffc0dde35a2d8
(#319), localized note9dd7d583e50336aea6e0625d57dffabc50ed4f3e (#324), and
log-cap note b158965faf0f4113309d825ce1892743910fc028 (#327 head e71fd6ecd59071181d4e476d0e4e87287d4488b1).
None of those three is a quantitative premise of the generic lemma below.

Publication reconciliation: both quantitative inputs retain these exact blobs at
`516235290e12decdcd223cfb20928a2d97b824f1`. Sections 2–5 below are byte-identical
to the retained local proposal. Its original NOTE blob was
`be56eb758eb9ae0091def24a5a176659188ce281`; the immutable R8 ZIP has SHA256
`b7416404ec7a1627251f902ea99da493a376ced40390b4204675100b5dbb8ee3`.
The source and proof are not credited as another new derivation at publication.

## 2. Generic lemma and an explicit constant

Let P be ONE probability measure. N is a nonnegative integer-valued random
variable, K>=1, and E is a measurable event. Fix gamma>0, theta>0, rho>0,
0<Xi<=1, a>=0 and s>0. Assume the following numerical interfaces, with constants
independent of rho and Xi in the parameter family:

    E_P[N exp(theta N^gamma)] <= B rho,                 (M)
    E_P[1_E] <= A0 rho Xi,
    E_P[K^(2a) 1_E] <= A2a rho Xi.                     (F)

The product N exp(theta N^gamma) is zero at N=0. The marked moment in (M)
is NOT an assertion that E exp(theta N^gamma)=O(rho); the latter has a zero-count
contribution and usually cannot vanish at the rare-event scale.

Put L=log(e/Xi)>=1. For u>0 set

    k_u = max(0,ceil((u-1)/gamma)),
    H_u = k_u! (2/theta)^k_u,
    c_u = max(1,(2/theta)^(u/gamma)),
    C_u = A0 c_u + B H_u.

Then

    E_P[N^u 1_E] <= C_u rho Xi L^(u/gamma),             (S)
    E_P[K^a N^s 1_E]
        <= sqrt(A2a C_(2s)) rho Xi L^(s/gamma).         (MT)

Only the two event moments in (F) are required. The statement allows arbitrary
correlations between N,K,E. Constants are fixed, and no moment order depends on
rho or Xi. The case a=0 is included; (S) at u=s then gives a direct alternative
constant. For s=0 use (F) at the relevant event moment, rather than turn a local
zero-count outcome into a nonempty event. Xi=0 need not be assigned a logarithm:
(F) would make E null; the displayed expression has continuous limiting value 0.

### Proof of (S)

Choose

    T = max(1,(2L/theta)^(1/gamma)).

Then T^u<=c_u L^(u/gamma) and theta T^gamma/2>=L. The low-count contribution is

    E[N^u; E,N<=T] <= T^u P(E)
                    <= A0 c_u rho Xi L^(u/gamma).      (1)

For x>=1, x^(u-1)<=x^(gamma k_u), including u<=1 with k_u=0.
The exponential series gives, for y>=0,

    y^k exp(-theta y/2) <= k! (2/theta)^k.

Consequently x^(u-1)exp(-theta x^gamma/2)<=H_u for x>=1. On N>T>=1,

    N^u <= H_u N exp(theta N^gamma)
                     exp(-theta T^gamma/2).

Integrating, discarding E only in this tail term, and using (M) yields

    E[N^u; E,N>T] <= B H_u rho exp(-L)
                    = B H_u rho Xi/e.                 (2)

Adding (1) and (2), and using L>=1, proves (S) with the stated slightly enlarged
constant C_u. No full-field cap, independence or additional normalizer was used.

### Proof of (MT)

Cauchy–Schwarz is applied on the SAME event and probability law:

    E[K^a N^s 1_E]
      <= E[K^(2a)1_E]^(1/2) E[N^(2s)1_E]^(1/2)
      <= sqrt(A2a C_(2s)) rho Xi L^(s/gamma).

Both squared factors contain rho Xi. Therefore the final result contains rho Xi,
not rho^(1/2), Xi^(1/2), or a second factor of the endpoint normalizer. The use
of FR at 2a, not merely a, is explicit. This completes the proof.

## 3. Exact-field application and improvement in scope of thresholds

Fix d>=3, torus side L_torus>0, an observation radius R>=1, compact birth heights,
and a strictly positive compact gap interval [k_-,k_+] with k_->0. Frames vary on
the same compact orthogonal group. Take the minimum of the FR and MF small-radius
cutoffs and 1/2. All constants may depend on these fixed data, a and s.

Under P_r=Q_r^W, both sources use the identical variance-one periodized Gaussian
field, maximum/saddle value-and-gradient pins, typed endpoint product W_r and
FULL endpoint-only normalizer Z_r. There is no separately normalized sector law.
N is MF's all-index torus-wide count in the open between-pin height interval,
pins excluded. N_R is FR's local count, so 0<=N_R<=N. K is FR's fixed C4 norm
control. No derivative variable from a witness kernel is substituted for this K.

For 1<=q<=d-2 choose deterministic ordered thresholds
0<=eta_2<=...<=eta_(q+1)<=1/2. Let h_j be FR's ordered negative midpoint transverse
eigenvalues, possibly nonpositive at finite r, and define

    S={h_j<=eta_j for 2<=j<=q+1},
    E={N_R>0} intersect S,
    Xi=product_(j=2..q+1)(eta_j+r)^(j+2).

Then 0<Xi<=1. FR supplies (F) at powers0 and2a with rho=r^3.
MF1 supplies (M) with gamma=2/d, some FIXED theta>0, and the SAME rho=r^3.
Applying (MT) gives the candidate field corollary

    E_(Q_r^W)[K^a N^s; E]
      <= C r^3 Xi [log(e/Xi)]^(d s/2),                 (MT-field)
    E_(Q_r^W)[K^a N_R^s; S]
      <= C r^3 Xi [log(e/Xi)]^(d s/2).

The second line uses s>0 and N_R^s 1_S=N_R^s 1_E. It does NOT license
E[N^s;S] on remote-only outcomes where N_R=0. Zero thresholds and all-soft transverse
matrices are included exactly through FR. No inverse Hessian moment is added.

Unlike a cutoff selected only by r, this cutoff is selected by Xi. Thus ANY
admissible deterministic thresholds with Xi(r)->0 yield o(r^3), because
x log(e/x)^c ->0 for every fixed c>0 as x decreases to0. In particular arbitrarily
slow shrinking thresholds are covered, not just power-law ones. It suffices for
one factor of Xi to tend to0 while the other factors remain bounded.

At eta_j=r^alpha_j, alpha_2>=...>=alpha_(q+1)>0, put
B_soft=sum_(j=2..q+1)(j+2)min(alpha_j,1). Then

    MT-field = O(r^(3+B_soft) [log(1/r)]^(d s/2)).       (3)

The full soft POWER is retained, with a sector-size logarithmic penalty.
It is not O(r^3 Xi) with a constant penalty. At equal thresholds eta_j=r,
B_soft=q(q+7)/2. Examples:

| d,q,s | Bound |
|---|---|
| 3,1,1 | O(r^7 [log(1/r)]^(3/2)) |
| 3,1,2 | O(r^7 [log(1/r)]^3) |
| 4,2,1 | O(r^12 [log(1/r)]^2) |

For Xi=(log(1/r))^(-kappa), kappa>0, the normalized deleted contribution is
O((log(1/r))^(-kappa) [loglog(1/r)]^(d s/2)), which tends to0 for every kappa>0.
This example is stated at the Xi level; the thresholds must still obey FR's
order and range. It is realizable, for example by equal thresholds chosen so
Xi equals that value for sufficiently small r.

### Comparison, not invalidation, of the predecessor results

CT's fixed moment p>s gives r^3 Xi^(1-s/p). For any fixed epsilon>0,
Xi log(e/Xi)^(d s/2) = o(Xi^(1-epsilon)). Thus MT is stronger asymptotically
as Xi->0, but imports MF1, a stronger marked theorem, rather than just fixed moments.

The #327 log-cap result gives r^3 Xi [log(1/r)/loglog(1/r)]^(d s). At a power-law
sector the ratio of the new penalty to that one tends to0. This does not refute
#327's sharpness relative to its DIFFERENT numerical inputs. MF1 contains the
additional rare-scale marked tail information that its abstract cap-tail model
was not required to satisfy. No claim of unconditional improvements to the
underlying field, all-mark uniformity, or fewer inherited MF proof obligations
is made.

## 4. Polynomial observables and local tuple measures

For a fixed integer j>=1, (N_R)_j<=N_R^j. Therefore an r^-3-scaled expected
positive measure of ordered distinct local j-tuples changes, upon deleting S,
by total mass at most

    C Xi [log(e/Xi)]^(d j/2).                          (4)

The same bound applies to signed tuple functions bounded by K^a, via absolute
expectation. The variation convention is the total mass of a positive measure,
not half the L1 norm for probability measures. It provides deletion stability
of an existing limit, not existence or uniqueness of the whole spatial limit.
Fixed polynomial positive-count intensity norms follow as well, with the
constant term attached to the nonempty event. Factorial degrees stay fixed.

Local-nonempty conditioning and factorial size-biased laws still need their
own lower denominators. This argument creates no lower bound at orders>=3,
no local occurrence lower bound and no elder matching or lifetime integration.

## 5. Sharpness for the numerical interfaces, not the actual Gaussian field

Fix any integer d>=3 and s>0. One abstract family suffices for all moment powers.
For integer j>=2 set

    r_j=2^(-j^2), rho_j=r_j^3, K=1,
    ordinary atom: probability rho_j, N=N_R=2, h_2=2,
    rare atom: probability r_j^7, N=N_R=j^d, h_2=r_j,
    remaining atom: the rest of the probability, N=N_R=0, h_2=2.

Set h_1=r_j/2. This is the q=1 sector. For every allowed threshold eta,
E={N_R>0,h_2<=eta} is empty below r_j and otherwise the rare atom. Hence

    E[K^t;E] <= rho_j(eta+r_j)^4

for ALL thresholds and ALL fixed t, not only the diagonal. The probabilities
are positive and sum to1. If desired use Q=P and W=Z=r_j^2 to represent an
abstract single normalized weight; it is not an endpoint Hessian product.

Take gamma=2/d and theta=log2. On the rare atom N^gamma=j^2, so

    rho_j^-1 E[N exp(theta N^gamma)]
      <= 8 + j^d 2^(-3j^2) <= 8+d! 2^(d-1).           (5)

The last bound follows from
j^d<=d! binomial(j+d-1,d)<=d!2^(j+d-1) and j-3j^2<=0.
The ordinary bound8 uses 2^(2/d)<=2 for d>=2. Thus the SAME fixed positive
marked exponent works uniformly along the family. It implies every fixed
polynomial/factorial moment bound as well; these are not separate models.

At eta=r_j, Xi=(2r_j)^4, and

    E[N_R^s;S]/(rho_j Xi) = j^(d s)/16.                (6)

Put L_j=log(e/Xi)=1+(4j^2-4)log2. Since 1/2<log2<1 and j>=2,

    j^2 <= L_j <= 4j^2.

Consequently

    1/(16*2^(d s))
       <= E[N_R^s;S]/(rho_j Xi L_j^(d s/2)) <= 1/16.   (7)

No penalty of smaller order than log(e/Xi)^(d s/2) is uniformly deducible from
(M),(F) alone. In particular a constant loss-free bound does not follow even
from MF1's quantitative marked moment. This is an abstract count/mark model,
NOT a Gaussian field, covariance, smooth sample path or Hessian realization.
It proves optimality of an inference from numerical estimates, not an actual
field lower asymptotic. A better true-field result must use further geometric
information, such as the separate sector-conditioned count estimates previously
identified; it is not ruled out here.

## 6. Verification and release boundary

The accompanying standard-library helpers and 15-method suite are finite
Fraction/integer controls. They include correlated-mark Cauchy–Schwarz,
polynomial tail domination, exact marked-budget powers, all-threshold spike
mass, sharp ratios, tuple counting, zero-count normalization and invalid domains.
All baseline and mutation processes are separately captured under evidence/.
There are no pip dependencies, network calls, local-model calls, or Lean calls.
The proof is the general argument above, not an extrapolation from those tests.

Nonauthor review is REQUIRED before any acceptance. The targeted review is:
(1) the constants and marked rather than unmarked tail in section2;
(2) exact shared law and derivative order2a in section3;
(3) comparison of input strengths without claiming ancestor independence;
(4) every-threshold uniform marked budget and sharpness in section5;
(5) scopes of local deletion versus normalization/whole-process conclusions.

This publication succeeds the local-only R8 proposal after write access returned.
The former no-write observation remains in the sealed predecessor report; it is
not a current publication limitation. The two Python source files are unchanged.
Actual replay, native Git identities and a nonauthor review belong in the linked
PR receipts; a green existing-core workflow does not prove this note or silently
run its standalone suite. No self-merge or scientific-status promotion is allowed.
The separate FR+SH+P growing-order concentration scope (main#259/6008758240) stays
with its owner; this note covers fixed powers using the stronger MF input.
General IBA2-012/IBA2-009, k->0, growing R,d,L, hard-Hessian higher jets,
remote-only sectors, full cluster-law convergence, elder/lifetime matching,
independent alignment and physical-laptop readiness remain open.
