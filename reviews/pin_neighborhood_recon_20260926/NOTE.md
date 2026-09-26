# Pin-neighborhood reconnaissance — endpoint chart

Scientific effect: **NONE**. This note does not change `lemma_closed`, prizes, premises, or any status graph. It does not claim elder pairing, a global count, or a numerical constant. Existing review files are not modified and are not used as proofs of the scalings below.

## Conclusion

**(A) Desingularized chart.** Around one endpoint the scaled coordinate `s=(X-M)/r` is enough. Ordinary Kac–Rice is singular exactly when the witness equals that endpoint. Off that point the normalized gradient has an explicit rank and Jacobian ledger, and the ledger is integrable. No further base blow-up is required to state a count lemma.

The bound the ledger supports, for the punctured disk `0<|s|≤1/4` and for small `r`, is

`E[N(M+r{0<|s|≤1/4})] ≤ C r^2 log(1/r)`

under the original six pins and the endpoint weight `W_r/Z_r`, all heights. The symmetric chart at `S` has the same shape. This is larger than the reviewed annulus power `r^3` and is not asserted to be sharp.

## Outer boundary, imported only

Merged PR28 at `dedc69e1b786f7ad148e6b66718277f4145c99cd`, `frontiers/rn_annulus_bridge_20260925/PROOF.md`, blob `6f317515b3d417661f86e2fed09bc7d950899c2b`, SHA256 `d55e2c03bb17e7977ff94130cc1ff21e54840cd1e20dc4e41ea9ad52228beb05`, as accepted by merged PR44. That theorem covers the fixed annulus `A≤sqrt(u^2+v^2)≤B` with `1<A<B<∞`, all heights, and gives physical intensity `O(r)`. It excludes the open disk `sqrt(u^2+v^2)<A`. Both pins sit in that disk: in midpoint coordinates they are `(u,v)=(±1/2,0)`.

Pins, unchanged:

`M=(-r/2,0)`, `S=(r/2,0)`,
`f(M)=b`, `f(S)=b-k r^3`, `grad f(M)=grad f(S)=0`.

`Q_r` is the Gaussian regression on those six values. `W_r=F_2(H_M)F_1(H_S)` and `Z_r=E_{Q_r} W_r≥c_Z r^2` are taken from that same endpoint normalizer. They are not re-proved here.

## Chart

Set `X=M+r s` with `s=(p,q)`, so the midpoint coordinates are `u=p-1/2`, `v=q`. The disk `|s|≤1/4` stays inside `ρ≤3/4<A`, so it does not meet the reviewed annulus. The other pin is `s=(1,0)`, outside this disk.

On the conditional-mean cubic,

`f_x(M+r(p,0))/r^2 = 6 k p(p-1)`.

At `S`, the symmetric chart `X=S+r(p',q')` has

`f_x(S+r(p',0))/r^2 = 6 k p'(p'+1)`.

The rest of the note is the `M` chart. The `S` chart is the same ledger with this drift.

Through order `r^3`, with free jets `S=f_{zz}(M)`, `T=f_{xxz}(M)`, `C=f_{xzz}(M)`, `Q=f_{xxxx}(M)`,

```
f_x/r^2 = 6k p(p-1) + q(p-1/2) T + (q^2/2) C
          + r Q p(2p-1)(p-1)/12 + O(r^2),
f_z/r   = q S + r [T p(p-1)/2 + p q C + (q^2/2) f_{zzz}(M)] + O(r^2).
```

The displayed `O(r)` and `O(r^2)` coefficients are linear forms in the remaining degree-4 jets. They were matched exactly on that jet.

## Where ordinary Kac–Rice is singular

`grad f(M)` is one of the six pins, so under `Q_r` it is the zero vector almost surely and

`Cov_{Q_r}(grad f(M)) = 0`.

That is the whole singularity locus of the un-normalized gradient covariance. For `s≠0`, `X` is a different point from `M` and from `S` inside `|s|≤1/4`. Distinct-site derivative evaluations stay nondegenerate for this periodic covariance at each fixed `r>0`, so the `2×2` conditional covariance is positive definite off the pin. Its eigenvalues tend to `0` as `s→0` because `grad f(X)→grad f(M)=0` in `L^2`.

The rate is read off the expansion. For `|p|≤1/4`,

`std(f_x) = O(r^2 max(|q|, r|p|))`, `std(f_z) = O(r max(|q|, r|p|))`.

Both vanish at `s=0` and nowhere else in the closed disk.

## Rank ledger

Write `ξ=f_x/r^2` and `ζ=f_z/r`. The order-zero map on `(S,T,C)` is

```
( q(p-1/2) T + (q^2/2) C , q S ).
```

The sum of squares of its `2×2` minors equals

`q^4 ((p-1/2)^2 + q^2/4)`.

It vanishes if and only if `q=0`. On the axis the limit covariance of `(ξ,ζ)` is the zero matrix; the first noise is the order-`r` quartic term.

Three regimes cover `0<|s|≤1/4`.

**Transverse cone.** `|q|≥r|p|` and `|p|≤|q|`. Divide by `q`:

`Y=(ξ/q, ζ/q) → (-T/2, S)`

as `r/|q|→0` and `q→0`, up to the bounded drift `-6k(p/q)`. The `(S,T)` minor of that limit is `1/2`, independent of the slope `p/q`. For large fixed `κ` and `κ r≤|q|≤1/4`, the `O(r/|q|+|q|)` jet remainder keeps `λ_min(Cov Y)≥c>0`. Cauchy–Schwarz against `std(f_x)≍r^2|q|` and `std(f_z)≍r|q|` keeps the cross-covariance of every third derivative with `Y` bounded, so the conditional `C^3` moment at `Y=0` stays bounded.

The raw Jacobian is `∂(f_x,f_z)/∂Y = r^3 q^2`. Three-gradient geometry in this cone gives `||H_M||` and `||H_X||` of order `r M_3`, while `H_S` keeps one factor `r` and one unsuppressed transverse entry. The conditional determinant product is `O(r^5)`. With `Z_r^{-1}=O(r^{-2})`,

`ρ ≤ C / q^2`

per physical area. The cone has `dp` of width `O(|q|)`. Integrating `r^2 dp dq` produces

`∫_{κ r}^{1/4} r^2 |q| / q^2 dq = O(r^2 log(1/r))`.

**Steep approach, quartic noise.** `|q|≤r|p|` and `p≠0`. Then `ξ=6k p(p-1)+Θ_p(r p)`. On `|p|≤1/4`,

`(E ξ)^2 / Var(ξ) ≥ (2304 k^2 / Var(Q)) / r^2`

at leading order, since the ratio `5184 k^2/((2p-1)^2 Var(Q))` is at least `2304 k^2/Var(Q)`. The density of the gradient at `0` is `O(r^{-C}) exp(-c/r^2)` and does not affect the `r^2 log(1/r)` budget.

**Steep approach, still transverse-dominated.** `r|p|<|q|<|p|`. The drift is large compared with `std(ξ)≍|q|`, and the cost is `exp(-c p^2/q^2)`. The same absorption used on the annulus axis integrates this strip to `O(r^2)`.

**Inner disk.** `|p|≤κ r` and `|q|≤κ r`, physical area `O(r^4)`. The normalization `(f_x/r^3, f_z/r^2)` has Jacobian `r^5`. The same determinant count `O(r^5)` and normalizer `r^{-2}` give intensity `O(r^{-2})`, hence expected count `O(r^2)`. The factor `1/κ^2` in the density cancels the area factor `κ^2`.

Adding the regimes gives the punctured-disk bound above. The point `s=0` is not included in the integral. It is the conditioned pin, not an extra witness.

## Overlap with the reviewed annulus

The collision disk `|s|≤1/4` and the annulus `ρ≥A>1` are disjoint, because `|s|≤1/4` implies `ρ≤3/4<1<A`.

A direct stitch needs the same chart continued to some radius `s_out≥A-1/2`. The distance from `M` to the circle `ρ=A` is `A-1/2>1/2`. On the collar

`A ≤ sqrt((p-1/2)^2+q^2) ≤ A_1`, `|s|≤s_out`,

with `A<A_1<B` and `s_out≥A_1+1/2`, one has `|s|≥A-1/2>1/2`. The witness is then separated from both pins by a positive multiple of `r`, which is the non-collision regime already estimated by PR28/PR44. This note does not re-prove that collar. Stopping at `|s|=1/4` leaves the region `1/4<|s|` and `ρ<A` open.

The symmetric `S` chart uses `s'=(X-S)/r` and the same overlap test against `ρ≥A`, with separation `A-1/2` from `S`.

## Not claimed

No global count on the disk `ρ<A`, no height-window factor, no lower bound, no elder or lifetime statement, and no identification of `C` or `r_*`. The `O(r^2 log(1/r))` ledger is the pin-disk upper bound only. Promoting it, or gluing it to PR28, is a later argument.

## Computation

`python3 -B -S reviews/pin_neighborhood_recon_20260926/algebra_check.py`

Script SHA256 `12ef53137ae21a0ec1f816eef87b12cd50aa39fcf96f1d5bd3338c21458a4242`. It checks the degree-4 pin expansion, both cubic drifts, the minor `q^4((p-1/2)^2+q^2/4)`, the transverse minor `1/2`, the axis ratio `2304`, and the overlap inequality `A-1/2>1/2`.

## Provenance

| Field | Value |
|---|---|
| Provider | xAI |
| Model | Grok 4.7 (`grok-4.7-high-fast`) |
| Agent | Cursor cloud run `bc-3524e567-7204-4e06-a9f5-94d0fd3e7f9d` |
| Run URL | https://cursor.com/agents/bc-3524e567-7204-4e06-a9f5-94d0fd3e7f9d |

Organizational independence is not awarded. The candidate geometry this chart attaches to was authored by OpenAI. This note is a nonauthor reconnaissance of the endpoint scaling.
