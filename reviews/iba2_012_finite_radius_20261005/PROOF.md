# IBA2-012: a finite-radius additional-soft cluster estimate

**Object:** IBA2-012-FINITE-R-CLUSTER-20261005-R3-v1.1.  
**Author:** OpenAI / GPT-6 Astra Pro, continuation session `iba2-012-publication-audit-20261005-r3`, acting for Dylan Roy.  
**Disposition:** NEW AUTHOR-SIDE PROOF CANDIDATE, conditional on the exact imported source interfaces below; nonauthor mathematical review required.  
**Scientific effect:** NONE. No existing status, theorem, proof, register, review, flag or prize is changed. This is an additive publication of the preceding local proposal, not an accepted theorem or a review of its own mathematics. The author is exposed to the predecessor audit and other agents' reports; independence credit is zero.

## 1. What this adds and what it does not

SC §4 already establishes qualitative exclusion of further soft transverse eigenvalues from the fixed-radius, rescaled nonempty cluster measure. Codex `/root`'s main#259 comments 6003533425 and 6003547392 isolate and quantify the corresponding **limiting** measure: q additional hard eigenvalues in `(0,eta]` cost `eta^[q(q+7)/2]`. That work is credited, not reclaimed.

A limiting estimate does not by itself allow `eta = r`. The present proposal proves an original-law **finite-r** bound, including norm tails, so this substitution becomes valid at fixed positive compact marks and fixed observation radius. It is separate from the preceding author's small-k cusp estimate (main#259/6004452810): that estimate concerns a different normalization and range of marks. The present argument does not consume that new, not-yet-reviewed lemma.

This is not an exhaustive IBA2-012 closure, a rate of convergence of the full cluster distribution, a sharp lower bound, an all-mark result, or an elder matching theorem. No uniformity is claimed as the observation radius, dimension, volume, or marks escape their specified sets.

## 2. Exact bindings and consumed interfaces

Repository: `d6g8k5htny-coder/Math-`. Source cut:

`04f47774bace871e3ad7dedc409e04f0280dfdd7`.

| Tag | Path | Complete Git blob | Consumed material |
|---|---|---|---|
| P | `imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md` | `dfed3b8d318a3ab1950957f393307733a4bef3f2` | §3 (3.5); §4 full-field regression and conditional moments; §5 endpoint bounds and full normalizer (5.5); §6 typed determinant inequality (6.2); §7 Lebesgue spectral Jacobian |
| SC | `frontiers/spectral_cluster_closure_20260929/PROOF.md` | `16c56821b52fd76b0be791622b9c3809eafde75a` | §3 deterministic vector exclusion (11); §4 is the qualitative predecessor, not a quantitative premise |

The consumed interfaces were re-read at this source cut and have the same complete Git blobs as the preceding e31b6ad8 and c08e8359 cuts. The core finite-radius proof is retained; v1.1 adds the unequal-scale corollary below and publication/reproduction details. The new proof does not need C6's all-order factorial moment theorem, remote kernels, the cubic classifier, or a full-variation convergence rate. A source-interface read is not represented as a fresh independent review of all ancestors.

Immutable sources:
- https://github.com/d6g8k5htny-coder/Math-/blob/04f47774bace871e3ad7dedc409e04f0280dfdd7/imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md
- https://github.com/d6g8k5htny-coder/Math-/blob/04f47774bace871e3ad7dedc409e04f0280dfdd7/frontiers/spectral_cluster_closure_20260929/PROOF.md

## 3. Precise statement

Fix `d >= 3`, `m=d-1`, `L>0`, a compact birth set B, a compact positive mark interval `[k_-,k_+]` with `k_->0`, and a fixed `R>=1`. Use P's exact variance-one periodized field, original Gaussian pin law Q, typed maximum/saddle weight W, and **full** normalizer Z. All frames are allowed, with constants uniform on the compact frame space.

Write `A_o = D_y^2 f(0)` and order the eigenvalues of `-A_o` as

    h_1 <= h_2 <= ... <= h_m.

The h_i may be negative at finite r. Let N_R count additional critical points in the physical ball of radius Rr about the midpoint, with heights strictly between the pin heights, excluding the pins. Choose `K >= 1` as a fixed dimension-dependent multiple of `1+||f||_{C^4}` large enough to bound the operator derivatives in P and SC.

For every fixed real `a>=0`, and every integer `1<=q<=m-1`, set

    beta_q = 4q + q(q-1)/2 = q(q+7)/2.

There are `C<infinity` and `r_*>0` such that, for `0<r<=r_*`, `0<=eta<=1`, and the fixed parameter ranges above,

    E_{Q^W}[K^a ; N_R>0, h_{q+1}<=eta]
        <= C r^3 (eta+r)^beta_q.                       (FR)

The event does not require h_1,...,h_{q+1} to be positive. Hence it also covers the narrower SC strip with positive hard eigenvalues, or `|h_{q+1}|<=eta`.

The q=0 version is the usual fixed-R `O(r^3)` occurrence bound. For d=2 there is no additional transverse direction, so the q>=1 assertion is empty.

## 4. Proof

**Charts and measurability.** Reduce r_* so r<=1 and the closed radius-Rr ball and its surrounding cylinder embed in one torus chart. For fixed pins and marks, the event N_R>0 is Borel: exhaust the punctured closed ball by compact sets at distance at least 1/n from the pins and require the critical value to lie in [b-kr^3+1/n,b-1/n]. Existence of a zero gradient satisfying these closed conditions is closed in C^1, since its location lies in a fixed compact set; the countable union is precisely the nonempty event. Eigenvalue and norm conditions are Borel as well. No extra zero-count moment theorem is needed.

### 4.1 Original-law moment and density facts

On typed support, set `B_M=-D_y^2f(M)>0`, with ordered eigenvalues

    0<lambda_1<=...<=lambda_m.

P (3.5) gives a common upper bound `C exp(-c||B_M||_F^2)` for its density on symmetric-matrix Lebesgue space. P (4.2) and its bounded regression coefficients imply, for every fixed s,

    E_Q[K^s | B_M] <= C_s (1+||B_M||_F)^s.             (1)

This is conditioning on the whole endpoint transverse matrix, not asserting independence of its eigenvalues. The bounded compact pin target is included in C_s. P §5 gives `Z>=z_*r^2` and `W/r^2<=CK^(2d)`.

### 4.2 Convert near occurrence into a first-eigenvalue width

Let

    E_large = {rK > k_-/(4R)}.

Off E_large, SC (11) applies. If there is any additional critical point in the ball, there is one in the surrounding SC cylinder. The contrapositive of its exclusion criterion gives

    h_1 <= (8RK+56RK^2/k)r <= C_R rK^2.

The Hessian Lipschitz bound and the min-max eigenvalue inequality give, for every i,

    |lambda_i-h_i| <= CrK.

Therefore, on `{N_R>0,h_{q+1}<=eta}` outside E_large,

    lambda_1 <= C_R rK^2,
    lambda_{q+1} <= eta+CrK.                           (2)

This step is the additional localization not supplied by a bare determinant-layer statement. It uses no hard-eigenvalue inverse.

### 4.3 Retain all endpoint determinant factors

P (6.2), with `M3<=K` and a larger fixed constant, yields

    W/r^2 <= C K^2 prod_{i=1}^m lambda_i(lambda_i+c rK).
                                                               (3)

In particular the saddle factor is retained even where a transverse eigenvalue is smaller than r. Replacing `lambda_i+c rK` by `lambda_i` would be invalid in that range.

Split `K` into bands `[t,2t)`, `t=2^j`, j>=0. Let

    delta=c_1 rt,
    A_t=c_2 rt^2,
    B_t=eta+c_3 rt,

where constants are enlarged so that `delta<=B_t` and (2) is contained in `lambda_1<=A_t`, `lambda_{q+1}<=B_t` on that band.

By (1), for an arbitrarily large fixed s,

    P_Q(K>=t | B_M) <= C_s t^(-s)(1+||B_M||)^s.         (4)

After bounding `K^(a+2)` by `(2t)^(a+2)`, conditioning on B_M, and multiplying its density, the remaining polynomial from (4) must be absorbed **before** dropping any small-eigenvalue Gaussian factor:

    (1+||B_M||)^s exp(-c||B_M||^2)
        <= C_s exp(-(c/2)||B_M||^2).                   (5)

The constant may depend on the chosen s. Crucially, no power of t depending on s remains. This ordering prevents a circular choice of the tail moment.

### 4.4 Spectral integration with two different widths

Put `p=q+1` and `v_p=p(p-1)/2`. The Lebesgue spectral Jacobian is the Vandermonde times finite angular measure, independent of whether the Gaussian density is rotationally invariant.

On the actual ordered integration domain, all of the first p eigenvalues are at most B_t. Their internal Vandermonde is therefore at most `B_t^v_p`. Every cross difference between a soft and a remaining hard eigenvalue is bounded by the hard eigenvalue; absorb these and all hard-hard differences into a fixed polynomial in the remaining eigenvalues. The hard determinant factors obey

    lambda_i(lambda_i+delta) <= C t(1+lambda_i)^2,

because r<=1 and t>=1. The hard Gaussian integrals are thus at most `C t^(m-p)`.

Only after those bounds are imposed on the actual domain, extend the nonnegative remaining soft integrals to independent intervals: lambda_1 in `[0,A_t]` and each of the other q soft variables in `[0,B_t]`. This extension remains valid even if A_t>B_t: the Vandermonde estimate was made before extension, not asserted on the enlarged domain.

The first integral is

    int_0^{A_t} x(x+delta) dx
      = A_t^3/3+delta A_t^2/2 <= C r^3 t^6.             (6)

Each other integral is at most

    int_0^{B_t} x(x+delta) dx <= (5/6)B_t^3,             (7)

using delta<=B_t. The numerical 5/6 may be absorbed into C. No dimension-dependent singular integral remains.

Since

    3q+v_p = 3q+q(q+1)/2 = beta_q,
    B_t <= C t(eta+r),

the contribution of the jth band, after dividing by the full Z and using (3)-(7), is at most

    C_s r^3(eta+r)^beta_q
       t^[a+8+(m-p)+beta_q-s].                         (8)

Choose an integer `s>a+9+(m-p)+beta_q`. The dyadic sum converges. Its constant depends on the fixed parameters, q and a, but not on eta or r. This proves (FR) off E_large.

### 4.5 The large-norm branch is paid for, not discarded

For any M>0, the full normalizer and original Q moments give

    E_{Q^W}[K^a ; E_large]
      <= C E_Q[K^(a+2d); K>k_-/(4Rr)]
      <= C_M r^M.                                     (9)

Choose an integer M>=3+beta_q. Since eta+r>=r and r<=1,

    r^M <= r^(3+beta_q) <= r^3(eta+r)^beta_q.

Adding (9) proves (FR), including eta=0. This finishes the analytic argument.

## 5. Quantitative consequences

For eta>=r, (FR) is `O(r^3 eta^beta_q)`. For eta<=r, the estimate saturates at `O(r^[3+beta_q])`. There is no claim of an extra eta power below the perturbation scale r.

| Additional soft directions q | Total transverse corank addressed | beta_q | Bound at eta=r |
|---:|---:|---:|---:|
| 1 | 2 | 4 | O(r^7) |
| 2 | 3 | 9 | O(r^12) |
| 3 | 4 | 15 | O(r^18) |
| 4 | 5 | 22 | O(r^25) |

Rows require `d>=q+2`. The exponent equals the compact p-soft count `3p+p(p-1)/2` at p=q+1, but now the count has an original-law proof with a nonempty spatial event and all derivative tails retained.

More generally, for eta=r^alpha with alpha>0,

    E_{Q^W}[K^a ; N_R>0, h_{q+1}<=r^alpha]
       = O(r^[3+beta_q min(alpha,1)]).                  (10)

This is a joint event/derivative-weight estimate, not a rate for arbitrary test functions of the entire cluster process. Exact-count events `N_R=j` are subevents and inherit the same upper bound. Inserting a factor `N_R^j` would require a separate count-moment argument; it is not silently included.

The estimate does not control an effective quartic-zero sector with a hard transverse Hessian, repeated nonzero hard eigenvalues, remote collisions, the limit R->infinity, or k->0. Those need their own source-bound statements. The preceding small-k cusp lemma and this fixed-positive-k cluster lemma cannot be combined into an all-mark theorem by relabeling constants.

## 6. Why limiting mass alone cannot justify the diagonal

For 0<r<1, the nonnegative measures on (0,1)

    dmu_r(h) = [h^3 + 2r 1_{[r/2,r]}(h)] dh

converge in total variation to `h^3 dh`, and share an integrable majorant. The limit has `mu_0([0,eta])=eta^4/4`. Nevertheless,

    mu_r([0,r])=r^4/4+r^2,

which is not O(r^4). This is an abstract measure obstruction, not a realization in the Gaussian field. It shows precisely why the new original-law estimate is necessary; neither nullity, dominated convergence, nor a quantitative limiting measure alone is enough.

## 7. Adversarial self-audit and review request

This is author verification, not a nonauthor verdict. The following failure points were checked in the written argument:

1. **Endpoint versus midpoint:** use the ordered-eigenvalue Lipschitz bound for every index; no shared eigenbasis is presumed.
2. **Two widths:** the first width is O(rt^2), others O(eta+rt). Make the Vandermonde bound before enlarging the domain.
3. **Correlations:** use conditional norm moments given the whole matrix, not independence of K or eigenvalues.
4. **Moment choice:** absorb the conditional polynomial into the Gaussian before dropping small-variable decay, so increasing s genuinely makes the dyadic sum converge.
5. **Large derivatives:** bound in original coordinates with the full normalizer, choose M after beta_q, and retain eta=0.
6. **Finite-r saddle factor:** keep lambda_i+delta, so no false improvement is asserted below r.
7. **No extra counting weight:** N_R>0 is an event only. No unexplained determinant or factorial moment is added.
8. **Scope:** fixed d,L,R and positive compact marks throughout; all status changes withheld.

The smallest useful nonauthor review is the chain SC(11) -> (2), the matrix-conditioned dyadic integration (3)-(8), and exception absorption (9), against the two exact blobs. No full re-audit of C6/remote ancestors is required for this proposition because they are not consumed.

The accompanying standard-library exact checker tests the exponent ledger and soft polynomial integrals, including degree-changing negative controls. These are algebra controls, not formal verification of Gaussian regression or the continuum exclusion argument.

## 8. Unequal soft scales: the same finite-radius argument

**Corollary FR-mixed.** Keep every hypothesis of (FR). Fix `q` with `1<=q<=m-1`, put `p=q+1`, and choose deterministic thresholds `0<=eta_2<=...<=eta_p<=1`. Then, with C independent of all these thresholds and r,

    E_{Q^W}[K^a; N_R>0, h_j<=eta_j for every 2<=j<=p]
        <= C r^3 prod_{j=2}^p(eta_j+r)^(j+2).           (FR-mixed)

The remaining eigenvalues have no hard lower bound. The all-soft case `p=m` is included. This is still a nonempty event bound, not a count-moment or convergence-rate theorem.

*Proof.* In each norm band `[t,2t)`, keep `lambda_1<=A_t=c_2 r t^2` from (2) and set `B_{j,t}=eta_j+c_3 rt`, increasing c_3 so `delta<=B_{j,t}`. The actual ordered domain satisfies `lambda_j<=B_{j,t}`. Bound each internal Vandermonde factor by its larger eigenvalue, so

    prod_{1<=i<j<=p}(lambda_j-lambda_i)
        <= prod_{j=2}^p B_{j,t}^(j-1).

Make this bound on the original ordered domain, before extending lambda_1 to `[0,A_t]` and the remaining soft variables to `[0,B_{j,t}]`. The first integral remains `O(r^3 t^6)`; each other determinant integral is `O(B_{j,t}^3)`. Thus the product is

    O(r^3 t^6 prod_{j=2}^p B_{j,t}^(j+2)).

Each `B_{j,t}<=C t(eta_j+r)`, while `sum_{j=2}^p(j+2)=beta_q`. Conditional-moment absorption, hard Gaussian integration and the dyadic sum are exactly (4)-(8), with the same moment choice and no inverse eigenvalue. The large-norm estimate (9), with `M>=3+beta_q`, is absorbed because `prod(eta_j+r)^(j+2)>=r^beta_q`. This proves the result, including zero thresholds.

For positive exponents with `eta_j=r^alpha_j` (ordered consistently),

    contribution = O(r^[3+sum_{j=2}^p(j+2)min(alpha_j,1)]).

For example `q=2`, `eta_2=r^(1/2)` and `eta_3=r^(1/4)` give `O(r^(25/4))`; equal thresholds recover (FR). The factors have different powers: exchanging two exponents is not innocuous. This corollary adds hierarchical softening to the equal-width slice, not a general classification of arbitrary effective-jet or collision sectors.

## 9. External reconnaissance boundary

Consensus Primary again returned its monthly quota error in this continuation; no Consensus paper was retrieved or used. Public primary metadata for Armentano–Azais–Leon, arXiv:2304.07424, confirms that the current landing page is v4, while the project cites v3. No version substitution is made here. Azais–Delmas, arXiv:1911.02300v3, studies isotropic critical-point correlations; it is not a replacement for this exact-periodic determinant-weighted pin law. This proposition imports only P and SC as listed above and makes no literature novelty claim.

## 10. Publication and reproduction

Run `python -B -S test_finite_radius_cluster.py` and `python -B -O -S test_finite_radius_cluster.py` from this packet. The twelve test methods include the retained nine equal-scale controls and three mixed-scale checks. They are exact finite algebra tests, not a simulation, Lean replay or proof of the imported Gaussian interfaces. The newly added helper tests were run before implementing the helpers and failed for their two missing definitions; their successor run is recorded separately. No shared workflow is changed and the existing repository CI does not automatically run this standalone packet. Nonauthor analytic review and applicable current-candidate hosted checks remain required before integration.
