# Reverse localization and the full microscopic H0 process in one Gaussian family

17 October 2026 UTC. **New conventional mathematical author proposal; separate nonauthor review is required.** Authors: OpenAI/Codex Root (mechanism, problem selection and sketch) and `/root/reverse_global_bar_localization_20261017` (reconstruction, attack, source joins and this proof). Same-provider organizational-independence credit 0. This is not Lean verification, source adoption, a field experiment, a scientific-status transition or a theorem for arbitrary spectra. Accepted source/proposal/review bytes are unchanged. All new files are confined to `reverse-localization-author-20261017/`.

The new argument counts a short bar by its **one birth maximum**, uses a whole small-ball barrier at that maximum, and obtains conditional local Sobolev moments by actual finite Gaussian regression. This proves an integrable bound on the birth jets of short bars. Away from the excluded birth-jet sectors it constructs the nearby saddle by the intermediate value theorem and then consumes the accepted asymmetric trap to identify the actual elder death. The resulting first-moment complement permits the full lifetime/spatial Poisson projection. It does not, by itself, prove convergence of unmarked factorial moments of order greater than one.

## 1. Exact source family, observable and consumed results

Keep exactly the family in `HIGHER_CONFIGURATION_GAUSSIAN_ROUTE.md`, 32938 B / SHA-256 `43bd77fd5320a717c77bba28c1a6eec080ff67db56c911c6ddea5351a1279b7e`:

```text
L(t)t^(1/3) -> ell_* in (0,infinity),
Lambda_*(t)^2 ~ B log(1/t), for ONE fixed B>0,
K(t)=ceil(L(t)Lambda_*(t)/(2pi)),
q_(t,n) proportional to exp(-|(2pi/L(t))n|^2/2),
                          |n|infinity<=K(t).
```

Every q is positive, symmetric and normalized. Use the original independent standard real DC/sine/cosine coefficients, not a finite-word sampler or an independent-copy field. Write `V=L^2` and `v_*=lim Vt^(2/3)=ell_*^2`. Each member is a finite smooth Gaussian field on the square torus. No common realization over uncountably many t is needed.

The exact consumed conventional source is Main `85b928b326ff0586715a56ae91f51d3fbd89557a`, with the following complete bodies read:

| Source | Bytes / SHA-256 | Content used |
|---|---|---|
| `finite_gaussian_contact/PROOF.md` | 25367 / `7fea2656e11d986e1a5d6bfb0a05c8421bd93262d28051b8cfef05320595f474` | Real Gaussian source, physical derivatives, finite regression, contact functional |
| `finite_candidate_lifetime/PROOF.md` | 29190 / `ed31f562f0ffaaf6d4bd2ceb1ae3d234798e983a55d55c6983b128fce27133f5` | §§4–6 Morse/distinct locus, all-Borel coefficient-area argument, Gaussian disintegration; §10 coefficient normalization |
| `finite_h0_lifetime/PROOF.md` | 27064 / `5ea91111fa5f3d78d7c4188ebe84b3bc2c452b05dfdfc62c74b03123cb2696d1` | §§3–4 intrinsic Borel elder death, actual finite Morse-component/elder-basis induction, unique maximum/bar once-counting and selector (7) |

The last result is consumed with its explicitly stated local normal-form and critical-free-flow imports. It proves on the compact Morse/distinct locus that every maximum except the unique global maximum has exactly one finite H0 elder bar, dying at one unique quotient index-one merger saddle; each finite bar is counted once by its maximum. It does **not** already prove that the physical endpoints approach each other uniformly in this changing family. That is the question here. The essential class is excluded throughout.

The exact accepted local inputs, read in full within their mathematical scopes, are:

* Isolation proposal `827c82953845eb12005542ff6a4e1c99886b68d1ea9f1aeae16f981622ac6a30` and its review `f06c61e3f3e60c795a1a14e824640f1689d4143dba4f6698cada7a41929eec90`.
* Uniform local-norm proposal `8e1eefca9888d43824a9fd9caca34c44d2de4bf8e30c668b474fa2097491c76b` and its review `ff552dfacadede53405530a219302c1163dca8ba97d518f02d407970d3de3c1c`.
* Higher-configuration proposal above and integrated review, 26385 B / `21a93d3626032c954338e2de638db61040833c6e578526613c4d14b128be8012`.
* Asymmetric proposal, 28291 B / `6d07631c068019bf9f081ad0b6f50325679e3ab554f221265e002d5c047f17ac`, and integrated review, 25687 B / `16678abc7de50986b0fc6d54303449bf1b4c5ba8b10f6a3ccc7f9d03a97a4e9f`.

The latter accepted join gives compact regular-mark convergence for the actual elder-selected process Y_t, with mark space

`E=(0,infinity)_s x R_b x (0,infinity)_k x (-infinity,0)_A x T_1^2_y x S^1_u`

and intensity

```text
nu = v_*144 s^(-1/3) k^(4/3) A^2
       p_Jinfty,u(b,0,0,12k,0,0,A)
           ds db dk dA dy d sigma(u),   A<0.             (1)
```

Here `s=ell/t`, `k=ell/r^3`, `A=F_vv(M)`, `y=M/L`, `u=(S-M)/r`, `v=Ju`, and r is the endpoint distance. The circle measure is ordinary arclength of mass 2pi. This accepted conclusion is compact/vague; the needed singular/unbounded-mark complement is not an imported premise.

All listed identities, including the Root sketch, are bound by `INPUT_IDENTITIES_BEFORE.json` and checked again at freezing. Prior controls are not rerun. Full old reviews are not claimed to review these new bytes.

## 2. A local Gaussian Hilbert norm at each deterministic location

Choose a fixed `Lmin>0` valid eventually and use the accepted cutoff construction with

```text
b=min(1,Lmin/16),  chi_b=1 on [-2b,2b]^2,
support chi_b subset [-3b,3b]^2,   6b<Lmin,
H=H^6(R^2;R),
Y_x(z)=chi_b(z) F(x+z),
N_x=1+||Y_x||_H >=1.                                  (2)
```

The periodic lift defines this function for every x, including seam points. The support is embedded. This uses a cutoff centered at the **deterministic Rice integration location x**; no grid or field-selected Gaussian conditioning is used. For each finite field, `(x,xi)->Y_x` is continuous into H. Thus N_x is a jointly Borel coefficient/location mark. Stationarity makes its law independent of x. The fixed-axis cutoff need not be rotated with an eigenframe.

The accepted source comparison supplies normalized variance and a uniform physical twelfth moment. The local-norm proof gives a uniform finite number T such that, writing the actual finite standard Gaussian coefficient vector as Z,

```text
Y_x=A_x Z,    ||A_x||_HS^2=E||Y_x||_H^2 <=T.           (3)
```

On every rotated radius-b square around x, the cutoff is identically one because `sqrt(2)b<2b`. The accepted Fourier calculation gives, in arbitrary unit directions,

```text
sup ||D^3F||op <= p3 N_x,  p3=1/15,
sup ||D^4F||op <= p4 N_x,  p4=2/15                     (4)
```

there. The same holds on the radius-b ball. Constants p3,p4 are rational upper bounds, not isotropy assumptions. The trace bound controls the norm in the growing coefficient space without using `E||Z||^q`, which would introduce its dimension.

For a **fixed** oriented frame `(e,v=Je)`, put

`J_(x,e)=(F,F_e,F_ee,F_eee,F_v,F_ev,F_vv)(x)=L_(x,e) Z`.

Eventually, uniformly in x,e,t,

```text
m0 I <= Gamma=L L^T <= M0 I,   0<m0<=M0<infinity.       (5)
```

This follows either from the accepted p=1 floor and covariance approximation or directly from the following limit covariance. In the Euclidean Gaussian limit, the odd block `(F_e,F_v,T=F_eee)` has variances `(1,1,15)` and only nonzero off-diagonal covariance `Cov(F_e,T)=-3`. The even block `(F,F_ee,F_ev,F_vv)` has covariance of `(F,F_ee,F_vv)` equal to

```text
[[ 1,-1,-1],
 [-1, 3, 1],
 [-1, 1, 3]],
```

with independent `F_ev` of variance 1. Indeed `(F,F_ee+F,F_vv+F,F_ev)` has diagonal covariance `(1,2,2,1)`, and `(F_e,F_v,T+3F_e)` has diagonal covariance `(1,1,6)`. Both blocks are positive definite. Odd and even blocks are independent. Isotropy of the **limit**, together with the accepted uniform derivative-covariance convergence through order six, gives (5) for the actual generally nonisotropic finite torus law. The upper bound also follows from the uniform physical moment.

The density therefore obeys

`p_(t,e)(z) <= C exp(-c|z|^2)`                           (6)

uniformly. This is an unconditional seven-coordinate density. It is not a positive conditional covariance assertion for pinned coordinates.

### Actual conditional fourth moment

For every target z define the canonical finite Gaussian regression

```text
Z=L^T Gamma^-1 z + P Z',
P=I-L^T Gamma^-1 L,
Y_x=A_x L^T Gamma^-1 z + A_x P Z'.                     (7)
```

P is an orthogonal projection. The conditional H-mean has norm at most

`||A_x||op ||L^T Gamma^-1||op |z| <=sqrt(T/m0)|z|`.

The conditional centered covariance has trace `tr(A_x P A_x^*)<=T`; this inequality follows from `0<=P<=I`, not from a statement about an algebraically generic regression fiber. In the finite-dimensional image of A_x, orthogonal diagonalization gives

`E||A_x P Z'||^4=(tr Q)^2+2tr(Q^2)<=3T^2`.

Since `(a+b+c)^4<=27(a^4+b^4+c^4)` for nonnegative a,b,c,

```text
E[N_x^4 | J_(x,e)=z] <= C4 (1+|z|)^4.                 (8)
```

This is an all-target canonical conditional bound, uniform in coefficient dimension, x,e,t. The same calculation gives every fixed positive moment with a moment-dependent constant, but only (8) is needed. An unconditioned tail alone would not justify it. In particular conditional means grow with z; a purported bound independent of arbitrary z is false even in a one-dimensional Gaussian example.

## 3. A genuine whole-ball birth barrier

Let M be a nondegenerate maximum with height m and soft Hessian magnitude lambda>0, so `Hess F(M)<=-lambda I`. Use N=N_M and put

`c0=min(b,1/p3)>0`.

For `0<lambda<=1`, choose `rho=c0 lambda/N`. For lambda>1 choose `rho=c0/N`. In both cases `rho<=b` and `p3 N rho<=lambda`. Taylor along every radial segment, using criticality at M and (4), gives for |z|<=rho

```text
F(M+z) <= m-lambda |z|^2/2+(p3N)|z|^3/6
         <= m-lambda |z|^2/3.                          (9)
```

Thus there is no point of height greater than m inside the ball; its entire sphere is at most `m-lambda rho^2/3`. Any path to a higher point must cross that sphere. The strict-clearance elder threshold is consequently at most that sphere height. For the finite bar attached to M by the exact source §4,

```text
ell >= c0^2 lambda^3/(3N^2),       0<lambda<=1,
ell >= c0^2/(3N^2),               lambda>1.             (10)
```

The second inequality weakens the factor lambda>1 and is sufficient. This is a ball whose radius **shrinks with the soft eigenvalue**. It is unrelated to the false assertion that the full boundary of a fixed fold-isolation square lies below the maximum. That previous counterexample remains false and unchanged: the outgoing older ridge arm is outside the small birth ball.

Fix S>0. Every finite bar with `ell<=St` satisfies, respectively,

```text
lambda^3 <= C_S t N^2,       lambda<=1,
N^2 >= c_S/t,                lambda>1,                (11)
```

where `C_S=3S/c0^2`, `c_S=c0^2/(3S)`. These are deterministic necessary conditions. No local saddle, radius comparison, elder selector or desired correspondence has been assumed to obtain them.

## 4. All-Borel one-point Rice, and why there is only one volume factor

Here is the finite-dimensional counting statement needed for the random norm mark. For any nonnegative Borel w(x,xi),

```text
E sum_(gradF(x)=0) w(x,xi)
 = integral_X p_gradF(x)(0)
       E[|det Hess F(x)| w(x,xi) | gradF(x)=0] dx.       (12)
```

We use the equal-dimensional **weighted area formula**, with a nonnegative Borel integrand, as an explicit classical import, exactly as `finite_candidate_lifetime/PROOF.md` §§4–5 does: for a locally Lipschitz map Phi between equal-dimensional Euclidean domains and h>=0 Borel,

`integral h(z)|det D Phi(z)| dz = integral sum_(Phi(z)=xi) h(z) dxi`,

as an extended nonnegative equality, with countable localization where necessary. Its named classical source and read-status limits are those of the consumed candidate proof; no new licensed Federer-book audit is claimed. The new single-point application is as follows. On a coordinate patch choose two invertible gradient coefficient columns `B_C(x)`. Write the critical equation as `zeta=a(x,eta)=-B_C^-1 B_D eta`. The incidence map `Phi(x,eta)=(a(x,eta),eta)` has equal-dimensional domain and target. Differentiating the constraint at its solution gives

`D_x a=-B_C^-1 Hess F(x)`,
`|det D Phi|=|det Hess F(x)|/|det B_C(x)|`.

Apply the weighted area formula with `rho_N(Phi)w(x,Phi)`. Localize in coefficients and chart positions and use monotone convergence. A disjoint Borel partition subordinate to the nonzero minors avoids double counting. At fixed x the linear change `(zeta,eta)->(gradF(x),eta)` has determinant `|det B_C|`. Gaussian disintegration yields (12) at the literal gradient target 0. This is a coefficient-incidence formula at a fixed target, not an almost-every-target coarea argument. Rank follows already from (5). The field is almost surely Morse before this formula, by the source's independent Sard argument; no Morse/Rice cycle occurs.

This derivation allows w to depend on **all** coefficients through N_x and even through a Borel global lifetime. For our upper bounds only the local necessary conditions (11) and local jet/norm events are needed. All Borel assertions follow from the actual finite coefficient fields and the source's finite Morse branches; there is no continuous-mark-only Rice substitution. No conditional fiber is assumed Morse.

For primary-source context I freshly inspected Armentano–Azaïs–León, [*On a general Kac-Rice formula for the measure of a level set*, arXiv:2304.07424v3](https://arxiv.org/html/2304.07424v3), §§2 and 5. Their unmarked Gaussian result supports the framework; the arbitrary Borel norm mark here is justified by the displayed coefficient-incidence application, with the weighted area formula named explicitly. A classical theorem is imported, not claimed to have been proved by finite controls.

We apply (12) to birth **maxima**, one per finite bar, rather than to all max/saddle endpoint pairs. The spatial integral is over x once. Since all bounds below are uniform in x, it costs exactly V. There is no V^2 factor and no extra physical Hessian determinant in w.

### Eigenframe coordinates without conditioning on a selected frame

At a maximum let its eigenvalues be `-lambda,-mu`, with `0<lambda<mu`. Write

`H=Q_theta diag(-lambda,-mu) Q_theta^T`, `0<=theta<pi`.

This is a once-only parametrization of the soft eigenline, except null boundaries and repeated eigenvalues. Direct differentiation of the three entries `(H11,H12,H22)` gives the absolute Jacobian `mu-lambda`. Conjugation by a fixed rotation has determinant one on these three raw symmetric-matrix coordinates; physical gradient rotation also has absolute determinant one. Thus the maximum factor in (12) is

`lambda mu (mu-lambda) d lambda d mu d theta`.          (13)

Repeated Hessian eigenvalues have zero Lebesgue measure under the fixed-point Hessian conditional density; (12) shows the expected number of such critical points is zero. They can be removed almost surely. No arbitrary two-site second-jet rank is used.

To include T=F_eee, first disintegrate the coefficient law given the fixed-point F, gradient and physical Hessian. For each value of that Hessian substitute its deterministic theta in the scalar directional row and its canonical conditional law. Equivalently, after the Hessian change of variables, for each integration theta use the seven-coordinate density p_(t,e_theta) and the regression (7). The Hessian entries in that frame are exactly `(-lambda,0,-mu)`. This is a measurable-kernel disintegration for deterministic integration parameters. It does not assert the original law conditioned on a random eigenframe is the law for a fixed frame. No derivative of theta contributes another Jacobian in this conditional disintegration.

Explicitly, the resulting formula for a nonnegative Borel maximum mark w is

```text
E sum_(M maximum) w(M,xi)
 = integral_X integral_(theta in[0,pi)) integral_(mu>0)
       integral_(0<lambda<mu) integral_R integral_R
       lambda mu(mu-lambda) p_(t,e_theta)(z)
                     E[w(x,xi)|J_(x,e_theta)=z]
                dT db0 dlambda dmu dtheta dx,
z=(b0,0,-lambda,T,0,0,-mu).                           (13a)
```

The canonical kernels in (7) depend continuously on the deterministic frame and target, so the required measurability is available. Formula (13a) is the precise density-and-weight interface used below.

For `lambda<=min(1,mu)`, set

`W0=1+mu+|b0|+|T|`.

At the target `z=(b0,0,-lambda,T,0,0,-mu)`, (6) and (8) give

```text
p_(t,e)(z) <= C exp[-c(b0^2+mu^2+lambda^2+T^2)],
E[N_x^4|J=z] <= C W0^4.                              (14)
```

Constants are uniform in all integration theta. Choosing e's sign to make T positive later does not double (13). For estimates we integrate both signs of T on this single eigenline domain.

## 5. Integrable short-bar domination and all birth-jet tails

By (11), (14) and conditional Markov,

```text
P(ell<=St necessary condition | J=z)
 <= min(1, D_S W0^4 t^2 lambda^-6),     lambda<=1.      (15)
```

The left phrase means the local necessary event in (11), not an assumed conditional lifetime law. Replacing the actual short-bar mark by this event increases its Rice count.

The key exact integral, for D>0, is

```text
integral_0^infinity lambda min(1,D t^2 lambda^-6) dlambda
 = (3/4) D^(1/3)t^(2/3).                             (16)
```

Split at `lambda_*=D^(1/6)t^(1/3)`; the lower and upper contributions are respectively `lambda_*^2/2` and `lambda_*^2/4`. We may extend `0<lambda<=min(1,mu)` to this larger integration domain after dropping its Gaussian factor. Since `lambda mu(mu-lambda)<=lambda mu^2`, every first-moment short-bar estimate is bounded by

```text
C_S Vt^(2/3) integral mu^2 W0^(4/3)
                  exp[-c(mu^2+b0^2+T^2)] dmu db0 dT,
                           mu>0,                      (17)
```

times the fixed theta length pi. This integral is finite. It is a genuine uniform Palm-weighted bound, rather than a growing global norm event.

For lambda>1, (11) and (8) instead give probability at most `C_S t^2 W0^4`, now with `W0=1+mu+|b0|+|T|` still controlling lambda since lambda<=mu. Integration of the factor in (13) and the density (14) over `1<lambda<mu` has a finite Gaussian polynomial moment. Therefore

`E[number of short bars with lambda>1] <= C_S Vt^2`.   (18)

This tends to zero absolutely in the declared family. It is `O(t^(4/3))`, because `V=O(t^-2/3)`. It is not merely bounded per area while a second spatial integral diverges.

The same estimates, with marks restricting the birth jet, give for `0<a<=1`, `0<tau<=1`:

```text
E short bars with mu<a
       <= C_S Vt^(2/3) a^3,
E short bars with |T|<tau
       <= C_S Vt^(2/3) tau + C_S Vt^2,                (19)
```

where the first event cannot intersect lambda>1. For the first line integrate `mu^2` from 0 to a and use `W0<=2+|b0|+|T|` there. For the second line the integrable envelope is bounded uniformly for |T|<=1, and that interval has length 2tau. This uses an actual all-frame seven-jet density; no independent cubic/Hessian assumption is introduced.

There is a deterministic tail function `h(A,H,U)->0` as A,H,U tend to infinity such that

```text
E short bars with mu>A or |birth|>H or |T|>U
 <= C_S Vt^(2/3) h(A,H,U) + C_S Vt^2.                (20)
```

For example take the integral in (17) over that union; Gaussian decay absorbs its polynomial. One may include the polynomial tail from (18), or retain (18) as the displayed vanishing error. The constants do not depend on moving coefficient dimension.

For the norm tail, the joint necessary event and `N_x>R`, R>=1, imply

```text
P(N_x>R, lambda^3<=C_S tN_x^2 | J=z)
 <= C W0^4 min(R^-4, C_S^2 t^2 lambda^-6).             (21)
```

Both conditions require N to exceed the **maximum** of two thresholds, so no conditional independence or separate product of probabilities is used. The exact second integral is

```text
integral_0^infinity lambda min(R^-4,D t^2 lambda^-6) dlambda
 = (3/4)D^(1/3)t^(2/3)R^(-8/3).                      (22)
```

Here the split is at `D^(1/6)t^(1/3)R^(2/3)`. Combining (21), (22), the Gaussian envelope and (18) proves

`E short bars with N_M>R <= C_S Vt^(2/3)R^(-8/3)+C_S Vt^2`. (23)

The W0 power here is 4, outside the minimum, rather than 4/3. Its Gaussian integral is still finite. This distinction does not change the R exponent.

Finally apply (15)–(18) with lifetime cap `epsilon t` instead of St. The constants from (11) have the needed scaling: `C_epsilon` is proportional to epsilon, so the soft contribution is proportional to epsilon^(2/3) and the hard contribution to epsilon^2. Thus for `0<epsilon<=1`,

`E N_bar((0,epsilon t]) <= C Vt^(2/3)epsilon^(2/3)+C Vt^2 epsilon^2`. (24)

This controls arbitrarily tiny bars without differentiating a cumulative bound. All estimates apply to the actual finite elder bars by once-counting at maxima and deterministic domination; none requires conditional global Morse genericity.

## 6. Constructing the local saddle from a regular birth jet

Fix constants

```text
0<a<=A<infinity,  0<tau<=U<infinity,
|birth|<=H,  N_M<=R,  a<=mu<=A,  tau<=|T|<=U,         (25)
```

and consider an actual finite bar of lifetime `ell_global<=St`. For small t its soft magnitude satisfies lambda<=1 and, by (11),

`lambda <= (C_S R^2 t)^(1/3) ->0` uniformly.           (26)

The case lambda>1 is impossible once `St<c0^2/(3R^2)`. For small t also lambda<mu, so the eigenframe is unique as a line. Orient its soft direction e so `F_eee(M)=|T|>=tau`; choose hard direction Je. In the rotated radius-b chart, (4) supplies the fixed bounds

```text
B0=p3 R,  C0=p4 R,
rho_* = min(b, a/(32B0), tau/[32(C0+B0^2/a)]) >0.
```

The accepted isolation proof gives the ridge h, `h(0)=h'(0)=0`, `|h'|<=1/8`, strict vertical concavity, and reduced f on `[-rho_*,rho_*]` satisfying

```text
f'(0)=0,  f''(0)=-lambda,
tau/2 <= f'''(x) <= U1:=U+tau/2.                      (27)
```

Use B0,C0 as upper bounds even if the actual derivatives are smaller. The accepted error inequality is uniform at this smaller fixed radius. No second critical point is an input.

Put g=f'. On x>=0, Taylor integration gives

`-lambda x+tau x^2/4 <= g(x) <= -lambda x+U1 x^2/2`.

For small positive x the right side is negative. At `x=4lambda/tau` the left side is zero. For t small this point is inside the chart. The intermediate value theorem gives a second root s>0, with

```text
2lambda/U1 <= s <= 4lambda/tau.                       (28)
```

The endpoint test may be equality, which still supplies a root there. Strict convexity g''>=tau/2 implies at most two roots, so this is the unique second root. Also g'(s)>0, as in the accepted chart argument. Thus `S_loc=(s,h(s))` is a nondegenerate saddle of the actual field. This proves existence, not just a type classification for an assumed pair.

Since g vanishes at both endpoints, comparison with quadratic functions of the same endpoints gives on [0,s]

`(U1/2)x(x-s) <= g(x) <= (tau/4)x(x-s)`.

For example subtract the right quadratic; its second derivative is nonnegative and its endpoint values are zero, so it lies below its chord. Integrating the negatives yields

```text
tau s^3/24 <= ell_local:=f(0)-f(s) <= U1 s^3/12.      (29)
```

In particular ell_local tends to zero uniformly under (25),(26), without having assumed it equals ell_global. For small t, (28) puts s in the half chart, and (29) gives the strict inequalities

`ell_local<a rho_*^2/8`, `ell_local<tau rho_*^3/96`.

Every deterministic premise of the accepted asymmetric trap is now derived. That trap gives its older outgoing point, strict-clearance cut exactly at `d=F(S_loc)`, and attained first elder merger. The actual bar born at M therefore has

```text
ell_global=ell_local,
S_global=S_loc as a quotient point.                  (30)
```

The second equality uses compact Morse/distinct critical values and the exact finite-event source once, not a desired localization certificate. The gate is a component merger, not a loop saddle. Periodic Euclidean lifts remain nonunique.

The physical endpoint distance obeys, by |h'|<=1/8,

```text
s<=r=sqrt(s^2+h(s)^2)<=c_h s,   c_h=sqrt(65)/8,
tau/(24c_h^3) <= k=ell_global/r^3 <= U1/12.            (31)
```

For the actual pair-normal v, its Hessian mark at M is

`A_pair= -lambda sin(alpha)^2-mu cos(alpha)^2`,

where `cos(alpha)=s/r>=1/c_h`. Consequently

`-A <= A_pair <= -64a/65 <0`.                         (32)

These are fixed regular compact marks, derived from the birth jet rather than imposed on an arbitrary endpoint pair. Birth and spatial/directional marks are also in their fixed compact sets. For `epsilon t<=ell_global<=St`, the lifetime mark lies in `[epsilon,S]`. The associated atom thus lies in a fixed compact K of E depending only on (25), epsilon,S. Every bar satisfying the birth conditions has exactly that local candidate as its actual elder pair.

## 7. Exhaustion of all short bars and reverse-localization probability

For each S>0 and any positive epsilon,a,tau with epsilon,a,tau<=1, and finite A,H,U,R, Section 6 produces a compact K in E containing every actual bar with `epsilon<=ell/t<=S` whose birth conditions (25) hold, for all sufficiently small t. Combining (18)–(24) gives

```text
limsup_(t->0) E[ number of bars with 0<ell/t<=S
                                whose marked atom is outside K ]
 <= C_S [ epsilon^(2/3)+a^3+tau+h(A,H,U)+R^(-8/3) ].  (33)
```

Here `Vt^(2/3)` is bounded and `Vt^2->0`; constants have been enlarged accordingly. The right side can be made arbitrarily small by first fixing small epsilon,a,tau and large A,H,U,R, then taking t small. The estimates are additive with constants independent of these cutoffs in their declared ranges. The deterministic threshold for t may depend on them; no exchange requiring a uniform threshold is made.

This proves the actual missing first-moment compact-containment statement. If an increasing sequence of compacts is preferred, take finite unions with a standard compact exhaustion of E after choosing the successive cutoff windows. Monotonic enlargement only reduces the omitted counts.

There is a slightly stronger geometric conclusion without the epsilon cutoff. The birth-tail estimates (19),(20),(23) control **all** bars with `0<ell<=St`. On the regular birth sector Section 6 proves `r<=C(a,tau,U,R,S)t^(1/3)` even when ell/t is arbitrarily small. Thus for every delta>0 there are finite fixed birth cutoffs for which the limsup probability of any short bar not arising from its unique local fold is at most delta. Markov's inequality changes expected omitted count to this probability.

Choose delta_j->0, choose the jth birth cutoffs so that the limiting expected exceptional count is at most delta_j, and then choose thresholds t_j->0 so that the actual expected exceptional count is at most 2delta_j for every t<=t_j. Shrink the jth fixed isolation chart radius further to `min(rho_*,1/j)`; all ridge inequalities survive restriction. Decrease t_j enough that, for every t<=t_j, its second root lies in the half chart, both strict asymmetric gap conditions hold at this smaller radius, and its physical endpoint distance is <=1/j. This is possible by (26)–(29). On `t_(j+1)<t<=t_j`, use that sector and chart. It follows that

```text
P(every finite bar with 0<ell<=St has its unique
  actual elder saddle in a shrinking local fold chart) ->1,
max_(0<ell<=St) dist_T(M,S) ->0 in probability,         (34)
```

with the maximum over an empty set defined as zero. This is an asymptotic probabilistic statement for this one family, with possibly slowly moving cutoffs. It is **not** a deterministic assertion that every realization or every finite t has regular jets, not a uniform fixed compact window with zero omitted probability, and not a quantitative usable numerical radius. No remote small-gap max/saddle pairs are separately counted: a hypothetical actual remote short elder bar must have one of the exceptional birth jets already bounded above.

## 8. Full lifetime/spatial Laplace limit and expected-count asymptotic

The density (1) is integrable over all b,k,A,u when `0<s<=S`. Indeed the limit covariance is positive definite, so

`p_Jinfty,u(b,0,0,12k,0,0,A)<=C exp[-c(b^2+k^2+A^2)]`,

uniformly in u. Therefore `k^(4/3)A^2` is integrable on k>0,A<0, and `s^-1/3` is integrable at zero. This proves finite measure on the whole lifetime band, including the previously excluded singular/unbounded marks. It does not appeal to a compact bound outside its scope.

Define the actual finite-bar process projected to lifetime and birth position,

`Z_t=sum_(finite H0 elder bars) delta_(ell/t, M/L)`

on `[0,infinity) x T_1^2`, assigning no atoms at zero. Let f>=0 be continuous with support in `[0,S]xT_1^2`. It may be nonzero at s=0. The function `f(s,y)` lifted to E need not have compact support, so the compact theorem cannot be applied directly.

Choose a compact K as in (33) and `chi in C_c(E)`, `0<=chi<=1`, with chi=1 on K. Enlarge K/chi as needed so that the finite limiting measure outside its plateau in `0<s<=S` is also arbitrarily small. Such enlargement cannot increase the omitted-bar bound in (33). The accepted regular-sector theorem applies to the compact continuous test

`f_K(s,b,k,A,y,u)=f(s,y)chi(s,b,k,A,y,u)`.

The elementary inequalities `|exp(-a)-exp(-b)|<=min(1,|a-b|)` and `0<=chi<=1` give

```text
|E exp(-Z_t(f))-E exp(-Y_t(f_K))|
 <= ||f||infinity E[number of actual band bars outside K]. (35)
```

The same bound with nu controls the two limiting Poisson exponents. First take t->0 using the accepted compact Laplace theorem, then exhaust K using (33) and the finite-measure tail just proved. The result is

```text
E exp(-Z_t(f))
 -> exp[-v_* c_G integral_(T_1^2) integral_0^infinity
                  (1-exp(-f(s,y))) s^(-1/3) ds dy],   (36)
```

where

```text
c_G=144 integral_(S^1) integral_R integral_(k>0) integral_(A<0)
       k^(4/3) A^2 p_Jinfty,u(b,0,0,12k,0,0,A)
                      dA dk db d sigma(u) >0.          (37)
```

Equation (36) is the full lifetime/spatial Poisson Laplace law, including tests touching zero. The intensity is locally finite on `[0,infinity)xT^2` and has no atom at zero. The same proper closed embedding/Laplace criterion already explicitly imported and reviewed in the accepted higher proof applies to this simpler space: use `[0,infinity)x(S^1)^2` as a closed subset of R5. Thus it also supplies vague convergence in distribution of the projected point processes. This uses the previously named bounded-Laplace convergence import; no expectation convergence for arbitrary unbounded functionals is asserted.

For expected counts, compact first-moment convergence from the same accepted theorem and (33) give, by upper/lower cutoff approximation and the finite continuous limiting density,

```text
E N_bar((0,St]) -> (3/2) v_* c_G S^(2/3),
E N_bar((0,St]) / (Vt^(2/3)) -> (3/2)c_G S^(2/3).      (38)
```

For completeness, choose the containing compact K to be a regular rectangular mark box with full compact torus/angle factors and a lifetime interval whose endpoints have zero nu measure; the density (1) makes all fixed real-coordinate boundary faces null. The compact first-moment theorem and upper/lower continuous approximations then give convergence of expected counts on its intersection with the lifetime band. Its discrepancy from the full count is bounded by (33). Exhaust the boxes and use the finite nu band mass. Equivalently one can use compact cutoff tests and arbitrarily thin boundary strips within a slightly larger regular box. This yields matching upper/lower limits. No differentiation of (38) is used to claim a pointwise changing-source lifetime-density asymptotic.

In particular `N_bar((0,St])` converges in distribution to a Poisson variable of mean `(3/2)v_*c_G S^(2/3)`. This also follows from (36) by approximating the cap boundary, whose limiting intensity is zero. The process law retains joint spatial/lifetime structure, not only a one-dimensional count.

The contact functional is the existing source coefficient with the limit covariance:

```text
c_G = Gamma(7/6)/(24^(1/3)sqrt(pi))
       integral_(S^1) p_G(0) p_Vu(0) tau_u^(4/3)
                                      (s_u^2/2) d sigma(u).
```

For `R(h)=exp(-|h|^2/2)`, `p_G(0)=1/(2pi)`, `p_Vu(0)=1/(2pi sqrt(3))`, `tau_u^2=6` and `s_u^2=8/3`. Hence, algebraically,

`c_G=2 Gamma(7/6)(3/2)^(1/3)/(3sqrt(3) pi^(3/2))`.     (39)

This evaluation uses the already derived source Gaussian half-moment identity; there is no new numerical quadrature or coefficient-digit certificate. The universal gamma/Jacobian factor is separated from the model's local jet invariant. Formula (39) is specific to this normalized unit-length Gaussian covariance, not a universal numerical coefficient for arbitrary fields.

An independent normalization check in the exact reduced cubic gives `ell=2lambda^3/(3T^2)` and therefore `lambda dlambda=(1/3)(3/2)^(2/3)|T|^(4/3)ell^(-1/3)dell`. The birth eigenline domain theta in [0,pi), together with both signs of T, becomes the full oriented outgoing circle with T>0 exactly once. Its prefactor `(1/3)(3/2)^(2/3)=12^(-1/3)` agrees with the candidate change `144 k^(4/3)dk=12^(-1/3)T^(4/3)dT`, T=12k. This checks the angular half and coefficient factors; it is not used as a substitute for the complement proof.

## 9. Attacks, negative evidence and exact remaining limits

* **Conditioning the global coefficient norm:** `E||Z||^4` grows with the Fourier dimension and would destroy uniformity. The proof uses `tr(A_xA_x^*)<=T` and actual conditional Hilbert regression instead. An unconditioned tail without its conditional mean is insufficient.
* **Field-selected eigenframe:** a conditional law given a randomly selected angle is not substituted for a fixed-frame Gaussian law. The Hessian change of variables and subsequent deterministic-theta kernels in §4 are essential. Using theta over a full 2pi without a half would count each Hessian twice; the derived once-only domain has length pi. The candidate intensity still uses the full oriented displacement circle and its already accepted coefficient 144.
* **A second volume or determinant:** counting all possible saddle partners would introduce V^2 and does not close this proof. Source §4 counts once by the birth maximum, and Rice contributes one physical determinant. The local barrier does not enumerate partner candidates.
* **Dropping the norm-tail intersection:** the correct event is N larger than the maximum of its two thresholds. Multiplying unrelated tail probabilities is unjustified. The exact minimum in (21) gives R^(-8/3).
* **Replacing local norm tails by a global logarithmic good event:** powers of log(1/t) need not vanish under fixed singular-mark cutoffs. The fixed local Palm envelope (17) is what permits a cutoff limit after t->0.
* **Assuming the second root:** the root is constructed by an endpoint sign test and IVT; a strictly positive endpoint is unnecessary when the endpoint itself is a root. Convexity gives uniqueness and saddle type. The local gap is shown small before applying the trap; equality with the global gap comes afterward.
* **Zero cubic:** a quartic reduced germ can have two nearby saddles and a gap of quadratic order in its soft curvature, so no uniform regular fold follows if the lower cubic cutoff is simply removed. Here its birth contribution is bounded by (19) and then exhausted. A zero cubic at a specified frame is not asserted to be impossible in every realization.
* **The fixed full fold-square barrier stays false:** the whole-ball barrier (9) uses a lambda-dependent small radius and excludes a higher point inside it. The asymmetric trap uses a different domain with an outgoing point above the maximum. Neither changes the retained negative evidence.
* **Higher factorial moments:** a vanishing first-moment number of omitted atoms controls bounded Laplace observables and first moments. It does not control a rare omitted atom multiplied by an arbitrarily large retained count. Consequently no new all-mark factorial-moment theorem of order p>1 is claimed here. The prior compact regular factorial theorem remains valid in its exact scope.

This proposed result closes the **probabilistic all-short-bar reverse complement and lifetime/spatial process law for the one declared ideal Gaussian truncation family**, conditional only on the exact accepted conventional inputs and named classical area/Laplace imports. It is stronger than another certificate equivalent to localization: the sufficient birth-jet sectors have a derived vanishing complement, and the saddle is actually constructed.

It does not prove an every-realization deterministic local pairing statement, universality across arbitrary covariance spectra/geometries/dimensions, non-Gaussian laws, Hk, an infinite-carrier source theorem, an effective finite numerical window, a blind 50-model experiment, a Lean implementation, independent-provider acceptance, external scientific uptake or the full project objective. No scientific/source/status adoption follows from author completion. A fresh substantive nonauthor review must attack especially §§2,4,5,6,8 before this proposal is consumed as an accepted theorem.

The new exact controls check selected regression inequalities, the symmetric-matrix Jacobian, the two threshold-integral identities, coefficient algebra and nonconstant root/gap examples. Their role is to catch finite algebra and normalization errors; they do not establish the continuous Gaussian/Rice/topological/asymptotic statements by enumeration. No field draws, approximate critical roots, numerical eigenvalues, Rice integration, old-control replay or Lean execution occurs.

The actual new control execution at 21:25:04 UTC exited 0, with 106 exact checks passed, five negative-control families and empty stderr. Its first run at 21:24:09 UTC failed in the checker because Python integer division created a float in the expected incidence determinant ratio. The unchanged failed script/stdout/stderr/receipt and a demonstrated Fraction-versus-float root cause are preserved in `initial-control-failure/`. The correction converts that ratio to Fraction before division; it changes no mathematical source or input. The full proof itself remains conventional author work pending review. The freshly retained primary HTML is identified in `primary-source/SOURCE_IDENTITY.json`, with its bounded read scope stated separately from byte custody.
