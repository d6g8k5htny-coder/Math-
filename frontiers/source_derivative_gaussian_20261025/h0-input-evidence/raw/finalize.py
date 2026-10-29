import datetime
import hashlib
import json
import pathlib

ROOT = pathlib.Path('/workspace/scratch/actual-h0-support-inputs')
PACKET = pathlib.Path('/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025')

def identity(path):
    path = pathlib.Path(path)
    data = path.read_bytes()
    return {'path': str(path), 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}

bindings = json.loads((ROOT / 'BINDINGS.json').read_text())
environment = json.loads((ROOT / 'environment.json').read_text())
receipts = [json.loads(path.read_text()) for path in sorted((ROOT / 'runs').glob('*/receipt.json'))]
by_module = {receipt['module']: receipt for receipt in receipts}
modules = ['ClosedSuperlevel', 'OrdinaryH0', 'ElderInterval', 'ElderBridge']
assert len(receipts) == 4 and set(by_module) == set(modules)
for binding in bindings['modules']:
    receipt = by_module[binding['module']]
    assert receipt['exit_code'] == 0
    assert receipt['source_before'] == receipt['source_after'] == binding['successor']
    assert receipt['source_snapshot']['sha256'] == binding['successor']['sha256']
    assert receipt['stdout']['bytes'] == receipt['stderr']['bytes'] == 0

freeze = max(receipt['ended_utc'] for receipt in receipts)
artifacts = {'schema': 1, 'scope': 'Four old-body narrow-import support compositions only',
    'frozen_utc': freeze, 'new_research_target_credit': 0,
    'qualified_by': 'Exactly one successful -DwarningAsError=true compilation of each current successor source, with literal original-body bindings.',
    'root_owns_registration_and_cache_copy': True, 'helper_wrote_production_cache': False,
    'eligible_named_production_objects': [], 'ineligible': 'All other scratch files, runners, snapshots, manifests and reports; no helper/control object is production eligible.',
    'reused_old_mathematical_evidence': True, 'new_kernel_replays': 0, 'new_old_controls_or_audits': 0,
    'new_mathematical_review_credit': 0, 'scientific_effect': 'NONE'}
for module in modules:
    receipt = by_module[module]
    artifacts['eligible_named_production_objects'].append({'module': module,
        'source': receipt['source_after'], 'compile_receipt': str(ROOT / 'runs' / receipt['label'] / 'receipt.json'),
        'olean': receipt['olean'], 'ilean': receipt['ilean']})
(ROOT / 'ARTIFACTS.json').write_text(json.dumps(artifacts, indent=2) + '\n')

binding_rows = []
for b in bindings['modules']:
    binding_rows.append(f"| {b['module']} | {b['origin']['bytes']} | `{b['origin']['sha256']}` | {b['successor']['bytes']} | `{b['successor']['sha256']}` |")
body_rows = []
for b in bindings['modules']:
    body_rows.append(f"| {b['module']} | {b['origin_body_byte_offset']} | {b['successor_body_byte_offset']} | {b['body_bytes']} | `{b['body_sha256']}` |")
compile_rows = []
object_rows = []
for module in modules:
    r = by_module[module]
    compile_rows.append(f"| {module} | `{r['label']}` | {r['exit_code']} | {r['elapsed_seconds']:.9f} | empty / empty |")
    for kind in ['olean', 'ilean']:
        a = r[kind]
        object_rows.append(f"| `{module}.{kind}` | {a['bytes']} | `{a['sha256']}` |")

report = f'''# Four actual-H0 support input compositions

All four support successors passed strict compilation on their first and only attempt at Lean 4.34.1 / Mathlib `d13f23b723b8a846827a245b89c10fc7d3f11612`. Every byte after the original import headers is preserved. `ElderBridge` is whole-file exact. The support Lean sources and objects were frozen at `{freeze}`; the producer was directly notified before its final own-module kernel. These four reused support roots earn **zero new research theorem targets**. Scientific effect NONE.

## Scope, authority and reusable evidence

Task owner `/root` delegated only new `inputs/elder/{{ClosedSuperlevel,OrdinaryH0,ElderInterval,ElderBridge}}.lean` and this scratch directory to OpenAI/Codex `/root/actual_h0_support_inputs`. Root alone owns root registration, configuration, cache copying, manifests, commits and publication. This helper did not edit any existing input, configuration, cache, source root or manifest, and did not create commits, external posts or subagents. The only repository writes are the four new input files.

Read authority: `/workspace/AGENTS.md`, repository `AGENTS.md`, local canonical mandate/delegation copies in `/workspace/main/governance`, published H0 specification and plan at PRECODE `{bindings['precode_commit']}`, and `/workspace/scratch/actual-torus-h0-preflight/REPORT.md`. The observed repository HEAD at preparation was the same PRECODE commit. Frozen specification/plan snapshots are under `evidence/`.

The workspace owner clarification requires completed, applicable verification to be reused. A new agent/session/handoff is no reason to replay unchanged checks. The old 37-source/28-input execution and the old eight-module H0 mathematical/kernel/control campaign remain reusable. The retained historical report records eight standard own-module kernel replays and 49 distinct named axiom targets limited to `propext`, `Classical.choice`, `Quot.sound`; it explicitly does not claim an exhaustive generated-constant inventory. The old controls and separate nonauthor ACCEPT_SCOPED result are carried forward on their actual assumptions. No old kernel, control, axiom audit, proof campaign or mathematical review was replayed here. Provider-distinct process requirements are separate and receive no new credit from this helper.

Standing authority links, carried for onboarding and handoff:

- https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OWNER_MANDATE_20261015.md
- https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OP-AUTONOMY-20260923-v2.1.md

Carrying these links does not establish that a future recipient has read them.

## Origin custody and literal preservation

Published origin commit: `{bindings['origin_published_commit']}`. `ClosedSuperlevel` and `OrdinaryH0` come from `companions/torus_filtration_20261011`; `ElderInterval` and `ElderBridge` come from `frontiers/asymmetric_elder_bridge_20261017`. Each was extracted with `git show <published>:<path>`, retained under `origins/`, and matched byte-for-byte against its last-change commit blob. The recorded last-change commit is `c4eabc1a917ba2c1b96fe4af425cf2a484877c03` for all four. Exact Git blob identities, paths, header strings and comparisons are in `BINDINGS.json`.

| Module | Origin bytes | Origin SHA-256 | Successor bytes | Successor SHA-256 |
|---|---:|---|---:|---|
{chr(10).join(binding_rows)}

The boundary is immediately after the leading contiguous import lines; all following whitespace, comments, declarations, statements and proofs are literal preserved bytes. The following offsets are zero-based byte offsets. The original and successor suffixes were compared literally once during preparation. Each strict receipt later binds the unchanged source to that recorded successor hash; no repeated unchanged body check was needed.

| Module | Origin body offset | Successor body offset | Body bytes | Equal body SHA-256 |
|---|---:|---:|---:|---|
{chr(10).join(body_rows)}

`IMPORT_ONLY.diff` and the four per-module `.diff` files retain exact changes. The bridge diff is empty. There were no source revisions after the initial candidates.

## Finite import environment

`ClosedSuperlevel` replaces the umbrella by `Mathlib.AlgebraicTopology.SingularHomology.HomologyZero`, `Mathlib.Topology.Instances.Real.Lemmas`, `Mathlib.Tactic.Linarith` and `Mathlib.Tactic.NormNum`.

`OrdinaryH0` replaces its umbrella by `Mathlib.AlgebraicTopology.SingularHomology.HomologyZero` and retains `ClosedSuperlevel`.

`ElderInterval` retains `OrdinaryH0` and adds `Mathlib.Algebra.Category.ModuleCat.Biproducts`, `Mathlib.CategoryTheory.Abelian.FunctorCategory` and `Mathlib.Tactic.Abel`.

`ElderBridge` retains exactly `ElderClearance` and `ElderInterval`. Its clearance branch resolves from the existing packet cache; the newly compiled H0 branch resolves from this helper's unique scratch build. No full Mathlib umbrella, variant duplicate root, replacement topology source, compact-Morse input, `SuperlevelBarField` or `Specifications.Field` was introduced. No module/namespace/declaration was renamed.

## Actual compile receipts

The specific uncovered obligation was artifact availability for these four new narrow-import compositions under the current pin and imported environment. Each module was compiled once, sequentially in dependency order, with `-DwarningAsError=true`. No plain-compile fallback, disabled warning, failed attempt, kernel replay, control launch or new audit occurred. No unchanged successful module was compiled again.

| Module | Receipt | Exit | Measured seconds | stdout / stderr |
|---|---|---:|---:|---|
{chr(10).join(compile_rows)}

`compile.py` is the executed runner. Every `runs/<module>-strict-001/receipt.json` retains the actual argument array, working directory, full `LEAN_PATH`, source and source-snapshot identity, runner identity, UTC start/end, monotonic elapsed time, exit code, diagnostic identities and output identities. Empty `stdout.log`/`stderr.log` files are retained. Every receipt records identical source-before/source-after identities. `environment.json` retains actual Lean version, platform, explicit `/home/agent/.elan/bin/lake` identity, Mathlib HEAD and the base `lake env printenv LEAN_PATH` value.

The compile process used direct pinned Lean at `/home/agent/.elan/toolchains/leanprover--lean4---v4.34.1/bin/lean` after obtaining the packet environment via `/home/agent/.elan/bin/lake env printenv LEAN_PATH`, prepending `/workspace/scratch/actual-h0-support-inputs/build`. The helper wrote only its own `build/` objects, never the packet cache.

The shell calls that executed the finite preparation/compile stage were:

```text
python3 /workspace/scratch/actual-h0-support-inputs/prepare.py
python3 /workspace/scratch/actual-h0-support-inputs/compile.py ClosedSuperlevel
python3 /workspace/scratch/actual-h0-support-inputs/compile.py OrdinaryH0
python3 /workspace/scratch/actual-h0-support-inputs/compile.py ElderInterval
python3 /workspace/scratch/actual-h0-support-inputs/compile.py ElderBridge
```

All returned exit 0. Preparation records its observed UTC timestamp in `BINDINGS.json`; compile timing is exact in the receipts. No compile failures exist to report or omit. Two earlier read-only discovery commands returned nonzero: an `rg` tactic-name search found no matches and a chained Git lookup for the pinned delegation path in the separate local main checkout found no such path at that commit. Neither launched Lean, changed a file, or invalidated the local mandate/delegation text already read; the standing canonical links are retained unchanged above. These discovery outcomes were not counted as mathematical evidence.

## Frozen production-eligible objects and producer handoff

Only the following eight named objects under `/workspace/scratch/actual-h0-support-inputs/build` are eligible for root's production copy. `ARTIFACTS.json` binds each pair to its exact source and strict receipt. Every other scratch file is ineligible for production object copying. No helper/control object exists in this build.

| Object | Bytes | SHA-256 |
|---|---:|---|
{chr(10).join(object_rows)}

The producer may use the frozen support build explicitly from packet cwd:

```sh
/home/agent/.elan/bin/lake env sh -c 'LEAN_PATH=/workspace/scratch/actual-h0-support-inputs/build:$LEAN_PATH exec lean ...'
```

The unchanged old API is `TorusFiltration.elderTrap_of_boundary`, then `elderSection`, `elderRetraction`, `elderSection_retraction`, and `elderDirectSummand` with `(k := K)`. The accepted old declarations use a common universe for carrier and coefficient field; `(K : Type) [Field K]` matches the actual torus without a new lift obligation. The import composition preserves the actual ordinary singular-H0 functor. It supplies no new geometry, canonical Morse partner, exhaustive barcode, weighted count, probability bound or scientific promotion.

Finalization only joined stored preparation/compile metadata and wrote this report, `ARTIFACTS.json` and its receipt index; it launched no verification command. Support sources/artifacts remain frozen, and no further helper Lean launch is planned.
'''
(ROOT / 'REPORT.md').write_text(report)
index = {'schema': 1, 'assembled_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'frozen_utc': freeze, 'new_lean_launch_count': 4, 'strict_success_count': 4, 'strict_failure_count': 0,
    'compile_receipts': [str(ROOT / 'runs' / by_module[module]['label'] / 'receipt.json') for module in modules],
    'all_compile_sources_join_literal_body_bindings': True,
    'BINDINGS': identity(ROOT / 'BINDINGS.json'), 'ARTIFACTS': identity(ROOT / 'ARTIFACTS.json'),
    'REPORT': identity(ROOT / 'REPORT.md'), 'environment': identity(ROOT / 'environment.json'),
    'prepare_runner': identity(ROOT / 'prepare.py'), 'compile_runner': identity(ROOT / 'compile.py'),
    'historical_and_spec_snapshots': [identity(path) for path in sorted((ROOT / 'evidence').iterdir())],
    'no_further_lean_launch_planned': True}
(ROOT / 'EXECUTION_RECORD_INDEX.json').write_text(json.dumps(index, indent=2) + '\n')
print(json.dumps({'report': index['REPORT'], 'bindings': index['BINDINGS'], 'artifacts': index['ARTIFACTS'],
    'frozen_utc': freeze, 'strict_success_count': 4, 'strict_failure_count': 0}, indent=2))
