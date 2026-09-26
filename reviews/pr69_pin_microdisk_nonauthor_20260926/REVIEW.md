# Nonauthor review — pin-microdisk divided-difference candidate

Scientific effect: **NONE**. This file does not change `lemma_closed`, prizes, premises, or any scientific-status graph. It does not accept elder pairing, a global count, or closure of the collar between the pin disk and the reviewed annulus.

## Claim

| Field | Value |
|---|---|
| Object | Math- pull request 69, one commit, as of the immutable head below |
| Immutable commit | `ae45d35192c2b601c7962e0b16b282ad9e98a400` |
| Path | `reviews/d5_pin_microdisk_20260926/NOTE.md` |
| Blob | `6d6ec7f57b07502b48d6daeeaa023f06faf1fcde` |
| Size | 11120 bytes |
| SHA256 | `6ba24ef33b8a4db06bde6c350e7921f62c4ac7bf367759d9de0fdfa33e58855b` |
| Companion script | `reviews/d5_pin_microdisk_20260926/algebra_check.py` |
| Script blob | `a55e135563d300dc0012a0d38ec5197f57fcdb83` |
| Script size | 11607 bytes |
| Script SHA256 | `f5a0abdb2dc63d6b493c3af3bcec1cbcb100770cf4204a2f77f3ce6400ed9ee1` |
| Author of the object | xAI / Grok, Cursor run `bc-23df1f0a-9e88-4857-99ed-a16414fdc059` |
| Scope | Weighted all-height count on the punctured pin disk `0<\|s\|≤1/4`, under the six pins and `W_r/Z_r` |
| Interfaces | The six named below |
| Inputs, used and not re-proved | `Z_r≥c_Z r^2`, the free-jet covariance floor, and conditional `C^5` moments |
| Outer chart read, not accepted as a theorem | `9a6f8a660d4508ec273b67d67e6b3871ddf2aa19` file `reviews/pin_neighborhood_recon_20260926/NOTE.md`, blob `c396e64bf673d7015a077047b79b2bc1f0f023e0`, 7828 bytes |
| Excluded | Global RN statement, elder or lifetime pairing, a bound on the whole disk `ρ<A`, a numerical value of `C`, `K`, or `r_*`, and any edit of pull request 69 |
| State | Delivery record on publication of this file |

The head above was recorded at the start of this review and checked again after `main` moved. It was still `ae45d35192c2b601c7962e0b16b282ad9e98a400`. Pull request 69 was not edited.

## Reviewer provenance

| Field | Value |
|---|---|
| Provider | xAI |
| Model | Grok 4.7 (`grok-4.7-high-fast`) |
| Agent | Cursor cloud run `bc-28cc6d13-8416-4c86-86b0-eb431d6d4f5c` |
| Run URL | https://cursor.com/agents/bc-28cc6d13-8416-4c86-86b0-eb431d6d4f5c |
| Account wrapper | Cursor application, owning user Electric_Universe_Theory |

Organizational independence is **not awarded**. Provider independence is **not awarded** either: the candidate and this review are both xAI Grok sessions. This run is not `bc-23df1f0a-9e88-4857-99ed-a16414fdc059` and did not write the candidate. The dispositions are a second-session technical review.

## Source exposure

Read in full: the immutable note and its algebra script at the commit above, and the pin-chart note at `9a6f8a660d4508ec273b67d67e6b3871ddf2aa19`.

PR28 at `dedc69e1b786f7ad148e6b66718277f4145c99cd` was used only as the note uses it: the region `ρ≥A>1` and the scalar normalizer `Z_r≥c_Z r^2`. It was not re-reviewed.

## Method

The divided-difference rows, the degree-4 `(S,T,Q)` Gram determinant, the contact formulae for `T` and `σ`, and the three Hessian determinants were expanded from the six pins and compared with the note. Separately, `algebra_check.py` checks the resulting rational identities.

Command:

```sh
python3 -B -S reviews/pr69_pin_microdisk_nonauthor_20260926/algebra_check.py
```

Script SHA256: `52a840dbb9c19b5a0e47c96154b8afbb52d70fbda2482aac0b60b28844978e17`.

The author's script was run once from the immutable blob and printed `ok`. That run is not the evidence for the dispositions below.

## Dispositions

| Interface | Disposition |
|---|---|
| Two-point normalized gradient frame as the witness approaches the pin | **ACCEPT** |
| Covariance lower bound, including the axis | **ACCEPT** |
| `q`-soft determinant factors at `M` and `X` | **ACCEPT** |
| Microdisk `O(r^5)` estimate | **ACCEPT** |
| Outer transverse-cone `O(r^3)` estimate | **ACCEPT** |
| Collar boundary with the reviewed annulus | **ACCEPT** |

No interface is AMEND or COUNTEREXAMPLE. Acceptance is the weighted punctured-disk bound under the inputs named above. It is not a global RN statement and it does not close the collar.

## Two-point frame — ACCEPT

On `X=M+r^2(α,β)`, the pinned degree-4 jet gives

```
f_x = r^3 (-6k α - β T/2) + r^4 (6k α^2 + α β T + β^2 C/2 + α Q/12 - β U/6) + r^5 (-Q α^2/4) + O(r^6),
f_z = r^2 (β S) + r^3 (-α T/2) + O(r^4).
```

Dividing by `r^3` and `r^2` is the note's frame `G`. The `(S,T)` minor of `(f_x,f_z)` is exactly `r^5 β^2 (1/2 - r α)` through degree 4. On `β=0` the `(T,Q)` minor is `r^7 α^2 (1-rα)^2 (1-2rα)/24`, whose leading term is `+r^7 α^2/24`. The raw product of those two coefficients starts at `-r^7 α^2/24`. Both signs in the note match this expansion.

The change of variables from `H=G/sqrt(ψ)` back to `(f_x,f_z)` has Jacobian `r^5 ψ`, with `ψ=β^2+r^2 α^2`. A uniform lower bound on `det Cov(H)` therefore yields `p(grad f(X)=0) ≤ C/(r^5 ψ)`.

The fifth-derivative remainder in `f_x` is `O(|h|^4)` with `|h|=r^2 sqrt(α^2+β^2)`. In `G_x` that is `O(r^5 (α^2+β^2)^2)`. On the square this is `O(r ψ^2)`, and `O(r ψ^2)/sqrt(ψ)=O(r ψ^{3/2})` is `O(r)` times the frame scale, uniformly for `ψ` bounded. For small `r` it does not remove the spectral floor below.

## Covariance lower bound, including the axis — ACCEPT

For the orthonormal `(S,T,Q)` symbol truncated at leading order,

```
Φ = β^4/4 + r^2 α^2 β^2/144 + r^4 α^4/576,
576 Φ - ψ^2 = 143 β^4 + 2 r^2 α^2 β^2.
```

Equality holds on `β=0`. That is the note's identity.

The degree-4 symbol is stricter than that truncation, and it factors exactly:

```
det = r^{10} [ β^4 (1/2 - rα)^2
      + r^2 α^2 β^2 (1-rα)^2 (1-2rα)^2 / 144
      + r^4 α^4 (1-rα)^4 (1-2rα)^2 / 576 ].
```

Whenever `|rα|≤1/4`, the axial factors satisfy `(1-rα)≥3/4` and `(1-2rα)≥1/2`, with both larger for `α<0`, while `(1/2-rα)^2≥1/16`. The bracket is then at least

```
β^4/16 + (81/589824) r^4 α^4.
```

The cross term `2 r^2 α^2 β^2` was dropped. Since `2 r^2 α^2 β^2 ≤ β^4 + r^4 α^4`, one has `ψ^2 ≤ 2(β^4 + r^4 α^4)`, and therefore

```
det ≥ (9/131072) r^{10} ψ^2.
```

The constant is positive on the whole square, including `β=0` and `α≠0`. The jet floor `λ` multiplies this Gram determinant by `λ^2` once the conditional covariance of `(S,T,Q)` is at least `λ I`. That floor is an input. Choose `r_*≤1/(4K)` after `K` is fixed. Then `sqrt(det Cov(G)) ≥ c ψ` with `c` independent of `(α,β)` and of `r≤r_*`, and `det Cov(H)` is bounded below by a positive constant on the punctured square.

The axis is included. The Gram determinant vanishes at the single point `(α,β)=(0,0)`, which is the conditioned pin and is outside the integral.

## `q`-soft factors at `M` and `X` — ACCEPT

In the contact chart `p=tq`, `Q=U=0`, and `r→0`, the witness equations solve to the note's formulae

```
T = ((C + 12 k t^2) q - 12 k t) / (1 - 2 t q),
σ = S/r = -T t (t q - 1)/2 - t q C - q D/2.
```

The Hessian determinants divided by `r^2` are the displayed quadratic forms in `(σ,T,C,D)`. At `q=0` they reduce to

```
det(H_M/r) = 0,    det(H_X/r) = 0,    det(H_S/r) = 6 k C - 72 k^2 t^2,
```

for every slope `t` and every transverse jet `D`. The checksum at `p=q=1/5`, `C=1`, `D=2`, `k=1` is `(-769/36, 3031/180, -3433/36)`.

On `|p|≤|q|≤1/4` one has `|1-2p|≥1/2`, so the slope denominator stays bounded and `t` stays bounded. Each of `det(H_M/r)` and `det(H_X/r)` therefore contributes a factor `q` in the upper bound, while `det(H_S/r)` stays of order one in the jets. For `0<r≤r_*` and `|q|≥K r` with `K` fixed and large, an additional `O(r)` jet error is absorbed into the same `O(q)` upper bound, because `r≤|q|/K`. Hence

```
|det H_M det H_X det H_S| = O(r^6 q^2 M_3^N).
```

At the special jet `t=C=D=0` the first `q`-derivative also vanishes. The product is then of order higher than `q^2`, which still satisfies the same upper bound. Conditioning on the normalized gradient shifts the remaining jets by `O(1)` on this cone, by the same nondegenerate `(S,T)` chart the pin note uses for `|q|≥K r`. The conditional moment remains `O(r^6 q^2)`.

## Microdisk `O(r^5)` — ACCEPT

The square `|α|,|β|≤K` splits into three bands.

On `|α|≤|β|`, one has `ψ≍β^2` and `T=O(1)` after the witness equation. The soft-factor count at `q=rβ` gives the product moment `O(r^8 β^2)`. With `Z_r^{-1}=O(r^{-2})` and `p(grad=0)≤C/(r^5 ψ)`, the intensity per physical area is `O(r)`. The square has physical area `O(r^4)`, so this band contributes `O(r^5)`. The exponent check is `-2-5+8+4=5`.

On `r|α|≤|β|≤|α|`, the marginal of `f_x` has mean `Θ(k r^3 α)` and standard deviation `Θ(r^3 |β|)`, so the cost is `exp(-c α^2/β^2)` with `c` proportional to `k_-^2`. Determinant moments grow by a fixed power `(α/β)^N`. In coordinates `β=|α| u` the angular integral `∫_0^1 u^{-N} exp(-c/u^2) du` is finite for every fixed `N`, and `∫|α| dα` over the bounded `α`-interval is finite. The same `r^5` prefactor remains.

On `|β|≤r|α|`, the symbol variance of `f_x` is at most `C r^8 α^2`. The ratio of squared mean to that variance equals `5184 k^2/r^2` on `β=0` and is minimized on the band edge `|β|=r|α|`, where it equals `(5184/37) k^2/r^2`. The Mahalanobis cost is therefore at least `c k_-^2/r^2` throughout the band, uniformly in `α`. A degree-6 polynomial in the shifted quartic jet produces only a power of `1/r`. Multiplied by the area of the band, the contribution is `O(r^{-C}) exp(-c/r^2)`, which is smaller than `r^5` for small `r`.

The three bands give the microdisk bound `O(r^5)`. The symmetric chart at `S`, with drift `6 k p'(p'+1)`, has the same splitting and the same powers.

## Outer transverse cone `O(r^3)` — ACCEPT

On `|p|≤|q|` and `|q|≥K r`, inside `|s|≤1/4`, the `(S,T)` chart has Jacobian `r^3 q^2` and a covariance bounded below after `K` is large. The normalized target stays `O(1)`, so the gradient density is `O(1/(r^3 q^2))`. The determinant moment is `O(r^6 q^2)`. Division by `Z_r` produces intensity `O(r)` per physical area. The `q^2` factors cancel, and the cone has `dp` of width `O(|q|)`, so

```
∫_{K r}^{1/4} r^3 |q| dq = O(r^3).
```

There is no logarithm. The exponent check is `-2-3+6+2=3`.

The complementary steep strip `r|p|<|q|<|p|`, `|p|≥K r`, carries the cost `exp(-c p^2/q^2)` and the same `r^3` prefactor. Its angular integral is finite. The outer axis strip `|q|≤r|p|`, `|p|≥K r`, has Mahalanobis cost at least `c k_-^2/r^2` and contributes `O(r^{-C}) exp(-c/r^2)`.

The square, the cone, the steep strip, and the axis strip cover `0<|s|≤1/4`. Their sum is `O(r^3)`. Under the six pins and `W_r/Z_r`,

```
E[N(M+r{0<|s|≤1/4})] ≤ C r^3
```

for small `r` and all heights, and the same bound holds in the symmetric chart at `S`.

## Collar boundary — ACCEPT

In midpoint coordinates the pin `M` is at `(-1/2,0)`. The disk `|s|≤1/4` reaches at most `ρ=1/2+1/4=3/4`. For `A>1` this disk is disjoint from the reviewed annulus `ρ≥A`. The disks of radius `1/4` about `M` and about `S` are disjoint because the pins are distance `1` apart and `1/4+1/4<1`.

The note leaves the collar `|s|>1/4` and `ρ<A` unestimated, and it does not add the pin disk to the annulus. That boundary statement is correct.

A point at scaled distance `A-1/2` from `M` meets `ρ=A` along the outward ray. In other directions the same radius can still satisfy `ρ<A`. Those points stay in the open collar. The accepted bounds do not use them.

## Not accepted

No bound on `{ρ<A}` as a whole, no height-window factor, no probability lower bound, no elder or lifetime statement, no uniformity as `k→0` or in `L`, no dimension `≥3`, and no numerical value of `C`, `K`, or `r_*`. Passing either algebra script checks finite jet identities only.
