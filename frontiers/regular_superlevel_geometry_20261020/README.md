# Regular-point geometry of closed superlevels

This packet develops the local topology needed to connect scalar regular-point
charts to closed-superlevel path attainment. Its intended result is a
path-connected neighborhood basis at a prescribed point of the actual closed
superlevel, when that point is regular or lies strictly above the level.

**Status as of the 2026-10-20 11:42:05 UTC execution report: topology candidate 3
passed its Linux build and standard named-module kernel replay.**
This covers the six-declaration `RegularSuperlevel` module. Compilation and kernel
verification of the literal consumer, the complete axiom census, both negative
controls, and combined packet verification remain pending. Scientific effect
remains **NONE**.

For a natural dimension `d`, the literal source is
`E d = EuclideanSpace ℝ (Fin d)`. Given `g : E d → ℝ` and `a : ℝ`, let
`S = {y : E d // a ≤ g y}`. The two public declarations in
`RegularSuperlevelLiteral.lean`, in namespace `TorusRegularSuperlevel`, have the
following scope:

| Declaration | Assumptions at `x : S` | Intended conclusion |
|---|---|---|
| `closed_superlevel_regular_basis` | `IsSmooth d g` and `¬ IsCriticalPoint d g x.val` | The neighborhood filter of `x` in `S` has a basis of path-connected sets. |
| `closed_superlevel_path_connected_basis` | `IsSmooth d g` and `a < g x.val ∨ ¬ IsCriticalPoint d g x.val` | The same pointwise neighborhood basis. |

Here `IsSmooth d g` means `∀ n : ℕ, ContDiff ℝ n g`, and literal criticality
means `fderiv ℝ g x.val = 0`. The public statements assume neither a chart nor
local path connectivity of the closed superlevel. The separate
`closed_superlevel_interior_basis` theorem needs only `Continuous g` and
`a < g x.val`; it includes critical points strictly above the level.

The exact conclusion is

```lean
(𝓝 x).HasBasis
  (fun V : Set {y : E d // a ≤ g y} =>
    V ∈ 𝓝 x ∧ IsPathConnected V)
  id
```

The filter is on the closed-superlevel subtype. For example, with `g(t) = t`
and `a = 0`, the sets `[0, ε)` are path-connected relative neighborhoods of
zero in `[0, ∞)`. They are not ambient neighborhoods of zero in `ℝ`. The packet's
interfaces preserve this distinction.

The topology module contains six supporting declarations, including the
strict-interior result. It restricts a supplied chart to corresponding relative
source and target neighborhoods, obtains local path connectivity of the model
halfspace from convexity, and transports the resulting basis into `S`.
The two literal consumers obtain their chart from the separately owned C296
module. The source inventory and exact assumptions are listed in
[SOURCE_SCOPE.md](SOURCE_SCOPE.md).

The C296 chart remains attributed to **Research Task Watch**. This packet consumes
the [owner-released chart source at commit
`72edcf5b93be45c29f2d10a26f7d8e861a48f528`](https://github.com/d6g8k5htny-coder/Math-/blob/72edcf5b93be45c29f2d10a26f7d8e861a48f528/frontiers/regular_point_chart_20261020/RegularPointChart.lean),
2,767 bytes, SHA-256
`5568c8d6e03f7064cd5924ebe2814ae746100505ae31789d5c975902528f9fa2`.
Its model factor is the kernel of the actual derivative. The chart's construction,
branch, and tests retain their original ownership; this packet implements their
relative-topology consumer. See the
[C296 owner release](https://github.com/d6g8k5htny-coder/Math-/pull/488#issuecomment-6289952847).

Execution evidence currently records:

| Attempt | Observed result |
|---|---|
| Candidate 1, native Darwin | Timed out after 600.061 seconds during observed import reads; no compiler diagnostic or object. |
| [Candidate 1, Claude S Linux execution](https://github.com/d6g8k5htny-coder/Math-/pull/487#issuecomment-6289663934) | Return code 1 after 48 seconds: three elaboration errors in two declarations, plus four style warnings. No object or kernel replay. |
| [Candidate 2, Claude S Linux execution](https://github.com/d6g8k5htny-coder/Math-/pull/487#issuecomment-6289854822) | Return code 1 after 47 seconds: one remaining type-inference error. No object or kernel replay. |
| [Candidate 3, Claude S Linux result](https://github.com/d6g8k5htny-coder/Math-/pull/487#issuecomment-6290047895), following the [exact-source request](https://github.com/d6g8k5htny-coder/Math-/pull/487#issuecomment-6290009856) | Build return code 0 with warnings treated as errors and empty streams, 12.5 seconds. Standard `leanchecker -v RegularSuperlevel` return code 0, 10.0 seconds. The exact 6,405-byte source remained unchanged. |

The successful phases were executed by Anthropic Claude, session
`session_01S16677s1SGeAJmN3QMz4ip` (Claude S), on Linux x86_64.
The kernel phase replayed the named topology module against its imported
environment; it was not a `--fresh` dependency-closure replay. The report did not
execute the literal consumer, an axiom census, or the negative controls, and did
not review the mathematics or chart-consumer fit. The C297 source author read
this execution report and did not execute these Linux phases.

The two negative interface controls deliberately omit, respectively, the
regular-or-strict-interior premise and the chart coordinate identity. They are
intended to reject an unsaturated theorem application after its dependencies
compile. They are not mathematical counterexamples, and an import, syntax, or
resource failure would not establish their intended outcome.

A separate paper-only analytical control uses
`g(t) = exp(-1/t²) sin(1/t)` for `t ≠ 0`, with `g(0) = 0`.
This function is smooth and infinitely flat at zero. Alternating positive and
negative intervals accumulate at zero, preventing a path-connected relative
neighborhood of zero in `{t | 0 ≤ g(t)}`. It shows why smoothness alone cannot
replace the regular-or-interior condition for arbitrary smooth functions. The
example is non-Morse and does not refute the smooth Morse target. It has not been
formalized or executed as a Lean counterexample.

Critical points on the boundary level remain outside the present result.
Deriving their local geometry from literal Morse data, transporting the
pointwise result through the actual torus quotient, and proving full closed-level
local path connectivity remain open. The complete ordinary-H0 finite-bar
adapter, exhaustive once-counted bar correspondence, elder pairing, and the
stochastic obligations also remain open. No numerical constants, normalizers,
field laws, or orders of limits are changed by this packet.

The C297 source author is OpenAI Codex `/root/adapter_feasibility_c292`,
coordinated by OpenAI Codex `/root` for Dylan Roy. Preliminary nonauthor source
review was performed by OpenAI Codex `/root/c292_geometry_review`, with prior
source and proof-shape exposure: same provider, organizational independence 0,
human review 0. Claude S's Linux reports are separately attributed execution
evidence, not mathematical approval. Dylan Roy's personal reading is pending.
