# IBA2-012: count-weighted transfer for finite-radius multi-soft sectors

Object: IBA2-012-COUNT-TRANSFER-20261006-v1.
Author: OpenAI / GPT-6 Astra Pro, session `iba2-count-weight-transfer-r6-20261006`, Dylan Roy — delegated AI work.
Disposition: AUTHOR-SIDE MATHEMATICAL CANDIDATE; nonauthor source review required.
Scientific effect NONE. No prior proof, review, status, catalog, formal manifest or prize changes.
The author wrote the FR precursor and is exposed to prior reviews; organizational-independence credit0.

## 1. The precise gap addressed

The landed finite-radius packet FR, Math-#306, §5 explicitly says that inserting a factor N_R^j needs a separate count-moment argument. Its §8 proves an unequal-soft-threshold occurrence estimate, not a count-weighted estimate. This note supplies that missing transfer, conditional on the sharp C6 fixed-order count moments and the matching first moment. It does not re-prove P §7, FR's eigenvalue integration, or C6's witness/collision proof.

The result preserves the rare r^3 scale, proves negligibility for every fixed polynomial count weight on these sectors, and explains why loss-free preservation of the full soft exponent does NOT follow from these inputs. The last assertion is an abstract countermodel to an inference, not a Gaussian-field counterexample.

## 2. Exact source bindings and interface alignment

Repository `d6g8k5htny-coder/Math-`; source cut `2f8b6f372be383d752e9dd30d38234faa977243c`.

| Tag | Path | Full Git blob | Consumed interface |
|---|---|---|---|
| FR | `reviews/iba2_012_finite_radius_20261005/PROOF.md` | `5ed684c9bb446efc9bef5f3980717c6dc039abfd` | §§3,5,8: finite-r event bound with every fixed derivative-norm power and mixed thresholds |
| C6 | `frontiers/c6_palm_route_20260929/PROOF.md` | `89eb8adf08fe7afc2cab9662d3a9875c05ae5cc5` | §1.1 same tilted law and all-index torus window count; §1.2 Theorem Q; Corollary Theta only for optional normalized consequences |
| DL | `frontiers/d5_dimension_lift_20260929/PROOF.md` | `9d82c707fdb17d3072a8930f26dabedf59e456fc` | §1.2 Theorem G_d (1.7), summed over d+1 indices |
| DE | `reviews/d5_dimension_lift_erratum_20261005/ERRATUM.md` | `23df87bbe4ffd3b2d786cd695fb9f5448cfa1d05` | Original DL and C6 are read with the additive Lipschitz-factor/citation correction; their consumed final estimates are unchanged |
| P | `imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md` | `dfed3b8d318a3ab1950957f393307733a4bef3f2` | Same field/pins/full normalizer; §5 (5.5) only for the optional unnormalized numerator statement |
| SC | `frontiers/spectral_cluster_closure_20260929/PROOF.md` | `16c56821b52fd76b0be791622b9c3809eafde75a` | FR's deterministic-exclusion ancestry; no new quantitative premise or re-review here |

FR's scoped nonauthor review is Math-#306/6005379068; its landing is f4c33a98a982d50aa490e49ce9327c755682527c. C6 and DL retain the source-exposed review/ancestor limitations recorded in their own introductions and §2. This note neither creates another vote for those ancestors nor erases inherited obligations. Every conclusion here is conditional on the quoted interfaces at these exact bytes. A defect in an imported estimate blocks the corresponding inference.

Fix d>=3, L>0, a compact birth interval, a gap-mark interval [k_-,k_+] with k_->0, all orthonormal frames, and a fixed observation radius R>=1. Use the variance-one normalized periodized Gaussian field, pins M=-(r/2)u and S=(r/2)u, heights b and b-kr^3, and zero endpoint gradients. In all sources,

    Q_r = original Gaussian pin law,
    W_r = F_d(H_M) F_(d-1)(H_S),
    Z_r = E_Q[W_r],   P_r = Q_r^W = (W_r/Z_r) Q_r.

There is ONE tilted law and ONE full normalizer, not a separately normalized soft-sector law. Restrict r to the minimum of the finitely many source cutoffs needed for a chosen moment order. Constants may depend on that order, d,L,R and the fixed mark compacts.

Let N be C6's all-index count on the whole torus, pins removed, with heights strictly in (b-kr^3,b). Let N_R be FR's count in the physical ball of radius Rr. Thus 0<=N_R<=N pathwise. Write K>=1 for FR's fixed multiple of 1+||f||_(C^4). C6 also uses the letter K for a C^6 control; that variable is NOT identified with ours and is not inserted into its moment theorem.

Put m=d-1. For 1<=q<=m-1, choose deterministic 0<=eta_2<=...<=eta_(q+1)<=1/2, and take r<=1/2. Let h_j be the ordered eigenvalues of the negative midpoint transverse Hessian, exactly as in FR. They need not be positive at finite r. Define

    E_r = {N_R>0, h_j<=eta_j for 2<=j<=q+1},
    Pi_r = product_(j=2)^(q+1) (eta_j+r)^(j+2),
    beta_q = sum_(j=2)^(q+1)(j+2) = q(q+7)/2.

Here 0<Pi_r<=1. Extra eigenvalues have no unstated lower bound. The all-soft case q=m-1 is allowed. The local-occurrence condition N_R>0 is essential: nothing here controls {N>0,h_j<=eta_j} when no local witness occurs.

FR supplies, for every fixed t>=0,

    E_(P_r)[K^t ; E_r] <= A_t r^3 Pi_r.                    (F)

DL and C6 supply

    E_(P_r)[N] <= B_1 r^3,
    E_(P_r)[(N)_j] <= B_j r^3 for every fixed integer j>=2. (C)

## 3. The count-weighted transfer theorem

**Theorem CT.** Fix a>=0, s>0, and an integer p>s. Put theta=1-s/p in (0,1). Under the exact interfaces above,

    E_(P_r)[K^a N^s ; E_r] <= C_(a,s,p) r^3 Pi_r^theta.    (CT)

The same upper bound holds with N_R^s or (N_R)_j, s=j, in place of N^s. In particular, for every fixed delta in (0,1), choosing one fixed integer p>=s/delta and p>s gives

    E_(P_r)[K^a N^s ; E_r] <= C_(a,s,delta) r^3 Pi_r^(1-delta). (CT-delta)

No constant is asserted uniform in p, delta->0, R->infinity, k->0, L or d.

*Proof.* The Stirling identity for nonnegative integers is

    N^p = sum_(j=1)^p S(p,j) (N)_j,

with nonnegative Stirling numbers S(p,j). It has no constant term. Applying (C), including the first-moment term j=1, gives

    E[N^p] <= M_p r^3,   M_p=sum_(j=1)^p S(p,j) B_j.       (1)

This also shows N<infinity almost surely. Merely knowing E[N^p]=O(1) would be insufficient to preserve the r^3 scale in the next step.

Apply Holder under the SAME probability law P_r, with conjugate exponents 1/theta and p/s:

    E[K^a N^s 1_E]
      <= (E[K^(a/theta) 1_E])^theta (E[N^p])^(s/p)
      <= A_(a/theta)^theta M_p^(s/p)
           (r^3 Pi_r)^theta (r^3)^(s/p)
      =  A_(a/theta)^theta M_p^(s/p) r^3 Pi_r^theta.

The indicator is retained in the first factor; no independence of counts, K, Hessian, or E is used. Since a/theta is fixed, (F) applies. Since theta+s/p=1, the radial factor is exactly r^3, not r^(3theta). Monotonicity gives the local-count and factorial-count claims. Finally theta>=1-delta and Pi_r<=1 imply CT-delta. This chooses p ONCE for a specified delta; p is not a function of r. QED.

**Unnormalized numerator.** If needed, P(5.5)'s upper bound Z_r<=z^*r^2 gives

    E_Q[W_r K^a N^s ; E_r] <= C r^5 Pi_r^theta.

This multiplies by the one existing Z_r. It does not divide by Z_r again or change the probability law.

## 4. Scaling and a useful positive-count measure consequence

For equal eta_j=r^alpha, alpha>0,

    CT = O(r^[3+theta beta_q min(alpha,1)]).               (2)

For eta_j=r^alpha_j with alpha_2>=...>=alpha_(q+1)>0,

    CT = O(r^[3+theta sum_(j=2)^(q+1)(j+2)min(alpha_j,1)]). (3)

The ordering is reversed for alpha because 0<r<1. The saturation min(alpha,1) is inherited from the retained finite-r saddle factor in FR, not replaced by alpha below scale r.

Examples with eta=r:

| q | beta_q | count power s | imported moment p | exponent of r |
|---:|---:|---:|---:|---:|
| 1 | 4 | 1 | 2 | 5 |
| 1 | 4 | 1 | 4 | 6 |
| 1 | 4 | 2 | 6 | 17/3 |
| 2 | 9 | 2 | 4 | 15/2 |
| 3 | 15 | 3 | 6 | 21/2 |

Rows require d>=q+2. With q=2, eta_2=r^(1/2), eta_3=r^(1/4), s=1,p=4, the exponent is 87/16. These are upper bounds with fixed-order constants, not sharp asymptotics or lower bounds.

For any deterministic shrinking thresholds eta_j(r)->0, Pi_r->0. Therefore every fixed polynomial-count/norm weighted contribution in CT is o(r^3). It is enough to let one factor of Pi_r tend to zero; requiring all thresholds to shrink is a simple sufficient condition.

Here is a measure statement that does not presume convergence of the cluster law. Let Y=N or Y=N_R and define positive-count intensities

    mu_r(n) = r^-3 P_r(Y=n),  n>=1.

Delete the exceptional outcomes by Y'=Y 1_(E_r^c), and let mu'_r be its positive-count intensity. Since Y>=1 on E_r,

    sum_(n>=1) n^s |mu_r(n)-mu'_r(n)|
      = r^-3 E[Y^s ; E_r] <= C Pi_r^theta.                (4)

The analogous nonnegative measure with K^a inserted obeys the same identity and CT. For s=0, use FR directly and obtain C Pi_r without a loss. The norm in (4) is on POSITIVE counts: including the transferred mass at zero would add another term. This does not assert that either family mu_r converges, give its coefficients, or control locations/elder labels. It shows that deleting THESE sectors cannot change any existing weighted-l1 limit or subsequential limit in a fixed polynomial norm.

## 5. Normalized consequences and a denominator boundary

C6 Corollary Theta and DL give

    P_r(N>=1) >= P_r(N>=2) >= c r^3,
    E[N] >= 2P_r(N>=2) >= c r^3,
    E[(N)_2] >= c r^3.

Only in this paragraph do we consume those lower statements. Divide CT by these explicit denominators. It follows that the E_r contribution tends to zero in polynomial moments under global nonempty conditioning, and its probability tends to zero under the first and second factorial size-biased laws. For example, for j=1,2 and p>j,

    E[(N)_j 1_E]/E[(N)_j] <= C Pi_r^(1-j/p).             (5)

Additional K^a or polynomial weights are treated by CT at the corresponding larger s.

For factorial order j>=3, (5) is CONDITIONAL on a separately supplied lower denominator c_j r^3. C6 supplies only upper bounds at those orders. The distribution P(N=2)=r^3, P(N=0)=1-r^3 has all fixed upper moment bounds and E[(N)_2]=2r^3, but E[(N)_3]=0. No third factorial Palm law exists for that example. Likewise no lower bound on P(N_R>0) is imported for arbitrary R; global nonempty conditioning is not silently changed to local nonempty conditioning.

## 6. Why the loss-free soft exponent is not implied

**Proposition NL (abstract obstruction).** The interfaces F and C, even with K=1 and every finite count moment, do not imply E[N^s;E_r]=O(r^3 Pi_r) for any fixed s>0.

It suffices to give a family along r_n=2^-n, n>=1, in the q=1 case beta=4. On a three-atom probability space, set

    P(N=0)=1-r_n^3-r_n^7,
    P(N=2)=r_n^3,
    P(N=n+3)=r_n^7.

Let E_n be the last atom, take K=1, N_R=N, and set h_2=r_n there and h_2=2 on the other atoms. For any threshold 0<=eta<=1/2, the event {N_R>0,h_2<=eta} is empty if eta<r_n and equals E_n otherwise. Consequently its probability is bounded by r_n^3(eta+r_n)^4 for EVERY allowed eta; all K^t bounds in F hold with A_t=1. This is more than an estimate only on one diagonal.

For every fixed integer p>=1,

    E[N^p] = r_n^3 [2^p+(n+3)^p 2^-4n] <= C_p r_n^3,

because a polynomial times a decreasing exponential is bounded. Hence all fixed factorial upper bounds hold. Also P(N>=2)>=r_n^3 and E[(N)_2]>=2r_n^3, so the first/second lower-scale consequences hold as well.

Yet at eta=r_n, Pi_r=(2r_n)^4,

    E[N^s;E_n]/(r_n^3 Pi_r) = (n+3)^s/16 -> infinity.   (6)

Thus no loss-free estimate follows from these abstract premises. No Gaussian covariance, Hessian geometry, analytic sample path, or actual field realization is asserted for this countermodel. It blocks an inference from the quoted estimates, not a possible sharper theorem for the real Gaussian model.

In particular, taking p->infinity in CT is invalid without control of M_p and A_(a/theta). A sufficient additional lemma for loss-free transfer would be a uniform conditional sector bound E[K^a N^s | E_r]<=C whenever P(E_r)>0, combined with F at t=0; or a direct source-bound spectral/witness estimate with the count insertion. Neither is supplied here. The smallest remaining question for that stronger goal is the joint count/soft-sector estimate, not another proof of the cap layer or of the unweighted event.

## 7. Sector ledger and scientific boundaries

| Sector/interface | Disposition at the exact bindings of §2 |
|---|---|
| Finite-radius occurrence with extra soft eigenvalues, including unequal scales and norm tails | Covered by FR §§3,8; inherited scoped result, not this author's new PASS |
| Fixed polynomial/factorial count insertion on the SAME event/law | New CT proof candidate, conditional on FR + C6 + DL/DE; source-bound nonauthor review required |
| Same full soft power with no count/exponent loss | AMEND_EXTRAPOLATION: does not follow from these inputs, by the explicit NL family |
| First/second factorial normalization and global nonempty conditioning | CT plus explicit r^3 denominator lower bounds only |
| Higher factorial or arbitrary local-nonempty normalization | Lower denominator missing; not asserted |
| Small k, escaping marks, R->infinity, hard-Hessian higher-jet degeneracy, remote-only soft events, full cluster-law convergence, elder matching | Not controlled here; general IBA2-012 and IBA2-009 remain OPEN |

There is no spatial radial integration in CT: r is the fixed pin separation and the height window is kr^3. In particular an o(r^3) probability/count statement on compact marks is not an all-mark lifetime-density expansion. The codimension/determinant/Vandermonde powers remain those already derived in FR; Holder transfers their integrated bound and is not a new spectral power count.

## 8. Reproduction and review

Run `python -B -S test_transfer.py`, its `-O` equivalent, and `python -B -S transfer_check.py`. The tests check finite exact Holder inequalities, the Stirling/factorial identity, the exponent ledger, positive-count histogram deletion, the rare-spike formula and the missing higher denominator. Five named mutants exercise incorrect exponents, omitted first moments, a loss-free inference and a fabricated third-order lower bound. Unknown labels exit2. No unhandled crash is an intended mathematical rejection.

These finite tests do NOT prove the arbitrary-law Holder theorem, the asymptotic countermodel, FR, C6, or Gaussian-field facts; the ordinary proofs above provide the new argument. No local Lean execution or new formal target is claimed. Existing repository checks do not automatically run these standalone tests.

The smallest useful nonauthor review is §2 law/count alignment; the two factors and r^3 cancellation in CT; weighted-intensity and denominator conventions; and NL's simultaneous all-fixed-moment/threshold premises. No repeat review of unchanged ancestor proofs is requested. Consensus Primary returned quota exhaustion; no external paper was retrieved or used as a new premise. No claim of literature novelty is made.
