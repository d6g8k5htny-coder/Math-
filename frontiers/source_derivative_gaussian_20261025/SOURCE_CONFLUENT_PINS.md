# Actual six pins and an invertible confluent frame

Frozen before code, 25 October 2026. OpenAI/Codex root and
/root/dm2_landed_composition. Scientific effect NONE.
Source: LM006 endpoint-extension NOTE section 2 (immutable identity in sibling
SOURCE_GAUSSIAN_COUPLING.md). This is that particular equivalent frame, not the
different GP-DER-044 historical frame.

Sole new SourceConfluentPins.lean. In raw pin order
(fM,fS,fxM,fxS,fyM,fyS), define for r!=0

    P0=(fM+fS)/2, P1=(fxM+fxS)/2, P2=(fyM+fyS)/2,
    P3=(fxS-fxM)/r, P4=(fyS-fyM)/r,
    P5=(12/r^2)*(P1-(fS-fM)/r).

Prove this is an actual continuous linear equivalence with inverse

    fM=P0-r*P1/2+r^3*P5/24,
    fS=P0+r*P1/2-r^3*P5/24,
    fxM=P1-r*P3/2, fxS=P1+r*P3/2,
    fyM=P2-r*P4/2, fyS=P2+r*P4/2.

For literal prescribed raw pins (b,b-r^3/6,0,0,0,0), prove the transformed
value is exactly (b-r^3/12,0,0,0,0,2). Preserve arbitrary real b and r!=0;
do not substitute an incorrect nonzero P1 or the planar conditional mean.

Define these raw observations as the actual values and x/y first derivatives
of smoothSourceField 2 L at (-r/2,0),(r/2,0). Derive their joint Gaussianity
from the completed heterogeneous derivative theorem. Define actual confluent
pins by the proved linear equivalence and derive Gaussianity as a CLM image.
Optional joint Gaussianity with actual endpoint second derivatives may be
included by one finite heterogeneous derivative vector, not by assuming
Gaussianity of the endpoint variables or independence of observations.

This proves the literal pin transform and prescribed target. Covariance
limits/invertibility, integral formulas for adjusted endpoints, regression
block identification and actual Palm events remain original research work.

Reuse completed verification. Narrow pinned imports and only this new module;
root integrates Lakefile/source inventory/evidence. No old-source edits,
invented scientific acceptance, custom axioms or assumed conclusions.
