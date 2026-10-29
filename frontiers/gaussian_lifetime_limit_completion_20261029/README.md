# Completing the lifetime moment limits

[Uniform inverse moments](INVERSE_MOMENTS.md) · [Large-ratio action bridge](LARGE_RATIO.md) ·
[Exact sources](SOURCES.json) · [Verification](VERIFICATION.md)

This additive candidate closes the missing uniform-integrability step for
inverse moments of the actual finite-death failure law. It also connects
the critical-window essential event to the sharp Gaussian action.

| Result | Scope |
| --- | --- |
| `P_r(F_r,0<X_r<=t) <= C r^3 t^(2/3)`, `0<t<=1` | Original periodized Gaussian; fixed dimension/torus, compact birth/gap ranges with gaps bounded away from zero, every frame, uniformly for small separation. |
| `r^-3 E[X_r^-p;F_r,finite] -> integral lambda^-p dmu_fail` for `0<p<2/3` | Each fixed parameter choice, using the existing actual marked law. Conditional moments converge after division by its positive failure mass. |
| `tau^-2 log p_E(tau;b,u) -> -I(1,u)` | The preceding C4/cube-three spectral class, fixed direction and compact births; first take the contact limit at fixed critical ratio, then let that ratio grow. |

Here `F_r` means the prescribed saddle is not the actual elder partner,
`X_r=(b-d_f(M))/(k r^3)`, and the original typed determinant weight and full
normalizer are retained. The short-lifetime proof controls all tail sectors,
including a separate scalar hard-block argument. It uses no inverse hard
eigenvalue moment or assumed independence between the field norm and Hessian.

Together with the existing positive-moment theorem [POSITIVE, Section3] and
the existing failure-mass limit, the new inverse result gives the complete
finite-valued moment convergence range for this finite-failure convention:

    r^-3 E_Pr[X_r^q;F_r,ell_r finite]
                       -> integral lambda^q dmu_fail,
    E_Pr[X_r^q | F_r,ell_r finite]
                       -> (1/a_fail) integral lambda^q dmu_fail,
                                      every real q>-2/3.

The three cases are the new inverse theorem for negative q, the known mass
limit for q=0, and the already proved positive-moment transfer for q>0.
For q<=-2/3 the prelimit finite-failure moment is infinite at each fixed
positive separation, so there is no corresponding finite-valued convergence
claim. The essential class is explicitly excluded; including its infinite
lifetime would change positive moments. The separate fourth-power endpoint
law concerns additional sequential distant-partner conditioning.

The large-ratio theorem matches the SAME constrained RKHS energy `I(1,u)`
as the fixed-positive-gap rare-event theorem. It gives an ordered bridge,
with compact-birth uniformity for the contact share, and does not exchange
the separation and critical-ratio limits.

Both arguments are conventional author-side candidates. Fresh same-family
technical checks provide error detection; different-family scientific review
remains pending. No existing proof, workflow, status or premise file changes.

```sh
python -B -S frontiers/gaussian_lifetime_limit_completion_20261029/check_exact.py
python -B -S -O frontiers/gaussian_lifetime_limit_completion_20261029/check_exact.py
```

The standard-library script checks finite algebra and source identities.
The Gaussian, geometric and limiting-measure arguments are in the proof text.
