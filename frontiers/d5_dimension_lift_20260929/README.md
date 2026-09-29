# D5 in every fixed dimension (CL-D5-DIMENSION-LIFT-20260929-v1)

Author-side proof candidate by Anthropic Claude. **Nonauthor analytic review required.** Scientific effect: NONE.

## What it proves, if the arguments hold

The three planar D5 components and their composition, in every fixed `d >= 2`, for the exact model of `imports/lifetime_parent_20260925` with compact marks, the original endpoint weight and the full normalizer:

| Result | Statement | Planar source it lifts |
|---|---|---|
| Theorem P_d | all-height punctured pin ball: `E N_j(M + rE) <= C r^3 ∫_E max(|q|, r|p|)^(2-d)` | `PUNCTURED_PIN_PROOF.md` (P2) |
| Theorem C_d | compact collar `E N_j(rE) <= C r^3 |E|` and the fixed scaled ball minus pins | `COLLAR_PROOF.md` (C1), (C2) |
| Theorem I_d | height-window shells `E N <= C r^3[(r/s)^2 + s^2]`, dyadic sum `C r^3(A_0^-2 + rho^2)` | `intermediate_window_20260928` (I3), (I4) |
| Theorem G_d | global window first moment `E_(Q^W) N(T^d minus {M,S}) <= C r^3` | `intermediate_window_20260928` (I5) |
| Corollary F_d | `c r^3 <= Q^W(A_r) <= C r^3` in every `d` | closes the `d > 2` conditional in `remote_collision_20260928` Corollary F |
| Corollary M_d | `Q^W(N_r >= 2) = Theta(r^3)` in every `d`; no `O(r^5)` global factorial bound | `LOCAL_MULTIPLICITY.md` Theorem L, `elder_dimension_lift` (A4) |

The application dimension of the program is `d = 3` (SIDE24). Until now every D5 upper bound was planar.

## The five devices (PROOF.md §3)

1. Two soft directions: `|det H| <= ||He|| ||He'|| K^(d-2) / sigma` through the second exterior power. Replaces the planar two-column bound at each of the three Hessians.
2. One soft direction: `|det H| <= ||He|| K^(d-1)` (Hadamard). The angle-free bound.
3. Jet functionals on `R^m`: the Gram of `S -> S beta` is at least `|beta|^2/2`; the `C` and `D` functionals have norms at least `|beta|^2/2` and `|beta|^3/12`. Gives the frame floors, including the explicit pin-frame floor `det(BB^T) >= (9/64)^(d-1)/2048`, which is the planar `9/131072` at `d = 2`.
4. Transverse block determinant: `det S = eps det S' - w^T adj(S') w`. The Euler identity controls `eps` and the gradient equation controls `w`; together they control `det` of the endpoint transverse blocks with the same `(r + s^2)/|v|^2` as the planar scalar.
5. Integrable pin weight `max(|q|, r|p|)^(2-d)`: the intensity is unbounded on the axis for `d >= 3`, but its integral over the ball is `O(1)`, so the count keeps order `r^3`.

## Run

    python -B -S lift_exact_check.py                      # rc 0, output = RESULTS.json
    python -B -O -S lift_exact_check.py                   # rc 0, byte-identical
    python -B -S lift_exact_check.py --mutant NAME        # rc 1 for each of the ten names in the docstring

Nine groups of exact checks (`X G R RO EU TB N L W`): exterior-power inequality and its equality case, frame rank and floors on rational points of the sphere, confluent interpolation rank in `d = 2, 3, 4` with the degree-four negative control, the `d = 3` row operation on an exactly pinned cubic, the `d = 3` Euler identity, the block-determinant identity, the three jet-functional norms, all power ledgers for `d = 2..6`, and the pin-weight exponents. They verify identities, ranks, floors and exponents only.

## Review requests (exact interfaces)

1. Lemma D1: the singular values of `Λ²H` are the pairwise products; the plane coefficient bound `1/sigma`.
2. Lemma D3: the Gram of `S -> S beta` over independent entries, `>= |beta|^2/2`; the block-Schur computation (4.4).
3. Lemma D4 and its use in (6.8): that `hat v^T S_0 hat v` (Euler) and `S_0 hat v` (gradient equation) together control `det A_i`, with the `s^2/|v|^2` cross term.
4. Lemma D5: integrability of the weight and the `O(r^5)` nested-ball bound; the region I/II ledgers (4.11), (4.12).
5. §5.1 and §6.1: degree-five interpolation in `d` variables, the confluent families, and the compactness step.
6. The tiling in §7, and the claim that [RM] Theorem A, [RC] (F-) and [EDL] (A4) are consumed at their stated every-`d` scope.
7. Every step cited as "verbatim" from a planar source: confirm it is in fact dimension-free. The vector-valued
   statements behind (4.1), (5.2) and (6.2) are derived in §4.2, §5.3 and §6.3 rather than cited.
8. For the `d >= 3` continuum read: `CONTINUUM_CROSSWALK.md` lists every held continuum step with its planar line,
   the place where the `d`-dimensional argument is written, and the complete list of changes.

## What this does not do

No all-height global count, no torus-wide second factorial moment, no collision estimate outside the fixed remote region, no elder-selection claim, no numerical constant, no uniformity in `k`, `L` or `d`, no recovery of historical carriers, no register change. The relation to `hist.OBL-H5-JETMOD` and the D5 region nodes of `frontiers/downstream_gate_20260925/GRAPH.json` is a matter for a later source-bound reconciliation after nonauthor review; this packet asserts nothing about them.

## Provenance

Consumed sources and their exact identities: `SOURCE_MAP.json`. This packet's own inventory: `SOURCE_FILES.json`. External check: `RECONNAISSANCE.md`. Same GitHub account as every lane; zero organizational-independence credit. The planar sources are OpenAI-authored and were reviewed by Anthropic and xAI lanes at their exact heads; those reviews are cited for their own scopes only and do not transfer to this note.
