# D5 obstruction ledger — transverse cone vs Hessian product

Date: 2026-09-26. Revised candidate: 2026-09-27.
Author-side packet: Harper cycle-4 (D)
Scientific effect: NONE. This is a power-counting isolation, not a count lemma and not a review.

Preserved predecessor of this file: commit `05c20b67ca49281601532f7a0224f871a8dae8d6`, SHA256 `ba0f5f2e48ea9704d9078fe26a042815b7228a261c7685010a28bd9e6c0ca57b`. Review `5332391136` binds to that head only and is not carried here. The rational denominator repair in `CLOSED_FORMS_FTS_FTT.md` is unchanged. Two stronger assertions of the predecessor (the deterministic `f_tt = ∓6kr + O(r^3)` display, and the claim that a marginal `f_ss(S) = O_p(1)` rules out a refined `r^6 q^2` product) are withdrawn in Sections 4 and 5. D5, SARD-G A1, and A6 remain AMEND.

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

Unconditional third-jet Taylor at `p=0`, where the displacement from `M` is `r q e_s` and the pinned values `f_t(M) = f_s(M) = 0` remove the constant terms:

```
f_t(X) = r q f_ts(M) + (r^2/2) q^2 f_tss(M) + O(r^3 |q|^3)
       = r^2 q beta + (r^2/2) q^2 f_tss + O(r^3 |q|^3),
f_s(X) = r q f_ss(M) + (r^2/2) q^2 f_sss(M) + O(r^3 |q|^3).
```

The remainders carry the full displacement power `(r|q|)^3`; writing them as a bare `O(r^3)` would lose the `q` factors that are divided out below and would leave an `O(r/q)` term that is only `O(1)` at the cone boundary `|q| = Theta(r)`. Here and below, `O(.)` applied to a Gaussian jet or to a polynomial in Gaussian jets denotes a conditional-moment (`O_p`, or `L^p` for each fixed `p`) scale, not a pathwise bound: conditioned Gaussian variables remain unbounded. A Kac–Rice assembly that uses these scales needs `L^p` bounds together with uniform integrability, or an explicit truncation with a separately bounded tail. That assembly is not performed in this note.

Let `S := f_ss(M)` (contact, order one before imposing `grad f(X)=0`) and `Y = (beta, S)`.
The leading map `Y |-> (f_t, f_s)` has Jacobian matrix `diag(r^2 q, r q)` and determinant

```
partial(f_t, f_s) / partial(beta, S) = r^3 q^2.
```

This matches the PR53 raw Jacobian and the AMEND-review identity
`sqrt(det Cov(grad f)) = r^3 q^2 / 2` on the leading `(S,T)` chart at `p=0` up to the constant. The constants differ because the charts differ: in the `(beta, S)` chart used here, `Var(beta | pins) -> 1/2` (Section 2), `Var(S | pins) -> 2` (the `f_ss` slot after pins; see `../benjamin/REDUCED_FRAME_4SLOT.md`), and `Cov(beta, S | pins) = 0` by `s`-parity, so `sqrt(det Cov(beta, S | pins)) -> 1` and the leading conditional gradient density has scale `1 / (r^3 q^2)` with constant `1`, not `1/2`. The `1/2` in the recon note is the minor of its `(S, T)` chart with `T` a third jet. Constants do not enter the power ledger below. (Amended 2026-09-27; an earlier version attributed the `1/2` to `sqrt(det Cov(beta, S))`, which is off by a factor of two.)

The axial-belt chart `X = R(r u, r^2 w)` uses the normalized map `(f_t/r^3, f_s/r^2)` with Jacobian `r^5`. On the overlap `|q| ~ r` one has `r^3 q^2 ~ r^5`. Same geometric density, different coordinates.

Verdict: `O(r^3 q^2)` versus `O(r^5)` is a coordinate rewrite. It is not an obstruction and not a congruence statement. The AMEND-review remark that the pin-disk density prefactor exceeds the axial scale `r^{-5}` by `2 r^2/q^2` is exactly the Jacobian ratio `r^5 / (r^3 q^2)`.

## 4. Congruence object: Hessian product on `{grad f(X)=0}`

Imposing `grad f(X)=0` at `p=0` and dividing the two displayed equations by `r^2 q` and by `r q` respectively slaves the endpoint jets:

```
beta = - (q/2) f_tss + O(r q^2),
S    = - (r q / 2) f_sss + O(r^2 q^2).
```

The remainders are uniform on the cone `|q| <= 1/4` because the Taylor remainders above retain the displacement factor. Thus on the event, `S = O_p(r |q|)` and `beta = O_p(|q|)` in the conditional-moment sense stated in Section 3.
Endpoint axial second derivative at `M`, conditional on the six pins. Transverse pins drop out of this regression by `s`-parity, so the conditional law is the four-pin law on `{f, f_t}` at both ends, with values `(f(M), f_t(M), f(S), f_t(S)) = (b, 0, b - k r^3, 0)`. Write

```
f_tt(M) = μ_M + ζ_M,
μ_M := E[f_tt(M) | six pins],
```

where `ζ_M` is centered Gaussian. Its variance does not depend on `(b, k)` and is identity TT of `CLOSED_FORMS_FTS_FTT.md`:

```
Var(ζ_M) = Var(f_tt(M) | six pins)
         = r^4/6 - r^6/30 + r^8/360 - r^{10}/12600 + O(r^{12}).
```

The leading term is `r^4/6`, so the conditional standard deviation is `r^2/sqrt(6) * (1 + O(r^2))`. In the conditional-moment sense of Section 3, `ζ_M = O_p(r^2)`. The predecessor display `f_tt(M) = -6 k r + O(r^3)` is withdrawn: a centered Gaussian of variance `~ r^4/6` is not an `O(r^3)` remainder.

The conditional mean is a separate deterministic function of `(b, k, r)`. Exact series division of the four-pin regression (same Gram and cross vector as identity TT; `test_ftt_conditional_mean.py`) gives

```
μ_M = -6 k r - (b/4) r^2 + k r^3 + (b/24) r^4 - (k/20) r^5
      - (b/192) r^6 - (k/120) r^7 + (b/5760) r^8 + O(r^9).
```

The coefficient of `r^2` is `-b/4`. The conditional mean itself is therefore `-6 k r - (b/4) r^2 + k r^3 + O(r^4)`, which is a mean expansion, not a bound on the random variable. Setting `α_M := f_tt(M)/r` rewrites `μ_M = r E[α_M | 4-pin]`, and the coefficients above agree with every term displayed in `../benjamin/ALPHA_4PIN_SERIES.md`. That agreement is a coefficient check. It does not change the disposition recorded in the alpha note.

The conditional second moment of the remainder is then

```
E[(f_tt(M) + 6 k r)^2 | pins]
  = (μ_M + 6 k r)^2 + Var(ζ_M)
  = (b^2/16 + 1/6) r^4 - (b k / 2) r^5 + O(r^6).
```

Both the mean correction and the centered fluctuation contribute at order `r^4` inside this square. The root-mean-square scale of `f_tt(M) + 6 k r` is order `r^2`.

Reflection `t ↦ r - t` is a kernel isometry. It preserves the six-pin σ-algebra up to deterministic signs on the first `t`-derivatives, and it sends `f_tt(M)` to `f_tt(S)`, so `Var(f_tt(S) | six pins) = Var(ζ_M)`. The same regression at `S` gives the conditional mean

```
μ_S := E[f_tt(S) | six pins]
     = 6 k r - (b/4) r^2 - k r^3 + (b/24) r^4 + (3/10) k r^5
       - (b/192) r^6 - (k/30) r^7 + (b/5760) r^8 + O(r^9),
```

and `f_tt(S) = μ_S + ζ_S` with `ζ_S` centered of that variance. The predecessor display `f_tt(S) = 6 k r + O(r^3)` is withdrawn on the same ground.

Endpoint Hessian at `M`, with the split left explicit:

```
H_M = [[μ_M + ζ_M, r beta], [r beta, S]],
det H_M = (μ_M + ζ_M) S - r^2 beta^2
        = (-6 k r) S + (μ_M + 6 k r) S + ζ_M S - r^2 beta^2.
```

Here `(μ_M + 6 k r)` is the deterministic series `- (b/4) r^2 + k r^3 + O(r^4)`. The products `(μ_M + 6 k r) S` and `ζ_M S` are not given a new `L^p` bound in this note. The predecessor line `det H_M = (-6 k r) S - r^2 beta^2 + O(r^3 |q|)` is withdrawn with the `O(r^3)` expansion it used.

Transport of the Hessian to the witness remains the on-axis Taylor step `H_X = H_M + r q * (third jets) + O(r^2 q^2)`, in the conditional-moment sense of Section 3. Substituting the gradient slaving of Section 4 into the transverse and mixed entries still gives

```
f_ss(X) = S + r q f_sss + O(r^2) = -S + O(r^2) = O_p(r |q|),
f_ts(X) = r beta + r q f_tss + O(r^2) = - r beta + O(r^2) = O_p(r |q|).
```

The axial entry is the unreduced decomposition

```
f_tt(X) = μ_M + ζ_M + r q f_ttt(M) + O_p(r^2 q^2).
```

The predecessor line `f_tt(X) = -6 k r + O(r |q|)` is withdrawn, and with it the predecessor conclusion `det H_X = O(k r^2 |q|)`.

Far-endpoint Hessian `H_S`: the witness sits at physical distance `Theta(r |q|)` from `M` and distance `Theta(r)` from `S`. After the six pins only, `f_tt(S) = μ_S + ζ_S` as above. The marginal scale `f_ss(S) = O_p(1)` on that six-pin law does not determine `det H_S` on `{grad f(X) = 0}`. The predecessor conclusions `det H_S = O(k r)` and

```
det H_M * det H_X * det H_S = O(k^3 r^5 q^2)
```

are withdrawn. No three-determinant product is claimed on the on-axis slice. A `p`-uniform version on the cone was already absent; see Section 6.

## 5. Open obligation: same-law transport, not a one-power obstruction

The reviewed annulus (`|v| >= eta`, `A <= |s| <= B`) does slave `f_zz` at both endpoints:

```
0 = r(u+1/2) f_xz(M) + r v f_zz(M) + O(r^2 M_3),
```

and `|v| >= eta` forces `f_zz(M) = O(r)` on that chart, hence `det H_M = O(r^2)` and likewise `det H_S = O(r^2)`, hence `W_r |det H_X| = O(r^6)` as in the transverse-bound candidate. That is an annulus statement. It is not a cone theorem.

The predecessor treated the cone as the opposite congruence: a witness adjacent to `M` does not see `S`, a marginal `f_ss(S) = O_p(1)` after the six pins was read as `det H_S = O(k r)`, and Math-#58's `O(r^6 q^2)` was declared to be the annulus product copied into cone coordinates, over-counting one power of `r`.

That declaration is withdrawn. An upper scale `f_ss(S) = O_p(1)` on the six-pin law alone does not control `f_ss(S) - f_ss(M)` under the joint law of the six pins together with the witness condition `grad f(X) = 0`. Until that transport is estimated (conditional mean and conditional moments, on that same law), neither of the following is a conclusion of this note:

- that the on-axis product is `O(k^3 r^5 q^2)`;
- that `O(r^6 q^2)` over-counts a power of `r`.

Both remain an open obligation. This note does not supply the missing transport estimate.

Review `5332391136` on the preserved predecessor records a finite 8-pin numerical grid. That grid is diagnostic only. It is not a uniform estimate, it is not reproduced here, and it is not a theorem.

## 6. What this does not close

- Inner square `|p|,|q| <= kappa r`. On `p=0`, if `beta = S = 0` the displayed linear part of `grad f` vanishes for every `q`. Isolation is then carried by third jets that the cone ledger does not estimate. The AMEND-review pathwise majorant `|det H_S| = O(r^2 M_3^2 / |q|)` is not `O(r^5)` uniformly for `|q| < kappa r`. No replacement integral is supplied here.
- Nested microdisk `s = r S` (physical distance `O(r^2)`). Math-#58 remains open. A two-point divided-difference frame that stays nondegenerate as `X -> M` is not constructed in this note.
- Intermediate belt `r << |x| << rho` and shrinking-separation collisions remain open as recorded in `PROOF_INDEX.md`.
- No all-height `O(r^3)` pin-neighborhood expected-count lemma is claimed. The formal product that an earlier draft of this section multiplied into an `O(k r^2)` cone expression was `O(k^3 r^5 q^2)`. Section 5 withdraws that slice product. The expression `O(k r^2)` is not available from this note, including as an on-axis heuristic. A `p`-uniform product estimate, the witness-conditional transport of `f_ss(S)`, remainder control in `L^p` with uniform integrability, index indicators, and the inner-square gap are all missing.

## 7. One-line ledger

| Object | Power | Kind | Status |
|---|---|---|---|
| pin-chart Jacobian at `p=0` | `r^3 q^2` | coordinate | matches PR53 / AMEND-review; equals axial `r^5` at `|q|~r` |
| `f_tt(M)` given six pins | mean `-6kr -(b/4)r^2 + k r^3 + O(r^4)`; centered variance `~ r^4/6` | conditional law | predecessor `O(r^3)` remainder withdrawn |
| `f_tt(S)` given six pins | mean `6kr -(b/4)r^2 - k r^3 + O(r^4)`; same variance | conditional law | predecessor `O(r^3)` remainder withdrawn |
| `det H_M`, `det H_X`, `det H_S` on the cone | — | open | witness-conditional transport of `f_ss(S)` not estimated |
| three-det product on-axis cone | — | withdrawn | predecessor `O(k^3 r^5 q^2)` |
| #58 product `O(r^6 q^2)` | — | open | not shown here to over-count a power of `r` |
| annulus product | `O(r^6)` | congruence | on `|v|>=eta`, not on the pin disk |
| inner square / microdisk | — | missing | AMEND; linear part vanishes; needs third-jet blow-up |

D5 pin-neighborhood remains AMEND. This ledger does not restore `O(r^2 log(1/r))` and does not claim `O(r^3)`.
