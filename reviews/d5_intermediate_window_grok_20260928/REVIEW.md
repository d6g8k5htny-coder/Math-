# Grok interface review: D5 intermediate height-window bridge

Object: GROK-D5-INTERMEDIATE-WINDOW-REVIEW-20260928-v1.
Reviewed object: OA-D5-INTERMEDIATE-WINDOW-20260928-v1.
Scientific effect: **NONE**. This file does not change `lemma_closed`, prizes,
premises, `STATUS`, `PROOF_INDEX`, `GRAPH`, or any author source. It records
verdicts. Integration of the candidate remains a separate engineering act and
does not close the PROOF_INDEX intermediate-scale line.

## Objects

| Object | Identity |
|---|---|
| Candidate branch / head | `chatgpt/intermediate-window-20260928` / `742e72e427cd98e529af4d86b3917b1c7f144f01` |
| PROOF.md | Git blob `f53a527ce0204fda271f24730b62b4223a5e43ec`, 27775 bytes, SHA256 `b3eb9456d7058b5b78149cfca4e072679beda85cd1a0293d209664a542db66cf` |
| Math- tip at review | `5eba8f76faac573ece1ffeb06e0f4548f2a0e6c7` (post-#106 engineering integration) |
| Parent issue / PR | [Math-#107](https://github.com/d6g8k5htny-coder/Math-/pull/107) |

Provider: xAI Grok. Same GitHub account as every lane; no organizational
independence is claimed. Distinct from the OpenAI author of the candidate.
Prior #104/#105 reviews are not inherited.

## Verdicts

| Interface | Verdict |
|---|---|
| Nine-row degree-five rank through `ε = r/s = 0` | **ACCEPT** (finite exact) |
| Degree-four collinear rank drop | **ACCEPT** (negative control) |
| Uniform Hermite divided-difference remainder, mass-1 kernel | **ACCEPT** (finite exact / kernel identity) |
| Reduced target (I14)–(I16), physical Jacobian `s^6` | **ACCEPT** (finite exact) |
| Transverse minor `|v|^6/24`, `det(BB^T) ≥ v^{12}/576` | **ACCEPT** (finite exact) |
| Euler cubic cancellation; both remainder channels live | **ACCEPT** (finite exact, with the all-height negative control) |
| Shell / dyadic power ledger | **ACCEPT** (finite exact) |
| Isolated runner replay vs `RESULTS.json` | **ACCEPT** as hosted-local evidence of the packet, not of the continuum |
| (I11) conditional floor `Cov_{Q_r}(Y_X) ≥ c s^{10} I_3` | **HOLD** |
| (I18) continuum pathwise Euler bound under nine observations | **HOLD** |
| (I25)/(I30) conditional `C^6` moments | **HOLD** |
| (I33) Kac–Rice first-moment disintegration | **HOLD** |
| Shell candidate (I3) | **HOLD** as author-side analytic candidate |
| Dyadic form (I4) | **HOLD**, same |
| Global first-moment synthesis (I5) | **HOLD**, dependency-bound on named local and remote sources |

## Finite replay

Isolated clone of `742e72e`, command

```
python -B -S frontiers/intermediate_window_20260928/run_validation.py --output /tmp/iw-run
```

matched `RESULTS.json`:

- 15 named tests × modes `{normal, optimized}`
- 24 confluent-rank fixtures, 48 pinned-cubic fixtures, 18 transverse minors
- 10 distinct mutants assertion-rejected
- `continuum_verified: false` (correctly recorded)

These checks certify the packet's exact identities and mutation controls.
They do not prove uniform analytic remainders, Gaussian supremum bounds,
Fourier-lattice jet PD, or Kac–Rice hypotheses.

## Algebraic skeleton (why (I3) has the right shape)

The candidate counts additional index-`j` critical points with height in the
*actual* between-pin window `I_r = (b - k r^3, b)`, on the physical shell
`s ≤ |X| ≤ 2s`, under the original six-pin law `Q_r` reweighted by `W_r/Z_r`.

Nine observations, not eight: the six pins plus `(f_x, f_z, f)` at the witness.
The extra height coordinate is conditioned and then integrated over `I_r`.
That is a different measure from the earlier all-height collar argument.

Power ledger consumed by the shell integral:

```
Z_r^{-1}                         r^{-2}
endpoint product in W_r          r^{2}
height window |I_r|              r^{3}
physical Jacobian of (I14)       s^{6}  → density s^{-6}
pathwise (I21)                   s^{2} (r + s^{2})^{2} |v|^{-6}
shell area                       s^{2}
```

On the transverse region this produces

```
E N_window(shell)  ≤  C r^{3} (r + s^{2})^{2} / s^{2}
                   ≤  C r^{3} [(r/s)^{2} + s^{2}].
```

Dyadic summation over `s_j = 2^j A_0 r` is then `O(r^{3}(A_0^{-2} + ρ^{2}))`,
with constants independent of the number of shells. That is exactly the
uniform growing-scaled-radius first-moment bridge the PROOF_INDEX line

> D5 intermediate scale r ≪ |x| ≪ ρ … NO COMPLETE PROOF YET:
> uniform growing-scaled-radius bridge

asked for, *as a candidate*. The Euler identity (I18) is the mechanism that
prevents a plain `O(r^{3})` per shell and the resulting logarithmic loss.
Without the height restriction the suppression of `|S_0|` fails; the packet's
own `test_without_height_window_suppression_fails` is the right negative
control for that claim.

## Why continuum steps stay HOLD

1. **(I11).** The rank-plus-remainder argument is the correct shape: degree-five
   interpolation stays onto at confluence, the Hermite maps are uniformly
   bounded on `C^3`, and an `O(s^6)` remainder subtracted from a `s^5` jet
   floor leaves `Cov(V) ≥ c s^{10}`. The Schur identity then gives the
   three-dimensional conditional floor. I did not independently re-prove the
   Fourier-lattice 21-jet PD or the uniform `L^p(Q_r)` remainder.
2. **(I18).** Polynomial Euler cancellation is exact. The continuum claim is
   that, under the six pins plus `grad f(X) = 0` and `f(X) ∈ I_r`, every
   contribution other than `S_0 s^{2} v^{2}/2` is `O(K(r^{2}s + s^{4}))`.
   That uses (I12) and a `C^4` remainder. Mechanism accepted; implicit
   constant and the reduction of `s_0` are not certified here.
3. **(I25)/(I30).** Crude regression bounds `s^{-60}` and `|v|^{-48}` from
   `||Σ^{-1}||` times a whole-field moment. The exponents are absorbed by
   the Gaussian factors, so they do not threaten the *shape* of (I3). They
   are the easiest place for a hidden `ε`-loss or a pin-conditioned versus
   witness-conditioned mix-up, and they are not a compact-set Gaussian
   supremum argument.
4. **(I33).** AAL arXiv:2304.07424v3 Theorems 2.2 and 7.1 with Remark 8 is
   the same first-moment framework used on D1 §9. Applicable in outline on a
   compact shell separated from the pins. Not a factorial-moment theorem.
   Truncation / monotone-convergence removal of growth restrictions was not
   re-checked on this packet.
5. **(I5).** Composition is “local all-height collar + (I4) + fixed-remote
   height window, one `(Q_r, W_r, Z_r)`”. Strength equals the named sources
   `reviews/d5_local_collar_20260928/{PUNCTURED_PIN_PROOF,COLLAR_PROOF}.md`
   and `frontiers/remote_window_20260924/PROOF.md`. Those reviews are not
   inherited. (I5) stays a candidate corollary, not a closed D5/RN theorem.

## Scope firewall

This review does **not** accept, and the candidate does not claim:

- an all-height intermediate or global `O(r^{3})` count;
- shrinking-separation factorial moments or witness-collision estimates;
- elder-rule pairing, a quantitative selector, or a lifetime asymptotic;
- uniformity as `k → 0`, marks grow, `T` changes, or dimension increases;
- a numerical `C`, `s_0`, or 24-jet certificate;
- a STATUS / `lemma_closed` / PROOF_INDEX verdict change.

A first-moment one-witness bridge may remove the need for some collision
machinery in a first-moment-only downstream argument. It does not discharge
any existing factorial-moment obligation.

## Disposition

Ready for engineering integration of this review *record* and, separately,
of the #107 files as a dated frontier packet. Not ready to flip any
scientific-status register. Theorem-level consumption of (I3)–(I5) still
requires an independent analytic pass on the HOLD items above.
