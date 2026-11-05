# Constructed C2 transverse ridge — frozen formal continuation

Add AdaptiveFoldTransverseRidge.lean for the existence/regularity step preceding
the completed scalar barrier. Reuse current pinned mathlib's C2 implicit-function
theorem and the already qualified cap strategy; do not reprove IFT or replay the
old cap/H0 library. No full Mathlib umbrella import.

Use literal coordinate partials of V : Real x Real -> Real, defined by fderiv
on the coordinate unit vectors. Structural inputs: C4 V on an open neighborhood
of a closed rectangle [l,u] x [-R,R], R>0, c>0, negative vertical second partial
at most -c on that rectangle, and strictly positive/negative transverse first
partial on its lower/upper boundaries. Supply all continuity/domain hypotheses.

Construct an open parameter neighborhood U of [l,u] and a function zeta, unique
among transverse roots in [-R,R] on U, with zeta in (-R,R), Vy(x,zeta)=0, and
C2 regularity on U. No preexisting zeta, its continuity or any ridge/elder
certificate may be a premise. A compact structural collar and equality to local
implicit functions must be proved, so full derivatives at the original interval
endpoints are valid. Treat behavior outside U as immaterial.

Derive first and second derivative jets from the zero equation, using the actual
partials Gx,Gy and D2G for G=Vy. Retain the nonzero denominator proved by vertical
concavity. From structural center/coordinate derivative bounds M0,M1,M2 on the
rectangle, derive |zeta|<=M0/c, |zeta1|<=M1/c and
|zeta2|<=(M2/c)(1+|zeta1|)^2. Coordinate bilinear bounds must be explicit; do not
silently identify product and Euclidean operator norms.

Expose the potential/profile derivative jets needed by AdaptiveFoldScalarBarrier
if the construction permits a concise adapter. Do not assume its conclusion as
a premise or claim actual Gaussian-source geometric signs have been discharged
unless a separate literal source adapter is proved. Actual ambient boundary/path,
H0/elder/counting and Parent A/B Lean theorems remain separate.

Root owns this frozen contract, registration/manifests/commits/publication.
Producer owns only the new source and scratch evidence. New-only compile, one
named kernel replay, exact axiom/inventory coverage and substantive positive/
negative controls are required. Preserve all failures, commands/exits, snapshots,
source/artifact identities and helper lineage; standard3 axioms, no admissions.
Reuse completed applicable31-module/25-input evidence under /workspace/AGENTS.md;
source-review process remains separate from mathematical verification.
