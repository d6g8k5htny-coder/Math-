Public path projection of the retained reviewer-authored record; original 18027 bytes, SHA-256 `c794c85794767711c05f5580bed49d35c011d939c39d0c4a51872b7cccdebc4d`. Only native-root locators are replaced by the named placeholders below; mathematical and review text is unchanged.

- `$C297_ROOT` replaces a native filesystem prefix (1 occurrence(s)).

---

# C297 candidate 3 exact-source nonauthor review

Disposition: **PASS_SCOPED_SOURCE**. No unresolved mathematical, public-interface, census-design, or negative-fixture source finding. This is not final formal acceptance: the C297 literal consumer, full module-origin census, and both negative fixtures still require their actual execution evidence.

The one provenance-comment finding raised during this review was corrected by the author before this report was completed. The corrected literal source is bound below. The reviewer did not edit any Lean source.

## Reviewer and exposure

Actual reviewer: OpenAI Codex `/root/c292_geometry_review`, delegated work for Dylan Roy. This is same-provider, source-exposed nonauthor review: organizational independence 0, human review 0.

Exposure includes C292–C295 reviews, proof-shape advice for C294, C297 relative-topology and analytical-control advice, the complete candidate 1 topology source, the provisional literal consumer, and the exact peer chart source. The reviewer authored the analytical control and preliminary review notes, but did not author the peer chart, topology module, literal consumer, audit source, or either Lean negative fixture. This is not a blind review or a provider-distinct review.

The complete five Lean module sources and both negative fixtures were read for this review. The literal comment-only amendment was then reread and compared with its retained predecessor. The final source identity check is reported below. Prior review notes remain unchanged.

## Exact source bindings

Root directory:

`$C297_ROOT`.

| Relative path | Bytes | SHA-256 |
|---|---:|---|
| `project/Lifetime.lean` | 51,383 | `90f4892608e953ecc696bb32ea159d1c178ceb8a1c6edfd11acfceb14af462c6` |
| `project/RegularPointChart.lean` | 2,767 | `5568c8d6e03f7064cd5924ebe2814ae746100505ae31789d5c975902528f9fa2` |
| `project/RegularSuperlevel.lean` | 6,405 | `0db6ce3ea7358a59c089680d774a6806f0fb747c24d9828850377458156e2f02` |
| `project/RegularSuperlevelLiteral.lean` | 2,299 | `334759063a3ae58b42b8cd4a45e3bfd6f3a31b668d18526aa6fdcb5ea65c13d3` |
| `project/RegularSuperlevelAxiomAudit.lean` | 3,248 | `807de09540b9f7f4f4e14c3408f1f82cb08b1e4232c68c04da5a2355cec02f9e` |
| `negative-project/WithoutCoordinateIdentity.lean` | 950 | `167d0afb49457303a61fac6927784e4f0157ed5725739903bf5e33224974b081` |
| `negative-project/WithoutRegularOrInterior.lean` | 838 | `d3c12e33718a00be343d0e2b3cbbd9a1cdf08e8a2062eb3bfeb7026fb47a543d` |

The chart is the separately owned C296 input released at Math- PR488 head `72edcf5b93be45c29f2d10a26f7d8e861a48f528`, production path `frontiers/regular_point_chart_20261020/RegularPointChart.lean`, Git blob `77a75a4611040973ad355aff40555a808f1816e7`. The reviewer independently computed that Git blob and verified equality of the project bytes with the file content recorded in `evidence/PEER_CHART_DELIVERED_READBACK.json`. That readback is 32,186 bytes, SHA-256 `1eb5139b0e658fd9bdf5fc47d642e784ab46cfb21bb5f8066a4200507e05d2c4`, and contains the owner's release comment `6289952847`. This review did not repeat the remote fetch or independently certify the peer's entire hosted execution.

## Literal statement and imported hypotheses

The imported definitions have their actual intended meaning:

- `E d` is `EuclideanSpace ℝ (Fin d)`.
- `IsSmooth d g` means `∀ n : ℕ, ContDiff ℝ n g`.
- `IsCriticalPoint d g x` means `fderiv ℝ g x = 0`.

No field, bar interface, Gaussian law, Morse predicate, periodicity condition, supplied path, or global local-path-connectivity instance is used to obtain the C297 public conclusions. The unrelated Lifetime statements remain definitions/specifications and are not promoted by this work.

The literal theorem `closed_superlevel_regular_basis` supplies a path-connected neighborhood basis at the prescribed point of `{y : E d // a ≤ g y}` from smoothness and literal noncriticality. Its public inputs contain neither a chart nor an LPC premise.

The second public theorem, `closed_superlevel_path_connected_basis`, retains the explicit condition

`a < g x.val ∨ ¬ IsCriticalPoint d g x.val`.

It handles strict-interior points and regular points, including regular boundary points. It does not handle a critical boundary point merely because the function is smooth or Morse. The point is a subtype point, so its membership in the weak superlevel is already supplied.

The statements allow any natural dimension. In dimension zero the regular branch has an impossible nonzero scalar derivative premise; the strict-interior branch remains valid. This is not a missing positive-dimension assumption. Smoothness is stronger than the continuity needed for the interior branch and supplies the strict derivative needed for the peer chart.

## Mathematical reconstruction

### Peer chart consumption

The peer first proves that literal noncriticality makes the derivative's underlying linear map nonzero. Pointwise extensionality converts a hypothetical zero underlying linear map into zero of the continuous linear map. The scalar dual range theorem then yields full range.

The separate smoothness lemma supplies `HasStrictFDerivAt g (fderiv ℝ g x) x` from smoothness at order one. These two actual facts instantiate the existing finite-dimensional-target implicit-function chart. Its target is the actual product `ℝ × (fderiv ℝ g x).ker`; no assumed coordinate identification of the kernel is needed.

The chart's source-membership lemma and first-coordinate identity are passed to the C297 topology theorem at the same `g` and `x`. Its global first-coordinate equality is used only where the topology theorem requires it, on the chart source. No global inverse behavior is inferred.

The derivative kernel carries the required real normed-space structure. The topology theorem does not require it to be complete or explicitly finite dimensional; the existing normed-space structure suffices for the convex half-space argument.

### Relative topology

`path_connected_basis_of_openEmbedding` pulls an arbitrary target neighborhood back through a continuous open embedding, selects a smaller path-connected domain neighborhood, and maps it forward. Openness supplies target-neighborhood membership and continuity supplies path connectivity. The image lies inside the original target neighborhood. No global LPC of the codomain is required.

`path_connected_basis_of_open` specializes this to inclusion of an open subtype that is already LPC.

`relative_chart_homeomorph` restricts the domain to points of `S` lying in `p.source` and the codomain to points of `T` lying in `p.target`. In its inverse, `p.map_target` first puts the inverse image in the source. The source-local membership equivalence and the chart right-inverse identity then prove membership in `S`. The two inverse identities and continuity arguments use exactly the chart restrictions under which those properties hold.

`path_connected_basis_of_relative_chart` makes the source and target intersections open in their respective subtypes. It obtains LPC of the target intersection from LPC of `T`, transports it through the restricted homeomorphism, and then transfers the pointwise basis through the open inclusion into `S`. It does not assume ambient openness of either `S` or `T`.

`closed_superlevel_basis_of_chart` takes the model half-space

`H = {z : ℝ × F | a ≤ z.fst}`.

The explicit convexity proof uses nonnegative scalar weights summing to one. The real normed product is locally convex, so convexity supplies LPC of the subtype `H`. The coordinate identity gives the exact membership equivalence on `p.source`. This proves the relative basis result without assuming the desired superlevel LPC.

For arbitrary `g`, this generic chart theorem does not assert that the whole superlevel is ambient-closed: its public hypotheses only constrain `g` on the chart source. Its conclusion is still valid. In the literal smooth consumer the weak superlevel is genuinely closed by continuity, although global closedness is not needed by the local argument.

`closed_superlevel_interior_basis` takes the open ambient set `U = {y | a < g y}`. Continuity proves its openness and the Euclidean LPC instance gives LPC of `U`. The inclusion into `S = {y | a ≤ g y}` is the restriction of the identity open embedding. The explicit `MapsTo` proof and specified `(s := U) (t := S)` instantiate the actual restriction interface correctly. Its image is relatively open in `S`; the proof does not require `S` to be ambient-open.

All final neighborhood filters are those of the actual superlevel subtype. The implementation avoids the false requirement that a boundary point admit an ambient neighborhood contained in its closed superlevel.

## Candidate changes and closed finding

The candidate 1 to candidate 3 topology diff changes only proof elaboration details:

- the `hasBasis_self` witness uses the correct flat constructor grouping;
- four proposition-valued local instance introductions use `let`;
- membership in the let-bound superlevel subtype is explicitly reduced to an inequality;
- the strict-interior inclusion uses an explicitly typed identity, an explicit `MapsTo` proof, and named source/target arguments.

The six declaration statements and their mathematical roles are unchanged. Candidate 2 to candidate 3 changes only the final open-embedding restriction elaboration.

During this review, the old 2,271-byte literal file still described the peer chart as provisional at `9873446f5728799ef3d12808df65344827ac4754`, despite its delivered owner-release readback. This was a nonblocking provenance defect, not a theorem defect. The author corrected the header to the released `72edcf5b93be45c29f2d10a26f7d8e861a48f528` input and retained the explicit pending status of the C297 consumer's own execution. The reviewer read the corrected header and verified that every byte from `open Set Filter Topology` onward is identical to the retained `a8c1946f07cee68a4e3210304fdc997455a4e443d0f9edb3b54bfac387702d4e` predecessor. **Finding closed.**

## Full-census source design

The audit source imports the literal consumer, thereby importing the four intended source/proof modules. Its census selects declarations by actual module origin for `Lifetime`, `RegularPointChart`, `RegularSuperlevel`, and `RegularSuperlevelLiteral`. It does not restrict the census to a namespace or a handpicked list of public theorem names.

The environment view is set to nonexporting before enumerating constants, so private and generated declarations are eligible. Each requested module must exist and have a nonempty inventory. Every enumerated name must be present in the checked kernel environment. The code invokes `Lean.collectAxioms` for every name and rejects any returned axiom outside `propext`, `Classical.choice`, and `Quot.sound`; thus `sorryAx` is not permitted.

The additional required list contains exactly 17 names: two literal Lifetime definitions, seven peer-chart declarations, six topology declarations, and two literal consumers. This is an omission guard, not the total-census definition or a claim that the total inventory has size 17. The actual complete inventory count must be measured from the run.

The reviewer also read the installed Lean `Lean/Util/CollectAxioms.lean`: it uses the private environment, kernel declarations, and transitive axiom information, including precomputed information for imported declarations. The audit therefore is not a fresh kernel replay of the full import closure. The three initial `#print axioms` commands and three explicit `#check` commands provide selected additional output; they do not replace the module-origin enumeration.

The audit implementation is source-appropriate for the stated four-module census. No actual census success, count, or standard-only outcome is inferred before its execution. The hosted runner and its output parser are outside this source review.

## Negative fixtures and analytical control

`WithoutCoordinateIdentity.lean` supplies the chart and source-membership proof but omits the final source-local first-coordinate identity from the actual `closed_superlevel_basis_of_chart` invocation. The remaining term has a function type from that identity premise to the basis conclusion, whereas the fixture requests the basis proposition itself. A meaningful execution result is the corresponding premise/function-versus-conclusion type mismatch after successful imports. Syntax, unknown-name, import, resource-limit, or timeout failures do not satisfy this control.

`WithoutRegularOrInterior.lean` supplies smoothness, the level, and the subtype point, but omits the final disjunction from the actual `closed_superlevel_path_connected_basis` invocation. The expected meaningful rejection is again the remaining premise function versus the requested basis proposition, identifying the regular-or-strict-interior condition. This fixture does not prove that no different theorem or proof could cover a particular critical point.

Both fixtures are deliberately ill-typed interface tests, not Lean counterexamples, and neither had an executed outcome in the evidence reviewed here.

The supporting analytical control is the smooth function

\[
g(0)=0,\qquad g(x)=e^{-1/x^2}\sin(1/x)\quad(x\ne0).
\]

All its derivatives at zero vanish, by the polynomial-times-flat-exponential derivative formula. For \(k\ge1\), set

\[
p_k=\frac{2}{(4k+1)\pi},\qquad q_k=\frac{2}{(4k+3)\pi}.
\]

Then \(0<q_k<p_k\), both sequences tend to zero, \(g(p_k)>0\), and \(g(q_k)<0\). Every relative neighborhood of zero in \(S=\{g\ge0\}\) contains some \(p_k\). A path in that neighborhood from zero to \(p_k\) would pass through \(q_k\) by the intermediate value theorem, which is impossible. Thus there is no path-connected relative neighborhood basis at this critical boundary point.

This demonstrates that arbitrary smoothness does not justify dropping both alternatives. It is non-Morse and does not refute the project's Morse target. The detailed sign intervals, flatness argument, optional smooth periodic composition, and limitations are recorded in the unchanged `reviews/ANALYTIC_CONTROL_AND_PRELIM_REVIEW.md`, 10,767 bytes, SHA-256 `a3c688550b970899389024fddd6b94c7bf7feb5dfeb175f9d7b38a1139f791ca`.

The separate topology trap is \(g(x)=x\), level zero, at the regular boundary point zero. The sets \([0,\varepsilon)\) are path-connected relative neighborhoods in \([0,\infty)\), but are not ambient neighborhoods of zero in \(\mathbb R\). The reviewed statements and proofs use the correct subtype filters. This mathematical check is not reported as an executed Lean control.

## Observed execution records and their limits

This reviewer initiated no Lean build, kernel replay, negative test, or hosted run. The following are records of Claude S's separate execution, read from the retained evidence:

- Candidate 1: source `0758454e88cb02ad56483face96483d8a878afe5eaa72f1ea629f0ca5a29760f`, compile rc 1, 48 seconds, no object and no kernel replay. The full projected stdout is 2,087 bytes, SHA-256 `8b828f7860a2106ab45d8d37cf5560c842f6ea3bb9652592fff9c41c7ad5db45`. Constructor grouping and subtype elaboration failed; four style warnings were also present.
- Candidate 2: source `b5733777504470cc1a2edfff780d0d7b7f271fdfc3db377cdb093f7e356f946d`, compile rc 1, 47 seconds, no object and no kernel replay. The retained report `evidence/CANDIDATE2_RESULT.json` is 10,735 bytes, SHA-256 `4fbdb29d4c2eecf5b5ec13daf770ef3c225e83c5f41bf584cebd8e7b08b1d866`. The actual reported error concerns inference of the source subset/topology in `IsOpenEmbedding.restrict`.
- Candidate 3: source `0db6ce3ea7358a59c089680d774a6806f0fb747c24d9828850377458156e2f02`, build rc 0 under warning escalation, empty streams, 12.5 seconds; standard `leanchecker -v RegularSuperlevel` rc 0, 10 seconds. The reported Linux object is 208,992 bytes, SHA-256 `cffe26cd70fb2b8e2ddf965562a794745a1358bc22e012a85953578d14220526`, unchanged after replay.

For candidate 3 the reviewer read `evidence/LINUX_CANDIDATE3_RESULT.json` (11,077 bytes, SHA-256 `ab3b3d8de572310e6054d83e8cf5475ea9f6223c6fc648f89f59246571d9f950`) and the complete `evidence/linux-candidate3-receipt.json` (2,864 bytes, SHA-256 `3f479a7fc32198389acb8d9db23f913495a5357b1ae1e56cd39e6107074e9ef0`). The saved kernel stdout was read and hashed: 28 bytes, SHA-256 `92c0c414a888780c0722d6767245b01bd449841486bdd45f93f47c116fe57b0b`, containing `replaying RegularSuperlevel` and its newline. The report is Math487 comment `6290047895`; the executor is Anthropic Claude session `session_01S16677s1SGeAJmN3QMz4ip`.

That successful execution covers the six-declaration topology module against its imported environment. It is not `--fresh`, does not establish the literal consumer's elaboration, and includes no C297 full census or either negative fixture. The reviewer did not fetch or independently replay the Linux object. Earlier clean-looking declarations in failed candidates are not counted as separately verified objects.

## Final boundary

No unresolved source-level finding prevents freezing these exact proof inputs for the next execution stage. This verdict does not grant formal acceptance in advance of the remaining evidence.

Still outside this result are the critical-point Morse local form, relative topology at critical boundary points, quotient chart transport, actual global closed-level LPC, C294's critical-level LPC premise removal, strict death drop, and the complete ordinary-H0 adapter. Scientific effect is NONE. Source identities, semantic review, external execution reports, full-census execution, negative-control execution, and eventual final acceptance remain distinct evidence categories.

Only this new review note was written by the reviewer. Earlier review notes, all Lean sources, imported inputs, execution artifacts, claims, and remote records were left unchanged by the reviewer.
