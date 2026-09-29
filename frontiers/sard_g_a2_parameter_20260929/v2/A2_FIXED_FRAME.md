# A2 at C2: fixed-frame bounded trajectories, not a differentiable C1 graph transform

Object: OA-SARD-A2-FIXED-FRAME-20260929-v2.
Author: OpenAI / ChatGPT. Status: AUTHOR-SIDE SUCCESSOR; nonauthor analytic review required.
Scientific effect NONE. The original #137 manuscript remains a historical,
noncontrolling predecessor; its moving-eigenframe/C1-into-C1 claim is withdrawn.

## 1. The exact target and the false stronger claim

Put X=C^2(T_L^2) with its usual Banach norm, and V_f=grad f. Fix a reference field
f_* in X and a nondegenerate saddle p_*. All assertions are LOCAL on a sufficiently
small X-neighborhood U of f_*. There are four labelled local branch germs, with
fixed compact graph-parameter intervals, for which:

(T) f -> Gamma_f is continuous into C^1 arcs;
(D) (f,s) -> Gamma_f(s) is jointly Frechet C^1 into the surface;
(B) for fixed s, |D_f Gamma_f(s)[h]| <= C ||h||_{C^1}.

Finite regular flow, robust local-section launches, and robust central hits have
the same joint differentiability and local derivative bounds. In particular the
scalar mismatch D_chi is Frechet C^1 on every robust chart from [RC-S], with
|D D_chi(f)[h]| <= C_chi,f ||h||_{C^1}; its derivative is continuous in operator
norm on X*. It therefore also supplies Claude's weaker line form A2-G in [CL].

(D) DOES NOT assert that f -> Gamma_f is differentiable into the C^1 arc norm.
That extra derivative is not needed by the hitting IFT or the Gaussian slicing.
[RC-S] A2-D is read literally as joint C^1 evaluation; graph axes are fixed with
the atlas neighborhood, not recomputed from a moving Hessian. This specifies the
previously ambiguous graph-coordinate sentence without changing the geometry.

The original #137 Section 3 incorrectly claimed that H_f(p(f)), its eigenframe,
and its recentered nonlinearity are C^1 in the necessary strong norms for f in C^2.
They need not be. Here is a concrete counterexample in a coordinate ball, with a
fixed smooth cutoff equal to one near zero:

 f_t(x,y)=(x^2-y^2)/2 +(2/3)xy(x^2+y^2)^(1/4)
                         -t x -(2/3)t|t|^(1/2)y.                (F1)

The homogeneous nonpolynomial term has degree 5/2, is C^2, and its second
derivatives tend to zero at zero. The map t -> f_t is C^1 into C^2. The saddle
p_t=(t,0) has Hessian

 H_{f_t}(p_t)=[[1,sqrt(|t|)],[sqrt(|t|),-1]].                    (F2)

Its positive eigenline has slope

 m(t)=sqrt(|t|)/(1+sqrt(1+|t|)).                               (F3)

For 0<t<=1, m(t)/t>=1/(3 sqrt(t)), so it is not differentiable at zero. A fixed-x
graph of the local unstable manifold, anchored at p_t, has derivative m(t) at its
anchor. Differentiability into C^1 arcs would imply differentiability of that
slope, which is false. Periodization is harmless because all calculations are
inside the cutoff-one ball. This example refutes the old proof's strong regularity,
not the joint C^1 evaluation target (D). No C^3 assumption will be inserted to
hide the issue.

## 2. Tracked saddle and fixed coordinates

The map (f,x) -> grad f(x) is jointly C^1, with

 D[grad f(x)][h,z]=grad h(x)+H_f(x)z.                           (F4)

For example its remainder is bounded by
omega_{H_f}(|z|)|z|+||h||_{C^2}|z|. Continuity of the derivative in operator norm
uses uniform continuity of H_f and
sup_{||h||C2<=1}|grad h(x)-grad h(y)|<=C|x-y|. This agrees with [CL] Lemma J.
The Banach IFT therefore gives the unique nearby saddle p(f), with

 Dp(f)[h]=-H_f(p(f))^{-1} grad h(p(f)).                        (F5)

We USE the derivative of p, but we do NOT differentiate H_f(p(f)). Its continuity
suffices for the local inverse bound. Choose the origin p_* and an orthonormal
eigenframe of H_{f_*}(p_*) ONCE. In these fixed coordinates

 A=diag(lambda,-mu), lambda,mu>0,
 V_f(x)=A x+R_f(x),                                          (F6)

where R_f=V_f-Ax. The saddle p(f) is not translated out of the vector field.
In particular R_f(0) is usually nonzero and must be retained.

## 3. A fixed compact cutoff with a uniformly small Lipschitz constant

Let chi be a fixed smooth cutoff equal to one on the ball B_a and zero outside
B_{2a}, in a coordinate ball contained in the declared endpoint neighborhood.
Set

 N_f(x)=chi(x)(V_f(x)-Ax),                                   (F7)

and extend by zero to R^2. This need not be a gradient vector field outside B_a;
all local trajectories used below remain in B_a, where it is the original field.
The map f -> N_f is affine and bounded C^2->C^1 on this fixed coordinate region.
The functions N_f and DN_f are globally bounded; DN_f is uniformly continuous
for each fixed f. There is no moving cutoff or moving-coordinate derivative.

Given epsilon>0, first choose a small a so ||DV_{f_*}-A||<=epsilon on B_{2a}.
Then ||R_{f_*}(x)||<=epsilon|x| there. If ||f-f_*||C2<=delta,

 ||DN_f||_infinity <= C_chi(epsilon+delta/a+delta),             (F8)

by the product rule. Thus by choosing a and THEN delta sufficiently small,
we may arrange ||DN_f||<=ell with ell as small as desired, uniformly on U.
Also ||N_f(0)||<=C delta. All constants below use an adapted max norm on the
fixed stable/unstable factors; projections have norm one.

Choose beta with 0<beta<lambda (for instance half the smaller spectral gap), and
arrange

 C_0=1/lambda+1/mu,     theta_0=ell C_0<1/4,
 C_beta=1/(lambda-beta)+1/(mu+beta), theta_beta=ell C_beta<1/4. (F9)

No moving eigenvalue occurs in these denominators.

## 4. A genuine C1 contraction on bounded backward trajectories

Let E_0=C_b((-infinity,0],R^2), with the sup norm. It is a Banach space; no
probability law or separability assumption on E_0 is needed. For w in E_0 define

 (Kw)_u(t)=-integral_t^0 exp(lambda(t-s)) w_u(s) ds,
 (Kw)_s(t)= integral_-infinity^t exp(-mu(t-s)) w_s(s) ds.        (F10)

Both integrals converge and ||K||<=C_0. Given the FIXED unstable coordinate a_0 at
time zero, solve

 x=T(f,a_0,x):= (exp(lambda t)a_0,0)+K[N_f(x(.))].             (F11)

T is a contraction in x with norm at most theta_0. It maps E_0 to itself because
N_f is bounded. It has a unique fixed point x_{f,a_0}. Its unstable component at
time zero equals a_0 exactly. Differentiating the two integrals in time verifies
x'=Ax+N_f(x); this uses only continuity of the forcing.

Here the Nemytskii operator (f,x(.))->N_f(x(.)) really IS C^1 into E_0. Its
variation is

 (h,z(.)) -> chi(x(.)) grad h(x(.))+DN_f(x(.))z(.).             (F12)

For the x part, the uniform remainder is at most
omega_{DN_f}(||z||infinity)||z||infinity. The mixed f/x remainder is at most
C||h||C2 ||z||infinity. The parameter derivative is continuous in operator norm
because, uniformly on ||h||C2<=1, chi grad h is Lipschitz; DN_f changes uniformly
under C^2 field changes. A compact fixed cutoff ensures these estimates also
hold for trajectories outside the local ball. Hence T is genuinely C^1 on
U x R x E_0; no spatial derivative of DN_f is differentiated.

Banach IFT applied to x-T(f,a_0,x), or the differentiable-contraction argument,
now proves (f,a_0)->x_{f,a_0} is jointly Frechet C^1 into E_0. Its derivative z
in direction (h,da_0) is the unique bounded solution

 z=(exp(lambda t)da_0,0)
      +K[chi(x(.))grad h(x(.))+DN_f(x(.))z(.)].                (F13)

In particular

 ||z||infinity <= (|da_0|+C_0 C_chi||h||C1)/(1-theta_0).      (F14)

The inverse I-K DN_f is its norm-convergent Neumann series. This is the correct
fixed-point differentiability argument, in a C^0 trajectory norm, replacing the
unproved C^1-graph-transform assertion. The time interval is infinite but the
paths are bounded and DN_f is uniformly continuous, so no exponentially growing
Nemytskii domain is being differentiated.

## 5. Localization, convergence to the moved saddle, and full-germ coverage

The fixed point estimate gives

 ||x_{f,a_0}||infinity
     <= (|a_0|+C_0||N_f(0)||)/(1-theta_0).                    (F15)

Choose |a_0| and U small enough that this is strictly below a/2. The entire
backward trajectory then stays where chi=1 and is a trajectory of V_f. It is
not an artefact of the cutoff.

Let p=p(f) and a_p=P_u p. The constant path p is the fixed point of (F11) for
a_0=a_p, since Ap+N_f(p)=0. Subtracting this constant path gives the equation

 y=(exp(lambda t)(a_0-a_p),0)+K[N_f(p+y)-N_f(p)].              (F16)

For THIS existence comparison only, use E_beta with norm
sup_{t<=0} exp(-beta t)|y(t)|. The elementary two integral estimates give the
bound C_beta in (F9), so (F16) has a unique fixed point in E_beta, satisfying

 ||y||beta <= |a_0-a_p|/(1-theta_beta).                       (F17)

This fixed point also belongs to E_0 and solves (F16) there; E_0 uniqueness
identifies it with x_{f,a_0}-p. Thus x(t)->p exponentially as t->-infinity. No
differentiability in E_beta is invoked. In particular we never differentiate
the moving p inside DN_f or an exponentially weighted composition operator.

Conversely, any backward trajectory of the original V_f that stays in the small
ball is bounded. Variation of constants gives (F10)-(F11): the stable homogeneous
term from a time -T disappears as T->infinity because the trajectory is bounded.
The unstable part uses its value at zero. By uniqueness it is one of our graphs.
This proves that the construction gives the full local unstable germ, not a
selected orbit or an arbitrary continuously chosen curve. Reversing time proves
the stable germ, with the roles of lambda and mu interchanged.

Define the anchored graph parameterization by

 Gamma_f(s)=x_{f,a_p(f)+s}(0), |s|<=s_*,                      (F18)

on a compact interval with strict smallness slack. Its unstable projection is
a_p(f)+s, so partial_s Gamma is nonzero and it is embedded. Gamma_f(0)=p(f).
Formulae (F5),(F13) prove joint C^1 evaluation (D) and the C^1 perturbation bound
(B). Joint continuity of partial_s Gamma, uniform on compact s-intervals, proves
f->Gamma_f is CONTINUOUS into C^1 arcs. We do not differentiate partial_s Gamma
in f. Restrict s to either sign for the two half-branches. Fixed frame plus
fixed sign labels produce the four branches needed by [RC-S].

The construction is localized: if h vanishes on the endpoint neighborhood that
contains the cutoff and subsequent local arc, then N_{f+th}=N_f there and all
local branch launches are identical. A germ may be propagated to any declared
nearby local section by a finite flow inside that neighborhood; the same locality
holds. This is the endpoint-support fact needed by the companion proof.

## 6. Finite flows, robust sections, and mismatch derivatives

On each compact finite-time region, the integral equation
Phi_f(t,z)=z+integral_0^t V_f(Phi_f(s,z)) ds is a contraction on sufficiently short
time slabs. Its Nemytskii map in the C^0 path norm is C^1 by (F4). The same IFT
argument and concatenation of finitely many slabs give jointly C^1 dependence
in (f,z,t), with continuous derivatives. The field variation satisfies

 w'=H_f(Phi_f)w+grad h(Phi_f),                                (F19)

with initial derivative if z=z(f). Gronwall bounds it by C||h||C1. There is no
need for positive speed merely to solve or differentiate this ODE; positive speed
is required on the finite regular arcs used for transverse hits and chart margins.
Physical flow starting exactly at the saddle is stationary; (F18), not that flow,
parameterizes the local germ across its anchor.

For a fixed section rho=0 and a robust transverse hit at parameter tau, [RC-S] R1
ensures the nearby zero stays the FIRST contact with the CLOSED section. Joint
C^1 evaluation and the scalar IFT give

 Dtau(f)[h]=-D_f[rho(Gamma(f,tau))][h]/partial_s[rho(Gamma(f,tau))]. (F20)

The transverse denominator is bounded away from zero on a smaller neighborhood.
This gives the required derivative bounds for launches, central hits, and
D_chi=s(z_u)-s(z_s). Applying it to EVERY local and central section supplies the
literal A2-T and joint A2-D hypotheses of [RC-S], with graph coordinates fixed
once per atlas chart. The same reasoning yields A2-G and its bound for [CL].

A2-G alone supports the reduced slicing application, but does not by logical
implication prove an arbitrary stronger Frechet statement. Here joint Frechet
C^1 was proved separately by (F11)-(F14); no Gâteaux/Frechet identification is
being made from the line theorem alone.

## 7. Interface disposition and remaining use

This is an author-side full argument for the precise A2 interface. [CL]'s Lemma J,
regularity diagnosis and weaker-use observation are credited. Its center-manifold
citations are not imported as unverified substitutes: the hyperbolic construction
above is displayed in full, including cutoff smallness, forcing, differentiability,
decay and complete local-germ identification.

No false C^1-into-C^1 conclusion remains in this successor. The companion manuscript
supplies a new A3/A4 route, the generic full-measure argument, and a qualitative
planar no-connection composition. The robust first-contact geometry still has the
exact [RC-S] source/review lineage. A nonauthor review must evaluate these actual
arguments, not infer them from the finite scalar checks or the previously merged
R3/R4 conditional review. No C103 bound, RN/JETMOD, 3D theorem, numerical constant,
scientific-status transition, or claimed historical novelty is included.
