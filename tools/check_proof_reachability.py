#!/usr/bin/env python3
"""Check docs/integration/2026-10-02-proof-reachability.md against git (standard library only).

The document pins a cut commit. For that cut, every row of its reachability table must name a
frontiers/<folder>/PROOF.md that exists there, with its exact git blob; the stated integration commit
must be the first-parent commit of the cut's history that added the path; the "linked" column must
agree with PROOF_INDEX.md at the cut; every frontiers/*/PROOF.md at the cut must appear exactly once;
the rows must follow first-parent integration order (position in `git rev-list --first-parent --reverse
<cut>`, ties by folder name); the commit and blob prefixes of the second (chain) table must agree with
the first; and no line of either table may carry a verdict word. Availability only: nothing here reads
or grades a proof. The additive post-C126 supplement also preserves the historical
document bytes and checks its separately pinned one-level delta, named nested
collections, full proof identities and immutable links.

Usage: python3 -B -S tools/check_proof_reachability.py [document]   (exit 0 iff every check passes)
"""
import functools
import hashlib
import re
import subprocess
import sys

DOC = 'docs/integration/2026-10-02-proof-reachability.md'
CUT_RE = re.compile(r'^Cut: `([0-9a-f]{40})`', re.M)
ROW_RE = re.compile(
    r'^\| \[`(?P<folder>[A-Za-z0-9_]+)`\]\(\.\./\.\./frontiers/(?P=folder)/PROOF\.md\) '
    r'\| `(?P<blob>[0-9a-f]{40})` '
    r'\| \[#(?P<pr>\d+)\]\(https://github\.com/d6g8k5htny-coder/Math-/pull/(?P=pr)\) '
    r'\| `(?P<commit>[0-9a-f]{12})` \((?P<date>\d{4}-\d{2}-\d{2})\) '
    r'\| (?P<linked>yes|no) \|$')
CHAIN_RE = re.compile(
    r'^\| `(?P<folder>[A-Za-z0-9_]+)` \| #(?P<pr>\d+) \| `(?P<commit>[0-9a-f]{12})` '
    r'\| `(?P<blob>[0-9a-f]{12})` \| (?P<receipt>\d+) \|$')
VERDICT_WORDS = ('ACCEPT', 'AMEND', 'HOLD', 'CONFIRMED', 'VERIFIED', 'PASS', 'REJECT', 'APPROVED', 'FAIL')
POST_START = '<!-- post-c126:start -->'
POST_END = '<!-- post-c126:end -->'
HISTORICAL_HEAD = 'ee087cea7cfa932daf0122aaee8227d1dfbadef4'
POST_ROW = re.compile(
    r'^\| \[source: `(?P<path>frontiers/[A-Za-z0-9_/]+/PROOF\.md)`\]'
    r'\(https://github\.com/d6g8k5htny-coder/Math-/blob/(?P<cut>[0-9a-f]{40})/(?P=path)\) '
    r'\| `(?P<blob>[0-9a-f]{40})` \| `(?P<sha256>[0-9a-f]{64})` \|$')


@functools.lru_cache(maxsize=None)
def git(*args):
    """Every query names the pinned cut, so its answer cannot change within a run; cache it."""
    return subprocess.run(['git', *args], capture_output=True, text=True, check=True).stdout.strip()


def parse(text):
    """Return (cut, rows, table_lines) from the document text (inventory rows only)."""
    m = CUT_RE.search(text)
    cut = m.group(1) if m else None
    rows, table_lines = [], []
    for line in text.splitlines():
        if line.startswith('| [`'):
            table_lines.append(line)
            mm = ROW_RE.match(line)
            rows.append(mm.groupdict() if mm else {'malformed': line})
    return cut, rows, table_lines


def all_table_lines(text):
    """Every line of every Markdown table in the document: headers, separators and data rows."""
    return [line for line in text.splitlines() if line.startswith('|')]


def chain_rows(text):
    """Data rows of the second (chain) table: lines of the form | `folder` | #PR | ..."""
    out = []
    for line in text.splitlines():
        if line.startswith('| `'):
            mm = CHAIN_RE.match(line)
            out.append(mm.groupdict() if mm else {'malformed': line})
    return out


def verdict_words(lines):
    bad = []
    for line in lines:
        for w in VERDICT_WORDS:
            if re.search(r'\b' + w + r'\b', line, flags=re.I):
                bad.append((w, line[:80]))
    return bad


@functools.lru_cache(maxsize=None)
def source_bytes(cut, path):
    """Retain every byte, including terminal newlines, for identity checks."""
    return subprocess.run(['git', 'show', cut + ':' + path],
                          capture_output=True, check=True).stdout


def check_post_cut(text, old_cut):
    """Check the additive later-cut inventory without replacing the historical cut."""
    if text.count(POST_START) != 1 or text.count(POST_END) != 1:
        return ['post-cut supplement must occur exactly once']
    original, rest = text.split(POST_START)
    supplement, tail = rest.split(POST_END)
    failures = []
    if tail.strip():
        failures.append('unexpected content after post-cut supplement')
    if original.encode('utf-8') != source_bytes(HISTORICAL_HEAD, DOC):
        failures.append('historical document changed')
    cuts = re.findall(r'^Post-C126 cut: `([0-9a-f]{40})`\.$', supplement, re.M)
    if len(cuts) != 1:
        return failures + ['post-cut commit must occur exactly once']
    cut = cuts[0]
    try:
        if git('merge-base', old_cut, cut) != old_cut:
            return failures + ['post-cut does not descend from historical cut']
        old_paths = set(git('ls-tree', '-r', '--name-only', old_cut).splitlines())
        new_paths = set(git('ls-tree', '-r', '--name-only', cut).splitlines())
    except subprocess.CalledProcessError:
        return failures + ['post-cut commit unavailable']
    old_one = {p for p in old_paths if re.fullmatch(r'frontiers/[^/]+/PROOF\.md', p)}
    new_one = {p for p in new_paths if re.fullmatch(r'frontiers/[^/]+/PROOF\.md', p)}
    added, retained, removed = new_one - old_one, new_one & old_one, old_one - new_one
    nested = {p for p in new_paths if re.fullmatch(
        r'frontiers/(planar_soft_layer_chain_20261003/C\d+|'
        r'planar_rejected_endpoint_margin_20261003/A4)/PROOF\.md', p)}
    counts = 'One-level inventory: %d paths; %d retained; %d added; %d removed.' % (
        len(new_one), len(retained), len(added), len(removed))
    nested_count = 'Nested inventory: %d proof paths in the two named collections below.' % len(nested)
    if supplement.splitlines().count(counts) != 1 or supplement.splitlines().count(nested_count) != 1:
        failures.append('post-cut inventory count mismatch')
    for path in retained:
        if git('rev-parse', old_cut + ':' + path) != git('rev-parse', cut + ':' + path):
            failures.append('retained proof changed: ' + path)
    seen = []
    for line in supplement.splitlines():
        if not line.startswith('| [source:'):
            continue
        match = POST_ROW.fullmatch(line)
        if not match:
            failures.append('malformed post-cut source row')
            continue
        row = match.groupdict()
        path = row['path']
        seen.append(path)
        if path not in added | nested:
            failures.append('unexpected post-cut source: ' + path)
            continue
        if (row['cut'] != cut or row['blob'] != git('rev-parse', cut + ':' + path)
                or row['sha256'] != hashlib.sha256(source_bytes(cut, path)).hexdigest()):
            failures.append('post-cut source identity mismatch: ' + path)
    if len(seen) != len(set(seen)) or set(seen) != added | nested:
        failures.append('post-cut source membership mismatch')
    if seen != sorted(added) + sorted(nested):
        failures.append('post-cut source order mismatch')
    return failures


def check(text):
    failures = []
    cut, rows, table_lines = parse(text)
    if cut is None:
        return ['no cut commit line']
    for w, line in verdict_words(all_table_lines(text)):
        failures.append('verdict word %s in table row: %s' % (w, line))
    paths = sorted(p for p in git('ls-tree', '-r', '--name-only', cut).splitlines()
                   if re.fullmatch(r'frontiers/[^/]+/PROOF\.md', p))
    index = git('show', cut + ':PROOF_INDEX.md')
    position = {h: i for i, h in enumerate(git('rev-list', '--first-parent', '--reverse', cut).splitlines())}
    seen, keys, computed = {}, [], {}
    for r in rows:
        if 'malformed' in r:
            failures.append('malformed row: ' + r['malformed'][:100])
            continue
        path = 'frontiers/%s/PROOF.md' % r['folder']
        seen[path] = seen.get(path, 0) + 1
        if path not in paths:
            failures.append('not a PROOF.md at the cut: ' + path)
            continue
        blob = git('rev-parse', cut + ':' + path)
        if blob != r['blob']:
            failures.append('blob mismatch: ' + path)
        added = git('log', cut, '--first-parent', '--diff-filter=A', '--format=%H %cs', '--', path).splitlines()
        if not added or not added[-1].startswith(r['commit']) or added[-1].split()[1] != r['date']:
            failures.append('integration commit/date mismatch: %s (%s)' % (path, added[-1] if added else 'none'))
        if added:
            commit = added[-1].split()[0]
            keys.append((position[commit], r['folder']))
            computed[r['folder']] = (r['pr'], commit, blob)
        linked = ('frontiers/%s/' % r['folder']) in index or r['folder'] in index
        if (r['linked'] == 'yes') != linked:
            failures.append('PROOF_INDEX linkage mismatch: ' + path)
    for p in paths:
        if seen.get(p, 0) != 1:
            failures.append('appears %d times: %s' % (seen.get(p, 0), p))
    for a, b in zip(keys, keys[1:]):
        if a > b:
            failures.append('row order: %s (first-parent position %d) is listed before %s (position %d)'
                            % (a[1], a[0], b[1], b[0]))
    for c in chain_rows(text):
        if 'malformed' in c:
            failures.append('malformed chain-table row: ' + c['malformed'][:100])
            continue
        if c['folder'] not in computed:
            failures.append('chain-table packet not in the inventory: ' + c['folder'])
            continue
        pr, commit, blob = computed[c['folder']]
        if c['pr'] != pr or not commit.startswith(c['commit']) or not blob.startswith(c['blob']):
            failures.append('chain-table identity mismatch: ' + c['folder'])
    failures.extend(check_post_cut(text, cut))
    return failures


def main(argv):
    doc = argv[1] if len(argv) > 1 else DOC
    with open(doc, encoding='utf-8') as fh:
        failures = check(fh.read())
    for f in failures:
        print('FAIL', f)
    print('proof-reachability: %s' % ('OK' if not failures else '%d failure(s)' % len(failures)))
    return 0 if not failures else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv))
