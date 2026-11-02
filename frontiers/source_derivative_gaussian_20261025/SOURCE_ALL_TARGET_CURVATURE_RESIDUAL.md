# Whole-carrier curvature reconstruction: all-target residual radius

Add SourceAllTargetCurvatureResidual.lean. This is the independent next formal
join in /workspace/scratch/actual-fold-cutoff-probability-preflight/REPORT.md
item2; completed mathematics there and in old SourceCurvatureDecomposition is
reused, not rechecked. Import existing SourceCompactTargetMoments and
SourceCurvatureDecomposition, not the active new probability/weight modules.

Define S(hL,r,p,rho)=sourceGammaRadius L(posteriorSample hL r p rho), literal
SAME smooth carrier and arbitrary six-vector targetp. Prove measurability and
S>=1, posterior contactQ absolute bound byS. Generalize existing reconstruction
majorant/shift-image/moment interfaces to p, keeping oldexports untouched.
Use existing curvaturePosterior_residual_eq_shift (alreadytakesp), all-target
posterior moments and direction envelope at b=0 (covariance direction is
target-independent). Do not redo whole-carrier independent scalar/productlaw
or Gaussian interval-density proofs already available for everyp.

Required closed uniform endpoint: hL:L!=0 alone chooses0<delta<=1 and fixed
nonnegative A,H BEFORE r,p,rho,q,n such thatfor0<r<delta,
Gamma(curvatureReconstruct hL r p rho q)<=A*(absq+S(hL,r,p,rho)), and the
residual-image bound usesGamma(posteriorSample hL r p omega)+H*abs(curvatureZ).
For every naturaln derive Cn>=0 independentofr,p with integrable S^n under
curvatureResidualLaw hL r and integral<=Cn*(1+normp)^n. Covarianceinvertibility,
positivevariance and summable envelopes are derived internally, not final
certificatepremises. Same signed periodincludingnegativeL; no mean-zero
assumption or replacement p.

A useful corollary substitutes literal sourceGapPins r b k, |k|<=K,K>=0,
r<=1, to get moment<=Cn(L,K)*(1+absb)^n on onehL-onlyinterval, allb,k,n.
Its integration law is the ACTUAL residual law, not sourceGapLaw mislabeled
as residual. The targetnorm bound and original all-target posterior moments
alreadyproved are dependencies, not new math/review obligations.

Freezecontrolcontract BEFOREcode. Producer ownsONLYnewsource and
/workspace/scratch/all-target-curvature-residual-construct. No workers,oldfile/
config/cache/manifest/commit/post edits. Root ownsregistration/cache/publication.
New-onlystrictWerrorcompile, EXACTLY ONE namedownmodulekernel AFTERfreeze,
exhaustivemodule-index allconstant standard3 axiom/classification, meaningful
negativeL=-1/genericp/nondefaultgap/b controls andexactolddefault-radius
specialization. Checktargetgrowthfactor andradiusquantifierorder, n=0case,
same reconstruction/carrier andmoment law. A counterexample-backed false
arithmetic step erasing polynomialtargetgrowth can be a soleFalsemutation;
state that scope honestly, not a counterexample to all possible uniform
moment bounds. Preserveallfailures/commands/exits/times/sourceobject/lineage.
No sorry/customaxiom/native_decide/implemented_by/Mathlibumbrella oroldreplay.
Nevercopycontrol/helperobjectstoproductioncache.

This gives all-target residual domination/moments, not weightedr5numerator,
positivecompactnormalizer or normalizedvaryingmarkprobability. Existing
conventional Parent math remainsaccepted onits evidence. Canonicalpartner/
conditionalMorse,framedlaw/countdensity/ParentLean remainseparate. Provider-
distinctprocessseparate; scientificeffectNONE.
