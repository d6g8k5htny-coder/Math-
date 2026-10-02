# The elder cusp kernel: the candidate rate, and no linear term at fixed `κ`

**Author-side proof candidate (Anthropic Claude). Scientific effect: NONE. Nonauthor review required.**

Object `CL-ELDER-CUSP-PARITY-20261002-v1`. Full text: [`PROOF.md`](PROOF.md).

## Results

| | Statement | Compared with |
|---|---|---|
| **Lemma Q′** (§1) | #220's elder decision lemma with relaxed margins: `Γ = \|γ\|/λ` becomes `Γ̃ = \|A^{−1}γ\|`, the ridge maximizer is located in a ball of radius `max(1, 8ḡ/λ)`, and every `φ` is decided (two new cases, `φ > 1` and `φ < −1`). | #220 Lemma Q needs `8C₁𝒩r(1 + 5Γ) ≤ λ` and `\|φ\| ≤ 1`. |
| **Proposition CE⁺⁺** (§2) | The elder cusp kernel with error `Cr(1 + κ)`, the candidate's rate. | #229 (CE⁺.1): `C(r(1 + κ) + κ²r^{3/2} + κ³r²)`. The two elder-only rows of #229's ledger disappear; `3/7` is unchanged. |
| **Theorem N** (§§3–5) | For `κ` in a compact subset of `(0, ∞)`: the elder and the candidate cusp kernels have **no `O(r)` term**, pointwise in the birth height; the error is `O(r²)`. | #237 (open) proves this for the candidate after the `b`-integral (Lemma U); its Remark 3 records the elder case as formal only. |
| **Corollary N′** (§6) | In every fixed window `κ₀ ≤ ℓ/r⁴ ≤ κ₁`, the elder, candidate and rejected densities are `(const)·ℓ^{1/4} + O(ℓ^{3/4})`: no `ℓ^{1/2}` term. | The formal `ℓ^{1/2}` term of #218 §0 and #229 §0 would come from an `O(r)` cusp correction. |

**The mechanism.** Both first-order effects at the cusp scale are multiples of one jet polynomial,

    Q₁ = f₅/120 − ηᵀA^{−1}γ/12 + γᵀA^{−1}BA^{−1}γ/8,

the coefficient of the quintic ridge correction `rQ₁X(X² − ¼)²`:
- the edges of the elder window move from `|φ| = 1/3` to `|φ| = 1/3 + rQ₁/(2κ)` (Lemma Q″, the `d ≥ 2` form of #238's Lemma W);
- the typed weight changes by `12κrΔ²Q₁`: in #232's expansion, the first-order parts of `12kΔV` and `−U²` combine into
  `12kΔ²Q₁` (Lemma Ω, via `ΔJ_B = Δ_BJ − JBJ`).

`Q₁` is odd under the point reflection of the jets and every zeroth-order quantity is even. So the `O(r)` term is
`r·E[Q₁Ψ_κ]` with `Ψ_κ` even, which is `O(rk)` by the parity factorization (#220 (F7)).

**What is not claimed.** Nothing about the whole elder density beyond #229's `O(ℓ^{3/7})`. Theorem N is not uniform as
`κ → ∞` (the soft region `λ ≈ |γ|²/κ`, where the expansion is in `k`, not `r`) or as `κ → 0` (the intermediate
separations). Remark 1 of `PROOF.md` gives the conditional ledger: a uniform version would give `ℓ^{4/9}log(1/ℓ)`, still
short of `ℓ^{1/2}`, because the fold family `ρ_f⁵/ℓ` balances `ℓ²ρ_f^{−5}` at `ℓ^{1/2}`.

## Dependencies

| | Sources |
|---|---|
| Consumed (all merged) | #220 (`c8767dde`, merged at `0d79778`): §1 (Lemma CU.1′, Lemma S, Lemma Q, (M1)–(M6)), §2 ((F1)–(F7), Lemma G, Lemma CE). #229 (`110ed33a`, merged at `6f74f7a`): Lemma L, Lemma CE⁺, §5. #218 (`70ca57ef`): Lemma D, (1.2), Step F1, Step C1, Step C3. #232 (`54cc4a1a`): §2 (2.1)–(2.4). #207 (`f6df5a73`): §0, Theorem CU.2, Proposition CU.3, (4.1). [R], [P], #191 (Lemma E Step 3) |
| Cited (open) | #237 (Lemma Π, Lemma K, Lemma U, Remarks 3–4), #238 (Lemma W), #216 (Monte Carlo) |

## Controls

`ecp_check.py` uses the standard library and exact rationals. Its output is `RESULTS.json`, byte-identical under `-O` and
on CPython 3.10–3.14 (under a second).

| Control | Checks |
|---|---|
| X1 | Lemma Q′'s `C⁰`, `C¹`, `C²` polynomial bounds and the constant `220`; `\|q\| ≥ λΓ̃²` and the trace bound on random negative definite rational matrices; the constants of the sufficient conditions (2.3). |
| X2 | The model ridge: (M1), (M4), the new cases of Step Q6′, the constants near the edges (`c₃ = 281/128`, `c₄`), and the expansions (3.4) with `\|Ψ₂\| ≤ 90`, `\|ω_±\| ≤ 120`, proved by exact Bernstein positivity on `\|t\| ≤ 1/96`. |
| X3 | Pinned polynomial fields: the window field is `𝔓 + r𝔔 + O(r²)` with the monomial bound of Lemma CU.1″ (`d = 2, 3`); #232's family (2.4) in window coordinates; Lemma Ω (a) at orders `r⁰`–`r³` (`d = 2, 3, 4`). |
| X4 | `ΔJ_B = Δ_BJ − JBJ` (including singular `A`), (4.2), `P₁ = Δ²Q₁`, `V_o = ΔQ₁ + α₄Δ_B`, `𝔔(X, Ξ*) = Q₁X(X² − ¼)²`, and the parities. |
| X5 | The first-order bookkeeping: edge values of `w₀`, the edge shift `36rQ₁`, `I′(0) = Ψ_κ/36` on polynomial test densities, the candidate's kink windows. |
| X6 | Corollary N′'s integral, #229's ledger with and without the elder-only rows (`3/7` both), and the conditional ledger of Remark 1. |

Mutants `M1`–`M7` each fail exactly their own control, and an unknown label exits 2.

    python3 -B -S ecp_check.py                 # exit 0, output = RESULTS.json
    python3 -B -S ecp_check.py --mutant M3     # exit 1

The controls check exact algebra, model constants and arithmetic. The probabilistic estimates are proved in prose only.

## Exploration (not part of the proof)

`d = 2`, Gaussian kernel (project archive `V2_2/frontiers_elder_cusp_parity_20261002/exploration/`; numpy, scipy, mpmath):
- `cusp_quad.py`: `𝒜^{cand}`, `𝒜^{eld}` by quadrature under the contact law.
- `elder_f4int.py`: the kernels at `r > 0` by Monte Carlo under the exact pinned law. Common random numbers across six `r`,
  antithetic odd jets, `f₄` integrated in closed form, the elder interval in `f₄` by bisection. The fitted levels agree with
  the quadrature. The rejected kernel's linear coefficient is consistent with zero at all four `(b, κ)` points; at `κ = ½`
  it is `0.04 ± 0.04` of the absolute first-order scale `E|Q₁Ψ_κ|` (`first_order_scale.py`).
- `altfit.py`: on #216's archived Monte Carlo, two-power residual fits with `ℓ^{2/3} + ℓ^{3/4}` and with `ℓ^{1/2} + ℓ^{3/4}`
  are comparable (`|Δχ²| ≤ 2.6`); the data do not single out `ℓ^{1/2}`.

## Review record

One clean-context same-family referee (an Anthropic Claude subagent) read the note, the checker and the consumed
sources at their declared blobs, re-derived Lemmas Q′, R₂, Q″ and Ω and Steps N1–N6 by hand, verified the Lemma Ω identity
symbolically, the model constants with mpmath, and the edge location `±(1/3 + rQ₁/(2κ)) + O(r²)` numerically on #232's
exact family. Verdict: **no blocking error**. One MAJOR finding and eleven MINOR ones, all applied before submission:
- MAJOR: in Step N2 the edge windows were integrated in `f₄` on an event that involves `f₄`. The `f₄`-free event `𝔊″` is
  now introduced, on which the windows have bounded width and lie near `3q ± 24κ`, and the term `k|P₁|` is bounded by
  `c_eκ²Δ²` there.
- MINOR: conditioning for Lemma D when the threshold involves `f₄`; the definition of `𝔅_4′` (as #229's); `r₂′ ≤ r₂`; the
  orders of the pin corrections in Lemma CU.1″; the citation (F1); the exponent `N₂` in the margin on `|Δ|`; `≥ 0` in the
  case identity; Remarks 2–4 (the candidate fit artefact, the `χ²` order, the rejected-adjacent counts); the description
  of the controls and the mutants.

Same GitHub account and same provider as the author: zero organizational-independence credit. Nonauthor review is
required for every slice (`PROOF.md` §10).
