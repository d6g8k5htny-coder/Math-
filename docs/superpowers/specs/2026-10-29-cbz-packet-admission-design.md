# Close omitted source declarations in two Lean packet gates

Task main#684, contribution CBZ-VERIFIER-AUDIT-DB642. Owner's 29 October Crystalline Baseline Protocol authorizes autonomous repair, and makes auditor soundness/verification truth immutable.

Observed at Math8151f592918a845bf19eb8eafaf8444540a32734: determinant_moment_20261025 source gate accepts a rebound unused axiom, sorry definition, and private theorem. CapFirstExit source gate accepts an omitted private theorem. Source hashes alone do not establish a complete declared-target census. Reproducer: controller evidence cbz/discovery/math/probe_admission.py.

## Chosen correction

Retain each existing public theorem-target ABI and all proof bytes. Add a separately bound complete supported-source declaration census, including existing private declarations, definitions, abbrev, instances and structures. Compare actual declarations to that census and refuse forbidden logical-placeholder/axiom/native-code tokens and unsupported declaration-bearing or metaprogramming syntax. Preserve nested comments, strings, namespaces and sections correctly, or fail closed when a spelling cannot be understood. Refuse incomplete/unbalanced lexical input.

Reuse existing exact source identities and gate tests. Do not transplant the core's theorem-only grammar: determinant already has legitimate private declarations, DM2Jet abbrev and regressionKernel_isMarkov instance; Cap has structures and nested namespaces/sections. No renaming or visibility change of mathematical declarations to satisfy a parser.

Prefer one small shared source-admission helper under tools/lean_packet_admission.py, explicitly byte-bound by both packet manifests and checked before import/use. Tests under tests/test_lean_packet_admission.py plus existing packet tests. A fixed helper path, symlink refusal and exact SHA are required; no arbitrary out-of-packet path from manifest.

This is a bounded source admission check. It is NOT the G2 all-compiled-constant axiom audit. Keep current Lean build, leanchecker, target axiom and rejection controls unchanged, and state the residual compiled-census gap truthfully. No source/lexical test qualifies G2, G4, semantic alignment, vacuity or all Layer A. A missing runtime is not mathematical quarantine.

## Evidence and integration

Add meaningful RED tests for the demonstrated escapes and other unsupported forms, then implementation, normal/-O tests and isolated mutations of the new auditor itself. Changed checker/census bytes require fresh hosted packet execution before any new kernel claim. Cap already has an exact path-triggered workflow. Determinant lacks one: a narrow path-triggered hosted qualification using the repository's pinned Lean action/dependencies is authorized if necessary, with actual failure preservation and nonzero test discovery. It must not claim final CBZ or replace existing gates.

Private source remains private. Parent owns remote publication and canonical tool/decision registration. No remote cleanup in this contribution.
