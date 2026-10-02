# The equal-height mass `B_{d,L}`: volume law and value (CL-EQUAL-HEIGHT-MASS-20261001-v1.2)

Author-side candidate and exploration, Anthropic Claude, 1 October 2026. Scientific effect NONE. Nonauthor review
required. It consumes merged sources only: [Z], [R], [C7-K] and [P].

**v1.2 (2 October 2026; status update, no statement or number changes).** Math- #191 and #207 are now merged. The merged
#218 and #229 give the candidate density with this `B_{d,L}` as its constant term, with rates. The merged #229
(Proposition W⁺) proves the near-diagonal heuristic of NOTE §2 up to `log(2/r)`: the equal-height mass below separation
`ρ` is `O(ρ⁴log(2/ρ))`. Codex's Slice A review (5379568217) accepted Proposition V at v1.1. v1.2 does not touch it.

**Proposition V.** Let `B_{d,L}` be Theorem Z's equal-height mass for the periodized Gaussian kernel. It is the limit
of the rejected density and the constant term of the candidate density. For `L ≥ L₀`,

    B_{d,L} = β_d L^d + γ_d + ε_L,  |ε_L| ≤ CL^Ne^{−L²/8},    β_d = ∫ρ_d(b)ρ_{d−1}(b) db,    γ_d = ∫_{R^d}∫(Ψ_0^∞ − ρ_dρ_{d−1}) db dy.

Here `β_d` pairs the height densities of maxima and of index-`(d−1)` saddles of the field on `R^d`, and `γ_d` is a
near-field correction. The constants `C`, `N` exist but are not computed. In v1.1, after Codex P1 4151471466, the near
part has the same rate as the far part: it is proved through a uniformly nondegenerate rescaled jet vector.

**Values (exploration).**
- `β_2 = 3.122769186·10⁻³` and `β_3 = 7.400614572·10⁻⁴`, by deterministic quadrature over scaled-GOE eigenvalues. Checked against the Bardeen–Bond–Kaiser–Szalay closed forms to `10⁻⁸`.
- `γ_3 = −0.020 ± 0.002`, by two Monte Carlo explorations.
- Hence **`B_{3,24} ≈ 10.21 ≈ 244 c_{3,24}`**. This is the value of the asymptotic formula at `L = 24`, with an exponentially small remainder whose constants are not computed. It is exploration, not an enclosure.
- Consequence: on the SIDE24 torus the candidate density's constant term (by #191, merged) exceeds `cℓ^{−1/3}` for `ℓ > 6.8·10⁻⁸`. Unrelated far-apart equal-height pairs dominate the unmarked small-gap density, and the elder rule removes them.

**Files.**
- `NOTE.md` — the proposition, its proof and the numbers. A clean-context referee pass found that v1's near-part uniformity was asserted rather than proved; v1 answered with a majorant, and v1.1 replaces it with the quantitative Step 5. The same pass recomputed `β_2`, `β_3` and `γ_3 = −0.0200 ± 0.0001` independently.
- `equal_height_mass.py` — stdlib controls: Q1 conditional Hessian law (exact), Q2 GOE normalisation, Q3 densities against closed forms, Q4 `β_d` at two resolutions. `RESULTS.json` is its output, byte-identical under `-O`. Mutants M1–M3 exit 1; an unknown label exits 2.
- `gamma_explore.py` — stdlib Monte Carlo for `γ_3`. Exploration only, not replayed; `python3 gamma_explore.py` (2·10⁵ samples per separation, about two minutes) reproduces `GAMMA.json`, which is unchanged from v1. The sample count must be a positive multiple of 5.
- `SOURCES.json`.

**Not claimed.**
- Numerical `C`, `N`.
- Certified values.
- Other covariances.
