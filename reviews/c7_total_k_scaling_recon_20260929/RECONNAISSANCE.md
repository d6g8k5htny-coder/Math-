# Reconnaissance memo — C7-total: the gap-mark scaling of selection failure and the `ℓ^{−1/4}` conjecture — 2026-09-29

**Object:** CL-C7-TOTAL-K-SCALING-RECON-20260929-v1. **Author:** Anthropic Claude (session `session_01NMeKEismAyeqgdB4sy2NJU`).
**Scientific effect:** NONE. **This memo proves nothing.** It records a
scaling analysis of the parent's own proof with the gap mark `k` tracked, states the conjecture it points to, and lists
the exact proof obligations, so that a lane attacking C7-total attacks the right object.

## 1. The open question, as the C7 record leaves it

`reviews/c7_nonvanishing_openai_20260929/REVIEW.md` §5: far rejected pairs have density `Θ(1)` (Theorem U lower, parent
(14.1) upper); the **total** unrestricted rejected density `ρ_rej(ℓ) := ν_cand^all(ℓ) − ν_eld^all(ℓ)` is known only to be
`o(ℓ^{−1/3})`; the inverse-moment strip `q ∈ (−1, −2/3]` for the rejected measure is unresolved; "no unrestricted `O(1)`
conclusion follows."

## 2. Where the near rejected density comes from

By the parent's (13.5) applied to the candidate/elder difference (`1 − p_r` in place of `p_r`), with `r = (ℓ/k)^{1/3}`,

    ρ_rej^near(ℓ) = ℓ^{−1/3} ∫_{ℝ×(0,∞)×S^{d−1}} 1{k ≥ ℓ/r_0³} [1 − p_r(b,k,u)] A_r(b,k,u) / (3k^{2/3}) db dk dσ(u).

Everything is in how `1 − p_r` depends on `k` as `k ↓ 0`. The parent's Theorem A is stated for compact `K ⊂ (0,∞)` and
deliberately never tracks `k` (P §13: "Do NOT require … a globally uniform constant in (1.1)").

## 3. Tracking `k` through P §§5–7: the selection bound is `min{1, (r/k)³}`, heuristically

Read P §7 with `k` explicit:

- The cap region is `G_r = {λ_min(−A_M) > (4/(3k)) r M_3², rM_4 ≤ 3k/10}`. So depth failure is the layer
  `0 < λ_1 ≤ D r U²` with `D = 4K²/(3k)` (P (7.1)): **the layer width is `∝ r/k`**.
- P (7.3) integrates the soft factor over that layer: `∫_0^{DrU²} λ_1(λ_1 + ErU) dλ_1 ≍ (Dr)³ ≍ (r/k)³` (times moments of
  `U`). Combined with the `r²` from the other factors, the numerator `E_Q[W_r 1_{fail}]` is `≍ r² (r/k)³` — **if** the
  axial factors are kept at their true size.
- P (6.1)–(6.2) bound `|α_M|, |α_S|` by `h/2 = M_3/2` (canceled-pivot). But P (5.2) says `α_M ≈ −6k`, `α_S ≈ 6k` when
  `rM_4 ≪ k`. Bounding `6k` by `M_3/2` loses a factor `k²` in the numerator that the denominator does not lose:
  P (5.4) gives `Z_r/r² → z_0 = (6k)² E[det(A_0)² 1{A_0<0}]`, i.e. **`Z_r ≍ k² r²`**. With the true axial size the `k²`
  cancels between numerator and normalizer; with the canceled-pivot bound it does not.
- The fourth-derivative exception P (7.7) is `[10r/(3k)]⁴ E[(W/r²) M_4⁴] ≍ (r/k)⁴`, subdominant to `(r/k)³` for `r < k`.

Heuristic conclusion (H): `1 − p_r(b,k,u) ≲ C min{1, (r/k)³} · (1 + |b| + k)^N` uniformly, for `r ≤ r_0`.
For `k` in a compact window this is the parent's `C r³`; the new content is the `k^{−3}` growth as `k ↓ 0` and the
saturation at `r ≍ k`. Physically: the whole cubic pair landscape `G_k` is `O(k)` in scaled units (every term of
`G_k` carries `k`), while third-order fluctuations are `O(1)`; when `k ≪ 1` the pairing survives only if the
transverse curvature beats the fluctuation, `λ_1 ≳ rM_3²/k`.

## 4. Consequence if (H) holds: `ρ_rej(ℓ) = O(ℓ^{−1/4})`, and the strip splits at `−3/4`

Insert (H) into §2 with the parent's majorant `H(b,k)` (P (13.4)) and `r³ = ℓ/k`, so `(r/k)³ = ℓ/k⁴`:

    ρ_rej^near(ℓ) ≲ ℓ^{−1/3} ∫_{ℓ/r_0³}^{∞} min{1, ℓ/k⁴} k^{−2/3} H̃(k) dk.

The threshold is `k_* = ℓ^{1/4}`. Below it (`ℓ/r_0³ ≤ k ≤ ℓ^{1/4}`) the integrand is `k^{−2/3}` and the integral is
`≍ k_*^{1/3} = ℓ^{1/12}`; above it the integral is `ℓ ∫_{k_*}^∞ k^{−14/3} dk ≍ ℓ · k_*^{−11/3} = ℓ^{1/12}`. Hence

    ρ_rej^near(ℓ) = O(ℓ^{−1/3 + 1/12}) = O(ℓ^{−1/4}),

and with the far part `Θ(1)`: **`ρ_rej(ℓ) = O(ℓ^{−1/4})`**. The rejected measure then has finite inverse moments
`∫ ℓ^q ρ_rej dℓ` for **`q > −3/4`**, narrowing the unresolved strip from `(−1, −2/3]` to `(−1, −3/4]` on the upper side.
(Checker `exponent_check.py` verifies the threshold algebra and both piecewise integrals exactly, and the contrast
scenario: a `k`-uniform `C r³` would give `ρ_rej^near = O(1)` and threshold `q > −1`.)

## 5. Conjecture, and why the every-`d` lower-bound event does *not* settle it

**Conjecture C7-τ.** `ρ_rej(ℓ) ≍ ℓ^{−1/4}` as `ℓ ↓ 0`, in every fixed `d ≥ 2`; the rejected measure's inverse-moment
threshold is exactly `q = −3/4`; in particular the unrestricted difference is **not** `O(1)`.

The upper half is §4 given (H). The lower half needs a small-`k` failure mechanism of the right size. The direct
lower-bound events of the planar record and of PR #149 (soft eigenvalue pinned at `(3k/2) r`, third-order jets pinned
within `εk` of `O(k)` targets) have mass `∝ k⁴ r`, weight `∝ k⁴ r⁴`, normalizer `∝ k² r²`: they yield only
`1 − p_r ≥ c k⁶ r³` — a specific `O(k)`-geometry event that becomes rare as `k ↓ 0`. The conjectured dominant
mechanism is different: a soft eigenvalue at the **larger** scale `λ_1 ≍ rM_3²/k` with `O(1)` third derivatives
(mass `∝ r/k`, weight `∝ r⁴` with `k` cancelling in `6kr · (r/k)`, normalizer `∝ k²r²`, ledger `(r/k)³`). Proving
pairing fails with probability bounded below on that layer is the open obligation.

## 6. Proof obligations (ordered; each is a bounded task)

1. **k-explicit Theorem A (upper).** Re-run P §§5–7 keeping `|α_i| = 6k(1 + O(rM_4/k))` (not `M_3/2`) in (6.1)–(6.2),
   `D = 4K²/(3k)` in (7.1)–(7.4), the `(r/k)⁴` term (7.7), and `Z_r ≥ z_* k² r²` from (5.4)–(5.5) with the `k²`
   made explicit. Expected output: `1 − p_r ≤ C min{1, (r/k)³}(1 + |b| + k)^N e^{−c(b² + k²)}`-type bound on
   `r ≤ r_0`, with the `b`-tail from P (13.2)–(13.3). This alone upgrades `o(ℓ^{−1/3})` to `O(ℓ^{−1/4})`.
2. **k-explicit lower bound.** A failure event on the layer `λ_1 ≍ rM_3²/k` with `Q^W`-mass `≥ c (r/k)³` for
   `r ≤ ck`; the polygonal-path method should adapt with a model in which the third-order term dominates the
   cubic, but the margins are no longer `O(k)`.
3. **Assembly.** DCT is not needed for the upper bound (it is an integral of a majorant); for the lower bound one
   needs `A_r ≥ c > 0` on a positive-measure `k`-range near `k_*`, which P (10.3) gives on compacts only — a small
   extension to `k ↓ 0` at fixed `b` is required (the `k²` in `z_0` is the only degeneracy).

## 7. What this memo is not

Not a theorem, not a review verdict, not a register change. Consistent with every accepted statement: the compact-
window `Θ(ℓ^{2/3})` loss (unchanged), Theorem U's far `Θ(1)` (unchanged), and `o(ℓ^{−1/3})` (implied by `O(ℓ^{−1/4})`).
It contradicts nothing in tree; it sharpens the open question's expected answer and names the exact steps.

## Reproduce

    python -B -S exponent_check.py            # prints RESULTS.json byte for byte; -O identical
    python -B -S exponent_check.py --mutant M # exit 1 for M in {M1, M2}
