# C296 scope

## Exact claim

For arbitrary `d`, `g : E d → ℝ`, and `x : E d`, the packet consumes:

- `hg : IsSmooth d g`;
- `hx : ¬ IsCriticalPoint d g x`.

It proves the literal derivative range equality, the strict derivative, and the
regular scalar chart with its first-coordinate, base-point, source-membership,
and target-membership identities.  The derivative is exactly
`fderiv ℝ g x`; it is not replaced by an abstract equivalent.

## Logical boundary

Noncriticality is used to show that the continuous linear functional is
nonzero, then `Module.Dual.range_eq_top_of_ne_zero` yields scalar surjectivity.
Smoothness at order one supplies `HasStrictFDerivAt`.  Mathlib's existing
`HasStrictFDerivAt.implicitToOpenPartialHomeomorph` supplies the chart.

The equality of the first coordinate with `g` is global as an equality of the
underlying chart function.  Inverse and homeomorphism properties remain
restricted to the chart source and target.  No global product decomposition is
claimed.

## Explicit exclusions

- no chart or normal form at a critical point;
- no Morse lemma formalization;
- no proof that a closed superlevel is locally path connected;
- no quotient, half-space, or relative-LPC transport;
- no removal or weakening of C294 premises;
- no stochastic, persistence-pairing, registry, acceptance, or integration
  transition.

`WithoutNoncriticality.lean` omits only `hx`.  A qualifying negative result is a
nonzero Lean exit with a type mismatch exposing `¬ IsCriticalPoint`; timeout,
setup, syntax, import, or unknown-production-identifier errors do not qualify.

The exact C294 `Lifetime.lean` is consumed in place through a read-only Lake
library.  Existing C294 bytes are not copied or modified.
