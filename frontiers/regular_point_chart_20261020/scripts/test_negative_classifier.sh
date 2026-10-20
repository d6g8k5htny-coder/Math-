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
  ¬ IsCriticalPoint g x → OpenPartialHomeomorph (E d) (ℝ × ker)
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

echo "negative classifier mutation tests: PASS"
