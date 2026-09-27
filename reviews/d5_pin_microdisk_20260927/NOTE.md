# D5 pin microdisk note — divided-difference frame and the nested-axis obstruction

**Object:** D5-PIN-MICRODISK-20260927-v1  
**Author lane:** OpenAI. **Scientific effect:** **NONE**. This additive note does not close D5, does not change `lemma_closed`, prizes, premises, `STATUS`, `PROOF_INDEX`, or any graph classification, and does not edit PR53 or the reviewed annulus sources.

## Scope

This is one bounded author-side microdisk task for [Math #58](https://github.com/d6g8k5htny-coder/Math-/issues/58), using the original six endpoint pins

`M=(-r/2,0)`, `S=(r/2,0)`,
`f(M)=b`, `f(S)=b-k r^3`, `grad f(M)=grad f(S)=0`,

with witness chart

`X=M+r(p,q)=(-r/2+r p, r q)`,

and the nested microdisk

`p=r P`, `q=r Q`

so the physical witness distance from `M` is `O(r^2)`.

Input source identities:

- PR53 reconnaissance note at commit `9a6f8a660d4508ec273b67d67e6b3871ddf2aa19`, path `reviews/pin_neighborhood_recon_20260926/NOTE.md`, blob `c396e64bf673d7015a077047b79b2bc1f0f023e0`.
- PR55 review at commit `4e188e25b1e1ef560f3eeb75c0d354d2ccf0ea22`, path `reviews/d5_pin_neighborhood_20260926/REVIEW.md`, blob `11a6b8d0d9a3b57f3c391975a524bf6bdabd3b8e`.
- The reviewed fixed annulus remains the merged PR28/PR44 lane already cited in `PROOF_INDEX.md`.

The local exact algebra packet here is finite evidence only. It is not a continuum proof, not a new review, and not an annulus collar argument.

## Exact six-pin cubic and two-point divided differences

Using the same exact six-pin cubic ansatz as the retained finite-`r` repair lane,

```text
f_x/r^2 = 6k p(p-1) + T q (p-1/2) + (C/2) q^2,
f_z/r   = A q + r [T p(p-1)/2 + C q (p-1/2) + (D/2) q^2],
```

with free jets `(A,T,C,D)=(f_zz(M), f_xxz(M), f_xzz(M), f_zzz(M))`.

Because `grad f(M)=0` is one of the six pins, ordinary Kac–Rice degenerates at `X=M`. For `q != 0`, the two-point divided-difference rows

```text
Delta_x := (f_x(X)-f_x(M)) / (r^2 q),
Delta_z := (f_z(X)-f_z(M)) / (r q),
```

are exact and equal to

```text
Delta_x = 6k p(p-1)/q + T (p-1/2) + (C/2) q,
Delta_z = A + r [T p(p-1)/(2q) + C (p-1/2) + (D/2) q].
```

Relative to the jet columns `(A,T,C,D)`, the reduced frame is

```text
[ 0, p-1/2,          q/2,     0   ]
[ 1, r p(p-1)/(2q), r(p-1/2), r q/2 ].
```

The `(A,T)` minor is exactly

```text
1/2 - p.
```

Hence the reduced frame stays nondegenerate as `X -> M` provided the approach is off-axis (`q != 0`) and `|p| < 1/2`. In the nested chart `p=rP`, `q=rQ`,

```text
Delta_x = -6k P/Q - T/2 + O(r),
Delta_z = A + O(r),
```

with exact Jacobian scaling

```text
d(f_x,f_z) = r^3 q^2 d(Delta_x,Delta_z) = r^5 Q^2 d(Delta_x,Delta_z).
```

So the covariance/gradient-density singularity is the familiar `q^-2` one, but the frame itself does not lose rank off the axis.

## Exact axis solve and soft determinant factors

On the axis branch `p=0`, `q != 0`, the witness-gradient equations from the same cubic packet solve exactly as

```text
T = C q,
A = r (C - D q)/2.
```

Substituting those relations into the three Hessian determinants gives exact `q` divisibility at `M` and at `X`:

```text
det H_M = q * [r^2 (3k D - C^2 q/4)],
det H_X = q * [r^2 (-3k D - C^2 q/4 + C D q^2/2)],
det H_S = r^2 [6k C - 3k D q - C^2 q^2/4].
```

The algebra packet therefore certifies the extra soft transverse factor at `M` and `X`, and only `q^2` divisibility for the triple product. This exact finite cubic check is the author-side mechanism behind the regularized transverse-cone ledger; it is **not** a proof of the full conditional Gaussian moment estimate.

## Outer transverse cancellation rechecked

The bounded claim supported here is the same soft-cancellation mechanism stated in the issue packet:

- the reduced gradient density contributes `p_{grad(X)}(0) ~ q^-2`;
- after imposing `grad f(X)=0`, the witness determinant picks up one soft transverse factor (`E|det H_X| = O(r q)` in the planar BF ledger);
- polar area contributes one more `q`.

So `p_0 * E|det H_X| * q` is regular as `q ↓ 0`. Forgetting that soft factor would leave a logarithmic divergence.

This note does **not** upgrade that regularity to a uniform all-microdisk majorant, because the remaining on-axis nested disk is not resolved here.

## Obstruction returned by this bounded task

The off-axis divided-difference frame is nondegenerate and the outer cone cancellation is favorable, but the named obstruction remains:

1. the `9`-pin Gram is still singular on the axis;
2. the nested microdisk `q=O(r^2)` with `Q -> 0` is not covered by the off-axis divided-difference frame;
3. no uniform `E_{Q_r}[N_mu W_r]/Z_r` lemma is proved here;
4. the collar from the pin chart to the reviewed fixed annulus is still missing.

Therefore this bounded task returns **obstruction remains** rather than a uniform microdisk majorant. The all-height `O(r^3)` pin-neighborhood lemma is **not** certified here. D5 stays **AMEND**.

## Exact packet contents

- `microdisk_exact.py` prints `RESULTS.json`.
- `test_microdisk_exact.py` contains exact `Fraction` checks for the divided-difference rows, nested Jacobian scaling, axis witness solve, and soft determinant factors.
- `run_validation.py --output NEW_DIRECTORY_OUTSIDE_THIS_TREE` runs the tests in normal and optimized mode and checks deliberate mutants.

`SOURCE_FILES.json` records byte identities for this additive packet only. The tests are finite exact algebra checks, not a continuum proof.
