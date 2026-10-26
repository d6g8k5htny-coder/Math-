# Normalizer floor directly from Gaussian parameter limits

Frozen before implementation, 25 October 2026. OpenAI/Codex root and
/root/normalizer_palm_research. Scientific effect NONE.
Sources: the immutable LM006 endpoint-extension and stability notes identified
in SOURCE_GAUSSIAN_COUPLING.md and SOURCE_GAUSSIAN_NORMALIZER.md.

Sole new GaussianNormalizerLimit.lean target combines already proved square-root
coupling, Gaussian reference positivity, Fatou and the actual endpoint identity.
Let m_r and S_r be six-dimensional Gaussian means/covariances in LM006 order
(aM,aS,bM,bS,cM,cS), tending as r->0+ to m0,S0. Assume eventual PSD S_r and
PSD S0, allowing singular matrices. Assume only the concrete contact moment
relations

    m0_0=-1, m0_1=1, m0_2+m0_3=0, m0_4-m0_5=0,
    S0_00=0, S0_11=0,
    S0_22+2*S0_23+S0_33=0,
    S0_44-2*S0_45+S0_55=0, and S0_44>0.

Prove existence c,delta>0 such that for every 0<r<delta,
integral r^2*T_r(v) under multivariateGaussian(m_r,S_r) is at least c*r^2.
Do not assume an almost-sure contact vector, common-coupling convergence,
weight integrability, normalized-expectation convergence or a desired floor.
Derive contact identities from zero variances under the limiting Gaussian;
derive Q's genuine Gaussian law with arbitrary mean m0_4 and nonzero variance;
construct the common square-root coupling from parameter convergence; and
obtain current integrability from Gaussian polynomial moments. The actual
literal endpoint-weight integral follows by the proved coordinate permutation
and weight identity. Export this consequence if it remains short.

This freezes a concrete finite-dimensional Gaussian normalizer theorem. Actual
conditional-field mean/covariance identification, their limiting contact
relations and positive Q Schur variance must still be established for the
torus source. These remain original research obligations, not outside scope.

Narrow pinned imports; preserve earlier proof/evidence and reuse completed
verification. Root owns final integration and provider-distinct review routing.
