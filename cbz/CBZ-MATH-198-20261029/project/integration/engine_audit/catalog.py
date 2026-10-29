"""Versioned P15 source-evidence catalog. No Lean process is started here."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sys

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
PRIOR = HERE/'sources/prior_completion'
CATALOG = HERE/'catalog.json'
MANIFEST_SHA = '9ea8b07875b1cdd71bd8209a01739ca7da94a12b74f306875a4fbd2fc4d0aea9'
SPEC_SHA = 'a30d9e6938b64d4e2728c5380d41b3a627cde42448df254069293e3839a41ca6'
ALLOWED_AXIOMS = {'propext', 'Classical.choice', 'Quot.sound'}
SCOPE = ('Saved source and receipt integrity only. No new kernel proof is executed; '
         'this is not a structural worker-v2 proof certificate. All endpoints are '
         'source-exposed proof reuse, training_eligible=false; no discovery or speedup credit.')


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def sha(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024*1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def file_at(root, name):
    """Resolve canonical package paths without following symlink components."""
    require(type(name) is str and bool(name), 'invalid evidence path')
    path = PurePosixPath(name)
    require(not path.is_absolute() and path.as_posix() == name
            and all(part not in ('.', '..') for part in path.parts), 'noncanonical evidence path')
    result = Path(root)
    for part in path.parts:
        result = result/part
        require(not result.is_symlink(), 'symlink in evidence path: '+name)
    require(result.is_file(), 'missing evidence file: '+name)
    return result


def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def canonical_json(value):
    # Python equality equates False with0 and175 with175.0. Their JSON types
    # have different admission meaning and must remain exact at this boundary.
    return json.dumps(value, sort_keys=True, separators=(',', ':'),
                      ensure_ascii=True, allow_nan=False).encode()


def evidence(project=PROJECT, prior=PRIOR):
    """Bind a subset of the prior sealed inventory to the copied formal chain."""
    manifest_path = file_at(prior, 'checksum_manifest.json')
    require(sha(manifest_path) == MANIFEST_SHA, 'prior manifest trust anchor mismatch')
    manifest = read_json(manifest_path)
    require(manifest['schema'] == 'ul-p15-completion-manifest-v1', 'wrong prior manifest schema')
    pinned = manifest['files']
    expected = {p for p in pinned if p.startswith('evidence/final01/')}
    expected.update({'endpoint_map.json', 'audit_targets.json'})
    actual = set()
    for path in Path(prior).rglob('*'):
        require(not path.is_symlink(), 'symlink in prior evidence')
        if path.is_file(): actual.add(path.relative_to(prior).as_posix())
    require(actual == expected|{'checksum_manifest.json'}, 'prior evidence inventory mismatch')
    for name in sorted(expected):
        require(sha(file_at(prior, name)) == pinned[name], 'prior evidence hash mismatch: '+name)
    result = read_json(file_at(prior, 'evidence/final01/results.json'))
    require(result['status'] == 'PASS' and result['cache_was_fresh'] is True
            and result['old_project_cache_on_lean_path'] is False, 'prior build was not fresh passing evidence')
    require(len(result['order']) == len(set(result['order'])) == len(result['records']) == 17,
            'incomplete prior compile graph')
    require(len(result['sources']) == 17, 'incomplete source binding')
    for name, digest in result['sources'].items():
        require(name.startswith('formal/') and pinned[name] == digest, 'source pin mismatch')
        require(sha(file_at(project, name)) == digest, 'current copied formal source drift: '+name)
        require(sha(file_at(prior, 'evidence/final01/frozen_sources/'+name[7:])) == digest,
                'frozen compiled source drift: '+name)
    require(result['sources']['formal/Specifications/P15.lean'] == SPEC_SHA,
            'original specification changed')
    for module, record in zip(result['order'], result['records']):
        require(record['module'] == module, 'compile record order mismatch')
        receipt_name = 'evidence/final01/'+record['receipt']
        receipt_path = file_at(prior, receipt_name)
        receipt = read_json(receipt_path)
        require(all(record.get(key) == value for key, value in receipt.items()),
                'embedded compile receipt mismatch')
        require(receipt['succeeded'] is True and receipt['returncode'] == 0
                and receipt['timed_out'] is False and receipt['output_limit_exceeded'] is False,
                'prior compile failed')
        source_name = 'formal/'+module.replace('.', '/')+'.lean'
        require(record['source_sha256'] == result['sources'][source_name], 'compiled source mismatch')
        for stream, info in receipt['streams'].items():
            stream_path = file_at(prior, str(PurePosixPath(receipt_name).parent/stream))
            require(stream_path.stat().st_size == info['bytes'] and sha(stream_path) == info['sha256'],
                    'compile stream mismatch')
    audit_name = 'evidence/final01/16-Completion.FinalAudit/stdout.txt'
    lines = file_at(prior, audit_name).read_text(encoding='utf-8').splitlines()
    rows = []
    for line in lines:
        if line.startswith('P15_AUDIT|'):
            parts = line.split('|')
            require(len(parts) == 6 and parts[2:5] == ['closed', 'kernel', 'declaration'],
                    'invalid saved theorem audit')
            axioms = sorted(set(filter(None, parts[5].split(','))))
            require(set(axioms) <= ALLOWED_AXIOMS, 'forbidden saved theorem axiom')
            rows.append({'name': parts[1], 'axioms': axioms})
    names = read_json(file_at(prior, 'audit_targets.json'))['names']
    require(rows == result['audited_theorems'] and [r['name'] for r in rows] == names
            and len(names) == len(set(names)) == 53 and 'P15_AUDIT_COMPLETE|53' in lines,
            'incomplete saved theorem audit')
    endpoint_map = read_json(file_at(prior, 'endpoint_map.json'))
    endpoints = endpoint_map['endpoints']
    require(endpoint_map['schema'] == 'ul-p15-completion-endpoint-map-v1'
            and len(endpoints) == len({e['target'] for e in endpoints}) == 49,
            'incomplete original endpoint map')
    return endpoints, {r['name']: r for r in rows}, result, pinned


def make_catalog(project=PROJECT, prior=PRIOR):
    endpoints, audits, build, pinned = evidence(project, prior)
    specification = file_at(project, 'formal/Specifications/P15.lean').read_text(encoding='utf-8')
    entries = []
    for row in endpoints:
        target, theorem, source = row['target'], row['theorem'], row['source']
        require(target.startswith('UniversalLaw.Spec.P15.') and theorem in audits
                and row['status'] == 'closed_fresh_kernel_verified', 'unaccepted original endpoint')
        short = target.rsplit('.', 1)[1]
        matches = list(re.finditer(r'^def '+re.escape(short)+r'\b[^\n]*(?:\n(?!\n)[^\n]*)*', specification, re.M))
        require(len(matches) == 1, 'ambiguous original statement: '+target)
        statement = matches[0].group(0)+'\n'
        source_path = file_at(project, source)
        source_lines = source_path.read_text(encoding='utf-8').splitlines()
        require(type(row['line']) is int and 1 <= row['line'] <= len(source_lines), 'invalid theorem source line')
        require(re.match(r'^\s*theorem '+re.escape(theorem.rsplit('.', 1)[1])+r'\b',
                         source_lines[row['line']-1]) is not None, 'theorem source locator mismatch')
        entries.append({'id': 'p15.'+short, 'target': target, 'theorem': theorem,
                        'statement': statement, 'statement_sha256': hashlib.sha256(statement.encode()).hexdigest(),
                        'specification_source': 'formal/Specifications/P15.lean',
                        'specification_source_sha256': SPEC_SHA,
                        'proof_source': source, 'proof_source_sha256': build['sources'][source],
                        'proof_source_line': row['line'], 'saved_audit': audits[theorem],
                        'status': 'saved_closed_kernel_evidence', 'source_exposed': True,
                        'training_eligible': False})
    return {'schema': 'ul-p15-endpoint-catalog-v1', 'version': 1,
            'provenance': {'prior_package': 'universal-law-p15-completion',
                           'prior_manifest_sha256': MANIFEST_SHA,
                           'original_endpoint_map_sha256': pinned['endpoint_map.json'],
                           'saved_build_results_sha256': pinned['evidence/final01/results.json'],
                           'copied_formal_sources_sha256': build['sources']},
            'scope': SCOPE, 'endpoints': entries}


def verify_catalog(path=CATALOG, *, project=PROJECT, prior=PRIOR):
    catalog = read_json(path)
    require(canonical_json(catalog) == canonical_json(make_catalog(project, prior)),
            'catalog differs from pinned endpoint evidence')
    return catalog


def export_value(catalog, target):
    matches = [r for r in catalog['endpoints'] if target in (r['target'], r['id'])]
    require(len(matches) == 1, 'unknown endpoint target/id')
    canonical = canonical_json(catalog)
    return {'schema': 'ul-saved-endpoint-evidence-v1',
            'catalog_content_sha256': hashlib.sha256(canonical).hexdigest(),
            'endpoint': matches[0], 'scope': SCOPE}


def verify_certificate(path, *, catalog_path=CATALOG, project=PROJECT, prior=PRIOR):
    catalog = verify_catalog(catalog_path, project=project, prior=prior)
    certificate = read_json(path)
    require(type(certificate) is dict and type(certificate.get('endpoint')) is dict,
            'invalid saved endpoint certificate')
    target = certificate['endpoint'].get('target')
    require(canonical_json(certificate) == canonical_json(export_value(catalog, target)),
            'saved endpoint certificate mismatch')
    return certificate


def receipt(*, endpoints=49, certificate=False):
    return {'status': 'PASS', 'endpoints': endpoints, 'certificate_checked': certificate,
            'verification_kind': 'saved_source_and_receipt_integrity',
            'kernel_executed': False, 'structural_worker_certificate': False,
            'training_eligible': False, 'scope': SCOPE}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project-root', type=Path, default=PROJECT)
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('list')
    check = sub.add_parser('verify')
    check.add_argument('--certificate', type=Path)
    export = sub.add_parser('export')
    export.add_argument('target')
    export.add_argument('--output', type=Path, required=True)
    build = sub.add_parser('build')
    build.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.command == 'build':
            value = make_catalog(args.project_root)
            with args.output.open('x', encoding='utf-8') as stream:
                stream.write(json.dumps(value, indent=2, ensure_ascii=False)+'\n')
            output = receipt()
        else:
            value = verify_catalog(project=args.project_root)
            if args.command == 'list': output = value
            elif args.command == 'export':
                certificate = export_value(value, args.target)
                with args.output.open('x', encoding='utf-8') as stream:
                    stream.write(json.dumps(certificate, indent=2, ensure_ascii=False)+'\n')
                output = receipt(endpoints=1, certificate=True)
            else:
                if args.certificate:
                    verify_certificate(args.certificate, project=args.project_root)
                output = receipt(certificate=args.certificate is not None)
        print(json.dumps(output, indent=2, ensure_ascii=False))
        return 0
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps({'status': 'FAILED', 'error': type(exc).__name__, 'reason': str(exc),
                          'kernel_executed': False}), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
