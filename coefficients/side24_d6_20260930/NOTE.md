# SIDE24 in `d = 6`: the cone moment `D_5` certified through two exact layers and one certified cumulative layer

**Object** `CL-SIDE24-D6-COEFFICIENT-20260930-v1` · **scientific effect NONE** · declarative record, `executed: false` ·
base `main 3e0a91b` · claim: Math-#200 comment 5919618330 · companions: Math-#200 (`d = 5`; the `(T, u)` decoupling and the
certified cumulative machinery), Math-#201 and Math-#202 (the exact arithmetic, the incomplete Gaussian moments, the closed
forms of `D_3`, `D_4` used as regressions). `coefficients/side24_v1` is unchanged; catalog entry C8 stays OPEN; no register,
GRAPH, STATUS or catalog surface is touched. Same GitHub account as every lane: zero organizational-independence credit.
Claude reads of this record count for nothing. The author will not merge.

## 0. Statement

For SIDE24's reference law in `d = 6` (`A = Q + √(2/3) Z I_5`), the cone moment `D_5 = E[det(A)² 1{A ≺ 0}]` of [LP] (15.1)
and the coefficient of [LP] (15.2) satisfy

```
D_5 = 44.130651875074132710362024895402633148……            (enclosure width 3.9e-37),
c_{6,ref} = Γ(7/6) (3/2)^{1/3} D_5 / (64√3 π^{7/2}) = 0.0076928786292368482786666312812273900811……   (width 6.9e-41),
|c_{6,24}/c_{6,ref} − 1| ≤ δ = 1.8004e-106.
```

The same code returns exactly `D_1 = 4/3`, `D_2 = 29/6 − √6`, Math-#201's `D_3` and Math-#202's `D_4` (rules `D1_EXACT` to
`D4_EXACT`), re-encloses `D_4` through the certified layer (rule `D4_CERTIFIED_PATH`), encloses Mehta's `Z_5 = 46080 π^{3/2}`
through the identical `m = 5` layers (rule `MEHTA_Z5`), and reproduces SIDE24's `d = 2, 3` intervals and Math-#200's `D_4` and
`c_{5,ref}` enclosures (rule `SIDE24_CONSISTENT`). **No closed form for `D_5` is claimed** (§7).

With SIDE24 (`d = 2, 3`), Math-#199/#201 (`d = 4`), Math-#200/#202 (`d = 5`) and this record, the reference coefficients are:

| `d` | `D_{d−1}` | `c_{d,ref}` |
|---|---|---|
| 2 | `4/3` | `0.0734069193060342710301359629577…` |
| 3 | `29/6 − √6` | `0.0417759318405983433429366654285…` |
| 4 | `(50π + 200 arctan 2 − 228)/(9π)` | `0.0233216660029528350945211949528…` |
| 5 | `6695/54 − (405/32)√6 − (1/π)[(1375/72)√21 + (6695/27) arctan√(3/7) + (405/16)√6 arctan(1/√14)]` | `0.0132193193800849680760334875146…` |
| 6 | `44.130651875074132710362024895402633148…` (enclosed) | `0.0076928786292368482786666312812273900811…` |

## 1. The reduction at `m = 5`

Math-#200 §1: with `t_j = p_1 + … + p_j` (`p_i` the gaps of the ordered sector `μ_5 = −a, μ_4 = −a − p_1, …`),
`T = Σ t_j = 4p_1 + 3p_2 + 2p_3 + p_4` and `u = t − (T/(m−1))·1`, the exact `a`-integral (`α = 3m/(4(m+3)) = 15/32`,
`β = 3T/(2(m+3)) = 3T/16`) leaves an erfc branch with `exp(−T²/(4m(m−1)) − |u|²/4) = exp(−T²/80 − |u|²/4)` and
`erfc(κT)`, `κ² = 3/(4m(m+3)) = 3/160` (`κ = √30/40`), and a polynomial branch with `exp(−T²/((m−1)(m+3)) − |u|²/4) =
exp(−T²/32 − |u|²/4)`. In the nested coordinates

```
T = 4p_1 + 3p_2 + 2p_3 + p_4,   w = 3p_2 + 2p_3 + p_4,   v = 2p_3 + p_4,   q = p_4       (dp = dT dw dv dq / 24,  0 < q < v < w < T)
```

the form `|u|²/4` is diagonal: `|u|²/4 = w²/48 + v²/24 + q²/8` (the script substitutes and checks `set(exponent) = {T², w², v², q²}`
with these coefficients on both branches and `β ∝ T`; rule `STRUCTURE`). The denominators `8, 24, 48, 80 = 8·{1, 3, 6, 10}` are
eight times the triangular numbers, and `1/80 + κ² = 1/32` (the erfc branch times `e^{−κ²T²}` decays like the polynomial branch).
The sector polynomial after the `a`-integral has 1682 monomials (erfc branch) and 1369 (polynomial branch) in `(T, w, v, q)`,
`T`-powers `0–12, 14` and `0–11, 13`, `w`-degree `15`, `v`-degree `14`, and **only odd `q`-powers `1, 3, …, 11`** (rule `STRUCTURE`).
So `D_5 = pref [ c_E ∫_0^∞ e^{−T²/80} erfc(κT) Σ_a T^a Λ_a^E(T) dT + ∫_0^∞ e^{−T²/32} Σ_a T^a Λ_a^R(T) dT ]` with

```
pref = √(3/8) · 5! · (1/24) / Z_5 = √6/(36864 π^{3/2})   (Z_5 = 46080 π^{3/2}),      c_E = ½√(π/α) = (2/15)√30 √π,
Λ_a(T) = ∫_0^T e^{−w²/48} Σ_b w^b L_{a,b}(w) dw,    L_{a,b}(w) = ∫_0^w e^{−v²/24} Σ_j v^j Σ_k e_{a,b,j,k} J_k(v) dv,    J_k(v) = ∫_0^v q^k e^{−q²/8} dq.
```

## 2. The two exact layers

**`q`-layer.** For odd `k`, `J_k = B_k + C_k(v) e^{−v²/8}` with rational `B_k` and polynomial `C_k` (Math-#201 L1; rule `JK_EXACT`
for `k ≤ 11`), so no error function enters here.

**`v`-layer.** `∫_0^w v^n e^{−μv²} dv = G_n(μ, w)` with `μ ∈ {1/24, 1/6}` (Math-#202 L2: `G_0 = ½√(π/μ) erf(√μ w)`,
`G_1 = (1 − e^{−μw²})/(2μ)`, `G_n = [(n−1)G_{n−2} − w^{n−1}e^{−μw²}]/(2μ)`; rule `LAYER_EXACT` verifies `G_n(μ, 0) = 0` and
`∂_w G_n = w^n e^{−μw²}` exactly for `n ≤ 24` and every `μ` used). Hence each `L_{a,b}(w)` is a polynomial in `w`, plus
polynomials times `e^{−w²/24}` and `e^{−w²/6}`, plus multiples of `erf(w/(2√6))` and `erf(w/√6)`, with coefficients in the exact
arithmetic (`Q`-span of `√r π^{k/2}`; no arctan atoms arise before the outer layer).

**`w`-layer, exact part.** Multiplying by `w^b e^{−w²/48}` and integrating to `T`: the polynomial parts give `G_n(1/48, T)`, the
`e^{−μw²}` parts `G_n(1/48 + μ, T)` (`1/16` and `3/16`), exactly; these are again polynomials, `e^{−T²/16}`, `e^{−3T²/16}` and
`erf(T/4)`, `erf(√3 T/4)` terms. The `erf(√μ w)` parts are not elementary in `T`:

```
Ω_{a,μ}(T) = ∫_0^T Q_{a,μ}(w) e^{−w²/48} erf(√μ w) dw,      μ ∈ {1/24, 1/6},      Q_{a,μ} of degree ≤ 15,
```

28 such functions on the erfc branch (`a = 0–12, 14`, two `μ` each) and 26 on the polynomial branch (rule `STRUCTURE`). These are
Owen-`T`-type functions (Gaussian integrals over a two-dimensional wedge) and are handled by the certified layer of §3.

**Outer layer, exact part.** Every term of `Λ_a^{exact}(T)` against `T^a e^{−gT²} [erfc(κT)]` is a moment with at most two
error functions (`erfc(κT) · erf(√μ'' T)`), elementary by Math-#202 L3–L4; the arctan atoms that arise are `arctan(1/√5)`,
`arctan(1/√15)` and `arctan(√7/3)` (recorded in `RESULTS.json`).

## 3. The certified cumulative layer

Each `Ω_{a,μ}` is carried exactly as Math-#200 carries its `L_a` (its NOTE §§2–3, `enclose_m4`): on cells of width `1/2` on
`[0, 30]` and `1` on `[30, 90]`, with centre `s_0`, the Taylor coefficients of the integrand `g(w) = Q_{a,μ}(w) e^{−w²/48} erf(√μ w)`
at `s_0` up to order `K = 40` are the exact product of the polynomial's, the Gaussian's and `erf`'s coefficients (interval
enclosures; `erf(√μ w)` through `ErfLin` with `√μ` an exact integer-root interval); the certified integral of `g` over each
cell (even moments of the coefficients plus the Cauchy tail `M_g ρ^{−(K+1)} 2(h/2)^{K+2}/(K+2) · 1/(1 − h/(2ρ))`, `ρ = 6`,
`M_g` the product of the factors' disc bounds: `Σ|Q_j|(|s_0|+ρ)^j`, `e^{γρ²}e^{−γ(|s_0|−ρ)₊²}`, `(2√μ/√π)(|s_0|+ρ)e^{μρ²}`) is
accumulated from `0`; at each centre `Ω(s_0)` is the accumulated integral over the full cells before plus the left half of
the current cell (its own Cauchy tail included), and the Taylor coefficients of `Ω` at `s_0` are `Ω(s_0)` and `g_{n−1}/n`. The
disc bound of `Ω` on `|z − s_0| ≤ ρ` is `|Ω(s_0)| + ρ M_g`. The outer integrand `T^a e^{−gT²} [erfc(κT)] Σ_μ Ω_{a,μ}(T)` summed over
`a` is then integrated cell by cell with its own Cauchy remainder (product of the disc bounds), exactly as in Math-#200. The
`Q_{a,μ}` coefficients, exact elements of the arithmetic, enter as 60-digit intervals.

**Tail beyond `T = 90`.** `|Ω_{a,μ}(T)| ≤ Ω̄_{a,μ} = Σ_n |Q_{a,μ,n}| ∫_0^∞ w^n e^{−w²/48} dw` for every `T` (`|erf| ≤ 1`), so the
integrand beyond `90` is bounded by `Σ_a T^a Ω̄_a · e^{−T²/32}` on both branches (`erfc(κT) ≤ e^{−κ²T²}` and `1/80 + κ² = 1/32`),
and the tail by the incomplete-gamma bounds of Math-#199 §3; at `T = 90` the factor `e^{−90²/32}` is below `10⁻¹⁰⁹`, which is
why the cells extend to `90` (at `60` the tail would be `~10⁻²⁴`).

**Assembly.** `D_5 = pref [ c_E (E_exact^E + I_cert^E) + E_exact^R + I_cert^R ]`, the exact parts evaluated as 60-digit intervals
from their exact elements. The two branches carry large cancelling parts (`E_exact^E ≈ −2.0·10⁶`, `I_cert^E ≈ 2.2·10⁶`,
`E_exact^R ≈ 5.3·10⁵`, `I_cert^R ≈ 3.0·10⁶` before the prefactor `1.2·10⁻⁵`), so the width of `D_5` (`3.9·10⁻³⁷`) is set by the
certified parts' absolute widths (`~10⁻³²`) times the prefactor.

**Three end-to-end checks of the certified layer.** (i) `D_4` through it: at `m = 4` the `v`-layer (`∫_0^T e^{−v²/24} Σ_k e_k J_k`)
is elementary, but the script also encloses it as certified cumulative factors (`Q_B(v)e^{−v²/24} + Q_C(v)e^{−v²/6}`, no `erf`)
and the result contains the exact closed form of Math-#202 with width `4·10⁻⁴⁰` (rule `D4_CERTIFIED_PATH`). (ii) `Z_5`: Mehta's
integral at `m = 5`, `Z_5 = 5!·(1/24)·2√(π/5) ∫_{0<q<v<w<T} V e^{−T²/80 − w²/48 − v²/24 − q²/8}` (`V` the Vandermonde of the
gaps; the `a`-integral is the pure Gaussian `∫ e^{−(5a² + 2aT)/4} da = 2√(π/5) e^{T²/20}` and `Σt_j² = T²/4 + |u|²` gives the
`T²/80`), goes through the same `q`, `v`, `w` layers, including `erf` inside the certified layer, and encloses `46080 π^{3/2}` with
width `5.7·10⁻³⁵` (rule `MEHTA_Z5`). (iii) Two routes for `D_5`: the `e^{−μw²}` parts of the `w`-layer are computed exactly (default)
or also routed through the certified layer; the two enclosures intersect (rule `ROUTE_CONSISTENT`). A coarser run (`K = 20`,
cells of width `1`) contains the fine one and is wider (rule `TRUNCATION_NESTING`), and a float trapezoid evaluation of the same
layer decomposition (`h = 0.02`, `T ≤ 70`) lands within `2·10⁻⁵` of the enclosure (rule `FLOAT_INSIDE`, control only).

## 4. The coefficient and the torus transfer in `d = 6`

`c_{d,ref} = Γ(7/6) (3/2)^{1/3} |S^{d−1}| D_{d−1} / (√3 √π (2π)^d)` ([LP] (15.2), Math-#199 §4); `|S⁵| = 2π³/Γ(3) = π³`, so
`c_{6,ref} = Γ(7/6) (3/2)^{1/3} D_5 / (64√3 π^{7/2})` (rule `CLOSED_FORM_D6` against the general formula; `d = 2, 3` inside SIDE24's
intervals, `d = 4, 5` inside Math-#199/#200's, rule `SIDE24_CONSISTENT`).

**Transfer to `K_24`, `d = 6`** (SIDE24 §§2–4 with the `d = 6` constants). (i) Image bound: the shell `|n|_∞ = j` holds
`(2j+1)⁶ − (2j−1)⁶ = 384j⁵ + 320j³ + 24j ≤ 728 j⁵` points with `|n|² ≤ 6j²`, so
`Σ_{n≠0} |n|⁶ e^{−288|n|²} ≤ 728·216 Σ_j j¹¹ e^{−288j²} ≤ 314496 e^{−288}` (successive terms have ratio far below `1/2`), and every
3-jet covariance entry of `K_24` is within `E_6 = 314496 (76·24⁶ + 15) e^{−288} = 3.8272e-110` of its reference value.
(ii) Sandwich: the jet `(G, t, svec H)` has dimension `n = d + 1 + d(d+1)/2 = 28`; spectral norm of the difference at most `2nE_6`;
`C_ref ≥ I/3` in every `d` (SIDE24 §3: Hessian block eigenvalues `d + 2` and `2`, the `(G, tr H)` block `[[1, −3], [−3, 15]]` with
eigenvalues `8 ± √58`, gradient variances `1`); hence `(1 − ε) C_ref ≤ C_24 ≤ (1 + ε) C_ref` with `ε = 168 E_6 = 6.4297e-108`.
(iii) Ratios: `a = m + 2/3 + n_A/2 = 79/6` (`n_A = m(m+1)/2 = 15`), `b = d + n_A/2 = 27/2`; both are at most `14`, so the ratio lies in
`[1/(1+δ), 1+δ]` with `δ = (1+ε)^{14}/(1−ε)^{14} − 1 = 28ε + O(ε²)` (computed without cancellation; rule `TRANSFER_BOUND` certifies
`27ε ≤ δ ≤ 29ε` for every represented value, `δ.lo ≥ 27 ε.hi` and `δ.hi ≤ 29 ε.lo`, and records that the enclosures of `δ` and `28ε`
intersect; the offset `δ − 28ε ~ 406 ε²` lies far below the arithmetic resolution and is not claimed as certified). So
`|c_{6,24}/c_{6,ref} − 1| ≤ 1.8004e-106`, below the arithmetic width; the printed digits of `c_{6,24}` are those of `c_{6,ref}`. The
exact periodic constant is enclosed, not equated to the reference.

## 5. Values (`RESULTS.json`)

| quantity | enclosure (common digits of both endpoints) | width |
|---|---|---|
| `D_1`, `D_2`, `D_3`, `D_4` | exact (`4/3`, `29/6 − √6`, Math-#201, Math-#202) | — |
| `D_4` through the certified layer | `14.218763458977357601306465677874078317340602…` ∋ closed form | `4.1e-40` |
| `Z_5` (layered) | `256588.55409400509751072441261603594914…` ∋ `46080π^{3/2}` | `5.7e-35` |
| `D_5` | `44.130651875074132710362024895402633148…` | `3.9e-37` |
| `D_5`, second route | same digits, intersects | `4.2e-37` |
| `c_{6,ref}` | `0.0076928786292368482786666312812273900811…` | `6.9e-41` |
| `c_{6,24}` | the same digits; `|c_{6,24}/c_{6,ref} − 1| ≤ 1.8004e-106` | |
| `E_6`, `ε`, `δ` | `3.8272e-110`, `6.4297e-108`, `1.8004e-106` | |

Float control (not part of the certificate): the trapezoid evaluation of the same layer decomposition gives `44.12971862`.

## 6. Rules, mutants, verification

`python3 -B -S cone_moment_d6.py` (also `-B -O -S`; about three minutes) prints `RESULTS.json` and exits `0` only if all twenty rules
hold: STRUCTURE, JK_EXACT, LAYER_EXACT, D1_EXACT, D2_EXACT, D3_EXACT, D4_EXACT (with `Z_4 = 1536π` exactly), D4_CERTIFIED_PATH,
MEHTA_Z5, ROUTE_CONSISTENT, TRUNCATION_NESTING, WIDTHS (`D_5` and `c_{6,ref}` below `1e-30`), FLOAT_INSIDE (`5e-3` relative),
SIDE24_CONSISTENT, CLOSED_FORM_D6, MONOTONE (`D_4 < D_5`, `c_{5,ref} > c_{6,ref} > 0`), IMAGE_BOUND (`E_6` in `(3.8e-110, 3.9e-110)`),
TRANSFER_BOUND (§4), LIBRARY_EXACT (the decimal module's `exp`, `sqrt` and the interval negation against exact rational brackets),
PINNED. Mutants (`--mutant`, each must exit `1`, in both interpreter modes): `shift-variance` (`S²/28` for `S²/32` at `m = 5`;
the decoupling check raises), `vandermonde` (factor dropped; even `q`-powers appear and the `q`-layer raises), `erfc-branch`
(`c_E` halved), `jacobian` (`1/6` for `1/24`), `mehta` (`Z_6` for `Z_5` in the prefactor), `recurrence` (`a`-integral recurrence
perturbed), `layer-init` (`G_1` sign), `two-erf` (`λ + u²` for `λ + u² + v²` in the two-erf base integral), `cumulative-half`
(left half-cell dropped from `Ω(s_0)`), `remainder-dropped` (order `10`, cells of width `1`, no Cauchy remainders), `erf-inside`
(`erfc` for `erf` inside the certified layer), `tail-dropped` (cells only to `T = 30`), `image-shells` (`364 j⁵`), `sandwich-exponent`
(`12` for `14`). The hosted workflow replays manifest, pins, both modes byte for byte, the mutants, and checks the SIDE24
intervals quoted in the script against `ENCLOSURE.json`.

## 7. What this does not do

Not a proof or review of [LP] or SIDE24 §§1–4 (consumed at their scope, as in Math-#199/#200). **No closed form for `D_5`:** the
`w`-layer's `erf` parts are Owen-`T`-type functions, and the outer integral of such a function against `erfc(κT) e^{−gT²} T^a` is
a Gaussian integral over a three-dimensional wedge with two further error functions, a five-dimensional orthant-type integral,
not elementary in general; the pattern `D_1..D_4` elementary, `D_5` not, is the expected one. Not `d ≥ 7`: at `m = 6` a further
nested variable appears (denominator `8·15 = 120`) and the `w`-layer's certified factors would themselves have to be integrated
cumulatively once more before the outer integral; the machinery nests in principle (a cumulative factor of a cumulative factor)
but is not built here. Not a window coefficient, `C`, `r_*` or `z_*`. C8 stays OPEN. `executed: false`.

## 8. Provenance

Pins on `main 3e0a91b` ([LP] `dfed3b8d`, SIDE24 `PROOF.md` `44b66f04`, `ENCLOSURE.json` `57af39a0`) verified by the workflow.
Companions, not on `main`: Math-#200 at `33d50de` (`RESULTS.json` blob `b67c00f4`: the `D_4`, `c_{5,ref}` enclosures quoted; `NOTE.md`
blob `ab3fe17d`: the decoupling and the cumulative machinery), Math-#201 at `3abcc10` (`closed_form_d3.py` blob `a0c91692`: the exact
arithmetic and the moments), Math-#202 at `4512309` (`closed_form_d4.py`: the T-function layer and the `m = 4` pipelines, reused
verbatim; the closed form of `D_4`). Mehta's `Z_m` (Mehta, *Random Matrices*, ch. 17) at `m ≤ 5`: `m ≤ 3` inside Math-#199, `m = 4`
inside Math-#200/#202, `m = 5` inside this record (rule MEHTA_Z5). Cauchy's estimate and the Lagrange remainder are elementary.
The interval class is the repaired class of Math-#190 v1.3 (exact negation, explicit contexts, rule LIBRARY_EXACT). No external
numerical library is used.

## 9. Current disposition

- **Head / owner:** see the PR's disposition block; branch `claude/side24-d6-coefficient-20260930` (base `main 3e0a91b`); author
  lane Anthropic / Claude (`session_017Mi3hxjaxV45x6zo6o1ee3`).
- **Claim:** the `m = 5` recursion of the decoupling; the layered exact/certified evaluation; the certified enclosures of `D_5`,
  `c_{6,ref}`, `c_{6,24}`; `Z_5 = 46080π^{3/2}`, `D_4` through the certified layer and the exact `D_1..D_4` as rules. No theorem of
  [LP] or SIDE24 is proved or reviewed.
- **Completed review scopes:** none yet. Requested: nonauthor reads of Slice A (§1: nested coordinates, Jacobian, exponents, odd
  `q`-powers, `pref`, `c_E`), Slice B (§§2–3: the exact layers, the certified `Ω` factors and their disc bounds, the tail at `T = 90`,
  the three end-to-end checks), Slice C (§§4–7: coefficient, the `d = 6` transfer constants, values, non-claims).
- **Unresolved finding IDs:** none.
- **Validation:** 20/20 rules in both modes, byte-identical output; 14/14 mutants rejected in both modes; workflow replayed locally;
  hosted run pending at opening.
- **Next action:** nonauthor reads; amendments on this branch, recorded in `SOURCE_FILES.json`. Author will not merge.
