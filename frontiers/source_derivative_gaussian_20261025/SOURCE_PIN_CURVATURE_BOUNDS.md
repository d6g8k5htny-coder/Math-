# Frozen source contract: actual pin curvature bounds

Base 37f8f01db8b7e30190f09bf784d1b4e3419da540; 26 October 2026.
Owner /root/dm2_landed_composition. Sole production file SourcePinCurvatureBounds.lean.
Consume unchanged 18 qualified modules and 23 exact inputs; do not recheck them.
Define measurable R=1+sum k:Fin 6, sourceDerivativeMajorant L k, prove R>=1.
For actual smooth samples on X3=X4=0, X5=2 and 0<r<=1, prove the six
normalized endpoint errors around (-1,1,-a/2,a/2,q,q), with errors <=r Gamma4
for first four and <=r Gamma3 for last two; q=fyy(0), a=fxxy(0).
Derive individual first-four coordinate absolute bounds by R, factored actual
endpoint determinant bounds R*|q|+2*r*R^2, and literal physical typed weight
W<=2*r^2*R^2*q^2+8*r^4*R^4. Actual Peano identities and derivative bounds are
required; no midpoint quartic substitution or assumed desired endpoint bound.
On positive strict max/saddle weight support prove q<r Gamma3. Therefore
q>=-K*r*R^5 implies |q|<=max(K,1)*r*R^5. Preserve zero-weight type boundaries.
Derive application a.e. on the actual prescribed-pin law from completed support.
If exporting raw radius, literal q-inclusive nine-jet radius is bounded by
1+Gamma2+3 Gamma3+5 Gamma4<=5R; validate exact coordinate normalization.
Do not claim noncapture inclusion or adjacency from these bounds alone.
Only standard Lean axioms; no sorry/admit/custom axiom/native_decide.
New-module compile, kernel, axiom and meaningful controls, raw receipts with
before/after source hashes; no unchanged baseline reruns. Different-family
scientific review remains separate from author-side qualification.
