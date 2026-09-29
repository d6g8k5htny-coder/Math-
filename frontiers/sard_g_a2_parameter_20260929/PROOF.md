# SARD-G A2 parameter-regularity interface

Object: OA-SARD-A2-PARAMETER-20260929-v1.  
Author: OpenAI / ChatGPT.  
Disposition: AUTHOR-SIDE DOWNSTREAM CANDIDATE; nonauthor analytic review required.  
Scientific effect: NONE.

## 1. Exact interface

Let X=C^2(T_L^2) and V_f=grad f, viewed as a C^1 vector field. Fix f0 and a
nondegenerate index-one critical point p0. After shrinking an X-neighborhood U
of f0 and a coordinate ball B about p0, the following are the A2-T/A2-D claims
consumed by Math-#135.

**A2.1 tracked saddle.** There is a unique map p:U->B with V_f(p(f))=0. It is
C^1 as a map from the Banach space X to R^2. Its derivative is
Dp(f)[h]=-H_f(p(f))^{-1} grad h(p(f)).

**A2.2 local branch germs.** After choosing one stable/unstable eigendirection
and its sign at f0, there are fixed compact graph-parameter intervals and maps
Gamma_f^sigma on them whose images are the four labelled local invariant
half-branches. The map f -> Gamma_f^sigma is continuous U->C^1, and C^1 after
possibly shrinking U. The graph parameter, not physical flow time at p(f), is
used at the stationary endpoint.

**A2.3 local-section launch.** If a fixed finite section is transverse to the
chosen germ at an interior point, its first robust closed-section hit, under the
R1 hypotheses of #135, depends continuously on f; under A2.2 C^1 dependence it
is C^1 by the scalar implicit-function theorem.

**A2.4 regular finite flow.** Let z(f) be such a C^1 launch point and suppose a
compact finite trajectory segment stays in a coordinate region on which
|V_f|>=eta>0. For every fixed finite time horizon before leaving that region,
Phi_f^t(z(f)) is C^1 jointly in (f,t). Its field derivative u=D_f Phi_f^t(z)[h]
satisfies the variational equation
    u'=H_f(Phi_f^t)u + grad h(Phi_f^t),
with the corresponding initial derivative. Consequently any transverse robust
first hit along this finite segment is C^1 in f.

These statements are local. They do not prove A3-A4, Gaussian genericity,
global connection absence, or any C103 estimate.

## 2. Why C2 is the right field topology

The linear map f -> V_f=grad f is bounded C^2->C^1. Evaluation
(f,x)->V_f(x) is C^1 from X x T^2 to R^2: its field derivative is grad h(x)
and its spatial derivative is H_f(x), continuous because f is C^2. Therefore
the Banach implicit-function theorem proves A2.1 directly.

For finite regular flow, write the integral equation
    x(t)=z + integral_0^t V_f(x(s)) ds.
On a compact coordinate region, V_f and D_x V_f are uniformly bounded and
continuous in f in the C^1 norm. Standard contraction on short time slabs gives
existence and continuous dependence. Differentiate the fixed-point equation in
the Banach parameter f. The derivative is the unique solution of the displayed
linear variational equation. Concatenating finitely many slabs proves A2.4 on a
fixed finite horizon. No derivative of H_f is used; C^2 field regularity is
therefore sufficient for this finite-flow part.

## 3. Local invariant graph by a parameter-dependent contraction

Translate p(f) to zero and use a continuously chosen orthonormal eigenframe of
the symmetric Hessian H_f(p(f)); the simple positive/negative eigenvalues remain
separated after shrinking U. In coordinates (x,y), write
    V_f(x,y)=(lambda_f x, -mu_f y)+N_f(x,y),
where lambda_f,mu_f>=lambda_*>0 and N_f(0)=DN_f(0)=0. The map
f -> (lambda_f,mu_f,N_f) is C^1 into the natural C^1 coefficient space: the
eigenvalues/eigenprojections of a simple symmetric 2x2 matrix are C^1, and the
coordinate change and p(f) are C^1.

Choose a small radius so sup ||DN_f|| is uniformly below a fixed fraction of
lambda_*. The usual graph transform on C^1 graphs y=g(x), g(0)=g'(0)=0, is then
a uniform contraction on a closed C^1 ball. Importantly, its contraction
constant is <1 uniformly in f. The transform is C^1 in (f,g): it is assembled
from V_f, finite local flow, coordinate projections and inverses whose
derivatives stay uniformly nonzero on this small ball.

The fixed point g_f therefore depends C^1 on f. A direct proof avoids importing
a differentiable fixed-point theorem: from g_f=T(f,g_f),
    [g_{f+h}-g_f]/||h||
is Cauchy because the difference quotient equals the parameter difference
quotient of T plus a contraction applied to the graph difference quotient.
Taking the limit gives
    Dg_f[h]=(I-D_g T(f,g_f))^{-1} D_f T(f,g_f)[h],
where the inverse is the convergent Neumann series since ||D_gT||<1.
Continuity of these derivatives follows from continuity of DT and the same
uniform contraction bound. The unstable graph is obtained by applying the same
argument to reversed time. Restricting x to positive or negative compact
subintervals gives the labelled half-branches and proves A2.2.

This argument uses C^1 graph transforms, not a claim that an arbitrary C^1
vector field has C^2 invariant manifolds. The output required downstream is
only a C^1 arc with C^1 dependence on the C^2 field parameter.

## 4. Hitting maps

Let Gamma(f,s) be any local germ or regular-flow arc already proved C^1 in
(f,s), and let a finite section be rho=0 with d rho(Gamma_s) nonzero at the
first robust hit. The R1 geometry in #135 supplies an open neighborhood on
which that zero remains the first closed contact. The Banach scalar IFT gives
a C^1 hit parameter tau(f), with
    D tau(f)[h]= -D_f(rho o Gamma)(f,tau)[h]
                  / partial_s(rho o Gamma)(f,tau).
Composition gives the C^1 hit point. This proves exactly the differential part
of A2-D once R1 supplies the robust first-contact predicate.

## 5. Scope and review target

The only non-elementary local ingredient above is the uniform C^1 graph
transform. A reviewer should check that its chosen graph space and transform
really are C^1 in the Banach parameter when f is only C^2, and that no hidden
third derivative of f is used. The finite-flow argument needs only H_f
continuous; the local invariant graph uses the C^1 vector field V_f and its
C^1 parameter dependence.

No literature priority claim is made. Consensus search was attempted on
2026-09-29 and returned the monthly quota error; no result is fabricated from
that call. This note is intended to discharge the precise imported A2-T/A2-D
interface after independent review, not to promote SARD-G by itself.
