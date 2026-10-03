# Counting rare replacement bars once

Object: OA-UNIQUE-REPLACEMENT-BAR-20261001-v1. Authors: OpenAI/Codex `/root`, `/root/c50_multiplicity_feasibility` and its `boundary_nullity` contributor, under Dylan Roy's delegation. This is an additive source-bound mathematical candidate. Technical review, imported-source acceptance, organizational independence and scientific acceptance remain separate. Scientific effect NONE; no controlling status is changed.

## 1. Model, population and the result

Fix the planar torus `T_L^2`, with `L>0` fixed before all limits, and the centered unit-variance Gaussian field with covariance

```
K_L(z) = sum_(n in Z^2) exp(-|z+Ln|^2/2)
         / sum_(n in Z^2) exp(-|Ln|^2/2).
```

Use ordinary superlevel H0 persistence with distinct critical values: a finite bar is indexed by its birth maximum `M`, its actual global elder partner `S_*(M)`, and death `d_f(M)=f(S_*(M))`. Its length is `f(M)-d_f(M)>0`. Exclude the essential global-maximum class. Work on the almost-sure Morse/distinct-value locus supplied by [P,REC]; give all expressions value zero off it. No Morse–Smale, branch-adjacency or separatrix convention is substituted.

Fix intervals `B=[b_-,b_+]`, `K=[k_-,k_+]` of positive lengths, with `0<k_-<k_+<infinity`, and constants `0<c_0<C_0<infinity`. All these parameters, including L, remain fixed. For `h>0` small enough that `C_0 h<L/4`, let

```
D_h(M) = #{index-1 saddles S:
   c_0 h <= dist(M,S) <= C_0 h,
   (f(M)-f(S))/dist(M,S)^3 in K,
   S != S_*(M)}.
```

This is a count of rejected **maximum/saddle candidates**, with M fixed, not a count of extra window witnesses or of ascending branches. For a finite maximum only, define the mark

```
V_h(M) = ( f(M), disp(M,S_*(M))/h,
           (f(M)-d_f(M))/h^3 ).
```

Here `disp` is the Borel shortest torus displacement in a fixed half-open fundamental square; ties use a fixed rule. For local candidates the short displacement is unique. Remote partner marks may cross the chart boundary at finite h; the proof below controls their failure mass and does not discard them beforehand.

For bounded continuous `Phi: B x R^2 x [0,infinity) -> R`, set

```
I_h(Phi) = L^-2 E sum_(finite maxima M,
                        f(M) in B, D_h(M)>0) Phi(V_h(M)).       (1)
```

Each actual bar is counted once. The shrinking selection concerns its rejected candidates; it does not impose the same distance/gap cutoff on its actual partner. This is an expected intensity, not sampling a field conditioned on having such a bar.

The source quantities used in the theorem are defined in §3. Conditional on the exact imported interfaces in §2, the new conclusion is

```
h^-5 I_h(Phi) -> C_U(Phi),                                  (2)

C_U(Phi) = integral_(B x K x S^1) integral_(c_0)^(C_0)
 t^4 A_0(b,k,u)
 integral [ Phi(b, t R_u(Y_*-M_0), -t^3 h_*) / D_(t,k)(theta) ]
          d mu_fail^(b,k,u)(theta)
 dt db dk d sigma(u).                                       (3)
```

`sigma` is ordinary arc measure, and `R_u=(u,Ju)` is the oriented orthonormal frame, with J the counterclockwise quarter-turn. The limit integrates only the nonempty typed failure sector. On its generic part, `D_(t,k)` is either 1 or 2. With `C_R` the corresponding coefficient obtained by replacing `1/D` by 1,

```
0 < C_R/2 <= C_U(1) <= C_R < infinity.                       (4)
```

Thus `I_h(1) ~ C_U(1) h^5`. Formula (3) identifies a finite weak limiting measure in the displayed birth/location/lifetime variables. It does not assert a density in any of those variables, a rate, finite-h moment convergence, all-mark exhaustion, an infinite-volume limit, or a higher-dimensional result.

## 2. Exact dependencies and division of work

All consumed files are pinned at Math commit `044d42d5bd7f31df6f7e6b9034d6711e8fb7ee43` in SOURCES.json. The historical source headers are preserved, not treated as current acceptance decisions.

- **[P]** `imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md`: §§1–5 for model, regression and one full normalizer; (7.8) for the uniform compact-parameter failure bound; §§8–10 for the global selector, marked pair measure and `r A_r dr` ledger. Read with **[CAP]** the marked cylinder-cap proof, **[E1]** the congruence erratum, **[E2]** the full-field Borel Section9 repair, and **[REC]** the reconciliation's W1/embedded-chart and source-reading rules. These are retained analytic inputs, not re-proved or newly accepted by this paper.
- **[CUB]** `frontiers/planar_cubic_cluster_20260929/PROOF.md`: the pinned cubic and conic/line equations; nonsingular joint jet and positive Gaussian density; conditional full-field coupling (G6)–(G9), physical jet disintegration (G10), positive finite failure-sector integrals (G11)–(G13).
- **[ELDER]** `frontiers/local_elder_geometry_20260930/PROOF.md`: Theorem E for exact eventual actual partner identification, §§8.3–8.6 for the original weighted failure-tail exhaustion and determinant envelope, §8.8 for partner marks, §9 for the already supplied compact parameter bounds. In particular its §9 explicitly does not count each replacement bar once.

The new work is the reciprocal counting identity and its legitimate whole-field mark, all-root and cutoff stability in ROOTS.md, their insertion into the existing disintegration, and radial integration. The endpoint law in `frontiers/short_bar_endpoint_law_20261001/PROOF.md` is contextual: it already concerns ordinary finite bars, but its leading law does not identify this h^5 rare subset. Neither it nor a factorial-moment bound substitutes for the present count correction.

## 3. Cubic notation and the exact multiplicity

Under the six endpoint pins use midpoint coordinates with `M_0=(-1/2,0)`, `S_0=(1/2,0)`, heights `0,-k`. The limiting cubic is

```
P_theta(X,Z)=2kX^3-3kX/2-k/2+sZ^2/2
 +(a/2)(X^2-1/4)Z+(beta/2)XZ^2+(q/6)Z^3,
theta=(s,a,beta,q),
B_s=beta-a^2/(12k),
D_s=(q-a beta/(4k)+a^3/(72k^2))/2,
T_k={s<-|B_s|/2}.
```

The subscripts on `B_s,D_s` distinguish shear coefficients from the birth interval and multiplicity. Let `n(theta)` count the extra critical points in `-k<P_theta<0`. On `T_k` outside the algebraic null sets in [ELDER] and ROOTS.md, if n>0, let `Y_*` be the unique highest window saddle and `h_*=P_theta(Y_*)`. Then `-k<h_*<0`; [ELDER] identifies the actual global partner with its continuation under the coupled fields.

For `c_0<t<C_0`, `k_-<k<k_+`, count **all** cubic saddles, including those below `-k`:

```
D_(t,k)(theta) = #{saddle roots Y of grad P_theta=0:
   P_theta(Y)<0, Y != Y_*,
   c_0 <= t |Y-M_0| <= C_0,
   -P_theta(Y)/|Y-M_0|^3 in K}.                            (5)
```

Distances in (5) are in the original Euclidean `(X,Z)` coordinates, never the sheared coordinates. The pinned S_0 has distance 1 and normalized gap k; on failure it is rejected, so (5) is at least one. There are at most four cubic critical points: the maximum, the pinned saddle and two additional roots. Excluding the actual partner leaves at most two rejected saddles. ROOTS.md supplies the all-root proof rather than extrapolating the window classifier. Define `1/D=0` on exceptional sets or if D=0; these definitions carry no limiting mass. At finite h the denominator is at least one whenever the sampled admissible pair is rejected and its maximum is finite.

With the original full normalizer `Z_r=E_Q W_r`, define exactly as in the sources

```
z_0=lim Z_r/r^2,
w(theta)=9k^2(4s^2-B_s^2) on T_k,
d mu_fail = z_0^-1 w(theta) h_0(0,a,beta,q)
             1_{T_k,n>0} ds da d beta dq,
A_r=12 pi_r Z_r/r^2,       A_0=12 pi_0 z_0.                (6)
```

Here h_0 is the full midpoint-jet Gaussian density conditional on contact `(b,0,0,12k,0,0)`; its correlations, b,k,u,L dependence are retained. In (3), `A_0 dmu_fail=12 pi_0 w h_0 1_{T_k,n>0}dtheta`: exactly one z_0 cancels. There is no extra pin density, factor 1/2, GOE replacement or adjacency normalization.

## 4. Exact once-per-bar identity and measurability

A Morse function on a compact torus has finitely many critical points. For each eligible finite maximum M, the summand `Phi(V_h(M))` is independent of which rejected candidate S is used to represent it. Therefore, pathwise,

```
sum_(finite M, f(M) in B, D_h(M)>0) Phi(V_h(M))
 = sum_(admissible rejected (M,S), M finite)
       Phi(V_h(M))/D_h(M).                               (7)
```

There are D_h(M) equal terms on the right for that maximum. This identity works for signed bounded Phi; there is no independence assumption about different candidates. Essential maxima appear on neither side.

The marked Kac–Rice use of (7) is legitimate. Around any C2 Morse function on the compact torus, its finitely many critical roots have continuous local charts, their inertia is constant, and the remaining compact set has a gradient floor. A sufficiently small C2 neighborhood has exactly these roots. The separable C2 function space admits a countable subcover of these neighborhoods. On each neighborhood, distance, heights and normalized positive-distance gaps of each pair are continuous. The global elder death is Borel by [P,E2]; finiteness and partner inequality are Borel. Consequently each finite root sum defining D_h and the actual-partner mark is Borel. Overlapping root enumerations give identical counts. Extending by zero off the Borel Morse/distinct-value locus gives a whole-field Borel mark. With the zero-denominator convention, its absolute value in (7) is bounded by `||Phi||_infinity`.

Apply [E2]'s equality of finite measures on compact pair domains separated from the diagonal, then its height disintegration and [P]'s exact radial ledger. For each fixed h the radial band is separated from zero; its expected pair count is finite by the uniform bound on A_r. Translation invariance turns the midpoint integral into L²; hence the per-volume identity is

```
I_h(Phi)= integral_(B x K x S^1) integral_(c_0 h)^(C_0 h)
 r A_r E_QrW[1_F 1_finite Phi(V_h(M))/D_h(M)]
 dr db dk d sigma(u),                                    (8)
```

where F is failure of the sampled saddle to be the actual global partner. The same full `W_r/Z_r` is used in (6) and (8). Signed tests follow by subtraction of their nonnegative parts. No unordered pair multiplicity is introduced: maximum/saddle roles order the pair, and u records its directed separation.

## 5. Joint multiplicity stability at fixed outer parameters

Put r=th. For almost every `(t,k,theta)` under Lebesgue measure with t,k in their intervals, ROOTS.md proves:

1. Every finite cubic critical point is nondegenerate outside an explicit nonzero-polynomial null set. The actual candidates lie in the fixed scaled disk `|Y-M_0|<=C_0/t<=C_0/c_0`; all roots in an enlarged fixed disk continue, and the compact complement has a gradient floor. Thus there are no unaccounted roots inside the admissibility band. This is fixed-disk C2 stability, not a growing-domain assertion.
2. The boundaries `t|Y-M_0|=c_0,C_0` are null by integrating t. The normalized-gap endpoint boundaries are null by positive simultaneous scaling of `(k,s,a,beta,q)`: roots stay fixed and each positive normalized gap scales strictly. The integrated joint jet measure is absolutely continuous in those variables. The conclusion is joint almost-everywhere stability; no assertion at every fixed k is required.
3. On the failure sector, [ELDER] gives the eventual actual partner among the continued roots. Its exclusion in D_h therefore stabilizes jointly with all cutoff memberships. In particular `D_(r/t)(M)->D_(t,k)(theta)` (eventually equality of integers), and the actual scaled mark tends to `(b,t R_u(Y_*-M_0),-t^3 h_*)`.

The retained null sets include the source Sigma_k, Delta_k, D_s=0 and the all-root Hessian discriminant in ROOTS.md. They are excluded only under absolutely continuous integration. A zero-probability exact degeneracy has not been used to assert a quantitative near-degeneracy rate. Such a rate is unnecessary for bounded marked convergence with the source envelope.

## 6. Weighted disintegration and actual-failure exhaustion

Fix a generic `(t,k)` and b,u. Use the full-field regression coupling [CUB G6] on an ambient compact theta box. It preserves the six pins and satisfies C2 convergence on every fixed disk and the C4 moment envelope. On the generic typed domain, the previous section and [ELDER E] give pointwise convergence of the bounded multiplier

```
G_r = 1_F 1_finite Phi(V_(r/t)(M))/D_(r/t)(M)
 -> 1_{n>0} Phi(b,t R_u(Y_*-M_0),-t^3 h_*)/D_(t,k).
```

On the typed complement no selector convergence is needed: the limiting typed determinant weight is zero. On its boundary the same follows from continuity of determinant times inertia, as in [ELDER S11]. The physical midpoint change `f_zz(0)=rs` has Jacobian r, so the rescaled marked integral has density

```
(r^2/Z_r) h_r(rs,a,beta,q) E[(W_r/r^4) G_r].              (9)
```

This is `r^-3 * r * r^4 / Z_r`, not an extra Palm renormalization. The envelope `W_r/r^4 <= C_T(1+||F_0||_C4)^4` from [ELDER S12], bounded local densities, and the normalizer floor dominate (9). Compact-box dominated convergence gives the desired limit with the reciprocal mark. Weak convergence of the old location/death marginal alone would not justify this discontinuous root-count mark; (9) supplies the new argument.

Now exhaust theta boxes. The omitted actual contribution is at most

```
||Phi||_infinity r^-3 Q_r^W(F,||Theta_r||>T),
```

which vanishes in the iterated limit by [ELDER S9]. The limit tail is bounded by `||Phi||_infinity mu_fail(||theta||>T)`, which vanishes by [CUB G13]. This proves

```
r^-3 E_QrW G_r -> integral Phi(b,t R_u(Y_*-M_0),-t^3 h_*)
                                  /D_(t,k) dmu_fail.     (10)
```

The essential class and any out-of-chart actual partner have no limiting contribution: they disappear on every generic compact coupled sector by [ELDER E], and the same actual-failure exhaustion controls their remainder. They were included until this bound, not removed by a presumed local/global equivalence.

The sequence formulation of the source coupling suffices: prove (10) along each sequence r decreasing to zero, with exceptional null sets handled under the corresponding integrals. No common probability-one event over uncountably many pins or parameters is asserted.

## 7. Radial limit, coefficient, and what changes

Substitute r=th in (8). Exactly,

```
h^-5 I_h(Phi)= integral_(B x K x S^1) integral_(c_0)^(C_0)
 t^4 A_(th) [(th)^-3 E_Q(th)W G_(th)] dt db dk d sigma(u). (11)
```

The exponent ledger is the parent's `r dr` times the rare-failure factor `r^3`, hence `r^4 dr=h^5 t^4 dt`. The bounded reciprocal introduces no power and no singular denominator. It corrects counting rather than changing the rare-event order.

By [P (7.8)], `|r^-3 E G_r|<=C ||Phi||_infinity` uniformly on these compact b,k,u ranges for sufficiently small r. By [P (10.3)], A_r has a common finite bound and converges to A_0. Since t lies in a compact interval bounded away from zero, the right side of (11) has an integrable common majorant. Joint boundary nullity plus Fubini permits (10) for almost every outer t,k, and dominated convergence proves (2)–(3). The limit order is: fix L,B,K,c_0,C_0; compact-box coupling limit r→0 at fixed t; exhaust theta boxes using S9/G13; integrate fixed outer variables using the common source bound. No limit L→infinity or K→(0,infinity) is taken.

For Phi=1, the coefficient without reciprocal is

```
C_R=((C_0^5-c_0^5)/5)
     integral_(B x K x S^1) A_0(b,k,u)(alpha_1+alpha_2) db dk d sigma(u).
```

It is finite and positive by the imported bounds and positive failure-sector density. Since `1/2<=1/D<=1` almost everywhere on that sector, (4) follows. The coefficient is an identified Gaussian/angular integral; no numerical enclosure is supplied. In general the reciprocal depends on t,k and the full cubic, so multiplying C_R by an arbitrary constant (for example 1/2) is not justified. ROOTS.md supplies exact open-set fixtures with D=1 and D=2 for one fixed choice of bands, demonstrating that both multiplicities can matter.

This closes, conditional on the explicitly retained analytic interfaces, the compact-band unique-count consumer left open by [ELDER §9]. It does not close all shrinking-witness, occurrence-conditioned or per-field cluster questions. In particular the limit describes intensity-weighted selected bars; dividing by its total mass gives that limiting intensity-normalized mark law, not the law of a bar sampled uniformly after conditioning a random field to contain one.

## 8. Review and falsification targets

Review A: pathwise identity and Borel full-field mark; Review B: ROOTS all-root and null-boundary proofs; Review C: physical disintegration, failure exhaustion, outer domination and normalization. A fresh nonauthor review must bind exact files and consumed source slices; no same-author calculation counts as peer review.

Useful falsifiers include a generic admissible cubic with an uncounted extra critical root; a non-null membership boundary under the actual integrated measure; a finite bar counted with weights summing differently from one; a near-layer tail escaping the source S9 bound; or a second normalizer/pin-density inserted in (8)–(11). The supplied exact script checks finite algebra and count fixtures, with deliberately wrong alternatives. It does not prove the continuum coupling, imported cap theorem, or domination. Those are analytic obligations of this proof and its named dependencies.
