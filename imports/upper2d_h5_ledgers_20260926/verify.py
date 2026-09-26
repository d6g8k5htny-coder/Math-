#!/usr/bin/env python3
"""Raw-file custody and source-bound loader audit; no numerical theorem check."""
import argparse
import ast
from collections import Counter
from decimal import Decimal, localcontext
import glob
import hashlib
import json
import os
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
SOURCE_HASHES = {
    'hunt_wedges.py': 'f03507da809d91eb6b358c4bf51298ba9d26bb6ab733e801cb5784394b96d48e',
    'hunt_rim.py': 'de73e5fed00782c3709d2f9a8b1cddca23926606a8ef5ffc4cf0de8aefb66f90',
}


def require(test, message):
    if not test:
        raise ValueError(message)


def strict_json(text):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, 'duplicate JSON object name: ' + key)
            result[key] = value
        return result

    def constant(value):
        raise ValueError('nonstandard JSON numeric constant: ' + value)

    return json.loads(text, object_pairs_hook=pairs, parse_constant=constant)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def custody():
    manifest = strict_json((ROOT / 'MANIFEST.json').read_text())
    require(manifest['scientific_effect'] == 'NONE' and manifest['source_labels_adopted'] is False,
            'custody must not adopt scientific labels')
    files = manifest['files']
    names = [item['path'] for item in files]
    require(len(names) == len(set(names)) == 48, 'expected 48 unique raw files')
    actual = {p.relative_to(ROOT).as_posix() for p in (ROOT / 'raw').rglob('*') if p.is_file()}
    require(actual == set(names), 'raw inventory mismatch')
    for item in files:
        name = PurePosixPath(item['path'])
        require(not name.is_absolute() and '..' not in name.parts and
                name.parts[:2] == ('raw', 'H5_closure') and len(name.parts) == 3,
                'unsafe raw path')
        require(not any((ROOT / Path(*name.parts[:i])).is_symlink()
                        for i in range(1, len(name.parts) + 1)), 'symlink rejected')
        raw = (ROOT / name).read_bytes()
        db = digest(b''.join(hashlib.sha256(raw[i:i+4194304]).digest()
                             for i in range(0, len(raw), 4194304)))
        blob = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
        require((len(raw), digest(raw), db, blob) ==
                (item['size'], item['sha256'], item['dropbox_content_hash'], item['git_blob_sha1']),
                'source identity mismatch: ' + item['path'])
    sha_lines = ''.join(item['sha256'] + '  ' + item['path'] + '\n' for item in files)
    require((ROOT / 'MANIFEST.sha256').read_text() == sha_lines, 'SHA256 manifest disagreement')
    return manifest


def probe_key(row):
    part = row.get('part')
    if part == 'sconeprobe':
        return ('scone', row['thS'], row['dS'])
    if part == 'sdiskprobe':
        return ('sdisk', row['thS'])
    if part == 'sringprobe':
        return ('sring', row['thS'], row['dS'])
    if part == 'mbackprobe':
        return ('mfwd' if int(row['thM']) < 90 else 'mbwd', row['thM'], row['dl'])
    return None


def audit(manifest):
    sources = {}
    for name, expected in SOURCE_HASHES.items():
        path = REPO / 'imports/upper2d_stage_e_20260926/raw/STAGE_E' / name
        raw = path.read_bytes()
        require(digest(raw) == expected, 'pinned loader source changed: ' + name)
        sources[name] = ast.parse(raw, filename=name)
    parts = Counter()
    files_by_radius = Counter()
    sites = {}
    rims = {}
    overwrites = []
    failures = []
    rows = 0
    matched = 0
    for path in sorted((ROOT / 'raw/H5_closure').glob('h5_results_*.jsonl')):
        radius = path.name.removeprefix('h5_results_r').split('_', 1)[0]
        require(Decimal(radius).is_finite(), 'invalid filename radius')
        files_by_radius[radius] += 1
        for line_no, line in enumerate(path.read_text().splitlines(), 1):
            if not line.strip():
                continue
            row = strict_json(line)
            require(isinstance(row, dict), 'expected JSON object')
            rows += 1
            part = row.get('part')
            parts[str(part)] += 1
            origin = {'file': path.relative_to(ROOT).as_posix(), 'line': line_no,
                      'filename_radius': radius, 'part': part}
            if 'fail' in str(part).lower():
                failures.append(dict(origin, row=row))
            key = probe_key(row)
            if key is not None:
                value = Decimal(row['rho_hi'])
                require(value.is_finite(), 'nonfinite selected density')
                matched += 1
                record = dict(origin, key=list(key), rho_hi=row['rho_hi'])
                if key in sites:
                    previous = sites[key]
                    overwrites.append({'key': list(key), 'previous': previous, 'replacement': record,
                                       'value_changed': Decimal(previous['rho_hi']) != value,
                                       'radius_changed': previous['filename_radius'] != radius})
                sites[key] = record
            if part == 'rimprobe':
                rims[row['th']] = dict(origin, rho_hi=row['rho_hi'])
    maxima = {}
    for key, record in sites.items():
        family = key[0]
        value = Decimal(record['rho_hi'])
        maxima[family] = max(maxima.get(family, Decimal(0)), value)
    values = (2 * maxima['scone'], 2 * maxima['mfwd'], 2 * maxima['mbwd'],
              2 * max(Decimal(v['rho_hi']) for k, v in sites.items()
                      if k[0] in ('sdisk', 'sring', 'scone')))
    # Execute only the hash-pinned, inspected loader function. No source imports,
    # QMC, covariance code or main() is executed. Decimal replaces mpf solely
    # for exact input-selection/decimal arithmetic; this is not mpmath replay.
    function = next(n for n in sources['hunt_wedges.py'].body
                    if isinstance(n, ast.FunctionDef) and n.name == 'merged_constants')
    module = ast.Module(body=[function], type_ignores=[])
    namespace = {'glob': glob, 'json': json, 'os': os, 'mpf': Decimal,
                 'H5DIR': str(ROOT / 'raw/H5_closure')}
    exec(compile(module, '<hash-pinned merged_constants only>', 'exec'), namespace)
    require(tuple(namespace['merged_constants']()) == values, 'original loader selection disagreement')
    literal = next(n for n in sources['hunt_rim.py'].body if isinstance(n, ast.Assign)
                   and any(isinstance(t, ast.Name) and t.id == 'RHO_HI' for t in n.targets))
    constants = ast.literal_eval(literal.value)
    comparisons = []
    for angle, text in sorted(constants.items()):
        require(angle in rims, 'rim literal has no ledger row')
        row = rims[angle]
        comparisons.append({'angle': angle, 'script_literal': text, 'ledger_winner': row,
                            'exact_decimal_match': Decimal(text) == Decimal(row['rho_hi'])})
    return {
        'scope': 'custody and exact-decimal loader selection only; no QMC or proof validation',
        'scientific_effect': 'NONE', 'raw_files': len(manifest['files']),
        'raw_bytes': sum(x['size'] for x in manifest['files']),
        'files_by_filename_radius': dict(sorted(files_by_radius.items())),
        'rows': rows, 'parts': dict(sorted(parts.items())), 'matching_probe_rows': matched,
        'selected_sites': len(sites), 'ignored_rows': rows - matched,
        'overwrites': len(overwrites),
        'value_changing_overwrites': sum(o['value_changed'] for o in overwrites),
        'cross_radius_overwrites': sum(o['radius_changed'] for o in overwrites),
        'selected_sites_by_filename_radius': dict(sorted(Counter(
            r['filename_radius'] for r in sites.values()).items())),
        'decimal_constants': dict(zip(('scone_C', 'mfwd_C', 'mbwd_C', 'sdisk_C'), map(str, values))),
        'original_loader_decimal_crosscheck': True,
        'selected': sorted(sites.values(), key=lambda x: json.dumps(x['key'])),
        'overwrite_history': overwrites, 'ignored_failure_rows': failures,
        'rim_literal_comparisons': comparisons,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--emit', action='store_true', help='emit regenerated receipt to stdout')
    args = parser.parse_args()
    with localcontext() as context:
        context.prec = 120
        result = audit(custody())
    if args.emit:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        expected = strict_json((ROOT / 'SELECTION_AUDIT.json').read_text())
        require(result == expected, 'selection receipt changed')
        print('CUSTODY AND SELECTION VERIFIED: 48 raw ledgers; scientific effect NONE')
        print('No numerical enclosure, QMC result, or mathematical theorem certified.')


if __name__ == '__main__':
    main()
