"""Documentary bootstrap only; no proof or mathematical execution."""
from datetime import datetime, timezone
import json
from pathlib import Path

BASE = Path('/workspace/scratch/actual-source-regular-local-collar-construct')
PUB = Path('/workspace/scratch/actual-source-regular-local-collar-publication')
go = json.loads((PUB/'ROOT_GO66_INITIAL_CONTEXT_ONLY.json').read_text())
if go['status'] != 'ROOT_GO66_INITIAL_RUNNER_AND_FULL_LITERAL_CONTEXT_ONLY':
    raise RuntimeError('Exact initial context-only GO required')
cache = json.loads((BASE/'FIRST_ID_CACHE.json').read_text())
names = ['FROZEN_CONTEXT.md', 'INITIAL_SOURCE_COMMON.lean.txt', 'BOOTSTRAP_PLAN.md',
         'CONTROL_CONTRACT.md', 'runner/capture66.py', 'runner/record_run.py',
         'runner/bootstrap_context.py']
rows = [cache[str(BASE/name)] for name in names]
record = {'status': 'INITIAL66_FULL_LITERAL_CONTEXT_FROZEN_PENDING_ROOT_FULL_ACCEPTANCE',
          'observed_utc': datetime.now(timezone.utc).isoformat(),
          'creator': go['creator'], 'proper_precode_published_head': go['published_precode_head'],
          'initial_context_and_runner_ids_REUSED_from_preworker_cache': rows,
          'source_proof_fixture_ordinary_harness_body_created': False,
          'helper_proof_text_released': False, 'mathematical_execution_performed': False,
          'mathematics_and_existing_ID_replays': 0,
          'worker_receipt_closes_later': str(BASE/'runs/context-bootstrap001/receipt.json'),
          'outer_receipt_closes_later': str(BASE/'outer/context-bootstrap001/RECEIPT.json'),
          'entry_receipt_closes_later': str(BASE/'entry/context-bootstrap001/RECEIPT.json'),
          'gate': 'Root personally FULL accepts effective complete literal context; optional helper personally FULL ACKs before separate explicit TEXT release.'}
with (BASE/'INITIAL_CONTEXT_FREEZE.json').open('x') as stream:
    json.dump(record, stream, indent=2); stream.write('\n')
print(json.dumps({'status': record['status'], 'observed_utc': record['observed_utc'],
                  'frozen_payloads': len(rows), 'proof_or_math_execution': False}))
