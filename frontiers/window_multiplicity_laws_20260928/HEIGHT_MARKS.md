# The missing single-witness height mark: uniformity and joint conditional law

Object: OA-WINDOW-MULTIPLICITY-HEIGHT-20260928-v1.
Author: OpenAI / ChatGPT, foreground research session, 28 September 2026.
Disposition: AUTHOR-SIDE COROLLARY; NONAUTHOR ANALYTIC REVIEW REQUIRED.
Scientific effect: NONE. No existing source or scientific disposition changes.

## 1. The premise is pointwise in the height, not only an integrated mean

Use the fixed-remote setting of [RM] and [RC] from SOURCE_MAP.json. The original
endpoint observations, maximum/saddle determinant tilt, full normalizer, fixed
d>=2,L,rho>0, and compact positive gap marks are unchanged. Let E be any
deterministic Borel subset of the same D_rho. Its positive volume may depend on r.
Let N_r count all critical indices in E whose heights are in I_r=(b-k r^3,b).

The remote singleton-law candidate [SL] explicitly discards the height mark.
Its integrated mean formula alone does not determine the height distribution:
equal integrals can belong to different densities. The stronger premise needed
here is already written and proved in **[RM, Section 5, immediately after (13)]**.
In its notation the exact pre-height-integrated density is

    R_{r,j}(x,h)
      = p_{(grad f(x),f(x))|U_r=v_r}(0,h)
        E[W_r F_j(H_x) | U_r=v_r,grad f(x)=0,f(x)=h]/Z_r,

and, uniformly for x in D_rho, h in [b-k r^3,b], j and compact marks/frames,

    |R_{r,j}(x,h)-Lambda_j(x;b,k,u)| <= C r.                (H1)

This is exactly the complete integrand of [RM, (12)] after its r^2/Z_r factor.
The proof retains the **actual additional height pin**, uses a common Gaussian
regression coupling, controls W_r/r^2 under that extra conditioning, and compares
the full normalizer with z_0. No zero mean, independence, or extra endpoint
Jacobian is inserted here.

The weighted Kac-Rice identity is a finite measure identity in location, height
and index. One obtains it first for continuous nonnegative height test functions
by the expected-integral formula, then for bounded Borel test functions by equality
of measures and monotone approximation. Individual endpoint heights have zero
mean count. These facts are already part of [RM]'s height disintegration; the
application does not feed an arbitrary Borel weight directly into a theorem whose
stated hypothesis is lower semicontinuity.

## 2. The rescaled height mean measure

Define the normalized deficit mark

    theta=(b-f(x))/(k r^3), 0<theta<1.

Let Xi_r put one atom (x,j,theta) at every counted critical point, on
S_E=E x {0,...,d} x (0,1). Its total count is still N_r; adding marks has not
created extra points. Changing variables h=b-k r^3 theta gives the exact mean
measure

    mu_r(dx,{j},dtheta)
       =k r^3 R_{r,j}(x,b-k r^3 theta) dx dtheta.           (H2)

The absolute Jacobian is k r^3, not r, r^2, or a pin-frame Jacobian. Equation (H1)
therefore implies the uniform density statement

    | dmu_r/(k r^3 dx dtheta) - Lambda_j(x) | <= C r.       (H3)

Put

    A_E=sum_j integral_E Lambda_j(x) dx,
    pi_E(dx,{j})=Lambda_j(x)dx/A_E,
    mu_{0,r}=k r^3 Lambda_j(x)dx dtheta.

On the fixed compact remote parameter set Lambda_j are continuous, positive and
bounded. Thus for positive-volume E, uniformly over these E,

    c r^3 |E| <= m_r:=E N_r <= C r^3 |E|,
    ||mu_r-mu_{0,r}||_var <= C r^4 |E|,
    dTV(mu_r/m_r, pi_E tensor Uniform(0,1)) <= C r.         (H4)

Probability TV is one half of the full variation norm. To see the normalization
bound directly, for positive measures mu,nu of masses m,n>0,

    ||mu/m-nu/n||_var
       <= (||mu-nu||_var+|m-n|)/m
       <= 2||mu-nu||_var/m.

The factor |E| cancels. A null-volume E has zero count almost surely and no
conditional nonempty or singleton law is asserted there.

## 3. From a mean mark to the actual unique witness

Let q_r=E[N_r(N_r-1)]. The fixed-remote bound [RC, Corollary D] gives

    q_r <= C r^5 |E|, q_r/m_r <= C r^2.                    (H5)

Write sigma_r for the mark submeasure from singleton configurations and eta_r
for the mean mark measure contributed on N_r>=2. Then

    mu_r=sigma_r+eta_r,
    sigma_r(S_E)=p_{1,r}:=P(N_r=1),
    eta_r(S_E)=a_r:=E[N_r;N_r>=2] <= q_r.

For small r, p_{1,r}=m_r-a_r>=m_r-q_r>0. The exact mixture identity

    mu_r/m_r=(p_{1,r}/m_r)(sigma_r/p_{1,r})+eta_r/m_r

gives dTV(sigma_r/p_{1,r},mu_r/m_r)<=a_r/m_r<=C r^2. Combining with (H4) proves:

**Theorem H1 (single-point joint height law).** Uniformly for every deterministic
positive-volume E=E_r inside the same fixed D_rho,

    dTV(Law((x,index,theta) of the unique point | N_r=1),
        pi_E tensor Uniform(0,1)) <= C r.                 (H6)

In particular the deficit height tends to a uniform distribution and is
asymptotically independent of the **joint** location/index mark. No independence
between location and index is claimed.

For completeness the integer inequalities imply

    m_r-P(N_r>=1) <= q_r/2,
    P(N_r>=2 | N_r>=1) <= q_r/(2P(N_r>=1)) <= C r^2.       (H7)

There is also a complete-configuration version: conditioned on nonemptiness,
Law Xi_r differs by at most C r from a singleton with mark law
pi_E tensor Uniform(0,1). Indeed the singleton submeasure sigma_r/m_r is dominated
by both Law(Xi_r | N_r>=1) and a singleton with law mu_r/m_r, and has mass
p_{1,r}/m_r. The resulting TV bound is a_r/m_r, then use (H4). This is a statement
about configuration laws, not an arbitrary rule for choosing a point from a
multiple configuration.

The elementary mixture and common-submeasure arguments are rederived here; [SL]
is credited as the parallel source of the location/index formulation, not silently
consumed as an already independently accepted theorem.

## 4. Why the single and pair height laws differ

The leading single-point mean density has no dependence on theta, so its normalized
height is uniform. In REMOTE_PAIR_LAW.md, the normalized **factorial-pair mean**
instead has density (5/9)|theta-theta'|^(-1/3), with gap Beta(2/3,2). Pair weighting
samples a different object: configurations with more qualifying pairs receive
more weight. There is no contradiction, and the beta law is not the law of two
independent samples from the single-point uniform limit.

There is likewise no global conditional-singleton claim. LOCAL_MULTIPLICITY.md
exhibits a local two-saddle mechanism of probability order r^3 in d=2, the same
order as a global occurrence. The fixed positive spatial exclusion in (H1)-(H7)
is indispensable.

## 5. Scope, tests, and review obligations

The order-Cr bound depends on the fixed d,L,rho and compact b,k ranges of its inputs.
It does not allow rho->0, k->0, increasing dimension/torus size, or a set E chosen
from the realized field. Unlike the sharp remote pair asymptotic, this pointwise
height-kernel argument does permit arbitrary deterministic varying E_r, because
all errors are bounded by its volume before normalization.

These are critical-point height marks within a prescribed between-pin window,
not a persistence-partner distribution or lifetime distribution. No new numerical
value of C or cutoff is supplied. The finite tests verify the Jacobian, the mean
normalization algebra, and the failure of an integrated-mean-only inference.
They do not verify the continuum uniform density estimate (H1); its exact source
and its correct mathematical scope are part of the nonauthor review obligation.
