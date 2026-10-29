Corpus admission policy verifier — local standard-library tool

admission.py checks a proposed train/validation/test manifest against a separately
pinned operator-trusted policy. It checks byte integrity, exact task/target/source/
proof/receipt bindings, whole-root acceptance fields, allowed axioms, zero free
variables/metavariables, provenance and reviewed exposure attestations, frozen
family splits, content identities and duplicates. It never launches Lean or RL.

A positive decision means only that these documented policy conditions match
trusted saved documents. It does not prove the receipt's mathematical assertion,
the reviewer's honesty/authority, complete historical non-exposure, novelty,
statistical independence, usefulness of the corpus, or an RL benefit. There is
no signature infrastructure here: the independent policy SHA256 is the trust
anchor. Approve that policy and its authorized reviewers/evidence out of band;
never obtain its expected hash from the untrusted proposal itself. Changing the
policy and supplying its new hash is a new operator trust decision, not proof.

Known exposure remains denied regardless of proposed labels. The pinned local
blocked_evidence.json records all49known P15 target names, source/proof/statement
hashes, and both historical self-local trace export hashes. The original files
stay immutable. The P15 namespace, historical origin disclosures and diagnostic
open-context flags also deny. Renaming a known target does not conceal a known
source hash. These finite controls cannot detect every rewritten derivative;
mandatory lineage/exposure/dependency review supplies that separate policy claim.
Default denial applies to missing attestations, receipts, provenance and families.

No self-asserted claimed_eligible flag can grant admission. The actual root must
have an operator-pinned acceptance receipt bound to the trusted artifact and
exact target/source/proof/runtime/baseline identity. Its fields must record closed
whole-root kernel checking and checked insertion, exact target equality, no free
variables/metavariables and no forbidden axioms. A saved attestation is mandatory
and independently bound to the provenance, artifact, families and permitted split.
The verifier validates saved claims; it does not re-execute those proof checks.

Use Python3.12+ and standard library only. All evidence references are relative
to the policy directory, byte-pinned, nonsymlink files, without path traversal;
each file is limited to8MiB. JSON duplicate keys/nonfinite constants deny.
All recognized present Boolean metadata must use JSON true/false exactly, including
optional exposure/eligibility fields; numbers, null and strings cannot alias them.
Lone Unicode surrogates, nonfinite exponent-overflow floats and JSON integers
longer than4300digits deny cleanly. These checks apply recursively to metadata
in the proposal, trusted policy and referenced documents. Output flags are actual
Boolean values. Content
IDs bind immutable task/proof/source identities and record split/families. The
policy separately freezes reviewer, receipt, provenance and attestation versions.
Within a dataset, duplicate record/artifact/task IDs deny; shared theorem,
derivation, source or transport family across any two splits denies. Empty
transport-family lists are allowed; other family categories must be nonempty.
The same frozen family map must be reused across future datasets when enforcing
cross-campaign separation; this tool cannot infer undisclosed earlier datasets.

CLI (read-only; writes its JSON result only to stdout):
  python -B admission.py DATASET.json --policy TRUSTED_POLICY.json --expected-policy-sha256 INDEPENDENT_SHA256
Exit0 means documented policy admission; exit1 means denial. Any row failure
refuses the entire dataset and removes positive row-level admission labels.
actual_training_authorized and scientific_corpus_established are always false:
this read-only tool neither authorizes execution nor upgrades scientific status.

The supplied fixtures/positive directory contains two entirely synthetic records
and self-authored synthetic receipt/review objects for branch testing. They do
NOT contain Lean proofs, newly collected theorem data or scientific attestations.
Their only positive label is policy_admitted_fixture. Fixture policy mode cannot
admit candidate-kind records, and candidate mode cannot admit fixture-kind rows.
They exist to test byte/policy controls and must not enter real model training.

Run regressions directly in normal and optimized Python:
  python -B -m unittest discover -s tests -v
  python -B -O -m unittest discover -s tests -v
Retain a fresh bounded verification campaign outside a sealed package:
  python -B run_verification.py --output /ABS/NEW_OUTPUT
The runner runs tests and positive/denied CLI controls in both modes, retains
stdout/stderr/CPU/wall/return-code receipts and source hashes, and verifies its
inputs remain unchanged. It performs no native proof work or network action.

This closes a missing admission-tool gap. The actual eligible representative
learning corpus remains absent. The49known source-exposed entries, historical
self-local traces and synthetic fixtures are not that corpus.
