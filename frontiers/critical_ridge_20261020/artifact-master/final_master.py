#!/usr/bin/env python3
"""C299 final native artifact master: no Lean, network, or archive-builder execution.

Default invocation is once-only and must be authorized by the source owner after
stable inputs. Separate unittest controls exercise parser/receipt guards using
temporary bytes; they do not create a final-master start/result or accept delivery.
See FINAL_MASTER_NOTES.md for the explicit input-envelope contract.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import re
import stat
import sys
import zipfile

ROOT = Path(__file__).absolute().parent
PREFIX = 'frontiers/critical_ridge_20261020/'
WORKFLOW = '.github/workflows/c299-critical-ridge.yml'
REPOSITORY = 'd6g8k5htny-coder/Math-'
MODULES = ('Lifetime', 'TorusTopology', 'MorseFiniteCritical',
           'CriticalRidge', 'CriticalRidgeAxiomAudit')
NEGATIVES = ('WithoutCriticality', 'WithoutNegativeDefiniteness')
SOURCE_PATHS = {f'project/{m}.lean' for m in MODULES} | {
    f'negative-project/{m}.lean' for m in NEGATIVES}
AXIOMS = {'propext', 'Classical.choice', 'Quot.sound'}
REQUIRED = {
    'UniversalLaw.Spec.Lifetime.' + n for n in ('IsSmooth', 'IsCriticalPoint', 'hessian')
} | {'TorusMorseFinite.literal_hessian_eq_fderiv'} | {
    'TorusCriticalRidge.' + n for n in (
        'restrictCovector', 'ridgeAddition', 'negativePartialGradient', 'negativeHessianBlock',
        'negativeHessianBlock_apply', 'negativeHessianBlock_isInvertible',
        'negativePartialGradient_contDiff', 'negativePartialGradient_hasFDerivAt',
        'exists_negative_partial_gradient_ridge')
}
PINS = {
    'plausible': '118aa17ee84656b8bd727fef7c458ee8c833385c',
    'LeanSearchClient': 'ddf04cf3949fa556442341e87d47f9f6e6074707',
    'importGraph': 'e928b72544873815af278d38681b31c0293588e3',
    'proofwidgets': '106ff4fafc74ef4ac99d81dbf3ab399118f497a5',
    'aesop': '355695d523e41d0554926416cba2a2b3544fbbc9',
    'Qq': '6a489d9af5d0c47e5b259e2e8bcdfc1811b5a259',
    'batteries': 'f2effa3d803fda822b1f97b806c47cf2adfbcbc2',
    'Cli': 'e92c9f15fdfacc8536f31cfb3b7ad26c3c8cd204',
    'mathlib': 'd13f23b723b8a846827a245b89c10fc7d3f11612',
}
SUPPORT_PATHS = {WORKFLOW, PREFIX + 'c299_hosted_verify.py',
                 PREFIX + 'test_c299_hosted_verify.py'}
REVIEW_VERDICTS = {
    'source_review': 'ACCEPT_SCOPED_SOURCE',
    'engineering_review': 'ACCEPT_SCOPED_ENGINEERING_SOURCE',
    'negative_qualification_review': 'ACCEPT_SCOPED_NEGATIVE_DIAGNOSTICS',
    'hosted_artifact_review': 'ACCEPT_SCOPED_FORMAL_HOSTED',
    'master_source_review': 'PASS_SCOPED_MASTER_SOURCE_REVIEW',
}
ENVIRONMENT_POLICY = (
    'Remove inherited LEAN*, LAKE*, LD_* and DYLD_* overrides, except the '
    'Lake-provided LEAN_PATH; prepend the fresh local object directory to that '
    'path and set LEAN_NUM_THREADS=2. Retain declared PATH for launcher lookup. '
    'Other inherited variables remain available but are not recorded. Record '
    'only selected non-secret path/thread values and removed variable names.')


def now():
    return datetime.now(timezone.utc).isoformat()


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def identity(raw):
    return {'bytes': len(raw), 'sha256': sha(raw)}


def git_blob(raw):
    return hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()


def need(ok, message):
    if not ok:
        raise ValueError(message)


def json_bytes(raw):
    def unique(rows):
        result = {}
        for key, value in rows:
            need(key not in result, 'duplicate JSON key: ' + key)
            result[key] = value
        return result
    return json.loads(raw.decode('utf8'), object_pairs_hook=unique,
                      parse_constant=lambda s: (_ for _ in ()).throw(ValueError('nonfinite JSON: ' + s)))


def member_path(name):
    need(isinstance(name, str) and name and not name.startswith('/')
         and '\\' not in name and ':' not in name
         and all(ord(c) >= 32 and ord(c) != 127 for c in name), 'unsafe relative path')
    need(all(p not in ('', '.', '..') for p in name.split('/')), 'unsafe relative component')
    return Path(*PurePosixPath(name).parts)


def measured_audit(text, modules=MODULES[:-1], required=REQUIRED):
    """Independent whole-record regex parser, including multiline axiom arrays."""
    token = re.compile(
        r'(?m)^CRITICAL_RIDGE_AUDIT_MODULE (?P<module>\S+) COUNT (?P<count>\d+)\s*$'
        r'|^CRITICAL_RIDGE_AUDIT_DECL (?P<name>\S+) AXIOMS \[(?P<axioms>[^\[\]]{0,4096})\][ \t]*$'
        r'|^CRITICAL_RIDGE_AUDIT_STANDARD_ONLY_PASS COUNT (?P<total>\d+)\s*$')
    counts, names, all_names, current, total = {}, {}, set(), None, None
    consumed = 0
    for match in token.finditer(text):
        consumed += 1
        if match['module'] is not None:
            current = match['module']
            need(current not in counts and current in modules and total is None,
                 'duplicate, unexpected or late audit module')
            count = int(match['count'])
            need(count > 0, 'empty audit module')
            counts[current], names[current] = count, []
        elif match['name'] is not None:
            name = match['name']
            need(current in counts and total is None and name not in all_names,
                 'duplicate or misplaced audit declaration')
            axs = {s.strip() for s in match['axioms'].split(',') if s.strip()}
            need(axs <= AXIOMS, 'forbidden transitive axiom')
            names[current].append(name)
            all_names.add(name)
        else:
            need(total is None, 'duplicate audit completion marker')
            total = int(match['total'])
    marker_count = len(re.findall(
        r'CRITICAL_RIDGE_AUDIT_(?:MODULE|DECL|STANDARD_ONLY_PASS)\b', text))
    all_markers = re.findall(r'CRITICAL_RIDGE_AUDIT_([^\s]+)', text)
    need(set(all_markers) <= {'MODULE', 'DECL', 'STANDARD_ONLY_PASS', 'PROGRESS'},
         'unknown audit marker')
    need(consumed == marker_count, 'malformed, interrupted or truncated audit record')
    need(tuple(counts) == tuple(modules) and all(len(names[m]) == counts[m] for m in counts)
         and total == len(all_names) == sum(counts.values()) and set(required) <= all_names,
         'incomplete census or missing required declaration')
    return {'module_counts': counts, 'declaration_count': total,
            'module_declarations': names, 'required_targets': sorted(required),
            'allowed_axioms': sorted(AXIOMS)}


def canonical_digest(value):
    return sha(json.dumps(value, sort_keys=True, separators=(',', ':')).encode())


def validate_expectations(expected):
    required = {'pr', 'head', 'base', 'tree', 'tested_commit', 'tested_tree',
                'run_id', 'run_attempt', 'source_manifest_sha256', 'support_sha256',
                'module_counts', 'required_ci_names', 'negative_qualification'}
    need(isinstance(expected, dict) and set(expected) == required, 'incomplete final expectations')
    for key in ('pr', 'run_id', 'run_attempt'):
        need(type(expected[key]) is int and expected[key] > 0, 'invalid final identity: ' + key)
    for key in ('head', 'base', 'tree', 'tested_commit', 'tested_tree'):
        need(isinstance(expected[key], str) and re.fullmatch('[0-9a-f]{40}', expected[key]),
             'invalid frozen Git identity: ' + key)
    need(re.fullmatch('[0-9a-f]{64}', expected['source_manifest_sha256']) is not None,
         'invalid source manifest hash')
    support = expected['support_sha256']
    need(set(support) == SUPPORT_PATHS and all(re.fullmatch('[0-9a-f]{64}', x) for x in support.values()),
         'incomplete final support identities')
    counts = expected['module_counts']
    need(set(counts) == set(MODULES[:-1]) and all(type(n) is int and n > 0 for n in counts.values()),
         'missing actual module census')
    roles = expected['required_ci_names']
    need(isinstance(roles, list) and len(roles) == len(set(roles))
         and all(isinstance(x, str) and x for x in roles)
         and {'downstream-replay', 'formal / formal-evidence', 'math-downstream-gates'} <= set(roles),
         'incomplete applicable CI inventory')
    qualification = expected['negative_qualification']
    need(set(qualification) == {'status', 'diagnostics'} and qualification['status'] == 'QUALIFIED'
         and set(qualification['diagnostics']) == set(NEGATIVES), 'actual negative qualification pending')
    for record in qualification['diagnostics'].values():
        need(set(record) == {'stdout_sha256', 'stderr_sha256', 'expression', 'actual', 'expected'}
             and all(isinstance(x, str) and x for x in record.values())
             and all(re.fullmatch('[0-9a-f]{64}', record[k]) for k in ('stdout_sha256', 'stderr_sha256')),
             'incomplete actual negative diagnostic record')


def qualified_negative(name, code, stdout, stderr, qualified):
    """Independent section parser and complete same-ridge missing-premise check.

    The exact observed sections/hashes are frozen by the owner after diagnostic
    review. They cannot replace the semantic shape checks below. Presentation
    changes require a reviewed source change, not an envelope-only bypass.
    """
    need(name in NEGATIVES, 'unexpected negative control')
    need(sha(stdout) == qualified['stdout_sha256'] and sha(stderr) == qualified['stderr_sha256'],
         'negative streams differ from reviewed actual diagnostics')
    text = (stdout + b'\n' + stderr).decode('utf8').strip()
    flat = ' '.join(text.split())
    forbidden = ('unknown identifier', 'unknown module', 'file not found', 'no such file',
                 'memory_exception', 'out of memory', 'unexpected token', 'unsolved goals',
                 'maximum recursion', 'maximum heartbeats', 'failed to', 'panic', 'sorry')
    need(code == 1 and text.count('error:') == 1 and all(w not in flat.lower() for w in forbidden),
         'unrelated negative-control failure')
    header, separator, remainder = text.partition('\n')
    need(separator and re.fullmatch(r'[^\n]*' + re.escape(name) + r'\.lean:\d+:\d+: error: Type mismatch', header),
         'negative diagnostic names a different source or error')
    pieces = re.split(r'\nhas type\s*\n|\nbut is expected to have type\s*\n', remainder)
    need(len(pieces) == 3, 'negative diagnostic must have one actual and expected type section')
    expression, actual, expected_type = (' '.join(piece.split()) for piece in pieces)
    need(all(value == qualified[key] for key, value in
             (('expression', expression), ('actual', actual), ('expected', expected_type))),
         'actual diagnostic sections differ from reviewed sections')
    target = 'TorusCriticalRidge.exists_negative_partial_gradient_ridge'
    if name == 'WithoutCriticality':
        need(expression == 'fun hcritical => ' + target + ' f p V hsmooth hcritical hneg',
             'criticality omission is not the actual theorem lambda')
        premise = 'IsCriticalPoint d f p'
    else:
        need(expression == target + ' f p V hsmooth hcritical',
             'negative-definiteness omission is not the actual theorem application')
        premise = '(∀ v ∈ V, v ≠ 0 → hessian d f p v v < 0)'
    need(actual == premise + ' → ' + expected_type, 'wrong missing premise or actual function conclusion')
    # Deliberately fixed source semantics; actual display variants need review.
    conclusion = (r'∃ r, r 0 = 0 ∧ ContDiffAt ℝ 2 r 0 ∧ '
                  r'\(∀ᶠ w in 𝓝 0, ∀ \(z : ↥V\), \(fderiv ℝ f \(p \+ w \+ ↑\(r w\)\)\) ↑z = 0\) ∧ '
                  r'∀ \(w : E d\) \(z : ↥V\), hessian d f p \(w \+ ↑\(\(fderiv ℝ r 0\) w\)\) ↑z = 0')
    need(re.fullmatch(conclusion, expected_type) is not None, 'wrong four-part same-ridge conclusion')


def environment_binding(report, record, object_directory):
    contract = report.get('environment_contract')
    need(isinstance(contract, dict) and set(contract) == {
        'policy', 'retained_lake_lean_path', 'removed_variable_names', 'selected_environment', 'sha256'},
        'missing exact environment contract')
    body = {k: val for k, val in contract.items() if k != 'sha256'}
    need(contract['policy'] == ENVIRONMENT_POLICY and contract['sha256'] == canonical_digest(body),
         'environment contract policy or digest mismatch')
    selected = contract['selected_environment']
    need(set(selected) == {'PATH', 'LEAN_PATH', 'LEAN_NUM_THREADS'}
         and all(isinstance(x, str) and x for x in selected.values()), 'incomplete selected environment')
    inherited = contract['retained_lake_lean_path']
    need(isinstance(inherited, str) and PurePosixPath(object_directory).is_absolute()
         and '..' not in PurePosixPath(object_directory).parts
         and selected['LEAN_PATH'] == object_directory + (':' + inherited if inherited else '')
         and selected['LEAN_NUM_THREADS'] == '2', 'fresh-object precedence or thread count mismatch')
    removed = contract['removed_variable_names']
    need(isinstance(removed, list) and all(isinstance(k, str) for k in removed)
         and removed == sorted(set(removed)) and all(k.startswith(('LEAN', 'LAKE', 'LD_', 'DYLD_'))
             and k != 'LEAN_PATH' for k in removed), 'invalid removed-variable name record')
    measured = {'selected_environment': record.get('selected_environment'),
                'unexpected_override_names': record.get('unexpected_override_names')}
    need(record.get('selected_environment') == selected
         and record.get('environment_contract_sha256') == contract['sha256']
         and record.get('unexpected_override_names') == []
         and record.get('environment_validation_error') is None
         and record.get('environment_sha256') == canonical_digest(measured),
         'phase environment differs from bound contract')


def runtime_binding(report, prefix_stdout):
    prefix = PurePosixPath(prefix_stdout.decode('utf8').strip())
    need(prefix.is_absolute() and '..' not in prefix.parts, 'invalid printed runtime prefix')
    for name in ('lean', 'leanchecker'):
        need(report['runtimes'][name]['path'] == str(prefix / 'bin' / name),
             'measured runtime path does not derive from printed prefix')
    launcher = report['lean_launcher']
    need(type(launcher['bytes']) is int and launcher['bytes'] > 0
         and re.fullmatch('[0-9a-f]{64}', launcher['sha256']) is not None
         and Path(launcher['path']).is_absolute(), 'invalid executor-measured launcher identity')
    if launcher['path'] == report['runtimes']['lean']['path']:
        need(launcher == report['runtimes']['lean'], 'same-path launcher/runtime records differ')


def final_review_records(acceptance):
    reviews = acceptance['reviews']
    need(set(reviews) == set(REVIEW_VERDICTS), 'missing role-specific final review')
    records = []
    for role, verdict in REVIEW_VERDICTS.items():
        review = reviews[role]
        need(set(review) == {'path', 'bytes', 'sha256', 'verdict'} and review['verdict'] == verdict,
             'nonpassing or incomplete final review: ' + role)
        records.append(review)
    need(len({r['path'] for r in records}) == len(records), 'final review paths are not distinct')
    return records


class Master:
    def __init__(self, root=ROOT):
        self.root = Path(root).absolute()
        self.checks, self.observed = [], {}

    def check(self, label, condition):
        self.checks.append({'name': label, 'pass': bool(condition)})
        need(condition, label)

    def path(self, value):
        p = Path(value)
        if not p.is_absolute():
            p = self.root / member_path(str(value))
        self.check('input contained in native continuation: ' + str(value),
                   p.is_relative_to(self.root) and '..' not in p.parts)
        return p

    def read(self, value):
        p = self.path(value)
        self.check('regular nonsymlink input: ' + str(p),
                   p.is_file() and all(not q.is_symlink() for q in (p, *p.parents)))
        raw = p.read_bytes()
        spec = identity(raw)
        self.check('stable reread: ' + str(p), p not in self.observed or self.observed[p] == spec)
        self.observed[p] = spec
        return raw

    def doc(self, value):
        return json_bytes(self.read(value))

    def bound(self, spec):
        self.check('complete bound-input identity', set(spec) == {'path', 'bytes', 'sha256'}
                   and type(spec['bytes']) is int and spec['bytes'] >= 0
                   and re.fullmatch('[0-9a-f]{64}', spec['sha256']) is not None)
        raw = self.read(spec['path'])
        self.check('bound input bytes: ' + spec['path'],
                   identity(raw) == {k: spec[k] for k in ('bytes', 'sha256')})
        return raw

    def verify_publication(self, envelope):
        gh = json_bytes(self.bound(envelope['github_readback']))
        self.check('exact public PR head and tree', gh['repository'] == REPOSITORY
                   and gh['pr'] == envelope['expected']['pr'] and re.fullmatch('[0-9a-f]{40}', gh['head'])
                   and re.fullmatch('[0-9a-f]{40}', gh['tree'])
                   and gh['tree_untruncated'] is True and gh['native_remote_byte_equality'] is True
                   and gh['pr_body_exact_readback'] is True
                   and all(gh[k] == envelope['expected'][k] for k in ('pr', 'head', 'base', 'tree')))
        files = gh['files']
        self.check('complete final public byte readbacks', len(files) == gh['files_count']
                   and len({r['path'] for r in files}) == len(files) and len(files) > 0)
        published = {}
        inputs = json_bytes(self.bound(envelope['publication_inputs']))
        native_inputs = {r['path']: r for r in inputs}
        self.check('publication input path set', len(native_inputs) == len(inputs) == len(files)
                   and set(native_inputs) == {r['path'] for r in files})
        for row in files:
            rel = row['path']
            member_path(rel)
            self.check('bounded public path: ' + rel, rel == WORKFLOW or rel.startswith(PREFIX))
            raw, remote = self.read(row['local']), self.read(row['remote_file'])
            measured, blob = identity(raw), git_blob(raw)
            self.check('native/remote/Git-tree bytes: ' + rel,
                       raw == remote and row['raw_byte_match'] is True
                       and measured == {'bytes': row['bytes'], 'sha256': row['sha256']}
                       and row['remote_sha256'] == measured['sha256']
                       and row['git_blob'] == row['tree_blob'] == blob)
            original = native_inputs[rel]
            self.check('original publication binding: ' + rel, row['local'] == original['local']
                       and measured == {k: original[k] for k in ('bytes', 'sha256')})
            if 'reused_same_git_blob' in row:
                self.check('honest raw-byte readback ref: ' + rel,
                           re.fullmatch('[0-9a-f]{40}', row['byte_read_ref']) is not None
                           and (row['byte_read_ref'] != gh['head'] if row['reused_same_git_blob']
                                else row['byte_read_ref'] == gh['head']))
            published[rel] = raw
        self.check('published byte total', sum(len(b) for b in published.values()) == gh['bytes'])
        native_packet = self.path(envelope['publication_directory'])
        actual_packet = {PREFIX + str(p.relative_to(native_packet))
                         for p in native_packet.rglob('*') if p.is_file()}
        self.check('complete native publication tree', actual_packet | {WORKFLOW} == set(published))
        for rel in actual_packet:
            self.check('final composite/published bytes: ' + rel,
                       self.read(native_packet / member_path(rel[len(PREFIX):])) == published[rel])
        commit = json_bytes(self.bound(envelope['github_commit']))
        ref = json_bytes(self.bound(envelope['github_ref']))
        pr = json_bytes(self.bound(envelope['github_pr']))
        tree = json_bytes(self.bound(envelope['github_tree']))
        self.check('native current Git tree identity', tree['sha'] == gh['tree']
                   and tree.get('truncated') is False)
        tree_rows = {r['path']: r for r in tree['tree']}
        self.check('unique native tree paths', len(tree_rows) == len(tree['tree']))
        used_paths = set(published) | {'formal/lean-toolchain', 'formal/lakefile.toml', 'formal/lake-manifest.json'}
        self.check('native tree covers every used delivery/config blob', used_paths <= set(tree_rows))
        if 'scope_note' in tree:
            self.check('explicit complete used-path tree projection', set(tree_rows) == used_paths
                       and isinstance(tree['scope_note'], str) and tree['scope_note'].strip()
                       and type(tree['native_entry_count']) is int
                       and tree['native_entry_count'] >= len(tree_rows))
        for row in files:
            self.check('native current tree blob: ' + row['path'], row['path'] in tree_rows
                       and tree_rows[row['path']]['type'] == 'blob'
                       and tree_rows[row['path']]['sha'] == row['tree_blob'])
        self.check('native GitHub commit/ref/PR evidence',
                   commit['sha'] == ref['object']['sha'] == pr['head']['sha'] == gh['head']
                   and commit['tree']['sha'] == gh['tree'] and pr['number'] == envelope['expected']['pr']
                   and pr['base']['sha'] == gh['base']
                   and pr['head']['repo']['full_name'] == REPOSITORY)
        return gh, published, tree_rows

    def verify_sources_reviews(self, envelope, published):
        expected = envelope['expected']
        raw = self.bound(envelope['source_manifest'])
        self.check('frozen source manifest identity', sha(raw) == expected['source_manifest_sha256']
                   and raw == published[PREFIX + 'HOSTED_SOURCE_MANIFEST.json'])
        manifest = json_bytes(raw)
        self.check('exact five modules and two controls', manifest['schema_version'] == 1
                   and manifest['scientific_effect'] == 'NONE' and set(manifest['files']) == SOURCE_PATHS)
        for rel, spec in manifest['files'].items():
            self.check('frozen published Lean identity: ' + rel, identity(published[PREFIX + rel]) == spec)
        origins = manifest['source_origins']
        self.check('complete input source origins', set(origins) == set(MODULES[:3]))
        upstream = json_bytes(self.bound(envelope['upstream_readback']))
        self.check('exact upstream byte-readback set', isinstance(upstream, list)
                   and len(upstream) == 3 and {r['module'] for r in upstream} == set(MODULES[:3]))
        for row in upstream:
            origin = origins[row['module']]
            raw_origin = self.bound(row['raw_file'])
            self.check('source-bound remote upstream bytes: ' + row['module'],
                       origin == {'commit': row['commit'], 'path': row['path']}
                       and re.fullmatch('[0-9a-f]{40}', row['commit']) is not None
                       and raw_origin == published[PREFIX + 'project/' + row['module'] + '.lean']
                       and git_blob(raw_origin) == row['git_blob'] and row['raw_byte_match'] is True)
            member_path(row['path'])
        for rel, digest in expected['support_sha256'].items():
            self.check('reviewed final hosted support: ' + rel, sha(published[rel]) == digest)
        acceptance = json_bytes(self.bound(envelope['root_acceptance']))
        self.check('scoped exact formal evidence acceptance',
                   acceptance['verdict'] == 'ACCEPT_SCOPED_FORMAL_EVIDENCE'
                   and acceptance['expected'] == expected)
        self.check('actual nonauthor identity and exposure',
                   all(isinstance(acceptance.get(k), str) and acceptance[k].strip()
                       for k in ('author', 'reviewer', 'root', 'exposure'))
                   and acceptance['author'] != acceptance['reviewer'])
        self.check('no manufactured human, independent or scientific credit',
                   acceptance['human_review_credit'] == acceptance['organizational_independence_credit'] == 0
                   and acceptance['scientific_effect'] == 'NONE')
        for review in final_review_records(acceptance):
            self.check('nonempty bound final review: ' + review['path'],
                       bool(self.bound({k: review[k] for k in ('path', 'bytes', 'sha256')})))
        # Optional public-safe projections are separately bound, never mistaken for originals.
        for projection in envelope.get('review_projections', []):
            original = self.bound(projection['original'])
            public = published[projection['public_path']]
            self.check('explicit review projection identity: ' + projection['public_path'],
                       identity(original) == {k: projection['original'][k] for k in ('bytes', 'sha256')}
                       and identity(public) == projection['public_identity'])
        return manifest

    def verify_artifact(self, envelope):
        archive = self.bound(envelope['hosted_artifact_zip'])
        directory = self.path(envelope['hosted_artifact_directory'])
        prefix = envelope.get('hosted_member_prefix', '')
        if prefix:
            member_path(prefix.rstrip('/'))
            self.check('explicit ZIP member prefix', prefix.endswith('/'))
        self.check('bounded hosted archive', len(archive) <= 128 * 1024 * 1024)
        members = {}
        with zipfile.ZipFile(io.BytesIO(archive)) as z:
            infos = z.infolist()
            self.check('bounded unique hosted ZIP records', len(infos) <= 512
                       and len({i.filename for i in infos}) == len(infos))
            self.check('bounded decompressed hosted bytes', sum(i.file_size for i in infos) <= 128 * 1024 * 1024)
            for info in infos:
                self.check('hosted ZIP member prefix', info.filename.startswith(prefix))
                rel = info.filename[len(prefix):]
                if not rel and info.is_dir():
                    continue
                member_path(rel.rstrip('/') if info.is_dir() else rel)
                mode = info.external_attr >> 16
                self.check('hosted ZIP regular file or directory: ' + rel,
                           not stat.S_ISLNK(mode) and not (info.flag_bits & 1)
                           and (stat.S_IFMT(mode) in (0, stat.S_IFREG, stat.S_IFDIR)))
                if info.is_dir():
                    continue
                self.check('bounded hosted member: ' + rel, info.file_size <= 32 * 1024 * 1024)
                raw = z.read(info)
                actual = self.read(directory / member_path(rel))
                self.check('downloaded ZIP/extracted bytes: ' + rel, raw == actual)
                members[rel] = raw
        self.check('exact extracted hosted file set', set(members) == {
            str(p.relative_to(directory)) for p in directory.rglob('*') if p.is_file()})
        return archive, members

    def verify_ci(self, envelope, gh, archive, report):
        ci = json_bytes(self.bound(envelope['hosted_ci']))
        context = report['context']
        self.check('scoped hosted final success', report['status'] == 'PASS_HOSTED_C299_EXACT_TARGETS'
                   and report['scientific_effect'] == 'NONE' and context['human_review_credit'] == 0
                   and context['executor'] == 'GitHub-hosted runner executing C299 verification code'
                   and report.get('negative_predicates_qualified') is True
                   and report.get('negative_classification_errors') == [])
        self.check('native hosted run identity', ci['repository'] == gh['repository'] == context['github_repository']
                   and ci['head'] == gh['head'] == context['pull_request']['head_sha']
                   and ci['tested_commit'] == context['tested_commit'] == context['github_sha']
                   and str(ci['run_id']) == str(context['github_run_id'])
                   and str(ci['run_attempt']) == str(context['github_run_attempt'])
                   and context['pull_request']['number'] == envelope['expected']['pr']
                   and context['github_event_name'] == 'pull_request'
                   and all(str(ci[k]) == str(envelope['expected'][k])
                           for k in ('run_id', 'run_attempt', 'tested_commit')))
        merge = json_bytes(self.bound(envelope['tested_merge_commit']))
        self.check('native tested merge commit/tree/parents', merge['sha'] == ci['tested_commit']
                   and merge['tree']['sha'] == context['tested_tree'] == envelope['expected']['tested_tree']
                   and len(merge['parents']) == 2
                   and {p['sha'] for p in merge['parents']} == {gh['base'], gh['head']}
                   and context['pull_request']['base_sha'] == gh['base'])
        self.check('honest shallow checkout parent observation', context['tested_parents'] == []
                   or set(context['tested_parents']) == {gh['base'], gh['head']})
        run, job, artifact = ci['run'], ci['job'], ci['artifact']
        self.check('native successful workflow metadata', str(run['id']) == str(ci['run_id'])
                   and str(run['run_attempt']) == str(ci['run_attempt']) and run['head_sha'] == gh['head']
                   and run['status'] == 'completed' and run['conclusion'] == 'success'
                   and run['path'] == WORKFLOW)
        self.check('native successful scoped job', str(job['run_id']) == str(ci['run_id'])
                   and job['name'] == 'c299-hosted-formal' and job['status'] == 'completed'
                   and job['conclusion'] == 'success' and context['github_job'] == 'c299-hosted-formal')
        self.check('artifact belongs to exact run and attempt', artifact['name'] ==
                   f"c299-hosted-{ci['run_id']}-{ci['run_attempt']}"
                   and artifact['expired'] is False and str(artifact['workflow_run']['id']) == str(ci['run_id'])
                   and artifact['workflow_run']['head_sha'] == gh['head'])
        download = ci['download']
        self.check('actual artifact download identity', str(download['artifact_id']) == str(artifact['id'])
                   and {'bytes': download['bytes'], 'sha256': download['sha256']} == identity(archive)
                   and artifact['size_in_bytes'] == len(archive))
        if artifact.get('digest'):
            self.check('native artifact SHA-256 digest', artifact['digest'] == 'sha256:' + sha(archive))
        applicable = ci['applicable_jobs']
        self.check('applicable hosted checks all succeeded', isinstance(applicable, list) and len(applicable) >= 3
                   and len({j['id'] for j in applicable}) == len(applicable)
                   and all(j['head_sha'] == gh['head'] and j['status'] == 'completed'
                           and j['conclusion'] == 'success' and j.get('run_id') and j.get('run_attempt')
                           for j in applicable)
                   and {'downstream-replay', 'formal / formal-evidence', 'math-downstream-gates'}
                       <= {j['name'] for j in applicable}
                   and set(envelope['expected']['required_ci_names']) <= {j['name'] for j in applicable})
        steps = job['steps']
        self.check('actual scoped job steps completed successfully', isinstance(steps, list) and bool(steps)
                   and len({step['number'] for step in steps}) == len(steps)
                   and all(step['status'] == 'completed' and step['conclusion'] == 'success' for step in steps))
        log = self.bound(ci['job_log'])
        self.check('scoped complete job log contains actual checkout', ci['tested_commit'].encode() in log)
        for spec in ci.get('additional_native_evidence', []):
            self.bound(spec)
        return ci

    def verify_hosted_execution(self, envelope, members, manifest, published, tree_rows):
        report = json_bytes(members['RESULT.json'])
        source = report['source_identity']
        self.check('hosted exact source identity before/after', source == report['source_identity_after']
                   and source['manifest'] == {k: envelope['source_manifest'][k] for k in ('bytes', 'sha256')}
                   and source['files'] == manifest['files'] and source['source_origins'] == manifest['source_origins']
                   and source['dependency_pins'] == PINS
                   and report['packages_before'] == report['packages_after'] == PINS)
        self.check('source snapshot manifest', members['HOSTED_SOURCE_MANIFEST.json'] == self.bound(envelope['source_manifest']))
        for rel in SOURCE_PATHS:
            self.check('hosted/native reviewed source snapshot: ' + rel,
                       members['source-snapshot/' + rel] == published[PREFIX + rel])
        self.check('exact three hosted support inputs', set(source['support_files']) == SUPPORT_PATHS)
        for rel in SUPPORT_PATHS:
            self.check('hosted/native support snapshot: ' + rel,
                       members['source-snapshot/repository/' + rel] == published[rel]
                       and source['support_files'][rel] == identity(published[rel]))
        self.check('hosted exact formal configuration records', set(source['formal_config']) == {
            'formal/lean-toolchain', 'formal/lakefile.toml', 'formal/lake-manifest.json'}
            and all(type(s['bytes']) is int and s['bytes'] > 0 and re.fullmatch('[0-9a-f]{64}', s['sha256'])
                    for s in source['formal_config'].values()))
        configs = json_bytes(self.bound(envelope['formal_config_readback']))
        self.check('complete native formal configuration readback',
                   len(configs) == 3 and {r['path'] for r in configs} == set(source['formal_config']))
        config_bytes = {}
        for row in configs:
            raw = self.read(row['native_file'])
            config_bytes[row['path']] = raw
            self.check('hosted/native/current-tree formal config: ' + row['path'],
                       identity(raw) == source['formal_config'][row['path']]
                       == {'bytes': row['bytes'], 'sha256': row['sha256']}
                       and git_blob(raw) == row['git_blob'] == tree_rows[row['path']]['sha'])
        self.check('actual formal dependency lock and toolchain',
                   config_bytes['formal/lean-toolchain'].decode().strip() == 'leanprover/lean4:v4.34.1'
                   and {row['name']: row['rev'] for row in json_bytes(config_bytes['formal/lake-manifest.json'])['packages']} == PINS
                   and ('rev = "' + PINS['mathlib'] + '"') in config_bytes['formal/lakefile.toml'].decode())
        runtimes = report['runtimes']
        self.check('measured Lean and kernel binary records', set(runtimes) == {'lean', 'leanchecker'}
                   and all(type(v['bytes']) is int and v['bytes'] > 0
                           and re.fullmatch('[0-9a-f]{64}', v['sha256'])
                           and Path(v['path']).is_absolute() and Path(v['path']).name == k
                           for k, v in runtimes.items()))
        phases = report['phase_results']
        phase_names = ['runtime-print-prefix', 'runtime-version'] + ['build-' + m for m in MODULES]
        phase_names += ['kernel-' + m for m in MODULES[1:]] + ['negative-' + m for m in NEGATIVES]
        self.check('exact 13 unique phases in order', [r['name'] for r in phases] == phase_names
                   and len({r['name'] for r in phases}) == 13)
        first_source = PurePosixPath(phases[2]['command'][-1])
        self.check('first fresh build source path', first_source.is_absolute()
                   and str(first_source).endswith('/' + PREFIX + 'project/Lifetime.lean')
                   and '..' not in first_source.parts)
        checkout = first_source.parents[3]
        object_dir = str(checkout / '.lake/c299-hosted-evidence/objects')
        project_dir = str(checkout / PREFIX / 'project')
        negative_dir = str(checkout / PREFIX / 'negative-project')
        known, audit, generated = {}, None, set()
        lean, kernel = runtimes['lean']['path'], runtimes['leanchecker']['path']
        for record in phases:
            name = record['name']
            environment_binding(report, record, object_dir)
            self.check(name + ': exact selected execution environment', True)
            self.check(name + ': aggregate/per-phase receipt equality',
                       json_bytes(members[name + '.receipt.json']) == record)
            self.check(name + ': completed expected process', record['status'] == 'PASS'
                       and record['timed_out'] is False and record['spawn_error'] is None
                       and record['object_validation_error'] is None
                       and type(record['duration_seconds']) in (int, float)
                       and record['duration_seconds'] >= 0)
            streams = {}
            for stream in ('stdout', 'stderr'):
                raw = members[name + '.' + stream]
                self.check(name + ': exact ' + stream, identity(raw) == {
                    'bytes': record[stream + '_bytes'], 'sha256': record[stream + '_sha256']})
                streams[stream] = raw
            args = record['command']
            if name.startswith('runtime-'):
                self.check(name + ': bounded runtime probe', record['exit_code'] == 0
                           and record['timeout_seconds'] == 30 and record['objects_before'] is None
                           and record['objects_after'] is None and record['cwd'] == str(checkout / 'formal'))
                if name == 'runtime-version':
                    self.check(name + ': actual pinned version', args == [lean, '--version']
                               and 'version 4.34.1' in streams['stdout'].decode()
                               and streams['stderr'] == b'')
                else:
                    self.check(name + ': measured launcher prefix', args == [report['lean_launcher']['path'], '--print-prefix']
                               and streams['stderr'] == b'')
                    runtime_binding(report, streams['stdout'])
                    self.check(name + ': runtime paths and launcher record bound to prefix', True)
                continue
            self.check(name + ': exact imported objects and resource cap', record['objects_before'] == known
                       and record['timeout_seconds'] == 900)
            if name.startswith('build-'):
                module = name[6:]
                want_start = [lean, '-j2', '-M14000'] + ([] if module == 'Lifetime' else ['-DwarningAsError=true'])
                self.check(name + ': exact build command', args[:len(want_start)] == want_start
                           and len(args) == len(want_start) + 3 and args[len(want_start)] == '-o'
                           and args[-1].endswith('/' + PREFIX + 'project/' + module + '.lean')
                           and args[-2] == object_dir + '/' + module + '.olean'
                           and args[-1] == project_dir + '/' + module + '.lean'
                           and record['cwd'] == project_dir and record['exit_code'] == 0)
                after = record['objects_after']
                self.check(name + ': unchanged imported objects', all(after.get(k) == v for k, v in known.items()))
                added = set(after) - set(known)
                allowed = {module + s for s in ('.olean', '.olean.private', '.olean.server', '.ilean', '.ir')}
                self.check(name + ': only own newly built outputs', module + '.olean' in added
                           and added <= allowed and not generated & added)
                generated |= added
                known = after
                self.check(name + ': produced object identity', record['object'] == known[module + '.olean'])
                if module == 'CriticalRidgeAxiomAudit':
                    audit = measured_audit((streams['stdout'] + b'\n' + streams['stderr']).decode())
                else:
                    self.check(name + ': clean non-audit build streams', not streams['stdout'] and not streams['stderr'])
            elif name.startswith('kernel-'):
                self.check(name + ': standard named-module kernel', args == [kernel, '-v', name[7:]]
                           and record['exit_code'] == 0 and record['objects_after'] == known
                           and record['cwd'] == project_dir)
            else:
                fixture = name[9:]
                self.check(name + ': actual negative command', args[:3] == [lean, '-j2', '-M14000']
                           and len(args) == 4 and args[-1].endswith('/' + PREFIX + 'negative-project/' + fixture + '.lean')
                           and record['objects_after'] == known
                           and args[-1] == negative_dir + '/' + fixture + '.lean' and record['cwd'] == negative_dir
                           and record.get('intended_missing_premise_rejection') is True
                           and record.get('diagnostic_qualification_pending') is False
                           and record.get('candidate_parser_match') is True
                           and record.get('negative_classification_error') is None)
                qualified_negative(fixture, record['exit_code'], streams['stdout'], streams['stderr'],
                                   envelope['expected']['negative_qualification']['diagnostics'][fixture])
                self.check(name + ': independently checked intended rejection', True)
        self.check('complete independently measured module-origin census', audit is not None
                   and report['audit']['module_counts'] == audit['module_counts']
                   and report['audit']['declaration_count'] == audit['declaration_count']
                   and report['audit']['module_declarations'] == audit['module_declarations']
                   and set(report['audit']['required_targets']) == REQUIRED
                   and set(report['audit']['allowed_axioms']) == AXIOMS
                   and audit['module_counts'] == envelope['expected']['module_counts'])
        self.check('stable final hosted object inventory', report['objects_after_builds'] == report['objects'] == known
                   and {m + '.olean' for m in MODULES} <= set(known)
                   and {n[8:] for n in members if n.startswith('objects/')} == set(known))
        for name, spec in known.items():
            self.check('downloaded exact object: ' + name, identity(members['objects/' + name]) == spec)
        expected_members = {'RESULT.json', 'HOSTED_SOURCE_MANIFEST.json'}
        expected_members |= {'source-snapshot/' + r for r in SOURCE_PATHS}
        expected_members |= {'source-snapshot/repository/' + r for r in SUPPORT_PATHS}
        expected_members |= {'objects/' + n for n in known}
        expected_members |= {n + ext for n in phase_names for ext in ('.stdout', '.stderr', '.receipt.json')}
        self.check('complete exact hosted evidence member set', set(members) == expected_members)
        return report, audit

    def verify_custody(self, envelope):
        custody = envelope['custody']
        external = {self.root / name for name in
                    ('FINAL_MASTER_INPUTS.json', 'FINAL_MASTER_START.json', 'FINAL_MASTER.json',
                     'FINAL_MASTER.stdout', 'FINAL_MASTER.stderr')}
        external |= {self.path(custody[k]['path']) for k in
                     ('archive', 'remote_archive', 'receipt', 'canonical_verification')}
        required = set(self.observed) - external
        bindings = custody['bindings']
        self.check('explicit native-to-packet evidence bindings', isinstance(bindings, list) and bool(bindings))
        mapped_sources, mapped_payloads = set(), {}
        for row in bindings:
            self.check('packet binding fields', set(row) == {'source_path', 'packet_path'})
            source = self.path(row['source_path'])
            payload = str(member_path(row['packet_path']))
            self.check('unique acyclic packet binding: ' + payload,
                       source not in mapped_sources and payload not in mapped_payloads
                       and source not in external and not source.is_relative_to(self.root / 'PACKET'))
            native = self.read(source)
            packet = self.read(Path('PACKET') / member_path(payload))
            self.check('validated native evidence/packet bytes: ' + payload, native == packet)
            mapped_sources.add(source)
            mapped_payloads[payload] = native
        self.check('packet contains every actual accepted input', required <= mapped_sources)
        archive = self.bound(custody['archive'])
        remote = self.bound(custody['remote_archive'])
        receipt = json_bytes(self.bound(custody['receipt']))
        canonical = json_bytes(self.bound(custody['canonical_verification']))
        self.check('root-owned exact private archive custody', archive == remote
                   and receipt['owner_only'] is True and receipt['actual_raw_download_equal'] is True
                   and receipt['bytes'] == len(archive) and receipt['sha256'] == sha(archive))
        self.check('root-performed canonical archive verification', canonical['ok'] is True
                   and canonical['archive_bytes'] == len(archive) and canonical['archive_sha256'] == sha(archive)
                   and canonical['scientific_effect'] == 'NONE' and canonical['files'] > 0)
        # The root already executed the canonical verifier. Independently bind every
        # payload member to the native PACKET without invoking or reimplementing it.
        with zipfile.ZipFile(io.BytesIO(archive)) as z:
            manifest_raw = z.read('DELIVERY_MANIFEST.json')
            self.check('actual canonical manifest digest',
                       canonical['manifest_sha256'] == sha(manifest_raw))
            document = json_bytes(manifest_raw)
            files = document['files']
            names = {r['filename'] for r in files}
            excluded_names = {p.name for p in external}
            self.check('archive excludes current cyclic control/output files',
                       all(Path(name).name not in excluded_names for name in names))
            self.check('canonical count and required accepted payload bindings',
                       canonical['files'] == len(files) and set(mapped_payloads) <= names)
            for name, native in mapped_payloads.items():
                self.check('validated source/packet/archive triple equality: ' + name, z.read(name) == native)
            self.check('unique canonical archive payload members', len({r['filename'] for r in files}) == len(files)
                       and len(z.namelist()) == len(set(z.namelist()))
                       and set(z.namelist()) == {r['filename'] for r in files} | {'DELIVERY_MANIFEST.json'})
            for row in files:
                rel = member_path(row['filename'])
                raw = z.read(row['filename'])
                self.check('canonical archive/native payload bytes: ' + str(rel),
                           raw == self.read(Path('PACKET') / rel)
                           and identity(raw) == {'bytes': row['size'], 'sha256': row['sha256']})
            packet = self.root / 'PACKET'
            self.check('complete canonical/native payload file set', {r['filename'] for r in files} == {
                str(p.relative_to(packet)) for p in packet.rglob('*') if p.is_file()})
        return {'archive': identity(archive), 'canonical_verifier_executed_by_this_master': False}

    def verify(self, envelope):
        self.check('master input envelope schema', envelope['schema_version'] == 1)
        validate_expectations(envelope['expected'])
        self.check('qualified final expectations admitted', True)
        self.bound(envelope['master_contract'])
        self.bound(envelope['master_notes'])
        self.check('executed master equals reviewed bound source',
                   self.bound(envelope['master_source']) == Path(__file__).read_bytes())
        gh, published, tree_rows = self.verify_publication(envelope)
        manifest = self.verify_sources_reviews(envelope, published)
        archive, members = self.verify_artifact(envelope)
        report, audit = self.verify_hosted_execution(envelope, members, manifest, published, tree_rows)
        ci = self.verify_ci(envelope, gh, archive, report)
        history = envelope['historical_hosted_attempts']
        self.check('development history retained', isinstance(history, list) and bool(history))
        seen = set()
        for prior in history:
            prior_raw = self.bound(prior['archive'])
            native_report = self.bound(prior['report'])
            self.check('bounded historical hosted ZIP', len(prior_raw) <= 128 * 1024 * 1024)
            with zipfile.ZipFile(io.BytesIO(prior_raw)) as zipped:
                infos = [info for info in zipped.infolist() if info.filename == 'RESULT.json']
                self.check('unique bounded historical result member', len(infos) == 1 and infos[0].file_size <= 4 * 1024 * 1024)
                self.check('exact retained historical report', zipped.read(infos[0]) == native_report)
            failed = json_bytes(native_report)
            old_context = failed['context']
            key = (str(old_context['github_run_id']), str(old_context['github_run_attempt']))
            self.check('distinct declared incomplete hosted history', key not in seen
                       and key != (str(ci['run_id']), str(ci['run_attempt']))
                       and key == (str(prior['run_id']), str(prior['run_attempt']))
                       and failed['status'] == prior['status'] == 'HOLD_NOT_COMPLETED'
                       and 'completed_at' not in failed and old_context['pull_request']['head_sha'] == prior['head']
                       and old_context['github_repository'] == REPOSITORY)
            seen.add(key)
        self.check('retained additional failure/source evidence', isinstance(envelope['retained_inputs'], list)
                   and bool(envelope['retained_inputs']))
        for spec in envelope['retained_inputs']:
            self.bound(spec)
        custody = self.verify_custody(envelope)
        for path, spec in list(self.observed.items()):
            self.check('final stable native input: ' + str(path), path.is_file()
                       and all(not q.is_symlink() for q in (path, *path.parents)) and identity(path.read_bytes()) == spec)
        return {'census': audit, 'hosted_run_id': ci['run_id'], 'hosted_run_attempt': ci['run_attempt'],
                'hosted_tested_commit': ci['tested_commit'], 'custody': custody,
                'verification_limit': 'Artifact and execution-record binding; runtime hashes are executor-measured records, not independently downloaded/native binary reproduction. No Lean execution, remote fetch, human review, or scientific promotion.'}



def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    args = parser.parse_args()
    root = args.root.absolute()
    start, output = root / 'FINAL_MASTER_START.json', root / 'FINAL_MASTER.json'
    if start.exists() or output.exists():
        print('REFUSED: final master already started; preserve prior evidence', file=sys.stderr)
        return 1
    # Fixed external names prevent user-controlled output/custody cycles.
    envelope_raw = (root / 'FINAL_MASTER_INPUTS.json').read_bytes()
    master_raw = Path(__file__).read_bytes()
    with start.open('x') as handle:
        json.dump({'started_at': now(), 'master_sha256': sha(master_raw),
                   'input_envelope_sha256': sha(envelope_raw), 'scientific_effect': 'NONE'}, handle, indent=2)
        handle.write('\n')
    checker = Master(root)
    result = {'status': 'HOLD_ARTIFACT_VERIFICATION', 'scientific_effect': 'NONE'}
    try:
        checker.check('exact master invocation bytes', checker.read(Path(__file__)) == master_raw)
        checker.check('exact master input envelope bytes', checker.read('FINAL_MASTER_INPUTS.json') == envelope_raw)
        result.update(checker.verify(json_bytes(envelope_raw)))
        result['status'] = 'PASS_ARTIFACT_VERIFICATION_NOT_THEOREM_PROOF'
    except BaseException as exc:
        result['error'] = repr(exc)
    result.update(finished_at=now(), checks=checker.checks, check_count=len(checker.checks),
                  observed_identities={str(path): spec for path, spec in checker.observed.items()})
    with output.open('x') as handle:
        json.dump(result, handle, indent=2, sort_keys=True)
        handle.write('\n')
    print(json.dumps({'status': result['status'], 'checks': result['check_count']}))
    return 0 if result['status'].startswith('PASS_') else 1


if __name__ == '__main__':
    raise SystemExit(main())
