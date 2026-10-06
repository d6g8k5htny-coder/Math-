# Cap I4: spectral-plane to iterated-chamber bridge

Dylan Roy — delegated AI work. OpenAI / GPT-6 Astra Pro,
cap-i4-chamber-bridge-r21-20261006; pickup main#229/6020425628.
Author/source-exposed, organizational-independence credit0, scientific effect NONE.
Isolated child of R20 76e307707e8fc37d4264210da86915e6ba0be81a.

## Exact scope

Four statements connect the existing spectral-plane expression to R20's finite
iterated bound. First, a measurable nonnegative test on 0<lambda<Lambda is
integrated in reverse order: Lambda>0 outside and 0<lambda<Lambda inside.
The coordinates are NOT swapped in the test, and no extra Jacobian appears.
The proof uses the pinned symmetric nonnegative Tonelli theorem and indicators;
no finiteness assumption is needed for this equality.

Second, specialize to the exact R16 kernel, Gaussian reference envelope and gap,
keeping pi inside the original residual integral until extracting it by its
measurable nonnegative integral identity. The residual measure is arbitrary for
this equality, not silently normalized. The two remaining statements transfer
R20's explicit finite r^5 estimate and finiteness to the original plane expression.
They retain finite residual mass, AE j>=1, integrable |j|^9, c>0, k0>0 and all
nonnegative parameter assumptions. The actual cutoff remains lambda<=L inside
the unchanged depthKernel. r>=0 in the bound does not erase upstream r<=1 or
permit normalization at zero.

This does not instantiate the actual field density/independence/Hessian/weight
bounds, prove uniform family constants, handle E4 or cap geometry, or divide by
a full normalizer. No MatrixDepthTransport or persistence acceptance is promoted.
The prior exact sources and reviews retain their own scopes. Parent branches,
production formal/, manifests and existing workflows are not modified.

## Execution and provenance

The initial module has imports only: its four exact Contract applications must
fail with absent declarations before proof bodies are supplied. Seven finite
source tests alone do not establish theorem completeness; the exact Contract,
type/axiom reports and completed fresh kernel check are separate requirements.
The source runner is a scoped adaptation of the unchanged R20 replay0c907680,
not another evidence framework. It binds twelve exact parent Lean blobs, builds
them with the child, checks all four types and transitive axioms, and executes
leanchecker --fresh followed by inherited scalar/sign rejection controls.
Those negatives do not independently prove the measure rearrangement.

Pinned Lean4.34.1/mathlibd13f23b723b8a846827a245b89c10fc7d3f11612 is unchanged.
The actual API inspected is Measure/Prod.lean blobdcda187671ab2b4ded4e301fb30ca0391eb41c3b:
lintegral_prod_symm, with both component measures s-finite. Here both are Lebesgue.
Public generated documentation was used for discovery only, not as a new pin.

From a complete checkout with the pinned dependencies:

```sh
ROOT="$PWD"
(cd formal && lake env python3 -B -S "$ROOT/companions/cap_i4_chamber_bridge_20261006/replay.py")
```

An existing output directory fails rather than inheriting old evidence. All
completed commands, failed outcomes and source-before/after contexts are kept.
No local Lean run is claimed when unavailable. A successful hosted run and a
nonauthor scoped read are distinct; this branch is not a main integration PR.
