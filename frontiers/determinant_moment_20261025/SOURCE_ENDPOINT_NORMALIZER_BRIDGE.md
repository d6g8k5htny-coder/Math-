# Literal endpoint weight and continuous normalizer: frozen before code

25 October 2026, OpenAI/Codex root. This adds a mathematical join to the
ongoing original research goal; it makes no scientific-status change.

Sources and immutable identities are already recorded in
SOURCE_GAUSSIAN_MOMENTS.md (GP-DER-047 section 13, actual endpoint vector) and
SOURCE_GAUSSIAN_NORMALIZER.md (LM006 stability sections 1–2, continuous weight).
The two coordinate orders differ and must be converted explicitly:
egm order (aM,bM,cM,aS,bS,cS) becomes gn order (aM,aS,bM,bS,cM,cS).

Frozen target for a sole new EndpointNormalizerBridge.lean module: define that
literal permutation and prove, for every real six-vector and r>0,
egm_weight r j = r^2 * gn_normalizedWeight r (permutation j).
Keep the exact strict negative-definite maximum condition and strict negative
saddle determinant. The identity must hold on all zero/type boundaries, with
no assumed negative eigenvalues, null-boundary premise or Gaussian hypothesis.
It follows by the 2x2 Sylvester criterion and positive/negative parts of the
determinants. A random-vector integral equality and the transfer of the proved
common-coupling lower floor to the literal egm_weight may be included as proved
consequences, not assumed identities. Do not replace the actual six-vector by
the source's normalized quartic nine-vector.

An eventual integrability premise in the generic floor is permitted at this
join, but the Gaussian endpoint moment theorem supplies it in applications:
the physical weight is L2 and hence L1 on a probability space, and division by
the nonzero scalar r^2 recovers integrability of the normalized weight. Concrete
conditioned-field construction and convergence remain research obligations;
they are not claimed from this algebraic identity alone.

Preserve existing proofs and evidence. Narrow pinned Mathlib imports only;
root alone integrates the root module, target manifest and final gate receipt.
Source review requires a different actual model family from OpenAI authors.
