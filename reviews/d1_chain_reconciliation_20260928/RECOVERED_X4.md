## Section 4 verdict — residual field after conditioning on A_r

Frozen parent `UNIFORM-MATRIX-CAP-LIFETIME-20260924-v1`, Drive `[REDACTED DRIVE DOCUMENT ID]`, 40261 bytes, SHA256 `9350ad6eaba6626b93c3dedeef9e2ff816e5cdf1c8318e85fb27499141c84bc7`. Lines below are that body. Source was not edited.

Reviewer: Cursor cloud agent `bc-9142fddf-0d94-5ecb-a764-00d3fba0c5d9`, Grok 4.7, xAI. Author: OpenAI / ChatGPT. Different provider. No organizational independence credit.

Exposure: the same parent bytes as the Section 9 review; Section 4 lines 115–136, the Section 3 sentences those lines cite (93–94, 103–110), and Section 2 lines 59–67. Sections 5–7, the normalizer, the cap theorem, Theorem A, Theorem C, equation (15.2), and RN/24-jet status were not reviewed and are not accepted.

The source law is Q_{r,b,k,R}: Gaussian regression on the 2(d+1) physical pins, equivalently on U_r=v_r because T_r is deterministic and invertible (lines 72–94). That is six scalar coordinates when d=2 and eight when d=3. The argument does not use a special count of six.

All five interfaces are **ACCEPT** on the small-r regime where the Section 3 imports below are in force. None is a counterexample or a block.

### Imported Section 3 covariance hypotheses (not re-proved, not accepted as Section 3)

- **I3a.** For all sufficiently small r, Sigma_r(R) is uniformly positive definite and Sigma_r^{-1} is uniformly bounded (line 105).
- **I3b.** v_r is uniformly bounded for small r (lines 93–94 and 103).
- **I3c.** Under Q, Cov(A_r) is uniformly bounded above and below, and E_Q A_r is uniformly bounded (lines 109–110). A_r has m(m+1)/2 symmetric entries.
- **I3d.** Those Hessian entries do not repeat the contact functionals (3.4), so the enlarged covariance is nondegenerate (lines 107–109). This is the stated reason the Schur complement in I3c is positive definite.

Section 2 line 61, sum_n sqrt(a_n)(1+|n|)^q < infinity for every q, is the Fourier input. It was already the nondegeneracy input checked for Section 9. It is used again here and is not a new acceptance of Sections 3 or 5.

### R1 — uniform conditional C^q L^p moments — ACCEPT

On the small-r set, I3a and I3b bound the regression energy v_r^T Sigma_r^{-1} v_r. For a standardized Fourier coefficient ξ, |E_Q ξ| <= sqrt(energy) because Cov(ξ,U) Sigma^{-1} Cov(U,ξ) <= Var(ξ)=1, and the conditional centered variance is at most 1. Every such ξ is therefore Gaussian under Q with L^p norm bounded by a constant that depends on p and the energy bound, uniformly in the mode and in (b,k,R).

The C^q norm is at most a constant times sum_n sqrt(a_n)(1+|n|)^q |ξ_n|. Minkowski's inequality and the Section 2 series then give (4.1) for every finite p and every derivative order q. The supremum is over that small-r set, over B, over K, and over frames. The display writes sup_{r,b,k,R}; the bound that is proved is the one on which I3a and I3b hold.

### R2 — C^4 regression construction and orthogonality — ACCEPT

(4.2) is ordinary Gaussian regression under Q. mu_r(z)=E_Q f(z). B_r(z)=Cov_Q(f(z),A_r) Cov_Q(A_r)^{-1}. g_r is the residual. I3c makes the inverse legitimate, so the normal equations give Cov_Q(g_r(z), A_r)=0 for every z.

The field has a smooth version (Section 2 line 61). mu_r and B_r are deterministic and smooth in z because they are built from derivatives of K_L. Hence g_r is a C^4-valued random field, which is the regularity (4.3) uses. Differentiating in z passes inside the covariance, so every derivative evaluation D^α g_r(z) is the residual of D^α f(z) and is orthogonal to every entry of A_r.

Finite collections of those evaluations are jointly Gaussian with A_r under Q, and the cross-covariance is zero, so each such finite collection is independent of the whole matrix A_r. Line 127 keeps the residual's internal correlations and does not claim that raw Hessian entries, endpoint variables, or sampled derivative maxima are independent of A_r.

### R3 — countable collection to the smooth field — ACCEPT

The torus has a countable dense set D. The countable family {g_r(q): q in D} is jointly Gaussian with A_r and uncorrelated with it, hence independent of A_r. A continuous version is a measurable function of those values. Rational difference quotients recover derivatives through order 4, so the C^4-valued random element is measurable with respect to that countable sigma-algebra, up to null sets. Independence of g_r from A_r follows. No uncountable family of Gaussians is declared independent in one step. Separability of C^4 and continuity are the whole upgrade.

### R4 — bounds on B_r through order 4, and residual C^4 moments — ACCEPT

D^β B_r for |β|<=4 is a conditional cross-covariance of a derivative of f against A_r, times Cov_Q(A_r)^{-1}. I3c bounds the inverse. Each conditional cross-covariance is the unconditional derivative of K_L minus the pin-regression term. Those kernels are bounded uniformly in z by the Section 2 series, and Sigma_r^{-1} is bounded by I3a, so the derivatives of B_r through order 4 are uniformly bounded on the small-r set.

The Fourier coefficients of g_r are centered under Q, with variance at most 1. The same Minkowski-plus-summable-series argument as R1, with regression energy zero because the residual coefficients are centered, gives uniformly bounded L^p norms of ||g_r||_{C^4} for every finite p.

### R5 — envelope J_r and the M3/M4 bound — ACCEPT

J_r=1+||g_r||_{C^4} in a fixed coordinate norm. R3 makes J_r independent of A_r, because the norm is a measurable function on the separable space C^4. R4 gives sup ||J_r||_p < infinity for every finite p, and J_r>=1.

On the cylinder,
D^α f = D^α mu + (D^α B)·(A_r - E_Q A_r) + D^α g_r
for |α| in {3,4}. The first term is deterministic and bounded by R1. The coefficient of the matrix is bounded by R4. I3c bounds E_Q A_r, so the middle term is at most C(1+||A_r||_F). The last term is at most J_r. Therefore both suprema are at most K_0(J_r+||A_r||_F). The factor that compares a partial-block operator norm with this coordinate norm depends only on d. No inverse eigenvalue of a random Hessian enters.

The name M3/M4 is the cap theorem's name for those derivative suprema. Using the name does not accept the cap theorem.

## Not accepted

Section 3 is only the import list I3a–I3d. Sections 5–7, the normalizer floor, the cap theorem, Theorem A, Theorem C, equation (15.2), and RN/24-jet status are outside this verdict. No scientific-status flag moves.