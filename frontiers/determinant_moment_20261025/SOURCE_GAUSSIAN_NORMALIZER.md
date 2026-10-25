# Gaussian reference positivity and endpoint-box lower bound

Frozen before implementation, 25 October 2026. Author OpenAI/Codex root; coauthor
/root/normalizer_palm_research. Actual scientific review must use another family.

Source: reviews/lm006_normalizer_stability_20261005/NOTE.md at Math-main
 e75cb81e8961d178f43aa9967dddd11cd579dc8a, blob
5790aaa0332bd8e79b276be1577e4c5f3502eed6, SHA256
2e63518026cef54bb91757ccbdba986a0765f8a8b640240417ba30c59e2f5fd4.
Sections1–2 define T_r=F_r G_r for v=(aM,aS,bM,bS,cM,cS),
F_r=max(max(-aM,0)*max(-cM,0)-r*bM²,0),
G_r=max(r*bS²-aS*cS,0), and prove T_r equals physical typed W_r/r² for r>0.
Its contact value at v0(a,q)=(-1,1,-a/2,a/2,q,q) is (max(-q,0))².
This continuous weighted variable includes all singular/type boundaries.

Target gn_gaussian_reference_integrable_pos: for every real m and nonnegative
real variance v with v!=0, under gaussianReal m v the actual function
q |-> (max(-q,0))² is integrable and its integral is strictly positive. No assumed
positive moment, planar reference or zero-mean substitution is permitted.

Target gn_open_box_floor: define the literal T_r above. If r>=0, K>0,
r*K²<=1/4, aM in(-5/4,-3/4), aS in(3/4,5/4), cM,cS in(-2,-1),
and |bM|,|bS|<K, prove T_r(v)>=3/8. This is a new explicit open-box consequence
of source formula(1), not a claim that the source stated these exact constants.
Its proof uses F_r>=1/2 and G_r>=3/4, without inverse eigenvalues.

Research application: a nondegenerate reference Gaussian Q charges(-2,-1).
Together with finite mixed coordinates, an increasing family of these boxes has
positive reference mass for some K. Under actual endpoint weak convergence,
Portmanteau gives mass>=p/2 eventually, and integration gives the full-normalizer
floor Z_r>=(3p/16)*r². The current targets prove reference positivity and the exact
pointwise weight component, not the concrete field convergence or box-mass claim.
That missing conditioned-derivative/Palm identification remains in the research
scope and must be supplied; it is not replaced by a target-assuming hypothesis.

Implementation is one new GaussianNormalizer.lean module with narrow pinned
Mathlib imports, using the same Lean4.34.1/mathlib revision and the unchanged
kernel/axiom/control gate. Preserve all prior proof/evidence bytes and check only
new code during development. No old source review is silently rebound. This
source note does not qualify as an independent scientific review or status change.

## Full lower-floor deduction from a common coupling: frozen before code

New NormalizerFloor.lean target: on one probability space let X_r be measurable
six-endpoint vectors in LM006 order(aM,aS,bM,bS,cM,cS). Suppose as r->0+ they
converge almost surely to(-1,1,-A/2,A/2,Q,Q), where Q has gaussianReal(m,v)
law with v!=0 (m arbitrary), and each T_r(X_r) is genuinely integrable for
positive r sufficiently near0. Then prove existence of c,delta>0 with
integral r²*T_r(X_r) >= c*r² whenever0<r<delta. All-measure or sequential
formulation details must preserve this full conclusion, not replace it by a
weaker sample-sequence floor. Current integrability is not an assumed moment
upper bound or normalizer lower bound, and is supplied by the Gaussian endpoint
moment result in applications.

The proof may use Fatou for nonnegative weights: T_r(X_r) converges pointwise to
(max(-Q,0))²; its positive integral is proved, not assumed. Thus UI/full moment
asymptotics and type-boundary nullity are unnecessary just for a lower floor.
No normalized-expectation-limit, positivity or desired floor may be added as a
premise to obtain a passing proof. Source LM006 stability sections2,4 supplies
the literal continuous weight and common coupling interpretation. Actual field
construction/identification of such a coupling remains a concrete input join,
not an implication of this generic theorem.
