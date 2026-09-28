# Faster within-window height decoupling at fixed remote separation

Object: OA-REMOTE-HEIGHT-DECOUPLING-20260928-v1.
Author: OpenAI / ChatGPT, foreground continuation, 28 September 2026.
Disposition: AUTHOR-SIDE PROOF CANDIDATE; source-bound nonauthor review required.
Scientific effect NONE. No parent source, verdict, graph or scientific status changes.

## 1. Precise improvement and inputs

Use the exact fixed-remote setting of RM and RC in SOURCE_MAP.json: the normalized
periodic Gaussian field on the fixed d-dimensional torus, d>=2, fixed rho>0,
compact birth marks b and gap marks 0<k_-<=k<=k_+, all orthonormal endpoint frames,
original endpoint pins M=-(r/2)u and S=(r/2)u with heights b and b-k r^3 and zero
gradients, Gaussian law Q_r and the SAME full endpoint determinant tilt W_r/Z_r.
Here W_r=F_d(H_M)F_(d-1)(H_S). Put l=k r^3 and I_r=(b-l,b).

Let E=E_r be any deterministic positive-volume Borel subset of the SAME fixed
remote domain D_rho. Count all Hessian indices of critical points in E with
heights in I_r; N_r is the count. Let theta=(b-f(x))/l be the normalized deficit,
and put Y=(x,index). Thus theta is in (0,1). Adding marks does not change N_r.

The prior HEIGHT_MARKS candidate establishes O(r) total variation (TV) to the
LIMITING contact location/index profile times Uniform(0,1), by comparing the
full mean density with its contact limit. This note proves a stronger but
DIFFERENT target: comparison to the point's OWN finite-r location/index law.
No change is made to that prior note or to the O(r) rate for the contact profile.

Probability TV is sup_A |P(A)-Q(A)|, half the full variation norm. Write lambda
for Uniform(0,1), mu_r for the expected marked point measure, m_r=E N_r, and
q_r=E[N_r(N_r-1)]. Denote the normalized mean location/index marginal by pi_r.
Let S_r be the joint (Y,theta) law conditioned on N_r=1, and pi_{r,1} its actual
location/index marginal.

**Theorem H.** Uniformly on the above fixed parameter sets and deterministic E_r,
for all sufficiently small r:

    dTV(mu_r/m_r, pi_r tensor lambda) <= C r^3;                       (H1)
    dTV(S_r, pi_{r,1} tensor lambda) <= C r^2;                        (H2)
    dTV(Law(theta | N_r=1), lambda) <= C r^2.                         (H3)

Consequently, for the height H=f(x) of that unique point,

    E[H | N_r=1] = b - k r^3/2 + O(r^5),
    Var(H | N_r=1) = k^2 r^6/12 + O(r^8).                            (H4)

A complete-configuration version, conditioned on N_r>=1, is within O(r^2) of a
single point with location/index law pi_{r,1} and independent uniform theta.
A measurable point-selection rule on nonempty configurations which returns the
unique point when N_r=1 has the same O(r^2) height-uniformity and own-marginal
independence conclusions. This is not an assertion that a finite-r location and
index are mutually independent.

The full joint law compared to the LIMITING contact profile pi_E tensor lambda
remains O(r), as before. The stronger height/decoupling estimates do not supply
a faster location-profile convergence rate or a height law for persistence
partners. No numerical C or cutoff, global/no-rho statement, or optimal Gaussian
rate is claimed.

### Exact imported premises

RM Sections 2-5 supply the uniform positive covariance sandwich for the transformed
pins U_r plus Y_x=(grad f(x),f(x)), all fixed C^q Gaussian regression moments,
the filtered-determinant estimate (8), Z_r/r^2 bounded above and away from zero,
and the full pre-height-integrated density

    R_{r,j}(x,h)=p_{Y_x|U_r=v_r}(0,h)
       E[W_r F_j(H_x)|U_r=v_r,Y_x=(0,h)]/Z_r.                       (H5)

Its pointwise contact comparison and positive contact kernels give

    c r^3 |E| <= m_r <= C r^3 |E|.                                 (H6)

RC Corollary D supplies q_r<=C r^5 |E|. These premises concern the same fixed
remote law and all indices. They are not imported from a global cap event or
from a probability bound in the wrong direction. The new work below is a
same-r comparison in the actual height h, retaining the homogeneous endpoint
constraints so that division by Z_r does not lose r^2.

## 2. Height regression changes along a smooth homogeneous-pin direction

Fix r,x and all endpoint marks/frames. Order V_r=(U_r,grad f(x),f(x)), and let e_h
be the target coordinate vector for its last entry. With one unconditioned field
F, use RM's Gaussian regression realization for each height target h:

    F_h(z)=F(z)+Cov(F(z),V_r) Sigma_r^{-1}(a_h-V_r),
    a_h=(v_r,0,h),   Sigma_r=Cov(V_r).

For h,h' in the closed between-pin interval this gives the exact pathwise identity

    F_h-F_{h'}=(h-h') g_{r,x},
    g_{r,x}(z)=Cov(F(z),V_r) Sigma_r^{-1} e_h.                       (H7)

All fixed derivatives of the cross-covariance in z are uniformly bounded, by
Cauchy-Schwarz and the smooth field's uniform derivative variances. The inverse
covariance is uniformly bounded by RM Section 2. Thus for each fixed q,

    ||g_{r,x}||_{C^q} <= C_q.                                      (H8)

Applying the observation vector V_r to g_{r,x} gives Sigma_r Sigma_r^{-1}e_h=e_h.
Therefore U_r g=0, grad g(x)=0 and g(x)=1. Since the transformed U_r is invertible
as a re-expression of the ORIGINAL endpoint observations for r>0,

    g(M)=g(S)=0,   grad g(M)=grad g(S)=0.                           (H9)

This step uses the same exact pin law, not contact pins substituted at finite r.
The direction is deterministic; the conditioned Gaussian residual is shared.
All field supremum moments are uniform over h,h' by RM's extra-height regression
argument. No independence of endpoint and witness Hessians is asserted.

## 3. The vanishing endpoint columns survive the height comparison

For any smooth g with both gradient pins zero, the average of D^2g u over the
endpoint segment vanishes. At either endpoint i,

    ||D^2g(i)u||
      <= (1/r) integral_0^r t dt * ||D^3g||_infinity
      = (r/2)||D^3g||_infinity.                                   (H10)

For M, subtract D^2g(M+tu)u from D^2g(M)u inside its zero-average integral;
for S reverse the segment. This is a vector integral identity, not an unjustified
simultaneous vector Rolle point.

For each conditioned F_h define its endpoint blocks as in RM Section 4:

    H_i(h)=[[r alpha_i(h), r beta_i(h)^T],
            [r beta_i(h), A_i(h)]],
    K_i(h)=[[alpha_i(h), sqrt(r) beta_i(h)^T],
            [sqrt(r) beta_i(h), A_i(h)]].

Equations (H7)-(H10) give, uniformly in small r,

    |alpha_i(h)-alpha_i(h')|+||beta_i(h)-beta_i(h')||
                              <= C|h-h'|,
    ||A_i(h)-A_i(h')|| <= C|h-h'|,
    ||K_i(h)-K_i(h')||+||H_x(h)-H_x(h')|| <= C|h-h'|.               (H11)

The normalizations alpha=f_uu/r and beta=grad_perp f_u/r therefore do NOT cause
an r^-1 loss. Every matrix in (H11) has moments of all fixed orders uniformly in
h, by the gradient-pin bounds and the extra-conditioned Gaussian moments.

Positive congruence gives exactly, including at singular Hessians,

    W_r(F_h)/r^2 = F_d(K_M(h)) F_(d-1)(K_S(h)).                    (H12)

## 4. Uniform Lipschitz continuity of the full height density

The deterministic estimate in RM (8) is

    |F_j(A)-F_j(B)|
       <= d max(||A||,||B||)^(d-1)||A-B||.                        (H13)

It concerns the determinant TIMES the index indicator, not the indicator alone.
Across index changes the matrix segment reaches determinant zero, so this bound
does not require eigenvalues bounded away from zero.

Apply (H13), (H11), and the product difference identity to the three factors in

    T_h=F_d(K_M(h))F_(d-1)(K_S(h))F_j(H_x(h)).

Hölder and the uniform moments give

    |E T_h-E T_{h'}| <= E|T_h-T_{h'}| <= C|h-h'|,
    sup_h E|T_h| <= C.                                           (H14)

The conditional Gaussian density p_{Y_x|U_r=v_r}(0,h) and its first h derivative
are uniformly bounded on this compact target/covariance domain. Its difference
is at most C|h-h'|. Multiply (H14) by this density and by r^2/Z_r, which is bounded
and does NOT depend on the additional witness height h. Equation (H5) yields

    |R_{r,j}(x,h)-R_{r,j}(x,h')| <= L |h-h'|                      (H15)

with L uniform over remote x, compact endpoint marks/frames and small r.
This is stronger for within-window variation than comparing each height to the
contact kernel with an O(r) error. No derivative of a discontinuous index
indicator or differentiation under an unbounded expectation is being used.

## 5. Exact finite-r mean decoupling and its third-order rate

The finite measure form of weighted Kac-Rice in RM gives, after h=b-l theta,

    mu_r(dx,{j},dtheta)=l R_{r,j}(x,b-l theta) dx dtheta.            (H16)

Write Rbar_{r,j}(x)=integral_0^1 R_{r,j}(x,b-l t)dt. The location/index marginal
of mu_r has density l Rbar. By (H15),

    integral_0^1 |R(x,b-l theta)-Rbar(x)| dtheta
       <= L l integral_0^1 integral_0^1 |theta-t| dt dtheta
       = L l/3.

Sum over the d+1 indices and integrate over E. The FULL variation estimate is

    ||mu_r - mu_r^Y tensor lambda||_var
       <= (d+1)L l^2 |E|/3 <= C r^6 |E|.                          (H17)

Both measures have the SAME mass m_r. Divide by 2m_r and use (H6), obtaining (H1).
Unlike a comparison with the limiting contact profile, there is no normalization
error between two different total masses. The volume factor cancels even when
E_r varies and tends to zero in volume. A zero-volume E has no conditional law
and is explicitly excluded.

## 6. Conditional singleton law and physical-height moments

Let sigma be the expected marked measure restricted to N_r=1, of mass p_1.
Let eta be the mean marked measure on N_r>=2, of mass a=E[N_r;N_r>=2]. Then

    mu_r=sigma+eta,    m_r=p_1+a,    a<=q_r.                       (H18)

For small r, p_1>=m_r-q_r>0. The mixture identity implies

    dTV(S_r, mu_r/m_r) <= a/m_r,   S_r=sigma/p_1.                 (H19)

Marginal contraction gives dTV(pi_{r,1},pi_r)<=a/m_r. Tensoring with a fixed
probability measure preserves TV. The triangle inequality and (H1) therefore give

    dTV(S_r,pi_{r,1} tensor lambda) <= 2a/m_r+C r^3 <= C r^2.

For the height marginal alone, compare first with mu_r/m_r and then with pi_r
tensor lambda. Its bound is a/m_r+C r^3, again O(r^2). This proves (H2)-(H3).
The factor two in the joint own-marginal comparison is kept, not silently removed.

Since 0<=theta<=1, TV controls its first two moments:
E theta=1/2+O(r^2), E theta^2=1/3+O(r^2), Var theta=1/12+O(r^2).
Using H=b-l theta and l=k r^3 proves (H4), with uniform compact-k constants.

Bonferroni and the factorial bound give

    P(N_r>=1)>=m_r-q_r/2,
    epsilon_r:=P(N_r>=2 | N_r>=1)<=q_r/(2m_r-q_r)=O(r^2).          (H20)

The nonempty configuration law is a mixture of its singleton part and a
multiple-configuration part with mass epsilon_r. Its TV distance from the
singleton law S_r, embedded into configurations, is exactly epsilon_r. Combining
with (H2) proves the complete-configuration assertion.

Any measurable rule selecting one actual point from a nonempty configuration
agrees with S_r on N_r=1, hence its selected-mark law differs from S_r by at most
epsilon_r. Applying marginal contraction once more proves O(r^2) decoupling from
its OWN selected location/index marginal, and O(r^2) height uniformity. A rule
may be randomized via a probability kernel; the same mixture argument applies.

## 7. Why this does not improve the contact-profile rate

If pi_E is the limiting contact spatial/index profile, RM gives only
TV(pi_r,pi_E)=O(r). Therefore

    TV(S_r,pi_E tensor lambda) <= O(r^2)+TV(pi_{r,1},pi_E)=O(r).

There is no contradiction with the sharper own-marginal factorization. The old
O(r) comparison can be dominated by spatial/index drift which is common to
all heights and vanishes when that finite-r marginal is retained.

Nor do the moment premises alone permit O(r^3) conditional height error. For a
simple abstract marked process at two distinct locations A,B, choose m=r^3 and
p_2=r^5/2. A two-point configuration occurs with probability p_2 and contains one
point at each location with a common height uniform on (0,1/2). Choose the
singleton submeasure to make the TOTAL mean mark measure exactly m times the
uniform law on {A,B} times Uniform(0,1): its height density summed over locations
is m-4p_2 on (0,1/2) and m on (1/2,1). These are nonnegative for r<=1/2 and have
mass p_1=m-2p_2. Put the remaining probability 1-m+p_2 on the empty configuration.

This process has an exactly height-flat mean and q=2p_2=r^5, but its singleton
height TV from uniform is

    p_2/(m-2p_2)=r^2/[2(1-r^2)].                                 (H21)

It shows the O(r^2) multiplicity correction cannot be eliminated from just these
mean/factorial premises. It is NOT an example of the conditioned Gaussian field
and does not prove that the rate is optimal for that specific field.

## 8. Review and verification boundaries

The new load-bearing analytic step is (H15): the shared regression direction,
homogeneous endpoint constraints, normalized Hessian columns, filtered
polynomial determinant bound, and extra-conditioned moments. The finite tests
check the TV convention, actual finite-r marginal, pair multiplicity weights,
normalizations, the explicit homogeneous-pin polynomial, and the rate-barrier
example. They do not establish a covariance floor, a Gaussian supremum bound,
or Kac-Rice applicability.

This note does not permit rho->0, changing d/L, unbounded birth marks or k->0,
or field-selected random E. It does not imply global uniqueness, change a
persistence-partner definition, or recover/retry the unrelated blocked code in
Math-#116. Authorship/exposure is OpenAI, including the prior remote source;
independent acceptance requires an actual source-bound nonauthor review.
