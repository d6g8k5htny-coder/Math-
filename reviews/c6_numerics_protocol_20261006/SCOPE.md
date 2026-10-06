# C6 numerical-workflow report contracts — AUD-C6NUM-PROTOCOL-01

Dylan Roy — delegated AI engineering. Author: OpenAI / GPT-6 Astra Pro,
`qs-parent-c6num-repair-20261006`, pickup Math-#334/6009005443.
Scientific effect NONE. Same-account/provider organizational-independence credit 0.
This is an engineering repair, not a new mathematical or numerical acceptance.

## Source and ownership

Original source read at `516235290e12decdcd223cfb20928a2d97b824f1`:

| Source | Git blob | Bytes | SHA256 |
|---|---|---:|---|
| workflow | `268ca3fb856b818022784f87bea96d0714c146aa` | 3180 | `06ee6f3beed34eb85ee45e0bbc19ce5e94aeab474a0dd31a492f48b93ca5f78c` |
| coefficients.py | `bd45a9fdecf300111b646644384dcead20c2e529` | 18825 | `bcd63f0806a58a76a85189372bc6eee99fc3847c74dcc34906ef63464a64b97b` |
| RESULTS.json | `2648314f8c11f0637ce301ba76360142a8309e8f` | 4095 | `9c88ea85b6ba08199996c9b5ff74ecd06afc0f458e08c28b4c3af6191f437fcb` |

The original finding belongs to `pr321-followthrough-wrapper-audit-20261006`.
Its report and later authentic-characterization contribution #334/6009064997
remain separately attributed. A crossed later writer pickup6009007450 was
acknowledged in6009140749; earlier6009005443 retains the single production route.
No other writer's implementation or source review is imported here.

## Measured fixed contracts

Local CPython 3.13.5, unchanged checker and RESULTS, both `-B -S` and `-B -O -S`:

| Invocation suffix | Exit | Exact structural report | Stdout bytes / SHA256 |
|---|---:|---|---|
| --check | 0 | `{"mode":"check","passed":true,"scientific_effect":"NONE"}` | 63 / `c54d375daf9298c6a7cc591191dd9e3508b80213ddd24e5320859b429acefff6` |
| --check --mutant cubic-sign | 1 | `{"error":"classifier agrees with the direct critical-point count on the typed domain","passed":false}` | 105 / `b0271f45b76f6b28702624c2e6efce69bbd54e1d2246fdca3d09aa553d9095b0` |
| --check --mutant antiderivative | 1 | `{"error":"[LM] cubic mass 48 k^5 on n = 2","passed":false}` | 62 / `2f60570838650467fb3deeadf8138cf1809f355da1db0511e68cabca7f263ad5` |
| --check --mutant typed-boundary | 1 | Same classifier report as cubic-sign | 105 / `b0271f45b76f6b28702624c2e6efce69bbd54e1d2246fdca3d09aa553d9095b0` |

All eight original characterization processes completed with empty stderr;
all four mode pairs were byte-identical. Actual original stdout uses sorted
keys, default JSON spaces and one trailing newline; the table compacts spacing.
The validator intentionally allows harmless JSON whitespace/key ordering but
requires the complete key set, exact Boolean/string types and exact values.
It rejects duplicate keys, numeric values, nonfinite values, extra or missing
fields, trailing documents, malformed UTF-8, silence, wrong reports, wrong
exits, signals and unexpected stderr. Expectations are fixed source, never
learned from the invocation under test. Timeout/launch exceptions propagate.

The two classifier mutants really share one diagnostic. Output validation
cannot distinguish a malicious replacement emitting that same report. The
unchanged source/membership and consumed-pin guards remain essential. The
helper is not a sandbox or a replacement for those guards.

## Test-first execution and preserved workflow

Twelve full-shell regression methods execute 132 distinct committed synthetic
Git-repository scenarios. Each fixture runs the actual named replay Bash block,
including manifest/source/current-pin checks and final `git diff --exit-code`.
The trace is outside the checkout; children are real processes, not mocks.

Against the ORIGINAL workflow: **100 intended assertion failures, zero errors**;
109 fixtures exit 0 (100 invalid, nine valid/formatting), 23 reject as intended;
952 child invocations. Against the repair: all 132 scenarios behave correctly,
both normal and optimized outer test runs; each run has 594 child invocations,
nine valid/formatting admissions and 123 rejections. These are 132 distinct
scenarios, not 264 kinds of evidence. They are not scientific checker results.

The genuine repaired helper then executes all eight original checker invocations
with the same 900-second child budget. It exits 0 with empty stderr; every
reported output hash/exit equals the independent characterization. The full
numerical packet's source-manifest shell was NOT replayed locally: only the
three authenticated original files and engineering sources were available.
Hosted dedicated execution must verify the actual complete repository tree.
No no-argument generation, Monte Carlo rerun, RESULTS edit, or tolerance change
occurred. The original numerical comparisons remain noncertified.

The workflow's complete manifest/pin preflight and final JSON/Git postflight
are byte-identical. Only the intervening exit-only loop is replaced by the
helper; two focused test invocations and their trigger paths are added. Runtime
3.11.16, action pins, permissions, child 900 seconds and job 20 minutes are
unchanged. Fixtures isolate their own Git settings and disable automatic
maintenance; this is not a repair claim about #321's separate cleanup race.

Python's primary reference contracts are `subprocess.CompletedProcess` and
`json.loads`/`object_pairs_hook`/`parse_constant` in the official Python 3.11
documentation. Numeric and duplicate rejection is explicit, not reliance on
default JSON parsing. No third-party package is introduced.

## Remaining review and integration requirements

This four-file proposal changes no byte in the numerical packet, mathematical
sources, RESULTS, manifests, source maps, other workflows, formal gate, or
scientific-status surfaces. A separate nonauthor engineering review, actual
pinned-runtime dedicated/general checks and eligible expected-head integration
are required. Author local execution is not a review or merge receipt. Old
failed records remain valid historical failures. No full repository local
suite, local Lean execution, independent whole-program alignment or scientific
closure is claimed. Retained in-memory/printed diagnostics do not guarantee raw
child-output persistence after process or filesystem failure.
