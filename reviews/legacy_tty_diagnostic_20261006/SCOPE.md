# Legacy replay: match the captured child's diagnostic width

Dylan Roy — delegated AI engineering. Actual author: OpenAI / GPT-6 Astra Pro,
`legacy-tty-followon-20261006`. Scientific effect **NONE**; shared-account
organizational-independence credit **0**. This is a narrow successor to #330,
not a new review of that repair or a scientific checker change. The original
#330 author and integrator retain their own attribution.

## Source and placement

The predecessor is Math-#330 reviewed head
`f220b70da3c8b21131116d8e91473f5dbf65e446`. Its helper is Git blob
`7f10e0c549c850ab151b55e982eb9fa827a8f8c0`, its test file is
`3dd05f3b26361cab2299b3f646157c9db3de21c9`, and its reference JSON is
`349fc3276ce02ba80aecd7ecc897e37349c65007`. That source review
[6008784871](https://github.com/d6g8k5htny-coder/Math-/pull/330#issuecomment-6008784871)
reported the terminal mismatch as nonblocking for the verified hosted workflow.
This work was separately claimed in
[6008915837](https://github.com/d6g8k5htny-coder/Math-/pull/330#issuecomment-6008915837).
It does not reopen that verdict or write to the parent's branch. Integration is
a separately reviewed follow-on after #330, never a merge into its author branch.

## Reproduced cause

The parent `_unknown_stderr` reconstructs the fixed C6 argparse grammar; the
actual checker is launched with `capture_output=True`. CPython's HelpFormatter
uses terminal columns minus two unless an explicit width is supplied. The
terminal-size helper first accepts a positive integer `COLUMNS`, otherwise it
queries `sys.__stdout__`, and falls back to 80 columns for a pipe.

Thus a parent connected to a 30- or 220-column real terminal can render different
usage bytes from its captured child when `COLUMNS` is absent or invalid. Merely
using the same interpreter does not make their output devices identical. This
is a false rejection of a valid unknown-label diagnostic, not acceptance of an
unrelated crash and not a mathematical counterexample.

Primary references:
- [Python 3.13 terminal-size semantics](https://docs.python.org/3.13/library/shutil.html#shutil.get_terminal_size).
- [Pinned CPython 3.11.16 HelpFormatter](https://github.com/python/cpython/blob/v3.11.16/Lib/argparse.py).

## Smallest repair

Only the C6 grammar renderer now supplies an explicit HelpFormatter width. It
uses the inherited positive integer `COLUMNS`, or 80 when absent, invalid or
nonpositive, then subtracts two just as CPython 3.11–3.13 does. It does not change
the environment, the actual checker, its flags, or its captured output. It does
not execute the checker to learn an expectation, strip usage text, accept a
substring, or relax full-byte stderr comparison.

All other helper functions, original twelve test methods, reference reports,
scientific scripts/RESULTS/manifests/proofs, and workflow source guards remain
unchanged. The added `os` import has no mutation side effect. No new dependency,
workflow, timeout, permission, action pin, or scientific flag is introduced.
The existing three workflow path filters and direct test-file invocations
already discover the new tests.

## Test-first evidence

Actual local runtime: CPython 3.13.5, standard library, Linux. The three new
methods use real pseudo-terminals, not terminal/subprocess mocks. Every case
checks the parent really has a TTY at the requested width and invokes the
unchanged authentic C6 script, Git blob
`91f485f529e09bebcd92f5a8f41d87bf01efc6d6`, with `--mutant unknown`. This exits
before the script's mathematical checks; it is diagnostic execution only.

The cases cover widths 30, 80 and 220 with no override; positive overrides
35, 80, 220 and whitespace-padded 110; and empty, zero, negative and nonnumeric
overrides. Parent and checker each run normally and optimized. That is 38 PTY
cases per outer suite run. All child exits must be 2, stdout empty, and stderr
byte-identical to the independently constructed parent expectation.

Before changing production code, these three methods failed in exactly twenty
subcases in each outer mode, with assertion failures and no errors. After the
fix they passed all 38 cases per mode. The final complete test file passed
**15/15 methods in each outer mode**: the original 201 whole-shell synthetic
fixtures plus 38 new PTY cases, 478 cases across both final runs. Original
crash/silence/wrong-reason/source-tamper rejection and harmless formatting
acceptance remain exercised. Repeated focused runs are not new unique tests.

```sh
python -B -S tests/test_legacy_json_workflows.py
python -B -O -S tests/test_legacy_json_workflows.py
```

The PTY class is explicitly skipped on non-POSIX systems; no Windows PTY result
is claimed. File descriptors close in `finally`, and real subprocesses have
finite timeouts. The unchanged whole-shell fixtures still inherit the parent's
ambient Git-signing limitation; that separate observation is not repaired here.

## Assurance boundary

Local inputs were reconstructed from authenticated public blobs because direct
GitHub DNS was unavailable. This is not a full repository checkout, a genuine
complete ancestor-manifest replay, local Lean execution, or a hosted 3.11.16
receipt. The full-shell fixtures are synthetic; only the new invalid-label
child uses the authentic scientific script. Applicable fresh hosted checks and
a separate nonauthor delta review are required before eligible integration.

The width calculation targets the documented/pinned CPython behavior, not an
unreviewed future argparse implementation. No theorem review, numerical
certificate, new error budget, formal alignment, or whole-program audit closure
follows. The old #330 review does not automatically approve these changed bytes.
