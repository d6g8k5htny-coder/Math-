# Pin-neighborhood reconnaissance — endpoint chart

Scientific effect: **NONE**. This note does not change `lemma_closed`, prizes, premises, or any status graph. It does not claim elder pairing, a global count, or a numerical constant. Existing review files are not modified and are not used as proofs of the scalings below.

## Conclusion

**(A) Desingularized chart.** Around one endpoint the scaled coordinate `s=(X-M)/r` is enough. Ordinary Kac–Rice is singular exactly when the witness equals that endpoint. Off that point the normalized gradient has an explicit rank and Jacobian ledger. Whether that ledger integrates down to `s=0` is **not** established here (see "Inner disk" below); the transverse cone does integrate, and to a better power than first stated.

**Amended 2026-09-27** after the OpenAI and Claude nonauthor comments on PR #53. Two changes:

1. *Transverse cone.* The first version bounded the conditional three-determinant product by `O(r^5)` and obtained a cone contribution `O(r^2 log(1/r))`. That mechanism was wrong. Under both witness-gradient equations the endpoint determinants satisfy `det(H_M)/r^2 = O(|q|+r)`, `det(H_X)/r^2 = O(|q|+r)`, `det(H_S)/r^2 = O(1)` on the cone, so the product is `O(r^6 (|q|+r)^2)`, the `q^{-2}` of the gradient density cancels, the cone intensity is `O(r)` per physical area and the cone contributes `O(r^3)`. The logarithm was an artifact. The computation is in the "Transverse cone" paragraph and in `algebra_check.py` (`check_contact_determinants`).
2. *Inner disk.* The first version asserted an `O(r^2)` inner-disk contribution from an `O(r^{-2})` intensity. That intensity needs the density of the normalized gradient at `0` to be `O(1)` uniformly on `|P|,|Q| ≤ κ`, which is not shown and is false on the axis `Q=0` without a compensating determinant factor. The inner-disk contribution is therefore **open**, and no punctured-disk bound is claimed.

What the ledger now supports: for the outer cone and the two steep strips, `κ r ≤ |s| ≤ 1/4`,

`E[N(M+r{κ r ≤ |s| ≤ 1/4})] ≤ C r^3`

under the original six pins and the endpoint weight `W_r/Z_r`, all heights, at reconnaissance level (finite-jet identities checked, conditional-moment and uniform-integrability steps stated but not written out). The formerly displayed `E[N(0<|s|≤1/4)] ≤ C r^2 log(1/r)` is withdrawn: it is neither proved nor sharp. The symmetric chart at `S` has the same shape.

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

Through order `r^3`, with free jets `S=f_{zz}(M)`, `T=f_{xxz}(M)`, `C=f_{xzz}(M)`, `D=f_{zzz}(M)`, `Q=f_{xxxx}(M)`, `U=f_{xxxz}(M)`, `V=f_{xxzz}(M)`, `W=f_{xzzz}(M)`, `Z=f_{zzzz}(M)`, the degree-4 pinned jet gives exactly

```
f_x/r^2 = 6k p(p-1) + q(p-1/2) T + (q^2/2) C
          + r [ Q p(2p-1)(p-1)/12 + U q(p^2/2 - 1/6) + V p q^2/2 + W q^3/6 ],
f_z/r   = q S + r [ T p(p-1)/2 + p q C + (q^2/2) D ]
          + r^2 [ U p(p^2-1)/6 + V p^2 q/2 + W p q^2/2 + Z q^3/6 ].
```

For fixed nonzero `(p,q)` the `U, V, W` terms in `f_x/r^2` are order `r`, the same order as the `Q` term; the first version displayed only the `Q` term and hid the others in `O(r^2)`, which was wrong. On the degree-4 jet the expansions above are exact (no remainder); for the actual field the remainder is the degree-5 Taylor term, `O(r^3 |s|^5 M_5)` for `f_x` and `O(r^4 |s|^5 M_5)` for `f_z`, with `M_5` the fifth-derivative bound, which is `O(r^2 |s|^3)` relative to the leading terms shown. `algebra_check.py` matches every coefficient exactly.

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

The raw Jacobian is `∂(f_x,f_z)/∂Y = r^3 q^2`, so the conditional gradient density at `0` is `O(1/(r^3 q^2))` on the cone.

*Determinants at contact (amended).* Impose both witness-gradient equations `f_x(X)=f_z(X)=0` and solve them for `T` and `S`. At leading order,

```
T = -(12k p(p-1) + q^2 C) / (q(2p-1)),
S = -r [ T p(p-1)/2 + p q C + q^2 D/2 ] / q + O(r^2/|q|).
```

On the cone `|p|≤|q|` this gives `S = O(r)`, hence `f_zz(M) = S = O(r)` and `f_zz(S) = S + C r + O(r^2) = O(r)`: **every** entry of all three Hessians is `O(r)`; `H_S` has no "unsuppressed transverse entry" (the first version's mechanism was wrong). Now write `p = t q` and let `q→0`: `T → -12k t` and `S/r → -6k t^2`, so

`det(H_M)/r^2 = -6k (S/r) - T^2/4 + O(r) → 36k^2 t^2 - 36k^2 t^2 = 0.`

The leading rank-one matrices at `M` and at `X` have zero determinant; the first surviving term is linear in `q`. Exactly the same cancellation holds for `H_X`, while `det(H_S)/r^2` has a generally nonzero constant term. Hence on `|q| ≥ κ r`

`det(H_M)/r^2 = O(|q|+r)`, `det(H_X)/r^2 = O(|q|+r)`, `det(H_S)/r^2 = O(1)`,

and the conditional three-determinant product is `O(r^6 (|q|+r)^2)`, not `O(r^5)`. Exact values on the degree-4 jet of `algebra_check.py` (`k=4/3`, `t=1/3`): `det(H_M)/r^2 = -0.697, -0.0652, -0.00648` at `q = 10^{-1}, 10^{-2}, 10^{-3}`, stable in `r ∈ {10^{-2},10^{-3},10^{-4}}`, i.e. `(det(H_M)/r^2)/q ≈ -6.5`; `det(H_X)/r^2` has the same size with opposite sign; `det(H_S)/r^2 ≈ -19`. These `O(·)` statements are conditional-moment scales for the remaining Gaussian jets (`C`, `D`, `Q`, … are unbounded); the Kac–Rice use needs the corresponding `L^p` bounds with uniform integrability, which the bounded conditional `C^3` moment supplies at this reconnaissance level.

With `Z_r^{-1}=O(r^{-2})`, the weighted intensity per physical area is

`ρ ≤ C r^6 q^2 / (r^3 q^2 · r^2) = C r`,

so the `q^{-2}` of the gradient density cancels against the determinant product. The cone has `dp` of width `O(|q|)`; integrating `r^2 dp dq` gives

`∫_{κ r}^{1/4} r^2 · r · |q| dq = O(r^3)`,

with **no logarithm**. The first version's `O(r^2 log(1/r))` on this cone was an artifact of the crude `O(r^5)` product. This independently agrees with the P3 remark in the OpenAI nonauthor comment on PR #53 and with the Claude comment's exact evaluation.

**Steep approach, quartic noise.** `|q|≤r|p|` and `p≠0`. Then `ξ=6k p(p-1)+Θ_p(r p)`: the fluctuation of `ξ` collects the `r Q p(2p-1)(p-1)/12` term and, since `|q| ≤ r|p|` here, the `q(p-1/2)T`, `(q^2/2)C` and `r U q(...)` terms are all `O(r|p|)` as well. So `Var(ξ) ≤ c_1 r^2 p^2` with `c_1` a constant depending on the joint variance of `(Q, T, C, U, V, W)` under the pins, and on `|p|≤1/4`

`(E ξ)^2 / Var(ξ) ≥ c / r^2`

with an unspecified positive `c` (the first version quoted `2304 k^2 / Var(Q)`, which counts only the `Q` noise and is not the right constant; the `r^{-2}` scale is unchanged, and `algebra_check.py` still records the `Q`-only ratio `5184 k^2/((2p-1)^2 Var Q) ≥ 2304 k^2/Var Q` as the `Q` contribution). The density of the gradient at `0` is `O(r^{-C}) exp(-c/r^2)` and does not affect the `r^3` budget.

**Steep approach, still transverse-dominated.** `r|p|<|q|<|p|`. The drift is large compared with `std(ξ)≍|q|`, and the cost is `exp(-c p^2/q^2)`. The same absorption used on the annulus axis integrates this strip to `O(r^3)` once the corrected cone determinant product is used (the Gaussian factor only improves the cone estimate).

**Inner disk — open (amended).** `|p|≤κ r` and `|q|≤κ r`, physical area `O(r^4)`. The normalization `(f_x/r^3, f_z/r^2)` has Jacobian `r^5`; that much is correct. But an intensity `O(r^{-2})` requires the density of the normalized vector at `0` to be `O(1)` uniformly on `|P|,|Q|≤κ` (`p=rP`, `q=rQ`), and it is not: the order-one fluctuations of the normalized vector are `-(Q/2)T` and `Q S`, so its `(S,T)` minor is `Q^2/2` — the `q^4((p-1/2)^2+q^2/4)` ledger restricted to the disk. On the axis `Q=0` every jet coefficient of the normalized vector is `O(rP)` (exact on the degree-4 jet: at `r=1/100` and `P=1/2, 1/10, 1/100` the `T`-coefficient of `f_z/r^2` is `-2.5e-3, -5.0e-4, -5.0e-5` and the `Q`-coefficient of `f_x/r^3` is `4.1e-4, 8.3e-5, 8.3e-6`). The density at zero is therefore `≍ 1/(r^5 Q^2)` off the axis, and integrability as `s→0` needs the determinant repulsion `det H_M, det H_X = O(|s|)` under both vanishing gradients — the same cancellation as on the cone, but now uniformly down to the pin — which this note does not prove. "The point `s=0` is not included" is not a majorant. What is needed is a two-point `(M,X)` critical-pair normalization, or an explicit Schur lower bound on `Cov(f_x/r^3, f_z/r^2)` with the compensating determinant factor (the OpenAI P5 and Claude item 2 comments ask for the same object; merged Math- #82 and #90 record the constrained `det H_M` cancellation and a bounded microdisk note for this region and should be consulted before any new attempt). Until then the inner disk contributes an unknown amount and no punctured-disk bound is claimed.

Adding the three outer regimes gives the `O(r^3)` bound on `κ r ≤ |s| ≤ 1/4` stated in the Conclusion. The point `s=0` is the conditioned pin, not an extra witness, but excluding it does not by itself make the inner-disk integral finite.

## Overlap with the reviewed annulus

The collision disk `|s|≤1/4` and the annulus `ρ≥A>1` are disjoint, because `|s|≤1/4` implies `ρ≤3/4<1<A`.

A direct stitch needs the same chart continued to some radius `s_out≥A-1/2`. The distance from `M` to the circle `ρ=A` is `A-1/2>1/2`. On the collar

`A ≤ sqrt((p-1/2)^2+q^2) ≤ A_1`, `|s|≤s_out`,

with `A<A_1<B` and `s_out≥A_1+1/2`, one has `|s|≥A-1/2>1/2`. The witness is then separated from both pins by a positive multiple of `r`, which is the non-collision regime already estimated by PR28/PR44. This note does not re-prove that collar. Stopping at `|s|=1/4` leaves the region `1/4<|s|` and `ρ<A` open.

The symmetric `S` chart uses `s'=(X-S)/r` and the same overlap test against `ρ≥A`, with separation `A-1/2` from `S`.

## Not claimed

No global count on the disk `ρ<A`, no height-window factor, no lower bound, no elder or lifetime statement, and no identification of `C` or `r_*`. The `O(r^3)` ledger covers `κ r ≤ |s| ≤ 1/4` only; the inner disk `|s| ≤ κ r` is open, so no all-height punctured-disk count is claimed and the withdrawn `O(r^2 log(1/r))` is not replaced by a disk bound. Promoting any of this, or gluing it to PR28, is a later argument.

## Computation

`python3 -B -S reviews/pin_neighborhood_recon_20260926/algebra_check.py`

```sh
python3 -B -O -S reviews/pin_neighborhood_recon_20260926/algebra_check.py
python3 -B -S reviews/pin_neighborhood_recon_20260926/algebra_check.py --mutate   # negative control, must exit nonzero
```

Script SHA256 `449d93419aaf2f8242b4cf152279db6237d709dbd372fec0ef5fbe865c5c52f5` (amended; the first version was `12ef53137ae21a0ec1f816eef87b12cd50aa39fcf96f1d5bd3338c21458a4242`). It checks the full degree-4 pin expansion including the `U,V,W,Z` terms, both cubic drifts, the minor `q^4((p-1/2)^2+q^2/4)`, the transverse minor `1/2`, the `Q`-only axis ratio, the overlap inequality `A-1/2>1/2` for every `A>1`, and — new — the contact-limit determinant cancellation: after solving both witness-gradient equations for `(T,S)` on the degree-4 jet, `det(H_M)/r^2` and `det(H_X)/r^2` are bounded by a fixed multiple of `|q|+r` while `det(H_S)/r^2` stays of order one, and the exact limit identity `-6k(-6kt^2) - (12kt)^2/4 = 0`. Checks raise explicit exceptions rather than `assert`, so `python -O` does not weaken them, and `--mutate` injects a wrong pin solve that must be detected. The script checks finite jet identities only.

## Provenance

| Field | Value |
|---|---|
| Provider | xAI |
| Model | Grok 4.7 (`grok-4.7-high-fast`) |
| Agent | Cursor cloud run `bc-3524e567-7204-4e06-a9f5-94d0fd3e7f9d` |
| Run URL | https://cursor.com/agents/bc-3524e567-7204-4e06-a9f5-94d0fd3e7f9d |

Organizational independence is not awarded. The candidate geometry this chart attaches to was authored by OpenAI. This note is a nonauthor reconnaissance of the endpoint scaling.
