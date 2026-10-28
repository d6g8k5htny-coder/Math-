#!/usr/bin/env python3
"""One integration per immutable original helper; first new identities only."""
import datetime
import hashlib
import json
from pathlib import Path
import sys

TASK = Path('/workspace/scratch/actual-source-morse-local-model-construct')
SOURCE = Path('/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025/SourceActualMorseLocalModel.lean')
REGISTRY = TASK / 'HELPER_INTEGRATIONS.json'
IDENTITIES = TASK / 'ARTIFACT_IDENTITIES.json'
label, section_name, imports_name, provenance_name, frozen_name = sys.argv[1:]
registry = json.loads(REGISTRY.read_text()) if REGISTRY.exists() else {'integrations': []}
if any(x['label'] == label for x in registry['integrations']):
    raise SystemExit('This original section has already been integrated; amend owned source instead.')
store = json.loads(IDENTITIES.read_text()) if IDENTITIES.exists() else {'artifacts': []}
bound = []
for role, name in [('section', section_name), ('imports', imports_name),
                   ('provenance', provenance_name), ('freeze', frozen_name)]:
    path = Path(name)
    data = path.read_bytes()
    snapshot = TASK / 'helper-originals' / label / path.name
    snapshot.parent.mkdir(parents=True, exist_ok=True)
    snapshot.write_bytes(data)
    item = {'role': f'helper_{label}_original_{role}', 'path': str(path),
            'snapshot': str(snapshot), 'bytes': len(data),
            'sha256': hashlib.sha256(data).hexdigest(),
            'first_bound_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'new_sha256_operations': 1}
    store['artifacts'].append(item)
    bound.append(item)
IDENTITIES.write_text(json.dumps(store, indent=2) + '\n')
source = SOURCE.read_text()
for line in Path(imports_name).read_text().splitlines():
    if line.startswith('import ') and line not in source.splitlines():
        source = line + '\n' + source
begin = f'/- BEGIN COMPLETE ORIGINAL HELPER {label} -/'
end = f'/- END COMPLETE ORIGINAL HELPER {label} -/'
block = begin + '\n' + Path(section_name).read_text() + '\n' + end + '\n\n'
closing = 'end I4SourceActualMorseLocalModel'
position = source.rfind(closing)
if position < 0:
    raise SystemExit('Missing owned namespace closing boundary')
source = source[:position] + block + source[position:]
SOURCE.write_text(source)
entry = {'label': label, 'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
         'integration_count': 1, 'helper_executions': 0, 'original_identities': bound,
         'begin_marker': begin, 'end_marker': end,
         'original_section_snapshot': bound[0]['snapshot']}
registry['integrations'].append(entry)
REGISTRY.write_text(json.dumps(registry, indent=2) + '\n')
print(json.dumps(entry, indent=2))
