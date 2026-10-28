#!/usr/bin/env python3
"""PROPOSAL: root constructs ONLY a new source65 blob/tree, never a commit/ref."""
from pathlib import Path
import argparse
import json
import os
import re
import sys
from capture import CaptureRun, put_new, require

PARENT = 'ee5b141d5ff41a0a9040256a8025690ec22d7266'
SOURCE_PATH = 'frontiers/source_derivative_gaussian_20261025/SourceActualSaddleUppercuts.lean'
SOURCE_ID = {'bytes': 36869, 'sha256': 'd292c767e789b98a6fbb56e5c21ec8867979faa832a97c1e79c79c899b777129'}


def oid(raw):
    value = raw.decode('ascii').strip()
    require(re.fullmatch('[0-9a-f]{40}', value), 'Expected a literal Git SHA1 object ID.')
    return value


def perform(args, run):
    repo = Path(args.repo).resolve()
    frozen = Path(args.frozen_source).resolve()
    require(args.expected_parent == PARENT, 'Parent change requires a separately reviewed root binding.')
    source = frozen.read_bytes()
    require(len(source) == SOURCE_ID['bytes'], 'Frozen source size differs from qualified source65.')
    require((repo / SOURCE_PATH).read_bytes() == source, 'Owned worktree source differs from frozen qualified bytes.')
    head = oid(run.command('head-before', ['git', 'rev-parse', 'HEAD'], repo))
    require(head == PARENT, 'Local HEAD is not the expected qualified64 parent; no implicit reconciliation.')
    parent_tree = oid(run.command('parent-tree', ['git', 'rev-parse', PARENT + '^{tree}'], repo))
    index_text = run.command('main-index-location', ['git', 'rev-parse', '--git-path', 'index'], repo).decode().strip()
    index_path = Path(index_text)
    if not index_path.is_absolute():
        index_path = repo / index_path
    main_index_before = index_path.read_bytes() if index_path.exists() else None
    if args.known_blob_record:
        known = json.loads(Path(args.known_blob_record).read_text())
        require(known['source_identity'] == SOURCE_ID and known['source_path'] == SOURCE_PATH,
                'Known new-blob record does not bind this exact qualified source.')
        blob = known['blob_sha']
        require(re.fullmatch('[0-9a-f]{40}', blob), 'Known blob SHA is malformed.')
        blob_type = run.command('known-new-blob-type', ['git', 'cat-file', '-t', blob], repo).decode().strip()
        require(blob_type == 'blob', 'Known new source object is not an available blob.')
        blob_origin = 'Existing recorded NEW source65 Git blob reused; no blob hash repeated.'
    else:
        blob = oid(run.command('new-source-blob', ['git', 'hash-object', '-w', '--stdin'], repo,
                               stdin_bytes=source,
                               stdin_binding={'path': str(frozen), **SOURCE_ID,
                                              'sha256_effect': 'REUSED, not calculated here'}))
        blob_origin = 'ONE NEW Git blob construction from exact retained source bytes; no SHA256 recomputation.'
    blob_record = {'status': 'NEW_SOURCE65_BLOB_BOUND', 'blob_sha': blob,
                   'source_path': SOURCE_PATH, 'source_identity': SOURCE_ID,
                   'frozen_source': str(frozen), 'origin': blob_origin}
    put_new(run.path / 'NEW_BLOB_ID.json', blob_record)
    isolated = run.path / 'isolated.index'
    require(not isolated.exists(), 'Isolated index must be new.')
    env = {'GIT_INDEX_FILE': str(isolated)}
    run.command('isolated-read-parent', ['git', 'read-tree', PARENT], repo, env_overrides=env)
    run.command('isolated-add-source', ['git', 'update-index', '--add', '--cacheinfo',
                                      '100644,' + blob + ',' + SOURCE_PATH], repo, env_overrides=env)
    tree = oid(run.command('write-new-source-only-tree', ['git', 'write-tree'], repo, env_overrides=env))
    main_index_after = index_path.read_bytes() if index_path.exists() else None
    require(main_index_after == main_index_before, 'Main index changed during isolated tree preparation; preserve and stop.')
    require(oid(run.command('head-after', ['git', 'rev-parse', 'HEAD'], repo)) == PARENT,
            'HEAD changed during source-tree preparation.')
    return {'status': 'PASS_NEW_SOURCE_BLOB_AND_SOURCE_ONLY_TREE', 'parent_sha': PARENT,
            'parent_tree_sha': parent_tree, 'tree_sha': tree, 'blob_sha': blob,
            'source_path': SOURCE_PATH, 'source_identity': SOURCE_ID,
            'frozen_source': str(frozen), 'known_blob_cache': str(run.path / 'NEW_BLOB_ID.json'),
            'isolated_index': str(isolated), 'main_index_exact_bytes_unchanged': True,
            'local_HEAD': PARENT, 'commit_created': False, 'ref_movement': False,
            'network_or_credentials': 'NONE', 'sha256_computations': 0,
            'foreign_untracked66': 'No add/reset/checkout/clean or worktree traversal; no foreign path is staged.'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', required=True)
    parser.add_argument('--frozen-source', required=True)
    parser.add_argument('--run-dir', required=True)
    parser.add_argument('--expected-parent', default=PARENT)
    parser.add_argument('--known-blob-record')
    args = parser.parse_args()
    run = CaptureRun(args.run_dir, 'prepare-source65-new-git-blob-and-tree')
    try:
        run.finish(perform(args, run))
        return 0
    except Exception as exc:
        run.finish({'status': 'FAIL_PRESERVED_NO_RETRY', 'exception': repr(exc),
                    'commit_created': False, 'ref_movement': False})
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
