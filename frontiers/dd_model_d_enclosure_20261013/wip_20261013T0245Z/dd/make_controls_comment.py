"""Builds the controls comment for note DD from: the branch manifest (pinned commit, per-file SHA-256), the controls stdout
(both modes), the mutants stdout, the assembly stdout (both modes) and the shard run record."""
import sys, json, hashlib, os
HERE = os.path.dirname(os.path.abspath(__file__))

def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()

def main(commit, run_id, artifacts_json, out_path):
    man = json.load(open('/home/claude/wt-ddwip/frontiers/dd_model_d_enclosure_20261013/wip_20261013T0245Z/MANIFEST.json'))
    files = {f['path']: f for f in man['files']}
    mods = ['dd/ddcore.py', 'dd/ddbounds.py', 'dd/ddtaylor.py', 'dd/ddint.py', 'dd/ddvq.py', 'dd/ddgauss.py', 'dd/ddS.py', 'dd/dd_exact.py', 'dd/dd_controls.py', 'dd/dd_mutants.py', 'dd/cells_full.json']
    nodes = ['dd/nodes/nodes_%d.json' % k for k in range(12)]
    controls = open(os.path.join(HERE, 'controls_stdout.txt')).read()
    mutants = open(os.path.join(HERE, 'mutants_stdout.txt')).read()
    assembly = open(os.path.join(HERE, 'assembly_stdout.txt')).read()
    arts = json.load(open(artifacts_json))
    lines = []
    lines.append('**Controls of note DD — the certificate\'s files, pinned; the controls, the mutants and the assembly, with their stdout.** Companion of the note comment above. Dylan Roy — delegated AI work; actual performer Anthropic Claude, session `session_01NMeKEismAyeqgdB4sy2NJU`. Scientific effect NONE.\n')
    lines.append('**Where the bytes are.** The certificate is too large for one comment (eleven files, about 140 KB). It is pinned at Math- commit `%s` (branch `claude/dd-model-d-enclosure-wip-20261013`, draft PR Math-#446), directory `frontiers/dd_model_d_enclosure_20261013/wip_20261013T0245Z/`; `MANIFEST.json` there lists every file with its byte count and SHA-256. The files that matter for the reads:\n' % commit)
    lines.append('| File | Bytes | SHA-256 |\n|---|---|---|')
    for m in mods + nodes:
        f = files[m]
        lines.append('| `%s` | %d | `%s` |' % (m, f['bytes'], f['sha256']))
    lines.append('')
    lines.append('**The node values** (`dd/nodes/nodes_k.json`, `k = 0..11`: the cells with index `≡ k (mod 12)`) were computed on GitHub-hosted runners by the branch workflow `.github/workflows/dd-wip-shards.yml`, run [%s](https://github.com/d6g8k5htny-coder/Math-/actions/runs/%s) (`python -B -S ddgauss.py eval cells_full.json nodes_k.json 4 k/12`); the stored files are the run\'s artifacts byte for byte (artifact ids and digests: %s). Anyone can recompute any node: `python3 -c "import ddgauss as G, json; ..."` as in `dd_exact.py`\'s sample check, or the whole shard (26–75 minutes on four cores).\n' % (run_id, run_id, ', '.join('`%s` `%s`' % (a['id'], a['digest']) for a in arts)))
    lines.append('**How to replay** (Python 3.11+, standard library only; from `dd/`):\n```\npython3 -B -S dd_controls.py            # C1–C9, exit 0\npython3 -B -S dd_mutants.py             # nine mutants, each must be rejected, exit 0\npython3 -B -S dd_exact.py cells_full.json nodes/nodes_0.json ... nodes/nodes_11.json   # tiling, every cell remainder recomputed, 24 node values recomputed, D and the corollary\n```\nThe stdout of each is identical under `python3 -B -O -S` (checked). `dd_exact.py` takes about 20 minutes (the remainder recomputation); `--no-recheck` skips it.\n')
    lines.append('**`dd_controls.py` stdout** (both modes identical):\n```\n' + controls.strip() + '\n```\n')
    lines.append('**`dd_mutants.py` stdout:**\n```\n' + mutants.strip() + '\n```\n')
    lines.append('**`dd_exact.py` stdout** (both modes identical):\n```\n' + assembly.strip() + '\n```\n')
    lines.append('**Author-side referee round** (clean context, same session, before posting): lemmas PASS; implementation BLOCK + AMEND as listed in the note\'s Remark 4, all applied before the final run. Not review evidence.\n')
    lines.append('🤖 Generated with [Claude Code](https://claude.com/claude-code)')
    open(out_path, 'w').write('\n'.join(lines))
    print(out_path, len('\n'.join(lines)), 'chars')

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
