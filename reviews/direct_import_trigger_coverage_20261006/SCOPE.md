# Direct-helper package-shadow trigger coverage

Dylan Roy — delegated AI engineering. Actual author OpenAI / GPT-6 Astra Pro,
`qs-direct-import-trigger-20261006-r7`, pickup Math-#322/6015484094.
Scientific effect NONE; source-exposed; organizational-independence credit 0.
Author replay is not nonauthor review. No author self-merge.

## Source and mechanism

Authenticated source cut: `11f9127f00ce922e5d39b0da42af76134eb78a21`.
Original complete workflows:

| Workflow | Bytes | Git blob |
|---|---:|---|
| c6-cluster-coefficients-numerics.yml | 3089 | e4f49dcb48350d2f1546a7d7d2108c112e9498f3 |
| remainder-rate.yml | 5354 | 3ee30582e1e3fd3c2ad997cf68cc9ed121d4c514 |

Both workflows prepend the repository's `tools` directory to `sys.path`, then
import a bare module. A same-name package containing `__init__.py` is selected
instead of the helper `.py` file. The two named paths are
`tools/c6_coefficient_numerics_replay/__init__.py` and
`tools/remainder_rate_replay/__init__.py`; neither matched the old filters.
This is a future-change coverage gap, not an allegation that such shadow
packages are presently committed or that a numerical output was incorrect.

This differs from #351/#361's `from tools...` package import: here a root
`tools.py` or `tools/__init__.py` alone does not affect the bare helper import.
The real probes retain those negative cases. No #361 source/review is reused
as approval of this new four-file change; its source stays frozen separately.

## Minimal change and preservation

Each workflow adds `tools/**` and this new regression file's trigger, then a
separate step invoking the complete regression normally and under `-O`.
The latter step precedes the original full-shell output-contract suite.
Removing exactly those two path lines and the four-line step recovers each
entire original workflow byte for byte. Existing imports and all original
run blocks, source preflights, historical dependency/API checks, final Git
checks, permissions, action/Python pins and job budgets are unchanged.
No helper, output contract, old test, proof, RESULTS, manifest, scientific
status, formal package, dependency or peer branch is changed.

## Actual local verification

Linux, CPython 3.13.5, selected authenticated source files only. Full GitHub
clone failed DNS resolution. No full local repository, authentic numerical
packet replay, blob-API fallback or local Lean compilation is claimed.

The new six-method suite against the original workflows failed first in
exactly ten intended subcases per outer mode: four shadow-path cases,
two self-trigger cases and four mode-wiring cases; zero harness errors.
The same suite then passed 6/6 normally and 6/6 optimized. Its real-import
method runs twenty actual Python children per suite: two helpers, two child
modes and five variants (module, regular shadow package, namespace directory,
unrelated tools initializer, root tools module). It extracts the exact two
import-setup lines from the current workflows; only the helper bodies and
filesystem are synthetic. Package execution is witnessed by a real marker.
No import/subprocess mock, network, real signer or scientific child is used.

Three isolated removal variants reject in both modes with exactly 4/2/2
assertion failures and zero errors: tools subtree coverage, self-trigger,
optimized invocation. Original RED and all later outputs are retained in the
owner evidence, not overwritten. Both complete YAML documents parsed and all
run blocks passed `bash -n`; PyYAML was used only for this local syntax check,
not added to the repository or required by the committed stdlib tests.

## Boundaries and release

The test's reader intentionally supports only the current flat positive list,
literal paths and a terminal `/**`; other syntax fails visibly. It is not a
replacement for a YAML parser or GitHub's scheduler. Normal GitHub changed-file
limits, branch filters and commit-skip behavior remain external boundaries.
No hosted changed-path-only scheduling experiment was performed locally.
Broad `tools/**` deliberately causes more dedicated runs. This does not
prevent an authorized source change, sandbox imports, cover every root
standard-library shadow/import hook, or establish mathematical acceptance.

Actual dedicated and applicable general CI, one nonauthor delta review, and a
separate eligible integrator's then-current source/check/ownership review and
expected-head merge remain required. No old candidate receipt transfers to a
new main. #316/#359 integration and #361/#363/C7 repairs retain their scopes.

Primary background consulted 6 October 2026: Python 3.13 Modules documentation,
https://docs.python.org/3.13/tutorial/modules.html ; GitHub workflow path filters,
https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax .
The observed package precedence is also established by the recorded real probes.
