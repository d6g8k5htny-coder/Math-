# Cap I4: actual-kernel inner integration

Dylan Roy — delegated AI work. Actual author OpenAI / GPT-6 Astra Pro,
`cap-i4-inner-integration-r19-20261006`; pickup main#229/6017442778.
Scientific effect NONE; author/source-exposed; organizational credit 0.

This isolated branch joins the unchanged R16 and R17 sources. It changes neither
parent branch, production formal/, nor the integration queue. The source proof
P is bound at dfed3b8d318a3ab1950957f393307733a4bef3f2 with its erratum.
R17's clipped primitive is credited, not rediscovered. R18's outer Gaussian
moment work remains separately owned and is not implemented here.

## Exact scope

Five exact contracts connect R17's finite clipped integral to R16's actual
`depthKernel`, without an independent surrogate definition. The cutoff remains
lambda <= D*r*(j+Lambda)^2. The gap is nonnegative only on its original chamber;
the proof clips first and never integrates the signed gap beyond Lambda.
The inner bound retains both U^9 and U^8. The ninth-only corollary requires j>=1,
not merely j>=0. Radius r=0, K=0, Lambda=0 and cutoff equality are included.
These purely inner bounds allow r>=0 with no upper radius restriction; R16's
separate determinant-to-kernel reduction still requires r<=1. The Gaussian
inner drop permits c=0; finite outer Gaussian moments require c>0 separately.

The two-parent preparation is an isolated source union, not main integration or
proof acceptance. Parent source blobs are fixed in replay.py. An imports-only
stub is committed first: the actual exact-contract execution must fail at its
five missing theorem names before implementation is written. Results belong to
the exact tested head in main#229, not to this historical preparation text.

## Verification

From a full checkout with the existing pinned Lean/mathlib installed:

```sh
ROOT="$PWD"
(cd formal && lake env python3 -B -S "$ROOT/companions/cap_i4_inner_integration_20261006/replay.py")
```

The source-bound replay is adapted from R16, not a new acceptance framework.
It builds nine exact parent modules and this child, then the exact Contract,
five axiom/type reports, fresh leanchecker, and two inherited scalar/sign False
controls. Those controls do not independently prove the integration theorem.
Warnings remain errors. Timeouts retain available output but create no completed
process receipt. Before/after sources, hosted context and dependencies must match.

Seven finite/source methods include 256 domain controls,64 exact clipped
integrals,270 actual-kernel radius comparisons,27 Gaussian-exponent comparisons,
and a counterexample to U^8<=U^9 below1. These are not kernel proof. The initial
local Gaussian case loop had a two-tuple/three-variable fixture error; the failed
inspection was retained, corrected before publication, and both modes rerun.

No full-plane Tonelli assembly, outer moment estimate, Gaussian field density or
independence construction, Hessian bound, cap geometry, E4 bound, full normalizer,
family-uniform theorem or scientific-status promotion is supplied by this child.
Nonauthor alignment and any future eligible integration remain separate.
