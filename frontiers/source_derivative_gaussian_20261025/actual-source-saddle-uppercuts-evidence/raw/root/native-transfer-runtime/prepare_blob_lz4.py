#!/usr/bin/env python3
"""UNEXECUTED root proposal: capture ONE supplied NEW Git blob and raw-LZ4 it.
No SHA256, mathematical verification, network, credential or API operation.
"""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import base64
import ctypes
import json
import os
import re
import subprocess
import sys
import time


def utc():
    return datetime.now(timezone.utc).isoformat()


def write_json_new(path, value):
    with Path(path).open('x', encoding='utf-8') as stream:
        json.dump(value, stream, indent=2, ensure_ascii=False)
        stream.write('\n')
        stream.flush()
        os.fsync(stream.fileno())


def write_bytes_new(path, value):
    with Path(path).open('xb') as stream:
        stream.write(value)
        stream.flush()
        os.fsync(stream.fileno())


def main():
    parser = argparse.ArgumentParser(description='Root Git-byte transport only, no digest calculation.')
    parser.add_argument('--repo', required=True)
    parser.add_argument('--new-blob-sha', required=True)
    parser.add_argument('--run-dir', required=True)
    parser.add_argument('--base64-chunk-chars', type=int, default=32768)
    args = parser.parse_args()
    if not re.fullmatch('[0-9a-f]{40}', args.new_blob_sha):
        parser.error('An actual supplied local NEW Git SHA1 blob ID is required.')
    if args.base64_chunk_chars <= 0 or args.base64_chunk_chars % 4:
        parser.error('Base64 chunk length must be a positive multiple of4.')
    repo = Path(args.repo).resolve()
    run = Path(args.run_dir).resolve()
    run.mkdir(parents=True, exist_ok=False)
    started = utc()
    tick = time.monotonic()
    write_json_new(run / 'STARTED.json', {
        'script_argv': sys.argv, 'cwd': os.getcwd(), 'started_utc': started,
        'known_blob_sha': args.new_blob_sha,
        'scope': 'Transfer supplied NEW Git blob bytes only; caller has already excluded remote-known blobs.',
        'old_math_checks_hashes_network_credentials_API': 'NONE',
    })
    try:
        command = ['git', 'cat-file', 'blob', args.new_blob_sha]
        git_start = utc()
        git_tick = time.monotonic()
        write_json_new(run / 'GIT_INTENT.json', {
            'command_argv': command, 'cwd': str(repo), 'started_utc': git_start,
            'supplied_known_NEW_blob_sha': args.new_blob_sha,
            'stdout': 'git.stdout.blob', 'stderr': 'git.stderr.log',
            'capture': 'Prospective full original separate streams; no content printed.',
        })
        with (run / 'git.stdout.blob').open('xb') as out, (run / 'git.stderr.log').open('xb') as err:
            process = subprocess.run(command, cwd=str(repo), stdout=out, stderr=err)
            out.flush()
            os.fsync(out.fileno())
            err.flush()
            os.fsync(err.fileno())
        write_json_new(run / 'GIT_RECEIPT.json', {
            'command_argv': command, 'cwd': str(repo), 'started_utc': git_start,
            'ended_utc': utc(), 'elapsed_seconds': time.monotonic() - git_tick,
            'exit_code': process.returncode, 'stdout': 'git.stdout.blob', 'stderr': 'git.stderr.log',
            'stdout_bytes': (run / 'git.stdout.blob').stat().st_size,
            'stderr_bytes': (run / 'git.stderr.log').stat().st_size,
            'known_blob_sha_reused': args.new_blob_sha, 'digest_computations': 0,
        })
        if process.returncode:
            raise RuntimeError('Actual git cat-file failed; preserve all original streams, no automatic retry.')
        raw = (run / 'git.stdout.blob').read_bytes()
        if len(raw) > 0x7E000000:
            raise RuntimeError('Input exceeds liblz4 raw-block supported maximum; no truncation.')
        lib = ctypes.CDLL('liblz4.so.1')
        lib.LZ4_compressBound.argtypes = [ctypes.c_int]
        lib.LZ4_compressBound.restype = ctypes.c_int
        lib.LZ4_compress_default.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.c_int]
        lib.LZ4_compress_default.restype = ctypes.c_int
        bound = lib.LZ4_compressBound(len(raw))
        if bound <= 0:
            raise RuntimeError('liblz4 returned invalid compression bound.')
        source = ctypes.create_string_buffer(raw, max(1, len(raw)))
        target = ctypes.create_string_buffer(bound)
        count = lib.LZ4_compress_default(ctypes.cast(source, ctypes.c_void_p),
                                        ctypes.cast(target, ctypes.c_void_p), len(raw), bound)
        if count <= 0 or count > bound:
            raise RuntimeError('liblz4 raw-block compression failed.')
        compressed = target.raw[:count]
        write_bytes_new(run / 'blob.raw-lz4', compressed)
        encoded = base64.b64encode(compressed)
        write_bytes_new(run / 'blob.raw-lz4.b64', encoded)
        chunks = run / 'base64-chunks'
        chunks.mkdir()
        rows = []
        for number, offset in enumerate(range(0, len(encoded), args.base64_chunk_chars)):
            part = encoded[offset:offset + args.base64_chunk_chars]
            path = chunks / ('%06d.txt' % number)
            write_bytes_new(path, part)
            rows.append({'index': number, 'path': str(path), 'base64_chars': len(part)})
        result = {
            'status': 'NEW_GIT_BLOB_RAW_LZ4_TRANSFER_PREPARED_NOT_YET_NATIVE_UPLOAD_QUALIFIED',
            'known_local_git_blob_sha': args.new_blob_sha,
            'raw_bytes': len(raw), 'raw_original_stdout': str(run / 'git.stdout.blob'),
            'compressed_format': 'LZ4 raw block; NO frame/header/checksum',
            'compressed_bytes': count, 'compressed_path': str(run / 'blob.raw-lz4'),
            'compressed_base64_path': str(run / 'blob.raw-lz4.b64'),
            'compressed_base64_chars': len(encoded), 'ordered_base64_chunks': rows,
            'required_receiver_gate': 'PureJS bounds/exact-size decode, upload exact decompressed bytes as base64; native returned Git blob SHA MUST equal known_local_git_blob_sha.',
            'content_transformation': 'NONE: source is exact git cat-file stdout bytes; no JSON parse/reconstruction/newline conversion.',
            'sha256_or_math_checks': 0, 'API_or_external_or_credential_actions': 0,
            'started_utc': started, 'ended_utc': utc(), 'elapsed_seconds': time.monotonic() - tick,
        }
        write_json_new(run / 'TRANSFER.json', result)
        print(json.dumps({'status': result['status'], 'metadata': str(run / 'TRANSFER.json'),
                          'raw_bytes': len(raw), 'compressed_bytes': count,
                          'base64_chunks': len(rows), 'known_blob_sha': args.new_blob_sha}, sort_keys=True))
        return 0
    except Exception as exc:
        write_json_new(run / 'FAILURE.json', {
            'status': 'ACTUAL_TRANSFER_PREPARATION_FAILURE_PRESERVED_NO_AUTOMATIC_RETRY',
            'exception': repr(exc), 'known_blob_sha': args.new_blob_sha,
            'started_utc': started, 'ended_utc': utc(), 'elapsed_seconds': time.monotonic() - tick,
            'child_capture_limit': 'If a child never spawned or was interrupted, no invented child exit/outer UTC is supplied.',
        })
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
