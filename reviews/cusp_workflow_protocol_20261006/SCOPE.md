# Cusp workflow: complete deterministic rejection reports

Dylan Roy — delegated AI engineering. Actual author: OpenAI / GPT-6 Astra Pro,
`rfgate-followthrough-cusp-contract-20261006`; pickup Math-#322/6016381591,
characterization/implementation notice 6016664543. Scientific effect **NONE**;
source/report exposed, organizational-independence credit 0. No author self-merge.

## Original source and observed defect

Source cut `11f9127f00ce922e5d39b0da42af76134eb78a21`:

| File | Bytes | Git blob |
|---|---:|---|
| `.github/workflows/cusp-second-order.yml` |5776|7060635b18af66cf0802f49e44e692b730fa3b8c|
| `frontiers/cusp_second_order_20261001/cusp_check.py` |35169|98ac5070c26655bd3aa979a86319e655462156ae|
| packet `SOURCES.json` |8629|5d7678b033856407b472ed687f1f2ea6390e90ab|
| packet `RESULTS.json` |1596|c5cc870726dc17e1a1abd5765f01b3ff85b46f07|

The original wrapper checks baseline stdout but ignores stderr. It accepts each
named mutant solely by exit 1 and M9 solely by exit 2; it does not independently
require the complete ordered mutant inventory. A crash or wrong report can thus
count as the expected negative control. This is an engineering finding, not a
counterexample to the original mathematical arguments or finite identities.

## Genuine reports, not guessed diagnostics

Isolated execution snapshot `b05b0ddc6f982ee68e73b5d1d5e7317e1c1acb69` adds only
one branch-restricted read-only characterization workflow to the source cut.
That never-merge driver is NOT part of this proposal. Actual GitHub Actions run
**37465152509/1**, job112274212867, completed successfully at Python3.11.16.
It authenticated the six packet files and exact membership, then ran the original
baseline, M1-M5 and M9 in normal and optimized modes: **14 real subprocesses**.
All seven pairs of stdout AND stderr are byte-identical. Baseline matches the
original RESULTS. The original checker is self-contained; this characterization
did not revalidate all consumed upstream mathematical files or run exploration.

Artifact11413459080:58209B, SHA256
`393e02ad9defd6ac8167e154835be035ec0d802d6ed161b613b14af22ec20aff`.
Its30members are28binary streams, a run-bound record and an exact tracked-source
tar. All members/CRCs/stream identities and eight archived original source files
were independently verified. A second local CPython3.13.5 run of all14 original
invocations matched every captured stream and exit.

| Mutant | Sole false check | Exact `info` |
|---|---|---|
|M1|C2_elder_window_exact_maximin|elder window fails at phi = -29/60 (death level None)|
|M2|C6_cusp_integrals|elder cusp integral|
|M3|C4_cusp_limit_field_pinned_polynomials|cusp limit field mismatch (m = 1): -181/240 vs -67/80|
|M4|C3_fiber_reduction|fiber identity fails (m = 1)|
|M5|C8_gap_affine_structure_and_cand_constants|d det K_M / dk != -6 det A_M (m = 1)|

Each complete mutant JSON retains every other baseline check, its own label,
overall Boolean false, object and scientific-effect fields. It exits1 with empty
stderr. M9 exits2, stdout empty, stderr exactly `unknown mutant label\n`.
The checker source explicitly selects the corresponding C2/C6/C4/C3/C8 mutation;
these are not inferred solely from a generic process failure.

## Repair and deliberately unchanged behavior

The existing workflow now requires the exact M1-M5 ordered inventory before any
checker child. The five fixed stdout sizes/SHA256s bind their ENTIRE original
reports, together with exit1 and empty stderr. Baseline retains exact RESULTS
comparison and additionally requires empty stderr. M9 requires its complete
exit2/stdout/stderr triple. References are not learned from the current mutant
run; a changed report requires deliberate source-bound review and rebinding.

Exact bytes intentionally reject even JSON whitespace/ordering changes. This is
a deterministic internal command contract, not a general JSON-format API.
It avoids a new helper import, parser framework or dynamic auxiliary dependency.

The complete source preflight and final clean-Git block are unchanged. This
includes nonempty consumed/cited/tree-or-API dependency identity checks and the
existing fail-closed behavior on source drift. No source hash was widened or
rebased to hide a historical dependency mismatch. Original packet, proof,
checker, RESULTS, SOURCES, exploration, formal, rules and scientific flags are
untouched. Existing action/Python pins, read-only permissions,10-minute budget
and600-second child timeouts remain. Only the new test trigger and two-mode test
step are added outside the changed result-validation block.

## Test-first evidence and limits

The new8-method test file executes the complete actual verification shell inside
real disposable committed Git repositories. A synthetic child emits the known
original report bodies; no subprocess is mocked and no numerical calculation is
claimed by these fixtures. Packet and all three upstream source categories have
nonempty identity-bound data. All source preflight and final dirty-tree checks
remain active. A separate child trace checks the complete sequence or exact
stopping prefix; named source failures also require their own diagnostics.
Signing and automatic maintenance are disabled only on the disposable Git commit.

Each complete run covers **85 scenarios**. The final unchanged test file against
the original workflow yields **60 intended assertion failures,0errors** in EACH
normal/optimized mode:59 unsafe admissions plus missing regression wiring.
The other26 scenarios behave correctly. The amended workflow yields **8/8 methods
PASS,85/85 scenarios** in EACH mode. Cases cover every mutant's crash/silence/
stderr/wrong exit; wrong check/reason/label structure, Boolean coercion, duplicate
keys, nonfinite/trailing/extra/formatted JSON; baseline and M9 streams/exits;
source tamper/membership/symlink, missing/reordered/duplicated control lists and
the final tracked-tree mutation. The whole-shell child itself runs both modes.

Local runtime: CPython3.13.5/Git2.47.3/Linux. YAML and all run-block Bash syntax
checks passed; unchanged preflight/postflight were compared explicitly. Local
work is an authenticated source subset, not a complete repository test/Lean
execution. Direct GitHub DNS was unavailable. An unavailable streaming-execution
attempt launched no test; completed foreground runs and original failed results
are retained. No timeout or failure was converted to a pass.

Reproduction at the repository root:

```sh
python -B -S -m unittest discover -s tests -p test_cusp_workflow_protocol.py -v
python -B -O -S -m unittest discover -s tests -p test_cusp_workflow_protocol.py -v
```

For RED, use an isolated copy of the original tree with the new test retained.
The original seven packet files must stay present. `CUSP_WORKFLOW_ROOT` selects
an isolated workflow/reference tree for local counterfactual testing only.

This is not a hostile-executable sandbox, proof of an arbitrary child's internal
failure location, exhaustive API/loader/fs coverage or durable timeout-evidence
system. A malicious program could print a known report; source trust and proof
validity remain separate. The earlier never-merge characterization is NOT a
production candidate's required-check receipt. Actual full current-candidate
cusp/source replay, all applicable hosted checks and one nonauthor engineering
review remain required before separate eligible guarded integration. #322 stays
open for its broader class; other active authors and integration slots are intact.
