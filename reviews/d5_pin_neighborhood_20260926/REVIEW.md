# Review of the endpoint pin-neighborhood chart

**Claim.** One bounded review of the pin-neighborhood reconnaissance. No elder pairing, no global count, and no status change is inferred.

**Source.** Math- PR53 at `9a6f8a660d4508ec273b67d67e6b3871ddf2aa19`, path `reviews/pin_neighborhood_recon_20260926/NOTE.md`, blob `c396e64bf673d7015a077047b79b2bc1f0f023e0`, 7828 bytes, SHA256 `f6efc9c26f07bf873ee7b56bb4c77d16d7c878528aa14650fb68467add5bd3ef`. The companion `algebra_check.py` is blob `f683d8e5e190131c06ffbee401ba3efaddde4ca8`, SHA256 `12ef53137ae21a0ec1f816eef87b12cd50aa39fcf96f1d5bd3338c21458a4242`. It was run and prints `ok`. Those identities are not the conditional-integral argument.

**Imported boundary, not re-reviewed.** PR28 at `dedc69e1b786f7ad148e6b66718277f4145c99cd`, `frontiers/rn_annulus_bridge_20260925/PROOF.md`, blob `6f317515b3d417661f86e2fed09bc7d950899c2b`, SHA256 `d55e2c03bb17e7977ff94130cc1ff21e54840cd1e20dc4e41ea9ad52228beb05`, accepted by merged PR44. Used only for the region `ρ≥A>1`, the six pins, and `Z_r≥c_Z r^2`.

**Not edited.** The PR53 files were not changed.

**Scientific effect: NONE.**

## Provenance

| Item | Value |
|---|---|
| Reviewer model | Grok 4.7, xAI (`grok-4.7-high-fast`) |
| Agent | Cursor cloud session `bc-ff620630-782c-4f77-b994-35d0967e5dce` |
| Provider | xAI. The note is also an xAI reconnaissance, session `bc-3524e567-7204-4e06-a9f5-94d0fd3e7f9d`, of geometry from the OpenAI annulus candidate. Same provider, different session. Organizational independence is not awarded. |
| Source exposure | The note, its algebra script, and the PR28 statement of the annulus domain were read. The dispositions below were rederived. The script's `ok` is not an acceptance. |

## Dispositions

| Interface | Result |
|---|---|
| Endpoint-collision covariance | **ACCEPT** |
| Transverse-cone Jacobian and minor | **ACCEPT** |
| Determinant-product power on that cone | **ACCEPT** |
| Axis-strip exponential penalty | **ACCEPT** |
| Steep strip `r\|p\|<\|q\|<\|p\|` | **ACCEPT** |
| Inner-disk integration | **AMEND** |
| Overlap and stitch to the reviewed annulus | **ACCEPT** |

The summed bound `E[N]≤C r^2 log(1/r)` stays **AMEND**, because it adds the inner square to the three regimes that do close. This is not a counterexample to that bound, and it is not an acceptance of it.

## Endpoint-collision covariance — ACCEPT

Under `Q_r` the six pins include `grad f(M)=0`, so `Cov_{Q_r}(grad f(M))=0`. Inside `|s|≤1/4` the other pin `s=(1,0)` is outside the disk. For `s≠0` the eight evaluations consisting of the six pins and `grad f(X)` are supported at two or three distinct points and are linearly independent as distributions. The periodized covariance of the annulus candidate is positive definite on that set, so the `2×2` conditional covariance is positive definite. Both marginal standard deviations are therefore positive off the pin, and both tend to zero as `s→0` because `grad f(X)→grad f(M)` in `L^2`.

The upper bounds `std(f_x)=O(r^2 max(|q|,r|p|))` and `std(f_z)=O(r max(|q|,r|p|))` on `|p|≤1/4` follow from the degree-4 pin expansion once conditional `C^4` moments are `O(1)`, which is the regression bound already used for `Z_r`. The two-sided comparison `std(f_x)≍r^2|q|` and `std(f_z)≍r|q|` is the cone statement below, not a claim on the axis.

## Transverse cone — ACCEPT

On `|p|≤1/4` the `(S,T,C)` map has minor sum of squares `q^4((p-1/2)^2+q^2/4)`, hence rank drop only at `q=0`. Dividing by `q` sends the random part to `(-T/2,S)`, whose `(S,T)` minor is `1/2`, plus the bounded drift `-6k(p/q)`. For `|p|≤|q|` the coefficient error is `O(r+|q|)`. Large fixed `κ` and `κ r≤|q|≤δ` make `λ_min(Cov Y)≥c>0`. The raw change of variables `(f_x,f_z)=diag(r^2 q, r q) Y` has Jacobian `r^3 q^2`.

Cauchy–Schwarz against those standard deviations keeps the `C^3` cross-covariance with `Y` bounded, and the Gaussian density of `Y` at the origin is bounded. Conditional third-derivative moments at `Y=0` stay `O(1)`.

## Determinant product — ACCEPT on the cone

`grad f(M)=grad f(S)=0` gives `f_xx(M), f_xz(M), f_xx(S), f_xz(S)=O(r M_3)`. On `|p|≤|q|` the witness constraint also gives `f_zz(M)=O(r M_3)`, so `H_M` and, by Lipschitz comparison, `H_X` are `O(r M_3)`. Their determinants are `O(r^2 M_3^2)`. The same constraint at `S` gives `f_zz(S)=O(r M_3/|q|)`, so

`|det H_S|=O(r^2 M_3^2/|q|)`.

For `|q|≥κ r` this is `O(r M_3^2/κ)`. The product of the three absolute determinants is `O(r^5 M_3^6/κ)`. With `Z_r^{-1}=O(r^{-2})` and `p(grad=0)≤C/(r^3 q^2)`,

`ρ≤C/(κ q^2)`

per physical area. The cone has `dp` of width `O(|q|)`, and

`∫_{κ r}^{1/4} r^2 |q|/q^2 dq = O(r^2 log(1/r))`.

The exponent check is `-2-3+5=0` before the `1/q^2`.

## Axis strip — ACCEPT

On `|q|≤r|p|` and `κ r≤|p|≤1/4`, the conditional mean of `ξ=f_x/r^2` is `6k p(p-1)+O(r|p|)`, hence at least `c k |p|` for small `r`, while `std(ξ)=O(r|p|)`. Thus `(E ξ)^2/Var(ξ)≥c k^2/r^2`. The Mahalanobis distance of the gradient is at least this marginal ratio, and the prefactor is at most a power of `r^{-1}` on `|p|≥κ r`. The contribution is `O(r^{-C}) exp(-c/r^2)` and does not affect an `r^2 log(1/r)` budget.

The printed constant `2304` is the exact minimum, at `p=-1/4`, of the pure-`Q` axial ratio `5184/((2p-1)^2)`. In the strip the `T` term is the same order as the `Q` term, so it can reduce the constant. It does not remove the `1/r^2` in the exponent while `k≥k_->0`. That lower threshold on `k` is the one already required for `Z_r`; the penalty is not claimed as `k→0`.

## Steep strip — ACCEPT

On `r|p|<|q|<|p|≤1/4`, outside the inner square, `std(ξ)≍|q|` and the drift is `Θ(|p|)`, so the Gaussian cost is `exp(-c p^2/q^2)`. The cone Jacobian `r^3 q^2`, the three-Hessian majorant `O(r^6 M_3^6/q^6)`, and a conditional moment `(O(|p|/|q|))^6` produce, after division by `Z_r`, an integral `O(r^3 log(1/r))`. For small `r` that is within `O(r^2)`. The absorption is the same comparison the annulus uses: the exponential dominates every negative power of the slope. The pin chart supplies its own powers; they were recomputed here and not quoted from the annulus integral.

## Inner disk — AMEND

The square `|p|≤κ r`, `|q|≤κ r` is where the cone hypothesis `|q|≥κ r` was spent. The paragraph applies that cone's determinant count `O(r^5)` and the normalization `(f_x/r^3,f_z/r^2)` as if they gave a uniform intensity `O(r^{-2})`, with a factor `1/κ^2` cancelling the area `κ^2`.

That uniform bound is not justified. In the leading `(S,T)` chart at `p=0`,

`sqrt(det Cov(grad f)) = r^3 q^2/2`,

so the density prefactor is larger than the Jacobian scale `r^{-5}` by `2 r^2/q^2`. On the square this ratio runs from `2/κ^2` at `|q|=κ r` up to arbitrarily large values as `q→0`. The sentence that `1/κ^2` cancels `κ^2` describes only the outer edge of the square.

The same chart shows why a next-order estimate is required on `p=0`: if `S=T=0`, the displayed linear part of `grad f` vanishes for every `q`. Isolation of the witness, and any integrable determinant factor, comes from jets that this paragraph does not estimate. The pathwise majorant `|det H_S|=O(r^2 M_3^2/|q|)` is also not `O(r^5)` uniformly for `|q|<κ r`.

No replacement integral is supplied here. The cone, axis strip, and steep strip do not cover this square, so they do not restore the summed `r^2 log(1/r)` bound.

## Overlap and stitch — ACCEPT

`|s|≤1/4` around `M=(-1/2,0)` reaches at most `ρ=3/4`. Since `A>1`, the closed collision disk and the annulus `ρ≥A` are disjoint. The distance from `M` to `ρ=A` is `A-1/2>1/2`, and the same separation holds from `S`. Continuing the chart until it meets `ρ≥A` lands in the region PR28/PR44 already estimate, where the witness is separated from both pins by a positive multiple of `r`. The note does not estimate that overlap, and it leaves `1/4<|s|` with `ρ<A` open. The symmetric chart at `S` has the same separation `A-1/2`. Nothing here glues the pin disk to the annulus or extends the count to `ρ<A`.

## Computation

Python 3.12.3, standard library. `check_pin_chart.py` checks the minor identity, the transverse minor `1/2`, both endpoint drifts' difference `12p`, the axial ratio minimum `2304`, the cone exponent `-2-3+5=0`, the overlap `1/2+1/4=3/4<1`, the cone product factor `1/κ`, and the inner-square density ratio `2 r^2/q^2`. The author script was run separately and prints `ok`.
