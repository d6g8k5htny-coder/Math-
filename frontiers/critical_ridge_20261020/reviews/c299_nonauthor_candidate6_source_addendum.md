# C299 candidate6 nonauthor source-repair addendum

Review time: 2026-10-20 15:15:51 UTC. Reviewer: OpenAI Codex `/root/c299_nonauthor_review`, delegated by `/root` for Dylan Roy. Source author: `/root/adapter_feasibility_c292`. Actual nonauthor review with same-provider source exposure; organizational/provider independence credit 0, human review credit 0, scientific effect NONE.

**Disposition: ACCEPT_SCOPED_SOURCE_REPAIR for exact candidate6, limited to the final bounded hosted development attempt authorized by root.** The two diff hunks directly address the actual remaining candidate5 errors. I found no new source blocker. Candidate6 remains uncompiled, and this disposition does not establish a ridge object, kernel/census result, negative qualification or final acceptance.

## Exact binding and failed predecessor

Candidate6 `project/CriticalRidge.lean` is **9053 bytes**, SHA-256 `9ff65416927182f6dad06646f04821b3af6bdd131740d93bf229354a81e19c38`. The separately frozen source-attempt copy has the same freshly checked hash. `execution/author/CANDIDATE6.diff` is 821 bytes, SHA-256 `115d82a173293d95d418d2950724775c4a4152c55982c1dcaf32b366ae9732d8`; `CANDIDATE6_FREEZE.json` is 1352 bytes, SHA-256 `939794111ac7c956d9d9b1c2e98783f1059b24505883d6d00ea3710ffa2305b3`. Direct snapshot comparison with candidate5 `669b94138531a694f134d24ee9d34ecf6cda5ccec125e2bac279f9e49e1a4aae` reproduces exactly these hunks.

The retained actual hosted4 result names run **39445649166**, attempt 1, PR491 head `3111e77c882b4e441b3b4c5ed6f01da46cf8e34c`, tested merge `d93ff50e029d0c6edb3f94f1889fcd991b85721b`, and status `HOLD_NOT_COMPLETED`. I read its context plus the full failing phase stdout and receipt.

The stdout is 1601 bytes, SHA-256 `1cc98e9540608d20c0f1a9b66a0fdb3fcb4b5910ec671da7b1e8624c508d4d7c`; the phase receipt hashes to `b9a4454c5356a65f64d129141ddce26a6f8efd6673ef65f53f64592f23276406`. Actual candidate5 execution exited 1 after **21.013988 seconds**, without outer timeout or reported internal heartbeat failure. Three upstream objects remain; no ridge object or subsequent audit/kernel/negative evidence was produced.

The complete diagnostic reports one unsolved `case hr`, a derivative-map equality precomposed with `ContinuousLinearMap.inr`, and two unreachable-tactic errors at line 202 columns 40 and 58. The source-author freeze binds that actual failure. `hosted-development4/DISPOSITION.json` was absent during this review; I do not claim to have read a separate disposition or newly verified the original remote archive.

## Exact repair assessment

I checked the pinned `ContinuousLinearMap.prod_ext` theorem in `PiProd.lean`: its registered extensionality rule splits equality of maps out of a product into `inl` and `inr` obligations. This explains the actual `hr` remaining after the prior generic `ext q z; rfl` sequence. My candidate5 review reconstructed the value-level equality but did not establish coverage of every tactic-generated branch; the actual failed run supplies that correction to the review record.

Candidate6 replaces generic `ext` with two explicit applications of `ContinuousLinearMap.ext`. The first introduces one arbitrary argument of the actual product domain `E d × V`, without selecting the registered product-splitting rule. The second introduces one argument of the covector domain `V`. This gives one pointwise value equality for the nested linear maps, rather than separate left/right product obligations. After the existing `comp_zero` and `zero_add` reduction, both values are definitionally the application of `D²f p` to `ridgeAddition V q` and then to `z`, through the same subtype inclusion. The final `rfl` therefore targets the actual pointwise equality. I checked the pinned explicit extensionality signature, which requires only `∀ x, f x = g x`, and retained the earlier inspection of `compL`/`flip` application definitions.

The second hunk removes exactly the two trailing `<;> rfl` sequences that the actual compiler identified as unreachable: one after converting `hgraph`, and one after the outer graph-chain-rule conversion. Their `convert!` invocations remain. No premise, derivative term, graph function, point equality or mathematical conclusion is removed. The actual diagnostic gives specific evidence that those trailing tactics were not being executed in candidate5; removing them preserves the proof work already performed and preserves the warning-as-error policy.

The diff changes no public signature, import or mathematical definition. All nine declaration names/types remain unchanged. It adds no option, cap increase, linter suppression, axiom, `sorry`, `admit`, unsafe declaration or assumed ridge. The earlier mathematical construction and adversarial cases therefore retain their original scope.

## Remaining gates

This review is source-level evidence for the two exact edits, not a compiler observation for candidate6. The next hosted attempt must still demonstrate fresh successful compilation before any ridge formal claim. The full audit, four named kernels, actual negative fixtures and diagnostic qualification remain separate requirements. The final artifact master remains a source-reviewed verifier whose complete invocation is unobserved in this review.

I performed source/diff/hash/receipt/API reads and wrote only this additive review. No author/support source was edited; no Lean, test, mathematical program, workflow or complete master was executed by me; no remote action occurred. Root owns publication byte binding, the declared hosted attempt and final custody.

All earlier failed attempts and source dispositions remain immutable historical evidence. Critical basis, quotient/full LPC, C294 hclosedLPC, bars and broader scientific promotion remain OPEN.
