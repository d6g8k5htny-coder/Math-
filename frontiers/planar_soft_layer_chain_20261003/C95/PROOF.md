# Corrected explicit trap and actual weighted maximin selection

Object: C95-CORRECTED-TRAP-WEIGHTED-MAXIMIN-20261003-v1.
Integrator and author of the composition: OpenAI/Codex root01a0bbb5,
acting for Dylan Roy — delegated AI work. Original A2 author: Anthropic
Claude, session_01NMeKEismAyeqgdB4sy2NJU. The three corrections were
proposed in the C90 OpenAI/Codex reviews; they are not claimed as a new
discovery by this integrator. Disposition: frozen candidate for fresh
nonauthor review. Personal reading PENDING; organizational independence0;
scientific effect NONE.

This is an additive correction to a named source, followed by a new explicit
composition with C94. The literal original A2v1 remains AMEND. No original
source is overwritten, and this does not impersonate a Claude-issued v2.
The corrected mathematical object is the ordered pair (A2v1, sections1–3
below), together with the retained hypotheses recorded in section4. The
source's old numerical-check reports remain historical author reports;
they are not new verification evidence or substitutes for these repairs.

## 0. Exact sources and role

- A2v1: main229 comment5963200491, 24223 UTF-8 bytes, SHA256
  d5f1f1f0e5d39602d012591ffadb5f3b4caa3f2ad564bc89c8c9f13d4189a9fd.
- C90 combined review: comment5963477339, 4817B, SHA256
  9f4958107d26dea94240be94a801c13ae76d0658f6548ffb8ea88fa6f4e55c42.
  Its complementary slices are comments5963376279 and5963452713.
- QS: comment5961415030, 37032B, SHA256
  12ffa126e45253fea5eec47f50ffa842a61165a2cbc0f5917e3543e81c09c1f2.
  We use its explicit local polynomial bounds, not its older implicit
  global-flow trap construction.
- CUB: blob bb446d08db8a944537a743ad550b88c1c2ad5758, 19889B,
  SHA256117e9299a71e6139270266889eb772ed97518e402d9af029bbdb67caf9d4a0f0;
  only the extra-critical-point identities C7–C8 are consumed.
- C94: comment5964517708, 15407B, SHA256
  0fe4fa2028f8ddbbf5a79df3879bcbd3789f19409fb44ad739caeabedff1af3c;
  full review5964735560, 30074B, SHA256
  327abea538b814f279a936a71072960de08e53314f0f08dd32c2f8870a32d65e.
  C6–C20 are accepted within their stated hypotheses. Its section6 was
  explicitly conditional on G; section5 below supplies that input from
  the corrected source, without changing C94's historical disposition.

SOURCE_IDENTITIES.json also pins C91–C93 and their reviews. All source
identities establish custody; the argument and imported premises below
establish the mathematical dependency chain. No review vote proves a lemma.

## 1. Replacement for A2 Lemma7(b)'s positive-c reciprocal step

Retain A2's notation and hypotheses, especially (H). For c>0 write
omega=c/psi. Lemma6 gives 0<omega<1/2. Put

    a0=599/250, b0=277/250, k0=256/125,
    K=b0+k0*a0=187969/31250,
    omega0=a0/K=74875/187969.                         (G1)

Replace the sentence containing the unrestricted reciprocal minimum by:

    For 0<omega<=omega0,
      psi F* <= b0/(1-k0*omega) <= K;
    for omega0<=omega<1/2,
      psi F* <= a0/omega <= K.                     (G2)

Here the first bound is used only on the first interval. To prove it,
eta<m_S<=27/250, t_eta<=2eta/9<=3/125, and A2's preceding inequalities
give psi F*<=a0/omega everywhere and
a_min>=1-k0*omega. The latter implies the reciprocal bound only where
its right side is positive. At the switch point,

    1-k0*omega0=b0/K=34625/187969>0.               (G3)

Hence the reciprocal is positive and increasing on the entire first
interval, with endpoint value K. The function a0/omega is decreasing
on the second interval, also with endpoint value K. Moreover
0<omega0<125/256<1/2 and K=6.015008<121/20=6.05.
This proves the same advertised upper bound without evaluating a
nonpositive denominator. The preceding derivative constant is valid since

    A'(u_eta)/2 <= 3(128/125)^2-3/4
                     =149733/62500 <599/250.

The c<=0 cases in the source are unchanged. Therefore psi F*<6.05
still holds in every case. In particular 144K<(148/5)^2, so the source's
29.6/sqrt(psi) height bound, and then its 30/sqrt(psi) box, remain valid.

The original display is not silently retained: at omega=49/100 its
reciprocal denominator is -11/3125, and at omega=125/256 it is zero.
Both points lie in the formerly claimed interval.

## 2. Replacement for the segment assertion in A2 Lemma7(c)

Take c=0, psi=1, R=4/sqrt(1+m), with
0<m<min(m_S,epsilon_M). Let Zs=48/R=12sqrt(1+m).
The extra saddle Y=(-1/2,Zs) has P(Y)=-1-m, hence is not in the trap
at level ell=-1-eta when 0<eta<m. Replace the assertion that the full
segment from M to Y lies in T^v by the following exact statement.

For each eta in (0,m), there is a unique t_eta in (0,1) with

    (1+m)(3t_eta^2-2t_eta^3)=1+eta.                (G4)

Only the segment {(-1/2,t Zs):0<=t<t_eta} lies in T^v. Its endpoint at
t_eta is on the defining level, and the saddle at t=1 lies below it.
Indeed along that line,

    P(-1/2,t Zs)=-(1+m)(3t^2-2t^3).              (G5)

The right-hand factor increases strictly from0 to1 on (0,1), because
its derivative is6t(1-t)>0. Thus the initial segment has P>ell and is
connected to M while avoiding the vertical cut at u=1/2. This proves
membership in the defining component. The rest of the segment has
P<=ell and cannot belong to that component.

As eta increases to m, t_eta increases to1. In this example
F*=(1+eta)/psi=1+eta. The supremal height of that initial segment,
divided by sqrt(F*), is

    12t_eta sqrt((1+m)/(1+eta)) ->12.             (G6)

Consequently the universal constant12 cannot be lowered. This is a
supremum/limit claim; no saddle is placed inside the trap. The admissible
family is nonempty: choose m=1/1000. Then R<4 and
tau_S=tau_M=(4+R)/(6sqrt(3))<5/6. Hence
m_S>72/3125>m and epsilon_M>9/50>m. This sharpness assertion is not an
input to the geometric criterion or the probabilistic composition.

## 3. Replacement for A2 Corollary9(c)'s integration domain

Retain gamma!=0 in the raw chart and rho>0. Write a=|c| and

    x=25(|gamma|+12)^2/(4 gamma^2 rho^2)>0.

The actual integration set is {psi:a<psi<x}. Its weighted mass is

    I(a,x)=0,                                  x<=a;
    I(a,x)=x^3/3-a^2*x+2a^3/3,                 x>a. (G7)

For x>a, I=(x-a)^2(x+2a)/3, so it is nonnegative. It is at most x^3/3
because -a^2*x+2a^3/3<=0. For x<=a, zero is also at most x^3/3.
Thus the source's upper bound is valid on the true typed domain, with
an explicit empty-domain branch. Multiplication by gamma^6 gives

    gamma^6 I(a,x)
       <=(25/4)^3 (|gamma|+12)^6/(3 rho^6).       (G8)

This is the reference soft-measure bound stated by A2; it is not used as
an actual weighted-Palm tail. In particular C94 retains its separate
actual radius bound C(rho^-8+r rho^-4). Gamma=0 is not a pointwise raw
chart. Under C92's continuous finite-jet law it is null, and multiplication
by the integrable determinant weight preserves that null set.

## 4. Corrected geometric interface G: precise consumable theorem

Write

    P(u,Z)=A(u)-(psi+2cu)Z^2/48+RZ^3/3456,
    A(u)=2(u+1/2)^2(u-1), M=(-1/2,0), S=(1/2,0).

Let psi>|c|, allowing all R and including the source's exceptional
curve Delta. Define mu as the maximum of P(Y)+1 over extra nondegenerate
saddles, or -infinity if none. Define

    kappa_S=(psi+c)/48, kappa_M=(psi-c)/48,
    tau_j=2/(3sqrt(3))+|c|/(24sqrt(3)kappa_j)
                           +|R|/(3456 kappa_j^(3/2)),
    rtilde=1/(5tau_S), m_S=2/(125tau_S^2),
    rho_M=1/(2tau_M), epsilon_M=min(rho_M^2/2,1).

Let E_S and E_M be the ellipses of rescaled radii rtilde and rho_M,
respectively, in coordinates (sqrt(3)(u-u_j),sqrt(kappa_j)Z).
Let mu<0 and 0<eta<min(-mu,m_S,epsilon_M), with -mu=infinity if
there is no extra saddle. Put ell=-1-eta, let L0 be the vertical
diameter of E_S, and let T^v be the component of {P>ell}\L0 containing
M. Define the CONTROL SET to include the whole axis segment:

    V'_eta=closure(T^v) union ([-1/2,3/2] times {0}).

Suppose g=P+e is continuous on R^2, C2 on the two ellipses, and

    e(M)=e(S)=0, grad e(M)=grad e(S)=0,
    sup_{V'_eta}|e|<eta,
    sup_{E_S} ||J_S D^2e J_S|| <=2/5,
    sup_{E_M} ||J_M D^2e J_M|| <1,               (G9)

where J_j=diag(1/sqrt(3),1/sqrt(kappa_j)). Then

    d_g(M):=sup_{paths M->x, g(x)>0} min_t g(path(t))=-1. (G10)

Furthermore the two ellipses and V'_eta lie in

    W=[-5/4,3/2] times [-30/sqrt(psi),30/sqrt(psi)]. (G11)

For gamma!=0, X=u-Z/12, zeta=Z/gamma and psi gamma^2=24lambda>0,
the raw image of W has Euclidean radius at most

    Rbox=3/2+(5/2)(|gamma|+12)/sqrt(24lambda).     (G12)

**Proof and dependency audit.** A2 Lemmas5–6 are unchanged; C90's full
first slice reconstructs them. Their polynomial identities follow from
the displayed P, and the imported CUB C7–C8 classify the finitely many
extra critical points. QS's local Lemmas1,2(a)(b),3 and its explicit
tangency-level estimate are retained. The boundary barrier proof in A2
Lemma7(a) is unchanged: every exit from its trapezoid outside L0 has
P<=ell. On its top edge, an interior maximum is an extra saddle below
ell or an allowed degenerate point below -1-m_S; the latter inequality
is the stated QS tangency estimate. Consequently T^v is bounded and
its boundary lies in {P=ell} union L0. No flow estimate at infinity,
critical-free strip, or exclusion of Delta is being imported.

Section1 repairs the only invalid estimate used by Lemma7(b). It proves
the same height bound. A2 Corollary9(a) then bounds the vertical trap,
the two ellipses and the axis by W. In detail eta<27/250 gives
u_eta>=-1-2eta/9>-5/4; the ellipse horizontal extents are at most3/10
at S and3/4 at M. Their squared scaled vertical extents are at most
324/25 and81, respectively. These bounds use
(1+omega)/(1+omega+3|omega|)^2<=1 and
(1-omega)/(1-omega+3|omega|)^2<=1 on -1<omega<1.
The axis endpoint is3/2. Neither the sharpness claim nor G7–G8 is used
to establish this box. Proposition8's stable-cut comparison is also
unnecessary for this vertical-cut theorem and is not a new premise.

For clarity the maximin step is explicit. QS Lemma3 gives g<0 on
E_M\{M}. On closure(T^v) outside the interior of E_M, P<=-epsilon_M:
the boundary values are at most -rho_M^2/2 on the M ellipse and at
most -1 on the trap boundary; an interior maximum cannot be an extra
saddle/degenerate point below ell, or an extra minimum. Hence g<0
there by eta<epsilon_M, so g<=0 on the entire closed trap.

Any path from M to g>0 must leave the trap. At its first boundary point,
g<-1 on {P=ell} and g<=-1 on L0 by the S-ellipse Hessian estimate.
This proves d_g(M)<=-1. Conversely use the retained axis to (3/2,0).
There P+1=2(u-1/2)^2(u+1). Inside the S ellipse QS Lemma2(b) gives
g+1>=0; outside it P+1>m_S>eta, so g>-1. Its far endpoint has
g>4-eta>0. This is a path with minimum exactly g(S)=-1, proving
the reverse inequality and nonemptiness of the path family.

Finally |zeta|<=30/sqrt(24lambda) and
|X|<=3/2+(5/2)|gamma|/sqrt(24lambda). The Euclidean norm is at most
the sum of these component bounds, yielding G12. QED.

Thus G is supplied by the corrected object with its explicit QS/CUB local
premises. This does not upgrade every statement in those parent packets,
and does not accept A2v1's literal false lines. C90's separate stable-cut
review remains at its original scope and is not counted twice.

## 5. Actual torus maximin consequence of C94

Use exactly C92/C94's Gaussian field, pin law Q_r, determinant weight W_r,
full normalizer Z_r=r^2 z_r and weighted law Q_r^W. The parameters are
d=2, fixed finite L>0, k=1, birth b in a fixed nonempty compact set B0,
all orthonormal frames and fixed finite Lambda>0. Do not let Lambda grow
with r. Let E and Good be exactly C94's sector and certificate, with
w=r^(-1/16), delta=r^(1/2), and eta=min(m_S,epsilon_M,-mu)/2.
All constants/cutoffs have precisely C94's permitted parameter dependence.

The actual physical pins are M_r=(-r/2,0), S_r=(r/2,0), with values
b and b-r^3. Define the torus observable, using continuous paths, by

    D_f(M_r)=sup_{paths M_r->x, f(x)>b} min_t f(path(t)),   (G13)

with value -infinity if no higher endpoint exists. For the periodic lift,
F_r(X,zeta)=(f(rX,r zeta)-b)/r^3. In the gamma!=0 chart put
g(u,Z)=F_r(u-Z/12,Z/gamma). This is globally continuous; the chart is
an invertible linear map of R^2, irrespective of its condition number.
The exact cubic identity is G_raw=P under that map, so g=P+e with
the exact pins and local C2 regularity. Every continuous torus path from
M_r has a unique lift starting at its chosen lift; every planar path
projects to a torus path. The endpoint inequalities are preserved, and
positive affine height scaling preserves minima and suprema. Therefore

    D_f(M_r)=b+r^3 d_g(M).                        (G14)

This is equality of the two path families' supremal values, not an
assumption that paths remain in one local patch. C94 also ensures the
small control window embeds (2rw<=L/4). The compact trap prevents any
escape route from raising the maximin value, including paths that later
wind around the torus.

On Good, C94 supplies all G9 hypotheses: the raw radius is at most w;
the actual value error is strictly below eta; both rescaled Hessian
errors have the required bounds; and the entire axis is included.
Its eta satisfies (H). Applying section4 and G14 yields the deterministic
implication

    Good implies D_f(M_r)=b-r^3=f(S_r).           (G15)

The path to the axis endpoint also gives f(x)>b, so M_r is not the
global maximum on Good. This is an actual-field maximin statement.

The events are measurable. For fixed r,b,M_r the set {D_f(M_r)>a} is
open in the uniform topology: any witnessing path has a strict endpoint
gap above b and a strict minimum gap above a, both retained under a
sufficiently small uniform perturbation. It is a union of such open
conditions over paths. Hence D_f is lower semicontinuous as an extended
real functional and {D_f(M_r)=b-r^3} is Borel. E and Good are measurable
by C94. The chart-null set gamma=0 is null under Q_r and Q_r^W by C92.

Let A_r denote {D_f(M_r)=f(S_r)}. C94 C18–C20 and G15 now give

    Q_r^W(E minus A_r) <= C r^(7/2),              (G16)
    Q_r^W(E intersect A_r)
             =r^3 m_E/z0+O(r^(7/2)),             (G17)
    Q_r^W(A_r | E)=1-O(sqrt(r)).                 (G18)

For G17, use Q_r^W(E)=r^3 m_E/z0+O(r^4) and subtract the nonnegative
error bounded by G16; r^4<=r^(7/2) for0<r<=1. C94 supplies uniform
positive lower bounds for m_E and z0, together with upper bounds, so
division gives G18. The full weighted normalizer is still Z_r; no new
soft-layer or reference-model normalization is inserted.

## 6. What is closed, and what is not

This closes the three exact corrections and the explicit geometric input
used by C94 section6, within the retained local QS/CUB hypotheses. It
also supplies the actual weighted maximin conclusion G16–G18. Historical
sources keep their original status; acceptance of this new object requires
its own review. No numerical check or registration is a mathematical
promotion.

The observable is G13. Its translation to a finite ordinary superlevel
H0 persistence bar additionally needs the intended Morse/distinct-critical-
value convention and an explicit event-identification argument. In
particular M is the birth maximum whose component would die when it
meets a higher-born component; it must not be described as the surviving
elder maximum merely because the project uses the label model-elder.
No branch-adjacency equivalence is asserted. The converse from all small
bars to local witnesses, rejected-side chord control, unbounded soft/hard
strata, all marks, shrinking witness collisions, intermediate/coarea
composition and the final lifetime density/remainder remain outside scope.

## 7. Verification role

Exact rational controls test G1–G8, the repaired height and box constants,
admissible sharpness examples, positive affine height conversion and the
rate ledger. Deliberate variants reinstate each faulty domain or omit a
normalization/scope premise and must be rejected. They do not establish
topology, Gaussian bounds or path lifting by finite sampling. Those are
the written argument and explicitly retained source inputs above.
