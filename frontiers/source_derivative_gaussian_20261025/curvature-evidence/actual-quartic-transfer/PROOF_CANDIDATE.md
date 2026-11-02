# Actual pin-preserving quartic comparison and capture interface

Author-side mathematical candidate by OpenAI/Codex root, 26 October 2026.
This is new research, not a Lean result or an independent review. Existing
verification of unchanged source modules and the closed conditional LM001
certificate is reused. No scientific-status change is made.

## Source objects and exact scope

Use an actual sample f = smoothSourceField 2 L omega. Its global derivative
majorants Gamma_k are those in the qualified SourceConditionalMajorant.lean
at Math- 37f8f01db8b7e30190f09bf784d1b4e3419da540. In particular every
kth multilinear derivative has operator norm at most Gamma_k globally.
The field is smooth on R^2. Lean source coordinates carry the Pi sup norm.
For the Euclidean interpretation below, ||v||_infinity<=||v||_2 means every
Euclidean unit direction is admissible in the scalar multilinear derivative
bound. Thus Gamma_k also bounds the Euclidean directional derivatives used
here. Vector-gradient and matrix operator conversions are made explicitly
componentwise with the safe factor two in Section 3; no equality between
Pi and Euclidean norms is assumed. Write G=Gamma_5 and

    R = 1 + sum_{k=0}^5 Gamma_k >= 1.

Fix 0<r<=1, h=r/2, M=(-h,0), S=(h,0). Assume the exact physical pins

    grad f(M)=grad f(S)=0,
    f(S)-f(M)=-r^3/6.

These are derived almost surely under the actual canonical sourceSmoothLaw
hL r b when its current pin covariance is invertible, by the qualified raw
prescribed-pin support theorem. For L nonzero that hypothesis is derived on
a sufficiently small positive-radius interval; support is not asserted for
all 0<r<=1. This proof first treats a deterministic pinned sample. No arbitrary
null-pin conditional version is substituted.

At the origin define literal, unscaled partial derivatives

    q=f_yy, a=f_xxy, w=f_xyy, z=f_yyy,
    c40=f_xxxx, c31=f_xxxy, c22=f_xxyy,
    c13=f_xyyy, c04=f_yyyy, t=f_xxx.

Let U=(a,w,z,c40,c31,c22,c13,c04) and

    R0=1+|a|+|w|+|z|+|c40|+|c31|+|c22|+|c13|+|c04|.

The q coordinate is deliberately not part of LM001's U or R0. The global
majorants give R0<=1+3 Gamma_3+5 Gamma_4<=5R. Each scalar derivative is
bounded by the operator norm by evaluation on unit coordinate directions.

Compare the actual scaled gradient

    F_r(X,Y)=r^-2 grad f(rX,rY)

with the EXACT polynomial F_r^(4) displayed in LM001, with s=q/r and the
literal U above. The polynomial is not asserted to be the unmodified
ordinary Taylor polynomial. Its lower coefficients are changed to preserve
the two gradient pins, and its axial cubic coefficient is exactly two.

LM001 source: imports/hardening_ebedb780/P02-LM-001/proof.md.export.txt
in Math- 37f8f01, LCR-CAP-009-v1.0 (closed conditional degree-four capsule).
LM004 v1.1 source: main git blob bb2ee617fa88ecbae41193887dd2ff6c7e91c955,
frozen body SHA256 d43179f3abfd7e93f988725f3b89a5826cc71e0fa04840f65c7f93f3359d0f87.
The robustness implication below remains conditional on that exact LM004
result's validity/applicability; its old candidate header is not promoted.

## 1. Fifth-order control of the axial cubic coefficient

Let u(x)=f(x,0). The completed actual confluent pin identities yield

    2 = 6 integral_{-1/2}^{1/2} (1/4-v^2) u'''(rv) dv.

This also follows directly from the two zero axial gradient pins and the
height difference, using the exact pin5 Peano identity. Taylor's theorem
applied to u''' gives

    |u'''(rv)-t-rv*c40| <= (G/2)*r^2*v^2.

The Peano kernel is nonnegative and even, with

    6 integral K = 1,
    integral K*v = 0,
    6 integral K*v^2 = 1/20.

Hence

    |t-2| <= G*r^2/40.                                      (1)

The symmetry cancellation is essential: a mere Lipschitz bound by Gamma_4
would only give an O(r Gamma_4) estimate and would not justify (1).

## 2. Low Taylor coefficients forced by exact gradient pins

For v(x)=f_x(x,0), Taylor to degree three at +/-h has remainder at most
G*h^4/24=G*r^4/384 at either endpoint. Adding and subtracting the zero
endpoint values gives

    |f_x(0)+t*r^2/8| <= G*r^4/384,
    |f_xx(0)+c40*r^2/24| <= G*r^3/192.

Using (1) in the first inequality,

    |f_x(0)+r^2/4| <= (11/1920)*G*r^4.                       (2)

Apply the same degree-three expansion to v(x)=f_y(x,0). Its second and
third derivatives are a and c31. The exact transverse gradient pins give

    |f_y(0)+a*r^2/8| <= G*r^4/384,
    |f_xy(0)+c31*r^2/24| <= G*r^3/192.                       (3)

These use total derivative order five for the remainder of a gradient
component. They neither confuse c31 with f_xxxx nor identify f_xxy with
the axial cubic derivative.

## 3. Uniform Euclidean/operator C1 comparison on the fixed ball

Let T be the degree-three Taylor polynomial of grad f at the origin,
scaled as r^-2 T(rX,rY). With d=||(X,Y)||_2, component Taylor remainders
and the fifth derivative bound give

    ||F_r-r^-2 T(rX,rY)||_2 <= G*r^2*d^4/12,
    ||DF_r-D(r^-2 T(rX,rY))||_op <= G*r^2*d^3/3.            (4)

The safe constants use sqrt(2)<=2 for the vector and the 2-by-2 operator
norm at most twice the maximum absolute entry for the Hessian remainder.
All derivatives and errors use the Euclidean and induced operator norms.
The C1 norm is exactly LM004's MAX of the value-norm supremum and the
derivative-operator-norm supremum, not their sum. This norm convention is
needed for the stated constant three.

The EXACT LM001 field is

    P_X=X^2-1/4+aXY+(w/2)Y^2
      +r[(c40/6)X(X^2-1/4)+(c31/6)(3X^2-1/4)Y
          +(c22/2)XY^2+(c13/6)Y^3],
    P_Y=(q/r)Y+(a/2)(X^2-1/4)+wXY+(z/2)Y^2
      +r[(c31/6)X(X^2-1/4)+(c22/2)X^2Y
          +(c13/2)XY^2+(c04/6)Y^3].

Equations (1)--(3) show that the scaled Taylor polynomial differs from P
by a constant vector of norm <=G*r^2/120, a linear symmetric matrix of
operator norm <=G*r^2/64, and the single term ((t-2)X^2/2,0). The latter
has value norm <=G*r^2*d^2/80 and derivative norm <=G*r^2*d/40.
Combining these estimates with (4),

    ||F_r-P||_2 <= G*r^2*(1/120+d/64+d^2/80+d^4/12),
    ||DF_r-DP||_op <= G*r^2*(1/64+d/40+d^3/3).

On the closed Euclidean ball of radius two the two constants are
683/480 and 2623/960 respectively, both strictly less than three. Thus

    ||F_r-F_r^(4)||_{C1(ball(0,2))} <= 3*r^2*Gamma_5.        (5)

This is the missing actual pin-preserving Taylor comparison with an
explicit constant independent of r, U, b and the sample. The gradient
property is preserved: F_r is the gradient of r^-3 f(rX,rY), and P is
symmetric by direct differentiation of its displayed formula. The exact
pins F_r(+/-1/2,0)=0 are retained.

## 4. The same global regularity cutoff controls the adaptive tolerance

Put K0=4096, epsilon0=1/(1024*K0), and

    epsilonStar=epsilon0/5^5,
    Kcap=2*K0*5^5+10=25600010.

Suppose

    r*R^5 <= epsilonStar,
    q <= -Kcap*r*R^5.                                     (6)

Because R0<=5R, (6) implies the exact LM001 regularity condition
r*R0^5<=epsilon0. Also R>=1 implies

    2*K0*R0^5+2*R0 <= (2*K0*5^5+10)*R^5,

so q/r<=-(2*K0*R0^5+2*R0), the exact curvature threshold.

Let W=Fstar/(K0*R0^5), Fstar>=1, be the certificate width. Then
R0*W>=1/(K0*R0^4). Since Gamma_5<=R and r<=1,

    12*K0*R0^4*r^2*Gamma_5
      <=12*K0*5^4*r^2*R^5
      <=12*K0*5^4*r*epsilonStar
      =3*r/1280 <=3/1280 <1.

Therefore (5) is smaller than R0*W/4, exactly the Euclidean/operator
adaptive tolerance in LM004. No additional fifth-derivative cutoff is
needed: Gamma_5 is already included in R and controlled by (6).

The LM001 certificate regions fit within the radius-two ball: its size
bound R0*W<=1/2048 gives endpoint radius rho=8R0W<=1/256, endpoints of
norm1/2, and strip width W<=1/2048. The cone pieces, central rectangle,
endpoint balls and connecting sections are all contained in that ball.
The exact field is smooth on an open neighborhood of the ball.

## 5. What this establishes, and what still needs proof

As a deterministic source join, (1)--(5) prove the literal actual-field
comparison required by LM004. If the exact LM004 robustness implication
is accepted as an input, (6) implies selected-branch capture for F_r.
Positive scaling of space and time identifies this branch with the
actual source gradient flow: x=r*(X,Y), and d(X,Y)/dt=r^-1 grad f(rX,rY)
is r times F_r, with r>0. The orientation e_u dot(M-S)>0 is preserved.

For an actual measurable noncapture event defined with this branch, the
corresponding deterministic inclusion would be

    noncapture subset {epsilonStar < r*R^5}
                       union {q > -Kcap*r*R^5}.

The cubic curvature module being implemented bounds the larger event with
q>=-Kcap*r*R^5 by C*r^3 under the existing actual full-carrier weighted
law. Thus a qualified capture theorem and event measurability join would
convert that probability driver into a local selected-branch complement
estimate. This does not identify the law with a geometric point-process
Palm disintegration, settle global elder pairing, or prove the remaining
lifetime/counting parent. No such closure is asserted here.

Next proof obligations are exact formalization of (1)--(5), source-bound
independent review, the current validity/review of LM004, and an explicit
measurable definition/application of the actual capture event. An old
closed finite-degree certificate is not silently promoted to the exact
field, and this new analytic proof is not described as kernel checked.
