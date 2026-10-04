# From replacement-bar intensity to field occurrence

Object: OA-REPLACEMENT-BAR-OCCURRENCE-20261001-v1.
Authors: OpenAI/Codex root and c51_excess_feasibility, under Dylan Roy's delegation.
This is a conditional mathematical candidate. It does not change scientific status.
The source identities, including the unmerged C50 candidate, are fixed in SOURCES.json.

## 1. Fix the observable before taking a limit

Use exactly [U50, §1]: the centered unit-variance periodized Gaussian field on the
fixed planar torus T_L²; ordinary finite superlevel H0 bars indexed by their
birth maximum M; the actual global elder death saddle S_*(M); and exclusion of
the essential global maximum. Fix L, a positive-length compact birth interval
B, a positive-length compact K=[k_-,k_+] with k_->0, and 0<c0<C0.
All remain fixed before h decreases to zero. No isotropy of the torus is assumed.

Let D_h(M) count the index-1 saddles S satisfying

    c0 h <= dist(M,S) <= C0 h,
    (f(M)-f(S))/dist(M,S)^3 in K,
    S != S_*(M).

Let A_h(f) be the finite set of finite maxima M with f(M) in B and D_h(M)>0,
and N_h=|A_h(f)|. Work on the almost-sure Morse/distinct-value locus and assign
these quantities zero off it. Define V_h(M) exactly as in [U50]:

    V_h(M)=(f(M), disp(M,S_*(M))/h, (f(M)-f(S_*(M)))/h³).

The displacement uses U50's fixed half-open shortest torus chart. There is no
additional cutoff on the actual partner. Distinct maxima give distinct finite
bars. N_h does not count multiple rejected saddles for the same maximum.

Write C_U(Phi) for the coefficient in [U50, (3)], and
lambda_U=L² C_U(1)>0. U50 supplies, for bounded continuous Phi,

    E sum_(M in A_h) Phi(V_h(M))
       = L² C_U(Phi) h^5 + o(h^5).                       (O1)

This is a first moment. The new question is whether the same leading mass is
carried by fields with exactly one selected bar.

## 2. The conditional theorem and exact dependencies

**Theorem O.** Conditional on [U50] and its retained analytic interfaces,
for the population just fixed,

    E[N_h 1{N_h>=2}] = o(h^5),                            (O2)
    E[(N_h-1)_+] = o(h^5).                               (O3)

Consequently,

    P(N_h>0) = lambda_U h^5 + o(h^5),                    (O4)
    Law(N_h | N_h>0) -> delta_1 in total variation.       (O5)

For the experiment which first conditions a field on N_h>0 and then chooses
one of its N_h selected bars uniformly, its mark has the weak limit

    E[ N_h^-1 sum_(M in A_h) Phi(V_h(M)) | N_h>0 ]
        -> C_U(Phi)/C_U(1).                              (O6)

The zero-denominator expression is defined as zero when N_h=0 before
conditioning. Formula (O6) is for every bounded continuous Phi on
B x R² x [0,infinity). It does not assert total-variation convergence of marks.

[U50] is the exact source at published head
b5bf02879a5645da9a69d9944dee610e6bb14bf6: PROOF.md and ROOTS.md are reproduced
unchanged under sources/c50 with their original source map. At candidate
creation this parent is reviewed but still an unmerged draft; consuming it is
an explicit mathematical hypothesis, not an integration or acceptance claim.

Its seven underlying sources [P,CAP,E1,E2,REC,CUB,ELDER] are pinned at
044d42d5bd7f31df6f7e6b9034d6711e8fb7ee43. In particular:

- [P, §§2–4]: positive Fourier spectrum, distinct finite derivative rank,
  nonsingular averaged contact frame, and global smooth Gaussian regression.
  The rank and mesh argument in §8 is used at a new full-contact conditioning;
  GLOBAL.md gives that argument explicitly instead of quoting pinned Morse
  genericity at a different conditioning.
- [CUB, G6–G10]: the full-field ten-jet coupling, physical midpoint-jet density,
  compact-sector C4 envelope and r^4 determinant scaling.
- [ELDER, S9 in §8.3 and the subsequent determinant bounds]: exhaustion of the
  *actual weighted failure* outside compact soft-jet boxes. This is not inferred
  from finiteness of a limiting integral.
- [U50, §§4–7]: Borel reciprocal counting, exact pair/radial formula, its outer
  uniform bound and the positive finite coefficient. [U50 ROOTS] supplies the
  generic all-root nondegeneracy and finite cubic critical set.

GLOBAL.md proves the new deterministic and Gaussian mechanism needed for (O2).
The rest of this note inserts it into the existing weighted integral and
derives the probability consequences. No new joint Kac–Rice integrability,
independence between regions, factorial bound or inverse Hessian moment is
assumed. Existing analytic-source hypotheses and acceptance boundaries remain.

## 3. The pathwise mechanism

Fix b,k,u and an interior t in [c0,C0]; put r=t h. In the full-field coupling,
fix generic theta=(s,a,beta,q) on the typed sector. GLOBAL.md proves:

    N_(r/t)(f_r^theta) <= 1 eventually as r -> 0,         (O7)

almost surely under that coupling. The threshold may depend on the complete
coupled sample, theta, t and the outer parameters; no uniform random threshold
is claimed or needed.

There are three essential pieces. The contact-conditioned limit is almost
surely Morse away from its single forced degenerate point. A quantitative
Taylor bound excludes critical points at every intermediate distance
Rr <= |x| <= delta, with R finite and delta positive selected for that sample.
Inside Rr all critical points continue from the generic pinned cubic, whose
affine Hessian permits at most one strict local maximum. Outside delta,
ordinary C2 structural stability gives finitely many separated critical roots;
for small h none can form a pair at distance at most C0 h.

Thus all admissible rejected pairs must use the single possible local
maximum. This is a statement about the actual field's critical points, not a
statement that a cubic describes the field on a growing disk. No candidate
cutoff-boundary convergence is needed for (O7): the global number of maxima
capable of having a nearby saddle is at most one before applying B or K or the
actual-elder rejection mark.

## 4. A bounded whole-field mark, not a second-moment calculation

For each fixed h, define H_h(f)=1{N_h(f)>=2}. The root-chart/Borel argument in
[U50, §4] makes N_h and H_h Borel on the full field space. Every Morse function
on the compact torus has finitely many critical points, so these are ordinary
finite sums. Extend by zero off the stated Borel generic locus.

The exact pathwise reciprocal identity remains valid with this global mark:

    N_h H_h
      = sum_(admissible rejected (M,S), M finite)
                         H_h / D_h(M).                  (O8)

The denominator is positive on every summand and 1/D_h<=1. Multiplication by
H_h preserves the full-field Borel property. It does not introduce a second
selected maximum into the Kac–Rice pin list and it assumes no independent
relationship between H_h and the pinned field.

Set J_h=L^-2 E[N_h H_h]. The same marked finite-measure identity [E2] used by
U50 gives, with its ordered maximum/saddle convention,

    J_h = integral_(B x K x S1) integral_(c0 h)^(C0 h)
          r A_r E_QrW[1_F 1_finite H_h / D_h(M)]
          dr db dk d sigma(u).                          (O9)

Here F is failure of the sampled saddle to be the actual elder partner,
A_r=12 pi_r Z_r/r², and QrW is the *original* weighted pin law W_r/Z_r.
There is no extra full-field probability normalization. The midpoint
integration is L² and has already been divided out in J_h. The integrand is
bounded by the one-failure integrand, so its finiteness follows from the same
compact-parameter bounds as U50.

## 5. Vanishing within the physical weighted disintegration

Keep t,b,k,u fixed. Define the bounded mark under the pin law

    G_r=1_F 1_finite H_(r/t) / D_(r/t)(M),  0<=G_r<=1_F.

Disintegrate the physical midpoint jet as in [CUB G10; U50 (9)] with
f_zz(0)=r s. On a compact theta box, the rescaled marked density is

    (r²/Z_r) h_r(rs,a,beta,q)
                  E[(W_r(f_r^theta)/r^4) G_r(f_r^theta)]. (O10)

This expression already includes the Jacobian r of f_zz=r s. It has precisely
the scaling r^-3 times r times r^4 divided by Z_r. No second normalizer has
been inserted.

For almost every theta in the typed sector, (O7) makes H_(r/t)=0 eventually,
so the expectation's integrand tends to zero pathwise. On the complement of
the limiting typed sector, the determinant-times-type factor W_r/r^4 tends
to zero; no global selector or count convergence is required there. The
typed boundary is null, and the same determinant continuity suffices there
as well. The generic null sets and the conditional almost-sure sets are
handled by Fubini at each fixed parameter, or along each sequence r_i->0;
there is no common-null-set assertion over all uncountably many pins.

The source envelope on each compact theta box is

    W_r/r^4 <= C_T (1+||F||_C4)^4,

with finite expectation, locally bounded h_r and bounded r²/Z_r.
Since 0<=G_r<=1, dominated convergence in theta and the coupled field gives
zero for the limit of the integral of (O10) on that box.

The actual complement is bounded, without changing the conditioning, by

    r^-3 QrW(F, ||Theta_r||>T).

[ELDER S9], the same retained tail input used by U50, gives

    lim_(T->infinity) limsup_(r->0)
      r^-3 QrW(F, ||Theta_r||>T) = 0.

First take r->0 on a fixed box, then exhaust the boxes. Consequently

    r^-3 E_QrW G_r -> 0.                                (O11)

This is where integrability of the multi-occurrence statistic is obtained.
Almost-sure stabilization by itself would not justify taking an expectation
of the unbounded count N_h; (O8) and the bounded mark supply the needed
weighted domination.

## 6. Radial integration and count-to-probability conversion

Substitute r=t h into (O9):

    h^-5 J_h = integral_(B x K x S1) integral_c0^C0
        t^4 A_(th) [(th)^-3 E_Q(th)W G_(th)]
        dt db dk d sigma(u).                            (O12)

The full count has order h^5 because r dr times the weighted failure factor
r³ is r^4 dr. The new bounded mark tends to zero at that same scale.
[P (7.8)] gives r^-3 E G_r <= C on these fixed compact outer parameters;
A_r is uniformly bounded by the source radial interface. Since t is in a
fixed compact interval away from zero, this is an integrable common
majorant. Dominated convergence using (O11) proves J_h=o(h^5), hence (O2).
The fixed factor L² converts per-volume intensity back to a probability
coefficient; it cannot be omitted.

For every finite nonnegative integer n,

    0 <= (n-1)_+ <= n 1{n>=2},
    n - 1{n>0} = (n-1)_+,
    2 1{n>=2} <= n 1{n>=2}.                             (O13)

Taking expectations proves (O3) and, using (O1) with Phi=1,

    P(N_h>0)=E N_h-E[(N_h-1)_+]
             =lambda_U h^5+o(h^5).

For small enough h this probability is positive. The total-variation
distance in (O5) is exactly P(N_h>=2 | N_h>0), which is bounded by
E[N_h 1{N_h>=2}]/(2P(N_h>0)) and tends to zero.

For bounded Phi, let S_h(Phi)=sum_(M in A_h) Phi(V_h(M)). Pointwise,

    |S_h(Phi)-1{N_h>0} S_h(Phi)/N_h|
        <= ||Phi||_infinity (N_h-1)_+.                   (O14)

Thus the unconditional numerator of the field-first sampling experiment is
L² C_U(Phi)h^5+o(h^5), by (O1), (O3) and (O14).
Dividing by (O4) proves (O6). It is now legitimate to use the normalized
intensity law for this different sampling experiment because the excess
has been bounded, rather than because the laws were declared identical.

## 7. What this closes and what remains outside it

The estimate closes the C50 next-step excess-multiplicity obligation for its
precisely defined compact-band population, conditional on the named sources.
It identifies the first occurrence coefficient lambda_U=L² C_U(1) and the
corresponding weak field-conditioned mark law.

It does not prove a bound for E[N_h(N_h-1)], convergence of higher moments,
a quantitative o(h^5) rate, independence of occurrences, a Poisson process,
all birth/gap marks, growing torus volume, infinite volume, higher dimensions,
or a broader universal persistence theorem. In particular probability
convergence to a single selected bar does not control arbitrarily rare
fields with large counts at second-moment scale. Ordinary short-bar leading
laws, C8 and formal statement alignment are not promoted by this result.

Limit order: fix L,B,K,c0,C0 and each outer t,b,k,u; on each fixed compact jet
box use the full-field coupling as r->0, with sample-dependent R and delta
only inside its pointwise proof; remove the jet box with the original
weighted-failure tail; integrate the fixed outer parameters. No exchange
of a growing-domain limit with the coupling is used.

The finite exact controls check count identities, normalization, a Taylor
annulus budget and algebraic counterexamples to omitted hypotheses. They
do not establish off-contact Morse genericity, the coupling, or weighted
tail exhaustion. Those analytic steps are in GLOBAL.md, §§4–6 above and
the explicitly retained sources, and require substantive nonauthor review.

