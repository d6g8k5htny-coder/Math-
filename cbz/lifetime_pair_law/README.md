# Scoped pair-law countermodel

This preserves two literal Lean declarations about the existing
`PairLawInterface` in `Specifications/Lifetime.lean`. The proof source is
byte-identical to the historically executed source (Git blob
`3b7712e41e8a6b0569c31c549a83857d9fe2ada6`, SHA-256
`812ba30d02f16a69abdcb8b23d28fa4a8fe68e3a016911d7f08e98ebe04cdfc7`).
The source was moved outside the statement-only package because its checker
requires an exact packet file inventory; the original branch and job log remain
preserved.

For any supplied field and elder interfaces, the artificial probability
`p = 1` satisfies the upper predicate. For supplied positive `L`, the two
interfaces and an orthonormal frame, the same law violates the E4 two-sided
predicate on the singleton windows `[0,0]` and `[1,1]`. The upper
predicate's original positive-`L` and window antecedents are retained; it can
hold vacuously on invalid inputs. Existence of the supplied elder interface is
not established. The artificial law is not identified with the intended
geometric elder event, and no parent model theorem is disproved or closed.

Historical [run 40957238766](https://github.com/d6g8k5htny-coder/Math-/actions/runs/40957238766),
job `123740377857`, at exact commit
`5a470bfd739aba22e32b91587d5dfc031a7de3fc` compiled the proof and
completed `leanchecker`; both declarations printed only `propext`,
`Classical.choice` and `Quot.sound`. The connector's decoded GitHub job log is retained under
`evidence/original-job.log`; byte identity of the original log download has not
independently been verified. GitHub artifact `12936365078`
reports ZIP SHA-256
`d2cebfee006c1fdb924c49dec0d9a80c745579335953b989a3225eae5b9a166d`;
its ZIP bytes have not independently been downloaded here.

The new integration candidate uses the same Lean source bytes with a moved
path and the then-current main tree. It adds a scoped workflow, whose exact
commands are in `.github/workflows/cbz-lifetime-pair-law-countermodel.yml`:
check the unmodified statement-packet inventory, build the pinned package,
compile the proof, compare both axiom report lines exactly, and execute
`leanchecker`. It creates and removes a temporary copy only after requiring
that no same-named package file exists; original tracked inputs are retained.
The workflow is an execution aid, not a federation-wide auditor, and assumes
the runner, Lean executable and pinned dependencies are trusted during the
run. No fresh candidate pass is asserted until the hosted job completes.
