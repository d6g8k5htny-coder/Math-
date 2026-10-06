# Cap I4: original-law independence adapter

Dylan Roy — delegated AI work. Author OpenAI / GPT-6 Astra Pro,
`cap-i4-independence-r15-20261006`; pickup main#229/6015381342.
Scientific effect NONE; organizational-independence credit0.
Isolated child of 64d3b9294e8d9c612db646a33815248bf05089f5.

Three exact contracts: (1) derive the joint-product law from actual mathlib
IndepFun under the original probability measure and the specified matrix
marginal density; (2) the residual pushforward has mass one; (3) obtain R14's
spectral integral bound for an almost-everywhere, rather than everywhere,
dominated nonnegative weight. The caller does not supply the final joint-law
identity or an extra SFinite density premise: the latter follows from the
matrix marginal being a pushforward of the probability law.

The original-law independence and the marginal density are still real hypotheses.
This does NOT construct Gaussian regression, infer independence from marginals,
or preserve independence after conditioning on typing. It does not identify the
field derivative norm, moving boundary, determinant bound, moments, cap geometry,
or full normalizer. No Cauchy–Schwarz replacement and no additional normalization.
The RHS retains pi, the eigenvalue gap and the nonseparable residual/eigenvalue
kernel. A general nonmeasurable W is interpreted only through its nonnegative
lintegral; to read it as an expectation, use the source's measurable actual weight.

Parent R14 source d659b0ae3416990fbf976ca1a1bc2dedaccc6541 is unchanged;
its successful run37452674632 and alignment request6014703547 are separate.
Earlier spectral source cf60892c9233352ae861d8dacc7ab1d591014980 and alignment
request6009704131 are likewise not promoted by this wrapper.
The exact mathlib pin is d13f23b723b8a846827a245b89c10fc7d3f11612:
Probability/Independence/Basic.lean blob3f348954b4478a5a81be29aaff1bb761d4eb197b,
indepFun_iff_map_prod_eq_prod_map_map and IndepFun.map_prod_eq_prod_map_map.
Source law applicability still comes from P(3.5),(4.2)-(4.3), not this code.

The initial Lean module is an imports-only stub, deliberately failing the three
exact Contract applications. No passing kernel execution is claimed by this
README; actual frozen-head outcomes and original failures belong in the hub.
Run in a complete pinned checkout:

```sh
ROOT="$PWD"
(cd formal && lake env python3 -B -S "$ROOT/companions/cap_i4_independent_20261006/replay.py")
```

The runner is a minimal adaptation of exact R14 replay blob48cf4db7bee9309f95b9cf89abe160cb57d8cede.
It checks six exact parents, current child/workflow, nine dependencies and tested
head/run/attempt. It compiles seven modules and exact Contract with warnings as
errors, inventories three axiom/type reports, fresh-checks CapI4Independent,
requires two inherited scalar/sign False controls and compares before/after
source records. Those controls do not prove probabilistic independence. Existing
formal/ bytes and manifests remain untouched; no current-main aggregate receipt
or independent-human alignment is claimed. Native source review and eligible
future integration remain separate. No author self-merge.
