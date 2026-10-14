#!/usr/bin/env bash
# Replay of the torus-filtration companion: TorusTopology and ClosedSuperlevel (C254), the registered
# SuperlevelBar (C263) and OrdinaryH0 (C264) successors, the owner-authored OrdinaryH0Controls (C264 owner
# task item 4) and the owner-authored SuperlevelBarField (the C263 Field adapter), which imports the statement
# packet's Specifications.Field, compiled here first from its pinned bytes (check.py EXTERNAL_INPUTS). It runs
# neither formal/gate.py nor the formal tests: the companion consumes only the pinned toolchain, lakefile and
# dependency lock from formal/, and its evidence is kernel-checked declarations, not alignment or acceptance.
set -euo pipefail
# The outer Python mode is the one named on each command line below, never an ambient PYTHONOPTIMIZE (C262 G1).
unset PYTHONOPTIMIZE
# leanchecker over the five modules peaked at about 8.4-8.7 GiB resident at two threads and exceeded a 13.36 GiB
# memory limit at four (2026-10-11, this lane); over the six, sampled peaks of 8.64 and 9.31 GiB in two runs at two
# threads (2026-10-12); default to the hosted job's two threads unless the operator sets otherwise.
export LEAN_NUM_THREADS="${LEAN_NUM_THREADS:-2}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SIDE="$ROOT/companions/torus_filtration_20261011"
OUT="$ROOT/.lake/torus-filtration-evidence"
# Build output of the external Field module: outside the source tree and outside the evidence directory.
SPEC_OUT="$ROOT/.lake/torus-filtration-spec"
cd "$ROOT"
test ! -e "$OUT"
test ! -e "$SPEC_OUT"
mkdir -p "$OUT" "$SPEC_OUT/Specifications"
python3 -B -S "$SIDE/check.py" source > "$OUT/source.json"
python3 -B -S "$SIDE/test_torus_filtration.py" 2>&1 | tee "$OUT/tests.log"
python3 -B -O -S "$SIDE/test_torus_filtration.py" 2>&1 | tee "$OUT/tests-optimized.log"
python3 -B -S "$SIDE/check.py" emit "$OUT"
export TORUS_SIDE="$SIDE" TORUS_OUT="$OUT" TORUS_ROOT="$ROOT" TORUS_SPEC_OUT="$SPEC_OUT"
cd "$ROOT/formal"
lake env bash <<'INNER'
set -euo pipefail
# The fresh Field build comes first: it holds only Specifications/Field.olean and did not exist before this run, so
# it shadows nothing, and no other Specifications/Field.olean (say, an untracked one in the companion directory) can
# shadow it.
export LEAN_PATH="$TORUS_SPEC_OUT:$TORUS_SIDE:${LEAN_PATH:-}"
export LEAN_SRC_PATH="$TORUS_SIDE:${LEAN_SRC_PATH:-}"
# Runtime guard: the running Lean and every installed dependency (`<name> <HEAD> <clean|dirty>`, clean meaning
# `git status --porcelain --untracked-files=normal` prints nothing) are observed before the first Lean execution and
# again after the last one (toolchain-final.log, packages-final.log); check.py finish requires both observations.
# Each git result is taken by a plain assignment, so a failing git aborts the replay under `set -e` (a command
# substitution inside printf's arguments would not).
observe_packages() {
  local log="$1" pkg name head porcelain state
  : > "$log"
  for pkg in "$TORUS_ROOT"/formal/.lake/packages/*/; do
    name="$(basename "$pkg")"
    head="$(git -C "$pkg" rev-parse HEAD)"
    porcelain="$(git -C "$pkg" status --porcelain --untracked-files=normal)"
    if [ -z "$porcelain" ]; then state=clean; else state=dirty; fi
    printf '%s %s %s\n' "$name" "$head" "$state" >> "$log"
  done
  cat "$log"
}
lean --version > "$TORUS_OUT/toolchain.log"
cat "$TORUS_OUT/toolchain.log"
observe_packages "$TORUS_OUT/packages.log"
run_lean() {
  local label="$1"; shift
  local code=0
  "$@" >"$TORUS_OUT/$label.log" 2>&1 || code=$?
  printf '%s\n' "$code" >"$TORUS_OUT/$label.status"
  cat "$TORUS_OUT/$label.log"
  test "$code" -eq 0
}
# The statement packet's Field module, with the packet's own leanOptions (autoImplicit false) and without
# warnings-as-errors: it is the packet's source, not the companion's; only SuperlevelBarField imports it.
run_lean build-spec-Field lean -DautoImplicit=false --root="$TORUS_ROOT/specifications/lean_statements_20261010" -o "$TORUS_SPEC_OUT/Specifications/Field.olean" "$TORUS_ROOT/specifications/lean_statements_20261010/Specifications/Field.lean"
run_lean build-TorusTopology lean -DwarningAsError=true --root="$TORUS_SIDE" -o "$TORUS_SIDE/TorusTopology.olean" "$TORUS_SIDE/TorusTopology.lean"
run_lean build-ClosedSuperlevel lean -DwarningAsError=true --root="$TORUS_SIDE" -o "$TORUS_SIDE/ClosedSuperlevel.olean" "$TORUS_SIDE/ClosedSuperlevel.lean"
run_lean build-SuperlevelBar lean -DwarningAsError=true --root="$TORUS_SIDE" -o "$TORUS_SIDE/SuperlevelBar.olean" "$TORUS_SIDE/SuperlevelBar.lean"
run_lean build-OrdinaryH0 lean -DwarningAsError=true --root="$TORUS_SIDE" -o "$TORUS_SIDE/OrdinaryH0.olean" "$TORUS_SIDE/OrdinaryH0.lean"
run_lean build-OrdinaryH0Controls lean -DwarningAsError=true --root="$TORUS_SIDE" -o "$TORUS_SIDE/OrdinaryH0Controls.olean" "$TORUS_SIDE/OrdinaryH0Controls.lean"
run_lean build-SuperlevelBarField lean -DwarningAsError=true --root="$TORUS_SIDE" -o "$TORUS_SIDE/SuperlevelBarField.olean" "$TORUS_SIDE/SuperlevelBarField.lean"
run_lean build-TorusFiltration lean -DwarningAsError=true --root="$TORUS_SIDE" -o "$TORUS_SIDE/TorusFiltration.olean" "$TORUS_SIDE/TorusFiltration.lean"
run_lean positive lean -DwarningAsError=true --root="$TORUS_OUT" "$TORUS_OUT/Positive.lean"
run_lean axioms lean -DwarningAsError=true --root="$TORUS_OUT" "$TORUS_OUT/Audit.lean"
run_lean types lean -DwarningAsError=true --root="$TORUS_OUT" "$TORUS_OUT/Types.lean"
run_lean census lean -DwarningAsError=true --root="$TORUS_OUT" "$TORUS_OUT/Census.lean"
# Kernel replay of the companion modules' own declarations against the cached, prebuilt dependency
# .oleans (30 s at 2 threads locally for the three C254 modules, 53 s for the five, 56 s for the six, 75 s with the
# `lake env` start-up). Since SuperlevelBarField the external Specifications.Field, compiled above, is replayed too.
# All six companion modules `import Mathlib` (OrdinaryH0 also imports ClosedSuperlevel, OrdinaryH0Controls imports
# OrdinaryH0, SuperlevelBarField imports SuperlevelBar and Specifications.Field), so `--fresh` (re-check of the whole
# import closure) does not fit a hosted job: still running at 1500 s with 6.6 GB resident at 4 threads.
# TORUS_LEANCHECKER_FRESH=1 selects it for an operator's local run; the receipt records which mode ran.
if [ "${TORUS_LEANCHECKER_FRESH:-0}" = 1 ]; then
  LEANCHECKER_COMMAND='leanchecker --fresh TorusFiltration'
else
  LEANCHECKER_COMMAND='leanchecker Specifications.Field TorusTopology ClosedSuperlevel SuperlevelBar OrdinaryH0 OrdinaryH0Controls SuperlevelBarField TorusFiltration'
fi
printf '%s\n' "$LEANCHECKER_COMMAND" > "$TORUS_OUT/leanchecker.cmd"
# shellcheck disable=SC2086
run_lean leanchecker $LEANCHECKER_COMMAND
# False statements about the companion's own definitions: Lean itself must refuse each with exactly `⊢ False`.
for control in RejectSuperlevelSignFlip RejectSuperlevelBelowThreshold RejectConstantNotPeriodic RejectEssentialDeathBound RejectReducedPointClass RejectMergerKillsPointClass RejectSeparationWithoutNonzeroCoeff RejectNonmergerKillsDifference RejectEssentialDeathDetermined; do
  code=0
  lean -DwarningAsError=true --root="$TORUS_OUT" "$TORUS_OUT/$control.lean" >"$TORUS_OUT/$control.log" 2>&1 || code=$?
  printf '%s\n' "$code" >"$TORUS_OUT/$control.status"
  python3 -B -S "$TORUS_SIDE/check.py" negative "$TORUS_OUT/$control.log" --control "$control" --status "$code"
done
# Admission injections run WITHOUT warnings-as-errors: Lean accepts the file, only the axiom audit refuses it.
for control in RejectSorry RejectCustomAxiom RejectNativeDecide; do
  code=0
  lean --root="$TORUS_OUT" "$TORUS_OUT/$control.lean" >"$TORUS_OUT/$control.log" 2>&1 || code=$?
  printf '%s\n' "$code" >"$TORUS_OUT/$control.status"
  python3 -B -S "$TORUS_SIDE/check.py" negative "$TORUS_OUT/$control.log" --control "$control" --status "$code"
done
# Runtime guard, after the last Lean execution: the same observations again.
lean --version > "$TORUS_OUT/toolchain-final.log"
cat "$TORUS_OUT/toolchain-final.log"
observe_packages "$TORUS_OUT/packages-final.log"
INNER
cd "$ROOT"
python3 -B -S "$SIDE/check.py" finish "$OUT"
echo 'PASS: torus-filtration companion replay; kernel-checked declarations only. Alignment review, scientific effect and acceptance are not decided here.'
