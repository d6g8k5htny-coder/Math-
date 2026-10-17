#!/usr/bin/env python3
"""Fail if a tracked text file contains an absolute local home path.

Flagged: macOS per-user homes, Linux /home/<user> (except the GitHub Actions
runner), and Windows C:/Users or C:\\Users homes.  Agent-container scratch
paths under /root are not personal homes and are not flagged.  Files listed in
docs/custody/LOCAL_PATH_MAP.json are allowed only while their git blob is
unchanged, so any edit to such a file that keeps or adds a home path fails.

Patterns are assembled from fragments so this file never contains a literal
home path itself.
"""
import hashlib, json, pathlib, re, subprocess, sys

SEP = '/'
MAC = SEP + 'Us' + 'ers' + SEP
LINUX = SEP + 'ho' + 'me' + SEP
WIN = 'C:' + '[\\\\/]+' + 'Us' + 'ers' + '[\\\\/]+'
RUNNER = 'run' + 'ner'
NAME = r'[A-Za-z0-9._-]+'
PATTERN = re.compile(
    '(?:' + re.escape(MAC) + NAME + ')'
    + '|(?:' + re.escape(LINUX) + '(?!' + RUNNER + r'(?![A-Za-z0-9._-]))' + NAME + ')'
    + '|(?:' + WIN + NAME + ')',
    re.IGNORECASE)
MAP = 'docs/custody/LOCAL_PATH_MAP.json'


def blob(data):
    return hashlib.sha1(b'blob %d\0' % len(data) + data).hexdigest()


def tracked(root):
    out = subprocess.run(['git', '-C', str(root), 'ls-files', '-z'],
                         check=True, capture_output=True).stdout
    return [p for p in out.decode('utf-8', 'surrogateescape').split('\0') if p]


def load_allow(root):
    path = pathlib.Path(root) / MAP
    if not path.is_file():
        return {}
    doc = json.loads(path.read_text(encoding='utf-8'))
    if doc.get('schema') != 'local-path-map/v1':
        raise SystemExit('unexpected schema in ' + MAP)
    return {e['path']: e['git_blob'] for e in doc['files']}


def scan(root, files=None):
    root = pathlib.Path(root)
    allow = load_allow(root)
    findings = []
    for rel in (files if files is not None else tracked(root)):
        p = root / rel
        if p.is_symlink() or not p.is_file():
            continue
        data = p.read_bytes()
        if b'\0' in data[:8192]:
            continue
        if allow.get(rel) == blob(data):
            continue
        text = data.decode('utf-8', 'replace')
        for n, line in enumerate(text.split('\n'), 1):
            if PATTERN.search(line):
                note = ' (allowlisted file changed)' if rel in allow else ''
                findings.append(f'{rel}:{n}: absolute local home path{note}')
    return findings


def main(argv):
    root = argv[1] if len(argv) > 1 else '.'
    findings = scan(root)
    for f in findings:
        print(f)
    print(json.dumps({'findings': len(findings), 'scientific_effect': 'NONE'}))
    return 1 if findings else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
