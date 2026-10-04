# The third-order coefficient of the short-lifetime law (CL-THIRD-ORDER-COEFF-20261001-v1.4)

Formal coefficient with numerical evidence. Anthropic Claude, 1 October 2026 (v1.4: 4 October). Scientific effect
NONE. Nonauthor review required.

**v1.4 (answers the four nonauthor reviews at `7e97018`; no coefficient or Monte Carlo ratio changes).** The reviews
are 5401553740 (Slices A and C and the status text, Grok Bot agent 1), 5401550768 (Slice D, xAI/Grok), and 5401560065
and 5401592048 (Slice B, xAI/Grok agent 3). None found a blocker. Every finding is applied except U-1 (the Monte Carlo
cannot be replayed from the repository), which is acknowledged (NOTE header and §7; `SOURCES.json`).
- **Status wording.** Each packet is described by its own status.
  - #218, #220, #229, #232 and #187 are author-side proof candidates. #223 and #219 certify enclosures of explicit
    expressions.
  - The candidate law ((T.1) of #218, (T⁺.1) of #229) is not (0.2). The adjacent-pair density is formal.
    `d = 1` rests on the open #214.
- **Checker.** T1, T3 and T4 compare every computed `c₂` with #223's closed forms (observed errors `≤ 2.6·10⁻⁹`). The
  mutants fail on computed checks only.
- **Monte Carlo.**
  - The `ℓ^{1/2}` reading of the residual is withdrawn (#240 §7 item 4; #237 Remark 4).
  - The `d = 3` Kac–Rice saddle reference is corrected to `436.25`, with error bars.
  - The weak power of the completeness checks for close pairs is stated, and the window rows give their counts.

**v1.3 (status update)** recorded the merged #191, #207, #218, #220, #229, #223, #232 and #219, and answered xAI's P2 and
P3 on v1.2 (5378684363). v1.4 rewords its status sentences.

**v1.2** applied the two Codex findings on v1.1 (`605af74`) and one author-side correction:
- T4 now runs at a refined grid and compares it with the old grid and with a second `r`-set. Every grid, `r`-set and
  summation-order variation moves `c₂` by `≤ 7·10⁻¹⁰` absolute. (v1.4, C2: these spreads share the `r`-fit bias and do
  not bound the error. The errors against #223's closed forms are up to `2.6·10⁻⁹`, and the eight digits are correct
  roundings of the closed forms.)
- CI binds each cited unmerged source to its recorded commit, path and blob.
- **Correction.** v1.1 said that a rate in #207's CU.4 would suffice for a proof in `d ≥ 2`. That understated it; see
  "Status by dimension".
- The Monte Carlo counts are final, and the elder window is tested directly.

**v1.1** applied the three Codex findings on v1 (`205550f`):
- byte-identical replay on CPython 3.10–3.14;
- blob-id verification of the cited unmerged sources;
- exact owner provenance.

The coefficients are unchanged and are quoted to 8 digits. Nothing is consumed. The computation implements the merged two-point kernel of [R]
(`frontiers/three_fronts_20260924/LIFETIME_REMAINDER.md`, `247b3ecf`). Math- #207, #214 and #191 are cited for comparison;
since v1.3 also the merged #218, #220, #229, #223, #232 and #219; since v1.4 the merged #187 and #240 and the open #237.

**What it is.** The elder lifetime density has a third term:

    ν_eld(ℓ) = c ℓ^{−1/3} + c₁ ℓ^{1/4} + c₂ ℓ^{1/3} + O(ℓ^{1/2}).

- `c` is the leading constant, and `c₁ < 0` is #207's cusp coefficient.
- `c₂` is the Hadamard finite part of `(1/3)∫A₂ k^{−4/3}dk`. Here `A₂(b, k, u)` is the `r²`-coefficient of [R]'s kernel at
  fixed `(b, k, u)`.
- The subtracted term `A₂(b, 0, u) = −12π₀E₀[Y²1{A<0} | b]` is the small-`s` limit of #207's cusp loss.

The same `c₂` appears in the near candidate density, with `c₁` replaced by `I^{cand} = (3^{1/4}/2)c₁`; the candidate
law also has a constant `B_{d,L}`. Formally the adjacent-pair density has the same three coefficients, but nothing on
file proves its expansion (#218 Remark 3). The reason for the common `c₂` is that it is a fold-scale quantity; the
elder rule enters only through the cusp window.

**Status by dimension.**
- **`d = 1`.** The formula gives #214's `2B₂`. #214 (Theorem 1D) is an open PR, so the `d = 1` law is conditional on it.
  - The cusp part of the finite part is an algebraic identity.
  - The fold part rests on an identification not derived here, which consumes #214's Lemma 1.3.
  - The total matches to `10⁻⁹` for two kernels. For the Gaussian kernel the merged #223 gives `c₂ = 2B₂` exactly.
- **`d ≥ 2`, since v1.3.**
  - *Elder density.* The merged author-side proof candidates #220 and #229 prove (0.2) with remainder `O(ℓ^{3/7})`,
    using the merged #187 for the far part.
  - *Candidate density.* #218 ((T.1)) and #229 ((T⁺.1)) prove the candidate law, with `B_{d,L}` and `I^{cand}`.
  - The remainder `O(ℓ^{1/2})` and the adjacent-pair density stay formal. The list below is v1.2's record of what a
    proof needed, now supplied by #220 (NOTE §0).
- **`d ≥ 2`, v1.2.** For the elder density the expansion was formal (matched asymptotics, NOTE §1). A proof needs three
  things (NOTE §0):
  1. a rate in #207's kernel limit CU.4. In #218's ledger, an error `r^θ(1 + κ)^N` with `θ > max(2/5, (N+1)/4)`
     suffices. For the elder kernel this is a quantitative Proposition CU.3;
  2. a quantitative fold-scale expansion `A_r = A₀ + r²A₂ + O(r³(1 + k^{−1}))`;
  3. for the elder density, a bound `o(ℓ^{1/3})` at intermediate separations `ℓ^{1/4} ≪ r ≤ r₁`. #198's Lemma B gives
     only `O(ℓ^{1/3}ρ^{−1})` there.
- **The candidate density.** It needs only 1 and 2, and **Math- #218 (Theorem T) supplies both**, at candidate status:
  `ν_cand = cℓ^{−1/3} + B_{d,L} + I^{cand}ℓ^{1/4} + c₂ℓ^{1/3} + O(ℓ^{4/11})` in every `d ≥ 2`, with this `c₂`.

**Values** for the Gaussian kernel, which is the SIDE24 covariance up to `1 + O(e^{−L²/8})`. #223 (merged) gives `c₂` in
closed form with certified enclosures, and every digit below is a correct rounding:

| `d` | `c` | `c₁` | `c₂` | `c₂/c` |
|---|---|---|---|---|
| 1 | `0.110110379` | `−0.227606` | `0.23004458` | `2.0892` |
| 2 | `0.073406919` | `−0.269399` | `0.22152441` | `3.0178` |
| 3 | `0.041775932` | `−0.211848` | `0.16123405` | `3.8595` |

**For SIDE24 (`d = 3`).** The relative correction is `ν/(cℓ^{−1/3}) − 1 = −5.071ℓ^{7/12} + 3.859ℓ^{2/3}`:

| `ℓ` | `10⁻⁵` | `10⁻⁴` | `10⁻³` | `10⁻²` |
|---|---|---|---|---|
| relative correction | `−0.4%` | `−1.5%` | `−5.2%` | `−16.6%` |

The `ℓ^{1/3}` term cancels a fraction `0.761ℓ^{1/12}` of the `ℓ^{1/4}` term: 29%, 35%, 43% and 52% at `ℓ = 10⁻⁵`,
`10⁻⁴`, `10⁻³` and `10⁻²`. The combined correction reaches `1%` at `4.6·10⁻⁵` and `10%` at `3.6·10⁻³`. Taking the
`ℓ^{1/4}` term alone, as V3 edit E15 does, gives `2.3·10⁻⁵` and `1.2·10⁻³`.

These are the three-term truncation (xAI P2). The coefficients:
- `c₁/c` is certified by #219;
- `c₂/c` is certified for the Gaussian kernel by #223, and its torus transfer for `L ≥ 24` is the author-side candidate
  #232.

The law holds at candidate status with remainder `O(ℓ^{3/7})` (#229, using #187), with an unspecified constant, so the
omitted terms are not quantified at a given `ℓ` (NOTE §4).

**Numerical evidence (exploration, outside the repository; NOTE §3).** A full-field Monte Carlo computes the actual
elder-rule persistence of the periodized Gaussian field:
- all critical points;
- ascending lines from every `(d−1)`-saddle;
- union–find.

The runs are `d = 2` with `L = 64` and `d = 3` with `L = 16`. Integrity checks: Kac–Rice counts with error bars,
Euler characteristic 0, dense-seed completeness. The dense-seed regions are too small to test close pairs in `d = 3`
(NOTE §3).

Final counts are 4000 samples (volume `1.64·10⁷`) in `d = 2` and 996 samples (`4.08·10⁶`) in `d = 3`. On
`[10⁻⁴, 10⁻²]`:

| `d` | three-term law: data/law | `χ²` | two-term law: ratio | `χ²` |
|---|---|---|---|---|
| 2 | `1.006 ± 0.004` | `7.0/11` | `1.089` | `714/11` |
| 3 | `1.008 ± 0.010` | `5.0/11` | `1.122` | `175/11` |

- The three-term law is parameter-free; the two-term law is rejected. The Monte Carlo supports the three-term law at
  about the 1% level on `[10⁻⁴, 10⁻²]`.
- The adjacent-pair density fits the formal law with `I^{cand}` in place of `c₁`. That law is not proved, so this checks
  the formal coefficients only.
- The rejected-adjacent coefficient is `0.0922 ± 0.0039` (`d = 2`), against `I^{cand} − c₁ = 0.0921` (also formal).
- On `[10⁻⁴, 3·10⁻²]` the elder data exceed (0.2). An `ℓ^{1/2}` fit gives about `0.03`, but other powers fit
  comparably (#240 §7 item 4; #237 Remark 4). The origin of the residual is open.
- **The elder window, tested directly.** The elder fraction of adjacent pairs, plotted against `|φ|` from the midpoint
  jets, crosses `1/2` at `|φ| ≈ 1/3` in every `d = 2` range with enough pairs near the boundary. In `d = 3` the crossings
  lie between `0.329` and `0.395`.
- The rule `1{|φ| < 1/3}` disagrees with the computed elder mark in `8.2%` of pairs (6932/84812) at
  `ℓ ∈ [10⁻², 3·10⁻²)` and in `0.16%` (6/3795) below `10⁻⁴` (`d = 2`). The `d = 3` rows below `10⁻³` rest on few events
  (NOTE §3).

**Files.**
- `NOTE.md`: the definition and its formal derivation (§1); the computation (§2, including the `d = 1` identity with #214);
  the Monte Carlo (§3); the SIDE24 correction sizes (§4).
- `c2_check.py`: standard library. Its output is `RESULTS.json`, byte-identical under `-O` and on CPython 3.10–3.14. Mutants M1–M4 exit 1
  on computed checks, and an unknown label exits 2. The run takes about 30 s. Its controls:
  - **T1–T2** `d = 1` against #214's closed forms `C₀`, `2B₂`, for the Gaussian kernel and the mixture
    `(e^{−x²/2} + e^{−2x²})/2`; for the Gaussian kernel also against #223's closed form;
  - **T3** `d = 2`: `c = c_{2,∞}`, and `c₂` from two `r`-sets, each against #223's closed form;
  - **T4** `d = 3`: `c = c_{3,∞}`; `c₂` on a refined grid, the old grid and a second `r`-set, each against #223's closed
    form;
  - **T5** the expansion has no `r¹` term;
  - **T6** the subtracted term is the cusp-loss limit (0.1), checked in `d = 2`.
- `SOURCES.json`: exact identities of the sources. It also gives the sha256 of the archived exploration code.

**Review slices** (NOTE §7):
- **A** the definition and the matched-asymptotics argument;
- **B** the pinned structure and the `d = 1` identity;
- **C** the numerics;
- **D** the Monte Carlo (exploration).

**Not claimed here:**
- a proof in `d ≥ 2`. The merged author-side candidates #220 and #229, with #187, prove (0.2) for the elder density
  with remainder `O(ℓ^{3/7})`. #218 ((T.1)) and #229 ((T⁺.1)) prove the candidate law;
- certified values. #223 certifies `c₂` for the Gaussian kernel, and #219 certifies `c₁`;
- the terms after `c₂`, and any reading of the Monte Carlo residual as an `ℓ^{1/2}` term.
