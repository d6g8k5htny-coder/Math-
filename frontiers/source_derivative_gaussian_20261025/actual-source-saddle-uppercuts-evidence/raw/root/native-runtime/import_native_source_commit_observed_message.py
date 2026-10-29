#!/usr/bin/env python3
"""ROOT AMENDMENT: ONE unsigned candidate using literal observed API message bytes.
Only a matching native Git SHA permits root's local CAS/source-index sync.
"""
from pathlib import Path
from datetime import datetime
import argparse
import json
import os
import re
import sys
from capture import CaptureRun, put_new, require
from prepare_source_tree import PARENT, SOURCE_PATH, SOURCE_ID, oid


def identity_header(kind, value):
    require(isinstance(value, dict), 'Missing actual ' + kind + ' metadata.')
    name, email, date = value.get('name'), value.get('email'), value.get('date')
    require(isinstance(name, str) and name and isinstance(email, str) and email,
            'Actual identity name/email are required; no substituted identity.')
    require(not any(c in name + email for c in '\r\n\x00<>'), 'Unsupported identity delimiter; fail closed.')
    require(isinstance(date, str), 'Actual ISO date required.')
    match = re.fullmatch(r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})(?:\.(\d+))?(Z|[+-]\d{2}:\d{2})', date)
    require(match is not None, 'Unsupported actual date; no timezone/date guessing.')
    require(not match.group(2) or set(match.group(2)) <= {'0'}, 'Nonintegral commit timestamp is unsupported.')
    offset = match.group(3)
    stamp = datetime.fromisoformat(match.group(1) + ('+00:00' if offset == 'Z' else offset))
    epoch = int(stamp.timestamp())
    zone = '+0000' if offset == 'Z' else offset.replace(':', '')
    return (kind + ' ' + name + ' <' + email + '> ' + str(epoch) + ' ' + zone).encode('utf-8')


def write_bytes_new(path, data):
    with Path(path).open('xb') as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())


def perform(args, run, state):
    repo = Path(args.repo).resolve()
    tree_record = json.loads(Path(args.tree_record).read_text())
    require(tree_record['status'] == 'PASS_NEW_SOURCE_BLOB_AND_SOURCE_ONLY_TREE', 'A complete actual A record is required.')
    require(tree_record['parent_sha'] == PARENT and tree_record['source_identity'] == SOURCE_ID,
            'Tree record has different qualified source/parent.')
    require(tree_record['source_path'] == SOURCE_PATH, 'Tree record path differs.')
    tree, blob = tree_record['tree_sha'], tree_record['blob_sha']
    require(re.fullmatch('[0-9a-f]{40}', tree) and re.fullmatch('[0-9a-f]{40}', blob), 'Malformed tree/blob IDs.')
    native = args.native_sha
    require(re.fullmatch('[0-9a-f]{40}', native), 'Native create_commit returned SHA required.')
    response_path = Path(args.commit_json).resolve()
    response_bytes = response_path.read_bytes()
    commit = json.loads(response_bytes)
    require(commit.get('sha') == native, 'Actual Git-data commit response SHA differs.')
    require(commit.get('tree', {}).get('sha') == tree, 'Actual native tree differs from A tree.')
    parents = commit.get('parents')
    require(isinstance(parents, list) and len(parents) == 1 and parents[0].get('sha') == PARENT,
            'Actual native commit must have exactly the qualified64 sole parent.')
    verification = commit.get('verification')
    require(isinstance(verification, dict), 'Actual verification metadata required; do not assume unsigned.')
    require(verification.get('signature') is None and verification.get('payload') is None,
            'Unexpected signature/payload: STOP; this script invents no signature/raw signed object.')
    require(verification.get('verified') is False and verification.get('reason') == 'unsigned',
            'New native commit is not explicitly unsigned; STOP for separate exact-byte handling.')
    require(not commit.get('encoding') or commit['encoding'].lower() == 'utf-8', 'Unexpected encoding header.')
    requested_path = Path(args.requested_message).resolve()
    requested = requested_path.read_bytes()
    require(requested.endswith(b'\n') and not requested.endswith(b'\n\n'),
            'Retained actual create_commit request must end in EXACTLY ONE LF.')
    requested_text = requested.decode('utf-8')
    require('\x00' not in requested_text, 'NUL in requested message unsupported.')
    api_message = commit.get('message')
    require(isinstance(api_message, str) and api_message.rstrip('\n') == requested_text.rstrip('\n'),
            'API normalized message does not match exact retained requested message.')
    # Concrete first import failed exact SHA matching with retained request bytes.
    # This revised NEW candidate uses the literal actual Git-data message value,
    # with NO newline addition/removal and no author/timezone alternatives.
    # Exact native SHA equality remains mandatory before ANY local movement.
    raw = b'\n'.join([('tree ' + tree).encode('ascii'), ('parent ' + PARENT).encode('ascii'),
                      identity_header('author', commit.get('author')),
                      identity_header('committer', commit.get('committer'))]) + b'\n\n' + api_message.encode('utf-8')
    write_bytes_new(run.path / 'NATIVE_COMMIT_RESPONSE.exact.json', response_bytes)
    write_bytes_new(run.path / 'REQUESTED_MESSAGE.exact.txt', requested)
    write_bytes_new(run.path / 'CANDIDATE_RAW_COMMIT.bin', raw)
    frozen = Path(args.frozen_source).resolve()
    require(len(frozen.read_bytes()) == SOURCE_ID['bytes'] and (repo / SOURCE_PATH).read_bytes() == frozen.read_bytes(),
            'Worktree source must still equal immutable qualified source bytes.')
    require(oid(run.command('head-before-import', ['git', 'rev-parse', 'HEAD'], repo)) == PARENT,
            'Local HEAD changed; no implicit parent correction.')
    branch_ref = args.branch if args.branch.startswith('refs/heads/') else 'refs/heads/' + args.branch
    actual_ref = run.command('actual-symbolic-branch', ['git', 'symbolic-ref', '-q', 'HEAD'], repo).decode().strip()
    require(actual_ref == branch_ref, 'Actual local branch differs; no detached/other-branch update.')
    run.event({'event': 'ONE_NEW_RAW_COMMIT_CONSTRUCTION_INTENT', 'native_sha': native,
               'raw_candidate': str(run.path / 'CANDIDATE_RAW_COMMIT.bin'),
               'literal_actual_API_message_no_newline_modification': True,
               'prior_failed_request_message_candidate_preserved': '/workspace/scratch/actual-source-saddle-uppercuts-publication/native-source-import001/action/RESULT.json'})
    imported = oid(run.command('ONE-new-commit-object', ['git', 'hash-object', '-w', '-t', 'commit', '--stdin'], repo,
                               stdin_bytes=raw,
                               stdin_binding={'path': str(run.path / 'CANDIDATE_RAW_COMMIT.bin'),
                                              'bytes': len(raw), 'scope': 'ONE NEW Git metadata candidate only; no SHA256'}))
    state['constructed_object_sha'] = imported
    require(imported == native, 'Candidate SHA DOES NOT MATCH native SHA; STOP before ANY local HEAD/index movement. No guess loop.')
    state['matching_native_object_imported'] = True
    run.event({'event': 'EXACT_NATIVE_SHA_MATCH_BEFORE_ANY_LOCAL_MOVEMENT', 'native_sha': native,
               'actual_tree': tree, 'actual_parent': PARENT})
    run.command('CAS-owned-local-branch', ['git', 'update-ref', '-m', 'native source65 cut import',
                                         branch_ref, native, PARENT], repo)
    state['local_ref_cas_completed'] = True
    run.command('sync-ONLY-owned-source-index-entry', ['git', 'update-index', '--add', '--cacheinfo',
                                                      '100644,' + blob + ',' + SOURCE_PATH], repo)
    state['source_index_sync_completed'] = True
    require(oid(run.command('head-after-local-cut', ['git', 'rev-parse', 'HEAD'], repo)) == native,
            'Actual local HEAD after CAS differs.')
    entry = run.command('owned-source-index-entry', ['git', 'ls-files', '--stage', '--', SOURCE_PATH], repo).decode().strip()
    require(entry == '100644 ' + blob + ' 0\t' + SOURCE_PATH, 'Owned source index entry differs after sync.')
    return {'status': 'PASS_NATIVE_SOURCE_COMMIT_IMPORTED_AND_LOCAL_CUT_ESTABLISHED',
            'native_sha': native, 'source_cut': native, 'parent_sha': PARENT,
            'tree_sha': tree, 'blob_sha': blob, 'source_path': SOURCE_PATH,
            'source_identity': SOURCE_ID, 'local_branch_ref': branch_ref, 'local_HEAD': native,
            'remote_ref_write': False,
            'remote_ref_scope': 'No remote operation in this script. Root retains separate actual ee5 remote-head observation; remote ref remains unmoved by these local actions until later final publication.',
            'requested_message': str(requested_path), 'actual_commit_response': str(response_path),
            'author_committer_source': 'Actual returned ISO metadata/offsets; exact native SHA matched.',
            'message_source': 'Literal actual Git-data API message UTF8 bytes, no newline modification; previous request-message candidate failed and is retained.',
            'sha256_computations': 0, **state}


def main():
    parser = argparse.ArgumentParser()
    for name in ['repo', 'tree-record', 'commit-json', 'requested-message', 'native-sha', 'branch', 'frozen-source', 'run-dir']:
        parser.add_argument('--' + name, required=True)
    args = parser.parse_args()
    run = CaptureRun(args.run_dir, 'import-one-native-source65-unsigned-commit')
    state = {'matching_native_object_imported': False, 'local_ref_cas_completed': False,
             'source_index_sync_completed': False, 'remote_ref_write': False}
    try:
        run.finish(perform(args, run, state))
        return 0
    except Exception as exc:
        run.finish({'status': 'FAIL_PRESERVED_NO_ALTERNATE_CANDIDATE_OR_AUTOMATIC_RETRY',
                    'exception': repr(exc), **state,
                    'partial_operation_rule': 'Inspect actual receipts/events; if CAS succeeded but index sync failed, recover ONLY that affected operation. Never repeat new-object construction or move a different parent silently.'})
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
