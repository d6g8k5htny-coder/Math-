# The cusp crossover and the second-order term of the elder lifetime law (CL-CUSP-SECOND-ORDER-20261001-v1)

Author-side proof candidate, Anthropic Claude, 1 October 2026. Scientific effect NONE. Nonauthor review required.
**Depends on Math- #191** (Lemma E, (E.1), §2; v1.1 blob `441152df`) **and Math- #198** (§1, Lemma B (B.2), Lemma F′,
§3 (3.1)–(3.2), Lemma W; v1.1 blob `abfb98ae`), both unmerged author-side candidates of this session: this packet cannot
be integrated before them and must be rebound if either changes. Everything else consumed is merged: [R], [C7-K], the
reconciled [P] chain directly; [182] and [Z] transitively, through #191 and #198.

**Statement (Theorem CU).** For the periodized Gaussian field on the fixed torus (every `d ≥ 2`, `L > 0`) and the
canonical marked Kac–Rice version of the elder lifetime density,

    ν_eld(ℓ) = c ℓ^{−1/3} + c₁ ℓ^{1/4} + o(ℓ^{1/4}),
    c₁ = −(192/7)·2^{1/4} ∫_{S^{d−1}}∫_R π₀(u; v₀(b,0)) E₀[|Y|^{7/4}|Δ|^{1/4}1{A < 0} | b] db dσ(u) < 0,

`Y = (f₄/12)Δ − γᵀadj(A)γ/4`, `Δ = det A`, built from the jets `f₄ = ∂_u⁴f(0)`, `γ = ∇_Θ∂_u²f(0)`, `A = D_Θ²f(0)` under the
zero-gap contact law. #198 had the order `O(ℓ^{1/4})`; this packet identifies the term and its sign. For the manuscript's
field (`d = 3`, `L = 24`) the exploration gives `c₁ ≈ −0.21185`, `c₁/c ≈ −5.071`:
`ν_{3,24}(ℓ) = c_{3,24}ℓ^{−1/3}(1 − 5.071ℓ^{7/12} + o(ℓ^{7/12}))`, a 1% correction at `ℓ ≈ 2.3·10⁻⁵`.

**Mechanism — the cusp crossover.** At the scale `r ≍ k` (gap `ℓ = kr³` comparable to `r⁴`; `κ := k/r = ℓ/r⁴`), rescaled by
`x = rX` (axis), `y = r²Ξ` (transverse), heights `r⁴`, the pinned field converges to a universal random polynomial
`𝔓 = 2κ(X + ½)²(X − 1) + (f₄/24)(X² − ¼)² + ½(X² − ¼)γ·Ξ + ½ΞᵀAΞ` (Theorem CU.1). Maximizing over the concave transverse
fibers reduces its superlevel topology exactly to the quartic ridge `g(X) = κ[2(X + ½)²(X − 1) + 3φ(X² − ¼)²]`,
`φ = Y/(6κΔ)` (Theorem CU.2). The pair is typed iff `|φ| < 1` (the sign window of #198 Lemma W) and **`S` is `M`'s elder
partner iff `|φ| < 1/3`**: the critical values factor as `g(X₃) + κ = κ(φ + 1)³(3φ − 1)/(16φ³)` and
`g(X₃) = κ(φ − 1)³(3φ + 1)/(16φ³)`, and at `φ = ±1/3` the two competing saddles (resp. maxima) have equal heights. The
decision is stable under `C²`-small perturbations in a fixed window, by compact-window path-and-trap arguments only
(Proposition CU.3), so the typed and elder kernels converge at fixed `κ` (Theorem CU.4); a window-probability bound
(Lemma CU.5: `E[W_r/r²] ≤ C(k² + r⁴)(min(1, k/r)^{1/2} + r^β)P^N`) controls the intermediate separations; and the cusp
integral `∫₀^∞ loss ds = (16/7)2^{1/4}|Y|^{7/4}|Δ|^{1/4}` gives `c₁`. The scale `r ≍ k` interpolates between the cap
regime (`κ → ∞`: rejected fraction `≍ (r/k)³`, the `Θ(r³)` of [P] Theorem A) and the small-`κ` end, where the typed
weight is `O(κ)` of the contact weight and the elder share of it tends to `13/27` (Remark 1; Theorem Z's
all-rejected statement is the different, non-commuting limit `k → 0` at fixed `r`).

**Not claimed:** a rate for the `o(ℓ^{1/4})`; certified numerical values (the numbers are exploration); the candidate
and rejected expansions (formal, Remark 2); uniformity in `d, L`.

**Files.** `PROOF.md`. `cusp_check.py` (stdlib exact controls; `RESULTS.json` its output, byte-identical under `-O`;
mutants M1–M4 exit 1, an unknown label exits 2): C1 the quartic-ridge identities and boundary factorizations; C2 the
elder window by exact 1D maximin for 117 rational `φ`; C3 the fiber reduction; C4 the cusp limit field for pinned
polynomials of degree 6 in `d = 2, 3`; C5 the model's endpoint determinants and typed window; C6 the cusp integrals;
C7 the Gaussian-kernel conditional covariances used by the exploration. `explore_cusp.py` (stdlib, floating point,
**not a control**, not replayed by the workflow, about a minute; `EXPLORE.json` its output): X1 the actual global elder
rule of random pinned plane quintics at `r = 0.01` agrees with `|φ| < 1/3` in 32/32 typed cases, and in targeted cases at
`r = 0.003` the boundary lies between `|φ| = 0.32` and `0.345`; X2 `c₁` for the Gaussian kernel — `d = 2`: `−0.26939883`,
`c₁/c = −3.669938` (Gauss–Legendre quadrature, two resolutions agree to ten digits); `d = 3`: `−0.21184835`,
`c₁/c = −5.071062` (deterministic quadrature over the negative-definite cone, two resolutions agree to `10⁻⁸`
relative; a fixed-seed Monte Carlo over the same law gives `−0.21163 ± 0.00014`). `SOURCES.json` (exact identities;
#191/#198 recorded as consumed-unmerged and verified by the workflow by blob).

**Pre-submission referee record (same author family; not acceptance).** Two clean-context Claude referee passes read
v1 before this PR. Slices A/B confirmed CU.1–CU.2 symbolically and by an independent two-dimensional maximin of the
full model (34 cases) and found closeable gaps in Proposition CU.3 (all real zeros of `g'` in Step 5, the margin
`−2κ − 1` in Step 3, `X_R := min(2, X₃ − τ)`); slices C/D found closeable gaps in Lemma CU.5 (`E₁` must control `T`; the
`J'`-measurable window event; the Carbery–Wright uniformity) and a false remark (the small-`κ` elder share is `13/27`,
not `0`), and independently reproduced `c₁` (`d = 2` quadrature; `d = 3` Monte Carlo `−0.211848 ± 0.000024`). Every
finding is applied in this version.

**What the controls do not test.** Theorem CU.1 for non-polynomial fields, Proposition CU.3, Theorem CU.4,
Lemma CU.5 and the assembly (§6) are proved in prose only. Review slices (PROOF.md §10): A the cusp field and the
model; B stability; C the kernel limits and the window probability; D the assembly and the remarks.
