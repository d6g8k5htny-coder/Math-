# Third-order rate workflow: complete child-result contracts

Dylan Roy — delegated AI engineering. Author/executor: OpenAI / GPT-6 Astra Pro,
`pr349-followthrough-third-order-protocol-20261006-r4`, Math-#322 pickup6017164236.
Scientific effect NONE; source/report exposed; organizational-independence credit0.
No author self-merge. This repairs execution validation, not a mathematical proof.

## Frozen predecessor and exact scope

Source cut: `37bd017be7b1a48455fe651977fedc5b7105d188`.

| Source | Bytes | Git blob |
|---|---:|---|
| .github/workflows/third-order-rate.yml |9922|85859c3ca46faf9b6302427de28aa488e1e13aee|
| frontiers/third_order_rate_20261001/r37_check.py |19191|d521770d56d7c59604a949645332820091d69b8e|
| frontiers/third_order_rate_20261001/RESULTS.json |2234|8a2921cfb82deb8962bd45923ba7559401f020e7|
| frontiers/third_order_rate_20261001/SOURCES.json |11327|1cccc27e4aea99a2a861bc32ebb556eba4a2408e|

The original workflow accepts named mutants solely by exit1, unknown M9 solely
by exit2, and ignores baseline stderr. The earlier #322 list identified this
path as a candidate; this work supplies its specific executable counterexample
and repair. No scientific packet, proof, original checker, RESULTS, source map,
formal source, theorem annotation, dependency or scientific register changes.

Only the existing workflow, one dedicated regression, and this scope are changed.
The 7056-byte original dependency/packet preflight and 137-byte final report/Git
postflight remain byte-identical. The tracked-tree regular-file, source hash,
commit/path/blob API, live dependency-PR drift and untracked-path guards are
retained without alteration. Action pins, Python3.11.16, read-only permissions,
600-second numerical-child and10-minute job budgets are unchanged.

## Original checker characterization

Twenty actual native commands completed under local CPython3.13.5: baseline,
M1–M8 and M9 in each normal/optimized Python mode. All ten mode-paired stdout AND
stderr streams are byte-identical. Baseline exactly matches the native RESULTS
blob/SHA256 `7f877f034baaa5b7c8a879a76dd2b825e57869478fdc396897cde1da9bf10ade`.
Named mutants exit1 with empty stderr and full JSON. M9 exits2 with empty stdout
and exactly `unknown mutant label` followed by one LF on stderr.

| Mutant | Failed check; other checks remain present |
|---|---|
| M1, M2, M6, M8 |R1_exponent_ledger (four different complete reports)|
| M3 |R2_lemma_L (also changes equality_instances to41)|
| M4 |R3_refined_B4|
| M5 |R4_typed_window|
| M7 |R6_C_plus_CE_plus_bookkeeping|

The repair compares the entire report, not just that failed-check column.
Its eight fixed canonical JSON SHA256 values were measured from the authenticated
unchanged checker before implementation and cross-checked in both modes. They
are not learned from a currently running child. Duplicate keys, floating or
nonfinite numbers, extra/missing/type-confused fields, trailing JSON, wrong
mutant/reason/info and unrelated failures reject. JSON whitespace and key order
are semantically immaterial under canonical serialization. The baseline keeps
its stricter original byte-equality rule and now requires empty stderr. Every
named output also requires empty stderr and exit1; M9 requires its complete
three-part exit/stdout/stderr contract. Manifest mutants must equal the exact
ordered M1–M8 list before the first child. No predicate relies on Python assert.

The verifier prints each successfully validated child's original stream hashes
and exit; it stops at the first invalid result. Timeout/spawn failures propagate
rather than being mistaken for intended rejection. It is not a hostile-child
sandbox: a malicious executable can print the expected report. Source identity,
process output, mathematical validity and independent alignment remain distinct.
Output-memory/durable-artifact/process-group guarantees are not introduced.

## Test-first whole-shell evidence — initial root-suite publication

The same final ten-method test source was run against the exact original and
repaired workflow in BOTH outer Python modes. Each completed suite runs146
isolated real Git/Bash/Python shell scenarios; no subprocess is mocked. Each
fixture retains a nonempty consumed and cited tracked source, coherent packet
hashes, all20 ordered child slots and final Git-diff validation. Actual children
are synthetic carriers for independently fixed native reports, not numerical
proof computations. Four independent fixtures may execute concurrently; they
share no repo, HOME, trace or process environment. Assertion evaluation remains
in the parent test thread. Optional evidence output is outside fixture repos.

Predecessor: **98 intended assertion failures, zero test errors, each mode**:
94 undesired report admissions, three incomplete/reordered/duplicate mutant
inventories, and one missing regression-wiring assertion. These are finite
protocol counterexamples, not98 independent mathematical defects. Seventeen
valid/formatting cases and the inherited rejecting exit/source/postflight
controls retain their intended outcomes.

Candidate: **10/10 methods,146/146 expected outcomes each mode**, no failures,
errors or skips. Seventeen valid/formatting admissions and129 rejections. All
failed targets stop at the precise ordered prefix; preflight guards run before
children and dirty-tree rejection occurs after all20. Full normal/optimized
suite elapsed times were50.490s/41.571s including launch. The two completed
predecessor calls took79.245s/84.323s. Four completed suites retain584 scenario
records,1168 raw shell streams and8144 child trace entries. These counts overlap
and do not represent independent proofs.

A separate execution of the exact repaired numerical-loop slice ran all20
GENUINE original checker commands again. Every exit and stdout/stderr hash
matches the pre-repair characterization; final acceptance annotation stays
false. That execution deliberately does not claim the original dependency/API
preflight ran locally. Fresh hosted full workflow execution is still required.

An initial sequential full-suite tool call stopped after17 completed cases;
there is no final suite summary, and it is excluded. A streaming-execution tool
attempt was unavailable and launched nothing. The independent fixtures were
parallelized without removing any case or weakening a product timeout. Final
complete paired runs use identical test bytes. Initial partial records and the
local execution-driver histories remain in the owner's evidence delivery.

## Reproduction and integration boundary

```sh
python -B -S -m unittest discover -s reviews/third_order_protocol_20261006 -p test_third_order_rate_workflow.py -v
python -B -O -S -m unittest discover -s reviews/third_order_protocol_20261006 -p test_third_order_rate_workflow.py -v
```

The dedicated review-folder test path triggers its workflow, which runs both commands
unconditionally before its original verification step. There is no new imported
helper/package-resolution dependency. Local development used an authenticated
selected-source repository after direct GitHub DNS failed, not a full upstream
checkout. The local whole-shell fixtures cover merged-source preflights, not
successful live API retrieval; that code is byte-preserved and the hosted job
must supply its own full-source/current-runtime evidence. No local Lean or new
whole-mathematics review is claimed.

Source remains frozen for one actual nonauthor engineering read. Required scope:
exact reports and canonical parser, whole original/new shell and source guard
preservation, meaningful counterfactual outcomes and actual hosted bindings.
A distinct eligible nonauthor/nonreader integrator must later reconcile live
refs/queue/full diff/reviews/threads/dependencies and every applicable check,
use ordinary expected-head merge, and read back the landed tree/push evidence.
This author will not merge. #322 remains open for its broader affected class;
#312, soft-fold, equal-height, factorial budget and all other owners keep scope.

## Placement amendment — review6018064228 / author6018127566

The first published head f8ef14235d9f6ebb71c54a1bd7359fa7f3ef768a placed
the suite at tests/test_third_order_rate_workflow.py. Actual nonauthor xAI/Grok4.7
Cursor bc-72db5126-ae87-41f1-ab3e-4de522fb26a6 confirmed the complete report
contract and independently reproduced the original98 failures and repaired146
outcomes per mode, but returned AMEND for repeated broad-suite workload.

Its original factorial37474577146/job112306533590 remains CANCELLED. Both240
repository methods/mode passed (281.005s/281.295s), but the replay step did not
complete. Its final JSON printed immediately before cancellation at14:04:48Z,
approximately10minutes after job setup. Timing supports budget expiry; the actor
is not identified by the log. Final JSON is not final Git/step success.

The amendment moves ALL ten methods/146 scenarios to
reviews/third_order_protocol_20261006/test_third_order_rate_workflow.py.
ROOT changes parents[1] to parents[2]. Only the wiring method changes its three
path expectations and additionally rejects a duplicate root test. All other
module AST nodes, helpers, fixed reference deltas, nine behavioral test methods,
case inventory, fixture isolation, timeout values and concurrency are identical.
The workflow changes only its new trigger and two discovery commands; its entire
verification shell, including every source/API/control/postflight predicate,
remains byte-identical to the first repair. No factorial workflow/budget change.

Test-first route checks retain one intended wiring assertion in EACH mode against
the original routing, then success after relocation. A separate deliberate root
copy also fails the duplicate-file check. Complete relocated ten-method suites
then run normally and optimized with the same146 scenarios, saved raw streams
and exact stop-order checks; these are new executions, distinct from the initial
584 records. No existing test case was dropped or hidden by a skip.

The dedicated workflow still runs both full modes before authentic numerical
replay, and triggers when either its source test or workflow changes. Avoiding
unrelated broad discovery does not clear the historical factorial cancellation.
A new actual factorial execution on the exact resulting current-base candidate,
including its unchanged full repository suites, authentic replay and Git
postflight within the existing10minute limit, is still required. A bounded
successor source review must reconcile this amendment. No old green result,
path-filter absence or manual-dispatch request counts as that completion.

The base-only inputs from37bd017b to08f86862 are separately reconciled unrelated
LM006 certificate/direct-import changes. They are not new third-order sources.
The author does not self-review or self-merge, and #374's separate budget repair
and all existing integration owners retain their scopes.
