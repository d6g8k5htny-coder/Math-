# LM001 Q2/Q3 first Lean algebra artifact

Scope: scratch-only mechanization of algebra in the already closed conditional
P02-LM-001 capsule, under root authorization 26 October 2026. This is not new
scientific verification of the paper certificate. No production source,
manifest, lakefile, commit, post, or unchanged baseline proof has been edited
or rerun.

Exact source capsule:
`/workspace/Math-curvature-20261026/imports/hardening_ebedb780/P02-LM-001/proof.md.export.txt`.
Exact polynomial and constants imported from qualified
`SourcePinPreservingQuartic.lean` (final source SHA
8e23717ef98518b6d701db921d1f17958c3dee2c893745cafa7aa6172f1621d9).

In namespace `I4QuarticCaptureAlgebra`, for U : Fin 8 -> R define:

* R = rawRadius U = 1 + sum_i |U i|.
* regular r U means r R^5 <= 1/(1024 quarticK0), with quarticK0 = 4096.
* W = captureWidth r U = quarticFstar r U/(quarticK0 R^5).
* quarticFstar r U = 1+|U 0|/8+r|U 4|/48.
* sigma = captureSigma r U = 4 R W.

GeometrySupport.lean (author /root/uniform_jet_moment_sources) derives R>=1,
each |U i|<=R-1, W>0 for r>=0, RW<=1/2048 for r<=1, sigma<=1/512,
and r<=W/1024 from r>0 and regularity. No desired gate is assumed.

CaptureAlgebra.lean (author /root/regression_kernel) proves the independent
transverse forcing bound Fstar-1, the Y-dependent transverse remainder bound
2RW, and the axial remainder bound (3/4)RW on |X|<=1/2, |Y|<=W. Their helper
premises are explicit monomial bounds and derived by GeometrySupport in the
final gates.

CaptureGates.lean (author /root/regression_kernel) has exactly these public
gates, using the imported literal pinPreservingQuartic r q U:

* quartic_strip_upper: r>0, r<=1 and q/r<=-(2 K R^5+2R) imply
  Py(X,W)<=-1 for |X|<=1/2.
* quartic_strip_lower: the same imply Py(X,-W)>=1.
* quartic_central_transit: r>0, r<=1 and regular r U imply
  Px(X,Y)<=-3RW<0 whenever |X|<=1/2-sigma and |Y|<=W.

The strip gates do not need REG; the central gate does not need the scalar
threshold. These stronger dependency statements follow from the literal
polynomial. All premises of the requested Q2/Q3 conclusions are derived or
explicit original LM001 hypotheses; neither desired conclusion is a premise.

The first Lean artifact consists only of finite-dimensional polynomial
inequalities. ODE existence, selected unstable branch, flow transit/capture,
measurability, robustness, geometric Palm identification and P0.2 are not
conclusions of these gate theorems. The inherited closed paper status and
provider-distinct review history are preserved separately.

Verification is new-scope only. Failed development logs are retained. The
final receipt records source hashes and actual observed compile/kernel/axiom
and new control outcomes, without inventing intermediate source hashes.
