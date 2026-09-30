# The remainder of Theorem R has a rate: `ν_eld(ℓ) = cℓ^{−1/3} + O(ℓ^{1/4})` (CL-D2-REMAINDER-RATE-20260930-v1.1)

Author-side proof candidate, Anthropic Claude, 30 September 2026. Scientific effect NONE. Nonauthor review required.
**Depends on Math- #191** (Theorem R+ (R+.3), all of Lemma E through (E.1), and its §2; unmerged author-side candidate
of this session, v1.1 blob `441152df`):
this packet cannot be integrated before #191 and must be rebound if #191 changes. Everything else consumed is
merged and reviewed: [R] Theorem R, [C7-K], [182] (the deterministic barrier), [Z], the reconciled [P] chain.

**Statement (Theorem R++).** For the periodized Gaussian field on the fixed torus (every `d ≥ 2`, `L > 0`) and the
canonical marked Kac–Rice version of the elder lifetime density, there are `C, ℓ_0` depending on `d, L` only with

    |ν_eld(ℓ) − cℓ^{−1/3}| ≤ C ℓ^{1/4}    (0 < ℓ ≤ ℓ_0),      i.e.      ν_eld(ℓ) = cℓ^{−1/3}(1 + O(ℓ^{7/12})).

Theorem R (D2) gave `O(1)`; #191 gave `o(1)` with a rate only conditionally (on unmerged far-elder packets and on
a polynomial `ρ`-dependence of their constants). This packet gives the rate unconditionally, modulo #191's Lemma E.

**Mechanism.** Split the elder density by separation at `ρ = ℓ^{1/12}` and at the fixed radius `r_0^*`. Below `ρ`:
**Lemma W** (sign window) — on the support of the typed weight the two scaled endpoint determinants have opposite
signs, and by #191 Lemma E Steps 1–3 they are `∓6k det A_0 + rY + O(r²)` with the *same* `rY`, so `|rY| ≤ 6k|det A_0|
+ O(r²)` and `E_Q[W_r/r²] ≤ C(k² + r⁴(1 + k)²)P^N` — improving [C7-K] (K1)'s `(k + r)²` at `k < r`; with it the
candidate excess over the contact law below `ρ` is `C(ℓ^{1/4} + ρ³ + ℓ²ρ^{−7})` (sharpening #191 (R+.3)) and the
rejected mass below `ρ` is `C(ℓ^{1/4} + ρ³)` (sharpening [C7-K] §4), and the equal-height kernel mass of Theorem Z
below separation `ρ` is `O(ρ³)`. Between `ρ` and `r_0^*`: **Lemma B**
— every elder pair of lifetime `ℓ` is born at a maximum whose weakest curvature is `≤ (ℓK²/c_L)^{1/3}` ([182] §3's
deterministic barrier, applied under the near-pair regression law of [R] whose moment and density bounds
(R4), (R5), (R9) are uniform in `r ≤ r_0^{[R]}`), so the typed weight is `≤ Cℓ^{1/3}r^{−1}(k + r)K^{d−1/3}T^d` and the
elder mass at separations in `[ρ, r_0^*)` is `≤ Cℓ^{1/3}(ρ^{−1} + ℓρ^{−5})`. Beyond `r_0^*`: **Lemma F′**, the same barrier
under the far regression law of [P] §14 / [Z] §2, `≤ Cℓ^{1/3}` (Math- #187 has `ℓ^{2/3}`; not needed). The ledger at
`ρ = ℓ^{1/12}` has eight terms, five of them `ℓ^{1/4}`, the others `ℓ^{17/12}`, `ℓ^{11/12}`, `ℓ^{1/3}`; `1/4` is now fixed by
the transition `r = k` at separation `ℓ^{1/4}` (the (E.1) excess below it, (K2)'s loss, and the tail of the leading
law), independently of `ρ`.

v1 → v1.1 (same day, before any nonauthor read): v1 had the rate `1/6` from (R+.3) and [C7-K] §4 directly (ledger at
`ρ = ℓ^{1/6}`); the clean-context referee pass on v1 suggested the sign window as a heuristic; Lemma W is its rigorous
form and needs only the sign structure of the typed weight plus Lemma E's Steps 1–3 (the assembly still needs (E.1)
below separation `ℓ^{1/4}`). v1's ledger survives as a parenthetical in §4 and in checker E1. A second referee pass
on v1.1's §§3–5 found Lemma W proved and the assembly correct; its findings (the dependency on all of Lemma E, the
eight-term count, `k ≥ 0` in Lemma W, the `min(ℓ^{1/4}, ρ)` form of (W.2), notation, and the rewriting of Remark 1 —
its own formal computation replaces v1.1's wrong "not expected to be the true order") were applied.

**Not claimed:** sharpness of `1/4` in either direction — Remark 1 records, as unproved, the second referee pass's
formal leading-order computation indicating that `ℓ^{1/4}` is the true order with a *negative* coefficient (the
contact law overcounts at the cusp scale `r ≍ k ≍ ℓ^{1/4}`); numerical constants; a rate for the candidate remainder
or for `ρ_rej → B_{d,L}`; uniformity in `d, L`.

Files: `PROOF.md`; `rate_ledger_check.py` (stdlib exact controls; `RESULTS.json` its output, `-O` identical; mutants
`M1`–`M4` exit 1, unknown label exit 2: both exponent ledgers and their optimality within the ledger, the barrier's
algebra, the soft-eigenvalue determinant inequality on rational orthogonal conjugates, the integrals and the
[C7-K] cutoff ledger, the sign-window inequality of Lemma W); `SOURCES.json` (exact identities of every merged source; #191 recorded as consumed-unmerged
with its blob, #187/#188 as cited-unmerged). A clean-context referee agent (same provider; not a nonauthor
review) read a first version before landing: no error found in Lemma B, Lemma F′, the decomposition or the ledger;
it confirmed Lemma E's Steps 1–3 symbolically on pinned quintics in `d = 2, 3`; its thirteen findings (the
canonical-version wording of the statement, a false sentence and an overclaim in Remark 1, Remark 3's gating,
citation precision for [R] §4 / [Z] (Z14) / [P] §2, the range `[r_0^*, diam X]`, `ρ ≤ r_0^*`, the explicit uniformity of
(R+.3)'s constant, the provenance of [182]'s barrier review) were applied.

**What the controls do not test.** Lemma B, Lemma F′ and Lemma W as statements about the Gaussian laws (the
expansions imported from #191 Lemma E, the moments, the Kac–Rice disintegrations), and the assembly's use of #191
and [C7-K] §4, are prose only. Review slices (PROOF.md §8): A Lemma B; B Lemma F′; C Lemma W and (W.2)–(W.4); D the
assembly, provenance and remarks.
