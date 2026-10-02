#!/usr/bin/env python3
"""Check docs/integration/2026-10-02-proof-reachability.md against git (standard library only).

The document pins a cut commit. For that cut, every row of its reachability table must name a
frontiers/<folder>/PROOF.md that exists there, with its exact git blob; the stated integration commit
must be the first-parent commit of the cut's history that added the path; the "linked" column must
agree with PROOF_INDEX.md at the cut; every frontiers/*/PROOF.md at the cut must appear exactly once;
and the table must carry no verdict words. Availability only: nothing here reads or grades a proof.

Usage: python3 -B -S tools/check_proof_reachability.py [document]   (exit 0 iff every check passes)
"""
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
VERDICT_WORDS = ('ACCEPT', 'AMEND', 'HOLD', 'CONFIRMED', 'VERIFIED', 'PASS', 'REJECT', 'APPROVED', 'FAIL')


def git(*args):
    return subprocess.run(['git', *args], capture_output=True, text=True, check=True).stdout.strip()


def parse(text):
    """Return (cut, rows, table_lines) from the document text."""
    m = CUT_RE.search(text)
    cut = m.group(1) if m else None
    rows, table_lines = [], []
    for line in text.splitlines():
        if line.startswith('| [`'):
            table_lines.append(line)
            mm = ROW_RE.match(line)
            rows.append(mm.groupdict() if mm else {'malformed': line})
    return cut, rows, table_lines


def verdict_words(lines):
    bad = []
    for line in lines:
        for w in VERDICT_WORDS:
            if re.search(r'\b' + w + r'\b', line, flags=re.I):
                bad.append((w, line[:80]))
    return bad


def check(text):
    failures = []
    cut, rows, table_lines = parse(text)
    if cut is None:
        return ['no cut commit line']
    for w, line in verdict_words(table_lines):
        failures.append('verdict word %s in table row: %s' % (w, line))
    paths = sorted(p for p in git('ls-tree', '-r', '--name-only', cut).splitlines()
                   if re.fullmatch(r'frontiers/[^/]+/PROOF\.md', p))
    index = git('show', cut + ':PROOF_INDEX.md')
    seen = {}
    for r in rows:
        if 'malformed' in r:
            failures.append('malformed row: ' + r['malformed'][:100])
            continue
        path = 'frontiers/%s/PROOF.md' % r['folder']
        seen[path] = seen.get(path, 0) + 1
        if path not in paths:
            failures.append('not a PROOF.md at the cut: ' + path)
            continue
        if git('rev-parse', cut + ':' + path) != r['blob']:
            failures.append('blob mismatch: ' + path)
        added = git('log', cut, '--first-parent', '--diff-filter=A', '--format=%H %cs', '--', path).splitlines()
        if not added or not added[-1].startswith(r['commit']) or added[-1].split()[1] != r['date']:
            failures.append('integration commit/date mismatch: %s (%s)' % (path, added[-1] if added else 'none'))
        linked = ('frontiers/%s/' % r['folder']) in index or r['folder'] in index
        if (r['linked'] == 'yes') != linked:
            failures.append('PROOF_INDEX linkage mismatch: ' + path)
    for p in paths:
        if seen.get(p, 0) != 1:
            failures.append('appears %d times: %s' % (seen.get(p, 0), p))
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
