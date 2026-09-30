"""Replay finite controls and exact packet custody; not theorem acceptance."""
from pathlib import Path
import hashlib
import json
import stat
import subprocess
import sys

HERE = Path(__file__).absolute().parent
REPO = HERE.parents[1]
RADIAL = REPO / 'reviews/radial_moment_corollaries_20260930'


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def read_regular(root, name):
    part = Path(name)
    require(part.parts and not part.is_absolute() and '..' not in part.parts,
            'unsafe source path')
    path = root / part
    cursor = REPO
    require(not cursor.is_symlink() and cursor.is_dir(), 'invalid repository root')
    for component in path.relative_to(REPO).parts:
        cursor = cursor / component
        mode = cursor.lstat().st_mode
        require(not stat.S_ISLNK(mode), 'symlink source path: ' + str(cursor))
        require(stat.S_ISREG(mode) if cursor == path else stat.S_ISDIR(mode),
                'non-regular source path: ' + str(cursor))
    return path.read_bytes()


def verify_lifetime_paths():
    sources = json.loads(read_regular(HERE, 'SOURCES.json'))
    for row in sources['sources']:
        read_regular(HERE, row['local_path'])
    for name in ('PROOF.md', 'check_exact.py', 'LOSS_COROLLARY.md', 'check_loss_exact.py'):
        read_regular(HERE, name)


def verify_radial(root):
    custody = json.loads(read_regular(root, 'COROLLARY_CUSTODY.json'))
    for row in custody['artifacts'] + custody['sources']:
        name = row.get('path', row.get('local_path'))
        raw = read_regular(root, name)
        require(len(raw) == row['bytes'], 'size drift: ' + name)
        require(hashlib.sha256(raw).hexdigest() == row['sha256'], 'SHA256 drift: ' + name)
        if 'git_blob' in row:
            blob = hashlib.sha1(f'blob {len(raw)}\0'.encode() + raw).hexdigest()
            require(blob == row['git_blob'], 'Git blob drift: ' + name)
    return len(custody['artifacts']) + len(custody['sources'])


def main():
    require(sys.version_info[:2] == (3, 11), 'Python 3.11 required')
    verify_lifetime_paths()
    count = verify_radial(RADIAL)
    rows = []
    for flags in ([], ['-O']):
        mode = 'optimized' if flags else 'normal'
        suffix = '_OPTIMIZED' if flags else ''
        lifetime = subprocess.run([sys.executable, '-B', *flags, '-S', str(HERE/'check_exact.py')],
                                  check=True, capture_output=True, text=True)
        current = json.loads(lifetime.stdout)
        expected = json.loads(read_regular(HERE, f'CHECK_RECEIPT{suffix}.json'))
        require(current == expected, 'lifetime replay differs from exact receipt')
        radial = subprocess.run([sys.executable, '-B', *flags, '-S', str(RADIAL/'moment_consequence_checks.py')],
                                check=True, capture_output=True, text=True)
        current_radial = json.loads(radial.stdout)
        require(current_radial == json.loads(read_regular(RADIAL, f'moment-checks-{mode}.json')),
                'radial replay differs from exact receipt')
        loss = subprocess.run([sys.executable, '-B', *flags, '-S', str(HERE/'check_loss_exact.py')],
                              check=True, capture_output=True, text=True)
        current_loss = json.loads(loss.stdout)
        require(current_loss == json.loads(read_regular(HERE, f'LOSS_CHECK_RECEIPT{suffix}.json')),
                'loss replay differs from exact receipt')
        rows.append({'mode': mode,
                     'lifetime_quartics': current['good_quartic_cases'],
                     'lifetime_negative_controls': current['outside_hypothesis_axial_negative_controls'],
                     'normalization_exponents': current['normalization_exponent_cases'],
                     'lifetime_sources': len(current['source_identity_checks']),
                     'radial_tests': current_radial['tests'], 'loss_controls': current_loss})
    print(json.dumps({'passed': True, 'modes': rows, 'radial_custody_records': count,
                      'scientific_effect': 'NONE'}, sort_keys=True))


if __name__ == '__main__':
    main()
