# Marked Fourier cap: exponential-power control of rare critical-point clusters

Object: OA-C6-MARKED-FOURIER-20260929-v1.1 (publication successor).
Author: OpenAI / ChatGPT. Date: 29 September 2026.
Disposition: AUTHOR-SIDE CANDIDATE; NONAUTHOR ANALYTIC REVIEW REQUIRED.
Scientific effect NONE. This note changes no source, review, graph, register or prize.

## 1. Exact model and proposed strengthening

Use precisely the original variance-one periodized Gaussian field, fixed dimension
`d>=2`, fixed torus side `T`, compact birth and positive-gap marks with `k>=k_->0`,
and original maximum/saddle value-and-gradient pins of sources F and P below.
The original endpoint-conditioned law is Q_r, the typed determinant weight is
W_r, and the full endpoint-only normalizer is Z_r. Write Q_r^W=(W_r/Z_r)Q_r.
N counts additional all-index critical points in (b-kr^3,b), excluding both pins.
No random observation set, changing dimension, vanishing gap floor, or additional
normalizer is introduced.

Source F provides a Borel functional Psi_F of the FULL field, constructed from
Fourier truncation and successful Rouche radii, which bounds its total critical
count. Source P provides canonical Gaussian witness kernels, the witness-excluded
annulus geometry, the joint-frame floors, and the regional marked Kac--Rice
estimates. This note must extend F under those witness kernels; F's unconditional
tail by itself is not enough.

**Proposed theorem.** There are theta>0, C<infinity, and r_*>0 such that, uniformly
on the stated fixed compact family,

    E_{Q_r^W}[ N exp(theta N^(2/d)) ] <= C r^3,     0<r<=r_*.       (MF1)

All constants are existential and may depend on d,T and the mark compacts.
In d=2 this is an exponential cluster-size moment. In d>2 it is stretched
exponential with exponent 2/d, NOT an ordinary exponential moment.

With the accepted additional-point lower event (P's source EDL), P(N>=1)>=c r^3.
Consequently both of the following are uniformly bounded:

    E[exp(theta N^(2/d)) | N>=1],
    E_sizebiased[exp(theta N^(2/d))],
    dP_sizebiased = N dQ_r^W / E_{Q_r^W}N.                         (MF2)

These two probability laws are different. The theorem does not claim equality
or independence of their marks. Also

    P(N>=n) <= C r^3 n^(-1) exp(-theta n^(2/d)),  n>=1.             (MF3)

This is a new proposed quantitative strengthening of the source's fixed-order
moment conclusions, not another acceptance of the source theorem.

## 2. Source identities and dependencies

F: `frontiers/c6_fourier_cutoff_20260929/PROOF.md`, on Math- main
`e1ca400b3414e5a7bec13b91bc4f1e5293df32be`, Git blob
`1d9177a259654df0fb7c558fcb803685e09608d2`, SHA256
`c1692379a3a066589bd2522aaa5b4d480e736b737c8c39a474d1735185793733`.
Consumed: conditioned Fourier-coefficient method, fixed cover, local exponential
coordinate injectivity, isolated-zero Bezout and the successful-frequency cap.
The unconditioned Fourier tail is not assumed to hold under a witness kernel.

P: `frontiers/c6_palm_route_20260929/PROOF.md`, merged by PR145 at
`820d4435c5f13c12b9c2f3590e859212d2648dc0`, Git blob
`89eb8adf08fe7afc2cab9662d3a9875c05ae5cc5`, SHA256
`aa37f16040ab9e05bb2e4e3f1d678367497e8dc2cf43eef197a4d6592c2f129b`.
Consumed: Sections 4.1--4.4 definitions and witness slab; Section 5 canonical
kernel / nonnegative Borel field-mark formula; Section 6 joint floors and
regional determinants/density bounds; EDL only for the lower probability used
in MF2. Its mathematical Sections 3--7 are the source-reviewed successor;
the PR was open during the earlier local draft but is now merged. The proof blob
is unchanged from the originally read `78ac1100217279e7b692f0959f86eee34cd1910e`.
The exact landed dependency and its source map are verified by this packet workflow.

G: the dimension-matched first-moment source was integrated by PR141 at the
above main commit; P binds its proof blob `9d82c707fdb17d3072a8930f26dabedf59e456fc`.
The marked argument below uses P's REGIONAL proof, not merely G's small mean.

Prior-result credit: the independently reviewed and merged #153 packet
`frontiers/c6_rare_cluster_laws_20260929/PROOF.md`, blob
`2ab625cedfc2e47575c4a7fa4853413418c532da`, already supplies the independent-replica
and polynomially weighted compactness consequences from fixed-order moments.
Section 7 repeats the elementary replica proof for self-containment, not priority.
The new contribution there is exponential-power weighted compactness; MF1 is NOT
inferred from #153's finite-moment hypotheses or its ordinary TV bounds.

This note is exposed to the earlier OpenAI work and reviews. An actual nonauthor
review of the new conditional Fourier argument and its exponential-mark insertion
is still required. No new theorem is inferred just from the supplied programs.

## 3. Fourier coefficients under the actual witness regression

Fix a witness kernel Q'=Q_r(. | Lambda=tau), where Lambda is one of P's regional
frames with invertible covariance Sigma, and let d_tau=tau-E_Qr Lambda. Put

    beta = sqrt(sum_i Var_Qr Lambda_i) ||Sigma^(-1)|| |d_tau|.

For a real component c_n of the Fourier coefficient, let a_n be its prior
variance scale. Source F and bounded original pin-regression energy give
|E_Qr c_n|<=C sqrt(a_n), and Var_Qr(c_n)<=C a_n.
The EXTRA regression correction obeys

 |Cov_Qr(c_n,Lambda) Sigma^(-1)d_tau|
 <= sqrt(Var_Qr c_n) sqrt(sum_i Var_Qr Lambda_i)
                         ||Sigma^(-1)|| |d_tau|
 <= C sqrt(a_n) beta.

Hence |E_Q'c_n|<=C sqrt(a_n)(1+beta), while Var_Q'c_n<=C a_n by projection.
For every fixed p, ||c_n||_{L^p(Q')}<=C_p sqrt(a_n)(1+beta). Real/imaginary parts
are treated separately; they need not be conditionally independent.

Let P_m be the gradient of the frequency-m truncation of the FULL realized
field, in its fixed torus lattice. On the same fixed complex tube as F, Gaussian
spectral decay and Minkowski therefore give constants a>0,C independent of the
particular regional kernel such that

 E_Q' R_m^2 <= C(1+beta^2) exp(-4a m^2),
 E_Q' L^2   <= C(1+beta^2),                                      (MF4)

where R_m=sup|grad f-P_m| and L is the fixed-annulus supremum of its derivative.
The frequency truncation is not a new pinned field. Only the original field
is used by N,W,Z, by the kernel, and by the conditional covariance floors.
The conditional MEAN is included in MF4; omitting it would invalidate the result.

## 4. Witness-excluded Fourier tail

Retain exactly the Psi_F of F, independent of which witness is being integrated.
Its definition allows all test radii in each interval [eta_j,2eta_j]. At a fixed
witness X, remove the slab of radii within zeta_0 of its local periodic lift's
distance from the centre, as in P. The actual cover has zeta_0<=eta_j/8. Failure
of the ORIGINAL cap test at all radii implies failure on this retained subset.
Thus one does not define or insert a different witness-dependent mark.

Let Phi=max(1,phi^(-1/2)) with phi the infimum of det Cov_Q'G on the protected,
witness-excluded annuli, G=(Re grad f, Im grad f/t). All following bounds are
vacuous if phi=0; P's regional lemmas supply positive floors where used.
P's small-gradient volume bound reads, for small h,

 E_Q' Vol{ |grad f|<=3h in retained annuli }
       <= C Phi h^(2d)(1+log(1/h)).                            (MF5)

Take h_m=exp(-a m^2), lambda_m=exp(a m^2/(4d)), and delta_m=h_m/lambda_m.
For all m above a FIXED geometric threshold, delta_m<=eta_j/8 and <=zeta_0/2.
On R_m<=h_m and L<=lambda_m, failure on every retained radius yields separated
open balls in the sublevel set. Their number is at least c eta_j/delta_m.
P's corrected packing gives volume at least c eta_j delta_m^(2d-1).
Mean-volume Markov and MF4 consequently bound the three failure contributions by

 C Phi (1+a m^2) exp[-a(2d+1)m^2/(4d)],
 C(1+beta^2) exp(-2a m^2),
 C(1+beta^2) exp[-a m^2/(2d)].                                  (MF6)

Absorb the fixed polynomial by reducing the rate. With A=1+beta^2+Phi>=1,

 Q'(k_j>m) <= C A exp(-c m^2),
 Q'(Psi_F>x) <= C A exp(-c x^(2/d)), x>=0,                       (MF7)

after constants absorb finitely many small cutoffs. No monotonicity of success
at the individual frequency m is assumed; 'success by m' is the finite union
used by F. The source's zero-count cap is pathwise, so no new analytic zero-set
or generic-coefficient hypothesis has entered.

Set alpha=2/d and Y=Psi_F^alpha. From MF7, for 0<u<c,

 E_Q' exp(uY)
 = 1 + integral_0^infinity u exp(ut) Q'(Y>t)dt
 <= 1 + C A u/(c-u) <= C_u A.                                  (MF8)

The prefactor A is retained. A uniform exponential moment without this prefactor
has NOT been proved for arbitrary witness regressions.

## 5. The exponential mark uses the same regional absorption

Choose theta>0 with 2theta<c, uniformly in the original compact family.
Pathwise N exp(theta N^alpha)<=N exp(theta Psi_F^alpha). Apply P's canonical
nonnegative Borel marked Kac--Rice formula with mark

    Xi(f)=W_r(f) exp(theta Psi_F(f)^alpha).

On each compact puncture all kernels are the explicitly chosen Gaussian
regression kernels. The mark is a Borel function of the FULL field: finite
Fourier coefficients are continuous real-field functionals; the analytic
extensions and successful-radius tests are measurable limits and countable
unions. Set the cap to infinity off its measurable convergence set; that set's
complement is null under every kernel used, by MF4--MF7. Use increasing truncated caps to define the product, so it is zero when W_r
is zero even on the exceptional infinite-cap set. Nonnegative truncation and
monotone convergence allow the unbounded mark.

The conditional insertion is

 E_Q'[W_r F_j(H_X) exp(theta Psi_F^alpha)]
 <= E_Q'[(W_r F_j(H_X))^2]^(1/2)
                      E_Q'[exp(2theta Psi_F^alpha)]^(1/2)
 <= C E_Q'[(W_r F_j(H_X))^2]^(1/2)
                                  (1+beta+sqrt(Phi)).          (MF9)

This is exactly the prefactor absorbed by P's regional proof. It contains one
original W and, after disintegration, one original Z. In particular:

- R1: the additional factor is polynomial in chi and is absorbed by the
  pin-ball Gaussian penalty; the integrable |q|^(2-d) weight remains.
- R2a/R3a: polynomial powers of r^-1 or s^-1 from beta and the joint floor are
  absorbed by exp(-c r^-2/3) or exp(-c s^-1/4). The R3a determinant bound is the
  corrected AXIS-SAFE bound on the entire strip, not just at v=0.
- R2b/R3b: inverse powers of |v| are absorbed by exp(-c/|v|^2); the shell height
  integration keeps the required r^3 and its summable radial ledger.
- R2c/R4: beta,Phi are uniformly bounded; the original endpoint r^2 weight
  cancels the one endpoint normalizer, and the remote height window gives r^3.

Thus summing P's original tiling proves MF1. This is a genuine marked estimate;
substituting the unconditional tail of F for MF4--MF9 would be an invalid proof.
The integral over the first two all-height regions dominates the same window
count and is not a claim of an all-height global O(r^3) estimate.

## 6. Cluster tails, moment growth, and a bounded-size lower witness

The source lower event gives P(N>=2)>=c r^3, hence EN>=P(N>=1)>=c r^3; G gives
EN<=C r^3. On N>=1, exp(theta N^alpha)<=N exp(theta N^alpha), proving both MF2
bounds after normalizing by the proper denominator. MF3 follows by Markov with
the increasing function n exp(theta n^alpha).

For integer p>=2, (N)_p<=N N^(p-1), and elementary calculus gives

 sup_{x>=0} x^(p-1) exp(-theta x^alpha)
      = [(p-1)/(e theta alpha)]^((p-1)/alpha).

Consequently the proposed theorem makes the growth of the earlier unspecified
factorial constants explicit:

 E(N)_p <= C r^3 [(p-1)/(e theta alpha)]^((p-1)/alpha).           (MF10)

It does not give a lower bound of order r^3 for p>=3. A count taking only values
0 and2 is still a counterexample to that unwarranted inference.

Since MF3 makes the rescaled tail uniformly small, choose a FIXED M sufficiently
large that C M^-1 exp(-theta M^alpha)<=c/2. Then

 P(2<=N<=M)>=c r^3/2.

Thus the known multiple-point lower event cannot owe all its order-r^3 mass to
clusters of diverging size. This is not a limit law for cluster shape or location.

## 7. A subsequential independent-replica consequence, not a Poisson field claim

Fix one parameter sequence r_n down to zero in the admissible family. Define
nu_n(k)=r_n^-3 P(N_{r_n}=k), k>=1. MF1 gives
sum_k k exp(theta k^alpha) nu_n(k)<=C. Thus there is a subsequence converging
coordinatewise to a finite measure nu on the positive integers. For theta'<theta,
the convergence is also in the weighted l1 norm with weight exp(theta' k^alpha),
by a uniform tail bound followed by finite-dimensional convergence.
The total mass is bounded away from zero, and sum_{k>=2}nu(k)>0, using the original
lower event and tightness. Uniqueness of nu is NOT implied by these bounds.

For independent copies of the field at each r_n, take floor(t/r_n^3) copies and
sum their window counts. Its probability generating function is exactly

 [1+r_n^3 sum_{k>=1}nu_n(k)(z^k-1)]^floor(t/r_n^3), 0<=z<=1,

which tends along the selected subsequence to

 exp[t sum_{k>=1}nu(k)(z^k-1)].

The replica sums are tight because their means are uniformly bounded. Every
subsequential weak limit has the displayed probability generating function,
which uniquely determines a probability measure on the nonnegative integers.
This is a compound-Poisson law with finite activity sum nu(k) and jump-size law
nu/sum nu. In d=2 the generating functions have a common complex neighborhood
of the closed unit disk, because alpha=1; in d>2 no such analytic-disk conclusion
follows from the stretched-exponential estimate alone.

This conclusion concerns INDEPENDENT REPLICAS on a diverging sample-count scale.
It is not a Poisson or compound-Poisson spatial limit within one field, nor a
unique r->0 count distribution. Alternating rare counts of size2 and3 satisfy
the moment/tail hypotheses but produce different subsequential jump measures.

## 8. Review boundary and useful falsifiers

No full-field simulation or finite algebra test proves MF1. Review must check:
extra-conditioned coefficient means; a cap fixed before witness selection;
retained-radius geometry at tiny imaginary parts and periodic lifts; the uniform
positive rate in MF7 versus its nonuniform prefactor A; 2theta<c at Holder;
canonical Borel field-mark insertion; all-region absorption of sqrt(A); and the
per-fixed-family scope. The independent-replica construction requires explicit
independence and passage to a subsequence unless coefficient convergence is
proved elsewhere.

The included finite tests verify algebra and scope barriers only. The prior
local-only v1 handoff is superseded by this explicitly attributed publication
successor; its analytic argument and constants are unchanged. New custody checks
validate all named direct proof inputs and the credited #153 proof, including
historical Git-object identities when run in a full checkout. Local packet-only
execution does not establish that upstream check; hosted execution is separate.
Consensus was actually queried and quota-exhausted. The reconnaissance file logs
a limited primary abstract read; no outside theorem or novelty claim is imported.
An unanswered review request and passing checks do not establish acceptance.
