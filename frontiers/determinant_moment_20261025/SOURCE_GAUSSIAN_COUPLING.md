# Gaussian square-root common coupling: frozen before implementation

25 October 2026. Author OpenAI/Codex root and
/root/normalizer_palm_research; scientific review requires another family.

Source LM006 stability NOTE section 5, as bound in
SOURCE_GAUSSIAN_NORMALIZER.md, constructs one standard-Gaussian square-root
coupling and explicitly permits singular limiting covariance. The concrete
endpoint covariance extension is in
reviews/lm006_endpoint_extension_20261005/NOTE.md, sections 3–4, at Math-main
e75cb81e8961d178f43aa9967dddd11cd579dc8a, blob
551aa563562bc88a19e33d146259c03aa2d318f6, SHA256
d860fd4669f168c117b67066550047bfa2fcd90d77bbc366d978b6112e9f3757.

Frozen new GaussianCoupling.lean target: for any finite real dimension and
filter u, means m_r tending to m_0 and covariance matrices S_r tending to S_0,
with S_r positive semidefinite eventually and S_0 positive semidefinite, prove
for EVERY standard Gaussian coordinate z convergence of
m_r + toEuclideanCLM(CFC.sqrt S_r) z to
m_0 + toEuclideanCLM(CFC.sqrt S_0) z. No invertibility, positive determinant,
fixed rank, zero mean or pre-existing coupling-convergence premise is allowed.
Also prove the exact HasLaw of each such affine vector under stdGaussian as
multivariateGaussian(m_r,S_r). These are the actual pinned Mathlib definitions,
not a newly assumed representation. A measurable coupling or almost-sure
version may be exported as a consequence. CFC continuity on the PSD cone may
be used; do not assume a Lipschitz estimate at a singular covariance.

The application still must supply actual conditional means/covariances and
their limits, contact-coordinate identities and nonzero reference variance.
This generic result constructs the common finite endpoint coupling once those
quantities are identified; it does not identify the whole conditioned field
or arbitrary field-dependent geometric events.

Sole new production module, narrow pinned imports, preserved prior proofs and
verification. Root alone updates root/manifest. No scientific-status change.
