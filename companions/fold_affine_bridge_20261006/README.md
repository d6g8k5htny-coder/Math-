# Exact fold derivatives and affine coordinates

Scientific effect: NONE. Author: OpenAI, `fold-affine-bridge-author-20261006`,
exact model/session UNKNOWN, organizational-independence credit 0. This is
Dylan Roy's delegated AI work, not his personal reading. The author is
source-exposed and will not supply independent alignment or integrate this work.

Reservation and source-bound statement contract:
- https://github.com/d6g8k5htny-coder/main/issues/275#issuecomment-6027534463
- https://github.com/d6g8k5htny-coder/main/issues/275#issuecomment-6027637137
- https://github.com/d6g8k5htny-coder/main/issues/275#issuecomment-6027667849
- Own continuation: https://github.com/d6g8k5htny-coder/main/issues/275#issuecomment-6027692808

## Publication phase

The initial commit f83bb592 was an intentionally empty test-first stub.
Dedicated run37549682550/1 at merge checkout
fcf5c6ba05d15323f10d8e555c9a3e125a079d8b passed both full Python modes, the
unchanged primary kernel gate and the stub module build, then Contract.lean
failed on absent new declarations (exit1). Its original artifact11451893422
is retained,48344bytes/SHA2566060fc6658508d97b544290742c759512513f9216f27ae04bce8619ba7da41bf.
Proof bodies are supplied only after that observed failure. Their compilation,
current-source kernel evidence and independently authenticated statement/source
alignment remain separate pending stages. Failed attempts stay in the PR record. The first proof-source head48544ac5
failed candidate compilation in37551282778/1 after the full suites and unchanged
core passed: pointwise function equalities needed explicit extensionality, one
tactic was unreachable under warnings-as-errors, and adjacent absolute-value
bars/multiplication formed the Lean |* token. Original artifact11453177336
(45870bytes, SHA25686036e287059a5d8540bad534ae1a8348e4cd5bd7075b3a0571e9b6717cfc0c5)
is retained. The successor repairs these source issues without changing target
hypotheses; candidate contract/axiom/recheck/negative stages were unrun there.
The next exact run37552472542/1 at ea86cd53 failed only on unreachable
tactics in unused extensionality branches and a trailing ring after field_simp
had closed the absolute-gap goal. Artifact11453480961 retains that failure
(23452bytes, SHA256a51829d0a2bbb1666bd859abd10f2fe71b7d08e47224fea688f9d1665e2a1b73).
The successor removes those dead tactics without disabling any linter or
changing theorem statements. Its later stages still require actual execution.

## Exact mathematical contract

All parameters are real. Reuse `ResearchFormalCoreR1.foldPotential s x`,
F_s(x)=-x^3/3+s^2*x, and its existing `ec005_fold_gap` subtraction theorem.
New definitions only: G(y)=c*F_s(a*y+b), plusPoint=(s-b)/a,
minusPoint=(-s-b)/a, physicalSeparation=2*abs(s)/abs(a).
Plus/minus labels name the source coordinate, not spatial order or extrema.

The 29 target declarations are explicitly inventoried in replay.py and
SOURCE_FILES.json; the four definitions are audited too. Contract.lean is an
exact-type consumer of every target. It retains all quantifiers/hypotheses:

- Canonical HasDerivAt witness and derivative s^2-x^2, second derivative -2*x,
  and complete critical set x=s or x=-s. Both Hessians are nonzero iff s is
  nonzero; at s the curvature is negative iff s>0 and at -s positive iff s>0.
- Affine first/second derivative witnesses and formulas
  c*a*(s^2-(a*y+b)^2) and -2*c*a^2*(a*y+b), including zero parameters.
- With a,c nonzero, full critical set plusPoint/minusPoint; source-coordinate
  identities and Hessians -2*c*a^2*s / 2*c*a^2*s. Nondegeneracy iff s is
  nonzero; source-labelled maximum/minimum classification depends on c*s.
- Orientation plusPoint-minusPoint=2*s/a. Absolute separation equals r and
  is nonnegative; for a nonzero it vanishes exactly when s=0.
- With a nonzero, invoke ec005_fold_gap to transfer the signed gap
  c*(2*s)^3/6 and absolute gap abs(c)*abs(a)^3*r^3/6. The algebra allows c=0;
  the isolated-pair interpretation requires c nonzero.
- Exact point increments -c*(a*h)^2*(s+a*h/3) and
  c*(a*h)^2*(s-a*h/3). For a,c,s nonzero and
  0<abs(h)<abs(s)/abs(a), multiplying by c*s gives negative/positive signs,
  certifying strict local extrema with the stated labels.
- At s=0, the two labels coincide at -b/a, both derivatives vanish, and the
  increment is -c*a^3*h^3/3. For a,c,h nonzero, the two increments at h and
  -h have negative product, explicitly witnessing the stationary crossing.
  If a=0 or c=0 the function is constant instead, with every point critical.

Positive controls include arbitrary b, signed s/a/c, s=0, and s=1,a=2,c=3:
r=1, absolute gap4 and labelled Hessians -24/+24. Three separate false
propositions must produce the exact named unsolved-False-goal diagnostic:
omit the affine scale factor; assert nondegeneracy at s=0; retain the s>0
curvature label at s=-1. Missing imports, toolchain failure, other diagnostics,
stderr, wrong exit status or timeouts do not satisfy this negative gate.

## Sources, execution and limits

Frozen source base: Math- 34618d0d032f4361c1ec163f3b4cfd6ad01ab814.
Consumed AlgebraV2 blob: a8b42432cc65095b37750b24ea2d617dd437092a.
Unchanged primary formal tree: d7422c6b1acbf3e20c75a1ed7fc13fc30125ec14.
The only source import is ResearchFormalCoreR1.AlgebraV2, including its Mathlib
import. No duplicate canonical fold definition or subtraction proof is added.
Lean remains leanprover/lean4:v4.34.1; mathlib remains
 d13f23b723b8a846827a245b89c10fc7d3f11612; lake configuration/manifest untouched.
Driver patterns reuse the inspected d2_square_schur companion, with separate
stdout/stderr, bounded children and an output build directory. The unchanged
primary gate's exact-hash axiom auditor is reused, not replaced by this driver.
The small explicit inventory is not the RF312 general declaration scanner.

From the repository root:

    python3 -B -S companions/fold_affine_bridge_20261006/test_contract.py
    python3 -B -O -S companions/fold_affine_bridge_20261006/test_contract.py
    python3 -B -S companions/fold_affine_bridge_20261006/replay.py source
    python3 -B -S companions/fold_affine_bridge_20261006/replay.py controls
    python3 -B -S companions/fold_affine_bridge_20261006/replay.py execute

Execute requires the existing pinned toolchain already available. Its fresh
output directory defaults to .lake/fold-affine-bridge-evidence. It runs the unchanged primary kernel gate, then candidate warnings-as-errors
build, exact-type consumers, transitive axiom/type audits, fresh leanchecker
and reason-specific controls. Both full root/formal Python suites and companion
tests in normal and optimized modes remain mandatory before any final receipt.
This early-positive ordering changes failure latency only; unrun stages never
inherit earlier results. The companion .olean
is written only under the separate output/build directory. Every child keeps
raw stdout/stderr/status, including failure and timeout. Receipt creation is
last and cannot turn a partial run into success. The dedicated read-only
workflow preserves original outputs on success or failure. Required aggregate
checks and current tested checkout remain separately binding before integration.

No local Lean execution was available when this stub was prepared. Local
Python arithmetic is finite diagnostic evidence only. A configured workflow
is not an executed result; the primary package does not check this companion.
No nonlinear/approximate chart, random-field construction, stochastic or Palm
realization, persistence pairing, probability, multiplicity or parent theorem
is claimed. There is no primary target registration, formal-manifest change,
scientific-status promotion or transfer of older review acceptance.
