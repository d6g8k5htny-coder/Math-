"""ONE ordinary Controls integration from the independently frozen text."""
import datetime
import json
from pathlib import Path
from bind_owned import bind

TASK = Path('/workspace/scratch/actual-source-morse-local-model-construct')
ORIGINAL = Path('/workspace/scratch/morse-local-model-actual-fixtures-text')
RECEIPT = TASK / 'CONTROLS_INTEGRATION.json'
if RECEIPT.exists():
    raise SystemExit('Controls original already integrated; amend actual ordinary source instead.')
identities = []
for suffix, role in [('SECTION.lean.txt', 'section'), ('IMPORTS.txt', 'imports'),
                     ('PROVENANCE.md', 'provenance'), ('FROZEN.json', 'freeze')]:
    path = ORIGINAL / ('CONTROLS_' + suffix)
    identities.append(bind(path, 'helper_Controls_original_' + role))
    target = TASK / 'controls-originals' / path.name
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(path.read_bytes())
source = TASK / 'controls' / 'MorseLocalModelControls.lean'
source.parent.mkdir(parents=True, exist_ok=True)
source.write_text((ORIGINAL / 'CONTROLS_IMPORTS.txt').read_text() + '\n' +
                  (ORIGINAL / 'CONTROLS_SECTION.lean.txt').read_text())
record = {'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'integration_count': 1, 'helper_executions': 0,
          'source': str(source), 'original_identities': identities,
          'coverage': 'ordinary Controls compilation only, not production kernel'}
RECEIPT.write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps(record, indent=2))
