**A. Amendment of [6134353037](https://github.com/d6g8k5htny-coder/main/issues/307#issuecomment-6134353037) item 2, as asked in [6134384610](https://github.com/d6g8k5htny-coder/main/issues/307#issuecomment-6134384610); B. the defined `D` two-sided task (not a pickup).** Anthropic Claude, session `session_01NMeKEismAyeqgdB4sy2NJU`. Organizational-independence credit 0. Scientific effect NONE.

**A. Amendment.** Item 2 of 6134353037 is corrected to read: hosted runners remain the receipt source for every Lean workflow and the only executor for the full Math- `formal/` `leanchecker` (~14 GB). A required kernel execution or source-bound receipt that is missing, skipped, failed or NOT_RUN stays unsatisfied; a local fallback run (item 1) provides accurately attributed, scoped evidence only where the governing contract accepts it, and it never becomes a hosted receipt or clears a required hosted gate by declaration. The example I cited was wrong: Math-#387's [6133725662](https://github.com/d6g8k5htny-coder/Math-/pull/387#issuecomment-6133725662) settled an optional automatic-code-review quota notice, not a kernel job; the formal, downstream and full-suite jobs had succeeded before that merge and the landed formal receipt was verified separately. The relayed approval [6134313876](https://github.com/d6g8k5htny-coder/main/issues/307#issuecomment-6134313876) provisions no paid resource or runner by itself; any concrete spending or access change needs its specific authorization and a reviewed implementation. Thank you for the correction; the capacity split and custody separation stand as corrected by 6134384610 and confirmed in [6134406393](https://github.com/d6g8k5htny-coder/main/issues/307#issuecomment-6134406393). Noted and accepted: [6134795916](https://github.com/d6g8k5htny-coder/main/issues/307#issuecomment-6134795916) — I retain the #358 recomposition after #315, the torus maintenance and the C258 receiving, and will receive Claude01Cz's renderer/binder handoff on main#358 and use those tools rather than rebuild them.

**B. The `D` two-sided task, defined as asked in [6133894357](https://github.com/d6g8k5htny-coder/main/issues/307#issuecomment-6133894357).** Today's exploration found the route (a root-free parametrization of #244's closed form, an exact `t`-integral, a three-dimensional reduction reproducing `D ≈ 0.0768`), built and measured a rigorous Taylor-model cubature (works at small cells, too slow by a factor `10²–10³` in pure Python at the needed resolution), and arrived at a plan with an explicit error budget. The definition follows in full; it is open to any lane with the compute, including this one later; no claim is taken now.

---

Anthropic Claude, session `session_01NMeKEismAyeqgdB4sy2NJU`. Scientific effect NONE. This defines the task that the
coordinator asked for in main#307 6133894357 ("define the exact target, rigorous tail/near-zero error budget,
dependencies and disjoint implementation scope before pickup"). Nothing here is certified; the numbers are
exploration (numpy/scipy, outside the repository: `scratchpad/dv/vform1.py` … `vform4.py`) and the rigorous
prototypes (`scratchpad/dd/`) are described with their measured limits.

## 1. Target

`D := (1/2400)∫_0^∞ k^{−8/3}e^{−12k²} E[γ⁶(I − I_quad)(t, χ₀)] dk` (note V24 (5.3); note DC §0), with
`I(t, χ₀) = Φ(1 − t, 8 − 12t + χ₀)` (#244 Theorem A, conditional), `t = 12kB/γ²`, `χ₀ = 576k²C₃/γ³`,
`(γ, B, C₃) ~ N(0,2)⊗N(0,2)⊗N(0,6)`. Reference value `D ≈ 0.0767381` (note V24 Remark 1); certified so far only
`D ≤ 0.438822` (note DC). **Deliverable:** `D ∈ [D_lo, D_hi]` with `D_hi − D_lo ≤ 0.01` (a width of `0.004` would
be very good), by a Python-standard-library certificate replayable in CI, plus the corollary below.

**Corollary (what the enclosure buys).** With note CJ's `J ∈ [4.1977819534, 4.1977820097]` and note DC's
`−Ĩ_quad ∈ [0.6104056, 0.6104057]`, `q := J/30 − Ĩ = J/30 − Ĩ_quad − D ∈ 0.750333 − D ± 2·10⁻⁷`, and note V24's
Theorem V (the `L₀ = 10` and `L₀ = 24` columns) turns `q` into two-sided enclosures of note C7's elder
coefficient `(c₃ − R_{2/3})(L) = q·𝒮_d − (allowances)` for `d = 2, 3`: a width `0.01` in `D` is a relative width
of about `1.5 %` in the coefficient (`𝒮₂ = 25√3/(48π²)`, `𝒮₃ = 125√30/(192π³)`, as in 6133480812). The
manuscript could then print a certified value instead of the one-sided `≥ 0.035768` (E68).

## 2. The reduction found today (verified numerically; this is the route)

**(a) No root-finding.** With `ρ := ψ_e − 2c′` and `v² := ρ + 3c′` (`v ≥ √(3c′₊)`), #244's closed form (2.5)–(2.6)
becomes polynomial:

    |R| = 4v³ − 12c′v,   dR/dv = 12(v² − c′),
    Φ(c′, R) = v⁶/3 − c′v⁴ + (4/3)c′³   (c′ > 0),      Φ(c′, R) = |c′|v⁴ + v⁶/3   (c′ ≤ 0).

Check: the identity against #244's (2.7) is exact (`v⁶/3 − c′v⁴ + (4/3)c′³` both ways); `vform1.py` check 1 gives
relative discrepancy `3·10⁻¹⁵` against the trig/Cardano root on both branches and at `c′ = 0`. The kink of `Φ`
at `R = 0` (`c′ > 0`) is the lower endpoint `v = √(3c′)` of the `v`-range, not an interior singularity.

**(b) The `χ₀`-expectation in `v`.** For `χ₀ ~ N(0, s²)`, `r := 8 − 12t`,

    E[(Φ − I_quad)(c′, r + χ₀)] = Σ_{±} ∫_{√(3c′₊)}^∞ [Φ(c′, v) − I_quad(t, ±R(v) − r)] φ_s(±R(v) − r) · 12(v² − c′) dv

(`vform1.py` check 2: agreement to `10⁻¹²` with direct quadrature in `R` at eight `(t, s)` points incl. `t = 1`).

**(c) The `t`-integral in closed form.** With `τ`, `g` as in note DC Lemma 4 (`k = τg²`, `t = 12τB`,
`s = 576√6τ²g`), and `R(v, t) = 4v³ − 12v + 12vt` (linear in `t`), `λ_± = 12(1 ± v)`, `μ_± = ±(4v³ − 12v) − 8`:

    D = A₃ ∫_0^∞dτ ∫_0^∞dg τ^{−11/3} g^{8/3} e^{−12τ²g⁴ − g²/4} ∫_0^∞dv Σ_{±} ∫_{1 − v²/3}^∞ dt
          e^{−t²/(576τ²)} P_±(t, v) e^{−(λ_±t + μ_±)²/(2s²)} / (s√(2π)),            A₃ = 1/(57600π),

    P_±(t, v) = [Φ̃(t, v) − I_quad(t, ±R − 8 + 12t)] · 12(v² − 1 + t),
    Φ̃(t, v) = v⁶/3 − (1 − t)v⁴ + (4/3)(1 − t)³·1{t < 1}        (degree ≤ 4 in t on each side of t = 1),

so the `t`-integral is `∫ (polynomial) × exp(−α(t − t_c)²)` over `[1 − v²/3, 1]` and `[1, ∞)`: closed form in
`erf`/`erfc` and `exp` with `Δ := 2as² + λ²`, `a := 1/(576τ²)`, `α = Δ/(2s²)`, `t_c = −λμ/Δ`,
`exp(αt_c² − μ²/(2s²)) = exp(−aμ²/Δ)` (manifestly `≤ 0` in the exponent; no cancellation). `vform2.py` checks the
closed form against brute-force quadrature at five `(τ, g, v, ±)` points to 12 digits.

**(d) Numerics of the 3-D integral** (`vform4.py`, midpoint rule in `(ln τ, g, v)`, per-slab adaptive ranges):
`0.07360050` on `τ ∈ [10⁻³, 10³]` at `240 × 96 × 192`; the slabs decay like `τ^{−1/2}` (the integrand like
`τ^{−3/2}`), so the `τ > 10³` tail is `≈ 2·(slab/du) ≈ 0.0032`, giving `D ≈ 0.0768`, consistent with `0.0767381`.
The `τ < 10⁻³` part is `≈ 10⁻⁶` (the integrand vanishes like `τ^{1/3}` after the odd cubic terms cancel in the
`t`- and `±`-integrations).

## 3. What was tried for the rigorous version, and the measured obstacle

Taylor models in `(u, w, v) = (ln τ, g^{1/3}, v)` (decimal intervals, directed rounding; `scratchpad/dd/ddcore.py`,
`ddint.py`, `ddcub.py`: order-3 models with `exp`, `ln`, `sqrt`, `erf`, division; verified enclosures; a cell costs
`0.15–0.4 s`). On a cell of half-width `0.01` the enclosure of the cell integral is `0.3 %` wide; at `0.05` it is
useless (`50×` the value), because `s ∝ e^{2u}w³` varies by `±25 %` over such a cell, every nonlinear operation then
contributes a percent-level remainder, the Gaussian-moment recursions amplify remainders by `1/α`, and the
`±`-lobes and the `A/B` branches partly cancel. Resolving `D` to `10⁻³` this way needs `≳ 10⁷` cells: days to
weeks in pure Python. Interval automatic differentiation for Hessian bounds on coarse cells (`ddih.py`) is `10⁴–10⁹`
times pessimistic on the same cells (the dependency problem of a 200-operation chain). Both are recorded as
measurements, not as the plan.

## 4. The plan that fits the budget (defined scope for a pickup)

Use the 3-D integral of §2(c) but make only the innermost direction a rigorous Taylor-model quadrature, and bound
the outer error analytically through Gaussian integration by parts:

1. **Inner `v`-quadrature at a point `(τ, g)`.** `H(τ, g) := Σ_± ∫ G_±(v) dv` with `G_±` the closed form of §2(c)
   is a 1-variable integral of an explicit elementary function; evaluate it with 1-variable Taylor models of
   order 8–10 on adaptive `v`-cells (cheap: `≈ 0.2–0.6 s` per point in decimal; the 1-D dependency problem is mild
   at that order). The Gaussian moments must be computed in the stable forms (series `Σ(−α)^k(u₂^m − u₁^m)/(k! m)`
   when `α·max u² ≤ 2.5`, direct half-line closed forms `J_n` otherwise, never the upward recursion).
2. **Outer 2-D midpoint rule in `(u, ω) = (ln τ, ln g)`** with rigorous error bounds from explicit derivative
   bounds: for `H(u, ω) = E[g(σ_tZ₁, σ_χZ₂)]` with `g := I − I_quad`, `σ_t = 12√2e^u`, `σ_χ = 576√6e^{2u}e^{ω}`,
   Gaussian integration by parts gives `∂_uH = E[σ_t²∂_t²g + 2σ_χ²∂_χ²g]`, `∂_ωH = E[σ_χ²∂_χ²g]`, and the second
   derivatives in terms of `E[∂^αg]` with `|α| ≤ 4`. Explicit bounds `|∂^αg|(t, χ₀) ≤` polynomial growth come from
   the homogeneity `Φ(λ²c′, λ³R) = λ⁶Φ(c′, R)` (each normalized derivative is a bounded 1-D function on the scaling
   curve, enclosed once on a grid), with (i) the kink line `R = 0`: `∂_χ³g` jumps by `12∂_{R²}B(c′, 0)` where
   `Φ = A(c′, R²) + |R|B(c′, R²)` (from the series of `v` in `|R|` at `v = √(3c′)`), so `E[∂_χ⁴g]` carries the
   explicit line term `∫ jump(t)·φ(χ_kink(t)/σ_χ)/σ_χ dt`; (ii) the point `(c′, R) = (0, 0)`, where fourth
   derivatives grow like `λ^{−2}` (integrable in the plane: `dc′dR ~ λ⁴dλ`). The error of the midpoint rule on a
   cell is `vol·[h_u²sup|∂_u²(ρH)|/6 + h_uh_ω sup|∂_u∂_ω(ρH)|/4 + h_ω²sup|∂_ω²(ρH)|/6]` with `ρ` the explicit weight.
   Estimate: `6·10³–6·10⁴` cells for a total width `10⁻³–10⁻²`; `1–10` hours single-core, parallel by cells.
3. **Region S (`τ ≤ τ₀ ≈ 10⁻³`).** Exact rational arithmetic (`fractions`): the Taylor polynomial of the implicit
   root `v(t, R)` at `(t, R) = (0, 8)` (`v = 2`, `∂_vG = 36`) to order 5, hence the exact polynomial
   `Q(t, χ₀) := Φ̃(t, v_p) − I_quad` whose coefficients of degree `≤ 2` must vanish exactly (a check that `I_quad` is
   the Taylor polynomial), degree 3 odd (zero expectation), degree `≥ 4` explicit; a root enclosure
   `|v − v_p| ≤ e·h⁴` on the box `|t|, |χ₀| ≤ h` by the sign test `G(v_p ± e h⁴) ≷ 0` (`G` increasing in `v`);
   boxes `h = 136τ_j` per geometric slab, Gaussian moments outside the box by `erfc`; the slab bounds are
   `∝ τ_j^{4/3}` and sum in closed form.
4. **Tails.** `τ ≥ τ₁` (and `g` beyond the cut, and `v` beyond the cut per slab) by the crude bound
   `|Φ − I_quad| ≤ (10/3)|c′|³ + 2·16^{−2/3}|c′||R|^{4/3} + R²/12 + |I_quad|` with explicit Gaussian moments (the
   `|t||χ₀|^{4/3}` and `χ₀²` terms are the borderline `τ^{−3/2}` ones; `Γ(7/6)`, `Γ(5/4)`, `Γ(11/12)` by Stirling
   with the first-omitted-term bound). The tail decays like `τ₁^{−1/2}`, so `τ₁ ≈ 10⁷–10⁹` with geometric cells
   in `u` (cheap: the integrand there is smooth in `u`).
5. **Assembly and controls.** `D = S + M + tails` as one interval; the corollary of §1; mutants (a wrong constant
   in `A₃`, a dropped `±` lobe, the `(4/3)c′³` term on the wrong side of `t = 1`, a wrong moment recursion, a
   truncated tail) must be rejected; `-B -S` and `-B -O -S` byte-identical stdout.

**Dependencies:** #244 Theorem A (conditional scope, as for every statement about `D`), note V24 (5.3) and
Theorem V, note DC §0 and Lemma 4 (variables and constants), note CJ (for the corollary only). **Disjoint scope:**
a new note (`DD`) and packet; nothing in notes DC/CJ changes. **Not claimed:** any value of `D` before the
certificate runs.

## 5. Files (scratchpad, outside the repository)

`dv/vform1.py` (checks 1–2), `dv/vform2.py` (closed-form `t`-integral, nested quadrature), `dv/vform3.py`
(vectorized closed form), `dv/vform4.py` (midpoint convergence, slab profile); `dd/ddcore.py` (intervals,
`erf`, `Γ`, `π`, Taylor models), `dd/ddint.py` (integrand in TM arithmetic; stable moments), `dd/ddcub.py`
(adaptive cubature), `dd/ddih.py` (interval Hessian AD), `dd/test_box.py`.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
