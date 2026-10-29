#!/usr/bin/env python3
"""UNEXECUTED root-only66 publication preparation. Import performs no action."""
import argparse
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import sys

# Reuse this already-qualified process utility unchanged; its legacy location is historical.
sys.path.insert(0, '/workspace/scratch/actual-source-saddle-uppercuts-publication/native-runtime')
from capture import CaptureRun, put_new, require

REPO = Path('/workspace/Math-curvature-20261026')
PUB = Path('/workspace/scratch/actual-source-regular-local-collar-publication')
PACK = Path('/workspace/scratch/actual-source-regular-local-collar-packaging')
REL = 'frontiers/source_derivative_gaussian_20261025/'
MODULE = 'SourceActualRegularLocalCollar'
SOURCE = REL + MODULE + '.lean'
BASE = '263b9d4329043e6debd299a8c27327ee515670d7'
BASE_TREE = '9f53f31af3dfed688a3d683589fa8a3ed0e621fc'
BRANCH = 'refs/heads/codex/cubic-curvature-20261026'
TRANSPORT_STATUS = 'LOCAL_METADATA_TREE_READY_NATIVE_UPLOAD_PENDING'
EXTRA67 = {'SOURCE_ACTUAL_LOWER_SEPARATION' + x for x in ['.md', '_PLAN.md', '_CONTROLS.md', '_CONTENDERS.json']}


def read(path): return json.loads(Path(path).read_text())


def sha(value, length=40):
    require(isinstance(value, str) and re.fullmatch('[0-9a-f]{%d}' % length, value), 'Actual existing identity required')
    return value


def safe(value):
    p = PurePosixPath(value)
    require(not p.is_absolute() and str(p) == value and '..' not in p.parts and value.startswith(REL), 'Owned explicit relative path')
    require(not any(x in p.parts for x in ['.git', '.lake', 'build', '__pycache__']), 'No cache/build/index path')
    require(not value.endswith(('.olean', '.ilean', '.o', '.so', '.pyc', '.bin')), 'No actual binary/object path')
    return value


def known_file(path, row):
    require(stat.S_ISREG(Path(path).lstat().st_mode), 'Non-symlink regular file required')
    require(Path(path).stat().st_size == row['bytes'], 'Known exact new transfer size')
    sha(row['sha256'], 64)  # Format association only: no content digest calculation.


def source_go(path):
    value = read(path)
    require(value['status'] == 'ROOT_GO66_SOURCE_CUT_AFTER_FINAL_QUALIFICATION', 'Actual final root sourcecut GO')
    require(value['qualified_baseline'] == BASE, 'Qualified65 baseline')
    require(all(value[k] for k in ['all_math_complete', 'final_review_pass', 'source_frozen']), 'No partial source cut')
    return value


def tree_plan(run, parent, base_tree, paths, phase, index=None, previous=None, base_bindings=None):
    paths = [safe(x) for x in paths]
    require(len(paths) == len(set(paths)), 'Unique explicit stage paths')
    index = Path(index) if index else run.path / 'isolated.index'
    env = {'GIT_INDEX_FILE': str(index)}
    if previous is None:
        require(not index.exists(), 'Fresh isolated index only')
        run.command('isolated-index-from-actual-parent', ['git', 'read-tree', parent], REPO, env_overrides=env)
    # The sole previous-plan caller checks the actual isolated-tree lease BEFORE copying its tail.
    pathspec = run.path / 'EXPLICIT_STAGE_PATHS.nul.txt'
    pathspec.write_bytes(b''.join(x.encode() + b'\0' for x in paths))
    run.command('stage-ONLY-explicit-owned-paths', ['git', '--literal-pathspecs', 'add',
                '--pathspec-from-file=' + str(pathspec), '--pathspec-file-nul'], REPO, env_overrides=env)
    tree = run.command('write-actual-new-tree', ['git', 'write-tree'], REPO, env_overrides=env).decode().strip()
    comparison = previous['tree_sha'] if previous else parent
    raw = run.command('actual-changed-paths', ['git', 'diff', '--cached', '--name-only', '-z', comparison, '--'], REPO, env_overrides=env)
    changed = {x.decode() for x in raw.split(b'\0') if x}
    require(changed <= set(paths), 'No changes outside explicit new rows')
    if previous: require(changed == set(paths), 'Only and all fresh publication-tail additions')
    all_changed = changed | ({x['path'] for x in previous['tree_entries']} if previous else set())
    stage = run.command('actual-isolated-index-bindings', ['git', 'ls-files', '--stage', '-z'], REPO, env_overrides=env)
    entries = []
    for item in stage.split(b'\0'):
        if not item: continue
        header, path = item.split(b'\t', 1)
        mode, blob, number = header.decode().split()
        if path.decode() in all_changed:
            require(mode == '100644' and number == '0', 'Only resolved regular text bindings')
            entries.append({'path': path.decode(), 'mode': mode, 'type': 'blob', 'sha': sha(blob)})
    require({x['path'] for x in entries} == all_changed, 'Every changed path bound')
    if base_bindings:
        captured = Path(base_bindings).read_bytes()  # Reuse the actual first captured sourcecut tree IDs.
        binding_path = str(Path(base_bindings).resolve())
    else:
        captured = run.command('remote-known-actual-parent-tree-bindings', ['git', 'ls-tree', '-r', '-z', parent], REPO)
        binding_path = str(run.path / ('%02d-remote-known-actual-parent-tree-bindings' % run.counter) / 'stdout.log')
    known = set()
    for item in captured.split(b'\0'):
        if item:
            header, unused_path = item.split(b'\t', 1)
            unused_mode, kind, blob = header.decode().split()
            if kind == 'blob': known.add(blob)
    new = {}
    previous_blobs = {x['sha']: x for x in previous['new_unique_blobs']} if previous else {}
    for entry in entries:
        if entry['sha'] not in known:
            byte_count = previous_blobs[entry['sha']]['bytes'] if entry['sha'] in previous_blobs else (REPO / entry['path']).stat().st_size
            new.setdefault(entry['sha'], {'sha': entry['sha'], 'representative_path': entry['path'],
                'bytes': byte_count, 'paths': []})['paths'].append(entry['path'])
    value = {'status': TRANSPORT_STATUS, 'stage66_phase': phase, 'sourcecut': parent,
        'base_tree_sha': base_tree, 'tree_sha': tree, 'tree_entries': sorted(entries, key=lambda x: x['path']),
        'new_unique_blobs': [new[x] for x in sorted(new)], 'explicit_stage_paths': paths if not previous else previous['explicit_stage_paths'] + paths,
        'binding_SKIP_paths': [] if not previous else previous['binding_SKIP_paths'],
        'base_tree_binding_stdout': binding_path, 'isolated_index': str(index),
        'main_index_untouched': True, 'all_object_actions': 'SKIP', 'native_writes_performed': False,
        'old_SHA256_hashes': 0}
    return value


def copy_rows(run, rows, overlay=None, fresh=False):
    for row in rows:
        dst = REPO / safe(row['path'])
        src = Path(row['source']) if overlay is None else Path(overlay) / row['path']
        known_file(src, row)
        require(dst.parent.resolve().is_relative_to(REPO.resolve()), 'Destination stays within repository')
        if fresh: require(not dst.exists(), 'Fresh tail paths only')
        elif dst.exists(): require(stat.S_ISREG(dst.lstat().st_mode), 'Existing destination regular text')
    for row in rows:
        dst = REPO / row['path']
        src = Path(row['source']) if overlay is None else Path(overlay) / row['path']
        if dst.exists():
            old = run.path / 'previous-shared-bytes' / row['path']
            old.parent.mkdir(parents=True, exist_ok=True); old.write_bytes(dst.read_bytes())
        payload = src.read_bytes(); require(len(payload) == row['bytes'], 'Exact transfer size')
        dst.parent.mkdir(parents=True, exist_ok=True)
        temporary = dst.with_name(dst.name + '.root66-new-transfer')
        with temporary.open('xb') as stream:
            stream.write(payload); stream.flush(); os.fsync(stream.fileno())
        os.replace(temporary, dst)
        run.event({'event': 'explicit_text_row_copied', 'path': row['path'], 'bytes': row['bytes'], 'known_sha256_reused': row['sha256']})


def prepare_source(args, run):
    go = source_go(args.input)
    known_file(REPO / SOURCE, go['source_identity'])
    require(run.command('actual-HEAD-before-source', ['git', 'rev-parse', 'HEAD'], REPO).decode().strip() == BASE, 'Qualified65 local lease')
    value = tree_plan(run, BASE, BASE_TREE, [SOURCE], 'source_cut')
    require([x['path'] for x in value['tree_entries']] == [SOURCE], 'Exactly one new66 source')
    value['source_identity_reused'] = go['source_identity']
    return value


def prepare_metadata(args, run):
    plan = read(PACK / 'APPLY_PLAN.json'); result = read(PACK / 'ASSEMBLY_RESULT.json')
    cut = read(args.input); parent = sha(cut['source_cut'])
    require(cut['status'] == 'EXACT_NATIVE66_COMMIT_IMPORTED_LOCAL_ONLY' and cut['phase'] == 'source_cut'
            and cut['parent_sha'] == BASE, 'Actual genuine root66 sourcecut record')
    require(plan['status'] == 'ROOT_ONLY_EXACT66_APPLY_AFTER_METADATA_PASS', 'Final66 apply status')
    require(result['status'] == 'NEW66_METADATA_ASSEMBLY_AND_BOUNDED_ASSOCIATIONS_PASS', 'Metadata PASS')
    require(parent == plan['expected_HEAD'] == result['source_cut'] and plan['qualified_baseline'] == BASE, 'Actual final66 sourcecut binding')
    require(Path(plan['overlay_root']) == PACK / 'overlay' and Path(plan['destination_root']) == REPO, 'Exact roots')
    require(len(plan['skip']) == 5 and not plan['cache_object_actions'], 'Five bindings SKIP; all objects SKIP')
    journal = [json.loads(x) for x in (PACK / 'VALIDATION_PROGRESS.jsonl').read_text().splitlines()]
    require(len({x['name'] for x in journal if x['event'] == 'check_passed'}) == 7, 'Seven completed metadata associations reused')
    paths = [safe(x['path']) for x in plan['apply']]; skips = [safe(x['path']) for x in plan['skip']]
    require(len(paths) == len(set(paths)) and len(skips) == len(set(skips)), 'Unique apply and SKIP rows before mutation')
    require(not set(paths) & set(skips), 'Binding SKIPs disjoint')
    docs = read('/workspace/scratch/actual-source-lower-separation-publication/PRECODE67_IDENTITIES.json')['documents']
    extras = [safe(str(Path(x['path']).relative_to(REPO))) for x in docs]
    require(len(extras) == 4 and {Path(x).name for x in extras} == EXTRA67, 'Only four proper67 identity rows')
    require(not set(extras) & (set(paths) | set(skips)), 'Future67 extras excluded66 qualification')
    for row in docs: known_file(row['path'], row)  # Metadata/stat binding only; no future document content inspection.
    require(run.command('actual-HEAD-before-metadata', ['git', 'rev-parse', 'HEAD'], REPO).decode().strip() == parent, 'Actual sourcecut lease')
    copy_rows(run, plan['apply'], overlay=PACK / 'overlay')
    value = tree_plan(run, parent, sha(cut['tree_sha']), paths + extras, 'metadata')
    value['binding_SKIP_paths'] = skips; value['apply_plan_identity_reused'] = result['apply_plan_identity']
    value['extra67_documents_excluded66_qualification'] = docs
    return value


def prepare_tail(args, run):
    frozen = read(args.input); previous = read(args.plan)
    require(frozen['status'] == 'ROOT_FROZEN66_PUBLICATION_TAIL_FILES', 'Actual root-frozen explicit final tail')
    require(previous['status'] == TRANSPORT_STATUS and previous['stage66_phase'] == 'metadata', 'Actual first66 metadata tree')
    rows = frozen['files']; prefix = REL + 'actual-source-regular-local-collar-publication-tail/'
    require(all(x['path'].startswith(prefix) for x in rows), 'Only final66 publication evidence extras')
    require(len({x['path'] for x in rows}) == len(rows), 'Unique frozen tail rows before mutation')
    require(not {x['path'] for x in rows} & set(previous['explicit_stage_paths']), 'No reapply or restage of prior metadata/docs')
    for scope in ['entry', 'outer']:
        receipt = read(PACK / (scope + '-captures') / 'metadata-attempt-001' / 'RECEIPT.json')
        require(receipt['status'] == 'PASS_ACTUAL_CHILD_EXIT_ZERO' and receipt['child_exit_code'] == 0
                and receipt['spawn_or_wrapper_exception'] is None, 'Actual closed66 wrapper required')
    index = Path(previous['isolated_index'])
    require(index.is_file() and not index.is_symlink(), 'Same actual first isolated index')
    current = run.command('actual-isolated-tree-lease-before-any-tail-copy', ['git', 'write-tree'], REPO,
                          env_overrides={'GIT_INDEX_FILE': str(index)}).decode().strip()
    require(current == previous['tree_sha'], 'Actual original isolated-tree lease before mutation')
    copy_rows(run, rows, fresh=True)
    value = tree_plan(run, previous['sourcecut'], previous['base_tree_sha'], [x['path'] for x in rows], 'metadata',
        index=previous['isolated_index'], previous=previous, base_bindings=previous['base_tree_binding_stdout'])
    value['original_transport_plan'] = str(Path(args.plan).resolve()); value['original_tree_sha'] = previous['tree_sha']
    value['publication_tail_scope'] = 'Final immutable receipts/handoff/closed captures EXTRA outside sealed66 qualification manifest/archive'
    return value


def import_commit(args, run):
    plan = read(args.plan); commit = sha(args.commit)
    require(plan['status'] == TRANSPORT_STATUS, 'Actual local source or metadata tree plan')
    parent = sha(plan['sourcecut']); rows = plan['tree_entries']; paths = [safe(x['path']) for x in rows]
    require(len(paths) == len(set(paths)) and set(paths) <= set(plan['explicit_stage_paths']), 'Only unique explicitly authorized index entries')
    require(not set(paths) & set(plan['binding_SKIP_paths']), 'Five metadata bindings remain SKIP')
    require(all(x['mode'] == '100644' and x['type'] == 'blob' and sha(x['sha']) for x in rows), 'Regular blob bindings')
    if plan['stage66_phase'] == 'source_cut':
        require(parent == BASE and paths == [SOURCE], 'Only actual66 source-cut import')
        require(not (PUB / 'ROOT_SOURCE_CUT.json').exists(), 'Sourcecut record absent before local CAS')
    require(run.command('local-HEAD-before-import', ['git', 'rev-parse', 'HEAD'], REPO).decode().strip() == parent, 'Actual local parent lease')
    require(run.command('actual-symbolic-branch', ['git', 'symbolic-ref', '--quiet', 'HEAD'], REPO).decode().strip() == BRANCH, 'Owned branch only')
    run.command('exact-public-native-commit-fetch', ['env', 'GIT_TERMINAL_PROMPT=0', 'GIT_CONFIG_NOSYSTEM=1', 'GIT_CONFIG_GLOBAL=/dev/null',
        'git', '-c', 'credential.helper=', '-c', 'http.extraHeader=', '-c', 'http.https://github.com/.extraHeader=', '-c', 'core.askPass=/bin/false',
        'fetch', '--no-write-fetch-head', '--no-tags', '--no-recurse-submodules', '--no-auto-maintenance',
        'https://github.com/d6g8k5htny-coder/Math-.git', commit], REPO)
    raw = run.command('exact-native-commit-bytes', ['git', 'cat-file', 'commit', commit], REPO)
    header = raw.split(b'\n\n', 1)[0].splitlines()
    require([x[5:].decode() for x in header if x.startswith(b'tree ')] == [plan['tree_sha']]
            and [x[7:].decode() for x in header if x.startswith(b'parent ')] == [parent], 'Actual raw tree and sole parent')
    (run.path / 'NATIVE_COMMIT.exact.txt').write_bytes(raw)
    run.command('CAS-only-owned-local-branch', ['git', 'update-ref', BRANCH, commit, parent], REPO)
    payload = b''.join((x['mode'] + ' ' + x['sha'] + '\t' + x['path']).encode() + b'\0' for x in rows)
    binding = run.path / 'ONLY_OWNED_INDEX_BINDINGS.nul.txt'; binding.write_bytes(payload)
    run.command('sync-ONLY-owned-index-bindings', ['git', 'update-index', '-z', '--index-info'], REPO,
                stdin_bytes=payload, stdin_binding=str(binding))
    value = {'status': 'EXACT_NATIVE66_COMMIT_IMPORTED_LOCAL_ONLY', 'commit_sha': commit,
        'source_cut': commit if plan['stage66_phase'] == 'source_cut' else parent, 'tree_sha': plan['tree_sha'],
        'parent_sha': parent, 'phase': plan['stage66_phase'], 'owned_index_rows_synchronized': len(rows),
        'remote_ref_updated': False, 'commit_JSON_reconstruction': False, 'all_object_actions': 'SKIP'}
    if plan['stage66_phase'] == 'source_cut': put_new(PUB / 'ROOT_SOURCE_CUT.json', value)
    return value


def copy_own(args, run):
    go = source_go(args.input); cut = read(PUB / 'ROOT_SOURCE_CUT.json')
    require(cut['phase'] == 'source_cut' and cut['parent_sha'] == BASE, 'Actual genuine66 sourcecut')
    require(not (PUB / 'ROOT_OWN_OBJECT_COPY.json').exists(), 'Sole own copy not previously recorded')
    src = Path(go['eligible_object_path']); dst = REPO / REL / '.lake/build/lib/lean' / (MODULE + '.olean')
    require(src.name == MODULE + '.olean', 'Only eligible new own module')
    known_file(src, go['eligible_object_identity']); require(not dst.exists(), 'Only first new own destination')
    require(run.command('genuine-sourcecut-HEAD', ['git', 'rev-parse', 'HEAD'], REPO).decode().strip() == cut['source_cut'], 'Copy after actual native sourcecut')
    payload = src.read_bytes(); require(len(payload) == go['eligible_object_identity']['bytes'], 'Eligible new copy size')
    dst.parent.mkdir(parents=True, exist_ok=True)
    with dst.open('xb') as stream: stream.write(payload); stream.flush(); os.fsync(stream.fileno())
    require(dst.read_bytes() == payload, 'Immediate new copy byte-transfer equality; no content digest replay')
    value = {'status': 'ELIGIBLE66_OWN_OBJECT_COPIED_ONCE_ALL_FURTHER_SKIP', 'source_cut': cut['source_cut'],
        'source': str(src), 'destination': str(dst), 'known_identity_reused': go['eligible_object_identity'],
        'copies': 1, 'further_copy_actions': [], 'old_helper_ordinary_objects': 'SKIP', 'SHA256_recomputations': 0}
    put_new(PUB / 'ROOT_OWN_OBJECT_COPY.json', value)
    return value


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('mode', choices=['source-tree', 'metadata-tree', 'tail', 'import', 'copy-own'])
    ap.add_argument('--input'); ap.add_argument('--plan'); ap.add_argument('--commit')
    ap.add_argument('--run-dir', required=True); ap.add_argument('--root-approved-execute', action='store_true')
    args = ap.parse_args(); require(args.root_approved_execute, 'Root-only execution; prepared helpers carry no approval')
    run = CaptureRun(args.run_dir, 'root66-' + args.mode)
    fn = {'source-tree': prepare_source, 'metadata-tree': prepare_metadata, 'tail': prepare_tail,
          'import': import_commit, 'copy-own': copy_own}[args.mode]
    value = fn(args, run)
    if args.mode in ['source-tree', 'metadata-tree', 'tail']:
        put_new(run.path / 'NATIVE_TRANSPORT_PLAN.json', value)
        run.finish({'status': value['status'], 'stage66_phase': value['stage66_phase'], 'tree_sha': value['tree_sha'],
            'changed_paths': len(value['tree_entries']), 'new_unique_blobs': len(value['new_unique_blobs']),
            'transport_plan': str(run.path / 'NATIVE_TRANSPORT_PLAN.json'), 'all_object_actions': 'SKIP'})
    else: run.finish(value)


if __name__ == '__main__': main()
