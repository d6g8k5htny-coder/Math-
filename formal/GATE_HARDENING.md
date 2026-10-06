# Gate hardening RF-GATE-01: environment inventory instead of a source scan

Scientific effect: **NONE**. Dylan Roy, delegated AI work (Anthropic / Claude, Claude
Code session `session_015wNj8LPTKXsaT68G3DgPPh`). No Lean proof, manifest target,
`SCOPE.md` or status entry changes; `formalization_status` stays `proved` and
`alignment_status` stays `PENDING_INDEPENDENT_REVIEW`.

## The gap

Before this change `gate.py` built its target inventory by scanning the source modules
for lines beginning, at column 0, with `theorem` or `lemma`, and compared that list with
`manifest.json["targets"]`. Everything downstream (the `#print axioms` audit, the
elaborated-type dump, the Blueprint link check) ran on that list. A declaration the
scanner did not see was therefore never audited:

- an indented `theorem`, a `private theorem`, a `protected theorem`, or a `@[simp] theorem`
  on the same line;
- a `def`, `instance`, `opaque` or `abbrev` whose body uses `sorry` but is not a target;
- an `axiom` that no target mentions;
- a theorem keyword hidden in a block comment that the scanner mis-counted.

Such a declaration compiles (Lean only warns on `sorry`), lands in the package's `.olean`,
and is exported to every importer, while the gate reports the manifest targets as clean.
Finding RF-GATE-01 (main#229).

## The fix: two layers, the second authoritative

1. **Grammar pre-check on source (`grammar_check`).** The stripper first lexes string
   literals (with escapes), raw strings and character literals, so a `--` or `/-` inside a
   literal is not a comment; literal contents are kept, so refusals see them. Interpolated
   strings (`s!"…"`, and any plain string containing a brace, because macros such as
   `throwError` interpolate plain literals), unterminated literals and unterminated block
   comments are refused. Comments are then removed (nesting-aware), keeping newlines. On
   the remaining code:
   - every line with a `theorem`/`lemma`/`def` keyword must be the one canonical column-0
     declaration on that line (`theorem <name>`, `lemma <name>`, `def <name>` or
     `noncomputable def <name>`);
   - declaration-bearing and metaprogramming commands the scanner does not inventory are
     refused at the start of any line (`private`, `protected`, `opaque`, `abbrev`,
     `structure`, `class`, `instance`, `inductive`, `mutual`, `syntax`, `macro`, `elab`,
     `initialize`, `example`, `attribute`, `notation`, `local`, `scoped`, `section`, `run_cmd`,
     and every `#` command);
   - each module has exactly one column-0 `namespace ResearchFormalCoreR1` … `end
     ResearchFormalCoreR1` block, so a nested namespace cannot be mis-prefixed;
   - no declaration name repeats, and the manifest target list has no duplicates;
   - the tokens `sorry`, `axiom`, `native_decide`, `implemented_by`, `extern` and `unsafe`
     are refused outright, including inside string literals.

   This is a pre-check: it keeps the source legible for the rest of the pipeline and fails
   early, but it is not what the gate trusts.

2. **Environment inventory at execute time (`inventory_source`, `audit_inventory`).**
   After `lake build`, the gate writes and runs `Inventory.lean`, a Lean program that
   enumerates, from the compiled environment's own module tables
   (`env.header.moduleData[idx].constNames` for every module under the package prefix),
   **every** constant of every package module: public, private, compiler-generated, used
   or unused. For each constant it prints one `INV` line with its kind, its **provenance**
   and its module and name; one `MODULE` line per module with the module-system flag and
   constant counts; and then it axiom-closes all package constants together in one shared
   traversal that replicates `Lean.CollectAxioms.collect` (axiom: record and visit its
   type; def/theorem/opaque: type and value; quot: nothing; ctor/rec: type; inductive: type
   and constructors). The union is printed as one `AXIOMS` line.

   - **Provenance** is Lean's own record, `findDeclarationRanges?`: `user` when Lean stored
     a source range for the constant (every user-written declaration, private or not), `aux`
     when it did not (compiler-generated constants). On the current package this splits the
     116 constants into 63 `user` theorems (exactly the targets), 10 `user` definitions and
     43 `aux` theorems (`_proof_N`, `_simp_N_M`, `eq_N`).
   - **Names are encoded losslessly.** Each name is printed as its components joined by
     `/`, with `s<hex of UTF-8>` for a string component and `n<decimal>` for a numeric one.
     `Name.toString` is never parsed, so private names such as
     `_private.«.lake».«formal-evidence».hidden_sorry.0.ResearchFormalCoreR1.hiddenAdmission`,
     quoted components and names that differ only by escaping all stay distinct and
     parseable. Decoding is strict (canonical lowercase hex, valid UTF-8, canonical decimal).

   `audit_inventory` first parses the transcript strictly; any malformed line, a missing
   or repeated `AXIOMS`/`CLOSURE` record, or an empty inventory is an
   `InventoryProtocolError`, never a rejection. It then collects **every** policy finding
   as a `(code, name)` pair and raises `InventoryRejected` with the complete list:
   - `unregistered_module`, `missing_module`, `duplicate_module`, `module_system`,
     `root_not_empty`, `codegen_extra`: the module table is exactly the registered
     `source_modules` plus the empty root, none compiled under the module system, no
     code-generator extras;
   - `outside_module`, `duplicate_name`, `count_mismatch`, `package_axiom`: every constant
     sits in a registered module, names are unique, per-module counts match the table, and
     no constant is itself an `axiom`;
   - `extra_theorem`, `missing_theorem`: the `user` theorem-kind constants, private ones
     included, are exactly the manifest targets, whatever their names look like;
   - `unbound_auxiliary`: every `aux` theorem-kind constant hangs below a `user` constant
     of the same module through compiler suffix components only (`_proof_N`, `_simp_N_M`,
     `eq_N`, `eq_def`, `match_N`). The name shape is used only in conjunction with Lean's
     provenance and a user-written parent, never on its own;
   - `forbidden_axiom`, `reported_axiom_omitted`, `impossible_closure`: the axiom closure of
     the whole package is inside `{propext, Classical.choice, Quot.sound}` (so a `sorry`
     anywhere, in any kind of declaration, appears as `sorryAx`), contains every axiom the
     per-target `#print axioms` audit reported, and is at least as large as the inventory.

   Union-of-closure is equivalent to the per-constant condition: every constant's axioms
   are inside the allowed set if and only if their union is.

3. **Admission controls, each bound to its own reason (`check_admission`).** The execute
   path compiles four files that each append one declaration the old scanner could never
   see to the inventory program (with the current file's constants included):

   | Control | Injected declaration | Required findings, exactly |
   |---|---|---|
   | `hidden_sorry` | `private theorem hiddenAdmission … := by sorry` | `forbidden_axiom sorryAx` and `extra_theorem` (the private name) |
   | `hidden_theorem` | indented `@[simp] theorem indentedAdmission … := rfl` | `extra_theorem ResearchFormalCoreR1.indentedAdmission` |
   | `hidden_def` | unused `noncomputable def unusedAdmission … := by sorry` | `forbidden_axiom sorryAx` |
   | `outside_namespace` | column-0 `theorem outsideNamespaceAdmission` outside the namespace | `extra_theorem outsideNamespaceAdmission` |

   For each, the transcript must parse, the injected constant must appear exactly once with
   the expected kind, provenance, privacy and module, and the set of findings must equal the
   required set. A protocol error, a pass, a missing injection or any other set of findings
   fails the run; there is no "any `ValueError` counts" path.

4. **Compiled-package admission experiment (`compiled_admission`).** The controls above
   inject into the inventory program's own file. The gate also copies the package (sources
   plus the freshly built `.lake/build`, dependencies by symlink) into
   `.lake/compiled-admission`, outside the uploaded evidence directory, audits the unmodified
   copy (it must pass and reproduce the real package's inventory digest, the positive
   baseline), then adds `private theorem compiledAdmission : (1 : Nat) = 1 := by sorry` to
   `ResearchFormalCoreR1/AlgebraV2.lean`, runs `lake build` in the copy, and requires the
   inventory of the rebuilt package to be rejected with exactly `forbidden_axiom sorryAx`
   and `extra_theorem` for that private theorem in module `ResearchFormalCoreR1.AlgebraV2`.
   The copy is removed afterwards; its three logs and the injected module's sha256 stay in
   the evidence.

## History of the admission evidence

The first helper revision (`dec3f646`) printed names with `Name.toString` and credited any
`ValueError` from `audit_inventory` as a rejection. Replaying its real logs showed 3 of 4
controls rejected for their intended reason; `hidden_sorry` stopped earlier, at a
malformed-line error on the quoted private name, although `sorryAx` was in that log's
closure (PR #312 comments 6008555025 and 6008954175). That defect and the name-shaped
auxiliary exemption (which let a user-written `ResearchFormalCoreR1._unregistered` theorem
pass, 6009106591) are what this revision repairs. The historical transcript shape is kept as
a regression: it is a protocol error, and `check_admission` does not count it.

## What the receipt gains

`receipt.json` has an `inventory` object: number of package constants, number of public
theorems, number of compiler-generated theorems, the axiom closure, the closure size, a
sha256 of the inventory lines, the per-control outcomes with their exact findings, and the
compiled-package experiment's outcome, module and baseline digest.
`required_formal_check.py` binds fixed keys and tolerates the extra object. All earlier
receipt fields are unchanged.

## Cost and measurements (local, Lean 4.34.1, Mathlib `d13f23b7`)

| Step | Wall time |
|---|---|
| Inventory via whole-environment scan (`env.constants.map₁`) | about 8 minutes (interpreter) |
| Inventory via module tables, with provenance and encoding (shipped) | about 11 seconds |
| Four admission controls plus the compiled-package experiment | about 75 seconds |

The shared closure of all 116 package constants visits 26 853 constants.

## Limits

- Provenance is what Lean records. A metaprogram that adds a theorem without a declaration
  range would be classified `aux`; it must still hang below a user-written constant through
  compiler suffixes, and its axioms are still in the closure. The pre-check refuses every
  `#` command, `run_cmd`, `elab`, `macro` and `initialize`, so the package sources cannot
  contain such a metaprogram.
- The inventory covers constants that reach the environment through the package's
  modules. Constants a downstream file realizes lazily (reserved names such as `eq_1`)
  belong to that downstream file, not to the package.
- `extraConstNames` (code-generator auxiliaries) must be empty for every package module;
  a module that needs compiled code therefore fails this gate on purpose. Inductive types,
  structures and instances are refused by the pre-check and would need a reviewed
  extension of the auxiliary suffixes before they could be admitted.
- `leanchecker` replays the package in the execute path; on one local 15 GB container it
  was killed for memory (exit 137), so local precommit runs of this helper skipped that
  stage and say so. A complete execution with `leanchecker` exit 0 is recorded separately.
- The gate still does not decide mathematics. A clean inventory says the package's
  compiled declarations are exactly the registered ones and depend on nothing beyond the
  three standard axioms; alignment with the prose remains a separate human/nonauthor
  review.

## Tests

`tests/test_inventory_gate.py` covers the string-aware stripper (comment markers inside
strings, escapes, character and raw literals, refused interpolation and unterminated
literals), the grammar pre-check (spellings, unsupported commands, namespace structure,
duplicates, forbidden tokens), the lossless name encoding (round trips, collisions that a
dotted rendering would make, strict decoding), the generated Lean program's shape,
`audit_inventory` on synthetic inventories (every finding code, the quoted private `sorry`
case, extra user theorems whatever their names, auxiliary binding, protocol errors), and
`check_admission` (expected reason, pass, other reason, protocol error, missing or misplaced
injection). Sol's PR #312 source-gate regression cases (indented, private, attributed,
unused `sorry` definition, `opaque`, `axiom`, comment ghost, duplicate target, nested
namespace) are replayed against a copied formal tree. The live modules are checked to pass
the grammar and to reproduce `manifest.json["targets"]`.
