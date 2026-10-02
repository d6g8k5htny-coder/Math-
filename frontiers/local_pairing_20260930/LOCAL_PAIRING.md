# Local pairing: the local landscape decides the elder pairing, and the selection loss is bounded below by the local cluster mass

Object: CL-LOCAL-PAIRING-20260930-v1.
Author: Anthropic Claude (claude.ai session `session_01NMeKEismAyeqgdB4sy2NJU`), 30 September 2026.
Disposition: AUTHOR-SIDE PROOF CANDIDATE; NONAUTHOR REVIEW REQUIRED. Lemmas 2.1–2.2, Lemma P, Lemma P′
and Proposition 3.3 are deterministic statements about the pinned cubic with complete written proofs
(reviewed twice by clean-context referee agents before landing; every blocking finding and amendment they
raised is applied below). Theorem LP (the lower bound with an identified functional) is conditional: it consumes exact
interfaces of [SC], [CUB] and [P] at their own review status. Conjecture LP= (equality) is stated with its
single remaining probabilistic obligation. **Relation to Math-#170 and Math-#175 (v1.1, added after landing).**
The OpenAI packet Math-#170 (`frontiers/local_elder_geometry_20260930/PROOF.md`, head `79f18f0`, blob
`ef2aa579`, opened before this packet; integrated into main at `fa2e990`) proves the same deterministic statement as Lemma P′ + Proposition 3.3
(its Theorem E, by the cubic critical-chord identity and a normalized-gradient collar rather than the explicit
paths used here) and proves the **equality** `r⁻³(1 − p_r) → α₁ + α₂` at fixed planar marks (its Theorem S) by a
route this packet does not use: [P]'s cap implication `F_r ⊂ G_r^c` and a retained-tail integration of [P] §7.
Math-#175 (`frontiers/concave_fibre_elder_20260930/`, head `9c6a734`, proof blob `923d3236`; integrated into main at
`eb659bd`) lifts it to fixed `d ≥ 3` by a contained
hard-negative tube. So Conjecture LP= below is Math-#170 Theorem S (planar) / Math-#175 Theorem F (`d ≥ 3`),
conditional on their interfaces and review; what this packet adds is an independent same-account derivation
of the deterministic core with exact controls, and the cap-free lower bound Theorem LP. Scientific effect:
NONE — no register, graph, STATUS, prize or Boolean changes; no numerical constant is claimed.
**v1.2 (2 October 2026), answering the Slice C review.** Codex's Slice C review (C85, 5396856086) found
C-01: v1.1's optional §5 margin sketch confined `M`'s component at one level above `f(S)` only, and it gave an
exact falsifier. v1.2 withdraws that sketch as a proof. In its place §5 states Lemma 5.1, a common-radius
acceptance lemma that controls the component through the exact saddle level. It is consumed from QS-E (main#229
5961415030; author-side candidate, nonauthor review requested), with exhausting jet-scaled margin sets
`𝓜(η, R)`. §5 also records the review's notes on the weighted normalization and on Gaussian conditioning, and
now says that the reverse reduction (O1′) ⇒ (O1) is conditional on Lemma 5.1. Lemmas 2.1–2.2, P, P′,
Proposition 3.3, Theorem LP, the controls and the cap bypass are unchanged.

## 0. What this packet answers, and what it does not

The question put to the project on 2026-09-30 (input relayed by the owner) was: the account knows how many
extra window critical points there are near a short-lifetime pair (Theorem Q: `Θ(r³)`), but not *which
of them pair* and whether *the pairing is local*. Three sub-questions were asked. The answers, at the
scope stated below:

1. **Mixed pairs are already local, conditionally.** For any cutoff `δ_r → 0` with `δ_r/r → ∞`, the
   ordered-pair mass with a point outside the `δ_r` ball is `o(r³)` ([TSL] Theorem L, from [SC] (24) and
   the [C6] moments; nonauthor-reviewed at conditional scope). Remote–remote pairs are `O_ρ(r⁵)` ([SC] (2)).
   The only non-local piece of the *nonempty* event is a **remote singleton** of positive mass `β_far`
   ([SC] (22); [TSL] Theorem T). So "the rare event is local" is true for pairs and false for singletons.
   Nothing in this packet re-proves those statements. (The leading-mass localization residual of Math-#160 §5
   is bound to Theorem L as its direct statement by the declarative record [RES], Math-#173; that record proposes
   register transitions and executes none.)
2. **Which witnesses pair.** On the limiting local landscape — the pinned planar cubic `P_θ` of [CUB] —
   the elder rule is decided exactly: off the null tie set `{s ≤ B, D² = T}`, `(M,S)` is the elder pair **iff**
   the cubic has no extra strict-window critical point (`n(θ) = 0`) (Lemmas P, P′); if `n(θ) ≥ 1`, `M` dies at
   the highest extra window saddle (Proposition 3.3).
   Transferred to the field, this gives the lower bound
   `liminf r⁻³ (1 − p_r) ≥ a₁ + a₂ = ν₁ + ν₂ − β_far` (Theorem LP), where `a₁, a₂` are the local coefficients
   of [SC] (20) and `β_far` its remote coefficient. Equality — the statement that **remote witnesses never
   pair** — is Conjecture LP= with one obligation (§5); it is proved by Math-#170 Theorem S (planar) and
   Math-#175 Theorem F (`d ≥ 3`) by the cap route described in the header, at their conditional scope. This is
   the bridge from the count law to the lifetime law: it bounds the existential `Θ(r³)` selection loss of [P]
   Theorem A / [ELDER] / [E_d] from below by an explicit functional of the cluster measure, and identifies it
   under LP=.
3. **Cluster law.** Nothing new: [SC] (3) identifies `ν = ν₁δ₁ + ν₂δ₂`; this packet uses only its local part.

What the bridge is worth for the lifetime density is stated without inflation in §6: it bounds from below
(and, under LP=, fixes) the coefficient of the `Θ(ℓ^{2/3})` compact-window selection loss — relative order
`ℓ` against the leading `ℓ^{−1/3}`; the leading law never needed it, and the unrestricted density's bounded
remainder is a different object.

## 1. Setting and exact sources

Fixed `d ≥ 2`, torus side `L`, birth `b`, gap mark `k > 0`, one orthonormal frame. Pins
`M = (−r/2, 0)`, `S = (r/2, 0)`, `f(M) = b`, `f(S) = b − k r³`, zero gradients; regression law `Q_r`;
typed determinant weight `W_r`, FULL normalizer `Z_r`, `Q_r^W = (W_r/Z_r) Q_r`. `p_r` is the `Q_r^W`
probability that the **global ordinary superlevel elder death partner** of `M` is `S` ([P] §1, [ELDER] §1).
On the generic locus its death height is the maximin

    d_f(M) = sup { min_t f(γ(t)) : γ(0) = M, f(γ(1)) > f(M) },                    (E1)

with the empty-supremum convention of [P] §8; `S` is the death partner iff `d_f(M) = f(S)` and `S` is the
critical point at that level ([ELDER] §1). A path from `M` to a point strictly above `b` whose values stay
strictly above `f(S)` therefore proves that `S` is **not** the death partner. Nothing here uses gradient
trajectories or separatrices.

Sources (exact identities in `SOURCES.json`; none is revalidated here):

| Tag | Source | What is consumed |
|---|---|---|
| [P] | `imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md` | §1 model and `p_r`; Theorem A upper bound `1 − p_r ≤ C r³`; §8 genericity; §§9–11 radial ledger and (E9)-type intensity. |
| [ELDER] | `frontiers/window_multiplicity_laws_20260928/ELDER_LOWER_AND_DENSITY_GAP.md` | (E1) maximin characterisation; §2 the stable-`C⁰`-connectivity transfer template; §4 (E9)–(E11) density gap in `d = 2`. |
| [CUB] | `frontiers/planar_cubic_cluster_20260929/PROOF.md` | (C1)–(C3) pinned cubic and shear; (C4) typed condition; Theorem C classifier `n(θ) ∈ {0,1,2}`; (C7)–(C13). Only the deterministic part. |
| [SC] | `frontiers/spectral_cluster_closure_20260929/PROOF.md` (Math-#162, reviewed at head `382c0f9`, merged at `358f256` with identical bytes; proof blob `16c56821`) | §2 spectral coordinates and (10); §5 normal form: `[f(rX,rZ,0) − b]/r³ → P_θ` in `C²` on bounded sets, the limit `W_r/r⁴ → ∏h_j² w`, and the rescaled typed-jet measure (17); (18)–(20): `a₁, a₂`; (22): `β_far`; (2), (24) as cited in §0. |
| [TSL] | `frontiers/two_scale_cluster_geometry_20260929/TWO_SCALE_LAW.md` (Math-#166, reviewed at head `7c82252`, merged at `ab13a08` with identical bytes; blob `a32fd5f7`) | Theorem L, Theorem T — cited in §0 only; not consumed by any proof below. |
| [E_d], [EDL] | `frontiers/elder_lower_all_d_20260929/PROOF.md`, `frontiers/elder_dimension_lift_20260928/PROOF.md` | The existential lower bound `1 − p_r ≥ c r³` in every `d` that Theorem LP sharpens; not consumed. |
| [C7] | `frontiers/c7_total_bounded_20260929/PROOF.md` (Theorem K / Corollary T), `frontiers/c7_zero_gap_limit_20260929/PROOF.md` (Theorem Z), `frontiers/unrestricted_selection_difference_20260929/PROOF.md` (Theorem U) | Cited in §6.3 only for the order of the unrestricted remainder; not consumed. |
| [RES], [NUM] | `reviews/c6_residual_closure_20260930/RECONCILIATION.md` (Math-#173), `frontiers/c6_cluster_coefficients_numerics_20260930/NOTE.md` (Math-#168) | Cited in §0 and §6.4 only (the residual-closure record; uncertified numerical values of the near coefficients); not consumed. |

A defect in a consumed interface blocks the corresponding statement here. In particular Theorem LP is
conditional on [SC] at exactly the same scope as [TSL].

## 2. The pinned cubic and the elder rule on it

In the sheared coordinates `(u, Z)` of [CUB] (C2)–(C3), with `B = β − a²/(12k)` and
`D = (c − aβ/(4k) + a³/(72k²))/2`,

    P(u, Z) = A(u) + (Z²/2)(s + Bu) + (D/3) Z³,        A(u) = 2k (u − 1)(u + 1/2)².          (2.1)

`M = (−1/2, 0)` with `P = 0`, `S = (1/2, 0)` with `P = −k`. The typed domain is `s < −|B|/2` ([CUB] (C4)).
Elementary facts about (2.1) (the identities among them, and the shear (2.1) itself against [CUB] (C1)–(C3),
are checked exactly by `pairing_check.py`, I0–I3; the monotonicity statements are one-line calculus):

* **Axis.** `A′(u) = 6ku² − 3k/2`, so `A` is decreasing on `(−1/2, 1/2)` from `0` to `−k` and increasing for
  `|u| > 1/2`; `A(u) + k = (k/2)(u + 1)(2u − 1)²`, so `A(u) > −k` iff `u > −1` and `u ≠ 1/2`; `A(u) > 0` iff
  `u > 1`; `A(u) → +∞` as `u → +∞`. Because (2.1) has no term linear in `Z`, `∇P(u, 0) = (A′(u), 0)`: the
  sheared axis `{Z = 0}` is an invariant line of `∇P`.
* **Vertical lines.** At fixed `u`, `∂_Z P = Z (s + Bu + DZ)`. If `s + Bu < 0` and `D ≠ 0`, `P(u, ·)` decreases
  from `A(u)` at `Z = 0` to a minimum at `Z₁(u) = −(s + Bu)/D` (on the side `sign Z = sign D`) and then
  increases to `+∞`. If `s + Bu = 0` and `D ≠ 0`, `P(u, Z) = A(u) + DZ³/3` is monotone to `+∞` on the `D` side
(level if `D = 0`).
* **Extra critical points.** `(u₁, Z₁)`, `Z₁ ≠ 0`, is critical iff `A′(u₁) + (B/2)Z₁² = 0` (conic) and
  `s + Bu₁ + DZ₁ = 0` (line); then `P(u₁, Z₁) = A(u₁) + Z₁²(s + Bu₁)/6` ([CUB] (C8) in this form), so
  `P(S₁) < A(u₁)` iff `s + Bu₁ < 0`, and `D ≠ 0` unless `s + Bu₁ = 0`. [CUB] Theorem C: every strict-window
  extra critical point is a nondegenerate saddle, there are at most two, and their number `n(θ)` is (C6). For
  `B > 0` they satisfy `−1/2 < u₁ < u_w < 1/2`; for `B < 0`, `u_w < u₁ < −1/2` with `u_w = −1/2 − B/(2s)`;
  for `B = 0`, `u₁ = −1/2`.
* **`M` is a strict local maximum.** `Hess P(M) = diag(−6k, s − B/2)` and `s − B/2 < 0` on the typed domain.

**Lemma 2.1 (growth at infinity; older components).** For every typed `θ`: (a) `|∇P(x)| → ∞` as `|x| → ∞`,
and `P` has finitely many critical points; (b) for every `h ≥ −k`, every unbounded component of `{P > h}`
contains points with `P > 0`.

*Proof.* (a) Suppose `|∇P| ≤ C` along a sequence with `|x| → ∞`. If `|Z|` stayed bounded, `∂_u P = 6ku² − 3k/2
+ (B/2)Z²` would diverge; so `|Z| → ∞` and `|s + Bu + DZ| ≤ C/|Z| → 0`. If `B = 0` this forces `D = 0` and then
`|s| ≤ C/|Z| → 0`, impossible. If `B ≠ 0`, `u = −(DZ + s)/B + o(1)` and
`∂_u P = [6kD²/B² + B/2] Z² + (12kDs/B²) Z + O(1)`; the `Z²` coefficient vanishes only when `12kD² + B³ = 0`,
which needs `B < 0` and `D ≠ 0`, and then the linear term `12kDs/B²` is nonzero because `s < 0`; either way
`∂_u P` diverges. Critical points are the intersections of the conic `A′(u) + (B/2)Z² = 0` (irreducible for
`B ≠ 0`; the two lines `u = ±1/2` for `B = 0`) with `Z = 0` or the line `s + Bu + DZ = 0`, finitely many.
(b) Write `P(ρ cos φ, ρ sin φ) = c₃(φ)ρ³ + c₂(φ)ρ² + c₁(φ)ρ + c₀` with `c₃(φ) = 2k cos³φ + (B/2) cos φ sin²φ
+ (D/3) sin³φ`, `c₂(φ) = (s/2) sin²φ` (the only quadratic term of (2.1) is `sZ²/2`), `c₁(φ) = −(3k/2) cos φ`,
`c₀ = −k/2`. At a zero `φ₀` of `c₃`, `sin φ₀ ≠ 0` (since `c₃(0), c₃(π) = ±2k`), so by continuity and compactness
there are `η ∈ (0, 2k)` and `σ > 0` with `|sin φ| ≥ σ` on `{|c₃(φ)| ≤ η}`; put `μ = |s|σ²/2`, so that `|c₂| ≥ μ`
there, and note `|c₂| ≤ |s|/2` everywhere. Choose `ρ₀` so large that for all `ρ′ ≥ ρ₀`:
`ηρ′³ > |s|ρ′²/2 + (3k/2)ρ′ + 3k/2`, `(μ/4)ρ′² > (3k/2)ρ′ + 3k/2`, `(μ/4)ρ′ > 3k/2`, and `3ηρ′² > |s|ρ′ + 3k/2`.
For `ρ ≥ ρ₀` and any `φ` one of four cases holds:
(1) `c₃ ≤ −η`: `P ≤ −ηρ³ + |c₂|ρ² + |c₁|ρ + |c₀| < −k`;
(2) `|c₃| < η` and `c₃ρ ≤ (3/4)|c₂|`: `P ≤ (3/4)|c₂|ρ² − |c₂|ρ² + (3k/2)ρ + k/2 ≤ −(μ/4)ρ² + (3k/2)ρ + k/2 < −k`;
(3) `0 < c₃ < η` and `c₃ρ > (3/4)|c₂|`: for every `ρ′ ≥ ρ`, `∂_ρ P(ρ′) = 3c₃ρ′² + 2c₂ρ′ + c₁ ≥ 3c₃ρρ′ − 2|c₂|ρ′ −
3k/2 > (1/4)|c₂|ρ′ − 3k/2 ≥ (μ/4)ρ′ − 3k/2 > 0`;
(4) `c₃ ≥ η`: for every `ρ′ ≥ ρ`, `∂_ρ P(ρ′) ≥ 3ηρ′² − |s|ρ′ − 3k/2 > 0`.
So every point with `|x| ≥ ρ₀` and `P(x) > −k` is of type (3) or (4), and along its ray `P` increases strictly to
`+∞`: the point is connected outward, inside `{P > P(x)}`, to points with `P > 0`. An unbounded component of
`{P > h}`, `h ≥ −k`, contains points with `|x| ≥ ρ₀`, hence points with `P > 0`. ∎

**Lemma 2.2 (the death level is a critical value).** For every typed `θ`, `h* := d_P(M)` satisfies
`−k ≤ h* < 0`, and if `h* > −k` then `h*` is the value of an extra strict-window critical point of `P`, so
`n(θ) ≥ 1`.

*Proof.* `h* ≥ −k` by the axis path `M → S → {u > 1}` (values `≥ −k`, endpoint `A(u) > 0` for `u > 1`);
`h* < 0` because `M` is a strict local maximum, so for `h` close to `0` the `M`-component of `{P > h}` is a
small disk containing no point with `P > 0`. Suppose `h* > −k` is not a critical value. By Lemma 2.1(a) the
critical values are finitely many, so there is `ε > 0` with no critical value in `[h* − ε, h* + ε]`, and
`|∇P| ≥ c > 0` on `P^{−1}[h* − ε, h* + ε]` (a Palais–Smale sequence there would be bounded by Lemma 2.1(a) and
converge to a critical point at a level in the interval). Let `φ_t` be the flow of `∇P/|∇P|²` on the slab
`P^{−1}[h* − ε, h* + ε]`, along which `P` increases at unit rate, and define `η(x) = φ_{h* + ε − P(x)}(x)` for
`x` in the slab and `η(x) = x` for `P(x) ≥ h* + ε`; `η` is continuous, maps `{P ≥ h* − ε}` into `{P ≥ h* + ε}`,
and fixes `{P ≥ h* + ε}`. Shrink `ε` so that `ε < |h*|`. By definition of `h*` there is a path from `M` to a
point `y` with `P(y) > 0` with values `> h* − ε`; `η` of it is a path with values `≥ h* + ε > h*` from `M`
(fixed, since `P(M) = 0 > h* + ε`) to `y` (fixed), contradicting the supremum. So `h*` is a critical value in
`(−k, 0)`. A critical point at a level in `(−k, 0)` is not a pin and is counted by `n` ([CUB] §2: `n` counts
all additional critical points with height strictly between `−k` and `0`), so `n ≥ 1`; by Theorem C it is a
nondegenerate saddle. ∎

## 3. Lemma P: every extra window saddle rejects the pair

**Lemma P.** Let `θ = (s, a, β, c)` be typed with `n(θ) ≥ 1`, and let `(u₁, Z₁)` be an extra strict-window
critical point. Then there is an explicit path `γ` from `M` to a point with `P > 0` whose minimum exceeds
`−k`; consequently `d_P(M) > −k`, and `(M,S)` is **not** the elder pair of `P`. The path is one of:

* **V (vertical descent at `u₁`)** — when `s + Bu₁ < 0` and `−1 < u₁ < 1/2`: along the axis from `M` to
  `(u₁, 0)`, then along the vertical line through `S₁` past `S₁` to `+∞` on the `D` side. Its minimum is
  `P(S₁) ∈ (−k, 0)`, attained at `S₁`.
* **U (vertical rise at `u₀`)** — when `B < 0` and `s > B` (equivalently `|B|/2 < |s| < |B|`): along the
  axis from `M` to `(u₀, 0)`, `u₀ = −s/B ∈ (−1, −1/2)`, then along the vertical line at `u₀`, on which
  `P = A(u₀) + DZ³/3`, to `+∞` on the `D` side. Its minimum is `A(u₀) ∈ (−k, 0)`.

Let `S_V` be the extra strict-window root with the largest `u`-coordinate. The proof shows that path V
applies at `S_V` whenever `D ≠ 0` (in case (iv) `S_V` is the root on the side `u > u₀` of `u₀ = −s/B`, which
exists both for `n = 1` and for `n = 2`); path U is a second valid path in case (iv), and the `D = 0` subcase
of (iv) has its own path. The margin of Lemma P is `m(θ) := P(S_V) + k` for `D ≠ 0` and `A(u₀) + k` for
`D = 0` in case (iv); it is positive, and it is continuous on the typed `n ≥ 1` domain: `S_V` is a
nondegenerate root ([CUB] Theorem C), so it depends continuously on `θ` by the implicit function theorem; it
persists across `s = B` and across `D² = T` (the root that appears or disappears there is the other one, at
`u_w`); and as `D → 0` in case (iv) its value tends to `A(u₀)`. Theorem LP uses this continuity to make its
jet sets compact.

*Proof.* Axis parts: by the monotonicity of `A` in §2, the values along the axis from `M` to `(u*, 0)`
lie in `[A(u*), 0]`, and `A(u*) > −k` because `−1 < u* < 1/2` in both cases. Vertical parts: by the
vertical-line fact in §2. It remains to see that every typed jet with `n ≥ 1` falls in V or U.

(i) `B > 0`. Then `−1/2 < u₁ < 1/2` and `s + Bu₁ < −B/2 + Bu₁ = B(u₁ − 1/2) < 0` by the typed condition: V.

(ii) `B = 0`. Then `u₁ = −1/2` and `s + Bu₁ = s < 0`: V (the axis part is empty; the vertical line starts at `M`).

(iii) `B < 0`, `s ≤ B` (`|s| ≥ |B|`). Then `n = 1` by (C6) and `u_w = −1/2 − |B|/(2|s|) ≥ −1`, so
`−1 < u₁ < −1/2`. The linear function `s + Bu` vanishes at `u₀ = −s/B = −|s|/|B| ≤ −1 < u₁` and is
decreasing in `u` (`B < 0`), hence `s + Bu₁ < 0`: V.

(iv) `B < 0`, `s > B` (`|B|/2 < |s| < |B|`). Then `u₀ = −|s|/|B| ∈ (−1, −1/2)` and `A(u₀) > −k`. If `D ≠ 0`:
in the proof of [CUB] Theorem C the extra roots are the solutions of `g(u) = D` on the `Z > 0` branch and of
`g(u) = −D` on the `Z < 0` branch of the window conic, where `g` is strictly increasing on `(u_w, −1/2)`
([CUB] (C12)) and vanishes at `u₀` (there the line `s + Bu + DZ = 0` reduces to `DZ = 0`). Hence for `n = 2`
the two roots lie on opposite sides of `u₀`, and for `n = 1` the single root solves `g(u) = |D| > 0 = g(u₀)`;
in both cases `S_V` has `u₁ > u₀`, so `s + Bu₁ < 0` (`s + Bu` decreases in `u` for `B < 0`) and
`−1 < u₀ < u₁ < −1/2`: V at `S_V`. Path U — along the axis to `(u₀, 0)`, then the vertical line
`P = A(u₀) + DZ³/3` to `+∞` on the `D` side, minimum `A(u₀)` — is a second valid path. If `D = 0`,
`P(u, Z) = A(u) + (Z²/2) B (u − u₀)` and the vertical line at `u₀` is level; take instead
`M → (u₀, 0) → (u₀, Z) → (u₀ − ε, Z)` with `Z` large: on the last segment `B(u − u₀) ≥ 0`, so
`P ≥ A(u) ≥ A(u₀ − ε) > −k` for small `ε`, and its endpoint value `A(u₀ − ε) + (Z²/2)|B|ε` exceeds `0` for
`Z` large. ([ELDER]'s witness `(−3k/2, 0, −2k, 0)` is this subcase with `u₀ = −3/4`; its polygonal path (E5)
has minimum `−7k/32`, and `pairing_check.py` P2 verifies that both extra saddles sit exactly at `−7k/32`.)

In V the minimum along the whole path is `P(S₁)`, which lies in `(−k, 0)` by the strict-window hypothesis;
in U it is `A(u₀) > −k`; in the `D = 0` path it is `A(u₀ − ε) > −k`. In all of them the far end has `P > 0`. ∎

`pairing_check.py` P1 verifies, exactly, on `6840` rational chart points (three values of `k`), that every
chart point is a typed strict-window critical point with `n ≥ 1`, and the inequalities of the path through
the chart root: V when `s + Bu₁ < 0` and `−1 < u₁ < 1/2` (`4680` points: `A(u₁) > P(S₁) > −k`,
`sign Z₁ = sign D`, the rise past `0`), otherwise U (`2160` points, all in case (iv) with the chart root on the
side `u₁ < u₀`: `u₀ ∈ (−1, −1/2)`, `A(u₀) > −k`, the rise past `0`). For those `2160` points it also computes
the other root exactly (Vieta on [CUB] (C13)), and verifies that it is a strict-window root on the side
`u > u₀`, that V applies to it, and that it is the higher of the two — so the proof's assignment (V at `S_V`)
and the ordering claim of Proposition 3.3 are exercised on every chart point. Smallest margin `1/1200`
(absolute; attained at `k = 1/3`).

**Lemma P′ (converse).** If `θ` is typed, `n(θ) = 0`, and `S` is the only critical point of `P` at level
`−k` (this excludes the null set `{s ≤ B, D² = T}` of [CUB] (C6)), then `(M,S)` is the elder pair of `P`:
`d_P(M) = −k` and the merge at level `−k` is through `S`.

*Proof.* By Lemma 2.2 and `n = 0`, `d_P(M) = −k`. Let `C` be the component of `M` in `{P > −k}`. `C` contains
no point with `P > 0` (such a point would give `d_P(M) > −k`), so by Lemma 2.1(b) `C` is bounded. The sheared
axis is `∇P`-invariant with `∇P(u, 0) = (A′(u), 0)`: the segment `(−1/2, 1/2)` is the ascending branch of `S`
into `M` (`A` increases toward `M` on it, and its values lie in `(−k, 0)`, so it lies in `C`), and the ray
`u > 1/2` is the other ascending branch of `S`, on which `A` increases to `+∞` and exceeds `0` for `u > 1`.
So one upper sector of `S` lies in `C` and the other in a component `C′` of `{P > −k}` containing points with
`P > 0`; `C′ ≠ C`. At level `−k` the component of `M` in `{P ≥ −k}` therefore contains `C′` through `S`, and
through no other point, since `S` is the only critical point at that level. `M`, the younger, dies at `S`. ∎

**Proposition 3.3 (the death saddle).** If `θ` is typed with `n(θ) ≥ 1`, then `d_P(M) = max{P(S′) : S′ an
extra strict-window saddle}`. Off the additional null set `{D = 0}` the maximum is attained at exactly one
extra window saddle, and `M` dies there: the highest extra window saddle. (For `D = 0` in case (iv) the two
extra saddles `(u₀, ±Z₀)` have the same height `A(u₀)` — the [ELDER] witness is such a jet — so only the death
level, not a unique death saddle, is determined; on the Morse distinct-value locus of the field this tie
does not occur.)

*Proof.* By Lemma P, `d_P(M) > −k`; by Lemma 2.2, `d_P(M)` is the value of an extra strict-window saddle.
If `n = 1` there is nothing more to show. `n = 2` occurs only in case (iv) of Lemma P (`B < 0`, `s > B`,
[CUB] (C6)). There, in [CUB]'s notation, the two saddles solve `g(u) = D` on the `Z > 0` branch and
`g(u) = −D` on the `Z < 0` branch of the window conic, with `g` strictly increasing on `(u_w, −1/2)` and
`g(u₀) = 0` at `u₀ = −s/B` (at `u = u₀` the line reduces to `DZ = 0`). So for `D ≠ 0` the two roots lie on
opposite sides of `u₀` (case (iv) of Lemma P); the one with `u₁ > u₀` has `s + Bu₁ < 0` and `−1 < u₀ < u₁`,
hence Lemma P's path V passes through it and `d_P(M) ≥ P(S₁)`. Along the window branch the
height of the root is [CUB] (C9), `P/k = −(u + 1/2)[1 + (2s/B)(u − 1/2)]`, whose derivative is
`−k(B + 4su)/B`; for `B < 0` this is positive by [CUB]'s `B + 4su > 0` on (C11). So the root with the larger
`u` is the higher saddle, and `d_P(M)` equals its value; for `D = 0` both saddles have the height `A(u₀)`, which
is then the death level. ∎

Together: **on the limiting local landscape, off the null tie set `{s ≤ B, D² = T}`, `(M,S)` is the elder
pair iff `n(θ) = 0`; otherwise `d_P(M)` is the highest extra window critical value, and off `{D = 0}` `M` dies
at the unique highest extra window saddle.** The exploration in `exploration/` (standard library only; not a
proof, not run in CI) computes the death level of `M` by the discretised elder rule on a grid — cells merged in
decreasing order of `P_θ`, death when `M`'s component first meets a point with `P_θ > 0` — for sampled jets,
and compares it with the closed-form critical points: see `exploration/RESULTS_EXPLORATION.json` (seed 7,
spacing `0.02`, `k ∈ {1, 1/2}`): for all 120 sampled jets with `n ≥ 1` (80 with `n = 1`, 40 with `n = 2`) the
grid death level agrees with the highest window critical value to within `1.5·10⁻³` and the merge cell lies at
that saddle; for all 40 sampled typed jets with `n = 0` the death level is `−k` to within `10⁻⁴`, with the merge
cell at `S` in 39 cases and, in one case with `s + B/2 ≈ −0.024` (a jet close to the typed boundary, where the
saddle at `S` is nearly degenerate in `Z`), displaced `0.18` along the flat valley of `S` at the correct level;
the [ELDER] witness dies at `−7/32`, a tie of its two saddles.

## 4. Theorem LP: the identified lower bound for the selection loss

Let `a₁, a₂` be the local coefficients of [SC] (20): `a_j = ∫ 1{n(θ) = j} dM(θ)`, with `M` the rescaled
typed-jet measure (17) (finite on `{n ≥ 1}` by (19)), so that `ν₁ = a₁ + β_far`, `ν₂ = a₂`.

**Lemma 4.1 (pathwise normal form on the soft plane).** In the frame (axis, soft eigenvector `e_soft(O)`,
hard eigenvectors) of [SC] (7), with `s` the soft eigenvalue of the midpoint transverse Hessian divided by
`r`, `a = τ_xxz`, `β = τ_xzz`, `c = τ_zzz`, and `K ≥ 1` a bound for `‖f‖_{C⁴}`: for every `R ≥ 1` and
`|(X, Z)| ≤ R`,

    f(rX, rZ, 0) − b = r³ [ P_θ(X, Z) + ρ_r(X, Z) ],     sup_{B(R)} |ρ_r| ≤ C_R K r,                 (4.0)

with `C_R` depending only on `R` (and `d`); the same holds for the first two derivatives of `ρ_r` in `(X, Z)`.

*Proof.* Write `g(x, z) = f(x, z, 0)` and expand `g` at the midpoint to third order with the Lagrange
remainder `|R₄| ≤ C K (|x| + |z|)⁴`. The six pin data — values `b`, `b − kr³` and vanishing `x`- and
`z`-derivatives at `(±r/2, 0)` — determine the coefficients: the axial cubic `g(x, 0)` is the Hermite
interpolant of `(b, 0)` and `(b − kr³, 0)` at `±r/2` up to `O(K r⁴)`, which in the scaled variable is
`r³(2kX³ − 3kX/2 − k/2)`; the two conditions `∂_z g(±r/2, 0) = 0` give `g_z(0) = −g_xxz r²/8 + O(K r³)` and
`g_xz(0) = O(K r²)`; and `g_zz(0) = rs`, `g_xxz = a`, `g_xzz = β`, `g_zzz = c` by the definition of the spectral
coordinates. Collecting the `z`-dependent terms in `x = rX`, `z = rZ`:
`g_z z + g_xz xz + g_zz z²/2 + g_xxz x²z/2 + g_xzz xz²/2 + g_zzz z³/6 = r³[(a/2)(X² − 1/4)Z + (s/2)Z² + (β/2)XZ²
+ (c/6)Z³] + O(K r⁴ R⁴)`, which with the axial cubic is `r³ P_θ(X, Z)` up to `O(K r⁴ R⁴)`. Differentiating
the same expansion gives the `C²` statement. ∎

This is the quantitative form of [SC] §5's `C²` convergence `[f(rX, rZ, 0) − b]/r³ → P_θ`; in `d = 2` it is
[ELDER] (E7) / [CUB] (G8). It uses no hard implicit function: the path of Lemma P lies in the soft plane.
(4.0) is stated in the unsheared coordinates `(X, Z)` of the frame; the vertical legs of the paths of Lemma P
are the lines `X = u₁ − aZ/(12k)` there, and "lies in `B(R)`" below is read in `(X, Z)`.

**Lemma 4.2 (compact typed jets).** Let `K ⊂ {typed jets}` be compact in the spectral coordinates
`(s, h, O, τ)` with `h₂ ≥ δ > 0`. Then `r⁻³ Q_r^W(θ_r ∈ K) → M(K)` as `r → 0`. The same proof gives the
statement for bounded Borel `K` on which `M` charges no boundary.

*Proof.* In the spectral coordinates the rescaled law `r⁻³ Q_r^W(θ_r ∈ dθ)` has density
`(c_m r²/Z_r) h_r(A, T) J_r 1{h₂ > −rs} E[W_r/r⁴ | jet]` ([SC] (7)–(9) and the disintegration below (16); the
finite-`r` type indicator is part of `W_r`). On `K`: `h_r → h₀` pointwise ([SC] §2), `J_r → J_0 = ∏h_j ∏(h_j −
h_i)`, `1{h₂ > −rs} → 1`, `Z_r/r² → z₀` ([SC] §1), and `E[W_r/r⁴ | jet] → ∏h_j² w(s, a, β)` ([SC] §5: the soft
`2×2` blocks of the endpoint Hessians divided by `r` converge to `M_M, M_S`, whose determinants multiply to
`9k²(4s² − B²)` on the typed domain, the hard block to `−diag(h)`, and the mixed soft–hard entries are `O(r)`,
so the determinants and the type indicator converge off the null typed boundary). Domination on `K` by [SC]
(10), (15) and (6) with the bounded prefactor `c_m r²/Z_r`; the exceptional branch of (14) plays no role
because `s` is bounded on `K`. Dominated convergence gives the claim. ∎

In `d = 2` this is [CUB] Theorem G summed over the count, which is not consumed here. [SC] displays only the
nonempty-count version (18) and stresses that there is no finite uncentered `n = 0` formula; Lemma 4.2 is
about compact jet sets, on which the total mass is finite whatever the count.

**Theorem LP.** Conditional on [SC] §§1, 2, 4 (15), 5 and (17)–(20) at their stated fixed-`d, L, b, k`, frame
scope, on [P] §4 (4.1), §5 (5.5), §8 and the maximin characterisation (E1), and on [CUB] Theorem C,

    liminf_{r→0} r⁻³ (1 − p_r) ≥ a₁ + a₂ = ν₁ + ν₂ − β_far.                                (4.1)

Combined with [P] Theorem A, `1 − p_r = Θ(r³)` with `a₁ + a₂ ≤ liminf r⁻³(1 − p_r) ≤ limsup r⁻³(1 − p_r) ≤ C`.

*Proof.* Fix `δ > 0` and `R ≥ 4`. Let `K_{δ,R}` be the set of jets `θ` with `s ≤ −|B|/2 − δ` (typed with
margin), `n(θ) ≥ 1`, `|D| ≥ δ`, `h₂ ≥ δ`, `|s| + |h| + |τ| ≤ 1/δ`, whose path V at `S_V` has margin `m(θ) ≥ δ`
and, truncated at the first point where `P ≥ δ`, lies in `B(R)` in the `(X, Z)` coordinates. It is compact in
the spectral coordinates: it is bounded, and it is closed because along a convergent sequence in it the
roots `S_V` converge (Lemma P: `m` is continuous) to a point with `P ≥ −k + δ`, `Z ≠ 0` (`|D| ≥ δ` and
`s + Bu < 0`) and `u ∈ (−1, 1/2)`, which is again an extra strict-window root of the limit jet, and the
other conditions are closed. It is invariant under the reflection `e_soft → −e_soft` (`n` and `m` are). As
`δ → 0` and `R → ∞`, `K_{δ,R}` increases to `{n ≥ 1}` minus an `M`-null set (`M` is absolutely continuous in
`(s, h, τ)`; the excluded sets are `{D = 0}`, the typed boundary, and the set where the margin vanishes,
which lies on the window boundary), so `M(K_{δ,R}) → a₁ + a₂` by monotone convergence and (19)–(20).

Transfer. On the event `E_r := {θ_r ∈ K_{δ,R}} ∩ {C_R K r < δ/2}`, Lemma 4.1 shows that the truncated path
`γ_θ`, scaled by `r` and placed in the soft plane of the actual frame, is a path in the torus from `M` along
which `f > b − k r³ + (δ/2) r³ > f(S)` and whose endpoint has `f > b + (δ/2) r³ > b`. By (E1),
`d_f(M) > f(S)`, so `S` is not the elder death partner: `E_r ⊂ {rejected}`.

Measure. By Lemma 4.2, `r⁻³ Q_r^W(θ_r ∈ K_{δ,R}) → M(K_{δ,R})`. For the complementary event, [SC] §1 (from
[P] (5.3)) gives `W_r/r² ≤ C K^{2d}` and [P] §5 gives `Z_r ≥ z_* r²`, so `E_{Q_r^W}[K^p] ≤ (C/z_*) E_{Q_r}[K^{2d+p}]`
is bounded uniformly in `r` for every `p` (Gaussian moments of the `C⁴` norm under the regression law, [P]
§4); Markov then gives `Q_r^W(C_R K r ≥ δ/2) ≤ E_{Q_r^W}[K^p] (2 C_R r/δ)^p = O_p(r^p)`. Hence

    liminf r⁻³ (1 − p_r) ≥ liminf r⁻³ Q_r^W(E_r) = M(K_{δ,R}),

and `δ → 0`, `R → ∞` give (4.1). ∎

Remarks. (a) The proof uses no window critical point of the field, no gradient trajectory, no near
count: only field values along an explicit path in the soft plane. It is the [ELDER] §2 mechanism run over
the whole `n ≥ 1` domain instead of one witness, with [SC]'s typed-jet measure replacing the one-point
positivity argument of [ELDER] §3. (b) In `d = 2` the soft plane is the whole space. (c) `a₁ + a₂ > 0` by [SC]
(20), so Theorem LP re-derives, conditionally on [SC], the existential lower bounds of [ELDER] / [EDL] / [E_d]
at fixed parameters, with a constant. It does not re-derive their uniformity on compact mark sets, which they
have and this statement does not claim.

## 5. Conjecture LP= and its one obligation

**Conjecture LP=.** `1 − p_r = (a₁ + a₂) r³ + o(r³)`. Equivalently: remote and mixed witnesses never change
the elder partner at leading order, and the entire selection loss is the local nonempty cluster mass.

By Theorem LP it suffices to show `limsup r⁻³ (1 − p_r) ≤ a₁ + a₂`. Write, for fixed `R`,

    Q_r^W(rejected) ≤ Q_r^W(N_R ≥ 1) + Q_r^W(rejected, N_R = 0),

where `N_R` counts strict-window critical points of `f` in `B(Rr)` other than the pins. The first term is
`(a₁^R + a₂^R) r³ + o(r³)` by [SC] (18) and `a₁^R + a₂^R → a₁ + a₂` as `R → ∞` by (20). The obligation is

    (O1)   limsup_{r→0} r⁻³ Q_r^W(rejected, N_R = 0) → 0   as R → ∞.

What is known toward (O1), and what is not (amended in v1.2). The v1.1 sketch here confined the
`M`-component of the rescaled field at the single level `−k + δ/2`. It did not control the levels between
`f(S)` and `f(S) + (δ/2)r³`, where a remote saddle can still kill `M` on `{N_R = 0}`. Codex's Slice C review
(C85, 5396856086, finding C-01) gives an exact falsifier of that finite-radius implication.
- *The construction.* Take `k = δ = 1` and `P = A(X + HZ) − σZ²/2`, with `H = 10⁹`, `σ = 10¹⁴` and `R = 125`.
- *Why the v1.1 margins hold.* The cubic is typed with `n = 0`, its component at `−3/4` lies in `B(124)`, and
  `N_R = 0`. A bump placed outside `B(125)` leaves the actual `C²` error on `B(R)` equal to zero.
- *Why acceptance fails.* The sheared vertical path from `M` stays above `−7/8` and leaves `B(125)`. A bump
  there, outside `B(125)`, makes the pair rejected.

The v1.1 sketch is therefore withdrawn as a proof. What (O1) needs is a *common-radius acceptance lemma*:
one that controls the component through the exact saddle level and slightly below it. For the planar cubic,
QS-E supplies it.

Notation for the lemma.
- *Coordinates.* Work in [CUB]'s sheared coordinates `(u, Z)`, normalized by `k`, so that `P_θ/k` has the
  pins `0` and `−1`. These are the coordinates of main#229 5961415030, where `u = X + aZ/(12k)`.
- *The saddle margin.* `μ(θ) := 1 + max{P_θ(Y)/k : Y an extra nondegenerate saddle}`, and `μ = −∞` if there is
  none. Every extra critical point lies below `0`, so `n(θ) = 0` iff `μ ≤ 0`. Off the tie set `Σ`, `n = 0`
  forces `μ < 0`.
- *The QS sets* (QS §§1–4):
  - the tolerances `m_S` and `ε_M`;
  - the ellipses `E_S` and `E_M`;
  - the cut trap `T_ℓ`: the `M`-component of `{P > ℓ}` cut along the stable curve of `S`;
  - the axis segment `A = [M, (3/2, 0)]`.

**Lemma 5.1 (common-radius acceptance; QS-E).** Let `θ` be typed, off `Δ ∪ Σ`, with `n(θ) = 0`. Let
`0 < η < min(|μ|, m_S, ε_M)`, and let `V_η(θ) := T̄_{−1−η} ∪ A ∪ E_S ∪ E_M`, taken in raw coordinates.
Suppose `V_η(θ) ⊂ B(R)`. Let `F` be a planar function with the exact pins of `P_θ/k` such that:
- `|F − P_θ/k| < η` on `T̄_{−1−η} ∪ A`;
- QS's rescaled `C²` bounds (E2) and (E3) hold on `E_S` and `E_M`.

Then `d_F(M) = F(S)` (elder), whatever `F` is outside `B(R)`.

Both of QS-E's bounds use only paths inside `V_η ⊂ B(R)`:
- the exit from the trap, for the upper bound;
- the axis `A`, for the lower bound.

So the lemma applies to the torus field through the chart, exactly as in #170 §5.

This is Theorem QS-E of main#229 5961415030, an author-side candidate whose nonauthor review is requested;
this packet consumes it at that status. QS Remark 4 shows why the axis beyond `S` must be in `V_η`. The
lemma needs no `N_R = 0`. In the C-01 cubic, along the sheared vertical path, the level-`(−1 − η)` component
reaches `|X| ≈ H(2/σ)^{1/2} ≈ 142`, beyond `B(125)`. So the containment hypothesis fails there, as it must.
The exact C-01 cubic, with `B = D = 0`, also lies on `Δ`.

The margin sets. Put

    𝓜(η, R) := {θ typed : n(θ) = 0, θ ∉ Δ ∪ Σ, η < min(|μ|, m_S, ε_M), V_η(θ) ⊂ B(R − 1)}.

These sets are jet-scaled, and they increase to `{n = 0} \ (Δ ∪ Σ)` as `η ↓ 0` and `R ↑ ∞`: QS Lemma 4
makes the trap bounded at each such `θ`, although its size is not explicit. Two bounds hold on
`𝓜(η, R)`:
- `E_S ⊂ B(R − 1)` gives `κ_S ≥ r̃²/(R − 1)²`, and `η < m_S = (2/5)r̃²` then gives
  `1/κ_S < 2(R − 1)²/(5η)`.
- In the same way, `1/κ_M < (R − 1)²/(2η)`.

So the raw-coordinate thresholds of (E2) and (E3) are at least `c(η, R)/(1 + |a|/(12k))²`.

The decomposition in `d = 2`. Lemma 4.1's planar `C²` error on the fixed ball `B(R)` is `O(C_R K r)`, so

    {rejected, N_R = 0} ⊂ {rejected, n(θ_r) = 0, θ_r ∉ 𝓜(η, R)} ∪ {θ_r ∈ 𝓜(η, R), error on B(R) above θ_r's thresholds}
                          ∪ {n(θ_r) ≥ 1, N_R = 0} ∪ {θ_r ∈ Δ ∪ Σ},

where untyped `θ_r` are placed in the first set.
- *The second set* is `O(r^p)`, as in Theorem LP, by the Gaussian moments of `a` and of `K`.
- *The third set* has `r⁻³`-limit `M(n ≥ 1, n_R = 0)` at fixed `R`, since its jets have all their extra roots
  outside `B(R)`. This follows from three facts:
  - Lemma 4.2, on compact subsets;
  - [SC] §5's joint spectral-jet/count convergence in total variation;
  - the tightness of `M` on `{n ≥ 1}` ([SC] (19): `|s| ≤ 2|B| + (48kD²)^{1/3}` there, with (10)/(15)/(6)
    domination).

  This limit tends to `0` as `R → ∞`.
- *The last set* is null.

Three conditions apply to these statements.
- Do not condition the Gaussian regression on `{N_R = 0}`; that would destroy its Gaussian structure. Keep
  every intersection indicator under the original law `Q_r^W`, with positive majorants.
- In `d ≥ 3` the same conclusion needs the hard-direction slaving of the superlevel components:
  - fiberwise concavity in the hard coordinates `w`;
  - `f_ww ≤ −h₂/2` on the cylinder;
  - the correspondence between the components of `{f > h}` and those of the reduced planar potential
    `max_w f`.

  [SC] §5 carries this out for the critical points; this note does not carry it out for the superlevel sets.
- (O1) ⇒ (O1′) holds already. At fixed regular `R`, [SC] §5's nonempty joint convergence gives
  `r⁻³Q_r^W(n(θ_r) = 0, N_R ≥ 1) → 0`. The converse direction is the decomposition above. So, granting
  Lemma 5.1 (and, in `d ≥ 3`, the slaving step), (O1) is equivalent to

    (O1′)   limsup_{r→0} r⁻³ Q_r^W(rejected, n(θ_r) = 0, θ_r ∉ 𝓜(η, R)) → 0   as η ↓ 0 and R ↑ ∞.

At fixed planar marks, this equality is supplied on main by Math-#170 Theorem S (OpenAI; reviewed at head `79f18f0`,
proof blob `ef2aa57959ea9f721bbf2316ce94cf616c1c9113`), whose route avoids the margin set altogether: the failure event
is contained in the bad cap of [P] §8 (`F_r ⊂ G_r^c`), the bad cap's mass restricted to a large residual norm
is `o(r³)` by keeping the indicator inside [P]'s (7.5) scalar integral, and the remaining compact-jet part
converges by dominated convergence with the pointwise limit of the failure indicator (its Theorem E). The
`d ≥ 3` slaving step named above is Math-#175's H1. Read on its own, the margin set must be jet-scaled (a fixed `δ` fails: near
`M`, `P(M + Z e_Z) = (Z²/2)(s − B/2) + (D/3)Z³` exceeds any fixed `−δ` for `|Z|` slightly beyond `δ` once
`|s|` is large, so a fixed-margin set would exclude a region of infinite `M`-mass and (O1′) would restate
(O1)); the typed-jet measure is not finite on `{n = 0}` ([SC] after (17)), so its complement cannot be
handled by Lemma 4.2; and the events in the complement — a second soft eigenvalue, a large jet, a jet near
the typed boundary, a landscape whose `M`-component reaches far — are the ones [P] §§6–7 and [SC] §4 control
in unweighted or occurrence-weighted form, not in rejection-weighted form. C85's review records the
normalization:
- [P] §§6–7 keep the double soft factor `W_r ≲ r²λ₁(λ₁ + CrU)`. So the soft interval gives an `O(r⁵)` weighted
  numerator, and one division by `Z_r ≥ z_*r²` gives `O(r³)`.
- Exhausting the margins needs more than that displayed bound: a written rejection-tail deduction that keeps
  the residual and hard-spectrum tail indicators inside the same integral.
- [SC] §4's domination covers only the nonempty near-occurrence measure.

What is needed is either a direct
argument that a long excursion of `M`'s window component without a window saddle inside `B(Rr)` has
weighted probability `o(r³)`, or the boundary-layer estimates of [P] §7 restated at `o(r³)` on the no-witness
event. That, together with the `d ≥ 3` slaving step, is what separates Theorem LP from LP=.

Falsifiers. LP= is false if there is a configuration class of weighted probability `≍ r³` in which
`(M,S)` is rejected although no strict-window critical point lies within `O(r)` of the pair — for example
a mechanism where the far sector of `S` reconnects to `M`'s component (self-attachment) through a region
at distance `≫ r`. Lemma P′ and Lemma 5.1 show that no such class exists on the accurate planar cubic model with margins.
The margins must control the component down to the exact saddle level; C-01 shows that confinement at
one level above `f(S)` is not enough. A counterexample would have to live where the model is inaccurate
or unmargined, or where the hard-direction reduction fails.

## 6. Consequences for the lifetime law, stated without inflation

1. **Leading law.** Theorem 2.1 of the manuscript and [P] Theorems B, C need `1 − p_r = O(r³)` only; nothing
   here changes the leading term `c ℓ^{−1/3}`.
2. **Compact-window selection loss, `d = 2`.** With [ELDER] (E9)–(E10) (compact `B`, `K`, `r_*`; `r³ = ℓ/k`),
   Fatou's lemma and Theorem LP at every fixed `(b, k, u)` give

       liminf_{ℓ↓0} ℓ^{−2/3} [ν_cand(ℓ) − ν_eld(ℓ)] ≥ (1/3) ∫_B ∫_K ∫_{S¹} k^{−5/3} A₀(b,k,u) (a₁ + a₂)(b,k,u) dσ dk db,   (6.1)

   using `A_r → A₀` uniformly on the compact parameters ([ELDER] (E9)). Under LP= the limit
   `lim ℓ^{−2/3}[ν_cand − ν_eld]` exists and (6.1) is an equality, by dominated convergence with the uniform
   constant of [P] Theorem A; (E11)'s existential two-sided bound would then carry an explicit limit. Without
   LP=, (6.1) is a lower bound with an identified functional. The every-`d` version follows the same way from
   [E_d]'s ledger once its (E9) analogue is cited.
3. **Ranking.** The loss (6.1) is `Θ(ℓ^{2/3})` ([ELDER] (E11), [P] Theorem B): relative order `ℓ` against the
   leading `ℓ^{−1/3}`. For the unrestricted density the compact-window difference estimate is explicitly not
   asserted ([P] Theorem C), and the rejected density there is bounded with a positive limit (`ρ_rej = O(1)`
   by [C7] Theorem K / Corollary T, `ρ_rej → B_{d,L} > 0` by [C7] Theorem Z), so the selection coefficient
   bounded here is a compact-window statement; neither [P] §11 nor [C7] claims a second-order expansion of
   either density separately, and none is claimed here. What this packet adds is the structure on the local
   landscape — which points pair — and a lower bound for its weight; locality of the decision for the field
   is Conjecture LP=.
4. **Not claimed.** No numerical value of `a₁ + a₂` (uncertified floating-point values of the planar near
   coefficients exist in [NUM], Math-#168, under its own conditions; this packet neither consumes nor confirms
   them); no rate; no uniformity in marks or `d`; no statement about the joint law of several bars; no change
   to the C6 / C7 / witness-collision registers.

## 7. Finite controls

`pairing_check.py` (standard library, exact rationals): I0–I3 — the shear (2.1) against [CUB] (C1)–(C3),
the conic identity, an exact central-difference check of `∂_Z P`, and `A(u) + k` — on rational points; P1 the
Lemma-P path inequalities on 6840 chart points under the assignment of §3 (path V at the chart root when
`s + Bu₁ < 0`; otherwise — case (iv) with the chart root on the side `u < u₀` — path U at `u₀` is verified
and, in addition, the partner root `S_V` is computed exactly by Vieta on [CUB] (C13), checked to be a
strict-window root with `u > u₀` and the higher of the two, and path V is verified there), with the minimal
margin reported; P2 the [ELDER] witness; N1 a typed `n = 0` grid on which the U hypothesis
`B < 0 < s − B` never holds (consistency of (C6) with case (iv)).
Deterministic JSON, byte-identical in `-O`; mutants `M1` (typed condition broken), `M2` (root pushed below
the window), `M3` (wrong conic identity), `M4` (margin sign) exit 1; unknown label exits 2.
`exploration/elder_grid.py` (standard library only; **not** run in CI, **not** a proof) and
`exploration/RESULTS_EXPLORATION.json` record the grid elder-rule computation of §3 (closed-form critical
points, discretised maximin by union-find, boundary treated by the ray criterion of Lemma 2.1(b); its
numerical limits are stated in the script header). None of this certifies the Gaussian steps of §4–§5.

## 8. Non-claims

No register, STATUS, GRAPH, PROOF_INDEX or catalog edit; no `lemma_closed`, prize or premise change; no
acceptance of [SC], [CUB], [TSL] or [P] beyond their own records; no numerical constant; no uniformity as
`k ↓ 0`, in `L`, or in `d`; no rate for the `o(r³)`; no claim about the finite-`r` spatial law of the
witnesses; no `d ≥ 3` hard-direction statement beyond what [SC] §5 supplies for the soft plane.

## 9. Review division

* **Slice A (deterministic, `d`-free):** §2, Lemma P and Lemma P′, and the exact controls. Any lane.
* **Slice B (Gaussian transfer):** §4 Theorem LP — the coupling identity, the compact-jet convergence read
  from [SC] §5, and the `O(r^p)` tail. Best read by a lane not exposed to [SC]'s authorship.
* **Slice C (the obligation):** §5 — whether (O1) follows from [P] §§6–7 and [SC] §4 as stated, or needs
  a new estimate. This is the lane where the next theorem is decided.
  Reviewed by Codex (C85, 5396856086): the remaining weighted obligation and the cap bypass are sound at
  their conditional scope. Finding C-01 is applied in v1.2: the v1.1 sketch is withdrawn, Lemma 5.1 is consumed
  from QS-E, and the reverse reduction is marked conditional.
