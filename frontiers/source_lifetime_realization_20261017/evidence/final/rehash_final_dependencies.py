"""Re-read every frozen dependency artifact after final execution.

Records byte/path-set equality, including standard library artifacts. Cache
compilation itself is not claimed: these are pinned, pre-existing dependencies.
"""
from datetime import datetime, timezone
import fcntl
import hashlib
import json
from pathlib import Path
from run_final_phase import ROOT, dependency_paths, require


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def main():
    output = ROOT / 'FINAL_DEPENDENCY_REHASH.json'
    require(not output.exists(), 'final dependency rehash already exists')
    inventory_path = ROOT / 'FINAL_DEPENDENCY_ARTIFACTS.json'
    inventory = json.loads(inventory_path.read_text())
    started = datetime.now(timezone.utc).isoformat()
    with (ROOT / 'lean-slot.lock').open('a+') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        expected = inventory['artifacts']
        paths = dependency_paths(inventory['roots'])
        require([str(p) for p in paths] == [x['path'] for x in expected],
                'dependency artifact path set changed')
        mismatches = []
        for i, (p, item) in enumerate(zip(paths, expected)):
            stat = p.stat()
            stamp = [stat.st_size, stat.st_mtime_ns, stat.st_ino]
            digest = sha(p)
            after = p.stat()
            if (p.is_symlink() or digest != item['sha256'] or stamp != item['stat'] or
                    stamp != [after.st_size, after.st_mtime_ns, after.st_ino]):
                mismatches.append({'path': str(p), 'before': item, 'after_sha256': digest,
                                   'after_stat': stamp})
            if (i + 1) % 20000 == 0:
                print(json.dumps({'stage': 'REHASHED', 'count': i + 1}), flush=True)
        final_paths_match = dependency_paths(inventory['roots']) == paths
        report = {'started_utc': started, 'ended_utc': datetime.now(timezone.utc).isoformat(),
                  'inventory_sha256': sha(inventory_path), 'count': len(paths),
                  'total_bytes': sum(x['stat'][0] for x in expected),
                  'final_paths_match': final_paths_match, 'mismatches': mismatches,
                  'status': 'PASS_EXACT_DEPENDENCY_BYTES_AND_PATHSET' if
                    not mismatches and final_paths_match else 'HOLD_DEPENDENCIES_CHANGED',
                  'dependency_source_rebuild': 'NOT_CLAIMED', 'scientific_effect': 'NONE'}
        with output.open('x') as f:
            json.dump(report, f, indent=2)
            f.write('\n')
        print(json.dumps(report), flush=True)
        require(not mismatches and final_paths_match, report['status'])


if __name__ == '__main__':
    main()
