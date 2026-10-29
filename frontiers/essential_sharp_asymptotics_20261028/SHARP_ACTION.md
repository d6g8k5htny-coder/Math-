# A sharp Gaussian action for the essential event

28 October 2026. OpenAI/Codex GPT-6 author-side candidate by `/root`, with
variational and regression analysis from `sharp_rate_route`. Same-family
technical checks do not qualify as different-family scientific review.

## 1. Statement and scope

Use the fixed stationary real Gaussian torus field of PR524, with even
nonnegative spectrum a_n, positive a_n on the frequency cube [-3,3]^d and
sum_n sqrt(a_n)(1+|n|)^4<infinity. Fix d>=2,L>0, birth b, gap mark k>0
and unit direction u. There is no uniform convergence claim over directions,
spectra, dimensions or volumes in this theorem. Let H be the source RKHS,
with its original covariance normalization. At M=0,S=ru use EXACTLY

    f(M)=b, f(S)=b-kr^3, grad f(M)=grad f(S)=0,
    Q_r=canonical conditional Gaussian regression,
    W_r=|det H_M det H_S|1{H_M<0,index(H_S)=d-1},
    Z_r=E_Qr W_r, P_r=(W_r/Z_r)Q_r,
    E_r={max f<=b}.                                  (SA1)

Define the closed convex feasible set in H

    C_(k,u)={g: g(x)<=0 for all x, g(0)=0,
                  D_u^2g(0)=0, D_u^4g(0)<=-24k},
    I(k,u)=(1/2) min_(g in C_(k,u)) ||g||_H^2.        (SA2)

The minimum exists and is unique. It is strictly positive and finite, and

    lim_(r->0) r^2 log Q_r(E_r)
      =lim_(r->0) r^2 log P_r(E_r)=-I(k,u).            (SA3)

In particular the determinant tilt does not change the sharp exponential
coefficient. That coefficient is independent of b and

    I(k,u)=k^2 I(1,u), I(k,-u)=I(k,u),
    (24k)^2/(2 sigma_4(u)^2)<=I(k,u)
                           <=(k^2/2)||q^2||_H^2,     (SA4)

where sigma_4(u)^2 is the variance of D_u^4F(0) under the zero-target
contact conditioning, and q(x)=sum_i2(1-cos(omega x_i))/omega^2,
omega=2pi/L. Thus (SA2) characterizes the optimal coefficient as a Gaussian
energy minimum; it is not an evaluated numerical coefficient or a probability
prefactor. The original periodized Gaussian satisfies these assumptions.

The threshold24, pin right inverse, normalizer estimates and critical-window
ridge geometry are reused from the exact predecessor sources. The new step
is the constrained small-noise limit and matching recovery profiles. Exact
identities and reading roles are retained in SOURCES.json.

## 2. Conditional small-noise limit in C4

Use the desingularized observations U_r and target v_r of PR524 §2:

    v_r=(b-kr^3/2,-kr^2,0,12k,0,...,0).

Their contact rows U_0 are value, axial first/second/third derivatives,
and transverse first and axial-transverse second derivatives at0. Write

    Sigma_r=Cov(U_rF), R_r(x)=Cov(F(x),U_rF)Sigma_r^-1,
    G_r=F-R_r U_rF, mu_r=R_r v_r, f_r=G_r+mu_r.      (SA5)

This common source-field construction has marginal law Q_r. The finite
covariance gap and Fourier summability in the predecessor give uniformly
bounded R_r:R^(2d+2)->C4, convergence R_r->R_0, and bounded mu_r in C4/H.
In fact U_r->U_0 in operator norm C4->R^(2d+2). For its most singular row,

    U_3g=(6/r^3)int_0^r t(r-t)D_u^3g(tu)dt,

so its difference from D_u^3g(0) is bounded by C r||g||_C4. The other rows
have the same or better continuity. Cross-covariances converge in C4 using
derivatives through total order seven, controlled by sum a_n(1+|n|)^8.
Consequently, for deterministic epsilon_r->0,

    ||G_r-G_0||_C4<=epsilon_r ||F||_C4.               (SA6)

The source Fourier C4 majorant supplies E exp(eta||F||_C4^2)<infinity for
some eta>0. Hence for every delta>0,

    limsup r^2 log Pr{||r(G_r-G_0)||_C4>delta}
                                                   =-infinity. (SA7)

The bounded deterministic drift r mu_r tends to zero. Thus Y_r=r f_r is
exponentially equivalent at speed r^-2 to rG_0. The latter has the good
Gaussian small-noise rate

    J(g)=(1/2)||g||_H^2 if g in H cap ker U_0,
         +infinity otherwise.                       (SA8)

Here is a construction of the standard Gaussian large-deviation ingredient
in this particular setting. Expand F=sum_j xi_j phi_j in real independent
standard Gaussian coordinates with sum_j||phi_j||_C4<infinity. Apply the
bounded operator T_0=Id-R_0U_0 to obtain G_0. Finite truncations are
finite-dimensional Gaussian vectors, whose small-noise rate is their
least squared coordinate norm divided by two, directly from their Gaussian
densities. The C4 norm of each omitted tail is bounded by
sum_(j>N)||T_0phi_j||_C4|xi_j|. Weighted Jensen and the Gaussian marginal
integral give exponential-square tails with parameter tending to infinity
as N grows. Thus the truncations are exponentially accurate at speed r^-2.

The operator ell2->C4 taking coordinates to sum_j T_0phi_j coefficients
is compact: its finite truncations converge in operator norm, by the
square-summable C4 norms of the omitted functions. This identifies compact
rate level sets and the limiting least-coordinate-norm rate. Combining
the finite-dimensional upper/lower bounds with the exponentially small
tails gives the C4 open-set lower bound, closed-set upper bound and
exponential tightness. This is the Gaussian Radon small-noise principle,
with no non-Gaussian concentration or full-C4-support hypothesis.

Finally Gaussian projection identifies its Cameron-Martin space with
H cap ker U_0, equipped with the inherited H norm: T_0 is the orthogonal
projection off the finite observation-representer span on H. This proves
(SA8) with the original normalization. Applying (SA7) preserves this LDP
for the moving conditioned fields Y_r.

## 3. The shrinking pins force a nonzero quartic constraint

On essentiality Y_r has pins

    Y_r(0)=rb, Y_r(ru)=rb-kr^4,
    grad Y_r(0)=grad Y_r(ru)=0, max Y_r<=rb.           (SA9)

Consider any sequence r_j->0 of such fields Y_j converging in C4 to g.
The first conditions give g(0)=0, grad g(0)=0 and g<=0. Gradient difference
or U_2 gives D_u^2g(0)=0. Crucially, exact scalar Hermite interpolation
outside the two interpolation nodes, evaluated at2ru, gives

    Y_r(2ru)-rb=4kr^4+(r^4/6)D_u^4Y_r(xi u),
                                           0<=xi<=2r. (SA10)

The left side is nonpositive. Compact C4 convergence therefore forces
D_u^4g(0)<=-24k. Omitting this moving-scale constraint would give the
incorrect zero-cost global cone and contradict the existing rare-event
bound. It is a boundary-layer constraint, not just max g<=0.

These are all the contact constraints needed in the rate. A C4 function
with a maximum at0 has zero gradient and nonpositive Hessian. If its axial
Hessian entry is zero, nonpositivity makes the whole axial Hessian row
zero. Its restriction to the axial line then has zero cubic derivative,
since a nonzero cubic would be positive on one side. Thus every feasible
g in (SA2) already belongs to ker U_0.

For the moving-set upper bound, define D_(k,u) in the AMBIENT C4 space by
the four constraints in (SA2), without an H-membership requirement. It is
C4-closed, and its finite-rate intersection is exactly C_(k,u), since the
contact rows were shown to be automatic. On every compact C4 set, all
limits of essential pinned fields belong to D_(k,u). Equivalently their
distance to this ambient closed set tends uniformly
to zero on the compact set; otherwise a convergent countersequence would
contradict (SA10). Exponential tightness from §2 discards the complement
of a compact set at any prescribed exponential rate. The LDP upper bound
on successively smaller closed neighborhoods, and goodness of J, give

    limsup r^2 log Q_r(E_r)<=-I(k,u).                 (SA11)

This does not assume convergence of unscaled rare fields or interchange
a shrinking geometric event with a weak Gaussian limit.

## 4. Existence, symmetry and scale of the minimizer

The H embedding in C4 is continuous. Hence (SA2)'s pointwise inequalities
and derivative constraints define a norm-closed convex subset of H. It
is nonempty: -kq^2 is a finite Fourier element of H, is nonpositive with
zero value/axial Hessian at0, and D_u^4(-kq^2)(0)=-24k for every unit u.
Hilbert projection gives the unique minimum-norm element g_*.

The zero-target contact covariance appended by D_u^4 has full rank by
the cube-two polynomial-grid argument. Thus sigma_4(u)>0. The norm of the
fourth-derivative functional on H cap ker U_0 is sigma_4(u); Cauchy-Schwarz
gives the positive lower bound in (SA4). The explicit element -kq^2 gives
its finite upper bound.

If D_u^4g_*(0)<-24k, scaling g_* by a factor in (0,1) to make equality
preserves all constraints and strictly reduces its norm. Consequently

    D_u^4g_*(0)=-24k.                               (SA12)

Total spatial inversion Vg(x)=g(-x) is an RKHS isometry, since the source
spectrum is even. It preserves (SA2). Uniqueness therefore gives Vg_*=g_*.
Every odd derivative of g_* at0 vanishes, in particular the transverse
cubic vector B=D_u^2 grad_y g_*(0). Scaling the whole feasible set by k
gives I(k,u)=k^2I(1,u), and even axial derivatives give I(k,-u)=I(k,u).
No birth mark occurs in (SA2), establishing b independence once the lower
bound is matched.

## 5. Strict recovery fields and the exact original weight

Let s_i(x)=sin(omega x_i)/omega and P_u=Id-uu^T. For 0<epsilon<2 put

    g_epsilon=g_*-epsilon k q^2-epsilon|P_u s|^2.     (SA13)

It is in H, tends to g_* in H and has a UNIQUE global maximum0 at0,
because q(x)>0 away from0. It remains even and in ker U_0. In the fixed
(u,y) frame its contact transverse Hessian, cubic vector and axial fourth
derivative satisfy

    A_epsilon<0, B_epsilon=0,
    c_epsilon=-24k(1+epsilon),
    gamma_epsilon=c_epsilon/12 in (-6k,-2k).          (SA14)

The hard sine penalty has zero axial fourth derivative: P_u s(tu)=O(t^3),
so its squared norm is O(t^6). The q^2 term has zero Hessian and fourth
axial derivative24. This justifies every entry of (SA14), including the
strict typed window; mere nonpositivity would not ensure the saddle type.

Use PR524's fixed finite-mode pin right inverse D_r, bounded in both C4
and H, and set

    v_r^Y=(rb-kr^4/2,-kr^3,0,12kr,0,...,0),
    Yhat_r=g_epsilon+D_r(v_r^Y-U_rg_epsilon),
    h_r=Yhat_r/r.                                   (SA15)

Since U_0g_epsilon=0 and ||U_r-U_0||_(C4->Euclidean)=O(r), the correction
in (SA15) is O(r) in H/C4. Therefore h_r has the exact ORIGINAL pins and

    Yhat_r->g_epsilon in C4 and H,
    r^2||h_r||_H^2->||g_epsilon||_H^2.               (SA16)

Fix any B<infinity. Uniformly for zero-pin perturbations v with
||v||_C4<=B, the scaled fields r(h_r+v) converge in C4 to g_epsilon and
have the exact critical-gap pins (SA9). Apply the DETERMINISTIC argument
of PR524 CRITICAL_WINDOW §§4--5, with gap ratio tau=k and birth rb.
Its hard ridge exists in a fixed chart because A_epsilon<0. Its reduced
fourth derivative tends to12gamma_epsilon<-24k. Exact Hermite interpolation
then proves no value above rb in that whole chart, including intermediate
scales r<<|x|<<1. The unique maximum of g_epsilon gives a strict gap on
the compact exterior. Thus EVERY such h_r+v is essential for small r.
No Gaussian genericity or non-tied critical values of g_* are assumed.

Endpoint Taylor/Schur limits are also uniform over this ball. For the
SCALED field, hard blocks tend to A_epsilon, mixed blocks divided by r
tend to0, and axial entries divided by r^2 tend to
gamma_epsilon-6k at M and gamma_epsilon+6k at S. These have strictly
negative/positive signs by (SA14). Dividing the Hessians by r to return
to h_r+v gives the literal original types and

    W_r(h_r+v)>=c_epsilon r^(4-2d).                 (SA17)

## 6. Gaussian translation and matching rates

The centered conditional law nu_r has a symmetric zero-pin C4 ball A_B
of probability at least one half for one fixed B, by the predecessor's
variance-contraction/Fourier-majorant estimate. The conditional mean mu_r
is the orthogonal H projection of every exact pinned h_r onto the pin
representer span. Hence h_r-mu_r is in the conditional Cameron-Martin
kernel and ||h_r-mu_r||_H<=||h_r||_H. Translation plus reflection gives

    Q_r(h_r+A_B)>=(1/2)exp(-||h_r-mu_r||_H^2/2).

Using essentiality, (SA16), and then epsilon->0 proves the lower bound
matching (SA11) for Q_r. Using in addition (SA17) and the SAME full
normalizer Z_r<=C r^2 gives

    P_r(E_r)>=c_epsilon r^(2-2d)
                              exp(-||h_r-mu_r||_H^2/2).

All prefactors are polynomial and disappear after multiplication of their
logarithms by r^2. Therefore the same lower rate holds under P_r.

For its upper rate, the predecessor proves Z_r>=c r^2 and, for every fixed
p>1, sup_r E_Qr[(W_r/r^2)^p]<infinity. Holder gives

    P_r(E_r)<=C_p Q_r(E_r)^(1-1/p).

Use (SA11), then let p tend to infinity AFTER the r upper limit. This
gives the upper rate -I(k,u), completing (SA3).

## 7. What is resolved and what is not

The essential event now has an exact optimal exponential coefficient,
characterized by (SA2), at each fixed positive gap mark and direction in
the declared class. It also has the explicit k^2 law and birth-independent
coefficient. This strengthens the predecessor's two-sided logarithmic-order
bounds; its threshold24 and local geometry remain credited to that source.

Evaluating the constrained RKHS minimum, deriving a probability prefactor,
or proving convergence uniformly over moving directions/parameters requires
further work. No such claim is inferred from (SA3). Nor does this theorem
exchange the critical-window r,tau limits or establish global counting
intensities. Scientific acceptance, different-family review and formal
alignment remain separate from this conventional author-side proof.
