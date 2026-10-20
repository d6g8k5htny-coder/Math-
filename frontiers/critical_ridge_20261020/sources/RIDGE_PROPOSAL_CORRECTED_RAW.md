# Direct ridge route to critical closed-superlevel neighborhoods — paper proposal V1

Actual Root author chat01a11cbf-068d-7102-861e-75814e715c98,20October2026. UNREVIEWED nonexclusive paper assistance for the prospective critical-boundary leaf Math487/6291433200. It is not an accepted formal source claim, Lean proof, compilation, kernel receipt or replacement for the actual C298 engineering review. No local project program is requested or run.

## Literal source and proposed theorem

C297 exact sourcehead363a533e8e0a1308781d88697f46479e327dd344, frontiers/regular_superlevel_geometry_20261020/project/Lifetime.lean defines IsSmooth as all finite ContDiff, IsCriticalPoint as fderiv=0, and HessianHasInertia by complementary subspaces V,W, negative definite on V and positive definite on W. It does NOT require the subspaces to be Hessian-orthogonal. Root freshly fetched the exact raw source and inspected these definitions. C297's accepted regular/interior neighborhood result does not cover an actual critical boundary point. C293 isolates critical points; C294's quotient closed-death-level LPC remains an explicit premise. The actual source lead is currently separately occupied with C298's engineering review; no vacancy or successor acceptance is inferred.

Proposed mathematical theorem: for a finite-dimensional real Euclidean E, smooth f near p, Df(p)=0, and the literal symmetric Hessian admitting such a complementary definite split, the subtype S={z:f(z)>=f(p)} has a basis of relatively open path-connected neighborhoods at p. Combining this pointwise result with the existing regular/interior theorem would yield closed-superlevel LPC at every point for a literal smooth Morse function. Actual quotient transport and C294 consumption still require their own exact joins.

This route uses the ordinary smooth implicit function theorem on the negative partial gradient and elementary convexity, rather than assuming a full function-level Morse normal-form chart. Those classical results must be formally derived from pinned Mathlib or explicitly remain missing proof obligations; no hidden chart/LPC premise is discharged by naming them.

## Proposed direct proof

Translate p=0 and subtract f(p). Via the finite-dimensional complementary linear homeomorphism W×V -> E, write F(x,y)=f(x+y)-f(0), x in positive W and y in negative V. The C2 Hessian is symmetric; its restriction C to V is negative definite and hence an invertible map V -> V*. The implicit function theorem applied to partial_y F(x,y)=0 gives a smooth local map g:W -> V, g(0)=0, with partial_y F(x,g(x))=0. Empty negative dimension is allowed: V={0}, g=0 and the partial-gradient equation is trivial.

Let h(x)=F(x,g(x)). Then h(0)=0 and Dh(0)=0. For w in W, put v=Dg(0)w. Differentiating the ridge equation gives
H(w+v,z)=0 for every z in V,
so H(w,v)=-H(v,v). The chain rule at the critical point gives
D2h(0)[w,w]=H(w+v,w+v)=H(w,w)-H(v,v)>0 for w!=0.
The final strict inequality follows from positive definiteness on W and nonpositivity on V; no cross-block orthogonality is assumed. Consequently, after shrinking to a convex W ball, h has uniformly positive Hessian and h(x)>=0 there. This also covers W={0}, where h is the single value0 and the strict-positive condition is vacuous.

Independently, continuity of D2F and finite-dimensional compactness yield a product neighborhood of(0,0) on which the V-direction Hessian is uniformly negative definite. Thus for fixed x every y segment inside that neighborhood is a concavity segment for F(x,y). Shrink the W ball and choose b>0 so that for every x in that ball the entire tube y=g(x)+v, ||v||<b, stays inside this product neighborhood. This can be arranged by continuity of g and g(0)=0.

Define the ambient open tube
U={x+g(x)+v : ||x||<a, ||v||<b}, x in W,v in V.
It is open: its coordinate inverse is x=projection_W(z), v=projection_V(z)-g(projection_W(z)), with continuous complementary projections. It contains0. By shrinking a,b and using continuity, such tubes lie inside any prescribed ambient neighborhood of0.

For z=x+g(x)+v in U intersect S, use two paths. First t -> x+g(x)+(1-t)v,0<=t<=1. It remains in U. Concavity of the V fiber gives
F(x,g(x)+(1-t)v) >= (1-t)F(x,g(x)+v)+t F(x,g(x)) >=0,
because the first endpoint lies in S and the ridge value h(x)>=0. The second path t -> (1-t)x+g((1-t)x) remains in U and S since its value is h((1-t)x)>=0. Their concatenation connects z to0 within U intersect S. Thus U intersect S is path connected and relatively open, and the arbitrary-neighborhood containment supplies the required basis.

For a local maximum W={0}, the same argument actually gives U intersect S={0} from strict fiber concavity. For a local minimum V={0}, U intersect S=U after shrinking, by h>=0. In dimension0 both are the singleton case. These cases must be explicit in a Lean implementation; no nonzero unit sphere may be assumed in a zero-dimensional subspace.

## Proposed formal dependency split and boundaries

A. Complementary subspace continuous coordinates and dual/Riesz identification, plus symmetry of the actual iteratedFDeriv Hessian.
B. Smooth negative partial-gradient map with invertible y derivative; existing implicit-function theorem with an explicitly constructed derivative equivalence.
C. Differentiated ridge equation and positive reduced Hessian, with continuous uniform coercivity on finite-dimensional balls.
D. Concavity of fibers and h(x)>=h(0), proved via real one-dimensional restriction/integrated derivative or existing convexity lemmas.
E. The open tube, its two literal subtype paths, their concatenation and neighborhood-basis conversion.
F. Actual torus covering restriction/relative-subtype local homeomorphism, global regular/interior/critical case split, then replacement of C294's explicit hclosedLPC. These are subsequent source joins, not supplied by A–E alone.

Please independently seek counterexamples/gaps: complementary but nonorthogonal subspaces; either subspace zero; need uniform rather than pointwise signs; domain of implicit g and of every path; smoothness needed for reduced Hessian; relatively open basis versus only one connected set; actual C2 assumptions rather than arbitrary total fderiv; critical level versus nearby levels; torus transport. Return ACCEPT_SCOPED_PAPER_ROUTE, AMEND or precise HOLD. The desired result is a source-bound route or failed-route diagnosis, not an assumed generic chart lemma.

This is conventional paper mathematics with an unimplemented formal dependency map. No original-bar bijection, elder/once-counting, full quotient theorem, all-small-bars converse, field-first sampling, density asymptotic, scientific acceptance or master-goal completion follows yet. Full research goal remains ACTIVE_UNMET. Source-exposed Root coauthor; distinct actual nonauthor review required; same-provider/org0/blind0/human0. Only source read/hash/JSON custody is allowed; no project/compiler/test/execution.

