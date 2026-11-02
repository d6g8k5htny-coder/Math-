# Actual fixed-axis Gaussian source: wide rectangle and attained path

Add SourceAdaptiveFoldEstimates.lean. Reuse the qualified actual chart and
boundary/path modules; authoritative implementation map is
/workspace/scratch/actual-fold-estimates-preflight/REPORT.md. This continuation
must derive the missing wider elder-rectangle data from actual source majorants,
normalized pins and Peano. The old half-unit capture gates are not a substitute.

On the SAME original sample use exactly Gamma=sourceGammaRadius L sample,
D=max(1,1/(6*k0)), T=D*(8*Gamma), physicalq=sourceQ L sample,
kappa=-physicalq/(6*k*r), V=actualFoldPotential r k sample,
R=4/sqrt(kappa), c=kappa/2,M0=T,M1=3*T,M2=T,A=2-3*r*T.
Keep the r denominator in kappa. Inputs are hL:L!=0, k>=k0>0, r>0 and actual
sample cutoffs r*T^5<=1/100 and 1024*T^5<=kappa. Existing normalized actual
source data may be an INTERNAL deterministic adapter premise, discharged from
the chart law in every CLOSED public actual-law endpoint.

Required closed actual-law theorem sourceGapLaw_structural_rectangle:
there exists delta>0,delta<=1 derived from hL alone BEFORE k0,r,b,k, such that
for every k0>0,0<r<delta,b real,k>=k0, almost every sample under the exact
sourceGapLaw hL r b k satisfies:
  r*T^5<=1/100 -> 1024*T^5<=kappa ->
  StructuralRectangleData V univ R c T (3*T) T (2-3*r*T)
  AND T/c<=R AND 1<=(c/2)*(R-T/c)^2.
No final IsUnit, normalized/raw pin, desired sign/derivative/profile/budget/ridge
or path premise. Derive all fields, not a wrapper around assumed structural data.
A second closed actual-law corollary sourceGapLaw_actual_rectangle_boundary_path
must call the qualified boundary constructor and return ONE witness U,z carrying
its RidgeScalarData and RectangleBoundaryPathData. Pointwise posterior counterpart
is optional if direct. No probability of the cutoffs is asserted in this slice.

Finite analytic requirements, retaining literal ordered coordinate entries:
1. Reuse generic pullback_jet plus actual source derivative majorants to prove
   all third coordinate entries <=T and fourth coordinate entries <=r*T. New
   wrappers for D2(Vy)[u,v] append physical Y LAST; D2(Vx)[u,v] append X LAST.
   Keep both mixed orders explicit. Derive Hy=Gx from the proved actual source
   permutation identity, never an unproved symmetry or Euclidean norm premise.
2. Prove the new generic full-jet two-zero bound on J=[-3/2,3/2]: if g(+-1/2)=0
   and |g''|<=T, then |g(x)|<=(T/2)|x^2-1/4|<=T and |g'(x)|<=2T for ALL
   x in J, including outer arms. Convex comparisons T*q+-g plus Rolle suffice;
   do not use an interpolation theorem valid only between the pins.
3. Coordinate mean-value transport gives |Gy(X,Y)-Gy(0,0)|<=T(|X|+|Y|),
   |Gx(X,Y)-Gx(X,0)|<=T|Y| and the analogous Hy bound; for
   K=D2(Vx)[ex,ex], |K(X,Y)-K(u,0)|<=r*T(|X-u|+|Y|).
   No product operator norm may be silently replaced by an entrywise bound.
4. From R<=1/8 derive |Gy+kappa|<=2T, Gy<=-kappa/2, center |G(X,0)|<=T,
   |Gx|,|Hy|<=3T, and strict opposite G boundary signs by integrating Gy
   from0 to+-R; use T<2sqrt(kappa). These must hold on the FULL J rectangle.
5. Peano weight w=3/2-6u^2 is nonnegative with mass1. Reuse the completed
   abs_weighted_integral_sub_mass_le and actual normalized integral2 to obtain
   |2-K(X,Y)|<=3*r*T, hence axial lower A. Do not reprove old Peano mathematics.
6. Pure numerical glue from T>=1,r>0,r*T^5<=1/100,1024*T^5<=kappa:
   kappa,c,R positive; R<=1/8; 2T<=kappa/2; T<2sqrt(kappa);
   r*T<=1/100; s=6T/kappa<=1; profileError c (3T) T<=42T^2/kappa
   (the safe72 bound also suffices); 1+profileError<=2-3rT;
   T/c<=R and (c/2)(R-T/c)^2>=1. Supply actual positivity before divisions
   and square-root identities before squaring.

Root may dispatch two disjoint scratch-only helpers: fold_two_pin_bounds for2,
fold_numeric_budget for6. Producer integrates required frozen bodies once with
exact helper lineage, owns actual ordered jets/oscillation/assembly/law endpoint.
No worker may dispatch subagents. Root owns registration/manifests/commits/posts;
producer owns only new source plus its scratch. Narrow imports, standard3 axioms,
no admissions/customaxioms/native_decide/implemented_by/full Mathlib umbrella.
Reuse all completed34-module/25-input qualifications and accepted conventional
source/Peano/Cap/H0 evidence; no old rechecks for handoff or pending process.

Controls must cover the extended arm: g=(x^2-1/4)/2 at x=3/2,T=1 saturates
|g|=1, refuting a false central-only T/8 bound on J. Numeric positive controls
T=1,r=1/10000,kappa=1024 instantiate every budget. Dropping only the large-kappa
cutoff, T=1,r=1/100,kappa=1 has profileError=342 and violates the advertised
curvature budget; dropping only r-smallness, T=1,r=1,kappa=1024 gives A=-1
and also violates it. Prove real counterexamples and a sole-False expected
rejection for at least the omitted-kappa mutation. Exercise the CLOSED actual
law interface at nonzero b and k!=1/6 with no IsUnit/pin premise; no high-cutoff
probability conclusion may be inferred from an implication control.
New-only strict compile, exactly ONE named ownmodule kernel after finalsource,
exhaustive classified axiom/inventory coverage, all failures/commands/exits/
source-object identities and measured or honestly unavailable timings. Helper
scratch elaboration is not a separate duplicate kernel/audit qualification.

Actual conditional statement remains centered fixed-axis. Framed-law/isotropy,
physical injective torus chart/frontier, endpoint/H0/elder interpretation,
measurable weighted events and bad-probability/count/density Parent A/B Lean
joins remain later obligations. Scientific effect NONE; provider-distinct
new-source review remains separate from completed mathematical evidence.
