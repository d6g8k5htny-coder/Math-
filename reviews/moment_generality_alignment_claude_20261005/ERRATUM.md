# Erratum to REVIEW.md (Math-#281 evidence)

Scientific effect: **NONE**. Dylan Roy, delegated AI work. Author: Anthropic /
Claude, Claude Code session `session_015wNj8LPTKXsaT68G3DgPPh`, the author of
the `REVIEW.md` and `alignment.candidate.json` in this directory.

This file is additive. `REVIEW.md` (SHA-256
`71d13aec20a053b7e0447576230561de5f062244733b7501b701b6b174c4a0e8`) and
`alignment.candidate.json` (SHA-256
`b2099c804b8c28006a4e877c092501a1da1942897bf3abed40fff35dffc47e25`) stay
byte-identical, as bound by the nonauthor custody read Math-#281 review
5418603211 and by the candidate's evidence digest. No verdict, target,
disposition or lineage entry changes. Both corrections come from the Codex
review of Math-#281 (threads 4187180231 and 4187180222). Both were verified
against primary sources before being written here.

## E1. Commit checked by the hosted kernel evidence (REVIEW.md, "Identity of what was reviewed", Hosted kernel evidence row)

The row says run 37334385439 ran "`pull_request` on the frozen head". The
correct identity is as follows:
- The run's `head_sha` is the PR head
  `f6672c1a77d67b6257c43acaf5a4481b28fd87e0`.
- The required-check evidence is bound to the commit that was actually checked,
  the synthetic merge `494551a02d87dff751b5e08dab00a0d24096d732`. This is
  recorded in `required-check-binding.json` of artifact 11356251099, with
  receipt SHA-256
  `a51c2be316b57505bbf412ccdb21063cac67f17e87b78595cf772e0952591d26`.
- That merge's tree, `a5a8efaa0421ee974f6bd97dcf42b0bd7c4cdef6`, equals the
  frozen head's tree. Tree equality is a separate fact, and it does not replace
  the commit binding.

The artifact was later downloaded and authenticated by the custody read
5418603211. This session could not download it.

## E2. Promotion of the candidate record (REVIEW.md, "Lineage", final paragraph)

The sentence "the change is one field: `"disposition": "ACCEPTED"`. Everything
else is already bound" is **withdrawn**. It stopped being true when Math-#283
landed:
- `formal/gate.py::check_alignment` now rejects a declared proposer whose
  provider or family is a placeholder such as `UNKNOWN`. The #277 entry in
  `proposal_authors` has exactly that.
- The candidate binds manifest `74c5a338…` (the #279 head `f6672c1`). The
  manifest on `main` after #279's reconciliation and landing is `ba9fe1d9…`.

Any future accepted record would therefore need all of the following:
1. the #277 proposer's provider and family established from evidence;
2. a rebinding to the then-current manifest and scope digests;
3. an alignment review of those exact bytes;
4. a pass under the gate as it is at that time.

Under option (a) (main#229 5999351698, 5999541966 and 5999543473) the record
stays **WITHHELD**, as disclosure only.
