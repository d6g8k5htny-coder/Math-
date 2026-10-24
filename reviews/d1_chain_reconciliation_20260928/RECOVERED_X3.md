## Section 3 verdict — contact covariance behind the Section 4 imports

Frozen parent `UNIFORM-MATRIX-CAP-LIFETIME-20260924-v1`, Drive `[REDACTED DRIVE DOCUMENT ID]`, 40261 bytes, SHA256 `9350ad6eaba6626b93c3dedeef9e2ff816e5cdf1c8318e85fb27499141c84bc7`. Lines are that body. Source was not edited.

Reviewer: Cursor cloud agent `bc-9142fddf-0d94-5ecb-a764-00d3fba0c5d9`, Grok 4.7, xAI. Author: OpenAI / ChatGPT. Different provider. No organizational independence credit.

Exposure: the same parent bytes; Section 3 lines 69–113, equations (3.1)–(3.5); Section 2 lines 59–67 only as the positive-spectrum input named below. Sections 5 and later, the normalizer, the cap theorem, the coefficient, and RN status were not reviewed and are not accepted.

All five interfaces are **ACCEPT**. This discharges the Section 4 imports I3a–I3d on the small-r regime. It does not accept Section 4's moment or independence argument again, and it does not accept anything past Section 3.

### C1 — exact pin transform — ACCEPT

On the axial coordinates a=-r/2, c=r/2, with columns ordered (f(a), f(c), f_x(a), f_x(c)) after a sign-only reordering of (3.1), T_r is block lower-triangular. The value block has determinant 1/r. The derivative block has determinant -12/r^3. Each transverse pair (f_yj(a), f_yj(c)) contributes another factor 1/r, and there are m=d-1 such pairs. Absolute determinant:

|det T_r| = (12/r^4) (1/r)^{d-1} = 12 r^{-(d+3)}.

Every block is nonzero for r>0, so T_r is invertible. A coordinate permutation changes only the sign. Checked at r=2: axial determinant equals -12/r^4.

With the physical pins f(a)=b, f(c)=b-k r^3, and both axial derivatives zero, the image is exactly

U0=b-k r^3/2, U1=-k r^2, U2=0, U3=12k,

and every transverse row is zero. That is v_r in (3.3), for every r>0, not merely in the limit. Checked at b=3, k=5, r=4.

### C2 — uniform convergence U_r to U0*, including U3 — ACCEPT

The symmetric Taylor expansion at the midpoint gives U0→f, U1→f_x, U2→f_xx, and the transverse rows →(f_yj, f_xyj). For U3 the order-1 terms cancel:

f_x(a)+f_x(c)-2(f(c)-f(a))/r = (r^2/6) f_xxx(0) + O(r^4),

so (6/r^2) times that expression tends to f_xxx(0). The divided difference is an average of the third derivative plus an integral remainder. It is not a difference of two uncontrolled copies of f_x.

Section 2 line 61 supplies finite L^2 norms of every derivative. Those directional norms are continuous in the frame and O(d) is compact, so the L^2 remainder is O(r^2) with a constant independent of the frame. Thus U_r→U0* in mean square, uniformly over frames. The same uniform L^2 convergence gives uniform convergence of the covariances and of cross-covariances against any fixed finite jet. Stationarity supplies the translation, not rotational invariance of the torus.

### C3 — uniform positive-definite contact covariance — ACCEPT

This discharges I3a and the small-r half of I3b. The contact list (3.4) is a set of distinct derivative functionals at one point of a rotated frame. Section 2: every Fourier weight a_n is positive, so a vanishing-variance relation is a polynomial P(R^T n)=0 on the integer lattice. A polynomial vanishing on Z^d is identically zero, and R^T is invertible, so P is zero. Linear independence follows in every frame. The argument never maps the lattice to itself and never uses rotational invariance of K_L.

Sigma_0(R) is therefore positive definite at every R. Its entries are continuous in R because they are directional derivatives of a smooth stationary covariance. The minimum of λ_min(Sigma_0) on compact O(d) is positive. C2 gives Sigma_r(R)→Sigma_0(R) uniformly in R, so for all sufficiently small r, Sigma_r is uniformly positive definite and Sigma_r^{-1} is uniformly bounded. That is I3a. The explicit formula (3.3) bounds v_r on that same small-r set, uniformly in b∈B, k∈K, and the frame. That is I3b. Distinct orientations are not identified.

### C4 — append A_r and the Schur complement — ACCEPT

This discharges I3c and I3d. A_r is the transverse Hessian at M, stored as m(m+1)/2 independent entries. At r=0 those multiindices e_i+e_j, with i,j transverse, are disjoint from the contact multiindices {0, e_x, 2e_x, 3e_x, e_j, e_x+e_j}. Section 2 therefore makes the enlarged contact covariance positive definite. No contact functional is repeated.

For small r the joint covariance of (U_r, A_r) converges uniformly over frames to that enlarged contact covariance: U_r converges by C2, and derivatives at M, which is distance r/2 from the midpoint, converge by uniform continuity of the smooth covariance. Positive-definiteness is open, so the enlarged covariance is uniformly positive definite for small r.

The Gaussian conditional covariance of A_r given U_r is the Schur complement. Uniform positive-definiteness of the joint matrix bounds that complement above and below, independently of the conditioning value (b,k). The conditional mean is Cov(A_r,U_r) Sigma_r^{-1} v_r, and all three factors are uniformly bounded. That is I3c.

### C5 — Gaussian density envelope (3.5) — ACCEPT

Under Q, A_r is Gaussian on the fixed Euclidean space of symmetric-matrix coordinates, with covariance eigenvalues in a fixed interval [λ_*, λ^*] and with mean bounded, by C4. Then

(det Σ)^{-1/2} is uniformly bounded, and (A-μ)^T Σ^{-1} (A-μ) ≥ c ||A-μ||_F^2 ≥ (c/2)||A||_F^2 - C.

Hence density_Q(A) ≤ C_0 exp(-c_0 ||A||_F^2), with C_0,c_0 independent of small r, of the frame, and of (b,k). Conjugation by an eigenvector rotation preserves Frobenius measure up to the fixed coordinate Jacobian on symmetric matrices, so the same envelope survives that orientation change. The law itself is not claimed to be invariant under O(m), and the source says orthogonal invariance of the density is not required.

## What this does not accept

Section 4's R1–R5 deduction is not re-issued here; its covariance imports I3a–I3d are the part discharged. Sections 5 and later, the normalizer, the cap theorem, Theorem A, Theorem C, equation (15.2), and RN/24-jet status stay outside. No scientific-status flag moves.