# PR7 §5 → this package (exact identities)

**Object:** RN-MESOSCOPIC-CHART-PR7-CROSSWALK-20260925-v1  
**PR7 claim:** `RN-MESOSCOPIC-ANNULUS-REDUCTION-20260925-v1` (Math- PR7, paused)  
**This package tip:** see `SOURCE_FILES.json` / Math- PR9  
**Scientific effect: NONE.** Does not edit PR7's proof body or promote CONTROLLING status.

PR7 §5 lists five load-bearing calculations. This table records which are enumerated here versus still open.

| PR7 §5 step | Status in this package | Exact carrier |
|---|---|---|
| (1) Independent contact rows `J_0(y)` after pin constraints | **Partial** — enumerated on `C_transverse`, `C_axial`, and `C_thin_belt` (shared jet helper); pin-site jets **not** enumerated | `mesoscopic_chart.py` contact / thin-belt / axial rows; `C_pin_centered` frame only |
| (2) Exact `r`-power of `det S_r(y)` on each rank chart | **Partial** — gradient Jacobian powers `3` (transverse/thin) and `4` (axial); Hessian raw `det H` leading power `1` | `SCALING_EXPONENTS`, `AXIAL_SCALING_EXPONENTS`, `HESSIAN_SCALING_EXPONENTS`, `contact_integrand_power_ledger` |
| (3) Conditioned witness Hessian in the same chart | **Partial** — contact Hessian polynomials recorded; conditioned Gaussian expectation **open** | `hessian_contact_rows` / `axial_hessian_contact_rows`; `hessian_ledger_evaluated=false` |
| (4) Combine typed Hessian with gradient-density Jacobian | **Partial** — exact power identity only (`spatial - grad_jac + hess_det + height_window`); density factor unbound | net `r^3` transverse / `r^2` axial; `contact_density_bound_proved=false` |
| (5) Local integrability across chart boundaries; uniform bound on `A≤\|y\|≤B` | **Open** — cover inventory + thin-belt `1/\|y2\|` conditioning + pin-frame diagnosis; no uniform bound | `chart_cover_report`, `thin_belt_ledger_for_point`, `pin_centered_ledger_for_point` |

## Chart cover (PR7 annulus `A>1`)

| Region | Contact rows | Uniform bound |
|---|---|---|
| `C_transverse` | yes | open (density) |
| `C_axial` | yes | open (and area-measure zero in 2D) |
| `thin_belt_open` | yes (same jets) | open (`1/\|y2\|` not bare-L1; cancellation required) |
| `near_pin` | no (pins exterior for `A>1/2`) | n/a on PR7 annulus |

Small-A (`A≤1/2`) is a separate diagnostic regime only: pin-local frame recorded, pin-site jets refused as not yet enumerated.

## Hard-gate mapping

Node `math.rn-mesoscopic-chart-j0` on the Math- hard-gate graph (PR12) points at this author-side candidate. Classification remains `AUTHOR_SIDE_CANDIDATE`; promotion stays refused.
