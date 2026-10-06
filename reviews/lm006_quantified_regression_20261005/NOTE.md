# LM006: an explicit linear coupling rate from the pin-frame derivatives

Dylan Roy — delegated AI mathematical work. Actual author OpenAI / GPT-6
Astra Pro, `round17-quantified-regression-audit-20261005`. Scientific effect NONE.
This is a new analytic companion with finite exact checks, not a Lean theorem,
scientific-status change, or independent reclassification of an older proof.

## 1. What is new, and which hypotheses are stronger

Math-#301's endpoint note at `e31b6ad8356e0760c8a7fb6e816ff640c45176c9`,
`reviews/lm006_endpoint_extension_20261005/NOTE.md`, blob
`551aa563562bc88a19e33d146259c03aa2d318f6`, proves qualitative convergence
using mean-square F C3, H_y C2 and Q continuous. Here
F(x)=f(x,0), H_y(x)=f_y(x,0), Q(x)=f_yy(x,0). Its explicit frame and adjusted
endpoint formulas, not an unspecified historical frame, are our inputs.

We assume instead F C4, H_y C3 and Q C1 as maps into the common Gaussian
Hilbert space H=L2 of the UNCONDITIONED field. This extra regularity yields
quantified row errors. A finite eighth spectral moment is sufficient; the
older sixth-moment assumption alone is not silently upgraded. Section 6
gives a well-posed Gaussian counterexample to such an upgrade.

Our contribution is an explicit regression-residual coupling and its constant
K, with e_r <= K r despite a singular limiting endpoint covariance. We do not
assume a Lipschitz estimate for the principal covariance square-root map.
Pathwise Gaussian conditioning is established prior methodology; see Wilson,
Borovitskiy, Terenin, Mostowsky and Deisenroth, JMLR 22(105):1–47 (2021),
*Pathwise Conditioning of Gaussian Processes*, arXiv:2011.04026. Only its
abstract/publication record was consulted; no theorem is imported from it.
The Gaussian argument below is complete. Repository remote-window work also
already uses regression couplings; no general coupling novelty is claimed.

## 2. A quantitative finite-target conditioning lemma

Let P_r in H^p and V_r in H^q be centered jointly Gaussian random vectors on
ONE probability space, for 0<=r<=Rbar, where 0<Rbar<=1. Their joint family
may be Gaussian in an infinite-dimensional H. Write ||U||_H^2=E||U||^2,
and assume

 ||P_r-P_0||_H <= Lp r,    ||V_r-V_0||_H <= Lv r,           (1)
 ||P_0||_H <= p0,         ||V_0||_H <= v0,
 G_0=Cov(P_0) >= lambda I_p,  lambda>0.

All constants are fixed, not r-dependent. Let prescribed pin values d_r
satisfy ||d_0||<=d0 and ||d_r-d_0||<=Ld r. Define

 U=p0+Lp Rbar,  V=v0+Lv Rbar,
 Lg=2 U Lp,    Lk=U Lv+V Lp,
 B=2 V U/lambda,
 Lb=2 Lk/lambda + 2 V U Lg/lambda^2,
 Cm=Lb d0+B Ld,       Cz=Lv+Lb p0+B Lp,
 K=sqrt(Cm^2+Cz^2).                                      (2)

Set R=min(Rbar,lambda/(2 Lg)) when Lg>0, and R=Rbar if Lg=0.
For every r in [0,R], G_r is positive definite and the canonical conditional
law of V_r given P_r=d_r admits a joint Gaussian coupling X_r,X_0 with

 e_r^2=E||X_r-X_0||^2 <= K^2 r^2.                         (3)

This is a statement for every prescribed d_r, not conditioning on a
positive-probability event. No lower eigenvalue bound on the TARGET's
conditional covariance is needed. A singular target law is permitted.

### Proof with constants

For Hilbert-valued vector rows, Cauchy–Schwarz entrywise gives
||Cov(A,B)||_F <= ||A||_H ||B||_H. Thus, writing
G_r=Cov(P_r), J_r=Cov(V_r,P_r),

 ||G_r-G_0||_op <= Lg r,
 ||J_r-J_0||_F <= Lk r,      ||J_r||_F <= V U.             (4)

The first bound uses (||P_r||_H+||P_0||_H)||P_r-P_0||_H.
The second uses Cov(V_r-V_0,P_r)+Cov(V_0,P_r-P_0). The radius ensures
G_r >= lambda I/2 and ||G_r^-1||_op<=2/lambda. The resolvent identity gives

 ||G_r^-1-G_0^-1||_op <= 2 Lg r/lambda^2.

Let B_r=J_r G_r^-1. Then ||B_r||_F<=B and
||B_r-B_0||_F<=Lb r. These estimates use the PIN Gram inverse only.
Now set

 Z_r=V_r-B_r P_r,       m_r=B_r d_r,
 X_r=m_r+Z_r.                                              (5)

The residual Z_r is Gaussian and Cov(Z_r,P_r)=0. The joint Gaussian
characteristic function therefore factors, even when Cov(Z_r) is singular;
Z_r is independent of P_r. Consequently X_r has precisely the canonical
conditional law of V_r given P_r=d_r.

All Z_r are on the original unconditioned probability space. Algebra gives

 ||m_r-m_0|| <= ||B_r-B_0||_F ||d_0||+||B_r||_F||d_r-d_0||
              <= Cm r,
 ||Z_r-Z_0||_H
   <= ||V_r-V_0||_H+||(B_r-B_0)P_0||_H+||B_r(P_r-P_0)||_H
   <= Cz r.

The residual difference is centered, so its cross term with the deterministic
mean difference is zero. Squaring gives (3). This does not assert that the
coupling is optimal or a common conditional realization of every full-field
event. For each fixed pair r,0, the joint residual vector in R^(2q) has a
positive-semidefinite covariance and a standard finite Gaussian
representation. Its two factor blocks A_r,A_0 have a common width at most
2q, and

 ||m_r-m_0||^2+||A_r-A_0||_F^2=e_r^2.                     (6)

Thus the factor-error premise used in #315/#318 is satisfied by THESE
coupling factors. It is not a rate for separately selected principal roots.
The unweighted endpoint laws also satisfy W2<=e_r by the definition as an
infimum over couplings; no W2 claim for their tilted laws is inferred.

## 3. Row rates for exactly the LM006 pin-adjusted coordinates

Use I=[-1/2,1/2], and the exact #301 frame

 P0=(F(-r/2)+F(r/2))/2,
 P1=(F'(-r/2)+F'(r/2))/2,
 P2=(H_y(-r/2)+H_y(r/2))/2,
 P3=int_I F''(ru)du,   P4=int_I H_y'(ru)du,
 P5=6 int_I (1/4-u^2)F'''(ru)du.                           (7)

The last three integral identities are the divided differences in #301;
its inverse frame loses no raw pin. At zero, P equals
(f,f_x,f_y,f_xx,f_xy,f_xxx)(0). For b=6/5, heights b and b-r^3/6 and zero
endpoint gradients give exactly

 d_r=(b-r^3/12,0,0,0,0,2),  ||d_r-d_0||=r^3/12.

We can take Ld=Rbar^2/12 and d0=sqrt(b^2+4). This is the exact target,
not an unproved inference from the endpoint types.

Let F_j, H_j and Q_1 be uniform Hilbert-norm upper bounds on the indicated
mean-square derivatives over [-Rbar/2,Rbar/2]. The fundamental theorem gives
||U(ru)-U(0)||_H<=|ru| sup||U'||_H. Applying it to (7) yields component
rate bounds

 (F1/2, F2/2, H1/2, F3/4, H2/4, 3 F4/16).

Here int_I |u| du=1/4 and 6 int_I |u|(1/4-u^2)du=3/16. Therefore

 Lp^2=F1^2/4+F2^2/4+H1^2/4+F3^2/16+H2^2/16+9F4^2/256.    (8)

For the adjusted target vector V_r=(A_-,A_+,B_-,B_+,C_-,C_+), use exactly

 A_-=-int_I(1/2-u)F'''(ru)du,  A_+=int_I(1/2+u)F'''(ru)du,
 B_-=-int_I(1/2-u)H_y''(ru)du, B_+=int_I(1/2+u)H_y''(ru)du,
 C_-=Q(-r/2), C_+=Q(r/2).                                 (9)

Since int_I |u|(1/2±u)du=1/8, the six component bounds are
(F4/8,F4/8,H3/8,H3/8,Q1/2,Q1/2), so

 Lv^2=F4^2/32+H3^2/32+Q1^2/2.                             (10)

The subtraction of P3/P4 is performed BEFORE conditioning. On the actual
pin subspace these rows become the physical Hessian entries divided by r.
Using raw unconditioned F''/r instead would not satisfy (1).

Equations (8)–(10), positive pin Gram, and the exact target now discharge
(1) and give (3) on the explicit sufficient radius. The limiting conditioned
vector is the #301 section (-1,1,-a/2,a/2,Q_L,Q_L). In particular its first
two entries are deterministic and its last two coincide; nothing in the
proof requires their six-dimensional covariance to be invertible.

## 4. A sufficient spectral class; no numerical field certificate

Suppose an actual centered stationary real Gaussian field has covariance

 C(z)=sum_{k in Z^2} p_k exp(i nu k.z),  nu=2pi/L,
 p_k=p_-k>=0,   S8=sum_k p_k(1+|nu k|^8)<infinity.          (11)

As in #301's lower-order argument, weighted-L2 difference quotients with
|exp(it)-1|<=|t| give mean-square derivatives through order4. Dominated
convergence makes the highest derivatives continuous. Lower orders are
bounded by the same S8 because t^(2j)<=1+t^8 for 0<=j<=4. Stationarity
makes each derivative's Hilbert norm independent of position. Thus each
F_j,H_j,Q_1 needed above is at most sqrt(S8), giving

 Lp <= sqrt(233 S8)/16,    Lv <= 3 sqrt(S8)/4,
 p0 <= sqrt(6 S8),        v0 <= sqrt(3 S8).                (12)

A positive limiting pin Gram is still needed. If every lattice weight p_k
is STRICTLY positive, it follows directly: the seven symbols of
(f,f_x,f_y,f_xx,f_xy,f_xxx,f_yy) are distinct monomials in k, up to nonzero
complex factors. A nonzero linear combination is a nonzero polynomial, which
cannot vanish on all Z^2 (fix one integer coordinate, then use the infinitely
many roots in the other, and repeat). Its spectral variance sum p_k|s(k)|^2
is positive. Thus the seven-function Gram is positive definite, implying
both the pin condition and Var(Q_L | pins)>0. The canonical conditional Q_L
is then a nondegenerate real Gaussian; its negative half-line has positive
probability, so z0=E(Q_L)_-^2>0.

This proves a conditional spectral-class corollary, not an assertion that an
unread named field or finite approximation has (11) with all weights positive.
The all-positive hypothesis can be weakened to independence on the actual
support; merely having a finite S8 is not nondegeneracy. Choose Rbar<L as
well as <=1 in a torus application. Neither this note nor its finite polynomial
model is a numerical evaluation of the actual infinite side24 spectrum,
lambda, K or an optimal radius. Birth height and other marks are fixed.

## 5. Consequences for the reviewed normalizer and sign interfaces

Let X_r,X_0 be the coupling above, with the LM006 contact section at zero,
and assume z0=E(Q_L)_-^2>0, either as an explicit premise or via §4's
strictly-positive spectral hypothesis. From (5), uniformly in [0,R],

 ||m_r|| <= B(d0+Ld Rbar)=:M,
 ||Cov(X_r)||_op <= E||V_r||^2 <= V^2=:Lambda.

The covariance bound is the usual subtraction of a positive-semidefinite
regression term. It does not bound the mean, which was handled separately.
Use #315's pointwise estimate and integrate its ABSOLUTE value, as #318 did.
With the exact physical endpoint function T_r and z_r=E T_r=Z_r^phys/r^2,

 Delta_r=E|T_r(X_r)-T_0(X_0)| <= Cw r,
 Cw=Bs K+Ds,
 Bs=sqrt(2048(M^6+480 Lambda^3)), Ds=8(M^4+48 Lambda^2).     (13)

For r<=Rz=min(R,z0/(2Cw)) when Cw>0 (omit the second term when Cw=0),
z_r>=z0/2. This is a symbolic sufficient radius, not a computed enclosure.
#318 gives d_BL(nu_r,nu_0)=O(r) with its displayed constant and metric
convention. It still does not give total-variation convergence of the two
endpoint pushforwards; their singular-support obstruction is unaffected.

The separately reviewed #325 NOTE, at1dfe801eb61a8335a2e42b886fca9b000fb3598c,
`reviews/lm006_typed_sign_suppression_20261005/NOTE.md`, blob
`9015971fa03f44ae99d410facc6f3d8c26cdc945`, (8), gives for E={c_+>=0}

 E[T_r(X_r)1_E] <= sqrt(2 C6) K r^2 + sqrt(105 C2) K^4 r^4/8,
 C2=M^2+6Lambda,  C6=32(M^6+480Lambda^3).

Therefore, for 0<r<=Rz,

 nu_r(E) <= min(1, (2/z0)[sqrt(2 C6)K r^2
                                +sqrt(105 C2)K^4 r^4/8]). (14)

This now supplies the O(r^2) conclusion on our explicitly STRONGER derivative
and Gram hypotheses, instead of assuming an unspecified e=O(r). It does not
supply a bare-event margin, full-field capture, elder pairing, a persistence
law, uniformity in changing marks, or a higher-dimensional matrix theorem.
It does not overwrite #325's still-correct statement that its own hypotheses
alone do not establish the field rate. The Gaussian error variables can be
dependent and degenerate. Their eighth-moment premise is not erased.

## 6. The extra derivative is real, not cosmetic

For F(x)=|x|^(7/2), F is C3 but not C4 at zero. At h=1/n^2, r=2h, its adjusted
endpoint values are both (21/8)sqrt(h), while the limiting third derivative
is zero. The ratio to r is21n/16, unbounded. This already disproves a
uniform linear ROW rate from the old hypotheses alone.

It also yields a nonsingular-pin Gaussian example, not just a deterministic
row warning. Take independent standard Gaussian coefficients and the model
in the checker, replacing Z8*x^4/24 by Z8*|x|^(7/2). The limiting six-pin
Gram is I6. In the even F block, eliminating the quadratic pin gives two
observations of Z8 with coefficients -(3/4)h^(7/2) and (7/2)h^(3/2) against
independent unit Gaussian noises Z0 and Z3. Thus

 Var(Z8 | pins)=1/[1+(49/4)h^3+(9/16)h^7],
 Var(A_- | pins)=(441/64)h/[1+(49/4)h^3+(9/16)h^7].        (15)

The limiting A_- is the deterministic value -1. Any coupling to that limit
has mean-square error at least (15), of order r. Hence no coupling with
RMS error O(r) is possible in this example; its RMS error is bounded below by a positive multiple of sqrt(r).
The arbitrary prescribed targets affect the mean, not this variance. This
finite Gaussian polynomial-plus-power field is not stationary and is not
claimed to realize the periodic model. It satisfies the old local H-valued
regularity and positive limiting pin Gram, which are exactly the assumptions
being distinguished.

## 7. Reproduction and assurance boundary

`regression_check.py` uses Fraction row matrices against independent unit
Gaussian coefficients, with exact Gauss–Jordan inversion. For a smooth finite
model it computes every pin, covariance, regression coefficient, mean and
residual from direct endpoint polynomials. No simulated Gaussian sample,
external numerical library, conditional field API or principal root is used.
The model is

 f=Z0+Z1 x+Z2 y+Z3 x^2/2+Z4 xy+Z5 x^3/6+Z6 x^2 y/2
      +Z7 y^2/2+Z8 x^4/24+Z9 x^3 y/6+Z10 xy^2/2.

On |x|<=1/2 all required derivative norms are<=2. Conservative inputs
Lp=Lv=2,p0=3,v0=2,lambda=1,Rbar=1,d0=4,Ld=1/12 give
U=5,V=4,Lg=20,Lk=18,B=40,Lb=836,Cm=10042/3,Cz=2590,R=1/40.
Nine dyadic radii within that range verify (3). Error is genuinely nonzero:
the two Q endpoints alone contribute r^2/2. Five rough-model cases check
(15) by an independent full conditional-covariance calculation.

Run `python -B -S test_regression.py` and the optimized equivalent. Twelve
methods cover36 frame inversions; contact Gram/rows;8 orthogonality cases;
an exact affine second-moment identity;9 nontrivial coupling-rate cases;
9 row-rate cases;5 rough conditional variances; input/CLI/error contracts.
The standalone baseline has87 controls and identical stdout in both modes.
M1–M6 must exit1 with, respectively, CONDITIONAL_MEAN,
RESIDUAL_ORTHOGONALITY, CUBIC_PIN_TARGET, KERNEL_LIPSCHITZ_MASS,
NO_SQRT_LIPSCHITZ, EXTRA_REGULARITY_REQUIRED, prefixed `REGRESSION_FAIL: `.
Invalid labels/options exit2. These finite countermodels cannot prove the
continuum Hilbert statement. The provided proof and source hypotheses need
a fresh nonauthor read. Existing CI does not automatically run these scripts
or formalize this note. No old review or kernel receipt is rebound.
