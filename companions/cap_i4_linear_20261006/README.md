# Cap I4: two linear-volume interfaces

Author: OpenAI / GPT-6 Astra Pro, `cap-i4-linear-volume-20261006`, delegated by Dylan Roy.
Scientific effect NONE. Author/source-exposed work; organizational independence credit 0.
Pickup: main#229 comment 6008077621.

This additive companion is a child of angular head
`778805dbe6635f82488098b478739a0ed4026130`; it changes neither that branch nor
its polar parent `035e14017267fe15276fdccf1758618ca7f96b45`. No production
`formal/` source, manifest, scientific register or existing workflow is edited.

## Exact scope

Two definitions and twelve theorems concern actual product Lebesgue measure on
R x R. `tracePair(a,d)=((a+d)/2,(a-d)/2)` has determinant -1/2 and maps volume
to twice volume. `spectralPair(t,rho)=(t-rho,t+rho)` has determinant 2 and maps
volume to half volume. The proof uses the pinned Haar linear-map theorem, not
an assumed change-of-variables conclusion.

These maps are NOT mutual inverses with the source's traceless sign convention:
`tracePair(spectralPair(t,rho))=(t,-rho)` and
`spectralPair(tracePair(a,d))=(d,a)`. The determinant and inverse-volume factors
are nevertheless correct. Explicit tests reject the false identity convention.

The positive-domain theorem transforms exactly `0<rho<t` to `0<lambda<Lambda`.
The weighted theorem retains BOTH the inverse Jacobian 1/2 and
`rho=(Lambda-lambda)/2`, hence its coefficient is 1/4. Measurability of the
nonnegative test G is explicit; infinite integrals are allowed. No positive
floor for the larger eigenvalue or inverse-eigenvalue moment is used.

This is NOT a completed three-entry matrix spectral pushforward. Product
reassociation between `(a,(b,d))`, `((a,d),b)` and the trace/traceless plane,
Tonelli/Fubini assembly with the angular theorem, and resulting matrix-density
comparison remain separate tasks. No matrix-library identification, actual
Gaussian law, residual independence, uniform moment, determinant-tilt,
geometric-event or full-normalizer instantiation is supplied. The unchanged
CapI4 consumer and the ordinary moment8/9 results do not become new Lean facts.

## Source binding

P: `imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md`,
blob `dfed3b8d318a3ab1950957f393307733a4bef3f2`; read with its inverse-congruence
erratum blob `213594d6ca6a86fb938110f4d166d9ce275a02d0`.
Ordinary spectral derivation: PR313 PROOF blob
`c30e3f5ff600b058a30087ff794c7cf304e4aafc` at reviewed head
`8e90773b28ecce66ed30458d58aef1b6cb83666a`. Its review is not a review of this
new module. The parent angular/polar source and reviews remain frozen.

Lean toolchain: `leanprover/lean4:v4.34.1`; mathlib
`d13f23b723b8a846827a245b89c10fc7d3f11612`.
The actual imported linear-map scaling theorem is
`map_linearMap_addHaar_eq_smul_addHaar` in
`Mathlib/MeasureTheory/Measure/Lebesgue/EqHaar.lean`, blob
`58e8db04a65a8f78caaa702d66a5ebab016edb0b`.
Map-integral rules are from `Integral/Lebesgue/Map.lean`, blob
`10de8856a750888634152dddf232848a299061d4`.

## Reproduction and limits

From the complete repository with pinned dependencies installed:

```sh
ROOT="$PWD"
(cd formal && lake env python3 -B -S "$ROOT/companions/cap_i4_linear_20261006/replay.py")
```

The source and evidence suites run in both normal and optimized Python modes.
The module and exact-type contract are compiled with warnings as errors, all
14 declared types and axiom reports are inventoried, fresh leanchecker is run,
and two concrete false statements must fail with their intended False goal.
Before/after source, workflow and dependency identities must match. Evidence
is not reused: an existing output directory causes failure. The process log
records completed child executions; on timeout partial output is retained and
the overall run fails, but no completed process receipt is manufactured.

`SOURCES.json` is a trusted versioned identity manifest, not a signature or an
independent proof. Type-log parsing validates names and diagnostics; the critical
exact propositions are checked by `Contract.lean`, not by a text grammar.
Only the new module is built here; no fresh 63-target core replay is claimed.
A separate nonauthor source-alignment read and actual successful hosted evidence
are required. Local finite/source/parser tests are not kernel verification.
