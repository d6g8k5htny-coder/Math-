COMPONENT HISTORY / SCOPED CHECKPOINT

This file preserves the development-time sequence and its exact evidence boundaries.
It does not certify a later baseline replay. Current contribution acceptance is
recorded in the enclosing baseline campaign and its source-hash inventory.
Earlier/native-numbered receipts remain historical; no failed trial is erased.

P15 endpoint integration and resource-aware search — 29 October 2026 UTC

From this directory:
  python -B catalog.py list
  python -B catalog.py verify
  python -B catalog.py export p15.FullTransformedPriceBudget --output /ABS/NEW.json
  python -B catalog.py verify --certificate /ABS/NEW.json
  python -B -m unittest discover -s tests -p 'test_*.py' -v
  python -B -O -m unittest discover -s tests -p 'test_*.py' -v

The catalog covers all49 original P15 packet targets. Each record supplies the
full original statement definition and SHA256, exact target/theorem names, proof
module SHA256 and source line, and saved closed/body/type/declaration/axiom audit.
The hard-pinned prior completion manifest binds every copied final01 artifact;
verification also requires the corresponding17 current formal modules to match
the actual freshly compiled source bytes. No prior directory is modified.

An exported ul-saved-endpoint-evidence-v1 record is saved source/receipt evidence.
Its checker executes no Lean kernel and it is not a structural worker-v2 proof
certificate. Current fresh project kernel verification is a separate root build.
All49 entries remain source_exposed=true and training_eligible=false. This closes
a usable catalog/list/export/integrity gap; extending the native trusted worker
from its8 task IDs to typed49-endpoint proof reuse remains separate work.

catalog.py verify_catalog(path=CATALOG, *, project=PROJECT, prior=PRIOR) returns a
validated catalog or raises ValueError/OSError. verify_certificate(path, *,
catalog_path=CATALOG, project=PROJECT, prior=PRIOR) validates an export against the
same independently reconstructed catalog. Canonical JSON comparison preserves
exact Boolean/integer/float types, including the false eligibility flag. Default project root is this package's
grandparent, so relocation works with the complete closure package. Use the CLI
--project-root flag before the subcommand for another current formal root.
The original P15 specification and all17 closed proof modules are immutable
bindings: changing a supporting module requires a new version with new reviewed
kernel evidence, not silent repinning. New General modules can coexist.

ul_engine/search.py and worker.py are copied from the latest sealed certified-
frontier-v2 engine. Expanded-parent release, sibling preservation, drop confirmation
and fairness were already fixed there; this package does not claim those fixes as
new work. The derivative adds state/request capacity admission and explicit
termination_reason. status exhausted remains compatible and means
termination_reason frontier_exhausted. resource_exhausted distinguishes
state_capacity from request_capacity; attempt_budget means the actual admitted
attempt limit was consumed. No pending child is evicted to hide exhausted space.

Use the copied LeanWorker with CheckpointSearch to expose session-wide
active_state_count and remaining_requests, including handles/requests from earlier
operations. The transport's remaining count uses the smaller of configured client
requests and the pinned native256-request cap. Admission conservatively reserves
candidate verification, live-handle cleanup, one possible new handle and shutdown.
A valid accepted proof survives a failed final drop; cleanup_complete,
cleanup_status, unreleased_states and resources_after_cleanup report that
lifecycle separately. Unreleased means no successful drop acknowledgement; a
timed-out/reaped worker may already have freed actual storage.

When adapting an existing RuntimeConfig, construct this copied LeanWorker from
config.command(), config.environment() and config.identities(). Calling the
older RuntimeConfig.worker() imports its own older transport and omits the new
resource metadata.

Workers lacking resource metadata preserve the old interface, but cannot supply
the new capacity admission guarantees. Search assumes one scheduler controls a
session; concurrent independent schedulers can race resource admission.

Evidence/resource_examples.json uses synthetic protocol transitions to expose
scheduling behavior; it does not establish proof correctness or native memory or
speed improvements. All proof success still requires separate native verify.
Native worker memory remains about9GiB in prior measured workloads; wide frontier
capacity, safe eviction/replay recovery, eligible learning data and trained routing
are still open. No new native process, RL run or performance benchmark was launched
for this integration. Read REPORT.txt and ../../notes/engine_gap_audit.txt.

SUBSEQUENT AUTHORIZED NATIVE EXTENSION
The earlier8-task limitation is now closed by ../native_worker:57 native tasks,
49 source-exposed wrappers, actual49 exports/fresh49 requested-target rechecks.
See that directory for separate runtime/cache boundaries and final session02.
The shared transport gained shutdown_grace default2s (positive finite<=5s), with
explicit ACK/forced-termination/teardown receipt fields. Current local suite43
normal +43 optimized and complete original engine47+47 pass; final receipt is
evidence/verification_teardown_final.json. Earlier37/40 logs and reviewed hashes
are preserved history. No RL eligibility or speedup conclusion changed.
