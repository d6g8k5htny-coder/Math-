# The third-order lifetime laws with remainder `ℓ^{3/7}`

**Author-side proof candidate (Anthropic Claude). Scientific effect: NONE. Nonauthor review required.**

Object `CL-THIRD-ORDER-RATE-20261001-v1`. Full text: [`PROOF.md`](PROOF.md).

## Result

For every `d ≥ 2` and `L > 0`, as `ℓ ↓ 0`:

    ν_cand(ℓ) = c ℓ^{−1/3} + B_{d,L} + I^{cand} ℓ^{1/4} + c₂ ℓ^{1/3} + O(ℓ^{3/7})                 (T⁺.1)
    ν_eld(ℓ)  = c ℓ^{−1/3} + c₁ ℓ^{1/4} + c₂ ℓ^{1/3} + ν_eld^{far,r_0^*}(ℓ) + O(ℓ^{3/7})          (E3⁺.0)
    ν_eld(ℓ)  = c ℓ^{−1/3} + c₁ ℓ^{1/4} + c₂ ℓ^{1/3} + O(ℓ^{3/7})        (with merged #187)      (E3⁺.1)
    ρ_rej(ℓ)  = B_{d,L} + (I^{cand} − c₁) ℓ^{1/4} + O(ℓ^{3/7})            (with merged #187)      (R⁺.1)

Math- #218 and #220 proved these with `O(ℓ^{4/11})`. Also:
- the elder density from intermediate separations is `O(ℓ^{4/9}log(1/ℓ))`; #220 had `O(ℓ^{2/5})`;
- **Proposition W⁺**, the typed-window bound `E_Q[W_r/r²] ≤ Cr²(κ + r)²(κ + r log(2/r))P^N` for `k ≤ r`;
- at `k = 0`, the equal-height kernel satisfies `r^{d−1}Ψ_0(b, ru) = O(r³log(2/r))`, so the equal-height mass below
  separation `ρ` is `O(ρ⁴log(2/ρ))`. This sharpens #198 (W.4) and proves, up to a factor `log(2/r)`, the order that
  #211 suggests heuristically.

## The three new ingredients

| | Statement | Replaces |
|---|---|---|
| **Lemma L** | `|(c² − y²)₊ − (c² − y′²)₊| ≤ |y − y′|(|y| + |y′|)`: a Lipschitz constant free of `c = 6κ|det A|` (the inequality #218 Step C3 already uses, now applied where the global constant was) | the constant `12κ|det A|` in #218 Step C2 and #220 Step E3, the source of `(1 + κ)²` |
| **(3.1)–(3.2)** | on the elder decision's edge window, `|f₄| ≥ 6κ` or `λ ≤ |γ|²/(2κ)`, so the window costs `O(rκ)` | #220's `O(rκ²)` for `𝔅_4` |
| **Proposition W⁺** | the typed window `|Y| ≤ 6κ|det A| + O(r)` has conditional probability `O(κ + r/|det A|)` (`Y` is affine in `f₄`) | #198 (W.1), which does not charge the window |

So the cusp kernels have errors `Cr(1 + κ)` (candidate, Lemma C⁺) and `C(r(1 + κ) + κ²r^{3/2} + κ³r²)` (elder,
Lemma CE⁺), where #218 and #220 have `Cr(1 + κ)²`. With the splits `ρ_f = ℓ^{2/7}`, `ρ_c = ℓ^{2/9}` and `a = ℓ^{1/9}`,
four error terms are exactly `ℓ^{3/7}` and all others are `O(ℓ^{4/9}log(1/ℓ))`.

## Dependencies

| | Sources |
|---|---|
| Consumed, unmerged | #207 (`f6df5a73` at `782211f`), #218 (`70ca57ef` at `0cf048d`), #220 (`736a35de` at `e481d23`) |
| Consumed, merged | [R], [P] with [E1]/[E2]/[REC], [Z], [C7-K], #191, #198, and #187 (`07260114`, merged 1 Oct at `c2f1270`; used only for (E3⁺.1) and the second form of (R⁺.1)) |
| Cited | #216, #223 (`c₂`); #211 (Remark 3); #188 |

The packet cannot be integrated before #207, #218 and #220, and must be rebound if any of them changes. The workflow
checks every pin, including the current head (or the merge commit) of each consumed pull request.

## Controls

`r37_check.py` uses the standard library and exact rationals. Its output is `RESULTS.json`, byte-identical under `-O`
and on CPython 3.10–3.14.

| Control | Checks |
|---|---|
| R1 | the exponent ledger: least `3/7`, attained exactly by the stated terms; others `≥ 4/9`; split hypotheses; optimality of the splits; regressions to `4/11` (#218) and `2/5` (#220); Remark 1's max–min |
| R2 | Lemma L, with equality instances |
| R3 | (3.2), on scalar instances and on exact rational matrix instances `m = 1, 2, 3` |
| R4 | the sign window, (4.1), the exact length of the `f₄`-window, the splitting inequality |
| R5, R6 | the bookkeeping of Proposition W⁺ and of Lemmas C⁺, CE⁺ |

Mutants `M1`–`M8` each fail only their own control, and an unknown label exits 2:

    python3 -B -S r37_check.py                  # exit 0, output = RESULTS.json
    python3 -B -S r37_check.py --mutant M1      # exit 1

## Review record

- **Same-family referee.** A clean-context referee (Anthropic Claude) read the note against all ten sources at their
  declared blobs. Verdict: **ACCEPT WITH MINOR FIXES**, with no major finding. Its two minor findings and twelve nits
  are applied:
  - Remark 1's account of which terms block a further improvement;
  - the parity statements of §2 and Remark 2 are now consistent.
- **The referee's independent checks:**
  - an exact ledger;
  - Lemma L on 93,025 grid points;
  - (3.2) on 5,400 matrix instances;
  - 20,000 bookkeeping instances;
  - a `d = 2` Gaussian-field Monte Carlo of Proposition W⁺.
- **Independence.** The referee is the same provider and the same GitHub account as the author, so it carries zero
  organizational independence. Nonauthor review is required. The review slices are in PROOF §9.

## Not claimed

- sharpness of `3/7`; the formal next term is of order `ℓ^{1/2}`;
- certified constants;
- uniformity in `d` or `L`;
- the adjacent-pair density.
