"""Replay finite controls and exact packet custody; not theorem acceptance."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

HERE = Path(__file__).resolve().parent
RADIAL = HERE.parents[1] / 'reviews/radial_moment_corollaries_20260930'


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def verify_radial(root):
    custody = json.loads((root / 'COROLLARY_CUSTODY.json').read_text())
    for row in custody['artifacts'] + custody['sources']:
        name = row.get('path', row.get('local_path'))
        part = Path(name)
        require(not part.is_absolute() and '..' not in part.parts, 'unsafe source path')
        raw = (root / part).read_bytes()
        require(len(raw) == row['bytes'], 'size drift: ' + name)
        require(hashlib.sha256(raw).hexdigest() == row['sha256'], 'SHA256 drift: ' + name)
        if 'git_blob' in row:
            blob = hashlib.sha1(f'blob {len(raw)}\0'.encode() + raw).hexdigest()
            require(blob == row['git_blob'], 'Git blob drift: ' + name)
    return len(custody['artifacts']) + len(custody['sources'])


def main():
    require(sys.version_info[:2] == (3, 11), 'Python 3.11 required')
    count = verify_radial(RADIAL)
    rows = []
    for flags in ([], ['-O']):
        lifetime = subprocess.run([sys.executable, '-B', *flags, '-S', str(HERE/'check_exact.py')],
                                  check=True, capture_output=True, text=True)
        current = json.loads(lifetime.stdout)
        expected = json.loads((HERE/'CHECK_RECEIPT.json').read_text())
        require(current == expected, 'lifetime replay differs from exact receipt')
        radial = subprocess.run([sys.executable, '-B', *flags, '-S', str(RADIAL/'moment_consequence_checks.py')],
                                check=True, capture_output=True, text=True)
        current_radial = json.loads(radial.stdout)
        require(current_radial == json.loads((RADIAL/'moment-checks-normal.json').read_text()),
                'radial replay differs from exact receipt')
        loss = subprocess.run([sys.executable, '-B', *flags, '-S', str(HERE/'check_loss_exact.py')],
                              check=True, capture_output=True, text=True)
        current_loss = json.loads(loss.stdout)
        require(current_loss == json.loads((HERE/'LOSS_CHECK_RECEIPT.json').read_text()),
                'loss replay differs from exact receipt')
        rows.append({'mode': 'optimized' if flags else 'normal',
                     'lifetime_quartics': current['good_quartic_cases'],
                     'lifetime_negative_controls': current['outside_hypothesis_axial_negative_controls'],
                     'normalization_exponents': current['normalization_exponent_cases'],
                     'lifetime_sources': len(current['source_identity_checks']),
                     'radial_tests': current_radial['tests'], 'loss_controls': current_loss})
    print(json.dumps({'passed': True, 'modes': rows, 'radial_custody_records': count,
                      'scientific_effect': 'NONE'}, sort_keys=True))


if __name__ == '__main__':
    main()
