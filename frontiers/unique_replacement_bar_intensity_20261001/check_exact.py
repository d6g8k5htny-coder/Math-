#!/usr/bin/env python3
"""Exact finite fixtures for ROOTS.md; not a continuum theorem certificate."""

from fractions import Fraction as F
import hashlib
import json
from pathlib import Path, PurePosixPath


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


SOURCE_COMMIT = '044d42d5bd7f31df6f7e6b9034d6711e8fb7ee43'
SOURCE_KEYS = {'P', 'CAP', 'E1', 'E2', 'REC', 'CUB', 'ELDER'}


def contained_file(repo, relative):
    require(isinstance(relative, str) and bool(relative), 'source path must be text')
    pure = PurePosixPath(relative)
    require(not pure.is_absolute() and str(pure) == relative
            and all(part not in ('', '.', '..') for part in pure.parts)
            and '\\' not in relative, 'source path must be canonical and relative')
    target = repo
    for part in pure.parts:
        target = target / part
        require(not target.is_symlink(), 'source path must not contain symlinks')
    require(target.is_file(), 'source path must name a regular file')
    resolved = target.resolve(strict=True)
    require(resolved == target and repo in resolved.parents,
            'source path must remain within repository')
    return target


def verify_source_entry(repo, entry):
    require(isinstance(entry, dict), 'source entry must be an object')
    require(entry.get('commit') == SOURCE_COMMIT, 'source commit mismatch')
    target = contained_file(repo, entry.get('path'))
    data = target.read_bytes()
    require(type(entry.get('bytes')) is int and len(data) == entry['bytes'],
            'source byte length mismatch')
    require(hashlib.sha256(data).hexdigest() == entry.get('sha256'),
            'source SHA-256 mismatch')
    blob = hashlib.sha1(b'blob ' + str(len(data)).encode('ascii') + b'\0' + data).hexdigest()
    require(blob == entry.get('blob'), 'source Git blob mismatch')
    return entry['key']


def verify_sources():
    script = Path(__file__).absolute()
    require(not script.is_symlink(), 'check script must not be a symlink')
    repo = script.resolve(strict=True).parents[2]
    relative = 'frontiers/unique_replacement_bar_intensity_20261001/SOURCES.json'
    manifest = json.loads(contained_file(repo, relative).read_text())
    require(manifest.get('source_commit') == SOURCE_COMMIT, 'manifest source cut mismatch')
    entries = manifest.get('sources')
    require(isinstance(entries, list) and len(entries) == 7, 'exactly seven source entries required')
    keys = [verify_source_entry(repo, entry) for entry in entries]
    require(len(set(keys)) == 7 and set(keys) == SOURCE_KEYS, 'source key set mismatch')
    require(len({entry['path'] for entry in entries}) == 7, 'duplicate source paths')
    mutant = dict(entries[0])
    mutant['sha256'] = '0' * 64
    rejected_wrong_digest = False
    try:
        verify_source_entry(repo, mutant)
    except RuntimeError as exc:
        require(str(exc) == 'source SHA-256 mismatch', 'wrong-digest probe failed for another reason')
        rejected_wrong_digest = True
    require(rejected_wrong_digest, 'wrong source digest was not rejected')
    return {'verified_keys': sorted(keys), 'source_commit': SOURCE_COMMIT,
            'checks': ['canonical_relative_paths', 'no_symlinks', 'repository_containment',
                       'byte_lengths', 'sha256', 'git_blob'],
            'wrong_digest_probe': 'REJECTED'}


M = (F(-1, 2), F(0))
S = (F(1, 2), F(0))


def value(p, y):
    k, s, a, beta, c3 = p
    x, z = y
    return (2*k*x**3 - 3*k*x/2 - k/2 + s*z**2/2
            + a*(x**2-F(1, 4))*z/2 + beta*x*z**2/2 + c3*z**3/6)


def gradient(p, y):
    k, s, a, beta, c3 = p
    x, z = y
    return (6*k*x**2-3*k/2+a*x*z+beta*z**2/2,
            s*z+a*(x**2-F(1, 4))/2+beta*x*z+c3*z**2/2)


def determinant(p, y):
    k, s, a, beta, c3 = p
    x, z = y
    xx, xz, zz = 12*k*x+a*z, a*x+beta*z, s+beta*x+c3*z
    return xx*zz-xz*xz


def shear_data(p):
    k, s, a, beta, c3 = p
    b = beta-a*a/(12*k)
    d = (c3-a*beta/(4*k)+a**3/(72*k*k))/2
    sigma = 12*k*d*d+(s-b)**2*(b+2*s)
    delta = 12*k*d*d+b**3
    h = delta-4*b*s*s
    return b, d, sigma, delta, h


def distance_squared(p, y, use_shear=False):
    x, z = y
    if use_shear:
        x += p[2]*z/(12*p[0])
    return (x-M[0])**2+z*z


def admissible(p, y, band, gaps, t, use_shear=False):
    if determinant(p, y) >= 0 or value(p, y) >= 0:
        return False
    d2 = distance_squared(p, y, use_shear)
    lo, hi = band
    if not (lo*lo <= t*t*d2 <= hi*hi):
        return False
    klo, khi = gaps
    height_squared = value(p, y)**2
    return klo*klo*d2**3 <= height_squared <= khi*khi*d2**3


def verify_strict_margins(name, p, roots, band, gaps, t, use_shear=False):
    for y in roots:
        if determinant(p, y) >= 0:
            continue
        d2 = distance_squared(p, y, use_shear)
        require(d2 > 0, name + ': saddle separated from maximum')
        require(all(t*t*d2 != endpoint*endpoint for endpoint in band),
                name + ': strict radius membership margins')
        require(all(value(p, y)**2 != endpoint*endpoint*d2**3 for endpoint in gaps),
                name + ': strict gap membership margins')


def rejected(p, roots, partner, band, gaps, t, *, window_only=False,
             include_partner=False, use_shear=False):
    answer = []
    for y in roots:
        if y == partner and not include_partner:
            continue
        if window_only and y != S and not (-p[0] < value(p, y) < 0):
            continue
        if admissible(p, y, band, gaps, t, use_shear):
            answer.append(y)
    return answer


def verify_fixture(name, p, extra, expected_heights, expected_dets):
    roots = [M, S] + extra
    require(len(set(roots)) == 4, name + ': roots must be distinct')
    b, d, sigma, delta, h = shear_data(p)
    require(p[1] < -abs(b)/2, name + ': strict endpoint typing')
    for label, number in [('D', d), ('Sigma', sigma), ('Delta', delta), ('H', h)]:
        require(number != 0, name + ': excluded ' + label)
    for y in roots:
        require(gradient(p, y) == (0, 0), name + ': critical gradient')
        require(determinant(p, y) != 0, name + ': Morse root')
    require(value(p, M) == 0 and value(p, S) == -p[0], name + ': pin heights')
    for y, expected_height, expected_det in zip(extra, expected_heights, expected_dets):
        require(value(p, y) == expected_height, name + ': extra height')
        require(determinant(p, y) == expected_det, name + ': extra determinant')
        u = y[0]+p[2]*y[1]/(12*p[0])
        require(h*y[1]**2 == 3*p[0]*(b+4*p[1]*u)**2,
                name + ': all-root identity')
    window = [y for y in extra if -p[0] < value(p, y) < 0]
    require(bool(window), name + ': failure window must be nonempty')
    partner = max(window, key=lambda y: value(p, y))
    require(sum(value(p, y) == value(p, partner) for y in window) == 1,
            name + ': unique highest window saddle')
    return roots, partner


def main():
    source_binding = verify_sources()
    p1 = (F(1), F(-21, 10), F(0), F(-3), F(3, 5))
    y11, y12 = (F(-5, 8), F(3, 4)), (F(-5, 6), F(-4, 3))
    roots1, partner1 = verify_fixture('two_window', p1, [y11, y12],
                                      [F(-23, 320), F(-13, 45)],
                                      [F(-27, 4), F(-12)])
    band1, gaps1 = (F(1, 2), F(2)), (F(1, 10), F(2))
    verify_strict_margins('two_window', p1, roots1, band1, gaps1, F(1))
    verify_strict_margins('radius_crossed', p1, roots1, band1, gaps1, F(8, 5))
    count1 = len(rejected(p1, roots1, partner1, band1, gaps1, F(1)))
    require(count1 == 2, 'two_window: full count')
    require(sum(F(1, count1) for _ in range(count1)) == 1,
            'reciprocal multiplicity must count maximum once')
    require(count1 != 1, 'negative control: omission of reciprocal must differ')
    include_actual = len(rejected(p1, roots1, partner1, band1, gaps1, F(1),
                                  include_partner=True))
    require(include_actual == 3, 'negative control: actual partner inclusion')
    crossed = len(rejected(p1, roots1, partner1, band1, gaps1, F(8, 5)))
    require(crossed == 1 and crossed != count1, 'negative control: radius crossing')
    require(len(rejected(p1, roots1, partner1, band1, gaps1, F(1),
                         window_only=True)) == count1,
            'original fixture must not claim below-window coverage')

    p2 = (F(1), F(-39, 16), F(0), F(-3), F(3, 2))
    y21, y22 = (F(-5, 8), F(3, 4)), (F(-37, 24), F(-35, 12))
    roots2, partner2 = verify_fixture('below_window', p2, [y21, y22],
                                      [F(-53, 512), F(-11125, 4608)],
                                      [F(-297, 32), F(-1155, 32)])
    require(value(p2, y22) < -p2[0], 'below_window: genuinely below pin')
    require(determinant(p2, M) == F(45, 8) and determinant(p2, S) == F(-189, 8),
            'below_window: pin determinants')
    d22 = distance_squared(p2, y22)
    q22 = value(p2, y22)**2/d22**3
    require(d22 == F(5525, 576), 'below_window: original coordinate distance')
    require(q22 == F(71289, 10793861), 'below_window: gap ratio squared')
    band2, gaps2 = (F(1, 2), F(4)), (F(1, 100), F(2))
    verify_strict_margins('below_window', p2, roots2, band2, gaps2, F(1))
    count2 = len(rejected(p2, roots2, partner2, band2, gaps2, F(1)))
    window_count = len(rejected(p2, roots2, partner2, band2, gaps2, F(1),
                                window_only=True))
    require(count2 == 2 and window_count == 1,
            'negative control: below-window omission must change count')

    p3 = (F(1), F(-21, 10), F(12), F(9), F(18, 5))
    y31, y32 = (F(-11, 8), F(3, 4)), (F(1, 2), F(-4, 3))
    roots3, partner3 = verify_fixture('nonzero_shear', p3, [y31, y32],
                                      [F(-23, 320), F(-13, 45)],
                                      [F(-27, 4), F(-12)])
    band3, gaps3 = (F(1, 2), F(3, 2)), (F(1, 100), F(2))
    verify_strict_margins('nonzero_shear_physical', p3, roots3, band3, gaps3, F(1))
    verify_strict_margins('nonzero_shear_mutant', p3, roots3, band3, gaps3, F(1), True)
    physical_count = len(rejected(p3, roots3, partner3, band3, gaps3, F(1)))
    shear_count = len(rejected(p3, roots3, partner3, band3, gaps3, F(1),
                               use_shear=True))
    require(physical_count == 1 and shear_count == 2,
            'negative control: sheared distance must change count')

    scale = F(7, 3)
    scaled = tuple(scale*v for v in p2)
    for y in roots2:
        require(gradient(scaled, y) == (0, 0), 'positive scaling preserves roots')
        require(value(scaled, y) == scale*value(p2, y), 'positive scaling of values')
    require(shear_data(scaled)[0] == scale*shear_data(p2)[0], 'scaling of B')
    require(shear_data(scaled)[1] == scale*shear_data(p2)[1], 'scaling of D')

    print(json.dumps({
        'status': 'PASS_EXACT_FINITE_FIXTURES',
        'source_binding': source_binding,
        'arithmetic': 'fractions.Fraction; no floating-point root tests',
        'guards': 'explicit conditionals active under python -O',
        'counts': {'two_window': count1, 'radius_crossed': crossed,
                   'include_actual_mutant': include_actual,
                   'below_window': count2, 'window_only_mutant': window_count,
                   'physical_coordinates': physical_count,
                   'sheared_coordinates_mutant': shear_count},
        'below_window_exact': {'height': str(value(p2, y22)),
                               'distance_squared': str(d22),
                               'gap_ratio_squared': str(q22)},
        'negative_controls': ['omit_reciprocal', 'include_actual_partner',
                              'retain_after_radius_crossing', 'omit_below_window',
                              'use_sheared_distances'],
        'scope': 'Finite fixture checks only; not continuum proof or scientific acceptance.'
    }, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
