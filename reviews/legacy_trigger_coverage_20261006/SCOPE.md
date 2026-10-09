# Legacy package-resolution trigger coverage

Dylan Roy — delegated AI engineering. Actual author OpenAI / GPT-6 Astra Pro,
`qs-continuation-legacy-trigger-20261006-r6`. Pickup Math-#351/6014859323.
Scientific effect **NONE**; organizational-independence credit 0. No self-merge.

## Finding and isolated scope

Native #351 discussion_r4191758835 identifies two repository paths which can
change the meaning of `from tools.legacy_json_replay import replay` without
matching any of the three dedicated workflow filters: `tools/__init__.py` and
root `tools.py`. The original helper lives in an implicit namespace package.
An initializer executes on import; a root module can supersede that namespace
and make the submodule import fail. This is missing trigger coverage, not a
claim that the current numerical result is wrong or that a malicious file exists.

Base: #351 head `18afecd9e505167b6eb1d9457b17ed9aacee6677`.
This proposal changes only three workflows, adds one regression file, and this
scope note. It is stacked to isolate its delta, NOT permission to merge into
#351's or #330's owner branch. Canonical parent adoption stays with that owner.

Each workflow retains every original path and adds `tools/**`, `tools.py`, and
`tests/test_legacy_workflow_triggers.py`. The broad subtree intentionally runs
these checks for additional tools changes; it does NOT cover root `tools.py`,
which is therefore explicit. A separate step runs the regression in normal and
optimized Python before the existing full-shell protocol tests. No negative
path patterns, new events, permissions, action/runtime pins, job budgets,
production imports, numerical commands, or acceptance contracts are changed.

The entire original workflow is recovered by removing exactly the three added
path entries and the four-line new step. The original source preflight,
checker/replay invocation, final JSON statement and Git postflight are byte-exact.
All helper/contracts, original tests, scientific inputs/proofs/RESULTS/manifests,
formal code, scientific registers, premises and review history are unchanged.

## Test-first execution

Local: CPython 3.13.5, Git 2.47.3, Linux. GitHub clone failed DNS, so the local
worktree is an authenticated three-file source subset, not a full repository.
All original workflow bytes reconstruct their native Git blob identities:

| Workflow | Original Git blob |
|---|---|
| local-pairing.yml | 8ea45e74672c42687176462e79df33adaf83c98d |
| far-elder-rate.yml | 37c0dd197e3d6c0fd10a172a656b79f496943aa2 |
| c6-cluster-law.yml | ae5bf02b6358c0e83fe8a52b470eb4734536f113 |

The five-method new suite against the original workflows fails **15 intended
assertions per outer interpreter mode, zero errors**: nine named resolver-path
coverage cases, three missing self-triggers and three missing two-mode steps.
The actual-import method passes even on the predecessor, establishing the
mechanism independently of the repaired configuration. It executes the exact
import line read from each workflow against a synthetic helper in isolated
subprocesses: three families, two child modes, namespace/initializer/root-module
variants, **18 real children per outer run**. Initializers and root modules leave
observable markers; root-module selection also yields the expected package error.
No import/subprocess implementation is mocked. Child environments are private
and remove ambient PYTHON variables; the caller environment is not changed.

After the 21-line workflow amendment, **5/5 methods pass in each outer mode**.
Four separately copied configuration mutations then reject in both modes with
exactly 3/6/3/3 assertion failures and zero errors: remove root-module coverage,
remove subtree coverage, remove the test's trigger, or remove its optimized
invocation. Valid old paths and unrelated-path negatives are retained. All three
YAML documents parse and every run block passes `bash -n`; the product test itself
uses only the standard library, not the auxiliary YAML inspection dependency.

From the repository root:

```sh
python -B -S tests/test_legacy_workflow_triggers.py
python -B -O -S tests/test_legacy_workflow_triggers.py
```

## Evidence and integration boundaries

The test uses a deliberately restricted reader for the actual positive,
single-quoted path lists, and literal/subtree patterns. It rejects unsupported
syntax rather than claiming to implement GitHub's full YAML/glob evaluator.
These checks establish configured coverage and real Python import behavior;
they do NOT constitute a hosted changed-path-only scheduling experiment, a
hostile-source sandbox, an exhaustive import-dependency audit, or a theorem.
GitHub's own changed-file/diff limits remain. Arbitrary future loader hooks,
root standard-library shadows and installed dependencies are outside this fix.

Full original legacy tests and source-authenticated numerical replays were not
executed locally. Actual dedicated and applicable general hosted checks on the
published candidate, a bounded nonauthor delta review, and an explicit owner
adoption/reconciliation are still required. No earlier #330/#351 review transfers
to changed YAML merely because the numerical block is preserved. Keep the native
finding open until its actual source/review disposition is satisfied. A stacked
success is not a current-main integration receipt. Parent and later #348/signing
branches must not be overwritten; reconcile their real ordering and source.

Primary technical references consulted 2026-10-06:
- https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax
  (`on.<event>.paths`, diff limits, literal and `**` path patterns).
- https://docs.python.org/3.13/reference/import.html
  (regular/namespace packages and submodule import resolution).
