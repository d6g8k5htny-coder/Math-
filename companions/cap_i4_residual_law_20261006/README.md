# Cap I4 residual-law support and ninth-moment adapter

Dylan Roy — delegated AI work. Actual OpenAI / GPT-6 Astra Pro,
cap-i4-residual-law-r22-20261006; pickup main#229/6020693661.
Prior Cap author/reviewer exposure; organizational credit0, scientific effect NONE.

Isolated child of R20 76e307707e8fc37d4264210da86915e6ba0be81a. Only this
five-file companion and one new read-only workflow are added. R21's chamber
owner and every parent source, primary formal package and integration slot are
unchanged. No author self-merge or scientific acceptance is requested.

## Exact contract

Four statements transport from a measurable source random variable J to its
ACTUAL marginal Q.map J: Q-almost-everywhere J>=1 implies marginal support;
absolute ninth-moment integrability is equivalent; the finite ninth moments
are equal; hence the original support, integrability and upper bound M supply
the corresponding three outer-envelope inputs with the SAME M.

These are wrappers around the pinned measure-map and Bochner integral theorems,
not new probability laws or new Gaussian moment estimates. Measurability of J
is explicit. The exact integral equality requires source integrability so it
is not advertised as a finite-moment conclusion from a totalized integral.
The measure Q need not be normalized. Probability or finite-measure instances
are supplied by the actual source application, not proved by these wrappers.
R15's already-proved mass1 and joint-law results are not duplicated.

The source J>=1 and finite ninth moment remain INPUTS. No mean-only inference,
normalization of an arbitrary measure, clipping/redefinition of J, field
regression construction, uniform-family estimate, independence, moving-kernel
integration, E4 or full normalizer is supplied. R18/R20 still require their
other exact hypotheses. R21's measure rearrangement stays separately owned.

Pinned mathlib d13f23b723b8a846827a245b89c10fc7d3f11612 APIs inspected:
Measure/Map.lean: ae_map_iff; Function/L1Space/Integrable.lean:
integrable_map_measure; Integral/Bochner/Basic.lean: integral_map.
The project Lean4.34.1/toolchain/dependency manifest are unchanged.

## Execution

Initial source contains imports only. Contract.lean has four exact applications;
a real missing-declaration failure is required before implementation. The five
finite/source controls allow that stub so the kernel contract is the decisive
missing-implementation test. Finite atomic examples are not Gaussian simulation.

Run from a complete checkout with pinned dependencies installed:

```sh
ROOT="$PWD"
(cd formal && lake env python3 -B -S "$ROOT/companions/cap_i4_residual_law_20261006/replay.py")
```

The bounded runner follows the existing Cap process/source-binding pattern and
reuses the exact inherited axiom/negative validators. It compiles only this
mathlib-based child, its unchanged contract, four type/axiom reports and fresh
leanchecker; it does NOT rerun the older Cap chain. Its two false arithmetic
examples check rejection plumbing, not measure transport independently. Failure
and timeout output remain failure evidence; an existing output directory fails.
A completed hosted run and a separate source-alignment review remain distinct.
The author's local runtime was unavailable at preparation: no local tests or
local Lean execution are claimed. Observed hosted results belong to their exact
run/head, not to a later branch or current-main integration candidate.
