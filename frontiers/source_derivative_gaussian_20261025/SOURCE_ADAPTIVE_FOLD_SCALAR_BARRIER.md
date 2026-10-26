# Adaptive fold scalar barrier — frozen formal continuation

Add AdaptiveFoldScalarBarrier.lean for the normalized scalar step of the completed
conventional adaptive elder proof. Reuse the accepted elder boundary/H0 results;
do not rebuild or restate that topological library. Existing CapFirstExit generic
zero/interpolation results and their verification stay reusable; its old ridge
profile has different endpoints/constants and does not solve this new interface.

On J=[-3/2,3/2], for scalar a, a1, a2 and an antiderivative phi, use explicit
HasDerivAt jets. From a(-1/2)=a(1/2)=0, a2>=1 and the exact gap
phi(-1/2)-phi(1/2)=1/6, derive the quadratic comparison with
q(x)=(x^2-1/4)/2, interior/exterior signs, derivative margins at the two nodes,
the exact lower arm gains5/12, and the left/right potential separation1/4.
Derive the asymmetric ceiling phi(x)<=phi(-1/2) for x in[-3/2,1/2] and the
corresponding floor phi(1/2)<=phi(x) for x in[-1/2,3/2].

A convex core with ConvexOn(a-q) and a second-derivative adapter may share a Prop
bundle. Supply differentiability/continuity needed by the derivative and FTC
arguments explicitly. Use narrow mathlib APIs rather than importing the old full
Mathlib CapFirstExit umbrella or redeclaring its generic interpolation library.
The primitive x^3/6-x/8 gives the two q integrals5/12.

This is a deterministic scalar companion. It proves neither actual ridge existence
nor ambient rectangular boundaries, a physical chart/attained path, elder death,+nor a parent probability theorem by itself. No desired barrier/elder conclusion
is a hypothesis of its final second-derivative theorem.

Producer owns only this new source and scratch evidence. Root owns lakefile,
manifests/commits/publication. Only this new component gets compile/kernel/axiom
checks, meaningful canonical-fold positive control, and the mathematical negative
control rejecting a ceiling on the full symmetric[-3/2,3/2] interval. Record all
failures, snapshots, exact commands/exits and source/artifact bindings. Standard3
axioms only, no admissions/native_decide. Reuse completed applicable checks under
/workspace/AGENTS.md; process/source review is separate from mathematical evidence.
