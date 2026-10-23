# Root internal mathematical check — C292

Executor: OpenAI Codex `/root`, delegated for Dylan Roy. This is an internal author-side reconstruction, not an additional nonauthor vote. Proof checked in full: 25,662 bytes, SHA-256 `39f92734da35aa4c3ad97ea9d8e194cea4ee3a0b23054a8a412f331294d74762`.

I checked the literal `SuperlevelBar.lean` definitions: essentiality is global maximality, clearance quantifies actual Euclidean paths with strict height inequalities, and death is the conditional real supremum with an empty-set default. Nonessentiality and continuity activate the existing nonempty strict-cut theorem; the proof does not interpret the empty default as a finite bar.

The complementary-sign Hessian argument is exact: if z=v+w lies in the radical, symmetry yields B(v,v)=-B(v,w)=B(w,w). Negative and positive definiteness on the complementary subspaces force v=w=0, even with nonzero cross terms. At a maximum the negative subspace has full dimension. This justifies the classical local Morse and inverse-function imports without adding a nonsingular-Hessian premise.

The strict drop uses the first exit from an ordinary Euclidean ball around M, so no quotient-chart injectivity is silently required for that step. The compact sphere is nonempty because n>=1. A path to a higher endpoint must exit; the uniform sphere ceiling bounds every member of the clearance set and hence the nonempty supremum.

The endpoint step maximizes F over the compact closure of an open path component of {F>a}. The maximum is strictly above a, so relative closedness returns it to the original open component. It is an unconstrained local maximum. Finiteness of the quotient critical set then supplies one fixed higher maximum along a cofinal subsequence; no limit of merely higher endpoint heights is used.

The nested sets are closed connected components of closed superlevels, not a purported compact space of paths. Their intersection gives only connectedness. The Morse quadratic cone supplies local path connectivity of the ambient closed superlevel, whose connected component then supplies an actual path. This is the missing justification that prevents an invalid connected-implies-path-connected inference.

For C the strict-death path component and D its closure, D intersect {F>death}=C and C is open. A frontier point of D above death would lie in C and thus in the interior of D. A point of C above the birth height would contradict the strict cut at death. Continuity extends the birth ceiling to D. The older endpoint is outside D by its strictly larger value. These match every input of the unchanged `elderTrap_of_boundary` and `elderBoundaryDirectSummand` read in full.

Boundary controls are mathematical, not numerical experiments: (1) the essential maximum is excluded before the empty-default death could be used; (2) strict clearance at death is impossible while closed attainment is allowed; (3) connectedness is never promoted to path connectivity without local Morse geometry; (4) the older endpoint is fixed before compact intersection; (5) the region may contain younger branches, so the theorem does not replace elder death by first adjacency; (6) a split for each supplied M is not a simultaneous exhaustive barcode. The review must independently assess these points.

I found no must-fix mathematical defect in this frozen draft. This internal conclusion is subject to the separate actual nonauthor review. The proof remains conventional and deterministic; formalization, exact-law almost-sure Morse admission, all-bars/counting and regional collision claims are absent.
