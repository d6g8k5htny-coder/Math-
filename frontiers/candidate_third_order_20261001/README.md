# The candidate density to third order (CL-CANDIDATE-THIRD-ORDER-20261001-v1)

Author-side proof candidate. Anthropic Claude, 1 October 2026. Scientific effect NONE. Nonauthor review required.

**Statement (Theorem T).** For every `d ≥ 2` and `L > 0`, as `ℓ ↓ 0`,

    ν_cand(ℓ) = c ℓ^{−1/3} + B_{d,L} + I^{cand} ℓ^{1/4} + c₂ ℓ^{1/3} + O(ℓ^{4/11}).

- `c` is the leading constant.
- `B_{d,L}` is the equal-height mass of [Z].
- `I^{cand} = (3^{1/4}/2)c₁` is #207's cusp coefficient.
- `c₂` is the Hadamard finite part `(1/3)∫∫∫[A₂(b, k, u) − A₂(b, 0, u)]k^{−4/3}`. Here `A₂` is the `r²`-coefficient of
  [R]'s two-point kernel at fixed `(b, k, u)`, and `A₂(b, 0, u) = −12π₀E₀[Y²1{A<0} | b]`.

This is the `ℓ^{1/3}` coefficient that Math- #216 defines and computes numerically: `0.22152441` in `d = 2` and
`0.16123405` in `d = 3` (SIDE24) for the Gaussian kernel. Here it is proved to be the third coefficient of the candidate
density in every dimension.

**Corollary T′.** `ν_cand − cℓ^{−1/3} − B_{d,L} − I^{cand}ℓ^{1/4} = O(ℓ^{1/3})`. This is a rate for #207's (CU′.1), and
it closes the open item "a rate for the `o(ℓ^{1/4})`" for the candidate density.

**The three new lemmas.**
- **Lemma F (fold expansion).** `A_r = A₀ + r²A₂ + O(r³(1 + k^{−1}))`. The `r¹` term vanishes by the cancellation of
  #191 and #198. The `r³/k` remainder is the boundary layer of the typed region near `det A = 0`, bounded through an
  eigenvalue-layer estimate (Lemma D).
- **Lemma C (cusp kernel with a rate).**
  `|r^{−2}(A_r − A₀)(b, κr) − (𝒜^{cand} − 𝒜^{con})(b, κ)| ≤ Cr(1 + κ)²(…)` for `κr ≤ 1`. This is a quantitative form of
  #207's CU.4 for the candidate kernel. The proof is a pathwise case analysis (Haynsworth, the sign window), followed
  by a parity argument for the target.
- **Lemma O (overlap).** `(𝒜^{cand} − 𝒜^{con})(b, κ) = A₂(b, 0) + O(κ^{−1})`. This makes the fold-scale finite part match
  the cusp integral.

**The assembly.** It splits `ν_cand − cℓ^{−1/3} − B_{d,L}` at `ρ_f = ℓ^{1/4+1/44}` (fold | cusp) and at
`ρ_c = ℓ^{1/4−1/36}` (cusp | intermediate). #207's Lemma L handles the intermediate and far separations. The exponent
`4/11 = 1/3 + 1/33` is the least in the ledger; checker T1 checks it exactly.

**Not claimed:**
- the elder density's `ℓ^{1/3}` term. That needs an elder Lemma C, a bound for intermediate elder separations, and a far
  elder bound (Remark 1);
- certified constants;
- sharpness of `4/11`;
- uniformity in `d` and `L`.

**Dependencies.**
- *Consumed, unmerged:* Math- #191, #198 and #207. This packet must be rebound if any of them changes.
- *Merged:* [R], [P] (with [E1], [E2], [REC]) and [Z].
- *Cited:* #216, #214, #187, #188, #211 and [C7-K].

**Files.**
- `PROOF.md`.
- `thmT_check.py`: standard library, exact rationals. Its output is `RESULTS.json`, byte-identical under `-O` and on
  CPython 3.10–3.14. The controls are:
  - **T1** the exponent ledger;
  - **T2** Lemma C's case analysis;
  - **T3** its Lipschitz step;
  - **T4** Lemma D's Vandermonde inequality;
  - **T5** the product structure (2.2) on exactly pinned polynomial fields in `d = 2, 3`.

  Mutants M1–M4 exit 1, and an unknown label exits 2.
- `SOURCES.json`: the exact identities of all sources.

**Review record.** Before submission, a clean-context same-family referee read the whole note. It reported no major
issue; its five minor findings and eight nits are applied. Same account, zero organizational independence.

**Review slices** (PROOF §8):
- **A** Lemma D, (1.2) and Lemma F;
- **B** Lemma C;
- **C** Lemma O and the assembly.
