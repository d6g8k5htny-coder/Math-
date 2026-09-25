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
- uniform bare-conditioning bound `1/|y2| ≤ 1/δ` on `C_transverse` (chart singularity cleared; Gaussian density still open);
- uniform bare-conditioning bound `2/y1^2 ≤ 2/A^2` on `C_axial` (chart singularity cleared; area-measure zero; Gaussian density still open);
- unmatched transverse height density `r^1` from `H_height_next` (explicitly not absorbed);
- thin-belt unmatched height density `r^1` (same jet dependence as transverse; density near y2→0 still open);
- pin-centered unmatched height density `r^1` after Morse leading order (cubic `H_height_next`; density / higher jets still open);
- axial height independence at leading order (`J_height=2k y1^3`; unmatched height `r`-power `0`; area-measure zero);
- exact axial shared-gap-mark identity `J_height=(y1/3)J_grad_x` (distinct scalings `p_x=2`,`p_height=3` keep unmatched height `r` at 0);
- pin-site leading Morse contact rows `J_grad = H_pin z`, `J_height = (1/2) z·H·z` with max/saddle Hessian signature test;
- pin-site cubic next-order rows `H_grad_next = (1/2)D³f(z,z)`, `H_height_next = (1/6)D³f(z,z,z)` with `z·H_grad_next = 3 H_height_next`;
- pin-site quartic residuals `Q_grad_next = (1/6)D⁴f(z,z,z)`, `Q_height_next = (1/24)D⁴f(z,z,z,z)` with `z·Q_grad_next = 4 Q_height_next`;
- pin-site quintic residuals `P_grad_next = (1/24)D⁵f(z,z,z,z)`, `P_height_next = (1/120)D⁵f(z,z,z,z,z)` with `z·P_grad_next = 5 P_height_next`;
- pin-site sextic residuals `S_grad_next = (1/120)D⁶f(z,z,z,z,z)`, `S_height_next = (1/720)D⁶f(z,z,z,z,z,z)` with `z·S_grad_next = 6 S_height_next`;
- pin-site septic residuals `T_grad_next = (1/720)D⁷f(z,z,z,z,z,z)`, `T_height_next = (1/5040)D⁷f(z,z,z,z,z,z,z)` with `z·T_grad_next = 7 T_height_next`;
- pin-site octic residuals `U_grad_next = (1/5040)D⁸f(z,z,z,z,z,z,z)`, `U_height_next = (1/40320)D⁸f(z,z,z,z,z,z,z,z)` with `z·U_grad_next = 8 U_height_next`;
- pin-site nonic residuals `N_grad_next = (1/40320)D⁹f(z,z,z,z,z,z,z,z)`, `N_height_next = (1/362880)D⁹f(z,z,z,z,z,z,z,z,z)` with `z·N_grad_next = 9 N_height_next`;
- pin-site decic residuals `D_grad_next = (1/362880)D¹⁰f(z^9)`, `D_height_next = (1/3628800)D¹⁰f(z^10)` with `z·D_grad_next = 10 D_height_next`;
- pin-site undecic residuals `E_grad_next = (1/3628800)D¹¹f(z^10)`, `E_height_next = (1/39916800)D¹¹f(z^11)` with `z·E_grad_next = 11 E_height_next`;
- pin-site dodecic residuals `F_grad_next = (1/39916800)D¹²f(z^11)`, `F_height_next = (1/479001600)D¹²f(z^12)` with `z·F_grad_next = 12 F_height_next`;
- pin-site tridecic residuals `G_grad_next = (1/479001600)D¹³f(z^12)`, `G_height_next = (1/6227020800)D¹³f(z^13)` with `z·G_grad_next = 13 G_height_next`;
- pin-site tetradecic residuals `I_grad_next = (1/6227020800)D¹⁴f(z^13)`, `I_height_next = (1/87178291200)D¹⁴f(z^14)` with `z·I_grad_next = 14 I_height_next`;
- pin-site pentadecic residuals `J_grad_next = (1/87178291200)D¹⁵f(z^14)`, `J_height_next = (1/1307674368000)D¹⁵f(z^15)` with `z·J_grad_next = 15 J_height_next`;
- pin-site hexadecic residuals `K_grad_next = (1/1307674368000)D¹⁶f(z^15)`, `K_height_next = (1/20922789888000)D¹⁶f(z^16)` with `z·K_grad_next = 16 K_height_next`;
- pin-site heptadecic residuals `L_grad_next = (1/20922789888000)D¹⁷f(z^16)`, `L_height_next = (1/355687428096000)D¹⁷f(z^17)` with `z·L_grad_next = 17 L_height_next`;
- pin-site octadecic residuals `M_grad_next = (1/355687428096000)D¹⁸f(z^17)`, `M_height_next = (1/6402373705728000)D¹⁸f(z^18)` with `z·M_grad_next = 18 M_height_next`;
- pin-site nonadecic residuals `O_grad_next = (1/6402373705728000)D¹⁹f(z^18)`, `O_height_next = (1/121645100408832000)D¹⁹f(z^19)` with `z·O_grad_next = 19 O_height_next`;
- pin-site icosic residuals `R_grad_next = (1/121645100408832000)D²⁰f(z^19)`, `R_height_next = (1/2432902008176640000)D²⁰f(z^20)` with `z·R_grad_next = 20 R_height_next`;
- pin-site henicosic residuals `V_grad_next = (1/2432902008176640000)D²¹f(z^20)`, `V_height_next = (1/51090942171709440000)D²¹f(z^21)` with `z·V_grad_next = 21 V_height_next`;
- pin-site docosic residuals `W_grad_next = (1/51090942171709440000)D²²f(z^21)`, `W_height_next = (1/1124000727777607680000)D²²f(z^22)` with `z·W_grad_next = 22 W_height_next`;
- pin-site tricosic residuals `X_grad_next = (1/1124000727777607680000)D²³f(z^22)`, `X_height_next = (1/25852016738884976640000)D²³f(z^23)` with `z·X_grad_next = 23 X_height_next`;
- pin-site tetracosic residuals `Y_grad_next = (1/25852016738884976640000)D²⁴f(z^23)`, `Y_height_next = (1/620448401733239439360000)D²⁴f(z^24)` with `z·Y_grad_next = 24 Y_height_next`;
- pin-site pentacosic residuals `Z_grad_next = (1/620448401733239439360000)D²⁵f(z^24)`, `Z_height_next = (1/15511210043330985984000000)D²⁵f(z^25)` with `z·Z_grad_next = 25 Z_height_next`;
- pin-site hexacosic residuals `A_grad_next = (1/15511210043330985984000000)D²⁶f(z^25)`, `A_height_next = (1/403291461126605635584000000)D²⁶f(z^26)` with `z·A_grad_next = 26 A_height_next`;
- pin-site heptacosic residuals `B_grad_next = (1/403291461126605635584000000)D²⁷f(z^26)`, `B_height_next = (1/10888869450418352160768000000)D²⁷f(z^27)` with `z·B_grad_next = 27 B_height_next`;
- pin-site octacosic residuals `C_grad_next = (1/10888869450418352160768000000)D²⁸f(z^27)`, `C_height_next = (1/304888344611713860501504000000)D²⁸f(z^28)` with `z·C_grad_next = 28 C_height_next` (twenty-ninth-and-higher jets open);
- pin-centered integrand power identity (net `r^3`: spatial 2 − grad 2 + hess 0 + height 3);
- per-chart contact-density obstruction inventory (`global_contact_density_bound_proved=false`);
- free-jet residual inventory after leading gradient contact (transverse/thin rank-2 ⇒ 2 free dirs; axial isolates `f_xxy`,`k`; pin Morse rank-2 ⇒ 1 free Hessian dir; density still open);
- exact gradient-contact Jacobians `|det|=|y2|^3/2` (transverse/thin), `3|y1|^4` (axial), and pin Morse `|det|=z2²` (or `z1²` on axis); thin reciprocal diverges as y2→0; algebraic density shape only;
- conditioned Hessian residual polynomials after eliminating constrained jets (transverse/thin free `(k,f_xxy)`; axial free `f_yy`; pin Morse free `H_xx` or `H_yy`; thin reciprocal diverges as y2→0; expectation still open);
- transverse/axial/thin/pin conditioned `|det H|` free-jet linear skeletons (`det=α_k·k+α_f·f_xxy` / `det=α_fyy·f_yy` / `det=α·free+β`; thin reciprocal diverges as y2→0; expectation still open);
- contact integrand algebraic factor product `(1/|det J_grad|)·|det H_skeleton|` on transverse/axial/thin-belt/pin-centered (Gaussian density still open; thin-belt reciprocal diverges as y2→0; pin Morse `|det|=z2²` or `z1²`);
- transverse algebraic-factor × unmatched height `r^1` combined skeleton (product identity recorded; neither factor absorbed; density still open);
- thin-belt algebraic-factor × unmatched height `r^1` combined skeleton (reciprocal diverges as y2→0; neither factor absorbed; density still open);
- pin-centered algebraic-factor × unmatched height `r^1` combined skeleton (neither factor absorbed; density / higher jets still open);
- inventory bundling those combined skeletons (`C_axial` exempt: no unmatched height r); density still open;
- pin-site unmatched height-r power inventory for cubic through octacosic (`r^1`…`r^26`; none absorbed; twenty-ninth+ open);
- transverse height residual `H_height_next` after the same eliminations (unmatched `r^1` still open);
- thin-belt height residual `H_height_next` after the same eliminations (reciprocal diverges as y2→0; unmatched `r^1` still open);
- thin-belt integrand residual after jet-map cancel (bare reciprocal L1 cleared; residual geometric factor = 1; density near y2=0 open);
- pin-site jet obstruction ledger (midpoint collision; Morse rows elsewhere);
- finite mutation controls on those algebraic statements.

**Still open (explicitly):**

- absorbing the explicit `r` in the transverse / thin-belt height density into a uniform integrand bound;
- uniform bound on the contact Gaussian density factor (the missing step for `γ_AB ≤ C r^(-d)`);
- uniform thin-belt contact Gaussian density bound near `y2→0` (bare `1/|y2|` L1 cleared by jet-map cancel; residual geometric factor = 1);
- conditioned Gaussian expectation of the typed Hessian factor on either chart;
- higher-order pin-site divided-difference jets beyond octacosic residuals;
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

Height is already independent at this axial leading order (cubic mark). Exact shared-gap-mark identity: `J_height = (y1/3) J_grad_x`; distinct scalings keep unmatched height `r` at 0.

## 4.6 Cover inventory, thin belt, and near-pin diagnosis

For the PR7 convention `A > 1`, both scaled pins satisfy `|pin| = 1/2 < A`, so they lie **exterior** to the annulus. The finite partition of annulus points (off the open thin belt) is therefore:

- `C_transverse`: `|y2| ≥ δ`,
- `C_axial`: `y2 = 0`,
- `thin_belt_open`: `0 < |y2| < δ` (still away from pins),

with `near_pin` empty on this fixed annulus. The machine cover report records `enumerated_charts = {C_transverse, C_axial}`, `open_regions = {thin_belt_open}`, and `cover_complete = false`.

The thin belt is not absorbed into `C_transverse`: although the contact polynomials extend (and are enumerated on `C_thin_belt`), `J_grad_y = f_yy · y2` has coefficient `y2 → 0`, so Schur / change-of-variables conditioning deteriorates as `1/|y2|`. Dyadic shells show the bare factor is not locally `L^1` at `y2=0` (each shell contributes at least `1` to `∫ dy2/|y2|`). Pointwise, the jet map factor `∂J_grad_y/∂f_yy = y2` cancels that reciprocal (`|y2|·(1/|y2|)=1`), but this is **not** a conditioned-density bound. On `C_transverse` itself (`|y2|≥δ`) the bare reciprocal is uniformly bounded by `1/δ`, so the chart-conditioning singularity is cleared there; the remaining transverse obstruction is the contact Gaussian density / Hessian expectation, not `1/|y2|`. Across the interface `|y2|=δ` the transverse and thin-belt charts share identical contact polynomials, so the transition Jacobian on those rows is `1` (nonsingular). The checker still marks `uniform_integrand_bound_proved = false` and `gaussian_density_factor_bounded = false`.

A separate **small-A** regime (`0 < A ≤ 1/2`, `require_pr7_A=False`) is used only to diagnose pin-neighbourhood points when pins can enter the annulus. The checker records the pin-local frame `z = y − pin`, that midpoint `U_0` rows do not apply, and the leading Morse contact residuals after pin constraints:

    J_grad = H_pin · z,    J_height = (1/2) z · H_pin · z,

with scalings `p_grad=1`, `p_height=2` (gradient Jacobian `r`-power `2`), plus an exact Sylvester signature test (`M` ⇒ negative definite, `S` ⇒ indefinite), plus cubic through hexadecic residuals (unmatched `r^1`…`r^14`). Seventeenth-and-higher pin-site jets and the contact density remain open (`pin_site_higher_jets_enumerated = false`). This does not alter the PR7 fixed-annulus statements.

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
