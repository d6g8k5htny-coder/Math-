# D3 L4 replay coverage and execution custody

Object: R2-D3-L4-EXECUTION-20261005-v1.
Author: OpenAI / GPT-6 Astra Pro, session `d3-l4-round2-audit-20261005`;
Dylan Roy — delegated AI work. Scientific effect NONE. Author will not self-merge.

## Finding and frozen mathematical input

AUD-D3L4-EXEC-001: the green general checks on Math-#304 did not execute the
new coefficient calculation. Run 37383541867 had downstream, formal and aggregate
jobs, but no dedicated `d3-l4` replay. Those successful checks are valid at their
own scope, not numerical execution evidence for this packet.

This is an isolated follow-on to Math-#304. Keep its head
`5059e6d7049c5d65cd1e813545310bc71b86a12f` and all ten files under
`coefficients/d3_l4_anisotropic_20261005/` unchanged while its nonauthor mathematical
read is active. Claude's actual pickup is Math-#304 comment 6004751792; the
acknowledgment and separate engineering scope are comment 6004801985.

The frozen `SOURCE_FILES.json` has SHA-256
`bba2ab2e351b644bbd3eec3b468ab88a2969242db9345f619294d4a8770a2f34`.
It names nine packet payload files and four upstream pins. The driver authenticates
that manifest before reading its instructions, verifies exact directory membership,
all payload sizes/hashes/git blobs, all upstream git blobs, and the additional
upstream SHA-256 when supplied. Symlinks and path aliases/traversals are rejected.
This manifest is a custody root; neither a hash nor a replay is mathematical review.

## Execution contract

The dedicated workflow runs on relevant pull requests and main pushes, with path
coverage for the entire packet, the replay machinery and every named upstream
source. It also allows manual diagnostics. It has read-only contents permission,
no persisted checkout credentials, full-commit action pins and Python 3.13.5.
It does not edit a ruleset, change the general aggregate, or convert a manual run
into required-PR evidence.

Each of the normal and optimized matrix jobs runs the full repository `tests/`
unittest discovery. It then executes the original seven packet tests, full N=128
coefficient calculation, N=4 nonperiodic reference calculation, and source crosscheck.
The main coefficient and reference outputs must match their frozen files byte for
byte, with exit zero and empty stderr. A test process must actually report seven
successful tests; zero collected tests do not count as a pass.

For crosschecks, all interval strings, gamma strings, booleans, keys and other
fields must match exactly. Only the five fields explicitly named
`independent_disk_midpoint_diagnostic` may vary by at most 1e-10 across libm builds.
These are already labeled noncertificate floating diagnostics in the source;
this portability allowance is NOT added to or substituted for any certificate
error. Nonfinite values, including exponent overflow such as `1e999`, are rejected.
Duplicate JSON keys, malformed payloads and wrong JSON types are rejected.

The execution driver, regression file and workflow are checked against the actual
Git HEAD before and after replay. The driver must execute from that checkout.
On GitHub the recorded HEAD must equal GITHUB_SHA, and repository/run/attempt
identity must be present and consistent. A dirty execution tool cannot claim a
clean tested commit. Source pins are verified again after execution.

Commands have bounded timeouts. A crash, wrong exit, unexpected stderr, changed
result or timeout is failure, never a successful negative control. Raw stdout,
stderr and process metadata are retained, including a failed receipt on failures
after evidence-directory creation. Existing evidence directories are not reused
or overwritten. Workflow logs/artifacts survive failures through `if: always()`.
The receipt always leaves scientific acceptance and independent review false.

## Fresh local evidence and limits

Twenty replay-protocol test methods pass under both `-B -S` and `-B -O -S`.
They include real Python processes for success, crash, wrong exit, stderr,
timeout and CLI-failure receipts, plus a temporary real Git repository to test
dirty execution-source rejection. The source fixtures are explicitly synthetic,
not a substitute for the mathematical packet.

The initial 17-method suite failed because the driver was absent. A subsequent
JSON exponent-overflow test and execution-source binding test each failed before
their guards were implemented. An intermediate test-only module-reload exception-
identity error was corrected by caching the imported test module; no numerical
source was changed. These local development failures are retained in the audit
bundle rather than represented as historical successes.

The original N=128 numerical calculation and the source crosscheck were also
freshly run in both modes in this round; their outputs match the delivered files
exactly. This is author-side execution, not the provider-distinct mathematical
review requested on #304.

A complete local repository checkout could not be downloaded in this environment;
therefore complete local repository tests and an end-to-end local run of the new
CLI with all four upstream payloads are NOT claimed. The hosted jobs are designed
to supply that missing execution evidence. Their actual conclusions and tested
commits must be read before integration; configured coverage is not a passed run.

## Review and integration

Review this engineering delta separately from the frozen coefficient proof.
After #304 lands, the follow-on owner must reconcile the base, verify that all ten
packet identities and four upstream pins are preserved, obtain fresh applicable
hosted checks and the scoped nonauthor disposition, then hand off to an eligible
integrator. Do not merge this proposal into the live mathematical-review branch.
No audit verdict, theorem flag, original proof, parent workflow or scientific
status register is changed by this proposal.
