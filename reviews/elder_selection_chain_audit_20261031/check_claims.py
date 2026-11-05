#!/usr/bin/env python3
"""Identity and dependency check for CLAIMS.json (reviews/elder_selection_chain_audit_20261031).

What it checks, and nothing more:
  * every source entry resolves in the local Git object store to a blob of exactly the recorded
    byte length and SHA-256; when the recorded commit is available locally, the recorded path
    must exist at that commit and map to that blob (a missing path is FAIL; only an absent
    commit is a NOTE);
  * every claim uses a status from the owner's five-value taxonomy, cites at least one source,
    and every `depends_on`, `sources` and `reviews` reference resolves;
  * a claim marked Proved depends only on claims marked Proved (status propagation: a Proved
    claim resting on a Conditional, Conjectural, Refuted or Proved-under-assumptions claim is
    Conditional by the record's own rule);
  * every review names its performer and verdict.
Sources in another repository are checked only when that repository is given with
`--repo NAME=DIR`; otherwise they are reported as SKIPPED and do not fail the run.
This is a custody check. It certifies no mathematics and no Layer A property.
Exit 0 on success, 1 on any mismatch, 2 on a usage error.
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys

TAXONOMY = ('Proved', 'Proved under assumptions', 'Conditional', 'Conjectural', 'Refuted')
HERE = os.path.dirname(os.path.abspath(__file__))


def git(repo_dir, *args):
    return subprocess.run(['git', '-C', repo_dir, *args], capture_output=True, check=False)


def check_source(key, src, repos, out):
    repo_dir = repos.get(src['repo'])
    if repo_dir is None:
        out.append('SKIPPED %s: repository %s not given' % (key, src['repo']))
        return True
    blob = git(repo_dir, 'cat-file', 'blob', src['blob'])
    if blob.returncode != 0:
        out.append('FAIL %s: blob %s not found in %s' % (key, src['blob'], src['repo']))
        return False
    data = blob.stdout
    ok = True
    if len(data) != src['bytes']:
        out.append('FAIL %s: %d bytes, recorded %d' % (key, len(data), src['bytes']))
        ok = False
    digest = hashlib.sha256(data).hexdigest()
    if digest != src['sha256']:
        out.append('FAIL %s: sha256 %s, recorded %s' % (key, digest, src['sha256']))
        ok = False
    have_commit = git(repo_dir, 'cat-file', '-e', src['commit'] + '^{commit}').returncode == 0
    if not have_commit:
        out.append('NOTE %s: commit %s not available locally; blob checked by identity only'
                   % (key, src['commit'][:12]))
    else:
        at = git(repo_dir, 'rev-parse', '--verify', '--quiet', '%s:%s' % (src['commit'], src['path']))
        if at.returncode != 0:
            out.append('FAIL %s: path %s does not exist at commit %s' % (key, src['path'], src['commit'][:12]))
            ok = False
        elif at.stdout.decode().strip() != src['blob']:
            out.append('FAIL %s: %s:%s is blob %s, recorded %s'
                       % (key, src['commit'][:12], src['path'], at.stdout.decode().strip(), src['blob']))
            ok = False
    if ok:
        out.append('OK %s %s %d %s' % (key, src['blob'][:12], src['bytes'], src['path']))
    return ok


def check_structure(doc, out):
    ok = True
    sources, reviews, claims = doc['sources'], doc['reviews'], doc['claims']
    ids = [c['id'] for c in claims]
    status_of = {c['id']: c['status'] for c in claims}
    if len(set(ids)) != len(ids):
        out.append('FAIL duplicate claim ids')
        ok = False
    for key, rev in reviews.items():
        for field in ('performer', 'verdict', 'record'):
            if not rev.get(field):
                out.append('FAIL review %s lacks %s' % (key, field))
                ok = False
    for c in claims:
        if c['status'] not in TAXONOMY:
            out.append('FAIL %s: status %r not in taxonomy' % (c['id'], c['status']))
            ok = False
        if not c.get('sources'):
            out.append('FAIL %s: no source' % c['id'])
            ok = False
        for s in c.get('sources', ()):
            if s not in sources:
                out.append('FAIL %s: unknown source %s' % (c['id'], s))
                ok = False
        for r in c.get('reviews', ()):
            if r not in reviews:
                out.append('FAIL %s: unknown review %s' % (c['id'], r))
                ok = False
        for d in c.get('depends_on', ()):
            if d not in ids:
                out.append('FAIL %s: depends_on unknown claim %s' % (c['id'], d))
                ok = False
            elif c['status'] == 'Proved' and status_of[d] != 'Proved':
                out.append('FAIL %s: Proved but depends on %s, which is %s' % (c['id'], d, status_of[d]))
                ok = False
        if c['status'] == 'Proved' and not (c.get('reviews') or c.get('kernel_checked')):
            out.append('FAIL %s: Proved without a nonauthor review or kernel check' % c['id'])
            ok = False
        if c['status'] == 'Conditional' and not c.get('depends_on'):
            out.append('FAIL %s: Conditional without depends_on' % c['id'])
            ok = False
    return ok


def run(claims_path, repos):
    with open(claims_path, encoding='utf-8') as fh:
        doc = json.load(fh)
    out = []
    ok = check_structure(doc, out)
    for key in sorted(doc['sources']):
        ok = check_source(key, doc['sources'][key], repos, out) and ok
    out.append('RESULT %s: %d claims, %d sources, %d reviews'
               % ('PASS' if ok else 'FAIL', len(doc['claims']), len(doc['sources']), len(doc['reviews'])))
    return ok, out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--claims', default=os.path.join(HERE, 'CLAIMS.json'))
    ap.add_argument('--repo', action='append', default=[], metavar='NAME=DIR',
                    help='repository checkout for sources of that repo (default: Math-=this checkout)')
    args = ap.parse_args(argv)
    repos = {'Math-': os.path.abspath(os.path.join(HERE, '..', '..'))}
    for item in args.repo:
        name, _, path = item.partition('=')
        if not name or not path:
            ap.error('--repo expects NAME=DIR')
        repos[name] = path
    try:
        ok, out = run(args.claims, repos)
    except (OSError, ValueError, KeyError) as exc:
        print('check_claims error: %s' % exc, file=sys.stderr)
        return 2
    print('\n'.join(out))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
