# Cap I4 — finite Gaussian outer envelope

Dylan Roy — delegated AI work. Actual author OpenAI / GPT-6 Astra Pro,
`cap-i4-gaussian-envelope-r18-20261006`; pickup main#229/6017183944.
Scientific effect NONE. Organizational-independence credit 0. No self-merge.

Six exact contracts formalize the OUTER finite-integrability step of the
already-known ordinary PR313 ninth-moment envelope, not a new asymptotic result.
For finite residual measure nu with integrable |j|^9, and c>0, the full positive
half-line product integral of (|j|+|T|)^9 T^2 exp(-cT^2) is finite and bounded by

    256 [ (integral |j|^9 dnu) G2(c) + nu.real(univ) G11(c) ],

where Gn(c)=integral_(0,infinity) |T|^n exp(-cT^2) dT. Actual Gaussian moment
integrability is proved using pinned mathlib, not supplied as an assumption.
The finite measure's mass stays explicit; probability specialization has mass 1.
The absolute-value extension covers arbitrary residual signs. Source J>=1 can
specialize this without falsely deducing support from a probability hypothesis.
The two Gaussian constants are genuine finite integrals, NOT Bochner-totalized
infinite integrals. Their classical closed forms are not new Lean declarations.
A nonnegative-integral bound is included only after integrability is established.

The signed Vandermonde belongs to R17's clipped interval; it is not extended
past T here. No eigenvalue-independence, typing-conditioned independence,
Cauchy-Schwarz, hard-eigenvalue cutoff, r power, weight or normalization change.
Joining R16/R17's domains/prefactors to this envelope and instantiating Gaussian
field density/regression/derivative bounds, uniform moments, geometry/E4 and full
normalizer remain distinct obligations. Ninth-moment sufficiency is not optimality.

Parent cut189f4efe86414a94082e612f20d2b8986a1949d8 stays unchanged. This new
module imports mathlib only; old Cap modules are not recompiled by this replay.
P sections6-7 blobdfed3b8d and erratum213594d6 remain source context.
Pinned Lean4.34.1/mathlibd13f23b723b8a846827a245b89c10fc7d3f11612.
GaussianIntegral.lean blob13927ae74e7ce60a2d053df06eacec80b3f924a0;
Integral/Prod.lean blob7484a64e40beacdd472da61f858f02c8ffb62863.

Initial source is deliberately imports-only. Contract applications must fail on
six missing names before implementation. A successful full hosted run requires
warning-as-error compilation, exact Contract, six type/axiom reports, fresh
leanchecker, both scalar rejection controls and unchanged before/after sources.
Earlier failed runs stay failed; actual outcomes belong in the exact-head thread.
The inherited replay helper is reused at its exact source pin. Its factor/control
checks are sanity tests, not proofs of moment integrability. Source tests are
finite exact rational checks, not a continuum Gaussian or field calculation.

Reproduce with the existing pinned toolchain in a complete checkout:

```sh
ROOT="$PWD"
(cd formal && lake env python3 -B -S "$ROOT/companions/cap_i4_gaussian_envelope_20261006/replay.py")
```

This branch is outside the integration queue. Nonauthor source alignment,
current-base integration and scientific acceptance are separate from execution.
