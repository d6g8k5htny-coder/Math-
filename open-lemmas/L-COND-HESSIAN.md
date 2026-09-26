# L-COND-HESSIAN — Conditional Hessian moments after rare target

**Status in this map:** open lemma (only for regimes not already covered).

## Target

Uniform integrable bounds on products of `|det H_M det H_S det H_X|` (typed) after conditioning on the rare witness gradient target, in regions still open for RN synthesis.

## Already accepted (do not re-open)

- Fixed-transverse R4
- Annulus-bridge R3 (full conditional C³ moments)
- Fixed-annulus height-window stitch
- Two-scale S16 (extra-conditioned sixth moment)

Those accepts already cover the fixed scaled annulus, including the transverse belt inside `K_AB`.

## Tasks to close

1. Prove a sufficient sixth-moment (or product) bound on the remaining holes: pin neighborhoods and mesoscopic distances `r ≪ dist ≪ ρ` ([L-PIN-COLLISION](L-PIN-COLLISION.md), [L-SHRINKING-EXCLUSION](L-SHRINKING-EXCLUSION.md)).
2. Feed each new bound into a weighted Kac–Rice ledger with the original endpoint normalizer.
3. Keep the fixed-annulus / transverse accepts unchanged.

## Notes

Do not substitute bare Gaussian gradient-density smallness for a weighted count without this control outside the accepted charts.
