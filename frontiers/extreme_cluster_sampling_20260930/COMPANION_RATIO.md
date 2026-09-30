# Addendum: an explicit unit-square law for the whole extreme doublet

Object: OA-EXTREME-CLUSTER-SAMPLING-20260930-D1.
Author: OpenAI / GPT-6 Astra Pro. New conditional derivation; nonauthor review OPEN.
Scientific effect NONE. PROOF.md remains byte-identical. This addendum consumes
that manuscript's E12-E19/E29 as candidate inputs; their review is not inferred
from finite tests. It introduces no additional Gaussian source assumption.

## 1. The law and its exact domain

Consider the limiting ordinary extreme cluster of PROOF Theorem2, conditioned
on being a doublet. Its outer-root shape has density Q/J on S2_outer, with
J=1083417/280. Write p=-u, A=12p^2-3 and ell=v/A. Define

  rho=|Z_companion/Z_outer| in (0,1),
  w=2ell,
  z=(1+rho)(w-1)/(2rho).                                  (D1)

The map is a smooth bijection, up to the boundary null sets already stated in
PROOF, between S2_outer and the OPEN UNIT SQUARE 0<rho<1,0<z<1. In these coordinates
its unnormalized density, whose integral is J, is

  L(rho,z)=165888 rho z^7(z+1)^4
        *(rho*z+1)^4(rho*z+rho+1)^7
        /[(rho+1)^5(2rho*z+rho+1)^9].                      (D2)

Consequently L/J is the exact universal joint density of the companion/maximum
radius ratio rho and the shape coordinate z under the already-formed limiting
EXTREME DOUBLE-CLUSTER law. It is not the law of a uniformly chosen extra point,
a finite-r Gaussian sample, or a remote singleton.

The downward heights of the maximum anchor and companion respectively are

  eta_out=z^2(rho*z+1)(rho*z+2rho+1)
                       /[(rho+1)(2rho*z+rho+1)],
  eta_in=rho^3 z^2(z+1)(rho*z+rho+2)
                       /[(rho+1)(2rho*z+rho+1)].          (D3)

They satisfy 0<eta_in<eta_out<1 on the square. In fact direct subtraction gives

  eta_out-eta_in=z^2(1-rho)(rho*z+rho+1)^2/(2rho*z+rho+1),
  1-eta_out=(1-z^2)(rho*z+rho+1)^2
                                  /[(rho+1)(2rho*z+rho+1)].

Both are manifestly positive in the open square. The overall Pareto(11) maximum
scale and the cusp orientation/parameter law remain independent of (rho,z),
by PROOF E29. To reconstruct both marked positions use PROOF E30 and these heights.

## 2. Derivation of the bijection and density

For an outer root its companion has u_c=-p_c, t_c=-rho. The two invariants in
E13 and the stationary line give

  4p_c^2-1=rho^2(4p^2-1),
  ell=(p_c+rho*p)/(1+rho).

Thus with w=2ell,

  p=[(1+rho)w^2-(1-rho)]/(4rho*w),
  p_c=[(1+rho)w^2+(1-rho)]/(4w).                          (D4)

The outer condition is p>p_c, equivalent to w>1 for 0<rho<1. The height formulas
before replacing w are

  eta_out=(w-1)^2(rho*w-rho+w+1)(rho*w+3rho+w+1)
                                             /(16rho^2 w),
  eta_in=(w-1)^2(rho*w+rho+w-1)(rho*w+rho+w+3)/(16w),
  1-eta_out=-(w+1)^2(rho*w-3rho+w-1)(rho*w+rho+w-1)
                                             /(16rho^2 w).  (D5)

All positive factors displayed are strictly positive for w>1,0<rho<1. Hence
eta_out<1 is precisely

  1<w<(1+3rho)/(1+rho).

On this interval the companion is also in the strict window: eta_in>0 directly,
and eta_in<eta_out by E17 (or by subtracting D5). This proves both directions
of the bijection D1. No root or type constraint is silently dropped.

The shape change (p,ell)->(u,v)=(-p,A ell) has absolute Jacobian A. At fixed w,

  |partial p/partial rho|/2=(w^2-1)/(8rho^2 w).

Together with Q=A^3(4ell^2-1)(4p ell-1), the density in (rho,w) is

  81(1+rho)(w-1)^7(w+1)^7
    *(rho*w-rho+w+1)^4(rho*w+rho+w-1)^4
    /(4096rho^11 w^9).                                   (D6)

Insert w=1+2rho*z/(1+rho) and its Jacobian2rho/(1+rho) to obtain D2. These
identities can be checked by direct substitution; test_ratio_law.py also uses
independent exact two-variable differentiation of the inverse map to check
L=Q|det d(u,v)/d(rho,z)| on72 rational interior cases. Integration of D2 is J
because this is a bijective change of variables from the source outer sector,
not because of numerical normalization.

## 3. A new small-companion asymptotic

Let f_rho be the marginal density of rho under the doublet law. Set

  H0=integral_0^1 z^7(z+1)^4 dz=6401/3960,
  Csmall=82944 H0/J=137647104/3972529.                      (D7)

The rational factor multiplying165888 rho z^7(z+1)^4 in D2 tends uniformly
to1 as rho->0. Its denominator is bounded away from zero on the closed square.
Therefore

  f_rho(rho) ~ (275294208/3972529) rho,
  P(rho<epsilon | limiting extreme doublet)
                     ~ Csmall epsilon^2.                 (D8)

This is a further limit INSIDE the already-formed extreme-doublet law: the order
is r->0, then the microscopic extreme threshold->infinity, then epsilon->0.
It is not a uniform triple-scale assertion for the original field.

More precisely, conditional on rho<epsilon, (rho/epsilon,z) converges weakly to
independent variables Qsmall,Zsmall with densities

  2q dq, 0<q<1;
  z^7(z+1)^4/H0 dz, 0<z<1.                               (D9)

Indeed substitute rho=epsilon q in D2 and divide by D8. Uniform convergence of
the bounded rational factor proves convergence of the densities in L1; thus D9
is even total variation on these FIXED scalar-coordinate spaces. This is not a
transfer of total variation through an epsilon-dependent spatial root map.

By direct uniform limits of D3,

  eta_out -> Zsmall^2,
  eta_in/rho^3 -> 2 Zsmall^2(Zsmall+1).                    (D10)

Equivalently eta_in/epsilon^3 has limit2 Qsmall^3 Zsmall^2(Zsmall+1). The small
companion thus approaches the upper height boundary with a CUBIC radius-ratio
scale while the outer height remains nonzero. This describes normalized height
marks, not an elder-pairing or actual finite-r persistence-lifetime theorem.

The limiting outer-height density in D10 is particularly simple:

  e^3(1+sqrt(e))^4/(2H0), 0<e<1,
  E[e]=483876/582491.                                     (D11)

It follows by e=z^2 and termwise polynomial integration. No model-dependent
Gaussian integral remains in D7-D11.

At the other endpoint, rho->1-, continuity of D2 and integration on the bounded
z interval give

  f_rho(1-)=857223/2889112-(945/361139)log2.                (D12)

For verification L(1,z)=81 z^7(z+2)^7/[8(z+1)]. Put x=z+1 and expand
(x^2-1)^7/x on[1,2]: its integral is2571669/2240-(81/8)log2. Dividing by J
gives D12. The equal-radius boundary itself still has probability zero.

## 4. A rejection sampler with a certified ideal-real acceptance rate

Define

  a(rho,z)=(rho*z+1)^4(rho*z+rho+1)^7
                   /[(rho+1)^5(2rho*z+rho+1)^9].          (D13)

It satisfies0<a<=1 on the square. Indeed rho*z+1<=rho+1 and
rho*z+rho+1<=2rho*z+rho+1, so

  a<=1/[(rho+1)(2rho*z+rho+1)^2]<=1.

Use the proposal density

  q0(rho,z)=2rho z^7(z+1)^4/H0.                            (D14)

It is a product distribution: draw rho=sqrt(U) for uniform U in(0,1); independently
choose j in{0,...,4} with probabilities C(4,j)/[(8+j)H0], and draw z=V^(1/(8+j))
for independent uniform V. The five integer mixture weights are

  (495,1760,2376,1440,330), with sum6401.

Accept with probability a(rho,z), otherwise repeat with independent proposals.
Since q0*a=L/(82944 H0), the accepted law is exactly L/J in an IDEAL REAL
uniform-random model. Its exact acceptance probability and mean proposal count are

  p_accept=J/(82944H0)=3972529/137647104,
  E[proposals]=137647104/3972529.                          (D15)

Thus the same number Csmall in the small-ratio CDF is the ideal sampler's expected
proposal count. This is an identity of the explicit integrals, not an empirical
performance estimate.

ratio_law.sample_doublet implements the algorithm using Python's ordinary
floating-point pseudorandom numbers, with reproducible seeding, open-interval
checks and a bounded trial budget. It returns rho,z and both height marks only;
it does not simulate the Gaussian cusp parameters, spatial direction, Pareto
maximum scale or the original field. Numerical roundoff is NOT interval-enclosed
and the simulator is not an exact-real sampler. Its tests check reproducibility,
ranges, rejection limits and exact underlying algebra, not distributional accuracy
of floating-point draws.

Example:

    import random
    from ratio_law import sample_doublet
    marks = sample_doublet(random.Random(20260930))

## 5. Separate review boundary

Requested Slice D: the square bijection and Jacobian D1-D6; both normalized
height formulas and ordering; density/CDF small-ratio constants, the further
conditional law and order of limits D7-D12; the proposal/envelope and ideal-real
acceptance probability D13-D15. These consume the main manuscript's new results
conditionally; an acceptance of this algebra alone would not accept PROOF's
Gaussian limit. The16 new test methods are finite evidence, not analytic review.
No original PROOF.md, extremes.py, source pin, or prior review byte is amended.

## 6. Exact falsifier against a finite-scale interpretation

A supporting author-exposed recovery lane supplied PR169 comment5902401772;
the values below were independently recomputed here with Fraction arithmetic.
This is an exact negative example, not an additional analytic acceptance.

Take k=1,a=-12,s=-14/5,beta=33/4,c=-31/40, and the root shape
u=-3/4,v=14/5,Z=1. The companion is

  u_c=-20907/28124, v_c=670215854/247174805, Z_c=-6919/7031.

Both are typed strict-window saddles. Nevertheless, with the actual unsheared
coordinates X=u-aZ/(12k),

  R_seed^2=17/16,
  R_companion^2=3126268865/790959376,
  eta_seed=13/60, eta_companion=618523783/2966097660.

Although |Z_c|<|Z|, the companion has GREATER physical radius and SMALLER downward
height. Thus finite-scale physical ordering is not the |Z| ordering, and the
farther-is-deeper statement is not an assertion at every finite radius. The
maximum selector in PROOF Section5 is the actual physical selector before the
limit; the limiting ordering and this addendum concern the second, already-formed
extreme law. The new exact regression pins this distinction without changing
any original proof bytes.
