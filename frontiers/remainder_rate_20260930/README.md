# The remainder of Theorem R has a rate: `ν_eld(ℓ) = cℓ^{−1/3} + O(ℓ^{1/6})` (CL-D2-REMAINDER-RATE-20260930-v1)

Author-side proof candidate, Anthropic Claude, 30 September 2026. Scientific effect NONE. Nonauthor review required.
**Depends on Math- #191** (Theorem R+ (R+.3), unmerged author-side candidate of this session, v1.1 blob `441152df`):
this packet cannot be integrated before #191 and must be rebound if #191 changes. Everything else consumed is
merged and reviewed: [R] Theorem R, [C7-K], [182] (the deterministic barrier), [Z], the reconciled [P] chain.

**Statement (Theorem R++).** For the periodized Gaussian field on the fixed torus (every `d ≥ 2`, `L > 0`) and the
canonical marked Kac–Rice version of the elder lifetime density, there are `C, ℓ_0` depending on `d, L` only with

    |ν_eld(ℓ) − cℓ^{−1/3}| ≤ C ℓ^{1/6}    (0 < ℓ ≤ ℓ_0),      i.e.      ν_eld(ℓ) = cℓ^{−1/3}(1 + O(ℓ^{1/2})).

Theorem R (D2) gave `O(1)`; #191 gave `o(1)` with a rate only conditionally (on unmerged far-elder packets and on
a polynomial `ρ`-dependence of their constants). This packet gives the rate unconditionally, modulo #191's Lemma E.

**Mechanism.** Split the elder density by separation at `ρ = ℓ^{1/6}` and at the fixed radius `r_0^*`. Below `ρ`:
#191 (R+.3) bounds the candidate density's deviation from the contact law by `C(ρ + ℓ²ρ^{−7})` and [C7-K] §4
(the proof of (T1) with cutoff `ρ`) bounds the rejected mass by `C(ℓ^{1/4} + ρ)`. Between `ρ` and `r_0^*`: **Lemma B**
— every elder pair of lifetime `ℓ` is born at a maximum whose weakest curvature is `≤ (ℓK²/c_L)^{1/3}` ([182] §3's
deterministic barrier, applied under the near-pair regression law of [R] whose moment and density bounds
(R4), (R5), (R9) are uniform in `r ≤ r_0^{[R]}`), so the typed weight is `≤ Cℓ^{1/3}r^{−1}(k + r)K^{d−1/3}T^d` and the
elder mass at separations in `[ρ, r_0^*)` is `≤ Cℓ^{1/3}(ρ^{−1} + ℓρ^{−5})`. Beyond `r_0^*`: **Lemma F′**, the same barrier
under the far regression law of [P] §14 / [Z] §2, `≤ Cℓ^{1/3}` (Math- #187 has `ℓ^{2/3}`; not needed). The ledger at
`ρ = ℓ^{1/6}` is `ℓ^{1/6} + ℓ^{5/6} + ℓ^{1/4} + ℓ^{1/6} + ℓ^{1/6} + ℓ^{1/2} + ℓ^{1/3}`.

**Not claimed:** sharpness of `1/6` (Remark 1 records two routes past it, one suggested by the referee pass);
numerical constants; a rate for the candidate remainder or for `ρ_rej → B_{d,L}`; uniformity in `d, L`.

Files: `PROOF.md`; `rate_ledger_check.py` (stdlib exact controls; `RESULTS.json` its output, `-O` identical; mutants
`M1`–`M3` exit 1, unknown label exit 2: the exponent ledger and its optimality within the ledger, the barrier's
algebra, the soft-eigenvalue determinant inequality on rational orthogonal conjugates, the integrals and the
[C7-K] cutoff ledger); `SOURCES.json` (exact identities of every merged source; #191 recorded as consumed-unmerged
with its blob, #187/#188 as cited-unmerged). A clean-context referee agent (same provider; not a nonauthor
review) read a first version before landing: no error found in Lemma B, Lemma F′, the decomposition or the ledger;
it confirmed Lemma E's Steps 1–3 symbolically on pinned quintics in `d = 2, 3`; its thirteen findings (the
canonical-version wording of the statement, a false sentence and an overclaim in Remark 1, Remark 3's gating,
citation precision for [R] §4 / [Z] (Z14) / [P] §2, the range `[r_0^*, diam X]`, `ρ ≤ r_0^*`, the explicit uniformity of
(R+.3)'s constant, the provenance of [182]'s barrier review) were applied.

**What the controls do not test.** Lemma B and Lemma F′ as statements about the Gaussian laws, and the assembly's
use of #191 (R+.3) and [C7-K] §4, are prose only. Review slices (PROOF.md §7): A Lemma B; B Lemma F′; C the assembly,
provenance and remarks.
