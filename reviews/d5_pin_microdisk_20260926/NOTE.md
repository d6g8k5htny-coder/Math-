# Pin microdisk — divided-difference frame

Scientific effect: **NONE**. This note does not change `lemma_closed`, prizes, premises, or any status graph. It does not claim elder pairing, a global count, or a numerical constant. PR53, the reviewed annulus sources, and the existing review files are not modified.

## Conclusion

The nested microdisk closes the inner-disk gap left by the pin chart. No deeper blow-up is required.

Let `M=(-r/2,0)`, `S=(r/2,0)`, and let `N` count critical points of any index at all heights. Under the original six pins and the endpoint weight `W_r/Z_r`, there are `K`, `C`, and `r_*>0` such that for `0<r≤r_*`,

```
E[N(M+r{0<|s|≤1/4})] ≤ C r^3,
```

and the same bound in the symmetric chart at `S`. The square `|p|≤K r`, `|q|≤K r` inside that disk contributes at most `C r^5`.

The gain on the outer part of the same disk is the transverse cancellation: after the witness-gradient equations,

```
det(H_M/r) and det(H_X/r) vanish at q=0,
det(H_S/r)|_{q=0} = 6 k C - 72 k^2 t^2,
```

with `p=t q`. On the cone `|p|≤|q|` and `|q|≥K r` the product of the three absolute determinants is `O(r^6 q^2)`. The logarithm in the earlier `O(r^2 log(1/r))` ledger is absent from this cone.

The disk `|s|≤1/4` reaches at most `ρ=3/4` and does not meet the reviewed annulus `ρ≥A>1`. The collar between `|s|=1/4` and `ρ=A` is not estimated.

## Inputs, not re-proved

Pins, unchanged:

```
f(M)=b, f(S)=b-k r^3, grad f(M)=grad f(S)=0,
0<k_-≤k≤k_+<∞.
```

`Q_r` is the Gaussian regression on those six values. `W_r=F_2(H_M)F_1(H_S)` and `Z_r=E_{Q_r} W_r≥c_Z r^2` are the endpoint normalizer already used by the pin chart. They are an input. The lower bound on `Z_r` is the one recorded for the six pins in the fixed-annulus argument, imported here only as that scalar bound.

The free jets at `M` that the six pins do not fix — including `S=f_zz(M)`, `T=f_xxz(M)`, `Q=f_xxxx(M)`, `C=f_xzz(M)`, and `D=f_zzz(M)` — have a conditional covariance bounded above and below by positive constants for small `r`. That is the same distinct-monomial floor the pin chart uses off the endpoint. Conditional `C^5` moments under `Q_r` stay bounded. Both facts are used as inputs; this note does not reopen their proofs.

PR28 at `dedc69e1b786f7ad148e6b66718277f4145c99cd`, blob `6f317515b3d417661f86e2fed09bc7d950899c2b`, as accepted by merged PR44, is imported only as the region `ρ≥A>1` and as the source of the normalizer just named. It is not re-reviewed. The pin-chart file at `9a6f8a660d4508ec273b67d67e6b3871ddf2aa19` is the outer chart being completed, not an accepted theorem.

## Coordinates

`X=M+r s` with `s=(p,q)`. The microdisk is the further scaling `s=r(α,β)`, so

```
X = M + r^2 (α, β), |α|≤K, |β|≤K, (α,β)≠(0,0).
```

Physical distance to `M` is `O(r^2)`. The point `(α,β)=(0,0)` is the conditioned pin, not a witness. Write

```
ψ = β^2 + r^2 α^2.
```

## Divided-difference frame

`grad f(M)=0` under `Q_r`, so the gradient at `X` is already a two-point increment. The pin curvature `f_xx(M)` is order `r`, while `f_zz(M)` is order 1, so the two components are scaled differently:

```
G_x = f_x(X) / r^3,    G_z = f_z(X) / r^2.
```

On the degree-4 jet these rows are exact. Through the orders that carry `(S,T,Q)`,

```
G_x = -6 k α - (β/2) T + r (6 k α^2 + α β T + β^2 C/2 + α Q/12 - β U/6) + O(r^2),
G_z = β S - (r α/2) T + O(r^2).
```

The `(S,T)` minor of the map into `(f_x,f_z)` is `r^5 β^2 (1/2 - r α)`. The axial `(T,Q)` minor, the case `β=0`, starts at `-r^7 α^2/24` in the raw product and at `+r^7 α^2/24` as a `2×2` minor. In the orthonormal `(S,T,Q)` symbol the covariance determinant of `(f_x,f_z)` equals

```
r^{10} Φ,   Φ = β^4/4 + r^2 α^2 β^2/144 + r^4 α^4/576.
```

The Gram comparison is the polynomial identity

```
576 Φ - ψ^2 = 143 β^4 + 2 r^2 α^2 β^2 ≥ 0,
```

so `Φ ≥ ψ^2/576`, with equality on the axis `β=0`, `α≠0`. Thus

```
sqrt(det Cov(G)) ≥ c ψ
```

for small `r`, uniformly for `0<ψ≤K^2+r^2 K^2`, after the jet floor `λ` multiplies `Φ` and the `O(r)` coefficient errors are absorbed. Equivalently

```
sqrt(det Cov(grad f(X))) ≥ c r^5 ψ.
```

The normalized frame

```
H = G / sqrt(ψ)
```

therefore has `det Cov(H)` bounded below by a positive constant independent of `(α,β)` and of small `r`. It stays nondegenerate as `X→M` through the microdisk, including along `β=0`. The change of variables back to `(f_x,f_z)` has Jacobian `r^5 ψ`, so

```
p(grad f(X)=0) ≤ C / (r^5 ψ).
```

The fifth-derivative remainder in `G_x` is `O(r ψ^2)` on this square, which is `o(sqrt(ψ))` as `r→0`, uniformly in `(α,β)`. It does not cancel the symbol.

## Determinant repulsion

Write `det(H/r)` for `det(H)/r^2`.

**Contact chart, outer cone.** Set `p=t q` and pass to the limit `r→0` with `Q=U=0`. The witness equations determine

```
T = ((C + 12 k t^2) q - 12 k t) / (1 - 2 t q),
σ = S/r = -T t (t q - 1)/2 - t q C - q D/2.
```

Then

```
det(H_M/r) = -6 k σ - T^2/4,
det(H_X/r) = (-6 k + 12 k p + T q)(σ + C p + D q) - (-T/2 + T p + C q)^2,
det(H_S/r) = 6 k (σ + C) - T^2/4.
```

At `q=0` the first two values are `0` for every slope `t`, and

```
det(H_S/r) = 6 k C - 72 k^2 t^2.
```

So `M` and `X` each contribute one factor of `q`, while `S` keeps a transverse value of order 1. For `0<r≤r_*` and `|q|≥K r`, with `K` fixed and large, the same count persists with an `O(r)` error:

```
|det H_M det H_X det H_S| = O(r^6 q^2 M_3^N).
```

On `|p|≤|q|≤1/4` one has `|1-2p|≥1/2`, so the slope denominator stays bounded and `t` stays bounded. Conditioning on `G=0` shifts the remaining jets by `O(1)`. The conditional moment of the product is `O(r^6 q^2)`.

**Microdisk, transverse square `|α|≤|β|`.** The same solved symbol gives

```
det H_M = O(r^3 |β| M),   det H_X = O(r^3 |β| M),   det H_S = O(r^2 M).
```

The product is `O(r^8 β^2 M^N)`. Here `ψ≍β^2` and the regression shift of `H` is `O(|α|/|β|)≤O(1)`, so the conditional moment is `O(r^8 β^2)`.

**Microdisk, axial square `|β|≤|α|`.** The solved slope is `T=Θ(α/β)`. Conditional moments of the determinants grow like a fixed power `(α/β)^N`. They are kept inside the Gaussian integral below, not discarded.

## Integrable majorant

The weighted intensity per physical area is at most

```
Z_r^{-1} · p(grad=0) · E[|det H_X| W_r | grad=0].
```

`W_r≤|det H_M det H_S|` and `Z_r^{-1}=O(r^{-2})`.

On the transverse microdisk, `ψ≥β^2` and the product moment is `O(r^8 β^2)`, so the intensity is `O(r)`. The physical area of the square is `O(r^4)`. Its expected count is `O(r^5)`.

On the axial band `r|α|≤|β|≤|α|`, the marginal of `f_x` has mean `Θ(k r^3 α)` and standard deviation `Θ(r^3 |β|)`. The cost is `exp(-c α^2/β^2)`. Every power `(α/β)^N` is absorbed by that exponential, and `∫ |α| dα ∫ u^{-N} exp(-c/u^2) du` over `u∈(0,1]` is finite. The contribution is `O(r^5)`.

On the quartic band `|β|≤r|α|`, the symbol variance of `f_x` is at most `C r^8 α^2`. The exact `(T,Q)` ratio with unit variances is at least `(5184/37) k^2/r^2`, with equality at `|β|=r|α|`, and equals `5184 k^2/r^2` on `β=0`. After the jet variances, the Mahalanobis lower bound is `c k_-^2/r^2`. The band contributes `O(r^{-C}) exp(-c/r^2)`, which is smaller than `r^5`.

Adding the three bands gives the microdisk bound `O(r^5)`.

## Outer cone, steep strip, axis strip

These are the parts of `0<|s|≤1/4` outside the square `|p|,|q|≤K r`.

**Transverse cone** `|p|≤|q|`, `|q|≥K r`. The gradient density in the `(S,T)` chart is `O(1/(r^3 q^2))`. The determinant moment is `O(r^6 q^2)`. Division by `Z_r` produces intensity `O(r)` per physical area. The cone has `dp` of width `O(|q|)` and

```
∫_{K r}^{1/4} r^3 |q| dq = O(r^3).
```

The powers of `q` cancel, so there is no logarithm.

**Steep strip** `r|p|<|q|<|p|`, `|p|≥K r`. The drift of `f_x/r^2` is `Θ(|p|)` and its standard deviation is `Θ(|q|)`, so the cost is `exp(-c p^2/q^2)`. The conditional determinant moment grows like a fixed power of `|p/q|`. In coordinates `q=|p| u`,

```
∫_{K r}^{1/4} |p| dp ∫_0^1 u^{-N} exp(-c/u^2) du
```

is finite for every fixed `N`. The prefactors are the same `r^{-2}·r^{-3}·r^6·r^2` that produce `r^3`. The strip contributes `O(r^3)`.

**Axis strip** `|q|≤r|p|`, `|p|≥K r`. The ratio `(E ξ)^2/Var(ξ)` is at least `c k_-^2/r^2`, as in the pin chart. The contribution is `O(r^{-C}) exp(-c/r^2)`.

The square, the cone, the steep strip, and the axis strip cover `0<|s|≤1/4`. The sum is `O(r^3)`. The symmetric chart at `S` has the drift `6 k p'(p'+1)` and the same bounds.

## Stitch

| Region | Bound | Role |
|---|---|---|
| Microdisk `\|p\|,\|q\|≤K r` | `O(r^5)` | Divided-difference frame and `β^2` repulsion |
| Cone, steep strip, axis strip inside `\|s\|≤1/4` | `O(r^3)` | Soft factors `q` on `H_M` and `H_X`; Gaussian cost off the cone |
| Pin disk `0<\|s\|≤1/4` | `O(r^3)` | Sum of the two rows above |
| Reviewed annulus `ρ≥A>1` | `O(r^3)` per unit scaled area | Imported from PR28/PR44, not re-proved |
| Collar `\|s\|>1/4` and `ρ<A` | not estimated | Left open |

`|s|≤1/4` around `M=(-1/2,0)` reaches at most `ρ=3/4`. Since `A>1`, that disk and the annulus are disjoint. The disks of radius `1/4` about `M` and about `S` are disjoint because the pins are distance `1` apart in the scaled coordinate. Continuing either chart out to distance `A-1/2>1/2` lands in the separated-site regime PR28/PR44 already estimate. This note does not estimate the collar, and it does not add the pin disk to the annulus.

## Not claimed

No bound on `{ρ<A}` as a whole, no height-window factor, no lower bound, no elder or lifetime statement, no uniformity as `k→0` or in `L`, no dimension `≥3`, no witness-witness collision, and no numerical value of `C`, `K`, or `r_*`. The algebra script checks finite jet identities only.

## Computation

```sh
python3 -B -S reviews/d5_pin_microdisk_20260926/algebra_check.py
```

Script SHA256 `f5a0abdb2dc63d6b493c3af3bcec1cbcb100770cf4204a2f77f3ce6400ed9ee1`. It checks the degree-4 divided-difference rows, the `(S,T)` minor `r^5 β^2(1/2-r α)`, the axial `(T,Q)` factor `r^7 α^2/24`, the Gram identity `576 Φ-ψ^2=143 β^4+2 r^2 α^2 β^2`, the contact values `(-769/36, 3031/180, -3433/36)` at `p=q=1/5`, the vanishing of `det(H_M/r)` and `det(H_X/r)` at `q=0`, the transverse value `6 k C-72 k^2 t^2`, the quartic threshold `5184/37`, the ledgers `r^5` and `r^3`, and the separation `1/4+1/4<1`. Six semantic mutants of those coefficients are refused. Passing the script is not a proof of the integral.

## Provenance

| Field | Value |
|---|---|
| Provider | xAI |
| Model | Grok 4.7 (`grok-4.7-high-fast`) |
| Agent | Cursor cloud run `bc-23df1f0a-9e88-4857-99ed-a16414fdc059` |
| Run URL | https://cursor.com/agents/bc-23df1f0a-9e88-4857-99ed-a16414fdc059 |
| Input chart | `9a6f8a660d4508ec273b67d67e6b3871ddf2aa19` |
| Task | https://github.com/d6g8k5htny-coder/Math-/issues/58 |

Author-side note. Organizational independence is not awarded.
