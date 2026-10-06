# Cap I4: clipped soft-eigenvalue integral

Dylan Roy — delegated AI work. Actual author OpenAI / GPT-6 Astra Pro,
`cap-i4-clipped-integral-20261006-r17`; pickup main#229/6016641184.
Scientific effect NONE; organizational-independence credit 0. No self-merge.

An isolated child of fb767a09b745fc80fc087c64b1f642e884c13148. This packet
changes neither R15 nor the active R16 depth-kernel branch. No production
formal/ source, theorem inventory, workflow, proof or scientific flag is edited.

## Six exact contracts

For a=min(T,L), the finite integral of x(x+b)(T-x) is computed exactly, with
nonnegativity and the upper bound T*(L^3/3+b*L^2/2) when T,L,b are nonnegative.
The full-chamber value is T^4/12+b*T^3/6. Substituting L=D*r*U^2 and b=E*r*U
and retaining A*r^2*T*U^3 proves the scalar r^5 envelope with U^9 and U^8.
The sixth statement connects the clipped nonnegative ENNReal integral on Ioc
to the exact real polynomial; finite-interval integrability is proved, not assumed.

The signed gap T-x is used only on [0,min(T,L)]. Enlarging that signed integrand
beyond T is invalid. The upper bound first discards its nonnegative subtraction
on the original interval and only then increases the polynomial endpoint.
Both soft factors remain. T=0,L=0,b=0 and r=0 are included. The scalar prefactor
result permits all r>=0; it does not by itself weaken the r<=1 hypothesis of a
separate determinant majorant. It proves neither a Gaussian integral nor a
uniform residual moment or probability bound.

The old CapI4.lean double_soft_integral/matrix_soft_integral (blob
4769930d132a485f88b75c4f4d901a3c4db7d43e at f4079f65) is credited prior work.
This new clipped identity is the retained-gap version needed between the moving
cutoff and the outer Gaussian envelope. P sections6–7, blob
dfed3b8d318a3ab1950957f393307733a4bef3f2, and its inverse-congruence erratum
213594d6ca6a86fb938110f4d166d9ce275a02d0 remain unchanged. The ordinary d3
moment-nine envelope already appears in PR313; no new moment-optimality claim.

## Execution boundary

The initial imports-only source at bc04723c produced actual run37467529583: the
stub compiled, then Contract.lean failed ONLY at its six absent declarations.
Original artifact11415057753 is retained. The current source supplies proof bodies
with the exact same Contract. A finished child requires its warnings-as-errors build,
exact Contract, all six axiom/type reports, fresh leanchecker, intended negative
controls and equal source-before/after records. Pending or failed runs are not PASS.
The factor/sign negative probes are scalar controls, not independent integral proofs.

The replay is a scoped adaptation of the previously executed R15 runner. It reuses
the exact parent evidence helper and pins source/toolchain/dependency identities,
but compiles ONLY this new module. No current-main core or old Cap kernel replay
is claimed. Trusted versioned source identities are not a cryptographic signature.

```sh
ROOT="$PWD"
(cd formal && lake env python3 -B -S "$ROOT/companions/cap_i4_clipped_integral_20261006/replay.py")
```

Lean4.34.1; mathlib d13f23b723b8a846827a245b89c10fc7d3f11612. Exact rational
and source controls run in normal/optimized Python. Their 96 signed polynomial,
100 clipped, and144 moving-prefactor cases supplement rather than replace the
Lean proof. Actual Gaussian density, original-law independence, concrete field
weight domination, outer integration/moments, geometric cap and full normalizer
still require their own source-model realization. Nonauthor alignment is separate.
