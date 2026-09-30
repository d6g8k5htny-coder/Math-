# The compact-window coefficient `c_{B,K}` in `d = 3`: transfer to the torus for every `L ≥ 10` and every frame

**Object** `CL-C8-WINDOW-COEFFICIENT-D3-TORUS-20260930-v1` · **scientific effect NONE** · declarative record, `executed: false` ·
base `main 3e0a91b` · claim: Math-#197 comment 5921235693 · companion: Math-#197 (`frontiers/c8_window_coefficient_planar_20260930`,
head `63e123f`), whose §4 gives the `d = 3` reference closed form and states "no torus transfer is made in `d = 3`"; this record
supplies that transfer. Catalog entry C8 stays OPEN; no register, GRAPH, STATUS or catalog surface is touched. Same GitHub account
as every lane: zero organizational-independence credit. Claude reads of this record count for nothing. The author will not merge.

## 0. Statement

Let `f` be the unit-variance stationary Gaussian field on `R³/(LZ³)` with the parent kernel `K_L` of [LP] §1, `B = [b_−, b_+]` a birth
window and `K = [k_−, k_+]` a gap window (`k_− ≥ 0`), and `c^(3)_{B,K}` the leading coefficient of [LP] Theorem B for the pairs with
birth in `B` and scaled gap in `K` ([LP] (11.3), §15; both stated for every `d`).

**Proposition (d = 3 torus transfer).** For every `L ≥ 10` and every frame, `c^(3)_{B,K}` lies in the interval computed by
`window_coefficient_d3.py` from the entry box of radius `E^(3)_10 = 2.058·10⁻¹¹`; on the C8 band `B = [0, 1]`, `K = [1/2, 2]`,

```
c^(3)_{B,K}(torus, every L ≥ 10, every frame) ∈ [0.00097438236231621369…, 0.00097438236973228724…]   (relative half-width 3.8e-9),
c^(3)_{B,K}(reference)                     = 0.0009743823660242504624710565467842206863682961221797073…,
c^(3)_{B,K}(torus, L = 24)                 = the reference digits to 55 places (arithmetic-limited).
```

The same holds on every window of §5, with relative half-width at most `4.3·10⁻⁹` at `L ≥ 10`; the full window reproduces SIDE24's
`c_{3,24}` interval.

## 1. The object

[LP] (11.3) reads `c_{B,K} = 4 ∫_{B×K×S^{d−1}} k^{−2/3} π_0 z_0 db dk dσ` with `z_0 = 36k² E[det(A)² 1{A ≺ 0} | f = b, V = 0]` and, by
§15, `π_0 = p_{(f,V)}(b, 0) p_G(0) φ_τ(12k)`, `p_{(f,V)}(b, 0) = p_V(0) p_{f|V=0}(b)`. In `d = 3`, frame `(u, w_1, w_2)`, `G = ∇f ∈ R³`,
`V = (f_uu, f_uw1, f_uw2)`, `A = (f_{w_i w_j})` the `2×2` transverse Hessian, `t = f_uuu`, `τ² = Var(t | G = 0)`:

```
c^(3)_{B,K} = 144 ∫_{S²} p_G(0) p_V(0) I_B(u) J_K(u) dσ(u),
I_B(u) = ∫_B p_{f|V=0}(b) E[det(A)² 1{A ≺ 0} | f = b, V = 0] db = E[1{f ∈ B} det(A)² 1{A ≺ 0} | V = 0],
J_K(u) = ∫_K k^{4/3} φ_τ(12k) dk.                                                                         (1.1)
```

Odd and even derivatives are independent for an even kernel, so `(G, t)` is independent of `(f, V, A)`. For the reference kernel
Math-#197 §4 gives `I^ref_B = ∫_B φ_{2/3}(b) m_{3,b} db` with `m_{3,b} = (b³ + b)φ(b) + (b⁴ + 2b² + 7)Φ(b) − 4√2 e^{−b²/4} Φ(b/√2)`,
and `c^(3,ref)_{B,K} = c_{3,ref} F^(3)_B G_K`. What fails on the torus is that the conditional mean of `A` given `f = b, V = 0` is
`b·μ` with `μ` only close to `−I`, and the truncated cone moment then has no closed form.

## 2. The sandwich lemma

**Lemma S.** Let `X = (f, A_11, A_12, A_22)` be centred Gaussian with covariance `C'`, `C` a positive definite `4×4` matrix and
`0 ≤ ε < 1` with `(1 − ε) C ≤ C' ≤ (1 + ε) C`. For `g(x) = 1{x_f ∈ B} det(A)² 1{A ≺ 0}` and `I^C_B := E_C[g]`,

```
(1 − ε)⁴/(1 + ε)² · I^C_{B/√(1−ε)}  ≤  E_{C'}[g]  ≤  (1 + ε)⁴/(1 − ε)² · I^C_{B/√(1+ε)},          B/s = [b_−/s, b_+/s].
```

*Proof.* `det C' ≥ (1 − ε)⁴ det C` and `C'^{−1} ≥ C^{−1}/(1 + ε)`, so
`p_{C'}(x) ≤ (1 − ε)^{−2} (2π)^{−2} det(C)^{−1/2} exp(−xᵀC^{−1}x/(2(1+ε))) = ((1+ε)/(1−ε))² p_{(1+ε)C}(x)`. Since `g ≥ 0`,
`E_{C'}[g] ≤ ((1+ε)/(1−ε))² E_{(1+ε)C}[g] = ((1+ε)/(1−ε))² E_C[g(√(1+ε) Y)]`. Now `det(sA)² = s⁴ det(A)²`, `1{sA ≺ 0} = 1{A ≺ 0}` and
`1{s y_f ∈ B} = 1{y_f ∈ B/s}`, so `E_C[g(sY)] = s⁴ I^C_{B/s}`, giving the upper bound with `s⁴ = (1+ε)²`. The lower bound is the same
argument with `det C' ≤ (1 + ε)⁴ det C`, `C'^{−1} ≤ C^{−1}/(1 − ε)` and `s² = 1 − ε`. ∎

The birth window is the only ingredient that is not homogeneous; the lemma trades the unknown covariance for a rescaled window
(`b_± ↦ b_±/√(1 ± ε)`) under the known one. This is SIDE24 §4's argument, which there applies to the full window only (`B = R` is
scale-invariant); Math-#197 §3 notes that it "does not" apply to a window as such. Two exact tests (rule `SANDWICH_EXACT_SCALING`):
for `C' = (1 + η) C_ref'` exactly, `E_{C'}[g] = (1 + η)² I^ref_{B/√(1+η)}`, and this value lies inside the sandwich with `ε = |η|` for
`η ∈ {±1/50, ±1/200}` and five windows, among them `[3, 7/2]` and `[−7/2, −3]`, where the window rescaling dominates the density
factor (the mutants that rescale the wrong way or exchange the two rescalings fail there, and their bounds come out of order, rule
`SANDWICH_ORDERED`).

## 3. The reference law and the eigenvalue floor

The reference covariances come from `Cov(∂^a f, ∂^b f) = (−1)^{|a|} ∂^{a+b} e^{−|z|²/2}|_0` and
`∂^α e^{−|z|²/2}|_0 = Π_i (−1)^{α_i/2} (α_i − 1)!!` (even `α`), computed in exact rationals. Conditioning `(f, A_11, A_12, A_22)` on
`V = 0` (`Cov V = diag(3, 1, 1)`, only `f_uu` correlated with `f, A_11, A_22`, with covariances `(−1, 1, 1)`):

```
C'_ref = [[2/3, −2/3, 0, −2/3], [−2/3, 8/3, 0, 2/3], [0, 0, 1, 0], [−2/3, 2/3, 0, 8/3]],
A | f = b, V = 0  ~  N(−b(1, 0, 1), diag(2, 1, 2))  =  −b I + Q,       τ² = 15 − 9 = 6,       det Cov V = 3,  det Cov G = 1
```

(rule `REFERENCE_EXACT`; this is Math-#197 §4's law). Its eigenvalues are `2 ± √(8/3)`, `2` (on `(0, 1, 0, −1)`) and `1` (the `A_12`
coordinate), so `λ_min = 2 − √(8/3) = 0.367`; the script certifies the floor `C'_ref ≥ I/3` exactly by Sylvester's criterion on
`C'_ref − I/3` in rationals (rule `LAMBDA_FLOOR`; SIDE24 §3 has the same floor `1/3` for the full jet). Hence for any `C'`,
`‖C'_ref^{−1/2}(C' − C'_ref)C'_ref^{−1/2}‖ ≤ 3 ‖C' − C'_ref‖_F`, and `ε := 3 ‖C' − C'_ref‖_F` satisfies the hypothesis of Lemma S.

`I^ref_B` is Math-#197 §4's closed form, evaluated with interval endpoints: `∫ φ_{2/3}(b)(b³ + b)φ(b) db = −(2b²/5 + 18/25)e^{−5b²/4}/(2πσ)`,
`∫ φ_{2/3}(b)(b⁴ + 2b² + 7)Φ(b) db = σ⁴G_4 + 2σ²G_2 + 7G_0` at `x = b/σ`, slope `σ = √(2/3)`, and
`∫ φ_{2/3}(b) 4√2 e^{−b²/4}Φ(b/√2) db = (4/σ) G_0(√2 b; 1/2)`, with Math-#197's Owen primitives `G_0..G_4` (code reused verbatim).
The full window returns `29/6 − √6` to `1e-50` (rule `D2_EXACT`) and `m_{3,b}` agrees with the direct double integral at six points
(rule `M3_FLOAT`).

## 4. The torus: image bound, entry box, `ε`

**Image bound in `d = 3`.** As in Math-#197 §3 (the contraction bound `|D^q φ(x)| ≤ 76|x|⁶φ(x)` for `|x| ≥ 1`, `q ≤ 6`, any unit
directions, `|D^q φ(0)| ≤ 15`, the normalization `S ≥ 1`), with the `d = 3` shell count: `|n|_∞ = j` holds
`(2j+1)³ − (2j−1)³ = 24j² + 2 ≤ 26 j²` points with `|n|² ≤ 3j²`, so `Σ_{n≠0} |n|⁶ e^{−L²|n|²/2} ≤ 702 Σ_j j⁸ e^{−L²j²/2} ≤ 1404 e^{−L²/2}`
(ratio of successive terms at most `2⁸ e^{−3L²/2} < 1/2` for `L ≥ 10`), and every covariance entry of the 3-jet of `K_L`, in every
frame, is within

```
E^(3)_L = 1404 (76 L⁶ + 15) e^{−L²/2}:     E^(3)_10 = 2.0581e-11,   E^(3)_12 = 1.7142e-20,   E^(3)_24 = 1.7086e-112      (rule IMAGE_BOUND)
```

of its reference value; `E^(3)_L` decreases in `L`, so the `L = 10` box contains the jet of every `L ≥ 10` in every frame.

**Interval evaluation.** The class `Space3(E)` widens the 28 entries of the even block `(f, f_uu, f_uw1, f_uw2, A_11, A_12, A_22)`
(other than `Var f = 1`) and the 10 entries of the odd block `(f_u, f_w1, f_w2, t)` by `±E`, and evaluates `p_G(0) = (2π)^{−3/2} det(Cov G)^{−1/2}`,
`τ² = Var t − cᵀ Cov(G)^{−1} c`, `p_V(0) = (2π)^{−3/2} det(Cov V)^{−1/2}` and the Schur complement `C'` of `V` in `(f, A)` by interval
linear algebra (adjugate inverses); `ε = 3·‖C' − C'_ref‖_F` with each entry's deviation the supremum over its interval. Every quantity
depends on the frame only through the entries, so one box bounds the integrand of (1.1) for every `u`, and `|S²| = 4π`. Values
(rule `EPSILON`):

```
ε(L ≥ 10) = 5.972e-10,   ε(L ≥ 12) = 4.974e-19,   ε(L = 24) = 3.8e-58 (arithmetic-limited),   ε(E = 0) = 4.3e-59;
τ²(L ≥ 10) ∈ 6 ± 1.1e-9,   p_G p_V (L ≥ 10) = 0.0023275540108… ± 1.3e-13.
```

Then `c^(3)_{B,K} ∈ 144 · 4π · [p_G p_V] · Lemma S(I^ref, ε) · J_K(τ²)` with `J_K` by Math-#197 (2.2) at the interval `τ²`.

## 5. Values (`RESULTS.json`)

`F^(3)_B` and `G_K` are Math-#197's (its `birth_factor_d3_reference` table, reproduced here); `c^(3,ref) = c_{3,ref} F^(3)_B G_K`,
`c_{3,ref} = 0.0417759318405983433429366654285755564666815196…` (SIDE24 (1) at `d = 3`).

| `B` | `K` | `c^(3)` reference | torus, every `L ≥ 10`, every frame | rel. half-width |
|---|---|---|---|---|
| `[0,1]` | `[1/2,2]` | `0.00097438236602425046247…` | `[0.00097438236231621369, 0.00097438236973228724]` | `3.8e-9` |
| `[0,1]` | `(0,∞)` | `0.01446277713931286117278…` | `[0.01446277709167767642, 0.01446277718694804607]` | `3.3e-9` |
| `[−1,1]` | `[1/2,2]` | `0.00110183822983417559227…` | `[0.00110183822558582647, 0.00110183823408252472]` | `3.9e-9` |
| `[−2,2]` | `[1/2,2]` | `0.00244005150534917491086…` | `[0.00244005149542905292, 0.00244005151526929693]` | `4.1e-9` |
| `[0,∞)` | `[1/2,2]` | `0.00268447988228775572900…` | `[0.00268447987082819968, 0.00268447989374731181]` | `4.3e-9` |
| `(−∞,0]` | `[1/2,2]` | `0.00013003706128481170262…` | `[0.00013003706072970715, 0.00013003706183991625]` | `4.3e-9` |
| `R` | `[1/2,2]` | `0.00281451694357256743162…` | `[0.00281451693155790684, 0.00281451695558722806]` | `4.3e-9` |
| `R` | `(0,∞)` | `0.04177593184059834334293…` | `[0.04177593168364896978, 0.04177593199754771746]` | `3.8e-9` |

At `L = 24` every enclosure agrees with the reference to about 55 digits; the full window lies inside SIDE24's `c_{3,24}` interval
`[0.04177593184059834334, 0.04177593184059834335]` (rule `SIDE24_CONSISTENT`). The C8 band carries `34.6 %` of the `d = 3` birth mass
(against `48.3 %` in `d = 2`: `m_{3,b}` rises faster in `b`, so the mass sits higher) and `6.74 %` of the gap mass (the gap factor is
dimension-free), `2.33 %` in all.

**Float control (not part of the certificate).** For a non-scalar perturbation of the even block (five entries moved by `±10⁻³`,
e.g. `Cov(f, A_12) = 10⁻³`, so that `A_12 | f = b` acquires the mean `0.001 b` and the conditional mean is no longer a multiple of the
identity), `ε = 8.12·10⁻³`; a float evaluation of `I'_B` (the `A_12`-integral over `|A_12| < √(A_11 A_22)` in closed form through
truncated normal moments, then Gauss–Legendre in `A_11, A_22` and `b`; the same code reproduces `I^ref_B` to `2·10⁻⁹`) lies inside
the sandwich on `[0, 1]`, `[−1/2, 3/2]` and `[1, 2]` (`0.82683` in `[0.79096, 0.86102]`, etc.; rule `FLOAT_CONTROL`).

## 6. Rules, mutants, verification

`python3 -B -S window_coefficient_d3.py` (also `-B -O -S`; about ten seconds) prints `RESULTS.json` and exits `0` only if all fifteen
rules hold: `REFERENCE_EXACT`, `LAMBDA_FLOOR`, `D2_EXACT`, `M3_FLOAT`, `IMAGE_BOUND`, `EPSILON`, `SANDWICH_EXACT_SCALING`, `FLOAT_CONTROL`,
`FACTORIZATION` (the pipeline at `E = 0` reproduces `c_{3,ref} F^(3)_B G_K` on all twelve windows), `SIDE24_CONSISTENT`, `NESTING` (the
`L ≥ 10` enclosure contains the reference and intersects the `L = 24` one, which is `10⁴⁰` times narrower), `WIDTHS`, `SANDWICH_ORDERED`,
`LIBRARY_EXACT`, `PINNED`. Eleven mutants exit `1` in both interpreter modes: `image-shells` (`13j²` shells), `lambda-min` (floor `1`),
`sandwich-swap` (the two rescalings exchanged), `window-scale` (`B·s` for `B/s`), `d3-cross` (the cross term of (4.1) halved),
`schur-sign`, `sphere` (`2π` for `4π`), `tau-cross` (`Cov(t, f_u)` dropped), `no-owen`, `gamma-shape`, and `tail-dropped` (series tails
dropped; rejected when the truncated incomplete gamma function, evaluated at the two ends of an interval argument, comes back out of
order and the interval class refuses the empty interval). The hosted workflow replays manifest, pins, both modes byte for byte, the
SIDE24 `d = 3` interval quoted in the script, and the mutants.

## 7. What this does not do

- It encloses `c^(3)_{B,K}` for the torus; it does not revalidate [LP] Theorems B and §15 (consumed at their scope), and it does not
  review Math-#197.
- Not `d ≥ 4` window coefficients: Lemma S holds in every `d` (with `n = 1 + m(m+1)/2` coordinates and degree `2m`), but the reference
  birth integral `I^ref_B` for `m ≥ 3` with a window is not in closed form (the full-window value is Math-#199/#201 and #200/#202); a
  certified quadrature in `b` would supply it.
- Not `C`, `r_*` or `z_*`; C8 stays OPEN; no register surface is touched; `executed: false`.

## 8. Provenance

Pins on `main 3e0a91b` (workflow-checked): [LP] `imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md` blob `dfed3b8d`
((11.3), §15); SIDE24 `coefficients/side24_v1/PROOF.md` blob `44b66f04` (§§2–4: image bound, `C_ref ≥ I/3`, scaling argument) and
`ENCLOSURE.json` blob `57af39a0` (the `d = 3` interval quoted in the script). Companion, not on `main`: Math-#197 at `63e123f`,
`window_coefficient.py` blob `43b4f51b` (the interval class, special functions, Owen primitives and incomplete gamma reused verbatim;
`F3_ref` generalized to interval endpoints), `NOTE.md` blob `56d99b48` (§4: the `d = 3` closed form (4.1)), `RESULTS.json` blob
`95443edf` (its `d = 3` reference factors, reproduced here). No external numerical library is used.

## 9. Current disposition

- **Head / owner:** see the PR's disposition block; branch `claude/c8-window-d3-torus-20260930` (base `main 3e0a91b`); author lane
  Anthropic / Claude (`session_017Mi3hxjaxV45x6zo6o1ee3`).
- **Claim:** Lemma S and its use; the `d = 3` image bound; the certified `ε`; the torus enclosures of `c^(3)_{B,K}` for every `L ≥ 10`
  and every frame, and for `L = 24`, on the windows of §5. No theorem of [LP] or SIDE24 is proved or reviewed.
- **Completed review scopes:** none yet. Requested: nonauthor reads of Slice A (§§1–2: the object, Lemma S and its proof, the exact
  scaling tests), Slice B (§§3–4: the reference law, the eigenvalue floor, the image bound, the entry box and `ε`), Slice C (§§5–7:
  values, float control, rules, mutants, non-claims).
- **Unresolved finding IDs:** none.
- **Validation:** 15/15 rules in both modes, byte-identical output; 11/11 mutants rejected in both modes; workflow replayed locally;
  hosted run pending at opening.
- **Next action:** nonauthor reads; amendments on this branch, recorded in `SOURCE_FILES.json`. Author will not merge.
