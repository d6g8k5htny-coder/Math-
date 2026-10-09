# Fixed-r inverse-lifetime replay: authenticate negative-control reasons

Dylan Roy — delegated AI engineering. Author: OpenAI / GPT-6 Astra Pro,
`release-integrity-fixed-r-protocol-20261006`; issue322 pickup6014890577.
Scientific effect NONE. Author checks are not nonauthor review or mathematical
acceptance. This is one additional execution-contract repair, not closure of
the entire legacy-wrapper class or of any theorem.

## Original source and defect

The source was read at `98c8fb0c626314f95a08145af61a284482af5f87`.
The complete verifier is blob `22db229cfc2be9d3486d7759c82c50bea83b14e0`
(5190 bytes); inverse.py is `62698d649ff1eba92656fb555bf57d603f2bbc37`
(6501 bytes); manifest is `dd68713445e08f113f6e93fb54372b691486bab8`.
The baseline is exactly 516 bytes, SHA256
`46ccc0f5e2d8cba11040ca1bc617e9e99e54ca7b19ac85ff4091e2601104efeb`.

The original verifier checks baseline bytes and stderr, authenticates a full
packet manifest and historical Git sources, and runs both interpreter modes.
However, its six named mutants are credited solely for exit1, and the unknown
label solely for exit2. Unrelated errors can therefore be accepted as intended
negative controls. This is an execution-protocol defect, not a counterexample
to the fixed-separation inverse-lifetime theorem.

## Small bounded change

Only verify.py's main function changes among its existing function bodies.
A fixed independent six-label/reason map and validate_rejection are added.
The complete ordered mutant tuple must equal the independent map before any
child execution. Each named negative result must have exit1, empty binary
stderr, and exactly the two JSON fields `error` and Boolean `passed:false`,
with the exact expected reason. Duplicate keys, invalid UTF-8/JSON, extra or
missing fields, nonfinite constants, false/int/null confusion and trailing
objects are rejected. JSON whitespace and key ordering remain immaterial.

The unknown-label result requires exit2 and empty stdout. The entire usage and
error diagnostic is matched after ASCII-whitespace normalization. Exactly two
choice-list spellings are supported: Python3.11's quoted labels and Python3.13's
unquoted labels. Both retain every label, its order, the option, invalid value,
and reason. Arbitrary diagnostic text, changed choices or extra stdout/stderr
is not accepted. No extra production subprocess learns expected child output.

Baseline matching, original 45-second child and Git budgets, 120-second unit
suite budget, source/inventory functions, historical parent pins and final
inventory check are unchanged. Exceptions still abort execution. MANIFEST.json
changes only the three identity fields for verify.py; every other entry and
the historical NONAUTHOR_REVIEW_OPEN field remain unchanged.

The existing dedicated workflow adds one path trigger and invokes the new root
test file in both modes. Its action pins, Python3.11.16 pin, read-only
permissions, complete-history checkout, exact parent fetch, original genuine
verification command and final clean Git check remain byte-preserved.
No scientific proof, inverse.py, RESULTS.json, SOURCES.json, old packet test,
formal source, dependency pin, scientific register or other workflow is edited.

## Actual test-first evidence

Local runtime: CPython3.13.5 / Git2.47.3 on Linux, standard library only.
Complete original inverse.py bytes were authenticated before execution.
Sixteen genuine native invocations (baseline, six mutants, unknown; both modes)
produced eight byte-identical stdout/stderr pairs and the native baseline hash.
A further sixteen genuine invocations passed the repaired validator's contracts;
the scientific checker itself remained unchanged.

The initial seven-method suite has 92 independent full-verifier scenarios.
Against the exact original verifier it completed in BOTH outer Python modes
with 65 intended assertion failures, zero test errors. It exposes wrong-reason
admission, not merely missing implementation. Complete raw logs and per-case
child sequences are retained in the requester delivery.

The initial repair passed those same 92 scenarios per mode. Before publication,
official pinned3.11 argparse source exposed its quoted-choice spelling. A new
four-scenario compatibility method failed the first repair by two intended
assertions, then passed after accepting the two complete fixed diagnostic
forms. A separate workflow-wiring test failed the original YAML by one intended
assertion before the trigger and regression commands were added.

Final frozen tests: NINE methods, 96 unique full-verifier scenarios in EACH
normal and optimized outer mode, all expected outcomes correct: seven valid
or harmless-formatting admissions and 89 rejections, with 772 checker children
per mode. Each verifier itself runs normal and optimized child stages until
the specified failure; stopping prefixes and unit-suite invocations are checked.
The tests use actual disposable Git histories, full source/inventory guards,
real test discovery and real checker child processes. Four workers use disjoint
temporary roots; no subprocess is mocked. They do not replace the scientific
checker with a fake and then claim a genuine mathematical replay: the full
verifier scenarios are explicitly synthetic execution-contract fixtures.

Synthetic fixture commits have command-local maintenance and signing disabled;
system/global Git config is excluded only from those child environments. No
persistent real repository or user settings change. Original packet tests are
left intact, including their existing Git-fixture behavior.

Some early sequential/parallel whole-suite invocations were interrupted by the
tool command envelope near30seconds despite longer requested outer limits.
Their partial logs have no completed verdict and are excluded. The completed
original and final runs described above retained all selected cases. An initial
file-ownership error before a Python retry launched no test; it is not a test
failure or a pass. No assertion was removed to resolve either tooling issue.

## Scope of assurance and required next step

These local executions use authenticated selected source, not a complete
repository checkout or the genuine historical parent proof. The complete
source-bound packet replay and its old tests must actually execute in the
dedicated hosted workflow at the pinned runtime. General/required checks and
all other path-triggered jobs must also pass at their exact tested candidate.
No local Lean execution or new independent mathematical alignment is claimed.

An actual bounded nonauthor engineering review must check the carrier contract,
complete inventory, genuine outputs, both diagnostic spellings, unchanged old
source/test/pin boundaries and meaningful predecessor failures. Then a separate
eligible nonauthor/nonreader integrator must reconcile live refs, current
findings and all applicable execution before ordinary expected-head merge,
followed by landed/push readback. No author self-merge or old-receipt rebinding.

This does not make a hostile executable safe, prove that an arbitrary program
failed internally at the advertised assertion, limit captured output memory,
supply durable timeout logs or eliminate every ambient Git configuration issue.
A malicious child can intentionally print an expected diagnostic. Source
identity and trusted execution remain separate boundaries.

## Reproduce

From an exact checkout:

```sh
python -B -S tests/test_fixed_r_replay_protocol.py
python -B -O -S tests/test_fixed_r_replay_protocol.py
python -B -S frontiers/fixed_r_inverse_lifetime_20260930/verify.py
```

The last command requires the unchanged exact historical Git parent. Do not
silently substitute --local-only and call it a historical-source replay.

## Primary references inspected

- Python3.11 json: object_pairs_hook and parse_constant,
  https://docs.python.org/3.11/library/json.html
- Python3.11 argparse error exit/usage contract,
  https://docs.python.org/3.11/library/argparse.html
- Exact pinned argparse choice rendering, `_check_value`,
  https://github.com/python/cpython/blob/v3.11.16/Lib/argparse.py

These explain library behavior; the actual unchanged checker outputs and
source-bound tests establish this packet's expected diagnostics.
