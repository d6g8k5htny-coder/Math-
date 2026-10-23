# Bounded original d2/L24 collision-expression certificate

This standard-library package evaluates and checks a rational enclosure of
the original full-spectrum physical C_alg(2,24). It preserves the zero mode
and full normalizer. Engineering relative-width goal:1/100. Scientific
effect NONE; scientific_acceptance=false. See PROOF.md for the exact
expression, trust base and retained scientific HOLDs.

The authorized original target evaluation is frozen before execution in a
local source commit. RESULT.json and original command receipts identify
that actual source version. A consumer can independently check those bounds:

    python -B verify_coefficient.py RESULT.json --expected-commit SOURCE_COMMIT

Use the literal frozen source commit from the original receipt, not a
later evidence-only commit. This checker imports the unchanged moment
checker and shared parsing/custody module; it never imports the new
coefficient producer. Upstream full identities are in SOURCE_MAP.json.

The applicable package suite is:

    python -B -m unittest -v test_coefficient.py
    python -O -B -m unittest -v test_coefficient.py

The suite checks primitive roots, Gamma extrema/tail normalization, an
interior angular-ratio maximum, positive variance floors, request/parser
guards, false target status and full certificate/tamper cases. Before the
original target output exists, certificate-dependent cases are explicitly
skipped. All must execute in the final applicable package verification.

The original producer invocation is recorded, not an invitation to launch
scientific experiments or repeat target execution merely for timestamps.
Output creation is exclusive; existing evidence is never overwritten by
the producer. Failed development checks and source-transfer corrections
are retained alongside final receipts. No repository-wide unaffected
suite or existing hosted workflow is rerun by this bounded package stage.
