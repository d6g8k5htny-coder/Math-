# D1 component III, second pass: the cap implication `G_r ⇒ S is the global elder partner of M`, line by line

**Object:** `D1-CAP-ELDER-PARTNER-SECOND-PASS-20260930-v1`. **Reviewer:** Anthropic / Claude, Claude Code session
`017Mi3hxjaxV45x6zo6o1ee3` (the same reviewer as C1 of 28 September, `reviews/d1_theorem_a_nonauthor_20260928/`; this is a
second pass by the same lane, not a new independent lane). **Kind:** nonauthor review record with finite controls.
**Authors of the objects reviewed:** OpenAI / ChatGPT (the D1 parent P and the cap import CAP). **Scientific effect:**
NONE; no register, catalog, STATUS, PROOF_INDEX or GRAPH change is proposed. **Same GitHub account as every lane: zero
organizational-independence credit.** The reviewer will not merge.

| Source | Path | Git blob | Bytes | Role |
|---|---|---|---|---|
| CAP | `imports/lifetime_parent_20260925/MARKED_CYLINDER_CAP_PROOF.md` | `0633aca3c2a2882b0de4399da0a75d64c2e6b2e1` | 15160 | the deterministic theorem, sections 2–5 (the object of this record) |
| P | `imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md` | `dfed3b8d318a3ab1950957f393307733a4bef3f2` | 40261 | Theorem A (1.1); §7 (`G_r`, (7.8)); §8 (Morse / distinct-value locus, Borel maximin); (4.3) |
| ERR | `imports/lifetime_parent_20260925/ERRATUM_CONGRUENCE.md` | `213594d6ca6a86fb938110f4d166d9ce275a02d0` | 1782 | the congruence-scaling correction the audit mentions (affects A2, not this record) |
| C1 | `reviews/d1_theorem_a_nonauthor_20260928/REVIEW.md` | `bc11369c41ebc76de5700df3f931939ccfc88b9b` | 24105 | first pass by this lane (A1–A7, CAP, §9); its script checked the constants and identity (11) for transverse dimensions 1 and 2 |
| REC | `reviews/d1_chain_reconciliation_20260928/RECONCILIATION.md` | `75da2597971510f843f8d90c743950cb8c177342` | 23312 | component table (III), embedding radius, provider ledger |

All five are on `main` at `3e0a91b` and are verified by blob in the workflow. Read but not pinned (they move with the
register): `PROOF_INDEX.md` (`030447a1`), `frontiers/downstream_gate_20260925/GRAPH.json` (`220b5686`), and the two
declarative records named in section 5.

## 0. Why this record exists

An external audit of the D1 chain (30 September 2026; text supplied to this session, not a repository object) reached the
same reading as the repository's own records — no elementary contradiction, a scoped source-bound result with
machine-assisted nonauthor review and no external peer review — and named one step as the single load-bearing
dependency: the implication from the good event `G_r` to the statement that `S` is the *global* elder-rule partner of
`M`, "including the geometry of the separating cap and the maximin connection level". It asked for that argument to be
checked line by line rather than accepted from a review ledger.

This record does three things. Section 2 redoes CAP §§2–5 in the reviewer's own words, numbering every inequality and
giving its exact arithmetic. Section 3 redoes the two steps that compose the deterministic theorem into Theorem A (the
rescaling to `G_r` and P §8's genericity and measurability). Section 4 adds finite controls of the theorem's
*conclusion* on explicit functions — a grid maximin / union-find computation showing the merge at `S` on landscapes
that satisfy the hypotheses, and a landscape that violates them whose partner is not `S` — which neither the source's
own tests nor C1's script contained (the source tests exact algebra, finite examples and mutations; C1 checked the
constants and identity (11)). Section 5 maps the audit's remaining items to the present state of the repository.

## 1. The statement under review

P §1 defines `p_r(b, k, R)` as the `Q^W` probability that the global ordinary superlevel elder death partner of `M` is
`S`, and Theorem A asserts `0 <= 1 - p_r(b, k, R) <= C r^3` (1.1) for `0 < r <= r_*`, `b in B`, `k in K`, all frames.
The chain is

    G_r := { lambda_min(-A_M) > (4/(3k)) r M_3^2,  r M_4 <= 3k/10 }                      (P §7)
    on G_r ∩ {f Morse with distinct critical values}: the global elder partner of M is S   (CAP §§2–5, P §8)
    hence 1 - p_r <= Q^W(G_r^c) <= C_3 r^3 + C_4 r^4                                       (P (7.8))

Here `A_M = D_y^2 f(M)` is the transverse Hessian at `M`, `M_3`, `M_4` the partial-block norms of CAP §1 on the local
cylinder, and `k` the scaled gap mark (`f(M) - f(S) = k r^3`; CAP writes `kappa`). This record reviews the middle line and
the way the first line feeds it. The probability estimate `Q^W(G_r^c) <= C r^3` is A1–A7 (C1 by this lane, G1 by
xAI/Grok, both recorded in REC) and is not re-reviewed here.

## 2. The deterministic theorem, line by line

Normalize `kappa = 1/6` (the general case is L26). Coordinates `(x, y) in R x R^(d-1)`; cylinder
`D = [-2r, 2r] x B̄(0, 2r)`; `f in C^4` near `D`; pins `M = (-r/2, 0)`, `S = (r/2, 0)` critical with `f(M) = b`,
`f(S) = b - r^3/6 =: s`; `m := M_3`, `n := M_4`; `lambda := lambda_min(-D_y^2 f(M))`. Hypotheses (CAP (4)):

    (H1) lambda > 8 r m^2,        (H2) r n <= 1/20.

**L1 (Hermite identity).** Let `g_0(x) = f(x, 0)`, `a = -r/2`, `c = r/2`; `g_0'(a) = g_0'(c) = 0` because the pins are
critical. With `phi(x) = (x - a)(c - x)` (so `phi'' = -2`, `phi(a) = phi(c) = 0`), two integrations by parts give
`g_0(c) - g_0(a) = -(1/2) ∫_a^c phi g_0'''`. **Exact:** `∫_a^c phi = ∫_{-r/2}^{r/2} (r^2/4 - x^2) dx = r^3/4 - r^3/12 = r^3/6`.
Hence `f(S) - f(M) = -(r^3/12) · avg_phi(f_xxx) = -r^3/6`, so the `phi`-weighted average of `f_xxx(·, 0)` on the pin
interval is exactly `2`.

**L2.** Therefore `m >= 2`, and by continuity some `x_0 in [-r/2, r/2]` has `f_xxx(x_0, 0) = 2`.

**L3 (increments).** For a `C^1` quantity `u` and points `p, q in D`, moving first in `x` then in `y` inside the product
`D`, `|u(p) - u(q)| <= sup‖∂_x u‖ |Δx| + sup‖D_y u‖ ‖Δy‖`. **Exact:** from `(x_0, 0)` or from `M` to any point of `D`,
`|Δx| <= 2r + r/2 = 5r/2` and `‖Δy‖ <= 2r`, total `<= 9r/2 < 5r`.

**L4 (CAP (5)).** `f_xxx >= 2 - 5 r n >= 2 - 1/4 = 7/4` on `D` (L2, L3, H2). For the transverse Hessian, in the
quadratic-form order, `D_y^2 f(p) <= D_y^2 f(M) + 5 r m · I <= -(lambda - 5 r m) I =: -delta I`, using that
`∂_x D_y^2 f` and `D_y^3 f` are third-order blocks bounded by `m`. **Exact:** `delta = lambda - 5rm > 8rm^2 - 5rm
= rm(8m - 5) =: rmk`, and `k = 8m - 5 >= 11` by L2.

**L5 (CAP (6)).** `w(x) := ∇_y f(x, 0)` vanishes at `a, c`; `‖w''‖ <= m`. For a unit vector `e`, the scalar `⟨w, e⟩`
vanishes at the two nodes, so by the two-node interpolation remainder `⟨w(x), e⟩ = (1/2)⟨w''(ξ), e⟩(x - a)(x - c)` with
`ξ` in the convex hull of `{a, c, x}` — valid outside the pin interval too. Taking `e = w(x)/‖w(x)‖`:
`‖w(x)‖ <= (m/2)|x^2 - r^2/4|`. **Exact:** on `|x| <= 2r`, `max |x^2 - r^2/4| = 15r^2/4`, so `‖w‖ <= (15/8) m r^2 < 2 m r^2`.

**L6 (CAP (7)).** `∫_a^c w'(t) dt = w(c) - w(a) = 0`, so `w'(x) = (1/r) ∫_a^c (w'(x) - w'(t)) dt` and, with the Lipschitz
constant `m` of `w'` along the `x`-segment, `‖w'(x)‖ <= (m/r) ∫_a^c |x - t| dt`. **Exact:** the kernel equals `r|x|` for
`|x| >= r/2` and `x^2 + r^2/4` for `|x| < r/2`; its maximum on `|x| <= 2r` is `2r^2`. Hence `‖w'(x)‖ <= 2 m r`. No common
zero of the components of `w'` is assumed.

**L7 (unique transverse maximizer).** For fixed `x`, `y ↦ f(x, y)` is `delta`-strongly concave on `B̄(0, 2r)` (L4). On
`‖y‖ = 2r`: `∇_y f(x, y) · y = w(x) · y + ∫_0^1 (D_y^2 f(x, ty) y) · y dt <= ‖w‖ · 2r - delta · 4r^2`. **Exact:**
`‖w‖ · 2r < 4 m r^3` and `delta · 4r^2 > 44 m r^3` (L4: `delta > 11 rm`), so the radial derivative is negative on the
boundary. The maximum over the compact ball is therefore attained in the interior, is unique by strict concavity, and
is the unique critical point of `f(x, ·)` in the ball; call it `h(x)`. `h(a) = h(c) = 0` (the pins are transverse
critical points). By the implicit function theorem (`D_y^2 f` invertible), `h in C^3`.

**L8 (CAP (8)).** Strong monotonicity between `0` and `h(x)`: `⟨∇_y f(x, h) - ∇_y f(x, 0), h⟩ <= -delta ‖h‖^2`, i.e.
`delta ‖h‖^2 <= ⟨w(x), h⟩ <= ‖w‖ ‖h‖`. **Exact:** `‖h‖ <= ‖w‖/delta < 2 m r^2 / (r m k) = 2r/k`.

**L9 (CAP (9)).** `h' = -(D_y^2 f)^{-1} ∂_x ∇_y f` at `(x, h(x))`; `‖∂_x ∇_y f(x, h)‖ <= ‖w'(x)‖ + m ‖h‖` (L3 in `y`) and
`‖(D_y^2 f)^{-1}‖ <= 1/delta`. **Exact:** `‖h'‖ < (2rm + 2mr/k)/(rmk) = 2/k + 2/k^2 =: u`, and `u <= 24/121` at `k = 11`,
decreasing in `k`.

**L10 (CAP (10)).** With `m = (k + 5)/8`: `m u = (k + 5)(2k + 2)/(8k^2) = (1 + 6/k + 5/k^2)/4`; at `k = 11` this is
`(121 + 66 + 5)/484 = 48/121`, decreasing in `k`.

**L11 (the ridge function and its derivatives).** `g(x) := f(x, h(x))`, `F := g' = f_x(x, h(x))` (the `∇_y f · h'` term
vanishes on the ridge). Differentiating the ridge equation `∇_y f(x, h(x)) = 0` once and twice:

    ∂_x ∇_y f + D_y^2 f · h' = 0,
    ∂_x^2 ∇_y f + 2 ∂_x D_y^2 f [h'] + D_y^3 f [h', h'] + D_y^2 f · h'' = 0.

Then `F' = f_xx + f_xy[h']` and `F'' = f_xxx + 2 f_xxy[h'] + f_xyy[h', h'] + f_xy[h'']`. By the first identity
`f_xy[h''] = -h'^T D_y^2 f h''`, and by the second `D_y^2 f h'' = -(f_xxy + 2 f_xyy[h'] + f_yyy[h', h'])`, so
`f_xy[h''] = f_xxy[h'] + 2 f_xyy[h', h'] + f_yyy[h', h', h']`. Substituting,

    F'' = f_xxx + 3 f_xxy[h'] + 3 f_xyy[h', h'] + f_yyy[h', h', h']                       (CAP (11))

with no `h''` term. (Equivalently: `g''' = D^3 f[v, v, v] + 3 D^2 f[v, v'] + Df · v''` with `v = (1, h')`, `v' = (0, h'')`,
`v'' = (0, h''')`, and both correction terms vanish because `(H_f v)_y = 0` and `f_y = 0` on the ridge.) The identity
uses only `∇_y f = 0` along `y = h(x)`; it does not identify the ridge with a gradient line. The script checks it as an
exact polynomial identity for transverse dimension 3 with a curved ridge, an `x`-dependent transverse Hessian and cubic
transverse terms (rule `RIDGE_IDENTITY_M3`; mutants `coefficient-two`, `drop-cross-terms` are refuted).

**L12 (CAP (12)).** Each correction term is bounded by `m ‖h'‖^j`, `j = 1, 2, 3`, so the adverse part is at most
`m u (3 + 3u + u^2)`. **Exact:** at `k = 11`, `(48/121)(3 + 72/121 + 576/14641) = (48/121)(53211/14641) =
2554128/1771561`, and `F'' >= 7/4 - 2554128/1771561 = 2184415/7086244 = 0.3082... > 1/4` (the bound is monotone in `k`).

**L13 (zeros of `F`).** `F(a) = f_x(M) = 0` and `F(c) = f_x(S) = 0` (L7 gives `h(a) = h(c) = 0`). `F` is strictly convex
(L12), so these are its only zeros, `F < 0` on `(a, c)` and `F > 0` outside `[a, c]`.

**L14 (critical points of `f` in `D`).** A critical point has `∇_y f = 0`, hence `y = h(x)` (L7), and `f_x = F(x) = 0`,
hence `x in {a, c}` (L13). So `D` contains exactly the two pins.

**L15 (Morse indices).** At a ridge point the Schur complement of `D_y^2 f` in the full Hessian is
`f_xx - f_xy (D_y^2 f)^{-1} f_yx = f_xx + f_xy[h'] = F'(x)`. `F'(a) < 0` (L13: `F` decreasing through its left zero) makes
`H_M` negative definite; `F'(c) > 0` gives `H_S` exactly one positive eigenvalue: `M` is a maximum, `S` has index `d - 1`.

**L16 (the cap and the ceiling `b`).** `C := [-2r, r/2] x B̄(0, 2r)`. `f(x, y) <= g(x)` (L7) and, on `C`, `g <= g(a) = b`
(L13: `g` increases up to `a`, then decreases to `c`). So `f <= b` on `C`, with equality only at `M`.

**L17 (CAP (13), longitudinal faces).** `F - (x - a)(x - c)/8` has second derivative `F'' - 1/4 > 0` (L12), vanishes at
`a, c`, hence is `>= 0` outside `[a, c]`. **Exact:** `∫_{-2r}^{a} (x - a)(x - c)/8 dx = ∫_{c}^{2r} (x - a)(x - c)/8 dx
= 9r^3/32` (substituting `t = x - a in [-3r/2, 0]`: `(1/8)∫ (t^2 - rt) dt = (1/8)(9r^3/4)`). Thus `g(-2r) <= b - 9r^3/32
= s - 11r^3/96` and `g(2r) >= s + 9r^3/32 = b + 11r^3/96` (`9/32 - 1/6 = 11/96`).

**L18 (CAP (14), curved side).** On `‖y‖ = 2r`: `f(x, y) <= g(x) - (delta/2)‖y - h(x)‖^2` (strong concavity about the
maximizer), `‖y - h‖ >= 2r - 2r/k >= 20r/11` (L8) and `delta > 22r` (L4 with `m >= 2`). **Exact:**
`(22r/2)(20r/11)^2 = 4400 r^3/121 > r^3/6`, so `f < b - 4400r^3/121 < s` on the whole curved side, corners included.

**L19 (end faces).** Right face `x = c`: `h(c) = 0`, `g(c) = s`, so `f(c, y) <= s - (delta/2)‖y‖^2 <= s` with equality only
at `S`. Left face `x = -2r`: `f <= g(-2r) < s` (L17). With L18: **every boundary point of `C` has value `<= s`, and only
`S` attains it.**

**L20 (the ridge path).** The ridge `x ↦ (x, h(x))`, `a <= x <= 2r`, lies in `D` (`‖h‖ < 2r/11`), starts at `M`, passes
through `S` and ends at `z = (2r, h(2r))` with `f(z) = g(2r) > b` (L17). Along it `f = g`, which decreases from `b` to `s`
on `[a, c]` and increases on `[c, 2r]` (L13), so its minimum is exactly `s`, attained at `S`.

**L21 (maximin level).** Every point with `f > b` lies outside `C` (L16). A continuous path from `M` to such a point
meets `∂C`, where `f <= s` (L19); so its minimum is `<= s`, whatever it does afterwards (leaving, returning, remote
excursions). The ridge path attains `s` with endpoint above `b` (L20). Therefore

    d_f(M) := sup { min_γ f : γ(0) = M, f(γ(1)) > f(M) } = s.

**L22 (elder rule).** For a Morse function with distinct critical values on a compact manifold, in the superlevel
filtration `{f >= t}` the component born at the local maximum `M` (at `t = b`) dies at the largest `t` at which it
contains a point of value `> b`, i.e. at `t = d_f(M)`; the older endpoint (`f(z) > b`) excludes the essential class. The
merge happens at a critical point of value `d_f(M) = s`; distinct critical values make it `S`. So **the global ordinary
elder death partner of `M` is `S`**. Merges of `M`'s component with *younger* components at levels above `s` do not kill
`M`'s class and do not change this.

**L23 (unstable branches; not needed for pairing).** `H_S` restricted to the transverse hyperplane is `<= -delta I`
(L4), so the positive eigenvector `e_+` of `H_S` has a nonzero `x`-component (a purely transverse vector has negative
quadratic form). For the ascending gradient flow (of any smooth Riemannian metric) the unstable manifold of `S` is
one-dimensional, tangent to `e_+`; one half-branch enters `C` (where `f > s` immediately), the other leaves it. The
branch in `C` cannot exit: exiting requires a boundary point of value `<= s` while `f` increases along the branch; its
omega-limit set is a connected set of critical points in `C`, hence `{M}` or `{S}`, and not `S` (height). The other
branch can never enter `C` for the same boundary reason. Exactly one branch ends at `M`.

**L24 (what is not claimed).** No Morse–Smale hypothesis; the ridge is not asserted to be a flow line; no statement about
points of `D` outside `C` other than L14–L15 and L20.

**L25 (uniqueness of the minimum point on the ridge).** Not needed: L21 uses only `min = s` and the endpoint value.

**L26 (general `kappa`; CAP §5).** Apply L1–L23 to `f̃ = f/(6 kappa)`: pins critical, gap `r^3/6`, birth `b/(6 kappa)`,
norms and `lambda` divided by `6 kappa`. (H1) becomes `lambda/(6kappa) > 8 r (m/(6kappa))^2`, i.e. `lambda > (4/(3kappa)) r m^2`;
(H2) becomes `r n <= 6 kappa/20 = 3 kappa/10`: exactly CAP (1) and P's `G_r`. Rescaled constants: `F'' > 6kappa/4 = 3kappa/2`
(CAP's "reduced third derivative" is the ridge's `g''' = F''`, not `f_xxx`, whose rescaled bound is `21 kappa/2`; a
reading note, not an error), longitudinal drop `6kappa · 9/32 = 27 kappa/16`, excess over the gap `6kappa · 11/96 =
11 kappa/16`, transverse drop `6kappa · 4400/121 = 26400 kappa/121`. The geometry (ridge, cap, maximin) is unchanged.
Rotating the frame changes nothing in L1–L23 as long as the product chart is embedded (section 3).

**Verdict on §§2–5:** every step re-derived; every constant reproduced exactly (rule `EXACT_CONSTANTS`; mutants
`kernel-mass`, `depth-four` show that a weaker forced third derivative or a weaker depth constant breaks the chain at
L12). No gap found. This confirms C1's ACCEPT.

## 3. Composition into Theorem A

**(a) Hypotheses match `G_r` without any norm conversion.** P §7 defines `G_r` in the cap theorem's own partial-block
norms ("for `M3`, `M4` on the local cylinder"). The conversion (4.3) between those norms and the fixed coordinate `C^4`
norm, with constants depending only on `d`, enters only the *probability* bound on `G_r^c` (through `J_r`), not the
implication `G_r ⇒` pairing. Checked against P lines 129–136 and 216–219.

**(b) The Morse / distinct-value locus.** CAP's global conclusion needs `f` Morse with distinct critical values on the
compact torus. P §8 proves this for `Q` at every fixed `r, b, k` (overdetermined-zero lemma on countable exhaustions
with bounded Gaussian densities from the uniform covariance positivity of P §3; pinned Hessians have full density;
pinned heights differ because `k, r > 0`) and transfers it to `Q^W` by absolute continuity (`0 < Z_r < ∞`). No
common null set over uncountably many parameters is claimed or needed: Theorem A is a statement for each `(r, b, k, R)`.

**(c) Measurability.** P §8 represents `{d_f(M) > h}` by countably many polygonal-path tests with rational vertices
and strict clearances, so `{d_f(M) = f(S)}` is Borel in `(M, f)`; the event in `p_r` is therefore a `Q^W`-event. L21
is exactly the equality `d_f(M) = s`.

**(d) Embedding.** The cylinder `D` must be an embedded product chart of the torus so that L1–L23 (in particular L21's
"every path from `M` to a higher point meets `∂C`") are statements about the torus. REC makes the radius explicit,
`r < L/(4√2)`, and D1's `r_*` is below it. On `G_r` and the locus of (b), L22 then says the *torus* elder partner of `M`
is `S`: this is the middle line of section 1, and (7.8) closes Theorem A.

**Verdict on the composition:** ACCEPT at Theorem A's existential scope (fixed `d >= 2`, `L`, compact `B`, `K` with
`k_- > 0`, all frames, `r <= r_*`), unchanged from C1/G1 and REC.

## 4. Finite controls (`cap_maximin_check.py`, standard library, about 4 s)

| Rule | What it establishes | Result |
|---|---|---|
| `EXACT_CONSTANTS` | L1–L18 and L26 constants in exact arithmetic: kernel mass `1/6`, average `2`, distance `9/2 < 5`, `7/4`, `k >= 11`, `15/4`, kernel max `2`, `u = 24/121`, `mu = 48/121`, adverse `2554128/1771561`, `F'' >= 2184415/7086244 > 1/4`, exterior integrals `9/32`, excess `11/96`, drop `4400/121 > 1/6`, rescaled `3kappa/2`, `27kappa/16`, `11kappa/16`, `26400kappa/121`, and `(4/(3kappa), 3kappa/10)` | true |
| `RIDGE_IDENTITY_M3` | identity (11) for transverse dimension 3, `f = p(x) - ½(y - Q)^T A(x)(y - Q) + cubic(y - Q)` with quadratic and cubic `Q_i(x)`, `A(x) = A_0 + x A_1`, `x`-dependent cubic coefficients and a quartic `p` (so `F''` is not constant); the ridge gradient vanishes, `g = p`, LHS = RHS as polynomials, and `F'' ≠ f_xxx` on the family | true |
| `MAXIMIN_D2`, `MAXIMIN_D3` | explicit landscapes `f = b + p(x) - (λ/2)‖y‖² + ε(x² - r²/4) y_1` with `p' = x² - r²/4`, `r = 1/50`, `λ = 1`, `ε = 1/2`: `M_3 = 2`, `M_4 = 0` exactly, `λ = 1 > 8 r M_3² = 16/25`, so (H1)–(H2) hold; on grids of spacing `r/20` (`81²` cells) and `r/12` (`49³` cells), activating cells in decreasing height with union-find, the component of `M` first acquires a point of value `> b` exactly when the grid point `S` is activated: grid maximin level `= s = 1.19999866667`, merge offset from `S` `0` steps | true |
| `HYPOTHESIS_LOAD_BEARING` | the same pins with a quartic transverse rim `+ β‖y‖⁴`, `β = 10^5`: `M_3 >= 48 β r = 96000`, `r M_4 = 48000`, so (H1)–(H2) fail inside `D`; the rim pass along `x = -r/2` sits at `b - 1/(16β) = 1.199999375 > s` and inside `D`; the grid maximin level is `1.19999938667` (above `s` by `0.54` of the gap `κ r³`) and the merge happens `42` steps from `S`: the elder partner of `M` is the rim pass, not `S` | true |

Mutants (each exits 1): `kernel-mass`, `depth-four` (constants chain), `coefficient-two`, `drop-cross-terms` (identity),
`no-depth` (the rim landscape fed to `MAXIMIN_D2`), `gap-sign` (`S` above `M`). Both interpreter modes give
byte-identical output. The grids are demonstrations on explicit polynomials; they prove nothing about arbitrary `C^4`
fields. The proof is section 2.

## 5. The audit's other items, against the repository at `3e0a91b`

| Audit item | State | What would change it |
|---|---|---|
| **19.1** reviews are not institutionally independent | Correct, and stated in every record (REC §"Providers": author OpenAI; nonauthor lanes xAI/Grok and Anthropic/Claude; one GitHub account; zero organizational-independence credit). Nothing inside the repository can change this. | External human peer review of P, CAP and the A1–A7/§8 arguments. This record is offered as a self-contained line-by-line derivation to make that review cheaper, not as a substitute. |
| **19.2** a real correction (congruence scaling) | ERR (`213594d6`): `D_r = diag(r^{-1/2}, I)`, not `diag(√r, I)`. It affects A2 (the Hessian congruence in the normalizer), not CAP; C1's `check_a2` uses the corrected scaling. The reading rule "P read with ERR" is the object accepted in REC. | Nothing further; the erratum is in the provenance chain. |
| **19.3** no numerical `c_{d,L}` in general | P (1.3): the constant is an identified finite Gaussian/angular integral, "no elementary closed form or numerical enclosure is claimed". `coefficients/side24_v1` encloses `c_{2,24}` and `c_{3,24}` (`0.07340691930603427103…104`, `0.04177593184059834334…335`), explicitly conditional on the identification with the finite-bar coefficient. | Certified enclosures for `d = 4, 5` need the negative-definite cone moments `D_u` of `3 x 3` and `4 x 4` Gaussian matrices (Math-#184 gives uncertified values `m_{d,0}` for `d <= 5`); feasible with the SIDE24 machinery, not done. |
| **19.4** no quantitative remainder for the unrestricted theorem | P (1.2) gives `0 <= ν_cand - ν_eld <= C ℓ^{2/3}` on compact windows only; (1.3) is a leading term. Open candidates awaiting non-Claude reads: Math-#191 (`ν_cand = cℓ^{-1/3} + B_{d,L} + o(1)`, `ν_eld = cℓ^{-1/3} + o(1)`; constant term identified, no rate), Math-#187 (far elder `O(ℓ^{2/3})`), Math-#188 (far elder `O(ℓ^N)`). | A rate for the unrestricted remainder needs the far-elder constant's dependence on the separation `ρ` (Math-#191 Remark 2). Not resolved. |
| **19.5** no formal verification | Not supplied for D1; the Lean checks in the repository cover scalar companions only. | A Lean formalization of P/CAP; out of scope for this record. |
| **§20** `math.rn-region.witness-collision` `OPEN_ACTIVE` | True in the live register at `3e0a91b` (GRAPH node: layer D5, catalog C6, `OPEN_ACTIVE`; PROOF_INDEX line "NO COMPLETE REGIONAL PROOF YET"). The **merged, reviewed** declarative record Math-#160 (`reviews/c6_witness_collision_reconciliation_20260929/PROPOSED_TRANSITIONS.json`, blob `8d70ee74`) proposes `OPEN_ACTIVE → PROVED_REVIEWED` for this node at the scope stated there (torus-wide factorial moments of the window count, every fixed `d >= 2`, existential constants, upper bounds for Borel selectors, lower bound global on the EDL event), resting on the merged sources it lists (the Palm route, the factorial-moment record, the dimension lifts, P, the D5 reconciliation); the residual node it opens (leading-mass localization) is closed by the merged Math-#173 (`reviews/c6_residual_closure_20260930`, blob `3706e8ac`). The register edits themselves are a separate execution reserved for a non-Claude lane; Math-#183 (open) makes the three records' checkers accept the installed state so that execution can be gated. The PROOF_INDEX sentence is scheduled to keep its text with a citation to the closure record (Math-#160 OBLIGATION). **D1 does not depend on this node**: REC's required edges for the D1 node are E1, E2, CAP and the §9 repair, as the audit also observes. | The non-Claude execution of #160/#167/#173 (after which the node reads `PROVED_REVIEWED` at the stated scope), or a non-Claude review that rejects those records. |

## 6. Verdict

The implication `G_r ∩ {Morse, distinct values} ⇒ d_f(M) = f(S) ⇒ S is the global elder partner of M` is proved by CAP
§§2–5 as written, with every constant exact and every step re-derived here (L1–L26); its composition into Theorem A
through P §§7–8 and the embedding radius of REC is sound. **ACCEPT, unchanged.** No new finding; one reading note (L26).
The finite controls of section 4 add executable evidence that the conclusion holds on explicit functions satisfying
(H1)–(H2) and fails on an explicit function violating them.

## 7. Exposure, limits, non-claims

This lane authored none of P, CAP, ERR or REC's sources; it authored C1 (28 September), the D1 chain reconciliation REC
(disclosed there as a dual role), the register alignment and C6 reconciliation records named in section 5, and the
readiness packet Math-#183. Same account and same provider as the other Claude lanes; the xAI/Grok reads (D1-A–E,
`EMBEDDED_CHART_AND_MORSE`) are the provider-distinct ones. A second pass by the same reviewer adds depth and
executable controls, not independence. Not reviewed here: A1–A7 (the probability of `G_r^c`), §9, Theorems B and C,
SIDE24. No register, catalog, STATUS, PROOF_INDEX or GRAPH change; scientific effect NONE; the reviewer will not merge.

## 8. Files

`REVIEW.md` (this record), `cap_maximin_check.py`, `RESULTS.json` (its stdout, byte-identical under `-B -S` and
`-B -O -S`), `SOURCE_FILES.json` (manifest and the five `main` pins), workflow
`.github/workflows/d1-cap-elder-partner-second-pass.yml` (manifest, pins by blob, both modes, six mutants, clean tree).

    python -B -S reviews/d1_cap_elder_partner_second_pass_claude_20260930/cap_maximin_check.py | diff - reviews/d1_cap_elder_partner_second_pass_claude_20260930/RESULTS.json
