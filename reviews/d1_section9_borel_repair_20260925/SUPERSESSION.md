# Section 9 Borel repair — one disposition

**Disposition: SUPERSEDED_NONBLOCKING.**

The accepted parent §9 already contains the repaired argument. The repair file should stay in Git as historical provenance. It should not be indexed as an active amendment.

**Scientific effect: NONE.** This note does not edit `REPAIR.md`, the parent, `GRAPH.json`, or `lemma_closed`. It does not re-review §§2–§7, the cap theorem, or coefficient (15.2).

## Sources

| Item | Identity |
|---|---|
| Repair | `reviews/d1_section9_borel_repair_20260925/REPAIR.md`, blob `fe9b9ce4999908bb3814b500ee2d0ceb0c6f704a`, 9062 bytes, SHA256 `845abf9f9c99d672c2a10a887b5a2e7206a3d2de3d876f35f75ff6e2dc13e62f`, commit `694b7ff3047dd8e52817b1432d40c99ea0135a08` |
| Parent | `imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md`, blob `dfed3b8d318a3ab1950957f393307733a4bef3f2`, 40261 bytes, SHA256 `9350ad6eaba6626b93c3dedeef9e2ff816e5cdf1c8318e85fb27499141c84bc7` |
| Accepted §9 review | main issue 63, comment 5841570965, interface D1-B **ACCEPT** of parent lines 298–308. Session `bc-ce4bf0bc-0a0b-4cb1-abaf-7c5b8914418c` |
| Primary PDF | arXiv:2304.07424v3, https://arxiv.org/pdf/2304.07424v3 |

The parent blob is the same object at Math- `703e947` (the review pin) and at current `main` `1e1114f5eb8ef8cdbcde591bf74126274c250f88`.

## Why the repair is superseded

Parent lines 302–308 already do the work the repair writes out again:

- Kac–Rice on compact off-diagonal pair domains, with Jacobian `|det H_x det H_y|`.
- Conditional laws of the whole smooth field, continuous in the imposed gradients by finite-dimensional Gaussian regression.
- Theorem 7.1 applied to bounded nonnegative continuous cylinder weights of the 2-jet.
- Two finite measures on location × `C^2`, with mass from the unweighted formula.
- Cylinder evaluations on a countable dense set generating the Borel σ-algebra.
- Equality on the bounded continuous test-function algebra, extended by the monotone-class theorem to bounded Borel global marks.
- The elder indicator kept Borel, and kept out of the lower-semicontinuous hypothesis.
- The §8 elder mark and type indicators, height disintegration, candidate intensity equal to the full-pin density times `E_Q[W]`, and selected intensity equal to that quantity times `p_r`.
- Off-diagonal exhaustion by the locally integrable `r dr` bound and nonnegative monotone convergence.

D1-B accepts those lines and states the closure in the same form: both sides are finite measures, the cylinder algebra generates `Borel(C^2)`, and bounded pointwise limits stay in the identity by dominated convergence against a finite expected pair count. The elder mark is bounded and Borel by §8, so the identity reaches it. The typed weight `|det H_M det H_S| 1_type` is the Kac–Rice Jacobian times a bounded Borel factor, counted once.

`REPAIR.md` §§9.1–9.4 name the regression kernel, the measures `μ` and `ν`, and the three functional-monotone-class properties. Those sentences spell the same accepted argument. They do not add a hypothesis or a conclusion absent from parent lines 298–308 and from D1-B.

## Line map

| Repair | Parent | Accepted #63 reading |
|---|---|---|
| Lines 13–19: Theorem 2.2 unweighted; Theorem 6.1 Crofton; Theorem 7.1 weighted formula (7.2); continuous cylinders only | Line 304 cites Theorem 7.1 for bounded nonnegative continuous weights and refuses to treat the elder mark as lower semicontinuous. Lines 492–494 keep the pair/Borel application in §9 | D1-B: v3 Theorem 7.1 is the weighted identity under lower semicontinuity; continuous 2-jet cylinders meet it |
| Lines 27–35: `G`, `Δ = \|det H_x det H_y\|`, Theorem 2.2 for finiteness on compact `D` | Lines 302–304: the same vector field, the same Jacobian, finiteness “by the unweighted formula” | D1-B: the unweighted formula supplies the mass on each compact off-diagonal pair domain |
| Lines 37–55: kernel `K(t,z,A) = P{m_(t,z)+R_t ∈ A}` | Line 302: whole-field conditional laws by finite-dimensional Gaussian regression. Line 306: the continuous regression kernel is the canonical density version | D1-B uses that regression for the conditional mark law |
| Lines 57–74: finite `μ`, `ν` and (9.1) on continuous cylinders | Line 304: the two measures are finite and agree on the bounded continuous cylinder algebra | D1-B: both sides are finite measures on a Polish space and agree on the cylinder algebra |
| Lines 76–92: countable 2-jet evaluations generate `Borel(D×E)`; `H` is a vector space, contains constants, and is closed under bounded pointwise convergence | Line 304: countable dense cylinder evaluations plus location coordinates generate the Borel σ-algebra; the monotone-class theorem passes from the test-function algebra to bounded Borel marks | D1-B: the cylinder algebra generates `Borel(C^2)`; bounded pointwise limits stay inside the identity by dominated convergence |
| Lines 94–108: §8 path tests make the elder mark Borel; index indicators are Borel; `Δ` times the type indicators is `W_r` once; intensity is the full-pin density times `E_Q W_r`, and the selected intensity multiplies by `p_r` | Lines 26–27 define `W_r`. Lines 290–294 make `{d_f(M)=f(S)}` Borel. Line 306 is the same intensity accounting | D1-A accepts lines 276–296. D1-B: the elder mark is bounded and Borel by §8, and the typed weight is the Jacobian times one bounded Borel factor |
| Line 110: exhaust `D` by the parent `r dr` bound | Line 308: the same exhaustion, using the bound proved in §10 | D1-C accepts §10, including that radial factor. Line 110 also names §§3 and §5; the repair does not accept those sections, and this note does not review them |

## Primary-source check used for the citation lines

The v3 PDF, not the ar5iv HTML, is the numbering source. In that PDF:

- Theorem 2.2 is the Gaussian unweighted formula, with finite expected measure on compact domains.
- Theorem 6.1 is Crofton’s formula, displayed as (6.3).
- Theorem 7.1 is “Expected integral on the level set,” displayed as (7.2), under lower semicontinuity in the location and in the auxiliary field, and continuity of the conditional law. Remark 8 records that a joint Gaussian law gives condition (c). The proof reduces a monotone limit of continuous weights to the continuous case.

That is the map in repair lines 13–17. The parent’s use of Theorem 7.1 for the continuous-cylinder base is the same citation. The ar5iv HTML renumbers these statements; it is not the PDF the repair names.

## Indexing

Keep `reviews/d1_section9_borel_repair_20260925/REPAIR.md` as historical provenance of an explicit rewrite of an argument the accepted parent already contains. On current `main` the only Git hit for this object is the file itself; it is not a landing-claim row. Do not add it as an active amendment.

## Provenance of this note

| Item | Value |
|---|---|
| Reviewer | Grok 4.7, xAI (`grok-4.7-high-fast`) |
| Session | `bc-98eef704-4871-4800-abb4-adf3f66a7237` |
| Repair author | OpenAI / ChatGPT |
| Relation to D1-B | D1-B is the assigned acceptance record for parent lines 298–308. This note compares the repair with that record and with those lines. It is a different session from `bc-ce4bf0bc-0a0b-4cb1-abaf-7c5b8914418c` |
