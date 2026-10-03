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

**Extension C89 (incorporated 3 October 2026; `PROOF.md` and Theorem G unchanged).** OpenAI / Codex
(`root01a0bbb5`) proved a quantitative, moving-cutoff form of Theorem G on this PR. A separate OpenAI / Codex
reviewer passed it as PASS_TECHNICAL_SCOPED, with organizational independence 0. It is kept here byte for byte.
- `C89_V1_1_PROOF.md`, Theorem QSF (comment 5963100306). Write `F(ℓ, ρ)` for [G]'s density (0.1) at separation `≥ ρ`.
  For every integer `q ≥ 1` put `N = 2(q + 1)`, `J = (d + 1)(d + 2)/2` and `A_N = 24J + 12dN + 12N(N + 1)(d + 1)`.
  Then `F(ℓ, ρ) ≤ C_q ρ^{−A_N} ℓ^{q+1}` for `0 < ρ ≤ min(1, L/4)` and `0 < ℓ ≤ ρ²/(64N²)`. Consequences:
  - `F(ℓ, ℓ^β) = O(ℓ^q)` for each fixed `0 < β ≤ 1/A_N`;
  - `F(ℓ, c[log(e/ℓ)]^{−a}) = O(ℓ^q)` for every fixed `q`.

  In `d = 2` with `q = 1`, `A_N = 960`, so `F(ℓ, ℓ^{1/960}) = O(ℓ)`.
- `C89_V1_PROOF.md`, the historical v1 (comment 5963042579). It keeps its AMEND: its explicit constant was a
  maximum of bounds where the product `C_* = C_Q C_R C_Z` is needed.
- `C89_V1_1_REVIEW.md` is the full review (comment 5963217842). `c89_reviewer_controls.py` and
  `c89_reviewer_stdout.json` are the reviewer's script and its stdout, exactly as published there.
- `c89_replay.py` re-runs that script on the exact sources: [P], this packet's `PROOF.md` as [G], and the C89
  copy. It requires the published stdout byte for byte, and it checks that an altered C89 copy changes the output.

**What C89 uses from [G].** It uses (0.1), Lemmas 1–3, §2(d), and §3's shells with the volume bound (3.1). It
does not use Remark 6. This packet's author checked those uses against `PROOF.md`; that is an author-side
interface check, not a review of C89.

**How it bears on Remark 6.** Remark 6 shows, conditionally on merged #198, that Theorem G's constant must grow
at least like `ρ^{1−4N}` as `ρ ↓ 0`. C89 gives an explicit polynomial upper growth `ρ^{−A_N}`. It does not settle
all-order decay at any fixed power cutoff `ρ = ℓ^a`, because order `q` needs `β ≤ 1/A_{2(q+1)}`, which shrinks as
`q` grows. All orders do hold at logarithmic cutoffs.

**Not established by C89** (its §5 and the review): contact or intermediate localization; regional
multiple-witness collision; actual-field confinement; witness uniqueness; control of rejected candidates; and the
two-sided canonical-witness/persistence correspondence.

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
