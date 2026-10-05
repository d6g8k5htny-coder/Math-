# Exact formal scope and alignment review

Scientific effect: NONE. The original pilot offers 13 scalar companion statements from recovered GP-FOR-192. Its original archive has SHA256 a6440511fc259706457b18227734013966251105d538fdeabe633bb73f168631 (10,644 bytes). The two recovered source modules are preserved byte-identically under originals/*.lean.txt. The separately named AlgebraV2 and ProbabilityCompanionsV2 execution successors apply only the three documented compiler repairs in COMPATIBILITY.md; their thirteen theorem statements are unchanged. Neither version is a transcription of the full research theorem. Original Status.lean and metadata are deliberately not imported: labels for EC-012, EC-013 and Theorem-B-Jacobian did not supply those theorems.

| Targets | Exact coverage | Not established |
|---|---|---|
| ec005_fold_gap | Canonical polynomial foldPotential gap for every real s | Random-field normal-form construction or persistence pairing |
| ec008_factor_expansion | Scalar polynomial factor identity in real c,s | Construction/positivity of the actual conditional covariance matrix |
| ec010_generic, ec010_transverse | Polynomial identities for arbitrary real parameters | Validity/coverage of the underlying geometric charts |
| ec011_scalar_cancellation | Commutative real scalar cancellation | An ODE, matrix adjoint transport or Hessian symmetry |
| ec014_contact_power | Scalar inverse-power cancellation for r nonzero | Six-pin determinant, change of variables or Kac–Rice density |
| p02_lm008_r2_cancel | Quotient cancellation when r,cZ are nonzero | A probabilistic conditioning argument |
| p02_lm008_cross_multiplied, p02_lm008_quotient_bound | Implications from supplied numerator and lower-normalizer bounds and displayed sign assumptions | Conditional Cauchy–Schwarz, moment estimates, existence or uniformity of the lower normalizer |
| p02_lm009_bad_event_threshold, p02_lm009_power40_identity | Deterministic threshold and exponent algebra | Markov/moment hypotheses or tail-event measurability |
| p02_lm009_r4_le_r3, p02_lm009_palm_r4_to_r3 | Polynomial comparison on 0 <= r <= 1 and conditional bound with C >= 0 | Existence of a uniform C, all-small-r stochastic theorem or parent closure |

GP214's upper bound Z_r <= 15 r^2 cannot discharge the required lower bound cZ r^2 <= z. None of these targets is the SIDE24 coefficient enclosure, the elder-rule selection theorem, or the joint extremum/merging-saddle law. Some algebraic assumptions are stronger than necessary; preserving them is intentional. Reducing them requires a separately scoped change, not silent strengthening of a parent theorem.

## Additive measure-theoretic bridge (seven new declarations)

This retained layer consists of 20 declarations: the original 13 above and seven in
`ResearchFormalCoreR1/MeasureBridge.lean`. The exact statement mapping and retained
hypotheses are in the hash-bound [bridge scope](MEASURE_BRIDGE.md).

| Targets | Exact coverage | Not established |
|---|---|---|
| p02_lm008_integral_cs | Bochner-integral Cauchy–Schwarz for nonnegative L² functions under one measure | Any concrete model moment estimate |
| p02_lm008_event_cs | Indicator specialization under one probability measure, with measurable event and nonnegative L² weight | Independence is neither assumed nor concluded |
| p02_lm008_event_numerator | Derives the r² numerator bound from the actual integral second-moment premise | Validity or uniformity of that premise in a field model |
| p02_lm008_measure_transfer | Bounds the same-law integral ratio using the explicit positive lower normalizer and second-moment premises | Construction of the reweighted/Palm probability measure or proof of its lower normalizer |
| p02_lm009_measure_transfer_r8_to_r3 | Transfers a supplied eighth-order event bound to a cubic ratio bound on 0 < r <= 1 | An event-tail theorem, uniform family of constants, P0.2 or parent closure |
| p02_lm008_sqrt_counterexample, p02_lm008_upper_normalizer_counterexample | Exact scalar witnesses excluding missing-square-root and reversed-normalizer mutations | Kernel construction of the finite probability-space realizations |

All new statements remain conditional at their displayed hypotheses. They do not
transfer historical reviews to new bytes. The original two modules, their proofs,
the gate and its five executable rejection controls remain unchanged. The two
new counterexamples are included in the normal target/axiom inventory. The changed
manifest and scope require a fresh separately authenticated alignment review.

## Additive weighted probability law (nine further declarations)

This retained layer has 29 theorem targets. [WEIGHTED_LAW.md](WEIGHTED_LAW.md)
is the hash-bound exact scope for the new `WeightedLaw.lean` module. It consumes
all earlier formal source unchanged and supplies the abstract PT1 construction
excluded by MeasureBridge: an integrable a.e.-nonnegative weight with positive
normalizer defines a probability measure, whose real mass on measurable events
is the same-law integral ratio. Null sets and a.e.-equal weights are respected;
zero and unit weights are checked. The two final declarations compose this
constructed measure with the existing conditional square-root and cubic bounds.

This construction does not identify a concrete Gaussian/typed Palm law or prove
its moment, lower-normalizer, event-tail, uniformity or persistence hypotheses.
The previous scope exclusions describe their respective modules; the abstract
construction alone is added here. The executable gate and five negative controls
are unchanged, and all nine new targets enter its transitive axiom inventory.
No existing review is silently rebound to the changed manifest or scope.

## Additive moment-to-tail composition (seven further declarations)

The current total is 36 theorem targets. [MOMENT_TAIL.md](MOMENT_TAIL.md) is the
hash-bound scope for `MomentTail.lean`: actual finite-measure Markov inequality,
strict-event measurability/threshold inclusion, the fortieth-moment-to-eighth-order
event tail, fourth-order and cubic weighted probability bounds, and an explicit
uniform-family assembly. The event is exactly {epsilon < r R^5}, not the entire
research good-event complement. Its moment bound, the weight's second moment,
positive lower normalizer and uniform-family premises remain assumptions.
No concrete Gaussian jet/Palm construction, derivative-supremum bound, P0.2 or
parent theorem is established. All earlier29 proof bytes, the executable gate
and its five rejection controls are unchanged. Existing package-level alignment
records do not automatically cover these new targets or changed scope.

## Review contract
The source manifest is an evidence sidecar, not another scientific register. A trusted successful workflow establishes kernel evidence only for these target declarations and their displayed hypotheses, relative to Lean's kernel/standard foundations/toolchain. Independent review must compare each Lean statement and definition to this scope note and the source actually cited. Review author, provider, family and agent must be explicit. Validate an authenticated record with `python formal/gate.py --alignment review.json`; then the existing controlling gate must decide whether its wider requirements are met. The validator does not authenticate a review merely because a JSON string names a reviewer.

The record contains disposition ACCEPTED, manifest_sha256, scope_sha256, exactly the targets, author/reviewer objects with provider/family/agent, and evidence repository/path/40-character commit/sha256. At publication, no independent alignment review is claimed. A fresh source, scope, toolchain or manifest digest stales the old review. Reject missing or ambiguous lineage, same provider/family/agent, stale digest, partial coverage, or non-ACCEPTED review.
