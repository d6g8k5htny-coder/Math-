# C7-total: a gap-mark-explicit failure intensity and the bounded unrestricted selection difference

**Object:** CL-C7-TOTAL-BOUNDED-20260929-v1.2 (v1.1 + the fixed-frame wording of the shifted-Gaussian step, see Revision history; v1.1 supersedes the withdrawn v1 memo CL-C7-TOTAL-K-SCALING-RECON-20260929-v1;
see `RECONNAISSANCE.md` for the retraction). **Author:** Anthropic Claude (session `session_01NMeKEismAyeqgdB4sy2NJU`).
**Disposition:** author-side proof candidate; **nonauthor analytic review required**. Scientific effect: NONE.

## 0. Statement of what is closed, and what is consumed

The C7 record (`reviews/c7_nonvanishing_openai_20260929/REVIEW.md` §5) leaves open the **order of the total
unrestricted rejected density** `ρ_rej(ℓ) := ν_cand^all(ℓ) − ν_eld^all(ℓ)` (known: `o(ℓ^{−1/3})`; far part `Θ(1)`) and
the **inverse-moment strip `q ∈ (−1, −2/3]`** of the rejected measure.

**Theorem K (gap-mark-explicit failure intensity).** In the setting of P §1 (fixed `d ≥ 2`, `L > 0`; law `Q_r =
Q_{r,b,k,R}`; typed weight `W_r`; cap region `G_r` of P §7), there are `r_0 > 0`, `N < ∞`, `C < ∞` depending on
`d, L` only, such that for every `b ∈ ℝ`, every `k > 0`, every frame, and `0 < r ≤ r_0`:

    (K1)   E_Q[W_r / r²]              ≤ C (k + r)² (1 + |b| + k)^N ;
    (K2)   E_Q[(W_r / r²) 1_{G_r^c}]  ≤ C (r³ / k) (1 + |b| + k)^N       whenever r ≤ min{k, r_0}.

No lower bound on the normalizer `Z_r` is used anywhere.

**Corollary T (C7-total).** For every fixed `d ≥ 2`, `L > 0`, as `ℓ ↓ 0`:

    (T1)  ν_cand^all(ℓ) − ν_eld^all(ℓ) = O(1)   (a version bounded on (0, ℓ_0]);
    (T2)  with Theorem U (far rejected density ≥ c_* > 0):  ν_cand^all − ν_eld^all = Θ(1);
    (T3)  the rejected measure ρ_rej(ℓ) dℓ satisfies  ∫_0^t ℓ^q ρ_rej(ℓ) dℓ < ∞  ⇔  q > −1.

So the unrestricted selection difference is bounded (the "no unrestricted `O(1)` conclusion" caveat of the C7
record is discharged), and the strip `(−1, −2/3]` lies entirely on the finite side for the rejected measure; the
candidate and elder measures individually keep the parent's threshold `−2/3`.

Consumed unchanged: P = `imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md` (blob `dfed3b8d…`)
with the reconciliation reading rule — §§1–5 (in particular (4.1), (4.3), (5.1), (5.2), (5.3)), §§6–7 verbatim
except where a bound is replaced as stated, §8, §§9–10 (the intensity identity), (13.2), (13.3), (14.1);
`frontiers/unrestricted_selection_difference_20260929/PROOF.md` (Theorem U). Nothing in those sources is
re-proved.

## 1. Where the parent loses `k`, and why it does not matter to the parent

P (6.1) bounds the axial entry by `|α_M| ≤ h/2 = M_3/2` (from (5.1)), although P (5.2) gives the sharper
`|α_M + 6k| ≤ rM_4/2`, i.e. `|α_M| ≤ 6k + rM_4/2`. On a compact gap window `k ≥ k_- > 0` the two are equivalent up to
constants, so the parent loses nothing. As `k ↓ 0` the difference is a factor `k²` in the weight — the same `k²`
that appears in the normalizer `z_0 = (6k)² E[det(A_0)² 1{A_0 < 0}]` (P (5.4)) and produces the `k^{4/3}` of the (15.2)
gamma integral. Theorem K is P §§6–7 with that factor kept and with the constant `D = 4K²/(3k)` of (7.1) tracked.

## 2. Proof of (K1)

By the pin identity P (5.3), for `i ∈ {M, S}`,
`|det H_i| / r ≤ |α_i| |det A_i| + r ‖β_i‖² ‖adj A_i‖`. Use (5.2) for `α_i`, (5.1) for `β_i`, and `‖A_i‖ ≤ M_2`,
`|det A_i| ≤ M_2^m`, `‖adj A_i‖ ≤ M_2^{m−1}` (`m = d − 1`, `M_j` the local `C^j` seminorms of P §4):

    |det H_i| / r ≤ (6k + rM_4/2) M_2^m + (r M_3²/4) M_2^{m−1} ≤ C (k + r) (1 + ‖f‖_{C⁴})^{m+2}.

Hence `W_r / r² ≤ C (k + r)² (1 + ‖f‖_{C⁴})^{2m+4}`. P (4.1) holds for every derivative order `q` and every finite
`p`; its target-growth version P (13.3) is stated for `C³` but its proof ("the same summability/Minkowski proof as
Section 4") uses only the summable Fourier weights and the regression-mean bound `C|v_r|`, hence applies verbatim
to `C⁴`: `E_Q (1 + ‖f‖_{C⁴})^p ≤ C_p (1 + |b| + k)^p` uniformly for `r ≤ r_0` and all frames. Taking
`p = 2m + 4` gives (K1). ∎

## 3. Proof of (K2)

Work on the typed support with `B = −A_M ≻ 0`, eigenvalues `0 < λ_1 ≤ … ≤ λ_m = Λ`, `h = M_3`. Two of the parent's
§7 inputs are stated there for compact `B × K` only and must be replaced by their polynomial-growth versions before
`b` and `k` are unrestricted (P §13 itself warns against "the compact-target bound (4.1) applied outside its scope"):

- **(4.3) with growth.** In the regression decomposition P (4.2), `f = μ_r + B_r·(A_r − E_Q A_r) + g_r`, the mean
  `μ_r` is linear in the target, so `‖μ_r‖_{C⁴} ≤ C |v_r| ≤ C(|b| + k)`, and likewise `‖E_Q A_r‖ ≤ C(|b| + k)`;
  `B_r` and `g_r` are as in P §4 (target-independent). Hence `M_3, M_4 ≤ K_0 (J_r + ‖A_r‖_F) + C(|b| + k)`. Put
  `U := J_r + ‖A_r‖_F + |b| + k ≥ 1`; then `h, M_4 ≤ K U` with `K` depending on `d, L` only.
- **(3.5)/(7.2) with a shifted center.** The `Q`-density of `A_r` is Gaussian with covariance uniformly bounded
  above and below (P §3) and mean `m_A = E_Q A_r`, `‖m_A‖_F ≤ C(|b| + k)`: `density_Q(A) ≤ C_0 exp(−c_0 ‖A − m_A‖_F²)`.
  The eigenvalue integration is performed **after fixing the orthogonal frame**: write `B = −A = O diag(λ) O^T`
  and, for fixed `O`, `‖A − m_A‖_F² = ‖diag(λ) + O^T m_A O‖_F² = Σ_i (λ_i + q_i)² + (fixed off-diagonal squares)`,
  `q = diag(O^T m_A O)`, `|q_i| ≤ ‖m_A‖`. The Gaussian factor in `λ_1` is dropped on the layer (as in P §7); the
  remaining `λ_2, …, λ_m` integrals are one-dimensional *shifted* Gaussian polynomial moments, `∫ λ^p e^{−c_0(λ+q)²}dλ
  ≤ C_p (1 + |q|)^p`, hence polynomial in `‖m_A‖ ≤ C(|b| + k)`, uniformly over the compact `O`; the Vandermonde has
  already been replaced by the nonnegative polynomial `Λ^{m(m−1)/2}`, and the Haar integral over `O` is then taken.
  This replaces P's centered `e^{−c Σ λ_j²}` without any `exp(C‖m_A‖²)` loss, and it does **not** assert that the
  shifted matrix law is orthogonally invariant — only the centered covariance bound is.

With these two replacements, P §7 runs verbatim.

**(6.2′) — the weight bound with the axial entries at their true size.** Write `a := 6k + rM_4/2 ≤ 6k + rKU/2`, so
that `|α_M|, |α_S| ≤ a` by P (5.2). P's canceled-pivot argument for (6.1) reads `|det H_M| ≤ r |α_M| det B`
(the Schur complement `B − (r/|α_M|) β β^T ≻ 0` and determinant monotonicity); it does not depend on how `|α_M|` is
bounded afterwards, so `|det H_M| ≤ r a λ_1 ∏_{j≥2} λ_j`. For the saddle there is **no** (5.2)-type improvement of
the mixed term: P's derivation of the second line of (6.2) uses `|α_S| ≤ h/2` *and* `‖β_S‖² ≤ h²/4` (from (5.1)),
and only the first of these sharpens. Keeping the second as it is,

    |det H_S| ≤ r [ a (λ_1 + rh) + r h²/4 ] ∏_{j≥2} (λ_j + rh),

and therefore

    W_r ≤ r² a · λ_1 [ a λ_1 + a r K U + r K² U² / 4 ] · ∏_{j≥2} λ_j (λ_j + r K U).                (6.2′)

(At `a = h/2` this is P's (6.2) exactly: `(h/2)[λ_1 + rh] + rh²/4 = (h/2)[λ_1 + (3/2) rh]`.)

**The failure set.** P §7: `G_r^c ⊂ {λ_1 ≤ D r U²} ∪ {r M_4 > 3k/10}` with `D = 4K²/(3k)` (P (7.1)), and for
`m = 1` the additional far branch `{λ > 1/(4Dr)}` of P (7.5).

**Depth failure, `m ≥ 2`.** The layer integral of the `λ_1`-bracket of (6.2′) is exact (checker):

    ∫_0^{DrU²} λ_1 [ a λ_1 + a r K U + r K² U²/4 ] dλ_1 = r³ U⁵ [ a D³ U / 3 + a K D² / 2 + K² D² U / 8 ].

With `D = 4K²/(3k)`: `D³ ∝ k^{−3}`, `D² ∝ k^{−2}`. Insert (6.2′) into the eigenvalue measure (P (7.2), shifted
version above) and integrate `λ_1` first, as in P (7.4); every other factor is bounded as there. Collecting the
`a`-dependence, and using `a ≤ 6k + rKU/2`, the numerator is

    E_Q[W_r 1_{depth}] ≤ C r⁵ E∫ [ a² k^{−3} + a² k^{−2} + a k^{−2} ] U^{2m+6} Λ^{m(m−1)/2} (shifted Gaussian) dλ_2 … dλ_m .

Now `a² ≤ 72k² + r²K²U²/2` gives `a² k^{−3} ≤ C k^{−3}(k² + r²) U²`, `a² k^{−2} ≤ C k^{−3}(k² + r²) U²` for `k ≤ 1`,
and `a k^{−2} ≤ C (k + rU) k^{−2} ≤ C k^{−3}(k² + r²) U` since `r k^{−2} ≤ (k^{−1} + r² k^{−3})/2` (AM–GM). Moments
are polynomial in `(1 + |b| + k)` by the fixed-frame shifted-Gaussian step above and the `C⁴` moment of §2. So

    E_Q[W_r 1_{depth}] ≤ C r⁵ k^{−3} (k² + r²) (1 + |b| + k)^N          (k ≤ 1),

and for `r ≤ k`: `E_Q[(W_r/r²) 1_{depth}] ≤ C (r³/k)(1 + |b| + k)^N`. For `k ≥ 1`, `D ≤ 4K²/3` and `a ≤ C(k + r)U`,
so `E_Q[W_r 1_{depth}] ≤ C r⁵ (k + r)² (1 + |b| + k)^N ≤ C r⁵ k^{-1} (1 + |b| + k)^{N+3}` — the same form with a
larger `N`; henceforth `N` denotes the larger exponent.

**`m = 1`.** P (7.5): depth failure is contained in `{λ ≤ 4DrJ_r²} ∪ {λ > 1/(4Dr)}` (with `U` as redefined above). The
near branch gives the same `r⁵ k^{−3}(k² + r²)` numerator by direct integration of the bracket of (6.2′) in `λ`
(P's `C r⁵ E J_r^{10}` with the axial factor kept and the `r h²/4` mixed term retained, as above). The far branch, by P (7.6) with the weight bounded as in §2,
`E_Q[(W_r/r²) 1_{far}] ≤ (4Dr)⁴ E_Q[(W_r/r²) λ⁴] ≤ C (r/k)⁴ (k + r)² (1 + |b| + k)^N`, and for `r ≤ k` this is
`≤ 4C (r/k)⁴ k² = 4C (r³/k)(r/k) ≤ 4C r³/k` (times the polynomial).

**The fourth-derivative exception.** P (7.7) with the weight of §2:
`E_Q[(W_r/r²) 1{rM_4 > 3k/10}] ≤ (10r/(3k))⁴ E_Q[(W_r/r²) M_4⁴] ≤ C (r/k)⁴ (k + r)² (1 + |b| + k)^N ≤ 4C r³/k`
for `r ≤ k`, as above.

Summing the pieces gives (K2) for `r ≤ min{k, r_0}`. No division by `Z_r` occurred, and no compact-window
constant was used outside its scope. ∎

**Remark (normalized form).** On compact `b`-sets, P (5.4)–(5.5) made `k`-explicit — `z_0 ∝ k²` and the
convergence `Z_r/r² → z_0` uniform for `r ≤ ck` because the relative error in (5.2) is `rM_4/(12k)` — turn (K2) into
`1 − p_r ≤ Q^W(G_r^c) ≤ C_B (r/k)³` for `r ≤ ck`. Corollary T does not use this.

## 4. Proof of Corollary T

**The rejected intensity identity.** P §§9–10 disintegrate the marked Kac–Rice measure into the pin density
times `E_Q[W_r e]` for the elder mark `e` and `E_Q[W_r]` for candidates. Applying the same disintegration to the
mark `1 − e` (Borel, bounded), the per-volume rejected intensity is `r A_r (1 − p_r) dr db dk dσ` with

    A_r (1 − p_r) = 12 π_r(v_r) · E_Q[(W_r/r²)(1 − e)],

and on the generic locus `1 − e ≤ 1_{G_r^c}` because on `G_r` the global elder partner of `M` is `S` (P §8). With
the change of variables P (11.1) and the near/far split of P §§13–14,

    ρ_rej^near(ℓ) = ℓ^{−1/3} ∫∫∫ 1{k ≥ ℓ/r_0³} · 12 π_r(v_r) E_Q[(W_r/r²)(1 − e)] / (3 k^{2/3}) db dk dσ(u),   r = (ℓ/k)^{1/3},

with `π_r(v_r) ≤ C e^{−c(b² + k²)}` by P (13.2) (target-free covariance band, `r ≤ r_0`).

**Split at `k_* = ℓ^{1/4}`** (equivalently `r = k`, since `r³ = ℓ/k`).

- `k ≥ k_*` (so `r ≤ k`): by (K2), the integrand is at most
  `C (ℓ/k²) k^{−2/3} (1 + |b| + k)^N e^{−c(b² + k²)}`; the `b`-integral is finite and the `k`-integral is
  `≤ C ℓ ∫_{k_*}^∞ k^{−8/3} dk = (3/5) C ℓ k_*^{−5/3} = C′ ℓ^{7/12}`.
- `ℓ/r_0³ ≤ k < k_*` (so `r > k`): by (K1), `(k + r)² ≤ 2k² + 2r² = 2k² + 2(ℓ/k)^{2/3}`; the `k`-integrals are
  `∫_0^{k_*} k^{4/3} dk = (3/7) k_*^{7/3} = C ℓ^{7/12}` and
  `ℓ^{2/3} ∫_{ℓ/r_0³}^{k_*} k^{−4/3} dk ≤ 3 ℓ^{2/3} (ℓ/r_0³)^{−1/3} = 3 r_0 ℓ^{1/3}`.

Hence `ρ_rej^near(ℓ) ≤ ℓ^{−1/3} [ C ℓ^{7/12} + C r_0 ℓ^{1/3} ] = C ℓ^{1/4} + C r_0`. The far part is
`ρ_rej^far ≤ ν_cand^far ≤ C` by P (14.1). This proves (T1). (T2) is Theorem U's lower constant on the far part.
(T3): a density that is bounded above near `0` (T1) and bounded below by a positive constant (T2) has
`∫_0^t ℓ^q dℓ`-type moments finite exactly for `q > −1`. ∎

**Remark (what the `O(1)` is made of).** The `C r_0` term comes from separations `r ∈ [k, r_0]` with tiny gap
marks `k ~ ℓ/r³` — pairs at macroscopic separation whose height gap happens to be `ℓ`. These behave like far
pairs (Theorem U's mechanism), the near/far cutoff `r_0` is arbitrary, and (T1)'s constant is not a rate. The
genuinely near part (`r ≤ k`) is `O(ℓ^{1/4})`, i.e. rejection is *rarer* than `ℓ^{2/3}`-scale only in the
compact-window sense; on the unrestricted population the far pairs dominate the rejected measure.

## 5. What is new relative to the parent, and what is not claimed

New: (K1) is a sharper majorant than P (13.4) by the factor `(k + r)²`, obtained from (5.2) instead of (5.1); (K2)
is P §7 with `k` tracked. Everything else is the parent's own machinery. Not claimed: any numerical constant; any
rate for `ν_cand` or `ν_eld` individually; any change to the parent's existential scope or to Theorem A's compact
formulation; any statement about the *selected* measure's threshold (still `−2/3`); nonauthor acceptance.

## Revision history

- v1 (withdrawn): `RECONNAISSANCE.md` retraction; the `ℓ^{−1/4}` conjecture is not revived.
- v1.1 (2026-09-29, blob `1fe08e2a…`): Theorem K / Corollary T with the saddle mixed term retained.
- v1.2 (2026-09-29): the shifted-Gaussian eigenvalue integration in §3 is now stated explicitly as performed after
  fixing the orthogonal frame `O` (separable shifted one-dimensional moments, uniform over compact `O`, Haar integral
  last), as recommended in the OpenAI reviews
  [5357773376](https://github.com/d6g8k5htny-coder/Math-/pull/150#pullrequestreview-5357773376) and
  [5358141048](https://github.com/d6g8k5htny-coder/Math-/pull/150#pullrequestreview-5358141048). Wording only; no
  theorem, constant or checker change; `RESULTS.json` bytes unchanged.

## 6. Review requested (non-Claude lane)

(i) that P's canceled-pivot step (6.1) admits the `k`-dependent axial bound (5.2), and that the saddle bound keeps
the `r h²/4` mixed term — the v1.1 draft had wrongly sharpened it, caught in an author-side adversarial pass;
(ii) the `C³ → C⁴` extension of (13.3) and the polynomial-growth versions of (4.3) and (7.2) used for unrestricted
`b`; (iii) the `k`-tracked three-term layer integral and (7.5)–(7.7) arithmetic (exact in the checker);
(iv) the rejected-intensity identity with mark `1 − e ≤ 1_{G_r^c}`; (v) the piecewise integrals of §4 (checker).
**OpenAI** (parent author) is the natural lane for (i)–(iii); any lane for (iv)–(v).

## Reproduce

    python -B -S exponent_check.py            # prints RESULTS.json byte for byte; -O identical
    python -B -S exponent_check.py --mutant M # exit 1 for M in {M1, M2, M3}
