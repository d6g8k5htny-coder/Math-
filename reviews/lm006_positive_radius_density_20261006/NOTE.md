# LM006: the actual positive-radius endpoint law has a density

Dylan Roy — delegated AI mathematical work. Actual performer: OpenAI / GPT-6
Astra Pro, `lm006-density-premise-followthrough-20261006`.
Author-side source-interface application; scientific effect NONE; organizational
independence credit 0. Pickup: Math-#318 comment 6007692671. This additive note
does not edit #318 or its existing xAI review and is not a new review of that
packet's normalized-density, bounded-Lipschitz or event-margin argument.

## 1. Fixed object and exact sources

Fix d=2, L=24, b=6/5, axial endpoints M=(-r/2,0), S=(r/2,0), and the canonical
Gaussian regression law Q_r given

    O_r=(f(M),fx(M),fy(M),f(S),fx(S),fy(S))
        =(b,0,0,b-r^3/6,0,0).

Use 0<r<=min(1,r0), with r0<24. In particular the sites are distinct modulo the
torus lattice; r=0 and period-sized aliasing are excluded. No new numerical
choice of r0 or uniform covariance lower bound is asserted.

Source bindings in d6g8k5htny-coder/Math-:

- P: `imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md`,
  blob `dfed3b8d318a3ab1950957f393307733a4bef3f2`, read at
  `5e027afcae8c7bd42a6df8ae2025f82105b3e586`, §§1–4 and the definitions in §5.
  P supplies the actual normalized-periodized covariance, positive lattice
  spectrum, smooth Gaussian derivatives and finite-jet independence.
- E: `reviews/lm006_endpoint_extension_20261005/NOTE.md`, blob
  `551aa563562bc88a19e33d146259c03aa2d318f6`, landed #301 at
  `e31b6ad8356e0760c8a7fb6e816ff640c45176c9`, §§1,3–5. Its pin-adjusted variables
  equal the physical divided Hessians only after imposing the actual pins.
- N: `reviews/lm006_normalizer_stability_20261005/NOTE.md`, blob
  `5790aaa0332bd8e79b276be1577e4c5f3502eed6`, commit
  `5e027afcae8c7bd42a6df8ae2025f82105b3e586`, §§1–2 and5: physical coordinate
  order, exact typed weight, quartic envelope and contact map.
- T: `reviews/lm006_tilted_endpoint_law_20261005/NOTE.md`, blob
  `6633cdf0bfee55e2fc2046176effbf44634454b3`, frozen #318 head
  `ecafa5206c528b0c662ea0bcbb26938681251aa5`, §§1,3,5. The new application here
  supplies only the actual-field density premise explicitly retained in §5.

P's model specializes to these pins with k=1/6; it is not a planar covariance
substitution. These source interfaces are premises, not newly reviewed parent
theorems. Existing conditional or independent-alignment records are unchanged.

## 2. The twelve-function joint Gram is positive at every permitted positive r

At each of M and S take the six independent derivative functionals

    f, fx, fy, fxx, fxy, fyy.

They comprise the six pins plus the six independent symmetric Hessian entries.
In particular fxy and fyx are not counted twice. P §2 gives strictly positive
Fourier weights at every n in Z^2:

    p_n = exp(-2*pi^2*|n|^2/L^2) / sum_j exp(-2*pi^2*|j|^2/L^2).

For any real linear combination ell of these twelve functionals,

    Var(ell f) = sum_n p_n |ell exp(i*nu*n.x)|^2, nu=2*pi/L.

If the variance vanishes, ell annihilates every Fourier character. Equivalently,
the finite-order distribution consisting of its two finite delta-jet sums has
all Fourier coefficients zero. Fourier uniqueness for distributions gives zero;
smooth test functions supported separately near the two distinct sites, with
arbitrary prescribed finite jets, force every coefficient to vanish. This is
exactly P's finite-distinct-jet argument applied to the actual twelve entries,
not a deduction from positivity of the contact six-pin block alone.

Therefore the real joint covariance G_r of pins and physical Hessians is
strictly positive definite for each fixed allowed r. A constructive finite
spectral certificate for this particular axial configuration is given in §3.
There is no assertion that the least eigenvalue has a positive limit as r→0.

## 3. An explicit twelve-frequency certificate, including its collision limit

Translate M to zero. On the second site the Fourier character acquires the
phase z^n_x, where z=exp(i*nu*r); z is nonzero and z!=1 on our radius range.
Use these twelve frequencies, ordered by the transverse frequency:

    (n,0), n=0,...,5;  (n,1), n=0,...,3;  (n,2), n=0,1.

After multiplying derivative columns by the nonzero constants
(i*nu)^(-|alpha|), the ordinary jet symbols are n_x^a n_y^b, a+b<=2, at each
site. Replace n_y^2 by n_y(n_y-1) at each site, an invertible triangular column
operation involving the n_y column. Group columns by transverse degree b=0,1,2;
within each group put the M horizontal degrees first, followed by the S ones.
There are respectively six, four and two columns. The row and column groupings
make the evaluation matrix A(z) block lower triangular, with diagonal blocks

    B_3(z), B_2(z), 2 B_1(z),
    B_j(z) = [n^k | n^k z^n]_(n=0,...,2j-1; k=0,...,j-1).

The top-right zero blocks use n_y=0, and n_y(n_y-1)=0 at n_y=0,1. The factor2
in the last block is n_y(n_y-1) at n_y=2, and acts on BOTH of its columns.

For completeness the elementary confluent Vandermonde identity is

    det B_j(z) = (product_(k=0)^(j-1) k!)^2
                 z^[j(j-1)/2] (z-1)^[j^2].                 (1)

To see (1), start with the ordinary Vandermonde columns t^n at j nodes
coalescing to1 and j nodes coalescing toz. Successive divided-difference column
operations, followed by the collision limit within each cluster, give columns
(d/dt)^k t^n / k!. Cross-cluster differences tend to (z-1)^(j^2); changing to
unscaled derivative columns contributes the squared product of factorials.
At either nonzero node the Euler derivatives (t d/dt)^k t^n=n^k t^n are a
triangular combination of t^ell(d/dt)^ell with leading coefficient1. Its
column determinant contributes t^(0+...+j-1), which at1 is1 and atz gives the
power in (1). All steps are finite polynomial identities; no random-field
limit or unproved covariance estimate is hidden in this calculation.

Consequently, in the precise transformed column order just defined,

    det A(z) = 16 z^4 (z-1)^14 != 0.                      (2)

The factor16 is4 from det B_3 and4 from det(2B_1). The original translation
only multiplies each Fourier row by a nonzero phase. The original derivative
scalings, column permutation and triangular changes are invertible. Thus any
zero-variance real functional combination must vanish on these twelve modes
and hence have all coefficients zero. Positive mass at these actual modes
suffices; no numerically sampled Gram is being used as the proof.

At z=1 the paired site columns coincide. The displayed A has rank6 (also
checked exactly below), not12. Formula (2) is a spectral evaluation determinant,
NOT a determinant formula or an asymptotic equality for the Gaussian covariance.
It supplies neither a uniform contact eigenvalue floor nor a numerical radius.

## 4. Condition on pins, then use the exact physical endpoint scaling

Partition the covariance with the six pins first and the six unscaled Hessian
entries second:

    G_r = [[C_r,D_r^T],[D_r,B_r]],
    H_r = (fxx(M),fxx(S),fxy(M),fxy(S),fyy(M),fyy(S)).

C_r>0. The conditional Hessian covariance under canonical Gaussian regression
at ANY finite target is

    Sigma_r^H = B_r-D_r C_r^(-1) D_r^T > 0.

Indeed for any h!=0, evaluate the positive quadratic form G_r on
(-C_r^(-1)D_r^T h,h); the value is h^T Sigma_r^H h>0. Its covariance is target
independent; the prescribed unequal heights change the finite conditional mean
but do not invalidate this argument. No positive-probability pin event is used.

E §3.2 subtracts the two pin averages P3,P4 before dividing. Their targets are
both zero, so under these exact pins its V_r is precisely

    V_r = R_r H_r, R_r=diag(1/r,1/r,1/r,1/r,1,1).

R_r is invertible for every r>0 and |det R_r|=r^-4. Thus V_r has a smooth,
everywhere-positive Gaussian density p_r with respect to six-dimensional
Lebesgue measure. In terms of the unscaled density it is

    p_r(v)=r^4 p_r^H(R_r^(-1)v).

This Jacobian is merely a density change of variables, not an extra factor in
W or its full normalizer. Singular contact covariance remains allowed at r=0.

## 5. The full typed normalizer is finite and strictly positive, pointwise in r

Use exactly N's identity

    W_r = r^2 T_r(V_r),
    T_r(v)=[(a_-)_-(c_-)_- - r b_-^2]_+
           [r b_+^2-a_+c_+]_+.

For our range 0<r<=1, N gives 0<=T_r(v)<=||v||^4. A finite-dimensional Gaussian
has finite fourth moment, so E_Q T_r(V_r)<infinity for each fixed r. Moreover
at v*=(-1,1,0,0,-1,-1), T_r(v*)=1 for every r. Continuity makes it positive on
a nonempty open neighborhood; the full Gaussian density gives that neighborhood
positive mass. Therefore

    0<Z_r=r^2 E_Q T_r(V_r)<infinity.                       (3)

This proves positivity at each radius directly, not a uniform asymptotic floor.
The determinant/index tilted endpoint law nu_r has density

    v -> T_r(v) p_r(v) / E_Q T_r(V_r).

It is absolutely continuous; it is NOT claimed everywhere positive, since the
typed weight is zero outside the appropriate Hessian-type support.

## 6. Exact source-bound consequence: the endpoint TV distance is one

P §2's summability supplies E's Hilbert-space derivative regularity; its six
contact-jet symbols give E's G0>0. E's exact transformed target has cubic pin2,
consistent with k=1/6. Thus its contact-law description applies here, without
assuming a six-dimensional density at contact. That law is supported on

    S={a_-=-1,a_+=1,b_-+b_+=0,c_--c_+=0},

an affine two-dimensional plane in R^6. Its limiting typed weight is (Q_-)^2.
For the actual field, appending fyy(0) to the six distinct contact pin jets
keeps the jet family independent by P §2. Its one-coordinate Schur complement
is positive, hence Q is a nondegenerate real Gaussian. In particular
0<E(Q_-)^2<infinity; this is also the already resolved original LM006 input,
not a fresh claim of original-reviewer succession.

The normalized contact tilted law nu0 is consequently a probability supported
on S. By §5, nu_r(S)=0 for every allowed positive r, whereas nu0(S)=1. With
T's convention TV(mu,nu)=sup_A |mu(A)-nu(A)|,

    TV(nu_r,nu0)=1, for every 0<r<=min(1,r0), r0<24.       (4)

Thus T §5's retained actual finite-r density premise is supplied for this fixed
LM006 object. This is an application of its already reviewed obstruction, not
a refutation of LM006, N or T. It is compatible with endpoint weak/BL convergence
and with normalized-weight L1 convergence on a common latent space. Different
pushforward maps are essential. It supplies no rate for a covariance factor,
no event-boundary margin, no full-field event identification, no Palm/global
closure, and no Lean verification or independent scientific acceptance.

## 7. Exact diagnostics and exclusions

`joint_rank.py` independently expands the three small polynomial determinants
by the Leibniz formula (up to720 permutations), and compares their coefficients
with (1). Exact Gaussian-rational row elimination verifies the FULL12x12
identity(2) at nine distinct unit-circle phases, including one near1. Collision
z=1 has rank6; removing a spectral row has rank11; duplicating a jet column has
rank11. These are real negative rank controls, not crashes or parser failures.
The nine unittest methods also check the block-zero structure, distinct modes,
physical r^-4 scaling and the positive typed-weight witness at four radii.

The first run preceded implementation: nine intended missing-implementation
assertion failures, no test errors. The completed suite passes9/9 in normal
and optimized CPython3.13.5. Both exact-checker outputs are byte-identical.
These finite diagnostics supplement the ordinary proof of (1)–(4); they do not
sample or certify an infinite covariance, reconstruct source history, inspect
all downstream mathematics, run Lean or exercise repository-hosted CI.

External context was checked at the author abstract of Gass–Stecconi,
*The number of critical points of a Gaussian field: finiteness of moments*,
arXiv:2305.17586, and Lu's publisher record, *Fast Algorithms for Confluent
Vandermonde Linear Systems and Generalized Trummer's Problem*, SIAM J. Matrix
Anal. Appl.16(2),655–674(1995), DOI10.1137/S0895479893257444. These establish
related context only; no count-moment theorem, paper formula or numerical
algorithm from those abstracts is a premise of this note. No general novelty
claim is made. P's spectral identity and the explicit proof above are used.
