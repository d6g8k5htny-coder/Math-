# A4 compact-sector eigenframe and ridge coauthor derivation

This is a focused analytic **coauthor contribution**, not a nonauthor review or a claim that the complete Gaussian A4 sector theorem has been proved. The main author owns the global selection argument and final proof. No source publication, network mutation, Lean execution, field draw, or reservation is made here.

## 1. Conventions and precise conclusions

Work on a fixed flat oriented two-dimensional torus. Write an oriented orthonormal frame as `(u,v)`, with `v=Ju`, and use the raw mixed-derivative coordinates of every symmetric tensor. In particular the Hessian measure is

`dH11 dH12 dH22`,

with one, unweighted, off-diagonal coordinate. At a critical maximum let the soft eigenvalue be `s=-lambda`, the hard eigenvalue be `a`, and assume

`a <= -a0 < 0`, `0 < lambda`, and `-lambda > a`.

The conclusions established below are:

1. The Hessian change of variables has absolute Jacobian `|a+lambda|`.
2. A full angular circle together with the restriction `Q5>0` counts each admissible oriented soft eigendirection exactly once. There is no further factor `1/2` in this convention.
3. The ridge corrections are

   `Q4 = Fuuuu - 3 gamma^2/a`,

   `Q5 = Fuuuuu - 10 eta gamma/a + 15 gamma^2 B/a^2`,

   where `gamma=Fuuv`, `eta=Fuuuv`, and `B=Fuvv`.

4. Replacing the two pure derivatives `(Fuuuu,Fuuuuu)` by `(Q4,Q5)`, with all other jets fixed, has Jacobian one.
5. The sector substitution

   `(lambda,T3,Q4)=(alpha r^3,beta r^2,-36r)`

   has absolute Jacobian `36 r^5`. Together with one-point Rice and the Hessian parametrization, the exact finite-r algebraic weight is

   `36 alpha (-a) |a+alpha r^3| r^8`.

   Its leading coefficient is `36 alpha a^2 r^8`.
6. Uniform spatial `C7` bounds on the conditional fields and their parameter derivative suffice for the bounded-r-derivative remainder needed in the lifetime change of variables. No `C8` bound is required by this step.

All density formulas below retain the actual full joint Gaussian jet density in the moving frame. Rotation invariance of the field and independence of derivative orders are not used.

## 2. Hessian Jacobian with the raw off-diagonal coordinate

Let `R_theta` have columns `u_theta=(cos theta,sin theta)` and `v_theta=(-sin theta,cos theta)`. Then

`H=R_theta diag(-lambda,a) R_theta^T`.

In the fixed ambient frame,

`H11=-lambda cos^2 theta+a sin^2 theta`,

`H12=(-lambda-a) sin theta cos theta`,

`H22=-lambda sin^2 theta+a cos^2 theta`.

At `theta=0`, the columns of the derivative with respect to `(lambda,a,theta)` are

`(-1,0,0)`, `(0,0,1)`, and `(0,-lambda-a,0)`.

The determinant therefore has absolute value `|-lambda-a|=|a+lambda|`. Conjugation by `R_theta` on symmetric matrices has determinant one in the coordinate volume `dH11 dH12 dH22`: it is a continuous representation of the rotation group; its determinant is positive, and it preserves the equivalent quadratic form `H11^2+2H12^2+H22^2`, so its determinant is exactly one. This transports the calculation at zero to every angle.

Consequently, on the simple-eigenvalue chamber with the eigenvalues ordered as above,

`dH11 dH12 dH22=|a+lambda| d lambda da d theta`

when `theta` ranges over any half-open interval of length `pi`. This is a one-to-one parametrization except for the angular endpoint, a null set. Using an orthonormalized off-diagonal coordinate `sqrt(2)H12` would change the coordinate density and Jacobian together. That is a different convention and supplies no extra factor here.

The gradient rotation has determinant one. For each order `k`, rotation on `Sym^k(R^2)` has determinant one in the raw mixed-derivative coordinates: it preserves a positive factorial-weighted quadratic form and is connected to the identity. Thus simultaneous conversion of all jets through order five into the moving frame has unit determinant at fixed `theta`. Although the moving-frame high-jet coordinates depend on `theta`, the combined Jacobian is block triangular once the Hessian coordinates have been parametrized. Its only nonunit factor is the Hessian factor just calculated.

## 3. Why the full circle with Q5>0 has no extra half

Changing `theta` to `theta+pi` changes both frame vectors to their negatives. A derivative tensor component of total order `k` gains the factor `(-1)^k`. Thus `a`, `lambda`, `Fuuuu`, and `eta` are unchanged; `gamma`, `B`, `T3=Fuuu`, and `Fuuuuu` change sign. The formulas in Section 4 give

`Q4(theta+pi)=Q4(theta)`, `Q5(theta+pi)=-Q5(theta)`.

On the sector `Q5` in a compact interval contained in `(0,infinity)`, each soft eigenline has exactly one representative on the full circle satisfying `Q5>0`. Therefore the parametrization

`theta in [0,2pi)`, `Q5>0`

is one-to-one on this chamber, up to the angular endpoint. Equivalently, start with the length-pi angular parametrization and split its `Q5>0` and `Q5<0` pieces. On the negative piece, send `theta` to `theta+pi` and negate all odd-order components. This is a unit-Jacobian transformation and sends the negative piece into the other half of the full-circle positive-Q5 chart.

The same argument applies with additional sector restrictions, including `T3/r^2` in a positive interval: those restrictions are evaluated only in the uniquely selected positive-Q5 frame. There is no claim that their values are the same in both frames. There is no unordered-pair convention in this one-point birth count.

The event `Q5=0` is outside the chosen compact sector. Under a nonsingular full jet density it is also a null hypersurface. It plays no role in this normalization.

## 4. Exact nonlinear ridge derivatives

Use Euclidean coordinates `(s,y)` along `(u,v)` centered at the critical point. Suppose

`F_s=F_y=F_sy=0`, `F_yy=a != 0`.

The implicit-function theorem gives the transverse critical ridge `y=h(s)`, defined near zero by `F_y(s,h(s))=0`, with `h(0)=h'(0)=0`. Set

`c2=h''(0)`, `c3=h'''(0)`.

Differentiating the defining equation, or comparing its Taylor coefficients, gives

`a c2+gamma=0`,

`a c3+3B c2+eta=0`.

Hence

`c2=-gamma/a`, `c3=-eta/a+3B gamma/a^2`.

Let `g(s)=F(s,h(s))`. Up to order five, the terms affected by the ridge are precisely

`a h(s)^2/2 + gamma s^2 h(s)/2 + B s h(s)^2/2 + eta s^3 h(s)/6`.

Writing `h(s)=c2 s^2/2+c3 s^3/6+O(s^4)`, the order-four coefficient is

`a c2^2/8+gamma c2/4=-gamma^2/(8a)`.

After multiplication by `4!`, this gives

`g''''(0)=Fuuuu-3gamma^2/a=Q4`.

The order-five coefficient is

`a c2 c3/12+gamma c3/12+B c2^2/8+eta c2/12`.

The first two terms cancel because `a c2+gamma=0`. Multiplying the remaining terms by `5!` gives

`g'''''(0)=Fuuuuu-10 eta gamma/a+15 gamma^2 B/a^2=Q5`.

Also `g''(0)=-lambda` and `g'''(0)=T3`. None of these identities requires `lambda=0`.

The local source `singularity-taxonomy-next-gap-20261017/math-elder-cusp-proof.md`, SHA-256 `35b9c5943cf35919f2046ba194945ba759be654edf5d5ad77ba17b1f5c5377fd`, lines 63-74, uses the same correction: its `120 Q1` is the present `Q5`. Only this formula and its stated conventions were consulted here; no claim of a new whole-source review is made.

Fix `a`, `gamma`, `eta`, `B`, and every jet coordinate other than the two pure components. Then

`(Fuuuu,Fuuuuu) -> (Q4,Q5)`

has derivative matrix equal to the two-dimensional identity. It is an affine translation in these two coordinates; its Jacobian is exactly one. With the other coordinates retained as variables, the complete transformation remains triangular with unit determinant. The inverse formulas are

`Fuuuu=Q4+3gamma^2/a`,

`Fuuuuu=Q5+10 eta gamma/a-15 gamma^2 B/a^2`.

They are smooth with uniformly bounded derivatives on a compact hard-eigenvalue interval bounded away from zero. A condition on the raw pure fourth derivative alone is not the condition `Q4=-36r`.

## 5. Radial sector substitution and the coefficient ledger

Let `omega` denote all moving-frame derivatives of orders three through five other than `T3`, `Fuuuu`, and `Fuuuuu`; there are twelve such raw mixed-derivative coordinates. In particular `gamma`, `eta`, and `B` are retained in `omega`. Retain `b=F(0)` and the hard eigenvalue `a`. Use

`lambda=alpha r^3`, `T3=beta r^2`, `Q4=-36r`, `Q5=q`.

The derivative of `(lambda,T3,Q4)` with respect to `(alpha,beta,r)` is

`[[r^3,0,3alpha r^2],[0,r^2,2beta r],[0,0,-36]]`.

Its absolute determinant is `36r^5`, with no factors involving alpha or beta. The one-point Rice determinant is `|det H|=lambda(-a)` on the maximum chamber. Multiplying it by the Hessian and radial Jacobians gives

`lambda(-a)|a+lambda| * 36r^5 = 36alpha(-a)|a+alpha r^3|r^8`.

For sufficiently small r, compactness and `a<=-a0` give `-lambda>a`; the absolute value can then be written `-a-alpha r^3`. The factor divided by `r^8` tends uniformly to `36alpha a^2`.

To specify the density argument without hiding any Gaussian independence, order the complete moving-frame 5-jet as

`Jtheta=(F,Fu,Fv,Fuu,Fuv,Fvv, all raw order-3, order-4, order-5 entries)`.

Its dimension is 21. The target is

`z_r=(b,0,0,-alpha r^3,0,a,T3=beta r^2, omega, Fuuuu=-36r+3gamma^2/a, Fuuuuu=q+10eta gamma/a-15gamma^2B/a^2)`

with entries placed in their stated tensor order. Let `p_{x,theta}(z_r)` be its actual 21-dimensional density. At r=0 the limiting target retains the nonlinear mixed-jet terms:

`Fuuuu=3gamma^2/a`,

`Fuuuuu=q+10eta gamma/a-15gamma^2B/a^2`.

These raw derivatives are generally nonzero. Replacing them by `(0,q)` in the Gaussian density would be an error.

For fixed `(x,theta)`, write the canonical Gaussian conditioning as `F_r=m(z_r)+R`, with R independent of the jet and with a distribution not depending on r. If all components through order five are conditioned, the residual projection is unchanged by a moving-frame rotation, because that rotation is an invertible change of coordinates on the same finite jet span. The notation may still retain `(x,theta)` if convenient.

Suppose the main proof supplies a deterministic marked lifetime

`Delta_r=r^5 L_r`,

on a compact parameter box and on a fixed residual cutoff, with `L_r -> L0>0` uniformly and `sup |partial_r L_r|<infinity`. The fixed residual cutoff is essential to this immediate formulation: a cutoff on the full field changing with r would require a separate boundary argument.

For small r,

`partial_r Delta_r=r^4(5L_r+r partial_r L_r)>0`.

The lifetime density obtained from this radial coordinate therefore has leading coefficient

`(36/(5 Vol X)) integral alpha a^2 L0^(-9/5) p_{x,theta}(z_0) P(residual cutoff at x,theta) dx dtheta db da domega dq dalpha dbeta`.

The integration ranges are the main proof's fixed compact boxes, including the full angular circle and positive q interval. This displayed coefficient is conditional on the main proof establishing the deterministic lifetime and count-once mark. The coarea algebra supplies the power `ell^(4/5)` because `r^8/(partial_r Delta_r)` tends to `r^4/(5L0)` and `r^4=ell^(4/5)L_r^(-4/5)`. The corresponding cumulative exponent is `9/5`, with coefficient `(5/9)` times the density coefficient. This concerns the restricted compact sector, not the leading density of all bars.

## 6. C7 control is enough for the radial derivative

Here is the precise sufficient setup. Fix the compact jet parameters other than r, including a hard eigenvalue bounded away from zero. Suppose `r -> F_r` is continuously differentiable with values in spatial `C7`, and both `||F_r||C7` and `||partial_r F_r||C7` are uniformly bounded. The Gaussian regression above has this property on a fixed `C7` residual ball: the mean is linear in the finite targets, which are polynomial in r with smooth coefficients on the chosen parameter box. Compact invertibility of the jet covariance controls the mean and its r derivative.

On a sufficiently small fixed rectangle, the transverse derivative remains uniformly negative. The implicit ridge `h(r,s)` has uniformly bounded spatial derivatives through order six. Its direct construction uses `F_y` in spatial `C6`. The ridge value `g_r(s)=F_r(s,h(r,s))` has bounded spatial `C7` norm because

`partial_s g_r=(F_r)_s(s,h(r,s))`.

The right side is spatial `C6`, so this identity gives the seventh spatial derivative without needing a seventh derivative of h. The parameter envelope identity is

`partial_r g_r(s)=(partial_r F_r)(s,h(r,s))`.

It is spatial `C6` with a uniform bound. These assertions follow by the implicit-function chain rule and induction; the denominator in each implicit derivative is the uniformly nonzero transverse Hessian. There is no division by the small soft curvature.

Let `T_r(s)` be the exact degree-five Taylor polynomial of `g_r` at zero, whose coefficients are the ridge identities above. Write `R_r(s)=g_r(s)-T_r(s)`. Taylor's integral formula, also applied to `partial_r g_r`, yields uniformly

`|partial_s^j R_r(s)| <= C |s|^(6-j)` for `0<=j<=3`,

`|partial_s^j partial_r R_r(s)| <= C |s|^(6-j)`

where the second bound is used for `0<=j<=2`. Differentiation of the Taylor coefficients is legitimate because of the established mixed regularity. On a fixed compact xi interval define

`E_r(xi)=r^(-5) R_r(r xi)`.

Then `||E_r||C2(xi)<=Cr`. Moreover

`partial_r E_r=-5r^(-6)R_r(rxi)+r^(-5)(partial_r R_r(rxi)+xi partial_s R_r(rxi))`,

and the preceding bounds, differentiated in xi up to order two, give `||partial_r E_r||C2(xi)<=C`.

Consequently the scaled ridge converges in `C2`, and its r derivative stays bounded in `C2`. On a fixed compact polynomial sector with simple, uniformly separated roots, the implicit critical roots have bounded r derivatives. The lifetime between the selected birth and selected critical saddle then has `L_r=L0+O(r)` and bounded `partial_r L_r`. The main proof must establish which root gives the actual global elder death; these estimates alone do not establish that selection.

## 7. Pitfalls and remaining owner work

- Keep the raw Hessian measure and full-circle positive-Q5 convention together. Adding an antipodal half to that convention undercounts.
- Keep both hard-Hessian factors: one comes from Rice and the other from the eigenframe Jacobian. Their product tends to `a^2`, not `|a|`.
- Keep all mixed jets in the Gaussian density, including the nonlinear limiting values of the pure fourth and fifth derivatives.
- Use a fixed regression-residual cutoff to make the conditioning measure fixed in r. If changing that definition, recheck the lifetime pushforward and boundary contribution.
- The simple-root bounds and actual curved global trap remain the main author's responsibility. This document does not establish a full restricted-sector theorem by itself.
- No numerical onset, all-sector matching, full next correction, Poisson law, higher homology, Lean verification, scientific acceptance, or provider-distinct review follows from these calculations.

This finite contribution ends with the two coordinate transformations and regularity ledger delivered. There is no continuing source or runtime reservation.
