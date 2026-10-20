Public path projection of the retained reviewer-authored record; original 10767 bytes, SHA-256 `a3c688550b970899389024fddd6b94c7bf7feb5dfeb175f9d7b38a1139f791ca`. Only native-root locators are replaced by the named placeholders below; mathematical and review text is unchanged.

- `$C297_ROOT` replaces a native filesystem prefix (1 occurrence(s)).
- `$PINNED_MATHLIB` replaces a native filesystem prefix (1 occurrence(s)).

---

# C297 analytical control and preliminary source review

Disposition: **PRELIMINARY_SOURCE_REVIEW; NO FINAL ACCEPTANCE**.

This note combines the requested mathematical negative-control analysis with a read-only review of candidate 1 of `project/RegularSuperlevel.lean`. Compilation was reported as running when the review was requested. This note does not establish successful elaboration, kernel replay, axiom audit, execution of controls, or a frozen final artifact.

Reviewer: OpenAI Codex `/root/c292_geometry_review`, delegated work for Dylan Roy. The reviewer did not author or modify this Lean module. Exposure includes previous C292–C295 source reviews, proof-shape advice for C294, and the topology/control advice reproduced below. This is same-provider, source-exposed nonauthor review: organizational independence 0, human review 0. The mathematical control is supporting analysis within C297's claimed scope, not a separate theorem delivery.

## Exact candidate and reviewed scope

The complete candidate was read and its identity checked again after the source/API inspection:

- Path: `$C297_ROOT/project/RegularSuperlevel.lean`.
- Length: **6,173 bytes**.
- SHA-256: **0758454e88cb02ad56483face96483d8a878afe5eaa72f1ea629f0ca5a29760f**.
- Six explicit declarations, lines 17–131, under `TorusRegularSuperlevel`.

The imported `project/Lifetime.lean` is 51,383 bytes, SHA-256 `90f4892608e953ecc696bb32ea159d1c178ceb8a1c6edfd11acfceb14af462c6`. Its `import Mathlib` and the previously reviewed literal `E d` convention were retained. This review did not rereview all of Lifetime's unrelated specifications.

The relevant existing API declarations were read in the pinned Mathlib checkout rooted at:

`$PINNED_MATHLIB`.

Specifically:

- `Mathlib/Topology/Connected/LocallyPathConnected.lean`: the neighborhood-basis definition, open-subspace inheritance, and homeomorphism transport.
- `Mathlib/Topology/Constructions.lean`, lines 573–592: restriction of inducing maps, embeddings, and open embeddings to mapped subsets.
- `Mathlib/Topology/Algebra/Module/LocallyConvex.lean`, especially lines 104–121: local path connectivity of real locally convex spaces and convex subsets.

The review covers the semantic match of these six declarations and their relative-topology interfaces. It does not inspect or construct the separately owned scalar implicit-function chart, nor claim a literal regular-point consumer already exists.

## Preliminary source findings

**No concrete mathematical or interface bug was identified in this exact candidate.** This is a preliminary source finding, not a compilation or final acceptance verdict.

1. `path_connected_basis_of_openEmbedding` (lines 17–29) transfers a path-connected neighborhood basis from the domain to the image point. Continuity pulls the ambient target neighborhood back; the domain's local path connectivity supplies a smaller path-connected neighborhood; openness makes its image a neighborhood of the image point. The image lies in the originally prescribed target neighborhood. It does not require or conclude global local path connectivity of the codomain.

2. `path_connected_basis_of_open` (lines 32–36) applies that result to the inclusion of an open subtype. Its hypothesis is local path connectivity of this open subtype, and its conclusion concerns an ambient point belonging to the open set. This is a legitimate local transfer, not inheritance by an arbitrary subset.

3. `relative_chart_homeomorph` (lines 40–68) uses the correct restricted spaces: points of `S` whose ambient values belong to `p.source`, and points of `T` whose ambient values belong to `p.target`. In the inverse, `p.map_target` first establishes that the inverse image lies in the chart source; only then is `hmem` used. The chart's right-inverse identity transfers membership in `T` back to membership in `S`. Both inverse identities and both continuity proofs are confined to their proper chart domains. No global inverse behavior is assumed.

4. `path_connected_basis_of_relative_chart` (lines 72–86) proves that these source and target intersections are open in `S` and `T` respectively, by preimages under subtype inclusion. It obtains local path connectivity of the target intersection from that of `T`, transports it through the restricted homeomorphism, and uses the open inclusion into `S`. The final `𝓝 x` is the neighborhood filter in the subtype `S`; no ambient openness of `S` or `T` is assumed.

5. `closed_superlevel_basis_of_chart` (lines 93–115) takes an actual open partial homeomorphism, source membership of the point, and the scalar-coordinate identity on the entire chart source. The model half-space `H = {z : ℝ × F | a ≤ z.fst}` is proved convex, and its local path connectivity is obtained from the real normed-space structure. The coordinate identity then gives the required membership equivalence exactly on the source. This is sufficient for the preceding relative chart result. The proof does not assume a global locally path-connected superlevel, and does not construct a regular-point chart from a derivative. Completeness or finite dimensionality of `F` is unnecessary for this topology step.

6. `closed_superlevel_interior_basis` (lines 119–131) uses continuity to make `U = {y | a < g y}` open in the Euclidean source. This open set is locally path connected. Its inclusion into `S = {y | a ≤ g y}` is obtained by restricting the identity open embedding using `U ⊆ S`. The actual `IsOpenEmbedding.restrict` interface requires the original source subset to be open, which is precisely the proved `hU`; it does not require `S` to be ambient-open. The final point is the prescribed subtype point, and the output is a basis in `S`.

The candidate therefore avoids the relative-topology trap described below. The source/target restriction is present in the homeomorphism itself, and the model half-space inherits local path connectivity from proved convexity. The separately owned chart constructor still must supply `p`, `hx`, and `hcoord` before a literal noncritical-point corollary is established.

## Analytical control: smoothness alone is insufficient

Define the real function

\[
g(x)=
\begin{cases}
e^{-1/x^2}\sin(1/x),&x\ne0,\\
0,&x=0,
\end{cases}
\qquad S=\{x\in\mathbb R:g(x)\ge0\}.
\]

For every nonnegative integer \(m\), on \(x\ne0\) the derivative has the form

\[
g^{(m)}(x)=e^{-1/x^2}
\bigl(P_m(1/x)\sin(1/x)+Q_m(1/x)\cos(1/x)\bigr)
\]

for real polynomials \(P_m,Q_m\). Differentiation preserves this form. The exponential factor dominates every reciprocal power of \(|x|\), so both these expressions and their difference quotients at zero tend to zero. Induction establishes \(g\in C^\infty(\mathbb R)\) with \(g^{(m)}(0)=0\) for every \(m\). In particular, \(0\) is critical and its Hessian is zero.

For each integer \(k\ge1\), set

\[
I_k=\left[\frac1{(2k+1)\pi},\frac1{2k\pi}\right],
\qquad
J_k=\left(\frac1{(2k+2)\pi},\frac1{(2k+1)\pi}\right).
\]

Since the exponential factor is positive off zero, \(g\ge0\) on \(I_k\), with strict positivity in its interior, and \(g<0\) on \(J_k\). Explicit points are

\[
p_k=\frac2{(4k+1)\pi},\qquad q_k=\frac2{(4k+3)\pi}.
\]

Then \(0<q_k<p_k\), both tend to zero, and

\[
g(p_k)=e^{-1/p_k^2}>0,\qquad
g(q_k)=-e^{-1/q_k^2}<0.
\]

Let \(N\subseteq S\) be any neighborhood of zero in the subspace topology of \(S\). There is \(\varepsilon>0\) such that

\[
S\cap(-\varepsilon,\varepsilon)\subseteq N.
\]

For sufficiently large \(k\), the points \(0,p_k\) belong to \(N\). Any path in \(N\) joining them, composed with the inclusion into \(\mathbb R\), must attain \(q_k\) by the intermediate value theorem. This is impossible because \(q_k\notin S\). Thus zero has no path-connected relative neighborhood, and in particular has no path-connected relative neighborhood basis. The interval property of connected subsets of \(\mathbb R\) also excludes connected relative neighborhoods. The positive and negative values accumulating at zero establish that it is a boundary point.

This refutes removal of both the regular-point and strict-interior alternatives from a statement for arbitrary smooth scalar functions. It does not show that regularity is necessary for every individual function: the zero superlevels of \(x^2\) and \(-x^2\) are locally path connected at their critical point.

The counterexample is non-Morse, because the critical point at zero is infinitely flat. It does not refute the project's smooth Morse target or show that the project's eventual critical-point argument cannot succeed. It is a conventional mathematical argument, not a formal Lean counterexample or an executed premise-removal test.

Periodicity is not an obstruction to such a smooth non-Morse control. For any \(L>0\), the explicit function

\[
G_L(x)=g\bigl(\sin(2\pi x/L)\bigr)
\]

is smooth and \(L\)-periodic. The inner map is a local diffeomorphism at zero, so it transports the same local superlevel obstruction. All derivatives of \(G_L\) at zero still vanish. This optional observation adds no Morse or quotient theorem to the review.

## Wrong-relative-topology control for later review

For \(g(x)=x\), level \(a=0\), and the regular point \(x=0\), the closed superlevel is \(S=[0,\infty)\). The sets \([0,\varepsilon)\) form a path-connected relative neighborhood basis at zero. They are open in \(S\), but they are not ambient neighborhoods of zero in \(\mathbb R\).

A purported boundary-point proof that requires its superlevel neighborhoods to belong to the ambient `𝓝 x`, or to be ambient-open subsets of \(S\) containing zero, imposes a false requirement. The intended filter is the neighborhood filter of the superlevel subtype, or the corresponding `𝓝[S] x`. In addition, chart inverse transport must stay inside the chart target.

The exact candidate reviewed here respects both requirements: all final neighborhood filters are on the superlevel subtype, and the relative homeomorphism explicitly restricts to source and target.

## Execution and final-review boundary

No Lean process, compiler, test, kernel replay, or remote post was initiated by this reviewer. Only source reads, local identity calculations, and creation of this authorized review note were performed. No implementation or imported source was modified.

The final review must bind the eventual frozen source, any separately owned chart input or literal consumer actually included, and the observed build/kernel/control records. This preliminary review does not anticipate those results or grant formal acceptance.
