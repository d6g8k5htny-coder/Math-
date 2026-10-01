# The elder density to third order (CL-ELDER-THIRD-ORDER-20261001-v1.1)

Author-side proof candidate. Anthropic Claude, 1 October 2026. Scientific effect NONE. Nonauthor review required.

**Statement (Theorem E3).** For every `d ≥ 2` and `L > 0`, as `ℓ ↓ 0`,

    ν_eld(ℓ) = c ℓ^{−1/3} + c₁ ℓ^{1/4} + c₂ ℓ^{1/3} + ν_eld^{far,r_0^*}(ℓ) + O(ℓ^{4/11}),   0 ≤ ν_eld^{far,r_0^*}(ℓ) ≤ C ℓ^{1/3}.   (E3.0)

Hence:

    ν_eld(ℓ) = c ℓ^{−1/3} + c₁ ℓ^{1/4} + O(ℓ^{1/3});                      (E3.1)
    ν_eld(ℓ) ≥ c ℓ^{−1/3} + c₁ ℓ^{1/4} + c₂ ℓ^{1/3} − C ℓ^{4/11};            (E3.2)

and, by Math- #187's Theorem F (merged on 1 October 2026) at the one separation `ρ = r_0^*` (the far elder density
there is `O(ℓ^{2/3})`),

    ν_eld(ℓ) = c ℓ^{−1/3} + c₁ ℓ^{1/4} + c₂ ℓ^{1/3} + O(ℓ^{4/11}).           (E3.3)

- (E3.0) reduces the elder third-order law exactly to the far elder density at the fixed separation `r_0^*`. The law
  holds with remainder `O(ℓ^θ)`, `θ ≤ 4/11`, if and only if that far density is `O(ℓ^θ)`.
- `c₁ < 0` is #207's cusp coefficient (CU.2).
- `c₂` is #218's (0.1): the fold-scale Hadamard finite part that Math- #216 defines and computes (`0.16123405` in `d = 3`
  for the Gaussian kernel; a numerical approximation, not certified).
- (E3.1) is a rate for #207's (CU.1), which claimed none.

**Corollary E3′ (the rejected density).** With Theorem T (#218),
`ρ_rej = B_{d,L} + (I^{cand} − c₁)ℓ^{1/4} − ν_eld^{far,r_0^*}(ℓ) + O(ℓ^{4/11})`. In particular:
- `ρ_rej = B_{d,L} + (I^{cand} − c₁)ℓ^{1/4} + O(ℓ^{1/3})`, a rate for #207's (CU′.2);
- `ρ_rej ≤ B_{d,L} + (I^{cand} − c₁)ℓ^{1/4} + Cℓ^{4/11}`;
- under #187, `ρ_rej = B_{d,L} + (I^{cand} − c₁)ℓ^{1/4} + O(ℓ^{4/11})`. The candidate and elder densities have the same
  `ℓ^{1/3}` coefficient, so the rejected density has no `ℓ^{1/3}` term.

**What changed in v1.1.** v1 bounded the intermediate separations by an `ε`-argument (`Cℓ^{1/3}r₁^β`, then `r₁ ↓ 0`).
So its (E3.3) had no rate, and it needed #187 at every small separation. v1.1 replaces v1's Lemma B′ with Lemmas H and
S′. The intermediate separations then contribute `O(ℓ^{2/5})`, and only the far part at the fixed radius `r_0^*` is
left. #207's Lemma CU.5 is no longer consumed.

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
- **Lemma H (the rescaled Hessian at `M`; new in v1.1).** `H̃ = D_r^{−1}D²f(M)D_r^{−1}`, with `D_r = diag(r, 1, …, 1)`,
  equals `−6κe_ue_uᵀ` plus explicit segment integrals of `∂_u⁴f` and `∂_u²∇_Θf` (the exact form (H.1)). It is a
  Gaussian with covariance between `cI` and `CI` uniformly in `r ≤ r_0^*`, by [P] §2's linear independence at `r > 0`
  and at `r = 0`. This is the conditional variance bound for the axial curvature under the pins that #198 Remark 1
  asks for.
- **Lemma S′ (new in v1.1).** `E_Q[(W_r/r²)e] ≤ Cℓ^{2/3}r^{−2}(κ + r)P^N` for `r ≤ r_0^*` and `k ≤ r`.
  - #198's barrier puts `λ_min(−H̃)` below `Cℓ^{1/3}r^{−2}`.
  - Lemma D for `H̃` charges that event twice: once in `|det H̃|` and once in probability.

**The assembly.** It uses #218 §4's decomposition and ledger with the elder kernel, so the least exponent is again `4/11`.
- The fold-region elder deficit is `O(ρ_f⁵/ℓ)`, by [C7-K] (K2).
- The intermediate separations `[ρ_c, r_0^*]` contribute `O(ℓ^{2/5})`: #198 (W.1) below `ℓ^{2/15}`, Lemma S′ above.
- The far part `ν_eld^{far,r_0^*}` is kept in (E3.0). #198 Lemma F′ bounds it by `Cℓ^{1/3}`, and #187 by `Cℓ^{2/3}`.

**Numerical illustration (exploration).** The elder-pair row of Math- #216 v1.2's full-field Monte Carlo uses the exact
elder rule, by union–find. It fits the three-term law with data/law `1.006 ± 0.004` in `d = 2` and `1.008 ± 0.010` in
`d = 3`, and rejects the two-term law.

**Not claimed:**
- (E3.3) and Corollary E3′(3) without #187;
- sharpness of `4/11`;
- certified constants;
- uniformity in `d` or `L`;
- anything about the adjacent-pair density.

**Dependencies.**
- *Consumed, unmerged:* Math- #207 and #218. This packet must be rebound if either changes.
- *Consumed, merged:* Math- #191 and #198 (merged on 1 October 2026 with the blobs consumed here); #187 (merged on
  1 October 2026 at `c2f1270` with the blob consumed here), for (E3.3) and Corollary E3′(3) only, at `ρ = r_0^*`; [R],
  [P] (with [E1], [E2], [REC]), [C7-K] and [Z].
- *Cited:* #216, #188.

**Files.**
- `PROOF.md`.
- `e3_check.py`: standard library, exact rationals. Its output is `RESULTS.json`, byte-identical under `-O` and on
  CPython 3.10–3.14; the run takes about 11 s. The controls are:
  - **X1** the exponent ledger, with the intermediate split at `ℓ^{2/15}`;
  - **X2** the ridge identities;
  - **X3** the margins and the sharpness of `3/2`;
  - **X4** the one-dimensional decision under perturbation, in all three cases;
  - **X5** the weighted Taylor structure on exactly pinned polynomial fields in `d = 2, 3`;
  - **X6** Lemma S and the `C⁰`/`C²` polynomial bounds;
  - **X7** the pointwise facts of Lemmas CE and O′;
  - **X8** Lemma S′'s linear algebra (`det H_M = r² det H̃`; `λ_min(−H_M) ≥ r²λ_min(−H̃)` by principal minors; a negative witness at `r = 2`);
  - **X9** Lemma H's exact form (H.1) on exactly pinned polynomial fields, and its `r = 0` values.

  Mutants M1–M8 exit 1, and an unknown label exits 2.
- `SOURCES.json`: the exact identities of all sources.

**Review record.**
- v1, same-family: a clean-context referee read the whole note against its sources. Verdict: ACCEPT WITH MINOR FIXES,
  with no major finding; its four minor findings and nine nits are applied. A delta check of the revision by the same
  referee: ACCEPT. Its two-dimensional union–find test of Lemma Q's decision agreed in 48 of 48 exactly pinned fields
  (floating point; exploration).
- v1, nonauthor (on #220, at head `6da0715`):
  - OpenAI / Codex (delegated) reviewed Slices A, B and C, each PASS_TECHNICAL at its stated scope. It requested two
    amendments. OA-220-B-01 (the integrability hypothesis of Lemma G (b)) is applied. OA-220-C-01 (v1 Remark 2's
    shrinking cut-off) is superseded, because v1.1 has no shrinking cut-off.
  - xAI checked the ridge identities of Lemma Q with sympy.
- v1.1, same-family: a clean-context referee read the v1 → v1.1 delta against all eight sources. Verdict: ACCEPT WITH
  MINOR FIXES, with no major finding; one minor finding and eleven nits, all applied. Its delta check of the fixes:
  ACCEPT.

Same account, zero organizational independence.

**Review slices** (PROOF §8):
- **A** §1: Lemma CU.1′, Lemma S and Lemma Q;
- **B** §2: Lemma G and Lemma CE;
- **C** §§3–4: Lemmas O′, H and S′, and the assembly.
