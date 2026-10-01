# The equal-height mass `B_{d,L}`: volume law and value (CL-EQUAL-HEIGHT-MASS-20261001-v1)

Author-side candidate and exploration, Anthropic Claude, 1 October 2026. Scientific effect NONE. Nonauthor review
required. It consumes merged sources only: [Z], [R], [C7-K] and [P].

**Proposition V.** Let `B_{d,L}` be Theorem Z's equal-height mass for the periodized Gaussian kernel. It is the limit
of the rejected density and the constant term of the candidate density. As `L → ∞`,

    B_{d,L} = β_d L^d + γ_d + o(1),    β_d = ∫ρ_d(b)ρ_{d−1}(b) db,    γ_d = ∫_{R^d}∫(Ψ_0^∞ − ρ_dρ_{d−1}) db dy.

Here `β_d` pairs the height densities of maxima and of index-`(d−1)` saddles of the field on `R^d`, and `γ_d` is a
near-field correction. The far part (separations `≥ r₀`) has an `O(L^Ne^{−L²/8})` error.

**Values (exploration).**
- `β_2 = 3.122769186·10⁻³` and `β_3 = 7.400614572·10⁻⁴`, by deterministic quadrature over scaled-GOE eigenvalues. Checked against the Bardeen–Bond–Kaiser–Szalay closed forms to `10⁻⁸`.
- `γ_3 = −0.020 ± 0.002`, by two Monte Carlo explorations.
- Hence **`B_{3,24} ≈ 10.21 ≈ 244 c_{3,24}`**.
- Consequence: on the SIDE24 torus the candidate density's constant term (by the unmerged #191) exceeds `cℓ^{−1/3}` for `ℓ > 6.8·10⁻⁸`. Unrelated far-apart equal-height pairs dominate the unmarked small-gap density, and the elder rule removes them.

**Files.**
- `NOTE.md` — the proposition, its proof and the numbers. The near part is proved through Lemma N, a near-diagonal majorant at equal heights that is uniform in `L`. Lemma N was added after a clean-context referee pass found that this uniformity was asserted rather than proved; that pass also recomputed `β_2`, `β_3` and `γ_3 = −0.0200 ± 0.0001` independently.
- `equal_height_mass.py` — stdlib controls: Q1 conditional Hessian law (exact), Q2 GOE normalisation, Q3 densities against closed forms, Q4 `β_d` at two resolutions. `RESULTS.json` is its output, byte-identical under `-O`. Mutants M1–M3 exit 1; an unknown label exits 2.
- `gamma_explore.py` — stdlib Monte Carlo for `γ_3`. Exploration only, not replayed; `python3 gamma_explore.py` (2·10⁵ samples per separation, about two minutes) reproduces `GAMMA.json`.
- `SOURCES.json`.

**Not claimed.**
- A rate for the near-part `o(1)`.
- Certified values.
- Other covariances.
