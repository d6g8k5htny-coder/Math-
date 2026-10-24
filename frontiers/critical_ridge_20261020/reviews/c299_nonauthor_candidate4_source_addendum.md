# C299 candidate4 nonauthor source-repair addendum

Review time: 2026-10-20 14:52:36 UTC. Actual reviewer: OpenAI Codex `/root/c299_nonauthor_review`, delegated by `/root` for Dylan Roy. Actual mathematical author: `/root/adapter_feasibility_c292`. Same-provider, source-exposed nonauthor review; organizational/provider independence credit 0, human review credit 0, scientific effect NONE.

**Disposition: ACCEPT_SCOPED_SOURCE_REPAIR for candidate4 at the exact identity below.** The bounded successor diff addresses the actual candidate3 diagnostics without changing the mathematical hypotheses or conclusions. I found no new source blocker to the next root-owned, declared hosted development attempt. Compilation, kernel verification, full origin census and actual negative diagnostics are unconfirmed for candidate4. This disposition is not a formal PASS.

This addendum preserves the earlier source reviews and actual failures. Candidate3's prior source acceptance did not establish successful elaboration; its actual hosted attempt failed. I did not author or edit this repair.

## Exact source and actual failure

Fresh native byte/hash reads establish:

| Item | Bytes | SHA-256 |
|---|---:|---|
| `project/CriticalRidge.lean`, candidate4 | 8664 | f3a515bd0a984c8a8affbfc79f4768e7a357b7798eee8990a5a34adbdcf6f0f7 |
| `execution/author/CANDIDATE4.diff` | 2160 | 1b02ee505c6d1bd4a3ad86ef92c4fa12fd7e92747fc3d8bd25f6ffce6f15c180 |
| `execution/author/CANDIDATE4_FREEZE.json` | 1302 | d5f98f98928b053de563a1ed637cffdc2e8b8eb0baa286e265d12c72a156aef1 |
| Actual candidate3 `build-CriticalRidge.stdout` | 3059 | a784390b5d21162fef912eb6fefc803a57dfd4ca887a8d2402ce453b275746d6 |

The separately frozen candidate4 source snapshot also hashes to `f3a515bd0a984c8a8affbfc79f4768e7a357b7798eee8990a5a34adbdcf6f0f7`. I directly compared it with the retained candidate3 snapshot `2a93240fa5034544a1dbcf5ec0a10ab11be1ca5d05f60b4df0e2663fa769f442`; the actual diff agrees with the handoff.

The actual candidate3 failure is run **39440510935**, attempt 1, PR491 head `8336bb7c16e34db69837b10e3678fb1bc894179c`, tested merge `55ad6bad497da1a9c7ddd6002ba0c718994c26e1`. The root disposition identifies its original artifact as 480098 bytes, SHA-256 `da3a551f550fb50eea816f1ad00c3f0f6532f4192ba99ac5805bd58522c72a46`; original artifact custody is root's verified evidence, not a new remote fetch by me.

I read the complete failing stdout and phase receipt under `hosted-development2/extracted/`, plus `hosted-development2/DISPOSITION.json`. The phase receipt hashes to `08e1d5320a15693c7b2c68a8b82c7b28eb374b6c3703b326596fa7db377db0ac`; the disposition to `6749268f876cfe6a1f0bfc5e8a142c68e6dab9a678b22508bc38b330734e31dc`. The failure was exit 1 after **12.745656 seconds**, with empty stderr and no timeout. Its object inventory remains the three upstream objects. No CriticalRidge object was produced, and no audit build, kernel phase or negative fixture was reached. Passing other CI jobs does not repair that failed phase.

## Changed proof reconstruction

The actual derivative failure left an equality between the intended restricted Hessian chain and the bilinear CLM-composition derivative containing an extra zero summand and `compL.flip`. Candidate4 removes that expansion. It uses the derivative of the already-defined continuous linear restriction map and composes it directly with `hcomp`, the derivative of `q ↦ Df(p + ridgeAddition V q)`. The pinned `ContinuousLinearMap.hasFDerivAt` theorem gives the restriction map itself as derivative; the pinned chain rule gives exactly its composition with `hcomp`'s derivative. Unfolding `negativePartialGradient` and function composition identifies the same original function. This preserves the literal Hessian derivative and removes the failed `convert`/extensional-simplification branch, including the unused-simp warning reported under warning-as-error.

Two `set_option backward.isDefEq.respectTransparency false in` commands are new, scoped to `negativePartialGradient_hasFDerivAt` and the endpoint theorem. This changes elaboration's definitional-equality transparency handling; it is not a new hypothesis, axiom, admitted proof, changed theorem type, disabled warning policy or bypass of the eventual kernel gate. I checked actual declaration-local precedents in pinned Mathlib `FDeriv/Congr.lean` and `FDeriv/Basic.lean`, and examples where the same local command precedes a theorem documentation comment. The option's use is plausible for the displayed product/topological instance-coherence failures. I do not claim that source inspection proves it resolves every elaboration failure: that requires the next actual compilation. An optional lookup at an assumed local elan core-source path was absent; no Lean-core source inspection or compiler invocation is claimed.

The actual IFT failure displayed eventual pointwise equality on one side and `EventuallyEq` on the other. Candidate4 explicitly changes the IFT result to

`∀ᶠ w in 𝓝 0, G (w, r w) = G 0`

and the target to the corresponding equality with zero. It then uses `h.mono` and equality transitivity with the already-proved `hG0`. This is the same local IFT equation for the same chosen `r`; no extra local equation is assumed, no neighborhood is strengthened and no local statement is promoted to a global statement.

The final chain-rule failure concerned the base point `((0 : E d), r 0)` versus product zero. Candidate4 rewrites `hr0` in that goal before applying `hDG`, then uses the unchanged graph derivative and chain rule. The resulting differentiated equation is still `D ∘ (id, Dr 0) = 0`, evaluated on arbitrary ambient `w` and `z : V`. The actual endpoint remains `hessian d f p (w + Dr(0)w) z = 0` using the same ridge.

## Preserved scope and verification boundary

Direct snapshot comparison shows no edits to any declaration's binders or result type. There remain four definitions and five theorems. No `sorry`, `admit`, axiom, opaque placeholder, unsafe declaration, new assumed ridge/chart/inverse certificate, or altered import is introduced by this repair. The two elaborator settings are local. The public endpoint still derives one ambient-parameter ridge from literal `IsSmooth`, actual criticality at `p` and strict negative definiteness on the literal subspace.

The earlier mathematical reconstruction and its nonorthogonal cross-block, zero-subspace, degenerate restriction and missing-criticality checks remain applicable because the types and mathematical construction are unchanged. I did not rerun or broaden those unchanged reviews. Full origin census, generated declarations and transitive axioms still require actual audit output; the nine textual public declarations are not that census.

I performed source/diff/hash/receipt reads and read relevant pinned Mathlib APIs only. I did not invoke Lean, tests, mathematical programs, a workflow or the artifact master; did not edit author/support sources; and performed no claims, publication, CI, merge or access action. This addendum covers candidate4 proof source. Any new manifest/workflow publication identities need root's separate exact-byte binding.

The next evidence gate is actual hosted candidate4 compilation followed, if it succeeds, by the declared audit/kernel/negative phases. Final diagnostic qualification and final collector/master evidence remain separate gates. Full critical basis, quotient/full LPC, C294 hclosedLPC, bars and broader scientific obligations remain OPEN.
