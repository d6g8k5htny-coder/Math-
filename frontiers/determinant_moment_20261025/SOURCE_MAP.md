# DM2 exact source binding and implementation plan

Author: OpenAI/Codex /root, 2026-10-25. Author-side; alignment pending.

Source repository d6g8k5htny-coder/Math-, commit c4eabc1a917ba2c1b96fe4af425cf2a484877c03,
path imports/hardening_ebedb780/P02-LM-002/proof.md.export.txt,
Git blob d1fd7eccd5947cb6c5bf8724a77b7ec1c380a29b,
SHA256 0f8f80922feb603e5b6e530eb885a7819b3a98d90d3c42d60a68259af766f7de.
This is the preserved closure capsule's complete statement/proof, sections 2–3;
its claimed historical reviews are source claims, not reviews of this Lean work.
The uninspected primary GP-DER-071 and CL-AUD-052 are not represented as inspected.

Before proof implementation, freeze the following mathematical contract.
A jet is nine real coordinates q,a,w,z,c40,c31,c22,c13,c04, in that order.
R is exactly 1 plus their nine absolute values; unused z,c13,c04 remain included.
HM and HS are symmetric two-by-two real matrices with the exact entries of section 2:
HM=(-r+r²c40/12, -ar/2+r²c31/12; same, q-rw/2+r²c22/8),
HS=( r+r²c40/12,  ar/2+r²c31/12; same, q+rw/2+r²c22/8).
Negative definite means the quadratic form is strictly negative at every nonzero
real two-vector. W=|det HM * det HS| on the conjunction of HM negative definite
and det HS<0, and zero elsewhere. No typing, nonsingularity, Gaussianity or
independence premise is permitted in the pointwise theorem.

Target `dm2_pointwise`: for every real r and jet j, 0<r and r<=1 imply
W(r,j)^2 <=16*r^4*R(j)^8. Prove stronger untyped bound first, then indicator restriction.
Target `dm2_moment`: on any probability space with measurable jet J, an integrable
R(J)^8 with integral<=M8 implies integrability of W(r,J)^2 and its integral
<=16*M8*r^4 for 0<r<=1. M8 is a bound, not an assumed target conclusion.
The theorem at each r yields the source's uniform family corollary by instantiation.

Parent dependency: formal/MOMENT_TAIL.md and MeasureBridge require an actual
second-moment estimate cW*r^4; this result supplies cW=16*M8 for the exact normalized
jet convention. Remaining: identify the actual endpoint field jets with this
convention; prove the concrete uniform eighth moment and normalizer floor;
construct/identify the same typed Palm law; prove the event tail and good-event
coverage. P0.2, GT5, exact capture, lifetime and persistence conclusions stay open.

Plan: (1) independent packet using unchanged gate.py, pins, scalar baseline and
five rejection controls; no edits to occupied core formal paths. (2) prove exact
factorization, coefficient domination, pointwise and integral results. Check with
pinned Lean v4.34.1/mathlib d13f23b723b8a846827a245b89c10fc7d3f11612.
(3) run source checks, gate tests, fresh build, leanchecker, transitive axiom audit,
and all rejection controls; retain failed executions. (4) freeze exact source
identities, publish draft PR, request actual nonauthor source/statement review.
Report real lineage; author replay never supplies independent alignment.
(5) supply website mapping as candidate evidence, no graph or status promotion.

## Import-only successor after observed memory failure

At proof commit deb28a751f620715ec65d3bd73690905e6fee94d the ordinary fresh build
passed, but leanchecker exited 137; cgroup memory.max was 17179869184 bytes and
memory.events recorded one OOM kill. The failed original build/checker/version logs
remain under evidence/history/umbrella-mathlib-oom/. No successful receipt exists
for that commit. The compiler proof bodies and theorem types are unchanged.

The successor replaces only each of the three modules' `import Mathlib` headers
with exact narrow Mathlib imports. The two copied successor-preservation tests
now require those exact import lists and continue comparing the entire remaining
baseline bodies with the preserved originals plus their documented historical
compiler repairs. Their test-first run failed exactly those two tests before the
import change. Original source bytes remain in formal/ at the base and in the
preserved originals. Gate.py, pins, allowlist and all five rejection controls are
unchanged. This is a new dependency/source candidate, requiring its own execution
and review; neither the previous source review nor successful compilation is
silently rebound to it.
