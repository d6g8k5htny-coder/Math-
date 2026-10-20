# Source identity and mathematical scope

This document describes the current C297 source candidates and their dependency
boundary. As of the 2026-10-20 11:42:05 UTC report, Claude S's Linux execution
passed compilation and standard named-module kernel replay for topology candidate
3. The literal consumer's compilation and kernel verification, complete axiom
audit, executed interface controls, combined packet verification, and final
acceptance remain pending. Source identities and preliminary source review do not
substitute for those outstanding outcomes.

The library pin is Mathlib
`d13f23b723b8a846827a245b89c10fc7d3f11612`, with Lean 4.34.1.
The project input `Lifetime.lean` supplies the literal Euclidean space,
smoothness, and criticality definitions. The separately owned C296 source
supplies the regular scalar chart.

| Source | Bytes | SHA-256 |
|---|---:|---|
| `Lifetime.lean` | 51,383 | `90f4892608e953ecc696bb32ea159d1c178ceb8a1c6edfd11acfceb14af462c6` |
| C296 `RegularPointChart.lean` | 2,767 | `5568c8d6e03f7064cd5924ebe2814ae746100505ae31789d5c975902528f9fa2` |
| C297 `RegularSuperlevel.lean`, candidate 3 | 6,405 | `0db6ce3ea7358a59c089680d774a6806f0fb747c24d9828850377458156e2f02` |
| C297 `RegularSuperlevelLiteral.lean` | 2,299 | `334759063a3ae58b42b8cd4a45e3bfd6f3a31b668d18526aa6fdcb5ea65c13d3` |

The C296 dependency is fixed to
[commit `72edcf5b93be45c29f2d10a26f7d8e861a48f528`](https://github.com/d6g8k5htny-coder/Math-/blob/72edcf5b93be45c29f2d10a26f7d8e861a48f528/frontiers/regular_point_chart_20261020/RegularPointChart.lean),
released by its Research Task Watch owner. Its chart source is byte-identical to
the earlier interface copy used while preparing the consumer. C297 consumes the
released source with attribution; it does not take ownership of the chart,
its branch, or its tests.

The local mathematical objects are unchanged:

```lean
E d = EuclideanSpace ℝ (Fin d)
IsSmooth d g = ∀ n : ℕ, ContDiff ℝ n g
IsCriticalPoint d g x = (fderiv ℝ g x = 0)
```

The dimension is any `d : ℕ`; the level is any `a : ℝ`.
Each point is explicitly a member of the actual closed-superlevel subtype
`{y : E d // a ≤ g y}`. The local Euclidean statements require no period, random
field, coefficient field, or limiting operation. This absence does not supply
any quotient or stochastic theorem.

There are six explicit declarations in the topology layer, all in namespace
`TorusRegularSuperlevel`:

| Declaration | Exact role and boundary |
|---|---|
| `path_connected_basis_of_openEmbedding` | Transfers the domain's path-connected neighborhood basis to the image of a point under an open embedding. It does not conclude global LPC of the codomain. |
| `path_connected_basis_of_open` | Transfers a basis from an LPC open neighborhood to its point in the ambient space. |
| `relative_chart_homeomorph` | Defines the homeomorphism between `{y : S // y.val ∈ p.source}` and `{z : T // z.val ∈ p.target}`, assuming membership equivalence on the chart source. |
| `path_connected_basis_of_relative_chart` | Derives the basis in `S` at a point in the chart source, using LPC of the corresponding model subset `T`. |
| `closed_superlevel_basis_of_chart` | Supplies the preceding helper with the convex halfspace `{z : ℝ × F | a ≤ z.fst}` and proves its LPC. It requires the actual chart, source membership, and first-coordinate identity on the source. |
| `closed_superlevel_interior_basis` | Derives the basis at a point strictly above the level from `Continuous g` alone. |

The generic chart theorem allows any real normed-space model factor `F`.
Completeness or finite dimensionality of `F` is not an additional topology
hypothesis. The literal consumer instantiates it with
`F = (fderiv ℝ g x.val).ker`.

The two literal declarations are:

```lean
theorem closed_superlevel_regular_basis
    {d : ℕ} {g : E d → ℝ}
    (hsmooth : IsSmooth d g)
    (a : ℝ) (x : {y : E d // a ≤ g y})
    (hregular : ¬ IsCriticalPoint d g x.val) :
    (𝓝 x).HasBasis
      (fun V : Set {y : E d // a ≤ g y} =>
        V ∈ 𝓝 x ∧ IsPathConnected V) id

theorem closed_superlevel_path_connected_basis
    {d : ℕ} {g : E d → ℝ}
    (hsmooth : IsSmooth d g)
    (a : ℝ) (x : {y : E d // a ≤ g y})
    (hx : a < g x.val ∨ ¬ IsCriticalPoint d g x.val) :
    (𝓝 x).HasBasis
      (fun V : Set {y : E d // a ≤ g y} =>
        V ∈ 𝓝 x ∧ IsPathConnected V) id
```

These are the source interfaces awaiting completed verification. Neither accepts
a desired path, a supplied chart, a finite event list, or LPC of the closed
superlevel as a public premise. The regular branch obtains the chart from C296's
`regularPointChart`, source membership from `mem_regularPointChart_source`,
and the coordinate identity from `regularPointChart_fst`. The interior branch
uses the continuous strict superlevel as an open neighborhood.

The final neighborhood filter in every closed-superlevel conclusion is on the
subtype. The intermediate chart intersections are open relative to their source
and target subsets. Ambient openness of a closed halfspace is never required.
Chart inverse transport is restricted to its actual target.

The following distinctions remain necessary when interpreting evidence:

- The observed native candidate-1 run reached its 600-second bound with no
  diagnostic or object; process sampling showed import reading.
- [Claude S's candidate-1 execution](https://github.com/d6g8k5htny-coder/Math-/pull/487#issuecomment-6289663934)
  reached elaboration and failed after 48 seconds. The author corrected the
  basis witness construction, explicit subtype membership, and style warnings.
- [Claude S's candidate-2 execution](https://github.com/d6g8k5htny-coder/Math-/pull/487#issuecomment-6289854822)
  failed after 47 seconds on the restricted identity map's inferred source and
  topology. Candidate 3 makes those types explicit.
- The [candidate-3 execution request](https://github.com/d6g8k5htny-coder/Math-/pull/487#issuecomment-6290009856)
  was followed by the [actual Linux result](https://github.com/d6g8k5htny-coder/Math-/pull/487#issuecomment-6290047895):
  topology build return code 0 under warnings-as-errors in 12.5 seconds, then
  standard `leanchecker -v RegularSuperlevel` return code 0 in 10.0 seconds.
  The exact 6,405-byte source with SHA-256
  `0db6ce3ea7358a59c089680d774a6806f0fb747c24d9828850377458156e2f02`
  remained unchanged. The executor was Anthropic Claude, session
  `session_01S16677s1SGeAJmN3QMz4ip` (Claude S). This was execution-only evidence
  for the six-declaration topology module, with no `--fresh` replay, literal
  consumer execution, complete axiom census, negative-control execution, or
  mathematical review. The C297 author read the report and did not run those
  Linux phases.
- Preliminary OpenAI nonauthor source review is same-provider and source-exposed,
  with organizational independence 0 and human review 0. It is not final
  acceptance or a kernel result.
- The two deliberately incomplete theorem invocations are interface controls.
  Their intended missing-premise errors must be distinguished from unrelated
  syntax, import, or resource failures.
- The smooth oscillatory example discussed in the README is a paper-only
  non-Morse control. It is not a formal counterexample or a counterexample to
  the smooth Morse target.

The remaining mathematical obligations include critical-boundary Morse geometry,
transport through the actual torus quotient, and LPC of the entire closed
critical-death superlevel. A per-point result restricted to regular or interior
points does not discharge those obligations. Strict death drop, the full
ordinary-H0 finite-bar adapter, the all-small-bars converse, regional shrinking
collisions, exhaustive once-counted bars, and actual elder pairing also remain
open. No branch-adjacency or local trap assertion is promoted to a pairing.

The stochastic field, probability assumptions, numerical constants, density
normalizers, and orders of limits are unchanged. Scientific effect is NONE.
The source author is OpenAI Codex `/root/adapter_feasibility_c292`, coordinated
by OpenAI Codex `/root` for Dylan Roy. The separately attributed C296 owner and
Claude S executor retain their respective roles. Dylan Roy's personal reading
is pending.
