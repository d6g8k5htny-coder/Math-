# Matching Gaussian scale for the essential event on coordinate axes

28 October 2026. Author-side mathematical candidate, OpenAI/Codex GPT-6
`/root`, with template/control support by `essential_template` and Gaussian
translation support by `essential_gaussian_cost`. Source-overlap corrections
by `next_marked_hypothesis`. Exact inputs are in [SOURCES.json](SOURCES.json).
No qualifying different-family scientific review or status promotion.

## 1. Statement and exact scope

Keep the explicit periodized Gaussian covariance, original Gaussian pin law
Q_r, typed weight W_r, full normalizer Z_r and P_r=Q_r^W of PR522's
Gaussian-lifetime proof. Fix `d>=2,L>0`, compact birth interval I and compact
gap interval J in `(0,infinity)`. Restrict the axial unit vector to a signed
coordinate vector of the cubic torus. Transverse coordinates are arbitrary
orthonormal completions; they do not change the physical zero-gradient pins,
determinants or inertia.

There are constants `C_L,c_U,C_U,r_*>0`, uniform over these marks and axes,
such that the actual essential event E_r satisfies

    exp(-C_L/r^2) <= P_r(E_r) <= C_U exp(-c_U/r^2),
                                    0<r<=r_*.          (1)

Thus `-log P_r(E_r)=Theta(r^-2)` at this scope. The upper bound is the proved
source result (T2) of PR522; the lower bound is proved here. This is a matching
scale, not an optimal constant in the exponent or a large-deviation limit.

E_r means that no point has value strictly greater than the pinned birth
`f(M)=b`; equivalently the source's path-defined elder death is `-infinity`.
This is a Borel event, since `E_r={max f<=b}` under the exact pin law. The
constructed subevent below has M as its UNIQUE global maximum and has the
strict endpoint Hessian types. No global Morse or marked-law premise is used.

For a more explicit one-sided rate bound, put `omega=2pi/L` and let a_n be
the actual positive Fourier variances. For each fixed b,k,

    liminf_(r->0) r^2 log P_r(E_r) >= -I_tpl(k),
    I_tpl(k) = k^2/(2omega^8)
                 [144/a_0+128/a_e1+8/a_(2e1)].         (2)

This is an available template cost, not a claimed minimizer. The same
expression applies to every coordinate axis by exact signed-permutation
symmetry, not by an arbitrary rotation of the torus.

## 2. An exact finite-frequency global-maximum template

By stationarity translate M to 0 and S to `r e_1`, applying a signed coordinate
permutation if necessary. For the TEMPLATE choose the standard lattice
transverse coordinates, so `(x,y)` is a fundamental lift in
`[-L/2,L/2]^d`, `m=d-1`. Arbitrary observational transverse completions do
not change the resulting pin law or Hessian types, but are not used to rotate
the cosine modes in (4). Write

    tau=omega r, c=cos(tau), s=sin(tau), v=1-c,
    beta=s(8+tau^4/v^2)/c,
    gamma=8v/c+tau^4(1+2c)/(v c),
    q_tau(theta)=8(1-cos(theta))-beta sin(theta)+gamma,
    F_tau(theta)=(1-cos(theta))q_tau(theta).             (3)

Take r small enough that `c>0`. With a fixed transverse strength T to be
chosen, define the literal periodic trigonometric polynomial

    h_r(x,y)=b-[k/(omega^4 r)]F_tau(omega x)
               -T sum_(j=1)^m(1-cos(omega y_j)).      (4)

Direct algebra using `s^2=v(1+c)` gives

    F_tau(0)=F_tau'(0)=0,
    q_tau(tau)=tau^4/v,
    F_tau(tau)=tau^4, F_tau'(tau)=0.                   (5)

Hence h_r has EXACTLY the original values and zero gradients at both pins.
Its axial second derivatives satisfy

    h_xx(0)=-k gamma/(omega^2 r),
    h_xx(r)=-k F_tau''(tau)/(omega^2 r),
    F_tau''(tau)=8v/c+tau^4(1-2c-2c^2)/(v c).          (6)

Taylor expansions with their removable singularities treated at tau=0 give

    beta=12tau+O(tau^3), gamma=10tau^2+O(tau^4),
    F_tau''(tau)=-2tau^2+O(tau^4).                     (7)

In particular `h_xx(0)/(kr)->-10` and `h_xx(r)/(kr)->2`.

The maximum is GLOBAL. Let

    R_tau=sqrt(64+beta^2), phi_tau=atan(beta/8),
    epsilon_tau=8+gamma-R_tau.

Then

    q_tau(theta)=epsilon_tau+R_tau[1-cos(theta-phi_tau)],
    epsilon_tau=tau^2+O(tau^4),
    phi_tau=(3/2)tau+O(tau^3).                         (8)

Thus epsilon_tau is strictly positive for small nonzero tau. On
`theta in [-pi,pi]`, the difference `theta-phi_tau` stays in a fixed compact
subinterval of `(-2pi,2pi)`. The continuous extension of
`(1-cos z)/z^2` at zero has a positive lower bound there. Since
`|phi_tau-tau|<=C tau`, (8) implies

    q_tau(theta)>=c_1[(theta-tau)^2+tau^2].

Also `1-cos(theta)>=2theta^2/pi^2` on `[-pi,pi]`. It follows that, for a
fixed positive a depending on L and the compact gap floor,

    b-h_r(x,y) >= (a/r)x^2[(x-r)^2+r^2]
                       +(8T/L^2)|y|^2.               (9)

Here all lifted coordinates lie in the full fundamental cube. This is not
just a local chart estimate. In particular M is the unique global maximum.
All constants and the radius interval can be common over the stated compact
parameter family.

## 3. A fixed C4 zero-pin ball preserves the event and the typed weight

Use the coordinate C4 norm from PR522. Fix a finite B0, and let g be any
real periodic C4 function satisfying ALL zero value/gradient pins at M,S
and `||g||_C4<=B0`. Four-node Hermite interpolation and the two-node
interpolation formula, including extrapolation in the lifted interval, give

    |g(x,0)|<= (B0/24)x^2(x-r)^2,
    |partial_yj g(x,0)|<= (B0/2)|x(x-r)|.              (10)

The latter uses the zero values of each transverse derivative at both pins
and its second axial derivative, of total order three. Taylor in y gives,
with `X=x(x-r)`,

    g(x,y)<= (B0/24)X^2
                +(sqrt(m)B0/2)|X||y|+(mB0/2)|y|^2.    (11)

Choose T, independent of r, so that

    D_y=8T/L^2-mB0/2>0,
    H_y=T omega^2-mB0>0.

Young's inequality bounds the mixed term in (11) by

    (mB0^2/(8D_y))X^2+(D_y/2)|y|^2.

Put `J0=B0/24+mB0^2/(8D_y)`. For r sufficiently small, `a/r>=2J0`;
combining (9)-(11) gives

    b-(h_r+g)(x,y)
       >= [a/(2r)]X^2+a r x^2+(D_y/2)|y|^2.           (12)

This is strictly positive except at M. Thus EVERY function in this fixed
zero-pin ball around h_r has M as its unique global maximum. There is no
shrinking C2/C4 small-ball assumption hidden in this construction.

The Hessian types and weight are uniform too. The pin identities imply

    |g_xx(M)|,|g_xx(S)|<=B0 r^2/12,
    |g_xyj(M)|,|g_xyj(S)|<=B0 r/2.                    (13)

The first estimate follows by taking the endpoint quadratic limit in (10).
For the second, the zero endpoint transverse gradients make the average of
g_xyj zero, and its axial derivative is bounded by B0.
The transverse Hessian blocks of h_r+g are bounded above by `-H_y I`.
Their inverses have norm at most `1/H_y`.

The Schur complement of either transverse block differs from the axial
entry by a nonnegative quantity of order r^2. Equations (6)-(7),(13) therefore
give a negative Schur complement of order r at M and a positive one of
order r at S. Inertia is exactly d negative eigenvalues at M and d-1 at S.
Their determinant magnitudes are bounded below by fixed positive constants
times r, since the transverse determinant has magnitude at least H_y^m.
Consequently, on the entire fixed ball,

    W_r(h_r+g)>=w_* r^2, w_*>0.                      (14)

The original typed indicator equals one on this ball; it is not discarded
or replaced by an unrelated weight for the lower bound.

## 4. Finite Fourier support and its true Gaussian translation cost

The exact expansion is

    F_tau(theta)=(12+gamma)-(16+gamma)cos(theta)
                   +4cos(2theta)-beta sin(theta)
                   +(beta/2)sin(2theta).              (15)

Thus h_r uses only the constant, axial frequencies e_1 and 2e_1, and the
first transverse coordinate frequencies. These are ACTUAL lattice modes of
the periodic field. No off-lattice rotated profile is used.

For the original covariance, a real trigonometric polynomial with constant
coefficient c0 and cosine/sine coefficients C_n,S_n has RKHS norm

    ||h||_H^2=c0^2/a_0
                  +sum_representatives (C_n^2+S_n^2)/(2a_n). (16)

All the finitely many relevant a_n are strictly positive. Equations (7),(15)
show that `||h_r||_H^2<=C_H/r^2` uniformly on the compact marks. More exactly,

    r^2||h_r||_H^2 -> k^2/omega^8
                         [144/a_0+128/a_e1+8/a_(2e1)]. (17)

The bounded birth and fixed transverse term contribute no leading r^-2
cost. Translating back to the original symmetric pin locations rotates the
sine/cosine coefficient pairs and preserves (16).

Let L_r be the original finite value/gradient pin map, mu_r its regression
mean, and nu_r the centered conditional field law. Finite-dimensional
Gaussian conditioning identifies its Cameron-Martin space as

    H_r=H intersect ker L_r,

with the inherited H norm. This also follows directly by taking the
H-orthogonal projection off the span of the pin representers. Since h_r
has the exact target pins, that projection gives

    a_r:=h_r-mu_r in H_r,
    ||a_r||_(H_r)^2=||h_r||_H^2-||mu_r||_H^2
                                        <=||h_r||_H^2. (18)

This uses the actual pin regression, not absolute continuity of Q_r with
the unconditioned field law. Those laws are singular.

Let S_4 be the convergent Fourier C4 majorant from PR522. Each centered
conditional standardized Fourier coefficient has variance at most one,
with its correlations retained. Hence for G_r of law nu_r,

    E||G_r||_C4<=S_4.

Choose the previously fixed radius `B0=max(1,2S_4)`. The symmetric Borel
event `A={||G_r||_C4<=B0}` has nu_r-probability at least 1/2, and its samples
have zero pins. Cameron-Martin translation and symmetry give

    nu_r(a_r+A)
      =exp(-||a_r||^2/2) integral_A exp(-ell_(a_r)(g)) dnu_r(g)
      >=exp(-||a_r||^2/2) nu_r(A)
      >=(1/2)exp(-||h_r||_H^2/2).                     (19)

Here ell is the centered Gaussian translation functional. The inequality
is exact: reflect g to -g on the symmetric event and average the two
integrands to obtain cosh(ell)>=1. Thus no uncontrolled linear translation
penalty or shrinking-small-ball cost is assumed.

Adding the mean identifies the translated event as `h_r+A` under Q_r.
Sections 2-3 show it lies in E_r with W_r bounded below as in (14).

## 5. Return to the actual full determinant tilt

The source-derived conditional norm estimate and the zero-gradient
determinant bound of PR522 imply

    0<Z_r<=C_Z r^2.                                  (20)

Positivity also follows directly from the positive-probability event (19)
and (14). Dividing by the SAME full normalizer exactly once gives

    P_r(E_r)
      >=(w_* r^2/Z_r) Q_r(h_r+A)
      >=[w_*/(2C_Z)]exp(-||h_r||_H^2/2).              (21)

Equations (17),(21) prove (2) and the lower bound of (1), absorbing the fixed
positive prefactor by increasing C_L and reducing r_* if necessary.
The source (T2) supplies the upper bound at these axes. Fixed-probability
zero-pin perturbations are the reason the lower cost has the same inverse
separation scale as the upper estimate.

## 6. Resolved question and retained boundaries

This supplies a model-realized quantitative lower bound where the previous
essential-support proof gave only positivity for each fixed r. Together
with the source upper bound it identifies the logarithmic ORDER r^-2 on
coordinate axes. The explicit quantity I_tpl is only a one-sided available
cost, not the sharp rate coefficient.

Arbitrary axial directions on the torus remain outside this construction;
rotating a finite periodic Fourier profile would generally leave the lattice.
No noncompact-mark uniformity, probability prefactor asymptotic, new
marked-law/moment-limit proof, global elder-counting join, or parent status
promotion is asserted. Existing conventional marked-law and inverse-moment
proofs are not called unproved merely because a review or integration is
pending. This new packet itself still requires different-family scientific
review under the project policy.
