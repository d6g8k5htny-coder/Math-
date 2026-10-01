# The one-dimensional lifetime and crest-to-trough laws with remainder `O(h^{3/4})`

**Author-side proof candidate (Anthropic Claude). Scientific effect: NONE. Nonauthor review required.**

Object `CL-D1-SHARP-REMAINDER-20261001-v1`. Full text: [`PROOF.md`](PROOF.md).

## Result

On the circle `T = R/LZ`, under Math- #214's hypothesis (H), as `h ↓ 0` and `ℓ ↓ 0`:

    ν₊(h) = (C₀/2) h^{−1/3} + (I/2) h^{1/4} + B₂ h^{1/3} + O(h^{3/4})           (D1⁺.1)
    ν(ℓ)  =  C₀ ℓ^{−1/3}   +  C₁ ℓ^{1/4}  + 2B₂ ℓ^{1/3} + O(ℓ^{3/4})           (D1⁺.2)

- **What it improves.** Math- #214 proved these with `O(h^{1/2})`; its proof gives `O(h^{0.57})` for (D1.1). The
  constants are #214's.
- **Consequence.** `2ν₊(ℓ) − ν(ℓ) = (I − C₁)ℓ^{1/4} + O(ℓ^{3/4})`.
- **The exponent.** `3/4` is the order of the first correction to the cusp term (PROOF §5.1). Its coefficient is not
  computed.

## The new ingredients

| | Statement | Replaces |
|---|---|---|
| **Lemma E** | `0 ≤ G_θ − g_θ ≤ C[v₂ min(1, s) + tail]` with `s = m v₁^{−1/2} ≍ κ` | #214's `E₂`-correction bound `Ct²` (`O(h^{0.61})`) |
| **Prop. 2.2⁺** | The model kernel `k_θ` (fold − cusp) is `O(h³t^{−12})` beyond `t_*`, so the fold and cusp terms are integrated to a fixed `t₀` | #214's cuts at `t_*` (`O(h^{0.57})`) |
| **Lemma Φ** | Under the pinned law, regressing the even part on `E₁` writes the window field as `g_{φ_G} + O + B + φ_GÊ`. Here `φ_G = E₁/m` is independent of `(O, B)`, `‖Ê‖ = O(t²)` (and `Ê` is even), `E O = O(t²)`, and `O − E O = O(t/κ)`. | — |
| **Lemma W** | Given everything but `φ_G`, the elder set is an interval `(φ₋, φ₊)`. Its edges move by `−η_{±1/3}(∓3/2)/12 + O(ε²)`, since the slope of the competing critical value is `12`. Also `φ₊ − φ₋ − 2/3 = O(3/2)/6 − Ê(3/2)/18 + O(ε²)`: the even remainder only translates the window. | #214 Lemma 3.3's margin `η` at the edges |
| **Prop. M** | The elder kernel differs from the sign kernel by relative `O(t² + (t/κ)²)` of the edge mass, `O(h^{3/4})` in total | #214's misclassification bound `O(h^{1/2})` |

The gain in (D1⁺.2) comes from a mean. The edges of the elder window fluctuate by `O(t/κ)`. But conditionally on
everything except `φ_G`, the elder set is an interval whose endpoints are independent of `φ_G`. So the misclassified mass
is first order only in the *mean* of the first-order part of `φ₊ − φ₋ − 2/3`, and second order in the fluctuation. That
mean is `O(t²)`, for three reasons:
- the even fluctuation cancels and is centered;
- `Ê = O(t²)`;
- the odd part's mean is proportional to `E[f^{(5)} | pins] ∝ α ≍ κt`.

## Dependencies

**Consumed.** Math- #214 (open; head `cf162b1`, PROOF blob `873532b9`, v1.1):
- §§0–5 as stated, plus the intermediate estimates in its proof of Prop. 2.2 (c)–(d), which are rerun on a longer range;
- nonauthor analytic review by OpenAI Codex on `f4a58df`: "Slices A–D and Theorem D1 ACCEPTED at the stated circle
  scope".

**Cited only.**
- Math- #237: the `d ≥ 2` parity argument for the candidate density;
- Math- #207 (merged), #220 and #229: the elder window and densities in `d ≥ 2`.

The workflow binds #214 to its pinned blob through the repository API, with a drift gate:
- if #214 lands, the bytes must be identical, or this packet needs rebinding;
- the gate is evaluated when CI runs, so re-run CI before any merge.

## Controls

`d1p_check.py` uses the standard library: exact rationals for C1–C4 and C7, `Decimal` at 60 digits for C5, and float
quadrature, reported to 6 digits, for C6. Its output is `RESULTS.json`, byte-identical under `-O` and on CPython
3.10–3.14 (under a second).

| Control | Checks |
|---|---|
| C1 | The model's parity split; the edge functions `Γ_±` (slope `12` at `±1/3`, derivative `3(1 − φ²)²/(16φ⁴)`); `g''(X₃)`; the mirror symmetry `g(−X, −φ) = −1 − g(X, φ)` |
| C2 | The margins of Lemma W on `J_± = ±[1/3 − 1/100, 1/3 + 1/100]`, exactly, including the quadratic-growth factor `≥ 2.24` used by the envelope bound and `g'' ≥ 5.1` near `X₃` |
| C3 | The pin algebra of Lemma Φ as polynomial identities: the odd cubic and Hermite basis; the odd profiles `X(X² − ¼)²/120` and `X(X² − ¼)²(2X² + 1)/10080`; the even pin identity and profiles; `E₁ = a₄τ²/3 + ρ₁`. As scalar arithmetic: the leading regression constant `3`, and for the Gaussian kernel `E[a₅ | a₁ = 0, a₃ = α] = −10α`, hence `E_QO(3/2) → −6t²` |
| C4 | A bookkeeping check of the window-length identity (3.3): the even part cancels |
| C5 | (W.2)–(W.3) at 60 digits, for four perturbation shapes. The edge errors divided by (shape coefficient)² converge: to `±1/12` for the odd shape and `±3/4` for the even shape |
| C6 | Lemma E numerically, on a 16-point grid: `0 ≤ (G_θ − g_θ)/v₂ ≤ 2 min(1, s)`, and the small-`v₂` limits |
| C7 | The ledger. Checked: `(4/3)h^{3/4}`, by scaling and the exact antiderivatives; the band tail `37/49 ≥ 3/4`; integrability; the disjoint fold and cusp exponent sets. Recorded only: the heuristic `4/5` |

Mutants `M1`–`M7` each fail in their own control, and the workflow checks the failing control by name. An unknown or
bare label exits 2.

    python3 -B -S d1p_check.py                 # exit 0, output = RESULTS.json
    python3 -B -S d1p_check.py --mutant M4     # exit 1

C5 and C6 are numerical consistency checks. Lemmas E, Φ and W (including (W.1)), Proposition M and the assembly are proved
in prose only.

## Numerical evidence (exploration, outside the repository)

The model is the exact Gaussian-kernel process `e^{−x²/2}Σξ_nx^n/√(n!)`, with exact Matheron conditioning on the pins.
At fixed `s` (the cusp scale), the relative elder misclassification divided by `t²` is flat over
`t = 0.2, 0.1, 0.05, 0.025`:

| `s` | `t = 0.2` | `t = 0.1` | `t = 0.05` | `t = 0.025` |
|---|---|---|---|---|
| 2 | `−0.285` | `−0.274` | `−0.367` | `−0.272` |
| 1 | `+0.214` | `+0.222` | `+0.270` | `+0.266` |

The `s = 2` values carry `±0.018`–`0.036` and the `s = 1` values `±0.04`–`0.08`.

- A first-order term `∝ t` would grow these ratios eightfold.
- A referee's independent reduced leading-order model predicts the limits `+0.164` (`s = 1`) and `−0.308` (`s = 2`). The
  values for `t ≤ 0.1` are consistent with them (`χ² ≈ 3.7` and `4.7` on 3 degrees of freedom).
- For `t ∈ {0.1, 0.05}`, the interval structure of Lemma W matched a direct grid decision on all `3.3·10⁵` typed
  samples.

## Review record

Two clean-context same-family referees (Anthropic Claude subagents) reviewed the note before submission. Referee A took
§§0–3.1 and referee B took §§3.2–8, the controls, the workflow and this README. Each read the whole note against [D1] at
its pinned blob.

**First pass: both ACCEPT WITH MINOR FIXES; no MAJOR findings.** All findings are applied: seven minor, 18 nits and one remark. The
minor ones:
- (W.3) needs `Ê` even. The statement now gives the general form and the even case; `Ê` is even in Proposition M.
- The bad-event bound in Proposition M now carries the factor `(1 + s)` and the fourth-moment step.
- The dependency declaration now includes the intermediate estimates of #214's proof of Prop. 2.2 (c)–(d) that §2 reruns.
- The displayed bound `∫t^{−4}e^{−ct^{−2δ}} ≤ …` in Prop. 2.2⁺(a) now has its constant.
- §5.1's sharpness sentence is narrowed.
- C2 now checks the envelope's quadratic-growth constant.
- C7 now separates the checked items from the recorded ones.

Other changes:
- Lemma E is now unconditional (the trivial case `m² < 64v₂` is added), which removes the `t₁` bookkeeping.
- The window edges are renamed `φ±`, since `L` is the circle's length.
- The `|φ| > 2` typing case is spelled out, and `‖·‖_{C²}` is defined.
- §5.4 now gives exact conditional values and the correct sample count.
- The workflow now checks each mutant's failing control and the bare `--mutant`.

**Second pass (delta check of the revision): both ACCEPT.** The remaining nits were applied:
- the declaration of what the rerun estimates rest on;
- `§§0–5`;
- the bound `v₂ ≤ Cm²` cited in Proposition M's mean step;
- `E_Q[O(3/2)⁴]`;
- the renaming `φ_a → χ_a` in Lemma E;
- the attribution of `Γ₋ = −Γ₊(−·)` to C1;
- more test points for C2's quadratic-growth identity;
- §5.4's `χ²` scope and its sign-change sentence;
- the edge names in `RESULTS.json`;
- the workflow's path filter.

**The referees' independent checks.**
- *Replay.* Byte-identical on CPython 3.10–3.14 with and without `-O`; the mutant matrix is clean.
- *Lemma E.* Without cancellation, the sup of `(G − g)/(v₂ min(1, s))` is `1.5958 = 4/√(2π)` for `θ = 1` and `0.99994`
  for `θ = 1/3`.
- *Lemma Φ.* Exact conditioning at 140 digits for the Gaussian and mixture kernels, with all scalings bounded.
  `E_QO(3/2)/t² → −6`, `Ê(3/2)/t² → −13.2`, and `Cov(E₂, O(3/2))κ/t⁴ → 1/20`.
- *Prop. 2.2⁺ (c), at 45 digits.* The model remainder is `−0.0217h^{3/4}` (`θ = 1`) and `+0.0333h^{3/4}` (`θ = 1/3`).
  The `θ = 1/3` sign-kernel total is `0.0381h^{3/4}`, matching #214 §6.2. The new tail is `Θ(h^{37/49})`, and the old
  separate tails `Θ(h^{4/7})` cancel.
- *Lemma W.* The second-order coefficients `1/12` and `3/4` were derived by hand. (W.1) was tested by a direct
  decision: no mismatch in about `2.5·10⁵` typed decisions at `C²` norm `≤ 0.5`.
- *Workflow.* Run end to end with the API stubbed; a simulated advance of #214 trips the drift gate.

**Independence.** The referees are the same provider and the same GitHub account as the author, so they carry zero
organizational independence. Nonauthor review is required; the review slices are in PROOF §8.

## Not claimed

- the `h^{3/4}` coefficient, its sign, or the sharpness of `3/4`. #214 §6.2 records a `θ = 1/3` sign-kernel remainder
  `≈ 0.038h^{3/4}` for the Gaussian kernel, which is evidence about that integral only.
- anything in `d ≥ 2`. Whether the edge argument lifts to the elder density there is open (PROOF §5.3).
- uniformity in the covariance; anything on `R`.
