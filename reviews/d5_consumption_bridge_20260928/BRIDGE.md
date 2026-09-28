# Consumption bridge for recorded D5 / D1 pieces

Scientific effect: **NONE**. This file records exact consumption edges among
already-reviewed statements and reusable finite identities. It does not accept
Math-#116 continuum claims, Math-#118, Math-#120, catalog C6, or C8.

Reviewer: xAI / Grok. Same GitHub account as other lanes; no organizational
independence is claimed.

Base: Math- `main` at `4f6abcb05bd59a7770f12cb7f79640d8b7a9a734`.

## 1. Recorded ACCEPT pieces used as inputs

| ID | Statement | Record |
|---|---|---|
| P2 | punctured-pin first moment, all-height nested disk | `reviews/d5_local_collar_20260928/PUNCTURED_PIN_PROOF.md` |
| collar C1 | `E N_j(r E) \le C r^3 \|E\|` on compact collar `C(\u03b7,R)` | Math-#119 |
| scaled-ball C2 | same bound on scaled ball of fixed `R` minus pins | Math-#119, corollary of P2 + collar C1 at `η=1/4` |
| I3, I4 | height-window shells and intermediate annulus | Math-#117 |
| D4 A | remote first moment `O(r^3 \|E\|)` on `D_\u03c1` | `frontiers/remote_window_20260924/PROOF.md` |
| I5 | `E N_{I_r}(T^2 \setminus \{M,S\}) \le C r^3` | Math-#117: C2 + I4 + D4 A |
| F− | `P(A_r) \ge c r^3` | Math-#110 remote A+E |
| F+ | `P(A_r) \le C r^3` | Math-#117 Markov on I5 |
| Pη | `E N_\u03b7(N_\u03b7-1) \le C_\u03b7 r^5` at fixed `η>0` | Math-#119 / #110 |
| H1–H3 | generic TV identities | Math-#115 |
| H4 | remote singleton law at fixed `D_\u03c1` | Math-#115 |
| Thm A (1.1) | `0 \le 1-p_r \le C r^3` compact B,K, frames | parent (1.1), review `reviews/d1_theorem_a_nonauthor_20260928/` |

Event `A_r = \{ N_{I_r}(T^2 \setminus \{M,S\}) \ge 1 \}`.

## 2. Closed downstream edges

### E1. Window first moment (already recorded)

    I5  ←  C2  +  I4  +  D4 A.

Height window on I4 is load-bearing. All-height intermediate `O(r^3)` is false
for the shell method and is not an input.

### E2. Planar event probability (already recorded)

    F+  ←  Markov(I5),     F  ←  F− ∧ F+.

In `d=2`,

    c r^3  ≤  P(A_r)  ≤  C r^3.

This is an event probability on the torus minus the two pins. It is not
`E N(N-1)` and not an elder-pairing theorem.

### E3. Remote singleton at fixed `D_\u03c1` (already recorded)

    H4  ←  H1–H3  +  D4 A  +  #110 Corollary D.

Scope is a deterministic positive-volume `E \subset D_\u03c1`. Not torus-wide
uniqueness, not a height law, not Poisson.

### E4. Compatibility of H4 and planar F

H4 lives on `D_\u03c1`, which excludes a neighborhood of the pins. Planar F counts
any extra window critical point on `T^2 \setminus \{M,S\}`, including the pin
neighborhood that H4 does not see. Both statements can hold at once: remote
configurations are close to Bernoulli at rate `O(r^5)\|E\|`, while the event
that *some* extra window point exists anywhere off the pins is `Θ(r^3)`.

### E5. Thin-tube first moment is not an open obligation

The thin-tube region sits inside any fixed scaled ball. C2 already bounds that
first moment. The tube note remains a more precise intensity; it is not an
unfinished first-moment gate for I5 or F.

### E6. Compact-mark selection-difference *upper* bound

Parent `imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md`
§11:

    r dr/dℓ = (1/3) k^{-2/3} ℓ^{-1/3},                              (11.1)
    ν_cand(ℓ) = ℓ^{-1/3} ∫ A_{(ℓ/k)^{1/3}} / (3 k^{2/3}).         (11.2)

On a compact mark window `B × K` with `k \ge k_- > 0`, `A_r` is bounded by the
parent A3 majorant and `∫_K k^{-5/3} dk < ∞`. Theorem A (1.1) gives
`0 \le 1-p_r \le C r^3`. Substituting `r = (ℓ/k)^{1/3}` into the difference
form of (11.2) yields

    0  ≤  ν_cand(ℓ) − ν_eld(ℓ)  ≤  C_{B,K} ℓ^{2/3}.

This uses only the *upper* half of (1.1). It does not use Math-#116 C1, does
not claim sharpness `Θ(ℓ^{2/3})`, and does not extend to unrestricted marks
(catalog C7).

### E7. Off-pin second moment does not upgrade to the torus

Split, for any `η>0`,

    N = N_η + N_{<η},
    E[N(N-1)] = E[N_η(N_η-1)] + E[N_{<η}(N_{<η}-1)] + 2 E[N_η N_{<η}].

Pη bounds the first summand. The other two summands require a pair floor with
at least one witness in `{\|X\|<η}`. Cauchy–Schwarz on I5 does not produce
those terms. Catalog C6 remains open. The elementary comparison
`N(N-1) \ge 2 1{N\ge2}` is unconditional; applying it to a proposed
`P(N\ge2) \ge c r^3` is conditional on catalog C2 and is not used here.

## 3. Reusable finite identities

These are polynomial / calculus identities. They may be consumed by a later
continuum review. They are not Gaussian theorems.

### L1. Collar B-frame Gram

    det(BB^T) = u^2 v^4 + v^6/4 = v^4(4u^2+v^2)/4.

Nonnegative, and positive for `(u,v) \ne 0`.

### L2. Overlap integral

    ∫_0^∞ s (k − s^3 |t|)_+ ds = (3/10) k^{5/3} |t|^{-2/3}.

Direct antiderivative on `s \le (k/|t|)^{1/3}`:
`k s_*^2/2 − |t| s_*^5/5` with `s_*^3 = k/|t|`.

### L3. Pinned cubic and path

    G_k = k(2X^3 − 3X/2 − 1/2 − 3Z^2/4 − X Z^2).

Pins: `G(±1/2, 0)` and `∇G(±1/2, 0) = 0`, with values `0` and `−k`.
Path `(−1/2,0) → (−3/4,0) → (−3/4,9/4) → (−1,9/4)` takes values
`0`, `−7k/32`, `−7k/32`, `+17k/64`. Extra critical points at
`X=−3/4`, `Z^2=15/8`: height `−7k/32`, `det H = −15 k^2/2`.

### L4. Gap Beta moments

Density `(10/9) g^{-1/3}(1-g)` on `(0,1)` is Beta`(2/3,2)`.
Mean `1/4`. Variance `9/176`.
Joint density `(5/9)|a-b|^{-1/3}` on `(0,1)^2` is a different object from this
scalar gap law.

### L5. Factorial split

`E[N(N-1)]` expands as in E7. Pointwise `N(N-1) \ge 2 1{N\ge2}`.

## 4. Explicit non-edges

- Math-#116 C1–C5 continuum steps, including `1-p_r \ge c r^3` and the pair kernel `K_{ij}`.
- Catalog C6 torus-wide second factorial moment.
- Catalog C7 unrestricted difference rate.
- Catalog C8 numerical constants.
- Math-#118 P15 (separate program).
- Math-#120 remote height decoupling (C5 refinement; not a corollary of H4).
- Feeding planar F or I5 into H4 as a torus-wide uniqueness theorem.

No STATUS / GRAPH / lemma_closed / prize change.
