#!/usr/bin/env bash
set -euo pipefail

classifier="$(dirname "$0")/classify_negative.sh"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

expect_pass() {
  local name="$1" status="$2" log="$3"
  if ! bash "$classifier" "$log" "$status"; then
    echo "expected pass: $name" >&2
    exit 1
  fi
}

expect_fail() {
  local name="$1" status="$2" log="$3"
  if bash "$classifier" "$log" "$status"; then
    echo "expected rejection: $name" >&2
    exit 1
  fi
}

cat > "$tmp/intended.log" <<'EOF'
WithoutNoncriticality.lean:13:2: error: Type mismatch
  regularPointChart hSmooth ?_ x
has type
  ¬IsCriticalPoint d g x → OpenPartialHomeomorph (E d) (ℝ × ker)
EOF
expect_pass intended 1 "$tmp/intended.log"

cat > "$tmp/syntax-token.log" <<'EOF'
WithoutNoncriticality.lean:13:2: error: unexpected token 'end'; expected term
-- IsCriticalPoint regularPointChart
EOF
expect_fail syntax-token 1 "$tmp/syntax-token.log"

cat > "$tmp/resource-token.log" <<'EOF'
regularPointChart noncritical
lake env lean: Killed
fatal: out of memory
EOF
expect_fail resource-token 137 "$tmp/resource-token.log"

cat > "$tmp/setup-token.log" <<'EOF'
noncritical regularPointChart
error: unknown module prefix 'Mathlib'
EOF
expect_fail setup-token 1 "$tmp/setup-token.log"

expect_fail unexpected-success 0 "$tmp/intended.log"
expect_fail resource-exit-status 137 "$tmp/intended.log"

expect_usage() {
  local name="$1" status="$2" log="$3" rc=0
  bash "$classifier" "$log" "$status" || rc=$?
  if [[ "$rc" -ne 2 ]]; then
    echo "expected usage error (exit 2): $name" >&2
    exit 1
  fi
}

# Each control below keeps all three intended markers, so only the check
# under test can reject it.
with_intended() {
  local out="$1"; shift
  cat "$tmp/intended.log" > "$out"
  printf '%s\n' "$@" >> "$out"
}

for sig in \
  "error: unknown package 'Mathlib'" \
  "error: invalid import: Foo" \
  "error: failed to fetch dependency" \
  "error: cannot find module Foo" \
  "no such file or directory" \
  "error: file not found: Foo.lean" \
  "lake: command not found" \
  "fatal: unable to access 'https://example.invalid/'" \
  "could not resolve host: example.invalid" \
  "HTTP 403" \
  "parser error" \
  "syntax error" \
  "invalid syntax" \
  "unexpected identifier" \
  "expected token" \
  "operation timed out" \
  "lake env lean: Killed" \
  "fatal: out of memory" \
  "OOM" \
  "memory exhausted" \
  "resource temporarily unavailable" \
  "no space left on device" \
  "terminated by signal 9" \
  "exit code 137"; do
  with_intended "$tmp/signature.log" "$sig"
  expect_fail "intended-plus: $sig" 1 "$tmp/signature.log"
done

for st in 124 143; do
  expect_fail "resource-exit-status-$st" "$st" "$tmp/intended.log"
done

sed '/error: Type mismatch/d' "$tmp/intended.log" > "$tmp/no-mismatch.log"
expect_fail missing-type-mismatch 1 "$tmp/no-mismatch.log"
sed 's/error: Type mismatch/error: unsolved goals/' "$tmp/intended.log" > "$tmp/other-error.log"
expect_fail other-error-kind 1 "$tmp/other-error.log"
sed 's/¬IsCriticalPoint/IsCriticalPoint/' "$tmp/intended.log" > "$tmp/no-negation.log"
expect_fail missing-negated-premise 1 "$tmp/no-negation.log"
sed 's/→ OpenPartialHomeomorph/→ PartialEquiv/' "$tmp/intended.log" > "$tmp/no-chart.log"
expect_fail missing-chart-codomain 1 "$tmp/no-chart.log"
expect_usage non-numeric-status x "$tmp/intended.log"

echo "negative classifier mutation tests: PASS"
