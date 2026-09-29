# The unrestricted selection difference does not vanish: disposition of candidate C7

Object: CL-D1-UNRESTRICTED-DIFFERENCE-20260929-v3.
Author: Anthropic Claude (Claude Code session `session_017Mi3hxjaxV45x6zo6o1ee3`).
Disposition: AUTHOR-SIDE CANDIDATE; nonauthor analytic review required.
Scientific effect: NONE. No `STATUS`, `PROOF_INDEX`, `GRAPH`, claim, lemma flag, prize or source body changes.

## 1. The candidate and the result

The D1 parent `imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md` (blob `dfed3b8d…`, see
SOURCE_FILES.json; reconciled in Math-#126) proves two things:
- in Theorem B, the compact-window difference `0 ≤ ν_cand(ℓ) − ν_eld(ℓ) ≤ C_{B,K} ℓ^{2/3}` (1.2);
- in Theorem C, the unrestricted leading asymptotics `ν_cand^all(ℓ) ~ ν_eld^all(ℓ) ~ c_{d,L} ℓ^{−1/3}` (1.3).

It states explicitly that (1.2) is not asserted for the unrestricted densities (lines 52, 384, 433). Candidate C7 of
`reviews/candidates_pending_20260928/CANDIDATES.md` proposes the unrestricted rate

    0 ≤ ν_cand^all(ℓ) − ν_eld^all(ℓ) ≤ C ℓ^{2/3}.                                   (C7)

Here `ν_cand^all` counts all ordered local-maximum / index-`(d−1)`-saddle pairs with height difference `ℓ`, and
`ν_eld^all` counts all finite superlevel `H_0` bars. Both are expected densities per unit volume on the fixed torus
`X = ℝ^d/(Lℤ^d)`, `d ≥ 2`, for the parent's periodized Gaussian field.

**Theorem U.** Fix `0 < r_0 < L/4` as in parent §13 and put `ρ = r_0/2`. There are `c_* > 0` and `ℓ_0 > 0` such
that for `0 < ℓ ≤ ℓ_0`

    ν_cand^all(ℓ) − ν_eld^all(ℓ)  ≥  ν_cand^far(ℓ) − ν_eld^far(ℓ)  ≥  c_*,          (U1)

where "far" means torus distance `≥ r_0` between the two points, as in parent §14. Consequently:
- **(U2)** (C7) is false. `D(ℓ) := ν_cand^all(ℓ) − ν_eld^all(ℓ)` satisfies `D(ℓ)/ℓ^α → ∞` for every `α > 0`.
  Combined with parent (14.1) and Theorem C, `c_* ≤ D(ℓ) = o(ℓ^{−1/3})`.
- **(U3)** The expected per-unit-volume number of candidate pairs with lifetime in `(0, t]` that are not bars is at
  least `c_* min(t, ℓ_0)` for every `t > 0`, and so at least `c_* t` for `0 < t ≤ ℓ_0 = 1`. In the compact window, parent (12.1) gives at most `C t^{5/3}`.
- **(U4)** For `q ≤ −1`, the nonselected sum `E Σ_{candidate, not bar, ℓ ≤ t} ℓ^q` is infinite for every `t > 0`. In
  the compact window, parent (12.3) makes it finite for every `q > −5/3`.

The obstruction comes from pairs at macroscopic separation. Among pairs at distance `≥ r_0` with small height
difference, a positive density are separated by a level curve and so cannot be persistence partners. Theorem U does
not decide whether `D` is bounded (§5).

## 2. Kac–Rice form of the far difference

Parent §14 writes the far candidate density from the original full-pin covariance, which is uniformly nondegenerate
on `{dist(x,y) ≥ r_0}`:

    ν_cand^far(ℓ) = L^{−d} ∫∫_{dist(x,y) ≥ r_0} ∫_ℝ p_{x,y}(b, b−ℓ)
                      E[F_d(H_x) F_{d−1}(H_y) | 𝒫_{x,y}(b, ℓ)] db dx dy,           (2.1)

Here:
- `𝒫_{x,y}(b, ℓ)` is the pin event `{∇f(x) = ∇f(y) = 0, f(x) = b, f(y) = b − ℓ}`;
- `p_{x,y}` is the joint density of `(∇f(x), ∇f(y), f(x), f(y))` at `(0, 0, b, b−ℓ)`;
- `F_j` is the absolute determinant restricted to index `j`;
- the height map `(f(x), f(y)) ↦ (b, b−ℓ)` has Jacobian one.

The mark below is the indicator of an open set of `(x, y, f)`, hence lower semicontinuous. The same
arXiv:2304.07424v3 Theorem 7.1 interface used in parent §9 and in [RC] (3.1) therefore gives, for the count of far
pairs carrying the mark,

    N_O(ℓ) = L^{−d} ∫∫_{dist ≥ r_0} ∫ p_{x,y}(b, b−ℓ)
               E[F_d(H_x) F_{d−1}(H_y) 1_{O_{x,y,ℓ}}(f) | 𝒫_{x,y}(b, ℓ)] db dx dy,    (2.2)

    O_{x,y,ℓ} = { f :  sup_{∂B(x,ρ)} f < f(y) }.

## 3. A separating level curve forbids pairing

**Lemma 1.** Let `f` be a Morse function with distinct critical values (the almost-sure generic locus of parent §8).
Let `x` be a local maximum and `y` an index-`(d−1)` saddle with `dist(x, y) ≥ r_0`, and suppose `f ∈ O_{x,y,ℓ}`, that
is, `sup_{∂B(x,ρ)} f < s := f(y)`. Then `(x, y)` is not a finite `H_0` persistence pair of the superlevel
filtration.

*Proof.* We work at the closed critical superlevel `{f ≥ s}`, not above `s`.

We use one incidence fact on the generic locus. If a finite `H_0` bar is born at `x` and killed at `y`, then `y` lies
in the closure of the component `C` of `{f > s}` that contains `x`. The reason is the local picture at a Morse saddle
of index `d−1` at level `s`. Near `y`, `{f > s}` consists of two local cones. The merge at `y` joins the two global
components of `{f > s}` that contain them, and the bar killed at `y` is the younger of those two components, which is
`C`. Since `cl(C) ⊂ {f ≥ s}` is connected, `x` and `y` lie in one connected component `K` of `{f ≥ s}`.

Now `f < s` on `∂B(x, ρ)`, so `K` does not meet `∂B(x, ρ)`. Since `ρ < r_0 < L/4`, the ball is embedded and its
boundary separates it from its complement. As `K` is connected and contains `x`, `K ⊂ B(x, ρ)`. But
`dist(x, y) ≥ r_0 > ρ`, so `y ∉ B(x, ρ)`, a contradiction. ∎

The height difference `ℓ = f(x) − f(y)` is positive for every actual pair. The value `ℓ = 0` enters below only as an
endpoint of the compact parameter set in Lemmas 2–3, never as a paired event.

Hence the far candidate pairs carrying the mark in (2.2) are not bars, and

    ν_cand^far(ℓ) − ν_eld^far(ℓ) ≥ N_O(ℓ).                                         (3.1)

## 4. The marked intensity is bounded below

**Lemma 2 (support).** For all `x, y` with `dist(x, y) ≥ r_0`, all real `b` and all `ℓ ∈ [0, 1]`, the conditional
law `Q_{x,y,b,ℓ}` of `f` given `𝒫_{x,y}(b, ℓ)` gives positive probability to the open set

    𝒪 = { f ∈ C²(X) : H_x < 0,  H_y nonsingular of index d−1,  sup_{∂B(x,ρ)} f < f(y) }.

*Proof.* `Q = Q_{x,y,b,ℓ}` is a Gaussian measure on the separable Banach space `C²(X)`. Its mean `m` is smooth and
satisfies the pins. By the Gaussian support theorem, its support is `m + cl_{C²}(H_0)`, where `H_0` is the
Cameron–Martin space of the unconditioned field restricted to `h(x) = h(y) = 0`, `∇h(x) = ∇h(y) = 0`.

Every Fourier weight is positive (parent §2), so `H_0` contains every trigonometric polynomial satisfying those
`2(d+1)` linear conditions. Their `C²`-closure is `V_0 = {φ ∈ C² : φ, ∇φ vanish at x and y}`. To see this, take
`φ ∈ V_0` smooth (a general `φ ∈ V_0` is first smoothed in `C²` and then corrected by the same finite constraints;
only the smooth `G − m` below is needed) and trigonometric polynomials `τ_n → φ` in `C²`. The `2(d+1)` point functionals are linearly
independent on trigonometric polynomials (parent §2, distinct-site jets), so there are trigonometric polynomials `ψ_i`
dual to them. Then `τ_n − Σ_i λ_i(τ_n) ψ_i` lies in `H_0` and converges to `φ`, because `λ_i(τ_n) → λ_i(φ) = 0`.

Choose a smooth `G` with:
- `G ≡ b − ℓ − 1` outside the two disjoint balls `B(x, ρ/2)` and `B(y, ρ/2)`, whose closures are disjoint since
  `dist(x, y) ≥ 2ρ`;
- `G(x) = b`, `∇G(x) = 0`, `D²G(x) = −I`;
- `G(y) = b − ℓ`, `∇G(y) = 0`, `D²G(y) = diag(−1, …, −1, +1)`.

Bump functions give such a `G`. Then `G − m ∈ V_0`, since both satisfy the pins. Also `G ∈ 𝒪`, since
`sup_{∂B(x,ρ)} G = b − ℓ − 1 < G(y)`. So `G` lies in the support, and `𝒪`, which is open in `C²`, has positive
`Q`-probability. ∎

**Lemma 3 (uniformity).** Put `Φ(x, y, b, ℓ) = E_Q[F_d(H_x) F_{d−1}(H_y) 1_𝒪]`. It is lower semicontinuous and
strictly positive on `K = {dist(x, y) ≥ r_0} × [0, 1] × [0, 1]`, so `Φ ≥ φ_* > 0` on `K`.

*Proof.* Realize every `Q_{x,y,b,ℓ}` on one unconditioned field `F` by regression on the `2(d+1)` observations. The
observation covariance is uniformly nondegenerate on `K` (parent §14), so the regression coefficients and targets are
continuous and the conditioned fields converge pathwise in `C²` along any convergent parameter sequence. The weight
`F_d F_{d−1}` is continuous, and `1_𝒪` is lower semicontinuous because `𝒪` is open and `(x, y) ↦ 𝒪` varies
continuously. Fatou's lemma gives lower semicontinuity of `Φ`. It is positive: on `𝒪` the weight is positive, and by
Lemma 2 `𝒪` has positive probability. A positive lower semicontinuous function on a compact set is bounded below by
a positive constant. ∎

**Proof of Theorem U.** On `K` the density `p_{x,y}(b, b−ℓ)` is continuous and positive, hence `≥ p_* > 0`. By
(2.2), restricting `b` to `[0, 1]`,

    N_O(ℓ) ≥ L^{−d} p_* φ_* |{(x, y): dist(x, y) ≥ r_0}| =: c_* > 0,   0 < ℓ ≤ 1.

With (3.1) this proves (U1), with `ℓ_0 = 1`, and (U2).

*Density convention.* As in the parent, (U1) is a statement about compatible density versions. The marked
Kac–Rice identity (parent §9, a finite-measure identity for Borel marks) dominates the nonselected expected measure
on `ℓ ∈ (0, 1]` from below by the measure with density `N_O(ℓ)`. So the nonselected density is at least `N_O(ℓ)` for
almost every `ℓ`, and the versions in (U1) are chosen compatibly. The generic-locus assertion of Lemma 1 is used
only almost surely inside that identity, never pointwise at an exceptional conditioning value. The support
argument at `ℓ = 0` needs no genericity and is only a compactness endpoint.

For (U3), integrate (U1) over `(0, min(t, ℓ_0)]`. For (U4), the nonselected measure has density at least `c_*` on `(0, ℓ_0]`,
and `∫_0 ℓ^q dℓ = ∞` for `q ≤ −1`. The bound `D = o(ℓ^{−1/3})` is Theorem C, since both densities are
`c_{d,L} ℓ^{−1/3}(1 + o(1))`. ∎

`witness_check.py` gives an explicit exact instance of the separating configuration, a trigonometric polynomial on
`(ℝ/2πℤ)²`:

    g(u, v) = α cos u + cos² u + cos v,   α = ℓ/2 − 1.

It has a maximum at `(0, 0)` and an index-1 saddle at `(π, π)` with height difference exactly `ℓ`. On the boundary of
the square `|u|, |v| ≤ a` with `cos a = −α/2` (rational), `g < g(π, π)`. The script checks this for three values of
`ℓ` in exact rational arithmetic. It illustrates Lemma 2; it is not a substitute for it.

## 5. What is and is not settled

- **Settled.** (C7) fails. The unrestricted difference is bounded below by a positive constant, and it is
  `o(ℓ^{−1/3})`.
- **Not settled: the order of `D`.** Near pairs at distance `δ ≤ r_0` contribute
  `∫_0^{r_0} δ^{−2} ∫ A_δ(b, ℓδ^{−3}, u)(1 − p_δ(b, ℓδ^{−3}, u)) db dσ dδ`. This is parent (11.2) after the
  substitution `k = ℓδ^{−3}`. Macroscopic `δ` gives another `Θ(1)` term. Whether `D` stays bounded depends on the
  nonselection probability `1 − p_δ` in the degenerate regime of gap mark `k = ℓδ^{−3} → 0`, which no source
  controls. A heuristic balance puts the crossover near `δ ≍ ℓ^{1/4}`. It is not a claim.
- **The compact-window rate (1.2) is untouched.** Restricting marks to compact `B × K` with `inf K > 0` and distances
  to `≤ r_*` removes the obstruction, because such pairs have `r = (ℓ/k)^{1/3} → 0`. The natural corrected target is
  the rate with unbounded birth mark and gap marks bounded away from zero. It needs the parent's selection estimate
  with mark-dependent constants and is left open.
- No numerical `c_*`, no event-probability statement, and no status change.

## 6. Dependencies

- Parent §2 (positive Fourier weights, distinct-site jet rank), §9 (weighted Kac–Rice interface), §13 (`r_0`) and
  §14 (far covariance, height Jacobian one, (14.1)).
- Theorem C (1.3), as reconciled in Math-#126 (`8224783`).
- The Gaussian support theorem and the lower-semicontinuous-mark Kac–Rice formula (arXiv:2304.07424v3, Theorem 7.1),
  the same interface as parent §9 and [RC] (3.1).

Nothing from the elder-selection upper estimate of Theorem A is used.

## Revisions

- **v3.** Qualifications requested in
  [5890428429](https://github.com/d6g8k5htny-coder/Math-/pull/133#issuecomment-5890428429): (U3) holds as
  `c_* min(t, ℓ_0)`; an explicit density-version convention (expected-measure domination, a.e. densities); a note
  on the full `V_0` closure. No change to Theorem U or the witness.
- **v2.** Lemma 1 is repaired as requested in
  [5890369316](https://github.com/d6g8k5htny-coder/Math-/pull/133#issuecomment-5890369316). The v1 proof asserted that
  `y` lies in the closure of `x`'s component of `{f > t}` for `t > f(y)`. That is false, because such a closure lies
  in `{f ≥ t}` and `f(y) < t`. v2 argues at the closed critical superlevel `{f ≥ f(y)}`, using the generic-locus merge
  incidence stated explicitly, and treats `ℓ = 0` only as a compactness endpoint. Theorem U, Lemmas 2–3, the witness
  and the corollaries are unchanged.
