# NEW Git blob byte transport — unexecuted proposal

This is byte transfer only. Neither file has been executed, imported, tested, hashed or used for an API/credential/external action by the helper. No proof/source role or mathematical verification is introduced. Prior source-cut/unsigned-import originals remain untouched; the latter is historical and MUST NOT be used for final commit import. Exact public Git fetch with authentication disabled is the root's already-proven raw-commit import route.

Root can wrap this future Python CLI in the already-supplied capture.py entry/outer/worker recorders:

    python prepare_blob_lz4.py --repo ACTUAL_REPO --new-blob-sha ACTUAL_NEEDED_NEW_LOCAL_BLOB_SHA --run-dir NEW_ROOT_TRANSPORT_RUN

Caller must supply only a needed NEW local blob, after excluding all remote-known blob SHAs from the sourcecut b2d4c91162d98a1daefb5377bf3e65ef8615dd57 tree. No automatic old-blob enumeration, hash or remote read occurs here. git cat-file blob SHA is captured in full to git.stdout.blob plus git.stderr.log, with actual argv/cwd/start/end/exit and no large output printing. Source bytes are not parsed as JSON or normalized. liblz4.so.1 is loaded only upon future root execution; root's availability observation is reused. LZ4_compressBound/LZ4_compress_default yield a RAW block, not an LZ4 frame. TRANSFER.json records raw/compressed sizes, compressed paths, supplied known Git blob SHA and ordered32768-character base64 chunk file paths. There is no SHA256 calculation.

The pure JavaScript file defines four functions directly, with no imports/atob/TextDecoder/DecompressionStream or automatic API call. Root loads/pastes these definitions into its functions isolate, reads the small compressed base64 chunks in numeric order, and obtains:

    const content = exactGitBlobBase64FromLZ4(chunks, transfer.raw_bytes, transfer.compressed_bytes);

The functions manually decode/encode standard base64 and decode standard raw LZ4 token literals, extended lengths, little-endian offsets and overlapping match copies. Input/output bounds, padding and exact supplied sizes are checked. Those bounds are transport integrity checks, not mathematical verification or a content hash.

Root then calls native github_create_blob with {content, encoding:'base64', repository_full_name:actualRepo}. It MUST require returned blob SHA equals TRANSFER.known_local_git_blob_sha before using that SHA in a tree entry. This ONE new upload SHA match is the actual qualification of the new transport. This proposal makes no passing/tested claim. Never print the decompressed11MB content or its15MB base64 as a tool response. Keep actual API response/intent/ID-match result; no duplicate uploads to obtain labels and no silent retry after uncertain writes.

Build native trees only from blob SHA entries plus the actual base tree; bounded batches may upload unique NEW blobs, reusing remote-known/in-call-created IDs. No content reconstruction through JSON is needed. Root alone performs native writes/final normal fast-forward expectedee5/forcefalse and exact raw-commit public Git fetch; packager/math verification remains unchanged. Metadata's single association attempt is STILL on hold until explicit final GO.
