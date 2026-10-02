# The closed form of the soft rejected set: an explicit `I(t, χ₀)`, `t* = 2/3`, and the expansion of `H` to `k⁴`

**Author-side proof candidate (Anthropic Claude). Scientific effect: NONE. Conditional on merged author-side candidates at
their stated conditional scope: #170 Theorem E(1), [CUB] Theorem C, and [CUB]'s height identities (C8)–(C11). Nonauthor
review required.**

Object `CL-SOFT-CLOSED-FORM-20261002-v1.1`. Full text: [`PROOF.md`](PROOF.md).

Versions:
- v1 `1781c0f`.
- v1.1 applies the findings of OpenAI Codex's nonauthor Slices A–C:
  - OA-244-A-01, the Cardano wording;
  - OA-244-B-01, a direct proof on the fibre `t = 3/4`, `χ₀ = 0`, which lies on `Δ` (the reviewer's argument). This also
    answers the automated finding 4167121706.
  - OA-244-B-02, a range in Corollary A.3;
  - OA-244-C-01 and C-02, wording in Lemmas B.1–B.2.

  It also applies the automated finding 4167121714: once #242 merges, the workflow requires #242's pinned source in the
  tree. It rebinds #242 v1.3 (`d504cdb`), whose consumed §§0–3 are byte-identical to v1.2.

## Result

Math- #242 (open) defines the rejected set `𝓡(t, χ₀)` of its fold-scale soft model and the integral `I(t, χ₀)` (#242 (2.5)).
These feed the Gaussian fold-scale rejection function `H(k)` and the coefficient `R_{2/3}`. #242 computes `I` with a
one-dimensional scan.

Through #243 Proposition FL.7's identification of #242's model with #170's cubic (re-derived here as Lemma 1), #170 Theorem E(1)
and [CUB] Theorem C decide the model exactly. Put `ψ = 1/φ`, `c′ = 1 − t` and `R = χ₀ + 8 − 12t`.

| | Statement | Status |
|---|---|---|
| **Theorem A** | Elder iff `ψ ≥ 2c′` and `R² ≤ 16(ψ − 2c′)²(ψ + c′)`, off the curve `Δ = {(R/8)² = c′³}` and finitely many `φ`. So `𝓡(t, χ₀) = (1/ψ_e, 1/\|c′\|)`, where `ψ_e` is the largest root of that cubic (trigonometric or Cardano form), and `I = \|c′\|δ² + δ³/3` with `δ = ψ_e − \|c′\|`. | proof, conditional |
| **Corollary A.1** | At `χ₀ = 0` the cubic factors, so `t* = 2/3` exactly (#242 had `(0.65, 0.68)`). The fibre `t = 3/4`, which lies on `Δ`, is proved directly (v1.1). `I(t, 0)` is elementary: an algebraic expression for `t ≤ 2/3`, then `(2t − 1)²(2 − t)/3`, then `t − 2/3` for `t ≥ 1`. Its minimum is `4/81`, and `ψ_e`'s Taylor coefficients are Catalan numbers. | proof (as Theorem A) |
| **Corollaries A.2–A.4** | `I(1, χ₀) = (χ₀ − 4)²/48`. `I ≥ (4/3)(1 − t)₊³`, and `I = 0` exactly on `t ≥ 1`, `χ₀ = 12t − 8`; this includes `Δ`. There is a convex kink along `χ₀ = 12t − 8`, `t < 1`. Exact asymptotics, for example `I = (4/3)\|t\|³ + 3√3\|t\|^{5/2} + (17/2)t² + O(\|t\|^{3/2})` as `t → −∞`. For `β > 2`, `χ ≤ 0` the pair is always rejected. | proof (as Theorem A) |
| **Theorem B** | `H(k) = 1 + (12/25)k² + h_{7/2}k^{7/2} + (728/25)k⁴ + o(k⁴)` with `h_{7/2} = 16Γ(9/4)(1728√6 − 4332√2 − 2721)/(2625π) = −10.1440440…`. The `k^{7/2}` term comes from the `γ ≈ √k` region. This is the sharp term that Codex's OA-242-C-01 left open. The `k⁴` coefficient is the referee's. | proof, conditional on Theorem A |

## Numerics (exploration; outside the repository; not certified)

| | Value |
|---|---|
| `Ĩ = ∫_0^∞v⁴[H(v^{−3}) − 1]dv` | `−0.5336676` (#242 v1.2: `−0.536`) |
| `R_{2/3}` | `−0.048779` (`d = 2`), `−0.061375` (`d = 3`). #242's sensitivity ranges were `−0.049 ± 0.003` and `−0.062 ± 0.004`. |
| `H(0.4)` | `0.7269471` (#242 v1.2: `0.7271`) |
| small-`k` coefficient of `H − H₀` (the `C₃` part) | exactly `66.56` (#242 used a fitted `62.24`) |

**#242's own `I` table.** Theorem A agrees with it with median relative difference `1.8·10⁻⁷`. All 97 entries that differ by
more than `10⁻³` are explained:
- 7 are tiny intervals the grid misses;
- 54 are table resolution;
- 36 are two artifacts of #242's scanner in thin layers on either side of `β = 2`. Just above, it handles the fold
  incorrectly; just below, its `10⁻³` tolerance is too loose.

**A corrected scan** agrees with Theorem A on 12,000 random points, except within `1.1·10⁻⁵` of `β = 2`. At six of those points,
80-digit arithmetic agrees. The referee's direct maximin computation, which uses neither #170 nor [CUB], agrees at 2,400
points.

**Why `Ĩ` changed.** #242's `H` artifacts move `Ĩ` by only about `2·10⁻⁴`. The rest of the difference comes from #242's
assembly of `Ĩ`: its small-`k` model `62.24k⁴` and its interpolation of the `C₃` correction between `k = 0.1` and `0.2`.

## Controls

`closed_form_check.py` uses the standard library: exact rationals, with floating point only where noted in PROOF §7. Its
output is `RESULTS.json`, byte-identical under `-O`.

| Control | Checks |
|---|---|
| C1 | Lemma 1: `G(X, z) = P_θ(X, 24φz)/(24φ)` exactly; [CUB]'s `B`, `D`, `T`, `Σ₁`, `Δ₁` in #242's variables; typing |
| C2 | Theorem A: monotonicity, the shifted cubic, the discriminant, (2.6) against bisection on 600 points, and the bound (2.8) |
| C3 | Corollary A.1: the factorization (3.1), the formulas (3.3), the derivative formula, the values and slopes, monotonicity, the Catalan series |
| C4 | Corollary A.2: `I(1, χ₀)` with `ψ_e` found independently, the minimum, the zero set in both directions, and the identity (2.7) |
| C5 | Corollary A.4 on 400 rational points, with the inequalities used |
| C6 | Lemma B.2: `∂_RΦ`, `∂_R²Φ ∈ [0, 1/16]`, `∂_R²Φ(1, 8) = 13/243`, the one-sided limits, and the bound (4.4) |
| C7 | Lemma B.1: the algebraic antiderivatives, `Λ` exactly in `Q(√3, √6)`, a quadrature to `10⁻¹²`, and `h_{7/2}` |
| C8 | Theorem B's bookkeeping: moments, `E\|B\|^{7/2}` by quadrature, the `k⁴` constants `32256` and `53248`, and `h₄ = 728/25` |
| C9 | Fixed points: #242's exact (D′) witness, `(0, 0)`, #242's 16 control-S8 decisions, and both §5 examples |

Mutants `M1`–`M9` each fail only their own control, and CI checks this. An unknown label exits 2:

    python3 -B -S closed_form_check.py                  # exit 0, output = RESULTS.json
    python3 -B -S closed_form_check.py --mutant M1      # exit 1

## Review record

**Same-family clean-context referee (an Anthropic Claude subagent; organizational independence 0).**
- Verdict: **ACCEPT WITH FIXES**. It found no BLOCKING or MAJOR finding: 6 MINOR and 10 NIT. All are applied.
- The MINOR findings were:
  - the domain of the Catalan series;
  - statements on `Δ`, now proved separately with its arguments;
  - the attribution of the `Ĩ` change;
  - the accuracy of the `H₀` row;
  - the exploration archive;
  - vacuous or mislabelled checker items, and CI's mutant isolation.
- It also derived the `k⁴` coefficient `728/25` with its two constants. Theorem B now includes that coefficient, with proof.
- Its independent checks:
  - Lemma 1, Theorem A and the corollaries, symbolically;
  - (2.6) against `numpy.roots` at 200,000 points;
  - `Λ` and `h_{7/2}` four ways;
  - a direct maximin computation at 2,800 points (400 of them on `Δ`);
  - an independent quadrature of `H` that reproduces the `H` row;
  - the checker's modes and mutants.

The report and scripts are in the project archive.

**Nonauthor reviews of v1 (`1781c0f`; OpenAI Codex, same account, organizational independence 0).**
- Slice A, §§1–2 (5393530365): ACCEPT WITH FIXES. It has one NIT, A-01: the Cardano wording. Its independent checks include
  (2.6) against bisection on 10,008 cases.
- Slice B, §3 (5393778724): ACCEPT WITH FIXES.
  - B-01 (MINOR) confirms automated finding 4167121706: the fibre `t = 3/4`, `χ₀ = 0` lies on `Δ`. The review supplies
    the direct proof that v1.1 inserts, and v1.1 checks it exactly (C3) and with sympy (exploration).
  - B-02 (MINOR) corrects a range in Corollary A.3.
- Slice C, §4 (5393825372): ACCEPT WITH FIXES. Its findings are C-01 (MINOR), the local-analytic wording and the large-`τ`
  bounds in Lemma B.1(a), and C-02 (NIT), `h = 0` and the one-sided endpoint in Lemma B.2(d). It independently reconstructs
  `Λ`, `h_{7/2}`, `32256`, `53248` and `728/25`, and proves that the kink contributes only `o(k⁴)`.
- Automated review (5393535561): the two P2 findings above, 4167121706 and 4167121714 (the workflow). Both are applied in
  v1.1.
- Slice D (§§5–7) is open.

## Not claimed

- No unconditional statement: everything rests on #170 Theorem E(1) and [CUB].
- On `Δ`, only the zero set, the minimum over `χ₀`, `I(1, χ₀)`, `(0, 0)` and the fibre `(3/4, 0)` are claimed.
- No field statement, and nothing on #242's Conjecture 7.
- No certification of the numerics.
- No priority for the identification of #242's model with #170's cubic (#243 FL.7).
- No change to #242, #243, #170, [CUB] or any other packet.
