# The third-order coefficient of the short-lifetime law: the fold-scale finite part, `d = 1, 2, 3`

Object: CL-THIRD-ORDER-COEFF-20261001-v1.4.1.
Author: Anthropic Claude (claude.ai session `session_01NMeKEismAyeqgdB4sy2NJU`), 1 October 2026 (v1.3: 2 October; v1.4
and v1.4.1: 4 October 2026).
**v1.4.1 (answers the two readbacks of v1.4; no number changes).** C129 (OpenAI/Codex, review 5404127976,
AMEND_SCOPED) and Grok Bot agent 1's confirming readback (5976332101, AMEND, scoped) found no blocker. They found no
error in the coefficients or the checker.
- *C129-A1.* In §2.2, the transverse covariance `2/0/1` is the contact limit. At finite `r` it is `2 + σ_r²`, `σ_r²`
  and `1`, with `σ_r² = Var(f(0) | U_r) = r⁸/6144 + O(r¹⁰)`. No number changes.
- *C129-A2 (= N6-1).* The dependency sentence separates numerical inputs (none consumed) from the analytic
  identifications: #214 Lemma 1.3, #218 (F.2), and #218 Lemma O with #220 Lemma O′.
- *C129-R1.* The window intervals are labelled as nominal binomial counting intervals. Their coverage under
  within-field dependence is not assessed.
- *C129-N1 and N6-2.* `1.9%` becomes `1.8%` (355/19215). §7 and the README say "the `d = 1` comparison with #214".
- *Merged since v1.4.* #214 (as `e4ca2b3`) and #237 (as `cb73b11`), with the pinned blobs unchanged. Both are now bound
  from the tree, and the text calls them merged author-side proof candidates.

**v1.4 (answers the four nonauthor reviews at `7e97018`; no coefficient or Monte Carlo ratio changes).** The reviews are
Grok Bot agent 1 on Slices A and C and the status text (5401553740; signature corrected in 5974176267), xAI/Grok on
Slice D (5401550768), and xAI/Grok agent 3 on Slice B (5401560065, 5401592048). No finding is a blocker.
- S1 and S2 are P1. The others are P2 items, two issues "to fix or answer" (D-1, D-2), minor issues and optional
  amendments.
- All are applied except U-1 (the Monte Carlo cannot be replayed from the repository), which is acknowledged.
- `SOURCES.json` (`nonauthor_reviews`) records each disposition.

The changes, by group:
- *Status wording (S1–S5).* The discharge and "certified" wording of v1.3 is replaced by each packet's own status.
  - #218, #220, #229, #232 and #187 are author-side proof candidates. #223 and #219 certify enclosures of explicit
    expressions; #223's is the Gaussian-kernel surrogate, with no torus transfer.
  - The candidate law ((T.1) of #218, (T⁺.1) of #229) is not (0.2). The adjacent-pair density is formal.
  - `d = 1` rests on #214, which was open at v1.4 (merged since; v1.4.1). #187 is now bound.
- *Checker (C1, C2).* T1, T3 and T4 compare every computed `c₂` with #223's closed forms; the observed errors are at most
  `2.6·10⁻⁹`. The mutants now fail on computed checks only. §0 and §2.4 quote the errors, not the spreads.
- *Monte Carlo (D-1 to D-6, C3).*
  - The `ℓ^{1/2}` reading of the residual is withdrawn: other powers fit comparably (#240 §7 item 4; #237 Remark 4).
  - The adjacent-pair comparisons are labelled formal.
  - The `d = 3` saddle reference is corrected to `436.25`, and error bars are added.
  - The weak power of the completeness checks for close pairs is stated, and the window rows give their counts.
  - The cancellation fraction is stated per `ℓ`, and §4 explains its last-digit rounding.
- *§§0–2 (A1–A3, XA-216-B-01 to B-06).*
  - (0.1) and the interface cancellation are cited to #218 (F.2) and Lemma O and to #220 Lemma O′.
  - §2.2 states its domain, its proof (#218 Lemma F), its non-uniformity in small `k` and its kernel scope.
  - §2.1 states the truncation error per dimension. §2.3 states the coordinate map to #214 and what it consumes.

**v1.3 (status update; no number changes).** The packets cited as unmerged in v1.2 had landed. §0 "Status since v1.2"
records what they supply; v1.4 rewords it (S1–S3). xAI's P2 and P3 on v1.2 (5378684363) were answered.
- P2: §4 separates the coefficients from the three-term truncation, whose error at a given `ℓ` is not quantified.
- P3: this note consumes nothing, so it imposes no landing order.
- Labels: #214's theorem is Theorem 1D, with displays (1D.1)–(1D.2); the label note is 5942064561. #214 is rebound to
  v1.3 (`54666d2`), whose `B₂` is unchanged.

**v1.2 (after the Codex review of v1.1, head `605af74`, and one author-side correction).**
- *Requirements for a proof (author-side correction).* v1.1 said that a rate `O(r)` in #207's CU.4 would suffice for a
  proof in `d ≥ 2`. That understated it. §0 "What is not claimed" now lists three requirements:
  - a rate in CU.4;
  - a quantitative fold-scale expansion;
  - for the elder density, a bound `o(ℓ^{1/3})` at intermediate separations. On file, #198's Lemma B gives only
    `O(ℓ^{1/3}ρ^{−1})` there.

  The candidate density needs only the first two, and Math- #218 (Theorem T) now proves its expansion with this `c₂`,
  at candidate status.
- *Digits.* T4 now runs at a refined grid and compares it with the former production grid and with the second `r`-set.
  v1.1's coarse comparison grid used 32 nodes in `b`, which under-resolves the height integral and moved `c₂` by
  `4.5·10⁻⁸`. The converged value is unchanged. All stated digits are stable to `≤ 7·10⁻¹⁰` (§2.4). (v1.4, C2: these
  are spreads, not errors.)
- *Sources.* The workflow binds each cited unmerged source to its recorded commit and path, not only to its blob id.
- *Monte Carlo.* §3 gives the final counts and a direct test of the elder window.

The coefficients are unchanged.

**v1.1 (after the Codex review of v1 on Math- #216, head `205550f`).**
- *Replay.* The replay is now interpreter-independent: every float sum uses `math.fsum`, and the `r`-fit uses `r/max r`.
  The output is byte-identical on CPython 3.10–3.14.
- *Precision.* `c₂` is quoted to 8 significant digits. Summation order moves the 10th digit.
- *Workflow.* The workflow verifies the cited unmerged sources by blob id.
- *Provenance.* The owner's post-stop instructions are recorded exactly (`SOURCES.json`, `delivered_under`).
The coefficients are unchanged.

Disposition: FORMAL COEFFICIENT WITH NUMERICAL EVIDENCE. In `d = 1` the law is Theorem 1D of Math- #214, a merged
author-side proof candidate. In `d ≥ 2` the expansion (0.2) is not proved here. For the elder density, the merged
author-side proof candidates #220 and #229 prove it with remainder `O(ℓ^{3/7})`, using the merged #187 for the far
part. For the candidate density, #218 ((T.1)) and #229 ((T⁺.1)) prove the analogous candidate law, which has `B_{d,L}` and `I^{cand}`
(§0, "Status since v1.2"). Nonauthor review required. Scientific effect: NONE — no register, graph, STATUS,
PROOF_INDEX, prize or Boolean change. Same GitHub account as every lane; zero organizational independence.
**Dependencies (v1.4.1, C129-A2).** No numerical input is consumed: the checker implements the merged kernel of [R]
(`frontiers/three_fronts_20260924/LIFETIME_REMAINDER.md`, blob `247b3ecf`) directly. The analytic identifications
use, at their own status:
- #214 Lemma 1.3 (the `d = 1` fold identification, §2.3);
- #218 Lemma F, (F.2) ((0.1));
- #218 Lemma O with #220 Lemma O′ (the interface cancellation, §1).

All three are merged author-side proof candidates. The following are cited for comparison:
- Math- #214 (`d = 1`, Theorem 1D; merged as `e4ca2b3`);
- Math- #207 (Theorem CU: `c₁` and the cusp loss; merged);
- Math- #191 (the even contact expansion; merged);
- the merged values of `c_{2,∞}` and `c_{3,∞}`;
- since v1.3, the merged #218 (Theorem T), #220 (Theorem E3), #229 (Theorems T⁺ and E3⁺), #223 (`c₂` in closed form),
  #232 (`c₂` on the torus) and #219 (`c₁` certified);
- since v1.4, the merged #187 (Theorem F, the far part of #220 and #229) and #240 (§7 item 4), and #237 (Remark 4;
  merged as `cb73b11`).

## 0. Statement

**Setting.** We use the notation of [R] §§2–4 and #207 §0:
- the [P] field on `X = R^d/(LZ^d)`, with pins `M = −ru/2` and `S = ru/2`;
- the symmetric pin vector `U_r`, with target `v_r = (b − kr³/2, −kr², 0, 12k, 0, …, 0)`;
- its density `π_r`;
- the two-point kernel

      A_r(b, k, u) = 12 π_r(v_r) E[ |det H_M| |det H_S| 1{typed} | U_r = v_r ] / r²,

  so that the near part of the elder lifetime density is `∫dσ(u)∫db∫dr r^{−2}A_r^{eld}(b, ℓ/r³, u)` (#207 (0.1)).

In `d ≥ 2`, at fixed `(b, k, u)` with `k > 0`, `A_r = A₀ + r²A₂ + O(r³(1 + k^{−1}))` (#218 Lemma F, (F.1)); `d = 1`
rests on #214 (merged; an author-side proof candidate; §2.2–§2.3). There is no `r¹` term (#191's even contact
expansion; #218 (2.2); checker T5). Here `A₀ = 12π₀(v₀)·36k²E[Δ²1{A<0} | v₀]` is the contact kernel, and

    A₂(b, 0, u) = −12 π₀(u; v₀(b, 0)) E₀[ Y² 1{A < 0} | b ]                                              (0.1)

is the small-`s` limit of #207's cusp loss `loss(s) → Y²` (`s → 0`), with `Y = (f₄/12)Δ − γᵀadj(A)γ/4`. (0.1) is not
part of a definition.
- In `d ≥ 2` it is #218 Lemma F, (F.2) (merged; candidate status), which also gives `A₂(b, ·, u) ∈ C¹[0, ∞)`. #218 does
  not cover `d = 1`.
- This packet checks it numerically in `d = 2` only (T6). In `d = 1` a development check, not replayed, agrees to
  `2·10⁻¹²`. There is no `d = 3` check.

Define

    c₂ := (1/3) ∫_{S^{d−1}} ∫_R ∫_0^∞ [A₂(b, k, u) − A₂(b, 0, u)] k^{−4/3} dk db dσ(u),

the Hadamard finite part of `(1/3)∫A₂k^{−4/3}dk`. The integral converges: `A₂(b, k) − A₂(b, 0) = O(k)` as `k → 0`.

**Claim (formal in `d ≥ 2`).**

    ν_eld(ℓ) = c ℓ^{−1/3} + c₁ ℓ^{1/4} + c₂ ℓ^{1/3} + O(ℓ^{1/2})        (ℓ ↓ 0),                         (0.2)

with `c₁` the coefficient of #207 (CU.2). The same `c₂` appears in the near candidate density, with `c₁` replaced by
`I^{cand} = (3^{1/4}/2)c₁` (#207 (CU′.1)). The candidate law ((T.1) of #218, (T⁺.1) of #229) also has the constant
`B_{d,L}`. Formally, the density of adjacent (max, saddle) pairs has the same three coefficients and no `B_{d,L}`.
Nothing on file proves that expansion (#218 Remark 3; #220 and #229 list it as not claimed). The reason for the common
`c₂` is that it is a fold-scale quantity: the elder rule enters only through the cusp window.

**What is established here.**
1. **`d = 1`.** The formula gives #214's `2B₂` (§2.3).
   - The cusp component is an algebraic identity for every covariance satisfying #214's (H).
   - The fold component is an identification not derived here: it consumes #214's Lemma 1.3.
   - The total is checked numerically to `10⁻⁹` for two kernels (checkers T1, T2). For the Gaussian kernel the merged
     #223 gives `c₂ = 2B₂` as an identity of exact numbers.

   In `d = 1`, (0.2) is #214's Theorem 1D. #214 is a merged author-side proof candidate, so the `d = 1` law holds at
   that status.
2. **Values for the Gaussian kernel `e^{−|z|²/2}`** (the SIDE24 covariance up to factors `1 + O(e^{−L²/8})`):

   | `d` | `c` (recomputed; equals the merged value) | `c₂` | `c₂/c` | `c₁/c` (#207, #214) |
   |---|---|---|---|---|
   | 1 | `0.110110378959` (`C₀`) | `0.23004458` (`= 2B₂`) | `2.089218` | `−2.0671` |
   | 2 | `0.073406919306` (`c_{2,∞}`) | `0.22152441` | `3.017759` | `−3.6699` |
   | 3 | `0.041775931841` (`c_{3,∞}`) | `0.16123405` | `3.859496` | `−5.0711` |

   Merged #223 gives these `c₂` in closed form, with certified enclosures: for example,
   `c₂ = (13/18)·12^{1/6}Γ(5/6)/π^{3/2}` in `d = 2` and `(5/48)(33 − 7√6)·12^{1/6}Γ(5/6)/π^{5/2}` in `d = 3`. Every
   digit in the table is a correct rounding: of #223's closed forms for `c`, `c₂` and `c₂/c`, and of #219's enclosures
   for `c₁/c` (in `d = 1`, of #219's `c₁` over #223's `c`).
   - *Accuracy (v1.4, C2).* Changing the `r`-set, refining the grids, or replacing exactly rounded summation by plain
     left-to-right summation moves `c₂` by at most `7·10⁻¹⁰` (§2.4). These variations share the bias of the `r`-fit, so
     their spreads do not bound the error. v1.2 and v1.3 inferred the digits from the spreads, which was not justified.
   - Against #223's closed forms (checkers T1, T3, T4) the observed errors are:
     - `5.7·10⁻¹⁰` in `d = 1`;
     - `1.9·10⁻⁹` and `2.6·10⁻⁹` in `d = 2` (the two `r`-sets);
     - `1.0–1.4·10⁻⁹` in `d = 3` (three runs).
   - The exact values lie at least `4.1·10⁻⁹` from a rounding boundary of the printed digits. The floating values alone
     would not have settled the eighth digit in `d = 2`.

3. **Full-field Monte Carlo in `d = 2` and `d = 3` (§3; exploration, outside the repository).** The *parameter-free*
   three-term law (0.2) matches the actual elder-rule persistence of the periodized Gaussian field on `[10⁻⁴, 10⁻²]`,
   at about the 1% level. Both the leading term alone and the two-term law `cℓ^{−1/3} + c₁ℓ^{1/4}` are rejected. On
   `[10⁻⁴, 3·10⁻²]` the data exceed (0.2); the form of the excess is open (§3).

**Consequence for SIDE24 (`d = 3`).** The relative correction is
`ν/(cℓ^{−1/3}) − 1 = −5.071ℓ^{7/12} + 3.859ℓ^{2/3} + …`. The `ℓ^{1/3}` term cancels the fraction `0.761ℓ^{1/12}` of the
`ℓ^{1/4}` term:

| `ℓ` | `10⁻⁵` | `10⁻⁴` | `10⁻³` | `10⁻²` |
|---|---|---|---|---|
| fraction cancelled | 29% | 35% | 43% | 52% |

So the fraction is 40–50% only for `ℓ ∈ [4.4·10⁻⁴, 6.5·10⁻³]`. The combined correction is `1%` at `ℓ ≈ 4.6·10⁻⁵` and
`10%` at `ℓ ≈ 3.6·10⁻³`. For the `ℓ^{1/4}` term alone (#207 §8, V3 edit E15) the corresponding values are `2.3·10⁻⁵`
and `1.2·10⁻³`. §4 gives the table and the status of these numbers.

**Status since v1.2 (v1.3; reworded in v1.4, S1–S3).** All the packets below are merged. #218, #220, #229, #232 and
#187 are author-side proof candidates; #223 and #219 certify enclosures of explicit expressions. Each item holds at its
packet's stated conditional scope.
- **Candidate density.** #218 (Theorem T) proves the candidate law: (0.2) with the constant `B_{d,L}` added and `c₁`
  replaced by `I^{cand}`, with this `c₂` and remainder `O(ℓ^{4/11})`. #229 (Theorem T⁺, (T⁺.1)) improves the remainder
  to `O(ℓ^{3/7})`.
- **Elder density.** #220 (Theorem E3) supplies the three requirements below:
  1. the elder cusp rate, through its Lemmas Q and CE;
  2. the fold expansion, through #218 Lemma F;
  3. the intermediate separations, `O(ℓ^{2/5})`, through its Lemmas H and S′.

  With #187's Theorem F for the far part, #220 proves (0.2) with remainder `O(ℓ^{4/11})` (E3.3). #229 (Theorem E3⁺,
  (E3⁺.1)) improves the remainder to `O(ℓ^{3/7})`. Without #187, #220 gives (E3.0)–(E3.2) only.
- **What remains formal here.**
  - The remainder `O(ℓ^{1/2})` of (0.2) in `d ≥ 2`. #229 Remark 1 explains why its method stops at `3/7`.
  - The adjacent-pair density. No packet proves its expansion (#218 Remark 3; #220 and #229 list it as not claimed).
  - Any reading of the Monte Carlo residual of §3 as a term of order `ℓ^{1/2}` (v1.4, D-1).
- **The coefficients.**
  - **`c₂`** is certified for the Gaussian kernel by #223: closed forms with certified enclosures of the fixed-cone
    surrogate expression of §2.2.
    - Its identification with the typed kernel's `A₂` rests on #218 Lemma F, which #223 consumes.
    - #223 makes no torus transfer. The transfer to the periodized covariance for every `L ≥ 24`, with error `< 10⁻⁶⁰`,
      is the author-side candidate #232.
  - **`c₁`** is certified by #219, with `c₁/c_{3,24} ∈ [−5.07106215, −5.07106213]`.

**What is not claimed.** (Items 1–3 below are v1.2's record of what a proof needed. The merged candidates above now
supply them.)
- No proof of (0.2) for the elder density in `d ≥ 2` *here*. A proof needs three ingredients. For the candidate density
  the first two are supplied, at candidate status, by **Math- #218** (Theorem T; see below).
  1. **A rate in CU.4.** #207's kernel limit CU.4 must hold with a rate:
     `|r^{−2}(A_r − A₀)(b, κr, u) − (𝒜 − 𝒜^{con})(b, κ, u)| ≤ C r^θ (1 + κ)^N (1 + |b|)^N e^{−cb²}`.
     - In #218's ledger, `θ > max(2/5, (N + 1)/4)` suffices. `θ > 1/3` alone does not suffice there; this corrects an
       earlier draft of this item, found by #218's referee.
     - #218's Lemma C proves `θ = 1`, `N = 2` for the *candidate* kernel.
     - For the elder kernel this needs a quantitative form of Proposition CU.3. The decision's height margin is
       `κ·min(1, 12||φ| − 1/3|)`: linear in the distance from the window's edge.
  2. **A quantitative fold-scale expansion.** `A_r = A₀ + r²A₂ + O(r³(1 + k^{−1}))`, uniformly down to `k ≈ r^{1−}`.
     The `r³/k` term is the boundary layer of the typed region near `det A = 0`. #218's Lemma F proves it, together with
     the identification `A₂(b, 0, u) = −12π₀E₀[Y²1{A<0} | b]` of (0.1).
  3. **For the elder density only: the intermediate separations.** The contribution of `Sℓ^{1/4} ≤ r ≤ r₁`, for one
     fixed `r₁ > 0`, must be `o(ℓ^{1/3})`.
     - At v1.2 the tools on file did not give this. #198's Lemma B bounds this range by `O(ℓ^{1/3}ρ^{−1})`, which is
       never `o(ℓ^{1/3})`, and #207's Lemma CU.5 route gives only `o(ℓ^{1/4})`. Since v1.3, #220's Lemmas H and S′
       give `O(ℓ^{2/5})`, and #229 gives `O(ℓ^{4/9}log(1/ℓ))`.
     - Formally the range is `O(ℓ^{1/2})`. The cusp-scale elder weight is `O(κ³)`, with relative corrections
       `O(r/κ)`.
     - Beyond `r₁`, the far bounds `O(ℓ^{2/3})` of #187 (merged) and `O(ℓ^N)` of #188 (open) suffice. #198's Lemma F′
       (`O(ℓ^{1/3})`) does not.

  The **candidate** density needs only 1 and 2. Its intermediate separations are bounded by
  `O(ℓ^{1/4}S^{−7} + ℓ^{1/2}S^{−2})` (#207 Lemma L), which is `o(ℓ^{1/3})` for `S = ℓ^{−a}`, `a > 1/84`. Its far part
  is `O(ℓ)` (#207 (7.2)). **Math- #218 (Theorem T)** proves, at candidate status,
  `ν_cand = cℓ^{−1/3} + B_{d,L} + I^{cand}ℓ^{1/4} + c₂ℓ^{1/3} + O(ℓ^{4/11})` with this `c₂`.

  v1.1 said only that "a rate `O(r)` in CU.4" was needed. That understated 2 and missed 3.
- No certified enclosure of `c₂` here. The values are floating point. Checkers T1, T3 and T4 compare them with #223's
  closed forms (v1.4), and #223 encloses those with certified intervals.
- No statement about the terms after `c₂`.
- Nothing about `L ≠ ∞`, beyond the `O(e^{−L²/8})` periodization factors. #232 (an author-side candidate) transfers
  `c₂` to the torus for `L ≥ 24`.

## 1. Why the finite part (formal derivation)

Put `s := rℓ^{−1/4}`, so that `κ = ℓ/r⁴ = s^{−4}` and `k = ℓ/r³ = ℓ^{1/4}s^{−3}`. The near integrand `r^{−2}A_r^{eld}(b, ℓ/r³, u)`
has two regimes.

- **Fold regime (`s ≪ 1`, `κ ≫ 1`).** Every typed pair is an elder pair: the non-elder part is `O(r³/k)`, [C7-K] (K2).
  At fixed `k`,

      r^{−2}A_r = r^{−2}A₀(b, k) + A₂(b, k) + O(r).

- **Cusp regime (`s ≍ 1`).** By #207 CU.4,

      r^{−2}A_r^{eld} = r^{−2}A₀ + (𝒜^{eld} − 𝒜^{con})(b, κ) + o(1),

  and `(𝒜^{eld} − 𝒜^{con})(b, κ) = −12π₀E₀[loss(s) | b] → A₂(b, 0)` as `κ → ∞`, by (0.1).

The composite approximation

    r^{−2}A₀(b, k) + A₂(b, k) + [(𝒜^{eld} − 𝒜^{con})(b, κ) − A₂(b, 0)]

reproduces both regimes:
- for `s ≪ 1` the bracket vanishes;
- for `s ≍ 1` we have `k → 0` and `A₂(b, k) → A₂(b, 0)`.

Integrating over `r` gives three pieces, each converging separately:

    ∫ r^{−2}A₀ dr = cℓ^{−1/3},
    ∫ [A₂(b, ℓ/r³) − A₂(b, 0)] dr = (ℓ^{1/3}/3) ∫ [A₂(b, k) − A₂(b, 0)] k^{−4/3} dk,
    ∫ (𝒜^{eld} − 𝒜^{con})(b, ℓ/r⁴) dr = ℓ^{1/4} ∫ (𝒜^{eld} − 𝒜^{con})(b, s^{−4}) ds.

The third piece is #207's `c₁` integrand. The neglected pieces are formally `O(ℓ^{1/2})`:
- the fold remainder. With requirement 2 of §0 it is `O(ρ_f² + ρ_f⁵/ℓ)` below `r = ρ_f`, which is `o(ℓ^{1/3})` for
  `ρ_f = ℓ^{1/4+a'}`, `a' > 1/60`;
- the cusp remainder. With requirement 1 it is `o(ℓ^{1/3})`;
- the mixed term `A₂(b, k) − A₂(b, 0) = O(k)` at `s ≍ 1`, which integrates to `O(ℓ^{1/2}σ^{−2})` above `s = σ`;
- the intermediate separations `ℓ^{1/4} ≪ r ≤ r₁` and the far part. For the elder density these need requirement 3, and
  #187 or #188.

Given requirements 1–3, these estimates close the argument. The interface terms `±A₂(b, 0)ρ_f` cancel, because
`(𝒜^{eld} − 𝒜^{con})(s) = A₂(b, 0) + O(s⁴)` as `s → 0`, that is `O(κ^{−1})` with `κ = s^{−4}`. For the candidate kernel
this is #218 Lemma O (O.1). For the elder kernel it is #220 Lemma O′ (O′.1), combined with Lemma O. This is a sketch; it
is not written here as a proof. #218 §4 and #220's proof of Theorem E3 carry it out. v1.1 listed only the first three
pieces.

In `d = 1` this is exactly the structure of #214's Proposition 2.2:
- the fold part (c) gives `B₂^{(1)}`;
- the cusp part (d), split as `p₃(α) = p₃(0) + (p₃(α) − p₃(0))`, gives the Mellin term `(I_θ/2)h^{1/4}` and the finite
  part `B₂^{(2)}`.

There it is proved, in #214 (merged; an author-side proof candidate).

## 2. The computation

**2.1 Pinned Gaussian structure.**
- *Jets.* The jets `J = (∂^αf(0))_{|α|≤N}` at the midpoint have covariance `(−1)^{|β|}∂^{α+β}ρ(0)`. We take `N = 12, 10, 8`
  for `d = 1, 2, 3`.
- *Pin rows and Hessians.* Both are linear forms in `J`, by Taylor along `u = e₁`.
- *Truncation.* The error is of order `r^{N−2}` times a Gaussian moment; no constant is stated. The measured sizes
  (v1.4, XA-216-B-04) are:
  - `≤ 7·10⁻¹⁵` relative (float resolution) in `d = 1, 2`, against an untruncated kernel (nonauthor Slice B read
    5401592048, B-10);
  - in `d = 3`, against `N = 10`: up to `2.3·10⁻¹³` relative at `r = 0.011` and `2.2·10⁻¹⁴` at `r = 0.007` (measured
    by the reviewer and reproduced here);
  - the `d = 3` `c₂` moves by `1.2·10⁻¹¹` between `N = 8` and `N = 10`. v1.3's "below `10⁻¹⁵` at `r ≤ 0.011`" was
    wrong for `d = 3`.
- *Conditioning.* We condition on `U_r = v_r` in Decimal arithmetic (50 digits), then pass to floats. The small conditional
  variances, `O(r⁴)`, come from `O(1)` cancellations and need the extra digits.

**2.2 The typed indicator.** *Domain (v1.4, XA-216-B-01):* fixed `(b, k, u)` with `k > 0`, and
`0 < r ≤ min(r_0^*, 1/2)`.
- **`d = 1`.** At fixed `k > 0` the typed event has probability `1 − O(e^{−ck²/r²})`, so `E[(−h_M)h_S]` is used. By
  Cauchy–Schwarz the kernel error is `O(e^{−ck²/(2r²)})`. This is a fixed-`k` sketch. It is not covered by #218 Lemma F,
  which is stated for `d ≥ 2`.
- **`d = 2`.** `1{typed} = 1{f_yy(0) < 0}` up to shifts of the boundary of size `O(rT(1 + T/k))`, where `T` is #218's
  dominating variable and this size is its `υ`.
  - On the layer between the two boundaries both scaled determinants are `O(r)`, so the product is `O(r²)` there. The
    layer has probability `O(υ)`.
  - So the error in `A_r` is `O(r³(1 + k^{−1}))`. This is #218 Lemma F, Step F2 and (2.3), with the surrogate paragraph
    after its proof.
  - Combining (2.3) with #218 (2.1) (`Φ` against the exact product, `O(r⁴)`), the nonauthor Slice B read (5401560065,
    B-2) obtains `|A_r − Ã_r| ≤ Cr³(1 + k^{−1})P^Ne^{−c(b² + k²)}`. Here `P = 1 + |b| + k` as in #218, and `Ã_r` is
    the fixed-cone surrogate, in #223's notation.
  - The expectation of the quartic product given `f_yy(0)` follows from Isserlis' formula; the half-line integral uses
    truncated Gaussian moments.
- **`d = 3`.** `1{typed} = 1{A < 0}`, with `A = D_y²f(0)` (`2 × 2`), again up to `O(r³(1 + k^{−1}))` (Lemma F with
  `m = 2`).
  - The conditional law of `A` is invariant under transverse rotations.
  - Its covariance is `Var a₁₁ = Var a₂₂ = 2`, `Cov(a₁₁, a₂₂) = 0` and `Var a₁₂ = 1` in the contact limit.
  - At finite `r` (reference kernel; v1.4.1, C129-A1), `A + f(0)I` is independent of the pins with this GOE covariance.
    So `Var a₁₁ = Var a₂₂ = 2 + σ_r²`, `Cov(a₁₁, a₂₂) = σ_r²` and `Var a₁₂ = 1`, where
    `σ_r² := Var(f(0) | U_r) = r⁸/6144 + O(r¹⁰)` (checked at 60 digits: `1.6276·10⁻¹²` at `r = 0.1`).
  - Rotation invariance and the eigenvalue reduction are unaffected. The checker uses the full conditional covariance
    of its truncated-jet model, so no number changes.
  - So `E[det H_M det H_S | A]` depends only on the eigenvalues. It is a polynomial of degree `≤ 6` in
    `(b_eff, k, λ₁, λ₂)`, obtained from Isserlis' formula over the 76 partial matchings of each of the 36 permutation
    products.
  - It is integrated over `λ₂ < λ₁ < 0` with the eigenvalue Jacobian `π(λ₁ − λ₂)`.
  - Here `b_eff := b − kr³/2`, the target's height coordinate. The transverse block's conditional mean does not depend on
    `k`, by parity; the checker asserts this.
- **Not uniform in small `k` (v1.4, XA-216-B-02).** The constant grows like `k^{−1}`. For `k ≲ r`, the cusp scale, the
  typed and fixed-cone kernels differ at order `r²`. The difference is the cusp correction
  `r²·12π₀E₀[(Y² − 36κ²Δ²)₊1{A<0} | b] = r²[(𝒜^{cand} − 𝒜^{con})(κ) − A₂(b, 0)]`, with `κ = k/r`, and it decays like
  `κ^{−1}` (#218 Lemma O).
  - So the `O(r³)` of this section must not be used uniformly in small `k`. Integrals down to `k → 0` need Lemma F's
    `k^{−1}` together with the cusp analysis (#207 CU.4; #218 Lemmas C and O).
  - The definition of `c₂` needs only the fixed-`k` statement. Pointwise in `k > 0` it gives `A₂ = Ã₂` for the
    `r²`-coefficients of `A_r` and `Ã_r`. Both are `C¹` on `[0, ∞)` ((F.2) and #218's surrogate paragraph), so they
    agree at `k = 0` too.
- **Kernel scope (v1.4, XA-216-B-03).**
  - For `d ≥ 2` the replacement holds for any [P] covariance, including the torus covariance `K_L` at fixed `L` (Lemma F;
    its constants are not uniform in `L`).
  - The `d = 3` rotation invariance and the covariance above (`2/0/1` in the contact limit) are facts about the
    reference kernel `φ`. For `φ`, pins on `e₁` make the transverse law isotropic; `K_L` has only cubic symmetry.
  - The `d = 1` statement is the fixed-`k` sketch above.

**2.3 The finite part in `d = 1`.** This section uses #214 (merged; an author-side proof candidate). (#214's `c₂` in
its Lemma 1.3 is a jet coefficient, unrelated to this note's `c₂`.) `∫A₂(b, k)db` has two components.
- *The cusp component (v1.4, XA-216-B-05).* With `Y = f₄/12` and `∫π₀E₀[f₄²]db = p₁₂p₃·σ₄²`, the expression of (0.1)
  evaluated at `v₀(b, k)` instead of `v₀(b, 0)` has `b`-integral `−(σ₄²/12)p₁₂p₃(12k)`. At `k = 0` this is the
  `b`-integral of (0.1) itself, `−(σ₄²/12)p₁₂p₃(0)`.
- So the cusp component contributes `(2/3)(−σ₄²p₁₂/12)12^{1/3}∫₀^∞(p₃(α) − p₃(0))α^{−4/3}dα` to the finite part, with
  `α = 12k`. This is `2B₂^{(2)}` of #214 §2(d), which defines it (§2(e) gives its closed form). The factor 2 accounts
  for the two orientations.
- *The fold component (v1.4, XA-216-B-06)* is the rest of `∫A₂(b, k)db`. It is #214's `τ²`-coefficient of
  `(12/t⁴)p_tm²` (§2(c)), which integrates to `2B₂^{(1)}`.
  - The coordinates correspond as `t = r`, `τ = r/2`, `α = 12h/t³ = 12k` and `h = ℓ`. The relative order `r²` of
    `∫db r^{−2}A_r` is the relative order `τ²` of `(12/t⁴)p_tm²`, plus the cusp component.
  - This identification is not derived here. It consumes #214's Lemma 1.3.
  - It is checked numerically by T1–T2 for the totals. The nonauthor Slice B read (5401592048, B-14) checked it pointwise
    in `k`, for both kernels, to `≤ 2·10⁻¹⁶` relative (exploration outside the repository).
- T1 and T2 check the total against the closed form `2B₂` (#214 (1D.2)):
  - Gaussian kernel: `0.2300445808` against `0.2300445803`, which is also #223's closed form (v1.4);
  - mixture `(e^{−x²/2} + e^{−2x²})/2`: `0.5760427428` against `0.5760427425`.

**2.4 Numerics.**
- *Expansion coefficients.* `A₀` and `A₂` come from least squares on `(1, r², r³, r⁴)` over five separations:
  `r = 0.001…0.005` in `d = 1`, `r = 0.003…0.011` in `d = 2, 3`.
- *Quadrature.* Gauss–Legendre in `b ∈ [−8, 8]` and in `t = k^{1/3} ∈ [0, K^{1/3}]`, with `K = 8`, and `K = 27` for the
  mixture.
- *Tail.* The term `|S^{d−1}|K^{−1/3}∫db(−A₂(b, 0))` beyond `K` is added analytically.
- *`d = 3` cone.* A Gauss–Legendre rule in `(s, t)`, with `λ₁ = −s` and `λ₂ = −s − t`.
- *Convergence (v1.2).* All changes below are absolute changes of `c₂`.

  | `d` | `c` relative error | `r`-set | grid refinement | plain summation |
  |---|---|---|---|---|
  | 1 | `2·10⁻¹⁴` | against `2B₂`: `6·10⁻¹⁰` (Gaussian), `4·10⁻¹⁰` (mixture) | `k`: `80 → 120`, `5·10⁻¹²` | — |
  | 2 | `8·10⁻¹⁴` | `7·10⁻¹⁰` | `(48, 80) → (64, 120)`: `< 10⁻¹²` | `3·10⁻¹⁰` |
  | 3 | `7·10⁻¹³` (grid `(56, 120, 48²)`) | `3·10⁻¹⁰` | `(40, 80, 32²) → (56, 120, 48²)`: `6·10⁻¹¹`; `(64, 160, 64²)`: `2·10⁻¹¹` more | `2·10⁻¹⁰` |

  - The `r`-fit bias dominates. Every variation is below `10⁻⁹`, but the variations share that bias, so they do not
    bound the error (v1.4, C2).
  - Against #223's closed forms the errors are `5.7·10⁻¹⁰` (`d = 1`), `1.9·10⁻⁹` and `2.6·10⁻⁹` (`d = 2`), and
    `1.1·10⁻⁹`, `1.0·10⁻⁹` and `1.4·10⁻⁹` (`d = 3`: production grid, comparison grid, second `r`-set). That is up to
    about four times the largest spread. T1, T3 and T4 now report them.
  - v1.1's comparison grid `(32, 48, 24²)` moved `c₂` by `4.5·10⁻⁸` (Codex P2). The cause is the height quadrature:
    32 nodes on `b ∈ [−8, 8]` under-resolve the `d = 3` integrand, while `(32, 80, 32²)` and `(40, 48, 32²)` isolate it.
  - v1.1's summation sensitivity `2·10⁻⁸` predates the scaled `r`-fit; the measured value is `≤ 3·10⁻¹⁰`.

## 3. Full-field Monte Carlo (exploration; outside the repository)

**Method** (C and numpy; archived with the project record, not part of this packet, per the standard-library rule).
- **Synthesis.** Exact spectral synthesis of the periodized kernel, with `ρ̂(k) = (2π)^{d/2}L^{−d}e^{−|k|²/2}`:
  - `d = 2`: `L = 64`, on a `2048²` grid;
  - `d = 3`: `L = 16`, on a `256³` grid.
- **Critical points.** All critical points are found and refined:
  - candidates from the fine-grid gradient;
  - Newton on degree-10 (`d = 2`) or degree-8 (`d = 3`) Taylor expansions, from spectrally exact coarse-grid derivatives;
  - a partner search along soft Hessian directions, for close fold pairs inside one cell.
- **Merges.** Ascending lines from every `(d−1)`-saddle, by RK2 with a backtracking line search, give the merges.
- **Persistence.** The superlevel `H₀` persistence follows by union–find with the elder rule. It is exact for the computed
  critical values.
- **Integrity.**
  - Critical-point counts match Kac–Rice. The errors are standard errors of the per-sample mean (D-3). v1.4 computed them
    from the raw sample records. These are pinned by sha256 in `SOURCES.json` but kept only in the session workspace, not
    in the project archive, because of their size.
    - `d = 2`: `376.42 ± 0.16` maxima and `752.70 ± 0.25` saddles per sample, against `376.37` and `752.75`.
    - `d = 3`: `142.99 ± 0.24` maxima and `142.52 ± 0.24` minima per sample, against `142.80`. The saddles number
      `436.20 ± 0.49` (index 1) and `436.67 ± 0.50` (index 2), against `436.25`. The saddle reference is the BBKS value,
      with saddle-to-extremum ratio `(29 + 6√6)/(29 − 6√6)`; v1.2 printed it as `436.4`.
  - The Euler characteristic is 0 in every retained sample.
  - Every maximum but one dies.
  - A dense-seed Newton search found no missed critical point in six `20 × 20` subregions (`d = 2`) and two `5³` subregions
    (`d = 3`).
  - *Power for close pairs (v1.4, D-4).*
    - These regions are small. By (0.2) they are expected to contain about 11.5 elder pairs with `ℓ < 10⁻²` (2.6 with
      `ℓ < 10⁻³`) in `d = 2`, and 0.66 (0.15) in `d = 3`. So the search tests completeness for close pairs only weakly
      in `d = 2`, and not at all in `d = 3`.
    - In `d = 3`, completeness for close pairs rests on the partner search. The Kac–Rice match bounds their loss only
      coarsely. There are about 10.8 elder pairs with `ℓ < 10⁻²` per sample, against `142.8` maxima. The maxima count
      (`142.99 ± 0.24`) excludes a loss of more than about 0.3 maxima per sample (2σ), that is about 3% of those pairs.
    - Missing close pairs would bias the elder ratios low, and the observed ratios are above 1.
  - Taylor evaluation matches exact trigonometric evaluation to `10⁻¹⁴` (`d = 2`) and `3·10⁻¹⁰` (`d = 3`).
  - In `d = 3`, 4 of 1000 samples are flagged and excluded: 3 have a failed ascent and 1 has Euler characteristic 1. In
    `d = 2`, none of 4000 is flagged.

**Results (final, v1.2: `d = 2`, 4000 samples, volume `1.64·10⁷`; `d = 3`, 996 samples, volume `4.08·10⁶`).** Counts
are binned in 24 logarithmic bins on `[10⁻⁵, 0.3]` and compared with the bin integrals of (0.2). There are no free
parameters. A range selects the bins whose geometric centres lie in it (v1.4, stated at the Slice D read's request).
- `[10⁻⁴, 10⁻²]` is 11 bins, spanning `[8.57·10⁻⁵, 9.65·10⁻³]`.
- `[10⁻⁴, 3·10⁻²]` is 14 bins, spanning `[8.57·10⁻⁵, 3.50·10⁻²]`.

| `d` | range of `ℓ` | elder pairs: data/(0.2) | `χ²/bins` | adjacent pairs: data/(formal law, `I^{cand}` for `c₁`) | `χ²/bins` |
|---|---|---|---|---|---|
| 2 | `[10⁻⁴, 10⁻²]` | `1.006 ± 0.004` | `7.0/11` | `1.004 ± 0.004` | `6.9/11` |
| 2 | `[10⁻⁴, 3·10⁻²]` | `1.013 ± 0.002` | `44.9/14` | `1.004 ± 0.002` | `12.8/14` |
| 3 | `[10⁻⁴, 10⁻²]` | `1.008 ± 0.010` | `5.0/11` | `0.999 ± 0.010` | `5.8/11` |
| 3 | `[10⁻⁴, 3·10⁻²]` | `1.026 ± 0.007` | `26.9/14` | `1.001 ± 0.006` | `6.5/14` |

*The adjacent-pair columns compare with a formal law (v1.4, D-2).* Adjacent pairs have no `B_{d,L}` term, and nothing on
file proves their expansion (#218 Remark 3; #237 Remark 4). These columns, and the rejected-adjacent coefficient below,
check consistency with the formal coefficients only.

**Shorter laws.** On `[10⁻⁴, 10⁻²]` both are rejected:

| `d` | leading term alone: ratio | `χ²` | two-term law: ratio | `χ²` |
|---|---|---|---|---|
| 2 | `0.941` | `335/11` | `1.089` | `714/11` |
| 3 | `0.911` | `116/11` | `1.122` | `175/11` |

The interim runs (1150 and 240 samples) gave consistent ratios.

**Beyond the three-term law (reworded in v1.4, D-1).**
- On `[10⁻⁴, 3·10⁻²]` the elder data exceed (0.2). A fit `eℓ^{1/2}` gives `e = 0.029 ± 0.005` in `d = 2` and
  `0.031 ± 0.007` in `d = 3`. On `[10⁻⁴, 10⁻²]` the same fit is not significant: `0.03 ± 0.02` and `0.01 ± 0.03`.
- Other powers fit comparably.
  - On `[10⁻⁴, 0.3]`, fits with `ℓ^{1/2} + ℓ^{3/4}` and with `ℓ^{2/3} + ℓ^{3/4}` differ by `|Δχ²| ≤ 2.6` (#240 §7 item 4).
  - A single extra power fits best at `p ≈ 0.14–0.33` in six of eight elder and rejected fits (#237 Remark 4).
  - So the data do not single out `ℓ^{1/2}`. Whether the residual comes from decision effects or from Monte Carlo
    systematics is open.
- v1.3 read it as "about `0.03ℓ^{1/2}`" and as consistent with the formal `O(ℓ^{1/2})` remainder. Nothing contradicts
  that remainder, but the data do not support the reading.
- So the Monte Carlo supports the three-term law at about the 1% level on `[10⁻⁴, 10⁻²]` only.
- The adjacent-pair residual is consistent with zero. It is so on this note's two ranges (the `χ²` above), and in #237
  Remark 4's joint fits on `[10⁻⁴, 0.3]` and `[10⁻⁴, 0.1]`.

**Rejected adjacent pairs.** These are adjacent pairs (the saddle ascends to the maximum) that are not elder pairs. They
test the cusp window directly, because the fold terms cancel. A fit `aℓ^{1/4} + bℓ^{1/2} + eℓ^{3/4}` on `[10⁻⁴, 0.3]`
gives:
- `d = 2`: `a = 0.0922 ± 0.0039`, against `I^{cand} − c₁ = 0.0921`;
- `d = 3`: `a = 0.069 ± 0.006`, against `0.0724`.

On `[10⁻³, 0.3]` the fit gives `0.091 ± 0.004` and `0.072 ± 0.007`. A fit without the `ℓ^{1/2}` term gives
`0.0821 ± 0.0006` and `0.0593 ± 0.0011`, which is biased. In `d ≥ 2` the rejected data carry a further correction whose
power the data do not fix (#240 §7 item 4; #237 Remark 4), so `a` depends on the nuisance terms (v1.4, D-1). In `d = 1`
there was no such correction (#214 §6.2).

**The elder window, tested directly (v1.2).** Theorem CU.2 says that, at the cusp scale, an adjacent pair is an elder
pair iff `|φ| < 1/3`. Here `φ = (f₄ − 3γᵀA^{−1}γ)/(72κ)` is computed from the jets at the midpoint, with `κ = ℓ/r⁴`.
For each `ℓ`-range the simulation tabulates the elder fraction against `|φ|`. The `|φ|` at which it crosses `1/2`, and
the rate at which the rule `1{|φ| < 1/3}` disagrees with the computed elder mark, are:

| `ℓ` range | `d = 2`: 50% crossing | `d = 2`: disagreement (count) | `d = 3`: 50% crossing | `d = 3`: disagreement (count) |
|---|---|---|---|---|
| `[10⁻⁶, 10⁻⁴)` | (too few near `1/3`) | `0.16%` (6/3795) | (too few) | `0.4%` (2/503) |
| `[10⁻⁴, 3·10⁻⁴)` | `0.329` | `0.40%` (17/4244) | `0.334` | `0.0%` (0/568) |
| `[3·10⁻⁴, 10⁻³)` | `0.347` | `0.91%` (90/9876) | `0.395` (few) | `1.7%` (23/1392) |
| `[10⁻³, 3·10⁻³)` | `0.337` | `1.8%` (355/19215) | `0.357` | `2.4%` (66/2704) |
| `[3·10⁻³, 10⁻²)` | `0.343` | `4.3%` (1936/45256) | `0.329` | `6.0%` (374/6252) |
| `[10⁻², 3·10⁻²)` | `0.335` | `8.2%` (6932/84812) | `0.339` | `11.7%` (1353/11560) |

*Reading the table (v1.4, D-5).*
- In `d = 2` the crossing sits at `1/3` within the binning in every range with enough pairs near the boundary. The
  disagreement falls steadily as `ℓ ↓ 0`, roughly like `ℓ^{2/3}`: a log–log fit of the five rows above `10⁻⁴` gives
  slope `0.66`.
- In `d = 3` the crossings lie between `0.329` and `0.395`. The lowest range has no crossing.
- The two lowest `d = 3` rows rest on few events. Their nominal 95% binomial counting intervals (Clopper–Pearson,
  treating the pairs as independent) are `0.05–1.4%` for 2/503 and `0–0.65%` for 0/568. Their coverage under
  within-field dependence has not been assessed (v1.4.1, C129-R1). So below `10⁻³` the `d = 3` disagreement is small
  but not resolved as monotone.

The archived figure `results/mc_final.png` shows three panels for each of `d = 2, 3`:
- the elder density divided by `cℓ^{−1/3}`, with the leading, two-term and three-term laws;
- the rejected adjacent density divided by `ℓ^{1/4}`;
- the window test.

## 4. The SIDE24 correction sizes (`d = 3`, Gaussian kernel)

| `ℓ` | `−5.071ℓ^{7/12}` | `+3.859ℓ^{2/3}` | sum (three-term relative correction) |
|---|---|---|---|
| `10⁻⁵` | `−0.0061` | `+0.0018` | `−0.0044` |
| `10⁻⁴` | `−0.0235` | `+0.0083` | `−0.0152` |
| `10⁻³` | `−0.0902` | `+0.0386` | `−0.0516` |
| `10⁻²` | `−0.3455` | `+0.1791` | `−0.1663` |

Each entry is rounded separately from the unrounded coefficients `−5.07106214` (#219) and `3.85949617` (#223) (v1.4,
C3). So at `10⁻⁵` and `10⁻²` the sum differs by one unit in its last digit from the sum of the displayed columns. The
unrounded sums are `−0.00435`, `−0.01522`, `−0.05158` and `−0.16635`.

The combined correction is `1%` at `ℓ ≈ 4.6·10⁻⁵` and `10%` at `ℓ ≈ 3.6·10⁻³`. V3 edit E15's sizes describe the
`ℓ^{1/4}` term only (#214 caution); with this note the manuscript can quote both.

*Status of these numbers (v1.3, xAI P2 in 5378684363; reworded in v1.4, S1).*
- **The coefficients.**
  - `c₁/c_{3,24}` is certified by #219.
  - `c₂/c` is certified for the Gaussian kernel by #223's closed form. Its transfer to the torus `L ≥ 24` is the
    author-side candidate #232.
  - `c_{3,24} = c_{3,∞}(1 + O(e^{−288}))`. The ratios `−5.071` and `3.859` are roundings of these values.
- **The table is the three-term truncation, not a certified prediction of `ν`.**
  - The three-term law holds at candidate status with remainder `O(ℓ^{3/7})` (#229, using #187), with an unspecified
    constant. So the size of the omitted terms at a given `ℓ` is not quantified.
  - In §3's Monte Carlo the elder data exceed the three-term law by about 1–3% on `[10⁻⁴, 3·10⁻²]` (ratios `1.013` and
    `1.026`). The form of the excess is open (exploration).

## 5. Sources (exact identities in `SOURCES.json`)

Merged:
- [R] `frontiers/three_fronts_20260924/LIFETIME_REMAINDER.md` (`247b3ecf`): the kernel, the pin vector and its target;
- `reviews/side24_v1_coefficient_claude_20260929/RESULTS.json`: `c_{2,∞}`;
- `coefficients/side24_v1/ENCLOSURE.json`: `c_{3,24} = c_{3,∞}(1 + O(e^{−288}))`.

Cited, merged since v1.2 (verified from the tree):
- #207 `frontiers/cusp_second_order_20261001/PROOF.md` (`f6df5a73`): `c₁`, the cusp loss, Theorem CU′;
- #191 `frontiers/remainder_vanishing_20260930/PROOF.md` (`441152df`): the even contact expansion;
- #218 `frontiers/candidate_third_order_20261001/PROOF.md` (`70ca57ef`): Theorem T, (0.1), Lemmas C and F;
- #220 `frontiers/elder_third_order_20261001/PROOF.md` (`c8767dde`): Theorem E3, Lemmas Q, CE, H, S′;
- #229 `frontiers/third_order_rate_20261001/PROOF.md` (`110ed33a`): Theorems T⁺, E3⁺, Remark 1;
- #223 `frontiers/c2_exact_20261001/NOTE.md` (`a2798b87`): `c₂` in closed form, certified enclosures;
- #232 `frontiers/c2_finite_jet_transfer_20261001/PROOF.md` (`54cc4a1a`): `c₂` on the torus, `L ≥ 24`;
- #219 `frontiers/cusp_coefficient_certified_20261001/NOTE.md` (`b2866871`): `c₁` certified, `c₁/c_{3,24}`.

Cited, merged, bound since v1.4:
- #187 `frontiers/far_elder_rate_20260930/PROOF.md` (`07260114`): Theorem F, the far part of (E3.3) and (E3⁺.1);
- #240 `frontiers/elder_cusp_parity_20261002/PROOF.md` (`16a1db06`): §7 item 4, fits of the Monte Carlo residual.

Cited, merged since v1.4 (verified from the tree; the pinned blobs are unchanged; v1.4.1):
- #214 `frontiers/d1_third_order_law_20261001/PROOF.md` (`1591ecee`; merged as `e4ca2b3`): `B₂` and its proof in
  `d = 1` (Theorem 1D);
- #237 `frontiers/candidate_parity_rate_20261001/PROOF.md` (`a97bf528`; merged as `cb73b11`): Remark 4, the Monte
  Carlo residuals.

## 6. Controls

`c2_check.py` uses the standard library only. Its output is `RESULTS.json`, byte-identical under `-O`. Mutants M1–M4 exit 1,
and an unknown label exits 2. The run takes about 30 seconds.
- **T1–T2** `d = 1`: `c = C₀` to `10⁻¹⁰` and `c₂ = 2B₂` to `10⁻⁸`, against #214's closed forms, for the Gaussian kernel and
  the mixture. For the Gaussian kernel `c₂` is also within `10⁻⁸` of #223's closed form (observed `5.7·10⁻¹⁰`; v1.4).
- **T3** `d = 2`: `c = c_{2,∞}` to `10⁻¹⁰`; `c₂` from two `r`-sets, each within `10⁻⁸` of #223's closed form (observed
  `1.9·10⁻⁹` and `2.6·10⁻⁹`; v1.4).
- **T4** `d = 3`: `c = c_{3,∞}` to `10⁻¹⁰`; `c₂` at the grid `(56, 120, 48²)`, at the grid `(40, 80, 32²)` and from the
  second `r`-set, each within `10⁻⁸` of #223's closed form (observed `1.1·10⁻⁹`, `1.0·10⁻⁹` and `1.4·10⁻⁹`; v1.4).
- *Closed forms.* The checker evaluates #223's closed forms with `math.gamma`. It first checks that each lies in #223's
  certified interval, as a transcription control.
- **T5** no `r¹` term: the ratio to `A₀` is below `10⁻⁶` at six test points, while the `r²` ratio is `O(1)`.
- **T6** the overlap term (0.1) in `d = 2`: at four heights, `A₂(b, 0)` from the `r`-fit equals `−12π₀E₀[Y²1{A<0} | b]`
  to `10⁻⁶`. The latter is computed directly from the jets, with `Y = f_xxxx a/12 − γ²/4`. In `d = 1` the same identity
  holds to `2·10⁻¹²` (development check).
- **Mutants,** with the checks that reject them (both modes):
  - M1 drops the finite-part subtraction: T1–T4;
  - M2 takes the `r³` coefficient for `A₂`: T1–T4;
  - M3 uses a wrong sphere measure in `d = 2`: T3;
  - M4 drops the analytic tail: T1–T4.

  Every rejection is computed (v1.4, C1). v1.3 forced the M1 failure of T6 and the M2 failure of T5 by hand, and M2 and
  M4 passed T3 and T4.

What the controls do not test: the formal derivation of §1 in `d ≥ 2`, and the Monte Carlo of §3, which is exploration.

## 7. Review slices

- **A** §0 and §1: the definition of `c₂`, and whether the composite-expansion argument is right. In particular, that the
  overlap term is exactly (0.1).
- **B** §2.1–§2.3: the pinned structure, the `O(r³)` indicator replacement, and the `d = 1` comparison with #214.
- **C** §2.4 and `c2_check.py`: the numerics and their convergence.
- **D** §3–§4: the Monte Carlo method and its interpretation (exploration).

**Changed bytes in v1.4** (against v1.3 at `7e97018`; each change is tagged with its finding ID):
- *Header:* the object label, the v1.4 block, the shortened v1.3 block, the Disposition sentence and the dependency
  list.
- *§0:*
  - the fold expansion and (0.1) with their sources (A1);
  - the adjacent-pair sentence (S3);
  - item 1 (S5, B-06), item 2's accuracy paragraph (C2) and item 3 (D-1);
  - the SIDE24 fraction table (D-6, C3);
  - "Status since v1.2" (S1–S3) and "What is not claimed" (A3).
- *§1:* the interface cancellation (A2), and "#214 (an open PR)".
- *§2.1:* truncation (B-04). *§2.2:* domain, layer size, non-uniformity and kernel scope (B-01 to B-03). *§2.3:* cusp and
  fold components (B-05, B-06). *§2.4:* the errors against #223 (C2).
- *§3:*
  - the Kac–Rice counts with error bars (D-3) and the power of the completeness checks (D-4);
  - the bin spans (Slice D request) and the adjacent-pair label (D-2);
  - "Beyond the three-term law", and the nuisance-term note on the rejected-adjacent fit (D-1);
  - the window counts (D-5).
- *§4:* the rounding note (C3) and the status paragraph (S1).
- *§5:* #187, #240 and #237. *§6:* T1, T3, T4 and the mutants (C1). *§7:* this list.

**Changed bytes in v1.4.1** (against v1.4 at `1bfdf28`):
- *Header:* the object label and the v1.4.1 block.
- *Disposition and dependencies:* #214 and #237 are merged, and the dependency sentence is reworded (C129-A2).
- *§0:* "rests on #214 (merged; …)" and item 1's status sentence.
- *§1:* "in #214 (merged; …)". *§2.2:* the finite-`r` covariance (C129-A1) and the kernel-scope wording.
- *§2.3:* its first sentence. *§3:* `1.8%` (C129-N1), the interval label (C129-R1) and "(#237 Remark 4)".
- *§5:* #214 and #237 move to the merged list. *§7:* "comparison" (N6-2) and this list.

`c2_check.py` and `RESULTS.json` are unchanged in v1.4.1. In v1.4, `c2_check.py` adds the #223 comparisons and drops
the two hand-forced mutant failures, and `RESULTS.json` changes only by the new fields and the object label. No
coefficient value, control value or Monte Carlo ratio changes in either version. v1.3 changed only status text (against
v1.2 at `04c08e1`).
