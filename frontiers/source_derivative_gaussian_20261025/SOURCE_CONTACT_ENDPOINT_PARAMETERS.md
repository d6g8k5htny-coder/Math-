# Actual limiting endpoint mean and covariance contact relations

Frozen before code, 25 October 2026. OpenAI/Codex root and
/root/normalizer_palm_research. Scientific effect NONE.
Source LM006 endpoint-extension NOTE sections 3–4 and stability NOTE sections
2,5, with immutable identities in the sibling Gaussian source contracts.

Sole new SourceContactEndpointParameters.lean. On the actual smooth source2L,
let J=(f,fx,fy,fxx,fxy,fxxx), A=fxxy and Q=fyy at0, and define
T=(-J5/2,J5/2,-A/2,A/2,Q,Q). Set G0=Cov(J,J), C0=Cov(T,J),
B0=Cov(T,T), d0=(b,0,0,0,0,2),
m0=C0 G0^(-1)d0, S0=B0-C0 G0^(-1)C0^T.

For L!=0 and arbitrary real b, prove G0 unit from completed actual contact
positivity, S0 PSD from an actual Gaussian/residual covariance, and exactly
the GaussianNormalizerLimit contact relations:

    m0_0=-1, m0_1=1, m0_2+m0_3=0, m0_4-m0_5=0,
    S0_00=0, S0_11=0,
    S0_22+2*S0_23+S0_33=0,
    S0_44-2*S0_45+S0_55=0, and S0_44>0.

The last strict inequality must be joined to the actual curvature residual
Schur variance already proved in SourceContactSchur, not assumed. Mean and
zero-variance identities follow from literal linear relations in T and the
conditioned cubic pin value2, not an assumed contact vector law. Preserve
the actual noncentered Q mean; no planar N(-b,2) substitution. An actual
contact Gaussian kernel/law identification is useful but not needed to
replace the concrete matrix/contact conclusions.

Coordinate the literal T,C0,B0 definition names with the SourceConfluentLimits
owner. Reuse the completed regression/Schur/covariance proofs and verify only
this new module. Root owns integration/evidence and different-family review.
