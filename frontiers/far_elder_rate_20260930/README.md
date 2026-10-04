# Far elder density rate (CL-FAR-ELDER-RATE-20260930-v1)

**Erratum 1 (4 October 2026):** `ERRATUM_20261004.md` records that the §0 SIDE24 manuscript and audit (F-02)
citations are context only and not repository sources. It answers the second-provider read 5975813301; the mathematics
reads PASS, and no mathematical change follows.

Author-side proof candidate, Anthropic Claude, 30 September 2026. Scientific effect NONE. Nonauthor review required.

**Statement.** For the periodized Gaussian field on the torus and a fixed separation `ρ`, the density (per unit
volume) of elder pairs `(M, S)` at torus distance `≥ ρ` with lifetime `ℓ` is `O(ℓ^{2/3})` as `ℓ ↓ 0` (Theorem F).
Previously on file: bounded ([P] (14.1)) and `o(1)` without rate ([Z]). The manuscript's Proposition A.3.2 asserts
`O(ℓ)` without a valid proof (July audit F-02); Theorem F is the proven replacement, with the weaker exponent.

**Mechanism.** Every finite bar of lifetime `ℓ` is born at a maximum whose weakest curvature is at most
`(ℓK²/c_L)^{1/3}` (Lemma 1, deterministic; the barrier of Math- #182 §3, re-proved here). Under the Kac–Rice weight
`|det H_M|` the soft eigenvalue costs `∫_0^{u} λ dλ ≍ u²`, i.e. `ℓ^{2/3}`; Markov's inequality conditional on the
pins and both Hessians keeps the derivative norm inside the weighted integral (Math- #182 §§2–4's route, transplanted
to a far saddle pinned at gap `ℓ`, made uniform over the compact separation set).

Files: `PROOF.md`; `far_elder_check.py` (stdlib exact controls; `RESULTS.json` its output, `-O` identical; mutants
`M1`–`M4` exit 1, unknown label exit 2); `SOURCES.json` (exact identities of every source; nothing unmerged is
consumed). A clean-context referee agent read the note before landing; its findings (F2 framing, the far rejected
limit on `D_ρ`, credit to #182's method, wording of the heuristic) were applied.

Review slices (§7): A deterministic (Lemma 1; xAI is the provider distinct from both #182's author and this one);
B Gaussian (§§2–3); C consequences (Corollaries F1–F2, §4).
