# Planar growing-window Taylor control and raw-to-rescaled Hessian bounds

Object: C91-PLANAR-WINDOW-TAYLOR-TRANSFER-20261003-v1.
Author: OpenAI/Codex root01a0bbb5, acting for Dylan Roy — delegated AI work.
Disposition: AUTHOR-SIDE PROOF CANDIDATE; full nonauthor review pending.
Personal reading PENDING; organizational independence0; scientific effect NONE.

This closes a deterministic estimate, not a Gaussian-law comparison. It makes
the planar window-size dependence implicit in FL.1 explicit, strengthens its
smoothness requirement from C5 to C4 for this purpose, and tracks values,
gradients and Hessians separately. The transfer formulas retain both genuine
typing-edge denominators. They do not introduce a separate pole at gamma=0.

## 0. Sources, setting and norms

Motivating source: Math243, frontiers/soft_fold_limit_20261002/PROOF.md,
head e8c76a4080e8e8be3dd9f613006263be6d53bad3, blob
6502cf7ba2edee47761e40308c15b7563b06d1f8, merged as
fa8b0d219e41f940fc58c9cdc7475236b5027b4a. Only its planar raw coordinates
and cubic model in Sections0–1 are needed; the Taylor proof below is complete
and does not consume its Gaussian or decision-limit theorem. The older source
header is not a current review register.

The coordinate comparison is with QS comment5961415030 and its local ellipse
notation. Its exact raw-model identity is re-derived below. A2 comment5963200491
supplies the proposed explicit trap box; its literal v1 is AMEND_REQUIRED in
C90 review5963477339. Any application of that particular box remains conditional
on the explicitly corrected geometric statement, not acceptance of the false
v1 lines. The main Taylor and matrix results here do not depend on A2.

Fix a flat planar torus of side L>0, an orthonormal frame (u,e), 0<k_-<=k_+,
k in[k_-,k_+], w>=1, r>0, and a C4 real field f. In this frame use the periodic
lift f(x,z). Put H=1+k_+ and assume

    r H w <= L/4.                                                    (W0)

This puts the physical raw window and the pin segments inside an injective
ball. The Taylor inequalities also hold for the lift without this restriction;
(W0) makes their local torus interpretation explicit. Let N be the maximum,
over the torus and all coordinate partials of orders0 through4, of their
absolute values. The frame is fixed; a frame-uniform operator derivative norm
may be used instead if it dominates all these partials.

Assume the exact pins

    M=(-r/2,0), S=(r/2,0), f(M)=b, f(S)=b-k r^3,
    grad f(M)=grad f(S)=0.                                       (W1)

No Gaussian, nondegeneracy, Morse, or independence hypothesis is needed for
Theorems1–2. In particular the sign or size of f_zz(0) is unrestricted in
Theorem1. Define the midpoint coefficients

    lambda_tilde=-k f_zz(0)/r,
    gamma=f_xxz(0), B=f_xzz(0), C3=f_zzz(0),
    F_r(X,zeta)=(f(rX,rk zeta)-b)/(k r^3),
    G_k=2X^3-3X/2-1/2 +(gamma/2)(X^2-1/4)zeta
        -(lambda_tilde/2)zeta^2 +(kB/2)X zeta^2
        +(k^2 C3/6)zeta^3.                                    (W2)

For a function E on W_w={|X|<=w,|zeta|<=w}, let |E|_j be the maximum
of the suprema of all coordinate derivatives of EXACT total order j.
Thus |E|_2 bounds entries of its Hessian, not its operator norm.

## 1. Explicit estimates for every window size

Put M1=max(1/k_-,1), M2=max(1/k_-,1,k_+), and

    K0=9/(64 k_-)+1/16+H^4/(24 k_-),
    K1=33/(128 k_-)+1/16+M1 H^3/6,
    K2=17/(48 k_-)+1/24+M2 H^2/2.                          (W3)

**Theorem1.** Under(W0)–(W2), for j=0,1,2,

    |F_r-G_k|_j <= K_j N r w^(4-j).                        (W4)

The constants do not depend separately on a transverse eigenvalue. Its
quadratic coefficient is retained exactly in G_k. For k_-=k_+=1,

    K0=167/192, K1=635/384, K2=115/48.                    (W5)

### 1.1 All pin correction coefficients

Write a=r/2 and g(x)=f(x,0), g_i=g^(i)(0). Taylor's theorem gives

    g(+-a)=g_0+-a g_1+a^2 g_2/2+-a^3 g_3/6+rho_+-,
    g'(+-a)=g_1+-a g_2+a^2 g_3/2+tau_+-,
    |rho_+-|<=N a^4/24, |tau_+-|<=N a^3/6.              (W6)

Adding/subtracting the zero derivative pins yields

    |g_1+a^2 g_3/2|<=N a^3/6, |g_2|<=N a^2/6.

The value difference is -8k a^3. After substituting the first identity,
it equals -(2/3)a^3 g_3 plus an error bounded by
2a(Na^3/6)+2(Na^4/24)=5Na^4/12. Consequently

    |g_3-12k|<=5Na/8=5Nr/16,
    |g_1+6k a^2|<=23Na^3/48=23Nr^3/384.               (W7)

The value average is b-4k a^3. It gives

    |g_0-(b-k r^3/2)|<=Na^4/8=Nr^4/128,
    |g_2|<=Nr^2/24.                                  (W8)

Now Taylor-expand q(x)=f_z(x,0) to order2 at +-a. Its third derivative is
bounded by N because f is C4, and q(+-a)=0. The same sum/difference gives

    |f_z(0)+a^2 gamma/2|<=Na^3/6=Nr^3/48,
    |f_xz(0)|<=Na^2/6=Nr^2/24.                        (W9)

These estimates require no fifth derivative and hold without distributional
assumptions. The pure transverse second derivative and the other third
derivatives in(W2) are kept exact.

### 1.2 Cubic Taylor remainder and differentiation

Let T3 be the full cubic Taylor polynomial of f at0. For alpha=(i,j),
m=|alpha|<=2, Taylor's theorem applied to D^alpha f gives

    |D^alpha(f-T3)(x,z)|
      <= N (|x|+|z|)^(4-m)/(4-m)!.                    (W10)

Indeed D^alpha T3 is precisely the Taylor polynomial of D^alpha f of
degree3-m; the multinomial sum bounds the remainder by the displayed
l1 power. Applying the raw derivatives r^i(rk)^j and dividing by k r^3
shows that the remainder's order-m raw derivatives are bounded by

    N r k^(j-1) (H w)^(4-m)/(4-m)!.                   (W11)

For m=0,1,2 the maxima of k^(j-1) are bounded respectively by
1/k_-, M1, M2. These are the final summands in(W3).

After division by k r^3, the difference between T3 and G_k is a linear
combination of the six monomials below. Its coefficient magnitudes are at
most N r times the middle column. The remaining columns bound exact-order
derivatives, after division by w^(4-m), uniformly for w>=1.

    monomial    coefficient/(N r)      m=0    m=1    m=2
    1           1/(128 k_-)              1      0      0
    X           23/(384 k_-)             1      1      0
    X^2         1/(48 k_-)               1      2      2
    X^3         5/(96 k_-)               1      3      6
    zeta        1/48                     1      1      0
    X zeta      1/24                     1      1      1

The last three column sums are respectively

    9/(64 k_-)+1/16,
    33/(128 k_-)+1/16,
    17/(48 k_-)+1/24.

Combining these with(W11) proves(W3)–(W4), including mixed derivatives.
Substitution H=2, M1=M2=1 proves(W5). QED.

### 1.3 The three window powers cannot generally be removed

In a fixed small coordinate neighbourhood take

    f_r(x,z)=b+2kx^3-(3/2)kr^2x-kr^3/2
                   +t(x^2-r^2/4)^2, t!=0 fixed.        (W12)

It has the exact pins, and its raw cubic model is the axial polynomial
in(W2). The error is EXACTLY

    (t r/k)(X^2-1/4)^2.                               (W13)

Its derivatives of orders0,1,2 grow respectively like r w^4, r w^3,
and r w^2. A fixed smooth cutoff equal to1 on a smaller neighbourhood
extends this family to the torus with a C4 norm bounded uniformly as r->0;
the coefficients of f_r are uniformly bounded there. Choose w->infinity
with r w->0 so the raw window stays in that smaller neighbourhood. Thus
no bound uniform in w with a smaller power in any of the three estimates
follows from the stated C4 assumptions. This is a deterministic rate
obstruction, not a Gaussian counterexample.

For example w=r^(-beta), 0<=beta<1/4, and bounded N give value error
O(r^(1-4beta)), gradient error O(r^(1-3beta)), and Hessian-entry error
O(r^(1-2beta)). This does not by itself assert that N is uniformly bounded
under a family of conditioned Gaussian laws.

## 2. Exact Hessian transfer without a standalone gamma denominator

Now set k=1, gamma!=0, lambda_tilde>0, and define

    psi=24 lambda_tilde/gamma^2,
    c=1-12B/gamma^2,
    R=8-144B/gamma^2+576C3/gamma^3,
    u=X+gamma zeta/12, Z=gamma zeta.

Expanding the cubic in(W2) gives EXACTLY

    G_1(X,zeta)=P(u,Z),
    P=2(u+1/2)^2(u-1)-(psi+2cu)Z^2/48+RZ^3/3456.      (W14)

The u^2 Z terms cancel; the u Z^2 coefficient is -c/24 and the Z^3
coefficient is R/3456. This verifies the model identity without consuming
an asymptotic law. Suppose psi>|c| and put

    a_S=24 lambda_tilde+gamma^2-12B>0,
    a_M=24 lambda_tilde-gamma^2+12B>0,
    kappa_S=(psi+c)/48, kappa_M=(psi-c)/48.

Then gamma^2 kappa_i=a_i/48 for i=S,M. At the respective pin, the
rescaled-to-raw derivative matrix is

    T_i = [[1/sqrt(3), -1/(12 sqrt(kappa_i))],
           [0,          1/(gamma sqrt(kappa_i))]].      (W15)

**Theorem2.** Let E be any C2 raw error on W_w, and suppose the raw image
of the ellipse being considered lies in W_w. If every entry of its raw
Hessian has absolute value at most epsilon2, then the corresponding
rescaled Hessian of e(u,Z)=E(u-Z/12,Z/gamma) satisfies

    ||D_i^2 e||op <= (2 epsilon2/3)
                         [1+(gamma^2+144)/a_i].        (W16)

*Proof.* The raw symmetric two-by-two Hessian has operator norm at most
2 epsilon2. By the chain rule the new Hessian is T_i^T (D^2 E) T_i.
Using the Frobenius norm to bound the matrix operator norm gives

    ||T_i||F^2=1/3+(1/144+1/gamma^2)/kappa_i
              =1/3+(gamma^2+144)/(3a_i).

This proves(W16). QED. Gamma=0 itself is outside this coordinate chart;
the formula proves a bound on nonzero gamma, not a chart defined at0.
The right side stays bounded as gamma->0 if a_i stays bounded below.
It still diverges when a_i approaches0, which is the genuine typing-edge
loss. No uniform statement across that boundary is asserted.

Applying Theorem1 at k=1 gives the explicit sufficient quantities

    epsilon0=(167/192)N r w^4,
    epsilon2=(115/48)N r w^2.                          (W17)

In particular this Hessian transfer uses the smaller w^2 factor, not the
value-error w^4 factor. The estimate is deterministic and independent of
any conditioning or weighting convention.

## 3. Precisely conditional geometric application

Suppose a valid QS elder-trap certificate at these parameters supplies its
sets V_eta, E_S and E_M, with their raw images contained in W_w. Retain the
certificate's hypotheses: global continuity, local C2 regularity, exact
pin values and gradients, typing, (H), and the axis in V_eta. Its conclusion
is the maximin identity d_g(M)=-1 under E1/E2/E3. This is an EXPLICIT
IMPORTED IMPLICATION, not an assertion that literal A2 v1 has been accepted.

For the actual raw field F_r and the model P, sufficient conditions for
that implication are

    epsilon0 < eta,
    (2 epsilon2/3)[1+(gamma^2+144)/a_S] <= 2/5,
    (2 epsilon2/3)[1+(gamma^2+144)/a_M] < 1.            (W18)

Theorem1 supplies E1, Theorem2 supplies E2/E3, and(W1) gives the exact
error pins. A torus field lifts continuously to the whole raw plane.
Every path on the torus starting at the chosen M has a lift starting at
that lift of M, and every raw path projects to a torus path, preserving
field values and the endpoint condition f>b. Thus the two maximin values
coincide. Under the imported certificate, (W18) proves

    d_f(M)=b-r^3=f(S).                                (W19)

This is a deterministic sufficient condition. Unique persistence pairing
additionally requires the intended Morse/critical-value convention; it
is not inferred merely from equality of two heights here.

The corrected A2 box, IF supplied as that geometric input, proposes the
explicit choice

    w >= 3/2+(5/2)(|gamma|+12)/sqrt(24 lambda_tilde).

Its correction and acceptance status must be carried when using it. The
derivative estimates (W4), (W16) and (W17) are unconditional within their
own deterministic assumptions and do not await A2 incorporation.

## 4. Boundary of this result

This note gives explicit growing-window constants and precise deterministic
transfer inequalities. It does not supply a probability of (W18), moments
of N under a weighted conditional field law, density or determinant-weight
comparisons, the rejected-side chord window, shrinking multiple-witness
control, an intermediate-separation coarea theorem, or a final persistence
density/remainder. A rho^-6 model-weight tail from corrected A2 cannot be
silently substituted for those missing field estimates. No program-level
status, historical proof bytes, review disposition, CI result or prize gate
is changed by this candidate.
