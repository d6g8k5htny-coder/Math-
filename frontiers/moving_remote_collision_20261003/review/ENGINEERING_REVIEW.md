# C107 publication engineering review — repaired packet

**Verdict: ACCEPT for the exact engineering files identified below.**
The initial review/control linkage gap is repaired. No unresolved blocking
engineering finding remains in this reviewed packet. This is an engineering
addendum only: it does not repeat, revise, broaden or add an analytic vote to
`REVIEW.md`. Same-provider organizational independence credit remains **0**;
human review is **NONE**; scientific/register effect is **NONE**.

Reviewer: OpenAI Codex `/root/c107_nonauthor_review`.
Reviewed location: `work/continuation107/checkout`, with the packet at
`frontiers/moving_remote_collision_20261003`.

## Exact engineering target

| File relative to checkout | Bytes | SHA256 |
|---|---:|---|
| `.github/workflows/moving-remote-collision.yml` | 4,126 | `73f6f6daa08f3695c8ec247c99f6822a5dc0fc6734bf4978662516dc76c71171` |
| `frontiers/moving_remote_collision_20261003/verify_sources.py` | 6,441 | `8120c84af4f7341077423ae86ed77252fdfcee310a3ab6a06de6bce2712bfbe1` |
| `frontiers/moving_remote_collision_20261003/test_verify_sources.py` | 8,198 | `8bf806c74861a0ea2ccaa4295d0b3d95c2799453d9723da4a0332d5bc090a5fa` |
| `frontiers/moving_remote_collision_20261003/README.md` | 3,553 | `8252a44ad04478f9086f406bcaf19b23b6cc1d26cfa0e92e714f178b3ad8c324` |

The workflow byte count is independently recorded in the final engineering
receipt. Hashes, rather than mutable checkout HEAD, identify this review.
Any change to these engineering files requires assessing its effect on this
addendum. The frozen proof, source snapshots, author controls and original six
review artifacts are unchanged.

## Initial finding and repair

The initial verifier, SHA256
`87101b1733bb503f5035fc59f15e62e63b9c6ae73edce75ec138a361b7d4ca8c`,
bound five proof/source/author anchors but none of the six copied review files.
The workflow ran `review/independent_controls.py` and checked its reported
PASS and counts. Consequently those reported values could be preserved by
replacing the checker with a script that only printed them; changing review
prose or its receipt likewise escaped custody verification. This was a
publication-linkage defect, not a defect in the frozen analytic argument.
Root independently identified the same gap. The reviewer requested exact
review-file anchors and negative tests for these substitutions.

The repaired verifier has **11 anchors**, including all six original frozen
review artifacts. The new tests substitute the fake PASS-printing checker,
append an unreviewed extension to review prose, and mutate the review receipt;
each must raise a frozen-anchor mismatch. Test fixture setup now creates
parent directories before copying the nested review anchors. The updated
README correctly links the included review and states its same-provider,
conditional scope.

The reviewer verified the repaired behavior directly. In addition to the
maintained tests, a separate temporary-copy experiment changed every one of
the 11 anchored files individually; all 11 were rejected. A byte-matching
symlink replacing the review directory was also rejected. No source or
candidate file was changed by those experiments.

## Verifier and failure behavior

**Source custody:** The six snapshot bytes must satisfy length, SHA256 and
independently recomputed Git blob identity. They are also compared with the
current original source paths. The historical lookup requires an exact
forty-hex commit, verifies that it is a commit object, and requires the exact
`100644 blob <id><tab><path>` tree entry at that cut. Reading the blob and
checking its content identity separately prevents a mere matching pathname
from satisfying the historical claim. Git replacement objects are disabled
both by command-line option and environment override. Missing history fails;
the verifier does not fetch a substitute.

**Paths and symlinks:** Paths must be canonical relative POSIX paths without
NUL, backslash, empty components, dot components or traversal. The file must
be regular and contained within the chosen base. The base and each traversed
path component are checked for symlinks, including byte-identical symlink
substitutions. Historical symlink mode is rejected by the exact `100644`
requirement. The unit tests cover leaf and ancestor symlinks, missing sources,
unsafe paths and a historical symlink object; the review adds a symlinked
review-directory case.

**JSON and schema:** The complete source manifest is a frozen anchor before
parsing, so a self-consistent rewritten manifest cannot silently authorize a
new source. The parser rejects duplicate keys. The verifier requires the
repository, source cut, exact six-key set, deterministic snapshot paths and
source URLs. Byte counts must be positive integers, excluding booleans.
The length/hash/blob comparison validates the source contents. This is a
verifier for one pinned manifest, not a claim to accept arbitrary external
schemas safely. The anchored review receipt and review prose now preserve
their exact binding to the same frozen proof and source manifest.

**Failure propagation and optimization:** Validation uses explicit exceptions,
not removable Python `assert` statements. The CLI returns failure for the
relevant validation, I/O, schema and Git-timeout errors. The maintained tests
use `unittest` assertions, which remain active under `-O`. Normal and optimized
verifier execution both reported six verified sources, 11 frozen anchors,
historical/current source checks, no remote-review authentication and no
mathematical acceptance. All **17 custody tests passed in each mode**.

The maintained suite includes current-source drift, snapshot/proof/control
drift, a rewritten manifest, missing files, wrong historical commit and path,
noncommit/missing objects, symlink tree mode, and a real Git replacement-object
fixture. It now also covers all three reported review-linkage failures.

## Workflow and public explanation

The workflow triggers on the packet, all six original source paths and its
own file, for pull requests and main pushes, and permits manual dispatch.
Checkout requests full history because the verifier consumes exact historical
objects. Checkout, Python setup and artifact upload actions are pinned to
immutable commit identifiers; credentials are not persisted, and permissions
are read-only. This review inspected those pins as part of the workflow bytes;
it did not authenticate their external hosting service.

The normal/optimized matrix keeps both jobs even when one fails. Bash uses
`set -euo pipefail`; the source verifier runs before the maintained tests and
both mathematical control programs. Thus the independently implemented
checker cannot be replaced by a PASS-printing script while retaining a green
custody step. The author output is compared with the frozen expected stdout
under the explicitly pinned Python 3.11.16 version; the independent output is
checked for its expected PASS and counts. A later context step binds the
executed Git HEAD to `GITHUB_SHA`, and the workflow checks for tracked-file
drift. Evidence upload runs even on failure and names the mode and run.

The workflow label and output describe custody/finite checks, not continuum
proof acceptance. The README links the exact proof, source manifest, review
and independent-run record, explains the Python-version line in recorded
stdout, and preserves the missing inner/mixed/persistence interfaces. It does
not claim the verifier authenticates the reviewer or promotes scientific
status.

This is static workflow review plus local verifier/test execution. No GitHub
Actions run was observed or certified by this addendum. Repository-wide
required checks, branch protection and any later PR/merge remain outside this
engineering review.

## Evidence and boundary

`ENGINEERING_RUNS.json`, SHA256
`ac99011d56f5fdd0674a798bace78de7560c160849c4bce9460b4f047ffbe5fe`,
records exact commands, Python runtime, stdout/stderr, candidate hashes,
normal/optimized results and the 12 additional rejection experiments. Test
fixtures were confined to temporary directories beneath this reviewer
directory and removed afterward. The author and independent mathematical
controls were **not rerun** for this engineering request.

The original analytic `REVIEW.md` and `REVIEW_RECEIPT.json` remain unchanged.
Their statement that the publication packet had not yet been reviewed is a
historical statement at their original freeze; this separate addendum records
the subsequent engineering work without rewriting that history. No candidate,
workflow, source, original review artifact or register was edited by this
reviewer. The engineering result does not authenticate a remote reviewer,
supply human/organizational independence, or close any mathematical interface.
