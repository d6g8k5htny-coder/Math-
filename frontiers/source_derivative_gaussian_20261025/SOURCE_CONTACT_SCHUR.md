# Literal six-pin covariance and reference Schur variance

Frozen before code, 25 October 2026. OpenAI/Codex root and
/root/regression_kernel. Scientific effect NONE.

Sole new SourceContactSchur.lean, depending on the completed actual-source
SourceContactCovariance and generic ContactJetCovariance certificate. Define
the actual principal six-pin covariance G, cross vector b and Q variance d
from sourceContactCovariance in order (f,fx,fy,fxx,fxy,fxxx; Q=fyy).
From L!=0 alone, prove G positive definite and invertible, and
d - b dotProduct (G inverse mulVec b) > 0. Supply the exact reindexing between
the actual seven-observation covariance and its 6+1 block representation;
no assumed block identity, pin invertibility, Schur positivity or variance
lower bound is allowed. The existing contact_schur_pos may be applied after
the literal block identity and positivity transport are proved.

If short, express this as the actual variance of Q minus its linear least
squares prediction from J using the proved covariance formulas and Gaussian
L2 integrability. This may be a consequence, not a premise. Preserve arbitrary
period L!=0, and do not identify a torus conditional mean with planar -b or
a variance with 2. Finite-r invertibility and parameter limits remain separate
original research obligations.

Reuse all completed module/kernel/axiom/control evidence on unchanged files.
Check only this new module and its own mathematical controls. Root owns
Lake/source/evidence integration and different-family scientific review.
