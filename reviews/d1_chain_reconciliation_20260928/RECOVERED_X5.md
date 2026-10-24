## Section 5 verdict — endpoint identities and the full normalizer

Frozen parent `UNIFORM-MATRIX-CAP-LIFETIME-20260924-v1`, Drive `[REDACTED DRIVE DOCUMENT ID]`, 40261 bytes, SHA256 `9350ad6eaba6626b93c3dedeef9e2ff816e5cdf1c8318e85fb27499141c84bc7`. Lines are that body. Source was not edited.

Reviewer: Cursor cloud agent `bc-9142fddf-0d94-5ecb-a764-00d3fba0c5d9`, Grok 4.7, xAI. Author: OpenAI / ChatGPT. Different provider. No organizational independence credit.

Exposure: the same parent bytes; Section 5 lines 138–182, equations (5.1)–(5.5); the Section 3 and Section 4 sentences named below, already reviewed. Section 6 and later, the cap theorem, Theorem A, Theorem C, equation (15.2), and RN status were not reviewed and are not accepted.

All six interfaces are **ACCEPT**. None is a counterexample or a block.

### Imports already reviewed, versus new input

Used, and already accepted on this parent:

- **Section 3 C1–C5.** Exact target (3.3), including the contact component 12k; uniform mean-square convergence of the contact jet; uniform positive-definiteness of Sigma_r and a uniform bound on Sigma_r^{-1} and on v_r for small r; transverse Hessian not among the contact functionals; Schur complement giving Cov_Q(A) bounded above and below with bounded mean; density envelope (3.5).
- **Section 4 R1 and (4.3).** Uniform C^q L^p(Q) moments (4.1). On the local cylinder, M3 and M4 are at most K_0(J_r+||A_r||_F), and J_r has every finite moment. The dimensional comparison between coordinate norms and partial-block operator norms sits inside K_0.

Proved in Section 5 itself, not previously accepted and not an external citation: the integral identities (5.1)–(5.3), the congruence scaling, and the passage from that scaling to (5.4)–(5.5).

No new unproved input. The predecessor cap theorem is not used in Section 5. The historical numerical floor 17/10 is not used. There is no restricted-event normalizer and no extra pin density.

### N1 — endpoint averages (5.1) — ACCEPT

The axial pins f_x(a)=f_x(c)=0 give ∫_a^c f_xx = 0. With |f_xxx| controlled by the M3-Lipschitz constant,

|r f_xx(a)| = |∫_0^r ∫_0^s f_xxx| <= M3 r^2/2,

so |alpha_M| <= M3/2, and the same backward integral gives |alpha_S| <= M3/2. The constant 1/2 is the integral of the linear weight and is achieved when f_xxx is constant.

The transverse gradient pins give ∫_a^c ∂_x ∇_y f = 0, so the average of the vector ∇_y f_x is zero. The same integral, applied to that vector and its derivative, gives ||beta_i|| <= M3/2. This is not a simultaneous vector Rolle zero. A Rolle argument would ask for one point where every component of ∇_y f_x vanishes at once; that point need not exist, and the proof does not use it.

The third line is the fundamental theorem, not the pins: ||A_S-A_M||_op <= r M3 whenever M3 bounds the axial derivative of the transverse Hessian in operator norm. That is the norm already compared with the coordinate C^3 norm in the accepted bound (4.3).

### N2 — height and third-derivative estimates (5.2) — ACCEPT

With f(c)-f(a)=-k r^3 and both axial derivatives zero, integration by parts gives the exact weight identity

∫_0^r u(r-u) f_xxx(a+u) du = 2 k r^3.

The weight u(r-u) has integral r^3/6, so its weighted mean of f_xxx is exactly 12k. This matches the contact value U3=12k from (3.3), which is exact at the pins, not only in the limit.

If |f_xxxx| <= M4, then f_xxx stays within r M4 of this weighted mean. Substituting f_xxx=12k+η into

f_xx(a)=-(1/r)∫_0^r (r-u) f_xxx(a+u) du

gives f_xx(a)=-6 k r plus an error at most M4 r^2/2, hence |alpha_M+6k| <= r M4/2. At the right endpoint the same expansion gives f_xx(c)=6 k r plus an error of the same size, hence |alpha_S-6k| <= r M4/2.

### N3 — block determinant (5.3) and moments — ACCEPT

For H=[[r alpha, r beta^T],[r beta, A]], the Schur calculation when A is invertible is

det H = det(A) (r alpha - r^2 beta^T A^{-1} beta) = r alpha det A - r^2 beta^T adj(A) beta,

because det(A) A^{-1}=adj(A). Both sides are polynomials in the entries, so the identity survives at singular A and at alpha=0. Dividing by r is (5.3). Checked on nonsingular, singular, and zero-alpha blocks in dimensions m=1,2,3, including the empty-product adjugate 1 when m=1.

By (5.1), alpha and beta are bounded by M3/2. By (5.3), det H_i/r is a polynomial in those quantities and in the Hessian entries. (4.1) and (4.3) give every finite moment of M3 and of the C^2 norm, uniformly in small r and in (b,k,R). Cauchy–Schwarz lifts that to every finite moment of W_r/r^2 = |det H_M/r| |det H_S/r| times the type indicator. Uniform L^{1+δ} bounds are the uniform integrability used below. No inverse of alpha_i or of A_i is taken.

### N4 — scaled Hessian convergence — ACCEPT

The matrix that converges is the congruence D^{-1} H D^{-1} with D=diag(sqrt(r), I):

[[alpha_i, sqrt(r) beta_i^T],[sqrt(r) beta_i, A_i]].

Its off-diagonal entries are exactly sqrt(r) beta_i, as written. By (5.1) and the uniform moments of M3, those entries tend to 0 in probability, uniformly in the parameters. By (5.2) and the uniform moments of M4, alpha_M → -6k and alpha_S → 6k in probability, uniformly on compact B×K. By (5.1), A_S-A_M → 0 in probability in operator norm.

A_M is a finite-dimensional Gaussian regression of the transverse Hessian at distance r/2 from the origin. Section 3 supplies uniform convergence of the contact covariance, of v_r to v_0=(b,0,0,12k,0,…), and of the cross-covariance, over compact frames. Means and covariances of A_M therefore converge to those of A_0, uniformly in (b,k,R). The scaled endpoint Hessians converge in distribution, uniformly on that compact set, to diag(-6k, A_0) and diag(6k, A_0). The errors that are not the limiting Gaussian go to 0 in probability.

k>=k_->0, and the conditional law of A_0 is nondegenerate by the Section 3 Schur complement, so the limiting matrices are nonsingular almost surely.

### N5 — full endpoint weight once, display (5.4) — ACCEPT

For r>0, det(D^{-1} H D^{-1})=det(H)/r, and Sylvester's law preserves inertia. Therefore

W_r/r^2 = |det scaled_M| |det scaled_S| 1{H_M<0, index(H_S)=d-1}.

The product of the two absolute determinants tends to (6k)^2 det(A_0)^2. Both type conditions become A_0<0: the axial eigenvalue -6k is negative and 6k is positive, so the maximum indicator and the index-(d-1) indicator are the same event in the limit. Because A_S-A_M	o0, the two transverse matrices converge to one copy of A_0, and the indicator appears once, not as a product of two independent copies. The endpoint weight itself is the product of both determinants. That is the full normalizer in the sense of Section 1: no extra pin density, coordinate Jacobian, or adjacency factor.

The discontinuity of the type indicator is the singular locus of A_0, which has probability zero under every nondegenerate Gaussian in the uniform covariance window. Uniform integrability from N3, continuous dependence of Gaussian means and covariances, and the subsequence argument on the compact parameter set give

Z_r/r^2 → (6k)^2 E[det(A_0)^2 1{A_0<0}],

uniformly in (b,k,R). The common integrable majorant for the limiting polynomial is the Section 3 envelope (3.5), transferred to A_0 by the uniform conditional covariance bounds: det(A)^2 is dominated by a Gaussian moment that does not depend on the parameter.

### N6 — qualitative floor (5.5) — ACCEPT

On B×K×O(d), (6k)^2 >= (6 k_-)^2 > 0. The conditional covariance of A_0 is continuous and positive definite, hence uniformly positive definite on the compact set. A nondegenerate Gaussian charges every nonempty open set. The negative-definite cone has nonempty interior, and det^2 is not almost surely zero there, so z_0(b,k,R)>0 at every parameter. The same uniform density envelope makes z_0 continuous. A continuous positive function on a compact set has a positive minimum and a finite maximum.

Uniform convergence from N5 therefore yields, after reducing r_* if needed,

0 < z_* <= Z_r/r^2 <= z^* < infinity.

The constants are existential. They are not the historical numerical floor 17/10. The expectation is the full typed weight E_Q W_r, not a normalization on a further restricted good event.

## What this does not accept

Section 6 and later, the cap theorem, Theorem A, Theorem C, equation (15.2), and RN/24-jet status stay outside. No scientific-status flag moves.