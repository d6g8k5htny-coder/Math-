# C7 total-bounded workflow protocol repair

Dylan Roy — delegated AI engineering. Actual author OpenAI / GPT-6 Astra Pro,
`c7-protocol-followthrough-20261006-r3`; pickup Math-#322/6015371102.
Scientific effect NONE; organizational-independence credit 0. No author self-merge.

## Scope and design

This changes only the existing C7 workflow and adds its focused regression file
and this note. No new helper or validation framework. The mathematical packet,
its checker, proof, erratum, results, manifest and reading notes remain unchanged.
The original workflow ignores baseline stderr and accepts M1/M2/M3 solely on
exit 1. The replacement also requires empty stderr and each independently
measured exact stdout line, including its single LF. Baseline stdout remains
byte-exact against the original RESULTS.json. No substring, whitespace trimming,
JSON coercion or child-generated oracle is used. The existing eight-command
inventory, inherited working directory, 300-second subprocess budgets,
10-minute job budget, action/Python pins and read-only permissions remain.
Launch and timeout exceptions are not caught or suppressed. Successful command
records now print stage, flags, exit and stream hashes. The added regression step
runs before the original source-check/replay step, in both Python modes.

## Authenticated original sources

Source cut: `11f9127f00ce922e5d39b0da42af76134eb78a21`.

| Path | Bytes | Git blob |
|---|---:|---|
| .github/workflows/c7-total-bounded.yml |2662|3d025b1aefdaaf43a62acbbf2b318bfc8b687ecf|
| frontiers/c7_total_bounded_20260929/exponent_check.py |7736|0f9d4cf4b7f2d79bb5fa338fc8e1bc77506dd8c9|
| frontiers/c7_total_bounded_20260929/RESULTS.json |1056|52df86b1712f22d629a5e630aa199dca3f6d4b9e|
| frontiers/c7_total_bounded_20260929/SOURCE_FILES.json |unchanged|9da912e8db14792d841593e08a518743a51c9dd6|

Native eight-case characterization used unchanged checker bytes on local
CPython 3.13.5. Each baseline/M1/M2/M3 stdout and stderr matched between normal
and optimized child modes. Baseline SHA256 is the existing manifest's
`dd5c89362090bd2ff62080e363b1b54a79ed3fcfb28f93b24d182ecd6ec20777`.
The failure lines are:

- M1: `FAIL T_pieceB1_7_12` plus LF, exit 1, empty stderr.
- M2: `FAIL T_threshold_is_r_equals_k` plus LF, exit 1, empty stderr.
- M3: `FAIL K_62prime_layer_integral_exact` plus LF, exit 1, empty stderr.

Eight further genuine commands through the changed process-loop extraction
matched all original exits and stream hashes. That extraction omits the packet
preflight and is explicitly a selected-source replay, not a complete six-file
packet authentication. Actual full-packet execution must come from dedicated CI.

## Test-first evidence

The unchanged published regression file has seven methods and 107 distinct
whole-shell scenarios. Real temporary Git repositories, actual Bash and child
Python processes, no subprocess mocks. Each synthetic packet is committed with
its own correct manifest before any intentional corruption. An external trace
must reach the intended stage and stop there; five source guards stop before
children; the dirty-tree control reaches all eight commands before Git rejects.
Synthetic signing and maintenance are disabled only on its disposable commit;
no real user Git configuration, signer or credential is modified.

Full original runs in BOTH outer modes: 75 intended assertion failures, zero
errors, 107 fixture records and 722 child commands each. Of the 74 noncanonical
output admissions, 18 concern formatting alone (missing LF, CRLF, extra LF);
56 concern crashes, silence, wrong/noisy output, wrong reasons or stderr. The
remaining assertion is absent regression wiring. The valid fixture passes, and
32 existing exit/source/dirty-tree controls reject. These categories do not
represent 74 independent bugs or 74 semantic theorem failures.

Full repaired runs in BOTH outer modes: seven methods OK, all 107 expected
outcomes, one valid admission and 106 correct rejections, 496 child commands per
mode. Same test bytes/scenario keys in all four runs: 428 fixture records and
2436 child invocations total, not 428 distinct scenarios. One initial normal RED
attempt hit the external tool deadline; its partial records are retained and
excluded. All four counted runs completed without partitioning or skips.

## Preserved boundaries and remaining requirements

The original source preflight (including import, 972 indented bytes) has SHA256
`7b6f4f2b7e841fedc5e5dd2fd1f3aae62ad6a142900ca7dc46d804afb093113d`.
The original final JSON/Git postflight (135 bytes) has SHA256
`502344625c8ab44b2065a9ffda2f0acb2cb5d8c7ee1974169a6baf2a7a31d490`.
Both remain byte-identical. Existing manifest consumption metadata is not newly
asserted to be an executed dependency check. No unknown-label control is added:
this proposal preserves the original M1/M2/M3 invocation scope, not a new CLI.

A distinct nonauthor engineering review, actual dedicated/general/applicable
current-candidate checks, and a separate eligible guarded integration are still
required. Historical evidence is not rebound to a later base. #322 remains open
for other wrappers. Direct Git clone failed DNS; there is no full local checkout,
full local repository suite, local Lean, live dependency-fetch or mathematical
re-review claim. This is not a hostile-source sandbox, output-memory bound,
durable-output guarantee, theorem acceptance or global audit clearance.
