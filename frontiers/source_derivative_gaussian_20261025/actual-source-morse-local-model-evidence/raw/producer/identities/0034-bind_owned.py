"""First identities for genuinely new owned artifacts; reuse identical bytes."""
import datetime
import hashlib
import json
from pathlib import Path
import sys

TASK = Path('/workspace/scratch/actual-source-morse-local-model-construct')
IDENTITIES = TASK / 'ARTIFACT_IDENTITIES.json'

def bind(path, role):
    path = Path(path)
    data = path.read_bytes()
    store = json.loads(IDENTITIES.read_text()) if IDENTITIES.exists() else {'artifacts': []}
    for item in store['artifacts']:
        if item['role'] == role and Path(item['snapshot']).read_bytes() == data:
            return dict(item, reused_identity=True)
    snapshot = TASK / 'identities' / f'{len(store["artifacts"])+1:04d}-{path.name}'
    snapshot.write_bytes(data)
    item = {'role': role, 'path': str(path), 'snapshot': str(snapshot),
            'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(),
            'first_bound_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'new_sha256_operations': 1}
    store['artifacts'].append(item)
    IDENTITIES.write_text(json.dumps(store, indent=2) + '\n')
    return dict(item, reused_identity=False)

if __name__ == '__main__':
    result = [bind(Path(__file__), 'owned_artifact_binding_harness')]
    for role, path in zip(sys.argv[1::2], sys.argv[2::2]):
        result.append(bind(path, role))
    print(json.dumps(result, indent=2))
