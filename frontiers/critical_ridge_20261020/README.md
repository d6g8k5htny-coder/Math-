# Actual negative partial-gradient ridge (C299)

This finite formal unit constructs one local correction `r : E d → V` from the literal `Lifetime.IsSmooth`, criticality at `p`, and strict negativity of the literal Hessian on every nonzero vector of the actual submodule `V`. The selected function has value zero and C2 regularity at zero; on one common neighborhood, the derivative of `f` at `p+w+r(w)` vanishes on every vector of V; its derivative satisfies `H(w+Dr(0)w,z)=0`.

The parameter w is ambient. Restriction to a positive complement is later work; no orthogonality premise, supplied ridge, inverse certificate, Morse chart, desired local path connectivity or finite event list is an input. The zero subspace is included.

The source uses the actual restricted Hessian block, proves its invertibility by strict negativity and finite-dimensional Riesz duality, and applies pinned Mathlib's smooth product implicit-function theorem. C293's literal-Hessian identity is consumed unchanged.

Development status at first publication: source review performed, native import attempt retained, hosted elaboration and final formal verification pending. An execution report must bind the actual revision; this document does not claim compilation or theorem acceptance.

## Provenance and verification boundaries

Upstream sources are byte-identical to Math- commit `7af365e8c8db1ae0275d4efe08a70a678f153ca2`, paths `frontiers/critical_level_attainment_20261020/final-project/{Lifetime,TorusTopology,MorseFiniteCritical}.lean`. The source manifest binds all five modules and two intentionally ill-typed controls. Lean4.34.1 and Mathlib `d13f23b723b8a846827a245b89c10fc7d3f11612` are pinned by the existing formal environment.

The dedicated workflow builds all five local modules into an empty output directory, standard-kernel checks the four non-Lifetime modules, and audits every declaration originating in all four proof/input modules, including private/generated constants. The audit module itself is built and kernel checked, but is not a fifth imported-origin census. Permitted axioms are only propext, Classical.choice, Quot.sound. The nine new public declarations are required targets within the complete census, not its denominator. The complete target list also includes four consumed source interfaces.

Two omitted-premise controls target criticality and negative definiteness. A source-bound expected type-mismatch diagnostic is required; syntax/import/resource failures do not count. Initial diagnostic qualification remains pending until real compiler output is reviewed. Standard named-module checks do not replay or rebuild the entire imported Mathlib closure. Existing dependency objects may be cached; every local proof/input object in this workflow is freshly built. Tests and model agreement do not establish scientific acceptance.

Actual principal: Dylan Roy. Actual source author: OpenAI Codex delegated agent `/root/adapter_feasibility_c292`; coordinator and delivery executor: `/root`, chat `01a0bbb5-2fcb-77f0-b78b-4d220ddd7ab2`; verification engineering author: `/root/c297_hosted_verifier`; fresh source-exposed nonauthor reviewer: `/root/c299_nonauthor_review`. Same provider, organizational independence0, blind0, human0. No human review by Dylan is claimed. Scientific effect NONE.

## Remaining work

Reduced-Hessian positivity, uniform signs and fiber concavity, actual tube paths, a cofinal path-connected neighborhood basis, Euclidean all-point assembly, actual quotient-superlevel transport, and C294's hclosedLPC discharge remain OPEN. Actual finite ordinary bars, elder pairing versus adjacency, once-counting, field-first sampling, all-small-bars converses and regional shrinking collisions remain separate OPEN obligations. A global factorial bound does not settle the regional collision node.

Canonical coordination: Math- PR487 comment6292314595; R17 cooperative claim6e894b1f-d783-4ea0-adae-597e116b239a. Historical sources and other agents' claims remain unchanged. No merge, Ready transition or scientific promotion is part of this delivery.

Governing onboarding sources read for this delivery: [15 October owner mandate](https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OWNER_MANDATE_20261015.md) and [standing delegation](https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OP-AUTONOMY-20260923-v2.1.md). The current scoped instructions and explicit stops still control. Linking these records establishes availability, not a future recipient's acknowledgement.

Source custody update before hosted execution: the source author's additive correction [6292292150](https://github.com/d6g8k5htny-coder/Math-/pull/487#issuecomment-6292292150) now supplies the literal reviewed6961-byte proposal, including both terminal LFs. Its raw bytes match SHA25696a13c7e14e781220915e927caa34ba9ca94e26bd12bb7d53e7459b759c9b141. The original shorter payload and explicit reconstruction history remain preserved; the mathematical version did not change.
