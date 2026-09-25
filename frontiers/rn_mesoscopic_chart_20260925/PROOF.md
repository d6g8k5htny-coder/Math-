# RN mesoscopic chart: exact d=2 transverse J0 rows

**Object:** RN-MESOSCOPIC-CHART-J0-D2-TRANSVERSE-20260925-v1  
**Author:** Cursor. **Disposition:** author-side algebraic chart enumeration; complements [Math- PR7](https://github.com/d6g8k5htny-coder/Math-/pull/7) without editing its proof body. **Scientific effect: NONE.**

[Research home](https://github.com/d6g8k5htny-coder/main) · [Fixed-remote parent](../remote_window_20260924/PROOF.md) · [PR7 reduction (branch)](https://github.com/d6g8k5htny-coder/Math-/blob/chatgpt/rn-mesoscopic-annulus-20260925/frontiers/rn_mesoscopic_20260925/PROOF.md) · [§5 crosswalk](CROSSWALK.md)

## 1. Scope of this chart

PR7 isolates the load-bearing missing calculation as the exact contact rows `J_0(y)` and the transform-determinant / witness-Hessian ledger on scaled annuli `x = r y`. This note performs steps (1)–(2) of PR7 §5 for **one declared chart only**:

**Chart `C_transverse` (d=2).** Fixed `1 < A < B < ∞`, witness coordinate `y=(y1,y2)` with

- `A ≤ |y| ≤ B`,
- `|y2| ≥ δ > 0` (here δ=1/4 in the finite checker),
- `dist(y, ±e1/2) ≥ η > 0` (here η=1/10),

so the point stays off the scaled pin sites and off the axial line where the leading `f_y` residual vanishes.

No claim is made for pin-collision charts, axial charts with `y2\to0`, intermediate `r≪|x|≪ρ`, witness collisions, or the full annulus cover.

## 2. Contact Taylor jet after the six pins

Use the same contact limit as the fixed-remote / matrix-cap sources:

    U_0 = (f, f_x, f_xx, f_xxx, f_y, f_xy)_0
        = (b, 0, 0, 12k, 0, 0).

Expand at `x = r y`. The leading raw witness residuals are

    f_y(ry)     = r · f_yy · y2 + O(r^2),
    f_x(ry)     = (r^2/2)·(12k y1^2 + 2 f_xxy y1 y2 + f_xyy y2^2) + O(r^3),
    f(ry) − b   = (r^2/2)· f_yy · y2^2 + O(r^3).

Hence the divided-difference scalings on this chart are

    p_y = 1,    p_x = 2,    p_height = 2.

The **gradient-density Jacobian** power for the raw→`J` map on `(f_x,f_y)` is

    r^(p_x + p_y) = r^3

(so the density picks up `r^(-3)` when changing to contact coordinates). The height mark scales by `r^2` separately inside the between-pin window integral of length `k r^3`. Spatial volume contributes `r^2 dy` in d=2. This package records those powers exactly; it does **not** evaluate the conditioned Hessian factor needed to finish the Kac–Rice integrand.

## 3. Contact rows J0 on C_transverse

Define the contact divided differences by stripping the displayed leading powers of `r`:

    J_grad_y = f_yy · y2,
    J_grad_x = 6k y1^2 + f_xxy y1 y2 + (1/2) f_xyy y2^2,
    J_height = (1/2) f_yy · y2^2.

With `|y2|≥δ>0`, `J_grad_y` isolates `f_yy`. The leading height row satisfies

    J_height = (y2 / 2) · J_grad_y

so height is **dependent at leading order**. Restoring the next Taylor term gives

    (f(ry)−b)/r^2 = J_height + r · H_height_next + O(r^2),

    H_height_next = 2k y1^3 + (1/2) f_xxy y1^2 y2 + (1/2) f_xyy y1 y2^2 + (1/6) f_yyy y2^3.

Thus the height mark becomes an independent contact observation only after keeping the explicit factor of `r` (or passing to a further divided difference). The finite checker records `H_height_next` exactly; it does not eliminate that `r` from the Kac–Rice density.

The two gradient rows are the independent contact observations for the gradient factor on this chart at leading order.

## 4. What is proved here vs open

**Recorded / checked (exact arithmetic):**

- chart membership predicates for `C_transverse`;
- contact-row polynomials above, including `H_height_next`;
- leading-order height–`J_grad_y` dependence identity;
- scaling exponents and gradient Jacobian `r`-power `3`;
- Hessian contact rows and raw `det H` leading `r`-power `1` on `C_transverse` and `C_axial`;
- thin-belt contact polynomials (same jet forms; not absorbed; no uniform bound);
- contact integrand `r`-power identity (net `3` transverse / `2` axial);
- finite mutation controls on those algebraic statements.

**Still open (explicitly):**

- absorbing the explicit `r` in the transverse height density into a uniform integrand bound;
- uniform bound on the contact Gaussian density factor (the missing step for `γ_AB ≤ C r^(-d)`);
- uniform thin-belt integrand bound controlling the `1/|y2|` singularity;
- conditioned Gaussian expectation of the typed Hessian factor on either chart;
- pin-site divided-difference contact rows on any scale where pins enter the annulus;
- any numerical RN / 24-jet certificate.

## 4.5 Axial chart C_axial

On `y2=0` with `|y1|` in the annulus and away from `±1/2`, the leading transverse `f_y` and height powers drop:

    f_y(r y1, 0) = (r^2 y1^2 / 2) f_xxy + O(r^3),
    f_x(r y1, 0) = (r^2/2)(12k y1^2) + O(r^3),
    f(r y1, 0)−b = 2k r^3 y1^3 + O(r^3 · other 3-jets).

Hence axial scalings are `p_x=2`, `p_y=2`, `p_height=3`, and the gradient Jacobian power is `r^4`. Contact rows:

    J_grad_y = (y1^2 / 2) f_xxy,
    J_grad_x = 6k y1^2,
    J_height = 2k y1^3.

Height is already independent at this axial leading order (cubic mark).

## 4.6 Cover inventory, thin belt, and near-pin diagnosis

For the PR7 convention `A > 1`, both scaled pins satisfy `|pin| = 1/2 < A`, so they lie **exterior** to the annulus. The finite partition of annulus points (off the open thin belt) is therefore:

- `C_transverse`: `|y2| ≥ δ`,
- `C_axial`: `y2 = 0`,
- `thin_belt_open`: `0 < |y2| < δ` (still away from pins),

with `near_pin` empty on this fixed annulus. The machine cover report records `enumerated_charts = {C_transverse, C_axial}`, `open_regions = {thin_belt_open}`, and `cover_complete = false`.

The thin belt is not absorbed into `C_transverse`: although the contact polynomials extend (and are enumerated on `C_thin_belt`), `J_grad_y = f_yy · y2` has coefficient `y2 → 0`, so Schur / change-of-variables conditioning deteriorates as `1/|y2|`. Dyadic shells show the bare factor is not locally `L^1` at `y2=0` (each shell contributes at least `1` to `∫ dy2/|y2|`). Pointwise, the jet map factor `∂J_grad_y/∂f_yy = y2` cancels that reciprocal (`|y2|·(1/|y2|)=1`), but this is **not** a conditioned-density bound. Across the interface `|y2|=δ` the transverse and thin-belt charts share identical contact polynomials, so the transition Jacobian on those rows is `1` (nonsingular). The checker still marks `uniform_integrand_bound_proved = false`.

A separate **small-A** regime (`0 < A ≤ 1/2`, `require_pr7_A=False`) is used only to diagnose pin-neighbourhood points when pins can enter the annulus. The checker records the pin-local frame `z = y − pin` and that midpoint `U_0` rows do not apply; it does **not** enumerate pin-site divided-difference contact rows (`pin_site_jet_rows_enumerated = false`), and it does not alter the PR7 fixed-annulus statements.

## 4.7 Hessian contact rows on C_transverse

After the same `U_0` constraints, the witness Hessian at `x = r y` has mixed leading powers:

    f_xx(ry) = r (12k y1 + f_xxy y2) + O(r^2),
    f_xy(ry) = r (f_xxy y1 + f_xyy y2) + O(r^2),
    f_yy(ry) = f_yy + O(r).

Contact entries after stripping those powers:

    H_xx_contact = 12k y1 + f_xxy y2,
    H_xy_contact = f_xxy y1 + f_xyy y2,
    H_yy_contact = f_yy.

Hence

    det H = r · H_xx_contact · H_yy_contact − r^2 · H_xy_contact^2 + O(r^2),

so the raw determinant contributes a leading factor `r^1`. The same leading powers hold on `C_axial` after dropping `y2` terms (`H_xx_contact = 12k y1`, `H_xy_contact = f_xxy y1`). The finite checker records these polynomials and the power; it does **not** evaluate the conditioned Gaussian expectation of the typed Hessian factor needed to finish the Kac–Rice integrand (`hessian_ledger_evaluated = false`).

## 4.8 Contact integrand r-power identity

On a declared chart the mesoscopic expected-count integrand contributes the exact powers

    r^(spatial) · r^(-grad_jac) · r^(hess_det) · r^(height_window)

with `spatial=2`, `height_window=3`, `hess_det=1`, and `grad_jac = 3` on `C_transverse` (resp. `4` on `C_axial`). The resulting net powers are

    C_transverse: 2 − 3 + 1 + 3 = 3,
    C_axial:      2 − 4 + 1 + 3 = 2

(the axial chart is area-measure zero inside the 2D annulus integral). This is a **power identity only**: it does not bound the contact Gaussian density factor, so it does not yet prove the PR7 target `γ_AB ≤ C r^(-d)`.

## 5. Relation to PR7 and #86

This is the Codex-offered D5 slice from [main #86](https://github.com/d6g8k5htny-coder/main/issues/86): declared scaled-annulus charts, separate branch/artifact, no edit to PR7's proof body. Downstream-first still applies: this does not promote a CONTROLLING RN closure while D0–D4 reviews remain open.
