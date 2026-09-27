# Quantitative critical-point geometry and a cubic intermediate-saddle identity

Object: OA-SIMPLEX-CUBIC-20260925-v1. Author: OpenAI / ChatGPT.
Disposition: new author-side derivation with explicit proofs and exact algebra checks; no independent acceptance or global RN/persistence promotion.

## 1. Scope and the correction to the informal statement

The statement “three nearby noncollinear critical points force three small Hessians” requires a uniformly nondegenerate *scaled* triangle and a bound on the Hessian Lipschitz constant. Mere noncollinearity separately at each radius is insufficient. The deterministic result does not require Gaussianity, endpoint indices or prescribed heights.

The later cubic-index identity does use the six maximum/saddle pin equations and a third critical point at an intermediate height. It is distinct from the Gaussian count theorem in TRANSVERSE_CONTACT_ASYMPTOTIC.md.

## 2. Quantitative simplex theorem

Let f be C^{2,1} on an open set containing a convex domain K, with

    ||H(x)-H(y)||_op <= L ||x-y||,  x,y in K.

Choose x_0,...,x_k in K, 1<=k<=d, and write e_i=x_i-x_0. Suppose the d-by-k matrix E=[e_1 ... e_k] has full column rank. Let V=range(E), P_V its orthogonal projector, and

    G=[grad f(x_1)-grad f(x_0) ... grad f(x_k)-grad f(x_0)],
    R4=(sum_i ||e_i||^4)^(1/2),  s=sigma_min(E)>0.

Then

    ||H(x_0) P_V||_op <= (||G||_F + (L/2) R4)/s.                 (2.1)

For each j,

    ||H(x_j) P_V||_op <= (||G||_F + (L/2) R4)/s + L||e_j||.    (2.2)

Proof. The vector-valued fundamental theorem of calculus gives

    grad f(x_i)-grad f(x_0)=H(x_0)e_i+R_i,
    ||R_i|| <= integral_0^1 Lt||e_i||^2 dt = (L/2)||e_i||^2.

Thus H(x_0)E=G-R, with ||R||_F<=(L/2)R4. Since E E^+=P_V and ||E^+||=1/s, (2.1) follows. Hessian Lipschitz continuity proves (2.2). QED.

If x_i=x_0+r v_i, Vmat=[v_1 ... v_k], sigma_min(Vmat)>=sigma_*>0, and the gradients vanish, then

    ||H(x_j)P_V|| <= Lr [(sum_i||v_i||^4)^(1/2)/(2sigma_*)+||v_j||]. (2.3)

If instead ||grad f(x_i)||<=epsilon, replace the right side by

    2 sqrt(k) epsilon/(r sigma_*)
      + Lr [(sum_i||v_i||^4)^(1/2)/(2sigma_*)+||v_j||].        (2.4)

Consequently numerical critical-point tolerances must be O(r^2), or better, to retain an O(r) Hessian conclusion at a uniformly shaped simplex. A fixed gradient tolerance is not enough as r decreases.

### Full-dimensional and partial-span consequences

For k=d, P_V=I, so d+1 well-shaped nearby critical points force every Hessian to be O(Lr). Then

    product_{j=0}^d |det H(x_j)| <= C (Lr)^{d(d+1)}.           (2.5)

For k<d, only k singular values are forced small. If ||H(x_j)||<=K_2 and ||H(x_j)P_V||<=delta_j, the singular-value minimax principle gives

    |det H(x_j)| <= delta_j^k K_2^{d-k}.                     (2.6)

Three noncollinear points in dimension three therefore do NOT force the full Hessian norm small: they constrain a two-dimensional span. A term z^2/2 in the remaining coordinate is an immediate counterexample to the stronger assertion. They do give determinant suppression O(r^2) per Hessian if the remaining norm is bounded.

## 3. An explicit constant for the planar transverse chart

Let M=(-r/2,0), S=(r/2,0), X=(ru,rv), |(u,v)|<=B and |v|>=eta>0. Assume all three gradients are zero and the same Lipschitz bound holds on their convex hull. Put D=B+1/2 and

    C0 = (1/2)[1+(D^2+D)/eta],
    CH = C0+D.

Then

    ||H_M|| <= C0 Lr,
    ||H_S|| <= (C0+1)Lr,
    ||H_X|| <= CH Lr,
    |det H_M det H_S det H_X| <= CH^6 L^6 r^6.               (3.1)

Proof. The endpoint pair gives ||H_M e_x||<=Lr/2. Expanding the vector gradient from M to X gives

    ||H_M((u+1/2),v)|| <= (Lr/2)[(u+1/2)^2+v^2].

Subtract (u+1/2)H_M e_x and divide by v. The resulting second-column bound, together with ||H||<=||H e_x||+||H e_z||, yields C0. Transport to S and X by the Lipschitz bound. In two dimensions |det H|<=||H||^2. QED.

This explicit 1/eta dependence identifies a real geometric boundary. It does not solve the shrinking thin belt eta->0.

### Sharpness in r

    f_r(x,z)=x^3/3-rx^2/2+z^3/3-rz^2/2

has critical points (0,0),(r,0),(0,r). Their Hessians are diag(-r,-r), diag(r,-r), diag(-r,r); the absolute triple product is exactly r^6. The third-derivative bound is uniform. The exponent 6 cannot be improved from these deterministic assumptions alone.

### Why noncollinearity alone is insufficient

Set

    f_r(x,z)=(z-x^2)^2/2+x^4/4-rx^3+r^2x^2.

The three points (0,0),(r,r^2),(2r,4r^2) are critical and noncollinear for each r>0. They approach one another and f_r has uniformly bounded third derivatives on a common compact neighborhood, but f_zz=1 everywhere. The scaled triangle becomes flat, and no uniform O(r) bound on the full Hessian is true. This counterexample does not claim that its determinant product violates a separate determinant-only estimate.

## 4. All cubic polynomials obeying the six pins

Use scaled coordinates (s,t), with endpoint heights 0,-k at (-1/2,0),(1/2,0), k>0. Every real polynomial of total degree at most three satisfying these six constraints has the form

    P(s,t)=-k/2+2ks^3-(3k/2)s
             +(A/2)t^2+(q/2)(s^2-1/4)t+(c/2)st^2+(d/6)t^3. (4.1)

This is obtained by solving the six affine equations for the ten cubic coefficients. In particular the -1/4 term and midpoint height offset are forced, not optional conventions.

Let X=(u,v), v!=0, and impose

    grad P(X)=0,  P(X)=-k theta,  0<theta<1.

Writing D=u^2-1/4 and Lc=2u^3-3u/2-1/2, solve for the remaining three coefficients in terms of q:

    c=-12k D/v^2-2qu/v,
    d=12k(Lc+theta)/v^3+3qD/v^2,
    A=(12ku+6k+qv-12k theta)/(2v^2).                        (4.2)

The scaled Hessians are

    B_M=[[-6k,-q/2],[-q/2,A-c/2]],
    B_S=[[ 6k, q/2],[ q/2,A+c/2]],
    B_X=[[12ku+qv,qu+cv],[qu+cv,A+cu+dv]].                 (4.3)

## 5. Exact intermediate-saddle identity

Define

    w=(qv+12ku)/(6k).

Direct substitution into (4.3) gives

    det B_M = (9k^2/v^2)[4theta-(w+1)^2],
    det B_S = (9k^2/v^2)[4(1-theta)-(w-1)^2],
    det B_X = -(9k^2/v^2)[(w+1-2theta)^2+4theta(1-theta)]. (5.1)

Every factor in the bracket in the last line is nonnegative, and the second term is strictly positive. Therefore

    det B_X < 0.                                           (5.2)

**Exact cubic theorem:** a noncollinear third critical point at a strictly intermediate height in the six-pin cubic model is necessarily a nondegenerate saddle. This conclusion needs no presumed endpoint index. It is an exact polynomial result; for a smooth non-cubic field it describes the leading contact model, not an automatic pointwise assertion at finite r.

### Feasibility and positivity, not an empty event

Set w=-1. For every u, v!=0, k>0 and theta in (0,1), choose q=6k(-1-2u)/v and then (4.2). The determinants are

    det B_M=36k^2 theta/v^2>0,
    det B_S=det B_X=-36k^2 theta/v^2<0.

Since (B_M)11=-6k<0, M is a maximum; S and X are saddles. Thus an open neighborhood of these coefficients satisfies the prescribed endpoint types and a saddle witness.

A rational example is u=2,v=1,k=1,theta=1/2:

    q=-30,  A=-3,  c=75,  d=-363/2.

The Hessians are

    B_M=[[-6,15],[15,-81/2]], det=18,
    B_S=[[ 6,-15],[-15,69/2]], det=-18,
    B_X=[[-6,15],[15,-69/2]], det=-18.

All three gradients vanish and P(X)=-1/2. This example supplies a nonempty type-compatible contact set; it does not identify an elder-rule failure event.

## 6. Provenance and limits of the contribution

The simplex theorem is an elementary consequence of Taylor's formula and linear algebra; it should not be advertised as a worldwide-first theorem. Gaussian multi-point interpolation and determinant renormalization are established tools, notably in Gass–Stecconi (arXiv:2305.17586). The possible research contribution here is the exact six-pin specialization, typed determinant identity and its use in a specified persistence-pair conditional count. That novelty still requires an independent literature review.

No general persistence-pairing theorem, thin-belt estimate, d=3 full-Hessian claim, or global RN closure follows from this note alone.
