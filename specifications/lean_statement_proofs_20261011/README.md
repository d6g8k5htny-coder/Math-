# Lean statement proofs (`specifications/lean_statement_proofs_20261011`)

**Scientific effect: NONE.** Organizational-independence credit: 0 (Anthropic / Claude). Alignment
status of every statement proved here: **PENDING_INDEPENDENT_REVIEW**. No claim, premise, obligation
or disposition changes status because of anything in this directory.

## What this packet is

Kernel-checked Lean 4 proofs of statements that are *already registered* in the statement packet
[`specifications/lean_statements_20261010`](../lean_statements_20261010) (`REGISTER.json`, modules
`Specifications/{Field,Lifetime,Side24,RN,P15}.lean`). That packet holds `def … : Prop`
declarations and interface `structure`s and nothing stronger; this packet depends on it by path
(`lakefile.toml`, `[[require]] path = "../lean_statements_20261010"`) and never edits it.

Every theorem in the inventory has as its *type* a registered Prop constant applied to exactly the
theorem's own parameters:

```lean
theorem rhoStarBelowSixSevenths : UniversalLaw.Spec.P15.RhoStarBelowSixSevenths := …
theorem fullBlockCoverIff {X : Type} [Fintype X] [DecidableEq X] (F : RealizedData X) :
    UniversalLaw.Spec.P15.FullBlockCoverIff F := …
```

A theorem of the shape `theorem foo (h : extra) : P` or `theorem foo : P → P` or
`theorem foo (n : ℕ) : P (n + 1)` is **refused**: an extra hypothesis or a narrowed argument is a
finding about the statement (report it), never a theorem of it.

## What a green run establishes, and what it does not

| established by a green `check.py --execute` | not established |
|---|---|
| each inventoried theorem was accepted by the Lean kernel (`lake build`, replayed by `leanchecker`) at Lean `v4.34.1` (commit `5045d005…`), Mathlib `d13f23b7…`, against the statement modules whose SHA-256 the receipt records | that any informal Layer 0 claim is true, aligned with its Lean statement, reviewed or accepted |
| its transitive axioms are within `propext`, `Classical.choice`, `Quot.sound` (`#print axioms`, and Lean's `collectAxioms` on every constant the modules add) | anything about the statement's fidelity to its source: alignment is PENDING_INDEPENDENT_REVIEW and is written only by an independent reviewer |
| its type, after `forallTelescope`, is a registered Prop constant applied to exactly the telescope's variables (Lean's `ConstantInfo`, not source text), and Lean's inventory equals the lexical scan's | any change to `REGISTER.json`: the register's labels (`specified` for every statement of the statement packet) are untouched; a register row of kind `theorem` naming this packet is the statement packet maintainers' decision, not this gate's |
| no `sorry`, `axiom`, `native_decide`, `unsafe`, `opaque` or proof-written-as-`def` anywhere in the modules; `maxHeartbeats` above 400000 only with a justifying comment | a LANDING_CLAIMS disposition (`HOLD_WITH_DOMAIN`, `FAIL_CLOSED`, `EXACT_COUNTEREXAMPLE`, `REVIEWED_SCOPED`, `ENGINEERING_HOLD`): transcribed in the register, never derived here |
| the negative controls refused for the intended reasons (sorry via the axiom audit; a custom axiom; an unregistered type; a smuggled hypothesis and a `P → P` implication; a tightened false arithmetic statement rejected by Lean) | the parent theorems, the identification of interface structures with the informal objects, independence (credit 0), or any prize claim |

Vocabulary (docs/FORMAL_VERIFICATION.md): the source-mode summary says `formalization_status:
"proved"` (the label of a committed proof package); `kernel-checked` appears **only** in a run
receipt (`.lake/evidence/receipt.json`). On the evidence ladder a kernel-checked theorem is L5
*for that Prop*; the informal claim it serves keeps the ladder level and formal-progress label the
register gives it.

## Layout

```
README.md  SCOPE.md  check.py  test_check.py  replay.sh
lakefile.toml  lean-toolchain  lake-manifest.json  SpecificationProofs.lean
SpecificationProofs/<Family>.lean      one module per family, namespace UniversalLaw.Proofs.<Family>
```

Rules for every module (enforced by `check.py`, see its module docstring):

* imports only `Specifications.<Module>` and Mathlib, never another proof module;
* exactly one top-level `namespace UniversalLaw.Proofs.<Family>`; helpers are `private` or live under
  a `…Aux` namespace and are not inventory items;
* every non-aux theorem's docstring carries `Proves:` (naming the registered Prop), `Method:` and
  `Does not establish:`;
* no `sorry`, `admit`, `axiom`, `native_decide`, `unsafe`, `opaque`, `partial`, `implemented_by`,
  `extern`, `include`, `_root_`, metaprogramming commands, `#` commands, `debug.*`/`bootstrap.*`
  options or `autoImplicit`; declaration and scope keywords start their own line.

## How to run

```bash
export PATH="$HOME/.elan/bin:$PATH"
P=specifications/lean_statement_proofs_20261011
python3 -B -S $P/check.py                 # source mode (git identity, lexical scan, inventory); add --allow-dirty locally
python3 -B -S $P/test_check.py            # unit tests; the LeanHelpers class runs only when `lake` is on PATH
python3 -B -O -S $P/test_check.py
python3 -B -S $P/check.py --execute       # fresh lake build, leanchecker, #check/#print axioms, environment audit, controls, receipt
bash $P/replay.sh [--allow-dirty]         # all of the above in order
```

Compile one module while writing it: `cd $P && lake env lean -DwarningAsError=true
SpecificationProofs/<Family>.lean`. The gate refuses warnings in proof modules in the build log.
Never run `lake update`; `.lake/packages` may be a symlink to a prebuilt dependency tree locally (the
receipt records `packages_dir`), and each package directory must be at its locked revision.
`lakefile.toml` is pinned byte-exactly (Lake would accept a `moreLeanArgs = ["-Ddebug.skipKernelTC=true"]`
line that no "contains these lines" check sees).

Resource needs of `--execute`: the `leanchecker` replay of the Mathlib-importing environment holds
roughly 14 GB of anonymous memory (it was memcg-killed at 13.5 GB RSS on a shared 16 GB machine; on
an idle one it finishes in about a minute), the fresh `lake build` of the packet takes a few minutes
once the Mathlib oleans are present. The hosted runner (`ubuntu-latest`) is where the first receipt
for a commit exists. On a smaller machine `LEAN_PROOF_SKIP_LEANCHECKER=1 python3 -B -S $P/check.py
--execute --allow-dirty` runs every other stage; the variable is honoured only together with
`--allow-dirty` (never in CI), the receipt then reads `leanchecker: "SKIPPED_LOCAL_ONLY"` and, like
every `--allow-dirty` receipt, is not evidence about any commit.

CI: [`.github/workflows/lean-specification-proofs.yml`](../../.github/workflows/lean-specification-proofs.yml)
(`leanprover/lean-action`, `use-mathlib-cache: 'true'`; the statement packet, a path dependency,
builds from source) uploads `.lake/evidence/` as an artifact. A green workflow is a run, not a review.

## Receipt

`.lake/evidence/receipt.json` (`LEAN-PROOF-RECEIPT-20261011-v1`): `checked_commit`, `worktree`
(`CLEAN` or `UNVERIFIED` with `--allow-dirty`, in which case the receipt is not evidence about any
commit), the Lean version line, dependency revisions, SHA-256 of the register, the statement modules
and the proof modules, the theorem inventory (name, module, registered Prop, claim ids it serves,
axioms), the environment-audit class counts, the negative-control outcomes and the log digests.
`theorems.json` beside it carries the elaborated signatures.
