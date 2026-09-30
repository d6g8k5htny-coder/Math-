"""Byte-bound upstream evidence, including explicitly credited prior results."""
from pathlib import Path, PurePosixPath
import argparse
import hashlib
import json
import subprocess


def decode(text):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError('duplicate JSON key: '+key)
            result[key] = value
        return result
    return json.loads(text, object_pairs_hook=pairs)


def identity(data):
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(),
            'git_blob': hashlib.sha1(f'blob {len(data)}\0'.encode()+data).hexdigest()}


def verify_files(root, entries):
    root = Path(root).resolve()
    seen = set()
    ids = set()
    for item in entries:
        rel = PurePosixPath(item['path'])
        if (not rel.parts or rel.is_absolute() or '..' in rel.parts or
                '\\' in item['path'] or str(rel) in seen or item['id'] in ids):
            raise ValueError('unsafe or duplicate source path/id')
        seen.add(str(rel)); ids.add(item['id'])
        path = root.joinpath(*rel.parts)
        if any(root.joinpath(*rel.parts[:i]).is_symlink() for i in range(1, len(rel.parts)+1)):
            raise ValueError('symlink source component')
        if not path.is_file():
            raise ValueError('missing regular source: '+str(rel))
        expected = {key:item[key] for key in ('bytes','sha256','git_blob')}
        if identity(path.read_bytes()) != expected:
            raise ValueError('source byte identity differs: '+item['id'])
    return len(entries)


def verify_git(root, entries):
    for item in entries:
        commit = item['commit']
        if len(commit)!=40 or any(c not in '0123456789abcdef' for c in commit):
            raise ValueError('full lowercase commit identity required')
        target = commit+':'+item['path']
        run = subprocess.run(['git','cat-file','blob',target],cwd=root,capture_output=True,timeout=30)
        if run.returncode or run.stderr:
            raise ValueError('historical source unavailable: '+item['id'])
        if identity(run.stdout) != {key:item[key] for key in ('bytes','sha256','git_blob')}:
            raise ValueError('historical source identity differs: '+item['id'])


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo',type=Path,required=True)
    args=parser.parse_args()
    entries=decode((Path(__file__).resolve().parent/'SOURCE_MAP.json').read_text())['sources']
    count=verify_files(args.repo,entries)
    verify_git(args.repo,entries)
    print(json.dumps({'upstream_files':count,'current_and_historical_bytes':'PASS',
                      'analytic_acceptance':False},sort_keys=True))

if __name__=='__main__':main()
