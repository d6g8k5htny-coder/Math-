"""Fail-closed packet replay. --local-only explicitly excludes Git source pins."""
import argparse
import hashlib
import json
import pathlib
import re
import subprocess
import sys


def read_json(path):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError('duplicate JSON key: ' + key)
            result[key] = value
        return result
    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=unique)


def identity(data, entry):
    blob = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    if (len(data) != entry['bytes'] or
            hashlib.sha256(data).hexdigest() != entry['sha256'] or
            blob != entry['git_blob']):
        raise ValueError('source identity mismatch: ' + entry['path'])


def packet_identity(root):
    entries = read_json(root/'SOURCE_FILES.json')['files']
    names = [entry['path'] for entry in entries]
    if len(set(names)) != len(names):
        raise ValueError('duplicate manifest path')
    if sorted(p.name for p in root.iterdir()) != sorted(names+['SOURCE_FILES.json']):
        raise ValueError('packet tree differs from manifest')
    for entry in entries:
        name = entry['path']
        path = root/name
        if pathlib.PurePosixPath(name).name != name or path.is_symlink() or not path.is_file():
            raise ValueError('flat regular packet files required')
        identity(path.read_bytes(), entry)


def source_identity(root):
    pins = read_json(root/'SOURCE_PINS.json')
    entries = [(entry, True) for entry in pins['sources']]
    entries.append((pins['prior_in_project_result'], False))
    for entry, full_identity in entries:
        commit, path = entry['commit'], entry['path']
        pure = pathlib.PurePosixPath(path)
        if not re.fullmatch('[0-9a-f]{40}', commit) or pure.is_absolute() or '..' in pure.parts:
            raise ValueError('unsafe source identity')
        run = subprocess.run(['git', 'show', commit+':'+path], cwd=root,
                             check=True, capture_output=True, timeout=60)
        if full_identity:
            identity(run.stdout, entry)
        else:
            data = run.stdout
            blob = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
            if blob != entry['git_blob']:
                raise ValueError('prior-result blob mismatch: ' + path)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--local-only', action='store_true')
    args = parser.parse_args()
    root = pathlib.Path(__file__).resolve().parent
    packet_identity(root)
    if not args.local_only:
        source_identity(root)
    expected = (root/'RESULTS.json').read_bytes()
    # Literal list is separate from the checker's list so silent removals fail.
    mutants = ['palm-is-conditional', 'cp-rate-is-mean', 'erase-cross-term',
               'third-lower', 'unique-limit', 'wrong-r6-ledger', 'ordinary-poisson']
    for flags in (['-B', '-S'], ['-B', '-O', '-S']):
        subprocess.run([sys.executable, *flags, '-m', 'unittest', 'discover', '-v'],
                       cwd=root, check=True, timeout=120)
        command = [sys.executable, *flags, str(root/'cluster_check.py')]
        run = subprocess.run(command, capture_output=True, check=True, timeout=30)
        if run.stdout != expected:
            raise ValueError('deterministic replay mismatch')
        for mutant in mutants + ['unknown']:
            run = subprocess.run(command+['--mutant', mutant], capture_output=True, timeout=30)
            if run.returncode != (2 if mutant == 'unknown' else 1):
                raise ValueError('negative control not rejected: ' + mutant)
    print(json.dumps({'passed': True, 'source_pins_checked': not args.local_only,
                      'scientific_effect': 'NONE', 'mathematical_acceptance': False}, sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
