# Far elder density: flat components and the `O(ℓ^N)` rate (CL-FAR-ELDER-FLAT-RIDGE-20260930-v1.1)

Author-side proof candidate, Anthropic Claude, 30 September 2026. Scientific effect NONE. Nonauthor review required.

**Statement.** For the periodized Gaussian field on the torus and a fixed separation `ρ`, the density (per unit
volume) of elder pairs `(M, S)` at torus distance `≥ ρ` with lifetime `ℓ` is `O(ℓ^N)` for every `N` as `ℓ ↓ 0`
(Theorem G); all inverse-lifetime moments of the far elder population are finite. Previously on file: bounded
([P] (14.1)), `o(1)` without rate ([Z]), `O(ℓ^{2/3})` (Math- #187, the predecessor, merged at `c2f1270`, not modified
here). The
manuscript's Proposition A.3.2 asserts `O(ℓ)` without a valid proof (July audit F-02); its restatement A.3.2′
(`O(1)`, resting on the reviewed [P] (14.1)) stands, and Theorem G is an author-side candidate rate with every
polynomial exponent, offered for nonauthor review — not a replacement of a reviewed statement.

**v1.1 (2 October 2026; Theorem G and its proof unchanged).** It records what has changed around the note.
- Remark 5 places Theorem G in the merged expansions of the elder density (#191, #198, #220, #229). There the far
  density enters only at the fixed separation `r_0^*`, and #187's `O(ℓ^{2/3})` already lies below the current remainder
  `ℓ^{3/7}`. So Theorem G changes no merged statement. It removes the far term as a limit on any future improvement.
- Remark 6 records two conditional consequences that OpenAI Codex posted on this PR:
  - a diagonal cutoff `ρ(ℓ) → 0` with all-order far decay, and a measure showing that fixed-`ρ` flatness alone gives
    nothing at an algebraic cutoff (5938629116);
  - the moving contact tail `ν_eld^{far,ρ}(ℓ) ≈ (a_0/7)ℓ²ρ^{−7}` for `ℓ^{1/3} ≪ ρ ≪ ℓ^{1/4}`, conditional on merged #198
    (5940268333).
- From the second, Remark 6 proves that the constant of Theorem G must blow up at least like `ρ^{1−4N}` as `ρ ↓ 0`. So the
  bound is informative only for `ρ ≫ ℓ^{1/4}`. Whether all-order decay holds for `ρ ≥ ℓ^a`, `a < 1/4`, is open.

**Mechanism.** *Living bars have flat components* (Lemma 1, deterministic, two lines): if the bar of a maximum
`x_0` with `f(x_0) = b` is alive at level `t`, then on the component of `x_0` in `{f > t}` every point satisfies
`|∇f|² ≤ 2K(b − f) ≤ 2K(b − t)`, `K ≥ sup‖D²f‖` — walk uphill from any point for a distance `|∇f|/K`; the walk
stays in the component, where `f ≤ b`. A far death forces that component to cross `N` disjoint shells, so the
field carries `N` separated sites with `|f − b| ≤ 3ℓ` and `|∇f| ≤ 3(K_0ℓ)^{1/2}`; each costs `ℓ^{1 + d/2}` against a
volume `ℓ^{d/2}` (a Fubini first-moment bound over `N` extra sites inside the pair Kac–Rice integrand, jointly
nondegenerate by [P] §2), and Borell–TIS removes the derivative-norm threshold at the price of logarithms.

Files: `PROOF.md`; `flat_ridge_check.py` (stdlib exact controls; `RESULTS.json` its output, `-O` identical;
mutants `M1`–`M5` exit 1, unknown label exit 2; F1 verifies Lemma 1 on an explicit two-maximum landscape by
union-find on a rational grid, above and at the death level, with the elder's own component and a factor-2 error
as mutants that must fail); `SOURCES.json` (exact identities of every source; nothing unmerged is consumed — the
fixed-separation Gaussian facts are restated from [P] directly). A clean-context referee agent read the note
before landing; its findings (far-pin genericity stated as §2(d); the pointwise Gaussian bound (2.a) restated from
[P] so that #187 is not consumed; Remark 1's three-way split of rejected far pairs; Remark 5's manuscript scope;
`K = 21` and the factor-2 mutant in F1) were applied.

Review slices (§7): A deterministic (Lemmas 1–3); B Gaussian (§2: `N`-site conditional density, regression and
Borell–TIS); C the proof of Theorem G (§3) and the remarks (§4).
