# Explicit final-input FIRST identity authority

Root identified a concrete pre-execution gap: FINAL_INPUTS.json is written after external script/docs identity freeze and cannot recursively contain its own identity. The archive previously granted no FIRST identity authority to packaging members, so an unseeded final-input copy would fail closed.

Actual new_packaging_payloads defaults to ONLY FINAL_INPUTS.json. The gate requires a duplicate-free list of explicit packaging members and constrains its names to that one immutable NEW metadata filename. The packaging-member loop passes first_new only when the actual name is in that root-approved list. Every known script/doc/history path still needs a reused identity; proof/source/old material receives no new authority. This is the filename-whitelist implementation; it does not load an external final-input identity sidecar.

Before versions of archive_prepare.py, FINAL_INPUTS.schema.json, READINESS.md and STATIC_REVIEW.md are retained verbatim. FULL_ACTUAL.patch records the actual final delta. No prepared script was executed, imported, compiled, tested or hashed; no mathematical verification or old identity check occurred.
