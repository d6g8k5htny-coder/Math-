# Gaussian upper tails for essential and long finite lifetimes

28 October 2026. Source-derived mathematical candidate, OpenAI/Codex GPT-6
`/root`; finite algebra support by `/root/axial_technical_check`. No qualifying
different-family scientific review, Lean verification or status promotion.
The [source manifest](SOURCES.json) binds exact bytes and reading rules.

## 1. Result for a specified model

Fix `d>=2`, `L>0`, compact real birth interval `B` and compact gap interval
`J=[k_-,k_+]` with `k_->0`. Let the centered unit-variance Gaussian field on
`T_L^d` have covariance

    K_L(z)=sum_n exp(-|z+Ln|^2/2) / sum_n exp(-|Ln|^2/2).

For any orthonormal frame R, put `u=Re_1`, `M=-ru/2`, `S=ru/2`, and use
the ORIGINAL continuous Gaussian regression law `Q_r` at

    f(M)=b, f(S)=b-kr^3, grad f(M)=grad f(S)=0.

Let

    W_r=|det H_M det H_S| 1{H_M<0,index(H_S)=d-1},
    Z_r=E_Q W_r, P_r=(W_r/Z_r)Q_r,
    K=1+max_{|alpha|<=4} sup_x |partial^alpha f(x)|.

The index counts negative eigenvalues. For all sufficiently small `r>0`
the full normalizer is positive. There are `lambda>0`, `C<infinity`,
`c>0` and `r_*>0`, uniform in `b in B,k in J,R`, such that

    E_Pr exp(lambda K^2)<=C.                            (T1)

Define death by the original path convention: `d_f(M)` is the supremum of
path minima over all continuous paths starting at M and ending at a point
with value strictly larger than b; set it to `-infinity` if there is no
such point. Put `X_r=(b-d_f(M))/(kr^3)` and
`E_r={d_f(M)=-infinity}`. Then

    P_r(E_r)<=C exp(-c/r^2),                            (T2)

and, for every fixed real `q>0`, some `C_q<infinity` satisfies

    r^-3 E_Pr[X_r^q;d_f(M)>-infinity,X_r>1]
          <=C_q exp(-c/r^2).                           (T3)

The same positive c can be used for every fixed q, with different C_q.
All constants are existential or defined by convergent sums/compact extrema;
no numerical onset radius or evaluated probability bound is asserted.

These statements are derived below from the specified covariance and pins.
Neither an all-order norm-moment hypothesis, a failure-mark weak law, a
selection probability estimate, nor an extra uniform-integrability premise
is assumed. The model and compact-parameter restrictions remain essential.

Measurability is concrete. The Fourier construction below takes values in
the separable C4 space; each derivative supremum equals its supremum on a
fixed countable dense set. Also `E_r={max f<=b}`. For death, take countably
many polygonal paths from the fixed M, with all subsequent vertices rational
in lifts of torus charts. Paths with endpoint value `>b` are an open-endpoint
test, and their minima are continuous C0 functionals. Assign `-infinity`
when a tested endpoint is not older. Their countable supremum equals the
displayed death: every continuous path can be uniformly approximated by such
paths, keeping an endpoint strictly older and approximating its minimum.
Thus death and the finite-death moments in (T3) are Borel. No global Morse
or elder-partner identification is needed for this path-functional theorem.

## 2. Source Fourier series and bounded regression energy

Poisson summation gives positive Fourier variances

    a_n=exp(-2pi^2 |n|^2/L^2) / sum_j exp(-2pi^2 |j|^2/L^2)>0.

Take one representative from every pair `{n,-n}`, n nonzero. The real basis
is the constant `sqrt(a_0)`, and, for each representative, the sine and
cosine functions with amplitude `sqrt(2a_n)`. Write it as `(phi_j)` with
independent unconditioned standard Gaussian coefficients `(xi_j)`.
There are positive deterministic majorants `w_j>=||phi_j||_C4` whose sum

    S_4=sqrt(a_0)+2 sum_{n representatives}
                     sqrt(2a_n)(1+2pi|n|/L)^4 <infinity (17)

is finite. The same holds at every derivative order. In particular the
series converges absolutely in C4 almost surely and in each fixed Lp(C4).

Use the exact contact observations from P §3: for axial coordinates
`a=-r/2,c=r/2`, four rows are

    U0=(f(a)+f(c))/2,
    U1=(f(c)-f(a))/r,
    U2=(f_x(c)-f_x(a))/r,
    U3=(6/r^2)[f_x(a)+f_x(c)-2(f(c)-f(a))/r],

with the remaining rows `(f_yj(a)+f_yj(c))/2` and
`(f_yj(c)-f_yj(a))/r`. This is invertible for r>0 and has exact pin target

    v_r=(b-kr^3/2,-kr^2,0,12k,0,...,0).

Integral remainders or the summable Fourier series show that their covariance
`Sigma_r(R)` extends continuously to r=0, where the observations are

    (f,f_x,f_xx,f_xxx,f_y1,f_xy1,...,f_y(d-1),f_xy(d-1))(0).

That contact covariance is positive definite for every frame: a zero-variance
linear combination would annihilate every Fourier mode, so its differential
polynomial would vanish on the full integer lattice. A polynomial vanishing
on that lattice is zero (apply the one-variable polynomial fact successively
to each coordinate). The rotated monomials in this list are linearly
independent, so all coefficients vanish. The same argument applies after
appending the independent symmetric entries of the transverse Hessian.

Continuity and compactness of O(d) give a positive least-eigenvalue bound
for `Sigma_0`, hence for `Sigma_r` on a common small-radius interval.
The targets are bounded on the compact mark window. Therefore

    E0:=sup_{small r,b,k,R} v_r^T Sigma_r^-1 v_r <infinity. (18)

This is derived finite-jet rank, not a sampled numerical covariance check.
No rotational invariance of the periodized covariance is assumed.

For each standardized original coefficient, Gaussian regression gives

    xi_j=m_j+eta_j, |m_j|<=sqrt(E0)=:M0,
    E eta_j=0, Var(eta_j)<=1.                           (19)

The mean bound is covariance Cauchy-Schwarz for projection onto U_r.
The entire vector `(eta_j)` can be correlated. Applying the same regression
to the countable original coefficients constructs the null-pin version of
Q_r; the Fourier series remains absolutely C4-summable because
`sum_j w_j E_Q|xi_j|<=S_4(M0+1)`. It therefore represents the actual
regressed field, with the prescribed observations, rather than an unrelated
independent coefficient model.

## 3. Exponential-square estimate with drift and correlations retained

Set `T=sum_j w_j|eta_j|`, `D0=1+M0 S_4`. Then

    K<=D0+T.

For a finite partial sum, weighted Cauchy followed by Jensen gives

    exp(t T_N^2)
      <= sum_{j<=N} (w_j/S_4) exp(t S_4^2 eta_j^2)
         + (1-sum_{j<=N} w_j/S_4).                    (20)

The missing weight is assigned to zero. Each centered Gaussian marginal
with variance at most one satisfies

    E exp(h eta_j^2)<=(1-2h)^(-1/2), 0<=h<1/2.

Monotone convergence in (20) gives

    E_Q exp(t T^2)<=(1-2t S_4^2)^(-1/2).

Consequently, for `0<eta<1/(4S_4^2)`,

    E_Q exp(eta K^2)
      <= exp(2eta D0^2)(1-4eta S_4^2)^(-1/2).          (21)

In particular choose `eta0=1/(8S_4^2)`, and let B0 denote the finite
right side. This proves a uniform exponential-square norm estimate directly;
it is not inferred from the mere existence of each polynomial moment.
Existing C124 §5 and GaussianWeightedMajorants already use closely related
Fourier/Jensen ideas; the new work here is their full tilted-field and
lifetime application, not a claim to invent Gaussian concentration.

## 4. Actual determinant weight and derived full-normalizer floor

For this coordinate norm, tensor norm comparisons give

    ||D^2 f||_op<=dK,
    ||D^3 f||_op<=d^(3/2)K,
    |D^4 f[u,u,u,u]|<=d^2 K.                           (22)

The gradient pins imply `integral_a^c H(tu)u dt=0`. Comparing either endpoint
to this average and using the third derivative bound gives

    ||H_i u||<=(r/2)d^(3/2)K, i=M,S.

Use an orthonormal frame with first direction u and apply Hadamard to the
Hessian columns. Its other d-1 columns have length at most dK. Thus

    |det H_i|<= (r/2)d^(d+1/2)K^d,
    W_r/r^2<=C_W K^(2d), C_W=d^(2d+1)/4.               (23)

This holds pathwise on the pin fiber, without any type or independence
relaxation beyond discarding the nonnegative type indicator for an upper
bound. Equation (21) supplies all finite moments needed below.

For clarity the normalizer floor is derived, not added as a premise. Let
`A_M` be the entire transverse Hessian at M. Appending its independent
symmetric entries to U_r has a positive contact covariance by §2.
Conditional Gaussian means/covariances therefore converge uniformly to a
full-support nondegenerate Gaussian `A_0` on symmetric `(d-1)` matrices.
Their parameters depend continuously on `(b,k,R)`.

The exact four axial pins and Rolle give a point with `f_xxx=12k` between
the pins. Together with the zero average of `f_xx`, this implies

    f_xx(M)/r=-6k+O(rK), f_xx(S)/r=6k+O(rK).

The gradient averages also bound each normalized mixed entry
`f_xyj(i)/r` by a fixed multiple of K, and `A_S-A_M=O(rK)`.
Use the CORRECT congruence

    D_r=diag(r^(-1/2),I).

Then `D_r H_i D_r` has axial entry `f_xx(i)/r`, mixed entries
`f_xyj(i)/sqrt(r)=O(sqrt(r)K)`, and the original transverse block.
Since (21) bounds K uniformly, the two matrices converge jointly IN LAW to

    diag(-6k,A_0), diag(6k,A_0).

No common random A_0 or convergence-in-probability identification is imposed.
The full Gaussian density gives `P{det A_0=0}=0`. Hence determinant/type
mapping applies almost surely at the limit, while (21),(23) give uniform
integrability of `W_r/r^2`. It follows that

    Z_r/r^2 -> z0(b,k,R)
       =36k^2 E[det(A_0)^2 1{A_0<0}]>0.               (24)

Positivity follows because a full Gaussian density charges an open
negative-definite matrix ball. The limit is continuous in the compact marks
and R. Uniformity follows by a subsequence argument: any allegedly bad
parameter sequence has a convergent subsequence; continuous Gaussian
parameters, the null determinant boundary and uniform integrability give
the same limit along it. Thus, after decreasing r_*,

    Z_r/r^2>=z_*>0                                    (25)

uniformly. This reconstructs P §5 with its congruence erratum and REC's
in-law correction. No matrix-cap selection theorem or failure-mark law is
consumed; §9 Borel Kac-Rice replacement remains separate source context.

Choose `lambda=eta0/2`. For x>=0,

    x^(2d) exp(-(eta0-lambda)x^2)
        <=[d/(e(eta0-lambda))]^d.

Combining (21),(23),(25) and dividing by the full normalizer ONCE gives

    E_Pr exp(lambda K^2)
      <= (C_W/z_*) B0 [d/(e(eta0-lambda))]^d.           (26)

This proves (T1) for the actual typed determinant tilt. No exponential
moment of the weight itself, or independence of weight and norm, is used.

## 5. Escape gives the lifetime bounds without a marked-law premise

Take r_* also below `L/(4sqrt(2))`, respecting the source's embedded-chart
restriction. By (22) the axial fourth-derivative bound is `H<=d^2 K`.
The proved sharp escape theorem implies that an essential death or a finite
lifetime fraction greater than one requires

    K>=A/r, A=24k_-/d^2>0.                            (27)

Indeed outside that event, `rH<24k_-<=24k`; an axial path reaches a strictly
older point with minimum f(S), so `d_f(M)>=f(S)` and `X_r<=1`.
This does not identify the actual elder partner as S.

Markov applied to (T1) gives

    P_r(E_r)<=C exp(-lambda A^2/r^2).                  (28)

For a finite death, the connected torus has a path to an older point and
every such path has minimum at least `min f`. Therefore

    0<=X_r<=2K/(k_- r^3).

For fixed q>0, put `B_q=[q/(e lambda)]^(q/2)`. Polynomial absorption gives

    E_Pr[K^q;K>=A/r]
        <=B_q C exp(-lambda A^2/(2r^2)).               (29)

Multiply by `(2/k_-)^q r^(-3q-3)` for the normalized finite-lifetime tail.
Choose `c=lambda A^2/4`. For `m=3q+3`,

    r^-m exp(-c/r^2)<=[m/(2ec)]^(m/2).

Thus this polynomial can be absorbed into half the exponential rate in
(29), yielding (T3) with this SAME c for all fixed q. Equation (28) gives
(T2) with it as well. The entire exceptional-tail conclusion is independent
of any limit law for pairing failure.

## 6. What is now derived, and what remains open

For this explicit covariance and compact mark family, the norm-moment and
normalizer estimates required by the sharp-escape packet are now proved in
this text, not left as extra stochastic assumptions. The essential and
finite long-lifetime upper bounds improve faster-than-every-power estimates
to a stated Gaussian scale in the inverse separation.

No matching lower bound or sharp exponential rate is asserted. This upper
bound does not make the essential event null at a fixed r. It does not
produce the failure-mark weak law or m_q needed for a lifetime-moment LIMIT,
prove noncompact-mark uniformity, extend to arbitrary covariance/non-Gaussian
models, or identify the path-functional death with a newly formalized global
elder/counting object. Distinct-family scientific review and any controlling
project acceptance remain separate. No parent status or historical bytes
are changed.
