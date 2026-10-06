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

1. **Grammar pre-check on source (`grammar_check`).** After stripping `--` and nested
   `/- -/` comments, every line containing the `theorem`/`lemma` keyword must match the
   canonical column-0 spelling `theorem <name>`; otherwise the gate refuses the module
   with the line number. The tokens `sorry`, `axiom`, `native_decide`, `implemented_by`,
   `extern` and `unsafe` are refused outright, outside comments. This is a pre-check:
   it keeps the source legible for the rest of the pipeline and fails early, but it is
   not what the gate trusts.

2. **Environment inventory at execute time (`inventory_source`, `audit_inventory`).**
   After `lake build`, the gate writes and runs `Inventory.lean`, a Lean program that
   enumerates, from the compiled environment's own module tables
   (`env.header.moduleData[idx].constNames` for every module under the package prefix),
   **every** constant of every package module: public, private (`_private.…`),
   auxiliary (`proof_1`, `match_1`, `_eq_1`), used or unused. It prints one `INV` line
   per constant with its kind, module and name, one `MODULE` line per module with the
   module-system flag and constant counts, and then axiom-closes all package constants
   together in one shared traversal that replicates `Lean.CollectAxioms.collect`
   (axiom: record and visit its type; def/theorem/opaque: type and value; quot: nothing;
   ctor/rec: type; inductive: type and constructors). The union is printed as one
   `AXIOMS` line. `audit_inventory` then requires:
   - the module table is exactly the registered `source_modules` plus the empty root
     module, none compiled under the module system, no code-generator extras;
   - every constant sits in a registered module; names are unique; per-module counts
     match the table;
   - no constant is itself an `axiom`;
   - the axiom closure of the whole package is inside `{propext, Classical.choice,
     Quot.sound}` (so a `sorry` anywhere in the package, in any kind of declaration,
     shows up as `sorryAx` and fails the gate);
   - the per-target `#print axioms` results are a subset of that closure (cross-check);
   - the public theorem-kind constants (kind `theorem`, name not auxiliary) are exactly
     the manifest targets.

   "Public" is decided by the kernel's kind and the name shape, not by where the
   keyword sat in the file. Union-of-closure is equivalent to the per-constant condition:
   every constant's axioms are inside the allowed set if and only if their union is.

3. **Admission controls.** The execute path then compiles four files that each append
   one declaration the old scanner could never see, in the package namespace, to the
   inventory program (with the current file's constants included): a `private theorem`
   proved by `sorry`, an indented `@[simp] theorem` proved by `rfl`, and an unused
   `noncomputable def` built by `sorry`, and a column-0 `theorem` placed outside the
   package namespace (the RF-GATE-02 shape, which the source scanner would mis-prefix).
   Each file must compile, and `audit_inventory` must reject each one (`sorryAx` in the
   closure, or an extra public theorem). If any
   escapes, the run fails with `admission control escaped the environment inventory`.
   Outcomes are recorded in the receipt under `inventory.admission_controls`.

## What the receipt gains

`receipt.json` has a new `inventory` object: number of package constants, number of
public theorems, the axiom closure, the closure size, a sha256 of the inventory lines,
and the admission-control outcomes. `required_formal_check.py` binds fixed keys and
tolerates the extra object. All earlier receipt fields are unchanged.

## Cost and measurements (local, Lean 4.34.1, Mathlib `d13f23b7`)

| Step | Wall time |
|---|---|
| Inventory via whole-environment scan (`env.constants.map₁`) | about 8 minutes (interpreter) |
| Inventory via module tables (shipped) | about 10 seconds |
| Shared axiom closure of all 82 package constants | about 2 seconds, 26 808 constants visited |

The module-table enumeration printed the same 82 constants as the whole-environment scan.

## Limits

- The inventory covers constants that reach the environment through the package's
  modules. Constants a downstream file realizes lazily (reserved names such as `eq_1`)
  belong to that downstream file, not to the package; they are not part of the exported
  package `.olean`.
- `extraConstNames` (code-generator auxiliaries) must be empty for every package module;
  a module that needs compiled code therefore fails this gate on purpose.
- The grammar pre-check cannot parse string literals; a keyword inside a string is
  refused rather than guessed. The modules on `main` contain none.
- The gate still does not decide mathematics. A clean inventory says the package's
  compiled declarations are exactly the registered ones and depend on nothing beyond the
  three standard axioms; alignment with the prose remains a separate human/nonauthor
  review.

## Tests

`tests/test_inventory_gate.py` covers the comment stripper (nesting, unterminated), the
grammar pre-check (indented, private, protected, attributed, comment-hidden keywords,
forbidden tokens), the generated Lean program's shape, and `audit_inventory` on synthetic
inventories: clean pass, hidden `sorry`, custom axiom, extra public theorem, axiom kind,
unregistered module, missing module, module system, non-empty root, code-generator
extras, count mismatch, local constants, missing target, duplicates, malformed lines, the
per-target cross-check, and the auxiliary-name pattern. The live modules on `main` are
checked to pass the grammar and to reproduce `manifest.json["targets"]`.
