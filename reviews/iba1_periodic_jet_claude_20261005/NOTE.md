# Exact-periodic contact-jet covariances and measured anisotropy

Object: `CL-IBA1-ITEM2-PERIODIC-JET-20261005-v1`. Author: Anthropic Claude, session `017Mi3hx…` (Dylan Roy — delegated AI work).
Scientific effect: **NONE**. No proof, status, register, catalog, PROOF_INDEX, GRAPH or `formal/` surface is touched.

## Scope

This packet carries out item 2 of "Remaining work and falsification experiments" in the first independent audit,
[main#252](https://github.com/d6g8k5htny-coder/main/issues/252) (IBA-20261003-P1):

> Independently implement exact-periodic derivative tensors and conditional covariance Schur complements for several
> directions in d=2,3,4; check positivity and explicitly measure anisotropy. Use image sums or spectral sums with
> controlled tails, not an isotropic surrogate.

It also evaluates P's coefficient formula (15.2) in `d = 2` by directional quadrature (part of item 3). At `L = 24` the value
is checked against the published enclosure of `coefficients/side24_v1`; at smaller `L` it is reported as a diagnostic.
The disposition map for the audit is [main#252 comment 6001303987](https://github.com/d6g8k5htny-coder/main/issues/252#issuecomment-6001303987).

The field is P's: centred, variance one, with the exact normalized periodized covariance

    K_L(z) = sum_{n in Z^d} exp(-|z + L n|^2 / 2) / sum_{n in Z^d} exp(-|L n|^2 / 2).

## Method

1. **Product structure.** `exp(-|z|^2/2)` factorizes over coordinates, so the image sum does too:
   `K_L(z) = prod_i q_L(z_i)` with `q_L(t) = theta_L(t)/theta_L(0)` and `theta_L(t) = sum_n exp(-(t + L n)^2/2)`.
   Every derivative tensor of `K_L` at `0` is therefore the moment tensor of a spectral law with independent coordinates,
   determined by `q2 = q_L''(0)`, `q4 = q_L''''(0)` and `q6 = q_L^(6)(0)`. No isotropy is assumed.
2. **Image sums with a controlled tail.** `theta_L^(j)(0) = sum_n He_j(L n) exp(-(L n)^2/2)` for `j = 0, 2, 4, 6`.
   The sum is truncated once `(L n)^2/2` exceeds the working precision, and the two-sided tail is bounded by
   `8 x^6 exp(-x^2/2)` at the first omitted node `x ≥ 10`. That bound is recorded per `L`, and is at most `3.93e-373` (at `L = 3`).
3. **Moments from cumulants.** With `m2 = -q2`, `m4 = q4`, `m6 = -q6`, the cumulants are `k2 = m2`,
   `k4 = m4 - 3 m2^2` and `k6 = m6 - 15 m4 m2 + 30 m2^3`. Then `E[prod <xi, v_k>]` is the sum over partitions into
   even blocks: `k2 <v_a, v_b>` for a pair, and `k_{2j} sum_i prod v_{k,i}` for a block of size 4 or 6. Finally
   `Cov(d_A f, d_B f) = (-1)^|B| (-1)^((|A|+|B|)/2) E[prod <xi, v>]`.
4. **The contact jet in a frame `(u, w_1, …, w_m)`.**
   - Odd block: `G = grad f` and `t_u = d_u^3 f`.
   - Even block: `f`, `V_u = H u` and the transverse block `A_u`.
   - Schur complements: `tau_u^2 = Var(t_u | G = 0)` and `Sigma_{A|V} = Cov(A_u | V_u = 0)`.
   - Positivity: the Cholesky pivots of the odd block, the even block and `Sigma_{A|V}`.
5. **Anisotropy.** For `det Cov(G)`, `det Cov(V_u)`, `tau_u^2`, `det Sigma_{A|V}` and `tr Sigma_{A|V}`, take the largest
   relative deviation over the tested directions from the value at `e_1`. Here `tr` is the Frobenius trace of the
   conditional covariance of `A_u` as a symmetric matrix: the diagonal variances plus twice the off-diagonal ones. The directions are:
   - `d = 2`: 16 equally spaced;
   - `d = 3`: 10 (the axes, the face and body diagonals, and three generic directions);
   - `d = 4`: 8.

   These quantities do not depend on the choice of transverse frame. Check R6 verifies this at fixed `u`. The raw
   upper-triangle sum of variances, used in the first revision, is frame-dependent for `d ≥ 3` (finding PJ-A-001,
   below).
6. **`d = 2` coefficient.** In (15.2), `A_u` is a centred scalar normal, so `D_u = Sigma_{A|V}/2`. The angular integral
   uses the trapezoid rule, which converges geometrically for this smooth periodic integrand.

Arithmetic: Python `decimal` at 270 significant digits. This is floating, not interval, arithmetic: see the limits below.

## Results (`RESULTS.json`)

| `L` | `k4/k2^2` | max relative anisotropy, `d = 2 / 3 / 4` | smallest Cholesky pivot |
|---|---|---|---|
| 24 | `5.6e-120` | `4.0e-118` / `4.7e-118` / `4.9e-118` | `1.0` |
| 8 | `1.0e-10` | `7.5e-10` / `8.8e-10` / `9.2e-10` | `1.0` |
| `2π` | `8.3e-6` | `3.5e-5` / `4.0e-5` / `4.2e-5` | `0.9999996` |
| 4 | `0.175` | `0.283` / `0.311` / `0.312` | `0.979` |
| 3 | `2.54` | `6.20` / `6.20` / `6.20` | `0.647` |

`d = 2` coefficient (15.2):
- reference (nonperiodic contact covariance): `c_2 = 0.0734069193060342710301359629577740500177…`;
- `L = 24`: relative difference from the reference `-2.2e-118`, on 8 and on 16 directions. Both values lie inside
  `side24_v1`'s published interval `(0.07340691930603427103, 0.07340691930603427104)`;
- smaller `L` (diagnostic; 256 and 512 directions agree to `< 1e-26`): `c_{2,L} / c_2` is `0.999999999615` at `L = 8`,
  `0.999983180835` at `L = 2π`, `0.920467147230` at `L = 4` and `0.679492248662` at `L = 3`.

## What this shows

- Every conditional covariance is positive definite in every tested direction, at every tested `L`. This is consistent
  with P §2's finite-jet rank, which holds for every `L > 0`.
- At `L = 24` the anisotropy is nonzero and measured, at about `4e-118` relative. That is about twelve orders of magnitude
  below `side24_v1`'s periodization bound of `1e-106`, and consistent with it. This is a floating-point consistency
  check, not an independent proof of that bound. The isotropic reference value of `c_{2,24}` agrees far beyond its 20
  published digits.
- At smaller `L` the anisotropy is material: 31% at `L = 4`, and a factor of about 7 in `tau_u^2` at `L = 3`. An isotropic
  surrogate would be wrong there, as the audit warned; the mutant M1 shows it.

## What this does not show

- The arithmetic is floating `decimal`, not interval. The `L = 24` values are checked against the published enclosure, but
  the smaller-`L` values are diagnostics, not certified enclosures.
- The anisotropy is a maximum over finitely many directions, so it is a lower bound on the supremum over the sphere. In
  `d = 2` the 16 directions include the extremes `ψ = 0` and `ψ = π/4`.
- `d = 3, 4` coefficients are not evaluated: `D_u` for a non-scalar `A_u` needs a cone integral.
- `Γ(7/6)` comes from a Stirling series with shift 200 and is accurate to about `1e-108` relative, not to the full 270
  digits. That accuracy is ample for every stated number, since the prefactor cancels in every ratio. R4's `1e-100`
  equality compares two outputs of the same code; the external anchors are `side24_v1`'s interval and its closed form.
- Nothing here bears on the lifetime theorem itself; (15.2) is imported from P (blob `dfed3b8d`).

## Checks and mutants

`periodic_jet_check.py` asserts:
- **R1**: the nonperiodic reference reproduces `side24_v1` §1. That means `Cov G = I`, `det Cov V = 3`, `tau^2 = 6`,
  `Sigma_{A|V} = 8/3` in `d = 2`, and Frobenius trace `8/3 + 8/3 + 2·1 = 22/3` in `d = 3`.
- **R2**: positivity for every `L` and `d`.
- **R3**: the `L = 24` anisotropy lies in `(1e-130, 1e-106)`, and the `L = 4` anisotropy exceeds `1e-3`.
- **R4**: `c_{2,24}` lies in `side24_v1`'s interval and equals the reference to `1e-100`.
- **R5**: the small-`L` quadrature has settled to `1e-12` relative.
- **R6**: at `u = e_1` and `L = 4`, rotating the transverse frame by `(cos, sin) = (3/5, 4/5)` changes none of the five
  invariants (`d = 3, 4`; changes `≤ 1e-268`).

The mutants must fail (exit 1):
- **M1**: an isotropic surrogate for the fourth- and sixth-order tensors (fails R3);
- **M2**: the transverse block not conditioned on `V = 0` (fails R1 and R4);
- **M3**: the (15.2) prefactor divided by 12 (fails R4);
- **M4**: the raw upper-triangle trace (fails R1 and R6).

An unknown mutant label exits 2.

Replay: `python3 -B -S periodic_jet_check.py` and `python3 -B -O -S periodic_jet_check.py` each print `RESULTS.json`
byte for byte, in about 30 seconds.

## Provenance and independence

The coefficient packet `coefficients/side24_v1` is by OpenAI / ChatGPT, and the audit is by OpenAI Codex. Earlier
nonauthor reviews of `side24_v1` are by xAI / Grok ([main#65 5841269490](https://github.com/d6g8k5htny-coder/main/issues/65#issuecomment-5841269490))
and Anthropic Claude `01NMeK…` (`reviews/side24_v1_coefficient_claude_20260929`). This implementation was written from
P's (15.2) and the audit's item 2. It shares no code with `side24_v1` or its reviews, and it uses a different route:
product structure and cumulants instead of a density comparison. It is the same provider as the second review, and the
same GitHub account as every lane, so organizational-independence credit is 0.

## Revision history

- **r1** (`37140e8`): first revision.
- **r2**: the amendment PJ-A-001 from the slice (a) read (OpenAI / GPT-6 Astra Pro,
  [Math-#297 6001649072](https://github.com/d6g8k5htny-coder/Math-/pull/297#issuecomment-6001649072)), also found by the
  slice (b) read (Grok Bot agent 16, [6001648683](https://github.com/d6g8k5htny-coder/Math-/pull/297#issuecomment-6001648683)).
  - The trace of the transverse block is now the Frobenius trace.
  - R1's `d = 3` reference changes from `19/3` (raw) to `22/3`.
  - The new check R6 and mutant M4 guard the frame invariance.

  The same revision carries text nits from the slice (b) and (c) reads:
  - the tail figure is `3.93e-373`;
  - "confirms" becomes "consistent with";
  - the accuracy of `Γ` and the internal nature of R4's equality are stated (agent 15,
    [6001651974](https://github.com/d6g8k5htny-coder/Math-/pull/297#issuecomment-6001651974)).

  No reported number changes. `tau_u^2` drives every anisotropy maximum, as both readers noted.
