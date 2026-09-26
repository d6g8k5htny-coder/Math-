# D5 obstruction ledger — transverse cone vs Hessian product

Date: 2026-09-26
Author-side packet: Harper cycle-4 (D)
Scientific effect: NONE. This is a power-counting isolation, not a count lemma and not a review.

Scope: planar Bargmann–Fock, d=2, original six endpoint pins
`f(M)=b`, `f(S)=b-k r^3`, `grad f(M)=grad f(S)=0`,
`M` and `S` a distance `r` apart on an axis `t`, transverse coordinate `s`.
Witness chart: `X = M + r(p,q)`. Transverse cone: `|q| >= max(kappa r, |p|)` and `|q| <= 1/4`.
On-axis slice of the cone: `p=0`.

Parent objects used only as cited sources:
- pin-neighborhood reconnaissance (Math- `9a6f8a66`, PR53 note)
- AMEND review (Math- `4e188e25`)
- Math-#58 task statement
- reviewed fixed-annulus / transverse-bound candidate (PR16 / PR22 / PR28 scopes)

No object below is promoted.

## 1. Two different powers in circulation

Three incompatible-looking expressions appear in the public notes:

1. raw gradient Jacobian on the pin chart: `O(r^3 q^2)`
2. crude recon determinant product: `O(r^5)`
3. Math-#58 suggested product after “soft transverse factors”: `O(r^6 q^2)`

The reviewed fixed-annulus bound uses a fourth expression, `W_r |det H_X| = O(r^6)`, valid only for `|v| >= eta > 0` and `A <= |s| <= B`.

These are not four estimates of one quantity. They mix a coordinate Jacobian with a slaved Hessian product, and they mix the annulus slaving of the far endpoint with the pin-cone geometry.

## 2. Mixed slaving that feeds the Jacobian (closed, planar BF)

On planar BF with `E[f(x)f(y)] = exp(-|x-y|^2/2)`:

```
Var(f_ts(M) | six pins) = (e^{r^2} - 1 - r^2) / (e^{r^2} - 1).
```

Proof: `f_ts(M)` is orthogonal to `{f, f_t, f_s}(M)` and to `{f, f_t}(S)`. The only surviving cross is

```
Cov(f_ts(M), f_s(S)) = r e^{-r^2/2},
Cov(f_s(M), f_s(S)) = e^{-r^2/2},
Var(f_ts) = Var(f_s) = 1.
```

Two-pin Schur on `(f_s(M), f_s(S))` produces the displayed rational. Write `beta := f_ts(M)/r`. Then

```
Var(beta | pins) = (e^{r^2} - 1 - r^2) / (r^2 (e^{r^2} - 1)) -> 1/2
```

as `r -> 0`, so `f_ts(M) = O_p(r)` after pins. This is the extra factor of `r` in the pin-chart Jacobian.

## 3. Coordinate object: the gradient Jacobian

Unconditional third-jet Taylor at `p=0`:

```
f_t(X) = r q f_ts(M) + (r^2/2) q^2 f_tss(M) + O(r^3)
       = r^2 q beta + (r^2/2) q^2 f_tss + O(r^3),
f_s(X) = r q f_ss(M) + (r^2/2) q^2 f_sss(M) + O(r^3).
```

Let `S := f_ss(M)` (contact, order one before imposing `grad f(X)=0`) and `Y = (beta, S)`.
The leading map `Y |-> (f_t, f_s)` has Jacobian matrix `diag(r^2 q, r q)` and determinant

```
partial(f_t, f_s) / partial(beta, S) = r^3 q^2.
```

This matches the PR53 raw Jacobian and the AMEND-review identity
`sqrt(det Cov(grad f)) = r^3 q^2 / 2` on the leading `(S,T)` chart at `p=0`
(the factor `1/2` is `sqrt(det Cov(beta,S))` in the recon limit minor).

The axial-belt chart `X = R(r u, r^2 w)` uses the normalized map `(f_t/r^3, f_s/r^2)` with Jacobian `r^5`. On the overlap `|q| ~ r` one has `r^3 q^2 ~ r^5`. Same geometric density, different coordinates.

Verdict: `O(r^3 q^2)` versus `O(r^5)` is a coordinate rewrite. It is not an obstruction and not a congruence statement. The AMEND-review remark that the pin-disk density prefactor exceeds the axial scale `r^{-5}` by `2 r^2/q^2` is exactly the Jacobian ratio `r^5 / (r^3 q^2)`.

## 4. Congruence object: Hessian product on `{grad f(X)=0}`

Imposing `grad f(X)=0` at `p=0` slaves the endpoint jets:

```
beta = - (q/2) f_tss + O(r),
S    = - (r q / 2) f_sss + O(r^2).
```

Thus on the event, `S = O(r |q|)` and `beta = O(|q|)`.
Endpoint Hessian at `M`:

```
H_M = [[f_tt(M), f_ts(M)], [f_ts(M), f_ss(M)]]
    = [[-6 k r + O(r^3), r beta], [r beta, S]].
```

So

```
det H_M = (-6 k r) S - r^2 beta^2 + O(r^3 |q|)
        = O(k r^2 |q|) + O(r^2 q^2).
```

Transport to the witness by `H_X = H_M + r q * (third jets) + O(r^2)` and substitute the same slaving:

```
f_ss(X) = S + r q f_sss + O(r^2) = -S + O(r^2) = O(r |q|),
f_tt(X) = -6 k r + O(r |q|),
f_ts(X) = r beta + r q f_tss + O(r^2) = - r beta + O(r^2) = O(r |q|),
det H_X = O(k r^2 |q|).
```

Far-endpoint Hessian `H_S`: the witness sits at physical distance `Theta(r |q|)` from `M` and distance `Theta(r)` from `S`. The two gradient equations at `X` do not constrain `f_ss(S)`. After the original pins only,

```
f_tt(S) = 6 k r + O(r^3),    f_ss(S) = a_S = O_p(1),
det H_S = O(k r).
```

Three-determinant product on the on-axis cone:

```
det H_M * det H_X * det H_S = O(k^3 r^5 q^2).
```

If `W_r = |det H_M det H_S|`, then `W_r |det H_X| = O(k^3 r^5 q^2)` on this slice.

## 5. Why Math-#58 `O(r^6 q^2)` over-counts one power of `r`

The reviewed annulus (`|v| >= eta`, `A <= |s| <= B`) does slave `f_zz` at both endpoints:

```
0 = r(u+1/2) f_xz(M) + r v f_zz(M) + O(r^2 M_3),
```

and `|v| >= eta` forces `f_zz(M) = O(r)`, hence `det H_M = O(r^2)` and likewise `det H_S = O(r^2)`, hence `W_r |det H_X| = O(r^6)` as in the transverse-bound candidate.

Transporting that far-endpoint slaving onto the pin cone is a congruence error: a witness adjacent to `M` does not see `S`. Replacing `det H_S = O(r)` by `det H_S = O(r^2)` manufactures the extra `r` in `O(r^6 q^2)`.

Verdict: `O(r^6 q^2)` is the annulus product written in cone coordinates, not the cone product.

## 6. What this does not close

- Inner square `|p|,|q| <= kappa r`. On `p=0`, if `beta = S = 0` the displayed linear part of `grad f` vanishes for every `q`. Isolation is then carried by third jets that the cone ledger does not estimate. The AMEND-review pathwise majorant `|det H_S| = O(r^2 M_3^2 / |q|)` is not `O(r^5)` uniformly for `|q| < kappa r`. No replacement integral is supplied here.
- Nested microdisk `s = r S` (physical distance `O(r^2)`). Math-#58 remains open. A two-point divided-difference frame that stays nondegenerate as `X -> M` is not constructed in this note.
- Intermediate belt `r << |x| << rho` and shrinking-separation collisions remain open as recorded in `PROOF_INDEX.md`.
- No all-height `O(r^3)` pin-neighborhood expected-count lemma is claimed. A formal Kac–Rice assembly from the cone product `O(k^3 r^5 q^2)`, the Jacobian `r^3 q^2`, physical area `r^2 dp dq`, and `Z_r = Theta(k^2 r^2)` produces an `O(k r^2)` cone contribution after the `q^2` cancels, but that assembly is not a proof: remainder control, index indicators, and the inner-square gap are missing.

## 7. One-line ledger

| Object | Power | Kind | Status |
|---|---|---|---|
| pin-chart Jacobian at `p=0` | `r^3 q^2` | coordinate | matches PR53 / AMEND-review; equals axial `r^5` at `|q|~r` |
| slaved `det H_M` on-axis cone | `O(k r^2 \|q\|)` | congruence | from `{grad f(X)=0}` + `f_tt(M)~-6kr` |
| slaved `det H_X` on-axis cone | `O(k r^2 \|q\|)` | congruence | transport of the same slaving |
| `det H_S` on pin cone | `O(k r)` | congruence | far endpoint, transverse contact unslaved |
| three-det product on-axis cone | `O(k^3 r^5 q^2)` | congruence | this note |
| #58 product `O(r^6 q^2)` | extra `r` | error | over-slaves `det H_S` by copying the annulus |
| annulus product | `O(r^6)` | congruence | accepted on `|v|>=eta`, not on the pin disk |
| inner square / microdisk | — | missing | AMEND; linear part vanishes; needs third-jet blow-up |

D5 pin-neighborhood remains AMEND. This ledger does not restore `O(r^2 log(1/r))` and does not claim `O(r^3)`.
