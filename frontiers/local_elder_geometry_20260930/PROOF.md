# Planar cubic elder mark: a compact-bar transfer theorem

Object: OA-PLANAR-LOCAL-ELDER-20260930-v1.
Authors/contributors: OpenAI root, elder_bridge_audit and its local_topology child, foreground continuation, 30 September 2026. The companion scale analysis has an additional OpenAI contributor, mixed_geometry_audit. The proof is AUTHOR_SIDE / HOLD pending qualified source-bound mathematical review. All these agents have the same provider and earn zero organizational-independence credit. Existing source headers are not treated as live acceptance decisions. Publication, source hashes and engineering checks do not establish mathematical acceptance or promote any parent claim.

This is a new full proof candidate. Only this additive directory is written; no source body, count theorem, register, graph, numerical certificate or integration disposition is changed. Exact dependency interfaces, provenance and unresolved obligations appear below and in SOURCES.json.

## 1. Exact source cut and estimands

The main source cut is Math- commit 98fdb54954a2d9ac0b8ba8ca03e279701f70d751. Immutable source links and blob identities are in SOURCES.json.

* [P] imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md, blob dfed3b8d318a3ab1950957f393307733a4bef3f2, §§1,8,10–14. Read with its congruence erratum (blob 213594d6ca6a86fb938110f4d166d9ce275a02d0), §9 Borel repair (blob fe9b9ce4999908bb3814b500ee2d0ceb0c6f704a), and [REC] §1 reading rule/W1/embedding restriction. [REC] is reviews/d1_chain_reconciliation_20260928/RECONCILIATION.md, blob 75da2597971510f843f8d90c743950cb8c177342.
* [CUB] frontiers/planar_cubic_cluster_20260929/PROOF.md, blob bb446d08db8a944537a743ad550b88c1c2ad5758, §2 (C1)–(C14), §3 Lemma S, §4 (G6)–(G10).
* [LOW] frontiers/window_multiplicity_laws_20260928/ELDER_LOWER_AND_DENSITY_GAP.md, blob aaefc8da9668e819591dd9db0b34442394f2362e, §§1–4; and frontiers/elder_lower_all_d_20260929/PROOF.md, blob 7f41c9e315be0a7985d4c770a11a2cdf717bd46a, §§0,3–5.
* [TWO] frontiers/two_scale_cluster_geometry_20260929/TWO_SCALE_LAW.md at PR166 head be9b7fa95de9b7e59a67347640e157ed3027f624, blob a32fd5f7d941bbe1fe943df045b1e0fbec8d691c, §§1–4, (M1)–(M2), Theorem L and (L3).
* [Q] frontiers/c6_palm_route_20260929/PROOF.md, blob 89eb8adf08fe7afc2cab9662d3a9875c05ae5cc5, §1.2 Theorem Q and §1.3 non-claims.
* [U] frontiers/unrestricted_selection_difference_20260929/PROOF.md, blob 5a55b179a974a90c65d257f3f93765cc6fb30bb8, §§1,3–5.

For the actual pinned law Q_r^W, the pins are M_r=(-r/2,0), S_r=(r/2,0), heights b and b-kr^3, and both gradients zero. The weight is W_r=F_2(H_M)F_1(H_S), with exactly one FULL Z_r=E_Q W_r.

N_r in [Q]/[TWO] counts **additional critical points of all indices in the open height window**, excluding the two pins. The ordered pair measure (L3) is a measure of two additional window witnesses. Its microscopic limit has two index-1 saddles. It is not a maximum/saddle persistence-pair measure.

The elder selector in [P] is different:
d_f(M)=sup_{gamma(0)=M, f(gamma(1))>f(M)} min_t f(gamma(t)),
and p_r=Q_r^W{d_f(M)=f(S)} on the Morse distinct-value locus. Its candidate maximum/saddle intensity is r A_r dr db dk d sigma with A_r=12 pi_r(Z_r/r^2); its selected intensity is r A_r p_r with the same measures. The lifetime pushforward ell=kr^3 supplies r dr/dell=ell^(-1/3)/(3k^(2/3)), [P] §§10–11. There is no adjacency normalization, no factor 1/2 and no second Z_r.

Consequently, localization of (L3) alone does not supply the elder mark. The common leading candidate/elder lifetime density is already supplied by the reconciled D1 cap/selection/Kac–Rice chain, rather than by C6 localization. [LOW] identifies the compact-window rejected density order ell^(2/3); [U] separately shows a positive far rejected density and forbids importing that compact-window decay as an unrestricted difference rate.

The following theorem adds an actual topological mark to the planar cubic sector. It uses neither a new count argument nor any remote witness theorem.

## 2. Deterministic theorem

Fix k>0 and a typed cubic from [CUB]:
P(X,Z)=2kX^3-3kX/2-k/2+sZ^2/2
       +(a/2)(X^2-1/4)Z+(beta/2)XZ^2+(c/6)Z^3.
Write M=(-1/2,0), S=(1/2,0), so P(M)=0, P(S)=-k and both gradients vanish. With the determinant-one shear u=X+aZ/(12k), set
B=beta-a^2/(12k),
D=(c-a beta/(4k)+a^3/(72k^2))/2.
The typed domain is s<-|B|/2.

Exclude the two algebraic sets
Sigma_k={12kD^2+(s-B)^2(B+2s)=0},
Delta_k={12kD^2+B^3=0}.
Both are nonzero polynomial zero sets after clearing fixed positive k denominators, hence Lebesgue-null. The first is [CUB]'s window transition; the second is the only additional exclusion made here.

Let C(P) be the additional critical points with -k<P<0, and put
h_*(P)=max({-k} union {P(Y):Y in C(P)}).
The cubic classifier already proves C(P) finite and its points nondegenerate saddles.

**Theorem E.** For every such generic typed cubic:

1. Its ordinary maximin connection level to a point higher than M is h_*(P).
2. Suppose global smooth functions f_i are defined on compact surfaces, with embedded coordinate charts at shrinking scales r_i->0. Suppose their scaled functions
   g_i(X,Z)=(f_i(r_iX,r_iZ)-b)/r_i^3
   converge to P in C^2 on every fixed compact disk, and retain the exact pins, gradients and values 0,-k. Then their global normalized death levels satisfy
   (d_{f_i}(M_i)-b)/r_i^3 -> h_*(P).
   No conditions are imposed outside the shrinking coordinate disks.
3. Continue the finitely many points of C(P) to local critical points of g_i by pinned C^2 root stability, and include the exact pinned saddle S. For every sufficiently large i the global death level is exactly the highest *actual* height in this finite continued set. On the global Morse distinct-value locus its unique highest point is the actual elder partner. If C(P) is empty, that point is exactly S_i; if C(P) is nonempty, it is a continued window saddle and S_i is not the partner. Thus the selector-failure indicator converges to 1{C(P) nonempty}.

The theorem is planar and pointwise in the cubic and coupling realization. It makes no assertion uniform over marks, dimensions, radii or approaching exceptional sets.

## 3. The critical-chord identity supplies the lower bound

For any polynomial of degree at most three and any two critical points M,Y, put q(t)=P(M+t(Y-M)). Since q'(0)=q'(1)=0, interpolation gives exactly
q(t)=P(M)+(P(Y)-P(M))(3t^2-2t^3).
This also holds when the restriction has lower degree.

Here P(M)=0 and h=P(Y)<0. On 0<=t<=2 the minimum of h(3t^2-2t^3) is h, attained at t=1; the endpoint is -4h>0. Every negative critical point therefore gives a finite path from M to a strictly higher point whose bottleneck is exactly its own critical height.

Apply this to Y=S and to each window saddle. It follows that d_P(M)>=h_*.

For g_i, the same fixed finite path has endpoint strictly above zero and minimum at least h_* minus an error tending to zero. Hence the global normalized death has liminf at least h_*. This path is a path in the actual surface after rescaling; no claim about its being a separatrix or an ascending branch is made.

When C(P) is nonempty, h_*>-k, so the strict margin alone proves eventual failure of selection of S_i.

## 4. No finite-height escape at infinity

In the sheared coordinates the leading homogeneous cubic is
H(u,Z)=2ku^3+(B/2)uZ^2+(D/3)Z^3.
Its derivatives are
H_u=6ku^2+(B/2)Z^2,
H_Z=Z(Bu+DZ).

A nonzero common zero requires Z nonzero. If B=0 it exists exactly when D=0; if B is nonzero it exists exactly when 12kD^2+B^3=0. Thus off Delta_k, grad H has no zero on the unit circle. Compactness and homogeneity give |grad H(z)|>=c|z|^2, and lower-order terms then give
|grad P(z)|>=c_0|z|^2 for |z|>=R_0
after increasing R_0. The invertible shear preserves such a bound up to constants.

There are no critical points of P with value in (h_*,0), by the definition of h_* and [CUB]'s complete classification of all window points. Near M a sufficiently high negative regular level t_0 has a small closed level oval enclosing a disk K_0. The disk contains only the strict maximum M.

For any h in (h_*,t_0), choose a smooth height cutoff chi with 0<=chi<=1, equal to one on [h,t_0], supported in a slightly larger critical-free strip inside (h_*,0), and zero near zero. The vector field
V=-chi(P) grad P/|grad P|^2
is smooth and globally bounded after setting it to zero outside that strip. The gradient-growth bound controls it at infinity, and compactness controls it elsewhere. Its flow is defined for the finite time t_0-h; it fixes M. The initial boundary stays where chi=1, so its P-value decreases at speed exactly one and ends at P=h. The image K_h is compact, contains M and has boundary P=h.

Moreover P is nonpositive throughout K_h: the initial disk has P<=0 and along the flow P never increases. Thus every path from M to a point with P>0 exits K_h and has minimum at most h. Letting h decrease to h_* proves d_P(M)<=h_*. Together with §3 this proves part 1.

This is the missing compact-bar/escape argument. Merely having finitely many window roots would not exclude a finite asymptotic critical level; the Delta_k exclusion and the gradient estimate do.

## 5. Transfer of the upper bound to the actual global field

Fix h with h_*<h<0. Choose the initial maximum-level oval in §4 at a level t_0 strictly between h and 0. The compact disk K_h has P=h on its boundary and P<=0 inside. Its only point with P=0 is M.

For completeness, this last uniqueness does not require a global Morse hypothesis on P below the window. At any extra critical point [CUB] (C8) gives
P=-k(u+1/2)+(s/6)Z^2.
If B>0, the conic forces |u|<1/2, so this is negative. If B<0, either u>=1/2, when it is below -k, or u<-1/2; (C9) and 2s/B>1 again make it negative. For B=0, the two extra possible heights are s^3/(6D^2) and -k+s^3/(6D^2), both negative. Thus M is the only critical point at value zero or above. A second interior zero maximum of K_h would be another such critical point. Boundary h is negative.

The exact pin M and C^2 convergence imply g_i<=0 on K_h for all sufficiently large i: in a fixed small ball around M its Hessian remains negative definite and M remains critical with value zero; outside that ball P has a strictly negative maximum on the remaining compact set, so C^0 convergence suffices. Boundary values of g_i are at most h+epsilon for all large i.

Any actual global path to a point above birth must leave the embedded r_i K_h because there is no such point inside. It therefore crosses a boundary at value at most b+r_i^3(h+epsilon). This proves the normalized limsup is at most h+epsilon. Let epsilon->0 and h->h_* to prove part 2.

This uses a local compact boundary to control the global maximin, so exterior connectivity cannot invalidate the bound.

## 6. Exact selection of the highest actual continued local saddle

Convergence of death heights alone would not identify the location or exact partner. The following finite-index strengthening supplies both.

Let the finite set be C(P) union {S}. For each Y in it, let Y_i be the unique continued critical point, using exact S_i=S for the pinned saddle. All their values are negative for large i. They lie in the window except S, whose value is exactly -k. Define

    h_i=max{g_i(Y_i): Y in C(P) union {S}}.

Fix t_0<0 close enough to zero to have a small maximum-level oval and to satisfy t_0>h_*. Then h_i<t_0 for all sufficiently large i. Choose R_0 large enough for the gradient-growth estimate and to contain the pins, all the continued roots and a small maximum-level oval. Increase R further, also containing every doubled critical-chord path used below, so that

    R-R_0 > 2k/(c_0 R_0^2)+1.

For all large i, C^1 convergence gives |grad g_i|>=c_0|z|^2/2 on R_0<=|z|<=R+1. By [CUB] Lemma S, using exact pins and excluding Sigma_k, sufficiently small C^2 perturbations on B_(R+1) have exactly the continued roots in (-k,0), together with the exact pins at 0,-k. Small disjoint neighborhoods give one root each; the rest of the compact enlarged height band has a positive gradient floor. Thus there is no critical point in (h_i,0) inside B_(R+1). The same sufficiently large index satisfies all these statements, independently of the lower height h chosen next.

### Exact upper bound by a common finite-disk collar

Negative-definite Hessians and exact pinning give a small maximum-level oval for g_i at t_0 inside B_(R_0), enclosing M in a disk with g_i<=0. For each h with h_i<h<t_0, choose a smooth height cutoff chi_h supported in a slightly larger strip inside (h_i,0), equal to one on [h,t_0] and zero near zero. Choose a smooth spatial cutoff eta equal to one on B_R and supported strictly inside B_(R+1). Define

    V_(i,h)=-eta(z) chi_h(g_i(z)) grad g_i(z)/|grad g_i(z)|^2.

The root-free active strip makes this a smooth compactly supported vector field, extended by zero to the plane. Its flow is globally defined for finite times and transports the whole initial disk homeomorphically, fixing M. While a boundary trajectory stays in B_R and its height is in [h,t_0], that height drops at speed exactly one.

It cannot reach the boundary of B_R before time t_0-h<k, because h>h_i>=-k. A first passage from B_(R_0) to that boundary traverses the annulus, where speed is at most 2/(c_0 R_0^2). The chosen width makes this take more than k. Thus all boundary trajectories remain in B_R and reach height h at time t_0-h. They form a Jordan curve, and its enclosed image disk is inside B_R: the complement of B_R is connected and lies in the curve's unbounded component. The cap contains M and g_i<=0 throughout since the cutoff flow never increases height.

Every older path therefore crosses a boundary of height h. For this SAME sufficiently large i the conclusion holds for every h in (h_i,t_0). Taking h down to h_i gives exact normalized global death <=h_i, without exchanging i and h limits and regardless of the exterior geometry.

### Exact lower bound through each continued critical point

For any one Y, consider the moving straight critical chord

    q_i(t)=g_i(M+t(Y_i-M)),             0<=t<=2.

The actual exact criticality of M and Y_i gives q_i'(0)=q_i'(1)=0. C^2 convergence and Y_i->Y give C^2 convergence of these one-dimensional restrictions to

    q(t)=P(Y)(3t^2-2t^3).

Writing h_Y=P(Y)<0, the limiting derivative is negative on (0,1), positive on (1,2), and

    q''(0)=6h_Y<0,                   q''(1)=-6h_Y>0.

C^2 convergence preserves the second-derivative signs near 0 and 1. Together with the *exact* derivative zeros, this preserves the required derivative signs on those endpoint neighborhoods. C^1 convergence preserves them on the remaining compact subintervals. Hence q_i decreases strictly from t=0 to t=1, then increases strictly to t=2. Its exact minimum is g_i(Y_i), and its endpoint is positive since its limit is -4h_Y>0.

There are finitely many roots, so the same sufficiently large index works for all these paths, including S. Selecting the root attaining h_i provides an actual older path of exact minimum h_i. Thus normalized global death >=h_i. With the collar bound it equals h_i exactly. Even when two limiting saddle heights tie and the actual winning root switches, the finite collection of paths proves the same result.

On the actual global Morse distinct-value locus, the unique critical value h_i identifies the highest continued local saddle as the ordinary elder partner. Empty sectors select S exactly; nonempty sectors select one of the continued window saddles and preempt S. This proves Theorem E part3 and identifies the actual partner, not only its limiting height.

### A unique limiting position for almost every jet

For the position mark only, exclude D=0 as well. This is another nonzero polynomial zero set in the physical jet coordinates, hence Lebesgue null. When B!=0, (C9) gives

    (d/du)(P/k)=-1-(4s/B)u.

On the B>0 window conic this derivative is strictly negative (at its largest allowed u=u_w it is 1+2s/B<0); on the B<0 window conic it is strictly positive because u<-1/2 and s/B>1/2. Equal window heights therefore force the same u. If D!=0, the line s+Bu+DZ=0 then forces the same Z, so distinct window roots have distinct heights. For B=0 there is at most one window root. Accordingly outside this extra null set there is a unique highest cubic window point Y_*(theta) when n>0, and the actual elder partner's scaled position converges to it. Use S as the default position when n=0. This position exclusion is unnecessary for the exact finite-index death and partner conclusion above.

## 7. A compact-sector marked selection law under the actual tilt

This corollary uses only the planar compact-sector disintegration already displayed in [CUB] §4; it does not modify its count theorem.

For a compact Borel C in the typed domain, define the finite measure
dM_C(theta)=1_C(theta) z_0^(-1) w(theta) h_0(0,a,beta,c) dtheta,
with the full z_0 of [CUB] (G3), and define lambda(theta)=-h_*(P_theta)/k in (0,1].

Under the regression coupling [CUB] (G6)–(G8), Theorem E applies pathwise for almost every theta and almost every coupling realization. Define I_r=1{the global partner of M is not S} and D_r=(d_f(M)-b)/r^3. For every bounded measurable psi(theta), the marked identity
r^(-3) E_QW[psi(Theta_r) I_r; Theta_r in C]
  -> integral_C psi(theta) 1{n(theta)>0} dM_C(theta)
holds.

For every bounded continuous phi(theta,t),
r^(-3) E_QW[phi(Theta_r,D_r); Theta_r in C]
  -> integral_C phi(theta,h_*(theta)) dM_C(theta).
On the exceptional essential-class event define phi arbitrarily at D_r=-infinity; each good coupling eventually has an explicit local path to an older point, so that arbitrary choice disappears from the limit.

Proof: replace the count indicator in [CUB] (G10) by the Borel elder mark, or by the indicated bounded functional of the Borel maximin. The multiplier is
1_C(theta) (r^2/Z_r) h_r(rs,a,beta,c)
       E[(W_r/r^4) times mark].
Theorem E supplies pointwise convergence of the mark. Equations (G7)–(G9) supply the same integrable domination as before. Dominated convergence proves both statements. The first works for every bounded measurable psi because theta itself is not moved by the coupling and the failure indicator converges pointwise; this also yields total variation for the joint theta/Boolean measure on the compact sector. The real-valued death-height mark is asserted weakly, not in total variation.

The marked corollary gives a selection law on every fixed compact soft-jet sector. Compact convergence alone does not justify a full-global coefficient: it needs tightness of the rescaled *elder-failure measure*, rather than of the nonempty witness measure. The next section proves that tightness by retaining the rare scalar layer in the parent's cap-failure integral and explicitly converting endpoint control to the actual midpoint coordinates.

## 8. Full planar elder-failure tightness and global marked selection law

### 8.1. Fixed model and immutable interfaces

Fix the planar periodized Gaussian model, L>0, b in R, k>0 and one frame. Write Q_r for the exact six-pin regression at M_r=(-r/2,0), S_r=(r/2,0), heights b,b-kr^3 and zero gradients. Set
W_r=F_2(H_M)F_1(H_S), Z_r=E_Q W_r, dQ_r^W=(W_r/Z_r)dQ_r.
Let
F_r={the global ordinary superlevel elder partner of M_r is not S_r},
Theta_r=(f_zz(0)/r,f_xxz(0),f_xzz(0),f_zzz(0))=(s,a,beta,c),
D_r=(d_f(M_r)-b)/r^3.
The essential class uses d_f=-infinity. All event definitions are Borel by parent §8 and its reconciled §9 whole-field interface.

[P] is imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md at main commit 98fdb54954a2d9ac0b8ba8ca03e279701f70d751, blob dfed3b8d318a3ab1950957f393307733a4bef3f2. It is read WITH the congruence erratum, §9 Borel replacement, and reconciliation/W1/embedding rule in SOURCES.json. The consumed equations here are (3.5), (4.2)–(4.3), (5.5), (6.2), (7.5)–(7.7), and the good-cap implication in §8.

[CUB] is frontiers/planar_cubic_cluster_20260929/PROOF.md at the same main cut, blob bb446d08db8a944537a743ad550b88c1c2ad5758. The consumed equations are (C1)–(C14), Lemma S, (G1)–(G3), regression (G6)–(G9), physical midpoint disintegration (G10), and coefficients (G11) with finiteness (G13).

For theta=(s,a,beta,c), let P_theta be its pinned cubic, B=beta-a^2/(12k), D=(c-a beta/(4k)+a^3/(72k^2))/2, and D_k={s<-|B|/2}. Let n(theta) be the existing cubic classifier and
h_*(theta)=max({-k} union {P_theta(Y):Y is an additional window critical point}).
The function h_* is Borel: by Theorem E it is the cubic maximin, whose strict upper-level events have the same countable finite polygonal-path representation as [P] §8; each path stays in a compact plane region.
Extend it by a fixed value on the excluded polynomial sets and outside D_k when using an ambient test function. Those Borel sets have null or zero-weight contribution to the limiting failure measure, so the extension changes none of the identities.
Write
w_+(theta)=9k^2 [B-2s]_+ [-B-2s]_+.
This equals w(theta)=9k^2(4s^2-B^2) on D_k and is zero elsewhere, including its boundary.

Define the finite candidate limit measure
dmu_fail(theta)=z_0^(-1) w_+(theta) h_0(0,a,beta,c)
                       1{theta in D_k,n(theta)>0} dtheta.       (S1)
Here z_0 is the FULL normalizer limit [CUB] (G3), and h_0 is the actual raw midpoint Gaussian jet density under the exact contact law. No GOE substitution, adjacency normalization or extra pin-density factor appears.

**Theorem S (fixed planar selection law).** Conditional on Theorem E and the exact source interfaces above,
r^(-3) Q_r^W(Theta_r in ·,F_r) -> mu_fail
in total variation as finite measures on R^4. Consequently,
r^(-3)(1-p_r) -> alpha_1+alpha_2,                         (S2)
with alpha_j exactly [CUB] (G11).

Moreover, for every bounded continuous phi on R^4 x R,
r^(-3) E_QW[phi(Theta_r,D_r);F_r]
 -> integral phi(theta,h_*(theta)) dmu_fail(theta).       (S3)
Give the test an arbitrary bounded value on the essential-class event; that event has o(r^3) tilted mass. Thus the height-mark assertion is weak convergence, not total variation. After division by alpha_1+alpha_2>0 it is the actual conditional law given elder failure.

There is no claim about the unmarked full r^(-3) joint theta measure. Its typical s-coordinate escapes and its total mass diverges.

### 8.2. Good cap excludes failure

Let G_r be the parent's good cap. On the almost-sure Morse distinct-value locus, [P] §8 proves that the global ordinary partner is S on G_r. Hence
F_r subset G_r^c                                         (S4)
up to a Q_r^W-null set. This includes essential maxima: the good cap supplies a finite older endpoint, so the essential class cannot occur there.

This implication concerns the same actual global selector p_r as [P], not a new local adjacency event. It is the only place where the cap is used to contain the failure event.

### 8.3. Rare-layer tail bound from the independent endpoint residual

In the plane set lambda=-f_zz(M)>0 on typed support. Under [P] (4.2), the residual field g_r is independent of the scalar endpoint transverse Hessian. Write
J_r=1+||g_r||_(C4).
Its moments of every finite order are bounded along small-r sequences by (4.3). The bounded C4 regression coefficients and bounded mean in (4.2) give the pathwise inequality
||f||_(C4)<=C(J_r+lambda).                                (S5)
The mean and E_Q f_zz(M) terms are absorbed into C using the bounded fixed-parameter pin regression and J_r>=1.

Let D_cap>0 be the fixed scalar depth constant from [P] (7.5). By that split, depth failure is contained in
near: 0<lambda<=4D_cap rJ_r^2,
far: lambda>1/(4D_cap r).
On the near branch, r<=1 implies
||f||_(C4)<=C'J_r^2, M3<=C'J_r^2.                         (S6)

The m=1 typed weight bound (6.2) gives
W_r<=C r^2 J_r^4 lambda(lambda+C rJ_r^2)
on this branch. The density of lambda is bounded by (3.5), and J_r is independent of lambda. Retaining a tail restriction J_r>A in the SAME integration yields
E_Q[W_r;near,J_r>A]
 <= C r^2 E[ J_r^4 1{J_r>A}
           integral_0^(4D_cap rJ_r^2) lambda(lambda+C rJ_r^2) d lambda ]
 <= C r^5 E[J_r^10;J_r>A].
Divide by the FULL floor Z_r>=z_*r^2 from (5.5):
r^(-3) Q_r^W(near,J_r>A)
 <= C E[J_r^10;J_r>A].                                  (S7)
Higher moments of J_r imply the right side tends to zero as A increases, uniformly along small-r sequences.

The far branch (7.6) and the fourth-derivative exception (7.7) each have tilted mass O(r^4), hence o(r^3). Their union with the near branch covers G_r^c on typed support. Therefore the rare-layer tail estimate applies to F_r via (S4).

An unconditional C4 tail estimate followed by Cauchy–Schwarz would lose the rare factor. The retained scalar integral above supplies r^5 before division by the one full Z_r; this is why the tilted r^3 scale survives.

### 8.4. Explicit endpoint-to-midpoint control

Between M and the midpoint,
|f_zz(0)|/r <= lambda/r + M3/2
by the mean-value derivative bound. On the near branch,
lambda/r<=4D_cap J_r^2.
The other midpoint coordinates a,beta,c are third derivatives and are bounded by ||f||_(C3). Equations (S6) therefore imply
||Theta_r||<=C J_r^2.                                   (S8)

No density-coordinate replacement occurs here: (S8) is a deterministic control of the actual midpoint target by the scalar endpoint residual. Together with (S7) and the o(r^3) exceptions, it proves
lim_(T->infinity) limsup_(r->0)
 r^(-3) Q_r^W(F_r,||Theta_r||>T)=0.                       (S9)
The same proof gives
lim_(T->infinity) limsup_(r->0)
 r^(-3) Q_r^W(F_r,||f||_(C4)>T)=0.                        (S10)

Thus the leading failed population is ambient-midpoint-soft in the plane. Since there is only one transverse direction, bounded residual sectors force f_zz(M), f_zz(0), f_zz(S)=O(r), the last by (5.1). The axial and mixed endpoint entries are O(r) by (5.1)–(5.2), so both endpoints have the r^4 determinant-product scale. At finite r the far and fourth-derivative branches still exist; their smaller mass is retained above.

### 8.5. Compact-box disintegration, including the typed boundary

Fix an ambient compact box K_T in R^4. Although [CUB] states its count theorem on compact subsets of D_k, its actual regression construction (G6), moment bound (G7), Taylor convergence (G8), and determinant bound (G9) apply to ANY bounded midpoint target. They rely on the nonsingular joint covariance and bounded target, not on endpoint typing. No count convergence is invoked outside D_k.

Under this coupling, the endpoint Hessians divided by r converge to
H_M(P)=[[-6k,-a/2],[-a/2,s-beta/2]],
H_S(P)=[[6k,a/2],[a/2,s+beta/2]].
Their determinants are 3k(B-2s) and 3k(B+2s). Since the axial signs are fixed, the limiting typed weight is exactly
W_r/r^4 -> F_2(H_M(P))F_1(H_S(P))=w_+(theta).             (S11)
Each F_j is continuous even at a degenerate matrix: its determinant factor tends to zero there. Hence (S11) holds on the typed boundary as well, with zero weight. On the whole box the integrable envelope
W_r/r^4 <= C_T(1+||F||_(C4))^4                            (S12)
follows from the same endpoint Taylor bound as (G9).

The fixed-k algebraic exceptional sets
Sigma_k={12kD^2+(s-B)^2(B+2s)=0},
Delta_k={12kD^2+B^3=0}
are nonzero polynomial zero sets, hence null for the absolutely continuous midpoint density. No distinct-height exclusion is needed between the two window saddles.

For almost every theta in D_k and coupling realization, Theorem E gives
1_F_r -> 1{n(theta)>0},
D_r -> h_*(theta).
For theta outside D_k, including its boundary, no convergence of the selector is required: its bounded multiplier is killed by (S11). Thus [CUB]'s physical midpoint disintegration (G10), with the count mark replaced by the Borel global failure mark, gives the density
u_r(theta)
 = (r^2/Z_r) h_r(rs,a,beta,c)
          E[(W_r/r^4)1_F_r].                             (S13)
The one factor r in (S13) comes from f_zz(0)=rs. It is not a spectral/endpoint change of variables. The prefactor is r^(-3)*r*r^4/Z_r=r^2/Z_r.

By (S11)–(S12), the full normalizer limit, local boundedness of h_r, and dominated convergence in theta and F,
integral_(K_T) |u_r(theta)-u_0(theta)| dtheta -> 0,
u_0(theta)=z_0^(-1) w_+(theta) h_0(0,a,beta,c)
                                  1{n(theta)>0}.        (S14)
Here define the final indicator arbitrarily off D_k, where w_+=0.

This simultaneously handles thin typed-boundary neighborhoods and the exceptional polynomial sets; neither can carry an unidentified atom of the leading failure measure.

### 8.6. Exhaustion gives global total variation and the coefficient

The limiting density u_0 is integrable. It is exactly the sum of the two nonempty coefficient densities (G11), whose integrability follows from [CUB] (G13) and Gaussian polynomial tails. Its total mass is alpha_1+alpha_2, finite and strictly positive.

Choose T large. On K_T, the L1 error tends to zero by (S14). Outside K_T, the actual density's mass is controlled by (S9), and the limiting density's mass tends to zero by integrability. Therefore
integral_(R^4) |u_r-u_0| dtheta -> 0.
This is total-variation convergence of the finite failure measures (under either conventional factor in the TV norm), proving Theorem S and (S2).

The proof exhausts only the marked failure measure. It never integrates the divergent n=0/unmarked total soft-jet measure and never asserts an uncentered r^(-3) probability law.

### 8.7. The normalized death mark on actual failure

For a bounded continuous phi(theta,t), use (S13) with multiplier
1_F_r phi(theta,D_r).
On every ambient compact box the same domination applies. Theorem E gives pointwise convergence on typed generic theta to
1{n(theta)>0} phi(theta,h_*(theta));
outside the typed domain the zero weight suffices. Dominated convergence gives the compact-box marked limit.

The bounded test's omitted actual mass is at most ||phi||_infinity times the failure tail in (S9). The limiting omitted mass is controlled by the integrable u_0. Exhausting boxes proves (S3).

The essential-class mark has zero scaled limit: on a good typed cubic coupling Theorem E's finite critical-chord path supplies a local point above the birth for all small r, and outside the typed domain the weight limit is zero. The compact-box domination and (S9) again exhaust the actual essential-failure mass. Thus it is o(r^3).

Normalizing (S3) by (S2) identifies the weak actual conditional failure-height law. This is not a density result for persistence lifetimes, not a rate, and not a spatial or real-height TV assertion.

### 8.8. Actual replacement location and the lifetime mark

Let T_r be the actual elder partner's coordinates divided by r in a fixed embedded midpoint chart. Give it a sentinel value when the partner is outside the chart or the class is essential. Theorem E part3 proves that on every generic typed coupling the partner is eventually a continued local window saddle on failure. Outside the additional null set D=0, it is the continuation of the unique highest root Y_*(theta), so

    T_r -> Y_*(theta),               D_r -> h_*(theta).

This is an actual partner assertion; no witness factorial pair is relabelled. The functions Y_* and h_* are Borel on the generic typed domain: the finitely many nondegenerate roots continue continuously locally, and strict height comparison selects a unique root. Arbitrary Borel extensions on the excluded sets have zero limit mass.

For every bounded continuous test phi(theta,y,t), the same compact-box domination as S13, followed by the actual failure-tail bound S9, gives

    r^(-3) E_QW[phi(Theta_r,T_r,D_r);F_r]
      -> integral phi(theta,Y_*(theta),h_*(theta)) dmu_fail(theta).

Give bounded tests arbitrary values at either sentinel. On compact good couplings those sentinel events eventually vanish, and S9 exhausts their omitted failure mass. In particular their tilted mass is o(r^3). The joint location/death assertion is weak convergence. Dividing by the positive total mass alpha_1+alpha_2 identifies the genuine conditional replacement-partner law under the original pair-Palm law given failure.

The corresponding normalized actual lifetime on failure is

    (b-d_f(M))/r^3 -> -h_*(theta) in (0,k),
    lambda(theta)=-h_*(theta)/k in (0,1).

Its law is the pushforward of mu_fail/(alpha_1+alpha_2); thus the local geometry determines which saddle pairs and its lifetime under this specified law. This is not an intensity obtained by duplicating rejected candidates attached to the same maximum.

The weak finite replacement-location measures have converging total masses and a finite limit on R^2, hence they are tight. Therefore for every deterministic cutoff delta_r with delta_r/r->infinity,

    Q_r^W(F_r, dist(partner(M),midpoint)>delta_r)=o(r^3).

For the proof, first fix a large scaled radius A, use tightness outside A, and then use delta_r/r>A for all sufficiently small r; let A increase. The o(r^3) sentinel mass is included. No growing-radius uniform root enclosure is asserted or needed. This localizes the **actual failed elder pairing**; it neither needs nor promotes the contextual factorial-count localization results.

## 9. A compact rejected-candidate lifetime coefficient

The local-to-elder bridge is now supplied by Theorem E and the full marked failure limit S2, rather than postulated from a count theorem. One precise lifetime consequence follows by consuming the parent's *existing* compact-parameter domination; no new uniform convergence theorem is needed.

Retain exactly [P] §§10–12's populations: candidate maximum/saddle pairs and the selected subset, per unit midpoint volume, with birth b in a compact interval B and positive gap mark k in a compact interval K, both intervals of positive lengths and K bounded away from zero, and directed orientation u in S^1 with ordinary arc measure. Write

    A_r(b,k,u)=12 pi_r(u;v_r) Z_r(b,k,u)/r^2,
    A_0=12 pi_0(u;v_0) z_0(b,k,u),
    a_fail(b,k,u)=alpha_1(b,k,u)+alpha_2(b,k,u)>0.

For every fixed (b,k,u), S2 identifies

    (1-p_r(b,k,u))/r^3 -> a_fail(b,k,u).

The source [P] (7.8), with its compact parameter hypotheses, bounds this ratio by a common finite constant for all sufficiently small r, b,k and frames in these compacts. Equations (10.2)–(10.3) bound A_r uniformly and identify its limit. These are already-displayed source bounds, not uniformity deduced from our pointwise cubic topology theorem. The conditional a_fail is Borel as the limit of Borel quantities, and is bounded by that same cap constant.

Let nu_rej^{B,K}(ell)=nu_cand^{B,K}(ell)-nu_eld^{B,K}(ell) denote the density of the **nonselected candidate counting measure**, in the parent's canonical Kac–Rice versions. With r=(ell/k)^(1/3), [P] (11.1)–(11.2) give exactly

    ell^(-2/3) nu_rej^{B,K}(ell)
      = integral_(B x K x S^1)
          [A_r(b,k,u)/(3k^(5/3))]
          [(1-p_r(b,k,u))/r^3] db dk d sigma(u).

The common compact bounds dominate this integrand by an integrable constant, because k is bounded below and the integration domain has finite measure. Pointwise convergence and dominated convergence prove

    nu_rej^{B,K}(ell) ~ C_fail^{B,K} ell^(2/3),
    C_fail^{B,K}=integral_(B x K x S^1)
                  A_0 a_fail/(3k^(5/3)) db dk d sigma(u).

The coefficient is finite and is strictly positive when B and K have positive lengths. It is an identified Gaussian integral, not a numerical estimate. The original full z_0 cancels if the integrand is written as

    A_0 a_fail/(3k^(5/3))
      = 4 pi_0(u;v_0) k^(-5/3)
          integral_(D_k) w(theta) h_0(0,a,beta,c)
                                    1{n(theta)>0} dtheta.

There is still only one original pin density, one determinant weight and one full normalizer. By direct integration,

    E N_rej^{B,K}(0,t] ~ (3/5) C_fail^{B,K} t^(5/3).

This is a sharp coefficient for the selected-versus-candidate **difference** on the exact compact-mark population. It is not a separate second-order expansion of nu_eld: the convergence of A_r itself has not been given an expansion here. It is also not a density of replacement elder bars obtained by counting every rejected candidate. One actual maximum can participate in several rejected candidate pairs; doing that pushforward would require the appropriate de-biasing/selection identity. Theorem S3 instead identifies the actual death-height law under the specified candidate pair-Palm law conditioned on failure, which is a different, well-defined estimand.

No unrestricted version of this difference asymptotic is inferred. [U] already proves a positive far rejected density and excludes such an inference. No k down to zero limit, new parameter uniformity, higher-dimensional lift or numerical coefficient is added.

## 10. Hypotheses, exclusions and falsifiers

The deterministic Theorem E assumes the exact displayed planar cubic, k>0, strict endpoint typing, Sigma_k and Delta_k excluded, pinned C^2 convergence on every fixed disk, and embedded shrinking charts. Exact partner statements additionally assume the actual global Morse distinct-value locus. Only the unique limiting position mark additionally excludes D=0; exact finite-index partner identification permits tied limiting heights. It does not need Morse–Smale or a separatrix identification.

The Gaussian statements consume the exact original six-pin regression, full Z_r, nonsingular finite contact-jet covariance, full-field conditional C^4 moment coupling, and the reviewed cap implication/integration interfaces of [P] with all three reading rules. The algebraic exclusions are Lebesgue null, not discarded positive-probability events. The tightness proof includes the scalar large-lambda and fourth-derivative branches as o(r^3), handles the typed boundary by continuous determinant weight, and keeps all random-field correlations. Theorem S concerns fixed planar marks. Section9 uses only the parent's already uniform compact-mark bound for its explicitly restricted lifetime difference.

The following would falsify the corresponding new step:

* A generic typed displayed cubic whose maximin level differs from h_*, or a pinned local C^2 sequence on compact surfaces whose actual death fails to approach h_*, falsifies Theorem E. A sequence with no cubic window saddle but eventual preemption of S would specifically falsify its exact empty-sector argument.
* A failure of the cap's global older-path implication, or of the endpoint-independent residual and rare scalar integration with the original W_r/Z_r, would invalidate S4–S9 and reopen full failure exhaustion.
* A leading failure mass escaping every bounded midpoint-jet box would contradict S9; a nonzero leading typed-boundary mass would contradict S11–S14. These are explicit measure claims, not inferences from tests or finite samples.
* An erroneous Jacobian/full normalizer in G10 or the parent's radial lifetime ledger would invalidate the corresponding marked/lifetime identities. Unrestricted or replacement-bar uses of Section9's compact rejected-candidate coefficient are outside its scope.

The new scientific candidate is the planar local-to-global actual elder partner, full rescaled selector-failure law, joint conditional replacement location/death/lifetime law, and compact rejected-candidate lifetime coefficient. Mixed factorial pairs remain two additional saddle witnesses rather than max/saddle persistence pairs. Higher-dimensional replacement geometry and any unrestricted refined lifetime law remain unproved by this note. Source-bound review and publication do not change any controlling status, graph, prize, premise or parent acceptance.
