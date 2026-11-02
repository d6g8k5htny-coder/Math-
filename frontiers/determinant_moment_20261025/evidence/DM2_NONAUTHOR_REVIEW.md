# DM2 nonauthor source and statement review

Signed: OpenAI / GPT-6-Codex family / agent `/root/dm2_statement_review`,
2026-10-25. Exact underlying model identifier is unavailable to this reviewer.
Author reviewed: OpenAI/Codex `/root`. This is a separate reviewer context,
same provider, original proof visible. Organizational-independence credit 0;
acceptance credit 0; scientific effect NONE. No machine ACCEPTED alignment
record is supplied.

## Exact reviewed identity

Repository `d6g8k5htny-coder/Math-`, frozen commit
`deb28a751f620715ec65d3bd73690905e6fee94d`.
All paths below are relative to `frontiers/determinant_moment_20261025/`.

| File | SHA256 |
|---|---|
| ResearchFormalCoreR1/DeterminantMoment.lean | c12731c88cd7c7dee32b2cb59b3a4eb5016f2b59a96e3cda4b523632a0bf61c4 |
| SOURCE_MAP.md | 1d21d9d283047a2bbaceec402e2af0009b2b53e3eb3c4fa47654b73bc748460e |
| SCOPE.md | 7d8c3205bf1d382cb069aec38b7754a44af540e411762507e889eb61239ead4e |
| manifest.json | fb0aac53dac710c4f03ae599aabc4b0955395e4a4bad047bd126595cc956d436 |
| controls/false_omit_q.lean.txt | cbcd846199ff2f48099bc33518188ddfcd3667f9e7a9ef932a2627e69b540a46 |
| controls/false_r6.lean.txt | c0ce4598ff5e188475e0ec9d0eeb3c3465169583a457baec90625d7b0f3a8439 |

The actual public source inspected is
`imports/hardening_ebedb780/P02-LM-002/proof.md.export.txt` at base
`c4eabc1a917ba2c1b96fe4af425cf2a484877c03`, Git blob
`d1fd7eccd5947cb6c5bf8724a77b7ec1c380a29b`, SHA256
`0f8f80922feb603e5b6e530eb885a7819b3a98d90d3c42d60a68259af766f7de`.
Both the base blob and working source hash were checked. Its claims about
historical reviews remain source claims. GP-DER-071 and CL-AUD-052 themselves
were not inspected. The original public proof and proposed implementation
were visible; this is source-aware review, not clean-room reconstruction.

## Findings

No substantive mathematical source mismatch was found in the five new DM2
declarations and their definitions. The final source was reread after the
compiler repairs; their noncomputable annotations, classical decidability,
algebra normalization and explicit measurable-set arguments preserve the
mathematical contract reviewed initially.

`DM2Jet` has nine real coordinates in the declared order. `dm2Radius` includes
all nine absolute values plus one, including the unused z,c13,c04 coordinates.
Both Hessians match section 2 exactly: the +/-r and +/-ar/2 signs, the
rw/2 signs, and the 12 and 8 denominators all agree.

`dm2Negative` is strict quadratic-form negativity at every nonzero real
two-vector. Applied to the symmetric HM it is the source condition. The
conjunction with strict det HS < 0 implements both indicators; singular and
type-boundary cases need no exclusion or null-set assumption.

`dm2_untyped` proves the stronger determinant-product square estimate before
indicator restriction. Its factorization and coefficient bounds follow the
source algebra. `dm2_pointwise` has exactly arbitrary real jets and 0 < r <= 1,
with no Gaussianity, independence, type, or nonsingularity premise.

`dm2_negative_iff` is the correct symmetric two-dimensional Sylvester
criterion. Its forward direction tests (1,0) and (-b,a); the converse uses
a times the quadratic form as the sum of the two displayed nonnegative
squares, with strict positivity for a nonzero vector. The measurable-weight
proof uses continuous polynomial strict inequalities and works for every
real r, without a type-boundary measure premise.

`dm2_moment` assumes a measurable jet map, actual integrability of R^8 and
its integral bounded by M8. It derives squared-weight integrability and
integral <= 16 M8 r^4 by domination. It does not assume its desired second
moment. The arbitrary-measure generality is sound and stronger than the
source probability-law implication. No explicit M8 >= 0 premise is needed:
it follows from the nonnegative integrand and the supplied integral bound.
The source uniform-family statement follows by applying this theorem to each
law with the same M8; a concrete uniform M8 is not established here.

The final declaration-level SCOPE accurately states these boundaries and
resolves the initial short-scope documentation limitation. The source map's
parent exclusions agree with formal/MOMENT_TAIL.md and MeasureBridge's
remaining premises. Concrete field-jet identification, uniform moment bounds,
normalizer floor, same typed Palm identification, full good-event coverage,
GT5, P0.2, lifetime and persistence remain open. No full parent composition
or baseline-target alignment is certified by this review.

## False mutation checks

Both fixtures state genuinely false inequalities, established here by exact
hand substitution, independently of any compiler-failure report.

For false_omit_q, r=1/2 and q=-100 with other coordinates zero give
det HM=50, det HS=-50, and LHS=6,250,000. The mutated RHS is 1. The actual
radius is 101. Thus omission of q destroys the proposed bound.

For false_r6, r=1/128 and q=-1 with other coordinates zero give R=2,
det HM=r and det HS=-r. The LHS is r^4=2^-28 and mutated RHS
16 r^6 2^8=2^-30, so the LHS is four times the RHS. In both controls HM is
negative definite and det HS is negative; the same witnesses also refute
the corresponding typed-weight mutations. These fixtures directly state
counterexample inequalities rather than universal mutated theorem statements.

## Gate and review boundary

The retained gate SHA256 is
`25e08d9054b929dd657668e4ee4a3524688dc476e5af958f950de3b919f04e9a`,
equal to formal/gate.py at the cited base. Its provider-distinct alignment
validator remains unchanged. OpenAI author and OpenAI reviewer fail that
identity condition, regardless of separate agent contexts. The later owner
loosening allows truthful same-provider review labels; it does not make this
review pass the unchanged executable validator. The review is limited to the
five new DM2 declarations, source mapping, explicit scope and two mutations;
it is not full 18-target baseline alignment.

Compiler success was reported by the author during the final revalidation
request. This reviewer did not execute or audit the build, leanchecker,
transitive axiom inventory, rejection-control runs or hosted checks. Their
actual execution evidence must be assessed separately. No execution success
or independent acceptance is inferred from source inspection or hashes.

Read-only review of production files; this evidence note is the reviewer's
only authored repository addition.
