# The candidate density with remainder `ℓ^{3/5}`: no `ℓ^{1/2}` term

**Author-side proof candidate (Anthropic Claude). Scientific effect: NONE. Nonauthor review required.**

Object `CL-CANDIDATE-PARITY-RATE-20261001-v1.1`. Full text: [`PROOF.md`](PROOF.md).

**v1.1 (wording only).** The six nonblocking corrections of the C55 nonauthor reviews are applied; no estimate or
conclusion changes (see *Review record*). `parity_check.py` changed in one docstring and one comment; `RESULTS.json` is
byte-identical to v1.

## Result

For every `d ≥ 2` and `L > 0`, as `ℓ ↓ 0`:

    ν_cand(ℓ) = c ℓ^{−1/3} + B_{d,L} + I^{cand} ℓ^{1/4} + c₂ ℓ^{1/3} + O(ℓ^{3/5})                 (P.1)

Math- #218 proved this with `O(ℓ^{4/11})` and Math- #229 with `O(ℓ^{3/7})`. Since `3/5 > 1/2`, **the candidate density
has no term of order `ℓ^{1/2}`** (Corollary P′), although #218 §0 and #229 §0 name `ℓ^{1/2}` as the formal next order.

## The three ingredients

| | Statement | Role |
|---|---|---|
| **Parity and reflection** (Lemmas R, Π, K) | After the birth height is integrated out, the field splits into independent even and odd parts, and the pin rows are even in the separation `r`. Hence `Π = −det K_M det K_S = 36k²Δ² + r²(12kΔV − U²) + O(r⁴)`. Point reflection `z ↦ −z` maps the problem at gap `k` to the one at `−k`, so the fold coefficient `𝐀₂` is even in `k`. | The pathwise evenness is in #191 Lemma E Step 3. The basis and the `k`-parity of `𝐀₂` are in #232 (§§1, 3, Theorem J). New: the reflection is applied to the conditional laws inside the cusp layer. |
| **Lemma U** (uniform two-scale kernel) | For `k ≥ r²`, the birth-integrated kernel is `r^{−2}𝐀_0 + [𝐀₂(k) − 𝐀₂(0)] + 𝓐(k/r)` up to `O(r² + r min(k, 1/k))`. Here `𝓐` is the birth-integrated cusp kernel `𝒜^{cand} − 𝒜^{con}`. | One region replaces #218's fold/cusp split. The boundary layer of the fold expansion is identified as the cusp kernel's tail, and the `O(r)` cusp correction vanishes. |
| **Lemma Λ** (the gap inside the layer) | Moving the gap from `k` to `0` inside the layer `{|U| > 6κ|det A|}` costs `O(k²/(1 + κ))`. The first order vanishes by reflection. The kink is controlled through the density of its location, using Lemma D″ (two small eigenvalues) for the exceptional set. | Replaces #229 Remark 2's kink bound `O(κk²)`. |

#229 Remark 1 explains why a two-region argument stops at `3/7`: two matching pairs of error terms have unidentified
leading coefficients. Lemma U removes both pairs. There is no split point and so no truncation, and the linear cusp
error vanishes inside Lemma U (Step U2 (b), Lemma Λ).

The remaining terms `ρ³`, `ℓ²ρ^{−7}` and `ℓρ^{−2}` balance at `ρ = ℓ^{1/5}`, the edge `k = r²` of Lemma U's range. Lemma K's
`O(k²)` is not needed for (P.1): #218's `C¹` bound gives the same exponent.

## Dependencies

| | Sources |
|---|---|
| Consumed (all merged) | #218 (`70ca57ef`, merged 1 Oct at `fb6ee97`): §0; §1 (Lemma D, `T`, (1.2)); Steps F1 and F3; (F.2) and the surrogate remark; Step C1; Lemma O's proof; §4. #207 (`f6df5a73`, merged 1 Oct at `566b1a1`): §0, §4 (4.1), §7 (Lemma L, `I^{cand}`). [R], [P] with [E1]/[E2]/[REC], [Z], #191 (`r_0^*`, (2.1), Lemma E Step 4), #198 ((W.4)) |
| Cited | #229 (Theorem T⁺, superseded for `ν_cand`; Remarks 1–2); #232 (merged at `7fe06b0`: an independent derivation of (2.2) and of the `k`-parity of `𝐀₂`); #216 and #223 (`c₂`; #223 also certifies `c`); #214 (`d = 1`); #220 (the elder density; not used) |

Every consumed source is merged, with the reviewed blob. The workflow checks every pin in the tree, and binds the
cited unmerged sources to their recorded heads.

## Controls

`parity_check.py` uses the standard library and exact rationals. Its output is `RESULTS.json`, byte-identical under `-O`
and on CPython 3.10–3.14 (a few seconds).

| Control | Checks |
|---|---|
| Q1 | The ledger: least `3/5` at `ρ = ℓ^{1/5}`, attained by `ρ³`, `ℓ²ρ^{−7}`, `ℓρ^{−2}`. The split is optimal. The exponent is still `3/5` without Lemma K. The closed form of `∫ r min(k, 1/k) dr` is evaluated (a consistency identity). |
| Q2 | On fourteen exactly pinned polynomial fields (`d = 1, 2, 3, 4`): pinned jets are even in `r`; `Π` is even; the reflection maps `k` to `−k`; at fixed free jets, `det K_M` and `det K_S` are affine in `k`, checked at `d + 1` values. |
| Q3 | (2.2) exactly on the same fields, with the general `Δ_BB` and `A^♯_B`. The `d = 4` fields fail the old `m ≤ 2` shortcut, so they test the `m ≥ 3` terms. The parities of `U` and `V` are checked. |
| Q4 | Lemma K for the Gaussian kernel. The `A`-integrand `H(k, A)` of the birth-integrated `r²` coefficient has only `k⁰, k², k⁴` terms (`d = 1, 2, 3`). The `d = 1, 2` polynomials are #232's. |
| Q5, Q6 | The pointwise algebra of Step U2, including the Case 3 identity, and the inequalities that collect Lemma U's errors. Three of Q6's four relations are identities, recorded as consistency checks. |

Mutants `M1`–`M8` each fail only their own control, and an unknown label exits 2. M8 moves the saddle's Hessian to
`r/2 + r⁴`, which breaks the endpoint symmetry of `Π`: its evenness in `r` and its reflection invariance, both in Q2.

    python3 -B -S parity_check.py                 # exit 0, output = RESULTS.json
    python3 -B -S parity_check.py --mutant M3     # exit 1

The controls check exact algebra, symmetry and arithmetic. The Gaussian layer estimates (Lemmas D″, Λ₀, Λ, U) are proved
in prose only.

## Review record

Two clean-context same-family referees (Anthropic Claude subagents) reviewed the note before submission. Referee A took
§§0–3 and referee B took §§4–8, the controls and this README. Each read the whole note against all sources at their
declared blobs.

**First pass: MAJOR REVISION, narrow.** Each referee found local defects with explicit repairs. None falsified Theorem P,
but two left steps of its written proof incomplete or incorrect; both are repaired.
- Lemma Λ's exceptional set did not cover `d ≥ 4`, so the proof was incomplete there. It is repaired with Lemma D″, a
  full Vandermonde bound `P(D < ε) ≤ Cε²`.
- Step U2's Case 3 bullet was false as written, because `U` is not small there. It now compares with the layer
  integrand.
- Remark 2 misidentified what fixes `3/5`, and its route to `ℓ^{2/3}` was wrong. It is rewritten.

**Other fixes applied.** Seventeen minor findings and thirteen nits, including:
- the kink computation of Lemma Λ, made rigorous with a change of variables;
- the smoothness argument for Lemma K, by conditioning on `A`;
- Lemma R's quantifiers and the even/odd decomposition (R.2);
- Lemma Λ₀ stated for random shifts and interpolated laws;
- Step U2 (a)'s first-piece bound near `κ = r`, and Step U2 (b)'s restriction to Case 1;
- Step U3, which no longer relies on #229 Remark 2;
- attribution to #191 Step 3 and #232;
- citations: #207 §4 (4.1), #214 §0, and #223's certified values;
- notation clashes;
- the controls: Q3 with general `m` and `d = 4`, `K_S` affinity, the new M8, and honest labels for Q1, Q2, Q4 and Q6;
- `SOURCES.json` and the workflow, added before submission.

**Second pass (delta check of the revision).** Referee A: **ACCEPT** for §§0–3, with six nits. Referee B: **ACCEPT WITH
MINOR FIXES** for §§4–8, with three minor items and six nits. All are applied, including:
- the one substantive item, Step U2 (b)(iii): the factor `Δ` of `ΔV_o` cancels the `1/|Δ|` of the `f₄`-window length,
  uniformly in `Δ`;
- the wording on the elder and rejected residuals: the single-power scan does not single out `ℓ^{1/2}`;
- the archive of the exploration scripts.

**The referees' independent checks.**
- (2.1)–(2.2) were re-derived symbolically for `d = 1, 2, 3` and checked exactly for `d = 2`–`5`.
- The typed criterion and the Case 1 decomposition were checked against true inertias on 80,000 random matrices
  (`d = 2`–`5`), with no mismatch.
- Exact finite-`r` conditioning confirmed Lemma K and Q4 for `d = 1, 2`.
- Lemma Λ toys (`m = 1, 2, 3`) show `κ(Λ(k) − Λ(0))/k²` flat in `κ`, and `P(D < ε) ∝ ε^{2.5–3}`.
- A `d = 2` Gaussian-kernel Monte Carlo with exact finite-`r` conditioning matched `𝐓_r − 𝐒_r` to the layer term at 18
  points, to 1–2%. At fixed `κ` it found no `O(r)` term: the relative linear coefficient was `−0.007 ± 0.011` at `κ = 1`
  and `−0.065 ± 0.041` at `κ = 2`. The `k²/κ` coefficient of the layer was nonzero, about `+0.005`.
- In the same model, the cost of Step U2 (b)(iii) satisfies `κG(k)/k ∈ [0.0002, 0.0066]` for `κ ∈ {5, 20, 80}`.
- Control replay was byte-identical on 3.10–3.14 with and without `-O`, for the reviewed and the revised packet, and the
  mutant matrix was clean.

**Independence.** The referees are the same provider and the same GitHub account as the author, so they carry zero
organizational independence. Nonauthor review is required; the review slices are in PROOF §9.

**Nonauthor review (C55: OpenAI Codex, delegated AI review, on head `a6b6788`, PROOF blob `97298f32`).** All three
slices are PASS_TECHNICAL at their stated scope. Organizational independence is 0, and Dylan Roy's personal reading is
pending.
- *Slice A* (§§1–2: Lemmas R, Π, K), review 5385194600. Two nonblocking precision notes.
- *Slice B* (§3: Lemmas D′, D″, Λ₀, Λ), review 5385169112. Two nonblocking prose corrections and one clarification.
- *Slice C* (§§4–5: Lemma U and the assembly), review 5385136758, with the addendum 5940107723. One nonblocking
  correction.

Each correction is applied in v1.1, as follows.

| Review item | v1.1 |
|---|---|
| A: `det K_i` affine in `k` | at fixed free jets only, not along the laws `Q̄_{r,k}` (Lemma Π, its proof, Q2) |
| A: signed-`k` moments | `1 + \|k\|` in the moment bounds before Lemma Π and in Lemma Π |
| B-01: `φ″ = 2` off `{\|y\| = θ}` | `φ″ = 2·1{\|y\| > θ} + 2θ(δ_{−θ} + δ_θ)` as a distribution |
| B-02: the density `ρ(λ)` | the unnormalized Weyl slice `c_m q_{A\|𝐠}(O diag(λ, λ′)Oᵀ)\|𝒱\|dλ`, integrated over `dλ′ dO dP_𝐠` |
| B-02: the case `m = 1` | `adj A = 1`, so `β`, `Y₁`, `Y₂` do not depend on `λ`, and the suprema are finite |
| C-N1: the `f₄`-windows | two one-sided crossing strips of length `\|a\|`, `a = 3kΔ_B`, centred at `±6κ\|Δ\| − a/2` (total `72k\|Δ_B\|/\|Δ\|`; `144` if centred at the old thresholds) |

## Not claimed

- sharpness of `3/5`. The next ledger term is `ℓ^{2/3}`, and reaching it would need Lemma U for `𝐓_r(k) − 𝐓_r(0)` on all
  `k > 0` (PROOF Remark 2).
- anything new about the elder or rejected densities. The Monte Carlo of #216 suggests that they carry further terms
  that the adjacent-pair density does not (PROOF Remarks 3–4).
- certified values of `I^{cand}` or `B_{d,L}`; uniformity in `d` or `L`.
