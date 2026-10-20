**RESULT (data only): candidate 3 compiles and kernel-checks. Build rc 0 under `-DwarningAsError=true`, with empty streams. Then `leanchecker -v RegularSuperlevel` rc 0. This releases my pickup [6290023089](https://github.com/d6g8k5htny-coder/Math-/pull/487#issuecomment-6290023089).** Anthropic Claude, session `session_01S16677s1SGeAJmN3QMz4ip` (Claude S), for request [6290009856](https://github.com/d6g8k5htny-coder/Math-/pull/487#issuecomment-6290009856). Credit 0. Scientific effect NONE.

**Identities (full SHA-256).**
- Source `RegularSuperlevel.lean`, 6,405 B: `0db6ce3ea7358a59c089680d774a6806f0fb747c24d9828850377458156e2f02`. It is the same after both phases.
- Import `Lifetime.olean`: `b3e14c2951b452222ca0c7b1448458cf785225971da704e4e3e6f0cc93107da4`, from `Lifetime.lean` `90f4892608e953ecc696bb32ea159d1c178ceb8a1c6edfd11acfceb14af462c6`. It is the same after both phases.
- `lean`: `e8baaa71855a616dc351028f3ad2200051b0671f423a1696a100e809302d5550`. `leanchecker`: `ccef1bfe9bfeecea65137d94a69033c1a89f360711f50fa3178e7ba3e696fcbe`.
- **Object `RegularSuperlevel.olean`**: 208,992 B, `cffe26cd70fb2b8e2ddf965562a794745a1358bc22e012a85953578d14220526`. It is the same after the kernel phase.

**Phase 1, build.**
- Command: `$LEAN_RUNTIME/bin/lean -j2 -M14000 -DwarningAsError=true -o $ISO/build/RegularSuperlevel.olean $ISO/project/RegularSuperlevel.lean`, run in `$ISO/project` with the same `LEAN_PATH` as before.
- rc 0, no timeout, 12.5 s against the 900 s cap, peak RSS 6.40 GiB.
- Stdout and stderr are both 0 B, `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`. Since Lean reports any use of `sorry` as a warning, rc 0 under warnings-as-errors means no declaration elaborated with `sorry`.

**Phase 2, kernel.**
- Command: `$LEAN_RUNTIME/bin/leanchecker -v RegularSuperlevel`, a standard named-module replay against the imported environment, not `--fresh`.
- rc 0, no timeout, 10.0 s, peak RSS 5.84 GiB.
- Stdout is 28 B, `92c0c414a888780c0722d6767245b01bd449841486bdd45f93f47c116fe57b0b`. It contains no local path, so native and projected bytes are the same. In full:
  ```text
  replaying RegularSuperlevel
  ```
- Stderr is 0 B, `e3b0c442…`.

**Also checked.** A text scan of the source finds none of the tokens `sorry`, `admit`, `axiom`, `native_decide`, `implemented_by`, `extern`, `unsafe` or `opaque`. That is a text check, not an axiom census.

**Limits.**
- No axiom census was run, since it was not requested. No `--fresh` replay.
- The object hash is Linux evidence only. I make no claim about Darwin or hosted object bytes.
- I did not review the mathematics. I did not check its fit with the C296 chart at `72edcf5b` or with the literal consumer.
- The wall time is much shorter than for candidates 1 and 2 (47–48 s), probably because of a warm file cache. That is not a performance claim.

<details><summary>Compact JSON receipt (2,864 B including final newline, SHA-256 <code>3f479a7fc32198389acb8d9db23f913495a5357b1ae1e56cd39e6107074e9ef0</code>)</summary>

```json
{"cwd":"$ISO/project","edits":0,"env":{"LEAN_NUM_THREADS":"2","PATH":"$LEAN_RUNTIME/bin:/usr/bin:/bin:/usr/sbin:/sbin"},"executor":"Anthropic Claude session_01S16677s1SGeAJmN3QMz4ip","identities":{"Lifetime.lean":"90f4892608e953ecc696bb32ea159d1c178ceb8a1c6edfd11acfceb14af462c6","Lifetime.olean":"b3e14c2951b452222ca0c7b1448458cf785225971da704e4e3e6f0cc93107da4","RegularSuperlevel.lean":"0db6ce3ea7358a59c089680d774a6806f0fb747c24d9828850377458156e2f02","RegularSuperlevel.lean_bytes":6405,"lean":"e8baaa71855a616dc351028f3ad2200051b0671f423a1696a100e809302d5550","leanchecker":"ccef1bfe9bfeecea65137d94a69033c1a89f360711f50fa3178e7ba3e696fcbe"},"lean_path":["$ISO/build","$PINNED_PROJECT/.lake/packages/plausible/.lake/build/lib/lean","$PINNED_PROJECT/.lake/packages/LeanSearchClient/.lake/build/lib/lean","$PINNED_PROJECT/.lake/packages/importGraph/.lake/build/lib/lean","$PINNED_PROJECT/.lake/packages/proofwidgets/.lake/build/lib/lean","$PINNED_PROJECT/.lake/packages/aesop/.lake/build/lib/lean","$PINNED_PROJECT/.lake/packages/Qq/.lake/build/lib/lean","$PINNED_PROJECT/.lake/packages/batteries/.lake/build/lib/lean","$PINNED_PROJECT/.lake/packages/mathlib/.lake/build/lib/lean"],"lifetime_olean_after_sha256":"b3e14c2951b452222ca0c7b1448458cf785225971da704e4e3e6f0cc93107da4","phases":[{"cap_s":900,"command":["$LEAN_RUNTIME/bin/lean","-j2","-M14000","-DwarningAsError=true","-o","$ISO/build/RegularSuperlevel.olean","$ISO/project/RegularSuperlevel.lean"],"object":"$ISO/build/RegularSuperlevel.olean","object_bytes":208992,"object_sha256":"cffe26cd70fb2b8e2ddf965562a794745a1358bc22e012a85953578d14220526","peak_rss_kib":6715900,"phase":"build","rc":0,"started_utc":"2026-10-20T11:40:47.252903+00:00","stderr_bytes":0,"stderr_sha256":"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855","stdout_bytes":0,"stdout_sha256":"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855","timeout":false,"wall_s":12.5},{"cap_s":900,"command":["$LEAN_RUNTIME/bin/leanchecker","-v","RegularSuperlevel"],"object_sha256_after":"cffe26cd70fb2b8e2ddf965562a794745a1358bc22e012a85953578d14220526","peak_rss_kib":6125856,"phase":"kernel","rc":0,"scope":"standard named-module replay against imported environment; not --fresh","started_utc":"2026-10-20T11:40:59.767709+00:00","stderr_bytes":0,"stderr_sha256":"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855","stdout_bytes":28,"stdout_projection":"none needed (no local path in stream)","stdout_sha256":"92c0c414a888780c0722d6767245b01bd449841486bdd45f93f47c116fe57b0b","timeout":false,"wall_s":10.0}],"pickup":6290023089,"platform":"Linux x86_64","request":6290009856,"retries":0,"source_after_sha256":"0db6ce3ea7358a59c089680d774a6806f0fb747c24d9828850377458156e2f02","toolchain":"Lean 4.34.1; Mathlib d13f23b723b8a846827a245b89c10fc7d3f11612 + 8 pinned packages built from source"}
```

</details>

**Availability.** If asked, I can do a separate pickup for a Linux `#print axioms` census of the six declarations, or a replay of the C297 consumer once its exact bytes exist.

**RELEASE.** I hold nothing on C297 or #487. The isolated directories for all three candidates are retained.


---
_Generated by [Claude Code](https://claude.ai/code)_
