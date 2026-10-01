# Hard-negative fibres identify the actual elder law in every fixed dimension

Author-side successor by OpenAI, 30 September 2026. Scientific effect NONE.
Disposition: AUTHOR_SIDE / HOLD pending qualified source-bound review.
The root, concave_fibre_geometry and higher_d_source_interface are contributors;
their source audits are not nonauthor acceptance. All source conditions below
are retained. No count moment or remote-count theorem is a premise.

The complete deterministic lift, including its counterexample, is proved in
[HARD_FIBRE_LEMMA.md](HARD_FIBRE_LEMMA.md). The detailed analytic source
interface and retained matrix integral are in
[SOURCE_INTERFACE.md](SOURCE_INTERFACE.md). [SOURCES.json](SOURCES.json)
binds the complete public sources by immutable commit/path/blob/SHA256.
Together these files expose the full new argument; source hypotheses are not
accepted merely by being linked or having verified hashes.

## 1. Model and the actual pairing estimand

Fix an integer d>=3, torus side L>0, birth b in R, positive gap mark k, and an
orthonormal axial/transverse frame R. Use the exact variance-one periodized
Bargmann–Fock Gaussian field of [P], with strictly positive Fourier weights.
At M=(-r/2,0), S=(r/2,0), impose the original observations

    f(M)=b, f(S)=b-k r^3, grad f(M)=grad f(S)=0.

Q_r is this original 2(d+1)-observation Gaussian regression. Set

    W_r=F_d(H_M) F_(d-1)(H_S),  Z_r=E_(Q_r) W_r,
    Q_r^W=(W_r/Z_r) Q_r.

F_j is absolute Hessian determinant restricted to j negative eigenvalues.
There is one original weight and one FULL normalizer. No adjacency restriction,
extra pin density or good-event normalizer is inserted. [P] gives
Z_r/r^2 -> z0>0, with its congruence erratum [ERR] and convergence-in-law reading
rule [REC]. The ordinary global elder death is the superlevel maximin

    d_f(M)=sup_(gamma(0)=M, f(gamma(1))>b) min_t f(gamma(t)).

An essential maximum has d_f(M)=-infinity. On the almost-sure global Morse
distinct-value locus of [P] §8, d_f(M) is the value of the actual elder merge
saddle when finite. Define

    F_r={actual ordinary elder partner of M is not S},
    p_r=Q_r^W(F_r^c),   D_r=(d_f(M)-b)/r^3.

The event is Borel by [P] §8; whole-field marked Kac–Rice uses the exact [BOREL]
repair, not an assumption that elder selection is a continuous local mark.
These are candidate pair-Palm estimands; counting every rejected candidate
does not count each replacement elder bar once.

## 2. Original spectral coordinates and the soft cubic

Put m=d-1. Write the signed ordered eigenvalues of -D_y^2 f(0) as
mu1<...<mum and use

    mu1=-r s,  h=(mu2,...,mum),
    D_y^2 f(0)=O diag(rs,-h2,...,-hm) O^T.

The additional independent third-derivative list T omits only f_xxx. The
finite-r observation frame U_r contains its averaged divided difference;
the contact frame U_0 supplies f_xxx=12k. At finite r the actual midpoint
derivative is 12k+O(rK), rather than an additional exact pin. Rotate T by
diag(1,O) and denote the resulting tensor coordinates by tau. Retain every
tensor entry, every angular variable, and the actual non-isotropic Gaussian
density. No GOE or full rotational invariance is assumed.

Precisely, the spectral law below is the extended disintegration of [SC] §2:
ordered eigenvalues and normalized Haar O with the multiplicity constant c_m
fixed by [SC] (8). Equivalently, augment the raw matrix with a uniformly chosen
sign frame among its diagonalizers on the simple-spectrum locus. A deterministic
eigenvector selection is not silently assigned this Haar law. Repeated spectra
are null, and the physical conclusions are gauge invariant.

Let Theta_r=(s,h,O,tau) in that extended law. The raw conditional density of
(D_y^2 f(0),T) is h_r, converging locally uniformly to h0. Write
a=tau_xxz, beta=tau_xzz, c=tau_zzz. The soft profile is the original-coordinate
cubic

    P(X,Z)=2kX^3-3kX/2-k/2+sZ^2/2
             +(a/2)(X^2-1/4)Z+(beta/2)XZ^2+(c/6)Z^3.

Set B=beta-a^2/(12k), D=(c-a beta/(4k)+a^3/(72k^2))/2.
The positive typed domain is s<-|B|/2. Exclude the polynomial null sets

    Sigma=12k D^2+(s-B)^2(B+2s)=0,
    Delta=12k D^2+B^3=0.

The exact [CUB] classifier, also consumed by [LOCAL], gives n in {0,1,2}
additional nondegenerate soft saddles in -k<P<0. Let C(P) be these roots, in
the ORIGINAL (X,Z) coordinates, and

    h_*(P)=max({-k} union {P(Y):Y in C(P)}).

The algebraic shear u=X+aZ/(12k) is used only to classify roots; locations
recover X=u-aZ/(12k). For n>0, -k<h_*<0. For the unique limiting location mark
additionally exclude D=0, as in [LOCAL] §6. All these exclusions are nonzero
polynomial Lebesgue null sets; the source densities do not charge them.

## 3. The deterministic hard-fibre bridge

Fix spectral targets with 0<h2<...<hm, a generic typed soft cubic and a realization
of the source coupling with finite C4 norm. [SC] §5 supplies a unique hard
maximum graph in original orthogonal coordinates (x,z,w), w in R^(d-2):

    w=zeta_r(x,z)=O(r^2),
    G_r(X,Z)=[f(rX,rZ,zeta_r(rX,rZ))-b]/r^3 -> P in C2

on every fixed soft disk. Write M0=(-1/2,0), S0=(1/2,0) for the normalized
soft pins, keeping M,S for the physical original pins. The graph retains
EXACT critical pins and values G_r(M0)=0, G_r(S0)=-k, since the original hard
gradients vanish there and the hard stationary point is unique. The proof of the supplied C2 interface,
including its derivative powers, is displayed in SOURCE_INTERFACE §2.

The missing geometry is a full-dimensional barrier, not another root count.
For a fixed soft disk containing the planar collar and doubled critical chords,
let eta=min_j h_j>0. Taylor and the fixed C4 bound give

    f_ww <= -(eta/2) I

on that soft disk at physical r scale and on a hard ball of radius c0 r, for
all sufficiently small r. This is a pointwise fixed-target bound; constants may
depend on eta. Twice integrating along a straight hard fibre gives

    f(t,zeta_r(t)+v) <= f(t,zeta_r(t))-(eta/4)|v|^2.

Choose fixed rho with D0=eta rho^2/4>k. The centred hard tube
|v|<=rho r^(3/2) fits inside the c0 r ball, since zeta_r=O(r^2) and
r^(3/2)=o(r). On its hard boundary the normalized drop is at least D0.
This is the quantitative hard-depth hypothesis of HARD_FIBRE_LEMMA. The r^2
scale of the critical graph alone would give a drop of order r^4 and would
not block escape across a death window of order r^3.

For each continued soft window root Y_r, and the exact normalized S0, put

    h_r=max({-k} union {G_r(Y_r):Y in C(P)}).

Theorem H (actual highest partner). Under the displayed fixed-target hypotheses,
for every sufficiently small r,

    d_f(M)=b+r^3 h_r.                                    (H1)

On the actual global Morse distinct-value locus, the unique highest continued
graph saddle is the actual ordinary elder partner. Its full Hessian has one
positive and d-1 negative directions. If n=0 the partner is EXACTLY S; if n>0
a continued local window saddle preempts S. Limiting ties do not obstruct H1;
the comparison is between the finitely many ACTUAL heights at that r.

Proof. [LOCAL] §§3–6 construct, in the reduced profile, compact disks K_(r,h)
for every h_r<h<t0<0, with G_r=h on the boundary and h<G_r<=0 inside.
The fixed soft collar works at the same sufficiently small r for every such h.
Thicken each disk by the centred hard tube just verified. Its lateral boundary
has f<=b+r^3 h, its hard boundary has f<b-k r^3, and its interior has f<=b.
Any global path from M to a point older than birth must exit this compact
embedded barrel. It therefore has minimum <=b+r^3h, regardless of the exterior.
Let h decrease to h_r at that same r: the upper bound is exact.

For the lower bound, follow each moving soft critical chord from M0 through
Y_r to its doubled endpoint along the hard graph. The reduced restrictions
converge in C2 to P(Y)(3t^2-2t^3), have exact derivative zeros at t=0,1, and
therefore decrease to Y_r then increase to an older endpoint. Their exact
minimum is G_r(Y_r). The largest one supplies the opposite bound. The explicit
Schur quadratic-form completion in HARD_FIBRE_LEMMA §3 adds d-2 hard negative
directions and proves the full saddle type. Distinct global critical values
identify that root as the merge saddle. The full cap regularity, root stability,
common-index collar and chord proof are given in HARD_FIBRE_LEMMA §§3–6. QED.

Thus D_r->h_* pointwise in this coupling. When D!=0, the highest soft root
Y_*(Theta) is unique and the actual partner divided by r tends, in the original
physical axial frame, to

    T_*(Theta)=R(X_*, O(Z_*,0,...,0)).                    (H2)

The hard graph coordinates divided by r vanish. Sign changes of an eigenframe
change Z_*,tau and O together, leaving H2 invariant. No separatrix or
Morse–Smale premise is needed. HARD_FIBRE_LEMMA §8 gives an explicit smooth
counterexample if the contained hard-depth tube is omitted, even when graph
convergence is exact and the physical hard Hessian is uniformly negative.

## 4. Full failure-measure exhaustion from the endpoint matrix

H1 is pointwise in fixed jets. It does not alone identify the full rare failure
law. This section supplies the required exhaustion from the actual endpoint
matrix, independently of any count or near-occurrence event.

On typed support put B_M=-D_y^2 f(M)>0, with ordered eigenvalues

    0<lambda1<=lambda2<=...<=lambdam=Lambda,  m=d-1>=2,
    v=m(m-1)/2.

[P] (4.2)–(4.3) regress the whole field on the ENTIRE endpoint matrix and give
an independent residual g_r. Put J=1+||g_r||C4, U=J+Lambda. All fixed J moments
are uniformly bounded, J is independent of the whole matrix, and

    K=1+||f||C4 <= C(J+||B_M||F) <= C U.                 (E1)

Here Lambda is among the retained eigenvalues lambda2,...,lambdam; its being
independent of lambda1 for this conditional integration is why m>=2 matters.
No independence among matrix entries, derivative suprema or internal residual
evaluations is asserted.

The exact global good-cap implication [CAP]/[P] §8 gives F_r subset G_r^c,

    G_r={lambda1>[4/(3k)] r M3^2, r M4<=3k/10}.

[P] (7.7), divided by the FULL Z floor once, bounds the M4 exception by O(r^4),
which is o(r^3). On the remaining depth branch,

    lambda1<=D r U^2,
    W_r<=C r^2 U^(2m) lambda1(lambda1+C r U).             (E2)

The second factor is essential: it retains the saddle mixed-square term in
[P] (6.2). The endpoint matrix density has Gaussian bound [P] (3.5); its
spectral Jacobian is at most C Lambda^v. For every retained event E depending
only on J and the hard eigenvalues, the SAME integral gives

    E_Q[W_r;depth,E]
      <= C r^2 E_J integral_hard exp(-c sum_hard lambda_j^2)
             Lambda^v U^(2m) 1_E
             integral_0^(D r U^2) lambda1(lambda1+C rU) d lambda1
      <= C r^5 E_J integral_hard exp(-c sum_hard lambda_j^2)
             Lambda^v U^(2m+6) 1_E d lambda_hard.         (E3)

The extension of the lambda1 interval beyond its actual ordered interval is
an upper bound of a nonnegative majorant. U and E are retained while integrating
lambda1; its Gaussian factor may be dropped. Equation E3 is the retained-mark
version of [P] (7.4), not a new independence or cutoff inversion.

Taking E={U>A}, using arbitrarily high J moments and Gaussian polynomial
integrability, and dividing once by Z_r>=z_*r^2, gives, for every fixed p>0,

    limsup_r r^-3 Q_r^W(F_r,U>A) <= C_p A^-p.            (E4)

Taking E={lambda2<=epsilon} in E3 gives

    lim_epsilon->0 limsup_r
        r^-3 Q_r^W(F_r,lambda2<=epsilon)=0.              (E5)

Indeed integration of the hard Gaussian polynomial over this strip tends to
zero; for epsilon<=1 a constant times epsilon suffices after integrating all
other hard variables and the J moments. All higher-corank intersections are
included, with no inverse-hard-eigenvalue or inverse-gap factor.

Weyl's eigenvalue inequality and Hessian Lipschitz control give

    |muj-lambdaj| <= r M3/2 <= C rU.

On the depth branch this implies

    |s|<=D U^2+C U,   |h|+|tau|+K<=C U.                 (E6)

Consequently E4 is tightness of the FULL failure measure in the actual midpoint
jets and derivative norm, not just a compact-near count estimate. On U<=A,
midpoint h2<=epsilon implies endpoint lambda2<=2epsilon for sufficiently small
r at fixed epsilon,A. Equations E4–E5 and the M4 exception yield

    lim_epsilon->0 limsup_r
        r^-3 Q_r^W(F_r,h2<=epsilon)=0.                  (E7)

Midpoint hard eigenvalues of either sign near zero can carry no lost leading
failure mass. Inverse hard eigenvalues are used only at fixed positive targets
for graph convergence; they never enter E3. The complete detailed derivation
is SOURCE_INTERFACE §§4–5. No scalar shortcut is used: for d=2 one must retain
[LOCAL] §8's separate scalar near/far split, since Lambda=lambda1 there.

## 5. The identified full elder-failure measure

Let the limiting hard domain be 0<h2<...<hm, retain normalized Haar dO and the
complete d tau, and put

    w_+(s,a,beta)=9k^2 [B-2s]_+[-B-2s]_+.

Define the finite measure

    dmu_fail=(c_m/z0) h0(O diag(0,-h) O^T,Rot_O tau)
          product_(j>=2) h_j^3
          product_(2<=i<j<=m)(h_j-h_i)
          w_+(s,a,beta) 1{n(s,a,beta,c)>0}
          ds dh dO d tau.                              (S1)

It is extended by zero off the stated hard/typed domain. The deterministic
classifier bound [SC] (19) proves integrability: if x=-s>0 and n>0, then
x<=2|B|+(48kD^2)^(1/3), and

    integral_s w_+ 1{n>0} <=384k^2 |B|^3+2304k^3 D^2.

The remaining hard spectral factor is a polynomial, while h0 has uniform
Gaussian decay in the ORIGINAL orthogonally rotated raw variables. All angular
variables remain inside the integral. Positive Gaussian density on open typed
nonempty sectors gives mu_fail(total)>0. In [SC] (20)'s notation its mass is

    a_fail=a1+a2.                                      (S2)

This consumes the displayed deterministic integral, not [SC]'s global count
limit. Its remote singleton coefficient beta_far does not enter S1 or S2.

Theorem F (full fixed-dimensional selector-failure law). Under the exact
source interfaces and H1, in the extended spectral law of §2,

    r^-3 Q_r^W(Theta_r in dot, F_r) -> mu_fail in total variation,
    (1-p_r)/r^3 -> a1+a2>0.                             (S3)

Proof. On a fixed bounded spectral box with hard eigenvalues bounded below,
[SC] §2 disintegrates the actual additional full jet. Its soft eigenvalue
change has Jacobian r c_m J_r, where

    J_r=product_(j>=2)(h_j+rs) product_(2<=i<j<=m)(h_j-h_i).

The exact scaled density, with a bounded full-field multiplier I, is

    (c_m r^2/Z_r) J_r h_r(O diag(rs,-h) O^T,Rot_O tau)
                         E[(W_r/r^4) I].               (S4)

This ledger is r^-3 times one spectral r times the original r^4 weight over
the original Z_r. [SC] §5 gives W_r/r^4 -> product h_j^2 w_+. Its limiting
weight is zero off the typed domain and ON the typed boundary; selector
convergence is unnecessary there. For a typed generic target H1 gives the
actual indicator I=1_F eventually equal to 1{n>0}. The excluded algebraic
sets are null, not discarded positive mass.

The independent complete-jet coupling [SC] (5)–(6) gives
K<=C_box(1+||F||C4). Its two-short-column bound [SC] (15) bounds W_r/r^4 by an
integrable fixed polynomial in that coupling norm on the box. Thus pointwise
convergence, the exact weight limit, and dominated convergence give compact
L1 convergence of S4 to S1, including near the typed boundary. Repeated hard
spectra are null; no uniform inverse-gap estimate is required on the box.
E4–E7 exhaust the ACTUAL failure measure, and S1 is integrable. First exhaust
bounded boxes and then let the positive hard lower bound decrease to zero.
The limsup of both excluded tails tends to zero. Compact L1 plus those two
tails is global L1, which is precisely the total variation statement S3.
Taking total masses proves its coefficient. QED.

This establishes the pairing relevance of the microscopic soft geometry.
It does not equate two extra saddle witnesses with one maximum/saddle pair.
Neither a factorial moment nor fixed-remote mixing is used to infer selection.
When the fixed-r almost-sure global Morse/distinct-value locus is used in this
conditional coupling, take a countable intersection along an arbitrary fixed
sequence r_j->0. Dominated convergence along every such sequence proves the
stated limit. No common probability-one locus for uncountably many pinned laws
is assumed.

## 6. Actual replacement location, death and lifetime

On F_r let T_r be the actual elder partner's displacement from the midpoint,
in the local torus chart, divided by r. Use an isolated sentinel if the partner
is essential or outside that chart. For the same reason use a sentinel in D_r
when d_f(M) is not finite. These exceptions have r^-3 mass tending to zero:
on each regular compact jet sector H1 provides a local older path and actual
partner for all sufficiently small r; E4–E7 exhaust the remaining failure mass.

Theorem M (actual marked law). The finite measures

    r^-3 Q_r^W((Theta_r,T_r,D_r) in dot, F_r)

converge WEAKLY to the pushforward of S1 under

    Theta -> (Theta,T_*(Theta),h_*(Theta)).               (M1)

The conditional-on-failure law is M1 divided by a_fail. The lifetime mark
(b-d_f(M))/r^3 converges in that law to -h_* in (0,k), and its fraction of the
candidate lifetime converges to -h_*/k in (0,1).

Proof. At a generic positive hard target H1 identifies the exact actual
winning continued root. Off the additional null set D=0, [LOCAL] §6's winning
soft root is unique; continuation and the vanishing r-scaled hard graph give
H2 and D_r->h_*. Insert any bounded continuous joint test function in S4.
The same compact dominated-convergence argument proves convergence of its
integral. E4–E7 remove the tails; sentinel mass has already been excluded.
No continuity across the polynomial transition sets is assumed. QED.

Weak, not total variation, convergence is claimed for these real-valued marks.
Tightness of M1 also gives, for EVERY deterministic delta_r->0 with
delta_r/r->infinity,

    Q_r^W(F_r, dist(actual elder partner,midpoint)>delta_r)=o(r^3).  (M2)

For a given tolerance choose a fixed large radius with arbitrarily small
limiting marked tail, use weak tightness including the sentinel, then use
delta_r/r eventually larger than that radius. This is actual failed-partner
localization, rather than localization of a count-defined witness.

## 7. Exact compact lifetime-density consequence

Retain [P] §§10–12's exact compact population: birth b in an interval B, gap k
in an interval K, both of positive length and K bounded away from zero, axial
orientation u in S^(d-1) with ordinary area measure, per unit midpoint volume.
Choose a Borel transverse completion R(u) as in the source. The coefficient
a_fail is independent of that completion: the original selection probability
is physical and independent of a transverse coordinate choice, and S3 is its
unique limit. This does not assert torus rotational invariance or birth-factor
cancellation in higher dimensions.

Use the source's ACTUAL radial ledger, in every fixed d:

    A_r=12 pi_r(R(u);v_r) Z_r/r^2,
    nu_cand(ell)=ell^-1/3 integral_(B x K x S^(d-1))
                         A_((ell/k)^(1/3))/(3k^(2/3)).

The selected density has the additional p_r. The dimension powers have already
cancelled in [P] §10; no new spatial Jacobian or dimension-dependent lifetime
power may be inserted. [P] (7.8) supplies a common compact-mark bound on
(1-p_r)/r^3, and [P] (10.2)–(10.3) supply common bounds and A_r->A0. These are
existing domination interfaces, not uniformity inferred from pointwise H1.

With r=(ell/k)^(1/3), the exact nonselected candidate density therefore has

    ell^-2/3 [nu_cand^(B,K)(ell)-nu_eld^(B,K)(ell)]
       = integral_(B x K x S^(d-1))
                  A_r/(3k^(5/3)) [(1-p_r)/r^3].

Dominated convergence and S3 identify

    nu_rej^(B,K)(ell) ~ C_fail^(B,K) ell^(2/3),
    C_fail^(B,K)=integral_(B x K x S^(d-1))
                  A0(b,k,u) a_fail(b,k,u)/(3k^(5/3)) db dk d sigma(u). (L1)

C_fail is finite and strictly positive. The full z0 cancels if A0=12pi0z0 is
substituted into S1; there is still one original pin density and no additional
normalization.

L1 is the compact candidate-minus-selected counting measure. It is not a
replacement-bar intensity obtained by counting all rejected candidates, nor a
standalone second-order selected-density expansion. An unrestricted refined
difference does not follow; its far rejected population is different. No new
k->0, d->infinity, volume, or escaping-mark uniformity is claimed.

## 8. Hypotheses, explicit falsifiers and review boundary

H1 assumes a generic typed cubic and its pinned reduced C2 convergence, an
embedded fixed soft collar, and a CONTAINED negative hard tube with drop D0>k.
The graph and tube are proved from [SC]'s actual smooth field on fixed positive
hard targets. The exact finite-r partner additionally uses the source's actual
global Morse distinct-value locus. A unique limiting position additionally
excludes D=0, a null set. The deterministic lemma does not require probability,
Morse–Smale, a separatrix assertion or control of the exterior.

The stochastic statements require the original positive-spectrum field,
nonsingular contact/full-jet regression, independent endpoint-matrix residual
with all C4 moments, actual cap implication, double soft-factor weight bound,
full normalizer floor, and the original spectral density/coupling interfaces.
They are source-bound conditions, not consequences of tests or publication.
All inverse-hard constants are pointwise only. The actual rare failure tail
and multiple-soft exclusion are proved by E3–E7, rather than borrowed from a
near-count event. The full typed boundary is treated by its continuous zero
weight. The Haar-gauge extension is part of the precise measure statement.

Falsifiers:

- A full path bypassing a contained hard-depth cap at height above h_r, or a
  graph-lifted moving chord whose exact minimum is not the continued root,
  invalidates H1. The thin-tube counterexample in HARD_FIBRE_LEMMA §8 explains
  why graph convergence alone is not a substitute for that hypothesis.
- A leading failure mass escaping every bounded midpoint jet set, or staying
  at a nonvanishing fraction on h2<=epsilon as epsilon->0, contradicts E4/E7.
  A defect in the parent cap implication, original residual independence or
  retained matrix soft integral would reopen that analytic step.
- A dropped saddle mixed-square factor, extra restricted normalizer, omitted
  hard/sign multiplicity or GOE substitution changes S1 and invalidates S3.
- A positive leading essential/sentinel mass contradicts M1. Total variation
  for real-valued location/lifetime marks is outside the claim.
- Replacement-bar, unrestricted refined-density, new parameter-uniform or
  numerical uses of L1 are outside this proof's interface.

This is a new fixed-dimensional actual elder/failure/lifetime candidate, with
full proofs and source identities exposed. d=2 remains the separate [LOCAL]
scalar proof. No controlling acceptance, status, graph, prize, Boolean, parent
proof or source history is altered. Qualified nonauthor review must bind this
successor itself; acceptance of a count packet or of [LOCAL] alone is not an
acceptance of this higher-dimensional lift.
