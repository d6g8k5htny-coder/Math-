# Actual source endpoint moment, normalizer and weighted-event estimates

Frozen before code, 25 October 2026. OpenAI/Codex root and
/root/dm2_landed_composition. Scientific effect NONE.

Sole new SourceEndpointEstimates.lean. Combine the actual source confluent
covariance limits, contact pin/Schur positivity and contact parameter relations,
canonical every-pin kernel Gaussian law, and regression limits with the already
verified moment/normalizer/Palm-reweighting components. Those components are
byte-identical inputs from the 66-target packet at16f81b973a02783f8be83081aa7f198724cf5767,
whose source hashes and execution receipt are recorded in INPUT_BINDING.json.

For every L!=0 and fixed real height b, derive constants C>=0,c>0,delta>0,
delta<=1 such that for all0<r<delta the literal canonical adjusted endpoint
law K_r at sourcePrescribedPins(r,b) has physical weight W_r with

    Integrable(W_r^2,K_r), integral W_r^2 <= C*r^4,
    c*r^2 <= integral W_r.

Here the LM006-order vector is explicitly permuted to the actual egm order
(aM,bM,cM,aS,bS,cS); the strict maximum/saddle determinant weight is the
proved literal one, not a midpoint quartic replacement. Derive all actual
Gaussian laws, uniform parameters, current invertibility, PSD/contact moment
conditions, integrability and floor from the preceding actual-source results;
do not add any of those desired conclusions as model premises. No uniformity
over unbounded b is asserted. Means remain noncentered and target covariances
may be singular.

Construct the explicit W_r-weighted endpoint probability from K_r and derive
for every measurable endpoint event E the bound
weightedProbability(E) <= sqrt(C)/c * sqrt(K_r.real(E)).
This is the actual endpoint reweighting interface. Whole-field geometric
Kac–Rice/Palm identities and arbitrary field-dependent events, GT5 and further
parents still require their actual remaining joins; do not claim them from
an endpoint marginal. Intermediate composition lemmas are useful, but a final
actual-source theorem may not assume the desired covariance limits or kernel
law merely to make it compile.

Coordinate exact public APIs with the owners of SourceConfluentLimits and
SourceContactEndpointParameters. Preserve all completed verification and
artifacts; only this new affected module receives new checks. Root integrates
source/evidence and different-family review. No historical-source edits.
