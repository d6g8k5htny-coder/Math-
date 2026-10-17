# Focused nonauthor review of reverse localization, Sections 2–5

17 October 2026 UTC. Reviewer: OpenAI/Codex
`/root/reverse_localization_nonauthor_review_20261017/rice_hilbert_nonauthor`.
Parent review owner:
`/root/reverse_localization_nonauthor_review_20261017`.

**Verdict: ACCEPT_SCOPED for Sections 2–5 of the exact frozen proposal. No
mathematical amendment is required within this focused scope.** The local
Hilbert regression, whole-ball birth barrier, all-Borel one-point Rice
application, fixed-angle Hessian disintegration and first-moment tail
estimates close as conventional mathematics under the explicitly imported
assumptions. This verdict does not independently accept Sections 6–8, the
reverse-fold construction, the full point-process conclusion, or any broader
universality claim. Those joins belong to the parent's integrated review.

The reviewed proposal is
`reverse-localization-author-20261017/REVERSE_LOCALIZATION_PROPOSAL.md`,
**38,534 UTF-8 bytes**, SHA-256
`8e48835527e283b45acdff4f604b385bd9dec4f8b1fcd1b54bbd52d44099a794`.
The byte identity was independently reproduced before and after this review.
This is a fresh source-exposed nonauthor mathematical reconstruction. The
reviewer did not write the proposal or contribute its author-side sketch or
controls. All agents involved are OpenAI/Codex; organizational-independence
credit is **0**, and this is not blind, human or provider-distinct review.
No Lean compilation, kernel audit, production/source adoption, scientific
promotion, field draw, numerical Rice integral, GitHub/Drive/R17 write or
status change was performed. All new files are confined to this child review
directory.

## 1. Exact scope and imports

The review reads Sections 2–5 in full and reconstructs the displayed
interfaces rather than treating an earlier accepted review as acceptance of
these new bytes. Section 1 and the neighboring localization/exhaustion text
were inspected for interface context. The complete read scopes and actual
byte identities are in `INPUT_IDENTITIES_BEFORE.json`; the final manifest
uses paths relative to the core audit directory and the child output
directory.

The important consumed sources are:

* `UNIFORM_LOCAL_NORM_DIAGONAL_PROPOSAL.md`, 26,687 bytes, SHA-256
  `8e1eefca9888d43824a9fd9caca34c44d2de4bf8e30c668b474fa2097491c76b`,
  Sections 1–6. These supply the fixed cutoff, normalized variance plus
  uniform physical twelfth moment, Hilbert trace bound and explicit
  directional derivative bounds.
* `HIGHER_CONFIGURATION_GAUSSIAN_ROUTE.md`, 32,938 bytes, SHA-256
  `43bd77fd5320a717c77bba28c1a6eec080ff67db56c911c6ddea5351a1279b7e`,
  the exact Gaussian square-truncation family and its Section 1 covariance
  and spectral-moment comparison. No fresh full audit of the higher-point
  proof is claimed by this focused reviewer.
* `experiments/universality/finite_candidate_lifetime/PROOF.md`, 29,190
  bytes, SHA-256
  `ed31f562f0ffaaf6d4bd2ceb1ae3d234798e983a55d55c6983b128fce27133f5`,
  especially Sections 4–6. Its named equal-dimensional weighted area
  theorem and coefficient-incidence construction are relevant. The new
  one-point application is checked directly below.
* `experiments/universality/finite_h0_lifetime/PROOF.md`, 27,064 bytes,
  SHA-256
  `5ea91111fa5f3d78d7c4188ebe84b3bc2c452b05dfdfc62c74b03123cb2696d1`,
  Sections 3–4. These establish the Borel elder-death threshold, exclude the
  essential class, and count every finite ordinary-H0 elder bar exactly once
  by its maximum on the compact Morse/distinct-value locus.

The equal-dimensional weighted area formula is an explicit classical import
with nonnegative Borel integrands. This review accepts that named theorem
with the source's stated read limits; it does not claim to have obtained or
audited the complete licensed Federer book. The finite-field source separately
establishes almost-sure Morse genericity by coefficient incidence and Sard
before Rice is used.

For primary-source context, I freshly inspected Sections 2, 3.2 and 5 of
Armentano–Azaïs–León, [*On a general Kac-Rice formula for the measure of a
level set*, arXiv:2304.07424v3](https://arxiv.org/html/2304.07424v3).
The Gaussian theorem and its distinction between fixed and almost-every
levels agree with the role assigned in the proposal. Its unmarked result is
context, not the justification for the arbitrary Borel elder/norm mark here.
The latter follows from the explicit coefficient-incidence argument.
The retained 622,641-byte primary HTML was hashed; that is not a claim to a
full-paper audit.

## 2. The localized norm and its Gaussian regression are dimension-free

At every deterministic integration location x, define the real Hilbert-space
variable `Y_x(z)=chi_b(z)F(x+z)` in `H^6(R^2)` and `N_x=1+||Y_x||`.
The cutoff is fixed in the physical coordinate axes. It equals one on the
axis-aligned square of radius `2b`; any rotated square of radius b is inside
that region because `sqrt(2)b<2b`. Thus the existing full multilinear
`D^3` and `D^4` operator bounds apply in arbitrary eigenframes, without
rotating the cutoff or assuming isotropy of the finite field.

For each finite law, x-to-`Y_x` is smooth into this Hilbert space: the field
is a finite sum of smooth trigonometric coefficient functions multiplied by
a fixed compact smooth cutoff. Joint continuity in x and the coefficient
vector makes the norm a Borel coefficient/location mark. Periodic lifts
handle seam points. Stationarity, not rotation invariance, makes its law
independent of x.

Write `Y_x=A_x Z` for the actual finite standard real Gaussian coefficient
vector. The inherited uniform trace calculation gives

`||A_x||_HS^2 = E||Y_x||^2 <= T`.

This estimate uses both `sum q_n=1` and the uniform physical twelfth spectral
moment. A bound on the latter alone would not control the DC variance. The
declared Gaussian square truncations supply both premises. No bound involving
the mean norm of the entire coefficient vector is used.

For a fixed deterministic frame e, let `J=LZ` be the seven raw contact
coordinates. The Euclidean limiting covariance has positive even and odd
blocks. The linear combinations

`(F,F_ee+F,F_vv+F,F_ev)` and `(F_e,F_v,T+3F_e)`

have diagonal covariances `(1,2,2,1)` and `(1,1,6)`, respectively. Parity
makes the blocks independent. The uniform through-order-six covariance
comparison for the declared family, together with compactness of the frame
circle, yields eventual constants `m0 I <= LL^T <= M0 I`. This does not
assert isotropy of a finite truncation or positive conditional covariance of
coordinates already pinned.

The resulting seven-dimensional density satisfies

`p(z) <= (2pi)^(-7/2)m0^(-7/2) exp[-|z|^2/(2M0)]`.

This proves the proposal's uniform Gaussian envelope. Both the lower and
upper covariance bounds have a role: the lower one bounds the prefactor,
and the upper one supplies uniform decay in the target.

For every target z, the canonical coefficient conditional law is

`Z = L^T Gamma^(-1)z + PZ'`,
`P=I-L^T Gamma^(-1)L`, `Gamma=LL^T`.

Here `P=P^T=P^2` and `0<=P<=I`. Consequently

`||(A_x L^T Gamma^(-1))z|| <= sqrt(T/m0)|z|`,
`Q=A_x P A_x^*`, `tr Q <= T`.

The second inequality is a covariance contraction in the Hilbert image of
`A_x`; it does not require A and P to commute, and it is not an assertion
about a generic algebraic slice. In the finite-dimensional Hilbert image,
diagonalization of Q gives

`E||A_x PZ'||^4 = (tr Q)^2+2tr(Q^2) <= 3T^2`.

Apply the triangle inequality and the elementary three-term fourth-power
bound to `1+||mean||+||centered||`. This yields

`E[N_x^4 | J=z] <= C4(1+|z|)^4`

at every target, with no coefficient-dimension factor. Padding the source
coefficient vector with unused coordinates would leave A, L and this bound
unchanged, whereas using `E||Z||^4` would introduce a false dimension cost.
Conversely, deleting the target growth is not licensed: in the scalar example
`Y=Z`, `J=Z`, the fourth conditional moment of Y is `z^4`. The proposal
retains the necessary target dependence.

At `z=(b0,0,-lambda,T,0,0,-mu)` with `lambda<=min(1,mu)`,
`1+|z| <= C(1+mu+|b0|+|T|)=C W0`. In the hard branch
`1<lambda<mu`, the same comparison holds with a different numerical C.
These are the two comparisons actually needed later; no uniform-in-target
centered-law shortcut has entered.

## 3. The birth barrier does not presume a local saddle

Let M be a nondegenerate maximum and `lambda>0` its smaller Hessian magnitude.
On the embedded radius-b ball, the local norm gives the deterministic bound
`||D^3F||op <= p3 N_M`. Put `c0=min(b,1/p3)` and choose

`rho=c0 min(lambda,1)/N_M`.

Then `rho<=b`, `p3 N_M rho<=lambda`, and Taylor's formula along any radial
segment from M gives

`F(M+z) <= F(M)-lambda|z|^2/2 + p3 N_M |z|^3/6`
`         <= F(M)-lambda|z|^2/3`, for `|z|<=rho`.

The ball is embedded because b is below the fixed injectivity-radius
margin. Its interior contains no point higher than M, and its entire sphere
is at most `F(M)-lambda rho^2/3`. Every continuous path from M to a point
higher than M must meet that sphere. Hence no strict-superlevel path above
the sphere bound can reach an older point. The intrinsic rational
strict-clearance supremum from the exact H0 source is therefore at most
that bound.

For a finite bar at M this proves

`ell >= c0^2 lambda^3/(3N_M^2)`, for `lambda<=1`,
`ell >= c0^2/(3N_M^2)`, for `lambda>1`.

The second line merely weakens its true factor lambda. These necessary
conditions are independent of the existence, position or identity of any
nearby saddle. The essential maximum is excluded before talking about a
finite lifetime. There is no attempt to prove the old false whole-boundary
claim for a fixed fold-isolation square: this is a different ball with
radius shrinking with the soft curvature.

## 4. Literal-target all-Borel Rice is justified by coefficient incidence

The marked formula needed here is stronger than an unmarked Rice theorem
or a continuous-mark result. I checked its actual finite-dimensional
construction. On a torus coordinate patch choose an invertible two-column
minor `B_C(x)` of the coefficient matrix for `grad F(x)`. Such minors exist
because the gradient covariance is positive definite. Split coefficients
as `(zeta,eta)` and solve the literal critical equation as

`zeta=a(x,eta)=-B_C(x)^(-1)B_D(x)eta`.

The equal-dimensional incidence map
`Phi(x,eta)=(a(x,eta),eta)` is smooth on that patch times coefficient space.
At a solution, differentiation at fixed full coefficient vector gives

`D_x a=-B_C^(-1) Hess F(x)`,
`|det D Phi|=|det Hess F(x)|/|det B_C(x)|`.

The full derivative also contains eta derivatives, but its lower block is
`(0,I)`; they do not create an additional determinant. Apply the explicitly
imported weighted area theorem to
`rho_N(Phi(x,eta))w(x,Phi(x,eta))`, with any nonnegative Borel w. Localize
to bounded regions as necessary, then use nonnegative monotone convergence.
Preimages of a coefficient vector are exactly its critical points in the
patch. A disjoint Borel partition subordinate to the minor patches removes
overlap. Although the number of possible minors changes with coefficient
dimension, it does not become an estimate factor: the partition rejoins to
one integral over the physical torus.

At each fixed x, the affine fiber integral divided by `|det B_C(x)|`
is precisely `p_gradF(x)(0)` times the canonical Gaussian conditional
expectation at **target 0**. This is a pointwise identity of the explicit
Gaussian affine-fiber measures. No passage from an almost-every target
identity to the exceptional target zero is required, and the conditional
kernel is not left unspecified on a null set of targets.

The result is exactly

`E sum_(gradF(x)=0) w(x,Z)`
` = integral_X p_gradF(x)(0)`
`        E[|det Hess F(x)| w(x,Z) | gradF(x)=0] dx`.

The determinant occurs once. Genericity is separately known from the
source's coefficient-incidence/Sard argument, so there is no
Morse-to-Rice-to-Morse circularity. Finiteness of the desired short-bar
expectations is derived from the estimates, not assumed to license the
nonnegative formula.

For precision, the actual global bar mark may be written as

`1_G(Z) 1_(M is a maximum) 1_(d_Z(M) finite)`
`  1_(0<F(M)-d_Z(M)<=St) times the desired local jet/norm mark`,

where G is the unconditional full-measure compact Morse/distinct-value
locus. The finite H0 source makes `d_Z(M)` jointly Borel and identifies one
finite bar per nonessential maximum on G. Thus the nonlocal dependence
causes no continuity problem. The whole-ball inequality bounds this actual
mark by a local event on G. Only after that point is `1_G` dropped to obtain
an upper bound. It is unnecessary, and would be unjustified merely from
unconditional genericity, to assert that every conditional coefficient
fiber is Morse. The proposal does not make that assertion.

Counting one maximum per bar is decisive. There is only the x integral,
whose mass is V. Uniformity in x then costs V, not `V^2`. No endpoint-pair
enumeration or additional physical Hessian determinant is hidden in the
bar mark.

## 5. The eigenline density formula has the stated Jacobian and multiplicity

At a maximum with distinct Hessian eigenvalues, write

`H=Q_theta diag(-lambda,-mu)Q_theta^T`,
`0<lambda<mu`, `0<=theta<pi`.

This parametrizes the soft eigenline once. At theta zero, differentiating
the raw coordinates `(H11,H12,H22)` in `(lambda,mu,theta)` gives determinant
of absolute value `mu-lambda`; rotation preserves that determinant.
Conjugation on the three raw symmetric-matrix coordinates has determinant
one, as does rotation of the two gradient coordinates. Thus the area factor
multiplies the Rice determinant `lambda mu` to give

`lambda mu(mu-lambda) d lambda d mu d theta`.

There is no factor two from the eigenline. Both signs of the scalar cubic T
are still integrated over `R`; orienting the soft direction to make T
positive later does not require a second copy of this counting measure.
Repeated eigenvalues occupy a Lebesgue-null fixed-point Hessian set. The
marked Rice identity applied to that event shows there are almost surely
no such critical points. This conclusion does not rely on a two-site
second-jet covariance assumption.

The random-frame pitfall is also avoided. First condition on the physical
height, gradient and Hessian. Given a Hessian value, theta is a deterministic
integration parameter; add its scalar directional cubic row and use the
corresponding canonical Gaussian kernel. After changing Hessian variables,
this is equivalent, for each fixed integration theta, to the seven-jet
density with target

`z=(b0,0,-lambda,T,0,0,-mu)`.

The gradient density at zero is already part of that seven-dimensional
joint density. It must not be inserted again. The actual conditional
expectation of a general coefficient mark uses the same deterministic
theta kernel. No assertion equates conditioning on a selected random frame
with conditioning in an unrelated fixed frame, and no derivative of theta
appears in the scalar conditional disintegration. This verifies (13a),
including its normalizations.

## 6. The integrable envelope and every tail exponent check

For the soft branch, the necessary short-bar condition gives

`N_M^2 >= lambda^3/(C_S t)`.

Conditional Markov applied to the fourth moment, together with the trivial
probability bound one, gives

`P(necessary event | J=z)`
` <= min(1,C_S' W0^4 t^2 lambda^(-6))`.

For the integration in lambda, W0 depends only on mu, b0 and T. Dropping the
nonnegative lambda Gaussian and enlarging the lambda interval gives an
upper bound. Splitting at `lambda_*=(D t^2)^(1/6)` yields

`integral_0^infinity lambda min(1,D t^2 lambda^(-6)) d lambda`
` = (1/2+1/4)D^(1/3)t^(2/3)`.

This proves the coefficient `3/4` and the powers in (16). Since
`lambda mu(mu-lambda)<=lambda mu^2`, the resulting envelope is a constant
times

`V t^(2/3) mu^2 W0^(4/3) exp[-c(mu^2+b0^2+T^2)]`.

It is integrable over `mu>0,b0,T in R`, uniformly in theta. The polynomial
does not interfere with Gaussian tails, including at mu zero where `mu^2`
is integrable. No bound on the norm of the full Fourier coefficient vector
or a high-probability global cover event is needed at this step.

For the hard branch `1<lambda<mu`, short lifetime requires
`N_M^2>=c_S/t`. The same fourth-moment calculation gives a probability
bound `C_S t^2 W0^4`. Its remaining lambda/Hessian integral has a finite
Gaussian polynomial moment because lambda is below mu. Hence the error is
`O_S(V t^2)`. Under `V t^(2/3)->v_*`, it is `O_S(t^(4/3))` and vanishes
absolutely.

I independently checked each cutoff consequence:

* **Hard-curvature degeneration.** For `mu<a<=1`, the hard branch is absent.
  Integrate the `mu^2` envelope from 0 to a and bound its other factors
  uniformly there. The result is `C_S V t^(2/3) a^3`.
* **Vanishing soft cubic.** For `|T|<tau<=1`, the envelope is uniformly
  integrable in mu and b0 with T in that bounded interval. Its integral is
  `C_S V t^(2/3) tau`, plus the allowed full hard-branch error. This does not
  require independence between T and the Hessian or the height.
* **Large jet/height marks.** Restrict the integrable envelope to the union
  `mu>A or |b0|>H or |T|>U`. Dominated convergence gives a deterministic
  tail function tending to zero as all three bounds tend to infinity.
  The constants do not depend on unrelated lower cutoffs or R.
* **Localized-norm tail.** The two necessary lower thresholds on N combine
  as a maximum, not a product of probabilities. Thus the soft conditional
  bound is `C W0^4 min(R^(-4),C_S^2 t^2 lambda^(-6))`. Splitting its lambda
  integral at `D^(1/6)t^(1/3)R^(2/3)` gives
  `(3/4)D^(1/3)t^(2/3)R^(-8/3)`. The factor W0 has power four outside the
  minimum, as the proposal correctly says; its Gaussian integral remains
  finite. The norm-tail result is `C_S V t^(2/3)R^(-8/3)+C_S Vt^2`.
* **Arbitrarily small lifetimes.** Replacing the cap St by `epsilon t`
  changes the soft Markov numerator by `epsilon^2` and hence its integrated
  contribution by `epsilon^(2/3)`. The hard contribution changes by
  `epsilon^2`. The cumulative bound (24) follows directly; differentiating
  it to claim a density bound would be an extra, unproved step, and is not
  used here.

These are first-moment bounds on actual finite elder bars. Their constants
are uniform in moving coefficient dimension, spatial position and the
deterministic angle. The cutoff parameters are fixed before taking the
small-t limit. Constants in the additive bounds can be chosen independently
of the cutoffs within their declared ranges; the localization threshold in
the parent's later step may depend on the chosen cutoffs. No exchange of
those quantifiers is required by Sections 2–5.

## 7. Disposition and limitations

There is **no must-fix mathematical finding in this focused scope**. The
following distinctions are necessary to the acceptance and are already
present in the frozen proposal:

1. The Hilbert trace and seven-jet covariance estimates use the declared
   normalized Gaussian truncation family, not arbitrary growing spectra.
2. The weighted area theorem remains an explicit conventional import.
   AAL's unmarked Gaussian theorem is not promoted to a theorem for every
   arbitrary Borel nonlocal mark without the incidence argument.
3. The global Morse/distinct-value indicator is retained in the actual bar
   mark before deterministic domination; no conditional genericity is
   assumed.
4. The whole-ball barrier proves a necessary short-lifetime condition before
   any local saddle is constructed.
5. The eigenline angle has length pi, the cubic is integrated with both
   signs, the Gaussian joint density includes gradient pins once, and the
   Rice determinant appears once.
6. The resulting control is first moment. It does not establish convergence
   of unmarked factorial moments of order greater than one, and it is not
   by itself the full marked or projected point-process theorem.

No author controls, old accepted controls, numerical experiments or parent
controls were rerun. No new executable mathematical controls were necessary
for this focused review; the evidence is the independent reconstruction
above and exact source-identity verification. The parent has a separate
new-control record, which this child verdict does not claim to execute or
independently reproduce. No consumed source bytes were changed.

The focused recommendation is therefore **ACCEPT_SCOPED, no amendment**, to
be joined only with the parent's actual independent review of reverse-fold
existence, elder localization, compact exhaustion and the final process
transfer. The full persistence/universality objective remains unmet.
