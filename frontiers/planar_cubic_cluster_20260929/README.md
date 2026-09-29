# Planar cubic cluster law: exact classification and a compact Gaussian sector

OpenAI / GPT-6 Astra Pro. Author-side conditional proof candidate; nonauthor review OPEN. Scientific effect NONE. No governing status or parent source is changed. No self-merge or organizational-independence claim.

The packet adds an exact zero/one/two classification for the full typed pinned cubic, a Gaussian r^3 coefficient and joint total-variation limit in every fixed compact soft-jet sector, finite positive nonempty coefficient integrals, and birth-height factorization of the limiting sector law. It does NOT identify the full global C6 limiting measure: uniform scaled tails outside compact jets and spatial regions remain unproved.

Start with PROOF.md. The deterministic classifier is (C6); the conditional Gaussian law is (G4); explicit global LOWER bounds are (G12); birth factorization is (G15). In particular neither the local support {0,1,2} nor limiting sector birth independence is asserted globally.

## Reproduction

Python standard library only, with Git needed for full source verification:

    python -B -S verify.py

Run in a checkout containing the exact source commit in SOURCES.json. This checks every declared source identity, the complete flat packet inventory, tests in normal and optimized Python, deterministic output, eight rejected semantic mutants and unknown-label rejection. Hosted full-repository and Lean checks remain separate; this packet is not Lean-formalized.

    python -B -S verify.py --local-only

The second command explicitly reports source_pins_checked=false and does not authenticate the project source Git objects. It is appropriate for the standalone download only. Source preservation and full hosted checks are not waived.

The independent finite oracle counts exact conic roots, including double roots, linear degree drops and open endpoints, without floating point or calls to the classifier's threshold formula. The code does not evaluate the Gaussian coefficients numerically and does not prove the analytic limit.

## Review requested

A: shear, endpoint types, classifier, strict window boundary and saddle signatures.
B: compact C^2 stability, conditional full-field coupling, density Jacobian and joint total-variation limit.
C: integrability, positive coefficients and justified lower-bound exhaustion, parity factorization and global non-claims.

Exact review bindings and subsequent dispositions belong in the PR discussion or an additive review record; an author-time header is not a scientific status register.

DEEP_TRANSVERSE_EXCLUSION.md is a separate deterministic addendum: under a C4 bound, a sufficiently negative transverse Hessian excludes every additional critical point in a fixed Rr square. It proves an explicit compact soft-jet containment but does not supply the missing derivative-weighted Gaussian tail. Its five finite companion tests bring the packet suite to 43 tests per Python mode. This addendum has its own nonauthor review obligation; PROOF.md and cubic.py remain unchanged.
