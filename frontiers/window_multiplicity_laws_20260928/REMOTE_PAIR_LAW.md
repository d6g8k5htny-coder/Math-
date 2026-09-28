# The leading remote factorial-pair measure and its universal height-gap law

Object: OA-WINDOW-MULTIPLICITY-REMOTE-20260928-v1.
Author: OpenAI / ChatGPT, foreground research session, 28 September 2026.
Disposition: AUTHOR-SIDE PROOF CANDIDATE; NONAUTHOR ANALYTIC REVIEW REQUIRED.
Scientific effect: NONE. No old source, review verdict, or governing status is changed.

## 1. Exact setting and count convention

Use the exact field, pins, Q_r, W_r, Z_r and positive compact gap-mark range of
[RM] and [RC] in SOURCE_MAP.json. Dimension d>=2 and torus side L are fixed;
0<rho<L/4 is fixed. M=-(r/2)u is pinned to height b and S=(r/2)u to b-k r^3,
with both gradients zero. W_r=F_d(H_M)F_{d-1}(H_S), where F_j is the absolute
determinant restricted to negative index j and zero on singular matrices. The
law Q_r^W has density W_r/Z_r relative to the original 2(d+1)-observation Gaussian
law Q_r. No adjacency event or further normalizer is inserted.

Fix a deterministic Borel set E of positive volume inside D_rho={dist(x,0)>=rho}.
Let N_j(E) count index-j critical points of height in I_r=(b-k r^3,b), and
N(E)=sum_j N_j(E). Let T_ij(E) count **ordered distinct pairs** (x,x') of indices
i,j, both in E and with both heights in I_r. Thus T_ii=N_i(N_i-1), T_ij=N_iN_j
for i!=j, and sum_ij T_ij=N(N-1).

[RC] gives E_Qr^W T_ij(E)<=C r^5 |E|. This note proposes the leading coefficient,
its index support, and a normalized **factorial-pair mean** height law. It does
not infer a pair-occurrence probability asymptotic from a factorial expectation.

## 2. Contact coefficient

Let U_0=v_0 be the endpoint contact observations from [RM, (4)]: in the pin frame,

    U_0=(f,f_x,f_xx,f_xxx,f_yj,f_xyj) at 0,
    v_0=(b,0,0,12k,0,...,0), Q_0=Law(f | U_0=v_0).

Let B_0 be the transverse Hessian at 0 on u-perp, and define

    w_0=(6k)^2 (det B_0)^2 1{B_0<0}, z_0=E_Q0 w_0>0.

For x in D_rho and unit e, put

    Y_{x,e}=(grad f(x), H_x e, f(x)),
    T=D^3 f(x)[e,e,e], A=H_x restricted to e-perp.           (R1)

Use the conditional Gaussian density p_{Y|Q0} at (0,0,b), and keep all dependence
between B_0, A and T inside conditional expectations. Define chi_ij(A,T) as follows,
where a is the negative index of a nonsingular A:

    T>0: chi_ij=1 iff (i,j)=(a+1,a);
    T<0: chi_ij=1 iff (i,j)=(a,a+1);
    T=0 or det A=0: chi_ij=0.                              (R2)

The values on singular A and T=0 do not affect the following product. With ordinary
unnormalized surface measure de on S^{d-1}, define

    K_ij(x;b,k,u)
      = (3/40) 12^(2/3) k^(5/3) / z_0
        * integral_S p_{Y|Q0}(0,0,b)
          E_Q0[w_0 |T|^(4/3) (det A)^2 chi_ij(A,T)
               | Y_{x,e}=(0,0,b)] de.                     (R3)

Choice of an orthonormal basis of e-perp or u-perp has no effect on determinants,
indices, or this expectation. Local orthonormal frames suffice; no global frame
section over the sphere is assumed.

**Theorem R.** For every fixed E as above,

    E_Qr^W T_ij(E) = r^5 integral_E K_ij(x) dx + o(r^5).     (R4)

The coefficient is continuous and finite on the fixed compact parameter ranges.
It is strictly positive for adjacent indices |i-j|=1, and identically zero for
all other index pairs. Moreover K_ij=K_ji after integration in e. Consequently

    E_Qr^W[N(E)(N(E)-1)] ~ r^5 integral_E sum_ij K_ij > 0,
    E_Qr^W[N_j(E)(N_j(E)-1)] = o(r^5).                     (R5)

These are fixed-domain qualitative asymptotics; no numerical remainder or rate
for the little-o is asserted. The convergence can be taken uniform in the fixed
compact mark/frame ranges for a given fixed E. It is **not** asserted uniform over
arbitrary r-dependent oscillatory sets E_r. Null-volume E has zero counts by [RM].

## 3. The conditional collision frame and its actual coupling

For x'=x+delta e, 0<delta<eta_0<=rho/2, use the exact frame of [RC]:

    V_delta=(grad f(x), (grad f(x')-grad f(x))/delta, f(x),
        [f(x')-f(x)-(delta/2)e.(grad f(x)+grad f(x'))]/delta^3).

At delta=0 its continuous extension is

    V_0=(grad f(x), H_xe, f(x), -T/12).                    (R6)

[RC, Lemma 1] gives a covariance sandwich through r=delta=0 for the joint
observations (U_r,V_delta), and [RC, Lemma 2] bounds conditional field-norm moments
by a polynomial in the last target t, with rapidly decaying target density.
The same argument supplies every fixed C^q moment, not just C^3: the periodized
Fourier series has summable square-root spectral weights with arbitrary polynomial
factors, and cross-covariance derivatives against these observation averages are
uniformly bounded.

For precision the needed convergence is not assumed just from separate marginal
convergence. On one unconditioned smooth field F, regress on O_{r,delta}=(U_r,V_delta):

    F^{r,delta}(z)=F(z)+Cov(F(z),O_{r,delta})Cov(O_{r,delta})^{-1}
                             (a_{r,delta}-O_{r,delta}),
    a_{r,delta}=(v_r,0,0,y,t).

Ur is an invertible re-expression of the original pins for r>0. All frame entries
are point evaluations or integral derivative averages; covariance and derivative
cross-covariances extend continuously to r=delta=0. The positive joint covariance
floor persists there. Therefore, as r,delta->0 and y->b, this representation
converges in every fixed L^p(C^q), uniformly on compact x,e,frame,mark,t sets, to
the corresponding regression on (U_0,V_0)=(v_0,0,0,b,t). The density of V_delta
under Q_r converges on the same bounded target sets to the density of V_0 under
Q_0. The Gaussian conditional means need not be zero.

At the limit, T=-12t. Away from the origin the derivative orders 0,1,2,3 in
(U_0,V_0) are independent linear functionals. The order-two block H->He is onto.
Adding the independent entries of B_0 and A completes the Hessian entries at their
respective sites. Positive Fourier weights then give full conditional support for
(B_0,A,T) given (U_0,Y), using the distributional jet-independence argument of [RM].
This also proves the uniform conditional moment bounds used with (R3).

## 4. Two determinant limits without inverse Hessians

Under the exact pair-gradient conditions, Taylor's integral identity gives

    H_x e / delta = -(1/2) D^3 f(x)[e,e,.] + O(delta ||f||C4),
    H_x' e / delta = +(1/2) D^3 f(x)[e,e,.] + O(delta ||f||C4). (R7)

Indeed integrate the gradient difference over the segment and expand its Hessian
once. The second identity follows from the other endpoint. The C^4 control is
valid under the extra observations by Section 3. In a frame beginning with e,
congruence by diag(delta^(-1/2),I) gives limits

    K_x -> diag(-T/2,A), K_x' -> diag(T/2,A).

The off-diagonal scaled entries are O(sqrt(delta)||f||C3); the lower-right entries
converge to A. Congruence preserves inertia and changes determinant by delta^{-1}.
For each j, the function F_j is continuous even on singular matrices, with the
polynomial Lipschitz bound established in [RM, (8)]. Hence under the coupled
conditional fields,

    F_i(H_x)/delta -> F_i(diag(-T/2,A)),
    F_j(H_x')/delta -> F_j(diag(T/2,A))                     (R8)

in L^p for each finite p on bounded target sets. This avoids a division by det A,
a lower eigenvalue assumption, or a discontinuous type-indicator limit.

The same exact pin identities as [RM, Section 4], now under this additional
conditioning, give W_r/r^2 -> w_0 in L^p. The full endpoint-only normalizer is
Z_r/r^2 -> z_0; it is not changed to a pair-conditioned normalizer. The product
limit in (R8) is

    (T^2/4)(det A)^2 chi_ij(A,T).

Thus it vanishes at leading order unless the two indices are adjacent. Same-index
pairs are not impossible at positive delta: for example, with a nonzero mixed
third derivative and T=0, a cubic can give two saddle determinants of order delta^2
rather than delta. The finite negative control records this distinction.

## 5. Blow-up delta=r s, dominated convergence, and the coefficient

Apply the already justified marked pair Kac-Rice formula [RC, (3.1)] under the
Gaussian Q_r, using W_r once and each witness determinant once, then divide by
Z_r once. Polar coordinates contribute delta^{d-1}; the joint value-gradient
change of variables contributes delta^{-d-3}. With

    y=b-r^3 z, delta=r s, t=(y'-y)/delta^3,

we have dy'=delta^3 dt. The two windows are exactly

    0<z<k, (z-k)/s^3 < t < z/s^3.                        (R9)

Pulling out r^5 leaves s ds dz dt times the target density and the conditional
expectation of (W_r/r^2)(F_i(H_x)/delta)(F_j(H_x')/delta), divided by Z_r/r^2.
There is no leftover dimension-dependent radial power:

    (d-1) - (d+3) + 3 + 2 = 1.

At finite t the limit conditional determinant product is 36t^2(det A)^2 chi_ij,
because T=-12t. The pathwise estimates W_r<=r^2 K^{2d} and
|det H_x det H_x'|<=delta^2 K^{2d}/4, together with the conditional Gaussian
moment/density bounds, dominate the nonnegative integrand by

    C s (1+|t|)^(-p) 1{(R9)},

for p chosen large enough. Integrating z and t bounds this by
C s min(1,s^{-3}), uniformly in r and all other compact parameters. This is
integrable on (0,infinity). The constants absorb the fixed positive k bounds.
The s-domain delta<eta_0 becomes s<eta_0/r; zero-extension outside this interval
has the same envelope. Therefore dominated convergence applies.

The spatial factor is 1_E(x)1_E(x+rse), not just 1_E(x). For a general fixed Borel
E, a pointwise boundary argument is invalid. Instead use continuity of translations
in L^1 on the torus:

    sup_{|h|<=epsilon} ||1_E(.+h)-1_E||_1 -> 0.

On bounded s,t regions the remaining density is uniformly bounded. The displayed
translation estimate removes the second indicator in L^1; the integrable envelope
controls the tails. This proves the same limit for every fixed Borel E without
assuming a smooth boundary. It does not supply a uniform estimate for arbitrary
oscillating E_r, which is why that extension is excluded in Theorem R.

Integrating z in (R9) gives (k-s^3|t|)_+. For t!=0,

    integral_0^infinity s(k-s^3|t|)_+ ds
       =(3/10) k^(5/3)|t|^(-2/3).                       (R10)

Multiply by 36t^2. Integrating the last observation and converting T=-12t to its
conditional Gaussian distribution yields

    (54/5) k^(5/3) E[|T/12|^(4/3) ... |Y]
       =(3/40)12^(2/3)k^(5/3) E[|T|^(4/3) ... |Y].        (R11)

This is exactly (R3), including the surface-measure and ordered-pair conventions.
One may first restrict |t|>epsilon, apply Tonelli to nonnegative functions, and
then let epsilon decrease to zero. The resulting |T|^(4/3) moment is finite;
t=0 is a Lebesgue-null exceptional target. No cancellation of an undefined
zero-times-infinity value is required.

Separated pairs delta>=eta_0 contribute O(r^6)|E|^2 by [RC, Lemma 5] and are
negligible after division by r^5. This proves (R4).

Full conditional Gaussian support makes the integrand positive on an open set
B_0<0, A of any chosen index a, and T of either chosen nonzero sign. Therefore
K_ij>0 precisely for adjacent indices. Continuity follows from regression and
polynomial domination. The weighted indicator is continuous at every possible
index boundary because det A or T vanishes there. Compactness gives finite upper
bounds and positive lower bounds for each adjacent coefficient. The substitution
e->-e flips T, preserves A and w_0, and changes H e only by a sign at its zero
target; it exchanges i and j without a density Jacobian. This proves symmetry
and (R5). For unordered total pairs, divide the total coefficient by two.

## 6. Universal height marks under the factorial-pair mean

For each counted critical point define its normalized height deficit

    theta(x)=(b-f(x))/(k r^3) in (0,1).

Define a probability measure on (0,1)^2 by normalizing the **expected ordered-pair
count measure**:

    Pi_r(C)= E_Qr^W sum_{x!=x' counted in E}
                      1{(theta(x),theta(x')) in C}
                 / E_Qr^W[N(E)(N(E)-1)].                 (R12)

This is a factorial-moment normalization, sometimes called pair weighting. It is
not the law obtained by first conditioning on N>=2 and then choosing a pair
uniformly from that realized configuration. Those two sampling procedures need
not agree when configurations have different multiplicities.

**Theorem H2.** In probability total variation (one half of the full signed
variation norm), Pi_r converges to the density

    h(a,b)=(5/9)|a-b|^(-1/3), 0<a,b<1.                  (R13)

No convergence rate is supplied. For an ordered adjacent index pair i=j+1, the
corresponding normalized pair mean has density
(10/9)(b-a)^(-1/3) on 0<a<b<1. For i+1=j the triangle is reversed. Nonadjacent
pair means have no positive r^5 coefficient, so no analogous normalization at
that scale is asserted.

**Proof.** The preceding dominated-convergence argument is convergence in L^1 of
the nonnegative blown-up pair densities (including the spatial indicators), not
merely convergence of their total masses. The map to the two deficits is now
independent of r:

    theta=z/k, theta'=z/k-s^3 t/k.

The total-variation norm cannot increase under a measurable pushforward. At the
limit condition on a nonzero T=-12t, the remaining contact jets, x and e. Put

    g=s^3 |T|/(12k)=|theta'-theta|.

Then s ds=(1/3)(12k/|T|)^(2/3)g^(-1/3)dg and dz=k dtheta. The contact factor is
independent of theta and g. The allowed theta interval has length 1-g. Each sign
of T consequently gives a normalized triangular density proportional to g^(-1/3),
whose integral is

    integral_0^1 g^(-1/3)(1-g) dg = 9/10.

The e->-e symmetry gives equal total mass to the two triangles. This proves (R13)
and its index-resolved version. The separated-pair mass is o(r^5), so it does not
change the normalized limit. Notice that the argument pushes forward to HEIGHT
marks: it does not claim total-variation convergence of unscaled distinct spatial
pairs to a measure supported on the spatial diagonal, which would be impossible.

The gap g=|a-b| therefore has the **Beta(2/3,2)** density and CDF

    f_gap(g)=(10/9)g^(-1/3)(1-g),
    F_gap(g)=(5/3)g^(2/3)-(2/3)g^(5/3), 0<=g<=1.          (R14)

Given g, the smaller deficit is uniform on (0,1-g). Useful exact consequences are

    E[g^n]=10/((3n+2)(3n+5)), n=0,1,...,
    E[g]=1/4, E[g^2]=5/44, Var(g)=9/176;
    E[a]=E[b]=1/2, E[a^2]=29/88, E[ab]=3/11,
    Corr(a,b)=2/7.                                      (R15)

The marginal pair-weighted deficit density is
(5/6)(a^(2/3)+(1-a)^(2/3)), not uniform. For comparison, two independent uniform
heights would have mean absolute difference 1/3 rather than 1/4. None of these
pair-weighted assertions is a persistence-lifetime law.

## 7. Explicit limits of the result

The coefficient in (R3) is a Gaussian conditional integral, not a numerical
enclosure. Positivity and the r^5 order do not by themselves prove
Q_r^W(N>=2)~(r^5/2) integral sum K: triples or higher multiplicities would require
additional estimates. A finite probability-law counterexample in the tests
exhibits a factorial moment asymptotic of order r^5 with much smaller event
probability. No third factorial moment or event-conditioned pair-gap law is claimed.

The spatial exclusion remains fixed. The local theorem in LOCAL_MULTIPLICITY.md
shows that global multiple occurrences have order r^3 in d=2, so neither (R4) nor
(R13) is silently extended to pairs near the pins. Other exclusions are changing
L or d, k->0, random field-selected E, arbitrary oscillating E_r for the sharp
asymptotic, all-height counts, elder pairing and governing-status transitions.

The new obligations are the extra-conditioned determinant limits, L^1 domination
through the collision, the fixed-Borel translation step, the coefficient constants,
and the factorial-mean interpretation of the beta law. Finite exact controls test
algebra, not those continuum arguments. Literature context and the limits of the
reconnaissance are recorded separately; no historical-priority claim is made.
