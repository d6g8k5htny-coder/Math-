#!/usr/bin/env python3
"""PROPOSAL: root-only eligible source65 own-object copy ONCE, no digest calculation."""
from pathlib import Path
import argparse
import json
import os
import sys
from capture import CaptureRun, put_new, require, sync_dir
from prepare_source_tree import SOURCE_ID, oid

OBJECT_ID = {'bytes': 1852408, 'sha256': '5fbf02004a484d7447147d09b0cd8d19bc84b0ef5c96e97aa6655fc54f88a319'}
OBJECT_NAME = 'SourceActualSaddleUppercuts.olean'


def perform(args, run, state):
    cut = json.loads(Path(args.source_cut_record).read_text())
    require(cut['status'] == 'PASS_NATIVE_SOURCE_COMMIT_IMPORTED_AND_LOCAL_CUT_ESTABLISHED',
            'Genuine native source cut/local CAS/index completion must precede eligible own copy.')
    require(cut['source_identity'] == SOURCE_ID, 'Different qualified source identity.')
    native = cut['native_sha']
    record_path = Path(args.copy_record).resolve()
    destination = Path(args.cache_destination).resolve()
    require(destination.name == OBJECT_NAME, 'Only eligible new source65 own module may enter cache.')
    if record_path.exists():
        old = json.loads(record_path.read_text())
        require(old['status'] == 'PASS_ROOT_ONLY_ELIGIBLE_OWN_COPY_ONCE' and
                old['source_cut'] == native and old['own_object_identity'] == OBJECT_ID and
                old['destination'] == str(destination), 'Existing copy record differs; STOP, never overwrite.')
        return {'status': 'SKIP_ALREADY_COMPLETED_OWN_COPY_EVIDENCE_REUSED',
                'copy_record': str(record_path), 'source_cut': native, 'own_object_identity': OBJECT_ID,
                'new_copies_this_invocation': 0, 'completed_copy_count_reused': 1,
                'existing_object_rehash_or_byte_recheck': False}
    intent_path = record_path.with_name(record_path.stem + '_INTENT.json')
    require(not intent_path.exists(), 'Prior unresolved copy intent; preserve uncertainty, no automatic retry.')
    require(not destination.exists(), 'Destination exists without the matching completed copy record; STOP, no overwrite/backfill.')
    source = Path(args.object_source).resolve()
    require(source.name == OBJECT_NAME and source != destination, 'Only distinct qualified source65 own object may be copied.')
    kernel = json.loads(Path(args.kernel_receipt).read_text())
    require(kernel['exit_code'] == 0 and any('leanchecker' in x for x in kernel['command_argv']),
            'Completed actual own-kernel PASS record required; no kernel execution here.')
    matching = [v for v in kernel['after'].values() if isinstance(v, dict) and
                v.get('bytes') == OBJECT_ID['bytes'] and v.get('sha256') == OBJECT_ID['sha256']]
    require(matching, 'Stored kernel binding does not include the qualified final eligible own object.')
    require(oid(run.command('actual-genuine-sourcecut-HEAD', ['git', 'rev-parse', 'HEAD'], args.repo)) == native,
            'Own copy must bind the actual imported native source cut.')
    data = source.read_bytes()
    require(len(data) == OBJECT_ID['bytes'], 'Qualified own-object size changed; no replacement or rehash.')
    intent = {'status': 'ROOT_ONLY_ELIGIBLE_NEW_SOURCE65_OWN_COPY_INTENT',
              'source_cut': native, 'source': str(source), 'destination': str(destination),
              'own_object_identity': OBJECT_ID, 'qualified_source_identity': SOURCE_ID,
              'kernel_receipt': str(Path(args.kernel_receipt).resolve()),
              'source_cut_record': str(Path(args.source_cut_record).resolve()),
              'identity_effect': 'Known completed qualification identity REUSED; SHA256 NOT computed.',
              'all_other_objects': 'SKIP Controls/helper/old/ilean/intermediate objects'}
    put_new(intent_path, intent)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open('xb') as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    sync_dir(destination.parent)
    state['new_copy_write_completed'] = True
    require(destination.read_bytes() == data, 'NEW copy byte transport mismatch; preserve, no overwrite/retry.')
    result = {**intent, 'status': 'PASS_ROOT_ONLY_ELIGIBLE_OWN_COPY_ONCE',
              'copy_count': 1, 'further_copy_actions': 'ALL_SKIP',
              'new_copy_byte_transport_equal': True, 'sha256_computations': 0}
    put_new(record_path, result)
    return {**result, 'copy_record': str(record_path), 'new_copies_this_invocation': 1}


def main():
    parser = argparse.ArgumentParser()
    for name in ['repo', 'object-source', 'cache-destination', 'source-cut-record', 'kernel-receipt', 'copy-record', 'run-dir']:
        parser.add_argument('--' + name, required=True)
    args = parser.parse_args()
    run = CaptureRun(args.run_dir, 'root-only-new-source65-eligible-own-copy')
    state = {'new_copy_write_completed': False}
    try:
        run.finish(perform(args, run, state))
        return 0
    except Exception as exc:
        run.finish({'status': 'FAIL_COPY_PRESERVED_NO_AUTOMATIC_RETRY', 'exception': repr(exc), **state,
                    'all_other_objects': 'SKIP', 'copy_failure_rule': 'Never overwrite an existing/partially written destination or recompute an old digest. Root resolves only the actual incomplete operation.'})
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
