# The SIDE24 cone moment `D_4` in closed form (`d = 5`)

**Object** `CL-SIDE24-D4-CLOSED-FORM-20260930-v1` · **scientific effect NONE** · declarative record, `executed: false` ·
base `main 3e0a91b` · claim: Math-#200 comment 5918942608 · companions: Math-#200 (`coefficients/side24_d5_20260930`, head
`33d50de`), whose reduction is the input and whose certified enclosure is the independent check, and Math-#201
(`coefficients/side24_d4_closed_form_20260930`), whose exact arithmetic and lemmas are extended here by one cumulative layer.
`coefficients/side24_v1` is unchanged; catalog entry C8 stays OPEN; no register, GRAPH, STATUS or catalog surface is touched.
Same GitHub account as every lane: zero organizational-independence credit. Claude reads of this record count for nothing.
The author will not merge.

## 0. Statement

**Proposition (closed form of `D_4`).** For SIDE24's reference law in `d = 5` (`A = Q + √(2/3) Z I_4`, `Q` the `4×4` GOE of
density `∝ exp(−tr Q²/4)`, `Z` an independent standard normal), the cone moment `D_4 = E[det(A)² 1{A ≺ 0}]` of [LP] (15.1) is

```
D_4 = 6695/54 − (405/32)√6 − (1/π) [ (1375/72)√21 + (6695/27) arctan√(3/7) + (405/16)√6 arctan(1/√14) ]
    = 14.21876345897735760130646567787407831734060231608202158418…
```

(`arctan√(3/7) = arctan(√21/7)`, `arctan(1/√14) = arctan(√14/14)`). The exact arithmetic returns the two last atoms as
`arctan(√14/4)` and `arctan(√14/7)` with coefficients `∓(405/16)√6/π`; they combine by the subtraction formula,
`(√14/4 − √14/7)/(1 + 14/28) = √14/14`, both angles lying in `(0, π/2)` with a positive difference below `π/2` (rule
`SIMPLIFIED_FORM` evaluates both forms in interval arithmetic).

**Corollary (the `d = 5` reference coefficient).** With [LP] (15.2) as written out in Math-#200 §4 (`|S⁴| = 8π²/3`),

```
c_{5,ref} = Γ(7/6) (3/2)^{1/3} D_4 / (12√3 π^{7/2}) = 0.01321931938008496807603348751464139652105289012569990545…
```

and `c_{5,24}` is as in Math-#200: `|c_{5,24}/c_{5,ref} − 1| ≤ 1.8554·10⁻¹⁰⁷`.

With SIDE24 §1 (`D_1 = 4/3`, `D_2 = 29/6 − √6`) and Math-#201 (`D_3 = (50π + 200 arctan 2 − 228)/(9π)`), the reference
coefficients `c_{d,ref}` of [LP] (15.2) are now in closed form for every `d ≤ 5` (§5). `D_5` (`d = 6`) is not claimed (§6).

**What is proved here and from what.** The identity is obtained by exact integration of the integral to which Math-#200
reduces `D_4` (that reduction is exact algebra on the ordered-sector integrand, re-run here by the same code, and checked at
`m = 1, 2, 3` against `4/3`, `29/6 − √6` and Math-#201's `D_3` through the identical path). The computation lives in the
finite-dimensional `Q`-vector space with basis `√r · π^{k/2} · A` (`r` squarefree, `k ∈ Z`, `A = 1` or an arctan atom), so its
output is an identity. Math-#200's certified enclosure of `D_4` (an independent method: order-40 Taylor quadrature with Cauchy
remainders and certified cumulative integrals) contains the interval evaluation of the closed form, which lies at its centre
(`1.94·10⁻⁴²` from either endpoint of a `3.9·10⁻⁴²`-wide enclosure; 43 common digits; rule `D4_INSIDE_CERTIFIED`). Mehta's
`Z_4 = 1536π` is reproduced **exactly** by the same triangle machinery (rule `MEHTA_Z4_EXACT`).

## 1. Input: the reduction of Math-#200 (its NOTE §§1–2)

With `t_j = p_1 + … + p_j`, `T = Σ t_j`, the exact `a`-integral (`α = 3m/(4(m+3)) = 3/7`, `β = 3T/(2(m+3)) = 3T/14`), the
coordinates `p_1 = (T − 2p_2 − p_3)/3`, `v = 2p_2 + p_3` (Jacobian `1/6`, region `0 < p_3 < v < T`), and the decoupled
exponents `T²/48 + v²/24 + p_3²/8` (erfc branch) and `T²/21 + v²/24 + p_3²/8` (polynomial branch), Math-#200 writes

```
D_4 = pref [ c_E ∫_0^∞ e^{−T²/48} erfc(κT) Σ_a T^a L_a^E(T) dT + ∫_0^∞ e^{−T²/21} Σ_a T^a L_a^R(T) dT ],
L_a(T) = ∫_0^T e^{−v²/24} q_a(v) dv,   q_a(v) = Σ_k e_{a,k}(v) J_k(v),   J_k(v) = ∫_0^v p_3^k e^{−p_3²/8} dp_3,
```

`pref = √(3/7)·4!·(1/6)/Z_4 = √21/(2688π)` (`Z_4 = 1536π`), `c_E = ½√(π/α) = √21√π/6`, `κ = β/(2√α)/T = √21/28`
(`κ² = 3/112`; note `1/48 + κ² = 1/21`, the polynomial branch's exponent). The rational polynomials `e_{a,k}(v)` (erfc branch:
122 monomials, `T`-powers `0–9, 11`, `v`-degree `≤ 11`; polynomial branch: 95 monomials, `T`-powers `0–8, 10`) are listed in
`RESULTS.json` (`reduction_data`). In both branches the `p_3`-powers are `k ∈ {1, 3, 5, 7, 9}` — **only odd `k`** (rule
`STRUCTURE`), exactly as in the `d = 4` case of Math-#201. Hence `J_k = B_k + C_k(v) e^{−v²/8}` with rational `B_k` and
rational polynomials `C_k` (no error function inside `J_k`), and

```
L_a(T) = Σ_{k,j} e_{a,k,j} [ B_k G_j(1/24, T) + Σ_i C_{k,i} G_{j+i}(1/6, T) ],      G_n(μ, T) = ∫_0^T v^n e^{−μv²} dv.
```

## 2. Four lemmas

**L1 (the primitives `J_k`).** As Math-#201 L1: `J_k(0) = 0`, `J_k' = s^k e^{−s²/8}`, `J_k(∞) = ½8^{(k+1)/2}Γ((k+1)/2)`, verified
exactly for `k ≤ 9` (rule `JK_EXACT`); for odd `k`, `A_k = 0`.

**L2 (incomplete Gaussian moments).** For `μ > 0`, `T ≥ 0`:

```
G_0(μ, T) = ½√(π/μ) erf(√μ T),     G_1(μ, T) = (1 − e^{−μT²})/(2μ),     G_n = [ (n−1) G_{n−2} − T^{n−1} e^{−μT²} ]/(2μ)   (n ≥ 2),
```

by parts on `[0, T]` (`v^{n−1} · v e^{−μv²}`; the boundary term is `−T^{n−1}e^{−μT²}/(2μ)` at `T` and `0` at `0`). So every
`G_n(μ, ·)` is a polynomial in `T`, plus a polynomial times `e^{−μT²}`, plus (even `n`) a multiple of `erf(√μ T)`. The script
represents such "T-functions" exactly and verifies `G_n(μ, 0) = 0` and `∂_T G_n = T^n e^{−μT²}` in that space for `n ≤ 20`,
`μ ∈ {1/24, 1/6}` (rule `CUMULATIVE_EXACT`); the two identities characterise `G_n`.

**L3 (base integrals).** For `λ, u, v > 0`:

```
M_0(λ, 1) = ½√(π/λ),   M_1(λ, 1) = 1/(2λ),   M_0(λ, erf(u·)) = arctan(u/√λ)/√(πλ),
M_0(λ, erf(u·) erf(v·)) = arctan( uv / √(λ(λ + u² + v²)) ) / √(πλ).
```

*Proof of the last.* Differentiate in `v`: the left side gives `(2/√π) ∫_0^∞ s e^{−(λ+v²)s²} erf(us) ds`, which by parts is
`(2/√π) · u/(2(λ+v²)√(λ+v²+u²))` (Math-#201 L3 at `n = 1`), i.e. `u/(√π (λ+v²) √(λ+u²+v²))`. On the right, with
`g(v) = uv/√(λ(λ+u²+v²))`: `g' = u(λ+u²)/(√λ (λ+u²+v²)^{3/2})` and `1 + g² = (λ+u²)(λ+v²)/(λ(λ+u²+v²))`, so
`(arctan g)' = u√λ/((λ+v²)√(λ+u²+v²))`, and dividing by `√(πλ)` gives the same expression. Both sides vanish at `v = 0`. ∎
(The single-erf case is Math-#201 L2; rule `BASE_INTEGRALS_FLOAT` checks all four at the parameters that occur.)

**L4 (moments by parts).** For `n ≥ 1` and `f` a product of at most two error functions (or `1`),

```
M_n(λ, f) = [ (n−1) M_{n−2}(λ, f) + Σ_{u∈f} (2u/√π) M_{n−1}(λ + u², f∖{u}) ]/(2λ),
```

with vanishing boundary terms (`n ≥ 2`, or `f(0) = 0`); the case `n = 1, f = 1` is the base value `1/(2λ)`. At `f = 1` the
recurrence reproduces `½Γ((n+1)/2)λ^{−(n+1)/2}` exactly for `n ≤ 20` and the thirteen values of `λ` that occur (rule
`GAUSS_MOMENTS`).

By L1–L4 every term of `D_4` is an outer moment of one of three kinds: a polynomial part (`λ = g`, no extra factor), an
`e^{−μT²}` part (`λ = g + μ`), or an `erf(√μ T)` part (slope `√μ`), each multiplied on the erfc branch by `erfc(κT) = 1 − erf(κT)`,
so the two-error-function moments of L3–L4 occur exactly for the products `erf(√μ T) erfc(κT)`.

## 3. The exact computation

`closed_form_d4.py` extends Math-#201's arithmetic (dictionaries `(r, 2k, atom) → Fraction` with exact surd reduction,
`arctan` arguments `1, √3, 1/√3` folded into `π`, arguments above `1` reflected, all other algebraic arguments kept as atoms
with argument in `(0, 1]`) by the T-function layer of L2. The two branches of §1 are assembled with the exact `pref` and `c_E`
(from Mehta's `Z_4` and `α = 3/7` in the same arithmetic):

```
erfc branch       :  6695/54 − (6066622595/603979776)√6 − (46299277168087/1415577600000)√21/π
                     − (6695/27) arctan(√21/7)/π − (6066622595/301989888)√6 [arctan(√14/4) − arctan(√14/7)]/π
polynomial branch :  − (1577496445/603979776)√6 + (19265677168087/1415577600000)√21/π
                     − (1577496445/301989888)√6 [arctan(√14/4) − arctan(√14/7)]/π
D_4               :  6695/54 − (405/32)√6 − (1375/72)√21/π − (6695/27) arctan(√21/7)/π − (405/16)√6 [arctan(√14/4) − arctan(√14/7)]/π
```

(`603979776 = 2²⁶·9`; the large rational coefficients of the two branches cancel to `405/32`, `1375/72`, `405/16`.) The atoms
created along the way are `arctan(√15/5)` (from `m = 2`, and again from the two-erf base at `λ = 1/48`, `μ = 1/24`),
`arctan(1/2)` (`m = 3`), `arctan(√14/4)`, `arctan(√21/7)`, `arctan(√14/7)` and `arctan(1/√7)` (`κ/√λ` at `λ = 3/16`); the last
and `arctan(√15/5)` cancel identically in `D_4`. Mehta's `Z_4` through the same triangle machinery (§1 of Math-#200:
`4!√π(1/6) ∫e^{−T²/48}∫_0^T e^{−v²/24}∫_0^v V e^{−p_3²/8}`, `V` the Vandermonde) returns exactly `1536π`; `m = 1, 2, 3` return
exactly `4/3`, `29/6 − √6` and Math-#201's `D_3`.

## 4. Verification

Sixteen rules; all exact except the two float controls and the three interval containments:

| rule | content |
|---|---|
| `STRUCTURE` | `α = 3/7`, `κ = √21/28`, `λ_erfc = 1/48`, `λ_poly = 1/21 = λ_erfc + κ²`, `p_3`-powers `{1,3,5,7,9}` in both branches, the atoms created |
| `GAUSS_MOMENTS` | L4 at `f = 1` equals `½Γ((n+1)/2)λ^{−(n+1)/2}` exactly, `n ≤ 20`, thirteen `λ` |
| `JK_EXACT` | L1 for `k ≤ 9`, exactly |
| `CUMULATIVE_EXACT` | L2: `G_n(μ, 0) = 0` and `∂_T G_n = T^n e^{−μT²}` in the T-function space, `n ≤ 20`, `μ ∈ {1/24, 1/6}` |
| `D1_EXACT`, `D2_EXACT`, `D3_EXACT` | `4/3`, `29/6 − √6`, `50/3 − 76/(3π) − (200/(9π)) arctan(1/2)` exactly |
| `MEHTA_Z4_EXACT` | `Z_4 = 1536π` exactly, and equal to the closed-form Mehta element |
| `D4_FORM` | the output equals the stated closed form exactly (pinned coefficients in the raw basis) |
| `BASE_INTEGRALS_FLOAT`, `MOMENTS_FLOAT` | Simpson quadrature (`math.erf`) of the base integrals (five single-erf, three two-erf parameter sets) and of sampled `M_n` agrees to `10⁻⁹`/`10⁻⁸` (controls) |
| `D4_INSIDE_CERTIFIED` | the 60-digit interval evaluation of the closed form lies inside Math-#200's certified `D_4` enclosure, width `< 10⁻⁵⁵` |
| `SIMPLIFIED_FORM` | the form with `arctan(1/√14)` intersects the raw form's interval and lies inside the enclosure |
| `C5_CLOSED` | the same for `c_{5,ref}` against Math-#200's enclosure |
| `LIBRARY_EXACT`, `PINNED` | as Math-#201 |

Fourteen mutants exit 1 in both interpreter modes: `shift-variance` (`S²/24` for `S²/28` at `m = 4`), `vandermonde` (rejected
by the structural check: without the Vandermonde factor even `p_3`-powers appear),
`erfc-sign`, `jacobian` (`1/6 → 1/2`), `mehta` (`Z_5` for `Z_4`), `by-parts`, `one-erf`, `two-erf` (`λ + u²` for
`λ + u² + v²` in L3), `jk-init`, `gauss-half`, `boundary-term`, `atom-pi`, `cumulative-init` (`G_1` sign), `cumulative-recurrence`
(`n−1 → n` in L2). Runtime about two seconds.

## 5. The coefficient in every `d ≤ 5`

With `c_{d,ref} = Γ(7/6)(3/2)^{1/3} |S^{d−1}| D_{d−1} / (√3 √π (2π)^d)` ([LP] (15.2); Math-#199 §4, Math-#200 §4):

| `d` | `D_{d−1}` | `c_{d,ref}` | value |
|---|---|---|---|
| 2 | `4/3` | `2Γ(7/6)(3/2)^{1/3}/(3√3 π^{3/2})` | `0.0734069193060342710301359629577…` (SIDE24) |
| 3 | `29/6 − √6` | `Γ(7/6)(3/2)^{1/3}(29/6 − √6)/(2√3 π^{5/2})` | `0.0417759318405983433429366654285…` (SIDE24) |
| 4 | `(50π + 200 arctan 2 − 228)/(9π)` | `Γ(7/6)(3/2)^{1/3}(50π + 200 arctan 2 − 228)/(72√3 π^{7/2})` | `0.0233216660029528350945211949528…` (Math-#201; #199 encloses) |
| 5 | Proposition above | `Γ(7/6)(3/2)^{1/3} D_4/(12√3 π^{7/2})` | `0.0132193193800849680760334875146…` (this record; #200 encloses) |

The torus constants `c_{d,24}` remain enclosed through the SIDE24 §§3–4 sandwich with the constants of Math-#199 and #200.

## 6. Scope and non-claims

- The Proposition is an identity, proved by L1–L4 applied to the exact reduction of Math-#200. It consumes [LP] (15.1)–(15.2) and
  SIDE24 §1 at their scope and does not review them.
- **No closed form for `D_5` (`d = 6`) is claimed or expected by this method.** The `m = 5` reduction needs a second cumulative
  layer: the first produces `erf(√μ v)` terms (L2), and a cumulative integral of `e^{−μ'v²} · polynomial · erf(√μ v)` is not
  elementary in its upper limit (it is an Owen-`T`-type function), so the outer integrand would carry a non-elementary factor;
  equivalently, the terms are Gaussian integrals over a three-dimensional wedge with an `erfc` and an `erf` factor, five-dimensional
  orthant-type integrals, which are not elementary in general.
- Math-#200 §7 says "no closed form for `D_4`"; this record supplies one. Math-#200 is not edited here.
- C8 stays OPEN; `coefficients/side24_v1` is unchanged; no register, GRAPH, STATUS, PROOF_INDEX, SELECTOR_REGION or catalog
  surface is touched; `executed: false`.

## 7. Files, pins, how to run

`coefficients/side24_d5_closed_form_20260930/{NOTE.md, closed_form_d4.py, RESULTS.json, SOURCE_FILES.json}` and
`.github/workflows/side24-d5-closed-form.yml` (manifest, pins, byte-identical replay in `-B -S` and `-B -O -S`, the stated
closed-form string, the fourteen mutants). Pins on `main 3e0a91b`: [LP] `imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md`
blob `dfed3b8d`; SIDE24 `coefficients/side24_v1/PROOF.md` blob `44b66f04`. Companions, not on `main`: Math-#200 at `33d50de`
(`coefficients/side24_d5_20260930/RESULTS.json` blob `b67c00f4`, the two enclosures quoted in the script; `NOTE.md` blob
`ab3fe17d`, the reduction); Math-#201 at `3abcc10` (`closed_form_d3.py` blob `a0c91692`, the arithmetic and L1, L3–L4, reused
verbatim). Run: `python3 -B -S closed_form_d4.py` (exit 0, JSON on stdout identical to `RESULTS.json`); `--mutant NAME` exits 1.

## 8. Current disposition

- **Head / owner:** see the PR's disposition block; branch `claude/side24-d4-closed-form-20260930` (base `main 3e0a91b`);
  author lane Anthropic / Claude (`session_017Mi3hxjaxV45x6zo6o1ee3`).
- **Claim:** the Proposition and Corollary of §0, proved by exact integration of the Math-#200 reduction; exact `m = 1, 2, 3`
  and `Z_4` regressions; the closed form at the centre of the independent certified enclosure. No theorem of [LP] or SIDE24 is
  proved or reviewed.
- **Completed review scopes:** none yet. Requested: nonauthor reads of Slice A (§1: the reduction data, odd `k`, the constants;
  L1), Slice B (§2 L2–L4 and §3: the T-function layer, the two-erf base integral, the by-parts recurrences, the atoms and
  cancellations, the `Z_4` identity), Slice C (§§4–6: rules, mutants, containment, the coefficient table, the `D_5` non-claim).
- **Unresolved finding IDs:** none.
- **Validation:** 16/16 rules in both modes, byte-identical output; 14/14 mutants rejected in both modes; workflow replayed
  locally; hosted run pending at opening.
- **Next action:** nonauthor reads; amendments on this branch, recorded in `SOURCE_FILES.json`. Author will not merge.

## 9. Revisions

- **v1.1 (Codex review 5371784947 on `60e56ef`).** (i) Thread 4149168080 (P2), taken: the `mehta` mutant altered `Z_3` (a
  leftover of the Math-#201 script) and was rejected only through `D3_EXACT`; it now replaces `Z_4` by `Z_5` in the `m = 4`
  prefactor and is rejected by `MEHTA_Z4_EXACT`, `D4_FORM` and the containments. (ii) Thread 4149168070 (P1, the replay
  workflow and the 2026-09-27 owner stop), not taken; the reasons are on the thread: the per-packet replay workflow is the
  repository's standing convention (88 workflow files on `main 3e0a91b`, about thirty of them added by every lane since
  2026-09-27), the owner's later directives quoted in `AGENTS.md` and the owner workflow of 2026-09-30 govern this record, and
  the workflow is path-scoped to this packet and its pins. The owner can direct its removal at any time; the record is
  runnable locally in two seconds without it. No certified value changed.
