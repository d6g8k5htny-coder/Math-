# GP-DATA-114 embedded-source custody

Object: **OA-GP-DATA-114-EMBEDDED-CUSTODY-20260930-v1**. Scientific effect: **NONE**.
OpenAI / Codex recovery packet; **custody review required**. Shared-account work
supplies zero organizational-independence credit. [Root pickup](https://github.com/d6g8k5htny-coder/main/issues/86#issuecomment-5901405370).

This packet makes the two original embedded payloads individually readable. The
input is the already-public historical **GP-DATA-114-v1.1 clean wrapper**, which
intentionally retains v1.0 payload filenames. The distinct corrupt original
v1.0 publication is excluded. No bytes were reconstructed from a description,
reformatted, repaired, or replaced with a similar source.

## Exact source

Repository: `d6g8k5htny-coder/main`.
Commit: `7caac254cbba5f513b2dc0afb56b78a598bc0c93`.
Wrapper: 9220 bytes; Git blob
`0a1a98169a5283b7a253890fe8bb54a8a91cfe71`; SHA256
`948881341e610800b126623e559c9a45a6a1160a55b6fc69e172ef47ca107c37`.
The full immutable path and public URLs are in [SOURCES.json](SOURCES.json).
The wrapper is linked, not duplicated in this packet.

| Original basename | Bytes | SHA256 | Git blob |
|---|---:|---|---|
| `GP-DATA-114-v1.0_uniform_q_degree4_interval.py` | 9787 | `9d7cb5d6e13579533c5b485775e67c77da83c149c0bf8bbbe7b7bf85aefdb4ef` | `bbbfacee088332b4e4df9953079d579400f2282c` |
| `GP-DATA-114-v1.0_receipt.json` | 5047 | `8472209ee589f44f1f3c472c7040d183494743a89e21ad9487a1879d192003bc` | `77c511eaaab0dcd7863d4eebadfd2dcc69c9cb71` |

Both base64 blocks match the wrapper's declared compressed sizes and hashes:
source gzip 3416 bytes / `18c8768cf37d4557a8c04a9ae6e60523a185098012527403c0e627b259ff1e5c`;
receipt gzip 1692 bytes / `88bb5bce0b875ac2959d7cbcaff235db7ea60249e3124faeccc0d26fe8351222`.
Each is exactly one complete gzip member, with valid CRC and no trailing bytes
or additional member. Decoding verifies the full output size, SHA256 and Git
blob before permitting output.

## Reproduce without executing the archived verifier

Acquire the exact wrapper at the public immutable URL in SOURCES.json into a
separate temporary file, preserving BOM, CRLF and all bytes. From this directory:

```sh
python -B -S inert_decoder.py --wrapper-input /path/to/exact-wrapper.txt --verify-existing .
python -B -S test_inert_decoder.py --wrapper-input /path/to/exact-wrapper.txt
python -B -O -S test_inert_decoder.py --wrapper-input /path/to/exact-wrapper.txt
```

`--wrapper-input -` accepts exact bytes on stdin. To reproduce the two files in
a separate, previously nonexistent directory, use the new decoder's
`--write-new /path/to/new-directory` option. It verifies both payloads before
creating that directory and refuses an existing destination. The decoder uses
only the Python standard library. Its test fixture rebinding is an internal
test API; the CLI always pins the complete original wrapper.

Fresh checks: 15 controls in each normal/optimized mode, with identical JSON
summaries and zero failures/errors; original-file verification emits identical
reports in both modes. Controls include truncation, bad CRC, concatenated
members, trailing bytes, wrong hashes/sizes, duplicate markers, invalid base64,
unsafe names, altered stored payloads and symlinks. Real malformed gzip
fixtures are rebound to their own compressed identity to test the stream gate
itself. Test-first failures and all verification boundaries are retained in
[VALIDATION.json](VALIDATION.json). [MANIFEST.json](MANIFEST.json) binds every
packet file except itself; its exclusion avoids self-reference.

## Historical scope and limits

The source header describes an outward interval certificate for a degree-four
uniform-q Route-B corridor box, `0 < r <= 1/20`, and explicitly separates mass,
exact-field transfer, P0.1 and P0.2. Those are the historical source's claims,
not new verdicts supplied here. The recovered receipt is an original saved
result, not a fresh execution receipt. Its success labels remain historical.

Only new custody code was run or imported. The archived verifier was neither
run nor imported; its mpmath dependency was not installed or changed. No
mathematical acceptance, source-to-current-theorem alignment, numerical
certificate validation, status/graph transition, Boolean or prize follows
from byte identity. Original authorship is not inferred from the GP prefix.

The wrapper was already public. Current main/Math path checks and targeted
public-main blob probes found no individual decoded payload; these are bounded
observations. Earlier broader private extraction outputs may already contain
these hashes: **UNKNOWN**, not inspected. This packet claims individually
readable public byte custody, not globally new recovery. No private carrier,
credentials, unrelated material or live integration branch was inspected or
modified.
