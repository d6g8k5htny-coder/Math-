# Canonical weighted probability and actual Cauchy–Schwarz transfer

Frozen before code, 25 October 2026. OpenAI/Codex root; scientific effect NONE.
Source: imports/hardening_ebedb780/P02-LM-008/proof.md.export.txt, sections 1–3,
at Math-main e75cb81e8961d178f43aa9967dddd11cd579dc8a.
This is the measure-theoretic interface, beyond the retained scalar algebra.

Sole new PalmReweighting.lean target: on a probability space with nonnegative
measurable real weight W, integrable W^2 and positive Z=integral W, construct
the literal weighted measure by density W/Z. Prove it has total mass one and
for every measurable event E its real probability equals integral over E of W
divided by Z. Derive W integrability from its L2 premise; do not assume the
conditional/Palm event identity or the Cauchy–Schwarz numerator bound.

For C>=0, c>0, r>0, if integral W^2 <= C*r^4 and c*r^2 <= integral W,
prove the actual weighted event probability <= (sqrt C/c)*sqrt(mu.real E).
The numerator estimate must follow from integral Cauchy–Schwarz and the event
indicator. All r-powers must cancel in the proved inequality. An equivalent
explicit normalized set-integral bound may be an auxiliary, but the final
statement must concern the constructed probability measure, not arbitrary
symbols p,z,n supplied as premises. No nonzero event probability premise;
include empty/null events and zero C wherever compatible with the other premises.

The already proved actual endpoint Gaussian second moment and common-coupling
normalizer floor supply the weight estimates once their concrete conditional
field inputs are identified. This generic weight construction does not by
itself identify a geometric Kac–Rice Palm law or arbitrary whole-field event.
Those actual-law/event joins remain in the original research scope.

Use narrow pinned imports, preserve old proofs/gate/pins and reuse completed
verification. Record exact commands/exits and meaningful mathematical controls.
Root alone updates root/manifest and final evidence. Different-family source
review remains separate from proof execution and author-side technical work.
