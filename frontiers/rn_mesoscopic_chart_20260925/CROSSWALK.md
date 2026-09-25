# PR7 §5 → this package (exact identities)

**Object:** RN-MESOSCOPIC-CHART-PR7-CROSSWALK-20260925-v1  
**PR7 claim:** `RN-MESOSCOPIC-ANNULUS-REDUCTION-20260925-v1` (Math- PR7, paused)  
**This package tip:** see `SOURCE_FILES.json` / Math- PR9  
**Scientific effect: NONE.** Does not edit PR7's proof body or promote CONTROLLING status.

PR7 §5 lists five load-bearing calculations. This table records which are enumerated here versus still open.

| PR7 §5 step | Status in this package | Exact carrier |
|---|---|---|
| (1) Independent contact rows `J_0(y)` after pin constraints | **Partial** — enumerated on `C_transverse`, `C_axial`, and `C_thin_belt` (shared jet helper); pin-site **leading Morse + cubic through octic** rows + max/saddle Hessian signature; ninth-and-higher pin jets open | `mesoscopic_chart.py` contact / thin-belt / axial / `pin_site_morse_contact_rows` / `pin_site_morse_next_order_rows` / `pin_site_morse_quartic_rows` / `pin_site_morse_quintic_rows` / `pin_site_morse_sextic_rows` / `pin_site_morse_septic_rows` / `pin_site_morse_octic_rows` / `pin_morse_hessian_signature` |
| (2) Exact `r`-power of `det S_r(y)` on each rank chart | **Partial** — gradient Jacobian powers `3` (transverse/thin), `4` (axial), `2` (pin Morse); Hessian raw `det H` leading power `1` (midpoint charts) / `0` (pin); pin-centered net `r^3` | `SCALING_EXPONENTS`, `AXIAL_SCALING_EXPONENTS`, `PIN_CENTERED_*`, `HESSIAN_SCALING_EXPONENTS`, `contact_integrand_power_ledger`, `pin_centered_integrand_power_ledger` |
| (3) Conditioned witness Hessian in the same chart | **Partial** — contact Hessian polynomials recorded; free-jet residual inventory after gradient contact recorded; residual Hessian polynomials after eliminating constrained jets recorded; free-jet linear `|det H|` skeleton recorded; conditioned Gaussian expectation **open** | `hessian_contact_rows` / `axial_hessian_contact_rows` / `contact_free_jet_residual_inventory` / `transverse_conditioned_hessian_residual_ledger` / `axial_conditioned_hessian_residual_ledger` / `contact_conditioned_det_free_jet_skeleton_inventory`; `hessian_ledger_evaluated=false` |
| (4) Combine typed Hessian with gradient-density Jacobian | **Partial** — exact power identity only; unmatched transverse height `r^1` recorded; axial height independent at leading order (no unmatched height r); height residual after grad contact enumerated; free-jet / Hessian residuals and gradient-contact |det| shape enumerated; algebraic factor product `(1/|det J|)·|det H|` recorded; density factor unbound | net `r^3` transverse / pin / `r^2` axial; `transverse_height_r_factor_ledger`; `axial_height_independence_ledger`; `transverse_height_residual_after_grad_contact`; `contact_free_jet_residual_inventory`; `contact_gradient_jacobian_density_shape_inventory`; `contact_integrand_algebraic_factor_skeleton_inventory`; `contact_density_obstruction_inventory`; `contact_density_bound_proved=false` |
| (5) Local integrability across chart boundaries; uniform bound on `A≤\|y\|≤B` | **Partial** — `|y2|=δ` transition is identity (det 1); `C_transverse` bare `1/\|y2\|≤1/δ` and `C_axial` bare `2/y1^2≤2/A^2` cleared; thin-belt bare reciprocal L1 cleared by jet-map cancel (residual geometric factor = 1, locally L1); thin-belt algebraic factor product recorded (reciprocal diverges as `y2→0`); contact Gaussian density near `y2→0` still open | `chart_boundary_transition`, `transverse_conditioning_uniform_bound`, `axial_conditioning_uniform_bound`, `thin_belt_reciprocal_shell_lower_bound`, `jet_map_f_yy_to_J_grad_y_factor`, `thin_belt_integrand_residual_after_cancel`, `thin_belt_contact_integrand_algebraic_factor_skeleton` |

## Chart cover (PR7 annulus `A>1`)

| Region | Contact rows | Uniform bound |
|---|---|---|
| `C_transverse` | yes | chart conditioning cleared (`1/\|y2\|≤1/δ`); Gaussian density open |
| `C_axial` | yes | chart conditioning cleared (`2/y1^2≤2/A^2`); area-measure zero; Gaussian density open |
| `thin_belt_open` | yes (same jets) | bare `1/\|y2\|` L1 cleared by jet-map cancel; Gaussian density near `y2→0` open |
| `near_pin` | no (pins exterior for `A>1/2`) | n/a on PR7 annulus |

Small-A (`A≤1/2`) is a separate diagnostic regime: pin-local frame, leading Morse + cubic through octic rows, max/saddle Hessian signature test, and obstruction ledger recorded; ninth-and-higher pin jets and density open.

## Hard-gate mapping

Node `math.rn-mesoscopic-chart-j0` on the Math- hard-gate graph ([PR #14](https://github.com/d6g8k5htny-coder/Math-/pull/14), superseding closed PR12) points at this author-side candidate. Classification remains `AUTHOR_SIDE_CANDIDATE`; promotion stays refused.
