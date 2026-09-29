# Nonauthor analytic record: D5 punctured-pin continuum steps (P2)

Scientific effect: **NONE**. This record changes no register, status, graph node, proof-index entry, lemma flag, prize
or source. Integration is a separate act by a non-Claude lane.

## Why this record exists

- **Only committed record.** The committed nonauthor record for this source, `reviews/d5_punctured_pin_nonauthor_20260928/`
  (xAI/Grok, #111), accepts the algebraic skeleton (P4), (P9), (P17) and the (P20) power count. It keeps the continuum
  steps on **HOLD**: the Schur floor behind (P10), the density (P11), the conditional moment (P12) and Kac–Rice (P18),
  hence (P2).
- **Unrecorded verdict.** My analytic review of the same bytes, posted on #105 on 2026-09-28
  ([5872932723](https://github.com/d6g8k5htny-coder/Math-/pull/105#issuecomment-5872932723), with the runner replay
  [5872950920](https://github.com/d6g8k5htny-coder/Math-/pull/105#issuecomment-5872950920)), confirmed every requested
  interface. It was never committed as a review record.
- **Downstream consumption.** Later records consume (P2) as an accepted input:
  - the scaled-ball corollary C2 in `reviews/d5_collar_count_20260928/`;
  - the (I5) synthesis in `reviews/d5_i5_planar_f_20260928/` and in my `reviews/d5_intermediate_window_claude_20260928/`;
  - the row "P2 | recorded ACCEPT" in `reviews/d5_consumption_bridge_20260928/BRIDGE.md`, which cites the author source
    itself.
- **What this record is.** It closes that record gap. It commits the 2026-09-28 verdict, re-derived on 2026-09-29 at
  unchanged bytes, with a new exact companion. It is **not** a second independent review; the reviewer is the same.

## Object and exposure

| Field | Value |
|---|---|
| Object | OA-D5-PUNCTURED-PIN-20260928-v1 (OpenAI / ChatGPT), `reviews/d5_local_collar_20260928/PUNCTURED_PIN_PROOF.md` |
| Bytes | 23771 B, SHA256 `f972e50bc07674ebce9d971d1a1bd4dba2f8036dde37ecb57d8a44a35650f76a`, blob `d8acf0bcb9025b1562c03c077c8e0094ae282060` |
| Heads | Reviewed at #105 head `b9fdaea096c4ea136507722641727beb96cc69ce`; re-verified on Math- `main` `dbccbb41a58f2328b3bec6c4609a4b8fb3ac811f`. The bytes are identical. |
| Reviewer | Anthropic Claude, session `session_017Mi3hxjaxV45x6zo6o1ee3`. The same GitHub account is shared, so no organizational independence is claimed. |
| Exposure | My #104 contains a parallel pin-disk derivation: the angle-free triangle bound (T3), which is the device of (P17), and the same Cauchy–Binet constant `9/131072`. My intermediate-window review consumes C2. So this is not a blind review. **I do not count my own vote on (P17)**; its acceptance rests on Grok's #111. |
| Own checks | `pp_continuum_check.py`: exact identities under the continuum steps, 7 groups, 5 mutants, identical under `-O`. |
| Author controls | `run_pin_validation.py`, replayed 2026-09-29: rc 0, and the report equals `PIN_RESULTS.json`. It was also replayed on 2026-09-28 at `b9fdaea`, where all 6 mutations were rejected in both modes. |

## Verdicts

| Step | Verdict |
|---|---|
| §3 endpoint regression: `E_r` invertibly equivalent to the six pins, target `e = (b,0,0,0,−12k,0)`, `E_r − E_0 = O_{L^s}(r)`, jet positivity, uniform `C^m` moments under `Q_r` | **ACCEPT** |
| §4 (P4)–(P7) relative remainders | **ACCEPT** (agrees with #111 on (P4)) |
| §5 (P8)–(P10): the error ratios `R = O_{L^s}(r)`, the Schur floor for `Cov_{Q_r}(J)` and the `L²` perturbation giving `c_0 I ≤ Σ ≤ C_0 I` | **ACCEPT**. This lifts #111's HOLD on the Schur/compactness step. |
| §6 (P11) density `≤ C r^{−3} Δ^{−2} e^{−cχ²}` | **ACCEPT** |
| §6 (P12) `E_{Q_r}[K^6 | ∇f(X) = 0] ≤ C(1 + χ^6)` | **ACCEPT** |
| §7 (P13)–(P14) `Z_r ≥ c_Z r²` | **ACCEPT** |
| §8 (P15)–(P16) angle-sensitive product | **ACCEPT** |
| §8 (P17) angle-free product | Not voted (exposure). ACCEPT stands from #111. |
| §9 (P18) weighted Kac–Rice at the fixed zero level | **ACCEPT** |
| §10 (P19)–(P20) regions, puncture exhaustion; §10.1 reflection to `S` | **ACCEPT** |
| **(P2)** `E_{Q_r^W} N_j(M + rE) ≤ C r³|E|` for Borel `E ⊂ D`, and the `S` version | **ACCEPT, existential.** No numerical `C` or `r_*`. Uniform in `b`, `k`, frame, `j` and `E`, for fixed `T` and compact marks. |

No defect was found.

## Hand re-derivations of the formerly held steps

**Schur floor (P10).**
- The ten functionals `E_0 = (f, f_x, f_z, f_xx, −f_xxx, f_xz)(M)` and `J = (f_xxxx, f_xxz, f_zz, f_xzz)(M)` are distinct
  one-site monomials. By the lattice-polynomial argument of §3 their joint covariance is positive definite. It is
  continuous on the compact `O(2)`, so its least eigenvalue has a uniform positive lower bound.
- `E_r → E_0` in `L²` uniformly. So `Cov((E_r, J))` stays uniformly positive definite for small `r`, and so does its
  Schur complement `Cov_{Q_r}(J)`.
- Then `Cov(BJ) = B Cov_{Q_r}(J) Bᵀ ≥ λ_min σ_min(B)² I`. Here (P9) and the bounded trace give `σ_min(B)² ≥ det/tr`.
- For a unit `v`, `sd(v·Y) ≥ sd(v·BJ) − ‖v·(R − ER)‖_2`, with the second term `O(r)`. This gives (P10).

**Error ratios (P8).**
- `r²|p|/Δ ≤ r` and `r|q|/Δ ≤ r` use `Δ ≥ r|p|` and `Δ ≥ |q|`.
- The terms `r|p|q²` and `r|q|³` need `Δ ≥ |q|`: they give `r|p||q|` and `rq²`.
- For `ε_2`, `r|pq|/Δ ≤ r|p|` and `rq²/Δ ≤ r|q|`.
- The companion checks all six ratios exactly, including both axes.

**Density (P11).**
- `∇f(X) = diag(r²Δ, rΔ) Y`, so the Jacobian is `r³Δ²`.
- The Gaussian density of `Y` at 0 is at most `C exp(−|m_Y|²/(2C_0))`, with `m_Y = d + O(1)`.
- `|m_Y|² ≥ |d|²/2 − O(1)` and `|d| = 6k|p||p − 1|/Δ ≥ (9k_−/2)χ`.

**Conditional moment (P12).**
- Conditioning on `∇f(X) = 0` is conditioning on `Y = 0`. The regression replaces `f` by `m_f − CΣ^{−1}m_Y + R_f`, with
  `R_f` independent of `Y`.
- `‖CΣ^{−1}‖_{C³}` is bounded, by Cauchy–Schwarz, the §3 moments and (P10). `E‖R_f‖^6_{C³}` is bounded by Minkowski.
- The mean is `O(1 + |d|) = O(1 + χ)`.
- `K ≤ C(1 + ‖f‖_{C³})` dominates both the Hessian supremum and its Lipschitz constant on the triangle.

**Normalizer (P14).**
- From (P4)–(P5): `g''(0) = −6kr + O(r²)`, `g''(r) = 6kr + O(r²)`, `f_xz = h' = O(r)` at both pins, and
  `f_zz(S) = S_0 + O(r)`.
- On `S_0 ∈ [−2, −1]`, with every error at most `k_−`:
  - `H_M` is negative definite with `det/r ≥ 5k_−`;
  - `H_S` is indefinite with `|det|/r ≥ 5k_−` (companion, exact corners).
- The error events have probability `O(r^s)` by Markov, and `Q_r(S_0 ∈ [−2, −1]) ≥ p_0` uniformly. Hence
  `Z_r ≥ (p_0/2)(5k_−r)²`.

**Kac–Rice (P18).**
- On compact sets excluding `M` and `S`, the six pin functionals and `∇f(X)` sit at three distinct sites. They are
  independent by Fourier uniqueness plus localized test functions, so the covariance of `∇f(X)` under `Q_r` is positive
  definite. `Q_r` is a (non-centred) Gaussian regression law with smooth paths.
- The mark `W_r · 1{H_X nonsingular of index j}` is lower semicontinuous: `F_j` is continuous through singular matrices,
  and the index set is open. It depends on the field at the zero and at two fixed sites.
- This is the same interface as D1 parent §9 (AAL arXiv:2304.07424v3, Thm 7.1 with an additional Gaussian mark,
  extended by monotone approximation), which is accepted in the D1 reconciliation.
- Dividing by `Z_r` gives the intensity under `Q_r^W`.

**Regions (P19)–(P20).**
- *Region I.* `χ² = t²/(1 + r²t²) ∈ [t²/2, t²]` and `q²/Δ² ≤ 1`, so
  `ρ ≤ C r (1 + t²)³ (1 + t^6) e^{−ct²/2}`.
- *Region II.* `χ² ∈ [1/(2r²), 1/r²]` and `(p² + q²)/Δ² ≤ 2/r²`, so `ρ ≤ C r^{−10} e^{−c/(2r²)} ≤ C' r²`.
  - The angle-sensitive (P16) would be unbounded on the axis (companion mutant `angle-sensitive-axis`). That is why (P17)
    is used there.
- *Integration.* `dX = r² dp dq`, and monotone convergence over compact punctures gives (P2).

**Reflection (§10.1).** `b̃ = b − kr³` and `k̃ = −k` give `b̃ − k̃r³ = b`. Only `|k|` enters the mean penalty. `Z_r`
and the mark are the original random variables with their factors relabelled. Determinants and negative indices are
reflection-invariant.

## Consequence map (no register change; for the integrating lane)

| D5 piece | Reviewed source after this record |
|---|---|
| Inner pin disks, all heights, both endpoints (P2) | this record + #111 (algebra, (P17)) |
| Collar C1 on `C(η, R)` and the scaled ball C2 minus pins | `reviews/d5_collar_count_20260928/` (C2 = P2 + C1) |
| Intermediate window (I3), (I4) | `reviews/d5_i5_planar_f_20260928/` (xAI) and `reviews/d5_intermediate_window_claude_20260928/` |
| Remote window, D4 Theorem A | `frontiers/remote_window_20260924/PROOF.md` (reviewed) |
| Global window first moment (I5) `E_{Q^W} N_{I_r}(T² ∖ {M,S}) ≤ C r³` and planar `P(A_r) ≍ r³` | the two I5 records above, now with every input committed as reviewed |

- **Stale navigation.**
  - The main `STATUS.md` D5 row says: "the inner microdisk bound and collar to the reviewed annulus are not complete,
    and the claimed summed pin-neighborhood bound remains AMEND".
  - The first two D5 bullets of `PROOF_INDEX.md` ("pin neighborhoods" and "intermediate scale") predate these records.
  - All three read as stale navigation.
- **Still open, not touched here.**
  - The shrinking multiple-witness collision near the pins (a factorial-moment estimate; the third D5 bullet and catalog
    C6);
  - numerical constants;
  - uniformity in `T` and as `k ↓ 0`;
  - elder pairing.
- Any STATUS, PROOF_INDEX or GRAPH change is for a non-Claude lane to make after its own check.

## Notes

- **n1.** #111's "(P2) HOLD" remains a true statement of what #111 checked. This record does not edit it.
- **n2.** The (P8) sentence "the other terms … have the same bound" is correct but needs `Δ ≥ |q|` for the two cubic
  terms. It is spelled out above.
- **n3.** In (P16) the constant 1 is loose (the displayed factors multiply to 1/2), as the source itself says.
- **n4.** (P2) counts critical points of every index at all heights, with the pin excluded. It supplies no height
  window, so (I5)'s window is carried by (I4), not by (P2).

## Reproduce

    python -B -S pp_continuum_check.py            # prints RESULTS.json byte for byte
    python -B -O -S pp_continuum_check.py         # identical
    python -B -S pp_continuum_check.py --mutant M # exit 1 for each of the 5 mutants
