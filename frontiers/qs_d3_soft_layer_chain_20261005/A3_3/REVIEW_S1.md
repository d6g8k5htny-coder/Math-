## A3.3 S1 — PASS_SCOPED: Lemma P, with a direct C4 error reconstruction

**No required analytic amendment to Lemma P (P.1).** This delivers pickup5999545712. It is not acceptance of W3/TE, the whole A3.3 chain, its Gaussian transfer, or any scientific-status change.

Dylan Roy — delegated AI review. Actual performer OpenAI / GPT-6 Astra Pro, session `github-round2-20261005T1711Z`. I did not author A3.3. No helpers or local agents used. Public task/source summaries were visible; this is not a blind audit. Organizational-independence credit0.

### Sources and actual scope

- Original note5998500022, `CL-QS-A3-3-WEIGHT-TRANSFER-20261004-v1`, §2 including its C4 paragraph. Author's served-body identity:20654B, SHA256 `54f123821b36ee99b17f9ae1b2cc159920b8dde48b1a553b812d70c114d96f1b`. This is the declared whole-comment digest, not a newly recomputed full-body hash by me. I read the complete §2 statement/proof and necessary notation.
- Controls5998502385: read `MULTI`, `pinned_field`, `rand_free`, factorial/Laurent helpers, `window_hessian_lp`, and the entire `k4`. No full `a33_exact.py` replay is claimed; S3 owns that.
- Parent reads fixed at Math- commit `ab3a4b5b904f26d85467dbb8e828dc558280cee8`: #243 `frontiers/soft_fold_limit_20261002/PROOF.md`, blob `6502cf7ba2edee47761e40308c15b7563b06d1f8`, §0 and FL.1; #242 `frontiers/soft_rejected_pairs_20261002/PROOF.md`, blob `271412dbc96a29590f5f805258e15c9e335cb430`, (2.1) and Proposition2′ (2.6). Their identities match the note's pins. I do not adopt the parents' global elder/limit conclusions in this slice.

### S1.1 — the affine chart and six entries

Fix one midpoint eigenframe; it is constant as the chart variables move. With `r>0`, `k>0`,

`A = diag(r,rk,r^(3/2))`, `Hess(F) = (kr^3)^(-1) A^T Hess(f) A`.

The six multipliers of the physical Hessian entries `(xx,xy1,y1y1,xy2,y1y2,y2y2)` are exactly

`(1/(kr), 1/r, k/r, 1/(k sqrt(r)), 1/sqrt(r), 1/k)`.

Thus the claimed soft blocks and the two mixed coefficients have the correct k-factors, signs and powers. The pin sign is `sigma=-1` at M and `sigma=+1` at S:

`P_sigma = [[6sigma, sigma gamma/2], [sigma gamma/2, -lambda_tilde + sigma kB/2]]`,

`q_sigma = (sigma gamma2/(2k), sigma beta2/2)`.

Direct differentiation of #242 (2.1) gives those P blocks; differentiating (2.6)'s `eta*a(X,zeta)` at a pin gives exactly the off-diagonal block `sqrt(r)*q_sigma`, and zero planar/stiff blocks. The `zeta^2` term in a has zero gradient there. The two determinants are `6lambda_tilde+Y` and `-6lambda_tilde+Y`, with `Y=3kB-gamma^2/4`.

A repeated or zero transverse eigenvalue does not obstruct this calculation: choose any orthonormal diagonalizing frame and keep it fixed. No derivative of an eigenvector, no inverse eigenvalue and no eigenvalue-gap bound is used. Torus-chart injectivity is not needed for this local Hessian identity; the periodic lift supplies the axial segment.

### S1.2 — direct C4 proof, without assuming the stronger C5 expansion

Here is an explicit reconstruction of the note's final C4 paragraph. Let N* bound the absolute values of all third/fourth coordinate derivatives in this fixed orthonormal frame on the lifted axial segment `[-r/2,r/2]`. The usual C4 norm controls N* up to a fixed dimension/norm-convention factor. The following constants are for this explicitly defined derivative bound.

**Axial entry.** Write the segment as t in `[0,r]`. Its cubic Hermite interpolant from the exact height and derivative pins is

`q(t)=b-3kr*t^2+2k*t^3`.

It has `q''(0)=-6kr`, `q''(r)=6kr`. Two integrations of Taylor's integral remainder give

`h''(0)-q''(0) = integral_0^r [t(r-t)^2/r^2] h''''(t) dt`.

The reflected formula holds at r. Both nonnegative kernels integrate to `r^2/12`. Therefore

`|f_xx(sigma r/2)-6sigma kr| <= N* r^2/12`.

This uses the actual endpoint pins, not a contact-law substitution.

**Axial/transverse entries.** Put `g_i(x)=f_yi(x,0,0)` and `a=r/2`. The transverse gradient pins give `g_i(±a)=0`. Symmetric Taylor expansion through degree2, using `|g_i'''|<=N*`, yields

`|g_i'(0)| <= N* a^2/6`.

Taylor expansion of g_i' to first order then gives

`|g_i'(sigma a)-sigma a*g_i''(0)| <= (1/6+1/2)N*a^2 = N*r^2/6`.

Here `g_1''(0)=gamma`, `g_2''(0)=gamma2`.

**Transverse entries.** The exact midpoint frame gives `f_y1y1(0)=-r lambda_tilde/k`, `f_y1y2(0)=0`, `f_y2y2(0)=-lambda2`. Taylor to first order gives remainder at most `N*r^2/8` for the first two. For the last, the fundamental theorem of calculus gives `|f_y2y2(sigma r/2)+lambda2|<=N*r/2`.

### S1.3 — explicit anisotropic errors

Subtract the displayed P block, stiff entry and mixed `sqrt(r)` block. In the chart coordinates `(X,zeta,eta)`, the symmetric remainder E satisfies:

| Entry | Bound |
|---|---|
| XX | `N*r/(12k)` |
| X,zeta | `N*r/6` |
| zeta,zeta | `kN*r/8` |
| X,eta | `N*r^(3/2)/(6k)` |
| zeta,eta | `N*r^(3/2)/8` |
| eta,eta | `N*r/(2k)` |

Here N denotes N* from the preceding definition, not a newly assigned Gaussian norm. For `r<=1` the row-sum bound gives

`||E||_op <= N*r * max(1/(4k_-)+1/6, k_+/8+7/24, 2/(3k_-)+1/8)`.

After the fixed norm-equivalence factor, this proves exactly (P.1) with the note's C4 norm, hence also with its C5 norm. It even retains the sharper `r^(3/2)` mixed remainder. The constants require `k_->0` and bounded k_+; nothing is claimed uniformly as k tends to0. They do not divide by gamma, lambda_tilde or lambda2, so zero/sign-changing hard curvature is harmless **for this Hessian estimate**. No claim about sign stability of a nearly singular Hessian follows merely from the estimate.

### S1.4 — finite controls and their limits

K4's factorial coefficient convention and composed exponents `2i+2j+3l-6` are consistent with the affine chart. Its exact quartic pin corrections agree with solving the eight pin equations. The coefficient of s^0 is the model; the coefficient of s^1 is the mixed block; planar/stiff entries are even in `s=sqrt(r)`, and mixed entries are odd. Its M3 doubles Da and should be caught at the mixed entry. This is a source inspection of K4, not its execution.

I also ran a **separate** symbolic/quintic diagnostic (SymPy1.14.0), solving the eight pin equations with linear algebra rather than copying the author's solved coefficients. It includes every quintic monomial that can affect a pin Hessian, plus an invisible transverse cubic. Results:

- **12/12 methods PASS normally and12/12 under -O**.
- **192 exact entry-bound inequalities** over16 rational parameter choices and both pins pass; norm bounds are derived on the axial segment, not presented as global polynomial C4 norms on a torus.
- Four mutations each fail by the intended assertion in both modes: omitted mixed block, missing soft-coordinate k, exchanged pin signs, and missing determinant k.
- All five normal/optimized stdout pairs agree byte for byte. An initial batched tool call hit its execution limit before the tenth result; the final optimized determinant mutation was run separately. All ten final outcomes are recorded; no timeout is labeled a mathematical rejection.

Scratch script SHA256 `4b238cbea3bac37e8bb834dc7f0484093008120418d52a360bffa3574e9477a1`; execution inventory SHA256 `3f1d20d39a901ea947a4750a51359d3d1bffad6328205139be2e83eeeb4d1cdf`. These are local scratch artifacts, not claimed GitHub paths or Lean certificates. The proof above, not these finite controls, establishes the C4 estimate.

**Ordering note:** K4's random diagonal values, and some of my broader algebraic probes, do not enforce `lambda1<=lambda2`. P.1 itself was proved without ordering, so those are legitimate algebraic-frame controls, not samples of every ordered spectral branch. I saw S2 finding5999623189 only after my S1 reconstruction/checks; that distinct K5 witness-domain AMEND remains with S2 and the author. This S1 PASS neither resolves it nor enlarges the parent proposition's stiff-positive elder conclusions to signed curvature.

### Delivery boundary and release

**S1 PASS at the original note's §2; no required P.1 amendment.** The explicit constants above are reviewer derivation/support and may be cited as such; no silent author-source rewrite occurred. W3/TE, its control-scope amendment, Gaussian conditioning/uniform moments, normalization and scientific closure remain outside this verdict. S2 and S3 retain their own owners. Release my S1 claim5999545712 now; no writer/merge reservation or scientific flag change.