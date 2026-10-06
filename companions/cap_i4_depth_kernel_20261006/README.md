# Cap I4: explicit moving depth kernel

Dylan Roy — delegated AI work. Actual author OpenAI / GPT-6 Astra Pro,
`cap-i4-depth-kernel-r16-20261006`, pickup main#229/6016138034.
Scientific effect NONE; author/source-exposed; organizational independence credit0.
Isolated child of fb767a09b745fc80fc087c64b1f642e884c13148. No parent or formal/ edit.

One definition and five theorem contracts specialize the R15 transport to the
actual m=2 determinant-product algebra from P(6.2), blobdfed3b8d318a3ab1950957f393307733a4bef3f2.
The explicit kernel has D=4K^2/(3k_min), E=3K/2, A=K^2(1+K)/4, U=j+Lambda:

    1{lambda <= D r U^2} ofReal[A r^2 Lambda U^3 lambda(lambda+E r U)].

Both soft factors, the hard Lambda factor and equality at the depth threshold
are retained. Measurability is proved for all real parameter values. The
pointwise estimates require 0<=r<=1, K>=0, k>=k_min>0, nonnegative h,j and
h<=K(j+Lambda) on positive-weight support. The final statement DOES NOT require
positive matrices under the entire original Gaussian law: its deterministic
premises are conditional on w>0, almost everywhere. Nonpositive real w is
handled by ofReal, not interpreted as a negative probability weight.

The source observable remains to be instantiated, including measurable
nonnegative weights and the actual Hessian determinant inequality. The theorem
then concludes an extended nonnegative integral inequality with the exact
pi/gap factor, under original-law independence and the matrix marginal density.
It does not evaluate the moving spectral integral, prove residual support or
moments, divide by a normalizer, prove cap geometry, or establish full Cap I4.
No Cauchy-Schwarz replacement or independence after typing is used. Scope is d=3.

## Reproduction

From the complete repository with its pinned Lean/mathlib dependencies:

    ROOT="$PWD"
    (cd formal && lake env python3 -B -S "$ROOT/companions/cap_i4_depth_kernel_20261006/replay.py")

The runner is a scoped adaptation of R15 replay5fa273cd30b118fae29115b12ae7c2ebb37c8db1,
not a new evidence framework. It compiles seven exact parents, the child and
six exact-use contracts; inventories the definition plus five theorem types
and axioms; executes fresh leanchecker, two inherited scalar/sign false-goal
controls, and before/after source checks. Old output is rejected, failures
retained. Eight finite/source tests per mode include 864 rational determinant
comparisons and counterexamples to omitting radius/derivative/mark hypotheses.
Those tests are not continuum, Gaussian or kernel evidence.

The first child was imports-only. Actual run37463555390 compiled all seven
parents and the stub, then the exact Contract failed with nine unknown-name
diagnostics: four occurrences of depthKernel and the five missing theorem names.
There were no other compiler diagnostics. Original artifact11413193585 is retained.
Implementation follows that observed failure and preserves Contract.lean exactly.
An actual complete successful hosted successor is still required before any
kernel-success claim; later execution outcomes belong in the exact-head work
record. Separate nonauthor alignment of this child and unreturned parent
alignment requests are not transferred or declared completed by CI.
