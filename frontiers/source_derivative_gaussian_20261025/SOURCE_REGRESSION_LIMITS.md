# Continuous regression blocks and uniform small-radius parameters

Frozen before code, 25 October 2026. OpenAI/Codex root and
/root/normalizer_palm_research. Source LM006 endpoint-extension NOTE section 4,
immutable identity in sibling SOURCE_GAUSSIAN_COUPLING.md. Scientific effect NONE.

Sole new GaussianRegressionLimits.lean. For arbitrary finite pin/target sizes,
let G_r,C_r,B_r,d_r converge as r->0+ to G0,C0,B0,d0, with G0 invertible.
Define the actual regression formulas
m_r=C_r*G_r^(-1)*d_r and S_r=B_r-C_r*G_r^(-1)*C_r^T.
Prove eventual invertibility of G_r and convergence of m_r,S_r to those same
formulas at0. Do not assume current invertibility, regression parameter limits
or boundedness as premises. Matrix determinant/inverse continuity on its unit
domain may be used. No inverse or nondegeneracy is required of target S_r/S0.

Derive existence of B,V>=0 and delta>0 such that every0<r<delta satisfies
all coordinate mean absolute values<=B and all covariance diagonal absolute
values<=V. This supplies the Gaussian moment bounds once the literal
conditional law/variance identities are joined. Preserve empty finite sizes
if the underlying matrix APIs permit them; do not require zero means or a
planar covariance. Concrete pin target d_r is already identified in
SourceConfluentPins; actual source G0 invertibility is in SourceContactSchur.

The required G,C,B limits must still be proved by the actual coefficient/Peano
identities, not assumed proved for the source merely by this generic theorem.
Preserve/reuse all completed verification, narrow pinned imports, new-module
checks only. Root integrates Lake/evidence and different-family review routing.
