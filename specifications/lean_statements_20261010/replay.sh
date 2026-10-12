#!/usr/bin/env bash
# Local replay of the statement-only package check. Scientific effect: NONE.
# Order: source check (fails closed before any Lean), unit tests in both Python modes, then the
# Lean execution (fresh lake build, leanchecker, #check / #print axioms of every registered
# declaration, the environment audit of every constant the modules add, the negative controls,
# receipt under .lake/evidence/).
# Extra arguments are passed to check.py (local development: --allow-dirty; a receipt produced
# that way records the worktree as unverified and is not evidence about any commit).
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
P="$ROOT/specifications/lean_statements_20261010"
cd "$ROOT"
export PATH="$HOME/.elan/bin:$PATH"
export PYTHONDONTWRITEBYTECODE=1
mkdir -p "$P/.lake"
python3 -B -S "$P/check.py" "$@"
python3 -B -S "$P/test_check.py" 2>&1 | tee "$P/.lake/tests.log"
python3 -B -O -S "$P/test_check.py" 2>&1 | tee "$P/.lake/tests-optimized.log"
python3 -B -S "$P/check.py" --execute "$@"
echo 'PASS: statements elaborated and inventoried; formal progress specified; alignment PENDING_INDEPENDENT_REVIEW; scientific effect NONE.'
