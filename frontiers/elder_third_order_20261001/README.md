# The elder density to third order (CL-ELDER-THIRD-ORDER-20261001-v1)

Author-side proof candidate. Anthropic Claude, 1 October 2026. Scientific effect NONE. Nonauthor review required.

**Statement (Theorem E3).** For every `d ≥ 2` and `L > 0`, as `ℓ ↓ 0`,

    ν_eld(ℓ) = c ℓ^{−1/3} + c₁ ℓ^{1/4} + O(ℓ^{1/3});                      (E3.1)
    ν_eld(ℓ) ≥ c ℓ^{−1/3} + c₁ ℓ^{1/4} + c₂ ℓ^{1/3} − C ℓ^{4/11};            (E3.2)

and if, in addition, Math- #187's Theorem F holds (the far elder density is `O(ℓ^{2/3})` at each fixed separation),

    ν_eld(ℓ) = c ℓ^{−1/3} + c₁ ℓ^{1/4} + c₂ ℓ^{1/3} + o(ℓ^{1/3}).           (E3.3)

- `c₁ < 0` is #207's cusp coefficient (CU.2).
- `c₂` is #218's (0.1): the fold-scale Hadamard finite part that Math- #216 defines and computes (`0.16123405` in `d = 3`
  for the Gaussian kernel; a numerical approximation, not certified).
- (E3.1) is a rate for #207's (CU.1), which claimed none.

**Corollary E3′ (the rejected density).** With Theorem T (#218):
- `ρ_rej = B_{d,L} + (I^{cand} − c₁)ℓ^{1/4} + O(ℓ^{1/3})`, a rate for #207's (CU′.2);
- `ρ_rej ≤ B_{d,L} + (I^{cand} − c₁)ℓ^{1/4} + Cℓ^{4/11}`;
- under #187, `ρ_rej = B_{d,L} + (I^{cand} − c₁)ℓ^{1/4} + o(ℓ^{1/3})`. The candidate and elder densities have the same
  `ℓ^{1/3}` coefficient, so the rejected density has no `ℓ^{1/3}` term.

**The new lemmas.**
- **Lemma Q (the elder decision with explicit margins).** This is #207's Proposition CU.3 made quantitative. The elder
  decision is `1{|φ| < 1/3}` whenever the rescaled ridge is within `(3/2)κ||φ| − 1/3|` of the model ridge in `C⁰` and
  within `κ/4` in `C²`. Both distances are `O(𝒩r(1 + |γ|/λ)²)`, by Lemma CU.1′ (`Ξ`-weighted Taylor bounds) and Lemma S
  (a Schur-complement perturbation bound). The margin constant `3/2` is sharp, with equality at `φ = 1`.
- **Lemma CE (the elder cusp kernel with a rate).**
  `|r^{−2}(A_r^{eld} − A_0)(b, κr) − (𝒜^{eld} − 𝒜^{con})(b, κ)| ≤ Cr(1 + κ)²(…)`. This is the candidate rate of #218
  Lemma C. Wrong decisions cost little because the weight `36κ²Δ²` vanishes to second order in the transverse concavity
  `λ`. The passages to the contact law and to the zero-gap target use Gaussian comparisons (Lemma G), which need no
  regularity of the jumping elder loss.
- **Lemma O′ (elder overlap).** `𝒜^{cand} − 𝒜^{eld} = O(1/κ)`, so the elder cusp loss tends to `A₂(b, 0)` like the
  candidate loss.
- **Lemma B′ (intermediate separations).** #198's barrier, times the sign window, times #207 CU.5's typed probability,
  gives `Cℓ^{1/3}r₁^β` on `[ℓ^{1/5}, r₁]`.

**The assembly.** It uses #218 §4's decomposition and ledger with the elder kernel, so the least exponent is again `4/11`.
- The fold-region elder deficit is `O(ρ_f⁵/ℓ)`, by [C7-K] (K2).
- The far part is `O(ℓ^{1/3})` by #198 Lemma F′, which gives (E3.1).
- With #187's `O(ℓ^{2/3})` and `r₁ ↓ 0`, the far part gives (E3.3).

**Numerical illustration (exploration).** The elder-pair row of Math- #216 v1.2's full-field Monte Carlo uses the exact
elder rule, by union–find. It fits the three-term law with data/law `1.006 ± 0.004` in `d = 2` and `1.008 ± 0.010` in
`d = 3`, and rejects the two-term law.

**Not claimed:**
- a rate in (E3.3);
- (E3.3) without #187;
- certified constants;
- uniformity in `d` or `L`;
- anything about the adjacent-pair density.

**Dependencies.**
- *Consumed, unmerged:* Math- #191, #198, #207 and #218; for (E3.3) and Corollary E3′(3) only, #187. This packet must be
  rebound if any of them changes.
- *Merged:* [R], [P] (with [E1], [E2], [REC]), [C7-K] and [Z].
- *Cited:* #216, #188.

**Files.**
- `PROOF.md`.
- `e3_check.py`: standard library, exact rationals. Its output is `RESULTS.json`, byte-identical under `-O` and on
  CPython 3.10–3.14; the run takes about 10 s. The controls are:
  - **X1** the exponent ledger, with the intermediate terms;
  - **X2** the ridge identities;
  - **X3** the margins and the sharpness of `3/2`;
  - **X4** the one-dimensional decision under perturbation, in all three cases;
  - **X5** the weighted Taylor structure on exactly pinned polynomial fields in `d = 2, 3`;
  - **X6** Lemma S and the `C⁰`/`C²` polynomial bounds;
  - **X7** the pointwise facts of Lemmas CE and O′.

  Mutants M1–M5 exit 1, and an unknown label exits 2.
- `SOURCES.json`: the exact identities of all sources.

**Review record.** Before submission, a clean-context same-family referee read the whole note against its sources.
- Verdict: ACCEPT WITH MINOR FIXES, with no major finding. Its four minor findings and nine nits are applied.
- A delta check of the revision by the same referee: ACCEPT.
- The referee's two-dimensional union–find test of Lemma Q's decision agreed in 48 of 48 exactly pinned fields
  (floating point; exploration).

Same account, zero organizational independence.

**Review slices** (PROOF §8):
- **A** §1: Lemma CU.1′, Lemma S and Lemma Q;
- **B** §2: Lemma G and Lemma CE;
- **C** §§3–4: Lemmas O′ and B′, and the assembly.
